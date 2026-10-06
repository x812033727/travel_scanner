---
id: 2026-10-05-localize-ai-income-investing-batch
title: Localize the AI income and investing batch into en, ja, ko and zh-CN
status: open
priority: P3
area: docs
owner:
claimed_at:
created_at: 2026-10-05T08:07:40Z
completed_at:
branch:
depends_on:
  - 2026-10-05-life-ai-income-investing-batch
scope:
  - docs/article-localization/ai-income-investing
---

# Localize the AI income and investing batch into en, ja, ko and zh-CN

## Why

`2026-10-05-life-ai-income-investing-batch` shipped twelve articles in zh-TW only, as most
of the AI and finance series do. The `/ai` hub reaches readers in five languages; these
articles are absent from the other four.

## Definition of done

- [ ] The twelve packs carry en, ja, ko and zh-CN, translated and reviewed per locale through
      skill `article-localization`, and released with its receipts.
- [ ] The finance pieces keep their disclaimer as the last block in every locale (the
      finance lint keys on the zh-TW marker; check what it keys on for the other locales
      before translating).

## Notes

Start only after the zh-TW batch is published on the site; the localization pipeline
snapshots the published article.
