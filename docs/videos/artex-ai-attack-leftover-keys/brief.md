# AI 駭客不到 3 小時打進雲端：它沒有猜你的密碼，是撿走你放著的鑰匙（ARTEX）

企劃日期 2026-10-26。AI／科技時事，**教學卡片短片**（`format: "slides"`、`category: "ai-news"`、`theme: "paper"`，
teaching-flow §十「一個概念」＋§十二 畫面規格；結構接 `php2shell-ai-found-it-first`，但例子、開場與卡片順序都換掉）。
字卡主語言 zh-TW，產品、工具、設定名稱、引文、數字、指令保留英文（SKILL.md 規矩 14）。
站上沒有這則新聞的文章，所以沒有 `source_guide`、沒有 `cta`。

事實來源（2026-10-26 都開過，原始 HTML 存在工作區 `_tools/sources/`）：
Microsoft Threat Intelligence 2026-10-21 的報告（Storm-0940、ARTEX、ConnectWise、時間與次數）；
91APP 2026-10-22《2026 遭受駭客攻擊事件 18 天調查報告》新聞稿（ARTEX 痕跡、Appsmith、GitLab 裡的資料庫金鑰）；
Zeabur 2026-10-19 初步報告與 10-17 停止營運公告（明文、無期限的管理憑證、八月沒輪替到）；
GMO サイバーセキュリティ by イエラエ 10-19 的調查（ScanNetSecurity 10-21、iThome 轉述）；
iThome 2026-10-21 對數發部資安署示警記者會的報導（韓國 7 家金融機構、國內 7 月監測、AI 會放棄基礎扎實的企業）；
Google 帳戶說明「變更或重設密碼」「管理 Google 帳戶與第三方應用程式之間的連結」；GitHub Docs「Removing sensitive data from a repository」「Reviewing your authorized OAuth apps」。
本片有一次**本頻道自己跑的紀錄**：2026-10-26 在 Ubuntu 24.04.5 LTS、git 2.43.0 上建一個示範倉庫，看刪掉的 `.env` 還在不在歷史裡（`terminal` 卡，`ran_on` 2026-10-26）。

## 先搜（news-flow §一；YouTube 搜尋依觀看數、本週，2026-10-26，十三組查詢；訂閱數與逐字稿本機沒抓）

| 題目（節錄） | 頻道 | 長度 | 觀看 | 上架 |
| --- | --- | --- | --- | --- |
| 【緊急】マイクロソフトが発表、世界を狙ったAIサイバー攻撃の"黒幕"⇒中国政府系ハッカーの恐ろしい手口が判明… | 令和政治ナビ | 8:30 | 52 萬 | 3 天前 |
| 'BLACK OCTOBER': AI Cybersecurity NIGHTMARE As BANKS Infiltrated | Breaking Points | 18:00 | 50 萬 | 4 天前 |
| The shadow of Chinese AI agent "ARTEX" behind cyberattacks: Unstoppable data breaches hit police ... | TBS NEWS DIG | 5:12 | 42 萬 | 6 天前 |
| It's Happening... AI Just Started the Biggest Internet Nightmare in History | AI Revolution | 14:06 | 26 萬 | 2 天前 |
| Calmly analyzing the "ARTEX" controversy from China: Why were Japanese companies targeted? | 海外Yパパラジオ | 17:17 | 18 萬 | 3 天前 |
| Surge in Unauthorized Access: The Rise of Chinese AI【NIKKEI NEWS NEXT】 | テレ東BIZ | 10:05 | 7 萬 | 2 天前 |
| Global Cybersecurity Nightmare "Black October": 91APP and Zeabur Hit by Hacks, PHP Vulnerability ... | fOx Hsiao | 11:50 | 2.3 萬 | 2 天前 |

讀法：日本台講「中國 AI 打日本企業」，英文台講「AI 讓網攻失控」，都在講**誰打的、打了誰**；沒有一支講**它實際從哪裡進去**。
三份官方說法（Microsoft、91APP、資安署）指向同一件事：AI 沒有新開一個洞，是在幾小時內把放著的鑰匙找出來用掉。這支切的就是這個概念，
收在觀眾自己能跑的檢查。完整研究紀錄與另外三群候選在 `docs/videos/reference-study-20261026-ai-news/README.md`。長度照短片 8–9 分鐘。

## 觀眾

