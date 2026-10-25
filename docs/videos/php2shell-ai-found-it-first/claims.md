# 查核清單：php2shell-ai-found-it-first

撰稿 2026-10-25。每一行一個可查的主張：編號｜主張（旁白或畫面怎麼說）｜出處｜查證日｜用到它的場景 id。
本片有一組**本頻道自己跑的紀錄**（RUN）：2026-10-25 06:52 UTC，在一台 Ubuntu 24.04.5 LTS 的測試機（PHP 8.3.6 (cli)、dpkg 1.22.6）上執行
`php -v`、`dpkg-query -W -f='${Package} ${Version}\n' php8.3-cli`、`zcat /usr/share/doc/php8.3-cli/changelog.Debian.gz | head -n 4`，三張 `terminal` 卡的指令與輸出逐字取自這次執行；
其他全部是 CITED（官方頁或具名的媒體報導，卡片 `source` 標出處）。沒有任何攻擊示範。
「我的看法是」「我查不到」「我拿我這台測試機試」是站主觀點的提案與本機執行紀錄，不是事實主張。汽車召回是說明用的生活對照，旁白在 tw-order 說明哪裡不能照對照理解。
原始頁面存在工作區 `_tools/sources/`（2026-10-25 用 `Mokaair-editorial/1.0` 抓；本機副本在 scratchpad/src）。

縮寫：P＝php.net 2026 新聞存檔 https://www.php.net/archive/2026.php （10-20 預告、10-21 安全公告 `#2026-10-21-5`、10-23 資訊性建議 `#2026-10-23-1`）；
PS＝ https://www.php.net/supported-versions.php ；F＝PHP Foundation 2026-10-21 https://thephp.foundation/blog/2026/10/21/todays-php-security-release-and-how-were-strengthening-php-security/ ；
W＝Wiz 2026-10-21 https://www.wiz.io/blog/php2shell-php-rce ；CF＝Cloudflare 2026-10-21 https://blog.cloudflare.com/php-vulnerabilities-waf-protection/ ；
AWS＝ https://aws.amazon.com/blogs/security/amazon-threat-intelligence-identifies-php2shell-exploitation-prior-to-public-disclosure-in-madpot/ ；
WT＝watchTowr FAQ https://watchtowr.com/intelligence/php-cve-2026-109618-faq/ ；U＝ https://ubuntu.com/security/CVE-2026-109618 ；D＝ https://security-tracker.debian.org/tracker/CVE-2026-109618 ；
W3＝ https://w3techs.com/technologies/details/pl-php ；N＝NCSC https://www.ncsc.gov.uk/news/critical-security-issue-affecting-php ；
M＝資安署新聞稿 2026-10-22 https://moda.gov.tw/ACS/press/news/press/21134 ；I＝iThome 2026-10-22 https://www.ithome.com.tw/news/179891 ；
B1＝BBC 2026-10-21 https://www.bbc.com/news/articles/cmly0lg3w5x2o ；B2＝BBC 2026-10-23 https://www.bbc.com/news/articles/c3qjnwye0ep5o ；
J＝Japan Cyber Watch https://japancyberwatch.com/articles/php2shell-critical-php-flaws-japan-services-pause-2026 ；HN＝ https://news.ycombinator.com/item?id=50167754 （時間戳由 hn.algolia.com API：2026-10-20T15:20:35Z）；
TT＝TechTarget 2026-10-22 https://www.techtarget.com/cybersecurity/news/366652613/PHP2Shell-disclosure-unravels-after-leaks-forced-early-patch-drop ；X＝Greg Brockman https://x.com/gdb/status/2112921529650688312 。

