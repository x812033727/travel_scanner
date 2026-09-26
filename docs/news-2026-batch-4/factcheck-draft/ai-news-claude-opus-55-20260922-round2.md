# 查核第二輪：ai-news-claude-opus-55-20260922

查核者：獨立查核代理（第二輪，claude-opus-5-5；不是撰稿者，也不是第一輪），2026-09-26（台北）。規格：`FACTCHECK-48.md`、`docs/news-2026-batch-4/agents/ai/SECOND-ROUND.md`（第一輪規格 `agents/ai/FACTCHECK.md` 全部適用）、DELTA-4-8 全文、DELTA-4-7 第 3、4、10、11、14、16 條、DELTA-4-5、BRIEF.md 十二種錯誤型態、第一輪報告 `ai-news-claude-opus-55-20260922-round1.md`。

## 摘要

- 主張 124 條：CONFIRMED 112、CHANGED 11、NOT FOUND 1（刪）。範圍：第一輪改過或新寫的 43 條（含研究紀錄 7 處）、第一輪 CONFIRMED 129 條裡隨機抽 43 條（`random.Random(20260926)`）、限定詞與五個小標回掃 30 條、協調者裁定 6 條、兩個結尾連結。
- 內容包 12 處事實修正、4 處騰字數精簡；研究紀錄 7 處修正與 `factcheck.second_round`。段落 2,994 → 2,997／3,000，標題 60／60。
- 最重的五處：
  1. 標題照裁定 1 改成「Claude Opus 5.5 推出：牌價降 20%、付費方案五小時上限提高，40% 是 Anthropic 的成本估計」，三段各對到公告原句；研究紀錄 `title` 同步。
  2. 第五節第二段照裁定 2 限縮：「（AutomationBench 除外：它沒開備援，防護介入就算失敗）」，出自公告註腳 2。
  3. 第三節第三段「以上定價與前一節的 API 價格都未含稅，且可能調整」是 NOT FOUND：定價頁的稅務與「subject to change」註記只印在個人方案與 Team／Enterprise 價格卡下方，API 區與公告頁都沒有寫稅 → 「以上價格未含稅，且可能調整」。研究紀錄的 fact 40、`not_said`、`must_not_write` 本身把「未含稅」套到所有價格，已同改，下一輪不要改回。
  4. 限定詞：「a less reliable guide」是比較級，「越來越不能反映」→「越來越難以反映」（summary 5、第五節第一段、FAQ 7，研究紀錄 fact 14 同改）；說明中心的 “potentially higher-risk” 補「疑似」（第四節第一段、FAQ 5，fact 24 同改）；定價頁 “subject to change” 的「會更動」→「可能更動」（第三節第一段、callout）。
  5. FAQ 3 第一輪加的「定價頁 API 價格區列出的最新模型仍是 Sonnet 5 與 Haiku 4.5」不在正文（FAQ ⊆ 正文），刪掉；研究紀錄那條 fact 保留，仍撐正文「截至查核日還沒推出」。另外 description 的「付費方案用量上限」補成「五小時上限」，與第一輪改過的標題同一個範圍。
- 裁定 5：Sonnet 5.5／Haiku 5.5 在台北 22:53 重查一次，news、sitemap、blog、models overview、定價頁都沒有，「截至查核日還沒推出」保留。裁定 4：蒸餾類照說明中心與 System Card「直接擋下」，沒有重開。
- 第一輪新寫的句子全部對得上原文；第一輪的 22 處修正沒有一處要改回，只有 FAQ 3 多加的那半句因為不在正文而刪掉（內容本身屬實）。第一輪報告把定價頁稅務註記說成「頁尾」、並把 #79「API 價格未含稅」判 C，這一條錯了。
- 引文：研究紀錄 60 條 `verbatim_quote` 對我自己的正規化全文做連續字串比對，全部找到；沒有一條含 `...`、`…` 或 `|`。
- 自檢：`check_article.py` → `OK ai-news-claude-opus-55-20260922 zh-TW paragraphs 2997`（exit 0）；`pack_cli lint` 只有 `image_missing` ×2 與 `raw_internal_url`（exit 1，預期內）。
- 結論：`ok`。

## 重抓結果

