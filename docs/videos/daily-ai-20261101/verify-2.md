# daily-ai-20261101 查核第 2 輪

查核日 2026-11-02。第二位查核代理，不是撰稿人，也不是第 1 輪的查核代理。
第 1 輪改了 5 個事實（超過 3 個），所以照 `verifier-video.md` 再查一輪。本輪做了兩件事：一是重查第 1 輪改過的每一行與卡片，加上協調者點名的開場 xatk；二是用新的眼光把整份稿子再看一遍（超過「已確認項目隨機抽三分之一」的要求）。
今天重新打開的頁面有兩類。站上 7 篇文章（`/api/travel/guides/life/<slug>?locale=zh-TW`，間隔 1.5 秒；不帶 `life/` 的路徑回 404）全部 HTTP 200、`status: published`，news_date 五篇 2026-10-30、兩篇 2026-10-31。`video.json` `sources` 列的 8 個官方頁或報導（間隔超過 1 秒）也全部 HTTP 200，沒有轉址，也沒有被擋。
來源代號沿用 `verify-1.md`：站上文章是 S1–S7，官方頁與報導是 O1、O1d、O2–O7。O1d（支出上限說明文件）今天仍是「Last updated 2026-10-26 UTC」。

## 一、第 1 輪改過的 5 處與開場（全部重查）

| # | 主張 | 位置 | URL | HTTP | 判定 | 修改前 → 修改後 |
| --- | --- | --- | --- | --- | --- | --- |
| R1 | 「可是有些用量，碰到上限也不會停。」；loops[0].what；標題「但有些不會停」 | 9cf8；loops[0]；youtube.title | O1、O1d | 200 | CONFIRMED。O1：「Provisioned Throughput is never halted」。O1d：「Spend caps don't pause any on-going, fixed usage associated with persistent resources (such as compute and storage services), which remain active and continue to accrue charges」，另有「Any in-flight requests … are processed to completion, accruing charges」。不會停的不只一種，「有些」對。 | |
| R2 | 「開場說有些用量不會停，就在這裡。」；keys[0]「有些用量不會停」 | n8n7；g-except.keys[0] | O1d | 200 | CONFIRMED（同 R1） | |
| R3 | Provisioned Throughput 照常執行，常駐的運算和儲存照樣計費；卡片 right「Provisioned Throughput」「常駐的運算與儲存資源」；keys[2]「預留容量、常駐資源：照常」；source 加說明文件 | mu9u；g-except | O1、O1d | 200 | CONFIRMED（事實）。O1：「requests using reserved capacity will continue to run, and serve traffic normally」；O1d 原文見 R1。本輪只為縮句把產品名留在卡片上（見〈三〉），意思不變。 | 見〈三〉 |
| R4 | 「…只要帳戶不是透過經銷商開的，今天就能做。」；g-do.source「經銷商帳戶不適用（說明文件）」 | ryzv；g-do | O1、O1d | 200 | CONFIRMED。O1d：「Spend cap budgets are limited to first-party Google Cloud customers. Reseller accounts are out of scope.」O1：「Get started today」，O1 與 O1d 都沒有地區限制。 | 見〈三〉（縮句） |
| R5 | 「金融時報則說，領投的會是一群阿拉伯聯合大公國的投資人。」 | 82ee；o-open.rows[2] | O2 | 200 | CONFIRMED。O2：「The round will be led by a group of investors from the United Arab Emirates, the FT said.」 | |
| R6 | 「華爾街日報也說，部分大型投資人的反應很冷淡。」；o-tepid 引句 | ynw6；o-tepid | O2 | 200 | CONFIRMED。O2：「A follow-up story in The Wall Street Journal offered more details, namely that the company has secured $11 billion so far, and that its fundraising efforts had met with a “tepid” response from some large investors.」引句逐字相符。 | |
| R7 | 「10 月 30 日，TechCrunch 報導，美國外送平台 DoorDash 在財報電話會議上，」 | 5qw9；d-open.source | O5、S5 | 200 | CONFIRMED。O5 是「6:54 AM PDT · October 30, 2026」，寫「revealed during its third-quarter earnings call」，沒有寫電話會議日期；日期掛在 TechCrunch 上是對的。 | 見〈三〉（縮句） |
| R8 | 開場「預算用完，雲端用量就自動暫停。」；open.data.key「預算用完，用量自動暫停」 | xatk；open.data.key | O1d、S1 | 200 | CHANGED。O1d：「Spend caps are limited to budgets that are scoped to a single Google Cloud project and a single eligible service」，「In this release, the eligible services include Gemini API, Agent Platform (formerly known as Vertex AI), Cloud Run, and Cloud Run functions」，「No other projects or other services are impacted」。「雲端用量就自動暫停」聽起來像整個 Google Cloud 帳戶都會停，但影片裡沒有任何一句交代只有指定的服務會停（9cf8、mu9u 講的是那項服務裡不停的部分，不是其他服務）。在台灣用 Compute Engine 之類的服務跑 AI 的人會以為也被保護。S1 也寫「暫停特定專案或服務的用量」。 | xatk「預算用完，雲端用量就自動暫停。」→「預算用完，你指定的雲端服務就自動暫停。」；open.data.key「預算用完，用量自動暫停」→「預算用完，指定服務自動暫停」；claims.md c2 跟著改 |

