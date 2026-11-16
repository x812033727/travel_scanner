"""Episode 23 remake (r2): the writer spec for ../e001-r2/build-r2.py. Source: docs/videos/zhong-tian-qu-qi-e023-r2/script.md
(c01-c40 = s01-s40, c13 split into s13 and s13b; the CG-era r2 script), including its sections 「這版改了什麼」, 「2026-11-06 審稿後的修改」 and
「真人版的改動（2026-11-16）」, which override the tables. Every line is the script's, word for word; only the staging changes.
Bible: production/r2-bible-e021-e030.md (rules 1-30, the 22->23 and 23->24 hand-overs, the props and picture tables). The third
episode of arc 3 〈搶親〉: midnight at the ferry landing, the boat through the night to sunrise, the county inn in the afternoon.

Written from the start the way e022-r2/r2.py stands AFTER its independent review (../e022-r2/review.md), with the e921 and e920
lessons (colab/runs/e921-live/{picks-merged.tsv,fix1/mkspec.py}, e920-live/review3-plan.md, refs-live/README.md arc 3):
- OFFSCREEN_SPEECH = False (rule 15): every shot with an off-screen line, a thought or a system line writes the silence of
  each person on screen (quiet(), SILENT_HE).
- Tang Xiaotang never speaks on camera (rule 3): every one of her lines on screen is from behind her (TBACK, nospeak; spec
  drops her pictures and identity sentence): s03, s07, s10, s14, s17, s18, s20, s22, s24, s27 on the boat; s29, s31, s33, s36
  at the inn. Her silent faces: s19 (the blush while he laughs), s37 (side by side with him), s40 (looking at Wei Shaoqing
  while the system speaks); l1 and angle-a only (her long-ribbon angle-b nowhere), no abacus in her identity sentence.
  s01 and s21 show her small and unnamed (peach-pink, two buns) on the boat, no picture.
- The gold abacus (rule 20 as corrected by the coordinator, 2026-11-16, the bible's props row: the long flat abacus of the
  prop picture, as long as her forearm, inserts only; the palm-sized wording is withdrawn): only in the three lap inserts s11, s15, s25, the prop picture prop-jinsuanpan-l1 in the
  set slot and NOBODY_ABACUS (no "the set layout stays as it is": e022 必改 11, the prop picture's cabinet grew a second
  abacus in e920 s37b). The script's untying (c10), picking up (c22), holding (c24) and hanging it back (c27) are not shot;
  the sound effects carry them. Every other shot of her writes her hands in her lap or on the table, the abacus unnamed.
- Wei Shaoqing's fan stays closed in every shot (e921 fix1 s28: an open fan's face grew brush calligraphy in both seeds):
  the script's half-open fan (c28), its fanning (c30) and the fan flicked open by his face (c38) are written closed, tapped
  or held upright like a short slim stick (FAN). He may smile (rule 30): s28, s30, s32, s37, s38.
- Name only what should be drawn (e920 fix1): the wager is rule 27's plain paper, only folded or its blank side; the red
  paste is one small dish in s39 only; the elders are three thin old men by the screen, soft, side-on, never a front face
  (rule 25), no pictures; the boatman (rule 23) only from behind or side-back.
- Rule 23 (water): the water up to his thighs every time he is in it, both empty hands held up, no swimming. His robe is
  soaked dark from the thighs down from s02 to s18, half-dry s19-s21, dry and creased with a ring of dried mud at the trouser
  hems at the inn. The lantern stays stuck upright in the mud at the landing (s01), nobody holding it.
- Back views without a face picture keep his hair right (e921 fix1 s36): the unnamed small figures write their hair.
- A night set with no set picture drifts to a street-stall look (e921 s21b, s22b, s23): every night shot on the water sends
  a picture; the close shots on the boat send a free plate of plain fog (set-chuan-ye-wu-l1), the dawn ones a plate of pale
  mist (set-chuan-chen-wu-l1) (both cut from the boat pictures where only fog is; looked at full size).
- No more than three named faces (rule 1): s37 Wei Shaoqing, Tang Xiaotang, Xu Yan (the elders soft, side-on). Unnamed
  foregrounds get no picture (rule 2): her buns at the left edge in s34, Wei Shaoqing's hand in s39-s40.
- Nobody is flipped (rule 9); sides are screen left/right. One visible action per shot; props in a named hand from the
  first frame; nothing negated by name (rule 18). One finger read as the middle finger (e916): s36 pushes the paper with
  the flat of her fingers.

AFTER THE INDEPENDENT REVIEW (review.md in this folder: the 11 必改 all applied as written, the cheap 建議 the coordinator
listed taken; 2026-11-16, the coordinator deciding for the owner; where this differs from the paragraphs above and below,
this wins):
- The night fog plate (必改 1): set-chuan-ye-wu-l1 remade under the same id with eq=saturation=0.55:gamma=0.75 (mean RGB
  44/109/143 -> 34/73/87, as dark as set-chuan-ye-l1; no clip had been shot with it). The sunrise mist plate (建議 1):
  set-chuan-chen-wu-l1 remade under the same id with colorbalance=rm=0.10:bm=-0.10:rh=0.10:bh=-0.12 (156/158/162 ->
  174/158/141, the warm gold of its mother's top). refs-live/README.md has both commands and what was seen at full size.
- Water and framing (必改 2): s03 he stands in the river framed from the waist up, the boat's low edge at his waist and both
  hands flat on it, the water at his thighs; she kneels at the boat's side leaning out and looking down at him (boat_back
  takes facing=, no "facing left toward the stern" there). s04 waist up, the edge at his waist, the water at his thighs.
  s05 is a high-angle medium shot from her height, framed from his thighs up, the edge across the lower right corner;
  LOC boat_w puts him "in the dark river water beside one small boat" (never on it) and LIGHT boat_w names only the fog and
  the far glow on the shore.
- Back views (必改 3): s07 is shot side-on as its set picture is (bow and lantern on the right, the near side of the boat in
  the foreground), she sits "turned away from us toward the far side of the boat"; s17 and s22 "facing straight away from
  us"; s27 too, and its boatman "standing with his back to us, his wide hat brim hiding his face" (no side-on).
- The inn (必改 4): s28 Xu Yan half hidden behind her with the head-still line of his own; the three elders already stand
  just inside the door, backs to us, and stay there (fewer people moving). s29 the elders side-on, turned toward Wei
  Shaoqing, faces in profile. s31 and s36 put Xu Yan back at her right shoulder as in s29 (chars and pictures: his l1 and
  angle-a; "exactly three people"; his silence written).
- The wager (必改 5): WAGER is "one sheet of thick smooth cream paper folded in half, its blank outside facing up, smooth and
  empty" in s29, s31, s36, s37; s37 lays it soft at the very bottom edge of the frame; s40's thumb presses on the same
  paper. s39 keeps "its plain blank side up".
- s20 buys 8 s (必改 6; BUY). s18 "lips pressed together and still" (必改 7).
- 建議 taken: the fog and mist plates show no canopy, so boat_c and dawn_c say only fog or mist, the close shots' backgrounds
  "only the thick grey fog", and where he sits "under the canopy" one curved rib of dark bamboo is written just above his
  head (RIB, UNDER); s14 an over-the-shoulder close shot, her head and shoulder filling the right third; s24 a low-angle
  over-the-shoulder shot from the height of the boards; s21 "the only spot of pink anywhere in the picture"; the inn
  "on a bright winter afternoon" (not clear: a blue sky would fight the picture's grey-white window).
- 建議 not taken: the optional window crop set-kezhan-pm-chuang-l1 was made and looked at full size but is not sent
  (two thirds of it is the overcast sky seen from under the eaves outside; as the only picture of a close shot it would
  seat Wei Shaoqing on a veranda against a grey sky, and s38 writes the screen, which it lacks; e022's close shots of him
  without a set mostly passed). Not on the coordinator's list, so left for the picks: the over-the-shoulder Xu Yan "a
  little left of the middle" with her "facing into the frame" (s10, s18, s20 keep "facing left toward the stern"), the
  lantern light sentence of the fog close shots (only s05's changed, with 必改 2), the wet-robe sentence on chest-up shots,
  s01 "a few boat lengths", s08's gaze, s19 side-on, s30 the fan on his palm, s34 his left hand, s36 buying 8 s (only if the
  picks need more than 0.6 s off its head). The ribbon (建議 15) is accepted as e920-e922.
- Recordings a37, a32 and a29 stay as they are (the review agrees).

THE AXES (rule 29: the set picture decides):
- Ferry landing (set-dukou-ye-l1, as e022 s39-s41): the old pier from the LEFT, reeds at the lower left, still water and fog
  on the right; the boat (not in the picture) written ten metres out on the right. He wades out from the reeds at the left.
- The boat at night (set-chuan-ye-l1): the arched woven canopy in the middle, the bow with its lantern pole to the RIGHT,
  the stern to the left. Xu Yan sits at the stern-side mouth of the canopy (LEFT), Tang Xiaotang under the canopy (RIGHT),
  the boatman at the bow (far right). Her back shots: she in the right foreground, he beyond her on the left looking screen
  right. His close shots look screen right toward her; hers from behind look left at him, or ahead (right) at the water.
- The boat at sunrise (set-chuan-chen-l1, s19 on; bible rule 23): the same boat, the lantern unlit, low gold sun on the
  RIGHT. From s22 she sits forward at the bow (still right), he moves closer behind her (left).
- The inn in the afternoon (set-kezhan-pm-l1, the free warm grade of e022's room): the window and the bench under it on the
  LEFT, the square table in the middle, the folding screen at the back, the double door in the RIGHT wall (as e022). Wei
  Shaoqing on the bench (the script's carved chair), looking screen right; Tang Xiaotang at the right side of the table, her
  back to the door, Xu Yan at her right shoulder; the elders by the folding screen at the back. The picture's window is
  still grey-white: "the bright pale sky" and warm light are written, the slanting sunbeams are not.

PLACES (the coordinator's decisions, 2026-11-16; every picture looked at full size; script.md 〈真人版的改動〉):
- Ferry s01: set-dukou-ye-l1 (swapped for set-dukou-l2). s02 (his legs into the water): the free crop set-dukou-ye-shui-l1
  (the reeds and dark water at the foot of the pier).
- Night boat, wide and medium s04, s07: set-chuan-ye-l1 (swapped for set-dukou-l2: the boat prompts say "ferry landing" so
  gen-dh gives a set with a live picture, as e022 s40). Close and over-the-shoulder shots s03, s05, s06, s08-s10, s12-s14,
  s16-s18: the fog plate set-chuan-ye-wu-l1. Lap inserts s11, s15: prop-jinsuanpan-l1.
- Sunrise boat, s19 and s21: set-chuan-chen-l1; s20, s22-s24, s26, s27: the mist plate set-chuan-chen-wu-l1; s25:
  prop-jinsuanpan-l1.
- Inn s28, s29, s37, s40: set-kezhan-pm-l1; inserts s35, s39: the free crop set-kezhan-pm-table-l1 (e022's table crop on the
  afternoon grade); close shots s30-s34, s36, s38 none.
- gen-dh SET phrases: "ferry landing" (never "ferry boat", which takes the CG boat id), "county inn guest room".
- Inserts and shots with nobody named (s02, s06, s21, s35, s39) open their motion with NOBODY; the lap inserts s11, s15, s25
  with NOBODY_ABACUS (their clips-dh text holds "keeps the first frame's set layout and props. " once instead).
- Shared files: no code changed (every speaker is in build-r2.py's EN; no new gen-dh place; cast.json untouched). Four new
  free pictures in refs-live (new ids with their own l1, rule 19; README paragraph).
"""
EP = 923  # internal working number; the published slug is zhong-tian-qu-qi-e023-r2
SLUG = "zhong-tian-qu-qi-e023-r2"
EP_TITLE = "他涉水追上船，她說出真相，賭上自己（重製版 r2）"
OUTLINE_SECONDS = 200  # script.md: 199.5 s, 40 shots (8 + 19 + 13)
TARGET_MINUTES = [3, 4]
TITLE = "妳不是我贏來的，也不是誰的債｜種田娶妻打天下 第23集（重製版）"
DESCRIPTION = "子時，許硯把燈籠插在渡口的泥裡，涉進初冬的溪水追船：船家，回頭！唐小棠罵他瘋了，還是把他拉上了船。船往縣城撐了一整夜，她終於說出實話：宰相扣了唐家八條鹽船，逼她爹把她指給魏家；她拿一支金釵跟媒婆換了病死的林二丫的名額，躲進配婚名冊。許硯說：妳不是我贏來的，也不是誰拿來抵的債。天亮時她擦乾眼淚：這門親，她要自己去賭掉。午後在縣城客棧，她當著商會三位老人跟魏少卿立下賭約：許記跟魏記鬥商三十日，許記贏，他撤婚書；輸了，她跟他回京。魏少卿笑著把拇指按在紙上。系統跳出紅框：強制任務，失敗，唐小棠好感歸零。《種田娶妻打天下》第 23 集（重製版）。"
THUMB = ("妳不是我贏來的", "s12")
CHARACTERS = ["xuyan", "tangxiaotang", "weishaoqing", "xitong"]
MINOR = {}
MUSIC = "one cue per scene: a long erhu note over fog at a river landing joined by a low drum pulse, one soft accent as a hand reaches down; then a slow piano and erhu on a boat at night, one soft accent on a quiet promise, brightening and moving forward at sunrise, one accent on a decision; then a tense cue with an abacus-like rhythm in an inn room, one accent on a call for witnesses and one big accent with a red warning before it ends; ancient Chinese rural drama, no vocals"

