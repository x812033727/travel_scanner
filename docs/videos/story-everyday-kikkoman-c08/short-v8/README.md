# C08 short-v8 canonical project

This is a reviewable, nonpaid projection of the exact owner-approved short-v8 narration and visual plan. It lives under the C08 source directory so the existing 84-line project remains intact. `build.mjs` refuses either frozen input if its SHA-256 changes and checks all 36 IDs, order, six chapters, 30 shots and 6 cards before writing the project files.

| Status | Evidence |
| --- | --- |
| Exact narration and visual direction approved | Owner decision in the 2026-10-24 task conversation; SHA-256 `040d9a499ddb864f62ebf0edcc948cc58439ffa13d0dae0ce5a9475297ee5d69` and `0676e76a4c9d49b12ece74df1835a72ce264eabb24a3158635921f57244dd241` |
| Independent source and visual review | `../reviews/v8-short-independent-review-20261024.md`: 36/36 and 36/36 PASS; two blind readers had no shared required-question veto |
| Media and release | No audio, pictures, music, measured duration, price authorization, import, upload or publication |

Run `node docs/videos/story-everyday-kikkoman-c08/short-v8/build.mjs` to regenerate the projection. Run `node tools/video/cli.mjs lint --file docs/videos/story-everyday-kikkoman-c08/short-v8/video.json` to inspect lint. Because this project is nested, `--slug` still points to the historical top-level C08 project. The short route needs an explicit later integration decision before import or paid production.

`tools/video/core/paths.mjs` resolves a slug only as `docs/videos/<slug>/video.json`; `status`, TTS and the worker use that path. Thus `--slug story-everyday-kikkoman-c08` selects the original 84-line project, while `--slug story-everyday-kikkoman-c08-short-v8` has no top-level project yet. This nested package is a reviewed **candidate for promotion**, not a runnable worker project. Once the short-duration policy and episode identity are resolved, promote the generated `video.json`, `series.json`, `brief.md`, `claims.md`, `verify-1.md`, `script.md` and `visual-plan.json` together to `docs/videos/story-everyday-kikkoman-c08-short-v8/`, recheck their hashes and lint with `--slug story-everyday-kikkoman-c08-short-v8`, and verify a fresh workdir uses the same slug. Keep the original C08 files and approvals intact.

`python -m app.cli video-story-import` reads a compiled `stories.json` plan from standard input; it does not read this `video.json`. Any eventual backend import must separately select and dry-run the exact C08 episode/slug in that plan, reconcile the existing episode-8 record, and confirm the worker reads the promoted short-v8 project before an apply. Neither a local file lint nor a dry-run imports this package.

The 480-second long-form minimum remains active. A v8 short lint error on `target_minutes` and estimated length is expected. `MoMA` in the exact approved narration also needs an independently reviewed pronunciation before TTS. The `stats` preview for `v7e03` cannot draw the approved flat spout diagram, which remains a postproduction and visual acceptance task.

The shortened YouTube title, description, series logline and inherited thumbnail text are planning metadata in this package. The owner's exact approval binds narration and visual direction only; metadata and final packaging still need review before any upload.
