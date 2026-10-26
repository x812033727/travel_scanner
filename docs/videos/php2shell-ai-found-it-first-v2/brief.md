# AI 先找到 PHP 的洞，全球網站卻自己關站：PHP2Shell 四天內發生了什麼，你的網站怎麼查

企劃日期 2026-10-25。AI／科技時事，**教學卡片短片**（`format: "slides"`、`category: "ai-news"`、`theme: "paper"`，
teaching-flow §十「一個概念」＋§十二 畫面規格；範本是 `claude-duet-proactive-agent`、`google-ai-search-ads-exception` 的紙底版，PR #1700、#1833）。
字卡主語言 zh-TW，產品與設定名稱、引文、數字、指令保留英文（SKILL.md 規矩 14，PR #1843）。
站上沒有這則新聞的文章（2026-10-25 查 mokaair.com/zh-TW/life 的 ai-news 清單，沒有 PHP2Shell），所以沒有 `source_guide`、沒有 `cta`。

事實來源：PHP 官方公告（php.net 2026-10-20 預告、10-21 安全公告、10-23 資訊性建議）、PHP Foundation 2026-10-21 的部落格（稽核、延遲、走漏與破埋的時間）、
Wiz 2026-10-21 的研究文（70%、5.4 起、用的模型、時間表）、Cloudflare 2026-10-21 的部落格（WAF 03:02 UTC、免費方案）、AWS 安全部落格（蜜罐 10-17）、
watchTowr 的 FAQ（版本表、CISA KEV 狀態）、Ubuntu 的 CVE 頁（24.04 修好的套件版本）、Debian 安全追蹤頁、英國 NCSC 的公告、新加坡 CSA 的警訊、
數位發展部資安署 2026-10-22 新聞稿、iThome 2026-10-22 對資安署署長記者會的報導（2.8 萬、200）、BBC 2026-10-21／23 的報導（各國下線、日本首相、Cloudflare 執行長的數字）、
Japan Cyber Watch 2026-10-23（日本停站的服務與時間）、Hacker News 走漏貼文（Algolia API 的時間戳）。OpenAI 自己的文章 openai.com/index/php2shell 對本機回 403，只用 Greg Brockman 在 X 上的原句與 PHP Foundation、TechTarget 的轉述。
本片有一次**本頻道自己跑的紀錄**：2026-10-25 在一台 Ubuntu 24.04.5 的測試機上查 PHP 版本、套件版本與套件更動紀錄（`terminal` 卡，`ran_on` 2026-10-25）。

## 先搜（teaching-flow §十一；YouTube 搜尋依觀看數、本週，2026-10-25，`search_query` 四組英文；訂閱數本機拿不到，watch 頁回 429）

| 題目（節錄） | 頻道 | 長度 | 觀看 | 上架 |
| --- | --- | --- | --- | --- |
| Websites taken down worldwide as AI reveals critical cyber-security threat | BBC News | 1:57 | 225 萬 | 3 天前 |
| PHP flaw: How AI just hacked an unhackable part of the internet (About That) | CBC News | 11:29 | 63 萬 | 1 天前 |
| The PHP internet crisis could just be the beginning | Sky News | 6:21 | 62 萬 | 2 天前 |
| Websites went down around the world. Did AI stop it getting worse? | BBC News | 14:09 | 36 萬 | 2 天前 |
| Elon's $100B AI Bet, Anthropic's Claude Duet, and the PHP Flaw Hiding in 70% of the Web | Peter H. Diamandis | 2:25:00 | 20 萬 | 1 天前 |
| The OPENAI Cyberattack on Hugging Face Was WAY BIGGER Than We Thought | The Infographics Show | 17:53 | 27 萬 | 1 天前 |
| Did Google just dethrone OpenAI and Anthropic?（Gemini 4 Argon） | Fireship | 6:33 | 186 萬 | 4 天前 |
| AI agents accessing bank accounts without approval, report says | CBS News | 5:22 | 22 萬 | 1 天前 |
| Claude Made My Old Android TV Feel Brand New!（同題七支 15–93 萬） | Ansub Khan 等 | 4:02–12:31 | 16–93 萬 | 2–6 天前 |

