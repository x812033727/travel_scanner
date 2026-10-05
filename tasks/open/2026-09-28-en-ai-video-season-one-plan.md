---
id: 2026-09-28-en-ai-video-season-one-plan
title: English AI video season one plan: six videos aimed at one million views
status: open
priority: P1
area: docs
owner:
claimed_at:
created_at: 2026-09-28T02:13:08Z
completed_at:
branch: claude/ai-video-planning-l43qas
depends_on: []
scope:
  - docs/ai-video-en-season-01
---

# English AI video season one plan: six videos aimed at one million views

## Why

站主要幾支點閱率高的英文 AI 影片，目標單支破 100 萬觀看，並且和 Codex 已經做好的中文第一季（`docs/ai-video-season-01/`）比誰的點閱高。頻道現有的投影片產線只會做 zh-TW 旁白，也還沒有任何英文選題；企劃要以檔案落地，不能留在對話裡。

## Definition of done

- [x] `docs/ai-video-en-season-01/` 有 `README.md`（目標與數學、選題規律、六支總表、排程、製作路線、包裝規則、比賽規則、風險、下一步）、六份 `briefs/`、`packaging.csv`、`schedule.csv`、`scoreboard.csv`、`sources.json`。
- [x] 站主決定（2026-09-28）：英文旁白路線做下去；先做 1、4、3（`openai-agents-broke-in`、`always-on-agent-explained`、`gpt6-vs-opus55-worth-paying`）。
- [x] 站主決定（2026-09-28）：影片是繁體中文影片，英文用英文字幕與英文配音音軌；不另開英文頻道。
- [ ] 站主決定：頻道立場存進 `/admin/videos` 設定（存了 Jev 才會替影片挑大綱）。
- [x] 三支製作票已開並認領：`2026-09-28-en-video-01-openai-agents-broke`、`2026-09-28-en-video-04-always-on-agent`、`2026-09-28-en-video-03-gpt6-vs-opus55`。

## Steps

- [x] 讀 `youtube-video` skill、`docs/videos/*.md`、Codex 的四條影片分支，確認題目不重複。
- [x] 查 2026-09 的新聞鉤子與英文 AI 影片的對照點閱（`sources.json`）。
- [x] 寫企劃與六份簡報；每份有觀眾、能做的事、站主觀點（套用立場條號）、實算、兩個大綱、會過期的事實、素材、不做的事、包裝。
- [x] 站主回覆兩個決定（路線、順序）→ README 狀態行更新；頻道與立場仍待決定。

## How to verify

```bash
python3 -c "import json,csv;json.load(open('docs/ai-video-en-season-01/sources.json'));[list(csv.DictReader(open('docs/ai-video-en-season-01/'+f))) for f in ['packaging.csv','schedule.csv','scoreboard.csv']]"
npm run check:tasks
```

打開 `docs/ai-video-en-season-01/README.md`，六支的 slug 在 README 第 3 節、`schedule.csv`、`packaging.csv` 與 `briefs/` 檔名一致。

## Notes

- 2026-09-28（claude-fable-5-1）：企劃完成並推上分支 `claude/ai-video-planning-l43qas`。沒有開始撰稿，沒有上傳任何東西。
- Codex 的參賽作品在分支 `codex/ai-video-season-01`（中文旁白六集、Windows 合成聲線、每兩週一支，10/11 起）；另外 `codex/ai-general-videos`、`codex/ai-developer-videos`、`codex/ai-shorts-pilot` 是走產線的中文影片與 Shorts 工具。這份刻意不重複那些題目，只有「工作」一題同主題但角度不同。
- 產線寫死 zh-TW：`tools/video/core/schema.mjs` 的 `NARRATION_LOCALE`、lint 的字典規則、`apps/api/app/video_speech/checking.py` 的轉寫提示、`youtube.default_language`。多語言音軌（`docs/videos/DUBS.md`）畫面仍是中文，只當替代路線。
- 對照點閱都是搜尋索引的快照：ColdFusion「AI Fails at 96% of Jobs」約 90 萬、3Blue1Brown LLM 解說約 760 萬、MKBHD AI 影片約 920 萬。YouTube 影片頁對 fetcher 只回頁尾，openai.com 的兩頁回 403，撰稿當天要有人開官方頁。
- 沒有找到頻道現在的訂閱數或已上架影片數；README 第 1 節的曝光假設以新頻道為前提。
- 2026-09-28（claude-fable-5-1，第二輪）：站主決定做英文路線、先做 1、4、3。工具票的程式已在同一分支落地（`narration_locale`），三支的 brief、video.json、claims 與示範紀錄寫在 `docs/videos/<slug>/`。每支都經過兩輪獨立查核（第一輪各改 5、4、8 個事實：第 1 支把教育部那段歸給發現它的研究團隊、依研究者的重建改寫 Hugging Face 的細節、標題改成一次入侵加探查；第 4 支補上代理實際寫的第四列、把背景執行那句歸給 NVIDIA；第 3 支發現快取寫入不是加收而是取代輸入價，job 2 三個總額全改），第二輪各 2、0、0 個，不需第三輪；聽眾審稿各改十幾行口語。三支 lint 零錯誤，投影片渲染零版面問題（容器裡 Playwright 的 Chromium 版本不合，用既有的 1194 版接上）。旁白以後的階段需要站主的影片工具權杖，不在這個 session 做。
- 2026-10-04 board sweep (claude-opus-5-5-incomplete-tickets, approved by the owner): the claim by claude-fable-5-1 (since 2026-09-28T02:13:08Z) was stale and is released so it stops locking its scope. Landed: #968 #1019. Still open: Owner decision: save the channel stance in the /admin/videos settings so Jev picks outlines.
