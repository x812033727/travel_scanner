# Batch 035: newsletter pair A

This review batch adds zh-CN, en, ja, and ko documents to two already-published zh-TW lifestyle guides:

| Article | Published source | Target documents | Localized assets |
| --- | --- | ---: | ---: |
| `mailchimp-wordpress-newsletter` | zh-TW v4, pack SHA-256 `fa14992d47a97aa2baa74a6d590f5c9f48f5a75ab167a83a05d7f699516133d6` | 4 | 12 |
| `email-newsletter-planning` | zh-TW v4, pack SHA-256 `255393b9f653fda9ccda7058511fa0c2f92d809b0fc5ae2ab169ba173866ea39` | 4 | 12 |

The source article identity is v2 in the 2026-09-28 read-only production inventory. Both published source documents matched their repository packs. The inventory's Git base was `e36db07bbb1a511046def7c42cd6978f3888cc52`. Immediately before this PR, `origin/main` was `55e75518e147adcf54dcdda7055be1e79fef4262`; neither source pack nor either source asset directory changed between those refs.

Each target retains the original 33-block structure, all source URLs and `checked_on` dates, image credits, article-reference slugs/kinds, ordering, topics, visibility, and root metadata. Titles, descriptions, all body text, list and table cells, callouts, image captions and alt text, link text, and source titles are localized. The original zh-TW document is structurally identical to `origin/main`.

The four target languages each have an editable `hero-<locale>.svg`, a rendered 1600×900 JPEG companion, and a 1600×900 `diagram-1-<locale>.svg` per article. SVG text was measured against the available width and rendered; all eight diagrams, eight SVG covers, and eight JPEG covers were visually checked in contact sheets for overlap, clipping, missing glyphs, and dimensions. Diagram labels use at least 18 SVG px before the article's 1180/1600 display scaling. Original Mokaair author/license credits remain.

All referenced destination articles had only zh-TW published in the read-only inventory. The target documents retain `article` inlines with translated text. The API's `resolve_article_links` includes only published documents in the reader's locale, and the frontend renders a missing target as plain text. Thus these references are non-clickable until that destination language is actually published; they then use the same-language path.

Validation:

- `uv run python -m app.guides.pack_cli lint --slug mailchimp-wordpress-newsletter --slug email-newsletter-planning`: passed. Existing no-summary guidance remains for the zh-TW source and its translations. Complete English translations exceed the optional 6000-character life-guide guideline; they were not shortened at the expense of source details.
- `uv run pytest tests/test_guides_content_pack.py tests/test_guides_content_links.py tests/test_guides_pack_ingest.py -q`: 67 passed, 5 skipped.
- `npm run test --workspace @travel-scanner/web -- components/content-blocks.test.tsx`: 65 passed.
- `npm run check:i18n`: validated five locales across 25 namespaces.
- `npm run check:tasks`: exit 0, with unrelated existing stale/overlapping-task warnings.
- Independent structural/image audit: zh-TW and root metadata unchanged; 4 target locales per article, 33 blocks, unchanged source URLs/dates and link slugs, 24 existing 1600×900 language assets, and preserved key numbers (`4.12.0`, `400`, `20`, `5%`, `6`). Audit receipt SHA-256: `10ec622c383ecb3f1db01b0f467bd8c4a4407fc80cddaca31f9e0a7f8c4009e5`.

Editorial follow-up corrected the Japanese and Korean Mailchimp table's *email address/list* wording, the Korean planning guide's generic identity-number example, and the Japanese planning diagram's suppression wording. The revised diagram was rendered again at 1600×900 and visually checked. Pack lint, structural/image audit, `git diff --check`, and the targeted API tests passed after these corrections.

This PR is content and artwork only. It does not import drafts, publish locales, deploy assets, or claim browser verification.
