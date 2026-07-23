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

The operator's stated iterative model: good first run, then passes. Open as of 2026-07-21, from his word in the build transcript:

1. **Full Runware catalog** — tap Runware's model search from the app so the UI lists the live catalog (Nano Banana, Seedream, Ideogram, Kling, …) instead of four hand-picked entries. His ask, verbatim intent: "can we just tap a runware api and get a list of all of their available models?"
2. **HF relic cleanup** — the UI cost line still says "HF credits"; run.ps1 and app.py headers still name HuggingFace as the provider. Small, but the docs lie until fixed.
3. **Design-reference pass** — apply the collected reference corpus ([[design-with-the-code|design with the code]]) to the surface.
4. **Gallery / Workbench views** — the fuller browsing surface Haldir proposed and never built.
5. **LoRA horizon** — Runware exposes LoRA-training endpoints; the operator's own-LoRA vision waits on a settled catalog first.

Done and verified (for contrast): backend on Runware, vault-pulled key, four models live, real per-image cost, session gallery + saved configs, mockup in DESIGN. **2026-07-21: seed/reference images** — `/api/upload` (file → Runware UUID), `seedImage` on the inference task, per-model `img`/`imgMax` capability, and the drag-drop reference section from the App2 mockup + animation video (v2 design, both in DESIGN\). Verified end-to-end: gallery image uploaded → UUID → img2img render landed with the ref recorded.

Related: [[the-runware-backend|The Runware backend]] · [[the-model-registry|The model registry]]
