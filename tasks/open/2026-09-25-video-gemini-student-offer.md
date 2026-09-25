---
id: 2026-09-25-video-gemini-student-offer
title: 影片：Google AI 學生方案免費一年，台灣大學生怎麼領，加上 Gemini Notebook 讀書流程
status: in-progress
priority: P2
area: docs
owner: claude-opus-5-5
claimed_at: 2026-09-25T01:24:24Z
created_at: 2026-09-25T01:23:07Z
completed_at:
branch: claude/video-batch-2
depends_on: []
scope:
  - docs/videos/gemini-student-offer
---

# 影片：Google AI 學生方案免費一年，台灣大學生怎麼領，加上 Gemini Notebook 讀書流程

## Why

熱門話題研究第二名：在 Google 搜尋趨勢的台灣資料裡，「gemini 學生 方案」上升 190%，兌換期限是 2026-12-31。站主 2026-09-25 選了大綱 A（四道關卡）。企劃書在 `docs/videos/gemini-student-offer/brief.md`，來源文章 `ai-news-gemini-student-offer-20260820`。

## Definition of done

- [ ] `docs/videos/gemini-student-offer/` 有 `brief.md`、`video.json`、`claims.md`、`verify-1.md`（必要時 `verify-2.md`），`lint` 零錯誤。
- [ ] 旁白通過 `check-audio`，站主核准旁白、看完成片（`approvals.json` 三筆，雜湊與成品一致）。
- [ ] 站主在 Studio 上傳成私人，影片 ID 寫回 `video.json`。

## Steps

- [x] 企劃代理寫 brief，站主選大綱（2026-09-25，選項 A）。
- [ ] 撰稿（sonnet）→ 查核（opus，換人）→ 聽眾優先審稿。新詞列在 `lexicon-additions.json`，由協調者併進共用字典。
- [ ] tts → check-audio → 核准旁白 → render → assemble → CC → package。
- [ ] 台灣學生的資格，官方沒有一句話寫明「台灣可以」。片中只講官方寫了什麼、沒寫什麼，不承諾一定領得到。

## How to verify

```bash
node tools/video/cli.mjs lint --slug gemini-student-offer
node tools/video/cli.mjs status --slug gemini-student-offer
```

## Notes

- 2026-09-25 claude-opus-5-5 認領；分支 `claude/video-batch-2`，疊在試作片分支 `claude/video-pilot-audio` 上（要用它的 `docs/videos/lexicon.json`）。
