---
id: db-platform-20260526
type: dev-brief
title: "Dev brief — MARA platform: judges app, clustering, UX, live updates, AI assistant (+ ZK roadmap candidate)"
date: 2026-05-26
language: it
summary: "Sei candidati feature emersi dalla sessione strategica del 26 maggio 2026 (1-5 funzionali, 6 nice-to-have visivo), più ZK proofs flaggati come candidato architettura roadmap. Ogni voce con cosa è / perché / domande aperte / scope rough. Cinque decisioni del team prima dello sprint successivo."
headline: "6 feature platform + ZK proofs roadmap candidate. 5 decisioni di prodotto/architettura da prendere prima dello sprint"
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

<!-- NARRATIVE_SUMMARY -->
Sei feature candidate uscite dalla sessione strategica del 26 maggio. Cinque funzionali, una nice-to-have visiva, più un candidato architettura (ZK proofs) che è roadmap non sprint. Brief organizzato per concept level: cosa è, perché serve, cosa è ancora aperto, rough estimate.

**Le funzionali in due righe**: Judges web app centralizza la valutazione che oggi gira tra mail, doc condivisi e canali partner. Clustering raggruppa le challenge per tema così lo scroll della lista non diventa doloroso quando il catalogo cresce. UX back-arrow è un fix piccolo di routing in-app — sproporzionato il valore vs la complessità. Live updates eliminano il reload manuale (importante soprattutto per i giudici durante la valutazione). AI assistant per analisi presentazioni è quella con varianza scope enorme — stesso name, 3 giorni di lavoro o 6 settimane a seconda di come la interpretiamo. Va deciso il target prima di tutto il resto.

**Architettura roadmap (ZK proofs)**: credenziali con privacy on-chain per dimostrare il completamento di una challenge senza esporre score o dati partner. Non per sprint corrente — decisione roadmap: lo teniamo nella Q3 2026 eval o lo spostiamo più avanti?

Cinque decisioni di prodotto/architettura da prendere insieme prima del prossimo sprint planning. Sono blocker, non preferenze — ogni domanda non risposta sposta una feature.
<!-- /NARRATIVE_SUMMARY -->

## Contesto

Sessione strategica del 26 maggio 2026. Sono emerse sei feature candidate per la piattaforma e un candidato architettura (ZK proofs). Tutto a livello concept — niente è committato, è materiale per il prossimo planning round.

Questo brief le organizza con la stessa struttura per ognuna: cosa è, perché serve, cosa è ancora aperto, rough scope. L'obiettivo è poterle prioritizzare senza perdere nessuna nel rumore.

## Elaborazione

Le feature 1-5 sono funzionali e si misurano. La 6 è nice-to-have visiva. Le ZK proofs sono architettura — decisione di roadmap, non di sprint.

L'AI assistant (feature 5) è quella con la varianza di scope più grossa di tutto il brief: lo stesso nome può significare 3 giorni di lavoro (wrapper su LLM hosted con prompt fisso) o 6+ settimane (modello rubric custom + UX multi-stakeholder). Va deciso il target *prima* di tutto il resto — altrimenti il pianificamento è inutile.

L'architettura candidate (ZK proofs) si allinea bene alla narrativa "credenziali on-chain con privacy" che il deep-dive recruiter¹ tira fuori come potenziale differentiator vs credenziali tradizionali. Ma è ricerca, non sprint. Il punto è decidere se nei prossimi 90 giorni mettiamo bandwidth di ricerca su questo o no.

Capacity reale: la challenge Lux Collective è la priority commitment in corso². Tutto il dev nuovo deve respect quell'envelope finché Lux non chiude (era 21 aprile 2026 — verificare se ancora aperto). Vale la pena vedere se qualcuna delle feature 1-5 ci sta dentro prima del wrap-up.

## Brainstorming — le sei feature

### 1. Judges web app

**Cosa è**: web app dedicata per i giudici delle challenge (chi valuta le submission), separata dalla piattaforma principale studenti/partner.

