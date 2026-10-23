# C03 Moleskine｜2016 年底直營店數更正紀錄

日期：2026-10-22。本檔記錄作者對現行稿件的一處事實更正，**不是獨立來源查核或成片核准收據**。獨立覆核應另按下列新雜湊簽收。

## 版本與改動

| 項目 | 讀值 |
| --- | --- |
| 更正前畫面版 `video.json` SHA-256 | `5729039524FA9F0F915002C96D7CD6F8BAD8BA6C8C2C042EA5DE6DBB6B7FD792` |
| 更正後 `video.json` SHA-256 | `2DCFE691C05C5A041B16BCDBB77ACC8FDAE2955D0247CC41F951C5C9097F7833` |
| 更正後 `narration-draft.md` SHA-256 | `4C23F1DB6F45F9BD9220FCAB74257600F7CC17B8236AEF0B914CCFC9426E8314` |
| 唯一改動的口播 | `c03-p12-s02`／`c031202`：「七十八家」→「七十九家」；同一張 `stats` 卡改為 `79 家` 並換來源 |

2017 年[投資人簡報](https://dieterengroup.imgix.net/documents/presentations/moleskine_lorenzo_viglione.pdf)投影片 15 顯示 **78**，原稿與舊複核收據採了該數字。[D’Ieteren 2016 Activity Report](https://dieterengroup.imgix.net/annual-reports/rapport_en.pdf)印刷頁 35 明說直接營運門市，頁 37 的 2016 欄列 **79**；[2017 Annual Report](https://dieterengroup.imgix.net/annual-reports/annualreport2017_en_0-1.pdf)印刷頁 7 明載 2016 年底為 **79**。新稿採兩份年報相互支持的年底數字，在 `source-matrix.md` S6 留下與投資人簡報相衝的紀錄。批發銷售據點的 `doors` 仍與直營店分開。

## 保留與待驗

- 94 個場景 ID、順序、`look`、21 條 `loops`、67 張插畫和 27 張字卡不變；另外 93 句旁白的 ID、文字與情緒不變。`script.md` 與 `narration-draft.md` 同步更正同一個數字。
- `verify-1.md` 至 `verify-4.md`、既有盲評及畫面複核收據按當時的稿件雜湊保留，不默改其中的 78 或把舊 PASS 套到新版。新數字仍須獨立核對來源與現行稿件。
- 原 `build-local-video.mjs` 是 83 插畫／11 字卡和 78 家投資人簡報讀值的歷史產生器；現在明標 archival，已移除寫入 `video.json` 的路徑。不得用它重建現行 67／27 影片。
- 本次未執行 TTS、圖片、配樂或組裝。既有 `c031202` 音檔、時間軸及字幕仍是舊句；先做單句 TTS 乾跑和必要重錄，再量正文純語音是否達 480 秒，並重新做音訊與成片檢查。上傳、發布與站主看片仍各自另行驗收。
