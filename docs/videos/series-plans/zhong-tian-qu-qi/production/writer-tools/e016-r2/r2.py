"""Episode 16 remake (r2): the writer spec for ../e001-r2/build-r2.py. Source: docs/videos/zhong-tian-qu-qi-e016-r2/script.md
(c01-c42 = s01-s42; the CG-era r2 script of PR #2024), including its sections 「這版改了什麼」, 「2026-11-06 審稿後的修改」 and
「真人版的改動（2026-11-15）」, which override the tables. Every line is the script's, word for word; only the staging changes.
Bible: production/r2-bible-e011-e020.md (rules 1-18).

Live action from the first draft, written the way e015-r2/r2.py stands AFTER its independent review (review.md in ../e015-r2)
and the e913-e915 picking lessons (colab/runs/e91{3,4,5}-live/{review-picks-a,review-picks-b,picks-merged}.tsv,
e913-live/pick-review.md, e914-live/fix1 and e915-live/fix1/mkspec.py):
- OFFSCREEN_SPEECH = False (bible rule 15): every shot with an off-screen line, a thought or a system line writes the silence
  of each person on screen (quiet(), SILENT_HE), after the action.
- Bible rule 18: nothing is negated by name. Backgrounds say what is there; the long things people hold are written by their
  shape (the punting poles: plain green bamboo, smooth and round along their whole length, ends cut flat); paper is blank,
  thick and lit from the front or the side, never from behind; a face that must not smile gets things it does, held after
  the last word. extras.json keeps only "no subtitles, captions or text" and the clear-air line; Sun Zhanggui's cast
  sentence loses "(no jade balls)" (a negated noun) and "smiling".
- Hands and props are placed in the composition sentence (the first frame), each prop attached to its owner's named hand
  (e915 s41: Tang Xiaotang's abacus drifted into Lai San's hand): the slip in the man's fingers (s01), the mats in the hands
  that hold them, the punting pole in Qin Shuang's hands, the brush in Xu Yan's right hand, the coins in the scholars' hands,
  the blue cloth pouch and the oilcloth packet at and in Tang Xiaotang's own hands.
- The paper moulds are written only by their shape, never "mould" (e914 s30/s32: the noun became a beam or a rake): MAT, a
  flat rectangular mat of thin split bamboo strips, carried flat like a tray.
- Tang Xiaotang never speaks on camera (bible rule 3): her fourteen lines are shot from close behind her (TBACK, nospeak, spec.json
  drops her three face pictures and her identity sentence: s03, s06, s16, s20, s24, s26, s29, s32, s33, s37, s42) or are
  inserts of her hand (s27, s38); s04 is her point of view (voice off screen). Every back shot says she is the only one in
  the frame with buns and pink ribbons and gives her one fixed screen side for the whole shot (e915 s26/s41: a second Tang
  appeared when her back was in the foreground). Her silent face (s01, s07, s11, s18, s34, s39) gets e907's neutral face
  sentences in spec.json. Costume: the live portrait l1, cross-collared and closed, no outer coat (bible rule 4).
- Lai San gives no face this episode (script): his back in s01 and s07 is unnamed (LAI_BACK, no picture);
  his two lines (s02, s08) are from behind him, nospeak, with his picture and identity sentence dropped in spec.json.
- No weapon in this episode (bible rule 5): Qin Shuang's belt is empty (extras.json drops the knife from her look); the two
  servants' staffs are plain wooden staffs, smooth and round to both ends; the punting poles are bamboo.
- No more than three named faces in a shot (bible rule 1); the scholars and servants are small and soft.
- Night is night: s18-s28 the raft under stars by its one paper lantern (no moon: script); s39 before dawn, the lantern
  burning low (the picture has it lit; see Places).
- Nobody is flipped in the edit: every speaker wears a cross collar; sides are written as screen left/right.
State at the junction (e015 r2.py s42, after its review): the stone bridge at dawn; Lai San behind the log barrier on screen
right facing left, holding the folded slip a hand's width in front of Xu Yan's chest; Xu Yan at the front of the wheelbarrow
on screen left, left hand on the oilcloth bundle; Tang Xiaotang beside the cart between them. s01 is the same moment from the
other side of the log: Lai San's back in the right foreground, Xu Yan facing us on screen left, Tang Xiaotang behind him.
Places (the coordinator's decisions, 2026-11-15, after the independent review review.md in this folder; listed again in
script.md 〈真人版的改動〉). FOUR PICTURES ARE REDRAWN in live-action/screen-test-e016.py (seeds 37013/37014, manifest
~/mokaair-work/videos/_series/zhong-tian-qu-qi/live-screen-test-e016/e016.json, 8 jobs, NOT run here); prep916.sh stops until
all four and the raft mirror are in refs-live (pilot.py takes the newest l-version of a set):
- the stone bridge set-shiqiao-l2 (e015's redraw: arch in the middle, stone path on the left; the log and its trestles are
  written in each shot as e015 did). Kept.
- the work shed by day set-gongpeng-l3 (NEW, an edit of l2): bare packed-earth floor, the far left only the bare stone wall
  (l2's two tall A-frames of poles gone), both vats with bare rims (l2's crossed stirring sticks gone); the text writes
  exactly that (review 必改 4). The script's third tub is written as one new small tub in front of the table.
- the raft at night set-zhufa-ye-l2 (NEW, a real-photo redraw of l1, same layout: bow at the lower left, the stern pole and
  lantern on the right, two oilcloth bundles stacked low). gen-dh SET gets "bamboo raft" -> dh-set-zhufa-ye-t1 before
  "bamboo grove" and "stream|...|reeds" (shared edit; e910-e915 rebuild byte for byte). s39 (upstream, the bow on screen
  right; review 必改 16) uses its mirror set-zhufa-ye-l2-flip.png (ffmpeg hflip after the pick; an empty set has no cross
  collar), swapped in by prep916.sh from spec.json "swap_pictures"; pilot.py now ignores such non-l<N> names when it picks
  the newest l-version (shared edit). s39 keeps the lantern burning low as the picture has it.
- the academy gate set-shuyuan-l2 (NEW, review 必改 8): normal lens, vermilion doors and steps on the right, one smooth blank
  plaque with straight grain, plain plaster walls and dark plank shop fronts with plain dark eaves, a stone courtyard and a
  tree through the doors. The shots from the gate side (s29, s32, s33, s34, s37; review 必改 14) have their own place
  sentence (academy_rev): the street and the carriage on the RIGHT. Inserts send no set picture (review 必改 5, the e915 s08
  lesson): s31 and s12 send only xuyan-angle-a-l1, s27 and s38 only tangxiaotang-portrait-l1, each named as the owner of the
  hands; s35 (inside the carriage) sends only Sun Zhanggui's portrait.
- the ferry landing set-dukou-l2 (NEW, review 必改 17-18): the l1 landing at dawn with one column of black smoke rising behind
  the village on the right and the jetty standing empty (l1's moored covered boat would be read as the raft). s41 and s42
  send it; s40 (a medium shot on the raft against the sky) sends none.
New face: Sun Zhanggui (sunzhanggui-portrait-l1, e907: thin long face, grey-streaked beard, green satin robe), voice Charon as
cast.json has it; he appears only in s35, inside the carriage.
"""
EP = 916  # internal working number; the published slug is zhong-tian-qu-qi-e016-r2
SLUG = "zhong-tian-qu-qi-e016-r2"
EP_TITLE = "書院門口賣白紙（重製版 r2）"
OUTLINE_SECONDS = 222  # script.md: 222 s, 42 shots (17 + 11 + 14)
TARGET_MINUTES = [3, 4]
TITLE = "書院門口賣白紙｜種田娶妻打天下 第16集（重製版）"
DESCRIPTION = "石橋頭，賴三要五十兩買紙坊換一條路；許硯把那張紙摺好塞回他手裡：不賣。橋是錢家的，橋下的柳溪可不是。三張竹簾抄了一整天，抄到三百二十張；當夜秦霜撐著竹筏順流而下，唐小棠在紙堆上打哈欠，許硯擔心行會一張都不收，她卻說：不賣書坊，直接賣給書生。第二天上午，縣學書院門口同一支筆、同一滴墨當場比，柳溪白紙寫字不洇墨，書生排到街角，三百張賣完。街角那輛黑篷馬車裡，魏記的孫掌櫃低聲吩咐「報給少爺」。逆水撐了一夜，天亮回到柳溪口，紙坊的方向冒起濃煙。《種田娶妻打天下》第 16 集（重製版）。"
THUMB = ("書院門口賣白紙", "s29")
CHARACTERS = ["xuyan", "tangxiaotang", "qinshuang", "shimujiang", "laisan", "sunzhanggui", "xitong"]
MINOR = {}  # every speaker has a cast.json voice; the servants, the scholars and the driver are silent
MUSIC = "one cue per scene: a light tense cue of muted plucks on a misty stone bridge at dawn turning into a bright quick rhythm of wooden percussion and strings in a busy paper workshop, one bright accent when three hundred and twenty sheets are counted; then a quiet night cue of a bamboo flute and soft water on a starlit river, a light accent and the rhythm lifting when a young woman sits up with an idea; then a bright busy market cue at an academy gate, one accent when the ink stays clean, sinking into low strings at a dark carriage, a low drone before dawn and one big heavy accent on a distant shout; ancient Chinese rural drama, no vocals"

# Scene headers. Scene 1 is the stone bridge at dawn (set-shiqiao-l2) and the work shed by day and at sunset (set-gongpeng-l2);
# scene 2 the bamboo raft at night (set-zhufa-ye-l1, new); scene 3 the county academy gate in the morning (set-shuyuan-l1), the
# raft again before dawn and the ferry landing at dawn (set-dukou-l1). Close shots use the short `_c` headers.
# No person's name in a place phrase. gen-dh SET takes the FIRST pattern in its list order that the whole prompt matches, so the
# raft prompts never say "ferry", "grove", "bridge" or "shed"; the ferry-landing prompts say "ferry landing" (before "bamboo
# raft" in SET); no prompt says "small ferry boat", "village entrance", "city gate", "dark pool" or "willow".
# Bible rule 18: every place is written as what is there.
BRIDGE = ("an old grey stone arch bridge over the misty water, a stone-paved path running from the left foreground to a small "
          "flat stone landing at the near foot of the bridge, green bamboo along both banks, open misty water with round stones "
          "and reeds along the bank at the right, tiled houses on the far bank")
BAR = ("one thick rough log laid across the small stone landing at the foot of the bridge as a barrier, each end resting on a "
       "low wooden trestle")
# review.md 必改 4 with the coordinator's redraw set-gongpeng-l3 (screen-test-e016.py): bare earth floor, the far left wall bare,
# the vats' rims bare (l2's A-frames of poles and crossed stirring sticks are gone from the picture, so nothing long is written).
SHED = ("a dark timber roof on rough wooden posts, open on the right side, a low back wall of fitted stone with green plants at "
        "its foot, two big round wooden vats at the left filled with smooth milky white bamboo pulp, their round rims bare, a "
        "squat stone mortar in the middle, an old plain wooden table at the right and in front of the table one new small round "
        "wooden tub of the same milky pulp; at the far left only the bare stone wall; the floor bare packed earth, smooth and "
        "even")
# set-zhufa-ye-l2 (the real-photo redraw of l1, same layout): bow at the lower left, the stern pole and lantern on the right.
RAFT = ("one long bamboo raft of eight thick green-yellow bamboo poles with natural nodes lashed side by side with rough hemp "
        "rope, two rounded bundles wrapped in worn brown oilcloth and tied with rope stacked low in its middle, one tall bamboo "
        "pole standing at its stern on the right with a short crossbar from which hangs one plain blank pale paper lantern with "
        "a small candle burning inside, its warm glow on the water")
