# ai-survey-design-analysis 查證記錄

查證日一律 2026-10-05（實際打開頁面的日期）。格式：主張｜來源網址｜查證日｜怎麼讀到的。
抓頁工具：`/home/user/batch-ai-office/_tools/ai-survey-design-analysis/fetch.sh`（curl -sSL、編輯部 UA、記 HTTP 狀態與最終網址），
`html2text.py` 先刪 `<!-- -->` 註解、script、style 再轉純文字；原始檔與文字檔在同目錄的 `pages/`。
除特別註明外，每頁都是 curl 200 直接讀全文，沒有用 Wayback。

## 題目偏誤（澳洲統計局、英國政府分析專業）

- 雙重問題：用「和」「或」把不同概念接在同一題；只有部分概念適用或方向相反時難以作答，填答者較容易答錯或跳過｜https://www.abs.gov.au/statistics/standards/abs-forms-design-standards/2023/general-forms-design-principles-question-structure｜2026-10-05｜curl 200，讀全文（ABS Forms Design Standards, 2023，Released 11/08/2023）。正文表格「兩者評價不同時答不出來」據此改寫。
- 評分題用平衡的方式問（例 "Do you favour or oppose"）；正負選項用意思正好相反、強度相當的詞（例 Very difficult／Very easy）；敏感題可先列否定選項｜同上｜2026-10-05｜同上。正文表格「正負用詞相反、強度相當」出自此處；「否定選項放前面」正文最後刪掉未用。
- 引導性問題：把填答者推向某個答案或讓某些答案看起來比較好｜同上｜2026-10-05｜同上
- 情緒性字眼（loaded questions）：含有會引發強烈情緒或意見的詞，填答者會對那個詞反應而不是對議題反應；例 'puts your health at risk'，改問 'Do you currently smoke?'｜同上｜2026-10-05｜同上。正文表格「填答者回應的是字眼，不是議題」據此改寫；「浪費時間的週會」是自擬示意例句。
- 選項順序效應（primacy／recency），網路表單可隨機排列選項｜同上｜2026-10-05｜同上（初稿寫過，為控制字數刪除，正文未用）。
- 預設前提：'How many days did you work last week?' 在沒先確認是否有工作時是引導性問題｜https://www.abs.gov.au/websitedbs/d3310114.nsf/home/Basic+Survey+Design+-+Questionnaire+Design｜2026-10-05｜curl 200（ISO-8859-1），讀全文（This page last updated 1 March 2023）。英國指引也用同一個例子。正文表格「預設前提」一列的例句「你上週加班了幾天？」為改寫。
- 不平衡的題目與選項：'Are you in favour of gun control?' 只給一個方向；中性地問 "Please rate your overall health" 卻只給 "Poor"、"Good"、"Excellent"｜同上｜2026-10-05｜同上。正文表格「量表不對稱」一列的「差、好、非常好」對應這個例子。
- 避免引導性問題（例 "Did everyone enjoy the course? We always get really good feedback about it"）；問平衡的問題（"if any"、"Are you for, or against, hybrid working?"）；拆開雙重問題（講師與教材的例子）｜https://analysisfunction.civilservice.gov.uk/policy-store/questionnaire-design-guidance/｜2026-10-05｜curl 200，讀全文（頁面日期 14 March 2023；相關連結區日期至 19 August 2026）。正文表格「引導性問題」「雙重問題」兩列的例句據此改寫。
- 量表：建議至少 5 點 Likert 量表，中間一律放中立選項；適當時在選項最後加 "Don't Know" 或 "Unsure"｜同上｜2026-10-05｜同上。正文「至少五個等級、中間放中立選項」。
- 敏感題：只問符合研究目的的；不要放在問卷開頭；說明為什麼要問；提供 "Prefer not to say"｜同上｜2026-10-05｜同上。正文「不願透露」為中文改寫。
- 英國的 Government Analysis Function 正文譯為「英國政府分析專業」，是自譯，不是官方中文名。

## Google 表單

