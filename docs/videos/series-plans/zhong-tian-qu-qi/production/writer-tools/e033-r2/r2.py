"""Episode 33 remake (r2): the writer spec for ../e001-r2/build-r2.py. Source: docs/videos/zhong-tian-qu-qi-e033-r2/script.md
(c01-c40; the CG-era r2 script), including its sections 「這版改了什麼」 and 「2026-11-06 審稿後的修改」, which override the tables.
Every line is the script's, word for word; only the staging changes. 40 shots, one per script shot (s01-s40 = c01-c40).
Bible: production/r2-bible-e031-e040.md (arc 4 〈旱年〉: rules 1-43, 〈場景〉, 〈接點〉 32->33 and 33->34, the props, people,
〈小角色〉 and 原版必修 tables; 〈還沒解決的〉 8: the geomancer is a minor role with no portrait, far and side-on only) and
r2-bible-e011-e060.md (accounts: no affection change this episode; Tang Xiaotang 42, Qin Shuang 41, A-ling 32; the drought
quest's third night 「剩七日」 and tenth day 「今日到期」; the sugar for thirty jin of iron nails). The third episode of arc 4: the
ancestral hall at dusk (the same moment as e032 s37) and that night, the deep pool with the half-built waterwheel on the
fourth day, the finished wheel on the tenth morning and at noon.

Written from the start the way e032-r2/r2.py stands AFTER its independent review and its live production (e032-live fix1-fix3,
REVIEW 3), with the task file's lessons:
- OFFSCREEN_SPEECH = False (rule 15): every shot with an off-screen line, a thought or a system line writes the silence of
  each face on screen (quiet(), SILENT_HE).
- Rule 31: a line said to someone outside the frame is written "toward someone out of sight beyond the left/right edge of the
  frame", that side set only all the way to the edge, and the speaker the only person in the frame (off()); GAZE_REFINE puts
  the same direction into the refine text. Nobody who is not in the first frame is named or described anywhere. A look at a
  place names the place (the tablets, the beam, the wheel, the worksite, the field edge). Over-the-shoulder foregrounds are
  unnamed backs with no picture (rule 2).
- e032 fix3 (the mud drawn as gold-leaf flakes): no mud this episode; nothing is written "caked" or "yellow mud", and no
  person stands lit by orange light with anything smeared on him. Xu Yan's knees are not written dirty (e032's XU_PALE had
  "dried yellow mud on its knees"; XU_HALL drops it).
- e032 fix2 (the hook that did not read: the hoe handle and the carrying pole drawn as one long stick): the long things of this
  episode (the beam, the rope, the ladder, Qin Shuang's bamboo pole, the sluice rope) are never written touching another long
  thing in the first frame; the episode's hook, the wheel turning half a turn and stopping (s34), is a static side-on wide of
  the whole wheel with the result written first, so the half turn and the stop are readable; the sluice (s33) is side-on too.
- e932 cut review (the white-bearded old villager next to Elder Han in e032 s36 reads as a second Elder Han): from this
  episode on the old village man wears a cloth head wrap and a short grey beard (CT_VILLAGERS, BANK).
- Background people are written with what their hands hold (rope, torch, plank, nothing), never a weapon word; no negated
  noun anywhere (rule 18: a negated noun is drawn).
- Tang Xiaotang (rule 40): she speaks once on screen (s17) from close behind, in the middle of the frame, head still, exactly
  two round buns (TBACK, alone(); nospeak; the spec drops her pictures); s19 her back is an unnamed soft shoulder at the frame
  edge and her line is a recording. No front face this episode. Her l1 costume (rule 4), never the t2 high collar.
- Qin Shuang (bible 〈人物〉, rule 5): her chopper is NOT written; scene 2 a bare bamboo pole (rule 33: the script's 「素色布旗」
  is dropped) and the stitched booklet (rule 38: plain grey cover, closed); scene 3 her hands empty.
- Wang Erniu: not smiling in every shot (brows knotted, jaw set) except s24, the script's laugh; scene 2 one wooden mallet.
- The geomancer (〈小角色〉, 〈還沒解決的〉 8): no portrait, never named, never a front close-up: s19 far on the field edge
  behind Qian Yuanwai (Qian in front), s20 a side-on medium of him alone (the script's frontal 「中景正面」 changes), s21 and
  s25 a cut-off sleeve and shoulder at the frame edge; his voice is MINOR (Charon), a recording (his line is 「畫外」 for TTS).
  Thin and long-faced, so Qian Yuanwai stays the only portly round face (同框撞臉).
- One visible action per shot (rule 32); the previous action done in the first frame; the hand's action in a frame where it
  is seen; hand gestures with the flat hand, fingers together. The script's follows and tracks are slow push-ins; the wheel's
  half turn (s34) is static. No word "open" (rule 36: the sluice gate "is pulled up", the sack's neck "untied"). Nothing hung
  (rule 33). Paper is plain and edge-on or rolled (rule 38): the waterwheel roll "its outside plain", the sheets on Xu Yan's
  table face down, the charcoal lifted above the paper.
- 原版必修 e033 (bible): the waterwheel looked different in every shot -> only set-shentan-gongdi-l2 (scene 2) and set-shentan-l3
  (scene 3) and their free crops are sent, and the text says "the water wheel exactly as in the picture" with only its paddle
  count. The independent review (writer-tools/e033-r2/review-independent.md 必改 1) found set-shentan-l1's wheel has NO paddles
  while eleven prompts and the lines need twelve: option A was taken, set-shentan-l2 = set-shentan-l1 with twelve flat wooden
  paddles on the rim (one Qwen-Image-Edit, colab/runs/e933-live/shentan-l2/, seed 9331205), and l3 its free clean. 原版建議: the pinwheel is four plain white paper vanes on a thin bamboo stick; Xiaohe is eight; the ending is not three
  laughing shots (s35-s38 the stop, s39-s40 Qian Yuanwai).
- No blue light (rule 11): s08, s16, s30's panels and system lines are the editor's; the script's 「臉被面前的淡藍光照亮」 is not
  written.

THE AXES (rules 29, 42: the pictures decide):
- Scene 1, the ancestral hall (set-citang-huang-l1 at dusk s01-s04; the free night version set-citang-ye2-l1 from s05): the pair
  of lattice doors on the LEFT, the altar table with five plain tablets, the censer and two candles along the back wall on the
  RIGHT, the dark main beam across the top of the back wall. e032 s36-s37 as cut (zhong-tian-qu-qi-e932-dh/cut/e932-live.mp4,
  203-218 s): s36 the wide at chest height, Xu Yan standing in the doorway at the left, Elder Han kneeling in the middle by the
  altar turned back to him, the eight villagers kneeling in the right half, their faces toward the doorway; s37 Xu Yan in the
  doorway, waist up, the roll held across his waist in his right hand, fading out. s01 keeps s36's camera and picks him up one
  step inside the doorway. Kneeling before the altar everyone faces the back wall, so the faces are shot side-on from the
  table's LEFT END (-huang-zuo, -huang-zuo2, as e032 s34-s35): the speaker looks screen RIGHT at the tablets. The beam comes down
  at night: the rope crew at the left toward the doorway, the beam's far end at the right by the wall; Carpenter Shi and Xu Yan
  crouch over the lowered beam, Xu Yan at the LEFT (doorway side), the carpenter at the RIGHT (altar side) in s09-s11.
- Scene 2, the deep pool on the fourth day (set-shentan-gongdi-l1, round 5, 37045, the same pond and camera as set-shentan-l1
  with the wheel taken away): the camera stands at the near stone edge of a round pond of still green water; two tall wooden
  frames stand at the pond's far edge, the low one at the left with a rope slanting down from it, the tall one at the right with
  a long top beam; a bare round wooden axle on a small wooden trestle in the water between them; stone steps and a small wooden
  landing at the LEFT; a big grey boulder on the stone edge at the RIGHT; a pile of long cut timbers on the bank at the right
  behind the boulder; a flat sandy bank beyond, dry furrowed fields to the horizon. So the worksite and the men are on the bank
  at the LEFT (-gongdi-an), Qin Shuang stands on the boulder at the RIGHT facing screen left, the timbers and Carpenter Shi at
  the right (-gongdi-mu), the field edge where Qian Yuanwai and the geomancer stand is far at the RIGHT beyond the tall frame
  (-gongdi-geng). The script's 「潭在右、岸在左」 holds; its 「田埂在右上」 is the field edge beyond the right frame.
- Scene 3, the tenth day (set-shentan-l3: set-shentan-l1 of round 3, 37041, with twelve flat wooden paddles added by one edit,
  set-shentan-l2, then the low frame's rope, the pylon and the horizon poles painted out for free): the same camera with the
  whole wheel standing in the pond against the far stone edge, left of the middle, its axle on the trestle, eleven paddles in
  sight and the twelfth behind the trestle in the water. The sluice of the script is written at the LEFT, at the narrow gap in
  the stone edge by the steps and the landing (-an); the villagers stand on the stone edge at the left; the wheel is to their
  right (-bian: the stone edge at the left, the near rim and paddles at the right; -lun: the wheel's lower half); Qian Yuanwai
  and two retainers on the field edge far at the right (-geng). Dawn s28-s30 gets the free grey-gold grade (-chen, -chen-bian,
  -chen-an), noon s31-s40 the picture as it is.

PLACES (gen-dh SET takes the FIRST pattern in its list order that matches; spec.json will swap with absolute paths):
- "ancestral hall" (scene 1) gives dh-set-citang-t1 (pilot.py's set-citang-l1, never sent), swapped at dusk for the free
  set-citang-huang-l1 (s01) and its crops -huang-zuo2 (s02), -huang-liang (s03), -huang-zuo (s04); at night for the free
  set-citang-ye2-l1 (s05; citang_ye_clean.py: set-citang-ye-l1 with the beam's crack strokes painted out as citang_huang.py
  does) and its crops -ye2-men (s06, s08, s10), -ye2-tang (s09), -ye2-qiang (s07, s11: the plain candle-lit wall right of the
  beam and above the tablets; the review's 必改 4: -huang-qiang has the beam in its top-left corner).
- "deep pool" (scenes 2 and 3) gives dh-set-shentan-t1 (pilot.py's newest set-shentan, l3). Scene 2 swaps it for
  set-shentan-gongdi-l2 (s12; set-shentan-gongdi-l1 with the pylon and the horizon poles painted out) and its free crops
  -gongdi-an-l2 (s14, s16, s22, s24, s26), -gongdi-mu-l2 (s13, s17, s18), -gongdi-tian-l2 (s15, s23; the insert s27 as the colour
  of the sky only), -gongdi-geng-l2 (s19, s20, s21, s25); scene 3 keeps set-shentan-l3 (s34) and sends its free crops -an-l3
  (s31, s32, s33, s36, s37), -bian-l3 (s35), -lun-l3 (s38), -geng-l3 (s39), -tian-l3 (s40), and at dawn -chen-l3 (s28),
  -chen-an-l3 (s29), -chen-bian-l3 (s30) (shentan_clean.py + shentan_l3.sh).
No "sluice" or "channel" ahead of "deep pool" in any prompt (gen-dh's dh-set-xinqu-t1); "deep pool" opens every pool LOC.
Shared files: none changed (build-r2.py's EN has every speaking name; the geomancer never speaks on screen, so he needs no EN
entry; gen-dh.mjs, pilot.py, cast.json untouched; his voice is MINOR). The d1 prep (colab/runs/e933/extras.json,
colab/runs/e933-live/{mkspec.py,spec.json}, the scratchpad's prep933.sh, rec933.sh and e933d1.sh) was written 2026-11-19
(colab/runs/e933-live/PREP.md).
"""
EP = 933  # internal working number; the published slug is zhong-tian-qu-qi-e033-r2
SLUG = "zhong-tian-qu-qi-e033-r2"
EP_TITLE = "祠堂的梁（重製版 r2）"
OUTLINE_SECONDS = 222  # script.md: about 222.5 s, 40 shots (11 + 16 + 13)
TARGET_MINUTES = [3, 4]
TITLE = "拆了祠堂的梁，水車只轉半圈｜種田娶妻打天下 第33集（重製版）"
DESCRIPTION = "許硯跪在柳溪的牌位前：向祖宗借這根梁，三年之內還一座新的。韓伯跪到他身邊：祖宗要怪，就怪老頭子。當夜火把下，梁放了下來——系統：剩七日。石木匠說七天做不出兩丈高的輪子，許硯說：我畫一片，你做一片。第四天，秦霜照許硯寫的冊子把壯丁分成三班，唐小棠拿糖坊的糖換回三十斤鐵釘；錢員外帶來的風水先生在田埂上喊「拆祠堂，遭天譴」，大家都停了手，小禾跳上木頭：「祖宗也口渴！水來了，祖宗先喝！」第十天清晨，最後一根木栓敲進去，水車立起來了。正午開閘，水打在葉板上，輪子嘎吱轉了半圈——停住了。田埂上，錢員外笑到岔氣——《種田娶妻打天下》第 33 集（重製版）。"
THUMB = ("祖宗也口渴！", "s23")
CHARACTERS = ["xuyan", "hanbo", "shimujiang", "erniu", "qinshuang", "tangxiaotang", "xiaohe", "qianyuanwai", "fengshui", "xitong"]
# 〈小角色〉 (bible): the geomancer has no portrait and no on-screen speech; only his voice (Charon, the bible's choice).
MINOR = {
    "fengshui": {"id": "fengshui", "name": "風水先生",
                 "appearance": "East Asian man of about fifty, tall and thin with a long narrow face and a thin grey goatee, a plain mustard-yellow long robe with wide sleeves and a plain black cloth cap, one round wooden compass in his right hand",
                 "voice": {"provider": "gemini", "name": "Charon", "style": "標準國語，咬字清楚，台北人平常說話的語調；五十歲的江湖風水先生，男聲、尖細、拖長音、裝神弄鬼，喊話時一個字拉得老長"}},
}
MUSIC = "one cue per scene: a deep low cello in a candle-lit ancestral hall at dusk, one heavy note on a vow of three years, then a low steady work chant rhythm of drums as a great roof beam is lowered by torchlight at night; then a bright lively work tune by a deep green pond under a hot sun, dropping to an eerie wooden-block motif under a geomancer's warning and back to the bright tune on a burst of laughter; then quiet strings at a grey-gold dawn, drums building as a sluice is pulled at noon, everything cutting to silence but one long wooden creak as a waterwheel stops; ancient Chinese rural drama, no vocals"

