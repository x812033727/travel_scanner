"""R2 authored narration/anonymous picture intentions, not review findings."""
ROWS=[]
def add(key,refs,kind,action,*lines):
    ROWS.append({'key':key,'chapter':key[0],'refs':refs.split(',') if refs else [],'kind':kind,'action':action,'lines':list(lines)})

add('h00','P1-shape','hypothetical','watching a small soft modeled form slump on a plain tray',
    '如果你捏的形狀，手一放就垮，還會再拿這罐嗎？')
add('h02','H1-scale','attributed','holding a plain closed modeling dough pot',
    '孩之寶二〇二四年說，Play-Doh年出貨逾五億罐。')
add('h01','M1-wall','hypothetical','opening a plain cleaning tin beside a wallpaper sample',
    '想像你在一九五〇年代的辛辛那提，正打開一罐壁紙清潔材料。')
add('h03','M1-demand','hypothetical','holding an unused cleaning lump beside a nearly clean wallpaper panel',
    '但在你眼前，牆上的煤灰正在變少。你取出材料，手感還好好的，卻得找個理由，讓人再次打開這罐。')
add('h04','M1-demand','opinion','examining an unused plain cleaning tin on a counter',
    '我覺得最棘手的，是材料還能用，原本的工作卻正在縮小。')
add('h05','M2-hard','teaser','looking at a small handprint beside a firm clay lump',
    '有一雙更小的手，正被另一團材料難住。')
add('h06','H3-display','teaser','examining a completed modeled flower beside a plain vase',
    '另一張桌上，一束剛做完的花，還得過最後一關。')
add('h07','K1-kay,P1-store,H3-display','promise','holding a plain modeling dough pot toward the viewer',
    '今天跟著Play-Doh，追一團材料怎麼在不同人的手上留下來。')
add('h08','K1-kay,P1-goals,H3-display','question','turning a small plain lump between both hands',
    '拿它的手換了，它究竟要替那個人做對什麼？')

add('o01','M1-kroger','attributed','placing a plain cleaning tin beside a blank order folder',
    '開場那罐材料，得先接到一份清潔訂單。史壯玩具博物館把故事的這一步，放在一九三三年。')
add('o02','K1-cleo,M1-kroger','history','holding a blank order folder at a small shop counter',
    '克里奧・麥克維克替Kutol接下克羅格的生意，要做現成的壁紙清潔材料，放到商店裡賣。')
add('o03','M1-kroger','question','looking from a blank order folder to an empty mixing bowl',
    '麻煩的是，館方說他們以前沒做過這種東西。訂單到手了，誰把材料做出來？')
add('o04','M1-noah','attributed','holding a plain malleable cleaning lump beside a mixing bowl',
    '依這篇回顧，負責產品開發的兄弟諾亞拿出了配方；柔軟、像黏土的清潔材料，就接上了這份工作。')
add('o05','M1-wall','hypothetical','pressing a pale cleaning lump against a smudged wallpaper sample',
    '如果你家牆面沾了煤灰，手裡這團能變形的材料，就有了一個要處理的目標：牆上那層髒污。')
add('o06','M1-wall','hypothetical','flattening a plain cleaning lump on a small tray',
    '想像你把它攤開，再收回手心；你在意的是，手上這次動作，能不能讓那片壁紙好看一點。')
add('o07','M1-wall','opinion','looking at a wallpaper sample beside a plain cleaning lump',
    '我覺得，這時候你需要留下的，是剛才那團形狀嗎？牆面乾淨，這個動作就能收手；手裡的外形，只是過程。')
add('o08','M1-1949','attributed','holding a closed plain family business folder',
    '館方接著記下，一九四九年克里奧去世，兒子約瑟夫接手了生意。輪到他想辦法讓公司繼續做下去。')
add('o09','M1-demand','question','looking at a cleaner wallpaper panel beside a closed tin',
    '但一筆生意，能不能只靠原來那面牆，一直做下去？')
