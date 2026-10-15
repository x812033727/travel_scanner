---
id: 2026-10-14-support-10-minute-minimax-cute-brand
title: Support 10-minute MiniMax cute brand-story series
status: review
priority: P1
area: tools
owner: codex-8a78-story-route
claimed_at: 2026-10-14T16:11:01Z
created_at: 2026-10-14T16:10:55Z
completed_at:
branch: codex/brand-stories-five-20261014
depends_on: []
scope:
  - tools/video/automation/story.mjs
  - tools/video/automation/story.test.mjs
  - tools/video/automation/flow.mjs
  - tools/video/story-plans/plan.mjs
  - tools/video/story-plans/plan.test.mjs
  - apps/api/app/video_automation/stories.py
  - apps/api/app/video_automation/schemas.py
  - apps/api/app/video_automation/series.py
  - apps/api/tests/test_video_story_import.py
  - apps/api/tests/test_video_story_series.py
  - tools/video/core/drama.mjs
  - tools/video/core/explainer-family.test.mjs
  - tools/video/core/story.test.mjs
---

# Support 10-minute MiniMax cute brand-story series

## Why

The owner selected MiniMax `image-01`, the exact `{"preset":"cute-mystery"}` look and about 10 minutes for five brand stories after the A01/B18 pilot. The existing story-series importer and compiler require 12–15 minutes with nonempty custom style/negative; the worker forces `video.json.look.preset=custom`. Merely changing the five treatments would still produce the old visuals and length. Preserve the original 100-story Gemini/13-minute route while allowing a separate five-story series to use the new settings.

## Definition of done

- [x] A new story series with 10 minutes, `image-01` and exact `{"preset":"cute-mystery"}` look validates through local compiler and API importer checks.
- [x] The six-chapter story worker emits a `video.json` with that exact look, while original custom story series still emits its old look unchanged.
- [x] Focused JS/Python regression tests pass, including rejection of malformed mixed custom/preset looks.
- [x] The five-story worker rejects a merged script before paid keyframes if its body is empty, under 70% illustrated shots, has more than three consecutive cards, or loses the exact cute-mystery look; A01/B18 retain their original route.
- [x] A01/B18 v2 hold before TTS until an independent review receipt binds the worker's actual six-chapter script, current plan, source and narrative checks, and the frozen independently reviewed Markdown reference. A stale receipt holds again before downstream stages.

## Steps

- [x] Extend the narrow story-series validators/schema without changing the original 100-story source files.
- [x] Carry the preset through series state to `video.json`; keep the story writer and fact-checker route.
- [x] Run focused tests and record any remaining server or import gate.

## How to verify

Run `node --test tools/video/story-plans/plan.test.mjs tools/video/automation/story.test.mjs` plus the targeted API tests under `apps/api`, and check a 10-minute preset payload and original 13-minute custom payload. This task does not import, render or purchase media.

## Notes