| 來源 | HTTP | bytes（落地） | 落地 URL | body |
| --- | --- | --- | --- | --- |
| https://www.anthropic.com/claude-opus-5-5 | 200 | 619,967 | 同 | 正文；與第一輪、研究代理逐位元組相同 |
| https://support.claude.com/en/articles/16049681-… | 200 | 365,182 | 同 | 正文（Intercom，Updated yesterday）；位元組不同、正規化全文與第一輪相同 |
| https://claude.com/pricing | 200 | 1,171,532 | 同 | 正文（`<title>` Plans & Pricing \| Claude by Anthropic）；位元組不同、正規化全文相同 |
| https://anthropic.com/claude-opus-5-5-system-card | 200 | 17,795,106 | www-cdn.anthropic.com/…/Claude%20Opus%205.5%20System%20Card.pdf | PDF 230 頁，逐位元組相同；系統 python pypdf 重抽 |
| https://www.anthropic.com/news（只查裁定 5） | 200 | 459,343 | 同 | 最新 Sep 23，沒有 Sonnet／Haiku 5.5 |
| https://platform.claude.com/docs/en/models/overview（同上） | 200 | 392,263 | 同 | 現役 Fable 5.1、Opus 5.5、Sonnet 5、Haiku 4.5 |
| https://www.anthropic.com/sitemap.xml（同上） | 200 | 69,048 | 同 | 537 個 loc；有 /claude-opus-5-5，沒有 sonnet／haiku 5.5 |
| https://claude.com/blog（同上） | 200 | 805,184 | 同 | 最新 September 25, 2026，沒有 Sonnet／Haiku 5.5 |

抓取時間 2026-09-26T14:52:43–14:53:15Z（台北 22:52–22:53），UA `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)`，同主機間隔 ≥1.5 秒，請求沒有任何人的姓名或 email；紀錄在 `_raw/ai-news-claude-opus-55-20260922/round2/fetch-log.tsv`。後四頁只用來反駁「Sonnet／Haiku 5.5 已上線」，不撐文章任何一句。比對 Sonnet／Haiku 5.5 時連 `sonnet-5-5`、`haiku_5_5` 這類寫法一起查，五頁 0 次，只有公告頁 “will follow in the coming weeks” 那句。

## 主張逐條

C＝CONFIRMED，CH＝CHANGED，NF＝NOT FOUND（改寫／刪）。出處縮寫：A＝公告頁、H＝說明中心 16049681、P＝定價頁、S＝System Card。

### A. 第一輪改過或新寫的句子（43）

