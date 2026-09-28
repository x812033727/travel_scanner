---
id: 2026-09-28-video-dubs-zh-cn-is-not
title: Video dubs: zh-CN is not dubbed by default, only when chosen
status: in-progress
priority: P2
area: tools
owner: claude-opus-5-5
claimed_at: 2026-09-28T09:53:44Z
created_at: 2026-09-28T09:53:25Z
completed_at:
branch: claude/relaxed-wright-18jppu
depends_on: []
scope:
  - tools/video/dubs/plan.mjs
  - tools/video/dubs/cli.mjs
  - tools/video/core/stages.mjs
  - tools/video/package/cli.mjs
  - tools/video/dubs/dubs.test.mjs
  - tools/video/core/stages.test.mjs
  - tools/video/package/package.test.mjs
---

# Video dubs: zh-CN is not dubbed by default, only when chosen

## Why

The owner (2026-09-28): a Simplified Chinese dub is not needed by default, because it sounds
the same as the Traditional Chinese narration. When nobody chose the dub languages (`dub`
without `--locale`, or a work directory with no `languages.json`), the tools used every dub
locale, zh-CN included, and spent a Gemini voice run on a track that adds nothing.

## Definition of done

- [x] `dub --slug S` with no `--locale` makes en, ja and ko, not zh-CN.
- [x] `captions` and `package` without a language choice leave zh-CN out of the dubs too.
- [x] `dub --locale zh-CN` and a zh-CN dub ticked on /admin/videos still work.

## Steps

- [x] `DEFAULT_DUB_LOCALES` in `tools/video/dubs/plan.mjs` (every dub locale but zh-CN).
- [x] The three no-choice fallbacks use it: `dubs/cli.mjs`, `core/stages.mjs`, `package/cli.mjs`.
- [x] Test in `dubs/dubs.test.mjs`: a dry run without `--locale` lists en, ja, ko and no zh-CN.

## How to verify

```bash
node --test tools/video/dubs/dubs.test.mjs tools/video/core/stages.test.mjs tools/video/package/package.test.mjs
npm run test:tools
```

## Notes

- The admin language panel already pre-ticks no dub at all ("tick the defaults" sets dub off),
  so nothing changed on the site; zh-CN captions and metadata are unaffected.
- `DUB_LOCALES` stays the set `--locale` accepts; only the default narrowed.
- Claimed with `--force`: the overlapping claims (2026-09-26-video-dubs-worker,
  2026-09-27-video-languages-skill-docs) are stale review tasks whose work landed in #870.
