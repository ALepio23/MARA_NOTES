#!/usr/bin/env python3
"""
sync.py — MARA.notes viewer sync + encrypted payload generator.

Reads all .md files in the repo root, rebuilds index.json, encrypts the INDEX
payload with the password stored at ~/.config/mara-notes-pass (never committed),
and updates index.html with the encrypted blob.

The viewer (index.html) shows a password gate. On submit, the browser uses
Web Crypto API (PBKDF2-HMAC-SHA256 + AES-GCM) to derive the key and decrypt
the embedded payload entirely client-side. Without the password, the JSON
payload is genuinely unreadable.

Run after adding/editing any .md file in this directory:
    python3 sync.py
Then:
    git add . && git commit -m "update notes" && git push
"""

import os, sys, re, json, base64, secrets, pathlib
from datetime import datetime, timezone
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import hashlib

ROOT = pathlib.Path(__file__).parent.resolve()
INDEX_JSON = ROOT / "index.json"
INDEX_HTML = ROOT / "index.html"
PASS_FILE = pathlib.Path.home() / ".config" / "mara-notes-pass"

PBKDF2_ITERS = 200_000
SALT_LEN = 16
IV_LEN = 12

GATE_CSS = """
/* === GATE OVERLAY === */
.gate-overlay {
  position: fixed; inset: 0;
  background: #fafaf9;
  z-index: 9999;
  display: flex; align-items: center; justify-content: center;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}
.gate-card {
  max-width: 360px; width: 90%;
  padding: 32px 28px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 24px rgba(0,0,0,0.08);
  display: flex; flex-direction: column; gap: 12px;
}
.gate-title { font-size: 20px; font-weight: 600; }
.gate-sub { font-size: 13px; color: #666; margin-bottom: 8px; }
.gate-card input { padding: 10px 12px; border: 1px solid #ddd; border-radius: 8px; font: inherit; }
.gate-card input:focus { outline: 2px solid #111; outline-offset: 0; }
.gate-card button { padding: 10px; background: #111; color: white; border: 0; border-radius: 8px; cursor: pointer; font: inherit; }
.gate-card button:hover { background: #333; }
.gate-error { color: #c00; font-size: 13px; }
body.locked > *:not(.gate-overlay) { display: none !important; }
"""

GATE_HTML = """
<div class="gate-overlay" id="gateOverlay">
  <div class="gate-card">
    <div class="gate-title">MARA.notes</div>
    <div class="gate-sub">Inserisci la password per sbloccare il viewer.</div>
    <input type="password" id="gatePassword" autofocus placeholder="Password" />
    <button id="gateUnlock">Sblocca</button>
    <div class="gate-error" id="gateError" hidden>Password errata. Riprova.</div>
  </div>
</div>
"""

GATE_SCRIPT_TEMPLATE = """
<script>
const ENC_PAYLOAD = __ENC_PAYLOAD__;

async function _maraDecrypt(password) {
  const enc = new TextEncoder();
  const dec = new TextDecoder();
  const fromB64 = s => Uint8Array.from(atob(s), c => c.charCodeAt(0));
  const salt = fromB64(ENC_PAYLOAD.salt);
  const iv = fromB64(ENC_PAYLOAD.iv);
  const data = fromB64(ENC_PAYLOAD.data);
  const km = await crypto.subtle.importKey("raw", enc.encode(password), "PBKDF2", false, ["deriveKey"]);
  const key = await crypto.subtle.deriveKey(
    { name: "PBKDF2", salt, iterations: __PBKDF2_ITERS__, hash: "SHA-256" },
    km,
    { name: "AES-GCM", length: 256 },
    false,
    ["decrypt"]
  );
  const plain = await crypto.subtle.decrypt({ name: "AES-GCM", iv }, key, data);
  return JSON.parse(dec.decode(plain));
}

async function _maraUnlock() {
  const pw = document.getElementById('gatePassword').value;
  const errEl = document.getElementById('gateError');
  errEl.hidden = true;
  try {
    const idx = await _maraDecrypt(pw);
    window.MARA_INDEX = idx;
    document.getElementById('gateOverlay').remove();
    document.body.classList.remove('locked');
    startMaraApp();
  } catch (e) {
    errEl.hidden = false;
  }
}

document.getElementById('gateUnlock').addEventListener('click', _maraUnlock);
document.getElementById('gatePassword').addEventListener('keydown', e => {
  if (e.key === 'Enter') _maraUnlock();
});
</script>
"""


def parse_fm(fm: str) -> dict:
    out = {}
    cur_key = None
    for line in fm.split("\n"):
        if not line.strip():
            continue
        if line.startswith("  - "):
            out.setdefault(cur_key, [])
            if isinstance(out[cur_key], list):
                out[cur_key].append(line[4:].strip().strip('"'))
        elif ":" in line:
            k, _, v = line.partition(":")
            k = k.strip()
            v = v.strip()
            if v == "":
                out[k] = []
                cur_key = k
            else:
                out[k] = v.strip('"')
                cur_key = k
    return out


