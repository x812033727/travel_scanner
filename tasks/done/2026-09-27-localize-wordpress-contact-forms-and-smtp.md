---
id: 2026-09-27-localize-wordpress-contact-forms-and-smtp
title: Localize WordPress contact forms and SMTP guides batch029
status: done
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-09-27T09:35:08Z
completed_at: 2026-10-07T01:43:02Z
branch: codex/article-localization-batch029-contact-pair-a
depends_on: []
scope:
  - apps/api/app/guides/content/wordpress-contact-forms.json
  - apps/api/app/guides/content/wordpress-smtp-delivery.json
  - apps/web/public/guides/wordpress-contact-forms
  - apps/web/public/guides/wordpress-smtp-delivery
---

# Localize WordPress contact forms and SMTP guides batch029

## Why

The published WordPress contact-form and mail-delivery guides currently exist only in Traditional Chinese. Readers selecting English, Japanese, Korean or Simplified Chinese need the complete instructions and language-specific text in both figures. These two guides form Pair A of the four-article Batch029 contact/booking group; another owner handles the two disjoint Pair B articles. Publication is a separate guarded release task.

## Definition of done

- [x] `wordpress-contact-forms` and `wordpress-smtp-delivery` each have complete en, ja, ko, zh-CN documents, including titles, descriptions, paragraphs, list, table, callout, conditional link labels, image alt/caption and source titles.
- [x] Each target locale references its own `hero-<locale>.jpg` and `diagram-1-<locale>.svg`; localized hero SVG/JPG and diagram SVG render with no overflow, overlap, missing glyph or wrong numeric detail.
- [x] Original zh-TW documents, source assets, article metadata, links, URLs, checked dates and visibility are preserved. Target links remain conditional on actual destination locale publication.
- [x] Independent Pair B review of these eight documents and 24 image assets passes; scoped lint, structural/source checks and appropriate repository tests pass before integration.

## Steps

- [x] Claim four exact content/asset paths and bind current live source and assets.
- [x] Translate all reader-visible strings without shortening source claims or inferring nationality from language.
- [x] Render and inspect all new images, review with Pair B owner, and repair findings.
- [x] Hand off reviewed bytes and hash-bound receipt to the Batch029 integrator; do not publish or open a separate content PR without coordination.

## How to verify

Run `uv run python -m app.guides.pack_cli lint --slug <slug>` for both slugs from `apps/api`; inspect a normalized source/target field comparison, all rendered images, link destinations and immutable original hashes. Run `npm run check:tasks`, API ruff/mypy and relevant frontend checks before the combined PR. Production dry-run, backup, publication and browser QA are outside this drafting task.

## Notes

Production source captured 2026-09-27T09:29:15Z in a `REPEATABLE READ, READ ONLY` transaction: both articles published, active, unexpired, article v2, zh-TW draft/published v4; all four target-locale DB rows absent. Full snapshot SHA-256 `2557112824db91c3eff0365927d48230d42aee65c7c3a09f13c5d8a0ac6b731d`; comparison receipt SHA-256 `3331a9013922e6549c7c399075d27d760135c9f30590d4634eda2b887d0ef850`; twelve original host assets match Git SHA-256 (`4e761853fbc52f0902637c39653ed5f632865b2c591234636882c45d7f9fd70f`). Evidence directory: `C:/Users/x8120/.codex/article-localization-release/batch029-contact-inventory`. Source comparison used main `e97172c297f537170f19fbe6e4813c505a22893a`; latest starting main `bd98f4678ddc786ef1b058d30a950b36e11ec586` has no changes to these four article/asset paths. Recheck before production release.

Current source references `wordpress-user-roles` and `wordpress-plugin-theme-translation` from the contact-form article and `wordpress-contact-forms` and `dns-records-troubleshooting` from the SMTP article. Do not turn unpublished target-locale destinations into clickable public links. Keep Contact Form 7, WordPress, Flamingo, Turnstile, WP Mail SMTP, Brevo, DNS record names, `your-email`, `[your-email]`, `Mail (2)`, `Reply-To`, `do_not_store`, `flamingo_email`, `flamingo_name`, `flamingo_subject`, `From Email`, `From Name`, `Force From Email`, `SMTP & API`, `API Key`, `Email Test`, `Debug Events` and `message ID` accurate. The source explicitly targets Taiwan small-site owners; do not recast translations as guidance for readers of a presumed nationality.

Pair A author receipt: `C:/Users/x8120/.codex/article-localization-release/batch029-contact/pair-a/author-receipt.json`, SHA-256 `b5e8f41578988d98e1c657034936ba79aef7ddf400cc738ed15d1d61fafc7e2b`. Edge-measured 16 localized SVG layouts pass: `browser-layout-review.json`, SHA-256 `452d2fb2107873b928c3898bd5fe7fcc0d9aa129c8ba9b548e96df62c5715b1b`; all eight hero JPGs were rerendered in Edge and four updated contact sheets were visually inspected. Pair B independent structural/editorial review passes: `C:/Users/x8120/.codex/article-localization-release/batch029-contact-pair-b/pair-a-structural-review.json`, SHA-256 `e46950db6f336ffb6e6778ef56b14b1aa1b8363451481134e5f7da54c9f8b1eb`. Both scoped pack lints pass with only inherited `no_summary` and an English body-length advisory. Relevant API tests: 69 passed, 2 skipped. `npm run check:i18n` and `npm run check:tasks` pass; root-level `tools/*.test.mjs` passes 96 tests and skips 1. Full `npm run test:tools` still fails 17 unrelated `tools/video/**` test files in this Windows checkout; they exit before reporting assertions. No PR, production import, publish or deployment has occurred for this pair.

## 2026-10-07 看板總整理（由站主授權，非原持有者）

標記完成。依據：All DoD ticked; content integrated via PR #857 (merged); wordpress-contact-forms.json & wordpress-smtp-delivery.json have 5 locales, localized diagram-1-<loc>.svg/hero-<loc>.jpg present; publication recorded in tasks/done/2026-09-27-record-batch029-five-language-wordpress-contact.md
