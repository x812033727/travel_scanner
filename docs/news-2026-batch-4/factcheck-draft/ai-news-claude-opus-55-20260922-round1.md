# 查核第一輪：ai-news-claude-opus-55-20260922

查核者：獨立查核代理（第一輪，claude-opus-5-5），2026-09-26（台北）。規格：`FACTCHECK-48.md`、`docs/news-2026-batch-4/agents/ai/FACTCHECK.md`、DELTA-4-8 全文、DELTA-4-7 第 3、4、10、11、14、16 條、DELTA-4-5、BRIEF.md 十二種錯誤型態。

## 摘要

- 主張 158 條：CONFIRMED 129、CHANGED 24、NOT FOUND（改寫或刪）4、OUT OF SCOPE 1。
- 事實修正 22 處（內容包 20 個替換、牽動 28 條主張），另有 3 處純精簡（段落原本 2,980／3,000，補但書要空間）；研究紀錄 4 處修正加 3 條新 verified_facts 與 `factcheck` 欄。
- 最重的五處：
  1. 標題「付費方案用量上限也提高」→「付費方案五小時上限也提高」：公告只提高 five-hour usage limits，付費方案另有每週上限，舊標題會被讀成全部上限都提高。
  2. FAQ 7「評測表裡其他公司模型的分數是那家公司自己公布的」：只有 Terminal-Bench 4.0（GPT-6 Astra、GPT-5.6 Sol）與 Terminal-Bench-Science（GPT-6 Astra）是 OpenAI 自報；AutomationBench 的 OpenAI 型號分數來自 Zapier 的公開排行榜，其餘列公告沒註明。「合作夥伴」改成 Zapier。
  3. 提示注入段：「退步」與「已緩解」出自 System Card，原稿寫「Anthropic 也承認…Anthropic 說」，改成 System Card，同時把該段歸因從 3 個降到 2 個；「每種情境（寫程式、…）」補回 including（「包括」）。
  4. 方案比較表那句在第一段、summary、callout 沒有查核日（研究紀錄明令不可省）；callout 的「只有定價頁……」是排他說法，刪掉「只有」並補日期。
  5. 限定詞：說明中心的資安轉換是 may fall back（正文、FAQ、summary 三處補「可能」）；公告的 “We see signs that” 補「跡象」；表格 Fast mode「限 Claude Code 與 Claude Platform」改成「提供」（公告沒寫 only）；生命科學驗證方案的「今天」是 9 月 22 日，改「從公告當天起」；「所以多數資安任務轉給 Opus 4.8」是自己加的因果，改成並列。
- 指派訊息點名的五件事：三個數字在標題、summary、正文、表、FAQ、callout 都分開（正文第一節那句 40% 補「估計」與「條件見下一節」）；歸因逐一對頁；方案可用性只照定價頁「Opus」系列列並帶查核日；Cyber 照說明中心（not currently available in CVP）、蒸餾照說明中心與 System Card（blocked outright）；被刪的只有快取寫入價格與外部評估者名稱（允許），另外找到一個被刪的但書（換回 Opus 5.5 後、原請求還在對話裡時可能再被換掉），已補回；Sonnet 5.5／Haiku 5.5 截至台北 22:39 仍未上線（news、sitemap、blog、models overview、定價頁都沒有），「還沒推出」保留，但改成截至查核日的狀態並在 FAQ 指到定價頁。
- 自檢：`check_article.py` → `OK ai-news-claude-opus-55-20260922 zh-TW paragraphs 2994`（exit 0）；`pack_cli lint` 只有 `image_missing` ×2 與 `raw_internal_url`（exit 1，預期內）；verbatim_quote 60 條（4 sources + 56 facts）對我自己的正規化全文全部找到。
- 結論：`needs_second_round`（事實修正超過十處，而且第四、五節有第一輪自己寫進去、沒人查過的句子）。

## 重抓結果

