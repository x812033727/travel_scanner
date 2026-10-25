#!/usr/bin/env python3
"""Author source builder. No provider, backend, runtime state or approvals are written."""
import copy, hashlib, json, re
from pathlib import Path
DEST=Path(__file__).resolve().parent
ROOT=DEST.parents[3]
OLD=ROOT/'docs/videos/story-everyday-moleskine-c03'
source=json.loads((OLD/'video.json').read_text())
old_by={s['id']:s for s in source['scenes']}
SLUG='story-everyday-moleskine-c03-remake-20261025'
chapters=['一本空白本被股市標價','舊式本子被出版社重新生產','空白頁走進書店與股市','貨架背後多了一箱要安排的貨','新主人接下門市與產品的考驗','補貨回來了，名字仍要接受檢驗']
# S1a etc. are precise source anchors, not verdicts. Publication-era scope is explicit.
anchors={
'S1a':{'source':'S1','locator':'PDF 123／印刷121；PDF139／印刷137，舊式型制、1995重新生產','scope':'發行人回顧，不證法國原工坊直接傳承'},
'S1b':{'source':'S1','locator':'§11.2，PDF260／印刷258，Il primo deposito…26 novembre 1997','scope':'首次商標申請，不能寫當日完成核准'},
'S1c':{'source':'S1','locator':'PDF139–140／印刷137–138，libro ancora da scrivere；prioritariamente…librerie','scope':'公司定位、目標客群與書店策略，非全體買家動機'},
'S1d':{'source':'S1','locator':'PDF140／印刷138，新管理層投入communication/brand management/merchandising','scope':'2006收購後策略，非獨立效果測試'},
'S1e':{'source':'S1','locator':'PDF159–160／印刷157–158，Sviluppo e controllo dei fornitori','scope':'2013招股書所述委外、流程品質與滾動12月需求規劃，不推現在製造地'},
'S1f':{'source':'S1','locator':'§6.1.3.5，PDF165／印刷163，直間接通路synergy','scope':'發行人策略與自述效益，非已證唯一成長原因'},
'S1g':{'source':'S1','locator':'PDF166／印刷164，consignment/non-consignment貨權與風險；向零售商售出後提貨','scope':'2013招股書當時一般契約，非消費者結帳，非2025特定客戶合約'},
'S1h':{'source':'S1','locator':'PDF167／印刷165，non-consignment出貨或交付；月度向零售商銷售資料與庫存','scope':'2013當時契約，配送商到零售商的Sell-In，非終端消費者Sell-Out'},
'S2':{'source':'S2','locator':'Our Heritage，A Creative History','scope':'品牌轉述查特文及1986停產故事；非同期工廠檔案'},
'S3':{'source':'S3','locator':'Code of Ethics §1 Purpose and Scope','scope':'歷史人物使用舊類型；2007-01-01公司名稱，不能說使用現代品牌'},
'S5':{'source':'S1','locator':'PDF123–124／印刷121–122，2006收購及法人重整','scope':'非1997品牌初創，非2016交易'},
'S6a':{'source':'S6','locator':'2017投資人日投影片11、15–16，批發doors','scope':'約1.2萬/2萬是批發據點，非自營店、非全書店'},
'S6b':{'source':'S6B','locator':'2016 Activity Report印刷35、37；2017 Annual Report財務印刷7／PDF65','scope':'2016年底79直營店；保留投資簡報78衝突'},
'S7':{'source':'S7','locator':'2013-04-03上市新聞稿，STAR；market capitalisation €487.6m','scope':'上市時整家公司市值，不是銷售收入或募入現金'},
'S8a':{'source':'S8','locator':'2016-09-22公告PDF1，41%/€2.40/€506m equity value','scope':'簽約及計畫，不是已全數收購；估值不是公司現金收入'},
'S8b':{'source':'S8','locator':'2016-09-22公告PDF1–2，2015營收€128m及premium/outsourcing/cost management','scope':'買方當時獲利解釋，未來目標不能當已完成'},
'S9':{'source':'S9','locator':'2017-01-24 Holds 100% of the Shares公告','scope':'完成餘股強制收購、連庫藏股達全部、同日撤牌'},
'S10a':{'source':'S10','locator':'2017 Activity Report分冊PDF6／印刷44–45，81%/19%及Smart Writing','scope':'2017銷售比重與當年產品，非現在產品組合或數位轉型成功'},
'S10b':{'source':'S10','locator':'2017 Activity Report分冊PDF5–6／印刷44–45，直營+16.6%、網店-3.7%、平台遷移及人員/IT','scope':'當年銷售、營運及投資，不等於利潤'},
'S10c':{'source':'S10B','locator':'2017 Annual Report財務印刷7／PDF65，loss-making Retail channel','scope':'當年零售通路虧損，不可說每一家店虧損或造成2025減損'},
'S11':{'source':'S11','locator':'2025 Full-Year Results PDF10，Moleskine Results；數表PDF23–25','scope':'2025同比、部分美國大客戶控庫存，不是全體消費者拒買'},
'S12':{'source':'S11','locator':'2025 Full-Year Results PDF10、42，品牌無形資產減損與2026–2030現金流','scope':'€107.4m稅前品牌減損，非現金支出、退貨或稅後€77.4m'},
'S13a':{'source':'S13','locator':'2026 Half-Year Results PDF9、11，銷售52.2m/2.2%、有機定義；PDF16營業比較','scope':'只比同半年；有機排除匯率及合併範圍變動；非全年'},
'S13b':{'source':'S13','locator':'2026 Half-Year Results PDF9、21，€76.4m waiver、186.8m intersegment financing','scope':'減免部分本金降低財務費用，非全數免債或營業利潤回升'},
}
# Author rows: key, text, source anchors, old prompt candidate or None, new conceptual prompt.
rows=[]
def add(key,text,refs,old=None,prompt=None,card=None):
 rows.append(dict(key=key,text=text,refs=refs.split(',') if refs else [],old=old,prompt=prompt,card=card))
