"""Episode 19 remake (r2): the writer spec for ../e001-r2/build-r2.py. Source: docs/videos/zhong-tian-qu-qi-e019-r2/script.md
(c01-c41 = s01-s41; the CG-era r2 script of PR #2024), including its sections 「這版改了什麼」, 「2026-11-06 審稿後的修改」 and
「真人版的改動（2026-11-16）」, which override the tables. Every line is the script's, word for word; only the staging changes.
Bible: production/r2-bible-e011-e020.md (rules 1-18).

Live action from the first draft, written the way e018-r2/r2.py stands AFTER its independent review (review.md in ../e018-r2:
16 必改 and the cheap 建議) and the e918 picking lessons (colab/runs/e918-live/{picks-merged.tsv, fix1/mkspec.py,
fix2/mkspec.py}), the e917 ones (e917-live/picks-merged.tsv) and refs-live/README.md:
- OFFSCREEN_SPEECH = False (bible rule 15): every shot with an off-screen line, a thought or a system line writes the silence
  of each person on screen (quiet(), SILENT_HE), after the action.
- Bible rule 18: nothing is negated by name; backgrounds say what is there. Paper is never read: the ledger page is held up
  toward the dais with its blank back to us (s18) or folded (s20); the ledger is closed, its cover plain.
- Hands and props are placed in the composition (the first frame), each in its owner's named hand; contact between two people
  is a state from the first frame, never a grab: Qian Yuanwai's silk-wrapped arm along Xu Yan's (s01, e918 fix1's s40),
  Qin Shuang's hands on Lai San's collar and shoulder (s04) and at the knot of his rope (s10), the black-sleeved hands already
  holding Qian Yuanwai's forearms (s12) and upper arms (s26), Tang Xiaotang's hand already on Xu Yan's sleeve (s27), the box of
  silver already in Tang Xiaotang's hands (s28) and under Qin Shuang's arm (s29, s37).
- Gestures: no pointing finger (e916 s26): Xu Yan's accusations (s14, s20) are an open hand, palm up.
- Tang Xiaotang never speaks on camera (bible rule 3): her five on-screen lines (s18, s28, s36, s39, s41) are said from behind
  her (TBACK = e916 fix1's two high round buns, nospeak; spec.json drops her three face pictures and her identity sentence),
  one fixed gaze per shot, her head held still (no head shake in s39, no turn in s41: a turning head shows the face, e914
  s24); s19 (her reading of the page) is Qian Yuanwai's face draining, her line off screen; s27 is her hand only. Her silent
  face (s06, s07, s20, s38) gets e907's neutral face sentences in spec.json. Costume: the live portrait l1, cross-collared and
  closed, no outer coat (bible rule 4; the script's t2 high collar and apricot coat are not used).
- No weapon and no yamen man anywhere (bible rules 5, 16-18): Qin Shuang's belt is empty (extras.json); the four yamen men are
  only their hands in plain black cotton sleeves, their owners outside the frame (s12 holding his forearms, s26 dragging
  Qian Yuanwai out; s28's handing over of the box is a sound and the line, review 必改 17); the 「威武」 and the beating are sounds; the gavel block is a flat oblong block of
  wood. The onlookers are two backs at the bottom edge of s08.
- Red hands (bible rule 12; e918 review 必改 10): an even matte persimmon orange-red like dye in cloth, from the fingertips to
  the wrists, written as a state from the first frame (Lai San from s04, Qian Yuanwai from s12, when his sleeves are already
  bunched at his elbows). Before s12 (s01, s02, s04, s09) Qian Yuanwai's hands are inside his sleeves, framed out above the elbows
  or below the bottom edge, and his cast sentence loses the gold rings (spec.json); after s12 his hands are behind his back
  (s15, s17, s19) or out of the frame (s26), and only s12, s13 and s23 show them.
- Qian Yuanwai (e918 fix1, fix2): his cap is the portrait's tall round smooth black cap and his robe the portrait's round
  collar (spec.json replaces cast.json's small cap and cross collar in his identity sentence); his hands never leave his
  sleeves by day before s12 (the s01 arm is e918 fix1's s40 tube of silk, the frame above both men's elbows); he grinned while
  begging in e918 s37 (three takes), so his one defeated line, the confession s23, is said face-down to the floor (nospeak,
  the recording laid in); his other lines are angry, defiant or spiteful (s02, s09, s12, s15, s17, s26: e918 s34 and s36
  held), every one with the mouth corners written pulled down.
- Magistrate Hu and Qian Yuanwai (two plump round-faced middle-aged men) are never in one frame (bible 同框撞臉): Hu's three
  shots (s05, s22, s24) are on the dais crop; s21's script over-the-shoulder past his hat is Xu Yan alone looking up at the dais
  (a back with no picture grows a second person: e918 s19, and the dais crop exists to keep a second magistrate out).
- No more than three named faces in a shot (bible rule 1): s07 (Tang Xiaotang, Qin Shuang, Lai San with his head bowed), s10
  (Xu Yan, Lai San, Qin Shuang); s04 is two faces and Qian Yuanwai's unnamed back at the right edge, s37 Qin Shuang alone
  (review 必改 6, 7).
- Nobody is flipped in the edit: every speaker wears a cross or round collar; sides are written as screen left/right.
State at the junction (e018 s40 as retaken in e918 fix1): the side room, Xu Yan on screen left, Qian Yuanwai on screen right
with his left arm laid along Xu Yan's right upper arm in one continuous tube of gold silk, the frame above both men's elbows,
Qian's tall round smooth cap. s01 starts in that state.
Places (the coordinator's decisions, 2026-11-16; listed again in script.md 〈真人版的改動〉; every picture looked at full size):
- the side room set-xianya-ceting-l1 (s01-s03; swap_pictures in place of set-xianya-l1, the gate, which gen-dh's "county yamen"
  line gives): the long grey curtain in the doorway on the left, the long table and two armchairs, the lattice window on the
  right. Grey overcast morning.
- the court hall, the afternoon: set-xianya-gongtang-floor-l1 (e918's crop: two pillars, lattice windows, a low white panel, the
  tiles; no desk, armchair or board) for every floor shot (s04, s06-s10, s12, s14-s21, s23, s25-s27) and
  set-xianya-gongtang-dais-l1 (e918's crop: the white panels, desk, armchair, block and brush rack, the board out of the frame)
  for Magistrate Hu (s05, s22, s24). The prompts on the floor never say "magistrate"; the dais is "the high dais above the top
  of the frame". The script's door on the left with its sunlit door frame is not in the picture: the light is soft warm
  afternoon daylight from the lattice windows (the picture's even grey light would win over a hard shaft of sun).
  The hand inserts s11 and s13 send no set picture, only the cloth of the owners' sleeves (review 必改 3: laisan-sleeve-l1 and
  qianyuanwai-sleeve-l1, the portraits cropped below the collar, no face).
- the yamen gate, the late afternoon: a NEW free crop set-xianya-steps-l1 = set-xianya-l1 crop=870:489:0:187 (refs-live/README.md,
  last paragraph): the left half of the gate hall with the whitewashed wall and its dark arched doorway, a red pillar, the open
  dark red doors, the big drum on its red frame and the top of the pale stone steps. The whole picture has an empty red rack on
  the right that reads as a weapon rack (bible rule 18: e913's yard grew spear racks); the crop leaves it out. The script's
  stone lions and black doors are not in the picture and are not written. s28-s37 send set-xianya-steps-l2 (review 必改 14: the
  red block behind the drum frame, a row of black glyph-like strokes at 4x, painted near-black by drawbox).
- the roof at night: a NEW free crop set-wuding-eave-l1 = set-wuding-l1 crop=840:472:0:130: the slope of dark tiles, the top of the
  ladder at the left eave and the black sky. The whole picture has a persimmon tree loaded with orange fruit on the right (the
  bible's red-bead glitch; the script's tree is almost bare) and the full moon in the middle of the sky; the crop leaves both
  out, the moon is written beyond the upper right. Only s38 sends a roof picture, set-wuding-eave-l2 (review 必改 15:
  set-wuding-l1 crop=800:450:0:96, the eave tiles with glyph-like reliefs cut off, the ladder top kept); s39-s41 send none
  (roof_c: the dark tiles and the black night sky in words), to keep the 3D look out of the closer shots.
- gen-dh.mjs, build-r2.py and cast.json are NOT changed: "county yamen" maps to set-xianya and "roof of the farmhouse" to
  set-wuding; the five pictures go in through spec.json swap_pictures (applied by prep919.sh with absolute paths).
No screen test is needed: every picture the jobs send is already in refs-live (two of them new free crops).

AFTER THE INDEPENDENT REVIEW (review.md in this folder: 18 必改 all applied, the cheap 建議 taken; 2026-11-16, the coordinator
deciding for the owner):
- Four free pictures (refs-live/README.md, last paragraph; swapped in by spec.json swap_pictures with absolute paths):
  set-xianya-steps-l2 (必改 14, s28-s37), set-wuding-eave-l2 (必改 15, s38 only; s39-s41 roof_c with no roof picture),
  qianyuanwai-sleeve-l1 and laisan-sleeve-l1 (必改 3, s13; 建議 s11 too). They are l2s of e919's own new ids (set-xianya-steps,
  set-wuding-eave) and new sleeve ids; pilot.py only looks up set-xianya and set-wuding, and prep919.sh checks the newest.
- Qian Yuanwai's angle-b (a hanging knot behind a two-layer cap) is sent nowhere (必改 13): s02, s12, s26 drop it; the close-ups
  s09, s15, s17, s19 send the portrait + angle-a. The paid cap edit and the paid roof edit are not done (coordinator).
- s01 his arm drops past the bottom edge, the sleeve closed (必改 12); s04 two faces, Qian's unnamed back at the right edge,
  his start moved to s09 (必改 7); s06 Tang Xiaotang behind Xu Yan on screen right (必改 2); s11 the palms stay up (必改 8);
  s12 body square, both black hands only hold, three silent seconds, the shout from the fourth; a11 laid ~1.3 s earlier over
  the end of s11 in the cut (必改 1); s13 the sleeve crops and a cloth sentence (必改 3); s16 the lantern sentence with its
  scale (必改 9); s18 no "writing" (必改 10); s23 no face pictures, no name, from above-front, the cap brim covering the face,
  the red hands flat on the floor: e918 fix2 s37's untested back-view approach (必改 4); s26 the left shoulder, lips pressed,
  a huff through the nose, no sneer (必改 5); s28 the box in her hands, no yamen hands (必改 17); s34, s36 the second the line
  starts (必改 11); s37 Qin Shuang alone, the left shoulder (必改 6); s38 the slope and the ladder poles, no eave tiles in the
  foreground (必改 15); s41 her chin on her knees from the first frame to the last (必改 18); a42 re-recorded (必改 16).
- 建議 taken: s17 and s26 buy 8 s; s22 the forehead wipe goes (stays 6 s); the gate light is soft warm light with the gate
  hall in shade; the silk corner only in s21; no pearl pins on her back; s02 the young man's head still; s38 Tang high on the
  slope below the ridge line; s11 the sleeve crop; the s12 length noted (9.4 s of speech, a 10.5 s file). Accepted as is:
  the cool court-hall crops (warmed in the grade), s38's long ribbon (look at it when picking), s41's unseen red eyes,
  s05/s24.
"""
EP = 919  # internal working number; the published slug is zhong-tian-qu-qi-e019-r2
SLUG = "zhong-tian-qu-qi-e019-r2"
EP_TITLE = "公道不拿來換，兩雙紅手並排（重製版 r2）"
OUTLINE_SECONDS = 226  # script.md: 226 s, 41 shots (27 + 10 + 4)
TARGET_MINUTES = [3, 4]
TITLE = "兩雙紅手｜種田娶妻打天下 第19集（重製版）"
DESCRIPTION = "縣衙側廳裡，錢員外拿落水的真相換一條生路，許硯把袖子抽回來：真相我自己查，公道不拿來換。午後升堂，秦霜押著賴三進門，許硯當眾說出錢員外想拿什麼換。錢員外不肯伸手，賴三的手先伸出來，橘紅到手腕；袖子一捲，兩雙一樣紅的手並排。薑黃碰上草木灰，洗一夜也不掉。唐小棠呈上錢府的帳頁：收魏記銀三百，起火前一天付賴三五兩。許硯輕拍懷裡：那晚從您袖子掉出來的東西，學生還收著。錢員外認了縱火，賠銀一百兩，被押下去時回頭丟下一句：你落水那天的事，回去問你許家人。三人好感突破二十，系統一口氣給了製糖法、隊列操練法和鴨群治蝗法。當夜屋頂上，唐小棠抱著膝蓋問他：若有人來帶我走，你會讓嗎？《種田娶妻打天下》第 19 集（重製版）。"
THUMB = ("兩雙紅手", "s13")
CHARACTERS = ["xuyan", "qianyuanwai", "huxianling", "laisan", "tangxiaotang", "qinshuang", "aling", "xitong"]
MUSIC = "one cue per scene: a slow heavy cue of deep drums in a county court hall growing denser as the trial goes on, one hard accent on a pair of red hands, one big accent on a confession, a soft chime, then low held strings under a spiteful last line; then a warm relaxed cue of plucked strings outside the court in the late afternoon, one bright accent and one beat of silence; then a quiet night cue of solo guqin on a moonlit roof, one held pause at the end; ancient Chinese rural drama, no vocals"