## 二、全片重看（第 1 輪標 CONFIRMED 的項目）

| # | 主張 | 位置 | URL | HTTP | 判定 | 修改前 → 修改後 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 10 月 30 日 Google Cloud 宣布支出上限正式推出；從預覽版轉正式版 | ru7q、rpf4；open、g-open | O1 | 200 | CONFIRMED（October 30, 2026；「generally available」「since the initial preview」） | |
| 2 | 暫停用量、不刪除資源 | 3gjh；g-open | O1、O1d | 200 | CONFIRMED（「without risking resource deletion」；O1d FAQ「No, resources or data aren't deleted」） | |
| 3 | 三件事：API 套到新測試專案；AI 服務以估算即時成本、幾分鐘內觸發；下個月初自動恢復、不用手動解除 | 4uc7–hew4；g-three | O1、O1d | 200 | CONFIRMED（「spins up a new sandbox project」「trigger within minutes of usage using estimated, live costs」「blocked services will seamlessly resume at the beginning of the next month」；手動覆寫照舊，卡片沒說沒有） | |
| 4 | 隨用隨付與承諾使用折扣涵蓋的請求會暫停 | n5u4；g-except.left | O1、O1d | 200 | CONFIRMED（「halt pay-as-you-go and CUD-covered requests」） | |
| 5 | Budgets and Alerts 頁面；先設測試專案、低金額；預設通知計費管理員與專案擁有者，50%／80%／100%；確認角色上有對的人 | 7nwk–ez5s；g-do | O1 | 200 | CONFIRMED（「Default alerts are automatically sent to billing administrators and project owners at 50%, 80%, and 100% of the cap. Make sure the right folks are set up in these roles.」） | |
| 6 | 300 億 → 200 億美元；已籌 110 億美元；TechCrunch 10-31 引述 FT | repi、qm94、dt7g；o-open | O2、S2 | 200 | CONFIRMED（9:12 AM PDT · October 31, 2026；FT「reported Friday」） | |
| 7 | TechCrunch 認為部分是時機不好，華爾街對 AI 基礎建設支出轉趨謹慎；TechCrunch 已去問 OpenAI | n94a、3m7v、htgq；o-why、o-you | O2 | 200 | CONFIRMED（「could be blamed, in part, on bad timing」「wary of heavy AI infrastructure spending」「has reached out to OpenAI for comment」） | |
| 8 | 法官駁回 xAI 撤案聲請；NAACP；孟菲斯附近 Colossus；渦輪機移動式、原告沒資格 vs 法官的裁定；至少 35 台 | 2hw3–32c6；x-open、x-dispute、x-not | O3、S3 | 200 | CONFIRMED（2:17 PM PDT · October 31, 2026；Judge Debra M. Brown 原文；「at least 35 combustion turbines」）。x-open kicker 今天已是「10 月 31 日 · TechCrunch」，第 1 輪〈懷疑但沒改〉那一項已處理。 | |
| 9 | 輿論似乎急轉；紐約暫停新建；其他州與地方考慮；Amazon、微軟不再用保密協議；可能是即將到來的期中選舉的重要因素 | hqkk–4g52；x-bg、x-watch | O3 | 200 | CONFIRMED（「seems to have turned sharply」「moratorium」「NDAs」「significant factor in the imminent U.S. midterm elections」） | |
| 10 | 10/1 發射；Gemma 4；俳句題目；經過挪威斯瓦巴；第一句「Blue marble below」；資料中心等級 TPU 在軌道上第一次（自述）；耐熱、抗輻射、2027 雙衛星互連 | 9a8s–9dz8；s-open、s-poem、s-claim、s-next | O4、S4 | 200 | CONFIRMED（Oct 30, 2026；引句三行逐字相符） | |
| 11 | 「幾百筆」引句；300 萬筆外送（2025 年報告）；不要逆勢也不要幻想；可能放廣告；6／7／9 月三個自家代理；Amazon 封鎖、Walmart 敞開大門 | yah9–nek4；d-* | O5、S5 | 200 | CONFIRMED（引句逐字相符；「laid out a red carpet for them in order to snag some business from its competitors」） | |
| 12 | Rosalind：10-30 補充文件；生物、藥物研發；只給合格的科學家、研究機構、企業與政府夥伴；與 GPT-6 Astra 同一組權重；拒答較少、仍拒絕生物武器化 | 5ijc–sm2h；r-open、r-same | O6 | 200 | CONFIRMED（Published October 30, 2026；Introduction 原文） | |
| 13 | 生物與化學 High、低於 Critical；網路安全沿用 Astra 評估列 Critical；遵守警告 21.7% 對 18.9%（越低越好） | gpc9–9yyg；r-risk、r-not | O6 | 200 | CONFIRMED（Table 12 欄序 GPT-Rosalind-6、GPT-6 Astra；「Respecting Warnings … ↓ 21.7% 18.9%」） | |
| 14 | 審核使命、用途、治理；正當需要、最小權限；輸出先經合格的人審查；文件沒寫台灣 | wtbk–vqed；r-you | O6 | 200 | CONFIRMED（4.2.1 Trust-based access 原文；全文沒有國家或地區） | |
| 15 | 教宗良十四世週五演說：解除武裝、機器是工具不是人；下個月日內瓦；禁止致命自主武器；人類有效監督；2024 年方濟各 | k9r3–5ra9；p-* | O7、S7 | 200 | CONFIRMED（Oct 30, 2026, 2:58 PM UTC；引句逐字相符） | |
| 16 | 縮圖、標題、說明欄、7 個 Mokaair 網址 | thumbnail、youtube | O1、O2、O4、S1–S7 | 200 | CONFIRMED（說明欄寫的是網站頁面網址 `/zh-TW/life/<slug>`，七篇都已發布） | |

