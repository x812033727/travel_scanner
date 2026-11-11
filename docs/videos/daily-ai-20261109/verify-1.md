# daily-ai-20261109 查核第 1 輪

查核日 2026-11-08（台北時間深夜，跨到 11-09 前完成抓取）。查核代理不是撰稿人。每一條旁白（`text`，Sola 與 Kai 兩位都查；本片沒有 `say`）、每張卡片的 `data`（含 `kicker`、`source`、`key`、`keys`）、章節名、縮圖、`youtube.title`、`description`、`tags` 都抽出來逐條對照（清單在工作區 `_tools/dump.txt`）。
來源：站上 4 篇文章（`/api/travel/guides/life/<slug>?locale=zh-TW`，間隔 1.2 秒，全部 HTTP 200、`status: published`，news_date 與 claims.md 相同），加上 `video.json` `sources` 的 5 個原始來源，用 `Mokaair-editorial/1.0` UA 以 curl 重開（去掉 `<!-- -->` 後讀全文，全部 200、沒有轉址）。另外打開田納西州 ELVIS Act 的法案原文，核對 The Verge 對法律的描述。web search 0 次。
撰稿人沒有打開 MS1（Microsoft），這一輪打開了；其餘四個原始來源撰稿人只拿來核對轉述，這一輪每個數字、引句、日期都對回原文。另有〈笑點檢查〉與〈清楚度檢查〉兩節。

## 來源代號

站上文章（全部 200，published）：

| 代號 | slug | news_date |
| --- | --- | --- |
| TSLA | tech-news-tesla-cybertruck-wind-down-20261106 | 2026-11-06 |
| ART | ai-news-artex-exposed-tools-20261106 | 2026-11-06 |
| NYT | ai-news-nyt-cooking-assistant-20261107 | 2026-11-07 |
| SUNO | ai-news-suno-elvis-eminem-lawsuits-20261108 | 2026-11-08 |

原始來源（全部 HTTP 200，沒有轉址）：

| 代號 | URL（頁面上的日期） |
| --- | --- |
| DC7 | https://decrypt.co/382703/tesla-to-wind-down-cybertruck-production-as-elon-musk-pivots-to-robotaxis-and-ai （馬斯克推文 2026-11-06） |
| VNY | https://www.theverge.com/tech/1029489/nyt-cooking-ai-assistant-review （Jennifer Pattison Tuohy，datePublished 2026-11-07T15:50Z；文末更新註記 11-08） |
| SUV | https://www.theverge.com/ai-artificial-intelligence/1029533/elvis-eminem-suno-ai-music-clone-lawsuit （Terrence O'Brien，datePublished 2026-11-08T17:23Z） |
| TC6 | https://techcrunch.com/2026/11/06/hundreds-of-artex-ai-hacking-tools-found-publicly-exposed-to-the-web/ （Zack Whittaker，10:44 AM PST, November 6, 2026） |
| MS1 | https://www.microsoft.com/en-us/security/blog/2026/10/21/storm-0940-uses-artex-agentic-ai-connectwise-supply-chain-compromise/ （2026-10-21） |
| TNL | https://www.capitol.tn.gov/Bills/113/Bill/HB2091.pdf （田納西州 HB2091／SB2096，Ensuring Likeness, Voice, and Image Security Act of 2024；只用來核對 c26，沒有加進 `sources`） |

## 主張表