在台灣用 Google 帳號登入一堆服務的一般人；有 GitHub 帳號、會把專案推上去的工程師與 vibe coding 的新手；替小公司管 Microsoft 365 或雲端的人；
以及在 91APP 合作品牌買過東西、這週收到防詐通知、想知道「AI 駭客」到底是什麼的人。
他們搜尋的是「ARTEX 是什麼」「AI 駭客 攻擊」「91APP 個資外洩」「Zeabur 被駭」「改密碼有用嗎」。
他們以為 AI 駭客就是「很會猜密碼的程式」，所以以為設了長密碼、開了兩步驟驗證就沒事；不知道授權過的 App、沒期限的金鑰、
刪掉的檔案留在 git 歷史裡，這幾樣不需要密碼就能用。

## 觀眾看完能做到的事

- 從一個「已經刪掉」的設定檔，用一行 `git log -p -G <你的金鑰名稱>` 找出它還在 git 歷史裡，再用 `git show` 拿回整個檔案；把 `PASSWORD` 換成自己專案的金鑰名稱（`API_KEY`、`sk-`、`SECRET`）重跑
  （第 6 章，三張 `terminal` 卡；RUN：本機 2026-10-26，git 2.43.0，示範倉庫 `shop-demo`）。
- 找到之後做對的那一步：先撤銷或輪替那把金鑰，不是先改寫歷史；知道只改寫歷史，複本、fork 與快取裡的那一份還在
  （第 6 章，`quote`＋`steps` 卡；CITED：GitHub Docs「Removing sensitive data from a repository」原句 "as a first step you need to revoke and/or rotate that secret"）。
- 在 Google 帳戶的「連結的應用程式」與 GitHub 的「Authorized OAuth Apps」裡，找出不認得或不再用的授權並移除；知道為什麼要做這件事而不是只改密碼：
  Google 寫明改密碼會登出所有裝置，**例外是你已經授權存取權的第三方應用程式**
  （第 5、6 章，`quote`＋`steps` 卡；CITED：Google 帳戶說明兩頁、GitHub Docs「Reviewing your authorized OAuth apps」；不登入任何人的帳戶畫面）。
- 管 Microsoft 365 的人：照 Microsoft 10-21 報告的清單，查服務主體（service principal）的登入、應用程式認證的新增與權限變更，而不是只看使用者登入
  （第 6 章，`bullets` 卡；CITED：Microsoft 報告〈Immediate actions〉）。

## 站主觀點

（頻道立場的文字沒有隨這次的啟動訊息帶進來，所以這一段是提案，站主選大綱時確認或改寫。）
我的看法是：ARTEX 這一波最值得記住的不是「中國駭客用 AI」，是 Microsoft 自己的數字——15 萬次猜密碼全部失敗，真正進去的是早就被允許的 App；
91APP 是一套沒更新的內部工具加上 GitLab 裡的一把資料庫金鑰。AI 沒有發明新的入口，它只是讓「放著的鑰匙」在三個小時內被找到。
資安署說 AI 評估成本後會放棄基礎扎實的企業，我把這句話當成一個好消息：一般人和小公司能做的事，就是讓自己不是那個最便宜的門。
我查不到的事：91APP 實際影響多少會員（報告說下週公布）、台灣 7 月那次 AI 攻擊是不是 ARTEX（資安署沒說工具名）、Zeabur 的攻擊者有沒有用 AI 工具（報告沒提）。

## 示範或實算

製作路線：教學卡片短片，`theme: "paper"`。一個生活對照撐全片：**門墊下的備用鑰匙**——小偷不撬鎖（猜密碼），翻每一家門墊（授權過的 App、沒期限的金鑰、
刪掉卻還在歷史裡的設定檔）；AI 讓小偷一個晚上翻幾千家，而且會跳過門墊下沒東西的那一家。哪裡不能照比喻理解：門墊上的鑰匙你看得到，
這些鑰匙你通常忘了自己放過（授權是好幾年前按的「允許」、金鑰在八月輪替時漏掉）。