add('o10','M1-demand','attributed','examining a simple domestic heating unit beside a clean wall',
    '回到開場那面煤灰變少的牆：館方說，二戰後家庭改用燃油或天然氣，到了五〇年代初，壁紙清潔材料的銷售開始下滑。')
add('o11','M1-demand','hypothetical','setting an unopened plain cleaning tin into a cupboard',
    '如果你家的煤灰問題少了，這罐東西就可能留在櫃子裡；它做得到原來的工作，也未必等得到你再買一罐。')
add('o12','M1-demand','opinion','holding a plain cleaning lump beside an unused tin',
    '我覺得，這比做壞一批貨更難想：材料還在，原本要處理的麻煩卻變少了，再努力擦同一面牆，也找不回那個需求。')
add('o13','K1-kay,M1-kay','question','turning a soft plain lump in one hand beside a blank classroom tray',
    '你若接住約瑟夫手上的材料，會讓它去見誰？有沒有一雙手，根本不打算拿它擦牆？')

add('k01','K1-kay,M1-kay,M2-hard','history','placing a small tray of soft modeling material on a classroom desk',
    '這雙不想擦牆的手，來自幼稚園。Kutol的公司史裡，老師凱・祖法爾是約瑟夫的姻親。')
add('k02','K1-kay,M1-kay,M2-hard','attributed','trying to flatten a firm clay lump with a frustrated expression',
    '博物館把她提出手工用途，放在一九五五年。還記得開場那雙小手嗎？名人堂說，一般塑形黏土太硬，孩子不好操作。')
add('k03','M2-hard','hypothetical','struggling to press a firm clay lump flat on a small plain desk',
    '想像你要做一隻小動物，連身體都壓不出來，耳朵怎麼接？作品還沒出現，手就先被難住了。')
add('k04','K1-kay,M2-hard','attributed','pressing a small indentation into a pliable plain lump',
    '名人堂回顧，約瑟夫送材料讓老師試；Kutol記下她把它帶進幼稚園，受到了歡迎。清潔材料，碰上了要塑形的小手。')
add('k05','M2-hard,M1-kay','hypothetical','adding a small soft ear to a plain modeled animal body',
    '換到容易推動的材料，你可以先壓一個身體，再接上一對耳朵；這樣的用途，有沒有真的讓經營者看見？')
add('k06','M1-kay','attributed','examining a classroom tray with simple modeled objects',
    '博物館接著寫，約瑟夫到學校看了孩子的作品，回去把產品重新調整、改作玩具，使用原有的設備和製造空間。')
add('k07','M1-kay','opinion','holding a simple modeled object beside a blank factory folder',
    '我喜歡這個具體的來回：他到桌邊看做出了什麼，再把這種用途帶回製造的地方，材料的評分方式已經變了。')
add('k08','M1-brand,H2-birthday','question','placing a plain toy tub on a classroom supply shelf',
    '教室願意用，下一步由誰把它當玩具來做？館方把Rainbow Crafts的成立，放在一九五六年。')
add('k09','M1-brand,H2-birthday','attributed','setting plain toy tubs into a classroom supply box',
    '那是Kutol的子公司，向辛辛那提一帶的小學推廣Play-Doh；孩之寶也把品牌的誕生放在這一年。')
add('k10','M1-colors,M2-colors','question','holding a pale modeled bird beside closed plain color pots',
    '但你做出一隻鳥，還想替它選嘴巴的顏色，只有原來那一團，夠不夠？')
add('k11','M1-colors,M2-colors','attributed','choosing red yellow and blue modeling material on a plain tray',
    '一九五七年，館方記下紅、黃、藍加入；名人堂的回顧還提到，材料變得更柔軟。')
add('k12','M1-colors','hypothetical','placing a small yellow beak onto a plain modeled bird',
    '你現在可以挑一小塊，讓嘴巴和身體不同色；想法不再只靠外形表現，選哪一塊接上去，也成了創作。')
add('k13','M1-colors','opinion','studying a small modeled bird beside a loose colored lump',
    '我覺得，顏色最有意思的地方，是它讓你做選擇。材料不是只等著被壓扁，它得跟得上你想做的東西。')
