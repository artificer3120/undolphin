---
type: playbook-note
project: unDolphin
operator: artificer
agent(s): alchemist.Segovia
created: 2026-07-21
updated: 2026-07-21
release_status: draft
CAN_status: live
tags: [undolphin, playbook, undolphin_playbook, definition]
---

# What unDolphin is

unDolphin is the local image-generation app — the image successor in the dolphin lineage, run local-first until the webmaster path settles. A thin Flask server on `127.0.0.1:8790` serves a single-page UI and routes generation to a real provider.

The load-bearing design decision: **the UI never changes when the backend provider changes.** Provider #1 shipped as HuggingFace, got swapped for [[the-runware-backend|Runware]] the same night; ComfyUI on a GPU node (picass0 / OCI) can slot in later behind the same `/api/generate` contract.

What the surface does today: model picker, prompt + optional negative, aspect-ratio chips, steps + image-count sliders, saved configs, a session gallery with a detail modal (seed, cost, reuse-settings, download).

Code: `LAB 70 - unDolphin\CODE\` (app.py, models.json, run.ps1, static/index.html). Design: [[design-with-the-code|the DESIGN folder]].

Related: [[the-model-registry|The model registry]] · [[run-and-verify|Run and verify]]