- 主例（RUN，2026-10-26，Ubuntu 24.04.5 LTS，git version 2.43.0；示範倉庫 `shop-demo`，兩個提交的日期固定成 2026-09-01、09-02，密碼是假的 `demo-not-a-real-secret`）：
  1. 建倉庫、提交 `.env`（`DB_HOST=orders-db.internal`、`DB_PASSWORD=demo-not-a-real-secret`），下一個提交 `git rm .env` 並把 `.env` 寫進 `.gitignore`。
  2. `ls -A` → `.git`、`.gitignore`（資料夾裡看不到 `.env`）。
  3. **不用這個方法（觀眾今天最簡單的一步）：** `grep -rn PASSWORD --exclude-dir=.git .` → 沒有輸出，exit 1。看資料夾、搜尋檔案都說「密碼已經不在了」。
  4. `git log --oneline` → `984e6d1 remove secrets from repo`、`b3faea1 add db config`。
  5. `git log -p -G PASSWORD --format='%h %ad %s' --date=short` → 兩個提交都列出來，`-DB_PASSWORD=demo-not-a-real-secret`（刪除那一筆）與 `+DB_PASSWORD=demo-not-a-real-secret`（新增那一筆）。
  6. `git show b3faea1:.env` → 整個檔案兩行原樣印出。
  觀眾猜不到的結果：「刪掉了、也加進 `.gitignore` 了」，一行指令還是拿得回來；這就是 91APP 報告說的「自 GitLab 取得資料庫金鑰」那一類鑰匙放的地方（只說同一類，不說 91APP 是這樣放的）。
  逐字輸出在工作區 `_tools/run/transcript.txt`；每行 ≤ 78 欄、沒有家目錄、提示字元只有 `$ `。
- 觀眾自己的那一行：把 `-G PASSWORD` 換成自己專案的金鑰名稱（`-G API_KEY`、`-G 'sk-'`），卡片上那一格標成「換成你的」。
- 對照（CITED）：GitHub Docs 說找到後第一步是撤銷或輪替，改寫歷史有副作用、複本與 fork 還在；Zeabur 報告說八月的輪替沒有涵蓋設定儲存庫裡的明文權杖，
  十月被用的正是那些——同一個教訓的另一面：輪替要輪到每一把。
- 要先實作：沒有。Google 與 GitHub 的授權頁需要登入，本頻道不登入任何人的帳戶錄畫面，那兩步用官方說明頁的步驟（`steps`），證據等級 CITED；
  不做任何攻擊示範、不碰 ARTEX 本身、不放它的連結。
- 示範在第 6 章（三張 `terminal`、一張「找到之後」的 `steps`、一張 Google／GitHub 的 `steps`、一張 Microsoft 365 管理員的 `bullets`）。

## 大綱

### 選項 A（推薦）：放著的鑰匙——照觀眾會問的順序走，收在一行找得到「已刪除」金鑰的指令

角度：整支只講一個概念「AI 攻擊不是撬鎖，是在幾小時內撿走放著的鑰匙」，章名是觀眾的問題；跟 B 差在不照國家與時間線講、跟 C 差在不以工具與開發者為主角。

開場（五句，20 秒內）：「10 月 21 日，Microsoft 公布：一個中國政府相關的駭客組織用 AI 工具 ARTEX，同時攻擊全球幾百個組織，有好幾次從鎖定到拿下雲端管理權限不到三小時；隔天台灣的 91APP 也在自己的系統裡找到 ARTEX 的痕跡。」／
「你可能會問：我又不是大公司，密碼也夠長，這種 AI 駭客跟我有什麼關係？」／「有關係，因為它進門的方法不是猜密碼：Microsoft 記錄到其中一波十五萬次猜密碼全部失敗，真正進去的，是早就被允許的 App 和沒人記得的金鑰。」／
「這些鑰匙你家也有：好幾年前按過『允許』的 App、刪掉卻還留在 git 歷史裡的設定檔，改密碼也收不回來。」／「接下來用三個官方報告講它從哪裡進去，再跑一行指令，把一個已經刪掉的密碼從歷史裡拿回來。」

案例與結果：「示範倉庫刪掉 `.env` 之後，`grep` 找不到密碼、`git log -p -G PASSWORD` 與 `git show` 把整個檔案拿回來；證據 RUN（2026-10-26，git 2.43.0）＋ CITED（GitHub Docs 先輪替）。」

例子在每章開頭的狀態：第 1–2 章只出現「門墊」；第 3 章門墊上是「授權過的 App」（Microsoft）；第 4 章多了「GitLab 裡的金鑰」「明文、沒期限的權杖」；第 5 章「換鎖（改密碼）收不回門墊下那把」；第 6 章翻自己的門墊（示範倉庫）。
旁白先講出來再答的疑問（§三）：「我又不是大公司」（第 1 章）、「我開了兩步驟驗證還不夠？」（第 3 章）、「那改密碼不就好了？」（第 5 章）、「我刪掉了啊？」（第 6 章）、「刪掉歷史就好？」（第 6 章）。
「我」的來源（§五）：執行紀錄（我刪掉的 `.env` 一行就回來）、頻道立場（不做攻擊示範）、查不到的事（91APP 影響人數、台灣 7 月那次是不是 ARTEX）。

