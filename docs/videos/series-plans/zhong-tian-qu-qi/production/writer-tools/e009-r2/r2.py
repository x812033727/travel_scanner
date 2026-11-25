"""Episode 9 remake (r2): the writer spec for ../e001-r2/build-r2.py. Source: docs/videos/zhong-tian-qu-qi-e009-r2/script.md
(c01-c38 = s01-s38), including its sections 「這版改了什麼」 and 「2026-11-06 審稿後的修改」, which override the tables (c19
「明天一定？宿主今晚第二次推託了。」, no longer a long shot; c03 he first picks the bedding up by the woodshed door; c21 one
candle on Qin Shuang's table, bent by the wind, upright again after c22 shuts the window).

Live action from the first draft (owner 2026-11-11: 「之後都用真人版」), written the way e008-r2/r2.py wrote it (route-a.md
2026-11-07 to 11-12, e908-live pick-review.md, cut-review.md, cut-review-2.md, fix1-fix5):
- Tang Xiaotang wears the live portrait's costume (tangxiaotang-portrait-l1: the cross-collared short jacket wrapped shut
  in a low closed V over a pleated skirt), TANG as e005-e008. The script's 「t2 高立領」 is the CG costume and has no live
  picture; no collar sentence is written (pilot.py refuses one).
- Qin Shuang is only in c01, from behind, both her hands on the reins, and no blade, no knife, no scabbard and no weapon of
  any kind anywhere in the frame (the script's 「柴刀插腰帶右邊」 is not shown; extras.json drops the knife from her cast
  sentence). c21's 「空的刀架」 is an empty wooden wall rack with nothing on it.
- A-ling's dagger is the episode's one weapon (c24-c32, c37): always in her LEFT hand in a forward grip, its edge turned in
  toward Xu Yan's neck and its blunt back outward, never changing hands (DAGGER, GRIP); c32 it sinks to her side point down,
  c37 it lies flat across her knees. The pale old scar inside her left wrist is written in every shot that shows that
  wrist (c24-c27, SCAR); c28 she pulls the sleeve over it, and from c29 on the sleeve covers it (written every shot). No shackles. Every
  shot with the dagger says no other blade or weapon anywhere in the frame.
- Every spoken line faces its listener (build-r2.py's gaze clause); every face is written part by part, NOSMILE where the
  script allows no smile (allowed: c03 Xu Yan's dry laugh, c08 his wry smile, c15 and c17 Tang Xiaotang, c35 his rueful
  line of the mouth).
- Tang Xiaotang's speaking close shots with a cool face (c09, c12) are shot from behind her as e908 fix1 shot s07/s11/s20:
  in the composition she is "one young woman" seen only from behind (the two looped buns, two long pink silk ribbons
  hanging from the buns over her shoulders, a pink inner collar, light peach-pink silk), her face and mouth never seen, her
  line `nospeak` (the recording is laid in); `colab/runs/e909-live/spec.json` drops her three face pictures there with
  `drop_pictures` and takes her identity sentence out (with them the model drew a second, front-facing her). c07 (a wide
  shot, her face small) keeps her face. Her silent shots get e907 fix2/fix3's neutral face sentences in spec.json. The
  word "camera" is never written into a composition.
- At most three named people on screen: c01 has Xu Yan, Qin Shuang (from behind) and A-ling; Tang Xiaotang has already
  gone in (the script has four). Point-of-view shots (c05, c21, c26) name nobody, so no picture of the one looking is
  sent, and say nobody is in the frame. Over-the-shoulder shots say the foreground person appears once and nobody else
  stands behind.
- Xu Yan's body is written in every shot: standing at his full height in the corridor and at the doors; in Tang Xiaotang's
  room he stands in c07-c08, sits on a low stool across the table from c09 (his head at the same height as hers) to c17,
  and stands up in c18; in A-ling's room he stands with his back to the door (c24-c30), kneels on the corridor floor in
  c31 and lies on his back (c33) then on his side (c35-c38) on the bedding. Tables, sills and stools are given heights.
- The bedding: one rolled bundle of grey-blue coarse cloth tied with hemp cord (BEDROLL), under his left arm c03-c07, by
  the door c08-c17, under his arm again c18-c24, dropped c25, picked up c29, unrolled outside the door c31. The candlestick
  is Xiaohe's c02-c04, his c04-c08, left on Tang Xiaotang's table from c08 (c18 he leaves it; none in his hands from c19).
  Xiaohe's straw rabbit is tucked into her sash (extras.json changes her cast sentence).
- Night light is named in every shot: the yard's lantern and cool moonlight; the corridor's candlelight from the door
  cracks and a little moonlight from the open end; one candle's warm yellow light in Tang Xiaotang's room; cold moonlight
  and one wind-bent candle in Qin Shuang's room; one dim candle in A-ling's room.
- No writing anywhere: the doors, the lantern, the window paper and the account book covers blank; the open account book's
  pages soft and out of focus. The system panels are overlays (s16, s33, s34). c34's eye extreme close-up is e907's EYES
  (the script's 「瞳孔裡映著淡藍光」 is an ERROR in preflight-prompts.py). Inserts open directly on their subject; no
  "leans" or "bends" (c03, c12, c17, c18, c29 are written as squatting, tipping forward or lifting with the head in the
  frame).
State: Xu Yan dusty from a day's riding, tired, the rims of his eyes a little red, every shot (XU). Tang Xiaotang's buns
re-done (not askew any more, the script). Opens on e008 c40's night: the three ride up to the Xu yard gate where A-ling
was waiting; the hidden task (e008 c36-c38) is not repeated.
Places: the yard at night "yard gate" (gen-dh -> set-xujia-yuan, live l2). The four rooms of the script have no picture
in any version yet (the owner is choosing live night screen tests from live-action/screen-test-e009.py); they are written
with their own names, which gen-dh.mjs's SET table now maps: the corridor "inside corridor of the Xu farmhouse" (->
set-xujia-zoulang), Tang Xiaotang's room "first bedroom of the Xu farmhouse" (-> set-xujia-tangfang), Qin Shuang's room
"second bedroom of the Xu farmhouse" (-> set-xujia-qinfang) and A-ling's room "third bedroom of the Xu farmhouse" (->
set-xujia-lingfang); the live pictures will be refs-live/<name>-l1.png. No names of people in those place phrases (gen-dh
would send that person's portrait). pilot.py stops on every shot in those four places until the pictures exist (listed in
FOOT); ref2manifest needs refs-dh/<name>-t1.png as well, which the CG version will never have (see FOOT).
"""
EP = 909  # internal working number; the published slug is zhong-tian-qu-qi-e009-r2
SLUG = "zhong-tian-qu-qi-e009-r2"
EP_TITLE = "洞房夜三扇門（重製版 r2）"
OUTLINE_SECONDS = 198  # script.md: 197.5 s, 38 shots (101 + 96.5)
TARGET_MINUTES = [3, 5]
TITLE = "洞房夜三扇門｜種田娶妻打天下 第9集（重製版）"
DESCRIPTION = "第四天夜裡，許硯三人騎著鏢局的馬回到家。小禾端著燭台擋在走廊：昨天成親他躲去睡柴房，今晚不准再躲，三扇門自己選一扇。第一扇是唐小棠，要他先把今天的三本帳對完；許硯不碰算盤就心算出二十兩一錢，還抓出一筆三錢記成三兩，唐小棠好感加二，接著又搬出十本帳。第二扇門裡沒有人，窗戶開著，他替秦霜把窗關上。第三扇門一推開，阿令的匕首就抵上他的脖子；他看到她手腕上的舊傷，問了一句就不再問：「妳睡床，我睡門口，誰要進來，先過我。」阿令丟出一條厚被子，好感加十，隱藏任務完成。夜裡，她隔著門板說：明天，我可能得走。《種田娶妻打天下》第 9 集（重製版）。"
THUMB = ("洞房夜，刀抵喉", "s24")
CHARACTERS = ["xuyan", "xiaohe", "tangxiaotang", "qinshuang", "aling", "xitong"]
MINOR = {}
MUSIC = "one cue per scene: a light playful comedy of pipa, woodblock and dizi through the night corridor and the warm candlelit room where the accounts are checked, dropping out for one beat on the system chime and pausing for a breath under the system's last jab; a low suspense cue of low cello and soft guqin in the dark corridor, the empty moonlit room and the dark candlelit room, one sharp hit as the blade touches his neck; from the lowered blade a very soft warm string cue, only the strings left under the last whispered line; ancient Chinese rural drama, no vocals"

