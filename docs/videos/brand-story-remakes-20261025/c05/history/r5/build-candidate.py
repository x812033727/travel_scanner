import copy, hashlib, json, re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4]
OUT=Path(__file__).resolve().parent
OLD=ROOT/'docs/videos/story-everyday-kincho-c05'
base=json.loads((OLD/'video.json').read_text())
# Source IDs refer to the preserved source-matrix.md. They remain PENDING for this revision.
chapters=[
('一根香燒完了，夜還很長', '''F02|你想讓一根蚊香陪你撐過長夜，早期一根卻約四十分鐘就燒完。|a worried adult seated at a small table watching a thin straight incense stick
F02|想像桌邊只剩一截灰，窗外仍暗著；你得再拿一根，夜晚才剛開始。|an adult placing an unlit straight incense stick beside a small pile of ash
F04|一八九五年留下的螺旋木模，像是替長香找到了一個藏身的圓。|an adult inspecting a plain wooden mold with a spiral groove
F04|但我覺得真正奇怪的，是想得出這個圓，還不一定做得成商品。|an adult frowning at a wooden spiral mold on a workshop bench
F09|後來保存的另一台工具，又把兩根長條交到工人手裡，問題還沒結束。|a worker lifting two plain soft strands beside a simple extrusion machine
F02,F04,F08|金鳥這一條香，我們從桌邊追到工廠，看一個形狀怎麼撐過製造和運送。|an adult holding a plain spiral coil above an open unmarked cardboard box
F02,F04,F08,F18|為什麼把香盤成螺旋，還不夠讓它久燃、完整地走上貨架？|an adult studying a single spiral coil resting on a plain tray'''),
('先有花種，卻還沒有能賣的形狀', '''F01|得先讓材料變成能交到人手上的東西；上山英一郎起初拿到的，只是種子。|an anonymous seed grower holding a small open paper packet
F01|金鳥後來整理的年表，從一八八五年的種苗交換約定開始記這段路。|a grower writing on a blank notebook beside several seed packets
F01|隔年，美國植物商寄來的種子裡，有了除蟲菊；新的材料這才到手。|a grower pouring a few seeds from a plain paper envelope
F01|但你把一包種子放到櫃台上，買家不會因此得到一根能用的蚊香。|a shopkeeper regarding a small seed packet on a bare counter
F01|先得種出花、收下花，再想怎麼把它做成能持續燃燒的東西。|a grower collecting plain small white flowers in a shallow basket
F01|一八八七年，年表記下首次收成和試磨；花被磨成粉，商品還沒成形。|a worker turning a small hand mill beside a bowl of dried flowers
F01|我讀到這裡才發現，熟悉的螺旋離這張工作桌，還隔著好幾個步驟。|an adult examining a bowl of powder beside an empty tray
F19|更早怎麼對付蚊子？金鳥資料館回顧，人們曾燻燒草木，靠煙來驅蚊。|an anonymous resident tending a small covered vessel of smoldering twigs outdoors
F19|資料館還說，草木燒旺時得設法增煙；煙多了，屋裡也可能跟著煙霧瀰漫。|a resident opening a window beside a hazy room
F19,F01|那包花種接下來面對的新難題，是能不能替粉料找到另一種商品形狀？|an adult comparing a basket of twigs with a bowl of dried flower powder
F01|一八八八年，上山與一位線香商人在東京同住，開始另一種試做。|an anonymous craftsman working alone at a modest workshop table
F01|公司年表寫，他用舶來除蚤粉和竹筒做蚊香；那包粉的配方，紀錄沒交代。|a craftsman placing a plain bamboo tube beside an unmarked powder bowl
F02|線香的做法給了一條路：把粉料變成細條，讓材料有可以持續燃燒的形狀。|a craftsman laying several straight incense sticks on a plain board
F01|到一八九〇年，年表裡終於出現直條產品上市，種苗變成可以出售的東西。|a shopkeeper setting plain straight incense sticks on a counter
F02|可是商品到了桌上，問題來了：單根撐不久，把它做得更長有用嗎？|a resident watching a short straight incense stick in a plain holder
F02|公司回顧，這種直條約二十公分長，當時往往得同時用上數根。|a resident arranging several separate straight sticks on a broad tray
F02|你多點幾根，可以讓眼前多幾個燃點，卻沒有把其中一根的路徑拉長。|a resident studying several separate sticks on a tray
F02|另一個麻煩在送達以前：原廠工廠說明回顧，細直條在運送途中容易折。|a shopkeeper examining a plain box containing a broken straight stick
F02,F03|要把一根香做長，又不讓桌面跟著拉長，手裡這條細線，能往哪裡走？|a craftsman bending a soft plain strand over a small round board'''),
('長條盤進圓，木模卻停住了', '''F03|把它往圓裡盤。依金鳥後來的記述，這個構想出自上山的妻子。|an anonymous woman gently curling a soft strand on a round board
F03|公司年表把提出構想和開始試作記在那一年；這是公司的後年歸屬。|an adult looking at a wooden spiral mold beside a blank archive card
F03,F04|國立科學博物館登錄的木模，也記作那時的試作品，物件確實留了下來。|a museum visitor studying a simple spiral wooden mold behind a display surface
F03|你可以拿一條線想像：直直擺，線有多長，桌面就得讓出多長的距離。|an adult stretching a plain cord across a small table
F03|把它一圈圈往裡收，路徑仍沿著線走，占用的平面卻縮小了。|an adult arranging a plain cord into a loose spiral on the same table
F03|我覺得這個轉身很漂亮，因為它先改的不是桌子，而是長條佔空間的方法。|an adult smiling at a plain spiral of cord on a round board
F04|可是桌上能盤出一圈，工廠就能每天交出同樣的成品嗎？|a worker comparing one soft spiral with several empty drying trays
F04|那塊木模的方案，是把原料填進去，再推出螺旋；形狀已經落成工具。|a craftsman gently pressing soft material into a plain wooden spiral groove
F04|你若只看展示品，很容易以為它就是後來大量生產的起點；這裡卻有個轉折。|a museum visitor leaning toward a plain wooden spiral mold
F04|金鳥技術遺產頁明說，這種木模不適合大量生產，最後沒有被採用。|a craftsman setting a wooden spiral mold aside on a workshop bench
F04|我原本也以為，工具都留下了，故事應該順理成章；偏偏它留作試作物。|an adult regarding an unused spiral mold on a shelf
F04,F06|能證明構想存在的物件，不能直接替它證明，商品已經源源不絕地做出來。|an adult holding a blank archive card beside a single wooden mold
F03,F04|歸屬也得停在資料能說的地方：公司記妻子的構想，博物館記了這件試作物。|a researcher placing a blank notebook beside a museum display
F03|國立公文書館介紹後年的授勳卷宗時，則把螺旋發明歸給上山英一郎。|a researcher inspecting a blank archival folder on a reading desk
F03|這些紀錄寫法不同，還不足以替我們補出一場誰先說、誰被忽略的家庭對話。|a researcher closing a plain archive folder thoughtfully
F04,F06|我們能繼續追的，反而是那個沒解掉的生產問題：圖畫成圓了，商品在哪裡？|a craftsman looking from a spiral sketch on a blank board to an empty tray
F05|公司年表再往下，有一個專利申請節點；申請能不能直接當作上市？|a clerk holding an unmarked application folder beside a spiral coil
F05,F06|你站在櫃台前要買一卷，等的是商品交得出來，還是紙上先多一筆紀錄？|a customer waiting beside an empty plain shop counter'''),
('上市後，工人把兩條合在一起', '''F05|不能。金鳥年表把螺旋蚊香的專利申請，記在一九〇〇年。|a clerk placing a plain application folder on a desk
F05|目前沒有原始申請文件可核對，所以這裡只說申請，不替它補成已經獲准。|a researcher studying an unmarked folder with a magnifying glass
F06|真正的上市節點，是一九〇二年；從提出螺旋構想到市售，隔了七年。|a shopkeeper placing a plain spiral coil on a counter
F04,F06|這七年最勾人好奇，可惜資料沒有逐年試作帳，不能替每一年安排一次失敗。|a researcher looking at a row of blank folders with several spaces between them
F04,F09|我寧可跟著下一件留存工具走：後來的人，究竟怎麼讓長條盤成形？|a museum visitor leaning toward a simple hand operated extrusion machine
F09|那是手卷用的擠出設備，原廠標示約從一九一〇年起使用，晚於上市。|a worker resting one hand on a simple extrusion machine in a workshop
F04,F09|和把原料填進木模不同，它先把材料擠成像麵條的長條，再交給人的雙手。|a worker lifting a single soft strand beside a plain extrusion nozzle
F09|注意工人接到什麼：兩根已擠出的長條，合在一起，才用手順著圓周盤卷。|a worker aligning two soft strands on a round work board
F09|原頁沒有說機器同時擠出兩條；能確認的是，手卷這一步把兩根放到一起。|a worker carefully curling two aligned soft strands on a board
F09,F08|你看到的兩個螺旋，為什麼非得靠在一起？原廠給它一個運送上的理由。|a packer holding a plain joined pair of spiral coils above a shallow box
F08|金鳥說，雙卷方式能降低運送中的折損與運輸成本；這裡沒有具體省下的金額。|a packer placing a joined pair of coils flat inside a plain cardboard box
F08,F03|我覺得有意思的是，同一個圓開始回答另一道題：做得長以後，還得送得完整。|a packer gently closing an unmarked box containing joined coils
F08,F18|不過，運送時彼此相連，跟單卷點燃後燒得多慢，並不是同一個機制。|an adult setting a joined pair beside one separated spiral coil
F07|那麼長香真正燒得久嗎？較晚的商品紀錄，才留下可以落地的數字。|a museum visitor looking at a plain spiral coil beside a blank measurement card
F07|金鳥資料館列出約一九一九年的一款螺旋，約五十八公分，燃燒約六小時。|a museum visitor studying a plain spiral coil in a shallow display tray
F07|這是資料館對那款較晚商品的標示，不能把它塞回試作木模或最早上市的那一天。|a researcher placing a blank date card beside a separate product tray
F14|資料館另列約一九二二年的手卷商品，燃燒約十二小時，又是另一款。|a museum visitor comparing a second plain coil in its own display tray
F07,F14|你現在看到的是不同時期、不同商品的刻度，沒有證據說它們用同一個配方。|a researcher comparing two separate product records on a desk
F02,F07|所以也不能把開場的短香與較晚螺旋相除，說成殺蚊本領增加了幾倍。|an adult moving a plain calculator away from a pair of incense samples
F07,F14|時數說的是燃燒持續多久；把它聽成效果有多強，就已經替資料加了一句話。|an adult studying a simple hourglass beside a plain coil
F10|到了戰前，海外宣傳海報也保存下來，產品被推向更遠市場的痕跡還在。|a visitor looking at an unmarked poster beside a plain export crate
F10|海報能證明宣傳出現過，卻不會自己開口告訴你，每個地方到底賣了多少。|a researcher examining the blank back of a poster at a desk
F09,F15|靠雙手盤出的圓，接下來碰上打型機；機器一完成，人的雙手就立刻退場了嗎？|a worker pausing between a hand rolling board and a simple stamping machine'''),
('新機器完成，舊手卷沒有立刻消失', '''F09,F15|沒有這麼整齊。公司年表記一九四〇年，自動輪轉打型式螺旋蚊香製造機完成。|a technician inspecting a simple rotary stamping machine
F09|可剛才那套手卷設備的留存介紹，使用期還一路記到約一九五七年。|a worker curling a soft strand by hand beside a plain extrusion machine
F09,F15|一條紀錄寫新機器完成，另一條寫舊設備仍在使用；它們並不要求同一天交棒。|a researcher comparing two blank equipment record cards
F09,F15|我覺得這才像生產史：一個發明的年份，往往放不下每條產線後來的生活。|an adult looking across a workshop with a hand work board in the foreground
F09,F15|但哪座工廠先換、哪天最後一次手卷，現有資料沒有給出，我們也就不演那一天。|a researcher leaving an empty space between two plain folders
F20|這段歲月，材料也在變；金鳥工廠回顧，為了增加糧食生產，除蟲菊栽培縮小。|an anonymous grower looking over simple planted rows under an overcast sky
F20|同一份說明又記，約一九五五年，合成成分丙烯菊酯開發並實用化。|a technician studying two sealed plain ingredient containers on a bench
F20|這說的是原廠回顧的材料進展，不能說所有蚊香在同一年就一起換了配方。|a technician arranging different plain ingredient containers separately
F16|接著，公司年表記改良型高效率自動打型機完成，工廠回顧也把機械打型放在這時。|a technician checking a plain spiral cutting die above a flat sheet
F16|而你把金鳥的卷拿起來看：工法轉換後，螺旋為什麼連方向都換了？|an adult holding a single plain coil flat above a table
F16|原廠說，當時同業多做右卷，自家便改成左卷，讓外形方向和別人有所區別。|a worker comparing two plain coils curling in opposite directions
F16|這不是哪邊比較會燒的比賽，而是公司對辨識方式的解釋；我差點也想反了。|an adult turning a plain coil over thoughtfully
F11|時間拉回你今天拿到的雙卷，兩卷相連著出貨，使用前該從哪裡分開？|an adult setting a plain joined pair of coils on a table
F11|原廠的現行問答說，從中間輕按，再捏住比較厚的中心，拆成各自的一卷。|close view of one adult hand gently separating a plain joined pair at the center
F11|如果從外緣硬拉，就可能折斷；暫時不用，反而要保持相連，才不容易變形。|an adult setting an intact joined pair carefully into a plain storage box
F11|你大概遇過這種心情：東西還沒開始用，先擔心自己的手把它弄壞了。|an adult with a sheepish expression holding an intact pair of plain coils
F11,F18|但分開只是讓每一卷成為自己的路徑；火為什麼能在那條路上慢慢走？|an adult following the path of a single unlit coil with a pointing finger'''),
('路徑在外面，速度藏在香體裡', '''F18|金鳥工廠給的解釋在香體斷面：空隙少，氧氣不容易進去，於是慢慢燃燒。|a technician inspecting a simplified solid incense cross section with a magnifier
F18,F03|所以你看見的螺旋，處理的是路徑放得下；材料的結構，影響那條路走得多快。|an adult comparing a spiral cord with a plain incense cross section
F18|我覺得最容易想錯的就在這裡：把形狀的本事，一口氣算成材料的本事。|an adult frowning thoughtfully at a plain spiral coil on a tray
F11|現行一般尺寸，金鳥標示單卷約七十五公分，燃燒約七小時，已經是另一代規格。|an adult holding a plain present day coil beside an unmarked measuring strip
F11|同一份問答還列短時和長時尺寸，並提醒環境會改變實際燃燒時間。|an adult examining three differently sized plain coils on separate trays
F12,F20|材料也沒有停在早年的花粉：原廠說明所述產品，使用合成擬除蟲菊酯有效成分。|a technician pouring material from a plain sealed container into a mixing bowl
F12|植物性粉末、木粉與黏結材料仍參與混合；有效成分換了，不等於植物材料都不見。|a worker blending plain powders in a broad workshop bowl
F12|把混合料加工成片，再打出螺旋並乾燥，這是工廠頁描述的另一種製法。|a worker lifting a plain spiral shape cut from a flat sheet
F09,F12|你剛才看過的手盤動作，在這裡換成打型；圓留下來了，做出圓的動作卻變了。|a technician comparing a hand rolled sample with a plain cutting die
F17|還有一個讓我意外的小細節：原廠說混料本來偏棕，熟悉的綠又從哪裡來？|a worker inspecting a plain brownish mixture in a shallow tray
F17|綠色是後來染上的；金鳥列的理由，先有容易均勻著色，也有夏季清涼的印象。|a worker stirring a plain mixture in a vat under soft workshop light
F17|說的是視覺印象，不是顏色真的替房間降溫；工廠沒有給這項功能。|an adult regarding an unlit plain coil beside an open window
F17,F19|公司還把這個顏色，連到昔日蚊遣用草葉的葉色，讓新商品接住熟悉的聯想。|an adult comparing a basket of plain leaves with an unlit spiral coil
F17,F19|這是原廠後來說明的設計理由，不表示早年每一根香，都已經有今天的配方。|a researcher placing a plain historical sample apart from a modern sample
F04,F09,F12|桌上的那塊木模沒能量產，後來的手卷與打型，卻接著把螺旋做成可交付的東西。|a museum visitor looking from a plain wooden mold toward a hand rolling board
F03,F08,F18|回到開場：你要的不是圖紙上一個好看的圓，而是一根能久燃、也送得完整的香。|an adult holding an intact plain coil above a closed cardboard box
F03,F08,F18|我的答案是：螺旋收進長路徑，香體結構影響慢燃，雙卷再按原廠說法減少運送折損。|an adult placing a single coil beside an intact joined pair
F04,F11|如果你曾把相連的雙卷拆斷，留言告訴我，你當時先抓的是中心，還是外緣？|an adult smiling awkwardly while holding an intact plain joined pair
F04,F09,F12|想看懂日用品背後這些不只靠一個好點子的選擇，歡迎訂閱奇聞檔案局。|an adult closing a plain notebook beside a spiral coil''')]

