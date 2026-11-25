"""Episode 8 remake (r2): the writer spec for ../e001-r2/build-r2.py. Source: docs/videos/zhong-tian-qu-qi-e008-r2/script.md
(c01-c08, c08b, c09-c25, c25b, c26-c40 = s01-s08, s08b, s09-s25, s25b, s26-s40), including its sections 「這版改了什麼」
and 「2026-11-06 審稿後的修改」, which override the tables (c13 「這箱連你手上那塊，七十塊，夠你們走一趟鏢。」; c14
「痛快！整箱我全包，大宗貨一塊算三分。」; c17 「騎我的馬去！明天把馬牽回來就行。」; c24 「這是抄本，原本在你家老爺手上，
寫的是日落。」; c08b the money box into the cloth bag and the folded copy into her sleeve; c25 split into c25 and c25b; the
lane's standing positions taken over from e007 c34-c37).

Live action from the first draft (owner 2026-11-11: 「之後都用真人版」), written the way e007-r2/r2.py wrote e004-e007's
reshoots in (route-a.md 2026-11-07 to 11-12, e907-live pick-review.md, review-picks and fix1-fix4):
- Qin Shuang's blade only where the script uses it: c25 she draws it, c25b and c26 it hangs blade-down in her right hand,
  c30 its back rests on her right shoulder. Every other shot of hers says both her hands empty (or only the reins) and no
  blade, no knife, no scabbard and no weapon of any kind anywhere in the frame; c33 (the script: 插回腰帶) and c35 do not
  show it. The escort agency's weapons rack (c10) is written as a stand of furled banners for the same reason.
- The soap: a flat square white bar, palm-sized and one finger thick, flat like a small tile; the crate and basket add no
  rolls, no cylinders and no round buns. The abacus: one small gold abacus no longer than her hand.
- Every spoken line faces its listener (build-r2.py's gaze clause); every face is written part by part, NOSMILE where the
  script allows no smile (allowed: c02 and c05 Sun Zhanggui's false smile, c15 and c33 Tang Xiaotang, c28 Qian Yuanwai's
  sneer).
- Tang Xiaotang's speaking close shots with a cool face (c07, c11, c24) are shot from behind her: she appears once, only
  the back of her head and her shoulders in the foreground, her mouth never seen; her line is `nospeak` (the recording is
  laid in). Her silent shots get e907 fix2/fix3's neutral face sentences in `colab/runs/e908-live/spec.json`. The word
  "camera" is never written into a composition (e907 s08, s20 drew a camera when told "turned away from the camera").
- At most three named people on screen: c26 leaves Tang Xiaotang out (the script has four); Zong Biaotou (the escort
  chief) and the gatekeeper have no portrait and are shown from behind or from the shoulders down only, their lines
  `nospeak` or off screen; the extras (escort men, servants, neighbours, the maid) are written in Song-dynasty clothing.
- Over-the-shoulder shots say the foreground person appears once and nobody else stands behind.
- No writing anywhere: boards, lanterns, the money box, abacus and ingot blank; the copy of the IOU (c08b, c24) folded or
  its blank back to the lens; c31's IOU face down. The panels are overlays (s03, s20, s30, s31, s36, s37, s38).
- Inserts open directly on their subject; c36's eye extreme close-up is e907's EYES (the script's 「瞳孔裡映著淡藍光」 is
  an ERROR in preflight-prompts.py); speakers who rise get headroom; no "leans" or "bends" (c02, c04, c08, c13, c29).
State: Xu Yan sweating with a little white soap dust on his cuffs c01-c18, dusty and panting c19-c32, tired c33-c39; Tang
Xiaotang's buns slightly askew with one pearl pin crooked from c19; the small gold abacus on the table c01-c08, at her
waist from c09; A-ling (no shackles) only in c40. Opens on the next instant after e007 c37: Sun Zhanggui's ingot on the
table, Xu Yan standing behind it, Tang Xiaotang half turned away beside him, Qin Shuang at the table's right end.
Places: the lane is "the lane behind the county silk shop" (gen-dh -> set-chouduan, live set-chouduan-l1); the escort
agency "escort agency" (-> set-biaoju-t1); the Qian manor gate and its outer wall "Qian manor gate" (-> set-qianfu-men-t1);
the hall "the main hall of the Qian manor" (-> set-qianfu-ting-t1); the road has no set; the Xu gate at night "yard gate"
(-> set-xujia-yuan, live l2). biaoju, qianfu-men and qianfu-ting have no live-action picture: pilot.py stops on those
shots until the owner has them drawn (listed in FOOT).
"""
EP = 908  # internal working number; the published slug is zhong-tian-qu-qi-e008-r2
SLUG = "zhong-tian-qu-qi-e008-r2"
EP_TITLE = "五十兩不賣方子，太陽還沒落（重製版 r2）"
OUTLINE_SECONDS = 244  # script.md 2026-11-06: 55 + 55 + 12 + 122 s, 42 shots
TARGET_MINUTES = [3, 5]
TITLE = "五十兩不賣方子，太陽還沒落｜種田娶妻打天下 第8集（重製版）"
DESCRIPTION = "第四天申時，綢緞莊後巷。孫掌櫃開五十兩買肥皂方子，許硯把銀錠推回去：「方子賣一次就沒了，肥皂能賣一輩子。」手上十八兩，還差二兩，城裡能賣的都賣光了；唐小棠看到一個滿身汗的鏢師走過巷口，想到城外的鏢局。宗鏢頭洗了一次就整箱七十塊包下，二兩一錢，湊齊二十兩一錢。秦霜騎著借來的馬載兩人趕路，錢府門房關門說「申時已過」，許硯指著還沒落的太陽：字據寫的是日落。秦霜踹開大門，錢員外想賴，看到門外半條街的街坊，只好把字據摔出來，許硯當場撕掉，負債清零。出了錢府，側門木樁上掛著一頂繫紅繩的舊草帽，跟他落水那晚河邊的一樣；系統接著下隱藏任務：今夜洞房花燭，失敗扣除種田技能。《種田娶妻打天下》第 8 集（重製版）。"
THUMB = ("太陽還沒落", "s22")
CHARACTERS = ["xuyan", "tangxiaotang", "qinshuang", "sunzhanggui", "zongbiaotou", "menfang", "qianyuanwai", "aling", "xitong"]
# No portrait and not in cast.json (script.md: 聲音沒有在 cast.json 裡，開拍前選定後記進去). The voices are a proposal
# for the owner; both men are always from behind or below the shoulders, so their lines are recorded (nospeak or off).
MINOR = {
    "zongbiaotou": {"id": "zongbiaotou", "name": "宗鏢頭",
                    "appearance": "East Asian man of forty-five, big and broad-backed, an ancient Chinese Song-dynasty escort's brown coarse hemp cross-collared short jacket with the sleeves rolled to the elbows, a brown cloth head-wrap, a wide leather belt with one grey cloth money pouch at the waist, cloth shoes; seen only from behind or from the shoulders down",
                    "voice": {"provider": "gemini", "name": "Alnilam", "style": "標準國語，咬字清楚，台北人平常說話的語調；四十五歲的鏢局鏢頭，男聲、粗、大嗓門、豪爽，說話短、一句一個重音"}},
    "menfang": {"id": "menfang", "name": "門房",
                "appearance": "East Asian man of fifty, thin, an ancient Chinese Song-dynasty gatekeeper's grey-blue cross-collared long gown, cloth shoes, both hands tucked into his sleeves; seen only from behind or from the shoulders down",
                "voice": {"provider": "gemini", "name": "Schedar", "style": "標準國語，咬字清楚，台北人平常說話的語調；五十歲的大戶人家門房，男聲、勢利、拖長音、狗仗人勢"}},
}
MUSIC = "one cue per scene: a light tense pulse of low plucked strings in the late afternoon silk shop lane, dropping out for one beat on the system chime and turning light and quick when the escort walks past; a bright playful comedy of woodblock, pipa and dizi in the escort agency's compound, one rising accent as the money is counted; fast urgent drums matching the hoofbeats on the road at sunset; a low tense cue of drums and erhu at the manor gate and in the hall, one heavy hit as the IOU is torn; a low suspense cue of low cello and soft guqin by the outer wall at dusk, dropping to only the wind on the last system line; ancient Chinese rural drama, no vocals"

