---
type: playbook-note
project: unDolphin
operator: artificer
agent(s): alchemist.Segovia
created: 2026-07-21
updated: 2026-07-21
release_status: draft
CAN_status: live
tags: [undolphin, playbook, undolphin_playbook, models]
---

# The model registry

`CODE\models.json` — config on the surface, mechanism in the dumb script. The app reads it at boot; adding a model means adding one JSON object, no code change.

Each entry: `id` (UI handle), `name`, `provider`, `air` (the Runware AIR ID that actually routes), `tag` (QUALITY / FAST / SDXL badge), `price` (per image), `default_steps` / `step_max`, `sizes` (aspect-ratio chips), and the image capability pair `img` (`none / optional / style / required`) + `imgMax` — added 2026-07-21 with the seed-image feature; the UI's reference section renders from these.

The four registered today:

| id | name | tag | price |
|---|---|---|---|
| juggernaut-pro | Juggernaut Pro Flux | QUALITY | $0.006 |
| flux-schnell | FLUX Schnell | FAST | $0.0013 |
| juggernaut-lightning | Juggernaut Lightning Flux | FAST | $0.002 |
| sdxl-copax | Copax Cute XL (SDXL) | SDXL | $0.0013 |

To add one: find its AIR ID via the Runware model search, copy an existing entry, set the fields, restart. The fuller move — pulling the whole live catalog through the API — lives in [[the-open-build-queue|the open build queue]].

Related: [[the-runware-backend|The Runware backend]]