1. ARTEX 是什麼？（50 秒）`title` → `big`（你可能會問）→ `big`（不是猜密碼：15 萬次 0 成功）→ `big`（利害：改密碼收不回）→ `bullets`（承諾：三份報告、一行指令）。
2. 跟我有關嗎？我又不是大公司（80 秒）`stats`（韓國 7 家金融機構、日本約 20 家、台灣 91APP）→ `quote`（資安署：AI 評估成本後放棄扎實的企業）→ `big`（AI 不挑大小，挑便宜）→ `compare`（撬鎖的小偷／翻門墊的小偷）。收尾問題：「那它到底從哪裡進去？」
3. AI 到底怎麼進去的？（95 秒）`screencast`（Microsoft 報告標題與第一段）→ `stats`（151,000 次失敗、98% 被鎖、0 次成功）→ `big`（你可能會想：兩步驟驗證擋住了，不就好了？）→ `quote`（"through applications that had already been granted access … without requiring an interactive user sign-in"＋translation）→ `big`（numeral 3：不到三小時）。收尾問題：「台灣這次的鑰匙放在哪？」
4. 鑰匙放在哪？三個例子（90 秒）`table`（UTC 一格一件事：10/3 91APP 訂單資料庫、10/14 Zeabur、10/16 ConnectWise 公告、10/19 GMO、10/21 Microsoft、10/22 91APP 報告）→ `steps`（91APP：沒更新的 Appsmith → 內網 → GitLab 裡的金鑰 → 訂單資料庫）→ `big`（Zeabur：明文、沒期限、八月沒輪替到；報告沒提 AI，只當同一類鑰匙）→ `quote`（Zeabur「即使八月事件後已經換過」）。收尾問題：「那我改個密碼總行吧？」
5. 換了密碼不就好了？（70 秒）`quote`（Google：改密碼登出所有裝置，例外是授權過的第三方應用程式）→ `big`（換了鎖，門墊下那把是另一扇門的）→ `quote`（Microsoft：改過的應用程式認證在原本的 App 修好後仍可當後門）→ `big`（所以要找的是鑰匙，不是鎖）。收尾問題：「我自己的門墊下有什麼？」
6. 我自己的鑰匙怎麼找？（130 秒）`terminal`（ls -A＋grep：找不到）→ `big`（問題來了：真的刪掉了嗎？）→ `terminal`（git log -p -G PASSWORD）→ `terminal`（git show b3faea1:.env）→ `big`（刪掉、加了 .gitignore，一行就回來）→ `code`（換成你的金鑰名稱）→ `quote`（GitHub Docs：先撤銷或輪替）→ `steps`（找到之後：輪替 → 再決定要不要改寫歷史 → 通知有複本的人）→ `steps`（Google 連結的應用程式、GitHub Authorized OAuth Apps）→ `bullets`（Microsoft 365 管理員：服務主體登入、認證新增、權限變更）。收尾：回到開場那句「改密碼收不回」。
7. 我的看法：現在先做什麼（60 秒）`big`（AI 沒發明新入口，只是找得更快）→ `big`（我查不到的）→ `steps`（今天：連結的應用程式；這週：自己的倉庫跑一次；之後：金鑰設期限）→ `big`（答案：不是最便宜的那扇門）→ `big`（留言題：你清掉了幾個連結的應用程式？）→ `outro`。

### 選項 B：一個月、三個國家——ARTEX 從韓國銀行走到日本企業、再到台灣電商

角度：事件型，照時間一格一格走（9 月下旬韓國金融機構、10/3 91APP、10/7 CrowdStrike、10/19 GMO、10/21 Microsoft、10/22 91APP 報告），每一格帶一個「鑰匙放在哪」。
跟 A 差在時間線是主線、觀眾的檢查只在最後一章；跟 C 差在不談工具本身。
開場：「9 月底，韓國幾家銀行的資料開始外流；一個月後，同一套 AI 工具的痕跡出現在台灣一家電商的系統裡。」
章節：1. 韓國（60 秒）2. 日本（70 秒）3. Microsoft 看到的全貌（90 秒）4. 台灣（90 秒）5. 為什麼是這些公司（60 秒）6. 你的檢查（100 秒）7. 結尾（40 秒）。
風險：觀眾最想知道的「關我什麼事」要等到第 5 章；韓國那一格只有資安署轉述與 CrowdStrike 的二手報導（CrowdStrike 原文本機沒開到），要補官方來源。