def use(p,s,text=None,refs=None):
 ident=f'c03-p{p:02}-s{s:02}'
 old=old_by[ident]
 default={2:'S2',3:'S1a',4:'S1b,S3',5:'S1c',6:'S1c',7:'S6a',8:'S5',9:'S3,S1c',10:'S7,S1c',11:'S7',12:'S1f,S6b',13:'S8a,S8b',14:'S9',15:'S10a',16:'S10b,S10c',17:'S11',18:'S11,S12',19:'S13a,S13b',20:''}[p]
 add(f'p{p:02}s{s:02}',text if text is not None else old['lines'][0]['text'],refs if refs is not None else default,ident)
def start(ch):rows.append({'chapter_marker':ch})
def new(key,text,refs,action,place='at a reading table',size='Medium shot'):
 add(key,text,refs,prompt=f'{size} {place}, one anonymous adult {action}, soft window light.')
start(chapters[0])
new('h01','你可能只是想買一本筆記本，賣小黑本的公司，上市時市值卻逼近五億歐元。','S7','holding a plain black pocket notebook with a surprised face','at an unmarked bookshop counter','Close-up')
new('h02','二〇一三年四月三日，義大利交易所宣布一家公司掛牌；它的招牌商品，翻開竟是一片空白。','S7','opening a blank notebook beside a closed plain office folder','at a neutral office desk','Medium shot')
new('h03','我看到這裡先愣了一下：沒有印好的故事，這本書靠什麼吸引你？','','looking at an empty notebook page with a curious face','at a reading table','Close-up')
new('h04','上市文件往前追，竟連到比現代品牌早得多的作家。','S1a,S3','studying a plain black notebook beside a closed blank archive folder','in a quiet reading room')
new('h05','多年後，一份財報又得重新計算這個名字的價值。','S12','turning a blank report page with a thoughtful face','at an office desk','Close-up')
new('h06','今天就跟著 Moleskine 這本小黑本，看看它怎麼從書架，走到剛剛那個公司市值。','S7','lifting a plain black notebook from an unmarked shelf','in a small bookshop','Wide shot')
new('h07','一本空白本，究竟怎麼讓人願意為它的名字付錢？','','holding an open blank notebook toward the viewer with a questioning face','at a bookshop counter','Medium shot')
start(chapters[1])
use(2,1,'要找這個名字的起點，Moleskine 官網先帶你去看旅行作家查特文的《歌之版圖》。')
use(2,2,'依官網轉述，他熟悉的小黑本買不到了：法國圖爾的製造者在一九八六年停業，他四處找剩下的本子。')
use(2,3,'我覺得這裡要停一下：我們聽到的是品牌轉述的作家故事，沒有那家工廠當年的完整檔案。')
use(2,4,'當時還沒有今天這個品牌；誰會讓那種本子再回到貨架？','S1a,S3')
use(3,1,'接下這個空位的，是米蘭出版商 Modo&Modo。')
use(3,2,'招股書記載，它在一九九五年重啟生產這類小本子：黑色硬封面、圓角、鬆緊帶，裡面有個口袋。')
new('o01','你看見的是一套熟悉的外形。出版商接住的是舊式物件，沒有接到歷史人物替新品牌寫下的推薦。','S1a,S3','examining the rounded corner of a plain black notebook','at a reading table','Close-up')
new('o02','招股書甚至把早年的本子形容成沒有名字、卻很容易辨認的東西。這就留下了一個可以命名的位置。','S1a','placing a plain black notebook beside an empty label card','at a simple design table')
use(3,4,'產品已重新做出來；出版商何時才替這套外形提出自己的商標申請？','S1a,S1b')
use(4,1,'一九九七年十一月二十六日，是招股書商標章節列出的首次申請日。','S1b')
new('o03','從這裡開始，老式小黑本和現代品牌得分開說；否則，不就變成了真人替後來的商品背書？','S1a,S1b,S3','sorting a plain old-style notebook and a blank modern folder into separate spaces','at a reading table')
use(4,2,'官網把梵谷、畢卡索、海明威連到的，是那種老式筆記本；','S3')
use(4,3,'他們沒有用過這個現代品牌的商品。','S3')
new('o04','所以開頭那些早於商標的作家，提供的是品牌借來說明型制的文化脈絡，不能把新商品的年紀往前加。','S1a,S3','closing a blank archive folder beside a plain notebook','in a quiet reading room','Close-up')
use(4,4,'你現在知道名字從哪裡來了，可是貨架上有那麼多空白本，買家為何要選它？','S1c')
start(chapters[2])
use(5,1,'出版商給的答案，是把它當成「一本還沒寫出來的書」。','S1c')
use(5,2,'你買到的紙張沒有現成內容，可以記旅行、畫草圖，或寫自己的日記。','S1c')
use(5,3,'在發行人的構想裡，買的人接過本子，也接過作者的位置。','S1c')
new('i01','我覺得這個轉法很聰明：一般書已經替你寫好，這本卻把完成它的工作，交到你手上。','','holding an open blank notebook beside a closed unlettered book','at a reading table')
new('i02','公司想聯繫的，是文化、記憶、想像和旅行。它判斷，這些意義可以跟著顧客移動，也能移到別的商品。','S1c','placing a blank notebook into a plain travel bag','at a station bench','Close-up')
use(5,5,'這種定位要在貨架前成立，本子該先擺進哪種店？','S1c')
use(6,1,'出版社優先選了書店。','S1c')
use(6,2,'書店的讀者正在找下一本書，這裡卻放了一本等你動筆的商品。','S1c')
new('i03','招股書說，書店是讓文字傳播文化的地方，因此適合接近公司想找的客群。選貨架，本身就在說故事。','S1c','placing a plain black notebook among unlettered books','inside an unmarked bookshop')
use(6,4,'這是公司的定位與通路選擇；光憑這份文件，不能說每個顧客都因名人故事而掏錢。','S1c')
use(6,5,'本子進了書架，若要在更多城市被看見，光靠一本一本介紹，還缺什麼？','S1c,S6a')
use(7,1,'它靠批發網出去，由各地的經銷商與店家把貨送向顧客。','S1g,S1h')
use(7,2,'後來的投資人簡報回看，二〇〇五年約有一萬兩千個批發銷售據點。','S6a')
use(7,3,'這些是代賣產品的據點，不能全算成自營門市，也不能全算成書店。','S6a')
use(7,6,'別人的貨架開始替它鋪路，下一步，被投資人買走的會只是那些存貨嗎？','S5')
use(8,1,'二〇〇六年秋，Modo&Modo 被投資方收購。','S5')
use(8,2,'交易接走的是擁有品牌與通路的生意；本子仍在店裡，背後控制權換了人。','S5')
new('i04','招股書記載，新管理層把更多資源放進品牌溝通，以及店裡的展示架和專屬陳列空間。','S1d','aligning plain notebooks on a simple dedicated shelf','inside a bookshop')
new('i05','這讓我注意到，空白頁的包裝沒有停在一段古老故事；還得有人安排它在現代店面怎麼被看見。','S1d','adjusting the position of a plain notebook display with a focused face','inside a small bookshop','Close-up')
use(8,4,'隔年，Moleskine 這個名字又被放到了哪裡？','S3,S5')
use(9,1,'二〇〇七年一月一日起，它也成了持有全球商標權的公司名稱。','S3')
use(9,2,'同一個名字，可以繼續帶著行事曆、書寫用品與旅行配件對外銷售。','S1c,S7')
new('i06','到二〇一〇年，批發銷售據點約兩萬個。你不必只走進它自己的店，才有機會碰到那本小黑本。','S6a','lifting a plain black notebook from a modest shop shelf','inside a neighborhood store','Wide shot')
use(10,1,'到了開頭那次掛牌前，公司賣的已不只是筆記本。','S7')
use(10,2,'義大利交易所把它描述為經營書寫、旅行與閱讀商品的集團。','S7')
use(10,5,'這門從空白頁長出的生意，終於到了股市；投資人替它標了多少？','S7')
use(11,1,'還記得開頭那次掛牌嗎？上市時整家公司市值約四億八千七百六十萬歐元。','S7')
use(11,2,'你看到的是股票市場給公司的估值，不能把它當成當年賣本子的收入。','S7')
use(11,4,'不過，讓公司值錢的未來訂單，還得靠一箱箱產品抵達貨架；它究竟怎麼安排？','S1e,S1g,S1h')
start(chapters[3])
new('e01','那箱貨的背後，先有一份排程。上市招股書說，實際生產交給外部供應商網路，公司仍管理流程與品質。','S1e','checking a plain notebook sample beside a closed supply carton','at a neutral operations desk')
new('e02','營運部門每個月都做一份往後十二個月的需求規畫，再安排採購訂單；歷史銷售、現有庫存和交期都得放進去。','S1e','arranging blank planning cards beside a sealed carton','at an operations desk','Close-up')
new('e03','你在書店只拿走一本，另一頭卻得提早決定要做多少。我覺得真正不浪漫的考題，就藏在這個數量裡。','S1e','studying a small stack of plain notebooks with a thoughtful face','at a warehouse desk')
new('e04','做出來還不算完成。貨到了經銷商倉庫，就一定已經變成公司的銷售了嗎？','S1g,S1h','examining a sealed carton on an unmarked storage shelf','inside a simple warehouse','Wide shot')
new('e05','招股書列了不同契約；其中寄售方式下，倉庫裡的產品，仍可能屬於 Moleskine。','S1g','placing a sealed plain carton onto a storage shelf','inside a simple warehouse')
new('e06','要等經銷商賣給零售店、據此從倉庫提貨，貨權與相關庫存風險才移轉。這還沒等你結帳；那經銷商負責什麼？','S1g','lifting a plain carton from a storage shelf','inside a simple warehouse','Close-up')
new('e07','經銷商仍負責向店家收訂單，並承擔信用與配送的風險及成本；這不是公司包下每一種風險。','S1g','sorting blank order cards beside a delivery carton','at a distribution counter')
new('e08','另一種非寄售方式，則依契約，在出貨或交到經銷商時完成銷售；同樣一箱本子，交棒的時點不同。','S1h','passing a sealed plain carton across an empty loading counter','inside a loading area','Wide shot')
new('e09','可交出去之後，誰知道倉庫裡是不是堆太多？公司的訂單漂亮，店家卻未必補得一樣快。','S1h','looking at a full plain storage shelf with a concerned face','inside a simple warehouse')
new('e10','當時公司逐步要求這類經銷商，每月分享賣給零售店的資料，拿來對照進貨，監看庫存過高或過低。','S1h','comparing two rows of blank order cards beside a notebook stack','at a warehouse desk','Close-up')
new('e11','這些是剛才那份二〇一三年文件揭露的安排，不能當成現在每個客戶的合約；但它讓貨架前的故事多了一條看不見的線。','S1g,S1h','following a plain carton along a short unmarked counter','at a distribution desk')
new('e12','你買走的是一本，企業要等的卻是一連串補貨決定。那為什麼還要自己開店，替這條路加一個入口？','S1f','holding a plain notebook while looking toward a small unmarked shop display','inside a retail store','Wide shot')
use(12,1,'招股書給的想法是，直接通路能控制品牌和全系列怎麼展示，間接通路則幫產品抵達更多地方。','S1f')
new('e13','公司設想，自家店讓人認識商品，需求也可能流到代賣店。這個直接接近顧客的入口，後來開了多大？','S1f','placing a plain pen beside a notebook on a simple shop display','inside an unmarked store')
use(12,2,'到二〇一六年底，已有七十九家直營店，也經營網路銷售。','S6b')
use(12,3,'自己的店能把本子、筆和包一起展示，也得由自己負責門市營運。','S1f,S10b')
new('e14','我覺得這才是那個選擇的重量：得到展示方式的控制權，也接過每天讓店面運轉的工作。','','checking a modest unmarked shop display with a focused face','inside a small store','Close-up')
use(12,5,'這張由批發、直營和網店接成的網，吸引了一個原本離紙張很遠的買方。','S8a,S8b')
start(chapters[4])
use(13,1,'買方是比利時 D’Ieteren。二〇一六年九月，它宣布簽約收購 Moleskine 四成一股權，再計畫收購餘股。','S8a')
use(13,2,'這個集團原來做汽車經銷和汽車玻璃服務；你大概也會好奇，它看上小黑本什麼？','S8a,S8b')
use(13,3,'公告把高端定位、委外生產和成本管理，列為 Moleskine 當時高獲利的理由。','S8b')
new('t01','公告列出二〇一五年營收一億兩千八百萬歐元；要買這門已在收錢的生意，股份被標成什麼價格？','S8b','reviewing a blank sales folder beside a plain notebook','at a neutral meeting table')
new('t02','協議每股價格是兩歐元四角，對整家公司股權的估值，約五億零六百萬歐元。','S8a','placing a plain closed share folder on a meeting table','in a neutral office','Close-up')
new('t03','這個價錢是拿來買股份，不是把同額現金存進本子公司的帳戶。我覺得這一步最容易把估值聽成收入。','S8a','sorting a blank share folder and a plain cashbook into separate spaces','at a neutral office desk')
use(13,5,'可是簽協議還有交割程序。剩下的股份，最後到誰手上？','S8a,S9')
use(14,1,'二〇一七年一月二十四日，D’Ieteren 完成剩餘股份的強制收購；','S9')
use(14,2,'連同庫藏股，Moleskine 全部股份都進入集團控制，股票也在同日從米蘭市場下市。','S9')
use(14,4,'新主人接下的，還主要是一門紙本生意嗎？','S10a')
use(15,1,'那一年，紙本仍占銷售額的百分之八十一。','S10a')
use(15,2,'背包、智慧筆與其他配件已在商品裡，卻還沒把紙本的主位換掉。','S10a')
new('t04','當年的智慧書寫組合，試著讓人先在紙上創作，再連到數位工具；這是產品方向，不能直接當成轉型成功。','S10a','writing on a blank notebook beside an unmarked dark tablet','at a reading desk','Close-up')
use(15,5,'產品跨出紙本，銷售也跨出代賣店。自己經營的店，那年交出了什麼成績？','S10b,S10c')
new('t05','二〇一七年，直營零售銷售比前一年成長，年報卻仍把它列為虧損通路。你看，營收增加，和賺錢並不是同一件事。','S10b,S10c','checking a blank sales folder beside a quiet shop till','inside a small store')
use(16,1,'網店則在遷移到新平台的那一年，銷售下降。改善購物體驗的投資，還得加上哪些營運工作？','S10b')
new('t06','公司同年還投入人員與資訊系統。這些工作不是黑封面上的故事能代勞的；商品得被展示，也得有人把訂單做完。','S10b','checking a plain closed order folder beside an unmarked computer','at a retail back-office desk')
use(16,4,'我看到這裡，才明白入口變多也會帶來負擔；多年後，最早替小黑本鋪路的批發網，又先踩了煞車。','S10b,S11')
start(chapters[5])
use(17,1,'踩煞車的年份是二〇二五年。Moleskine 全年銷售約一億一千七百八十萬歐元，比前一年少百分之三點七。','S11')
use(17,2,'不過，集團說除了批發，其餘通路按公司的有機口徑仍有成長。','S11')
new('n01','你也許會先想到，大家是不是不買紙本了？財報給的原因卻更具體：美國部分大客戶持續謹慎管理庫存。','S11','considering a small reorder stack beside a full notebook shelf','at a wholesale counter')
use(18,2,'還記得那箱到經銷商倉庫的貨嗎？公司、店家和最後買本子的人，本來就有不同的進貨時點。','S1g,S1h,S11')
use(18,3,'店家放慢補貨，可以先影響公司的銷售；這份報表並沒有逐一告訴我們，每位消費者在收銀台怎麼選。','S11')
new('n02','為什麼收入少一點，獲利卻可能少更多？那年調整後營業結果減半，公司指出通路組合、增加的行銷費與營運槓桿壓力。','S11','studying a blank cost folder beside a plain notebook with a worried face','at an office desk','Close-up')
new('n03','我覺得還得再追一問：營運承壓之後，開頭那個名字的帳面價值又怎麼辦？','S12','closing a blank expense folder beside a plain shop till','at a retail counter')
use(18,4,'這份二〇二五年度財報，記下開頭預告的帳面重算：品牌無形資產減損約一億零七百四十萬歐元。','S12')
new('n04','用往後五年的財務預測，把未來現金流折回今天，檢查帳上價值能不能支持。','S12','comparing a blank forecast folder and a plain ledger','at an office desk')
use(18,5,'所以這是品牌資產的帳面重算，不是那年多付了同額現金，也不是退回來那麼多本子。','S12')
new('n05','名字曾讓新商品帶著文化想像出發，現在預期能帶回多少收入，也得接受重新估計。下一個半年，補貨回來了嗎？','S12,S13a','looking from a plain black notebook toward a small reorder carton','at a wholesale counter')
use(19,1,'較新的二〇二六年上半年，集團說美國批發回升，零售通路也有不錯表現。','S13a')
use(19,2,'銷售約五千兩百二十萬歐元，比上年同半年增加百分之二點二。','S13a')
new('n06','這裡比的是同一個半年，不能拿它和上一個全年硬比。可收入回升，營業結果也跟著上來了嗎？','S13a','comparing two blank half-year folders of equal size','at a neutral office desk','Close-up')
use(19,4,'營業結果是七十萬歐元，比上年同期略低。','S13a')
use(19,3,'調整後集團應占稅前虧損縮小，主要因為部分股東貸款本金獲減免，財務費用降低。','S13b')
new('n07','我覺得這個收尾很誠實：少付融資費用，能讓虧損變小，卻不能代替產品和通路多賺一筆營業利潤。','S13a,S13b','putting a plain loan folder beside a separate blank sales folder','at an office desk')
use(19,5,'對你來說，補回架上的仍是那本小黑本；那一開始的問題，它到底憑什麼讓你為名字付錢？','S11,S13a,S13b')
use(20,1,'從招股書看，公司的做法是把舊式本子定位成一本等待你創作的書，再用展示和通路把它送到你面前。','S1c,S1d,S1f')
use(20,3,'如果是你挑筆記本，會先聽它的故事，還是先摸紙、試試好不好寫？留言告訴我。','')
use(20,4,'想繼續從日用品看懂一個名字怎麼變成生意，還要面對哪些現實考驗，歡迎訂閱。','')

