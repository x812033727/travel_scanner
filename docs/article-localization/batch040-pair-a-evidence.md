# Batch040 Pair A: affiliate marketing and store channels

## Completed repository content

`affiliate-marketing-basics` and `independent-store-marketplace` each gain full
zh-CN, en, ja and ko editions: eight documents and 24 localized assets (eight
hero SVGs, eight 1600×900 hero JPGs and eight diagram SVGs). All 33/32 source
blocks, titles, descriptions, tables, callouts, captions, alternative text,
link text and source titles are translated. Existing zh-TW documents, metadata,
category, order, validity, source URLs/check dates, credits and original images
remain unchanged. Code terms and structured article kind/slug targets are kept;
the existing published-locale link resolver decides whether to expose a link.

PR #930's source correction and its task closure in #948 are merged. This branch
was reconciled with main at `e6155e0903cacf488d2c1299adaff5d8f5a56684` before
claiming the two-pack installation task. A stale tracked open copy of the #930
task from the original branch was removed only after checking its completed
copy against main. No active task's scope was overridden.

## Source and production boundary

Corrected source packs were pinned before adding locales: affiliate
`daa111d1f166a0f61c249cc72cb36abea5f3615bd72845dcd46fe197c5b48609`, store channels
`67114b83f6fadb7069815a13916a32a4186fa6e084aa84e84a7fbea0d6a4fa22`.
The historical four-lock read-only receipt `receipt-20260928T133638Z.json`
has SHA-256 `676b67043693c188020e6adf9d5b16bd1e25a4b0a44f8660ed6034fb970dcd0d`.
It observed both articles active/published at article version 2, zh-TW
draft/published version 4 and no target-locale rows, with zero production writes.

That snapshot's affiliate article was still **pre-correction**:
`d8b48acf8b07e6d2175a68bd58ed20bbbb5233bdbf3f91dbf48f089a26e44e32`.
The corrected repository source document is
`c893c8eafcb6b941454590103fbac8359c0db4d29d03e1597a788acac56fc0ce`.
This mismatch must be reconciled through the Batch040 live-source task and a
fresh preflight; a merged source PR does not prove it is live. The store source
matched the historical live snapshot. These records are not fresh deployment
or publication approval evidence.

## Independent review and visuals

The coordinating Codex agent is separate from the drafting subagents and read
all eight target documents against the source. Review included applicability to
Taiwan, the US Amazon example, conditional tracking and payout rules, all cost
examples, customer-data caveats, code terms, URLs, dates and article links.
The store example stays currency-neutral (900−360−90−80−120=250); affiliate
retains the source's explicit NT$ units (1,200×5%×6=360, four eligible sales=240,
less 150 leaves 90). Earlier review removed an unsupported store currency
inference and polished two affiliate English paragraphs. The exact installed
candidates passed this final independent read without additional corrections.

Six original assets and all 24 localized files match the prior artwork audit
and their tracked Git blobs. `artwork-audit-receipt.json` SHA-256:
`8ca7097e7f020597400cef14a95d2db4cd0f4a406819bc1c8173e1ab410d31d1`.
All 16 localized SVG browser-layout cases passed; author and independent visual
review found no clipping, overlap or missing glyphs. `draft-render-receipt.json`
SHA-256: `1a57cdc5b96957b562456acd7a26a4e2e7411fb971e72c04eaccf5d53e9a2d52`.
All eight translated diagrams were also inspected at full resolution.

Final standalone local previews cover both articles in all five languages at
1365×900 desktop and 375×812 mobile: 20 renderings, all 33/32 blocks and eight/seven
sources present, both 1600×900 images loaded, zero console/page errors and no
page-level horizontal overflow. All desktop/mobile first-screen sheets were
inspected. Diagrams and tables use their own scroll containers on mobile.
These are local HTML layout checks, not the Next.js application or production
canonical/hreflang, link or publication acceptance.

## Validation and remaining gates

- Scoped `pack_cli lint`: two entries, zero errors. Both inherit `no_summary`
  warnings; the complete store English body has 7,362 characters, above the
  advisory 6,000 guideline. No content was shortened to silence it.
- `pytest tests/test_guides_content_pack.py tests/test_guides_links.py -q`:
  **15 passed, 11 database-dependent tests skipped** locally. CI must cover DB cases.
- ArticlePack/GuideDocument validation and final structural audit passed for
  ten documents, all protected fields, table/list shapes, links and media.
- Strict editorial intake is **not fully green**: affiliate inherits two source
  failures (first block is not summary; self-reference count 3 exceeds 1), store
  inherits one (first block is not summary). Internal article references and SVG
  numeric checks pass. The separate editorial task records these issues; this
  translation preserves the approved source instead of silently rewriting it.
- CI is pending for the draft PR. Runtime code is unchanged. A partial local npm
  install is not represented as frontend validation.
- No database import, deployment or publication occurred. Release requires the
  unavailable same-image nonproduction Docker rehearsal, source reconciliation,
  fresh conflict checks, backup/health gates, scoped dry-run/import and rerun
  verification, followed by five-language public browser acceptance.

## Exact review binding

Raw receipts and screenshots remain outside the repository. `review-hashes.json`
binds final pack bytes, GuideDocument-normalized SHA-256 values (UTF-8, sorted
keys, compact JSON) and all localized image hashes.

- Final review receipt SHA-256: `0590025b81b3e5b18a658169e9746452f29e7a710cdd83ecaad1abb6c4bc91b0`.
- Final preview receipt SHA-256: `09c314112f27bf35458a56f6f1282dec99f7e8b1314cb8cffb338fff10173421`.

| Pack | Locale | Reviewed document SHA-256 |
| --- | --- | --- |
| `affiliate-marketing-basics` | `zh-TW` | `c893c8eafcb6b941454590103fbac8359c0db4d29d03e1597a788acac56fc0ce` |
| `affiliate-marketing-basics` | `zh-CN` | `e641651be4ae027a4438fe0280e0143ca56ac2b2d0c661dbf3c0c90b8ab2a4ab` |
| `affiliate-marketing-basics` | `en` | `59d903bf04ff70a43be15338b550d4acd07ae187cddd55a407f1c99edef32346` |
| `affiliate-marketing-basics` | `ja` | `81defe39a0b72d6c8713d4cbcee63f653156d081af487ecb880f25f4b2f41d26` |
| `affiliate-marketing-basics` | `ko` | `2fde2eaabb5806bd943b0764a36964820e6593b798f5dda07a891890457a62ef` |
| `independent-store-marketplace` | `zh-TW` | `7cf113f88ce54b02f4e0b096584107bf7fb69093b8d5dd74829222a7d6d03985` |
| `independent-store-marketplace` | `en` | `d5ff72f6812047ca05a76b0bd219524ead5b977a524d960bb163e0c5fa8cc39d` |
| `independent-store-marketplace` | `zh-CN` | `1d8d659551cd1f322a886dc798cd62b481191fe52be6bb87ac74bbf6029e5102` |
| `independent-store-marketplace` | `ja` | `88abca048b9b07fb816ce88b627cc2c0004d25d30b52d30c0a75853fcc7084d5` |
| `independent-store-marketplace` | `ko` | `2deecc52e3e944025ce4a50e5e68703805f80a88425f4c5e486cba78086b4687` |

Final pack SHA-256 values:

- `affiliate-marketing-basics`: `dd37e34388867a41adbeeab51e867a58e770537e979ce9b808013638e13a68e3`.
- `independent-store-marketplace`: `ea35654f174d556f3d4921674c57d7e8359ab3e52d2cfd27b4085dfb5d5558c1`.
