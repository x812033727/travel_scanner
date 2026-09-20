---
id: 2026-09-20-travel-food-subtopics-seed
title: 旅遊主題第二層：美食底下的料理與咖啡店子主題（0082 種子、ingest 詞彙、測試、文件）
status: in-progress
priority: P1
area: api
owner: claude-fable-5-1
claimed_at: 2026-09-20T04:39:36Z
created_at: 2026-09-20T04:39:04Z
completed_at:
branch: claude/travel-food-subtopics-seed
depends_on: []
scope:
  - apps/api/app/guides/taxonomy.py
  - apps/api/app/guides/pack_ingest.py
  - apps/api/migrations/versions/0082_travel_food_subtopics.py
  - apps/api/tests/test_guides_migration.py
  - apps/api/tests/test_guides.py
  - apps/api/tests/test_guides_pack_ingest.py
  - apps/api/tests/test_guides_retopic.py
  - docs/travel-guides.md
  - docs/article-architecture.md
---

# 旅遊主題第二層：美食底下的料理與咖啡店子主題（0082 種子、ingest 詞彙、測試、文件）

## Why

站主要的韓國美食特輯是「一道料理、一個城市寫一篇」（「豬肉湯飯｜釜山美食特輯」「豬肉湯飯｜首爾美食特輯」），而且要能依料理分類瀏覽。攻略的分類只有 kind／目的地／主題三軸，目的地這一軸沒辦法把同一道料理跨城市收在一起；旅遊主題又刻意維持單層。兩層主題的機制（`parent_id`、分類 hub 頁、子主題 chips、延伸閱讀的「同子主題」層）在生活分享早就上線，API 與前端都是通用的，缺的只有旅遊這邊的種子：內容包只能用 `app/guides/taxonomy.py` 裡有的主題，`pack_ingest` 與正式站的 `_resolve_topics` 都會擋 `topic_unknown`。

站主 2026-09-20 決定：每道料理一個分類頁，掛在旅遊主題 `food` 底下，外加 `cafe`（咖啡店）；第一批 22 篇用到 15 個子主題。

## Definition of done

- [x] `0082_travel_food_subtopics` 種下 15 個 `section = 'travel'`、父主題為 `food` 的子主題與 zh-TW hub 導言；重跑不寫入、不覆蓋後台改過的名稱與導言；downgrade 只刪自己的列與指向它們的文章連結，`food` 本身進出都不變。
- [x] `taxonomy.TRAVEL_SEED_SUBTOPICS`／`TRAVEL_TOPIC_DESCRIPTIONS` 與 migration 逐項相同（測試鎖住）。
- [x] `pack_ingest._known_topics` 對 `howto`／`intel` 接受旅遊子主題，生活分享不接受。
- [x] 只掛料理子主題的文章仍會出現在 `?topic=food` 與美食 hub 的篇數裡；生活分享文章掛料理主題回 `422 guide_topic_section_mismatch`。
- [x] 與料理目錄同 slug 的子主題，`ko`／`zh-TW` 標籤等於該料理的名稱（測試鎖住；現在是 `kr-naengmyeon`、`kr-samgyetang`、`kr-tteokbokki`、`kr-bibimbap`，料理種子那張票再加五個）。
- [x] `docs/travel-guides.md`、`docs/article-architecture.md` 改寫「旅遊主題單層」的說法，並說明特輯只掛子主題的理由。

## Steps

- [x] 常數、`_known_topics`、migration。
- [x] 測試：migration 與常數一致、display_order 自成一段、0072→…→0080→0082 來回、`food` 被刪時落在頂層、互斥（含 discovery `LABELS` 與保留字）、行為測試、`pack_ingest`、`retopic`。
- [x] 五語系標籤逐語查核（對韓國觀光公社各語系站的實際用語）。
- [x] 文件。
- [ ] 合併前再查一次 migration 編號（見 How to verify）。
- [ ] 上線前在主機唯讀確認 `guide_topics` 沒有同名 slug。

## How to verify

```bash
cd apps/api
uv run ruff check . && uv run mypy app
uv run pytest -q tests/test_schema.py tests/test_guides_migration.py tests/test_guides.py \
  tests/test_guides_pack_ingest.py tests/test_guides_retopic.py tests/test_guides_content_pack.py \
  tests/test_guides_links.py tests/test_guides_search.py tests/test_migration_sql_dialect.py \
  tests/test_migration_dead_branches.py
```

