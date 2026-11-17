"""Episode 28 remake (r2): the writer spec for ../e001-r2/build-r2.py. Source: docs/videos/zhong-tian-qu-qi-e028-r2/script.md
(c01-c39 = s01-s39, c03 split into s03 and s03b, c15 into s15 and s15b; the CG-era r2 script), including its sections 「這版改了什麼」,
「2026-11-06 審稿後的修改」 and 「真人版的改動（2026-11-17）」, which override the tables. Every line is the script's, word for word;
only the staging changes. Bible: production/r2-bible-e021-e030.md (rules 1-30, the 27->28 and 28->29 hand-overs, the props,
people and picture tables). The eighth episode of arc 3 〈搶親〉: the lane behind the silk shop on the twenty-seventh night (the
same moment as e027 s37), the yamen steps at first light and the court hall on the twenty-eighth morning, the county jail gate on
the twenty-ninth night, and the town square at noon on the thirtieth day.

Written from the start the way e027-r2/r2.py stands AFTER its independent review (../e027-r2/review.md: the 13 必改 and the
cheap 建議 the coordinator took), with what the pickers caught in e924-e926 (colab/runs/e92{4,5,6}-live/{review-picks-a,
review-picks-b,picks-merged}.tsv) and the lessons in the task file (e921-e925):
- OFFSCREEN_SPEECH = False (rule 15): every shot with an off-screen line, a thought or a system line writes the silence of each
  person on screen (quiet(), SILENT_HE). Where a back-view, foreground or veiled character speaks, every face toward the camera
  "says nothing ... lips pressed together"; no word that invites a smile or talk on a listener unless the script lets him smile.
- A line said to someone outside the frame is written "toward someone out of sight beyond the left/right edge of the frame",
  that side of the frame is written as set only, all the way to the edge, and the speaker as the only person in the frame
  (s12, s19, s23, s25, s35, s38). No person who is not in the first frame is named or described anywhere, in the prompts or in
  the refine text (e925 lesson; e927 必改 5).
- Tang Xiaotang never speaks on camera and never shows her face (rule 3): her five lines (s08, s11, s16, s21, s34) are all from
  behind, in the middle of the frame, "facing straight away from us", head still, exactly two round buns (TBACK; nospeak; spec
  drops her pictures and identity sentence). The script's 高立領, 「下巴以上」 and 「襦裙從立領到腰一件闔上」 are CG wording and are
  not used (rule 4). Her abacus is never written (rule 20: only in inserts; this episode has no abacus insert, the 「喀」 of c21 is
  a sound).
- A-ling wears the veil in every shot (rule 21): aling-veil-portrait-l1 for her portrait, her angle pictures dropped, the veil
  sentence every time; all her lines are recordings (nospeak). Her short knife (rule 22 as e027's review rewrote it) is
  "one short knife sheathed in plain dark wood ... one closed piece of dark wood" (hand-over 27->28: it stays sheathed throughout);
  written only in s02, s03 and s03b (the fight); every other shot of her writes her sleeves. No "dagger", "blade" or "draw".
  The script's sweat-stuck strand (c07-c24) is "one loose strand of black hair fallen across her forehead" (rule 12: nothing small
  on the skin).
- The fight (rule 22): the two men never show a face, each shot has one man doing one thing; the script's one-take c03 is split
  into s03 (one man's stick swings down past her) and s03b (the other man, his stick slipping from his fingers, sinks to his knees),
  no knife touching anyone. The sticks are STICK.
- Zhao Butou and the yamen men (rules 16, 17): no word for their office ("Constable Zhao" in build-r2's speaking clause and
  cast.json's constable's hat are replaced by extras.json, the refine text by live_clips()); his iron ruler (c31, c32) is his
  bare forearm held across Xu Yan's chest; his ring of keys is a sound. The yawning yamen man at the gate, the two rows of eight
  with staves in the hall and on the square are left out (sounds), as e027.
- Magistrate Hu always wears the winged hat (HU); in the hall only on the dais crop, every hall shot "his shoulders square to the
  desk like the picture, only his head turned three-quarter to screen left" (e027 必改 11). The gavel is GAVEL. On the square he is
  never in a shot with Sun Zhanggui (bible 同框撞臉).
- Sun Zhanggui (sunzhanggui-portrait-l1): the food box FOODBOX (bible rule 24) at the jail; on the square his hands in his sleeves.
- The jail (rule 24): set-dalao-l1 as the coordinator picked it (README: its bars read dark and iron-like, the gate fills the
  frame): the picture decides (rule 29), so the bars are "thick square dark bars", no material named; the jail scene is staged at
  and through the gate (Xu Yan outside it; Sun Zhanggui, Zhao Butou and Lai San beyond it), Lai San shows only a shoulder in s29
  and his face only alone in s30 (rule 24: four named people, split).
- Name only what should be drawn (rules 7, 17, 27): the silver "a small silver ingot, its top smooth and plain" (the 魏記 mark is
  the line's; the script's underside with a square frame in c10 is not shown); the yellow paper YPAPER; the ledger STACK. No word
  "open" anywhere; no hung thing named (the lane's small warm light, as e027).
- Counts written everywhere (rule 25), the square's townspeople each in their own clothes (or they clone a main character).
- One visible action per shot, props and contacts in the first frame; the script's follows, tracks, rises, falls and pans are
  slow push-ins.

THE AXES (rule 29: the set picture decides):
- The lane (set-chouduan-ye-xiang-l2, e027's): the lane runs straight away from us; A-ling stands in the near part of the lane on
  the LEFT facing screen right down it, the two men further down right of centre facing her, the small warm light behind them;
  Lai San at the right-hand man's right shoulder (e027 s37). Everyone looks along the lane.
- The yamen steps (set-xianya-steps-l2, e019's): the porch at the top of broad stone steps that go down toward us; the thick red
  pillar in the middle, the white wall and arched doorway on the LEFT, the dark red doors and the drum on the RIGHT. Xu Yan and Tang
  Xiaotang wait on the paving at the top; A-ling and Lai San come up the steps toward the camera side. Xu Yan looks screen right and
  down the steps; A-ling, at the head of the steps, looks screen left toward the two.
- The court hall (set-xianya-gongtang-l1's crops, as e027): Magistrate Hu behind the desk facing screen left toward the floor;
  everyone on the floor faces screen right and up toward the desk.
- The jail gate (set-dalao-l1): we stand outside the gate; Xu Yan at its LEFT end; Sun Zhanggui and Zhao Butou beyond the bars in
  the torchlit room; Zhao Butou comes out and stands on the RIGHT of Xu Yan.
- The square (set-guangchang-l1 painted and cropped): the low stone platform in the middle with its steps toward us; the red desk
  at its back, the dark wooden armchair on its RIGHT (Wei Shaoqing), the wooden chest on the ground at its LEFT; Xu Yan stands on
  the LEFT of the platform, Lai San kneels in its middle, Tang Xiaotang below its left side, Sun Zhanggui below its right side.

PLACES (the coordinator's decisions, 2026-11-17; every picture looked at full size; script.md 〈真人版的改動〉): gen-dh's SET
phrases give set-chouduan (silk shop), set-xianya (county yamen), set-dalao (county jail) and set-guangchang (town square);
spec.json swaps each for the picture below with an absolute path.
- The lane: set-chouduan-ye-xiang-l2 (e027's; all of scene 1).
- The yamen steps: set-xianya-steps-l2 (e019's; s08, s09, s11-s17) and the new free crop set-xianya-steps-shi-l1 (the steps
  only; s10, the ingot caught).
- The court hall: set-xianya-gongtang-dais-l1 (Hu: s18, s20, s22) and set-xianya-gongtang-floor-l1 (the floor: s19, s21, s23-s25).
- The jail: set-dalao-l1 (s26, s27, s31) and two new free crops: set-dalao-bi-l1 (the bars before the torchlit wall: s29, s30,
  s32) and set-dalao-di-l1 (the bars and the stone beyond, brightened: s28).
- The square: five new free pictures from set-guangchang-l1 with the two yellow boards and the yellow stand at the hall doorway
  painted dark (they had stroke-like marks): set-guangchang-tai-l1 (the wide, the sun cropped off: s33, s39), -tai-zhong-l1 (the
  platform: unused this episode, made for e029), -shu-l1 (a bare tree and roofs against the sky: s35, s36, s38), -zuo-l1 (below
  the platform's left: s34), -you-l1 (below its right: s37).
- Inserts and shots with nobody named (s03b, s04, s10, s28) open their motion with NOBODY.
- Shared files: no code changed (every on-screen speaker is in build-r2.py's EN; no minor role speaks). refs-live gets eight new
  free pictures (new ids, own l1; rule 19) and a README paragraph.
"""
EP = 928  # internal working number; the published slug is zhong-tian-qu-qi-e028-r2
SLUG = "zhong-tian-qu-qi-e028-r2"
EP_TITLE = "下次帶我，人證翻供（重製版 r2）"
OUTLINE_SECONDS = 199  # script.md: about 199 s, 39 shots (7 + 18 + 7 + 7)
TARGET_MINUTES = [3, 4]
TITLE = "下次帶我，人證翻供｜種田娶妻打天下 第28集（重製版）"
DESCRIPTION = "巷口被兩根棍子堵住，阿令一個人放倒兩個打手，短匕連鞘都沒拔，把賴三和那錠銀子押回縣衙。天剛亮，許硯和唐小棠在縣衙門口等了一夜；銀子底下有魏記的戳。許硯不罵她，只說：昨天是我讓妳一個人去的，下次，帶我。她說你會拖累，好感卻加了七。公堂上賴三全招，胡縣令卻把公審訂在第三十日午時，讓許記封到賭約最後一天。第二十九日夜，許硯在大牢門外看見孫掌櫃提著食盒進去，下層滿滿是銀子。第三十日正午的廣場上，賴三舉起綁著的手，指向許硯：是許家逼我下的毒。《種田娶妻打天下》第 28 集（重製版）。"
THUMB = ("下次，帶我", "s13")
CHARACTERS = ["xuyan", "tangxiaotang", "aling", "laisan", "zhaobutou", "weishaoqing", "huxianling", "sunzhanggui", "xitong"]
MINOR = {}
MUSIC = "one cue per scene: short tense drum hits in a dark stone lane at night, one heavy beat when two wooden sticks hit the stones, then only the night wind; then a soft warm cue at a cold dawn that turns into dull low drums in a county court hall, one heavy accent when a date is set; then a low suspense pad and the crackle of torches at a jail gate, one heavy accent when silver is shown; then the murmur of a crowded square at noon with one low drum slowly building, one big hit at an accusation; ancient Chinese rural drama, no vocals"