# Exact old picture prompts are preserved only where their objects/actions still fit.
# No paid image files are available in this workspace, so this is eligibility, never actual reuse.
scenes=[];narrative=[];claims=[];reuse=[];line_for={};chapter='';cam=['push in','pan left','pull out','pan right','tilt up','tilt down']
newprompts={
'p04s01':'Close-up at an office desk, one anonymous clerk setting a blank application folder beside a plain black notebook, soft lamp light.',
'p11s01':'Medium shot in a neutral office, one anonymous analyst reviewing a blank share-price folder beside a plain notebook, soft window light.',
'p12s02':'Wide shot inside an unmarked small shop, one anonymous clerk arranging plain notebooks on a modest shelf, mild overhead light.',
'p13s01':'Medium shot at a neutral meeting table, one anonymous clerk placing a blank agreement folder beside a plain notebook, soft window light.',
'p13s02':'Close-up at a neutral office desk, one anonymous analyst holding a blank company folder with a curious face, soft lamp light.',
'p15s01':'Medium shot inside a stationery shop, one anonymous clerk arranging a large notebook stack beside a smaller pile of plain bags, mild overhead light.',
'p18s04':'Close-up at an office desk, one anonymous accountant studying a blank report folder with a concerned face, soft lamp light.',
'p18s05':'Medium shot at an office desk, one anonymous accountant closing a blank ledger beside a plain notebook, soft window light.',
'p19s02':'Close-up at a retail desk, one anonymous clerk placing a notebook beside a blank half-year sales folder, mild overhead light.',
'p19s04':'Medium shot at an office desk, one anonymous accountant studying a blank half-year folder beside a plain notebook, soft window light.',
}
# A small number of metric cards do work pictures cannot: show one exact measure and its period.
cards={
'p04s01':('商標第一次申請','1997.11.26','首次申請日；不是當天核准','2013招股書 §11.2，印刷258'),
'p11s01':('股票市場給公司的價','約4.876億歐元','2013上市時公司市值','義大利交易所，2013-04-03'),
'p12s02':('自己經營的門市','79家','2016年底直營店','2016活動報告印刷35、37；2017年報財務印刷7'),
'p13s01':('先簽股權協議','41%','2016年9月簽約；不是完成100%','D’Ieteren，2016-09-22'),
't02':('整家公司股權估值','約5.06億歐元','2016協議價格推算；非公司收入','D’Ieteren，2016-09-22，PDF1'),
'p15s01':('紙本仍是主體','81%','2017年銷售額占比','2017活動報告，印刷44–45'),
'p18s04':('名字的帳面價值重算','約1.074億歐元','2025品牌無形資產減損','2025全年業績，PDF10、42'),
'p19s02':('較新的半年銷售','約5,220萬歐元','2026上半年；同比增加2.2%','2026半年業績，PDF9'),
'p19s04':('營業結果沒有跟著升','70萬歐元','2026上半年；比上年同期略低','2026半年業績，PDF9、16'),
}
for row in rows:
 if 'chapter_marker' in row:chapter=row['chapter_marker'];continue
 key=row['key'];sid='c03r-'+key.lower();old=old_by.get(row['old']);prompt=row['prompt'];elig='new_conceptual_prompt'
 if old and old['template']=='shot':prompt=old['data']['prompt'];elig='eligible_prompt_verbatim'
 if not prompt:prompt=newprompts.get(key, f'Medium shot at a reading desk, one anonymous adult examining a plain black notebook with a thoughtful face, soft window light.')
 scene={'id':sid,'template':'shot','data':{'prompt':prompt,'visual':'still','camera':cam[len(scenes)%len(cam)]}}
 if key in cards:
  title,value,label,src=cards[key];scene={'id':sid,'template':'stats','data':{'title':title,'stats':[{'value':value,'label':label}],'source':src}}
  elig='card_no_image_reuse'
 if not scenes or chapter!=narrative[-1]['chapter']:scene['chapter']=chapter
 text=row['text']
 # These reviewed clause boundaries retain the exact r1 line IDs in a narrow r2 delta.
 fixed_parts={
  'h06':['今天就跟著 Moleskine 這本小黑本，','看看它怎麼從書架，走到剛剛那個公司市值。'],
  'p18s04':['這份二〇二五年度財報，記下開頭預告的帳面重算：','品牌無形資產減損約一億零七百四十萬歐元。'],
  'p20s01':['從招股書看，公司的做法是把舊式本子定位成一本等待你創作的書，','再用展示和通路把它送到你面前。'],
 }
 parts=fixed_parts.get(key) or [p for p in re.split(r'(?<=？)',text) if p]
 # Keep short natural TTS clauses; no timing padding or fake measured timeline.
 while any(len(p)>42 for p in parts):
  out=[];changed=False
  for part in parts:
   options=[m.end() for m in re.finditer('[，；：。？]',part) if 12<=m.end()<=len(part)-10]
   if len(part)>42 and options:
    pos=min(options,key=lambda x:abs(x-len(part)/2));out += [part[:pos],part[pos:]];changed=True
   else:out.append(part)
  parts=out
  if not changed:break
 scene['lines']=[]
 for j,part in enumerate(parts):
  lid='r3'+re.sub('[ps]','',key.lower())+str(j+1);line={'id':lid,'text':part,'emotion':'自然親近，問句上揚' if part.endswith('？') else '說書語氣，自然有起伏'}
  scene['lines'].append(line);line_for.setdefault(key,lid)
  narrative.append({'chapter':chapter,'id':lid,'text':part})
  supports=[dict(id=a,**anchors[a]) for a in row['refs']]
  if lid=='r3n051':supports.append(dict(id='S1c',**anchors['S1c']))
  claims.append({'chapter':chapter,'scene':sid,'line':lid,'text':part,'source_anchors':supports,'editorial':not bool(supports) or '我覺得' in part or '你' in part,'boundary':'所有公司定位及敘述保留歸屬；假想視角/旁白反應不是訪談或實測','status':'PENDING_NEW_INDEPENDENT_REVIEW'})
 reuse.append({'scene':sid,'old_scene':row['old'],'eligibility':elig,'prompt_sha256':hashlib.sha256(prompt.encode()).hexdigest() if scene['template']=='shot' else None,'prompt_verbatim':bool(old and old['template']=='shot' and scene['template']=='shot' and prompt==old['data']['prompt']),'media_available':False,'actual_media_reuse':False,'condition':'僅語意與提示詞相容；須取回原圖、核對hash及原評審，再按新旁白重審，不能憑此表宣稱重用'})
 scenes.append(scene)