## 三、縮短的句子（不改事實，id 不變，沒有刪句，reveal 與 keys 數不變）

| id | 修改前（字數） | 修改後（字數） |
| --- | --- | --- |
| rpf4 | 這個煞車，裝在 Google Cloud 的預算工具裡：支出上限從預覽版轉成了正式版。（43） | 這個煞車在 Google Cloud 的預算工具裡，從預覽版轉成了正式版。（37） |
| mu9u | 但預留容量的 Provisioned Throughput 照常執行，常駐的運算和儲存也照樣計費。（49） | 但預留容量的請求照常執行，常駐的運算和儲存也照樣計費。（27）；產品名留在卡片 right.points[0]；emotion「「不會」加重」→「「照常」加重」（句中已沒有「不會」） |
| ryzv | 對在台灣用 Google Cloud 跑 AI 的你，只要帳戶不是透過經銷商開的，今天就能做。（47） | 在台灣用 Google Cloud 跑 AI 的你，帳戶不是經銷商開的，今天就能做。（42） |
| 2hw3 | 10 月 31 日，TechCrunch 報導，美國一位聯邦法官駁回了 xAI 撤銷訴訟的聲請。（48） | 10 月 31 日，TechCrunch 報導，美國聯邦法官駁回了 xAI 的撤案聲請。（44） |
| 4g52 | 要觀察的是，TechCrunch 說這波反彈，可能成為美國即將到來的期中選舉的重要因素。（44） | TechCrunch 說，這波反彈可能是即將到來的美國期中選舉的重要因素。（37）；「要觀察的」仍在卡片 kicker |
| 9a8s | 10 月 30 日，Google 宣布，收到了 Project Suncatcher 原型衛星的第一個回應。（54） | 10 月 30 日，Google 說收到了 Suncatcher 原型衛星的第一個回應。（44）；全名在 s-open 卡片標題 |
| 5qw9 | 10 月 30 日，TechCrunch 報導，美國外送平台 DoorDash 在財報電話會議上，（49） | 10 月 30 日，TechCrunch 報導，美國外送平台 DoorDash 在財報會議上，（47） |
| 84ih | DoorDash 自己也在做代理：聊天機器人、命令列工具、文字下單，今年陸續推出。（41） | DoorDash 也有自家代理：聊天機器人、命令列工具、文字下單，今年陸續推出。（40） |
| txcc | 它其實跟 OpenAI 的旗艦推理模型 GPT-6 Astra，用的是同一組權重。（41） | 它跟 OpenAI 的旗艦推理模型 GPT-6 Astra，用同一組權重。（37） |
| gpc9 | 依 OpenAI 自己的整備框架，它在生物與化學列為高能力，還低於最嚴重的關鍵等級；（42） | 依 OpenAI 自己的整備框架，生物與化學列為高能力，低於最高的關鍵等級；（38） |