# Places. gen-dh SET takes the FIRST pattern in its list order that the whole prompt matches: lane prompts say "silk shop"
# (never "alley", "Xu family shop", "market street"); steps and hall prompts say "county yamen"; jail prompts say "county jail"
# (never "yamen"); square prompts say "town square" (never "yamen", "market street").
LANE = ("a narrow lane paved with worn stone slabs between dark blue-grey brick walls, running straight away from us; on the left "
        "a long bamboo pole with four plain cloths drying over it and two wooden tubs below, on the right a round brick well "
        "under a small thatched roof, and far down at the end of the lane one small warm light glowing on the wall above a dark "
        "wooden double door")
STEPS = ("a deep porch with one thick round red pillar in the middle, on the left a white wall above grey brick with one dark "
         "arched doorway, on the right tall dark red doors behind one big round drum on a red wooden stand, a floor of pale grey "
         "stone paving and broad pale stone steps going down toward us")
HALL = ("a floor of large grey stone tiles, thick round dark red-brown wooden pillars, tall dark wooden lattice windows along "
        "the side wall above a low white panel")
DAIS = ("at the back one long dark wooden desk with one dark wooden armchair behind it, before a wall of plain white panels; on "
        "the desk one flat oblong block of dark wood at the left and one small dark wooden rack at the right")
JAIL = ("a gate of thick square dark bars filling the frame from edge to edge, and beyond the bars a room of pale stone blocks "
        "with a round stone arch at the back and two torches burning in dark iron holders on its side walls")
SQ = ("a wide square of packed pale earth; in the middle one low square platform of grey stone slabs with a few steps up its "
      "front, one long desk draped in red cloth on it and one dark wooden armchair at its right side; one plain wooden chest "
      "standing on the ground at its left; two bare trees, and low tiled buildings and white walls all round")
LOC = {
    "lane": f"In the narrow lane behind the silk shop in the county town deep in the night: {LANE}; cold blue moonlight from above, the small warm light far down the lane, the wet stones gleaming",
    "lane_c": "In the narrow lane behind the silk shop in the county town deep in the night, dark blue-grey brick walls and worn wet stone slabs, cold blue moonlight from above",
    "lane_s": "In the narrow lane behind the silk shop in the county town deep in the night, low over the worn wet stone slabs, cold blue moonlight from above",
    "steps": f"Before the gate of the county yamen at first light on a cold clear winter dawn: {STEPS}; cold soft grey dawn light",
    "steps_c": "Before the gate of the county yamen at first light on a cold clear winter dawn, the thick red pillar, the white wall and the dark red doors of the porch, cold soft grey dawn light",
    "steps_s": "Before the gate of the county yamen at first light on a cold clear winter dawn, above the broad pale stone steps, cold soft grey dawn light",
    "hall": f"In the court hall of the county yamen early on a cold clear winter morning: {HALL}; clear cold daylight from the tall lattice windows",
    "hall_c": "In the court hall of the county yamen early on a cold clear winter morning, dark red-brown pillars and tall lattice windows, clear cold daylight",
    "dais": f"In the court hall of the county yamen early on a cold clear winter morning: {DAIS}; clear cold daylight from the tall lattice windows",
    "jail": f"At the gate of the county jail deep in the night: {JAIL}; warm torchlight beyond the bars, the cold blue night on this side",
    "jail_b": "At the gate of the county jail deep in the night, close to the thick square dark bars, beyond them the pale stone blocks of the wall and one torch burning in a dark iron holder; warm torchlight",
    "jail_d": "At the gate of the county jail deep in the night, the thick square dark bars and the torchlit stone floor and wall just beyond them; warm torchlight",
    "jail_g": "At the gate of the county jail deep in the night: thick square dark bars in the foreground, and beyond them the torchlit pale stone wall of the room with one small wooden lattice window and one torch burning in a dark iron holder; warm torchlight beyond the bars, the cold blue night on this side",
    "square": f"In the town square of the county town at noon on a cold clear winter day: {SQ}; hard bright low winter sun from the upper right behind, long shadows falling to the left across the earth",
    "square_c": "In the town square of the county town at noon on a cold clear winter day, the bare branches of a tree and the low tiled roofs against the clear blue sky, hard bright low winter sun from the right",
    "square_l": "In the town square of the county town at noon on a cold clear winter day, on the packed pale earth below the left side of the low stone platform, one plain wooden chest beside it, the low tiled buildings beyond; hard bright low winter sun from the upper right behind, long shadows falling to the left across the earth",
    "square_r": "In the town square of the county town at noon on a cold clear winter day, on the packed pale earth below the right side of the low stone platform, the long low tiled building with its plank doors beyond; hard bright low winter sun from the upper right behind, long shadows falling to the left across the earth",
}
LIGHT = {
    "lane": "the cold moonlight and the deep night stay unchanged",
    "steps": "the cold grey dawn light stays unchanged",
    "hall": "the clear cold daylight from the lattice windows stays unchanged",
    "jail": "the warm torchlight and the deep night stay unchanged",
    "square": "the hard winter sunlight stays unchanged",
}
# bible rule 15: no "<X> speaks off screen" / "the system voice speaks off screen".
OFFSCREEN_SPEECH = False

# Repeated wording (each prop is one object, written the same way every time).
XU_D = "Xu Yan, in his faded blue-grey scholar's robe patched at one elbow, its sleeves down"
XU_N = ("Xu Yan, in an old plain grey cotton outer coat over his faded blue-grey scholar's robe, one small clay oil lamp in his "
        "left hand, its small flame cupped behind his right palm")
XU_NC = "Xu Yan, in an old plain grey cotton outer coat over his faded blue-grey scholar's robe"
ZHAO = ("Zhao Butou, in his soft black futou cap and plain black round-collared cotton robe, a plain black cloth sash tied at "
        "his waist, nothing else at his waist")
LAI_A = ("Lai San, small and thin, in his checked grey-brown cross-collared short jacket, a coarse grey cloth apron tied at his "
         "waist, an old cloth head wrap below his topknot")
LAI_B = f"{LAI_A}, both his hands tied together before him at the wrists with a strip of his own grey cloth sash"
WEI = ("Wei Shaoqing, in his sapphire-blue brocade robe woven with gold thread, a white jade pendant at his waist, a small green "
       "jade ornament at the front of his topknot")
FAN = "one closed folding fan in his right hand, its dark bamboo ribs pressed tight together like a short slim stick"
ALING = ("A-ling, in her plain grey-white cotton dress with long sleeves covering her wrists, her black hair in a high bun with "
         "one plain wooden hairpin")
VEIL = ("a veil of soft, finely woven pale grey gauze over her nose, mouth and chin, tied behind both ears, falling to just below "
        "her jaw")
STRAND = "one loose strand of black hair fallen across her forehead"
SLEEVE = "her right sleeve falling down over her right hand"
KNIFE = "one short knife sheathed in plain dark wood, grip and sheath one closed piece of dark wood as long as her hand"
HU = "in his black gauze futou hat with two short stiff flat wings and his blue-green round-collared official robe"
GAVEL = "one flat oblong block of dark polished wood the size of half a brick, plain on every side"
SUN = ("Sun Zhanggui, tall and lean with a long narrow face and a thin grey-streaked beard, in his green satin robe with a jade "
       "belt hook")
FOODBOX = ("one two-tier round dark-lacquered wooden food box with a bent wooden handle, plain and smooth on every side")
INGOT = "one small silver ingot, its top smooth and plain"
STICK = "one plain wooden stick as long as his arm, smooth and round to its ends"
STICKS = "two plain wooden sticks, each as long as a man's arm, smooth and round to their ends"
MAN1 = "one broad man in a plain black cross-collared short jacket, a black cloth head wrap and cloth shoes"
MEN2 = "two broad men in plain black cross-collared short jackets, black cloth head wraps and cloth shoes"
STACK = "one thick stack of plain blank paper sheets stitched along one edge with cord"
YPAPER = "rough blank yellowish paper"
POUCH = "one small plain brown cloth pouch tied at its neck"
TOWNS = ("eight townspeople in Song-dynasty cotton robes and head cloths, standing in a loose line behind a rope, each dressed "
         "differently: an old man in a brown robe, a woman in a dull blue jacket and long skirt, a young man in a dark blue "
         "short jacket, a stout man in an indigo robe, a woman in a faded green jacket, a thin old woman in dark brown, a boy in a patched "
         "tan jacket and a man in an ochre robe")
HANDS = "their hands hold only what is described here"
SILENT_HE = "He says nothing in this shot: his lips stay pressed together from the first frame to the last, his jaw still, no talking, no mouthing words"
UNDERVEIL = "her lips stay still under the veil from the first frame to the last"
NOBODY = "Throughout the shot the set layout stays as it is. The pictures fix the place and the objects only, never the mood. "
# e924 fix1's back-of-head wording, as e925-e927
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


def alone(rest, where, frame="framed from the waist up", shot="medium shot"):
    """Tang Xiaotang from behind, in the middle of the frame (not at an edge: the pickers' cheek at the frame edge)."""
    return f"{shot} from close behind {TBACK}, {where} in the middle of the frame, {frame}, facing straight away from us; {only_tang()}; {rest}"