| # | 位置 | 主張 | 判定 | 依據 |
| --- | --- | --- | --- | --- |
| A1 | title | （第一輪）「付費方案五小時上限」 | C | A “increasing five-hour usage limits on Pro, Max, Team, and seat-based Enterprise plans”；新標題保留這段（見 D） |
| A2 | 第一段 | 截至查核日，定價頁比較表 Opus 系列 Free 標 No | C | P `Opus No Yes Yes Yes`；本輪只把「這個系列…欄位」精簡成「系列…欄」 |
| A3 | summary 3 | 截至 9 月 26 日，Opus 系列 Free 標 No | C | P |
| A4 | summary 3 | Pro、Max、Team 與按席次計費 Enterprise 提高五小時上限 | C | A |
| A5 | summary 3 | 公告沒寫提高多少，清單沒有 Free | C | A（正文詞界比對 Free 0 次，沒有任何倍數或百分比） |
| A6 | summary 4 | 資安類可能轉給 Opus 4.8 | C | H “may fall back to Opus 4.8” |
| A7 | summary 4 | 生物與前沿 LLM 開發類轉給 Opus 5 | C | H 兩段各有 “These classifiers cause Claude to fall back from Opus 5.5 to Opus 5” |
| A8 | summary 4 | 蒸餾類直接擋下、不轉 | C | H “blocked outright”、S “no fallback model”（裁定 4） |
| A9 | 一-1 | 估計執行成本少 40%（條件見下一節） | C | A “Our tests show that at default settings it will cost 40% less than Opus 5 on typical workloads.” |
| A10 | 一-3 | 公告寫「未來幾週」、沒有給日期 | C | A “will follow in the coming weeks” |
| A11 | 一-3 | 截至查核日還沒推出 | C | 裁定 5 重查：P Latest models＝Fable 5.1、Opus 5.5、Sonnet 5、Haiku 4.5；另四頁 0 次 |
| A12 | 表 | Fast mode「Claude Code 與 Claude Platform 提供」 | C | A “is also available in Claude Code and the Claude Platform” |
| A13 | 四-1 | 資安請求「可能會」轉給 Opus 4.8 | C | H may |
| A14 | 四-2 | （例如看懂檢驗報告…） | C | H “including interpreting lab results, understanding symptoms, and learning about biology” |
| A15 | 四-3 | 原請求還在對話裡時可能再被換掉 | C | H Note “the same safeguards may cause Claude to fall back again if your original request is still part of the conversation” |
| A16 | 四-3 | Config 裡的 MODEL & OUTPUT、訊息被標記時換模型的開關 | C | H “Config > MODEL & OUTPUT in Claude Code”、“Toggle Switch models when a message is flagged off” |
| A17 | 四-4 | LSVP 從公告當天起就能申請 | C | A “can apply today”；頁首日期 September 22, 2026 |
| A18 | 四-4 | 「；多數資安任務目前會轉給 Opus 4.8」（去掉因果） | C | A “most cybersecurity tasks will be re-routed to Opus 4.8”；A、H 都沒有「因為不在 CVP」 |
| A19 | 五-2 | 懷疑自己被評估的「跡象」 | C | A “We see signs that Opus 5.5 often suspects it is being evaluated” |
| A20 | 五-3 | 每種情境（「包括」寫程式…） | C | A “in every setting we tested, including coding, tool use, computer use, and web browsing” |
| A21 | 五-3 | System Card 列出退步：使用者貼進提示的文字裡被人埋入的惡意指令 | C | S 摘要 “more likely than previous models to follow malicious instructions in text that a user pastes into their own prompt”；§6.5.1 “instructions planted by someone else” |
| A22 | 五-3 | 最終版本加上產品改動已「緩解」 | C | S §6.5.1 “The ﬁnal snapshot … together with some changes in our products, has mitigated this issue.”（是緩解，不是解決） |
| A23 | 五-3 | 正在加上移除看不見字元、標記貼上文字的功能 | C | S “We are also adding product changes that remove invisible characters and mark pasted text” |
| A24 | 五-3 | 貼別人寫的文字＝讓對方控制一部分提示 | C | S §6.5.1 “they are effectively letting that person control part of their prompt” |
| A25 | FAQ 3 | 截至 9/26 查核還沒有 | C | 同 A11 |
| A26 | FAQ 3 | 定價頁 API 價格區最新模型仍是 Sonnet 5 與 Haiku 4.5 | CH（刪） | P 屬實，但正文沒有這句；FAQ ⊆ 正文（SECOND-ROUND 第 4 項）。研究紀錄那條 fact 保留 |
| A27 | FAQ 4 | 「公告則寫」CVP 未來幾週才擴大 | C | A “In the coming weeks we will also be expanding access to our Cyber Verification Program”；H 沒有這句 |
| A28 | FAQ 5 | 資安請求「可能」轉給 Opus 4.8 | C | H may（本輪另補「疑似」，見 C2） |
| A29 | FAQ 6 | MODEL & OUTPUT | C | H |
| A30 | FAQ 6 | 「Switch models when a message is flagged」 | C | H 原字串逐字 |
| A31 | FAQ 7 | OpenAI 模型的「部分」分數（例如 Terminal-Bench 4.0）是 OpenAI 自報 | C | A 表下註 “GPT-6 Astra at high effort, as reported by OpenAI”、註腳 1、註腳 3（Terminal-Bench-Science 的 GPT-6 Astra） |
| A32 | FAQ 7 | AutomationBench 的 Opus 5.5 分數是 Zapier 搶先使用期間跑的 | C | A 註腳 2 “Claude Opus 5.5 results come from Zapier’s own evaluation during early access.” |
| A33 | callout | 公告本身沒寫；截至 9/26 Opus 系列 Free 標 No | C | A、P（同句的「會隨時間更動」見 C5） |
| A34 | 第一段（精簡） | 刪「只印日期、沒有寫時刻」 | C | 日期還在；沒有刪限定詞 |
| A35 | 一-2（精簡） | 在 API 與 claude.ai 上都不能把思考模式關掉 | C | S “On both API and claude.ai , Claude Opus 5.5 is only available with thinking enabled.”；A “no longer available with “thinking” mode switched off” |
| A36 | 二-1（精簡） | 刪「兩者相加」 | C | 沒有刪限定詞（本輪再刪同句的「兩件事相加——」，見騰字數） |
| A37 | 研究紀錄 `title` | 第一輪標題 | C（被裁定 1 取代） | — |
| A38 | 研究紀錄 `diagram.nodes[2]` | 「五小時上限提高、未寫幅度」 | C | A |
| A39 | 研究紀錄 fact 19 | signs | C | A |
| A40 | 研究紀錄 fact 20 | including | C | A |
| A41 | 研究紀錄新 fact 18 | AutomationBench 其他三個模型的分數來自 Zapier 公開排行榜；沒開備援、介入算失敗；OpenAI 自報只適用 TB 4.0 與 TB-Science | C | A 註腳 1–3（引文 ×1） |
| A42 | 研究紀錄新 fact 30 | 換回後可能再換；說明中心「建議」先編輯前一則訊息 | C | H Note（引文 ×1）；原文是 “Editing your previous message before retrying often helps”，「建議」略強，只在紀錄、不在正文 |
| A43 | 研究紀錄新 fact 44 | Latest models 列 Fable 5.1、Opus 5.5、Sonnet 5、Haiku 4.5 | C | P（引文 ×1，位置在 “Latest models”（9,354）與 “Legacy models”（11,311）之間） |

