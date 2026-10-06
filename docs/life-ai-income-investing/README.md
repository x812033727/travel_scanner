# 生活分享批次：AI 賺錢與投資 × AI（12 篇，zh-TW）

票：`tasks/open/2026-10-05-life-ai-income-investing-batch.md`。站主 2026-10-05 以
maplefeather.com 的 AI 應用頁為參考，指出本站缺「用 AI 賺錢／副業」與「投資理財、AI 概念股」兩類題材。

這一批只寫 zh-TW（AI 與財經系列的既有慣例：662 篇 AI 文章中 535 篇只有 zh-TW），
其他語系之後走 skill `article-localization`。

## 與既有規格不同的地方（這份文件優先）

1. **新子主題 `ai-income`**（`ai` 底下，migration 0125）。第 1–6 篇用它；`pack_ingest` 認
   `LIFE_SEED_SUBTOPICS`，所以 dry-run 會過。
2. **第 7、9–12 篇帶 `finance`**，照 `docs/life-finance-series-brief.md` 全部規則：不點名個股、個別 ETF、
   個別基金、個別投顧或平台；不給買賣建議、不寫行情數字；最後一個區塊是第 5 節的免責 callout
   （「不是投資建議」六字不能改，中括號填「費用、稅負與交易規則」，查證日 2026-10-05）。
   這幾篇同時帶 `ai`，所以也會出現在 `/ai` 專區。
3. **第 8 篇帶 `ai` 與 `tech`，不帶 `finance`**：講產業結構，不講投資。可以寫產業分層與技術名詞，
   **不寫任何公司名**（台廠、美廠都不寫），不寫「受惠」「概念股」「營收成長」這類投資語言。
4. **第 1–6 篇不保證收入。** 不寫「月入 X 萬」「被動收入」「躺著賺」；報價與收入只寫計算方法與
   平台公開的抽成、費率；舉例用「假設」並寫明是假設。平台名（518 外包網、Tasker 出任務、Upwork、
   Fiverr、Adobe Stock、Shutterstock、Gumroad、OpenAI GPT Store 等）可以點名，因為講的是規則，不是推薦。
5. 查證日一律是實際打開官方頁的日期（今天是 2026-10-05）。

## 清單