# Places (gen-dh SET phrases in the first words of each LOC; see the docstring).
PIER = ("an old wooden pier on thin posts running out over the water from the left, a clump of dry reeds and a strip of black mud "
        "at its foot on the left, flat still dark water filling the right, a low line of reeds far off on the right fading into the fog")
BOATD = ("one small dark wooden boat with an arched canopy of woven bamboo over its middle, its bow to the right with one round paper "
         "lantern glowing warm on a bamboo pole, a long bamboo pole lying along its side, a folded grey blanket on the boards under "
         "the canopy")
BOATD_DAWN = ("one small dark wooden boat with an arched canopy of woven bamboo over its middle, its bow to the right with one round "
              "white paper lantern, unlit, on a bamboo pole, a long bamboo pole lying along its side, a folded grey blanket on the "
              "boards under the canopy")
BENCH = "a long low plain wooden bench under the window"
TABLE_INN = "the square dark-red wooden table"
TEA = "one brown clay teapot and two small clay cups"
INN = ("a wide window in the left wall with one dark wooden lattice shutter folded back, grey tiled roofs and a bright pale sky "
       f"beyond it, {BENCH}, a square dark-red wooden table in the middle of the room with {TEA} on it, a small square side "
       "table and a four-panel folding screen of plain cream panels against the dark back wall, a double door of dark wood "
       "in the right wall, dark wooden walls and a dark plank floor")
LOC = {
    "ferry": f"At the ferry landing of Liuxi at midnight in thick fog: {PIER}; everything cold grey-blue",
    "ferry_w": "At the ferry landing of Liuxi at midnight in thick fog, in the black water at the foot of the pier among dry reeds, in cold grey-blue light",
    "boat": f"Out on the water off the ferry landing of Liuxi at midnight in thick fog: {BOATD}; flat still dark water and grey fog all around, tall reeds dim far off on the right",
    "boat_c": "On a small boat out on the water off the ferry landing of Liuxi at midnight, thick cold grey-blue fog all around",
    "boat_w": "In the dark river water beside one small boat off the ferry landing of Liuxi at midnight, thick cold grey-blue fog all around",
    "boat_t": "On a small boat off the ferry landing of Liuxi at midnight, under its woven bamboo canopy in dim warm lantern light",
    "dawn": f"Out on the river downstream of the ferry landing of Liuxi at sunrise: {BOATD_DAWN}; flat calm water, thin pale mist lit warm gold by the low sun on the right, reeds along the far bank",
    "dawn_c": "On a small boat on the river downstream of the ferry landing of Liuxi at sunrise, thin pale mist all around over the water, lit warm gold from the right",
    "dawn_t": "On a small boat on the river downstream of the ferry landing of Liuxi at sunrise, in warm low morning light",
    "inn": f"In the county inn guest room upstairs on a bright winter afternoon: {INN}; warm afternoon light from the bright window on the left, the corners of the room dim",
    "inn_c": "In the county inn guest room upstairs on a bright winter afternoon, warm light from the window on the left",
    "inn_t": "In the county inn guest room upstairs on a bright winter afternoon, on the dark-red wooden table top in warm light",
}
LIGHT = {
    "ferry": "the thick cold grey fog and the one warm lantern glow stay unchanged",
    "ferry_w": "the cold grey-blue light and the dark water stay unchanged",
    "boat": "the thick cold grey fog and the warm glow of the one bow lantern stay unchanged",
    "boat_w": "the thick cold grey fog and the one far warm glow on the shore stay unchanged",
    "boat_t": "the dim warm lantern light stays unchanged",
    "dawn": "the warm low gold morning light and the thin mist stay unchanged",
    "dawn_t": "the warm low morning light stays unchanged",
    "inn": "the warm afternoon window light stays unchanged",
    "inn_t": "the warm light on the wood stays unchanged",
}
# bible rule 15: no "<X> speaks off screen" / "the system voice speaks off screen".
OFFSCREEN_SPEECH = False

# Repeated wording (each prop is one object, written the same way every time).
# e022 s27 on (script 角色表): the old grey outer coat over the robe, the whole episode
XU_N = "Xu Yan, in an old plain grey cloth outer coat worn open over his faded blue-grey scholar's robe"
# bible rule 23: the water to his thighs; the wet robe to s18, half-dry s19-s21, dry at the inn
WET = "his robe and coat soaked dark from the thighs down and clinging to his legs"
HALFDRY = "the lower half of his robe still damp and darker"
DRY = "his robe dry and creased, a ring of dried mud at the hems of his trousers"
# bible rule 30 with the portrait's jade (e020 review 必改 7, as e022)
WEI = ("Wei Shaoqing, in his sapphire-blue brocade robe woven with gold thread, a white jade pendant at his waist, a small green "
       "jade ornament at the front of his topknot")
# e921 fix1 s28: closed, its face never named
FAN = "one closed folding fan held upright in his right hand like a short slim stick, its dark bamboo ribs pressed tight together"
# her face shots (s19, s37, s40): the jacket only (e021 review 建議)
TANG = "in her peach-pink cross-collared short jacket wrapped shut across her chest"
LANTERN = "one round plain white paper lantern on its bamboo handle"
# bible rule 27: the wager (folded; the blank side only); the thumbprint in s39-s40 is a red smudge. e023 review 必改 11: one
# wording everywhere (s29, s31, s36, s37, s40), its texture and which side is up (e922 s30-s32's plain paper grew lines of text)
WAGER = "one sheet of thick smooth cream paper folded in half, its blank outside facing up, smooth and empty"
PASTE = "one small round shallow white dish of thick vermilion-red paste"
# bible rule 20 as corrected by the coordinator (2026-11-16, the props row): the series' abacus is the long flat one of
# prop-jinsuanpan-l1 (e920, e922 drew it long); "the size of a palm" is withdrawn. Inserts only, the prop picture sent.
ABACUS = ("one long flat gold abacus, as long as her forearm, a thin gold frame, lying flat across the skirt over her lap: a long "
          "row of thin gold rods set close side by side across its width, one thin gold crossbar running along its whole length, "
          "small round gold beads above and below the crossbar on every rod")
BOATMAN = "one boatman in a conical bamboo hat and a straw rain cape, seen only from behind"
# rule 25: the three elders, thin, never a front face, no picture
ELDERS = ("three thin old men in long Song-dynasty silk robes, one grey, one brown, one dark blue, each with a black square cloth "
          "cap and a short white or grey beard, standing together by the folding screen at the back, soft and out of focus, seen "
          "side-on")
HANDS = "their hands hold only what is described here"
SILENT_HE = "He says nothing in this shot: his lips stay pressed together from the first frame to the last, his jaw still, no talking, no mouthing words"
# No person named on screen: opens their motion so the clips-dh text holds "the set layout stays as it is. " once and the
# d1 prompt "never the mood. " once (refine-prep.py splices a retake's motion between those and "One continuous shot.").
NOBODY = "Throughout the shot the set layout stays as it is. The pictures fix the place and the objects only, never the mood. "
# the lap inserts (e022 必改 11): the prop picture's cabinet and shelves must not stay; refine-prep.py uses the clips-dh
# first-frame phrase "keeps the first frame's set layout and props. " (once); "never the mood. " stays once in the d1 prompt.
NOBODY_ABACUS = ("Throughout the shot the abacus keeps the long flat shape it has in <Picture 1>, and the pleated peach-pink silk "
                 "skirt fills the rest of the frame. The pictures fix the place and the objects only, never the mood. ")
# e916 fix1 / e918 review 必改 1 / e919 review 建議: two high round buns, a short ribbon round each, the nape bare.
TBACK = ("one young woman seen only from behind, appearing only once: the back of her head with all of her black hair gathered "
         "up into two round buns set high on her head, a short pink silk ribbon wrapped around each bun, the "
         "nape of her neck bare above a pink inner collar, and her light peach-pink silk shoulders; the back of her "
         "head toward us the whole time, her ear the furthest round her head we ever see")
HEADSTILL = "the young woman with the two high round buns keeps her head still, the back of her head toward us the whole shot"
# the unnamed small figures (s01, s21): their hair written (e921 fix1 s36)
SMALL_TANG = ("one small young woman in light peach-pink silk with her black hair in two round buns set high on her head, sitting "
              "hunched under the canopy with her arms around her knees, her back to us")
SMALL_XU = ("one young man in an old plain grey cloth outer coat over a blue-grey robe, his black hair in a topknot tied with a "
            "cloth band")


def quiet(who, pr="his", plural=False):
    verb = "say" if plural else "says"
    return f"{who} {verb} nothing in this shot: {pr} lips stay pressed together from the first frame to the last, no talking, no mouthing words"


