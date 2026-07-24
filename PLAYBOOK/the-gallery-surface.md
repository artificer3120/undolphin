---
type: playbook-note
project: unDolphin
operator: artificer
agent(s): alchemist.Segovia
created: 2026-07-24
updated: 2026-07-24
release_status: draft
CAN_status: live
tags: [undolphin, playbook, undolphin_playbook, gallery, ui]
---

# The gallery surface

The SESSION | GALLERY tabs in the topbar. SESSION shows the current run's strip;
GALLERY pulls the whole history. Both render in **true masonry** — a shortest-column
packer that flows newest left-to-right into the currently-shortest column, heights
predicted from each record's stored render ratio (no DOM measuring), re-packing on
resize (4/3/2 columns responsive). Per the App2 mockup, which the first build had
flattened to cropped squares.

Curation controls, all built 2026-07-24:
- **Delete** — soft: the PNG moves to OUTPUT/TRASH, the session row drops. Two-stage
  confirm button (no browser dialogs, so agents driving the UI never wedge).
- **Tags** — a tag editor on both detail surfaces; `PUT /api/image/<id>/tags`. The
  gallery chip row shows the vocabulary with counts; chips toggle a SET with **AND**
  semantics (`?tag=a,b` narrows to images carrying all).
- **Search** — `?q=` matches prompt / tags / model, server-side over full history.
- **Hover kit** — per-tile action bar (⟲ reuse-as-prompt, ⇩ download) + a select
  checkbox; brightness/border lift on hover.
- **Group select** — a floating bar (count, DOWNLOAD staggered, DELETE two-stage,
  CLEAR) across both views.
- **META toggle** (topbar) — on, every tile carries a strip (author · model · size ·
  cost); persisted in localStorage.

Related: [[authorship-and-bylines|Authorship and bylines]] · [[run-and-verify|Run and verify]]
