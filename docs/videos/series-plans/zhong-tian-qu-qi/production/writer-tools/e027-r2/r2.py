"""Episode 27 remake (r2): the writer spec for ../e001-r2/build-r2.py. Source: docs/videos/zhong-tian-qu-qi-e027-r2/script.md
(c01-c37 = s01-s37; the CG-era r2 script), including its sections 「這版改了什麼」, 「2026-11-06 審稿後的修改」 and
「真人版的改動（2026-11-17）」, which override the tables. Every line is the script's, word for word; only the staging changes.
Bible: production/r2-bible-e021-e030.md (rules 1-30, the 26->27 and 27->28 hand-overs, the props, people and picture tables).
The seventh episode of arc 3 〈搶親〉: the Xu shop front on the twenty-seventh morning (the same moment as e026 s40), the county
court hall near noon, the lane behind the silk shop and the stone bridge that night.

Written from the start the way e026-r2/r2.py stands AFTER its independent review (../e026-r2/review.md: the nine 必改 and the
cheap 建議), with what the pickers caught in e923-e925 (colab/runs/e92{3,4,5}-live/{review-picks-a,review-picks-b,picks-merged}.tsv)
and the newest lessons in the task file (e925: never "toward the young woman off screen"):
- OFFSCREEN_SPEECH = False (rule 15): every shot with an off-screen line, a thought or a system line writes the silence of each
  person on screen (quiet(), SILENT_HE, SILENT_SHE). Where a back-view, foreground or off-screen character speaks, every face
  toward the camera "says nothing ... lips pressed together ... listens"; no word that invites a smile or talk on a listener.
- A line said to someone outside the frame is written "toward someone out of sight beyond the left/right edge of the frame",
  that side of the frame is written as set only, all the way to the edge, and the speaker as the only person in the frame
  (s12: Xu Yan to Tang Xiaotang). The young woman is never named or placed off screen in any prompt or refine text.
- Tang Xiaotang never speaks on camera and never shows her face (rule 3; e024-e026): her one line (s05) is from behind, in the
  middle of the frame, "facing straight away from us", head still, exactly two round buns (TBACK; nospeak; spec drops her
  pictures and identity sentence). The script's c13 (her walking into the silk shop) is left out of the wide: s12's line says
  where she goes. The script's 高立領 and 「下巴以上」 are CG wording and are not used (rule 4).
- A-ling wears the veil in every shot (rule 21; e027 is the first episode with it): aling-veil-portrait-l1 is sent in place of
  her portrait (spec swap_pictures), her angle pictures are dropped (they have no veil), and the veil sentence is written every
  time ("falling to just below her jaw": the word for hanging is not used). Her lines are recordings: s11 from behind in the
  foreground (unnamed, rule 2), s32 a thought, s37 nospeak under the veil. Her dagger is written only in s37 (rule 22), drawn in
  its plain wooden sheath (script: 連木鞘抽出，沒出鞘); every other shot of her writes her right sleeve falling over her hand.
- The yamen men and Zhao Butou (rules 16, 17): no word for their office anywhere ("Constable Zhao" from build-r2's speaking
  clause and cast.json's constable's hat are replaced by extras.json, the refine text by live_clips() below); Zhao Butou is
  "a soft black futou cap and a plain black round-collared cotton robe, a plain black cloth sash tied at his waist, nothing else
  at his waist", the roll of blank white strips in his RIGHT hand (bible 人物表). Only two yamen men appear, small, from behind,
  carrying the plank (s03); the four of the script's scene 1 and the two rows of eight with staves in the court are sounds
  (e019: the hall with nobody but the named, the 「威武」 and the staves are sounds). Hands in black sleeves do the pasting (s04),
  the gripping (s11) and the handing over (s22).
- Magistrate Hu always wears the winged hat (HU, e018-e019's sentence; cast.json's "official gauze hat" is replaced by
  extras.json with the same words). He is only ever on the dais crop (set-xianya-gongtang-dais-l1) and Xu Yan on the floor
  crop (set-xianya-gongtang-floor-l1): the full hall picture has a framed board hung over the dais (it would grow characters).
  s14 and s17 put an unnamed back of a young scholar in the foreground (rule 2). The gavel is GAVEL, a flat oblong block.
- Sun Zhanggui (sunzhanggui-portrait-l1: long narrow face, grey-streaked beard, green satin robe, jade belt hook) is only in
  scene 3, Magistrate Hu only in scene 2 (bible 同框撞臉). His paper lantern (bible prop) is a hand torch: a lantern grows marks
  and the word is one of the hung-object words (e921 s37, e924, e925 必改 5); he carries "one short burning pine torch held upright
  in his left hand, the only flame in the frame". The script's 「用燈籠桿點一點銀子」 is a tip of the chin toward the silver.
- Wei Shaoqing (s06 only; rule 30): the fan closed, tapped twice on Xu Yan's shoulder; this is the one shot where the script lets
  him smile (「本鏡可以笑」: a thin lazy mocking smile). s07 has his back in the foreground, unnamed.
- Name only what should be drawn (rules 7, 17, 27): the seal strips are "two long strips of plain blank white paper" (never the
  word for a seal), the roll of them "one roll of long plain blank white paper strips"; the ledger is STACK; the doctor's slip
  "one small slip of plain paper folded shut, its blank outside toward us"; the wrapping paper YPAPER; the silver "a small silver
  ingot, its top smooth and plain" (the 魏記 mark is the line's). No word "open" anywhere (e924 fix1, e926 必改 1). No moon by
  name (the pictures carry it): "cold blue moonlight".
- Counts written everywhere (rule 25): onlookers (two shoulders in s01, four in s13), the two bearers (s03), the two men with
  sticks (s37); "exactly N people" in every shot with more than one.
- One visible action per shot, props and contacts in the first frame (e923-e926 picks): s02 the look up (already crouched, two
  fingers on the wrist); s03 the wave (the plank already moving); s04 the smoothing (the strips already crossed); s05 the box
  lifted; s06 the two taps; s07 the brush-off; s09 the rub; s15 the straightening (already bowed); s16 the toss; s20 the palm
  held out; s22 the drop; s23 the fold (the script's tuck into the sleeve goes to the cut); s27 the torch raised; s29 the
  setting down (the drop of water and the broken reflection are left out); s31 the tuck (the bite left out); s34 the toss and
  catch (the stop goes to s35/s36); s35 the slide; s37 the draw (the men already blocking; the slaps of the sticks are sounds).
  The script's follows (c01, c13, c25, c34), its track (c14), its truck (c26) and its pan (c37) are slow push-ins or static.

THE AXES (rule 29: the set picture decides):
- The shop front (set-xianjie-l1 and e024's crops): the Xu shop on the LEFT, the street running away from us, the Wei shop with
  the red silk across the street on the RIGHT (26->27: the man in grey lies on the paving a little right of the middle, Xu Yan at
  the doorway). People at the Xu shop look screen right; Zhao Butou, who came across the street, looks screen left at the man
  on the ground and at Xu Yan. The shots looking across the street send set-xianjie-weiji-l1 (s01, s03, s05), the shop front
  set-xianjie-xuji-l1 (s02, s04: the doors before and as they are closed), the paving and counter with the street behind
  set-xianjie-shi-l1 (s06-s12: after the sealing, so the picture's folded-back doors stay soft and partly out of the frame).
  The yamen lies down the street (s13: the two men walk away from us into the depth).
- The court hall (set-xianya-gongtang-l1's crops, as e018/e019): Magistrate Hu behind the desk on the dais, facing screen left
  toward the floor; Xu Yan on the floor facing screen right and up toward the dais. The script's sunlit doorway on the left is
  not in either picture: the light is clear cold daylight from the tall lattice windows.
- The lane behind the silk shop by night (bible: the lane picture set-chouduan-ye-l1; the Xu shop is next door to the silk shop):
  the new free set-chouduan-ye-xiang-l1 (cropped below the big blank board at the top left, the small blank board over a
  doorway painted out). The lane runs straight away from us; the road out of town is behind the camera. Lai San comes up the
  lane toward us (s25, s34); A-ling follows along the dark LEFT wall (s26); the two men step out across the lane on the RIGHT
  (s37). The script's whitewashed wall with its lantern on the right is not in the picture: the two shadows fall on the
  moonlit paving (s35), and Lai San calls toward the dark doorways on the right (s36).
- The stone bridge by night (set-shiqiao-ye-l1 and three new free crops): the humped arch over the dark water, the bare muddy
  bank with round stones on the LEFT. Lai San on the bank at the foot of the arch on the left faces screen right; Sun Zhanggui
  a little right of him in the shadow of the arch faces screen left; A-ling crouches on top of the bridge behind its parapet
  (s32, set-shiqiao-ye-qiao-l1, the night sky behind her); the close shots under the arch send set-shiqiao-ye-dong-l1; the
  hand-over above the water sends set-shiqiao-ye-shui-l1.

PLACES (the coordinator's decisions, 2026-11-17; every picture looked at full size; script.md 〈真人版的改動〉): gen-dh's SET
phrases give set-shiji (market street), set-xianya (county yamen), set-chouduan (silk shop) and set-shiqiao (stone bridge);
spec.json swaps each for the picture above with an absolute path. The lane prompts never say "alley" (gen-dh's back alley
line comes first and has no live picture); the street prompts never say "county yamen" or "Xu family shop".
- Inserts and shots with nobody named (s04, s09, s13, s22, s29, s35) open their motion with NOBODY.
- Shared files: no code changed (every on-screen speaker is in build-r2.py's EN; no minor role speaks). refs-live gets four new
  free pictures (new ids, own l1; rule 19) and a README paragraph.
"""
EP = 927  # internal working number; the published slug is zhong-tian-qu-qi-e027-r2
SLUG = "zhong-tian-qu-qi-e027-r2"
EP_TITLE = "封鋪，橋下的銀子（重製版 r2）"
OUTLINE_SECONDS = 192  # script.md: about 191.5 s, 37 shots (13 + 11 + 13)
TARGET_MINUTES = [3, 4]
TITLE = "封鋪，橋下的銀子｜種田娶妻打天下 第27集（重製版）"
DESCRIPTION = "灰衣客人倒在許記門口，趙捕頭撥開人群，一卷封條把許記封了。許硯先讓人把客人抬去醫館，唐小棠抱出帳本與錢箱；魏少卿晃過街來問三十日的賭還賭不賭得下去，許硯說：賭約寫的是三十日，今天才第二十七日。人群邊上，阿令看見賴三指甲縫裡的白粉：你去衙門，他我跟。公堂上醫館回話只是瀉藥，胡縣令還是照封；鬥商只剩三日，許硯只要一樣東西——包那塊糖糕的紙，黃的、粗的，許記從來只用白紙。當夜阿令跟著賴三到石橋下，看見孫掌櫃把一錠銀子交給他：少爺賞的。回程的巷子裡，兩根棍子堵住了路。《種田娶妻打天下》第 27 集（重製版）。"
THUMB = ("少爺賞的", "s30")
CHARACTERS = ["xuyan", "tangxiaotang", "aling", "laisan", "zhaobutou", "weishaoqing", "huxianling", "sunzhanggui", "xitong"]
MINOR = {}
MUSIC = "one cue per scene: tense low strings on a sunny county street, one heavy beat when paper strips are slapped on a door, one thin high note on a close-up of a hand; then a dull heavy cue of slow drums and low strings in a county court hall, one hard knock of a wooden block, one beat of silence under a cold voice, one soft high note when a scrap of paper lands in a palm; then a night suspense cue of only low tones and the sound of slow water under a stone bridge, one heavy accent when silver changes hands, one big hit before it ends; ancient Chinese rural drama, no vocals"