def only_tang(side=None):
    """e915 s26/s41: a second Tang appeared beside her back. One person with buns, one fixed side."""
    if not side:
        return "she is the only young woman with two high round buns in the frame"
    return (f"she is the only young woman with two high round buns in the frame, and she stays in the {side} "
            f"foreground from the first frame to the last")


def boat_back(rest, frame="framed from the waist up", pose="sitting on the boards", facing="facing left toward the stern",
              shot="over-the-shoulder medium shot"):
    """Tang Xiaotang on the boat, seen from behind (rule 3): the camera behind her on the bow side looks left at him."""
    return (f"{shot} from close behind {TBACK}, {pose} in the right foreground, {frame}, {facing}; {only_tang('right')}; {rest}")


def inn_back(rest, frame="framed from the waist up"):
    """Tang Xiaotang at the inn, seen from behind (rule 3), as e022: the camera behind her on the door side looks across the table."""
    return (f"over-the-shoulder medium shot from close behind {TBACK}, standing at the right side of {TABLE_INN} in the right "
            f"foreground, {frame}, facing across the table; {only_tang('right')}; {rest}")


XU_FACING = "facing us beyond her on the left"
# e023 review 建議 2: the fog and mist plates have no canopy; the close shots write one rib overhead, never the canopy
RIB = "one curved rib of dark bamboo just above his head at the top edge of the frame"
UNDER = f"sitting on the boards, {RIB}"

