# ai-sop-manual-writing 查核第二輪（2026-10-05）

所有來源今天重新抓過，用 curl -sSL 加編輯部 UA，註解先刪掉，PDF 用 pdftotext 讀。原始檔放在 /home/user/batch-ai-office/_tools/ai-sop-manual-writing/v2/pages/。
15 個網址（12 筆 sources，加上 EPA 入口頁和兩個 Microsoft 頁面的 en-us 版）都回 HTTP 200。營業秘密法頁第一次回的是 HTTP 200 的錯誤殼頁（「This page can't be displayed」），重抓一次就拿到條文全文。這個殼頁不算來源。
格式：主張｜判定｜來源網址

## A1. 第一輪改過的事實（逐條重查）
- Win+Shift+R 錄影片剪取和「開始」按鈕只出現在 Windows 11 分頁。Windows 10 分頁只列 Win+Shift+S、PrtSc 和開始選單。正文寫「Windows 11 錄畫面」｜ok｜https://support.microsoft.com/en-us/windows/apps/use-snipping-tool-to-capture-screenshots
- 「文字動作」與「快速修訂」可以遮電子郵件和電話號碼，辨識都在裝置本機進行。這只出現在 Windows 11 分頁，正文寫「Windows 11 的剪取工具」｜ok｜同上，zh-tw 版對照過
- 「Keep the result in the same paragraph as the action」只有 Google 寫。微軟的頁面只在範例裡把結果寫進同一步，正文把這條只歸給 Google｜ok｜https://developers.google.com/style/procedures ; https://learn.microsoft.com/en-us/style-guide/procedures-instructions/writing-step-by-step-instructions
- 中文頁上傳路徑寫「[常用]> [聽寫] 下拉式清單 >[轉譯]」（錄音路徑寫「[首頁>]」），正文寫「常用」索引標籤｜ok｜https://support.microsoft.com/zh-tw/word/transcribe-your-recordings
- 適用範圍：頁面「套用到」列出 Windows 版 Word、Word 網頁版、OneNote 三個分頁。「僅適用於商業租用戶中的 Windows 版」那則注意事項放在 Windows 分頁下，網頁版分頁有自己的步驟（Edge 或 Chrome）。正文寫「Windows 版與網頁版 Word 都有這項功能，帳號類型的限制以微軟說明為準」｜ok｜https://support.microsoft.com/en-us/word/transcribe-your-recordings
- EPA 2.1：「...can successfully reproduce the procedure when unsupervised」，正文寫「無人監督」｜ok｜https://www.epa.gov/sites/default/files/2015-06/documents/g6-final.pdf
- EPA 2.5：每頁的控制標註是 Short Title/ID #、Rev. #、Date、Page x of，正文寫「短標題與編號、版次、日期與頁數」｜ok｜同上
- Claude Skills：「Skills are available for users on Free, Pro, Max, Team, and Enterprise plans. This feature requires code execution to be enabled.」｜ok｜https://support.claude.com/en/articles/12512176-what-are-skills

## A2. 第一輪無法確認或留下的事項
- 字數：第一輪交件時 2,654，超過目標上限 2,600。本輪補了必要的日期、條號和人工核對句，又刪了重複的導言和「定稿前」，最後是 2,681，仍在 1,800–3,000 之內。多出來的字是合規需要的內容，不是灌水，所以沒有為了湊目標硬刪實質內容｜接受
- 幻覺泛指 AI：說明頁寫「a byproduct of some of the current limitations of frontier Generative AI models, like Claude」｜ok｜https://support.claude.com/en/articles/8525154-claude-is-providing-incorrect-or-misleading-responses-what-s-going-on
- EPA 版本：PDF 是 EPA/600/B-07/001，2007 年 4 月版。前言寫「It replaces EPA's March 2001's ... EPA/240/B-01-004」｜ok｜https://www.epa.gov/sites/default/files/2015-06/documents/g6-final.pdf
- Word 轉譯的帳號類型限制：頁面沒有說明個人版或家用版 Microsoft 365 在 Windows 上算不算「商業租用戶」。正文交給微軟的說明頁，不替讀者判斷｜保留
- intake 的「no hero title found」警告：自繪 SVG 的 hero 本來就會出現這個警告｜ok
- 站內連結：三個都在指派清單裡，repo 內容的 kind 都是 life，正式站今天都回 200｜ok

