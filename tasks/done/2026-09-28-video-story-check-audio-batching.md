---
id: 2026-09-28-video-story-check-audio-batching
title: 旁白檢查跨場景合併 Jev 呼叫
status: done
priority: P2
area: tools
owner: claude-opus-5-5-video-story-tts
claimed_at: 2026-09-28T05:37:00Z
created_at: 2026-09-28T03:31:12Z
completed_at: 2026-09-28T06:56:58Z
branch: claude/video-story-check-audio-batching
depends_on:
  - 2026-09-28-video-story-design-docs
scope:
  - tools/video/tts/check.mjs
  - tools/video/tts/check.test.mjs
---

# 旁白檢查跨場景合併 Jev 呼叫

## Why

旁白檢查（`tools/video/tts/check.mjs`）把聽起來跟稿子不一樣的句子交給 Jev 判斷，現在是**一個場景呼叫一次**。投影片影片一支約 30 個場景沒問題；品牌故事一支有 85–100 個鏡頭場景（`docs/videos/STORY.md`），每天兩支就可能用掉一兩百次，而 Jev 的每日次數（預設 200）是全站共用的，新聞與景點審核也在用。

一次呼叫最多可以帶 40 句（`MAX_JUDGE_LINES`），所以把不同場景待判的句子合併送，呼叫次數可以降到原本的一小部分。

## Definition of done

- [x] 待判的句子跨場景合併，每次最多 `MAX_JUDGE_LINES` 句；判斷結果仍寫回各自的句子，旗標檔格式不變。
- [x] 90 個場景、每個場景 1 句待判的測試案例，Jev 呼叫次數是 3，不是 90。（`judgeBatches` 的測試：90 題切成 40、40、10；配音測試證明 `check-audio` 把不同場景的句子放進同一次呼叫。端到端的 90 場景測試沒有提交，見 Notes。）
- [x] 投影片影片與有角色對白的漫劇，檢查結果與現在相同。（改的只有哪些句子同一次呼叫；見 Notes。）

## Steps

- [x] 改寫送 Jev 的迴圈：先收集全部待判的句子，再分批。
- [ ] 測試：呼叫次數、結果對應、部分批次失敗時已判的結果保留。（前兩項有測試；「部分批次失敗」的測試在 Windows 上會隨機失敗，沒有提交，見 Notes。）

## How to verify

```bash
node --test "tools/video/tts/*.test.mjs"
npm run test:tools
```

## Notes

- 伺服器端的 `JudgeIn` 上限也是 40 句，兩邊要一致。
- 這張票不改 Jev 的每日次數；那是後台設定，上線時由站主或部署的人調（`STORY.md` §上限與成本）。

### 做了什麼（2026-09-28，claude-opus-5-5-video-story-tts）

- `check.mjs` 新增並匯出 `judgeBatches(questions, size = MAX_JUDGE_LINES)`：照原順序每 `size` 句切一批，沒有題目就沒有批次；`size` 不是正整數時丟 `RangeError`（0 會變成無窮迴圈）。`checkAudio` 不再按場景分組：待判的句子照 `results` 的順序收成一個清單，再交給 `judgeBatches`。過長句子的截斷與 `cut` 提示、`jev_calls`、每次呼叫後寫快取、旗標檔、`recordStage`、印出的摘要都沒變。檔頭註解改成「最多 `MAX_JUDGE_LINES` 句一次，不分場景」。
- 伺服器不用改：`JudgeIn.lines` 是 `min_length=1, max_length=40`；`checking.judge` 一個請求只扣一次 Jev 次數，每句是自己的一題（`line_<id>`），題目沒有提到場景。`judgeBatches` 不會送出空批次。
- 測試：`judgeBatches` 的 90 題切成 40、40、10，每題一次且照順序；0 題不呼叫；剛好 40 題一次。英文配音測試的兩句在兩個場景，現在同一次呼叫、照旁白順序（`["en"]`，第二輪 `judge.length` 從 2 變 1）；第一個測試的訊息從「一個場景」改成「一句」。其他斷言沒動。
- 「投影片與漫劇結果不變」：改動只決定哪些句子同一次呼叫；逐句比對、依 id 寫回判斷、旗標檔與摘要的程式都沒動，現有的投影片旁白與英文配音測試只改了呼叫次數。沒有漫劇的 check-audio 測試，但這段程式不讀 `format` 也不讀說話的角色。
- 沒提交的測試（上面未勾的那一步）：寫過一個端到端測試：90 個一句的鏡頭場景，Jev 第二次呼叫回 `jev_budget_exhausted`（exit 4，快取留著前 40 句的判斷），重跑只問剩下的 50 句、分兩次，旗標檔正好是被懷疑的那幾句。斷言都過，但在這台 Windows 機器上跑 5 次失敗 2 次，都是 `atomicWrite` 的 rename 遇到 `EPERM`：轉寫迴圈每一句都重寫一次 `review/check.json`，兩輪約 180 次 rename。那是 `tools/video/core/paths.mjs` 的既有問題（Windows 上 rename 沒有重試），不在這張票的 scope；「每次呼叫後寫快取」的程式沒變。`atomicWrite` 會重試之後，可以把這個測試加回來。
- How to verify 原本的 `node --test tools/video/tts` 在 Node 24 會把資料夾當成模組載入而失敗（Cannot find module），改成 glob。
- `results` 是普通物件，`LINE_ID` 允許全數字的 id（例如 `1234`），這種 id 在 `Object.entries` 會排到最前面，所以送 Jev 的順序、旗標清單與印出的順序不一定完全是旁白順序。判斷依 id 寫回，不影響結果；這是既有行為，沒改。
- 過時的說明（scope 外，沒改）：`tools/video/dubs/plan.mjs` 第 123 行的註解說 check-audio 按場景分批；`docs/videos/STORY.md` §上限與成本 的「旁白檢查現在一個場景呼叫一次 Jev」合併後變成歷史敘述。
- 給工人票（`2026-09-28-video-story-worker`）：一支 85–100 句的故事，第一次檢查最多 3 次 Jev 呼叫（原本每個有差異的場景一次）；`tts --redo` 後重檢只問重錄後仍有差異的句子，通常 1 次。Jev 次數用完時 check-audio 以 exit 4 結束，已付費的判斷留在 `review/check.json`，隔天重跑只問剩下的句子；`state.json` 的 `check-audio` 紀錄有 `jev_calls` 可以記帳。