# Places. gen-dh SET takes the FIRST pattern in its list order that the whole prompt matches: street prompts say "market
# street" (never "Xu family shop", "county yamen", "clinic"); hall prompts say "county yamen"; lane prompts say "silk shop"
# (never "alley", "Xu family shop", "market street"); bridge prompts say "stone bridge" (never "bamboo grove", "silk shop").
TOWN = ("a narrow stone-paved street running straight away from us under a clear pale blue sky; on the left the front of the Xu "
        "shop, its tall plank doors of pale wood, a dark lattice transom above and a long low plain wooden counter along its "
        "front; on the right across the street a two-storey wooden shop front with dark lattice windows upstairs and long swags "
        "of red silk draped over a plain bare wooden beam above its wide doorway, a long low dark table before it; plain wooden "
        "shop fronts further down both sides")
WEI_FRONT = ("a two-storey wooden shop front with long swags of red silk draped over a plain bare wooden beam above its wide "
             "doorway and a long low dark table before it")
HALL = ("a floor of large grey stone tiles, thick round dark red-brown wooden pillars, tall dark wooden lattice windows along "
        "the side wall above a low white panel")
DAIS = ("at the back one long dark wooden desk with one dark wooden armchair behind it, before a wall of plain white panels; on "
        "the desk one flat oblong block of dark wood at the left and one small dark wooden rack at the right")
LANE = ("a narrow lane paved with worn stone slabs between dark blue-grey brick walls, running straight away from us; on the left "
        "a long bamboo pole with four plain cloths drying over it and two wooden tubs below, on the right a round brick well "
        "under a small thatched roof, and far down at the end of the lane one small warm light glowing on the wall above a dark "
        "wooden double door")
BRIDGE = ("an old humped stone arch bridge over slow dark water, a bare muddy bank with round stones and tufts of grass on the "
          "left, tall dark bamboo along both banks, low tiled houses on the right bank with a few warm-lit windows, thin mist "
          "lying on the water")
STREET_LIGHT = "in clear morning sunlight, the shop fronts across the street in full sun, the paving before the Xu shop in soft shade"
LOC = {
    "street": f"On the market street of the county town on a cold clear winter morning: {TOWN}; {STREET_LIGHT}",
    "street_x": f"On the market street of the county town on a cold clear winter morning, at the front of the Xu shop: its tall plank doors of pale wood folded back, a dark doorway, a dark lattice transom above, the grey stone paving before it, {STREET_LIGHT}",
    "street_xc": "On the market street of the county town on a cold clear winter morning, at the front of the Xu shop, in clear morning light",
    "street_w": f"On the market street of the county town on a cold clear winter morning, looking across the street from the Xu shop: {WEI_FRONT}, in bright morning sunlight",
    "street_t": f"On the market street of the county town on a cold clear winter morning, on the grey stone paving before the Xu shop by its long low plain wooden counter, the stone-paved street running away behind, {STREET_LIGHT}",
    "hall": f"In the court hall of the county yamen near noon on a cold clear winter day: {HALL}; clear cold daylight from the tall lattice windows",
    "hall_c": "In the court hall of the county yamen near noon on a cold clear winter day, dark red-brown pillars and tall lattice windows, clear cold daylight",
    "dais": f"In the court hall of the county yamen near noon on a cold clear winter day: {DAIS}; clear cold daylight from the tall lattice windows",
    "lane": f"In the narrow lane behind the silk shop in the county town deep in the night: {LANE}; cold blue moonlight from above, the small warm light far down the lane, the wet stones gleaming",
    "lane_c": "In the narrow lane behind the silk shop in the county town deep in the night, dark blue-grey brick walls and worn wet stone slabs, cold blue moonlight from above",
    "bridge": f"Under the old stone bridge at the edge of the county town deep in the night: {BRIDGE}; cold blue moonlight",
    "bridge_c": "At the foot of the old stone bridge at the edge of the county town deep in the night, the dark curve of its stone arch, the misty water and the muddy bank; cold blue moonlight",
    "bridge_top": "On top of the old stone bridge at the edge of the county town deep in the night, its low stone parapet, tall dark bamboo and low tiled roofs against the bright night sky; cold blue moonlight",
    "bridge_w": "Under the old stone bridge at the edge of the county town deep in the night, the slow dark water rippling, cold moonlight glittering on it",
}
LIGHT = {
    "street": "the clear morning sunlight stays unchanged",
    "hall": "the clear cold daylight from the lattice windows stays unchanged",
    "lane": "the cold moonlight and the deep night stay unchanged",
    "bridge": "the cold moonlight, the thin mist and the deep night stay unchanged",
}
# bible rule 15: no "<X> speaks off screen" / "the system voice speaks off screen".
OFFSCREEN_SPEECH = False

# Repeated wording (each prop is one object, written the same way every time).
XU_D = "Xu Yan, in his faded blue-grey scholar's robe patched at one elbow, its sleeves down"
ZHAO = ("Zhao Butou, in his soft black futou cap and plain black round-collared cotton robe, a plain black cloth sash tied at "
        "his waist, nothing else at his waist")
ROLL = "one roll of long plain blank white paper strips"
BLACKMEN = "men in plain black round-collared cotton robes, black caps and cloth shoes"
ONLOOKERS = "onlookers in plain Song-dynasty cotton robes and cloth head wraps"
GREY_DOWN = ("one man in a long plain grey cotton robe lying curled on his side on the paving, his back toward us, his face down "
             "toward the stones, his cloth head wrap pulled low")
LAI_A = ("Lai San, small and thin, in his checked grey-brown cross-collared short jacket, a coarse grey cloth apron tied at his "
         "waist, an old cloth head wrap below his topknot, limping on his left foot")
WEI = ("Wei Shaoqing, in his sapphire-blue brocade robe woven with gold thread, a white jade pendant at his waist, a small green "
       "jade ornament at the front of his topknot")
FAN = "one closed folding fan in his right hand, its dark bamboo ribs pressed tight together like a short slim stick"
ALING = ("A-ling, in her plain grey-white cotton dress with long sleeves covering her wrists, her black hair in a high bun with "
         "one plain wooden hairpin")
VEIL = ("a veil of soft, finely woven pale grey gauze over her nose, mouth and chin, tied behind both ears, falling to just below "
        "her jaw")
SLEEVE = "her right sleeve falling down over her right hand"
DAGGER = "a short plain dagger in a plain dark wooden sheath, as long as her hand, with a dark wooden grip"
HU = "in his black gauze futou hat with two short stiff flat wings and his blue-green round-collared official robe"
GAVEL = "one flat oblong block of dark polished wood the size of half a brick, plain on every side"
SUN = ("Sun Zhanggui, tall and lean with a long narrow face and a thin grey-streaked beard, in his green satin robe with a jade "
       "belt hook")
