---
id: db-platform-20260526
type: dev-brief
title: "Dev brief — MARA platform: judges app, clustering, UX, live updates, AI assistant (+ ZK roadmap candidate)"
date: 2026-05-26
language: en
summary: "Six feature candidates surfaced in the 2026-05-26 strategy session (1-5 functional, 6 nice-to-have visual), plus ZK proofs flagged as architecture roadmap candidate. Each item scoped with what/why/open questions/rough estimate. Five decisions needed from Ale Della Rocca."
people:
  - "Alessandro Della Rocca"
  - "Alessandro Pio Alvigi"
companies:
  - "MARA"
mara_projects:
  - "MARA platform roadmap"
  - "Judges web app"
  - "Challenge clustering"
  - "ZK proofs (architecture candidate)"
source_notes:
  - "Strategy session notes 2026-05-26 (chat paste batch 2)"
sources_used:
  - "mara-context: identity, milestones, product"
discrepancies_flagged: false
iteration_count: 2
created_at: 2026-05-26T22:45:00Z
updated_at: 2026-05-26T23:15:00Z
---

# Dev brief — MARA platform features + ZK roadmap candidate

**Lang**: EN (default for dev briefs)

<!-- NARRATIVE_SUMMARY -->
Six feature candidates surfaced in the 2026-05-26 strategy session, each scoped at concept level — what they do, why they matter, what's unresolved, rough effort estimate. The brief organizes them so Della Rocca can prioritize without losing any of them in the noise.

The first five are functional. **Judges web app** centralizes evaluation flow currently scattered across ad-hoc channels — auth model and scoring schema are the open architecture questions. **Challenge clustering** groups challenges by theme so discovery scales as the catalog grows — axis choice (skill / vertical / partner industry) is the design decision. **UX back-arrow / navigation history** is a surface-level fix to in-app routing — small scope, real friction. **Live updates** eliminate manual reload for judges and students mid-challenge — transport choice (WebSocket / SSE / polling) is the technical call. **AI assistant for presentation analysis** has *enormous scope variance* depending on target audience — same feature description means 3 days of work for one interpretation and 6+ weeks for another, so the target question must be answered first.

The sixth item — **life roadmap graphic timeline** on student profiles — is explicitly nice-to-have, not sprint material. Aligns with the "credential beats CV" narrative but doesn't block anything.

The **architecture candidate** is ZK proofs in the SBT pipeline — privacy-preserving credentials that let students prove challenge completion without revealing scoring details. **Not a sprint item**: roadmap decision needed (keep on Q3 2026 evaluation, or push further out).

Five decisions are flagged for Della Rocca: priority ranking of features 1-5, AI assistant target audience, ZK proofs roadmap slot, capacity check against Lux Collective load, and clustering axis choice. The brief is input for the next planning round — nothing here is committed.
<!-- /NARRATIVE_SUMMARY -->

## Context

Five feature candidates surfaced in the 2026-05-26 strategy session. Each is concept-level — this brief organizes them with what / why / open scope so you can prioritize without losing them. One architecture-candidate (ZK proofs) is flagged separately as roadmap, not sprint. Nothing here is committed — input for the next planning round.

---

## 1. Judges web app

**What**: A dedicated web app for challenge judges (the people evaluating submissions), separate from the main student/partner platform.

**Why**: Today judges receive submissions through ad-hoc channels (shared docs, email, partner-side). A dedicated app centralizes the evaluation flow, makes scoring consistent across challenges, and produces structured data (scores, comments, time-to-decision) we can use in the partner KPI pitch.

**Open questions**:
- Auth model: judges as platform users, or per-challenge invite link?
- Scoring schema: numeric / rubric / qualitative?
- Cross-challenge access (benchmarking) or sandboxed per challenge?
- Output: PDF report per challenge / real-time leaderboard / both?

**Rough scope**: 2–3 weeks for v1 if it's a thin wrapper on existing submission data.

---

## 2. Challenge clustering

**What**: Group challenges into clusters so students and partners can navigate by theme.

**Why**: The catalog will grow — without clustering, discovery gets painful. Also enables partner-side filtering ("all engineering hiring challenges") and student affinity filtering ("design / comms challenges").

**Open questions**:
- Cluster axis: skill / vertical / partner industry / hiring focus? (probably multiple axes)
- Multi-cluster allowed per challenge?
- Manual tagging vs auto-tagging from existing metadata?

**Rough scope**: ~1 week for taxonomy + DB schema + admin tagging UI; +1 week for filter UI on student/partner side.

---

## 3. UX: back arrow / navigation history

**What**: Add an in-app "back" arrow so users return to the previous view without using browser back.

**Why**: Surfaced as a friction point. Standard SPA pattern — keeps state in-app instead of relying on browser history.

