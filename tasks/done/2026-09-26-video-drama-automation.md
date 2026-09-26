---
id: 2026-09-26-video-drama-automation
title: Video drama T8: the host automation runs the drama steps, gates and shot fixer
status: done
priority: P2
area: tools
owner: claude-fable-5-1-video-drama
claimed_at: 2026-09-26T07:02:34Z
created_at: 2026-09-26T01:53:42Z
completed_at: 2026-09-26T07:13:51Z
branch:
depends_on:
  - 2026-09-26-video-drama-clips-music
  - 2026-09-26-video-drama-assemble
  - 2026-09-26-video-drama-tts-voices
  - 2026-09-26-video-drama-settings-and-look-gates
scope:
  - tools/video/automation
  - docs/videos/AUTOMATION.md
---

# Video drama T8: the host automation runs the drama steps, gates and shot fixer

## Why

主機工人（`tools/video/automation/flow.mjs`）目前只認識投影片的步驟。漫劇多了 look／keyframes／clips／music 與兩個關卡，QC 沒過要讓模型修提示詞再跑，預算超過要卡住並在審核頁寫原因。企劃、撰稿、查核的提示詞也要有 drama 版（故事聖經、每鏡 ≤10 秒、一句一個說話者、英文提示詞、每鏡最多 3 個角色）。

## Definition of done

- [x] `advance()` 處理 look generated／look approved／keyframes drawn／storyboard approved／clips generated／music generated（`media()`、`lookGate()`、`storyboardGate()`）；結束碼 4 下一輪再試、結束碼 3（上限、設定、金鑰）→ block 並回報、QC 結束碼 1 → `fixPrompts()`（writer 帶 `fix` payload：kind／targets／problems／owner_note）每種最多 2 輪；站主退回 look／storyboard 也走 `fixPrompts`。
- [x] `settle()` 依 `state.format` 寫 `format: "drama"`、`look.preset`（設定的 `style_preset`）、`subtitles.burn_in`、關音樂就刪 `music`；`prompts.mjs` 的 `DRAMA_INSTRUCTIONS`（planner／writer（含 FIX）／verifier／listener）與 `instructionsFor(stage, format)`；`references()` 多 `drama`、`drama_example`、`drama_brief`。站主的請求：`step()` 在排程草稿之前 `dramaNext()` → `draftDrama()`（企劃、`dramaStart`、送大綱），上架確認後 `dramaDone()`；回報帶 `format`。
- [x] 假站測試：站主請求 → 企劃 → 撰稿（drama 版）→ 查核 → 聽眾 → look 失敗一次交 writer 修 → look 過 → look 關卡（每角色一張，站主選）→ tts → 旁白關卡 → keyframes → storyboard（伺服器自動核准）→ render → clips 超單支上限 block 並帶原因；`settle`／`planProblem`／`instructionsFor` 的單元測試。媒體階段用 `ctx.runCommand` 假跑（各階段自己的測試在各自的檔案），`review-pull` 走真的。
- [x] `docs/videos/AUTOMATION.md` 補「漫劇」一節（`2026-09-25-video-auto-rollout-pair-the-worker` 目前沒人認領，只加一節不動其他）。

## Steps

- [x] flow.mjs 分支與 helper → prompts.mjs → 測試 → 文件。

## How to verify

```bash
node --test tools/video/automation/*.test.mjs
```

## Notes

設計全文在 `docs/videos/DRAMA.md`（跟 T1 一起合併）；供應商、價格、政策的研究依據也在那裡。

2026-09-26 做法（claude-fable-5-1-video-drama）：

- 站主的請求優先於排程草稿，但同樣受 `max_waiting_drafts` 限制（`room()`）；企劃兩次不成就以 `drama-<id 前 8 碼>` 開一支卡住的影片，站主在審核頁看得到原因（請求本身沒有失敗狀態）。排程草稿不做漫劇：漫劇只由站主發起。
- `fixPrompts()` 的來源：look 讀 `characters/manifest.json` 的 `needs_review` 角色（評語來自 `candidates[].judge.problems`），keyframes／clips 讀各自 manifest 的 `shots` 的 `needs_review`（`problems`，沒有就從 `takes[]` 收）；站主退回 look（各角色的 note）或 storyboard（payload 的 `needs_review` 鏡＋note）也走它。修完 `visual_hash`／`look_hash` 變了，只有改過的角色或鏡頭會重生（快取按請求鍵）。
- 階段成功會清掉 `prompt_fixes[kind]`，所以每一段各有兩輪，不是整支影片兩輪。
- 漫劇的 `narration()` 直接沿用（check-audio 逐句比對不看說話者）；`captions()` 也沿用（字幕文字含「【名字】」由 render 的字幕條處理，CC 不加前綴）。
- 測試把媒體階段換成 `ctx.runCommand`（寫出各階段的 manifest 讓 `pipelineStatus` 前進），`review-pull` 走真的，所以 look／storyboard 的讀回是真的程式碼在跑。
- 沒動 `tools/video/cli.mjs`；工人容器不用改（`auto` 指令同一支）。部署後要在後台開「AI 漫劇」，工人才會問請求。
