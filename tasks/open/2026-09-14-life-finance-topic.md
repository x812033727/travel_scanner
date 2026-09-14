---
id: 2026-09-14-life-finance-topic
title: 生活分享新增 finance 主題（taxonomy 與 seed migration）
status: open
priority: P1
area: api
owner:
claimed_at:
created_at: 2026-09-14T11:45:30Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/guides/taxonomy.py
  - apps/api/migrations/versions/0075_finance_topic.py
  - apps/api/tests/test_guides_migration.py
  - apps/web/lib/guide-affiliate.test.ts
---

# 生活分享新增 finance 主題（taxonomy 與 seed migration）

## Why

財經系列（[`docs/life-finance-series.md`](../../docs/life-finance-series.md)，120 篇）要用一個
`finance` 主題。生活分享的詞彙今天只有 `ai`、`tutorial`、`software`、`gadgets`、`productivity`、
`daily`、`misc` 七個，沒有財經類；`pack_ingest._known_topics` 讀的就是 `LIFE_SEED_TOPICS`，
所以在這張票落地前，**每一篇帶 `finance` 的內容包都會被 `topic_unknown` 擋下來**，六個批次一篇都進不來。

主題還是只能用 seed migration 新增——沒有寫入端點，那件事在
`tasks/open/2026-09-12-guide-topic-admin-crud.md`。

## Definition of done

- [ ] `apps/api/app/guides/taxonomy.py` 的 `LIFE_SEED_TOPICS` **末尾附加**一列（不是插在中間）：
      `("finance", ("Money & finance", "お金・家計", "돈・재테크", "理財與金錢", "理财与金钱"))`。
      五語系標籤齊全（`seed_names` 對 `LOCALES` 用 `strict=True`）。
- [ ] 新增 `apps/api/migrations/versions/0075_finance_topic.py`，`down_revision = "0074_lifestyle_guides"`。
- [ ] `uv run alembic heads` 只有一個 head；upgrade → downgrade → upgrade 都過。
- [ ] `apps/web/lib/guide-affiliate.test.ts` 裡列出七個 life slug 的那一行加上 `finance`（順手，不是必要）。
- [ ] `test_guides_migration.py`、`test_guides.py`、`test_guides_content_pack.py` 全綠。

## Steps

### 1. migration 的形狀

照 `0074_lifestyle_guides.py` 的 `_seed_life_topics()` 抄，但**範圍小得多**：
`section` 欄與兩個 CHECK 都是 0074 建好的，這張票**不動任何 CHECK、不動任何欄位**，
只 insert 一列 `guide_topics`。要保留 0074 的三個性質：

- [ ] `if context.is_offline_mode(): return` 擋在 seed 前面。
- [ ] 先 `SELECT slug FROM guide_topics`，**只插入不存在的 slug**——重跑是 no-op，
      也不覆寫管理員改過的東西（0072 的契約）。
- [ ] `FINANCE_SEED_TOPICS` 的五語系標籤**寫在 migration 檔案裡，不要從 `app.guides.taxonomy` import**。
      0074 也是這樣：migration 必須在應用常數之後再改時仍然跑得動。
- [ ] 欄位：`section="life"`、`source="seed"`、`is_active=True`、`display_order=270`（0074 用到 260）、
      `uuid4()` id、`datetime.now(UTC)`。
- [ ] `downgrade()` 先刪 `guide_article_topics` 的關聯再刪 topic（SQLite 沒有 pragma 時不串聯）。
      **條件是 `slug = 'finance' AND source = 'seed'`，不是 `section = 'life'`**——
      0074 刪的是全部 life seed 主題，這裡照抄會把 AI 系列的七個主題一起清掉。
- [ ] 沒有新欄位、沒有 `batch_alter_table`，所以沒有 `if "x" not in columns` 分支，
      `tests/test_migration_dead_branches.py` 不需要為它加 case。

### 2. 會壞掉的那個測試（重點）

`apps/api/tests/test_guides_migration.py` 的
`test_the_seeded_life_topics_match_the_python_vocabulary` 斷言的是**完全相等**：

```python
module = migration("0074_lifestyle_guides")
assert [(slug, labels) for slug, _, labels in module.LIFE_SEED_TOPICS] == list(LIFE_SEED_TOPICS)
```

一旦 `taxonomy.py` 多了 `finance`，0074 的清單就不再等於它，**這個測試會紅**。

- [ ] 把它改成把 0074 與 0075 的 seed 清單**依序串起來**再比對，例如
      `(*m0074.LIFE_SEED_TOPICS, *m0075.FINANCE_SEED_TOPICS)`。
      依序串接只有在 `taxonomy.py` 是**附加**而不是插入時才成立——這就是上面要求附加的原因。
- [ ] 新增一個測試跑 0074 → 0075：`finance` 以 `section="life"`、`display_order=270` 落地；
      重跑 0075 是 no-op；downgrade 先移除關聯再移除 topic，且**不影響 0074 的七個主題**。
- [ ] `test_guides.py` 不用改（`test_the_two_seed_vocabularies_stay_disjoint` 只看互斥與長度，
      display_order 的 fixture 是從 tuple 索引推出來的），**也不要把它加進 scope**——
      那個檔案被 `2026-09-12-guide-topic-admin-crud` 佔著，加了會互卡。

## How to verify

```bash
cd apps/api && uv run alembic heads          # 只有 0075_finance_topic
cd apps/api && uv run alembic upgrade head && uv run alembic downgrade -1 && uv run alembic upgrade head
cd apps/api && uv run pytest tests/test_guides_migration.py tests/test_guides.py \
  tests/test_guides_content_pack.py tests/test_migration_sql_dialect.py -q
cd apps/api && uv run ruff check . && uv run mypy app
npm run test:web
```

落地後這段應該能通過（在還沒有任何財經內容包時，它只是證明詞彙認得 `finance`）：

```bash
cd apps/api && uv run python -c "from app.guides.pack_ingest import _known_topics; print('finance' in _known_topics('life'))"
```

## Notes

- **前端不用改。** 主題標籤由 API 從資料庫的 `names_json` 讀回（`taxonomy.topic_label`），
  `apps/web` 正式程式碼沒有硬寫死的 life topic 清單，`/life` 的篩選晶片是跟
  `/guides/topics?section=life` 要的。`check:i18n` 不受影響（沒有新增訊息鍵）。
- `/life` hub 的介紹文（`common.json` 的 `lifeHubIntro`、`metadata.json` 的 `lifeDescription`）
  現在寫的是 AI 工具與生活雜記，沒有提財經。**等批次 01 上線後再改**，那要動五個語系的同一個鍵，
  現在改等於為零篇文章做五語系文案。另開一張小票即可。
- migration 只 insert 資料列，先於任何內容部署是安全的；0074 的 docstring 記的是反過來的陷阱
  （新 API 先於 migration 啟動），這裡不適用。