# Scene headers of script.md. Scene 1: the Xu yard at night (the yard gate on screen right, the house door at the back
# left, the horse shed in the back left corner, the lantern by the gate), then the inside corridor (the three doors in a
# row on screen right, the open end toward the yard on screen left, the woodshed door at the near end), then the first
# bedroom (the door on screen left, the table with Tang Xiaotang on screen right, the bed behind the table). Scene 2: the
# second bedroom (the open window on screen right), the corridor again, the third bedroom (the door on screen left, the
# bed on screen right), and the corridor floor outside its door. Close shots use the short `_c` headers.
LOC = {
    "yard": "At the yard gate in the bamboo fence of the Xu farmhouse at night: the yard gate on screen right with one blank paper lantern with no writing hanging beside it, the house door at the back left with warm candlelight in its doorway, one thatched horse shed in the back left corner, a packed-earth yard, cool blue moonlight over everything",
    "hall": "In the inside corridor of the Xu farmhouse at night: packed-earth walls and rough timber posts, three plain wooden doors in a row along the right-hand wall with no writing on them, warm candlelight glowing through the cracks around each door, the open end of the corridor on screen left letting in a little cool moonlight, one low woodshed doorway at the near left end; dark, lit only by the glow from the door cracks and the moonlight",
    "hall_c": "In the inside corridor of the Xu farmhouse at night, lit only by warm candlelight through the door cracks and a little cool moonlight",
    "tang": "In the first bedroom of the Xu farmhouse at night, a young woman's small neat room: one small plain wooden table on screen right, as high as a seated person's waist, with one lit candle on it, a low wooden stool on each side of it, a simple wooden bed with a pale pink quilt behind the table, one paper window covered with blank paper, the wooden door on screen left, packed-earth walls; warm yellow light from the one candle only",
    "tang_c": "In the first bedroom of the Xu farmhouse at night, warm yellow light from one candle on the table",
    "qin": "In the second bedroom of the Xu farmhouse at night, its owner gone: one empty wooden bed with the quilt folded square and neat, the paper window on screen right flung wide open to the night, its paper blank, one empty wooden wall rack beside the window with nothing on it, one small table under the window with one lit candle whose flame is bent low by the night wind; cold moonlight through the open window and a little flickering candlelight",
    "ling": "In the third bedroom of the Xu farmhouse at night, very small and very dark: the wooden door on screen left, one narrow wooden bed on screen right, one small low side table beside the bed with one lit candle, packed-earth walls; the one candle is the only light, warm and dim, deep shadows in the corners",
    "ling_c": "In the third bedroom of the Xu farmhouse at night, dark, lit only by one dim warm candle by the bed",
}
LIGHT = {
    "yard": "the cool moonlight and the lantern glow stay unchanged",
    "hall": "the warm glow from the door cracks and the faint cool moonlight stay unchanged",
    "tang": "the warm yellow light of the one candle stays unchanged",
    "qin": "the cold moonlight from the window stays unchanged",
    "ling": "the dim warm light of the one candle stays unchanged",
}

# Repeated wording (each prop is one object; the descriptions say "one" where it first appears).
XU = "his faded blue-grey scholar's robe with one small sewn cloth patch at one elbow and both shoulders whole, dusty from a long day's ride, tired, the rims of his eyes a little red"
HE = "little Xiaohe in her patched lilac short jacket with red-string pigtails and one front tooth missing, a small woven straw rabbit tucked into her sash"
TANG = "in her peach-pink cross-collared short jacket wrapped shut over a pleated skirt with a ribbon bow"
CHEST = "framed from the chest up with space above her head"
# e908 fix1: her back with no name and no face pictures (spec.json drops them); the ribbons, the pink inner collar and
# the light peach-pink written in (route-a.md 2026-11-12: without the pictures they came out short, white and orange).
BACK = ("one young woman appears only once: in the {side} foreground only the back of her head with two looped buns tied "
        "with pink silk ribbons and pearl pins, two long pink silk ribbons hanging from the buns down over her shoulders, a "
        "pink inner collar at the nape of her neck and her light peach-pink silk shoulders; she is the only woman in the whole "
        "shot; she keeps facing across the table toward the man the whole time, the back of her head toward us, her ear the "
        "furthest round her head we ever see, no cheek, no profile and no lips at any moment")
QIN = "her dark brown cross-collared short jacket, wide leather belt, black trousers, leather boots and high ponytail"
ALING = "A-ling in her plain grey-white cotton dress with long sleeves and one plain wooden hairpin, no shackles"
SCAR = "one pale old scar across the inside of her left wrist"
DAGGER = "one dagger with a single-edged iron blade about a palm long and a wooden grip wrapped in black cloth"
GRIP = "held in her left hand only, in a forward grip, its sharp edge turned in toward his neck and its blunt back facing outward"
NOWEAPON = "no other blade and no other weapon anywhere in the frame"
BEDROLL = "one rolled bedding bundle of grey-blue coarse cloth tied round with hemp cord"
CANDLE = "one small brass candlestick with one lit white candle"
BOOKS3 = "three thin account books with plain blue cloth covers, shut, the covers blank with no writing"
BOOKS10 = "a stack of ten thin account books with plain blue cloth covers, blank with no writing"
WOODABACUS = "one plain wooden abacus as long as her forearm, no marks or writing"
OPENBOOK = "one open account book, its pages soft and out of focus so no line can be read"
QUILT = "one thick quilt of dark indigo coarse cloth"
EYES = "extreme close-up filling the whole frame edge to edge with only Xu Yan's two eyes and brows, no nose and no mouth in the frame, the shot opens directly on his eyes from its very first frame, natural dark brown irises with a tiny catchlight, his gaze slightly off to screen left and never into the lens"
NOSMILE = "no smile at any moment, not even at the end of the shot, until the last frame"
ONCE = "each person appears only once, nobody else behind them"


def back(side="right"):
    return BACK.format(side=side)


