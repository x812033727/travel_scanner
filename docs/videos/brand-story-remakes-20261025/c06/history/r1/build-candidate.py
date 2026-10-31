#!/usr/bin/env python3
"""Author's deterministic C06 candidate; never calls providers or creates approvals."""
import hashlib
import json
import re
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
SLUG = 'story-everyday-play-doh-c06-remake-20261025'
DATE = '2026-10-25'
RESEARCH = json.loads((HERE / 'research-original.claims.json').read_text())
SOURCES = {s['id']: s for s in RESEARCH['sources']}
ROOT = HERE.parents[3]
STORY_VOICE_STYLE = subprocess.check_output(['node','--input-type=module','-e',"import {STORY_VOICE_STYLE} from './tools/video/automation/register.mjs'; console.log(STORY_VOICE_STYLE);"],cwd=ROOT,text=True).strip()
CHAPTERS = [
    ('h', '一罐材料，誰決定它的工作？'),
    ('o', '牆面不再需要它'),
    ('k', '老師換了一張工作桌'),
    ('t', '軟之外，還要做到什麼？'),
    ('b', '玩具離開，清潔公司留下'),
    ('n', '這次，完成後請別揉掉'),
]

# Each row is a scene: chapter, source anchors, kind, anonymous illustrated action,
# then exact spoken lines. HYP/OPINION/Q are editorial, not new historical evidence.
ROWS = [
('h','H1','mixed','opening a plain pot of soft modeling dough',
 '你打開一罐黏土，想要的是揉壞還能重來；但這個要求，會不會把一款清潔用品變成大生意？',
 '孩之寶在二〇二四年宣布，Play-Doh每年出貨超過五億罐。'),
('h','K1','hypothetical','holding a lump of pale dough beside a smudged wallpaper sample',
 '想像你正捏著這團軟材料，旁邊卻放著沾了煤灰的壁紙。它最早的工作，竟然是擦牆。',
 '你把它壓扁、再揉起來；同樣的動作，在清潔桌前，卻是為了帶走髒污。'),
('h','K1,P1','mixed','comparing a blank classroom tray with a closed document folder',
 '我覺得真正有意思的，是一位老師把它帶進教室，後來的專利又要求它做到軟以外的事。'),
('h','H1,K1','question','presenting a small dough lump at a worktable',
 '今天跟著Play-Doh，從擦牆膏走到一年數億罐的玩具，看材料如何換工作。',
 '使用的人變了，為什麼連顏色、工具，和做完之後要不要留下來，都得跟著變？'),

('o','K1','history','examining a plain cleaning tin at a small shop counter',
 '先把這團材料放回清潔用品的世界。依Kutol自己的回顧，這家公司一九一二年起於路易維爾，後來搬到辛辛那提。'),
('o','K1,M1','history','placing a closed cleaning tin beside a blank sales folder',
 '沒想到，原本被派去清算公司的克里奧・麥克維克，反而買下了生意；他還接到克羅格的壁紙清潔用品訂單。',
 '博物館說，公司那時還沒做過壁紙清潔材料；接下訂單，靠誰把它做出來？'),
('o','M1','attributed','holding a plain lump against a wallpaper panel',
 '史壯玩具博物館後來把這筆生意放在一九三三年，並說他的兄弟諾亞負責開發配方。'),
('o','M1','question','looking from a smudged wallpaper panel to a plain cleaning lump',
 '你若站在那面牆前，會先問它捏起來好不好玩嗎？當然不會；你要知道，牆上的髒污能不能拿掉。'),
('o','M1','hypothetical','pressing a pale cleaning lump onto a small dark smudge on a wallpaper sample',
 '想像你把一團清潔材料壓向煤灰沾過的壁紙；在這個工作裡，材料的價值跟牆上有什麼，緊緊連在一起。',
 '你的視線落在牆面，手裡的形狀只是過程；擦完以後，不需要有人欣賞它剛才被揉成什麼樣子。'),
('o','M1','question','studying a cleaner wallpaper sample beside an unused lump',
 '但如果家裡的牆，沒有以前那麼容易沾上煤灰了呢？同一團材料，還有多少機會被你拿出來？'),
('o','M1','attributed','looking at a simple closed domestic heating unit beside a wall',
 '沒想到，原來的髒污會變少。館方說，一九五〇年代初，家庭從燒煤轉向燃油或天然氣，煤灰少了，壁紙清潔用品的需求也下滑。'),
('o','M1','opinion','setting an unused cleaning lump beside an open storage box',
 '我覺得這個困境很具體：它原本要清的東西變少了，光把原來的工作做得更熟練，未必找得回客人。'),
('o','M1','attributed','holding a blank family business folder at a small desk',
 '依同一篇回顧，克里奧一九四九年去世後，兒子約瑟夫接手；到了這時候，生意得找新的出口。'),
('o','M1,K1','question','turning a plain lump between both hands at a workshop table',
 '如果是你接住這團材料，你會繼續找需要擦牆的人，還是找一雙根本不打算擦牆的手？'),
('o','K1','history','setting a small tray of soft dough on an empty classroom desk',
 'Kutol的公司史給了第二種答案：約瑟夫的姻親、老師凱・祖法爾，把壁紙清潔材料帶進了幼稚園。'),
('o','K1','opinion','looking with curiosity at a small modeled dough animal on a tray',
 '我喜歡這個轉向：新的使用者沒有要求把牆擦得更乾淨，反而開始在桌面上，把材料捏成別的東西。',
 '原本擦完就收起來的材料，現在，桌上的形狀成了要看的成果；同一雙手，開始為不同的結果忙。'),

('k','M2','attributed','pressing a small thumb into a firm clay lump on a classroom tray',
 '玩具名人堂的回顧說，凱發現孩子平常用的塑形黏土太硬，不容易操作；約瑟夫於是送材料給她試。'),
('k','M2','hypothetical','gently shaping a pliable lump on a child sized desk',
 '想像你想捏隻小動物，手卻被硬塊難住；身體壓不出來，耳朵要怎麼接？',
 '換成容易推動的材料，你才能先壓出身體，再加一對耳朵；孩子的作品，也才有往下做的空間。'),
('k','M1','attributed','examining a tray with a few simple dough figures',
 '博物館的故事接著說，約瑟夫到學校看見孩子捏的東西；後來，團隊利用原有設備和空間，把材料往玩具方向調整。'),
('k','M1','opinion','holding a simple dough figure beside a cleaning lump',
 '我覺得到學校這一步很具體，作品已經擺在桌上；但要送進更多教室，接下來由誰來做玩具生意？'),
('k','H2,M1','history','placing a plain toy tub on a shop shelf',
 '孩之寶把品牌的誕生放在一九五六年；館方也把Rainbow Crafts的成立，和向辛辛那提小學推廣，放在這一年。'),
('k','H2,M1','question','holding a pale dough lump beside three closed color pots',
 '可是，從清潔用品換成玩具，只換罐子就夠了嗎？如果你要捏的東西各有顏色，灰白的一團能滿足你嗎？'),
('k','M1,M2','attributed','choosing between red yellow and blue dough lumps on a tray',
 '館方把一九五七年的變化寫得很明白：紅、黃、藍加入了產品，名人堂還提到材料變得更柔軟。'),
('k','M1,M2','hypothetical','placing a yellow dough beak on a plain small dough bird',
 '想像你替小鳥加一個嘴巴；現在，你可以挑顏色，把它和身體分開，作品的選擇也跟著多了一步。'),
('k','M1,M2','opinion','looking at a small multicolored dough figure',
 '我喜歡這一筆，因為顏色在這張桌上有工作：它讓你選擇作品長什麼樣，和清潔牆面的要求已經不同。'),
('k','M2','question','carrying a plain closed toy case toward a blank display stand',
 '接下來是另一道門檻：教室裡有人願意玩，教室外的人，怎麼知道這罐東西可以拿來玩？'),
('k','M2','attributed','placing plain modeling dough tubs on a simple exhibition table',
 '名人堂的歷史還列出教育用品展、梅西和馬歇爾菲爾德百貨；在教室以外，多了讓人接觸和購買的地方。'),
('k','M1','attributed','watching a blank television screen beside a plain dough tub',
 '更麻煩的是，依博物館的回顧，約瑟夫缺乏大筆廣告預算；他卻和兒童節目《袋鼠船長》的主持人安排，至少每週用一次產品。',
 '對電視前的你來說，看到一隻手把軟材料變成形狀，和只在貨架上看見一罐包裝，是不同的認識方式。'),
('k','M1,M2','opinion','presenting a small finished dough animal toward the viewer',
 '對我來說，展台、貨架和電視，各自把同一件事搬給更多人看：一團軟材料，可以經過你的手變成作品。'),
('k','P1,M1','question','holding a completed dough shape beside a second loose lump',
 '不過，你剛捏好一個形狀，放下去卻黏住桌面，或沒多久就硬掉，下一次還想拿它出來嗎？'),

('t','M1','attributed','pressing the handle of a simple tabletop dough extruder',
 '一個手柄壓下去，軟材料就能擠成不同形狀；博物館把Fun Factory這個工具的推出，放在一九六〇年。'),
('t','M1','hypothetical','holding a narrow strand of dough over a tray',
 '如果你想做一把細長的頭髮，每根都慢慢搓，有沒有別的動作，能替你把材料做成長條？',
 '想像你先放進一團，接著施力，看材料從出口冒出來；你不必用手指一段一段，把同樣的截面重做一遍。'),
('t','M1','opinion','examining a small extruded dough shape beside a simple lever tool',
 '我覺得這個工具的巧處，在於它把作品的難題搬了一部分到開口上，讓你用按壓換取不同的形狀。'),
('t','P1','question','looking between a dough lump and a blank patent folder',
 '可是，工具可以幫你擠形狀，材料本身呢？它要一邊聽手的話，一邊留下形狀，這兩件事怎麼兼顧？'),
('t','P1','patent','opening a blank document folder beside a small plain dough lump',
 '這裡有一份後來核發的美國專利：諾亞和約瑟夫列名發明人，一九六〇年五月申請，一九六五年一月核發。',
 '文件裡，先要照顧你哪個動作？'),
('t','P1','patent','holding a blank patent page at a worktable',
 '它寫的是兒童玩耍用塑形材料，權利轉讓給Rainbow Crafts。'),
('t','P1','patent','folding a pliable lump of modeling dough on a tray',
 '文件先要求材料柔軟、可塑，而且乾得慢，可以反覆塑形；做出一個東西，不必就把下一次的玩法用完。'),
('t','P1','hypothetical','flattening a small dough animal back into a plain lump',
 '想像你把剛捏的小動物揉回一團，再改做一艘船；如果材料已經變硬，這次改主意就得停下來。',
 '所以，反覆塑形不是要你每次都做成功；它把推翻剛才那個形狀，也留在遊戲能做的事情裡。'),
('t','P1','question','lifting a small dough shape from a plain tabletop',
 '但把乾燥放慢，就什麼都解決了嗎？你把作品拿起來時，會不會連桌面都黏著，手上也沾得一塌糊塗？'),
('t','P1','patent','holding a clean lifted dough lump above a work tray',
 '所以，專利還把乾淨、不黏手、不沾染列進目標。它關心的已經包含你捏完後，材料怎麼離開手和桌面。',
 '你若想把一小塊接到另一塊上，材料要配合；等到你抬手離開，又不希望所有東西都跟著走。'),
('t','P1','question','holding a soft lump above a simplified model of small coated particles',
 '材料要黏成一團，又不要黏住你的手；專利作者怎麼解釋，這兩件事為什麼能一起做到？'),
('t','P1','patent_hypothesis','examining a simplified cross section model of a soft lump with tiny coated particles',
 '他們認為，烴類餾分會在固體顆粒外面形成薄膜，讓材料柔軟；文件也把滑順、不黏的觸感，連到這層包覆。',
 '文件接著描述，包覆的麵粉顆粒經濕熱糊化，形成柔軟而均勻的一團，而不要結出不想要的塊。'),
('t','P1','opinion','comparing a plain soft lump with a simple model of a coated particle',
 '我覺得有趣的是，你只要一句「手感不對」，專利的解釋卻得往裡走：顆粒怎麼合成一團，表面又怎麼碰到你的手。'),
('t','P1','opinion','comparing a shaped lump on a tray with a hand held loose lump',
 '我覺得這裡有個拉扯：你要推得動它，也希望放下去還看得出形狀，材料只要越軟越好嗎？',
 '專利的主張，同時要它容易塑形、能保留形狀；你施力改它，放下後又希望作品還站得住。'),
('t','P1','question','choosing a colored dough lump beside a plain lump',
 '還記得前面挑顏色的那隻小鳥嗎？如果漂亮的顏色讓材料變得難捏，這個選擇還算增加玩法嗎？'),
('t','P1','patent','pressing a small colored lump into a simple shape on a tray',
 '這份專利也處理了這個要求：可以加上顏色，又不妨礙可塑性。顏色和手感，要一起把工作做完。'),
('t','P1','patent','examining separate plain ingredient bowls beside a closed folder',
 '但文件中的材料，是靠什麼組成的？它列出植物麵粉、水、烴類餾分和鹽類，也談到著色等添加物。這不是早年擦牆膏的配方表。'),
('t','P1,H5','mixed','holding a plain modern dough pot beside a small wheat stalk bundle',
 '今天，孩之寶對一款經典組合說，主要成分是小麥、水和鹽；兩份資料各有自己的產品範圍，不能直接畫上等號。'),
('t','P1','question','holding a plain lid above an open modeling dough pot',
 '回到你開場打開的那罐材料，還有一個動作沒做：玩完以後，你要把它放到哪裡，才有機會下次接著玩？'),
('t','P1','patent','placing a soft dough lump inside a plain airtight pot',
 '這份專利在描述材料特性時，寫到平常放在密閉容器，玩過後也能放回去；如果充分乾硬，就不能再揉回原來的狀態。'),
('t','P1','hypothetical','closing the lid of a plain modeling dough pot beside an unfinished shape',
 '想像你今天只做到船身，決定明天再想帆怎麼做；你收起材料，是要替下一次改主意，留下還能動手的機會。',
 '我覺得這個蓋罐子的動作很關鍵：材料在做，使用的人也得配合，遊戲才有下一回。'),
('t','P1,H5','opinion','looking from a closed modern dough tub to a blank patent folder',
 '沒想到，文件也留了另一種結局：材料放在空氣中幾天會乾硬，乾硬後可以上色。你得先想，眼前這件要留著，還是這團要留著再玩？'),
('t','M1,K1','question','placing a plain toy tub beside a closed cleaning tin',
 '工具和材料都有了新工作，那麼原來的清潔公司呢？玩具賣出去以後，Kutol也整家離開清潔生意了嗎？'),

('b','M1,K1','history','moving a plain toy tub away from a separate cleaning tin on a desk',
 '館方把Rainbow Crafts售予通用磨坊放在一九六五年；Kutol公司史也說，做玩具的子公司後來賣掉了。'),
('b','K1','history','setting a plain liquid soap dispenser on a washroom counter',
 '留下來的公司，還能替你做什麼？依Kutol的回顧，比爾・羅登堡後來把重心轉向液體皂、乳液和給皂設備。'),
('b','K1','opinion','looking between a plain soap dispenser and a small dough tub',
 '我覺得這裡很容易看錯：玩具品牌離開，並不等於整家清潔公司被買走；同一段起點，分出了不同的工作。'),
('b','K1,M1','hypothetical','holding a plain soap dispenser at a sink',
 '你若站在洗手台前，需要的是把清潔用品按出來；你若坐到玩具桌前，需要的又是另一種手上動作。'),
('b','H4','question','examining a plain lever tool with two simple removable shape rails',
 '我們回到桌面，看看現在官網列的一款Fun Factory：想換一種形狀，你還需要把整個工具換掉嗎？'),
('b','H4','product','inserting a small shape rail into a plain tabletop dough extruder',
 '這款產品讓你放入材料，從兩條造型軌選一條，選好開口，再壓下手柄，把形狀擠出來。',
 '想像你拿擠出的長條，放到作品旁當一道邊框；工具提供一段形狀，接著擺在哪裡，仍然由你決定。'),
('b','H4','opinion','holding a removable shape rail beside a plain dough extruder',
 '我喜歡它把選擇留在你面前：換開口，手還是做按壓的動作，眼前得到的形狀卻可以改變。'),
('b','H4,H1','question','placing a simple dough tool beside a closed craft kit box',
 '可是，如果你這次要做的作品，想放久一點呢？反覆揉回去的玩法，會不會遇到另一種期待？'),
('b','H1','announcement','holding a plain craft kit box beside a small unfinished clay bowl',
 '二〇二四年，孩之寶宣布一項授權合作，規劃從二〇二五年起推出風乾黏土、手作套件和其他塑形材料。',
 '如果你挑的是風乾作品，完成後等待材料變乾，就可能是做完它的一部分；這和隨時準備揉回去，有不同的終點。'),
('b','H1','announcement','examining a small clay project beside a closed blank product folder',
 '都放在同一品牌底下，裡面材料就相同嗎？這則公告列的是不同材料的產品計畫，沒有說每一罐經典黏土都跟著換了配方。'),
('b','H1','opinion','looking at a small unfinished clay bowl on a craft table',
 '我看到的是另一個方向：作品不一定都要回到原來那一團。你做完後打算怎麼處理，也能變成產品問題。'),
('b','H3','question','holding a single soft modeled flower above a plain vase',
 '如果成品是一朵你想插進花瓶的花，你還願意隔天把它揉掉嗎？這一次，品牌真的把作品交給了另一群人。'),

('n','H3','announcement','opening a plain flower crafting kit at an adult worktable',
 '二〇二六年七月，孩之寶介紹一款成人花藝系列，稱這是品牌第一個專門為成人設計的系列。'),
('n','H3','opinion','holding a small modeled flower with a curious expression',
 '我覺得有趣的是，成人這次成了設計對象；你拿到的套件，會怎樣帶你做出一束花？'),
('n','H3','product','shaping a soft petal with a small plain molding tool',
 '官方介紹讓使用者做花瓣、組花，再排成花束；套件包含塑形材料、工具、模具、花瓶，以及最後處理用的噴霧。',
 '公司還提供每款套件的教學影片。你要從一片花瓣走到整束花，途中怎麼做，也跟著產品一起被安排。'),
('n','H3','hypothetical','placing a completed modeled flower into a plain vase',
 '想像你選好花瓣，慢慢排好位置，把花放進瓶子；如果這就是你想擺在桌上的成品，放進花瓶就做完了嗎？'),
('n','H3,P1','question','looking at a finished modeled flower beside a plain spray bottle',
 '前面把材料放回罐子，是替下一次揉捏留下機會；這束要展示的花，最後一步卻朝另一個方向走。'),
('n','H3','attributed','holding a plain finishing spray beside a modeled flower arrangement',
 '孩之寶說，這款特製的最後處理噴霧，可以幫花朵維持結構數月；這是公司對這款產品的說明。'),
('n','H3,P1','opinion','studying a modeled flower arrangement beside a loose dough lump',
 '我喜歡這個對照：前面，材料要讓你反覆改主意；這裡，最後一步卻幫你保留已經做好的決定。'),
('n','H3','announcement','holding a plain flower crafting kit box beside an unmarked shop shelf',
 '想找這款套件，公告列了哪些地方？依這則七月公告，當時列出的通路有亞馬遜、塔吉特和沃爾瑪。'),
('n','H3','opinion','looking at a finished flower arrangement on a personal desk',
 '你把它擺進生活裡，算不算讓材料又多了一份工作？我覺得，創作結束了，這束花的工作才剛開始。'),
('n','K1,M1,P1,H3','opinion','holding a plain dough lump beside a simple flower arrangement',
 '回到開場那罐材料，我的答案是：使用者換了，要完成的動作也跟著換；容易下手、能重捏、選形狀，到完成後保存，都得有人把它做出來。'),
]

