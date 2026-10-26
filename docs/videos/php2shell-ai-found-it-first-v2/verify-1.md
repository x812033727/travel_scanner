# 查核 1：php2shell-ai-found-it-first

查核日 2026-10-25（第 1 輪，查核者不是撰稿者）。對象：`video.json`（41 景、92 句）、`claims.md`、`brief.md`（只讀）。
官方頁的存檔副本在 scratchpad `src/`（2026-10-25 以 `Mokaair-editorial/1.0` 抓；下表「存檔」指這批），查核自己另外抓的頁在 scratchpad `verify/`（下表寫 HTTP 狀態）。
三張 `terminal` 卡在本機重跑 `php -v`、`dpkg-query`、`zcat … | head -n 4`，與卡片 `command`、`output` 逐 byte 比對；`lsb_release -ds`＝Ubuntu 24.04.5 LTS、`dpkg --version`＝1.22.6。
網搜用了 5 次（Google 收購 Wiz、Prince 貼文、高市貼文、Internet Archive、eastdakota）。

**靠媒體報導而非官方頁的主張**在 verdict 欄標「（媒體）」並寫出哪一家；卡片 `source` 是否標對也寫在那一欄。

## 來源縮寫

P＝php.net 2026 存檔 https://www.php.net/archive/2026.php ；PS＝ https://www.php.net/supported-versions.php ；PR＝ https://www.php.net/releases/index.php ；
F＝PHP Foundation 2026-10-21 https://thephp.foundation/blog/2026/10/21/todays-php-security-release-and-how-were-strengthening-php-security/ ；
W＝Wiz https://www.wiz.io/blog/php2shell-php-rce ；CF＝ https://blog.cloudflare.com/php-vulnerabilities-waf-protection/ ；
AWS＝ https://aws.amazon.com/blogs/security/amazon-threat-intelligence-identifies-php2shell-exploitation-prior-to-public-disclosure-in-madpot/ ；
WT＝ https://watchtowr.com/intelligence/php-cve-2026-109618-faq/ ；U＝ https://ubuntu.com/security/CVE-2026-109618 ；D＝ https://security-tracker.debian.org/tracker/CVE-2026-109618 ；
W3＝ https://w3techs.com/technologies/details/pl-php ；N＝ https://www.ncsc.gov.uk/news/critical-security-issue-affecting-php ；
M＝ https://moda.gov.tw/ACS/press/news/press/21134 ；I＝ https://www.ithome.com.tw/news/179891 ；
B1＝ https://www.bbc.com/news/articles/cmly0lg3w5x2o （2026-10-21）；B2＝ https://www.bbc.com/news/articles/c3qjnwye0ep5o （首發 2026-10-22 03:48Z，更新 10-23）；
J＝ https://japancyberwatch.com/articles/php2shell-critical-php-flaws-japan-services-pause-2026 ；TT＝ https://www.techtarget.com/cybersecurity/news/366652613/PHP2Shell-disclosure-unravels-after-leaks-forced-early-patch-drop ；
HN＝ https://hn.algolia.com/api/v1/items/50167754 ；X＝ https://x.com/gdb/status/2112921529650688312 ；
TX＝ https://x.com/takaichi_sanae/status/2112890642590564386 ；PX＝ https://x.com/eastdakota/status/2113079352682570051 ；
CNN＝ https://edition.cnn.com/2026/10/21/tech/php2shell-vulnerability-ai ；WIKI＝ https://en.wikipedia.org/wiki/PHP2Shell 。
X 貼文的時間由貼文 id 的 snowflake 時間戳換算（`(id>>22)+1288834974657` ms），與頁面顯示的 UTC 時間一致。

## 主張表

