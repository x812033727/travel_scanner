# 參考片研究 2026-10-26：本週海外高點閱的 AI 時事片，哪一群還沒做

接在 `reference-study-20261025-ai-news/README.md` 後面，做法照 `.agents/skills/youtube-video/references/news-flow.md` §一。
站主 2026-10-26 要「找新的影片主題」，從四群候選裡選了 A（ARTEX）；做出來的影片是 `docs/videos/artex-ai-attack-leftover-keys/`。

量法：2026-10-26 用 `Mokaair-editorial/1.0` 的 UA 抓 YouTube 搜尋結果頁（`sp=CAMSBAgDEAE%3D`＝依觀看數排序、本週，`hl=en&gl=US`），
十三組查詢：`AI news`、`OpenAI`、`Claude Code`、`AI agents`、`ChatGPT`、`Gemini`、`Anthropic`，第二輪加 `ARTEX AI`、`Anthropic IPO`、`Claude TV ads`、
`local AI privacy`、`bank AI agents`、`Apple Intelligence`，各取前 20 筆（`ytInitialData` 的 `videoRenderer`）。watch 頁沒有抓，所以**沒有逐字稿與訂閱數**。

## 一、先排除已經做過的

PHP2Shell（`php2shell-ai-found-it-first`）、Claude Duet（`claude-duet-proactive-agent`）、Meta Muse 購物代理（`ai-shopping-agents-blocked`）、
Gemini 4 Argon（已上架，重寫票 `2026-10-11-rewrite-gemini-4-argon-who-can-use-it`）。名人訪談（Jensen Huang、Altman）、聳動整理、搞笑片不選。

## 二、過門檻的四群（三家以上、各 20 萬以上、七天內）

| 群 | 頻道（觀看，2026-10-26） | 官方來源 | 觀眾今天能做的動作 | 判斷 |
| --- | --- | --- | --- | --- |
| **A. ARTEX：AI 自主滲透工具被拿來攻擊** | 令和政治ナビ 52 萬（3 天）、TBS NEWS DIG 42 萬（6 天）、AI Revolution 26 萬（2 天）、海外Yパパラジオ 18 萬、Breaking Points「BLACK OCTOBER」50 萬（4 天）；台灣 fOx Hsiao 2.3 萬 | Microsoft Threat Intelligence 10-21、GMO イエラエ 10-19、91APP 10-22 調查報告、資安署 10-21 示警（iThome 報導） | 撤掉放著的鑰匙：連結的應用程式、授權過的 OAuth App、git 歷史裡的金鑰 | **選這一群** |
| B. Anthropic 公開 S-1 | House of El 42 萬、Bloomberg 30 萬、VisualEconomik 28 萬；CNBC、WSJ、NBC 10-26 當天各 4–6 萬 | SEC EDGAR 的 S-1 | 弱：只能自己讀 S-1 | 財經題、觀眾沒有動作；本頻道用 Claude 做片，要揭露利益 |
| C. 用 Claude 清掉智慧電視廣告（CleanYourTV） | vbluuiza 92 萬、Oliur 65 萬、Lukas Margerie 32 萬、Saul Diaz 31 萬、Navy Geeks 30 萬、UG Tech 29 萬、Beebom 28 萬 | 開源專案的 GitHub（MIT）、TechCrunch 10-19 | 強：清自己的 Google TV | 要真的電視與執行紀錄（規矩 3），本機做不到；站主有裝置再做 |
| D. AI 代理進銀行帳戶 | Breaking Points 50 萬、CBS 27 萬、Fox News 27 萬、Neal K. Shah 22 萬、YTN 21 萬 | Axios 獨家、FT 報導（銀行的說法都是轉述） | 查哪些 App 有銀行授權 | 沒有官方來源、台灣沒有對應；跟 Muse 那支重疊 |

其他單支高的：InsideAI「AI agent builds itself a robot body」163 萬、BBC AI Decoded「Apple and Meta's bet against the cloud」120 萬、
Kai「Your Local AI Is Not as Private as You Think」45 萬，都只有一家。

## 三、為什麼是 A、怎麼切

- 新聞台講的是「中國 AI 攻擊日本企業」（TBS、令和政治ナビ）與「AI 讓網攻失控」（AI Revolution、Breaking Points）。他們沒講的是**這些攻擊實際是從哪裡進去的**：
  Microsoft 記錄到 15 萬次猜密碼全部失敗，進去的是早就被授權的 App；91APP 的破口是沒更新的內部工具加上 GitLab 裡的一把資料庫金鑰；
  資安署說 AI 會評估成本、放棄基礎扎實的企業。三份官方說法指向同一件事：**AI 不是新開一個洞，是在幾小時內把放著的鑰匙找出來用掉。**
- 這支切的概念就是「放著的鑰匙」，收在觀眾自己能跑的三個檢查；本機跑過的是 git 歷史那一個（刪掉的 `.env` 一行指令拿回來）。
- 台灣的數字有兩個官方來源：91APP 的 18 天調查報告（ARTEX 痕跡）、資安署 10-21 示警（7 月國內監測到類似活動）。
  Zeabur 10 月的事件是同一週的台灣事件，但官方報告沒有提到 ARTEX 或 AI 工具，**只能並列當「放著的鑰匙」的另一個例子，不能說有關**。

## 四、這次沒量到、下次補

- 各支的逐字稿與章節（沒開 watch 頁）；頻道訂閱數。
- 上架七天後把平均觀看時長、CTR 與 TBS 那支並排寫回這裡（news-flow §四）。
