# ai-proofreading-terminology 查證記錄

查證日一律 2026-10-05（實際打開頁面的日期）。格式：主張｜來源網址｜查證日｜怎麼讀到的。
所有 curl 都用 `-sSL`、UA「Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)」，先剝掉 `<!-- -->` 註解再讀。
本篇不含任何實測結果：沒有安裝或執行 OpenCC、沒有拿任何 AI 工具實際校稿；所有工具行為都來自該工具自己的文件或資料檔。

## 兩岸用語（教育部辭典）

- 《國語辭典簡編本》附錄「兩岸常用詞語對照表」：欄位為「臺灣語詞｜大陸語詞」；資料來源為中華語文知識庫／兩岸差異用詞與《兩岸每日一詞．一般名詞對照表》（中華文化總會授權提供）｜https://dict.concised.moe.edu.tw/appendix.jsp?ID=54｜2026-10-05｜curl 200，共 7 頁（page=1..7），以 `_tools/ai-proofreading-terminology/concised_pairs.py` 逐頁抓表格，共 620 列，存成 concised_pairs.json。
- 表中各列，正文表格與摘要用到的：軟體＝軟件；資料＝數據；影片＝視頻；程式＝程序；列印＝打印；品質＝品質／質量。查過但最後刪掉的列（控制字數）：網路＝網絡；螢幕＝屏幕／螢屏／視屏／螢光屏；滑鼠＝鼠標／鼠標器；部落格＝博客。其他參考：硬碟＝硬盤、伺服器＝服務器、資訊＝信息、專案＝項目、土豆＝花生／落花生／長生果、馬鈴薯＝洋芋／山藥蛋／馬鈴薯／土豆｜同上｜2026-10-05｜同上。注意：「使用者／用戶」不在這張表裡，所以正文只把它當成「同一份文件混用兩種寫法」的例子，沒有寫成兩岸對照。
- 表格「校稿時注意」欄：軟件（只換字形會留下，依 OpenCC 字表與 TWPhrases）；數據（修訂本「數據」釋義）；視頻→也可能是視訊（OpenCC TWPhrases 的兩個候選）；程序（修訂本「程序」釋義）；質量（修訂本「質量」釋義，見下段）。
- 《重編國語辭典修訂本》「質量」：義項包括「專指事物的品質。今大陸地區沿用之。」與「物體內所含物質的量。」｜https://dict.revised.moe.edu.tw/dictView.jsp?ID=113680｜2026-10-05｜curl 200，讀釋義全文。
- 《重編國語辭典修訂本》「土豆」：「落花生」的別名；大陸地區指馬鈴薯；「葫蘆茶」的別名｜https://dict.revised.moe.edu.tw/dictView.jsp?ID=54254｜2026-10-05｜curl 200（搜尋只有一筆時直接顯示詞條，ID 從搜尋頁取得後再開 dictView）。
- 《重編國語辭典修訂本》「程序」：辦事的一定規則次序；相似詞 步驟、次序｜https://dict.revised.moe.edu.tw/dictView.jsp?ID=124548｜2026-10-05｜curl 200。
- 《重編國語辭典修訂本》「數據」：經由調查或實驗得到，而尚未經過有效處理的數值｜https://dict.revised.moe.edu.tw/dictView.jsp?ID=133742｜2026-10-05｜curl 200。
- 《重編國語辭典修訂本》「公布」：把法律或命令公告周知；向公眾揭示某種事實；也作「公佈」｜https://dict.revised.moe.edu.tw/dictView.jsp?ID=75132｜2026-10-05｜curl 200。（同類例子：「雇主」也作「僱主」，ID=71572，未放進 sources。）
- 其他查過但未放進正文：「軟體」「影片」「滑鼠」「視訊」「項目」（事物分類的條目，ID=110258）「信息」（消息、音訊，ID=109410）「文件」（書札、公文之類的統稱，ID=162174）。

## 標點與術語