SHOTS = [
    # ---- scene 1: midnight, the ferry landing (22->23: the same moment). The lantern stays stuck in the mud.
    dict(chapter="渡口", loc="ferry", cam="Wide shot, tracking shot that follows the subject", chars=["xuyan"], night="ferry",
         comp=f"wide side-on shot from the reeds at the foot of the pier, dry reed stems in the soft foreground: {XU_N}, framed from the knees up, already wading out from the black mud into the dark water on the left from the first frame, the water up to his thighs, both empty hands held up at his chest, his face in profile to screen right toward the boat, never the lens; desperate: brows up, eyes straining ahead, mouth open, panting; behind him at the water's edge {LANTERN} stuck upright in the mud, glowing warm, nobody holding it; far off on the right in the fog the dim dark shape of one small boat with an arched canopy of woven bamboo, already ten metres out, {SMALL_TANG}, and at its far end one boatman in a conical bamboo hat and a straw rain cape, a small dark shape seen only from behind; {HANDS}; exactly three people: Xu Yan in the water and the two small figures on the boat",
         lines=[("xuyan", "船家，回頭！船上是我娘子！", "喊，喘著氣")],
         motion="Xu Yan wades on toward the boat on the right, pushing hard through the water with his hands held high, shouting after the boat, his breath white in the cold air",
         zh="全景、跟拍（側面，前景是棧橋下的乾蘆葦；送渡口夜霧圖 `set-dukou-ye-l1`，圖上沒有船，船寫在鏡頭裡）：許硯第一格已經從岸邊黑泥走進水裡、水到大腿（拍法 23），兩手空著舉在胸前，邊涉水邊朝畫右霧裡的小船喊（喘著氣，呼白氣）；身後水邊一盞白紙燈籠插在泥裡、沒人拿；畫右遠處小船上一個桃粉色雙丸子的小背影、船尾斗笠蓑衣的船夫（都不點名、不送圖）。稿子『先站在棧橋盡頭、跳下泥灘、插燈籠』三個動作不拍：剪接從第 22 集 s41 的棧橋直接接他已在水裡（跳水、插燈籠交給音效）"),
    dict(loc="ferry_w", cam="Insert close-up, slow push in", chars=[], night="ferry_w",
         comp="insert close-up at water height, the shot opens directly on two legs in a man's soaked blue-grey robe hem and dark cloth trousers plunging knee-deep into the black water among dry reed stems from its very first frame; only the two legs, the robe hem, the water and the reeds are in the frame",
         motion=NOBODY + "the legs drive forward through the water toward the right, the water rising up to the thighs and splashing up in pale sprays, the robe hem soaking dark",
         zh="插鏡（水面高度）、慢推（第一格就是腳入水；送渡口棧橋下的免費裁切 `set-dukou-ye-shui-l1`）：許硯的兩條腿（濕透的藍灰袍襬、深色布褲）往畫右衝進黑水，水升到大腿、濺起水花（無台詞；拍法 23 水到大腿）"),
    dict(loc="boat_c", cam="Over-the-shoulder medium shot, slow push in", chars=["tangxiaotang", "xuyan"], nospeak=["tangxiaotang"], night="boat",
         comp=boat_back(f"both her hands gripping the wooden edge from the first frame; below her on the left, facing us, {XU_N}, standing in the river beside the boat, framed from the waist up, the boat's low wooden edge at the height of his waist and both his hands flat on it, the flat dark water around his thighs just below the edge, {WET}, his wet black hair stuck to his forehead, his face tilted up to her, three-quarter to screen right, never the lens; shivering and fixed on her: eyes wide, lips pressed shut, his breath white; behind him only thick grey fog over the dark water; {HANDS}; exactly two people, the young woman in the foreground seen only from behind", pose="kneeling at the boat's side", facing="leaning out over the edge and looking down at him"),
         lines=[("tangxiaotang", "你瘋了？這是初冬的水，會凍死人的！", "嚇壞，又氣又急")],
         motion=f"the young woman leans further out over the side toward him, her shoulders shaking; {HEADSTILL}; she looks down at Xu Yan the whole shot; {quiet('Xu Yan')}; he keeps looking up at her, his teeth chattering",
         zh="過肩中景、慢推（送夜霧的霧色底圖 `set-chuan-ye-wu-l1`）：前景右唐小棠的背影第一格已經跪在船舷邊、兩手抓著船舷往外探，朝水裡的許硯（畫左下，臉朝畫右往上看她，濕髮貼額、呼白氣、嘴閉著、牙齒打顫）說；台詞 nospeak，剪接放錄音（拍法 3）。稿子『回頭、撲到船舷』的轉頭不拍（從背後拍，回頭會露臉）；船邊的水深照拍法 23 不寫他游泳。審稿必改 2：他腰以上取景、站在水裡，船舷在他腰的高度、兩手平按在船舷上、水在大腿；她跪在船舷邊往外探、往下看他（不寫『臉朝船尾』）"),
    dict(loc="boat", cam="Medium shot, slow push in", chars=["xuyan"], night="boat",
         comp=f"medium shot along the boat's side, the dark wet wooden edge of the boat in the soft foreground: at the right end of the boat {BOATMAN}, standing, both hands on one long bamboo pole, the lantern on its pole beside him; in the lower left foreground {XU_N}, framed from the waist up, standing in the river with the boat's low wooden edge at his waist and both hands gripping it, the dark water around his thighs, {WET}, his face three-quarter to screen right up toward the canopy, never the lens; spent: mouth open, panting, his breath white; {HANDS}; exactly two people",
         motion=f"the boatman stops poling, turns his hat a little toward the side so that only its rim shows, and drives the pole down into the riverbed to hold the boat still; {quiet('Xu Yan')}; he hangs on to the boat's edge, panting",
         zh="中景、慢推（前景是船舷；送夜霧小船圖 `set-chuan-ye-l1`）：船頭的船夫（斗笠蓑衣，背影，不點名、不送圖）停篙、斗笠往旁邊偏一點（只露帽沿）、把篙插進溪底穩住船；左下許硯腰以上、站在水裡，船舷在他腰的高度、兩手抓著，水在大腿（審稿必改 2），喘氣、呼白氣、嘴閉著；沒有人說話"),
    # He may give a wry smile (script c05).
    dict(loc="boat_w", cam="High-angle medium shot, slow push in", chars=["xuyan"], night="boat_w",
         comp=f"high-angle medium shot looking down from the boat's edge at {XU_N}, framed from his thighs up, standing in the river with the flat dark water around his thighs, the boat's low dark wooden edge across the lower right corner at the height of his waist, his left hand on it, his right hand already reaching up toward the upper right edge from the first frame, {WET}, his wet black hair stuck to his forehead, his face tilted up three-quarter to screen right toward Tang Xiaotang off screen above the right edge, never the lens; frozen but stubborn: a crooked rueful half smile, his teeth chattering, his breath white, lips moving between chattering words; behind him only thick grey fog over the dark water and one far small warm glow of a lantern on the shore",
         lines=[("xuyan", "冷，冷得要命。所以妳先拉我上去，再罵。", "牙齒打顫")],
         motion="Xu Yan holds his right hand up toward her as he speaks, his shoulders shaking with cold; after the last word he keeps the hand up, waiting",
         zh="俯角中景、慢推（審稿必改 2：從船舷、她的高度往下拍，大腿以上取景看得到水位；地點句寫他在船邊的水裡，不寫在船上；光句只寫霧與岸上遠遠一點暖光；送霧色底圖）：許硯站在船邊水裡、水到大腿、船舷在畫右下角他腰的高度、濕髮貼額、牙齒打顫、呼白氣，左手抓船舷、右手往上伸給畫右上方的唐小棠（畫外），苦笑著說（本鏡可以苦笑）；身後只有霧與岸邊遠遠一點燈籠光"),
    dict(loc="boat_c", cam="Insert close-up, slow push in", chars=[], night="boat",
         comp="insert close-up, the shot opens directly on a small hand in a thick opaque peach-pink silk sleeve cuff already gripping a man's wet wrist in a soaked blue-grey sleeve cuff above the dark wooden edge of the boat from its very first frame; only the two hands, their sleeve cuffs, the wooden edge and the dark water below are in the frame",
         motion=NOBODY + "the small hand pulls hard upward, and the man's other hand slaps onto the wooden edge and heaves, water streaming off the sleeve as the wrist rises up over the edge",
         zh="插鏡、慢推（第一格就是兩隻手；送霧色底圖）：唐小棠的手（桃粉不透的織錦袖口）抓住許硯濕透的手腕（藍灰袖口）用力往上拉，他另一手拍上船舷撐上來，水從袖子流下；翻上船、跌坐交給 s06→s07 的剪接（無台詞）"),
    dict(loc="boat", cam="Wide shot, slow push in", chars=["xuyan", "tangxiaotang"], nospeak=["tangxiaotang"], night="boat",
         comp=f"wide side-on shot of the boat as in the set picture, its bow and lantern on the right, a dark wet stretch of the near side of the boat in the soft foreground: on the left {XU_N}, already sitting on the boards at the stern-side mouth of the canopy from the first frame, framed full figure, both hands wringing the soaked hem of his robe, {WET}, his face three-quarter to screen right toward her, never the lens; miserable and stubborn: lips pressed shut, shivering; on the right under the canopy, an arm's length from him, {TBACK}, sitting with her arms around her drawn-up knees, turned away from us toward the far side of the boat and the fog beyond it; {only_tang()}; at the bow on the right {BOATMAN}, standing, both hands on one long bamboo pole; {HANDS}; exactly three people: Xu Yan, the young woman seen only from behind and the boatman seen only from behind",
         lines=[("tangxiaotang", "你回去。船家，別管他，照樣往縣城撐。", "別過臉")],
         motion=f"{HEADSTILL}; she sits stiffly turned away from us the whole shot; Xu Yan twists the hem of his robe and water drips onto the boards, and he shivers once; {quiet('Xu Yan')}; the boatman stands still at the bow",
         zh="全景、慢推（審稿必改 3：照送的夜霧小船圖從側面拍，船頭與燈在右，前景是近側濕黑的船身）：左邊許硯第一格已經坐在竹篷口的船板上擰濕衣襬、水滴在船板上、打一個哆嗦、嘴閉著；右邊竹篷下唐小棠的背影抱膝、背對鏡頭朝船的另一側與霧（『別過臉』照背影拍；不寫『臉朝船頭』，側面拍時那是畫右、會露側臉）說；船頭船夫（背影）。台詞 nospeak"),
    dict(loc="boat_c", cam="Medium shot, slow push in", chars=["xuyan"], night="boat",
         comp=f"medium shot of {XU_N}, {UNDER}, framed from the waist up with clear space above his head, {WET}, his face three-quarter to screen right toward the bow beyond the right edge, never the lens; settled and stubborn: calm eyes, lips moving between words; soft in the background on the right, at the bow, {BOATMAN}, standing with both hands on one long bamboo pole; behind them thick grey fog; {HANDS}",
         lines=[("xuyan", "船家，往縣城就往縣城，我跟她一起去。", "對船頭，冷得聲音發抖")],
         motion="Xu Yan lifts his right hand toward the bow as he speaks; in the soft background the boatman dips his hat once and pushes the pole down, and the fog begins to slide past behind them",
         zh="中景、慢推（送霧色底圖）：許硯坐在竹篷口，朝船頭抬手示意、說；右後虛焦船頭的船夫（背影）點一下斗笠、撐篙，霧開始往後滑。稿子『轉回頭看唐小棠』不拍（一鏡一個動作）（結尾）"),
    # ---- scene 2: the boat through the night (thick fog, set-chuan-ye-l1; close shots the fog plate).
    dict(chapter="船上", loc="boat_c", cam="Medium close-up, slow push in", chars=["xuyan"], night="boat",
         comp=f"medium close-up of {XU_N}, {UNDER}, leaning forward with both elbows on his knees, framed from the chest up with space above his head, {WET}, his face three-quarter to screen right toward Tang Xiaotang off screen right, never the lens; serious, the smile gone: steady eyes, brows level, lips moving between words, his breath white; behind him only the thick grey fog, soft",
         lines=[("xuyan", "船到縣城還要一整夜，妳為什麼走，這回說實話。", "收起笑，認真，冷得聲音帶抖")],
         motion="Xu Yan leans a little further toward her as he speaks; after the last word he holds still and waits, his eyes on her",
         zh="中近景、慢推（送霧色底圖）：許硯在竹篷下身子往前傾、兩手肘撐在膝上，收起笑、認真地對畫右的唐小棠（畫外）說，說完不動、等她"),
    dict(loc="boat_c", cam="Over-the-shoulder medium shot, slow push in", chars=["tangxiaotang", "xuyan"], nospeak=["tangxiaotang"], night="boat",
         comp=boat_back(f"her hands resting low in her lap; {XU_FACING}, {XU_N}, {UNDER}, framed from the chest up with clear space above his head, {WET}, his face three-quarter to screen right toward her, never the lens; listening hard: brows drawn, lips pressed shut; behind him only the thick grey fog, soft; {HANDS}; exactly two people, the young woman in the foreground seen only from behind"),
         lines=[("tangxiaotang", "我回魏家，他就不碰許家，你們就安全了。", "很小聲")],
         motion=f"the young woman's head lowers a little and her shoulders tremble once; {HEADSTILL}; {quiet('Xu Yan')}; his jaw tightens as he listens",
         zh="過肩中景、慢推（送霧色底圖）：前景右唐小棠的背影頭低一點、肩膀抖一下，很小聲地說（nospeak）；畫左許硯看著她、嘴閉著、下巴一繃。稿子『解下算盤放在膝上、勉強笑、掉淚』：算盤只在插鏡（拍法 20），解算盤交給音效；笑與淚從背後看不到"),
    dict(loc="boat_t", cam="Insert close-up, slow push in", chars=[], night="boat_t",
         comp=f"insert close-up, the shot opens directly on {ABACUS}, seated, resting on a pleated peach-pink silk skirt over her lap from its very first frame, two small fingertips in peach-pink silk sleeve cuffs already on its beads; only the fingertips, their sleeve cuffs, the abacus and the skirt are in the frame",
         motion=NOBODY_ABACUS + "the fingertips push the beads back one by one until every rod is cleared, and one small tear drops onto the gold frame and runs along it",
         zh="插鏡、慢推（第一格就是算盤：坐著、膝上桃粉百褶裙上平放的長金算盤（跟前臂一樣長；協調者更正，道具圖本身就是長的）；送道具圖 `prop-jinsuanpan-l1`，不寫『set layout stays』，第 22 集必改 11）：指尖把算珠一顆一顆撥回去歸零，一滴淚落在算盤框上（無台詞）"),
    dict(loc="boat_c", cam="Close-up, slow push in", chars=["xuyan"], night="boat",
         comp=f"close-up of {XU_N}, {UNDER}, framed from the chest up with space above his head, {WET}, his right arm already reaching down toward the lower right edge of the frame from the first frame, his face three-quarter to screen right toward Tang Xiaotang off screen right, never the lens; one side of his face lit warm by the far bow lantern, the other side in cold shadow; grave and certain: steady eyes, lips moving slowly between words; behind him the thick grey fog, soft",
         lines=[("xuyan", "妳不是我贏來的，也不是誰拿來抵的債。", "一字一字，冷得聲音帶抖")],
         motion="Xu Yan's right hand comes down beyond the lower right edge and rests there, covering her hand, as he speaks word by word; after the last word he keeps his hand there and holds her gaze",
         zh="近景、慢推（送霧色底圖；沒有月光，只有船頭燈的一點暖光照在半邊臉）：許硯右手往畫面右下緣外伸、按住她撥算珠的手（手出畫，算盤不入鏡），一字一字地說"),
    # The script's long shot (c13, 9 s: the system's two lines and his thought) is split at the natural break, one change of
    # face each (e022 s35/s35b): s13 the system (the panel), s13b, closer, his thought. Rule 11: no blue light written.
    dict(loc="boat_c", cam="Close-up, slow push in", chars=["xuyan"], night="boat",
         comp=f"close-up of {XU_N}, {UNDER}, framed from the chest up with space above his head, {WET}, his right hand at the lower right edge of the frame resting on a small hand in a peach-pink silk sleeve cuff, his face three-quarter to screen right toward her off screen right, never the lens; quiet and tender: soft eyes, lips pressed shut; behind him the thick grey fog, soft",
         lines=[("xitong", "叮。唐小棠，好感加六。", "冷，宣布"),
                ("xitong", "宿主泡在冰水裡說的話，倒是比平常值錢。", "冷")],
         panel=[("唐小棠 好感 +6 → 30", "affection")],
         motion=f"Xu Yan's fingers press the small hand once, gently, and stay there; then one corner of his mouth twitches; {SILENT_HE}; he is listening, not speaking",
         zh="近景、慢推（稿子 c13 的長鏡在系統兩句之後拆開；送霧色底圖；拍法 11 不寫藍光，面板由剪接疊上）：許硯的手還按在畫右下緣她的袖口上，輕輕捏一下；聽完系統吐槽嘴角抽一下；全程嘴閉著"),
    dict(sid="s13b", loc="boat_c", cam="Close-up, slow push in", chars=["xuyan"], night="boat",
         comp=f"tight close-up of {XU_N}, {UNDER}, framed from the shoulders up with a little space above his head, his wet black hair stuck to his forehead, his face three-quarter to screen right toward her off screen right, never the lens; wry and warm: one brow lifting, the corner of his mouth tucked in, lips pressed shut, his breath white; behind him the thick grey fog, soft",
         lines=[("xuyan", "值錢就好，這身衣服也算沒白濕。", "心裡話，錄得近、輕", "inner")],
         motion=f"Xu Yan breathes out once through his nose, a small white breath, and his eyes soften on her; {SILENT_HE}; he is thinking, not speaking",
         zh="近景（比 s13 再近，肩以上）、慢推（送霧色底圖）：許硯鼻子呼一口白氣、眼神軟下來；全程嘴閉著（心裡話畫外）"),
    dict(loc="boat_c", cam="Over-the-shoulder close shot, slow push in", chars=["tangxiaotang", "xuyan"], nospeak=["tangxiaotang"], night="boat",
         comp=boat_back(f"{XU_FACING}, {XU_N}, {UNDER}, framed from the chest up with clear space above his head, {WET}, his face three-quarter to screen right toward her, never the lens; waiting, gentle: eyes on her, lips pressed shut; behind him only the thick grey fog, soft; {HANDS}; exactly two people, the young woman in the foreground seen only from behind", shot="over-the-shoulder close shot", frame="framed from the shoulders up, the back of her head and her right shoulder filling the right third of the frame"),
         lines=[("tangxiaotang", "好，我說實話。宰相扣了唐家八條鹽船。", "咬牙")],
         motion=f"the young woman lifts her right hand and wipes her cheek once with the back of it, then straightens her back; {HEADSTILL}; she faces Xu Yan the whole shot; {quiet('Xu Yan')}; his brows draw together",
         zh="過肩近景、慢推（審稿建議 3：換景別，她的後腦與右肩占畫右三分之一；送霧色底圖）：前景右唐小棠的背影用手背抹一下臉頰、坐直、咬牙說（nospeak）；畫左許硯看著她、嘴閉著、眉頭一緊。稿子『兩手握緊膝上的算盤』不寫（拍法 20）"),
    dict(loc="boat_t", cam="Insert close-up, slow push in", chars=[], night="boat_t",
         comp=f"insert close-up, the shot opens directly on {ABACUS}, seated, resting on a pleated peach-pink silk skirt over her lap from its very first frame, one small fingertip in a peach-pink silk sleeve cuff already on the first bead; only the fingertip, its sleeve cuff, the abacus and the skirt are in the frame",
         lines=[("tangxiaotang", "船放不放，看我爹肯不肯，把我指給魏家。", "畫外，壓著哭")],
         motion=NOBODY_ABACUS + "the fingertip pushes eight beads up one at a time, each one knocking against the crossbar, and stops on the eighth",
         zh="插鏡、慢推（第一格就是算盤；送道具圖）：指尖一顆、一顆推上八顆算珠，每一顆都撞到橫樑；唐小棠的台詞畫外"),
    dict(loc="boat_c", cam="Close-up, slow push in", chars=["xuyan"], night="boat",
         comp=f"close-up of {XU_N}, {UNDER}, framed from the chest up with space above his head, {WET}, his face three-quarter to screen right toward Tang Xiaotang off screen right, never the lens; dawning understanding: brows drawn tight, eyes narrowing, lips moving slowly between words; behind him only the thick grey fog, soft",
         lines=[("xuyan", "所以妳逃婚。那名冊上的林二丫，又是怎麼回事？", "慢慢地，冷得聲音帶抖")],
         motion="Xu Yan's brows tighten and he slowly sits up straight as he speaks; after the last word he holds her gaze, waiting",
         zh="近景、慢推（送霧色底圖；身後只有霧）：許硯眉頭一緊、慢慢坐直，慢慢地問"),
    dict(loc="boat_c", cam="Medium shot from behind, slow push in", chars=["tangxiaotang"], nospeak=["tangxiaotang"], night="boat",
         comp=f"medium shot from close behind {TBACK}, sitting on the boards at the right side of the boat, framed from the waist up, facing straight away from us toward the dark water beyond the far edge of the boat, her hands resting low in her lap; {only_tang()}; beyond her only the low wooden edge of the boat, the flat dark water and the thick grey fog",
         lines=[("tangxiaotang", "媒婆說，林二丫病死了，名冊上的名額還空著。", "小聲")],
         motion=f"{HEADSTILL}; she sits very still looking out at the water, her shoulders drawn in; the fog drifts slowly past over the water",
         zh="中景（從背後）、慢推（送霧色底圖）：唐小棠的背影坐在船右邊、正背對鏡頭朝船另一側外黑黑的水看（審稿必改 3：不寫『朝右』，從背後拍朝右會露耳朵與臉頰），肩膀縮著，小聲說（nospeak）。稿子『拉下一截緞帶絞在手指上』不拍（從背後拉緞帶會亂了髮型，參考圖壓過文字）"),
    dict(loc="boat_c", cam="Over-the-shoulder medium shot, slow push in", chars=["tangxiaotang", "xuyan"], nospeak=["tangxiaotang"], night="boat",
         comp=boat_back(f"her hands resting low in her lap; {XU_FACING}, {XU_N}, {UNDER}, framed from the chest up with clear space above his head, {WET}, his face three-quarter to screen right toward her, never the lens; stunned: eyes wide, brows up, lips pressed together and still; behind him only the thick grey fog, soft; {HANDS}; exactly two people, the young woman in the foreground seen only from behind"),
         lines=[("tangxiaotang", "我拿一支金釵跟媒婆換的，頂了她的名字。", "心虛又倔")],
         motion=f"the young woman lifts her chin and squares her shoulders, waiting to be scolded; {HEADSTILL}; she faces Xu Yan the whole shot; {quiet('Xu Yan')}; he stares at her, unmoving",
         zh="過肩中景、慢推（送霧色底圖）：前景右唐小棠的背影下巴一抬、肩膀擺正，等他罵（nospeak）；畫左許硯愣住看她、眉毛一抬、嘴閉著不動（審稿必改 7：拿掉『嘴微張』，免得對嘴）"),
    # ---- first light (set-chuan-chen-l1 from here; bible rule 23). He may laugh (script c19); her silent face (blush).
    dict(loc="dawn", cam="Medium wide shot, slow push in", chars=["xuyan", "tangxiaotang"], night="dawn",
         comp=f"medium wide shot under the canopy from the stern end of the boat: on the left {XU_N}, sitting on the boards, framed from the waist up, {HALFDRY}, already turned toward her from the first frame, his face three-quarter to screen right, never the lens; caught out and amused: eyes wide, the corners of his mouth slowly curling up, lips moving between words; on the right, an arm's length from him, Tang Xiaotang, {TANG}, sitting with her knees drawn up, framed from the waist up, her face three-quarter to screen left toward him, never the lens; caught: cheeks flushing pink, eyes lowered and still a little red-rimmed, lips pressed shut; beyond the bow on the right the pale mist thinning in the first light; {HANDS}; exactly two people",
         lines=[("xuyan", "所以妳是自己花錢，嫁到我家來受苦的？", "愣住，忍不住笑")],
         motion=f"Xu Yan's mouth curls into a slow grin as he speaks; {quiet('Tang Xiaotang', 'her')}; her cheeks flush and her eyes drop to her knees",
         zh="中全景、慢推（從船尾拍竹篷下；送天亮的小船圖 `set-chuan-chen-l1`）：左邊許硯（衣服半乾）第一格已經轉向她，愣住、嘴角慢慢翹起來，忍不住笑著說（本鏡可以笑）；右邊唐小棠（**不說話的臉**：只送 l1 與 angle-a；臉頰紅起來、垂眼、眼眶還有點紅、嘴閉著；淚痕不寫，拍法 12 皮膚上不寫細小東西）。稿子的全景（船夫倚篙）改中全景，船夫不入鏡"),
    dict(loc="dawn_c", cam="Over-the-shoulder medium shot, slow push in", chars=["tangxiaotang", "xuyan"], nospeak=["tangxiaotang"], night="dawn",
         comp=boat_back(f"her right hand already raised beside her shoulder from the first frame; {XU_FACING}, {XU_N}, {UNDER}, framed from the waist up with clear space above his head, {HALFDRY}, his face three-quarter to screen right toward her, never the lens; grinning helplessly: eyes creased, lips pressed together in a smile; behind him the thin pale mist lit warm, soft; {HANDS}; exactly two people, the young woman in the foreground seen only from behind"),
         lines=[("tangxiaotang", "要你管！我算過，躲進名冊，比躲在哪裡都安全。", "又哭又笑")],
         motion=f"the young woman slaps Xu Yan's upper arm once with her open hand; {HEADSTILL}; {quiet('Xu Yan')}; he rubs his arm with his other hand, still smiling",
         zh="過肩中景、慢推（送天亮的薄霧底圖 `set-chuan-chen-wu-l1`；買 8 秒，審稿必改 6）：前景右唐小棠的背影一巴掌拍在許硯手臂上、又哭又笑地說（nospeak，哭笑從背後看不到，交給錄音）；畫左許硯揉著手臂、嘴閉著笑"),
    dict(loc="dawn", cam="Wide shot, slow pull back", chars=[], night="dawn",
         comp=f"wide shot from low over the water: {BOATD_DAWN.replace('one small', 'the one small')}, small in the middle of the frame on the wide calm river; under the canopy two small figures sitting side by side: {SMALL_XU}, on the left, and {SMALL_TANG.replace('sitting hunched under the canopy with her arms around her knees, her back to us', 'sitting close beside him')}; her small peach-pink figure is the only spot of pink anywhere in the picture, sitting close at his right side under the canopy; at the bow {BOATMAN}, standing, both hands on one long bamboo pole; the morning mist breaking up into long bands lit gold by the low sun on the right; exactly three people, all small in the frame",
         lines=[("xuyan", "躲進名冊最安全……現在名冊，反倒成了他的把柄。", "心裡話，錄得近、輕", "inner")],
         motion=NOBODY + "the boatman pushes the pole down once and the boat glides slowly downstream to the right; the two small figures sit still side by side; the mist bands drift and glow",
         zh="全景、慢慢拉遠（稿子的『慢慢升高』gen-dh 沒有對應的運鏡句，改慢拉遠；日出，晨霧散成一條條金帶；送天亮的小船圖）：河中間的小船很小，竹篷下兩個小人並肩坐著（灰外衣的許硯、桃粉雙丸子的唐小棠，都不點名、不送圖、寫髮型；審稿建議 4：寫她是畫面上唯一的桃粉色），船頭船夫撐一篙、船往下游滑；許硯心裡話畫外。稿子『許硯低頭看濕袖、抬眼看她』在全景看不出來，不寫"),
    dict(loc="dawn_c", cam="Low-angle medium shot from behind, slow push in", chars=["tangxiaotang"], nospeak=["tangxiaotang"], night="dawn",
         comp=f"low-angle medium shot from the height of the boards, from close behind {TBACK}, sitting forward at the bow on the right, framed from the waist up, facing straight away from us, downstream, the bright glittering water ahead of her filling the frame; {only_tang()}; beyond the water only the thin mist lit warm gold by the low sun",
         lines=[("tangxiaotang", "哭夠了。這門親，我自己去跟他賭掉。", "擦乾淚，眼神亮了")],
         motion=f"the young woman wipes her cheek once with the back of her right hand and sits up straight, squaring her shoulders; {HEADSTILL}; the light on the water glitters",
         zh="低角度中景（從船板高度、從背後）、慢推（送薄霧底圖）：唐小棠已經挪到船頭，背影正背對鏡頭朝下游（審稿必改 3）、手背一抹把淚擦掉、坐直（nospeak）；前方發亮的水面。稿子的近景（睫毛照成金色）是正面說話，改背影；『拿起算盤一撥』不寫（拍法 20），算珠響成一串交給音效"),
    dict(loc="dawn_c", cam="Close-up, slow push in", chars=["xuyan"], night="dawn",
         comp=f"close-up of {XU_N}, {UNDER}, framed from the chest up with space above his head, {HALFDRY}, his face three-quarter to screen right toward Tang Xiaotang off screen right at the bow, never the lens; one brow raised, curious and doubtful: lips moving between words; warm low morning light on his face from the right; behind him the thin pale mist, soft",
         lines=[("xuyan", "賭？妳一個人，拿什麼跟宰相府賭？", "挑眉")],
         motion="Xu Yan raises one brow and shifts a little forward toward her as he speaks; after the last word he waits, his head tilted",
         zh="近景、慢推（送薄霧底圖）：許硯挑眉，往船頭挪近一點，問畫右船頭的唐小棠（畫外）"),
    dict(loc="dawn_c", cam="Low-angle over-the-shoulder medium shot, slow push in", chars=["tangxiaotang", "xuyan"], nospeak=["tangxiaotang"], night="dawn",
         comp=boat_back(f"her hands resting low in her lap; {XU_FACING}, {XU_N}, sitting a little closer on the boards, {RIB}, framed from the waist up with clear space above his head, {HALFDRY}, his face three-quarter to screen right toward her, never the lens; listening, surprised: brows up, lips pressed shut; warm low light on his face; behind him the thin pale mist, soft; {HANDS}; exactly two people, the young woman in the foreground seen only from behind", pose="sitting at the bow", shot="low-angle over-the-shoulder medium shot from the height of the boards,"),
         lines=[("tangxiaotang", "拿許記。跟他的魏記鬥三十天，比誰賺得多。", "精明")],
         motion=f"the young woman lifts her head and tilts it a little to one side, sure of herself; {HEADSTILL}; she faces Xu Yan the whole shot; {quiet('Xu Yan')}; his brows rise higher",
         zh="低角度過肩中景（從船板高度往上；審稿建議 3 換景別）、慢推（送薄霧底圖）：前景右唐小棠的背影抬起頭、頭一偏、精明地說（nospeak）；畫左許硯挑眉、嘴閉著。稿子『兩手捧算盤、啪啪撥兩下』不寫（拍法 20），算珠聲交給音效"),
    dict(loc="dawn_t", cam="Insert close-up, slow push in", chars=[], night="dawn_t",
         comp=f"insert close-up, the shot opens directly on {ABACUS}, seated, resting on a pleated peach-pink silk skirt over her lap in warm morning light from its very first frame, one small fingertip in a peach-pink silk sleeve cuff already on a bead; only the fingertip, its sleeve cuff, the abacus and the skirt are in the frame",
         lines=[("tangxiaotang", "許記贏，他撤婚書，冒名的事永遠不准再提。", "畫外，一條一條算")],
         motion=NOBODY_ABACUS + "the fingertip pushes one bead up, then two more quickly one after the other, each one knocking against the crossbar",
         zh="插鏡、慢推（第一格就是算盤，晨光；送道具圖）：指尖先撥上一顆、再連撥兩顆，喀喀作響；唐小棠的台詞畫外"),
    dict(loc="dawn_c", cam="Close-up, slow push in", chars=["xuyan"], night="dawn",
         comp=f"close-up of {XU_N}, {UNDER}, framed from the chest up with space above his head, {HALFDRY}, his face three-quarter to screen right toward Tang Xiaotang off screen right at the bow, never the lens; the smile gone, worried: brows knitted, eyes hard on her, lips moving between words; warm low morning light on his face; behind him the thin pale mist, soft",
         lines=[("xuyan", "那要是輸了呢？輸了，妳怎麼辦？", "笑容收起")],
         motion="Xu Yan frowns and leans forward toward her as he speaks; after the last word he holds still, waiting for her answer",
         zh="近景、慢推（送薄霧底圖）：許硯笑容收起、眉頭一皺、往前探身問（原版建議：不笑）"),
    dict(loc="dawn_c", cam="Medium shot from behind, slow push in", chars=["tangxiaotang"], nospeak=["tangxiaotang"], night="dawn",
         comp=f"medium shot from close behind {TBACK}, sitting forward at the bow, framed from the waist up, facing straight away from us, downstream; {only_tang()}; beyond her on the right at the very prow one boatman in a conical bamboo hat and a straw rain cape, standing with his back to us, his wide hat brim hiding his face, both hands on one long bamboo pole; ahead of them the wide bright river glittering under the low sun and the thinning gold mist; {HANDS}; exactly two people, both seen only from behind",
         lines=[("tangxiaotang", "輸了，我跟他回京。船家，縣城碼頭靠岸。", "不眨眼")],
         motion=f"{HEADSTILL}; she sits straight and still, turned away from us the whole shot; the boatman nods his hat once and leans on the pole, and the boat slides on toward the bright water",
         zh="中景（從背後）、慢推（送薄霧底圖）：唐小棠的背影坐在船頭、朝前方下游（縣城）發亮的河面，朝船夫說（nospeak）；船頭最前面的船夫（背對鏡頭、寬帽沿遮臉；審稿必改 3：不寫側身）點一下斗笠、撐篙。稿子『把算盤掛回腰間』不寫（拍法 20），交給音效；『從船頭搖向河面』不寫（一鏡一個運鏡）（結尾）"),
    # ---- scene 3: the county inn in the afternoon (set-kezhan-pm-l1; as e022 the window and bench left, the door right).
    dict(chapter="客棧", loc="inn", cam="Medium shot, tracking shot that follows the subject", chars=["weishaoqing", "tangxiaotang"], nospeak=["tangxiaotang"], night="inn",
         comp=f"medium shot from just inside the open double door, the dark wooden door frame in the soft right foreground: on the left {WEI}, sitting on {BENCH}, framed from the knees up, {FAN}, already sitting up straight from the first frame, his face three-quarter to screen right toward the door, never the lens; surprised and amused: brows up, a slow smile, lips moving between words; walking into the room toward the right side of {TABLE_INN}, her back to us, {TBACK}; {only_tang()}; one step behind her on the right and half hidden by her, his back to us, {SMALL_XU}, {DRY}; the young man keeps his head still, the back of his head toward us the whole shot; behind them, {ELDERS.replace('standing together by the folding screen at the back, soft and out of focus, seen side-on', 'standing together just inside the door at the right edge, soft and out of focus, their backs to us')}; {HANDS}",
         lines=[("weishaoqing", "三日還沒到，妳就來了？怎麼還帶了一串人？", "意外，笑")],
         motion="Wei Shaoqing taps the closed fan once against his knee as he speaks, smiling; the young woman and the young man walk on toward the table, and the three old men stay by the door, all with their backs to us",
         zh="中景、跟拍（前景右是房門門框；送午後的客棧圖 `set-kezhan-pm-l1`）：左邊魏少卿第一格已經在窗下長凳上坐直，摺扇合著在膝上敲一下，意外地笑著說（本鏡可以笑；扇子一直合著，第 21 集 fix1：打開的扇面會長出假字）；唐小棠的背影、身後一步、被她擋住一半的許硯背影（衣襬皺、褲腳一圈泥，不送圖；審稿必改 8：頭不動、後腦一直朝鏡頭）；三位老人（灰、褐、深藍綢袍、黑方巾）第一格已經站在門內畫右邊緣、背對鏡頭、虛焦、不動（不拍一個接一個走進門：畫面上動的人太多會分身）"),
    dict(loc="inn", cam="Over-the-shoulder medium shot, slow push in", chars=["tangxiaotang", "xuyan", "weishaoqing"], nospeak=["tangxiaotang"], night="inn",
         comp=inn_back(f"her right hand already flat on {WAGER} on the table top from the first frame; standing close at her right shoulder, on the right edge of the frame, {XU_N}, {DRY}, framed from the waist up, his face three-quarter to screen left toward Wei Shaoqing, never the lens; tense: jaw set, lips pressed shut; facing us beyond the table a little left of the middle {WEI}, sitting on {BENCH}, framed from the waist up with clear space above his head, {FAN}, his face three-quarter to screen right looking up at her, never the lens; curious: one brow up, lips closed; far behind by the folding screen three thin old men in long silk robes, standing side-on to us and turned toward Wei Shaoqing, their faces in profile, soft and out of focus; {HANDS}"),
         lines=[("tangxiaotang", "我請了商會三位老人，來替我們的賭約作證。", "冷靜")],
         motion=f"the young woman slaps the folded paper down flat on the table and leaves her hand on it; {HEADSTILL}; she looks straight ahead at Wei Shaoqing the whole shot; {quiet('Wei Shaoqing')}; {quiet('Xu Yan')}; Wei Shaoqing glances at the paper",
         zh="過肩中景、慢推（送午後客棧圖）：前景右唐小棠的背影把摺好的紙（賭約，素面朝上、不見字；拍法 27）拍在桌上（nospeak）；她右肩後是許硯（衣襬皺、褲腳有泥、嘴閉著）；桌對面魏少卿坐在長凳、看紙、嘴閉著；後面屏風邊三位老人虛焦、側身朝魏少卿、臉是側面（拍法 25 不給正臉；審稿必改 9 寫明朝向）；賭約寫成厚而光滑的米色紙、對摺、空白的外面朝上（審稿必改 11）。稿子是正面拍她，照拍法 3 改背後；『從袖裡拿出』不拍，第一格紙已經在手下"),
    # He may laugh (rule 30).
    dict(loc="inn_c", cam="Low-angle close-up, slow push in", chars=["weishaoqing"], night="inn",
         comp=f"low-angle close-up from the height of the table top, {WEI}, sitting on the bench under the window, framed from the chest up with space above his head, {FAN}, his face three-quarter to screen right toward Tang Xiaotang off screen right, never the lens; mocking: eyes narrowed, a laugh starting, lips moving lazily between words; behind him the bright window and the grey roof tiles, soft",
         lines=[("weishaoqing", "賭約？妳拿什麼跟我賭，拿妳自己？", "拖長音")],
         motion="Wei Shaoqing glances down at the plain folded paper on the table, then lifts his eyes to her and laughs as he speaks, tapping the closed fan twice on his knee",
         zh="低角度近景（桌面高度往上拍）、慢推（不送場景圖）：魏少卿低頭看一眼桌上的紙、抬眼笑出聲、合著的摺扇在膝上敲兩下，拖長音地說（本鏡可以笑）。稿子『扇尖挑開紙角、搧兩下』不寫（扇子一直合著；紙不打開）"),
    dict(loc="inn", cam="Over-the-shoulder medium shot, slow push in", chars=["tangxiaotang", "xuyan", "weishaoqing"], nospeak=["tangxiaotang"], night="inn",
         comp=inn_back(f"both her hands already flat on the table top on either side of {WAGER} from the first frame, leaning forward over the table; standing close at her right shoulder, on the right edge of the frame, {XU_N}, {DRY}, framed from the waist up, his face three-quarter to screen left toward Wei Shaoqing, never the lens; tense: jaw set, lips pressed shut; facing us beyond the table a little left of the middle {WEI}, sitting on {BENCH}, framed from the waist up with clear space above his head, {FAN}, his face three-quarter to screen right looking up at her, never the lens; amused, weighing her: eyes narrowed, lips closed; behind him the bright window, soft; {HANDS}; exactly three people: the young woman seen only from behind, Xu Yan at her shoulder and Wei Shaoqing beyond the table"),
         lines=[("tangxiaotang", "對，拿我自己。許記跟魏記鬥商三十日，比營收。", "一字一字")],
         motion=f"the young woman leans further forward over the table on her two hands; {HEADSTILL}; she looks straight ahead at Wei Shaoqing the whole shot; {quiet('Wei Shaoqing')}; {quiet('Xu Yan')}; his smile thins",
         zh="過肩中景、慢推（送午後客棧圖）：前景右唐小棠的背影兩手撐在桌上往前傾，一字一字地說（nospeak）；她右肩後畫右邊緣是許硯（跟 s29 同一個機位；審稿必改 10：他不能中間消失，送他的 l1 與 angle-a，嘴閉著）；桌對面魏少卿瞇眼、嘴閉著、笑意收薄"),
    dict(loc="inn_c", cam="Medium close-up, slow push in", chars=["weishaoqing"], night="inn",
         comp=f"medium close-up of {WEI}, sitting on the bench under the window, framed from the chest up with space above his head, {FAN.replace('held upright in his right hand', 'held upright in his right hand just below his chin')}, his face three-quarter to screen right toward Tang Xiaotang off screen right, never the lens; unhurried and sly: eyes narrowing, a thin smile, lips moving slowly between words; behind him the bright window, soft",
         lines=[("weishaoqing", "我贏了呢？三日後的州府，還去不去？", "慢條斯理")],
         motion="Wei Shaoqing lowers the closed fan and taps it once on the table top in front of him as he speaks; after the last word he narrows his eyes at her",
         zh="中近景、慢推（不送場景圖）：魏少卿合著的摺扇豎在下巴下（不抵唇，免得擋嘴），在桌面輕敲一下，桃花眼瞇起、慢條斯理地問（本鏡可以笑）"),
    dict(loc="inn_c", cam="Over-the-shoulder close shot, slow push in", chars=["tangxiaotang", "weishaoqing"], nospeak=["tangxiaotang"], night="inn",
         comp=f"close over-the-shoulder shot from close behind {TBACK}, standing at the right side of the table in the right foreground, framed from the shoulders up; {only_tang('right')}; facing us beyond her shoulder, soft, {WEI}, sitting on the bench under the window, framed from the chest up, {FAN}, his face three-quarter to screen right toward her, never the lens; testing her: eyes narrowed, lips closed; {HANDS}; exactly two people, the young woman in the foreground seen only from behind",
         lines=[("tangxiaotang", "你贏了，我自己跟你回京，不用州府來拿。", "不眨眼")],
         motion=f"{HEADSTILL}; her shoulders stay square and still the whole shot, facing him; {quiet('Wei Shaoqing')}; his eyes widen a little, then narrow again",
         zh="過肩近景、慢推（不送場景圖）：前景右唐小棠的背影（肩以上）肩膀擺正不動（『不眨眼、嘴抿緊又張開』從背後看不到）（nospeak）；虛焦的魏少卿眼睛一睜又瞇回去、嘴閉著"),
    dict(loc="inn_c", cam="Close-up, slow push in", chars=["xuyan"], night="inn",
         comp=f"close-up of {XU_N}, standing close behind her right shoulder, framed from the chest up with space above his head, his face three-quarter to screen left toward her, never the lens; urgent, not smiling: brows drawn hard, lips moving fast and low between words; at the left edge of the frame, soft and cut off, the back of a young woman's head with two round buns set high, a short pink silk ribbon around each, appearing only once; behind him the dark wooden wall, soft",
         lines=[("xuyan", "小棠，三十天，魏記背後是整個宰相府。", "急，壓低聲音")],
         motion="Xu Yan turns his head sharply toward her and reaches his right hand out toward her arm as he speaks, low and fast; after the last word his hand stays reaching",
         zh="近景、慢推（不送場景圖）：許硯站在唐小棠肩後，猛地轉頭看她、伸手要拉她手臂，急、壓低聲音說，不笑（原版建議）；畫左緣虛焦是她的兩顆丸子（不點名、不送圖）"),
    dict(loc="inn_t", cam="Insert close-up, slow push in", chars=[], night="inn_t",
         comp="insert close-up, the shot opens directly on a small hand in a thick opaque peach-pink silk sleeve cuff already resting on a man's wrist in a faded blue-grey sleeve cuff at the edge of the dark-red wooden table top from its very first frame; only the two hands, their sleeve cuffs and the table edge are in the frame",
         lines=[("tangxiaotang", "我算過了。肥皂和白紙，他們做不出來。", "畫外，很輕")],
         motion=NOBODY + "the small hand presses down gently, the man's hand stops and slowly opens and relaxes, and the small hand stays on his wrist",
         zh="插鏡、慢推（第一格就是兩隻手；送午後客棧桌面的免費裁切 `set-kezhan-pm-table-l1`）：唐小棠的手（桃粉不透的織錦袖口）按住許硯的手腕（藍灰袖口）輕輕往下壓，他的手停住、慢慢鬆開；她的台詞畫外"),
    dict(loc="inn", cam="Over-the-shoulder medium shot, slow push in", chars=["tangxiaotang", "xuyan", "weishaoqing"], nospeak=["tangxiaotang"], night="inn",
         comp=inn_back(f"her right hand already flat on {WAGER} on the table top from the first frame; standing close at her right shoulder, on the right edge of the frame, {XU_N}, {DRY}, framed from the waist up, his face three-quarter to screen left toward Wei Shaoqing, never the lens; tense: jaw set, lips pressed shut; facing us beyond the table a little left of the middle {WEI}, sitting on {BENCH}, framed from the waist up with clear space above his head, {FAN}, his face three-quarter to screen right toward her, never the lens; cool and attentive: eyes on the paper, lips closed; behind him the bright window, soft; {HANDS}; exactly three people: the young woman seen only from behind, Xu Yan at her shoulder and Wei Shaoqing beyond the table"),
         lines=[("tangxiaotang", "許記贏了，你撤婚書，冒名的事一筆勾銷，州府也別去了。", "乾脆")],
         motion=f"the young woman slides the folded paper across the table toward him with the flat of her open hand; {HEADSTILL}; she looks straight ahead at Wei Shaoqing the whole shot; {quiet('Wei Shaoqing')}; {quiet('Xu Yan')}; his eyes follow the paper",
         zh="過肩中景、慢推（送午後客棧圖）：前景右唐小棠的背影用張開的手掌把紙往魏少卿那邊推（稿子『一根手指』改手掌：第 16 集單根手指會被讀成比中指）（nospeak）；她右肩後畫右邊緣是許硯（審稿必改 10，嘴閉著）；魏少卿看著紙、嘴閉著。稿子是正面拍她、前景是他的肩，照拍法 3 改從她背後"),
    dict(loc="inn", cam="Wide shot, slow push in", chars=["weishaoqing", "tangxiaotang", "xuyan"], night="inn",
         comp=f"wide shot across the room, {WAGER}, lying soft and out of focus on the near edge of {TABLE_INN} at the very bottom edge of the frame: on the left {WEI}, already standing up beside {BENCH} from the first frame, framed full figure, {FAN}, his face three-quarter to screen right, never the lens; pleased with himself: a wide smile, lips moving between words; on the right, standing side by side at the right side of the table, Tang Xiaotang, {TANG}, framed full figure, her face in profile to screen left toward him, never the lens; composed: lips pressed shut, eyes steady; and close at her right shoulder {XU_N}, {DRY}, framed full figure, his face three-quarter to screen left, never the lens; uneasy: jaw tight, lips pressed shut; at the back by the folding screen, {ELDERS}; {HANDS}",
         lines=[("weishaoqing", "好。三位老人家，聽清楚了，替本公子作個證。", "笑")],
         motion=f"Wei Shaoqing points the closed fan toward the three old men as he speaks, and the three old men glance at one another and nod together once; {quiet('Tang Xiaotang', 'her')}; {quiet('Xu Yan')}",
         zh="全景、慢推（前景是桌上的賭約，在畫面最下緣、虛焦，厚而光滑的米色紙、空白外面朝上：審稿必改 11；送午後客棧圖）：左邊魏少卿第一格已經站在長凳旁（站起來的那一下交給 s36→s37 的剪接與椅子音效），用合著的摺扇指向三位老人，笑著說（本鏡可以笑）；三位老人在後面屏風邊互看一眼、一齊點頭（虛焦、側面，不給正臉、不送圖）；右邊唐小棠（不說話的臉，l1 與 angle-a）與許硯並肩站在桌邊、嘴閉著（三張臉：拍法 1）"),
    dict(loc="inn_c", cam="Medium close-up, slow push in", chars=["weishaoqing"], night="inn",
         comp=f"medium close-up of {WEI}, standing and leaning forward over the table toward Tang Xiaotang off screen right, framed from the chest up with space above his head, {FAN} held beside his cheek, his face three-quarter to screen right, close to her, never the lens; a smile with an edge: eyes cold, one corner of his mouth curled, lips moving slowly between words; behind him the bright window and the folding screen, soft",
         lines=[("weishaoqing", "三十天後，我帶著花轎來接新娘。", "湊近，笑裡帶刀")],
         motion="Wei Shaoqing smiles slowly and coldly as he speaks; after the last word he lowers the closed fan and straightens up to his full height",
         zh="中近景、慢推（不送場景圖）：魏少卿隔著桌子往畫右的唐小棠（畫外）探身，合著的摺扇豎在臉旁（稿子『摺扇搖開在臉旁、一收』改成一直合著），慢慢冷笑著說，說完扇子放下、挺直身子（本鏡可以笑）"),
    dict(loc="inn_t", cam="Insert close-up, slow push in", chars=[], night="inn_t",
         comp=f"insert close-up, the shot opens directly on a man's left hand in a wide sapphire-blue brocade sleeve woven with gold thread, its thumb already red with paste, held just above one sheet of plain paper lying flat on the dark-red wooden table top with its plain blank side up, {PASTE} beside it, from its very first frame; only the hand, its sleeve cuff, the paper, the dish and the table top are in the frame",
         motion=NOBODY + "the thumb presses down hard onto the middle of the paper and holds there",
         zh="插鏡、慢推（第一格就是沾了印泥的拇指；送午後客棧桌面裁切）：魏少卿的左手（寶藍織金袖口）把拇指重重按在紙上（紙素面朝上、字不入鏡；一小碟朱紅印泥在旁；稿子的白玉戒指不寫，定妝照沒有）（無台詞）"),
    dict(loc="inn", cam="Medium shot, slow push in", chars=["tangxiaotang", "xuyan"], night="inn",
         comp=f"medium shot across the table: in the soft lower left foreground a man's left hand in a wide sapphire-blue brocade sleeve woven with gold thread, its thumb pressed down on one sheet of thick smooth cream paper, its blank outside facing up, on the table top from the first frame; across the table, standing side by side at the far side of it, Tang Xiaotang, {TANG}, framed from the waist up, her face three-quarter to screen left toward the man beyond the left edge, never the lens; steady, red-rimmed eyes: lips pressed shut; and on the right beside her {XU_N}, {DRY}, framed from the waist up, his face three-quarter to screen left toward the paper, never the lens; not smiling: eyes widening, his breath held, lips pressed shut; soft at the back on the left, {ELDERS}; {HANDS}",
         lines=[("xitong", "叮。強制任務：鬥商三十日，勝出。", "冷，宣布"),
                ("xitong", "失敗：唐小棠好感歸零。", "一頓，冷")],
         panel=[("強制任務：鬥商三十日，勝出", "penalty"), ("失敗：唐小棠好感歸零", "penalty")],
         motion=f"the thumb lifts from the paper and leaves one small round red smudge on it; Xu Yan's eyes widen and his jaw slowly tightens; {quiet('Tang Xiaotang', 'her')}; {quiet('Xu Yan')}",
         zh="中景、慢推（隔著桌子；送午後客棧圖）：前景左下虛焦是魏少卿的手（不點名、不送圖），拇指從紙（厚而光滑的米色紙、空白外面朝上，審稿必改 11）上抬起、留下一團圓圓的紅手印（紅印泥，不畫指紋線、不寫字：拍法 27）；對面唐小棠（不說話的臉：眼眶還紅、看著畫左外的魏少卿、嘴閉著）與許硯（眼睛睜大、一口氣停住、下巴慢慢繃緊、嘴閉著）；左後虛焦三位老人。系統兩句畫外、面板紅框由剪接疊上（拍法 11，不寫紅光）（結尾；懸念交給第 24 集）"),
]

