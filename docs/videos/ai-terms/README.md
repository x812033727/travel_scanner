# AI 名詞十分鐘：系列規格

2026-09-29 起草。一集講清楚一個 AI 名詞：它是什麼、怎麼運作、什麼時候該在意、跟誰容易搞混，每集約 10 分鐘。**不編集數**：每一集都能單獨看，不用等前一集；站上多一個名詞的文章，就能多出一集。題庫是站上已經查核發布的 81 篇 AI 名詞專文（[`../../ai-terms-series/ARTICLES.md`](../../ai-terms-series/ARTICLES.md)），影片是文章的「聽得懂」版本，說明欄連回文章。

- 名詞庫（81 個名詞、影片代號、對應文章、分層與建議順序、鉤子、狀態）：[`terms.json`](terms.json)
- 一集怎麼發起、做完怎麼登記：§一個名詞怎麼變成一集
- 產線與關卡：skill `youtube-video` 的全自動路線（`.agents/skills/youtube-video/references/automated.md`），畫面是插圖投影片（[`../ILLUSTRATED.md`](../ILLUSTRATED.md)），頻道規格在 [`../README.md`](../README.md)

## 站主的決定（2026-09-29）

| 項目 | 決定 |
| --- | --- |
| 名稱 | **AI 名詞十分鐘**（站主 2026-09-29 定案）。名稱就是承諾：一個名詞、十分鐘 |
| 形式 | 全自動路線的插圖投影片（`format: "slides"`、`look: tech-story`）：說書式旁白（頻道聲音 Gemini Sulafat）、AI 插圖加運鏡、深色字卡、繁中 CC 不燒錄 |
| 長度 | 約 10 分鐘：`target_minutes: [9, 11]` 量的是成片。lint 用每分鐘 250 字估，實際合成約每分鐘 300 字（`automated.md` §坑），所以稿子要寫到 **lint 估 11.8–12.3 分、約 2,650–2,750 個單位**，成片才會落在 10 分鐘上下；lint 的「about 12 minutes; the target is 9-11」是估計值的警告，可以留著（2026-09-30 試片的校正，`tts` 後用實際長度再修這一行） |
| 集數 | 不編號。標題、縮圖、說明欄都沒有「第 N 集」；先後靠播放清單與片尾的「下一個名詞」 |
| 題庫 | 81 篇已發布的名詞專文，一篇一集；新名詞先寫文章再出影片（§一個名詞怎麼變成一集） |
| 出片順序 | `terms.json` 的 `tier`：第 1 層 20 個入門名詞先出（`suggested_order`），第 2 層進階 55 個，第 3 層專業 5 個。順序是建議，站主隨時可以插隊 |
| 節奏 | 建議每週 2 支（週二、週五 20:00 台灣時間），跟新聞影片交錯；做好才排，沒做好就不硬出 |
| 語言 | 繁中先出；四語 CC 建議全勾，配音先只做 en，看數據再加（[`../LANGUAGES.md`](../LANGUAGES.md)） |
| 站主觀點 | 沿用後台「頻道立場」；另提兩條這個系列專用的立場（§YouTube 政策），站主決定要不要存進設定 |

名稱已定案；節奏、語言預設、縮圖印章與系列專用立場仍是提案，列在 §站主要決定的事。

## 各語系名稱

| 語系 | 系列名 | 標題後綴 |
| --- | --- | --- |
| zh-TW | AI 名詞十分鐘 | ｜AI 名詞十分鐘 |
| en | AI Terms in 10 Minutes | \| AI Terms in 10 Minutes |
| ja | 10分でわかるAI用語 | ｜10分でわかるAI用語 |
| ko | 10분 AI 용어 | \| 10분 AI 용어 |
| zh-CN | AI 名词十分钟 | ｜AI 名词十分钟 |

ja、ko 是草稿，第一集做字幕翻譯時由審稿模型確認；改了就同步 `terms.json` 的 `series.names` 與 `series.title_suffix`。

## 一集長什麼樣（10 分鐘）

觀點解說（`formats.md` §A）套在插圖投影片（§E）上，加上名詞特有的兩段：示範，和鄰近名詞。時間是比例，實際以 `tts` 的時間軸為準。

