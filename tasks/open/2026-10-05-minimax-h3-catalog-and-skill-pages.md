---
id: 2026-10-05-minimax-h3-catalog-and-skill-pages
title: MiniMax-H3 catalog and skill pages still promise 9 reference images the v2 adapter never sends
status: in-progress
priority: P3
area: api
owner: claude-opus-5-5-h3-reference-images-catalog
claimed_at: 2026-10-05T07:27:32Z
created_at: 2026-10-05T07:27:10Z
completed_at:
branch: claude/h3-reference-images-catalog
depends_on: []
scope:
  - apps/api/app/video_media/catalog.py
  - apps/api/tests/test_video_media_providers.py
  - .agents/skills/animation-production/references/cost-model.md
  - .agents/skills/animation-production/references/providers-and-plans.md
  - .agents/skills/animation-camera/references/model-misreads.md
  - apps/api/app/video_media/jobs.py
  - apps/api/tests/test_video_media_jobs.py
  - tools/video/media/clips.mjs
  - tools/video/media/clips.test.mjs
  - .agents/skills/animation-production/SKILL.md
  - .claude/skills/animation-production/SKILL.md
---

# MiniMax-H3 catalog and skill pages still promise 9 reference images the v2 adapter never sends

## Why

PR #1238 moved MiniMax-H3 onto the v2 video API. Its request (`_v2_body` in
`apps/api/app/video_media/providers/minimax.py`) carries only the text, the first frame and an
optional last frame, because the v2 page makes image-to-video and reference-to-video mutually
exclusive and every clip here has a first frame (`ClipJobIn.first_frame` is required). The rest
of the system still said otherwise:

- `apps/api/app/video_media/catalog.py` gave H3 `reference_images=9`. The media status serves
  that number to the clips tool and the settings tab shows the entry's note.
- The jobs layer (`apps/api/app/video_media/jobs.py`, `_request_fields`) accepted references for
  an H3 clip, checked their sizes against the 20 MB total and folded them into the request hash.
  Then the adapter dropped them without a word. `tools/video/media/clips.mjs` sent up to four
  (character sheets and the previous shot's last frame) to every model except Veo Lite.
- `cost-model.md` and `providers-and-plans.md` (animation-production) listed "9 張參考圖" for H3,
  and `model-misreads.md` (animation-camera) still said the adapter sends v1 fields with a first
  frame plus `subject_reference`.

A planner reading any of these would expect H3 to hold faces from character sheets. It holds
them only from the approved first frame.

## Definition of done

- [x] The catalog offers H3 no reference image. A clip job for H3 that carries one is refused
  with 422 `video_media_model_not_allowed` before anything is reserved or stored, the same way
  Veo Lite's always was. The same job with its frames alone passes.
- [x] `clips` sends no references to a model the catalog gives 0, so an H3 run does not trip that
  refusal. The character sheets still go to the judge.
- [x] The three skill pages, and the one SKILL.md row that counts references, say what the code
  does, with the file and constant beside each sentence.

## Steps

- [x] Re-read the official v2 create page (2026-10-05). It allows 9 reference images in
  reference-to-video only and makes that mode exclusive with first and last frames.
- [x] `catalog.py`: set H3 `reference_images=0`, rewrite its note, and record on the field that 0
  means the jobs layer refuses references.
- [x] `jobs.py`: replace the hard-coded Veo Lite reference refusal with one driven by the catalog
  (`model.reference_images == 0`). The change keeps the same number of lines, so the line
  references in the skill pages still hold.
- [x] `clips.mjs`: send `refs = []` when the chosen model's `reference_images` is 0. The Veo Lite
  regex stays as a fallback. Line count unchanged.
- [x] Tests: the providers test ties `V2_VIDEO_MODELS` to `reference_images == 0`. The jobs test
  refuses each reference role for H3 with nothing spent and passes the frames alone. The clips
  test checks that H3 requests carry no references while the judge still gets the sheet.
- [x] Skill text: `cost-model.md` rows for H3 and for reference images, `providers-and-plans.md`
  rows for frames and references, H3's catalog row and the sources table, the H3 row of
  `model-misreads.md`, and the request row in animation-production `SKILL.md` (both copies).

## How to verify

```bash
cd apps/api && PYTHONUTF8=1 uv run pytest -q tests/test_video_media_jobs.py tests/test_video_media_providers.py tests/test_video_media_catalog.py tests/test_video_media_api.py
cd apps/api && uv run ruff check . && uv run mypy app && uv run mypy tests
node --test tools/video/media/clips.test.mjs tools/skills.test.mjs tools/animation-production.test.mjs
node tools/video/long-form/cli.mjs check   # stale until an independent reviewer rebinds clips.test.mjs
```

## Notes

- Scope widened past the filed five paths. The coordinator asked for a jobs layer that refuses
  references for H3 cleanly. On origin/main the jobs layer never read `reference_images` at all
  (only the Veo Lite id check refused references), so setting the catalog to 0 alone would have
  changed nothing, which is why `jobs.py` and its test were added. Refusing in the server while
  `clips.mjs` still sent sheets would have broken every H3 run, so `clips.mjs` and its test were
  added too. The animation-production `SKILL.md` row "參考圖 ≤ 4（Lite 0）" became wrong for H3,
  so both copies are in scope (SKILL.md is the only mirrored file; the references live once under
  `.agents/skills`).
- `tools/video/media/clips.test.mjs` is bound by `docs/videos/long-form/review.json`, so
  `node tools/video/long-form/cli.mjs check` reports it stale. Rebinding it needs an independent
  reviewer. I did not edit review.json or review.md.
- The Veo Lite refusal message changed from "Veo Lite 不支援角色參考圖，請使用首幀" to
  "<label> 不收參考圖，只收首格與末格". Nothing matched on the old text.
- Clip cache keys for H3 change, because `references` now goes empty. The catalog notes that no H3
  clip has been made, so nothing cached is lost.
- Left alone: the web test fixtures (`apps/web/components/admin-video-settings.test.tsx`,
  `admin-video-drama-settings.test.tsx`) carry a made-up H3 option with `reference_images: 9` and
  durations `[4, 6, 8, 10]`. The UI only types the field, so those are arbitrary fixture values,
  not a contract.
- The live H3 check (a real key and a paid call, with the owner's approval) stays in
  `tasks/open/2026-10-05-minimax-h3-v2-live-check.md`, which was split from PR #1238's ticket.
  That ticket is unclaimed, and its scope shares `apps/api/tests/test_video_media_providers.py`
  with this one. This change only adds a catalog test there.
- Checks run: ruff clean. mypy app (461 files) and mypy tests (367 files) clean. pytest on the
  four media files passed 134. The clips, skills and animation-production tool tests passed 43.
  With the old `clips.mjs` the new clips test fails ("no sheet and no previous frame"), so the
  test does pin the change.
