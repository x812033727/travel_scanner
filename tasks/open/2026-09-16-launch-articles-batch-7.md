---
id: 2026-09-16-launch-articles-batch-7
title: 撰寫並上線第七批旅遊文章：二十篇 zh-TW 攻略與情報
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-09-16T23:06:26Z
completed_at:
branch: claude/new-travel-guide-k2q5h3
depends_on:
  - 2026-09-14-plan-articles-batch-7
scope:
  - apps/api/app/guides/content/lunar-new-year-2027-asia-travel.json
  - apps/api/app/guides/content/japan-golden-week-2027.json
  - apps/api/app/guides/content/krabi-airport-transport-where-to-stay.json
  - apps/api/app/guides/content/krabi-ao-nang-railay-4-islands.json
  - apps/api/app/guides/content/phuket-phi-phi-james-bond-island-hopping.json
  - apps/api/app/guides/content/chiang-rai-2-day-itinerary.json
  - apps/api/app/guides/content/bangkok-where-to-stay.json
  - apps/api/app/guides/content/southeast-asia-seasons-when-to-go.json
  - apps/api/app/guides/content/sendai-airport-access-loople-bus-guide.json
  - apps/api/app/guides/content/sendai-matsushima-2-day-itinerary.json
  - apps/api/app/guides/content/yamadera-day-trip-from-sendai.json
  - apps/api/app/guides/content/zao-fox-village-from-sendai.json
  - apps/api/app/guides/content/daegu-airport-ktx-subway-guide.json
  - apps/api/app/guides/content/daegu-2-day-itinerary.json
  - apps/api/app/guides/content/jeonju-hanok-village-day-trip-from-seoul.json
  - apps/api/app/guides/content/ha-long-bay-cruise-from-hanoi.json
  - apps/api/app/guides/content/hue-day-trip-from-da-nang.json
  - apps/api/app/guides/content/vietnam-domestic-flights-train-guide.json
  - apps/api/app/guides/content/macau-day-trip-from-hong-kong.json
  - apps/api/app/guides/content/sentosa-day-guide.json
  - apps/web/public/guides/lunar-new-year-2027-asia-travel
  - apps/web/public/guides/japan-golden-week-2027
  - apps/web/public/guides/krabi-airport-transport-where-to-stay
  - apps/web/public/guides/krabi-ao-nang-railay-4-islands
  - apps/web/public/guides/phuket-phi-phi-james-bond-island-hopping
  - apps/web/public/guides/chiang-rai-2-day-itinerary
  - apps/web/public/guides/bangkok-where-to-stay
  - apps/web/public/guides/southeast-asia-seasons-when-to-go
  - apps/web/public/guides/sendai-airport-access-loople-bus-guide
  - apps/web/public/guides/sendai-matsushima-2-day-itinerary
  - apps/web/public/guides/yamadera-day-trip-from-sendai
  - apps/web/public/guides/zao-fox-village-from-sendai
  - apps/web/public/guides/daegu-airport-ktx-subway-guide
  - apps/web/public/guides/daegu-2-day-itinerary
  - apps/web/public/guides/jeonju-hanok-village-day-trip-from-seoul
  - apps/web/public/guides/ha-long-bay-cruise-from-hanoi
  - apps/web/public/guides/hue-day-trip-from-da-nang
  - apps/web/public/guides/vietnam-domestic-flights-train-guide
  - apps/web/public/guides/macau-day-trip-from-hong-kong
  - apps/web/public/guides/sentosa-day-guide
---

# 撰寫並上線第七批旅遊文章：二十篇 zh-TW 攻略與情報

## Why

第七批的二十份規格 2026-09-16 定稿，在 [`docs/travel-guides-batch-7/`](../../docs/travel-guides-batch-7)，
規劃票是 `2026-09-14-plan-articles-batch-7`。規格已經過三輪一致性審查（連結與時效、區塊規則、
事實與口徑，共 38 條發現全部處理）。這張票是照規格把文章寫出來、查證、畫圖、上線。

這批補上目錄裡原本 0 篇的喀比（primary）、仙台、大邱、清萊；全州與順化以一日遊的形式進站。
做完之後目錄裡只剩大叻是 0 篇。

## Definition of done

- [x] 二十個內容包在 `apps/api/app/guides/content/`，zh-TW。slug、kind、destination、topics、
      display order、valid_until 與 `docs/travel-guides-batch-7/README.md` 的清單一致。
      每篇有 Commons hero、內文照片 1 到 2 張、自繪 SVG 圖解、表格、callout、summary 區塊、
      `related` 與 `aliases`、帶 `checked_on` 的 sources，以及規格指定的 offer。
- [x] 每個數字撰稿當天在官方頁重新核對過；官方頁沒寫的一律「以官網為準」。每篇留 `notes.md`。
- [x] 站內文章連結用 `article` inline（不是 `link` 區塊），城市頁與美食目錄用 `link` 區塊、
      網址用 `foods?destination_id=`。
- [ ] （部署後）`test_guides_content_pack` 綠、`pack_cli lint --kind howto` 與 `--kind intel` 沒有新的 error。
      部署後 `guides-import --dry-run` 只有這二十篇是 create，再 `--publish`，然後
      `guides-links-rebuild` 與 `guides-links-check`。
- [ ] 上線 PR 把各規格「上線後與交叉檢查」裡有日期的事項開成票，並把既有文章的反向連結
      彙整成一張票。

## Steps

- [x] 一篇一個撰稿代理，照規格與 `docs/travel-guides-batch-7/README.md` 寫；工作區在 repo 外。
      **一次不要超過 7 個代理**（20 個併發會撞到模型限額，第一次規劃就是這樣中斷的）。
