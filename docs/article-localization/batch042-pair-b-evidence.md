# Batch042 Pair B: technical SEO and learning roadmap

This branch contains 24 localized assets for `technical-seo-checklist` and `seo-learning-roadmap`: 16 editable hero/diagram SVGs and eight 1600×900 JPEG covers. Eight complete zh-CN, English, Japanese and Korean documents are independently reviewed and held outside the repository. The two article JSON files are not modified while source-link PR #942 remains unmerged. Original images and attribution are unchanged.

## Source and candidate versions

The historical read-only inventory (receipt SHA-256 `167d0a345864d1a3ca2117b585e8aaee91e5ef7dcd099954efd65f28e783f29f`) recorded both articles active/published with zh-TW v4 and no four-target-language versions. This is historical inventory, not current production verification. Source PR #942 removes three false AI-glossary links from these two articles without changing visible wording. Translations use that corrected repository source, which still needs live reconciliation before release.

| Article | Corrected source pack SHA-256 | Reviewed final LF candidate pack SHA-256 |
| --- | --- | --- |
| `technical-seo-checklist` | `a5f692c99703c5b15e683fd4543d7438c6179d46042f8336f8abaee6cdcc5e08` | `55f4a7ae7f33fd4b4b6d95fb1e95eb08e881984038ba5f1b45f311dd5bb53f48` |
| `seo-learning-roadmap` | `5d4d982e675e03e7cf3b9840e5ce26488bf7dbc8f54a40f75c7113fdd7635dd5` | `71f1033c6067eba0289ce7e7959100e84086e6c3b1504ef6cc2e582763b11ad4` |

Original candidate bytes are pinned as `e8c957078b059b357feccdb6ea44b3f03a3e519dd9c1ff5adfe277c2ddca2a50` and `3b9b46b26608749c72a483e4c925696e567316bed2e64f04186b46b494c652a0`. The final LF candidates have identical JSON values. The safe installer refuses unmerged/different source hashes or intervening target changes; its dry run currently refuses main because #942 has not merged. No source or candidate was overwritten to bypass that refusal.

## Independent text and visual review

The coordinating agent, distinct from the authors, read both originals and all eight complete translations: titles, descriptions, all 32 blocks, ordered checklists, tables, callouts, image alts/captions and six source titles. Earlier reviewer corrections are retained. Source URLs, checked dates, root metadata, original zh-TW, code/product terms, block order, table/list shape, credits and dimensions are preserved. No further correction was required.

The technical guide keeps access, indexing, rendering, canonical/version selection and reader experience separate; a successful status or test does not prove usability, indexing or ranking. The roadmap retains the Taiwan small-site example and distinctions among impressions, clicks, sessions and actual business actions. Source caveats and the observation range of hours to months are preserved. Remaining ArticleInline targets retain exact kind/slug and resolve only for actually published destination locales.

All 16 SVGs passed browser geometry checks without canvas/card overflow or text overlap. The coordinator inspected all eight final full-resolution diagrams and four final five-language desktop/mobile heading/cover sheets. No missing glyph, overlap, clipping or numeric mismatch was found. All 24 current asset bytes match the historical render receipt, allowing only proven CRLF/LF equivalence for SVGs.

Final standalone local previews cover both articles in all five languages at 1365×900 and 375×812: **20/20 passed**, 32 blocks, six sources and two loaded 1600×900 images per page, with no page errors or horizontal page overflow. These are local HTML previews; they do not establish actual Next.js or production acceptance.

## Portable evidence and checks

Raw receipts, candidates and screenshots remain outside the repository.

| Evidence | SHA-256 |
| --- | --- |
| Historical SVG/raster rendering | `2e46b05af9fdec825f3b4d0fb199b13383596048c85bf8c574b04d468b0c467a` |
| Earlier content audit | `e5a1e1d7bb67ba99b54da74d02045b49ecd815585a285887c762d55a5175b527` |
| Final content and asset bindings | `ba94ef1fd9cba3816be4705b0d9c18fc8d61b77c017e49b17c4857877350247f` |
| Final independent text and visual review | `d23e70caf6cccb02b8c9f79777bfbdbb0c5078928c54fe5ab67ceff1c1472621` |
| Final 20-case local article preview | `4516e9930c9c57c1cf80f9afe8a2fa6179a3f41664cc3298f394f8f1cede9731` |

Scoped candidate pack lint has zero errors; English lengths of 7,347/7,184 characters are advisory and complete paragraphs were retained. Strict intake of the corrected source is **not fully passed**: both start with paragraphs rather than summary blocks, and technical SEO contains two source self-references (limit one). Article targets and SVG numeric checks pass. Final installation must rerun focused content-pack/link tests, scoped lint and current-head CI.

## Remaining stages

`2026-09-28-batch042-pair-b-install-reviewed-locales` tracks guarded installation after #942 merges, exact source hashes match and the source task releases its scopes. This art stage remains a draft review. No database draft import, deployment, publication or live browser verification occurred. Same-image nonproduction rehearsal is unavailable; publication remains NO-GO pending that rehearsal, fresh scoped preflight, source reconciliation, backup/write-control checks, explicit slug/locale dry run and real-route acceptance.
