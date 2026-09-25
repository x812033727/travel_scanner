# verify-1 — chatgpt-ads-upgrade（查核第 1 輪，2026-09-25）

獨立查核，不是撰稿者。所有網址今天用 `curl -sSL -A 'Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)'` 抓取（同一主機間隔 ≥1 秒）；定價頁另外在內建瀏覽器以「未登入」打開，只讀畫面與頁面自己載入的公開價格設定，沒有登入任何帳號。網頁搜尋用了 2 次（只拿來找官方頁，不拿來證實數字）。原始檔與輔助腳本在 `videos/chatgpt-ads-upgrade/_tools/v1/`（`claims-list.txt` 是逐句抽出的 201 筆，`video.before.json`／`claims.before.md` 是改動前的備份）。

## 來源代號

| 代號 | 網址 | HTTP |
| --- | --- | --- |
| A | https://openai.com/index/chatgpt-ads-expands-southeast-asia-taiwan/（頁面日期 September 23, 2026） | 200 |
| RSS | https://openai.com/news/rss.xml（該篇 pubDate：Wed, 23 Sep 2026 02:00:00 GMT） | 200 |
| SM | https://openai.com/sitemap.xml/product/（該篇 lastmod：2026-09-24T02:01:30Z） | 200 |
| H | https://help.openai.com/en/articles/20001047-ads-in-chatgpt（Updated: 3 days ago） | 200 |
| HZ | https://help.openai.com/zh-hant/articles/20001047-ads-in-chatgpt | 200 |
| T | https://openai.com/index/testing-ads-in-chatgpt/（2/9 原文，3/26、5/7、8/11 更新） | 200 |
| E | https://openai.com/index/chatgpt-ads-expands-across-europe/（2026-08-18） | 200 |
| X | https://openai.com/index/expanding-access-to-ai-with-chatgpt-ads/（2026-08-31） | 200 |
| AP | https://openai.com/index/our-approach-to-advertising-and-expanding-access/（2026-01-16） | 200 |
| P | https://chatgpt.com/pricing/（openai.com/chatgpt/pricing/ 轉址）＋內建瀏覽器未登入畫面 | 200 |
| CTW | https://chatgpt.com/backend-anon/checkout_pricing_config/configs/TW（定價頁自己載入的公開價格設定） | 200 |
| CUS | https://chatgpt.com/backend-anon/checkout_pricing_config/configs/US | 200 |
| G | https://openai.com/index/introducing-chatgpt-go/（2026-01-16） | 200 |
| HG | https://help.openai.com/en/articles/11989085-what-is-chatgpt-go | 200 |
| HP | https://help.openai.com/en/articles/6950777-what-is-chatgpt-plus（Updated: 3 days ago） | 200 |
| V | https://help.openai.com/en/articles/11173733-taiwan-vat-and-egui | 200 |
| M | https://help.openai.com/en/articles/10421635-multicurrency-billing | 200 |
| BOT | https://rate.bot.com.tw/xrt/flcsv/0/day ＋ https://rate.bot.com.tw/xrt?Lang=zh-TW（牌價最新掛牌時間 2026/09/25 13:25） | 200 |
| HL | https://help.openai.com/en/articles/8357869-how-to-change-your-language-setting-in-chatgpt | 200 |
| SVG | repo `apps/web/public/guides/chatgpt-plans-plus-pro-2026/diagram-1.svg`（本機讀檔） | — |
| ART | repo `apps/api/app/guides/content/ai-free-vs-paid-plans-2026.json`（本機讀檔） | — |

## 逐項表

