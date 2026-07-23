---
type: playbook-note
project: unDolphin
operator: artificer
agent(s): alchemist.Segovia
created: 2026-07-21
updated: 2026-07-21
release_status: draft
CAN_status: live
tags: [undolphin, playbook, undolphin_playbook, backend, runware]
---

# The Runware backend

Generation routes through the Runware task-array API (`https://api.runware.ai/v1`). One POST, a JSON array of tasks; each task names a model by its **AIR ID** (`rundiffusion:130@100`, `runware:100@1`, `civitai:119226@140015`).

- **Credential**: `runware_api_key`, pulled once from the vault at boot (`VAULT_URL`/`VAULT_KEY` in the environment). The app fails fast at startup if the vault gate is dark. #iholdnokeys — never paste the key anywhere.
- **Cost**: Runware returns the real per-image cost in the response; the app records it per render (schnell ≈ $0.0013, Juggernaut Pro ≈ $0.006). No estimates.
- **Fallback**: some models reject `steps`/`negative`/`seed`; on error the call retries once with a stripped base task.
- **Catalog**: Runware's model search reaches far past the four registered models — Nano Banana, Seedream, Ideogram, Kling, plus LoRA-training endpoints. Wiring that catalog into the UI sits in [[the-open-build-queue|the open build queue]].

History: the first backend used HuggingFace inference (402'd on quota); Haldir swapped it for Runware 2026-07-20 and verified a real render end-to-end the same night.

Related: [[the-model-registry|The model registry]]
