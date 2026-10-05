# ai-proposal-writing 查證記錄

查證日一律 2026-10-05（實際打開頁面的日期）。格式：主張｜來源網址｜查證日｜怎麼讀到的。

## 企劃書骨架（行政院中長程個案計畫）

- 中長程個案計畫內容應包括：計畫緣起、計畫目標、現行相關政策及方案之檢討、執行策略及方法（主要工作項目、分期執行策略、執行步驟及分工）、期程與資源需求（期程、經費來源及計算基準、經費需求）、預期效果及影響、財務計畫、附則（含風險管理）（第五點）｜https://ws.ndc.gov.tw/Download.ashx?u=LzAwMS9hZG1pbmlzdHJhdG9yLzEwL3JlbGZpbGUvNTU2Ni80ODAzL2U2NjVlYTliLTkzYzItNDA4Ny1iMjRhLWE3ZTA1MDM4ZTc2ZS5wZGY%3D&n=6KGM5pS%2F6Zmi5omA5bGs5ZCE5qmf6Zec5Lit6ZW356iL5YCL5qGI6KiI55Wr57eo5a%2Bp6KaB6bueKOWQq%2BmZhOihqCkucGRm&icon=..pdf｜2026-10-05｜curl -sSL 200，application/pdf，pdftotext 讀全文。PDF 是國發會網站的下載檔，修正沿革最後一筆為 107 年 10 月 19 日院授發綜字第 1070801867 號函修正。國發會主管法規系統（theme.ndc.gov.tw/lawout/LawContent.aspx?id=GL000455）與 ndc.gov.tw 回 Cloudflare 403，Wayback 連線被重置，無法確認 107 年之後是否另有修正；WebSearch 的摘要也只列到 107 年 10 月。
- 計畫目標「應具體說明，並盡量以產出型或成果效益型指標為原則」（第五點第二款）｜同上｜2026-10-05｜同上（查核第一輪：此款屬已於 114 年修正的第五點，現行條文讀不到，正文已不引用此款）
- 修正計畫應包括：計畫修正理由說明、修正目標（含績效指標、衡量標準及目標值）、修正內容對照表等（第十點）｜同上｜2026-10-05｜同上（查核第一輪：112 年另有一次修正，現行第十點讀不到，正文已不引用此點）
- 自評檢核表「財源籌措及資金運用」：經費需求合理性（經費估算依據如單價、數量等計算內容）；「風險管理」：是否對計畫內容進行風險管理（附表一）｜同上｜2026-10-05｜同上
- 預算法第 34 條：重要公共工程建設及重大施政計畫，應先行製作選擇方案及替代方案之成本效益分析報告，並提供財源籌措及資金運用之說明，始得編列概算及預算案｜https://law.moj.gov.tw/LawClass/LawSingle.aspx?pcode=T0020001&flno=34｜2026-10-05｜curl 回 200 但內容是 MOJ 的「Unreachable Server」錯誤殼頁，不算來源；改用 WebFetch 讀到條文全文（頁尾法規資料更新至民國 115 年 9 月 24 日）。

## 官方統計與開放資料

- 中華民國統計資訊網由行政院主計總處維運，有統計發布訊息、主計總處統計專區、中央機關統計網站與縣市政府統計網站的入口｜https://www.stat.gov.tw/｜2026-10-05｜curl -sSL 200，讀首頁導覽文字。
- 政府資料開放授權條款－第1版（中華民國104年7月27日訂定）：使用者利用開放資料及衍生物，應以符合附件「顯名聲明」要求之方式，明確標示原資料提供機關之聲明；未盡顯名標示義務者，視為自始未取得開放資料之授權（第三點第二款）｜https://data.gov.tw/license｜2026-10-05｜curl -sSL 200，讀全文。
- 顯名聲明格式：提供機關／單位 [年份] [開放資料釋出名稱與版本號]，並說明依政府資料開放授權條款釋出（附件）｜同上｜2026-10-05｜同上

## AI 工具功能（只寫各家說明頁寫到的）