| # | slug | 標題（可微調） | topics | 切角與必寫 | 可連的站內文章（完整網址照抄） |
|---|---|---|---|---|---|
| 1 | `ai-freelance-getting-started` | AI 接案入門：哪些案子適合用 AI、在哪裡接、報價怎麼算 | ai, tutorial, ai-income | 適合／不適合用 AI 的案型；台灣與國際接案平台的抽成與收款規則（官網）；工時制與件計制的報價算法（用假設數字示範）；交付前的人工檢查 | ai-tools-choose-by-task、ai-hallucination-fact-check、website-income-models |
| 2 | `ai-freelance-client-confidentiality` | 接案用 AI 的保密與責任：客戶資料、合約條款與揭露 | ai, ai-income | 客戶資料能不能丟進 AI（各家消費版與商用版的資料使用政策，官網）；保密協議與著作權歸屬條款；要不要向客戶揭露用了 AI；個資法的基本義務 | ai-at-work-policy-checklist、ai-and-copyright-law-taiwan、ai-image-copyright-taiwan |
| 3 | `ai-translation-subtitle-freelance` | 翻譯與字幕接案搭配 AI：譯後編修流程、品質檢查與計價 | ai, tutorial, ai-income | 機器翻譯譯後編修（MTPE）是什麼；字幕的時間軸與字數規範（以平台公開規範為準）；品質檢查清單；按字、按分鐘計價的算法（假設數字） | ai-video-subtitles-translation、whisper-local-transcription、immersive-translate-guide |
| 4 | `selling-ai-digital-products` | 賣 AI 做的數位商品：圖庫投稿、模板與 GPTs 的平台規則 | ai, ai-income | Adobe Stock、Shutterstock 等對生成式 AI 投稿的規定；Gumroad 等平台的抽成；GPT Store 的分潤現況與地區限制（官網）；標示與授權 | ai-image-copyright-taiwan、licensed-assets-workflow、ai-image-tools-overview-2026 |
| 5 | `ai-content-side-business-costs` | 用 AI 經營內容副業：部落格、電子報與短影音的成本與時間 | ai, ai-income | 三種形式各自的固定成本（主機、電子報工具、AI 訂閱，官網價格）與每週時間；AI 能省哪一段、不能省哪一段；平台對 AI 內容的政策（Google 搜尋、YouTube 標示） | website-income-models、email-newsletter-planning、ai-for-youtube-creators、ai-free-vs-paid-plans-2026 |
| 6 | `ai-money-making-course-red-flags` | 「AI 自動賺錢」課程與話術：怎麼辨識誇大收入與付費陷阱 | ai, daily, ai-income | 常見話術類型；台灣消保與公平交易法規對誇大不實廣告的規範、通訊交易解除權與例外（主管機關頁）；報案與申訴管道 | ai-scams-deepfake-taiwan、online-banking-security、warning-account-prevention |
| 7 | `ai-concept-stocks-explained` | 「AI 概念股」是什麼：題材標籤、營收占比與公開資訊怎麼查 | finance, ai, investing | 「概念股」是媒體與市場標籤，不是官方分類；證交所產業分類與指數的差別；怎麼在公開資訊觀測站查營收組成與重大訊息（只講方法）；題材集中的風險。**不點名任何公司** | finance-glossary-50-terms、personal-finance-first-steps、online-banking-security |
| 8 | `ai-server-supply-chain-layers` | AI 伺服器怎麼組成：晶片、記憶體、封裝、組裝、散熱與電力 | ai, tech | 一台 AI 伺服器從晶片到機櫃的分層；HBM、先進封裝、液冷、電力密度是什麼（引用官方技術文件或國際組織報告）；資料中心用電的公開數據（IEA 等）。**不寫公司名、不寫投資語言** | local-ai-gpu-buying-guide、local-llm-hardware-requirements、ai-model-tiers-explained |
| 9 | `thematic-etf-index-rules` | 主題型 ETF 怎麼讀：AI 與半導體指數的編製規則、集中度與費用 | finance, ai, investing | 主題指數怎麼選成分股（公開說明書與指數編製規則）；權重上限、集中度、再平衡頻率；內扣費用與追蹤誤差在哪裡查（投信投顧公會、證交所）。**不點名任何 ETF 或指數商品** | finance-glossary-50-terms、personal-finance-first-steps |
| 10 | `ai-financial-report-reading` | 用 AI 讀財報與法說會：提示詞、對照原文與常見錯誤 | finance, ai, investing | 從公開資訊觀測站下載財報與法說會資料（方法）；用 AI 摘要時的提示詞範本；逐項對照原文的檢查法；AI 常見錯誤（單位、期間、合併與個體） | ai-hallucination-fact-check、ai-pdf-tools-summarize-translate、finance-glossary-50-terms |
| 11 | `robo-advisor-taiwan-explained` | 機器人理財是什麼：台灣的制度、費用結構與限制 | finance, investing | 金管會對「自動化投資顧問服務」的規範（作業要點、投信投顧公會規範）；KYC 問卷、再平衡、費用結構類型；能做與不能做的事。**不點名業者** | personal-finance-first-steps、finance-glossary-50-terms |
| 12 | `ai-trading-bot-claims` | 「AI 選股」「AI 交易機器人」的宣傳怎麼看：回測、績效宣稱與合法業者 | finance, ai, investing | 回測與實際績效的差別；投信投顧法對未經許可提供投資建議的規範；怎麼查合法業者（金管會、投信投顧公會名單）；與 AI 投資詐騙的分界 | ai-scams-deepfake-taiwan、online-banking-security、warning-account-prevention |

站內連結的完整網址是 `https://mokaair.com/zh-TW/life/<slug>`。本批 12 篇之間也可以互連。

## 圖

每篇自繪 `hero.svg` 與至少一張 `diagram-1.svg`。財經篇的圖不能是績效曲線、由低到高的長條或金幣堆；
第 8 篇的圖是分層結構圖。

## 流程

撰稿（一篇一位）→ 查核第一輪（換人，逐條對官方來源）→ 第二輪（再換人：法遵與讀者優先，
重查第一輪改過的項目與隨機三分之一）→ 機械關卡（dry-run、`intake_check.py`、渲染看圖）
→ 協調者 ingest、`pack_cli lint --kind life`、pytest、逐篇讀過法遵。
