---
id: 2026-09-26-video-i18n-sheet-flags-stale-chapters
title: Video i18n sheet flags stale chapters, title, description and tags
status: done
priority: P2
area: tools
owner: claude-opus-5-5
claimed_at: 2026-09-26T04:44:08Z
created_at: 2026-09-26T04:44:01Z
completed_at: 2026-09-26T04:52:11Z
branch: claude/video-i18n-metadata-hashes
depends_on: []
scope:
  - tools/video/i18n
  - tools/video/core/translations.mjs
  - tools/video/core/lint.mjs
  - tools/video/core/lint.test.mjs
  - .agents/skills/youtube-video/references/prompts/caption-translate.md
  - .agents/skills/youtube-video/references/automated.md
  - docs/videos/DESIGN.md
---

# Video i18n sheet flags stale chapters, title, description and tags

## Why

`node tools/video/cli.mjs i18n-sheet` (#745) writes a translation worksheet per locale. It marks a
caption line `todo: true` when the line's zh-TW text changed, because `i18n-merge` stores each
line's `source_hash` in `docs/videos/<slug>/i18n/<locale>.json`. Nothing else in that file has a
hash. The title, the description, the tags and the chapter titles (keyed by scene id under
`chapters`) are stored as bare text.

On 2026-09-26 the batch 2 videos (branch `claude/video-batch-2`) were re-paced. Chapters were
renamed and added, the zh-TW `youtube.description` got a new opening paragraph, and
`youtube.tags` were reordered. The worksheet marked none of this:

- A renamed chapter kept its old translation. The chapter now called 「ChatGPT 開始有廣告了」 still
  read "Intro".
- New chapters were just empty, with no `todo` flag.
- The description and the tags had no `todo` even though their `source` had changed.

Translators had to be told by hand to redo every chapter. The package step
(`tools/video/package/metadata.mjs`) takes each locale's chapter titles from `chapters` keyed by
scene id. So a chapter that moves to another scene must not leave an orphaned entry behind, and a
renamed chapter's translation must not pass as current.

## Definition of done

- [x] `i18n-sheet` marks the title, the description, the tags and each chapter `todo: true` with an empty `text` when its zh-TW source changed since the merge. That is the same rule lines follow.
- [x] `i18n-merge` records a source hash for each of them. It refuses a sheet made from older zh-TW text, and it writes no chapter entry for a scene that no longer opens a chapter.
- [x] Translation files written before this change still load. Their unhashed entries count as unknown, so the sheet marks them `todo` and lint reports them.
- [x] `lint` warns about stale, unknown and missing title, description, tags and chapters, and about orphaned chapter entries, per locale.
- [x] Tests sit next to the existing i18n and lint tests. `npm run test:tools` passes.

## Steps

- [x] `core/translations.mjs`: the source hash of each field and each field's status (current, stale, unknown, missing), plus the orphaned chapter entries.
- [x] `i18n/cli.mjs`: `buildSheet` uses those statuses for `todo`. `mergeSheet` checks each field's `source` against the script and writes `source_hashes`. The CLI summary names what is left to do.
- [x] `core/lint.mjs`: the new warnings.
- [x] Tests in `i18n/i18n.test.mjs` and `core/lint.test.mjs`.
- [x] Update the translator prompt, `automated.md` and `DESIGN.md` to say the worksheet now flags more than lines. The references are not mirrored under `.claude/skills` (only `SKILL.md` is), so the scope names the `.agents` copies only.

## How to verify

- `npm run test:tools`.
- On a checkout of `claude/video-batch-2`, `node tools/video/cli.mjs lint --slug chatgpt-ads-upgrade` reports the metadata of every locale as unknown. `i18n-sheet --slug chatgpt-ads-upgrade --locale en` marks the title, the description, the tags and all nine chapters `todo`.

## Notes

- **Where the hashes live.** `i18n/<locale>.json` gains `source_hashes: { title, description, tags, chapters: { <scene id>: hash } }`. `title`, `description`, `tags` and `chapters` stay plain text, so `package/metadata.mjs`, `review/sync.mjs` and old files need no change. Tags hash as one ordered list (`textHash(JSON.stringify(tags))`), because the first three become the description's hashtags and a reorder is a real change.
- **Old files.** A file without `source_hashes` loads as before. Its metadata status is `unknown`: lint says "merged before i18n-merge hashed their zh-TW text, so possibly stale", and the sheet marks it `todo` with an empty `text`, like a stale line. So the first `i18n-sheet` after this lands asks every existing locale to redo the title, description, tags and chapters once. That is on purpose. Prefilling an unknown entry would let a sheet-then-merge bless "Intro" for 「ChatGPT 開始有廣告了」 without anyone reading it.
- **Merge is stricter.** A title, description, tags or chapter that is empty, invalid, or made from zh-TW text the script no longer has is reported. It keeps its previous translation and hash, the way lines always did. Before, an empty or over-long title was written over the previous one. `i18n-merge` also reports untranslated tags now (only when the script has tags).
- **Orphans.** Merge writes `chapters` only for scenes that open a chapter now. Lint reports leftover entries in older files ("chapter titles for scenes that no longer open a chapter"). Even without the drop, a leftover entry could not pass as current under the new hashes.
- **Checked against batch 2.** I merged the pre-re-pace `chatgpt-ads-upgrade` (63101419) with its own en metadata to get hashes, then swapped in the re-paced `video.json` (85da5f2c). The sheet marked all 9 chapters (5 renamed, 4 new), the description and the tags `todo`, and kept the unchanged title. Lint named the stale ones, the missing ones and the orphaned `outro`. Linting the branch's current files as they are reports every locale's metadata as unknown.
- **Not done.** A chapter that moves to another scene with its zh-TW title unchanged is translated again instead of carried over. Carrying it over in the sheet would leave the sheet looking done. The automation (`sheetDone` in `automation/flow.mjs`) then skips `i18n-merge`, so the file would never move the entry to its new scene.
