---
id: 2026-09-13-adsense-auto-ads-overlay-setup
title: AdSense 後台開啟錨定／插頁／Multiplex，修正封鎖清單，兩週後比較收益
status: open
priority: P2
area: ops
owner:
claimed_at:
created_at: 2026-09-13T13:37:55Z
completed_at:
branch:
depends_on:
  - 2026-09-13-adsense-multi-slot-and-overlay-formats
scope:
  - docs/adsense-feasibility.md
---

# AdSense 後台開啟錨定／插頁／Multiplex，修正封鎖清單，兩週後比較收益

## Why

站主 2026-09-13 選了混合做法（`docs/adsense-feasibility.md` 的「D3 修訂」）：
- 文中廣告由程式放 1–3 個（`2026-09-13-adsense-multi-slot-and-overlay-formats`）。
- 錨定、插頁、Multiplex 用 AdSense 自動廣告開啟。

後兩者只能在 AdSense 後台設定，程式做不到。
**先部署程式再開錨定**：錨定廣告的 z-index 是最大值，沒有 `AnchorAdOffset` 讓位時會蓋住手機底部導覽列。

另外，同一天稍早在「封鎖控制項」加了 `.com.tw`、`.co.jp`、`.co.kr` 三筆。
Google 的說明（[封鎖廣告客戶網址](https://support.google.com/adsense/answer/164657)）要求輸入完整網域，
國碼網域要連同網域名稱一起寫（例如 `google.com.br`）。所以這三筆大概沒有作用：
既沒擋到競品的國碼網域（例如 `expedia.com.tw`），也不會擋掉所有台灣廣告主。要實際到後台確認。

## Definition of done

- [ ] mokaair.com 的自動廣告：錨定、插頁、Multiplex 開啟；橫幅、側邊欄、意圖導向格式、自動最佳化關閉。
- [ ] 封鎖清單裡沒有無效的國碼後綴項目，競品的國碼網域有逐一列出。
- [ ] 正式站手機實測：錨定廣告出現時，底部導覽列在它上面、沒有被蓋住。
- [ ] 開啟兩週後的分潤點擊、網頁 RPM 與 CLS 寫進 Notes 與評估文件。

## Steps

- [ ] 確認網站審核狀態。還在「審查中」時設定可以先存，但看不到任何廣告。
- [ ] 廣告 → mokaair.com「編輯」→ 疊加格式：
  - 錨定廣告開，進階設定選「僅底部」。程式也處理頂部，但底部不會跟頁首搶位置。
  - 插頁廣告開，「允許插頁廣告的額外觸發條件」維持關閉。
  - 側邊欄關。
- [ ] 頁內格式：橫幅廣告關，Multiplex 開。兩者是各自獨立的開關。
- [ ] 意圖導向格式關；自動最佳化維持關。
- [ ] 封鎖控制項 → 廣告客戶網址：看那三筆後綴實際存成什麼。
  - 無效就刪掉，改列競品實際在用的國碼網域（例如 `expedia.com.tw`、`expedia.co.jp`、`expedia.co.kr`）。
    每個網域先實際打開，確認存在、而且是那家公司的站。
  - 刪改前先跟站主確認。
- [ ] 記下開啟日期，兩週後比較：
  - `GET /admin/analytics/affiliates?range=` 的 guide placement 點擊，前後各兩週。
  - AdSense「報表」的網頁 RPM、各格式收益（依廣告格式分組）。
  - 文章頁 CLS，依 memory「cls-needs-a-top-level-page」的方式用 Playwright 量。

## How to verify

- 手機開一篇長文（例如 `https://mokaair.com/zh-TW/guides/howto/tokyo-where-to-stay`），錨定廣告出現後：
  - `getComputedStyle(document.documentElement).getPropertyValue("--ad-anchor-bottom")` 等於廣告高度。
  - 底部導覽列的 `getBoundingClientRect().bottom` 小於等於 `innerHeight - 廣告高度`。
- 文章 HTML 裡 slot 數字的出現次數等於版位數 × 2（HTML＋RSC）。

## Notes

- 插頁廣告的觸發條件（[說明](https://support.google.com/adsense/answer/16853623)）：
  - 切回分頁或視窗、點網址列（桌機）、在新分頁開同站頁面再切過去。
  - 讀者點分潤按鈕開新分頁去 Klook 再切回來，也算「切回分頁」，所以插頁可能出現在他回來的時候。
    點擊本身已經記到，但如果兩週後分潤點擊明顯下降，先關插頁。
  - 「額外觸發條件」包含上一頁按鈕與閒置 30 秒，對讀攻略的人干擾大，維持關閉。
- 錨定位置、側邊欄位置是 2026 新增的進階設定（[說明](https://support.google.com/adsense/answer/16242705)）。
- 2026-09-13 這個 session 的 Chrome 擴充功能一直連不上，所以這張票的後台操作沒有做。
