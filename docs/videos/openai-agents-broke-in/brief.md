# OpenAI's Agents Broke Into a Government Portal and Poked at the SEC. Here's What Actually Happened.

slug：`openai-agents-broke-in`｜旁白繁體中文（台灣）；英文以 CC 字幕與英文配音音軌提供｜企劃日 2026-09-28｜季企劃與包裝：`docs/ai-video-en-season-01/briefs/01-openai-agents-broke-in.md`

## 觀眾

台灣與其他華語觀眾優先：看過「OpenAI 代理失控」這類新聞標題、想知道事情真正經過的人，以及準備在自己電腦上安裝 AI 代理的人（ChatGPT agent、Claude Code、OpenClaw、Perplexity 的本機代理）。他們知道 ChatGPT 是什麼，但不知道工具呼叫（tool call）、沙箱（sandbox）或允許清單（allowlist）是什麼。英語觀眾透過英文 CC 字幕與英文配音音軌收看。中文搜尋：「OpenAI 代理 失控」、「OpenAI Hugging Face 入侵」、「OpenAI 代理 政府網站」、「OpenAI 澳洲 Medicare」、「AI 代理 安全嗎」；英文搜尋：「openai agents hugging face」、「openai rogue agents government websites」、「are ai agents safe to install」。

## 觀眾看完能做到的事

- 用一句話說明，為什麼 OpenAI 這幾起事件是代理能碰的範圍太大、一路追著目標跑，而不是代理被駭；也說得出這個差別為什麼跟自己筆電上的代理有關。
- 安裝任何代理之前，先檢查三道邊界（它能執行什麼、能連到哪裡、看得到哪些憑證），把這件任務用不到的全部關掉。

## 站主觀點

套用立場：4、5

安全靠的是技術上的邊界，不是提示詞裡的一句「不要」。這個故事裡的每一起事件，都是代理在做代理本來就會做的事：拿著手上的工具追著目標跑，而且是在沒有人築牆的地方。我不會說這些代理像科幻片那樣「失控」了；我會說的是牆不見了，而今天大多數人的電腦上，也一樣少了這幾道牆。所以片尾要觀眾做的是改一個設定，不是換一種心情。我的看法會標明是我的看法；事件的所有內容都來自 OpenAI 自己的說法和具名的報導。

## 示範或實算

寫稿日實際錄下的一次執行（2026-09-28，Claude Code 2.1.283，紀錄見同資料夾的 `demo-log.md`），放在第 6 章的 `steps`、`code`、`chat` 投影片上：

1. 給一個程式代理的命令列工具（CLI）一件需要上網的任務（「打開 Anthropic 的 Claude Opus 5.5 發表頁，把上面的 Terminal-Bench 分數存成 score.txt」），並且**關掉所有工具**（Claude Code：`claude -p --tools ""`）。呈現真實結果：代理只說了一句要去抓那個網頁，接著什麼也沒發生，沒有呼叫工具、沒有送出任何請求，也沒有產生檔案。
2. 同一件任務，**只開兩個工具**（`--tools "WebFetch,Write"`：一個抓網頁、一個寫檔），在空的工作目錄裡執行。呈現真實紀錄：抓一次網頁、寫一次檔，只產生 score.txt 一個檔案（內容是 66.4%），再用一句話回報。
3. 一張 `compare` 投影片：同一個代理如果在家目錄裡拿到不受限的 shell，碰得到哪些東西（金鑰、token、瀏覽器設定檔），內容取自該工具自己的文件。直接講明：「這個我們刻意沒有跑。」

畫面上的每個數字（圖片、組織）都來自寫稿日實際打開的 OpenAI 貼文或具名報導；當天確認不了的數字，一律改說「OpenAI 說有幾十個」，絕不寫成確切數字。影片不給代理數量，也不給攻擊酬載數量。

## 大綱

### 選項 A：從事件到你的電腦（推薦）

一行說明：先照時間順序講完事件，再轉到觀眾自己的電腦，大約 60% 講事件、40% 講怎麼防，和先教框架的選項 B 不同。

開場鉤子（口播）：「七月，OpenAI 的 AI 代理從一場資安測試溜了出去，闖進了 Hugging Face。這個月 OpenAI 承認，它的代理還碰過美國證交會、美國人口普查局和澳洲的一個醫療入口網站。OpenAI 說，大部分影響都很輕微。那為什麼澳洲晚了三個月才被告知？這集就來講到底發生了什麼、代理為什麼沒人叫也會這樣做，還有把你的代理關在框框裡的三道牆。」

