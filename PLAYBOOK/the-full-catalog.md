---
type: playbook-note
project: unDolphin
operator: artificer
agent(s): alchemist.Segovia
created: 2026-07-24
updated: 2026-07-24
release_status: draft
CAN_status: live
tags: [undolphin, playbook, undolphin_playbook, catalog, runware]
---

# The full Runware catalog

Beyond the four curated registry models ([[the-model-registry]]), the whole Runware
library answers by search. The rail's CATALOG box hits `/api/catalog?q=` (a proxy over
Runware's `modelSearch` task) — returns name, AIR id, category, and an img2img badge
where the model takes references. Click a result and it becomes the active model.

**AIR-direct generation**: a catalog model needs no registry entry. `/api/generate`
accepts `air` + `model_name` + `img` directly and generates straight off the AIR id,
registry-free. Cost returns real per render; catalog models with no fixed price bill
what Runware reports.

**Live balance**: the topbar shows `BAL $x.xxx`, pulled via `/api/balance`
(accountManagement.getDetails, number only — the response also carries team + key
metadata the UI never exposes). Refreshes after every render. An empty balance fails
generation with the provider's insufficient-funds error and nothing else — every prior
render stays on disk, the whole gallery/tag/search/byline surface keeps working; only
the Generate button goes quiet.

Related: [[the-model-registry|The model registry]] · [[the-runware-backend|The Runware backend]]