add('k14','M1-factory','hypothetical','rolling a narrow strand of modeling material between both hands',
    '可是，如果你想再替作品加一排細長條，每根都慢慢搓，要怎麼讓它們長得像你要的樣子？')

add('t01','M1-factory','attributed','pressing a simple tabletop modeling material extruder handle',
    '剛才要你慢慢搓的長條，可以改從一個出口擠出來；博物館把Fun Factory這件工具的推出，放在一九六〇年。')
add('t02','M1-factory','attributed','examining a simple lever tool beside a loose modeling lump',
    '館方說，約瑟夫請兩位工程師開發能有多種用途的配件，結果是用不大的力氣，把材料擠成不同形狀。')
add('t03','M1-factory','hypothetical','loading a small soft lump into a plain lever tool',
    '想像你先放進材料，再壓下手柄；原來要靠手指一段段搓出來的形狀，現在讓材料通過出口。')
add('t04','M1-factory','question','holding an extruded strand beside a plain modeled figure',
    '那你是不是什麼都不用做了？擠出來的長條，要放在哪一個位置，還是得由你選。')
add('t05','M1-factory','hypothetical','placing a short soft strand around the edge of a plain modeled object',
    '你可以想像，拿一段圍在作品旁，試試彎成一圈；工具替你做出形狀，接下來怎麼組合，作品才會變成你的。')
add('t06','M1-factory','opinion','comparing a hand rolled strand with a strand from a simple lever tool',
    '我喜歡這個分工：手不必包辦每一段細節，卻沒有把選擇交出去；一個小出口，改掉的是你施力的方法。')
add('t07','P1-header','question','looking from a plain lever tool to a completed soft modeled object',
    '還記得開場你手一放，形狀就垮的問題嗎？工具幫你擠出來，放開後的形狀，材料自己得接住。')
add('t08','P1-header','patent','holding a blank application folder beside a small plain modeling lump',
    '同在一九六〇年五月，諾亞和約瑟夫提出一件美國專利申請，受讓人列Rainbow Crafts。')
add('t09','P1-header','patent','examining a closed blank patent folder beside a lever tool',
    '它談的是兒童玩耍用塑形材料，寫下了玩具要面對的要求。')
add('t10','P1-shape','hypothetical','lifting both hands away from a small soft modeled object',
    '你擠出的長條，本來要接在作品旁；假如放下就變扁，連把它搬到作品上的那一下，都得重新想辦法。')
add('t11','P1-shape','question','watching a small soft modeled object standing on a plain tray',
    '但若材料硬得推不動，又回到那雙小手的困境；這件申請，究竟只顧你動手，還是也顧你放手？')

add('b01','P1-header,P1-shape','patent','opening a blank granted patent folder beside a small modeled object',
    '這兩個要求，在一九六五年一月核發的文本裡被放在一起：材料要可塑，也要有能保留形狀的稠度。')
add('b02','P1-shape','hypothetical','pressing one small part of a modeled figure while leaving its base standing',
    '對你來說，意思很直接：動手時能改它，放開以後，又希望看得出自己剛才做了什麼；只往一邊走，都會卡住。')
add('b03','P1-goals','question','holding a finished modeled animal beside a fresh loose lump',
    '但你只准自己做這一次嗎？如果明天想把動物變成船，材料還得替你留什麼？')
add('b04','P1-goals','patent','kneading a small modeled animal back into a loose lump',
    '文本把慢乾、可以反覆改形列為目標；捏完一個東西，並不必把材料下一次能做的事，一起用掉。')
add('b05','P1-goals','opinion','holding a reshaped soft lump with a small surprised smile',
    '我覺得這是很寬容的玩法：你可以推翻剛才的決定，再從同一團開始；不滿意，不一定要換一份材料。')
add('b06','P1-clean','question','lifting a soft modeled object from a plain tabletop',
    '可你把它從桌上拿起來，另一個問題就來了：手和桌面都黏住，作品還能好好移動嗎？')
