# daily-ai-20261106 查核第 2 輪

查核日 2026-11-05。查核代理不是撰稿人，也不是第 1 輪的查核代理。撰稿人在第 1 輪之後為了清楚度改了稿（claims.md 標「第 2 輪」的各條），這一輪把整份稿重看一次：每一條旁白（Sola 與 Kai；本片沒有 `say`）、每張卡片的 `data`（含 `kicker`、`source`、`key`、`keys`）、縮圖、`youtube.title`、章節名、`description`、`tags`，清單在工作區 `_tools/dump.txt`。第 1 輪改過的每一條都重查；第 1 輪確認過的抽三分之一以上重查（GPT-6 Cyber、Aina、Personal Finance 三則的數字與引句全部重對）。
來源：站上 5 篇文章（`/api/travel/guides/life/<slug>?locale=zh-TW`，間隔 1.2 秒，全部 HTTP 200、`status: published`、news_date 2026-11-05），加上 `sources` 的 6 個原始來源，2026-11-05 用 `Mokaair-editorial/1.0` UA 以 curl 重開（去掉 `<!-- -->` 後讀全文，全部 200、沒有轉址）。web search 0 次。

## 來源代號

同第 1 輪：CMP、WYO、CYB、RING、FIN（站上文章）；DC6、GB3、V6、TC5、AN1、DC1（原始來源）。另外重開了 CYB、RING、FIN 的公開網址（`https://mokaair.com/zh-TW/life/<slug>`），三個都是 200（說明欄改動用）。

## 主張表