讀法：本週 AI 時事裡被最多家、最大量觀看的是 PHP2Shell（新聞台 2–14 分鐘，標題都是「發生了什麼、為什麼網站下線」）；
大台已經把「發生了什麼」講完，所以這支切**一個概念**：洞在引擎不在車身、修補是一條鏈、版本號看不出修沒修——用本機真的跑過的檢查收尾，這是新聞台沒做的事。
長度照短片 8–9 分鐘。完整的研究紀錄在 `docs/videos/reference-study-20261025-ai-news/README.md`。

## 觀眾

在台灣有自己的網站（WordPress、公司官網、電商、社團網站）、或替老闆管網站、或只是看到「全球網站下線」的新聞想知道「關我什麼事、要做什麼」的人。
他們搜尋的是「PHP2Shell 是什麼」「PHP 漏洞 WordPress 要更新嗎」「PHP 8.3.36」「網站 為什麼 下線 PHP」。
他們知道 WordPress 要更新，不知道 PHP 是另一層、不知道主機商的套件會用舊版號出貨、也不知道那個流傳的「關一個設定就安全」是假的。

## 觀眾看完能做到的事

- 在自己的主機或主機商後台查出 PHP 版本，對照四個安全版本號（8.5.12、8.4.27、8.3.36、8.2.35），判斷自己的分支修了沒；8.1 以下的站知道官方不再出版本、要換分支或靠發行版
  （第 6 章，`table` 卡＋`terminal` 卡；RUN：本機 2026-10-25 `php -v` 得 8.3.6；CITED：php.net 2026-10-21 公告）。
- 看到版本號「看起來沒修」時，再看一層：用 Linux 發行版套件的，查套件版本與更動紀錄裡有沒有 CVE-2026-109618／109619，因為發行版事先拿到修補、用舊版號打包
  （第 6 章，兩張 `terminal` 卡；RUN：本機 2026-10-25 `dpkg-query` 得 `8.3.6-0ubuntu0.24.04.13`、changelog 第 1、3、4 行；CITED：ubuntu.com/security/CVE-2026-109618 列 24.04 修好的版本就是這一串；php.net「Linux distributions and LTS vendors received the patches in advance」）。
- 分辨「修補」與「緩解設定」：知道 `session.upload_progress.enabled=0` 只擋部分路徑、更新 WordPress 不等於更新 PHP、修好要重啟工作程序
  （第 6 章，`bullets` 卡；CITED：php.net 2026-10-21「only an update is a complete solution」、10-23 資訊性建議）。
- 把「要不要先關站」當成一個決定而不是失敗：說得出英國 NCSC、日本國家網路統括室、台灣資安署各自的順序（修補 → 防火牆 → 暫停）
  （第 5 章，`quote`＋`big` 卡；CITED：ncsc.gov.uk 2026-10-21；資安署新聞稿與 iThome 2026-10-22；Japan Cyber Watch 2026-10-23）。

## 站主觀點

（頻道立場的文字沒有隨這次的啟動訊息帶進來，所以這一段是提案；站主 2026-10-23、10-24 都說過大綱照推薦直接做。）
我的看法是：AI 把「找洞」從幾年壓成一週，這是真的；但「修洞」還是一條人的鏈——維護者要在幾種修法裡選一種、發行版要打包、主機商要部署、
站長要重啟，而這條鏈最弱的一環是兩個多月的保密只差兩天就破了。所以全球網站自己關站不是恐慌，是鏈還沒走完時唯一安全的位置。
我在意的不是「AI 好可怕」，是三件觀眾今天就能做的事：查版本、查套件紀錄（版本號會騙你）、分清楚緩解設定不是修補。
台灣那兩萬八千個站到今天修好了多少，我查不到；資安署說會持續掌握進度，我就照它的順序講：先修，修不了先上防火牆，都不行才暫停。

