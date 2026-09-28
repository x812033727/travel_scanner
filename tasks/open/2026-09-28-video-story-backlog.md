---
id: 2026-09-28-video-story-backlog
title: 100 個品牌故事的完整企劃清單
status: in-progress
priority: P1
area: docs
owner: claude-fable-5-1-video-story
claimed_at: 2026-09-28T03:37:23Z
created_at: 2026-09-28T03:31:10Z
completed_at:
branch: claude/video-story-backlog
depends_on:
  - 2026-09-28-video-story-design-docs
scope:
  - docs/videos/story-plans/brand-stories-100
  - tools/video/story-plans
---

# 100 個品牌故事的完整企劃清單

## Why

主機要每天從一份清單依序做兩支品牌故事（設計在 `docs/videos/STORY.md`）。清單要先有：100 個故事，每個都要有夠寫 12–15 分鐘的材料、查得到出處的核心說法、抓得到的來源網址，才不會讓工人開工之後才發現題目站不住腳。

站主 2026-09-28 核准了 100 個暫定題目與 50 天排程（日常用品與隱形標準 40、日韓台旅途品牌 40、科技與軟體 20），另有約 35 個備選。題目都避開參考頻道「黑猫研究院」做過的主題。這張票把每個題目寫成完整企劃，格式就是伺服器匯入時要的集數列（`STORY.md` §企劃清單與集數列）。

## Definition of done

- [ ] `docs/videos/story-plans/brand-stories-100/stories.json` 有 100 筆，分類是 40／40／20，`number` 1–100 不重複且等於排程順序，`slug` 不重複且符合影片代號規則（小寫、數字、連字號，最多 60 字元）。
- [ ] 每一筆都有 `question`、六段 `chapters`、`takeaway`、`must_verify`、至少 3 個 https 的 `sources`、`names`、`image_notes`、`publish`。
- [ ] 每一筆的核心說法（標題裡的那句話）至少有一個官方頁面或兩個獨立的可靠來源支持；不成立的題目已經換成備選，換掉的理由記在 `README.md`。
- [ ] `tools/video/story-plans/validate.mjs` 檢查以上規則與排程（50 天、每天 12:00 與 20:00 各一支），在 `npm run test:tools` 裡跑。
- [ ] `README.md` 說明清單怎麼讀、怎麼改、怎麼匯入，並附 50 天排程表與備選清單。

## Steps

- [ ] 定 `stories.json` 的形狀與 `tools/video/story-plans/validate.mjs`，先用 2 筆試作題目（A01 輪子行李箱、B18 迴轉壽司）寫完整。
- [ ] 分批研究與撰寫：每批約 10 個題目，一個代理寫、另一個代理查核核心說法與來源能否抓取。
- [ ] 查核沒過的題目從備選遞補，重排 `number` 與 `publish`。
- [ ] 寫 `README.md` 與排程表。
- [ ] `npm run test:tools`、`npm run check:tasks`。

## How to verify

```bash
node tools/video/story-plans/validate.mjs
npm run test:tools
```

預期：驗證腳本印出 100 筆、分類 40／40／20、50 天排程完整、0 個問題。

## Notes

- 研究代理抓網頁時，User-Agent 不可帶個人 email；用 `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)`，每個網域間隔至少 1 秒。
- 不讀參考頻道的逐字稿，也不抄它的標題與縮圖；只學題材類型。
- 會碰到版權角色的四個題目（東京迪士尼、日本環球影城、吉卜力、Hello Kitty）`image_notes` 要寫明只畫場景與人群，排在最後兩週。
- 空難、抗爭、官司的題目（黑盒子、GPS、成田機場、三養）`sensitivity` 是 `care`。