# Places.
C0 = "In the ancestral hall of Liuxi village at dusk on the third day of the drought"
CANDLE = "warm candlelight inside the hall, the last dim orange evening light through the lattice of the doors"
C1 = "In the ancestral hall of Liuxi village late that night"
TORCH = "warm candlelight and the wavering orange light of burning pine torches inside the hall, the night blue-black beyond the lattice of the doors"
TABLETS = "five small dark wooden tablets standing on it, their faces smooth and plain"
ALTAR = f"the long dark altar table against the wall with {TABLETS}, a bronze censer with a few incense sticks and two white candles"
D0 = "At the deep pool on the flat dry fields of Liuxi on the fourth day of the drought"
SUN = "bright hot midday sun high in a pale clear sky, short shadows"
E0 = "At the deep pool on the flat dry fields of Liuxi at dawn on the tenth day of the drought"
DAWN = "soft grey-gold dawn light, a thin pale mist lying low on the water, the air still"
E1 = "At the deep pool on the flat dry fields of Liuxi at noon on the tenth day of the drought"
NOON = "harsh white noon sun high overhead in a pale clear sky, short hard shadows"
POOL = ("a round pond of still deep green water edged with rough fieldstones in the foreground, two tall wooden frames standing "
        "at its far edge, stone steps and a small wooden landing at the left, a big grey boulder on the stone edge at the right, "
        "a flat sandy bank beyond, dry furrowed fields to the horizon")
GONGDI = f"the pool exactly as in the picture: {POOL}; between the frames a bare round wooden axle resting on a small wooden trestle in the water, and a pile of long cut timbers on the bank at the right behind the boulder"
WHEEL = "the big wooden water wheel exactly as in the picture, standing in the pond against the far stone edge, its twelve flat wooden paddles round its rim"
LOC = {
    "ct": f"{C0}: the hall exactly as in the picture: the pair of lattice doors swung back on the left with a dim passage and another lattice door glowing with the last orange dusk light beyond them, {ALTAR} on the right, the thick dark main beam across the top of the back wall, a floor of grey flagstones; {CANDLE}",
    "ct_z": f"{C0}, at the left end of {ALTAR}; {CANDLE}",
    "ct_l": f"{C0}, under the thick dark main beam across the top of the candle-warmed back wall; {CANDLE}",
    "ye": f"{C1}: the hall exactly as in the picture: the pair of lattice doors swung back on the left with a dark passage and another lattice door beyond them, blue-black with the night, {ALTAR} on the right, the thick dark main beam across the top of the back wall, a floor of grey flagstones; {TORCH}",
    "ye_men": f"{C1}, near the doorway, the lattice door leaves swung back, beyond them a dark passage and another lattice door, blue-black with the night; {TORCH}",
    "ye_q": f"{C1}, before the plain candle-warmed back wall; {TORCH}",
    "ye_t": f"{C1}, on the grey flagstone floor before {ALTAR}; {TORCH}",
    "gd": f"{D0}: {GONGDI}; {SUN}",
    "gd_c": f"{D0}, on the flat sandy bank by the half-built frames of the waterwheel; {SUN}",
    "gd_g": f"{D0}, on the edge of the dry furrowed field beyond the pool; {SUN}",
    "gd_e": f"{D0}; {SUN}",
    "ch": f"{E0}: the pool exactly as in the picture: {POOL}, and {WHEEL}; {DAWN}",
    "ch_c": f"{E0}, on the stone edge of the pond beside {WHEEL}; {DAWN}",
    "nn": f"{E1}: the pool exactly as in the picture: {POOL}, and {WHEEL}; {NOON}",
    "nn_c": f"{E1}, on the stone edge of the pond beside {WHEEL}; {NOON}",
    "nn_g": f"{E1}, on the edge of the dry furrowed field beyond the pool; {NOON}",
}
LIGHT = {
    "dusk": "the warm candlelight and the dim dusk at the doors stay unchanged",
    "night": "the warm candle and torch light and the dark night at the doors stay unchanged",
    "sun": "the bright midday light stays unchanged",
    "dawn": "the soft grey-gold dawn light stays unchanged",
    "noon": "the harsh white noon light stays unchanged",
}
# bible rule 15: no "<X> speaks off screen" / "the system voice speaks off screen".
OFFSCREEN_SPEECH = False

# Repeated wording (each prop is one object, written the same way every time).
XU_HALL = ("Xu Yan, in his faded blue-grey scholar's robe patched at one elbow, its sleeves rolled up to the elbows, his face pale "
           "and tired")  # e032 XU_PALE without "dried yellow mud on its knees" (e032 fix3)
XU_UP = "Xu Yan, in his faded blue-grey scholar's robe patched at one elbow, its sleeves rolled up to the elbows"
XU_WORN = ("Xu Yan, in his faded blue-grey scholar's robe patched at one elbow, its sleeves rolled up to the elbows, dark shadows "
           "under his eyes and a short dark stubble on his jaw after seven short nights")  # bible 〈人物〉: e033-e034
ROLL = "one rolled sheet of plain cream paper, its outside plain"  # rule 38: the waterwheel drawing, never its face
HAN = ("Elder Han, in his faded grey cotton cross-collared long robe, his long white beard down to his chest, his white hair in a "
       "small topknot, his polished old bamboo walking staff in his right hand")
HAN_NOSTAFF = ("Elder Han, in his faded grey cotton cross-collared long robe, his long white beard down to his chest, his white "
               "hair in a small topknot")
STAFF_LEANING = "his bamboo walking staff leaning against the end of the altar table"
CARP = ("Carpenter Shi, in his faded light tan cross-collared short work jacket with the sleeves rolled up and his worn brown "
        "leather apron, one plain wooden stick through his grey topknot")  # e032 (the portrait; light tan, rule 12)
CARP_WORN = f"{CARP}, his eyes red-rimmed and tired, his grey stubble grown rough"  # bible: seven nights without sleep
ERNIU = "Wang Erniu, in his coarse brown cross-collared short jacket with the sleeves rolled up, his face tanned dark from the sun"
QIN = ("Qin Shuang, in her fitted dark brown cross-collared short jacket cinched with a wide plain black leather belt, black "
       "trousers and leather boots, her high ponytail tied with black cord")  # e030's wording; no chopper (rule 5)
BAMBOO = "one long plain bamboo pole a little taller than she is, bare from end to end"  # rule 33: the script's cloth flag is dropped
BOOKLET = "one thin stitched booklet with a plain grey cover, closed"  # rule 38
XIAOHE = ("little Xiaohe, an eight-year-old girl in her patched lilac cotton jacket, her two little pigtails tied with red string, "
          "one front tooth missing, a small woven straw rabbit tucked into the cloth sash at her waist")
PINWHEEL = "a little pinwheel of four plain white paper vanes on a thin bamboo stick"  # bible 〈道具〉
QIAN = ("Qian Yuanwai, short and portly with a round face and a thin eight-shaped moustache, in his dark gold silk robe woven "
        "with small round medallions, the front of the robe plain brocade, three gold rings on his fingers")
FENG = ("a tall thin man of about fifty with a long narrow face and a thin grey goatee, in a plain mustard-yellow long robe with "
        "wide sleeves and a plain black cloth cap")  # the geomancer: never named, no picture (〈小角色〉)
COMPASS = "one round wooden compass, its face a plain dark disc with one thin needle"  # bible 〈道具〉
MALLET = "one wooden mallet with a plain wooden handle"
SACK = "one bulging brown hemp sack tied at the neck"
NAILS = "a handful of long dark iron nails"
LADDER = "one plain wooden ladder"
ROPE = "one thick hemp rope"
TORCHES = "each holding one burning pine torch high in one hand"
SLUICE = "a small wooden sluice gate of three plain wet planks set upright in the narrow gap of the stone edge, one thick rope tied to its top"
HANDS = "their hands hold only what is described here"
SILENT_HE = "He says nothing in this shot: his lips stay pressed together from the first frame to the last, his jaw still, no talking, no mouthing words"
NOBODY = "Throughout the shot the set layout stays as it is. The pictures fix the place and the objects only, never the mood. "
# rule 34 (e032 CT_VILLAGERS; e932 cut review: the old man no longer white-haired with a long beard, so he is not a second Elder Han)
CT_VILLAGERS = ("eight more people in Song-dynasty cross-collared homespun jackets and cloth shoes, each a different colour: a bent "
                "old woman in a faded deep plum jacket with a white head cloth, an old man with a short grey beard and a faded "
                "undyed hemp-beige jacket and head wrap, a middle-aged woman in a dark grey jacket with a faded indigo head cloth, "
                "a broad middle-aged man in a dull olive-green jacket, a young woman in a rust-red jacket, a boy of about ten in a "
                "mustard-yellow jacket, a girl of about seven in a faded green jacket with her hair in one small bun, and a lean "
                "middle-aged man in a dark charcoal jacket")
# the rope crew at night (s05, s06): three grown villagers on the rope with Erniu, two holding the torches
ROPE_MEN = ("three more men in Song-dynasty cross-collared homespun jackets, cloth head wraps and cloth shoes, both hands of each on "
            "the rope: an old man with a short grey beard in a faded undyed hemp-beige jacket, a broad middle-aged man in a dull "
            "olive-green jacket and a lean middle-aged man in a dark charcoal jacket")
TORCH_WOMEN = ("two women in Song-dynasty cross-collared homespun jackets and cloth shoes, a middle-aged woman in a dark grey jacket "
               "with a faded indigo head cloth and a young woman in a rust-red jacket, " + TORCHES)
BEAM_MEN = ("two more men in Song-dynasty cross-collared homespun jackets and cloth head wraps, a big man in a dark wine-red jacket "
            "and a young man in a faded green jacket")
# rule 34, scene 2 (bible 〈小角色〉: three gangs, each with its own head-wrap colour: grey, faded indigo, earth-yellow)
WORKERS = ("nine men in Song-dynasty cross-collared homespun short jackets and cloth shoes, each a different colour and age, in "
           "three loose groups by the colour of their cloth head wraps: grey head wraps on a lean young man in a rust-red jacket, "
           "a stocky middle-aged man in a dull olive-green jacket and an older man with a short grey beard in a faded undyed "
           "hemp-beige jacket; faded indigo head wraps on a broad young man in a dark charcoal jacket, a thin man of about thirty "
           "in a faded green jacket and a short middle-aged man in a dark ochre jacket; earth-yellow head wraps on a tall young man "
           "in a dark teal jacket, a wiry middle-aged man in a deep wine-red jacket and a young man of about twenty in a faded "
           "sand-coloured jacket")
TWO_WORKERS = ("two more men in Song-dynasty cross-collared homespun short jackets and grey cloth head wraps, a lean young man in a "
               "rust-red jacket and a stocky middle-aged man in a dull olive-green jacket, one long cut timber held level between them")
SIX_WORKERS = ("six more men in Song-dynasty cross-collared homespun short jackets, cloth head wraps and cloth shoes, each a different "
               "colour: a lean young man in a rust-red jacket, a stocky middle-aged man in a dull olive-green jacket, a broad young man "
               "in a dark charcoal jacket, a thin man in a faded green jacket, a tall young man in a dark teal jacket and a wiry man in "
               "a deep wine-red jacket, their hands empty")
# scene 3, the bank at noon: six of the hall's villagers (e033 CT_VILLAGERS)
BANK = ("six more people in Song-dynasty cross-collared homespun jackets and cloth shoes, each a different colour, their hands empty: "
        "a bent old woman in a faded deep plum jacket with a white head cloth, an old man with a short grey beard and a faded "
        "undyed hemp-beige jacket and head wrap, a middle-aged woman in a dark grey jacket with a faded indigo head cloth, a broad "
        "middle-aged man in a dull olive-green jacket, a young woman in a rust-red jacket and a lean middle-aged man in a dark "
        "charcoal jacket")
RETAINERS = ("two men in identical Song-dynasty black cross-collared short jackets, black cloth head wraps and cloth shoes, their "
             "hands empty at their sides")
# rule 40 (e031 TBACK): Tang Xiaotang from behind, her l1 costume (rule 4)
TBACK = ("one young woman seen only from behind, appearing only once: the back of her head with every strand of her black hair "
         "combed smooth and gathered up into just two round buns set high on her head, one bun on each side, one short pink "
         "silk ribbon wrapped around each bun, the nape of her neck bare and clear above a pink inner collar, and her light "
         "peach-pink silk shoulders; the back of her head facing straight away from us the whole time, her head still, her ear "
         "the furthest round her head we ever see")
HEADSTILL = "the young woman with the two high round buns keeps her head still, facing straight away from us, the back of her head toward us the whole shot"
TANG_EDGE = ("at the lower left edge of the frame, cut by it, soft and out of focus, only the back of a young woman's head with two "
             "round buns tied with short pink silk ribbons and one light peach-pink silk shoulder, toward us the whole shot")
# rule 2: over-the-shoulder backs, unnamed, no picture
BACK_XU = ("at the left edge of the frame, cut by it, soft and out of focus, only the back of one shoulder in a faded blue-grey "
           "robe and the back of a man's topknot, toward us the whole shot")
BACK_CARP = ("at the right edge of the frame, cut by it, soft and out of focus, only the back of one shoulder in a faded light tan work "
             "jacket with the strap of a leather apron across it and the back of a grey topknot with one plain wooden stick through "
             "it, toward us the whole shot")
FENG_EDGE_L = ("at the left edge of the frame, cut by it, soft, only one wide mustard-yellow sleeve and shoulder of a tall thin man "
               "standing just behind him")
FENG_EDGE_R = ("at the right edge of the frame, cut by it, soft, only one wide mustard-yellow sleeve and shoulder of a tall thin man "
               "standing one step behind him")  # bible 〈小角色〉: Qian Yuanwai in front; he faces left, so behind him is the right
