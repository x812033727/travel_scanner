---
id: 2026-10-25-fixprompts-look-blocked-sheet-prompt
title: 退件的設定圖沒有重畫：fixPrompts 後 look 階段的種子已用完就直接 blocked；沒有人形的角色要能在設定集給 sheet_prompt
status: review
priority: P2
area: tools
owner: claude-fable-vigilant-golick
claimed_at: 2026-10-25T16:00:12Z
created_at: 2026-10-25T15:55:44Z
completed_at:
branch: claude/vigilant-golick-332ac3
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

- [x] 設定圖審核被退件後，`fixPrompts("look")` 改完提示詞，`look` 階段會為被退的角色**重畫**（清掉該角色的 candidates 或改用新的 seed 區段），送出新的審核；只有重畫後仍沒有候選可送才 blocked。
- [x] 沒被退的角色不重畫、不重送（或重送時帶原本的 `suggested`／站主的選擇，不讓已核准的設定圖被換掉）。
- [x] 作品設定集的 cast 可以給 `sheet_prompt`（選填），`series.py` 驗證、寫手把它帶進每集 video.json 的 characters；`SERIES.md` 寫明用途（面板、系統、沒有人形的角色）。
- [x] 測試：退件 → 重畫 → 新審核；`sheet_prompt` 從設定集一路到 manifest 的 prompt。

## Steps

- [x] `flow.mjs lookGate`／`fixPrompts`：對 `targets` 裡的角色，在 manifest 刪掉 candidates（保留別的角色），或把 `prompt_fixes.look` 當 seed 區段的位移（seed = fixes*1000 + round*100 + index）。
- [x] `look.mjs`：重畫時 `entry.prompt` 用新的 `sheetPrompt`；manifest 的 `look_hash` 不變就不重畫其他角色。
- [x] `series.py`／`schemas.py`：cast 的 `sheet_prompt: str | None`（≤ 600 字）；寫手 prompt（`automation/prompts.mjs` 或 story 的 cast 投影）把它放進 characters。
- [x] 跑 `npm run test:tools`、api 的 ruff／mypy／pytest；收據：`flow.mjs`、`look.mjs` 在 `REVIEW_FILES`，要做 DURATION_ONLY 增量（獨立審查代理）。

## How to verify

e002-redo1 起「系統」的設定圖審核送上來的是空白光板；若站主退件一張設定圖，下一輪工人送上新的六張。

## Notes

- 看法在 `host_redo_status.js`（scratchpad）：`docker exec -i travel_scanner-video-worker-1 node -` 讀 `/var/lib/mokaair/video-work/<slug>/auto.json`（`blocked`、`prompt_fixes`、`notes`）、`characters/manifest.json`、`state.json`。
- 相關：票 `2026-10-25-judge-7-judge`（judge 沒推薦時的備援選法，#1850 已部署）只處理「沒推薦」，不處理「退件後沒重畫」。

## 做了什麼（2026-10-25，PR https://github.com/x812033727/travel_scanner/pull/1855）

- 真正的根因多一層：作品集的每集 `settle()` 會把寫手改過的角色換回設定集的 cast（逐字），所以 look 的提示詞修正根本動不了 `lookHash`，manifest 留著、seed 用完就什麼都不畫。
- `look.mjs`：新 `resetSheets(manifest, targets, { picks, now })`：被退（或 judge 兩輪都沒及格）的角色 candidates 清空、`redraws` 加一、退件備註／judge 修法記在 `sent_back`；其他角色不動，站主同一輪選過的（`picks`）寫成 `owner_pick` 與 `suggested`。seed 改為 `redraws × 1000 + (round−1) × 100 + index`（`sheetSeed`），每張重畫的提示詞都附 `sent_back` 的修法當 `Corrections`。
- `flow.mjs`：`lookGate` 退件分支從同輪已核准的審核收集站主的選擇（`choice` → options index，沒選就 `suggested`）傳給 `fixPrompts(..., { picks })`；`fixPrompts` 寫手改完後 `redrawSheets` 呼叫 `resetSheets` 改 manifest（judge 失敗那條路也會清，所以第一次 look 失敗後也是在新 seed 重畫）。沒改 `sync.mjs`：`lookSubmissions` 本來就讀 `entry.suggested`，站主選過的那張會當建議送上去，免關卡作品送達就核准。
- `series.py`：`_sheet_prompt_problem`（`SHEET_PROMPT_CHARS = 600`；`null` 等於沒給），設定集與故事聖經的 cast 都查。`schemas.py` 沒有 cast 模型（設定集是 body_json），不用改；`castFrom`（`series.mjs`）本來就會把 `character.sheet_prompt` 帶進 `series.json`／`video.json`，沒改。
- 沒做：企劃模型的設定集提示詞（`prompts.mjs planner:setting`）沒教它在角色層寫 `sheet_prompt`，站主在後台改設定集就能給；品牌故事（`story.mjs fixStoryPrompts`）那條 look 退件路沒改。要驗：部署後退件一張設定圖，看下一輪送上來的是 seed 1001–1003 的新圖、沒被退的角色建議欄是站主選過的那張。

## 補修（2026-10-26）

- #1855 部署後第一次實戰（e002-redo1）：退件 → `resetSheets` 清空 xitong 的 candidates → 工人**沒重畫就 `review-push`**（作品集 cast 逐字來自設定集，`lookHash` 不變，`pipelineStatus` 只看 hash 就把「look generated」當做完）→ 送出 `options: []` 的審核 → 站主核准沒 choice → `blocked: … waiting for xitong`。
- 補修 PR https://github.com/x812033727/travel_scanner/pull/1869：`state.mjs undrawnCharacters`（空 candidates ＝ look 未完成、下一步回 look）、`flow.mjs lookGate` 開頭守門、`sync.mjs lookSubmissions` 拒送、`admin_service.decision_problem` 拒絕核准沒 options 的 look 審核。測試：state／sync 各一、流程測試改成站主退件不改外觀（hash 不變）仍回 look、api 一個。
- 觀察：設定集改版不會回填已寫好劇本的集（e002-redo1 的 video.json 23:56 寫好，早於設定集第 6 版 00:23 加 `sheet_prompt`），已寫進 SERIES.md。