def load_doc(md_path):
    raw = md_path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", raw, re.DOTALL)
    if not m:
        return None
    fm_raw, body_md = m.group(1), m.group(2).lstrip("\n")
    fm = parse_fm(fm_raw)
    if "id" not in fm or "type" not in fm:
        return None
    return {
        "id": fm["id"],
        "type": fm["type"],
        "title": fm.get("title", md_path.stem),
        "date": fm.get("date", ""),
        "language": fm.get("language", "it"),
        "summary": fm.get("summary", ""),
        "people": fm.get("people", []),
        "companies": fm.get("companies", []),
        "mara_projects": fm.get("mara_projects", []),
        "source_notes": fm.get("source_notes", []),
        "sources_used": fm.get("sources_used", []),
        "discrepancies_flagged": str(fm.get("discrepancies_flagged", "false")).lower() == "true",
        "iteration_count": int(fm.get("iteration_count", "1") or 1),
        "created_at": fm.get("created_at", ""),
        "updated_at": fm.get("updated_at", ""),
        "filename": md_path.name,
        "filepath": str(md_path),
        "body_md": body_md,
    }


def build_index() -> dict:
    docs = []
    for p in sorted(ROOT.glob("*.md")):
        d = load_doc(p)
        if d:
            docs.append(d)
    docs.sort(key=lambda d: d.get("date", ""), reverse=True)
    return {"version": 1, "docs": docs}


def encrypt_index(idx: dict, password: str) -> dict:
    salt = secrets.token_bytes(SALT_LEN)
    iv = secrets.token_bytes(IV_LEN)
    key = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, PBKDF2_ITERS, dklen=32)
    aesgcm = AESGCM(key)
    plaintext = json.dumps(idx, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    ciphertext = aesgcm.encrypt(iv, plaintext, None)
    return {
        "salt": base64.b64encode(salt).decode("ascii"),
        "iv": base64.b64encode(iv).decode("ascii"),
        "data": base64.b64encode(ciphertext).decode("ascii"),
    }


def refactor_html_once(html: str) -> str:
    """One-time refactor of the original viewer to add gate UI + decrypt logic.
    Idempotent: detects the gate marker and skips if already refactored."""
    if "_maraDecrypt" in html:
        return html

    # 1. Add CSS at end of <style>
    html = html.replace("</style>", GATE_CSS + "</style>", 1)

    # 2. Add class="locked" to <body>
    html = re.sub(r"<body([^>]*)>", lambda m: f"<body{m.group(1)} class=\"locked\">", html, count=1)

    # 3. Insert gate UI right after <body...>
    html = re.sub(
        r"(<body[^>]*>)",
        lambda m: m.group(1) + "\n" + GATE_HTML.strip() + "\n",
        html,
        count=1,
    )

    # 4. Refactor IIFE: (function() { ... })();  →  function startMaraApp() { ... }
    # Find the IIFE open
    html = re.sub(r"\(function\(\) \{", "function startMaraApp() {", html, count=1)
    # Replace the closing })();  with }
    # Match the LAST )();\n</script> before EOF
    html = re.sub(r"\}\)\(\);\s*</script>", "}\n</script>", html, count=1)

    # 5. Replace const INDEX = {...big inline JSON...}; with placeholder
    # Use the robust boundary: next line is "  const docs = "
    html = re.sub(
        r"const INDEX = .+?;\s*\n(\s*const docs = )",
        "const INDEX = window.MARA_INDEX || {version: 1, docs: []};\n" + r"\1",
        html,
        flags=re.DOTALL,
        count=1,
    )

    # 6. Append gate decrypt script just before </body>
    gate_script = GATE_SCRIPT_TEMPLATE.replace("__PBKDF2_ITERS__", str(PBKDF2_ITERS))
    html = html.replace("</body>", gate_script + "\n</body>", 1)

    return html


def update_payload(html: str, payload: dict) -> str:
    """Replace the ENC_PAYLOAD literal with new encrypted data."""
    payload_js = json.dumps(payload, ensure_ascii=True)
    # Try exact placeholder first (initial refactor)
    if "__ENC_PAYLOAD__" in html:
        return html.replace("__ENC_PAYLOAD__", payload_js, 1)
    # Otherwise replace existing ENC_PAYLOAD assignment
    return re.sub(
        r"const ENC_PAYLOAD = .+?;",
        f"const ENC_PAYLOAD = {payload_js};",
        html,
        count=1,
        flags=re.DOTALL,
    )


def main():
    if not PASS_FILE.exists():
        print(f"ERROR: password file not found at {PASS_FILE}", file=sys.stderr)
        print("Create it with: printf 'your-password' > ~/.config/mara-notes-pass && chmod 600 ~/.config/mara-notes-pass", file=sys.stderr)
        sys.exit(1)
    password = PASS_FILE.read_text(encoding="utf-8").strip("\n\r")
    if not password:
        print(f"ERROR: password file at {PASS_FILE} is empty", file=sys.stderr)
        sys.exit(1)

    # 1. Build index from .md files
    idx = build_index()
    INDEX_JSON.write_text(json.dumps(idx, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"index.json: {len(idx['docs'])} docs")

    # 2. Encrypt
    payload = encrypt_index(idx, password)
    print(f"encrypted payload: salt={len(base64.b64decode(payload['salt']))}B, iv={len(base64.b64decode(payload['iv']))}B, data={len(base64.b64decode(payload['data']))}B")

    # 3. Read HTML, refactor if needed, inject payload
    if not INDEX_HTML.exists():
        print(f"ERROR: {INDEX_HTML} not found", file=sys.stderr)
        sys.exit(1)
    html = INDEX_HTML.read_text(encoding="utf-8")
    refactored = refactor_html_once(html)
    final = update_payload(refactored, payload)
    INDEX_HTML.write_text(final, encoding="utf-8")
    print(f"index.html: written ({len(final)} chars)")
    print(f"  gate active: {'_maraDecrypt' in final}")
    print(f"  payload size: {len(json.dumps(payload))} chars")


if __name__ == "__main__":
    main()
