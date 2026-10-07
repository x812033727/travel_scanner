# ai-survey-design-analysis 查核第二輪（2026-10-05）

第二輪查核者，非撰稿者、非第一輪。所有來源在 2026-10-05 由本輪重新 curl -sSL 抓取（編輯部 UA），
全部 HTTP 200、最終網址與 sources 相同；先刪 `<!-- -->` 註解再讀。原始檔在
`_tools/ai-survey-design-analysis/v2pages/`（抓取清單 `v2list.txt`、腳本 `v2fetch.sh`）。
另抓英文版 g1en、g2en、g3en、ms4en 交叉核對。改稿腳本：`verify2_edit.py`、`verify2_trim.py`、
`verify2_fix3.py`；改稿前的 pack 備份在 `_tools/ai-survey-design-analysis/pack.before-v2.json`。

格式：主張｜判定｜來源

## A1. 第一輪改過的事實（逐條重查）

- 個資法第 8 條第 2 項六款免告知（依法律得免告知、履行法定義務所必要、妨害公務、妨害公共利益、當事人明知、非營利且顯無不利影響）；摘要「除法定免告知情形外」與正文「同條第 2 項另有免告知的例外，是否適用要個案判斷」｜ok｜https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=I0050021
- 同一事實第一輪漏改兩處：description 仍寫「收到個資要依個資法第 8 條告知」、h2 寫「收到個資，就要先告知」，都是無例外的絕對說法，且「收到」與第 8 條「向當事人蒐集時」的時點不合｜**fixed**：description 改「蒐集個資原則上要依個資法第 8 條告知」，h2 改「蒐集個資前，原則上要先告知」｜同上
- 偏誤表導言「提醒避開」｜ok。補充：第一輪說「預設前提只在 ABS」不完全對——英國指引在 Avoid leading questions 底下也列 "How many days did you work last week?"（assumes they worked），並有 Ask balanced questions；但情緒性字眼（loaded）與選項不對稱（Poor／Good／Excellent）確實只在 ABS。「提醒避開」對兩份指引都成立，不需改｜https://analysisfunction.civilservice.gov.uk/policy-store/questionnaire-design-guidance/ ；https://www.abs.gov.au/websitedbs/d3310114.nsf/home/Basic+Survey+Design+-+Questionnaire+Design ；https://www.abs.gov.au/statistics/standards/abs-forms-design-standards/2023/general-forms-design-principles-question-structure
- Google「查看結果摘要」：「回覆結果摘要會顯示每個問題的回覆全文或圖表，凡是能回覆表單的使用者皆可查看」｜ok｜https://support.google.com/docs/answer/2839588?hl=zh-Hant
- Gemini 表單摘要：需符合資格的 Google Workspace 或 Google AI 方案；「只要有 3 到 200 則回覆，系統就會生成摘要」；「系統會自動在摘要區塊中，替各個文字問題產生摘要」；主題「最適合用於 8 到 200 則」、超過 200 則按鈕變灰，同頁提示又寫「少於或等於 8 則，或超過 500 則」變灰——矛盾仍在，正文不寫主題門檻數字是對的｜ok｜https://support.google.com/docs/answer/16231981?hl=zh-Hant
- 該頁 zh-Hant 版存在，標題「使用 Google 表單內建 Gemini 總結及分析回覆內容」｜ok｜同上
- Claude 個人方案（Free、Pro、Max）：使用者允許、對話被標記為安全審查、或明確加入訓練（如 Trusted Tester Program）時使用對話；頁面日期 March 16, 2026｜ok（明確加入訓練屬「使用者允許」的一種；按讚／倒讚回饋另有一段會用於訓練，正文未寫，屬不完整但不錯誤，未改）｜https://privacy.claude.com/en/articles/10023580-is-my-data-used-for-model-training

## A2. 第一輪無法確認的項目