# 必改 16 (s39): the mirrored picture set-zhufa-ye-l2-flip.png: the stern pole on screen left, the bow on screen right.
RAFT_UP = ("one long bamboo raft of eight thick green-yellow bamboo poles with natural nodes lashed side by side with rough hemp "
           "rope, its bow on screen right, only one rolled-up empty oilcloth lying in its middle, one tall bamboo pole standing "
           "at its stern on screen left with a short crossbar from which hangs one plain blank pale paper lantern burning low")
BANKS = "dark reeds and dark bamboo along both banks, black trees and low hills beyond them"
# 必改 8 with set-shuyuan-l2 (normal lens, plain plaster, one smooth blank plaque with straight grain, plain dark eaves).
ACADEMY = ("three wide stone steps at the right up to a pair of open vermilion doors under a dark tiled gate roof, one smooth "
           "blank wooden plaque of plain brown wood with fine straight grain above the doors; through the open doors only a "
           "stone-paved courtyard and one green tree; the stone-paved street running away to the left between long plain white "
           "plaster walls with dark tiled copings and dark wooden plank shop fronts, every eave plain dark wood")
TABLE = ("one long plain wooden table standing in front of the steps, two rounded bundles in dark brown oilcloth on its right end, "
         "one plain dark inkstone and one writing brush on its left end")
CARRIAGE = ("far down the street at the left, small, one closed carriage with a black canopy, a plain dark blue curtain and one "
            "brown horse, standing still")
# 必改 14: the shots from the gate side (behind Tang Xiaotang, or over the gate roof) look out the other way: the street and
# the carriage are on the RIGHT there.
ACADEMY_REV = ("seen from the gate steps looking out over one long plain wooden table: the stone-paved street running away to the "
               "right between long plain white plaster walls and dark wooden plank shop fronts, every eave plain dark wood; far "
               "down the street on the right, small, one closed carriage with a black canopy, a plain dark blue curtain and one "
               "brown horse, standing still; every scholar wears pale blue-green and a black cap, and nobody else wears pink")
# 必改 17, 18 with set-dukou-l2: the jetty empty, one column of black smoke behind the village (建議: the red glow low at the left).
DUKOU = ("wide calm water reflecting the sky, a few tall bare wooden mooring posts standing in the water, a low wooden jetty "
         "running out from the right bank, standing empty, its grey planks bare to its end, dry grass along the right bank, a "
         "dirt path up the bank to a cluster of low thatched and tiled village houses on the right, blue hills far off at the left")
SMOKE = ("from behind the village houses on the right one thick column of black smoke rising and rolling into the pale dawn sky "
         "above the village, the red glow low on the far left horizon")
LOC = {
    "bridge": f"At the near foot of the stone bridge into the county town in the early morning: {BRIDGE}; {BAR}; thin white mist lying on the water; low cold golden morning light from the right",
    "bridge_c": "At the foot of the stone bridge in the early morning, thin white mist on the water and low cold golden light from the right",
    "pm": f"In the open-sided work shed beside the Xu farmhouse on a clear autumn day: {SHED}; warm daylight slanting in from the open right side, leaf shadows on the walls",
    "pm_c": "In the open-sided work shed on a clear autumn day, warm daylight from the open right side",
    "eve": f"In the open-sided work shed beside the Xu farmhouse at sunset: {SHED}; low golden evening sunlight slanting straight in through the open right side, long warm shadows",
    "eve_c": "In the open-sided work shed at sunset, low golden evening sunlight from the open right side",
    "raft": f"On a bamboo raft drifting down a quiet river at night: {RAFT}; {BANKS}; deep dark night, only cold stars in the black sky, the black water lit only by starlight and the lantern's warm glow",
    "raft_c": "On a bamboo raft on a quiet river at night, deep dark night, cold starlight and the warm glow of one blank paper lantern",
    "predawn": f"On a bamboo raft moving slowly up a quiet river just before dawn: {RAFT_UP}; {BANKS}; the sky a deep cold blue just before dawn, the water dark",
    "academy": f"At the county academy gate in the county town on a clear autumn morning: {ACADEMY}; {TABLE}; {CARRIAGE}; bright clear morning sunlight, crisp shadows on the stone",
    "academy_c": "At the county academy gate on a clear autumn morning, bright clear sunlight",
    "academy_rev": f"At the county academy gate in the county town on a clear autumn morning, {ACADEMY_REV}; bright clear morning sunlight, crisp shadows on the stone",
    "carriage": "Inside a closed carriage at a street corner near the county academy gate on a clear autumn morning: dark wooden walls and a plain dark wooden bench, one small window with a plain indigo cloth curtain, bright daylight outside the window",
    "dawn": f"At the ferry landing below the village at dawn: {DUKOU}; {SMOKE}; cool dawn light",
    "dawn_c": f"At the ferry landing below the village at dawn; {SMOKE}",
}
LIGHT = {
    "bridge": "the thin mist on the water and the low cold golden light from the right stay unchanged",
    "pm": "the warm daylight from the open right side stays unchanged",
    "eve": "the low golden evening sunlight from the right stays unchanged",
    "raft": "the deep night, the cold starlight and the one warm lantern glow stay unchanged, the sky stays black",
    "predawn": "the deep cold blue before dawn stays unchanged",
    "academy": "the bright clear morning sunlight stays unchanged",
    "dawn": "the red dawn light and the column of smoke stay unchanged",
}
# bible rule 15: no "<X> speaks off screen" / "the system voice speaks off screen".
OFFSCREEN_SPEECH = False

# Repeated wording (each prop is one object).
XU2 = ("Xu Yan, in his faded blue-grey scholar's robe patched at one elbow, the sleeves tied back above his forearms with cloth "
       "strips")
XU_ROLL = "Xu Yan, in his faded blue-grey scholar's robe patched at one elbow, the sleeves rolled up to his elbows"
XU_COAT = "Xu Yan, in an old plain grey cloth outer coat over his faded blue-grey scholar's robe"
QIN = ("her dark brown cross-collared short jacket, wide plain leather belt with nothing tucked in it and nothing hanging from "
       "it, black trousers, leather boots and high ponytail tied with black cord")
CARP = ("Carpenter Shi, in his faded brown cross-collared short work jacket with the sleeves rolled up and his worn brown "
        "leather apron, one plain wooden stick through his grey topknot")
SUN = ("Sun Zhanggui, in his green satin cross-collared robe with a jade belt hook, his long narrow face and thin grey-streaked "
       "beard")
TANG = "in her peach-pink cross-collared short jacket wrapped shut over a pleated skirt with a ribbon bow"
GOLD = "the small gold abacus hanging at her right hip"
POUCH = "one small plain blue cloth money pouch tied at the front of her sash"
PURSE2 = POUCH + ", and the small gold abacus hanging at her right hip"
PACKET = "one small square packet wrapped in brown oilcloth and tied with string, the size of a book"
POLE = ("one long punting pole of plain green bamboo about twice a man's height and as thick as a wrist, smooth and round along "
        "its whole length, both ends cut flat")
SHORTPOLE = "one short pole of plain green bamboo as long as a man, smooth and round along its whole length"
POLE_ONLY = "the only long things in the frame are the bamboo poles of the raft and her one green bamboo punting pole"
# e914 fix1 s30/s32: the mould is written only by its shape and carried flat like a tray.
def mat(pr="his"):
    return ("a flat rectangular mat of thin split bamboo strips laid close side by side, as wide as " + pr + " shoulders and as "
            "deep as " + pr + " forearm is long, edged with a thin plain wooden border, pale straw-coloured all over, one small "
            "willow-leaf shape woven into its middle in the same pale strips")


MAT = mat()
SHEETS = "a neat stack of fresh plain white paper, every sheet blank, thick and matte, square"
BUNDLE = "one square bundle of paper wrapped in dark brown oilcloth and tied with rope"
CART = ("one wooden wheelbarrow with a single wooden wheel at the front and two long wooden handles, one square bundle wrapped "
        "in brown oilcloth and tied with rope on it")
SLIP = "one small slip of plain paper folded in half, only its blank back toward us, thick and opaque, lit from the front"
TESTSHEET = "one sheet of fresh plain white paper the size of a book page, thick and opaque, completely blank"
BRUSH = "one plain writing brush with a thin bamboo handle and a soft black tip"
YELLOW = "one blank sheet of thin yellowish bamboo paper"
WHITE = "one blank sheet of fresh plain white paper"
COINS = "a few round copper coins"
SERVANTS2 = ("two Qian household servants in plain grey Song-dynasty cross-collared short jackets and cloth head-wraps, small and "
             "soft, their faces shadowed under their head-wraps, each holding one end of the log in both hands")
SCHOLARS = ("young scholars in Song-dynasty pale blue-green cross-collared long robes and black square soft caps, cloth shoes, "
            "small and soft, their faces seen only from the side or from behind")
HANDS = "their hands hold only what is described here"
TBACK = ("one young woman seen only from behind, appearing only once: the back of her head with two looped buns tied with pink "
         "silk ribbons and pearl pins, two long pink silk ribbons hanging from the buns down over her shoulders, a pink inner "
         "collar at the nape of her neck and her light peach-pink silk shoulders; the back of her head toward us the whole time, "
         "her ear the furthest round her head we ever see, only hair, ribbons and shoulders, her face turned fully away")


def only_tang(side):
    """e915 s26/s41: a second Tang appeared beside her back. One person with buns and ribbons, one fixed side."""
    return (f"she is the only one in the frame with buns and pink ribbons, and she stays in the {side} foreground from the first "
            f"frame to the last")


LAI_BACK = ("one thin young man seen only from behind, appearing only once: only the back of his head with a small topknot above "
            "a wide grey-brown cloth band and his shoulders in a grey-brown hemp jacket, soft and dark, his face never in the frame")
CARP_BACK = ("one lean old man seen only from behind, appearing only once: only the back of his grey topknot with a plain wooden "
             "stick through it, his shoulder in a faded brown jacket and the strap of a worn leather apron, soft, his face never "
             "in the frame")
QIN_BACK = ("one young woman seen only from behind, appearing only once: only the back of her head with her high ponytail tied with "
            "black cord and her shoulder in a dark brown jacket, soft, her head turned fully away from us, her ear, cheek and "
            "profile never visible, her face never in the frame, her hands below the frame")
NOSMILE = "after the last word the lips press flat and the jaw sets, the brows stay drawn, held to the last frame"
SILENT_HE = "He says nothing in this shot: his lips stay pressed together from the first frame to the last, his jaw still, no talking, no mouthing words"
HEADSTILL = "she keeps her head still and never turns it, the back of her head toward us the whole shot"
HEADSTILL_HE = "he keeps his head still and never turns it, the back of his head toward us the whole shot"


def quiet(who, pr="his", plural=False):
    verb = "say" if plural else "says"
    return (f"{who} {verb} nothing in this shot: {pr} lips stay pressed together from the first frame to the last, no talking, "
            f"no mouthing words, the face set and still")


