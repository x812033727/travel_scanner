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

133 句。原 28 場景全稿第二輪查核覆蓋 261 項，實際本地重跑符合預期；七處歷史工具歸因缺證，另有一處「自寫」字卡含糊，八處均改為本地修補描述。「輸入驗證最容易被刪」缺乏相對頻率證據，已改為可能發生的審查風險。第三輪報告另存 `verify-3-20261008.md`，原生入口 `verify-3.md` 是完整逐位元副本。舊成片曾在 9/28 留有完成筆記，本輪有限查找尚未找到檔案與原始媒體收據，不能視為從未合成。

站主在具體重做預檢後再次指示「繼續」，本輪已依該授權完成新版 133 句主旁白。一次已收到音檔的 journal 確認紀錄遇本機 EPERM；完整原 sent／confirmed temp／WAV 已備份及核驗後恢復，原生續跑重用該答案，沒有重送未知請求。原 28 靜態畫面在實測時間軸上有 27 張停留超過 15 秒，因此改為 47 場景／88 個真正展開與高亮狀態。所有 133 句文字、IDs、聲音與原 WAV 全雜湊保持，六章節名稱和身分不變；新增的時間只來自原生場景間隔。新視覺版完整 350 項內容已獨立查核，正式來源綁定與表格見 `verify-4.md`。

逐句音訊第一輪 133 句均已檢查，98 句逐字相符、18 句僅同音／語氣差異、4 句 Jev 判為可接受、13 句仍被標記。這不是最終音訊核准；後續以真正盲轉寫及原生更新的結果為準。成片與待上架包仍待正常品管，未上傳或發布。

兩個官方 URL 已在本輪實際取得 HTTP 200，raw body、解析文字與完整 SHA256 均列於 `verify-2-20261008.md`。GitHub 文件支援留言、要求修改與核准；Claude CLI 文件不證實歷史執行。三關方法是本片的編輯建議。

