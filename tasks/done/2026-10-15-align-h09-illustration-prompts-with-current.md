---
id: 2026-10-15-align-h09-illustration-prompts-with-current
title: Align H09 illustration prompts with current Curio rules
status: done
priority: P1
area: docs
owner: codex-gpt6-h09-visual-prompts
claimed_at: 2026-10-15T02:38:13Z
created_at: 2026-10-15T02:38:04Z
completed_at: 2026-10-15T02:51:30Z
branch: codex/curio-h09-earhart-20261015
depends_on: []
scope:
  - docs/videos/curio-h09/video.json
---

# Align H09 illustration prompts with current Curio rules

## Why

The H09 storyboard predated the current Curio guidance. Object-only scenes invited faces on props or stray people, some prompts requested bright landscapes, and many other shots showed only hands, backs, or several people. Four accepted pictures from the paid seven-shot pilot also needed their exact cache keys preserved.

## Definition of done

- [x] All 92 shot prompts follow the fixed cute-mystery look, neutral soft lighting, and one visible person doing one clear action where needed.
- [x] The prompts preserve the approved narration's uncertainty: no confirmed Electra wreck, no recovered Taraia object, and one position line rather than two flight paths.
- [x] Four accepted pilot pictures retain exact image request keys. The rejected pilot pictures and source media remain available for targeted rework.
- [x] Video lint has zero errors and no new storyboard-diversity warnings; no paid generation or media deletion occurs in this ticket.

## Steps

- [x] Review current Curio and YouTube-video skills, narration, and all 92 prompts.
- [x] Rewrite 53 originally empty or object-only shots and 32 remaining back-facing, multi-person, hand-only, or expressionless shots.
- [x] Correct the one position-line prompt, the surface-search limitation prompt, and a premature medical-folder prompt.
- [x] Independently review the final storyboard against narration, facts, look, and chapter shot-size mix.
- [x] Recompute exact image cache keys for the accepted pilot pictures against the paid manifest.

## How to verify

- node tools/video/cli.mjs lint --slug curio-h09: 0 errors; three existing script or duration warnings.
- git diff --check -- docs/videos/curio-h09/video.json: no whitespace errors.
- Parsed JSON comparison with HEAD: 100 scenes, 92 shots, look exactly {preset: cute-mystery}; only prompts changed by this ticket. The parent task separately revised the unresolved-verdict narration line.
- Exact key recomputation with composeShotPrompt, keyframeKey, and mediaKey: hour-later-call, radio-0843, radio-silence, and search-plane-island match selected paid-manifest entries.

## Notes

- Final video.json SHA256: 4ba994ee7838e8e324b40dc9364e48e62212d7e9fb83fee8b3e49c19c8f2a8c9. A later parent-owned script-only edit will change the whole-file SHA without changing picture request keys.
- Accepted radio-0843, radio-silence, and search-plane-island prompts were restored from commit 5800dd6c2. More recent HEAD prompts did not match the already paid image keys. Hour-later-call was untouched.
- itasca-waits-1-trim passed the nine-question judge, but its sailor appears outside the hull at sea level and its Howland backdrop is a tall island. That suggests an overboard incident and a terrain inconsistent with the low coral island described by the U.S. Fish and Wildlife Service, so its revised prompt remains a retake request.
- All three low-fuel-warning and all three uncertain-broadcasts takes failed the judge. Seed 2 of low-fuel and seed 1 of uncertain-broadcasts may merit a no-cost crop and judge recheck before paying for another image; neither is accepted yet.
- The four accepted pilot pictures are illustration, not evidence reconstruction. Large hands, a resting hand instead of a lifted earcup, and cartoon eyes on the aircraft do not contradict the narration or change the series medium.
- Existing lint warnings concern a 10.6-second closing shot and two narration hook intervals. Narration text, speech overrides, scene count, media cache, STOP, and other H09 files were outside this ticket's edit scope.