## 示範或實算

製作路線：教學卡片短片，`theme: "paper"`，字卡 zh-TW、名詞與指令英文；一個生活對照撐全片：**汽車召回**——瑕疵在引擎（PHP）不在烤漆和座椅（你的網站程式）；
召回公告有人提前貼到網上（走漏）；車廠把召回提前一天；修車廠（發行版、主機商）事先拿到零件；路上已經有人在試這個瑕疵（蜜罐）；車先停到路邊（網站自己關站）；
修好引擎之後行照上的年份不會變（版本號 8.3.6 不變），要看維修紀錄（套件的 changelog）。哪裡不能照比喻理解：召回可以排時間，這次不行，公告當天攻擊就上百萬次。

- 主例（RUN，2026-10-25，Ubuntu 24.04.5 LTS，PHP 8.3.6 (cli)，dpkg 1.22.6）：
  1. `php -v` → `PHP 8.3.6 (cli) (built: Oct 19 2026 15:16:58) (NTS)`（四行）。對照 php.net 的表，8.3 分支要 8.3.36，看起來差 30 個版本。
  2. `dpkg-query -W -f='${Package} ${Version}\n' php8.3-cli` → `php8.3-cli 8.3.6-0ubuntu0.24.04.13`。
  3. `zcat /usr/share/doc/php8.3-cli/changelog.Debian.gz | head -n 4` → 第 1 行 `php8.3 (8.3.6-0ubuntu0.24.04.13) noble-security; urgency=medium`、第 3 行 `* SECURITY UPDATE: Remote RCE via state corruption issue`、第 4 行 `- debian/patches/CVE-2026-109618_109619.patch: Avoid state corruption via`。
  4. 對照 ubuntu.com/security/CVE-2026-109618：php8.3 在 24.04 noble「Fixed in 8.3.6-0ubuntu0.24.04.13」。結論：版本號說沒修，套件紀錄說修了；這就是觀眾猜不到的結果。
  另外 `php -i | grep session.upload_progress.enabled` → `On => On`（預設開著；只當 10-23 建議那張卡的背景，不上畫面）。
- 不用這個方法：觀眾今天最簡單的一步是在主機商後台看一眼 PHP 版本。這支片比那一眼多的，是：版本號對發行版套件會騙人、要看哪一行、四個分支各自的安全版本、以及緩解設定為什麼不算修補。
- 對照（CITED）：php.net 2026-10-21 公告的版本表與「Linux distributions and LTS vendors received the patches in advance」；Debian 安全追蹤頁（bookworm 8.2.35-1~deb12u1、trixie 8.4.27-1~deb13u1）。
- 要先實作：沒有。本機沒有 Apache／mod_php 可以示範攻擊面，攻擊細節一律引用官方公告與研究文，不做任何攻擊示範。
- 示範在第 6 章（三張 `terminal`、一張版本表、一張三種查法的 `steps`、一張三個誤會的 `bullets`）。

## 大綱

### 選項 A（推薦）：洞在引擎不在車身——照觀眾會問的順序走，收在一條版本號看不出來的檢查

角度：整支只講一個概念「PHP2Shell 的洞在 PHP 這顆引擎，所以修補是一條鏈、版本號不能告訴你修沒修」，章名是觀眾的問題；跟 B 差在不照時間線講、跟 C 差在不以 AI 為主角。

開場（五句，20 秒內）：「10 月 21 日，PHP 發了緊急安全更新，兩個漏洞合稱 PHP2Shell；前一晚日本首相請全國站長當晚檢查網站。」／
「你可能會問：我的網站是 WordPress，又不是我寫 PHP，關我什麼事？」／「有關：洞在 PHP 本身，不用登入，一個請求就能在伺服器上執行程式、讀出記憶體裡的密碼、改掉網站。」／
「正因為洞在底層，你的程式再乾淨也擋不住，而且修補公開前四天就有人在試。」／「看完你會知道：AI 怎麼在兩個月前找到它、修補為什麼提早一天、四個安全版本號，和一條光看版本號看不出來的檢查。」

