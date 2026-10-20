---
id: 2026-10-20-produce-lululemon-black-luon-x17-preproduction
title: Produce Lululemon black Luon X17 preproduction package
status: open
priority: P2
area: docs
owner:
claimed_at:
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
- [x] Independently audit v3 sources and obtain two truly fresh first-reader ballots on its frozen SHA; archive the HOLD reasons.
- [x] Revise v4 and re-freeze the author package with synchronized docs, schemas and local checks.
- [ ] Obtain a fresh source PASS and two first-reader narrative ballots on the v4 freeze before a reviewable PR.

## How to verify

`node docs/videos/story-everyday-lululemon-x17/compose-video.mjs`; `node docs/videos/story-everyday-lululemon-x17/compose-shorts.mjs`; `node tools/video/cli.mjs lint --slug story-everyday-lululemon-x17`; split the two Shorts and run `node tools/video/shorts/cli.mjs validate --file <single-json> --source-base docs/videos/story-everyday-lululemon-x17`; `npm run test:docs-videos`; `npm run check:tasks`; `git diff --check`.

## Notes

Source access: original SEC filings and company releases are reachable. The company describes a `pull-back`, not a regulatory recall. The March 2013 `$57–67m` lost-revenue projection is not a realized result; the `$17.5m` charge is an inventory provision. Long 10-K paragraphs fall outside the worker's first 40k parsed-text window, so essential FY claims use shorter SEC earnings exhibits. Independent factual and blind narrative reviews remain future gates. No paid calls are authorized in this task.

V1 independent [SEC source audit](../../docs/videos/story-everyday-lululemon-x17/reviews/script-source-audit-v1-independent.md) returned HOLD for two source phrasings and one Short citation; [blind A](../../docs/videos/story-everyday-lululemon-x17/reviews/blind-a-v1-independent.md) requested narrative changes. V2 revises those items, withholds the April answer from the opener, makes the pre-incident testing sequence physical, fixes loop payoffs, removes the FY2014 detour, and keeps six active SEC originals. The v1 votes do not transfer to v2. Fresh independent source audit and two new blind reads remain required before paid production; this ticket stays open.

V2 [source audit](../../docs/videos/story-everyday-lululemon-x17/reviews/script-source-audit-v2-independent.md) passed, but independent [blind A](../../docs/videos/story-everyday-lululemon-x17/reviews/blind-a-v2-independent.md) and [blind B](../../docs/videos/story-everyday-lululemon-x17/reviews/blind-b-v2-independent.md) both held the narrative. V3 changes the opening, chapter transitions, payoffs, repeated explanation, FY2013 tail, and Short 2 answer; [author response](../../docs/videos/story-everyday-lululemon-x17/reviews/v3-author-response.md) maps each correction. Fresh independent SEC and two blind reviews must bind the v3 freeze before paid media.

V3 frozen `video.json` SHA-256 `bb9677cbbf9830be8a116c4edf7ff5743b1384a165f823b197e9ef76b176ebf5` and `shorts.json` `089a8b37946f59d4fecd79bfaf470b5038088893abfb0caa881f921b1882fd8d` passed author lint 0/0, both Shorts schemas/episode source links and docs-video tests. The independent [source audit](../../docs/videos/story-everyday-lululemon-x17/reviews/script-source-audit-v3-independent.md) re-fetched S1–S5/S6a with matching raw SHA but returned **HOLD** on `x170501`, its card and Short 2 `x17s204`: 「第一季後七週」 can mean seven weeks **after** Q1 while S4 says Q1's **last** seven weeks. Two genuinely fresh [blind A](../../docs/videos/story-everyday-lululemon-x17/reviews/blind-a-v3-independent.md) / [blind B](../../docs/videos/story-everyday-lululemon-x17/reviews/blind-b-v3-independent.md) readers both marked mandatory Q8 NO on repeated 2006 specification/warehouse explanation; A also Q2 NO for an opening warehouse spoiler, B also Q7/Q13 NO for an unanswered finished-garment inspection question and FY2012 size detour. Thus v3 remains **HOLD**. V4 should replace all three time phrases with 「第一季最後七週」, withhold the warehouse/transit reveal until the later store/warehouse account, make the inspection question answerable or change it, and trim the FY2012 size and final-year accounting paths without losing the >=8-minute substantive body. Actual TTS and media remain unmeasured.

V4 [author revision map](../../docs/videos/story-everyday-lululemon-x17/reviews/v4-author-response.md) addresses those three independent HOLDs, without converting any old ballot to a PASS. `video.json` SHA-256 `5103c7a52e118c17cdea8dbb627564f08365a6c15d7a7a3014ad53f97037bc44` and `shorts.json` `58ca34c872aa4addb210e4697a9ce45939a649d837e351f4657f989c9dfdb059` are the new author freeze. V4 has 2,475 substantive Han/digits, 115 lines, 100 still shots, 8 native cards and 17 declared loops; local main lint is 0 errors/0 warnings and both Shorts validate against the new main SHA. Fresh SEC source and two fresh-context narrative votes must bind these exact files. TTS duration, generated visuals, official bookends, live links and production costs are still unmeasured; no paid media, host import, push or PR has occurred.

V4 independent [SEC audit](../../docs/videos/story-everyday-lululemon-x17/reviews/script-source-audit-v4-independent.md) re-downloaded all six necessary originals with matching raw bytes/SHA and confirmed the v3「第一季最後七週」repair, but returned **HOLD** on `x170519`: S4 reports increased site traffic and a lower **conversion rate**;「結帳卻變少」implies an unsupported fall in the absolute number of completed checkouts. Change to「完成結帳的比例卻下降」or equally precise wording, regenerate every derived file, freeze v5, and repeat source/dual-blind review on the new hashes. No v4 narrative ballot was commissioned because the source blocker was found first.