# Scene headers of script.md. Scene 1: the lane behind the county silk shop as e007 scene 3 (the small table and Xu Yan on
# screen left, the red back door on screen right, the mouth of the lane deep in the background), the low orange sun from
# the mouth of the lane. Scene 2: the escort agency's compound (the well and washing trough on screen right, the gate at
# the back left, the low sun from the left). The road: the horse runs right to left toward the red sun. Scene 3: the Qian
# manor gate (the gate up the steps on the right, the sun on the left), the hall (doorway left, table right), the outer
# wall at dusk (they walk toward screen left). Then the Xu yard gate at night. Close shots use the short `_c` headers.
LOC = {
    "lane": "In the lane behind the county silk shop in the late afternoon: one small plain wooden table on screen left with one small wooden money box on it, one plain wooden crate under it and one bamboo basket beside it, one empty wooden handcart at the table's right end, one red-painted back door in a whitewashed wall on screen right under a blank lintel board, bamboo poles hung with lengths of plain-dyed silk drying across the lane, flagstones, the mouth of the lane deep in the background, the low orange sun shining in from the mouth of the lane, long shadows stretching toward the foreground",
    "lane_m": "In the lane behind the county silk shop in the late afternoon: the small plain wooden table on screen left, plain-dyed silk drying on bamboo poles, flagstones, the mouth of the lane deep behind, the low orange sun from there and long shadows toward the foreground",
    "lane_c": "In the lane behind the county silk shop in the late afternoon, the low orange sun from the mouth of the lane",
    "agency": "In the packed-earth compound of an escort agency outside the city in the late afternoon: one stone well and one long stone washing trough on screen right, one wooden stand of escort banners furled tight with no writing in the left foreground, the compound gate at the back left under a blank board with no writing, the low sun from the left throwing long shadows across the packed earth",
    "agency_m": "In the packed-earth compound of an escort agency outside the city in the late afternoon: the stone well and washing trough on screen right, the compound gate at the back left, the low sun from the left",
    "agency_c": "In the compound of an escort agency in the late afternoon, the low sun from the left",
    "road": "On a dirt road through open countryside just before sunset: golden rice fields on both sides, a far mountain ridge with the low red sun hanging just above it ahead on screen left, the light coming from ahead, dust glowing in the air",
    "gate": "At the Qian manor gate at sunset: stone steps up to a vermilion double gate under a blank board with no writing, one stone lion on each side of the steps, the red setting sun half sunk behind a far ridge on screen left, red light from the left",
    "gate_c": "At the Qian manor gate at sunset, red light from the left",
    "hall": "In the main hall of the Qian manor at sunset: one red-wood table on screen right with a carved armchair behind it and a plain folding screen with no writing and no paintings behind that, the doorway on screen left, one beam of red-gold sunset light slanting in across the floor from the doorway",
    "hall_c": "In the main hall of the Qian manor at sunset, a beam of red-gold sunset light from the doorway on screen left",
    "wall": "Along the whitewashed outer wall beside the Qian manor gate at dusk: the sky turning deep blue, a few blank paper lanterns just lit along the wall, plain with no writing, one small side door in the wall with one wooden post beside it",
    "wall_c": "Along the whitewashed outer wall beside the Qian manor gate at dusk, warm lantern light and a deep blue sky",
    "night": "At the yard gate in the bamboo fence of the Xu farmhouse at night: one blank paper lantern with no writing hanging by the gate, the dark house door behind it, the dirt village road leading off to screen left, cool blue moonlight",
}
LIGHT = {
    "lane": "the low orange afternoon sun from the mouth of the lane stays unchanged",
    "agency": "the low afternoon sun from the left stays unchanged",
    "road": "the red sun low ahead keeps sinking slowly",
    "gate": "the red sunset light from the left stays unchanged",
    "hall": "the beam of red-gold sunset light stays unchanged",
    "wall": "the dusk light and the lantern glow stay unchanged",
    "night": "the cool blue night light and the lantern glow stay unchanged",
}

# Repeated wording (each prop is one object; the descriptions say "one" where it first appears).
XU_SWEAT = "his faded blue-grey scholar's robe with one small sewn cloth patch at one elbow and both shoulders whole, beads of sweat on his forehead, a little white soap dust on his cuffs"
XU_DUST = "his faded blue-grey scholar's robe with one small sewn cloth patch at one elbow and both shoulders whole, the robe dusty from the road, sweat on his forehead, breathing hard"
XU_TIRED = "his faded blue-grey scholar's robe with one small sewn cloth patch at one elbow and both shoulders whole, dusty, tired"
TANG = "in her peach-pink cross-collared short jacket wrapped shut over a pleated skirt with a ribbon bow"
# c19 on (script: 髮髻有點歪、一根珍珠簪斜了, every shot)
TANG_RODE = "in her peach-pink cross-collared short jacket wrapped shut over a pleated skirt with a ribbon bow, her two looped buns knocked a little askew and one pearl pin slanting"
CHEST = "framed from the chest up with space above her head"
# e907 fix3 s08/s20: the only way her cool lines held: her face never in the frame (no "camera" in the wording).
BEHIND = ("{who} appears only once: only the back of her head with its two looped buns and pink silk ribbons{extra} and her "
          "shoulders in the {side} foreground, her face turned away toward {to} and never seen at any moment, her cheek, lips "
          "and mouth never visible")
ABACUS = "one small gold abacus no longer than her hand, plain with no marks or writing"
QIN = "her dark brown cross-collared short jacket, wide leather belt, black trousers, leather boots and high ponytail"
EMPTY = "both her hands empty, no blade, no knife, no scabbard and no weapon of any kind anywhere in the frame"
REINS = "her hands holding only the reins, no blade, no knife, no scabbard and no weapon of any kind anywhere in the frame"
MACHETE = "her old firewood machete (a long narrow iron blade with a slightly hooked tip, black-cloth-wrapped wooden handle)"
SUN = "Sun Zhanggui, a lean man in his forties with a long narrow face, hollow cheeks and a thin grey-streaked beard, in a Song-dynasty green satin cross-collared robe with a jade belt hook"
QIAN = "Qian Yuanwai, a short portly man of fifty with a round face and a thin eight-shaped moustache, in his dark gold silk robe with roundel patterns, his hands of an ordinary skin tone"
ZONG = "the escort chief, a big broad-backed man in a Song-dynasty brown coarse hemp cross-collared short jacket with the sleeves rolled to the elbows, a brown cloth head-wrap and a wide leather belt"
GATEKEEPER = "the gatekeeper, an old servant in a Song-dynasty grey-blue cross-collared long gown and cloth shoes"
ESCORTS = "escort men in Song-dynasty coarse hemp cross-collared short jackets with the sleeves rolled up, cloth head-wraps and cloth shoes"
SERVANTS = "house servants in Song-dynasty black cross-collared short jackets, cloth head-wraps and cloth shoes"
NEIGHBOURS = "townsfolk in Song-dynasty coarse hemp cross-collared short jackets, cloth head-wraps and cloth shoes"
MAID = "one young servant girl of fifteen in a Song-dynasty pale green cotton cross-collared jacket, her hair in two small side buns"
SOAP = "one flat square white bar of soap, palm-sized and one finger thick, flat like a small tile, plain with no marks or writing"
CRATE = "one plain wooden crate of pale raw wood, a long box no wider than her shoulders, with its lid shut, no marks or writing"
CRATE_FULL = "rows of flat square white bars of soap, each palm-sized and one finger thick, flat like a small tile, packed flat in layers, no rolls, no cylinders and no round buns"
BASKET = "one bamboo basket full of flat square white bars of soap, each palm-sized and one finger thick, flat like a small tile, no rolls, no cylinders and no round buns"
CASHBOX = "one small wooden money box with a lid, as wide as a palm is long, plain wood with no marks or writing"
BAG = "one big grey cloth money bag tied with a drawstring"
POUCH = "one small grey cloth money pouch the size of a fist"
SILVER = "small lumps of plain broken silver"
INGOT = "one big silver yuanbao ingot shaped like a boat, as long as two palms side by side, plain silver-white with no marks or writing"
HORSE = "one chestnut-red horse with a saddle and reins"
HAT = "one old straw hat, wheat-coloured, one corner of its brim broken, one thin red cord tied round the brim"
EYES = "extreme close-up filling the whole frame edge to edge with only Xu Yan's two eyes and brows, no nose and no mouth in the frame, the shot opens directly on his eyes from its very first frame, natural dark brown irises with a tiny catchlight, his gaze slightly off to screen left and never into the lens"
NOSMILE = "no smile at any moment, not even at the end of the shot, until the last frame"
ONCE = "each person appears only once, nobody else behind them"


def behind(who="Tang Xiaotang", side="left", to="the person she speaks to", extra=""):
    return BEHIND.format(who=who, side=side, to=to, extra=extra)


