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
- [x] Repair v4 website conversion-rate source HOLD and re-freeze v5 with synchronized docs, schemas and local checks.
- [x] Obtain a fresh source PASS and two first-reader narrative ballots on the v5 freeze; common narrative failures require revision.
- [x] Revise to v6, rebuild all derived files and freeze exact SHA with author checks.
- [x] Obtain new same-SHA source and dual-blind review on v6; the common repetition finding holds the narrative.
- [x] Revise to v7, rebuild derived files and freeze exact SHA with author checks.
- [ ] Obtain new same-SHA source and dual-blind narrative passes before a reviewable PR.

## How to verify

`node docs/videos/story-everyday-lululemon-x17/compose-video.mjs`; `node docs/videos/story-everyday-lululemon-x17/compose-shorts.mjs`; `node tools/video/cli.mjs lint --slug story-everyday-lululemon-x17`; split the two Shorts and run `node tools/video/shorts/cli.mjs validate --file <single-json> --source-base docs/videos/story-everyday-lululemon-x17`; `npm run test:docs-videos`; `npm run check:tasks`; `git diff --check`.

## Notes

Source access: original SEC filings and company releases are reachable. The company describes a `pull-back`, not a regulatory recall. The March 2013 `$57–67m` lost-revenue projection is not a realized result; the `$17.5m` charge is an inventory provision. Long 10-K paragraphs fall outside the worker's first 40k parsed-text window, so essential FY claims use shorter SEC earnings exhibits. Independent factual and blind narrative reviews remain future gates. No paid calls are authorized in this task.

V1 independent [SEC source audit](../../docs/videos/story-everyday-lululemon-x17/reviews/script-source-audit-v1-independent.md) returned HOLD for two source phrasings and one Short citation; [blind A](../../docs/videos/story-everyday-lululemon-x17/reviews/blind-a-v1-independent.md) requested narrative changes. V2 revises those items, withholds the April answer from the opener, makes the pre-incident testing sequence physical, fixes loop payoffs, removes the FY2014 detour, and keeps six active SEC originals. The v1 votes do not transfer to v2. Fresh independent source audit and two new blind reads remain required before paid production; this ticket stays open.

V2 [source audit](../../docs/videos/story-everyday-lululemon-x17/reviews/script-source-audit-v2-independent.md) passed, but independent [blind A](../../docs/videos/story-everyday-lululemon-x17/reviews/blind-a-v2-independent.md) and [blind B](../../docs/videos/story-everyday-lululemon-x17/reviews/blind-b-v2-independent.md) both held the narrative. V3 changes the opening, chapter transitions, payoffs, repeated explanation, FY2013 tail, and Short 2 answer; [author response](../../docs/videos/story-everyday-lululemon-x17/reviews/v3-author-response.md) maps each correction. Fresh independent SEC and two blind reviews must bind the v3 freeze before paid media.

V3 frozen `video.json` SHA-256 `bb9677cbbf9830be8a116c4edf7ff5743b1384a165f823b197e9ef76b176ebf5` and `shorts.json` `089a8b37946f59d4fecd79bfaf470b5038088893abfb0caa881f921b1882fd8d` passed author lint 0/0, both Shorts schemas/episode source links and docs-video tests. The independent [source audit](../../docs/videos/story-everyday-lululemon-x17/reviews/script-source-audit-v3-independent.md) re-fetched S1–S5/S6a with matching raw SHA but returned **HOLD** on `x170501`, its card and Short 2 `x17s204`: 「第一季後七週」 can mean seven weeks **after** Q1 while S4 says Q1's **last** seven weeks. Two genuinely fresh [blind A](../../docs/videos/story-everyday-lululemon-x17/reviews/blind-a-v3-independent.md) / [blind B](../../docs/videos/story-everyday-lululemon-x17/reviews/blind-b-v3-independent.md) readers both marked mandatory Q8 NO on repeated 2006 specification/warehouse explanation; A also Q2 NO for an opening warehouse spoiler, B also Q7/Q13 NO for an unanswered finished-garment inspection question and FY2012 size detour. Thus v3 remains **HOLD**. V4 should replace all three time phrases with 「第一季最後七週」, withhold the warehouse/transit reveal until the later store/warehouse account, make the inspection question answerable or change it, and trim the FY2012 size and final-year accounting paths without losing the >=8-minute substantive body. Actual TTS and media remain unmeasured.

