---
id: 2026-10-25-fixprompts-look-blocked-sheet-prompt
title: 退件的設定圖沒有重畫：fixPrompts 後 look 階段的種子已用完就直接 blocked；沒有人形的角色要能在設定集給 sheet_prompt
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-25T15:55:44Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/automation/flow.mjs
  - tools/video/automation/automation.test.mjs
  - tools/video/media/look.mjs
  - tools/video/media/look-keyframes.test.mjs
  - apps/api/app/video_automation/series.py
  - apps/api/app/video_automation/schemas.py
  - apps/api/tests/test_video_story_series.py
  - docs/videos/SERIES.md
---

# 退件的設定圖沒有重畫；沒有人形的角色要能給 sheet_prompt

## Why

2026-10-25《系統說我是 BUG》第 1 集重做（`xitong-shuo-wo-shi-bug-e001-redo1`）：站主側把「系統」的設定圖審核退件（六張都畫了人，備註「只要一塊空白的淡藍光板」）。工人的 `lookGate` 看到 rejected 就走 `fixPrompts(state, "look")`，寫手改了提示詞、`prompt_fixes.look` 加到 2，然後 `look` 階段**什麼都沒重畫**：`characters/manifest.json` 裡那個角色已有 seed 1–3 與 101–103 共六張（`MAX_LOOK_ROUNDS = 2`、每輪 3 張），`look.mjs` 的迴圈對「已有候選且已評分」的 seed 直接 continue，manifest 的時間戳停在 08:34，之後就 `blocked: look still fails after 2 prompt fixes`。後台按重試只清 blocked 與 prompt_fixes，再跑一次還是同樣結果（15:14 第二次 blocked）。退件備註因此永遠到不了圖上。

第二層原因：設定圖的提示詞固定是 `DEFAULT_SHEET_PROMPT`（character design sheet：正面、四分之三、全身、站姿），角色外貌寫「no character picture… a blank pane of pale-blue light」也沒用，image-01 照樣畫一個人站在光板旁。`look.mjs sheetPrompt` 已支援 `character.sheet_prompt` 覆寫整句，但作品的設定集（`setting.json` 的 cast → `series.py` 驗證 → 每集 video.json 的 characters）沒有這個欄位，所以每一集的「系統」都會重畫成人；`series-store.mjs sheetKey` 又把 `sheet_prompt` 算進鍵，手改一集的 video.json 不會沿用到下一集。

當天的解法是手改主機：給 e001-redo1 的 video.json 加 `xitong.sheet_prompt`（只畫一塊空白光板、不畫人），刪掉 manifest 裡 xitong 那一筆，再按重試。

## Definition of done

- [ ] 設定圖審核被退件後，`fixPrompts("look")` 改完提示詞，`look` 階段會為被退的角色**重畫**（清掉該角色的 candidates 或改用新的 seed 區段），送出新的審核；只有重畫後仍沒有候選可送才 blocked。
- [ ] 沒被退的角色不重畫、不重送（或重送時帶原本的 `suggested`／站主的選擇，不讓已核准的設定圖被換掉）。
- [ ] 作品設定集的 cast 可以給 `sheet_prompt`（選填），`series.py` 驗證、寫手把它帶進每集 video.json 的 characters；`SERIES.md` 寫明用途（面板、系統、沒有人形的角色）。
- [ ] 測試：退件 → 重畫 → 新審核；`sheet_prompt` 從設定集一路到 manifest 的 prompt。

## Steps

- [ ] `flow.mjs lookGate`／`fixPrompts`：對 `targets` 裡的角色，在 manifest 刪掉 candidates（保留別的角色），或把 `prompt_fixes.look` 當 seed 區段的位移（seed = fixes*1000 + round*100 + index）。
- [ ] `look.mjs`：重畫時 `entry.prompt` 用新的 `sheetPrompt`；manifest 的 `look_hash` 不變就不重畫其他角色。
- [ ] `series.py`／`schemas.py`：cast 的 `sheet_prompt: str | None`（≤ 600 字）；寫手 prompt（`automation/prompts.mjs` 或 story 的 cast 投影）把它放進 characters。
- [ ] 跑 `npm run test:tools`、api 的 ruff／mypy／pytest；收據：`flow.mjs`、`look.mjs` 在 `REVIEW_FILES`，要做 DURATION_ONLY 增量（獨立審查代理）。

## How to verify

e002-redo1 起「系統」的設定圖審核送上來的是空白光板；若站主退件一張設定圖，下一輪工人送上新的六張。

## Notes

- 看法在 `host_redo_status.js`（scratchpad）：`docker exec -i travel_scanner-video-worker-1 node -` 讀 `/var/lib/mokaair/video-work/<slug>/auto.json`（`blocked`、`prompt_fixes`、`notes`）、`characters/manifest.json`、`state.json`。
- 相關：票 `2026-10-25-judge-7-judge`（judge 沒推薦時的備援選法，#1850 已部署）只處理「沒推薦」，不處理「退件後沒重畫」。
