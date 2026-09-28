---
id: 2026-09-28-video-story-design-docs
title: 品牌故事路線的設計文件與分票
status: done
priority: P1
area: docs
owner: claude-fable-5-1-video-story
claimed_at: 2026-09-28T03:35:12Z
created_at: 2026-09-28T03:31:10Z
completed_at: 2026-09-28T03:35:13Z
branch: claude/video-story-design-docs
depends_on: []
scope:
  - docs/videos/STORY.md
---

# 品牌故事路線的設計文件與分票

## Why

站主 2026-09-28 給了參考頻道「黑猫研究院」（YouTube `@qiqiqushi0`：品牌、日用品與隱形標準背後的商業故事，10–16 分鐘，卡通插畫約每 9 秒一張），要求規劃 100 個這樣的故事，並讓主機每天做出兩支，放在 Mokaair 現有頻道。

現有產線做不到：只有投影片教學與 AI 漫劇兩種格式，沒有題目佇列，漫劇與長篇作品的單集上限是 8 分鐘，一次模型呼叫也寫不完 13 分鐘的稿（轉送 295 秒、輸出上限 32,000）。

評估過兩種做法（新增第三種格式，或在漫劇底下加一種作品類型），採用後者：`format` 仍是 `drama`，作品的 `kind` 是 `story`。理由、合約與要改的地方都寫在 `docs/videos/STORY.md`，這張票交付那份文件與後面 11 張票。

## Definition of done

- [x] `docs/videos/STORY.md` 寫了站主的決定、為什麼是作品類型、一支影片的規格、企劃清單與集數列的合約、產線與關卡、伺服器改動、上限與成本、風險、分票。
- [x] 12 張 `2026-09-28-video-story-*` 票都在看板上，每張的 Why、完成條件、步驟、驗證都寫了。
- [x] `npm run check:tasks` 通過。

## Steps

- [x] 讀參考頻道的影片清單（311 支的標題、觀看數、片長）與一支影片的分鏡縮圖。
- [x] 讀現有的漫劇、長篇作品、免關卡設計與程式，列出擋住這件事的限制。
- [x] 跟站主確認題材、片長、頻道、自動化程度、圖片模型、吉祥物。
- [x] 寫 `docs/videos/STORY.md`。
- [x] 開 12 張票。

## How to verify

```bash
npm run check:tasks
npm run tasks -- list | grep video-story
```

預期：檢查通過；列出 12 張票（這張在合併前會搬到 done）。

## Notes

- 站主核准的計畫原稿在工作站的 `~/.claude/plans/https-www-youtube-com-qiqiqushi0-50-async-allen.md`，內含 100 個題目、50 天排程與備選清單；完整企劃由票 `2026-09-28-video-story-backlog` 寫進 repo。
- 圖片單價：repo 的 `apps/api/app/video_media/catalog.py` 把 Gemini 3.1 Flash Image 登記成 US$0.045，那是 0.5K 的價格；adapter（`providers/gemini_images.py`）只送 `aspectRatio`，實際輸出 1K，官方價目頁 2026-09-28 是 US$0.067。站主以更正後的數字確認用 Flash 1K。更正目錄在票 `2026-09-28-video-story-api-policy-languages`。
- PR #870（`claude/video-review-manga-workflow-fp1rpz`）加了作品的 `kind` 欄位並佔用遷移 0105–0108；伺服器、工人、後台三張票要等它合併。
- 平行的 Shorts 那條線（`docs/videos/SHORTS.md`）負責直式短片；故事的直式精華留到第二期交給那條線。
