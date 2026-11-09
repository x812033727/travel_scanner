# daily-ai-20261109 主張與證據

每一行：編號｜主張（旁白或卡片上的說法）｜站上文章；原始來源｜來源查證日｜行 id（場景）。
事實只用站上 news_date 2026-11-06、11-07、11-08 已發布的文章（`/api/travel/guides/life/<slug>?locale=zh-TW` 取得，2026-11-08，4 篇皆 HTTP 200、`status: published`）與它們列的來源。
撰稿人 2026-11-08 也打開了 SUV、DC7、VNY、TC6 四個原始來源（HTTP 200），只拿來核對文章的轉述；MS1 沒有打開，相關的一句（c34）依站上文章 ART 的轉述，查核代理要對回原文。
「自述」＝公司自己公布、沒有第三方確認；「指控」＝訴狀裡原告一方的說法；「解釋」＝節目用一句白話解釋名詞，是一般常識，不出自來源；「節目」＝節目自己的整理或看法；「笑點」＝沒有事實主張的誇張或類比，列在最後一節給笑點檢查。

站上文章簡稱：
- SUNO＝https://mokaair.com/zh-TW/life/ai-news-suno-elvis-eminem-lawsuits-20261108 ；SUV＝https://www.theverge.com/ai-artificial-intelligence/1029533/elvis-eminem-suno-ai-music-clone-lawsuit
- TSLA＝https://mokaair.com/zh-TW/life/tech-news-tesla-cybertruck-wind-down-20261106 ；DC7＝https://decrypt.co/382703/tesla-to-wind-down-cybertruck-production-as-elon-musk-pivots-to-robotaxis-and-ai
- NYT＝https://mokaair.com/zh-TW/life/ai-news-nyt-cooking-assistant-20261107 ；VNY＝https://www.theverge.com/tech/1029489/nyt-cooking-ai-assistant-review
- ART＝https://mokaair.com/zh-TW/life/ai-news-artex-exposed-tools-20261106 ；TC6＝https://techcrunch.com/2026/11/06/hundreds-of-artex-ai-hacking-tools-found-publicly-exposed-to-the-web/ ；MS1＝https://www.microsoft.com/en-us/security/blog/2026/10/21/storm-0940-uses-artex-agentic-ai-connectwise-supply-chain-compromise/

## Monologue

c1｜2026-11-09 是星期一（曆法）；hi03「上週五到這個週末的科技新聞」：三篇的 news_date 是 11-06（TSLA、ART）、11-07（NYT）、11-08（SUNO）｜各站上文章｜2026-11-08｜d9a1, hi03

### Cybertruck

c2｜據 Decrypt，馬斯克 11 月 6 日（週五）說，特斯拉會在 2027 年年中左右逐步停產德州超級工廠的 Cybertruck（DC7「around the middle of next year」，發文日 2026-11-06，所以是 2027 年；是大約時間）｜TSLA；DC7｜2026-11-08｜ct01；卡片 ct-what
c3｜「不鏽鋼皮卡」：DC7「The stainless-steel pickup」｜TSLA；DC7｜2026-11-08｜ct02
c4｜馬斯克回覆用戶：「True, but the Cybertruck fleet will be around for a long time.」（旁白「車隊還會存在很長一段時間」，卡片 'Around a long time' 是原話片段）｜TSLA；DC7｜2026-11-08｜ct04, ct06；卡片 ct-why
c5｜報導沒提停產後的零件和維修（TSLA「報導未提及停產後的售後服務或零件安排」；DC7 確實沒提）｜TSLA；DC7｜2026-11-08｜ct05
c6｜停產是為了騰出產能增產 Cybercab（DC7 引馬斯克「to make room for increased Cybercab production」）｜TSLA；DC7｜2026-11-08｜ct08；卡片 ct-cab kicker「Making room for」
c7｜Cybercab 是特斯拉的機器人計程車，雙座、沒有方向盤與踏板（DC7「a two-seater with no steering wheel or pedals」）；「機器人計程車」＝不需人類駕駛、由自動駕駛系統載客的計程車（TSLA 的解釋）｜TSLA；DC7｜2026-11-08｜ct09
c8｜Cybertruck 一直賣不好（DC7「has struggled to win buyers」）；據 Decrypt 引述 Electrek，銷量約為產線設計年產 25 萬輛的十分之一（旁白只說十分之一，25 萬不唸；卡片 kicker「Per Electrek, via Decrypt」）。旁白用「而且」接，不說成停產的原因：停產原因馬斯克說的是騰產能（c6），銷量是 Decrypt 補的背景｜TSLA；DC7｜2026-11-08｜ct12；卡片 ct-sales