rows=[]
for ci,(chapter,block) in enumerate(chapters,1):
 for line in block.splitlines():
  fids,text,subject=line.split('|',2)
  rows.append({'chapter_index':ci,'chapter':chapter,'id':f'c05r{len(rows)+1:03d}','text':text,'source_ids':fids.split(','),'subject':subject})

# A narrow r2 adds source-backed material detail and makes each actual unresolved turn audible.
revisions={
 'c05r012':'先得種出花、收下花；可是一碗磨好的粉，要靠什麼變成能點燃的商品？',
 'c05r032':'我覺得這個轉身很漂亮；但盤得進小桌面，就等於工廠能夠交貨了嗎？',
 'c05r033':'難題換了位置：桌上盤出一件，工廠要交出的，卻是一件接著一件的商品。',
 'c05r054':'你看到的兩個螺旋，為什麼非得靠在一起，才被送往貨架？',
 'c05r058':'那麼，這些較晚的商品，到底留下多長、燒多久的明確紀錄？',
 'c05r062':'你看到不同時期、不同商品的刻度，這些時數能不能直接換算成殺蚊本領？',
 'c05r072':'工法之外，這種形狀也得靠原料撐住；花田和材料，後來又發生了什麼事？',
 'c05r089':'原廠還列短時與長時尺寸，環境也會影響時數；可香體裡面，還是當年的花粉嗎？',
 'c05r094':'還有一個讓我意外的小細節：原廠說混料本來偏棕，熟悉的綠又從哪裡來？',
 'c05r099':'從那塊沒能量產的木模到你手裡，這一卷究竟靠哪些本事，才走到貨架？',
 'c05r100':'我的看法是，它最厲害的地方，是把桌邊、產線和送貨途中不同的難題接在一起。'
}
for r in rows:
 if r['id'] in revisions:r['text']=revisions[r['id']]