LOOPS = [
 ('h04','n10','使用者變了，材料的工作怎樣改變'),
 ('o06','o07','牆面較少煤灰後原工作為何縮小'),
 ('o10','o11','清潔需求下降後另一雙手在哪裡'),
 ('k06','k07','從清潔用品變玩具顏色怎樣改變'),
 ('k10','k11','教室外的人怎麼看見玩法'),
 ('k14','t07','材料乾硬後怎樣繼續改作品'),
 ('t04','t07','材料要回應哪些塑形要求'),
 ('t09','t10','作品拿起來時黏手黏桌的要求'),
 ('t11','t12','專利作者怎樣解釋柔軟與不黏同時成立'),
 ('t15','t16','顏色會不會妨礙可塑性'),
 ('t19','t20','玩完以後怎樣保留再玩的機會'),
 ('t23','b02','玩具賣掉之後清潔公司往哪裡走'),
 ('b05','b06','現在一款工具怎樣換形狀'),
 ('b08','b09','想保留作品時另一種材料方向'),
 ('b12','n03','成人花藝產品提供哪些動作與工具'),
 ('n04','n06','花做好後靠什麼保存結構'),
]

def dump(name, value):
    (HERE/name).write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n')

def units(text):
    tokens = re.findall(r"[A-Za-z][A-Za-z0-9.+#'_-]*|[0-9][0-9.,:/%]*|[\u3040-\u30ff\u3400-\u9fff\uf900-\ufaff\uac00-\ud7af]", text)
    return sum(1 if re.match(r'[\u3040-\u30ff\u3400-\u9fff\uf900-\ufaff\uac00-\ud7af]', t) else 2 for t in tokens)