| 來源 | HTTP | bytes（落地） | 落地 URL | body |
| --- | --- | --- | --- | --- |
| https://www.anthropic.com/claude-opus-5-5 | 200 | 619,967 | 同 | 正文；與研究代理檔案逐位元組相同 |
| https://support.claude.com/en/articles/16049681-… | 200 | 365,182 | 同 | 正文（Intercom，Updated yesterday）；位元組不同、正規化全文相同 |
| https://claude.com/pricing | 200 | 1,171,532 | 同 | 正文；位元組不同、正規化全文相同 |
| https://anthropic.com/claude-opus-5-5-system-card | 200 | 17,795,106 | www-cdn.anthropic.com/…/Claude%20Opus%205.5%20System%20Card.pdf | PDF 230 頁；逐位元組相同，pypdf 重抽 |
| https://www.anthropic.com/news（只查 Sonnet／Haiku 5.5） | 200 | 459,343 | 同 | 最新一則 Sep 23（enzyme），無 5.5 小型號 |
| https://www.anthropic.com/sitemap.xml（同上） | 200 | 69,048 | 同 | 537 個 loc，有 claude-opus-5-5、無 sonnet／haiku-5-5 |
| https://claude.com/blog（同上） | 200 | 805,184 | 同 | 最新 September 25, 2026，無 Sonnet／Haiku 5.5 |
| https://platform.claude.com/docs/en/models/overview（同上） | 200 | 392,248 | 同 | 現役：Fable 5.1、Opus 5.5、Sonnet 5、Haiku 4.5 |

抓取時間 2026-09-26T14:29–14:39Z（台北 22:29–22:39），UA `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)`，同主機間隔 ≥1.5 秒，紀錄在 `_raw/ai-news-claude-opus-55-20260922/round1/fetch-log.tsv`。後四頁只用來反駁「Sonnet／Haiku 5.5 已上線」，不撐文章任何一句；文章的「截至查核日還沒推出」撐在 sources[] 的定價頁（API 價格區 Latest models 列 Sonnet 5、Haiku 4.5）與公告（will follow in the coming weeks）。

## 主張逐條

C＝CONFIRMED，CH＝CHANGED，NF＝NOT FOUND（改寫／刪），OS＝OUT OF SCOPE。出處縮寫：A＝公告頁、H＝說明中心 16049681、P＝定價頁、S＝System Card。

