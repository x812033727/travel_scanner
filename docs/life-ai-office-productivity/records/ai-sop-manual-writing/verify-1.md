# ai-sop-manual-writing 查核第一輪（2026-10-05）

每個來源今天都用 curl -sSL 和編輯部 UA 重新抓取：HTTP 200、內容是真的，註解已刪除。原始檔在 /home/user/batch-ai-office/_tools/ai-sop-manual-writing/v1/pages/。
格式：主張｜判定｜來源網址

## 錄音與錄畫面
- Word 的轉譯（Transcribe）可以直接錄音或上傳音訊｜ok｜https://support.microsoft.com/zh-tw/word/transcribe-your-recordings
- 功能入口：原本只寫「在『聽寫』下拉選單裡」，現在寫「常用」索引標籤的「聽寫」下拉選單（中文頁上傳路徑是「[常用]> [聽寫] 下拉式清單 >[轉譯]」）｜fixed｜https://support.microsoft.com/zh-tw/word/transcribe-your-recordings
- 上傳格式 .wav、.mp4、.m4a、.mp3｜ok｜https://support.microsoft.com/en-us/word/transcribe-your-recordings
- 逐字稿依講者分段、帶時間戳記，點時間戳記可以回放該段｜ok｜https://support.microsoft.com/en-us/word/transcribe-your-recordings
- 語言清單有台灣華語（中文 (台灣華語) / Chinese (Taiwanese Mandarin)）｜ok｜https://support.microsoft.com/zh-tw/word/transcribe-your-recordings
- Microsoft 365 訂閱使用者每月最多可轉譯 300 分鐘的上傳音訊｜ok｜https://support.microsoft.com/zh-tw/word/transcribe-your-recordings
- 錄音存在 OneDrive（「轉譯的檔案」資料夾）｜ok｜https://support.microsoft.com/en-us/word/transcribe-your-recordings
- 適用範圍：原本寫「適用版本以微軟說明為準」，現在寫「Windows 版與網頁版 Word 都有，帳號類型限制以微軟說明為準」（Windows 版那一分頁的注意事項限定商業租用戶，網頁版分頁另有操作步驟）｜fixed｜https://support.microsoft.com/en-us/word/transcribe-your-recordings
- Mac：Shift + Command + 5 打開「截圖」App，可以錄整個螢幕或所選部分｜ok｜https://support.apple.com/zh-tw/102618
- Mac：在「選項」選一個麥克風，就能錄下說話的聲音｜ok｜https://support.apple.com/zh-tw/102618
- Mac：選「顯示滑鼠點按」後，每次點按時指標周圍會顯示黑色圓圈｜ok｜https://support.apple.com/zh-tw/102618
- Windows 用 Windows 標誌鍵 + Shift + R 錄影片剪取，選好範圍後按「開始」。這只出現在 Windows 11 分頁，正文改成「Windows 11 錄畫面」｜fixed｜https://support.microsoft.com/en-us/windows/apps/use-snipping-tool-to-capture-screenshots

## 寫步驟（風格指南）
- 微軟與 Google 都要求用編號清單、一步一個動作、先說位置再說動作、以祈使動詞開頭｜ok｜https://learn.microsoft.com/en-us/style-guide/procedures-instructions/writing-step-by-step-instructions ; https://developers.google.com/style/procedures
- 「結果寫在同一步」原本算成兩份指南共同的要求，其實只有 Google 明文寫出（Keep the result in the same paragraph as the action），現在只歸給 Google｜fixed｜https://developers.google.com/style/procedures
- 微軟提醒要寫出完成程序的動作（例如選取「確定」或「套用」）｜ok｜https://learn.microsoft.com/en-us/style-guide/procedures-instructions/writing-step-by-step-instructions
- 同一處的連續選單可以用「>」合成一步｜ok｜https://learn.microsoft.com/en-us/style-guide/procedures-instructions/writing-step-by-step-instructions ; https://developers.google.com/style/procedures
- 選擇性步驟在開頭標「選擇性：」（Google 寫 Optional:）｜ok｜https://developers.google.com/style/procedures
- 重複的程序改用參照，不重寫｜ok｜https://developers.google.com/style/procedures
- AI 可能寫出看似正確其實錯誤的內容。說明頁把這歸為前沿生成式 AI 模型共有的限制，所以泛指 AI 有根據｜ok｜https://support.claude.com/en/articles/8525154-claude-is-providing-incorrect-or-misleading-responses-what-s-going-on