**Open questions**:
- Specific flows: challenge detail → list, submission → challenge, profile → home, all of them?
- App-wide history stack or per-screen?

**Rough scope**: 2–3 days if routing is clean; longer if state needs to be threaded.

---

## 4. Live updates (no page reload)

**What**: Reflect server-side changes on the page in real time, no manual reload.

**Why**: Reload after submission/edit/comment disrupts flow. Most relevant for judges (live scoring) and for students checking submission status mid-challenge.

**Open questions**:
- WebSocket / SSE / polling?
- Scope: just submissions + scores, or platform-wide?
- Optimistic UI vs server-confirmed updates?

**Rough scope**: 1–2 weeks depending on backend support and chosen transport.

---

## 5. AI assistant — presentation analysis

**What**: An AI assistant that analyzes presentations and gives structured feedback. **Target presentations not yet defined** (see open questions).

**Why**: If applied to student final presentations → accelerates judge workload + gives students a pre-submission feedback loop. If applied to MARA pitch decks → internal content review tool. Very different feature depending on target.

**Open questions (critical — scope is undefined)**:
- **Target**: student submissions / MARA pitch decks / partner pitch reviews / something else?
- **Output**: rubric scoring / written feedback / both?
- **Trigger**: on-upload / on-demand / scheduled?
- **Model**: hosted (OpenAI/Anthropic) or self-host?
- **Privacy**: who sees the AI feedback — student only, judge only, both?

**Rough scope**: 3 days (thin wrapper on hosted LLM with a fixed prompt) → 6+ weeks (custom rubric model + multi-stakeholder UX). Answer the target question first; everything else follows.

---

## 6. Life roadmap — graphic timeline (nice-to-have)

**What**: A graphical timeline view on the student profile showing completed MARA challenges + SBT credentials + key milestones as a horizontal/vertical roadmap. Alternative visual layout to the standard CV-style list.

**Why**: Aligns with the "credential beats CV" narrative — the profile feels more like a portfolio journey than a résumé. Pure UI feature, no positioning push needed.

**Open questions**:
- Scope: MARA challenges only, or also external/self-declared experiences (with disclaimer)?
- Render: chronological / clustered by skill / branching?
- Sharing: public link mode (read-only) or login-only?
- Default view: timeline first or list first (toggle)?

**Rough scope**: 4–6 days for a basic horizontal timeline reading existing SBT + challenge data; longer if external experiences and sharing modes are added.

**Priority**: nice-to-have. Not blocking, not part of the next sprint unless capacity allows.

---

## Architecture candidate — ZK proofs

**What**: Zero-knowledge proofs integrated into the SBT credential pipeline on Polygon.

**Why** (context, not for sprint): privacy-preserving credentials let a student prove they completed challenge X without revealing scoring details or partner data. Aligns with the "credential beats CV" narrative and is a meaningful differentiator vs traditional credentials.

**Architectural impact**:
- Affects SBT issuance pipeline (Polygon).
- Library candidates: Semaphore / Aztec / circom — to evaluate.
- Off-chain proof generation vs on-chain verification cost tradeoff.

**Open questions**:
- Privacy of what exactly: completion-only / score-hidden / partner-hidden / all of the above?
- Verifier audience: hiring partners / public / both?
- Timeline urgency: eval now (Q3 2026) or roadmap further out?

**Note**: this is **not** a sprint item. Decision needed: roadmap slot or not.

---

## Domande a cui dobbiamo rispondere

Five product/architecture decisions that the team needs to take before the next sprint planning. They are blockers, not preferences — each unanswered question delays a feature.

- **Priority ranking of features 1–5** — which feature ships first this sprint? Without ranking, capacity gets fragmented across five fronts.
- **AI assistant target audience** — which presentations does the assistant analyze? Student final submissions, MARA pitch decks, partner pitch reviews? This is the biggest scope variance in the whole brief; same description means 3 days of work for one answer and 6+ weeks for another. Answer this first.
- **ZK proofs roadmap slot** — keep on Q3 2026 evaluation timeline, or push further out? The decision impacts how much research bandwidth gets allocated this quarter.
- **Capacity vs Lux Collective load** — does anything in features 1–5 fit before the Lux challenge closes (21 April 2026)? Lux is the priority commitment; new dev work must respect that envelope.
- **Clustering axis choice** — decide the taxonomy now as a single source of truth, or prototype with one axis and iterate? Both have valid trade-offs — committing now lowers rework risk, prototyping lowers commitment risk.

---

## Parked elsewhere

- **Penetration testing / ethical hacking** — surfaced in the same strategy session with zero scope attached. Parked in `~/Desktop/MARA.notes/note-generiche.md` until clarified. If this turns out to be a security audit request for the platform, will be surfaced back as a separate item.

## Fonti

[¹] Strategy session notes 2026-05-26 (chat paste, intake batch 2).