- Gemini 表單主題門檻 8／200／500 自相矛盾：今天重抓 zh-Hant 與 en 兩版仍一樣矛盾｜維持不寫數字
- Google 表單「自 2026 年 9 月起」每份表單 1 GB、50 萬則：頁面原文確認；既有企業表單超過上限者「在 2027 年 3 月前仍可接收新回覆」｜ok，過渡規定與一般讀者（新建問卷）無關，維持不寫｜https://support.google.com/docs/answer/139706?hl=zh-Hant
- Microsoft Forms「GCCH+DOD，表單/測驗最多可收到 50,000 個回應」；5,000,000 為一般上限｜ok，表格寫「商務與教育版 5,000,000 則」與頁面相符，GCC High／DoD 對台灣讀者無關，維持不寫｜https://support.microsoft.com/zh-tw/forms/form-question-response-and-character-limits-in-microsoft-forms
- 個資法第 1-1 條「本法之主管機關為個人資料保護委員會」：112 年增訂、114 年修正，施行日期由行政院定之；生效狀態「部分或全部條文尚未生效，最後生效日期：未定」。正文引用的第 2、3、5、6、7、8、19 條不在 112、114 年修正條次之列｜ok，正文不提主管機關，不需改｜https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=I0050021
- ChatGPT 訓練條款：正文沒有寫任何 ChatGPT 規則｜無需處理
- 篇幅：見 C 節
- intake WARN「8 條」是條號不是數量；自繪 hero 無法比對唯一性｜預期中，維持

## A3. 抽查（verify-1.md 主張列，從第 2 列起每三列一條）

- [2] 描述：Google「收集電子郵件地址」與 Microsoft Forms「記錄名稱」決定是否記名、各有回覆上限設定｜ok｜g2、ms1、ms4
- [5] 摘要：小團體、作答時間、背景題組合仍可能認出作答者｜ok（微軟列「只傳送給少數特定人員」「開始時間／完成時間」比對；「背景題」是編輯延伸，摘要未歸給微軟）｜https://support.microsoft.com/zh-tw/forms/set-up-your-survey-so-names-aren-t-recorded-when-collecting-responses
- [8] 預設前提：ABS 'How many days did you work last week?' 未先確認是否工作屬 leading question｜ok（英國指引也有同例）｜ABS Basic Survey Design
- [11] 情緒性字眼：'Respondents will tend to react more to the loaded phrase than the issue'｜ok｜ABS Forms Design Standards 2023
- [14] 英國：至少 5 點 Likert、中間放中立選項；適當時最後加 "Don't Know" 或 "Unsure"｜ok｜英國指引
- [17] Copilot in Forms：「必須擁有 Microsoft 365 帳戶和 Copilot 授權」｜ok｜https://support.microsoft.com/zh-tw/forms/welcome-to-copilot-in-forms
- [20] Copilot must not be used for "Employment-related situations such as evaluating performance"｜ok｜https://support.microsoft.com/en-us/forms/frequently-asked-questions-about-copilot-in-forms
- [23] 「僅限回覆 1 次」須登入，未開收集電子郵件就不記錄使用者名稱｜ok｜g1
- [26] 「設定截止日或回覆限制」；「如果多人同時送出回覆，系統會忽略回覆數量限制」｜ok｜g2
- [29] 主題歸納門檻（見 A1）｜ok
- [32] 「任何人都可以回應」：回應會自動收到，但不會記錄姓名｜ok｜ms1
- [35] Hotmail、Live、Outlook.com 帳戶無「記錄名稱」設定、自動不記｜ok｜ms1
- [38] 「每人一個回應」只在連續 50,000 個回應中強制執行｜ok｜ms4
- [41] 個人帳戶免費 200、付費 1,000｜ok｜ms4（en 版同）
- [44] 第 2 條第 1 款「……聯絡方式……及其他得以直接或間接方式識別該個人之資料」｜ok｜個資法
- [47] 第 5 條「不得逾越特定目的之必要範圍」｜ok｜個資法
- [50] 第 3 條五項權利、不得預先拋棄或以特約限制｜ok｜個資法
- [53] 施行細則第 16 條：告知得以……電子郵件、傳真、電子文件……為之（修正日期民國 105 年 03 月 02 日）｜ok｜https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=I0050022
- [56] Google Workspace：「Your content is not human reviewed or otherwise used for Generative AI model training outside your domain without permission」（Last updated: August 14, 2026）｜ok｜Workspace Privacy Hub
- [59] 站內連結三篇今天 200，頁面標題與連結文字相符｜ok｜mokaair.com
- [62] sources 18 筆今天全部 200｜ok