## 截圖
- 截圖要節制，介面元素難找時才放；裁切到相關範圍，介面其他部分改版時比較不必重截｜ok｜https://developers.google.com/style/images ; https://developers.google.com/style/procedures
- 文字、程式碼或終端機輸出不要做成圖片｜ok｜https://developers.google.com/style/images
- 截圖不得含個人可識別資訊；要用 100% 不透明的純色色塊蓋住，不用模糊或馬賽克，因為可能被還原｜ok｜https://developers.google.com/style/images
- 輸出成 PDF、TIFF 這類有圖層的格式時，先合併圖層｜ok｜https://developers.google.com/style/images
- Mac 用 Shift + Command + 4 拖選部分螢幕｜ok｜https://support.apple.com/zh-tw/102646
- Windows 用 Windows 標誌鍵 + Shift + S 截圖（Windows 10 與 11 都有）｜ok｜https://support.microsoft.com/zh-tw/windows/apps/use-snipping-tool-to-capture-screenshots
- 「文字動作」與「快速修訂」可遮電子郵件與電話號碼，辨識在裝置本機進行。這只出現在 Windows 11 分頁，正文改成「Windows 11 的剪取工具」｜fixed｜https://support.microsoft.com/en-us/windows/apps/use-snipping-tool-to-capture-screenshots

## EPA QA/G-6（2007 年 4 月版，EPA/600/B-07/001，取代 2001 年 3 月版 EPA/240/B-01-004）
- 來源版本：入口頁標題寫 2001，連結的 PDF 是 2007 年 4 月版，sources 的標題寫 2007｜ok｜https://www.epa.gov/sites/default/files/2015-06/documents/g6-final.pdf
- SOP 應由實際執行工作的人撰寫（2.1）｜ok｜https://www.epa.gov/sites/default/files/2015-06/documents/g6-final.pdf
- 經驗有限、但有基本理解的人能在無人監督下重現程序（2.1）。原本把 unsupervised 譯成「沒人指導」，現在改成「無人監督」｜fixed｜https://www.epa.gov/sites/default/files/2015-06/documents/g6-final.pdf
- 定稿前由撰寫者以外的人實際試做（2.2）｜ok｜https://www.epa.gov/sites/default/files/2015-06/documents/g6-final.pdf
- 程序變更時更新並重新核准；定期系統性複審，例如每 1 到 2 年；不再執行的 SOP 撤下封存（2.3）｜ok｜https://www.epa.gov/sites/default/files/2015-06/documents/g6-final.pdf
- 封面列標題、SOP 編號、發行或修訂日期、適用單位，以及撰寫與核准者的簽名（3.1）｜ok｜https://www.epa.gov/sites/default/files/2015-06/documents/g6-final.pdf
- 每頁的文件控制標註：原本漏了編號，現在寫「短標題與編號、版次、日期、第幾頁共幾頁」（2.5）｜fixed｜https://www.epa.gov/sites/default/files/2015-06/documents/g6-final.pdf
- 修訂紀錄欄位：版次、日期、修改人、改了什麼（附錄範例 Revision Record）｜ok｜https://www.epa.gov/sites/default/files/2015-06/documents/g6-final.pdf

## Claude Skills
- 技能是裝著指示、腳本與資源的資料夾，用得上時才載入｜ok｜https://support.claude.com/en/articles/12512176-what-are-skills
- 可用方案：原本寫「Free 到 Enterprise 各方案」，現在照頁面明列 Free、Pro、Max、Team、Enterprise｜fixed｜https://support.claude.com/en/articles/12512176-what-are-skills
- 需要開啟程式碼執行｜ok｜https://support.claude.com/en/articles/12512176-what-are-skills

## 法規
- 個資法第 2 條第 1 款：姓名、出生年月日、身分證統一編號、聯絡方式、財務情況，以及其他得以直接或間接識別個人的資料｜ok｜https://law.moj.gov.tw/LawClass/LawSingle.aspx?pcode=I0050021&flno=2
- 營業秘密法第 2 條：方法、技術、製程等可用於生產、銷售或經營的資訊；要件之一是所有人已採取合理的保密措施｜ok｜https://law.moj.gov.tw/LawClass/LawSingle.aspx?pcode=J0080028&flno=2

## 其他
- 編輯建議，沒有出處，也不是事實主張：兩輪試做、表格裡的「兩成」門檻（表內已註明由負責人訂）、提示詞範本、開錄前關通知｜ok（標成建議）｜-
- 表格 caption「整理於 2026 年 10 月」｜ok｜-
- diagram-1.svg 上的數字只有步驟編號 01–07 與頁尾 2026，沒有事實數字；看過 PNG，版面正常｜ok｜-
- hero.svg 只有一行字「從口述到可交接的步驟」，52 px；沒有 logo、人臉，也沒有遞增圖形｜ok｜-
- 站內連結 ai-note-taking-workflow、meeting-notes-action-template、claude-skills-explained：都在指派清單裡，kind 都是 life｜ok｜https://mokaair.com/zh-TW/life/ai-note-taking-workflow ; https://mokaair.com/zh-TW/life/meeting-notes-action-template ; https://mokaair.com/zh-TW/life/claude-skills-explained
- sources 12 筆：今天都是 HTTP 200，checked_on 都是 2026-10-05；剪取工具與 Word 轉譯兩筆的標題配合修正一併調整｜ok｜（見上）
