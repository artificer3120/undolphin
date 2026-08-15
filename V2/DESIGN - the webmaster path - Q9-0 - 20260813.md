---
doc_type: design
authoring_agent(s): webmaster.Q9-0
created: "1786679690"
updated: "1786679690"
release_status: released
CAN_status: provisional
CAP: true
version: 1
tags:
  - design
  - undolphinv2
  - undolphin
  - surface
  - webmaster
  - dynamic
  - mediaarchive
aliases:
  - "DESIGN - the webmaster path"
  - "unDolphin V2 design"
untemplated: false
---

# DESIGN — unDolphin V2, the webmaster path

**PROVISIONAL. Nothing here has run.** Written 2026-08-13 by webmaster.Q9-0 at the operator's ask, from live readings the same hour.

**This document answers a park, not a takeover.** alchemist.Segovia's own playbook note reads: *"the local image-generation app… run local-first **until the webmaster path settles**."* That path lands on the webmaster. The engine, the model registry, the provider contract, and the UI stay the alchemist's. **What follows covers only where it runs and how it reaches the operator.**

The operator's framing, verbatim: *"undolphin is in an odd state. its local but the 'spirit' is web. that needs to live on a server. I would definitely use it."*

---

## 1. Measured state, 2026-08-13

| reading | value |
| :--- | :--- |
| answering | HTTP 200 on `127.0.0.1:8790`, 40,675 bytes |
| code | `LAB 70 - unDolphin\CODE\` — `app.py` 17 KB, `models.json`, `static/index.html` 41 KB |
| stack | Flask, single-page UI, `/api/generate` contract |
| provider | Runware task-array API, credential `runware_api_key` pulled from the vault at boot |
| renders on disk | **134 files, 48.9 MB** at `_STORES\S3120STORES\unDolphin\OUTPUT` |
| reachable by | one machine — Rocky, and only from Rocky |

The provider contract already survives a swap: HuggingFace shipped first, Runware replaced it the same night, and the UI never changed. **A move to a node changes the host, never that contract.**

## 2. Three constraints, and each one eliminates options

**It runs code.** Flask serves `/api/generate`; a request executes a program. Cloudflare Pages holds files and nothing else, so no static path reaches this. **Kind: DYNAMIC** — see [[CONCEPT - SURFACE]].

**It reaches the vault over the tailnet.** The app pulls `runware_api_key` at boot from `100.83.251.119:8120`, a CGNAT address that routes only inside the tailnet, and it **fails fast at startup when the gate reads dark**. So the process has to sit ON the tailnet. Nothing outside can host it without moving the credential, and moving the credential breaks `#iholdnokeys`.

**Every render spends real money.** Runware bills per image and the app records the true cost per render (schnell ≈ $0.0013, Juggernaut Pro ≈ $0.006 — no estimates). **A publicly reachable unDolphin with no gate reads as an open wallet.** Anyone who finds the URL spends the operator's money, at his rate, without limit.

That third constraint outranks the other two, and it names a gap in the concept doc written the same day: **CONCEPT - SURFACE lists CONFIG as one of six parts and treats auth as a detail inside it. When a stack spends money, the auth gate stands beside the COST BAND as a first-class part.** unDolphin supplies the case that proves it.

## 3. The shape

```
   operator's browser
          │  login (Cloudflare Access, free ≤50 users)
          ▼
   undolphin.<zone>                      the public NAME
          │  Cloudflare Tunnel — the node dials OUT, nothing inbound opens
          ▼
   a tailnet node running Flask          the STACK + HOST
          │  reads runware_api_key from the vault, in-tailnet, never disked
          ▼
   Runware API                           the spend
          │
          ▼
   renders → OUTPUT store → the media archive (§6)
```

**Why a tunnel rather than an open port.** The node dials out; no inbound port opens on it. The lesson already sits in Tye's OCI runbook: *"a public port 22 draws a constant brute-force flood."* A tunnel keeps the node's only exposure a connection it made itself, and it keeps the vault reach intact because the process never leaves the tailnet.

**Why Access rather than an app-level login.** The gate lands before the app, so an unauthenticated request never reaches code that can spend. An app-level login puts the spending program in front of the door.

## 4. The node

| candidate | reads |
| :--- | :--- |
| **chindi** — OCI E2.1.Micro, x86, always-free | on the tailnet, stays up, $0 permanently. **Already runs Forgejo (ungit).** |
| **spark-salmon** — OCI A1.Flex, ARM | **rejected.** Oracle reclaims idle A1 nodes; a thing wanted on demand cannot sit on reclaimable capacity |
| **questboard-ec2** — AWS | account live (`102282012894`, user `librarian`, verified 2026-08-13). Free-tier status unread |
| **a NEW E2.1.Micro** | $0, always-free, and preserves one-node-one-purpose |

**Recommendation: a new E2.1.Micro, not chindi.** chindi currently means *ungit* — the private source of record, a node claimed for one job. An image app sharing that node couples an experiment to the estate's git authority. A second always-free micro costs nothing and keeps the claiming discipline intact.

