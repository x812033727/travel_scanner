---
id: 2026-10-20-produce-lululemon-black-luon-x17-preproduction
title: Produce Lululemon black Luon X17 preproduction package
status: in-progress
priority: P2
area: docs
owner: codex-x17-lululemon
claimed_at: 2026-10-20T22:21:14Z
created_at: 2026-10-20T22:21:12Z
completed_at:
branch: codex/brand-story-lululemon-x17
depends_on: []
scope:
  - docs/videos/story-everyday-lululemon-x17
---

# Produce Lululemon black Luon X17 preproduction package

## Why

The approved X17 topic needs a source-bound preproduction package before independent review or paid media. A black Luon pants pull-back in March 2013 offers a concrete product-and-business story, but its forecast lost sales, actual inventory charge, fiscal-year comparisons and product-quality explanation can be easily conflated.

## Definition of done

- [x] Six-chapter zh-TW Treatment and a substantive script with a paper body of at least eight minutes, two distinct 25–55-second Shorts, visual plans, and a cost-capped handoff are ready for independent audits.
- [x] Each factual claim is traceable to live original SEC submissions with byte counts, SHA-256 and denominator limits.
- [x] Schemas compose and local checks pass; no paid media, upload, push or PR has occurred.

## Steps

- [x] Create isolated branch/worktree from latest `origin/main`; claim this narrow package scope.
- [x] Freeze source matrix and draft one physical-object narrative through six chapters.
- [x] Compose main and Shorts schemas, line matrices, storyboard and production handoff.
- [x] Run local validation, record hashes and commit the package for independent audits.

## How to verify

`node docs/videos/story-everyday-lululemon-x17/compose-video.mjs`; `node docs/videos/story-everyday-lululemon-x17/compose-shorts.mjs`; `node tools/video/cli.mjs lint --slug story-everyday-lululemon-x17`; split the two Shorts and run `node tools/video/shorts/cli.mjs validate --file <single-json> --source-base docs/videos/story-everyday-lululemon-x17`; `npm run test:docs-videos`; `npm run check:tasks`; `git diff --check`.

## Notes

Source access: original SEC filings and company releases are reachable. The company describes a `pull-back`, not a regulatory recall. The March 2013 `$57–67m` lost-revenue projection is not a realized result; the `$17.5m` charge is an inventory provision. Long 10-K paragraphs fall outside the worker's first 40k parsed-text window, so essential FY claims use shorter SEC earnings exhibits. Independent factual and blind narrative reviews remain future gates. No paid calls are authorized in this task.

Local handoff checks on 2026-10-20: main lint 0 errors (3 recurrent-object prompt-word warnings), both Short schema/source hash checks pass, `npm run test:docs-videos` 236/236 pass, `npm run check:tasks` exits 0 with unrelated existing board warnings. Exact candidate SHA table is in the package README; source and blind reviews are pending, so this ticket remains open for the reviewer handoff.
