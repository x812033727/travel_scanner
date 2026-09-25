# verify-2 — chatgpt-ads-upgrade（查核第 2 輪，2026-09-25）

這一輪由另一位查核者負責，不是撰稿者，也不是第 1 輪的查核者。範圍有兩部分：第 1 輪改過的每一項（21 項 CHANGED，加上 2 項 NOT FOUND 後改寫），以及第 1 輪 CONFIRMED 的 39 項裡用種子亂數抽出的三分之一（13 項）。所有網址今天都用 `curl -sSL -A 'Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)'` 重新抓過（同一主機至少間隔 1 秒），定價頁另外在內建瀏覽器以未登入狀態打開，只讀畫面文字和頁面自己發出的公開請求。沒有登入任何帳號，也沒有用網頁搜尋。原始檔與輔助腳本放在 `videos/chatgpt-ads-upgrade/_tools/v2/`：`fetch.sh`、`totext.mjs`、`sample.mjs`、`listener.mjs`，`claims-list.txt` 是從目前的 video.json 逐項抽出的 201 筆，`video.before.json` 和 `claims.before.md` 是這一輪動手前的備份。

依照交代，這一輪沒有動 97p6、228y、英文介面名稱、方案階梯圖和文章連結；這些都留給統籌在聽眾審稿時決定。

## 抽樣方法

- 母體是第 1 輪 CONFIRMED 的 39 項：#2、3、4、5、7、8、10、12、13、14、16、18、19、20、21、22、23、25、27、28、29、30、32、33、34、41、42、44、48、49、50、51、52、53、54、59、60、64、67。
- `node sample.mjs 20260925` 的做法是：用 mulberry32 產生器，**種子 20260925**，對母體做 Fisher–Yates 洗牌，取前 ceil(39/3) = 13 項。
- 抽中的是 **#2、4、8、12、13、16、18、22、29、42、44、54、67**。

## 來源（今天重抓）