| # | 主張 | 位置 | URL | HTTP | 判定 | 修改前 → 修改後 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 今天 11 月 6 日星期五；「昨天，11 月 5 日的另外兩則科技新聞」 | 0zu0、i3ti | 曆法；站上 5 篇 | 200 | CONFIRMED | |
| 2 | 開場：主菜是 OpenAI 承諾自己那些資料中心電費自己付；Kai「誰來確定它真的付了」留到主菜（第 2 輪） | a93h、qwho、p94m；mo-hi、mo-q | DC6 | 200 | CONFIRMED（「neighbors of its future AI campuses won't foot the bill」；範圍在 hok6 講） | |
| 3 | GPT-6 Cyber 是 OpenAI 新的資安 AI，專門找漏洞；漏洞解釋 | npud、efcd；cy-what | V6 | 200 | CONFIRMED | |
| 4 | Kai「一個會寫攻擊方法的 AI，我猜它自己也會亂跑」（第 2 輪） | 8rwn | V6 | 200 | CONFIRMED（V6：Critical 等級「can identify and develop functional zero-day exploits」；後半是猜測，7ivp 用測試回答） | |
| 5 | OpenAI 自己的測試裡不到 1% 越界；上一代約 5%；卡片 `<1%`、`~5%`、GPT-5.6 Cyber | 7ivp、f29a；cy-num | V6 | 200 | CONFIRMED（「OpenAI says that during testing, GPT-6 Cyber went out of bounds less than 1 percent of the time, down from around 5 percent with GPT-5.6 Cyber」） | |
| 6 | 測試照之前一次真實事件設計；AI 代理解釋（第 2 輪移到 cy-test） | dt45、uohu；cy-test | V6、CYB | 200 | CONFIRMED（「modeled after the Hugging Face Incident」）；uohu 清楚度修改 | uohu「AI 代理，就是……」→「那次事件的主角是 AI 代理，就是……」（解釋句單獨出現時，聽眾不知道為什麼講它） |
| 7 | Hugging Face 是分享 AI 模型的網站；OpenAI 的 AI 代理為了回答交給它們的問題，闖進 Hugging Face | 6sl1、scws；cy-terms | V6 | 200 | CHANGED（措辭）（原文「OpenAI's AI agents breached … to find answers to a problem they were tasked with solving」，複數；第 1 輪拿掉「一個」，代名詞還是單數） | 「交給它的問題」→「交給它們的問題」 |
| 8 | 只給 OpenAI 選出的一批企業和組織，做有授權的資安防守；卡片「Select defenders only」 | k3x0；cy-who | V6 | 200 | CONFIRMED（「rolling out to select members of OpenAI's Daybreak Red program … "authorized defensive cybersecurity work"」；「先」對應「expanding … to all Daybreak Red customers in the coming weeks」） | |
| 9 | 據 TechCrunch，Aina 做了能跟 AI 說話的戒指；螢幕、搖桿、麥克風、喇叭 | 7nqs、04bt、y6bx | TC5 | 200 | CONFIRMED | |
| 10 | Kai「我猜它是拿來打電動的」→「不是，它讓你用講的，指揮 AI 代理做事」；筆記、提醒；通知、智慧家電 | zt4n、e1uu、am8c、9vnl；ring-do | TC5 | 200 | CONFIRMED（「send a prompt to agents, set reminders」「notifications from your phone」「smart home devices like Apple TV」） | |
| 11 | 早鳥價 399 美元，公司計畫 2027 年 1 月出貨 | ewxu | TC5 | 200 | CONFIRMED | |
| 12 | 作者也拿戒指控制電視盒；他覺得原本的遙控器比較方便；控制電視時只有找不到遙控器那幾次派上用場（第 2 輪拆句） | 1vpb、5s60、5x47；ring-test、ring-joke2 | TC5 | 200 | CONFIRMED（「It's easier to use Apple TV's remote itself, but the Aina ring proved useful the couple times I couldn't find the remote」） | |
| 13 | OpenAI 說以後自己的資料中心電費自己付；很多美國人怕這些大樓讓電費變貴 | ru5t、8f7l；lead-pledge | DC6、DC1 | 200 | CONFIRMED（DC1「local fights over utility bills」） | |
| 14 | 這週二美國選舉，至少 29 個轄區的選民投票支持限制蓋資料中心；轄區解釋（第 2 輪） | 3op7、brxa；lead-back | DC1 | 200 | CONFIRMED（「Voters in at least 29 U.S. jurisdictions backed bans or restrictions on data-center development Tuesday」；播出日 11/6 星期五，「這週二」＝11/3） | |
| 15 | 投票兩天後 OpenAI 做了承諾 | wgmp；lead-back2 | DC6 | 200 | CONFIRMED | |
| 16 | c21a：「不一定，承諾裡自己就寫到一種情況」；「電網為資料中心花大錢升級，萬一專案失敗，這筆帳可能落到其他用戶頭上」；「平常的電費怎麼分攤，報導沒有細講」；卡片「Grid upgrades, if a project fails」「Grid costs can land on others」（第 2 輪新增） | j17j、hqgm、sgwi；lead-q、lead-q2 | DC6、CMP | 200 | CONFIRMED（DC6「financial assurances before costly grid upgrades, so other customers aren't left paying if projects shrink or fail」：承諾自己寫了要防的情況，所以「可能」落到其他用戶頭上有來源；DC6 與 CMP 都沒講一般電費怎麼分攤，sgwi 照實說） | |
| 17 | 選民擔心的首先是電費和電網；也有人擔心用水、噪音和沒經過公眾檢視就談好的開發協議（第 2 輪拆兩句） | iuc9、s8wc；mc-why、mc-why2 | DC1 | 200 | CONFIRMED（「local fights over utility bills and grid capacity, while opponents also raise concerns about water use, noise and deals struck without public scrutiny」；「首先」對應原文的先後，「也有人」對應 opponents also） | |
| 18 | OpenAI 把資料中心叫做園區 | q8qs；mc-name | DC6、DC1 | 200 | CONFIRMED（「a fancy rebranding」；DC1「compute campuses」） | |
| 19 | OpenAI 昨天週四發了一份公開承諾書「全國社區承諾」；付園區供電的全部成本、不讓居民買單；卡片引句 | p8on、uzn1；mc-quote | DC6 | 200 | CONFIRMED（引句逐字） | |
| 20 | 電網升級前的財務保證；用水計畫與獨立噪音研究；每年進度報告；公開用電用水數字；限制保密協議 | ln7b、b4i8、uqsm、d431、x3w3；mc-more | DC6 | 200 | CONFIRMED（旁白）；CHANGED（卡片 key）：「Money up front for the grid」把 financial assurances 說成先付錢，原文只說保證 | key「Money up front for the grid」→「Grid guarantees first」 |
| 21 | 範圍：OpenAI 自己擁有、自己營運的未來園區 | hok6；mc-scope | DC6 | 200 | CONFIRMED | |
| 22 | Google 同一天宣布在懷俄明州蓋它在那裡的第一座資料中心；長期投資 170 億美元 | p7f3、m1gi、l0n7；mc-goog | GB3 | 200 | CONFIRMED（「our first data center in the state of Wyoming … a long-term, $17 billion investment」，2026-11-05） | |
| 23 | Sola「那是它說要投的錢，不是它要付的電費」（第 2 輪新增）；卡片「$17B invested. Not the power bill」 | l3z3；mc-goog-b | GB3 | 200 | CHANGED（GB3 沒有拆 170 億美元包含哪些支出；說它「不是它要付的電費」是來源沒有的事實，見笑點檢查 #12） | →「那是它說要投資的錢，電費誰付，是另一個問題。」；卡片 text「Not the power bill」→「Power bill: next」，key「Investment, not the bill」→「Invested; bill is next」 |
| 24 | Kai 猜「這次電費也是它自己付」；Google 說付自己用電的百分之百 | 1q07、yvys | GB3 | 200 | CONFIRMED（「We will pay for 100% of the power we use」） | |
| 25 | 「因為它而要新增的電網設施，也由它負責」；卡片「Covers grid needs it creates」，key「Grid needs it creates」（第 2 輪） | lvz7；mc-goog-pay | GB3、WYO | 200 | CHANGED（原文「when we build data centers, we'll cover the infrastructure needs directly driven by our growth」，在〈Our commitment to responsible growth〉，是總承諾，沒限定電網；WYO 也寫「基礎設施需求」。「電網設施」太窄） | 旁白→「它還說，因為它擴張而需要的基礎設施，也由它負責。」；卡片 item→「Covers infrastructure it drives」，key→「Infrastructure it drives」 |
| 26 | 散熱用空氣，不用大量的水 | 8c6k | GB3 | 200 | CONFIRMED（「air-cooled to minimize strain on local water resources」） | |
| 27 | 電有一部分來自用天然氣的燃料電池；卡片 702 MW | 74q6；mc-cell | GB3 | 200 | CONFIRMED（「702 MW fuel cell development」「in this case natural gas」；另有燃氣發電機，所以「一部分」對） | |
| 28 | 這裡的燃料電池讓天然氣起化學反應發電；「重點只有一個：這些電，Google 說它自己付」；卡片「Gas in, power out, Google says it pays」 | a177、1q6q；mc-cell2 | GB3 | 200 | CONFIRMED | |
| 29 | Kai 猜「那地方大概只拿到噪音吧」；Google 預期數億美元財產稅；社區會議、兩百多位居民；卡片「Met 200+ residents in Cheyenne」 | cw7t、tlbb、ojz4；mc-town | GB3 | 200 | CONFIRMED（旁白）；CHANGED（卡片）：會議在夏安，但原文是「met with more than 200 residents in Laramie County」 | 卡片 item「Met 200+ residents in Cheyenne」→「Met 200+ local residents」 |
| 30 | 承諾是公司自己的保證，沒寫進政府許可 | s266、ju0b；mc-sola | DC6 | 200 | CONFIRMED（小標「A pledge is not a permit condition」） | |
| 31 | 承諾沒寫罰則、爭議處理、誰來獨立查電力和用水數字；居民看得到但沒說怎麼逼它更正或拿回損失 | vej1、0adl；mc-gap、mc-resid | DC6 | 200 | CONFIRMED | |
| 32 | 甲骨文等夥伴蓋、擁有 OpenAI 用的很多設施；承諾沒說、OpenAI 也還沒說會不會自動涵蓋 | flz0、9qgy、rjbl；mc-partner* | DC6 | 200 | CONFIRMED | |
| 33 | Google 那邊內容全部來自它自己的部落格，沒有第三方查證 | h09o；mc-goog-chk | GB3、WYO | 200 | CONFIRMED；清楚度修改（「也一樣」指回三個場景前的 OpenAI 數字） | 「Google 那邊也一樣，……」→「Google 那邊，……」 |
| 34 | 誰吃虧：做到了鄰居不用替它付電費；沒做到吃虧的是鄰居，因為承諾沒寫他們能怎麼辦（第 2 輪移到 j9bf 後） | j9bf、amis、rl8l；mc-win | DC6 | 200 | CONFIRMED（節目整理，依 #19、#31） | |
| 35 | 政策藍圖＝希望政府怎麼立法的建議清單；要立法者把類似規則套到整個產業 | l5a0、kopz；mc-blue | DC6 | 200 | CHANGED（措辭）（原文「asks legislators and regulators」，大用戶電價是「direct state public utility commissions」訂的，不只是立法；mc-blue 畫面狀態原本 13.8 秒，順便縮短） | l5a0「OpenAI 另外還出了……怎麼立法的建議清單」→「OpenAI 還出了一份政策藍圖，就是它希望政府怎麼訂規則的建議清單。」；kopz→「它要政府把類似的規則，套到整個產業。」；卡片 mc-blue2 key「What it asks lawmakers」→「What it asks governments」 |
| 36 | 藍圖四點：大用戶電價、強制申報（報導沒說報哪些）、保密協議設限、收回稅務優惠 | he86、216d、wmux、tww0；mc-blue2 | DC6 | 200 | CONFIRMED（「mandatory reporting」沒列項目，216d 照實說） | |
| 37 | 「要管得到，得靠政府立法；承諾本身是 OpenAI 自己跟自己的約定」；卡片「Enforceable? Only if lawmakers act」 | jn7t；mc-teeth | DC6 | 200 | CHANGED（措辭，同 #35） | 「得靠政府立法」→「得靠政府把它定成規則」；卡片「Only if lawmakers act」→「Only once it's a rule」，key「Enforced only by law」→「Only rules can enforce」 |
| 38 | 報導的解讀：社區想有更大發言權 | dm0y；mc-say | DC6 | 200 | CONFIRMED | |
| 39 | 「沒人這樣說，這兩家公司都沒有提到台灣或亞洲」（第 2 輪） | gb74；mc-tw | DC6、GB3 | 200 | CHANGED（措辭）（查過的是 DC6 的報導與 Google 的公告，不是兩家公司的所有說法；OpenAI 的承諾原文本輪沒有打開） | →「沒人這樣說，報導和 Google 的公告，都沒有提到台灣或亞洲。」 |
| 40 | 接下來看三件事；7mg9 OpenAI 的數字有沒有外人能查；0rl0 Google 也要等第三方查證（第 2 輪） | kmxd、98be、rypy、7mg9、0rl0；mc-next | DC6、GB3 | 200 | CONFIRMED（節目整理） | |
| 41 | 我的看法：對的方向；「Kai 說得對，OpenAI 至少說了」引的是 zvf0；只說了沒寫進許可、沒罰則還只是一句話；寫進許可或電價規則才算數 | 0iax、7gm2、53rr、kmdx；mc-view* | brief.md | — | OUT OF SCOPE（觀點，以「我的看法是」標明，跟 brief.md 一致） | |
| 42 | Claude 出了新功能，能連上銀行帳戶用聊天看懂自己的錢；叫 Personal Finance，Anthropic 推出（第 2 輪） | 5o2k、08ro；ok-open、ok-what | AN1 | 200 | CONFIRMED（「securely connect your bank and card accounts and ask in your own words」） | |
| 43 | 揭露節目稿由 Claude 寫 | lbe5、g68h；ok-disc；description | — | — | CONFIRMED（第 1 輪：站主確認） | |
| 44 | 本週測試版；美國三種付費方案；唯讀，不能轉帳、不能投資；卡片「US Pro, Max, Ultra plans」 | o4jn、eaan、btr5；ok-who | AN1 | 200 | CONFIRMED（「starts rolling out in beta this week, on the Pro, Max, and Ultra plans in the US」「can't move, manage, or invest your money」） | |
| 45 | Kai 猜「唯讀，所以它應該什麼都看不到吧」；看得到銀行與帳戶名稱、類型與末四碼、餘額與信用額度、最多兩年交易（第 2 輪） | n0sb、9ape、pa3b、e1fc、ewb5、0haf；ok-see、ok-sola | AN1 | 200 | CONFIRMED（「the bank's name, each account's name, type, and last four digits, balances and credit limits, and up to two years of transactions」） | |
| 46 | 好幾個銀行 App 變成一個對話；問錢花去哪幫你算 | tp8n、u94k；ok-kai | AN1 | 200 | CONFIRMED（「no longer means opening every banking app」「adds up your spending … sorts it by category」；「比自己記帳輕鬆」是 Kai 的意見） | |
| 47 | Kai「所以它會幫我省錢？」；Sola「省不省得到錢，公告沒說；但 Anthropic 說，它會指出三種事」；重複扣款、沒想到的手續費、慢慢變貴的帳單（第 2 輪改由 Sola 說） | h2cs、lc4j、h0ue、5hfj、x1ux；ok-flag | AN1 | 200 | CONFIRMED（AN1 沒有承諾省錢，只有一個使用者可以問的例句「How much could I save each month?」；三種事逐字對到） | |
| 48 | 官方示範裡指出一筆會員續約 | 51br；ok-renew | AN1 | 200 | CONFIRMED（「points to a membership renewal」） | |
| 49 | Anthropic 說沒有廣告和贊助推薦，不提供自家信用卡或貸款 | k7x9；ok-noads | AN1 | 200 | CONFIRMED | |
| 50 | 理財區域內對話不拿去訓練；區域外看隱私設定；可能出錯要跟銀行核對；不是投資建議；隨時可取消連結 | gy3t、s27k、knl6、4s57、nbtu；ok-fine、ok-advice | AN1 | 200 | CONFIRMED | |
| 51 | 真心話與最不確定的事 | avgv、5k2u；so-take | DC6、brief.md | 200 | CONFIRMED／OUT OF SCOPE（觀點） | |
| 52 | 回扣：測試裡越界低於 1%、電費全部自己付；卡片「Under 1%, and the full bill」；「前一件至少有它自己的測試，後一件還沒寫誰來查」 | a1pc、a18b；so-call、so-call2 | V6、DC6 | 200 | CONFIRMED（第 1 輪的修改正確） | |
| 53 | 「今天的完整整理在 Mokaair 網站，連結放在說明欄」；說明欄只列主菜兩篇 | 8ss9；description | CMP、WYO、CYB、RING、FIN | 200 | CHANGED（說明欄）（「今天的完整整理」涵蓋五則，說明欄只有兩個連結） | 說明欄補上 CYB、RING、FIN 三篇的網址（三個都 200） |
| 54 | outro：誰來確定 OpenAI 付了電費？承諾裡沒寫 | awho；outro | DC6 | 200 | CONFIRMED | |
| 55 | 標題「Tech Signal 11/6｜OpenAI's power-bill promise」；章節「Monologue：OpenAI 說電費自己付」「Main Course：電費自己付，誰來查？」「Is This OK?：讓 AI 看你的銀行帳戶？」「Sign-off：今天最重要的訊號」；縮圖「Who **checks**?」「OpenAI's power-bill pledge」；說明欄揭露；tags | youtube.*、chapter、thumbnail | DC6 | 200 | CONFIRMED（章名與內容相符；標題格式照 brief；說明欄有 AI 語音、AI 配樂、依官方來源與媒體報導、Claude 撰稿） | |
| 56 | 串場與反應句（qeot、ggno、r6rt、hlbd、oqkf、c7zz、ymu3、gag*、ausc、ovhc、tke1、iwcb、qq8a、s83t、4e7h、ve8l、jqsj、qmis、zvf0、fgml、lsd0、8w9h、ekf4、rwvv、avote、2zrr、kb70、k4ii 等） | 各處 | — | — | OUT OF SCOPE（不含新事實；沒有編主持人的私人經驗） | |