案例與結果：「本機 `php -v` 得 8.3.6、對照表應該沒修；`dpkg-query` 與 changelog 證明 Ubuntu 的 8.3.6-0ubuntu0.24.04.13 已含 CVE 修補；證據 RUN（2026-10-25）＋ CITED（ubuntu.com、php.net）。」

1. PHP2Shell 是什麼？（55 秒）`title` → `big`（你可能會問）→ `big`（動詞清單）→ `big`（利害）→ `bullets`（承諾四樣）。
2. 跟我有關嗎？我又不寫 PHP（85 秒）`big`（numeral 69：七成網站）→ `compare`（車身／引擎）→ `big`（mod_php 風險最高）→ `stats`（台灣 2.8 萬、200、0）→ `big`（這個洞在 PHP 裡多久了？）。收尾問題：「為什麼現在才被找到？」
3. AI 怎麼找到的？（95 秒）`big`（2024 稽核看到徵兆）→ `quote`（PHP Foundation：structural failure）→ `steps`（7/30、8/11、8/24、原定 10/22）→ `big`（一個人一週）→ `quote`（Wiz：Heartbleed）→ `big`（你可能會想：好事還是壞事？先放著）。
4. 修補為什麼提早一天？（95 秒）`big`（10/20 15:20 UTC 走漏）→ `table`（六個時間點）→ `stats`（數千→數百萬）→ `big`（Amazon 蜜罐 10/17）。收尾問題：「網站能做什麼？」
5. 網站為什麼自己關站？（80 秒）`quote`（NCSC）→ `bullets`（日本、荷蘭、芬蘭與英國、維基媒體）→ `big`（日本首相）→ `big`（台灣：修補→WAF→暫停）。收尾問題：「我怎麼知道我的修到了沒？」
6. 修好了嗎？看版本就夠？（120 秒）`screencast`（php.net 公告）→ `table`（四個安全版本）→ `terminal`（php -v）→ `big`（看起來沒修）→ `terminal`（dpkg-query）→ `terminal`（changelog）→ `big`（其實修補早就進去了）→ `big`（為什麼版本號不變）→ `steps`（三種查法）→ `bullets`（三個誤會）→ `big`（10/23 又一則）。收尾：回到放著的那題。
7. 我的看法：現在先做什麼（70 秒）`big`（找洞變快、修洞還是人的速度）→ `big`（我查不到的）→ `steps`（今天、這週、之後）→ `big`（答案：修補是一條鏈）→ `big`（留言題）→ `outro`。

### 選項 B：四天的時間線——從 10 月 17 日蜜罐那一次試探講到 21 日下午兩點

角度：事件型，主角是這次修補的時間線，照 UTC 時間一格一格走（17 日蜜罐、20 日 15:20 走漏、19:30 預告、20:00 影片、21 日 03:02 WAF、07:41 映像檔、14:00 發布），每一格帶一條規則。
跟 A 差在時間線是主線、版本檢查只在最後一章；跟 C 差在不談 2024 稽核。
開場：「10 月 17 日，Amazon 的一台蜜罐記錄到一個請求；四天後，全世界才知道它在試什麼。」
章節：1. 17 日那一次（50 秒）2. 20 日下午三點（80 秒）3. 20 日晚上的預告與影片（80 秒）4. 21 日凌晨到早上（90 秒）5. 下午兩點之後（80 秒）6. 你的網站（90 秒）7. 結尾（40 秒）。
風險：觀眾最想知道的「關我什麼事」要等到第 6 章；時間點多，念出來像清單。

### 選項 C：AI 找到的第一個「網路級」漏洞——從 2024 年那次沒修成的稽核講起