| # | 位置 | 主張 | 判定 | 依據 |
| --- | --- | --- | --- | --- |
| 1 | title | Claude Opus 5.5 推出 | C | A |
| 2 | title | 40% 是成本估計 | C | A “Our tests show that at default settings it will cost 40% less” |
| 3 | title | 20% 是降價 | C | A “$4 and $20 per million, 20% less than Opus 5” |
| 4 | title | 付費方案用量上限也提高 | CH | A 只提高 “five-hour usage limits”；P 付費方案另有每週上限 → 「五小時上限」 |
| 5 | description | 9 月 22 日推出 | C | A 頁首 September 22, 2026 |
| 6 | description | Claude 5.5 家族第一個 | C | A |
| 7 | description | 公告沒有列出地區限制 | C | A 詞界比對 Taiwan／country／countries／region(s) 0 次（頁尾導覽的 Availability／Regional compliance 不算正文） |
| 8 | description | 40% 估計、20%／60% 官方降價 | C | A |
| 9 | description | 句尾（2026 年 9 月查證） | C | 讀者優先規則 |
| 10 | 第一段 | 9 月 22 日推出 | C | A |
| 11 | 第一段 | 新 Claude 5.5 家族第一個 | C | A |
| 12 | 第一段 | 公告頁只印日期、沒有寫時刻 | C（刪） | A 屬實，但是查證紀律（DELTA-4-7 第 14 條），為騰字數刪去；日期本身不變 |
| 13 | 第一段 | 沒有提到任何地區或國家限制 | C | 同 #7 |
| 14 | 第一段 | 提高 Pro、Max、Team、按席次 Enterprise 的五小時上限 | C | A “Pro, Max, Team, and seat-based Enterprise plans” |
| 15 | 第一段 | 多一次用量重置 | C | A “a rate limit reset” |
| 16 | 第一段 | 定價頁比較表 Opus 系列 Free 標 No | CH | P 屬實；補「截至查核日」（研究紀錄 unverified_or_excluded：不可省查核日） |
| 17 | 第二段 | 2026 年 9 月 26 日查核 | C | checked_on 四處一致 |
| 18 | 第二段 | 讀了公告、說明中心、定價頁、System Card | C | sources[] |
| 19 | 第二段 | 本站沒有實測、不提供訂閱建議 | OS | 編輯聲明 |
| 20 | summary 1 | 9/22、Claude 5.5 家族第一個 | C | A |
| 21 | summary 1 | 公告沒有列出地區或國家限制 | C | 同 #7 |
| 22 | summary 2 | 40% 是預設設定、一般工作負載下的估計 | C | A |
| 23 | summary 2 | 20% 是輸入輸出牌價降幅 | C | A |
| 24 | summary 2 | 60% 是快取讀取牌價降幅 | C | A |
| 25 | summary 3 | 比較表 Opus Free 標 No | CH | P；補「截至 9 月 26 日」與「系列」 |
| 26 | summary 3 | Pro、Max、Team 等付費方案提高五小時上限 | CH | A；「等」改成完整清單「與按席次計費的 Enterprise」 |
| 27 | summary 3 | 公告沒有寫提高多少或是否開放 Free | CH | A 清單本來就沒有 Free；「是否開放 Free」語意不明（像在說 Opus 5.5），改「清單裡也沒有 Free」 |
| 28 | summary 4 | 分類器依四類把對話轉給 Opus 4.8 或 Opus 5 | CH | H：蒸餾類不轉、直接擋；資安是 may fall back → 「資安類可能轉給 Opus 4.8，生物與前沿 LLM 開發類轉給 Opus 5，蒸餾類則…直接擋下」 |
| 29 | summary 4 | 蒸餾類直接擋下、不轉其他模型 | C | H “Distillation blocks don't fall back to another model, and the request is blocked outright.”；S “no fallback model” |
| 30 | summary 5 | 評測包含 OpenAI 與 Zapier 自行公布的數字 | C | A 註腳 1、2 |
| 31 | summary 5 | 評測時開著正式防護 | C | A |
| 32 | summary 5 | 評測分數差距越來越不能反映實際差異 | C | A “benchmark margins have become a less reliable guide to real-world differences”（意譯可接受，四處一致） |
| 33 | 一-1 | Anthropic 表示：多數工作達 Fable 5.1 水準 | C | A（廠商說法，已歸因） |
| 34 | 一-1 | 執行成本比 Opus 5 少 40% | CH | A 導言原句無條件，但同頁限定「at default settings… on typical workloads」，must_not_write 不准單寫；補「估計」「（條件見下一節）」 |
| 35 | 一-1 | 所有平台上線，舉例包括 AWS、Google Cloud、Azure | C | A “including”，文章用「舉例包括」 |
| 36 | 一-1 | 這段沒有提到訂閱方案或國家 | C | A Availability 段兩句 |
| 37 | 一-1 | Claude Platform 用 claude-opus-5-5 | C | A |
| 38 | 一-2 | 不能關掉思考 | C | A “no longer available with “thinking” mode switched off” |
| 39 | 一-2 | API 與 claude.ai 上都只能開著思考 | C | S “On both API and claude.ai , Claude Opus 5.5 is only available with thinking enabled.”（與 #38 合併成一句，精簡） |
| 40 | 一-2 | claude.ai 只開放 18 歲以上 | C | S §4.2 |
| 41 | 一-3 | 呼籲放慢前沿之後的第一個發布 | C | A |
| 42 | 一-3 | Sonnet／Haiku 5.5「未來幾週」、沒有日期 | C | A “will follow in the coming weeks” |
| 43 | 一-3 | Sonnet／Haiku 5.5 還沒推出 | CH | 原句掛在「Anthropic 表示」下，但「還沒」是 9/26 的狀態；今天重查 news、sitemap、blog、models overview、定價頁都沒有；改成「公告寫『未來幾週』推出、沒有給日期，截至查核日還沒推出」，否定句撐在 P（Latest models：Sonnet 5、Haiku 4.5），研究紀錄新增一條 |
| 44 | 二-1 | 40% 是 Anthropic 自己測出的估計，條件預設設定與一般工作負載 | C | A |
| 45 | 二-1 | 不是牌價降幅 | C | A |
| 46 | 二-1 | 每個 token 較便宜加上每個任務 token 較少 | C | A |
| 47 | 二-1 | 淨算出 40% | C | A “nets out to a 40% drop in costs”（刪去重複的「兩者相加」，精簡） |
| 48 | 二-2 | 輸入／輸出 4／20 美元 | C | A |
| 49 | 二-2 | 比 Opus 5 少 20% | C | A |
| 50 | 二-2 | 快取讀取 0.20 美元 | C | A |
| 51 | 二-2 | 少 60% | C | A |
| 52 | 二-2 | 官方說明快取讀取占代理與寫程式成本大部分 | C | A 括號句 |
| 53 | 二-3 | Anthropic 表示輸出快 30% 以上 | C | A “more than 30% faster” |
| 54 | 二-3 | Fast mode 在 Claude Code 與 Claude Platform | C | A |
| 55 | 二-3 | 最高 2.5 倍 | C | A “up to 2.5x” |
| 56 | 二-3 | 8／40 美元 | C | A |
| 57 | 表 | 40%｜估計｜預設設定、一般工作負載 | C | A |
| 58 | 表 | 20%｜4／20 對 5／25 | C | A 價格表 |
| 59 | 表 | 60%｜0.20 對 0.50 | C | A 價格表 |
| 60 | 表 | 2.5 倍｜「限」Claude Code 與 Claude Platform | CH | A 只寫 “is also available in”，沒寫 only（platform 文件另寫 API only，互相不一致）→「Claude Code 與 Claude Platform 提供」 |
| 61 | 表 | 8／40 美元 | C | A |
| 62 | 表 caption | 整理自 9/22 公告、查核日 9/26 | C | A |
| 63 | 三-1 | 比較表 Opus Free 標 No（截至查核日） | C | P `<th scope="row">Opus</th>` No／Yes／Yes／Yes |
| 64 | 三-1 | Pro、Max 5x、Max 20x 標 Yes | C | P |
| 65 | 三-1 | Team 與兩種 Enterprise 標 Yes | C | P |
| 66 | 三-1 | 系列名、沒有版本號 | C | P |
| 67 | 三-1 | 會更動的頁面 | C | P “Price and plans are subject to change” |
| 68 | 三-2 | 每個方案五小時滾動上限 | C | P FAQ |
| 69 | 三-2 | 付費方案另有每週上限 | C | P |
| 70 | 三-2 | 網頁、桌面、手機、Claude Code 共用額度 | C | P |
| 71 | 三-2 | 這次提高的方案清單 | C | A |
| 72 | 三-2 | 公告沒寫提高多少、是否永久 | C | A |
| 73 | 三-2 | 清單沒有 Free | C | A |
| 74 | 三-3 | 訂閱使用者一次 rate limit reset，可保留、自選時間 | C | A |
| 75 | 三-3 | Settings > Usage 看用量 | C | P FAQ |
| 76 | 三-3 | Pro 年繳每月 17 美元（一次 200 美元） | C | P |
| 77 | 三-3 | 月繳 20 美元 | C | P |
| 78 | 三-3 | Max 每月 100 美元起 | C | P |
| 79 | 三-3 | 未含稅、可能調整 | C | P 頁尾 |
| 80 | 圖 caption | 9/22 推出、四件事、查核日 9/26 | C | A |
| 81 | 四-1 | 說明中心：分類器看模型讀到的所有內容 | C | H |
| 82 | 四-1 | 包括記憶、連接器、搜尋結果、檔案 | C | H |
| 83 | 四-1 | 高風險攻擊性資安請求「會」轉給 Opus 4.8 | CH | H “may fall back to Opus 4.8” → 「可能會」 |
| 84 | 四-1 | 例如 exploit、滲透測試 | C | H “such as”，文章有「例如」 |
| 85 | 四-1 | 掃描原始碼弱點、分類資安問題仍可用 | C | H |
| 86 | 四-2 | 病毒學、毒理學、分子設計等兩用請求轉 Opus 5 | C | H “areas like”，文章有「這類」 |
| 87 | 四-2 | 日常健康問題（看懂檢驗報告…） | CH | H “including” → 補「例如」 |
| 88 | 四-2 | 前沿 LLM 開發分類器只有 Opus 5.5 | C | H |
| 89 | 四-2 | 少數能力轉 Opus 5 | C | H |
| 90 | 四-2 | 一般 AI／ML 開發與寫程式大多不受影響 | C | S “will not impact the vast majority”（H 是 shouldn't） |
| 91 | 四-2 | 蒸餾類直接擋下、不轉 | C | H、S |
| 92 | 四-2 | 請它解釋理由不受影響 | C | H |
| 93 | 四-3 | 換模型會出現通知 | C | H |
| 94 | 四-3 | 回覆標出模型 | C | H |
| 95 | 四-3 | 選單停在較弱模型 | C | H “for the rest of the conversation” |
| 96 | 四-3 | 可以自己換回來 | CH | H 屬實，但同頁 Note：原請求還在對話裡時可能再被換掉（may）→ 補回這個但書；研究紀錄新增一條 |
| 97 | 四-3 | Config 裡的「MODEL 與 OUTPUT」 | CH | H 原字串 “Config > MODEL & OUTPUT”（一個選單名，不是兩個）→ MODEL & OUTPUT |
| 98 | 四-3 | 關掉「切換被標記訊息時的模型」 | NF | 引號裡是自譯的介面字串，來源沒有；研究紀錄要求介面字串照英文。正文改成敘述「訊息被標記時換模型的開關」，FAQ 6 放英文原字串 |
| 99 | 四-3 | 關掉後暫停對話而不換模型 | C | H |
| 100 | 四-3 | API 預設不開、要自行設定 | C | H |
| 101 | 四-4 | 經審核的組織「今天」就能申請 LSVP | CH | A 的 today＝9 月 22 日 → 「從公告當天起」 |
| 102 | 四-4 | 用 Opus 5.5 做生物研究 | C | A |
| 103 | 四-4 | CVP「未來幾週」擴大 | C | A “In the coming weeks we will also be expanding access” |
| 104 | 四-4 | 截至查核日 Opus 5.5 不在 CVP | C | H “Note: Opus 5.5 isn't currently available in the Cyber Verification Program.” |
| 105 | 四-4 | 「所以」多數資安任務轉 Opus 4.8 | NF | 來源沒有這個因果：轉 4.8 是對所有使用者的防護（A、S），不是因為不在 CVP → 改成分號並列 |
| 106 | 四-4 | 多數資安任務轉 Opus 4.8 | C | A “most cybersecurity tasks will be re-routed to Opus 4.8” |
| 107 | 四-4 | 生物、蒸餾、前沿 LLM 開發在輸出前被擋仍計費 | C | H |
| 108 | 四-4 | 其他類別輸出前被擋不收費 | C | H |
| 109 | 五-1 | Anthropic 寫評測差距越來越不能反映實際差異 | C | A（同 #32） |
| 110 | 五-1 | 自己使用時與 Fable 5.1 差距比分數小 | C | A |
| 111 | 五-1 | Terminal-Bench 4.0 的 GPT-6 Astra、GPT-5.6 Sol 是 OpenAI 自報 | C | A 註腳 1 |
| 112 | 五-1 | AutomationBench 的 Opus 5.5 是 Zapier 搶先測 | C | A 註腳 2 |
| 113 | 五-2 | 開著正式防護評測 | C | A |
| 114 | 五-2 | 介入時資安由 4.8、生物與前沿 LLM 由 Opus 5 完成 | C | A（AutomationBench 例外：沒開備援、介入算失敗，見待決事項） |
| 115 | 五-2 | Anthropic 說可能拉低分數 | C | A “This likely reduces” |
| 116 | 五-2 | 看到 Opus 5.5 常常懷疑自己被評估 | CH | A “We see signs that…” → 補「的跡象」；研究紀錄同改 |
| 117 | 五-2 | 更難判斷真實環境行為 | C | A |
| 118 | 五-3 | 每種情境（寫程式、工具使用、電腦操作、網頁瀏覽） | CH | A “in every setting we tested, including …” → 「包括」；研究紀錄同改 |
| 119 | 五-3 | Anthropic 表示提示注入相當或更好 | C | A（S 也寫 “performed similarly or better”） |
| 120 | 五-3 | 「Anthropic 也承認」貼上文字的退步 | CH | 出處是 S 摘要 “However, it is more likely than previous models to follow malicious instructions in text that a user pastes into their own prompt” → 「System Card 則列出一個退步」 |
| 121 | 五-3 | 文字中「被人埋入」的惡意指令 | C | S §6.5.1 “instructions planted by someone else” |
| 122 | 五-3 | 貼別人寫的文字＝讓對方控制部分提示 | C | S §6.5.1 |
| 123 | 五-3 | 「Anthropic 說」最終版本加產品改動已緩解 | CH | S §6.5.1 “The ﬁnal snapshot…has mitigated this issue.” → 併入 System Card 的歸因 |
| 124 | 五-3 | 正在加上移除看不見字元、標記貼上文字 | C | S “We are also adding product changes…” |
| 125 | FAQ 1 | 比較表 Opus Free 標 No（截至 9/26） | C | P |
| 126 | FAQ 1 | Pro、Max 5x、Max 20x Yes | C | P |
| 127 | FAQ 1 | 系列名、可能更動 | C | P |
| 128 | FAQ 1 | 公告沒寫哪些方案選得到 | C | A（詞界比對 Free 0 次；Availability 段無方案） |
| 129 | FAQ 2 | 三個數字的定義與條件 | C | A |
| 130 | FAQ 2 | 40% 來自每 token 較便宜＋token 較少 | C | A |
| 131 | FAQ 3 | 還沒有 | CH | 補「截至 2026 年 9 月 26 日查核」與 P 的 Latest models（Sonnet 5、Haiku 4.5） |
| 132 | FAQ 3 | 未來幾週、沒有確切日期 | C | A |
| 133 | FAQ 4 | 多數資安任務轉 4.8 | C | A |
| 134 | FAQ 4 | 說明中心截至 9/26：不在 CVP | C | H |
| 135 | FAQ 4 | 「未來幾週」擴大（句子掛在說明中心下） | CH | H 沒有「未來幾週」，那是 A → 「公告則寫」 |
| 136 | FAQ 4 | 例行找錯、修錯仍可用 | C | A “identify and fix bugs … routine software development lifecycle” |
| 137 | FAQ 5 | 分類器看記憶、連接器、搜尋結果、檔案 | C | H |
| 138 | FAQ 5 | 資安請求轉 4.8 | CH | H “may” → 「可能」 |
| 139 | FAQ 5 | 生物、前沿 LLM 轉 Opus 5 | C | H |
| 140 | FAQ 5 | 蒸餾直接擋下 | C | H |
| 141 | FAQ 5 | 通知與標示 | C | H |
| 142 | FAQ 6 | Config 裡的 MODEL 與 OUTPUT、「切換被標記訊息時的模型」 | CH | H 原字串 → MODEL & OUTPUT、「Switch models when a message is flagged」（訊息被標記時切換模型） |
| 143 | FAQ 6 | 關掉後暫停對話 | C | H |
| 144 | FAQ 6 | API 預設不開 | C | H |
| 145 | FAQ 7 | 其他公司模型的分數是那家公司自己公布的 | CH | A：只有 Terminal-Bench 4.0 與 Terminal-Bench-Science 的 OpenAI 型號是 OpenAI 自報；AutomationBench 的 OpenAI 型號來自 Zapier 公開排行榜（“Results for Opus 5, GPT-5.6 Sol, and GPT-6 Astra come from Zapier’s public leaderboard.”）；其餘列沒註明 → 「OpenAI 模型的部分分數（例如 Terminal-Bench 4.0）」；研究紀錄新增一條 |
| 146 | FAQ 7 | 「合作夥伴」搶先使用期間自行跑 | NF | A 只寫 “Zapier’s own evaluation during early access”，沒說是合作夥伴 → 「Zapier」 |
| 147 | FAQ 7 | Anthropic 寫差距越來越不能反映實際差異 | C | A |
| 148 | callout 標題 | 三件事 | C | 內文對應 |
| 149 | callout | 40%／20%／60% 定義 | C | A |
| 150 | callout | 公告本身沒寫 Free 能不能用 | C | A |
| 151 | callout | 「只有」定價頁比較表標 No | NF | 排他說法（BRIEF 第 2 型「唯一」），來源撐不住 → 刪「只有」，補「截至 9 月 26 日」與「系列」 |
| 152 | callout | 規則與怎麼關掉可到說明中心查 | C | H |
| 153 | callout | 9/26 查核、沒有實測 | C | checked_on |
| 154 | 結尾連結 1 | 「2026 年 AI 新聞總整理：1 月至 9 月的重點與生活應用」 | C | 目標包 zh-TW title 逐字相同；五語齊（en、ja、ko、zh-CN、zh-TW） |
| 155 | 結尾連結 2 | 「Claude Opus 5 推出：一般工作使用者值得注意哪些改變？」 | C | 目標包 zh-TW title 逐字相同；五語齊；與 DELTA-4-8 第 5 條表一致 |
| 156 | hero_label | 估計與降價分開看 | C | A |
| 157 | diagram | 四格（成本估計／官方降價／付費方案「用量上限提高、未寫幅度」／幾週內才到） | CH | 第三格同 #4 → 「五小時上限提高、未寫幅度」（研究紀錄）；其餘三格 C |
| 158 | sources[] | 四條標題、網址、checked_on 2026-09-26 | C | 四條今天都讀到正文；System Card 標題對 PDF 封面，定價頁標題對 `<title>` Plans & Pricing |

