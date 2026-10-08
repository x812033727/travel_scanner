# 可查核主張：AI 修補的三道 PR 審查關

本輪查核日：2026-10-08。本片是本地分攤範例；沒有把它說成正式站事故或已合併的 PR。`demo/` 含可重現的起點、保留的 patch、事後驗收及輸出重排畫面。原始 Claude CLI 命令、結果 JSON 與退出紀錄未找到，本輪只驗證保留修補的行為，不宣稱已證實工具作者。歷史比較紀錄與 `verify-2-20261008.md` 保留原來的歸因及查核缺口。

| ID | 影片主張 | 依據 | 場景 |
| --- | --- | --- | --- |
| c1 | 起始兩個測試通過，但 `100/3` 只分出 99 分；新驗收可以重現缺陷 | `demo/fare.mjs`、`fare.test.mjs`、`acceptance.test.mjs`；本輪獨立重跑收據 | opening、why-green、old-test-code、bug-example |
| c2 | 保留的本地 patch 修改 `fare.mjs` 與測試；修補後原測試檔 9/9 通過，另加事後驗收共 13/13；非正式 PR | `demo/claude.patch`；`verify-2-20261008.md` 的實際重跑及完整 SHA256，檔名不作工具作者證據 | patch-source、not-real-pr |
| c3 | 題目契約為每人整數分、總和原值、差額最多一分、餘數先給前面的人；原有輸入規則要保留 | `../ai-coding-tools-same-task/demo/CHALLENGE.md`、`fare.mjs` | gate-one、contract、small-remainder、inputs、contract-case |
| c4 | 本地 patch 用基本份額和餘數配給前面的人，原輸入檢查未刪，只改程式和測試 | `demo/claude.patch`；本輪獨立重跑收據 | gate-two、diff-core、validation-stays、diff-check、test-assertions |
| c5 | 事後四類驗收在舊碼只過 1 類、本地 patch 4 類全過；性質測試覆蓋 0–500 分與 1–20 人 | `demo/acceptance.test.mjs`、`demo/claude.patch`、`demo/claude-acceptance.png`；圖片是保留輸出的重排，不是原始終端截圖；完整來源與本輪重跑見 `verify-2-20261008.md` | gate-three、red-first、property、test-output、property-check、inputs-test |
| c6 | 需求、diff 與回歸證據應交給負責審查的人作判斷，是本片的編輯建議 | 編輯判斷；[GitHub PR review quickstart](https://docs.github.com/en/pull-requests/get-started/reviewing-pull-requests-quickstart) | three-gates、review-summary、review-record、limits |
| c7 | GitHub PR 審查可以對變更留言、要求修改或核准；本片未對真實 PR 操作 | [GitHub PR review quickstart](https://docs.github.com/en/pull-requests/get-started/reviewing-pull-requests-quickstart) | github、outro |

## 與企劃不同的地方

把開頭及縮圖示例改為「100 分 → 99 分」，與程式的整數分單位一致。

## 我懷疑但沒動的事

真實帳務流程會有額外的資料、交易與回滾風險；這份小型示範不能代表那些流程的審查已完成。

## 進度

133 句、28 場景。2026-10-08 全稿第二輪查核覆蓋 261 項，實際本地重跑符合預期；七處歷史工具歸因缺證，另有一處「自寫」字卡含糊，八處均改為本地修補描述。「輸入驗證最容易被刪」缺乏相對頻率證據，已改為可能發生的審查風險。新版第三輪獨立覆核另存 `verify-3-20261008.md`，結論以該報告為準。舊成片曾在 9/28 留有完成筆記，本輪尚未找到檔案與原始媒體收據，不能視為從未合成，也不能據此宣告目前待上架包完成。

兩個官方 URL 已在本輪實際取得 HTTP 200，raw body、解析文字與完整 SHA256 均列於 `verify-2-20261008.md`。GitHub 文件支援留言、要求修改與核准；Claude CLI 文件不證實歷史執行。三關方法是本片的編輯建議。