add('b07','P1-clean','patent','holding a clean lifted modeling lump above a plain tray',
    '所以，乾淨、不黏手、不沾染，也是這份專利明列的要求；你玩完後怎麼把材料帶走，也在設計裡。')
add('b08','P1-film','question','holding a soft modeling lump beside a simple coated particle model',
    '它要自己合成一團，碰到你的手又別黏著不放；專利作者怎麼解釋這個差別？')
add('b09','P1-film','patent_hypothesis','examining a simplified model of small particles wrapped in thin layers',
    '他們認為，烴類餾分會包覆固體顆粒，形成薄膜；文件把柔軟、滑順和不黏的觸感，連到這層包覆。')
add('b10','P1-film','patent_hypothesis','holding a simplified model of a soft uniform mass beside separate coated particles',
    '文件再描述，包覆的麵粉顆粒經濕熱糊化，合成柔軟、均勻而不結塊的材料；這是作者對其組成的解釋。')
add('b11','P1-binding','patent','holding a cohesive plain modeling lump beside a simple particle model',
    '那裡面要怎麼合成一團？文件還允許加入有黏結作用的成分；表面要滑順，裡面也得合得起來。')
add('b12','P1-color','question','choosing a small colored lump beside the plain modeled bird',
    '還記得前面替小鳥挑的嘴巴嗎？如果加了顏色，卻把容易下手的手感弄丟，這個選擇還划算嗎？')
add('b13','P1-color','patent','pressing a small colored piece onto a plain modeled object',
    '文本也要求，能加入不同顏色，而不影響可塑性；讓你選外觀的同時，材料還得配合塑形。')
add('b14','P1-store,P1-mixing','question','holding a plain lid above an open modeling material pot',
    '還記得製造後立刻收起材料的容器嗎？玩到這裡，你要去做別的事了；這次用剩的，還能回得去嗎？')
add('b15','P1-store','patent','placing a soft lump into a plain airtight container',
    '文件寫到，玩過後也能放回密閉容器。你蓋上的，不只是今天剩下的一團，也是下次改主意的機會。')
add('b16','P1-dry','question','comparing a closed plain pot with a small hard modeled object',
    '那如果你偏要把成品留在外面呢？這份文本，也描述了另一個方向。')
add('b17','P1-dry','patent','holding a small hard modeled object beside a plain paintbrush',
    '它說，材料放在空氣中幾天會乾硬，乾硬後可以上色；但充分乾硬以後，就不能再揉回原來的狀態。')
add('b18','P1-store,P1-dry','hypothetical','holding a closed plain pot beside a finished small modeled object',
    '假設你今天做了一艘船，你得選：把材料收起來，明天重新做，還是接受不能重來，留下眼前這件。')
add('b20','H3-display','question','holding a completed modeled flower beside a plain vase',
    '如果你決定留下作品，而且想把它擺進家裡，最後這一步，有沒有另一種產品來幫你？')

add('n01','H3-display','announcement','setting a plain flower crafting kit beside an empty vase',
    '這個留下來展示的方向，到了二〇二六年七月，被孩之寶放進一套成人花藝產品；公司稱它是首個專為成人設計的系列。')
add('n02','H3-kit','opinion','holding a small soft modeled petal with a curious expression',
    '我覺得有趣的，是你這次買回來，要完成的是一束能放進生活裡的花；成人的手，有了被明確安排的動作。')
add('n03','H3-kit','question','holding a small plain flower mold beside a soft lump',
    '一團材料，怎麼變成整束花？公告裡的套件，從花瓣開始帶你做。')
add('n04','H3-kit','product','shaping one soft modeled petal with a small plain tool',
    '工具和模具幫你塑形，再把花組起來，最後排成花束；官方還提供每款的教學影片，讓步驟跟著套件一起到手。')
add('n05','H3-kit','hypothetical','placing a modeled flower into a plain vase',
    '想像你挑好位置，把花放進瓶子；做第一片花瓣時，你想調整，整束排好以後，你卻想讓它別再亂動。')
