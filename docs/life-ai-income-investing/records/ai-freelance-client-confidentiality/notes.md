# ai-freelance-client-confidentiality 查證記錄

格式：主張｜來源網址｜查證日｜怎麼讀到的

讀法說明：
- 「直接」= curl -sSL，UA 為 Mokaair-editorial/1.0，HTTP 200，去掉 HTML 註解後讀全文。
- 「讀取代理」= 查核第一輪（2026-10-05）改用的讀法。help.openai.com 對 curl 與 WebFetch 仍回 403（Cloudflare），web.archive.org 從本環境連線仍被重設。改用 r.jina.ai 即時讀取原頁（`https://r.jina.ai/<原網址>`，HTTP 200，回傳的是該頁今天的全文與 Updated 日期，不是摘要）。存檔在 _tools/ai-freelance-client-confidentiality/v1/jina_*.txt。撰稿時的「搜尋摘要」各條都已用這個讀法重讀並訂正，見下。sources 仍寫原始官方網址。

## ChatGPT（OpenAI）

個人服務（such as ChatGPT and Codex）可能用內容訓練模型；關閉方式為 Settings > Data controls 關掉 Improve the model for everyone，或在 Privacy Portal 選 Do not train on my content｜https://help.openai.com/en/articles/5722486-how-your-data-is-used-to-improve-model-performance｜2026-10-05｜讀取代理（Updated: 6 days ago）
個人方案名稱 Free、Go、Plus、Pro（「Signed-in ChatGPT Free, Go, Plus, and Pro users」）；路徑 設定 → Data controls → Improve the model for everyone｜https://help.openai.com/en/articles/7730893-data-controls-in-chatgpt｜2026-10-05｜讀取代理（Updated: 6 days ago）。查核第一輪把表格的「Free、Plus、Pro」改成「Free、Go、Plus、Pro」
中文介面官方用語：「資料控管」「為所有人改善模型」「臨時交談」「不要使用我的內容進行訓練」｜https://help.openai.com/zh-hant/articles/7730893-data-controls-in-chatgpt｜2026-10-05｜讀取代理。撰稿用的「資料控制」「為所有人改進模型」「暫時對話」是自譯，已改成官方用語
即使已退出訓練，按讚或倒讚時，該回饋相關的整段對話可能被用於訓練｜https://help.openai.com/en/articles/5722486-how-your-data-is-used-to-improve-model-performance｜2026-10-05｜讀取代理（FAQ 段，原文 "the entire conversation associated with that feedback may be used to improve our models, even if you've opted out"）
ChatGPT Business、Enterprise、Edu 與 API 預設不以輸入或輸出訓練模型｜https://help.openai.com/en/articles/5722486-how-your-data-is-used-to-improve-model-performance｜2026-10-05｜讀取代理（Business services and managed workspaces 段）。查核第一輪在表格補上 Edu
ChatGPT Business 工作區資料預設排除於訓練之外｜https://help.openai.com/en/articles/8798634-managing-data-sharing-and-privacy-in-chatgpt-business｜2026-10-05｜讀取代理（"Business data is excluded from training by default"）。sources 已滿 20 筆，這頁改由 7730893（同樣寫明受管理工作區預設不訓練）取代
臨時交談保持臨時狀態時不用於改進模型；OpenAI 可能為安全目的保留副本最多 30 天；存成一般對話後改依帳號的模型改善設定｜https://help.openai.com/en/articles/8914046-temporary-chat-faq｜2026-10-05｜讀取代理（Updated: 15 days ago）。「存成一般對話後改依帳號設定」是查核第一輪補上的
API：自 2023 年 3 月 1 日起送進 API 的資料不用於訓練，除非主動選擇分享（表中寫「API 要主動選擇分享才會用」）｜https://developers.openai.com/api/docs/guides/your-data｜2026-10-05｜直接（頁名 Data controls in the OpenAI platform）
API：濫用監控紀錄預設最多保留 30 天（法律要求或防止傷害時可更長）｜https://developers.openai.com/api/docs/guides/your-data｜2026-10-05｜直接

## Claude（Anthropic）

