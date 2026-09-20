---
id: 2026-09-20-correct-hong-kong-tram-luggage-guidance
title: Correct Hong Kong tram luggage guidance
status: done
priority: P1
area: docs
owner: codex-article-localization
claimed_at: 2026-09-20T09:04:25Z
created_at: 2026-09-20T08:51:01Z
completed_at: 2026-09-20T10:51:10Z
branch: codex/hong-kong-tram-luggage-source
depends_on: []
scope:
  - apps/api/app/guides/content/hong-kong-ferry-tram-day.json
---

# Correct Hong Kong tram luggage guidance

## Why

The published Traditional Chinese Hong Kong ferry/tram guide suggests that a
traveller with large luggage only needs to consider whether boarding is easy.
Hong Kong Tramways' passenger notice instead prohibits luggage above 7 kg in
weight or 30 litres in volume, and also permits the motorman to refuse goods
that would inconvenience other passengers. The guide must state the actual
rule before any new-language translation is released.

## Definition of done

- [x] The published zh-TW guide describes both luggage limits and the
      motorman's judgement, and tells readers with prohibited or unconfirmed
      luggage to use other transport.
- [x] Existing editorial metadata, article identity, images and other source
      checks remain unchanged; the corrected source version is available to
      the localization baseline before Hong Kong target locales publish.

## Steps

- [x] Verify the current Hong Kong Tramways passenger notice in English and
      Traditional Chinese.
- [x] Correct the two relevant paragraphs and update only the checked date
      and title of the already-cited passenger notice source.
- [x] Validate `ArticlePack`, exact changed JSON pointers and focused tests.
- [x] Merge the guarded PR, update the live zh-TW source, then repin the Hong
      Kong translation baseline before dependent locale publication.

## How to verify

Run `ArticlePack.model_validate` and compare normalized document hashes; run
`pytest tests/test_guides_content_pack.py tests/test_guides_content_links.py -q`
inside `apps/api`, `npm run check:tasks` and `git diff --check`. At publication,
compare live source version/hash with the pinned preimage before writing and
verify the resulting public zh-TW paragraph and source date.

## Notes

Based on `origin/main` commit `3bb3b7b979e304b473b8c9fb18ccf1b569aa044d`.
The original pack SHA-256 is
`208d95f876e63edac1e2a87b1b6741a7492005882e4a55de9795859263d5bc43`;
the corrected pack SHA-256 is
`de6ab95f2f85bfa3bb38b6db2d1f73b2380e9a73eda4db4164f3158cbdc4bc7a`.
Normalized zh-TW document SHA-256 changes from
`e03a3b07c6db7fe01b768d81410d15985ee8cbcb406e6939ad74b30f0137759d`
to `e59b60f8ca4b19233820cc03e9126ddb0c4a29c70b06bed79ec43a3e359c5efa`.
Only `blocks[6].text`, `blocks[17].text`, `sources[2].title` and
`sources[2].checked_on` changed; the last date is `2026-09-20`.

Official [Traditional Chinese passenger notice](https://www.hktramways.com/tc/notice-to-passengers)
item 9 expressly prohibits luggage exceeding either the 7 kg or 30 litre
threshold and goods the motorman considers inconvenient to others. The
existing [English notice](https://www.hktramways.com/en/notice-to-passengers)
remains the article's source URL; its check date was refreshed after reading
both official language versions. Do not infer publication from this repository
change: the last pinned production snapshot had zh-TW locale version 6 and
the old document hash, and a new snapshot is required before a live write.

Independent source review tightened the motorman condition to the official
Traditional Chinese meaning, `會對其他乘客構成不便`, rather than the narrower
`妨礙其他乘客`; the final pack and document hashes above reflect that revision.
- PR #590 merged as `968f7b8e56be8d92c03b4f4369d56e8e5ae77641`; the guarded deployment and verified backup completed.
- The public zh-TW locale is version 8 with published and draft normalized document SHA-256 `e59b60f8ca4b19233820cc03e9126ddb0c4a29c70b06bed79ec43a3e359c5efa`. Signed-out browser verification confirmed the corrected luggage rule and source date. The dependent four-language job is rebased to this exact live source.