new_after={
 'c05r085':[
  ('S21','原廠還提出一個具體比較：外形、材料、粗細和長度都不變，只把重量減輕。','a technician comparing two identically shaped plain coils on separate balance pans'),
  ('S21','外面看起來一樣，裡面比較鬆，空氣會不會更容易碰到材料？','a technician examining two simplified incense cross sections with a magnifier'),
  ('S21','照公司的解釋，密度較小，內外更容易接觸空氣，就應該燒得比較快。','a technician pointing at the open spaces in a simplified incense cross section'),
  ('S21,F11','這讓你分清一件事：原廠標示的時數，該跟著螺旋外形走，還是跟著每款產品看？','an adult comparing two identical plain coils with different simplified internal patterns')],
 'c05r091':[
  ('S21','工廠說，植物粉末裡還包括取走除蟲菊有效成分後留下的粉，材料並非只剩藥劑。','a technician holding a shallow tray of plain dry plant powder'),
  ('S21','但粉末一倒就散；這樣的材料，要靠什麼留住可以拿在手裡的螺旋？','a worker looking at a small loose powder pile beside an empty spiral mold'),
  ('S21','原廠列出黏結用的粉料和澱粉，與植物粉、有效成分一起混合，才得到可加工的原料。','a worker adding plain powder from a small bowl to a broad mixing basin'),
  ('S21','所以形狀背後還有材料的配合：你拿的是一個圓，工廠得先處理怎麼把粉料做成形。','a worker lifting a coherent plain spiral shape above a mixing tray')],
 'c05r092':[
  ('S21','你以為把粉料黏成圓就結束了？燃燒時，它還要把什麼交到空氣裡？','a technician watching a thin wisp above a plain incense coil in a workshop'),
  ('S21','燃燒時，有效成分會以極細微粒子的形式進入空氣，這也是原廠描述的工作方式。','a technician pointing at a simple magnified illustration of a few particles above an incense strand'),
  ('S21','所以粉料既要能成形，也得能持續燃燒；形狀、材料與時間，到這裡才真正接上。','a worker inspecting a single intact plain coil on a drying tray')]
}
expanded=[];extra=0
for r in rows:
 expanded.append(r)
 for fids,text,subject in new_after.get(r['id'],[]):
  extra+=1
  expanded.append({'chapter_index':r['chapter_index'],'chapter':r['chapter'],'id':f'c05rx{extra:03d}','text':text,'source_ids':fids.split(','),'subject':subject})
