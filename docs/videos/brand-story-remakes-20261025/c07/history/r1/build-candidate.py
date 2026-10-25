#!/usr/bin/env python3
"""Build the first C07 remake author candidate, without provider/backend calls."""
import copy
import hashlib
import json
import pathlib
import shutil
import subprocess

REPO = pathlib.Path('/workspace/work/brand-remakes-source')
OUT = pathlib.Path(__file__).resolve().parent
AUDIT = pathlib.Path('/workspace/work/brand-story-20261025/c07-audit')
RESEARCH = json.loads((AUDIT / 'claims.json').read_text())
SLUG = 'story-everyday-dr-martens-c07-remake-20261025'
TITLE = '馬汀靴：接底逾650度，換底為何得拆線？｜品牌故事'

# Each row is newly authored narration, its research claim IDs and a pictured action.
# Research IDs bind actual original bytes/excerpts below; they are not verifier PASS labels.
CHAPTERS = [
('鞋底磨平了，接縫還在', '''
你想替舊靴換底，碰到的卻可能是一道熱接縫。|N10,N18|turning over a worn plain lace-up boot at a repair counter
原廠現在的說明裡，接底熱刀的溫度超過六百五十度。|N10|examining a plain shoe sole beside an idle industrial tool
想像你在英國的維修檯前，把一隻靴子翻過來。|N17,N18|placing a worn plain lace-up boot upside down on a repair bench
底紋磨平了，鞋面卻還留著你穿出來的折痕。|N16|touching creases on a worn leather upper beside a worn smooth sole
我看到這裡，才發現鞋邊那圈線並不只是好看。|N08,N10,N18|looking closely at a line of stitches around a plain work boot
有人將褲腳收短，這雙靴子會被別人讀成什麼？|N14|looking down at plain work boots beneath cropped trouser legs
今天跟著馬汀靴的一道接縫，走過一九六〇年以來的六十多年。|N07,N17|holding one plain lace-up work boot above a blank workbench
它怎麼從撐住鞋面的地方，變成你不甘心連鞋一起丟掉的理由？|N10,N16,N18|holding a worn plain boot with a thoughtful face toward the viewer
'''),
('軟底把難題交給了鞋邊', '''
照品牌後來的回顧，一九四五年，馬汀斯傷了腳。|N01|resting one bandaged foot beside a plain hard-soled shoe
這名德國醫生想改善硬皮鞋底帶來的不適，做了一隻原型鞋。|N01|examining a plain prototype shoe at a small workshop table
他把帶著氣墊概念的鞋底，拿給工程師朋友馮克看。|N01|holding a simple cushioned sole sample at a workbench
兩人成了合夥人，到一九四七年開始正式生產。|N01|placing a finished plain shoe on an unmarked workshop shelf
日本的品牌沿革還提到，德國階段主要向年長女性販售。|N01|an older anonymous woman trying on a plain low shoe in a small shop
這個起點離後來的年輕人街頭造型，其實相當遠。|N01,N13,N14|an older anonymous customer studying a plain shoe beside a chair
如果你因腳傷而穿鞋，腳下能不能舒服些，會比鞋看起來多兇更急。|N01|carefully placing a recovering foot into a plain soft-soled shoe
可是鞋底一彎，連著它的地方，受得住嗎？|N05|bending a simple flexible footwear sample gently between both hands
我原先只注意軟不軟，讀到專利才發現，麻煩卡在邊上。|N05|tracing the edge of a flexible sole sample with one finger
一九五七年送件的一份美國專利，就把這個接合難題寫了下來。|N05|opening a blank technical folder beside a simple shoe section model
這份後來在一九六二年核准的方案，談的是彈性鞋底。|N05|examining a simple flexible sole sample beside blank technical pages
鞋底可以膠接或焊在沿條上；那它最容易從哪裡被拉開？|N05|pointing to the joining surface of an oversized plain footwear section model
作者描述，軟底受到側向的推力，接縫邊緣就會被拉扯。|N05|gently pushing the lower edge of a simple flexible sole demonstration model
例如鞋底勾到障礙物，下緣被扯開的方向，就可能拉開接合面。|N05|holding a shoe sole model with its outer edge caught on a plain low block
一個小小的外緣開口，還可能沿著接合面繼續分離。|N05|examining a short separated edge on a plain demonstration shoe joint
這是申請人在文件裡描述的失效情況，並非每雙靴子都會發生。|N05|studying a plain demonstration joint beside an intact shoe sample
要是你來處理，把接合面加寬就夠了嗎？|N05|sliding a broad plain strip beneath a flexible sole demonstration model
但文件接著指出，寬大的邊條會占掉裡頭的空間。|N05|comparing a broad strip with the open space inside a simple sole section
空腔變小，周圍的壁也變厚，原本想保留的彈性又受影響。|N05|pressing two simple sole section samples with different edge widths
接得住，還得能動，怎麼讓這兩個要求不打架？|N05|testing the movement of a plain sole section attached to an upper strip
於是這份方案在接合面邊緣附近，加入大致平行的槽或縫。|N05|pointing to a shallow groove near a joining surface on a plain section model
槽可以設在沿條、底的邊部，或設在兩邊。|N05|rotating a plain footwear section model to show alternative groove positions
照作者的解釋，這會改變拉力在接合面上的分布。|N05|holding a simple grooved joint model under a small sideways load
負荷不再只集中在最外緣，而能分到較寬的區域。|N05|examining a broad joining surface on an oversized grooved sole model
可是把外緣顧好了，接縫就不會再從別處裂開嗎？|N05|examining the inner edge of a simple footwear section model
文件還追到內側，因為鞋底和內底之間，可能留著空間。|N05|pointing into an open space inside an oversized plain sole section model
人踩下去，鞋底往上受壓；腳抬開時，底部又被彈性推回。|N05|pressing and releasing a simple flexible shoe section demonstration model
作者說，這也會拉扯接合面的內緣，尤其在前腳掌附近。|N05|pointing to the inner front joining region on a plain shoe section model
所以有的示例，讓槽由內部空間往邊部延伸，而不只處理外緣。|N05|examining a simple footwear section with a narrow groove opening inward
槽的位置跟著受力改；那今天鞋外的凹紋，就一定是這個構造嗎？|N05,N08|comparing a plain outer boot with a separate conceptual inner joint model
這裡的槽是具體的結構方案，不能直接拿來認定今天鞋邊每一道紋。|N05,N08|comparing a plain patent section model with the outside edge of a modern boot
專利留下的是接合構想，英國工廠實際採用哪一套，仍是另一件事。|N05,N06|closing a blank patent folder beside a plain unfinished work boot
文件還提出另一個難題：若在高溫環境工作，這種塑膠底受得了嗎？|N05|examining a plain polymer sole sample beside an idle guarded heating tool
作者擔心熱塑性材料被熱破壞，轉而討論更耐熱的橡膠或樹脂。|N05|comparing plain rubber and resin samples beside a simple joint model
但這些替代材料多半不能焊接，若要連到沿條，就得改用膠接。|N05|examining a plain nonweldable material sample beside a broad attachment strip
改用膠接時，文件說，需要的接合面又比焊接更寬。|N05|placing a broad plain attachment strip beside a narrow joined sole sample
你想保留彈性，又想改變耐熱性，材料和接法就得重新配合。|N05|matching plain material samples with separate demonstration joining strips
當一種鞋底交給另一家鞋廠，它會被做成什麼樣的靴子？|N06,N08|lifting a plain flexible sole toward an unfinished leather boot upper
'''),
('黃線繞上了英國靴', '''
一九五九年，照品牌的回顧，英國的格里格斯取得英國製造權。|N06|examining a plain sole sample in a modest footwear workshop
這項權利讓鞋廠能製造鞋子，並不是把所有地方的專利一口買斷。|N06|placing a blank agreement folder beside a plain shoe last
鞋廠用這種鞋底做出新靴，鞋面改得圓鼓而簡單。|N08|shaping a rounded plain leather boot upper over a last
你從側面看，鞋面下緣出現了一圈醒目的黃線。|N08|looking closely at a line of yellow stitches along a plain work boot
品牌沿革稱它是沿條車線，外底邊緣則帶著凹槽。|N08|pointing beside the grooved outer edge of an unmarked work boot
鞋後還加了拉環；可這雙新靴，什麼時候才真正下線？|N08,N07|holding the plain unlettered heel loop of an anonymous lace-up boot
我覺得有趣的是，接合的邊界沒有藏起來，反而被亮色劃了出來。|N08|examining a bright stitched boundary against a plain leather upper
到了品牌檔案記下的那一天，一九六〇年四月一日，第一雙靴子下線。|N07|placing a finished plain work boot at the end of a small production bench
格里格斯用這個日期替它取了型號，一四六〇。|N07|holding an anonymous eight-eye style work boot beside a blank product card
新靴用了Airwair這個名字，拉環是黑黃兩色；它會在哪裡見到買家？|N08,N07|studying an anonymous work boot with a plain unlettered two-tone heel loop
下一週，他帶著這款靴子和其他鞋款到展會，準備接夏季生產的訂單。|N07|placing a plain lace-up work boot on an unlettered exhibition counter
它說的是準備接單，夏季工廠還要把訂貨做出來。|N07|opening a blank order folder beside a finished plain work boot
想像你站在展檯前，先看到靴子的輪廓，再看到鞋底邊的一圈線。|N08|an anonymous visitor studying a plain stitched work boot on a small display
鞋面、沿條和底聚成一雙鞋，可它們是怎麼接住彼此的？|N08,N10|examining a plain boot with three simple separate component samples beside it
這圈線連著的沿條，往後會是理解這雙靴子的關鍵。|N10|tracing the strip directly below the upper of an unmarked work boot
但買鞋的人首先碰到的，是這雙靴子能不能陪他工作。|N13|tying a plain work boot while seated beside a simple utility bench
倫敦博物館後來的說明，提到長時間站立的工作穿著者。|N13|an anonymous delivery worker adjusting a plain work boot beside a doorway
館方列舉郵差、警察和工廠工人，這不是一雙只在舞臺上出現的靴子。|N13|an anonymous factory worker standing beside a closed plain tool cabinet
鞋底貼著路面，鞋帶得綁好，外觀先附著在一整天的活動上。|N13|tightening the laces of a plain boot before walking through an open doorway
可是工作結束後，這雙靴子只能留在工廠裡嗎？|N13,N14|an anonymous person stepping outside a plain workshop in work boots
到了六〇年代末，這雙鞋的觀看方式開始變了。|N13,N14|an anonymous young adult inspecting plain work boots in a bedroom mirror
褲腳往上收，鞋面被擦亮，原本在腳下的東西被人刻意露了出來。|N14|an anonymous young adult folding cropped trouser cuffs above plain boots
'''),
('褲腳把鞋邊露了出來', '''
倫敦博物館把光頭族採用這類靴子，放在六〇年代末。|N13|an anonymous short-haired young adult trying on plain lace-up work boots
研究者克魯克在二〇二一年的文章裡，細看了他們怎麼穿。|N14|an anonymous researcher examining a blank clothing study folder
牛仔褲的褲腳被裁短，另一種穿法則把長褲熨得筆挺。|N14|an anonymous young adult pressing a crease into plain trousers
吊帶拉住褲子，腳上那雙靴子的鞋面，還被仔細擦亮。|N14|polishing a plain work boot while seated beside folded trousers
如果你把褲管放長到蓋住鞋面，別人還看得到什麼？|N14|looking at a plain boot partly hidden beneath a long trouser cuff
收短之後，鞋的高度、輪廓和邊緣，便進入整套穿著的視線。|N14|studying the exposed side of plain boots below cropped trousers
在克魯克的分析裡，工作靴可以用來凸顯工人階級的認同。|N14|an anonymous young adult studying their plain work boots in a full-length mirror
我最意外的是，工作留下的物件，到了這裡還得被精心整理。|N14|an anonymous wearer carefully wiping the side of a plain work boot
鞋廠做出的外形，現在有了穿著者自己的安排。|N08,N14|adjusting a cropped trouser cuff while standing in plain work boots
那圈線跟著走上街頭，往後每個穿它的人，都會是同一種身分嗎？|N08,N14|an anonymous wearer stepping onto a plain pavement in stitched work boots
後來不同次文化繼續穿它，館方也把九〇年代的改款列進說明。|N13|an anonymous museum worker examining a plain boot on a simple display support
館裡有一雙製於一九九五年的紫黃格紋靴，外觀已經換了表情。|N13|an anonymous museum worker holding a muted purple and yellow checked lace-up boot
克魯克寫到當代穿法時，提出一個問題：穿上工人風格，就有工人的身分嗎？|N14|an anonymous reader studying a blank essay beside a plain pair of work boots
一個人可以借用這種風格，卻不必真的在工廠工作。|N14|an anonymous student adjusting plain work boots beside a closed notebook
你若只是喜歡那個輪廓，也可能穿上它，替它搭自己的衣服。|N14|an anonymous wearer choosing plain trousers beside a pair of work boots
但不管它被讀成什麼，鞋子仍然得先被製造出來。|N11,N14|an anonymous shoemaker placing an unfinished plain boot upper on a bench
當供貨交給新的工廠，那圈熟悉的邊，能不能照樣做出來？|N11|an anonymous technician inspecting a plain sample boot at a new work station
'''),
('熟悉的接縫走進新工廠', '''
二〇二一年的招股書，把新製造夥伴的導入，寫成一段漫長的工作。|N11|an anonymous technician opening a blank production folder beside a boot sample
公司說，這個過程可能長達一年，才能達到它要求的品質。|N11|an anonymous technician comparing an unfinished boot with a finished sample
一年指的是合作工廠導入，不是一雙靴子在機器上做一年。|N11|an anonymous planner studying a blank schedule beside a sample footwear rack
專用設備、製程和技術知識，都得在這個過程裡接上。|N11|an anonymous technician checking a simple footwear machine beside an unfinished boot
如果你拿到的是熟悉外形、接縫卻完全不同的鞋，還會覺得是同一種嗎？|N11,N12|an anonymous customer comparing the edges of two plain work boot samples
我讀到這段才懂，外觀能重複，不只靠一張產品照片。|N11,N12|an anonymous technician studying a boot sample beside a blank inspection sheet
正式揭露還記下，鞋廠使用的權利，有自有的，也有經授權取得的。|N12|an anonymous archivist sorting two blank agreement folders beside a plain boot
當時的黃線、底紋和刻槽等外觀權利，與品牌名稱的授權分開處理。|N12|an anonymous inspector examining the stitched edge of a plain boot beside blank folders
授權安排也要求提供產品樣品，並接受每年的製造場所檢查。|N12|an anonymous inspector checking a plain sample boot at a tidy factory bench
所以新工廠接手的，不只有外形；可這些部件究竟怎麼合成一雙鞋？|N11,N12,N10|an anonymous technician setting an inspected boot on a plain sample shelf
至於它如何接住鞋底，現在的原廠產品頁給了具體的工序。|N09,N10|an anonymous craftsperson setting a sole and an upper strip on a workbench
公司說，今天多數外底使用一種聚氯乙烯合金，也就是常說的PVC材料。|N09|an anonymous technician holding plain polymer granules above an unmarked mould
顆粒先熔融，再成型為外底，這時鞋面還是另一個部件。|N09,N10|an anonymous technician examining a newly moulded plain sole beside a separate boot upper
它也把Original系列裡的氣穴，說成舒適和吸震的來源。|N09|an anonymous technician holding a simple conceptual sole section with small internal spaces
這是原廠對現行系列的說明，不是把每一款鞋底都畫成密封氣球。|N09|an anonymous technician studying a simple conceptual footwear section on a stand
沿著鞋面往下看，外底還沒接上，為什麼要先縫一條沿條？|N10|an anonymous shoemaker stitching a plain welt strip to a leather boot upper
先把PVC沿條縫上鞋面，外底則還在下一道工序等著。|N10|an anonymous shoemaker holding a welted upper above a separate sole
還記得開場那把高溫熱刀嗎？沿條已縫好，它要碰哪兩個面？|N10|an anonymous technician positioning a guarded hot blade beside two plain footwear components
刀把接合部位加熱，加壓滾輪再將兩個部件壓在一起。|N10|an anonymous technician operating a guarded roller beside a plain sole and welt assembly
等到冷卻，原廠說，這兩個部件便接成了一件PVC。|N10|an anonymous technician examining a cooled plain sole and welt joint on a bench
你看見一圈線，鞋底卻沒有只靠線接住；那是不是還得上一層膠？|N10|an anonymous viewer tracing a stitched welt above the outer sole of a plain boot
產品頁還特別說，這道接底工序沒有使用黏著劑。|N10|an anonymous technician examining a plain heat-joined sole beside a clear work surface
它講的是這個程序，整雙鞋其他部位要另外看。|N10|an anonymous technician turning a finished plain boot to inspect its different components
熱接時的溫度也屬於製造工序，並不是讓你把成鞋拿去承受那種高溫。|N10|an anonymous craftsperson placing a finished boot safely away from an idle guarded tool
這雙鞋從不同材料、不同部件，變成了你能穿著走的一件東西。|N09,N10|an anonymous wearer lifting a finished plain boot from a workshop bench
但穿著會讓各個部位以不同速度老去，連得牢，並沒有讓它們一起磨完。|N16|an anonymous wearer inspecting a worn sole beneath a creased leather upper
底先磨掉、鞋面還好時，那道接縫又會把什麼難題交回來？|N16|an anonymous repairer placing a worn plain boot upside down on a repair bench
'''),
('舊底被拆了下來', '''
二〇二三年的產品說明會裡，主管梅基克談起消費者寄來的要求。|N16|an anonymous product specialist examining a worn plain work boot on a table
她說，有人珍惜自己的舊靴，外底用了二十年磨損，皮鞋面卻還很好。|N16|an anonymous owner touching a creased upper above a heavily worn sole
二十年是她描述的舊靴案例，不是一張保證每雙都能穿這麼久的保單。|N16|an anonymous owner examining a worn boot beside a blank repair enquiry sheet
她另外舉了一位顧客，開兩個半小時車，親自把鞋送到北安普頓的工廠。|N16|an anonymous owner holding a plain boot parcel beside a parked unmarked car
照她的說法，他只是想確定自己最喜歡的鞋，能被正確修理。|N16|an anonymous owner handing an unmarked boot parcel across a factory service counter
要的若只是外形，為何不買雙新鞋就好？|N16|an anonymous owner holding a familiar worn boot beside an empty plain shoe box
如果你已經把一雙鞋穿出自己的折痕，這個要求應該不難理解。|N16|an anonymous wearer tracing the creases on a familiar plain leather boot
我反而會先想，鞋面都還能留，為什麼換一塊底這麼麻煩？|N16,N17|an anonymous repairer studying the joining edge of a worn boot with a puzzled face
梅基克也展示了一隻最近換底的鞋，說它經歷了當年的格拉斯頓伯里音樂節。|N16|an anonymous product specialist showing a repaired boot with a worn leather upper
她讓聽眾看新外底、擦亮而清理好的鞋面；這是保留舊鞋的示範案例。|N16|an anonymous product specialist pointing to the new sole below a creased plain upper
梅基克當時解釋，這種沿條構造，讓傳統修鞋店難以替它換底。|N16|an anonymous cobbler examining a plain welted boot beside ordinary hand tools
她不是在說所有修鞋師都不會修，而是在說品牌需要專門的修復安排。|N16,N17|an anonymous repairer examining a plain boot beside specialised guarded equipment
當時公司說即將推出英國授權維修；可是換底，會只動鞋底嗎？|N16,N18|an anonymous owner placing a plain worn boot into an unmarked shipping box
二〇二六年報則已把修復寫成正在進行的服務。|N17|an anonymous repairer receiving a worn plain boot at a tidy service counter
它列出的這個財年英國修復量，是四千兩百八十七雙。|N17|an anonymous service worker placing a repaired plain boot on a finished work shelf
年報說，多數產品的沿條加熱封構造，可以按原來的材料和方法翻修。|N17|an anonymous repairer comparing a worn boot with replacement plain components
但這需要專門機器和技術，並非把任何新底拿過來貼上。|N17|an anonymous repairer checking a plain boot beside a guarded footwear machine
授權夥伴的經典換底服務，寫明了拆開的範圍。|N18|an anonymous repairer marking the joining edge of a worn plain boot with a blank tag
舊鞋底、沿條和縫線都移走，再用新的部件重新組回來。|N18|an anonymous repairer arranging a removed sole and welt beside a retained leather upper
保留下來的鞋面，要和新部件完成修復，那圈線也只能照舊嗎？|N18|an anonymous repairer setting a retained leather upper beside fresh plain replacement parts
而選擇哪種新底、哪種縫線，也成了送修時可以作的決定。|N18|an anonymous owner selecting one plain replacement sole beside a simple thread spool
年報也記下，二〇二五年十一月，倫敦布魯爾街的新店設了店內維修站。|N17|an anonymous repair specialist receiving a plain boot at an unlettered shop counter
店裡有人能當面提供修復意見，送修的人不必只對著一張網頁猜。|N17|an anonymous repair specialist presenting plain replacement components toward the viewer across a counter
可這樣的拆修，你在任何地方、拿任何一款，都辦得到嗎？|N17,N18|an anonymous owner holding a worn plain boot beside a blank repair service form
不過服務得先符合鞋款和鞋況，並非每一雙都能照同一套辦理。|N17,N18|an anonymous repairer inspecting a worn boot before setting it on a service tray
目前這個授權服務也只接受英國客戶，不能把它當成全球隨送隨修。|N17|an anonymous owner checking a plain repair parcel beside a blank service form
修好一次，材料就沒有後續問題了嗎？|N19|an anonymous technician sorting plain footwear material samples on a clean bench
原廠承認，鞋履由多種材料組成，日後分離與回收仍有難處。|N19|an anonymous technician examining separate plain footwear material samples
修復能把仍可用的部分留久一些，卻沒有自動消除這個材料問題。|N17,N19|an anonymous owner setting a repaired boot beside separated plain material samples
開場那雙舊靴，最終能留下多少，得看這次拆開後，哪些部分還接得回去。|N16,N17,N18|an anonymous repairer examining a retained leather upper above a fresh plain sole
如果你有一雙穿出折痕的鞋，會想保留原來的上半部，還是乾脆換新？留言告訴我。||an anonymous wearer considering a creased plain boot with a thoughtful face toward the viewer
訂閱品牌故事，我們繼續追那些天天碰到、卻很少拆開看的東西。||an anonymous narrator placing a plain boot on a simple workbench
'''),
]