add('n06','H3-display','question','looking at a completed modeled bouquet beside a plain spray bottle',
    '還記得開場那束要過最後一關的花嗎？現在花束已經排好，要怎麼把這個形狀留下？')
add('n07','H3-display','attributed','holding a plain finishing spray beside a completed modeled bouquet',
    '孩之寶說，套件裡特製的最後處理噴霧，能幫花維持結構數月；這是公司對這款產品的保存說明。')
add('n08','P1-store,H3-display','opinion','looking between a plain closed modeling pot and a modeled bouquet in a vase',
    '我喜歡它和剛才那個蓋子的對照：前面收起材料，是替下一回留餘地；這裡，最後一步要保住的是你已經選好的位置。')
add('n09','H3-display','hypothetical','adjusting a modeled bouquet on a personal shelf',
    '你若把它放到自己的桌邊，材料的工作，只到你放手的那刻嗎？它要進入每天看得到的地方，完成後的用途也跟著改變。')
add('n10','K1-kay,P1-store,H3-display','opinion','holding a plain modeling material pot beside a small modeled bouquet',
    '回到開場那罐等待被打開的材料，我的答案是：它得先接住眼前這雙手，真正要完成的事，才有下一次被需要的機會。')

def insert_before(before,key,refs,kind,action,*lines):
    row={'key':key,'chapter':key[0],'refs':refs.split(',') if refs else [],'kind':kind,'action':action,'lines':list(lines)}
    ROWS.insert(next(i for i,r in enumerate(ROWS) if r['key']==before),row)

insert_before('k14','k13a','M1-television','question','looking from a plain toy tub to a blank television screen',
    '但光把罐子交到你面前，你會知道能做什麼嗎？這時，讓人看見手怎麼動，也成了一件工作。')
insert_before('k14','k13b','M1-television','attributed','placing a plain modeling material tub beside a blank television screen',
    '更麻煩的是，博物館說約瑟夫沒有大筆廣告預算；他便和《袋鼠船長》的主持人安排，至少每週在節目裡用一次產品。')
insert_before('k14','k13c','M1-television','hypothetical','watching a plain screen showing a simple modeled figure',
    '如果你坐在電視前，看見材料被壓、被接起來，原本密封在罐裡的東西，就有了可以照著試的動作。')
insert_before('k14','k13d','M1-television','opinion','holding a plain pot while looking at a small modeled object',
    '我覺得，這種展示讓材料多走了一步：你不必先想出一整套玩法，可以從看見的一個動作開始，再改成自己的作品。')

insert_before('t06','t05a','M1-factory','question','holding two extruded strands of different lengths beside a plain lever tool',
    '如果你這次只需要短短一段，出口能替你決定長度嗎？這又得回到你手上。')
insert_before('t06','t05b','M1-factory','hypothetical','pinching a short section from a soft extruded strand',
    '想像你讓材料伸出一小段，取下來，試著放到作品旁；還不夠長，就再壓一次。你控制何時停，長度才跟著眼前的用途走。')

insert_before('b11','b10a','P1-mixing','question','examining a bowl with separate plain ingredients beside a simple mixer',
    '可是一碗分開的材料，怎麼變成你手裡均勻的一團？文件裡還有製造時的動作。')
insert_before('b11','b10b','P1-mixing','patent','looking into a plain dough mixer beside a closed blank document folder',
    '它描述用攪拌機混合材料，再把熱水與其餘成分拌成均勻團塊；甚至舉出一般麵糰攪拌機，說機型不是關鍵。')
insert_before('b11','b10c','P1-mixing','hypothetical','pressing a small plain lump beside a second lump with a firm internal bump',
    '想像你正壓出一片平面，指下突然遇到硬結塊，還能照原來的力氣推嗎？製造時追求均勻，到了桌面上才有意義。')