- 《重訂標點符號手冊》修訂版．引號：「」『』；用於標示說話、引語、特別指稱或強調的詞語；通常先用單引號，需要時單引號內再用雙引號｜https://language.moe.gov.tw/001/upload/files/site_content/m0001/hau/h6.htm｜2026-10-05｜curl 200，Big5 編碼，iconv 轉 UTF-8 後讀全文。
- （查過未用）書名號：《》多用於書名，〈〉多用於篇名｜https://language.moe.gov.tw/001/Upload/FILES/SITE_CONTENT/M0001/HAU/h12.htm｜2026-10-05｜同上。
- 國家教育研究院「樂詞網」：提供學術名詞、雙語詞彙與辭書查詢（關於我們頁：學術名詞 206 類約 193 萬則、雙語詞彙 21 類約 2 萬則、辭書 9 部約 6 萬則；正文沒有寫數字）｜https://terms.naer.edu.tw/（關於我們：https://terms.naer.edu.tw/mysite/about/1/）｜2026-10-05｜curl 200。

## 繁簡一對多（Unicode／OpenCC）

- Unihan kTraditionalVariant：U+53D1 发 → U+767C 發、U+9AEE 髮｜https://www.unicode.org/cgi-bin/GetUnihanData.pl?codepoint=53D1｜2026-10-05｜curl 200，讀 Variants 區。
- 同一資料庫其他字（正文清單用到，sources 只放 发 一筆以免超過 20 筆）：U+5E72 干 → 乾、干、幹；U+540E 后 → 后、後；U+53F0 台 → 台、檯、臺、颱；U+590D 复 → 复、復、複、覆；U+9762 面 → 面、麵；U+91CC 里 → 裏、裡、里；（未用：只、松、余、历、钟）｜https://www.unicode.org/cgi-bin/GetUnihanData.pl?codepoint=5E72 等｜2026-10-05｜curl 200。
- OpenCC STCharacters.txt：发→發 髮；干→幹 乾 干 榦；后→後 后；台→臺 檯 颱 台；复→復 複 覆；面→面 麪；里→裏 里 哩｜https://github.com/BYVoid/OpenCC/blob/master/data/dictionary/STCharacters.txt｜2026-10-05｜github.com 在這個環境經代理回 403，改讀同一 repo master 分支的 raw.githubusercontent.com/BYVoid/OpenCC/master/data/dictionary/STCharacters.txt（200）。sources 寫 github.com 原始網址。
- OpenCC STPhrases.txt：头发→頭髮、理发→理髮、发展→發展、干燥→乾燥、饼干→餅乾、干部→幹部、干涉→干涉、以后→以後、后来→後來、皇后→皇后、台灯→檯燈、台风→颱風、恢复→恢復、复制→複製、答复→答覆、面条→麪條、这里→這裏、公里→公里；「软件」「数据库」不在詞組表，軟件由逐字對應產生（软→軟，件不變）｜https://github.com/BYVoid/OpenCC/blob/master/data/dictionary/STPhrases.txt｜2026-10-05｜同上，讀 raw。注意：OpenCC 標準繁體用「麪」「裏」，台灣字形層（TWVariants.txt：麪→麵、裏→裡）才換成台灣用字，所以正文清單寫台灣字形「麵條」「這裡」，並另說明 s2t 不等於台灣用字。
- OpenCC TWPhrases.txt（用於 s2twp）：軟件→軟體、數據→資料 數據、數據庫→資料庫、視頻→影片 視訊、菜單→選單 菜單、鼠標→滑鼠、打印→列印、程序→程式、網絡→網路、用戶→使用者、屏幕→螢幕、博客→部落格｜https://github.com/BYVoid/OpenCC/blob/master/data/dictionary/TWPhrases.txt｜2026-10-05｜同上，讀 raw。
- OpenCC TWVariants.txt：麪→麵、裏→裡、爲→為、着→著（用於 s2tw、s2twp、t2tw）｜raw.githubusercontent.com/BYVoid/OpenCC/master/data/dictionary/TWVariants.txt｜2026-10-05｜讀 raw；未放 sources（正文只說 s2t 不等於台灣用字，README 已足以支持）。
- OpenCC README：基於詞庫的確定性轉換，不使用大語言模型，結果穩定可預期、可離線；嚴格審校一簡對多繁詞條；支援地區慣用異體字（裏／裡）與習慣用詞（鼠標／滑鼠）；配置 s2t＝簡體到 OpenCC 標準繁體、s2tw＝簡體到台灣正體、s2twp＝簡體到台灣正體（含台灣常用詞彙）；`--inspect` 範例中「数据库」第一階段為「數據庫」、第二階段為「資料庫」；`--ambiguities` 標出詞典對應為一對多的輸出片段（例：文丑可為文丑或文醜），單一對應（头发→頭髮）不標；`--ambiguities` 需要原生 OpenCC CLI（Python 與 npm 的 CLI 不支援）｜https://github.com/BYVoid/OpenCC｜2026-10-05｜讀 raw.githubusercontent.com/BYVoid/OpenCC/master/README.md（200）；README 提到目前版本 1.4.2。
- OpenCC DESIGN_PRINCIPLES.md（查過未放 sources）：s2t 的目標是 OpenCC 標準繁體這個中間層，不是任何地區的實際用字；臺灣正體模式長期參考教育部《重編國語辭典修訂本》；s2tw 不會主動把詞組改寫為臺灣慣用語，s2twp 才加慣用語詞典｜raw.githubusercontent.com/BYVoid/OpenCC/master/DESIGN_PRINCIPLES.md｜2026-10-05｜讀 raw。