SHOTS = [
    # ---- scene 1a: the stone bridge at dawn. Axis as e015 s36-s42: the cart and the village path on screen left, the log
    # barrier in the middle, Lai San behind it on the right facing left. Lai San gives no face (script): unnamed backs (no
    # picture), and his own two lines (s02, s08) from behind him with nospeak.
    # s01 = e015 s42 from the other side of the log: his back in the right foreground, Xu Yan facing us.
    dict(chapter="不賣", loc="bridge", cam="Over-the-shoulder medium shot, slow push in", chars=["xuyan", "tangxiaotang"], night="bridge",
         comp=f"over-the-shoulder medium shot from close behind {LAI_BACK}, standing behind the thick rough log barrier in the right foreground, the log lying level across the lower frame between him and the others, at its left end one hand in a plain grey sleeve resting on it, only that sleeved hand showing at the frame's left edge; the thin young man's right arm reaching across the log, {SLIP} held out between his right thumb and fingers; facing us beyond the log on screen left, a little left of the middle, {XU2}, standing beside the front of {CART}, framed from the waist up with clear space above his head, his left hand resting on the oilcloth bundle on the cart, his right hand at his side, his face three-quarter to screen right toward the man, his eyes on him just right of the lens, never the lens; calm and cool: brows level, eyes steady, lips moving evenly between words; one step behind him on the right side of the cart Tang Xiaotang {TANG}, {GOLD}, framed from the waist up, soft, her face three-quarter to screen right toward the man, never the lens; composed: brows level, lips closed; behind them only the stone-paved path, the bamboo and the mist; {HANDS}; exactly two faces, the man in the foreground seen only from behind",
         lines=[("xuyan", "紙坊不賣，五十兩你留著買別的。", "平靜")],
         motion=f"the thin young man in the right foreground keeps his head still, the back of his head toward us the whole shot; Xu Yan lifts his right hand and closes the man's fingers over the folded slip with his own fingers, then pushes the man's closed hand back across the log toward the man's chest; the slip stays folded inside the man's fist, only a corner of its blank back showing; {quiet('Tang Xiaotang', 'her')}; after the last word Xu Yan's lips press flat and his brows stay level, eyes steady on the man",
         zh="過肩中景、慢推（第一格接第 15 集 s42 的同一刻，從橫木另一邊拍）：前景右只有賴三的後腦、額上寬布帶與肩（不點名、不送圖），站在橫木後，右手隔著橫木捏著那張摺紙伸出來；橫木左端搭著一隻灰袖的手（家丁，審稿建議）；許硯在畫左推車前頭旁，抬起右手把賴三的手指按攏在摺紙上，把那隻握起的拳頭推回橫木那邊、推向他胸口（審稿必改 1：一拍，紙始終在賴三手裡、只露一角空白紙背），平靜地說；唐小棠在許硯身後、推車右邊（虛焦，中性臉、嘴閉著）；不笑"),
    dict(loc="bridge", cam="Over-the-shoulder medium shot, slow push in", chars=["laisan", "xuyan"], nospeak=["laisan"], night="bridge",
         comp=f"over-the-shoulder medium shot from close behind {LAI_BACK}, behind the thick rough log barrier in the right foreground, his right fist still closed around the folded slip; facing us beyond the log on screen left a step away, {XU2}, framed from the waist up with clear space above his head, standing beside the cart near its front, his face three-quarter to screen right toward the man, never the lens; cool and unmoved: brows level, eyes steady, lips pressed shut; behind him only the stone-paved path and the mist; {HANDS}; exactly two people, the man in the foreground seen only from behind",
         lines=[("laisan", "不賣？那就讓你的紙，全爛在村裡。", "冷笑")],
         motion=f"the thin young man in the foreground keeps his head still, the back of his head toward us the whole shot, while he stuffs the slip into the front of his jacket with his right hand, drags his left foot one limping step back and slaps the log once with his left palm; Xu Yan steps back along the side of the cart to its two handles and takes them in both hands; {quiet('Xu Yan')}",
         zh="過肩中景、慢推：前景右只有賴三的後腦與肩（背對鏡頭說話，nospeak；spec 拿掉他的定妝照與身分句），第一格右拳還握著那張摺紙（接 s01），把紙往懷裡一塞，拖著左腳往後退一步，左手拍一下橫木；畫左許硯第一格在推車側邊靠前，沿著車邊退回車把、兩手握住（審稿建議），嘴閉著。台詞剪接放錄音"),
    # Converted: from behind her at the parapet (she is the only person in the frame).
    dict(loc="bridge", cam="Medium shot, slow push in", chars=["tangxiaotang"], nospeak=["tangxiaotang"], night="bridge",
         comp=f"medium shot from behind and a little above: {TBACK}, standing at the low grey stone parapet at the near foot of the bridge, a little right of the middle, both her hands resting on the top of the parapet, {GOLD}; beyond the parapet below her only the slow misty water, the round stones and the green bamboo of the far bank; {only_tang('middle')}; nobody else in the frame",
         lines=[("tangxiaotang", "橋是他錢家的，橋底下的柳溪可不是。", "不慌")],
         motion=f"the young woman leans a little forward over the parapet and looks down at the water, both hands staying flat on the stone; {HEADSTILL}",
         zh="【改背後拍】中景、從背後稍高處、慢推：唐小棠站在橋頭的矮石欄邊（畫面中偏右），兩手平放在石欄頂上，往前探一點看橋下的水；欄外只有起霧的流水、圓石與對岸竹子；畫面裡只有她一個雙丸子頭粉緞帶的人，頭始終不轉。台詞 nospeak，剪接放錄音"),
    # Her point of view: nobody on screen; her line off screen.
    dict(loc="bridge", cam="Point-of-view medium shot, slow push in", chars=[], night="bridge",
         comp="point-of-view shot looking down over the low grey stone parapet of the stone bridge in the near foreground at the slow shallow water below, about two body-lengths wide, flowing gently toward screen left, round stones under the clear water, green bamboo along the bank; nobody anywhere in the frame; only the parapet, the water, the stones and the bamboo",
         lines=[("tangxiaotang", "順著溪往下漂一夜，天亮就是縣城。", "篤定")],
         motion="the thin mist on the water drifts apart and one bamboo leaf floats slowly away on the current toward screen left",
         zh="主觀（唐小棠從石欄往下看）、慢推：前景是石欄，橋下淺淺的溪水約兩丈寬、慢慢往畫左流，水底圓石、岸邊竹子；水面的霧散開，一片竹葉順水往畫左漂走；沒有人（她的台詞畫外）"),
    # Over her shoulder (unnamed, no picture): Xu Yan beside her at the parapet.
    dict(loc="bridge", cam="Over-the-shoulder medium shot, slow push in", chars=["xuyan"], night="bridge",
         comp=f"over-the-shoulder medium shot from close behind {TBACK}, standing at the low stone parapet in the right foreground; {only_tang('right')}; a step to her left beyond her, a little left of the middle, {XU2}, framed from the waist up with clear space above his head, both hands on the top of the parapet, bending to look down over it at the water, his face three-quarter to screen right, never the lens; surprised and doubtful: brows lifting, eyes widening, lips moving between words; behind him only the bamboo and the mist; {HANDS}; exactly two people, the young woman in the foreground seen only from behind",
         lines=[("xuyan", "走水路？我們家連一條小船都沒有。", "意外，半信半疑")],
         motion=f"Xu Yan glances down over the parapet at the water, his eyes light up, then he straightens and turns his face to her; {HEADSTILL}; after the last word his brows stay lifted, lips pressed",
         zh="過肩中景、慢推：前景右只有唐小棠的後腦與肩（不點名、不送圖），站在石欄邊；許硯在她左邊一步、畫面中偏左，兩手扶石欄彎腰往下看一眼、眼睛一亮，直起身轉頭看她，半信半疑地說；她頭始終不轉；不笑"),
    # Converted: from behind her; she points back toward the village with her left arm (on screen left).
    dict(loc="bridge", cam="Over-the-shoulder medium shot, slow push in", chars=["tangxiaotang", "xuyan"], nospeak=["tangxiaotang"], night="bridge",
         comp=f"over-the-shoulder medium shot from close behind {TBACK}, standing at the low stone parapet in the right foreground, {GOLD}; {only_tang('right')}; facing us a step away, a little left of the middle, {XU2}, framed from the waist up with clear space above his head, his hands at his sides, his face three-quarter to screen right toward her, his eyes on her face just right of the lens, never the lens; listening: brows raised, eyes quick, lips pressed shut; behind him only the stone-paved path running back toward the village at the left and the bamboo; {HANDS}; exactly two people, the young woman in the foreground seen only from behind",
         lines=[("tangxiaotang", "石叔教過二牛紮竹筏，村後的竹子要多少有多少。", "有一點得意")],
         motion=f"the young woman lifts her left arm (on screen left) and points straight back along the path toward the village at the left; Xu Yan's eyes follow her arm to the left and come back to her, and he nods once slowly; {HEADSTILL}; {quiet('Xu Yan')}",
         zh="【改背後拍】過肩中景、慢推：前景右只有唐小棠的後腦與肩，左手（畫左）抬起往畫左回村的石板路一指；許硯在她正前方、畫面中偏左，眼睛跟著她的手往左看再回來，慢慢點一下頭、嘴閉著；頭始終不轉。台詞 nospeak，剪接放錄音（她說時可以得意，看不到）"),
    # From behind the log (Lai San's back at the right, unnamed): Xu Yan turns the cart and pushes it away up the path.
    dict(loc="bridge", cam="Wide shot, slow push in", chars=["xuyan", "tangxiaotang"], night="bridge",
         comp=f"wide shot from behind the log barrier, the rough log lying across the bottom of the frame, one hand in a plain grey sleeve resting on its left end, only that sleeved hand showing at the frame's left edge; in the right foreground {LAI_BACK}, standing behind the log; beyond the log on the stone-paved path, {XU2}, gripping the two handles of {CART}, turning it round toward the village, framed full length, his face three-quarter to screen right toward the man as he looks back over his right shoulder, never the lens; cool: brows level, eyes flat, lips moving evenly between words; walking beside the cart on its right side Tang Xiaotang {TANG}, {GOLD}, framed full length, small, her face three-quarter to screen right, never the lens; composed: brows level, lips closed; behind them only the path, the bamboo and the misty morning; {HANDS}",
         lines=[("xuyan", "三爺，這座橋你留著，自己慢慢走。", "回頭，不冷不熱")],
         motion=f"the thin young man in the right foreground keeps his head still, the back of his head toward us the whole shot; Xu Yan swings the wheelbarrow round and pushes it two steps away up the path, then turns his head back over his right shoulder toward the man and speaks; Tang Xiaotang walks on beside the cart; the hand on the log stays still; {quiet('Tang Xiaotang', 'her')}; {NOSMILE}",
         zh="全景、慢推（從橫木後面拍，剪在推車掉頭的一半）：前景下緣是橫木、左端搭著一隻灰袖的手（家丁，不入臉）；前景右賴三的背影（不點名；審稿必改 2：『頭不轉』那句點名是前景那個人、放在許硯動作前）；橫木那邊許硯兩手握車把把推車掉頭往村裡推兩步，回頭從右肩看過來，不冷不熱地說；唐小棠走在推車右邊（中性臉、嘴閉著）；不笑"),
    dict(loc="bridge_c", cam="Low-angle medium shot, slow push in", chars=["laisan"], nospeak=["laisan"], night="bridge",
         comp=f"low-angle medium shot from the height of the stone landing: {LAI_BACK}, framed from the knees up with clear space above his head, standing behind the thick rough log at the near foot of the bridge, the low wooden trestle under the log's end beside his left foot; far up the stone-paved path beyond him, small and blurred, the wheelbarrow being pushed away toward the village by two small figures; the mist and the bamboo; he is the only person near the camera",
         lines=[("laisan", "好，看你的紙，能漂到哪裡去！", "咬牙")],
         motion=f"the man lurches one limping step forward after them, dragging his left foot, stops, and kicks the low wooden trestle hard with his left foot so the log jolts; {HEADSTILL_HE}",
         zh="低角度中景（從石台高度拍）、慢推：賴三的背影（spec 拿掉他的定妝照與身分句），拖著左腳往前追一拐、停住，用跛的左腳狠狠踢一下橫木下的木架、橫木一震；遠處石板路上推車往村裡走（很小、虛焦）；頭始終不轉，背對鏡頭說話，台詞剪接放錄音"),
    # ---- scene 1b: the work shed, the same day (open on the right; two vats at the left, the new small tub in front of the
    # table at the right). Carpenter Shi at the far vat, Xu Yan at the near vat, Tang Xiaotang at the new tub.
    dict(chapter="三張簾", loc="pm", cam="Wide shot, slow push in", chars=["shimujiang", "xuyan"], night="pm",
         comp=f"wide shot past the round wooden rim of the near vat in the left foreground: at the far vat a little left of the middle {CARP}, framed full length with clear space above his head, holding {MAT} level in both hands over the pulp, his face lowered to it, never the lens; gruff and busy: brows knotted, lips moving curtly between words; coming in through the open right side {XU_ROLL}, framed full length, both hands on the two handles of {CART}, his face three-quarter to screen left toward the old man, never the lens; brisk, lips closed; {HANDS}",
         lines=[("shimujiang", "第三張簾子剛做好，要多少紙就抄多少。", "頭也不抬")],
         motion=f"Carpenter Shi dips the flat mat straight down into the milky pulp, lifts it out level with a thin even layer of pulp on it and gives it one small shake, his eyes on the mat the whole time; Xu Yan pushes the wheelbarrow in through the open right side and stops it beside the table; {quiet('Xu Yan')}; {NOSMILE}",
         zh="全景、慢推、前景是畫左近桶的木桶沿（工棚重畫 l3：最左牆邊光禿、桶沿光禿）：石木匠在後面那個紙漿桶前（畫面中偏左），兩手平端一張竹簾（只寫形狀：平的細竹絲席、木邊、正中編一片柳葉），往漿裡一壓、平平抬起、輕晃一下，頭也不抬地說；許硯（袖子捲到手肘）推著獨輪車從畫右開口進來，停在木桌邊、嘴閉著；不笑"),
    dict(loc="pm", cam="Over-the-shoulder medium shot, slow push in", chars=["xuyan"], night="pm",
         comp=f"over-the-shoulder medium shot from close behind {CARP_BACK}, in the right foreground; facing us a few steps away at the near vat on screen left, a little left of the middle, {XU_ROLL}, framed from the waist up with clear space above his head, holding {MAT} flat at waist height in both hands like a tray, just lifted out of the pulp, his two hands only on the bamboo mat, his face three-quarter to screen right toward the old man, never the lens; keen and quick: brows up, eyes bright, lips moving between words; behind him only the bare stone back wall; {HANDS}; exactly two people, the man in the foreground seen only from behind",
         lines=[("xuyan", "三張簾一起抄，天黑前能抄到三百張嗎？", "盤算，問")],
         motion="the old man in the right foreground keeps his head still, the back of his grey topknot toward us the whole shot; Xu Yan holds the mat level while the water drips off its underside, then lifts his eyes from it to the old man; after the last word his brows stay up, lips pressed, eyes on the old man",
         zh="過肩中景、慢推：前景右只有石木匠的後腦、插木筆的髮髻、肩與皮圍裙帶（不點名、不送圖；審稿必改 2：『頭不轉』點名是前景的老人、放在許硯動作前）；許硯在前面那個紙漿桶邊（畫面中偏左），兩手只拿著剛撈起的竹簾、平端在腰前像托盤、水從底下滴，抬眼問；說完眉毛還揚著、抿嘴"),
    # Carpenter Shi does not smile (e913/e914: written as what his face does; short).
    dict(loc="pm", cam="Medium shot, slow push in", chars=["shimujiang", "tangxiaotang"], night="pm",
         comp=f"medium shot: a little left of the middle {CARP}, framed from the knees up with clear space above his head, standing beside a low board with a small stack of wet blank sheets on it, {MAT} with a wet sheet on it held face down in both his hands over the stack, his face three-quarter to screen left toward Xu Yan off screen left, never the lens; gruff and curt: brows knotted low, one eye narrowed, the corners of his mouth pulled down, lips moving curtly between words and pressed flat between them; on screen right, a few steps behind him, at the new small tub in front of the old table, Tang Xiaotang {TANG}, {GOLD}, framed from the waist up, her sleeves pushed back, pressing {mat('her')} down into the pulp with both hands, her face lowered to the tub, never the lens; intent: brows drawn together in concentration, lips closed; {HANDS}",
         lines=[("shimujiang", "三百張？我手不停，你們兩個別拖累我就行。", "嘴硬，短促")],
         motion=f"Carpenter Shi turns the mat over and lays the wet sheet down flat on the stack, then peels the mat away; Tang Xiaotang pushes her mat down into the pulp the way he does; after the last word he snorts once through his nose and presses his lips into a hard flat line; {quiet('Tang Xiaotang', 'her')}",
         zh="中景、慢推：畫面中偏左石木匠在矮木板邊，兩手把竹簾翻過來、把濕紙扣到紙堆上再揭開簾子，眉頭壓低、嘴角往下，嘴硬地說，說完鼻子哼一聲、嘴抿成一條線（不笑）；畫右後面唐小棠在木桌前的新小盆邊（袖子推起），學他把竹簾壓進漿裡，低頭專心、嘴閉著（中性臉）"),
    dict(loc="pm_c", cam="Insert close-up, slow push in", chars=["xuyan"], night="pm", act=3,
         comp=f"insert close-up, the shot opens directly on {MAT} rising level out of the milky white pulp in a round wooden vat from its very first frame, held flat by Xu Yan's two hands at its two sides, his blue-grey sleeves rolled up to the elbows; only the hands, the forearms, the mat and the pulp are in the frame; warm daylight from the right",
         lines=[],
         motion="the two hands lift the mat level out of the pulp; milky water streams down through the fine gaps between the strips and drips back into the vat, and a thin even layer of white pulp settles smooth across the whole mat",
         zh="插鏡、慢推（第一格就是竹簾從紙漿裡平平抬起；審稿必改 5：spec 不送工棚圖，只送許硯四分之三側面圖當手的主人）：許硯一雙捲袖的手端著竹簾兩側平平抬起，水從簾縫往下流、滴回桶裡，一層薄薄的白漿均勻鋪平；只有手、前臂、竹簾與紙漿（無台詞）"),
    # Qin Shuang comes in with the punting pole on her shoulder (a pole of plain green bamboo, smooth to its flat-cut ends).
    dict(loc="pm", cam="Wide shot, tracking", chars=["qinshuang", "xuyan"], night="pm",
         comp=f"wide shot following her past one rough timber post in the foreground: coming in through the open right side Qin Shuang, {QIN}, framed full length with clear space above her head, {POLE} resting on her right shoulder, held by her right hand, her face three-quarter to screen left toward Xu Yan, never the lens; brisk and direct: brows level, eyes steady, lips moving crisply between words; at the near vat on screen left {XU_ROLL}, framed full length, {MAT} held flat in both hands over the pulp, turning his head toward her, never the lens; lips closed; Qin Shuang's green bamboo pole is the only thing anyone carries, and Xu Yan's two hands are only on the bamboo mat; {HANDS}; exactly two people",
         lines=[("qinshuang", "小棠說要走水路。竹篙我削好了，筏子二牛照石叔說的在紮。", "乾脆，交代")],
         motion=f"Qin Shuang lowers the bamboo pole from her shoulder and stands it upright against the timber post, then walks over and stops a step to his right, facing him; Xu Yan stops working and turns round toward her, the mat still flat in his hands; {quiet('Xu Yan')}",
         zh="全景、跟拍、前景是棚柱：秦霜（腰帶空著）右肩扛一根比人高一倍的青竹篙（兩頭平切、通身圓滑）從畫右開口進來，把竹篙立靠在棚柱邊，走到許硯身後停下，乾脆地交代；許硯在畫左前面那個桶邊，兩手端著竹簾，回頭看她、嘴閉著"),
    dict(loc="pm", cam="Over-the-shoulder medium shot, slow push in", chars=["xuyan"], night="pm",
         comp=f"over-the-shoulder medium shot from close behind {QIN_BACK}, in the right foreground; facing us a step away beside the near vat on screen left, a little left of the middle, {XU_ROLL}, framed from the waist up with clear space above his head, {MAT} in both hands, his face three-quarter to screen right toward her, never the lens; worried: brows knotted, eyes searching hers, lips moving between words; behind him only the stone back wall; {HANDS}; exactly two people, the young woman in the foreground seen only from behind",
         lines=[("xuyan", "柳溪夜裡有灘，妳一個人撐得了一整夜？", "皺眉，擔心")],
         motion=f"Xu Yan lays the mat down flat across the rim of the vat, wipes both wet hands on the front hem of his robe and frowns at her; the young woman in the foreground keeps her head still, the back of her head toward us the whole shot; {NOSMILE}",
         zh="過肩中景、慢推：前景右只有秦霜的後腦、高馬尾與肩（不點名、不送圖）；許硯在畫左前面那個桶邊，把竹簾平放在桶沿上，兩手在書生袍前襬上擦一擦，皺眉看她、擔心地問；不笑"),
    dict(loc="pm_c", cam="Close-up, low angle, slow push in", chars=["qinshuang"], night="pm",
         comp=f"low-angle close-up of Qin Shuang, {QIN}, framed from the chest up with space above her head, her right hand on {POLE} standing upright beside her, her face three-quarter to screen left toward Xu Yan off screen left, never the lens; sure and proud: brows level, chin lifted, eyes steady, lips moving firmly between words; behind her only one rough timber post and the bright open side of the shed",
         lines=[("qinshuang", "哪裡有灘、哪裡有石頭，我都記得，你坐穩就好。", "篤定")],
         motion=f"Qin Shuang grips the upright pole, lifts it a hand's width and thumps its flat end down once on the earth, then lifts her chin; {NOSMILE}",
         zh="低角度近景、慢推（身後只有棚柱與亮的開口）：秦霜右手握著立在身旁的青竹篙，提起一點往地上一頓，抬起下巴，篤定地說；不笑"),
    # Converted: from behind her, crouched by the paper stack; Xu Yan and Carpenter Shi beyond her at the vats.
    dict(loc="eve", cam="Medium shot, slow push in", chars=["tangxiaotang", "xuyan", "shimujiang"], nospeak=["tangxiaotang"], night="eve",
         comp=f"medium shot from behind and a little above: {TBACK}, crouching in the right foreground beside the old wooden table, {SHEETS} knee-high on a low board in front of her, both her hands flat on top of it, {GOLD}; {only_tang('right')}; beyond her across the shed at the two vats on screen left, soft, {XU_ROLL} and {CARP}, each lifting a flat bamboo mat out of the pulp and setting it upright against the vat's side, their faces three-quarter toward each other, never the lens, tired, lips closed; the low sunset light from the open right side falls across the top of the stack; {HANDS}",
         lines=[("tangxiaotang", "三百二十張，一張不少，還多一張給你試筆。", "擦汗，眼睛亮，累但開心")],
         motion=f"the young woman presses the last few sheets flat with both palms, taps the top of the stack twice with her right forefinger (on screen right) and straightens her back; the two men at the vats set their mats aside; {HEADSTILL}; {quiet('Xu Yan and Carpenter Shi', 'their', True)}",
         zh="【改背後拍】中景、從背後稍高處、慢推：前景右唐小棠蹲在木桌邊、膝高的白紙堆前，兩手壓平最後幾張，右手食指（畫右）點兩下紙堆、挺直背；後面畫左兩個桶邊許硯、石木匠把竹簾從漿裡拿起來立在桶邊（虛焦、嘴閉著）；斜陽從畫右開口照在紙堆上；頭始終不轉。台詞 nospeak，剪接放錄音（她說時可以笑，看不到）"),
    dict(loc="eve", cam="Medium shot, slow push in", chars=["xuyan", "shimujiang"], night="eve",
         comp=f"medium shot: on screen left {XU_ROLL}, framed from the knees up with clear space above his head, bending to lift {BUNDLE} from the floor in both hands, his face three-quarter to screen right toward the old man, never the lens; decided: brows level, eyes firm, lips moving between words; on screen right a step away {CARP}, bent over a second {BUNDLE} on the floor, pulling its rope tight with both hands, his face lowered to the knot, never the lens; gruff, lips pressed shut; low golden sunset light from the open right side; {HANDS}; exactly two people",
         lines=[("xuyan", "好。天一黑就上筏，天亮前進縣城。", "定下來")],
         motion=f"Carpenter Shi yanks the rope tight and ties it off; Xu Yan swings his bundle up onto his right shoulder, steadies it with his right hand and nods once; {quiet('Carpenter Shi')}; {NOSMILE}",
         zh="中景、慢推：畫左許硯彎腰兩手抱起一捆油布紙捆、扛上右肩、右手扶著，點一下頭，定下來地說；畫右石木匠彎腰拉緊第二捆的麻繩打結、低頭、嘴閉著；斜陽從畫右開口照進來；不笑"),
    # ---- scene 2: the raft at night, downstream toward screen left (the bow and Qin Shuang on screen left; Tang Xiaotang on the
    # bundles in the middle; Xu Yan at the stern by the lantern on screen right), as the picture lies.
    dict(chapter="夜裡的柳溪", loc="raft", cam="Low-angle wide shot, tracking", chars=["qinshuang", "tangxiaotang", "xuyan"], night="raft", act=3,
         comp=f"low-angle wide shot skimming the water past drooping dark leaves in the foreground, keeping the whole raft in the frame: at the bow on screen left Qin Shuang, {QIN}, standing, framed full length, {POLE} in both her hands, her face three-quarter to screen left down the river, never the lens; intent: brows level, lips closed; sitting on the oilcloth bundles in the middle Tang Xiaotang {TANG}, framed full length, small, her face three-quarter to screen left, never the lens; sleepy, lips closed; at the stern on screen right beside the lantern pole {XU_COAT}, sitting, framed full length, small, his face three-quarter to screen left, never the lens; quiet, lips closed; {POLE_ONLY}; exactly three people",
         lines=[],
         motion=f"Qin Shuang plants the pole in the river bed and pushes back along it; the raft glides off toward screen left and rings of ripples spread out behind it in the lantern light; {quiet('Qin Shuang, Tang Xiaotang and Xu Yan', 'their', True)}",
         zh="低角度全景（貼著水面）、跟拍、前景是岸邊垂下的黑葉：筏頭（畫左）秦霜兩手握青竹篙插進水裡往後一撐，竹筏往畫左滑出去，燈籠光裡水波一圈圈散開；唐小棠坐在中間的油布紙捆上（小、中性臉），許硯（外披舊灰外衣）坐在筏尾燈籠竿旁（畫右）；三人嘴都閉著（無台詞）"),
    dict(loc="raft_c", cam="Medium shot, slow push in", chars=["qinshuang"], night="raft",
         comp=f"medium shot of Qin Shuang, {QIN}, standing at the bow of the raft, framed from the knees up with clear space above her head, {POLE} in both her hands, the warm lantern light from behind her on the right rimming her cheek and ponytail, her ponytail lifting in the night wind, her face three-quarter to screen left toward the dark water ahead, never the lens; alert: brows drawn, eyes narrowed ahead, lips moving crisply between words; ahead of her at the left edge one big dark rock in the water with white water foaming round it; behind her only the black river and the stars; {POLE_ONLY}",
         lines=[("qinshuang", "坐穩，前面有灘，石頭在左邊。", "頭也不回")],
         motion=f"Qin Shuang swings the pole across to her left side, plants it against the river bed and shoves, and the raft slides past the big rock; {NOSMILE}",
         zh="中景、慢推：秦霜站在筏頭，燈籠光從她右後方勾出臉頰與馬尾，馬尾被夜風吹起；前面畫左緣一塊大黑石、水翻白；她把竹篙換到左邊一撐，竹筏擦過大石頭，頭也不回地說（spec：視線在前面的水上）；不笑"),
    # Converted: from behind her, sitting on the bundles (the yawn is in the recording only).
    dict(loc="raft", cam="Medium shot, slow push in", chars=["tangxiaotang"], nospeak=["tangxiaotang"], night="raft",
         comp=f"medium shot from behind and a little to her right, looking across the raft toward the dark left bank: {TBACK}, sitting on the oilcloth bundles in the middle of the raft, a little right of the middle, her knees drawn up, {GOLD}; {only_tang('middle')}; the bow beyond the left edge of the picture; beyond her only the dark water, the black reeds of the left bank and the stars; the lantern glow from behind the camera warm on her shoulders and ribbons; nobody else in the frame",
         lines=[("tangxiaotang", "天亮前到得了縣城嗎？我眼皮都快黏起來了。", "打哈欠")],
         motion=f"the raft rocks once; the young woman puts her left hand (on screen left) down flat on the oilcloth beside her to steady herself, then lifts her right sleeve up in front of her face as her shoulders rise and sag in a long yawn; {HEADSTILL}",
         zh="【改背後拍】中景、從她右後方往左岸拍（審稿建議：筏頭出畫，秦霜不該消失在她前面）、慢推：唐小棠抱膝坐在筏中間的油布紙捆上（畫面中偏右），竹筏一晃，她左手（畫左）撐住紙捆，右手袖子抬到臉前、肩膀一聳一垮打個大哈欠（只在錄音裡）；前面只有黑水、左岸黑蘆葦與星空；頭始終不轉。台詞 nospeak，剪接放錄音（錄音 6.23 秒，句尾約 0.2 秒延到 s21 開頭）"),
    # Over her shoulder (unnamed, no picture) toward the bow.
    dict(loc="raft", cam="Over-the-shoulder medium shot, slow push in", chars=["qinshuang"], night="raft",
         comp=f"over-the-shoulder medium shot from close behind {TBACK}, sitting on the oilcloth bundles in the right foreground; {only_tang('right')}; beyond her at the bow on screen left, a little left of the middle, Qin Shuang, {QIN}, standing, framed from the knees up with clear space above her head, {POLE} in both her hands, her face three-quarter to screen right over her shoulder toward the young woman, never the lens; steady: brows level, eyes calm, lips moving evenly between words; behind her only the black river and a sky full of stars; {POLE_ONLY}; exactly two people, the young woman in the foreground seen only from behind",
         lines=[("qinshuang", "雞叫頭遍的時候，就到縣城外的碼頭了。", "穩")],
         motion=f"the young woman with the two buns and pink ribbons in the right foreground keeps her head still, the back of her head toward us the whole shot; Qin Shuang glances up once at the stars, then plants the pole and pushes the raft on with one long stroke; {NOSMILE}",
         zh="過肩中景、慢推：前景右只有唐小棠的後腦與肩（不點名、不送圖）坐在紙捆上；筏頭（畫面中偏左）秦霜抬頭看一眼星空，再一篙撐下去，從肩上回頭對她穩穩地說；頭始終不轉；不笑"),
    dict(loc="raft_c", cam="Close-up, slow push in", chars=["xuyan"], night="raft",
         comp=f"close-up of {XU_COAT}, sitting at the stern of the raft, framed from the chest up with space above his head, the paper lantern just behind him on the right lighting half his face warm and leaving the other half in cold starlight, his left hand on the oilcloth of a bundle beside him, his face three-quarter to screen left toward the middle of the raft, never the lens; worried: brows knotted, eyes lowered, lips moving low between words; behind him only the black water and the lantern glow",
         lines=[("xuyan", "到了也沒用，行會的告示一貼，書坊一張都不收。", "皺眉，發愁")],
         motion=f"Xu Yan presses his palm once on the oilcloth of the bundle beside him and lets out a long breath; {NOSMILE}",
         zh="近景、慢推（身後只有黑水與燈籠光）：許硯坐在筏尾，燈籠在他右後方照亮半邊臉，左手按一下身邊紙捆的油布，嘆一口氣，皺眉發愁地說；不笑"),
    # The system and a thought: he says nothing (bible rule 15); no blue light (bible rule 11).
    dict(loc="raft_c", cam="Close-up, slow push in", chars=["xuyan"], night="raft",
         comp=f"close-up of {XU_COAT}, sitting at the stern of the raft, framed from the chest up with space above his head, the lantern behind him on the right lighting half his face, his face three-quarter to screen left, never the lens; stung and stubborn: brows pulled together, eyes narrowing, lips pressed flat; behind him only the black water and the lantern glow",
         lines=[("xitong", "宿主還沒到就先認輸，效率真高。", "冷，毒舌"), ("xuyan", "我在想辦法，不是認輸……雖然還沒想到。", "嘴硬，心裡回嘴", "inner")],
         motion=f"Xu Yan rubs the bridge of his nose between two fingers with his right hand, then drops the hand and lifts his eyes to look ahead down the river, his jaw set; {SILENT_HE}; he is thinking, not speaking",
         zh="近景、慢推（身後只有黑水與燈籠光）：許硯右手兩指揉一下眉心，放下手、抬眼往前看，咬著下巴；全程嘴閉著（系統吐槽與心裡話畫外，吐槽不出面板）。不寫藍光"),
    # Converted: over her shoulder from behind, she in the LEFT foreground facing the stern; Xu Yan facing us at the stern.
    dict(loc="raft", cam="Over-the-shoulder medium shot, slow push in", chars=["tangxiaotang", "xuyan"], nospeak=["tangxiaotang"], night="raft",
         comp=f"over-the-shoulder medium shot from close behind {TBACK}, sitting on the oilcloth bundles in the left foreground, {GOLD}; {only_tang('left')}; facing us a step away at the stern, a little right of the middle, {XU_COAT}, sitting, framed from the waist up with clear space above his head, the paper lantern on its pole just behind him on the right, his face three-quarter to screen left toward her, his eyes on her face just left of the lens, never the lens; gloomy at first: brows knotted, lips pressed shut; behind him only the black water and the stars; {HANDS}; exactly two people, the young woman in the foreground seen only from behind",
         lines=[("tangxiaotang", "誰說要賣書坊？我們直接賣給書生。", "眼睛一亮")],
         motion=f"the young woman sits up straight all at once and slaps the oilcloth of the bundle beside her once with her right palm (on screen right); Xu Yan's eyes lift to her face and his brows rise; {HEADSTILL}; {quiet('Xu Yan')}",
         zh="【改背後拍】過肩中景、慢推：前景左唐小棠坐在紙捆上的背影，一下坐直、右手（畫右）拍一下身邊紙捆的油布；許硯坐在筏尾（畫面中偏右、燈籠在他右後方），抬眼看她、眉毛一揚、嘴閉著；頭始終不轉。台詞 nospeak，剪接放錄音（她可以笑，看不到）"),
    dict(loc="raft_c", cam="Close-up, slow push in", chars=["xuyan"], night="raft",
         comp=f"close-up of {XU_COAT}, sitting at the stern of the raft, framed from the chest up with space above his head, the paper lantern just behind him on the right lighting half his face warm and leaving the other half in cold starlight, his face three-quarter to screen left toward the middle of the raft, never the lens; doubtful: one brow up, eyes narrowed, lips moving between words; behind him only the black water and the lantern glow",
         lines=[("xuyan", "一家一家去敲書生的門？三百張要賣到哪天？", "不信，反問")],
         motion="Xu Yan sits up and leans forward toward the bundles, his forearms coming to rest on his knees; after the last word his brow stays up and his lips press flat",
         zh="近景、慢推（審稿建議：s24–s26 同一個過肩機位，本鏡改許硯乾淨近景，身後只有黑水與燈籠光）：許硯坐在筏尾，燈籠在右後方照亮半邊臉，坐直、往紙捆那邊前傾、前臂靠在膝上，挑眉不信地反問；說完眉毛還挑著、抿嘴"),
    # Converted: from behind her, tighter; she wags one finger.
    dict(loc="raft", cam="Over-the-shoulder medium close-up, slow push in", chars=["tangxiaotang", "xuyan"], nospeak=["tangxiaotang"], night="raft",
         comp=f"over-the-shoulder medium close-up from close behind {TBACK}, in the left foreground, her right hand raised at the height of her shoulder (on screen right) with one forefinger pointing up; {only_tang('left')}; facing us an arm's length away, a little right of the middle, {XU_COAT}, framed from the chest up with space above his head, the lantern glow on his face from the right, his face three-quarter to screen left toward her, his eyes on her finger and then on her face, never the lens; curious: brows raised, lips pressed shut; behind him only the black water; {HANDS}; exactly two people, the young woman in the foreground seen only from behind",
         lines=[("tangxiaotang", "不用敲門。縣學書院門口，一早就有幾百個書生進出。", "胸有成竹")],
         motion=f"the young woman wags her raised forefinger from side to side twice; Xu Yan's eyes follow the finger and then come back to her; {HEADSTILL}; {quiet('Xu Yan')}",
         zh="【改背後拍】過肩中近景、慢推：前景左唐小棠的後腦與肩，右手（畫右）舉到肩高、豎一根食指左右搖兩下；許硯（畫面中偏右）眼睛跟著手指再回到她臉上、嘴閉著；頭始終不轉。台詞 nospeak，剪接放錄音"),
    # Converted: an insert of her hand holding the spare test sheet beside the lantern (lit from the side, never from behind).
    dict(loc="raft_c", cam="Insert close-up, slow push in", chars=["tangxiaotang"], nospeak=["tangxiaotang"], night="raft",
         comp=f"insert close-up, the shot opens directly on one slender hand in a peach-pink silk sleeve holding up {TESTSHEET} from its very first frame, the sheet held just to the left of one plain blank pale paper lantern hanging from a bamboo crossbar, a small candle burning inside it, the sheet lit warmly from the side by the lantern, thick and opaque, its plain matte face clean and even; only the hand, the sleeve, the sheet and the lantern are in the frame; black night behind",
         lines=[("tangxiaotang", "拿他們自己的筆墨當場比，寫了不洇，自然就排隊。", "篤定，舉著紙")],
         motion="the hand lifts the sheet a little higher beside the lantern and turns it slowly so the warm light slides across its plain blank face",
         zh="【改插鏡】插鏡、慢推（第一格就是她的手舉著那張試筆白紙；審稿必改 5：spec 不送竹筏圖，只送唐小棠的定妝照當手與袖的主人，燈籠寫在文字裡）：一隻桃粉袖口的手把空白白紙舉在燈籠左邊，燈籠光從側面照（不從紙後透光）、紙厚不透、空白；手把紙再舉高一點、慢慢轉一下；臉不入鏡，台詞剪接放錄音"),
    dict(loc="raft", cam="Medium shot, slow push in", chars=["xuyan"], night="raft",
         comp=f"medium shot: {XU_COAT}, sitting at the stern of the raft, framed from the waist up with clear space above his head, the paper lantern on its pole just behind him on the right; held into the frame low at the left edge, below the lantern's height, by one slender hand in a peach-pink silk sleeve, {TESTSHEET}, its blank back toward us lit softly from the side by the lantern glow on his right, plain matte white, the lantern light falling on its edge; his right hand reaching out to take it, his face three-quarter to screen left toward the hand, never the lens; decided: brows level, eyes bright and firm, lips moving between words; behind him only the black water and the stars; {HANDS}",
         lines=[("xuyan", "好，就在書院門口，當場比給他們看。", "定下來")],
         motion=f"Xu Yan takes the sheet low with his right hand, folds it in half and in half again at once and tucks it into the front of his robe under the grey coat, then nods once; {NOSMILE}",
         zh="中景、慢推：許硯坐在筏尾（燈籠在右後方），畫左緣低處一隻桃粉袖口的手把試筆白紙遞進來（低於燈籠，紙背朝鏡頭、燈籠光從側面照到紙邊、空白不透；審稿必改 6：不從紙後透光）；他右手低低接過、立刻對摺兩次收進外衣裡的袍子前襟，點一下頭，定下來地說；不笑"),
    # ---- scene 3a: the county academy gate in the morning. From the street side (s30, s31, s36): the gate and steps on the
    # right, the table in front of them, the street and the carriage on the LEFT. From the gate side behind the table (s29, s32,
    # s33, s34, s37; review 必改 14, loc academy_rev): the street and the carriage on the RIGHT, Tang Xiaotang's back on the LEFT.
    # Converted: from behind the table; she stands on a low stool with two sheets raised, the scholars beyond her.
    dict(chapter="書院門口", loc="academy_rev", cam="Wide shot, slow push in", chars=["tangxiaotang"], nospeak=["tangxiaotang"], night="academy",
         comp=f"wide shot from behind the long table: {TBACK}, standing on a low wooden stool behind the table in the left foreground, both her arms raised high with one sheet of fresh plain white paper in each hand, {GOLD}; the morning sun is behind the camera on the left, lighting the backs of both sheets toward us flat and even, both sheets thick and opaque, plain matte white; {only_tang('left')}; beyond her across the table about eight {SCHOLARS}, walking up the street from the right toward the table and the camera and turning their heads toward her; the white walls and the dark shop fronts of the street behind them",
         lines=[("tangxiaotang", "各位公子，柳溪白紙，同一支筆，當場比給您看！", "揚聲，招呼")],
         motion=f"the young woman lifts both sheets higher and gives them one flourish in the air; the scholars slow down, stop and drift toward the table; {HEADSTILL}",
         zh="【改背後拍】全景、從桌後（門這邊）往街上拍、慢推（審稿必改 14：門這邊的反打，街與馬車在畫右）：前景左唐小棠站在矮凳上的背影，兩手高舉各一張空白白紙往上一揚；太陽在鏡頭後方左邊、平平照在朝鏡頭的紙背上、紙厚不透（審稿必改 7）；街上約八個書生（宋式淡青交領長衫、黑方巾，小、只見側臉或背影）從畫右沿街走來、轉頭看她、慢下來往桌子靠；頭始終不轉。台詞 nospeak，剪接放錄音（稿子的許硯、秦霜這鏡不入鏡）"),
    dict(loc="academy", cam="Medium shot, slow push in", chars=["xuyan"], night="academy",
         comp=f"medium shot of Xu Yan behind the long table: {XU_COAT}, framed from the waist up with clear space above his head, on the table in front of him {YELLOW} on the left and {WHITE} on the right lying side by side, {BRUSH} in his right hand above the inkstone, his left hand flat beside the sheets, his face three-quarter to screen left toward the scholars, never the lens; brisk and sure: brows level, eyes quick, lips moving between words; at the left edge of the frame, across the table, two young scholars in pale blue-green cross-collared robes and black square caps standing side-on in profile facing screen right, small and soft, round young faces different from his, their caps covering their hair; Xu Yan appears only once, behind the table; behind him only the vermilion doors and the white wall in the sun; {HANDS}",
         lines=[("xuyan", "左邊是書坊的紙，右邊是我們的，同一滴墨。", "清楚，當眾")],
         motion=f"Xu Yan smooths the two sheets flat side by side with his left palm, dips the brush into the inkstone and lifts it, the black tip wet; the two scholars lean in; {NOSMILE}",
         zh="中景、慢推（審稿必改 9：前景不放書生背影，改成畫左緣兩個側面的書生、圓臉、黑方巾蓋住頭髮，寫明許硯只出現一次）：許硯在長桌後，左手把左邊的黃竹紙、右邊的柳溪白紙並排抹平，右手毛筆在硯台裡蘸墨提起，當眾清楚地說；不笑"),
    # The brush insert: no set picture (the e915 s08 lesson); his side picture as the owner of the hand (spec.json).
    dict(loc="academy_c", cam="Insert close-up, top-down, locked", chars=["xuyan"], night="academy", act=3,
         comp=f"insert close-up looking straight down, seen from the street side of the table, the shot opens directly on two sheets lying side by side on the plain wooden table from its very first frame, {YELLOW} on screen left and {WHITE} on screen right; Xu Yan's right hand in a grey sleeve reaching in from the top edge of the frame, holding {BRUSH}, its wet black tip just above the yellowish sheet; only the hand, the sleeve, the brush, the two sheets and the wood are in the frame",
         lines=[],
         motion="the brush draws one single straight horizontal line across the middle of the yellowish sheet, then one across the white sheet; on the yellowish sheet the black ink slowly creeps outward into a fuzzy blurred edge, on the white sheet the line stays crisp and clean; only that one line is on each sheet, the rest of both sheets plain and blank",
         zh="插鏡、俯拍、鏡頭固定（第一格就是桌上並排的兩張紙；spec 不送書院圖，送許硯四分之三側面圖當手的主人）：許硯右手（灰袖）的毛筆在左邊黃竹紙上畫一橫、再在右邊白紙上畫一橫；黃紙上的墨慢慢往外暈成毛邊，白紙那一橫乾乾淨淨；每張只有那一橫、其餘空白（無台詞）"),
    # Converted: from behind her across the table; the scholars crowd in.
    dict(loc="academy_rev", cam="Over-the-shoulder medium close-up, slow push in", chars=["tangxiaotang"], nospeak=["tangxiaotang"], night="academy",
         comp=f"over-the-shoulder medium close-up from close behind {TBACK}, standing behind the long table in the left foreground, {GOLD}, her right hand (on screen right) holding {WHITE} up at shoulder height, the sun from the left grazing its edge, thick and opaque, plain matte white; {only_tang('left')}; across the table in front of her, soft, the heads of five or six {SCHOLARS}, bending over the table shoulder to shoulder and craning to look; the table edge and the inkstone soft in the lower frame",
         lines=[("tangxiaotang", "不洇墨，寫小楷也不毛邊，一張只要五文。", "輕快")],
         motion=f"the young woman holds the sheet a little higher and turns it once; the scholars push closer and crane their necks to look; {HEADSTILL}; the scholars say nothing, their lips closed",
         zh="【改背後拍】過肩中近景、慢推（審稿建議：推近一級，跟 s33 分開；必改 14 門這邊反打）：前景左唐小棠的背影，右手（畫右）把那張白紙舉到肩高，太陽從左邊擦過紙邊、紙厚不透（審稿必改 7：不寫舉進陽光）；桌前五六個書生的頭（虛焦）擠在一起伸頭看；頭始終不轉。台詞 nospeak，剪接放錄音"),
    # Converted: from behind her right shoulder, a little high; one hand takes the coins, the other stays on the paper.
    dict(loc="academy_rev", cam="Medium-wide shot, slight high angle, slow push in", chars=["tangxiaotang"], nospeak=["tangxiaotang"], night="academy",
         comp=f"slightly high medium-wide shot from behind her right shoulder: {TBACK}, standing behind the long table in the left foreground, {PURSE2}, her left hand (on screen left) flat on {SHEETS} on the table; {only_tang('left')}; across the table the whole queue of about fifteen {SCHOLARS}, running away from the table down the street on the right, the nearest one holding out {COINS} on his open palm",
         lines=[("tangxiaotang", "排好隊，一人限十張，賣完就沒有了！", "笑開，招呼")],
         motion=f"the young woman's right hand (on screen right) takes the coins from the nearest scholar's open palm and drops them into the blue pouch at the front of her sash, then the same right hand slides one small stack of paper across the table to him, while her left hand stays flat on the stack of blank paper the whole shot; the next scholar steps up; {HEADSTILL}; the scholars say nothing, their lips closed",
         zh="【改背後拍】稍高的中全景、從她右肩後拍、慢推（審稿建議：換景別、不跟拍；必改 14 隊伍往畫右的街上排）：前景左唐小棠的背影，左手（畫左）整鏡按在桌上的空白紙堆上；右手（畫右）從最前面那個書生攤開的手掌收下銅錢、丟進腰帶正前方的藍布錢袋，再用同一隻右手把一小疊紙推過桌面給他（審稿必改 10）；小金算盤掛在右胯（必改 11）；頭始終不轉。台詞 nospeak，剪接放錄音（她可以笑，看不到）"),
    # The system; three faces small in a high wide shot (her silent face: neutral sentences in spec.json).
    dict(loc="academy_rev", cam="Wide high-angle shot, slow push in", chars=["qinshuang", "xuyan", "tangxiaotang"], night="academy",
         comp=f"wide high-angle shot past the dark tiled corner of the gate roof in the top foreground: a long queue of about thirty {SCHOLARS}, winding from the long table along the street and round the corner at the right; behind the table, small: at its right end Qin Shuang, {QIN}, one big sheet of empty brown oilcloth in her hands; beside her {XU_COAT}, already holding the last small stack of blank paper out across the table to the scholar in front of him; at the left end Tang Xiaotang {TANG}, {PURSE2}, her left hand resting on {PACKET} on the table, her face three-quarter to screen right toward the queue, never the lens; busy: brows lifted, lips closed; every face small; Xu Yan appears only once, behind the table in his grey outer coat; the scholars are other young men with round faces and black square caps; {HANDS}",
         lines=[("xitong", "叮。白紙進城，售出三百張。", "冷，宣布")],
         panel=[("白紙進城，售出三百張", "panel")],
         motion=f"Xu Yan hands the last stack across the table to the scholar; Qin Shuang rolls up the empty oilcloth and tucks it under her left arm; Tang Xiaotang keeps her left hand resting on the oilcloth packet the whole shot; {quiet('Qin Shuang, Xu Yan and Tang Xiaotang', 'their', True)}",
         zh="全景、高角度略俯、慢推、前景是門樓瓦頂一角（門這邊，隊伍往畫右的街角拐；審稿必改 14）：約三十個書生排隊；桌後（人小）：右端秦霜手上一大塊空油布，許硯第一格已拿著最後一疊空白紙伸過桌面交給書生；左端唐小棠（腰帶正前方藍布錢袋、右胯小金算盤，左手按著桌上的油布小包＝留下的二十張，中性臉）；兩拍：許硯交出最後一疊、秦霜捲起油布夾在左腋下（審稿必改 12）；寫明許硯只出現一次、書生是別的圓臉年輕人（審稿建議）；三人嘴閉著（系統畫外，面板疊上）"),
    # Sun Zhanggui inside the carriage (spec drop_set: the academy picture is not inside a carriage). He may smile thinly.
    dict(loc="carriage", cam="Medium shot, slow push in", chars=["sunzhanggui"], night="academy",
         comp=f"medium shot past the dark wooden frame of the small carriage window in the foreground: inside the carriage {SUN}, seated on the bench, framed from the waist up with clear space above his head, his right hand holding up one corner of the plain indigo curtain, his narrow half-closed eyes on the street outside through the gap; cool and shrewd: eyes narrowed, a thin closed-lip smile; behind him only the dark wooden wall of the carriage; he is alone in the carriage",
         lines=[("sunzhanggui", "肥皂不賣，紙也不賣……回去報給少爺。", "低聲，慢條斯理")],
         motion="from the first frame he is already speaking low toward the front of the carriage on screen left, his eyes still on the street through the gap; on his last word his right hand lets the indigo curtain fall half shut",
         zh="中景、慢推、前景是馬車小窗的木框：孫掌櫃（瘦長臉、花白鬍、綠緞交領袍、玉帶鉤）坐在車裡，右手掀著深藍布簾一角；第一格就已經朝畫左車前（車夫，畫外）低聲說，眼睛還從縫裡看街；說到最後一個字右手一放、簾子落下一半（審稿必改 13：話與動作疊在一起，留 6 秒）；可以薄薄一笑；spec 不送書院圖"),
    # Her shoulder at the right edge: unnamed, no picture.
    dict(loc="academy", cam="Medium shot, slow push in", chars=["xuyan"], night="academy",
         comp=f"medium shot: behind the long table, a little left of the middle, {XU_COAT}, framed from the waist up with clear space above his head, {BRUSH} in his right hand over the inkstone, his face three-quarter to screen left toward the street, never the lens; wary: brows drawing together, eyes narrowing, lips moving low between words; at the right edge of the frame, soft, only the peach-pink silk shoulder and one hanging pink ribbon of the young woman beside him, her face out of the frame; far down the street at the left, small and soft, the closed black-canopied carriage; {HANDS}",
         lines=[("xuyan", "街角那輛黑篷車停了快一個時辰，是誰的？", "壓低聲音")],
         motion=f"Xu Yan's hand stops with the brush above the inkstone; he frowns, nudges the young woman beside him once with his right elbow and tips his chin toward the carriage down the street at the left; {NOSMILE}",
         zh="中景、慢推：許硯在長桌後（畫面中偏左），收拾毛筆的手停住，皺眉，用右手肘碰一下身邊的人（畫右緣只露她的桃粉衣肩與一條粉緞帶，不點名、不送圖），下巴往畫左遠處那輛黑篷車一點，壓低聲音說；不笑"),
    # Converted: from behind her, looking down the street at the carriage; her fingers stop on the abacus.
    dict(loc="academy_rev", cam="Over-the-shoulder medium shot, slow push in", chars=["tangxiaotang"], nospeak=["tangxiaotang"], night="academy",
         comp=f"over-the-shoulder medium shot from close behind {TBACK}, standing behind the long table in the left foreground, {PURSE2}, her right hand (on screen right) on the small gold abacus at her right hip; {only_tang('left')}; beyond her far down the sunlit street on the right, small, the closed carriage with its black canopy and brown horse; the scholars soft along the street; the white walls in the sun",
         lines=[("tangxiaotang", "魏記商行的孫掌櫃，我在江南見過他。", "很小聲，發白")],
         motion=f"from the first frame her right forefinger flicks the beads of the small gold abacus at her right hip, two quick flicks; then the finger stops dead on a bead and her shoulders go stiff and still to the last frame, looking down the street at the carriage; {HEADSTILL}",
         zh="【改背後拍】過肩中景、慢推（審稿必改 14：門這邊反打，唐小棠在左前景、馬車在畫右遠處，接 s36 許硯朝畫左看）：前景左唐小棠的背影，右手（畫右）按在右胯的小金算盤上，第一格食指撥兩下算珠，接著手指停在一顆珠上、肩膀僵住到最後一格（審稿必改 15；臉一白靠手與肩演）；腰帶正前方藍布錢袋（必改 11）；頭始終不轉。台詞 nospeak，剪接放錄音"),
    # Converted: an insert of her hands: the pouch tied shut, the packet taken up.
    dict(loc="academy_c", cam="Insert close-up, slow push in", chars=["tangxiaotang"], nospeak=["tangxiaotang"], night="academy",
         comp=f"insert close-up, the shot opens directly on her waist from its very first frame: {POUCH}, its drawstring held in two slender hands in peach-pink silk sleeves, and the small gold abacus hanging at her right hip; on the edge of the plain wooden table just beyond them {PACKET}; only her waist, her hands, the sleeves, the pouch, the abacus, the packet and the table edge are in the frame; bright sunlight",
         lines=[("tangxiaotang", "三百張收了一兩五錢，石叔那一成，我記在帳上。", "收好，盤算")],
         motion="the two hands pull the drawstring of the blue pouch tight and tuck the pouch into the front of her sash, then pick the oilcloth packet up off the table and draw it in against her, holding it with both arms",
         zh="【改插鏡】插鏡、慢推（第一格就是她腰間；審稿必改 5：spec 不送書院圖，只送唐小棠的定妝照當手、袖與腰帶的主人）：腰帶正前方的藍布錢袋、右胯的小金算盤（必改 11）；一雙桃粉袖口的手把錢袋口紮緊、塞進腰帶，再把桌邊的油布小包（留下的二十張）拿起來抱在懷裡；臉不入鏡，台詞剪接放錄音"),
    # ---- scene 3b: back up the river before dawn (the bow and Qin Shuang on screen right now), the ferry landing at dawn.
    dict(chapter="柳溪口", loc="predawn", cam="Wide shot, tracking", chars=["qinshuang", "xuyan", "tangxiaotang"], night="predawn", act=3,
         comp=f"wide shot past drooping dark leaves in the foreground, keeping the whole raft in the frame, the raft heading toward screen right: at the bow on screen right Qin Shuang, {QIN}, framed full length, leaning hard on {POLE}, her face three-quarter to screen right up the river, never the lens; straining: jaw set, brows drawn; at the stern on screen left {XU_COAT}, framed full length, small, pushing on {SHORTPOLE}, his face three-quarter to screen right, never the lens, lips closed; in the middle Tang Xiaotang {TANG}, small, curled up asleep against the one rolled-up empty oilcloth, {PACKET} hugged in her arms, her eyes closed; the lantern on its pole at the stern on screen left burning low; the only long things in the frame are the bamboo poles of the raft and the two green bamboo poles in their hands",
         lines=[],
         motion=f"Qin Shuang plants the pole and walks it back stroke after stroke, and the raft creeps upstream toward screen right; Xu Yan pushes on his short pole beside the stern; Tang Xiaotang sleeps on; {quiet('Qin Shuang, Xu Yan and Tang Xiaotang', 'their', True)}",
         zh="全景、跟拍、前景是岸邊黑葉：竹筏逆水往畫右走；筏頭（畫右）秦霜壓著青竹篙一篙一篙往上游撐；筏尾（畫左）許硯拿一根短竹竿幫著撐；中間唐小棠靠著捲起的空油布睡著、懷裡抱著油布小包（閉眼）；天亮前的深藍，筏尾燈籠在畫左低低亮著（審稿必改 16：送竹筏圖的水平鏡像 `set-zhufa-ye-l2-flip.png`，筏頭在畫右、只剩一捲空油布）；三人嘴閉著（無台詞）"),
    dict(loc="dawn", cam="Medium shot, slow push in", chars=["qinshuang"], night="dawn",
         comp=f"medium shot of Qin Shuang, {QIN}, standing at the bow of the raft, she stands on the green bamboo poles of the raft, framed from the knees up with clear space above her head, {POLE} in both her hands, her face three-quarter to screen right up the river toward the village, never the lens; the open water and the red dawn sky behind her on screen left; at first steady, then darkening: brows drawing down hard, eyes narrowing, lips moving low between words; {POLE_ONLY}",
         lines=[("qinshuang", "什麼味道？是煙，從村子那邊來的。", "聲音一沉")],
         motion=f"Qin Shuang's hands stop on the pole; she lifts her head and draws one breath through her nose, and her face darkens as her eyes find the smoke up the river; {NOSMILE}",
         zh="中景、慢推（審稿必改 16：spec 不送渡口圖，只送秦霜一張）：秦霜站在竹筏的青竹上，面向畫右上游、身後畫左是開闊的水與紅色天邊；撐篙的手停住，抬頭吸一口氣，臉一沉、眼睛找到上游的煙，聲音一沉地說（spec：視線在村子方向）；不笑"),
    # Xu Yan's point of view from the raft: nobody on the bank; Carpenter Shi's shout off screen.
    dict(loc="dawn", cam="Point-of-view wide shot, slow push in", chars=[], night="dawn", act=3,
         comp="point-of-view wide shot from a standing man's eye height over the front ends of the raft's bamboo poles in the bottom foreground, looking up the calm water to the ferry landing: the bare mooring posts, the low wooden jetty standing empty, the dirt path up the bank to the village houses on the right, and behind the houses the thick column of black smoke rising and rolling into the pale dawn sky above the village, the red glow low on the far left horizon; nobody anywhere on the bank or the jetty",
         lines=[("shimujiang", "許秀才——紙坊燒起來了！快回來！", "從坡上的院子遠遠嘶喊")],
         motion="the column of smoke rolls and climbs higher over the village roofs; the raft drifts slowly closer to the landing",
         zh="主觀（許硯站起來看上游）、慢推、下緣是竹筏筏頭的竹竿頭：渡頭的木樁、空著的矮木棧橋、上坡的土路到畫右的村子，屋後一柱黑煙往村子上方的淡色天空翻上去、紅霞低在畫左地平線（送重畫的 `set-dukou-l2`；審稿必改 18、建議）；岸上沒有人（石木匠的喊聲畫外）"),
    # The cliffhanger (bible 16->17): from behind her (LEFT foreground), Xu Yan standing facing us, Qin Shuang poling at the right.
    dict(loc="dawn", cam="Over-the-shoulder medium shot, slow push in", chars=["tangxiaotang", "xuyan", "qinshuang"], nospeak=["tangxiaotang"], night="dawn",
         comp=f"over-the-shoulder medium shot from close behind {TBACK}, kneeling on the raft in the left foreground, {PACKET} held against her in her left arm, her right hand (on screen right) gripping the grey sleeve of the young man in front of her; {only_tang('left')}; they are on the open bamboo raft of eight lashed green bamboo poles; facing us a step away, a little right of the middle, {XU_COAT}, standing, framed from the waist up with clear space above his head, his face three-quarter to screen right toward the smoke up the river, never the lens; shocked: eyes wide, brows drawn, jaw tight, lips pressed shut; at the right edge at the bow Qin Shuang, {QIN}, framed from the waist up, soft, both hands driving {POLE} down into the water, her face in profile to screen right, never the lens, jaw set, lips closed; the far bank and the black smoke beyond them in the pale dawn sky; exactly three people",
         lines=[("tangxiaotang", "紙坊燒起來了……裡面，還有人嗎？", "驚")],
         motion=f"the young woman with the two buns and pink ribbons in the left foreground keeps her head still, the back of her head toward us the whole shot, and tugs his sleeve hard twice; Xu Yan's eyes stay fixed on the smoke; Qin Shuang drives the pole down and the raft lurches toward the bank; {quiet('Xu Yan and Qin Shuang', 'their', True)}",
         zh="【改背後拍】過肩中景、慢推（送重畫的 set-dukou-l2：棧橋空著、村後一柱黑煙；審稿必改 16、17）：前景左唐小棠跪在竹筏上的背影，左臂抱著油布小包，右手（畫右）抓住許硯的灰袖子扯兩下（審稿必改 3：『頭不轉』點名是綁粉緞帶的她、放在秦霜動作前）；許硯站在她前面（畫面中偏右）盯著上游的煙、眼睛睜大、嘴閉著；畫右緣筏頭秦霜兩手把竹篙往水裡一撐、竹筏往岸邊一衝（側臉、嘴閉著）；頭始終不轉。台詞 nospeak，剪接放錄音（結尾，懸念接第 17 集）"),
]