SHOTS = [
    # ---- scene 1: the twenty-seventh night, the lane behind the silk shop (27->28: the same moment as e027 s37).
    dict(chapter="後巷", loc="lane", cam="Low medium shot, slow push in", chars=["laisan"], night="lane",
         comp=f"low medium shot at knee height down the lane, like the picture: in the soft left foreground the back of one young woman's shoulder and the side of her high bun with one plain wooden hairpin, the thin tie of a pale grey gauze veil behind her ear, her grey-white cotton dress, out of focus, unnamed; further down the lane right of centre {MEN2}, standing side by side across the stones facing her, the small warm light far behind them, their faces dark in shadow, each gripping {STICK} in his right hand; at the right shoulder of the right-hand man {LAI_A}, framed from the waist up, his face three-quarter to screen left toward the woman in the left foreground, never the lens; cowardly and shrill, not smiling: eyes wide, brows up, lips moving fast in a shout between words; {HANDS}; exactly four people",
         lines=[("laisan", "就她一個，給我上，打完有賞！", "縮在打手身後，喊")],
         motion="Lai San ducks in behind the right-hand man's shoulder and peers out past it as he shouts; the two men stand their ground, gripping their sticks, their lips closed; the young woman's back stays still",
         zh="低機位中景、慢推（送 `set-chouduan-ye-xiang-l2`；接點 27→28 同一刻，接第 27 集 s37 的站位）：前景左阿令的肩與髮髻、木簪、面巾細繩（不點名、不送圖，拍法 2）；巷子深處偏右兩個黑短打的人並肩面向她，巷底暖光在他們身後、臉在暗影裡（不給正臉）；賴三在右邊那人右肩旁，往他身後一縮、探頭喊。稿子『打手往前跨一步』不拍（一鏡一個動作，打手站定）；前景柴捆照圖不寫"),
    dict(loc="lane_c", cam="Close-up, slow push in", chars=["aling"], nospeak=["aling"], night="lane",
         comp=f"close-up of {ALING}, {VEIL}, standing on the wet stones, framed from the chest up with space above her head, {KNIFE} already held upright in her right hand before her chest from the first frame, her face three-quarter to screen right toward someone out of sight beyond the right edge of the frame, where only the dark brick wall reaches the edge, never the lens; calm and cold: brows level, eyes steady; behind her the dark brick wall, soft",
         lines=[("aling", "你們要先動手，那我就只還手。", "隔著面巾，平靜")],
         motion=f"A-ling's eyes move once from one spot beyond the right edge of the frame to another and back; {UNDERVEIL}",
         zh="近景、慢推（送後巷圖）：阿令（面巾，送面巾定妝照、不送角度圖，拍法 21）右手第一格已經把套著木鞘的短刀豎在胸前（刀柄連鞘一整塊閉著的深色木頭，接點 27→28：從頭到尾不出鞘；不寫 dagger、blade、draw），眼睛在畫右外看不到的地方來回掃一次（審稿必改 3：不描述畫外的人；那一側到邊緣只有暗磚牆；台詞放錄音，nospeak）。稿子『腳往後撤半步』近景看不到，不拍"),
    dict(loc="lane", cam="Wide shot, slow push in", chars=["aling"], night="lane",
         comp=f"wide shot down the lane at standing eye height, like the picture: in the middle of the wet stones {ALING}, {VEIL}, her back three-quarter to us, facing down the lane, framed full figure, {KNIFE} held low in her right hand at her side, never the lens; calm and quick: eyes on the man before her; two steps beyond her down the lane, facing her and us, {MAN1}, the small warm light far down the lane behind him, his face dark in shadow, framed full figure, {STICK} already raised high over his head in both hands from the first frame; {HANDS}; exactly two people",
         motion=f"The man brings his stick down in one hard stroke and A-ling sways aside, so the stick comes down a full arm's length to her right and cracks onto the empty wet stones; {UNDERVEIL}; nobody is hit",
         zh="全景、慢推（人眼高、照圖；送後巷圖）：稿子 c03『整個動作留在畫面裡』跟拍法 22『一鏡只拍一個打手的一個動作』衝突，照聖經拆成兩鏡：這一鏡只有一個打手：審稿必改 4，窄巷不能左右對峙——阿令背對我們四分之三、面向巷子深處，打手在她前方兩步、面向她與我們、巷底暖光在他身後（背光、臉在暗影裡），雙手舉棍第一格已經舉高，往下一砸，阿令側身一讓，棍子落在她右邊一臂外的空石板上（沒打到人，打擊聲交給音效）；木鞘短刀低握在身側"),
    dict(sid="s03b", loc="lane", cam="Medium shot, slow push in", chars=[], night="lane",
         comp=f"medium shot on the wet stones of the lane: {MAN1}, side-on to us facing screen left, framed from the knees up, already doubled over from the first frame, his face turned down toward the stones, dark in shadow, his left hand clutching his right wrist from the first frame, his right hand loosening on {STICK}; at the left edge of the frame only a slender hand in a long grey-white cotton sleeve reaching in from beyond the edge, holding {KNIFE}, low at her side; {HANDS}; exactly one man and one grey-white sleeved hand",
         motion=NOBODY + "the stick slips from the man's fingers and he sinks slowly to his knees on the wet stones, his head down; the grey-white sleeved hand stays still",
         zh="中景、慢推（送後巷圖；c03 的後半，拆鏡）：另一個打手第一格已經彎著腰、臉朝石板（暗影、不給臉）、左手抓著自己的右手腕（審稿必改 5：跪倒有原因，跟 s06 抱手腕一致；剪接在 s03 落棍後、s03b 前放一聲短促的木頭敲擊），手裡的棍子滑落、慢慢跪倒；畫左緣只有阿令灰白長袖的手低握木鞘短刀（不點名、不送圖，刀不碰人；拍法 22：不拍刀刃碰到人，連鞘點穴也不拍，跪倒的原因交給 s03 與剪接）"),
    dict(loc="lane_s", cam="Low-angle insert close-up, slow push in", chars=[], night="lane",
         comp=f"low-angle insert close-up, the shot opens directly on the worn wet stone slabs of the lane in the cold moonlight, from its very first frame, {STICKS} already falling a hand's height above the stones; only the stones and the two sticks are in the frame",
         motion=NOBODY + "the two sticks clatter down onto the wet stones, bounce once and lie still",
         zh="低角度插鏡、慢推（第一格就是石板與兩根木棍；送後巷圖）：兩根木棍砸在石板上、彈一下、落定（無台詞）。稿子『牆上一個插髮簪的高挑影子』拿掉（一鏡一個主體；影子第 27 集 s35 已用過）"),
    dict(loc="lane_c", cam="Medium shot, slow push in", chars=["laisan"], night="lane",
         comp=f"medium shot of {LAI_A}, sitting on the wet stones, framed from the waist up, a slender hand in a long grey-white cotton sleeve reaching in from the left edge of the frame already gripping the front of his jacket at the collar from the first frame, both his hands already raised before his chest with the palms out, his face three-quarter to screen left toward someone out of sight beyond the left edge of the frame, never the lens; terrified and pleading, not smiling: brows up and pinched, eyes wide, lips moving fast in a wail between words; behind him the dark brick wall, soft; {HANDS}; exactly one person and one grey-white sleeved hand",
         lines=[("laisan", "姑奶奶饒命！銀子給妳，放我走吧！", "哀叫")],
         motion="Lai San shakes his raised hands as he pleads; the grey-white sleeved hand keeps its grip on his collar",
         zh="中景、慢推（送後巷圖）：賴三第一格已經跌坐在石板上、兩手舉在胸前，畫左緣一隻灰白長袖的手揪著他前襟的衣領（阿令不入鏡、不點名）；他抖著手哀叫，朝畫左外看不到的人說（那一側只有暗磚牆）。稿子『跑兩步、被揪住往回拉、跌坐、舉手』只拍舉著手求饒（一鏡一個動作）"),
    dict(loc="lane", cam="Wide shot, slow push in", chars=["aling", "laisan"], night="lane",
         comp=f"wide shot down the lane at standing eye height, like the picture: in the middle of the lane {ALING}, {VEIL}, standing, framed full figure, her left hand already gripping the collar of {LAI_A}, who sits on the stones at her feet, his face three-quarter to screen right, never the lens, his lips closed; her face three-quarter to screen right, her eyes down on him, never the lens; cold and calm: brows level; further down the lane two men in plain black short jackets and black head wraps lying curled on their sides on the stones, their faces turned down to the stones, each holding his own wrist, two plain wooden sticks lying on the stones beside them; {HANDS}; exactly four people",
         motion=f"A-ling pulls {INGOT} out from the front of Lai San's jacket with her right hand; Lai San keeps his lips closed and stays where he sits; {UNDERVEIL}",
         zh="全景、慢推（人眼高、照圖；送後巷圖）：巷子中間阿令左手揪著坐在地上的賴三衣領，右手從他前襟掏出銀子（頂面平滑、沒有字，拍法 27）；遠一點兩個打手側躺在石板上抱著手腕、臉朝地（不給臉、沒有傷口），兩根木棍散在旁邊；嘴都閉著（無台詞）。稿子的高角度慢升改人眼高慢推（圖是平視）；『賴三伸手想搶又縮回去』拿掉（一鏡一個動作）"),
    dict(loc="lane_c", cam="Close-up, slow push in", chars=["aling"], nospeak=["aling"], night="lane",
         comp=f"close-up of {ALING}, {VEIL}, {STRAND}, framed from the chest up with space above her head, her head bowed, her eyes lowered to the lower edge of the frame, never the lens, where two thin wrists in checked grey-brown sleeve cuffs are held together before her with a strip of grey cloth wound round them, both her hands already gripping the two ends of the strip from the first frame; cold and set: eyes narrowed, brows level; behind her the dark brick wall, soft; {HANDS}",
         lines=[("aling", "銀子是證物，你也是。走，去縣衙。", "冷")],
         motion=f"A-ling pulls the two ends of the grey cloth strip hard into a tight knot round the two wrists; {UNDERVEIL}",
         zh="近景、慢推（送後巷圖）：阿令（面巾、額前一縷碎髮：稿子『被汗沾住』只寫頭髮，拍法 12 皮膚上不寫細小東西）低頭，畫面下緣兩隻灰褐袖口的瘦手腕被一條灰布條纏在一起，她兩手抓著布條兩端一拉、打死結（台詞放錄音，nospeak；本場結尾）。稿子『銀子塞進左袖、短匕收回右袖、推他的肩』只拍打結（一鏡一個動作）；之後的鏡不寫刀"),
    # ---- scene 2a: the twenty-eighth dawn, the yamen steps (set-xianya-steps-l2).
    dict(chapter="縣衙門口", loc="steps", cam="Medium shot from behind, slow push in", chars=["tangxiaotang", "xuyan"], nospeak=["tangxiaotang"], night="steps",
         comp=alone(f"{STACK} already held in her left arm against her chest from the first frame, only its pale edge showing at her side; beyond her, a little right of the middle, standing on the porch paving beside the thick red pillar, {XU_D}, framed from the waist up, his face three-quarter to screen right, his eyes past her toward the street below the steps, beyond the lower right edge of the frame, never the lens; heavy-eyed and tense after the long wait, not smiling: brows drawn, lips pressed shut; she stays in the middle of the frame the whole shot, her shoulders square to us; {HANDS}; exactly two people, the young woman in the middle seen only from behind",
                    "standing on the pale stone paving at the top of the steps,"),
         lines=[("tangxiaotang", "天都亮了，阿令跟了一整夜，怎麼還不回來？", "擔心，不笑")],
         motion=f"Xu Yan, standing still beside the pillar, lets his eyes drift down toward the street, only his eyes moving; {quiet('Xu Yan')}; {HEADSTILL}",
         zh="中景（從背後）、慢推（送縣衙門口 `set-xianya-steps-l2`：門廊、紅柱、左邊白牆拱門、右邊深紅門與鼓、往下的石階；第 19 集的圖）：唐小棠的背影在畫面正中、正背對鏡頭、頭不動、剛好兩顆丸子，左臂抱著帳本（縫邊的空白紙疊）；她前面偏右，許硯站在門廊地磚上的紅柱邊、站定不動，只有眼睛往下看街（審稿必改 10：不在石階邊、不再『停下』；她一直在畫面正中、肩膀正對我們；嘴閉著）（nospeak，拍法 3；她的圖與身分句由 spec 拿掉）。稿子『前景石獅、大門口打呵欠的衙役』不拍：圖上沒有石獅，衙役只寫有名字的人（第 19 集）；『眼睛有血絲』改寫熬夜的神情（拍法 12）"),
    dict(loc="steps", cam="Low-angle medium shot, slow push in", chars=["aling", "laisan"], nospeak=["aling"], night="steps",
         comp=f"low-angle medium shot from lower down the steps: at the head of the steps {ALING}, {VEIL}, {STRAND}, standing, framed from the waist up, her right hand already gripping the back of the collar of {LAI_B}, who stands bent forward beside her on the top step, from the first frame, her face three-quarter to screen left toward someone out of sight beyond the left edge of the frame, never the lens; cool and tired: eyes level, brows still; Lai San's face three-quarter to screen left, never the lens, scared, his lips pressed shut; behind them the thick red pillar and the dark red doors, soft; {HANDS}; exactly two people",
         lines=[("aling", "回來了。下藥的人，還有他收的銀子。", "隔著面巾")],
         motion=f"A-ling pushes Lai San down by the collar and he drops to his knees on the top step; {UNDERVEIL}; Lai San keeps his lips closed",
         zh="低角度中景（從石階下往上）、慢推（送門口圖）：阿令（面巾、額前碎髮）第一格已經揪著兩手被綁、彎著腰站在她旁邊階頂的賴三後領（審稿必改 12：不在下一階），一推，賴三跪在最上一階（台詞放錄音，nospeak）；朝畫左外看不到的人說（許硯、唐小棠不入鏡：一鏡最多三張臉、唐小棠不露臉）。稿子『衙役嚇醒、從左袖掏出銀錠』不拍（一鏡一個動作；銀子 s10 從拋出開始）"),
    dict(loc="steps_s", cam="Insert close-up, slow push in", chars=[], night="steps",
         comp=f"insert close-up, the shot opens directly on one man's right hand in a faded blue-grey sleeve cuff held up palm up in the cold dawn air above the pale stone steps, from its very first frame, {INGOT} already falling into it from above; the pale stone steps soft and out of focus below; only the hand, its sleeve cuff and the ingot are in the frame",
         lines=[("xuyan", "底下有戳……這是魏記的銀子。", "畫外，低")],
         motion=NOBODY + "the hand catches the silver ingot and closes round it, weighing it once",
         zh="插鏡、慢推（第一格就是攤開的掌心與落下的銀子；送免費新圖 `set-xianya-steps-shi-l1`：門口圖只剩石階）：許硯的手（藍灰袖口）接住拋來的銀子、掂一下（台詞放錄音，畫外低聲）。稿子『翻過來、底面一個方形戳印框』不拍：頂面平滑、底面不入鏡（拍法 27：魏記由台詞說；方框會長字）"),
    dict(loc="steps_c", cam="Close-up from behind, slow push in", chars=["tangxiaotang"], nospeak=["tangxiaotang"], night="steps",
         comp=alone("both her hands low at her sides; beyond her, soft, the thick red pillar and the dark red doors of the porch; " + HANDS,
                    "standing on the pale stone paving,", frame="framed from the shoulders up", shot="close-up"),
         lines=[("tangxiaotang", "妳一個人跟了他一整夜？不要命啦！", "又驚又氣")],
         motion=f"her shoulders jerk up once, sharp and angry; {HEADSTILL}",
         zh="近景（從背後）、慢推（送門口圖）：唐小棠的後腦與肩在畫面正中、正背對鏡頭、頭不動、剛好兩顆丸子，肩膀一聳（又驚又氣）（nospeak，拍法 3）。稿子『近景下巴以上、跺腳、抓住腰間小金算盤、瞪阿令』改背影：算盤只在插鏡入鏡（拍法 20），跺腳交給音效"),
    dict(loc="steps_c", cam="Close-up, slow push in", chars=["aling"], nospeak=["aling"], night="steps",
         comp=f"close-up of {ALING}, {VEIL}, {STRAND}, framed from the chest up with space above her head, her left hand already holding the cuff of her right sleeve from the first frame, her face three-quarter to screen left toward someone out of sight beyond the left edge of the frame, where only the soft red pillar reaches the edge, never the lens; she is the only person in the frame; cool and offhand: eyes half lidded, brows level; behind her the dark red doors, soft",
         lines=[("aling", "兩個打手，一個跛子，不費事。", "淡淡地")],
         motion=f"A-ling tugs her right sleeve down over her right hand with her left hand; {UNDERVEIL}",
         zh="近景、慢推（送門口圖）：阿令（面巾、額前碎髮）左手拉著右袖口往下一拉、蓋住右手（台詞放錄音，nospeak）；朝畫左外看不到的人（唐小棠，不點名），那一側到邊緣只有虛焦的紅柱、畫面裡只有她。稿子『聳一下肩』拿掉（一鏡一個動作，留拉袖）"),
    dict(loc="steps_c", cam="Over-the-shoulder medium shot, slow push in", chars=["xuyan"], night="steps",
         comp=f"over-the-shoulder medium shot: in the soft right foreground the back of one young woman's shoulder and the side of her high bun with one plain wooden hairpin, the thin tie of a pale grey gauze veil behind her ear, her grey-white cotton dress, out of focus, unnamed; facing us beyond her {XU_D}, framed from the waist up, {INGOT} already held in his right hand at his chest from the first frame, his face three-quarter to screen right toward her, never the lens; steady and quiet, not smiling and not angry: level eyes, lips moving calmly between words; behind him the white wall and the dark arched doorway, soft; {HANDS}; exactly two people",
         lines=[("xuyan", "昨天是我讓妳一個人去的。下次，帶我。", "很穩")],
         motion="Xu Yan slips the silver ingot into his right sleeve as he speaks, his eyes staying on her; the young woman's back stays still",
         zh="過肩（阿令肩後拍許硯）、慢推（送門口圖）：前景右虛焦的阿令肩、髮髻、木簪與面巾細繩（不點名、不送圖，拍法 2）；許硯第一格已經下了一階到她的高度、手上拿著銀子，邊說邊把銀子收進右袖、看著她；不笑、不生氣（本集的心）。稿子『往下走一階』在第一格已經完成"),
    dict(loc="steps_c", cam="Over-the-shoulder close-up, slow push in", chars=["aling"], nospeak=["aling"], night="steps",
         comp=f"over-the-shoulder close-up: in the soft left foreground the back of one young man's shoulder in a faded blue-grey scholar's robe and the back of his black topknot, out of focus, unnamed; facing us beyond him {ALING}, {VEIL}, {STRAND}, framed from the chest up, her face three-quarter to screen left toward him, never the lens; taken aback and wary: brows a little drawn, eyes wavering; behind her the dark red doors, soft; {HANDS}; exactly two people",
         lines=[("aling", "你會拖累。我還得分神顧你。", "別開臉，不帶笑")],
         motion=f"A-ling turns her face away from him a little and lowers her eyes; {UNDERVEIL}; the young man's back stays still",
         zh="反打（許硯肩後拍阿令）、慢推（送門口圖）：前景左虛焦的書生肩與髮髻（不點名、不送圖）；阿令別開臉、眼睛往下（台詞放錄音，nospeak）。稿子『面巾邊緣像嘴角往上動了一點點』不寫：預設不笑，面巾下的笑寫了會變成露嘴（配音也寫明不帶笑）"),
    dict(loc="steps_c", cam="Close-up, slow push in", chars=["xuyan"], night="steps",
         comp=f"close-up of {XU_D}, framed from the chest up with space above his head, his face three-quarter to screen right, his eyes lowered a little, never the lens; tired, then quietly touched: brows easing, lips pressed shut; behind him the thick red pillar and the dark red doors, soft; he is the only person in the frame",
         lines=[("xitong", "叮。阿令，好感加七。", "冷，宣布"),
                ("xitong", "她嫌你拖累，還加七。宿主的運氣比本事好。", "冷，嫌棄")],
         panel=[("阿令 好感 +7 → 28", "affection")],
         motion=f"Xu Yan blinks once and the corners of his mouth slowly lift into a small closed-lip smile; {SILENT_HE}; he is listening, not speaking",
         zh="近景、慢推（送門口圖；拍法 11 不寫藍光，稿子『臉被淡藍光照亮』不照用）：許硯眨一下眼、嘴角慢慢往上（稿子『本鏡可以笑』，閉著嘴的笑）；全程嘴閉著（系統兩句）。本集的鬥嘴；面板「阿令 好感 +7 → 28」由剪接疊上。稿子『身後虛焦是轉過身的阿令』拿掉（畫面裡只有他）。稿子 c15 三句錄音加起來 10.17 秒（超過約 10 秒），拆成 s15（系統兩句）與 s15b（心裡話）"),
    dict(sid="s15b", loc="steps_c", cam="Medium close-up, slow push in", chars=["xuyan"], night="steps",
         comp=f"medium close-up of {XU_D}, framed from the chest up with space above his head, his left hand already resting lightly over the cuff of his right sleeve at his chest from the first frame, his face three-quarter to screen right, his eyes lowered to his sleeve, never the lens; wry and quietly pleased: a small closed-lip smile, one brow a little raised, lips pressed shut; behind him the white wall and the dark arched doorway, soft; he is the only person in the frame",
         lines=[("xuyan", "被嫌也加分，這筆帳我記住了。", "心裡話，錄得近、輕", "inner")],
         motion=f"Xu Yan pats his right sleeve once with his left hand, still smiling with his lips closed; {SILENT_HE}; he is thinking, not speaking",
         zh="中近景、慢推（送門口圖；c15 拆出來的後半）：許硯左手第一格已經輕按在右袖上（袖裡是銀子），拍一下，仍閉著嘴笑（稿子 c15『本鏡可以笑』）；全程嘴閉著（心裡話：被嫌也加分）。換成中近景、背景換成白牆拱門，跟 s15 接起來不跳"),
    dict(loc="steps", cam="Medium shot from behind, slow push in", chars=["tangxiaotang", "xuyan"], nospeak=["tangxiaotang"], night="steps",
         comp=alone(f"her right hand already raised before her at shoulder height from the first frame, her left arm holding {STACK} against her chest; half a step beyond her right shoulder, close enough that his left upper arm is within reach of her right hand, {XU_D}, framed from the waist up, his face three-quarter to screen left toward her, never the lens; still pleased: a small closed-lip smile, eyes soft; behind him the thick red pillar, soft; she stays in the middle of the frame the whole shot, her shoulders square to us; {HANDS}; exactly two people, the young woman in the middle seen only from behind",
                    "standing on the pale stone paving,"),
         lines=[("tangxiaotang", "她嫌你拖累，你還笑得出來？", "皺眉")],
         motion=f"her right hand pokes his left upper arm once with its fingertips, only her forearm moving, her head and shoulders still; {quiet('Xu Yan')}; {HEADSTILL}",
         zh="中景（從背後）、慢推（送門口圖）：唐小棠背影在畫面正中、頭不動，右手第一格已經舉在肩高，指尖戳一下他的左上臂、只動前臂、頭與肩不動（不寫單根手指：第 16 集單指會被讀成比中指）；許硯在她右肩後半步、手臂在她右手搆得到的地方（審稿必改 11：不逼她轉身），還帶著閉嘴的笑（稿子『許硯還在笑』），嘴閉著（nospeak）"),
    dict(loc="steps", cam="Medium shot, slow push in", chars=["xuyan", "laisan"], night="steps",
         comp=f"medium shot on the top step: on the left {XU_D}, standing, framed from the waist up, his right hand already gripping the back of the collar of {LAI_B}, who kneels on the top step on the right with his head down, from the first frame; Xu Yan's face three-quarter to screen left toward someone out of sight beyond the left edge of the frame, never the lens; dry and steady, not smiling: one brow a little raised, lips moving between words; Lai San's face turned down toward the stones, his lips pressed shut; behind them the dark red doors, soft; {HANDS}; exactly two people",
         lines=[("xuyan", "笑她肯說實話。走，帶人進去見縣太爺。", "平靜")],
         motion=f"Xu Yan hauls Lai San up to his feet by the collar as he speaks; {quiet('Lai San')}",
         zh="中景、慢推（送門口圖）：許硯第一格已經揪著跪在石階頂的賴三後領，邊說邊把他拉起來（朝畫左外看不到的人：唐小棠，不點名）；賴三嘴閉著。稿子『往大門走、後面阿令』不拍（一鏡一個動作；阿令不入鏡，兩張臉）；切公堂由剪接接上"),
    # ---- scene 2b: the court hall that morning (the floor crop for those below, the dais crop for Magistrate Hu).
    dict(chapter="縣衙公堂", loc="dais", cam="Low-angle medium shot, slow push in", chars=["huxianling"], night="hall",
         comp=f"low-angle medium shot from the floor of the court hall: in the soft left foreground the back of one small thin man in a checked grey-brown short jacket and an old cloth head wrap, kneeling on the grey stone tiles, his hands tied before him, seen only from behind, unnamed; beyond him Magistrate Hu, {HU}, sitting behind the long dark desk, framed from the waist up, his right hand already gripping {GAVEL} raised a hand's height above the desk from the first frame, his shoulders square to the desk like the picture, only his head turned three-quarter to screen left toward the kneeling man, never the lens; pompous and stern, not smiling: chin up, brows lifted, mouth drawn long between words; behind him only the plain white panels; {HANDS}; exactly two people",
         lines=[("huxianling", "大清早就押人上堂。賴三，你下了什麼藥？", "官腔")],
         motion="Magistrate Hu brings the wooden block down flat on the desk with one sharp knock and speaks; the kneeling man stays still",
         zh="低角度中景（從堂下往上）、慢推（送公案裁切 `set-xianya-gongtang-dais-l1`；整張公堂圖案上方掛著匾，會長字，不送）：前景左賴三跪著的背影（不點名、不送圖）；胡縣令（有帽翅的黑紗幞頭、藍綠圓領官袍）肩膀照圖正對桌子、只有頭轉向畫左，右手第一格已經舉著驚堂木（長方形木塊），一拍、官腔問。稿子的全景推軌改中景慢推（全景要帶上整張公堂）；許硯、唐小棠、阿令、趙捕頭、兩排衙役不拍（一鏡最多三張臉、唐小棠不露臉；衙役交給音效，第 19 集）"),
    dict(loc="hall_c", cam="High-angle medium close-up, slow push in", chars=["laisan"], night="hall",
         comp=f"high-angle medium close-up of {LAI_B}, kneeling on the grey stone tiles, framed from the chest up, his head wrap pushed askew, his tied hands raised before his chest, his face three-quarter to screen right toward someone out of sight beyond the upper right edge of the frame, where only the soft pillars and the lattice windows reach the edge, never the lens; he is the only person in the frame; cringing and shifty, not smiling: brows up, eyes darting sideways, lips moving fast between words; behind him the grey stone tiles, soft",
         lines=[("laisan", "瀉藥！小的全招，是有人給銀子叫我下的！", "磕頭")],
         motion="Lai San bobs his head down in two quick bows as he speaks",
         zh="高角度中近景、慢推（送公堂地面裁切 `set-xianya-gongtang-floor-l1`）：賴三跪在灰石板上、頭巾歪著、綁著的手舉在胸前，連點兩下頭像磕頭、眼睛亂瞄，朝畫右上外看不到的人（縣令）說。稿子『額頭往地上磕兩下』改點頭（額頭貼地就看不到嘴與臉）"),
    dict(loc="dais", cam="Medium close-up, slow push in", chars=["huxianling"], night="hall",
         comp=f"medium close-up from below the desk: Magistrate Hu, {HU}, sitting behind the long dark desk, framed from the chest up with clear space above his hat, his right hand already resting on {GAVEL} on the desk from the first frame, his shoulders square to the desk like the picture, only his head turned three-quarter to screen left toward the floor below the desk, never the lens; sly and uneasy, not smiling: eyes sliding sideways, then narrowing, lips moving between words; behind him only the plain white panels",
         lines=[("huxianling", "既然招了，第三十日午時，縣城廣場公審！", "眼珠一轉")],
         motion="Magistrate Hu lifts the wooden block and brings it down once on the desk as he names the day",
         zh="中近景、慢推（送公案裁切）：胡縣令肩膀正對桌子、只有頭轉向畫左，眼珠一轉，舉起驚堂木一拍、訂下日子。稿子『額頭冒汗、手指在案上敲兩下』拿掉（拍法 12 皮膚上不寫細小東西；一鏡一個動作）"),
    dict(loc="hall_c", cam="Close-up from behind, slow push in", chars=["tangxiaotang"], nospeak=["tangxiaotang"], night="hall",
         comp=alone(f"both her hands low at her sides; beyond her, soft, the dark red-brown pillars and the bright lattice windows; {HANDS}",
                    "standing on the grey stone tiles,", frame="framed from the shoulders up", shot="close-up"),
         lines=[("tangxiaotang", "第三十日？那許記就得封到賭約最後一天！", "不笑")],
         motion=f"her shoulders square sharply once; {HEADSTILL}",
         zh="近景（從背後）、慢推（送公堂地面裁切）：唐小棠後腦與肩在畫面正中、正背對鏡頭、頭不動，肩膀一挺（nospeak，拍法 3）。稿子『往前一步、手指一撥腰間算盤「喀」』：算盤只在插鏡（拍法 20），「喀」交給音效"),
    dict(loc="dais", cam="Low-angle close-up, slow push in", chars=["huxianling"], night="hall",
         comp=f"low-angle close-up from below the desk: Magistrate Hu, {HU}, already leaning back in the dark wooden armchair behind the long dark desk from the first frame, framed from the chest up with clear space above his hat, {GAVEL} on the desk before him, his shoulders square to the desk like the picture, only his head turned three-quarter to screen left toward the floor below, never the lens; falsely genial: a broad false smile, heavy cheeks shaking, eyes cold, lips moving between words; behind him only the plain white panels",
         lines=[("huxianling", "公審要全城百姓都來看，急什麼？退堂！", "假笑")],
         motion="Magistrate Hu gives his bulging left sleeve one lazy wave toward the right edge of the frame as he speaks",
         zh="低角度近景、慢推（送公案裁切）：胡縣令第一格已經往椅背靠著，假笑（稿子『本鏡可以假笑，臉頰跟著抖』），甩一下袖子說"),
    dict(loc="hall_c", cam="Close-up, slow push in", chars=["xuyan"], night="hall",
         comp=f"close-up of {XU_D}, standing on the grey stone tiles, framed from the chest up with space above his head, his left hand already pressed over the cuff of his right sleeve at his chest from the first frame, his face three-quarter to screen left toward someone out of sight beyond the left edge of the frame, never the lens; that side of the frame is only the soft dark red-brown pillar and the lattice windows all the way to the edge, and he is the only person in the frame; low and hard, not smiling: eyes narrowed, lips moving low between words",
         lines=[("xuyan", "他故意拖到最後一天。拖得越久，越好動手腳。", "低聲")],
         motion="Xu Yan leans his head a little toward the left as he speaks low, his left hand staying on his right sleeve",
         zh="近景、慢推（送公堂地面裁切）：許硯左手第一格已經按在右袖口上（袖裡是銀子），頭往畫左一側、壓低聲音朝畫左外看不到的人（唐小棠，不點名）說；那一側到邊緣只有紅柱與格窗、畫面裡只有他"),
    dict(loc="hall", cam="Medium shot, slow push in", chars=["aling"], nospeak=["aling"], night="hall",
         comp=f"medium shot of {ALING}, {VEIL}, {STRAND}, standing beside a thick dark red-brown pillar on the grey stone tiles, framed from the waist up, {SLEEVE}, her face three-quarter to screen right toward someone out of sight beyond the right edge of the frame, never the lens; she is the only person in the frame; quiet and decided: eyes level, brows still; behind her the bright lattice windows and the low white panel, soft; {HANDS}",
         lines=[("aling", "家裡只剩小禾和秦霜，我回柳溪守著。", "隔著面巾")],
         motion=f"A-ling tips her head once toward the left, toward the way out; {UNDERVEIL}",
         zh="中景、慢推（送公堂地面裁切）：阿令（面巾、碎髮）站在紅柱邊，朝畫右外看不到的人（許硯、唐小棠，不點名）往畫左（出去的方向）一偏頭（台詞放錄音，nospeak）。稿子『站在大門口、前景門框、兩人走過來』不拍：兩張公堂圖都沒有門（第 27 集 s24 同理），一鏡最多三張臉、唐小棠不露臉"),
    dict(loc="hall_c", cam="Close-up, slow push in", chars=["xuyan"], night="hall",
         comp=f"close-up of {XU_D}, standing on the grey stone tiles, framed from the chest up with space above his head, his left hand already resting over his right sleeve from the first frame, his face three-quarter to screen left toward someone out of sight beyond the left edge of the frame, never the lens; that side of the frame is only the soft dark red-brown pillar and the lattice windows all the way to the edge, and he is the only person in the frame; resolved, not smiling: steady eyes, lips moving clearly between words",
         lines=[("xuyan", "好。銀子我收著不交。今晚明晚，我都去牢外守著。", "平靜")],
         motion="Xu Yan gives one small nod as he begins to speak, his eyes staying on that spot beyond the left edge",
         zh="近景、慢推（送公堂地面裁切）：許硯開口時點一下頭，手放在右袖上，朝畫左外看不到的人（唐小棠，不點名）說（結尾）。稿子『身後虛焦是大門外的亮光與阿令走遠的背影』不拍（圖上沒門，畫面裡只有他）；『對門外點頭再轉回來』只留點頭"),
    # ---- scene 3: the twenty-ninth night, the county jail gate (set-dalao-l1 and two crops).
    dict(chapter="大牢門外", loc="jail", cam="Wide shot, slow push in", chars=["xuyan"], night="jail",
         comp=f"wide shot at standing eye height, like the picture: on this side of the gate, pressed close against the bars at its left end, {XU_N}, framed from the knees up, his body turned toward the bars, half his face already peering between two bars into the torchlit room from the first frame, never the lens; tense and watchful: brows drawn, eyes narrowed, lips pressed shut; he is the only person in the frame; {HANDS}",
         lines=[("xuyan", "第二夜了……魏家要動手，就是今晚。", "心裡話，錄得近、輕", "inner")],
         motion=f"Xu Yan leans half his face a little closer to the gap between two bars; {SILENT_HE}; he is thinking, not speaking",
         zh="全景、慢推（人眼高、照圖；送大牢 `set-dalao-l1`，聖經拍法 24）：許硯（外披舊灰外衣、左手一盞小陶油燈、右手掌罩著火）貼在柵門左端，第一格已經探出半張臉往柵縫裡看，再湊近一點；全程嘴閉著（心裡話）。稿子『躲在石柱後』圖上沒有石柱：照圖改成貼在柵門左端（拍法 29）；柵欄照圖寫『粗方深色』、不寫材質（聖經寫木、圖是協調者挑定的深色柵，圖說了算）"),
    dict(loc="jail_g", cam="Point-of-view medium shot through the bars, slow push in", chars=["sunzhanggui", "zhaobutou"], night="jail",
         comp=f"point-of-view medium shot through the thick square dark bars of the gate, the bars soft in the foreground: beyond them in the torchlit stone room, on the left {SUN}, standing, framed from the waist up, {FOODBOX}, carried in his right hand by its bent handle, his left hand already holding {POUCH} out from the first frame, his face three-quarter to screen right toward Zhao Butou, never the lens; smooth and genial: a thin pleasant smile, eyes half lidded, lips moving slowly between words; on the right {ZHAO}, standing, framed from the waist up, his right palm already held out under the pouch, his face three-quarter to screen left toward Sun Zhanggui, never the lens; sly, not smiling, his lips pressed shut; {HANDS}; exactly two people",
         lines=[("sunzhanggui", "趙爺辛苦，少爺給賴三送頓飯。", "笑咪咪")],
         motion=f"Sun Zhanggui lays the cloth pouch in Zhao Butou's palm, and Zhao Butou's fingers close over it; {quiet('Zhao Butou')}",
         zh="主觀（許硯從柵縫看進去）、慢推（審稿必改 6：改送沒有鎖的 `set-dalao-bi-l1`，場景句照它寫柵欄、火光石牆、小木格窗與一支火把；交布袋不被輪盤鎖與門板擋住）：柵欄虛焦在前景；柵門裡火光的石室，左邊孫掌櫃右手提著食盒（兩層圓形深色漆木、彎木提把、素的，聖經拍法 24），左手把一個小布袋放進趙捕頭攤開的手掌，趙捕頭握起來（嘴閉著）；孫掌櫃『笑咪咪』（稿子）說。賴三從牢裡往外看不拍（拍法 24：這場四個有名字的人，賴三只露背影與手，或拆鏡）；趙捕頭拿鑰匙串開牢門不拍（鑰匙聲交給音效；拍法 16、17 腰間什麼都沒掛）"),
    dict(loc="jail_d", cam="Insert close-up at eye level, slow push in", chars=[], night="jail",
         comp=f"insert close-up at eye level, looking in between two thick square dark bars, the shot opens directly on {FOODBOX} standing on the stone floor just beyond the bars and filling the gap between the two bars in the lower half of the frame, from its very first frame, its top tier already lifted a hand's height off it by a thin hand in a green satin sleeve cuff, the lower tier below packed tight with small silver ingots, their tops smooth and plain, gleaming in the torchlight; only the bars, the box, the ingots, the hand and its sleeve cuff are in the frame",
         motion=NOBODY + "the green-sleeved hand lifts the top tier up and away out of the frame, leaving the lower tier full of silver in the torchlight",
         zh="平視插鏡、慢推（審稿必改 7 與建議 4：圖是平視，第一格就是兩根柵之間、塞滿下半部的食盒；送免費新圖 `set-dalao-di-zuo-l1`：三根柵、左邊石牆、下三分之一是石地，比 `-di-l1` 地面多，全尺寸看過）：綠緞袖口的瘦手第一格已經把食盒上層提起一點，往上提出畫面，下層塞滿頂面平滑、沒有字的小銀錠（無台詞）。稿子『牢房稻草上、上層一碗白飯一盤肉』改成柵門裡的石地、上層只拍被提走（許硯在柵外看得到的，c32 的『他看得到的』照這個）；不寫『打開』（不寫 open）"),
    dict(loc="jail_b", cam="Medium close-up through the bars, slow push in", chars=["sunzhanggui"], night="jail",
         comp=f"medium close-up through the thick square dark bars: beyond them {SUN}, crouching on the stone floor, framed from the chest up with space above his head, his right hand already resting on the soft shoulder of one small thin man in a checked grey-brown jacket at the left edge of the frame, seen only from behind, his tied hands before him, unnamed, from the first frame, his face three-quarter to screen left, leaning close to that man's ear, never the lens; smooth and cold, not smiling: eyes half lidded, lips moving low and slow between words; behind him the torchlit pale stone wall, soft; {HANDS}; exactly two people",
         lines=[("sunzhanggui", "明天公審，你照我教的說，這些全是你的。", "壓低聲音")],
         motion="Sun Zhanggui pats the thin man's shoulder twice as he speaks low into his ear; the thin man's back stays still",
         zh="中近景（隔著柵欄）、慢推（送免費新圖 `set-dalao-bi-l1`：柵欄後火光照著的石牆與一支火把）：孫掌櫃蹲在石地上，右手第一格已經搭在畫左緣賴三的肩上（只見背影與綁著的手，不點名、不送圖，拍法 24），湊到他耳邊拍兩下、壓低聲音說"),
    dict(loc="jail_b", cam="Close-up through the bars, slow push in", chars=["laisan"], night="jail",
         comp=f"close-up through the thick square dark bars: beyond them {LAI_A}, hunched on the stone floor, framed from the chest up with space above his head, wavering warm torchlight on his thin face, his face three-quarter to screen right, his eyes on something low below the lower edge of the frame, never the lens; greedy and afraid, not smiling: eyes wide and fixed, lips pressed shut; he is the only person in the frame; behind him the torchlit pale stone wall, soft",
         motion=f"Lai San slowly nods twice, his eyes staying on the silver below the frame; {SILENT_HE}",
         zh="近景（隔著柵欄）、慢推（送柵欄與石牆的免費裁切）：賴三縮在石地上，火光在尖臉上晃，眼睛盯著畫面下方外的銀子，慢慢點兩下頭；嘴閉著（無台詞；拍法 24 拆鏡：他的臉只在這一鏡、只有他一個人）。稿子『吞一口口水』拿掉（一鏡一個動作）"),
    dict(loc="jail_g", cam="Medium shot, slow push in", chars=["xuyan", "zhaobutou"], night="jail",
         comp=f"medium shot on this side of the gate, the thick square dark bars behind them: on the left {XU_NC}, standing, framed from the waist up, his face three-quarter to screen right toward Zhao Butou, never the lens; still and cool, not smiling, his lips pressed shut; on the right {ZHAO}, standing close, framed from the waist up, his left forearm already held straight out across Xu Yan's chest from the first frame, his face three-quarter to screen left toward Xu Yan, never the lens; sidelong and cold, not smiling: eyes narrowed sideways, lips moving between words; {HANDS}; exactly two people",
         lines=[("zhaobutou", "許秀才，探監的時辰過了，明天廣場見。", "斜眼")],
         motion=f"Zhao Butou presses his forearm a little firmer against Xu Yan's chest as he speaks; {quiet('Xu Yan')}",
         zh="中景、慢推（審稿必改 6：改送沒有鎖的 `set-dalao-bi-l1`）：柵門外，左邊許硯（舊灰外衣，油燈不寫：一鏡一個動作，空手）嘴閉著；右邊趙捕頭第一格已經出了柵門、左前臂橫擋在許硯胸前，斜眼說。稿子『伸出鐵尺橫擋』改前臂（拍法 16、17：不寫兵器與職稱字，腰間什麼都沒掛）"),
    dict(loc="jail_b", cam="Close-up, slow push in", chars=["xuyan"], night="jail",
         comp=f"close-up of {XU_NC}, framed from the chest up with space above his head, a forearm in a plain black cotton sleeve reaching in from the right edge of the frame, held across his chest at the lower edge from the first frame, the corner of one crumpled scrap of {YPAPER} already showing at the edge of his right sleeve cuff, his face three-quarter to screen right toward someone out of sight beyond the right edge of the frame, never the lens; calm and cold, not smiling: steady eyes, lips moving evenly between words; behind him the thick square dark bars and the torchlit stone beyond, soft",
         lines=[("xuyan", "好，明天廣場見。讓他說，說得越多越好。", "不笑")],
         motion="Xu Yan lifts his eyes from the black-sleeved forearm to that spot beyond the right edge of the frame as he speaks",
         zh="近景、慢推（送柵欄與石牆的免費裁切）：畫面下緣一條黑袖前臂橫在他胸前（趙捕頭不入鏡）；右袖口第一格已經露出一角粗黃紙（空白，拍法 27）；許硯從前臂抬眼看畫右外那一點、不笑地說（審稿必改 3：不寫『那個男人』）（結尾）。稿子『抽出黃紙一角又塞回去』只留露出的一角（一鏡一個動作）"),
    # ---- scene 4: the thirtieth day at noon, the town square (set-guangchang-l1 painted and cropped).
    dict(chapter="縣城廣場", loc="square", cam="Wide shot, slow push in", chars=["huxianling", "xuyan"], night="square",
         comp=f"wide shot at standing eye height, like the picture: in the soft foreground, seen from behind and out of focus, {TOWNS}; beyond them on the low stone platform, small: Magistrate Hu, {HU}, sitting behind the long desk draped in red cloth, his face turned down toward the kneeling man, never the lens; in the middle front of the platform the back of one small thin man in a checked grey-brown jacket kneeling, his hands tied, unnamed; on the left side of the platform {XU_D}, standing alone, his face three-quarter to screen right toward the desk, never the lens; the dark wooden armchair on the right of the platform empty; nobody on the platform is speaking, their lips closed; {HANDS}; exactly eleven people",
         motion="the eight townspeople lean forward together and crane their necks toward the platform; the people on the platform stay still",
         zh="全景、慢推（人眼高、照圖；送免費新圖 `set-guangchang-tai-l1`：廣場圖塗掉堂屋門口兩塊有筆畫的黃板與黃色架子、裁掉太陽）：前景虛焦八個背對的鎮民在繩子後（拍法 25，各穿不同的衣服），往前擠、伸長脖子；台上胡縣令在紅布案後、賴三背對跪在台中央（不點名、不送圖）、許硯站在台上左邊；右邊的椅子空著（魏少卿 s35 才入座）（無台詞）。稿子的高角度慢降改人眼高慢推（圖是平視）；兩排衙役與水火棍頓台板交給音效"),
    dict(loc="square_l", cam="Medium shot from behind, slow push in", chars=["tangxiaotang"], nospeak=["tangxiaotang"], night="square",
         comp=alone(f"{STACK} already held in her left arm against her chest from the first frame, only its pale edge showing at her side; beyond her, soft, the edge of the low stone platform and the plain wooden chest beside it in the low winter sun; she is the only person in the frame, seen only from behind; {HANDS}",
                    "standing on the packed pale earth below the left side of the platform,"),
         lines=[("tangxiaotang", "魏少卿也來了，就坐在台子右邊。", "小聲，抬頭對許硯")],
         motion=f"her left arm hugs the stack of paper tighter against her chest; {HEADSTILL}",
         zh="中景（從背後）、慢推（送免費新圖 `set-guangchang-zuo-l1`：台子左下的地面與木箱）：唐小棠背影在畫面正中、頭不動，左臂把帳本抱緊（nospeak，拍法 3）；畫面裡只有她。稿子『踮腳抬頭看許硯、往台子右邊一瞄』不拍（頭不動）；『背後人群擠得很緊』不拍（朝鏡頭的臉會變多、會長出分身）"),
    dict(loc="square_c", cam="Low-angle medium close-up, slow push in", chars=["weishaoqing"], night="square",
         comp=f"low-angle medium close-up of {WEI}, sitting in a dark wooden armchair, framed from the chest up with space above his head, {FAN}, its tip already resting on his knee from the first frame, his face three-quarter to screen left toward someone out of sight beyond the left edge of the frame, never the lens; that side of the frame is only the bare branches and the clear blue sky all the way to the edge, and he is the only person in the frame; lazy and mocking: a thin lazy smile, eyes half lidded, lips moving slowly between drawled words; behind him the bare branches of a tree and the clear blue sky",
         lines=[("weishaoqing", "許秀才，今天第三十日，你的鋪子還封著呢。", "懶懶地，本鏡可以笑")],
         motion="Wei Shaoqing taps the closed fan twice on his knee as he speaks",
         zh="低角度中近景、慢推（送免費新圖 `set-guangchang-shu-l1`：一棵禿樹與屋頂、晴空）：魏少卿坐在深色木椅上（稿子『雕花』不寫：雕花會長字），合著的扇子在膝上敲兩下（拍法 30：扇子一直合著；稿子『摺扇打開、搧兩下、翹腳』不拍），懶懶地笑著（稿子『本鏡可以笑』）朝畫左外看不到的人說"),
    dict(loc="square_c", cam="Low-angle close-up, slow push in", chars=["huxianling"], night="square",
         comp=f"low-angle close-up of Magistrate Hu, {HU}, sitting behind the long desk draped in red cloth, framed from the chest up with clear space above his hat, his right hand already gripping {GAVEL} raised a hand's height above the red cloth from the first frame, his face three-quarter to screen right toward the middle of the platform below, never the lens; pompous and uneasy, not smiling: chin up, brows lifted, mouth drawn long between words; behind him the bare branches of a tree and the clear blue sky; he is the only person in the frame",
         lines=[("huxianling", "賴三！當著全城百姓，誰指使你下藥？", "拖長音")],
         motion="Magistrate Hu brings the wooden block down hard on the desk with one loud knock and speaks",
         zh="低角度近景、慢推（送禿樹與晴空的裁切）：胡縣令（有帽翅的黑紗幞頭、藍綠官袍）在紅布案後，右手第一格已經舉著驚堂木（長方形木塊，原版必修：不是法槌），一拍、拖長音問（朝畫右下台中央的賴三）。稿子『額頭冒汗』不寫（拍法 12）。他跟孫掌櫃不同鏡（原版必修）"),
    dict(loc="square_r", cam="Medium close-up, slow push in", chars=["sunzhanggui"], night="square",
         comp=f"medium close-up of {SUN}, standing on the packed pale earth below the right side of the platform, framed from the chest up with space above his head, both his hands already tucked into his wide sleeves before him from the first frame; in the soft left foreground the shoulder of one townsman in an ochre robe and a head cloth, seen from behind, out of focus, unnamed; his face turned up three-quarter to screen left toward the platform above beyond the upper left edge of the frame, never the lens; calm and cold, not smiling: eyes half closed, lips pressed shut; behind him the long low tiled building and its plank doors, soft; {HANDS}; exactly two people",
         motion=f"Sun Zhanggui gives one small slow nod up toward the platform; {SILENT_HE}",
         zh="中近景、慢推（審稿必改 9：改送免費新圖 `set-guangchang-you-wu-l1`：一排瓦屋與木板門、黃土地與長樹影，沒有那把空椅子）：孫掌櫃兩手攏在袖子裡，前景左一個鎮民的肩（背影、虛焦、不點名），半閉的眼往畫左上台上一看、輕輕點一下頭；嘴閉著（無台詞）。原版必修：他跟胡縣令不同鏡（s36 縣令、s37 孫掌櫃）"),
    dict(loc="square_c", cam="Low-angle close-up, slow push in", chars=["laisan"], night="square",
         comp=f"low-angle close-up of {LAI_B}, kneeling, framed from the chest up with space above his head, his tied hands already raised before his chest from the first frame, his face three-quarter to screen left toward someone out of sight beyond the left edge of the frame, never the lens; that side of the frame is only the bare branches and the clear blue sky all the way to the edge, and he is the only person in the frame; trembling and loud, not smiling: brows up, eyes wide, lips moving hard in a shout between words; behind him the bare branches of a tree and the clear blue sky",
         lines=[("laisan", "是許家逼我下的毒，要栽贓給魏記！", "發抖，大聲")],
         motion="Lai San thrusts both his tied hands out together toward the left edge of the frame as he shouts",
         zh="低角度近景、慢推（送禿樹與晴空的裁切）：賴三跪著，綁著的兩手第一格已經舉在胸前，邊喊邊一起往畫左外（許硯，不點名）一戳（不寫單根手指：第 16 集單指會被讀成比中指）（結尾的台詞，懸念 → 第 29 集）。稿子『額頭冒汗』不寫（拍法 12）"),
    dict(loc="square", cam="Wide shot, slow push in", chars=["huxianling", "weishaoqing", "xuyan"], night="square",
         comp=f"wide shot at standing eye height, like the picture: in the soft foreground, seen from behind and out of focus, {TOWNS}; beyond them on the low stone platform, small: Magistrate Hu, {HU}, sitting behind the long desk draped in red cloth, his face turned down toward the kneeling man, his lips closed, never the lens; in the middle front of the platform the back of one small thin man in a checked grey-brown jacket kneeling, his tied hands lowered before him, unnamed; in the dark wooden armchair on the right of the platform Wei Shaoqing, small, in his sapphire-blue brocade robe, sitting back with his closed fan on his knee, his lips closed, never the lens; on the left side of the platform {XU_D}, standing apart, framed full figure, his hands at his sides, his face three-quarter to screen right, never the lens; calm and still, not smiling: level eyes, lips pressed shut; {HANDS}; exactly twelve people",
         motion=f"several of the townspeople raise an arm and point toward the young man on the platform; Magistrate Hu, the kneeling man and Wei Shaoqing in the armchair stay still; Xu Yan stands still and does not move; {quiet('Magistrate Hu, Wei Shaoqing and Xu Yan', 'their', plural=True)}",
         zh="全景、慢推（人眼高、照圖；送廣場寬景裁切）：前景虛焦八個背對的鎮民（各穿不同的衣服），幾個人舉手指向台上；台上胡縣令在紅布案後、賴三背對跪在台中央（不點名、不送圖）、魏少卿坐在台右的木椅上（審稿必改 2：接點 28→29，同一刻，送胡縣令與魏少卿的圖、拿掉許硯角度圖、十二人），都不動、嘴閉著；台上左邊許硯站著、一動不動、不笑、嘴閉著（無台詞；本集最後一鏡，留懸念的尾，接點 28→29：第 29 集第一鏡他平靜地舉起一塊糖糕）。稿子的搖鏡改慢推；唐小棠（會轉頭露臉）與兩排衙役交叉水火棍不拍；人聲交給音效"),
]