# Scene 1: the side room (set-xianya-ceting-l1 swapped in), then the court hall in the afternoon (set-xianya-gongtang-floor-l1 for
# the floor, set-xianya-gongtang-dais-l1 for Magistrate Hu, both swapped in). Scene 2: outside the yamen at the foot of the steps
# (set-xianya-steps-l2 swapped in). Scene 3: the roof at night (set-wuding-eave-l2 swapped in for s38 only). Close shots use the `_c` headers.
# gen-dh SET takes the FIRST pattern in its list order that the whole prompt matches: the yamen prompts say "county yamen" and
# never "city gate", "gatehouse", "town square", "official road", "alley", "teahouse" or "farmhouse"; the roof prompts say
# "roof of the farmhouse" and never "yard", "Xu farmhouse", "county yamen" or "campfire".
SIDE = ("a plain grey plastered back wall, a doorway on the left hung with a long plain grey cloth curtain, one long dark wooden "
        "table against the back wall with one dark wooden armchair at each end, one tall narrow lattice window on the right, a "
        "floor of grey stone tiles")
HALL = ("a floor of large grey stone tiles, thick round dark red-brown wooden pillars, tall dark wooden lattice windows along "
        "the side wall above a low white panel")
DAIS = ("at the back one long dark wooden desk with one dark wooden armchair behind it, before a wall of plain white panels; on "
        "the desk one flat oblong block of dark wood at the left and a small brush rack at the right")
# set-xianya-steps-l1/-l2 (the crop of set-xianya-l1; l2 has the red block painted out): what is in it.
GATE = ("pale stone steps rising to a raised stone platform, on it the open front of the gate hall: one thick red-lacquered round "
        "pillar, two tall dark red wooden doors standing open, one big round drum with a pale hide on a red wooden frame in front "
        "of the doorway, grey brick walls, and at the left a whitewashed wall with a dark arched doorway")
# set-wuding-eave-l2 (the crop of set-wuding-l1, review 必改 15): what is in it. Only s38 sends it; s39-s41 use roof_c.
ROOF = ("a long slope of plain dark grey curved roof tiles in even rows rising to the straight ridge that runs from the top left "
        "corner down to the right edge, the two bamboo poles of the ladder top at the bottom left, the black night sky with a few "
        "thin dark clouds above the ridge at the upper right")
LOC = {
    "side": f"In the side room of the county yamen on a grey overcast morning: {SIDE}; soft grey daylight from the window on the right",
    "side_c": "In the side room of the county yamen on a grey overcast morning, a plain grey wall, soft grey daylight from the window on the right",
    "hall": f"In the court hall of the county yamen in the afternoon: {HALL}; soft warm afternoon daylight from the tall lattice windows",
    "dais": f"In the court hall of the county yamen in the afternoon: {DAIS}; soft warm afternoon daylight from the tall lattice windows",
    "hall_c": "In the court hall of the county yamen in the afternoon, dark red-brown pillars and tall lattice windows, soft warm afternoon daylight",
    "gate": f"Outside the county yamen in the late afternoon, at the foot of its stone steps: {GATE}; soft warm late-afternoon light, the gate hall in soft shade",
    "gate_c": "Outside the county yamen in the late afternoon, the pale stone steps and the red pillar of the gate hall soft behind, soft warm late-afternoon light",
    "roof": f"On the roof of the farmhouse in the middle of the night in late autumn: {ROOF}; cold white moonlight from beyond the upper right, a pale frosty sheen on the tiles",
    "roof_c": "On the roof of the farmhouse in the middle of the night, dark grey tiles and the black night sky, cold white moonlight from beyond the upper right",
}
LIGHT = {
    "side": "the soft grey daylight stays unchanged",
    "hall": "the soft warm afternoon daylight stays unchanged",
    "gate": "the soft warm late-afternoon light stays unchanged",
    "roof": "the cold moonlight and the deep night stay unchanged",
}
# bible rule 15: no "<X> speaks off screen" / "the system voice speaks off screen".
OFFSCREEN_SPEECH = False

# Repeated wording (each prop is one object).
# The dark red silk pouch inside his robe all day (script; patted once in s21, never taken out).
XU_POUCH = ("Xu Yan, in his faded blue-grey scholar's robe patched at one elbow, a small rounded bulge at the left breast of his "
            "robe where a pouch is tucked inside")
XU_COAT = "Xu Yan, in an old plain grey cloth outer coat over his faded blue-grey scholar's robe"
QIN = ("her dark brown cross-collared short jacket, wide plain leather belt with nothing tucked in it and nothing hanging from it, "
       "black trousers, leather boots and high ponytail tied with black cord")
TANG = "in her peach-pink cross-collared short jacket wrapped shut over a pleated skirt with a ribbon bow"
GOLD = "the small gold abacus hanging at her right hip, still"
# e916 fix1 / e918 review 必改 1: two high round buns, a short ribbon wrapped round each, the nape bare.
TBACK = ("one young woman seen only from behind, appearing only once: the back of her head with all of her black hair gathered "
         "up into two round buns set high on her head, a short pink silk ribbon wrapped around each bun, the "
         "nape of her neck bare above a pink inner collar, and her light peach-pink silk shoulders; the back of her "
         "head toward us the whole time, her ear the furthest round her head we ever see")
HEADSTILL_TANG = "the young woman with the two high round buns keeps her head still, the back of her head toward us the whole shot"
TLEDGER = "one thread-bound ledger held closed against her chest in both arms, its cover one even plain dark blue cloth from edge to edge"
ALING = "in her plain grey-white cotton dress with long sleeves covering her wrists, her black hair in a high bun with one plain wooden hairpin"
# e918 fix1 (s35, s37, s40): the portrait's tall round smooth cap, never a small cap with tails; the portrait's round collar.
QIAN = ("Qian Yuanwai, in his dark gold silk round-collared robe with roundel patterns and long wide sleeves, a white inner collar "
        "at his neck, and his tall round smooth black cap, plain and smooth all the way round down to its rim")
SLEEVES_IN = ("both his hands pushed deep inside his long wide dark gold sleeves, the cuffs hanging well past his fingertips, the "
              "two sleeves joined in front of his belly, his hands hidden inside them the whole time")
BEHIND = "both his arms already behind his back from the first frame, his hands hidden behind him below the bottom edge of the frame"
LAI = ("Lai San, the thin small young man in his grey-brown hemp cross-collared short jacket and old cloth head wrap, his left "
       "foot dragging in a limp")
# bible rule 12, e918 review 必改 10: matte persimmon like dye in cloth; nothing negated.
RED = ("stained an even matte persimmon orange-red from the fingertips to the wrists, the colour sitting evenly in the skin like "
       "dye in cloth, the skin smooth, whole and dry")
ROPE_TIED = "his two wrists tied together in front of his belly with one plain hemp rope as thick as a finger"
HU = "in his black gauze futou hat with two short stiff flat wings and his blue-green round-collared official robe"
GAVEL = "one flat oblong block of dark polished wood the size of half a brick, plain on every side"
BUNDLE = "one bundle the size of two hands wrapped in an old plain blue cotton cloth, its knot loose"
# bible 道具表 (e017 r2 on): the charred lantern frame with the Qian manor's plain copper plate.
LANTERN = ("one charred lantern frame: a ring of blackened bamboo ribs two hands wide, its paper burnt away to a few brown "
           "scorched edges, and at its base one small plain copper plate the size of a thumbnail, far smaller than his palm, a "
           "raised ring round a small square hole, smooth and plain")
SILVERBOX = "one small plain dark brown wooden box the size of two hands, plain on every side"
BLACK_HANDS = "hands in plain black cotton sleeves"
HANDS = "their hands hold only what is described here"
SILENT_HE = "He says nothing in this shot: his lips stay pressed together from the first frame to the last, his jaw still, no talking, no mouthing words"
GAZE_HIM = "she looks straight ahead at the young man the whole shot"


def only_tang(side):
    """e915 s26/s41: a second Tang appeared beside her back. One person with buns, one fixed side."""
    return (f"she is the only young woman in the frame and the only one with two high round buns, and she stays in the {side} "
            f"foreground from the first frame to the last")


def quiet(who, pr="his", plural=False):
    verb = "say" if plural else "says"
    return (f"{who} {verb} nothing in this shot: {pr} lips stay pressed together from the first frame to the last, no talking, "
            f"no mouthing words, the face set and still")


def dais_shot(expr, gaze):
    return (f"low-angle medium close-up from below the dais: Magistrate Hu, {HU}, sitting behind the long dark desk, framed from "
            f"the chest up with clear space above his hat, his right hand already resting flat on {GAVEL} on the desk, {gaze}, "
            f"never the lens; {expr}; behind him only the plain white panels, the top of the frame at the top edge of the white panels")


