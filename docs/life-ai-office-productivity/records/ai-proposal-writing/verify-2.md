# ai-proposal-writing 查核第二輪（2026-10-05，非撰稿者、非第一輪查核者）

所有頁面今天重抓（curl -sSL，UA 照規定），存於 `_tools/ai-proposal-writing/verify2/pages/`，HTML 先去掉 `<!-- -->` 註解再轉文字，PDF 用 pdftotext。

格式：主張｜結果（ok / fixed / unresolved）｜來源網址｜怎麼讀到的

## A1. 第一輪改過的事實

- 編審要點第五點在 114 年 2 月 4 日以院授發管字第1141400149號函修正（含附表二、附表三人權影響評估檢視表、附表四淨零轉型自評檢核表；第一項第八款第三目與第二項人權部分自 114 年 7 月 1 日生效）｜ok｜https://www.ey.gov.tw/File/5B5C5FDCFE8479A9?A=C｜curl 200 application/pdf，pdftotext 逐字讀到。
- 骨架句的事項名稱（計畫緣起、計畫目標、執行策略及方法、期程與資源需求、預期效果及影響、財務計畫、附則含風險管理）｜ok，但 fixed 措辭｜https://ws.ndc.gov.tw/Download.ashx?u=LzAwMS9hZG1pbmlzdHJhdG9yLzEwL3JlbGZpbGUvNTU2Ni80ODAzL2U2NjVlYTliLTkzYzItNDA4Ny1iMjRhLWE3ZTA1MDM4ZTc2ZS5wZGY%3D&n=6KGM5pS%2F6Zmi5omA5bGs5ZCE5qmf6Zec5Lit6ZW356iL5YCL5qGI6KiI55Wr57eo5a%2Bp6KaB6bueKOWQq%2BmZhOihqCkucGRm&icon=..pdf｜curl 200 PDF，沿革最後一筆 107-10-19，第五點（一）到（八）與正文一致。正文原本寫「第五點列出……」，讀起來像現行條文；改成「107 年 10 月的版本從……」並把「修正過」改成「又修正過」，讓讀者知道列舉的是哪一版。法規名稱也從簡稱「行政院的《中長程個案計畫編審要點》」改成全名《行政院所屬各機關中長程個案計畫編審要點》（與 PDF 標題、114 年函主旨一致）。
- 第五點第二款（產出型或成果效益型指標）與第十點（修正內容對照表）已不再歸屬於編審要點｜ok（正文確實已無這兩處歸屬；第六段與第三十六段只剩一般建議）｜—
- Gemini：在提示框輸入「@」選檔案當參考｜ok｜https://support.google.com/docs/answer/14206696?hl=en｜curl 200。原文："At the bottom bar, click Sources > Add from Drive or other location. Or, you can type "@" and then search and select from the menu."
- Gemini：對話紀錄在重新整理瀏覽器、關閉再開啟文件、電腦離線時遺失，先插入文件｜ok｜同上｜原文三條 "You refresh your browser / You close and reopen the document / Your computer goes offline"，以及 "insert generated output in the document"。
- Microsoft 版本歷程頁標題「檢視舊版 Office 檔案」｜ok｜https://support.microsoft.com/zh-tw/office/collab-files/view-previous-versions-of-office-files｜`<title>` 解碼後為「檢視舊版 Office 檔案 | Microsoft Support」。
- NDC PDF 的 sources 標題寫明「107 年 10 月修正版全文」｜ok｜同上 NDC PDF｜沿革最後一筆確為 107 年 10 月 19 日。

## A2. 第一輪無法確認的

- 現行（114-02-04）第五點全文、112 年修正後的第十點｜unresolved｜theme.ndc.gov.tw 法規頁與 NewsContent?id=222：curl 403、WebFetch 503；ws.dgbas.gov.tw 112 年版 PDF：curl TLS 驗證失敗（不繞過）、WebFetch 503；WebFetch 不能連 web.archive.org。另找到兩份官方網域的副本：pbs.npa.gov.tw（98 年 4 月版）與 taoyuanairport.com.tw（107 年版），都不是現行版。ey.gov.tw 人權資訊網只寫「依第5點規定……應進行人權影響評估」，人權影響評估機制研修小組第 8、9 次會議紀錄沒有第五點條文。WebSearch 摘要說 114 年版第五點仍以計畫緣起、計畫目標……開頭，但摘要不是來源，不據以改寫。處理：正文明寫列舉的是 107 年 10 月版本，並保留「現行條文以國家發展委員會公告為準」；條文層級的細節（第二款、第十點）維持不寫。
- 預算法第 34 條｜ok｜https://law.moj.gov.tw/LawClass/LawSingle.aspx?pcode=T0020001&flno=34｜今天 curl 200 為真正條文頁。原文是「重要公共工程建設及重大施政計畫……始得編列概算及預算案」；正文漏了「建設」二字，fixed 為「重要公共工程建設與重大施政計畫」。
- 站內連結｜ok｜intake_check 三個 inline 都解析為 kind=life。
- intake WARN「no hero title found」｜預期內（自繪 hero、無 images.json）。

## A3. 抽查（verify-1.md 第 2、5、8……38 條，每三條取一）