| # | 主張 | 位置 | URL | HTTP | 判定 | 修改前 → 修改後 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 今天 11 月 9 日星期一；上週五到這個週末的新聞 | d9a1、hi03；intro、mo-hi | 曆法；站上 4 篇 | 200 | CONFIRMED（2026-11-09 是星期一；11-06 星期五、11-07 星期六、11-08 星期日） | |
| 2 | 上週五 11 月 6 日，馬斯克說特斯拉 2027 年年中左右逐步停產 Cybertruck；不鏽鋼皮卡 | ct01、ct02；ct-what | DC7 | 200 | CONFIRMED（推文 November 6, 2026「winding down production of the Cybertruck at Gigafactory Texas around the middle of next year」；「The stainless-steel pickup」） | |
| 3 | 馬斯克說車隊還會存在很長一段時間；卡片 'Around a long time' | ct04；ct-why | DC7 | 200 | CONFIRMED（回覆用戶「True, but the Cybertruck fleet will be around for a long time.」） | |
| 4 | 報導沒提停產以後的零件和維修 | ct05 | DC7、TSLA | 200 | CONFIRMED（DC7 全文沒有） | |
| 5 | 停產是為了把德州工廠的產能拿去多做 Cybercab | ct08；ct-cab | DC7 | 200 | CONFIRMED（「to make room for increased Cybercab production」，馬斯克推文） | |
| 6 | Cybercab 是機器人計程車，兩個座位，沒有方向盤也沒有踏板 | ct09；ct-cab | DC7 | 200 | CONFIRMED（「Cybercab, Tesla's robotaxi」「a two-seater with no steering wheel or pedals」） | |
| 7 | 據 Decrypt 引述的數字，一直賣不好，銷量約為產線規劃的十分之一；卡片 Per Electrek, via Decrypt | ct12；ct-sales | DC7 | 200 | CONFIRMED（「has struggled to win buyers」「roughly a tenth of the 250,000 units a year that Tesla built its production line to make, according to the outlet」） | |
| 8 | 紐約時報的食譜 App NYT Cooking 加了 AI 助理，照手邊食材改寫出你的版本 | ny01、ny02；ny-what | VNY | 200 | **CHANGED**（原句「第二則在 11 月 7 日週六，……加了 AI 助理」讀成 11/7 上線。11/7 是 The Verge 實測的發布日：記者「in my few days testing it」，文末更新註記說功能「was unofficially announced on a help page」，上線日報導沒寫） | ny01 →「第二則，紐約時報的食譜 App，NYT Cooking，最近加了 AI 助理。」；日期移到 ny06（#11） |
| 9 | 另做新版本，原食譜不動 | ny04；ny-why | VNY | 200 | CONFIRMED（「it doesn't change the existing recipe; it leaves it as is and creates a new one for you」） | |
| 10 | 目前只開放給 iOS 上的訂閱用戶 | ny05；ny-why | VNY | 200 | **CHANGED**（原文「available to subscribers on iOS only at launch」，是上線時的範圍，「目前」說的比來源多） | →「上線時只給 iOS 上的訂閱用戶用。」（同樣字數，ny-why 仍 12.9 秒） |
| 11 | The Verge 記者實測，拿雞柳、米、四季豆去問；幾秒鐘生出新食譜、換了標題 | ny06、ny07；ny-test | VNY | 200 | CONFIRMED（「chicken tenders … rice … green beans」「Within seconds, it created a new version of the recipe, with a new title」）；ny06 加上 #8 移過來的日期 | ny06 →「The Verge 的記者 11 月 7 日週六發了實測，她拿雞柳、米和四季豆去問。」 |
| 12 | 故意問能不能把分層甜點裡的手指餅乾換成牛絞肉；它說甜點裡哪裡都不能放 | ny08、ny09；ny-beef | VNY | 200 | CONFIRMED（「Then I threw in some curveballs」「Could I swap ladyfingers for minced beef in this trifle」「Minced beef cannot be used in place of the ladyfingers or anywhere in this sweet dessert trifle.」） | |
| 13 | 新版本沒辦法另外存 | ny12；ny-fail | VNY | 200 | CONFIRMED（「You can't save your new recipe separately」） | |
| 14 | 烤蛋糕時問奶油，它給了改過那一版的量，沒說哪一版 | ny13；ny-fail | VNY | 200 | CONFIRMED；措辭改了（原句沒說記者在做原版，聽不出為什麼給錯：「when I was cooking the original … gave me the modified recipe's 6 tablespoons」），見清楚度檢查 | →「記者照原版烤蛋糕，問奶油要放多少，它給了改版的量，沒說是哪一版。」 |
| 15 | 那個量真的照做，蛋糕會太乾；卡片「Wrong butter amount, a dry cake」 | ny15；ny-butter | VNY | 200 | **CHANGED（卡片）**（「would have made for a dry cake」，蛋糕沒有真的做壞，原文說兩個版本「Both turned out great」；旁白對，卡片讀成已經烤乾） | 卡片 text 第二行「a dry cake」→「almost a dry cake」（key 本來就是 Almost a dry cake） |
| 16 | 副廚不是主廚；記者說用量和時間還是要跟原食譜對；卡片 kicker「The Verge's advice」 | ny16、ny17；ny-check | VNY | 200 | CONFIRMED／**CHANGED（kicker）**（撰稿人懷疑的一條。副廚的比喻就是 The Verge 的評語：「works well as a sous chef, but it's not the head chef — I still felt the need to double-check amounts and cooking times and cross-reference them with the original」，所以 Kai 引的不是只出自站上文章。但「A sous-chef, not the chef」是評語，不是建議） | kicker「The Verge's advice」→「The Verge's verdict」；claims.md c17 更正出處 |
| 17 | 主菜：11 月 8 日週日，據 The Verge，兩組原告分別告了 AI 音樂公司 Suno | su01、su02；su-lead | SUV | 200 | **CHANGED（措辭）**（「Suno is facing yet another pair of lawsuits」對；但 11/8 是報導日，報導沒寫起訴日，原句「時間是 11 月 8 日週日」接「有兩組原告……告了」讀成 11/8 起訴） | su01 →「第三則是今天的主菜，來自 The Verge 11 月 8 日週日的報導。」；su02 →「報導說，有兩組原告，分別告了 AI 音樂公司 Suno。」 |
| 18 | 標題「Elvis and Eminem vs. Suno」；縮圖副標「Elvis, Eminem vs. Suno」；卡片 su-lead「Elvis, Eminem / vs. Suno」 | youtube.title、thumbnail.data.sub；su-lead | SUV | 200 | **CHANGED**（撰稿人懷疑的一條。原告是「A group of rights holders of Elvis Presley's music and the publisher of some of Eminem's biggest records」，不是本人；SUV 自己的標題是「Elvis and Eminem rights holders are suing Suno」。縮寫的標題在八語標題與縮圖上會讀成本人提告，Elvis 已經過世） | 標題 →「Tech Signal 11/9｜Elvis, Eminem rights holders vs. Suno」；縮圖副標 →「Elvis, Eminem rights holders vs. Suno」；su-lead →「Elvis, Eminem rights / **holders vs. Suno**」（20／17 字） |
| 19 | 想像打一行字，說要一首老派搖滾，幾秒後新歌就出來；Suno 做的就是這種事，你輸入文字，它生成音樂和歌詞 | mc01、mc02；mc-scene | SUV | 200 | CONFIRMED（撰稿人懷疑的一條。mc01 是節目情境。mc02 由三點撐住：發言人「we do not allow prompts for specific artists' names and songs」（用文字下提示）、原告「generates music and lyrics」、訴狀「in seconds」；沒有說到操作細節，沒有超出來源） | |
| 20 | 原告：Elvis Presley 的音樂權利人；Eminem 幾張招牌唱片的出版商；卡片 Elvis rights holders, Eminem's publisher | su03；su-who | SUV | 200 | CONFIRMED（原文見 #18；「貓王」是通稱） | |
| 21 | 他們都說，Suno 違法生成模仿這些歌手的音樂和歌詞 | su04；su-claim | SUV | 200 | CONFIRMED（「claiming it illegally generates music and lyrics that mimic those artists」；以「他們都說」標成指控） | |
| 22 | 提示詞、權利人的解釋 | mc03、mc04；mc-terms | SUNO | 200 | CONFIRMED（解釋） | |
| 23 | 照原告的說法，Suno 沒有拿到授權；卡片 No license, per the suit | mc08；mc-sides | SUV | 200 | CONFIRMED（訴狀「without a license」） | |
| 24 | Presley 案律師說 Suno 違反美國田納西州的 ELVIS Act | mc09、mc57；mc-law、mc-tw2 | SUV | 200 | CONFIRMED（「The lawyers in the Presley suit claim that Suno has violated Tennessee's … (ELVIS) Act」；以「律師說」標成主張，不是結論） | |
| 25 | 據 The Verge，這部法律規定 AI 公司複製歌手的聲音是違法的；卡片 AI cloning a singer's voice、key No AI voice cloning | mc10；mc-law2 | SUV、TNL | 200 | **CHANGED**（SUV 確實寫「which makes it illegal for an AI company to clone a singer's voice」，但法案原文管的是「without authorization」「without such individual's prior consent」：未經同意使用一個人的聲音或肖像、散布主要用途是未經授權產生聲音的工具，追民事責任；沒有一律禁止複製聲音，也不只管 AI 公司。旁白掛了 The Verge，卡片 key「No AI voice cloning」沒有掛名，等於替節目下了法律的範圍） | mc10 →「據 The Verge，這部法律讓 AI 公司未經同意複製歌手的聲音，成為違法的事。」；卡片 text →「AI cloning a voice, / **without consent**」，key →「Clones need consent」 |
| 26 | 英文全名縮寫起來就是 ELVIS；報導沒說是照貓王取的 | mc11、mc13；mc-acr、mc-acr2 | SUV、TNL | 200 | CONFIRMED（SUV「Ensuring Likeness Voice and Image Security (ELVIS) Act」；兩份來源都沒說命名由來） | |
| 27 | Eminem 出版商一案用什麼法律，報導沒有說明 | mc15、mc62、so02；mc-em、mc-next | SUV、SUNO | 200 | CONFIRMED（SUV 只寫 Presley 案的法律依據） | |
| 28 | 訴狀：人要花好幾年學的東西，Suno 沒有授權，幾秒鐘就複製；卡片引句「From the Presley complaint」 | mc19、mc20；mc-quote2 | SUV | 200 | CONFIRMED（「Later in the complaint, the lawyers write that "… coldly replicating without a license in seconds what takes years to learn …"」，前一段是 Presley 權利人的律師，所以是 Presley 訴狀；引句逐字） | |
| 29 | Suno 不是第一次被告；據 The Verge，一疊官司，原告包括 Sony、UMG 這些大型音樂公司；卡片 Sony, UMG, and more | mc24、mc25；mc-pile | SUV | 200 | CONFIRMED（「the pile of lawsuits Suno is currently facing from Sony, UMG, Isbell, Reservoir Media, and more」） | |
| 30 | The Verge 說兩案很像 9 月 Jason Isbell 等人的官司；那一案說 Suno 模仿原告，但沒直接主張著作權侵權；卡片「Imitation, not copyright」 | mc28、mc29；mc-isb | SUV | 200 | CONFIRMED（旁白）／**CHANGED（卡片）**（「closely mirror one filed by Jason Isbell and others in September, which claimed Suno created imitations of the plaintiffs but did not claim copyright infringement directly」；卡片拿掉了 directly） | 卡片 →「Imitation, / **not directly copyright**」（22 字） |
| 31 | 著作權的解釋；Kai「那一案告的不是作品，是模仿了人？」 | mc30、mc31；mc-isb2 | — | — | CONFIRMED（解釋；Kai 的問句只講 Isbell 案，跟 #30 一致） | |
| 32 | 照報導的寫法，這兩案告的重點是 Suno 做出來的東西在模仿誰；「學」不是唯一的重點；卡片「Not what it learned. / Who it sounds like」 | mc32、mc33；mc-turn | SUV | 200 | CONFIRMED（旁白）／**CHANGED（卡片）**（旁白對到「music and lyrics that mimic those artists」，mc33 說「不是唯一的重點」有保留；卡片「Not what it learned」卻說成跟學無關，但 Presley 訴狀也說 Suno「mechanically encoded itself with artists' identities」，跟學有關） | 卡片第一行 →「Not just learning.」 |
| 33 | 像不像要法院決定，現在都還只是原告的指控 | mc35、mc66；mc-judge、mc-view2 | SUNO、SUV | 200 | CONFIRMED（沒有判決；不下法律結論） | |
| 34 | Suno 發言人說，是要幫人做新的原創音樂，不是要利用任何人的名字或肖像；卡片 "New, original music" | mc36、mc37；mc-suno | SUV | 200 | CONFIRMED（「Suno exists to help people create new, original music, not to trade on anyone's name or likeness」） | |
| 35 | 「她也說了 Suno 怎麼防」；不讓在提示詞裡打特定歌手名字和歌名；跟外部廠商合作檢查上傳的音檔和歌詞；卡片 Suno says it | mc38、mc39、mc40；mc-guard | SUV | 200 | CONFIRMED（「we do not allow prompts for specific artists' names and songs and work with third-party providers to screen uploaded audio files and lyrics for potential misuse」，自述，標題「Suno says it」）／**CHANGED（措辭）**（來源只寫「Suno spokesperson Cat McCormack」，沒寫性別，「她」是猜的） | mc38 →「發言人也說了 Suno 怎麼防。」 |
| 36 | 它說它有擋，擋不擋得住，報導裡沒有人實際測過 | mc42；mc-kai2 | SUV | 200 | CONFIRMED（SUV 只引述發言人） | |
| 37 | 至少它自己也說，藝人的名字不能隨便用 | mc43；mc-kai2b | SUV | 200 | CONFIRMED（「not to trade on anyone's name … we prohibit any unauthorized use of an artist's work」） | |
| 38 | 原告說錢流向 Suno；訴狀說 Suno 把藝人的身分、努力、創意和時間編進系統，變成現金輸送帶；卡片引句 | mc46、mc47、mc48；mc-quote1 | SUV | 200 | CONFIRMED（「Suno has mechanically encoded itself with artists' identities, hard-work, creativity, and time, and harnessed them all for a consistent conveyor belt of cold hard cash.」；原文 of 與 cold 之間少一個空格，卡片寫對了） | |
| 39 | 要賠多少、Suno 賺多少，報導都沒寫 | mc50；mc-nonum | SUV、SUNO | 200 | CONFIRMED | |
| 40 | 照訴狀的說法，Suno 想讓人類的創意變得過時；卡片 "Human creativity obsolete" | mc51；mc-lose | SUV | 200 | CONFIRMED（「aims to make human creativity obsolete」；卡片是片段，沒有改字） | |
| 41 | 照原告的說法，Suno 沒拿到授權，就拿別人的招牌去賺錢 | mc54；mc-lose2 | SUV | 200 | CONFIRMED（#23＋#38 的白話，標成原告的說法） | |
| 42 | 報導完全沒有提到台灣或亞洲 | mc56；mc-tw | SUV、SUNO | 200 | CONFIRMED | |
| 43 | 接下來看三件事；卡片 source The Verge | mc59–mc63；mc-next | SUV | 200 | CONFIRMED（節目依 #25、#27、#36 整理，沒有預測結果） | |
| 44 | 我的看法：學習不是問題；拿別人的聲音和名氣做生意先問是基本禮貌；法院怎麼判我不知道 | mc64–mc66；mc-view、mc-view2 | brief.md | — | OUT OF SCOPE（觀點，見摘要） | |
| 45 | 11 月 6 日週五，據 TechCrunch，研究人員發現好幾百套 Artex 露在公開網路上 | af02；af-news | TC6 | 200 | CONFIRMED（「hundreds of copies of a Chinese-made AI hacking tool publicly exposed to the internet」，November 6, 2026） | |
| 46 | Artex 是開源的 AI 工具，會自己去找電腦系統的弱點；開源的解釋 | af03、af04；af-what | TC6 | 200 | CONFIRMED（「open source autonomous penetration testing tool, meaning software that automatically probes computer systems for weaknesses」「free for anyone to download」） | |
| 47 | 7 月公開以後，已跟好幾起真實的網路攻擊扯上關係 | af06；af-why | TC6 | 200 | CONFIRMED（「linked to several cyberattacks since its public release in July」） | |
| 48 | Microsoft 說，一個跟中國國家背景一致的駭客組織，從 9 月起用它自動攻擊了全球數百個組織；卡片「Hundreds of organizations hit」 | af07；af-ms | MS1 | 200 | **CHANGED**（撰稿人沒打開的一條。MS1：「As early as September 2026, Storm-0940, a China-state aligned actor, used … ARTEX to automate attacks targeting hundreds of organizations globally」，同文「the majority of the targeting wasn't successful」。「從 9 月起」少了 as early as；「攻擊了」與卡片的「hit」讀成數百個組織都被打中，原文是鎖定、且大多沒成功；「背景一致」不是 aligned 的意思） | af07 →「Microsoft 說，一個跟中國國家立場一致的駭客組織，最早從 9 月起，就用它自動攻擊全球數百個組織。」；卡片 →「Hundreds of / **organizations targeted**」（22 字），key「Hundreds of orgs hit」→「Hundreds targeted」 |
| 49 | 資安公司 Censys 找到超過 800 套，從網路上就連得進去，登入不用密碼；卡片 800+ | af08、af09；af-open | TC6 | 200 | CONFIRMED（「more than 800 distinct deployments of Artex that were accessible from the web without needing a password to log in」） | |
| 50 | 研究人員說不是每一套都被拿去做壞事，很多是有授權的測試人員在用；有授權的測試的解釋 | af12、af13；af-fair、af-test | TC6 | 200 | CONFIRMED（「not every instance of Artex is operated maliciously and many are used for authorized testers」；解釋是一般常識） | |
| 51 | 軟體本來不需要放到網路上，為什麼有幾百套露在外面還不清楚 | af14；af-why2 | TC6 | 200 | CONFIRMED（「it's unclear why hundreds of these Artex systems are exposed to the web, as the software does not require them to be accessible from the internet」） | |
| 52 | TechCrunch 說，公開的系統連攻擊工具也露出來，像藏在別人網路裡的惡意程式 | af15；af-kit | TC6 | 200 | CONFIRMED（「also expose attack tools, such as implants (hidden malicious software)」；沒有講用法） | |
| 53 | CrowdStrike 把 9 月一起針對韓國金融業的攻擊算到一個用 Artex 的駭客頭上；部分原因是駭客把目錄公開在網路上 | af18、af19；af-kr、af-kr2 | TC6 | 200 | CONFIRMED／**CHANGED（措辭）**（「attributed the attacks to a Chinese-speaking hacker who used an Artex instance … in part because the hacker had left an "open directory" hosting the system」；原文 the attacks 是複數，「一起」把它說成一起） | af18 拿掉「一起」 |
| 54 | Censys 的資料顯示這套系統公開了好幾個月，攻擊資料似乎不只韓國銀行 | af21；af-kr3 | TC6 | 200 | CONFIRMED（「publicly exposed for months, and appeared to contain more attack data that extended "well beyond South Korean banks"」） | |
| 55 | TechCrunch 說，很多跟 Artex 有關的攻擊靠的是基本弱點，像弱密碼或沒開多因素驗證；多因素驗證的解釋 | af23、af24；af-lesson、af-mfa | TC6、ART | 200 | CONFIRMED（「exploiting simple vulnerabilities, such as guessing weak or known passwords, and a lack of multi-factor authentication」） | |
| 56 | Artex 宣布不再開源，新版本只給付費客戶；還有幾十份副本留在程式碼分享網站 | af27、af28；af-closed | TC6 | 200 | CONFIRMED（「go closed-source, effectively limiting further releases for paid customers」「dozens of copies of Artex's code available on code-sharing sites」） | |
| 57 | 真心話：最重要是 Suno 兩件新官司；最不確定 Eminem 一案的法律依據 | so01、so02；so-take | SUV、brief.md | 200 | CONFIRMED（後半依 #27）／OUT OF SCOPE（觀點） | |
| 58 | 回扣：不肯把牛絞肉放進甜點的食譜助理 | so03；so-call | VNY | 200 | CONFIRMED（依 #12） | |
| 59 | 完整整理在 Mokaair，連結在說明欄；說明欄四個網址 | so05；so-site；description | 站上 4 篇 | 200 | CONFIRMED（四篇 published） | |
| 60 | outro：AI 跟人學歌差在哪？原告說，差在授權和速度 | ou01；outro | SUV | 200 | CONFIRMED（依 #28：without a license、in seconds）；句子為了時間改了，見清楚度檢查 | →「原告說，AI 跟人學歌，差在授權和速度。」 |
| 61 | 說明欄揭露（AI 合成語音、AI 配樂、Claude 撰稿、訴訟是指控、AI Fail 不說明攻擊方法、不構成建議）；章節名；tags | youtube.description、chapters、tags | — | — | CONFIRMED／OUT OF SCOPE | |
| 62 | 串場與 Kai 的反應句（hi01、hi02、ct03、ct07、ct11、ny03、ny11、su06、mc05、mc06、mc07、mc17、mc18、mc23、mc26、mc34、mc41、mc44、mc45、mc49、mc52、mc53、mc55、mc58、mc61、mc67、mc68、af01、af05、af16、af22、af30、so04 等） | 各處 | — | — | OUT OF SCOPE（不含新事實；沒有編主持人的私人經驗） | |