HEAD = [
    "- 重製版 r2、真人版（站主 2026-11-11「之後都用真人版」）：照 `docs/videos/zhong-tian-qu-qi-e023-r2/script.md`（c01–c40 對應 s01–s40；c13 拆成 s13、s13b，共 41 鏡；含「這版改了什麼」「2026-11-06 審稿後的修改」與「真人版的改動（2026-11-16）」）；台詞一字不改，只改拍法；每鏡一個看得見的動作、一句一筆不拆半句、預設不笑。篇章設定 `production/r2-bible-e021-e030.md`（拍法 1–30 條）。第 3 篇章〈搶親〉第三集。",
    "- 內部工作編號 923（`hailuo/{ff,clips}-dh-e923.json`、`colab/runs/e923/extras.json`、`colab/runs/e923-live/spec.json`，工作資料夾 `~/mokaair-work/videos/zhong-tian-qu-qi-e923-dh/`）；發布 slug `zhong-tian-qu-qi-e023-r2`。不放集數、不放片名卡；s01 接第 22 集 s41 同一刻（聖經接點 22→23：燈籠已插在岸邊泥裡、他已在水裡往船追）；s40 交給第 24 集第一場（聖經接點 23→24：拇指按在賭約上、商會三老在旁、系統紅框）。",
    "- 照第 22 集審稿後的寫法一開始就照做：`OFFSCREEN_SPEECH = False`；`quiet()` 只管嘴；背景寫在場的東西（拍法 18）；道具與接觸寫在第一格；只寫要畫出來的東西：賭約照拍法 27 寫「一張對摺的白紙」、只見素面；印泥只在 s39；商會三老、船夫不點名、不送圖。",
    "- **唐小棠不露嘴說話**（拍法 3）：她在畫面上的台詞全部從背後拍（s03、s07、s10、s14、s17、s18、s20、s22、s24、s27 船上；s29、s31、s33、s36 客棧；nospeak，spec 拿掉她的圖與身分句；兩顆高丸子、短粉緞帶、後頸露出、頭不動）；她的臉只在**不說話**的 s19（臉紅）、s37（並肩站著）、s40（看著魏少卿），只送 l1 與 angle-a。**小金算盤只在 s11、s15、s25 三支膝上插鏡**（拍法 20 與聖經道具表協調者 2026-11-16 更正：道具圖那把跟前臂一樣長的扁長金算盤、只在插鏡；送道具圖、寫平放）；稿子 c10 解下、c22 拿起、c24 捧著、c27 掛回都不拍，交給音效。",
    "- **魏少卿的摺扇整集合著**（第 21 集 fix1：打開的扇面長出書法假字）：c28 半開、c30 搧兩下、c38 搖開都改成合著敲、豎著。",
    "- **場景圖說了算**（拍法 29，協調者 2026-11-16 決定，每張放大看過）：渡口 `set-dukou-ye-l1`（棧橋從左來、左下乾蘆葦、圖上沒有船）；夜裡的小船 `set-chuan-ye-l1`（竹篷在中、船頭與燈在右：許硯在左、唐小棠在右、船夫在船頭）；天亮 `set-chuan-chen-l1`（燈熄、右邊低日金光）；午後客棧 `set-kezhan-pm-l1`（窗與長凳在左、方桌在中、門在右牆、屏風在後；魏少卿坐長凳，唐小棠在桌子右邊、許硯在她右肩後，三老在屏風邊）。近鏡：夜裡送霧色底圖 `set-chuan-ye-wu-l1`、天亮送薄霧底圖 `set-chuan-chen-wu-l1`（第 21 集挑片：夜戲不送場景圖會長出夜市攤子）；客棧近鏡不送。插鏡：渡口棧橋下 `set-dukou-ye-shui-l1`、客棧午後桌面 `set-kezhan-pm-table-l1`、算盤 `prop-jinsuanpan-l1`。四張新圖都是免費裁切、新 id 自帶 l1。**不需要試鏡**。",
    "- 長鏡要買的秒數（BUY）：照 38 句錄音核過（見 `r2.py` 的 BUY 註解）：**稿子 c13 的長鏡（系統兩句＋心裡話）拆成 s13 與 s13b 兩支 6 秒**；s40（系統兩句約 5.8 秒、本集最後一鏡，要留紅框與重音的尾）與 s20（a18 人聲 5.62 秒，6 秒要整支放慢才裝得下，背影鏡挑片常要剪掉開頭 0.5–1.25 秒；審稿必改 6）買 8 秒；s15、s35 插鏡 5 秒放得下畫外句；其餘 6 秒。重錄 a07、a10、a15、a29、a32、a36、a37（第一次的檔在 `audio/take1/`），a04 重錄較差、留第一次。",
    "- **表上的「秒」欄是 lint 估法**，比錄音短；剪接以錄音長度＋0.5 秒為準。",
    "- **開拍前獨立審稿後**（`writer-tools/e023-r2/review.md`，2026-11-16，協調者照站主授權決定；11 條必改照寫、建議取協調者列的幾條，細節在 `r2.py` 開頭）：夜霧底圖 `set-chuan-ye-wu-l1` 同 id 調暗去飽和、天亮薄霧底圖 `set-chuan-chen-wu-l1` 同 id 調暖；s03–s05 水到大腿、腰或大腿以上取景、船舷在他腰的高度，s05 從她的高度往下拍、地點句寫他在船邊水裡；背影鏡 s07（照圖側面拍）、s17、s22、s27 一律『背對鏡頭』；客棧 s28 許硯頭不動、三老已站在門內，s29 三老側面，s31、s36 許硯回到她右肩後；賭約一律『厚而光滑的米色紙、對摺、空白外面朝上』；s20 買 8 秒；s18 嘴閉著；霧色與薄霧底圖的近鏡不寫竹篷，只寫頭上一根竹骨；s14 過肩近景、s24 低角度過肩；s21 只有她是桃粉色；客棧寫『明亮的冬日午後』。",
]
FOOT = [
    "- **參考圖**（`assets/refs-live/`）：許硯（l1、angle-a；帶笑的 angle-b 整集不送）、唐小棠（l1 交領；只在 s19、s37、s40，l1 與 angle-a）、魏少卿 l1。船夫、商會三老、背影與手都不送圖。場景見上面。",
    "- 共用檔：程式都沒改（說話的人都在 `build-r2.py` 的 `EN`；地方都用 `gen-dh.mjs` 已有的 SET 句；`pilot.py`、`cast.json` 不動；船夫與三老不說話、沒有 `MINOR`）；`refs-live` 加四張免費裁切（新 id）與 README 一段。精修文字的 CG 立領句由本檔結尾的 `live_clips()` 在 build 後從 `clips-dh-e923.json` 拿掉（第 22 集的做法，`gen-dh.mjs` 不動）。",
    "- `colab/runs/e923/extras.json`（照第 22 集）與 `colab/runs/e923-live/spec.json`（`mkspec.py` 產生；種子 9231101／9231102）。",
    "- 免費準備：scratchpad `prep923.sh`（`DRY=1 … st1-ep.sh 923` → `pilot.py` → `retake.py` → `colab-jobs.json` 加 output_path、套 swap_pictures（絕對路徑）→ 逐鏡查送的場景圖與人物圖 → 精修用的分隔句（d1 的『never the mood. 』『One continuous shot.』各一次；clips-dh 的『the set layout stays as it is. 』各一次，三支算盤插鏡用首格那句『keeps the first frame's set layout and props. 』一次）→ `preflight-prompts.py` → 否定名詞與會長字的名詞掃描）。",
    "- 配樂：渡口接第 22 集的二胡長音加鼓點，s06 伸手一個輕重音；船上慢的鋼琴與二胡，s12 輕重音，s22 起轉亮，s27 重音；客棧算盤節奏的緊張 cue，s37「作證」重音、s40 紅框大重音後收。音效見 script.md〈音樂與音效〉（另外：s01 跳水與燈籠插泥、s10 解算盤、s22 算珠一串、s24 撥兩下、s27 算盤掛回腰間、s37 椅子後推，都交給音效）。",
]