| 代號 | 網址 | HTTP | 今天看到的重點 |
| --- | --- | --- | --- |
| A | https://openai.com/index/chatgpt-ads-expands-southeast-asia-taiwan/ | 200 | 頁面日期是 September 23, 2026。原文："Starting today, ChatGPT Ads will begin rolling out across Indonesia, Malaysia, the Philippines, Singapore, Thailand, Vietnam, and Taiwan."；"Plus, Pro, and Enterprise subscriptions will remain ad-free." |
| RSS | https://openai.com/news/rss.xml | 200 | 這篇的 pubDate 是 Wed, 23 Sep 2026 02:00:00 GMT，也就是台灣時間 9/23 10:00 |
| SM | https://openai.com/sitemap.xml/product/ | 200 | 這篇的 lastmod 是 2026-09-24T02:01:30.125Z，也就是台灣時間 9/24 10:01 |
| T | https://openai.com/index/testing-ads-in-chatgpt/ | 200 | 原文 2/9 發布，之後有 3/26、5/7、8/11 三次更新。2/9 那段寫："logged-in adult users on the Free and Go subscription tiers" |
| E | https://openai.com/index/chatgpt-ads-expands-across-europe/ | 200 | 8/18 發布："Six months after …"、"expanded to eight additional markets" |
| X | https://openai.com/index/expanding-access-to-ai-with-chatgpt-ads/ | 200 | 8/31 發布，寫明會擴大到更多市場 |
| AP | https://openai.com/index/our-approach-to-advertising-and-expanding-access/ | 200 | 廣告原則頁 |
| G | https://openai.com/index/introducing-chatgpt-go/ | 200 | 原文："In the US, Go is available for $8 per month." |
| H | https://help.openai.com/en/articles/20001047-ads-in-chatgpt | 200 | 標示「Updated: 3 days ago」 |
| HZ | https://help.openai.com/zh-hant/articles/20001047-ads-in-chatgpt | 200 | 中文介面名稱是「設定 > 廣告控制功能」「無廣告」「降低訊息限額」 |
| HP | https://help.openai.com/en/articles/6950777-what-is-chatgpt-plus | 200 | 原文："Price: $20/month (billed monthly)."；"we do not support annual billing … for ChatGPT Plus" |
| HG | https://help.openai.com/en/articles/11989085-what-is-chatgpt-go | 200 | 原文："we may adjust pricing over time" |
| V | https://help.openai.com/en/articles/11173733-taiwan-vat-and-egui | 200 | 2025-05-01 起，沒有提供台灣統一編號的台灣客戶要付 5% VAT |
| M | https://help.openai.com/en/articles/10421635-multicurrency-billing | 200 | 支援幣別裡有「TWD (NT$) Taiwan」，並寫 "For specific subscription prices, visit the ChatGPT pricing page" |
| HL | https://help.openai.com/en/articles/8357869-how-to-change-your-language-setting-in-chatgpt | 200 | 網頁版是「profile icon > Settings」，手機版是 "profile icon at the bottom of the screen" |
| P | https://chatgpt.com/pricing/（原始 HTML）＋內建瀏覽器未登入畫面 | 200 | 畫面上是 `$0`、`$270 /每月`、`$690/每月`、`From $3,300/每月`，頁尾寫「中文 台灣」。Go 卡片有「此方案可能包含廣告。」，英文 HTML 是 "This plan may include ads."。常見問題寫「我們提供 Go、Plus 和 Business 的月繳方案，以及 Business 和 Enterprise 的年繳方案」 |
| CTW | https://chatgpt.com/backend-anon/checkout_pricing_config/configs/TW | 200 | 內建瀏覽器的網路紀錄證實，定價頁載入的就是這一份。內容：`"symbol":"NT$"`、`"symbol_code":"TWD"`、go.month 270.0 inclusive、plus.month 690.0 inclusive、`"tax_percent":5.0`、`"pricing_rollout_gate":"is_pricing_enabled_for_twd"`，另有 plus.year 575.0 |
| CUS | https://chatgpt.com/backend-anon/checkout_pricing_config/configs/US | 200 | go.month 8.0、plus.month 20.0，都標 exclusive（未稅） |
| BOT | https://rate.bot.com.tw/xrt/flcsv/0/day ＋ https://rate.bot.com.tw/xrt?Lang=zh-TW | 200 | 牌價最新掛牌時間是 2026/09/25 13:45，美元即期賣出 31.855，和 13:25 那次一樣 |
| SVG | repo 內的 `apps/web/public/guides/chatgpt-plans-plus-pro-2026/diagram-1.svg`（本機讀檔） | — | 用文字比對圖上的內容 |

## 逐項表

「R1 #」是第 1 輪 verify-1.md 的編號。

### A. 第 1 輪改過的每一項

