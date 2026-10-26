# 查核 2：php2shell-ai-found-it-first

查核日 2026-10-25（第 2 輪，查核者不是撰稿者，也不是第 1 輪的查核者）。對象：`video.json`（41 景、96 句：第 1 輪後多了 `structural` 第 2、3 句、`heartbleed` 第 2 句、`ncsc` 第 2 句，與三張 `quote` 卡的 `translation`）、`claims.md`、`verify-1.md`、`brief.md`（只讀）。
範圍：第 1 輪標 **CHANGED** 的每一列與第 35 列的 NOT FOUND，加上第 1 輪 CONFIRMED 的隨機三分之一（43 列用固定種子 20261025 抽 14 列：#5、#6、#11、#13、#14、#17、#20、#31、#32、#34、#37、#39、#48、#54；抽法在 scratchpad `verify2/pick_random.py`），三張 `terminal` 卡本機重跑，四句新旁白與三個 `translation` 對原句查忠實度。
官方頁用的是 scratchpad `src/` 的存檔（2026-10-25 以 `Mokaair-editorial/1.0` 抓）與第 1 輪另抓的 `verify/`（X 貼文、CNN、HN API、php.net releases、ITdaily、nippon.com、Internet Archive 部落格）；本輪沒有重抓。網搜用了 1 次（Internet Archive 有沒有因 PHP2Shell 停機）。
三張 `terminal` 卡本機重跑 `php -v`、`dpkg-query -W -f='${Package} ${Version}\n' php8.3-cli`、`zcat … | head -n 4`，用腳本與卡片 `output` 逐 byte 比對（`verify2/compare_terminal.py`）；`lsb_release -ds`＝Ubuntu 24.04.5 LTS、`dpkg --version`＝1.22.6，與 `tool_version` 一致。
X 貼文的時間取頁面 `article:published_time`，並以貼文 id 的 snowflake 時間戳覆核：高市 2026-10-21T12:55:59Z、Prince 2026-10-22T01:25:51Z、Brockman 2026-10-21T14:58:43Z。

## 來源縮寫

同 `verify-1.md`：P＝php.net 2026 存檔；PS＝supported-versions；PR＝php.net releases；F＝PHP Foundation 2026-10-21；W＝Wiz；CF＝Cloudflare；AWS＝AWS 安全部落格；U＝Ubuntu CVE 頁；W3＝W3Techs；N＝NCSC（英國）；I＝iThome 179891；M＝資安署新聞稿 21134；B1＝BBC 2026-10-21；B2＝BBC 2026-10-23；J＝Japan Cyber Watch；HN＝hn.algolia API；X＝Brockman 貼文；TX＝高市早苗貼文；PX＝Matthew Prince 貼文；CNN＝edition.cnn.com 2026-10-21；WIKI＝英文維基 PHP2Shell；NIP＝nippon.com（Jiji Press 2026-10-21）。

## 主張表