### NYT Cooking

c9｜NYT Cooking App 最近加了內建 AI 助理，可依手邊食材改寫食譜（「改寫出你的版本」＝客製版本）；11 月 7 日是 The Verge 實測的發布日（VNY datePublished 2026-11-07T15:50Z），不是功能上線日：記者測了好幾天，VNY 的更新註記說功能是在說明頁上非正式宣布的。查核第 1 輪：ny01 拿掉日期（原「第二則在 11 月 7 日週六，……加了 AI 助理」讀成 11/7 上線），日期移到 ny06｜NYT；VNY｜2026-11-08｜ny01, ny02, ny06；卡片 ny-what
c10｜助理不改原食譜，另建新版本（VNY「it doesn't change the existing recipe; it leaves it as is and creates a new one for you」）｜NYT；VNY｜2026-11-08｜ny04
c11｜上線時僅 iOS 訂閱用戶（VNY「available to subscribers on iOS only at launch」；查核第 1 輪 ny05「目前只開放給」→「上線時只給……用」，照原文的 at launch）｜NYT；VNY｜2026-11-08｜ny05
c12｜記者手邊有雞柳、米、四季豆等（VNY 列 chicken tenders、ginger、garlic、rice、broth、limes、green beans、red onions；旁白只挑三樣），幾秒內生成新食譜、新標題（「Within seconds, it created a new version of the recipe, with a new title」）｜NYT；VNY｜2026-11-08｜ny06, ny07；卡片 ny-test
c13｜記者故意問能否把 trifle（分層甜點）的手指餅乾換成牛絞肉，助理說不行：「Minced beef cannot be used in place of the ladyfingers or anywhere in this sweet dessert trifle.」（旁白「甜點裡哪裡都不能放牛絞肉」）；「故意問」＝VNY「Then I threw in some curveballs」｜NYT；VNY｜2026-11-08｜ny08, ny09；卡片 ny-beef
c14｜新版本無法另外儲存（VNY「You can't save your new recipe separately」）｜NYT；VNY｜2026-11-08｜ny12
c15｜記者做原版蛋糕時問要多少奶油，助理給修改版的 6 大匙而非原版的四分之三杯，沒說用哪一版（VNY「when I was cooking the original … it gave me the modified recipe's 6 tablespoons rather than the original's three-quarter cup, without telling me which version it was using」；旁白不唸兩個量；查核第 1 輪 ny13 補「照原版」，沒有它聽不出為什麼給錯）｜NYT；VNY｜2026-11-08｜ny13；卡片 ny-fail
c16｜「6 tablespoons of butter would have made for a dry cake」（旁白「那個量真的照做，蛋糕會太乾」；蛋糕沒有真的做壞，查核第 1 輪卡片 ny-butter「a dry cake」→「almost a dry cake」，跟 key 一致）｜VNY｜2026-11-08｜ny15；卡片 ny-butter
c17｜記者說仍須複查用量與時間、對照原食譜（VNY「I still felt the need to double-check amounts and cooking times and cross-reference them with the original」）。「副廚，不是主廚」也是 The Verge 的評語：VNY「the NYT Cooking AI assistant works well as a sous chef, but it's not the head chef」（同一句接著講要複查用量）；撰稿時以為只出自站上文章，查核第 1 輪對回原文確認。卡片 ny-check kicker「The Verge's advice」→「The Verge's verdict」：副廚是評語，不是建議｜NYT；VNY｜2026-11-08｜ny16, ny17；卡片 ny-check

### 第三則（接主菜）

c18｜據 The Verge 11 月 8 日（週日）報導，兩組原告分別起訴 AI 音樂公司 Suno（SUV「Suno is facing yet another pair of lawsuits」，datePublished 2026-11-08T17:23Z；SUNO「據 The Verge 11 月 8 日報導」）。11/8 是報導日，不是起訴日（報導沒寫起訴日）：查核第 1 輪 su01「時間是 11 月 8 日週日」→「來自 The Verge 11 月 8 日週日的報導」，su02「據 The Verge，……」→「報導說，……」。卡片 su-lead「Elvis, Eminem / vs. Suno」→「Elvis, Eminem rights / holders vs. Suno」（原告不是本人，見 c61）｜SUNO；SUV｜2026-11-08｜su01, su02；卡片 su-lead
c19｜Kai 的問題（AI 聽歌學唱跟我們聽唱片學唱差在哪）在 outro 回答（c47）｜—｜—｜su05 → ou01