## 校對工具（微軟、Google）

- Microsoft Editor 各語言支援表：Chinese (Traditional) 一列為 Spell check ◌、Grammar check ●、Writing refinements ◌（英文三欄都是 ●）｜https://support.microsoft.com/en-us/word/editor-s-spelling-grammar-and-refinement-availability-by-language｜2026-10-05｜curl 200（舊網址 …-ecd60e9f-… 轉址到此），讀原始 HTML 的表格。頁面沒有圖例說明 ● 與 ◌，正文只寫「對繁體中文提供文法檢查」。
- 微軟「語法及完善指南的詳細敘述」（繁體中文，支援表的 Download details 連結）：需使用 Microsoft 365 帳號登入才會偵測；檢查項目含半形拉丁字母、中文引號、中文標點、易混淆錯字（我再你家門前→在）、數字格式、量詞、異體字選字（公佈→公布、僱主→雇主）、半形數字、冗贅標點、多餘空格、單字重複、注音符號、符號、形音相近錯字（以經→已經、因該→應該）、的地得、繁簡混用（后來→後來、几乎→幾乎、十多万→十多萬）｜https://download.microsoft.com/download/1/0/3/103d9025-7673-4746-8332-739f34b08a52/Editor%20guidance%20details_Chinese_Traditional.docx｜2026-10-05｜curl 200，22,704 bytes，解壓 docx 讀 word/document.xml；檔案屬性建立日期 2020-09-03，但目前仍由上述支援頁連結。
- Copilot in Word FAQ：品質預期以英文最高；建議來自 AI，可能出錯、誤解事實或產生不正確結果，接受前要審閱；Copilot 寫得流暢且合乎文法，但內容可能不正確，它無法理解意思或評估正確性｜https://support.microsoft.com/en-us/word/frequently-asked-questions-about-copilot-in-word｜2026-10-05｜curl 200，讀全文。
- Google 文件拼字和文法：修訂建議功能支援英文、西班牙文、法文、德文、葡萄牙文和義大利文；可「新增至字典」｜https://support.google.com/docs/answer/57859?hl=zh-Hant｜2026-10-05｜curl 200；頁面註明可能含 AI 翻譯內容，另抓 hl=en 版交叉確認同一份語言清單。
- Google 文件建議模式：可在不變更原始文字的情況下提出修訂建議，擁有者核准後取代原文；右上角「編輯」圖示 → 下拉選「建議」；新增的內容以新顏色顯示、刪除的以橫線劃除｜https://support.google.com/docs/answer/6033474?hl=zh-Hant｜2026-10-05｜curl 200，讀全文。
- Word 追蹤修訂：在 [檢閱]（同頁其他段落寫 [校閱]）索引標籤選取 [追蹤 > 追蹤修訂]；刪除以刪除線、新增以底線標示，不同作者不同色彩；可逐條接受或拒絕｜https://support.microsoft.com/zh-tw/word/training/track-changes-in-word｜2026-10-05｜curl 200，讀全文。正文用「校閱」索引標籤（台灣版 Office 的名稱，法律黑線頁也寫「校閱」）。
- Word 法律黑線比較：適用 Microsoft 365 Word、Word 2024、Word 2021 與其他 Windows 版 Word；[校閱] 索引標籤 [比較] 群組 → [比較] → 比較兩個版本的文件（法律黑線）；比較的文件不會變更，結果顯示在第三個新文件；可選擇在字元層級或文字層級顯示變更｜https://support.microsoft.com/zh-tw/word/compare-document-differences-using-the-legal-blackline-option｜2026-10-05｜curl 200，讀全文。（另一篇「比較及合併文件的兩個版本」只標示適用 Mac 版 Word 2019，未採用。）
- （查過未用）Word 自訂字典：右鍵 → 新增到字典；檔案 → 選項 → 校訂 → 自訂字典｜https://support.microsoft.com/zh-tw/word/add-or-edit-words-in-a-spell-check-dictionary｜2026-10-05｜curl 200。
- （查過未用）Word 的 Range.TCSCConverter（繁簡轉換，含 CommonTerms 參數）｜https://learn.microsoft.com/en-us/office/vba/api/word.range.tcscconverter｜2026-10-05｜curl 200；參數表沒有寫 CommonTerms 的說明，也找不到 support.microsoft.com 的中文轉換說明頁，所以正文不寫 Word 的繁簡轉換功能。

