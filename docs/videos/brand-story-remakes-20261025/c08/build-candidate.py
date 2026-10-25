#!/usr/bin/env python3
"""New C08 author candidate. No legacy/research mutation or external requests."""
import hashlib
import json
import pathlib

REPO=pathlib.Path('/workspace/work/brand-remakes-source')
OUT=pathlib.Path(__file__).resolve().parent
AUDIT=pathlib.Path('/workspace/work/brand-story-20261025/c08-audit')
SLUG='story-everyday-kikkoman-c08-remake-20261025'
TITLE='龜甲萬：倒出1滴，空氣為何不能進錯地方？｜品牌故事'
PROTECTED={
 'research-original.claims.json':'098d17da9a77136bfe3e3d2dafe5aa19d11c087c7203686ecd7f4e87906e7795',
 'research-original-patents.json':'2ed544c6ed699724c8b6cc26099433a8f6df38f8acc884e82861eca61e18951c',
 'research-preservation.json':'86beb0a5259ee374092a1e3295187f8a6bbf7d43d271abb19e04edad9b50cd73',
 'research-original-patents.md':'fa8aca895af38633b1d007cec176319ca1257c236abbce322b6d85b13912753e',
 'research-original.md':'632c82616fa87591482902731c7079288625160b5dd693a5c21893e9b5531ae3',
 'README.md':'59b955d5b0e06c73a1ee03e1832a50cc62fc64b25f4abb926b54695ef51fd145',
}
sha=lambda f:hashlib.sha256(pathlib.Path(f).read_bytes()).hexdigest()
for filename,expected in PROTECTED.items():
 assert sha(OUT/filename)==expected,filename
research=json.loads((OUT/'research-original.claims.json').read_text())
patents=json.loads((OUT/'research-original-patents.json').read_text())