## A3. 抽查 verify-1.md 其餘主張（取第 2、5、8…44 列，共 15 列）
- 2 功能入口「常用 > 聽寫 > 轉譯」｜ok（見 A1）
- 5 語言清單有「中文 (台灣華語)」和「Chinese (Taiwanese Mandarin)」｜ok｜zh-tw 與 en-us 轉譯頁
- 8 適用範圍｜ok（見 A1）
- 11 Mac「選項」裡的「顯示滑鼠點按」：每次按一下，指標周圍會出現黑色圓圈｜ok｜https://support.apple.com/zh-tw/102618
- 14 結果寫在同一步只歸給 Google｜ok（見 A1）
- 17 選擇性步驟開頭寫「Optional:」，頁面也把「(Optional)」列為不建議的寫法｜ok｜https://developers.google.com/style/procedures
- 20 截圖要節制（「For screenshots, be discreet」）；要裁切，裁切後介面其他部分改版時截圖比較不必重做；介面元素不好找時再放截圖｜ok｜https://developers.google.com/style/images ; https://developers.google.com/style/procedures
- 23 輸出成 PDF、TIFF 這類有圖層的格式時，先合併圖層（flatten）｜ok｜https://developers.google.com/style/images
- 26 快速修訂只在 Windows 11 有｜ok（見 A1）
- 29 EPA 2.1「無人監督」｜ok（見 A1）
- 32 EPA 3.1 封面要有：標題、SOP 編號、發行或修訂日期、適用單位、撰寫與核准者的簽名和日期｜ok｜EPA PDF
- 35 技能是「folders of instructions, scripts, and resources that Claude loads dynamically」｜ok｜Claude Skills 說明頁
- 38 個資法第 2 條第 1 款：條文和正文列出的項目一致（國民身分證統一編號、聯絡方式、財務情況，以及「其他得以直接或間接方式識別該個人之資料」）。頁首註明部分條文尚未施行，但第 2 條不在名單上｜ok｜https://law.moj.gov.tw/LawClass/LawSingle.aspx?pcode=I0050021&flno=2
- 41 表格 caption「整理於 2026 年 10 月」｜ok
- 44 站內連結｜ok（見 A2）

順便也重查了：營業秘密法第 2 條的三項要件，第三項是「所有人已採取合理之保密措施者」｜ok。Mac 的 Shift+Command+4 和 Shift+Command+5（「截圖」App）｜ok。微軟風格指南寫了「Multiple-step procedures: Use a numbered list」，也寫了「Most of the time, include actions that complete a procedure」｜ok。

## 修改了什麼、為什麼（pack.json）
1. 導言第一段原本是兩句：先鋪陳，再給答案。依 life-ai-series-brief §4，第一段要用一句話講清楚回答什麼、結論是什麼，所以改寫成一句完整的做法（SOP 第一次出現時仍附中文全名）。
2. 導言第二段原本重複第一段的流程清單，改成說明讀者做完會得到什麼，符合 §4 要求的「第二段講會帶讀者做到什麼」。
3. Word 轉譯每月 300 分鐘前面加「截至 2026 年 10 月」，Claude Skills 的方案清單前面也加「截至 2026 年 10 月」。批次規則要求寫出 AI 工具的方案和限制時附上日期，原文沒有附。
4. Skills 段補上「結果仍由負責人核對」。原文叫讀者把定稿的流程交給 AI 去做，旁邊卻沒有人工核對的步驟。
5. 快速修訂那句補上「遮完仍要逐張看過」。原文叫讀者使用自動遮蔽的結果，旁邊沒有人工檢查。
6. callout 補上條號，寫成「個人資料保護法第 2 條」和「營業秘密法第 2 條」，法規引用要附條號。
7. 文字修整：同一段出現兩次「另外」，第二個改成「也」。試做那段原本以「定稿前要試做。」開頭，後面一句又寫「定稿前」，所以把開頭刪掉，改成「試做的標準可以借用 EPA 指引：……；指引也建議定稿前由撰寫者以外的人實際試做」，把主詞交代清楚。
這次沒有改任何數字或事實。所有修改都是合規和寫法上的修正，事實修正是 0 筆。