| R1 # | 說法 | 位置 | 網址 | HTTP | 判定 | 修改前 → 修改後 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 官方 9 月 23 日公告；廣告「開始在台灣陸續上線」 | ads-launch-big.data.kicker、ntdx、irnq、youtube.description | A、RSS、SM | 200 | CONFIRMED | 不改。官方有兩個日期訊號：頁面日期 Sep 23、RSS pubDate 台灣 9/23 10:00，兩者一致。sitemap lastmod（台灣 9/24 10:01）和 Inside 報導的 datePublished（9/24 10:01 +08:00）是同一分鐘，台灣媒體寫的「24 日上午 10 點」很可能是頁面實際上線的時刻，但沒有任何官方文字寫 9/24。「begin rolling out」對應「陸續上線」 |
| 6 | 「一條線」改寫成「標明是贊助、和回答分開」 | 9mmy、j6fd、3yz4 | H、A、T | 200 | CONFIRMED | 不改。H："clearly labeled as sponsored and visually separated from ChatGPT's response"；A："always clearly labeled and separate from ChatGPT's answers"。三個官方頁都沒有描述分隔線 |
| 9 | 2 月的測試只有美國、登入的成年用戶看得到 | kkaf | T | 200 | CONFIRMED | 不改。T："logged-in adult users on the Free and Go subscription tiers"。這句寫的是限制條件，所以成立；原文其實還限定 Free 和 Go，句子沒講到，但不影響事實（見「懷疑但沒動」） |
| 11 | 9 月 23 日公告輪到台灣和東南亞 | ads-launch-bullets.items[2]、ny5e | A、RSS | 200 | CONFIRMED | 不改，理由同 #1 |
| 17 | 真正保證沒有廣告的，要到 Plus 以上 | wuun、youtube.description | H、HZ、A | 200 | CONFIRMED | 不改。H："Plus, Pro, Business, Enterprise, and Edu accounts will not have ads."。Plus 以上的每一級（Pro 三個價位、Business、Enterprise、Edu）都沒有廣告。這句講的是方案層級：Free 方案本身「可能」有廣告，Ads-Free 是 Free 裡的一個選項 |
| 24 | 「法律上叫保留空間」改成「等於替自己保留空間」 | ufzu | — | — | OUT OF SCOPE | 改寫後是評論，沒有可查的事實 |
| 26 | 官方判定未滿 18 歲的帳號不會看到廣告 | wj34、44tt、q1-bullets.items[1] | H、HZ | 200 | CONFIRMED | 不改。H："accounts identified as belonging to users under 18, based on account-level age information and age prediction where available"；HZ 寫「經系統判定」 |
| 31 | 切 Ads-Free 後「不會看到廣告」 | fxs4 | H、HZ | 200 | CONFIRMED | 不改。H 在 "What changes on Ads-Free" 下寫 "No ads"，還寫 "This removes ads"；HZ 寫「無廣告」「這麼做會移除廣告」 |
| 35 | Go 在台灣官網是 NT$270／月，一年 NT$3,240；台幣、含稅 | q3-table.rows[2]、ds5u、7pr3、bir5 | P、CTW、M | 200 | CONFIRMED | 不改。未登入的畫面顯示 `$270 /每月`，頁面載入 configs/TW，內容是 NT$、TWD、270.0、tax inclusive、5%；270 × 12 = 3,240。**頁面怎麼證明是台幣、含稅：畫面本身只有「$」符號，沒寫 NT$，也沒寫含稅**。台幣靠三件事撐：頁尾地區是「台灣」、美國 Go 只要 $8 所以 270 不可能是美元、M 把 TWD (NT$) 列為台灣幣別。「含稅」只有 CTW 的 `"tax":"inclusive"` 和 `"tax_percent":5.0` 能證明，觀眾自己打開頁面看不到這兩個字 |
| 36 | Plus 是 NT$690／月，一年 NT$8,280；「一年大約八千三百元」 | q3-table.rows[3]、v3vc | P、CTW、HP | 200 | CONFIRMED | 不改。畫面顯示 `$690/每月`；CTW 的 plus.month 是 690.0 inclusive。CTW 裡另有 plus.year 575.0，但 HP 寫 "we do not support annual billing"，定價頁常見問題也只說 Go、Plus 月繳，所以一年＝690 × 12 = 8,280，四捨五入是八千三百 |
| 37 | 表上的台幣月費是官網直接標給台灣的價格；一年是乘 12 算的；匯率換算只是估計 | y7sz、dbba、jjyh、q3-code.caption | P、CTW、M | 200 | CONFIRMED | 不改 |
| 38 | 第三條，Go，台灣官網標價每個月 270 元 | 9hmr | P、CTW | 200 | CONFIRMED | 不改 |
| 39 | 第四條，Plus，台灣官網標價每個月 690 元 | y3xm | P、CTW | 200 | CONFIRMED | 不改 |
| 40 | Plus 大約是 Go 的兩倍半 | 4vai | CTW、CUS | 200 | CONFIRMED | 不改。690 ÷ 270 = 2.56，8,280 ÷ 3,240 = 2.56，20 ÷ 8 = 2.5，「大約兩倍半」對字卡上每個數字都成立 |
| 43 | 台灣的個人訂閱，沒填統一編號要付 5% 營業稅 | 75ue | V、CTW | 200 | CONFIRMED | 不改。V：自 2025-05-01 起，對沒有提供統一編號的台灣客戶收 5% VAT。CTW 標 inclusive，表示 270／690 已經含這筆稅 |
| 45 | 算式：8 × 31.855 = 254.84／254.84 × 1.05 ≈ 268／官網台幣月費 270（已含稅）／270 × 12 = 3,240 | q3-code.data.code、highlight [4] | BOT、CTW | 200 | CONFIRMED | 不改。254.84 × 1.05 = 267.582；270 × 12 = 3,240。highlight 指向第 4 行，也就是年費那一行 |
| 55 | 能調的主要是廣告要不要跟你的興趣有關 | iq9t | H | 200 | CONFIRMED | 不改。Ad Controls 裡還有看歷史紀錄、刪除廣告資料、過往對話與記憶的開關；說「主要是」成立 |
| 57 | Ads-Free 效果甚至比付錢買 Go 還徹底，是真的沒有廣告 | kvw2 | H、P | 200 | CONFIRMED | 不改。Ads-Free 是 "No ads"，Go 卡片寫 "may include ads" |
| 58 | 代價是，額度和部分功能都會變少 | gkia | H | 200 | CONFIRMED | 不改。H："lower usage limits and reduced feature access" |
| 61 | 圖上把額度、模型、價格每一層都畫出來 | 72nt | SVG | — | CONFIRMED | 不改。五格都有價格、模型和額度（價格用美元標示） |
| 62 | 圖上只在免費版標了廣告，其實 Go 也可能有 | 67it | SVG、H | — | CONFIRMED | 不改。只有 Free 那格寫「部分國家有廣告」 |
| 65 | 四條路徑的完整算式留在說明欄 | du3c | youtube.description | — | CONFIRMED | 不改。說明欄列了 NT$0、NT$0、270 × 12、690 × 12 |
| 66 | 說明欄：9/23 公告、Plus 以上、官網台幣價（9/25 查看、已含 5% 營業稅）、四條路徑的算式 | youtube.description | A、H、P、CTW | 200 | CONFIRMED | 不改。「已含 5% 營業稅」只有 CTW 能證明，見 #35 |