個人方案（Free、Pro、Max）：你選擇允許、或被安全審查標記、或另行加入訓練（如 Trusted Tester）時才用於改進模型｜https://privacy.claude.com/en/articles/10023580-is-my-data-used-for-model-training｜2026-10-05｜直接（頁面日期 March 16, 2026）
無痕對話（Incognito chats）即使開啟模型改進也不用於改進 Claude｜https://privacy.claude.com/en/articles/10023580-is-my-data-used-for-model-training｜2026-10-05｜直接
關閉路徑：Settings → Privacy → Help improve our AI models 開關（桌面與手機相同）｜https://privacy.claude.com/en/articles/12109829-how-do-i-change-my-model-improvement-privacy-settings｜2026-10-05｜直接（頁面日期 August 3, 2026）
允許訓練時，去識別化資料在訓練流程中最長保留 5 年；刪除的對話 30 天內從後端刪除；回饋資料保留 5 年｜https://privacy.claude.com/en/articles/10023548-how-long-do-you-store-my-data｜2026-10-05｜直接（頁面日期 July 1, 2026）
商用產品（Claude for Work、Anthropic API、Claude Gov 等）預設不以輸入或輸出訓練模型；回報回饋或選擇允許時可能用於訓練｜https://privacy.claude.com/en/articles/7996868-is-my-data-used-for-model-training｜2026-10-05｜直接（頁面日期 August 18, 2026）
按讚倒讚回饋：整段相關對話在後端保存最長 5 年；Team 或 Enterprise 的 Primary Owner 或 Owner 可用 Rate chats 設定關掉回饋按鈕｜https://privacy.claude.com/en/articles/7996868-is-my-data-used-for-model-training｜2026-10-05｜直接
API 使用者的輸入與輸出在收到或產生後 30 天內從後端自動刪除（Files API、零資料保留協議、違反使用政策、法律要求等例外）｜https://privacy.claude.com/en/articles/7996866-how-long-do-you-store-my-organization-s-data｜2026-10-05｜直接（頁面日期 July 1, 2026）

## Gemini（Google）

Keep Activity 開著時，Google 用活動提供、開發與改進服務（包括訓練生成式 AI 模型），部分對話由人工審查｜https://support.google.com/gemini/answer/13594961｜2026-10-05｜直接（Gemini Apps Privacy Hub，Last updated September 24, 2026）
「不要輸入不想讓審查人員看到、或不想讓 Google 用來改進服務的機密資訊」｜https://support.google.com/gemini/answer/13594961｜2026-10-05｜直接（Privacy Notice 段，Last updated June 29, 2026）
關掉 Keep Activity 或使用暫時對話：對話仍保留 72 小時；暫時對話不用於訓練；Keep Activity 關閉且不送回饋時，未來對話不用於改進模型｜https://support.google.com/gemini/answer/13594961｜2026-10-05｜直接
經服務供應商審查的資料與帳號脫鉤，保留 3 年；刪除活動不會刪掉已審查的對話｜https://support.google.com/gemini/answer/13594961｜2026-10-05｜直接
Keep Activity 關閉時送出回饋：經審查的回饋、相關對話與資料最長保留 3 年｜https://support.google.com/gemini/answer/13594961｜2026-10-05｜直接
工作或學校帳號可能適用不同的資料處理條款（指向 Workspace Privacy Hub）｜https://support.google.com/gemini/answer/13594961｜2026-10-05｜直接
Workspace：內容未經許可不經人工審查，也不用於網域外的生成式 AI 模型訓練｜https://knowledge.workspace.google.com/admin/generative-ai/generative-ai-in-google-workspace-privacy-hub｜2026-10-05｜直接（Last updated August 14, 2026；頁尾 2026-10-01 UTC）

## 合約與著作權

智慧財產局「出資聘人完成著作契約（著作財產權歸出資人）」範本：保密約定，乙方首次公開發表前甲方不得公開內容，違反時最高相當於報酬 2 倍之懲罰性違約金｜https://www.tipo.gov.tw/tw/copyright/719-19274.html｜2026-10-05｜直接下載頁上的 DOCX（/wSite/public/Attachment/006/f1746517130120.docx），解壓讀 document.xml
同範本：保證本著作確為獨立創作、無抄襲等侵權，違反時自行承擔民刑事責任並賠償損害｜https://www.tipo.gov.tw/tw/copyright/719-19274.html｜2026-10-05｜同上
著作權法第 12 條：出資聘人完成之著作以受聘人為著作人；著作財產權依約定，未約定歸受聘人；出資人得利用｜https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=J0070017｜2026-10-05｜直接（修正日期民國 111 年 6 月 15 日）
著作權法第 36 條第 3 項：讓與範圍約定不明部分推定為未讓與；第 37 條第 1 項：授權約定不明部分推定為未授權｜https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=J0070017｜2026-10-05｜直接
營業秘密法第 2 條第 3 款：所有人已採取合理之保密措施｜https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=J0080028｜2026-10-05｜直接（修正日期民國 109 年 1 月 15 日）
智慧財產局電子郵件1111031：以 AI 為工具且有人類實際創意投入者可受保護；AI 獨立創作原則上無法享有著作權｜https://www.tipo.gov.tw/tw/copyright/692-16813.html｜2026-10-05｜直接（發布 111-10-31，更新 114-04-28）
智慧財產局電子郵件1150828c：生成式 AI 產製、無受保護人類創作內容的圖片，是否及如何標示製作者與來源，著作權法無規範，可自行決定；第三方圖片是否標示來源，建議於授權契約中約定｜https://www.tipo.gov.tw/tw/copyright/692-94326.html｜2026-10-05｜直接（發布 115-08-28，更新 115-09-10）
人工智慧基本法第 4 條第 5 款：透明與可解釋，人工智慧之產出應做適當資訊揭露或標記；條文主詞為「政府推動人工智慧之研發與應用」｜https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=H0160093｜2026-10-05｜直接（公布日期民國 115 年 1 月 14 日）