# set-only sides (the picture of each place, all the way to the edge)
SIDE_DOOR = "the dark lattice door leaf swung back against the wall"
SIDE_WALL = "the candle-warmed back wall of the hall"
SIDE_BANK = "the flat sandy bank and the dry furrowed field"
SIDE_SKY = "the pale clear sky"
SIDE_FRAME = "the tall wooden frame of the waterwheel"
SIDE_STONE = "the rough fieldstone edge of the pond and the still green water"
SIDE_WHEEL = "the wet wooden spokes and paddles of the wheel"
SIDE_STONE_RIM = "the rough fieldstone edge of the pond, the green water and the near rim of the still wheel at the very edge"


def quiet(who, pr="his", plural=False):
    verb = "say" if plural else "says"
    return f"{who} {verb} nothing in this shot: {pr} lips stay pressed together from the first frame to the last, no talking, no mouthing words"


def off(side, what, he="he"):
    """A line to someone outside the frame: the gaze, that side set only, and the only person (rule 31)."""
    edge = f"the {side} edge of the frame"
    return (f"toward someone out of sight beyond {edge}, never the lens; that side of the frame is only {what} all the way to the "
            f"edge, and {he} is the only person in the frame")


def only_tang():
    return "she is the only young woman with two high round buns in the frame"


def alone(rest, where, frame="framed from the waist up", shot="medium shot", lead=""):
    """Tang Xiaotang from behind, in the middle of the frame (not at an edge: the pickers' cheek at the frame edge)."""
    return f"{shot} from close behind{lead} {TBACK}, {where} in the middle of the frame, {frame}, facing straight away from us; {only_tang()}; {rest}"