SHOTS = [
    # ---- scene 1a: the side room, day 15 in the morning (set-xianya-ceting-l1). The junction of e018 s40 (fix1): Xu Yan left,
    # Qian Yuanwai right, the frame above both men's elbows. The curtained doorway is on the left: Xu Yan leaves that way.
    dict(chapter="側廳", loc="side_c", cam="Medium close two-shot, slow push in", chars=["xuyan", "qianyuanwai"], night="side",
         comp=f"medium close two-shot, the bottom edge of the frame cutting across both men just above the elbows: on screen left {XU_POUCH}, framed from the upper chest up with space above his head, his face three-quarter to screen right toward the man, his eyes lowered to his own right sleeve, never the lens; cold: brows drawn, lips pressed flat; on screen right {QIAN}, framed from the upper chest up, leaning in close to him; his left arm rests along Xu Yan's right upper arm from the first frame, wrapped in one long continuous tube of dark gold silk from his shoulder to below the bottom edge of the frame, the sleeve end hanging down past the bottom edge; his other arm held against his own belly inside its wide gold sleeve, below the frame; the only skin showing on either man is the face and neck; his face three-quarter to screen left toward Xu Yan, never the lens; waiting and sly: eyes narrowed, brows lifted, lips pressed together; behind them only the plain grey wall; {HANDS}; exactly two people",
         lines=[("xuyan", "真相我自己查，用不著你拿來換。", "冷，一字一字")],
         motion=f"in the first second Xu Yan pulls his right arm out from under the gold silk with one sharp tug, and the silk slides off it; Qian Yuanwai's gold-sleeved arm drops straight down past the bottom edge of the frame, the long sleeve closed round his hand; he lifts his eyes to the man's face and speaks coldly; after the last word he turns his shoulders toward screen left, away from the man; {quiet('Qian Yuanwai')}",
         zh="近景雙人、慢推（送 `set-xianya-ceting-l1`；接第 18 集 s40 重拍 fix1 的狀態：畫面下緣切在兩人手肘之上，錢員外左臂沿許硯右上臂、整條包在一條連續的金綢袖裡、袖口垂出畫外；高圓頂平滑黑帽）：許硯第一秒手臂一抽，把袖子從金綢下抽回來，錢員外那條金袖手臂直直垂到畫面下緣外、長袖口合著包住手（審稿必改 12），許硯抬眼冷冷地一字一字說；說完肩膀轉向畫左（門簾）；錢員外嘴閉著、瞇眼等著（手不入鏡）"),
    dict(loc="side", cam="Over-the-shoulder medium shot, slow push in", chars=["qianyuanwai"], night="side",
         comp=f"over-the-shoulder medium shot from close behind one young man in a faded blue-grey scholar's robe seen only from behind, appearing only once, in the left foreground, his body half turned toward the left, the back of his head toward us and still the whole shot, only the back of his head with a topknot and his right shoulder showing, soft; facing us a step away a little right of the middle, {QIAN}, framed from the chest up with clear space above his cap, {SLEEVES_IN}, his joined sleeves below the bottom edge of the frame, his face three-quarter to screen left toward the young man, never the lens; furious and frightened: brows knotted, eyes bulging, teeth clenched between words, the corners of his mouth pulled down; behind him only the plain grey wall and the tall lattice window at the right; {HANDS}; exactly two people, the young man in the foreground seen only from behind",
         lines=[("qianyuanwai", "你不要命了？過了今天，你就再也問不到！", "咬牙")],
         motion="Qian Yuanwai takes one quick step after the young man and stretches his neck forward, hissing the words through his teeth; the young man in the foreground keeps his head still, the back of his head toward us the whole shot; after the last word Qian Yuanwai's jowls quiver and his mouth stays pulled down",
         zh="過肩中景、慢推：前景左只有許硯的後腦（髮髻）與右肩（不點名、不送圖，身子半轉向畫左、後腦整鏡不動）；錢員外在畫面中偏右往前追一步、脖子一伸，咬牙壓著嗓子說（胸口以上，兩手在併在肚前的長袖裡、在畫面下緣外）；說完腮幫抖、嘴角往下（不笑）"),
    dict(loc="side", cam="Medium shot, slow push in", chars=["xuyan"], night="side",
         comp=f"medium shot at the curtained doorway on the left: {XU_POUCH}, standing in the doorway, framed from the knees up with clear space above his head, his left hand already holding the long plain grey cloth curtain lifted aside from the first frame, his body toward the doorway and his head and shoulders half turned back toward screen right, his face three-quarter to screen right toward Qian Yuanwai off screen right, never the lens; steady and cold: brows level, eyes hard, lips moving evenly between words; behind him only the grey curtain and the plain grey wall; {HANDS}",
         lines=[("xuyan", "我要的是公道，公道不拿來換。午後，堂上見。", "穩，冷")],
         motion="Xu Yan holds the curtain aside and speaks back over his shoulder; after the last word he turns, steps through the doorway and lets the curtain fall behind him, the curtain swinging",
         zh="中景、慢推（側廳左邊的布簾門口）：許硯第一格左手已經掀著灰布簾，身子朝門、頭與肩半回頭朝畫右（錢員外，畫外），冷冷地說；說完轉身走出去、放下布簾、簾子晃"),
    # ---- scene 1b: the court hall in the afternoon (set-xianya-gongtang-floor-l1 / -dais-l1). Floor axis as e018: Xu Yan on
    # screen left, Tang Xiaotang one step behind him at his right (screen right), Lai San kneeling in the middle with Qin Shuang behind him, Qian
    # Yuanwai kneeling on screen right; the dais is above the top of the frame. Hu and Qian Yuanwai are never in one frame.
    # (Review 必改 2: Tang Xiaotang is one step behind Xu Yan on screen RIGHT, as in s07, s20 and s27.)
    dict(chapter="公堂", loc="hall", cam="Medium shot, slow push in", chars=["qinshuang", "laisan"], night="hall",
         comp=f"medium shot on the stone floor, framed from the knees up, the pillars and the lattice windows behind, the high dais above the top of the frame: a little left of the middle {LAI}, standing hunched, {ROPE_TIED}, his tied hands in front of his belly, both his thin hands {RED}, his face lowered, never the lens; frightened: eyes darting, lips pressed together and trembling; close behind him on screen left Qin Shuang, {QIN}, standing, framed from the knees up with clear space above her head, her right hand gripping the back of his collar and her left hand on his near shoulder from the first frame, never the lens; cold: brows level, eyes hard, lips moving crisply between words; at the right edge, soft, one portly man in dark gold silk and a tall round smooth black cap kneeling with his back to us, seen only from behind; behind them only dark red-brown pillars and the tall lattice windows; {HANDS}; exactly three people, the kneeling man at the right edge seen only from behind",
         lines=[("qinshuang", "大人，人證帶到了，錢府的賴三。", "冷")],
         motion=f"In the first second she presses down on his shoulder and he drops to his knees on the stone; then she lifts her face toward the high dais above the top of the frame and speaks; {quiet('Lai San')}; the kneeling man at the right edge stays still, his back to us; after the last word her left hand stays on his shoulder",
         zh="中景、慢推（送公堂地面裁切圖 `set-xianya-gongtang-floor-l1`：柱子、格窗、白裙板、地磚；高台在畫面上緣外、胡縣令不入鏡）（審稿必改 7）：第一格賴三已經站在地中間偏左、兩手腕被麻繩綁在肚前、兩手已經橘紅；秦霜在他身後畫左，右手揪著他的後領、左手按著他近的那邊肩膀；第一秒她一按，他跪下；她抬臉朝上面的高台冷冷地說；畫右緣虛焦一個穿暗金綢、戴高圓帽跪著的背影（錢員外，不點名、不送圖；他那一驚交給 s09）。兩張臉。原稿前景衙役的水火棍與兩排衙役不拍，『威武』只留音效"),
    dict(loc="dais", cam="Low-angle medium close-up, slow push in", chars=["huxianling"], night="hall",
         comp=dais_shot("pompous: chin raised, brows lifted, eyes half lidded, mouth drawn long between words", "his face three-quarter to screen left"),
         lines=[("huxianling", "升堂！一個告逃稅，一個告縱火，誰先說？", "拖長官腔")],
         motion="in the first second Magistrate Hu lifts the wooden block a hand's height and brings it down flat on the desk with one sharp knock, then speaks, his eyes moving from screen left to screen right below him; after the last word his chin stays up and his eyes stay half lidded",
         zh="低角度中近景、慢推（送公案裁切圖 `set-xianya-gongtang-dais-l1`，匾在畫外，畫面上緣切在白屏板頂）：胡縣令（黑紗幞頭兩片短硬平翅、藍綠圓領官袍）右手第一格已經按在扁長方的驚堂木上，第一秒內抬起一掌高往案上一拍，再拖長官腔問，眼睛從畫左掃到畫右；說完下巴不放"),
    dict(loc="hall", cam="Medium shot, slow push in", chars=["xuyan", "tangxiaotang"], night="hall",
         comp=f"medium shot on the stone floor below the high dais: a little left of the middle {XU_POUCH}, standing, framed from the knees up with clear space above his head, his hands joined in front of his chest in a scholar's bow, his face tipped up toward the high dais above the top of the frame, never the lens; composed and firm: brows level, eyes steady, lips moving evenly between words; one step behind him on screen right, half behind his right shoulder, Tang Xiaotang {TANG}, {GOLD}, standing, framed from the knees up, soft, {TLEDGER}, her face three-quarter to screen left toward him, never the lens; tense: brows drawn, lips closed; behind them only a dark red-brown pillar and the tall lattice windows; {HANDS}; exactly two people",
         lines=[("xuyan", "學生先說。錢員外剛才在側廳，拿我落水的真相換生路。", "不慌不忙")],
         motion=f"Xu Yan steps forward and bows his joined hands once toward the high dais, then turns his head toward screen right, past her shoulder, toward Qian Yuanwai off screen right, as he speaks; {quiet('Tang Xiaotang', 'her')}; after the last word his eyes stay on the right",
         zh="中景、慢推：許硯往前一步、拱手朝上面的高台一拜，再轉頭越過她的肩朝畫右（錢員外，畫外）不慌不忙地說；唐小棠在他右後方半步（畫右，跟 s07、s20、s27 同一邊；審稿必改 2）抱著合起的素藍布帳冊、臉朝畫左看他（中性臉、嘴閉著）"),
    # The three wives hear 「不換」 (script): s07 Tang Xiaotang and Qin Shuang (Lai San kneeling with his head bowed), s08 A-ling.
    dict(loc="hall", cam="Medium shot, slow push in", chars=["tangxiaotang", "qinshuang", "laisan"], night="hall",
         comp=f"medium shot on the stone floor: on screen left Tang Xiaotang {TANG}, {GOLD}, standing, framed from the waist up with clear space above her head, {TLEDGER}, her face three-quarter to screen left toward the young man off screen left, her eyes lifted to him, never the lens; moved: eyes widening a little, brows lifting, lips pressed together; on screen right Qin Shuang, {QIN}, standing, framed from the waist up, her left hand resting on the shoulder of {LAI}, who kneels in front of her at the bottom right with his head bowed and his face toward the floor; Qin Shuang's face three-quarter to screen left toward the young man off screen left, never the lens; one brow lifting, lips closed; behind them only a dark red-brown pillar and the tall lattice windows; {HANDS}; exactly three people",
         lines=[("xuyan", "學生不換。請大人，先看看他那雙手。", "穩")],
         motion=f"Tang Xiaotang hugs the ledger tighter to her chest and lifts her eyes; Qin Shuang's brow lifts and her hand on the kneeling man's shoulder loosens for a moment; the kneeling man keeps his head bowed; {quiet('Tang Xiaotang, Qin Shuang and Lai San', 'their', True)}",
         zh="中景、慢推：畫左唐小棠抱緊帳冊、抬眼看畫左的許硯（畫外）；畫右秦霜站在跪著低頭的賴三身後，眉毛一挑、按著他肩膀的手鬆一下；三人嘴閉著（許硯那句畫外）。兩人都朝畫左看（許硯在她們左前方）"),
    dict(loc="hall", cam="Medium shot, slow push in", chars=["aling"], night="hall", act=3,
         comp=f"medium shot near the doorway of the court hall: A-ling, {ALING}, standing beside a dark red-brown pillar, framed from the waist up with clear space above her head, her right hand holding the cuff of her left sleeve, her face three-quarter to screen right toward the young man's back off screen right, never the lens; still and intent: eyes lifting, brows drawing together a little, lips closed; at the bottom edge of the frame in the soft foreground the shoulders and the backs of the heads of two townsmen in plain hemp head wraps, seen only from behind; behind her the tall lattice windows bright with afternoon light; {HANDS}",
         lines=[],
         motion=f"A-ling takes half a step forward past the pillar, her eyes lifting to him and staying there; her right hand tightens on the cuff of her left sleeve; {quiet('A-ling', 'her')}; the two townsmen in the foreground stay still, their backs to us",
         zh="中景、慢推：公堂門口附近，阿令（灰白布裙、高髻木簪、兩袖蓋住手腕）站在柱子旁，聽到「不換」抬眼看畫右許硯的背影（畫外），右手握住左袖口；前景下緣兩個圍觀縣民的肩與包頭背影（虛焦）；嘴閉著。圖上沒有門口，光從格窗來（無台詞）"),
    dict(loc="hall_c", cam="Close-up, slow push in", chars=["qianyuanwai"], night="hall",
         comp=f"close-up of {QIAN}, kneeling, framed from the chest up with space above his cap, {SLEEVES_IN}, his joined sleeves below the bottom edge of the frame, his face three-quarter to screen left toward Xu Yan off screen left, never the lens; stubborn: chin jutting up, brows drawn down hard, the corners of his mouth pulled down, lips moving stiffly between words; behind him only a dark red-brown pillar and the soft afternoon light",
         lines=[("qianyuanwai", "老夫的手，憑什麼給你看？", "嘴硬")],
         motion="Qian Yuanwai's eyes flick to the kneeling man at screen left, then his chin jerks up and he pulls his joined sleeves tighter in against his belly below the frame; after the last word he keeps his chin up and his mouth pulled down",
         zh="近景、慢推（身後只有柱子與午後的光；原稿身後衙役的黑袍拿掉）：錢員外先瞄一眼畫左跪著的賴三（s04 那一驚移到這裡，審稿必改 7），下巴一抬、把併在肚前的兩隻袖子往懷裡攏緊（在畫面下緣外），嘴硬地說；說完嘴角往下"),
    dict(loc="hall", cam="Medium shot, slow push in", chars=["xuyan", "laisan", "qinshuang"], night="hall",
         comp=f"medium shot on the stone floor: on screen left {XU_POUCH}, standing, framed from the knees up with clear space above his head, his face three-quarter to screen right toward the kneeling man, never the lens; cool and decided: brows level, eyes steady, lips moving evenly between words; in the middle {LAI}, kneeling, framed full length, {ROPE_TIED}, both his thin hands {RED}, his face lowered, never the lens, lips pressed together and trembling; on screen right Qin Shuang, {QIN}, standing close behind him, framed from the knees up, bending forward over his shoulder, both her hands already at the knot of the rope round his wrists from the first frame, her face lowered toward the knot, never the lens, lips closed; behind them only dark red-brown pillars and the tall lattice windows; {HANDS}; exactly three people",
         lines=[("xuyan", "那就先看賴三的。秦霜，讓他把手伸出來。", "冷靜")],
         motion=f"Xu Yan lifts his chin at the kneeling man as he speaks; Qin Shuang pulls the knot loose and the rope drops from his wrists to the floor; {quiet('Lai San and Qin Shuang', 'their', True)}; after the last word Xu Yan's eyes stay on the man's hands",
         zh="中景、慢推：畫左許硯朝跪在中間的賴三一抬下巴說；畫右秦霜站在賴三身後、彎腰越過他的肩，兩手第一格已經在麻繩結上，解開、繩子掉到地上；賴三低頭、嘴閉著發抖（兩手橘紅）。三張臉（拍法 1）"),
    # Insert: Lai San's hands held out by Qin Shuang's: only laisan-sleeve-l1 (review 建議; the cloth, no face), no set picture.
    dict(loc="hall_c", cam="Insert close-up, slow push in", chars=["laisan"], nospeak=["laisan"], night="hall",
         comp=f"insert close-up, the shot opens directly on two thin hands from its very first frame, held out palms up above the grey stone floor, grey-brown hemp cuffs at the wrists, the palms and fingers {RED}; two slim hands in dark brown sleeves reach in from the top edge of the frame and already hold the thin hands by the wrists; the frame cuts all four sleeves at the forearms at the edges; around the hands only the grey stone tiles; only the hands, the sleeves and the floor are in the frame; soft warm afternoon daylight from the left",
         lines=[("laisan", "小、小的不知道，昨晚一摸那箱子就紅了。", "畫外，發抖")],
         motion="the slim hands pull the thin hands a hand's length forward by the wrists, the palms still turned up toward us; the thin orange-red hands tremble all the time in their grip",
         zh="插鏡、慢推（第一格就是賴三攤開的兩手：灰褐袖口、掌心與手指從指尖到手腕均勻的啞光柿子橘紅；秦霜深褐袖的兩手從畫面上緣伸進來、第一格已經握著他的手腕；四隻袖子都在前臂處被畫框切掉；不送場景圖，只送賴三定妝照領口以下的裁切 `laisan-sleeve-l1` 當袖口的布料，審稿建議）：秦霜把他的手腕往前拉一個手掌遠、掌心一直朝上（審稿必改 8：第一格已經朝上，不再『翻』），賴三的手一直抖。台詞剪接放錄音（賴三畫外）"),
    # The order off screen, then his line on screen; his sleeves are already being pushed up (a state) and his hands are red.
    dict(loc="hall", cam="Medium shot, slow push in", chars=["qianyuanwai"], night="hall",
         comp=f"medium shot of {QIAN}, kneeling on the stone floor, framed from the knees up with clear space above his cap, his body square to the camera and his face three-quarter to screen left, both forearms held out in front of his belly toward us from the first frame, his wide gold sleeves already bunched at his elbows; from the left edge one hand in a plain black cotton sleeve grips his right forearm, from the right edge one hand in a plain black cotton sleeve grips his left forearm; the left and right edges of the frame cut both black sleeves at the forearm; both his plump hands {RED}, three gold rings on his fingers, his forearms above the wrists his own pale skin; never the lens; outraged and frightened: eyes bulging, brows shooting up, the corners of his mouth pulled down; behind him only a dark red-brown pillar and the tall lattice windows; {HANDS}",
         lines=[("huxianling", "來人，把錢員外的袖子捲起來！", "下令"),
                ("qianyuanwai", "放肆！老夫是原告，你們敢動我！", "掙扎")],
         motion="For the first three seconds his lips stay pressed together, his eyes go wide and dart between the two black-sleeved hands, and the hands only hold him, steady. From the fourth second he jerks back against their grip and shouts the line; after the last word he leans away, his orange-red hands still held out by the wrists",
         zh="中景、慢推（審稿必改 1）：錢員外跪著（膝蓋以上，身子正對鏡頭、臉四分之三朝畫左），兩條前臂第一格已經伸在肚前朝我們、寬金袖堆在手肘；畫左緣一隻黑布袖的手抓他右前臂、畫右緣一隻抓他左前臂，兩隻黑袖都在前臂處被畫框切掉（衙役只拍手、只抓不推，人在畫外；拍法 16–18）；兩手從指尖到手腕已經橘紅、戴三枚金戒指，手腕以上是原本的膚色；前三秒嘴閉著、瞪眼、眼睛在兩隻手之間亂轉（胡縣令畫外下令），第四秒起往後掙、吼（紅寫成第一格的狀態，不演『慢慢露出紅』）（長鏡）。剪接：a11 從 s11 片尾往前約 1.3 秒開始（a10 講完以後），s12 的第四秒接 a12"),
    # Insert: the two pairs side by side (script: one accent). The owners' portraits only (no set picture), faces out of frame.
    dict(loc="hall_c", cam="Insert close-up, slow push in", chars=["laisan", "qianyuanwai"], nospeak=["laisan", "qianyuanwai"], night="hall",
         comp=f"insert close-up, the shot opens directly on two pairs of hands held out palms up side by side above the grey stone floor from its very first frame: on the left two thin hands with grey-brown hemp cuffs, on the right two plump hands with three gold rings, their dark gold silk sleeves pushed up to the elbows; all four hands {RED}, exactly the same colour; the frame cuts the four arms at the forearms at the bottom edge; around the hands only the grey stone tiles; only the four hands, the sleeves and the floor are in the frame; soft warm afternoon daylight from the left",
         lines=[("xuyan", "大人請看，兩雙手，一模一樣的紅。", "穩")],
         motion="the four hands stay held out side by side; then the plump fingers with the gold rings curl back toward their palms, and the thin hands keep trembling",
         zh="插鏡、慢推（第一格就是兩雙並排的手：左邊賴三的瘦手、灰褐袖口；右邊錢員外的胖手、三枚金戒指、金袖推到手肘；四隻手一樣的啞光柿子橘紅；手臂在畫面下緣被切掉；不送場景圖，只送兩人定妝照領口以下的裁切 `laisan-sleeve-l1`、`qianyuanwai-sleeve-l1` 當袖口的布料，沒有臉，審稿必改 3）：兩雙手停住，錢員外的手指往回一縮，賴三的手一直抖。原稿『被衙役的手按著』不拍（多兩隻手）。許硯那句畫外"),
    dict(loc="hall", cam="Medium shot, slow push in", chars=["xuyan"], night="hall",
         comp=f"medium shot on the stone floor: {XU_POUCH}, standing a little left of the middle, framed from the knees up with clear space above his head, his face three-quarter to screen right, never the lens; sharp and clear: brows level, eyes bright and hard, lips moving crisply between words; in the soft foreground at the bottom right edge the back of one plump orange-red hand with a gold ring, out of focus, only the hand showing; behind him only a dark red-brown pillar and the tall lattice windows; {HANDS}",
         lines=[("xuyan", "箱面刷了薑黃，鎖扣抹了草木灰，碰到就紅，洗一夜也不掉。", "清楚，一句一句")],
         motion="Xu Yan holds his right hand out open, palm up, toward Lai San off screen left, then moves it across toward the hand in the right foreground as he speaks; after the last word he lowers his hand and his eyes stay on the right",
         zh="中景、慢推：許硯站在兩人中間（畫面中偏左），右手攤開、掌心朝上，先朝畫左（賴三，畫外）、再移向畫右前景虛焦的一隻紅手背（錢員外，戴金戒指，人在畫外）（不用手指指人：e916 s26）；說完放下手、眼睛看右"),
    dict(loc="hall_c", cam="Close-up, slow push in", chars=["qianyuanwai"], night="hall",
         comp=f"close-up of {QIAN}, kneeling, framed from the chest up with space above his cap, {BEHIND}, his gold sleeves pushed up, his face three-quarter to screen left toward Xu Yan off screen left, never the lens; stubborn and cornered: neck stiff, chin jutting, brows drawn down hard, the corners of his mouth pulled down, lips moving fast between words; behind him only a dark red-brown pillar and the soft afternoon light",
         lines=[("qianyuanwai", "染布染的！老夫昨天看了一天的布，不行嗎？", "硬撐")],
         motion="Qian Yuanwai pushes his hidden hands further behind his back and stiffens his neck; after the last word he keeps his chin up, his mouth pulled down and his eyes darting",
         zh="近景、慢推：錢員外第一格兩手已經藏在背後（畫面下緣外），脖子一梗、硬撐著快快地說；說完下巴不放、嘴角往下、眼睛亂轉（稿子：硬撐的乾笑也不要）"),
    dict(loc="hall", cam="Medium shot, slow push in", chars=["xuyan"], night="hall",
         comp=f"medium shot on the stone floor: {XU_POUCH}, crouching on screen left, framed full length with clear space above his head, both his hands already at the loose knot of {BUNDLE} lying on the stone tiles in front of him, his face lowered toward it, never the lens; calm and sure: brows level, lips moving evenly between words; around him only the large grey stone tiles, a dark red-brown pillar and the tall lattice windows behind; {HANDS}",
         lines=[("xuyan", "染布的手，怎麼跟偷箱的賴三一個顏色？還有這燈籠骨架。", "反問")],
         motion=f"Xu Yan opens the blue cloth and lifts out with both hands {LANTERN}; he sets it down on the stone floor in the middle of the frame and stands up beside it, speaking; after the last word he stands still beside it, his eyes toward screen right",
         zh="中景、慢推：許硯蹲在畫左，兩手第一格已經在地上舊藍布包的結上，解開、雙手拿出燒剩的燈籠骨架（一圈焦黑竹骨、兩個手掌寬、紙燒光只剩幾道褐邊，底座一塊拇指甲大、比手掌小得多的素銅片：凸起的素環圍一個小方孔、沒有字；審稿必改 9 把錯接的句子拆開、寫比例），擺到公堂正中的地上、站起來，邊做邊反問；說完站在它旁邊、眼睛看右（長鏡）"),
    dict(loc="hall_c", cam="Close-up, slow push in", chars=["qianyuanwai"], night="hall",
         comp=f"close-up of {QIAN}, kneeling, framed from the chest up with space above his cap, {BEHIND}, his face three-quarter to screen left, never the lens; blustering: brows shooting up, eyes glaring, mouth wide between words and the corners pulled down after; behind him only a dark red-brown pillar and the soft afternoon light",
         lines=[("qianyuanwai", "一個破燈籠，誰家沒有？你拿真憑實據來！", "扯著嗓子")],
         motion="Qian Yuanwai's eyes flick down to the floor at screen left, then snap up to glare at Xu Yan off screen left as he shouts; after the last word his jowls shake and his mouth stays pulled down",
         zh="近景、慢推：錢員外紅手藏在背後（畫外），瞄一眼畫左地上的燈籠骨架、再瞪著畫左的許硯扯著嗓子吼；說完腮幫抖、嘴角往下"),
    # Tang Xiaotang's line from behind her (bible rule 3): the page held up toward the dais, its blank back to us (rule 17).
    dict(loc="hall", cam="Medium shot, slow push in", chars=["tangxiaotang"], nospeak=["tangxiaotang"], night="hall",
         comp=f"medium shot from behind her left shoulder: {TBACK}, standing on the stone floor in the left foreground, her body turned toward screen right, framed from the waist up, holding up one unfolded sheet of thick opaque paper at shoulder height in both hands, facing the dais beyond the right edge of the frame; the side toward us is plain, blank and evenly lit from our side, thick and opaque, nothing showing through it; {only_tang('left')}; beyond her only a dark red-brown pillar and the tall lattice windows, out of focus; nobody else in the frame",
         lines=[("tangxiaotang", "真憑實據，我這有。錢府的帳頁，一兩銀子買的。", "篤定")],
         motion=f"the young woman lifts the sheet a little higher toward the dais and holds it steady with both hands; {HEADSTILL_TANG}; she looks straight ahead at the dais beyond the right edge of the frame the whole shot",
         zh="【改背後拍】中景、從她左肩後拍、慢推：前景左只有唐小棠的後腦、兩顆高丸子（短粉緞帶、後頸露出）與肩，身子朝畫右；兩手把攤開的帳頁舉到肩高、朝畫右外的高台（朝著高台，我們這面是空白的、從我們這邊受光、不透光；提示詞不寫 writing，審稿必改 10），再舉高一點、拿穩；頭不動、看著畫右外的高台。原稿『從右袖抽出』並進第一格之前。台詞 nospeak，剪接放錄音"),
    # Her reading of the page: Qian Yuanwai's face takes it (bible rule 3: the reaction goes to the other person).
    dict(loc="hall_c", cam="Close-up, slow push in", chars=["qianyuanwai"], night="hall",
         comp=f"close-up of {QIAN}, kneeling, framed from the chest up with space above his cap, {BEHIND}, his face three-quarter to screen left toward the young woman off screen left, never the lens; the colour draining from his face: eyes widening, brows lifting, a bead of sweat at his temple, lips pressed together and pulled down at the corners; behind him only a dark red-brown pillar and the soft afternoon light",
         lines=[("tangxiaotang", "上個月十八，收魏記銀三百；起火前一天，付賴三五兩。", "念帳，清楚")],
         motion=f"Qian Yuanwai's eyes go wide at the first figure and his throat moves as he swallows; at the second his head draws back into his collar; {SILENT_HE}",
         zh="【改成錢員外聽的臉】近景、慢推：唐小棠念帳那句畫外（拍法 3：她不露嘴說話，原稿的『下巴以上』近景改拍對面）；錢員外紅手藏在背後，聽到第一筆眼睛睜大、吞一口口水，第二筆頭往領子裡一縮、太陽穴冒汗；嘴閉著、嘴角往下"),
    dict(loc="hall", cam="Medium shot, slow push in", chars=["xuyan", "tangxiaotang"], night="hall",
         comp=f"medium shot on the stone floor: on screen left {XU_POUCH}, standing, framed from the knees up with clear space above his head, his face tipped up toward the high dais above the top of the frame, never the lens; loud and proud: brows raised, eyes bright, mouth wide between words; on screen right Tang Xiaotang {TANG}, {GOLD}, standing, framed from the knees up, one sheet of thick opaque plain paper folded twice and held against her chest in both hands, only its plain blank outside showing, her face three-quarter to screen left toward him, never the lens; shy and stirred: eyes lowered, cheeks and ears flushing pink, lips pressed together; behind them only a dark red-brown pillar and the tall lattice windows; {HANDS}; exactly two people",
         lines=[("xuyan", "大人，這帳是我娘子查出來的，一筆一筆都對得上。", "大聲")],
         motion=f"Xu Yan holds his right hand out open, palm up, toward the young woman beside him as he speaks loudly up to the dais; {quiet('Tang Xiaotang', 'her')}; after the last word he keeps his open hand toward her",
         zh="中景、慢推：畫左許硯朝上面的高台、右手攤開朝畫右的唐小棠，提高聲音說；畫右唐小棠兩手把摺好的帳頁按在胸前（只看得到空白的外面），垂下眼睛、耳根一紅（中性臉、嘴閉著）；說完手不收"),
    # The script's over-the-shoulder past Magistrate Hu's hat: Xu Yan alone, looking up at the dais (a back with no picture grows
    # a second man: e918 s19; Hu stays on the dais crop).
    dict(loc="hall_c", cam="Medium close-up, slow push in", chars=["xuyan"], night="hall",
         comp=f"medium close-up of {XU_POUCH}, standing on the stone floor, framed from the chest up with space above his head, his face tipped up toward the high dais above the top of the frame, never the lens; quiet and level: brows level, eyes steady, lips moving softly between words; behind him only a dark red-brown pillar and the tall lattice windows",
         lines=[("xuyan", "大人，那晚從您袖子掉出來的東西，學生還收著。", "平靜，聲音不大")],
         motion="Xu Yan lifts his right hand and pats the left breast of his robe once, lightly, and the corner of dark red silk shows at the edge of his collar; he speaks softly up toward the dais; after the last word his hand stays on his breast and his eyes stay on the dais",
         zh="中近景、慢推（原稿的過肩——胡縣令的官帽與肩在前景——改成許硯單人朝上面的高台：沒有圖的背影會多長一個人，e918 s19；胡縣令只在公案裁切圖上）：許硯抬右手在左胸衣襟上輕輕拍一下，衣襟邊露出一角暗紅綢，小聲平靜地說；說完手還按在胸口、眼睛看高台"),
    dict(loc="dais", cam="Low-angle medium close-up, slow push in", chars=["huxianling"], night="hall",
         comp=dais_shot("alarmed: sweat beading on his forehead under the hat brim, eyes shrinking, brows jumping, mouth tight then wide between words", "his face three-quarter to screen left, his eyes fixed on the chest of the young scholar standing below the dais at the left"),
         lines=[("huxianling", "錢某！人證物證都在，還不從實招來？", "急")],
         motion="Magistrate Hu's eyes shrink on the young man below; in the first second he snatches up the wooden block and brings it down hard on the desk with a loud knock, then turns his face toward screen right and shouts; after the last word he stays leaning forward, sweat on his brow",
         zh="低角度中近景、慢推（公案裁切圖）：胡縣令額頭冒汗，眼睛盯著畫左下許硯的衣襟一縮，第一秒內抓起驚堂木重重一拍，轉頭朝畫右（錢員外，畫外）急急地吼；說完身子還往前傾、額頭冒汗（審稿建議：擦額頭拿掉，6 秒放得下）"),
    # His confession face down (e918 s37: three takes grinned while he begged): nospeak, the recording laid in; the red hands on
    # the stone are the picture.
    dict(loc="hall", cam="High-angle medium shot, slow push in", chars=["qianyuanwai"], nospeak=["qianyuanwai"], night="hall",
         comp=f"high-angle medium shot from in front of him and well above, looking down on him: he kneels on the grey stone floor and leans forward with his forehead lowered almost to the backs of his hands from the first frame, the round crown of his tall black cap in the middle of the frame and its brim toward the camera covering his whole face; both plump hands planted flat on the grey tiles in front of his knees, {RED}, three gold rings on his fingers, his gold sleeves bunched at his elbows; the crown of the cap, his round shoulders and his two hands are all we see of him; around him only the large grey stone tiles; {HANDS}",
         lines=[("qianyuanwai", "是……是我叫賴三燒的，燈籠也是我府上的。", "洩了氣")],
         motion="His shoulders sag lower and his back heaves twice; his orange-red fingers spread on the stone; the crown of his cap stays low over his hands the whole shot",
         zh="【改成臉朝地；審稿必改 4，照第 18 集 fix2 s37 的背影做法：不送錢員外的三張圖、提示詞不點名，只送公堂地面圖，身分句換成一句衣著】高角度中景、從他前上方往下看、慢推：錢員外第一格已經往前傾、額頭低到快碰到手背，高圓帽頂在畫面正中、帽簷朝鏡頭蓋住整張臉；兩隻橘紅的手平貼在膝前的地磚上（金戒指、袖子堆在手肘），只看得到帽頂、圓肩與兩隻手；肩膀一垮、背起伏兩下，手指在地上張開。台詞 nospeak，剪接放錄音（e918 s37 三支求情都露齒笑，認罪這句改成臉朝地說）"),
    dict(loc="dais", cam="Low-angle medium close-up, slow push in", chars=["huxianling"], night="hall",
         comp=dais_shot("hurried and pompous: chin up, brows lifted, eyes darting, mouth drawn long between words", "his face three-quarter to screen right toward Qian Yuanwai off screen right below him"),
         lines=[("huxianling", "錢某縱火，賠銀一百兩；賴三，杖二十！", "官腔，急著結案")],
         motion="in the first second Magistrate Hu raises the wooden block and brings it down flat on the desk with one knock, then speaks fast; after the last word he flicks his left sleeve once toward screen right and looks away",
         zh="低角度中近景、慢推（公案裁切圖）：胡縣令第一秒內舉起驚堂木落下，官腔急著結案；說完朝畫右揮一下左袖、別開眼"),
    dict(loc="hall_c", cam="Close-up, slow push in", chars=["xuyan"], night="hall", act=3,
         comp=f"close-up of {XU_POUCH}, framed from the chest up with space above his head, his face three-quarter to screen right, never the lens; relieved: eyes closed, brows easing, lips pressed together; behind him only a dark red-brown pillar and the soft afternoon light",
         lines=[("xitong", "叮。任務完成。", "冷，宣布")],
         panel=[("任務完成", "task")],
         motion=f"Xu Yan keeps his eyes closed for a moment, breathes out slowly through his nose, his shoulders dropping, then opens his eyes; {SILENT_HE}",
         zh="近景、慢推（身後只有柱子；拍法 11：不寫藍光，面板由剪接疊上）：許硯閉著眼、從鼻子慢慢吐一口氣、肩膀一鬆，再睜開眼；全程嘴閉著（系統畫外）"),
    # Dragged out: only the yamen men's hands on his upper arms; his hands below the frame. A spiteful line, mouth corners down.
    dict(loc="hall", cam="Medium close-up, slow tracking shot to the left", chars=["qianyuanwai"], night="hall",
         comp=f"medium close-up of {QIAN}, framed from the chest up with clear space above his cap, being pulled toward screen left from the first frame by two {BLACK_HANDS} that grip his upper arms from the left and right edges of the frame, only the hands and sleeves of their owners showing, his own arms below the bottom edge of the frame, his body leaning toward screen left; his head turned back over his left shoulder toward screen right, his face three-quarter toward us, never the lens; cold and spiteful: eyes narrowed to slits, brows drawn low, lips closed and pressed thin, one corner of his mouth pulled hard down; behind him only the tall lattice windows and a dark red-brown pillar sliding past; {HANDS}",
         lines=[("qianyuanwai", "你落水那天的事，回去問你許家人。", "回頭冷笑，慢")],
         motion="the black-sleeved hands drag him step by step toward screen left while he keeps his head turned back; first he huffs once through his nose with his lips closed, then speaks slowly; after the last word he presses his lips together, one corner pulled hard down, his eyes still on the young man beyond the right edge of the frame, as he is pulled toward the left edge",
         zh="中近景、往左跟拍：錢員外第一格已經被兩隻黑布袖的手從左右緣抓住上臂、往畫左拖（衙役只拍手；他自己的兩手在畫面下緣外），他扭頭從左肩（靠鏡頭那邊）回望畫右的許硯（畫外）、臉四分之三朝我們，瞇眼、唇抿薄、一邊嘴角往下拉；先閉著嘴從鼻子哼一聲，再慢慢冷冷地說；說完抿嘴、嘴角往下、眼睛還盯著許硯，被拖向畫左緣（審稿必改 5：不寫 sneer，冷笑容易變咧嘴；回頭寫左肩）。胡縣令不入鏡（建議：買 8 秒）"),
    dict(loc="hall_c", cam="Close-up, slow push in", chars=["xuyan"], night="hall",
         comp=f"close-up of {XU_POUCH}, framed from the chest up with space above his head, his face three-quarter to screen left, his eyes following the man being dragged out at the left, never the lens; stunned: eyes fixed and wide, brows drawn together, lips pressed together; one small hand in a light peach-pink silk sleeve reaches in from the right edge of the frame and already holds the edge of his right sleeve from the first frame, only the hand and its sleeve showing; behind him only a dark red-brown pillar and the soft afternoon light",
         lines=[("tangxiaotang", "別聽他的，他就是想讓你家裡先亂。", "小聲")],
         motion=f"Xu Yan's eyes stay on the left; the pink-sleeved hand tugs his sleeve twice, and only then he turns his head toward screen right, toward the owner of the hand; {SILENT_HE}",
         zh="近景、慢推：許硯愣住、眼睛跟著畫左被拖走的錢員外；畫右緣伸進來一隻淡桃粉袖口的小手，第一格就已經拉著他的右袖（唐小棠，只拍手、不送圖）；拉兩下，他才轉頭朝畫右；嘴閉著（唐小棠那句畫外）"),
    # ---- scene 2: outside the yamen, the late afternoon (set-xianya-steps-l2). They come down the steps and walk off to the
    # left (the street); the gate hall is behind them up the steps.
    dict(chapter="縣衙門口", loc="gate", cam="Medium shot, slow push in", chars=["tangxiaotang"], nospeak=["tangxiaotang"], night="gate",
         comp=f"medium shot from behind her right shoulder: {TBACK}, standing on the bottom stone step in the right foreground, framed from the waist up, camera a little above her right shoulder, looking down over it: she holds {SILVERBOX} in both hands in front of her chest from the first frame, its lid raised a finger's width, a soft gleam of silver inside, the box clearly visible past her right shoulder; {only_tang('right')}; beyond her the stone steps and the open gate hall with the big drum, out of focus; {HANDS}",
         lines=[("tangxiaotang", "一百兩，兩錠五十兩的，一分不少。", "小聲，眼睛發亮")],
         motion=f"the young woman lifts the lid a little higher, looks down into the box and closes it again, hugging the box to her chest; {HEADSTILL_TANG}; she looks down at the box the whole shot",
         zh="【改背後拍】中景、從她右肩後拍、慢推（送縣衙門口裁切圖 `set-xianya-steps-l2`：門廳、紅柱、開著的深紅門、鳴冤鼓與石階；整張圖右邊的空紅木架像兵器架，裁掉）：前景右唐小棠的背影，鏡頭在她右肩稍上往下看，第一格兩手已經捧著小木匣（深褐、素面、兩個手掌大）、越過右肩看得清楚；衙役交匣的黑袖手拿掉（審稿必改 17：手要橫過整個畫面，最容易補出整個衙役；交匣交給音效與台詞），她把匣蓋掀高一點看一眼、蓋上、抱在胸前；頭不動、一直低頭看匣子。台詞 nospeak，剪接放錄音（本鏡稿子可以笑，背影看不到）"),
    dict(loc="gate", cam="Medium shot, slow tracking shot backward", chars=["qinshuang", "xuyan"], night="gate",
         comp=f"medium shot walking down the stone steps with them: on screen right Qin Shuang, {QIN}, framed from the waist up with clear space above her head, {SILVERBOX} already tucked under her left arm from the first frame, her face three-quarter to screen left toward the young man beside her, never the lens; grudging and curious: one brow raised, eyes sidelong, lips moving crisply between words; on screen left beside her {XU_POUCH}, framed from the waist up, walking down, his face lowered toward the steps, never the lens; calm: lips closed; behind them the gate hall and the big drum, soft; {HANDS}; exactly two people",
         lines=[("qinshuang", "他拿落水的真相跟你換，你連問都不問。", "挑眉")],
         motion=f"the two walk down one step and another side by side, the camera moving back with them; Qin Shuang glances sidelong at the young man as she speaks; {quiet('Xu Yan')}; after the last word she presses her lips together and looks ahead",
         zh="中景、跟拍（往後退）：畫右秦霜第一格已經把小木匣夾在左臂下，跟畫左的許硯並肩走下石階，邊走邊斜眼看他、挑眉說（稿子：嘴角一點服氣，不算笑）；許硯低頭看台階、嘴閉著（原稿『從唐小棠手上接過木匣』並進第一格）"),
    dict(loc="gate_c", cam="Close-up, slow push in", chars=["xuyan"], night="gate",
         comp=f"close-up of {XU_POUCH}, standing at the foot of the stone steps, framed from the chest up with space above his head, his face three-quarter to screen right, never the lens; steady and sure: brows level, eyes calm, lips moving evenly between words; behind him only the pale stone steps and the red pillar of the gate hall, soft",
         lines=[("xuyan", "問了就欠他人情。公道是公道，不拿來換。", "很穩")],
         motion="Xu Yan stops on the last step and glances back once over his shoulder up at the gate hall, then turns his face to screen right toward Qin Shuang off screen right and speaks; after the last word he gives one small nod",
         zh="近景、慢推（身後只有石階與門廳紅柱）：許硯走下最後一級石階停住，回頭看一眼縣衙門廳，再轉頭朝畫右的秦霜（畫外）很穩地說；說完點一下頭"),
    dict(loc="gate", cam="Medium shot, slow push in", chars=["aling"], night="gate",
         comp=f"medium shot at the foot of the stone steps: A-ling, {ALING}, framed from the waist up with clear space above her head, her hands joined in front of her waist inside her long sleeves, her face three-quarter to screen right toward Xu Yan off screen right, never the lens; quiet and searching: eyes lifted to him, brows drawing together a little, lips moving softly between words; behind her only the pale stone steps and the grey brick wall, soft; {HANDS}",
         lines=[("aling", "你落水的事，真的一點都不想知道嗎？", "很輕")],
         motion="A-ling takes one step toward screen right and lifts her eyes to his face as she asks; after the last word she waits, her lips pressed together and her eyes on him",
         zh="中景、慢推：石階下，阿令（灰白布裙、高髻木簪，兩手在長袖裡交握在腰前）往畫右走一步，抬眼看許硯（畫外），很輕地問；說完抿著嘴等他"),
    dict(loc="gate", cam="Over-the-shoulder medium shot, slow push in", chars=["xuyan"], night="gate",
         comp=f"over-the-shoulder medium shot from close behind one young woman in a plain grey-white cotton dress seen only from behind, appearing only once, in the left foreground, only the back of her head with a high black bun and one plain wooden hairpin and her left shoulder showing, soft; facing us a step away a little right of the middle, {XU_POUCH}, framed from the waist up with clear space above his head, his face three-quarter to screen left looking down at her, never the lens; honest and steady: brows level, eyes serious, lips moving evenly between words; behind him only the pale stone steps and the red pillar, soft; {HANDS}; exactly two people, the young woman in the foreground seen only from behind",
         lines=[("xuyan", "想。所以我要自己查，查到是誰都一樣。", "穩")],
         motion="Xu Yan looks down at her and nods once before he speaks; the young woman in the foreground keeps her head still, the back of her head toward us the whole shot; after the last word he holds her gaze, his lips pressed together",
         zh="過肩中景、慢推：前景左只有阿令的後腦（高髻、木簪）與左肩（不點名、不送圖）；許硯在畫面中偏右低頭看她、點一下頭再說；說完看著她、抿嘴"),
    dict(loc="gate_c", cam="Close-up, slow push in", chars=["xuyan"], night="gate",
         comp=f"close-up of {XU_POUCH}, standing at the foot of the stone steps, framed from the chest up with space above his head, his face three-quarter to screen left, never the lens; caught by surprise: eyes widening, brows lifting, lips pressed together; behind him only the soft pale stone steps and the gate hall",
         lines=[("xitong", "叮。唐小棠加六，秦霜加五，阿令加二。三人好感，突破二十。", "冷，宣布")],
         panel=[("唐小棠 好感 +6 → 24", "panel"), ("秦霜 好感 +5 → 23", "panel"), ("阿令 好感 +2 → 21", "panel"), ("三人好感，突破二十", "panel")],
         motion=f"Xu Yan stops in mid-step and his eyes go to a point in the air just in front of him, then move slowly across it from left to right; {SILENT_HE}",
         zh="近景、慢推（身後只有虛焦的石階與門廳；原稿『身後虛焦是三位妻子』拿掉，免得多出人）：許硯腳步一停，眼睛看向面前空中一點、再從左慢慢移到右；全程嘴閉著（系統畫外，三行面板加一行同一個面板）"),
    # Xu Yan may laugh here (script).
    dict(loc="gate_c", cam="Close-up, slow push in", chars=["xuyan"], night="gate",
         comp=f"close-up of {XU_POUCH}, framed from the chest up with space above his head, his face three-quarter to screen left, his eyes on a point in the air in front of him, never the lens; amazed: eyes wide, brows high, lips closed; behind him only the soft pale stone steps and the gate hall",
         lines=[("xitong", "獎勵：製糖法、隊列操練法、鴨群治蝗法。", "冷，宣布"),
                ("xuyan", "鴨子……治蝗？鴨子能吃蝗蟲？", "念出來，笑出聲"),
                ("xitong", "宿主覺得好笑，可以不要。", "冷，毒舌")],
         panel=[("獎勵：製糖法、隊列操練法、鴨群治蝗法", "reward")],
         motion="For the first four seconds Xu Yan's lips stay pressed together while his eyes grow wider; from the fourth to the eighth second he bursts out laughing and speaks the line through the laugh; from the eighth second he claps the back of his right hand over his mouth and keeps it there to the last frame, his eyes still creased",
         zh="近景、慢推（拍法 11：不寫金色光點，面板由剪接疊上）：前四秒（系統念獎勵）許硯眼睛越睜越大、嘴閉著；第四到第八秒噗地笑出聲、邊笑邊說（本鏡可以笑）；第八秒起用右手背擋住嘴到最後一格（系統吐槽）、眼睛還笑著（長鏡；審稿必改 11：寫第幾秒開始說）"),
    dict(loc="gate_c", cam="Close-up, slow push in", chars=["xuyan"], night="gate",
         comp=f"close-up of {XU_POUCH}, framed from the chest up with space above his head, the back of his right hand still pressed over his mouth from the first frame, his face three-quarter to screen left, never the lens; his eyes still creased with laughter; behind him only the soft pale stone steps and the gate hall",
         lines=[("xuyan", "要，三樣都要，連鴨子也一起要。", "心裡話，正經起來", "inner"),
                ("xitong", "主線任務開啟：天下歸心，百分之零。", "冷，宣布")],
         panel=[("主線任務開啟：天下歸心，百分之零", "task")],
         motion=f"Xu Yan lowers his hand, gives one small cough into his fist and straightens his face: brows level, eyes steady, lips pressed together; then his eyes widen slightly at a point in the air in front of him; {SILENT_HE}; he is thinking, not speaking",
         zh="近景、慢推：許硯第一格右手背還擋在嘴上，放下手、對著拳頭輕咳一聲、正經起來（眉平、眼穩、抿嘴），再對著面前空中一點眼睛微微一睜；全程嘴閉著（心裡話與系統都畫外）（長鏡）"),
    # Tang Xiaotang's line from behind her, then his on screen; he may smile a little (script).
    dict(loc="gate", cam="Over-the-shoulder medium shot, slow push in", chars=["tangxiaotang", "xuyan"], nospeak=["tangxiaotang"], night="gate",
         comp=f"over-the-shoulder medium shot from close behind {TBACK}, standing in the left foreground and leaning toward the young man; {only_tang('left')}; facing us a little right of the middle, {XU_POUCH}, framed from the waist up with clear space above his head, his face three-quarter to screen left toward her, never the lens; caught out and amused: one brow raised, eyes bright, lips closed; behind him only the pale stone steps and the gate hall, soft; {HANDS}; exactly two people, the young woman in the foreground seen only from behind",
         lines=[("tangxiaotang", "你一個人對著空氣笑什麼？", "狐疑"),
                ("xuyan", "沒什麼，想到以後要養很多很多鴨子。", "輕鬆")],
         motion=f"For the first two and a half seconds Xu Yan's lips stay closed while the young woman leans in; {HEADSTILL_TANG}; {GAZE_HIM}; from the third second he waves his right hand once and speaks lightly; after the last word he turns his shoulders toward screen left to walk on",
         zh="【改背後拍】過肩中景、慢推：前景左唐小棠的背影往許硯湊（頭不動、一直看著他）；許硯在畫面中偏右，前兩秒半嘴閉著（唐小棠那句 nospeak 放錄音），第三秒起擺一下右手、輕鬆地說（本鏡可以笑一下）；說完肩膀轉向畫左要往前走（長鏡）"),
    # Review 必改 6: Qin Shuang alone (four people would be four named faces, bible rule 1, and Tang Xiaotang would vanish
    # between s36 and s37); the others are off screen right, behind her.
    dict(loc="gate", cam="Medium full shot, slow tracking shot to the left", chars=["qinshuang"], night="gate",
         comp=f"medium full shot at the foot of the stone steps: Qin Shuang, {QIN}, framed from the knees up with clear space above her head, {SILVERBOX} tucked under her left arm from the first frame, walking toward screen left, her head turned back over her left shoulder toward screen right, toward the others coming down the steps behind her beyond the right edge of the frame, never the lens; brisk: brows level, lips moving crisply between words; behind her only the pale stone steps and the gate hall, soft",
         lines=[("qinshuang", "走吧，天黑前要回到村裡，銀子我抱著。", "催")],
         motion="she calls back over her left shoulder, then faces front and quickens her pace toward screen left",
         zh="中全景、往左跟拍（審稿必改 6：改成秦霜單人）：石階下，秦霜左臂第一格已經夾著小木匣往畫左走，回頭從左肩（靠鏡頭那邊）朝畫右外催一句（許硯、唐小棠、阿令在她身後畫外），再轉回前面、加快腳步往畫左。原稿四個人；一鏡最多三張臉（拍法 1），唐小棠也不會在 s36 之後憑空不見"),
    # ---- scene 3: the roof at night (set-wuding-eave-l2 for s38; s39-s41 no roof picture). Tang Xiaotang sits on the right facing left; Xu Yan comes up the ladder
    # at the left and sits an arm's length to her left, facing right.
    dict(chapter="屋頂", loc="roof", cam="Low-angle wide shot, slow push in", chars=["xuyan", "tangxiaotang"], night="roof",
         comp=f"low-angle wide shot up the long slope of plain dark grey tiles, the two bamboo poles of the ladder top at the bottom left: on screen right, high on the slope just below the ridge line, Tang Xiaotang {TANG}, {GOLD}, sitting on the tiles with her arms wrapped round her knees, framed full length, small, her face three-quarter to screen left toward the young man, never the lens; quiet and downcast: eyes lowered, lips closed; on screen left {XU_COAT}, framed full length, small, already stepping off the top of the ladder onto the tiles from the first frame, bent low, his face three-quarter to screen right toward her, never the lens; gentle and teasing: one brow raised, lips moving lightly between words; {HANDS}; exactly two people",
         lines=[("xuyan", "大半夜坐在屋頂上，十本帳又不對了？", "輕，逗她")],
         motion=f"Xu Yan walks bent low up along the tiles toward her and sits down an arm's length to her left, then speaks; {quiet('Tang Xiaotang', 'her')}; she keeps her arms round her knees",
         zh="低角度全景、慢推（送屋頂裁切圖 `set-wuding-eave-l2`（審稿必改 15：l1 下緣有字形浮雕的瓦當切掉）：一大片灰瓦斜坡、屋脊從左上角斜到右緣中間、左下竹梯兩根頂端、右上夜空；整張圖右邊結滿橘柿的柿子樹與正中的滿月不在，月亮寫在畫右上外；不寫『屋簷瓦在前景』）：畫右高處、屋脊線下方唐小棠抱膝坐著（中性臉、嘴閉著）；畫左許硯（披舊灰外衣）第一格已經從竹梯頂踏上瓦片，彎著腰走過去、在她左邊一臂外坐下，再輕輕逗她"),
    dict(loc="roof_c", cam="Over-the-shoulder medium shot, slow push in", chars=["tangxiaotang", "xuyan"], nospeak=["tangxiaotang"], night="roof",
         comp=f"over-the-shoulder medium shot from close behind {TBACK}, sitting on the tiles in the right foreground with her arms wrapped round her knees and her chin resting on them; {only_tang('right')}; facing us an arm's length away a little left of the middle, {XU_COAT}, sitting on the tiles, framed from the waist up with clear space above his head, his face three-quarter to screen right toward her, never the lens; listening: brows lifting a little, eyes on her, lips closed; behind him only the dark tiles and the black night sky; {HANDS}; exactly two people, the young woman in the foreground seen only from behind",
         lines=[("tangxiaotang", "十本帳早對完了。今天堂上，你說帳是我查的。", "很輕")],
         motion=f"the young woman presses her chin down onto her knees and draws them in closer; {HEADSTILL_TANG}; {GAZE_HIM}; {quiet('Xu Yan')}; his eyes soften",
         zh="【改背後拍】過肩中景、慢推（不送屋頂圖，審稿必改 15）：前景右唐小棠的背影（兩顆高丸子、後頸露出），抱膝、下巴擱在膝上，把膝蓋抱緊（原稿『搖搖頭』不拍：一轉頭就露臉，e914 s24）；對面一臂外許硯坐著看她、嘴閉著、眼神放軟。台詞 nospeak，剪接放錄音"),
    dict(loc="roof_c", cam="Medium close-up, slow push in", chars=["xuyan"], night="roof",
         comp=f"medium close-up of {XU_COAT}, sitting on the tiles, framed from the chest up with space above his head, leaning back on both hands planted on the tiles behind him, his face tipped up three-quarter to screen right toward the moon beyond the upper right of the frame, never the lens; easy and plain: brows relaxed, eyes calm, lips moving evenly between words; behind him only the dark tiles and the black night sky",
         lines=[("xuyan", "本來就是妳查的，我只是當著大家說了實話。", "平平地")],
         motion="Xu Yan leans back on his hands and looks up at the moon as he speaks; after the last word he keeps looking up, his lips pressed together",
         zh="中近景、慢推（原稿的過肩改成許硯單人，跟 s39、s41 的過肩分開）：許硯兩手撐在身後的瓦上，抬頭看畫右上外的月亮，平平地說；說完還看著月亮、抿嘴"),
    dict(loc="roof_c", cam="Over-the-shoulder medium close-up, slow push in", chars=["tangxiaotang", "xuyan"], nospeak=["tangxiaotang"], night="roof",
         comp=f"over-the-shoulder medium close-up from close behind {TBACK}, sitting in the right foreground hugging her knees tight, soft, her chin resting on her knees from the first frame to the last, the back of her head and the two high buns still; {only_tang('right')}; beyond her an arm's length away a little left of the middle, {XU_COAT}, sitting on the tiles, framed from the chest up with space above his head, his face tipped up three-quarter to screen right toward the moon at first, never the lens; lips closed; behind him only the dark tiles and the black night sky; {HANDS}; exactly two people, the young woman in the foreground seen only from behind",
         lines=[("tangxiaotang", "小棠問你一句……若有人來帶我走，你會讓嗎？", "聲音發緊")],
         motion=f"the young woman hugs her knees tighter, her chin pressed down on them; {HEADSTILL_TANG}; {GAZE_HIM}; halfway through her words Xu Yan turns his head from the moon to her and his eyes widen, his brows drawing together; {quiet('Xu Yan')}; after the last word he holds her gaze",
         zh="【改背後拍】過肩中近景、慢推（從中近景推到近景；不送屋頂圖，審稿必改 15）：前景右唐小棠的背影抱緊膝蓋、下巴從第一格到最後一格都擱在膝上（審稿必改 18；頭不動、看著他；原稿『轉頭看他』不拍）；對面許硯先抬頭看月亮，聽到一半轉頭看她、眼睛一睜、眉頭一皺；嘴閉著。台詞 nospeak，剪接放錄音（結尾，懸念：第 20 集第一鏡許硯回答）"),
]