| # | claim | where | URL | HTTP | verdict | before → after |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 台灣時間 9/24 上午 10 點，廣告正式在台灣上線 | ads-launch-big.data.kicker、ntdx、irnq | A、RSS、SM | 200 | CHANGED | 官方頁只寫 September 23, 2026 與 "Starting today ... will begin rolling out"，沒有台灣當地時刻；RSS 時間＝台灣 9/23 10:00，sitemap 修改時間＝台灣 9/24 10:01，「9/24 10 點」只見於台灣媒體。kicker「台灣時間 9 月 24 日上午 10 點」→「官方 9 月 23 日公告」；ntdx「9 月 24 日上午 10 點，台灣時間。」→「9 月 23 日，官方正式公告。」；irnq「正式在台灣上線」→「開始在台灣陸續上線」 |
| 2 | 同一篇、東南亞六個市場：印尼、馬來西亞、菲律賓、新加坡、泰國、越南 | ads-launch-big.data.sub、ck4m、mvyr | A | 200 | CONFIRMED | — |
| 3 | 這禮拜台灣的 ChatGPT 開始出現廣告 | sf4i | A | 200 | CONFIRMED | 會過期（「這禮拜」） |
| 4 | 不是台灣單獨測試，是一波擴張 | z5a2、5sq8 | A | 200 | CONFIRMED | 7 個市場同一篇公告 |
| 5 | 廣告出現在回答下面 | 9mmy | H | 200 | CONFIRMED | "Ads can appear below the end of a response" |
| 6 | 用一條線隔開；官方強調這條線 | 9mmy、j6fd、3yz4 | H、T、AP | 200 | NOT FOUND → 改寫 | 官方只寫 "clearly labeled as sponsored and visually separated"。9mmy →「廣告通常出現在回答下面，標明是贊助，和回答分開。」；j6fd →「官方特別強調，廣告和回答是分開的。」；3yz4 →「官方自己也把廣告和回答分開放，還清楚標示是贊助。」 |
| 7 | 看到廣告不代表答案被動過手腳 | uz5f | H | 200 | CONFIRMED | "Ads do not influence ChatGPT's answers" |
| 8 | 2 月從美國開始測試 | ads-launch-bullets.items[0]、kbhy | T、H | 200 | CONFIRMED | 2026-02-09 |
| 9 | 那時候只有一小群美國用戶看得到 | kkaf | T | 200 | CHANGED | 官方：測試對象是美國「已登入的成年」Free 與 Go 用戶，沒說一小群 →「那時候只有美國、登入的成年用戶看得到。」 |
| 10 | 8 月擴大到英國、日本、南韓等地 | items[1]、rnkh | T、E | 200 | CONFIRMED（附註） | 8/11 官方更新寫 "has now launched in the United Kingdom, Mexico, Brazil, Japan, and South Korea"；確切上線日官方沒寫（5/7 只說「接下來幾週」）；8 月另有歐洲 31 國 |
| 11 | 9 月 24 日輪到台灣和東南亞 | items[2]、ny5e | A | 200 | CHANGED | 同 #1。items[2] →「9 月 23 日公告輪到台灣和東南亞」；ny5e →「第三步，9 月 23 日公告，才輪到台灣和東南亞。」 |
| 12 | 從小範圍測試到全球擴大走了大半年；已測試大半年 | jm85、s44h | T、A | 200 | CONFIRMED | 2/9 → 9/23 約七個半月；官方自稱 pilot |
| 13 | 官方一路觀察數據才擴大 | avty | T、H | 200 | CONFIRMED | "deliberate, phased approach"；3/26 更新引用早期數據 |
| 14 | 台灣不是第一批，也不是最後一批 | bena | T、X | 200 | CONFIRMED | 官方寫今年會繼續擴大到更多市場（意向，不是保證） |
| 15 | 廣告不會突然消失；接下來只會擴大不會縮小 | 97p6、228y | — | — | OUT OF SCOPE | 預測，未標成觀點；見「觀點」 |
| 16 | Free 和 Go 可能看到廣告 | 6h4r、hwwr、th7i、kat8、myth-compare.points、outro.lines[0] | H、A | 200 | CONFIRMED | — |
| 17 | 真正保證沒有廣告的，只有 Plus | wuun | H | 200 | CHANGED | Plus、Pro、Business、Enterprise、Edu 都沒有廣告 →「真正保證沒有廣告的，要到 Plus 以上。」（說明欄同句一併改） |
| 18 | Plus 以上保證沒有廣告；白紙黑字 | y75y、u23a、2wc7、5jce、table Plus 列 | H | 200 | CONFIRMED | "Plus, Pro, Business, Enterprise, and Edu accounts will not have ads." |
| 19 | 免費版設定裡有不花錢的關閉開關 | mni7、4w53、tk9u、nwkh、5pcq、compare.left[1] | H、HZ | 200 | CONFIRMED | 只在有廣告的地區出現，台灣現在是 |
| 20 | 關掉要換更低額度 | zjwi、dcx6、compare.left[2] | H | 200 | CONFIRMED | — |
| 21 | Go 沒有免費的關閉開關 | 63sh、compare.right[1] | H | 200 | CONFIRMED | "Ads-Free is a Free-plan option" |
| 22 | 只有兩條路：切回 Free 或往上升級 | krra、5zhe | H | 200 | CONFIRMED | "switch back to Free ... or upgrade to a plan that's already ad-free" |
| 23 | Go 頁面寫 "may include ads"，是官方用詞 | myth-big.data、nivj、s6bb、id32、cuwu、pqey、2csg | P | 200 | CONFIRMED | Go 卡片："This plan may include ads."；台灣中文版「此方案可能包含廣告。」 |
| 24 | 這種寫法，法律上叫保留空間 | ufzu | — | — | NOT FOUND → 改寫 | 不是法律用語 →「這種寫法，等於替自己保留空間。」 |
| 25 | Go 付的是更高的訊息、上傳、圖片額度 | nsdk | P | 200 | CONFIRMED | "More messages with tools / More uploads / More image creation" |
| 26 | 官方不會對未滿 18 歲的帳號投放廣告 | wj34、44tt、q1-bullets.items[1] | H、HZ | 200 | CHANGED（精確化） | 官方是「經判定」未滿 18 歲（帳號年齡資訊＋年齡預測）→「官方判定未滿 18 歲的帳號，不會看到廣告。」 |
| 27 | 廣告和回答分開算，不改變模型的答案 | 85kr、g7e2、y9a8、q1-bullets.items[2] | H | 200 | CONFIRMED | — |
| 28 | 看廣告的 Free：額度預設、圖片生成照常 | q2-compare.left、njtm | P | 200 | CONFIRMED | Free 本來就是「有限額且速度較慢的圖像生成」 |
| 29 | Ads-Free 額度變低；官方沒公布降多少 | g3ca、8iyr、q2-compare.right[0] | H | 200 | CONFIRMED | 只寫 "fewer messages" |
| 30 | 圖片生成、深度研究跟著關 | 6e88、q2-compare.right[1] | H | 200 | CONFIRMED | "no access to some tools like image generation or deep research" |
| 31 | 切 Ads-Free「會少看到廣告」 | fxs4 | H | 200 | CHANGED | 官方："No ads" →「所以切了 Ads-Free，你不會看到廣告，但也會少用到一些功能。」 |
| 32 | 表格 Free 兩列 NT$0 | q3-table.rows[0..1] | P、CTW | 200 | CONFIRMED | — |
| 33 | Go 官方月費 8 美元 | q3-table.rows[2][1]、edsu、code 第 1 行 | G、CUS | 200 | CONFIRMED | 美國價；欄名「官方月費」→「美國月費」 |
| 34 | Plus 官方月費 20 美元 | q3-table.rows[3][1] | HP、CUS | 200 | CONFIRMED | HP "Price: $20/month (billed monthly)"；CUS plus.month 20.0 |
| 35 | Go 約 NT$268／月、約 NT$3,211／年（匯率估算） | q3-table.rows[2]、ds5u、7pr3、bir5、caption | P、CTW | 200 | CHANGED | 官網對台灣直接標價：Go $270/每月（CTW：NT$、TWD、270.0、tax inclusive）。rows[2] →「NT$270」「NT$3,240」；ds5u →「一年大約三千兩百多元…」；7pr3 →「官網標給台灣的 Go 月費是 270 元，已經含稅。」；bir5 →「乘上 12 個月，一年是三千兩百四十元。」 |
| 36 | Plus 約 NT$669／月、約 NT$8,027／年 | q3-table.rows[3]、v3vc | P、CTW | 200 | CHANGED | 官網標 $690/每月（CTW plus.month 690.0，含稅）→「NT$690」「NT$8,280」；v3vc「一年大約八千元」→「一年大約八千三百元」 |
| 37 | 台幣數字是估計、不是官方公布的台灣定價 | y7sz、dbba、jjyh、q3-code.caption、youtube.description | P、CTW、M | 200 | CHANGED | 官方台灣台幣價已公開在定價頁（M 也寫具體價格看定價頁）。y7sz →「表上的台幣月費，是官網現在直接標給台灣的價格。」；dbba →「一年的金額是我乘上 12 算的，實際以結帳畫面為準。」；jjyh →「用匯率換算只是估計，實際以官網的台幣價為準。」；caption →「Go 一年 NT$3,240，用台灣官網月費乘 12；匯率換算只是對照」 |
| 38 | 「第三條，Go，官方美金定價每個月 8 元」 | 9hmr | G | 200 | CHANGED（依 #35） | 美元價本身正確，但這一列的台幣欄已換成官方台幣價 →「第三條，Go，台灣官網標價每個月 270 元。」 |
| 39 | 「第四條，Plus，每個月 20 美元」 | y3xm | HP | 200 | CHANGED（依 #36） | →「第四條，Plus，台灣官網標價每個月 690 元。」 |
| 40 | Plus 貴 Go 兩倍多 | 4vai | CTW、CUS | 200 | CHANGED | 20/8 = 2.5、690/270 ≈ 2.56；「貴兩倍多」會被聽成三倍多 →「比較起來，Plus 大約是 Go 的兩倍半價錢，但至少廣告有官方保證。」 |
| 41 | 今天匯率 31.855，大約 31.9 | q3-code 第 1 行、szd9 | BOT | 200 | CONFIRMED | 2026/09/25 13:25 牌告，美元即期賣出 31.855 |
| 42 | 8 × 31.855 = 254.84，大約 255 | q3-code 第 1 行、p2fu | 算術 | — | CONFIRMED | — |
| 43 | 沒填統一編號要「加收」5% 稅 | 75ue | V、CTW | 200 | CHANGED | 5% 營業稅屬實，但台灣台幣價是含稅價，不是再加上去 →「台灣的個人訂閱，沒填統一編號要付百分之五的營業稅。」 |
| 44 | 254.84 × 1.05 = 267.58 ≈ 268 | q3-code 第 2 行、8hyr | 算術 | — | CONFIRMED | 保留作為「美元價換算對照」；第 2 行寫成「254.84 × 1.05 ≈ 268」 |
| 45 | 268 × 12 = 3,211 | q3-code 第 4 行 | 算術 | — | CHANGED | 算錯（268 × 12 = 3,216）。整段改為「官網台幣月費 270（已含稅）」「270 × 12 = 3,240」 |
| 46 | 多數個人用戶沒有填統一編號 | us42 | — | — | OUT OF SCOPE | 個人本來就沒有統一編號 |
| 47 | 跟手機上很多訂閱服務價位差不多 | mjth | — | — | OUT OF SCOPE | 模糊比較，無數字 |
| 48 | 官方定價會變動，回去核對 | tv8c | HG | 200 | CONFIRMED（措辭依 #35） | "we may adjust pricing over time"；「最新的美元數字」→「回官網核對最新的台幣數字」 |
| 49 | 手機 App 或網頁版都找得到設定 | wwyd、settings-steps.steps[0] | H | 200 | CONFIRMED | "Settings > Ad Controls ... on web or iOS"；手機沒看到要更新 App |
| 50 | 選單在左下角或頭像旁邊 | a4xx | HL | 200 | CONFIRMED | 網頁 "Click on your profile icon > Settings"；手機 "profile icon at the bottom of the screen" |
| 51 | 點進 Ad Controls；名字裡有廣告兩個字 | 2nyv、qmz5、steps[1] | H、HZ | 200 | CONFIRMED | 中文介面叫「廣告控制功能」 |
| 52 | Free 才看得到切到 Ads-Free 的選項 | cuxx、fgax、steps[2] | H | 200 | CONFIRMED | — |
| 53 | 點下去前會提醒額度會變低 | h36w | H | 200 | CONFIRMED | "You'll see a prompt that explains the tradeoff" |
| 54 | Go 進同一頁只能管個人化，看不到關掉廣告 | ugxh、6b6m、steps[3] | H | 200 | CONFIRMED（實質） | Ads-Free 只給 Free；Go 畫面實際長相無法不登入核對 |
| 55 | 能調的「只有」廣告要不要跟興趣有關 | iq9t | H | 200 | CHANGED | 還有廣告紀錄、刪除廣告資料、過往對話與記憶開關 →「能調的，主要是廣告要不要跟你的興趣有關。」 |
| 56 | 整個流程大概三十秒 | wpyz | — | — | OUT OF SCOPE | — |
| 57 | Ads-Free「效果跟付錢買 Go 一樣，都是沒有廣告」 | kvw2 | P、H | 200 | CHANGED | Go 可能有廣告，這句和全片論點相反 →「效果甚至比付錢買 Go 還徹底，是真的沒有廣告。」 |
| 58 | 「差別只在於，額度會變低」 | gkia | H | 200 | CHANGED（依 #57、#30） | →「代價是，額度和部分功能都會變少。」 |
| 59 | Plus 帶進更高訊息額度與官方主打的新模型 | c4m8、zeak | P | 200 | CONFIRMED | "Expanded messages and uploads"、"Advanced reasoning models with GPT-6" |
| 60 | 方案階梯圖把 Free、Go、Plus 放在一起 | eri7 | SVG | — | CONFIRMED | 圖上還有 Pro、Business |
| 61 | 額度、模型、「廣告」每一層都畫出來 | 72nt | SVG | — | CHANGED | 圖上只有免費版標「部分國家有廣告」→「額度、模型、價格，每一層差在哪都畫出來了。」 |
| 62 | 廣告只出現在最左邊兩層 | 67it | SVG、H | — | CHANGED | 事實對，但畫面上 Go 那格沒標廣告，觀眾會看到相反的東西 →「圖上只在免費版標了廣告，其實 Go 也可能有。」 |
| 63 | 完整的方案階梯在說明欄的文章裡 | d6pu、approach-diagram.caption | ART、SVG | — | NOT RESOLVED（未改） | 說明欄只自動附 source_guide（ai-free-vs-paid-plans-2026），這張階梯圖屬於另一篇 chatgpt-plans-plus-pro-2026；見「懷疑但沒動」 |
| 64 | 完整比較表在說明欄的文章裡 | tdny、outro.cta | ART | — | CONFIRMED | source_guide 有一張比較表 |
| 65 | 四條路徑的完整算式留在說明欄 | du3c | youtube.description | — | CHANGED | 撰稿版說明欄沒有算式；在說明欄加上四條路徑一年的算式（NT$0、NT$0、270 × 12、690 × 12） |
| 66 | 說明欄：9/24 上線、「真正保證沒有廣告的是 Plus」、台幣是估算不是官方價 | youtube.description | A、H、P、CTW | 200 | CHANGED | 依 #1、#17、#37 改寫，並註明「2026 年 9 月 25 日查看，已含 5% 營業稅」 |
| 67 | 標題、縮圖、hook 字卡 | youtube.title、thumbnail、hook.data | A | 200 | CONFIRMED | 只有「開始有廣告了」這個事實 |
| 68 | 方案階梯圖本身的內容（非口播） | approach-diagram.data.svg | SVG vs P、CTW | 200 | NOT RESOLVED（不能改資產） | 圖上寫「台灣：網頁刷卡以美元計價，沒填統一編號加 5% 營業稅」「台灣幣別以登入 chatgpt.com 後看到的為準」、Plus「GPT-5.6 Sol」，都已和今天的定價頁不符；Go 那格沒有標廣告 |
| 69 | 其餘修辭句（「很多人不知道」「這一點很多人會愣一下」「先講結論」等） | d9he、6rsj、7jze、yd6e、wssi、9t69、gcbd 等 | — | — | OUT OF SCOPE | 不含可查核事實 |
| 70 | tags | youtube.tags | — | — | OUT OF SCOPE | — |