def digest_bytes(value):
    return hashlib.sha256(value).hexdigest()

def digest_file(file):
    return digest_bytes(pathlib.Path(file).read_bytes())

def write_json(file, value):
    pathlib.Path(file).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')

OUT.mkdir(parents=True,exist_ok=True)
for source,target in [('research.md','research-original.md'),('claims.json','research-original.claims.json')]:
    actual=(AUDIT/source).read_bytes()
    target=OUT/target
    if target.exists():
        assert target.read_bytes()==actual, 'Never replace original research bytes'
    else:
        target.write_bytes(actual)

by_module={c['id']:c for c in RESEARCH['new_material_claims']}
by_source={s['id']:s for s in RESEARCH['sources']}
by_excerpt={s['id']:s for s in RESEARCH['short_excerpts']}
scenes=[]
claims=[]
lines=[]
chapters=[]
cameras=['push in','pan left','pull out','tilt down','pan right','tilt up']
sizes=['Medium shot','Close-up','Wide shot','Medium close-up']
lights=['soft overhead workshop light','mild light from an open doorway','gentle desk lamp light','soft overcast light from the left']
places=['at a plain repair bench','in a modest footwear workshop','beside a simple work table','inside a quiet dressing area','at a plain footwear factory station','at an unlettered repair counter']
for ci,(chapter,body) in enumerate(CHAPTERS):
    chapter_lines=[]
    for li,row in enumerate(body.strip().splitlines()):
        text,modules,action=row.split('|')
        modules=[x for x in modules.split(',') if x]
        sid=f'c07r1-{ci+1:02d}-{li+1:02d}'
        lid=f'c7r1{ci+1:02d}{li+1:02d}'
        line={'id':lid,'text':text,'emotion':'說書語氣，對一個人自然講述，問句上揚'}
        if text.startswith('我'):
            line['emotion']='像跟朋友分享發現，語氣有反應'
        pictured_actor_action=('one '+action[3:]) if action.startswith('an ') else 'one anonymous adult '+action
        scene={'id':sid,'template':'shot','data':{'prompt':f'{sizes[(li+ci)%len(sizes)]} {places[ci]}, {pictured_actor_action}, {lights[(li+2*ci)%len(lights)]}.','visual':'still','camera':cameras[(li+ci)%len(cameras)]},'lines':[line]}
        if li==0:
            scene['chapter']=chapter
        scenes.append(scene)
        record={'id':lid,'scene':sid,'text':text,'chapter':chapter,'research_claim_ids':modules}
        source_ids=list(dict.fromkeys(s for m in modules for s in by_module[m]['source_ids']))
        excerpts=list(dict.fromkeys(e for m in modules for e in by_module[m]['excerpt_ids']))
        # Only cite a facsimile or usable original body. Research-only mirrors are not narration support.
        source_ids=[s for s in source_ids if s not in ['DE808095C_HTML','AT217902B_HTML','AT209762B_HTML','T1_made_in_england']]
        record['source_ids']=source_ids
        record['evidence']=[{'source_id':s,'url':by_source[s]['url'],'raw_path':by_source[s]['raw_path'],'raw_sha256':by_source[s]['sha256'],'evidence_level':by_source[s]['evidence_level'],'scope_and_limits':by_source[s]['scope_and_limits']} for s in source_ids]
        record['source_excerpts']=[by_excerpt[e] for e in excerpts]
        if text.startswith(('想像','如果','你若','你想')) or text.startswith('對送修'):
            record['narrative_mode']='viewer_hypothesis_or_editorial_explanation; no claim of a documented individual scene'
        elif text.startswith(('我','今天跟著','它怎麼','可是工作','但不管','所以這圈','這雙鞋從','當一種','對送修')):
            record['narrative_mode']='attributed_editorial_reaction_or_bridge; underlying factual boundaries bound to cited sources'
        elif not modules:
            record['narrative_mode']='viewer_question_or_subscription_invitation; not a factual claim'
        else:
            record['narrative_mode']='source_bound_narration; source assessment still pending independent review'
        record['not_source_pass']=True
        record['written_visual']={'scene':sid,'prompt':scene['data']['prompt'],'mode':'anonymous conceptual illustration; not a historical reconstruction','review_state':'NOT_REVIEWED'}
        claims.append(record)
        lines.append({'id':lid,'text':text})
        chapter_lines.append(lid)
    chapters.append({'title':chapter,'line_ids':chapter_lines})