## Main Course

c20｜「想像一下，你打一行字……」是節目設定的觀眾情境，不是真人經歷；mc02「你輸入文字，它生成音樂和歌詞」：解釋。依據是 SUV 的「generates music and lyrics」與 Suno 發言人說的「prompts」（SUNO 把提示詞解釋成「使用者輸入給 AI、用來描述想生成內容的文字指令」）；來源沒有描述 Suno 產品怎麼操作，查核要確認這句沒有超出｜SUNO；SUV｜2026-11-08｜mc01, mc02；卡片 mc-scene
c21｜原告：一組 Elvis Presley 音樂的權利人（SUV「A group of rights holders of Elvis Presley's music」），一組 Eminem 部分最知名唱片的出版商（「the publisher of some of Eminem's biggest records」；旁白「幾張招牌唱片」）。旁白不說 Eminem 本人提告；「貓王」是 Elvis Presley 在台灣的通稱（解釋）｜SUNO；SUV｜2026-11-08｜su03；卡片 su-who
c22｜指控：Suno 違法生成模仿這些藝人的音樂與歌詞（「claiming it illegally generates music and lyrics that mimic those artists」）｜SUNO；SUV｜2026-11-08｜su04；卡片 su-claim
c23｜「提示詞」「權利人」的解釋照 SUNO（「擁有其音樂相關權利的一方」）；「不一定是歌手本人」是解釋｜SUNO｜2026-11-08｜mc03, mc04；卡片 mc-terms
c24｜兩人的立場是意見：Kai「AI 學音樂就跟人聽唱片學唱歌一樣」；Sola「歌是人家的，聲音也是人家的」；mc08「照原告的說法，Suno 沒有拿到授權」＝訴狀「without a license」（c28）。卡片 mc-sides 右欄「No license, per the suit」｜SUV｜2026-11-08｜mc05, mc06, mc07, mc08
c25｜Presley 案律師主張 Suno 違反田納西州的 ELVIS Act（旁白「美國田納西州」）｜SUNO；SUV｜2026-11-08｜mc09；卡片 mc-law
c26｜據 The Verge，ELVIS Act 讓 AI 公司複製歌手的聲音成為違法（「which makes it illegal for an AI company to clone a singer's voice」）。查核第 1 輪對了法案原文（TN HB2091，https://www.capitol.tn.gov/Bills/113/Bill/HB2091.pdf ，HTTP 200）：它管的是「未經授權」（without authorization／prior consent）使用一個人的聲音或肖像，以及散布主要用途是未經授權產生聲音的工具，追的是民事責任，不是把複製聲音一律禁止。旁白 mc10「這部法律規定，AI 公司複製歌手的聲音，是違法的」→「這部法律讓 AI 公司未經同意複製歌手的聲音，成為違法的事」（仍掛 The Verge）；卡片 mc-law2「AI cloning / a singer's voice」→「AI cloning a voice, / without consent」，key「No AI voice cloning」→「Clones need consent」｜SUNO；SUV；TN HB2091｜2026-11-08｜mc10；卡片 mc-law2、mc-tw2
c27｜法律全名 Ensuring Likeness Voice and Image Security Act，縮寫是 ELVIS（SUV 寫出全名與「(ELVIS) Act」；法案原文「Ensuring Likeness, Voice, and Image Security Act of 2024」）。Kai 問是不是照貓王的名字取的，Sola「報導沒這樣說，只說縮寫就是 ELVIS」：來源沒說命名由來。mc14（查核第 1 輪改寫）「不過一部縮寫拼成 ELVIS 的法律，現在真的被拿來替 Elvis 的歌打官司。」＝c25（Presley 權利人的訴訟援引 ELVIS Act），不說命名由來｜SUNO；SUV｜2026-11-08｜mc11, mc12, mc13, mc14；卡片 mc-acr、mc-acr2
c28｜Eminem 出版商一案的法律依據，報導未說明（SUNO 原文）｜SUNO；SUV｜2026-11-08｜mc15, mc16, mc62, so02；卡片 mc-em
c29｜訴狀：「Suno's ravenous race to the bottom aims to make human creativity obsolete, coldly replicating without a license in seconds what takes years to learn, struggle with, maintain, and endlessly attempt to make better and perfect.」旁白 mc20「人要花好幾年學習、磨練的東西，Suno 沒有授權，幾秒鐘就複製出來」；mc51「照訴狀的說法，Suno 想讓人類的創意變得過時」；卡片 mc-quote2 引中段、mc-lose 引「human creativity obsolete」（指控）｜SUNO；SUV｜2026-11-08｜mc19, mc20, mc51；卡片 mc-quote2、mc-lose
c30｜Suno 目前還面對 Sony、UMG、Isbell、Reservoir Media 等多起訴訟（SUV「the pile of lawsuits Suno is currently facing from Sony, UMG, Isbell, Reservoir Media, and more」；旁白「一疊官司」＝pile）；「大型音樂公司」是對 Sony、UMG 的解釋（來源只寫名字）｜SUNO；SUV｜2026-11-08｜mc24, mc25；卡片 mc-pile
c31｜這兩案與 Jason Isbell 等人 9 月提起的訴訟很像（「closely mirror」）；該案指稱 Suno 做出模仿原告的東西，但沒有直接主張著作權侵權（旁白「那一案說 Suno 模仿了原告」＝「claimed Suno created imitations of the plaintiffs」）。「歌手 Jason Isbell」：Isbell 是美國創作歌手，解釋。卡片 mc-isb「Imitation, / not copyright」→「Imitation, / not directly copyright」（原文「did not claim copyright infringement directly」，查核第 1 輪）｜SUNO；SUV｜2026-11-08｜mc28, mc29；卡片 mc-isb
c32｜「著作權，就是創作的人對自己作品的權利，像是誰可以拿去用、拿去賣」：解釋，不是法律定義；Kai mc31「所以那一案告的不是作品，是模仿了人？」只講 Isbell 那一案，跟 c31 一致｜—｜—｜mc30, mc31
c33｜mc32「照報導的寫法，這兩案告的重點，是 Suno 做出來的東西在模仿誰」＝c22（「generates music and lyrics that mimic those artists」）；mc33「學不是唯一的重點」是節目整理，故意不說這兩案沒告著作權（來源沒說）。Presley 訴狀也說 Suno 把藝人的身分「encoded itself」（c39，跟學有關），所以卡片 mc-turn「Not what it learned.」→「Not just learning.」（查核第 1 輪），跟 mc33 的「不是唯一的重點」一致｜SUNO；SUV｜2026-11-08｜mc32, mc33；卡片 mc-turn
c34｜「這要法院決定，現在都還只是原告的指控」：SUNO 的閱讀提醒「訴狀中的內容是原告一方的指控」；沒有判決｜SUNO｜2026-11-08｜mc35, mc66；卡片 mc-judge、mc-view2
c35｜Suno 發言人 Cat McCormack 對 The Verge 說，Suno 的目的是協助人們創作新的原創音樂，不是利用任何人的姓名或肖像（「not to trade on anyone's name or likeness」）；旁白不唸發言人的名字｜SUNO；SUV｜2026-11-08｜mc36, mc37；卡片 mc-suno
c36｜Suno 不允許以特定藝人姓名和歌曲作提示詞，並與第三方供應商合作篩查使用者上傳的音訊與歌詞是否可能遭濫用（自述；旁白「外部廠商」＝third-party providers）。mc38 原「她也說了」：來源沒寫發言人的性別，查核第 1 輪改成「發言人也說了」｜SUNO；SUV｜2026-11-08｜mc38, mc39, mc40, mc41；卡片 mc-guard
c37｜「擋不擋得住，報導裡沒有人實際測過」：SUV 只引述發言人，沒有測試｜SUV｜2026-11-08｜mc42
c38｜mc43「至少它自己也說，藝人的名字不能隨便用」＝發言人「not to trade on anyone's name」「we prohibit any unauthorized use of an artist's work」｜SUV｜2026-11-08｜mc43；卡片 mc-kai2b
c39｜訴狀：「Suno has mechanically encoded itself with artists' identities, hard-work, creativity, and time, and harnessed them all for a consistent conveyor belt of cold hard cash.」（指控；旁白 mc46「原告的說法是，錢流向了 Suno」、mc47、mc48；卡片 mc-quote1 只引最後一段）｜SUNO；SUV｜2026-11-08｜mc46, mc47, mc48；卡片 mc-quote1
c40｜要賠多少、Suno 賺了多少，報導都沒寫（SUV 與 SUNO 都沒有金額）｜SUNO；SUV｜2026-11-08｜mc50；卡片 mc-nonum
c41｜mc52「不會樂器的人也能做歌」是 Kai 的意見；mc53 是 Sola 的意見；mc54「照原告的說法，Suno 沒拿到授權，就拿別人的招牌去賺錢」＝c29「without a license」＋c39「artists' identities … cold hard cash」的白話（指控）｜SUV｜2026-11-08｜mc52, mc53, mc54
c42｜兩份來源（SUV、SUNO）都沒有提到台灣或亞洲；mc58 是節目的看法｜SUNO；SUV｜2026-11-08｜mc56, mc58；卡片 mc-tw
c43｜接下來看三件事：法院怎麼看 ELVIS Act（c26）、Eminem 案的法律依據（c28）、Suno 的防護有沒有外人能驗證（c37），是節目依來源整理的三點，沒有預測結果｜SUNO；SUV｜2026-11-08｜mc59, mc60, mc62, mc63；卡片 mc-next
c44｜「我的看法是」一段（mc64、mc65、mc66）是 Sola 的看法，不是來源的說法；mc67 是 Kai 改立場，回扣 mc05｜—｜—｜mc64, mc65, mc66, mc67