角度：以 PHP Foundation 自己承認的「結構性失敗」開場，主線是「人修不動的洞，AI 怎麼讓它非修不可」，收在這對開源維護者意味著什麼（BBC 的 Ondřej Surý 一週收到一年份的捐款）。
跟 A 差在以 AI 與維護者為主角、觀眾的檢查只佔一章；跟 B 差在不走時間線。
開場：「2024 年，PHP 做了第一次外部安全稽核，一位開發者看到了一個記憶體問題的徵兆；兩年後，是 AI 逼它非修不可。」
章節：1. 2024 年那個徵兆（60 秒）2. 為什麼修不動（70 秒）3. 8 月 11 日（90 秒）4. 兩天的走漏（80 秒）5. 一個志工的那一週（70 秒）6. 你的網站（80 秒）7. 結尾（40 秒）。
風險：站主立場是「給觀眾一個能做的動作」，C 的重心在人物與開源生態，示範弱。

## 會過期的事實

- 四個安全版本與緩解措施：https://www.php.net/archive/2026.php#2026-10-21-5 （撰稿當天再開：下一次例行版本會把 CVE-2026-115560 一起修，版本號會再往上）
- 10-23 資訊性建議：https://www.php.net/archive/2026.php#2026-10-23-1
- 支援中的分支與到期日（8.2 的安全支援到 2026-12-31）：https://www.php.net/supported-versions.php
- Ubuntu 各版修好的套件版本：https://ubuntu.com/security/CVE-2026-109618 ；Debian：https://security-tracker.debian.org/tracker/CVE-2026-109618
- PHP 占比（每天更新）：https://w3techs.com/technologies/details/pl-php （2026-10-25：69.2%）
- CISA KEV 有沒有收錄（watchTowr 10-22 說還沒）：https://www.cisa.gov/known-exploited-vulnerabilities-catalog （本機 403，撰稿時用 watchTowr 的 FAQ）
- 台灣的數字（2.8 萬、200）與資安署的順序：https://moda.gov.tw/ACS/press/news/press/21134 、https://www.ithome.com.tw/news/179891
- 攻擊嘗試的量（Cloudflare 執行長 X 貼文，BBC 引述）：https://www.bbc.com/news/articles/c3qjnwye0ep5o
- 蜜罐 10-17：https://aws.amazon.com/blogs/security/amazon-threat-intelligence-identifies-php2shell-exploitation-prior-to-public-disclosure-in-madpot/

## 素材

- `screencast`：https://www.php.net/archive/2026.php （公開頁；截 `a#2026-10-21-5` 所在的那一則公告標題與第一段；也是縮圖主體 `thumbnail.data.capture`）
- 三張 `terminal` 卡的指令與輸出逐字取自 2026-10-25 本機執行紀錄（上面「示範或實算」）；工具版本寫 PHP 8.3.6 (cli)／dpkg 1.22.6、Ubuntu 24.04.5 LTS
- 原始頁面的 HTML 存在工作區 `_tools/sources/`（php-news、phpfoundation-post、wiz、cloudflare、aws、watchtowr、ubuntu-cve、debian-tracker、ncsc-uk、csa-sg、moda-press2、ithome4、bbc-takendown、bbc-whatisphp、bbc-hero、japancyberwatch、techtarget、wikipedia，2026-10-25 存）
- 不用任何攻擊示範、不放 PoC、不畫 AI 插圖；不用任何人的帳戶畫面

## 不做的事

- 不講兩個 CVE 的技術細節（OOM、stale global state 的機制）超過一句；不教怎麼利用
- 不講 PHP 7.4／8.0／8.1 的原始碼回植怎麼編譯；不比較各家主機商
- 不下「AI 讓世界更危險」或「更安全」的結論；站主觀點只講鏈與三件能做的事
- 不講 Chainguard 與 PHP Foundation 的爭論誰對誰錯，只講時間與各自的說法
- 不講美國政府網站有沒有下線（來源互相矛盾）、不講日本 SoftBank 停掉災害警報（BBC 只引日媒）