TORCH_S = "one short burning pine torch held upright in his left hand, the only flame in the frame"
INGOT = "one small silver ingot, its top smooth and plain"
STICK = "one plain wooden stick as long as his arm, smooth and round to its ends"
MEN2 = ("two broad men in plain black cross-collared short jackets, black cloth head wraps and cloth shoes, the moonlight behind "
        "them, their faces in deep shadow")
STACK = "one thick stack of plain blank paper sheets stitched along one edge with cord"
BOX = "one small dark brown wooden cash box with a brass clasp"
YPAPER = "rough blank yellowish paper"
HANDS = "their hands hold only what is described here"
SILENT_HE = "He says nothing in this shot: his lips stay pressed together from the first frame to the last, his jaw still, no talking, no mouthing words"
NOBODY = "Throughout the shot the set layout stays as it is. The pictures fix the place and the objects only, never the mood. "
# e924 fix1's back-of-head wording, as e925 and e926
TBACK = ("one young woman seen only from behind, appearing only once: the back of her head with every strand of her black hair "
         "combed smooth and gathered up into just two round buns set high on her head, one bun on each side, one short pink "
         "silk ribbon wrapped around each bun, the nape of her neck bare and clear above a pink inner collar, and her light "
         "peach-pink silk shoulders; the back of her head facing straight away from us the whole time, her head still, her ear "
         "the furthest round her head we ever see")
HEADSTILL = "the young woman with the two high round buns keeps her head still, facing straight away from us, the back of her head toward us the whole shot"


def quiet(who, pr="his", plural=False):
    verb = "say" if plural else "says"
    return f"{who} {verb} nothing in this shot: {pr} lips stay pressed together from the first frame to the last, no talking, no mouthing words"


def only_tang():
    return "she is the only young woman with two high round buns in the frame"


def alone(rest, where, frame="framed from the waist up"):
    """Tang Xiaotang alone from behind, in the middle of the frame (not at an edge: the pickers' cheek at the frame edge)."""
    return f"medium shot from close behind {TBACK}, {where} in the middle of the frame, {frame}, facing straight away from us; {only_tang()}; {rest}"