| # | 主張 | 位置 | URL | HTTP／存檔 | 判定 | 之前 → 之後 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 10/21 PHP 發緊急安全更新，兩個漏洞合稱 PHP2Shell | 9ey5、open.data.subtitle、yt.title | P `#2026-10-21-5`、WT | 存檔 | CONFIRMED | — |
| 2 | 「前一晚」日本首相在 X 請站長當晚檢查網站 | cdnj | TX | 200 | **CHANGED** | 貼文 2026-10-21 12:55:59 UTC＝21:55 日本時間＝20:55 台灣時間，發布 14:00 UTC；是同一晚、早 64 分鐘。「前一晚，日本首相在 X 上請全國的網站管理者，當晚就去檢查自己的網站。」→「發布前一小時，日本首相在 X 上請全國網站管理者，當晚檢查自己的網站。」 |
| 3 | 洞在 PHP 本身：未登入、一個請求可執行程式、讀記憶體裡的密碼與 token、改掉網站 | h7nb、3ppu、verbs.data | P（who is at risk）、W（passwords, tokens, API keys；deface）、X（exfiltrate… modifying the site） | 存檔 | CONFIRMED | — |
| 4 | 修補公開前四天就有人在試 | vwd9、stakes.data.sub | AWS | 存檔 | CONFIRMED | AWS：Oct. 17, four days before public disclosure |
| 5 | AI 兩個月前找到、修補提早一天、四個版本號、一條看不出來的檢查 | 69ry、hsxu、promise.items | F、P | 存檔 | CONFIRMED | 8/11 → 10/21 約兩個月又十天 |
| 6 | 能查出伺服器語言的網站裡 69%／將近七成用 PHP；WordPress、Drupal、Joomla 在上面 | 9agr、seventy.data | W3、W | 存檔 | CONFIRMED | W3Techs 2026-10-25：69.2%（每日更新；卡片寫 69） |
| 7 | 洞在 PHP 執行環境，不在網站程式 | iecr、x493、engine.data | P、W | 存檔 | CONFIRMED | 卡 source 標 php.net 公告，對 |
| 8 | 「連只印一行 Hello World 的網站都有」 | c633 | W | 存檔 | **CHANGED** | W 原句 can be vulnerable。「都有」→「都可能中」 |
| 9 | 風險最高是 Apache mod_php，未登入請求在任何程式跑之前就能觸發 | qy4i、modphp.data | P | 存檔 | CONFIRMED | 原句逐字 |
| 10 | 台灣約 2.8 萬個對外網站用 PHP、政府機關約 200 個、到 10/22 記者會沒收到被駭通報 | 86sc、rsu6、taiwan.data | I（署長行政院會後記者會）、M | 存檔 | CONFIRMED（媒體：iThome 報導；M 新聞稿本身沒有數字） | 卡 source 標「iThome 報導資安署署長記者會」正確；說明欄原寫「照資安署新聞稿與 iThome 的報導」→「照 iThome 對資安署署長 10 月 22 日記者會的報導」 |
| 11 | 洞從 2012 年的 5.4 版就在，十幾年 | gffq | W（going back to version 5.4）、PR（5.4.0 Released: 01 March 2012）、X（14 years） | 存檔／200 | CONFIRMED | — |
| 12 | 2024 年 PHP「第一次」外部安全稽核，一位核心開發者看到記憶體問題的徵兆 | v5ur、audit.data.kicker | F | 存檔 | **CHANGED** | F：「first external security audit **in years**」。「第一次外部安全稽核」→「多年來第一次外部安全稽核」（卡片與旁白）；brief 寫的「第一次」與來源不同 |
| 13 | 沒人證明能被攻擊、幾種修法各有代價、小團隊要全體同意、停了又重啟拖好幾個月 | 92tm、audit.data.sub | F | 存檔 | CONFIRMED | theorized… no concrete vectors；consensus；stall and restart repeatedly over months |
| 14 | 引文「We won't pretend otherwise: the delay was a structural failure」 | structural.data.quote、daec | F | 存檔 | CONFIRMED | 逐字 |
| 15 | 7/30 Calif 在 OpenAI 的 Patch the Planet 下開始稽核 PHP | q9ga、found.steps[0] | F、X（our Patch the Planet initiative） | 存檔 | CONFIRMED | — |
| 16 | 8/11 Ryan Austin 用 GPT-5.6 Sol 交出無條件 RCE，根因同 2024 | 4649、jmju、found.steps[1] | F（Ryan A、8/11、unconditional RCE、same root cause）、X（Calif… used GPT-5.6 Sol… in August）、B2（Calif researcher Ryan Austin）、WIKI 引 WSJ | 存檔 | CONFIRMED（姓名靠媒體 BBC／WSJ；模型靠 OpenAI 總裁的貼文） | 卡 source 原只標 thephp.foundation、wiz.io，補 BBC、x.com/gdb |
| 17 | 兩週後 Google 旗下的 Wiz 用 Gemini 4 Argon、GPT-5.6 Sol 獨立找到同一個洞；WordPress、Drupal、Joomla 都打通 | i6qv、sqad、found.steps[2] | W（8/19 發現、8/24 回報、三個平台 latest 映像）、wiz.io 站上「Now part of Google Cloud」、ITdaily 2026-03-11 收購完成、WIKI 引 WSJ「Google's Wiz」 | 存檔／200 | CONFIRMED | B1 其實**沒有**寫 Google's Wiz（claims.md c14 原註錯），已改記出處；8/11→8/24 為 13 天 |
| 18 | 「從那天起」這件事變成「PHP 的第一優先」，修補定 10/22 | 2eju、found.steps[3] | F | 存檔 | **CHANGED** | F：from August 11th onward… top priority for all of the PHP Foundation's team working on security。旁白「從那天起，這件事變成 PHP 的第一優先」→「從八月十一日起，這是基金會資安團隊的第一優先」；卡片「從 8/11 起是 PHP 的第一優先」→「從 8/11 起是基金會資安團隊的第一優先」 |
| 19 | 一個研究員一週 vs 一整隊頂尖的人幾個月 | 26df、oneweek.data | W | 存檔 | CONFIRMED | 逐字 |
| 20 | 引文「We believe PHP2Shell could mark a similar turning point for the AI era」；2014 Heartbleed 是加密函式庫 | heartbleed.data、gbaz | W、WIKI（OpenSSL） | 存檔 | CONFIRMED | 逐字 |
| 21 | 保密兩個多月、最後兩天破了 | dy8w、v48u | F | 存檔 | CONFIRMED | 8/11 → 10/20；原定 10/22 |
| 22 | 10/20 15:20 UTC Hacker News 貼文「2x PHP RCE CVEs with CVSS 10.0 Incoming」；PHP 自評 9.2 | df33、7t2j、leak.data、timeline.rows[0]、sources[HN] | HN、P（10-20 預告：CVSS v4.0 9.2） | 200／存檔 | CONFIRMED | created_at 2026-10-20T15:20:35Z；標題逐字 |
| 23 | 四小時後 19:30 UTC 預告；從 10/22 14:00 改到 10/21 14:00 | d2mf、timeline.rows[1] | F、P | 存檔 | CONFIRMED | 15:20 → 19:30 |
| 24 | 約 20:00 UTC Calif 誤發攻擊示範影片，刪了但已流傳 | hafe、timeline.rows[2] | F | 存檔 | CONFIRMED | — |
| 25 | 10/21 03:02 UTC Cloudflare 對所有方案開規則，免費也有 | 4eea、timeline.rows[3] | CF | 存檔 | CONFIRMED | 「free or paid WAF… protected by default」「all plans… including Free」 |
| 26 | 07:41 UTC Chainguard 提前六個多小時放出含修補映像；攻擊者可反推 | pmy2、q6jq、timeline.rows[4] | F | 存檔 | CONFIRMED | more than six hours；study the fix in binary form |
| 27 | 14:00 UTC 四個版本準時發布 | ubbs、timeline.rows[5] | AWS（actual release… 1400 UTC）、M（台灣時間 22 時） | 存檔 | CONFIRMED | claims.md c22 補 AWS、M |
| 28 | Prince：公告前 10 小時數千、45 分鐘數萬、兩小時數十萬、「隔天」數百萬 | nxcc、2fht、attempts.data | PX、B2、TT | 200／存檔 | **CHANGED** | 貼文 2026-10-22 01:25:51 UTC，發布後 11 小時 26 分（台灣時間 10/22 早上 9:25）；引文逐字一致。「隔天」→「不到半天」（卡片 label、keys、2fht）；卡片標題「10/21」→「10/22 01:25 UTC」；source 補貼文時間 |
| 29 | Amazon 蜜罐 10/17 記錄到攻擊嘗試，比走漏早三天、比公開早四天 | us6i、honeypot.data | AWS | 存檔 | CONFIRMED | AWS 只寫 attempt，旁白沒說成功 |
| 30 | NCSC 引文「…organisations should consider taking the system offline until it can be fully mitigated」 | ncsc.data.quote、wppc | N、B1 | 存檔 | **CHANGED** | N 頁原句：「If you are unable to apply the temporary mitigations, or applying them would take too long, **you** should consider taking the system offline until it can be fully mitigated」；organisations 版本是 B1 引述。引文改成 N 頁原句；旁白 wppc 不變 |
| 31 | 日本國家網路統括室：暫停網站是降低風險的有效做法 | bqis | J、TX（首相貼文重申） | 存檔／200 | CONFIRMED（媒體 J；首相貼文佐證） | — |
| 32 | 10/21 日本 pixiv、niconico、電商 BASE、幼兒園用的 Codmon 進入維護 | kirn、offline.items[0] | J | 存檔 | CONFIRMED（媒體：J 引 Impress Watch、ITmedia） | 卡 source 標 J 正確 |
| 33 | 荷蘭數位身分系統、國會網站、國家資安中心自己的網站 | s8y2、offline.items[1] | B1（DigiD 在 J；Tweede Kamer、NCSC-NL 在 B1） | 存檔 | CONFIRMED（媒體 BBC、J） | 卡 source 標 BBC、J 正確 |
| 34 | 芬蘭政府全部對外服務；英國 32 個政府網站 | 3hp6、offline.items[2] | B1、B2 | 存檔 | CONFIRMED（媒體 BBC） | 英國政府 10/22 週四公布「32 sites had been taken down」，下線日期不明：卡片標題「10 月 21 日，自己關站的」→「10 月 21 日起，自己關站的」 |
| 35 | 維基媒體部分系統；Internet Archive 短暫停機 | wnky、offline.items[3]、offline.keys[3] | B1、B2、CNN（維基媒體）；Internet Archive 只在 WIKI，引 CNN ref 40 | 存檔／200 | 維基媒體 CONFIRMED；Internet Archive **NOT FOUND** | CNN 文（2026-10-25 抓）沒有 Internet Archive，blog.archive.org 沒有，網搜沒有。刪掉：旁白「維基媒體關了部分系統，Internet Archive 也短暫停機。」→「維基媒體也關了部分系統。」；卡片兩處同刪 |
| 36 | 首相 21:55 在 X 發「緊急請求」：今晚確認網站有沒有用 PHP | vrdu、56c5、pm.data | TX、B2、J | 200／存檔 | CONFIRMED（時間與原文直接取自貼文；原文「夜に対応して頂きたい大至急のお願いです」） | 時間是日本時間：kicker 與旁白補「（日本時間）」「日本時間」；卡 sub「BBC、Japan Cyber Watch」→「高市早苗的 X 貼文 2026-10-21；BBC 2026-10-23」；sources 多一筆 TX |
| 37 | 台灣順序：先修補；修不了先上 WAF；都不行才暫停；沒有要求關站 | khrf、g97x、tw-order.data | I、M | 存檔 | CONFIRMED（媒體 iThome 報導署長記者會；M 只呼籲修補與緩解） | — |
| 38 | 「公告當天攻擊就上百萬次」 | ksrk | PX | 200 | **CHANGED** | 同 #28：「公告當天」→「公告後不到半天」 |
| 39 | 公告標題最後是「update now」；連結在說明欄；指令在說明欄 | fx7j、57xv、cffr、advisory-page.data | P | 存檔 | CONFIRMED | 說明欄由 package 自動附 📚 來源連結，指令已在說明欄 |
| 40 | 四個安全版本 8.5.12／8.4.27／8.3.36／8.2.35；「8.1 以前」官方不再出版本 | zq2u、pacb、versions.data | P | 存檔 | **CHANGED** | P：PHP 8.1 **and older**。旁白「8.1 以前」→「8.1 以下」（卡片已是「8.1 以下」） |
| 41 | `php -v` 四行輸出；tool_version | phpv.data | 本機 RUN 2026-10-25 | — | CONFIRMED | 指令與輸出逐 byte 相同；Ubuntu 24.04.5 LTS |
| 42 | 8.3.6 與 8.3.36 差三十個版本 | 2qhy | P | 存檔 | CONFIRMED | — |
| 43 | `dpkg-query` 輸出 `php8.3-cli 8.3.6-0ubuntu0.24.04.13` | dpkg.data | 本機 RUN | — | CONFIRMED | 逐 byte 相同；dpkg 1.22.6 |
| 44 | changelog 前四行：noble-security、SECURITY UPDATE、CVE-2026-109618_109619.patch | changelog.data、94he、eea5 | 本機 RUN | — | CONFIRMED | 逐 byte 相同 |
| 45 | Ubuntu 24.04 修好的版本就是 8.3.6-0ubuntu0.24.04.13 | ur3m、patched.data.sub | U | 存檔 | CONFIRMED | php8.3 noble「Fixed in 8.3.6-0ubuntu0.24.04.13」；USN-8948-1 |
| 46 | php.net：Linux distributions and LTS vendors received the patches in advance | pmmz、why-same.data.sub | P | 存檔 | CONFIRMED | 逐字 |
| 47 | 三種查法（自己編譯或 Windows 看版本號；Linux 套件看更動紀錄；代管問主機商） | rvnm、48dz、w9gx、three-ways | P（Windows binaries；check your vendor） | 存檔 | CONFIRMED（建議，無數字） | — |
| 48 | 三個誤會：更新 WordPress≠更新 PHP；關 session 設定只擋部分路徑、不能取代更新；修好要重啟工作程序 | emqi、tgt8、pcpg、myths | P（only an update is a complete solution；blocks the confirmed session paths but not other variants；restart every worker） | 存檔 | CONFIRMED | 第一條是從 P「check your vendor for updated packages」推論，P 沒有逐字寫 WordPress |
| 49 | 10/23 建議：CVE-2026-115560 只在少見設定下成立；先關 session.upload_progress；等下一次例行版本 | anbx、f4cf、oct23.data | P `#2026-10-23-1` | 存檔 | CONFIRMED | — |
| 50 | 8.2 安全支援到 2026-12-31 | 7hcv、three-things.data.source | PS | 存檔 | CONFIRMED | 31 Dec 2026（頁面 2026-10-25 顯示 in 2 months）；8.3 到 31 Dec 2027 |
| 51 | 2.8 萬個站修好多少查不到；資安署說會持續掌握進度 | duf7、unsure.data | I、M | 存檔 | CONFIRMED（媒體＋新聞稿「持續掌握」） | — |
| 52 | 意見：找洞變快、修洞是人的鏈；鏈走完前停在路邊最安全 | gx6w、pmgi、v48u、w9rt | brief 站主觀點 | — | OUT OF SCOPE（意見，已標「我的看法是」，與 brief 一致） | — |
| 53 | 說明欄的日期、出處、指令、機器資訊 | yt.description | 各頁 | — | **CHANGED（出處）** | 台灣數字的出處改標 iThome 記者會報導；首相與 Prince 的數字改標 X 原貼文；其餘不動 |
| 54 | 標籤（PHP 8.3.36、CVE-2026-109618、Patch the Planet） | yt.tags | P、X | 存檔 | CONFIRMED | — |
| 55 | 縮圖「版本號 會騙你」 | thumbnail | — | — | OUT OF SCOPE | — |
| 56 | sources 的標題與日期 | sources[] | 各頁 `<title>` | 存檔 | **CHANGED** | 多一筆 TX；php.net、AWS、資安署、iThome、Japan Cyber Watch 五個標題縮短（內容不變）以符合說明欄 5000 bytes：原稿合成後已 5034 bytes（lint 錯誤，不是查核造成） |
| 57 | （claims.md c28）Debian bookworm 8.2.35-1~deb12u1、trixie 8.4.27-1~deb13u1 | claims.md | D | 存檔 | CONFIRMED | 旁白沒唸 |
| 58 | （claims.md c33）Brockman「one of the most severe bugs in open source software found in recent memory」 | claims.md | X | 存檔 | CONFIRMED | 逐字；旁白沒唸 |

