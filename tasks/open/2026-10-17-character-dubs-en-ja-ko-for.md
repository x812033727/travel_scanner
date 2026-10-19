---
id: 2026-10-17-character-dubs-en-ja-ko-for
title: Character dubs (en, ja, ko) for imported dramas, attached per episode — only after the owner confirms zh-TW
status: in-progress
priority: P2
area: tools
owner: claude-opus-5.5-zt-import-languages
claimed_at: 2026-10-18T14:24:52Z
created_at: 2026-10-17T17:46:56Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/import
  - docs/videos/COMPILATIONS.md
---

# Character dubs (en, ja, ko) for imported dramas, attached per episode — only after the owner confirms zh-TW

## Why

《種田娶妻打天下》episodes 1–24 were made outside the pipeline and reached /admin/videos through
`tools/video/cli.mjs import`, which sends only the 720p preview, the thumbnail and zh-TW CC with
the final cut. Their English, Japanese and Korean dub tracks and CC are finished (one folder per
episode under `~/mokaair-work/videos/zhong-tian-qu-qi-import/`), and the owner already ticked
en/ja/ko (titles, CC, dub) on every episode's language panel, but nothing can send them: the
language panel shows every part as "working" forever, and the owner has no place on the site to
fetch the tracks for Studio.

The 422 `video_locales_dub_not_for_drama` noted on 2026-10-18 does not apply: the import reports
`format: "slides"`, so the server already lets these videos choose a dub. The gap is the tool.

## Definition of done

- [ ] `import --from DIR --languages` sends one hand-pushed `languages` batch for a video the
  command imported, bound to the site's newest final (refused when it is not this folder's cut):
  `description_<l>` from `description.<l>.txt`, `captions_<l>` from `<l>.srt`, `dub_<l>`
  from `dub.<l>.m4a|mp3|wav`, only for the parts the owner ticked.
- [ ] A dub whose length differs from the cut by more than half a second is refused before
  anything is sent.
- [ ] The languages card on /admin/videos lists each language's files to download and waits for
  the owner (`hand_pushed`), and the language states read "ready".
- [ ] All 24 episodes carry their batch on production.

## Steps

- [ ] `languagesBatch` and `importLanguages` in `tools/video/import/import.mjs`, `--languages` in its cli.
- [ ] Tests in `import.test.mjs`.
- [ ] Translated titles and descriptions for the 24 episodes (on the series' production branch).
- [ ] Send the 24 batches; read one back.

## How to verify

`node --test tools/video/import/import.test.mjs`; GET `/api/video/reviews/zhong-tian-qu-qi-e001`
shows a pending `languages` review whose files are `description_*`, `captions_*`, `dub_*`
and whose `languages` states are "ready".

## Notes

Findings, decisions and dead ends, so the next agent does not repeat them.

Design and done criteria: `docs/videos/COMPILATIONS.md`, ticket 5 in「要做的票」. Owner request 2026-10-18: pick episodes in /admin/videos → channel intro + episodes + outro (end-screen layout), CC and dubs merged per language when every episode has them, then the normal publish flow.