## 改掉的地方（原文 → 改成，出處）

1. title：「付費方案用量上限也提高」→「付費方案五小時上限也提高」。A：“we’re increasing five-hour usage limits on Pro, Max, Team, and seat-based Enterprise plans”；P：“paid plans add weekly limits on top”。研究紀錄 `title` 同步。
2. 第一段：「不過 claude.com 定價頁的方案比較表…」→「不過截至查核日，claude.com 定價頁的方案比較表…」。P 是活頁面；研究紀錄 unverified_or_excluded 明令不可省查核日。
3. summary 3：「claude.com 定價頁的方案比較表把「Opus」列在 Free 欄標示「No」，Pro、Max、Team 等付費方案這次提高了五小時用量上限，但公告沒有寫提高多少或是否開放 Free。」→「截至 9 月 26 日，claude.com 定價頁的方案比較表把「Opus」系列列在 Free 欄標示「No」；Pro、Max、Team 與按席次計費的 Enterprise 方案這次提高了五小時用量上限，公告沒有寫提高多少，清單裡也沒有 Free。」（A、P）
4. summary 4：「分類器會依資安、生物、前沿 LLM 開發與蒸餾四類把對話轉給 Opus 4.8 或 Opus 5，其中蒸餾類…」→「分類器觸發時，資安類可能轉給 Opus 4.8，生物與前沿 LLM 開發類轉給 Opus 5，蒸餾類則會被直接擋下、不會轉給其他模型。」（H）
5. 第一節第一段：「執行成本比 Opus 5 少 40%」→「估計執行成本比 Opus 5 少 40%（條件見下一節）」（A；must_not_write）。
6. 第一節第三段：「Claude Sonnet 5.5 與 Claude Haiku 5.5 還沒推出，原文是「未來幾週」，沒有給日期。」→「Claude Sonnet 5.5 與 Claude Haiku 5.5 公告寫「未來幾週」推出、沒有給日期，截至查核日還沒推出。」（A、P）
7. 表格：「限 Claude Code 與 Claude Platform，8／40 美元」→「Claude Code 與 Claude Platform 提供，8／40 美元」（A “is also available in”）。
8. 第四節第一段：「會從 Opus 5 或 Opus 5.5 轉給 Opus 4.8」→「可能會從…」（H “may fall back”）。
9. 第四節第二段：「（看懂檢驗報告…）」→「（例如看懂檢驗報告…）」（H “including”）。
10. 第四節第三段：「可以自己從選單換回來。」→「可以自己從選單換回來，但原請求還在對話裡時可能再被換掉。」（H Note：“the same safeguards may cause Claude to fall back again if your original request is still part of the conversation”）。
11. 第四節第三段：「Config 裡的 MODEL 與 OUTPUT）關掉「切換被標記訊息時的模型」這個選項」→「Config 裡的 MODEL & OUTPUT）關掉訊息被標記時換模型的開關」（H 原字串）。
12. 第四節第四段：「經審核的組織今天就能申請」→「經審核的組織從公告當天起就能申請」（A 的 today 是 9/22）。
13. 第四節第四段：「…還不在這個計畫裡，所以多數資安任務目前會轉給 Opus 4.8。」→「…還不在這個計畫裡；多數資安任務目前會轉給 Opus 4.8。」（A、H 都沒有這個因果）。
14. 第五節第二段：「它看到 Opus 5.5 常常懷疑自己正在被評估，」→「…正在被評估的跡象，」（A “We see signs that”）。研究紀錄同改。
15. 第五節第三段：「每種情境（寫程式、…）」→「每種情境（包括寫程式、…）」（A “including”）。研究紀錄同改。
16. 第五節第三段：「但也承認一個退步：…去做——貼進別人寫的文字，等於讓那個人控制了一部分提示；Anthropic 說最終版本加上一些產品端的改動已經緩解這個問題，並正在加上…」→「System Card 則列出一個退步：…去做，最終版本加上一些產品端的改動已經緩解這個問題，並正在加上…。貼進別人寫的文字，等於讓那個人控制了一部分提示。」（S 摘要與 §6.5.1；該段歸因 3→2）。
17. FAQ 3：「還沒有。」→「截至 2026 年 9 月 26 日查核還沒有，claude.com 定價頁 API 價格區列出的最新模型仍是 Sonnet 5 與 Haiku 4.5。」（P）
18. FAQ 4：「這個計畫要在「未來幾週」才擴大」（掛在說明中心下）→「公告則寫這個計畫要在「未來幾週」才擴大」（A；H 沒有這句）。
19. FAQ 5：「較高風險的攻擊性資安請求轉給 Opus 4.8」→「…可能轉給 Opus 4.8」（H）。
20. FAQ 6：「MODEL 與 OUTPUT」「切換被標記訊息時的模型」→「MODEL & OUTPUT」「Switch models when a message is flagged」（訊息被標記時切換模型）（H）。
21. FAQ 7：「評測表裡其他公司模型的分數是那家公司自己公布的…其中一項評測的 Opus 5.5 分數是合作夥伴…」→「評測表裡 OpenAI 模型的部分分數（例如 Terminal-Bench 4.0）是 OpenAI 自己公布的…AutomationBench 的 Opus 5.5 分數是 Zapier…」（A 註腳 1–3）。研究紀錄新增一條。
22. callout：「公告本身沒寫，只有 claude.com 定價頁的方案比較表把「Opus」列在 Free 欄標示「No」」→「公告本身沒寫；claude.com 定價頁的方案比較表截至 9 月 26 日把「Opus」系列列在 Free 欄標示「No」」（P）。