SHOTS = [
    # ---- scene 1: the Xu yard at night, early in the hour of xu; then the corridor (three doors on screen right, Xu Yan
    # comes in from the left) and the first bedroom (the door on the left, Tang Xiaotang behind the table on the right).
    dict(chapter="回家", loc="yard", cam="Wide shot, tracking", chars=["xuyan", "qinshuang", "aling"], night="yard", act=4,
         comp=f"wide shot past the bamboo fence and the blank paper lantern in the foreground, everyone small in the frame: on screen right Xu Yan, {XU}, standing at his full height just inside the yard gate, his face three-quarter to screen left toward the house, never the lens; worn out: brows drawn together, eyes heavy, lips closed; in the middle, seen only from behind, Qin Shuang, {QIN}, both her hands on the reins of one chestnut-red horse with a saddle, leading it toward the horse shed at the back left, her face never seen, no blade, no knife, no scabbard and no weapon of any kind anywhere in the frame; small in the lit house doorway at the back left {ALING}, her sleeves pulled down over her wrists, standing; {ONCE}",
         lines=[],
         motion=f"Qin Shuang, both hands on the reins, leads the horse away toward the horse shed at the back left; Xu Yan rubs his stiff shoulder and walks a few steps toward the house; in the doorway A-ling looks at him for one beat, then turns and goes inside; nobody speaks; all lips stay closed; {NOSMILE}",
         zh="全景、跟拍、前景竹籬笆與空白燈籠：夜，許硯（衣服沾塵、累、眼睛有點紅）站在院門內；秦霜的背影兩手抓韁繩，牽棗紅馬往左後的馬棚走（稿子是許硯遞韁繩，改成已遞出、她牽走）；屋門口的阿令（沒戴鐵鐐、袖子蓋住手腕）看他一眼，轉身進屋；沒有人說話。live：一鏡最多三人，唐小棠已先進屋、不入鏡（稿子四人）；秦霜手上只有韁繩，畫面裡沒有刀"),
    dict(chapter="走廊", loc="hall_c", cam="Medium shot, slow push in", chars=["xiaohe"], night="hall",
         comp=f"medium shot past one rough timber post of the corridor in the left foreground: {HE}, framed from the knees up with space above her head, {CANDLE} raised in her right hand, her face three-quarter to screen left toward Xu Yan off screen left, never the lens; very earnest: brows drawn together, eyes wide and firm, lips firm between words; behind her only the packed-earth wall and one candlelit door crack of the same corridor",
         lines=[("xiaohe", "哥，昨天成親你躲去睡柴房，今晚不准再躲。", "很認真")],
         motion=f"Xiaohe runs in from screen right with the candlestick held high, stops in the middle of the corridor and throws her left arm out wide to block the way, the candle flame swaying; {NOSMILE}",
         zh="中景、慢推、前景走廊柱子：小禾（補丁淡紫短襖、紅繩小辮、缺門牙、草編兔子塞在腰帶上）右手舉一個銅燭台（一根白蠟燭），從畫右跑出來停在走廊正中間，左手張開擋住；很認真、不笑；朝畫左外的許硯說"),
    dict(loc="hall", cam="Over-the-shoulder medium shot, slow push in", chars=["xiaohe", "xuyan"], night="hall",
         comp=f"over-the-shoulder medium shot from behind Xiaohe: Xiaohe appears only once, only the top of her small head with its two red-string pigtails at the bottom right foreground, her face out of the frame; Xu Yan on screen left at the near end of the corridor beside the low woodshed doorway, standing at his full height, framed from the knees up with clear space above his head, {XU}, his face three-quarter to screen right toward her, never the lens; caught out: brows lifted, eyes shifting, a weak dry laugh between words; nobody else behind him",
         lines=[("xuyan", "我沒躲，柴房涼快。再說債剛還完，我累了。", "推託，乾笑")],
         motion=f"Xu Yan squats down beside the woodshed doorway, takes up {BEDROLL} under his left arm and rises again to his full height, his whole head staying in the frame, then takes half a step back toward screen left and hugs the bundle to his chest; Xiaohe's lips stay closed",
         zh="過肩（小禾肩後拍許硯）、慢推：前景右下只有小禾的頭頂與紅繩小辮；許硯在走廊口柴房門邊蹲下抱起一捲鋪蓋（灰藍粗布、麻繩綁著）夾在左臂、站直，往畫左退半步、把鋪蓋往懷裡一抱，乾笑推託（本鏡可以乾笑）。live：稿子「彎腰」寫成蹲下再站起、頭留在畫面裡；站著、膝以上"),
    dict(loc="hall_c", cam="Close-up, slow push in", chars=["xiaohe"], night="hall",
         comp=f"close-up of {HE}, framed from the chest up with space above her head, her face three-quarter to screen left and tilted up toward Xu Yan off screen left, never the lens; glaring: brows drawn down hard, eyes wide, lips firm between words; the brass candlestick in her right hand; behind her only the packed-earth wall of the same corridor",
         lines=[("xiaohe", "三扇門都留著燈，你自己選一扇進去。", "瞪眼")],
         motion=f"Xiaohe steps forward and thrusts the brass candlestick out of the frame at the bottom left into a man's hand there, then rises onto her toes, her whole head staying in the frame, glaring up; {NOSMILE}",
         zh="近景、慢推：小禾上前一步，把燭台硬塞進許硯的右手（燭台出畫面左下），踮腳瞪他；不笑；身後只有走廊的土牆"),
    dict(loc="hall", cam="Point-of-view shot, slow push in", chars=[], night="hall",
         comp="point-of-view shot looking along the corridor at the three plain wooden doors in a row on screen right, no writing on them, warm candlelight glowing through the cracks around each one; the small flame of one candle on a brass candlestick rising from the bottom edge of the frame, the hand that holds it below the frame; nobody in the corridor, no person and no face anywhere in the frame",
         lines=[("xuyan", "一扇算帳，一扇沒聲，一扇在磨刀。", "低聲")],
         motion="the candle flame at the bottom edge sways; the light in the crack of the first door flickers, the crack of the second door stays still, and a shadow passes once behind the crack of the third door; nobody appears",
         zh="主觀（許硯看走廊）、慢推：三扇木門（沒有字）、門縫透燭光；畫面下緣是他手上燭台的火（手在畫面外）；第一扇門縫的光晃、第二扇不動、第三扇門縫後一個影子晃過；許硯畫外低聲（算珠聲、磨刀聲是音效）。live：主觀鏡不送許硯的參考圖、寫明畫面裡沒有人"),
    dict(loc="hall", cam="Medium two-shot, tracking", chars=["xuyan", "xiaohe"], night="hall",
         comp=f"medium two-shot along the corridor, framed with clear space above Xu Yan's head: in front Xu Yan, {XU}, the bedding bundle under his left arm and {CANDLE} in his right hand, moving toward screen right, his face in profile toward the doors ahead, never the lens; helpless: brows lifted, eyes wide, lips closed; right behind him {HE}, both small hands pressed flat on the small of his back, her face lifted toward the back of his head; the first door ahead on screen right with candlelight glowing round its edges; {ONCE}",
         lines=[("xiaohe", "小棠嫂嫂那扇最亮，先去那裡準沒錯。", "推人")],
         motion=f"Xiaohe pushes Xu Yan along the corridor toward the first door on screen right; he stumbles two steps forward, the candle flame swaying; Xu Yan's lips stay closed; {NOSMILE}",
         zh="雙人鏡、跟拍：小禾從背後兩手推許硯的腰往畫右第一扇門走（門縫最亮），許硯（左臂夾鋪蓋、右手燭台）踉蹌兩步；小禾說話、許硯嘴閉著"),
    dict(chapter="唐小棠房", loc="tang", cam="Wide shot, tracking", chars=["tangxiaotang", "xuyan"], night="tang",
         comp=f"wide shot past the wooden door frame in the left foreground, both small in the frame, framed with clear space above their heads: on screen right Tang Xiaotang {TANG}, seated on a low stool behind the small table, her left hand resting flat on {BOOKS3}, {WOODABACUS} and the lit candle beside them, her face three-quarter to screen left toward Xu Yan, never the lens; businesslike and cool: brows level, eyes steady on him, lips firm between words; on screen left Xu Yan, {XU}, the bedding bundle under his left arm and the brass candlestick in his right hand, stepping in through the doorway at his full height; nobody in the doorway behind him; {ONCE}",
         lines=[("tangxiaotang", "來得正好，先把今天這三本帳對完再說。", "理所當然，不笑")],
         motion=f"Xu Yan shoulders the door open and steps into the room; Tang Xiaotang looks up from the books and presses her left hand flat on the three of them; Xu Yan's lips stay closed; {NOSMILE}",
         zh="全景、跟拍進門、前景門框：唐小棠坐在桌後（畫右）矮凳上，左手按在三本帳冊上（藍布封面、闔著、空白），桌上一把木算盤、一根蠟燭；許硯用肩頂開門進來（左臂鋪蓋、右手燭台），站著；唐小棠抬頭說話，不笑；門外的小禾不入鏡（回自己房）。live：全景臉小，照稿子正拍（不改背後）；冷臉講話若出笑，挑片時看"),
    dict(loc="tang", cam="Over-the-shoulder medium shot, slow push in", chars=["xuyan", "tangxiaotang"], night="tang",
         comp=f"over-the-shoulder medium shot from behind Tang Xiaotang's left shoulder: Tang Xiaotang appears only once, seated, her shoulder and the back of her head with its two looped buns and pink silk ribbons in the right foreground, her face out of the frame; Xu Yan standing at his full height on the near side of the small table on screen left, the tabletop as high as the middle of his thigh, framed from the waist up with clear space above his head, {XU}, his face three-quarter to screen right toward her, never the lens; dumbfounded: brows shot up, eyes wide, mouth twisting into a wry helpless half smile between words; on the table the three blue-covered account books, shut and blank, and the lit candle; nobody else behind him",
         lines=[("xuyan", "別人洞房喝交杯酒，我洞房對帳本？", "傻眼，苦笑")],
         motion="Xu Yan sets the brass candlestick down on the table and lets the bedding bundle drop by the door at his feet, his whole head staying in the frame, then looks from the books to her and back; Tang Xiaotang's lips stay closed",
         zh="過肩（唐小棠左肩後拍許硯）、慢推：前景右唐小棠的肩與丸子頭（坐著，只出現一次）；許硯站在桌前（桌面到大腿中段）把燭台放上桌、鋪蓋丟在門邊腳下，看看帳冊又看看她，苦笑說話（本鏡可以苦笑）；她嘴閉著。live：站著、腰以上、頭上留空"),
    # Converted: Tang Xiaotang's speaking close-up (script c09, 理所當然、不笑) from behind her; the line is laid in.
    dict(loc="tang", cam="Over-the-shoulder medium shot, slow push in", chars=["xuyan", "tangxiaotang"], nospeak=["tangxiaotang"], night="tang",
         comp=f"over-the-shoulder medium shot from close behind one young woman's left shoulder: {back('right')}; across the small table on screen left Xu Yan, {XU}, sitting down on the low stool on his side of the table, framed from the chest up with space above his head, his head at the same height as hers, his face three-quarter to screen right toward her, never the lens; deflated: brows drawn up, eyes on her, lips closed; on the table {WOODABACUS}, the three blue-covered account books, blank, and the lit candle; exactly two people in the frame, nobody else",
         lines=[("tangxiaotang", "交杯酒一壺二十文，帳錯一筆可是幾兩。", "理所當然，不笑")],
         motion=f"her right hand pushes the wooden abacus across the table toward him and her chin lifts once, the back of her head still toward us; Xu Yan sinks onto the stool, his head level with hers, and stares at the abacus; Xu Yan's lips stay closed; {NOSMILE}",
         zh="【改背後拍】過肩、慢推：從唐小棠左肩後拍，她只出現一次（前景右只有後腦、雙丸子頭、兩條長粉緞帶垂過肩、粉色內領、淡桃粉衣肩），臉與嘴不入鏡；她右手把木算盤推過桌面給許硯、下巴一抬；許硯在畫左坐上矮凳（頭跟她同高）、盯著算盤、嘴閉著。台詞 nospeak，剪接放錄音；spec.json 拿掉她三張臉部參考圖。稿子是下巴以上近景、她不笑講話"),
    dict(loc="tang_c", cam="Insert close-up, high angle, slow push in", chars=[], night="tang",
         comp=f"high-angle insert close-up, the shot opens directly on {OPENBOOK} on the table from its very first frame: one man's hand in a dusty blue-grey cuff, its forefinger running down the page; {WOODABACUS} beside the book, untouched; only the hand, cuff, book and abacus are in the frame, no face; the lit candle at the top edge",
         lines=[("xuyan", "後巷十二兩，客棧六兩，鏢局二兩一錢。", "邊翻邊念")],
         motion="the hand turns one page, then the forefinger runs down the blurred lines one by one; the hand never touches the abacus",
         zh="手部特寫、俯拍、慢推（第一格就是攤開的帳冊）：許硯的手（沾塵的藍灰袖口）翻一頁、食指一行一行往下劃，帳頁虛焦、看不到字；手不碰旁邊的木算盤；許硯畫外念"),
    dict(loc="tang_c", cam="Close-up, slow push in", chars=["xuyan"], night="tang",
         comp=f"close-up of Xu Yan sitting on the low stool at the small table, framed from the chest up with space above his head, {XU}, his face three-quarter to screen right toward Tang Xiaotang off screen right, never the lens; calm and sure: brows level, eyes steady, lips firm between words; behind him only the wooden door and the packed-earth wall of the same room in warm candlelight",
         lines=[("xuyan", "今天總共二十兩一錢，還完債剩下一錢。", "平穩")],
         motion=f"Xu Yan shuts the account book with one hand below the frame and lifts his eyes to her off screen right; {NOSMILE}",
         zh="近景、慢推：許硯坐在桌前矮凳上，闔上帳冊（手在畫面外），抬頭看畫右外的唐小棠說話；身後只有門與土牆"),
    # Converted: Tang Xiaotang's speaking close-up (script c12, 愣住、不笑) from behind her; the line is laid in.
    dict(loc="tang", cam="Over-the-shoulder medium shot, slow push in", chars=["xuyan", "tangxiaotang"], nospeak=["tangxiaotang"], night="tang",
         comp=f"over-the-shoulder medium shot from close behind one young woman's left shoulder: {back('right')}; her right hand resting on {WOODABACUS} on the table; across the small table on screen left Xu Yan, {XU}, sitting on the low stool, framed from the chest up with space above his head, his head at the same height as hers, his face three-quarter to screen right toward her, never the lens; unbothered: brows level, eyes calm on her, lips closed; the lit candle on the table; exactly two people in the frame, nobody else",
         lines=[("tangxiaotang", "你連算盤都沒碰，怎麼算得這麼快？", "愣住，不笑")],
         motion=f"her fingers stop dead on the abacus beads; the back of her head jerks up and her shoulders tip a little forward toward him over the table, the back of her head still toward us; Xu Yan looks back at her; Xu Yan's lips stay closed; {NOSMILE}",
         zh="【改背後拍】過肩、慢推：從唐小棠左肩後拍，她只出現一次（只有後腦、丸子頭、長緞帶與肩），臉與嘴不入鏡；她撥算珠的手停住、頭一抬、肩往前一傾（不寫 leans）；許硯坐在對面看她、嘴閉著。台詞 nospeak，剪接放錄音；spec.json 拿掉她三張臉部參考圖。稿子是下巴以上近景、她愣住講話"),
    dict(loc="tang", cam="Over-the-shoulder medium shot, slow push in", chars=["xuyan", "tangxiaotang"], night="tang",
         comp=f"over-the-shoulder medium shot from behind Tang Xiaotang's left shoulder: Tang Xiaotang appears only once, seated, her shoulder and the back of her head with its two looped buns and pink silk ribbons in the right foreground, her face out of the frame; Xu Yan sitting on the low stool across the small table on screen left, framed from the chest up with space above his head, his head at the same height as hers, {XU}, his face three-quarter to screen right toward her, never the lens; offhand: brows level, eyes steady, lips moving lightly between words, no smile; on the table {OPENBOOK} and the lit candle; nobody else behind him",
         lines=[("xuyan", "心算。還有，第三頁這筆，三錢記成了三兩。", "輕描淡寫")],
         motion=f"Xu Yan turns the account book to the third page, spins it round and slides it across the table to her, then taps one blurred line with his forefinger; Tang Xiaotang's lips stay closed; {NOSMILE}",
         zh="過肩（唐小棠左肩後拍許硯）、慢推：前景右唐小棠的肩與丸子頭（只出現一次）；許硯坐在對面把帳冊翻到第三頁、轉過來推到她面前，食指點一行（帳頁虛焦）；輕描淡寫說話，不笑；她嘴閉著"),
    dict(loc="tang_c", cam="Insert close-up, high angle, slow push in", chars=[], night="tang", act=3,
         comp=f"high-angle insert close-up, the shot opens directly on {WOODABACUS} from its very first frame: two slender hands in peach-pink silk cuffs on its beads; only the hands, cuffs and abacus are in the frame, no face; the dark wood of the table in warm candlelight",
         lines=[],
         motion="the slender fingers flick a whole row of beads across with quick clicks, stop, and the forefinger presses down hard on one bead",
         zh="插鏡、俯拍、慢推（第一格就是木算盤）：唐小棠的手（桃粉袖口）啪啪撥過一排珠子、停住，食指壓在一顆珠上（無台詞）"),
    # Tang Xiaotang may smile here (the script); written as face movements.
    dict(loc="tang_c", cam="Close-up, slow push in", chars=["tangxiaotang"], night="tang",
         comp=f"close-up of Tang Xiaotang {CHEST}, {TANG}, seated at the small table, her face three-quarter to screen left toward Xu Yan off screen left, never the lens; softening: eyes lifting slowly to him, brows easing, voice soft, the corners of her mouth slowly curving up into a small smile; behind her only the bed curtain of the same room in warm candlelight",
         lines=[("tangxiaotang", "真的錯了……我對了三遍都沒看出來。", "聲音軟下來")],
         motion="Tang Xiaotang slowly lifts her eyes from the abacus below the frame to him off screen left, and only then do the corners of her mouth curve up",
         zh="近景、慢推（稿子下巴以上，真人版胸口以上）：唐小棠慢慢抬頭看畫左外的許硯，嘴角這時才彎起來（本鏡可以笑），聲音軟下來"),
    dict(loc="tang_c", cam="Close-up, slow push in", chars=["xuyan"], night="tang",
         comp=f"close-up of Xu Yan sitting at the small table, framed from the chest up with space above his head, {XU}, his face three-quarter to screen right toward Tang Xiaotang off screen right, never the lens; awkward under her gaze: brows twitching, eyes sliding away to one side, lips pressed shut; behind him only the wooden door and the packed-earth wall in warm candlelight",
         lines=[("xitong", "叮。唐小棠，好感加二。", "冷淡，報數")],
         panel=[("唐小棠 好感 +2 → 15", "panel")],
         motion=f"Xu Yan rubs the side of his nose once with his right forefinger and his eyes slide off to screen left; his lips stay closed; {NOSMILE}",
         zh="近景、慢推：許硯被她看得不自在，伸手摸一下鼻子、眼睛往旁邊瞟；嘴閉著、不笑；系統（面板）"),
    # Tang Xiaotang may smile here (the script: 興奮).
    dict(loc="tang", cam="Medium two-shot, slow push in", chars=["tangxiaotang", "xuyan"], night="tang",
         comp=f"medium two-shot across the small table, both seated on low stools with their heads at the same height, framed from the waist up with clear space above both heads: on screen right Tang Xiaotang {TANG}, her face three-quarter to screen left toward Xu Yan, never the lens; excited: brows lifted, eyes bright, a wide eager smile between words; on screen left Xu Yan, {XU}, his face three-quarter to screen right toward her, never the lens; dismayed: brows shooting up, eyes wide, lips closed; on the table {OPENBOOK}, the wooden abacus and the lit candle; {ONCE}",
         lines=[("tangxiaotang", "相公這麼會算，那這十本也天亮前對完。", "興奮")],
         motion=f"Tang Xiaotang lifts {BOOKS10} up from the floor beside her stool with both arms and thumps it down in front of him, her whole head staying in the frame; Xu Yan's upper body jerks back on his stool; Xu Yan's lips stay closed",
         zh="雙人鏡、慢推：兩人隔桌坐在矮凳上、頭同高；唐小棠從凳邊地上抱起一疊十本帳冊（藍布封面、空白），砰地堆到許硯面前（本鏡可以笑），許硯身子往後一仰、嘴閉著。live：稿子「彎腰」寫成雙手抱起、頭留在畫面裡"),
    dict(loc="tang", cam="Medium shot, tracking", chars=["xuyan"], night="tang",
         comp=f"medium shot of Xu Yan, framed from the knees up with clear space above his head the whole time, {XU}, rising from the low stool to stand at his full height, his head well below the top edge of the frame, his face three-quarter to screen right toward Tang Xiaotang off screen right, never the lens; sheepish: brows lifted, eyes darting, an awkward polite half smile between words; at the right edge of the frame one peach-pink silk sleeve and the stack of blue-covered account books, blank, on the table; the brass candlestick with its lit candle left on the table; behind him the wooden door",
         lines=[("xuyan", "我先去看看別人，帳本明天一定陪妳對。", "推託"),
                ("tangxiaotang", "明天就明天。相公記得，你欠我十本。", "畫外，不急不慢")],
         motion="Xu Yan stands up, leaves the candlestick on the table, picks up the bedding bundle from the floor by the door, his whole head staying in the frame, backs into the doorway and rests one hand on the door; while the woman's voice answers from off screen his lips stay closed and he nods once",
         zh="中景、跟拍（長鏡，買 10 秒）：許硯從矮凳站起（膝以上、頭上留空），燭台留在桌上，抱起門邊的鋪蓋（頭留在畫面裡），退到門口一手扶門；先許硯說話；唐小棠畫外說話時許硯嘴閉著、點一下頭；畫右緣只有她的桃粉袖子與那疊帳冊"),
    dict(loc="hall_c", cam="Medium close-up, slow push in", chars=["xuyan"], night="hall",
         comp=f"medium close-up in the corridor, framed from the chest up with space above his head, Xu Yan, {XU}, standing at his full height, {BEDROLL} under his left arm, nothing in his hands, his back pressed against the shut wooden door, his face turned a little to screen right down the corridor, never the lens; worn out: brows drawn together, eyes half closed, lips closed; only the thin candlelight from the door crack beside him and a little cool moonlight; nobody else in the corridor",
         lines=[("xitong", "明天一定？宿主今晚第二次推託了。", "冷，嫌棄")],
         motion=f"Xu Yan lets out one long breath against the door; then he rolls his eyes, rubs between his brows with two fingers, pushes off the door and walks off toward screen right; his lips stay closed the whole shot; {NOSMILE}",
         zh="走廊中近景、慢推：許硯帶上門、背靠門板吐一口氣（左臂夾鋪蓋、手上沒有燭台）；系統說完，他翻個白眼、抬手揉一下眉心，離開門板往畫右的第二扇門走；嘴閉著"),
    # ---- scene 2: deep in the hour of hai. The corridor (doors on screen right), the second bedroom (the open window on
    # screen right), the third bedroom (the door on screen left, the bed on screen right) and the corridor floor outside it.
    dict(chapter="秦霜房", loc="hall_c", cam="Medium shot, slow push in", chars=["xuyan"], night="hall",
         comp=f"medium shot in the corridor, framed from the waist up with clear space above his head, Xu Yan, {XU}, the bedding bundle under his left arm, nothing in his hands, standing at his full height before the second plain wooden door on screen right, no writing on it, only a faint flicker of candlelight in its crack, his face in profile toward the door, never the lens; careful: brows lifted, eyes on the door, lips moving softly between words, no smile; cool moonlight from the open end of the corridor on screen left; nobody else",
         lines=[("xuyan", "秦霜，睡了嗎？我進來了，有事妳就喊。", "小聲")],
         motion="Xu Yan knocks twice on the door with the knuckles of his right hand, waits a beat, then pushes it open a crack and brings his face to the gap, his whole head staying in the frame",
         zh="中景、慢推：許硯（左臂夾鋪蓋、手上沒有燭台）在第二扇門前，右手指節敲兩下、等一下、推開一條門縫探頭；小聲說話；門縫只有一點晃動的燭光，走廊月光"),
    dict(loc="qin", cam="Point-of-view shot, slow push in", chars=[], night="qin",
         comp="point-of-view shot through the narrow gap of a door held ajar, the dark edge of the door in the left foreground: the room is empty, nobody in it, no person, no face and no hand anywhere in the frame; the empty bed with its quilt folded square; the open window's blank paper puffing in and out in the night wind; moonlight falling across the empty wooden wall rack, nothing hanging on it; the candle flame on the table bent flat by the wind, nearly out",
         lines=[("xuyan", "窗開著，柴刀也不在，大半夜去哪了？", "低聲")],
         motion="the view glides slowly in through the gap into the room; the blank window paper puffs in the wind and the candle flame bends low and flickers; nobody appears",
         zh="主觀（許硯從門縫看房內）、推軌、前景門縫：空床、被子疊好；窗戶大開、窗紙（空白）一鼓一鼓；月光照在牆上空的木架上（稿子「空的刀架」寫成空木架，畫面不出現刀）；桌上一根蠟燭被風吹得斜倒快滅；許硯畫外低聲。live：主觀鏡不送許硯參考圖、寫明沒有人"),
    dict(loc="qin", cam="Medium shot, tracking", chars=["xuyan"], night="qin",
         comp=f"medium shot, framed from the waist up with clear space above his head, Xu Yan, {XU}, the bedding bundle clamped under his left arm, standing at his full height at the open window on screen right, the windowsill as high as his belt, his face in profile toward the window, never the lens; uneasy: brows drawn together, eyes searching outside, lips moving low between words, no smile; outside the window only the empty yard wall in cold moonlight, nobody there; the small table with its wind-bent candle beside him",
         lines=[("xuyan", "人不在，我明天再問她。窗先替她關上。", "低聲")],
         motion="Xu Yan tightens the bundle under his arm, looks out of the window once, his head staying inside the room, then reaches out with his right hand and pulls the window shut; the candle flame on the table rises upright again",
         zh="中景、跟拍：許硯走到窗邊（窗台到腰帶高），夾緊鋪蓋、往窗外看一眼（頭留在房裡，不探出去），伸右手把窗關上，桌上燭火立直；窗外月光下空的院牆、沒有人"),
    dict(chapter="阿令房", loc="hall_c", cam="Low-angle medium shot, slow push in", chars=["xuyan"], night="hall",
         comp=f"low-angle medium shot in the corridor, framed from the knees up with clear space above his head, Xu Yan, {XU}, the bedding bundle under his left arm, standing at his full height before the third plain wooden door on screen right, no writing on it, a thin line of warm candlelight in its crack, his face in profile toward the door, never the lens; steeling himself: brows drawn together, jaw set, eyes on the door, lips firm between words, no smile; nobody else in the corridor",
         lines=[("xuyan", "阿令，我進來了。我只是來鋪個地鋪。", "給自己壯膽")],
         motion="Xu Yan draws one deep breath, his chest rising, then pushes the door inward with his right palm and the line of candlelight widens",
         zh="低角度中景、慢推：許硯站在第三扇門前（左臂夾鋪蓋），吸一口氣、右手推門，門縫的燭光變寬（磨刀聲停是音效）；給自己壯膽說話"),
    dict(loc="ling", cam="Medium shot, slow push in", chars=["xuyan", "aling"], night="ling",
         comp=f"medium shot inside the dark room, framed from the waist up with clear space above both heads, lit only by the one candle by the bed: in the middle Xu Yan, {XU}, the bedding bundle in his arms, standing at his full height just inside the threshold, his face three-quarter to screen right, never the lens; frozen: eyes wide and fixed, face drained, lips pressed shut; right behind him by the edge of the door {ALING}, her cold face showing past his left shoulder, her eyes on the side of his face, never the lens; cold and still: brows level, eyes hard, lips barely parting on her words, no smile; {DAGGER}, {GRIP}, {SCAR} showing as her sleeve slides back; her right hand gripping his right shoulder; {ONCE}; {NOWEAPON}",
         lines=[("aling", "別動。碰我一下，你就沒命。", "冷，貼在他身後")],
         motion=f"as Xu Yan steps in, A-ling's left arm in its grey-white sleeve comes round from behind his left shoulder and lays the dagger's edge against the left side of his neck, her right hand clamping his right shoulder; Xu Yan goes rigid; Xu Yan's lips stay closed; {NOSMILE}",
         zh="中景、慢推、房裡很暗只有一根蠟燭：許硯抱鋪蓋跨進門、站著；阿令（灰白布裙、木簪、沒戴鐵鐐）在他身後門板邊，臉從他左肩後露出來，左手（灰白袖子）從他左肩後繞過來把匕首貼上他左邊頸側（左手正握、刀刃朝脖子、刀背朝外），袖子滑開露出左手腕內側發白的舊傷；右手按住他右肩；許硯僵住、嘴閉著；阿令說話、不笑"),
    dict(loc="ling_c", cam="Medium close-up, slow push in", chars=["xuyan"], night="ling",
         comp=f"medium close-up of Xu Yan, framed from the chest up with space above his head, {XU}, standing at his full height, his eyes straining sideways toward A-ling off screen left behind his shoulder, his face three-quarter, never the lens; terrified: face pale, brows drawn up, eyes wide, mouth dry and stiff between words, no smile; at the bottom edge of the frame a woman's left hand in a grey-white sleeve, {SCAR}, holding {DAGGER}, its sharp edge turned in toward his neck and its blunt back facing outward; behind him only the dark room and a little candlelight; {NOWEAPON}",
         lines=[("xuyan", "不碰！我手上只有鋪蓋，妳看。", "聲音發乾")],
         motion="Xu Yan slowly lifts both open hands up beside his face; the bedding bundle slips out of the crook of his arm and drops below the frame at his feet; the dagger hand at the bottom edge does not move",
         zh="中近景、慢推：許硯臉發白，雙手慢慢舉到臉旁，鋪蓋從臂彎掉到腳邊（畫面外）；畫面下緣是阿令左手的刀（刀刃朝他、刀背朝外）與左手腕內側的舊傷；聲音發乾"),
    dict(loc="ling_c", cam="Insert close-up, slow push in", chars=[], night="ling", act=3,
         comp=f"insert close-up looking down, the shot opens directly on a woman's left hand from its very first frame: the left hand in a grey-white cotton sleeve holding {DAGGER} in a forward grip, its sharp edge turned up toward the edge of a blue-grey robe collar at the top of the frame and its blunt back facing outward; {SCAR}, clearly visible; warm flickering candlelight; only the hand, the sleeve, the dagger and the edge of that collar are in the frame, no person and no face; {NOWEAPON}",
         lines=[],
         motion="the candlelight flickers along the blade; the hand stays perfectly steady, only her fingers tighten once on the grip",
         zh="插鏡（許硯低頭的主觀）、慢推（第一格就是握刀的手）：阿令的左手正握匕首（刀刃朝畫面上緣許硯的領口、刀背朝外），左手腕內側一道發白的舊傷；燭火晃，手很穩、只有手指收緊一下（無台詞）。live：主觀鏡不送任何人的參考圖"),
    dict(loc="ling", cam="Over-the-shoulder medium shot, slow push in", chars=["aling", "xuyan"], night="ling",
         comp=f"over-the-shoulder medium shot from behind A-ling's right shoulder: A-ling appears only once, her grey-white shoulder and the back of her head with its one plain wooden hairpin in the right foreground, her face out of the frame; Xu Yan on screen left with his back pressed flat against the shut wooden door, standing at his full height, framed from the chest up with space above his head, {XU}, both hands still raised open beside his shoulders, his face three-quarter to screen right toward her, never the lens; gentle and steady: brows easing, eyes lowered to her wrist then back up to her, lips moving softly between words, no smile; her left hand holding the dagger with its sharp edge against the side of his neck and its blunt back facing outward, {SCAR} showing at her wrist; nobody else behind him; {NOWEAPON}",
         lines=[("xuyan", "妳手腕上那道傷，是怎麼來的？", "放輕")],
         motion=f"A-ling's right hand turns him round and pushes his back against the door with a thud, her left hand keeping the dagger at the side of his neck; Xu Yan's eyes drop to her left wrist and come back up to her; A-ling's lips stay closed; {NOSMILE}",
         zh="過肩（阿令右肩後拍許硯）、慢推：前景右阿令的肩與木簪（只出現一次）；阿令右手把他推轉過來、背抵門板，左手的刀仍抵在他頸側（刀刃朝脖子、刀背朝外），手腕內側的舊傷看得到；許硯兩手還舉著、眼睛落到她手腕上再抬起來，放輕說話；阿令嘴閉著"),
    dict(loc="ling", cam="Reverse over-the-shoulder medium shot, slow push in", chars=["xuyan", "aling"], night="ling",
         comp=f"reverse over-the-shoulder medium shot from behind Xu Yan's left shoulder: Xu Yan appears only once, his blue-grey shoulder and topknot in the left foreground, his face out of the frame; on screen right {ALING}, framed from the chest up with space above her head, her face three-quarter to screen left toward him, never the lens; guarded and flat: brows level, eyes lowered and turned a little aside from his, lips barely moving between words, no smile; her left hand still holding the dagger at the side of his neck, its sharp edge in and its blunt back outward, unmoving; behind her only the dark room and the one candle by the bed; nobody else; {NOWEAPON}",
         lines=[("aling", "翻牆刮的。那道牆很高，牆裡的人也狠。", "淡")],
         motion=f"A-ling's right hand pulls her left sleeve down over the pale scar on her left wrist; the dagger in her left hand does not move; Xu Yan's lips stay closed; {NOSMILE}",
         zh="反打（許硯左肩後拍阿令）、慢推：前景左許硯的肩與髮髻（只出現一次）；阿令用右手把左袖往下拉、蓋住舊傷，左手的刀不動；眼睛垂下、略避開他（build 的視線句要她朝他說，稿子寫「眼睛避開他看畫右」，改成臉朝他、眼睛垂下偏開）；淡淡說話、不笑"),
    dict(loc="ling_c", cam="Medium close-up, tracking", chars=["xuyan"], night="ling",
         comp=f"medium close-up of Xu Yan, framed from the chest up with space above his head the whole time, {XU}, his back to the shut door, his face three-quarter to screen right toward A-ling off screen right, never the lens; quiet and settled: brows level, eyes steady on her, lips moving calmly between words, no smile; at the right edge of the frame a woman's left hand, her left sleeve pulled down over the scar on her wrist, holding {DAGGER}, its sharp edge turned toward him and its blunt back outward; behind him only the dark wooden door; {NOWEAPON}",
         lines=[("xuyan", "好，我不問。妳睡床，我睡門口。", "平靜")],
         motion="Xu Yan slowly squats down, the frame following his head down, gathers the bedding bundle up off the floor and slowly rises again to his full height; the dagger hand at the right edge follows him down and up, its edge still toward him",
         zh="近景、跟拍：許硯不追問，慢慢蹲下撿起鋪蓋再站直（稿子「彎腰」寫成蹲下、畫面跟著他的頭），畫右緣阿令的左手與刀跟著他上下（刀刃仍朝他；左袖已蓋住舊傷）；平靜說話"),
    dict(loc="ling", cam="Medium two-shot, slow push in", chars=["aling", "xuyan"], night="ling",
         comp=f"medium two-shot inside the dark room, framed from the waist up with clear space above both heads: on screen right {ALING}, standing, her face three-quarter to screen left toward Xu Yan, never the lens; disbelieving: brows drawn together, eyes narrowed, lips firm between words, no smile; {DAGGER} raised in her left hand only, its sharp edge turned toward him and its blunt back outward, her left sleeve pulled down over the scar on her wrist; on screen left Xu Yan, {XU}, standing at his full height with the bedding bundle in both arms and his back to the door, his face three-quarter to screen right toward her, never the lens, lips closed; {ONCE}; {NOWEAPON}",
         lines=[("aling", "門口？你不怕我半夜，一刀下去？", "不信")],
         motion=f"A-ling takes one step back from him, the dagger in her left hand still raised toward him, and her brows knit tighter; Xu Yan's lips stay closed; {NOSMILE}",
         zh="中景、慢推：阿令在右、許硯在左抱著鋪蓋（背對門）；阿令退一步，左手的刀沒放下（刀刃朝他、左袖蓋住舊傷），眉頭皺起，不信；許硯嘴閉著"),
    dict(loc="hall", cam="Wide shot, slow pull out", chars=["xuyan", "aling"], night="hall",
         comp=f"wide shot from the corridor past the wooden door frame in the foreground, both small in the frame, framed with clear space above their heads: just outside the threshold on the packed-earth corridor floor Xu Yan, {XU}, kneeling to unroll the bedding bundle, his face turned back over his shoulder toward the open doorway in three-quarter profile, never the lens; calm and plain: brows level, eyes on her, lips moving between words, no smile; inside the open doorway in the dim candlelight {ALING}, standing at her full height, {DAGGER} in her left hand only, her left sleeve pulled down over the scar on her wrist, her lips closed, watching him; {ONCE}; {NOWEAPON}",
         lines=[("xuyan", "怕。所以我睡外面，誰要進來，先過我。", "平實")],
         motion=f"Xu Yan steps backward over the threshold into the corridor, kneels and unrolls the bedding bundle flat along the floor outside the door, then turns his head to look back at her through the doorway; A-ling's lips stay closed; {NOSMILE}",
         zh="全景、慢拉、前景門框（長鏡，買 8 秒）：許硯倒退跨出門檻，跪在走廊泥土地上把鋪蓋攤開在門外，回頭看門裡的阿令說話；阿令（左手握刀、左袖蓋住舊傷）站在門裡、嘴閉著。場景用走廊"),
    dict(loc="ling_c", cam="Close-up, slow push in", chars=["aling"], night="ling",
         comp=f"close-up of {ALING}, her left sleeve down over her wrist, framed from the chest up with space above her head, standing just inside the doorway of the dark room, her face three-quarter to screen left toward Xu Yan off screen left beyond the doorway, never the lens; softening only a little: brows easing, eyes lowered then back on him, one corner of her mouth moving the slightest bit without ever becoming a smile, speaking very softly; behind her only the dark room and a little candlelight; {NOWEAPON} except the dagger in her left hand",
         lines=[("aling", "傻子。門外風大，被子拿厚的那條。", "極輕")],
         motion="her left hand slowly lowers the dagger to her side, its point turning down toward the floor, until hand and dagger leave the bottom of the frame; no open smile at any moment",
         zh="近景、慢推：阿令在門裡，左手的刀慢慢垂到身側（刀尖朝地）、出畫面下緣；嘴角極輕地動一下（不笑開）；極輕說話；身後只有暗的房間與一點燭光"),
    dict(loc="hall_c", cam="Low-angle close-up, slow push in", chars=["xuyan"], night="hall",
         comp=f"low-angle close-up at floor level beside the bedding laid on the packed-earth corridor floor: Xu Yan lying on his back on the unrolled grey-blue bedding, his head toward screen right, {XU}, his face turned up toward the roof beams, never the lens; wide awake: eyes open, brows level, lips closed, no smile; the wooden threshold of the door along the top edge of the frame",
         lines=[("xitong", "叮。阿令，好感加十。", "冷淡，報數")],
         panel=[("阿令 好感 +10 → 11", "panel")],
         motion=f"{QUILT} is tossed out over the threshold and lands on him, only the cuff of a grey-white sleeve showing for a moment at the top edge; Xu Yan pulls the quilt up to his chin and lies still, eyes open on the roof beams; his lips stay closed; {NOSMILE}",
         zh="低角度近景（貼著地鋪）、慢推：許硯躺在走廊地鋪上（仰躺、頭朝畫右），畫面上緣是門檻；一條深藍粗布厚棉被從門裡丟出來落在他身上（只見一截灰白袖口）；許硯把被子拉到下巴、眼睛睜著看屋樑；嘴閉著；系統（面板）"),
    dict(loc="hall_c", cam="Extreme close-up, slow push in", chars=["xuyan"], night="hall",
         comp=f"{EYES}; his eyes wide awake in the dark",
         lines=[("xitong", "隱藏任務，完成。", "冷，宣布")],
         panel=[("隱藏任務，完成", "task")],
         motion="his eyes blink once, slowly; nothing else moves",
         zh="眼睛大特寫、慢推（第一格就是眼睛）：許硯眨一下眼；系統（面板）。live：稿子的「瞳孔映淡藍光」不寫（真人版畫成發光藍瞳，preflight ERROR），改第 7 集 EYES（深棕虹膜、一點眼神光）"),
    dict(loc="hall_c", cam="Close-up, slow push in", chars=["xuyan"], night="hall",
         comp=f"close-up of Xu Yan lying on the bedding on the corridor floor, framed from the shoulders up with the dark indigo quilt pulled to his chin, {XU}, his face in profile, never the lens; worn out and rueful: brows drawn up in the middle, eyes half closed, lips pressed shut in a small crooked wry line; behind him only the dark packed-earth floor of the corridor",
         lines=[("xuyan", "種田保住了。只是這洞房，睡的是門檻。", "心裡話，嘴閉著，苦笑", "inner")],
         motion="Xu Yan rolls onto his side, turning his back to the door, and settles the quilt over his shoulder; his lips stay closed the whole shot",
         zh="近景、慢推：許硯躺著、累，翻身側躺、背對門板，把被子拉上肩；嘴閉著（心裡話），苦笑（本鏡可以苦笑，寫成嘴閉成一條歪線）"),
    dict(loc="hall_c", cam="Close-up, slow push in", chars=["xuyan"], night="hall",
         comp=f"close-up of Xu Yan lying on his side on the bedding on the corridor floor, framed from the shoulders up, {XU}, the thick dark indigo quilt over his shoulder, his face toward screen left, eyes on nothing, never the lens; sour: brows drawn down, lips pressed shut, no smile; behind him only the dark corridor",
         lines=[("xitong", "睡哪不歸系統管。好感到了，就算數。", "冷")],
         motion=f"Xu Yan grimaces with his lips shut, then yanks the quilt up over his head and lies still under it; his lips stay closed; {NOSMILE}",
         zh="近景、慢推：許硯側躺；系統說完，他嘴閉著皺一下臉，把被子往頭上一拉、蒙住頭不動"),
    dict(loc="ling_c", cam="Close shot, slow push in", chars=["aling"], night="ling",
         comp=f"close shot inside the dark room, the shot opens directly on the inside of the shut wooden door from its very first frame: {ALING}, her left sleeve pulled down over her wrist, sitting on the floor with her back against the door, her face in profile at the left edge of the frame, turned toward the door and the man beyond it, never the lens; quiet and grave: brows level, eyes lowered, lips moving softly between words, no smile; {DAGGER} lying flat across her knees, its edge turned outward, her hands off it; the dim warm light of the one candle; {NOWEAPON}",
         lines=[("aling", "許硯，你聽著就好。明天，我可能得走。", "隔著門板，很輕，慢")],
         motion=f"A-ling lifts her right hand and lays her palm flat against the wooden door beside her shoulder and leaves it there; {NOSMILE}",
         zh="門板特寫、慢推（第一格就是門板內側）：阿令背靠門板坐在地上，側臉在畫面左緣；匕首平放在膝上（刀刃朝外、手不碰刀）；左袖蓋著舊傷；伸右手、手掌貼上門板；很輕、很慢地說話，不笑（結尾）"),
    dict(loc="hall_c", cam="Close-up, slow push in", chars=["xuyan"], night="hall", act=3,
         comp=f"close-up of Xu Yan lying on his side on the bedding on the corridor floor, framed from the shoulders up, {XU}, the thick dark indigo quilt pulled over his head at first; the bottom of the wooden door at the right edge of the frame; when his face shows: startled, then still and listening, brows lifting, eyes wide on the door, lips closed, no smile",
         lines=[],
         motion=f"Xu Yan pulls the quilt down off his head, opens his eyes wide and slowly turns his head to look at the door on screen right, his face three-quarter toward it, never the lens; his lips stay closed; {NOSMILE}",
         zh="近景、慢推：門外的許硯把蒙頭的被子拉下來，睜開眼睛，轉頭看畫右的門板；嘴閉著（無台詞；第 10 集 c01 接這裡）"),
]