## 個資法

第 2 條第 1 款個人資料定義（姓名、出生年月日、聯絡方式、財務情況等）｜https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=I0050021｜2026-10-05｜直接
第 4 條：受委託蒐集、處理或利用個人資料者，於本法適用範圍內，視同委託機關｜https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=I0050021｜2026-10-05｜直接
第 5 條：不得逾越特定目的之必要範圍｜https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=I0050021｜2026-10-05｜直接
第 8 條：依第 15 條或第 19 條向當事人蒐集時應明確告知名稱、目的、類別、利用期間地區對象方式、權利、不提供之影響｜https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=I0050021｜2026-10-05｜直接
修正日期民國 114 年 11 月 11 日；增訂第 20-1 條、刪除第 27 條等，施行日期由行政院定之；生效狀態欄「部分或全部條文尚未生效，最後生效日期：未定」｜https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=I0050021｜2026-10-05｜直接（法規整編資料截止日民國 115 年 9 月 24 日）
現行（民國 112 年 5 月 31 日版本）第 27 條：非公務機關保有個人資料檔案者，應採行適當之安全措施，防止個人資料被竊取、竄改、毀損、滅失或洩漏｜https://law.moj.gov.tw/LawClass/LawOldVer.aspx?pcode=I0050021｜2026-10-05｜直接
新增第 20-1 條（未施行）：非公務機關保有個人資料檔案者，應辦理安全維護事項，防止被竊取、竄改、毀損、滅失或洩漏｜https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=I0050021｜2026-10-05｜直接
施行細則第 8 條：委託監督至少包含範圍、類別、特定目的與期間、複委託之受託者、委託終止時載體返還與個資刪除等；受託者僅得於委託機關指示之範圍內蒐集、處理或利用，認指示違法應立即通知｜https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=I0050022｜2026-10-05｜直接（修正日期民國 105 年 3 月 2 日）

## 圖與數字

diagram-1 上唯一的數字是頁尾的 2026，正文表格 caption 有「2026 年 10 月」。
hero 只有一行字「客戶資料先過三關」（8 字、56px），三個圓圈同樣大小，不是遞增長條。

## 寫作上的判斷（非來源事實）

- 「放進 AI 前的三個判斷」順序、報價單寫明三件事、結案後刪除對話與檔案，屬實務建議，不是任何來源的規定。
- 「個資貼進 AI 服務算不算在指示範圍內，條文沒有點名」是對條文文字的描述，沒有引用主管機關解釋。

## 查核第一輪的其他訂正（2026-10-05，逐條見 verify-1.md）