SHOTS = [
    # ---- scene 1: the lane behind the county silk shop (as e007 scene 3), the hour of shen. Axis: the table and Xu Yan on
    # screen left, Tang Xiaotang beside him (middle), Qin Shuang at the table's right end, Sun Zhanggui in front of the
    # table on screen right facing left, the red back door on the right, the mouth of the lane deep behind.
    dict(chapter="後巷", loc="lane_m", cam="Over-the-shoulder medium shot, slow push in", chars=["sunzhanggui", "xuyan", "tangxiaotang"], night="lane",
         comp=f"over-the-shoulder medium shot from behind Sun Zhanggui's left shoulder: his green satin shoulder and the tip of his grey-streaked beard in the right foreground, his face out of the frame; Xu Yan standing behind the small table on screen left, framed from the waist up with space above his head, {XU_SWEAT}, his face three-quarter to screen right toward Sun Zhanggui, never the lens; calm and settled: brows level, eyes steady, lips firm between words; beside him in the middle of the frame, soft and out of focus, Tang Xiaotang {TANG}, half turned away, only her shoulder and her right hand resting on {ABACUS} on the table showing; on the table {INGOT} and {CASHBOX}; {ONCE}",
         lines=[("xuyan", "方子不賣。孫掌櫃，這銀子您收回去。", "平靜")],
         motion=f"Xu Yan sets two fingers of his right hand on the silver ingot, holds a beat, slides it across the tabletop to Sun Zhanggui and draws his hand back to rest on the table; Sun Zhanggui's lips stay closed; {NOSMILE}",
         zh="過肩（孫掌櫃左肩後拍許硯）、慢推（中景推到中近景）：前景右孫掌櫃的綠緞肩與花白鬍尾；許硯站在桌後（額頭有汗、袖口沾皂屑），兩根手指按住銀錠、停一拍、推過桌面，手收回放在桌上；畫面中間虛焦的唐小棠只露半轉身的肩與按在小金算盤上的右手；桌上一錠船形大銀、小金算盤、木錢箱。live：站位接第 7 集 s35–s36（許硯站著、孫掌櫃站在桌前畫右）；三人各出現一次"),
    dict(loc="lane_c", cam="Over-the-shoulder medium close-up, slow push in", chars=["sunzhanggui", "xuyan"], night="lane",
         comp=f"reverse over-the-shoulder medium close-up from behind Xu Yan's right shoulder: his blue-grey shoulder and topknot in the left foreground, his face out of the frame; {SUN}, standing on screen right across the small table, framed from the chest up with space above his head, his face three-quarter to screen left toward Xu Yan, never the lens; smooth and mocking: one corner of his mouth lifted in a thin false smile, eyes half-lidded, brows level; the silver ingot on the table at the bottom edge; {ONCE}; behind him only the drying silk of the same silk shop lane",
         lines=[("sunzhanggui", "五十兩不要？你還差人家二兩呢。", "慢條斯理")],
         motion="Sun Zhanggui strokes his grey-streaked beard once with his left hand, taps the silver ingot twice with his right forefinger without taking it, and his upper body tips a little forward over the table, his whole head staying in the frame; Xu Yan's lips stay closed",
         zh="反打（許硯右肩後拍孫掌櫃）、慢推（中近景推到近景）：孫掌櫃左手捻一下花白長鬍，右手食指敲銀錠兩下、不收，身子往前傾（寫成上身微微前傾、頭留在畫面裡，不寫 leans）；本鏡可以假笑（寫嘴角一邊往上的假笑）"),
    dict(loc="lane_c", cam="Close-up, slow push in", chars=["tangxiaotang"], night="lane", act=3,
         comp=f"close-up of Tang Xiaotang {CHEST}, {TANG}, standing at the table, half turned away from Sun Zhanggui off screen right; struck still: brows level, eyes wide and steady, lips closed; behind her only the brick wall of the same silk shop lane",
         lines=[("xitong", "叮。唐小棠，好感加三。", "冷淡，報數")],
         panel=[("唐小棠 好感 +3 → 13", "panel")],
         motion=f"her right hand, below the frame on the abacus, stops; she slowly turns her head toward Xu Yan off screen left and her eyes settle on him, never on the lens; her lips stay closed; {NOSMILE}",
         zh="近景、慢推（稿子下巴以上，真人版胸口以上）：唐小棠站在桌邊、半轉身背對畫右的孫掌櫃，按在算盤上的手停住（手在畫面外），慢慢轉頭看畫左的許硯，眼神定住；嘴閉著；系統（面板）。live：不說話的鏡，spec.json 加中性外貌句"),
    dict(loc="lane_c", cam="Medium close-up, tracking", chars=["xuyan"], night="lane",
         comp=f"medium close-up of Xu Yan standing behind the small table, framed from the waist up with clear space above his head, {XU_SWEAT}, {SOAP} in his right hand, the edge of one green satin sleeve at the right edge of the frame, his face three-quarter to screen right toward Sun Zhanggui off screen right, never the lens; steady and sure: brows level, eyes on him, lips firm between words; behind him only the drying silk of the same silk shop lane",
         lines=[("xuyan", "方子賣一次就沒了，肥皂能賣一輩子。", "很穩")],
         motion=f"Xu Yan lowers the bar of soap into the open crate at his feet below the frame, pulls the lid shut with a knock, and his eyes come back up to Sun Zhanggui, his whole head staying in the frame the whole time; {NOSMILE}",
         zh="中近景、跟拍：許硯把一塊白皂放回桌下的木箱、蓋上箱蓋，抬眼看孫掌櫃說話；畫右緣只露綠緞袖子。live：稿子「彎腰」改成手往下放進腳邊木箱、頭一直留在畫面裡（彎腰會出畫）"),
    dict(loc="lane_m", cam="Medium shot, tracking", chars=["sunzhanggui"], night="lane",
         comp=f"medium shot past the corner of the small table and the wooden money box in the left foreground: {SUN}, framed from the waist up with space above his head, the silver ingot in his right hand, his face three-quarter to screen left toward Xu Yan off screen left, never the lens; a thin false smile at one corner of his mouth, eyes cold and half-lidded; behind him the mouth of the lane in the low orange sun",
         lines=[("sunzhanggui", "志氣是好。只怕二兩還沒湊齊，太陽先落了。", "話裡藏刀")],
         motion="Sun Zhanggui slips the silver ingot into his right green satin sleeve, turns and walks two steps toward the mouth of the lane, stops and looks back over his shoulder toward the table",
         zh="中景、跟拍、前景左桌角與木錢箱：孫掌櫃把銀錠收進右邊綠緞袖子，轉身往巷口走兩步，停下回頭；本鏡可以假笑"),
    dict(loc="lane", cam="Low-angle wide shot, slow push in", chars=["sunzhanggui"], night="lane",
         comp=f"low-angle wide shot from floor level past one corner of the wooden crate under the table in the foreground: {SUN}, seen from behind, small in the frame, walking away down the lane toward its mouth through the drying silk; nobody else in the lane",
         lines=[("tangxiaotang", "他說得對，城裡今天能賣的都賣光了。", "畫外，小聲")],
         motion="Sun Zhanggui's back walks out of the mouth of the lane, his sleeve brushing the hanging silk, and turns right out of sight; the lengths of silk keep swaying after him; no face is seen",
         zh="低角度全景、慢推、前景桌下木箱一角：孫掌櫃的背影走出巷口，衣角拂過晾著的布，往巷口右邊消失；布還在晃；唐小棠畫外說話"),
    # Converted: Tang Xiaotang's speaking close-up (script c07) from behind her; the line is laid in from the recording.
    dict(loc="lane_c", cam="Over-the-shoulder medium shot, slow push in", chars=["tangxiaotang"], nospeak=["tangxiaotang"], night="lane",
         comp=f"over-the-shoulder medium shot from just behind Tang Xiaotang's right shoulder, looking down the lane: {behind(side='right', to='the mouth of the lane')}; deep beyond her at the mouth of the lane, small and soft, one of the escort men from the agency outside the city walking past, in a Song-dynasty coarse hemp cross-collared short jacket dark with sweat and a cloth head-wrap, one rolled-up banner tied on his back, rolled tight with no writing showing; nobody else in the lane",
         lines=[("tangxiaotang", "等等，城外有鏢局，鏢師天天一身臭汗！", "恍然，眼睛一亮，不笑開")],
         motion="the escort man walks from right to left across the mouth of the lane and out of sight; Tang Xiaotang's head turns slowly to follow him, then lifts sharply, her face still turned away toward the lane; her right hand rises into view at her shoulder and flicks three beads on the small gold abacus in it",
         zh="【改背後拍】過肩、慢推：從唐小棠右肩後往巷口看，她只出現一次（只有前景的後腦、丸子頭與肩），臉轉向巷口、嘴不入鏡；巷口虛焦一個鏢師（宋式粗布交領短打、汗濕、背上捲起的鏢旗看不到字）從右走到左；她的頭跟著轉、猛一抬，右手在肩邊撥三顆算珠。台詞 nospeak，剪接放錄音。稿子是下巴以上近景、她講話（冷臉近景講話必笑，第 7 集 s08、s20 的教訓）"),
    dict(loc="lane_m", cam="Over-the-shoulder medium shot, slow push in", chars=["xuyan", "tangxiaotang"], night="lane",
         comp=f"over-the-shoulder medium shot from behind Tang Xiaotang's left shoulder: Tang Xiaotang appears only once, her shoulder and the back of her head with its two looped buns and pink silk ribbons in the right foreground, her face out of the frame; Xu Yan behind the small table on screen left, framed from the waist up with clear space above his head, {XU_SWEAT}, his face three-quarter to screen right toward Qin Shuang off screen right, never the lens; decided: brows level, eyes bright and steady, lips firm between words; nobody else behind him",
         lines=[("xuyan", "一身汗的人最懂肥皂的好。秦霜，箱子交給妳。", "下定決心")],
         motion=f"Xu Yan hauls {CRATE} up from under the table with both hands and thumps it down on the right end of the tabletop, his whole head staying in the frame the whole time, then turns his face to Qin Shuang off screen right; Tang Xiaotang's lips stay closed; {NOSMILE}",
         zh="過肩（唐小棠左肩後拍許硯）、慢推（長鏡）：前景右唐小棠的肩與丸子頭；許硯從桌下抱出木箱（原木色長方形、蓋著），砰一聲放上桌子右頭，朝畫右外的秦霜說。live：不寫彎腰、頭留在畫面裡；唐小棠只出現一次"),
    dict(sid="s08b", loc="lane_c", cam="Insert close-up, high angle, slow push in", chars=[], night="lane",
         comp=f"high-angle insert close-up, the shot opens directly on the open wooden money box on the table from its very first frame: {CASHBOX} with its lid open, {SILVER} and a few strings of copper coins inside; two slender hands in peach-pink cuffs holding the mouth of {BAG} open beside it; one man's hand in a blue-grey cuff waiting at the edge of the frame; only the hands, cuffs, money box, bag and coins are in the frame, no face; behind them only the flagstones of the same silk shop lane",
         lines=[],
         motion="the slender hands tip the silver and the strings of coins from the money box into the cloth bag, pull the drawstring tight, knot it and lay the heavy bag in the man's hand, which closes on it and draws it out of the frame; then the slender fingers slide one folded slip of pale yellow paper, folded shut, out of the bottom of the empty box and tuck it away into the peach-pink sleeve",
         zh="手部特寫、俯拍、慢推（第一格就是錢箱）：唐小棠的兩手（桃粉袖口）把錢箱裡的碎銀、銅錢串倒進灰布大錢袋，拉緊打結，放到許硯手上（藍灰袖口），他接過收出畫；她再從空錢箱底抽出一張摺好的淡黃紙（摺著，紙面不露）收進右袖（無台詞）"),
    dict(loc="lane_m", cam="Wide shot, tracking", chars=["qinshuang", "xuyan", "tangxiaotang"], night="lane",
         comp=f"wide shot past lengths of drying silk in the foreground, everyone small in the frame: Qin Shuang, {QIN}, standing at the right end of the small table beside the wooden crate on it, her face in profile toward Xu Yan, never the lens; brisk: brows level, eyes steady, lips firm between words; behind the table Xu Yan, {XU_SWEAT}, and Tang Xiaotang {TANG}, {ABACUS} tied at her waist, lips closed; {BASKET} beside the table and the empty handcart at its right end; at the red back door on screen right in the background {MAID}; {ONCE}",
         lines=[("qinshuang", "鏢局在城東五里，扛著箱子跑，日落前到得了。", "乾脆")],
         motion=f"Qin Shuang lifts the wooden crate off the table with both arms, swings it up onto her right shoulder and strides off toward the mouth of the lane, her head staying in the frame; Xu Yan and Tang Xiaotang follow her; in the background the servant girl lifts the basket of soap and the empty money box onto the handcart and pulls the cart in through the red back door; all other lips stay closed; {NOSMILE}",
         zh="全景、跟拍、前景晾著的布（長鏡）：秦霜雙手抱起桌上木箱、一甩扛上右肩往巷口走，許硯、唐小棠（腰間繫回小金算盤）跟上；背景丫鬟把那筐白皂（十七塊）和空錢箱放上推車、拉進紅色後門寄放。live：稿子寫柴刀插腰帶，這鏡不提刀（兩手抱箱）；三人各出現一次"),
    # ---- scene 2: the escort agency's compound, late in the hour of shen. Axis: the three come in at the gate on the back
    # left and stand on screen left; the well, the trough, the escort men and Zong Biaotou on screen right.
    dict(chapter="鏢局", loc="agency_m", cam="Wide shot, tracking", chars=["tangxiaotang", "qinshuang", "xuyan", "zongbiaotou"], night="agency",
         comp=f"wide shot past the stand of furled banners in the left foreground, everyone small in the frame: on screen left Tang Xiaotang {TANG}, walking in through the compound gate, her face in profile toward the well on screen right, never the lens; bright and loud: brows lifted, eyes wide, mouth opening wide on each word; beside her Qin Shuang, {QIN}, {CRATE} on her right shoulder held with both hands, no blade, no knife and no weapon of any kind anywhere in the frame; Xu Yan, {XU_SWEAT}, behind them; on screen right at the well about five {ESCORTS} splashing water; in the right foreground the broad back of {ZONG}, his face out of the frame",
         lines=[("tangxiaotang", "宗鏢頭在嗎？柳溪許家來賣肥皂，洗一次就知道！", "揚聲")],
         nospeak=["zongbiaotou"],
         motion="Tang Xiaotang lifts one corner of the crate's lid on Qin Shuang's shoulder, takes out one flat square white bar of soap and holds it high as she calls out; the escort men at the well look up; the escort chief in the foreground turns half round, only his back and the back of his head-wrap seen",
         zh="全景、推軌（往右）、前景捲起的鏢旗架（長鏡）：唐小棠邊走進院門邊掀開秦霜肩上木箱一角，拿出一塊白皂高舉喊；井邊鏢師抬頭；前景右宗鏢頭的寬背轉過半身（只見背與後腦布包頭）。live：稿子的兵器架改成鏢旗架（畫面裡有兵器會跟秦霜的禁刀句衝突、也會被她拿起來）；全景臉小，唐小棠照稿子露臉喊"),
    # Converted: the script's over-the-shoulder from behind Zong (his face never shown) put her cool speaking face toward the
    # lens; now from behind her, his head above the top edge, both lines laid in from the recordings.
    dict(loc="agency_m", cam="Over-the-shoulder medium shot, slow push in", chars=["tangxiaotang", "zongbiaotou"], nospeak=["tangxiaotang", "zongbiaotou"], night="agency",
         comp=f"over-the-shoulder medium shot from just behind Tang Xiaotang's left shoulder: {behind(side='left', to='the escort chief')}; facing her on screen right, close, {ZONG}, framed so the top edge of the frame cuts him off at the chin: only his broad chest, belt and big hands are in the frame, his face never seen; one {SOAP.replace('one ', '', 1)} in her right hand; far behind, soft and out of focus, the escort men at the well; nobody else",
         lines=[("zongbiaotou", "又是賣肥皂的？上個月那批洗完還是臭！", "大嗓門，不耐煩"),
                ("tangxiaotang", "那是別人家的。這塊洗一次，不香不要錢。", "篤定")],
         motion="the escort chief's right hand waves her off with one big sweep; Tang Xiaotang steps in, presses the bar of soap firmly into his palm and closes his fingers over it, her head giving one small tilt, her face still turned away toward him",
         zh="【改背後拍】過肩、慢推（長鏡，10 秒）：從唐小棠左肩後拍，她只出現一次（前景只有後腦、丸子頭與肩），臉朝宗鏢頭、嘴不入鏡；宗鏢頭在畫右、畫面上緣切在他下巴，只見胸口、腰帶與大手；他右手一揮要趕人，她上前把白皂硬塞進他手裡、歪一下頭。兩句都 nospeak（宗鏢頭沒有臉、唐小棠背對），剪接放錄音。稿子是從宗鏢頭肩後拍唐小棠正臉講話"),
    dict(loc="agency_c", cam="Insert close-up, high angle, slow push in", chars=[], night="agency",
         comp=f"high-angle insert close-up, the shot opens directly on two big rough hands in a long stone washing trough of clear water from its very first frame: brown coarse hemp sleeves rolled to the elbows, {SOAP} between the hands; at the top edge two {ESCORTS.replace('escort men', 'escort men seen only from the shoulders to the chin')}; only the hands, sleeves, trough, water and soap and those two shoulders are in the frame, no full face; behind them only the packed earth of the same escort agency",
         lines=[("zongbiaotou", "咦……真的起泡，還有一股皂角香。", "一愣，驚訝")],
         motion="the big hands rub the soap and white lather swells up over both palms; the hands lift out of the water toward the top edge of the frame and stop there; the two escort men's chins push in closer to look",
         zh="手部特寫、俯拍、慢推（第一格就是手在洗衣槽裡）：宗鏢頭一雙粗大的手（褐色短打袖子捲到手肘）在石槽裡搓皂，泡沫堆滿手掌，手舉起來湊到畫面上緣去聞、停住；兩個鏢師只露肩與下巴湊過來；宗鏢頭畫外說話"),
    dict(loc="agency_m", cam="Low-angle medium shot, slow push in", chars=["qinshuang"], night="agency",
         comp=f"low-angle medium shot of Qin Shuang, framed from the knees up with clear space above her head, {QIN}, {EMPTY}, the wooden crate on her right shoulder, her face three-quarter to screen right toward the escort chief off screen right, never the lens; matter-of-fact: brows level, eyes steady, lips firm between words; two hands of escort men in Song-dynasty hemp sleeves reaching in from the right edge; behind her only the packed earth of the same escort agency",
         lines=[("qinshuang", "這箱連你手上那塊，七十塊，夠你們走一趟鏢。", "平淡")],
         motion=f"Qin Shuang swings the crate down off her shoulder and sets it on the ground with a thud, crouches and throws its lid open on {CRATE_FULL}, one gap in the top layer where one bar is missing, then rises again to her full height, her whole head staying in the frame, and turns to the escort chief off screen right; {NOSMILE}",
         zh="低角度中景、慢推（長鏡）：秦霜把木箱從右肩往地上一放（砰），蹲下掀開箱蓋：一層層排好的扁方白皂、上層缺一塊（六十九塊），站起來朝畫右外的宗鏢頭說；鏢師的手從畫右伸進來。live：兩手空、畫面裡沒有刀；膝以上、頭上留空"),
    dict(loc="agency_c", cam="Medium shot, slow push in", chars=["zongbiaotou"], nospeak=["zongbiaotou"], night="agency",
         comp=f"medium shot of {ZONG}, framed from the shoulders down so his face is never in the frame: his broad chest, wide leather belt and {POUCH} tied at his waist; the open wooden crate of {CRATE_FULL} before him at the bottom of the frame; one escort man's hand in a hemp sleeve reaching into the crate; behind him only the packed earth of the same escort agency",
         lines=[("zongbiaotou", "痛快！整箱我全包，大宗貨一塊算三分。", "豪爽")],
         motion="the escort chief's left hand slaps the escort man's hand away, his right palm smacks down flat on the crate's lid, then he unties the money pouch from his belt and tosses it out to screen left",
         zh="中景（宗鏢頭肩膀以下）、慢推：腰帶上一個拳頭大的灰布錢袋；他左手拍掉鏢師伸進箱子的手，右掌啪一聲拍在箱蓋上，從腰間解下錢袋往畫左一丟；臉不入鏡。台詞 nospeak（剪接放錄音）"),
    # Tang Xiaotang may smile here (the script); written as face movements. Waist up so the abacus at her waist is in the frame.
    dict(loc="agency_c", cam="Medium close-up, slow push in", chars=["tangxiaotang"], night="agency",
         comp=f"medium close-up of Tang Xiaotang framed from the waist up with space above her head, {TANG}, {ABACUS} tied at her waist, her face three-quarter to screen right toward the escort chief off screen right, never the lens; delighted: brows lifting, eyes shining, cheeks rising, mouth opening into a bright smile; behind her only the packed earth of the same escort agency",
         lines=[("tangxiaotang", "七十塊，二兩一錢。加上十八兩，湊齊了！", "笑")],
         motion=f"Tang Xiaotang catches {POUCH} in both hands and weighs it once, then her left fingertip flicks one bead on the abacus at her waist and she laughs",
         zh="中近景、慢推（稿子下巴以上；要拍到腰間算盤，改腰以上）：唐小棠雙手接住錢袋、掂一掂，左手指尖撥一顆腰間小金算盤的珠子，笑出來（本鏡可以笑）"),
    dict(loc="agency_m", cam="Over-the-shoulder medium shot, slow push in", chars=["xuyan", "tangxiaotang"], night="agency",
         comp=f"over-the-shoulder medium shot from behind Tang Xiaotang's right shoulder: Tang Xiaotang appears only once, her shoulder and the back of her head with its two looped buns and pink silk ribbons in the left foreground, her face out of the frame; Xu Yan on screen right, framed from the waist up with clear space above his head, {XU_SWEAT}, his face three-quarter to screen left toward her, never the lens; worried: brows drawn together, eyes narrowed, lips firm between words; nobody else behind him",
         lines=[("xuyan", "別高興太早。太陽偏西了，錢府還有十里。", "皺眉")],
         motion=f"Xu Yan takes the small money pouch from her hand and tucks it into the front of his robe beside the bulge of the big bag already there, then lifts his eyes to the low sun off screen left and his brows knit; Tang Xiaotang's lips stay closed; {NOSMILE}",
         zh="過肩（唐小棠右肩後拍許硯）、慢推：前景左唐小棠的肩與丸子頭（只出現一次），許硯在畫右從她手上接過錢袋塞進懷裡（懷裡已有大錢袋），抬頭看畫左的太陽，眉頭皺起；她嘴閉著"),
    dict(loc="agency_m", cam="Medium shot, tracking", chars=["qinshuang", "zongbiaotou"], nospeak=["zongbiaotou"], night="agency",
         comp=f"medium shot, framed from the waist up with space above the heads: on screen left Qin Shuang, {QIN}, {EMPTY}, her face three-quarter to screen right toward the escort chief, never the lens; level and steady: brows level, eyes on him, lips closed; from screen right {ZONG}, seen only from behind, his face never seen, leading {HORSE}; far behind, soft, two escort men at the well; nobody else",
         lines=[("zongbiaotou", "騎我的馬去！明天把馬牽回來就行。", "豪爽，背影")],
         motion=f"the escort chief leads the horse up to Qin Shuang and tosses the reins to her; Qin Shuang's lips stay closed; {NOSMILE}",
         zh="中景、跟拍：宗鏢頭的背影牽著棗紅馬（一匹、配鞍）從畫右走到秦霜面前，把韁繩往她一拋；背對說話（nospeak，剪接放錄音）；秦霜兩手空、嘴閉著"),
    dict(loc="agency_m", cam="Low-angle medium shot, slow push in", chars=["qinshuang", "xuyan", "tangxiaotang"], night="agency",
         comp=f"low-angle medium shot of Qin Shuang beside {HORSE}, framed with clear space above her head, {QIN}, {REINS}, her face three-quarter to screen left toward the two below her, never the lens; cool and dry: brows level, eyes narrowed, lips firm between words; at the bottom left edge only the shoulders and the backs of the heads of Xu Yan in his blue-grey robe and Tang Xiaotang with her two looped buns, their faces out of the frame; {ONCE}",
         lines=[("qinshuang", "上來，抓緊。掉下去我可不回頭撿。", "冷，乾脆")],
         motion=f"Qin Shuang catches the reins in her right hand, sets her left foot in the stirrup and swings up into the saddle, sits square, and reaches her right hand back down to the two at the bottom left, her whole head staying in the frame; {NOSMILE}",
         zh="低角度中景、慢推：秦霜右手接住韁繩，左腳踩鐙翻身上馬，坐穩回頭朝畫左下的兩人伸出右手；畫左下緣只露許硯、唐小棠的肩與後腦（臉不入鏡）。live：手上只有韁繩、沒有刀"),
    # ---- the road: one horse, three riders, running right to left toward the sun.
    dict(chapter="趕路", loc="road", cam="Wide shot, tracking", chars=["qinshuang", "tangxiaotang", "xuyan"], night="road",
         comp=f"wide side shot past rice stalks whipping by in the foreground: {HORSE} galloping toward screen left with three riders on it, everyone small in the frame: in front Qin Shuang, {QIN}, {REINS}, her face in profile ahead toward screen left, never the lens; cool: brows level, eyes narrowed ahead; in the middle Tang Xiaotang {TANG_RODE}, clutching her buns with her left hand, mouth wide open in a scream; behind her Xu Yan, {XU_DUST}, his left arm clutching the money bags at his chest and his right hand gripping the back edge of the saddle; {ONCE}",
         lines=[("tangxiaotang", "慢點！我的髮髻要散了，簪子也要掉了！", "被顛得尖叫"),
                ("qinshuang", "慢了就趕不上日落，髮髻散了回家再梳。", "頭也不回")],
         motion="the horse gallops toward screen left kicking up dust; Tang Xiaotang bounces in the saddle, pressing her buns down with her left hand; Qin Shuang keeps her eyes ahead and does not turn; Xu Yan hangs on behind",
         zh="全景、側面跟拍、前景稻穗掠過（長鏡）：一匹棗紅馬、三人在馬上往畫左快跑：秦霜在前抓韁、唐小棠在中間左手按住歪掉的髮髻尖叫、許硯在後左手抱懷裡錢袋右手抓馬鞍後緣、衣服沾塵；秦霜頭也不回答。live：秦霜手上只有韁繩"),
    dict(loc="road", cam="Point-of-view tracking shot", chars=["qinshuang", "tangxiaotang"], night="road",
         comp=f"point-of-view shot from the back of the galloping horse, looking ahead past two Song-dynasty riders seen only from behind: in the near foreground the back of Tang Xiaotang's head with its two looped buns knocked askew and one pearl pin slanting, beyond her the back of Qin Shuang's high ponytail and her shoulders; their faces never seen; far ahead the red sun sinking toward the mountain ridge",
         lines=[("xitong", "距日落，一刻鐘。", "冷，報時")],
         panel=[("距日落：一刻鐘", "panel")],
         motion="the horse's back bobs up and down; far ahead the red sun sinks a little lower toward the ridge; no face is seen",
         zh="主觀（許硯越過兩人肩頭看前方）、跟拍：前景唐小棠歪掉的丸子頭與秦霜的馬尾（背影）；遠處紅太陽一點一點往山脊沉；系統報時（面板，結尾）"),
    # ---- scene 3: the Qian manor gate at sunset. Axis: the gate up the steps on screen right, the sun in the west on the left.
    dict(chapter="錢府", loc="gate", cam="Low-angle wide shot, slow push in", chars=["menfang"], nospeak=["menfang"], night="gate",
         comp=f"low-angle wide shot past the stone back of one stone lion in the foreground: at the top of the steps {GATEKEEPER}, the top edge of the frame cutting him off at the shoulders so his face is never seen, his hands tucked into his sleeves; two {SERVANTS} pushing the two leaves of the vermilion gate shut; at the foot of the steps {HORSE}, just pulled up, with three Song-dynasty riders on it, dark silhouettes seen from behind against the red light",
         lines=[("menfang", "時辰到了，申時已過，老爺不見客！", "拖長音")],
         motion="the two servants push the gate until only a narrow crack is left; the gatekeeper steps forward into the crack and tucks his hands deeper into his sleeves; the three riders sit still on the horse",
         zh="低角度全景、慢推、前景石獅子的背：台階頂門房（畫面上緣切在肩膀，臉不入鏡、雙手揣袖），兩個家丁（黑短打）推門只剩一條縫；台階下棗紅馬剛停、三人在馬上（逆光剪影，不點名、不送參考圖）。門房 nospeak（剪接放錄音）"),
    dict(loc="gate_c", cam="Medium close-up, tracking", chars=["xuyan", "qinshuang", "tangxiaotang"], night="gate",
         comp=f"medium close-up of Xu Yan on the stone steps, framed from the waist up with clear space above his head, {XU_DUST}, his face three-quarter to screen right toward the gatekeeper at the top of the steps off screen right, never the lens; urgent and dogged: brows drawn down, eyes fixed, mouth working between hard breaths; behind him at the foot of the steps, soft and out of focus, Qin Shuang helping Tang Xiaotang down from the horse and looping the reins round a stone lion; {ONCE}",
         lines=[("xuyan", "太陽還沒落。字據寫的是日落，不是申時。", "喘，一字一字")],
         motion=f"Xu Yan comes up three steps in long strides, turns half round still breathing hard and flings his right arm out toward the sun off screen left, then turns his face back to the gatekeeper; behind him the two women's lips stay closed; {NOSMILE}",
         zh="中近景、跟拍（長鏡）：許硯（衣服沾塵、喘）三步跨上台階，半轉身右手往畫左（西邊）一指；背景虛焦秦霜扶唐小棠下馬、把韁繩繞上石獅子。live：稿子從翻身下馬開始，剪接切在動作中間，這鏡從上台階開始"),
    dict(loc="gate", cam="Over-the-shoulder shot, slow tilt up", chars=["xuyan"], night="gate",
         comp="over-the-shoulder shot from behind Xu Yan: his blue-grey shoulder, the back of his topknot and his raised right arm in its dusty blue-grey sleeve in the foreground, his face out of the frame; along his arm, far away to the west, the mountain ridge with half a red sun still above it; nobody else",
         lines=[("menfang", "我說過了就是過了，你們回吧！", "畫外，不耐煩")],
         motion="the view travels up along his raised arm to the far ridge, where half a red sun still hangs; a flock of birds crosses the sky; his face never turns",
         zh="過肩（許硯背後）、慢搖上：沿著許硯舉起的手臂往上，遠山還掛著半個紅太陽，一群鳥飛過；許硯背對、嘴不入鏡；門房畫外"),
    # Converted: Tang Xiaotang's speaking close-up (script c24) from behind her; the copy's blank back toward the lens.
    dict(loc="gate_c", cam="Low-angle over-the-shoulder medium shot, slow push in", chars=["tangxiaotang", "menfang"], nospeak=["tangxiaotang", "menfang"], night="gate",
         comp=f"low-angle over-the-shoulder medium shot from just behind and below Tang Xiaotang's left shoulder on the steps: {behind(side='left', to='the gatekeeper', extra=' knocked a little askew, one pearl pin slanting')}; in her raised right hand beside her head one unfolded slip of pale yellow paper held up toward the gatekeeper, its blank back toward the lens, soft and out of focus, nothing on it readable; above her at the top of the steps on screen right {GATEKEEPER}, the top edge of the frame cutting him off at the shoulders, his face never seen, standing in the narrow crack of the vermilion gate; nobody else",
         lines=[("tangxiaotang", "這是抄本，原本在你家老爺手上，寫的是日落。", "甜，但寸步不讓")],
         motion="Tang Xiaotang draws the folded slip out of her right sleeve, snaps it open and holds it up high toward the gatekeeper, her face still turned away up toward him; the gatekeeper's hands stay tucked in his sleeves",
         zh="【改背後拍】低角度過肩、慢推：從唐小棠左肩後下方往上拍，她只出現一次（前景只有歪掉的丸子頭、斜的珍珠簪與肩），臉朝門房、嘴不入鏡；她從右袖抽出 c08b 收的字據抄本，啪地攤開舉高對著門房，紙背朝鏡頭、虛焦、看不到字；門房在台階頂（畫面上緣切在肩）。台詞 nospeak，剪接放錄音。稿子是下巴以上近景、她講話"),
    # The first of the four shots that use the blade (the script: c25 she draws it).
    dict(loc="gate_c", cam="Low-angle medium shot, slow push in", chars=["qinshuang", "menfang"], nospeak=["menfang"], night="gate",
         comp=f"low-angle medium shot up the steps: {GATEKEEPER}, seen only from behind, his face never seen, blocking the narrow crack of the vermilion gate; behind him Qin Shuang, {QIN}, coming up the last step, framed with clear space above her head, her face three-quarter to screen right toward his back, never the lens; cold: brows low and level, eyes narrowed on him, lips closed; nobody else",
         lines=[("menfang", "抄本算什麼？門關了，就是關了！", "背影，拖長音")],
         motion=f"the gatekeeper steps sideways to fill the crack; Qin Shuang stops on the top step right behind him, draws {MACHETE} from the right side of her wide leather belt with her right hand and lets it hang blade-down at her side, the edge turned toward the ground; her lips stay closed; {NOSMILE}",
         zh="低角度中景、慢推：門房的背影跨一步擋住門縫、背對說話（nospeak）；秦霜踏上最上一階停在他身後，右手從腰帶右邊抽出柴刀、刀刃朝下垂在身側；嘴閉著。live：稿子真的用刀的第一鏡（刀照第 5 集 fix1 的寫法）"),
    dict(sid="s25b", loc="gate_c", cam="Low-angle medium shot, slow push in", chars=["qinshuang", "menfang"], nospeak=["menfang"], night="gate",
         comp=f"low-angle medium shot at the top of the steps, the whole action kept inside the frame: Qin Shuang, {QIN}, framed from the knees up with clear space above her head, {MACHETE} hanging blade-down in her right hand, the edge toward the ground, touching nobody; beside her {GATEKEEPER}, seen only from behind, his face never seen; the vermilion double gate before them; nobody else",
         lines=[("qinshuang", "讓開。我不打人，我只開門。", "冷")],
         motion=f"at normal speed Qin Shuang lifts her right foot and kicks the gate; both leaves fly inward and bang against the inner walls; the gatekeeper stumbles aside and sits down hard by the door frame; she plants her foot, looks down at him and turns her face to him; {NOSMILE}",
         zh="低角度中景、慢推、正常速度、整個動作留在畫面裡：秦霜抬右腳踹門，大門往內彈開撞牆，門房往旁邊跌坐在門邊；秦霜收腳站定，低頭看他說話（右手柴刀刀刃朝下、不碰人）"),
    # The hall. Axis: the doorway on screen left, the red-wood table and Qian Yuanwai on screen right. Four named in the
    # script (Tang Xiaotang behind Qin Shuang): she is left out here; she is back in c30.
    dict(loc="hall", cam="Wide shot, slow push in", chars=["xuyan", "qianyuanwai", "qinshuang"], night="hall",
         comp=f"wide shot past the door frame and the beam of sunset light in the foreground, everyone small in the frame: on screen left Xu Yan, {XU_DUST}, the money bags bulging in the front of his robe, striding in along the beam of light; on screen right behind the red-wood table {QIAN}, sitting, one small white porcelain teacup in his hand, his face three-quarter to screen left toward the door, never the lens; furious: brows slammed down, eyes bulging, mouth wide on each shout; in the doorway Qin Shuang, {QIN}, {MACHETE} hanging blade-down in her right hand, touching nobody, lips closed; {ONCE}; two {SERVANTS} behind the folding screen",
         lines=[("qianyuanwai", "誰讓你們進來的？來人，給我轟出去！", "拍桌")],
         motion=f"Xu Yan strides in; Qian Yuanwai puts down the teacup, plants both hands on the table and rises to his feet with space above his head, and slams his right palm on the table; the two servants rush out from behind the screen, see the blade in Qin Shuang's hand and stop dead; Xu Yan's lips stay closed",
         zh="大廳全景、慢推、前景門框與夕陽光束（長鏡）：許硯踩著光束大步走進來（懷裡鼓著錢袋）；錢員外放下白瓷小茶杯、撐桌站起、拍桌說話；屏風後衝出兩個家丁，看見門口秦霜手上的柴刀停住。live：稿子秦霜身後還有唐小棠（四個有名字的人），這鏡拿掉唐小棠（她 c30 回到門內側）"),
    dict(loc="hall_c", cam="Over-the-shoulder medium shot, slow push in", chars=["qianyuanwai", "xuyan"], night="hall",
         comp=f"over-the-shoulder medium shot from behind Qian Yuanwai's left shoulder: his dark gold silk shoulder with roundel patterns in the right foreground, his face out of the frame; Xu Yan standing at the red-wood table on screen left, framed from the waist up with clear space above his head, {XU_DUST.replace(', breathing hard', ', his breathing steadied')}, his face three-quarter to screen right toward Qian Yuanwai, never the lens; firm and level: brows level, eyes steady on him, lips firm between words; {ONCE}",
         lines=[("xuyan", "二十兩一錢，一錢不少。錢員外，請點。", "不卑不亢")],
         motion=f"Xu Yan takes {BAG} and {POUCH} from the front of his robe and sets them on the table, loosens their mouths so lumps of broken silver and a few small silver ingots slide out, and pushes the heap across to Qian Yuanwai with both hands; Qian Yuanwai's lips stay closed; {NOSMILE}",
         zh="過肩（錢員外左肩後拍許硯）、慢推：前景右錢員外深金色團花錦袍的肩；許硯從懷裡掏出一大一小兩個灰布錢袋放上桌、解開袋口，碎銀和幾錠小銀滑出來，雙手推到錢員外面前；喘已平"),
    # Qian Yuanwai may sneer here (the script).
    dict(loc="hall_c", cam="Over-the-shoulder medium shot, slow push in", chars=["qianyuanwai", "xuyan"], night="hall",
         comp=f"reverse over-the-shoulder medium shot from behind Xu Yan's right shoulder: his blue-grey shoulder and topknot in the left foreground, his face out of the frame; {QIAN}, behind the red-wood table on screen right, framed from the waist up with space above his head, the heap of broken silver on the table before him, his face three-quarter to screen left toward Xu Yan, never the lens; a cold sneer: one corner of his mouth curled, eyes narrowed; {ONCE}; behind him only the plain folding screen",
         lines=[("qianyuanwai", "過了申時，這筆不算數，地照收。", "死不認帳")],
         motion="Qian Yuanwai picks up one lump of silver between two fingers and flicks it across the tabletop so it rolls away, then sits back in his armchair; Xu Yan's lips stay closed",
         zh="反打（許硯右肩後拍錢員外）、慢推：錢員外右手拈起一塊碎銀往桌面一彈、碎銀滾開，身子往後一靠；本鏡可以冷笑"),
    dict(loc="hall_c", cam="Medium close-up, slow push in", chars=["xuyan"], night="hall",
         comp=f"medium close-up of Xu Yan at the table, framed from the waist up with clear space above his head, {XU_DUST.replace(', breathing hard', '')}, his face three-quarter to screen right toward Qian Yuanwai off screen right, never the lens; hard and quiet: brows drawn down, eyes fixed on him, lips firm between words, jaw set; behind him only the doorway and the beam of sunset light of the same hall",
         lines=[("xuyan", "字據寫日落，太陽還在天上。欠債還錢，字據拿來。", "壓低聲音")],
         motion=f"Xu Yan plants both hands on the silver-strewn table, his back straight and his whole head staying in the frame, then lifts his right hand and holds it out palm up toward Qian Yuanwai off screen right; {NOSMILE}",
         zh="中近景、慢推（中景推到中近景）：許硯兩手撐在撒滿碎銀的桌上（稿子「往前傾」改成腰桿挺直、頭留在畫面裡，不寫 leans），再伸出右手掌心向上"),
    # The blade's last shot: its back on her right shoulder, the edge outward, toward nobody.
    dict(loc="hall", cam="Point-of-view shot, slow push in", chars=["qinshuang", "tangxiaotang"], night="hall",
         comp=f"point-of-view shot from the table looking back at the doorway: in the doorway Qin Shuang, {QIN}, framed from the knees up with clear space above her head, {MACHETE} in her right hand, her face three-quarter to screen right toward Xu Yan at the table, never the lens; cold: brows level, eyes narrowed, lips firm between words; just inside the door behind her Tang Xiaotang {TANG_RODE}, {ABACUS} in her hands, her face toward the table, lips closed; outside the door about six {NEIGHBOURS} craning their heads in to look; far beyond them a sliver of the red sun above the ridge; {ONCE}",
         lines=[("qinshuang", "門外半條街的人都看見了，太陽還沒落。", "冷"),
                ("xitong", "叮。秦霜，好感加五。", "冷淡，報數")],
         panel=[("秦霜 好感 +5 → 10", "panel")],
         motion=f"Qin Shuang steps aside to clear the doorway and rests the back of the machete on her right shoulder, the edge turned outward and away from everyone; when her line ends her lips close and stay closed, her eyes easing a little; the townsfolk crane in and glance at one another, their lips closed; Tang Xiaotang's lips stay closed; {NOSMILE}",
         zh="主觀（許硯回頭看門口）、慢推（長鏡）：秦霜側身讓開門口、把柴刀刀背靠上右肩（刀刃朝外、不朝人）說話，說完嘴閉著、眼神鬆一點（不笑）；門內側唐小棠（髮髻歪）抱算盤、嘴閉著；門外約六個街坊（宋式粗布短打）探頭；遠山一角紅太陽；系統（面板）。注意：同鏡有露嘴台詞又有系統聲，模型可能把空檔講滿，剪接時系統句放在她閉嘴之後"),
    dict(loc="hall_c", cam="Insert close-up, slow push in", chars=[], night="hall",
         comp=f"insert close-up, the shot opens directly on the red-wood tabletop from its very first frame: one fat hand in a dark gold silk cuff with roundel patterns, of an ordinary skin tone, holding one sheet of paper face down, its blank back up, only a faint red thumbprint showing through the paper, nothing readable; {SILVER} scattered on the table; one man's hand in a dusty blue-grey cuff at the left edge; only the hands, cuffs, paper, silver and tabletop are in the frame, no face; behind them only the beam of sunset light of the same hall",
         lines=[("xitong", "負債清零。", "冷，前面停一拍")],
         panel=[("負債清零", "panel")],
         motion="the fat hand pauses, then slaps the paper face down on the table; the blue-grey hand picks it up and tears it in two, then again, and the blank backs of the pieces drift down through the beam of light; last the blue-grey hand pushes one small lump of silver back out of the heap and draws it out of the frame",
         zh="手部特寫、慢推（第一格就是桌面）：錢員外的胖手（深金色團花錦袍袖口、一般膚色）頓一下，把字據（紙背朝上，只透出紅手印）摔在桌上；許硯的手拿起來撕兩次，紙片空白背面在光束裡飄下；最後他從碎銀裡撥回一小塊（一錢）收出畫；系統（面板）"),
    dict(loc="hall_c", cam="Close-up, slow push in", chars=["qianyuanwai"], night="hall",
         comp=f"close-up of {QIAN}, framed from the chest up with space above his head, his face three-quarter to screen left toward Xu Yan off screen left, never the lens; red with fury: face flushed dark red, brows slammed down, eyes bulging, teeth clenched between words; behind him only the plain folding screen of the same hall",
         lines=[("qianyuanwai", "許硯，你今天走得出去，明天走不出柳溪！", "咬牙"),
                ("xuyan", "債清了，柳溪的路，我天天走給你看。", "畫外，平靜")],
         motion="Qian Yuanwai pounds his fist down on the table below the frame and the silver jumps; when his line ends his lips stay pressed shut and he glares toward screen left, his chest heaving",
         zh="近景、慢推（長鏡）：錢員外臉漲紅一拳捶桌、碎銀跳起，說話；許硯畫外回話時錢員外嘴閉著、瞪著畫左。注意：同鏡露嘴台詞後接畫外台詞，模型可能讓他繼續講，剪接時許硯那句放在他閉嘴之後"),
    # The outer wall at dusk. Axis: they walk toward screen left (the village road).
    dict(loc="wall", cam="Wide shot, tracking", chars=["qinshuang", "tangxiaotang", "xuyan"], night="wall",
         comp=f"wide shot past one plain lit lantern with no writing in the foreground, everyone small in the frame: Qin Shuang, {QIN}, {REINS}, leading {HORSE} in front; Tang Xiaotang {TANG_RODE}, walking beside Xu Yan, her face in profile toward him, never the lens; warm and pleased: eyes bright, cheeks lifting, a small smile between words; Xu Yan, {XU_TIRED}, walking a little behind, lips closed; {ONCE}",
         lines=[("tangxiaotang", "走吧相公，今晚回家，我給你記一大功。", "輕快，可以笑")],
         motion="the three walk along the wall toward screen left; Tang Xiaotang pats Xu Yan's sleeve twice as she speaks; Xu Yan nods once, his lips closed",
         zh="全景、跟拍、前景剛點上的燈籠（空白）：秦霜牽馬在前、唐小棠走在許硯旁拍拍他的袖子說話（本鏡可以笑）、許硯點一下頭。live：稿子寫「柴刀已插回腰帶右邊」，這鏡不提刀（兩手只牽韁繩、畫面裡沒有兵器）"),
    dict(loc="wall_c", cam="Insert close-up, slow push in", chars=[], night="wall",
         comp=f"insert close-up, the shot opens directly on the old straw hat from its very first frame: {HAT}, hanging on one wooden post beside the small side door in the whitewashed wall; nobody in the frame; behind it only the white wall in the dusk light",
         lines=[("xuyan", "這頂紅繩草帽……跟河邊那頂一樣。", "畫外，低聲")],
         motion="the red cord stirs in the evening breeze and the straw hat turns slowly half round on its post",
         zh="插鏡、慢推（第一格就是草帽）：側門旁木樁上一頂舊草帽（麥稈色、帽簷破一角、細紅繩，照第 1 集 c11 那頂），紅繩在晚風裡晃、草帽轉半圈；許硯畫外"),
    dict(loc="wall_c", cam="Over-the-shoulder medium shot, slow push in", chars=["qinshuang", "xuyan"], nospeak=["xuyan"], night="wall",
         comp=f"over-the-shoulder medium shot from behind Xu Yan's right shoulder: his blue-grey shoulder and topknot in the left foreground, his face out of the frame; Qin Shuang on screen right leading {HORSE}, framed from the chest up with space above her head so her belt stays below the bottom edge of the frame, {QIN}, her hands holding only the reins, no blade, no knife, no scabbard and no weapon anywhere in the frame, her face three-quarter to screen left toward him, never the lens; puzzled and cool: one brow slightly raised, eyes steady on him, lips firm between words; {ONCE}; behind her only the white wall in the dusk light",
         lines=[("qinshuang", "草帽滿街都是，你看它做什麼？", "淡淡"),
                ("xuyan", "沒什麼。我落水那晚，河邊也掛著一頂。", "背對鏡頭，低聲")],
         motion=f"Qin Shuang stops and looks back, glances past him toward the straw hat on its post off screen left, then her eyes come back to him; after her line her lips close and stay closed while she watches him; Xu Yan stays turned away; {NOSMILE}",
         zh="過肩（許硯右肩後拍秦霜）、慢推（長鏡）：秦霜停步回頭，看草帽一眼再看他說話；許硯背對回話（nospeak，剪接放錄音），她嘴閉著看他。live：胸口以上、腰帶在畫面下緣外、沒有刀"),
    dict(loc="wall_c", cam="Extreme close-up, slow push in", chars=["xuyan"], night="wall",
         comp=f"{EYES}; his eyes suddenly fixed and still",
         lines=[("xitong", "叮。隱藏任務：洞房花燭。", "冷，宣布")],
         panel=[("隱藏任務：洞房花燭", "task")],
         motion="his eyes, about to turn away, freeze and widen slightly; nothing else moves",
         zh="眼睛大特寫、慢推（第一格就是眼睛）：許硯正要轉身，眼睛猛地一定；系統（面板）。live：稿子的「瞳孔映淡藍光」不寫（真人版畫成發光藍瞳，preflight ERROR），改第 7 集 EYES"),
    dict(loc="wall_c", cam="Point-of-view medium shot, slow push in", chars=["tangxiaotang", "qinshuang"], night="wall",
         comp=f"point-of-view medium shot of the two women in the lantern light, both framed from the waist up with space above their heads: Tang Xiaotang {TANG_RODE}; Qin Shuang, {QIN}, {REINS}, holding the horse beside her; both faces three-quarter toward Xu Yan just off screen, never the lens; Tang Xiaotang curious: head tilted, brows lifted, eyes wide, lips closed; Qin Shuang wary: one brow raised, eyes narrowed, lips closed; {ONCE}; behind them only the white wall and the lit lanterns",
         lines=[("xitong", "今夜，任一妻好感加十。", "冷，宣布")],
         panel=[("今夜 任一妻 好感 +10", "task")],
         motion=f"both turn their heads back toward Xu Yan off screen at the same moment; Tang Xiaotang tilts her head, Qin Shuang lifts one brow; all lips stay closed; {NOSMILE}",
         zh="主觀（許硯看兩人）、慢推：唐小棠（髮髻歪）、秦霜（牽馬）同時回頭；唐小棠歪頭、秦霜挑一邊眉；嘴都閉著；系統（面板）"),
    dict(loc="wall_c", cam="Close-up, slow push in", chars=["xuyan"], night="wall",
         comp=f"close-up of Xu Yan framed from the chest up with space above his head, {XU_TIRED}, his face three-quarter to screen left, never the lens; shaken: face gone pale, brows drawn up in the middle, eyes wide and fixed, lips pressed shut the whole shot; his right hand gripping the back edge of a saddle at the bottom edge of the frame; behind him only the white wall in the dusk light",
         lines=[("xitong", "失敗，扣除種田技能。", "冷，宣布"),
                ("xuyan", "種田也扣？我就剩這一樣本事了。", "心裡話，嘴閉著，慌", "inner")],
         panel=[("失敗：扣除種田技能", "penalty")],
         motion=f"his hand jerks and then clamps hard on the saddle edge, his knuckles whitening; his head stays still; his lips stay closed; {NOSMILE}",
         zh="近景、慢推（長鏡）：許硯臉色一白，手一抖抓緊身旁馬鞍後緣；嘴閉著（心裡話）；系統（面板）。live：稿子的「喉結滾一下」改成指節發白（單人近景的吞嚥會變成閉嘴微笑，第 4 集 fix1）"),
    dict(loc="wall", cam="Medium shot, tracking", chars=["qinshuang", "tangxiaotang", "xuyan"], night="wall",
         comp=f"medium shot by the wall in the lantern light, framed with clear space above the heads: on {HORSE}, Qin Shuang in front, {QIN}, {REINS}, and Tang Xiaotang {TANG_RODE} behind her, both already mounted, faces in profile toward screen left, lips closed; beside the horse Xu Yan, {XU_TIRED}, his face three-quarter to screen left, never the lens; weary and resigned: brows drawn together, eyes lowered, lips closed; {ONCE}",
         lines=[("xitong", "所以才扣這一樣。宿主，天黑了。", "冷，嫌棄，句尾往下壓"),
                ("xuyan", "好，回家。今晚總得進一扇門。", "心裡話，嘴閉著，認命", "inner")],
         motion=f"Xu Yan wipes the sweat from his temple with his sleeve and swings up onto the horse's back behind Tang Xiaotang, his whole head staying in the frame; Qin Shuang shakes the reins and the horse walks off toward screen left; all lips stay closed; {NOSMILE}",
         zh="中景、跟拍（長鏡）：秦霜在前抓韁、唐小棠在中間（都已上馬）；許硯抬袖擦太陽穴的汗、翻身上後座；秦霜一抖韁繩，馬往畫左走；嘴都閉著（系統與心裡話）"),
    dict(loc="night", cam="Extreme wide shot, slow push in", chars=["aling"], night="night",
         comp="extreme wide shot past the Xu farmhouse's bamboo fence in the foreground at night, small in the frame: A-ling in her grey-white cotton dress, one plain wooden hairpin, no shackles, her sleeves pulled down over her wrists, sitting on the threshold of the yard gate under the plain lantern; nobody else",
         lines=[],
         act=3,
         motion="A-ling rises from the threshold, takes one step forward and looks toward the dark village road off screen left; her lips stay closed",
         zh="遠景、慢推、前景許家竹籬笆：夜，許家院門口一盞燈籠（空白）；阿令（灰白布裙、木簪、沒戴鐵鐐）從門檻上站起來，往前走一步，望向畫左的村路；嘴閉著（無台詞；第 9 集 c01 接這裡）"),
]