HEAD = [
    "- 重製版 r2、真人版（站主 2026-11-11「之後都用真人版」）：照 `docs/videos/zhong-tian-qu-qi-e019-r2/script.md`（c01–c41 對應 s01–s41；2026-11-06 的 r2 稿；含「這版改了什麼」「2026-11-06 審稿後的修改」與「真人版的改動（2026-11-16）」）；台詞一字不改，只改拍法；每鏡一個看得見的動作、一句一筆不拆半句、預設不笑。篇章設定 `production/r2-bible-e011-e020.md`（拍法 1–18 條）。",
    "- 內部工作編號 919（`hailuo/{ff,clips}-dh-e919.json`、`colab/runs/e919/extras.json`、`colab/runs/e919-live/spec.json`，工作資料夾 `~/mokaair-work/videos/zhong-tian-qu-qi-e919-dh/`）；發布 slug `zhong-tian-qu-qi-e019-r2`。不放集數、不放片名卡；s01 接第 18 集 s40（fix1 重拍後的狀態：畫面在兩人手肘之上、錢員外左臂整條包在金綢袖裡搭在許硯右上臂、高圓頂平滑黑帽）。",
    "- 照第 18 集審稿後的寫法與第 18 集挑片的教訓一開始就照做：`OFFSCREEN_SPEECH = False`；背景寫在場的東西；道具寫在第一格、在主人那隻手；兩人接觸寫成第一格就已經的狀態（s01、s04、s10、s12、s26、s27、s28）；紙只拍空白的背面或摺著（s18、s20），帳冊合著、素封面；不用手指指人（s14、s20 攤開手掌）。",
    "- **唐小棠不露嘴說話**：她五句在畫面上的台詞（s18、s28、s36、s39、s41）從背後拍（nospeak，spec 拿掉她三張臉部參考圖與身分句；兩顆高丸子各繞一條短粉緞帶、後頸露出，每鏡一個固定視線、頭不動）；s19 念帳那句改成錢員外聽的臉、她在畫外；s27 只拍她的手。她不說話的臉（s06、s07、s20、s38）用第 7 集的中性外貌句。",
    "- **錢員外**：高圓頂平滑黑帽、圓領（照定妝照；spec 換掉 cast 的 small cap、cross collar）。s12 以前兩手縮在袖裡、不入鏡（spec 拿掉金戒指）；**s12 袖子第一格已經堆在手肘、兩手已經橘紅**（紅寫成狀態），之後兩手藏在背後（s15、s17、s19）或在畫外（s26），露手的只有 s12、s13、s23。**s23 認罪臉朝地**（nospeak；第 18 集 s37 三支求情都露齒笑；審稿必改 4：不送錢員外的圖、不點名，前上方往下拍、帽簷蓋住整張臉）。他其他的台詞都是生氣、嘴硬、冷笑，每鏡寫嘴角往下。胡縣令與錢員外不同框。",
    "- **不拍兵器、不拍衙役與圍觀的人**：秦霜腰帶空著；衙役只拍黑布袖的手、人在畫外（s12 抓住前臂、s26 拖走；s28 交木匣只留音效與台詞，審稿必改 17），『威武』與打板子只留音效；驚堂木是扁長方的木塊；圍觀縣民只在 s08 下緣兩個包頭的背影。",
    "- 場景（協調者 2026-11-16 決定，每張放大看過）：側廳 `set-xianya-ceting-l1`（s01–s03）；公堂地面 `set-xianya-gongtang-floor-l1`、胡縣令 `set-xianya-gongtang-dais-l1`（第 18 集的兩張裁切圖；地面鏡不寫 magistrate）；手部插鏡 s11、s13 不送場景圖、只送手的主人定妝照領口以下的袖口裁切（`laisan-sleeve-l1`、`qianyuanwai-sleeve-l1`，沒有臉；審稿必改 3）；**新的免費裁切圖**（`refs-live/README.md`）：縣衙門口 `set-xianya-steps-l2`（整張 `set-xianya-l1` 右邊的空紅木架像兵器架，裁掉；審稿後再把鼓架後有字形筆畫的紅方塊塗黑；s28–s37）、屋頂 `set-wuding-eave-l2`（整張 `set-wuding-l1` 右邊結滿橘柿的樹與正中的滿月裁掉；審稿後重裁、切掉有字形浮雕的瓦當；只給 s38，s39–s41 不送屋頂圖）。錢員外帽後有結的側面角度圖整集不送（審稿必改 13）。都由 spec 的 `swap_pictures` 用絕對路徑換進去（`gen-dh.mjs` 不加行）。**不用試鏡**。",
    "- 長鏡要買的秒數（BUY）：照 45 句錄音核過（`~/mokaair-work/videos/zhong-tian-qu-qi-e919-dh/audio`，faster-whisper 一次一支逐句聽寫；見 `r2.py` 的 BUY 註解）：**s05（胡縣令拖長官腔的「升堂」約 8 秒，加拍案）、s12（胡縣令畫外加錢員外：人聲 9.4 秒、檔長 10.5 秒，剪接把 a11 提前到 s11 尾巴約 1.3 秒）、s34（系統、許硯、系統三句約 9.9 秒，一支裝得下、不拆）買 10 秒**；s02、s06、s16、s17、s19、s23、s24、s26、s35、s36、s38 買 8 秒（s17、s26 是審稿建議）；其餘 6 秒。",
    "- **表上的「秒」欄是 lint 估法**，比錄音短；剪接以錄音長度＋0.5 秒為準。",
]
FOOT = [
    "- **參考圖**（`assets/refs-live/`）：許硯、唐小棠（l1 交領）、秦霜、阿令（l1，高髻木簪；不用散髮角度圖）、賴三、錢員外（l1＋角度圖）、胡縣令的 l1。場景見上面。",
    "- `gen-dh.mjs`、`build-r2.py`、`cast.json` 都不改（`county yamen` 對到 `set-xianya`、`roof of the farmhouse` 對到 `set-wuding`；側廳、公堂、門口、屋頂由 spec 的 swap_pictures 換圖）。",
    "- `colab/runs/e919/extras.json`（照 e918：畫面不放字幕、空氣清澈那句；拿掉秦霜的柴刀；胡縣令的官帽官袍照 e910–e912 的寫法、拿掉『笑起來臉頰會抖』）與 `colab/runs/e919-live/spec.json`（`mkspec.py` 產生；種子 9191101／9191102）。",
    "- 免費準備：`prep919.sh`（`DRY=1 REFS=~/mokaair-work/videos/zhong-tian-qu-qi-e919-dh/runpod/refs-dh-e919 VIDEO_JSON=docs/videos/zhong-tian-qu-qi-e019-r2/video.json st1-ep.sh 919` → `pilot.py runpod/a/st1 runpod/live/st1 s01…s41` → `retake.py runpod/live/st1 runpod/live/d1 colab/runs/e919-live/spec.json` → `colab-jobs.json` 加 output_path、套 swap_pictures（絕對路徑）→ 查每張參考圖都是絕對路徑、每鏡送的場景圖照計畫 → `preflight-prompts.py` → 否定名詞掃描與會長字的名詞掃描（writing 等））。",
    "- 配樂：公堂沉的鼓、越審越密（s13 兩雙紅手一個重音、s23 認罪一個大重音、s25「叮」、s26 冷笑那句底下換低的弦）；縣衙門口鬆下來的暖曲（s33 三人好感一個亮的重音、s34 鴨子那句停一拍）；屋頂安靜的古箏（s41 問句停一拍）。音效表見 script.md〈音樂與音效〉（s04『威武』低聲與 s24 之後的打板子只有聲音，人不入鏡；s28 木匣、銀錠輕響）。",
]

