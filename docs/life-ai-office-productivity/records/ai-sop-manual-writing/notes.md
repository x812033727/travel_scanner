# ai-sop-manual-writing 查證記錄

查證日一律 2026-10-05（實際打開頁面的日期）。格式：主張｜來源網址｜查證日｜怎麼讀到的。
抓頁工具：`/home/user/batch-ai-office/_tools/ai-sop-manual-writing/fetch.sh`（curl -sSL、編輯部 UA、記 HTTP 狀態與最終網址），
`html2text.py` 先刪 `<!-- -->` 註解、script、style 再轉純文字；原始檔與文字檔在同目錄的 `pages/`。沒有用 Wayback。

## 步驟怎麼寫（技術寫作風格指南）

- 多步驟程序用編號清單；每個指示一個步驟，同一個介面位置的短步驟可合併；通常要寫出完成程序的動作（例如選取 OK 或 Apply）；先讓讀者知道在哪裡操作再描述動作；步驟以祈使動詞開頭、寫完整句子；簡單的連續選單可用「>」縮寫｜https://learn.microsoft.com/en-us/style-guide/procedures-instructions/writing-step-by-step-instructions｜2026-10-05｜curl 200，讀全文（頁尾 Last updated 2026-04-02）。
- 程序是一連串編號步驟；"In general, use one step for each action"，連續選單可用「>」合成一步；選擇性步驟開頭寫 "Optional:"；重複的程序不要重寫，改用參照與連結；先說在哪個工具或介面操作再說動作；先寫動作、後寫結果，結果放在同一段；介面元素難找時提供截圖｜https://developers.google.com/style/procedures｜2026-10-05｜curl 200，讀全文（Last updated 2026-06-08 UTC）。
- 「選擇性：」是 "Optional:" 的中文寫法，正文為改寫，不是官方中文譯名。

## 截圖（Google 風格指南圖片頁）

- 只在文字難以說明時用圖；截圖要節制，只截與討論相關的介面；截圖裁切到相關資訊，可讓介面其他部分改版時截圖不必重做；同一份文件截圖用同一套作業系統；不要用文字、程式碼或終端機輸出的圖片，改用真正的文字｜https://developers.google.com/style/images｜2026-10-05｜curl 200，讀全文（Last updated 2025-05-16 UTC）。
- 截圖不得含個人可識別資訊（PII）；原圖有 PII 時用 100% 不透明的純色色塊蓋住，不要用模糊、馬賽克，這類效果可被還原；輸出成可含圖層的格式（例如 PDF、TIFF）時要先合併圖層｜同上｜2026-10-05｜同上。正文「100%」出自此處。

## 標準作業程序的撰寫、試做、複審與文件控制（美國環保署 EPA QA/G-6）

