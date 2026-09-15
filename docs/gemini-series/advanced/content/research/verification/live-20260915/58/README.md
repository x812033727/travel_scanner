# 第 58 篇：引用、矛盾與未知實測

[返回研究批次](../../../README.md) · [原作者教材](../../../58/lesson.md) · [完整修訂稿](../../../revisions/20260915-58/lessons/58.md)

2026-09-15，Windows／Chrome／個人 Google AI Pro，使用本篇三份合成教材建立獨立 Notebook。三次人工提示、三份保存筆記；API 零次、額外支出 NT$0。後端模型型號未顯示，不自行推定。沒有更改分享權限；私人連結只保存在被 Git 忽略的 `../private/58-links.json`，不放進下載包。

## 真實回答與修正

| 回答 | 送出時間 UTC | 保存檔 | 審閱結果 |
| --- | --- | --- | --- |
| 五項原始回答 | 05:45:45 | initial.json | 名額 30 人正確，但日期與條件措辭過度確定 |
| 餐點、停車、退款 | 05:47:16 | unknown.json | 均保持未知；餐點與停車後引用容易被誤認為直接支持 |
| 修訂矩陣與未知清單 | 05:48:22 | corrected.json | 核心五列與兩項未知通過人工審閱；表格格式仍有瑕疵 |

第一輪把預定日期寫成「唯一確定之預定日期」，又把收到確認信擴大成「唯一必要條件」。這些是實際回覆中的問題。第二輪沒有捏造餐點、車位或退款金額，但在餐點與停車缺資料的敘述後加入 E1 引用；點開可見 E1 並沒有直接提供這些資訊。因此第三輪明確要求分開「已查來源」與「支持引文」，並保留預定、尚未決定等限制。

修訂後 C1 有效名額 30 人；C2 原預定 10 月 3 日、10 月 4 日只是待確認提案；C3 報名表負責人未指派；C4 僅保留原文確認信條件；C5 退款金額未知。C2 的 conflict 是工作表中「需保留資訊並待確認」分類，不代表兩個日期都是已確定的互斥公告。U1 餐點、U2 停車均 unknown，支持原文留空，另列已查 E1／E2／E3 與補件需求。

`citations.json` 保存第一輪七筆、未知題三筆、修訂矩陣七筆，共十七筆成功引用觀察。每筆均實際點擊並保存來源面板文字，三份原文也各自開啟核對。短文件顯示整份原文，因此章節與句子另由人工比對，沒有宣稱每次引用都精準反白單句。引用操作中曾發生工具逾時，已重新擷取既有回答與引用；未因此追加模型問題或將逾時當成模型錯誤。十七筆是保存的觀察數，不是所有嘗試點擊的總數。

## 保存與重開

三次回答各存一份筆記，保留 v1 與修正版。重新整理後三個回答的 FNV 校驗值依序為 `4aa8574e`、`f39231c1`、`5359b8cb`，與原擷取完全相同，三份來源仍選取。重開修正版筆記，文字等於原回答去除未展開按鈕標籤；再點 C2 的 E2 引用，仍看到「也許改到」與「尚未決定」原句。此第十八筆觀察另存 `reopen-check.json`，不重複計入十七筆回答引用。

原始文字保留 `Thoughts`／`expand_more`／`more_horiz` 等介面標籤，未擷取展開思考內容。修正版把原本二級章節寫成 `####`，部分表格換行顯示字面 `<br>`。這是未修飾的實際輸出；不能宣稱格式全部正確。

## 衍生資料與可重現故障

`normalize-matrix.py` 從 `corrected.json` 擷取五列，移除介面引用數字、整理來源分隔符號、把章節名稱與逐字原文分欄，輸出 `evidence-matrix.csv`。它沒有改寫主張或判斷；`normalization.json` 記錄變換與原檔雜湊。`unknown-register.json` 將 U1／U2 的已查來源與空支持引文分開。這兩份是 Codex 整理的模型衍生檔，不冒充 Notebook 直接下載的 CSV，也不覆寫原作者參考矩陣。

`run-fault-lab.py` 呼叫既有 `research_checks.evidence`，四個實際離線結果如下：

| 測試 | 字串／結構檢查 | 人工判斷 |
| --- | --- | --- |
| 審閱後矩陣 | accepted | 五列符合本次來源 |
| 把 E2 引文改為「總共有 54 人」 | rejected: fabricated_quote | 假引文，拒絕 |
| 保留真正引文，主張改為 54 人 | accepted | 拒絕：替代關係不能相加 |
| 還原正確主張與引文 | accepted | 30 人；日期仍保留待確認提案 |

後三列是刻意製造和修復的本機故障，沒有假稱模型曾輸出 54 人。原檢查器回傳 `modelCitationClicksTested: false`，表示該離線程式不執行瀏覽器點擊；真實點擊證據在另列的 capture 檔。它也不評估主張語意，所以 accepted 不代表論證正確。

## 檢查與限制

從 repository 根目錄執行：

```powershell
python docs/gemini-series/advanced/content/research/verification/live-20260915/58/normalize-matrix.py
python docs/gemini-series/advanced/content/research/verification/live-20260915/58/run-fault-lab.py
python docs/gemini-series/advanced/content/research/verification/live-20260915/audit-live58.py
```

前兩項可重建衍生檔與故障，第三項核對凍結證據、回答／筆記 FNV、來源原文、引用、五列章節、重開結果及 176 個歷史作者檔案。均不呼叫 Google。下載 ZIP 另附獨立雜湊檢查與離線故障指令；上述 repository 路徑不適用於解壓目錄。

[聊天與引用官方說明](https://support.google.com/gemininotebook/answer/16179559)及[來源官方說明](https://support.google.com/gemininotebook/answer/16215270?hl=en)查證於 2026-09-15。本輪只驗證三份短教材與三次回答，不推論其他文件或模型都不會出錯。手機依使用者要求先跳過；第 59–62 篇、整套整合、發布與 sitemap 尚待完成。