HEAD = [
    "- 重製版 r2、真人版（站主 2026-11-11「之後都用真人版」）：照 `docs/videos/zhong-tian-qu-qi-e028-r2/script.md`（c01–c39 對應 s01–s39，c03 拆成 s03、s03b，c15 拆成 s15、s15b；含「這版改了什麼」「2026-11-06 審稿後的修改」與「真人版的改動（2026-11-17）」）；台詞一字不改，只改拍法；每鏡一個看得見的動作、一句一筆不拆半句、預設不笑。篇章設定 `production/r2-bible-e021-e030.md`（拍法 1–30 條）。第 3 篇章〈搶親〉第八集。",
    "- 內部工作編號 928（`hailuo/{ff,clips}-dh-e928.json`、`colab/runs/e928/extras.json`、`colab/runs/e928-live/spec.json`，工作資料夾 `~/mokaair-work/videos/zhong-tian-qu-qi-e928-dh/`）；發布 slug `zhong-tian-qu-qi-e028-r2`。不放集數、不放片名卡；s01 接第 27 集 s37（接點 27→28：同一刻，賴三往打手身後一縮；阿令的短刀一直套在木鞘裡）；s39 交給第 29 集（接點 28→29：同一刻，許硯平靜地舉起一塊糖糕）。",
    "- 照第 27 集審稿後的寫法與第 21–26 集挑片學到的一開始就照做：`OFFSCREEN_SPEECH = False`；背影、前景、面巾下或畫外的人說話時，每張朝鏡頭的臉都寫不說話、嘴閉著；**對畫外的人說話寫「朝畫左／右外看不到的人」，那一側到邊緣只有景、畫面裡只有他一個人，不點名、不描述不在畫裡的人**（提示詞與精修文字都一樣）；掛著的東西不點名；不寫 open；道具與接觸寫在第一格；紙一律空白；寫人數，群眾每人一套不同的衣服。",
    "- **唐小棠不露嘴說話、不露臉**（拍法 3）：她五句（s08、s11、s16、s21、s34）全從背後拍、畫面正中、正背對鏡頭、頭不動、剛好兩顆丸子；spec 拿掉她的圖與身分句。算盤本集沒有（拍法 20；c21 的「喀」交給音效）。",
    "- **阿令整集戴面巾**（拍法 21）：送 `aling-veil-portrait-l1`、不送角度圖；台詞全放錄音（nospeak）；短刀只在打鬥三鏡（s02、s03、s03b），一律寫「套在素木鞘裡、刀柄連鞘一整塊閉著的深色木頭」（接點 27→28：從頭到尾不出鞘；不寫 dagger、blade、draw）。打鬥照拍法 22 拆鏡：一鏡一個打手、一個動作，不給打手正臉，刀不碰人。",
    "- **衙役與趙捕頭**（拍法 16、17）：不寫職稱字；鐵尺改前臂、鑰匙串交給音效；門口打呵欠的衙役、公堂與廣場的兩排衙役不拍（音效）。**胡縣令每鏡都戴有帽翅的黑紗幞頭**，公堂只送公案裁切、肩膀正對桌子只轉頭；跟孫掌櫃不同鏡。**大牢**（拍法 24）：送挑定的 `set-dalao-l1`，柵欄照圖寫粗方深色、不寫材質；整場在柵門內外拍，賴三的臉只在 s30 單人。",
    "- **場景圖說了算**（拍法 29，協調者 2026-11-17 決定，每張放大看過）：後巷 `set-chouduan-ye-xiang-l2`（第 27 集）；縣衙門口 `set-xianya-steps-l2`（第 19 集）；公堂地面與公案裁切（第 18 集）；大牢 `set-dalao-l1`；**新的免費圖八張**：`set-xianya-steps-shi-l1`、`set-dalao-bi-l1`、`set-dalao-di-l1`、廣場的 `set-guangchang-tai-l1`、`-tai-zhong-l1`（給第 29 集）、`-shu-l1`、`-zuo-l1`、`-you-l1`（廣場圖先塗掉堂屋門口兩塊有筆畫的黃板與黃色架子）。**不需要試鏡**。",
    "- 長鏡要買的秒數（BUY）：照錄音核過（見 `r2.py` 的 BUY 註解）。",
    "- **表上的「秒」欄是 lint 估法**，比錄音短；剪接以錄音的人聲長度為準。",
]
FOOT = [
    "- **參考圖**（`assets/refs-live/`）：許硯（l1、angle-a；帶笑的 angle-b 整集不送）、阿令（面巾 `aling-veil-portrait-l1`，不送角度圖）、賴三 l1、趙捕頭 l1、魏少卿 l1、胡縣令 l1、孫掌櫃 l1。唐小棠整集不送圖。兩個打手、鎮民、前景的肩與背影、手都不送圖。場景見上面。",
    "- 共用檔：程式都沒改（畫面上說話的人都在 `build-r2.py` 的 `EN`；本集沒有小角色說話）；`gen-dh.mjs`、`pilot.py`、`cast.json` 不動；`refs-live` 加八張免費圖（都是新 id）與 README 一段。趙捕頭的職稱字、胡縣令的帽子、孫掌櫃的笑眼、阿令的紅唇由 `colab/runs/e928/extras.json` 換掉；精修文字的 CG 立領句、唐小棠的名字與『Constable Zhao』由本檔結尾的 `live_clips()` 在 build 後從 `clips-dh-e928.json` 換掉。",
    "- `colab/runs/e928/extras.json`（照第 27 集）與 `colab/runs/e928-live/spec.json`（`mkspec.py` 產生；種子 9281101／9281102）。",
    "- 免費準備：scratchpad `prep928.sh`（`DRY=1 … st1-ep.sh 928` → `pilot.py` → `retake.py` → `colab-jobs.json` 加 output_path、套 swap_pictures（絕對路徑）→ 逐鏡查送的場景圖與人物圖 → 精修用的分隔句 → `preflight-prompts.py` → 否定名詞、會長字的名詞、掛著的東西、open、『畫外的年輕女子』與『點名的畫外人』掃描）。",
    "- 配樂：後巷短促的打鬥鼓點，s04 木棍落地一個重拍、之後只剩夜風；縣衙門口晨光的暖 cue（s13–s16 輕輕的），公堂轉低鼓，s20 訂日子一個重音；大牢低的懸疑 pad 與火把劈啪，s28 食盒一個重音；廣場人聲 bed 加慢慢壓上來的低鼓，s38 指認一個大重音。音效見 script.md〈音樂與音效〉（另外：打手往前一步、門口的雞叫與打呵欠、s11 跺腳、s21 算盤「喀」、鑰匙串與牢門、兩排衙役與水火棍、人群嘩然，都交給音效）。",
]