c1｜PHP 2026-10-21 發布 8.5.12、8.4.27、8.3.36、8.2.35，修兩個可未登入遠端執行程式的重大漏洞 CVE-2026-109618、CVE-2026-109619，合稱 PHP2Shell｜P、WT、W｜2026-10-25｜open, versions, timeline, advisory-page
c2｜日本首相高市早苗 10/21 晚在 X 發「緊急請求」，請站長確認網站有沒有用 PHP、當晚行動；J 記 21:55 左右（日本時間）｜B1、B2、J、I（數發部記者會也提到）｜2026-10-25｜open, pm
c3｜洞在 PHP 本身：未登入的請求可執行程式；可讀出 worker 記憶體裡的密碼、token、API key、憑證；可改網站（Brockman：exfiltrate private user data or modifying the site）｜P（who is at risk）、W（Executive Summary、Impact）、X｜2026-10-25｜verbs, engine
c4｜「修補公開前四天就有人在試」：AWS MadPot 記錄到 2026-10-17 的攻擊嘗試，公開是 10-21｜AWS｜2026-10-25｜stakes, honeypot
c5｜PHP 用於 69.2% 已知伺服器語言的網站（W3Techs 2026-10-25）；WordPress、Drupal、Joomla 建在 PHP 上｜W3、W｜2026-10-25｜seventy
c6｜洞在引擎、「即使 Hello World 也會中」：W「even a simple “Hello World” application running on an affected PHP version can be vulnerable」｜W｜2026-10-25｜engine
c7｜風險最高是 Apache mod_php：未登入請求在任何應用程式碼執行前就能觸發（P：「We consider the risk highest for mod_php, with a demonstrated exploit where an unauthenticated request can trigger the attack before any application code runs」）｜P｜2026-10-25｜modphp
c8｜台灣：資安署初步盤點約 2.8 萬個對外網站用 PHP、其中政府機關約 200 個；到 10/22 記者會為止沒有收到被駭通報（署長蔡福隆，行政院會後記者會）｜I；M 為新聞稿（不含數字）｜2026-10-25｜taiwan
c9｜受影響版本回到 2012 年的 PHP 5.4（W：「going back to version 5.4」；WT：PHP 5 也受影響）；5.4 發布年份依 php.net releases｜W、WT｜2026-10-25｜howlong
c10｜2024 年 PHP 第一次外部安全稽核（Sovereign Tech Agency 出資、OSTIF 組織、Quarkslab 執行），一位核心開發者看到 OOM 問題的徵兆；當時只理論化、沒有具體路徑；幾種修法各有代價、共識制卡住、停了又重啟數月｜F｜2026-10-25｜audit
c11｜引文逐字：「We won't pretend otherwise: the delay was a structural failure」｜F｜2026-10-25｜structural
c12｜Calif 7/30 在 Patch the Planet 下開始稽核；8/11 Calif 的 Ryan A（BBC、Wikipedia：Ryan Austin）回報無條件 RCE、根因同 2024；OpenAI 獨立回報同根因；OpenAI 9/18、Wiz 8/24 再補攻擊路徑；從 8/11 起是第一優先；原定 10/22 14:00 UTC 公開｜F、B2（Ryan Austin）、W（timeline）｜2026-10-25｜found
c13｜Ryan Austin 用 GPT-5.6 Sol（BBC B2「used advanced AI tools, developed by OpenAI」；Wikipedia 引 WSJ：GPT-5.6 Sol）；Wiz 用 Wiz Atlas、Gemini 4 Argon、GPT-5.6 Sol；8/19 發現、8/20 Drupal RCE、8/21 WordPress RCE、8/24 回報；在 WordPress、Drupal、Joomla 最新映像上做到未登入 RCE｜W、B2｜2026-10-25｜found
c14｜「Google 旗下的 Wiz」：BBC B1「Google's Wiz cybersecurity team」（Reuters 引）；Wikipedia：Alphabet 子公司、Google Cloud｜B1｜2026-10-25｜found
c15｜Wiz：「a single researcher completed in a week what previously would have taken a world-class team months of work」｜W｜2026-10-25｜oneweek
c16｜引文逐字：「We believe PHP2Shell could mark a similar turning point for the AI era」；Heartbleed 2014 是 OpenSSL（加密函式庫）｜W｜2026-10-25｜heartbleed
c17｜走漏：2026-10-20 15:20:35 UTC Hacker News「Tell HN: 2x PHP RCE CVEs with CVSS 10.0 Incoming」；F：約 15:00 UTC 起 CVE 編號在論壇流傳，附錯的發布時間與錯的 CVSS 10.0（實際 9.2）｜HN、F、P｜2026-10-25｜leak, timeline
c18｜PHP 19:30 UTC 提前發預告，發布從 10/22 14:00 改到 10/21 14:00｜F、P（10-20 預告）｜2026-10-25｜timeline
c19｜約 20:00 UTC Calif 誤發 PoC 影片，刪除後仍流傳｜F｜2026-10-25｜timeline
c20｜10/21 03:02 UTC 起 Cloudflare 的 WAF 對免費與付費方案預設保護；提前公開約 9 小時｜CF｜2026-10-25｜timeline
c21｜10/21 07:41 UTC Chainguard 提前發布含修補的映像檔，比協調發布早六小時以上；「attacker could now study the fix in binary form」｜F｜2026-10-25｜timeline
c22｜10/21 14:00 UTC 發布四個版本（WT：around the scheduled 14:00 UTC；J：22:38 日本時間略早）｜WT、J｜2026-10-25｜timeline
c23｜Cloudflare 執行長 Matthew Prince：公告前 10 小時數千次、45 分鐘後數萬次、兩小時內數十萬次、現在數百萬次｜B2、TT（引 X 貼文）｜2026-10-25｜attempts
c24｜NCSC 原句：「Where immediate remediation is not feasible, organisations should consider taking the system offline until it can be fully mitigated」（B1 引；N 頁本身為公告）；日本國家網路統括室：若來不及修補，暫停網站是降低風險的有效做法之一｜N、B1、J｜2026-10-25｜ncsc
c25｜10/21 自己停站：pixiv、DMM.com、niconico、BASE、Codmon、Shadowverse、Sakura Internet（J）；荷蘭 DigiD、MijnOverheid、國會、國家資安中心自己的網站（TT 引 NOS、B1）；芬蘭政府對外服務全部暫停（B1、Wikipedia 引 Reuters）；英國 32 個政府網站（B2）；維基媒體多個系統（B1）；Internet Archive 短暫停機（Wikipedia 引）｜J、B1、B2、TT｜2026-10-25｜offline
c26｜台灣資安署的順序：優先修補；無法立即升級先部署 WAF 等緩解；兩者都做不到才暫停對外服務（署長記者會）；新聞稿同樣呼籲儘速修補、無法修補時採取緩解措施｜I、M｜2026-10-25｜tw-order
c27｜RUN：`php -v` → `PHP 8.3.6 (cli) (built: Oct 19 2026 15:16:58) (NTS)` 等四行；`dpkg-query` → `php8.3-cli 8.3.6-0ubuntu0.24.04.13`；changelog 前四行如卡片｜本機 2026-10-25｜2026-10-25｜phpv, dpkg, changelog
c28｜Ubuntu 24.04 noble 的 php8.3 修好版本是 8.3.6-0ubuntu0.24.04.13（U，USN-8948-1）；Debian bookworm 8.2.35-1~deb12u1、trixie 8.4.27-1~deb13u1（D）｜U、D｜2026-10-25｜patched, three-ways
c29｜P 原句：「Linux distributions and LTS vendors received the patches in advance, so check your vendor for updated packages」；8.1 以下官方不再出版本、有 7.4／8.0／8.1 的最小原始碼回植｜P｜2026-10-25｜why-same, versions, three-ways
c30｜P：「only an update is a complete solution」；session.upload_progress.enabled=0 只擋已確認的 session 路徑、不擋其他變體；更新後要 restart 每個 worker（「restart every worker」）；更新應用程式（WordPress 等）不等於更新 PHP 執行環境（THN 整理 P 的說法：runtime comes from the server package, the host, or the container image）｜P｜2026-10-25｜myths
c31｜10/23 資訊性建議：CVE-2026-115560，只在少見的設定組合（serialize_handler 在執行期切換且 upload progress 開著）下成立；建議設 session.upload_progress.enabled=0 直到下一次例行版本；全文公告隨下一版發布｜P（`#2026-10-23-1`）｜2026-10-25｜oct23
c32｜8.2 的安全支援到 2026-12-31；8.3 到 2027-12-31｜PS｜2026-10-25｜three-things
c33｜Brockman（OpenAI）：「one of the most severe bugs in open source software found in recent memory… found as part of our Patch the Planet initiative」（只在說明欄與企劃，旁白沒唸）｜X｜2026-10-25｜—

