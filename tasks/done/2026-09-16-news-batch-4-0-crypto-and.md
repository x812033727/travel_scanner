---
id: 2026-09-16-news-batch-4-0-crypto-and
title: News batch 4.0: crypto and tech-news topics, migration 0079 and retopic rules
status: done
priority: P1
area: api
owner: claude-opus-5
claimed_at: 2026-09-16T11:27:59Z
created_at: 2026-09-16T11:27:54Z
completed_at: 2026-09-16T14:16:09Z
branch: claude/brave-hopper-8ezxba
depends_on: []
scope:
  - apps/api/app/guides/taxonomy.py
  - apps/api/app/guides/retopic.py
  - apps/api/migrations/versions/0080_crypto_and_tech_topics.py
  - apps/api/tests/test_guides_migration.py
  - apps/api/tests/test_guides_retopic.py
  - docs/article-architecture.md
---

# News batch 4.0: crypto and tech-news topics, migration 0079 and retopic rules

## Why

站主要求新增近期的 AI、科技與幣圈新聞（1/1 起的重要新聞、8/1 起的次要新聞，五語）。
站上已有 38 篇 `ai-news-*` 與月份索引，但**幣圈 0 篇**，非 AI 的科技新聞也只有
`ai-news-nvidia-rubin-20260105` 與 `ai-news-siri-ai-ios-27-20260914` 兩篇沾到邊。

兩個垂直都沒有主題可掛。`ai-news` 是 `ai` 的子主題，幣圈與科技新聞需要對應的位置，
否則文章進不了任何 hub、`/life` 的「最新新聞」列也看不到它們，
`retopic` 更沒有規則可以歸檔。這張票只做詞彙與規則，不寫任何文章。

## Definition of done

- [x] `crypto` 掛在 `finance` 底下，`tech-news` 掛在新父主題 `tech` 底下，五語標籤齊備。
- [x] migration `0079` 種子這三個 slug，re-run 是 no-op，downgrade 只刪自己這三筆。
- [x] `retopic` 認得 `tech-news-*` 與 `crypto-news-*`／`bitcoin-*`／`stablecoin-*`，
      且**既有 845 篇一篇都不會被改**。
- [x] `docs/article-architecture.md` 的詞彙表與「維持單層」那段同步。

## Steps

- [x] `taxonomy.py`：`LIFE_SEED_TOPICS` append `tech`；`LIFE_SEED_SUBTOPICS` append
      `tech-news`、`crypto`；`LIFE_TOPIC_DESCRIPTIONS` 補三段 hub 導言。
- [x] `0080_crypto_and_tech_topics.py`：形狀照 `0075`（純種子、不動 schema）＋ `0076` 的
      `parent_id`／`descriptions_json` 種子迴圈。display_order 接在 0076 的 520 之後：
      `tech` 530、`tech-news` 540、`crypto` 550。
- [x] `test_guides_migration.py`：四處要改，見 Notes。
- [x] `retopic.py` 加兩條 `Rule`，`test_guides_retopic.py` 加對應斷言。

## How to verify

```bash
cd apps/api
uv run pytest tests/test_guides_migration.py tests/test_guides_retopic.py -q
uv run python -m app.guides.pack_cli retopic --kind life     # 必須是 0 of 845 packs would change
uv run ruff check . && uv run mypy app
```

## Notes

**為什麼 `crypto` 掛在 `finance`、`tech` 卻是新父主題。**
`crypto` 是同一個 YMYL 主題、同一條免責規則（`pack_ingest.finance_no_disclaimer`），
`finance` 的 hub 導言本來就寫著「只講制度與方法，不推薦商品」，
而 `docs/life-finance-series.md` 規劃的六篇加密貨幣入門本來就掛在 `finance`。
另開一個頂層幣圈樹等於把這些全部複製一份。
`tech` 則是沒有地方可掛：`gadgets` 是 3C 裝置、`software` 是 App，
晶片、電信與平台法規兩邊都不是，而 `docs/article-architecture.md` 寫明那五個維持單層——
新增父主題才不會抵觸那條決策。

**`test_guides_migration.py` 有四處會壞，不是加一行就好：**

1. `LIFE_SEED_MIGRATIONS` 要加 `0079`。
2. `test_0076_...` 的 `travel, life, finance, hierarchy = modules` 會變成 5 拆 4 的
   `ValueError`——改成明確的名字 tuple，不要跟著 `LIFE_SEED_MIGRATIONS` 展開。
3. `test_the_seeded_sub_topics_match_the_python_vocabulary` 原本只讀 0076 一個模組。
   改成跨 `LIFE_SUBTOPIC_MIGRATIONS` 串接，並斷言各 revision 的 `TOPIC_DESCRIPTIONS`
   **key 互斥**——互斥才是「合併順序無所謂」的理由。
4. **合併後的 display_order 不再全域遞增。** 舊斷言是
   `orders == sorted(orders)`（parents 全部 + 0076 的 children），
   0079 的 parent 在 530、0076 的 children 到 520，串起來就是 `530` 之後接 `300`。
   那條斷言原本只是「每個 revision 都先種 parent 再種 child」的副作用。
   改成它真正要守的兩件事：全域唯一，且**每個 revision 自己遞增、起點高於前一個 revision 的最大值**。
   `test_the_seeded_life_display_orders_do_not_collide` 被新的那條涵蓋，已併入移除。

**`retopic` 不會替 `crypto` 補 `finance`。** `retopic.py:531` 的
`LIFE_SEED_TOPICS[:8]` 是原本的八個父主題（含 `finance`），規則只會替
`website`／`marketing` 這兩個後來新增的補父層。所以：
- `tech` 是新父主題 → `tech-news-*` 會自動帶到 `tech`。
- `crypto` 的父是 `finance`，屬於原本八個 → **不會**自動帶到 `finance`。

這就是 `pack_ingest.FINANCE_TOPICS` 必須單獨列出 `crypto` 的原因：
不能指望父主題會到位，否則幣圈文章會整批逃過免責規則。
兩邊的註解互相指到對方，改一邊時才看得到另一邊。

**驗過的：** `pack_cli retopic --kind life` 是 0 of 845 packs would change
（新規則對既有內容完全惰性）；`lint --kind life` 0 error；
`test_guides_migration` 17 passed、`test_guides_retopic` 6 passed；`ruff check`、`mypy` 全過。
0079 的測試做過變異驗證：把 `crypto` 的 parent 改錯會 `KeyError`，確認不是空轉。

**還沒做、屬於別張票的：** `apps/web/app/[locale]/life/page.tsx` 的
`LIFE_NEWS_TOPIC = "ai-news"` 是單一字串，`/life` 的「最新新聞」列只會顯示 AI 新聞。
幣圈與科技新聞要出現在那一列，需要改成讀三個子主題——另開一張 web 票。

## 改號紀錄（2026-09-16）

原本是 `0079_crypto_and_tech_topics`，**與 PR #537 的 `0079_guide_news_date` 撞號**
（兩個都接在 `0078_guide_article_links` 之後，`alembic upgrade head` 會看到兩個 head）。
#537 先合併，所以這一支改成 **`0080_crypto_and_tech_topics`** 並把 `down_revision`
接到 `0079_guide_news_date`——正是 #537 那支 migration 自己的 docstring 交代的做法。
除了編號與接點，內容沒有任何改變；仍然不動 schema、仍然只種那三個 slug。
`tests/test_guides_migration.py` 的三處引用一併更新。