## 笑點檢查

逐句看 claims.md〈笑點〉列的每一句，加上卡片上接梗的字。五條標準：暗示錯誤或來源沒有的事實、新的數字、替真人編話、打一般人、雙關或諧音。

| # | 笑點 | 位置 | 判定 | 理由 | 修改前 → 修改後 |
| --- | --- | --- | --- | --- | --- |
| 1 | 「『車隊還會存在很長一段時間』，這句話聽起來，很像分手時說的『我們還是朋友』。」（撰稿人不確定的第 1 個） | ct06；卡片 ct-ex | **留旁白，改 key** | 前半是馬斯克原話的中譯（#3），後半是一般的分手說法，主詞是「這句話聽起來很像」，沒有把「我們還是朋友」放進馬斯克嘴裡；笑的是有權力的人的回覆，沒有新數字、不是雙關。卡片有 kicker「Sola's analogy」，沒問題；但 key「'Let's stay friends'」單獨出現在關鍵句帶，沒有 kicker、又加了引號，英文觀眾會讀成馬斯克說的。 | key →「Sounds like a breakup」 |
| 2 | 「所以 Cybertruck 是被一台連方向盤都沒有的車，搶走了工作。」「連車都會被自動化取代！」 | ct10、ct11；ct-joke | **留** | 接 #5、#6，一聽就是誇張；對象是產品。 | |
| 3 | 「十分之一？那條產線都在放假吧！」 | ct13 | **留** | 誇張，沒有新數字；「放假」不會被當成產線停工的事實（ct08 剛說停產是明年）。 | |
| 4 | 「所以我要不要換手機？」×2；「不用，這次被換掉的是一台皮卡」「不用，你要換的是密碼」 | ct14、ct15、af25、af26 | **留** | 固定梗；af26 接 #55，是一般的帳號提醒。 | |
| 5 | 「冰箱剩什麼，它就幫我湊一道菜？」 | ny03 | **留** | Kai 的猜想，ny04「差不多」接著講事實。 | |
| 6 | 「這大概是今天整個 AI 產業，守得最成功的一道安全防線。」「終於有 AI 敢對人類說不了！」（撰稿人不確定的 ny10） | ny10、ny11；ny-joke | **留** | 「大概」加上「整個 AI 產業」，明顯是誇張，不會被當成評比；VNY 自己也稱讚「Good call」「smart enough to know when to say no」，方向跟來源一致；笑的是產品，沒有新數字、不打人、不是雙關。卡片 kicker「Sola's take」。「今天」指節目的這一集，可以接受。 | |
| 7 | 「所以蛋糕差點變成另一份食譜的蛋糕？」 | ny14 | **留** | 想歪，ny15 用記者的話更正。 | |
| 8 | 「所以這部法律，是照貓王的名字取的？」（撰稿人不確定的 mc12） | mc12；mc-acr | **留** | Kai 的問句，mc13 立刻說報導沒這樣說，沒有把命名由來說成事實。 | |
| 9 | 「不過這個縮寫，取得比很多歌名都用心。」（撰稿人不確定的 mc14） | mc14；mc-acr2 | **改** | 「取得用心」暗示有人刻意把縮寫拼成 ELVIS，正好是 mc13 剛說來源沒有的命名由來，前後打架；「比很多歌名」順手笑了寫歌的人，不是公司或權力者。不是雙關，但笑點建立在來源沒有的事實上。 | →「不過一部縮寫拼成 ELVIS 的法律，現在真的被拿來替 Elvis 的歌打官司。」（情境的反差，事實照 #24、#26）；卡片「An acronym / with real effort」→「The ELVIS Act, / now for Elvis」，key「A name with real effort」→「ELVIS Act, for Elvis」 |
| 10 | 「所以那一案，我們只知道告了，還不知道用什麼告。」 | mc16 | **留** | #27 的白話，不暗示原告隱瞞。 | |
| 11 | 「那模仿秀怎麼辦？模仿歌手的藝人，也要一起被告嗎？」「模仿秀的人，至少用的是自己的喉嚨。」（撰稿人不確定的 mc21／mc22） | mc21、mc22；mc-joke1、mc-joke1b | **留旁白，改卡片** | mc21 是誇張的問句，沒有說模仿藝人會被告；mc22 替模仿藝人說話（他們用的是自己的聲音），比較的是人與 AI，不是笑一般人；沒有說模仿秀合法或 Suno 違法，不是法律結論；「喉嚨」不是諧音。卡片「Their own / throat」英文讀起來像在講身體部位，key 已經是 own voice。 | 卡片 →「Their own / **voice**」 |
| 12 | 「好，這一分我先記在你那邊。」「一比一！」 | mc23、mc44 | **留** | 計分梗，沒有事實。 | |
| 13 | 「一疊？」「對，Suno 的官司，已經可以出一張精選輯了。」 | mc26、mc27；mc-pile2 | **留** | 接 SUV 的「pile」，沒有新數字；笑的是公司。 | |
| 14 | 「你看，它有擋，連打歌手的名字都不行！」 | mc41 | **留** | Kai 的立場，mc42 立刻說這是公司自己說的。 | |
| 15 | 「第一件，我賭會有很多律師很忙。」 | mc61 | **留** | 意見，不預測判決。 | |
| 16 | 「可是如果每首歌都要先問，AI 根本學不完吧？」「那就少學一點，人類歌手也沒有聽完全世界的唱片才出道。」 | mc68、mc69 | **留** | 意見與誇張的對比，沒有事實主張。 | |
| 17 | 「一套專門找別人弱點的工具，自己連密碼都沒設。」（撰稿人不確定的 af10） | af10；af-joke | **留** | 事實照 #49，主詞是「工具」，沒說是誰設的、也沒說他們都是駭客；af12 緊接著講很多是授權測試人員。 | |
| 18 | 「這是小偷把萬能鑰匙，掛在自己家門口吧！」（撰稿人不確定的 af11） | af11 | **改** | 「小偷」把 800 多套的主人都說成壞人，可是 TC6 說很多是有授權的測試人員（#50），兩句之後才更正；笑點等於暗示來源沒有的事，也打到正當工作的測試人員。 | →「這是鎖匠把萬能鑰匙，掛在自己家門口吧！」（鎖匠是替人開鎖、也可能被濫用的專業，對得上滲透測試工具，笑的仍是設定） |
| 19 | 「所以連武器庫都開放參觀？」 | af16 | **留** | 誇張，接 #52，沒有講任何工具怎麼用。 | |
| 20 | 「這就像小偷把作案行程表貼到網路上，還設成公開。」 | af20；af-kr2 | **留** | 對象是 CrowdStrike 指認的攻擊者，不是一般人；接 #53 的「in part because」，沒說駭客因此被抓。 | |
| 21 | 「壞人也會忘記鎖門，我有點安心。」 | af22 | **留** | 反應。 | |
| 22 | 「門現在才鎖，可是鑰匙早就被複製出去了。」「這集的教訓，是先鎖自己家的門。」 | af29、af30；af-end | **留** | 類比接 #56，「鑰匙」對的是程式碼副本，沒有新數字。 | |
| 23 | 「今天最有原則的 AI，是那個不肯把牛絞肉放進甜點的食譜助理。」「連食譜 AI 都懂得說不……」 | so03、so04；so-call | **留** | 回扣 #12，笑的是產品。 | |
| 24 | 「這題，主菜時我們吵給你聽。」 | su06 | **留** | 串場。 | |
| 25 | 縮圖「Ask **first**?」 | thumbnail | **留** | Sola 的看法（mc65）。 | |

