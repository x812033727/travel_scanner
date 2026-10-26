# 參考片研究 2026-10-25：本週海外高點閱的 AI 時事片在講什麼、怎麼切

站主 2026-10-25 要「製作新的 AI／科技時事影片，參考最近 YouTube 點閱率高的國外影片題目，也參考它們的內容補強沒有的 skill，
跟上他們的內容跟影片製作」。這份是研究紀錄；做出來的影片是 `docs/videos/php2shell-ai-found-it-first/`，
規則落在 `.agents/skills/youtube-video/references/news-flow.md`（SKILL.md 的 reference 表有一列）。

量法：2026-10-25 06:06 UTC 用 `Mokaair-editorial/1.0` 的 UA 抓 YouTube 搜尋結果頁（`sp=CAMSBAgDEAE%3D`＝依觀看數排序、本週），
四組查詢：`AI news`、`OpenAI`、`Claude Code`、`AI agents`，各取前 20 筆的標題、頻道、觀看、上架時間、長度（`ytInitialData` 裡的 `videoRenderer`）。
watch 頁（字幕、訂閱數）對這台機器回 429，所以**沒有逐字稿**；結構的讀法來自這些頻道同題的文字報導（BBC 三篇、TechTarget、NPR 標題）與片長、標題。
下一次要量字幕時，照 `reference-study-20261021/README.md` 的做法用內建瀏覽器開 watch 頁讀 `captionTracks`。

## 一、本週的題目（觀看數，2026-10-25）

| 題目（節錄） | 頻道 | 長度 | 觀看 | 上架 | 題材 |
| --- | --- | --- | --- | --- | --- |
| [News 'Pick'] Dogs and cats are about to be pushed out by AI... Jensen Huang | OBS뉴스 | 2:39 | 316 萬 | 3 天 | 名人言論 |
| Websites taken down worldwide as AI reveals critical cyber-security threat | BBC News | 1:57 | 225 萬 | 3 天 | **PHP2Shell** |
| Did Google just dethrone OpenAI and Anthropic? | Fireship | 6:33 | 186 萬 | 4 天 | Gemini 4 Argon |
| ChatGPT Whistleblower WARNS: “You’re Being LIED To” | The Diary Of A CEO Clips | 20:01 | 176 萬 | 4 天 | 訪談 |
| Claude Made My Old Android TV Feel Brand New! | Ansub Khan | 4:02 | 93 萬 | 6 天 | Claude Code 實作 |
| Mathematicians Are The Canary Down The AI Coal Mine | The Rest Is Science | 1:04:16 | 92 萬 | 6 天 | 訪談 |
| We Are No Longer in Control of the AI Situation | AI In Context | 33:14 | 80 萬 | 4 天 | 論述 |
| HOW TO COMPLETELY TRANSFORM YOUR TV WITH CLAUDE CODE FOR FREE! | vbluuiza | 11:38 | 72 萬 | 2 天 | Claude Code 實作 |
| PHP flaw: How AI just hacked an unhackable part of the internet (About That) | CBC News | 11:29 | 63 萬 | 1 天 | **PHP2Shell** |
| The PHP internet crisis could just be the beginning | Sky News | 6:21 | 62 萬 | 2 天 | **PHP2Shell** |
| OpenAI Had to Shut Down Its Server in an Emergency: 10 New GPT-6 Astra Anomalies | DenTrave | 20:36 | 57 萬 | 4 天 | 聳動整理 |
| Quantum breakthrough, Gemini 4 Argon, MOSS Image, KLING 4, OpenAI spy… AI NEWS | AI Search | 40:55 | 56 萬 | 7 天 | 週報 |
| Epic Just Forced Its Devs to Stop Writing Code | Bellular News | 17:19 | 46 萬 | 6 天 | 產業 |
| Gemini Has A New AI Super App, Here’s How To Master It | Paul J Lipsky | 14:44 | 39 萬 | 6 天 | Gemini 4 Argon 教學 |
| Unlimited Claude Code For Free (Runs On Your Computer) | Sharbel A. | 12:16 | 38 萬 | 6 天 | Claude Code |
| Websites went down around the world. Did AI stop it getting worse? | BBC News | 14:09 | 36 萬 | 2 天 | **PHP2Shell** |
| Build Your First AI Agent in 20 Minutes (No Coding) | Metics Media | 21:14 | 33 萬 | 5 天 | 教學 |
| AI agents accessing bank accounts without approval, report says | CBS News | 5:22 | 22 萬 | 1 天 | **銀行 AI 代理**（Axios 10/22 獨家） |
| The OPENAI Cyberattack on Hugging Face Was WAY BIGGER Than We Thought | The Infographics Show | 17:53 | 27 萬 | 1 天 | 資安 |
| 14 ವರ್ಷದ ರಹಸ್ಯ ಬಯಲು, PHP Vulnerability, PHP2Shell, OpenAI, CERT-In | Masth Magaa | 9:01 | 22 萬 | 2 天 | **PHP2Shell**（坎納達語） |