| # | 查核 1 的列 | 主張 | 位置 | URL | HTTP／存檔 | 判定 | 之前 → 之後 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | #2 | 發布前一小時，日本首相在 X 上請全國網站管理者，當晚檢查自己的網站 | cdnj | TX | 存檔（`article:published_time` 2026-10-21T12:55:59Z） | CONFIRMED | 貼文 12:55:59 UTC＝21:55 日本時間；發布 14:00 UTC＝23:00 日本時間；早 64 分鐘。原文「皆様に、今夜に対応して頂きたい大至急のお願いです。…公開しているウェブサイトでPHPを使用しているか確認し、今夜…準備をお願いします」。「全國」對應「皆様に」，首相對全國發言，可接受 |
| 2 | #8 | 連只印一行 Hello World 的網站都可能中 | c633 | W | 存檔 | CONFIRMED | W：even a simple “Hello World” application running on an affected PHP version **can be** vulnerable |
| 3 | #12 | 2024 年 PHP 多年來第一次外部安全稽核，一位核心開發者看到徵兆 | v5ur、audit.kicker | F | 存檔 | CONFIRMED | F：its first external security audit **in years**；a PHP core developer… found the first signs of the OOM problem |
| 4 | #16 | found 卡 source 補 BBC、x.com/gdb；Ryan Austin 用 GPT-5.6 Sol | found.source、4649 | F（Ryan A at Calif）、B2（Calif researcher Ryan Austin）、X（used GPT-5.6 Sol） | 存檔 | CONFIRMED | 姓名仍只靠媒體（B2；WIKI 引 WSJ 同），模型靠 OpenAI 總裁貼文；卡片 source 四個出處都對 |
| 5 | #18 | 從 8/11 起是基金會資安團隊的第一優先；修補定 10/22 公開 | 2eju、found.steps[3] | F | 存檔 | CONFIRMED | F：from August 11th onward, fixing it became the top priority for all of the PHP Foundation's team working on security；moved the release from October 22nd, 14:00 UTC |
| 6 | #28 | Prince：公告前 10 小時數千、45 分鐘數萬、兩小時數十萬、不到半天數百萬；卡片 10/22 01:25 UTC | attempts、nxcc、2fht | PX | 存檔（`article:published_time` 2026-10-22T01:25:51Z） | CONFIRMED | og:description 逐字「thousands… tens of thousands in the 45 minutes post announcement, hundreds of thousands within 2 hours, and millions now」；01:25 UTC 是發布後 11 小時 26 分，「不到半天」對 |
| 7 | #38 | 公告後不到半天攻擊就上百萬次 | ksrk | PX | 存檔 | CONFIRMED | 同第 6 列 |
| 8 | #30 | 引文「…you should consider taking the system offline until it can be fully mitigated」 | ncsc.quote | N | 存檔（Published 21 October 2026） | CONFIRMED | N 第 131 行逐字；它的前一句是「If you are unable to update…, the PHP Foundation have provided temporary mitigations」，再前一句是 Update to the latest version（修補 → 暫時緩解 → 下線；見第 34 列） |
| 9 | #34 | 芬蘭政府全部對外服務；英國 32 個政府網站；卡片標題「10 月 21 日起」 | 3hp6、offline.title | B1、B2 | 存檔 | CONFIRMED | B1：Finland has temporarily shut down the government's public web services；B2：The UK Government revealed on Thursday… 32 sites had been taken down as a precaution（下線日不明，「起」對） |
| 10 | #35 | Internet Archive 短暫停機（第 1 輪已刪）；維基媒體部分系統 | wnky、offline.items[3] | CNN、blog.archive.org、WIKI | 存檔／網搜 1 次 | NOT FOUND（維持刪除）；維基媒體 CONFIRMED | 只有 WIKI 一句「The Internet Archive briefly shut down to fix the issue [40]」；CNN（WIKI 說它引的）沒有、ia-blog 沒有、網搜沒有。維基媒體：B1、B2（took down a number of its systems）、CNN 都有 |
| 11 | #36 | 首相日本時間 21:55 在 X 發「緊急請求」：今晚就確認網站有沒有用 PHP | vrdu、56c5、pm.kicker／sub | TX、J（At about 21:55）、NIP（Jiji：Wednesday night） | 存檔 | CONFIRMED | 「大至急のお願い」＝緊急請求；「公開しているウェブサイトでPHPを使用しているか確認し」＝確認網站有沒有用 PHP；「今夜」；卡片 sub 的出處（高市貼文 2026-10-21；BBC 2026-10-23）對 |
| 12 | #40 | 8.1 以下官方不再出版本 | pacb、versions.source | P | 存檔 | CONFIRMED | P：PHP 8.1 and older no longer receive updates from the PHP project |
| 13 | #53 | 說明欄出處：台灣數字照 iThome 記者會報導；首相與 Prince 的數字照 X 原貼文 | yt.description | I、TX、PX | 存檔 | CONFIRMED | 與各頁一致；PX 不在 `sources`（說明欄合成後有 5000 bytes 上限，第 1 輪已說明），只記在 claims.md |
| 14 | #56 | sources 19 筆的標題與日期 | sources[] | 各頁 | 存檔 | CONFIRMED | TX「2026-10-21 21:55 JST」對；B2 標 2026-10-23（datePublished 2026-10-22T03:48Z、dateModified 10-23T12:24Z）；其餘標題與 `<title>` 一致 |
| 15 | #5 | AI 兩個月前找到、修補提早一天、四個版本號、一條看不出來的檢查 | 69ry、hsxu、promise | F、P | 存檔 | CONFIRMED | 8/11 → 10/21；10/22 → 10/21；8.5.12／8.4.27／8.3.36／8.2.35 |
| 16 | #6 | 69%／將近七成；WordPress、Drupal、Joomla 在上面 | 9agr、seventy | W3、W | 存檔 | CONFIRMED | W3Techs 2026-10-25：PHP is used by 69.2% of all the websites whose server-side programming language we know；W：powering WordPress, Joomla, Drupal |
| 17 | #11 | 從 2012 年的 5.4 版就在，十幾年 | gffq | W、PR、X | 存檔 | CONFIRMED | W：going back to version 5.4；PR：5.4.0 Released: 01 March 2012；X：14 years |
| 18 | #13 | 沒人證明能攻擊、修法各有代價、小團隊要全體同意、停了又重啟幾個月 | 92tm、audit.sub | F | 存檔 | CONFIRMED | theorized, but no concrete vectors；trade-offs；operating on consensus；the small team of core developers；stall and restart repeatedly over months |
| 19 | #14 | 引文「We won't pretend otherwise: the delay was a structural failure」 | structural.quote | F | 存檔 | CONFIRMED | 逐字 |
| 20 | #17 | 兩週後 Google 旗下的 Wiz 用 Gemini 4 Argon、GPT-5.6 Sol 獨立找到；WordPress、Drupal、Joomla 打通；8/24 回報更多路徑 | i6qv、sqad、found.steps[2] | W、F、wiz.io/about、ITdaily | 存檔 | CONFIRMED | W：8/19 發現、8/24 回報（8/11 → 8/24 為 13 天，與卡片日期一致）；Wiz Atlas, Gemini 4 Argon and GPT-5.6 Sol；wordpress:latest、drupal:latest、joomla:latest；F：further attack vectors… from Wiz on August 24th；wiz.io/about「Now part of Google Cloud」；ITdaily 2026-03-11「Google completes $32 billion acquisition of Wiz」 |
| 21 | #20 | 引文「We believe PHP2Shell could mark a similar turning point for the AI era」；2014 Heartbleed 是加密函式庫 | heartbleed.quote、gbaz | W、WIKI | 存檔 | CONFIRMED | 逐字；WIKI：Heartbleed, a 2014 vulnerability that affected OpenSSL, an encryption library |
| 22 | #31 | 日本國家網路統括室：暫停網站是降低風險的有效做法 | bqis | J、TX | 存檔 | CONFIRMED（媒體 J；首相貼文同句） | J：Japan's National Cyber Office said temporarily stopping websites is an effective way to reduce risk if patching quickly is difficult；TX 原文「ウェブサイト等を一時的に停止させることも、リスクを低減させるための有効策の一つ」並點名国家サイバー統括室 |
| 23 | #32 | 日本 pixiv、niconico、電商 BASE、幼兒園用的 Codmon 進入維護 | kirn、offline.items[0] | J | 存檔 | CONFIRMED（媒體 J 引 Impress Watch、ITmedia） | pixiv, DMM.com, niconico and the shop platform BASE to the childcare app Codmon went into emergency maintenance |
| 24 | #37 | 台灣：先修補；修不了先上 WAF；都不行才暫停；沒有要求關站 | khrf、g97x、tw-order | I | 存檔 | CONFIRMED（媒體 iThome 報導署長 10/22 記者會） | 「優先完成漏洞修補」→「先部署網站應用程式防火牆（WAF）等緩解措施」→「若既無法完成修補，也無法採取其他有效防護措施，則應暫時停止網站對外服務」；「沒有要求關站」是對「目前沒有對受影響的機關網站要求在時間點內完成處理」與這個順序的解讀 |
| 25 | #39 | 公告標題最後是 update now；指令在說明欄 | fx7j、57xv、cffr、advisory-page | P | 存檔 | CONFIRMED | 標題「Security advisory: Critical remote code execution vulnerabilities, update now」；三條指令在說明欄 |
| 26 | #48 | 三個誤會：更新 WordPress≠更新 PHP；關 session 設定只擋部分路徑；修好要重啟 | emqi、tgt8、pcpg、myths | P | 存檔 | CONFIRMED | only an update is a complete solution；This blocks the confirmed session paths but not other variants；restart every worker；第一條仍是從「check your vendor for updated packages」推論 |
| 27 | #54 | 標籤 PHP 8.3.36、CVE-2026-109618、Patch the Planet | yt.tags | P、X | 存檔 | CONFIRMED | — |
| 28 | #41 | `php -v` 四行；tool_version | phpv.data | 本機 RUN 2026-10-25 | — | CONFIRMED | 逐 byte 相同；Ubuntu 24.04.5 LTS |
| 29 | #43 | `dpkg-query` → php8.3-cli 8.3.6-0ubuntu0.24.04.13 | dpkg.data | 本機 RUN | — | CONFIRMED | 逐 byte 相同；dpkg 1.22.6 |
| 30 | #44 | changelog 前四行 | changelog.data | 本機 RUN | — | CONFIRMED | 逐 byte 相同 |
| 31 | 新 | translation「我們不假裝不是這樣：這個延遲是一次結構性的失敗。」；uyhr「這個延遲，是一次結構性的失敗。」 | structural.translation、uyhr | F | 存檔 | CONFIRMED | 忠於原句 |
| 32 | 新 | wavj「那是誰把它從抽屜裡拿出來的？」 | wavj | — | — | OUT OF SCOPE | 過場問句，不是引文的改寫 |
| 33 | 新 | translation「我們相信 PHP2Shell 可能是 AI 時代一個同樣的轉捩點。」；j6sz「他們說，這可能是 AI 時代一個同樣的轉捩點。」 | heartbleed.translation、j6sz | W | 存檔 | CONFIRMED | 忠於原句（could mark a similar turning point） |
| 34 | 新 | translation「無法立即修補的，應考慮先把系統下線，直到能完整緩解。」；vh8a「來不及修，就考慮先把系統下線。」 | ncsc.translation、vh8a、ncsc.keys[1] | N | 存檔 | **CHANGED** | N 原句的條件是「If you are unable to apply the temporary mitigations, or applying them would take too long」，前一句把暫時緩解措施留給不能更新的人：順序是修補 → 暫時緩解 → 下線，不是「無法立即修補就下線」。translation →「無法套用暫時緩解措施、或套用要花太久的，應考慮先把系統下線，直到能完整緩解。」；vh8a →「修補、緩解都來不及，就考慮先把系統下線。」；keys[1]「來不及修，就先下線」→「修補、緩解都來不及，就先下線」。引文本身、wppc、bqis 不動 |