insert_before('b11','b10d','P1-mixing','opinion','holding a smooth plain modeling lump beside a simple mixing bowl',
    '我覺得，從攪拌機到你的手，這裡接得很清楚：前面得讓材料一致，後面你才不用每捏一處，就重新猜它肯不肯動。')
insert_before('b11','b10e','P1-mixing','patent','placing a soft mixed mass inside a plain airtight container',
    '在文件的製法裡，材料混成可塑團塊後，立刻放進密閉容器；還沒交給玩的人，保存這件事就已經開始。')

insert_before('b16','b15a','P1-store','patent','setting a closed plain modeling pot on a small storage shelf',
    '蓋起來，只是留到明天嗎？文本聲稱，這樣保存可讓可塑性與工作特性，最長維持三年；同一罐東西，還有以後被打開的日子。')
insert_before('b18','b17a','P1-dry','hypothetical','painting the surface of a small hard modeled object with a plain brush',
    '你若等作品乾硬後再上色，顏色落到的是已經定下來的外形；你可以改表面，卻得接受下面那個輪廓不再任你揉。')
insert_before('b18','b17b','P1-color,P1-dry','opinion','holding a small paintbrush beside a colored soft piece and a hard modeled object',
    '還記得剛才替鳥接上去的黃色嘴巴嗎？那時你把色塊揉成形，現在則能在乾硬的作品上下筆；選哪個時機，連手上的動作都不同。')

insert_before('n05','n04a','H3-kit','hypothetical','shaping a small soft petal beside a simple flower mold',
    '假設你第一次做花，先只管眼前這片花瓣；模具讓你有個可以靠近的形狀，手再把細節調到自己想要的位置。')
insert_before('n05','n04b','H3-kit','question','holding a single modeled flower beside an unfilled plain vase',
    '可做完一朵，為什麼還沒結束？你得把它放進整束裡，看它和旁邊的花要怎麼站。')
insert_before('n05','n04c','H3-kit','hypothetical','positioning one modeled flower inside a small plain vase',
    '想像你拿起一朵，往旁邊移一點，再把另一朵靠近；這時候改的已經不只是單片形狀，而是整個擺在桌上的樣子。')

# Explain the optional binder before describing the document's mixing/packing sequence.
_binding=next(r for r in ROWS if r['key']=='b11')
ROWS.remove(_binding)
ROWS.insert(next(i for i,r in enumerate(ROWS) if r['key']=='b10a'),_binding)

LOOPS=[
    ('h00','b01','開場放手後形狀垮掉的問題在文本裡如何回應'),
    ('h08','n10','材料如何取得下一次被需要的機會'),
    ('h05','k04','被硬材料難住的小手得到什麼回應'),
    ('h06','n07','開場花束的最後保存關卡'),
    ('o03','o04','訂單到手後誰做出壁紙清潔材料'),
    ('o09','o10','原來的清潔工作為何縮小'),
    ('o13','k01','另一雙不想擦牆的手在哪裡'),
    ('k08','k09','由誰把用途接成玩具生意'),
    ('k10','k11','作品需要不同顏色時怎麼辦'),
    ('k13a','k13b','罐子之外如何讓人看見玩法'),
    ('k14','t01','細長條怎樣換一個製作動作'),
    ('t07','b01','鬆手後如何保住形狀'),
    ('t05a','t05b','工具擠出的長度由誰決定'),
    ('t11','b01','容易改形和保住形狀能否並存'),
    ('b03','b04','明天改主意時需要什麼材料條件'),
    ('b06','b07','材料如何離開桌面和手'),
    ('b08','b09','作者如何解釋聚成一團但不黏手'),
    ('b10a','b10b','分開的材料怎樣製成均勻團塊'),
    ('b12','b13','顏色會不會犧牲可塑性'),
    ('b14','b15','用剩的材料如何留下再玩機會'),
    ('b16','b17','留在外面的材料會走向什麼結局'),
    ('b20','n01','留下展示的方向後來出現什麼產品'),
    ('n03','n04','花藝套件怎樣帶人完成花束'),
    ('n06','n07','做完的花束靠什麼保留結構'),
]