## AI Fail

c45｜據 TechCrunch 11 月 6 日，研究人員發現數百份 AI 駭客工具 Artex 暴露在公開網路上（TC6「hundreds of copies of a Chinese-made AI hacking tool publicly exposed」；旁白不說「中國開發」，免得名字和標籤太多）｜ART；TC6｜2026-11-08｜af02；卡片 af-news
c46｜Artex 是開源的自主滲透測試工具，會自動探測電腦系統弱點（「open source autonomous penetration testing tool, meaning software that automatically probes computer systems for weaknesses」）；「開源＝程式碼公開，誰都可以免費下載」是解釋（TC6「free for anyone to download」）｜ART；TC6｜2026-11-08｜af03, af04；卡片 af-what
c47｜7 月公開發布以後，已和多起網路攻擊有關（「linked to several cyberattacks since its public release in July」）｜ART；TC6｜2026-11-08｜af06；卡片 af-why
c48｜Microsoft 說，與中國國家立場一致的行為者（Storm-0940，旁白不唸代號）最早自 2026 年 9 月起用 Artex 自動化攻擊全球數百個組織。查核第 1 輪打開 MS1（2026-10-21，HTTP 200）：「As early as September 2026, Storm-0940, a China-state aligned actor, used the agentic AI penetration testing framework ARTEX to automate attacks targeting hundreds of organizations globally」，同文「the majority of the targeting wasn't successful」。旁白 af07「從 9 月起用它自動攻擊了全球數百個組織」→「最早從 9 月起，就用它自動攻擊全球數百個組織」（as early as；「攻擊了」讀成都已得手）；「國家背景一致」→「國家立場一致」（aligned）；卡片 af-ms「organizations hit」→「organizations targeted」，key「Hundreds of orgs hit」→「Hundreds targeted」（hit 讀成得手，原文是 targeting，且大多沒成功）；旁白「駭客組織」＝threat actor｜ART；MS1｜2026-11-08｜af07；卡片 af-ms
c49｜Censys 找到超過 800 個不同的 Artex 部署，可從網路存取，登入不需要密碼（「more than 800 distinct deployments of Artex that were accessible from the web without needing a password to log in」）；「資安公司」＝cybersecurity firm｜ART；TC6｜2026-11-08｜af08, af09；卡片 af-open
c50｜Censys 的 Silas Cutler 說，不是每一套都被惡意使用，很多是授權測試人員在用；軟體不需要對網路公開，為何數百套暴露仍不清楚（旁白「研究人員也說」，不唸名字）；「有授權的測試＝公司請人來試攻自己的系統，好先把洞補起來」是解釋｜ART；TC6｜2026-11-08｜af12, af13, af14；卡片 af-fair、af-test、af-why2
c51｜公開的系統也暴露了攻擊工具，例如植入程式（隱藏的惡意軟體），用來入侵受害者網路並長期維持存取（旁白「像藏在別人網路裡的惡意程式」，沒有講怎麼用）｜ART；TC6｜2026-11-08｜af15；卡片 af-kit
c52｜CrowdStrike 把 9 月針對韓國金融業的攻擊（原文 the attacks，複數；查核第 1 輪 af18 拿掉「一起」），歸因於一名使用 Artex 實例的講中文駭客，部分原因是該駭客留下了託管系統的「open directory」（旁白「一個用 Artex 的駭客」，不說語言；「把放系統的目錄，公開在網路上了」＝open directory）｜ART；TC6｜2026-11-08｜af17, af18, af19；卡片 af-kr、af-kr2
c53｜Censys 的資料顯示該實例已公開暴露數月，似乎還含有遠超出南韓銀行的攻擊資料（「appeared to contain more attack data that extended "well beyond South Korean banks"」；旁白保留「似乎」）｜ART；TC6｜2026-11-08｜af21；卡片 af-kr3
c54｜很多和 Artex 有關的攻擊利用簡單弱點，例如猜測弱密碼或已知密碼，以及缺乏多因素驗證；「多因素驗證」的解釋照 ART（「除了密碼之外，再用第二種方式確認身分」），「像手機上的驗證碼」是例子（解釋）｜ART；TC6｜2026-11-08｜af23, af24；卡片 af-lesson、af-mfa
c55｜af26「你要換的是密碼」：接 c54，是一般的帳號防護提醒，不是來源的建議；ART 也寫「基本的帳號防護仍然重要」｜ART｜2026-11-08｜af26；卡片 af-gag
c56｜Artex 宣布轉為閉源，後續版本實際上只給付費客戶；程式碼仍有數十份副本留在程式碼共享網站（旁白「幾十份」＝dozens）｜ART；TC6｜2026-11-08｜af27, af28；卡片 af-closed