# Newly written narration. Research IDs are source anchors, never verifier verdicts.
# Prompts show anonymous concepts and keep the glass, early squeeze, and current PET types distinct.
CHAPTERS=[
('倒完後，手還不能收回去', '''
你只想倒一點醬油，為什麼還得擦桌子？|C08R09|holding a plain glass condiment dispenser over a small dish
龜甲萬說，到二〇一八年三月底，桌上瓶累計出貨已逾五億瓶。|C08R29|examining a plain glass condiment bottle with an unlettered cap
想像你坐在餐桌旁，握著玻璃瓶的細頸，倒完後把手收回。|C08R11,C08R15|setting a plain narrow-necked glass condiment bottle beside a small dish
嘴尖那一點褐色，會乖乖停住嗎？|C08R12,C08R14|looking closely at a tiny dark drop on a plain glass dispenser spout
但後來，連進入瓶裡的空氣，都成了難題。|C08R20,C08R21|examining a plain flexible condiment bottle beside a sealed empty pouch sample
最後一點倒不出來時，整座瓶蓋還藏著一個選擇。|C08R36|holding a nearly empty plain flexible condiment bottle at a counter
我想跟著龜甲萬的這一滴，追過六十多年的瓶子改動。|C08R16,C08R32|placing a plain glass dispenser beside a distinct larger flexible bottle
你手裡的瓶子，究竟要讓什麼出去，才能把想留的東西留住？|C08R12,C08R20,C08R36|holding a plain condiment bottle with a thoughtful face toward the viewer
'''),
('大瓶先讓出了餐桌', '''
照公司二〇二〇年的回顧，一九五五年十月，龜甲萬推出了一公升瓶。|C08R07|lifting a plain large glass sauce bottle from a kitchen shelf
它想服務小家庭，可後來收到的聲音，仍希望有更小的容器。|C08R07|comparing a plain large bottle with a small ceramic cruet on a counter
一公升已經變小了，為什麼還不夠？|C08R07,C08R08|looking from a large plain sauce bottle toward a small dining table
設計公司GK的刊物回顧，當年醬油買回來，還得倒進小陶壺才上桌。|A01|pouring sauce from a large plain bottle into a small plain ceramic cruet
裝著商品回家的瓶子，和餐桌上拿來倒的壺，原本分著兩份工作。|A01|placing a large plain sauce bottle behind a small ceramic pouring vessel
如果你只想替盤裡添一點，手裡卻得抱著一個大瓶，動作就不一樣。|C08R07,C08R08|trying to position a large plain glass bottle above a small sauce dish
我原本以為縮小就結束了，可公司想改的，只是容量嗎？|C08R08,C08R17|examining a small ceramic cruet beside an unopened plain glass bottle
龜甲萬後來的說法，是要做一個買回來便能直接放上桌的小容器。|C08R09,C08R17|setting a plain filled glass condiment bottle beside a bowl and a cup
它不只得裝得下醬油，還要像杯盤一樣，成為吃飯時用的器具。|C08R08|arranging a plain glass condiment dispenser among simple bowls and cups
商品瓶要走到餐具旁邊，它該長成什麼樣子？|C08R08,C08R10|studying an empty place beside a bowl with a blank sketch sheet
設計者榮久庵憲司，在二〇〇九年的回述裡，說委託來自一九五八年。|C08R10|opening a blank design folder beside a plain empty glass bottle
題目相當開放：怎麼讓一種存在幾百年的醬油，看起來有新的樣子？|C08R10|looking thoughtfully at a dark sauce bottle above a blank sketchbook
他說，自己曾想過像水龍頭一樣，轉開就能流出醬油。|C08R10|sketching an imagined plain tap on a blank design page
也想過改變醬油的黑色。這些是構想，最後該交到手裡的又是什麼？|C08R10|considering a plain dark sauce sample beside an unfinished blank sketch
但最後要交到使用者手上的，仍是一個能拿、能倒、能放回桌面的瓶子。|C08R11,C08R17|lifting a plain small glass bottle from a dining table
你把它拿起來時，手要抓哪裡？放下時，又靠哪裡站住？|C08R11|holding a plain narrow-necked bottle just above a table
榮久庵說，他把頸部做細，瓶身則往下逐漸變得寬而穩。|C08R11|tracing the narrow neck and wide base of a plain glass bottle
他的想像，是手指握住頸部，手的線條也能好看。|C08R11|holding a plain small glass bottle by its narrow neck
這是設計者對握持的意圖，不是每個人的手都會擺成同一個姿勢。|C08R11|comparing a relaxed hand grip with the narrow neck of a plain bottle
到了一九六一年，公司推出一百五十毫升的玻璃桌上瓶。|C08R16|placing a small plain glass condiment bottle with a red unlettered cap on a table
透明瓶身還讓人看見醬油餘量，不必先打開蓋子猜。|C08R15|looking through a plain transparent glass bottle at the remaining dark sauce
紅蓋與醬油的紅褐色，則是公司後來說明的色彩對比。|C08R15|examining a plain red unlettered cap above dark sauce in a clear glass bottle
它在桌上站好了，手也找到了握的位置，可手一收，嘴尖怎麼辦？|C08R12,C08R14|holding a plain glass dispenser over a small dish just after pouring
'''),
('嘴尖收住了，瓶口還得打開', '''
榮久庵回述這個難題時，先拿茶壺的嘴作比較。|C08R12|comparing a plain teapot spout with a separate dispenser cap sample
他說，像茶壺那樣讓下緣伸出去，醬油仍會往下滴。|C08R12|pointing to the longer lower lip of a plain conceptual spout sample
於是他把上下緣的關係反過來，讓上緣比較突出。|C08R12|examining a plain conceptual dispenser tip with a shorter lower edge
開場你收回手時在意的那一滴，就卡在這個小小的末端。|C08R12,C08R14|looking closely at the end of a plain dispenser tip over a dish
我最喜歡這裡，因為改動看來很小，管的卻是你每次倒完的收手。|C08R12,C08R14|placing a plain glass dispenser upright after pouring into a dish
但是瓶嘴只求不滴，就夠了嗎？|C08R14|holding a plain dispenser tip above a small dish with a measured small pool of sauce
紐約現代美術館後來的展覽標籤說，他做過接近一百個模型。|C08R14|examining a plain cap model among several simple unlettered samples
館方把難題寫成兩件事：防止滴液，還有控制流量。|C08R14|comparing two plain conceptual dispenser tips beside a small sauce dish
榮久庵自己回憶，這個設計前後做了三年，才把樣子與使用合在一起。|A03|examining a finished plain glass dispenser beside a blank sketch folder
它將末端的內傾形狀，和減少醬油留積在嘴尖的結果連起來。|C08R14|pointing to an inward-facing end on an oversized plain conceptual dispenser tip
這是後來策展的解說，不是給每個瓶子開一張永遠零滴的保證。|C08R14|examining an unlettered museum object card beside a plain glass dispenser
可注嘴這麼小，瓶裡用完時，醬油該從哪裡再裝進去？|C08R16,A02|holding an almost empty plain glass dispenser beside a larger refill bottle
再填走的不是注嘴。整個紅蓋拿下，露出的才是補充口。|A02,C08R16|removing a whole plain red cap from a glass dispenser to expose its wide mouth
GK刊物說，這個口比一升八大瓶的瓶口還稍寬，方便補充。|A02|comparing the open mouth of a small plain dispenser with a larger bottle mouth
你倒給盤子時，要的是小而俐落的出口；補進瓶子時，手卻需要較寬的入口。|A02,C08R12|positioning a large plain refill bottle above the wide mouth of a small dispenser
同一個蓋子，拿起來再填時，手又會碰到哪裡？|A02,C08R18|holding a plain detached cap beside an open glass bottle
到二〇〇七年度，歐洲子公司KFE的報告，還記下一個蓋子的改動。|C08R18|examining a plain detached dispenser cap beside a blank report folder
蓋上的凸起被改成圓角，目的是避免開蓋、再填時傷到手。|C08R18|touching a rounded protrusion on a plain detached dispenser cap
這個改動針對的是當時歐洲子公司，沒有被說成所有地方一起換版。|C08R18|placing one plain rounded cap sample beside an unlettered regional report folder
看瓶子的設計，不能只看它倒下來那幾秒；用完還有人得把蓋子拿起來。|A02,C08R18|holding a plain red cap above a small empty glass dispenser
那瓶身透明，裡頭的東西就一定能一直保持剛開的樣子嗎？|C08R15,C08R26|looking through a plain glass bottle at the dark sauce remaining inside
後來另一款醬油對保鮮提出的要求，讓瓶子碰到一個不同的問題。|C08R23,C08R26|placing a separate sealed sauce pouch beside an older plain glass dispenser
'''),
('保鮮袋碰到了放手的問題', '''
生醬油的這個新問題，恩田友貴在二〇二五年的公司訪談裡講得很直接。|C08R26|an anonymous product specialist examining a plain sealed sauce pouch
他說，這款生醬油沒有經過一般的火入加熱，而以特殊過濾去除微生物。|C08R26|an anonymous technician examining a plain filter sample beside a sealed sauce container
但它的色澤和香氣一碰到空氣，仍會改變。|C08R26|an anonymous product specialist comparing plain closed sauce samples on a bench
你即使沒把醬油滴到桌上，瓶裡的風味也還有另一道關要過。|C08R26|an anonymous cook setting a closed plain sauce container beside a clean dish
我在意的是，醬油還沒用完，風味卻可能先改變。|C08R26|an anonymous reader examining a plain dispenser beside a sealed pouch sample
要讓醬油出來，又不讓空氣跟著進去，原來的瓶子該怎麼變？|C08R20,C08R26|an anonymous designer examining a plain sauce container above a blank sketch
照二〇一一年的公告，龜甲萬已經研究密封容器超過十年。|C08R23|an anonymous researcher sorting plain container prototypes on a workbench
在二〇一〇年，它先推出裝五百毫升的密封軟袋。|C08R23|an anonymous cook setting a plain upright flexible sauce pouch on a counter
可是醬油少了之後，這個軟袋還能讓你放心放手嗎？|C08R24|an anonymous cook holding a partly emptied plain flexible pouch at a counter
恩田後來回憶，軟袋剩少時不容易自己站住，也有人想單手開蓋。|C08R24|an anonymous cook holding a partly collapsed plain pouch beside an empty space on a counter
想像你正在料理，一手還忙著拿東西，另一手要放開袋子。|C08R24|an anonymous cook holding a plain sauce pouch in one hand beside a simple bowl
如果它得靠手一直扶著，少掉的就不只是一點重量。|C08R24|an anonymous cook steadying a partly emptied plain sauce pouch upright
那能不能讓外形站住，裡面卻仍保留隔絕空氣的安排？|C08R20,C08R21,C08R24|an anonymous designer holding a plain rigid outline model beside a soft pouch
公司改與容器廠來回開發瓶型，恩田說，這一段十個月就商品化。|C08R25|an anonymous developer comparing a soft plain pouch with a separate flexible bottle prototype
二〇一一年七月的公告，預告新兩百毫升瓶要在八月十日推出。|C08R19|an anonymous shop worker placing a small plain flexible sauce bottle on an unlettered shelf
第一款的外形沿著舊紅蓋桌上瓶的線索，手裡卻換成可擠壓的新瓶。|C08R20,C08R25|an anonymous adult holding a small plain flexible bottle with an unlettered cap beside a separate glass dispenser
瓶蓋又要怎麼回應，料理時那隻騰不出的手？|C08R22,C08R24|an anonymous cook looking at the plain hinged lid of a small flexible bottle
公司把一按便能開的蓋子，列為這個新瓶的功能。|C08R22|an anonymous cook opening a plain hinged bottle lid with one hand
公司也把按壓控量，列成這個新瓶的功能。|C08R22|an anonymous cook gently pressing a small plain flexible bottle over a sauce dish
當年的這款新瓶，還以開栓後常溫維持鮮度九十天，作為公司的功能主張。|C08R22|an anonymous cook placing a closed small plain flexible bottle upright on a counter
你要少一點，就調整手裡的力；醬油不再只跟著瓶子傾斜而出。|C08R22|an anonymous cook adjusting a gentle grip on a plain flexible sauce bottle
可是當你的手放鬆，瓶子還得恢復可繼續使用的樣子。|C08R21|an anonymous cook releasing a grip on a small plain flexible bottle
空氣究竟該進哪裡，才不會把保鮮的工作一起拆掉？|C08R20,C08R21|an anonymous developer examining a plain two-layer container demonstration model
'''),
('空氣改走了外面那一層', '''
這一代新瓶，在外瓶裡，另外放了一個裝醬油的內袋。|C08R20|an anonymous technician holding a plain conceptual outer bottle beside a separate soft inner pouch
醬油往外倒，內袋隨著內容減少縮小。|C08R20,C08R21|an anonymous technician examining a partly shrunken inner pouch inside a plain demonstration shell
公告說，出去多少醬油，便有相當量的空氣進入外瓶和內袋之間。|C08R21|an anonymous technician pointing to the gap between a plain outer shell and a shrinking inner pouch
空氣填的是袋子外側，所以外瓶不必跟著醬油一起扁下去。|C08R21|an anonymous technician holding a plain outer bottle with a smaller inner pouch visible
我差點把這句看成空氣回到醬油裡，位置一換，事情就完全不同。|C08R21|an anonymous reader comparing the inner pouch with the space outside it in a simple model
那瓶蓋怎樣分辨，該讓出去的是液體，還是該讓回來的是空氣？|C08R20|an anonymous technician examining a plain conceptual cap above separate liquid and air path models
公告稱它採雙逆止閥的蓋子，讓醬油通過，卻不讓空氣進入醬油內袋。|C08R20|an anonymous technician holding a plain conceptual two-valve cap model over an inner pouch
可是袋裡的液體出去了，注嘴裡剩下的那一點，又由誰照顧？|P1|an anonymous technician examining a small residual pool inside a plain conceptual outlet model
後來的官方教材，把兩百毫升密封桌上瓶，連到一份日本專利。|P1,P2,P7|an anonymous researcher opening a blank technical folder beside a small plain flexible bottle
原件在二〇一五年登錄，描述的是一套特定的容器與液閥結構。|P1|an anonymous researcher examining a plain elastic valve demonstration part beside blank pages
以下看的是這份方案，並不是每一款現售瓶蓋都照同一張剖面。|P1|an anonymous researcher comparing a conceptual valve model with several plain closed bottle caps
文件要處理的，是液體沒有回到內器、卻留在出口附近而可能漏出的情況。|P1|an anonymous technician pointing to residual liquid inside a plain conceptual dispensing cap model
只把通往內袋的路關住，嘴口裡的殘液就會自己消失嗎？|P1|an anonymous technician inspecting a plain closed liquid valve with residual liquid beyond it
按這個方案，手擠壓時，內部壓力會推動有彈性的液閥。|P1|an anonymous technician pressing a simple flexible demonstration bottle connected to a valve model
閥件沿著通道的方向移動，開出讓內容物流過的路。|P1|an anonymous technician moving a plain axial valve demonstration part along a short channel model
閥件移多遠，也另有一個限制位移的部位管著。|P1|an anonymous technician pointing to a stop beside a plain elastic valve demonstration model
你一鬆手，壓力減弱，閥件便開始往內側回復。|P1|an anonymous technician releasing a plain elastic valve demonstration model
它先把連通孔關住，之後繼續回移，讓蓋內一處空間變大。|P1|an anonymous technician examining a widening chamber behind a plain closed valve model
這一點移動，要怎麼管到嘴尖？|P1|an anonymous technician looking closely at a plain valve model connected to an outlet tip
文件說，擴大的空間能把出口內的殘液往裡拉，減少它留在嘴口。|P1|an anonymous technician examining liquid drawn from an outlet into a plain cap chamber model
這裡拉入的是蓋內空間，不能直接說成把每一滴都吸回裝醬油的袋子。|P1|an anonymous technician pointing to a small cap chamber separate from a plain inner pouch
外界空氣能被吸進吐出口，讓嘴端少留殘液，連回內袋的孔卻已關閉。|P1|an anonymous technician pointing to an open outlet tip beyond a closed inner valve in a plain model
專利也把空氣閥與外側進氣通道列進構造，讓進氣和液閥各有自己的工作。|P1|an anonymous technician arranging separate plain air valve and liquid valve demonstration pieces
那手沒有擠瓶子、外蓋已關上時，液閥還需要管嗎？|P1|an anonymous technician lowering a plain outer cover over a conceptual valve model
文件另有含外蓋的構造，外蓋內側的密封部，也負責抑制液閥的彈性移動。|P1|an anonymous technician pointing to a plain cover insert above an elastic valve model
但把內袋藏好之後，你一眼還看得見它嗎？|C08R27,C08R32|an anonymous adult examining a clear flexible sauce bottle against a plain background
到了二〇一八年的四百五十毫升環保瓶，公司把主要材料從PE換成PET。|C08R27|an anonymous technician holding a larger plain clear flexible bottle beside plain polymer samples
這代也把標籤做成可剝離，讓用完後的分離動作進入容器安排。|C08R27|an anonymous adult peeling a blank label from an empty clear flexible bottle
這是後來的一代瓶型，不能拿它的材料，倒回去解釋早年的玻璃瓶。|C08R27,C08R16|an anonymous adult comparing a larger clear flexible bottle with a separate small glass dispenser
瓶子裡那個會變小的袋子，也把新的使用感帶回你的手裡。|C08R32,C08R33|an anonymous adult gently pressing a larger clear flexible sauce bottle with a small inner pouch visible
'''),
('最後一點，換了保存方式', '''
現行四百五十毫升密封瓶的FAQ，回答了一個很像沒做好的問題。|C08R32|an anonymous adult looking closely at a plain clear flexible sauce bottle
有人看著透明瓶身，覺得裡面根本沒有第二層。|C08R32|an anonymous adult holding a full plain clear flexible bottle up to soft light
公司解釋，內袋和外瓶都是透明PET，剛開始本來就不容易分辨。|C08R32|an anonymous technician comparing a clear inner pouch with a plain transparent outer bottle
約用到半瓶，內袋縮小，兩層之間的差別才比較看得出來。|C08R32|an anonymous adult examining a half-used plain clear bottle with a smaller inner pouch visible
我覺得這個反差很有趣：用掉一部分，才比較能看見裡頭原本就有的東西。|C08R32|an anonymous adult comparing a full clear bottle with a partly used clear demonstration bottle
如果連袋內都看見了氣層，難道又是外面漏進去了？|C08R34|an anonymous adult examining a small gas space inside a plain sealed pouch demonstration model
目前另一則FAQ解釋，內袋還封入了氮氣，來幫助醬油推出。|C08R34|an anonymous technician holding a sealed plain pouch with a small internal gas space
公司說，這種氣體不會讓醬油氧化；看見氣體，不等於看見外界空氣已漏入。|C08R34|an anonymous technician examining a plain sealed pouch beside an intact valve model
這則FAQ還說，瓶子傾斜時，氮氣移動可能帶來小小振動，傳到手上。|A04|an anonymous adult gently tilting a plain sealed flexible sauce bottle while feeling its movement
可是同樣的一隻手，用到後來，為什麼又覺得比較難擠？|C08R33|an anonymous cook gently pressing a partly used plain flexible sauce bottle
另一則FAQ說，袋子越縮小，手的力就逐漸隔著層間空氣，間接去壓內袋。|C08R33|an anonymous technician pointing to the air gap around a small pouch inside a plain demonstration bottle
傳力的方式跟著改變，所以公司要使用者依剩量調整按壓的力道。|C08R33|an anonymous cook adjusting a grip on a partly emptied plain flexible bottle
這不是一條精確的壓力刻度，而是瓶子在你使用途中留下的取捨。|C08R33|an anonymous cook considering a partly empty plain bottle beside a small dish
手放開之後，瓶蓋能不能立刻按回去？|C08R37|an anonymous cook pausing before closing a plain hinged bottle lid
現行這款的官方說明，是用完先直立放幾秒，再關蓋。|C08R37|an anonymous cook leaving a plain flexible bottle upright on a kitchen counter
嘴內的醬油較容易回到瓶內，關蓋時被擠出的量就能減少。|C08R37|an anonymous cook gently closing the plain hinged lid of an upright sauce bottle
平常翻開上蓋來倒，和把底座整個卸下，是兩種不同的開法。|C08R36,C08R37|an anonymous adult comparing a plain hinged lid with a separate whole cap base from a flexible bottle
現行這款瓶的保鮮目安，官網寫的是開栓後常溫一百二十天。|C08R38|an anonymous adult setting a closed plain flexible bottle beside a blank kitchen calendar
部分產品另有例外；這是公司的鮮度目安，不是每瓶安全使用期限的保證。|C08R38|an anonymous adult examining a plain closed bottle beside an unlettered product information card
你要的最後一點，若仍留在裡面，還有沒有別的拿法？|C08R36|an anonymous cook looking at a very small amount of sauce in a plain flexible bottle
官方FAQ說，剩很少時，可以從上方看，往右轉動整座蓋子。|C08R36|an anonymous adult rotating the whole cap base of a nearly empty plain bottle clockwise
蓋子會連底座一起卸下，瓶裡那一點便能再取出來。|C08R36|an anonymous adult lifting a detached cap base from a nearly empty plain flexible bottle
但這個動作也會切斷密封；取下以後，官方要求改放冰箱。|C08R36|an anonymous adult placing an opened plain sauce bottle inside a refrigerator
同一隻手想把殘量拿乾淨，就得接受保存方式跟著變。|C08R36|an anonymous cook holding the detached cap base beside an opened plain bottle
它並不是鼓勵你反覆拆蓋，再當成仍然完整密封的瓶子放回去。|C08R36|an anonymous adult examining an opened plain bottle with its whole cap base removed
等醬油真的用完，裡頭那個袋子，還得伸手挖出來嗎？|C08R35|an anonymous adult examining an empty clear flexible bottle with a small inner pouch
目前官方的答案是不必。內袋和外瓶同是PET，不用拆成兩件。|C08R35|an anonymous adult placing an empty clear outer bottle with its inner pouch intact on a sorting table
蓋子則另外分開，實際的資源回收還要照住處的規則處理。|C08R35|an anonymous adult placing a detached plain cap beside an empty clear bottle on a sorting table
瓶子最終離開餐桌的時候，手上的工作才算走到另一個邊界。|C08R27,C08R35|an anonymous adult carrying separated plain bottle and cap pieces toward a sorting area
開場你想留下的那一滴，最後連著的，是瓶子允許你開哪一個口、又得重新守哪一道界線。|C08R12,C08R36|an anonymous adult holding a plain empty bottle beside a small dish
如果是你，會為了取出最後一點而拆開密封、改放冰箱，還是讓它停在那裡？留言告訴我。||an anonymous adult considering a nearly empty plain bottle with a thoughtful face toward the viewer
訂閱品牌故事，我們繼續看日用品怎麼把看不見的取捨，放進你的每一個動作。||an anonymous narrator setting a plain empty condiment bottle on a simple table
'''),
]