- 文件版本：EPA/600/B-07/001，2007 年 4 月，取代 2001 年 3 月版。EPA 的頁面標題仍寫「EPA QA/G-6 from March 2001」，但連結的 PDF 是 2007 年 4 月版；sources 用 PDF 網址，標題寫 2007 年 4 月版｜https://www.epa.gov/sites/default/files/2015-06/documents/g6-final.pdf（入口頁 https://www.epa.gov/quality/guidance-preparing-standard-operating-procedures-epa-qag-6-march-2001，Last updated June 16, 2026）｜2026-10-05｜curl 200 application/pdf，pdftotext -layout 讀全文。
- SOP 應由熟悉該工作、實際執行工作或使用該流程的人撰寫；多工的流程可以團隊方式撰寫（2.1）｜同上｜2026-10-05｜同上
- SOP 要寫得夠詳細，讓經驗或知識有限、但有基本理解的人在無人監督下也能成功重現程序（2.1）｜同上｜2026-10-05｜同上。正文寫成「經驗不多、只有基本背景的人，在沒人指導下也能照著完成」。
- SOP 應由一位以上有相關訓練與經驗的人審查；"It is especially helpful if draft SOPs are actually tested by individuals other than the original writer before the SOPs are finalized."（2.2）｜同上｜2026-10-05｜同上。正文寫「建議定稿前由撰寫者以外的人實際試做」；「兩輪都順利才送核准」是編輯建議，不是 EPA 原文。
- 程序變更時 SOP 要更新並重新核准；應定期系統性複審，例如每 1 到 2 年（e.g. every 1-2 years）；描述已不再執行之流程的 SOP 應從現行檔案撤下並封存（2.3）｜同上｜2026-10-05｜同上。正文寫「每一到兩年」並標明是 EPA 舉的例子。
- 封面應有：清楚指出活動或程序的標題、SOP 編號、發行及／或修訂日期、適用的機關／單位名稱、撰寫與核准者的簽名與日期（3.1）｜同上｜2026-10-05｜同上
- 每頁（封面之後）的文件控制標註：短標題／編號、版次、日期、第幾頁共幾頁（2.5）｜同上｜2026-10-05｜同上
- 寫作：簡潔、逐步、易讀；用主動語態與現在式；可用流程圖說明（1.4、3.3）｜同上｜2026-10-05｜同上（正文未直接引用，供參）。
- 修訂紀錄範例欄位：Revision、Date、Responsible Person、Description of Change（附錄範例）｜同上｜2026-10-05｜同上。正文清單的「修訂紀錄：版次、日期、修改人、改了什麼」據此改寫。

## 錄音與逐字稿（微軟 Word 轉譯）

- 轉譯（Transcribe）把語音轉成文字並分隔每位講者；可播放帶時間戳記的音訊並編輯修正；選取任一段的時間戳記可播放該段｜https://support.microsoft.com/zh-tw/word/transcribe-your-recordings｜2026-10-05｜curl 200（原網址 /zh-tw/office/transcribe-your-recordings-7fc2efec-… 轉址至此），讀全文；英文版 https://support.microsoft.com/en-us/word/transcribe-your-recordings 同日 curl 200 交叉核對。
- 兩種方式：直接在 Word 錄製、上傳音訊檔；入口在「聽寫」（Dictate）下拉選單的「轉譯」。中文頁路徑寫作「[首頁>] 聽寫>[轉譯]」，英文寫 "Home > Dictate dropdown > Transcribe"；Word 中文介面的 Home 索引標籤一般叫「常用」，兩者不一致，正文只寫「在『聽寫』下拉選單裡」避開｜同上｜2026-10-05｜同上
- 上傳支援 .wav、.mp4、.m4a、.mp3｜同上｜2026-10-05｜同上
- 有 Microsoft 365 訂閱的使用者每月最多可轉譯 300 分鐘的上傳音訊（有 Microsoft Copilot 授權者 30,000 分鐘，正文未寫）｜同上｜2026-10-05｜同上
- 錄音與上傳的音訊存在 OneDrive 的「轉譯的檔案」資料夾，可在那裡刪除｜同上｜2026-10-05｜同上
- 語言清單（Language Availability，80+ locales）包含 Chinese (Taiwanese Mandarin)｜英文版同上網址｜2026-10-05｜同上
- 適用範圍：頁首注意事項寫「此功能目前僅適用於商業租用戶中的 Windows 版 Microsoft 365 Word；政府租用戶的謄寫功能僅適用於 Word 網頁版」，但同頁另有 Word 網頁版與 OneNote 的操作分頁，說法不一致；正文寫「適用版本以微軟說明為準」，不替讀者判斷｜同上｜2026-10-05｜同上

## 錄畫面與截圖（Windows 剪取工具、Mac 截圖 App）

