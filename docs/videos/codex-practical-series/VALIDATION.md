# 教材與產品證據

檢查日期：2026-10-11（Asia/Taipei）。作者參考實作、獨立代理重做、真實 Codex 執行與站主學習驗收分開列出。

| 範圍 | 實際結果 | 證據 |
| --- | --- | --- |
| 全系列規格 | 18 課、36 份獨立 App／CLI brief | curriculum.json、lessons、episodes；course check |
| 作者來源測試 | 23／23 PASS，無 skip／TODO | materials/source；獨立來源測試 |
| 54 份教材快照 | 18 課 × start／reference／challenge，參考版皆通過；起始版刻意失敗依課目保留 | labs integration；各課 lesson.json |
| 最終課程整合與防覆寫 | 11／11 PASS | canonical-course-tests.log；evidence/validation.json |
| ZIP 重建 | 18 份 ZIP 兩次 SHA-256 完全一致 | build-07／build-08 manifest；evidence/packages.json |
| 網站資料與畫面 | 最新 reference 的 8 項實際 Edge 檢查通過 | advanced-browser-03/receipt.json |
| 第 01 課真實 CLI | 只讀 exec 完成；內部測試 2 PASS／1 FAIL；五份起始檔案未變 | lesson-01-cli-session.json、input-hashes、原始 session |
| 第 01／03／05 課獨立重做 | 01 保留預期失敗；03／05 主案例和挑戰修後通過；35 項網站檢查為 34 PASS／1 EXPECTED_FAILURE | independent-learner/REPLAY-REPORT.md、輸入／輸出／範圍收據 |
| 第 07／11／17 課獨立覆核 | 真 DOM 發現 markup 被解析；重構前後拒絕非法日期；換週與缺檔保留正確參數／失敗收據 | independent-final-check 外部紀錄 |
| 第 01 課 CLI 稿件 | 未撰稿者查核20項主張通過；唯一聽眾改詞有逐欄差異覆核 | ../codex-practical-01-cli/verify-1.md |
| ZIP直接跟做 | 實際解壓18包並執行54段獨立複製，1029檔路徑／hash相同；新版只改01外層說明，1030快照程式檔不變 | zip-root-followalong、material-guide-paths外部收據 |

原始輸出在 `C:/Users/x8120/mokaair-work/codex-practical-series/runs`。ZIP 與影片媒體不進 Git；索引與 hash 保存在本目錄 evidence。

第 06 課起始檢查可 exit 0，但有尚未寫的需求測試；新增有意義的案例後先紅再修。第 07 課 Node 測試全綠仍有畫面錯誤，必須實際輸入 markup 驗證。不能用「所有起始版都非零」代替這兩課的教學目的。

全 repository 的 docs-videos 檢查 219／219 通過。Windows 全 tools 檢查未完成：既有 ffmpeg 空畫格範圍失敗及 automation fixture 的 C: ESM 匯入／等待問題，已另開看板票，未修改其他人的 active scope。這次不宣稱全 tools 綠燈。

上述代理重做不是人類新手的學習效果證明。Codex App 原生操作素材、站主跟做、YouTube 上傳／公開，以及其餘影片的產品操作與成片仍另列在 [STATUS.md](STATUS.md)。