def split_for_speech(text):
    if units(text)<=36: return [text]
    parts=re.findall(r'.+?[，；。？！：]|.+$',text)
    result=[]; current=''
    for part in parts:
        if current and units(current+part)>36:
            result.append(current); current=''
        current+=part
        if part.endswith(('？','?')):
            result.append(current); current=''
    if current: result.append(current)
    assert ''.join(result)==text
    return result

def evidence_for(source_id,short):
    s=SOURCES[source_id]
    locator=s['locator']; scope=s['limits']
    if source_id=='P1':
        if short in ['t05','t06']:
            locator='原PDF1標頭及文首：發明人、assignors、Filed May17,1960、Patented Jan26,1965、兒童用途。'
        elif short in ['t07','t08','t09','t10']:
            locator='原PDF1文首objects：slow drying、re-worked/re-molded、cleanliness、notsticky、non-staining。'
        elif short in ['t11','t12','t13']:
            locator='原PDF1印刷欄2：It is believed薄膜包覆段；其後coated flour particles／gelatinize及thin film／notsticky段。GooglePatents description369–370。'
            scope='專利作者提出的機制解釋；保留認為/文件描述，不是本稿的獨立實驗結果，也不套到1933或現代全部產品。'
        elif short=='t14':
            locator='原件claim8：moldable into any desired shape／consistency to retain its shape；特性段soft,pliable。'
        elif short in ['t15','t16']:
            locator='原PDF1 objects：different colors may be incorporated without affecting its moldable consistency。'
        elif short in ['t17','t18']:
            locator='原PDF1 generally described composition：vegetable flour、water、hydrocarbon distillate、soluble saline extender；optional perfume/color。'
        elif short in ['t19','t20','t21','t22','n05']:
            locator='原件末段characteristics：open air／dry hard／once thoroughly dry not reclaimed／painted；normally stored in an air tight container／returned after play。GooglePatents description498–500。'
            scope='核發文本對該組成的描述與主張，非本次性能測試；不讀保存年限或化學配方延續性。'
    if source_id=='M1' and short=='o02': locator='正文1933：Although they had never made wallpaper cleaner before，及Noah product developer段。'
    if source_id=='M1' and short=='k12': locator='正文1956/1957後段：缺廣告預算、Keeshan／Captain Kangaroo至少每週一次的安排；保留館方回顧歸屬。'
    if source_id=='H3' and short=='n08': locator='2026-07-09公告Starting at段，當時now available於Amazon／Target／Walmart；非全球各地庫存承諾。'
    return {'source_id':source_id,'url':s['url'],'locator':locator,'scope':scope,'research_raw_sha256':s['raw_sha256']}