# The close is one native card with answer, viewer question and subscription invitation.
closing=scenes[-3:]
scenes=scenes[:-3]
last={'id':'c07r1-outro','template':'outro','data':{'title':'一雙鞋，哪些部分值得留下？','cta':'你會想保留原來的鞋面嗎？'},'lines':[line for scene in closing for line in scene['lines']]}
scenes.append(last)
for claim in claims[-3:]:
    claim['scene']=last['id']
    claim['written_visual']={'scene':last['id'],'template':'outro','data':last['data'],'mode':'native closing card; not an illustration purchase','review_state':'NOT_REVIEWED'}

# Every loop points to real ordered narration. Callbacks are not synthetic timestamp gates.
def line_containing(fragment):
    matches=[line['id'] for line in lines if fragment in line['text']]
    assert len(matches)==1, (fragment,matches)
    return matches[0]
LOOP_TEXTS=[
('你想替舊靴換底','舊鞋底、沿條和縫線都移走','舊靴換底到底要動到哪一層'),
('接底熱刀的溫度','刀把接合部位加熱','開場高溫熱刀在接哪兩個部件'),
('有人將褲腳收短','工作靴可以用來凸顯','褲腳收短後，工作靴被讀成什麼'),
('可是鞋底一彎','例如鞋底勾到障礙物','彈性底把什麼負荷交給接縫'),
('那它最容易從哪裡被拉開','例如鞋底勾到障礙物','接縫受到外側拉扯的具體情況'),
('把接合面加寬就夠了嗎','空腔變小','單純加寬接面會犧牲什麼'),
('怎麼讓這兩個要求不打架','加入大致平行的槽或縫','既要接住又要能動的方案'),
('就不會再從別處裂開嗎','這也會拉扯接合面的內緣','接縫內側還會受到什麼負荷'),
('那今天鞋外的凹紋','不能直接拿來認定今天鞋邊每一道紋','專利構想不能直接當商用採納證據'),
('這種塑膠底受得了嗎','作者擔心熱塑性材料被熱破壞','文件對高溫使用提出的材料取捨'),
('當一種鞋底交給另一家鞋廠','一圈醒目的黃線','英國新靴讓接合邊緣有何外觀'),
('這雙新靴，什麼時候','第一雙靴子下線','英國靴下線的日期'),
('它會在哪裡見到買家','下一週，他帶著這款靴子','新靴如何進入展會接單'),
('可它們是怎麼接住彼此的','先把PVC沿條縫上鞋面','沿條如何接到鞋面'),
('這雙靴子只能留在工廠裡嗎','牛仔褲的褲腳被裁短','工作以外誰改變穿著方式'),
('往後每個穿它的人','卻不必真的在工廠工作','工人身分與後來風格有何差別'),
('就有工人的身分嗎','卻不必真的在工廠工作','當代穿著借用的風格與實際職業'),
('那圈熟悉的邊，能不能照樣做出來','可能長達一年','新工廠如何接上熟悉的構造'),
('它要碰哪兩個面','刀把接合部位加熱','沿條縫好之後怎麼和底接合'),
('是不是還得上一層膠','這道接底工序沒有使用黏著劑','原廠這道接底是否靠黏著劑'),
('那道接縫又會把什麼難題交回來','讓傳統修鞋店難以替它換底','鞋面好、底磨壞時的新難題'),
('為什麼換一塊底這麼麻煩','舊鞋底、沿條和縫線都移走','為何換底要拆到沿條和縫線'),
('換底，會只動鞋底嗎','舊鞋底、沿條和縫線都移走','授權服務的實際拆除範圍'),
('那圈線也只能照舊嗎','哪種新底、哪種縫線','修復時能選哪些接合外觀'),
('任何地方、拿任何一款','目前這個授權服務也只接受英國客戶','專業維修仍受鞋況與服務地域限制'),
('材料就沒有後續問題了嗎','日後分離與回收仍有難處','修復仍沒有消除的材料限制'),
]
LOOPS=[(line_containing(a),line_containing(b),what) for a,b,what in LOOP_TEXTS]
known=[x['id'] for x in lines]
for setup,payoff,what in LOOPS:
    assert setup in known and payoff in known and known.index(setup)<known.index(payoff), (setup,payoff)