HEAD = [
    "- 重製版 r2、真人版（站主 2026-11-11「之後都用真人版」）：照 `docs/videos/zhong-tian-qu-qi-e008-r2/script.md`（c01–c08、c08b、c09–c25、c25b、c26–c40 對應 s01–s08、s08b、s09–s25、s25b、s26–s40；含「這版改了什麼」與「2026-11-06 審稿後的修改」：c13、c14、c17、c24 用改過的台詞）；每鏡一個看得見的動作、對話用過肩與反打、一句一筆不拆半句、預設不笑。",
    "- 內部工作編號 908（`hailuo/*-dh-e908.json`、`colab/runs/e908/`、`colab/runs/e908-live/`）；發布 slug `zhong-tian-qu-qi-e008-r2`。不放集數、不放片名卡；s01 接第 7 集 s37 的下一刻（許硯站在桌後、孫掌櫃站在桌前畫右、銀錠在桌上）。",
    "- 真人版的寫法一開始就寫進來（第 5–7 集真人版的教訓）：秦霜只有 s25（拔刀）、s25b、s26（刀刃朝下拿著）、s30（刀背靠肩）有刀，其他鏡一律「兩手空著（或只拿韁繩）、畫面裡沒有任何刀、鞘、兵器」；白皂一律「扁方、掌心大、一指厚、像小磁磚」，木箱與竹筐加「沒有圓條、圓柱、圓饅頭」；算盤「不比她的手長」。",
    "- 唐小棠：冷臉講話的近景改成從她背後拍、嘴不入鏡、台詞 nospeak（s07、s11、s24，剪接放錄音）；不講話的鏡在 `e908-live/spec.json` 換中性外貌句；s15、s33 稿子允許笑。構圖裡不寫 camera 這個字（第 7 集 s08、s20 畫出攝影機）。",
    "- 一鏡最多三個有名字的人：s26 拿掉唐小棠（稿子四人）；宗鏢頭、門房沒有參考圖，只拍背影或肩以下，台詞 nospeak 或畫外；鏢師、家丁、街坊、丫鬟寫宋式衣著。",
    "- 沒有字：門匾、燈籠、錢箱、算盤、銀錠都空白；字據抄本摺著或紙背朝鏡頭、虛焦；s31 字據紙背朝上。系統面板用 overlays（s03、s20、s30、s31、s36、s37、s38）。s36 眼睛大特寫用第 7 集的 EYES（深棕虹膜、一點眼神光），不寫淡藍光。",
    "- 長鏡要買的秒數（BUY）：見 `r2.py` 的 BUY 註解；還沒錄音，照稿子長鏡清單與台詞字數估。",
]
FOOT = [
    "- **沒有真人參考圖、pilot.py 會停的**：鏢局 `set-biaoju`（s10–s18）、錢府大門與外牆 `set-qianfu-men`（s21–s25b、s33–s39）、錢府大廳 `set-qianfu-ting`（s26–s32）——`refs-dh/` 有第一季的 CG 場景圖，`refs-live/` 沒有真人版；要站主決定畫真人版場景圖，或改成不送場景圖（只用文字）。土路（s19、s20）沒有場景圖、只用文字。",
    "- 宗鏢頭、門房沒有定妝照（CG 也沒有），本集只拍背影、肩以下或手，不需要；若剪接要正臉，開拍前補 `zongbiaotou-portrait-l1`、`menfang-portrait-l1`。兩人的聲音不在 `cast.json`，`r2.py` 的 MINOR 先填了提案（宗鏢頭 Alnilam、門房 Schedar），站主選定後記進 `cast.json`。",
    "- 有真人定妝照：許硯、唐小棠、秦霜、阿令（含角度圖）、孫掌櫃、錢員外（錢員外有角度圖，孫掌櫃沒有）；後巷 `set-chouduan-l1`、許家院子 `set-xujia-yuan-l2`。",
    "- 秦霜的 `cast.json` 造型寫著「柴刀插在腰帶」：`extras.json` 與 `pilot.py` 都把這句從造型句拿掉，刀只在 s25、s25b、s26、s30 由構圖寫。",
    "- 配樂：後巷 tension 輕版（s03 叮抽一拍、s07 轉輕快）、鏢局 comedy（s15 上揚重音）、土路急鼓、錢府 tension（s31 撕字據重音）、外牆 suspense（s39 只留風）；音效表見 script.md〈音樂與音效〉。",
]

# Long shots: seconds to buy. script.md 長鏡清單: c08, c09, c10, c13, c19, c22, c26, c30, c32, c35, c38, c39 at 8 and c11
# at 10. Not in the list: by e007's estimate (zh characters with punctuation stripped / 3.7 + 0.5 s, against buy - 0.3 s
# at the cut's 1.1x), s01 (16 chars, 4.8 s + the push) and s05 (18 chars, 5.4 s + the walk), s16 (17 chars + the pouch)
# and s07 (17 chars, a recorded line after the escort walks past) get 8; s24 (19 chars, recorded, after she unfolds the
# paper) gets 8. The live drafts speak with the model's own voice, which pauses mid-line (route-a.md 2026-11-07), so
# these are a floor; re-check against the recorded or drafted voice before stage 1.
BUY = {"s01": 8, "s05": 8, "s07": 8, "s08": 8, "s09": 8, "s10": 8, "s11": 10, "s13": 8, "s16": 8, "s19": 8, "s22": 8,
       "s24": 8, "s26": 8, "s30": 8, "s32": 8, "s35": 8, "s38": 8, "s39": 8}