HEAD = [
    "- 重製版 r2、真人版（站主 2026-11-11「之後都用真人版」）：照 `docs/videos/zhong-tian-qu-qi-e016-r2/script.md`（c01–c42 對應 s01–s42；2026-11-06 的 r2 稿；含「這版改了什麼」「2026-11-06 審稿後的修改」與「真人版的改動（2026-11-15）」）；台詞一字不改，只改拍法；每鏡一個看得見的動作、一句一筆不拆半句、預設不笑。篇章設定 `production/r2-bible-e011-e020.md`（拍法 1–18 條）。",
    "- 內部工作編號 916（`hailuo/{ff,clips}-dh-e916.json`、`colab/runs/e916/extras.json`、`colab/runs/e916-live/spec.json`，工作資料夾 `~/mokaair-work/videos/zhong-tian-qu-qi-e916-dh/`）；發布 slug `zhong-tian-qu-qi-e016-r2`。不放集數、不放片名卡；s01 接第 15 集 s42 的同一刻，從橫木另一邊拍（賴三的背在畫右前景、許硯在畫左）。",
    "- 照第 15 集審稿後的寫法與第 13–15 集挑片的教訓一開始就照做：`OFFSCREEN_SPEECH = False`；畫外句、心裡話、系統句與錄音鏡，畫面上每個人寫整鏡不說話；背景寫在場的東西；竹篙寫成青竹、通身圓滑、兩頭平切；竹簾只寫形狀（平的細竹絲席、木邊、正中一片柳葉），平端像托盤；紙空白、正面或側面打光，不從背後透光；不笑寫成皺眉、嘴角往下、抿嘴、鼻子哼一聲，說完最後一個字也寫一個動作。手與道具寫在第一格的構圖句裡，每樣道具寫在主人的那隻手（第 15 集 s41 算盤跑到賴三手上）。",
    "- 唐小棠十四句台詞都不露嘴、放錄音（nospeak）：s03、s06、s16、s20、s24、s26、s29、s32、s33、s37、s42 從她背後拍，每鏡寫明「畫面裡只有她一個雙丸子頭粉緞帶的人」與她固定在哪一側（第 15 集 s26、s41 背影鏡冒出第二個她）；s27、s38 是她手的插鏡；s04 是她的主觀鏡（畫外）。spec.json 拿掉她三張臉部參考圖與身分句。她不說話的臉（s01、s07、s11、s18、s34、s39）用第 7 集的中性外貌句。",
    "- 賴三本集不給正臉（稿子）：s01、s07 過肩與全景的背影不點名、不送圖；他自己的兩句（s02、s08）從背後拍、nospeak，spec.json 拿掉他的定妝照與身分句。",
    "- 兵器：本集沒有刀（秦霜腰帶整集空著）；兩根竹篙寫成青竹；家丁只寫扶橫木的手。一鏡最多三張有名字的臉；書生寫小、只見側臉或背影。",
    "- 場景：石橋 `set-shiqiao-l2`（沿用）；審稿後**重畫四張**（`live-action/screen-test-e016.py`，種子 37013／37014，還沒跑；`prep916.sh` 在四張圖與竹筏鏡像都進 refs-live 之前停住）：工棚 `set-gongpeng-l3`（從 l2 改：地面光禿的夯土、最左只剩光禿石牆、兩個桶沿光禿；稿子的第三個盆寫成木桌前一個新的小圓盆）、竹筏夜景 `set-zhufa-ye-l2`（l1 同構圖的真人實拍質感；`gen-dh.mjs` 的 SET 加 `bamboo raft` 一行；s39 逆水用它的水平鏡像 `set-zhufa-ye-l2-flip.png`）、縣學書院門口 `set-shuyuan-l2`（一般焦距、素平空白木匾、素牆、屋簷不掛白板；門這邊往街上拍的 s29、s32、s33、s34、s37 另寫場景句：街與馬車在畫右）、柳溪口 `set-dukou-l2`（村後一柱黑煙、棧橋空著）。插鏡 s12、s27、s31、s38 與 s35 車裡、s40 竹筏上不送場景圖。",
    "- 新出場：孫掌櫃（`sunzhanggui-portrait-l1`，第 7 集畫的瘦長臉、花白鬍、綠緞袍），聲音照 `cast.json` 的 Charon；只在 s35 馬車裡。extras.json 把他造型句的「smiling」與「(no jade balls)」拿掉（否定名詞）。",
    "- 長鏡要買的秒數（BUY）：照 39 句錄音核過（`~/mokaair-work/videos/zhong-tian-qu-qi-e916-dh/audio`，見 `r2.py` 的 BUY 註解）：4 鏡買 8 秒（s23 系統加心裡話 7.8 秒，即稿子的長鏡；s07、s09、s13 台詞前後有好幾拍動作），s27 插鏡由 5 秒改 6 秒（a26 5.32 秒），其餘 6 秒（不能笑的 s11 石木匠、s35 孫掌櫃與唐小棠的背影都留 6 秒）。a18（s20 打哈欠那句）6.56 秒，句尾靜音剪到約 0.1 秒（6.23 秒，剪前的檔在 `audio/trim-takes/`），s20 照 6 秒。",
    "- **獨立審稿**（`writer-tools/e016-r2/review.md`，2026-11-15，必改 18、建議 18）照改，逐條見 `r2.py` 的註解與 script.md〈2026-11-15 獨立審稿後的修改〉；四張場景圖由協調者決定重畫。剪接：s20 錄音 6.23 秒，句尾約 0.2 秒延到 s21 開頭；s23 系統那句可往前疊到 s22 尾巴（或句間縮到 0.3 秒）。",
    "- **表上的「秒」欄是 lint 估法**，比錄音短；剪接以錄音長度＋0.5 秒為準。",
]
FOOT = [
    "- **參考圖**（`assets/refs-live/`）：許硯、唐小棠（l1 交領）、秦霜、石木匠（`shimujiang-portrait-l1`）、孫掌櫃（`sunzhanggui-portrait-l1`）；賴三（`laisan-portrait-l1`）兩鏡都由 spec 拿掉。場景 `set-shiqiao-l2`，與四張重畫的 `set-gongpeng-l3`、`set-zhufa-ye-l2`（＋鏡像 `set-zhufa-ye-l2-flip.png`）、`set-shuyuan-l2`、`set-dukou-l2`（**還沒畫**：`live-action/screen-test-e016.py`，manifest `~/mokaair-work/videos/_series/zhong-tian-qu-qi/live-screen-test-e016/e016.json`，8 支）。",
    "- `gen-dh.mjs` 的 SET 加一行：`bamboo raft` → `dh-set-zhufa-ye-t1`（排在 `bamboo grove` 與 `stream|…|reeds` 前、`ferry landing` 後：柳溪口那幾鏡寫了竹筏也送渡口圖）；第 910–915 集重建逐位元相同。`live-action/pilot.py` 取最新 l 版時只認 `set-<id>-l<N>.png`（竹筏鏡像 `-l2-flip` 不會被當成新版）。`build-r2.py` 的 EN 與 `cast.json` 不用改（孫掌櫃、賴三、石木匠都已登記）。",
    "- `colab/runs/e916/extras.json`（照 e915：畫面不放字幕、空氣清澈那句；拿掉秦霜造型句的柴刀；石木匠的造型句改宋式交領短工衣、皮圍裙不寫木屑；孫掌櫃的笑眼與否定名詞拿掉、綠緞袍寫成宋式交領）與 `colab/runs/e916-live/spec.json`（`mkspec.py` 產生；種子 9161101／9161102）。",
    "- 免費準備：`prep916.sh`（`DRY=1 REFS=~/mokaair-work/videos/zhong-tian-qu-qi-e916-dh/runpod/refs-dh-e916 VIDEO_JSON=docs/videos/zhong-tian-qu-qi-e016-r2/video.json st1-ep.sh 916` → `pilot.py runpod/a/st1 runpod/live/st1 s01…s42` → `retake.py runpod/live/st1 runpod/live/d1 colab/runs/e916-live/spec.json` → `colab-jobs.json` 加 output_path → `preflight-prompts.py`）。草稿等 Colab 空出來再拍。",
    "- 配樂：第一場石橋輕 tension，s05「走水路」起轉明亮，s16「三百二十張」一個重音；第二場夜裡竹筏安靜的笛子與水聲，s24「賣給書生」一個輕重音；第三場書院前市集節奏，s31 不洇墨一個重音，s35 馬車換低沉弦樂，s40 起只剩低鳴，s41 喊聲一個大重音。音效表見 script.md〈音樂與音效〉。",
]