doc=copy.deepcopy(json.loads((REPO/'docs/videos/brand-story-remakes-20261025/c06/video.json').read_text()))
doc['slug']=SLUG
doc['category']='story'
doc['voice']['performance']='跟著一雙靴子的接縫，向一個人說它怎麼被做出、被看見、被拆修。回顧保留歸屬，示意不演成歷史原件。'
doc['loops']=[{'setup':a,'payoff':b,'what':c} for a,b,c in LOOPS]
doc['scenes']=scenes
used=list(dict.fromkeys(s for row in claims for s in row['source_ids']))
doc['sources']=[{'title':by_source[s]['title'],'url':by_source[s]['url'],'checked_on':'2026-10-25'} for s in used]
doc['youtube']={'category_id':27,'made_for_kids':False,'default_language':'zh-TW','title':TITLE,
 'description':'一雙工作靴的接縫，怎麼走到街頭，又成為維修時必須拆開的地方？循著品牌回顧、1957申請的美國專利原件、倫敦博物館實物、研究者的穿法分析、正式揭露與現行授權換底服務，看鞋面、沿條與外底如何相接。原廠現行熱接程序不倒寫成1960工法；專利方案不冒充商用採納證據；圖像為匿名概念插圖。\n\n原件來源（查閱2026-10-25）\n'+'\n'.join(by_source[s]['title']+'\n'+by_source[s]['url'] for s in used),
 'tags':['Dr. Martens','馬汀靴','品牌故事','工作靴','日用品的意外轉身','鞋底','維修','青年文化'],'video_id':None}