- 限制只回覆一次：［設定］→「回覆」旁的向下箭頭→開啟［僅限回覆 1 次］；使用者必須登入 Google 帳戶，除非在「回覆」設定開啟「收集電子郵件地址」，否則不會記錄使用者名稱｜https://support.google.com/docs/answer/2839588?hl=zh-Hant｜2026-10-05｜curl 200，讀全文；英文版 ?hl=en 同日 curl 200 交叉核對（"Their usernames won't be recorded unless you turn on the 'Responses' setting to collect email addresses."）。
- 「呈現方式」→［查看結果摘要］：回覆結果摘要會顯示每個問題的回覆全文或圖表，凡是能回覆表單的使用者皆可查看｜同上｜2026-10-05｜同上
- 收集電子郵件地址：［設定］→「回覆」→「收集電子郵件地址」選「已驗證」（收集作答者的 Google 帳戶電子郵件，確認訊息顯示在表單每一頁）或「由作答者手動輸入」；開啟後作答者必須輸入電子郵件才能提交｜https://support.google.com/docs/answer/139706?hl=zh-Hant｜2026-10-05｜curl 200，讀全文；英文版 ?hl=en 同日 curl 200 交叉核對（Verified／Responder input）。因為開啟收集後電子郵件是必填，第 8 條清單第六項的例子改用「部門欄可不填」，不用「不填電子郵件仍可作答」。
- 回覆副本：收集電子郵件時可選擇是否寄回覆副本給作答者｜同上｜2026-10-05｜同上（正文最後未用）。
- 停止收集：「接受回應」下方「設定截止日或回覆限制」，可選日期或「回覆數量上限」；多人同時送出時，系統會忽略數量上限、接受所有同時提交的內容｜同上｜2026-10-05｜同上
- 連結試算表：與協作者共用表單時，協作者可能也有表單所連結試算表的存取權｜同上｜2026-10-05｜同上
- 自 2026 年 9 月起，每份表單總儲存空間上限 1 GB（含表單檔案與回覆資料，不含使用者上傳的檔案），最多 50 萬則回覆｜同上｜2026-10-05｜同上（中文頁寫「50 萬則」，英文頁寫 "500k responses"）。查證日已過 2026 年 9 月，所以正文寫成現況。
- Gemini 摘要：需要符合資格的 Google Workspace 或 Google AI 方案；可為開放文字題產生摘要；回覆有 3 到 200 則時才找得到摘要；測驗不能產生；摘要不會儲存；不會為姓名、地址這類直接問題產生摘要｜https://support.google.com/docs/answer/16231981?hl=zh-Hant｜2026-10-05｜curl 200，讀全文（查核第一輪更正：有繁體中文版「使用 Google 表單內建 Gemini 總結及分析回覆內容」，內容與 ?hl=en 一致，sources 改用 zh-Hant）。
- 主題歸納：可在 Google 試算表裡歸納開放題回覆的共同主題並算出比例（圓餅圖、各主題則數）；"works best with 8–200 responses"，超過 200 則時按鈕變灰；同頁另一則提示寫「少於或等於 8 則或超過 500 則時按鈕變灰」，兩處數字不一致，正文只寫「可歸納主題」，不寫數字｜同上｜2026-10-05｜同上
- "Gemini features may suggest inaccurate or inappropriate information."｜同上｜2026-10-05｜同上。正文「AI 可能出錯」。

## Microsoft Forms