## Sign-off

c57｜「今天最重要的是 Suno 的兩件新官司」「最不確定的是 Eminem 那一案的法律依據」是節目的看法；後者依 c28｜SUNO｜2026-11-08｜so01, so02
c58｜回扣：食譜助理不肯把牛絞肉放進甜點（c13）｜NYT；VNY｜2026-11-08｜so03
c59｜完整整理在 Mokaair，說明欄列四篇站上文章（四個網址 2026-11-08 皆 200）｜各站上文章｜2026-11-08｜so05
c60｜outro 答案 ou01「原告說，AI 跟人學歌，差在授權和速度。」（查核第 1 輪為了把 outro 壓到 12.5 秒以內，拿掉前面的問句，問題改寫進答案句裡）：依 c29（without a license；in seconds what takes years）｜SUNO；SUV｜2026-11-08｜ou01
c61｜縮圖「Ask **first**?」「Elvis, Eminem rights holders vs. Suno」；標題「Tech Signal 11/9｜Elvis, Eminem rights holders vs. Suno」：依 c21 與 Sola 的看法（c44）。原告是 Elvis 音樂的權利人與 Eminem 唱片的出版商，不是本人（SUV 標題「Elvis and Eminem rights holders are suing Suno」）；查核第 1 輪把標題、縮圖副標與卡片 su-lead 的「Elvis, Eminem vs. Suno」都加上 rights holders｜SUNO；SUV｜2026-11-08｜thumbnail, youtube.title

