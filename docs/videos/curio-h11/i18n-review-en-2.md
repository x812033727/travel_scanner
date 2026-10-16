# H11 English localization: independent review, round 2

Reviewed 2026-10-16 (Asia/Taipei). The reviewer did not edit the worksheet, Chinese script, task files, or media.

- Worksheet: `C:\Users\x8120\mokaair-work\videos\curio-h11\i18n\en.todo.json`, SHA-256 `FFC95559075A9A0BBCC7FF7416EE9374EE76C99B97445C42C08251CEEB3EBDD2`.
- Current Chinese source: `docs/videos/curio-h11/video.json`, SHA-256 `4D2AE2A2C3D12D634A1333317FD25A816785B8A44DC6BB6E68C1E27A305532DF`.
- Compared against [round 1](i18n-review-en-1.md), the current Chinese line text, chapter and metadata source fields, the worksheet's glossary and cue boundaries, and the source evidence referenced there.

**Verdict: PASS for English translation quality on these exact hashes.** No new English fix is required. This verdict does not approve the changed Chinese script or narration; the `v0e564e3` source correction still needs the separate source/media approval gates before merging, dubbing, or delivery.

## Six round-1 holds rechecked

| ID | Result |
| --- | --- |
| `v0e564e3` | Chinese source now says four **leaves** (`四葉`), and English says `four leaves`, matching the four leaves named in the original [Hodgins dating report](https://www.voynich.nu/papers/Carbon_GH_2009.pdf). No page/leaf substitution remains. |
| `vc25d396` | `that alone does not mean the paper was retracted` limits the inference to removal of the news release, as in the Chinese source and [Bristol statement](https://www.bristol.ac.uk/news/2019/may/voynich-manuscript.html). |
| `v965353b` | The line now says `columns of marks`; `three columns` is reserved for the following `v81627c3` reveal. |
| `vaa3669c` | Later readers' margin notes come first; separating traces before studying the text comes second, matching both Chinese cue order and narration. |
| `v7cfdf05` | Earlier text patterns come first; the question about similar generated writing follows. `prove` has been removed. |
| `vfc824ec` | The compared English title is now *On the Origin of Species*, as named in the [2013 paper](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0066344). |

## Full-sheet checks

- All 75 line IDs, scene IDs, and Chinese `source` strings match `video.json` in order. All 75 translations are nonempty, include `max_chars`, and stay at or below their individual dub limits. Nine lines exceed the approximate 80-character reading target; seven of those have multiple Chinese cue pieces, and none exceeds its hard dubbing limit. The two single-cue lines are 81 and 83 characters and remain readable in context.
- Seven chapter IDs and source strings, title, description, tags, and all three thumbnail source fields match the current Chinese source. Seven English chapter names are at most 30 characters; the title is 69 characters, has no translated channel name, and the tags stay below 500 characters. The thumbnail preserves its line break and `**` emphasis.
- All 29 declared multi-cue boundaries refer to existing lines and join back to the exact Chinese `source`; English clause and number order was checked against those boundaries. The review found no new reversal, omitted uncertainty, added decipherment claim, inconsistent named person/model, or unresolved metadata field.

H11 English: **meaning 0, facts 0, glossary 0, cue order 0, readability 0 blocking, budget 0, metadata 0, thumbnail 0 fixes** on this revision.
