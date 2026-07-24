---
type: playbook-note
project: unDolphin
operator: artificer
agent(s): alchemist.Segovia
created: 2026-07-21
updated: 2026-07-21
release_status: draft
CAN_status: live
tags: [undolphin, playbook, undolphin_playbook, queue]
---

# The open build queue

## Next-pass / cleanup riders (2026-07-21 evening, the overlap snag)

Two alchemists worked this lab the same day without seeing each other (Segovia held the
morning hand-off; Haldir worked it mid-day unaware). Merged state verified mostly
benign — app answers, seed-image path intact, models.json holds the img-capability
form — but three riders for the next pass:

1. ~~**Restart drift**~~ **CLOSED 2026-07-22**: the running process now carries the
   reroute code (someone restarted post-edit); /gallery serves from the store OUTPUT,
   confirmed live. The ghost-render mystery (Dylan's images invisible in the UI)
   resolved as TWO gaps at once: his files landed in the retired CODE gallery via
   direct writes, with no session.jsonl rows. Fix executed: four Dylan renders moved
   to the store OUTPUT, session rows backfilled (model "agent-direct"), UI now shows
   them; the CODE gallery dir removed so the old location can't collect strays again.
   Residual rule: agents rendering DIRECT (not via /api/generate) must write to the
   store OUTPUT and append a session row — or better, just use the API.
2. **AIR ID reconciliation**: Haldir's session updated AIR IDs somewhere; the live
   models.json carries the original four. Diff his savepoint/handoff record against
   the registry before the catalog pass, so no model silently routes wrong.
3. **One-lab-one-holder**: the SIGNIN ledger exists exactly for this — sign in before
   working the lab, read who holds it. The overlap = the operator's #cleanup/#nextpass
   snag of record.

The operator's stated iterative model: good first run, then passes. Original queue from 2026-07-21, updated 2026-07-24 with the bow pass:

1. ~~**Full Runware catalog**~~ **CLOSED 2026-07-24** — the CATALOG search + AIR-direct generation ship the whole library ([[the-full-catalog]]).
2. ~~**HF relic cleanup**~~ **CLOSED** — the "HF credits" cost line reads "Runware"; app.py/run.ps1 headers name Runware.
3. **Design-reference pass** — apply the collected reference corpus ([[design-with-the-code|design with the code]]) to the surface. STILL OPEN.
4. ~~**Gallery / Workbench views**~~ **CLOSED 2026-07-24** — the GALLERY tab with masonry, tags, search, curation ([[the-gallery-surface]]).
5. **LoRA horizon** — Runware exposes LoRA-training endpoints; the operator's own-LoRA vision waits on a settled catalog first. STILL OPEN.

## Shipped 2026-07-24 (the tweak session + bow)
- Delete-from-UI (soft, to OUTPUT/TRASH); true masonry gallery; GALLERY view + multi-tag
  AND filter + search; hover action bar (reuse/download) + group select + META toggle;
  **authorship/bylines** with author filter ([[authorship-and-bylines]]); full Runware
  catalog + AIR-direct gen + live balance ([[the-full-catalog]]).
- All at PARITY on the forge (`labs/undolphin`), verified by the parity tool per commit.

## Still open
- Design-reference pass (queue 3); LoRA horizon (queue 5); the phase-2 unMemory tie-in
  (author filter → identity crosswalk cross-query).

Done and verified (earlier): backend on Runware, vault-pulled key, four models live, real per-image cost, session gallery + saved configs, mockup in DESIGN. **2026-07-21: seed/reference images** — `/api/upload` → `seedImage`, per-model `img`/`imgMax`, drag-drop reference section, verified end-to-end.

Related: [[the-runware-backend|The Runware backend]] · [[the-model-registry|The model registry]]