`sources` 同步：「ChatGPT pricing」網址改為轉址後的 https://chatgpt.com/pricing/；新增三筆官方來源（What is ChatGPT Plus?、Introducing ChatGPT Go, now available worldwide、Testing ads in ChatGPT），全部 checked_on 2026-09-25。Inside 報導仍留在來源（第三方，片中已不靠它證實任何數字）。

## 摘要

- 查核項目 70 項（涵蓋全部 180 句、每個字卡欄位、標題、說明欄、縮圖與標籤）：CONFIRMED 39、CHANGED 21（其中 #38、#39、#58 是跟著改的口播措辭）、NOT FOUND 後改寫 2（「一條線」「法律上叫保留空間」）、NOT RESOLVED 2（#63、#68，都和方案階梯圖有關）、OUT OF SCOPE 6。
- 最大的發現：**ChatGPT 官網已經對台灣直接標台幣價**（未登入從台灣打開 chatgpt.com/pricing：Go $270、Plus $690、Pro 從 $3,300，頁面載入的官方設定寫 NT$／TWD、含稅、稅率 5%）。撰稿時「只有登入結帳頁看得到、所以用匯率估算」的前提不成立。表格與口播改用官方台幣價（Go 一年 NT$3,240、Plus 一年 NT$8,280），q3-code 保留美元換算，當作「270 元大約就是美元價換匯再加稅」的對照。
- 撰稿者標出的疑點：Plus 20 美元 CONFIRMED（HP＋CUS）；Go 8 美元 CONFIRMED（G＋CUS），Go 頁「This plan may include ads」CONFIRMED；Ads-Free 開關與代價 CONFIRMED，但「少看到廣告」改成「不會看到」；9/24 10:00 找不到官方出處（見 #1）；18 歲規則改成「官方判定」；台銀 31.855 CONFIRMED（13:25 牌告，只剩對照用途）；5% 稅 CONFIRMED，但台幣價已含稅，不能再加；算式 268 × 12 ≠ 3,211，已隨官方價更正。
- 會過期的事實：台灣台幣價 NT$270／NT$690（定價頁，今天 2026-09-25 看到；HG 寫價格會調整）；台銀匯率（2026/09/25 13:25）；「這禮拜」上線（官方公告日 2026-09-23）；Ads-Free 規則（H，3 天前更新，官方註明各平台文字可能不同）；Plus 價格頁（HP，3 天前更新）。
- 觀點不符：brief 站主觀點寫「免費開關效果跟付錢買 Go 一樣是沒有廣告」，事實上 Go 可能有廣告，kvw2 已按事實改，brief 那句要站主自己改；brief 寫「官方一直強調用一條線隔開」，官方沒有這樣寫；brief「示範或實算」的前提（沒有官方台幣價、要自己加 5%）已被定價頁推翻，大綱第 6 節是否照舊由站主決定。未標成觀點的預測：97p6、228y（廣告不會消失、只會擴大），和 brief「不做沒有根據的推測」不一致；a4qz「免費永遠不是真的免費」、wjbn「官方自己都沒把握」是評論語氣。
- 叫觀眾買哪個方案：沒有任何一句指定該買 Go 或 Plus。最接近建議的都在「我的做法」、有標「我的看法」、和 brief 一致：a6vv、xbum、dzuw、rptf（「如果你只是不想看廣告，免費的開關已經夠用」最像建議），另有 iez3 的條件句。2kvp 明講不替觀眾決定。
- 聽眾檢查：沒有超過 40 字的句子、沒有查證口吻、沒有括號或網址、拉丁字都在發音字典裡。片中用英文介面名稱 Settings／Ad Controls／Ads-Free，台灣中文介面是「設定 > 廣告控制功能」與「無廣告」，用中文介面的觀眾照唸的名字找不到（未改，交站主決定是否兩種都講）。d9he、mni7 連續兩句用「但」開頭。開場約 41 秒（已知的估速問題）。
- lint：`chatgpt-ads-upgrade: 0 errors, 2 warnings`（開場 41 秒、全片約 12.6 分鐘，都是已知的 250 字／分估速）。
- 懷疑但沒動：(1) 台灣上線日期：官方 RSS 是 9/23 02:00 GMT，sitemap 修改時間是 9/24 02:01 GMT，台灣媒體寫 9/24 10:00；片中改用官方頁上的日期「9 月 23 日公告」、拿掉時刻，若站主找到官方寫 9/24 的頁面可以改回。(2)「8 月擴大到英國、日本、南韓」：官方只給更新日期 8/11。(3) da3h「很可能已經看過了」：官方寫的是陸續上線、有相關商品才會出現。(4) 6b6m Go 的實際畫面沒辦法不登入核對。(5) 75ue 的 5% 是網頁訂閱；App 內購由 Apple／Google 收款。(6) 方案階梯圖（#63、#68）：資產不能改，建議換圖或重畫，並把說明欄連到正確文章。(7) 站上文章 chatgpt-plans-plus-pro-2026、ai-free-vs-paid-plans-2026 與那張圖都還寫「台灣網頁以美元計價／台幣價登入後才看得到」，已經過期，是網站的後續工作，不在本片範圍。
- 還沒解決：#63、#68（方案階梯圖）。在站主決定前，這份腳本不能算查核完成。
- **需要第 2 輪：是**（這一輪的事實修改遠超過三處）。