catalog={s['id']:s for s in research['source_catalog']}
# The source locates Onda in product-development work; the room name is not a managerial rank.
catalog['K7']['title']='Kikkoman interview with product-development staff Tomotaka Onda'
anchors={c['id']:c for c in research['claims']}
anchors['A01']={'id':'A01','claim':'Design-firm retrospective describes transfer from a 1.8-litre purchased bottle into a small ceramic cruet; new theme was a mass-producible filled sauce receptacle usable directly at table.','limits':'GK Report34 2018.10 author Kozo Yamada, not established as original participant. Anonymous conceptual scene, not a household population survey.','evidence':[{'source':'R1','locator':'PDF/printed p23; original scan author viewed','short_quote':'Housewives poured small amounts of sauce into a small ceramic soy sauce cruet for use on the table.','raw_sha256':catalog['R1']['sha256'],'visual_page':'/workspace/work/brand-story-20261025/c08-audit/source-cache/R1-page-23.png'}]}
anchors['A02']={'id':'A02','claim':'Whole cap removal exposes refill mouth described as slightly wider than a 1.8-litre bottle mouth, allowing easy refilling.','limits':'GK Report34 p24 original scan; refillable 1961-lineage glass dispenser, not sealed 2011/current PET bottle.','evidence':[{'source':'R1','locator':'PDF/printed p24; original scan author viewed','short_quote':'When the cap is removed, the width of the mouth of the bottle is a little wider than that of a 1.8 liter bottle to allow easy refilling.','raw_sha256':catalog['R1']['sha256'],'visual_page':'/workspace/work/brand-story-20261025/c08-audit/source-cache/R1-page-24.png'}]}
anchors['A03']={'id':'A03','claim':'Ekuan said in his 2009 first-person retrospective that the design combining appearance and use took three years.','limits':'Retrospective duration, not an original prototype/testing ledger.','evidence':[{'source':'E1','locator':'paragraph28','short_quote':'そういうデザインを3年がかりで作り上げたのです','raw_sha256':catalog['E1']['sha256']}]}
anchors['A04']={'id':'A04','claim':'Current official FAQ explains that nitrogen movement when the bottle is tilted can cause small vibrations felt in the hand.','limits':'Current sealed bottle FAQ account; not a physics experiment, not a finding about 1961 glass bottles or every possible vibration.','evidence':[{'source':'F4','locator':'complete FAQ article body, after nitrogen inclusion explanation','short_quote':'傾けると窒素ガスが動くために小さな振動が起こってそれが手に伝わります','raw_sha256':catalog['F4']['sha256']}]}
patent_source_names={'P1':'JP5727888B2.pdf','P2':'jpaa-design-pamphlet.pdf','P7':'inpit-ipmix.pdf'}
for pid,filename in patent_source_names.items():
 raw=next(s for s in patents['sources'] if s['name']==filename)
 catalog[pid]={'id':pid,'title':filename,'url':raw['url'],'raw_path':raw['local_path'],'sha256':raw['sha256'],'source_type':'original_granted_patent' if pid=='P1' else 'official_educational_product_bridge','publication_date_scope':'2015 registration / B2 publication distinct' if pid=='P1' else 'later official educational material; not 1961 filing'}
 finding=next(f for f in patents['findings'] if f['id']==pid)
 anchors[pid]={'id':pid,'claim':finding.get('safe_scope'),'limits':finding.get('limitation',finding.get('safe_scope')),'evidence':[{'source':pid,'locator':json.dumps(finding['precise_locators'],ensure_ascii=False),'short_quote':finding.get('title',filename),'raw_sha256':raw['sha256']}]}

# Frozen research expansion is evidence material, never an inherited SOURCE PASS.
EXPANSION_SHA={
 'research.md':'5b90d34f0c6733c0f9cacda16f1dd5be77092309208723db90cd2e331efe6610',
 'claims.json':'e51b59d2b54e53fce834853963c89f762b2ca0653ae53f2fc6cd1dd32fa299ff',
 'source-receipts.json':'867f5a58592a5350beacf0adebe92b980993eeb096e84afa0e16c8f23a701bc5',
}
for filename,expected in EXPANSION_SHA.items():assert sha(OUT/'research-expansion'/filename)==expected,filename
expansion=json.loads((OUT/'research-expansion/claims.json').read_text())
expansion_receipts=json.loads((OUT/'research-expansion/source-receipts.json').read_text())
for source in expansion_receipts['sources']:
 if source['id'] not in catalog:
  catalog[source['id']]={'id':source['id'],'title':'JP5053463B2 applicant-reported soft-film prototype tests' if source['id']=='P505' else source.get('title',source['id']),'url':source.get('article_url',source['url']),'raw_path':source['raw_path'],'sha256':source['sha256'],'source_type':source['source_type'],'publication_date_scope':source['publication_date_scope']}
for material in expansion['claims']:
 anchors[material['id']]={'id':material['id'],'claim':material['claim'],'limits':material['product_and_time_scope']+' '+json.dumps(material['not_supported'],ensure_ascii=False),'evidence':[{'source':e['source_id'],'locator':e['locator'],'short_quote':e['exact_short_quote'],'raw_sha256':e['raw_sha256'],'quote_sha256':e['quote_sha256'],'extracted_page_sha256':e['extracted_page_sha256'],'actual_original_path':e['raw_path']} for e in material['evidence']]}
anchors['A05']={'id':'A05','claim':'Company interview describes the sealed bottle as adjustable by hand pressure in one-drop units; opening uses one drop as the viewer desired quantity, not a universal measured guarantee.','limits':'K7 PDF p3 retrospective company feature description. Opening glass action is an anonymous viewer scene; do not transfer the sealed-bottle mechanism to1961glass.','evidence':[{'source':'K7','locator':'PDFp3 first two paragraphs; author directly read actual page text','short_quote':'押す力の加減で、1 滴単位で好きな分量を出せる','raw_sha256':catalog['K7']['sha256'],'page_text_path':'/workspace/work/brand-story-20261025/c08-audit/length-research/K7-p3.txt','page_text_sha256':'d2b91cd078796467c35a9f53d267c8f65213b27d8e3c6252926710d49bf5ce58'}]}

