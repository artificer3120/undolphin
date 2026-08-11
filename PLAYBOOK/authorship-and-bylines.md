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

What this puts on agents: a render made outside `/api/generate` carries no byline and
never enters the gallery record — Dylan's original strays showed it. The API route buys
authorship and findability; a render made anywhere else trades both away. An agent that
renders outside the API names what it gave up and moves on.

*Scar, 2026-08-02:* this paragraph formerly closed **"Render through the API, or the work
goes unsigned and invisible,"** and downstream `/blindPaint` hardened that into **"unDolphin
API only. Direct-to-provider writes break the authorship record."** The operator ruled the
exclusivity agent-minted — he never said it, and the estate takes postures and affinity
gradients rather than prohibitions. The cost stands; the ban does not. Do not re-graft it.

Related: [[the-gallery-surface|The gallery surface]]
