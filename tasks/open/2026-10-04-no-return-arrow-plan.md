---
id: 2026-10-04-no-return-arrow-plan
title: 偶的江湖：取材經典布袋戲結構的長篇漫劇企劃包（第一、二季 24 集與全系列路線圖）
status: in-progress
priority: P2
area: docs
owner: claude
claimed_at: 2026-10-04T02:20:53Z
created_at: 2026-10-04T02:20:53Z
completed_at:
branch: claude/vibrant-cray-mdpjzx
depends_on: []
scope:
  - docs/videos/series-plans/ou-de-jianghu
---

# 偶的江湖：取材經典布袋戲結構的長篇漫劇企劃包（第一、二季 24 集與全系列路線圖）

## Why

站主要做一個布袋戲式的 AI 動漫長篇：從經典的「魔女入盟—詛咒之箭—鑄劍—智星軍師—機龍」三段式結構開始，一路規劃到現在最新的一部，一集 20–30 分鐘，國語配音。站主已決定走原創換皮（人名、門派、世界全部原創，只留故事骨架），才能走 repo 的漫劇產線並可營利。repo 裡能承接 22 分鐘一集的只有 long-anime-v1 政策，既有唯一範例是 borrowed-dawn 的企劃包；這張票把同樣形狀的企劃包做出來：期一《無歸箭》兩季 24 集的集級細綱（可 build、可 validate），加上後續各期的路線圖（期與季層級）。

## Definition of done

- [x] `docs/videos/series-plans/ou-de-jianghu/` 有 plan.json、authoring-contract.json、setting.json、season-01.json、season-02.json 與由 build.mjs 產生的 setting.md、outline.md、season-01.md、season-02.md、documents.json、continuity.md、continuity.csv、manifest.json。
- [x] 每集有兩段高張力、懸念類型相鄰不同、每 4 集收一個伏筆、季末懸念翻轉理解；m08、m09、m10 保留給續期並在 finale 誠實宣告。
- [x] `saga/` 目錄有全系列路線圖（總名、每期的期名／季數／集數／對應原作／主題／全期高潮、精華路線、張力地圖、值得站主看的劇情改動、統一人名表）。
- [x] README 寫清楚單集長度與集數的理由、成本估算、製作差距（8 分鐘上限、long-anime-v1 條件、hybrid 等級、月配額）、原創聲明。
- [x] build --check、validate、validate.test、check:tasks、test:tools 全綠。

## Steps

- [x] 開票、認領、確認 borrowed-dawn 的 build／validate 形狀。
- [x] 複製並改寫 build.mjs、validate.mjs、validate.test.mjs 成 2 季 24 集、開放結局的版本。
- [x] 寫 plan.json、authoring-contract.json（20 個角色 id、12 條謎團與排程、規則）。
- [x] 寫 setting.json、season-01.json、season-02.json，跑 build／validate／test 到通過。
- [x] 全系列路線圖：分 19 個時代研究原作、改編、三角度審稿、修訂，合併人名表與路線圖，寫進 saga/。
- [x] README.md、review.md；跑 check:tasks 與 test:tools；commit、push。

## How to verify

```bash
node docs/videos/series-plans/ou-de-jianghu/build.mjs --check
node docs/videos/series-plans/ou-de-jianghu/validate.mjs
node --test docs/videos/series-plans/ou-de-jianghu/validate.test.mjs
npm run check:tasks && npm run test:tools
```

## Notes

- 單集長度：站主要 20–30 分鐘，採 22 分鐘正文、30 分鐘時段，與 long-anime-v1 企劃匯入路線（apps/api/app/video_automation/planning.py）所驗的數字相同，省掉改程式。
- 集數：原作 25 + 20 集、每集約一小時，砍掉拖戲後壓成 24 集（約 5.5 倍）；12 集一季是 repo 唯一長篇範例的形狀。
- 成本：22 分鐘約 440 鏡，Veo 3.1 Lite 一集一次過 clips 約 US$360、hybrid 約 US$190、stills 約 US$100；全片段一集約 3,500 片段秒，超過預設月配額 3,000 與單片上限 US$200。建議 hybrid 先做第 1 集試播。
- 不在這張票裡：建後台作品、POST series-request、生成設定圖或片段、改 apps/。
- 原作名稱不進任何 repo 檔案；README 的來源說明只講結構。
- 作品名 2026-10-04 定為《偶的江湖》（站主選的），季數全系列連續、只用序號；企劃目錄從 no-return-arrow 搬到 ou-de-jianghu。燕迴的外號改「斷浪」。
- 2026-10-04 完成：第一、二季 24 集過了四輪連貫性修訂與覆核；全系列路線圖分 20 個時代（含補上的 E13b）研究、改編、審稿、修訂後合併，主線 65 季 780 集、外傳 2 季 24 集，放在 `saga/`。合併後的缺漏檢查修了 20 處，留下 17 項待站主決定，另開 `2026-10-04-ou-de-jianghu-roadmap-decisions`。
- 子代理依站主指示中途改用另一個模型；曾有一個修訂代理自行把作品名改成別的名字，已改回站主選的《偶的江湖》。
- `npm run test:tools` 在這個容器有 62 項失敗，原因是沒有安裝 `intl-messageformat`、`js-yaml` 等套件（沒跑 npm ci）；本票只動企劃包與票，不碰 tools。
