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
branch:
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

- [ ] 二十個內容包在 `apps/api/app/guides/content/`，zh-TW。slug、kind、destination、topics、
      display order、valid_until 與 `docs/travel-guides-batch-7/README.md` 的清單一致。
      每篇有 Commons hero、內文照片 1 到 2 張、自繪 SVG 圖解、表格、callout、summary 區塊、
      `related` 與 `aliases`、帶 `checked_on` 的 sources，以及規格指定的 offer。
- [ ] 每個數字撰稿當天在官方頁重新核對過；官方頁沒寫的一律「以官網為準」。每篇留 `notes.md`。
- [ ] 站內文章連結用 `article` inline（不是 `link` 區塊），城市頁與美食目錄用 `link` 區塊、
      網址用 `foods?destination_id=`。
- [ ] `test_guides_content_pack` 綠、`pack_cli lint --kind howto` 與 `--kind intel` 沒有新的 error。
      部署後 `guides-import --dry-run` 只有這二十篇是 create，再 `--publish`，然後
      `guides-links-rebuild` 與 `guides-links-check`。
- [ ] 上線 PR 把各規格「上線後與交叉檢查」裡有日期的事項開成票，並把既有文章的反向連結
      彙整成一張票。

## Steps

- [ ] 一篇一個撰稿代理，照規格與 `docs/travel-guides-batch-7/README.md` 寫；工作區在 repo 外。
      **一次不要超過 7 個代理**（20 個併發會撞到模型限額，第一次規劃就是這樣中斷的）。
- [ ] 收件：讀 `notes.md` 抽查數字、跑 `ingest --dry-run`、渲染圖解看過，再正式 ingest。
- [ ] 工具檢查不到、要人工看的：article inline 的 slug 與 kind、offer 位置與相鄰、
      表格欄數、summary 的數字是否逐字出現在正文、Commons 作者欄位。
- [ ] **兩篇共用同一組數字的地方要逐字對**：喀比兩篇與普吉跳島篇（皮皮門票、瑪雅灣封閉期、
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