scenes=[]
claims=[]
lines=[]
chapters=[]
cameras=['push in','pan left','pull out','tilt down','pan right','tilt up']
sizes=['Medium shot','Close-up','Wide shot','Medium close-up']
places=['at a small dining table','in a modest kitchen beside a dining table','at a simple design workbench','in a plain kitchen preparation area','at a plain container development bench','beside a home kitchen counter']
lights=['soft overhead light','mild light from an open doorway','gentle desk lamp light','soft overcast light from the left']
for ci,(chapter,body) in enumerate(CHAPTERS):
 chapter_ids=[]
 for li,row in enumerate(body.strip().splitlines()):
  text,ids,action=row.split('|')
  ids=[x for x in ids.split(',') if x]
  sid=f'c08r1-{ci+1:02d}-{li+1:02d}'
  lid=f'c8r1{ci+1:02d}{li+1:02d}'
  line={'id':lid,'text':text,'emotion':'對一個人說書，自然有起伏，問句上揚'}
  if text.startswith('我'):line['emotion']='像跟朋友分享發現，語氣有反應'
  actor_action=('one '+action[3:]) if action.startswith('an ') else 'one anonymous adult '+action
  prompt=f'{sizes[(li+ci)%4]} {places[ci]}, {actor_action}, {lights[(li+2*ci)%4]}.'
  scene={'id':sid,'template':'shot','data':{'prompt':prompt,'visual':'still','camera':cameras[(li+ci)%6]},'lines':[line]}
  if li==0:scene['chapter']=chapter
  scenes.append(scene)
  source_ids=list(dict.fromkeys(e['source'] for a in ids for e in anchors[a]['evidence']))
  evidence=[{'anchor_id':a,'claim_scope':anchors[a]['claim'],'limits':anchors[a]['limits'],'source_locator':e, 'original':{k:catalog[e['source']].get(k) for k in ['id','title','url','raw_path','sha256','source_type','publication_date_scope']}} for a in ids for e in anchors[a]['evidence']]
  mode='source_bound_narration_pending_independent_review'
  if not ids:mode='viewer_question_or_subscription_invitation_not_factual_claim'
  elif text.startswith(('你','如果','想像','同一','它不只','但最後','這不是','等醬油','我','開場')):mode='viewer_hypothesis_or_editorial_explanation_with_bound_factual_limits; not a documented individual scene'
  record={'id':lid,'scene':sid,'chapter':chapter,'text':text,'anchor_ids':ids,'source_ids':source_ids,'evidence':evidence,'narrative_mode':mode,'not_source_pass':True,'written_visual':{'scene':sid,'prompt':prompt,'mode':'anonymous conceptual illustration; separate glass, 2011 squeeze, and current PET lineages, not an exact marketed-product cutaway','review_state':'NOT_REVIEWED'}}
  claims.append(record)
  lines.append({'id':lid,'text':text})
  chapter_ids.append(lid)
 chapters.append({'title':chapter,'line_ids':chapter_ids})

# r2 responds only to the two shared mandatory failures, chapters_link/no_recap.
# Keep the frozen r1 row IDs and all unaffected words/settings. Do not re-number after deletion.
R1_INPUTS={
 'video.json':'478496f1ef0f5f64680a5e34a34e01c4092f223be885a6bb6af608cae2bb0a3c',
 'script.md':'4c8cf7f9258ad84bd8e4fb4182094d5a9daabf52bf185952cae4b85ae1e69397',
 'narration-only.json':'23b4486a3a59c3e477df25ac1df9d88bb386626ab8497fab85aeaf4c63c60dd1',
 'claims.json':'57f5a58281ac9c6d2d2188813ab5f2eeccbf0140f9a78852c52046256f54f2be',
}
for filename,expected in R1_INPUTS.items():
 assert sha(OUT/'history/r1'/filename)==expected,filename
R2_TEXT={
 'c8r10204':'玻璃小瓶出現以前，你先把大瓶醬油倒進小陶壺，才把它端上餐桌。',
 'c8r10201':'一九五五年十月，龜甲萬推出給小家庭的一公升瓶。',
 'c8r10203':'可是仍有人想要更小的容器，一公升為什麼還不夠？',
 'c8r10211':'榮久庵憲司後來回憶，一九五八年，他接到了這個委託。',
 'c8r10401':'你拿起另一款生醬油，倒完放回桌上，剩下的還得等下一次取用。',
 'c8r10402':'公司主管恩田友貴後來解釋，這款醬油省去火入加熱，改用特殊過濾去除微生物。',
}
R2_DELETE={'c8r10202','c8r10322','c8r10603'}
for scene in scenes:
 for line in scene['lines']:
  if line['id'] in R2_TEXT:line['text']=R2_TEXT[line['id']]
scenes=[s for s in scenes if not any(l['id'] in R2_DELETE for l in s['lines'])]
moved=next(s for s in scenes if s['lines'][0]['id']=='c8r10204')
scenes.remove(moved)
chapter_start=next(i for i,s in enumerate(scenes) if s['lines'][0]['id']=='c8r10201')
moved['chapter']=scenes[chapter_start].pop('chapter')
scenes.insert(chapter_start,moved)
new_trigger=next(s for s in scenes if s['lines'][0]['id']=='c8r10401')
new_trigger['data']['prompt']='Medium close-up in a plain kitchen preparation area, one anonymous cook setting a plain sealed sauce pouch upright beside a small sauce dish, soft overcast light from the left.'
claim_map={c['id']:c for c in claims}
claims=[]
lines=[]
chapters=[]
for scene in scenes:
 if scene.get('chapter'):chapters.append({'title':scene['chapter'],'line_ids':[]})
 for line in scene['lines']:
  record=claim_map[line['id']]
  record['text']=line['text']
  record['written_visual']['prompt']=scene['data']['prompt']
  if line['id']=='c8r10204':
   record['narrative_mode']='bounded illustrative pre-1961 household transfer action; retrospective source class retained in evidence, not a newly documented individual'
  if line['id']=='c8r10401':
   record['narrative_mode']='viewer use scenario for the separately named raw-soy-sauce product; no newly documented person, experiment, or inferred psychology'
  claims.append(record)
  lines.append({'id':line['id'],'text':line['text']})
  chapters[-1]['line_ids'].append(line['id'])

# r3: one source-role correction and only the shared chapters_link/no_recap/no_detour.
# Environmental disassembly material remains in frozen research, not as a second narration thread.
R2_INPUTS={
 'video.json':'eacc578080f00d164221496c7061af1bd81ce07f24b9f68c327e9eac49292964',
 'script.md':'bee3726ceed3ab1506fffbdaf977c6f7123ef97bb1ad66c1f17441bfb8da1e32',
 'narration-only.json':'a3dee011045493e60160a5361ac59d1a80fe39f1c90556af7128da1c740b7810',
 'claims.json':'4dc8157c8420accbb75e92d6a8602486a613624a97ad023a5890d40f0a3a0273',
}
for filename,expected in R2_INPUTS.items():assert sha(OUT/'history/r2'/filename)==expected,filename
R3_TEXT={
 'c8r10402':'龜甲萬的產品開發人員恩田友貴後來解釋，這款醬油省去火入加熱，改用特殊過濾去除微生物。',
 'c8r10406':'這讓我想問：你要讓醬油出去，又不讓空氣進去，原來的瓶子該怎麼變？',
 'c8r10508':'我更想看，你已經鬆手了，注嘴裡剩下的那一點，又會去哪裡？',
 'c8r10520':'文件說，擴大的空間能把嘴端殘液拉進蓋內，這個位置和裝醬油的內袋分開。',
 'c8r10522':'外界空氣，此時能被吸進吐出口。',
 'c8r10526':'你拿起透明的密封瓶，裡面的內袋，一眼就看得出來嗎？',
 'c8r10527':'二〇一八年，公司在四百五十毫升的新瓶，把主要材料從PE換成PET。',
 'c8r10601':'你拿起現行四百五十毫升密封瓶，透明瓶身裡卻一時看不出那個內袋。',
 'c8r10608':'公司說，內袋裡的氮氣不會讓醬油氧化。',
 'c8r10619':'部分產品另有例外。',
 'c8r10620':'我還想知道，你要的最後一點留在裡面時，還有沒有別的拿法？',
}
R3_DELETE={
 'c8r10311','c8r10319',
 'c8r10404','c8r10405',
 'c8r10504','c8r10505','c8r10511','c8r10521','c8r10528','c8r10529','c8r10530',
 'c8r10602','c8r10605','c8r10613','c8r10624','c8r10625','c8r10626','c8r10627','c8r10628','c8r10629',
}
for scene in scenes:
 for line in scene['lines']:
  if line['id'] in R3_TEXT:line['text']=R3_TEXT[line['id']]
scenes=[s for s in scenes if not any(l['id'] in R3_DELETE for l in s['lines'])]
material=next(s for s in scenes if s['lines'][0]['id']=='c8r10527')
scenes.remove(material)
visibility_at=next(i for i,s in enumerate(scenes) if s['lines'][0]['id']=='c8r10526')
scenes.insert(visibility_at,material)
claim_map={c['id']:c for c in claims}
claims=[]
lines=[]
chapters=[]
for scene in scenes:
 if scene.get('chapter'):chapters.append({'title':scene['chapter'],'line_ids':[]})
 for line in scene['lines']:
  record=claim_map[line['id']]
  record['text']=line['text']
  if line['id']=='c8r10402':record['role_scope']='K7 describes product-development work, not a managerial rank; retrospective attribution retained.'
  if line['id']=='c8r10601':record['narrative_mode']='bounded viewer-use scenario for the current450mL bottle; not a new customer test or testimonial'
  if line['id'] in ['c8r10406','c8r10508','c8r10620']:record['narrative_mode']='narrator curiosity at an unresolved physical use question, not a repeated factual summary or an invented personal test'
  if line['id'] in ['c8r10520','c8r10522']:record['mechanism_scope']='Specific2015-granted patent cap-internal space; do not merge with the current PET bottle interlayer-air pressure mechanism.'
  claims.append(record)
  lines.append({'id':line['id'],'text':line['text']})
  chapters[-1]['line_ids'].append(line['id'])