## 摘要

- 查核主張：58 條（video.json 56 條＋claims.md 2 條）。CONFIRMED 45、CHANGED 11（事實 8：#2、#8、#12、#18、#28／#38、#30、#40、#35 刪除；出處與標註 3：#16 卡 source、#36 時區與來源、#53／#56）、NOT FOUND 1（#35 的 Internet Archive，已刪）、OUT OF SCOPE 2。
- 我改的每一處（旁白 id）：cdnj「前一晚，…當晚就去檢查自己的網站」→「發布前一小時，…當晚檢查自己的網站」；c633「都有」→「都可能中」；v5ur「做第一次外部安全稽核…看到了」→「多年來第一次外部安全稽核…看到」；2eju「從那天起，這件事變成 PHP 的第一優先」→「從八月十一日起，這是基金會資安團隊的第一優先」；2fht「隔天上百萬次」→「不到半天就上百萬次」；ksrk「公告當天攻擊就上百萬次」→「公告後不到半天攻擊就上百萬次」；wnky「維基媒體關了部分系統，Internet Archive 也短暫停機」→「維基媒體也關了部分系統」；vrdu 前加「日本時間」；pacb「8.1 以前」→「8.1 以下」。卡片：audit.kicker 加「多年來」；found.steps[3].detail、found.source；attempts.title／stats[3].label／keys[1]／source；ncsc.quote；offline.title／items[3]／keys[3]；pm.kicker／sub。說明欄出處兩句；sources 多一筆、五個標題縮短。claims.md c2、c6、c10、c12、c13、c14、c22、c23、c24、c25、c29 與新增「查核 1 改了什麼」一節。92 個 line id、41 景、reveal 與順序都沒動。
- 會過期的事實（看到的日期都是 2026-10-25）：W3Techs 69.2%（每日更新）；四個安全版本與 10/23 建議（P 說 CVE-2026-115560 的完整公告隨下一次例行版本發布，版本號會再往上）；8.2 安全支援 2026-12-31；Ubuntu 修好版本 8.3.6-0ubuntu0.24.04.13（之後若再修會換）；台灣 2.8 萬／200／0 是 10/22 的盤點；Prince 的「millions now」是 10/22 01:25 UTC 的數字；J 10/22 已有一家日本公司通報遭攻擊（Valtec，片中沒提）；B2 寫到 10/23 週五早上沒有成功攻擊的通報（片中沒提）。
- 意見不符：沒有。「我的看法是」「我查不到」「我拿我這台測試機試」都標成意見或本機紀錄，內容與 brief 站主觀點一致；但 brief 自己註明站主觀點是提案（頻道立場文字沒帶進來），站主要確認。
- 聽眾檢查（只報告）：超過 40 單位的句子：92tm（41，lint 警告，撰稿時已有）；查證敘述（「經查證」「根據官方文件」「本影片」）：沒有；不在 `docs/videos/lexicon.json` 的拉丁字：「X」（cdnj、vrdu，單字母）、「GPT-5.6」（4649、i6qv；lexicon 有 GPT、Sol，lint 沒報）；旁白沒有括號或網址；reveal 出現在景的第一句的有 promise 69ry、engine iecr、timeline d2mf、versions zq2u（句子本身就在介紹那幾項，順序沒問題）。
- lint：`node tools/video/cli.mjs lint --slug php2shell-ai-found-it-first` → 0 errors、2 warnings（92tm 41 單位；outro 一句，有意保留）。原稿 lint 其實有 1 個錯誤（說明欄合成後 5034 bytes，上限 5000），claims.md 的「0 錯誤」是舊紀錄。
- 懷疑但沒動：「Google 旗下的 Wiz」留著（wiz.io 站上「Now part of Google Cloud」、2026-03-11 收購完成的報導；B1 沒寫）；「Ryan Austin」姓名只靠 BBC／WSJ，F 只寫 Ryan A；「兩週後」是 8/11→8/24 回報的 13 天（Wiz 自己的發現日是 8/19）；「獨立找到同一個洞」：F 把 Wiz 8/24 寫成 further attack vectors，W 與 WSJ 寫獨立發現；4eea「對所有客戶開啟」：CF 寫「free or paid WAF」「all plans with WAF deployed」；CF 自己寫「about 9 hours ahead」但 03:02→14:00 是 11 小時（片中沒說差幾小時）；myths 第一條「更新 WordPress ≠ 更新 PHP」是推論，卡 source 標 php.net；khrf「台灣沒有要求關站」是對 iThome 報導的解讀；B2 在 sources 與卡片標 2026-10-23（首發 10-22 03:48Z、更新 10-23，頁面顯示 2 days ago）；日本「國家網路統括室」是 国家サイバー統括室 的譯名；offline 卡英國 32 個網站的下線日期來源沒寫。
- 與 brief 不同：brief 寫「2024 年 PHP 第一次外部安全稽核」與開場「前一晚日本首相…」，官方來源（F、TX）相反，照來源改了；站主決定大綱是否仍成立。
- **第二輪：需要**（事實改動 8 處，超過三處）。第二輪請重查上面 11 條 CHANGED 與隨機三分之一的 CONFIRMED。