## 笑點（無事實主張）

給查核代理做笑點檢查：每個笑點前一行的事實、笑點本身、為什麼不算新的事實。沒有新的數字、沒有雙關與諧音、沒有替真人編的話、不打一般人。

- ct06（Sola）「『車隊還會存在很長一段時間』，這句話聽起來，很像分手時說的『我們還是朋友』。」：類比，接 ct04（c4）。前半是馬斯克原話的中譯；「我們還是朋友」是一般的分手說法，不掛在任何真人嘴上；笑的是馬斯克的回覆（有權力的人）。卡片 ct-ex kicker「Sola's analogy」，「'let's stay friends'」不是任何人說的話。查核第 1 輪：留；key「'Let's stay friends'」單獨出現在關鍵句帶時沒有 kicker，加引號會讀成馬斯克的原話，改成「Sounds like a breakup」。ct07（Kai）「好痛！」是反應。
- ct10（Sola）「所以 Cybertruck 是被一台連方向盤都沒有的車，搶走了工作。」：誇張，接 c6、c7；車沒有工作，一聽就是玩笑。ct11（Kai）「連車都會被自動化取代！」：誇張。卡片 key「Laid off by a robotaxi」。
- ct13（Kai）「十分之一？那條產線都在放假吧！」：誇張，接 ct12（c8）；不暗示產線真的停工，沒有新數字。
- ct14／af25（Kai）「所以我要不要換手機？」：固定梗（11/6 起），沒有事實主張。ct15「不用，這次被換掉的是一台皮卡」接 c2；af26「不用，你要換的是密碼」接 c54（見 c55）。
- ny03（Kai）「冰箱剩什麼，它就幫我湊一道菜？」：猜想，ny04「差不多」接 c9、c10。
- ny10（Sola）「這大概是今天整個 AI 產業，守得最成功的一道安全防線。」：誇張，接 ny09（c13）；不是任何人的評價（VNY 自己寫「Good call」）。ny11（Kai）「終於有 AI 敢對人類說不了！」：誇張。卡片 ny-joke「Today's best AI safety win」，kicker「Sola's take」。
- ny14（Kai）「所以蛋糕差點變成另一份食譜的蛋糕？」：想歪，ny15 用記者的話更正（c16）。
- mc12（Kai）「所以這部法律，是照貓王的名字取的？」：問句，mc13 明說報導沒這樣說。
- mc14（Sola）原「不過這個縮寫，取得比很多歌名都用心。」：查核第 1 輪改。「取得用心」暗示有人刻意拼出 ELVIS，正好是 mc13 剛說報導沒講的命名由來；「比很多歌名」順手打了寫歌的人。改成「不過一部縮寫拼成 ELVIS 的法律，現在真的被拿來替 Elvis 的歌打官司。」：情境的反差，事實照 c25、c27，不說命名由來，不是法律結論。卡片 mc-acr2「An acronym / with real effort」→「The ELVIS Act, / now for Elvis」，key「ELVIS Act, for Elvis」。
- mc16（Kai）「所以那一案，我們只知道告了，還不知道用什麼告。」：c28 的白話，不暗示原告隱瞞。
- mc21（Kai）「那模仿秀怎麼辦？模仿歌手的藝人，也要一起被告嗎？」：誇張的問句，沒有法律主張；mc22（Sola）「模仿秀的人，至少用的是自己的喉嚨。」：對比人與 AI，替模仿藝人說話，不是笑他們；不是法律結論。mc23（Kai）「好，這一分我先記在你那邊。」：反應。查核第 1 輪：留；卡片 mc-joke1b「Their own / throat」→「Their own / voice」（英文的 throat 讀起來像在講身體，key 本來就寫 own voice）。
- mc26（Kai）「一疊？」：反應；mc27（Sola）「對，Suno 的官司，已經可以出一張精選輯了。」：誇張，接 c30「pile」，沒有新的數字。卡片 mc-pile2「a greatest-hits album」。
- mc41（Kai）「你看，它有擋，連打歌手的名字都不行！」：Kai 的立場，事實照 mc39（c36，Suno 自述）；mc42 立刻說這是它自己說的。
- mc44（Kai）「一比一！」：計分梗（mc23 給 Sola 一分、mc43 給 Kai 一分），沒有事實主張。
- mc61（Kai）「第一件，我賭會有很多律師很忙。」：意見，不是預測的事實。
- mc68（Kai）「可是如果每首歌都要先問，AI 根本學不完吧？」：意見；mc69（Sola）「那就少學一點，人類歌手也沒有聽完全世界的唱片才出道。」：誇張的對比，沒有事實主張。
- af10（Sola）「一套專門找別人弱點的工具，自己連密碼都沒設。」：接 af08、af09（c49）。注意：暴露的部署不全是駭客的，很多是授權測試人員（c50），af12 緊接著講；笑的是「工具被設定成不用密碼」這件事，不說是誰設的。
- af11（Kai）原「這是小偷把萬能鑰匙，掛在自己家門口吧！」：查核第 1 輪改成「這是鎖匠把萬能鑰匙，掛在自己家門口吧！」。「小偷」把 800 多套的使用者都說成壞人，TC6 卻說很多是授權測試人員（c50，af12 才更正），等於暗示來源沒有的事、也打到正當的測試人員；鎖匠（替人開鎖、也可能被濫用的專業）對得上滲透測試工具，笑的仍是設定。af10 留。
- af16（Kai）「所以連武器庫都開放參觀？」：誇張，接 af15（c51）；沒有說明任何工具怎麼用。
- af20（Sola）「這就像小偷把作案行程表貼到網路上，還設成公開。」：類比，接 af19（c52「in part because」）；不說駭客因此被抓，只說歸因的部分原因。
- af22（Kai）「壞人也會忘記鎖門，我有點安心。」：反應。
- af29（Sola）「門現在才鎖，可是鑰匙早就被複製出去了。」：類比，接 af27、af28（c56）；「鑰匙」對的是程式碼副本，沒有新數字。af30（Kai）「這集的教訓，是先鎖自己家的門。」：收尾，接 c54。
- so03（Sola）「今天最有原則的 AI，是那個不肯把牛絞肉放進甜點的食譜助理。」：回扣 ny09（c13）。so04（Kai）「連食譜 AI 都懂得說不，我對 AI 又多了一點信心。」：反應。
- su06（Sola）「這題，主菜時我們吵給你聽。」：串場（跟 11/6 同一句，固定說法）。