| 段落 | 時間 | 做什麼 | 常用場景 |
| --- | --- | --- | --- |
| 鉤子 | 0:00–0:20 | 觀眾自己的問題，或一句反常識的話；20 秒內落鉤，不打招呼、不報目錄 | `title` → `shot` |
| 你以為／其實 | 0:20–1:40 | 大家以為這個名詞是什麼 → 一句話定義 → 證明它的一個數字或例子 | `shot`、`big` 或 `stats` |
| 它怎麼運作 | 1:40–4:00 | 機制，用一個觀眾想像得到的場景或比喻講；文章的圖解直接用 | `shot`、`diagram`、`steps` |
| 示範或實算 | 4:00–6:30 | 輸入 → 步驟 → 輸出 → **出錯時長什麼樣**；每集必有 | `chat`、`code`、`table`、`quote` |
| 什麼時候該在意 | 6:30–8:00 | 三個判斷條件，各配一個「如果你是…」 | `bullets`（逐條）、`compare` |
| 跟誰容易搞混 | 8:00–9:00 | 2–3 個鄰近名詞，一張比較卡；已經有影片的名詞就指過去 | `compare` 或 `table` |
| 收尾 | 9:00–10:00 | 回到開場的問題一句話回答；站主觀點一句；一個下一步 | `shot` → `outro` |

- 旁白約 2,650–2,750 個單位（一個中文字 1 單位、一個英文詞 2 單位），lint 估 11.8–12.3 分；實際合成約每分鐘 300 字，成片約 10 分鐘。
- 章節 5–7 個，每章至少 10 秒，名稱寫觀眾會搜尋的說法（「token 不是字數」「算一次你的公告要花多少 token」），不寫「開場」「結論」。
- 每章最後一句是下一章要回答的問題；最後一章回答開場的問題（說書式旁白的規則，`script-writing.md` §說書式旁白）。
- 每 5–8 秒換一張插圖或字卡狀態，插圖至少佔一半時間；一個 shot 只帶一句（≤ 28 單位），10 分鐘的影片大約 50–80 個 shot（試片三集是 50、52、76）；插圖畫這個名詞的場景與比喻，不畫字、logo、真人。
- 外文名詞第一次出現要說中文意思；每個英文詞進 `docs/videos/lexicon.json`。

## 三種場景配方

同一個骨架、每集不同的版型順序：`lint` 會警告兩支影片的版型序列太像，這個系列最容易踩到。企劃在 `brief.md` 挑一種配方起手，撰稿再依內容增減；連續兩集不用同一種。

| 配方 | 起手 | 序列（骨架） |
| --- | --- | --- |
| A 先誤解 | 從「你以為」開始 | `title` → `shot` → `big` → `shot` → `diagram` → `shot` → `steps` → `chat` → `shot` → `table` → `bullets` → `shot` → `compare` → `shot` → `outro` |
| B 先場景 | 從一個具體場景開始 | `title` → `shot` → `shot` → `stats` → `chapter` → `diagram` → `shot` → `quote` → `code` → `shot` → `compare` → `chapter` → `bullets` → `shot` → `outro` |
| C 先示範 | 開場就做給你看 | `title` → `shot` → `chat` → `shot` → `big` → `chapter` → `steps` → `diagram` → `shot` → `table` → `shot` → `compare` → `shot` → `outro` |

## 每一集都要有的東西

一集一個資料夾 `docs/videos/ai-term-<名詞>/`，跟其他全自動影片一樣：`brief.md`、`video.json`、`claims.md`、`verify-*.md`、`i18n/`。這個系列另外要求：