SHOTS = [
    # ---- scene 1: the third day of the quest at dusk, the ancestral hall (32->33: the same moment as e032 s37), then night.
    dict(chapter="柳溪祠堂，黃昏到當夜", loc="ct", cam="Wide shot, slow push in", chars=["xuyan", "hanbo"], night="dusk", act=3,
         comp=f"wide shot at about chest height, level, like the picture: at the left, already one step inside the doorway from the first frame, {XU_HALL}, framed full figure, {ROLL} held across his waist in his right hand, his face toward the altar at the right, never the lens; grave and quiet, not smiling: brows level, eyes steady, lips pressed shut; kneeling in two loose rows on the grey flagstones in the lower right foreground, the nearer row cut at the knees by the bottom of the frame, {CT_VILLAGERS}, their hands resting on their knees, their faces turned toward him, their lips closed, never the lens; kneeling in the middle of the floor in front of them {HAN_NOSTAFF}, framed full figure, {STAFF_LEANING}, his face turned back over his shoulder toward Xu Yan, his lips pressed shut, never the lens; {HANDS}; exactly ten people",
         motion=f"Xu Yan walks slowly across the hall toward the altar at the right, and the kneeling people's heads turn to follow him; {quiet('Everyone in the frame', 'their')}",
         zh="全景、慢推（人眼高、照圖；送 `set-citang-huang-l1`，接點 32→33：**照第 32 集 s36–s37 實拍**（`e932-live.mp4` 203–218 秒）：s36 胸口高的全景，門在左、韓伯跪在中間回頭、八個村民跪在右半邊臉朝門口；s37 許硯在門口、圖卷橫在腰前右手拿著、淡出）：第一格許硯已經跨進門檻一步（稿子『從門口走進來』的前一半在第一格完成），右手圖卷橫在腰前（照 s37）；往右穿過大廳朝供桌走，跪著的人頭一個個跟著轉；韓伯跪在大廳中間、村民前面（獨立審稿建議 11：照第 32 集 s36 實拍，不在供桌邊），竹杖靠在供桌邊（接第 32 集 c34）、回頭看他。村民照第 32 集祠堂那八人、兩手放在膝上（同 s36 實拍），**白鬚老漢改成布包頭、短灰鬚**（e932 審片：跟韓伯撞）。稿子『把圖卷放在膝前、雙膝跪下』留給 s02 第一格（一鏡一個動作）；跟拍改慢推。沒有人說話"),
    dict(loc="ct_z", cam="Close-up, slow push in", chars=["xuyan"], night="dusk",
         comp=f"close-up of {XU_HALL}, kneeling on the grey flagstones at the left end of the altar table, side-on to us, framed from the chest up with space above his head, both hands already pressed together before his chest from the first frame, his right fist folded in his left palm, his face three-quarter to screen right toward the row of plain tablets on the altar table, his eyes on them, never the lens; that side of the frame is only the left end of the altar table, one white candle and the plain tablets all the way to the edge, and he is the only person in the frame; solemn, not smiling: candlelight on his face, brows level, eyes steady, lips moving slowly, one word at a time; behind him at the right, soft, one white candle, two plain dark wooden tablets, their faces smooth and plain, and the bronze censer; {HANDS}",
         lines=[("xuyan", "列位祖宗，晚生許硯，向柳溪借這根梁。", "一字一頓")],
         motion="Xu Yan raises his pressed-together hands slowly to his brow as he speaks",
         zh="近景、慢推（送 `set-citang-huang-zuo2-l1`：供桌左端、一支白蠟燭、兩塊素面牌位、香爐）：許硯第一格已經跪在供桌左端（側面，同第 32 集 s34–s35 韓伯的機位），右拳抱在左掌裡；兩手慢慢舉到額前，朝畫右的牌位一字一頓地說（答第 32 集 s36）。圖卷已經放在膝前地上（胸以上的框看不到，不寫）。稿子『抬頭看牌位』：臉本來就朝牌位"),
    dict(loc="ct_l", cam="Low-angle close-up, slow push in", chars=["xuyan"], night="dusk",
         comp=f"low-angle close-up of {XU_HALL}, kneeling, seen from just above the flagstones, framed from the chest up, his head just lifting from a deep bow from the first frame, his face tipping up toward the dark main beam above him, his eyes on it, never the lens; he is the only person in the frame; steady and resolved, not smiling: candlelight under his chin, brows level, lips moving firmly between words; above and behind him, soft and out of focus, only the thick dark main beam across the top of the candle-warmed back wall; {HANDS}",
         lines=[("xuyan", "水車造成，三年之內，我還柳溪一座新梁。", "很穩")],
         motion="Xu Yan lifts his head from the bow and looks up at the beam as he speaks",
         zh="低角度近景、慢推（送 `set-citang-huang-liang-l1`：牆頂那根深色主梁，裂紋已塗掉）：第一格許硯的頭剛從磕頭裡抬起來（稿子『磕下頭去、額頭碰地』在第一格前完成），抬頭看頭頂虛焦的梁、很穩地說（配樂在『三年』一個重音）"),
    dict(loc="ct_z", cam="Medium shot, slow push in", chars=["xuyan", "hanbo"], night="dusk",
         comp=f"medium shot at the left end of the altar table, both kneeling side by side on the grey flagstones, facing the altar at the right, seen three-quarter from the front left, framed from the waist up: nearer at the left {XU_HALL}, his face turning toward the old man beside him, his lips pressed shut, never the lens; quiet, not smiling; just beyond him at the right {HAN_NOSTAFF}, already shuffled close beside him on his knees from the first frame, {STAFF_LEANING}, his face three-quarter to screen right toward the plain tablets, never the lens; old and sure, not smiling: brows level, eyes on the tablets, lips moving slowly between words; beyond them, soft, the dark wooden post, the left end of the altar table, one white candle and the plain tablets in the candlelight; {HANDS}; exactly two people",
         lines=[("hanbo", "祖宗要怪，就怪我老頭子，別怪孩子們。", "慢，篤定")],
         motion=f"Elder Han bows his head slowly and deeply toward the tablets as he speaks; {quiet('Xu Yan')}",
         zh="中景（雙人、從左前三分之二側面）、慢推（送 `set-citang-huang-zuo-l1`：推開的門扇與深色柱子、供桌左端、蠟燭與牌位）：兩人並排跪在供桌左端、面向畫右的牌位，許硯在近的左邊、轉頭看韓伯、嘴閉著；韓伯第一格已經跪著挪到他右邊（稿子『跪著往左挪』在第一格完成：一鏡一個動作），竹杖靠在供桌邊，朝牌位慢慢磕下頭去、篤定地說"),
    dict(loc="ye", cam="Wide shot, slow push in", chars=["shimujiang", "erniu"], night="night",
         comp=f"wide shot at about chest height, level, like the picture, the beam at the top of the frame: against the back wall at the right, just beyond the right end of the altar table and clear of it, {LADDER} standing on the flagstones under the right end of the beam, and near its top {CARP}, framed full figure, already up on the ladder from the first frame, both hands pulling tight the knot of {ROPE} round the end of the beam, his face turned down over his shoulder toward the people below at the left, never the lens; gruff and loud, not smiling: brows knotted, lips moving hard between shouted words; from the beam the rope runs down and away to the left, where on the flagstones toward the doorway {ERNIU}, framed full figure, both hands on the rope, his face turned up toward the beam, his lips pressed shut, straining, not smiling, never the lens, and behind him {ROPE_MEN}, their lips closed, never the lens; at the left by the doorway {TORCH_WOMEN}, their lips closed, never the lens; the ladder stands well apart from the rope; {HANDS}; exactly seven people",
         lines=[("shimujiang", "繩套好了！都站開，梁要下來了！", "吼")],
         motion=f"Carpenter Shi gives the knot one last hard pull and shouts down; the four on the rope lean back and draw it taut; {quiet('Wang Erniu and the others', 'their', plural=True)}",
         zh="全景、慢推（照圖的高度與機位；送本集免費做的夜版 `set-citang-ye2-l1`（`citang_ye_clean.py`：`set-citang-ye-l1` 門外入夜、主梁裂紋照第 32 集塗掉））：**入夜**（時間跳在 s04→s05 這一刀）。石木匠在右邊後牆、供桌右端外側（不碰供桌，獨立審稿建議 6：原寫法木梯會立在供桌上，跟『別砸了供桌』打架）梁右端下的木梯上，把粗麻繩在梁頭最後一拉、回頭朝下吼；繩子從梁往左下拉到門那邊，二牛與三個村民（短灰鬚布包頭的老漢、暗橄欖綠、炭灰）握著繩子往後仰拉緊；門邊兩個婦人各舉一支松明火把（每支拿在一個人手裡，拍法 37）。稿子『低角度、從地上往上拍』照圖的機位（第 32 集審稿必改 3：照圖的高度）；『許硯、韓伯退到門邊』不入鏡（一鏡最多三張有名字的臉、人數讀得清）。木梯與繩子分開寫（第 32 集 fix2：長東西第一格不相連）"),
    dict(loc="ye_men", cam="Medium shot, slow push in", chars=["erniu"], night="night",
         comp=f"medium shot near the doorway, framed from the waist up: in front at the left {ERNIU}, both hands gripping {ROPE} that runs up and away beyond the upper right edge of the frame, already leaning back hard on it from the first frame, his face lifted three-quarter to screen right along the rope toward someone out of sight beyond the upper right edge of the frame, never the lens; straining and worried, not smiling: teeth gritted, brows knotted hard, lips moving hard between words; that side of the frame is only {SIDE_DOOR} all the way to the edge; behind him on the same rope, leaning back with him, {ROPE_MEN}, their lips closed, never the lens; behind them, soft, the dark lattice of the doors and the dark passage beyond them, blue-black with the night; {HANDS}; exactly four people",
         lines=[("erniu", "好沉的梁……許大哥，你那頭撐得住嗎？", "咬牙")],
         motion=f"the four of them let the rope out slowly hand over hand, their feet sliding a little on the flagstones and bracing again; {quiet('The three men behind Wang Erniu', 'their', plural=True)}",
         zh="中景、慢推（送夜版裁切 `set-citang-ye2-men-l1`：門口、格子門扇、門外的夜）：二牛在左前、三個村民在他身後同一條繩上，第一格已經往後仰著拉繩；四個人一手接一手慢慢放繩、腳底在青石地上一滑又站穩（剪在打滑那一下，照稿子〈剪接〉）；二牛臉順著繩子朝畫右上外看不到的人（梁另一頭的許硯，不點名）咬牙喊（自審：原寫『從右肩回頭』，但繩子往右上、他面向右，回頭會朝左，越軸），**不笑**（吃力）"),
    dict(loc="ye_q", cam="Medium shot, slow push in", chars=["xuyan"], night="night",
         comp=f"medium shot before the plain back wall, framed from the waist up: in the middle {XU_HALL}, already bent under the end of the thick dark beam from the first frame, its weight resting on his right shoulder, both hands braced under it, the long dark beam slanting up from his shoulder out of the upper right corner of the frame, his face three-quarter to screen right toward the two men beside him, never the lens; straining, not smiling: teeth gritted, brows knotted, lips moving hard between words; at the right, a step along the beam, {BEAM_MEN}, their shoulders under it, their lips closed, never the lens; behind them, soft, only the plain candle-warmed back wall with the wavering orange torchlight on it; {HANDS}; exactly three people",
         lines=[("xuyan", "撐得住！慢慢放，別砸了供桌！", "咬牙")],
         motion=f"the three of them sink slowly at the knees and lower the end of the beam toward the floor as Xu Yan speaks; {quiet('The two men beside him', 'their', plural=True)}",
         zh="中景、慢推（送本集免費做的 `set-citang-ye2-qiang-l1`：夜版主梁右下、牌位上方被燭光照暖的素牆，**沒有梁**（獨立審稿必改 4：原送的 `-huang-qiang` 左上角就是那根主梁，畫面會有兩根梁））：第一格梁的一頭已經壓在許硯右肩上（稿子『從梁壓到肩上開始』），兩個村民（深酒紅、褪色綠，不跟拉繩的人重複）一起頂著，長梁從他肩上斜出畫面右上角（獨立審稿建議 6：看得出是整根梁在往下放；木梯不入鏡）；三人膝蓋一彎、把梁頭慢慢往地上放，許硯咬牙喊。稿子『膝蓋一彎又撐住』與『放到地上』合成一個下沉的動作"),
    dict(loc="ye_men", cam="Close-up, slow push in", chars=["xuyan"], night="night",
         comp=f"close-up of {XU_HALL}, standing, framed from the chest up with space above his head, his hair damp and stuck to his forehead, his chest heaving, his eyes on the empty air before him at first, then his face turns three-quarter to screen right {off('right', SIDE_DOOR)}; spent but set, not smiling: brows drawn, lips pressed shut while he catches his breath, then moving firmly between words; behind him, soft, only the dark wooden door post and the lattice of the doors in the wavering orange torchlight; {HANDS}",
         lines=[("xitong", "叮。旱災任務，剩七日。", "冷，宣布"), ("xuyan", "石師傅，這水車得在七天之內立起來。", "喘，篤定")],
         panel=[("旱災任務，剩七日", "task")],
         motion="Xu Yan straightens up, panting, and turns his face toward the right edge of the frame to speak",
         zh="近景、慢推（送夜版裁切 `set-citang-ye2-men-l1`：深色門柱與格子門）：許硯直起腰、喘著，頭髮黏在額上（稿子『滿頭汗』寫成濕髮，拍法 12）；先嘴閉著聽系統（面板剪接時疊，**不寫淡藍光**，拍法 11），再轉頭朝畫右外看不到的人（石木匠，不點名）說。稿子『抹一把汗、看一眼面前的空氣、再轉頭』只留轉頭（一鏡一個動作）。長鏡"),
    dict(loc="ye_t", cam="Medium shot over the shoulder, slow push in", chars=["shimujiang"], night="night",
         comp=f"medium shot over a shoulder: {BACK_XU}; one step beyond it in the right half of the frame {CARP}, crouching on the flagstones beside the thick dark beam that lies along the floor, framed from the waist up, {ROLL} gripped in his left hand from the first frame, its outside toward us, his face three-quarter to screen left toward the man in the foreground, never the lens; disbelieving, not smiling: brows knotted, eyes narrowed, lips moving roughly between words; behind him, soft, the long dark altar table with the plain tablets and the two candles; {HANDS}; exactly two people, the one in the foreground seen only from behind",
         lines=[("shimujiang", "七天？兩丈高的輪子，十二片葉板，做不出來。", "不信")],
         motion="Carpenter Shi slaps his flat right hand down once on the beam as he speaks",
         zh="過肩中景、慢推（送夜版裁切 `set-citang-ye2-tang-l1`：供桌那一側與青石地）：前景左是虛焦的藍灰肩背與髮髻（不點名、不送圖，拍法 2）；石木匠蹲在放倒在地上的梁旁、左手握著圖卷（紙背朝外），右手平掌往梁上一拍、不信地說。稿子『把圖卷攤在梁上』改成握在手裡（拍法 27、38：攤開的紙會長出圖與字）"),
    dict(loc="ye_men", cam="Medium shot over the shoulder, slow push in", chars=["xuyan"], night="night",
         comp=f"reverse medium shot over a shoulder: {BACK_CARP}; one step beyond it in the left half of the frame {XU_HALL}, crouching on the flagstones by the thick dark beam that lies along the floor, framed from the waist up, his face three-quarter to screen right toward the man in the foreground, never the lens; calm and firm, not smiling: brows level, eyes steady, lips moving evenly between words; behind him, soft, the dark lattice of the doors and the dark passage beyond them, blue-black with the night; {HANDS}; exactly two people, the one in the foreground seen only from behind",
         lines=[("xuyan", "做得出來。你帶人做木工，我畫一片，你做一片。", "很穩")],
         motion="Xu Yan lays his flat right hand on the beam between them as he speaks",
         zh="反打過肩中景、慢推（送 `set-citang-ye2-men-l1`：反打的背景換成門那一側）：前景右是虛焦的淺褐肩背、皮圍裙帶與插木棍的灰髮髻（不點名）；許硯蹲在梁另一邊、平掌按在兩人中間的梁上、很穩地說。稿子『按住圖的一角、另一手的手指比一段長度』改一個平掌（單指會讀錯，拍法 32；圖在石木匠手上）"),
    dict(loc="ye_q", cam="Medium shot, slow push in", chars=["shimujiang"], night="night",
         comp=f"medium shot of {CARP}, already risen to his feet from the first frame, framed from the waist up, {ROLL} in his left hand, his face three-quarter to screen left {off('left', SIDE_WALL)}; weighing him up, not smiling: eyes narrowed to slits, jaw set, lips moving slowly between words; behind him, soft, only the plain candle-warmed back wall with the wavering orange torchlight on it; {HANDS}",
         lines=[("shimujiang", "好。做砸了，這根梁的帳，算在你頭上。", "瞇眼")],
         motion="Carpenter Shi grips the rolled paper hard and tucks it under his left arm as he speaks",
         zh="中景、慢推（送 `set-citang-ye2-qiang-l1`：沒有梁的素牆，獨立審稿必改 4）：石木匠第一格已經站起來（稿子『一把抓起圖卷站起來』的站起在第一格完成），瞇眼朝畫左外看不到的人（許硯，不點名）說，把圖卷一把夾到左腋下（第一場結尾）。稿子的近景改中景：手上的動作要看得見（拍法 32）"),
    # ---- scene 2: the fourth day, the deep pool with the half-built wheel (set-shentan-gongdi-l1).
    dict(chapter="深潭邊工地，第四日", loc="gd", cam="Wide shot, slow push in", chars=["qinshuang"], night="sun",
         comp=f"wide shot at standing eye height, like the picture: in the right foreground {QIN}, framed full figure, already standing on top of the big grey boulder at the pond's edge from the first frame, {BAMBOO} in her right hand, her face three-quarter to screen left toward the bank, never the lens; loud and bright, not smiling: brows level, eyes sharp, lips moving fast between words; on the flat sandy bank beyond the pond at the left, small, {WORKERS}, standing about here and there on the sand, their hands empty, their faces turned toward her, their lips closed, never the lens; {HANDS}; exactly ten people",
         lines=[("qinshuang", "全村壯丁聽好，從今天起，分三班！", "嗓門亮")],
         motion=f"Qin Shuang sweeps the bamboo pole once through the air above her head as she speaks, and the men fall still and look up; {quiet('The nine men', 'their', plural=True)}",
         zh="全景、慢推（人眼高、照圖；送 `set-shentan-gongdi-l2`（`set-shentan-gongdi-l1` 塗掉地平線的小電塔與細桿，獨立審稿建議 10）：潭在前景、兩座木架立在遠端潭邊、中間小木架上一根光禿的木軸、左邊石階與小木台、右邊潭邊大灰石、右岸一堆木料）：秦霜第一格已經站在右前的大石上（稿子『一步跳上大石』在第一格完成），右手一根光竹竿（**不綁旗**，拍法 33），竿子在頭上一揮、喊；左邊遠處沙岸上九個壯丁亂站著，安靜下來抬頭看她。壯丁照聖經〈小角色〉分三班：灰、褪色靛藍、土黃三種頭巾，每人衣色年紀不同、兩手空著（寫手上拿什麼）。推軌改慢推"),
    dict(loc="gd_c", cam="Medium shot, slow push in", chars=["qinshuang"], night="sun",
         comp=f"medium shot of {QIN}, standing on top of the big grey boulder at the pond's edge, framed from the knees up, {BOOKLET} in her left hand at her hip from the first frame, {BAMBOO} held upright in her right hand, its foot resting on the boulder by her boot, its top rising into the pale sky above her head, well apart from the timbers behind her, her face three-quarter to screen left {off('left', SIDE_BANK, he='she')}; brisk, not smiling: brows level, eyes quick, lips moving fast and clipped between words; behind her, soft, the pile of long cut timbers on the bank and the dry furrowed field in the hot sun; {HANDS}",
         lines=[("qinshuang", "一班做，兩班睡，輪著來，木頭不許停。", "俐落")],
         motion="Qin Shuang tips the top of the upright bamboo pole slowly from left to right across the sky above her head as she speaks",
         zh="中景（膝以上）、慢推（送 `set-shentan-gongdi-mu-l2`：右岸木料堆、潭邊大石）：秦霜站在大石上，左手一本素灰封面的薄線裝冊子（**闔著**，拍法 38），右手竹竿豎著、竿腳拄在大石上，竿頭在她頭頂的天空裡從左到右慢慢一劃（獨立審稿建議 3：竿子低掃會跟背後的木料與柱子疊成一根；稿子『點左、中、右三下』改一劃：一鏡一個動作），朝畫左外看不到的人（壯丁，不點名、不寫人）俐落地說。稿子『看一眼冊子』與『壯丁分成三堆』不拍（三堆交給 s12 的頭巾顏色與台詞）"),
    dict(loc="gd_c", cam="Close-up, slow push in", chars=["erniu"], night="sun",
         comp=f"close-up of {ERNIU}, framed from the chest up with space above his head, {MALLET} resting on his right shoulder from the first frame, his face tipped up three-quarter to screen right toward someone out of sight beyond the upper right edge of the frame, never the lens; that side of the frame is only {SIDE_SKY} all the way to the edge, and he is the only person in the frame; curious, not smiling: brows lifted, eyes wide, lips moving fast between words; behind him, soft, the flat sandy bank and the low wooden frame in the hot sun; {HANDS}",
         lines=[("erniu", "秦姑娘，這分班的法子，妳從哪學來的？", "好奇")],
         motion="Wang Erniu raises his flat left hand high and stretches his neck upward as he speaks",
         zh="近景、慢推（送 `set-shentan-gongdi-an-l2`：左邊石階、小木台、矮木架與光禿的木軸）：二牛木槌扛在右肩，舉起左手平掌、伸長脖子朝畫右上外看不到的人（大石上的秦霜，不點名）喊；好奇、**不笑**。稿子『身後只有其他壯丁的肩』改成沙岸與木架（不描述畫面外的人，拍法 31）"),
    dict(loc="gd_e", cam="Low-angle medium close-up, slow push in", chars=["qinshuang"], night="sun",
         comp=f"low-angle medium close-up of {QIN}, seen from below, framed from the waist up, {BOOKLET} already lowered to her belt in her left hand from the first frame, {BAMBOO} held upright in her right hand at her far side, its top beyond the upper edge of the frame, her face three-quarter to screen left, looking down toward someone out of sight beyond the lower left edge of the frame, never the lens; that side of the frame is only {SIDE_SKY} all the way to the edge, and she is the only person in the frame; dry, not smiling: one brow raised, eyes cool, lips moving evenly between words; behind her, soft, only the pale clear sky and the long top beam of the tall wooden frame; {HANDS}",
         lines=[("qinshuang", "他寫的冊子。寫得囉嗦，法子倒是對的。", "淡淡地，嘴硬")],
         motion="Qin Shuang tucks the closed booklet into her belt as she speaks, and her chin lifts a little toward the left",
         zh="低角度中近景、慢推（送 `set-shentan-gongdi-tian-l2`：淡藍天與高木架頂的長橫梁）：秦霜右手照樣豎著那根光竹竿（獨立審稿建議 4：s12、s13 有竹竿，這鏡不能消失），把闔著的冊子插回腰帶、下巴往左一抬，朝畫左下外看不到的人（二牛，不點名）淡淡地說。稿子的近景改腰以上（拍法 32：插回腰帶要看得見）"),
    dict(loc="gd_c", cam="Medium close-up, slow push in", chars=["xuyan"], night="sun",
         comp=f"medium close-up of {XU_UP}, sitting at a rough plank table on the flat sandy bank, framed from the chest up, the edge of the tabletop along the bottom of the frame, one stick of charcoal in his right hand held just above the tabletop from the first frame, a few loose sheets of plain cream paper lying face down on the table before him, his face three-quarter to screen right, his eyes lifted toward the big grey boulder beyond the right edge of the frame, never the lens; he is the only person in the frame; quietly amused: a faint smile tugging at one corner of his mouth, eyes warm, lips pressed shut; behind him, soft, the stone steps, the small wooden landing and the low wooden frame in the hot sun; {HANDS}",
         lines=[("xitong", "宿主寫的冊子，總算有人看完了。", "冷"), ("xuyan", "嫌囉嗦也好，至少她從頭看到了尾。", "心裡話，錄得近、輕", "inner")],
         motion=f"Xu Yan lifts his eyes toward the boulder, the corner of his mouth moves a little, and he lowers his eyes to the table again; {SILENT_HE}",
         zh="中近景、慢推（送 `set-shentan-gongdi-an-l2`；稿子的中景改中近景：只有抬眼與嘴角的反應，shot_reading motion.look）：許硯坐在沙岸上一張粗木板桌前，右手一根炭條舉在桌面上方（不落筆，拍法 38），桌上幾張紙**背面朝上**；抬眼看畫右外的大石（不寫秦霜）、嘴角動一下（本鏡可以有一點笑意）、又低頭；系統冷冷吐槽與他的心裡話都是錄音，**全程嘴閉著**（拍法 15）；不寫淡藍光（拍法 11）。長鏡"),
    dict(loc="gd_c", cam="Medium shot from behind, slow push in", chars=["tangxiaotang", "shimujiang"], nospeak=["tangxiaotang"], night="sun",
         comp=alone(f"{SACK} held against her chest in both arms from the first frame; one step beyond her in the right third of the frame, his whole figure clear of her head and shoulders, {CARP}, standing beside the pile of long cut timbers, framed from the waist up, {MALLET} in his right hand, his face three-quarter to screen left toward her, his lips pressed shut, never the lens; gruff and wary, not smiling; behind them, soft, the timbers and the big grey boulder at the pond's edge in the hot sun; she stays in the middle of the frame the whole shot; {HANDS}; exactly two people, the young woman in the middle seen only from behind",
                    "standing on the stone edge of the pond,", frame="framed from the hips up", shot="medium wide shot"),
         lines=[("tangxiaotang", "糖坊的糖，換了三十斤鐵釘，夠不夠？", "得意")],
         motion=f"she drops the heavy sack down at the carpenter's feet with a thump, only her arms moving; {quiet('Carpenter Shi')}; {HEADSTILL}",
         zh="中遠景（從背後）、慢推（送 `set-shentan-gongdi-mu-l2`）：唐小棠背影在畫面正中、頭不動（拍法 40：說話從背後、放錄音，nospeak）、雙丸子、l1 交領短襦（不寫 t2 高立領，拍法 4）；第一格已經抱著鼓鼓的麻布袋走到木料堆旁、站在潭邊石沿上（獨立審稿建議 13：圖的下半是潭與石邊）（稿子『從左邊小路走到水車架下』在第一格完成），把袋子往石木匠腳邊一放（只動手臂）；石木匠在右三分之一、拿木槌、嘴閉著。稿子『拍拍手』『本鏡可以笑』不拍（從背後看不到笑）；前景蘆葦不寫（圖上沒有）"),
    dict(loc="gd_c", cam="Medium shot, slow push in", chars=["shimujiang"], night="sun",
         comp=f"medium shot of {CARP}, crouching beside {SACK.replace(' tied at the neck', '')} whose neck is untied and folded back, on the sandy bank by the pile of long cut timbers, framed from the waist up, {NAILS} already in his left palm from the first frame, his face three-quarter to screen left {off('left', SIDE_BANK)}; grudgingly pleased: a rare satisfied look, the corners of his mouth easing a little, lips moving roughly between words; behind him, soft, the pile of long cut timbers and the big grey boulder in the hot sun; {HANDS}",
         lines=[("shimujiang", "好釘。釘十二片葉板，還有剩。", "難得滿意")],
         motion="Carpenter Shi weighs the nails in his palm and lifts one long nail up to his eye against the light as he speaks",
         zh="中景、慢推（送 `-gongdi-mu-l2`）：石木匠蹲在解開的麻布袋旁（寫『袋口解開翻下』，不寫 open，拍法 36）、左掌一把長鐵釘，掂一掂、挑一根舉到眼前對著光看，朝畫左外看不到的人（唐小棠，不點名）說；難得滿意、嘴角鬆一點。稿子『唐小棠在左』不入鏡（她的正臉每集最多兩鏡、本集不用；拍法 40）"),
    dict(loc="gd_g", cam="Wide shot, slow push in", chars=["qianyuanwai"], night="sun",
         comp=f"wide shot at standing eye height across the pool toward the dry furrowed field beyond the tall wooden frame: {TANG_EDGE}; far beyond the pool on the edge of the dry furrowed field, small, framed full figure, standing in the gap between the middle and right posts of the tall frame, in front {QIAN}, his hands clasped behind his back, his face toward the worksite, his lips pressed shut, never the lens; smug, a thin cold smile; one step behind him {FENG}, side-on to us, {COMPASS} raised before his chest in both hands, his lips closed, never the lens; {HANDS}; exactly three people, the young woman at the edge seen only from behind",
         lines=[("tangxiaotang", "田埂上穿黃袍的，是錢員外請來的風水先生。", "畫外，小聲")],
         motion=f"the thin man in the yellow robe turns slowly round on the spot with the compass held before him, peering at it; {quiet('Qian Yuanwai and the thin man in the yellow robe', 'their', plural=True)}",
         zh="全景、慢推（送 `set-shentan-gongdi-geng-l2`：高木架右邊遠處的乾裂旱田）：前景左下是虛焦、被畫框切掉的雙丸子後腦與桃粉肩頭（不點名、不送圖）；遠處旱田邊上、高木架中間與右邊兩根柱子之間（獨立審稿建議 12：小人不跟柱子疊），錢員外背著手站在**前**、黃袍瘦高的風水先生在他身後一步（聖經〈小角色〉：同框時錢員外在前，稿子『風水先生走在前』照聖經改），舉著素面羅盤原地慢慢轉一圈。唐小棠的話是畫外錄音（拍法 40），畫面上的人嘴閉著。稿子『低角度、從工地往上拍』照圖的高度；『田埂在右上』照圖是高木架右邊遠處的田邊"),
    dict(loc="gd_g", cam="Wide shot side-on, slow push in", chars=[], night="sun",
         comp=f"wide shot side-on at standing eye height, small in the frame: on the edge of the dry furrowed field, framed full figure, {FENG}, {COMPASS} held before his chest in his left hand from the first frame, his narrow face in profile to screen left toward the pool below, never the lens; he is the only person in the frame; shrill and solemn: eyes narrowed, eyebrows raised high, his mouth moving a little as he calls out; behind him, soft, only the dry furrowed field and the pale clear sky in the hot sun",
         lines=[("fengshui", "拆祠堂的梁，動了龍脈，要遭天譴！", "尖著嗓子，拖長音")],
         motion=NOBODY + "the thin man in the yellow robe lifts the round wooden compass high above his head toward the sky as he calls out",
         zh="全景（側面、人小）、慢推（送 `-gongdi-geng-l2`；**不送人**：風水先生是小角色、沒有定妝照，聖經〈小角色〉『只在田埂上遠景與側面，不給正臉近景』，稿子 c20『中景正面』照聖經改）：瘦高黃袍的風水先生側臉朝畫左（工地方向），把羅盤往天上一舉、尖著嗓子拖長音喊（喊聲放錄音，畫面上他嘴的動作小）。稿子『另一手指著工地裡的梁』不拍（一鏡一個動作）"),
    dict(loc="gd_g", cam="Medium shot, slow push in", chars=["qianyuanwai"], night="sun",
         comp=f"medium shot on the edge of the dry furrowed field, framed from the waist up: in the middle {QIAN}, both hands tucked into his wide sleeves from the first frame, his face three-quarter to screen left, looking down toward the worksite beyond the lower left edge of the frame, never the lens; oily and gloating: a sly cold smile, eyes narrowed, lips moving slowly between drawn-out words; {FENG_EDGE_R}; behind them, soft, only the dry furrowed field and the pale clear sky; {HANDS}; exactly two people, the tall thin man at the edge cut by the frame",
         lines=[("qianyuanwai", "祖宗都不要了，柳溪這一村，要絕後嘍。", "油滑，拖長音")],
         motion="Qian Yuanwai leans forward from the waist toward the worksite below as he speaks, his hands staying in his sleeves",
         zh="中景、慢推（送 `-gongdi-geng-l2`）：錢員外兩手攏在袖子裡、往前探身朝畫左下外的工地喊（本鏡可以冷笑）；畫右緣被切掉的是風水先生的黃袖子與肩（不點名、不送圖，只露半身照稿子；自審：錢員外朝左，『在他身後』是右邊，聖經：錢員外在前）"),
    dict(loc="gd_c", cam="Medium shot, slow push in", chars=["erniu", "hanbo"], night="sun",
         comp=f"medium shot on the flat sandy bank, framed from the waist up: in front at the left {ERNIU}, {MALLET} lowered at his right side from the first frame, his face in profile to screen right, turned toward the two men behind him at the right, never the lens; uneasy, not smiling: brows knotted, eyes darting, the skin of his face tight, lips moving low between words; beside him at the right {HAN}, leaning on the staff, his face three-quarter to screen left toward Wang Erniu, his lips pressed shut, troubled, not smiling, never the lens; behind them at the right, soft, {TWO_WORKERS}, held low behind them, well apart from the staff, setting it down on the sand, their lips closed, never the lens; {HANDS}; exactly four people",
         lines=[("erniu", "天譴……大家說，這梁還要接著做嗎？", "發毛")],
         motion=f"Wang Erniu lifts his free left hand, palm up, toward the two men behind him as he speaks; {quiet('Elder Han and the two men', 'their', plural=True)}",
         zh="中景、慢推（送 `-gongdi-an-l2`）：二牛在左前、木槌垂在右手邊（寫 lowered，不寫掛著），側臉朝畫右、看著右後方的兩個壯丁，左手掌心朝上一攤地問（獨立審稿建議 2：回頭看景深會把臉轉離鏡頭）、臉發毛、**不笑**（原版必修）；韓伯在他右邊拄杖、嘴閉著（韓伯第二場的一鏡）；後面兩個壯丁（灰頭巾的鐵鏽紅、暗橄欖綠）把一根木料放到沙地上（手上拿什麼寫清楚；木料壓低在他們身後、離韓伯的竹杖遠，建議 2：三根長東西不相連）。跟拍改慢推"),
    dict(loc="gd_e", cam="Low-angle medium shot, slow push in", chars=["xiaohe"], night="sun",
         comp=f"low-angle medium shot of {XIAOHE}, seen from below, framed from the knees up, already standing on a long cut timber lying on the sand from the first frame, {PINWHEEL} in her right hand, her face lifted three-quarter to screen right toward the field edge beyond the upper right edge of the frame, her eyes on it, never the lens; she is the only person in the frame; fierce and sure as only a child can be, not smiling: chin up, brows drawn down, lips moving loud and clear between words; behind her, soft, only the pale clear sky and the long top beam of the tall wooden frame; {HANDS}",
         lines=[("xiaohe", "祖宗也口渴！水來了，祖宗先喝！", "叉腰，大聲")],
         motion="Little Xiaohe plants her left fist on her hip and thrusts the pinwheel out toward the field edge as she speaks",
         zh="低角度中景（膝以上）、慢推（送 `set-shentan-gongdi-tian-l2`）：小禾第一格已經站在一根橫放的木料上（稿子『從村民腿邊鑽出來、爬上木料』在第一格完成），左手叉腰、右手紙風車往畫右上的田邊一指、奶聲奶氣大聲喊；八歲、補丁淡紫短襖、紅繩小辮、腰上草兔子；紙風車是四片白紙葉插在竹籤上（聖經〈道具〉）。她是畫裡唯一的人（稿子『其他人嘴閉著』：不寫在畫裡）"),
    dict(loc="gd_c", cam="Wide shot, slow push in", chars=["erniu"], night="sun",
         comp=f"wide shot on the flat sandy bank, everyone framed full figure: in front in the middle {ERNIU}, already bent double with laughter from the first frame, {MALLET} in his right hand, his face toward the men around him, never the lens; roaring with laughter: mouth wide, eyes creased, lips moving between bursts of laughing words; around him {SIX_WORKERS}, laughing with their heads thrown back, never the lens; behind them, soft, the stone steps, the low wooden frame and the bare axle on its trestle in the hot sun; {HANDS}; exactly seven people",
         lines=[("erniu", "對，祖宗先喝！大家接著做，別停！", "笑彎了腰")],
         motion=f"Wang Erniu straightens up laughing and swings the mallet up onto his shoulder as he speaks, and the six men laugh with him",
         zh="全景、慢推（送 `-gongdi-an-l2`）：大家第一格已經笑開（稿子『一愣』在第一格前），二牛笑彎了腰（**本鏡可以大笑**），直起身把木槌甩回肩上、喊；六個壯丁仰頭大笑、兩手空著。稿子『拍大腿』『壯丁撿起木料』只留一個動作"),
    dict(loc="gd_g", cam="Medium shot, slow push in", chars=["qianyuanwai"], night="sun",
         comp=f"medium shot on the edge of the dry furrowed field, framed from the waist up: {QIAN}, already turning away to the right from the first frame, his face looking back over his right shoulder toward the worksite beyond the lower left edge of the frame, never the lens; sour and dark: his face fallen, brows low, eyes cold, lips moving low between words; {FENG_EDGE_R.replace('standing one step behind him', 'already turned away to the right, tucking a round wooden compass into his sleeve')}; behind them, soft, only the dry furrowed field and the pale clear sky; {HANDS}; exactly two people, the tall thin man at the edge cut by the frame",
         lines=[("qianyuanwai", "笑吧。十日一到，看你們誰哭。", "陰")],
         motion="Qian Yuanwai gives his sleeve one sharp shake, walks away toward the right edge of the frame and throws the words back over his shoulder as he goes",
         zh="中景、慢推（送 `-gongdi-geng-l2`）：錢員外臉沉下來、甩一下袖子往畫右走，邊走邊從**右肩**回頭朝畫左下外的工地撂一句（獨立審稿必改 3：往右走、從左肩回頭會背對鏡頭）；畫**右**緣是風水先生收起羅盤、已經轉身往右走的黃袖子與肩（不點名；建議 1：s19、s21 他都在錢員外右邊，不換邊）"),
    dict(loc="gd_c", cam="Close-up, slow push in", chars=["xiaohe"], night="sun",
         comp=f"close-up of {XIAOHE}, framed from the chest up with space above her head, already up on tiptoe from the first frame, {PINWHEEL} held out in both hands before her chest, her face three-quarter to screen left {off('left', 'the rough plank table', he='she')}; proud and happy: a wide gap-toothed smile, eyes bright, lips moving eagerly between words; behind her, soft, the low wooden frame and the bare axle on its trestle in the hot sun; {HANDS}",
         lines=[("xiaohe", "哥，你看！我用你的白紙，也做了一個會轉的。", "奶聲奶氣")],
         motion="Little Xiaohe pushes the pinwheel out toward the left edge of the frame in both hands as she speaks",
         zh="近景、慢推（送 `-gongdi-an-l2`）：小禾第一格已經跑到桌邊、踮著腳，兩手捧著紙風車往畫左外看不到的人（桌邊的許硯，不點名）遞、奶聲奶氣地說（本鏡可以笑、缺門牙）"),
    dict(loc="gd_e", cam="Insert close-up, slow push in", chars=[], night="sun",
         comp=f"insert close-up, the very first frame is already a close view of {PINWHEEL}, held upright by its stick in a man's right hand with a faded blue-grey sleeve rolled up to the elbow, the four white vanes still; beyond it, soft and out of focus, only the pale clear sky fills the background to every edge; only the pinwheel, the hand and the forearm are in the frame",
         lines=[("xuyan", "做得好。等水車轉起來，妳的風車也一起轉。", "畫外，微笑")],
         motion=NOBODY + "a soft breath of air reaches the pinwheel and its four white vanes begin to spin, faster and faster",
         zh="插鏡、慢推（第一格就是紙風車特寫，拍法 10、35；d1 不寫地點句，背景只有淡藍天；H3 參考模式至少一張圖，送 `-gongdi-tian-l2` 寫成『只給天的顏色』（同第 32 集 s16、s25b 的寫法））：許硯的手（藍灰袖子捲到手肘）豎著拿竹籤，一口氣吹過去，四片白紙葉呼呼轉起來。許硯的話是畫外錄音，嘴不入鏡；稿子『小禾的臉在後面虛焦』不寫（不寫畫面裡不具名的臉）（第二場結尾）"),
    # ---- scene 3: the tenth day (set-shentan-l1): dawn (the free grey-gold grade), then noon.
    dict(chapter="深潭邊，第十日", loc="ch", cam="Wide shot, slow push in", chars=["shimujiang", "xuyan"], night="dawn",
         comp=f"wide shot at standing eye height, like the picture, the whole wheel in the frame: {LADDER} leaning from the stone edge up against the wheel's wooden trestle; at its top beside the round hub of the axle {CARP_WORN}, framed full figure, small, already up on the ladder from the first frame, {MALLET} raised in his right hand, his face toward the hub, never the lens; hoarse and spent, not smiling: lips moving roughly between words; at the foot of the ladder on the stone edge {XU_WORN}, framed full figure, small, both hands steadying the ladder, his face turned up toward him, his lips pressed shut, never the lens; {HANDS}; exactly two people",
         lines=[("shimujiang", "最後一根木栓。架子，立起來了。", "沙啞，七天沒睡好")],
         motion=f"Carpenter Shi strikes the last wooden peg into the hub three times with the mallet, then stops, panting, as he speaks; {quiet('Xu Yan')}",
         zh="全景、慢推（人眼高、照圖；送本集免費做的清晨版 `set-shentan-chen-l3`（`shentan_l3.sh`：加了十二片葉板、塗掉麻繩與電塔的 `set-shentan-l3` 降飽和、壓暗、偏灰金，讀得出清晨）；整架水車照圖（原版必修：每鏡同一款）：石木匠在靠著輪架的木梯頂上、軸頭旁（眼睛紅、鬍渣），掄木槌把最後一根木栓敲進軸頭三下、停手喘氣、沙啞地說；許硯在梯腳的石邊扶梯子、眼下發青、下巴鬍渣、嘴閉著。稿子『站在木架頂上』照圖改成輪架旁的木梯；『低角度』照圖的高度；潭上薄霧寫在光線句（時間跳在 s27→s28 這一刀：第二場的造到一半換成立好的水車）"),
    dict(loc="ch_c", cam="Medium shot, slow push in", chars=["shimujiang", "xuyan"], night="dawn",
         comp=f"medium shot on the stone edge of the pond by the stone steps, both framed from the waist up: on the left {XU_WORN}, his face three-quarter to screen right toward the carpenter, his lips pressed shut, never the lens; worn out, not smiling; on the right {CARP_WORN}, already down off the ladder from the first frame, {MALLET} in his left hand, his face three-quarter to screen left toward Xu Yan, never the lens; gruff, with a small tired grin at one corner of his mouth, lips moving roughly between words; behind them, soft, the stone steps, the small wooden landing and the low wooden frame in the grey-gold dawn; {HANDS}; exactly two people",
         lines=[("shimujiang", "轉不轉，就看中午開閘了。", "沙啞，鬆一口氣")],
         motion=f"Carpenter Shi claps Xu Yan once on the shoulder with his flat right hand as he speaks; {quiet('Xu Yan')}",
         zh="中景、慢推（送清晨版裁切 `set-shentan-chen-an-l3`：石階、小木台、矮木架，場景的麻繩已塗掉）：石木匠第一格已經下到石邊（稿子『從木梯爬下來』在第一格完成），右手平掌拍一下許硯的肩、說（獨立審稿建議 5：他在右、朝左，拍背要繞過身體；稿子『拍在背上』改肩）（本鏡可以有一點笑意）；許硯在左、嘴閉著。稿子『把木槌往腰上一插』不拍（一鏡一個動作）"),
    dict(loc="ch_c", cam="Close-up, slow push in", chars=["xuyan"], night="dawn",
         comp=f"close-up of {XU_WORN}, standing on the stone edge in the left half of the frame, framed from the chest up with space above his head, his flat right hand already resting on one wet wooden paddle on the rim of the wheel at the right edge of the frame from the first frame, his face three-quarter to screen right, lifted toward the top of the wheel, his eyes on it, never the lens; he is the only person in the frame; drained and grave, not smiling: shadowed eyes, brows drawn, lips pressed shut; beside him at the right, the near rim, spokes and paddles of the wheel; behind him, soft, the low wooden frame, the stone steps and the thin mist on the water in the grey-gold dawn; {HANDS}",
         lines=[("xitong", "叮。旱災任務，今日到期。", "冷，宣布"), ("xuyan", "知道了。七天，梁拆了，人也熬了，就賭今天。", "心裡話，錄得近、輕", "inner")],
         panel=[("旱災任務，今日到期", "task")],
         motion=f"Xu Yan's eyes travel slowly up the wheel and his hand stays pressed on the paddle; {SILENT_HE}",
         zh="近景、慢推（送清晨版裁切 `set-shentan-chen-bian-l3`：左邊石邊與石階、右邊是輪緣與葉板（獨立審稿必改 2：舊的 `-lun` 輪子在左、右緣是田與柱，手按『右緣的葉板』不成立））：許硯站在左半、眼下發青、鬍渣，右手平掌第一格已經按在一片葉板上（稿子『伸手摸一下葉板』在第一格完成），眼睛慢慢往上看整個輪子、手停在葉板上；系統與心裡話都是錄音、**全程嘴閉著**；面板剪接時疊（不寫淡藍光）。長鏡"),
    dict(loc="nn_c", cam="Wide shot, slow push in", chars=["hanbo", "qinshuang", "xiaohe"], night="noon",
         comp=f"wide shot on the stone edge of the pond at the left by the stone steps, everyone framed full figure: at the front by the water {HAN}, already stepped out in front of the others from the first frame, his face three-quarter to screen right toward the wheel beyond the right edge of the frame, never the lens; grave and sure, not smiling: brows level, lips moving slowly between words; just behind him {QIN}, her hands empty at her sides, her lips pressed shut, never the lens, and beside her {XIAOHE}, {PINWHEEL} in her right hand, her lips pressed shut, never the lens; behind them {BANK}, holding their breath, their lips closed, never the lens; {HANDS}; exactly nine people",
         lines=[("hanbo", "時辰到了。開閘，給柳溪的田放水！", "慢，篤定")],
         motion=f"Elder Han raises his bamboo staff high above his head in his right hand as he speaks; {quiet('Qin Shuang, little Xiaohe and the six others', 'their', plural=True)}",
         zh="全景、慢推（送 `set-shentan-an-l3`：左邊石階、小木台、矮木架與輪子左緣的葉板；場景的麻繩已塗掉，獨立審稿必改 5）：**正午**（時間跳在 s30→s31 這一刀）。韓伯第一格已經走到最前面的石邊（稿子『走到岸邊』在第一格完成），把竹杖高高舉起、朝畫右外的水車說；秦霜（空手）、小禾（紙風車）在他身後，六個村民（祠堂那幾人、白鬚老漢已改短灰鬚布包頭）屏住氣。石木匠在閘門邊不入鏡（一鏡最多三張有名字的臉，拍法 1）。跟拍改慢推"),
    dict(loc="nn_c", cam="Medium shot, slow push in", chars=["xuyan", "shimujiang"], night="noon",
         comp=f"medium shot on the stone edge of the pond by the stone steps, both framed from the waist up: on the left at the water's edge {CARP_WORN}, beside {SLUICE}, already gripping that rope in both hands from the first frame, side-on to us, his face three-quarter to screen right toward Xu Yan, his lips pressed shut, tense, not smiling, never the lens; on the right {XU_WORN}, his right hand already raised high from the first frame, his face three-quarter to screen left toward the carpenter, never the lens; tense and sharp, not smiling: brows drawn, lips moving in one short shout; behind them, soft, the stone steps and the low wooden frame in the hard noon sun; the raised hand stays well apart from the rope; {HANDS}; exactly two people",
         lines=[("xuyan", "石師傅，拉！", "手一落，短喊")],
         motion=f"Xu Yan brings his raised hand sharply down as he shouts, and Carpenter Shi sinks his weight back against the rope; {quiet('Carpenter Shi')}",
         zh="中景、慢推（送 `-an-l3`）：石木匠在左邊石邊的閘門旁、兩手第一格已經握著閘板上的粗繩（閘門照聖經〈道具〉寫在潭口左邊：石邊缺口裡一道三片濕木板的小閘，圖上石階與小木台那一段）；許硯在右、右手第一格已經舉著，往下一落、短喊；石木匠身子往後一沉、嘴閉著。手與繩分開寫（第 32 集 fix2）"),
    dict(loc="nn_c", cam="Medium shot side-on, slow push in", chars=["shimujiang"], night="noon",
         comp=f"medium shot side-on at the narrow gap of the stone edge by the stone steps, framed from the knees up: {CARP_WORN}, both hands gripping the thick rope tied to the top of the small wooden sluice gate of three plain wet planks before him from the first frame, his feet braced on the stone, side-on to us, his face three-quarter to screen right toward the wheel beyond the right edge of the frame, never the lens; that side of the frame is only {SIDE_STONE_RIM} all the way to the edge, and he is the only person in the frame; straining, not smiling: teeth gritted, brows knotted, lips moving hard between words; behind him, soft, the stone steps and the small wooden landing in the hard noon sun; {HANDS}",
         lines=[("shimujiang", "閘開了！水往輪子底下衝過去了！", "吃力")],
         motion="Carpenter Shi throws his weight back on the rope and the sluice gate is pulled up out of the gap: the pond water rushes through it in a white surge along the stone toward the wheel at the right",
         zh="中景（膝以上、側面）、慢推（送 `-an-l3`）：石木匠兩手第一格已經握著閘板上的繩、腳蹬在石頭上，往後一仰把閘板拉起來（寫 pulled up，不寫 open，拍法 36），潭水從缺口嘩地沿石邊往右邊的輪子衝（剪在水衝進去的一半，照稿子〈剪接〉）；吃力地喊（畫右緣看得到停著的輪子的輪緣：`-an` 右緣本來就是輪子，獨立審稿建議 7）。側面拍，拉起的動作讀得出來（第 32 集 fix2：鉤子動作換構圖）"),
    dict(loc="nn", cam="Wide shot, static", chars=[], night="noon", act=4,
         comp=f"wide shot at standing eye height, side-on, like the picture, the whole wheel in the frame from the first frame, the camera still: a white surge of water already rushing along the stone edge from the left into the pond under the wheel; only the wheel, its frames, the pond, the stone edge and the fields are in the frame",
         motion=NOBODY + "In this shot the wheel turns only half a turn and then stops dead: the rushing water strikes the lowest paddles, the big wheel creaks and swings slowly round half a turn, slows, and stops, and stays still to the last frame while the water churns white under it",
         zh="全景、**固定**（送整張 `set-shentan-l3`：`set-shentan-l1` 用一次 Qwen 編輯加上十二片平木葉板的 `-l2`，再免費塗掉麻繩與電塔（獨立審稿必改 1 選 A）；不送人）：整架水車從第一格就在畫面裡、側面、照圖（原版必修：每鏡同一款）；第一格水已經沿石邊從左邊衝進輪子底下；水打在最下面的葉板上，輪子嘎吱轉了半圈、慢下來、停住，到最後一格都不動，只有水在輪底翻白。**結果先寫**（這一鏡只轉半圈就停住），鏡頭固定（第 32 集 fix2：鉤子動作要讀得出來、H3 預設會漂，鎖定要明講）；稿子『低角度、前景石槽裡的水』照圖的高度。無台詞"),
    dict(loc="nn_c", cam="Close-up, slow push in", chars=["xuyan"], night="noon",
         comp=f"close-up of {XU_WORN}, standing on the stone edge in the left half of the frame, framed from the chest up with space above his head, both flat hands already pressed against one wet wooden paddle on the rim of the wheel at the right of the frame from the first frame, his face three-quarter to screen right toward the paddle under his hands, his eyes on it, never the lens; he is the only person in the frame; stunned, not smiling: his face drained white, eyes wide, brows drawn up, lips moving in disbelief between words; beside him at the right, the near rim, spokes and paddles of the still wheel; behind him, soft, the low wooden frame and the stone steps in the hard noon sun; {HANDS}",
         lines=[("xuyan", "轉啊……水明明打在葉板上，它卻不轉。", "不敢相信")],
         motion="Xu Yan shoves hard against the paddle with both hands, and the wheel stays still",
         zh="近景、慢推（送 `set-shentan-bian-l3`：左邊石邊、右邊輪緣與葉板（獨立審稿必改 2））：許硯站在左半、兩手平掌第一格已經按在一片濕葉板上（稿子『往前走兩步』在第一格完成），用力一推、推不動，臉發白、不敢相信地說；**不笑**"),
    dict(loc="nn_c", cam="Medium close-up, slow push in", chars=["hanbo"], night="noon",
         comp=f"medium close-up of {HAN}, standing on the stone edge of the pond, framed from the waist up, the bamboo staff still raised high in his right hand from the first frame, his face three-quarter to screen right toward the wheel beyond the right edge of the frame, his eyes on it, never the lens; that side of the frame is only {SIDE_STONE_RIM} all the way to the edge, and he is the only person in the frame; shaken, not smiling: his long white beard trembling, eyes wet, lips moving slowly and unsteadily between words; behind him, soft, only the stone steps and the small wooden landing in the hard noon sun; {HANDS}",
         lines=[("hanbo", "停了……七天的工，祖宗的梁啊。", "聲音發抖")],
         motion="Elder Han lowers the raised staff slowly until its foot rests on the stone as he speaks",
         zh="中近景（腰以上）、慢推（送 `-an-l3`）：韓伯舉著的竹杖第一格還在頭上，慢慢放下來、杖尾點在石頭上，白鬚發抖、聲音發抖地說；**不笑**。稿子的近景改腰以上（杖的動作要看得見，拍法 32）；『身後虛焦的人群』改成石階（不描述畫外的人、人數讀得清）"),
    dict(loc="nn_c", cam="Medium shot, slow push in", chars=["qinshuang", "xiaohe"], night="noon",
         comp=f"medium shot on the stone edge of the pond, both framed from the waist up: on the left {QIN}, her flat left hand resting on the girl's shoulder from the first frame, her face three-quarter to screen left toward someone out of sight beyond the left edge of the frame, never the lens; that side of the frame is only {SIDE_STONE} all the way to the edge; frowning, not smiling: brows knotted, eyes hard, lips moving fast between words; on the right beside her {XIAOHE}, {PINWHEEL} in her right hand, its four white vanes still, her left hand clutching the hem of Qin Shuang's jacket, her face turned up toward the wheel, her lips pressed shut, frightened, not smiling, never the lens; behind them, soft, the stone steps and the low wooden frame in the hard noon sun; {HANDS}; exactly two people",
         lines=[("qinshuang", "石師傅，是不是哪一根釘錯了？", "皺眉")],
         motion=f"Qin Shuang leans forward a little toward the left edge of the frame as she calls out; {quiet('Little Xiaohe', 'her')}",
         zh="中景（雙人）、慢推（送 `-an-l3`）：秦霜在左、左手平掌第一格已經按在小禾肩上，身子往前傾一點、朝畫左外看不到的人（閘門邊的石木匠，不點名）皺眉喊；小禾在右、紙風車不轉、左手抓著秦霜的衣角、抬頭看水車、嘴閉著、**不笑**。稿子『往前一步』改前傾（手還按在小禾肩上）"),
    dict(loc="nn_c", cam="Medium shot, slow push in", chars=["shimujiang"], night="noon",
         comp=f"medium shot of {CARP_WORN}, already up on the wheel's wooden trestle in the water from the first frame, framed from the waist up, both hands gripping the edge of one wet wooden paddle, his face three-quarter to screen left {off('left', SIDE_STONE)}; grim, not smiling: brows knotted, jaw set, lips moving roughly between words; behind him, soft, only the wet spokes and paddles of the still wheel in the hard noon sun; {HANDS}",
         lines=[("shimujiang", "釘得死緊，一根都沒錯。是水推不動它。", "粗啞")],
         motion="Carpenter Shi wrenches hard at the paddle twice, it does not give, and he shakes his head as he speaks",
         zh="中景、慢推（送 `set-shentan-lun-l3`：輪子下半、輪架與葉板）：石木匠第一格已經爬上輪架（稿子『從閘門邊跑到水車下、爬上木架』在第一格完成，接 2026-11-06 審稿後的修改），兩手扳一片葉板、用力扳兩下、扳不動、搖頭，朝畫左外看不到的人（岸上的秦霜，不點名）粗啞地說；**不笑**"),
    dict(loc="nn_g", cam="Wide shot, slow push in", chars=["qianyuanwai"], night="noon",
         comp=f"wide shot at standing eye height across the pool toward the dry furrowed field beyond the tall wooden frame, the edge of the still wheel at the left of the frame: far on the edge of the field, small, framed full figure, in front {QIAN}, his face toward the pool below, never the lens; roaring with laughter: head thrown back, mouth wide, his belly shaking, lips moving between bursts of laughing words; one step behind him {RETAINERS}, grinning with closed lips, never the lens; {HANDS}; exactly three people",
         lines=[("qianyuanwai", "哈哈！七天拆一根梁，就轉半圈！", "放聲大笑")],
         motion=f"Qian Yuanwai slaps his thigh and throws his head back in laughter as he speaks; {quiet('The two men behind him', 'their', plural=True)}",
         zh="全景、慢推（送 `set-shentan-geng-l3`：高木架右邊遠處的旱田、畫左是停住的輪子邊緣）：遠處旱田邊上錢員外一拍大腿、仰頭大笑（**本鏡可以大笑**），身後兩個錢家家丁（黑短打、黑布包頭、兩手空著，聖經〈小角色〉：只在遠景）咧嘴不出聲。稿子『低角度、從岸邊往上拍田埂』照圖的高度"),
    dict(loc="nn_g", cam="Medium close-up, slow push in", chars=["qianyuanwai"], night="noon",
         comp=f"medium close-up of {QIAN}, framed from the waist up with space above his head, already bent forward with laughter from the first frame, his left hand braced on his knee, his face three-quarter to screen left, looking down toward the pool beyond the lower left edge of the frame, never the lens; that side of the frame is only {SIDE_SKY} all the way to the edge, and he is the only person in the frame; laughing himself breathless: eyes squeezed half shut, mouth wide, lips moving clearly between gasps of laughter; behind him, soft, only the pale clear sky and the long top beam of the tall wooden frame; {HANDS}",
         lines=[("qianyuanwai", "許秀才，連老天都不幫你，還想跟天搶水？", "笑到岔氣")],
         motion="Qian Yuanwai flings his flat right hand out toward the pool below as he speaks, gasping with laughter",
         zh="中近景（腰以上）、慢推（送 `set-shentan-tian-l3`：淡藍天與高木架頂的橫梁）：錢員外笑到岔氣、左手扶著膝蓋，右手平掌往畫左下外的潭邊一甩、笑著把字說清楚（**本鏡可以大笑**；本集結尾，懸念交給第 34 集第一鏡：許硯按著停住的葉板、小禾的紙風車倒著轉；第 34 集不再重複他的笑）。稿子的近景改腰以上（扶膝蓋要看得見）"),
]

