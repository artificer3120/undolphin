---
type: playbook-note
project: unDolphin
operator: artificer
agent(s): alchemist.Segovia
created: 2026-07-24
updated: 2026-07-24
release_status: draft
CAN_status: live
tags: [undolphin, playbook, undolphin_playbook, authorship, cms]
---

# Authorship and bylines

Every render carries an author. Agents rendering through the API pass
`"author": "<nomen>"` in the `/api/generate` body; the browser UI omits it and signs
as `operator`. The byline rides the session record, shows in META strips (`@nomen`) and
both detail views, and filters the gallery: `?author=<nomen>`, vocabulary at
`/api/authors`.

Why it exists (the operator's CMS instinct): the render record already behaves like a
content store; authorship gives it bylines, so "who made what" resolves at a glance and,
later, joins unMemory — "everything Dylan rendered the week of the paintblind" becomes
one cross-system query once the identity crosswalk lands.

The rule this puts on agents: direct-to-provider renders (bypassing `/api/generate`)
break the byline AND the gallery record — Dylan's original strays proved it. Render
through the API, or the work goes unsigned and invisible.

Related: [[the-gallery-surface|The gallery surface]]
