---
id: 2026-09-28-en-ai-video-season-one-plan
title: English AI video season one plan: six videos aimed at one million views
status: in-progress
priority: P1
area: docs
owner: claude-fable-5-1
claimed_at: 2026-09-28T02:13:08Z
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
- [ ] 站主決定三件事：要不要做英文旁白路線（票 `2026-09-28-video-english-narration-locale`）、先做哪三支、英文頻道開不開與頻道立場存進設定。
- [ ] 決定之後，替選中的其餘影片各開一張製作票（第 1 支已開：`2026-09-28-en-video-01-openai-agents-broke`）。

## Steps

- [x] 讀 `youtube-video` skill、`docs/videos/*.md`、Codex 的四條影片分支，確認題目不重複。
- [x] 查 2026-09 的新聞鉤子與英文 AI 影片的對照點閱（`sources.json`）。
- [x] 寫企劃與六份簡報；每份有觀眾、能做的事、站主觀點（套用立場條號）、實算、兩個大綱、會過期的事實、素材、不做的事、包裝。
- [ ] 站主回覆三個決定 → 更新 README 的狀態行與排程。

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