合併前（另一個分支先佔了 0082 就改成下一號、重接 `down_revision`，測試檔只要改 `TRAVEL_SUBTOPIC_MIGRATIONS` 一個常數）：

```bash
git fetch origin main
git ls-tree --name-only origin/main apps/api/migrations/versions/ | sort | tail -3
gh pr list --state open --json number,headRefName,files \
  --jq '.[] | select([.files[].path] | any(startswith("apps/api/migrations/versions/"))) | "\(.number) \(.headRefName)"'
```

上線前在主機（唯讀）：

```sql
SELECT slug, section, source FROM guide_topics
WHERE slug IN ('cafe','kr-dwaeji-gukbap','kr-naengmyeon','kr-samgyetang','kr-beef-bone-soup',
  'kr-dak-hanmari','kr-kalguksu','kr-jokbal','kr-tteokbokki','kr-heukdwaeji','kr-gogi-guksu',
  'kr-jjim-galbi','kr-makchang','kr-ganjang-gejang','kr-bibimbap');
```

應該回 0 列；種子會跳過已存在的 slug，後台若有人手建了別的 section 的 `cafe`，內容包匯入會失敗。

## Notes

- **認領用了 `--force`。** scope 與四張 `review` 的票重疊：`2026-09-12-attribute-affiliate-clicks-to-the-guide`（握整個 `apps/api/migrations/versions`）、`2026-09-17-commons-non-ascii-filename-ingest`（`pack_ingest.py` 與它的測試）、`2026-09-12-api-windows-agents-md`（`test_guides.py`）、`2026-09-13-adsense-ads-txt-drift`（`docs/travel-guides.md`）。四張的程式碼都已經在 main（`d1117886` #565、`f521b902` #561、`14ce467d` #563），分支 `claude/travel-scanner-pr-552-rpq36m` 已不存在，票停在 review 是在等各自最後一項人工驗收。`claim` 的重疊檢查不看認領是否過期，所以只能 `--force`；那四張票本身沒動。
- **特輯只掛子主題、不同時掛 `food`。** 文章麵包屑取文章依 display_order 的第一個主題（`apps/web/components/guides/article-page.tsx` 的 `state.topics[0]`），`food` 是 110、子主題從 1000 起，同時掛就只會顯示「攻略 › 美食 › 標題」。本機實測（mock API＋next dev）：只掛 `kr-dwaeji-gukbap` 顯示「旅遊情報與攻略 › 旅遊攻略 › 美食 › 豬肉湯飯 › 標題」，兩種都不會出現文末的合作方案面板（`apps/web/lib/guide-affiliate.ts` 裡 `food` 與子主題都不對應任何模組）。生活分享有 856 篇同時掛父子主題，它們的麵包屑其實也只顯示父層——那是另一件事，沒有在這裡動。
- **slug 慣例**：子主題照料理種子的拼法（`kr-` 加羅馬拼音、詞間連字號），種子料理與它的 hub 同 slug。正式站有 15 道韓國料理是後台建立的、slug 沒有前綴（`dakhanmari`、`kalguksu`、`jokbal`、`ganjang-gejang`、`seolleongtang`…），它們的 hub 仍照慣例拼（`kr-dak-hanmari`），兩邊不同 slug。`kr-beef-bone-soup` 是雪濃湯與牛骨湯同一篇特輯共用的 hub，永遠不會是料理 slug；釜山小麥冷麵（`kr-milmyeon`）歸在 `kr-naengmyeon`，一個 hub 裡有首爾與釜山。
- **標籤**是對韓國觀光公社各語系站的實際用語逐一查過的：日文是テジクッパ不是デジクッパ、簡中用刀切面與猪蹄。`cafe` 的 zh-TW 用站主自己說的「咖啡店」（官方繁中站偏好「咖啡廳」，兩者在台灣都自然）。`kr-kalguksu` 的 zh-TW 是「刀切麵」：正式站資料庫那道料理現在叫「刀削手擀麵」（官方繁中站 0 筆），站主決定在後台改名，列在料理種子那張票的後台待辦。
- hub 沒有篇數門檻，只有一篇文章的料理 hub 也會被索引；沒有文章的子主題對讀者完全隱形（沒有 chip、`noindex`、不進 sitemap）。
- 後台清單的主題篩選是精確比對 slug：用 `food` 篩看不到只掛子主題的特輯，要用料理子主題篩。