doc['thumbnail']={'template':'thumb','data':{'layout':'d','headline':'換底得拆線？','sub':'接底熱刀逾650度','brand':'DR. MARTENS','tag':'品牌故事','shot':'c07r1-01-08'}}
doc['assets']=[]
write_json(OUT/'video.json',doc)
write_json(OUT/'narration-only.json',{'slug':SLUG,'scope':'new author narration only; no verdict or source notes','chapters':chapters,'lines':lines})
names=['Dr. Martens','Dr Martens','DR. MARTENS','馬汀靴','馬汀斯','Maertens','Klaus Maertens','馮克','Herbert Funck','Funck','格里格斯','Griggs','Bill Griggs','1460','一四六〇','Airwair','AIRWAIR','Original','PVC','London Museum','倫敦博物館','Arthur Crucq','Crucq','克魯克','Tuze Mekik','梅基克','Goodyear','The Boot Repair Company','Northampton','北安普頓','Brewer Street','布魯爾街','Glastonbury','格拉斯頓伯里']
series={'kind':'story','slug':'brand-stories-everyday-reversals','episode':7,'chapter':1,'title':TITLE,'logline':'沿著一雙靴子的接縫，從軟底的接合難題，到英國工作靴被穿出文化意義，再到現行製程與專業拆接的維修取捨。','names':names,'characters':[],'visual_tier':'stills','compilation':False,'target_minutes':13,'image_model':'image-01','look':{'preset':'cute-mystery'}}
write_json(OUT/'series.json',series)
brief='''# C07 馬汀靴｜接縫走過的六十多年

## 問題

一雙馬汀靴的接縫，如何從撐住鞋面的地方，走到穿著者願意保留舊鞋面、為它尋找專業維修的地方？

## 一句答案

鞋廠把連接處做成可辨識的外形，穿著者讓它進入自己的風格；當底先磨耗，沿條與熱接的構造又決定要由誰、拆開哪些部分，才能讓仍可用的鞋面繼續使用。

## 站主觀點

跟著鞋邊同一個接合問題推進，不把品牌史念成年代清單。工作用途、穿法、工廠複製和拆修，都只透過這雙靴子的外形與連接部位進來；不讓文化章或授權章擴成另一支片。以原件和歸屬處理已知界線，不讓查核警語占滿旁白。

### 選項 A：一條接縫，從工作靴走到維修檯

一行說明：從軟底牽動接縫的難題，追到鞋邊被人露出、被工廠重複製造，最後在舊靴上被拆開。

開場鉤子：你想替舊靴換底，面前卻是一道原廠說以高溫熱刀接合的邊；鞋面還能留下時，該從哪裡拆？

目標13分鐘；真正旁白正文需實測12–14分鐘，文字units和估時不當完成驗收。自然每秒4–5 units，不以停頓、慢播、重述或免責段湊長。

## 製作規格

MiniMax image-01，look只用cute-mystery；匿名概念插圖，不要求重建原型、專利商用布局、歷史工廠或真人。正文實際插畫時間至少70%，最多連續3卡。繁中燒錄與CC；濃縮後5秒片頭、21秒正式v4片尾需待正式素材身分驗收。縮圖layout d，品牌名、大黃字黑框、短白副標。預設英日韓西葡印尼越泰八語，中文稿通過後才做新稿文字，不宣稱配音、SRT或後台選項已套用。

## 來源界線

1945/1947/1959是明確歸因的企業後來回顧；US3046679是1957申請、1962核准的接合方案，未證格里格斯商用採納；1960下線與下一週展會分開。當代原廠熱接不倒寫1960，工序溫度不當耐熱性能。文化分析保留研究者與特定群體，不由鞋推每人職業或政治。2021權利和導入披露不冒充1959契約或今日供應鏈。20年為2023具名主管描述案例，不作每雙壽命；當前英國授權維修受鞋款鞋況地域限制，無全球保固宣稱。
'''
(OUT/'brief.md').write_text(brief)