# r4 removes only the shared no_recap sentence. Its function was already delivered
# by 10419; 10421 is not a loop endpoint. Retained text, images and cues stay fixed.
R3_INPUTS={
 'video.json':'1ff4baebc7feb689ee45c240a9b3d9417e3a37b121b2fdcd698cc87c6a8e2af0',
 'script.md':'dc31efca261f3eb1019f3bf385822aa602e05a8acf998c080f5e10e0a5a176da',
 'narration-only.json':'7b5005f8d8ef66fefd0b3e5fd2084b304c68ce9e0814a3113634d301fbbc640d',
 'claims.json':'06580afc5485f2da824f8bb36c4de443d42675e9f04b37fbd4a485d490a07463',
}
for filename,expected in R3_INPUTS.items():assert sha(OUT/'history/r3'/filename)==expected,filename
R4_DELETE={'c8r10421'}
R4_ROLE_SCOPES={
 'C08R24':'2025具名商品開發人員回述軟袋內容減少不自立，使用者希望單手開蓋',
 'C08R25':'2025商品開發人員說與容器廠合作十個月商品化，首200mL外觀沿舊紅蓋線索',
 'C08R26':'2025公司訪談中的商品開發人員恩田友貴解釋生醬油省火入，特殊過濾除微生物，空氣改色香',
}
scenes=[s for s in scenes if not any(l['id'] in R4_DELETE for l in s['lines'])]
claim_map={c['id']:c for c in claims}
claims=[]
lines=[]
chapters=[]
for scene in scenes:
 if scene.get('chapter'):chapters.append({'title':scene['chapter'],'line_ids':[]})
 for line in scene['lines']:
  record=claim_map[line['id']]
  for evidence in record['evidence']:
   if evidence['anchor_id'] in R4_ROLE_SCOPES:evidence['claim_scope']=R4_ROLE_SCOPES[evidence['anchor_id']]
  claims.append(record)
  lines.append({'id':line['id'],'text':line['text']})
  chapters[-1]['line_ids'].append(line['id'])

# r5 is limited to the shared no_recap observations. Keep the current-product
# condition and the concrete visibility obstacle; the capacity was already named.
R4_INPUTS={
 'video.json':'1ffd0235458af16c85bd2e62e8e4d55cb4b96abf89e5c0240b0ee7ef2462de6f',
 'script.md':'2222d15b789379c1742890a881d63c1b2aeb2822b269d46dce82213da8a1308f',
 'narration-only.json':'a55cf360762f776658082e4dc079f44273fd8172287360e2f673d253a0e9ee04',
 'claims.json':'b647932b55eaa1465ccbefd90dd202e7c16a489781a190b14f57c283b1e1a809',
}
for filename,expected in R4_INPUTS.items():assert sha(OUT/'history/r4'/filename)==expected,filename
R5_DELETE={'c8r10320'}
R5_TEXT={'c8r10601':'你拿起現行這款密封瓶，透明瓶身裡卻一時看不出那個內袋。'}
scenes=[s for s in scenes if not any(l['id'] in R5_DELETE for l in s['lines'])]
claim_map={c['id']:c for c in claims}
claims=[]
lines=[]
chapters=[]
for scene in scenes:
 if scene.get('chapter'):chapters.append({'title':scene['chapter'],'line_ids':[]})
 for line in scene['lines']:
  if line['id'] in R5_TEXT:line['text']=R5_TEXT[line['id']]
  record=claim_map[line['id']]
  record['text']=line['text']
  claims.append(record)
  lines.append({'id':line['id'],'text':line['text']})
  chapters[-1]['line_ids'].append(line['id'])

# r6 restores substantive action/results from a separately identified prototype
# case and current use guidance, while repairing only the shared opening/recap.
R5_INPUTS={
 'video.json':'aa4141c8ba7589ec6e6084b77e9f8cb6740fe7b35bc6ef2c790f84697f727232',
 'script.md':'de9dfcd98a527b5a689b4dd71dc56d49100a94fcb9a11414a35c0657cf1b299e',
 'narration-only.json':'94c280be06a865135651846829d9d4b02452686be4744379d10aa4114589cf7e',
 'claims.json':'cb58a45cfc8e594b6f3f311c9e2cb6f008d06b0c5e1c4245a4fed171705625ba',
}
for filename,expected in R5_INPUTS.items():assert sha(OUT/'history/r5'/filename)==expected,filename
r6=json.loads((OUT/'r6-materials.json').read_text())
R6_DELETE=set(r6['delete'])
scenes=[s for s in scenes if not any(l['id'] in R6_DELETE for l in s['lines'])]
claim_map={c['id']:c for c in claims}
for scene in scenes:
 for line in scene['lines']:
  if line['id'] in r6['texts']:
   line['text']=r6['texts'][line['id']]
   claim_map[line['id']]['text']=line['text']
  if line['id'] in ['c8r10101','c8r10102']:
   record=claim_map[line['id']]
   ids=['A05'] if line['id']=='c8r10101' else ['C08R16']
   record['anchor_ids']=ids
   record['source_ids']=list(dict.fromkeys(e['source'] for a in ids for e in anchors[a]['evidence']))
   record['evidence']=[{'anchor_id':a,'claim_scope':anchors[a]['claim'],'limits':anchors[a]['limits'],'source_locator':e,'original':{k:catalog[e['source']].get(k) for k in ['id','title','url','raw_path','sha256','source_type','publication_date_scope']}} for a in ids for e in anchors[a]['evidence']]
   if line['id']=='c8r10101':record['narrative_mode']='viewer wants one drop; question, not measured historical accident or universal glass-bottle dispensing claim'
  if line['id']=='c8r10103':claim_map[line['id']]['narrative_mode']='bounded viewer handling scene for the explicitly dated1961glass object, not a recorded historical user or a filmed experiment'
for block in r6['blocks']:
 at=next(i for i,s in enumerate(scenes) if any(l['id']==block['target'] for l in s['lines']))
 chapter=next(s['chapter'] for s in reversed(scenes[:at+1]) if s.get('chapter'))
 added=[]
 for index,row in enumerate(block['rows']):
  sid='c08r6-'+row['id'][4:]
  line={'id':row['id'],'text':row['text'],'emotion':'對一個人說書，自然有起伏，問句上揚'}
  scene={'id':sid,'template':'shot','data':{'prompt':row['prompt'],'visual':'still','camera':cameras[index%len(cameras)]},'lines':[line]}
  ids=row['anchor_ids'];source_ids=list(dict.fromkeys(e['source'] for a in ids for e in anchors[a]['evidence']))
  evidence=[{'anchor_id':a,'claim_scope':anchors[a]['claim'],'limits':anchors[a]['limits'],'source_locator':e,'original':{k:catalog[e['source']].get(k) for k in ['id','title','url','raw_path','sha256','source_type','publication_date_scope']}} for a in ids for e in anchors[a]['evidence']]
  record={'id':line['id'],'scene':sid,'chapter':chapter,'text':line['text'],'anchor_ids':ids,'source_ids':source_ids,'evidence':evidence,'narrative_mode':'source-bound action/result or forward viewer question; applicant-reported prototype and current product lineages remain separate','not_source_pass':True,'written_visual':{'scene':sid,'prompt':row['prompt'],'mode':'anonymous conceptual illustration; prototype bench is separate from marketed2010/2011/current containers, not an exact product cutaway or performed experiment','review_state':'NOT_REVIEWED'}}
  claim_map[line['id']]=record
  added.append(scene)
 scenes[at+1:at+1]=added
claims=[]
lines=[]
chapters=[]
for scene in scenes:
 if scene.get('chapter'):chapters.append({'title':scene['chapter'],'line_ids':[]})
 for line in scene['lines']:
  record=claim_map[line['id']]
  claims.append(record)
  lines.append({'id':line['id'],'text':line['text']})
  chapters[-1]['line_ids'].append(line['id'])

# r7 keeps the original test-results block intact. The opening quantity now
# describes a handling burden, and the small-cruet action is moved, not repeated.
R6_INPUTS={
 'video.json':'7d81e3fd3578d2885df7df2ea3bab930c7b865025e3719ce701bf89fccf6c623',
 'script.md':'2b62a3ebad0abe655617477bb4c60280d44b7012030c1039a722556f761c9fc0',
 'narration-only.json':'3b75bbd4aba27d0ee6ae9d5cef2089d2c08039b379b34719e98d0b34fee4579b',
 'claims.json':'668a17b43e61b58c8cc6ef08836f31fab9766e96bfe40e6e50da1452b62d7e97',
}
for filename,expected in R6_INPUTS.items():assert sha(OUT/'history/r6'/filename)==expected,filename
r7=json.loads((OUT/'r7-edits.json').read_text())
e1quote='依頼のあった1958年当時、しょうゆは多くの家庭で流し台の下に一升瓶に入って置かれていました。'
k4quote='当時のご家庭では、買ってきたしょうゆを小さなしょうゆ差しに移し替えて使っていたのですが、注ぐたびにしょうゆが垂れ、容器やテーブルを汚してしまっていました。'
for sid,quote in [('E1',e1quote),('K4',k4quote)]:
 assert sha(catalog[sid]['raw_path'])==catalog[sid]['sha256']
 assert quote in pathlib.Path(catalog[sid]['raw_path']).read_text()