# Long shots: seconds to buy. Measured 2026-11-15 against the 39 recordings (~/mokaair-work/videos/zhong-tian-qu-qi-e916-dh/audio;
# ffprobe, silencedetect -35 dB / 0.3 s; e013's test: a shot holds (buy - 0.3) x 1.1 s of speech, half a second between lines).
# Every single line is 2.72-5.68 s and fits 6 s except a18 (s20, Tang Xiaotang's yawn line, 6.56 s with a 0.43 s tail): its
# tail was trimmed to about 0.1 s (6.23 s; the take before is in audio/trim-takes/) and s20 stays at 6 (her back; a long back
# shot is time for the head to turn).
# 8 s go to: s23, the script's long shot (system a21 2.88 + thought a22 4.40 + 0.5 = 7.78 s), and the shots whose action has
# several beats before or around the line: s07 (turn the cart, two steps, look back, then a 4.08 s line), s09 (dip and lift
# the mat while the cart is pushed in; a09 5.28 s), s13 (come in, stand the pole, walk over, then a 5.40 s line).
# s27 (the hand insert) gets 6 instead of gen-dh's 5 (a26 5.32 s). Laugh-prone faces stay at 6: Carpenter Shi s11 (a11
# 5.28 s), Sun Zhanggui s35 (a33 5.48 s). Lai San's slow a02 (4.96 s, pauses 0.67/0.84 s) is said with his back to us, so the
# pauses need no lip sync. Every other shot is 6.
BUY = {"s07": 8, "s09": 8, "s13": 8, "s23": 8, "s27": 6}
