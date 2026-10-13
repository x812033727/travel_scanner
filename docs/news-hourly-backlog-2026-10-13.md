# AI 每小時自動新聞：2026-10-13 待審與需重寫名冊

## 範圍與證據界線

- 2026-10-13 13:46（Asia/Taipei）的正式站 `/zh-TW/admin/news` 基線：**待審查 46、需重寫／失敗 24、已發布 596、已退件 936**。本頁固定記錄這 70 個候選 ID；來源刊登日期不是候選所屬批次的證明。
- 2026-10-13 14:26（Asia/Taipei）UI 即時數字：**待審查 39、需重寫 18、已發布 601、已退件 946**。這是全站流動佇列，不能以基線數字相減當作本名冊的完成數。
- 2026-10-13 14:33（Asia/Taipei）UI 再盤點：**待審查 38、需重寫 15、已發布 603、已退件 949**。此間 AEMA／Citrix 發布、三筆舊預告退件；仍需按固定候選 ID 算終態。
- 2026-10-13 14:41（Asia/Taipei）UI 再盤點：**待審查 36、需重寫 15、已發布 603、已退件 951**。固定基線 70 筆中，此時可讀回 7 筆發布、12 筆退件；其餘 36 筆待審及 15 筆需重寫，合計 51 筆未有終態。這是固定 ID 的分類，不能以全站計數變化取代。
- 2026-10-13 14:50（Asia/Taipei）UI 再盤點：**待審查 34、需重寫 15、已發布 604、已退件 952**。Anthropic ART 經重新查核由 AI 判斷發布；Meta Connect 直播稿人工退件。固定名冊目前 8 筆發布、13 筆退件、49 筆未有終態；前述數量按候選 ID 判斷，非僅用全站差額推算。
- 2026-10-13 14:53（Asia/Taipei）UI 再盤點：**待審查 31、需重寫 15、已發布 604、已退件 955**。Apollo、Orchard、9/26 Decrypt 監管回顧三筆逐一退件並讀回，固定名冊目前 8 筆發布、16 筆退件、46 筆未有終態。
- 站主本次明確授權處理整個 46＋24 名冊，包含先前 10/07、10/10 批次；工作整合至既有 draft [PR #1480](https://github.com/x812033727/travel_scanner/pull/1480)。舊工作樹與舊票不在本票 scope，不能據此替它們結案。
- 下表的「來源變更」表示自動查核偵測到快照差異，**不等於**正文事實已變；需要比對保存的原快照、現在的正文、Guide 說法及來源可讀性。`manual_review`／`shadow_review` 是保留審查；`needs_redraft`／`failed` 是不同的重寫或故障路徑。不能用無旗標 backfill、整批 retry、單憑列表「已發布」或 `exit 0` 充當逐篇驗收。
- 「已送重新查核」只代表 UI 已建立後續工作，應讀回候選、run、Guide 五語、稽核及公開頁面的終態。本文記的是已觀察到的節點，沒有把未確認的公開頁面或語系算成完成。
- 正式站 SSH `plink` 連線在本次環境被自動審核阻擋；下列處理依後台 UI 及來源頁執行。不要改用另一種 SSH 方式繞過阻擋，也不要在付費請求結果不明時重送。

## 本次有稽核讀回的變更

| 候選 | 已執行／證據 | 待確認 |
| --- | --- | --- |
| `3e41d63a-28fb-4e2f-b96c-43831dfd2de9` Claude Sonnet 5.5 | `news_slug_conflict`；與已公開的 [2026-09-28 五語專文](https://mokaair.com/zh-TW/life/ai-news-claude-sonnet-55-20260928) 相同公告及主題。後台填原因退件，候選讀回「已退件」及稽核「人工決定：退件」。 | 舊公開文的 zh-TW、zh-CN、ko 頁曾讀回；en 未讀回、ja 當時 429，因此不可宣稱本次重新驗完五語。 |
| `4343e0fb-1806-4d6c-817b-440fa9e9eb2d` Morning Minute／Drake | 晚出的 Decrypt 摘要與同事件較完整的 [Decrypt 正文](https://decrypt.co/380363/ethereum-researcher-ai-break-encryption-before-quantum) 重複，原稿另有查證失敗及無關證據。後台填原因退件，讀回「已退件」及稽核「人工決定：退件」。 | 不代表原始完整來源的候選已公開；另看下列 `b0825f…`。 |
| `eb51db63-3889-4fc8-a713-21ab3175a5db` OpenAI／澳洲 | 原稿只據 9/24 The Verge 初報且 ja 審查未過；[澳洲政府說明](https://www.minister.defence.gov.au/transcripts/2026-09-24/press-conference-sydney)與 [OpenAI 9/28、10/04 更新](https://openai.com/index/how-we-will-do-better-for-australia/)已補各站實際存取、9/10 通知及 Medicare 統計入口與個人醫療系統差異。單語修正不能更新五語事實及候選證據，人工退件並讀回稽核。 | 如重做，需以更新後的一手來源重新立稿、查證；原 Guide 草稿仍在，不是已發文章。 |
| `b0825fb1-44dc-4c96-adab-1fe028f49113` Drake 完整來源 | Guide `f3aa3154-197d-44f8-a97b-ba6cb8573ef5`：修正 zh-TW「與比特幣創造者相關、公鑰已暴露的地址」主詞關係，以及 ja `今年初めに`→`今年に入って`、ko `올해 초`→`올해 들어`。三語各存成未公開草稿版本 2，後台按一次「重新查核」；後續原候選進入「已發布 · 598」清單，詳情有五語前台連結。五語公開頁 H1 均讀回，zh-TW／ja／ko 修正句讀回。 | 補記終態 run／稽核，核對全文與實際發出的 Guide 版本；H1 與指定錯句的讀回尚非全篇逐語驗收。 |
| `5186a9c9-ffb1-4282-ae82-cac3676da1a4` XRP Ledger | Guide `5f97b859-f882-49c0-b994-28bb851f6477`：依 [CoinDesk 報導](https://www.coindesk.com/tech/2026/10/09/xrp-ledger-adds-new-controls-for-banks-stablecoins-and-tokenized-funds) 與 [XRPLF issue](https://github.com/XRPLF/rippled/issues/8534) 修正 zh-TW／ja／ko 表格，明確說明是驗證者換金鑰後，部分伺服器漏算仍在線的驗證者。三語各存成未公開草稿版本 2，後台按一次「重新查核」，初讀「撰稿中／等待重新查核」；後續原候選進入「已發布 · 598」清單，詳情有五語前台連結。五語公開頁 H1 均讀回，zh-TW／ja／ko 修正句也讀回。 | 補記終態 run／稽核，核對全文與實際發出的 Guide 版本；H1 與指定錯句的讀回尚非全篇逐語驗收。 |
| `6384736e-5f57-48cf-a536-87bc77f98615` Falcon ASR | Guide `8c7d01df-f8cf-41c0-a4e1-8255fc097730` 五語各新增有來源說明的 WER／CER 表格（阿拉伯語六組平均 20.92%、阿聯酋方言內部 WER 22.73%／CER 10.19%、英文七組平均 5.74%），移到第 9 區塊、各存未公開草稿版本 3。數值按 [TII 官方文章](https://huggingface.co/blog/tiiuae/falcon-asr) 核對；後台按一次「重新查核」，原候選進入「已發布 · 599」清單，詳情有五語前台連結。zh-TW／zh-CN／en／ko 公開頁讀回 H1、表格與三組數值。 | ja 公開頁本次回傳 429，未能讀回；仍須補記終態 run／稽核、已發 Guide 版本及全篇驗收。 |
| `cf07bd04-7f3f-4b0d-89b9-37a715f1ecc9` Kalshi | 依 [CoinDesk 對 Kalshi 的採訪](https://www.coindesk.com/markets/2026/09/23/kalshi-says-it-is-not-being-investigated-by-the-cftc-over-trading-activity) 將五語標題、摘要與內文中「否認調查」等過度陳述改為有日期的公司說法：9 月 23 日尚未獲 CFTC 聯繫，且當時不認為已有正式審查。五語 Guide `f626dfe7-4701-4c7e-9e06-ecf951fb6e13` 各存草稿版本 2 並送一次重新查核。AI 代審表示稿件可發布，但原候選回到待審，標 `source_content_changed`（CoinDesk 正文與作者頁）及 `source_became_unreadable`（CoinDesk `/markets` 導覽頁）。 | 不能以 AI 代審意見跳過來源閘；先釐清導覽頁如何進入候選證據、是否可安全移除，及原正文差異，再用最新來源重查。不可盲按可能重抓全部來源的按鈕。 |
| `7bea807c-ffa3-44a2-b3be-92aee355e279` Flock | 依 [The Verge 原報導](https://www.theverge.com/policy/1000005/flock-senate-hearing) 將佛州女子的說法、Flock 發言人 Paris Lewbel 的同情與責任反駁並列；明示當時未即時回覆的是 Axon 與 Motorola Solutions，並收窄資安段的資料範圍。Guide `8e29cd15-b8b8-4766-a008-3e0db211fc60` 五語各存草稿版本 3，重新查核後原候選讀回「已發布 · 600」清單；五語公開頁 H1 與 Flock 回應已讀回。 | 仍須核對終態 run／稽核、已發 Guide 版本與全文。 |
| `13c96f09-f6fd-4255-b72c-ebade0fd4a79` XRP Ledger 延期 | 9/26 CoinDesk 只預告 BatchV1_1 最早 10/9 啟用；[XRPL 修正案儀表板](https://xrpldashboard.com/amendments)連結鏈上 EnableAmendment，顯示 10/9 14:47 UTC 在 ledger 107540993 已啟用。原五語草稿仍用未來式。人工以過時退件，讀回稽核與「已退件」。 | 新結果須另以現況立稿，不把舊預告重跑。 |
| `efc90b90-7f0d-41f9-b4a3-2b4f7d59b4b0` Ledger／CryptoBilis | 10/9 Decrypt 初報的同一事件已有本站 [Ledger 72 小時更新](https://mokaair.com/zh-TW/life/crypto-news-ledger-cryptobilis-20261012)與[後續損失調查](https://mokaair.com/zh-TW/life/crypto-news-ledger-cryptobilis-exploit-20261012)；兩篇公開內容讀回。原候選兩次重寫未過且無五語稿，人工以重複／過時退件，讀回稽核。 | 既有兩篇公開內容的全文／五語未在本次重新驗收。 |
| `e4270a94-512c-447e-85b0-9f6d2ecfd657` Google Vids 1080p | 候選引 [Google 9/23 公告](https://blog.google/products-and-platforms/products/workspace/gemini-omni-in-google-vids/)；本站[五語既刊專文](https://mokaair.com/zh-TW/life/ai-news-google-vids-omni-free-20260924)的繁中公開頁已涵蓋免費帳號、1080p、額度與限制。原候選兩次重寫未過且無新事件，人工退件，讀回稽核。 | 不代表已重新驗完既刊專文的五語。 |
| `31ddc338-8cff-4e5c-b647-38de7c7423a7` Gemini coworker agent | 10/8 Decrypt 候選與 [Google Cloud 公告](https://cloud.google.com/blog/products/ai-machine-learning/welcome-to-gemini-at-work-2026)同事件；本站[既刊專文](https://mokaair.com/en/life/ai-news-gemini-agent-20261008)英文公開頁已涵蓋專屬 email、持續儲存與權限。原候選兩次重寫未過，人工以重複退件，讀回稽核。 | 不代表已重新驗完既刊專文的五語。 |
| `ddf85a1f-84b9-4eec-8481-5eb0a94e0157` Meta Audio 眼鏡 | en Guide `4ccc44f1-4023-437f-852a-4d7cfb39605e` v2 已讀回無無據 Muse Charm 段落，單篇重新查核後回到「查核沒通過」。最新查核指出隱私功能應寫未來推出、不能把 Meta Glasses 與 Gen 3 都稱有鏡頭；候選證據仍有作者頁與舊 claim 的依賴。 | 需先獨立處理舊證據／claim，再按 [Meta 官方說明](https://about.fb.com/news/2026/09/introducing-ray-ban-meta-audio-glasses-new-styles-plus-muse/)核五語，不重複盲按重查。 |
| `dcc3116c-dc2f-489e-84cf-79a8ba439ea6` Citrix／Mandiant | 日文 Guide `ed67e2f3-996c-4666-8925-d1e1c3716970` 依 [Google Cloud 原文](https://cloud.google.com/blog/topics/threat-intelligence/defending-against-active-exploitation-of-citrix-netscaler-adc-and-gateway-appliances/)刪無據編輯句、在提示框補回攻擊經 DTLS／UDP 443 傳送，存 ja 草稿 v4。單篇重查後，僅對唯一 Google Cloud 正文按一次「用最新來源重新查核」；新查核又把偵測規則包名稱更正為 `Mandiant Intel Emerging Threats`，事實與五語審查及 Jev 最後一關均通過，原候選讀回「已發布」。[五語公開頁](https://mokaair.com/zh-TW/life/tech-news-citrix-netscaler-zero-day-20260929)各自 H1、正確規則包名稱、DTLS／UDP 443 均讀回，舊錯名未出現。 | 仍須補記終態 run／稽核、已發 Guide 版本及全文逐語驗收。 |
| `e69d8fbc-693b-4beb-90f7-3a6af0cdfcaa` NVIDIA Astra | 唯一[官方正文](https://blogs.nvidia.com/blog/gpus-openai-gpt-6-astra-ultrafast/)現行頁仍支持 Blackwell、API、資格與「最高 8 倍」等主張；繁中 Guide `ca84f575-e62f-4bcf-8459-6ab47de389ef` 修兩處半形逗號並存 v4。僅對該單一來源按一次「用最新來源重新查核」，原候選讀回「已發布」，有五語前台連結；zh-TW／zh-CN／en／ja／ko 公開頁 H1 及「最高 8 倍」均讀回，zh-TW 舊逗號未再出現。 | 仍須補記終態 run／稽核、已發 Guide 版本及全文驗收。 |
| `c5912455-a8cc-4a1e-8b29-33c3725de533` EvoLib | 唯一[Microsoft Research 正文](https://www.microsoft.com/en-us/research/blog/evolib-turning-experience-into-evolving-knowledge/)現行頁仍支持研究主要說法；只對該單一來源按一次「用最新來源重新查核」。新事實查核通過，之後原候選再次回到待審 `source_content_changed`。本地唯讀用正式解析器兩次抓取均 HTTP 200，正文 8073／8140 字與 body hash 不同，差異只在 `How EvoLib Works` 後 `msr-promo` 推廣卡輪替；同解析器精確排除 `msr-promo` 後兩次皆 7818 字、59 元素且 body hash 完全相同。 | [既有動態 widget 修復票](../tasks/open/2026-10-11-exclude-rotating-source-widgets-from-news.md)應補此專屬 fixture 並證明真正正文變更仍被擋；修復部署前不再盲刷。當前後台 UI 無現成來源 config 編輯入口。 |
| `6cbc274d-5837-4550-9008-af21079c6d13` Google Genesis | [Google Cloud 第一方公告](https://cloud.google.com/blog/topics/public-sector/accelerating-frontiers-of-scientific-discovery-40-million-dollar-commitment-genesis-mission/)日期為 7/22；4,000 萬美元是 AI tokens 與雲端額度，而非十月新現金投資。五語稿雖已查核，但作為 10/13 每小時新聞距事件近三個月且無新進展；人工填明確時效理由退件，後台「已退件」與 950 總數讀回。 | 若 DOE 有新的成果或承諾，用當時一手公告另立稿；不把此候選舊文重新查核放行。 |
| `f8830a55-0281-4e55-900a-c067ab4c4fda` Project Suncatcher | [本站已公開同日發射稿](https://mokaair.com/en/life/tech-news-google-project-suncatcher-satellite-20261001)的英文 H1／內文讀回，內容涵蓋 TPU 原型入軌、Planet 合作與實驗目的。原候選標題／摘要仍以同一發射為主，另稱 TechCrunch 標題 1,600 次、內文 1,800 次不一致；但 [TechCrunch 現行原文](https://techcrunch.com/2026/10/01/google-thinks-spacexs-starship-has-to-launch-1600-times-before-space-data-centers-get-off-the-ground/)已明列更正為 1,800 次。人工以重複且更正後失準退件，後台「已退件」與 951 總數讀回。 | 如另做發射成本模型專文，需以 [Google 論文](https://services.google.com/fh/files/misc/suncatcher_paper.pdf)核條件式估算，並與本站既刊新聞區分角度；不能沿用本候選。 |
| `2cb24617-530b-48b1-99c1-44d736c524a4` Anthropic ART | [Anthropic 9/23 一手公告](https://www.anthropic.com/news/claude-discovers-novel-enzyme-system)只說 ART 功能未知、結果為預印本。舊五語 FAQ 都斷稱「目前不是基因編輯工具」，提示框與另一 FAQ 又斷言截至現在沒有獨立同行審查；兩類都超出來源。Guide `65eae343-32fb-4faf-bfe5-6ec88c4febdf` 五語各修正為有日期的來源說法、未知功能及尚待學界評估，各存草稿 v4；填稽核原因送單篇「重新查核」。後台候選隨後讀回「已發布」，新 AI 代審明列功能未知、預印本及學界待驗；韓文 Guide 重載讀回「已發布 · 版本 6」，發布修訂記錄為 14:47:13。 [zh-TW](https://mokaair.com/zh-TW/life/ai-news-anthropic-claude-enzyme-system-art-20260923)、[zh-CN](https://mokaair.com/zh-CN/life/ai-news-anthropic-claude-enzyme-system-art-20260923)、[en](https://mokaair.com/en/life/ai-news-anthropic-claude-enzyme-system-art-20260923)、[ja](https://mokaair.com/ja/life/ai-news-anthropic-claude-enzyme-system-art-20260923)、[ko](https://mokaair.com/ko/life/ai-news-anthropic-claude-enzyme-system-art-20260923) 公開 H1／開頭與重點摘要均讀回。 | 補原生 run ID、五語已發 Guide 版本及全文逐語驗收；目前的公開讀回範圍不是全文查證。 |
| `89156804-f4f3-4f5d-bd02-c9bf671b4e76` Meta Connect 直播稿 | 9/23 [The Verge live blog](https://www.theverge.com/tech/998457/meta-connect-2026-live-blog-mark-zuckerberg-keynote)的候選五語稿，與同批固定總覽 `2ba410eb…` 主角和產品相同，卻另把 `/tech`、`/ai-artificial-intelligence`、`/gadgets` 與作者導覽頁列為「來源」。最新事實查核未通過，含相對日期及對來源未述價格／規格的無據斷言。人工填具體稽核原因退件，候選讀回「已退件」，全站已退件計數 951→952。 | 固定總覽仍需按 [Meta 官方整理](https://about.fb.com/news/2026/09/the-biggest-news-from-connect-2026/)補一手證據、修五語與來源閘；不得把直播稿的退件算成總覽稿已完成。 |
| `d266ad56-b020-4fc0-aada-feae4a1bd8df` Apollo 存款推論 | [CoinDesk 9/28 唯一證據](https://www.coindesk.com/markets/2026/09/28/ai-agents-could-drain-cheap-bank-deposits-apollo-s-torsten-slok-warns)與五語稿均把 1 萬美元 × 3.3%–5% 寫成約 100 美元年息，實際是 330–500 美元；後台來源快照與繁中表格均讀到錯誤。原始 [Apollo 9/27 短文](https://www.apollo.com/institutional/insights-news/insights/daily-spark/is-an-agentic-bank-run-coming)是未來假設，未支持稿內 x402／市場規模延伸。此 9/28 推論到 10/13 每小時新聞已過時，又標 `source_content_changed`；填具體原因退件、候選與 953 計數讀回。 | 若做常青分析，須用一手來源重寫並校正算術；不沿用錯數字及舊來源快照。 |
| `77a835d1-5f8e-4f53-a75d-d657dccbd537` Orchard | 唯一 [Microsoft Research 文章](https://www.microsoft.com/en-us/research/blog/orchard-an-open-framework-for-scalable-agentic-ai/)與後台擷取均明列 8/03 發表，距 10/13 已 71 天，未見候選中的十月新事件；五語稿仍以框架「發布」作新聞，最新事實查核未通過。人工以失時效且查核未過退件，候選與 954 計數讀回。 | 如做常青研究解說，另立稿核適用條件；不可把八月發表當十月即時新聞。 |
| `2c3e35f7-382e-4283-88a5-3483796d36da` Decrypt 監管回顧 | [Decrypt 9/26 報導](https://decrypt.co/379383/how-crypto-stopped-waiting-congress-learned-love-regulators)的五語稿仍含「上週／週四」等相對時間，唯一來源現標 `source_content_changed`；到 10/13 已無即時性，且 10/05 [CFTC 9307-26](https://www.cftc.gov/PressRoom/PressReleases/9307-26)擬議規則事前徵詢後續發展未被舊稿納入。人工以過時及證據未更新退件，候選與 955 計數讀回。 | 9307-26 是 ANPRM、非已生效規則，保留其獨立候選核實，不用本舊回顧替代。 |
| `e0e959d9-3862-4506-bf6b-68c9f860ed07` AEMA／NVIDIA | [NVIDIA 唯一第一方正文](https://blogs.nvidia.com/blog/ai-energy-management-alliance/)現行頁支持 9/16 聯盟成立、Emerald AI／Google／NVIDIA 三創始方、四項併網原則與彈性用電方式；本站 DSX 既刊文是不同事件。原五語稿硬檢與 AI 代審建議均可發布，只卡 `source_content_changed`。留稽核原因後僅按一次「用最新來源重新查核」，後台候選讀回「已發布」，末筆 AI 代審為「發布」，有五語前台連結。zh-TW／zh-CN／en／ja [公開頁](https://mokaair.com/zh-TW/life/tech-news-aema-alliance-20260916) H1 與聯盟三方讀回。 | ko 前台回 429，不能算本次已驗；仍須補終態 run／稽核、已發版本及全文驗收。 |
| `6b846276-450c-4392-9912-a5e51739f359` Evernorth 預告 | 10/1 Decrypt 只預計 10/7 交割、10/8 XRPN 開始交易；[公司 10/9 公告](https://www.nasdaq.com/press-release/evernorth-completes-business-combination-armada-acquisition-corp-ii-2026-10-09)與 [Nasdaq 通知](https://www.nasdaqtrader.com/TraderNews.aspx?id=ECA2026-726)顯示實際 10/9 合併、10/12 交易。本站已公開 [10/12 實際掛牌新聞](https://mokaair.com/zh-TW/life/crypto-news-evernorth-nasdaq-listing-20261012)，zh-TW H1／日期／約 4.73 億枚 XRP 讀回。舊預告人工以重複／過時退件，候選與稽核讀回。 | 新公開稿五語全文未在本次重新驗收。 |
| `068c4856-dea9-4d1b-9dd7-22ac91c6b07c` Pleterski 審訊預告 | 9/29 Decrypt 單篇稿只說「週一」將開始審訊、將自行辯護且日期不清。[10/7 當庭報導](https://globalnews.ca/news/12091683/crypto-king-trial-aiden-pleterski/)已記錄審訊、證人作證及代表律師，並載明不認罪；舊稿時態與主軸已過時。人工退件，候選與稽核讀回，理由明示不推定有罪。 | 若有後續正式法庭紀錄，可另立新稿；舊稿不重跑。 |
| `4c2952b8-c0ee-4ad6-8ce8-fe5defd55d5b` 澳洲聽證邀請預告 | Decrypt 9/28 預告 10/1 聽證；[參院邀請公告](https://cdn.prod.greens.systems/sa/news/media-release/ai-leaders-called-front-senate-inquiry)只能證實曾邀請，候選證據無法證實其後出席／回應。AI 查核亦指出單一二手來源、「首宗」無佐證及草稿其他推論；澳洲政府與 OpenAI 另已更新存取範圍。人工退回舊預告，候選與稽核讀回。 | 不推定 CEO 實際出席與否；若有正式聽證紀錄，另立新稿。 |

本段只描述候選處置與編輯。精確的最新正式站計數應重新查 UI／資料庫，不以 `46 - 已離開列表數` 推算，因為工作期間可能有新候選進入。尚未更動的候選與具體下一步如下。

## 基線 46 筆待審查

| # | 候選 ID／題目 | 基線關卡與下一步 |
| --- | --- | --- |
| 1 | `e25bc5a4-cca4-4e61-bb77-5b1b45243561` CFTC／SEC（CoinDesk） | 候選引用 [CFTC 9307-26](https://www.cftc.gov/PressRoom/PressReleases/9307-26) 的 10/05 ANPRM，官方抓取 `HTTPStatusError`／原生 403；與 #23 同公告，應對照稿件去重。#25 的 9303-26 是另一 FAQ 事件。評論期限是聯邦公報刊登後 60 天，不可直接從 10/05 起算。待既有抓取修復票。 |
| 2 | `2ba410eb-ea90-4de6-bc74-b1db01f195d3` Meta Connect（The Verge） | [The Verge 固定總覽](https://www.theverge.com/tech/998480/meta-connect-2026-biggest-news-announcements)與 #36 直播稿的 Muse Charm、無相機 Ray-Ban Meta 與 VR Glasses 高度重疊；#36 已退件，本站仍無本事件已刊稿的讀回。此稿混入 `/tech` 導覽頁，造成 `source_content_changed`，且查核同樣對價格／細節「報導未載明」的負面斷言提出異議。先對 [Meta 官方整理](https://about.fb.com/news/2026/09/the-biggest-news-from-connect-2026/)核實產品與推出時點、修五語，再解來源閘；不要把導覽頁當證據。 |
| 3 | `2cb24617-530b-48b1-99c1-44d736c524a4` Anthropic 生物學 | 五語 Guide 已修同一兩類無據斷言並送原生單篇重查，後續 AI 代審發布、候選「已發布」，五語公開 H1／開頭／重點摘要已讀回，見上；仍需補 run 與全文驗收。 |
| 4 | `f4602147-6d9d-47a0-899f-bf3eb495089b` THORChain／Bitget | [Bitget 9/25 修正公告](https://www.bitget.com/support/articles/12560603896108)把受影響額修至約 3.875 億美元；[THORChain 機制文件](https://docs.thorchain.org/technical-documentation/technical-deep-dive/security)是整鏈停機而非個別地址凍結。[CoinDesk 9/28 鏈上分析](https://www.coindesk.com/tech/2026/09/28/thorchain-rejects-bitget-request-to-block-hacker-as-usd6-million-moves-to-bitcoin)的 27 筆轉換與另 400 ETH 待處理不可相加稱追回；需逐條核五語與來源快照。 |
| 5 | `ec55a54c-9b7f-46a9-a1ce-294856fb32ac` 量子／Bitcoin／EU | [歐洲監理機關 9/23 原文](https://www.esma.europa.eu/press-news/esma-news/esas-call-vigilance-over-external-dependencies-cyber-threats-and-private)談未來足夠先進量子電腦的潛在風險，未說目前能破解 Bitcoin；約 690 萬枚 BTC 是 CoinDesk 另引 CryptoQuant，非 EU 估計。[歐盟 PQC 路線](https://digital-strategy.ec.europa.eu/en/policies/post-quantum-cryptography)非 Bitcoin 升級期限；核五語歸屬後再處理來源變更。 |
| 6 | `dbda9f17-0127-49a8-8f51-75248ccae17c` RedotPay | [公司 9/28 原文](https://www.redotpay.com/news/weve-received-an-clean-independent-financial-audit-from-a-big-four-firm)稱截至 2025 年底兩年合併財報獲無保留意見，為**可能的未來**上市準備，沒給 IPO 日期或核准；[CoinDesk](https://www.coindesk.com/business/2026/09/28/redotpay-completes-financial-audit-as-it-presses-ahead-with-u-s-ipo-plans)轉述公司否認延後。現存五語草稿僅引 CoinDesk，主軸已限定準備中；仍需對照官方／匿名估值及來源實際正文差異，不直接刷新放行。 |
| 7 | `d0ca3770-3d99-46fc-bed9-5fcb959b78dc` OpenAI 訓練暫停 | The Verge 來源變更；核原始報導 URL、事件與時間線。 |
| 8 | `eb51db63-3889-4fc8-a713-21ab3175a5db` OpenAI／澳洲 agents | 舊稿已因政府與 OpenAI 後續一手公告更新關鍵時序／範圍而人工退件，稽核讀回；如重做需以新事實重新立稿。 |
| 9 | `cf07bd04-7f3f-4b0d-89b9-37a715f1ecc9` Kalshi | 五語已修並重查；目前卡在 CoinDesk 正文／作者頁變動及 `/markets` 導覽頁不可讀，見上。 |
| 10 | `ab3d418f-d812-44ec-88e1-4f9fc6c6a09d` Bitcoin 多頭／駭客 | 來源變更；核來源正文與行情時點、避免沿用過期價格。 |
| 11 | `7bea807c-ffa3-44a2-b3be-92aee355e279` Flock | 五語已補公司回應、澄清其他公司的說法並重新查核；後台已發布且五語 H1／公司回應已讀回，見上。 |
| 12 | `e4e8e98a-83c2-43ef-a332-29704c9045ca` Bitcoin 抗量子成本 | [StarkWare 9/23 公告](https://starkware.co/blog/ai-research-competition-cut-quantum-safe-bitcoin-costs-by-79-in-a-week/)是 GPU 模擬準備成本約 $320→$67；[Yukon 動態看板](https://www.yukon.org/qsb)顯示 $66，非已上鏈實付手續費，且不能保護已露公鑰 UTXO。稿需標時點與假設，看板動態可能讓來源刷新循環。 |
| 13 | `e16c3ba7-bbfd-4323-852a-ef9f7ac83d8d` RockawayX | [Catapult 9/24 一手文章](https://rockawayx.com/insights/introducing-catapult)說透過既有 1.5 億美元以上 DeFi 載具提供流動性，非新募／已全數投出；官方 2030 估值區間 $2T–$30T 與 CoinDesk 專訪 $10T–$20T 不同。需逐條核五語數字與歸屬後再重查。 |
| 14 | `2c3e35f7-382e-4283-88a5-3483796d36da` 加密／監管 | 9/26 Decrypt 回顧已失十月即時性、未納 10/05 CFTC ANPRM 且來源變更；人工退件，見上。 |
| 15 | `6384736e-5f57-48cf-a536-87bc77f98615` Falcon ASR | 五語 `no_table` 已依官方資料補表並重新查核，後台已發布；ja 前台 429，其餘四語表格讀回，見上。 |
| 16 | `e69d8fbc-693b-4beb-90f7-3a6af0cdfcaa` NVIDIA GPT-6 Astra | 唯一官方來源已刷新與重查，後台已發布、五語公開 H1／8 倍主張已讀回，見上。 |
| 17 | `e3f1a1ff-fd77-48bb-873b-94a3ad0c2c69` Altman 評 AI 風險 | The Verge 來源變更；逐句核引述與脈絡。 |
| 18 | `d9deb48d-329b-4f43-9a37-52fb53a243d7` 代幣化股票聯盟 | 來源變更；核參與者、發表時點與具體承諾。 |
| 19 | `f3ff8879-2ed1-44f6-80b8-104a1e9201fb` Ethereum 2030 | 來源變更；核預測為誰的說法、非既成事實。 |
| 20 | `ddf85a1f-84b9-4eec-8481-5eb0a94e0157` Meta 攝影眼鏡 | en 無據段落已修並重查；最新事實查核仍失敗，涉及未來隱私功能、無鏡頭產品及舊證據依賴，見上。 |
| 21 | `e0e959d9-3862-4506-bf6b-68c9f860ed07` Emerald／NVIDIA | 唯一官方正文刷新、全套重查後候選已發布；四語前台 H1 已讀，ko 429，見上。 |
| 22 | `0c72c4f4-500d-45f6-9bc4-d08f7c531bea` Bernie／超級智慧 | fact-check 失敗；Bernie 的法案屬**提案**，非已成法律。五語稿另帶來源不支持的背景敘述；先核法案／原話與時間、刪無據段落，再送單篇查核。 |
| 23 | `3cfdd44b-8774-452b-a534-aa4d6a52caf0` CFTC 官方公告 | [CFTC 9307-26](https://www.cftc.gov/PressRoom/PressReleases/9307-26) 是 10/05 的擬議規則事前徵詢 ANPRM，非已生效規則；與 #1 同公告但不能與 #25 9303-26 FAQ 混成重複。原生抓取 403，先等來源可讀及稿件去重。 |
| 24 | `063d6bdb-9b14-435c-ad5b-8d808ab9d198` Deus X Capital | [公司首頁一手聲明](https://deusx.capital/)說預定 2027-01-31 關閉、返還資產與投資組合並轉往新載具；年化 36.5% 是公司自述。勿寫成已清算或將 2023 年 10 億美元資本當損失；需核來源變動與五語時態。 |
| 25 | `4e323ee2-8a54-40c1-984f-cd55ad3b213b` CFTC FAQs | [CFTC 9303-26](https://www.cftc.gov/PressRoom/PressReleases/9303-26) 是 9/24 登記業者／登記實體加密資產 FAQ 更新，與 #1／#23 的 10/05 ANPRM 不同；原生抓取 403，待來源可讀後核 FAQ 實際範圍。 |
| 26 | `4410c38a-711f-4eb9-a26e-b9867ad4a7a3` NEAR Intents 駭侵 | 來源變更；核事故範圍、金額與時點。 |
| 27 | `b0825fb1-44dc-4c96-adab-1fe028f49113` Drake／加密 | 三語錯句修正、單篇重查，協調者回報在後台已發布清單；需終態與五語公開讀回，見上。 |
| 28 | `c8248683-ab39-4f97-ae2f-05cd7c0dcd7c` Trump／穩定幣 | 來源變更；核權益關係、時間與金額，避免結論超過證據。 |
| 29 | `9c44b4b5-e727-4797-90f9-77445d4a8ace` Samsung／Solana／Sui | [Samsung 10/07 一手公告](https://news.samsung.com/us/samsung-wallet-bring-stablecoin-access-eligible-galaxy-users-us/)是 10 月最後一週**預定**在美國向合資格 Galaxy 用戶推出；8200 萬是相容裝置數、非已開通用戶，向銀行轉帳仍有可變費用。五語草稿的「已上線／零費用全球匯款」需修，且候選只存 CoinDesk 來源；待可稽核追加官方證據後才重查。 |
| 30 | `842bf9c7-bc01-47e7-9590-9a5feae9c872` Franklin Templeton／Bybit | [Bybit 一手公告](https://www.bybit.com/en/press/post/bybit-and-franklin-templeton-form-strategic-collaboration-to-expand-access-to-tokenized-investing-bbc84c1fff30514f669)說目前可用 Benji 貨幣市場基金作抵押的是合資格**機構**客戶、零售產品屬未來計畫；原五語稿泛稱一般用戶或錢包持有人已可用，需修並可稽核追加官方證據後重查。 |
| 31 | `f8830a55-0281-4e55-900a-c067ab4c4fda` Google／SpaceX 1600 | 已因本站同日發射稿重複、TechCrunch 現行更正標題為 1800 而人工退件，見上；未另作成本模型專文。 |
| 32 | `dcc3116c-dc2f-489e-84cf-79a8ba439ea6` Citrix／Google Cloud | ja 指定錯句已修；唯一官方來源刷新、全套審查通過，原候選已發布且五語 H1／規則包名／DTLS／UDP 443 讀回，見上。 |
| 33 | `c5912455-a8cc-4a1e-8b29-33c3725de533` EvoLib | 唯一 Microsoft Research 正文刷新後事實查核通過，但同頁再次顯示 `source_content_changed`；先診斷動態快照，見上。 |
| 34 | `9d72d9ce-cc0f-4d66-88ab-db40946324ce` rogue AI 攻擊 | The Verge fact-check 失敗；現稿把不同的異常／攻擊案例歸為同一事件，超出研究者說法。逐一對回原案例、實證與時間，再決定是否重寫或退件。 |
| 35 | `d266ad56-b020-4fc0-aada-feae4a1bd8df` AI agents 與存款 | 9/28 推論稿過時，唯一來源與五語稿均有 1 萬美元 × 3.3%–5% 年息算錯的實質問題；人工退件，見上。 |
| 36 | `89156804-f4f3-4f5d-bd02-c9bf671b4e76` Meta Connect live blog | 與 #2 固定總覽同事件重複，且持續更新頁與多個導覽／作者頁不足以支持五語稿；人工退件，見上。 |
| 37 | `5186a9c9-ffb1-4282-ae82-cac3676da1a4` XRP Ledger | 三語表格修正、單篇重查，協調者回報在後台已發布清單；需終態與五語公開讀回，見上。 |
| 38 | `7027afef-8836-43e9-b366-fb098bbcaec4` OpenAI 辦公套件 | [OpenAI DevDay 回顧](https://openai.com/index/devday-2026-recap/)顯示 Space／Pages 已推出，Slides 則預計接下來數週推出；現五語稿把 Slides 寫成已上線。需補一手來源並逐語修時態，再處理 TechCrunch 來源變更。 |
| 39 | `6cbc274d-5837-4550-9008-af21079c6d13` Google／Genesis Mission $40M | 官方 7/22 公告到 10/13 已近三個月，無新事件；人工以時效退件，見上。 |
| 40 | `62a29197-da43-4d14-a30d-8a3f8aca341f` OpenAI 數學解題 | TechCrunch 10/08 稿對 10/06 本站[既刊數學專文](https://mokaair.com/zh-TW/life/ai-news-openai-math-manuscripts-20261006)有 AGMAI／驗證的新角度，但原候選僅單一 TechCrunch 來源，719／722 份手稿數字不一致且事實查核失敗；先比對兩篇的獨立新增事實，必要時更新既刊稿，不逕自發布第二篇。 |
| 41 | `2cba0531-7fe5-4739-a2d3-360c13f440b2` Meta Muse Charm | TechCrunch 來源變更，另有兩個導覽 URL `source_became_unreadable`；先辨明原正文，再處理錯誤證據列，不能盲目 refresh。 |
| 42 | `5fcf6a8f-ba95-4dba-b9ed-ff1fec96829a` MoonPay／North Capital | 來源變更，另有導覽／作者頁 `source_became_unreadable`；清理非證據頁並核交易範圍。 |
| 43 | `63cb5134-d2fa-47d3-92bd-f18a3bfaecf8` Offloaded inference | Microsoft fact-check 失敗；核研究結論與適用條件。 |
| 44 | `9ffcd1c1-236a-4bab-8813-f3026e251476` 白宮／加密關係 | 來源變更，導覽／作者頁 `source_became_unreadable`；核責任歸屬與引述，清理來源列。 |
| 45 | `a540117f-7e42-4709-af6f-1ac7366b257d` GitHub 開發者政策 | fact-check 失敗；核政策原文、生效日及適用範圍。 |
| 46 | `77a835d1-5f8e-4f53-a75d-d657dccbd537` Orchard | Microsoft Research 唯一原文 8/03，五語稿仍作新發表且查核未過；人工以失時效退件，見上。 |

## 基線 24 筆需重寫／失敗

| # | 候選 ID／題目 | 基線關卡與下一步 |
| --- | --- | --- |
| 1 | `3e41d63a-28fb-4e2f-b96c-43831dfd2de9` Sonnet 5.5 | `news_slug_conflict` 且與既有專文重複；已人工退件，稽核讀回，見上。 |
| 2 | `3dd103c9-684f-4712-a3bd-e1715d9dc8b9` AI chatbot 預測 | [正式 Patterns 論文](https://www.sciencedirect.com/science/article/pii/S2666389926001753)研究 7 個 124M–12B 開放權重模型；Decrypt 的 15/16 是先前 preprint 口徑，不能稱最終研究準確率，也沒有已部署的聊天機器人監測器。AI 題誤歸 crypto，需分類修復、一手來源及重寫，不盲付費 retry。 |
| 3 | `9ca4d5ba-cec4-4da4-b8d5-8e3bbf0b3a3f` 法國委員會 | OAuth token refresh 失敗，AI 已核准但五語輸出／執行結果不明；先看 run、RQ、供應商收據，不能重送不明的付費請求。 |
| 4 | `b9c07491-5756-414c-b432-1f8f5d33aa3a` Solana 150ms | fact-check 失敗；核原始性能聲明及測試條件，再決定保留或退件。 |
| 5 | `7fa0b6b6-78f8-4b89-be28-8878f6ee439e` CLARITY Act | ja 翻譯失敗，標題時態「規則仍到來」需核；找原稿或快取後修 ja／重查。 |
| 6 | `28289a1b-5b85-4cb0-8fee-92beef07250f` AI Agents Keep Escaping | en 摘要 308 字超過 300，僅 zh-TW 快取／無完整 Guide，AI 題誤歸 crypto；先釐清已有恢復票與 artifact，再校正分類、補包及單篇查核。 |
| 7 | `511b2671-b444-4d24-a6b3-0d1622984481` SEC token buybacks | [SEC 員工 FAQ 2.5](https://www.sec.gov/about/divisions-offices/division-corporation-finance/faqs-crypto-assets)是有條件的 staff view、無法律拘束力，不是委員會新規或 blanket safe harbor；系統是否有中心管理者、回購是否暗示獲利與 managerial efforts 均須分清後重寫。 |
| 8 | `6b846276-450c-4392-9912-a5e51739f359` XRP Treasury | Evernorth 舊交割／上市預告與已刊 10/12 實際掛牌稿重複且過時；人工退件、稽核讀回，見上。 |
| 9 | `e4270a94-512c-447e-85b0-9f6d2ecfd657` Google 免費 1080p AI video | 官方公告與本站既刊文同事件；已以重複人工退件、稽核讀回，見上。 |
| 10 | `13c96f09-f6fd-4255-b72c-ebade0fd4a79` XRP Ledger 升級延遲 | 鏈上顯示修正案已於 10/9 啟用，舊預告過時；已人工退件、稽核讀回，見上。 |
| 11 | `a5ad16d0-0e30-4027-bf50-e4d0466e1aba` Google 建遊戲 | [Google 10/07 官方公告](https://blog.google/innovation-and-ai/technology/ai/playground-experimental-gaming-platform/)已推出 Playground 實驗平台，僅美國 18 歲以上、創建額度依 Google AI 訂閱層級；Unity Spark 整合是未來封測，不能寫成已開放。AI 題誤歸 crypto；需分類與時態重寫。 |
| 12 | `04a136f5-3738-45d1-80cf-f9a9a74cc756` Polygon／TRON 穩定幣 | [Polygon 10/08 官方文章](https://polygon.technology/blog/polygon-oms-supports-tron)說 OMS 支援 TRON 已上線；逾 940 億美元是 TRON 上 USDT 流通量，並非經 Polygon 搬運的金額。需修分母與產品範圍再重寫。 |
| 13 | `1f2dd889-0eeb-4f10-89e3-897f43273cbe` MetaMask／Lido validators | fact-check 失敗且細節提取因 parser 為空；先恢復可讀來源，再核事故範圍。 |
| 14 | `068c4856-dea9-4d1b-9dd7-22ac91c6b07c` Canada's Crypto King | 舊稿「即將審訊／將自行辯護」已被 10/7 當庭報導超越；人工退件，未推定有罪，見上。 |
| 15 | `4c2952b8-c0ee-4ad6-8ce8-fe5defd55d5b` 澳洲 AI agent 聽證 | 10/01 已過、現有證據不足以說明聽證結果且「首宗」無佐證；人工退件，未推定出席狀態，見上。 |
| 16 | `92c7561b-4595-4c03-a9a4-77412186427d` Haiku 5.5 | [Anthropic 10/07 官方公告](https://www.anthropic.com/claude-haiku-5-5)的平均成本估計約降 75%，與短請求定價最高降 90% 的口徑不同；超過 100k tokens 另為 50%。已可用，但候選事實查核失敗且嘗試上限 2；需分清數字並去重，不能直接付費重跑。 |
| 17 | `6de098ac-7c27-443c-8b5c-d91400839934` Pudgy Penguins／Abstract | [Decrypt 報導](https://decrypt.co/380225/pudgy-penguin-ethereum-layer-2-abstract-shutting-down)指向 12/15 自願停止與遷移提醒，非駭侵；官方 X 公告在本次讀取回 403，須取得原生可讀的官方公告／遷移頁再重寫，不以二手稿直接發。 |
| 18 | `4343e0fb-1806-4d6c-817b-440fa9e9eb2d` Morning Minute／Drake | 與較完整 Decrypt 原文同事件，且本稿證據不合；已人工退件，稽核讀回，見上。 |
| 19 | `d3c18ec1-d700-472b-8ffc-e9c2f9d37e50` OpenAI／Google AI safety pact | zh-CN 翻譯失敗、嘗試上限 2；修明確錯句後查核，先核 pact 的官方原文。 |
| 20 | `0f23dbf9-a6d0-4938-9fbf-825b4e582313` Manus $500M | fact-check 失敗，AI 題誤歸 crypto，單一二手來源；核交易原始來源與分類。 |
| 21 | `31ddc338-8cff-4e5c-b647-38de7c7423a7` Gemini own email | 與本站已公開 Gemini Agent 專文重複；已人工退件、稽核讀回，見上。 |
| 22 | `e2023dbd-28f9-4e87-8305-7d87772c767a` Bitcoin lending $500M | [Sui](https://www.sui.io/blog/hashi-mainnet-to-launch-with-500m-in-capital-backing-adds-anchorage-digital-to-coalition)與 [Anchorage](https://www.anchorage.com/press-room/anchorage-digital-joins-hashi-as-a-day-1-launch-partner)一手公告：超過 5 億美元是聯盟資本**承諾**，主網預計十月稍後分階段推出，非已放出貸款或已全面上線。需修金額與時態，嘗試上限 2 不盲重跑。 |
| 23 | `efc90b90-7f0d-41f9-b4a3-2b4f7d59b4b0` Ledger $87M reseller | 本站兩篇較新且已公開的同事件專文已讀回；此舊稿人工退件、稽核讀回，見上。 |
| 24 | `e0fee63a-ce83-4d71-b6a7-c5093001b227` Visa APAC stablecoin $1.2B | en 翻譯失敗，殘留 `not investment advice`；先核來源 10/05 URL 與 10/10 事件日期差異，再做原生單語修正及查核，不能整篇 retry。 |

## 接手順序與關卡

1. **先讀回 Kalshi 的來源障礙**：查候選、run、Guide 五語、稽核及公開頁。Drake／XRP／Falcon／Flock／NVIDIA／Citrix／AEMA 已在後台已發布清單，公開讀回範圍逐篇列於上表，仍需補終態 run／全篇證據、Falcon ja 與 AEMA ko 的 429。若新 run 未過關，記下精確 validator／judge 訊息，修該語／該事實後才單篇重送。
2. **可直接編輯的審稿問題**：Meta 眼鏡 #20 需先修證據與五語的時態／產品描述；不要以「稿五語齊」直接發布。OpenAI 澳洲 #8 的舊稿已退件，不能沿用過時時序。
3. **來源障礙分診**：CFTC #1／#23／#25 共查官方 HTTP 問題與去重；Meta Muse #41、MoonPay #42、白宮 #44 先把導覽／作者頁與正文分開；其餘 `source_content_changed` 比對舊快照和當前正文後才考慮 `refresh-evidence`。刷新會重新抓所有來源，單一失敗可能令候選維持原狀。
4. **15 筆尚未退件的 redraft／failed（以固定基線計）**：分清 AI handback、翻譯錯、來源不足、嘗試上限、provider 故障；既有 judge 已跑過的項目不應再當成「未審」整批跑。人工 `retry` 會開新的整篇撰稿並可能付費，且清掉原人工決定；只在有 run／RQ／供應商收據及單篇方案時用。French OAuth 故障先核未知結果。
5. 每個決定都寫必填稽核原因，讀回持久狀態；退件要保留和既有公開文章的去重證據。對照本名冊和最新正式站盤點調整未處理數，不把新流入或舊工作樹的認領混入完成率。

## 相關工作與限制

- 當前工作枝 `codex/news-hourly-review-20261013`，沿用 draft PR #1480；PR 綠燈、合併、部署、匯入、後台候選終態及公開頁驗證是不同關卡。PR #1480 仍是草稿，不能把 repo 修正當作正式站已部署。
- 舊批次由其他 worktree／票持有，這次處理的是站主明確指定的**正式站現有 70 筆**，不是搬動或結束那些票。若進一步修 API 或前端，不應在本票的單一 docs scope 下改程式；先盤點擁有者、擴增／另認領精確 scope。
- 已知的來源抓取與 AI run 故障應與現有恢復票比對，避免多個 session 重複付費或同改檔案。仍未通過的候選保持待審／需重寫；人工退件是終局編輯決策，不能把它算作文章已發布。