- Copilot in Word：可從提示詞、大綱、筆記或引用的檔案起草（Create）；改寫、調整語氣（Refine）；摘要文件、提問、壓力測試想法（Comprehend: "Summarize a document, ask questions, or pressure-test ideas"）；範例問法 "What decisions are needed before this document is ready to share?"；在對話窗格輸入「/」可指定要參考的文件、郵件或會議；在共用文件中會先在對話窗格預覽建議的變更，核准後才寫入；需要符合資格的 Microsoft 365 訂閱或 Microsoft Copilot 授權；Copilot 支援的語言比 Word 介面少｜https://support.microsoft.com/en-us/word/welcome-to-copilot-in-word｜2026-10-05｜curl -sSL 200（由 /en-us/office/welcome-to-copilot-in-word-2135e85f-… 轉址），讀全文。
- Copilot in Word FAQ：建議來自 AI，可能出錯、誤解事實或產生不正確結果，接受前要審閱；生成內容可能不正確或不恰當，它無法理解意思或評估正確性；要審閱、編輯並查證；品質預期以英文最高｜https://support.microsoft.com/en-us/word/frequently-asked-questions-about-copilot-in-word｜2026-10-05｜curl -sSL 200，讀全文。
- Gemini in Google Docs：右上角「Ask Gemini」開側邊欄，開啟有文字的文件時側邊欄會顯示摘要；可用「@」或底部 Sources → Add from Drive 指定參考檔案；"Gemini can pull stats, evidence, and citations directly from your Google Drive, Gmail, or the web into your document."；側邊欄對話在重新整理瀏覽器、關閉再開文件、電腦離線時會遺失，提示先把產出插入文件；需要符合資格的 Google Workspace 或 Google AI 方案｜https://support.google.com/docs/answer/14206696?hl=zh-Hant｜2026-10-05｜curl -sSL 200，頁面只有英文版（zh-Hant 顯示「目前並未提供你慣用的語言版本」），讀全文。

## 版本與審稿功能

- Google 文件：右上角「上次編輯」圖示開版本記錄，可查看、還原、複製舊版本；必須有編輯權限才看得到舊版本；可「為這個版本命名」，命名版本不會被合併；每份文件最多 40 個已命名版本（試算表 15 個）；系統有時會合併修訂版本；版本記錄刪除後無法復原｜https://support.google.com/docs/answer/190843?hl=zh-Hant｜2026-10-05｜curl -sSL 200，讀全文；英文版（hl=en）同樣寫 "up to 40 named versions per document"，交叉確認。
- Google 文件「建議」模式：在不變更原文的情況下提出修訂建議，擁有者接受後取代原文；Microsoft Office 的追蹤修訂與 Google 文件的修訂建議在轉檔時互相轉換｜https://support.google.com/docs/answer/6033474?hl=zh-Hant｜2026-10-05｜curl -sSL 200，讀全文。
- Microsoft 365 版本歷程記錄只適用於存在 OneDrive 或 SharePoint 的檔案；個人 Microsoft 帳戶可擷取最近 25 個版本，公司或學校帳戶的版本數量取決於文件庫設定｜https://support.microsoft.com/zh-tw/office/collab-files/view-previous-versions-of-office-files｜2026-10-05｜curl -sSL 200，讀全文；英文版同句 "last 25 versions" 交叉確認。
- Word 追蹤修訂：「校閱」索引標籤 → 追蹤 → 追蹤修訂；刪除以刪除線、新增以底線標示，不同作者不同顏色｜https://support.microsoft.com/zh-tw/word/training/track-changes-in-word｜2026-10-05｜curl -sSL 200（由 197ba630-… 舊網址轉址），讀全文。注意：頁面中文是「檢閱」索引標籤。

## 資料使用（企業版）

- Microsoft Copilot（原 Microsoft 365 Copilot）：提示詞、回應與透過 Microsoft Graph 存取的資料不用於訓練基礎 LLM｜https://learn.microsoft.com/en-us/microsoft-365/copilot/microsoft-365-copilot-privacy｜2026-10-05｜curl -sSL 200，頁面 updated_at 2026-09-30，讀相關段落。
- Google Workspace：未經客戶事先許可或指示，不用客戶資料（含提示詞）訓練模型；內容不會在網域外用於生成式 AI 模型訓練｜https://knowledge.workspace.google.com/admin/generative-ai/generative-ai-in-google-workspace-privacy-hub｜2026-10-05｜curl -sSL 200（support.google.com/a/answer/15706919 轉址到此），讀 Model training and data usage 段。