- ［設定］→「誰可以填寫此表單」：［任何人都可以回應］時回應不記錄姓名；［僅我組織中的人可以回應］／［我組織中特定的人員可以回應］時可取消勾選［記錄名稱］；勾選則表單收集含個人識別資訊的回覆；使用 Hotmail、Live 或 Outlook.com 的 Microsoft 帳戶時沒有［記錄名稱］設定，自動不記錄姓名；［記錄名稱］底下可勾選［每人一個回應］｜https://support.microsoft.com/zh-tw/forms/set-up-your-survey-so-names-aren-t-recorded-when-collecting-responses｜2026-10-05｜curl 200，讀全文；英文版 /en-us/ 同日 curl 200 交叉核對。
- 即使取消［記錄名稱］，仍可能識別作答者的例子（清單非窮舉）：題目要求提供姓名等個人識別資訊；表單只發給組織中少數特定人員；表單發給不同時區的人時，可依「開始時間」「完成時間」的時間戳記比對｜同上｜2026-10-05｜同上。正文「微軟舉了三種」指的就是頁面列的這三個例子；「人數少的單位最好合併成一個選項」是編輯建議，不是微軟原文。
- 保持［記錄名稱］勾選，會記錄每個回應者的名稱及電子郵件；回應者必須來自組織內部才能記錄名稱｜https://support.microsoft.com/zh-tw/forms/choose-who-can-fill-out-a-form-or-quiz｜2026-10-05｜curl 200，讀全文；英文版 /en-us/ 同日 curl 200 交叉核對（"record the name and email of each respondent"）。
- ［接受回應］未勾選即停止收集；［開始日期］與［結束日期］可指定開始和停止收集的日期與時間｜https://support.microsoft.com/zh-tw/forms/adjust-your-form-or-quiz-settings-in-microsoft-forms｜2026-10-05｜curl 200，讀全文；英文版（/en-us/office/adjust-your-form-or-quiz-settings-in-microsoft-forms-f255a4ba-…，轉址到 /en-us/forms/…）同日 curl 200 交叉核對。
- 中文介面名稱不一致：同一功能在一頁寫［每人一個回應］、另一頁寫［一人一個回應］；正文用「每人一個回應」｜同上兩頁｜2026-10-05｜同上
- 每份表單／測驗最多 5,000,000 個回應（適用 Office 365 教育版、Microsoft 365 Apps 商務版、GCC 等）；GCCH＋DoD 為 50,000；個人帳戶免費版 200、付費版 1,000｜https://support.microsoft.com/zh-tw/forms/form-question-response-and-character-limits-in-microsoft-forms｜2026-10-05｜curl 200，讀全文；英文版同日 curl 200 交叉核對（"Up to 5,000,000"；"up to 200 for free accounts up to 1,000 for paid accounts"）。
- 「每人一個回應」只在連續 50,000 個回應內強制執行，超過 50,000 時不保證涵蓋完整資料集｜同上｜2026-10-05｜同上
- 表單描述方塊最多 1,700 個字元｜同上｜2026-10-05｜同上。正文「說明欄最多 1,700 個字元」。
- Copilot in Forms：需要 Microsoft 365 帳戶與 Copilot 授權；可擬問卷、檢查並改寫；"You can avoid common pitfalls and biases in survey design, such as leading questions, double-barreled questions, or ambiguous wording."；分析結果時到［檢視回應］開啟 Copilot｜https://support.microsoft.com/zh-tw/forms/welcome-to-copilot-in-forms｜2026-10-05｜curl 200，讀全文；英文版 /en-us/ 同日 curl 200 交叉核對。消費者帳號另有用 AI 點數的精簡列，正文只寫「需有 Copilot 授權」。
- Copilot 不得用來產生的內容包括 "Employment-related situations such as evaluating performance"；產出可能聽來可信卻不完整、不正確或不恰當，要自行核對｜https://support.microsoft.com/en-us/forms/frequently-asked-questions-about-copilot-in-forms｜2026-10-05｜curl 200（原網址 /en-us/office/frequently-asked-questions-about-copilot-in-forms-c9941b72-… 轉址至此），讀全文。

## 個人資料保護法與施行細則（全國法規資料庫）

- 法規現況：修正日期民國 114 年 11 月 11 日；生效狀態欄標示「本法規部分或全部條文尚未生效，最後生效日期：未定」；114 年修正第 1-1、12、18、21、22～26、41、47～49、52、53、55 條，增訂第 1-2、20-1、21-1～21-5、51-1、53-1 條，刪除第 27 條，施行日期由行政院定之。正文引用的第 2、3、5、6、7、8、19 條不在這次修正之列｜https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=I0050021｜2026-10-05｜curl 200，讀全文。
- 第 2 條第 1 款：個人資料包括姓名、出生年月日、聯絡方式……及其他得以直接或間接方式識別該個人之資料｜同上｜2026-10-05｜同上。「電子郵件、員工編號、部門加職稱的組合都可能算在內」是依「間接識別」所做的推論，正文用「可能」。
- 第 3 條：查詢或請求閱覽、請求製給複製本、請求補充或更正、請求停止蒐集處理或利用、請求刪除，不得預先拋棄或以特約限制｜同上｜2026-10-05｜同上
- 第 5 條：不得逾越特定目的之必要範圍｜同上｜2026-10-05｜同上
- 第 6 條：病歷、醫療、基因、性生活、健康檢查及犯罪前科之個人資料不得蒐集、處理或利用，但有例外（含經當事人書面同意）｜同上｜2026-10-05｜同上。正文「原則上不得蒐集」。
- 第 7 條第 3 項：明確告知第 8 條第 1 項各款事項，當事人未表示拒絕並已提供個人資料者，推定已依第 15 條第 2 款、第 19 條第 1 項第 5 款表示同意｜同上｜2026-10-05｜同上
- 第 8 條第 1 項：依第 15 條或第 19 條向當事人蒐集個人資料時，應明確告知：機關名稱、蒐集之目的、個人資料之類別、利用之期間地區對象及方式、依第 3 條得行使之權利及方式、得自由選擇提供時不提供對其權益之影響｜同上｜2026-10-05｜同上。正文清單六項的「例如」都是自擬示意。第 2 項的免告知情形正文未寫。
- 第 19 條第 1 項：非公務機關蒐集或處理個人資料，應有特定目的並符合法定情形之一（含第 5 款經當事人同意）｜同上｜2026-10-05｜同上
- 施行細則第 16 條：第 8 條、第 9 條告知的方式，得以言詞、書面、電話、簡訊、電子郵件、傳真、電子文件或其他足以使當事人知悉或可得知悉之方式為之｜https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=I0050022｜2026-10-05｜curl 200，讀全文（修正日期民國 105 年 03 月 02 日）。「寫在表單開頭的說明欄最直接」是編輯建議，不是條文。
- 施行細則第 17 條：無從識別特定當事人，指以代碼、匿名、隱藏部分資料或其他方式無從辨識該特定個人｜同上｜2026-10-05｜同上（正文未直接引用，供參）。