SHOTS = [
    # ---- scene 1: the twenty-seventh morning, the Xu shop front (26->27: the same moment; the man in grey on the paving).
    dict(chapter="許記門口", loc="street_w", cam="Medium shot, slow push in", chars=["zhaobutou"], night="street",
         comp=f"medium shot past the soft shoulders of two {ONLOOKERS} in the foreground, seen from behind, out of focus; between them {ZHAO}, framed from the waist up, {ROLL} in his right hand, his left shoulder already pushing in between the two of them from the first frame, his face three-quarter to screen left, his eyes down on the paving beyond the lower left edge of the frame, never the lens; hard and gruff, not smiling: brows down, eyes narrowed, lips moving between loud words; behind him across the street the red silk of the shop front, soft; {HANDS}; exactly three people",
         lines=[("zhaobutou", "讓開！誰家的糖，吃倒了人？", "粗聲，撥開人群")],
         motion="Zhao Butou shoulders his way in between the two onlookers and stops, his eyes on the paving as he speaks; the two onlookers lean aside, their lips closed",
         zh="中景、慢推（送對街魏記門面 `set-xianjie-weiji-l1`：從許記門口看對街；接點 26→27 同一刻）：前景兩個圍觀的人的肩（背影、虛焦）；趙捕頭（黑幞頭、黑圓領布袍、腰間黑布帶什麼都沒掛，拍法 16、17 不寫職稱字）右手一卷空白白紙條（聖經人物表：右手），左肩第一格已經擠進兩人中間，停住、眼睛往畫左下的石板（倒地的客人）、粗聲說。身後兩個衙役不拍（第 19 集：只寫有名字的人；衙役在 s03）；稿子的跟拍改慢推"),
    dict(loc="street_x", cam="Over-the-shoulder medium shot, slow push in", chars=["xuyan"], night="street",
         comp=f"over-the-shoulder medium shot: in the soft right foreground the back of one man's shoulder and black futou cap in a plain black round-collared cotton robe, out of focus, unnamed; beyond him on the paving before the shop's doorway {XU_D}, crouching beside {GREY_DOWN}, framed from the waist up with space above his head, two fingers of his right hand already pressed to the wrist of the man on the ground from the first frame, his face three-quarter to screen right, never the lens; urgent, not smiling: brows drawn together, eyes wide, lips moving fast between words; {HANDS}; exactly three people",
         lines=[("xuyan", "許記的門口。人還有氣，先抬去醫館！", "急，不笑")],
         motion="Xu Yan lifts his eyes from the man on the ground to the man in black as he speaks, his two fingers still on the wrist; the man on the ground lies still",
         zh="過肩（趙捕頭肩後拍許硯）、慢推（送許記門面 `set-xianjie-xuji-l1`：門板還沒立回去）：前景右虛焦的黑幞頭與肩（不點名、不送圖，拍法 2）；許硯第一格已經蹲在倒地的灰衣客人旁（灰布長衫、背影、臉朝石板）、兩指按在手腕上，抬眼看黑衣人、急著說。稿子『快步走過去、蹲下』在第一格已經完成（一鏡一個動作）"),
    dict(loc="street_w", cam="Medium shot, slow push in", chars=["zhaobutou"], night="street",
         comp=f"medium shot of {ZHAO}, standing on the paving, framed from the waist up, {ROLL} in his right hand from the first frame, his left hand already raised to his waist, his face three-quarter to screen left toward Xu Yan off screen left, never the lens; cold and sly, not smiling: eyes narrowed sideways, mouth hard; behind him, small and soft, two {BLACKMEN} already carrying one long pale wooden plank between them toward the right edge of the frame, a man in a long plain grey cotton robe lying face down on it, their backs to us; {HANDS}; exactly four people",
         lines=[("zhaobutou", "抬走。許硯，你的鋪子先封了，人跟我回衙門。", "斜眼，冷")],
         motion="Zhao Butou gives his left hand one short wave toward the right as he speaks; behind him the two men in black carry the plank away at a walking pace, their lips closed",
         zh="中景、慢推（送對街魏記門面）：趙捕頭右手拿著那卷白紙條，左手往畫右一揮、斜眼朝畫左外的許硯說；身後遠處兩個黑圓領布袍的人（背影、小、虛焦）已經抬著卸下的門板往畫右走，門板上躺著灰衣客人（臉朝下）。稿子『一揮手、抬上門板、轉向許硯』三件事改成第一格已經抬著走、他只揮一下手"),
    dict(loc="street_xc", cam="Insert close-up, slow push in", chars=[], night="street",
         comp="insert close-up, the shot opens directly on the pale wooden planks of the shop's plank doors now standing closed side by side, from its very first frame, two long strips of plain blank white paper already crossed over the planks in an X, a hand in a plain black cotton sleeve cuff already pressed flat on the middle of the cross; only the hand, its sleeve cuff, the two blank white strips and the pale planks are in the frame",
         motion=NOBODY + "the flat hand smooths the two strips down hard against the planks once, and a faint puff of dust lifts from the old wood",
         zh="插鏡、慢推（第一格就是立回去的門板與交叉的兩條空白白紙；送許記門面）：黑袖的手第一格已經壓在交叉處，往下一抹，舊木頭揚起一點灰（無台詞）。封條只寫『兩條空白白紙條』（拍法 27，不寫 seal）"),
    dict(loc="street_w", cam="Medium shot from behind, slow push in", chars=["tangxiaotang"], nospeak=["tangxiaotang"], night="street",
         comp=alone(f"{STACK} already held in her left arm against her chest from the first frame, only its pale edge showing at her side, {BOX} held by its handle in her right hand; beyond her, soft, across the stone-paved street, the two-storey shop front with the red silk in the sunlight; {HANDS}",
                    "standing on the paving before the shop"),
         lines=[("tangxiaotang", "帳本跟錢箱我拿出來了，鋪子你們愛封就封！", "臉發白，硬撐，不笑")],
         motion=f"her shoulders square and her right hand lifts the cash box a little; {HEADSTILL}",
         zh="中景（從背後）、慢推（送對街魏記門面）：唐小棠的背影站在門前石板上、畫面正中、正背對鏡頭、頭不動，左臂第一格已經抱著帳本（縫邊的空白紙疊）、右手提著錢箱，肩膀一挺、把錢箱提高一點（nospeak，拍法 3；她的圖與身分句由 spec 拿掉）。稿子『從最後一道門縫側身擠出來、近景下巴以上、臉發白』改背影：側身會露臉；臉發白交給錄音"),
    dict(loc="street_t", cam="Low-angle medium shot, slow push in", chars=["weishaoqing", "xuyan"], night="street",
         comp=f"low-angle medium shot on the paving before the shop: on the left {XU_D}, standing, framed from the waist up, both hands down at his sides, his face three-quarter to screen right toward Wei Shaoqing, never the lens; still and cold, not smiling: jaw set, lips pressed shut; on the right {WEI}, standing close beside him, framed from the waist up, {FAN}, the tip of the closed fan already resting on Xu Yan's shoulder from the first frame, his face three-quarter to screen left toward Xu Yan, never the lens; mocking: a thin lazy smile, eyes half lidded, lips moving slowly between drawled words; {HANDS}; exactly two people",
         lines=[("weishaoqing", "毒糖鋪子，封得好。三十日的賭，你還賭得下去？", "笑，拖長音，本鏡可以笑")],
         motion=f"Wei Shaoqing taps the closed fan twice on Xu Yan's shoulder as he speaks; {quiet('Xu Yan')}; Xu Yan stands still",
         zh="低角度中景、慢推（送門前長櫃與石板 `set-xianjie-shi-l1`）：左邊許硯站著、嘴閉著、不動；右邊魏少卿第一格已經站在他身邊、合著的扇尖搭在他肩上，敲兩下、拖長音笑著說（稿子『本鏡可以笑』；扇子一直合著，拍法 30、第 21 集 fix1）"),
    dict(loc="street_t", cam="Over-the-shoulder medium shot, slow push in", chars=["xuyan"], night="street",
         comp=f"over-the-shoulder medium shot: in the soft right foreground the back of one man's shoulder in a sapphire-blue brocade robe woven with gold thread and the back of his black topknot, out of focus, unnamed, his right hand holding a closed folding fan, its dark bamboo ribs pressed tight together, its tip already resting on the shoulder of the young man facing us from the first frame; facing us beyond him {XU_D}, framed from the waist up, his face three-quarter to screen right toward the man in sapphire brocade, never the lens; steady and cold, not smiling: level eyes, jaw set, lips moving calmly between words; behind him, soft, the long pale wooden counter before the shop and the stone-paved street; {HANDS}; exactly two people",
         lines=[("xuyan", "賭約寫的是三十日，今天才第二十七日。", "很穩")],
         motion="Xu Yan pushes the fan off his shoulder with the back of his right hand as he speaks, his eyes on the man in sapphire brocade; the man in sapphire brocade says nothing, his lips closed",
         zh="反打（魏少卿肩後拍許硯）、慢推（送門前石板）：前景右虛焦的寶藍錦袍肩與髮髻（不點名、不送圖，拍法 2），合著的扇尖第一格搭在許硯肩上；許硯用手背把扇子撥開、正眼看他、很穩地說。稿子『魏少卿聽完轉身回對街』不拍（一鏡一個動作；他之後不入鏡）"),
    dict(loc="street_t", cam="Medium shot, slow push in", chars=["laisan"], night="street",
         comp=f"medium shot of {LAI_A}, standing at the edge of the onlookers beside the end of the long pale wooden counter before the shop, framed from the waist up, beads of sweat on his forehead, both hands already gripping the hem of his apron from the first frame, his face three-quarter to screen right, never the lens; guilty and jumpy, not smiling: brows twitching, eyes darting, lips moving in a low mutter between words; behind him the stone-paved street, soft; {HANDS}",
         lines=[("laisan", "吃壞肚子的事，誰知道是誰家的糖……", "心虛，小聲，自言自語")],
         motion="Lai San rubs both hands hard on the hem of his apron as he mutters",
         zh="中景、慢推（送門前石板）：賴三（跛腳、腰繫粗灰圍裙）在人群邊、門前長櫃的一端，額頭冒汗，兩手第一格已經抓著圍裙下襬，拚命擦、眼睛亂轉、自言自語。稿子的近景改中景（擦手要在畫裡）；前景的門板改長櫃（門板 s04 已立回去）"),
    dict(loc="street_t", cam="Insert close-up, slow push in", chars=[], night="street",
         comp="insert close-up, the shot opens directly on a thin hand in a checked grey-brown sleeve cuff gripping the hem of a coarse grey cloth apron, from its very first frame, a faint trace of greyish white powder along the edges of its fingernails; only the hand, its sleeve cuff and the grey cloth are in the frame",
         motion=NOBODY + "the hand rubs once hard across the cloth, and a faint puff of fine greyish white powder lifts off the fingertips",
         zh="插鏡、慢推（第一格就是指甲；送門前石板）：賴三的瘦手（灰褐格紋袖口）抓著粗灰圍裙，指甲縫邊緣一點灰白的粉（接第 26 集 s33 的伏筆；拍法 12 只寫指甲邊緣），一擦、一點細粉揚起（無台詞）。稿子『手立刻縮進袖子』拿掉（一鏡一個動作）"),
    dict(loc="street_t", cam="Close-up, slow push in", chars=["aling"], night="street",
         comp=f"close-up of {ALING}, {VEIL}, standing at the mouth of a narrow side passage beside the shop, framed from the chest up with space above her head, {SLEEVE}, her face three-quarter to screen right, her eyes lowered toward something low beyond the right edge of the frame, never the lens; sharp and watchful: brows still, eyes narrowing; behind her the stone-paved street, soft",
         motion="A-ling's eyes narrow on something low beyond the right edge of the frame; she stays still, saying nothing, her lips hidden under the veil",
         zh="近景、慢推（送門前石板）：阿令（灰紗面巾遮住口鼻，拍法 21；送面巾定妝照、不送角度圖）第一格已經站在許記旁小巷口，右袖垂著蓋住手（拍法 22：c10–c36 不寫刀），眼睛往畫右下（賴三的手）一瞇（無台詞）。稿子『從巷口走出來、停住、拉袖子』只拍瞇眼（一鏡一個動作）"),
    dict(loc="street_t", cam="Over-the-shoulder medium shot, slow push in", chars=["xuyan"], night="street",
         comp=f"over-the-shoulder medium shot: in the soft left foreground the back of one young woman's head and shoulder, seen only from behind, appearing only once, her black hair in a high bun with one plain wooden hairpin, the thin ties of a pale grey gauze veil behind her ear, her grey-white cotton dress, out of focus, unnamed; facing us beyond her {XU_D}, framed from the waist up, his face turned three-quarter to screen left toward her, never the lens; a hand in a plain black cotton sleeve cuff at the right edge of the frame already gripping his right sleeve from the first frame, its owner outside the frame; alert, not smiling: brows drawn, eyes on her, lips pressed shut; {HANDS}; exactly two people and one black-sleeved hand",
         lines=[("aling", "他指甲縫裡有白粉。你去衙門，他我跟。", "隔著面巾，很低")],
         motion=f"the black-sleeved hand tugs his sleeve once toward the right; {quiet('Xu Yan')}; he listens, his eyes on her",
         zh="過肩（阿令肩後拍許硯）、慢推（送門前石板）：前景左虛焦的阿令後腦（高髻、木簪、面巾的細繩，不點名、不送圖，拍法 2）；許硯側過頭朝她、嘴閉著聽；畫右緣黑袖的手第一格已經抓著他的袖子、拉一下（趙捕頭不入鏡）。阿令的台詞放錄音（面巾）"),
    dict(loc="street_t", cam="Close-up, slow push in", chars=["xuyan"], night="street",
         comp=f"close-up of {XU_D}, framed from the chest up with space above his head, his face three-quarter to screen right toward someone out of sight beyond the right edge of the frame, never the lens; that side of the frame is only the soft pale wooden front of the shop all the way to the edge, and he is the only person in the frame; low and steady, not smiling: eyes firm, lips moving low between words; behind him, soft, the pale plank front of the shop with two long strips of plain blank white paper crossed over it",
         lines=[("xuyan", "好。小棠，抱好帳本，去綢緞莊等我。", "壓低聲音")],
         motion="Xu Yan gives one small nod as he begins to speak, low and steady, his eyes staying on that spot beyond the right edge",
         zh="近景、慢推（送門前石板）：許硯一個人在畫裡，朝畫右外看不到的人（唐小棠）壓低聲音說，開口時點一下頭；畫右到邊緣只有虛焦的許記木門面（第 25 集教訓：不寫『朝畫外的年輕女子』）。稿子『點頭再轉頭』只留點頭（一鏡一個動作）"),
    dict(loc="street", cam="Wide shot, slow push in", chars=[], night="street",
         comp=f"wide shot down the street at standing eye height, like the picture: in the middle of the stone-paved street, a little way off, two men walking away from us side by side, their backs to us: on the left one man in a soft black futou cap and a plain black round-collared cotton robe, his right hand gripping the sleeve of the man beside him, and on the right one young man in a faded blue-grey scholar's robe with his black hair in a topknot; along both sides of the street four {ONLOOKERS}, small, side-on, their faces turned toward the two men; {HANDS}; exactly six people",
         lines=[("zhaobutou", "走快點！縣太爺等著問你話。", "背對鏡頭，不耐煩")],
         motion=NOBODY + "the two men walk away down the middle of the street at a brisk pace; the four onlookers watch them go, their lips closed",
         zh="全景、慢推（人眼高、照圖；送縣城大街 `set-xianjie-l1`）：趙捕頭押著許硯往街裡走（兩人都是背影、不點名、不送圖：背影送了臉部圖會轉頭）；街兩邊四個圍觀的人側面看著（拍法 25）；趙捕頭的話放錄音（結尾）。稿子『唐小棠走進綢緞莊、賴三往右走、阿令跟上』不拍：一鏡最多三張臉、她不露臉；去向由 s12 的台詞與第三場交代。跟拍改慢推"),
    # ---- scene 2: the court hall near noon (the floor crop for Xu Yan, the dais crop for Magistrate Hu).
    dict(chapter="縣衙公堂", loc="dais", cam="Low-angle medium shot, slow push in", chars=["huxianling"], night="hall",
         comp=f"low-angle medium shot from the floor of the court hall: in the soft left foreground the back of one young man in a faded blue-grey scholar's robe, his black hair in a topknot, standing on the grey stone tiles, seen only from behind, unnamed; beyond him, raised on the dais, Magistrate Hu, {HU}, sitting behind the long dark desk, framed from the waist up, his right hand already gripping {GAVEL} raised a hand's height above the desk from the first frame, his face three-quarter to screen left toward the young man below, never the lens; pompous and stern, not smiling: chin up, brows lifted, mouth drawn long between words; behind him only the plain white panels; {HANDS}; exactly two people",
         lines=[("huxianling", "許硯！毒糖害人，人證物證都在，你認不認？", "官腔，拍案")],
         motion="Magistrate Hu brings the wooden block down flat on the desk with one sharp knock and speaks; the young man below stands still",
         zh="低角度中景（從堂下往上）、慢推（送公案裁切 `set-xianya-gongtang-dais-l1`：整張公堂圖案上方掛著一塊匾，會長字，不送）：前景左許硯的背影（不點名、不送圖）；高台案後胡縣令（每鏡寫有帽翅的黑紗幞頭、藍綠圓領官袍），右手第一格已經舉著驚堂木（長方形木塊），一拍、官腔問。兩排衙役與水火棍頓地交給音效（第 19 集：公堂只拍有名字的人）；稿子的全景推軌改中景慢推（全景要帶上整張公堂，圖上案上方的匾會長字）"),
    dict(loc="hall", cam="Low-angle medium close-up, slow push in", chars=["xuyan"], night="hall",
         comp=f"low-angle medium close-up of {XU_D}, standing on the grey stone tiles, framed from the chest up with space above his head, both hands already joined before his chest in a bow from the first frame, his body still bent a little forward, his face three-quarter to screen right, his eyes raised toward the dais beyond the upper right edge of the frame, never the lens; calm and firm, not smiling: level brows, steady eyes, lips moving clearly between words; behind him a thick dark red-brown pillar and the bright lattice windows, soft",
         lines=[("xuyan", "糖是我做的，藥不是。那塊糖，也不是許記賣的。", "平靜，不卑不亢")],
         motion="Xu Yan straightens up from the bow and lifts his chin as he speaks; after the last word he keeps his eyes on the dais",
         zh="低角度中近景、慢推（送公堂地面裁切 `set-xianya-gongtang-floor-l1`）：許硯第一格已經拱手作揖，直起身、抬下巴，朝畫右上外的高台說。稿子『身後是大門口的白光』圖上沒有門：寫格窗的光"),
    dict(loc="dais", cam="Medium close-up, slow push in", chars=["huxianling"], night="hall",
         comp=f"medium close-up from below the dais: Magistrate Hu, {HU}, sitting behind the long dark desk, framed from the chest up with clear space above his hat, one small slip of plain paper folded shut in his right hand from the first frame, its blank outside toward us, {GAVEL} on the desk before him, his face three-quarter to screen left toward the floor below the dais, never the lens; impatient, not smiling: brows pinched, mouth turned down, lips moving fast between words; behind him only the plain white panels",
         lines=[("huxianling", "醫館回話了，只是瀉藥，那人拉了半天，死不了。", "不耐煩")],
         motion="Magistrate Hu tosses the folded slip down onto the desk as he speaks; after the last word he leans back in his chair",
         zh="中近景、慢推（送公案裁切）：胡縣令手上一張摺著的條子（空白的紙背朝鏡頭，拍法 27），往案上一丟、不耐煩地說。稿子『打開條子看一眼』不拍（攤開的紙會長字；本集提示詞不出現 open）、『甩袖』拿掉"),
    dict(loc="dais", cam="Over-the-shoulder medium shot, slow push in", chars=["huxianling"], night="hall",
         comp=f"over-the-shoulder medium shot from the floor: in the soft left foreground the back of one young man's shoulder in a faded blue-grey scholar's robe and the back of his topknot, out of focus, unnamed, his two hands joined before him; beyond him, raised on the dais, Magistrate Hu, {HU}, sitting behind the long dark desk, framed from the waist up, his right hand already resting flat on the desk beside {GAVEL}, his face three-quarter to screen left toward the young man, never the lens; bored and sour, not smiling: eyes half lidded, mouth turned down, lips pressed shut; behind him only the plain white panels; {HANDS}; exactly two people",
         lines=[("xuyan", "人沒事，那許記的鋪子，大人可以先解封了吧？", "有禮，追問")],
         motion=f"Magistrate Hu drums his fingers slowly on the desk while he listens; {quiet('Magistrate Hu')}",
         zh="過肩（許硯肩後拍胡縣令）、慢推（送公案裁切）：前景左虛焦的書生肩與髮髻（不點名、不送圖，拍法 2）；胡縣令手指在案上敲、嘴閉著聽（不說話、嘴閉著）；許硯的話放錄音"),
    dict(loc="dais", cam="Low-angle close-up, slow push in", chars=["huxianling"], night="hall",
         comp=f"low-angle close-up from below the dais: Magistrate Hu, {HU}, leaning forward over the long dark desk, framed from the chest up with clear space above his hat, his right hand already gripping {GAVEL} raised a hand's height above the desk from the first frame, his face three-quarter to screen left toward the floor below, never the lens; angry, not smiling: brows slammed down, heavy cheeks set, the corners of his mouth pulled down, lips moving hard between words; behind him only the plain white panels",
         lines=[("huxianling", "人沒事，名聲壞了！鋪子照封，等本官查清楚。", "拍案，發怒")],
         motion="Magistrate Hu brings the wooden block down hard on the desk with one loud knock, his heavy cheeks shaking, and speaks",
         zh="低角度近景、慢推（送公案裁切）：胡縣令身子壓在案上，驚堂木（長方形木塊，不是槌子）重重一拍、兩頰一抖，發怒不笑地說"),
    dict(loc="hall_c", cam="Close-up, slow push in", chars=["xuyan"], night="hall",
         comp=f"close-up of {XU_D}, standing on the grey stone tiles, framed from the chest up with space above his head, his face three-quarter to screen right toward the dais beyond the right edge of the frame, never the lens; hurt and holding it in: jaw clenched, brows drawn, lips pressed shut; behind him only a dark red-brown pillar and the soft light of the lattice windows",
         lines=[("xitong", "叮。鬥商剩三日。", "冷，宣布"),
                ("xitong", "鋪子封了，宿主只剩一張嘴。", "冷"),
                ("xuyan", "一張嘴不夠，那就再加一張紙。", "心裡話，錄得近、輕", "inner")],
         panel=[("鬥商剩三日", "task")],
         motion=f"Xu Yan shuts his eyes, draws one slow breath, and lifts his eyes again, calm and steady; {SILENT_HE}; he is thinking, not speaking",
         zh="近景、慢推（送公堂地面裁切；拍法 11 不寫藍光，稿子『臉被淡藍光照亮』不照用）：許硯下巴繃緊、閉眼吸一口氣、再抬眼時很穩；全程嘴閉著（系統畫外兩句、心裡話）。本集的鬥嘴；面板「鬥商剩三日」由剪接疊上"),
    dict(loc="hall", cam="Medium shot, slow push in", chars=["xuyan"], night="hall",
         comp=f"medium shot of {XU_D}, standing on the grey stone tiles, framed from the waist up, both hands already joined before his chest from the first frame, his face three-quarter to screen right toward the dais beyond the right edge of the frame, never the lens; calm and courteous, not smiling: steady eyes, lips moving clearly between words; behind him the thick dark red-brown pillars, the low white panel and the bright lattice windows, soft; {HANDS}",
         lines=[("xuyan", "大人，學生只要一樣東西：包那塊糖糕的紙。", "不卑不亢")],
         motion="Xu Yan lowers his joined hands and holds out his right hand flat, palm up, toward the dais as he speaks; after the last word he keeps the hand out",
         zh="中景、慢推（送公堂地面裁切）：許硯第一格已經拱著手，放下、右手掌心朝上平伸向高台說。稿子『再一揖、直起身』在 s15 拍過，這鏡只拍伸手"),
    dict(loc="dais", cam="Medium close-up, slow push in", chars=["huxianling"], night="hall",
         comp=f"medium close-up from below the dais: Magistrate Hu, {HU}, sitting behind the long dark desk, framed from the chest up with clear space above his hat, {GAVEL} on the desk before him, his face three-quarter to screen left toward the floor below, never the lens; scornful: a short sneering laugh through his nose, heavy cheeks shaking, eyes narrowed, lips moving between words; behind him only the plain white panels",
         lines=[("huxianling", "一張紙能救你？趙捕頭，給他。", "嗤笑，本鏡可以笑")],
         motion="Magistrate Hu gives his bulging left sleeve one lazy wave toward the right edge of the frame as he speaks",
         zh="中近景、慢推（送公案裁切）：胡縣令嗤笑一聲（稿子『本鏡可以笑』）、臉頰跟著抖，袖子朝畫右外（案邊的趙捕頭，不入鏡）一甩"),
    dict(loc="hall_c", cam="Insert close-up, slow push in", chars=[], night="hall",
         comp=f"insert close-up, the shot opens directly on one man's right hand held out flat, palm up, in a faded blue-grey sleeve cuff, from its very first frame, a hand in a plain black cotton sleeve cuff already held just above it with one crumpled greasy scrap of {YPAPER} pinched in its fingers, a few grains of greyish white powder caught in the creases of the paper; the grey stone tiles soft far below; only the two hands, their sleeve cuffs and the crumpled paper are in the frame",
         motion=NOBODY + "the black-sleeved hand lets the crumpled yellowish paper drop into the flat palm, and the grains of powder in its creases glint in the window light",
         zh="插鏡、慢推（第一格就是攤平的掌心；送公堂地面裁切）：許硯的掌心（藍灰袖口）朝上，黑袖的手第一格已經捏著一張揉皺、沾油的粗黃紙（空白，拍法 27、28），一鬆手落進掌心，摺痕裡幾粒灰白細粉在窗光下一閃（無台詞）。稿子『手指把紙攤開』不拍（攤開的紙會長字）"),
    dict(loc="hall_c", cam="Close-up, slow push in", chars=["xuyan"], night="hall",
         comp=f"close-up of {XU_D}, framed from the chest up with space above his head, his head bowed, his eyes lowered to one crumpled scrap of {YPAPER} held in both his hands at the lower edge of the frame from the first frame, its blank outside toward us; thinking hard, not smiling: brows drawn, eyes narrowed on the paper, lips pressed shut; behind him a dark red-brown pillar and the soft light of the lattice windows",
         lines=[("xuyan", "黃的，粗的……許記的包糖紙，從來只用白的。", "心裡話，錄得近、輕", "inner")],
         motion=f"Xu Yan slowly folds the scrap of yellowish paper once along its crease; {SILENT_HE}; he is thinking, not speaking",
         zh="近景、慢推（送公堂地面裁切）：許硯低頭看兩手間的黃紙（空白的外面朝鏡頭），沿摺痕摺一次；全程嘴閉著（心裡話）。稿子『收進右袖』交給剪接（一鏡一個動作；黃紙之後在右袖）"),
    dict(loc="dais", cam="Medium shot, slow push in", chars=["huxianling"], night="hall",
         comp=f"medium shot from the floor of the court hall: Magistrate Hu, {HU}, sitting behind the long dark desk on the dais, framed from the waist up, his right hand already resting on {GAVEL} on the desk, his face three-quarter to screen left toward the far end of the hall beyond the left edge of the frame, never the lens; bored and done with it, not smiling: chin up, eyes half lidded, mouth drawn long between drawled words; behind him only the plain white panels; {HANDS}",
         lines=[("huxianling", "人先放回去，隨傳隨到！退堂！", "在案後，拖長音")],
         motion="Magistrate Hu taps the wooden block down once on the desk as he calls out the last words",
         zh="中景、慢推（送公案裁切）：胡縣令在案後朝畫左外（許硯走出去的方向）拖長音喊，最後一聲驚堂木輕輕一敲（結尾）。稿子『許硯走向大門、門檻回頭一揖』不拍：兩張圖上都沒有門，許硯的腳步與跨門檻交給音效；第二場從 s23 的黃紙切到這一鏡、再切夜裡的巷子"),
    # ---- scene 3: that night, the lane behind the silk shop (set-chouduan-ye-xiang-l1) and the stone bridge.
    dict(chapter="後巷與石橋", loc="lane", cam="Wide shot, slow push in", chars=["laisan"], night="lane",
         comp=f"wide shot down the lane at standing eye height, like the picture: {LAI_A}, coming up the middle of the lane toward us, framed full figure, both hands already pushed into his sleeves before his chest from the first frame, his head already turned half back over his shoulder toward the far end of the lane, never the lens; nervous and hurried, not smiling: eyes darting, lips moving in a low mutter between words; in the soft left foreground the rim of one wooden tub; {HANDS}; he is the only person in the frame",
         lines=[("laisan", "拿了銀子就出城，這縣城待不得了。", "小聲，自言自語")],
         motion="Lai San limps quickly toward us along the wet stones, dragging his left foot at every step, as he mutters",
         zh="全景、慢推（人眼高、照圖；送綢緞莊後巷的免費新圖 `set-chouduan-ye-xiang-l1`：裁掉左上的大空白招牌、塗掉門楣上的小空白牌子）：賴三（圍裙沒解、跛腳）兩手攏在袖子裡，第一格已經回頭望巷子深處，一拐一拐朝鏡頭走、自言自語。稿子的『鏡頭在他前面往後退』改慢推；『柴捆、燈籠』照圖改成木桶（掛著的燈籠不寫）"),
    dict(loc="lane_c", cam="Medium close-up, slow push in", chars=["aling"], night="lane",
         comp=f"medium close-up of {ALING}, {VEIL}, pressed close along the dark brick wall on the left of the lane in deep shadow, framed from the chest up with space above her head, {SLEEVE}, her face three-quarter to screen right toward the far end of the lane, never the lens; tense and silent: brows level, gaze fixed ahead; behind her the dark brick wall, soft",
         motion="A-ling glides a few silent steps along the wall and stops still against it; she says nothing, her lips hidden under the veil",
         zh="中近景、慢推（送後巷圖）：阿令（面巾）貼著左邊磚牆走在暗影裡，無聲滑幾步、停住貼牆（無台詞）。稿子的橫移改慢推；『只有一雙眼睛映著月光』不寫（眼睛旁不寫光，preflight 的 eye-glow）"),
    dict(loc="bridge", cam="Wide shot, slow push in", chars=["laisan", "sunzhanggui"], night="bridge",
         comp=f"wide shot at standing eye height from the muddy bank, like the picture: the old stone arch bridge over the dark water; on the bare muddy bank on the left near the foot of the arch {LAI_A}, small, framed full figure, hunched, his face three-quarter to screen right toward Sun Zhanggui, never the lens, scared, his lips pressed shut; a little right of him in the shadow at the foot of the arch {SUN}, small, framed full figure, {TORCH_S}, his face three-quarter to screen left toward Lai San, never the lens; slow and cool, not smiling: eyes half lidded, lips moving slowly between words; {HANDS}; exactly two people",
         lines=[("sunzhanggui", "賴三，事辦乾淨了？沒讓人看見吧？", "慢條斯理")],
         motion=f"Sun Zhanggui raises the torch toward Lai San's face as he speaks; {quiet('Lai San')}",
         zh="全景、慢推（人眼高、照圖；送石橋月夜 `set-shiqiao-ye-l1`）：左邊泥岸、拱腳下賴三弓著背、嘴閉著；他右邊拱下暗處孫掌櫃（瘦長臉、花白鬍、綠緞袍、玉帶鉤；聖經同框撞臉：他只在第三場）左手一支松明火把（聖經的小紙燈籠改火把：燈籠會長字，第 25 集審稿），舉起火把照賴三的臉、慢條斯理地說。稿子的高角度（從橋欄往下）跟人眼高的圖打架，改人眼高"),
    dict(loc="bridge_c", cam="Medium close-up, slow push in", chars=["laisan"], night="bridge",
         comp=f"medium close-up of {LAI_A}, standing hunched at the water's edge at the foot of the stone arch, framed from the chest up with space above his head, both hands already rubbing together before his chest from the first frame, warm torchlight on his face from the right, his face three-quarter to screen right toward Sun Zhanggui off screen right, never the lens; eager to please and scared, not smiling: eyes wide, brows up, lips moving fast between words; behind him the dark curve of the stone arch and the misty water, soft",
         lines=[("laisan", "沒有沒有，三包都給了那人，他當場就倒。", "搓手，急著表功")],
         motion="Lai San rubs his hands faster and nods quickly as he speaks",
         zh="中近景、慢推（送拱下的免費裁切 `set-shiqiao-ye-dong-l1`）：賴三弓著背在拱下水邊，兩手第一格已經在搓，越搓越快、連連點頭說；火光從畫右照來"),
    dict(loc="bridge_w", cam="Insert close-up, slow push in", chars=[], night="bridge",
         comp=f"insert close-up, the shot opens directly on a thin palm held flat and face up in a checked grey-brown sleeve cuff above the dark rippling water, from its very first frame, a thin hand in a green satin sleeve cuff already holding {INGOT} just above it; cold moonlight glittering on the water below; only the two hands, their sleeve cuffs, the ingot and the water are in the frame",
         motion=NOBODY + "the green-sleeved hand sets the silver ingot down into the flat palm, and the glittering water below ripples",
         zh="插鏡、慢推（第一格就是兩隻手與水；送水面的免費裁切 `set-shiqiao-ye-shui-l1`）：綠緞袖口的手把一錠銀子（頂面平滑、沒有字，拍法 27）放進灰褐袖口的掌心，底下月光的水面起波（無台詞）。稿子『第一格就是水面倒影、一滴水打碎倒影』改成直接拍手與水（倒影裡的兩隻手與銀子是三件難畫的事）"),
    dict(loc="bridge_c", cam="Close-up, slow push in", chars=["sunzhanggui"], night="bridge",
         comp=f"close-up of {SUN}, framed from the chest up with space above his head, {TORCH_S}, held low at his chest, its warm light on his face from below, his face three-quarter to screen left toward Lai San off screen left, never the lens; cold and sly: one corner of his mouth lifting in a thin cold smile, eyes half lidded, lips moving slowly between words; behind him only the dark stone of the arch and the mist, soft",
         lines=[("sunzhanggui", "少爺賞的。底下有魏記的戳，別拿去花。", "慢條斯理，冷笑")],
         motion="Sun Zhanggui tips his chin once toward the silver in the other man's hands beyond the left edge of the frame as he speaks",
         zh="近景、慢推（送拱下裁切）：孫掌櫃火把低握在胸前、火光從下往上照，嘴角冷冷一勾（稿子『本鏡可以冷笑』），下巴朝畫左外的銀子一點。稿子『用燈籠桿點一點銀子』改下巴一點（火把不碰銀子）"),
    dict(loc="bridge_c", cam="Medium close-up, slow push in", chars=["laisan"], night="bridge",
         comp=f"medium close-up of {LAI_A}, at the foot of the stone arch, framed from the chest up with space above his head, {INGOT} already held up in both hands before his chest from the first frame, warm torchlight on his face from the right, his face three-quarter to screen right toward Sun Zhanggui off screen right, never the lens; greedy and delighted: a wide grin, eyes shining, lips moving fast between words; behind him the dark curve of the stone arch and the misty water, soft",
         lines=[("laisan", "替我謝謝魏少爺，我這就出城躲幾天。", "咧嘴，本鏡可以笑")],
         motion="Lai San tucks the silver ingot into the front of his jacket as he speaks and pats it flat once",
         zh="中近景、慢推（送拱下裁切）：賴三兩手捧著銀子，咧嘴笑（稿子『本鏡可以笑』）、塞進前襟拍一下。稿子『咬一口銀子邊』拿掉（一鏡一個動作）"),
    dict(loc="bridge_top", cam="Medium close-up from below, slow push in", chars=["aling"], night="bridge",
         comp=f"medium close-up from below of {ALING}, {VEIL}, crouched low on top of the old stone arch bridge behind its low stone parapet, framed from the chest up with space above her head, {SLEEVE}, her left hand already laid flat on the cold stone of the parapet at the lower edge of the frame from the first frame, the bright night sky behind her, the lower edge of her veil stirring a little in the night wind, her face turned down three-quarter to screen right toward the water below the bridge, never the lens; cold and certain: eyes narrowed, brows still; beside her the tall dark bamboo, soft",
         lines=[("aling", "綠緞袍的孫掌櫃……少爺，就是魏少卿。", "心裡話，錄得近、輕", "inner")],
         motion="A-ling's left hand slowly tightens on the stone of the parapet into a fist; she says nothing in this shot: her lips stay closed under the veil from the first frame to the last, no talking, no mouthing words; she is thinking, not speaking",
         zh="中近景（從下往上）、慢推（送橋頂的免費裁切 `set-shiqiao-ye-qiao-l1`：橋面、石欄、竹子與亮的夜空，月亮在圖上、提示詞不寫）：阿令伏在石欄後，左手第一格已經平按在石頭上、慢慢握緊；面巾下緣被夜風吹動一點；心裡話，嘴閉著"),
    dict(loc="bridge_c", cam="Close-up, slow push in", chars=["sunzhanggui"], night="bridge",
         comp=f"close-up of {SUN}, framed from the chest up with space above his head, {TORCH_S}, his face three-quarter to screen left toward Lai San off screen left, never the lens; smooth and cold, not smiling: eyes half lidded, lips moving slowly between words; behind him the dark stone of the arch and the misty bank, soft",
         lines=[("sunzhanggui", "兩個兄弟先去巷口等你，送你出城。", "慢條斯理")],
         motion="Sun Zhanggui swings the torch once toward the dark bank beyond the right edge of the frame as he speaks, his eyes staying on Lai San",
         zh="近景、慢推（送拱下裁切）：孫掌櫃火把朝畫右外的暗處泥岸一晃、眼睛仍看賴三，慢條斯理地說。稿子『兩個人影沿泥岸先走』不拍（一鏡一個動作；打手在 s37 才露背光的身形）"),
    dict(loc="lane", cam="Wide shot, slow push in", chars=["laisan"], night="lane",
         comp=f"wide shot down the lane at standing eye height, like the picture: {LAI_A}, walking slowly up the middle of the lane toward us, framed full figure, {INGOT} in his right hand from the first frame, his face three-quarter to screen left, his eyes on the silver, never the lens; smug and greedy, not smiling: eyes gleaming on the silver, lips moving between words; {HANDS}; he is the only person in the frame",
         lines=[("laisan", "魏少爺出手真大方，一錠頂我半年工錢。", "拋著銀子，得意")],
         motion="Lai San tosses the silver ingot a little way up and catches it again as he speaks, limping on",
         zh="全景、慢推（人眼高、照圖；送後巷圖）：回程的巷子，賴三一拐一拐往鏡頭走，把銀子往上一拋、接住、得意地說。稿子『腳步停在半空、盯著白牆』交給 s35、s36（一鏡一個動作）"),
    dict(loc="lane_c", cam="Insert close-up, slow push in", chars=[], night="lane",
         comp="insert close-up, the shot opens directly on the worn wet stone slabs of the lane in the cold moonlight, from its very first frame, the long dark shadow of a small hunched man stretched across them, and close behind it the edge of a second, slender shadow with one hairpin standing up from its high bun; only the stones and the two shadows are in the frame",
         motion=NOBODY + "the slender shadow slides up close behind the hunched one and stops still",
         zh="插鏡、慢推（第一格就是月光下的石板與兩個影子；送後巷圖）：駝背的影子後面，一個插著一根髮簪的細長影子滑上來、停住（無台詞）。稿子的『燈籠照著的白牆』圖上沒有（掛著的燈籠不寫），影子改落在月光的石板上；『駝背的影子一縮』拿掉（一鏡一個動作）"),
    dict(loc="lane_c", cam="Medium close-up, slow push in", chars=["laisan"], night="lane",
         comp=f"medium close-up of {LAI_A}, framed from the chest up with space above his head, {INGOT} already clutched against his chest in both hands from the first frame, his face pale, three-quarter to screen right toward the dark doorways beyond the right edge of the frame, never the lens; frightened and spiteful, not smiling: eyes wide, brows up, lips moving fast in a loud call between words; behind him the dark brick wall, soft",
         lines=[("laisan", "大哥們，有尾巴跟著我，就在牆那邊！", "朝暗處喊")],
         motion="Lai San shouts toward the dark doorways on the right, his voice carrying down the lane",
         zh="中近景、慢推（送後巷圖）：賴三轉過身、臉色發白、不笑（稿子），銀子緊抱在胸前，朝畫右外的暗門洞大喊。稿子『害怕扭成賊笑』跟『不笑』衝突，照『不笑』：害怕轉狠"),
    dict(loc="lane", cam="Low wide shot, static", chars=["aling", "laisan"], nospeak=["aling"], night="lane",
         comp=f"low wide shot at knee height down the lane: on the left in the middle of the lane {ALING}, {VEIL}, standing, framed full figure, her face three-quarter to screen right toward the men, never the lens; cold and calm: eyes narrowed, brows level; on the right, a few steps away, {MEN2}, standing side by side across the lane, side-on to us, framed full figure, each gripping {STICK} in his right hand; just behind them {LAI_A}, small, half hidden behind their shoulders, his face three-quarter to screen left, never the lens, his lips closed; {HANDS}; exactly four people",
         lines=[("aling", "兩根棍子，加你一個，一起來。", "隔著面巾，冷")],
         motion=f"with her right hand A-ling draws out of her right sleeve {DAGGER}, and holds it low at her side, still in its sheath; the two men and Lai San stand still, their lips closed",
         zh="低機位全景、定鏡（送後巷圖）：左邊巷子中間阿令（面巾）；右邊兩個黑短打、黑布包頭的人（背光、臉在暗影裡、側面，不給正臉，聖經〈小角色〉）並肩橫在巷子裡，各握一根木棍；賴三縮在他們身後。阿令右手從袖子裡抽出套著素木鞘的短匕（拍法 22；稿子：連鞘抽出、沒出鞘），低握在身側；台詞放錄音（面巾，nospeak）（結尾，懸念 → 第 28 集第一場）。稿子的搖鏡改定鏡；『木棍拍掌心、一步步逼近』交給音效（一鏡一個動作）"),
]