## 站內連結

- immersive-translate-guide、ai-prompt-library-personal、ai-tools-choose-by-task：三篇都存在於 apps/api/app/guides/content/，kind 皆為 life，有 zh-TW。

## 圖與檢查

- diagram-1.svg：四欄流程（字形轉換、詞彙轉換、AI 校稿、人工終校），由 `_tools/ai-proofreading-terminology/make_diagram.py` 產生。圖上唯一的阿拉伯數字是頁尾「2026」，兩張表格的 caption 都寫「查證於 2026 年 10 月」。圖上例字（发／發／髮、发展／頭髮、软件／軟件／軟體、再／在、以經／已經、后來／後來、數據／資料）正文都有。
- hero.svg：左邊文件加放大鏡，右邊一張卡片分出打勾與打叉兩張卡片，一行字「字對了，詞也要對」（52px）；由 `make_hero.py` 產生。沒有 logo、臉孔、遞增長條。第一版用筆畫拼成的抽象字塊渲染後看起來像「木」「米」兩個真字，改成文字線條卡片。
- 兩張圖都用 render_svg 渲染成 PNG 打開看過（第一版圖解第二欄提醒框的引號太靠邊，改成不加引號；第三、四欄下半部空白，往下挪）。
- 2026-10-05：pack_cli ingest --dry-run 通過；intake_check RESULT PASS（0 failures），body_length=2566，唯一 WARN 是自繪 hero 沒有 Commons 標題可查重；lint_document 與 check_svg 沒有任何問題。

## 查核第一輪（2026-10-05，獨立查核者）