HEAD = [
    "- 重製版 r2、真人版（站主 2026-11-11「之後都用真人版」）：照 `docs/videos/zhong-tian-qu-qi-e033-r2/script.md`（c01–c40 對應 s01–s40；含「這版改了什麼」「2026-11-06 審稿後的修改」）；台詞一字不改，只改拍法；每鏡一個看得見的動作、一句一筆不拆半句、預設不笑。篇章設定 `production/r2-bible-e031-e040.md`（拍法 1–43 條、〈場景〉〈接點〉〈小角色〉），帳照 `r2-bible-e011-e060.md`。**第 4 篇章〈旱年〉第三集**。",
    "- 內部工作編號 933（`hailuo/{ff,clips}-dh-e933.json`；`colab/runs/e933/extras.json`、`colab/runs/e933-live/spec.json`、工作資料夾 `~/mokaair-work/videos/zhong-tian-qu-qi-e933-dh/`）；發布 slug `zhong-tian-qu-qi-e033-r2`。不放集數、不放片名卡；**s01 照第 32 集 s36–s37 實拍改寫**（`e932-live.mp4` 203–218 秒：s36 胸口高的全景、門在左、韓伯跪在中間回頭、八個村民跪在右半；s37 許硯在門口、圖卷橫在腰前）：s01 同一個機位，第一格許硯已經跨進門檻一步；s40 交給第 34 集（接點 33→34：許硯按著停住的葉板、小禾的紙風車倒著轉，不重播錢員外的笑）。",
    "- 照第 32 集審稿與實拍後的寫法一開始就照做：`OFFSCREEN_SPEECH = False`；系統與心裡話的鏡，每張朝鏡頭的臉都寫不說話、嘴閉著；**對畫外的人說話寫「朝畫左／右外看不到的人」，那一側到邊緣只有景、畫面裡只有他一個人，不點名、不描述不在畫裡的人**；過肩前景是不點名、不送圖的背影；不掛東西；不寫 open；道具與接觸寫在第一格；寫人數；**背景的人寫手上拿什麼（繩子、火把、木料、空手），不寫兵器字；不寫否定名詞**；長東西（梁、繩、木梯、竹竿、閘繩）第一格不跟另一根長東西相連（第 32 集 fix2）；沒有泥（第 32 集 fix3：不寫 caked、yellow mud，不把沾東西的人放在橘光下）。",
    "- **人物**：秦霜柴刀整集不寫（拍法 5）；第二場一根光竹竿（**不綁旗**，拍法 33）與闔著的素灰封面線裝冊子（拍法 38），第三場空手。王二牛每鏡不笑，只有 s24 稿子的大笑；第二場一把木槌。唐小棠只在第二場：s17 說話從背後拍（畫面正中、頭不動、雙丸子，放錄音），s19 畫左下緣不點名的背影、話是畫外錄音；**本集不用她的正臉**；l1 交領短襦，不寫 t2 高立領（拍法 4、40）。小禾八歲、紙風車四片白紙葉插竹籤（聖經〈道具〉）。**風水先生**是小角色（聖經〈小角色〉、〈還沒解決的〉8）：不畫定妝照、不點名、不給正臉近景，只在田邊遠景（錢員外在前、他在後）與側面；聲音 Charon（`MINOR`），喊話放錄音。錢員外胸前沒有吊牌，錦袍寫小圓紋（不寫 pattern）。**村民**：祠堂照第 32 集那八人，**白鬚老漢改布包頭、短灰鬚**（e932 審片：跟韓伯撞）；拉繩三人、舉火把兩人、扛梁兩人分開寫；工地九個壯丁分三班（灰、褪色靛藍、土黃頭巾），每人衣色年紀不同。",
    "- **軸線（照圖）**：第一場祠堂：門在左、供桌牌位在右、主梁在牆頂；跪拜的臉從供桌左端側面拍，說話的人朝畫右看牌位；拉繩的人在左（門那邊）、梁的另一頭在右；s09–s11 許硯在左（門那側）、石木匠在右（供桌那側）。第二場深潭（`set-shentan-gongdi-l1`，輪子拿掉、木架與木軸）：鏡頭在潭近端石邊，潭在前景、兩座木架在遠端潭邊、左邊石階與小木台、右邊潭邊大灰石、右岸木料堆；工地與壯丁在左岸、秦霜站在右邊大石上朝畫左、石木匠在右邊木料堆、錢員外與風水先生在高木架右邊遠處的旱田邊。第三場同一個機位、整架水車立在潭邊（`set-shentan-l1`）：閘門寫在左邊石階那段石邊缺口，村民在左邊石邊、水車在他們右邊，錢員外與家丁在右邊遠處田邊。",
    "- **時間與光**：第一場 s01–s04 黃昏燭光（送第 32 集的 `set-citang-huang` 一族），**s05 起入夜**（送本集免費做的 `set-citang-ye2-l1` 一族：門外夜色、主梁裂紋塗掉），燭光加手上的松明火把；第二場第四日正午的烈日（稿子的上午與正午合成一種光：同一張圖）；第三場 s28–s30 清晨灰金（送本集免費做的清晨版 `-chen` 三張），**s31 起正午**白光。時間跳都在剪點（s04→s05、s27→s28、s30→s31），不在鏡頭裡變光。",
    "- **原版必修**（聖經第 33 集）：水車每鏡外型不一樣 → 第二場只送 `set-shentan-gongdi-l2` 一族、第三場只送 `set-shentan-l3` 一族（獨立審稿必改 1：`-l1` 的輪子沒有葉板，選 A：一次 Qwen 編輯加十二片平木葉板成 `-l2`，再免費塗掉麻繩與電塔成 `-l3`），文字只寫「the water wheel exactly as in the picture」加十二片葉板；原版建議：紙風車白紙竹骨、小禾八歲、結尾不是三鏡都在笑（s35–s38 停住與檢查、s39–s40 才是錢員外大笑）、風水先生的天譴照聖經只在遠景側面。",
    "- 要買的秒數（BUY；先照第 31、32 集的估法估，**2026-11-19 錄音後照 `span933.sh` 量人聲長度重核：41 句每句都放得下，不改**（最緊 s20 7.21 秒／8、s40 7.20／8、s30 兩句 8.06＋間隔／10；`audio/README-retakes.txt`）。估法：一句 6 秒的鏡放得下約 5.9 秒人聲；19 字以上、兩句一鏡、韓伯與石木匠慢的句子、有長停頓的、稿子的長鏡買 8 或 10）：s08、s16、s30 買 10 秒（系統加一句或心裡話）；s02、s03、s04、s06、s09、s10、s11、s19、s20、s21、s26、s27、s28、s31、s33、s35、s36、s38、s39、s40 買 8 秒；s32 買 5 秒（5 字的短喊）；s01、s34 買 6 秒（沒有台詞：走過大廳、轉半圈停住要停得住）；其餘照 `gen-dh.mjs` 的預設（說話 6 秒）。**錄音後照 `span932.sh` 量人聲長度重核**，放不下的改 BUY、重 build、重跑 prep。",
    "- **表上的「秒」欄是 lint 估法**，比錄音短；剪接以錄音的人聲長度為準。",
]
FOOT = [
    "- **參考圖**（`assets/refs-live/`）：許硯 l1、angle-a（帶笑的 angle-b 整集不送；全景 s01、s28 只送 l1）；韓伯 `hanbo-portrait-l1`、石木匠 `shimujiang-portrait-l1`（都沒有角度圖）；王二牛 l1、angle-a（全景 s05、s24 只送 l1）；秦霜每鏡只送 l1（`refs-dh` 沒有她的角度圖；`refs-live/angles` 有，但 `retake.py` 不能加圖，同上）；小禾每鏡只送 l1（gen-dh 沒送她的角度圖；獨立審稿建議 14 要加 angle-a：`retake.py` 只能換或拿掉圖、不能加圖，加圖要改共用工具，本集照 l1）；錢員外 l1、angle-a（angle-b 不送，同第 31 集）；**唐小棠 s17 從背後拍：三張臉部參考圖全部拿掉**（拍法 40）。s19 唐小棠的背影、過肩前景的背影（s09、s10）、風水先生（s19–s21、s25）、家丁、村民、壯丁、s27 插鏡的手都不送圖、不點名。",
    "- **場景圖**：祠堂黃昏送第 32 集做好的 `set-citang-huang-l1`（s01）與裁切 `-huang-zuo2`（s02）、`-huang-liang`（s03）、`-huang-zuo`（s04）；入夜送本集免費做的 `set-citang-ye2-l1`（s05）與裁切 `-ye2-men`（s06、s08、s10）、`-ye2-tang`（s09）、**`-ye2-qiang`**（s07、s11：沒有梁的素牆，獨立審稿必改 4）；深潭第二場送 `set-shentan-gongdi-l2`（s12）與裁切 `-gongdi-an-l2`（s14、s16、s22、s24、s26）、`-gongdi-mu-l2`（s13、s17、s18）、`-gongdi-tian-l2`（s15、s23；**s27 插鏡只當天的顏色**）、`-gongdi-geng-l2`（s19、s20、s21、s25）；第三場清晨送 `set-shentan-chen-l3`（s28）、`-chen-an-l3`（s29）、`-chen-bian-l3`（s30），正午送 `set-shentan-l3`（s34）、`-an-l3`（s31、s32、s33、s36、s37）、`-bian-l3`（s35）、`-lun-l3`（s38）、`-geng-l3`（s39）、`-tian-l3`（s40）。`set-citang-l1`、`set-citang-ye-l1`（主梁還有裂紋）、`-huang-qiang`（左上角有梁）、`set-shentan-l1`／`-l2` 與它們的 l1 裁切（沒有葉板／還有麻繩與電塔）不送。",
    "- **本集新做的圖**（2026-11-19，`live-action/free-e031-e040/`，各跑兩次逐位元一樣，寫進 refs-live README）：`citang_ye_clean.py`＋`citang_ye_crops.sh`（夜祠堂主梁裂紋照 `citang_huang.py` 塗掉 → `set-citang-ye2-l1` 與五張裁切，含獨立審稿後加的 `-ye2-qiang`）；**付費一張**：`set-shentan-l2`（獨立審稿必改 1 選 A：`set-shentan-l1` 只加十二片平木葉板，Colab `zt-live3` 的 Qwen-Image-Edit-2509，兩輪 8 支挑第二輪種子 9331205，2.12 CU；`colab/runs/e933-live/shentan-l2/`）；`shentan_clean.py`＋`shentan_l3.sh`（`-l2` 塗掉矮木架的麻繩、遠方小電塔與地平線細桿 → `set-shentan-l3` 與五張裁切、清晨調色與兩張裁切；`set-shentan-gongdi-l1` 塗掉電塔與細桿 → `set-shentan-gongdi-l2` 與四張裁切）。舊的 `shentan_crops.sh` l1 裁切留在 refs-live、本集不送。風水先生照聖經不畫定妝照；`script.md` 建議的 `prop-shuiche-t1` 道具圖不做（聖經〈原版必修〉第 33 集改成兩張場景圖每鏡送）。",
    "- **還缺、先用最接近的圖**（不花錢、註明在這裡）：(1) 稿子的**閘門與石槽**圖上沒有：寫在左邊石階與小木台那段石邊缺口（`-an-l3`；場景本身那條麻繩已塗掉，不會跟閘繩連成一條），s32–s34 的閘門與水是文字；挑片若閘門畫不出來，s33 剪在水衝出去的一半、s34 只用水打到輪子之後。(2) **木梯**、**木板桌**、**木料上站的小禾**都是文字加在圖上。(3) **田埂**：圖上是高木架右邊遠處的旱田、沒有高起的田埂，錢員外與風水先生站在田邊（遠、小）。(4) **夜裡的祠堂**用免費夜版，門外是夜、牆上那片格子光照舊（讀成月光，接受）。",
    "- 共用檔：沒有改（`build-r2.py` 的 `EN` 已有每個在畫面上說話的名字；風水先生不在 `chars`，台詞是錄音，不需要 `EN`）；`gen-dh.mjs`、`pilot.py`、`cast.json` 不動，風水先生的聲音在本檔 `MINOR`。對畫外說話、對牌位與水車說話的鏡，精修文字的通用說話視線由本檔結尾的 `live_clips()` 換成 d1 的方向句（`GAZE_REFINE`）；s17 唐小棠的背影：立領句拿掉、名字換成「從背後看的年輕女子」（同第 31 集）。",
    "- **獨立審稿**（`writer-tools/e033-r2/review-independent.md`，2026-11-19，必改 8、建議 15）全部照改，只有建議 14（秦霜、小禾加送角度圖）沒做、改寫參考圖那一行：必改 1 水車葉板選 A（`set-shentan-l2`／`-l3`）；必改 2 s30、s35 改送輪子在右的 `-bian`；必改 3 s25 右肩；必改 4 沒有梁的 `-ye2-qiang`；必改 5 塗掉麻繩的 `-an-l3`；必改 6 s34 拿掉布鞋句（mkspec）；必改 7 平地上的潭；必改 8 s12 不寫 crowd；建議見各鏡 zh。",
    "- **d1 前置**（2026-11-19，`colab/runs/e933-live/PREP.md`）：`colab/runs/e933/extras.json`、`colab/runs/e933-live/{mkspec.py,spec.json}`（種子 9331101／9331102）、scratchpad `tools/prep933.sh`、`tools/rec933.sh`（錄音，**沒跑**）、`e933d1.sh`（Colab session `zt-live3`，**沒跑**）。",
    "- 配音：**風水先生 Charon 第一次用**（聖經〈小角色〉；孫掌櫃第 29 集後不出場）；小禾（Leda）、韓伯（Enceladus）的音高第一次量（聖經〈還沒解決的〉10；韓伯第 32 集量到約 120 Hz）；石木匠（Schedar）第 32 集照第 43 條升了 3 個半音，本集同場跟韓伯（s31–s38）照樣比、差不到 3 個半音就移開。",
    "- 配樂：第一場接第 32 集的低沉大提琴，s03『三年』一個重音，s05 起低沉的號子鼓點；第二場明快的勞動曲，s20 風水先生底下換怪腔木魚，s24 笑聲切回明快；第三場清晨安靜的 strings，s31 開閘鼓聲漸強，s34 停住全部收掉只剩一聲木頭嘎吱，s39 起只有錢員外的笑聲。音效見 script.md〈音樂與音效〉。",
]