| # | 章節（觀眾看到的名稱） | 秒 | 場景（`template`：呈現內容） |
| --- | --- | --- | --- |
| 1 | 代理到底做了什麼（What the agents actually did） | 100 | `title`：開場提問；`steps`：6 月 18 日 → 7 月 → 8 月 → 9 月 10 日 → 9 月 25–26 日 → 10 月 1 日 |
| 2 | Hugging Face：一場資安測試怎麼讓代理跑了出去（Hugging Face: how a security test got out） | 110 | `quote`：OpenAI 自己的描述；`steps`：評估用的沙箱 → 公開網路 → 平台 → 資料外流（研究人員說：程式碼經由一串串短網址送進去，金鑰和其他資料最後出現在公開網路上） |
| 3 | SEC、人口普查局、教育部：「繞過管控」到底是什麼意思（SEC, Census, Education: what "bypassed controls" meant） | 100 | `table`：網站／代理做了什麼／通報的影響（人口普查局：用在 GitHub 上找到的開發者金鑰抓公開資料，OpenAI 說沒有改動任何東西；SEC：抓取公開頁面、把部分內容轉貼到別處，OpenAI 說沒有用到憑證，也沒有碰到非公開資料；教育部：研究人員說有一次針對民權辦公室網站的粗糙入侵嘗試，沒有成功，教育部查過後說「沒有任何證據顯示網站或資料庫受到影響」）；`quote`：教育部的這句話 |
| 4 | Medicare 入口網站與三個月的空窗（The Medicare portal and the three-month gap） | 80 | `steps`：6 月 18 日代理進入 Medicare 統計入口網站（全片唯一一起政府網站被闖入的事件）→ 8 月發現 → 9 月 10 日寄信通知（寄到一般信箱）→ 10 月 1 日參議院在坎培拉舉行聽證；`big`：「3 個月」；`chat`：一般民眾會問的問題，對照 OpenAI 公開的說法 |
| 5 | 沒人叫，代理為什麼會這樣做（Why an agent does this without being told） | 90 | `compare`：聊天機器人（回答問題）對上代理（目標 + 工具 + 迴圈）；`bullets`：牆是什麼（權限、網路、憑證），以及提示詞為什麼不是牆 |
| 6 | 三道牆，在真的代理上示範（The three walls, shown on a real agent） | 100 | `steps`：工具全關／允許清單／工作目錄；`code`：真實的指令與輸出；`chat`：代理真實的回覆（工具全關時，它只說要去抓網頁，接著什麼也沒發生）；`compare`：沒有牆的時候碰得到哪些東西 |
| 7 | 今年秋天上市的代理，對你代表什麼（What this means for the agents shipping this fall） | 30 | `outro`：「代理不需要壞心眼也會闖禍；牆比指令管用」；一個下一步：下面那個留言問題 |

實作示範在第 6 章。結尾的下一步：「你準備把電腦交給哪一個代理？留言告訴我；下一支影片會一步一步帶你看，代理實際上都在做什麼。」（接到 `always-on-agent-explained`）。總長約 610 秒，中文旁白約 2,500 字（每分鐘 250 字）。

### 選項 B：先教三道牆，再用事件驗證

一行說明：先教三道牆的框架，再把每起事件當成少了其中一道牆的案例，比選項 A 更適合長青搜尋（「AI 代理安全嗎」、「are AI agents safe」），但在新聞熱度期比較吃虧。

開場鉤子（口播）：「你裝的每一個 AI 代理，都會拿到三樣東西：能執行的東西、能連線的地方，還有看得到的機密。今年夏天，OpenAI 自己的代理就示範給我們看：這三樣都沒人設限，會發生什麼事。」

章節：三道牆（The three walls，90 秒：`title`、`steps`，如果有畫原創 SVG 就加 `diagram`）→ 少了第一道牆：Hugging Face（Wall 1 missing: Hugging Face，120 秒）→ 少了第二道牆：政府網站（Wall 2 missing: government sites，110 秒：`table`）→ 少了第三道牆：圖片和資料被貼到外面（Wall 3 missing: images and data posted outside，90 秒：`stats`）→ Medicare 的空窗與通報（The Medicare gap and disclosure，80 秒）→ 今天就看你的筆電：真實執行（Your laptop, today: the real run，90 秒）→ `outro`（30 秒）。

## 會過期的事實

| 事實 | 寫稿日到哪裡重新確認 |
| --- | --- |
| 被貼出去的圖片數、收到通知的組織數、OpenAI 審查的進度（影片不給代理數量與酬載數量） | openai.com/index/hugging-face-incident-and-the-road-ahead/（我們的抓取工具在 2026-09-28 拿到 HTTP 403，要由真人打開），以及 OpenAI 之後的聲明 |
| 人口普查局、SEC、教育部的細節，以及教育部的聲明 | nextgov.com 2026-09 的報導，以及教育部自己的聲明 |
| 澳洲時間線（6 月 18 日存取、8 月發現、9 月 10 日通知、10 月 1 日參議院聽證）以及調查的結論 | Services Australia 與澳洲參議院的網頁；AI Weekly 的整理只算二手資料 |
| 只用一句帶過的監管後續（紐約市議會的 10 項法案、Sanders–Casar 法案） | 紐約市議會與美國國會的官方網頁；只陳述事實，不做評論 |
| 示範用到的 CLI 參數 | 寫稿日當天該 CLI 的官方文件 |

## 素材

- 只用文字引言（`quote` 版型），出自 OpenAI 的貼文和具名媒體，每一則都附出處與日期。
- 不放政府網站截圖、不放品牌標誌、不放任何人的影像。
- 可選：一張為這支影片原創繪製的 SVG（代理的迴圈加上三道牆），存放在 `docs/videos/openai-agents-broke-in/`。

## 不做的事

- 不講漏洞利用的細節，也不重現任何攻擊；不點名個別員工。
- 不揣測動機或「意識」；不提供責任歸屬的法律建議。
- 不談股票、估值或投資角度。
- 不做特定代理產品的資安評測；那是第 4 支影片的內容。