# Split five long stills at already-authored clause boundaries; narration words are unchanged.
split_keys={'c03r-e02','c03r-e11','c03r-t06','c03r-n02','c03r-n05'}
expanded=[]
for scene in scenes:
 if scene['id'] in split_keys and len(scene['lines'])>1:
  after=copy.deepcopy(scene);after['id']+='-b';after.pop('chapter',None);after['lines']=scene['lines'][1:];scene['lines']=scene['lines'][:1]
  after['data']['prompt']={
   'c03r-e02':'Close-up at a warehouse desk, one anonymous planner examining a small stack of plain stock cartons, mild overhead light.',
   'c03r-e11':'Medium shot at a distribution desk, one anonymous clerk studying a plain carton beside a closed blank contract folder, soft lamp light.',
   'c03r-t06':'Close-up in a retail back office, one anonymous clerk opening a plain order folder beside an unmarked computer, mild overhead light.',
   'c03r-n02':'Medium shot at an office desk, one anonymous accountant examining a plain expense folder with a concerned face, soft lamp light.',
   'c03r-n05':'Close-up at a wholesale counter, one anonymous shopkeeper placing a plain reorder carton beside a notebook stack, mild overhead light.',
  }[scene['id']]
  moved={l['id'] for l in after['lines']}
  for claim in claims:
   if claim['line'] in moved:claim['scene']=after['id']
  reuse.append({'scene':after['id'],'old_scene':None,'eligibility':'new_conceptual_prompt','prompt_sha256':hashlib.sha256(after['data']['prompt'].encode()).hexdigest(),'prompt_verbatim':False,'media_available':False,'actual_media_reuse':False,'condition':'New planned illustration; no paid media exists here.'})
  expanded.extend([scene,after])
 else:expanded.append(scene)