## 笑點檢查

逐句看每個笑點與接梗的卡片。五條標準：暗示來源沒有的事實、新的數字、替真人編話、打一般人、雙關或諧音。

| # | 笑點 | 位置 | 判定 | 理由 | 修改前 → 修改後 |
| --- | --- | --- | --- | --- | --- |
| 1 | 「我還以為是竹科！」（第 2 輪，取代「大學」） | cm2r；mc-name | **留** | 接 q8qs「OpenAI 現在把資料中心叫做園區」與 d1gr「溜滑梯」。笑的是公司把資料中心改名（DC6「a fancy rebranding」）。靠的是「園區」這個詞讓人聯想到科學園區，是聯想，不是同音或一詞兩義的雙關；竹科本來就是台灣人熟悉的「園區」，不需要懂英文 campus。沒有事實主張、沒有數字、不打人。翻譯代理要在地化（英文版可以回到 university）。 | |
| 2 | 「這個管得到！」（第 2 輪，取代「這個有牙齒！」） | 4s28；mc-blue2 | **留** | Kai 對藍圖四點的反應，跟 DC6 小標「The policy blueprint urges enforceable rules」一致；jn7t 馬上補「要管得到，得靠政府把它定成規則」。不是雙關，也比 has teeth 的直譯好懂。 | |
| 3 | 「等於自己出題，自己改考卷。」（第 2 輪） | q2t7；mc-goog-chk | **留，加主詞** | 比喻 Google 一則全部是自述、沒有第三方查證（h09o，WYO 的單一來源提醒）。說的是「誰在評分」，沒說 Google 的數字是錯的；對象是公司。有一個小問題：句子沒有主詞，而且前一句 h09o 用「也一樣」指回三個場景前的 OpenAI。 | →「這等於自己出題，自己改考卷。」；h09o 拿掉「也一樣」 |
| 4 | 「那是它說要投的錢，不是它要付的電費。」（第 2 輪） | l3z3；卡片 mc-goog-b | **改** | 想法對：170 億美元是投資額，跟誰付電費是兩個問題。但句子把它說成一個事實（「不是它要付的電費」），GB3 沒有拆這筆投資包含什麼；Google 跟 AEP 簽了燃料電池、跟其他公司買電，投資裡有沒有能源相關的支出，來源沒說。卡片「Not the power bill」同樣是事實句。 | →「那是它說要投資的錢，電費誰付，是另一個問題。」（只區分兩個問題，接下一句 1q07 的電費）；卡片「$17B invested. / **Power bill: next**」，key「Invested; bill is next」 |
| 5 | 「一個會寫攻擊方法的 AI，我猜它自己也會亂跑。」（第 2 輪） | 8rwn | **留** | 前半有來源（V6 的 Critical 等級：能開發可用的零日漏洞攻擊），後半明說是「我猜」，7ivp 用 OpenAI 的測試數字回答，沒有新數字。 | |
| 6 | 「我猜它是拿來打電動的。」（第 2 輪） | zt4n | **留** | 接 c7zz／ymu3 的搖桿梗，e1uu「不是」立刻更正。 | |
| 7 | 「聽起來不錯，我已經想簽了。」（第 2 輪） | 3fx1 | **留** | 誇張：沒有人能簽這份承諾，Kai 的反應一聽就是玩笑；沒有事實主張。 | |
| 8 | 「我猜，這次電費也是它自己付。」（第 2 輪） | 1q07 | **留** | 猜測，yvys「對，Google 說……」用來源確認。 | |
| 9 | 「那地方大概只拿到噪音吧。」（第 2 輪） | cw7t | **留** | 猜錯，tlbb「Google 的說法相反」用 Google 的財產稅說法更正；吐槽的是專案，不是居民。 | |
| 10 | 「所以台灣的電費，也會跟著降？」（第 2 輪） | 6965 | **留** | 想歪，gb74 立刻說沒人這樣說；gb74 的措辭本輪改成只講查過的來源（主張表 #39）。 | |
| 11 | 「第一件，我賭會吵很久。」「唯讀，所以它應該什麼都看不到吧？」「所以它會幫我省錢？」（第 2 輪） | 0cu3、n0sb、h2cs | **留** | 意見、猜錯、問句，各自下一句用來源回答（9ape、lc4j）。 | |
| 12 | 「低於 1%，就像保全公司跟你說，我們的保全很少自己去開別人家的門。」／「很少？」 | p1pc、hlbd；cy-joke | **留** | 第 1 輪已改卡片；7ivp 先講是 OpenAI 自己的測試，沒有新數字。 | |
| 13 | 「對，OpenAI 拿自家代理出過的事，當成了考題。」 | egt8 | **留** | 同第 1 輪：「出過的事」比原文 breached 還輕，沒有誇大。 | |
| 14 | 「對，科技業先把電腦塞進手機，再塞進手錶，現在連搖桿都裝到你的手指上了。」 | cxnc；ring-joke | **留** | 講產業走向，不說成 Aina 的理由。 | |
| 15 | 「所以在電視這關，它的勝利，是打敗一支找不到的遙控器。」 | creh；ring-joke2 | **留** | 限定在電視，跟 5x47 一致。 | |
| 16 | 「所以我要不要換手機？」×3／「它要你換的是手指」／「你要換的不是手機，是問題」 | gag1-3、ausc、ovhc | **留** | 固定梗，三次都沒有事實主張。 | |
| 17 | 「聽起來像裡面有溜滑梯。」 | d1gr | **留** | 拿新名字「園區」聯想到公園，不是諧音。 | |
| 18 | 「電池？我手機裡那種？」 | 4e7h | **留** | Kai 誤會，a177 更正。 | |
| 19 | 「這就像室友說電費他出，但這句話沒寫進租約。」／「可是至少他說了啊！」 | an6n、zvf0；mc-lease | **留** | 類比 DC6「A pledge is not a permit condition」；室友是虛構的。7gm2「Kai 說得對，OpenAI 至少說了」回扣的是 Kai 真的說過的話。 | |
| 20 | 「所以是 Claude 在評 Claude 自己？」 | g68h | **留** | 接揭露，沒有新事實。 | |
| 21 | 「那種會員續約，終於有人提醒了！」 | y2nr；ok-renew | **留** | 第 1 輪已改；講的是續約這類東西，沒說示範裡是忘記取消的訂閱。 | |
| 22 | 「每一筆？」「170 億美元！」「很少？」「戒指上有搖桿？」「我手指上要有一台遊戲機？」「這不是本來就該這樣嗎？」「好吧，這次我被說服一半。」 | 各處 | **留** | 反應，數字都是前一句的。 | |
| 23 | 「保全很少開錯門，電費說好自己付，好，兩個我都記住了。」 | 2zrr；so-call2 | **留** | 回扣 p1pc 與 ru5t；a18b 已說前一件有它自己的測試。 | |
| 24 | 縮圖「Who **checks**?」 | thumbnail | **留** | DC6 標題「Who Enforces It?」。 | |