### B. 第一輪 CONFIRMED 的隨機三分之一（43；括號是第一輪的編號）

| # | 位置 | 主張 | 判定 | 依據 |
| --- | --- | --- | --- | --- |
| B1（#3） | title | 20% 是降價 | C | A；新標題寫成「牌價降 20%」 |
| B2（#6） | description | Claude 5.5 家族第一個 | C | A “the first model in our new Claude 5.5 family” |
| B3（#8） | description | 40% 估計、20%／60% 官方降價 | C | A |
| B4（#13） | 第一段 | 公告頁沒有提到任何地區或國家限制 | C | A 正文（“We’re introducing…” 到頁尾導覽前，37,940 字）詞界比對 Taiwan／country／countries／region／regions／regional 0 次 |
| B5（#17） | 第二段 | 2026 年 9 月 26 日查核 | C | `checked_on` 四處一致 |
| B6（#18） | 第二段 | 讀了公告、說明中心、定價頁、System Card | C | sources[]（WRITER 規格要求的第二段句型） |
| B7（#20） | summary 1 | 9/22、Claude 5.5 家族第一個 | C | A |
| B8（#22） | summary 2 | 40% 是預設設定、一般工作負載下的估計 | C | A |
| B9（#24） | summary 2 | 60% 是快取讀取牌價降幅 | C | A “Cache reads … $0.20 per million tokens, 60% less than Opus 5.” |
| B10（#31） | summary 5 | 評測時開著正式防護 | C | A “evaluated with its production safeguards enabled”（AutomationBench 也開著，只是沒有備援） |
| B11（#32） | summary 5 | 評測分數差距越來越「不能反映」實際差異 | CH | A “benchmark margins have become a less reliable guide to real-world differences”，比較級 →「越來越難以反映」 |
| B12（#33） | 一-1 | Anthropic 表示多數工作達 Fable 5.1 水準 | C | A “on most work”，已歸因 |
| B13（#37） | 一-1 | claude-opus-5-5 | C | A |
| B14（#38） | 一-2 | 不能關掉思考 | C | A |
| B15（#39） | 一-2 | API 與 claude.ai 都只能開著思考 | C | S |
| B16（#40） | 一-2 | claude.ai 只開放 18 歲以上 | C | S §4.2 |
| B17（#41） | 一-3 | 呼籲放慢前沿之後的第一個發布 | C | A “our first release since we called for pacing the frontier” |
| B18（#49） | 二-2 | 輸入輸出比 Opus 5 少 20% | C | A |
| B19（#51） | 二-2 | 快取讀取少 60% | C | A |
| B20（#53） | 二-3 | Anthropic 表示輸出快 30% 以上 | C | A “more than 30% faster” |
| B21（#54） | 二-3 | Fast mode 在 Claude Code 與 Claude Platform | C | A |
| B22（#57） | 表 | 40%｜估計｜預設設定、一般工作負載 | C | A |
| B23（#63） | 三-1 | 比較表 Opus Free 標 No（截至查核日） | C | P；「這個系列…欄位」精簡 |
| B24（#68） | 三-2 | 每個方案五小時滾動上限 | C | P FAQ “Every plan has usage limits that reset on a rolling five-hour session window” |
| B25（#74） | 三-3 | 訂閱使用者一次 rate limit reset，可保留、自選時間 | C | A “a rate limit reset, which you can now save and use whenever you choose” |
| B26（#75） | 三-3 | Settings > Usage 看用量 | C | P FAQ |
| B27（#78） | 三-3 | Max 每月 100 美元起 | C | P “From $100 Per month” |
| B28（#80） | 圖 caption | 9/22 推出、四件事、查核日 9/26 | C | A；與研究紀錄 `diagram.caption` 相同 |
| B29（#86） | 四-2 | 病毒學、毒理學、分子設計這類兩用請求轉 Opus 5 | C | H “areas like” →「這類」 |
| B30（#88） | 四-2 | 前沿 LLM 開發分類器只有 Opus 5.5 | C | H “apply only to Opus 5.5” |
| B31（#89） | 四-2 | 少數相關能力轉 Opus 5 | C | H “a small set of capabilities” |
| B32（#91） | 四-2 | 蒸餾類直接擋下、不轉 | C | H、S |
| B33（#93） | 四-3 | 換模型會出現通知、回覆標出模型 | C | H “you'll see a notice … labeled with the model that answered” |
| B34（#106） | 四-4 | 多數資安任務轉 Opus 4.8 | C | A “most cybersecurity tasks will be re-routed to Opus 4.8” |
| B35（#107） | 四-4 | 生物、蒸餾、前沿 LLM 開發在輸出前被擋仍計費，其他不收 | C | H Usage and billing；本輪精簡「這三類」「照樣」 |
| B36（#109） | 五-1 | 評測差距越來越「不能反映」實際差異 | CH | 同 B11 →「難以反映」 |
| B37（#110） | 五-1 | 自己使用時與 Fable 5.1 差距比分數小 | C | A “narrower than these scores suggest” |
| B38（#113） | 五-2 | 開著正式防護評測 | C | A |
| B39（#117） | 五-2 | 更難判斷真實環境行為 | C | A “challenges our ability to assess how it will act in the vast variety of real-world settings” |
| B40（#128） | FAQ 1 | 公告沒寫哪些方案選得到 Opus 5.5 | C | A：方案名只出現在用量上限那一句；picker／selector／default model 0 次 |
| B41（#129） | FAQ 2 | 三個數字的定義與條件 | C | A |
| B42（#130） | FAQ 2 | 40% 來自每 token 較便宜＋token 較少 | C | A “costs less per token … uses fewer tokens per task, which nets out to a 40% drop” |
| B43（#132） | FAQ 3 | 未來幾週、沒有確切日期 | C | A |