### B. 抽樣重查（種子 20260925）

| R1 # | 說法 | 位置 | 網址 | HTTP | 判定 | 修改前 → 修改後 |
| --- | --- | --- | --- | --- | --- | --- |
| 2 | 同一篇公告；東南亞六個市場是印尼、馬來西亞、菲律賓、新加坡、泰國、越南 | ads-launch-big.data.sub、ck4m、mvyr | A | 200 | CONFIRMED | — |
| 4 | 不是台灣單獨測試，是一波擴張 | z5a2、5sq8 | A | 200 | CONFIRMED | 7 個市場在同一篇公告裡 |
| 8 | 2 月從美國開始測試 | ads-launch-bullets.items[0]、kbhy | T、H | 200 | CONFIRMED | H："We began testing ads in the US on February 9, 2026." |
| 12 | 從小範圍測試到全球擴大走了大半年；已經測試了大半年 | jm85、s44h | T、E、A | 200 | CONFIRMED | 2/9 到 9/23 約七個半月。E 寫 "Six months after"；A 寫現在超過 60 國 |
| 13 | 官方一路觀察數據才擴大 | avty | T、H | 200 | CONFIRMED | T 在 3/26 寫 "early results are encouraging … These positive signals support moving into the next phase"；H 寫 "deliberate, phased approach" |
| 16 | Free 和 Go 可能看到廣告 | 6h4r、hwwr、th7i、kat8、myth-compare、outro.data.lines[0] | H、A | 200 | CONFIRMED | — |
| 18 | Plus 以上保證沒有廣告，白紙黑字 | y75y、u23a、2wc7、5jce、q3-table 的 Plus 列 | H、HZ | 200 | CONFIRMED | — |
| 22 | Go 想關掉只有兩條路：切回 Free，或往上升級 | krra、5zhe | H、HZ | 200 | CONFIRMED | H："you'd need to switch back to Free to use it, or upgrade to a plan that's already ad-free (like Plus or Pro)" |
| 29 | Ads-Free 額度變低；官方沒公布降多少 | g3ca、8iyr、q2-compare.right[0] | H | 200 | CONFIRMED | H 只寫 "fewer messages" 和 "you may hit rate limits more often"，沒有給數字 |
| 42 | 8 × 31.855 = 254.84，大約 255 | q3-code 第 1 行、p2fu | BOT | 200 | CONFIRMED | 13:45 掛牌仍是 31.855 |
| 44 | 254.84 × 1.05 ≈ 268 | q3-code 第 2 行、8hyr | 算術 | — | CONFIRMED | 算出來是 267.582 |
| 54 | Go 進同一頁只能管理個人化，看不到關掉廣告的選項 | ugxh、6b6m、settings-steps.steps[3] | H、HZ | 200 | CONFIRMED（實質） | H："Ads-Free is a Free-plan option"，Ad Controls 開放給 Free 和 Go 用戶。不登入就沒辦法看到 Go 的實際畫面，這個限制和第 1 輪一樣 |
| 67 | 標題、縮圖、開場字卡：「ChatGPT 開始有廣告了」 | youtube.title、thumbnail、hook.data | A | 200 | CONFIRMED | — |