HEAD = [
    "- 重製版 r2、真人版（站主 2026-11-11「之後都用真人版」）：照 `docs/videos/zhong-tian-qu-qi-e009-r2/script.md`（c01–c38 對應 s01–s38；含「這版改了什麼」與「2026-11-06 審稿後的修改」：c19 用改過的系統台詞，不再是長鏡；c03 先在柴房門邊抱起鋪蓋；c21 秦霜桌上一根被風吹斜的蠟燭）；每鏡一個看得見的動作、對話用過肩與反打、一句一筆不拆半句、預設不笑。",
    "- 內部工作編號 909（`hailuo/*-dh-e909.json`、`colab/runs/e909/`、`colab/runs/e909-live/`）；發布 slug `zhong-tian-qu-qi-e009-r2`。不放集數、不放片名卡；s01 接第 8 集 s40（夜，阿令在院門口等），三人騎回家；隱藏任務不重念。",
    "- 真人版的寫法一開始就寫進來（第 5–8 集真人版的教訓）：秦霜只在 s01、背影、兩手抓韁繩、畫面裡沒有任何刀鞘兵器（稿子「柴刀插腰帶」不拍）；s21 稿子「空的刀架」寫成空木架。阿令的匕首是本集唯一的兵器：一律左手正握、刀刃朝許硯脖子、刀背朝外、不換手（s32 垂下刀尖朝地、s37 平放膝上），左手腕內側發白的舊傷 s24–s27 每鏡寫出來、s28 她拉袖子蓋住、s29 起每鏡寫「左袖蓋著舊傷」，帶刀的鏡都寫「畫面裡沒有別的刀與兵器」。",
    "- 唐小棠：服裝用真人定妝照 `tangxiaotang-portrait-l1`（交領、closed V），不寫稿子 t2 的高立領（真人版沒有 t2）。冷臉講話的近景改成從她背後拍、嘴不入鏡、台詞 nospeak（s09、s12，剪接放錄音），`e909-live/spec.json` 拿掉她三張臉部參考圖、身分句刪掉（第 8 集 fix1）；s07 是全景、臉小，照稿子正拍；s15、s17 稿子允許笑；不講話的鏡換中性外貌句。構圖裡不寫 camera。",
    "- 一鏡最多三個有名字的人：s01 唐小棠已先進屋、不入鏡（稿子四人）；主觀鏡（s05、s21、s26）不點名、不送拍攝者的參考圖，寫明畫面裡沒有人。許硯的站、坐、跪、躺每鏡寫死：唐小棠房 s07–s08 站、s09–s17 坐矮凳（頭跟她同高）、s18 站起；阿令房站著背靠門；s31 跪在走廊地上攤鋪蓋；s33 起躺在地鋪上。",
    "- 沒有字：門、燈籠、窗紙、帳冊封面都空白；攤開的帳頁虛焦。系統面板用 overlays（s16、s33、s34）。s34 眼睛大特寫用第 7 集的 EYES（深棕虹膜、一點眼神光），不寫淡藍光。",
    "- 長鏡要買的秒數（BUY）：稿子長鏡清單 c18 買 10、c31 買 8；其餘照第 8 集的估法（見 `r2.py` 的 BUY 註解）。還沒錄音，草稿用模型自己的聲音會在句中停頓，這是下限。",
]
FOOT = [
    "- **沒有場景圖（任何版本都沒有）、pilot.py 會停的**：走廊 `set-xujia-zoulang`（s02–s06、s19、s20、s23、s31、s33–s36、s38）、唐小棠房 `set-xujia-tangfang`（s07–s18）、秦霜房 `set-xujia-qinfang`（s21、s22）、阿令房 `set-xujia-lingfang`（s24–s30、s32、s37）——37 鏡；真人夜景試鏡在 `live-action/screen-test-e009.py`，站主選定後存成 `refs-live/<名字>-l1.png`，pilot.py 就會自動對到（它照檔名找 `set-<名字>-l*.png`，不用改）。`gen-dh.mjs` 的 SET 表已加這四個地點。",
    "- 只有 s01 院子有真人場景圖 `set-xujia-yuan-l2`（夜）。",
    "- `st1-ep.sh 909` 的 ref2manifest 要 `refs-dh/set-xujia-{zoulang,tangfang,qinfang,lingfang}-t1.png`（CG 版場景圖），CG 版永遠不會畫；缺一張整批就停（exit 1）。這次的免費檢查用 `runpod/refs-dh-e909/`（refs-dh 的連結，加四個佔位連結指到 CG 的 `set-xujia-wu-t1.png`）手動跑；佔位圖只在 CG 那一層，pilot.py 換真人圖時照檔名找 `-l1`，找不到就停，不會把佔位圖送出去。真人圖到了以後照 FOOT 下一條重跑。",
    "- 真人圖到了以後：`node colab/ref2manifest.mjs … --refs <runpod>/refs-dh-e909`（同 st1-ep.sh 其餘參數）→ `extras_patch.py` → `live-action/pilot.py <runpod>/a/st1 <runpod>/live/st1 s01 … s38` → `retake.py <runpod>/live/st1 <runpod>/live/d1 colab/runs/e909-live/spec.json` → `preflight-prompts.py <runpod>/live/d1/retake.json`。",
    "- 有真人定妝照（含角度圖）：許硯、許小禾、唐小棠（只有 l1 交領版，沒有 t2 高立領）、秦霜、阿令（沒戴鐵鐐的樣子；舊傷不在定妝照上，由 prompt 寫）。本集沒有新配角。",
    "- 秦霜的 `cast.json` 造型寫著「柴刀插在腰帶」：`extras.json` 與 `pilot.py` 都把這句從造型句拿掉；小禾的「hugging a small woven straw rabbit」由 `extras.json` 改成塞在腰帶上。",
    "- 配樂：走廊與唐小棠房 comedy 輕版（s16 叮抽一拍、s19 系統那句底下停一下）、秦霜房與阿令房 suspense（s24 刀貼上脖子一個重音）、s32 起很輕的暖弦（s37 只剩弦）；音效表見 script.md〈音樂與音效〉。",
]

