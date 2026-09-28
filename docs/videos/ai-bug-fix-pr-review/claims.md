# 可查核主張：AI 修補的三道 PR 審查關

查核日：2026-09-27。本片是自己寫的本地範例；沒有把它說成正式站事故或已合併的 PR。`demo/` 含可重現的起點、實際 patch、事後驗收及真實輸出重排畫面；完整比較紀錄另見相鄰影片的 `comparison.md`。

| ID | 影片主張 | 依據 | 場景 |
| --- | --- | --- | --- |
| c1 | 起始兩個測試通過，但 `100/3` 只分出 99 分；新驗收可以重現缺陷 | `../ai-coding-tools-same-task/demo/fare.mjs`、`fare.test.mjs`、`acceptance.test.mjs`；本機輸出 | opening、why-green、old-test-code、bug-example |
| c2 | Claude Code 本次實際修改 `fare.mjs` 與測試、自寫 9/9 通過；這是本地 patch，非正式 PR | `../ai-coding-tools-same-task/demo/claude.patch`、`comparison.md` 與本機 JSON | patch-source、not-real-pr |
| c3 | 題目契約為每人整數分、總和原值、差額最多一分、餘數先給前面的人；原有輸入規則要保留 | `../ai-coding-tools-same-task/demo/CHALLENGE.md`、`fare.mjs` | gate-one、contract、small-remainder、inputs、contract-case |
| c4 | Claude patch 用基本份額和餘數配給前面的人，原輸入檢查未刪，只改程式和測試 | `../ai-coding-tools-same-task/demo/claude.patch` | gate-two、diff-core、validation-stays、diff-check、test-assertions |
| c5 | 事後四類驗收在舊碼只過 1 類、Claude patch 4 類全過；性質測試覆蓋 0–500 分與 1–20 人 | `demo/acceptance.test.mjs`、`demo/claude.patch`、`demo/claude-acceptance.png`；截圖是實際輸出的終端重排，來源見 `demo/README.md` | gate-three、red-first、property、test-output、property-check、inputs-test |
| c6 | 需求、diff 與回歸證據應交給負責審查的人作判斷，是本片的編輯建議 | 編輯判斷；[GitHub PR review quickstart](https://docs.github.com/en/pull-requests/get-started/reviewing-pull-requests-quickstart) | three-gates、review-summary、review-record、limits |
| c7 | GitHub PR 審查可以對變更留言、要求修改或核准；本片未對真實 PR 操作 | [GitHub PR review quickstart](https://docs.github.com/en/pull-requests/get-started/reviewing-pull-requests-quickstart) | github、outro |

## 與企劃不同的地方

把開頭及縮圖示例改為「100 分 → 99 分」，與程式的整數分單位一致。

## 我懷疑但沒動的事

真實帳務流程會有額外的資料、交易與回滾風險；這份小型示範不能代表那些流程的審查已完成。

## 進度

133 句、28 場景已寫，`lint` 零錯誤零警告；第一輪獨立查核和新增場景補查已做，新截圖場景待覆核；實際旁白與成片未完成。