附帶重看（未在抽樣內，但改稿涉及）：Gemini 隱私權專區「Google 會在人工審查員協助下，使用您的活動記錄提供、開發及改良服務 (包括訓練生成式 AI 模型)」「經過審查的對話記錄最多會保留三年」（上次更新 2026 年 9 月 24 日）；Microsoft 365 Copilot「Prompts, responses, and data accessed through Microsoft Graph aren't used to train foundation LLMs」｜ok

## B. 合規審查（辦公效率批次）

- 實測：全文無「實測」、分數、測試結果｜ok
- AI 工具功能與限制只照廠商說明：Copilot in Forms、Gemini 表單摘要、各家資料條款都對得上官方頁｜ok；**缺日期**：正文三處廠商功能／條款沒有日期｜**fixed**：Copilot 段加「截至 2026 年 10 月需 Copilot 授權」，AI 條款段加「2026 年 10 月的條款是」，內建摘要段加「截至 2026 年 10 月」
- 法規條號：第 2、3、5、6、7、8、19 條與施行細則第 16 條逐條對過全國法規資料庫原文｜ok；description 與 h2 的絕對說法已修（見 A1）
- 提示詞範本：label 為「提示詞範本」，沒有宣稱效果｜ok
- AI 產出旁的人工核對：開放題分類（人工修訂類別、人工抽查）與內建摘要（摘要只當線索）都有；**擬題範本後面沒有人工核對步驟**，只有「要它自我檢查」｜**fixed**：Copilot 段前加「AI 的自我檢查只是初篩，每題仍要由人對照下一節的表格看過。」
- 不偏袒工具：Google 與微軟並列，個人版與企業版的差別都以官方條款為理由｜ok
- Copilot FAQ 另禁止 legal advice：正文沒有叫讀者用 Copilot 寫個資告知，不衝突｜ok

## C. 讀者優先與文風

- 「本文」「這篇」0 次｜ok
- 研究過程敘述（查證、官網寫、查不到、本批、撰稿）：無｜ok。「澳洲統計局與英國政府分析專業的問卷設計指引，提醒避開下列寫法」「英國指引建議」「微軟提醒」「微軟舉了三種」是把建議歸給權威，不是研究過程，保留
- 外來詞第一次出現附中文：ABS、Government Analysis Function、Microsoft Forms、Copilot、Gemini、Claude、Google Workspace、Record name 都有；**AI 第一次出現（摘要第一點）沒有中文**｜**fixed**：「AI（人工智慧）擬的題目……」
- 台灣用語、無驚嘆號、無贅語｜ok（「總結」只出現在 Google 的頁面標題）
- 導言第一段一句話回答問題｜ok
- **區塊骨架**：life-ai-series-brief §4 要兩段導言（第二段講讀完能做到什麼），同批另外五篇都有；第一輪為了字數刪掉第二段｜**fixed**：補回「照順序做完，題目會中立、記名與否寫明並依法告知，開放題也能在不外流原文的情況下分好類、經人抽查再回報。」（成果，不是路線圖）
- 篇幅：上面的補充讓正文變長，另刪摘要第二、三點的重複字（「除了不收電子郵件、不記錄名稱」「向填答者」「資料」）、提示詞段改「最後要它自我檢查」、「Google 的企業版」改「Google 企業版」。body_length 2,606 → **2,700**：比 2,200–2,600 的目標多 100 字，全是合規補充，仍在工具的 1,800–3,000 內；沒有可刪而不損實質的段落，所以不再硬砍
- 圖：重新渲染 hero.png、diagram-1.png 看過。diagram 八格兩排、回頭虛線與全程守則框都沒有壓線或溢出，構圖置中；圖上數字（8、2026）正文都有。hero 一行字 44px、11 個中文字，無 logo、人臉、上升長條；alt 與畫面相符｜ok

## D. 結果

- `pack_cli ingest --dry-run`：exit 0，「dry run: nothing written」
- intake_check：RESULT PASS（0 failures），body_length=2700；WARN 只剩「8 條」兩則與 hero 唯一性一則，皆預期中
