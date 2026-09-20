---
id: 2026-09-20-correct-hanoi-old-quarter-source-sentence
title: Correct Hanoi Old Quarter source sentence
status: in-progress
priority: P2
area: docs
owner: codex-batch005-author
claimed_at: 2026-09-20T13:08:25Z
created_at: 2026-09-20T13:07:41Z
completed_at:
branch: codex/hanoi-source-sentence
depends_on: []
scope:
  - apps/api/app/guides/content/hanoi-old-quarter-walking-guide.json
---

# Correct Hanoi Old Quarter source sentence

## Why

The already-published zh-TW Hanoi Old Quarter walking guide has a broken final
sentence in paragraph block 11: “避開管理上” is not a complete expression. It
weakens otherwise clear advice to respect on-site restrictions and avoid
restricted railway areas. The four drafted translations already convey the
intended meaning, so the published source needs a small, version-guarded edit.

## Definition of done

- [x] Only the final sentence of zh-TW `/blocks/11/text` is made grammatical,
      preserving the advice, document structure, sources and all other prose.
- [x] ArticlePack schema validation and an exact scalar-path diff pass.
- [ ] A narrow source-correction PR is open for independent review.

## Steps

- [x] Read the current published source and compare all four drafted locales.
- [x] Confirm the existing safety advice against a primary Hanoi city source.
- [x] Change only the one source sentence and check normalized hashes.
- [ ] Run focused checks and open a PR. Do not publish or import locales.

## How to verify

Validate this pack with `ArticlePack.model_validate_json`. Compare its
pre/post normalized scalar leaves and require only
`/locales/zh-TW/blocks/11/text` to differ. Run focused content-pack tests,
`npm run check:tasks` and `git diff --check`. Before any later production
write, independently recheck the live article/locale versions and hashes.

## Notes

Read-only production capture at 2026-09-20T13:00:43Z found article v1,
published/active, and only zh-TW locale v6/published v6. Published and draft
document SHA-256 both equal
`7414980741ec969be8132a476130d6fb725ac6e079594b4b993823235b84d3d0`;
the current pack's raw SHA-256 is
`c961e441a75d7a26484482cad21da47666bebf16dc451b2afc6be2c40a5bb2a9`.
The read-only capture SHA-256 is
`6fecc19eedb5c6488b0fa020bb07eeb8ec757f50fbf240d49c03b5fad79f8fd4`.

The final sentence changes from “旅行照片的價值不應建立在闖入不開放區域，或跟著陌生人避開管理上。”
to “不應為了拍旅行照片闖入未開放區域，也不應跟著陌生人躲避現場管制。”
Everything before that sentence is unchanged. The four Batch006 draft
translations already express the same caution; they are not changed here.
ArticlePack validation passes and the only normalized scalar difference is
`/locales/zh-TW/blocks/11/text`. Proposed document SHA-256 is
`40be374880818890c3016859283ac18a94723a69a77dbb251ad7b305018ca942`;
new raw pack SHA-256 (LF-normalized Git bytes) is
`90994557776b210159dceb0a7e9e0d249585d9de6bf43b71e20d04bce2345906`.

Vietnam's official tourism Old Quarter page supports the walking and weekend
pedestrian context, while a Hanoi city police report specifically supports
keeping visitors out of restricted railway corridors:
`https://hanoi.gov.vn/tin-so-nganh/trien-khai-mo-hinh-vanh-dai-an-toan-duong-sat-4250407154648115.htm`.
This grammar edit adds no new safety rule or route claim. The existing
`https://vietnam.travel/places-to-go/northern-vietnam/ha-noi` source URL
currently returns HTTP 404, a separate pre-existing link issue.
It remains unresolved in this PR and should be handled under a separate
source-link task after this version-guarded correction.

Publication impact: the current Batch006 four-language jobs are pinned to the
old source/pack hashes. If this PR is merged and the zh-TW correction is
published, those jobs must be rebound to the new live version and independently
reviewed before importing or publishing translations. This PR must not publish
the source or the four drafted locales.

Focused verification: `test_guides_content_pack.py` and
`test_guides_content_links.py` completed with 12 passed, 5 skipped;
`npm run check:tasks` validated 636 task files (only unrelated existing
warnings), and `git diff --check` passed.