rows=expanded

# R3–R5 only remove the two-reader failures, retaining one-reader-only differences.
removed_ids={'c05r094','c05r095','c05r096','c05r097','c05r098','c05r099','c05r100','c05r065','c05r066','c05r086','c05r039','c05r040','c05r041'}
rows=[r for r in rows if r['id'] not in removed_ids]
for r in rows:
 if r['id']=='c05r101':
  r['text']='回到那塊沒進產線的木模：螺旋只是構想起點，還得把材料、製造和送達一起做成，才是商品。'
 if r['id']=='c05r103':
  r['text']='想看懂日用品背後這些不只靠一個好點子的選擇，歡迎訂閱這個頻道。'

p=copy.deepcopy(base)
p['slug']='story-everyday-kincho-c05-remake-20261025'
p['target_minutes']=[12,14]
p['subtitles']={'burn_in':True}
p.pop('series',None)
p['voice']['style']='標準國語，咬字清楚，台北人平常說話的語調。說書人，像在跟朋友講一件等不及要分享的真實日用品故事。有自然起伏，數字清楚，揭曉前停一拍，問句上揚。語速像平常聊天，一秒四到五個字，句與句之間不拖。絕不平、絕不像在念稿。'
p['voice']['performance']='開場直接對觀眾說；木模段帶好奇與意外；年代和歸屬讀清楚；工序自然連著講；不同商品時數不念成效力比較；結尾親近乾脆。'
p['youtube']['title']='金鳥蚊香：四十分鐘就燒完，盤成螺旋為何還不夠？｜品牌故事'
p['youtube']['description']='金鳥的早期直條蚊香，原廠回顧一根約四十分鐘就燒完。把它盤成螺旋，為什麼還不夠？沿著留下的木模、手卷擠出設備和後來的打型機，追一卷蚊香如何面對久燃、製造與運送的難題。歷史場景為原創情境插畫，數字與製程依來源所屬年代說明。\n\n參考資料\n'+'\n'.join(source['title']+'\n'+source['url'] for source in p['sources'])
p['youtube']['video_id']=None
p['thumbnail']={'template':'thumb','data':{'headline':'盤圓還不夠','sub':'四十分鐘後怎麼辦','brand':'金鳥','tag':'品牌故事','shot':'c05r001'}}
p['scenes']=[]
cameras=['push in','pan left','pull out','pan right','drift','tilt down']
framing=['Medium shot of ','Close-up of ','Wide shot of ']
for i,r in enumerate(rows):
 scene={'id':r['id'],'template':'shot','data':{'prompt':framing[i%3]+r['subject']+[' under an overcast sky.',' with soft lamp light from the right.',' in mild afternoon light.',' with soft grey daylight from a doorway.',' under a shaded workshop lamp.',' in soft morning light.'][i%6],'camera':cameras[i%len(cameras)],'visual':'still'},'lines':[{'id':r['id'],'text':r['text'],'emotion':'對一個朋友說書，自然起伏；意見用自己的反應，數字清楚'}]}
 if r['id']=='c05r005':scene['data']['prompt']=scene['data']['prompt'].replace('under a shaded workshop lamp.','with soft workshop daylight.')
 if i==0 or r['chapter_index']!=rows[i-1]['chapter_index']:scene['chapter']=r['chapter']
 p['scenes'].append(scene)