HEAD = [
    "- 重製版 r2、真人版（站主 2026-11-11「之後都用真人版」）：照 `docs/videos/zhong-tian-qu-qi-e027-r2/script.md`（c01–c37 對應 s01–s37；含「這版改了什麼」「2026-11-06 審稿後的修改」與「真人版的改動（2026-11-17）」）；台詞一字不改，只改拍法；每鏡一個看得見的動作、一句一筆不拆半句、預設不笑。篇章設定 `production/r2-bible-e021-e030.md`（拍法 1–30 條）。第 3 篇章〈搶親〉第七集。",
    "- 內部工作編號 927（`hailuo/{ff,clips}-dh-e927.json`、`colab/runs/e927/extras.json`、`colab/runs/e927-live/spec.json`，工作資料夾 `~/mokaair-work/videos/zhong-tian-qu-qi-e927-dh/`）；發布 slug `zhong-tian-qu-qi-e027-r2`。不放集數、不放片名卡；s01 接第 26 集 s40（接點 26→27：同一刻，趙捕頭帶衙役撥開人群，手上一卷封條；灰衣客人倒在石板上；許硯在門口）；s37 交給第 28 集（接點 27→28：同一刻，賴三往打手身後一縮）。",
    "- 照第 26 集審稿後的寫法與第 21–25 集挑片學到的一開始就照做：`OFFSCREEN_SPEECH = False`；背影、前景或畫外的人說話時，每張朝鏡頭的臉都寫不說話、嘴閉著、在聽；**對畫外的人說話寫「朝畫右外看不到的人」，那一側到邊緣只有景、畫面裡只有他一個人，不寫「畫外那個年輕女子」**（第 25 集教訓）；掛著的東西不點名；不寫 open；道具與接觸寫在第一格；紙一律空白；寫人數。",
    "- **唐小棠不露嘴說話、本集也不露臉**（拍法 3）：她唯一一句（s05）從背後拍、畫面正中、正背對鏡頭、頭不動、剛好兩顆丸子；spec 拿掉她的圖與身分句；其他鏡都沒有她（稿子 c13 走進綢緞莊不拍）。**算盤本集沒有**（拍法 20）。",
    "- **阿令整集戴面巾**（拍法 21，第一次）：送 `aling-veil-portrait-l1`、不送角度圖；台詞全是錄音（s11 背影在前景、s32 心裡話、s37 面巾下）；短匕只在 s37（拍法 22：套著素木鞘從右袖抽出），其他鏡寫右袖垂著蓋住手。",
    "- **衙役與趙捕頭**（拍法 16、17）：不寫職稱字；趙捕頭右手一卷空白白紙條；衙役只在 s03 遠處兩個背影抬門板，第二場兩排衙役與水火棍交給音效；貼封條、抓袖子、遞紙都只拍黑袖的手。**胡縣令每鏡都戴有帽翅的黑紗幞頭**、只送公案裁切；許硯只送公堂地面裁切（整張公堂圖案上方掛著匾，會長字）。**孫掌櫃**只在第三場，聖經的小紙燈籠改成一支松明火把（燈籠會長字）。",
    "- **場景圖說了算**（拍法 29，協調者 2026-11-17 決定，每張放大看過）：大街 `set-xianjie-l1` 與第 24 集的三張裁切（許記在左、魏記在右）；公堂地面 `set-xianya-gongtang-floor-l1`、公案 `-dais-l1`；**新的免費圖四張**：後巷 `set-chouduan-ye-xiang-l1`（綢緞莊後巷夜圖裁掉左上的大空白招牌、塗掉門楣上的小空白牌子）、石橋的三張裁切 `set-shiqiao-ye-dong-l1`（拱下）、`-qiao-l1`（橋頂與夜空）、`-shui-l1`（水面）。**不需要試鏡**。",
    "- 長鏡要買的秒數（BUY）：照錄音核過（見 `r2.py` 的 BUY 註解）。",
    "- **表上的「秒」欄是 lint 估法**，比錄音短；剪接以錄音的人聲長度為準。",
]
FOOT = [
    "- **參考圖**（`assets/refs-live/`）：許硯（l1、angle-a；帶笑的 angle-b 整集不送）、阿令（面巾 `aling-veil-portrait-l1`，不送角度圖）、賴三 l1、趙捕頭 l1、魏少卿 l1、胡縣令 l1、孫掌櫃 l1。唐小棠整集不送圖。圍觀的人、衙役、灰衣客人、兩個打手、手都不送圖。場景見上面。",
    "- 共用檔：程式都沒改（畫面上說話的人都在 `build-r2.py` 的 `EN`；本集沒有小角色說話）；`gen-dh.mjs`、`pilot.py`、`cast.json` 不動；`refs-live` 加四張免費圖（都是新 id）與 README 一段。趙捕頭的職稱字、胡縣令的帽子、孫掌櫃的笑眼、阿令的紅唇由 `colab/runs/e927/extras.json` 換掉；精修文字的 CG 立領句與『Constable Zhao』由本檔結尾的 `live_clips()` 在 build 後從 `clips-dh-e927.json` 換掉。",
    "- `colab/runs/e927/extras.json`（照第 26 集，加上述四項）與 `colab/runs/e927-live/spec.json`（`mkspec.py` 產生；種子 9271101／9271102）。",
    "- 免費準備：scratchpad `prep927.sh`（`DRY=1 … st1-ep.sh 927` → `pilot.py` → `retake.py` → `colab-jobs.json` 加 output_path、套 swap_pictures（絕對路徑）→ 逐鏡查送的場景圖與人物圖 → 精修用的分隔句 → `preflight-prompts.py` → 否定名詞、會長字的名詞、掛著的東西、open 與『畫外的年輕女子』掃描）。",
    "- 配樂：門口緊張的低弦，s04 封條一聲重拍、s09 指甲特寫一個細高音；公堂沉悶的鼓與低弦，s14、s18 驚堂木、s19 系統底下停一拍、s22 紙落掌心一個輕高音；後巷與石橋只有低音與水聲，s29 銀子一個重音，s37 大重音後收。音效見 script.md〈音樂與音效〉（另外：第二場的『威武』與水火棍頓地、s24 許硯的腳步與跨門檻、s33 兩個人影沿泥岸走開、s37 木棍拍掌心，都交給音效）。",
]