精簡（不是事實修正，沒有刪任何限定詞）：第一段刪「公告頁只印日期、沒有寫時刻，也」；第一節第二段把兩個同義句併成「Opus 5.5 在 API 與 claude.ai 上都不能把「思考」模式關掉」；第二節第一段刪重複的「兩者相加」。段落 2,980 → 2,994。

研究紀錄：`title`；`diagram.nodes[2]` 改「五小時上限提高、未寫幅度」；兩條 fact 補回 signs、including；新增三條 verified_facts（P Latest models、H 換回後可能再換、A AutomationBench 其他模型來自 Zapier 排行榜），三條引文都對今天的正規化全文比對過；檔尾加 `factcheck`。**研究紀錄本身錯的兩處**（signs、including）已同改，第二輪不要改回。

## 查過而且正確的部分（重點）

- 日期：公告頁首、news 清單、System Card 封面都是 September 22, 2026，沒有時刻；slug、news_date、第一段一致（DELTA-4-8 第 4 條）。
- 三個數字：40%（“at default settings … on typical workloads”）、20%（“$4 and $20 per million, 20% less”）、60%（“Cache reads … $0.20 per million tokens, 60% less”）在標題、summary、正文、表、FAQ、callout 都分開寫。
- 方案：P 的比較表 Opus 列 Free No／Pro Yes／Max 5x Yes／Max 20x Yes，Team／Enterprise 兩種都 Yes；文章每次都寫成「Opus 系列」並帶查核日，沒有「Anthropic 宣布 Free 不能用」。
- 歸因對頁：「Anthropic 表示」的四處（Fable 5.1 水準與平台、放慢前沿、輸出速度、提示注入的改善）都在 A；說明中心的句子掛 H；思考與 18 歲在 S（無歸因的直述，可以）；退步與緩解改掛 S。
- 否定句：「沒有提到地區或國家」（A 詞界比對 0 次）、「公告沒有寫提高多少、是不是永久」「清單沒有 Free」（A）、「表上沒有版本號」（P）、「不在 CVP」（H）、「不會轉給其他模型」（H、S）、「還沒推出」（A、P）都指得到 sources[]。
- 沒有購買建議、推薦式比價、GPT-6 Sol／Luna 比較或同批連結；評測比較都寫成 Anthropic 表上、OpenAI 或 Zapier 自報。

