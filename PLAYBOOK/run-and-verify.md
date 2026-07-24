---
type: playbook-note
project: unDolphin
operator: artificer
agent(s): alchemist.Segovia
created: 2026-07-21
updated: 2026-07-21
release_status: draft
CAN_status: live
tags: [undolphin, playbook, undolphin_playbook, runbook]
---

# Run and verify

**Run**: `CODE\run.ps1` — sets the working dir and starts `python app.py` on `127.0.0.1:8790`. Requires `VAULT_URL` + `VAULT_KEY` in the environment (the Runware key pulls from the vault at boot; openVault locked → generation fails until the operator authenticates). Then open `http://127.0.0.1:8790`.

**Verify** (state over story):
- `GET /api/models` returns 200 with the registry → app up.
- Fire a 1-image FLUX Schnell render → a new PNG lands in `CODE\gallery\` and a row appends to `CODE\state\session.jsonl` with a real seed + cost.

**Where state lives**:
- `CODE\gallery\` — every rendered PNG, named `<unix>_<hex>.png`.
- `CODE\state\session.jsonl` — one JSON row per render (prompt, model, seed, size, steps, cost, ts). The UI's session grid reads the last 60.
- `CODE\state\configs.json` — saved prompt/model presets.

Gallery and state count as operator product — never clean them as build debris.

**Agents rendering through the API SIGN THEIR WORK**: pass `"author": "<your nomen>"`
in the `/api/generate` body. The browser UI signs as `operator` by default. Authorship
rides the session record, shows in META strips and detail views, and filters the
gallery (`/api/session?all=1&author=<nomen>`, vocabulary at `/api/authors`). Direct
writes bypassing the API break the record — use the API.

Related: [[what-undolphin-is|What unDolphin is]]