字數照 `[...text].length` 計，空格與拉丁字母逐字算。xatk 因事實修改從 15 字變 19 字。

## 摘要

- 查了 24 條：第 1 輪改過的 7 處（9cf8／loops／標題、n8n7、mu9u／g-except、ryzv／g-do、82ee、ynw6、5qw9），加上協調者點名的開場 xatk，以及全片重看的 16 條。CONFIRMED 23 條，CHANGED 1 條，NOT FOUND 0 條。
- 事實改動 1 處：xatk「預算用完，雲端用量就自動暫停。」→「預算用完，你指定的雲端服務就自動暫停。」，open.data.key「預算用完，用量自動暫停」→「預算用完，指定服務自動暫停」，claims.md c2 跟著改（上限一次只管一個專案的一項符合資格的服務，其他服務不受影響）。
- 第 1 輪的 5 處事實修改：全部對照今天的官方頁確認是對的，沒有退回任何一處。
- 縮句 10 句（見〈三〉），都不改事實；超過 40 字的句子從 11 句降到 5 句：ryzv 42、2hw3 44、9a8s 44、5qw9 47、5ijc 44，多出來的字是日期與英文專有名詞的空格和字母，唸起來不長。
- `sources` 8 個網址 2026-11-02 全部 HTTP 200，`checked_on` 已是 2026-11-02，不用改。
- 會過期的事實：OpenAI 募資目標、已籌金額、領投方（O2，2026-10-31）；支出上限的適用服務與經銷商限制（O1d，Last updated 2026-10-26，「Additional services will be included in subsequent releases」）；xAI 案進度（O3，2026-10-31）；Suncatcher 2027 里程碑（O4，2026-10-30）；日內瓦會議（O7，「next month」）；美國期中選舉就在 2026-11-03，影片晚於那天上架時「即將到來」就不成立。
- 觀點：v-main、v-unsure 都標成觀點，與 brief.md〈站主觀點〉一致；kx9f「唯一一則讓你今天就能設防線」在加了經銷商條件後仍成立。沒有不一致。
- 聽眾檢查（只報告）：沒有「經查證」「根據官方文件」「本影片」，沒有括號或網址，揭曉都在介紹句之後。mu9u 不再唸 Provisioned、Throughput；9a8s 不再唸 Project，這三個字典詞現在只剩卡片用到。
- lint：`node tools/video/cli.mjs lint --slug daily-ai-20261101` → `daily-ai-20261101: 0 errors, 2 warnings`（「10」7 句、「30」5 句，是每則第一句報日期的結果，與第 1 輪相同；估計 10.4 分鐘，108 句）。
- 懷疑但沒改：
  - 適用服務清單（Gemini API、Agent Platform、Cloud Run、Cloud Run functions）仍沒有上卡。xatk 改成「你指定的雲端服務」後不再誤導，但站主若要更明確，可在 g-do 某張步驟的 detail 寫上。
  - O1d：「the enforcement of spend caps isn't instant and any cost overages are billed as normal」。影片沒說一毛都不會多收，沒改。
  - 3kcs 把「解除武裝」與「機器是工具，不是人」連成一句，兩句都出自同一場演說，沒改。
- 需要第三輪：否。本輪只改了 1 個事實（不超過 3 個）。在第二輪範圍內，這份稿子已經查核完成。