### C. 限定詞與小標回掃（30）

| # | 位置 | 主張 | 判定 | 依據 |
| --- | --- | --- | --- | --- |
| C1 | 四-1 | 「較高風險」的攻擊性資安請求 | CH | H “when our cyber classifiers flag potentially higher-risk offensive cybersecurity requests” →「疑似較高風險」 |
| C2 | FAQ 5 | 同上 | CH | 同上 |
| C3 | FAQ 7 | 差距越來越「不能反映」 | CH | 同 B11 |
| C4 | 三-1 | 「而且是會更動的頁面」 | CH | P “Price and plans are subject to change” →「而且頁面可能更動」（也省 1 字） |
| C5 | callout | 「這張表會隨時間更動」 | CH | 同上 →「可能隨時間更動」 |
| C6 | 三-3 | 「前一節的 API 價格都未含稅，且可能調整」 | NF | P 的 “Prices shown don’t include applicable tax. Price and plans are subject to change…” 只在正規化全文第 2,015 字（個人方案卡下）與 5,827 字（Team／Enterprise 卡下）；API 區（9,354 字起）“tax” 0 次；A 也 0 次 → 刪 API 部分 |
| C7 | 三-3 | 方案價格未含稅、可能調整 | C | P（個人方案卡下那一處） |
| C8 | description | 「付費方案用量上限提高的範圍」 | CH | A 只提高 five-hour usage limits；與第一輪改過的標題同一個範圍 →「五小時上限」 |
| C9 | 二-3 | 速度「最高」2.5 倍 | C | A “up to 2.5x speed” |
| C10 | 表 | Fast mode「最高」加速 | C | 同上 |
| C11 | 二-3 | 快 30%「以上」 | C | A “more than 30% faster” |
| C12 | 五-2 | 「可能」拉低分數 | C | A “This likely reduces”（「可能」比 likely 弱，方向安全） |
| C13 | 四-2 | 一般 AI／ML 開發與寫程式「大多」不受影響 | C | S “will not impact the vast majority”（H 是 shouldn't） |
| C14 | FAQ 4 | 「多數」資安任務轉 Opus 4.8 | C | A “most” |
| C15 | 五-2 | 「常常」懷疑 | C | A “often suspects” |
| C16 | FAQ 1 | 「也可能之後更動」 | C | P |
| C17 | callout | 40% 帶預設設定、一般工作負載 | C | A |
| C18 | 四-4 | CVP「未來幾週」才擴大 | C | A |
| C19 | 一-1 | 「舉例包括」AWS、Google Cloud、Azure | C | A “including” |
| C20 | 四-1 | 「例如」產生 exploit、滲透測試 | C | H “such as”（第三項 binary-based vulnerability scanning 沒寫，「例如」撐得住） |
| C21 | 四-1 | 掃描原始碼弱點、分類資安問題「這類」 | C | H “including” |
| C22 | 二-2 | 快取讀取占大部分成本（「官方說明」） | C | A 括號句，已歸因 |
| C23 | 四-3 | 選單停在較弱的模型 | C | H “for the rest of the conversation” |
| C24 | 五-3 | 相當「或更好」 | C | A “matches or beats” |
| C25 | FAQ 6 | 需要客戶自己「選擇並設定」備援 | C | H “must opt into and configure the fallbacks” |
| C26 | 小標 1 | 9 月 22 日…新家族先在所有平台上線 | C | A Availability；「先」指家族第一個模型，同節第三段寫 Sonnet／Haiku 5.5 還沒推出 |
| C27 | 小標 2 | 三個數字各自量的是什麼 | C | A |
| C28 | 小標 3 | 方案比較表與用量上限 | C | P、A |
| C29 | 小標 4 | 為什麼對話會突然換成別的模型 | C | H |
| C30 | 小標 5 | 誰測的、測的時候開著什麼 | C | A 表下註與註腳 1–3 |