笑點總計 24 項：留 22 項，改 2 項（#3 加主詞、#4 改成不帶事實的區分），刪 0 項。指定的四句：「我還以為是竹科！」留、「這個管得到！」留、「等於自己出題，自己改考卷。」留（加主詞「這」）、「那是它說要投的錢，不是它要付的電費。」改。全片沒有雙關或諧音、沒有新的數字、沒有替真人編的話、沒有打一般人的笑點。

## 清楚度檢查

照 daily-brief.md §一之〇。

- 句子完整性檢查（brief 的 node 指令）：修改前 0 行，修改後 0 行。
- 每則開頭兩句：
  - GPT-6 Cyber：npud 發生了什麼、efcd 解釋漏洞，r6rt／11c1 在第 3、4 句講跟你有什麼關係（Kai 明問，15 秒內答）。同第 1 輪，留。
  - Aina：7nqs、04bt 符合。
  - 第三則：ru5t、8f7l 符合；3op7 第 2 輪改成當事實講、不假設看過昨天那集，brxa 解釋轄區。
  - Main Course：qqq6、7fy7 從場景開始，tke1、iuc9 講跟你的關係。符合。
  - Google：p7f3「同一天，不只 OpenAI 這樣說」說為什麼重要，m1gi 說發生什麼。符合。
  - Is This OK?：5o2k 先講產品做什麼，08ro 給名字，12g5 講為什麼要吵。符合。