笑點總計：25 項，留 21 項，改 4 項（#1 key、#9、#11 卡片、#18），刪 0 項。全片沒有雙關或諧音、沒有新的數字、沒有替真人編的引句；修完後沒有打一般人的笑點（#9 原本笑歌名，#18 原本把測試人員算成小偷）。

## 清楚度檢查

照 daily-brief.md §一之〇。

- 句子完整性檢查（任務給的 node 指令，含 key 長度與 keys 數量）：修改前 0 行，修改後 0 行。`big`、`quote`、`outro` 都沒有 `reveal`；所有 `key`／`keys` ≤24 字；改過的卡片 text 每行 ≤22 字。
- 每則前兩句：
  - Cybertruck：ct01 說發生了什麼，ct02 解釋是什麼車，ct03／ct04 由 Kai 問「已經買了的人怎麼辦」帶出跟一般人的關係。符合。
  - NYT Cooking：原本 ny01 把 The Verge 實測的日期說成上線日（主張表 #8）；改完 ny01「加了 AI 助理」、ny02「能照你手邊的食材改寫出你的版本」，兩句就是發生什麼與跟你有什麼關係。ny13 原本沒說記者在做原版，聽不出「給了改過那一版的量」為什麼是錯，補「照原版」。
  - Suno：su01／su02 先說報導與誰被告，Kai 的 su05 問一般人會問的問題；主菜 mc01／mc02 再從場景講 Suno 是什麼。Monologue 停在問題前是節目格式。
  - Artex：af01 定位單元，af02 說發生了什麼，af05／af06 由 Kai 問跟一般人有沒有關係。符合。