# Seconds to buy. Rechecked against the recordings 2026-11-19 (span933.sh; audio/README-retakes.txt): every line fits, no change.
# First estimated as e931/e932 (a 6 s shot holds about 5.9 s of speech, 8 s about
# 7.3 s; e932's lines ran about 2.5-3.7 characters a second, Carpenter Shi 15 characters in 6.05 s, Elder Han 17 in 7.80 s).
# 10 s: s08 (system 8 + Xu Yan 16 characters, two voices), s16 (system 14 + thought 17), s30 (system 10 + thought 22).
# 8 s: s02, s03 (Xu Yan 15-17, 一字一頓 / 很穩), s04, s31, s36 (Elder Han, slow), s09, s11, s28, s33, s38 (Carpenter Shi 12-18,
#      slow and hoarse; s28 also three blows), s06, s35 (a long pause), s10 (20 characters), s19, s26, s27 (18-19 characters),
#      s20, s21 (drawn out), s39, s40 (laughing).
# 6 s: s01 (no line: the walk across the hall), s34 (no line: the half turn and the stop, held).
# 5 s: s32 (「石師傅，拉！」, five characters).
# 6 s (gen-dh's default for a spoken line): every other shot.
BUY = {"s08": 10, "s16": 10, "s30": 10,
       "s02": 8, "s03": 8, "s04": 8, "s06": 8, "s09": 8, "s10": 8, "s11": 8, "s19": 8, "s20": 8, "s21": 8, "s26": 8, "s27": 8,
       "s28": 8, "s31": 8, "s33": 8, "s35": 8, "s36": 8, "s38": 8, "s39": 8, "s40": 8,
       "s01": 6, "s34": 6, "s32": 5}