# Long shots: seconds to buy. Filled in after the recordings (see the end of this comment block).
# Measured 2026-11-17 against the 33 kept recordings (~/mokaair-work/videos/zhong-tian-qu-qi-e928-dh/audio; wave length and
# silencedetect -35 dB speech span; e013's test: a shot holds (buy - 0.3) x 1.1 s of speech, half a second between lines, so
# 5 s holds 5.17 s, 6 s 6.27 s, 8 s 8.47 s). faster-whisper medium read every take back, one clip per process, numpy input,
# once plain and once with the previous line and the line as context (audio/fw928.txt, fw928-retake.txt; audio/README-retakes.txt).
# The script's c15 (system 2.17 s + 0.5 + 3.98 s + 0.5 + his thought 3.02 s = 10.17 s) runs over about 10 s: split into s15 (the
# system's two lines, 6.65 s: buy 8) and s15b (his thought, 3.02 s: 6).
# 8 s: s18 (a17 Magistrate Hu's drawl, speech 6.35 s), s20 (a19, 7.06 s), s35 (a31 Wei Shaoqing's drawl, 6.60 s), s36 (a32,
#      7.40 s), s15 (above), s39 (the episode's last shot: the hook needs a held tail, as e923-e927).
# 6 s: every other speaking shot. The tightest: s22 (a21's retake 6.25 s; a short buy suits a shot that may laugh), s29 (a27 5.48 s),
#      s25 (a24's retake 4.84 s), s21 (a20 4.72 s).
# 5 s: the silent inserts s04, s10, s28 as gen-dh buys them, and the silent shots s03b (one fall), s30 (two nods), s37 (one nod).
# s03 (the swing), s06 (the silver pulled out) and s33 (the wide) keep gen-dh's 6. No shot runs over about 10 s after the split.
BUY = {"s15": 8, "s18": 8, "s20": 8, "s35": 8, "s36": 8, "s39": 8, "s03b": 5, "s30": 5, "s37": 5}


