---
id: 2026-09-14-guide-listing-curated-order
title: 文章列表不看精選與排序：/life 總覽篇排第 29、「精選攻略」列的是最後匯入的那批
status: done
priority: P2
area: api
owner: claude-fable-5-1
claimed_at: 2026-09-16T01:39:46Z
created_at: 2026-09-14T00:41:44Z
completed_at: 2026-09-16T06:08:27Z
branch: claude/travel-article-structure-search-sr9jiq
depends_on: []
scope:
  - apps/api/app/guides/service.py
  - apps/api/app/guides/router.py
  - apps/api/tests/test_guides.py
  - apps/web/lib/guides.server.ts
  - apps/web/lib/guides.server.test.ts
  - apps/web/app/[locale]/life/page.tsx
  - apps/web/app/[locale]/life/page.test.tsx
  - apps/web/app/[locale]/guides/page.tsx
  - apps/web/app/[locale]/guides/page.test.tsx
  - apps/web/app/[locale]/guides/[kind]/page.tsx
  - apps/web/app/[locale]/guides/[kind]/page.test.tsx
  - docs/travel-guides.md
  - apps/api/app/guides/schemas.py
  - apps/web/lib/guides.ts
---

# 文章列表不看精選與排序：/life 總覽篇排第 29、「精選攻略」列的是最後匯入的那批

## Why

公開文章列表 `GET /api/v1/guides`（`apps/api/app/guides/service.py:174` 的 `public_list`）只照
`published_at desc, slug` 排（`:215`），分頁 cursor 也只編這兩個值（`:156`、`:161`）。
每篇文章都有 `featured` 與 `display_order` 兩個欄位（`models.py:69-70`，內容包 `content_pack.py:67-68`），
但在公開端都沒有作用：
- `featured` 雖然有回傳，`apps/web` 只在型別檢查裡碰到它（`lib/guides.ts:242`），沒有任何畫面或排序用到。
- `display_order` 連回傳都沒有（`schemas.py:463` 的 `PublicSummary`）。

後台清單反而照 `featured desc, display_order, updated_at desc, slug` 排（`admin_service.py:962`），
所以編輯在後台看到的順序跟讀者看到的不一樣。

`guides-import` 在同一次執行裡照 slug 字母序逐篇發布。同一批的 `published_at` 前後只差兩秒左右，
列表於是變成「最後匯入的那批排最前面，批內是字母倒序」。2026-09-14 正式站的實際狀況：

- **`/zh-TW/life`**：40 篇生活分享在 2026-09-14T00:24:08–10 之間發布。其他文章都會連回的總覽篇
  `ai-tools-2026-overview` 排第 29，落在第二頁（每頁 24 篇）。它設了 `featured: true`、`display_order: 10`，
  `docs/life-ai-series-brief.md:63` 規定「總覽篇 10，其他 100」。第一頁第一篇是 `what-is-a-large-language-model`。
- **`/zh-TW/guides` 的「精選攻略」區塊**：它取 howto 的前 6 篇（`app/[locale]/guides/page.tsx:16,50`），
  實際列出的就是 2026-09-13T14:44 最後匯入的第四批（括號是 `display_order`）：
  `okinawa-4-day-itinerary`（430）、`new-chitose-airport-to-sapporo`（420）、`nagoya-3-day-itinerary`（440）、
  `korea-olive-young-tax-refund-shopping`（560，**根本沒標精選**）、`korea-ktx-srt-ticket-guide`（530）、
  `korea-esim-sim-wifi`（550）。照 `featured`／`display_order` 排應該是 `narita-haneda-to-tokyo`（10）、
  `tokyo-transit-passes`（20）、`tokyo-5-day-itinerary`（30）、`kansai-airport-to-osaka-kyoto`（40）、
  `osaka-kyoto-nara-4-day-itinerary`（50）、`incheon-airport-to-seoul`（60）。
  `docs/travel-guides.md:369` 對這個 hub 的描述也是「latest intel, featured guides」。
- **之後會更糟**：下一批生活分享（批次 03）發布後，這 40 篇整批往後推，總覽篇離第一頁更遠。

## Definition of done

- [x] `/zh-TW/life` 第一頁第一篇是總覽篇 `ai-tools-2026-overview`。其餘照 `display_order`；同值時新發布的在前，
      再同值照 slug。
- [x] `/zh-TW/guides` 的「精選攻略」與 `/{locale}/guides/howto` 列表照同一套規則：精選在前、`display_order` 小的在前。
- [x] 「最新情報」與 `/{locale}/guides/intel` 仍照發布時間排，因為情報有時效，新的在前才對。
      文章頁底部的延伸閱讀（`components/guides/article-page.tsx:128,151,154`）也不變。
- [x] 新排序跨頁不重複、不漏篇，包括大量並列的情況（40 篇同 `display_order`、兩秒內發布）。
- [x] 照發布時間排的列表，cursor 跟現在逐字相同，已經發出去的「看更多」連結照常能用。
- [x] 換成新排序的列表收到舊格式或模式不符的 `?cursor=` 時，不能回一頁 200 的「尚無內容」。
      今天 `fetchJson` 遇到 422 會回 null，頁面就顯示空的。導回不帶 cursor 的第一頁即可。