| 項目 | 規則 |
| --- | --- |
| `brief.md` | `prompts/planner.md` 的 8 節；「站主觀點」第一行 `套用立場：N、M`；「示範或實算」寫清楚在哪張卡 |
| 示範 | 文章本來就有一段「輸入、步驟、預期輸出、失敗怎麼讀」的示例（`docs/ai-terms-series/brief.md` 的規格），影片就做那一段，數字在寫稿當天重算或重查；文章示例不適合口播的，撰稿補一段觀眾能照做的 |
| 圖解 | 文章的 `apps/web/public/guides/<文章 slug>/diagram-1.svg` 用 `diagram` 版型直接放，`assets` 列出來源與授權（Mokaair 自有）；插圖不重畫同一張圖 |
| 來源 | `video.json` 的 `sources` 至少兩個一手來源，從文章的來源表挑，`checked_on` 是寫稿當天；文章的 `checked_on`（2026-09-14）不算數 |
| 會過期的事實 | 這個系列**不講**價格、方案、模型名稱、排行榜；非講不可就說「以官網為準」。名詞本身很少過期，不要為了鉤子加進會過期的數字 |
| 發音 | 名詞的英文全名與縮寫都進 `lexicon.json`（RAG、LoRA、DPO、A2A…）；試聽確認過才填 `null` |
| 鄰近名詞 | 從 `terms.json` 的 `related`（文章互相連結的名詞）挑 2–3 個講；片尾的下一步指已發布的那一集，還沒有就指文章 |
| Shorts | 撰稿順手交 `shorts.json`：兩支長片精華（`line: "cut"`），一支「一句話定義」、一支「最常見的誤解」（§Shorts） |

## 標題、縮圖、說明欄、播放清單

- **標題**：`<名詞>是什麼？<反常識的一句>｜AI 名詞十分鐘`。名詞放最前面（手機只顯示前 40 個全形字）；中文名詞第一次出現帶英文，例如「上下文視窗（Context Window）是什麼？塞得進去，不等於讀得懂｜AI 名詞十分鐘」；以縮寫通行的名詞直接用縮寫（「RAG 是什麼？…」）。沒有集數、沒有驚嘆號、沒有角括號。
- **縮圖**（`thumb` 版型）：`tag` 固定「AI 名詞十分鐘」、`headline` 是名詞本身（`terms.json` 的 `short`，超過版型上限就換行或縮短）、`sub` 是鉤子的短版。系列的辨識靠固定的 tag 與「名詞當大字」；要像原來如此事務所那樣有自己的印章與配色（`tools/video/templates/templates.mjs` 的 `THUMB_SERIES`），另開一張工具票，第一批先不等它。
- **說明欄**（`youtube.description` 本文）：前兩行說這集回答什麼、給誰看；本文最後一行放總索引 `https://mokaair.com/zh-TW/life/ai-terms-index?utm_source=youtube&utm_medium=video&utm_campaign=<影片代號>`。文章連結、章節、參考資料由 `package` 自動接（`source_guide` 指向那篇名詞文章）。
- **標籤**：名詞的中文、英文、縮寫與 `aliases`（例如「token」「詞元」「標記」），前三個會變成 #標籤。
- **播放清單**：一份總清單加八份分類清單（對應 `catalogue.json` 的八個分類），每集進總清單和它的分類清單；清單內照發布日期排，新集加在最後。五語名稱在 `terms.json` 的 `series.playlists`，第一集公開當天建立。

| 清單 | zh-TW | en | 名詞 |
| --- | --- | --- | --- |
| all | AI 名詞十分鐘（全部） | AI Terms in 10 Minutes (All) | 全部 |
| foundations | 基礎觀念 | Foundations | 人工智慧、機器學習、深度學習、生成式 AI、LLM、基礎模型、Transformer、混合專家模型、小型語言模型、模型參數 |
| prompts-context | 提示詞與上下文 | Prompts & Context | token、分詞、上下文視窗、系統提示詞、少樣本提示、零樣本提示、上下文學習、上下文壓縮、Context Rot、代理記憶 |
| agents | AI 代理 | AI Agents | AI 代理（既有三支影片）、代理迴圈、多代理系統、子代理、代理協調、ReAct、工具呼叫、MCP、A2A、Agent Skills |
| retrieval | 檢索與知識 | Retrieval & Knowledge | RAG、Agentic RAG、GraphRAG、嵌入向量、向量資料庫、語意搜尋、混合搜尋、重新排序、文件分塊、知識圖譜 |
| training | 訓練與推論 | Training & Inference | 預訓練、微調、SFT、RLHF、DPO、LoRA、知識蒸餾、量化、推理模型、推論時計算、提示詞快取 |
| engineering | 工程方法 | Engineering Practices | 提示詞工程、上下文工程、Harness Engineering、Loop Engineering、Agentic Engineering、Vibe Coding、規格驅動開發、LLMOps、AgentOps、提示詞串接 |
| evaluation-safety | 評測與安全 | Evaluation & Safety | Evals、基準測試、LLM-as-a-Judge、幻覺、提示詞注入、越獄提示、Guardrails、沙盒、人工介入、紅隊測試 |
| multimodal-open | 多模態與開放 | Multimodal & Open Models | 多模態 AI、擴散模型、文生圖、文生影片、語音辨識、語音合成、深偽、開放權重、開源 AI、內容憑證 |