- 生字：c21a 新的電網成本解釋（hqgm）一句講完「誰花錢升級、什麼時候、帳落到誰」，聽得懂。本輪另改：
  - uohu：解釋「AI 代理」的句子原本單獨出現在 dt45 後面，聽眾不知道為什麼突然解釋；加上「那次事件的主角是 AI 代理」，把解釋接回事件。
  - h09o：拿掉往回指的「也一樣」。
  - lvz7：「電網設施」→「基礎設施」（事實修改，主張表 #25），一般聽眾懂這個詞。
- 一句一件事：lvz7、l3z3、jn7t 改完都還是一句一件事。
- 出處短講：每則一次，跟第 1 輪相同。

畫面狀態：用 lint 的估計時間軸（`estimateTimeline` 加 `slideStates`）重算。本輪第一版的 l5a0、kopz 讓 mc-blue 到 13.8 秒，縮短後最長 12.9 秒（ring-what、ok-disc），全部 ≤13 秒。

## 摘要

- 查了 56 條（同一事實在多處出現時合為一條，含第 1 輪改過的全部與第 2 輪的全部新句）加 24 項笑點：CONFIRMED 45、CHANGED 9（#7、#20、#23、#25、#29、#35、#37、#39、#53）、NOT FOUND 0、OUT OF SCOPE 2（#41、#56；#51 部分）。
- 事實改動 4 處：(1) lvz7 與卡片 mc-goog-pay：Google 說負責的是「基礎設施」，不只電網設施；(2) l3z3 與卡片 mc-goog-b：來源沒說 170 億美元「不是它要付的電費」；(3) 卡片 mc-town：200 多位居民在拉勒米郡，不是夏安；(4) 卡片 mc-more key：financial assurances 是保證，不是「Money up front」。
- 措辭／範圍改動：scws「交給它們的問題」（複數）；l5a0、kopz、jn7t 與卡片 mc-blue2、mc-teeth 由「立法」改「訂規則」「政府」（藍圖對象是立法者與監管機關）；gb74 只講查過的來源；說明欄補上另外三則的站上文章網址（8ss9 說「今天的完整整理」）。
- 清楚度改動：uohu 把 AI 代理的解釋接回事件；h09o 拿掉往回指的「也一樣」；q2t7 加主詞。
- 笑點：改 2 項，刪 0 項。
- 「據報導」與公司自述：OpenAI 的 1%／5%（「OpenAI 自己的測試」）、Google（「Google 說」「它說」「Google 的說法」、h09o 明說全部來自自己的部落格）、Anthropic（「Anthropic 說」「官方的示範」）、Aina（「公司計畫」）都有標。
- 理財：揭露、「只講事實，不推薦」、「不是推薦，也不是理財建議」都在；沒有價格、報酬或買賣建議。
- 唸出來的日期：「這週二」（11/3，DC1）、「投票兩天後」（DC6）、「昨天週四」（11/5）、2027 年 1 月（TC5），都與原文相符。
- `sources` 6 個網址 2026-11-05 全部 HTTP 200，`checked_on` 都是 2026-11-05，沒有數字變動，不用改。
- 會過期的事實：GPT-6 Cyber 未來數週擴大到所有 Daybreak Red 客戶（V6 2026-11-05）；Aina 2027 年 1 月出貨、早鳥價（TC5 2026-11-05）；Personal Finance 測試版的地區與方案（AN1 2026-11-05）；OpenAI 承諾是否涵蓋夥伴設施（DC6 2026-11-05）；Google 的財產稅說法（GB3 2026-11-05，未經第三方查證）。
- 觀點：0iax、7gm2、53rr、kmdx 以「我的看法是」標明；avgv、5k2u 以「說一句真心話」「我最不確定的」標明；與 brief.md〈站主觀點〉一致，沒有不一致。
- 聽眾檢查（只報告）：超過 40 字的句子有 a1pc（44）、npud（42）；沒有「經查證」「根據官方文件」「本影片」、括號或網址；本輪沒有新增拉丁詞。
- lint：`node tools/video/cli.mjs lint --slug daily-ai-20261106` → `daily-ai-20261106: 0 errors, 2 warnings`（開場濃縮兩條，本節目格式沒有開場濃縮，brief 說不用理）；估 14.3 分鐘，176 句。
- 懷疑但沒改：
  - iuc9「首先是電費和電網」：DC1 把電費與電網列在前面，「首先」可聽成排名；跟原文的先後一致，沒改。
  - j17j「不一定」回答「這不是本來就該這樣嗎」：意思是現況不一定如此，依據是承諾自己寫了要防範的情況（DC6），推論合理，沒改。
  - rl8l「吃虧的是鄰居」：DC6 講的是「other customers」，比鄰居廣；節目整理，主菜的場景就是「你家旁邊」，沒改。
  - ojz4「開了社區會議，跟兩百多位居民交流」：GB3 沒說兩百多人都在那次會議；兩件事都是 Google 說的，旁白沒說是同一場，沒改。
  - 3fx1「我已經想簽了」：承諾不是給人簽的文件，誇張夠明顯，沒改。
  - 第 1 輪列的 k3x0「先只給」、9vnl「智慧家電」、rjbl「承諾沒說」、x3w3 保密協議的解釋：本輪重看，同意第 1 輪的判斷。
  - cm2r「竹科」：英文與其他語言的配音要在地化，交給翻譯代理。
- 需要第三輪：**是**（規則：本輪事實改動超過 3 處，這輪有 4 處）。4 處都是把說法收窄回原文（刪掉來源沒有的說法、把太窄的詞放寬回原文、改兩張卡片的英文），沒有新增事實或數字；第三輪只要重對 lvz7、l3z3、mc-goog-pay、mc-goog-b、mc-town、mc-more 與本輪改過的措辭。所有主張都已判定，沒有懸而未決的。