### C. 抽樣外、讀原文時順手核對的項目

| R1 # | 說法 | 位置 | 網址 | HTTP | 判定 | 備註 |
| --- | --- | --- | --- | --- | --- | --- |
| 10 | 8 月擴大到英國、日本、南韓等地 | ads-launch-bullets.items[1]、rnkh | T、E | 200 | CONFIRMED（附註） | T 在 5/7 寫「接下來幾週」要在這五國擴大試行，8/11 寫 "has now launched"。「8 月」是官方宣布已上線的月份，不是確切上線日；歐洲 31 國也是 8 月。沒有改，已補進 claims.md 的 c1a |
| 19、53 | Ads-Free 的「開關」、點下去之前會提醒額度變低 | mni7、4w53、tk9u、5pcq、rptf、h36w | H、HZ | 200 | CONFIRMED（措辭附註） | 官方流程是：設定 → Ads controls → "Change plan to go ad-free" → "Reduce message limits" → 確認，確認前會跳出說明取捨的提示。這是一個換方案的流程，不是一個開關按鈕；說成「開關」是口語，事實沒錯（見聽眾檢查） |
| 33、34 | 美國月費：Go 8 美元、Plus 20 美元 | q3-table.columns[1]、rows[2..3][1]、edsu | G、HP、CUS | 200 | CONFIRMED | CUS 是 8.0／20.0，都未稅 |

## 摘要