## AI 工具的資料條款

- Gemini 應用程式：「保留活動記錄」開啟時，Google 會用活動提供、開發與改進服務（包括訓練生成式 AI 模型），並由人工審查員協助；部分對話由人工審查（包括受過訓練的服務供應商）；審查過的對話最多保留三年；請勿輸入不想讓審查員看到的機密資訊；使用公司或學校帳戶時可能適用不同的資料處理條款｜https://support.google.com/gemini/answer/13594961?hl=zh-Hant｜2026-10-05｜curl 200，讀全文；英文版 ?hl=en 同日 curl 200 交叉核對（Last updated: September 24, 2026）。中文介面名稱「保留活動記錄」出自中文版。
- Google Workspace 的生成式 AI：未經許可，內容不會由人工審查或用於網域外的生成式 AI 模型訓練｜https://knowledge.workspace.google.com/admin/generative-ai/generative-ai-in-google-workspace-privacy-hub｜2026-10-05｜curl 200，讀全文（Last updated: August 14, 2026；頁尾 Last updated 2026-10-01 UTC）。
- Microsoft 365 Copilot：提示詞、回應與透過 Microsoft Graph 存取的資料不用於訓練基礎大型語言模型｜https://learn.microsoft.com/en-us/microsoft-365/copilot/microsoft-365-copilot-privacy｜2026-10-05｜curl 200（原網址 /en-us/copilot/microsoft-365/microsoft-365-copilot-privacy 轉址至此），讀全文（ms.date 2026-07-09，updated_at 2026-09-30）。
- Claude 個人方案（Free、Pro、Max）：使用者選擇允許時、對話被標記為安全審查時、或明確加入訓練計畫時，會用對話改進模型｜https://privacy.claude.com/en/articles/10023580-is-my-data-used-for-model-training｜2026-10-05｜curl 200，讀全文（頁面日期 March 16, 2026）。正文簡化為「在使用者允許時使用」，安全審查的情形未寫。
- OpenAI 說明中心（How your data is used to improve model performance）：curl 加 .json 回 403，WebFetch 也回 403，Wayback CDX 連線被重設；讀不到，所以正文不寫 ChatGPT 的訓練條款。

## 編輯判斷（不是來源原文）

- 提示詞範本、兩張表格的示意例句、第 8 條清單的「例如」、開放題分類的五個步驟（去識別、提類別、逐則標註、抽查、引用前再確認）都是編輯建議，沒有對應的官方原文；沒有寫任何抽查比例或數字。
- 「各類則數用試算表自己算」「摘要只當線索，結論要回到原文」是根據 Google 與微軟「AI 可能出錯」的提醒所做的建議。
- 圖解 diagram-1.svg 上沒有阿拉伯數字，只有頁尾的 2026（兩張表格 caption 都寫了 2026 年 10 月）與「第 8 條」的 8（正文有）。

## 查核第一輪（2026-10-05，另一代理）

全部 18 個來源重新 curl -sSL 抓取，皆 HTTP 200，原始檔在 `_tools/ai-survey-design-analysis/v1pages/`；逐條結果在 `verify-1.md`。改動：