## 編輯決定

- 標題微調：「數據查核」改「數字查核」（正文全篇用「數字」，台灣用語），意思不變。
- 圖解 diagram-1 上唯一的阿拉伯數字是頁尾的 2026，正文表格 caption「查證於 2026 年 10 月」有；其餘用「第一步」到「第四步」。
- hero 不放長條、曲線或金幣；唯一一行字「企劃書的每個數字都有出處」（12 字，46 px）。
- 正文的提示詞範本是寫法示範，不宣稱實測效果；沒有任何工具的實測結果。
- 預算法第 34 條原文是「重要公共工程建設及重大施政計畫」，正文寫「重要公共工程與重大施政計畫」，意思相同。
- 中長程個案計畫的骨架在正文寫成「計畫緣起、目標、執行策略及方法、期程與資源需求、預期效果、財務計畫等項目，並在附則做風險管理」，省略了「現行相關政策及方案之檢討」，用「等項目」帶過。

## 讀不到、沒有用的

- OpenAI help center（canvas 的版本記錄、"Does ChatGPT tell the truth"）：curl 與 WebFetch 都回 403，.json 讀法也 403/404；只拿到 WebSearch 摘要，不足以當來源，正文不寫 ChatGPT canvas 的功能。
- 國發會「行政院及所屬各機關風險管理及危機處理作業手冊」：ndc.gov.tw 回 403，沒有讀到官方檔，正文的風險欄位（可能性、影響、對策、負責人）寫成一般做法，不宣稱出自該手冊。


## 查核第一輪（2026-10-05，獨立查核，非撰稿者）

所有來源今天重抓，存於 _tools/ai-proposal-writing/verify1/pages/。逐條結果見 verify-1.md。

- 編審要點不是 107 年版：行政院 114 年 2 月 4 日院授發管字第1141400149號函修正第五點（含附表二性別、新增附表三人權影響評估、附表四淨零轉型通案自評檢核表；人權部分自 114 年 7 月 1 日生效）｜https://www.ey.gov.tw/File/5B5C5FDCFE8479A9?A=C｜2026-10-05｜curl -sSL 200 application/pdf，pdftotext 讀全文（一頁函稿）。行政院人權資訊網 https://www.ey.gov.tw/hrtj/53E0BF079282B90A 也寫「依編審要點第5點規定…應進行人權影響評估」。WebSearch 另列出 112 年 8 月 11 日院授發管字第1121401662號函修正版（主計總處 ws.dgbas.gov.tw 檔案）。
- 讀不到現行全文：theme.ndc.gov.tw 與 ndc.gov.tw 403；ws.dgbas.gov.tw 的 112、114 年版 PDF：curl TLS 驗證失敗、WebFetch 503；web.archive.org 連線被代理切斷（archive.org 的 availability API 顯示 20250712 有快照，但抓不到）；moea.gov.tw 403；ctsp.gov.tw 連線被切斷。gec.ey.gov.tw 的「編審要點.pdf」只是一張指向 NDC 法規系統的連結頁。
- 因此正文改法：骨架句保留第五點的事項名稱（107 年版全文今天讀得到，114 年函的生效條款仍提到「第一項第八款第三目」，表示第一項仍有附則等八款結構），並加上「這一點在 114 年 2 月修正過，現行條文以國家發展委員會公告為準」；目標段刪掉「編審要點要求…產出型或成果效益型指標」的歸屬，改成一般寫法；版本段刪掉「政府中長程計畫修正時要附修正理由說明與修正內容對照表」的歸屬（第十點的現行文字讀不到）。sources 的 NDC PDF 標題改註明「107 年 10 月修正版全文」，新增 114 年行政院函。
- 預算法第 34 條：今天 curl -sSL 直接 200 並讀到條文全文（不是錯誤殼頁），內容與正文相符。
- Gemini in Docs：「@」與 Sources → Add from Drive 寫在 Reference other files 段，位置是 bottom bar／prompt，不是側邊欄的描述；正文改成「在提示框輸入「@」」，對話遺失的三種情形補齊（重新整理、關閉再開、離線）。來源網址改用 hl=en（zh-Hant 只顯示「未提供你慣用的語言版本」橫幅，內容相同）。
- Microsoft 版本歷程記錄頁的實際標題是「檢視舊版 Office 檔案」，sources 標題照改。
- 其餘（Copilot in Word 起草／「/」／共用文件先預覽再核准／pressure-test ideas／方案需求；Copilot FAQ 不正確與無法評估正確性；Google 版本記錄 40 個命名版本、有時合併、需編輯權限；建議模式；Word 追蹤修訂；Microsoft 25 個版本；Microsoft Learn 不用於訓練基礎 LLM（updated_at 2026-09-30）；Workspace 未經許可不用客戶資料訓練；data.gov.tw 授權條款第三點第二款與顯名聲明；統計資訊網的中央機關與縣市統計網站入口）今天逐字比對無誤。
- 站內連結三個皆指向指派的 slug，repo 內三篇都存在且 kind=life。