- [x] 收件：讀 `notes.md` 抽查數字、跑 `ingest --dry-run`、渲染圖解看過，再正式 ingest。
- [x] 工具檢查不到、要人工看的：article inline 的 slug 與 kind、offer 位置與相鄰、
      表格欄數、summary 的數字是否逐字出現在正文、Commons 作者欄位。
- [x] **兩篇共用同一組數字的地方要逐字對**：喀比兩篇與普吉跳島篇（皮皮門票、瑪雅灣封閉期、
      渡輪班次）、仙台四篇（市內票券）、大邱兩篇、越南兩篇（SE 車次發車時刻）、
      農曆新年篇與黃金週篇。規劃時三輪審查抓到的錯，有一半以上就出在這裡。

## How to verify

```bash
cd apps/api && uv run pytest tests/test_guides_content_pack.py -q
uv run python -m app.guides.pack_cli lint --kind howto
uv run python -m app.guides.pack_cli lint --kind intel
```

正式站上每個 `/zh-TW/guides/<kind>/<slug>` 回 200、沒有 noindex，hero 與 diagram-1.svg 載得到。

## Notes

- 規格裡標「以官網為準」的地方是官方頁真的查不到，不要自己找第三方補數字。
- 這台機器讀不到的官方站列在 `docs/travel-guides-batch-7/README.md` 的「事實查核」一節。
- 撰稿代理呼叫 Commons 等外部站時，User-Agent 一律用 repo 工具的
  `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)`，不要放任何個人資料。

**Scope 與 claim（2026-09-16）**：scope 列的是這二十個內容包檔與圖檔目錄，不是整個內容目錄。
`2026-09-15-content-summary-howto-and-life`（claude-fable-5-1）持有 `apps/api/app/guides/content`
整個目錄，工具把底下任何路徑都當成重疊，所以這張票用 `--force` 認領；這二十個 slug 一個都不在那張票的
工作範圍裡（那張票是替既有文章補 summary 與 FAQ，本批的檔案還不存在）。第六批遇到同樣情形、同樣處理。

## 撰稿進度（2026-09-17）

**二十篇已經寫完、ingest 進 repo，PR #543 已開。** 還沒做的只有部署與正式站發布。

- `pack_cli ingest` 二十篇全部成功，`tests/test_guides_content_pack.py` 9 passed 5 skipped，
  `lint --kind howto` 與 `--kind intel` 對這二十篇**零 error 零 warning**（站上既有文章的舊 error 不在本批範圍）。
- 這個 commit 只新增檔案，沒有修改任何既有內容包。
- 收件檢查（`scratchpad/write7/intake_check.py`）跑工具檢查不到的部分：欄位值與清單一致、offer 數量與位置、
  表格欄數、summary 的數字逐字對正文、article inline 的 slug 與 kind、link 只有站內網址且不用 `?city=`、
  sources 都有 `checked_on`、字數。最後一輪 **20/20、零發現**。
- 共 285 筆查證來源。每篇的查證記錄留在撰稿工作區的 `notes.md`。

### 編輯規則的三處放寬（都記在 ERRATA.md）

README 沿用第六批的字數上限比站上實際出貨嚴。撰稿者用 `pack_ingest._body_length` 量過 main：
88 篇 zh-TW `howto` 中位數 3,183、最長 4,178；17 篇 `intel` 區間 1,574 到 2,174。
協調者把上限定在 howto 4,200、intel 2,200，並把七篇退回壓縮（最長的澳門篇 5,097 壓到 4,200）。
hero 壓不進 200 KB 時照第六批的做法在 ingest 之後補壓，腳本留在 `scratchpad/write7/shrink_heroes.py`。

### 撰稿階段抓到的事實問題

`ERRATA.md` 有 19 條。影響最大的兩條：

- **越南鐵路的票價表單**：規格說它「忽略出發站」，兩位撰稿者各自實測推翻——表單其實有吃出發站。
  真正的坑是查完一次之後站別會跳回端點，畫面上看不出算的是哪一段（實測顯示 728,000，重選才拿到 143,000，差五倍）。
  兩篇都改寫成真正的坑。
- **仙台機場的定額計程車**：規格寫的 5,000 日圓在官網 HTML 裡被註解掉、畫面上看不到，現行費率是 6,500。

### 還沒做的

- [ ] 部署，然後在正式站跑 `guides-import --dry-run`（確認只有這二十篇是 create）、`--publish`、
      `guides-links-rebuild`、`guides-links-check --locale zh-TW`。
- [ ] 把各規格「上線後與交叉檢查」的日期事項開成票（彙整在 `scratchpad/plan7/followups.md`）。
- [ ] 既有文章的反向連結（同一張票）。

## 釋出認領（由站主授權，2026-09-19）

claude-opus-5 應站主「整理目前所有工作狀態」處理，盤點見 `docs/work-status-2026-09-19.md`。

PR #543 於 2026-09-17 合併，二十篇都已上線：2026-09-19 查 `sitemaps/sitemap/travel-zh-TW.xml`，20／20 都在，網址形如 `/zh-TW/guides/howto/<slug>`。原持有者 claude-opus-5（2026-09-16 認領，review）。

剩下三件：部署後的 `test_guides_content_pack` 與 `pack_cli lint --kind howto`／`--kind intel`；把各規格「上線後與交叉檢查」的日期事項開成票（清單原本在某個 session 的 `scratchpad/plan7/followups.md`，可能已經不在，要從 `docs/travel-guides-batch-7/` 的規格重新整理）；既有文章的反向連結。