**That call belongs to the operator**, since the node-claiming design is his. Tye's runbook `RUNBOOK - stand up a new OCI free-tier node` covers the provision, with its OCI-console leg marked UNVERIFIED and never yet run end to end.

## 5. The NAME, and the one real blocker

The operator named the target: `undolphin.untitledprojects.io`.

**Measured 2026-08-13:**

```
untitledprojects.io            NS  ns63.domaincontrol.com, ns64.domaincontrol.com   (GoDaddy)
untitledprojects.io            A   3.149.50.128
neonforge.untitledprojects.io  A   100.83.251.119
undolphin.untitledprojects.io  —   no record
```

**Cloudflare Tunnel and Access both require the hostname's zone to sit on Cloudflare.** Our account holds exactly one zone, `lab3120.earth`. So `undolphin.untitledprojects.io` blocks on the nameserver migration written up at `#gymgodaddyroot` — a **nameserver change, not a registrar transfer**: free, minutes to act, reversible, and the mail records (MX, SPF, DKIM, DMARC) must land in Cloudflare *before* the cut.

**An interim exists:** `undolphin.lab3120.earth` works today, on a zone we already control, and proves the whole shape before the migration. The name can move afterward.

**Recorded rather than judged:** `neonforge.untitledprojects.io` publishes the vault host's tailnet address in public DNS. `100.64.0.0/10` does not route across the open internet, so nothing gets reached — but the address itself becomes public and DNS-history sites archive it. Publishing a tailnet IP this way reads as a known convenience trick, so this document holds it as possibly deliberate and flags it for the operator's word rather than calling it a defect.

## 6. The renders, and the archive question

The operator, same session: *"how do we preserve the media archive and make it accessible to me? I have been asking for a Pinterest clone for a while."*

**Census, 2026-08-13** (counts and sizes only; no file opened):

```
_VAULTS   673 files  1,322 MB
_DECKS    212 files    246 MB
_BASES    202 files     90 MB
                     ─────────
                     ~1.66 GB across ~1,087 files
plus  unDolphin OUTPUT   134 files, 48.9 MB
plus  7 cabin GALLERY dirs, ~33 files
S3: three buckets, none of them a media archive
```

**Preservation and access answer different questions.**

**Preservation.** 336 MB of that media sits inside `_DECKS` and `_BASES`, which run as git repos pushing to GitHub. Git handles already-compressed binaries badly — no useful delta compression, and every clone carries the full history of every image permanently. Media belongs in **object storage**. **Cloudflare R2** fits the estate's shape: 10 GB free, S3-compatible, and **zero egress fees**, so browsing costs nothing where S3 bills per byte read.

**Access — the Pinterest clone.** Masonry grid, lazy loading, tags, search: all client-side. **So the gallery lands STATIC** — Pages, no node, no 3am risk, $0.

```
media  →  R2 (durable, zero-egress, private)
             ↓  manifest generated at publish: filename, dimensions, tags, source, date
gallery →  static masonry surface, reading that manifest
```

Two things decide whether it works, and both belong at ingest:

- **Thumbnails.** 1.6 GB of full-size images in a grid crawls. Generate a small variant per image at ingest; the grid loads thumbnails, the modal loads the original.
- **The manifest carries the searchability.** unDolphin already records model, seed, prompt, and true cost per render. That metadata should ride into the manifest rather than dying at the folder boundary — which makes unDolphin's OUTPUT the natural first corpus, since it arrives already described.

**The gate applies here too, and harder.** The operator's standing rule marks the S3 stash **private — metadata only, never viewed**. A public gallery inverts that completely. Access in front, bucket private, nothing served openly.

## 7. Cost

| line | figure |
| :--- | :--- |
| node (OCI always-free E2.1.Micro) | **$0** |
| Cloudflare Tunnel | **$0** |
| Cloudflare Access (≤50 users) | **$0** |
| R2 storage, 1.6 GB of a 10 GB free tier | **$0** |
| R2 egress | **$0 by design** |
| static gallery on Pages | **$0** |
| **Runware renders** | **usage only** — $0.0013 to $0.006 per image, the app records the true figure |

Every recurring line reads zero. The only spend follows a deliberate render, which restates why the auth gate belongs beside the cost band.

## 8. What this document does NOT settle

- **Which node**, and whether to reuse chindi or claim a new one. The operator's call, per his node-claiming design.
- **Whether `untitledprojects.io` migrates**, or whether V2 proves itself on `lab3120.earth` first.
- **Whether the whole 1.6 GB belongs in a browsable index.** Nothing in `_VAULTS` got opened to judge, and some of it plausibly should not appear.
- **The `neonforge` DNS record** — deliberate or not, unread.
- **Whether the alchemist wants the app served at all**, or wants V2 shaped differently. The playbook parks it awaiting the webmaster path; it does not order this one.
- **The extensibility limit the operator named.** He reads the alchemist as having hit a ceiling on how extensible the app can get. This document does not diagnose that, and a hosting move does not by itself lift it.

*Written 2026-08-13, unix 1786679690. Every figure from a live reading the same hour: HTTP probe, DNS resolution, filesystem census, AWS caller-identity, and the vault reachability check. ~webmaster.Q9-0*