def main():
    counters={k:0 for k,_ in CHAPTERS}
    scenes=[]; narration=[]; claims=[]; index={}; visual=[]
    cameras=['push in','pan left','pull out','tilt down','pan right','tilt up']
    lights=['soft window light from the left','mild overcast window light','gentle desk lamp light from the right','soft doorway light']
    sizes=['Close-up','Medium shot','Medium close-up','Wide shot']
    for i,(ch,refs,kind,action,*lines) in enumerate(ROWS):
        lines=[segment for text in lines for segment in split_for_speech(text)]
        counters[ch]+=1; short=f'{ch}{counters[ch]:02d}'; sid=f'c06r-{short}'
        lids=[f'c06r{short}{j+1}' for j in range(len(lines))]; index[short]=lids
        locations={'h':'at a kitchen table','o':'inside a small cleaning-supply shop','k':'inside a classroom craft corner','t':'inside a playroom','b':'at a small product display','n':'at a home crafting corner'}
        place=locations[ch]
        for needles,location in [(['wallpaper'],'beside a freestanding wallpaper panel'),(['soap','washroom'],'beside a washroom sink'),(['television'],'in a living room'),(['exhibition'],'at a small exhibition stand'),(['patent','folder'],'at a document reading desk'),(['extruder','rail'],'inside a playroom'),(['flower','vase','petal'],'at a home crafting corner')]:
            if any(n in action for n in needles): place=location
        groups=[]; current=[]
        for pair in zip(lids,lines):
            if current and sum(units(x[1]) for x in current)+units(pair[1])>38:
                groups.append(current); current=[]
            current.append(pair)
        if current: groups.append(current)
        for j,group in enumerate(groups):
            part_id=sid if j==0 else sid+chr(ord('a')+j)
            k=len(scenes)
            person=['one anonymous adult facing the viewer','one curious person looking toward the viewer','one focused hobbyist with a thoughtful expression','one unidentified craftsperson with a puzzled expression'][k%4]
            prompt=f'{sizes[k%len(sizes)]} {place}, {person} while {action}, {lights[k%len(lights)]}.'
            scene={'id':part_id,'template':'shot','data':{'prompt':prompt,'visual':'still','camera':cameras[k%len(cameras)]},'lines':[{'id':lid,'text':text,'emotion':'自然親近，問句上揚' if '？' in text else '說書語氣，自然有起伏'} for lid,text in group]}
            if counters[ch]==1 and j==0: scene['chapter']=dict(CHAPTERS)[ch]
            scenes.append(scene)
            visual.append({'scene_id':part_id,'source_anchors':refs.split(','),'kind':'anonymous_concept_illustration','actual_historical_reconstruction':False,'scope':'動作示意，無品牌字樣、歷史人物肖像、可讀文件；非已生成或已驗收圖片。'})
        for lid,text in zip(lids,lines):
            narration.append({'chapter':dict(CHAPTERS)[ch],'id':lid,'text':text})
            scene_id=next(s['id'] for s in scenes if any(l['id']==lid for l in s['lines']))
            claims.append({'id':lid,'scene_id':scene_id,'text':text,'source_anchors':refs.split(','),'evidence':[evidence_for(ref,short) for ref in refs.split(',')],'kind':kind,'status':'PENDING_INDEPENDENT_REVIEW','boundary': '匿名概念插圖；假設動作或旁白觀點不主張為歷史現場。' if kind in ['hypothetical','opinion','question','mixed'] else '保留來源層級、年代與產品範圍；未經獨立新稿查核。'})
    out=[
        ('c06rn131','如果是你，會把一團材料反覆揉回去玩，還是留下一件完成的作品？留言告訴我，你最想做什麼。'),
        ('c06rn132','想繼續看熟悉的日用品，如何被使用者推著換工作，歡迎訂閱這個頻道。'),
    ]
    scenes.append({'id':'c06r-outro','template':'outro','data':{'title':'換一雙手，就換一種工作','cta':'你想反覆重做，還是留下成品？'},'lines':[{'id':lid,'text':text,'emotion':'溫暖收束，對一位觀眾說話'} for lid,text in out]})
    for lid,text in out:
        narration.append({'chapter':CHAPTERS[-1][1],'id':lid,'text':text})
        claims.append({'id':lid,'scene_id':'c06r-outro','text':text,'source_anchors':[],'kind':'editorial_cta','status':'PENDING_INDEPENDENT_REVIEW','boundary':'通用觀眾提問和有理由的訂閱邀請，未增加史實。'})
    video={
        'schema_version':1,'slug':SLUG,'format':'drama','category':'explainer','narration_locale':'zh-TW','target_minutes':[12,14],
        'voice':{'provider':'gemini','name':'Sulafat','style':STORY_VOICE_STYLE,'performance':'對一個人說材料怎麼換工作；企業與館方回顧自然保留歸屬。假設動作不演成歷史現場。'},
        'subtitles':{'burn_in':True},'look':{'preset':'cute-mystery'},'characters':[],
        'music':{'prompt':'light, curious, a little mysterious, no vocals','gain_db':-20,'duck_db':-10},
        'loops':[{'setup':index['h03'][0],'payoff':index['o11'][0],'what':'老師怎樣把清潔用品帶進教室'},{'setup':index['h03'][-1],'payoff':index['t07'][0],'what':'後來專利還要求材料做到哪些事'}]+[{'setup':index[a][-1],'payoff':index[b][0],'what':w} for a,b,w in LOOPS],
        'youtube':{'category_id':27,'made_for_kids':False,'default_language':'zh-TW','title':'Play-Doh：擦牆膏怎麼變成玩具？｜品牌故事','description':'一團原本擦壁紙的材料，怎麼換成孩子手上的玩具，又走向成人花藝？循著Kutol的公司史、The Strong的歷史回顧、美國專利，以及孩之寶的產品公告，看使用者如何改變顏色、工具與保存要求。1956是公司回顧的品牌生日；後來專利與現代套件各有自己的年代和產品範圍。匿名概念插圖不重建歷史現場。\n\n原件來源（查閱2026-10-25）\n'+'\n'.join(s['title']+'\n'+s['url'] for s in SOURCES.values() if s['id'] not in ['G1','G2']),'tags':['Play-Doh','培樂多','Kutol','品牌故事','黏土','日用品的意外轉身','玩具','商業故事'],'video_id':None},
        'thumbnail':{'template':'thumb','data':{'layout':'d','headline':'擦牆膏變玩具','sub':'2024稱逾5億罐','brand':'PLAY-DOH','tag':'品牌故事','shot':'c06r-h02'}},
        'sources':[{'title':s['title'],'url':s['url'],'checked_on':DATE} for s in SOURCES.values()],
        'assets':[],'scenes':scenes,
    }
    dump('video.json',video); dump('narration-only.json',narration)
    dump('claims.json',{'schema_version':1,'status':'AUTHOR_CANDIDATE_NOT_INDEPENDENTLY_REVIEWED','lines':claims,'written_visuals':visual,'source_catalog':'source-catalog.json','research_original':'research-original.claims.json'})
    dump('source-catalog.json',{'schema_version':1,'sources':list(SOURCES.values()),'original_sha256':hashlib.sha256((HERE/'research-original.claims.json').read_bytes()).hexdigest(),'status':'RESEARCH_RECORD_NOT_NEW_SCRIPT_APPROVAL'})
    dump('source-anchors.json',{'schema_version':1,'anchors':[{'id':s['id'],'url':s['url'],'locator':s['locator'],'excerpt':s.get('excerpt'),'raw_document_sha256':s['raw_sha256'],'published_on':s.get('published_on'),'limits':s['limits']} for s in SOURCES.values()],'lines':{c['id']:c['source_anchors'] for c in claims},'line_evidence':{c['id']:c.get('evidence',[]) for c in claims},'written_visuals':visual})
    dump('series.json',{'kind':'story','slug':'brand-stories-everyday-reversals','episode':6,'chapter':1,'title':video['youtube']['title'],'logline':'跟著一團能塑形的材料，從擦壁紙到教室、工具與成人花藝，看使用者如何改變材料的工作。','names':['Play-Doh','PLAY-DOH','培樂多','Kutol','Hasbro','孩之寶','Rainbow Crafts','Fun Factory','Blooms','凱・祖法爾','約瑟夫・麥克維克','諾亞・麥克維克','克里奧・麥克維克','The Strong','克羅格','Kroger','路易維爾','Louisville','辛辛那提','Cincinnati','比爾・羅登堡','Bill Rhodenbaugh','通用磨坊','General Mills','亞馬遜','Amazon','塔吉特','Target','沃爾瑪','Walmart','袋鼠船長','Captain Kangaroo'],'characters':[],'visual_tier':'stills','compilation':False,'target_minutes':13,'image_model':'image-01','look':{'preset':'cute-mystery'}})
    script=['# C06 Play-Doh｜全新作者候選','',f'新 slug：{SLUG}。此為作者逐字稿；不是原生canonical screenplay，也不是核准收據。','']
    for ch,title in CHAPTERS:
        script+=['## '+title,'']
        for n in narration:
            if n['chapter']==title: script += [f"**{n['id']}** {n['text']}",'']
    (HERE/'script.md').write_text('\n'.join(script)+'\n')
    md=['# C06 逐句來源與書面配鏡（作者待審表）','','這份表由作者建立。各句尚待不同代理核對原件，圖片尚未生成；不得當成獨立來源、敘事或媒體通過收據。','','| 旁白ID | 來源錨點 | 類別 | 限定 |','| --- | --- | --- | --- |']
    md += [f"| {c['id']} | {', '.join(c['source_anchors']) or '無新增史實'} | {c['kind']} | {c['boundary']} |" for c in claims]
    md += ['','## 原件與範圍','']
    for s in SOURCES.values(): md += [f"### {s['id']} — {s['title']}",f"{s['url']}\n\n定位：{s['locator']}。出版：{s.get('published_on') or '頁面未列初次出版日'}；查閱：{DATE}。\n\n範圍：{s['limits']}\n"]
    md += ['## 書面配鏡','', '所有 shot 均是匿名概念插圖，英文提示詞不放品牌、人名、標誌或可讀文字；不是歷史照片或專利原圖。1960 Fun Factory用通用槓桿擠壓示意，現代兩造型軌僅配現代官網B5554段；專利組成不配成1933配方，成人花藝不配成所有經典黏土的保存性能。實際出圖、視覺QA尚未成立。']
    md += ['','## 新稿使用的原件補充定位','', 'P1的顆粒薄膜／濕熱糊化段在PDF1印刷欄2，保留「專利作者認為」的解釋層級；claim8另寫可塑性與保留形狀。後半特性段的密閉容器、玩後放回、充分乾硬不可重塑及可上色，對應Google Patents description498–500；是文件對其組成的描述，沒有獨立性能測試。逐句的細定位及範圍另列claims.json的evidence及source-anchors.json的line_evidence。']
    (HERE/'claims.md').write_text('\n'.join(md)+'\n')
    ch_units={title:sum(units(n['text']) for n in narration if n['chapter']==title) for _,title in CHAPTERS}
    counts={'count_method':'native spokenUnits-compatible estimate, not measured audio','spoken_units_total':sum(ch_units.values()),'spoken_units_cold_open':ch_units[CHAPTERS[0][1]],'spoken_units_body':sum(ch_units.values())-ch_units[CHAPTERS[0][1]],'chapters':ch_units,'lines':len(narration),'scenes':len(scenes),'shot_scenes':len(visual),'outro_scenes':1,'loops_authored':len(video['loops']),'body_estimated_seconds_at_4_5_units_per_second':round((sum(ch_units.values())-ch_units[CHAPTERS[0][1]])/4.5,1)}
    hashes={name:hashlib.sha256((HERE/name).read_bytes()).hexdigest() for name in ['video.json','script.md','narration-only.json','claims.json','source-catalog.json','source-anchors.json','research-original.md','research-original.claims.json']}
    dump('author-notes.json',{'schema_version':1,'author':'/root/find_rules','date':DATE,'status':'AUTHOR_CANDIDATE_PENDING_ALL_INDEPENDENT_GATES','slug':SLUG,'counts':counts,'input_hashes':hashes,'scope':'Fresh C06 author candidate only; old C06 and other episodes untouched. Research originals copied byte-for-byte before authoring.','fact_limits':['1956 is attributed brand birthday, not independently established first invoice.','2017 scent application declares first use at least as early as1955-09-12; omitted from narration, not treated as independently verified first sale.','1933 cleaner formula and contemporary classroom records not obtained; later patent cannot prove their contents.','Kutol and museum history are attributed retrospectives, not contemporary classroom/business records.','Patent filing1960-05-17 and grant1965-01-26 distinct; goals are not independent performance tests, current formula or safety approval.','2024 annual cans are corporate shipments claim, not children, retail sales or revenue.','2024 licensing announcement is a plan, not proof of execution or a cause of the2026adult line.','2026adult-line and months-of-structure statements are company/product claims; no efficacy or sales-success claim.'],'production_plan':{'image_model':'image-01','look':{'preset':'cute-mystery'},'planned_shot_time_share_by_spoken_units':round(sum(units(c['text']) for c in claims if c['scene_id']!='c06r-outro')/sum(ch_units.values()),4),'consecutive_cards_max':1,'main_subtitles_burn_in':True,'cc_planned':True,'intro_after_cold_open_seconds':5,'outro_v4_seconds':21,'actual_branding_assets_verified':False,'fresh_production':True,'old_media_retrieval_prerequisite':False,'actual_paid_calls':0},'pending':{'independent_source_and_written_visual_review':True,'two_fresh_blind_narrative_readers':True,'independent_pronunciation_review':True,'owner_outline_approval':True,'owner_script_approval':True,'canonical_script_generation':True,'account_budget_admission':True,'tts_and_sentence_listening':True,'actual_body_runtime_12_to_14_minutes':True,'generated_images_and_visual_qa':True,'music':True,'assemble_and_final_qa':True,'owner_final_approval':True,'language_media':True},'no_approval_claim':'This author file confers no source/narrative/owner/audio/media/QA/budget approval.'})
    print(json.dumps(counts,ensure_ascii=False,indent=2))

if __name__=='__main__': main()
