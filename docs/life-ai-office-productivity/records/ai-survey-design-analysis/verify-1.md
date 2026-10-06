# ai-survey-design-analysis 查核第一輪（2026-10-05）

每個來源都在 2026-10-05 用 curl -sSL（編輯部 UA）重新抓取，全部 HTTP 200、最終網址與 sources 相同，先刪 `<!-- -->` 註解再讀全文。原始檔在 `_tools/ai-survey-design-analysis/v1pages/`。

格式：主張｜判定｜來源網址

## 標題、描述、摘要

- 標題「用 AI 設計問卷與整理開放題：題目偏誤、匿名與個資」與內容相符｜ok｜（內部一致性）
- 描述：Google 表單「收集電子郵件」與 Microsoft Forms「記錄名稱」決定是否記名、各有回覆上限設定｜ok｜https://support.google.com/docs/answer/139706?hl=zh-Hant ；https://support.microsoft.com/zh-tw/forms/set-up-your-survey-so-names-aren-t-recorded-when-collecting-responses
- 描述：收到個資要依個資法第 8 條告知｜ok（正文已補第 2 項例外）｜https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=I0050021
- 摘要第三點：收到個資「要依第 8 條先告知」寫成無例外；第 8 條第 2 項列有六款免告知情形｜fixed（改為「除法定免告知情形外」）｜https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=I0050021
- 摘要第二點：小團體、作答時間、背景題組合仍可能認出作答者｜ok｜https://support.microsoft.com/zh-tw/forms/set-up-your-survey-so-names-aren-t-recorded-when-collecting-responses

## 題目偏誤

- 「ABS 與英國指引都要求避開下列寫法」：情緒性字眼、預設前提、量表不對稱只在 ABS，英國指引沒有這三項｜fixed（改為「提醒避開下列寫法」）｜https://www.abs.gov.au/statistics/standards/abs-forms-design-standards/2023/general-forms-design-principles-question-structure ；https://analysisfunction.civilservice.gov.uk/policy-store/questionnaire-design-guidance/
- 引導性問題：先替填答者表態（英國 "Did everyone enjoy the course? We always get really good feedback"；ABS steer respondents）｜ok｜https://analysisfunction.civilservice.gov.uk/policy-store/questionnaire-design-guidance/
- 預設前提：未先確認是否有工作就問上週工作幾天屬引導性問題｜ok（ABS 歸在 Leading Questions 底下，表格自成一列屬編輯分類）｜https://www.abs.gov.au/websitedbs/d3310114.nsf/home/Basic+Survey+Design+-+Questionnaire+Design
- 雙重問題：用「和」「或」接兩個概念，部分適用或方向相反時難答｜ok｜https://www.abs.gov.au/statistics/standards/abs-forms-design-standards/2023/general-forms-design-principles-question-structure
- 雙重問題例（講師與教材）拆成兩題｜ok｜https://analysisfunction.civilservice.gov.uk/policy-store/questionnaire-design-guidance/
- 情緒性字眼：填答者對字眼反應多於議題｜ok｜https://www.abs.gov.au/statistics/standards/abs-forms-design-standards/2023/general-forms-design-principles-question-structure
- 量表不對稱：中性提問卻只給 Poor／Good／Excellent｜ok｜https://www.abs.gov.au/websitedbs/d3310114.nsf/home/Basic+Survey+Design+-+Questionnaire+Design
- 改寫方向：正負用詞相反、強度相當（Very difficult／Very easy）｜ok｜https://www.abs.gov.au/statistics/standards/abs-forms-design-standards/2023/general-forms-design-principles-question-structure
- 英國指引：Likert 量表至少五點、中間放中立選項、適當時最後加 Don't Know／Unsure｜ok｜https://analysisfunction.civilservice.gov.uk/policy-store/questionnaire-design-guidance/
- 敏感題：只問符合研究目的的、不放開頭、說明原因、提供 Prefer not to say｜ok｜https://analysisfunction.civilservice.gov.uk/policy-store/questionnaire-design-guidance/
- 表格例句、提示詞範本｜ok（編輯示意，caption 已標「例句為示意」）｜—

## Microsoft Forms Copilot