# Long shots: seconds to buy. Measured 2026-11-17 against the 32 kept recordings (~/mokaair-work/videos/zhong-tian-qu-qi-e927-dh/audio;
# wave length and silencedetect -35 dB speech span; e013's test: a shot holds (buy - 0.3) x 1.1 s of speech, half a second
# between lines, so 5 s holds 5.17 s, 6 s 6.27 s, 8 s 8.47 s). faster-whisper medium read every take back, one clip per process,
# numpy input, once plain and once with the previous line and the line as context (audio/fw927.txt; audio/README-retakes.txt).
# 8 s: s06 (a05 Wei Shaoqing's drawl, speech 6.52 s); s16 (a13, 6.68 s); s19 (the system a16 1.49 s + 0.5 + a17 1.82 s + 0.5 +
#      his thought a18's third take 2.87 s = 7.18 s: the script's long shot, one face); s21 (a20 with the sneer, 6.64 s); s37 (a32 2.65 s,
#      but it is the episode's last shot: the hook needs a held tail, as e923 s40, e924 s36, e925 s40b and e926 s40).
# 6 s: every other speaking shot. The tightest: s14 (a11 5.86 s), s18 (a15 5.83 s), s34 (a30 5.62 s), s23 (a21's third take 5.52 s),
#      s24 (a22 5.04 s), s15 (a12 4.81 s).
# Re-recorded (audio/README-retakes.txt; first takes in audio/take1/, second takes in audio/take2/): a02, a18, a21 (Xu Yan's YIN
# pitch outside 96-148 Hz; three takes each, the closest kept: 149, 95, 98 Hz); a18 also read 紙 as 嘴 twice, and a08 (指甲縫),
# a10 (縣太爺), a31 (就在) read wrong syllables plain: retaken once from a scratch copy of video.json with a pinyin hint for the
# one word (TTS input only; video.json and the subtitles keep the characters). 41 TTS calls, none reported a charge.
# 5 s: the silent inserts s04, s09, s22, s29, s35 as gen-dh buys them, and the silent close-up s10 (one look; gen-dh reads the
#      ";" of its motion as two beats and would buy 6). s26 (a glide and a stop) keeps gen-dh's 6.
# No shot runs over about 10 s, so nothing is split.
BUY = {"s06": 8, "s16": 8, "s19": 8, "s21": 8, "s37": 8, "s10": 5}