## 摘要

- 重查主張：34 列（第 1 輪 CHANGED／NOT FOUND 14 列、隨機三分之一 13 列（#34 與前者重複）、三張 terminal 卡、四句新旁白與三個 translation）。CONFIRMED 31、CHANGED 1（第 34 列：NCSC 引文的中譯與改寫句）、NOT FOUND 1（第 10 列 Internet Archive，維持第 1 輪的刪除）、OUT OF SCOPE 1（wavj）。
- 我改的每一處：`ncsc.data.translation`「無法立即修補的，應考慮先把系統下線，直到能完整緩解。」→「無法套用暫時緩解措施、或套用要花太久的，應考慮先把系統下線，直到能完整緩解。」；旁白 vh8a「來不及修，就考慮先把系統下線。」→「修補、緩解都來不及，就考慮先把系統下線。」；`ncsc.data.keys[1]`「來不及修，就先下線」→「修補、緩解都來不及，就先下線」。claims.md c24 補註，並加「查核 2 改了什麼」一節。96 個 line id、41 景、reveal 與順序都沒動；沒有 `say` 欄位要改。
- 第 1 輪的結論沒有一條被推翻：#2 的 64 分鐘、#28 的 01:25 UTC、#30 的 N 頁原句、#12 的 in years、#18 的基金會資安團隊、#40 的 8.1 and older、#35 的刪除都再次成立。唯一要補的是第 1 輪把 NCSC 引文改成 N 頁原句之後，之後加進來的中譯與改寫句把「無法套用暫時緩解措施」寫成「無法立即修補」，本輪改正。
- 會過期的事實（看到的日期都是 2026-10-25，與第 1 輪相同）：W3Techs 69.2%；四個安全版本與 10/23 建議（下一次例行版本會把 CVE-2026-115560 一起修）；8.2 安全支援 2026-12-31；Ubuntu 修好版本 8.3.6-0ubuntu0.24.04.13；台灣 2.8 萬／200／0 是 10/22 的盤點；Prince 的「millions now」是 10/22 01:25 UTC 的數字；J 10/22 已有一家日本公司（Valtec）通報遭攻擊、B2 寫到 10/23 週五早上沒有成功攻擊的通報（片中都沒提）。
- 意見不符：沒有。「我的看法是」「我查不到」「我拿我這台測試機試」都標成意見或本機紀錄，與 brief 站主觀點一致；brief 自己註明站主觀點是提案，站主要確認。
- 聽眾檢查（只報告，與第 1 輪相同）：超過 40 單位的句子只有 92tm（41，lint 警告，撰稿時已有）；沒有查證敘述；不在 lexicon 的拉丁字只有「GPT-5.6」（4649、i6qv；lexicon 有 GPT 與 Sol，lint 沒報）與單字母「X」；旁白沒有括號或網址；reveal 在景的第一句的有 69ry、iecr、d2mf、zq2u，句子本身就在介紹那幾項。
- lint：`node tools/video/cli.mjs lint --slug php2shell-ai-found-it-first` → 0 errors、2 warnings（92tm 41 單位；outro 一句，有意保留）。估 10.8 分、96 句。
- 懷疑但沒動（同第 1 輪）：「Google 旗下的 Wiz」（wiz.io「Now part of Google Cloud」、ITdaily 2026-03-11；B1 只寫 cyber-security firm Wiz）；「Ryan Austin」只靠 BBC／WSJ，F 只寫 Ryan A；「兩週後…獨立找到」對應 8/24 回報（Wiz 自己的發現日是 8/19，8 天）；「獨立找到同一個洞」：F 寫 Wiz 8/24 是 further attack vectors，W 與 WSJ 寫獨立發現；cdnj「全國網站管理者」對應貼文的「皆様に」；myths 第一條是推論；khrf「台灣沒有要求關站」是對 iThome 報導的解讀；PX 不在 `sources`。
- 與 brief 不同：同第 1 輪（brief 的「第一次外部安全稽核」與「前一晚日本首相…」已照 F、TX 改）；本輪沒有新的。
- **第三輪：不需要**（本輪事實改動 1 處，未超過三處）。全部 34 列都有判定，沒有未解決的主張；第 10 列的 Internet Archive 以刪除收案。