# Long shots: seconds to buy. Measured 2026-11-16 against the 45 recordings (~/mokaair-work/videos/zhong-tian-qu-qi-e919-dh/audio;
# wave length and silencedetect -35 dB; e013's test: a shot holds (buy - 0.3) x 1.1 s of speech, half a second between lines,
# so 6 s holds 6.27 s, 8 s 8.47 s and 10 s 10.67 s). faster-whisper medium read every take back, one clip per process
# (scratchpad fw919.txt; see the notes after BUY).
# 10 s: s05 (a05 8.56 s, Magistrate Hu's drawled 升堂 with a 0.9 s pause, 7.96 s of speech, after the knock in the first second);
#       s12 (Hu off screen a11 4.37 s of speech + 0.5 + Qian Yuanwai a12 5.00 s = 9.87 s; the script's 8 s does not hold it);
#       s34 (system a34 3.29 + Xu Yan a35 3.95 + system a36 1.70 + 2 x 0.5 = 9.94 s; one clip, no split needed).
# 8 s:  s02 (a02 6.25 s of speech, 6.84 s with the edges: over 6.27), s23 (the retake a23 7.21 s of speech, nospeak),
#       s16 (a16 6.52 s file; the script's long shot: unwrap, set down, stand), s19 (a19 6.41 s of speech), s24 (a24 6.35 s
#       of speech after the knock), s06 (a06 4.97 s of speech after the bow), s35 (a37 2.93 + 0.5 + a38 2.68 = 6.11 s after
#       the hand comes down), s36 (a39 1.92 + 0.5 + a40 3.18 = 5.60 s, the script's long shot: she leans in first),
#       s38 (a42 2.58 s, after he walks up the tiles and sits down).
#       s17 (review 建議: a17 is a 6.32 s file, speech 0.00-6.09 s at -40 dB, after a glance at the floor), s26 (review 建議:
#       a26 with the cold huff 5.46 s, then he is pulled to the left edge).
# 6 s:  every other line (1.72-5.6 s files; the tightest s15 a15 5.16 s of speech; s22 lost its forehead wipe, review 建議).
# Re-recorded once (audio/README-retakes.txt; first takes in audio/take1/): a15 (染布 heard 短不), a23 (燈籠 heard 登老), a41
# (銀子 heard 因此, a different meaning), a43 (說帳 heard 說這樣); a42 read 十本帳 as 審章 (take1, kept) and 是不是 (retake,
# take2/); after the review (必改 16) two more takes with the same words and only pauses in the input: take4
# 「大半夜坐在屋頂上……十本帳，又不對了？」 (5.48 s) reads 十本帳 whole and in its 2.0-5.48 s piece and is now zq919a42.wav
# (take1 moved to take1/, take3 to take3/); a human ear still checks it before the cut. a38 (system 主線 heard 首先 after the 1.3x post; the raw take reads right, a
# 1.2x re-process reads 主席) keeps the season's 1.3x. The rest are homophones or tone guesses of whisper.
BUY = {"s02": 8, "s05": 10, "s06": 8, "s12": 10, "s16": 8, "s17": 8, "s23": 8, "s19": 8, "s24": 8, "s26": 8, "s34": 10, "s35": 8,
       "s36": 8, "s38": 8}