## 與企劃不同的地方

- 大綱 A 第 3 章多了 `heartbleed` 一張 `quote`（Wiz 的原句），第 6 章的「看起來沒修」拆成一張 `big` 加一句「問題來了」，為了每 90 秒內有一個掛著的問題（lint 原本警告 06:41–09:04 沒有鉤子）。
- 開場承諾句從「看完你會知道」改成「九分鐘後你手上會有四樣東西」，避開 lint 的目錄句型；內容不變。
- 日期在旁白多用中文數字（十月二十日、二十一日），因為 lint 把「10」「21」「22」當成重複的數字；卡片仍用數字。
- `outro` 只留訂閱句，答案句與留言題各一張 `big`（跟 `google-ai-search-ads-exception` 一樣）；lint 因此留一條 outro 只有一句的警告。

## 我懷疑但沒動的事

- 「Google 旗下的資安公司 Wiz」：BBC 寫 Google's Wiz；Wiz 自己的文章沒提 Google 母公司。查核若覺得不穩，可改成「資安公司 Wiz」。
- 「Ryan Austin 用 GPT-5.6 Sol」：PHP Foundation 只寫「Ryan A」，模型名出自 Wikipedia 引 WSJ 與 OpenAI 相關報導；BBC 寫「advanced AI tools, developed by OpenAI」。查核若找不到 OpenAI 或 Calif 的原文，可改成「用 OpenAI 的模型」。
- 「連只印一行 Hello World 的網站都有」：Wiz 原句是 can be vulnerable（可能），旁白說「都有」偏絕對；查核可改「也可能中」。
- 「十七日就記錄到一次攻擊嘗試」：AWS 寫 exploitation attempt dating to Oct. 17；未說是否成功，旁白沒說成功。
- 資安署新聞稿本身沒有 2.8 萬與 200 的數字（來自署長記者會、iThome 報導），卡片 `source` 標 iThome。

## 進度

- 41 景、92 句全部寫完；lint 0 錯誤、1 條有意保留的警告（outro 一句）。