anchors['A06']={'id':'A06','claim':'Ekuan retrospectively locates the commission in1958 and describes soy sauce stored in large one-sho bottles under sinks in many households. The opening uses a bounded handling scenario, not a named family or particular day.','limits':'2009 first-person retrospective, not a1958 household survey. The1.8L quantity is separately explicit in GK p23/A01. Do not turn the source lumbar-pain wording into a medical injury claim or invent personal family details.','evidence':[{'source':'E1','locator':'paragraph0025; full actual HTML and paragraph cache directly checked by author','short_quote':e1quote,'quote_sha256':hashlib.sha256(e1quote.encode()).hexdigest(),'raw_sha256':catalog['E1']['sha256'],'excerpt_text_path':'/workspace/work/brand-story-20261025/c08-audit/source-cache/E1.paragraphs.txt'}]}
anchors['A07']={'id':'A07','claim':'Company staff retrospectively describe bought sauce transferred into a small cruet, with pouring drips soiling the vessel and table; the later tabletop product was intended to avoid this transfer/use problem.','limits':'2014 unnamed company communications staff retrospective; no actual household, specific day, universal drip rate, or injury cause claimed. Anonymous small ceramic cruet illustration is a bounded composite with GK p23.','evidence':[{'source':'K4','locator':'paragraph0018; actual HTML and paragraph cache directly checked by author','short_quote':k4quote,'quote_sha256':hashlib.sha256(k4quote.encode()).hexdigest(),'raw_sha256':catalog['K4']['sha256'],'excerpt_text_path':'/workspace/work/brand-story-20261025/c08-audit/source-cache/K4.paragraphs.txt'}]}
scenes=[s for s in scenes if not any(l['id'] in r7['delete'] for l in s['lines'])]
claim_map={c['id']:c for c in claims}
moved=next(s for s in scenes if s['lines'][0]['id']=='c8r10204')
scenes.remove(moved)
chapter_name=moved.pop('chapter')
next(s for s in scenes if s['lines'][0]['id']=='c8r10201')['chapter']=chapter_name
at=next(i for i,s in enumerate(scenes) if s['lines'][0]['id']=='c8r10102')
scenes.insert(at+1,moved)
oldr5=json.loads((OUT/'history/r5/video.json').read_text())
restored=next(s for s in oldr5['scenes'] if s['lines'][0]['id']=='c8r10220')
at=next(i for i,s in enumerate(scenes) if s['lines'][0]['id']=='c8r10221')
scenes.insert(at,restored)
claim_map['c8r10220']=next(c for c in json.loads((OUT/'history/r5/claims.json').read_text())['narration_claims'] if c['id']=='c8r10220')
claims=[]
lines=[]
chapters=[]
for scene in scenes:
 if scene.get('chapter'):chapters.append({'title':scene['chapter'],'line_ids':[]})
 for line in scene['lines']:
  lid=line['id'];record=claim_map[lid]
  if lid in r7['texts']:line['text']=r7['texts'][lid]
  if lid in r7['prompts']:
   scene['data']['prompt']=r7['prompts'][lid]
   record['written_visual']['prompt']=r7['prompts'][lid]
   record['written_visual']['mode']='anonymous composite kitchen-handling scene from attributed historical accounts; not a named person, particular day or medical injury reconstruction'
  record['text']=line['text'];record['chapter']=chapters[-1]['title']
  if lid in ['c8r10101','c8r10102','c8r10104']:
   ids={'c8r10101':['A01','A06'],'c8r10102':['A06'],'c8r10104':['A07']}[lid]
   record['anchor_ids']=ids;record['source_ids']=list(dict.fromkeys(e['source'] for a in ids for e in anchors[a]['evidence']))
   record['evidence']=[{'anchor_id':a,'claim_scope':anchors[a]['claim'],'limits':anchors[a]['limits'],'source_locator':e,'original':{k:catalog[e['source']].get(k) for k in ['id','title','url','raw_path','sha256','source_type','publication_date_scope']}} for a in ids for e in anchors[a]['evidence']]
   record['narrative_mode']='one-drop viewer need and large-bottle handling burden, then expressly attributed1958kitchen recollection and bounded anonymous pouring scene; no actual household or new experiment'
  claims.append(record);lines.append({'id':lid,'text':line['text']});chapters[-1]['line_ids'].append(lid)

# r8 removes the capacity side branch, orders the raw-soy case before its modern
# pouch, and answers the visible-inner-bag question at the next chapter opening.
# This is an author edit, never an independent source or narrative verdict.
R7_INPUTS={
 'video.json':'7c65e8cf79a9518741e5431865df469f5d8fefcaba219c4d93395f32d030f82b',
 'script.md':'4825e10b2e9c8faa33be384a6f1592625f2e5d351e5035c4ee6536fdca983712',
 'narration-only.json':'0cc35be215547b8ce77393f89a05dfb528b58c395396dc3f35bff270bb3c81b4',
 'claims.json':'497f251a28ff79c4998c6e0b56f81d3dd166ee008780f7b0723fb373d9f0bd98',
}
for filename,expected in R7_INPUTS.items():assert sha(OUT/'history/r7'/filename)==expected,filename
r8=json.loads((OUT/'r8-edits.json').read_text())
chapter_names={s['lines'][0]['id']:s['chapter'] for s in scenes if s.get('chapter')}
claim_map={c['id']:c for c in claims}
scenes=[s for s in scenes if not any(l['id'] in r8['delete'] for l in s['lines'])]
for scene in scenes:
 for line in scene['lines']:
  if line['id'] in r8['texts']:line['text']=r8['texts'][line['id']]
ordered=[next(s for s in scenes if s['lines'][0]['id']==lid) for lid in r8['chapter4_order']]
at=min(scenes.index(s) for s in ordered)
scenes=[s for s in scenes if s not in ordered]
scenes[at:at]=ordered
for scene in scenes:
 if scene['lines'][0]['id']=='c8r10401':scene.pop('chapter',None)
for first,oldfirst in [(r8['chapter2_first'],'c8r10201'),(r8['chapter4_first'],'c8r10401'),(r8['chapter6_first'],'c8r10601')]:
 next(s for s in scenes if s['lines'][0]['id']==first)['chapter']=chapter_names[oldfirst]
claims=[];lines=[];chapters=[]
for scene in scenes:
 if scene.get('chapter'):chapters.append({'title':scene['chapter'],'line_ids':[]})
 for line in scene['lines']:
  record=claim_map[line['id']]
  record['text']=line['text'];record['chapter']=chapters[-1]['title']
  claims.append(record);lines.append({'id':line['id'],'text':line['text']});chapters[-1]['line_ids'].append(line['id'])

# r9 deletes the unproductive historical aside rather than shifting its date.
# Keep only the new half-used visibility threshold at the chapter6 answer.
R8_INPUTS={
 'video.json':'213288299cdd5d4cef9a08172e1b1aa4c2b4a6a419ed766dc02d45a6b9de2e69',
 'script.md':'8fb8f52ba53704739a632ec74a12aaa6907030cedb2ab90a9ffe2bd08733493d',
 'narration-only.json':'65b2d46e1fd3b058f5759fe35629f08c16e5374c742cd44cbb58023e3d4ac5a5',
 'claims.json':'975993d111637bd4a4b8acf646e1154681a94ba7a575f0e4c8d8302b61ced182',
}
for filename,expected in R8_INPUTS.items():assert sha(OUT/'history/r8'/filename)==expected,filename
r9=json.loads((OUT/'r9-edits.json').read_text())
chapter4=next(s['chapter'] for s in scenes if s['lines'][0]['id']=='c8r6h01')
claim_map={c['id']:c for c in claims}
scenes=[s for s in scenes if not any(l['id'] in r9['delete'] for l in s['lines'])]
next(s for s in scenes if s['lines'][0]['id']==r9['chapter4_first'])['chapter']=chapter4
claims=[];lines=[];chapters=[]
for scene in scenes:
 if scene.get('chapter'):chapters.append({'title':scene['chapter'],'line_ids':[]})
 for line in scene['lines']:
  if line['id'] in r9['texts']:line['text']=r9['texts'][line['id']]
  record=claim_map[line['id']]
  record['text']=line['text'];record['chapter']=chapters[-1]['title']
  claims.append(record);lines.append({'id':line['id'],'text':line['text']});chapters[-1]['line_ids'].append(line['id'])

closing=scenes[-3:]
scenes=scenes[:-3]
outro={'id':'c08r1-outro','template':'outro','data':{'title':'想留下哪一滴？','cta':'你會拆開密封、改放冰箱嗎？'},'lines':[l for s in closing for l in s['lines']]}
scenes.append(outro)
for record in claims[-3:]:
 record['scene']=outro['id']
 record['written_visual']={'scene':outro['id'],'template':'outro','data':outro['data'],'mode':'native closing card; not a purchased illustration','review_state':'NOT_REVIEWED'}

def locate(fragment):
 found=[l['id'] for l in lines if fragment in l['text']]
 assert len(found)==1,(fragment,found)
 return found[0]
LOOP_TEXTS=[
 ('嘴尖那一點褐色','把上下緣的關係反過來','倒完收手時的滴液難題'),
 ('連進入瓶裡的空氣','空氣進入外瓶和內袋之間','進氣究竟被安排到哪裡'),
 ('整座瓶蓋還藏著一個選擇','這個動作也會切斷密封','取最後一點的保存代價'),
 ('它該長成什麼樣子','把頸部做細','瓶子拿起和放回的外形'),
 ('手要抓哪裡','把頸部做細','手與瓶子細頸的配合'),
 ('嘴尖怎麼辦','讓上緣比較突出','瓶身完成後嘴尖的改動'),
 ('醬油該從哪裡再裝進去','整個紅蓋拿下','小注嘴之外的補充入口'),
 ('瓶身透明，裡頭的東西','色澤和香氣一碰到空氣','新醬油的保鮮問題'),
 ('原來的瓶子該怎麼變','先推出裝五百毫升的密封軟袋','密封研究先走出的容器'),
 ('這個軟袋還能讓你放心放手嗎','軟袋剩少時不容易自己站住','剩量變少後袋子的新麻煩'),
 ('能不能讓外形站住','第一款的外形沿著舊紅蓋','從軟袋走向可擠壓的新瓶'),
 ('空氣究竟該進哪裡','空氣進入外瓶和內袋之間','放手後空氣應去的位置'),
 ('該讓出去的是液體','公告稱它採雙逆止閥','瓶蓋區分液體與進氣的安排'),
 ('注嘴裡剩下的那一點','擴大的空間能把嘴端殘液','特定專利方案對殘液的處理'),
 ('只把通往內袋的路關住','擴大的空間能把嘴端殘液','內袋關閉後出口殘液仍須另處理'),
 ('這一點移動，要怎麼管到嘴尖','擴大的空間能把嘴端殘液','液閥回移擴大蓋內空間的作用'),
 ('外蓋已關上時，液閥還需要管嗎','外蓋內側的密封部','含外蓋的專利構造如何限制液閥'),
 ('裡面的內袋，一眼就看得出來嗎','約用到半瓶，兩層之間的差別','現行透明內袋何時較易辨別'),
 ('難道又是外面漏進去了','內袋還封入了氮氣','目前密封瓶內袋可見氣層的官方解釋'),
 ('為什麼又覺得比較難擠','手的力就逐漸隔著層間空氣','內袋變小後的傳力取捨'),
 ('瓶蓋能不能立刻按回去','用完先直立放幾秒','現行瓶關蓋前的動作'),
 ('還有沒有別的拿法','往右轉','末段殘液的取出方法'),
 ('閥擋住了空氣，就一定還倒得出來嗎','醬油不再自然流出','另案原型的密封觀察與出液分歧'),
 ('這扇小門會只往外翻','小蓋可能被衝擊擠進筒內','另案小蓋衝擊陷入的原始問題'),
 ('你想要的兩件事','前兩天的幾個觀察點','原型初期靜置觀察的進氣與出液結果'),
 ('等到五天呢','醬油不再自然流出','原型五天觀察的固化與出液結果'),
 ('外面沒有漏出醬油','文件都沒有觀察到內容物漏到外面','原型外部無漏與內部失效分別觀察'),
 ('再抬高呢','一百六十公分那組','另案表列較高落下測點的失效'),
 ('瓶身卻還凹著','堵住空氣閥','現行系列瓶身不回復的可能條件'),
]
known=[l['id'] for l in lines]
loops=[]
for a,b,what in LOOP_TEXTS:
 setup,payoff=locate(a),locate(b)
 assert known.index(setup)<known.index(payoff),(a,b)
 loops.append({'setup':setup,'payoff':payoff,'what':what})

