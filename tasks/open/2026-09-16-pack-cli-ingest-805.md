---
id: 2026-09-16-pack-cli-ingest-805
title: pack_cli ingest 不認子主題，805 篇已上線的內容包重跑會被擋
status: open
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-09-16T13:31:06Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/guides/pack_ingest.py
---
# pack_cli ingest 不認子主題，805 篇已上線的內容包重跑會被擋

## Why

`pack_ingest._known_topics()`（`apps/api/app/guides/pack_ingest.py:656-658`）只讀 `LIFE_SEED_TOPICS`：

```python
def _known_topics(kind: Kind) -> set[str]:
    seeds = LIFE_SEED_TOPICS if section_of(kind) == "life" else SEED_TOPICS
    return {slug for slug, _ in seeds}
```

`LIFE_SEED_SUBTOPICS` 整組不在裡面，所以任何帶子主題的內容包跑 `ingest` 都會拿到
`error: topic_unknown: topics not in the life vocabulary: …` 而整篇被擋下。

寫入路徑（`admin_service._resolve_topics`）是接受子主題的，`lint` 也不做這個檢查——
只有 `ingest` 這一關擋。也就是說**站上已經發布、測試全綠的文章，用 repo 自己的工具重跑會失敗**。

2026-09-16 量過：

```
ai-chat 100、claude-code 97、ai-terms 85、codex 61、wordpress 60、web-basics 49、
ai-news 42、gemini-dev 39、ai-coding 36、seo 35、ai-work 31、ai-create 29、
content-marketing 27、woocommerce 20、ai-search 19、ai-safety 16、banking 16、
finance-basics 15、ai-plans 11、ads 11、credit 9、tax-insurance 5
→ 970 篇裡有 805 篇重跑 ingest 會被擋
```

怎麼發現的：`2026-09-16-ai-model-comparison-table` 要用 `["ai", "software", "ai-plans"]`
（跟它的姊妹篇 `ai-api-pricing-comparison-2026` 同一組），被 `ingest` 拒絕。
當時的繞法是先用 `["ai", "software"]` 跑 ingest，再把 `ai-plans` 補回產出的內容包，
`lint`、`test_guides_content_pack` 與 `test_guides_content_links` 都綠。
**那是繞法不是修法**，而且下一個人重跑那篇的 ingest 會再踩一次。

## Definition of done

- [ ] 帶子主題的內容包可以直接 `pack_cli ingest`，不需要先拿掉再補回。
- [ ] `ingest` 認得的主題集合跟寫入路徑（`admin_service._resolve_topics`）一致，
      兩邊將來一起改，不會再各自漂移。
- [ ] 有一個測試會在兩邊不一致時失敗，而不是等到有人跑 ingest 才發現。

## Steps

- [ ] `_known_topics` 併入 `LIFE_SEED_SUBTOPICS`（以及旅遊側對應的子主題，如果有的話）。
- [ ] 確認 travel 側的 `SEED_TOPICS` 有沒有同樣的漏洞，一起補。
- [ ] 加一個測試：拿站上實際用過的主題集合去跑 `_known_topics`，有一個對不上就失敗。
- [ ] 回頭把 `ai-model-comparison-table-2026` 的 `pack.json` 與 `build_pack.py` 裡那行
      「ai-plans re-added after ingest」的繞法註解拿掉，重跑一次 ingest 驗證。

## How to verify

```bash
cd apps/api
uv run python -m app.guides.pack_cli ingest \
  --from ../../docs/content-research --slug ai-model-comparison-table-2026 --dry-run
uv run pytest tests/test_guides_pack_ingest.py tests/test_guides_content_pack.py -q
```

修好以前，上面第一條會回 `topic_unknown: … ai-plans`。

## Notes

不要改 `LIFE_SEED_TOPICS` 或 `LIFE_SEED_SUBTOPICS` 的內容來解決這件事。
`taxonomy.py:70-72` 寫得很明白：那兩個 tuple 是 append-only，
`tests/test_guides_migration.py` 會拿 migration 0075／0076 的清單逐項比對，
搬動任何一個 slug 都會跟線上資料庫對不起來。要改的是 `_known_topics` 這一邊。