**Perché**: oggi i giudici ricevono le submission un po' a casaccio (mail, doc condivisi, lato partner). Una app dedicata centralizza il flusso di valutazione, rende lo scoring consistente tra challenge, e produce dati strutturati (score, commenti, time-to-decision) che usiamo nel pitch KPI verso i partner.

**Cosa è ancora aperto**:
- Auth model: giudici come utenti della piattaforma o invite link per-challenge?
- Schema di scoring: numerico, rubric, qualitativo?
- Accesso cross-challenge (per benchmark) o sandboxed per ogni challenge?
- Output finale: report PDF per challenge, leaderboard live, entrambi?

**Rough scope**: 2-3 settimane per la v1 se è un wrapper sottile sui dati submission che abbiamo già.

---

### 2. Challenge clustering

**Cosa è**: raggruppare le challenge per cluster tematici così che studenti e partner possano navigare per tema.

**Perché**: il catalogo cresce. Senza clustering la discovery diventa dolorosa man mano. Permette anche filtri lato partner ("tutte le challenge engineering hiring") e affinità lato studente ("challenge design/comms").

**Cosa è ancora aperto**:
- Asse di cluster: skill, verticale, industria del partner, focus di hiring (probabilmente assi multipli)?
- Una challenge può stare in più cluster?
- Tagging manuale vs auto-tagging dai metadati esistenti?

**Rough scope**: ~1 settimana per taxonomy + DB schema + UI di tagging admin; +1 settimana per il filter UI lato studente/partner.

---

### 3. UX: freccia indietro / cronologia in-app

**Cosa è**: pulsante "back" in-app perché l'utente torni alla vista precedente senza usare il back del browser.

**Perché**: emerso come friction point. Pattern SPA standard — tiene lo stato dentro l'app invece che appoggiarsi alla history del browser.

**Cosa è ancora aperto**:
- Quali flow specifici: challenge detail → list, submission → challenge, profile → home, tutti?
- Stack di history app-wide o per-screen?

**Rough scope**: 2-3 giorni se il routing è pulito; più tempo se serve passare stato in giro.

---

### 4. Live updates (no page reload)

**Cosa è**: riflettere i cambi server-side sulla pagina in tempo reale, senza reload manuale.

**Perché**: il reload dopo submission/edit/commento rompe il flow. Più importante per i giudici (live scoring) e per gli studenti che controllano lo stato della loro submission durante la challenge.

**Cosa è ancora aperto**:
- WebSocket, SSE, polling?
- Scope: solo submission + score, o tutta la piattaforma?
- UI ottimistica o solo conferme server-confirmed?

**Rough scope**: 1-2 settimane a seconda del supporto backend e del transport scelto.

---

### 5. AI assistant — analisi presentazioni ⚠ scope da definire

**Cosa è**: un assistente AI che analizza le presentazioni e dà feedback strutturato. **Target delle presentazioni non ancora definito** (vedi domande aperte).

**Perché**: se applicato alle presentazioni finali degli studenti → accelera il lavoro dei giudici + dà agli studenti un loop di feedback pre-submission. Se applicato ai pitch deck MARA → strumento di review interno. Feature molto diverse a seconda del target.

**Cosa è ancora aperto (critico — scope indefinito)**:
- Target: submission studenti, pitch deck MARA, review pitch partner, altro?
- Output: rubric scoring, feedback scritto, entrambi?
- Trigger: on-upload, on-demand, schedulato?
- Modello: hosted (OpenAI / Anthropic) o self-hosted?
- Privacy: chi vede il feedback AI — solo studente, solo giudice, entrambi?

**Rough scope**: 3 giorni (wrapper sottile su LLM hosted con prompt fisso) ↔ 6+ settimane (modello rubric custom + UX multi-stakeholder). **Rispondere prima al target — tutto il resto segue.**

---

### 6. Life roadmap — timeline grafica (nice-to-have)