- 剪取工具：Windows 標誌鍵 + Shift + S 開啟重疊以擷取影像；Windows 標誌鍵 + Shift + R 擷取影片剪輯，選取要錄製的區域後選「開始」｜https://support.microsoft.com/zh-tw/windows/apps/use-snipping-tool-to-capture-screenshots｜2026-10-05｜curl 200（原網址 /zh-tw/windows/use-snipping-tool-…-00246869-… 轉址至此），讀全文；英文版同日 curl 200 交叉核對。頁面沒有提到影片剪取時錄麥克風，正文因此不寫 Windows 能同時錄口述。
- 擷取後按「文字動作」啟用 OCR，可複製文字，或「快速修訂」剪取中的電子郵件地址與電話號碼；所有文字辨識都在裝置本機執行｜同上｜2026-10-05｜同上
- Mac：Shift + Command + 4 拖移十字線擷取部分螢幕；Shift + Command + 5 打開「截圖」App（macOS Mojave 10.14 或以上）｜https://support.apple.com/zh-tw/102646｜2026-10-05｜curl 200，讀全文（發佈日期 2026 年 09 月 21 日）。
- Mac 錄螢幕：Shift + Command + 5 打開「截圖」App，可錄整個螢幕或所選部分（所選視窗需 macOS Tahoe 26 以上）；「選項」中選一個麥克風可錄下說話聲；選「顯示滑鼠點按」時每次按一下指標周圍會顯示黑色圓圈｜https://support.apple.com/zh-tw/102618｜2026-10-05｜curl 200，讀全文（發佈日期 2026 年 09 月 21 日）。

## AI 的限制與技能

- Claude 可能產生不正確或誤導的回應（幻覺），可能寫出看起來正確但其實錯誤的內容；不應把 Claude 當成唯一的事實來源｜https://support.claude.com/en/articles/8525154-claude-is-providing-incorrect-or-misleading-responses-what-s-going-on｜2026-10-05｜curl 200，讀全文（頁面日期 March 16, 2026）。正文寫「它可能寫出看似正確其實錯誤的步驟」，泛指 AI，來源只有 Anthropic 這一家的說明。
- Skills 是 Claude 動態載入的指示、腳本與資源資料夾；Claude 會檢視可用技能並載入相關的；Free、Pro、Max、Team、Enterprise 方案可用；需要開啟程式碼執行｜https://support.claude.com/en/articles/12512176-what-are-skills｜2026-10-05｜curl 200，讀全文。

## 個資與營業秘密

- 個人資料保護法第 2 條第 1 款：個人資料指自然人之姓名、出生年月日、國民身分證統一編號、護照號碼、特徵、指紋、婚姻、家庭、教育、職業、病歷、醫療、基因、性生活、健康檢查、犯罪前科、聯絡方式、財務情況、社會活動及其他得以直接或間接方式識別該個人之資料｜https://law.moj.gov.tw/LawClass/LawSingle.aspx?pcode=I0050021&flno=2｜2026-10-05｜curl 200，讀到條文全文（不是錯誤殼頁）。頁首標示部分條文尚未生效（114 年 11 月 11 日修正條文施行日期由行政院定之），第 2 條本身未在該清單內。
- 營業秘密法第 2 條：營業秘密指方法、技術、製程、配方、程式、設計或其他可用於生產、銷售或經營之資訊，且符合：非一般涉及該類資訊之人所知、因其秘密性而具有實際或潛在之經濟價值、所有人已採取合理之保密措施｜https://law.moj.gov.tw/LawClass/LawSingle.aspx?pcode=J0080028&flno=2｜2026-10-05｜curl 200，讀到條文全文。正文只說「流程本身也可能是營業秘密」與要件之一，不做個案法律判斷。

## 沒有出處、屬編輯建議的內容（不是事實主張）

- 「邊做邊說」比憑記憶口述好、開錄前關通知與改用測試帳號、草稿保留【截圖】標記、試做時旁人只記錄不提示、兩輪試做、表格裡的口述改寫範例（含「兩成」門檻，已在表內註明由負責人訂）、提示詞範本：都是寫作建議與示意，沒有實測、不宣稱效果。
- 表格 caption 的「2026 年 10 月」是整理時間，同時讓圖解頁尾的 2026 在正文出現。

## 圖