# Long shots: seconds to buy. script.md 長鏡清單: c18 at 10 and c31 at 8. Not in the list, by e008's estimate (zh characters
# with punctuation stripped / 3.7 + 0.5 s, plus the shot's own action, against buy - 0.3 s at the cut's 1.1x): the lines
# of 14 characters or more with an action before or after them get 8 (s02 17, s03 16 + picking up the bedding, s04 15,
# s06 15, s07 16, s08 14 + setting down, s09 16 recorded, s10 15 off screen, s11 16, s12 14 recorded + the stop, s13 16,
# s17 16 + the books, s20 14 + the knock, s22 14 + the window, s23 14 + the push, s28 14, s35 15 inner + rolling over,
# s37 14 said slowly), and so do s19 (the system line, then the breath, the eyes, the brow and the walk), s27 (11 + the
# push round), s29 (11 + squatting down and up) and s32 (12 said very softly + lowering the blade). The rest stay at
# gen-dh's 5 or 6. The live drafts speak with the model's own voice, which pauses mid-line (route-a.md 2026-11-07), so
# these are a floor; re-check against the recorded or drafted voice before stage 1.
BUY = {"s02": 8, "s03": 8, "s04": 8, "s06": 8, "s07": 8, "s08": 8, "s09": 8, "s10": 8, "s11": 8, "s12": 8, "s13": 8,
       "s17": 8, "s18": 10, "s19": 8, "s20": 8, "s22": 8, "s23": 8, "s27": 8, "s28": 8, "s29": 8, "s31": 8, "s32": 8,
       "s35": 8, "s37": 8}
