---
id: 2026-09-28-video-story-backlog
title: 100 個品牌故事的完整企劃清單
status: done
priority: P1
area: docs
owner: claude-fable-5-1-video-story
claimed_at: 2026-09-28T03:37:23Z
created_at: 2026-09-28T03:31:10Z
completed_at: 2026-09-28T10:43:04Z
branch: claude/video-story-backlog
depends_on:
  - 2026-09-28-video-story-design-docs
scope:
  - docs/videos/story-plans/brand-stories-100
  - tools/video/story-plans
  - docs/videos/STORY.md
  - tasks/open/2026-09-28-video-story-worker.md
  - tasks/open/2026-09-28-video-story-admin.md
---

# 100 個品牌故事的完整企劃清單

## Why

主機要每天從一份清單依序做兩支品牌故事（設計在 `docs/videos/STORY.md`）。清單要先有：100 個故事，每個都要有夠寫 12–15 分鐘的材料、查得到出處的核心說法、抓得到的來源網址，才不會讓工人開工之後才發現題目站不住腳。

站主 2026-09-28 核准了 100 個暫定題目與 50 天排程（日常用品與隱形標準 40、日韓台旅途品牌 40、科技與軟體 20），另有約 35 個備選。題目都避開參考頻道「黑猫研究院」做過的主題。這張票把每個題目寫成完整企劃，格式就是伺服器匯入時要的集數列（`STORY.md` §企劃清單與集數列）。

## Definition of done

- [x] `docs/videos/story-plans/brand-stories-100/stories.json` 有 100 筆，分類是 40／40／20，`number` 1–100 不重複且等於排程順序，`slug` 不重複且符合影片代號規則（小寫、數字、連字號，最多 60 字元）。
- [x] 每一筆都有 `question`、六段 `chapters`、`takeaway`、`must_verify`、至少 3 個 https 的 `sources`、`names`、`image_notes`、`publish`。
- [x] 每一筆的核心說法（標題裡的那句話）至少有一個官方頁面或兩個獨立的可靠來源支持；不成立的題目已經換成備選，換掉的理由記在 `README.md`。（沒有題目被換掉。核心說法只有當事人自己的說法時標 `attributed`，標題也照這樣寫，例如 C01 的「負責人說拒絕過幾千萬歐元」。）
- [x] `tools/video/story-plans/validate.mjs` 檢查以上規則與排程（50 天、每天 12:00 與 20:00 各一支），在 `npm run test:tools` 裡跑。
- [x] `README.md` 說明清單怎麼讀、怎麼改、怎麼匯入，並附 50 天排程表與備選清單。

## Steps

- [x] 定 `stories.json` 的形狀與 `tools/video/story-plans/validate.mjs`，先用 2 筆試作題目（A01 輪子行李箱、B18 迴轉壽司）寫完整。
- [x] 分批研究與撰寫：每批約 10 個題目，一個代理寫、另一個代理查核核心說法與來源能否抓取。
- [x] 查核沒過的題目從備選遞補，重排 `number` 與 `publish`。（沒有題目需要遞補。）
- [x] 寫 `README.md` 與排程表。
- [x] `npm run test:tools`、`npm run check:tasks`。

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

### 做完之後記下來的事（2026-09-28）

- **沒有一個故事原封不動通過查核。** 100 個都由另一個代理在新的對話裡查過，全部改過，沒有換掉任何題目。流傳的商業故事常在年份、數字與「誰先做的」上出錯；標題跟核准時不一樣的列在產生的 `SCHEDULE.md`。寫的代理用較小的模型，查核用較大的模型，這個分工值得照做。
- **檢查用的是工人自己的讀取程式。** 一開始的 `--fetch` 只看回應是不是 200，會放過工人讀不到的來源。工人的 `pageReader` 不讀 PDF、不讀超過 3 MB 的頁面、一頁只留前 40,000 個字。現在的規則是每個必查事實至少有一頁工人讀得到；真的沒有時由查核的人列進查核紀錄的 `reviewer_only`，清單印在 `SCHEDULE.md`。
- **逾時不等於死連結。** 10 MB 的報告在讀取程式的時限內抓不完，但連結打得開。`--fetch` 對讀取程式放棄的頁面會再用成片品管的連結檢查（`tools/video/qa/links.mjs`）問一次：打得開就算「在、但讀不到」。有一輪補來源把這樣的報告當成死連結移除，後來放回去了。
- **對機器人回 403 的頁面**（`news.aa.com`、Gear Patrol、紐約時報等）改列網頁時光機的存檔。存檔算原發行者的頁面，跟原頁面算同一個來源。
- **查核紀錄的 `notes` 會跟著故事匯入**（`caveats`）。它寫的是給撰稿的指示：哪個軼事查不到出處不要講、哪個數字各來源說法不一。
- **在這台機器上 `npm run test:tools` 跑不完整**：這個 worktree 沒有 `npm ci`，缺 `pinyin-pro`、`jsdom` 與字型，tts、字型、登入那幾組會失敗，跟這張票無關。`node --test "tools/video/story-plans/*.test.mjs"` 全過；整套交給 CI。
- scope 多了 `docs/videos/STORY.md` 與兩張票的檔案：合約的欄位（`look`、`caveats`、`reviewer_only`、匯入指令的旗標）與「工人讀得到什麼」要寫在設計文件裡，工人票與後台票要知道這些。
