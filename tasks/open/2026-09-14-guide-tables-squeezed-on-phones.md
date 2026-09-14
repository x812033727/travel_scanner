---
id: 2026-09-14-guide-tables-squeezed-on-phones
title: 文章表格在手機上把每一欄擠到兩三個字寬
status: open
priority: P2
area: web
owner:
claimed_at:
created_at: 2026-09-14T00:49:21Z
completed_at:
branch:
depends_on: []
scope:
  - apps/web/components/content-blocks.tsx
  - apps/web/components/content-blocks.test.tsx
---

# 文章表格在手機上把每一欄擠到兩三個字寬

## Why

情報攻略與生活分享的 `table` 區塊在 375 px 寬的手機上幾乎沒法讀。`components/content-blocks.tsx`
把表格包在 `overflow-x-auto` 裡，但 `<table>` 本身是 `w-full`，瀏覽器會把每一欄硬塞進螢幕寬度，
外層那個捲動框永遠用不到；文章外層又有 `[overflow-wrap:anywhere]`，於是數字與單位從中間斷開
（「3,000 韓/元」），短欄位的表頭一個字一行（「休/館/日」）。

2026-09-14 在內建瀏覽器的 mobile 預設（375×812）量到的：五欄表格每欄只剩 44 到 58 px，
單一列高 281 到 329 px（`nami-island-petite-france-day-trip`、`himeji-castle-day-trip`、
`thailand-esim-sim-wifi` 摺成四欄以前）；四欄的 `hakone-day-trip-free-pass` 也有 161 px 高的列。
目前 repo 裡還有 39 張五欄以上的表格（`bangkok-airport-to-city`、`incheon-airport-to-seoul`、
`japan-ic-card-suica-icoca-guide`、`ai-model-tiers-explained` 六欄等），第五批只在內容端把四篇摺成四欄，
沒有動渲染器。

## Definition of done

- [ ] 375 px 寬時，表格每一欄至少能放大約五個中文字，數字與單位不會在中間斷行；放不下的表格在自己的框裡
      左右捲動，整頁仍然不會橫向捲動。
- [ ] 桌面版（`max-w-3xl` 欄寬）的表格長相不變。
- [ ] 同一個渲染器服務的其他頁面（法律頁若共用）沒有被改壞。

## Steps

- [ ] 依欄數給表格最小寬度（例如每欄 7 到 8rem，與 100% 取大者），讓 `overflow-x-auto` 真的能捲動。
- [ ] 表頭與表格儲存格不要繼承 `[overflow-wrap:anywhere]`（改回 normal），長網址另外處理。
- [ ] 在 `content-blocks.test.tsx` 補一條：多欄表格有最小寬度、外框仍是 `overflow-x-auto`。

## How to verify

內建瀏覽器切 mobile 預設，開 `/zh-TW/guides/howto/bangkok-airport-to-city` 與
`/zh-TW/life/ai-model-tiers-explained`，在頁面執行
`[...document.querySelectorAll('article th')].map(th => th.getBoundingClientRect().width)`：每欄不低於約 80 px，
`document.documentElement.scrollWidth === innerWidth`，表格可以在框內左右滑。

## Notes

- 本機不必起 Postgres：第五批用過的 mock API 讀 `apps/api/app/guides/content` 當已發布文章，見
  `tasks/done/2026-09-13-launch-articles-batch-5-twenty-more.md` 的 Notes。
- 用 headless Edge `--window-size=390,…` 截手機寬度會多出捲軸寬，看起來像整頁溢出；以內建瀏覽器的
  mobile 預設量 `innerWidth` 為準。