### D. 協調者裁定帶出的句子（6）

| # | 位置 | 主張 | 判定 | 依據 |
| --- | --- | --- | --- | --- |
| D1 | title | 整句換成新標題 | CH（裁定 1） | 見下三條 |
| D2 | title | 牌價降 20% | C | A “Input and output tokens are $4 and $20 per million, 20% less than Opus 5.”（快取寫入 6.25→5 也是 20%；快取讀取的 60% 在 description、summary、正文分開寫） |
| D3 | title | 付費方案五小時上限提高 | C | A；P 的 Enterprise 是 “$20 per seat per month plus usage”，按席次計費，所以「付費方案」撐得住，完整清單在第一段、summary 3、第三節第二段 |
| D4 | title | 40% 是 Anthropic 的成本估計 | C | A “Our tests show that at default settings it will cost 40% less” |
| D5 | 五-2 | 「防護介入時資安由 Opus 4.8、生物與前沿 LLM 由 Opus 5 完成」對所有評測 | CH（裁定 2） | A 表下註是通則，註腳 2 是例外 |
| D6 | 五-2 | （AutomationBench 除外：它沒開備援，防護介入就算失敗） | C | A 註腳 2 “These runs were performed without fallback models, so safeguard interventions were considered failures” |

### E. 結尾連結（2）

| # | 位置 | 主張 | 判定 | 依據 |
| --- | --- | --- | --- | --- |
| E1 | 連結 1 | 2026 年 AI 新聞總整理：1 月至 9 月的重點與生活應用 | C | 目標包 zh-TW title 逐字相同；locales zh-TW、en、ja、ko、zh-CN |
| E2 | 連結 2 | Claude Opus 5 推出：一般工作使用者值得注意哪些改變？ | C | 同上；與 DELTA-4-8 第 5 條表一致 |

## 改掉的地方（原文 → 改成，出處）

事實修正（12）：