**Cosa è**: una vista timeline grafica sul profilo studente che mostra challenge completate + SBT + milestone come una roadmap orizzontale/verticale. Layout visivo alternativo alla classica lista CV-style.

**Perché**: si allinea alla narrativa "credenziali batton il CV" — il profilo sembra più un portfolio journey che un curriculum. Feature pura di UI, non spinge nessun posizionamento nuovo.

**Cosa è ancora aperto**:
- Scope: solo challenge MARA, o anche esperienze esterne/self-declared (con disclaimer)?
- Render: cronologico, raggruppato per skill, branching?
- Sharing: link pubblico (read-only) o solo login?
- Vista default: timeline o lista (con toggle)?

**Rough scope**: 4-6 giorni per timeline orizzontale base che legge SBT + dati challenge esistenti; di più se servono esperienze esterne e modi di sharing.

**Priorità**: nice-to-have. Non blocca niente, non per il prossimo sprint a meno che non ci sia capacity extra.

---

## L'architettura candidate — ZK proofs

**Cosa è**: zero-knowledge proofs integrati nella pipeline SBT su Polygon.

**Perché** (contesto, non per sprint): credenziali privacy-preserving — lo studente prova di aver completato la challenge X senza esporre score o dati partner. Si allinea alla narrativa "credenziali batton il CV" ed è un differenziatore reale vs credenziali tradizionali.

**Impatto architetturale**:
- Tocca la pipeline di issuance SBT (Polygon).
- Library candidati: Semaphore, Aztec, circom — da valutare.
- Tradeoff: generazione proof off-chain vs verifica on-chain costs.

**Cosa è ancora aperto**:
- Privacy di cosa esattamente: solo completion, score hidden, partner hidden, tutti?
- Audience del verifier: hiring partner, pubblico, entrambi?
- Urgenza timeline: eval ora (Q3 2026) o roadmap più avanti?

**Nota**: **non** è uno sprint item. Serve solo decidere se metterlo nello slot roadmap o no.

---

## Domande a cui dobbiamo rispondere

Cinque decisioni di prodotto/architettura che il team deve prendere prima del prossimo sprint planning. Sono blocker, non preferenze — ogni domanda non risposta sposta una feature.

- **Priority ranking delle feature 1-5** — quale ship per prima nel prossimo sprint? Senza ranking, la capacity si frammenta su cinque fronti.
- **Target dell'AI assistant** — quali presentazioni analizza? Submission studenti, pitch deck MARA, review pitch partner? È la varianza scope più grossa del brief — stesso nome significa 3 giorni o 6+ settimane. **Rispondere a questa prima.**
- **Slot roadmap delle ZK proofs** — Q3 2026 eval o spingere più avanti? La decisione impatta quanta bandwidth di ricerca alloca questo trimestre.
- **Capacity vs carico Lux Collective** — qualcosa delle feature 1-5 ci sta dentro prima che Lux chiuda (era 21 aprile 2026)? Lux è la priority commitment, il dev nuovo deve respect quell'envelope.
- **Asse del clustering** — decidere ora la taxonomy come single source of truth, o prototipare con un asse e iterare? Entrambe hanno tradeoff validi — decidere ora abbassa il rework risk, prototipare abbassa il commitment risk.

---

## Parcheggiati altrove

- **Penetration testing / ethical hacking** — uscito nella stessa sessione strategica con zero scope attaccato. Parcheggiato in `~/Desktop/MARA.notes/note-generiche.md` finché non viene chiarito. Se diventa una richiesta di security audit per la piattaforma, lo riportiamo come item separato.

## Fonti

[¹] Deep-dive recruiter coexistence `2026-05-29-deep-dive-recruiter-coexistence.md` — analisi della narrativa "credenziali batton il CV" + posizionamento SBT come differenziatore.
[²] `mara-context/partners.md` — TLC challenge Lux Collective, durata 18 marzo – 21 aprile 2026, status priority commitment lato platform.
[³] Sessione strategica 2026-05-26 (note grezze, chat paste batch 2) — fonte originale delle 6 feature + ZK candidate.