- **重查了 39 項**：第 1 輪改過的 23 項（21 項 CHANGED 加 2 項 NOT FOUND 改寫），抽樣 13 項，另外順手核對 3 項。結果是 CONFIRMED 38、OUT OF SCOPE 1（ufzu 改寫後是評論）、**CHANGED 0**、NOT FOUND 0。**video.json 這一輪沒有改動。** claims.md 只補了證據（c1、c1a、c12）和進度，沒有改任何事實。
- **台幣價**：未登入從台灣打開 chatgpt.com/pricing，看到 Go `$270 /每月`、Plus `$690/每月`；網路紀錄證實頁面載入的是 configs/TW，內容寫 NT$、TWD、tax inclusive、5%。**畫面本身只顯示「$」，沒有 NT$，也沒有「含稅」**，所以「已含 5% 營業稅」只能靠頁面自己載入的官方設定來證明。configs/TW 還有 `pricing_rollout_gate: is_pricing_enabled_for_twd`，表示台幣價是逐步開放的，可能會變。plus.year 575 不是給個人的年繳方案（HP 和定價頁常見問題都這麼寫），一年仍是 × 12。
- **日期**：官方頁和 RSS 都是 9/23。台灣媒體的「9/24 上午 10 點」和 sitemap 修改時間是同一分鐘，很可能才是實際上線的台灣時間，但沒有官方文字寫 9/24。片中「官方 9 月 23 日公告」成立。brief 的觀眾描述寫「看新聞知道 9 月 24 日上線」，觀眾可能會注意到差一天，這是統籌的事。
- **快要過期的事實**（官方日期）：台灣台幣價 NT$270／NT$690（定價頁，2026-09-25 看到，而且有逐步開放的設定）；台灣銀行 31.855（2026/09/25 13:45 掛牌）；「這禮拜」（公告日 2026-09-23）；廣告說明頁（H，3 天前更新）；Plus 說明頁（HP，3 天前更新）；多幣別說明頁（M，昨天更新）。
- **和觀點不一致的地方**（只報告）：和第 1 輪相同。brief 寫「免費開關效果跟付錢買 Go 一樣」、「用一條線隔開」、「示範或實算」要自己加 5% 稅，這三個前提都已被官方來源推翻，要站主改 brief。有標「我的看法」的只有 a6vv。wjbn「官方自己都沒把握」和 p7qu「官方自己都沒有把話說死」是評論語氣，沒標成觀點。97p6、228y 留給統籌。
- **聽眾檢查**：`listener.mjs` 沒找到超過 40 字的句子、查證口吻、括號、網址，也沒有不在發音字典裡的拉丁字。另外兩點：(1) 片中五處把 Ads-Free 叫「開關」，但官方介面是「變更方案」按鈕加上「降低訊息限額」的確認流程，照「開關」去找的觀眾會找不到撥動式的開關。步驟字卡和 fgax 說「切到 Ads-Free 的選項」是準的。(2) 中文介面叫「廣告控制功能」「無廣告」；英文名稱依交代不動。
- **lint**：`chatgpt-ads-upgrade: 0 errors, 2 warnings`（開場約 41 秒、全片約 12.6 分鐘，都是已知的 250 字／分鐘估速問題）。
- **懷疑但沒改**：(1) kkaf 可以更準一點，寫成「美國、登入的成年 Free 和 Go 用戶」，但現在的句子也沒錯。(2) kbhy、jm85 的「小範圍」：官方只說是 test／pilot，沒說規模，不過只在一個國家開始，說小範圍站得住。(3) 開場 wuun「真正保證沒有廣告的要到 Plus 以上」和後面 kvw2「Ads-Free 是真的沒有廣告」，聽起來有點打架；方案層級上兩句都對，是否在開場加半句交給統籌。(4) 第 1 輪提到的 da3h「很可能已經看過了」、6b6m 的 Go 實際畫面、App 內購不經過這 5% 稅：這一輪也沒有辦法再往前查。(5) 方案階梯圖今天仍寫「台灣：網頁刷卡以美元計價」「台灣幣別以登入 chatgpt.com 後看到的為準」，Plus 那格寫「GPT-5.6 Sol」，但定價頁的 Plus 卡片現在寫「使用 GPT-6 Astra 與 GPT-5.6 的進階推理模型」。圖和文章連結是統籌的事。
- **還沒解決的**：第 1 輪的 #63、#68（方案階梯圖和說明欄連結），加上 97p6、228y，都在統籌手上。**文字事實已查核完成，但在這幾項定案之前，這份腳本還不能算「已查核」。**
- **需要第 3 輪嗎：不需要**（這一輪的事實修改是 0 處，沒有超過三處）。