1. title：「Claude Opus 5.5 推出：40% 是成本估計、20% 是降價，付費方案五小時上限也提高」→「Claude Opus 5.5 推出：牌價降 20%、付費方案五小時上限提高，40% 是 Anthropic 的成本估計」（裁定 1；https://www.anthropic.com/claude-opus-5-5）。研究紀錄 `title` 同步。
2. description：「並整理付費方案用量上限提高的範圍」→「並整理付費方案五小時上限提高的範圍」（https://www.anthropic.com/claude-opus-5-5）。
3. summary 5：「越來越不能反映實際差異」→「越來越難以反映實際差異」（A “a less reliable guide”）。
4. 第五節第一段：同上。
5. FAQ 7：同上。研究紀錄 fact 14 同改並註明原文。
6. 第三節第一段：「而且是會更動的頁面」→「而且頁面可能更動」（https://claude.com/pricing “subject to change”）。
7. callout：「這張表會隨時間更動」→「這張表可能隨時間更動」（同上）。
8. 第三節第三段：「以上定價與前一節的 API 價格都未含稅，且可能調整。」→「以上價格未含稅，且可能調整。」（https://claude.com/pricing：註記只在方案價格卡下方）。研究紀錄 fact 40、`not_said`、`must_not_write` 同改。
9. 第四節第一段：「較高風險的攻擊性資安請求」→「疑似較高風險的攻擊性資安請求」（https://support.claude.com/en/articles/16049681-… “potentially higher-risk”）。研究紀錄 fact 24 同改。
10. FAQ 5：同上。
11. 第五節第二段：「生物與前沿 LLM 開發題由 Opus 5 完成，Anthropic 說這可能拉低 Opus 5.5 在評測表上的分數。」→「生物與前沿 LLM 開發題由 Opus 5 完成（AutomationBench 除外：它沒開備援，防護介入就算失敗），Anthropic 說這可能拉低 Opus 5.5 的評測分數。」（裁定 2；A 註腳 2）。研究紀錄 fact 15 加註這個例外。
12. FAQ 3：「截至 2026 年 9 月 26 日查核還沒有，claude.com 定價頁 API 價格區列出的最新模型仍是 Sonnet 5 與 Haiku 4.5。」→「截至 2026 年 9 月 26 日查核還沒有。」（FAQ ⊆ 正文）。

騰字數（裁定 3；只刪重複敘述與贅字，沒有刪任何限定詞或但書）：

- 第一段、第三節第一段：「把「Opus」這個系列列在 Free 欄位標示」→「把「Opus」系列列在 Free 欄標示」（與 summary 3、callout 的寫法一致），各 −3。
- 第二節第一段：「官方說明它的來源是兩件事相加——每個 token」→「官方說明它的來源是每個 token」（下一句就列出兩件事；「相加」本來也不準，原文是 nets out），−7。
- 第四節第四段：「開發這三類請求……仍會照樣計費」→「開發類請求……仍會計費」，−4。
- 第 8 條刪掉沒有來源的 API 稅務說法也省下 13 字。段落 2,994 → 2,997。

研究紀錄（7 處加 `second_round`）：`title`；fact 14（難以反映，註明原文）；fact 15（AutomationBench 例外）；fact 24（potentially）；fact 40、`not_said` 第 4 條、`must_not_write` 第 14 條（「未含稅」只寫在訂閱方案價格上）。**研究紀錄本身錯的三處**（fact 40、not_said、must_not_write 把稅務註記套到 API 價格）已同改，下一輪不要改回。

## 查過而且正確的部分（重點）