## 我懷疑但沒動的事

- 「2027 年年中左右」：DC7 寫「next year」、發文 2026-11-06，換算成 2027；TSLA 標題也寫 2027 年中。
- ny-check 的 kicker：查核第 1 輪對回 VNY，副廚的比喻就是 The Verge 的評語（「works well as a sous chef, but it's not the head chef」），kicker 改成「The Verge's verdict」（見 c17）。
- 標題：查核第 1 輪改成「Elvis, Eminem rights holders vs. Suno」，縮圖副標與 su-lead 卡片一起改（見 c61）。
- mc02「你輸入文字，它生成音樂和歌詞」：來源沒有描述 Suno 怎麼用，是從「prompts」「generates music and lyrics」推的一般描述。查核第 1 輪：留。SUV 的發言人說「we do not allow prompts for specific artists' names and songs」（使用者用文字下提示）、原告說「generates music and lyrics」與「in seconds」，三點合起來就是這句；沒有說到任何操作細節。
- 「貓王」：Elvis Presley 在台灣的通稱；旁白第一次說「貓王 Elvis Presley」。
- c48 的 Microsoft 一句依站上文章的轉述，撰稿人沒有打開 MS1。查核第 1 輪打開了，改了措辭與卡片（見 c48）。

## 沒有放進來的

