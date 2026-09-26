---
id: 2026-09-26-video-drama-automation
title: Video drama T8: the host automation runs the drama steps, gates and shot fixer
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-09-26T01:53:42Z
completed_at:
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

- [ ] `advance()` 處理 look generated／look approved／keyframes drawn／storyboard approved／clips generated／music generated；結束碼 4 下一輪再試、預算類結束碼 3 → block 並回報、QC 結束碼 1 → `shot_fixer`（用 writer 階段帶 fix payload）最多 2 輪。
- [ ] `settle()` 依設定的 `drama_enabled` 寫 `format`；`prompts.mjs` 依格式選 planner／writer／verifier 的 drama 變體。
- [ ] 假站測試：一支 drama 走完 look → gate → keyframes → clips；QC 失敗兩次後 block；預算耗盡 block 並帶原因。
- [ ] `docs/videos/AUTOMATION.md` 補 drama 流程一節（與 `2026-09-25-video-auto-rollout-pair-the-worker` 協調，避免同時改）。

## Steps

- [ ] flow.mjs 分支與 helper → prompts.mjs → 測試 → 文件。

## How to verify

```bash
node --test tools/video/automation/*.test.mjs
```

## Notes

設計全文在 `docs/videos/DRAMA.md`（跟 T1 一起合併）；供應商、價格、政策的研究依據也在那裡。