# ---- the refine text (as e023-e032): hailuo/clips-dh-e933.json column 0 is the motion text refine-prep.py sends with a picked
# d1 draft. gen-dh.mjs opens every clip that lists tangxiaotang with the CG-era "Tang Xiaotang's high stand-up collar stays
# closed at her throat." and names her in "<names> shown in <Picture 1>"; in a back shot that draws the collar back and turns
# her face to the lens. Her back shot (s17): the sentence goes and her name becomes "the young woman seen only from behind",
# with someone else: "keep the same face, hair, costume and props as the first frame, the young woman's back to us" (e031).
# FRONT_TANG is empty (no front face this episode). Column 1 is recomputed. prep933.sh hands stage 1 the anchor form
# (anchor_form(), e028 review 必改 1; rule 39).
COLLAR = "Tang Xiaotang's high stand-up collar stays closed at her throat. "
FRONT_TANG = set()
# rule 31 (e030 review 建議 10): gen-dh's speaking gaze names "the person he/she is speaking to", who is not in the frame of these
# shots (or is a thing: the tablets, the beam, the wheel); the refine text gets d1's direction. anchor_form() puts gen-dh's
# words back for stage 1.
GAZE_GEN = {"he": "turned toward the person he is speaking to, face in profile or three-quarter profile, eyes on that person",
            "she": "turned toward the person she is speaking to, face in profile or three-quarter profile, eyes on that person"}