## 一個名詞怎麼變成一集

不編集數的意思是：任何時候、任何順序，一個名詞都能單獨開工。三種情況：

| 情況 | 怎麼做 |
| --- | --- |
| **名詞已經有文章**（81 篇都是） | 直接發起，`source_guide` 填文章 slug |
| **新名詞，還沒有文章** | 先走 skill `content-pipeline` 寫文章（slug `ai-term-<名詞>`，照 `docs/ai-terms-series/brief.md` 的規格：一手來源、示例、圖解、連到總索引），發布後再出影片。理由：查核在文章做過一次；說明欄要有文章可連；工人的不重複選題靠 `source_guide`。趕時間要先出影片也可以：`brief.md` 自己列兩個以上一手來源、`source_guide` 留空、說明欄連總索引，並開一張 content-pipeline 的票補文章 |
| **名詞已經有影片**（`existing_videos` 不是空的） | 先看那支講了什麼。講的是同一件事就不出（`status: "covered"`）；角度不同才出，`brief.md` 的「不做的事」寫明跟那支的分工 |

發起一集的步驟（人或代理都一樣）：

1. `terms.json` 找到那一列（沒有就照同樣的欄位加一列），`status` 改 `planned`；影片代號是 `video_slug`（`ai-term-<名詞>`）。
2. 照 `automated.md` 的主幹從第 1 步開始：企劃代理用 `prompts/planner.md`，IDENTITY 寫名詞、`source_guide`、目標 10 分鐘（`target_minutes: [9, 11]`）、最近五支本系列的影片代號（讓它避開同樣的開場與版型順序），並附上這份 README 的 §一集長什麼樣 與 §三種場景配方。`brief.md` 寫進 `docs/videos/<video_slug>/`。
3. `review-push --gate outline` 起，一路到 `package` 與語言，關卡照 `automated.md`；`status` 改 `in-production`。
4. 上架後：`terms.json` 填 `video_id`、`published_at`，`status` 改 `published`；影片加進總清單與分類清單。片尾指向它的那些集（別列的 `related` 含它）下次做時就能連到它。
5. 站主看數據要改順序，只改 `tier` 或 `suggested_order`，不動已發布的列。

主機工人目前只從最近 14 天發布的文章與搜尋挑題（`apps/api/app/video_automation/topics.py` 的 `SITE_DAYS`），名詞文章 2026-09-14 發布，已經不在窗口內；所以第一批由 session 逐集發起，工人接手每一集的後續步驟。要讓工人在沒有新題目時自己從名詞庫接下一個名詞，是票 `2026-09-29-video-worker-takes-next-ai-term`（P3，站主決定要不要）。

## 名詞庫與出片順序

`terms.json` 的每一列：`id`、`video_slug`、`source_guide`（文章 slug）、`article_url`、`article_title`、`zh`、`en`、`short`（縮圖大字）、`aliases`、`category`、`playlist`、`tier`、`suggested_order`（只有第 1 層有）、`hook`（只有第 1 層有，企劃可以改寫）、`related`（文章互相連結的名詞）、`existing_videos`、`status`、`video_id`、`published_at`、`notes`。狀態：`backlog` → `planned` → `in-production` → `published`；`covered`（既有影片講過，不出）、`skipped`（站主決定不做，寫原因）。

第 1 層 20 個先出，建議順序（鉤子是草稿，從文章的標題與描述來，企劃可以改寫；數字與名稱仍要當天查）：