V4 [author revision map](../../docs/videos/story-everyday-lululemon-x17/reviews/v4-author-response.md) addresses those three independent HOLDs, without converting any old ballot to a PASS. `video.json` SHA-256 `5103c7a52e118c17cdea8dbb627564f08365a6c15d7a7a3014ad53f97037bc44` and `shorts.json` `58ca34c872aa4addb210e4697a9ce45939a649d837e351f4657f989c9dfdb059` are the new author freeze. V4 has 2,475 substantive Han/digits, 115 lines, 100 still shots, 8 native cards and 17 declared loops; local main lint is 0 errors/0 warnings and both Shorts validate against the new main SHA. Fresh SEC source and two fresh-context narrative votes must bind these exact files. TTS duration, generated visuals, official bookends, live links and production costs are still unmeasured; no paid media, host import, push or PR has occurred.

V4 independent [SEC audit](../../docs/videos/story-everyday-lululemon-x17/reviews/script-source-audit-v4-independent.md) re-downloaded all six necessary originals with matching raw bytes/SHA and confirmed the v3「第一季最後七週」repair, but returned **HOLD** on `x170519`: S4 reports increased site traffic and a lower **conversion rate**;「結帳卻變少」implies an unsupported fall in the absolute number of completed checkouts. Change to「完成結帳的比例卻下降」or equally precise wording, regenerate every derived file, freeze v5, and repeat source/dual-blind review on the new hashes. No v4 narrative ballot was commissioned because the source blocker was found first.

V5 [author response](../../docs/videos/story-everyday-lululemon-x17/reviews/v5-author-response.md) repairs `x170519` to「完成結帳的比例卻下降」and marks the conversion-rate denominator explicitly in the source matrix and reviewer handoff. Both composers were rerun; the two Shorts' narration and `shorts.json` bytes are unchanged. V5 independent SEC source and two fresh-context narrative gates remain pending. No paid media, upload, push or PR has occurred.

V5 author freeze: `video.json` SHA-256 `66d584c4907cfa6041174ca0fd5d01cdb5cb868690e7804b84da02fde64e545a`; `shorts.json` `58ca34c872aa4addb210e4697a9ce45939a649d837e351f4657f989c9dfdb059`; `source-matrix.md` `8735a2d463863243de68ee689d2ee1d2a9444b8e95a83337d1b2fc84f3960106`; `drafts/narration.md` `d5515075414354a02d9846de5c7eddaa28d4ac5a13cba3655c6c9477f5a4de2e`; `visual-plan.md` `5a3c8d456e17998a1d53a5f756ec03640a8aef13715bfefa6703e942cef69351`. Paper substantive body is 2,480 Han/digits. Author lint 0/0, both Shorts schema/source hash checks and episode link check pass; `test:docs-videos` 236/236 and task-board check passes. Independent v5 PASS is not claimed.

V5 independent [SEC audit](../../docs/videos/story-everyday-lululemon-x17/reviews/script-source-audit-v5-independent.md) re-fetched all six originals with identical bytes/SHA and passed the conversion-rate repair on the frozen lines, cards and Shorts. New [blind A](../../docs/videos/story-everyday-lululemon-x17/reviews/blind-a-v5-independent.md) / [blind B](../../docs/videos/story-everyday-lululemon-x17/reviews/blind-b-v5-independent.md) each locked an uninfluenced 7.0/10 and marked mandatory Q8 and Q13 **No**: `x170630` repeats the earlier inventory provision and test finding without an explicit callback, and `x170213`'s generic weekly distribution frequency is never used to resolve the black-Luon failure. B also marked Q7 No because `x170211` asks exactly which old tests were absent, while the original only establishes that not all relevant variables were covered. Both Shorts stand alone on paper. Thus v5 narrative is **HOLD**; v6 needs to repair those precise lines, retain source scope, and re-freeze before two truly fresh ballots. A timeline estimate of 12.21 minutes exceeds the JSON's 8–10 minute target; actual spoken body and finished duration remain unmeasured. No paid media, official bumper files, MP4, upload, links or PR exists for X17.