- 個資法第 8 條第 2 項列有六款免告知情形，正文與摘要原本寫成一律要告知；摘要改「除法定免告知情形外」，正文補「同條第 2 項另有免告知的例外，是否適用要個案判斷」。
- 偏誤表的導言原寫「兩份指引都要求避開」：情緒性字眼、預設前提、量表不對稱只出現在 ABS，改為「提醒避開」。
- Google「查看結果摘要」顯示的是「回覆全文或圖表」，補上「或圖表」。
- Gemini 表單主題歸納不是 3 則起就能用（8 到 200 則最適合，同頁另一則提示又寫少於或等於 8 則、超過 500 則變灰），改為「回覆數符合條件時還能在試算表歸納主題」，不寫數字。
- Claude 個人方案除使用者允許外，對話被標記為安全審查時也會使用，已補上。
- sources：Gemini 表單頁改 zh-Hant 網址與中文標題；Gemini 隱私權專區改中文頁標題；ABS 標題刪掉正文未用的「選項順序效應」；Claude 標題補安全審查。
- 篇幅：刪掉導言的路線圖段落，「微軟表單服務」的中文說明移到 Microsoft Forms 第一次出現處；「人數少的單位最好合併成一個選項」縮為「最好合併」。body_length 2,606。
- 未變：Google 表單 2026 年 9 月起的 50 萬則／1 GB 上限（查證日已生效）；既有企業表單到 2027 年 3 月的過渡規定、GCC High／DoD 的 50,000 上限、個資法新主管機關（第 1-1 條施行日期由行政院定之）仍未寫進正文。

## 查核第二輪（2026-10-05，另一代理）

全部 18 個來源與 3 個站內連結重新 curl -sSL 抓取，皆 HTTP 200，原始檔在 `_tools/ai-survey-design-analysis/v2pages/`；逐條結果在 `verify-2.md`。改動：

- description「收到個資要依個資法第 8 條告知」與 h2「收到個資，就要先告知」仍是無例外的說法，時點也不對（第 8 條是「向當事人蒐集時」）：改為「蒐集個資原則上要依個資法第 8 條告知」「蒐集個資前，原則上要先告知」。
- 廠商功能與條款補日期：Copilot 授權、各家 AI 資料條款、兩套表單內建摘要三處加「2026 年 10 月」。
- 擬題範本旁補人工核對：「AI 的自我檢查只是初篩，每題仍要由人對照下一節的表格看過。」
- 摘要第一點 AI 補「（人工智慧）」；補回系列骨架要求的第二段導言（同批其他五篇都有）。
- 篇幅：body_length 2,700（目標 2,200–2,600，工具範圍 1,800–3,000）。
- 第一輪說「預設前提只在 ABS」：英國指引在 Avoid leading questions 也用了 "How many days did you work last week?"；「提醒避開」的措辭仍正確，未改。

## 機械與看圖關卡（2026-10-05）

- 只改版面，不改事實與正文：
  - diagram-1.svg：全程守則框從 y=372 上移到 y=361（文字基線 412 → 400）。原本框底離七、六兩個圓圈只有 10 px，上下距離不平均，現在上下各約 20 px。
  - hero.svg：三支深色箭頭與橘色虛線箭頭的 marker refX 從 9 改為 4，線段終點跟著內縮，箭頭尖端位置大致不變。原本線段的平頭從箭頭尖端兩側露出一小截，現在看不到。
  - hero alt 與 `<desc>` 補上「三支深色箭頭指向下方托盤」。
- 結果：dry-run exit 0；intake_check RESULT PASS（0 failures）。WARN 有三則，都預期中：「8 條」兩則是條號不是數量；自繪 hero 沒有 images.json，無從比對唯一性。
- 重新渲染 hero.png、diagram-1.png 看過：沒有文字壓線、溢出或互疊，構圖置中。圖上的數字只有 8 與 2026，正文都有。
- hero 與同批另外五篇的構圖不同：問卷卡加評分量表，對話框分進三個托盤。放大鏡在面試、校稿兩篇也有，但位置與構圖都不同。

## 跨篇核對（2026-10-05）

- Microsoft Learn 隱私頁今日重讀：頁首註明「Microsoft 365 Copilot is now named Microsoft Copilot」。正文改成「微軟企業訂閱的 Copilot（原名 Microsoft 365 Copilot）」，sources 標題改成頁面現在的名稱並註明更名；不用於訓練基礎模型的說法不變。
- 在開放題一節最後加了連到 ai-proposal-writing 的 article inline（調查結果寫進提案時，數字出處怎麼記）。
- intake_check 的兩個「8 條」WARN 是個資法第 8 條的條號，不是清單計數，保留。
- 重跑 dry-run 與 intake_check：0 FAIL，body_length=2711。