# Closing answer, personal comment question and subscription reason are one three-sentence outro.
p['scenes']=p['scenes'][:-3]+[{'id':'c05r-outro','template':'outro','data':{'title':'螺旋、香體、雙卷各解一題','cta':'參考資料在說明欄'},'lines':[{'id':r['id'],'text':r['text'],'emotion':'結尾親近乾脆'} for r in rows[-3:]]}]
# R4–R5 are pure scene deletions: preserve every retained r3 scene byte-for-byte.
r3_scenes={scene['id']:scene for scene in json.loads((OUT/'history/r3/video.json').read_text())['scenes']}
p['scenes']=[copy.deepcopy(r3_scenes[scene['id']]) for scene in p['scenes']]
# Explicit semantic setups/payoffs, authored for this revision; the narrative panel must still review them.
pairs=[('c05r001','c05r059','早期短香不足的利害，後年商品提供不同時數刻度'),('c05r003','c05r036','木模為何未能量產'),('c05r005','c05r052','兩根已擠出長條如何手卷'),('c05r007','c05r101','形狀、材料與運送各自回答主問'),('c05r011','c05r021','種子如何變成可售直條'),('c05r012','c05r020','粉料如何得到可持續燃燒的形狀'),('c05r017','c05r020','尋找商品形狀'),('c05r022','c05r031','長路徑如何收進平面'),('c05r025','c05r055','運送易折的後來工程答覆'),('c05r026','c05r031','把長條收進較小桌面'),('c05r032','c05r036','幾何構想是否足夠量產'),('c05r042','c05r047','實際市售的年份'),('c05r043','c05r045','申請與上市不同'),('c05r049','c05r051','後年設備如何成形'),('c05r054','c05r055','雙卷的運送理由'),('c05r057','c05r085','慢燃與運輸不是同一個機制'),('c05r058','c05r059','後年商品的燃燒時數'),('c05r062','c05r063','燃燒時數不等同殺蚊本領'),('c05r067','c05r069','機器完成是否讓手卷立刻消失'),('c05r072','c05r073','材料改變的背景'),('c05r077','c05r078','旋向的辨識理由'),('c05r080','c05r081','使用前如何處理相連雙卷'),('c05r084','c05r085','香體慢燃的解釋'),('c05rx002','c05rx003','同形狀較低密度的比較'),('c05rx004','c05r088','燃燒時數應依各款產品規格'),('c05rx009','c05rx010','燃燒時有效成分如何進入空氣'),('c05rx006','c05rx007','粉料如何凝成可加工材料'),('c05r089','c05r090','現行香體的有效成分來源是否仍相同'),('c05r094','c05r095','材料原色與熟悉外觀的差異'),('c05r099','c05r101','回答整段製造與送達的主問')]
# Use only valid forward ordered line IDs; rejected mis-indexed loops are not silently relabeled.
current_ids={r['id'] for r in rows}
p['loops']=[{'setup':a,'payoff':b,'what':what} for a,b,what in pairs if a in current_ids and b in current_ids]
(OUT/'video.json').write_text(json.dumps(p,ensure_ascii=False,indent=2)+'\n')
context={'kind':'story','slug':'brand-story-remakes-20261025','episode':5,'chapter':1,'target_minutes':13,'look':{'preset':'cute-mystery'},'image_model':'image-01','visual_tier':'stills','characters':[],'names':['金鳥','KINCHO','上山英一郎','ゆき'],'original_series':base.get('series'),'original_slug':base['slug'],'status':'candidate_unapproved','planned_slug':p['slug']}
(OUT/'series.json').write_text(json.dumps(context,ensure_ascii=False,indent=2)+'\n')
(OUT/'brief.md').write_text('# 金鳥蚊香｜10-25 新規則重製候選\n\n狀態：未核准，僅為新稿候選。依 PR #1844 的工作區製片方式重製既有 C05，保留原稿與舊媒體。\n\n## 問題\n\n為什麼把香盤成螺旋，還不夠讓它久燃、完整地走上貨架？\n\n## 一句答案\n\n螺旋收進長路徑，香體結構影響慢燃，雙卷再按原廠說法減少運送折損；試作木模、後年手卷與打型分別處理可製造性。\n\n## 站主觀點\n\n公司回顧、館藏登錄與現行規格留在各自年代；未有原件的專利核准、逐年試作故事與全廠換線日不補寫。新稿目標 13 分鐘；字數與文字估時不是音訊證據，實際 12–14 分鐘旁白仍須 TTS 量測。原創可愛示意插畫、MiniMax image-01、look 只用 cute-mystery、燒錄繁中字幕與 CC、開場後五秒正式片頭、二十一秒 v4 片尾、bold 縮圖。所有新核准均待獨立查核與雙盲；不挪用歷史 PASS，不觸發後台或付費。\n')
(OUT/'series-context.json').write_text(json.dumps(context,ensure_ascii=False,indent=2)+'\n')
(OUT/'narration-only.json').write_text(json.dumps([{'chapter':r['chapter'],'id':r['id'],'text':r['text']} for r in rows],ensure_ascii=False,indent=2)+'\n')
md=['# C05 金鳥蚊香｜10-25 新規則重製候選','', '狀態：未核准候選。只含新稿與逐句來源映射；未產生音訊或圖片，未沿用舊稿任何 PASS。正文時長須實測；以下 ID、來源與章名不進旁白。','']
for ci,(chapter,_) in enumerate(chapters,1):
 md+=['## '+str(ci)+'｜'+chapter,'','| ID | 旁白 | 來源矩陣列 |','| --- | --- | --- |']
 for r in rows:
  if r['chapter_index']==ci:md += [f"| {r['id']} | {r['text']} | {', '.join(r['source_ids'])} |"]
 md += ['']