- Cybertruck 的 8,295 輛、年減 48%、25 萬輛、Cybercab 約 3 萬美元、9 月 3 日奧斯汀載客、45 輛、NHTSA、Wes Morrill 的話、特斯拉與 SpaceX 合併。
- NYT Cooking 的辣椒、瑪芬、五顆蛋減成三顆、Alexa Plus 比較、訓練資料包含用戶留言、聊天框關不掉。
- Suno 發言人的名字 Cat McCormack、Reservoir Media、Jason Isbell 案的其他原告。
- Artex 的「中國開發」、Storm-0940、ConnectWise 供應鏈事件、2,250 個租戶、3 小時、Microsoft 對受影響組織的建議清單、Silas Cutler 的名字、「從偵察到資料外洩」。

## 進度

- 第 1 稿（2026-11-08）：77 個場景、150 句；`lint` 0 錯誤、3 條警告（「11」說了 5 次：每則各自說日期，照編輯指示；開場章節長度：本節目沒有開場濃縮；投影片順序跟 daily-ai-20261106 有 86% 相同：同一節目的固定版型，主菜的立場卡改成 compare 稍微降低）；估 13.5 分鐘，最長畫面狀態 13.0 秒（outro），其次 12.9 秒（ny-why、mc-scene）。
- 句子完整性檢查 0 行；`key`／`keys` 全部 ≤24 字、`keys` 數量與畫面狀態一致；`big`、`quote`、`outro` 沒有 `reveal`。
- 新加的發音字典詞（null）：Act、Artex、Censys、Cooking、CrowdStrike、Cybercab、Cybertruck、ELVIS、Elvis、Eminem、Fail、Isbell、Jason、NYT、Presley、Sony、Suno、UMG。
- 查核第 1 輪（2026-11-08，`verify-1.md`）：改了 c9、c11、c15、c16、c17、c18、c26、c27、c31、c33、c36、c48、c52、c60、c61 與四個笑點（ct06 key、mc14、mc22 卡片、af11）；outro 13.0 → 12.3 秒；`lint` 0 錯誤、3 條警告（同第 1 稿），估 13.6 分鐘、150 句，最長畫面狀態 12.9 秒。
- 待做（第 1 輪之前寫的）：另派查核代理照 `prompts/verifier-video.md` 逐句對回原始來源並做笑點檢查；盲讀；Whisper 第二意見與試聽。