全部來源重新抓取（`_tools/ai-proofreading-terminology/v1/`），github.com 仍回 403，改以 raw.githubusercontent.com（200）讀內容，並用 WebFetch 確認 github.com 的 repo 頁、STCharacters.txt、TWPhrases.txt 頁面可開（STPhrases.txt 約 1 MB，GitHub 檔案頁只顯示 Raw 連結）。修改：
- 摘要「資料不是數據」太絕對（修訂本「數據」指調查或實驗得到的數值，台灣照用），改成「台灣寫軟體、列印，大陸寫軟件、打印」。
- 兩岸表「品質」列：簡編本附錄的大陸語詞是「品質／質量」，原稿只寫「質量」；注意欄改為「大陸兩種都用；「質量」另有別的意思」。
- 兩岸表 caption 加上 OpenCC 台灣詞庫（「軟件」「視訊」兩格的依據是 TWPhrases.txt）。
- 「質量」釋義：修訂本寫「物體內所含物質的量」，沒有「在物理上」，刪去。
- Editor：「再／在」在指南裡屬「易混淆錯字」，不是「形音相近錯字」；登入條件是「Microsoft 365 帳號」，不是泛稱的微軟帳號。
- OpenCC：`--ambiguities` 只有原生 CLI 支援（README：Python 與 npm CLI 不支援），補上；「轉換工具不是逐字替換」改成只講 OpenCC。
- 法律黑線比較：結果「根據預設」顯示在新文件，可改成顯示在原始或修訂文件，補「預設」。
- 「AI 不會自動知道你要台灣用語」沒有來源，軟化為「不一定知道」。
- 確認無誤：Unihan 七字的 kTraditionalVariant、STCharacters／STPhrases／TWPhrases／TWVariants 各條、README 的 s2t／s2tw／s2twp 與 --inspect「數據庫→資料庫」、DESIGN_PRINCIPLES「默認模式為 s2t」、Copilot FAQ 三句、Google 拼字語言清單與建議模式步驟、Word 追蹤修訂步驟（頁面為機器翻譯，「檢閱」「校閱」混用）、標點手冊引號、樂詞網。Editor 語言表 Chinese (Traditional) 仍為 ◌／●／◌；guidance docx 建立日 2020-09-03，仍由支援頁連結。

## 查核第二輪（2026-10-05，另一位查核者）

全部來源重新抓取（`_tools/ai-proofreading-terminology/v2/`），簡編本附錄抓 page=1..7。github.com 仍回 403，改讀 raw.githubusercontent.com（200），並用 WebFetch 確認 github.com 的 repo 頁與 TWPhrases.txt 頁可以打開。詳細紀錄在 verify-2.md。
- 《重編國語辭典修訂本》「雇主」：僱用他人工作並支付薪資的人；也作「僱主」（只有一個義項）｜https://dict.revised.moe.edu.tw/dictView.jsp?ID=71572｜2026-10-05｜curl 200。風格表的例子從「公布或公佈」改成「雇主或僱主」，因為修訂本「公布」的「也作公佈」只掛在第 2 義，「把法律或命令公告周知」那一義只收「公布」。sources 中 ID=75132 換成 ID=71572。
- Editor 語言表：頁面注記寫 Japanese writing refinements (**) 桌面版還不能用，而 Japanese 的 refinements 格是「● **」，所以 ● 表示有提供。Chinese (Traditional) 仍是 ◌／●／◌。
- OpenCC 的 STPhrases 與 TWPhrases 都沒有质量、土豆的詞組條目，正文因此改成「OpenCC 的台灣詞庫不會替換」，不再泛指所有轉換工具。

## 跨篇核對（2026-10-05）

- hero 重畫：原圖的主體是「白色文件加壓在上面的藍色放大鏡」，和上一批 ai-concept-stocks-explained 的 hero 主體相同（上一批跨篇核對也因為同一個母題改過一張）。改成文件上的校對記號：一段被紅線劃掉、上方有綠色替換標記，另一段有紅色波浪底線，一行末端的橘色標記拉出藍色虛線到右邊的候選分岔卡片；右半邊與字卡不變。同步改了 `<desc>` 與 pack.json 的 hero alt。腳本：`_tools/_crosscheck/edit_hero_proofreading.py`，原檔備份在 `_tools/_crosscheck/backup/`。渲染後看過：沒有溢出、沒有重疊。
- 在風格表之後加了連到 ai-official-documents-taiwan 的 article inline（公文的數字、紀年、標點與稱謂另有手冊規定）。
- Copilot in Word FAQ 今日重讀：「can be inaccurate」「can't understand meaning or evaluate accuracy」「quality is expected to be highest in English」，與 ai-proposal-writing 的寫法一致。
- 重跑 dry-run 與 intake_check：0 FAIL，body_length=2598。
