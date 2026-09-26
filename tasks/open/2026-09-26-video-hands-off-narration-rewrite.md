---
id: 2026-09-26-video-hands-off-narration-rewrite
title: 影片交給 AI 決定：改寫重錄後仍被聽錯的旁白句子
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-09-26T16:18:46Z
completed_at:
branch:
depends_on:
  - 2026-09-26-video-hands-off-worker
scope:
  - tools/video/automation
---

# 影片交給 AI 決定：改寫重錄後仍被聽錯的旁白句子

## Why

2026-09-26 第二批的旁白，最後是靠人工改措辭才收斂：「和」改成「跟」、句尾的「答」改成「回答」、「旗艦」改成「旗艦模型」。這一步可以交給模型做，旁白關卡就不必再等站主（`docs/videos/HANDS-OFF.md` §旁白）。

## Definition of done

- [ ] 重錄到上限之後仍被標記的句子，連同 Gemini 聽到的內容，交給聽眾審稿模型，只改這幾句的措辭。
- [ ] lint 比對改寫前後：數字、拉丁字詞與專有名詞不能變，變了就退回這次改寫。
- [ ] 改完用 `tts --redo` 重錄這幾句，再檢查一次，最多兩輪；還是不過才送審，等站主。
- [ ] 改了哪些句子、改成什麼，記在 `auto.json` 的 notes，也記在審核頁的清單。

## Steps

- [ ] 改寫的提示詞（放在 skill 的 prompts 裡）。
- [ ] 流程與輪數上限。
- [ ] 前後比對的 lint。

## How to verify

```bash
npm run test:tools
```

## Notes

- TTS 的快取是按每一句的文字加聲音算的，所以只會重錄改過的句子。