claim_doc={'schema_version':1,'episode':'C07 Dr. Martens remake r1','status':'AUTHOR_CANDIDATE_PENDING_INDEPENDENT_SOURCE_WRITTEN_VISUAL_AND_TWO_READERS','research_original_sha256':{'research-original.md':digest_file(OUT/'research-original.md'),'research-original.claims.json':digest_file(OUT/'research-original.claims.json')},'original_inputs':RESEARCH['original_inputs'],'source_inventory':[by_source[s] for s in used],'narration_claims':claims,'paid_calls':0,'backend_actions':0,'actual_runtime_verified':False,'source_pass_issued':False,'owner_approval_issued':False}
write_json(OUT/'claims.json',claim_doc)
md=['# C07 r1｜作者逐句來源與書面分鏡索引','','此檔是作者主張表，未經獨立來源或書面配鏡驗收；不作SOURCE PASS、verify、站主或實際時長批准。','','## 研究保全','','- 原研究Markdown SHA '+claim_doc['research_original_sha256']['research-original.md'],'- 原研究JSON SHA '+claim_doc['research_original_sha256']['research-original.claims.json'],'','## 使用來源','']
for s in used:
    source=by_source[s]
    md += [f"- {s}: [{source['title']}]({source['url']})；{source['evidence_level']}；actual raw SHA `{source['sha256']}`。"]
