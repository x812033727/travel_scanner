---
id: 2026-10-20-target-canada-x08-brand-story-preproduction
title: Target Canada X08 brand-story preproduction package
status: review
priority: P2
area: docs
owner: codex-x08
claimed_at: 2026-10-20T17:21:41Z
created_at: 2026-10-20T17:21:37Z
completed_at:
branch: codex/brand-story-target-x08
depends_on: []
scope:
  - docs/videos/story-everyday-target-x08
  - tasks/open/2026-10-20-target-canada-x08-brand-story-preproduction.md
---

# Target Canada X08 brand-story preproduction package

## Why

The owner asked for the next new brand-story video, following the 奇聞檔案局 style and a separate PR after each episode. Target Canada offers a dated, documentable decision, but the popular retelling often confuses the January 2015 court filing with later store closure and treats a largely noncash exit charge as cash lost. This task builds a source-bound offline production package before any paid generation.

## Definition of done

- [x] Six-chapter Traditional Chinese narration and scene plan with at least eight substantive estimated minutes, a 30–60 second condensed opening, 5-second intro and 21-second outro handoff, and two derivative Shorts.
- [x] Every date, amount, causal claim and negative statement has an accessible primary source; two independent reviewers check the final candidate hash.
- [x] Budget and publishing handoff list all-in US$25 stop condition, no paid calls or unsupported claim of a produced film.

## Steps

- [x] Confirm nonduplicate topic and create isolated branch/worktree.
- [x] Find accessible SEC originals including the FY2015 Q1 closure status.
- [x] Write source notes, claim matrix and six-chapter treatment.
- [x] Build candidate narration, scene/visual package, Shorts and handoff.
- [x] Bind independent source and narrative reviews to final hash; run relevant local checks.
- [x] Commit and open reviewable PR; do not start paid media generation.

## How to verify

`node docs/videos/story-everyday-target-x08/compose-video.mjs`; `node docs/videos/story-everyday-target-x08/compose-shorts.mjs`; `node tools/video/cli.mjs lint --file docs/videos/story-everyday-target-x08/video.json --json`; `npm run check:tasks`; `git diff --check`. Source URLs manually read from SEC originals; independent reviews cite the final SHA. The eight-minute requirement is an estimate until actual TTS timing is measured.

## Notes

- Independent worktree `/workspace/travel_scanner_target_x08`, branch `codex/brand-story-target-x08` from `origin/main`; only this task's ticket and `docs/videos/story-everyday-target-x08` are in scope.
- FY2013 10-K says Canadian gross margin **14.9% in fiscal 2013** and attributes it to clearing excess inventory after lower-than-expected sales and supply-chain startup challenges. This is not company-wide gross margin or proof of literal empty shelves.
- Jan 15, 2015 company announcement said stores would remain open during liquidation. FY2015 Q1 10-Q says all Canadian stores had closed **by May 2, 2015**. No precise last-store date asserted.
- FY2014 10-K shows **US$5.105b pretax exit charges** including **US$4.766b noncash investment impairment**. These are different from FY2014 Canadian pretax operating loss **US$869m**, and from the Jan 15 contemporaneous forecast of about US$5.4b pretax loss on discontinued operations.
- Q2 FY2014 −11.4% comparable sales covers 48 mature stores; Q3 +1.6% covers 82, a different eligible sample. FY2014 Q3 Canadian segment EBIT was −US$211m for that quarter only; all from SEC-filed Target earnings releases. The script and cards must not imply the same cohort turned positive.
- Candidate `video.json` builds deterministically from `drafts/narration.md`, and final lint reports zero errors and warnings. The exact `video.json` SHA is `a6ffe45d1944839e0ae35c9e8418e340dacef578e7faa5304219b80fe4118bb4`, with 134 spoken lines, 113 illustration prompts and 14 native stats cards. A temporary untracked `node_modules` symlink used for local lint was removed before commit; no tracked package files changed.
- Independent full source audit plus focused final-line re-audit PASS on the exact `video.json` SHA above and unchanged `shorts.json` SHA `440ceee9649b30af2bd64ff1205bf38bff47d0be381b1b544cccff4601e2d543`; both independent blind readers PASS all 12 required questions and the optional chapter question on narration-panel SHA `f8547c2c1f9a30abaf6798515c74485f37d5caf36f14342b7145a3d9a96c66dc`. The four final receipts are linked from the package README; older failed receipts remain for audit trail. `npm run check:tasks` passes with unrelated existing repository warnings.
- No paid image, TTS, music or other media calls made for X08. The paired video tool is reachable in this cloud; X08's formal media workdir and selected official 5-second intro/21-second outro originals are still absent. This PR is an offline preproduction package, not a finished film. Formal TTS must confirm the substantive body is at least eight minutes.
- Reviewable preproduction PR: https://github.com/x812033727/travel_scanner/pull/1625. Keep this task in `review` while that PR is open; move to `done` only after merge. Formal media and publish gates remain explicit in the package handoff rather than falsely marked complete here.