- 生字第一次出現就解釋：Cybertruck、Cybercab／機器人計程車、trifle（分層甜點）、提示詞、權利人、ELVIS Act、著作權、開源、有授權的測試、多因素驗證都有解釋。「權利人」第一次出現在 su03，解釋在兩句後的 mc04（中間只隔 su04），「提示詞」的情境在 mc02 先講；沒有搬動場景（見〈懷疑但沒改〉）。
- 不往回指：outro 的 ou01 原本先重講問題再回答，這一輪為了時間拿掉問句，但把問題寫進答案句「原告說，AI 跟人學歌，差在授權和速度。」，離 su05 十分鐘也聽得懂。so02「Eminem 出版商那一案」重說名字，沒有寫「剛剛那案」。
- 出處短講：每則一次（據 Decrypt、據 The Verge、據 TechCrunch）；su02 改成「報導說」，因為 su01 已經說了 The Verge。mc25、mc28、mc10 再提 The Verge，是為了把法律描述與「一疊官司」標成報導的說法，不是轉引鏈。
- 一句一件事：沒有一句同時塞兩個數字和兩個名字。

畫面狀態：改完後用 lint 的估計時間軸（`tools/video/core/timeline.mjs` 的 `estimateTimeline` 加 `cadence.mjs` 的 `slideStates`）重算，outro 13.0 → **12.3 秒**（仍是三句：答案、留言題、訂閱邀請）；全片最長 12.9 秒（ny-why、mc-scene、so-take、so-call，沒動）。第一版改動讓 ny-test 13.6、ny-fail 13.6、su-lead 13.3 秒超過，已縮短 ny06、ny13、su01、su02，改完 ny-test 12.8、ny-fail 11.9、su-lead 12.4。