- 第一輪 22 處修正全部對得上原文，沒有一處要改回（FAQ 3 多加的半句屬實，只因 FAQ ⊆ 正文而刪）；第一輪自己新寫的句子（四-3 的換回但書、五-3 的 System Card 歸因、一-3 與 FAQ 3 的「截至查核日還沒推出」、FAQ 7 的 Zapier）逐句對過。
- 三個數字：40%（“at default settings … on typical workloads”）、20%（“$4 and $20 per million, 20% less”）、60%（“$0.20 per million tokens, 60% less”）在新標題、description、summary、正文、表、FAQ、callout 都分開寫。
- summary ⊆ 正文：五句都對得到正文（summary 5 的「Zapier 自行公布」正文寫「Zapier…自己跑的評測」，A 註腳 2 是 “run and reported by Zapier”，兩者都撐得住）。FAQ ⊆ 正文：FAQ 3 修正後七題都對得到；FAQ 4 的「找錯、修錯」例子見待決事項。圖上數字 40%、20%、60%、5.5 都在正文（checker 也過）。
- 否定句：「沒有提到地區或國家」（A 詞界 0 次）、「公告沒有寫提高多少、是不是永久」「清單沒有 Free」（A）、「沒有寫版本號」（P）、「還不在 CVP」（H）、「不會轉給其他模型」（H、S）、「截至查核日還沒推出」（A、P，另四頁今天 0 次）、「不是 Anthropic 跑的」（A 註腳 1）、「沒開備援」（A 註腳 2）都指得到 sources[]。
- 日期：slug、`news_date`、第一段都是 2026-09-22；公告頁首與 System Card 封面都印 September 22, 2026，沒有時刻（DELTA-4-8 第 4 條）。`checked_on` 在內容包四條、研究紀錄、第二段、表格 caption、圖說一致。
- 界線：topics 是 ai／software／ai-news，沒有 finance；只有一個 info callout；沒有訂閱、購買、升級建議；沒有推定台灣可用；廠商宣稱都有歸因（Fable 5.1 水準、40% 估計、30% 以上、提示注入、快取占比）；沒有 GPT-6 Sol／Luna，也沒有連同批文章；沒有攻擊手法細節。

## 讀者優先檢查

- 「本文」：0 處。
- 開頭段歸因 1 個（「公告頁沒有提到…」）；定價頁那句是在說表上印了什麼，不算歸因。
- 正文段歸因都 ≤2：第一節第三段、第五節第二段、第五節第三段各 2 個，其餘 0–1 個。
- description 163 字，以「（2026 年 9 月查證）」結尾；title、description、summary 沒有選題清點（description 的「三個數字」後面直接列出三個數）。
- 第二段「讀了 Anthropic 的公告頁……」是 `agents/ai/WRITER.md` 要求的第二段句型，沒有動。

## 留給協調者

1. 標題剛好 60／60 字、段落 2,997／3,000 字；之後任何補字都要等量精簡。
2. 標題的「付費方案」是 Pro、Max、Team 與按席次計費 Enterprise 的簡稱；定價頁的 Enterprise 本身就是按席次加用量計費，所以沒改，正文與 summary 都列了完整清單。
3. FAQ 4 的「一般軟體開發流程裡找錯、修錯」出自公告，正文第四節第一段的例子是說明中心的「掃描原始碼弱點、分類資安問題」；主張相同、例子不同，沒改。要嚴格照「FAQ ⊆ 正文」可以把 FAQ 4 的例子換成正文那兩個。
4. 公告頁 “all of which fall back to another model transparently” 與說明中心、System Card 的蒸餾類直接擋下仍然矛盾；照裁定 4 不重開。
5. 研究紀錄 `sourcing_notes` 仍把定價頁稅務註記叫「頁尾」，實際在兩個方案區的價格卡下方；那段是敘述，沒改。
6. 活頁面：說明中心 16049681（自印 Updated yesterday）、定價頁、Sonnet／Haiku 5.5 與 CVP 擴大，發布當天照 `live_data_warnings` 重讀；若 Sonnet／Haiku 5.5 已上線，第一節第三段與 FAQ 3 要改。

## 自檢輸出（原樣）

```
OK ai-news-claude-opus-55-20260922 zh-TW paragraphs 2997
check exit=0
```

```
ai-news-claude-opus-55-20260922
  warning: raw_internal_url: zh-TW: 2 article link(s) as raw URLs; run `pack_cli relink` so they become article inlines that follow the target's publication
  error: image_missing: zh-TW: /guides/ai-news-claude-opus-55-20260922/hero.jpg
  error: image_missing: zh-TW: /guides/ai-news-claude-opus-55-20260922/diagram-1.svg
1 entries checked
lint exit=1
```

```
TOTAL: 60 FAILURES: 0
```

工具與紀錄：`_tools/ai-news-claude-opus-55-20260922/fc2_fetch.sh`、`fc2_norm.py`、`fc2_quotes.py`、`fc2_edit.py`、`fc2_second_round.json`、`fc2_fix_record.py`、`fc2_fix_record2.py`；log 在同目錄 `fc2_check_before.log`、`fc2_check_after.log`、`fc2_lint.log`、`fc2_quotes_before.log`、`fc2_quotes_after.log`、`fc2_edit.log`、`fc2_fix_record.log`；原始抓檔在 `_raw/ai-news-claude-opus-55-20260922/round2/`。