- diagram-1.svg：七個環節的流程圖，圖上的數字只有步驟編號 01–07（工具視為步驟徽章）與頁尾 2026；正文 caption 有 2026。
- hero.svg：對話框（波浪線）→ 三個並排、同樣大小的橘色箭頭符號（機械與看圖關卡改掉原本的虛線彎箭頭：箭尖有殘段，且與問卷篇 hero 的橘色虛線彎箭頭雷同）→ 寫字板（四列等長步驟、三個綠勾、一個橘色菱形判斷點），一行字「從口述到可交接的步驟」（10 字，52 px）。沒有 logo、人臉、遞增長條。

## Fact-check round 1 (independent, 2026-10-05)

All 12 sources plus the EPA landing page and the en-us copies of both Microsoft support pages were re-fetched today with curl -sSL and the editorial UA (all HTTP 200, real content, comments stripped). Raw copies: /home/user/batch-ai-office/_tools/ai-sop-manual-writing/v1/pages/. Line-by-line verdicts: verify-1.md.

Corrections made to pack.json:
- Snipping Tool: Win+Shift+R video snip and the Text actions / Quick redact button appear only on the page's Windows 11 tab; the Windows 10 tab lists Win+Shift+S and PrtSc only. Body now says "Windows 11" in both places.
- Style guides: "keep the result in the same paragraph as the action" is stated by Google (Procedures > Steps with results or justifications); Microsoft only shows it in an example. Body now attributes that rule to Google alone (resolves writer doubt 4).
- Word Transcribe path: the zh-TW page's upload path reads "[常用]> [聽寫] 下拉式清單 >[轉譯]" (the record path reads "[首頁>] 聽寫>[轉譯]", a translation slip). Body now names the 「常用」 tab (resolves writer doubt 2).
- Word Transcribe scope: the "only available in Word for Microsoft 365 on Windows in Commercial Tenants" note sits under the page's Word for Windows tab; the Word for the Web tab has its own steps (Edge or Chrome, internet connection). It is tab-scoped, not a contradiction. Body now says Windows and web Word both have it; account-type limits left to Microsoft (resolves writer doubt 1).
- EPA 2.1 "unsupervised" now rendered 無人監督 (was 沒人指導); EPA 2.5 per-page notation now includes the ID number ("Short Title/ID #").
- Claude Skills: plans listed explicitly as Free, Pro, Max, Team, Enterprise (was "Free 到 Enterprise 各方案").

Checked and left as is: writer doubt 5 - the Claude help page attributes hallucination to "a byproduct of some of the current limitations of frontier Generative AI models, like Claude", so applying it to AI generally is supported. Writer doubt 3 (EPA 2007 PDF vs 2001 page title) confirmed: PDF foreword says it replaces EPA/240/B-01-004 of March 2001.

Body length after round 1: 2,654 (band 1,800-3,000; above the 2,600 aim by 54).

## Fact-check round 2 (independent, 2026-10-05)

All sources re-fetched today (curl -sSL, editorial UA, comments stripped, PDF via pdftotext); raw copies in /home/user/batch-ai-office/_tools/ai-sop-manual-writing/v2/pages/. All HTTP 200; the law.moj.gov.tw trade-secrets page first returned a 200 error shell ("This page can't be displayed") and was re-fetched until the article text appeared. Every round-1 correction re-confirmed; no factual changes. Compliance and wording edits only (dates on the Word Transcribe limit and the Skills plan list, article numbers on both statutes, human-check clauses next to Quick redact and Skills, intro paragraph 1 rewritten as one sentence, intro paragraph 2 no longer repeats it). Body length 2,681. Details: verify-2.md.

## 跨篇核對（2026-10-05）

- 在「文件頭、版次與新人試做」的欄位清單後加了連到 ai-proposal-writing 的 article inline（Word 與 Google 文件的版本記錄），檔案版本的細節不在這篇重寫。
- 個資法第 2 條今日重讀（全國法規資料庫，修正日期民國 114 年 11 月 11 日）：列舉項與正文一致，也與 ai-survey-design-analysis 的寫法一致。
- 重跑 dry-run 與 intake_check：0 FAIL，body_length=2681。