V6 [author response](../../docs/videos/story-everyday-lululemon-x17/reviews/v6-author-response.md) maps the exact repairs: `x170211` and `x170404` now ask whether the old checklist covered all relevant variables, which S3 can answer; `x170213` weekly delivery and `x170216` generic quality claim are removed; the remaining factory handoff is tied to S3's later partner training; `x170630` expressly returns to the opening empty rack without restating US$17.5m. `video.json` SHA-256 `39b6d9ffc3b1abe987d3f7b233333be6f2f11e6539c6233115679e81db4140ff`, `shorts.json` SHA-256 `58ca34c872aa4addb210e4697a9ce45939a649d837e351f4657f989c9dfdb059`, source matrix `52996623d155a2fe93495bb87411d5f8ddcc6bc36442e82a5565d0cebc40b913`, narration `e8085e0620169417842565794eb97d6866078fbad5636a4a1e1b90607cf12d44`, visual plan `e00b8ce0125fab4b7b667cb59a18a78f3fd63bf0c10331c74c5f6f840763378a`. Author compiler gives 114 lines, 99 still shots, eight cards, 17 loops, opening 181 visible characters and body 2,463 Han/digits. Main lint 0 errors/0 warnings, individual Short schema/source validations and episode links PASS, docs-video tests 236/236, task-board check exit 0 with unrelated existing warnings, `git diff --check` clean. These are author-side results, **not** v6 independent SEC or narrative PASS. The CLI's 250-unit estimate is 12.1 minutes including hook/outro; 320–330-unit paper pace targets nearer ten minutes with bookends, but actual TTS must measure substantive body >=8:00 before purchase or publication. No paid media, MP4, upload, real links or PR exists for X17.

V6 independent [SEC audit](../../docs/videos/story-everyday-lululemon-x17/reviews/script-source-audit-v6-independent.md) re-fetched all six necessary originals with identical bytes/SHA and passed the frozen lines, cards, Shorts and publishing scope. New [blind A](../../docs/videos/story-everyday-lululemon-x17/reviews/blind-a-v6-independent.md) and [blind B](../../docs/videos/story-everyday-lululemon-x17/reviews/blind-b-v6-independent.md) each scored 7/10 and both marked mandatory Q8 **No**: A cites adjacent `x170518–519` repeating website conversion and order-value falls; B cites `x170526` repeating the estimate-vs-actual caveat and `x170630` replaying April findings despite the opening callback. B also marked Q13 No for `x170422–423` staffing-report detour; A otherwise passed required questions. Both Shorts stand alone on paper. Thus v6 narrative is **HOLD**; v7 should remove those three repeated passages and fold/drop the staffing lines while preserving the product/test/accounting spine. Then freeze, re-audit and use two genuinely new first-blind readers. No paid media, official animations, finished film, upload, real links or PR exists for X17.

V7 [author response](../../docs/videos/story-everyday-lululemon-x17/reviews/v7-author-response.md) removes the shared Q8 repetitions and B's Q13 staffing detour, sharpens the opening fabric-versus-finished-garment question, and makes the fitting-room illustration explicitly hypothetical. The frozen SHA-256 values are `video.json` `206ac3e85da49521a7b09a5bc6b8ba3bb4a4de92d5f74e2ebef7c03011ba7983`, `shorts.json` `8ce8f5995b08e94ed9e864ada67233af1fd1b1aaf2311e82974ad339c5961915`, source matrix `96f92bfd151b6d201fddf60a3f5579b8de68250cf80d9651c1d7fc7e0fb1bb3a`, narration `26fcf907de7f2a95686d675cb3fc974e450b83fac416cb04f72b2891302003e2`, and visual plan `b1d4836ca314e4086d4c015cab72804f780d3dadb74245452e4e0d3929019230`. Author compiler yields 115 lines, 100 still shots, eight cards, 17 declared loops, an 185-visible-character condensed opening and 2,478 Han/digit substantive body. Main lint has 0 errors/0 warnings, both separate Short schema/source checks and episode links pass, docs-video tests pass 236/236, task-board check exits 0 with unrelated older warnings, and `git diff --check` is clean. These are author-side checks only; independent SEC and two fresh blind ballots must evaluate these exact v7 files. Actual TTS duration, official 5/21-second bookends, rendered MP4, final clickable links and costs remain unmeasured; no paid media, upload, push or PR has occurred for X17.