md += ['## 來源與限制','','來源矩陣為 [既有 C05 source-matrix.md](../../story-everyday-kincho-c05/source-matrix.md)，該矩陣的 2026-10-22 查核日期只代表既有資料讀值；本稿仍須逐句獨立重核。公司回顧、館藏登錄、原始申請與現行規格分開，不把公司說法升格為獨立實測。','','#1844 是製作方式與新版規則參考；本稿沒有挪用 H24／S30 的史實、查核或核准收據。']
(OUT/'script.md').write_text('\n'.join(md)+'\n')
cl=['# C05 新稿逐句主張表','','全部 **PENDING**。來源 Fxx 只表示作者對既有來源矩陣的映射，尚不是獨立查核結果。新稿每句必須由另一代理對原件與語境重核。','','| 行 | 旁白 | 來源 | 判定 |','| --- | --- | --- | --- |']
for r in rows:cl+=[f"| {r['id']} | {r['text']} | {', '.join(r['source_ids'])} | PENDING |"]
cl += ['', '## S21 新增段落來源', '', 'S21 為 2026-10-25 直接讀取的金鳥工廠說明：https://www.kincho.co.jp/factory/listen/detail.html。文字快照與 URL／日期見 source-snapshots/source-1.txt、source-1.metadata.json。新增範圍只包括原廠提出的同外形／材料／粗細／長度但低密度較快燃燒的條件比較、粉料與澱粉等黏結材料，以及有效成分於燃燒時以極細微粒子形式進入空氣。均是原廠技術說明，不是本集獨立實驗，也不延伸為安全或效力承諾。S21 每句同樣 PENDING，須由另一代理對照完整段落。']
(OUT/'claims.md').write_text('\n'.join(cl)+'\n')
spoken=len(re.sub(r'[^\w\u4e00-\u9fff]','',''.join(r['text'] for r in rows)))
notes={'status':'candidate_unapproved','basis_commit':'2b20c30d359fe5d93a4ea66f013a52fa20a35c05','reference_pr':1844,'original_slug':base['slug'],'candidate_slug':p['slug'],'counts':{'scenes':len(p['scenes']),'lines':len(rows),'spoken_characters':spoken,'characters_including_punctuation':sum(len(r['text']) for r in rows),'illustration_scenes':sum(s['template']=='shot' for s in p['scenes']),'cards':sum(s['template']!='shot' for s in p['scenes'])},'estimated_seconds_at_4_5_chars':round(spoken/4.5,2),'duration_gate_passed':False,'measured_tts_seconds':None,'prior_owner_approval_reused':False,'new_source_access_performed':True,'source_evidence':'Existing 2026-10-22 C05 source matrix plus 2026-10-25 source-snapshots/source-1.txt and source-2.txt; S21 adds the factory density comparison and binder ingredients; independent exact-script verification pending.','holds':['New candidate script needs independent line-by-line source review and two isolated narrative readers.','No TTS or image request has been made; actual 12–14 minute body duration remains unmeasured.','Candidate remake slug has no activated whole-film account; no paid call is allowed until production budget routing and attribution are ready.','Current C05 historic USD25/79-line/86-image approval does not cover this expanded remake.','Opening max-two-previews rule conflicts with legacy lint requirement of three opening loops; document result without manufacturing a third preview.'],'source_boundaries':['F03 wife attribution remains company retrospective; archival attribution differs and does not prove erasure.','F05 1900 is a company-recorded patent application only, not a grant.','F07/F14 describe separate circa-1919 and circa-1922 products, not a same-formula evolution or efficacy multiples.','F09 extruded strands are combined by hand; no claim of simultaneous double extrusion.','F15/F16 completion dates do not prove fleetwide changeovers.','F17 green color is the described modern product design rationale, not historic formula continuity.','F18 geometry, material burn rate and dual-coil shipping are different mechanisms.'],'input_sha256':{f:hashlib.sha256((OLD/f).read_bytes()).hexdigest() for f in ['script.md','source-matrix.md','video.json']},'file_sha256':{f:hashlib.sha256((OUT/f).read_bytes()).hexdigest() for f in ['video.json','script.md','claims.md','narration-only.json','series-context.json']}}
(OUT/'author-notes.json').write_text(json.dumps(notes,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(notes['counts'],ensure_ascii=False));print('Estimate',notes['estimated_seconds_at_4_5_chars'])