## 摘要

- 查了 62 條（同一事實在多處出現時合為一條）加 25 項笑點：CONFIRMED 44、CHANGED 14（含措辭與卡片）、NOT FOUND 0、OUT OF SCOPE 4（#44、#61、#62；#57 部分）。
- 事實改動 12 處：(1) NYT Cooking 的 11/7 是 The Verge 實測日，不是上線日（ny01、ny06）；(2) iOS 訂閱用戶是「上線時」的範圍（ny05）；(3) 卡片「a dry cake」→「almost a dry cake」，蛋糕沒有真的烤壞（ny-butter）；(4) ny-check kicker：副廚就是 The Verge 的評語，不是建議，改「The Verge's verdict」，claims.md c17 更正出處；(5) 11/8 是 The Verge 的報導日，不是起訴日（su01、su02）；(6) 標題、縮圖副標、su-lead 卡片加上 rights holders，原告不是 Elvis 或 Eminem 本人；(7) ELVIS Act 管的是未經同意的複製，旁白 mc10 與卡片 mc-law2 補上（對了法案原文）；(8) Isbell 案「沒有直接」主張著作權侵權，卡片 mc-isb 補 directly；(9) 卡片 mc-turn「Not what it learned」→「Not just learning」（訴狀也說到把藝人的身分編進系統）；(10) 發言人的性別來源沒寫，mc38「她」→「發言人」；(11) Microsoft：最早從 9 月起、攻擊鎖定（大多沒成功），af07 與卡片 af-ms「hit」→「targeted」、「國家背景一致」→「國家立場一致」；(12) CrowdStrike 歸因的是複數攻擊，af18 拿掉「一起」。
- 撰稿人的四個疑問：af07 改（#11）；mc02 留（三點來源合起來撐得住）；ny-check 改 kicker（副廚其實是 The Verge 的話）；標題改成「Elvis, Eminem rights holders vs. Suno」。
- 笑點：改 4 項，刪 0 項。撰稿人的疑問：ct06 旁白留、key 改；af10 留、af11 改（小偷→鎖匠）；mc12 留、mc14 改（不暗示命名由來）；mc21／mc22 旁白留、卡片 throat→voice；ny10 留。
- 訴訟：每一句都標成「他們都說」「律師說」「原告的說法」「訴狀說」；mc35、mc66 明說要法院決定、現在都是指控；說明欄同樣寫明。ELVIS Act 的效力掛 The Verge，並補上「未經同意」，節目沒有說 Suno 違法或會輸。
- 「據報導」與公司自述：Decrypt（銷量引 Electrek，卡片 kicker 寫明）、The Verge、TechCrunch 各有掛名；Suno 的防護是「它說」「發言人說」、卡片標「Suno says it」；Microsoft 的說法以「Microsoft 說」開頭；Censys、CrowdStrike 都有掛名。
- 唸出來的日期：11/6 週五（馬斯克推文、TechCrunch）、11/7 週六（The Verge 實測發布）、11/8 週日（The Verge 報導）、2027 年年中左右（馬斯克）、7 月（Artex 公開）、9 月（Isbell 案、韓國金融業攻擊、Storm-0940 最早開始），都與原文相符。
- `sources` 5 個網址 2026-11-08 全部 HTTP 200，`checked_on` 維持 2026-11-08（就是本輪抓取的日期）。TNL 只用來核對，沒有加進 `sources`（查核不加新來源條目；要不要放進說明欄由站主決定）。
- 會過期的事實：Cybertruck 停產時程與售後安排（DC7 2026-11-06）；NYT Cooking 助理的平台範圍（VNY 2026-11-07，「at launch」）；兩件 Suno 訴訟的進度、Eminem 案的法律依據、Suno 的防護（SUV 2026-11-08）；Censys 的 800 多套（TC6 2026-11-06）與 Artex 閉源後的情況。
- 觀點：mc64、mc65 以「我的看法是」標明，mc66 以「我不知道」標明，so01、so02 以「說一句真心話」「我最不確定的」標明，與 brief.md〈站主觀點〉一致（學習不是問題、拿別人的聲音和名氣做生意要先問、現在都是指控、不確定 Eminem 案的法律依據）。沒有不一致。
- 聽眾檢查（只報告）：超過 40 字（不算標點與空白）的句子 11 句：su03 53、af02 47、af07 46（本輪改過）、ct12 45、af15 44、af23 44、ct01 43、af18 43、mc09 42、af08 42、mc25 41；su03 最長，可以考慮拆成兩句。沒有「經查證」「根據官方文件」「本影片」、括號或網址；揭曉都在介紹句之後。本輪沒有新增字典外的拉丁詞（Elvis、ELVIS、Act、The Verge、Microsoft 都已在字典或撰稿人加過）。
- lint：`node tools/video/cli.mjs lint --slug daily-ai-20261109` → `daily-ai-20261109: 0 errors, 3 warnings`（開場章節長度：本節目沒有開場濃縮；「11」說了 5 次（d9a1、ct01、ny06、su01、af02）：每則各自說日期，照編輯指示；投影片順序跟 daily-ai-20261106 有 86% 相同：同一節目的固定版型）；估 13.6 分鐘，150 句。
- 懷疑但沒改：
  - ct12 的「十分之一」：Electrek 用的是包含 Cybertruck 的「other models」類別 8,295 輛去算，DC7 照轉；旁白掛了「據 Decrypt 引述的數字」，卡片寫 Per Electrek，沒改。
  - mc33「『像』才是」：照 The Verge 的寫法（mimic、AI music clones）可以這樣說，但訴狀也講到「encoded itself」；旁白前半已說「不是唯一的重點」，只改了卡片。
  - mc10 仍保留 The Verge 的「AI 公司」：法案本身不只管 AI 公司，但那是 The Verge 對這一案的描述，旁白掛了名，只補「未經同意」。
  - 「權利人」第一次出現（su03）比解釋（mc04）早一句；要調整得搬動場景順序，留給撰稿人或站主試聽時判斷。
  - ny10 的「今天」：新聞是 11/7，節目是 11/9；指的是這一集，沒改。
  - af-intro「翻車的是一套 AI 駭客工具」：翻車的是使用者把它露在網路上的設定，章節名「駭客工具自己沒上鎖」也一樣；af10 之後有講清楚，沒改。
- 需要第二輪：**是**。本輪改了 12 個事實（超過 3 個）。所有主張都已判定，沒有懸而未決的。