_L = "his face three-quarter to screen left toward someone out of sight beyond the left edge of the frame, his eyes on that spot"
_R = "his face three-quarter to screen right toward someone out of sight beyond the right edge of the frame, his eyes on that spot"
_HL = "her face three-quarter to screen left toward someone out of sight beyond the left edge of the frame, her eyes on that spot"
_TABLETS = "his face three-quarter to screen right toward the row of plain tablets on the altar table, his eyes on them"
_WHEEL = "his face three-quarter to screen right toward the wheel beyond the right edge of the frame, his eyes on it"
_WORKS = "his face three-quarter to screen left, looking down toward the worksite beyond the lower left edge of the frame, his eyes on it"
_POOL = "his face three-quarter to screen left, looking down toward the pool beyond the lower left edge of the frame, his eyes on it"
# sid -> (pronoun, the direction sentence)
GAZE_REFINE = {
    "s02": ("he", _TABLETS), "s04": ("he", _TABLETS),
    "s03": ("he", "his face tipped up toward the dark main beam above him, his eyes on it"),
    "s06": ("he", "his face lifted three-quarter to screen right along the rope toward someone out of sight beyond the upper right edge of the frame, his eyes on that spot"),
    "s08": ("he", _R), "s11": ("he", _L),
    "s13": ("she", _HL),
    "s14": ("he", "his face tipped up three-quarter to screen right toward someone out of sight beyond the upper right edge of the frame, his eyes on that spot"),
    "s15": ("she", "her face three-quarter to screen left, looking down toward someone out of sight beyond the lower left edge of the frame, her eyes on that spot"),
    "s18": ("he", _L),
    "s21": ("he", _WORKS),
    "s23": ("she", "her face lifted three-quarter to screen right toward the field edge beyond the upper right edge of the frame, her eyes on it"),
    "s25": ("he", "his face looking back over his right shoulder toward the worksite beyond the lower left edge of the frame, his eyes on it"),
    "s26": ("she", _HL),
    "s31": ("he", _WHEEL), "s33": ("he", _WHEEL), "s36": ("he", _WHEEL),
    "s35": ("he", "his face three-quarter to screen right toward the paddle under his hands, his eyes on it"),
    "s37": ("she", _HL), "s38": ("he", _L),
    "s39": ("he", _POOL), "s40": ("he", _POOL),
}
BACK_NAME = "the young woman seen only from behind"


def live_clips(path):
    import hashlib
    import json
    import re
    clips = json.load(open(path, encoding="utf-8"))
    for key, row in clips.items():
        text = row[0]
        sid = key.split("-", 1)[1]
        if COLLAR in text:
            text = text.replace(COLLAR, "")
            if sid not in FRONT_TANG:
                m = re.search(r"\[Shot 1\] 3D CG\. (.+?) shown in <Picture 1> (keeps?) ", text)
                names = [n for n in m.group(1).split(" and ") if n != "Tang Xiaotang"]
                who = " and ".join(names + [BACK_NAME])
                who = who[0].upper() + who[1:]
                verb = "keep" if names else "keeps"
                text = text.replace(m.group(0), f"[Shot 1] 3D CG. {who} shown in <Picture 1> {verb} ", 1)
                if names:
                    text = text.replace("keep the same face, hair, costume and props as the first frame", "keep the same face, hair, costume and props as the first frame, the young woman's back to us", 1)
                else:
                    text = text.replace("keeps the same face, hair, costume and props as the first frame", "keeps the same hair, costume and props as the first frame, her back to us", 1)
                assert "back to us as the first frame" not in text and ("back to us" in text), key
                assert "Tang Xiaotang" not in text, (key, "her name is left in a back shot's refine text")
        if sid in GAZE_REFINE:
            pr, gaze = GAZE_REFINE[sid]
            assert text.count(GAZE_GEN[pr]) >= 1, (key, "speaking gaze")
            text = text.replace(GAZE_GEN[pr], gaze, 1)
        assert "stand-up collar" not in text, key
        row[0] = text
        row[1] = hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]
    open(path, "w", encoding="utf-8").write(json.dumps(clips, ensure_ascii=False, separators=(",", ":")))


# e928 review 必改 1 (rule 39): ref2manifest.mjs (stage 1) strips gen-dh's refine anchor with ANCHOR_FF, and the back-shot wording
# live_clips() writes no longer matches it. prep933.sh hands stage 1 the anchor form of the live file (this), then puts the
# live file back; the refine text (clips-dh) keeps live_clips()'s wording.
def anchor_form(text):
    text = text.replace(", the young woman's back to us; the set layout stays as it is.", "; the set layout stays as it is.")
    text = text.replace("keeps the same hair, costume and props as the first frame, her back to us; the set layout stays as it is.",
                        "keeps the same face, hair, costume and props as the first frame; the set layout stays as it is.")
    assert "back to us; the set layout" not in text
    for pr, g in sorted(set(GAZE_REFINE.values()), key=lambda x: len(x[1]), reverse=True):
        text = text.replace(g, GAZE_GEN[pr])
    return text


def anchor_form_file(src, dst):
    import json
    clips = json.load(open(src, encoding="utf-8"))
    for row in clips.values():
        row[0] = anchor_form(row[0])
    open(dst, "w", encoding="utf-8").write(json.dumps(clips, ensure_ascii=False, separators=(",", ":")))


if __name__ == "r2spec":
    import atexit
    import os
    atexit.register(live_clips, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "hailuo", f"clips-dh-e{EP}.json"))