- 需要 Microsoft 365 帳戶與 Copilot 授權；可擬題、改寫｜ok｜https://support.microsoft.com/zh-tw/forms/welcome-to-copilot-in-forms
- 可協助避開引導性問題、雙重問題｜ok｜https://support.microsoft.com/zh-tw/forms/welcome-to-copilot-in-forms
- 產出可能不完整、不正確或不恰當｜ok｜https://support.microsoft.com/en-us/forms/frequently-asked-questions-about-copilot-in-forms
- 不得用於 "Employment-related situations such as evaluating performance"｜ok｜https://support.microsoft.com/en-us/forms/frequently-asked-questions-about-copilot-in-forms
- 分析結果：［檢視回應］開啟 Copilot｜ok｜https://support.microsoft.com/zh-tw/forms/welcome-to-copilot-in-forms

## Google 表單設定

- ［設定］→「回覆」→「收集電子郵件地址」選「已驗證」收集 Google 帳戶電子郵件，「由作答者手動輸入」由對方填｜ok｜https://support.google.com/docs/answer/139706?hl=zh-Hant
- 「僅限回覆 1 次」需登入，未開收集電子郵件就不記錄使用者名稱｜ok｜https://support.google.com/docs/answer/2839588?hl=zh-Hant
- 「查看結果摘要」讓能填表單的人看到每題的「回覆全文」：原文是「回覆全文或圖表」｜fixed｜https://support.google.com/docs/answer/2839588?hl=zh-Hant
- 連結試算表可能被表單協作者看到｜ok｜https://support.google.com/docs/answer/139706?hl=zh-Hant
- 「設定截止日或回覆限制」；多人同時送出時忽略數量上限｜ok｜https://support.google.com/docs/answer/139706?hl=zh-Hant
- 自 2026 年 9 月起每份表單 50 萬則回覆、總儲存空間 1 GB｜ok（查證日已過 2026 年 9 月；既有企業表單到 2027 年 3 月的過渡規定未寫）｜https://support.google.com/docs/answer/139706?hl=zh-Hant
- Gemini 摘要：需符合資格的 Google Workspace 或 Google AI 方案；3 到 200 則回覆時自動產生文字題摘要｜ok｜https://support.google.com/docs/answer/16231981?hl=zh-Hant
- 「3 到 200 則回覆時……並可歸納主題」：主題歸納另有門檻（最適合 8 到 200 則、超過 200 則按鈕變灰，同頁提示又寫少於或等於 8 則或超過 500 則變灰），不是從 3 則起就能用｜fixed（改為「回覆數符合條件時還能在試算表歸納主題」，不寫數字）｜https://support.google.com/docs/answer/16231981?hl=zh-Hant
- 這頁沒有繁體中文版（初稿 notes）：實際有 zh-Hant 版「使用 Google 表單內建 Gemini 總結及分析回覆內容」，內容與英文版一致（含同樣的 8／200／500 矛盾）｜fixed（sources 改用 zh-Hant 網址與中文標題）｜https://support.google.com/docs/answer/16231981?hl=zh-Hant
- Gemini 功能可能提供不正確的資訊｜ok｜https://support.google.com/docs/answer/16231981?hl=zh-Hant

## Microsoft Forms 設定

- 「誰可以填寫此表單」選「任何人都可以回應」時不記錄姓名｜ok｜https://support.microsoft.com/zh-tw/forms/set-up-your-survey-so-names-aren-t-recorded-when-collecting-responses
- 限組織內作答時取消勾選「記錄名稱」就不記｜ok｜同上
- 勾選「記錄名稱」記下每位回應者的名稱及電子郵件｜ok｜https://support.microsoft.com/zh-tw/forms/choose-who-can-fill-out-a-form-or-quiz
- 個人帳號（Hotmail、Live、Outlook.com）建立的表單沒有記錄名稱設定、自動不記｜ok｜https://support.microsoft.com/zh-tw/forms/set-up-your-survey-so-names-aren-t-recorded-when-collecting-responses
- 微軟列的三種仍認得出人的情況（題目要求姓名、只發給少數人、時區加開始／完成時間）｜ok（原文註明清單不詳盡）｜同上
- 「每人一個回應」｜ok（另一頁寫「一人一個回應」，機器翻譯不一致）｜同上；https://support.microsoft.com/zh-tw/forms/adjust-your-form-or-quiz-settings-in-microsoft-forms
- 「每人一個回應」只在連續 50,000 個回應內強制執行｜ok｜https://support.microsoft.com/zh-tw/forms/form-question-response-and-character-limits-in-microsoft-forms
- 「接受回應」開關、開始與結束日期｜ok｜https://support.microsoft.com/zh-tw/forms/adjust-your-form-or-quiz-settings-in-microsoft-forms
- 每份表單最多 5,000,000 個回應（教育版、商務版、GCC）｜ok（GCC High／DoD 50,000 未列）｜https://support.microsoft.com/zh-tw/forms/form-question-response-and-character-limits-in-microsoft-forms
- 個人帳戶免費版 200、付費版 1,000｜ok｜同上
- 表單描述方塊最多 1,700 個字元｜ok｜同上

