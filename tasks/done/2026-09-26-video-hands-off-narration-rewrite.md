---
id: 2026-09-26-video-hands-off-narration-rewrite
title: 影片交給 AI 決定：改寫重錄後仍被聽錯的旁白句子
status: done
priority: P2
area: tools
owner: claude-fable-5-1-video-narration
claimed_at: 2026-09-27T00:10:36Z
created_at: 2026-09-26T16:18:46Z
completed_at: 2026-09-27T00:23:02Z
branch: claude/video-hands-off-narration-rewrite
depends_on:
  - 2026-09-26-video-hands-off-worker
scope:
  - tools/video/automation
  - tools/video/review/sync.mjs
  - tools/video/review/sync.test.mjs
  - .agents/skills/youtube-video
  - .claude/skills/youtube-video
---

# 影片交給 AI 決定：改寫重錄後仍被聽錯的旁白句子

## Why

2026-09-26 第二批的旁白，最後是靠人工改措辭才收斂：「和」改成「跟」、句尾的「答」改成「回答」、「旗艦」改成「旗艦模型」。這一步可以交給模型做，旁白關卡就不必再等站主（`docs/videos/HANDS-OFF.md` §旁白）。

## Definition of done

- [x] 重錄到上限之後仍被標記的句子，連同 Gemini 聽到的內容，交給聽眾審稿模型，只改這幾句的措辭。
- [x] lint 比對改寫前後：數字、拉丁字詞與專有名詞不能變，變了就退回這次改寫。
- [x] 改完用 `tts --redo` 重錄這幾句，再檢查一次，最多兩輪；還是不過才送審，等站主。
- [x] 改了哪些句子、改成什麼，記在 `auto.json` 的 notes，也記在審核頁的清單。

## Steps

- [x] 改寫的提示詞（放在 skill 的 prompts 裡）。
- [x] 流程與輪數上限。
- [x] 前後比對的 lint。

## How to verify

```bash
node --test tools/video/automation/*.test.mjs tools/video/review/*.test.mjs
npm run test:tools
```

## Notes

- TTS 的快取是按每一句的文字加聲音算的，所以只會重錄改過的句子。
- 2026-09-27 claude-fable-5-1-video-narration 做完（分支 `claude/video-hands-off-narration-rewrite`，從 `origin/main` 併入 worker 票的分支 `origin/claude/video-hands-off-worker`；那張票的 PR #836 當時還沒合併，所以 claim 用了 `--force`）。併入時 `tools/video/automation/client.mjs` 有一個純文字衝突：main 已經有 #831 squash 進來的 `judgePolicy`，worker 分支在它後面加 `judgeOutline`，解法就是留下 `judgeOutline`。
- scope 加了 `tools/video/review/sync.mjs`：審核頁的清單要從送審 payload 來（`submission("audio")` 多讀一個 `review/rewrites.json`）；`tools/video/review/sync.test.mjs` 是它旁邊的測試。加了 `.agents/skills/youtube-video`、`.claude/skills/youtube-video`：提示詞放在 skill 的 prompts 裡（票的 Steps 要求）；`.claude` 那份只有 `SKILL.md` 的逐字複本，因為 `tools/skills.test.mjs` 只鏡像 `SKILL.md`。
- **流程**（`tools/video/automation/flow.mjs` 的 `narration()` → `rewriteNarration()`）：`check-audio` 結束碼 1 而且 `state.retakes >= max_retake_rounds` 之後才進改寫迴圈；`MAX_REWRITE_ROUNDS = 2`，輪數記在 `state.rewrites`（整支影片累計，和 `retakes` 一樣，站主退回旁白後重新合成也不歸零）。每輪：從 `review/check-flags.json` 的 `flags` 和 `review/check.json` 的 `heard`、`noul` 組出被標的句子，呼叫 `stage("listener", slug, payload, 16000, format, "rewrite")`（提示詞是 `prompts.mjs` 的 `LISTENER_REWRITE`，投影片與漫劇同一份，站主給 listener 的常設指示照舊接在後面）。payload：`{ lines: [{ id, text, heard, jev }], lexicon: [字典的詞], round, previous_problems? }`，`text` 是 `spokenText(line)`（有 `say` 就是 `say`）。答案 `{ lines: [{ id, text }] }`：不是被標的 id、空字串 → 退回；和原句相同 → 略過；`rewriteProblems(before, after, { lexicon })` 有問題 → 退回；其餘接受，改 `video.json` 那句的 `text`（同時拿掉 `say`、`say_for`），整份跑 lint，lint 有錯就還原、這輪全部退回。接受的 id 寫進 `review/rewrite-flags.json`（`{ slug, flags: [ids] }`）給 `tts --slug <slug> --redo <那個檔>`，再 `check-audio`；一句都沒接受就不重錄、不重檢，下一輪把退回原因放進 `previous_problems`。`tts` 失敗 → `block`；`check-audio` 結束碼 4 → `later`；答案沒有 `lines` 陣列 → `retryLater`（連續兩次卡住）。兩輪之後仍被標 → `review-push --gate audio`，站主決定。
- **記錄**：接受的改寫記 notes `narration rewritten: <id> 「before」 → 「after」`，退回的記 `narration rewrite dropped: <id>: <problem>`；`review/rewrites.json` = `[{ id, before, after, heard }]`，各輪累加；`submission("audio")` 附在 `payload.rewrites`（永遠是陣列，沒有檔案就是 `[]`），摘要多一段「；改寫 N 句」。旁白自動核准的規則沒動：重檢每句都過、而且 `auto_approve_audio` 開著，伺服器收到就核准。
- **比對**（`tools/video/automation/rewrite.mjs` 的 `rewriteProblems`，純函式）：數字含貨幣與百分號（`1.5`、`2026`、`10%`、`US$3`、`NT$1,200`；全形數字先轉半形）逐字比對多重集合；拉丁字詞 `[A-Za-z][A-Za-z0-9+.#-]*` 不分大小寫比對多重集合，句尾的 `.`、`-` 當標點；字典的詞按字典的拼法整詞比對（同 `tts/requests.mjs` `spokenParts` 的邊界），已經當成字詞回報過的不重複回報。回傳句子陣列，空陣列就是沒問題；沒改的句子一定是空陣列。
- 還沒做：審核頁顯示 `payload.rewrites` 的清單（web 那條線的票，這裡沒碰 `apps/`）；主機上還沒有影片走到這一步，第一支走過之後看 notes 決定要不要調 `MAX_REWRITE_ROUNDS` 或提示詞。