| # | 名詞 | 影片代號 | 文章 | 鉤子（草稿） |
| --- | --- | --- | --- | --- |
| 1 | token（Token） | `ai-term-token` | `ai-term-token` | 你以為 AI 算的是字數，其實它算的是自己的單位：同一段中文，換一個模型，用量就不一樣。 |
| 2 | 上下文視窗（Context Window） | `ai-term-context-window` | `ai-context-window-explained` | 聊天視窗裡的訊息都還在，不代表模型這一次全部讀到了：塞得進去，不等於讀得懂。 |
| 3 | 大型語言模型（Large Language Model） | `ai-term-large-language-model` | `what-is-a-large-language-model` | 大型語言模型不是一本會查資料的百科全書：它學的是語言的模式，所以答得流暢不等於答得正確。 |
| 4 | 幻覺（Hallucination） | `ai-term-hallucination` | `ai-hallucination-fact-check` | AI 附了連結、你再問一次它還是同一個答案、兩個模型都這樣講：這三件事沒有一件能證明它是對的。 |
| 5 | 提示詞工程（Prompt Engineering） | `ai-term-prompt-engineering` | `ai-term-prompt-engineering` | 指令越寫越長，答案卻沒有變好？提示詞工程不是寫得多，是測得出哪裡失敗。 |
| 6 | 系統提示詞（System Prompt） | `ai-term-system-prompt` | `ai-term-system-prompt` | 你在自訂助理裡寫「絕對不能透露」，它就真的不會透露嗎？系統提示詞是規則，不是保證。 |
| 7 | 檢索增強生成（RAG） | `ai-term-retrieval-augmented-generation` | `ai-term-retrieval-augmented-generation` | 回答附了引用，為什麼還是錯？RAG 的三個步驟，每一步都可能讓它拿著證據答錯。 |
| 8 | 嵌入向量（Embedding） | `ai-term-embedding` | `ai-term-embedding` | 「下雨可以去哪裡」跟「室內景點」沒有一個字一樣，AI 為什麼找得到？ |
| 9 | 微調（Fine-tuning） | `ai-term-fine-tuning` | `ai-term-fine-tuning` | 訓練成績變好了，實際上線卻退步：微調到底改了模型的什麼？ |
| 10 | 推理模型（Reasoning Model） | `ai-term-reasoning-model` | `ai-reasoning-models-explained` | 等更久、寫更長，不保證更對：推理模型多想的那幾步，到底在做什麼？ |
| 11 | 模型上下文協定（MCP） | `ai-term-model-context-protocol` | `ai-term-model-context-protocol` | MCP 不是模型，接上也不代表能完成任務：它是 AI 跟工具說話的共同插座。 |
| 12 | 代理技能（Agent Skills） | `ai-term-agent-skills` | `ai-term-agent-skills` | 把一段長提示詞換個檔名叫 SKILL.md，不算技能：Agent Skills 差在哪一步？ |
| 13 | 上下文工程（Context Engineering） | `ai-term-context-engineering` | `ai-term-context-engineering` | 回答錯了，常常不是模型笨，是它這一次根本沒看到那份資料。 |
| 14 | 提示詞注入（Prompt Injection） | `ai-term-prompt-injection` | `ai-term-prompt-injection` | 一封報名郵件裡藏一行字，就能讓你的 AI 助理改做別的事：提示詞注入是接上外部內容就會遇到的風險。 |
| 15 | 安全防護機制（Guardrails） | `ai-term-guardrails` | `ai-term-guardrails` | 加一個篩選器不等於安全：防護機制是放在輸入、資料、回答與工具四個地方的一整組檢查。 |
| 16 | 生成式 AI（Generative AI） | `ai-term-generative-ai` | `ai-term-generative-ai` | 它會生成，不會保證忠於事實：生成式 AI 跟分類、搜尋到底差在哪？ |
| 17 | 多模態 AI（Multimodal AI） | `ai-term-multimodal-ai` | `ai-term-multimodal-ai` | 它看得到圖片，不代表它看到了細節：多模態 AI 什麼時候在看，什麼時候在猜？ |
| 18 | 深偽（Deepfake） | `ai-term-deepfake` | `ai-term-deepfake` | 嘴形對得上、偵測分數很低、來源標記也有：這三樣都不能單獨判定一支影片是不是深偽。 |
| 19 | 開放權重（Open Weights） | `ai-term-open-weights` | `ai-term-open-weights` | 能下載的模型不等於開源，也不自動等於隱私：開放權重拿到的到底是什麼？ |
| 20 | 小型語言模型（Small Language Model） | `ai-term-small-language-model` | `ai-term-small-language-model` | 小模型不等於弱，離線也不等於隱私：小型語言模型該看的是任務、記憶體和資料流。 |