style='標準國語，咬字清楚，台北人平常說話的語調。說書人，像在跟朋友講一個等不及要分享的故事。有起伏、有戲：揭曉前刻意停一拍，問句上揚，「你以為」放慢放輕，「其實」亮起來。關鍵數字放慢，清單段落加快。語速像平常聊天，一秒四到五個字，句與句之間不拖。絕不平、絕不像在念稿。'
used_now=list(dict.fromkeys(s for record in claims for s in record['source_ids']))
r1_source_order=[s['id'] for s in json.loads((OUT/'history/r1/claims.json').read_text())['source_catalog']]
source_order=r1_source_order+['P505','F10_coldstorage']
assert set(used_now)<=set(source_order), 'only the frozen expansion sources are added'
used=[s for s in source_order if s in used_now]
sources=[{'title':catalog[s].get('title',s),'url':catalog[s]['url'],'checked_on':'2026-10-25'} for s in used]
doc={'schema_version':1,'slug':SLUG,'format':'drama','category':'story','narration_locale':'zh-TW','target_minutes':[12,14],
 'voice':{'provider':'gemini','name':'Sulafat','style':style,'performance':'跟著倒出、放回、用到最後的動作，向一個人講瓶子如何分配液體和空氣。回憶與原廠功能保留歸屬，不把示意變成假實驗。'},
 'subtitles':{'burn_in':True},'look':{'preset':'cute-mystery'},'characters':[],
 'music':{'prompt':'light, curious, a little mysterious, no vocals','gain_db':-20,'duck_db':-10},'loops':loops,'scenes':scenes,
 'youtube':{'category_id':27,'made_for_kids':False,'default_language':'zh-TW','title':TITLE,'description':'從1961可再填的150mL玻璃桌上瓶，走到2011的200mL內袋密封瓶，再看現行450mL PET瓶用到最後的力道、關蓋與拆開密封後的保存取捨。設計者本人回述、公司原公告、博物館標籤、後期專利原件和完整官方FAQ，分清不同年代和瓶型。後期閥門專利不當早年玻璃瓶原設計；匿名插圖是概念示意，非每款量產剖面。\n\n原件來源（查閱2026-10-25）\n'+'\n'.join(s['title']+'\n'+s['url'] for s in sources),'tags':['龜甲萬','Kikkoman','醬油瓶','品牌故事','工業設計','包裝','日用品的意外轉身','密封瓶'],'video_id':None},
 'thumbnail':{'template':'thumb','data':{'layout':'d','headline':'空氣別進錯！','sub':'一滴醬油改了瓶子','brand':'龜甲萬','tag':'品牌故事','shot':'c08r1-01-04'}},'sources':sources,'assets':[]}
doc['youtube']['description']=doc['youtube']['description'].replace('再看現行450mL PET瓶用到最後的力道、關蓋與拆開密封後的保存取捨。','另讀公開文件中500mL軟膜原型的靜置與落下試驗，再看現行450mL PET瓶用到最後的力道、關蓋與拆開密封後的保存取捨。原型試驗與上市瓶型分開，沒有把原型當成量產款履歷。')
names=['Kikkoman','龜甲萬','榮久庵憲司','Kenji Ekuan','GK','GK Design Group','MoMA','紐約現代美術館','恩田友貴','Tomotaka Onda','KFE','PET','PE','FAQ','吉野工業所','Yoshino Kogyosho','INPIT','JPAA']
series={'kind':'story','slug':'brand-stories-everyday-reversals','episode':8,'chapter':1,'title':TITLE,'logline':'跟著一滴醬油的倒出、瓶子的放回與最後取用，追三代容器如何安排液體、空氣和使用者的手。','names':names,'characters':[],'visual_tier':'stills','compilation':False,'target_minutes':13,'image_model':'image-01','look':{'preset':'cute-mystery'}}