- Claude 設定名稱：zh-TW 隱私中心寫「設定 → 隱私 →『幫助改進我們的 AI 模型』」，無痕對話官方譯名是「無痕聊天」｜https://privacy.claude.com/zh-TW/articles/12109829-how-do-i-change-my-model-improvement-privacy-settings、https://privacy.claude.com/zh-TW/articles/10023580-is-my-data-used-for-model-training｜2026-10-05｜直接。表格原本只寫「模型改進開關」，已改成官方名稱
- Anthropic API 30 天刪除有例外（Files API 等使用者控制的較長保留、零資料保留協議、違反使用政策、法律要求），表格原本寫成無條件「30 天內刪除」，改成「原則上 30 天內刪除，另有例外」｜https://privacy.claude.com/en/articles/7996866-how-long-do-you-store-my-organization-s-data｜2026-10-05｜直接
- Gemini zh-TW 官方用語：「保留活動記錄」「臨時對話」，臨時對話與關閉保留活動記錄時的對話都保留 72 小時｜https://support.google.com/gemini/answer/13594961?hl=zh-Hant｜2026-10-05｜直接。表格的「暫時對話」改成「臨時對話」，保留期一格補上臨時對話
- 著作權法第 12 條第 1 項有但書「契約約定以出資人為著作人者，從其約定」，原文漏寫，已補｜https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=J0070017｜2026-10-05｜直接
- 智慧財產局電子郵件1150828c 問的是「新聞圖片」，原文寫成泛稱「圖片」，已改成「新聞圖片」｜https://www.tipo.gov.tw/tw/copyright/692-94326.html｜2026-10-05｜直接
- 個資法第 27 條：民國 114 年 11 月 11 日修正是刪除第 27 條、另增訂第 20-1 條（文字由「採行適當之安全措施」改為「辦理安全維護事項」），不是單純改條號；原文的「改列」改成「改由新增的第 20-1 條規範」。沿革頁今天仍沒有行政院定施行日期的令，法規資料庫生效狀態「最後生效日期：未定」，整編截止日民國 115 年 9 月 24 日｜https://law.moj.gov.tw/LawClass/LawHistory.aspx?pcode=I0050021｜2026-10-05｜直接
- 「獨立創作的保證站不住」是撰稿者的推論，沒有來源直接這樣說。範本的保證是「確為甲方獨立創作之作品，其內容無涉及毀謗、抄襲等」，已改成較保守的「容易有爭議」
- 人工智慧基本法第 4 條：條文主詞是「政府推動人工智慧之研發與應用」，原句文法不通，改寫成「規範對象是推動 AI 研發與應用的政府」｜https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=H0160093｜2026-10-05｜直接
- diagram-1.svg 的「暫時或無痕對話」改成「臨時或無痕對話」（含 desc）；圖上唯一的數字仍是 2026

## 查核第二輪（2026-10-05，逐條見 verify-2.md）

- 個資法修正施行日期：個資會籌備處公告今天可直接讀到（HTTP 200）：「修正條文施行日期，將另由行政院依同法第56條第1項定之」｜https://www.pdpc.gov.tw/News_Content/20/1010/｜2026-10-05｜直接。修法問答集 PDF Q2：施行前仍依現行規定｜https://ws.pdpc.gov.tw/FS01/FilePath/3/relfile/30/1072/a842b3f2-3399-4742-96ae-3f6648bd071a.pdf｜2026-10-05｜直接
- help.openai.com 今天仍 403（curl、.json、WebFetch），Wayback 連線被重設；三頁與 zh-hant 頁再用讀取代理重讀，內容與第一輪一致。存檔 _tools/ai-freelance-client-confidentiality/v2/jina_*.txt
- 「著作權法沒有要求標示」改成「著作權法沒有要求標示用了 AI」：電子郵件1150828c 第三點另說明利用他人圖片原則上應標示著作人（第 16 條），只有第五點（AI 產製、無人類創作內容）是「本法亦無規範」｜https://www.tipo.gov.tw/tw/copyright/692-94326.html｜2026-10-05｜直接

## 機械與看圖關卡（2026-10-05）

- dry-run ingest 通過；intake_check 0 FAIL。唯一的 WARN「no hero title found to check uniqueness」只檢查 Commons 照片 hero（讀 images.json），自繪 hero 沒有這個檔，屬預期
- hero 重畫：原圖是「左邊文件、中間虛線上的打勾圓圈、右邊藍色對話框、下方一行字」，與同批 ai-financial-report-reading 的 hero（左邊表格文件、虛線上的打勾圓圈、右邊藍色對話框、下方一行字）在縮圖上幾乎同型。改成一條路上「掛鎖的橘色資料夾 → 三道同樣大小的拱門（內有向右箭頭記號）→ 有星芒的藍色方塊」，文字仍是「客戶資料先過三關」；整組放大 1.12 倍讓 400 px 縮圖也看得清楚；hero alt 與 SVG desc 已改成描述新圖。舊檔備份在 _tools/ai-freelance-client-confidentiality/gate/backup/
- diagram-1.svg：交件框高度由 90 改成 110（與其他框一致，內距 ≥ 20 px），兩個「處理後回到主線」標籤上移 1 px，置中於框與虛線之間；圖上唯一的數字仍是 2026（表格 caption「查證於 2026 年 10 月」）
- 圖解 caption 原寫「任何一關答案是「有」就先處理右邊那一格」，但第三關不是是非題，改成「前兩關答案是「有」就先處理右邊那一格，再回到主線；第三關選定帳號後才交件」，與圖一致

## 跨篇核對（2026-10-05）

- 新增姊妹篇連結：ai-freelance-getting-started（向客戶說明一節後）。