## 讀者優先檢查

- 「本文」：0 處。
- 開頭段歸因：0 個（第一段只有「公告頁沒有提到…」一個出處指引）。
- 正文段歸因上限 2：修正前第五節第三段 3 個（Anthropic 表示／也承認／Anthropic 說），修正後 2 個；其餘段 0–2 個。
- description 以「（2026 年 9 月查證）」結尾，120–200 字（162）。
- title／description／summary 沒有選題清點；description 的「三個數字」後面直接列出三個數，不算。
- 仍帶查證語氣、沒動的兩處：第二段「讀了 Anthropic 的公告頁…」（查核日句型）、第一節第一段「這段沒有提到訂閱方案或國家」（對讀者有用）。第一段「只印日期、沒有寫時刻」已刪。

## 留給協調者

1. 公告頁 “all of which fall back to another model transparently” 與 H、S 的蒸餾「直接擋下」矛盾；文章照 H、S。來源自相矛盾，發布當天若公告改字再看。
2. AutomationBench 沒開備援模型、防護介入算失敗（A 註腳 2），第五節第二段的「介入時由 Opus 4.8／Opus 5 完成」對這一項不適用；段落 2,994／3,000，沒加。要加得先精簡別處。
3. 標題前半「40% 是成本估計、20% 是降價」偏簡略，但沒說錯，照指示沒重寫；要不要改成「40% 是估計省下的成本」由協調者決定。
4. 第二輪只剩 6 個字的段落空間；補句要等量精簡敘述，不可刪但書。
5. 活頁面（H 自印 Updated yesterday、P）與 Sonnet／Haiku 5.5、CVP 擴大，發布當天照研究紀錄 `live_data_warnings` 重讀；若 Sonnet／Haiku 5.5 已上線，第一節第三段與 FAQ 3 要改。

## 自檢輸出（原樣）

```
OK ai-news-claude-opus-55-20260922 zh-TW paragraphs 2994
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

工具與紀錄：`_tools/ai-news-claude-opus-55-20260922/fc1_fetch.sh`、`fc1_norm.py`、`fc1_quotes.py`、`fc1_edit.py`、`fc1_len.py`、`fc1_factcheck.json`；log 在同目錄 `fc1_check_before.log`、`fc1_check_after.log`、`fc1_lint.log`、`fc1_quotes_after.log`、`fc1_edit.log`；原始抓檔在 `_raw/ai-news-claude-opus-55-20260922/round1/`。