## 合規審查（B）
- 實測：全文沒有「實測」，也沒有分數或測試結果。提示詞範本標成「提示詞範本」，沒有說它有什麼效果。表格裡的改寫例子 caption 寫明「示意」，「兩成」門檻也註明由負責人訂。
- AI 工具的功能都照廠商說明頁寫，日期見修改 3：Word 轉譯（位置、格式、上限、OneDrive、語言）、剪取工具、Mac「截圖」App、Claude Skills（方案、要開程式碼執行）。正文沒有寫任何說明頁上沒有的功能，例如 Windows 錄影片剪取能不能收麥克風聲音，這點正文刻意不寫。
- 法規：個資法第 2 條第 1 款和營業秘密法第 2 條，都是今天從全國法規資料庫讀到的條文，正文改寫後沒有偏離原意，現在也附上了條號。內容只說流程「可能」是營業秘密，不替讀者做個案法律判斷。
- 人工核對：讀者會用到的每一種 AI 或自動產出，旁邊都有人工核對的步驟：逐字稿（點時間戳記回放核對）、AI 草稿（對照錄影逐步核對）、AI 挑出的模糊字眼（答案由人提供）、快速修訂（逐張看過，本輪補上）、Skills 照做的結果（負責人核對，本輪補上）。
- 工具推薦：沒有說哪一個工具比另一個好。Mac 和 Windows 的寫法並列；Word 轉譯只當成一種做法的例子；Claude Skills 只寫成一個可選項，最後交由公司的 AI 使用規範決定。
- 個資與機密：開錄前改用測試帳號和假資料，逐字稿交給 AI 前先換成代號，截圖用不透明色塊遮，SOP 只寫角色、不寫帳號密碼。

## 讀者優先與寫法（C）
- 正文出現「本文」「這篇」0 次。正文沒有「官方」「官網」「查證」「撰稿」「本批」「我們」，也沒有驚嘆號和「總結來說」。
- 句子裡沒有敘述出處。「EPA 指引建議」「Google 的指南要求」這種寫法是告訴讀者這條規則是誰定的，不是在講查證過程，所以保留。
- 外文詞第一次出現都附了中文：SOP、EPA、Word、Transcribe、Microsoft 365、OneDrive、Skills、Claude。Free、Pro 這幾個方案名前面有「免費的／付費的」。
- 用的是台灣用語：軟體、資料、影片、介面、程式碼。掃過全文，沒有視頻、信息、用戶、軟件、默認、屏幕這類詞。
- 字數 2,681：在 1,800–3,000 的範圍內，比 2,200–2,600 的目標多 81 字（原因見 A2）。
- 圖：在暫存區重新把 hero.svg 和 diagram-1.svg 轉成 PNG 看過。流程圖的標籤沒有壓到線，文字沒有溢出框外，「試做卡住」的回頭虛線有標示。英文副標和 © 頁尾照 §7 的規定寫。hero 只有一行字，沒有 logo、人臉，也沒有遞增的圖形。

## 機器檢查
- pack_cli ingest --dry-run：exit 0（「dry run: nothing written」）。
- intake_check：結果是 PASS，0 筆失敗，body_length=2681，本文／這篇 0 次，sources 12 筆，checked_on 都是 2026-10-05。唯一的警告是自繪 hero 本來就會有的「no hero title」。