四組查詢合起來，同一則新聞被最多頻道、最多語言做、而且單支最高的是 **PHP2Shell**（BBC、CBC、Sky、Diamandis、印度坎納達語台、波蘭財經台都有）；
第二群是 **AI 代理進銀行帳戶**（CBS、Fox、WION、TYT、MS NOW、CBS Mornings 六支 8–22 萬，都在 1–2 天內）；
第三群是 **Claude Code 改造 Android TV**（七支 15–93 萬，全是個人頻道的實作片）；第四是 Gemini 4 Argon 的教學與 Fireship 的評論。

## 二、新聞台怎麼做同一題（從片長、標題與同台文字報導讀）

| | BBC（1:57、14:09） | CBC About That（11:29） | Sky（6:21） |
| --- | --- | --- | --- |
| 標題 | 事件＋後果：「Websites taken down worldwide as AI reveals…」「Did AI stop it getting worse?」 | 反直覺句：「How AI just hacked an unhackable part of the internet」 | 升級：「could just be the beginning」 |
| 長度 | 2 分鐘新聞、14 分鐘解釋 | 11 分鐘單題解釋 | 6 分鐘 |
| 文字報導的章序（BBC 2026-10-23 explainer） | What is PHP → What is the vulnerability → What websites have been affected → What happened after → How was AI involved → What does it mean for you | — | — |
| 鉤子 | 「AI 找到的最嚴重漏洞」「沒有人被駭、網站是自己關的」 | 「牢不可破的部分被 AI 打開」 | 「只是開始」 |

共同點：**先講後果（網站下線、首相發文），再講機制，最後一段「對你的意義」**；每一句引用都點名誰說的（Wiz、Calif 的 Ryan Austin、Cloudflare 執行長）；
數字只用官方或當事公司的（70%、9.2、數百萬次嘗試）。他們沒做的：給觀眾一條能自己跑的檢查。這是我們這支切進去的地方。

## 三、對我們的意思

1. **挑題看「群」不看單支**：同一則新聞三家以上、各 20 萬以上、七天內，才算本週的題；單支爆量的名人片（Jensen Huang、Altman 訪談）不是我們能做的型。
2. **大台講完「發生了什麼」，我們切一個概念**（teaching-flow §十）：PHP2Shell 的概念是「洞在引擎不在車身，所以修補是一條鏈、版本號看不出修沒修」，
   收在本機真的跑過的檢查（RUN），這是新聞台沒有的含金量。
3. **事件的時間線用 UTC、一格一件事**，放一張 `table`，旁白講四到六格就夠；台灣的數字（資安署 2.8 萬、200）一定要有，新聞台不會替台灣觀眾查。
4. **標題學他們的形狀**：事件＋後果＋對你的意義（「AI 先找到的洞，全球網站為什麼自己關站、你的網站怎麼查」），不學聳動整理台的「10 New Anomalies」。
5. **還沒做、記下來**：銀行 AI 代理那一群（Axios 10/22 獨家，台灣沒有對應的官方來源）；Claude Code 改 Android TV 那一群是實作片，要有真的電視與執行紀錄才能做（規矩 3）。

## 四、這次沒量到、下次補

- 三支新聞片的逐字稿與節拍表（watch 頁 429）；CBC About That 的章節時間。
- 頻道訂閱數（判斷「小頻道靠內容被推」）。
- 上架七天後我們這支的平均觀看時長，對照 BBC 14 分鐘那支的留存。