## 查核第二輪（2026-10-05）

逐條見 verify-2.md；頁面存於 _tools/ai-proposal-writing/verify2/pages/。

- 114 年 2 月 4 日行政院函（第五點修正）今天 curl 200 PDF 重讀無誤。現行第五點全文仍讀不到：theme.ndc.gov.tw 403／WebFetch 503，ws.dgbas.gov.tw TLS 驗證失敗（未繞過）／WebFetch 503，web.archive.org 無法連線；pbs.npa.gov.tw 與 taoyuanairport.com.tw 的副本是 98 年與 107 年版。正文改為明寫「107 年 10 月的版本」列出的事項，並用法規全名《行政院所屬各機關中長程個案計畫編審要點》。
- 預算法第 34 條原文「重要公共工程建設及重大施政計畫」，正文補上「建設」。
- Gemini「@」與對話遺失三條件、Microsoft 版本頁標題、25 個版本、Google 40 個命名版本與合併、建議模式、顯名聲明、Copilot「/」與 pressure-test ideas 今天重讀無誤。

## 機械與看圖關卡（2026-10-05）

- dry-run 通過、intake_check 0 FAIL；唯一 WARN「no hero title found to check uniqueness」是自繪 hero 沒有 images.json 的預期結果。事實未改動。
- diagram-1.svg：箭頭 marker 的 refX 由 9 改 7，橫向箭頭 x2 與縱向箭頭 y2 各縮 3 px。原本 4 px 粗的線段終點只在尖端後 1.6 px，線段兩角從三角形兩側露出，尖端變鈍；改後尖端銳利，離下一個框約 2 px。
- hero.svg：左上對話框裡的三個圓點改成一條藍色標題列加兩條縮排條列（大綱），避免與 ai-official-documents-taiwan 的 hero（同樣是三點對話框接文件）共用母題；hero 的 desc 與 pack.json 的 hero alt 同步改寫。其餘構圖（三層版本頁、橘色數字標記經打勾圓章連到資料表）是本批獨有。
- 重新渲染後目視：兩張圖文字都在框內、未壓線、未互疊，字級最小 15，構圖上下大致置中；圖上唯一數字 2026 在表格 caption 有。

## 跨篇核對（2026-10-05）

- 在「每個數字回到原始資料」一節加了連到 ai-survey-design-analysis 的 article inline（問題段的證據要自己發問卷時）。
- Microsoft Learn 隱私頁今日重讀：頁首註明 Microsoft 365 Copilot 已更名為 Microsoft Copilot，頁名是 Data, Privacy, and Security for Microsoft Copilot；「Prompts, responses, and data accessed through Microsoft Graph aren't used to train foundation LLMs」不變。sources 標題補上更名說明，與 ai-survey-design-analysis 一致；正文寫「以公司帳號使用的 Copilot」，不必改。
- Google Workspace Privacy Hub 今日重讀：「Use your prompt, Workspace content ... to train generative AI models without your permission」列在不做的事，與正文一致。
- 重跑 dry-run 與 intake_check：0 FAIL，body_length=2641。