def write_json(name,value):
 (OUT/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
write_json('video.json',doc)
write_json('series.json',series)
write_json('narration-only.json',{'slug':SLUG,'scope':'new author narration only; no verdicts or source discussion','chapters':chapters,'lines':lines})
claimdoc={'schema_version':1,'episode':'C08 Kikkoman remake r4','status':'AUTHOR_CANDIDATE_PENDING_INDEPENDENT_SOURCE_WRITTEN_VISUAL_AND_TWO_READERS','protected_research_files_sha256':PROTECTED,'previous_revision_input_sha256':R3_INPUTS,'source_catalog':[catalog[s] for s in used],'omitted_from_narration_research_only':{'C08R35':'Same-PET/disassembly/recycling branch omitted entirely; full evidence remains in the protected original research.','C08R27':'Keep only the dated PE-to-PET product-generation fact; omit label-peeling and end-of-life branch from narration.'},'author_additional_original_anchors':{k:anchors[k] for k in ['A01','A02','A03','A04','P1','P2','P7']},'narration_claims':claims,'source_pass_issued':False,'owner_approval_issued':False,'actual_runtime_measured':False,'paid_calls':0,'backend_writes':0}
claimdoc.update({'episode':'C08 Kikkoman remake r7','previous_revision_input_sha256':R6_INPUTS,'frozen_research_expansion_sha256':EXPANSION_SHA,'prototype_scope':'JP5053463B2 applicant-reported500mLsoft-film prototype; trial event dates not stated, distinct from2010commercial pouch,2011commercial200mL bottle,2015P1axial valve and current450mLPET.','duration_scope':'Official actual narration body is the full unwrapped voiced timeline including coldopen and CTA; only separate5secondintro/21secondoutro excluded. After-opening/strict counters are planning breakdowns, not the runtime gate.'})
claimdoc['author_additional_original_anchors'].update({k:anchors[k] for k in ['A06','A07']})
claimdoc['omitted_from_narration_research_only']['C08X02']='Current grip/child-sightline branch removed inR7; original frozen expansion research preserved.'
claimdoc.update({'episode':'C08 Kikkoman remake r8','previous_revision_input_sha256':R7_INPUTS})
claimdoc['omitted_from_narration_research_only']['C08R07']='1955 one-litre/small-household branch removed inR8; original frozen research remains unchanged.'
claimdoc.update({'episode':'C08 Kikkoman remake r9','previous_revision_input_sha256':R8_INPUTS})
claimdoc['omitted_from_narration_research_only']['C08X01']='1966 raw-soy sale/stop aside removed inR9; original frozen expansion research preserved.'
write_json('claims.json',claimdoc)
brief='''# C08 龜甲萬｜一滴醬油，瓶子替手作了什麼？

## 問題

從倒進盤子到放回餐桌，一個醬油瓶要讓什麼出去、把什麼留住，才能把最後一點也照顧到？

## 一句答案

早期玻璃瓶分開小注嘴和較寬補充口；後來的密封瓶把液體和進氣分路。餘量難以取出時，拆開整蓋會讓密封破掉，保存方式也得跟著換。

## 站主觀點

主角是一次倒出、放回、再取最後一點的使用問題，不把公司年表、海外市場或產品型號念成清單。玻璃150mL、2011密封200mL及現行PET450mL分時分型；機制只在證據範圍內說一次，不造假實驗，不用警語和重述補長。收束在取餘量與保存的真實選擇，回收和標籤研究留在查核資料，不另開一條產品線。

### 選項 A：讓一滴出去，把想留的留住

一行說明：從餐桌滴液走到內袋進氣，再讓最後一點殘液把拆蓋與保存的代價揭出來。

開場鉤子：你只想倒一點醬油，卻還得看著嘴尖；後來瓶子連空氣進哪裡、整蓋何時拆，都替手多設一道選擇。

目標13分鐘；實際旁白正文需720–840秒，自然4–5 units/秒。字量和原生估時不是實聲驗收，不改速度、停頓、慢播或重述來填長。

## 視覺與聲音規格

MiniMax image-01，look只用cute-mystery preset；匿名英文概念插圖無品牌名、人名、logo或可讀字，不重建原瓶精密閥件。三代容器不可混畫成同構。正文實際插畫時間至少70%，最多連續3卡，靜態圖配緩慢運鏡。精確STORY Sulafat自然說書、繁中燒錄與CC。濃縮後5秒正式片頭、21秒正式v4片尾仍待主機素材身分與實際成片驗收。縮圖layout d，品牌名、黃字黑框主標、短白副標。

## 來源與關卡界線

設計者2009回述、公司後代容器史、匿名職員2014訪談和GK2018刊物保留來源層級。近百模型不升格精確101或逐次原型台帳；不報瓶嘴角度、零黏度或永遠零滴。1961原功能專利未取得，2015後期閥門原件及官方產品橋不當1961設計或每個現售SKU的剖面。2011公告是當年功能與預定上市主張；現行FAQ依指定產品範圍。右旋整蓋後密封已破，須冷藏，不作可再填／重封保鮮建議。原版84句與short36句、六份研究文件均保留；新稿須獨立來源、書面配鏡與兩位全新讀者。預設八語於中文稿核對後接續，尚未翻譯／配音／造SRT或套後台選項。
'''
brief=brief.replace('收束在取餘量與保存的真實選擇，回收和標籤研究留在查核資料，不另開一條產品線。','收束在取餘量與保存的真實選擇，回收和標籤研究留在查核資料，不另開一條產品線。另一份公開文件所載500mL軟膜原型只回答「擋住空氣，等過之後是否仍能倒出、跌落後裡外是否仍正常」，明說申請人原型試驗，不冒稱2010上市袋、2011瓶或現行450mL剖面，也不把文獻公開年當試驗發生年。')
brief=brief.replace('實際旁白正文需720–840秒，自然4–5 units/秒。','原生duration的實際旁白body需720–840秒，含coldopen與有聲CTA，僅排另加5秒片頭／21秒片尾；after-opening／strict只作規劃分項。自然4–5 units/秒。')
brief=brief.replace('開場鉤子：你只想倒一點醬油，卻還得看著嘴尖；後來瓶子連空氣進哪裡、整蓋何時拆，都替手多設一道選擇。','開場鉤子：你只想添一滴，卻先搬1.8公升大瓶、分裝小壺；榮久庵回述1958家庭水槽下的大瓶，將負擔落在具體廚房動作，再追瓶嘴與後來進氣／拆蓋的選擇。')
brief=brief.replace('原件及官方產品橋不當1961設計或每個現售SKU的剖面。','原件及官方產品橋不當1961設計或每個現售SKU的剖面。另案JP5053463B2之500mL軟膜原型保留每條件五樣品、目視進氣、不同有無外蓋落下程序；表列140/160cm與靜置五天結果只限該試驗，不作市售產品耐摔／零氧／食品安全保證。現行系列的冷藏可能症狀及擦嘴動作，與拆整蓋後需冷藏分開。')
(OUT/'brief.md').write_text(brief)
md=['# C08 r4｜作者逐句來源與書面配鏡索引','','這是本版作者主張表，尚未獲新的獨立SOURCE／配鏡／敘事審核，不是verify或owner核准。r1／r2／r3歷史來源及共同敘事HOLD保留，不替本版授權。六份原研究和兩舊版不變。回收及剝標籤等未進新旁白的研究，仍在凍結原件內。','','## 使用原件','']
md[0]='# C08 r9｜作者逐句來源與書面配鏡索引'
md[2]=md[2].replace('r1／r2／r3歷史','r1／r2／r3／r4／r5／r6／r7／r8歷史')
for s in used:md.append(f"- {s}: [{catalog[s].get('title',s)}]({catalog[s]['url']})；actual raw SHA `{catalog[s]['sha256']}`；{catalog[s].get('source_type')}")
md+=['','## 逐句索引','','| ID | 旁白 | 來源anchor | 實際原件 |','|---|---|---|---|']
for r in claims:md.append('| '+r['id']+' | '+r['text']+' | '+','.join(r['anchor_ids'])+' | '+','.join(r['source_ids'])+' |')
md+=['','每句精確locator、原摘錄、原件SHA、禁止推論及匿名概念配鏡在claims.json。A01/A02是作者直接目視GK原掃描的補充錨點；P1/P2/P7承接已取得完整原件及官方產品橋，並非作者來源PASS。','']
(OUT/'claims.md').write_text('\n'.join(md))
script=['# '+TITLE,'','作者附來源稿；後台canonical screenplay需由官方writeScreenplay另產生。尚未核准。','']
for chapter,_ in CHAPTERS:
 script+=['## '+chapter,'']
 for r in claims:
  if r['chapter']==chapter:script += ['['+r['id']+'] '+r['text'],'來源：'+(', '.join(r['source_ids']) or '觀眾問題／訂閱邀請')+'；anchors：'+(', '.join(r['anchor_ids']) or '無事實主張'),'']
(OUT/'script.md').write_text('\n'.join(script)+'\n')
notes={'schema_version':1,'revision':'C08 r4','status':'HOLD_PENDING_INDEPENDENT_SOURCE_AND_TWO_NEW_ISOLATED_READERS','author':'/root/c07_author','new_slug':SLUG,'source_category':'story','old_episode_or_series_not_rebound':True,'protected_research_files_sha256':PROTECTED,'previous_revision_input_sha256':R3_INPUTS,'editorial_delta':{'changed_retained_lines':{},'deleted_lines':sorted(R4_DELETE),'first_function_delivery_retained':'c8r10419; pressing action in original written illustration, no duplicate sentence added','deleted_line_is_loop_endpoint':False,'loop_changes':0,'current_K7_role_claim_scope_corrections':R4_ROLE_SCOPES,'mandatory_targets':['no_recap'],'single_reader_no_not_targeted':['one_line'],'current450mL_90day_exception':'Evidence only; narration says guide120days and some products excepted, not the complete exception table. Historical2011 90day company feature claim is a distinct retained statement.','PET_same_material_and_bag_disassembly_narration_occurrences':0,'new_sources_added':False,'new_fact_or_unverified_psychology_added':False},'source_files_sha256':{f:sha(OUT/f) for f in ['video.json','script.md','narration-only.json','claims.json','claims.md','brief.md','series.json']},'counts':{'narration_lines':len(lines),'scenes':len(scenes),'illustration_shots':sum(s['template']=='shot' for s in scenes),'chapters':len(chapters),'loops':len(loops)},'actual_runtime_measured':False,'source_pass_issued':False,'written_visual_pass_issued':False,'narrative_pass_issued':False,'verify_written':False,'owner_approval_issued':False,'eight_language_text_written':False,'paid_calls':0,'backend_writes':0,'mechanical_lint':'PENDING_NATIVE_INITIALIZED_CONTEXT','narrative_scope':'one use problem across explicitly different bottle generations; not one physical bottle surviving unchanged for sixty years','native_target':'13 minutes; future actual narration body720–840 seconds, no padding or slowed speech'}
notes.update({'revision':'C08 r6','previous_revision_input_sha256':R5_INPUTS,'frozen_research_expansion_sha256':EXPANSION_SHA,'editorial_delta':{'changed_retained_lines':r6['texts'],'deleted_lines':sorted(R6_DELETE),'new_lines':[r['id'] for b in r6['blocks'] for r in b['rows']],'mandatory_targets':['scene_first','no_recap','substantive_length_extension'],'single_reader_no_not_targeted':['one_line'],'opening':'One-drop viewer stake;1961/150mL sourced object in line2;physical viewer tilt/upright action in line3;at most2unresolvedpreviews;named60yearpromise and centralquestion retained. No shipment count narrated.','prototype_case':'Distinct applicant-reported500mLsoftfilm prototype case, not commercial product lineage; no unverified test year, oxygen assay, mechanism causality or market outcome.','recap_fix':'1961/150mL appears only at opening; remove advancewholecap summary10617 and repeated10622; one actual removal/remaining-liquid delivery at10621.','normal_seal_and_removed_wholecap_conditions_distinct':True,'new_sources_added':['P505','F10_coldstorage'],'new_unverified_fact_or_psychology_added':False,'new_research_extension_added':True},'native_target':'13minutes target; official actual narration body720–840seconds includes fullcoldopen+voicedCTA, excludes onlyseparate5secondintro/21secondoutro. after-opening/strict counters planning only; no padding or slowed speech.'})
notes.update({'revision':'C08 r7','previous_revision_input_sha256':R6_INPUTS,'editorial_delta':{'changed_retained_lines':r7['texts'],'deleted_lines':r7['delete'],'moved_line':'c8r10204 moved to openingafter10102; text/prompt/camera/emotion unchanged','restored_line':'c8r10220 original1961/150mL fact restored only at historicalreleasepoint','changed_prompts':r7['prompts'],'new_author_anchors':['A06','A07'],'mandatory_targets':['scene_first','no_recap','no_detour'],'single_reader_no_not_targeted':['one_line1966','chapters_link10601'],'prototype_all21_lines_and_complete_scenes_unchanged':True,'removed_loop':'c8r6g01→c8r6g02 only; all other30values retained','new_sources_added':False,'new_unverified_fact_or_psychology_added':False,'no_specific_family_day_or_medical_injury_invented':True,'whole_runtime_not_measured':True}})
notes.update({'revision':'C08 r8','previous_revision_input_sha256':R7_INPUTS,'editorial_delta':{'changed_retained_lines':r8['texts'],'deleted_lines':r8['delete'],'chapter4_order':r8['chapter4_order'],'chapter2_first':r8['chapter2_first'],'chapter4_first':r8['chapter4_first'],'chapter6_first':r8['chapter6_first'],'mandatory_targets':['one_line','chapters_link','no_recap'],'opening_first_four_complete_scenes_unchanged':True,'capacity_branch':'Remove1955one-litre event and its dependent/repeatedcapacitybridges; existingdirect-to-table goal nowopenschapter2. Keep narratorcuriosity in theexistinghandlingquestion.','raw_soy_sequence':'Explicit1966companycase before2010commercialpouch; nextuse/rawsauce explanation follows that pouch;2011announcementresearchduration follows without changingitsdate/scope.','chapter6_answer':'10604 half-usedinnerbag visibility answers10526 immediately;10601 duplicate removed.','all_prompts_camera_emotion_unchanged':True,'all_retained_source_anchor_and_evidence_bindings_unchanged':True,'prototype_all21_lines_source_records_and_complete_scenes_unchanged':True,'removed_loop':'c8r10203→c8r10208 only; all other29values retained','new_sources_added':False,'new_unverified_fact_or_psychology_added':False,'whole_runtime_not_measured':True}})
notes.update({'revision':'C08 r9','previous_revision_input_sha256':R8_INPUTS,'editorial_delta':{'changed_retained_lines':r9['texts'],'deleted_lines':r9['delete'],'mandatory_targets':['one_line','chapters_link','no_recap'],'chapter4_first':r9['chapter4_first'],'retained_relative_order_unchanged':True,'historical_aside_removed':'1966sale/stop h01/h02 removed completely, not moved or redated. Existing10406sealquestion→10408explicit2010pouch now directly follows10321freshnessquestion. Fullpersonalname restored in10402asfirstintroduction.','chapter6_answer':'10604 retains only the approximatelyhalf-usedvisibilitythreshold; repeatedinnerbagshrinking clause removed. Half-bottlethresholdoccurs onlyhere.','opening_first_four_complete_scenes_unchanged':True,'prototype_all21_lines_source_records_and_complete_scenes_unchanged':True,'all_29_loop_objects_unchanged':True,'all_prompts_camera_emotion_unchanged':True,'all_retained_source_anchor_and_evidence_bindings_unchanged':True,'new_sources_added':False,'new_unverified_fact_or_psychology_added':False,'whole_runtime_not_measured':True}})
write_json('author-notes.json',notes)
for filename,expected in PROTECTED.items():assert sha(OUT/filename)==expected
print(json.dumps(notes['counts'],ensure_ascii=False))