### 選項 C：一個為「找洞」寫的工具，怎麼變成攻擊武器

角度：以 ARTEX 本身為主角：7 月公開、資安院說比人工快 10 倍以上、開發者在攻擊被報導後關閉原始碼；主線是「AI 滲透測試工具的兩面」，收在防守方也能用同一類工具先找自己的鑰匙。
跟 A 差在主角是工具與開發者、觀眾的檢查只佔一章；跟 B 差在不走時間線。
開場：「ARTEX 是一套讓 AI 自己做滲透測試的開源工具，寫它的人說，攻擊跟這個專案的目的無關。」
章節：1. 它是什麼（60 秒）2. 為什麼比人快（80 秒）3. 誰拿去用了（90 秒）4. 開發者關掉之後（60 秒）5. 防守方用同一招（90 秒）6. 你的檢查（80 秒）7. 結尾（40 秒）。
風險：開發者的說法、競賽奪冠、7 月公開這幾件只有媒體與資安院的轉述；容易被讀成在介紹攻擊工具（規矩：攻擊細節只講時間與誰說的），站主立場要的「觀眾能做的動作」最弱。

## 會過期的事實

- Microsoft 報告（次數、時間、受影響組織的說法、建議清單；報告可能更新）：https://www.microsoft.com/en-us/security/blog/2026/10/21/storm-0940-uses-artex-agentic-ai-connectwise-supply-chain-compromise/
- 91APP 調查報告（下週會更新受影響範圍）：https://91app.com/blog/91app-202610-security-incident/ 、報告頁 https://91app.com/91app-202610-security-incident/
- Zeabur 初步報告（調查進行中，會更新）：https://zeabur.com/zh-TW/blogs/october-2026-security-incident ；停止營運時程：https://zeabur.com/zh-TW/blogs/zeabur-is-shutting-down
- 資安署 10-21 示警（數發部官網新聞稿本機還沒開到，撰稿時要找原文；現在用 iThome 報導）：https://www.ithome.com.tw/news/179865
- GMO 的家數與攻擊主機數（媒體有「約 80 家」與「約 20 家」兩種，用 GMO 自己的約 20 家、6 台）：https://scan.netsecurity.ne.jp/article/2026/10/21/56522.html 、https://www.ithome.com.tw/news/179850
- 91APP 與 ARTEX 的報導：https://www.ithome.com.tw/news/179923
- Google 改密碼的例外：https://support.google.com/accounts/answer/41078?hl=zh-Hant ；連結的應用程式：https://support.google.com/accounts/answer/13533235?hl=zh-Hant
- GitHub：https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository 、https://docs.github.com/en/apps/oauth-apps/using-oauth-apps/reviewing-your-authorized-oauth-apps

## 素材

- `screencast`：Microsoft 報告頁（公開頁；截標題與第一段；也是縮圖主體 `thumbnail.data.capture`），91APP 新聞稿頁（標題與第一段）
- 三張 `terminal` 卡的指令與輸出逐字取自 2026-10-26 本機執行紀錄（上面「示範或實算」）；工具版本寫 git 2.43.0、Ubuntu 24.04.5 LTS
- 原始頁面的 HTML 與純文字存在工作區 `_tools/sources/`（msft、91app、zeabur、zeabur-close、ithome-179804、ithome-179850、ithome-179865、ithome-179896、ithome-179923、scan-gmo、google-pw、google-3p、gh-sensitive、gh-reviewing-your-authorized-oauth-apps，2026-10-26 存）
- 不放 ARTEX 的 GitHub 或任何連結、不截它的介面、不畫 AI 插圖、不用任何人的帳戶畫面；不念、不寫任何攻擊 IP

## 不做的事

- 不講 ARTEX 怎麼裝、怎麼用、怎麼設定；不示範任何攻擊或密碼噴灑
- 不說 Zeabur 被 ARTEX 或 AI 攻擊（它的報告沒這樣說）；不說台灣 7 月那次是 ARTEX（資安署沒說工具名）
- 不下「中國」「AI 好可怕」之類的結論，歸屬一律寫「Microsoft 評估」「GMO 研判」，不加形容詞
- 不講 91APP 受影響的品牌名單與人數（報告說下週公布）；不評論 91APP 通知得早不早
- 不講銀行 AI 代理（Axios 那一群）、不講 ConnectWise 產品細節與它的客戶該怎麼還原備份