AI 代理也在第 1 層，但已經有三支影片講過（`ai-agent-vs-chatbot`、`ai-agents-explained-what-they-cost`、`always-on-agent-explained`），`status: "covered"`，不單出一集；代理的機制由第 2 層的「代理迴圈」「工具呼叫」接手。第 2 層是其餘 55 個進階名詞，第 3 層是 5 個專業名詞（Harness Engineering、Loop Engineering、Agentic Engineering、LLMOps、AgentOps），看第 1 層的數據再排。

## 跟其他系列與既有影片的分工

| 對象 | 分工 |
| --- | --- |
| 原來如此事務所（[`../so-thats-why/`](../so-thats-why/README.md)） | 那邊回答「為什麼」，一集一個故事；這邊回答「是什麼、什麼時候該在意」。同一個機制兩邊都碰到時，鉤子不能一樣：A08 用 strawberry 講 token，本系列的 token 集用「同一段中文換模型用量不同」；A01 講 AI 為什麼胡說，幻覺集講怎麼把回答拆成可查主張；A16 講畫錯手指，擴散模型集不用手指梗。兩邊在說明欄與片尾互連 |
| 已經做好的長片 | AI 代理有三支，不再單出；vibe coding 有操作教學（`vibe-coding-first-website-2026`），名詞集只講定義與界線；本機 AI（`rtx-spark-local-ai`）講硬體，開放權重、量化、小模型三集講名詞本身。每一列的 `existing_videos` 與 `notes` 寫了分工 |
| 站上的 AI 名詞文章 | 影片是文章的「聽得懂」版：刪掉一半段落、表格改字卡最多三列、示例只做一個（`formats.md` §從 Mokaair 文章改編）；文章之後可以嵌入影片，另開 content-pipeline 的票 |
| AI 新聞影片 | 新聞影片提到某個名詞時，說明欄連到那一集；名詞集不追新聞 |

## YouTube 政策：這個系列最容易被當成模板量產

YouTube 的「非原創內容」政策點名的就是「AI 旁白配幻燈片、沒有創作者觀點、套模板量產」（[`../DESIGN.md`](../DESIGN.md) 的規則表、[`../HANDS-OFF.md`](../HANDS-OFF.md) §頻道立場）。一個 81 集的名詞系列，骨架一樣、旁白一樣、縮圖一樣，正是最像模板的東西。所以每一集都要做到：

1. **站主觀點是具體的**：不是「我覺得這個名詞很重要」，而是這個名詞會改變站主的哪一個決定（花不花錢、信不信答案、給不給權限）。`套用立場：N、M` 引用後台的頻道立場；提案再加兩條系列專用的立場，站主決定要不要存進設定（條號接在 `HANDS-OFF.md` 草稿的 7 條後面）：
   - 8. 名詞是用來做決定的：每個名詞都講到它會改變你的哪一個選擇（要不要花錢、信不信這個答案、給不給它權限），講不出來就不值得一集。
   - 9. 看過失敗的樣子才算懂：每個名詞至少示範一次它出錯時長什麼樣，以及怎麼分辨是資料、指令還是模型的問題。
2. **每集一段真的做過的示範**，不是唸定義：算一次 token、比一次兩種切法、跑一次檢索、拆一次幻覺主張。
3. **版型順序輪替、插圖畫名詞的場景**：三種配方輪流，`shot` 的提示詞是這個名詞的比喻（積木紙帶、會議紀錄、圖書室櫃台），不是通用的「AI 機器人」。
4. **鉤子與鄰近名詞每集不同**：`hook` 從文章的「常見誤解」來，`related` 從文章的互連來，沒有兩集講同一組。
5. 頻道立場還是空白時（2026-09-29 查證仍空白），Jev 不挑大綱、`qa` 的 `policy` 也不會過：第一集開工前，站主要先把立場存進 `/admin/videos` 的設定分頁。