# ---- the refine text (e022 review 必改 12, as e023-e027): hailuo/clips-dh-e928.json column 0 is the motion text
# refine-prep.py sends with a picked d1 draft. gen-dh.mjs opens every clip that lists tangxiaotang with the CG-era "Tang
# Xiaotang's high stand-up collar stays closed at her throat." and names her in "<names> shown in <Picture 1>"; in a back shot
# that draws the collar back and turns her face to the lens. Her shots are all back shots: the sentence goes and her name becomes
# "the young woman seen only from behind", and (e027 review 建議, taken here) "keeps the same face, hair, costume and props" of a
# back shot alone becomes "keeps the same hair, costume and props as the first frame, her back to us" (with Xu Yan: "..., the
# young woman's back to us"). build-r2.py's speaking clause names Zhao Butou
# "Constable Zhao" (bible rule 17): the refine text says "Zhao Butou". Column 1 is recomputed.
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
            if names:
                text = text.replace("keep the same face, hair, costume and props as the first frame", "keep the same face, hair, costume and props as the first frame, the young woman's back to us", 1)
            else:
                text = text.replace("keeps the same face, hair, costume and props as the first frame", "keeps the same hair, costume and props as the first frame, her back to us", 1)
            assert "back to us as the first frame" not in text and ("back to us" in text), key
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