md += ['','## 逐句索引','','| ID | 旁白 | 原研究claim | 原件 |','|---|---|---|---|']
for r in claims:
    md.append('| '+r['id']+' | '+r['text'].replace('|','／')+' | '+','.join(r['research_claim_ids'])+' | '+','.join(r['source_ids'])+' |')
md += ['','書面配鏡與每句實際快取SHA、來源層級、短原摘錄、禁止推論保留在claims.json；匿名動作是概念示意，不冒充有紀錄個人。unused早期Google專利轉錄未進新旁白。','']
(OUT/'claims.md').write_text('\n'.join(md))
script=['# '+TITLE,'','作者附來源稿；後台canonical screenplay須由官方writeScreenplay另行產生。此稿未核准。','']
for title,body in CHAPTERS:
    script+=['## '+title,'']
    for r in claims:
        if r['chapter']==title:
            script += [f"[{r['id']}] {r['text']}",f"來源：{', '.join(r['source_ids']) or '觀眾問題／訂閱邀請'}；原研究：{', '.join(r['research_claim_ids']) or '無事實主張'}",'']
(OUT/'script.md').write_text('\n'.join(script)+'\n')

notes={'schema_version':1,'revision':'C07 r1','status':'HOLD_PENDING_INDEPENDENT_SOURCE_AND_TWO_NEW_ISOLATED_READERS','author':'/root/c07_author','source_commit':'2b20c30d359fe5d93a4ea66f013a52fa20a35c05','new_slug':SLUG,'old_episode_not_rebound':True,'research_original_sha256':claim_doc['research_original_sha256'],'source_files_sha256':{f:digest_file(OUT/f) for f in ['video.json','script.md','narration-only.json','claims.json','claims.md','brief.md','series.json']},'counts':{'narration_lines':len(lines),'scenes':len(scenes),'illustration_shots':sum(s['template']=='shot' for s in scenes),'chapters':len(chapters),'loops':len(LOOPS)},'actual_audio_measured':False,'source_pass_issued':False,'written_visual_pass_issued':False,'native_narrative_pass_issued':False,'owner_approval_issued':False,'translations_written':False,'paid_calls':0,'backend_actions':0,'branding_scope':'5 second intro after condensation and 21 second formal-v4 outro are requirements, no selected bytes asserted','voice_scope':'native STORY_VOICE_STYLE copied exact; dictionary terms/speech have not been audibly reviewed','narrative_scope':'one recurring structural boundary; old prototype, present original-family boot and repair examples are not falsely one physically surviving object','mechanical_lint':'PENDING_NATIVE_INITIALIZED_CONTEXT'}
write_json(OUT/'author-notes.json',notes)
print(json.dumps(notes['counts'],ensure_ascii=False))