## 個人資料保護法與施行細則

- 法規現況：修正日期民國 114 年 11 月 11 日，部分條文施行日期由行政院定之；第 2、3、5、6、7、8、19 條不在 114 年修正之列｜ok｜https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=I0050021
- 第 2 條第 1 款：姓名、聯絡方式及其他得以直接或間接方式識別個人之資料｜ok｜同上
- 電子郵件、員工編號、部門加職稱「可能」算個資｜ok（依「間接識別」的推論，已用「可能」）｜同上
- 第 19 條：非公務機關蒐集應有特定目的並符合法定情形（含經當事人同意）｜ok｜同上
- 第 5 條：不得逾越特定目的之必要範圍｜ok｜同上
- 第 8 條第 1 項六款應告知事項｜ok｜同上
- 第 8 條第 2 項免告知情形：正文原本完全沒提｜fixed（正文補一句「同條第 2 項另有免告知的例外，是否適用要個案判斷」）｜同上
- 第 3 條五項權利、不得預先拋棄或以特約限制｜ok｜同上
- 第 7 條第 3 項：明確告知後未表示拒絕並提供資料，推定同意｜ok｜同上
- 第 6 條：病歷、醫療、基因、性生活、健康檢查及犯罪前科原則上不得蒐集｜ok｜同上
- 施行細則第 16 條：得以電子文件等方式告知｜ok｜https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=I0050022

## AI 工具資料條款

- Gemini 系列應用程式：「保留活動記錄」開啟時用於改良服務（含訓練生成式 AI 模型），部分對話人工審查，審查過的最多保留三年｜ok｜https://support.google.com/gemini/answer/13594961?hl=zh-Hant
- Claude 個人方案「在使用者允許時」使用對話：原文另有「對話被標記為安全審查時」與明確加入訓練計畫｜fixed（補上安全審查的情形）｜https://privacy.claude.com/en/articles/10023580-is-my-data-used-for-model-training
- Google Workspace 的 Gemini：未經許可不由人工審查、不用於網域外的生成式 AI 模型訓練｜ok｜https://knowledge.workspace.google.com/admin/generative-ai/generative-ai-in-google-workspace-privacy-hub
- Microsoft 365 Copilot：提示詞、回應與經 Microsoft Graph 存取的資料不用於訓練基礎 LLM｜ok｜https://learn.microsoft.com/en-us/microsoft-365/copilot/microsoft-365-copilot-privacy
- 開放題分類五步驟、抽查做法｜ok（編輯建議，沒有數字）｜—

## 站內連結

- ai-at-work-policy-checklist、ai-spreadsheet-automation、chatgpt-data-analysis-csv 三個都在允許清單，連結文字與現有文章標題相符｜ok｜https://mokaair.com/zh-TW/life/ai-at-work-policy-checklist ；https://mokaair.com/zh-TW/life/ai-spreadsheet-automation ；https://mokaair.com/zh-TW/life/chatgpt-data-analysis-csv

## 圖

- diagram-1.svg：沒有事實數字；「第 8 條」的 8 與頁尾 2026 都在正文；步驟內容與正文一致；重新渲染檢查，無壓線、溢出｜ok｜—
- hero.svg：只有一行字「問卷設計與開放題整理」，沒有數字；alt 與畫面相符｜ok｜—

## sources 清單

- 18 筆全部 HTTP 200（跟隨轉址後），checked_on 一律 2026-10-05｜ok
- 來源標題修正：Gemini 隱私權專區改用中文頁標題；ABS Question structure 刪掉正文未用的「選項順序效應」；Gemini 表單頁改 zh-Hant；Claude 頁補安全審查｜fixed（標題，非事實）

## 篇幅

- 刪掉導言第二段（路線圖），Microsoft Forms 的中文說明移到第一次出現處；body_length 2,606（目標 2,200–2,600，band 1,800–3,000）