# ---- the refine text (e022 review 必改 12, as e023-e026): hailuo/clips-dh-e927.json column 0 is the motion text
# refine-prep.py sends with a picked d1 draft. gen-dh.mjs opens every clip that lists tangxiaotang with the CG-era "Tang
# Xiaotang's high stand-up collar stays closed at her throat." and names her in "<names> shown in <Picture 1>"; in a back shot
# that draws the collar back and turns her face to the lens. Her only shot (s05) is a back shot: the sentence goes and her
# name becomes "the young woman seen only from behind". build-r2.py's speaking clause names Zhao Butou "Constable Zhao" (bible
# rule 17: no word for his office): the refine text says "Zhao Butou". Column 1 is recomputed.
COLLAR = "Tang Xiaotang's high stand-up collar stays closed at her throat. "
BACK_NAME = "the young woman seen only from behind"


def live_clips(path):
    import hashlib
    import json
    import re
    clips = json.load(open(path, encoding="utf-8"))
    for key, row in clips.items():
        text = row[0]
        if COLLAR in text:
            text = text.replace(COLLAR, "")
            m = re.search(r"\[Shot 1\] 3D CG\. (.+?) shown in <Picture 1> (keeps?) ", text)
            names = [n for n in m.group(1).split(" and ") if n != "Tang Xiaotang"]
            who = " and ".join(names + [BACK_NAME])
            who = who[0].upper() + who[1:]
            verb = "keep" if names else "keeps"
            text = text.replace(m.group(0), f"[Shot 1] 3D CG. {who} shown in <Picture 1> {verb} ", 1)
            assert "Tang Xiaotang" not in text, (key, "her name is left in a back shot's refine text")
        text = text.replace("Constable Zhao", "Zhao Butou")
        assert "stand-up collar" not in text and "onstable" not in text, key
        row[0] = text
        row[1] = hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]
    open(path, "w", encoding="utf-8").write(json.dumps(clips, ensure_ascii=False, separators=(",", ":")))


if __name__ == "r2spec":
    import atexit
    import os
    atexit.register(live_clips, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "hailuo", f"clips-dh-e{EP}.json"))