# Long shots: seconds to buy. Measured 2026-11-16 against the 38 recordings (~/mokaair-work/videos/zhong-tian-qu-qi-e923-dh/audio;
# wave length and silencedetect -35 dB speech span; e013's test: a shot holds (buy - 0.3) x 1.1 s of speech, half a second
# between lines, so 5 s holds 5.17 s, 6 s 6.27 s, 8 s 8.47 s). faster-whisper medium read every take back, one clip per process,
# numpy input, once plain and once with the previous line and the line as context (audio/fw923.txt, fw923-retake.txt;
# audio/README-retakes.txt).
# Re-recorded once (first takes in audio/take1/): a07 (魏家 heard 回家), a10 (宿主 heard 手作), a15 (媒婆 heard 梅伯),
# a29 (比營收 heard 鼻音收; the retake still does, -ng and tone of the Taiwan voice, kept), a32 (魏記 heard 危機, 宰相府 heard
# 宰相服務), a36 (花轎 heard 花架), a37 (勝出 heard 釋出). a04 was re-recorded too (照樣往縣城撐 heard 網線稱稱 plain) but the
# retake was worse (撐 heard 捧), so the first take stays (the retake in audio/take2/).
# 6 s: every other speaking shot. The longest: s16 (a14 5.66 s of speech), s37 (a35 5.58 s with the nod),
#      s13 (a09 2.34 + a10 3.0 + 0.5 = 5.8 s; the script's 9 s long shot is split, his thought a11 3.2 s in s13b).
# 5 s: the inserts with an off-screen line hold it: s15 (a13 3.35 s), s35 (a33 3.66 s).
# 8 s: s40 (a37 3.2 + a38 2.07 + 0.5 = 5.8 s fits 6 s, but it is the episode's last shot: the thumb lifts, the red panel and
#      its accent need a held tail, as e920 s38 and e921 s37 ended on a hold; the script's long-shot list buys 8 too).
# 8 s: s20 (e023 review 必改 6): a18 is 6.12 s long with 5.62 s of speech, which a 6 s clip holds only at the full 6.27 s; a back
#      shot's pick almost always loses its first 0.5-1.25 s (e921, e922 picks), and s21 after it is a 5.92 s off-screen line.
# No shot runs over about 10 s, so nothing more is split.
BUY = {"s20": 8, "s40": 8}