- The main branch's `curio-*` visual lint is slug-scoped; it does not automatically validate `story-*` episodes. This task's story worker now checks the five new `story-five-*` slugs when all six chapters are merged, before paid keyframes. Final image quality and actual scene mix still require review of generated media.
- The importer starts new `kind=story` series as active. The five-series payload stays local/dry-run until the A01/B18 pilot and owner gate; this task only makes the specified format possible.
- Local receipt (2026-10-15): `seriesProblems` accepts the five-series `series.json`; Python `check_story_file` accepts all five selected episode rows with zero problems/refusals. An in-memory SQLite import of one selected episode persisted 10 minutes, `image-01`, `style_preset=custom` and exact `look={"preset":"cute-mystery"}`. No live import was run.
- Worker receipt: the new route has a 9:00–11:00 narration band, `video.json.target_minutes=[9,11]`, and 80 budgeted illustrations at about 7.5 seconds each. The original 13-minute route retains its 11:30–15:30 band, `[12,15]` video target and 90 budgeted shots. The cute route's internal `brief.md` adds the two sections required by the preset lint; custom briefs keep their earlier sections.
- A29 cast smoke test: compose a video with its actual two-person cast, one shot referencing a cast ID, its real series look, and fixture scenes; `validateVideo` and `lintVideo` each reported zero errors. Its 21 warnings reflect short synthetic fixture scenes, not an approved production script.
- Checks: `node --test tools/video/automation/story.test.mjs` 21/21 passed using an ASCII `subst` drive because Windows Node 24 crashes in the existing fixture `cpSync` when the checkout's Unicode path is used directly; `node --test tools/video/story-plans/plan.test.mjs tools/video/core/explainer-family.test.mjs tools/video/core/duration.test.mjs` 47/47 passed; targeted Python pytest 9/9 passed; Ruff and mypy on changed Python files passed. The temporary drive mapping was removed.
- `npm run check:tasks` is currently red for an unrelated duplicate A21 correction ticket in both `tasks/open/` and `tasks/done/`; this task's new `review` status is not the failure.
- API PATCH follow-up (2026-10-15): added `series.py` to this ticket's scope after `who-is-on-it --scope apps/api/app/video_automation/series.py` found no active task or open PR touching it. The service checks the merged story series state before saving a change to look, duration, image model or style preset. A cute look must retain exactly 10 minutes, `image-01` and story `custom`; moving back to the original custom look requires its 12–15 minute story length and `custom` writer preset in one PATCH. Focused service/schema tests cover each partial break and both complete transitions. Checks: `uv run pytest tests/test_video_story_series.py tests/test_video_series.py -q` 58 passed, 3 skipped; Ruff and mypy on the two changed Python files passed. `npm run check:tasks` is still red only for the duplicate A21 open/done ticket noted above.
- Still gated: this is a local code and fixture check. The five-series live import, generated audio/images, render, upload, publication and owner acceptance remain separate decisions and receipts.
- Five-film scene gate (2026-10-15): `storyFiveVisualProblems` checks exact `look`, nonempty body, ≥70% `shot` scenes, and ≤3 consecutive body cards. The complete-story `relint` maps ratio and card errors back to the offending chapter via `scenes[index]`, so its writer can revise the script before keyframes. Original custom stories bypass it. Final story suite passed 23/23; `npm run test:docs-videos` passed 215/215 when its offline fixtures ran outside the restricted sandbox's blocked hard-link/loopback paths. No production media was made.
- A01/B18 v2 actual-script hold (2026-10-15): the two pilot slugs alone require `<VIDEO_WORKDIR>/<slug>/story/reviews/script-review.json` before the worker auto-approves `script` or runs TTS. Missing, malformed, cross-slug, non-PASS or stale evidence reports `STOPPED_HOLD` with blocked kind `pilot_script_review`; a human must place a fresh independent PASS receipt and explicitly retry that video in `/admin/videos`. The receipt covers current `script.md`, `video.json`, `series.json` (including imported beats), `claims.md`, `verify-1.md`, `review/narrative.json`, every `story/chapters/<key>.json`, and the exact frozen editorial Markdown hash. The gate rechecks these before subsequent steps, including after a length rewrite; it also verifies `script.md` is regenerated from the current `video.json`. It does not turn the separate editorial Markdown into the worker's spoken file.
- Operator handoff for that receipt: first read the worker's `docs/videos/<slug>/video.json` and `script.md`, six `story/chapters/*.json`, `claims.md`, `verify-1.md` and narrative verdict. Independently compare all spoken lines, cause and effect, facts and sources against the appropriate `brand-stories-pilot-v2-20261015/scripts/{A01,B18}.md` and its PASS review; resolve differences in chapter JSON and let the worker remerge/recheck before attesting. For current file hashes, run a read-only one-line Node import of `pilotScriptReviewEvidence({slug,root:ROOT,workdir:resolveWorkdir({slug,root:ROOT})})` from `tools/video/automation/story.mjs` and `tools/video/core/paths.mjs`. The file schema is `{ "schema_version":1, ...evidence, "status":"PASS", "reviewer_id":"<independent editor ID>", "independent":true, "reviewed_at":"<UTC ISO time>", "checks":{"reference_alignment":"PASS","factual_claims":"PASS","narrative":"PASS"} }`; do not have the worker or any of its writer/checker/listener stages claim the reviewer identity. Save it only after actual independent review, check `pilotScriptReviewProblem({slug,root:ROOT,workdir}) === null`, then use the explicit owner retry. A receipt is an editorial attestation, not owner acceptance, audio QA, visual QA or permission to publish.

  Read-only evidence command from the repository root, with `SLUG` set to one exact v2 pilot slug (prints hashes; does not write PASS):

  ```bash
  node --input-type=module -e 'import {ROOT,resolveWorkdir} from "./tools/video/core/paths.mjs"; import {pilotScriptReviewEvidence} from "./tools/video/automation/story.mjs"; const slug=process.argv[1]; console.log(JSON.stringify(pilotScriptReviewEvidence({slug,root:ROOT,workdir:resolveWorkdir({slug,root:ROOT})}),null,2))' "$SLUG"
  ```

- Pilot script integrity follow-up (2026-10-15): besides exact file hashes and `script.md` from `video.json`, the worker now recomposes all scenes from the six current chapter JSON files and current `series.json`, then compares them structurally with `video.json.scenes`. A newly signed chapter hash cannot certify a stale merged `video.json`/`script.md`; chapter narration, scene prompts, chapter labels and claim references must be the actual merged scenes. A metadata-only YouTube ID update does not fail this scene check, although its existing full-file receipt hash must still be renewed.
- Pilot flagged-audio follow-up (2026-10-15): A01/B18 v2 may retake the **same reviewed words** up to the configured retake count. If Jev still flags a line, the generic listener rewrite of `video.json` and immediate paid `tts --redo` are skipped for these two slugs. `review-push --gate audio` sends the flagged take to the owner; the worker waits. `drama_auto_approve_final` only applies to final/publish gates, and audio auto-approval requires all lines checked, zero flags and no `flagged_lines` (`apps/api/app/video_automation/settings.py` and `video_reviews/admin_service.py`), so this flagged card stays pending even if final-cut auto-approval is enabled. The owner can approve an audible false positive, or reject with a precise note. Rejection uses the existing six-chapter `listener:story` pass; after merge and narrative checks, changed words invalidate the old pilot script receipt and stop again before new TTS. An independent reader reviews the new chapter/merged files, records a fresh PASS receipt with current hashes, and the owner explicitly retries to record the revised lines. A note that changes nothing stops for a person instead of looping. The focused pilot test covers flag, pending review, rejection, stale-receipt hold, fresh receipt, and retry to TTS; original non-pilot narration rewrite route is unchanged.
- Verification of these two follow-ups: full `story.test.mjs` 27/27 and the three original non-pilot narration rewrite tests 3/3 pass with the bundled Node runtime. `npm run check:tasks` is still red only for the unrelated duplicate A21 open/done task file in this worktree; do not resolve it as part of this scoped task.