- [x] `docs/travel-guides.md` 寫明各列表的排序規則，以及 `featured`／`display_order` 在前台的作用。

## Steps

- [x] API：`GET /guides`（`router.py:43`）加 `sort=latest|curated`，預設 `latest`，行為不變。
      `curated` 的排序鍵是 `featured desc, display_order asc, published_at desc, slug asc`，cursor 帶上這四個值與排序模式。
      模式不符的 cursor 回既有的 `guide_cursor_invalid`（422）。
- [x] `tests/test_guides.py` 補四件事：
  - `curated` 的順序。
  - 跨頁不重複不漏篇：仿 `test_the_listing_pages_without_repeating_or_dropping_an_article`，再加同 `display_order` 同時發布的並列。
  - 模式不符的 cursor 會被拒。
  - `latest` 的 cursor 跟改動前一樣。
- [x] web：`GuideFilters` 加 `sort`，由 `query()`（`lib/guides.server.ts:57`）帶出去。三個地方改用 `curated`：
      `/life`（`life/page.tsx:19`）、hub 的 howto 區塊（`guides/page.tsx:16`）、`[kind]` 為 howto 時（`guides/[kind]/page.tsx:28`）。
- [x] web：換排序的列表如果讀取失敗、網址又帶 cursor，就導回第一頁，並補測試。
- [x] 更新 `docs/travel-guides.md`。

## How to verify

```bash
cd apps/api && uv run ruff check . && uv run mypy app && uv run pytest tests/test_guides.py -q
cd apps/web && npx vitest run lib/guides.server.test.ts "app/[locale]/life/page.test.tsx" "app/[locale]/guides/page.test.tsx" "app/[locale]/guides/[kind]/page.test.tsx"
npm run lint:web && npm run typecheck:web && npm run check:tasks
```

部署後不用重新匯入文章，排序只讀現有欄位。`/api/v1/guides` 對外不開放（nginx 回 Next 的 404），
從外面驗要走 BFF 的 `/api/travel/guides`：

```bash
curl -s 'https://mokaair.com/api/travel/guides?locale=zh-TW&kind=life&limit=1&sort=curated'    # 第一篇是 ai-tools-2026-overview
curl -s https://mokaair.com/zh-TW/guides | grep -o 'href="/zh-TW/guides/howto/[a-z0-9-]*"' | head -1   # narita-haneda-to-tokyo
curl -s https://mokaair.com/zh-TW/guides | grep -o 'href="/zh-TW/guides/intel/[a-z0-9-]*"' | head -1   # 與改動前相同：thailand-entry-2026-tdac
```

## Notes

- 2026-09-14 部署 #467、發布生活分享前 40 篇時發現，站主同意開票。
- **旅遊文章的 `featured` 幾乎全開**：howto 59 篇有 45 篇、intel 11 篇有 8 篇是 `true`，所以旅遊這邊實際決定順序的是
  `display_order`。內容包的 `display_order` 是逐批往後編的：第一批東京、關西、首爾從 10 起跳，第四批是 420–600，
  照它排就是核心攻略在前。站主如果想讓新的批次在前，改內容包的數字再跑 `guides-import` 即可
  （`content_pack.py:158-159` 會把它判成 taxonomy update），不用改程式。
- 生活分享只有總覽篇是 `featured: true`，其他 39 篇都是 `display_order: 100`，所以同值時照發布時間，同批再照 slug。
- 不採用：讓 `guides-import` 照 `display_order` 倒序發布，讓 `published_at` 剛好排出想要的順序。
  對已上線的文章沒用，因為重跑是 `unchanged`，而 `published_at` 記的是第一次發布
  （`test_published_at_records_the_first_publication_not_the_latest`）。之後任何一篇單獨發布也會打亂順序。
- 不採用：前台把精選文章另外抓出來疊在第一頁最上面。API 沒有 `featured` 篩選，而且同一篇會在後面的頁面再出現一次。
- sitemap 走另一個端點（`/guides/sitemap`），不受影響。

- 2026-09-16 落地（claude-fable-5-1，同分支 `claude/travel-article-structure-search-sr9jiq`）：
  API `GET /guides?sort=latest|curated`（`ListSort`），curated 的 cursor 是 `["curated", featured, display_order, published_at, slug]`，
  latest 的 cursor 逐字不變；跨模式的 cursor 回 422 `guide_cursor_invalid`。SQLite 下 `featured.is_(True)`／`.desc()` 與 Postgres 一致。
  web `GuideFilters.sort`（不設就不送）；`/life`、hub「精選攻略」、`/guides/howto` 用 curated；`/guides/intel` 與 hub「最新情報」不變。
  帶 `?cursor=` 而 API 拒絕（`available:false`）時 `redirect()` 回不帶 cursor 的列表（保留 `?topic=`）。
  測試：順序、同秒同 display_order 分頁不重不漏、跨模式 cursor、latest cursor 形狀；web 三頁與 loader。`docs/travel-guides.md` 有「sort」段。