- #2 description 與正文一致（三組提示詞、Word 與 Google 文件版本紀錄、決策紀錄欄位）｜ok｜—
- #5 第五點第二款歸屬已移除｜ok｜—
- #8 表格 caption「骨架參考行政院中長程個案計畫的格式，工具功能查證於 2026 年 10 月」｜ok｜—
- #11 Word Copilot 在對話窗格輸入「/」指定文件、郵件或會議｜ok｜https://support.microsoft.com/en-us/word/welcome-to-copilot-in-word｜"Type / in Copilot chat pane and start typing the name of a document, email, or meeting"
- #14 Copilot 列出 pressure-test ideas｜ok｜同上｜"Comprehend: Summarize a document, ask questions, or pressure-test ideas."
- #17 Gemini「@」｜ok｜見 A1
- #20 Gemini 從 Drive、Gmail、網路帶入統計、證據與引用｜ok｜https://support.google.com/docs/answer/14206696?hl=en｜原句逐字相符。
- #23 政府資料開放授權條款：依附件顯名聲明標示，未盡義務視為自始未取得授權｜ok｜https://data.gov.tw/license｜第三點第二款逐字相符；附件格式「提供機關／單位 [年份] [開放資料釋出名稱與版本號]」。
- #26 Google 文件：系統有時會合併修訂版本；命名版本不會被合併｜ok｜https://support.google.com/docs/answer/190843?hl=zh-Hant｜「系統有時會合併檔案的修訂版本」「確保系統不會合併這些版本」；另核每份文件 40 個已命名版本、需編輯權限、「上次編輯」圖示可查看／還原／建立副本。
- #29 個人帳戶最近 25 個版本、公司或學校帳戶看文件庫設定｜ok｜https://support.microsoft.com/zh-tw/office/collab-files/view-previous-versions-of-office-files｜「您可以擷取最近的 25 個版本……版本數量將取決於您的媒體櫃設定」；另核「僅適用於儲存在 Microsoft 365 中的 OneDrive 或 SharePoint 中的檔案」。
- #32 Google 文件「建議」模式｜ok｜https://support.google.com/docs/answer/6033474?hl=zh-Hant｜「在不變更原始文字的情況下……獲得擁有者核准，就會取代原始文字」。
- #35 個人帳號規則不同｜ok｜https://support.microsoft.com/en-us/word/welcome-to-copilot-in-word｜Privacy 段分列 work or school account 與 personal Microsoft account 兩個隱私頁。
- #38 hero 無數字、一行 12 字，alt 與圖相符｜ok｜重新渲染後目視：三層文件、橘藍版本標籤、深綠頁首與四組文字行、橘色數字標記經綠色打勾圓章以虛線連到藍框資料表的橘色格、左側藍色對話框與三列打勾橘框清單、底部一行字；沒有長條、曲線、金幣、logo、人臉。

## A4. 看圖

- diagram-1 重新渲染後目視：四欄三列泳道，文字都在框內、未壓線、未重疊，構圖上下置中；唯一數字 2026 在正文表格 caption 有。小注意：圖的順序是排大綱→補數字→找反方→寫摘要，正文章節順序是大綱→反方→數字→摘要；正文沒有宣稱章節即寫作順序，圖說也只說「由左到右是寫作順序」，不構成矛盾，未改。

## B. 合規

- 沒有實測、分數或「實測」字樣；三組提示詞都以「範本」標示，沒有宣稱效果｜ok
- 工具功能只寫 Microsoft 與 Google 說明頁寫到的，表格 caption 有查證年月｜ok
- 法規：預算法第 34 條條號與文字今天在全國法規資料庫核對（補「建設」二字）；編審要點改用全名並標明版本｜fixed
- 每個交給讀者使用的 AI 產出旁都有人工步驟：大綱（表格「人要確認的事」欄、材料不足標待補）、反方（「不一定成立……由你判斷」並寫入決策紀錄）、數字（數字清單＋親自打開原文）、摘要（每個數字回全文搜尋）｜ok
- 沒有推薦某一工具勝過另一個；Copilot 與 Gemini 並列，各寫官方說明的功能與方案需求｜ok
- callout 的企業版資料使用承諾以「微軟表示」「Google Workspace 也承諾」帶出，屬廠商自述，措辭沒有擴大｜ok

## C. 讀者優先與文字

- 「本文」「這篇」0 次；無驚嘆號、無「總結來說」；check_chars 只剩全形方括號［］（範本占位符用，屬正常）｜ok
- 正文沒有敘述查證過程；「查證」只出現在表格 caption 的查證年月（規格要求）｜ok
- 外文第一次出現：Copilot（AI 助理）、Gemini（Google 的 AI 助理）、OneDrive 或 SharePoint（微軟的雲端儲存與協作服務）、Google Workspace（Google 的企業版辦公套件）；Word、Gmail 是產品名，句中有「微軟」「郵件」帶出｜ok
- 導言第一段第一句就給答案（AI 省排結構、反方與摘要的時間，不保證數字、不記決策）｜ok
- 台灣用語（資料、軟體、使用者），標題用「數字查核」｜ok
- 正文字數：intake_check body_length 2,641（修改前 2,624），在 1,800–3,000 內、略高於 2,200–2,600 的目標；沒有灌水段落，未再刪減。

## D. 機械檢查

- `pack_cli ingest --dry-run`：exit 0，「dry run: nothing written」
- intake_check：RESULT PASS（0 failures），WARN 只有預期中的 hero title