scenes=expanded
for i,scene in enumerate(scenes):
 if scene['template']=='shot':scene['data']['camera']=cam[i%len(cam)]
# Explicit final three-line outro. Author-only projection still carries the final chapter.
last=scenes[-3:];outro_ids={s['id'] for s in last}
scenes=scenes[:-3]+[{'id':'c03r-outro','template':'outro','data':{'title':'名字有故事，生意要經營','cta':'留言：你先看故事，還是先摸紙？'},'lines':[l for s in last for l in s['lines']]}]
for c in claims:
 if c['scene'] in outro_ids:c['scene']='c03r-outro'
for r in reuse:
 if r['scene'] in outro_ids:
  r.update({'render_scene':'c03r-outro','eligibility':'not_used_outro_template','old_prompt_eligible':r['prompt_verbatim'],'prompt_verbatim':False})
loops=[
('h01','p20s01','小黑本如何把名字變成有人願意買的商品'),
('h04','o04','早於現代商標的作家，究竟和品牌是什麼關係'),
('h05','p18s04','後來哪份財報重新計算這個名字的價值'),
('o03','p04s03','歷史藝術家是否替後來的商品背書'),
('e06','e07','等到零售商下單之前，經銷商承擔什麼工作'),
('e13','p12s02','直營門市後來擴到多大'),
('t01','t02','已有營收的生意在協議裡如何標出股份價格'),
('p16s01','t06','改善購物體驗還需要投入哪些營運工作'),
('n02','n02','銷售小幅下滑時營業結果為何減半'),
('n03','n04','名字的帳面價值如何重新估計'),
('p19s05','p20s01','開場名字被買單的問題如何回答'),
('p02s04','p03s01','誰把買不到的舊型制重新送回貨架'),
('p03s04','p04s01','何時提出現代商標首次申請'),
('p04s04','p05s01','除了外形，出版社給空白本什麼定位'),
('p05s05','p06s01','待寫的書先擺進什麼店'),
('p06s05','p07s01','如何跨出一本一本介紹的範圍'),
('p07s06','p08s02','投資人買下的是存貨還是整門生意'),
('p08s04','p09s01','公司名稱如何承接品牌'),
('p10s05','p11s01','市場替公司標了多少價格'),
('p11s04','e01','一箱貨抵達貨架之前由誰安排生產'),
('e04','e05','貨到經銷商倉庫是否等於完成銷售'),
('e09','e10','交出去的貨，如何避免庫存訊號失真'),
('e12','p12s01','為什麼批發之外還要自己開店'),
('p12s05','p13s01','哪個遠離紙張的買方看上這張通路網'),
('p13s02','p13s03','做汽車業務的買方看中什麼獲利模式'),
('p13s05','p14s01','餘股收購何時完成'),
('p14s04','p15s01','新主人接到的產品還有多少靠紙本'),
('p15s05','t05','直營零售的成長是否變成盈利'),
('p16s04','p17s01','早期鋪路的批發網何時先踩煞車'),
('n01','p18s03','批發控庫存能否直接當成消費者不買'),
('n05','p19s01','下一個半年補貨是否回來'),
('n06','p19s04','銷售回升時營業結果是否同升'),
]
doc=copy.deepcopy(source);doc['slug']=SLUG;doc.pop('series',None);doc['target_minutes']=[12,14];doc['subtitles']={'burn_in':True};doc['look']={'preset':'cute-mystery'}
doc['voice']['name']='Sulafat';doc['voice']['performance']='對一位觀眾說故事，作家舊型制與現代品牌分開；通路用貨物動作說明；交易估值、收入、減損與貸款費用分開自然慢說。'
doc['scenes']=scenes;doc['loops']=[{'setup':line_for[s],'payoff':line_for[p],'what':w} for s,p,w in loops]
doc['loops']=[loop for loop in doc['loops'] if loop['setup']!=loop['payoff']]
# n02 asks and answers in distinct clauses of the same scene.
doc['loops'].append({'setup':line_for['n02'],'payoff':next(l['id'] for scene in scenes for l in scene['lines'] if l['id'].startswith('r3n02') and l['id']!=line_for['n02']),'what':'收入小幅下降時獲利為何受到更大壓力'})
doc['youtube']['title']='Moleskine賣空白本，公司為何值近5億？｜品牌故事'
doc['youtube']['description']='一本沒有印好內容的小黑本，為什麼能變成上市公司？沿著Moleskine的產品定位、書店與批發策略，看到自己開店的營運工作，以及2025年補貨、品牌減損與較新的2026上半年業績。\n\n歷史藝術家與舊式筆記本有關，沒有用過1997年才成形的現代品牌。精確的1997年11月26日是首次商標申請日。市值、股份估值、營收、品牌資產減損是不同數字；2013招股書的契約安排不代表2025特定客戶的合約。插圖均為匿名概念示意。\n\n資料作者閱讀：2026-10-25；本版仍待獨立逐句覆核。\n\n一手來源：\n'+'\n'.join(x['title']+'\n'+x['url'] for x in source['sources'])
doc['thumbnail']={'template':'thumb','data':{'layout':'d','brand':'Moleskine','tag':'品牌故事','headline':'把空白賣全球','sub':'公司市值近五億','shot':'c03r-h01'}}
series=copy.deepcopy(json.loads((OLD/'series.json').read_text()));series.update({'title':doc['youtube']['title'],'logline':'沿著一本黑色空白本，追出版社怎麼安排它的文化定位、貨架和補貨，直到公司估值與近年財務檢驗。','target_minutes':13,'image_model':'image-01','look':{'preset':'cute-mystery'}})
write=lambda name,value:(DEST/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
catalog_ids=['S1','S2','S3','S6','S7','S8','S9','S10','S10B','S11','S13']
catalog={k:{**s,'reviewer_only':'.pdf' in s['url']} for k,s in zip(catalog_ids,source['sources'])}
catalog['S6B']={'title':'D’Ieteren2016 ActivityReport及2017年報','url':'https://dieterengroup.imgix.net/annual-reports/3_moleskine.pdf','additional_url':catalog['S10B']['url'],'reviewer_only':True,'checked_on':'2026-10-22'}
for val in anchors.values():val.update({k:v for k,v in catalog[val['source']].items() if k in ('url','additional_url','title','reviewer_only')})
for claim in claims:claim['source_anchors']=[{'id':x['id'],**anchors[x['id']]} for x in claim['source_anchors']]
write('video.json',doc);write('series.json',series);write('narration-only.json',narrative);write('claims.json',claims);write('reuse-eligibility.json',reuse);write('source-anchors.json',anchors);write('source-catalog.json',catalog)
manifest={}
for name in ['prospectus','acquisition','fy2025','h12026','activity2017']:
 f=Path('/workspace/work/c03-audit')/(name+'.pdf')
 if f.exists():manifest[name]={'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'bytes':f.stat().st_size,'author_read_on':'2026-10-25','local_cache':str(f),'review_status':'AUTHOR_READ_ONLY_NOT_INDEPENDENT_APPROVAL'}
if manifest:write('source-snapshot-manifest.json',manifest)
script=['# '+doc['youtube']['title'],'','作者候選：10/25規則；未取得本版來源PASS、雙盲或站主劇本核准。實際TTS尚未生成。',''];previous=''
for row in narrative:
 if row['chapter']!=previous:script += ['## '+row['chapter'],''];previous=row['chapter']
 script += [f"[{row['id']}] {row['text']}",'']
(DEST/'script.md').write_text('\n'.join(script))
md=['# C03 新版逐句來源映射（待獨立覆核）','','這是作者來源映射，不是來源PASS或舊批准的延伸。舊稿、舊收據及本目錄existing-evidence均未改。','',
'來源URL沿用原C03 source-matrix.md的S1–S13；本版新增S1e–S1h為直接重開原招股書的委外、排程及契約機制。精確1997日期依§11.2修成首次申請，不沿用舊來源表的完成註冊說法。',
'PDF仍標reviewer_only；頁碼是原件定位，不代表主機工人可讀。S6B為2016活動報告及2017年報，S10B為2017完整年報；其URL見下方來源索引。','',
'| 句ID | 旁白 | 原件頁／段與範圍 | 狀態 |','| --- | --- | --- | --- |']
for c in claims:
 supports='；'.join(a['source']+' '+a['locator']+'〔'+a['scope']+'〕' for a in c['source_anchors']) or 'editorial：旁白反應、承諾、中心問句或留言/訂閱邀請，非另添史實'
 md.append(f"| {c['line']} | {c['text']} | {supports} | PENDING |")
md+=['','## 原件索引','']
for i,s in enumerate(source['sources']):md+=['- '+s['title']+'：'+s['url']]
md+=['- S6B 2016活動報告：https://dieterengroup.imgix.net/annual-reports/3_moleskine.pdf','- S10B 2017完整年報：https://dieterengroup.imgix.net/annual-reports/annualreport2017_en_0-1.pdf']
(DEST/'claims.md').write_text('\n'.join(md)+'\n')
notes={'status':'UNAPPROVED_CANDIDATE','author_revision':2,'author':'/root/remake_c03','slug':SLUG,'source_video_sha256':hashlib.sha256((OLD/'video.json').read_bytes()).hexdigest(),'source_base_commit':'2b20c30d359fe5d93a4ea66f013a52fa20a35c05','reference_pr':1844,'target_minutes':13,'required_measured_narration_minutes':[12,14],'measured_audio_seconds':None,'paid_calls':0,'backend_writes':0,'approvals_created':0,'unknown_historical_claims_included':0,'source_status':'PENDING_NEW_INDEPENDENT_REVIEW','narrative_status':'NOT_SUBMITTED','reuse_status':'FRESH_PRODUCTION_WITH_OPTIONAL_HISTORICAL_PROMPT_MAP','notes':['1997-11-26 corrected to first trademark filing using prospectus section11.2, not completed registration.','All contract and outsourcing mechanisms are explicitly scoped to the 2013 prospectus; no assertion about a 2025 named customer contract.','2016 year end: 79 stores. The 2016 signed 41% stake and EUR 506m equity valuation are distinct from company sales; full acquisition completed on 2017-01-24.','2025 revenue decline and brand impairment are distinct. H1 2026 is the newer period and is compared only with the same half.','No source pass, owner approval or blind reader answers are inherited.','No old paid media is available here; the compatible prompt map does not claim actual reuse.'],'holds':['New independent per-line sources and written-visual review','New isolated narrative readers after freezing the exact version','Owner script decision, full episode quotation and production admission','Fresh canonical story lexicon initialized by root; no old project lexicon copied','Actual TTS and measured 12–14 minute narration; full media QA and owner final review']}
write('author-notes.json',notes)
print(json.dumps({'scenes':len(scenes),'lines':len(narrative),'characters':sum(len(r['text']) for r in narrative),'han':len(re.findall('[\u4e00-\u9fff]',''.join(r['text'] for r in narrative))),'loops':len(loops),'prompt_candidates':sum(r['prompt_verbatim'] for r in reuse)},ensure_ascii=False))