## Shorts

每集兩支長片精華（[`../SHORTS.md`](../SHORTS.md) 的 `cut` 線，9:16、35–55 秒），撰稿順手寫 `docs/videos/<video_slug>/shorts.json`，長片的關鍵影格畫好後 `node tools/video/shorts/cli.mjs from-episode --slug <video_slug>`：

1. **一句話定義**：鉤子＋定義＋「完整的在長片」。
2. **最常見的誤解**：「你以為／其實」那一段，只講一件事。

Shorts 的說明欄第一行連回長片；精華線的每週配額照 `SHORTS.md`（預設每週 2 支），沒做出來不擋長片。

## 多語

照 [`../LANGUAGES.md`](../LANGUAGES.md)：成片核准後站主在影片頁勾語言。這個系列的建議預設：四語 CC 全勾（名詞是跨語言搜尋的題目，搜尋量在英文最大）、配音先只做 en。每語標題的名詞用該語系的通行寫法（英文用官方英文名，日韓保留英文縮寫加當地說法）；翻譯審稿時檢查「你以為／其實」對該語系觀眾是否仍成立。

## 查核規則

- 每個數字、名稱、誰說的，寫稿當天在一手來源確認，寫進 `## 來源` 附日期（skill 不變規矩第 2 條）；文章的來源表是起點，不是證據。
- 新興名詞（Context Engineering、Harness Engineering、Agent Skills…）沒有統一定義：影片要說「這裡用的是誰的說法」，不發明通用定義（文章的規格同樣要求）。
- 示範是這次真的做的；沒做過的不說「我測過」；不冒充任何產品的介面。
- 不講價格、方案、排行榜與模型比較；需要例子時用「以官網為準」帶過。

## 成本與產能（估計，試片三集後改成實測）

| 項目 | 每集 | 第 1 層 20 集 | 81 集 |
| --- | --- | --- | --- |
| 插圖（`ILLUSTRATED.md` 的估計：每支長片 US$8–15） | US$8–15 | US$160–300 | US$650–1,200 |
| 旁白＋配音（Gemini TTS） | 不到 US$1 | 約 US$20 | 約 US$80 |
| 撰稿、查核、翻譯 | 訂閱帳號的額度，不另計 | — | — |

每週 2 支的瓶頸是站主看成片、勾語言、在 Studio 上傳；自動關卡（旁白、分鏡、成片品管、上傳包）都上線後，站主每集只剩上架時間。試片票把三集的實際數字填回這一節。

## 站主要決定的事

已定案：系列名稱「AI 名詞十分鐘」（2026-09-29）；ja、ko 的名稱在第一集翻譯時確認。還要決定的：

1. 要不要把立場第 8、9 條加進後台「頻道立場」；立場空白前，第一集不會自動過大綱關卡。
2. 出片時段（提案週二、週五 20:00）與第一批的順序（`terms.json` 的 `suggested_order`）。
3. 語言預設：四語 CC、en 配音。
4. 要不要給這個系列自己的縮圖印章與配色（`THUMB_SERIES`）；不要的話用共用的 `thumb` 版型。
5. 要不要讓主機工人自動接名詞（票 `2026-09-29-video-worker-takes-next-ai-term`）。

## 檔案位置

| 檔案 | 用途 |
| --- | --- |
| `README.md` | 這份系列規格 |
| `terms.json` | 名詞庫：81 列，一列一集；新名詞加一列 |
| `../ai-term-<名詞>/` | 每一集的 `brief.md`、`video.json`、`claims.md`、`verify-*.md`、`i18n/`、`shorts.json` |
| `../../ai-terms-series/` | 文章批次的規格、目錄（`catalogue.json`）、發布收據 |

## 票

| 票 | 內容 |
| --- | --- |
| `2026-09-29-ai-terms-video-series-plan` | 這份規格與名詞庫 |
| `2026-09-29-ai-terms-video-pilot` | 前三集試片：token、上下文視窗、RAG；把實際長度、成本、留存數字填回這份 |
| `2026-09-29-video-worker-takes-next-ai-term` | P3：工人沒有新題目時從名詞庫接下一個名詞 |