# ---- e022 review 必改 12 (the refine text), the same here: hailuo/clips-dh-e923.json column 0 is the motion text refine-prep.py
# sends with a picked d1 draft. gen-dh.mjs opens every clip that lists tangxiaotang with the CG-era "Tang Xiaotang's high
# stand-up collar stays closed at her throat." and names her in "<names> shown in <Picture 1>"; in a back shot that draws the
# collar back and turns her face to the lens. In the back shots the sentence goes and her name becomes "the young woman seen
# only from behind"; in her silent face shots (s19, s37, s40) it becomes the cross-collared jacket. Column 1 is recomputed.
COLLAR = "Tang Xiaotang's high stand-up collar stays closed at her throat. "
COLLAR_LIVE = "Tang Xiaotang's cross-collared jacket stays wrapped shut across her chest. "
BACK_NAME = "the young woman seen only from behind"
FACES = {"s19", "s37", "s40"}


def live_clips(path):
    import hashlib
    import json
    import re
    clips = json.load(open(path, encoding="utf-8"))
    for key, row in clips.items():
        sid = key.split("-", 1)[1]
        text = row[0]
        if sid in FACES:
            text = text.replace(COLLAR, COLLAR_LIVE)
        elif COLLAR in text:
            text = text.replace(COLLAR, "")
            m = re.search(r"\[Shot 1\] 3D CG\. (.+?) shown in <Picture 1> (keeps?) ", text)
            names = [n for n in m.group(1).split(" and ") if n != "Tang Xiaotang"]
            who = " and ".join(names + [BACK_NAME])
            who = who[0].upper() + who[1:]
            verb = "keep" if names else "keeps"
            text = text.replace(m.group(0), f"[Shot 1] 3D CG. {who} shown in <Picture 1> {verb} ", 1)
            assert "Tang Xiaotang" not in text, (key, "her name is left in a back shot's refine text")
        assert "stand-up collar" not in text, key
        row[0] = text
        row[1] = hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]
    open(path, "w", encoding="utf-8").write(json.dumps(clips, ensure_ascii=False, separators=(",", ":")))


if __name__ == "r2spec":
    import atexit
    import os
    atexit.register(live_clips, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "hailuo", f"clips-dh-e{EP}.json"))
