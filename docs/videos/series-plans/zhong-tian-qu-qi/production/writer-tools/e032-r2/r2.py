"""Episode 32 remake (r2): the writer spec for ../e001-r2/build-r2.py. Source: docs/videos/zhong-tian-qu-qi-e032-r2/script.md
(c01-c37; the CG-era r2 script), including its sections 「這版改了什麼」 and 「2026-11-06 審稿後的修改」, which override the tables.
Every line is the script's, word for word; only the staging changes. c25 and c26 (three and two recordings: system lines and
Xu Yan's thoughts, about 11 s and 9 s) are split into s25/s25b and s26/s26b (as e031 c29): 39 shots.
Bible: production/r2-bible-e031-e040.md (arc 4 〈旱年〉: rules 1-43, 〈場景〉, 〈接點〉 31->32 as corrected 2026-11-17 to the flipped
dam, 32->33, the props, people, 〈小角色〉 and 原版必修 tables) and r2-bible-e011-e060.md (accounts: Qin Shuang +12 -> 41, the
first time over forty, the reward box: the waterwheel drawing; the drought quest's third day). The second episode of arc 4:
the dam upstream on the first afternoon of the quest (the same moment as e031 s41), the row of well pits on the third
morning and that evening, the ancestral hall at dusk.

Written from the start the way e031-r2/r2.py stands AFTER its independent review (../e031-r2/review.md: the 7 必改 and the
建議 the coordinator took), with the task file's lessons:
- OFFSCREEN_SPEECH = False (rule 15): every shot with an off-screen line, a thought or a system line writes the silence of
  each face on screen (quiet(), SILENT_HE).
- Rule 31: a line said to someone outside the frame is written "toward someone out of sight beyond the left/right edge of the
  frame", that side set only all the way to the edge, and the speaker the only person in the frame (off()); GAZE_REFINE puts
  the same direction into the refine text. Nobody who is not in the first frame is named or described anywhere: the twelve
  retainers appear only in s01 (far, on the crest), never in a close shot (rule 34); Tang Xiaotang, Qin Shuang's home, the
  village children outside the hall are never written. A look at a place names the place (the dam, the pit, the doorway,
  the tablets, the way ahead). Over-the-shoulder foregrounds are unnamed backs with no picture (rule 2).
- Tang Xiaotang is not in this episode (the script: 唐小棠留在田裡), so no back-shot wording; live_clips() keeps e031's
  structure and finds nothing of hers to change.
- Qin Shuang (bible 〈人物〉, 31->32): her chopper is NOT written (rule 5: the CG script's 「柴刀插腰帶右邊」 goes in every
  shot); the carrying pole she takes from a villager (POLE) s01-s09, given back before s10's first frame; the bamboo water
  tube (TUBE) s17-s19; Xu Yan over her right shoulder s23-s26b; her ears flushed red from s24 (rule 12: the whole ear, no
  dots).
- Wang Erniu (原版必修 e031 and e032: laughing at bad news, a red glow on his shoulder): not smiling in every shot (brows
  knotted, panting, jaw set); his face "tanned dark", not "flushed red" (e031's ERNIU), so nothing red is written near him;
  the only hoe in scenes 1 and 3 is his (HOE); in scene 2 he has no hoe (he holds the rope).
- The villagers (rule 34): at the dam and at the pits the same five people as e031 (VILLAGERS: hemp-beige, charcoal, faded
  indigo, dull olive, dark grey; never grey-blue), no hoe among them; in the hall eight people, each a different colour,
  age and sex (CT_VILLAGERS), none in the leads' colours, no red-string pigtails (little Xiaohe's).
- Elder Han (hanbo-portrait-l1: white topknot with a pin, long white beard, faded grey robe; no angle picture) and Carpenter
  Shi (shimujiang-portrait-l1: grey topknot with a plain wooden stick through it, not 「耳後墨線筆」, as e013-e017 wrote it;
  leather apron; no angle picture) in e015-e017's wording (HAN, CARP).
- One visible action per shot (rule 32); the previous action done in the first frame; the hand's action in a frame where it
  is seen; hand gestures with the flat hand, fingers together (c03's and c06's pointing, c31's 「往頭頂上一指」 are a flat
  hand or a turn of the head). The script's follows and tracks are slow push-ins. No word "open" (rule 36: the reward box is
  only the panel; Xu Yan's eyes "open a narrow crack" is written "his eyelids part"). Nothing hung (rule 33).
- 原版必修 e032 (bible): no head growing out of the ground (the pits are written empty: nobody stands in a pit; s16 is an insert of
  his two hands and the pick at the bottom of the shaft, no face (review 必改 2); the villagers stand full figure on the field); Erniu never smiles; Xu Yan is never seen
  climbing out: s20 is the rope hauled taut (he is not in the frame), s21's first frame already has him lying on the earth,
  eyes half closed. No waterwheel anywhere (the drawing is only the panel and a rolled sheet, plain side out, rule 38).
- No blue light (rule 11): s25-s26's panels are the editor's; the script's 「臉被面前的淡藍光照亮」 is not written.

THE AXES (rules 29, 42: the pictures decide):
- Scene 1, the dam (set-shangyou-ba-fx-l1, the flipped pick, exactly as e031 s32-s41 wrote it): the bank of round brown hemp
  sacks from the right foreground away to the far left, the muddy pond behind it on the right, the narrow stone-edged path at
  its left foot, a muddy ditch and a strip of green rice further left, bamboo hills. The Liuxi side is on the LEFT on the
  path, the dam on the RIGHT (bible 31->32). The hand-over (e031 s41): Erniu from behind in the lower left on the path, the
  hoe raised (as shot, 9311101: the retainers, about fourteen, stand in the pond's shallow water beyond the bank). s01 keeps that camera; Qin Shuang is already at his
  RIGHT (between him and the bank: 「站到兩幫人中間」) and the hoe flies off to the LEFT, where Xu Yan picks it up in s04. From
  s02 on, left to right on the path: Xu Yan, Erniu, Qin Shuang; Qin Shuang faces screen left (to them, her back to the dam),
  Xu Yan and Erniu face screen right; s03 Erniu looks right (to her), s06 left (to Xu Yan); s09 Xu Yan looks right (to her).
  s10 the group walks toward us down the path (the ditch flows toward us: downstream, to the village, is behind the camera).
- Scene 2, the pits (set-jingkeng-l1, round-2 pick 37040): one row of earth heaps from the near left away to the far right
  across cracked furrows (the script's 「從前左排到後右」), the near pit in the left foreground the nearest and clearest (a dark
  square mouth, a long wooden pole along its far rim, a wooden tub on its edge; a second open brick pit just right of the tub,
  review 建議), a golden willow at the right, roofs and hills far away, a low sun from the LEFT. So Xu Yan's pit is the NEAR one
  (the script's 「中間那一口」 changes). Xu Yan at the pit (left); Elder Han, Erniu and Qin Shuang come from the right along the row and stand at his
  right; Qin Shuang carries him off to the LEFT (the village roofs are at the far left). The picture's light is golden, so the
  morning (s11-s15) gets the free dawn versions (jingkeng_chen.sh: -chen, -kou-chen, -dui-chen; review 必改 1) and JM names no
  direction; the evening (s16-s26b) keeps the golden pictures and the low orange sun from the left; the time jump is
  the cut s15->s16, not a light change inside s16 (the original's c21 light jump was a 必修).
- Scene 3, the ancestral hall at dusk (set-citang-huang-l1: set-citang-l1 with the doorway's daylight turned to dim orange
  dusk and the beam's crack strokes painted out, citang_huang.py): the pair of lattice doors on the LEFT, the altar table with
  five plain tablets, the censer and two candles on the RIGHT, the dark main beam across the top of the back wall. There is no
  outside picture of the hall, so the script's 「門前三級石階」 scene (c27-c31) is played just inside the doorway (Han Bo:
  「你們在門口說的，我都聽見了」 still holds). The kneeling villagers face the altar (right), their backs to us; when they turn
  they look screen LEFT to the doorway, where Xu Yan stands (bible 32->33).

PLACES (gen-dh SET takes the FIRST pattern in its list order that matches; spec.json will swap with absolute paths):
- "stream" (scene 1: B0) gives dh-set-liuxi-he-t1, swapped for set-shangyou-ba-fx-l1 (s01) and its e031 crops: -fx-lu (s02,
  s04, s07, s08, s10), -fx-shan (s03, s06), -fx-jiao (s05), -fx-ding (s09).
- "well pit" (scene 2) gives dh-set-jingkeng-t1 (before "stream" and "willow" in SET), swapped at dawn for set-jingkeng-chen-l1 (s11),
  -kou-chen (s12, s14, s15), -dui-chen (s13) (jingkeng_chen.sh), at dusk for set-jingkeng-l1 (s20) and the free crops
  (jingkeng_crops.sh): -kou (s17-s19, s22), -dui (s23, s25), -tian (s24, s26, s26b), -di (s21). s16 and s25b are inserts with
  no picture at all: mkspec.py drops their place sentence from d1 (as e031 s18/s21) and spec.json sends nothing.
- "ancestral hall" (scene 3) gives dh-set-citang-t1, swapped for the free set-citang-huang-l1 (s36) and its crops
  (citang_huang.sh): -men (s27, s28, s30, s31, s37), -qiang (s29), -liang (s32), -tang (s33), -zuo (s34), -zuo2 (s35)
  (the left end of the altar table, review 必改 6; -zhuo is not sent).
No "spring field", "sluice", "channel", "pool", "courtyard", "yard" in any prompt (other SET rows).
Shared files: none changed (build-r2.py's EN has "Qin Shuang", "Wang Erniu", "Elder Han", "Carpenter Shi"; gen-dh.mjs,
pilot.py, cast.json untouched). The d1 prep (colab/runs/e932/extras.json, colab/runs/e932-live/{mkspec.py,spec.json}, the
scratchpad's prep932.sh and e932d1.sh) was written 2026-11-18 after the independent review (colab/runs/e932-live/PREP.md).

RECHECKED 2026-11-18 against e031 s41 as picked (colab/runs/e931-live/picks-merged.tsv: 9311101, 0-3.833; the refined clip
looked at at 0, 1.5, 3.0 and 3.8 s): Erniu's back fills the lower left quarter, cut at the hips, turned a little away to the
right, the hoe high over his head with its handle slanting to the upper left and the blade at the left edge; the retainers
are not on the crest but stand in one row in the pond's shallow water beyond the bank, from just right of the middle away to
the left, about fourteen (13-15), three-quarter to screen left toward him, black jackets, white leg wraps, staffs upright at
the cut. s01 is rewritten to that frame (RETAINERS_S01, fourteen; exactly sixteen people).

AFTER THE INDEPENDENT REVIEW (writer-tools/e032-r2/review.md, 2026-11-18; the coordinator took all 6 必改 and these 建議):
必改 1 dawn pictures + JM without a direction; 2 s16 a no-picture insert of the hands and the pick; 3 s20 (now the whole
set-jingkeng-l1), s23, s36 at the pictures' camera height, s25 likewise; 4 s19/s20 Erniu in front at the pit, Qin Shuang
behind him facing left; 5 s26/s26b behind him the willow, as the picture; 6 s34/s35 at the left end of the altar table
(-huang-zuo, -huang-zuo2). 建議: s25 a faceless wide shot and s25b an insert of his hanging hand (four upside-down faces become
two); s05/s26 buy 8 s; s11's refine gaze on the heaps; s18 names the right side; s01's hoe sticks blade first; s26b not
smiling; s32 level at eye height; s36's near row cut at the knees; the hall's old woman in deep plum and a lean charcoal man
instead of the little boy (e033 c05 needs men on the rope); Carpenter Shi in light tan (the portrait); -huang-men's doorway
written as a passage and another lit lattice door, not sky.
"""
EP = 932  # internal working number; the published slug is zhong-tian-qu-qi-e032-r2
SLUG = "zhong-tian-qu-qi-e032-r2"
EP_TITLE = "挖井挖到昏倒（重製版 r2）"
OUTLINE_SECONDS = 210  # script.md: about 210.5 s, 37 shots (10 + 16 + 11)
TARGET_MINUTES = [3, 4]
TITLE = "挖井挖到昏倒｜種田娶妻打天下 第32集（重製版）"
DESCRIPTION = "二牛的鋤頭還沒落下，秦霜一扁擔把它挑飛：打了，就是給錢家藉口。深潭的水在溝底、田在坡上，挑不活三畝田——那就挖井，挖到見水為止。第三天，十幾口井一口都沒見水，許硯自己綁繩下井，挖了一整天，被拉上來時滿臉是泥，只說得出「沒水」。秦霜扛起他就走，一路罵文弱書生，耳根卻紅了：好感突破四十，獎勵箱開啟——水車圖紙。可水車要三百斤的整木，村裡只剩祠堂頭頂那一根梁。韓伯帶全村跪下：拆祠堂的梁，給孩子換一口水——《種田娶妻打天下》第 32 集（重製版）。"
THUMB = ("文弱書生", "s23")
CHARACTERS = ["xuyan", "qinshuang", "erniu", "hanbo", "shimujiang", "xitong"]
MINOR = {}
MUSIC = "one cue per scene: a low dry drum at a dam in a bamboo valley, one heavy accent as a hoe is knocked flying, then steady low strings; then a pale dry drone at dawn by a row of dug pits, a low heartbeat drum as a rope is hauled, turning to a gentle slightly comic cue as a woman carries a man off on her shoulder, one bright accent as a reward box is announced; then a deep low cello in a candle-lit ancestral hall at dusk, one heavy note at the sight of the roof beam, one drum beat under an old man's vow, holding at its peak; ancient Chinese rural drama, no vocals"

# Places.
B0 = "In the bamboo valley upstream of the dry Liuxi stream on the first afternoon of the drought, at the Qian family's dam"
DAM = ("a long rough bank of stacked brown hemp sacks of earth on a footing of rough fieldstones, running from the right "
       "foreground away to the far left of the valley, uneven and handmade, its top a row of round lumpy sacks; behind it on the "
       "right a wide still pond of muddy brown water held back to a low line of stones at its far end; along its left foot a "
       "narrow stone-edged earth path and beside it a narrow ditch of muddy water flowing toward us, and at the left edge a strip "
       "of bright green young rice; steep green bamboo hills on both sides")  # e031 DAM: set-shangyou-ba-fx-l1 as it is
BAKE = "hazy white afternoon sunlight, dust in the hot air"
J0 = "At the row of new well pits on the cracked dry field outside Liuxi village early on the third morning of the drought"
JM = "soft pale early-morning light under a thin grey haze low over the field, the shadows faint, the air still cool"  # review 必改 1 (B): no direction; the -chen pictures carry the dawn
J1 = "At the row of new well pits on the cracked dry field outside Liuxi village at the end of the same day"
JE = "low orange evening sun from the left, long shadows to the right across the cracked furrows"
C0 = "In the ancestral hall of Liuxi village at dusk on the same day"
CANDLE = "warm candlelight inside the hall, the last dim orange evening light through the lattice of the doors"
JK = ("one row of earth heaps running from the near left away to the far right across the cracked furrows, the near pit's dark "
      "square mouth in the left foreground with a long wooden pole along its far rim and a wooden tub on its edge, a willow with "
      "yellowed drooping leaves at the right, low roofs and hills far away")
TABLETS = "five small dark wooden tablets standing on it, their faces smooth and plain"
ALTAR = f"the long dark altar table against the wall with {TABLETS}, a bronze censer with a few incense sticks and two white candles"
LOC = {
    "ba": f"{B0}: {DAM}; {BAKE}",
    "ba_c": f"{B0}, on the narrow stone-edged earth path at the foot of the bank of brown hemp sacks; {BAKE}",
    "jk": f"{J0}: the field exactly as in the picture: {JK}; {JM}",
    "jk_c": f"{J0}, at the near well pit, its dark square mouth and the long wooden pole along its far rim, the earth heaps beyond it; {JM}",
    "jk_e": f"{J1}: the field exactly as in the picture: {JK}; {JE}",
    "jk_ec": f"{J1}, at the near well pit, its dark square mouth and the long wooden pole along its far rim, the earth heaps beyond it; {JE}",
    "jk_ed": f"{J1}, beside the near well pit on the cracked furrows of the dry field; {JE}",
    "jk_et": f"{J1}, walking along the row of earth heaps toward the village, the wide evening sky and the dry field around; {JE}",
    "ct": f"{C0}: the hall exactly as in the picture: the pair of lattice doors swung back on the left with a dim passage and another lattice door glowing with the last orange dusk light beyond them, {ALTAR} on the right, the thick dark main beam across the top of the back wall, a floor of grey stone flags; {CANDLE}",
    "ct_men": f"{C0}, just inside the doorway, the lattice door leaves swung back, beyond the doorway a dim passage and another lattice door glowing with the last orange dusk light; {CANDLE}",
    "ct_q": f"{C0}, before the plain candle-warmed back wall under the dark main beam; {CANDLE}",
    "ct_l": f"{C0}: the thick dark main beam across the top of the candle-warmed back wall; {CANDLE}",
    "ct_z": f"{C0}, before {ALTAR}; {CANDLE}",
}
LIGHT = {
    "hot": "the hazy white afternoon light stays unchanged",
    "morn": "the pale early-morning light stays unchanged",
    "eve": "the low orange evening light stays unchanged",
    "dusk": "the warm candlelight and the dim dusk at the doors stay unchanged",
}
# bible rule 15: no "<X> speaks off screen" / "the system voice speaks off screen".
OFFSCREEN_SPEECH = False

# Repeated wording (each prop is one object, written the same way every time).
XU_UP = "Xu Yan, in his faded blue-grey scholar's robe patched at one elbow, its sleeves rolled up to the elbows, dust on its hem"
ROPE = "one thick hemp rope knotted round his waist, its other end tied to the long wooden pole along the pit's rim"
XU_ROPE = f"{XU_UP}, {ROPE}"
XU_MUD = ("Xu Yan, in his faded blue-grey scholar's robe patched at one elbow, the robe, his arms and his face caked with wet "
          "yellow mud, his hair matted")  # bible 〈人物〉: the mud on the robe and the cheeks in large patches, no dots (rule 12)
XU_PALE = ("Xu Yan, in his faded blue-grey scholar's robe patched at one elbow, its sleeves rolled up to the elbows, dried yellow "
           "mud on its knees, his face washed clean and pale")
QIN = ("Qin Shuang, in her fitted dark brown cross-collared short jacket cinched with a wide plain black leather belt, black "
       "trousers and leather boots, her high ponytail tied with black cord")  # e030's wording; no chopper (rule 5)
POLE = "one plain wooden carrying pole as long as she is tall, smooth and round to its ends"
TUBE = "one bamboo water tube with a rope handle"
ERNIU = "Wang Erniu, in his coarse brown cross-collared short jacket with the sleeves rolled up, his face tanned dark from the sun"
ERNIU_MUD = ("Wang Erniu, in his coarse brown cross-collared short jacket with the sleeves rolled up, dried yellow mud caked on "
             "the jacket and his forearms, his face tanned dark from the sun")
HOE = "one hoe with a plain wooden handle and an iron blade"
PICK = "one short-handled iron pick with a plain wooden handle"
HAN = ("Elder Han, in his faded grey cotton cross-collared long robe, his long white beard down to his chest, his white hair in a "
       "small topknot, his polished old bamboo walking staff in his right hand")
HAN_NOSTAFF = ("Elder Han, in his faded grey cotton cross-collared long robe, his long white beard down to his chest, his white "
               "hair in a small topknot")
CARP = ("Carpenter Shi, in his faded light tan cross-collared short work jacket with the sleeves rolled up and his worn brown "
        "leather apron, one plain wooden stick through his grey topknot")  # e015-e017; the picture has no brush behind his ear
ROLL = "one rolled sheet of plain cream paper, its outside plain"  # rule 38: the waterwheel drawing, never its face
# rule 34 (e031 review 必改 7): the same five Liuxi villagers as e031, five colours that are none of the leads'
VILLAGERS = ("five more people in Song-dynasty cross-collared homespun short jackets, each a different colour, cloth head wraps and "
             "cloth shoes: a white-haired old man in a faded undyed hemp-beige jacket and a lean middle-aged man in a dark charcoal "
             "jacket, each with one wooden carrying pole on his shoulder and an empty wooden bucket at each end of it; a thin boy of "
             "fifteen in a faded indigo jacket, a broad middle-aged man in a dull olive-green jacket and a middle-aged woman in a "
             "dark grey jacket with a faded indigo head cloth, each with one bamboo basket on the back and one wooden spade in hand")
VILLAGERS_PIT = ("five more people in Song-dynasty cross-collared homespun short jackets, each a different colour, cloth head wraps "
                 "and cloth shoes, yellow mud on their jackets, each standing full figure on the field beside the far earth heaps: "
                 "a white-haired old man in a faded undyed hemp-beige jacket and a lean middle-aged man in a dark charcoal jacket, "
                 "each with one carrying pole on his shoulder and a bamboo basket of yellow earth at each end of it; a thin boy of "
                 "fifteen in a faded indigo jacket, a broad middle-aged man in a dull olive-green jacket and a middle-aged woman in "
                 "a dark grey jacket with a faded indigo head cloth, each with one wooden spade")
RETAINERS = ("twelve men in identical Song-dynasty black cross-collared short jackets, black cloth head wraps and cloth shoes, each "
             "holding one plain wooden staff")
# s01 as e031 s41 was shot (9311101): about fourteen of them, white cloth leg wraps, standing in the pond's shallow water
RETAINERS_S01 = ("fourteen men in identical Song-dynasty black cross-collared short jackets, black trousers with white cloth leg wraps "
                 "below the knee and black cloth head wraps, each holding one plain wooden staff")
# rule 34: the hall, eight people each a different colour, age and sex; no leads' colours, no red-string pigtails (Xiaohe's)
CT_VILLAGERS = ("eight more people in Song-dynasty cross-collared homespun jackets and cloth shoes, each a different colour: a bent "
                "old woman in a faded deep plum jacket with a white head cloth, a white-haired old man in a faded undyed hemp-beige "
                "jacket, a middle-aged woman in a dark grey jacket with a faded indigo head cloth, a broad middle-aged man in a "
                "dull olive-green jacket, a young woman in a rust-red jacket, a boy of about ten in a mustard-yellow jacket, a girl "
                "of about seven in a faded green jacket with her hair in one small bun, and a lean middle-aged man in a dark charcoal "
                "jacket")  # review 建議 9: the pits' charcoal man (e031/e032), one more grown man for e033 c05
HANDS = "their hands hold only what is described here"
SILENT_HE = "He says nothing in this shot: his lips stay pressed together from the first frame to the last, his jaw still, no talking, no mouthing words"
NOBODY = "Throughout the shot the set layout stays as it is. The pictures fix the place and the objects only, never the mood. "
# rule 2: over-the-shoulder backs, unnamed, no picture
BACK_XU = ("at the left edge of the frame, cut by it, soft and out of focus, only the back of one shoulder in a faded blue-grey "
           "robe and the back of a man's topknot, toward us the whole shot")
BACK_ERNIU = ("at the right edge of the frame, cut by it, soft and out of focus, only the back of one broad shoulder in a coarse "
              "brown jacket with a wooden hoe handle resting on it and the back of a man's head, toward us the whole shot")
BACK_ERNIU_MUD = ("at the right edge of the frame, cut by it, soft and out of focus, only the back of one broad shoulder in a coarse "
                  "brown jacket caked with dried yellow mud and the back of a man's head, toward us the whole shot")
BACK_CARP = ("at the right edge of the frame, cut by it, soft and out of focus, only the back of one shoulder in a faded light tan work "
             "jacket with the strap of a leather apron across it and the back of a grey topknot with one plain wooden stick through "
             "it, toward us the whole shot")
# the man over her shoulder (s23-s26b): unnamed where his face is not in the frame (no picture)
CARRIED = ("over her right shoulder the limp body of a man in a mud-caked faded blue-grey robe, his head and arms hanging down "
           "behind her back")
# set-only sides (the picture of each place, all the way to the edge)
SIDE_GULLY = "the soft green bamboo slope of the valley"
SIDE_SKY = "the hazy white sky and the green bamboo slope"
SIDE_FIELD = "the cracked furrows of the dry field"
SIDE_DOOR = "the dark lattice door leaf swung back against the wall"
SIDE_HALL = "the candle-warmed back wall of the hall"


def quiet(who, pr="his", plural=False):
    verb = "say" if plural else "says"
    return f"{who} {verb} nothing in this shot: {pr} lips stay pressed together from the first frame to the last, no talking, no mouthing words"


def off(side, what, he="he"):
    """A line to someone outside the frame: the gaze, that side set only, and the only person (rule 31)."""
    edge = f"the {side} edge of the frame"
    return (f"toward someone out of sight beyond {edge}, never the lens; that side of the frame is only {what} all the way to the "
            f"edge, and {he} is the only person in the frame")


SHOTS = [
    # ---- scene 1: the first afternoon of the drought quest, the Qian dam upstream (31->32: the same moment as e031 s41).
    dict(chapter="上游錢家的壩前", loc="ba", cam="Wide shot, slow push in", chars=["qinshuang"], night="hot",
         comp=f"wide shot at standing eye height toward the dam, like the picture: in the lower left foreground, on the stone-edged path at the foot of the bank of sacks, filling the lower left quarter of the frame and cut at the hips by the bottom of the frame, one big young man seen only from behind, turned a little away from us toward the right, in a coarse brown cross-collared short jacket with the sleeves rolled up, {HOE} raised high above his head in both hands, its handle slanting up to the upper left and its iron blade high at the left edge of the frame, the back of his head toward us the whole shot; just at his right, between him and the bank, {QIN}, cut at the waist by the bottom of the frame, already right beside him from the first frame, {POLE} in both her hands, its end already under the raised hoe handle, her face in profile to screen left toward him, never the lens; cold and fast, not smiling: brows level, eyes hard, lips closed; beyond the bank of sacks on the right, standing in one row in the shallow muddy water of the pond along the far side of the bank, from just right of the middle of the frame away to the left, the nearest at the right the tallest and the farther ones smaller and smaller, {RETAINERS_S01}, their faces three-quarter to screen left toward the young man, their staffs held upright; {HANDS}; exactly sixteen people; the only hoe in the frame is the young man's",
         motion=NOBODY + f"Qin Shuang flicks the carrying pole sharply upward: the hoe is knocked out of the young man's hands, flies up and away to the left and drops blade first, sticking in the earth of the path at the left edge of the frame; the fourteen men in the pond stay where they are; {quiet('Everyone in the frame', 'their')}",
         zh="全景、慢推（人眼高、照圖；送整張 `set-shangyou-ba-fx-l1`，接點 31→32，同第 31 集 s41 的機位）：**照第 31 集 s41 實拍（9311101 精修片，剪在 3.833 秒）重核**：二牛的背影佔左下約四分之一、被畫框下緣切在臀部、身子略朝右轉離鏡頭，鋤頭兩手高舉過頭、柄往左上斜、鐵刃在畫面左緣上方（不點名、不送圖，同 s41）；秦霜第一格已經在他**右邊**（他和麻袋土埂之間的石邊土路上：稿子『站到兩幫人中間』），兩手握著木扁擔、扁擔頭已經頂在鋤頭柄下，側臉朝畫左看他、不笑；家丁照實拍寫成**站在土埂右後方水塘的淺泥水裡**、沿土埂排成一排，從畫面中間偏右（最近、最高）往左後越來越小，臉三分之二朝畫左看二牛、棍子豎直（s41 剪點時棍子已從前傾回到豎直）；人數照實拍約 13–15 人寫**十四人**（稿子的十二人改掉，免得 s41→s01 少了兩三個；拍法 34 仍只在這個遠景），黑短打、黑頭巾、膝下白綁腿（實拍的樣子）。動作只有一個：扁擔往上一挑，鋤頭脫手、往**左**飛、刃朝下插在畫左緣的土路上（給 s04 許硯從左邊拔起來；審稿建議）。稿子『從畫面左跑進來、從村民肩上抽走扁擔、兩步衝到二牛身後』在第一格已經完成（聖經 31→32）；『在空中轉兩圈、插進裂泥』照圖改落在土路上（圖上沒有裂泥）；許硯與村民不入鏡（第 31 集 s41 也沒拍）。**柴刀不寫**（拍法 5）。無台詞"),
    dict(loc="ba_c", cam="Medium shot, slow push in", chars=["qinshuang", "erniu"], night="hot",
         comp=f"medium shot on the narrow stone-edged earth path at the foot of the bank of sacks, both framed from the waist up, side-on to us: on the left {ERNIU}, his hands empty, already stumbling back from the first frame, his face three-quarter to screen right toward her, never the lens; stunned and furious, not smiling: brows knotted, jaw clenched, chest heaving, his lips pressed shut; on the right {QIN}, facing screen left, her back to the bank of sacks, {POLE} upright in her right hand, its end on the earth, her left hand already gripping the front of his collar from the first frame, never the lens; cold and level, not smiling: eyes hard, brows level, lips moving fast and clipped between words; behind them, soft, the bank of brown hemp sacks rising at the right and the narrow muddy ditch at the left in the hazy white sun; {HANDS}; exactly two people",
         lines=[("qinshuang", "打了，就是給錢家藉口。你想讓全村吃官司？", "冷，不回頭")],
         motion=f"Qin Shuang shoves him one step back toward the left by his collar as she speaks; {quiet('Wang Erniu')}",
         zh="中景（雙人、側面）、慢推（送 e031 的免費裁切 `set-shangyou-ba-fx-lu-l1`：左邊泥水小溝、石邊土路、右邊麻袋坡）：二牛在畫左、兩手空了、第一格已經踉蹌、嘴閉著、不笑（原版必修）；秦霜在畫右、背對麻袋土埂朝畫左（『不回頭』：不回頭看家丁）、右手扁擔立在地上，左手第一格已經揪住他的衣領，把他往左（離開壩那邊）推一步、冷冷地說。稿子『把他拉到自己身後、扁擔橫在身前』改成一個動作（推一步）；家丁不進近鏡（拍法 34），不寫"),
    dict(loc="ba_c", cam="Close-up, slow push in", chars=["erniu"], night="hot",
         comp=f"close-up of {ERNIU}, framed from the chest up with space above his head, his hands empty, his face three-quarter to screen right {off('right', SIDE_GULLY)}; desperate, not smiling: red-rimmed eyes, brows knotted hard, jaw clenched, chest heaving, lips moving fast between panting words; behind him, soft, only the green bamboo slope of the valley in the hazy white sun; {HANDS}",
         lines=[("erniu", "可水都被截了！不打，難道看著田乾死？", "急，不笑")],
         motion="Wang Erniu's flat right hand sweeps once toward the right edge of the frame, toward the dam, and drops again as he speaks",
         zh="近景、慢推（送 `set-shangyou-ba-fx-shan-l1`：虛焦的竹坡，稿子『身後只有乾裂的河岸』照圖改）：二牛眼睛發紅、喘、咬牙，朝畫右外看不到的人（秦霜，不點名）急著說，右手平掌往壩那邊一揮又放下（稿子『握緊拳頭往壩那邊指一下』：單指會讀錯，拍法 32）。**不笑**、臉寫 tanned dark 不寫 flushed red（原版必修：大笑、肩上一片紅暈）"),
    dict(loc="ba_c", cam="Medium shot, slow push in", chars=["xuyan", "erniu", "qinshuang"], night="hot",
         comp=f"medium shot on the narrow stone-edged earth path, all three framed from the waist up: on the left {XU_UP}, already bent over from the first frame, both hands gripping the wooden handle of {HOE} whose iron blade is stuck in the earth of the path, his face three-quarter to screen right toward the other two, never the lens; out of breath and steady, not smiling: panting, brows level, lips moving between breaths; in the middle {ERNIU}, his hands empty, his face three-quarter to screen left toward Xu Yan, his lips pressed shut, not smiling, never the lens; on the right {QIN}, {POLE} upright in her right hand, her face three-quarter to screen left, her lips pressed shut, never the lens; behind them, soft, the bank of brown hemp sacks rising at the right and the narrow muddy ditch at the left in the hazy white sun; {HANDS}; exactly three people; the only hoe in the frame is the one in Xu Yan's hands",
         lines=[("xuyan", "秦霜說得對。錢員外就等我們先動手。", "喘，很穩")],
         motion=f"Xu Yan straightens up, pulling the hoe out of the earth, as he speaks; {quiet('Wang Erniu and Qin Shuang', 'their', plural=True)}",
         zh="中景（三人）、慢推（送 `-fx-lu-l1`）：照軸線左到右許硯、二牛、秦霜；許硯第一格已經彎著腰握住插在土路上的鋤頭（s01 鋤頭往左飛），直起身、把鋤頭從土裡拔出來、喘著穩穩地說；二牛（兩手空）與秦霜朝畫左看他、嘴閉著。稿子『從左後跑上來』在第一格已經完成；跟拍改慢推"),
    dict(loc="ba_c", cam="Medium shot over the shoulder, slow push in", chars=["xuyan"], night="hot",
         comp=f"medium shot over a shoulder: {BACK_ERNIU}; one step beyond it in the left half of the frame {XU_UP}, standing on the narrow stone-edged earth path, framed from the waist up, his hands empty, his flat right hand already raised a little toward the man's shoulder from the first frame, his face three-quarter to screen right toward the man in the foreground, never the lens; firm and calm, not smiling: steady eyes, brows level, lips moving evenly between words; behind him, soft, the narrow ditch of muddy water beside the stone-edged path in the hazy white sun; {HANDS}; exactly two people, the one in the foreground seen only from behind",
         lines=[("xuyan", "水，我們自己找。不靠他的壩，也要讓田見水。", "穩")],
         motion="Xu Yan pats the shoulder of the man in the foreground once with his flat right hand as he speaks",
         zh="過肩中景、慢推（送 `set-shangyou-ba-fx-jiao-l1`：泥水小溝、石邊土路）：前景右是被畫框切掉、虛焦的褐色肩背與肩上的鋤頭柄（不點名、不送圖，拍法 2；鋤頭第一格已經還給他）；許硯在畫左半、朝畫右，平掌拍一下他的肩、穩穩地說。稿子『許硯左肩後拍二牛、許硯說話』改成反過來（說話的人臉朝鏡頭、聽的人是過肩背影）；『把鋤頭塞回二牛手裡』在第一格已經完成（一鏡一個動作）"),
    dict(loc="ba_c", cam="Close-up, slow push in", chars=["erniu"], night="hot",
         comp=f"close-up of {ERNIU}, framed from the chest up with space above his head, {HOE} on his right shoulder from the first frame, his face three-quarter to screen left {off('left', SIDE_GULLY)}; it comes to him, not smiling: eyes going wide and bright, brows lifting, mouth set, lips moving fast between words; behind him, soft, only the green bamboo slope of the valley in the hazy white sun; {HANDS}",
         lines=[("erniu", "下游還有一口深潭，潭裡的水沒乾！", "想到了")],
         motion="Wang Erniu's head comes up and his eyes widen as he speaks, his mouth set",
         zh="近景、慢推（送 `-fx-shan-l1`）：二牛鋤頭扛回右肩（第一格），抬起頭、眼睛一亮（想到了，不笑），朝畫左外看不到的人（許硯，不點名）說。稿子『轉身往畫面左（下游）一指』不拍（單指會讀錯；一鏡一個動作）：他的臉本來就朝左"),
    dict(loc="ba_c", cam="Medium shot, slow push in", chars=["xuyan", "erniu", "qinshuang"], night="hot",
         comp=f"medium shot on the narrow stone-edged earth path, all three framed from the waist up: on the left {XU_UP}, his hands empty, his face three-quarter to screen right toward the young man beside him, never the lens; level and patient, not smiling: brows drawn a little, lips moving evenly between words; in the middle {ERNIU}, {HOE} on his right shoulder, his face three-quarter to screen left toward Xu Yan, his lips pressed shut, not smiling, never the lens; on the right {QIN}, {POLE} upright in her right hand, her face three-quarter to screen left, her lips pressed shut, never the lens; behind them, soft, the bank of brown hemp sacks rising at the right and the narrow muddy ditch at the left in the hazy white sun; {HANDS}; exactly three people; the only hoe in the frame is Wang Erniu's",
         lines=[("xuyan", "潭在溝底，田在坡上，一擔擔挑，挑不活三畝田。", "搖頭")],
         motion=f"Xu Yan shakes his head slowly as he speaks; {quiet('Wang Erniu and Qin Shuang', 'their', plural=True)}",
         zh="中景（三人）、慢推（送 `-fx-lu-l1`）：照軸線許硯在**左**、二牛在中、秦霜在右（稿子『許硯在中、二牛左、秦霜右』會讓二牛換邊，照 s04–s06 的左右改）；許硯朝二牛慢慢搖頭地說，兩人嘴閉著。稿子『先手往下指、再往上一抬』不拍（一鏡一個動作，手勢會讀錯）"),
    dict(loc="ba_c", cam="Medium shot over the shoulder, slow push in", chars=["qinshuang"], night="hot",
         comp=f"medium shot over a shoulder: {BACK_XU}; one step beyond it in the right half of the frame {QIN}, standing on the narrow stone-edged earth path, framed from the waist up, {POLE} upright in her right hand from the first frame, its end just above the earth, her face three-quarter to screen left toward the man in the foreground, never the lens; impatient, not smiling: brows drawn, eyes narrowed, lips moving fast and clipped between words; behind her, soft, the bank of brown hemp sacks rising at the right in the hazy white sun; {HANDS}; exactly two people, the one in the foreground seen only from behind",
         lines=[("qinshuang", "別繞了，說人話。到底要怎麼做？", "不耐煩")],
         motion="Qin Shuang thumps the end of the carrying pole down on the earth once, a little dust rising, as she speaks",
         zh="過肩中景、慢推（送 `-fx-lu-l1`）：前景左是虛焦的藍灰肩背與髮髻（不點名、不送圖）；秦霜在畫右半、背後是麻袋坡，扁擔往地上一頓、揚起一點灰，不耐煩地說。二牛在 s07 站在兩人中間，過肩略過他（換機位）"),
    dict(loc="ba_c", cam="Low-angle medium shot, slow push in", chars=["xuyan"], night="hot",
         comp=f"low-angle medium shot of {XU_UP}, framed from the waist up, {HOE} already raised over his right shoulder in both hands from the first frame, his hair stuck to his forehead in the heat, his face three-quarter to screen right {off('right', SIDE_SKY)}; resolved, not smiling: jaw set, eyes steady, lips moving firmly between words; behind him, soft, only the hazy white sky and the green bamboo slopes of the valley; {HANDS}",
         lines=[("xuyan", "挖井。就在田邊挖，挖到見水為止。", "很穩")],
         motion="Xu Yan swings the hoe down hard into the earth at his feet, out of the bottom of the frame, as he speaks",
         zh="低角度中景、慢推（送 `set-shangyou-ba-fx-ding-l1`：霧白的天與竹林山谷，稿子『身後只有天空』）：許硯第一格已經從二牛肩上拿過鋤頭、兩手舉在右肩上，往腳邊用力一鋤（出畫下緣），朝畫右外看不到的人（秦霜，不點名）很穩地說。稿子的近景改腰以上（拍法 32：鋤頭的動作要看得見）；『汗從額角流下』寫髮絲黏在額上（拍法 12）"),
    dict(loc="ba_c", cam="Wide shot, slow push in", chars=["qinshuang", "xuyan", "erniu"], night="hot",
         comp=f"wide shot along the narrow stone-edged earth path at the foot of the bank of sacks, everyone framed full figure, already walking toward us down the path from the first frame, in a loose line: at the front {QIN}, her hands empty, her face turned back over her left shoulder toward the people behind her, never the lens; brisk and cold, not smiling: brows level, lips moving between words; behind her {XU_UP} and {ERNIU} with {HOE} on his right shoulder, their lips pressed shut, never the lens; behind them {VILLAGERS}, their lips closed, never the lens; at the right the bank of brown hemp sacks, at the left the narrow muddy ditch, in the hazy white sun; {HANDS}; exactly eight people; the only hoe in the frame is Wang Erniu's",
         lines=[("qinshuang", "好，聽你的。都走，別在這裡讓人看笑話。", "乾脆")],
         motion=f"the eight of them walk steadily toward us down the stone-edged path as Qin Shuang speaks; {quiet('Xu Yan, Wang Erniu and the five others', 'their', plural=True)}",
         zh="全景、慢推（送 `-fx-lu-l1`）：一行八人第一格已經沿壩腳的石邊土路朝鏡頭走來（泥水小溝流向鏡頭，下游、村子在鏡頭這一邊；稿子『往左走』照圖改）：最前面秦霜兩手空了（扁擔第一格已經還給村民：本色麻衣老漢與炭灰中年各挑扁擔兩頭空桶），從左肩回頭說；許硯、二牛（鋤頭）、五個村民（e031 的五種衣色，沒有鋤頭）嘴閉著跟著走（第一場結尾）。稿子『回頭看壩上一眼、遠處家丁放下棍子』不拍（一鏡一個動作；家丁不進全景以外的鏡、這張裁切也看不到土埂頂，拍法 34）；跟拍改慢推"),
    # ---- scene 2: the third day of the quest, the row of well pits (set-jingkeng-l1), morning then evening.
    dict(chapter="柳溪田邊的井坑", loc="jk", cam="Wide shot, slow push in", chars=["hanbo", "xuyan"], night="morn",
         comp=f"wide shot at standing eye height, like the picture: in the left foreground at the rim of the near well pit {XU_ROPE}, framed full figure, small, standing still, {PICK} stuck upright in the earth at his feet, his face turned toward the old man, his lips pressed shut, never the lens; walking slowly toward him along the row of earth heaps from the right {HAN}, framed full figure, small, his eyes on the heaps he passes, not smiling: weary, brows drawn, his head shaking, lips moving slowly between words, never the lens; far along the row {VILLAGERS_PIT}, their lips closed, never the lens; {HANDS}; exactly seven people; every pit is empty, everyone stands on the field",
         lines=[("hanbo", "第三天了，挖了十幾口，一口都沒見水。", "蒼老，慢")],
         motion=f"Elder Han walks slowly on along the row of heaps toward the near pit, leaning on his staff, as he speaks; {quiet('Xu Yan and the five others', 'their', plural=True)}",
         zh="全景、慢推（人眼高、照圖；送本集免費做的清晨版 `set-jingkeng-chen-l1`（`jingkeng_chen.sh`：`set-jingkeng-l1` 第二輪 37040 塗掉遠處像人影的樹幹、降飽和、壓暗、偏冷，金柳降成灰黃；一排土堆從左前斜到右後、左前那口坑最近、畫得最清楚，黑方口、遠邊一根長木桿、坑邊一個木盆，木盆右邊還有一口；右邊垂柳，遠處屋頂與山）：清晨，光寫淡淡的晨光與灰霧、**不寫方向**（審稿必改 1）。許硯在**左前那口坑邊**（稿子『中間那一口』照圖改：圖上這口最近）、腰上第一格已經綁好麻繩、短柄鎬插在腳邊、嘴閉著；韓伯拄竹杖從右邊沿土堆慢慢走過來、搖頭地說；遠處土堆旁五個村民（e031 那五人、身上沾泥，兩人挑兩筐黃土、三人拿木鍬，**沒有鋤頭**），**每個人都整個人站在田上、坑裡沒有人**（原版必修：地上長出二牛的人頭）。稿子『村民在坑裡掄鋤頭往上吊土』『韓伯一口一口往坑裡看』照這樣改；推軌改慢推"),
    dict(loc="jk_c", cam="Medium shot, slow push in", chars=["xuyan", "hanbo"], night="morn",
         comp=f"medium shot at the rim of the near well pit, both framed from the waist up: on the left {XU_ROPE}, both hands already on the knot at his waist from the first frame, {PICK} stuck upright in the earth at his feet, his face three-quarter to screen right toward the old man, never the lens; gentle, not smiling: soft eyes, lips moving quietly between words; on the right {HAN}, standing, leaning on the staff, his face three-quarter to screen left toward Xu Yan, his lips pressed shut, never the lens; behind them, soft, the dark square mouth of the pit, the long wooden pole along its far rim and the first earth heaps in the pale morning haze; {HANDS}; exactly two people",
         lines=[("xuyan", "韓伯，待會日頭就毒了，您回樹蔭下歇著。", "溫和")],
         motion=f"Xu Yan pulls the knot at his waist tight with one hard tug as he speaks; {quiet('Elder Han')}",
         zh="中景（雙人）、慢推（送清晨版裁切 `set-jingkeng-kou-chen-l1`：坑口、長木桿、土堆）：許硯在左、腰上的麻繩打結、用力一拉試緊、溫和地說（台詞是 2026-11-06 審稿後改的「待會日頭就毒了」）；韓伯在右拄杖、嘴閉著（原版必修：許硯與韓伯同框，不長出二牛的人頭）。稿子『衣襟上沾著露水』不寫（拍法 12）；『抬頭看韓伯』不拍（一鏡一個動作）"),
    dict(loc="jk_c", cam="Medium shot over the shoulder, slow push in", chars=["hanbo"], night="morn",
         comp=f"medium shot over a shoulder: {BACK_XU}; one step beyond it in the right half of the frame {HAN}, already lowering himself from the first frame onto a flat fieldstone at the edge of the pit, both hands on the staff, his face three-quarter to screen left toward the man in the foreground, never the lens; stubborn and sure, not smiling: brows level, eyes steady, lips moving slowly between words; behind him, soft, the row of earth heaps running away across the cracked furrows in the pale morning haze; {HANDS}; exactly two people, the one in the foreground seen only from behind",
         lines=[("hanbo", "你一個秀才都要下去，老頭子哪坐得住。", "篤定")],
         motion="Elder Han sits down on the flat stone, leaning on his staff, and stays as he speaks",
         zh="反打過肩中景、慢推（送清晨版 `set-jingkeng-dui-chen-l1`：一排土堆斜過裂田、遠處屋頂與山）：前景左是虛焦的藍灰肩背與髮髻（不點名）；韓伯拄杖在坑邊一塊平石上坐下（不走），篤定地說（答 s12：不肯）。稿子『搖頭』不拍（一鏡一個動作）"),
    dict(loc="jk_c", cam="Medium shot, slow push in", chars=["xuyan", "erniu"], night="morn",
         comp=f"medium shot at the rim of the near well pit, both framed from the waist up: on the left {XU_ROPE}, his face three-quarter to screen right toward the young man, his lips pressed shut, never the lens; tired, not smiling; on the right {ERNIU_MUD}, already standing close beside him from the first frame, his face three-quarter to screen left toward Xu Yan, never the lens; urgent, not smiling: brows knotted, eyes wide, lips moving fast between words; behind them, soft, the dark square mouth of the pit and the long wooden pole along its far rim in the pale morning haze; {HANDS}; exactly two people",
         lines=[("erniu", "許大哥，你沒挖過井，讓我下去！", "急，不笑")],
         motion=f"Wang Erniu's right hand grabs the rope at Xu Yan's waist as he speaks; {quiet('Xu Yan')}",
         zh="中景（雙人）、慢推（送 `-kou-chen-l1`）：二牛第一格已經從右邊大步走到許硯身邊（滿身乾泥，寫成整片），右手一把抓住許硯腰上的繩子、急著說，不笑；許硯在左、嘴閉著。稿子『從右邊大步走過來』在第一格已經完成（原版必修：二牛整個人入鏡，不是一顆頭）；跟拍改慢推。第二場二牛不拿鋤頭（他拉繩）"),
    dict(loc="jk_c", cam="Medium shot over the shoulder, slow push in", chars=["xuyan"], night="morn",
         comp=f"medium shot over a shoulder: {BACK_ERNIU_MUD}; one step beyond it in the left half of the frame {XU_ROPE}, framed from the waist up, the loose end of the rope already in his left hand from the first frame, his face three-quarter to screen right toward the man in the foreground, never the lens; tired and firm, not smiling: shadows under his eyes, brows level, lips moving evenly between words; behind him, soft, the long wooden pole along the far rim of the pit and the cracked furrows in the pale morning haze; {HANDS}; exactly two people, the one in the foreground seen only from behind",
         lines=[("xuyan", "你挖了兩天了。這口換我，上面拉繩靠你。", "累，穩")],
         motion="Xu Yan holds the loose end of the rope out to the man in the foreground as he speaks",
         zh="過肩中景、慢推（送 `-kou-chen-l1`）：前景右是虛焦、沾泥的褐色肩背（不點名、不送圖）；許硯在畫左半、累、不笑，把繩尾遞給他、穩穩地說。稿子『按住二牛的手、把繩子拿回來、再把繩尾塞給他、二牛點頭』拆成第一格已經拿回繩子加一個遞的動作（一鏡一個動作）"),
    dict(loc="jk_ec", cam="High-angle insert, slow push in", chars=[], night="eve", act=3,
         comp=f"high-angle close shot looking straight down: the very first frame is already a close view of two mud-caked hands in rolled-up faded blue-grey sleeves gripping {PICK}, raised near the top of the frame, and below them the dark damp yellow earth at the bottom of a deep narrow shaft; rough dug yellow earth walls close in on every edge, only a thin warm orange glow along the top edge, the rest in shadow; only the two hands, the forearms and the pick are in the frame",
         motion="the pick swings down into the earth and one damp clod breaks loose",
         zh="俯拍插鏡、慢推（**不送任何圖**、不送臉，審稿必改 2：`-kou` 是從高處斜看磚坑的外面，送了會長出『地上一顆人頭』）：第一格已經是兩隻沾泥、袖子捲起的手握著短柄鎬舉在上緣，下面是窄井底的暗濕黃土，四面土壁、只有上緣一道橘光；鎬往下一刨、一塊濕土鬆脫。`mkspec.py` 要拿掉 d1 的地點句（同第 31 集 s18／s21），`prep932.sh` 掃 `well pits`、`field`、`village` 不能出現。井兩人深交給 s17 探頭與 s18 台詞。**已經是傍晚**：時間的跳接在 s15→s16 這一刀（稿子『井口的天光從灰白慢慢轉成橘』不拍成鏡頭裡變光：原版 c21 同一鏡光線跳是必修），橘光只在上緣坑口。稿子『從井底往上拍、二牛的頭在井口往下看』改俯拍手與鎬、不拍井口的頭與他的臉（原版必修：地上的人頭）。無台詞"),
    dict(loc="jk_ec", cam="Medium shot, slow push in", chars=["qinshuang", "erniu"], night="eve",
         comp=f"medium shot at the rim of the near well pit, both framed from the waist up: on the right {QIN}, standing at the rim, {TUBE} in her right hand, already leaning to look down into the dark pit from the first frame, never the lens; frowning, not smiling: brows drawing together, lips moving fast between words; on the left {ERNIU_MUD}, crouching on the rim, both hands gripping the rope that runs taut down into the pit, his face three-quarter to screen right toward her, his lips pressed shut, worried, not smiling, never the lens; behind them, soft, the long wooden pole along the far rim and the earth heaps in the low orange evening light; {HANDS}; exactly two people",
         lines=[("qinshuang", "他下去多久了？上頭的人都沒換他？", "皺眉")],
         motion=f"Qin Shuang's eyes lift from the pit to Wang Erniu, her brows drawn, as she speaks; {quiet('Wang Erniu')}",
         zh="中景（雙人）、慢推（送 `-kou-l1`）：傍晚；秦霜第一格已經從右邊走到坑邊（秦霜從右來）、右手提竹水筒、探頭往坑裡看，眼睛從坑抬到二牛、皺眉地說（原版建議：秦霜問話時臉在畫面上，所以全景改中景）；二牛在左蹲在坑邊兩手握著繃緊的繩、嘴閉著、不笑。前景木樁與繩子照圖寫成坑口的長木桿"),
    dict(loc="jk_ec", cam="Close-up, slow push in", chars=["erniu"], night="eve",
         comp=f"close-up of {ERNIU_MUD}, crouching, framed from the chest up with space above his head, both hands gripping the rope at the bottom of the frame, his face turned down toward the dark pit at first, never the lens; the right side of the frame is only the cracked furrows of the dry field all the way to the edge, and he is the only person in the frame; frightened, not smiling: brows knotted up, eyes wide, panting, lips moving fast between words; behind him, soft, only the long wooden pole along the rim of the pit in the low orange evening light; {HANDS}",
         lines=[("erniu", "一整天了，叫他也不上來，剛才就沒聲了。", "喘，擔心")],
         motion="Wang Erniu's face comes up from the pit and turns three-quarter to screen right, toward someone out of sight beyond the right edge of the frame, as he speaks",
         zh="近景、慢推（送 `-kou-l1`）：二牛蹲著、兩手握繩，臉從坑口抬起、轉向畫右外看不到的人（秦霜，不點名）擔心地說；**不笑**（原版必修）。稿子『往井裡探頭喊一聲沒回音』的喊聲收在音效（〈配音〉），第一格臉已經朝下看坑"),
    dict(loc="jk_ec", cam="Medium shot, slow push in", chars=["qinshuang", "erniu"], night="eve",
         comp=f"medium shot at the rim of the near well pit, both framed from the waist up, side-on to us, the rope running taut from the dark pit at the left: in front, nearer the pit, {ERNIU_MUD}, both hands already on the rope, his face in profile to screen left, his lips pressed shut, not smiling, never the lens; just behind him on the right {QIN}, both her hands already gripping the same rope from the first frame, {TUBE} standing on the earth at her feet, her face in profile to screen left toward the young man in front of her, never the lens; commanding, not smiling: brows drawn, eyes hard, lips moving fast between words; behind them, soft, the earth heaps in the low orange evening light; {HANDS}; exactly two people",
         lines=[("qinshuang", "沒聲了還等什麼？二牛，一起拉！", "命令")],
         motion=f"Qin Shuang braces her boots on the earth and leans back hard on the rope as she speaks; {quiet('Wang Erniu')}",
         zh="中景（側面）、慢推（送 `-kou-l1`）：**二牛在前、靠坑**（同 s17 二牛在左），秦霜在他身後（右）、第一格已經把竹水筒擱在腳邊、兩手抓住同一條從左邊坑口繃出來的繩子，側臉朝畫左對著前面的二牛下令，腳一蹬、身子往後拉；二牛側臉朝左、嘴閉著、不笑（審稿必改 4：原本秦霜從右肩回頭，臉轉離鏡頭，又跟 s17 換了邊）。稿子『把水筒往地上一擱、兩手握繩』在第一格已經完成；『兩個村民跑過來』放到 s20 第一格（一鏡一個動作）"),
    dict(loc="jk_e", cam="Wide shot, slow push in", chars=["qinshuang", "erniu"], night="eve", act=3,
         comp=f"wide shot from a little above standing eye height, looking down a little, like the picture: the dark square mouth of the near pit in the lower left, the thick hemp rope stretched taut from it toward the right across the cracked furrows; four people in a line on the rope, all framed full figure, already leaning back hard from the first frame, side-on to us: at the front {ERNIU_MUD}, then {QIN}, then a lean middle-aged man in a dark charcoal homespun jacket and a broad middle-aged man in a dull olive-green homespun jacket, cloth head wraps; every face strained, not smiling, lips pressed shut, never the lens; behind them, soft, the earth heaps in the low orange evening light; {HANDS}; exactly four people; the pit at the left is dark and its mouth shows only the rope",
         motion=NOBODY + f"the four of them haul the rope in together, hand over hand, twice, stepping back toward the right; {quiet('All four', 'their')}",
         zh="全景、慢推（照圖從略高於人眼往下看；改送整張 `set-jingkeng-l1`，審稿必改 3：`-kou` 是近框、放不下四個全身的人，圖也不是低角度）：左下是左前那口坑的黑方口，粗麻繩從坑口往右繃過裂田；二牛、秦霜與兩個村民（e031 那五人裡的炭灰瘦中年、暗橄欖綠壯中年）第一格已經排成一列往後倒、側面，一起把繩子往右拉兩把。**許硯不入鏡**：原版必修（被拉上來時自己走出淺坑）照聖經拆成「繩子繃緊」與下一鏡「第一格已經躺在坑邊」，不拍爬出來。無台詞"),
    dict(loc="jk_ed", cam="Close-up from overhead, slow push in", chars=["xuyan"], night="eve",
         comp=f"overhead close-up looking straight down: {XU_MUD}, lying on his back on the cracked furrows beside the pit from the first frame, framed from the chest up, his lips dry and pale, his eyes half closed, his face tipped up toward the evening sky, never the lens; nearly fainted, not smiling: slack face, brows loose, lips barely moving between breathy words; only the cracked dry yellow furrows with a few short dead stalks around his head and shoulders to every edge, in the low orange evening light; he is the only person in the frame",
         lines=[("xuyan", "沒……沒水。再往下一丈，也許就有……", "虛弱，眼睛半閉")],
         motion="Xu Yan's lips move weakly and, as he finishes speaking, his head rolls slowly to one side on the earth",
         zh="俯拍近景、慢推（送免費裁切 `set-jingkeng-di-l1`：乾裂的田壟與幾根短枯桿）：許硯第一格已經仰躺在坑邊（原版必修：不拍他爬出來），滿臉泥、嘴唇乾白（拍法 12：不寫裂口的細節）、眼睛半閉，嘴唇勉強動、氣聲地說，說完頭往旁邊一歪"),
    dict(loc="jk_ed", cam="Medium shot, slow push in", chars=["qinshuang", "xuyan", "erniu"], night="eve",
         comp=f"medium shot beside the near well pit: on the left {QIN}, down on one knee from the first frame, her right hand already resting on the forehead of the man lying before her, framed from the waist up, her face three-quarter to screen right toward the others, never the lens; grim and short, not smiling: brows drawn, lips moving low and fast between words; lying on his back across the bottom of the frame {XU_MUD}, his eyes closed, his face turned up, his lips pressed shut, never the lens; on the right, crouched close, {ERNIU_MUD}, framed from the waist up, his face three-quarter to screen left toward her, his lips pressed shut, not smiling, never the lens, and beside him, side-on to us, a broad middle-aged man in a dull olive-green homespun jacket, his lips pressed shut; behind them, soft, the earth heaps in the low orange evening light; {HANDS}; exactly four people",
         lines=[("qinshuang", "都讓開。曬昏了，得馬上送回屋裡。", "低聲，不耐煩")],
         motion=f"Qin Shuang sweeps her flat left hand once toward the two men on the right as she speaks; {quiet('Wang Erniu and the man beside him', 'their', plural=True)}",
         zh="中景、慢推（送 `-kou-l1`）：秦霜在左單膝跪著、右手第一格已經摸在他額頭上，左手平掌往右邊兩人一揮、低聲說；許硯仰躺在畫面下緣、眼睛閉著、嘴閉著；右邊二牛與暗橄欖綠的村民（側面）蹲著、嘴閉著。三張臉：秦霜、許硯（閉眼）、二牛（拍法 1）。稿子『摸額頭、臉一沉』在第一格已經完成"),
    dict(loc="jk_et", cam="Wide shot, slow push in", chars=["qinshuang", "erniu"], night="eve",
         comp=f"wide shot from a little above standing eye height, like the picture, along the row of earth heaps: {QIN}, framed full figure, already standing upright from the first frame with {CARRIED}, her right arm locked round his legs, striding toward the left edge of the frame, her face in profile to screen left, her eyes on the way ahead, never the lens; cross and embarrassed, not smiling: brows drawn, mouth tight, lips moving fast between words; a few steps behind her at the right {ERNIU_MUD}, {TUBE} in his right hand, following, his lips pressed shut, not smiling, never the lens; behind them, soft, the row of earth heaps running away to the right in the low orange evening light; {HANDS}; exactly three people, the man over her shoulder seen only from behind",
         lines=[("qinshuang", "文弱書生，逞什麼能，挖什麼井！", "罵，嫌棄")],
         motion=f"Qin Shuang strides on toward the left with the man over her shoulder, her ponytail swinging, as she speaks; {quiet('Wang Erniu')}",
         zh="全景、慢推（照圖從略高於人眼往下看，審稿必改 3；送 `set-jingkeng-dui-l1`）：秦霜第一格已經把許硯扛在右肩上站直（他頭與手垂在她背後；背影，不點名、不送他的圖），大步往畫左（村子：圖上屋頂在左遠處）走、馬尾一甩一甩、罵；二牛提竹水筒跟在右後、嘴閉著、不笑。稿子『蹲下、一肩扛起來、站直、邁步』在第一格已經完成（一鏡一個動作；剪接照稿子剪在 s22 蹲下的一半）；跟拍改慢推"),
    dict(loc="jk_et", cam="Close-up, slow push in", chars=["qinshuang"], night="eve",
         comp=f"close-up of {QIN}, framed from the shoulders up with space above her head, walking, {CARRIED}, only his muddy back and one limp hand in the frame behind her shoulder, her ears flushed red, her face in profile to screen left, her eyes on the way ahead, never the lens; she is the only one whose face is in the frame; awkward and cross, not smiling: eyes fixed ahead, brows drawn, lips moving low and quick between muttered words; behind her, soft, only the wide evening sky, a willow with yellowed leaves and the dry field in the low orange light",
         lines=[("qinshuang", "在樹蔭下指一指就好，偏要自己下去。", "小聲，耳根紅")],
         motion="Qin Shuang hitches the man on her shoulder up once with a shrug, her eyes still on the way ahead, as she mutters",
         zh="近景、慢推（送免費裁切 `set-jingkeng-tian-l1`：傍晚的天、黃葉垂柳、乾田）：秦霜側臉朝畫左、眼睛看前面不看他，**耳根紅**（拍法 12：寫整個耳朵泛紅；好感帳第 32 集），把肩上的人往上顛一下、小聲嘀咕（可以有一點不自在，不笑）；肩後只見他沾泥的背與一隻垂下的手（不點名）。跟拍改慢推"),
    dict(loc="jk_et", cam="Wide shot, slow push in", chars=["qinshuang", "erniu"], night="eve",
         comp=f"wide shot from a little above standing eye height, like the picture, along the row of earth heaps: {QIN}, framed full figure, small, {CARRIED}, striding toward the left edge of the frame, her face in profile to screen left, her lips pressed shut, never the lens; a few steps behind her {ERNIU_MUD}, {TUBE} in his right hand, his lips pressed shut, not smiling, never the lens; the long low orange light and their long shadows across the furrows; {HANDS}; exactly three people, the man over her shoulder seen only from behind",
         lines=[("xitong", "叮。秦霜，好感加十二。", "冷，宣布"),
                ("xitong", "加十二。宿主差點死在井裡，才換到這些。", "冷")],
         panel=[("秦霜 好感 +12 → 41", "affection")],
         motion=f"the two of them walk on at the same pace toward the left; {quiet('Qin Shuang and Wang Erniu', 'their', plural=True)}",
         zh="全景、慢推（照圖從略高於人眼往下看；送 `set-jingkeng-dui-l1`；審稿建議 1：四鏡倒掛臉減成兩鏡，系統句畫外、不需要他的臉）：秦霜扛著他（背影，不點名、不送他的圖）、二牛提竹水筒跟在後，照原速往左走，兩人嘴閉著；低斜的橘光與長影子。稿子『臉被面前的淡藍光照亮』不拍（拍法 11）。面板「秦霜 好感 +12 → 41」由剪接疊上（好感帳第 32 集；系統的吐槽是本集鬥嘴）。稿子 c25 三句估約 11 秒，拆成 s25（系統兩句）與 s25b（心裡話），同第 31 集 c29"),
    dict(sid="s25b", loc="jk_et", cam="Insert close-up, slow push in", chars=[], night="eve",
         comp=f"low orange evening light from the left: insert close-up, the very first frame is already a close view of one limp mud-caked hand in a faded blue-grey sleeve hanging down and swinging gently with each step beside the back of a pair of black trousers and a striding leather boot, dust rising from the cracked earth; only the hand, the sleeve, the trousers and the boot are in the frame",
         lines=[("xuyan", "死不了……換得到一口水，就值得。", "心裡話，錄得近、輕，迷迷糊糊", "inner")],
         motion="the limp hand swings gently with each step and the boot strides on",
         zh="插鏡、慢推（**不送任何圖**、不寫地點，審稿建議 1）：第一格已經是一隻沾泥、藍灰袖子的手垂著、隨步子晃，旁邊是黑褲與大步走的皮靴、裂土揚起一點灰。許硯的心裡話（迷迷糊糊、錄得近）是畫外。`mkspec.py` 拿掉 d1 的地點句。從 c25 拆出（見 s25）"),
    dict(loc="jk_et", cam="Close-up, slow push in", chars=["xuyan"], night="eve",
         comp=f"close-up of {XU_MUD}, slung head down over a shoulder, his muddy cheek against the dark brown cloth of a jacket's back, his face upside down in the frame, his eyes half closed at first, never the lens; he is the only one whose face is in the frame; dazed, not smiling: lips pressed shut; behind him, soft, the wide evening sky and the long yellowed hanging branches of a willow in the low orange light",
         lines=[("xitong", "秦霜好感，突破四十。獎勵箱開啟：水車圖紙。", "冷，宣布")],
         panel=[("秦霜好感，突破四十", "affection"), ("獎勵箱開啟：水車圖紙", "reward")],
         motion=f"Xu Yan's eyelids part a narrow crack and his eyes rest on the empty air before his face; {SILENT_HE}",
         zh="近景、慢推（送 `-tian-l1`；背景照圖寫黃葉垂柳，審稿必改 5 A）：許硯倒掛的臉（草稿兩個種子都看『臉倒著、眼睛半閉、嘴閉著』，都不行就改用 s25 的全景構圖重拍），眼皮撐開一條縫、看著面前的空氣（拍法 36：寫 eyelids part，不寫 open），嘴閉著。面板「秦霜好感，突破四十」「獎勵箱開啟：水車圖紙」由剪接疊上（聖經〈系統〉第 32 集；開箱只在面板）。稿子 c26 兩句估約 9 秒，拆成 s26（系統）與 s26b（心裡話）；**畫面上沒有水車**（原版必修）"),
    dict(sid="s26b", loc="jk_et", cam="Close-up, slow push in", chars=["xuyan"], night="eve",
         comp=f"close-up of {XU_MUD}, slung head down over a shoulder, his muddy cheek against the dark brown cloth of a jacket's back, his face upside down in the frame, his eyes a narrow crack, never the lens; he is the only one whose face is in the frame; a faint stubborn hope, not smiling: eyes a narrow crack, brows drawn a little, lips pressed shut; behind him, soft, the wide evening sky and the long yellowed hanging branches of a willow in the low orange light",
         lines=[("xuyan", "水車……有了水車，深潭的水就上得來。", "心裡話，錄得近、輕", "inner")],
         motion=f"Xu Yan's brows draw together a little, his lips staying pressed together; {SILENT_HE}; he is thinking, not speaking",
         zh="近景、慢推（送 `-tian-l1`；背景照圖寫垂柳）：許硯的心裡話（接回 s07 的深潭），眉頭微微一收、嘴閉著、**不笑**（審稿建議：原本『嘴角動一下』精修會變成笑）（第二場結尾）。從 c26 拆出（見 s26）"),
    # ---- scene 3: the same day at dusk, the ancestral hall (the free set-citang-huang-l1: the doorway at dusk).
    dict(chapter="柳溪祠堂", loc="ct_men", cam="Medium shot, slow push in", chars=["shimujiang", "xuyan", "erniu"], night="dusk",
         comp=f"medium shot of the doorway from inside the hall, the lattice door leaves swung back: just inside the threshold {CARP}, framed from the waist up, already turned back three-quarter to screen left toward the doorway from the first frame, {ROLL} in his right hand, never the lens; gruff, not smiling: brows bunched, lips moving roughly between words; beyond him on the threshold at the left of the doorway {XU_PALE}, framed from the waist up, his face toward the carpenter, his lips pressed shut, never the lens, and at the right of the doorway {ERNIU}, {HOE} on his right shoulder, his lips pressed shut, not smiling, never the lens; behind them a dim passage and another lattice door glowing with the last orange dusk light; {HANDS}; exactly three people; the only hoe in the frame is Wang Erniu's",
         lines=[("shimujiang", "圖是好圖。可這輪子，要三百斤好木頭。", "粗啞")],
         motion=f"Carpenter Shi gives the rolled paper one shake toward Xu Yan as he speaks; {quiet('Xu Yan and Wang Erniu', 'their', plural=True)}",
         zh="中景（三人）、慢推（送免費的 `set-citang-huang-men-l1`：祠堂門口從裡往外看，格子門往兩邊推開、門外是昏暗的橘色暮光；本集新做，`citang_huang.py`）：**祠堂沒有外景圖**，稿子『門前三級石階、走上石階』改在門裡門檻邊：石木匠第一格已經跨進門檻、回身、右手拿圖卷（紙背朝外，拍法 38）朝許硯晃一下、粗啞地說；門檻上左邊許硯（洗過臉、臉色發白、袍子膝上乾泥）、右邊二牛扛鋤頭，嘴閉著、不笑。三個人三張臉（拍法 1）。跟拍改慢推。石木匠的墨線筆照定妝照寫成插在髮髻的木棍（同第 13–17 集）；短衣照定妝照寫淺褐偏卡其（`faded light tan`，跟二牛的褐色分開，審稿建議 10）；門外照圖寫門廊與另一扇透光的格子門、不寫天空（審稿建議）"),
    dict(loc="ct_men", cam="Medium shot over the shoulder, slow push in", chars=["xuyan"], night="dusk",
         comp=f"medium shot over a shoulder: {BACK_CARP}; one step beyond it in the left half of the frame {XU_PALE}, standing on the threshold, framed from the waist up, his left hand already braced on the dark wooden door frame from the first frame, his face three-quarter to screen right toward the man in the foreground, never the lens; worn out, not smiling: pale, brows level, eyes tired but steady, lips moving hoarsely between words; behind him, soft, the lattice door leaf and beyond the doorway a dim passage and another lattice door glowing with the last orange dusk light; {HANDS}; exactly two people, the one in the foreground seen only from behind",
         lines=[("xuyan", "我醒來就把它畫出來了。石師傅，這車做得出來嗎？", "啞")],
         motion="Xu Yan draws one slow breath, leaning on the door frame, as he speaks",
         zh="過肩中景、慢推（送 `-huang-men-l1`）：前景右是虛焦的褐色工作服肩背、皮圍裙的帶子與插木棍的灰髮髻（不點名、不送圖）；許硯在畫左半、左手扶著門框、喘一口氣、啞著聲問。稿子『抬頭看石木匠』不拍（一鏡一個動作）"),
    dict(loc="ct_q", cam="Medium shot over the shoulder, slow push in", chars=["shimujiang"], night="dusk",
         comp=f"medium shot over a shoulder: {BACK_XU}; one step beyond it in the right half of the frame {CARP}, framed from the waist up, {ROLL} held in his left hand from the first frame, his face three-quarter to screen left toward the man in the foreground, never the lens; frowning, not smiling: brows knotted, eyes narrowed, lips moving roughly between words; behind him, soft, only the plain candle-warmed back wall of the hall under the dark beam; {HANDS}; exactly two people, the one in the foreground seen only from behind",
         lines=[("shimujiang", "做得出。料呢？三百斤的整木，村裡上哪找？", "皺眉")],
         motion="Carpenter Shi raps twice on the rolled paper with the knuckles of his right hand as he speaks",
         zh="反打過肩中景、慢推（送 `set-citang-huang-qiang-l1`：梁下一面被燭光照暖的素牆，沒有牌位、沒有燭火）：前景左是虛焦的藍灰肩背與髮髻（不點名）；石木匠皺眉、左手拿圖卷、右手指節敲兩下、問。背景只用素牆：近門的反打不讓供桌與跪著的村民入鏡（他們在 s33 才出現）"),
    dict(loc="ct_men", cam="Medium shot, slow push in", chars=["erniu"], night="dusk",
         comp=f"medium shot of {ERNIU}, standing on the threshold, framed from the waist up, {HOE} on his right shoulder at first, his face three-quarter to screen right {off('right', SIDE_DOOR)}; glum, not smiling: a sullen frown, the corners of his mouth turned down, lips moving heavily between words; behind him, soft, the lattice door leaf and beyond the doorway a dim passage and another lattice door glowing with the last orange dusk light; {HANDS}; the only hoe in the frame is his",
         lines=[("erniu", "村裡的大樹，去年秋天就砍光了。", "悶，不笑")],
         motion="Wang Erniu sets the hoe down off his shoulder and leans on its handle as he speaks",
         zh="中景、慢推（送 `-huang-men-l1`）：二牛站在門檻上，把鋤頭從肩上放下來拄著，朝畫右外看不到的人（石木匠，不點名）悶悶地說；**不笑**（原版建議）。稿子『站在石階下』照沒有外景圖改在門檻；『抓後腦、搖頭』不拍（一鏡一個動作）"),
    dict(loc="ct_men", cam="Medium shot, slow push in", chars=["xuyan", "shimujiang"], night="dusk",
         comp=f"medium shot just inside the doorway, both framed from the waist up: on the left {XU_PALE}, {ROLL} already in his right hand from the first frame, his face three-quarter to screen right toward the carpenter, his lips pressed shut, never the lens; on the right {CARP}, his hands empty at first, his face three-quarter to screen left toward Xu Yan, never the lens; low and grim, not smiling: brows drawn, lips moving low between words; behind them, soft, the lattice door leaves swung back and beyond the doorway a dim passage and another lattice door glowing with the last orange dusk light; {HANDS}; exactly two people",
         lines=[("shimujiang", "這麼大的料，村裡只剩一根，就在頭頂上。", "壓低")],
         motion=f"Carpenter Shi raises his flat right hand, fingers together, up toward the roof above them inside the hall as he speaks low; {quiet('Xu Yan')}",
         zh="中景（雙人）、慢推（送 `-huang-men-l1`）：許硯在左、圖卷第一格已經回到他右手（稿子『塞回許硯手裡』在第一格完成）；石木匠在右平掌往頭頂上、堂內的方向一抬、壓低聲音說（單指會讀錯，拍法 32）；許硯嘴閉著。稿子『前景是半開的格子門』照圖：門往兩邊推開"),
    dict(loc="ct_l", cam="Point-of-view wide shot, slow push in", chars=[], night="dusk",
         comp=f"point-of-view shot from the doorway at standing eye height, like the picture: the thick dark main beam running across the top of the candle-warmed back wall, below it the tops of a row of plain dark wooden tablets and a few thin incense sticks, a thin thread of incense smoke rising toward the beam in the candlelight; only the beam, the wall, the tablets and the smoke are in the frame",
         lines=[("xuyan", "祠堂的梁……這是全村祖宗的屋頂。", "畫外，愣住")],
         motion=NOBODY + "a thin thread of incense smoke drifts slowly up toward the dark beam",
         zh="主觀、慢推（人眼高、水平，照圖；『抬頭看梁』交給推鏡與台詞，審稿建議；送免費裁切 `set-citang-huang-liang-l1`：牆頂一根粗大的深色主梁，裂紋筆畫已免費塗掉免得長字，下面一排素面牌位的頂與幾支香）：一縷香煙往梁上飄；許硯的台詞是畫外（主觀，嘴不入鏡）。牌位素面（聖經〈道具〉）。**沒有水車**"),
    dict(loc="ct_z", cam="Wide shot, slow push in", chars=["hanbo"], night="dusk",
         comp=f"wide shot on the grey stone floor before {ALTAR}: at the left end of the altar table {HAN}, framed full figure, already risen to his feet from the first frame, leaning on the staff, his face three-quarter to screen left toward the doorway beyond the left edge of the frame, never the lens; old and steady, not smiling: brows level, eyes grave, lips moving slowly between words; kneeling on the stone floor before the altar in two loose rows, their backs to us, facing the altar, {CT_VILLAGERS}, all framed full figure, their lips closed, never the lens, two of them lifting their heads; {HANDS}; exactly nine people",
         lines=[("hanbo", "許秀才，你們在門口說的，我都聽見了。", "蒼老，慢")],
         motion=f"Elder Han turns slowly from the altar toward the doorway beyond the left edge of the frame as he speaks; {quiet('The eight kneeling people', 'their', plural=True)}",
         zh="全景、慢推（送免費裁切 `set-citang-huang-tang-l1`：供桌那一側與青石地，不含門口）：韓伯第一格已經拄杖站起來、在供桌左端，慢慢轉向畫左外的門口（看門口，不寫門口的人）、蒼老地說；供桌前青石地上兩排跪著的八個村民（背對我們、面向神龕，各自衣色、年紀、男女不同：深梅紫衣白頭巾老婦（原本黑衣，跟錢家家丁同色）、本色麻老漢、深灰靛藍頭巾婦人、暗橄欖綠壯漢、鐵鏽紅年輕婦人、芥黃十歲男孩、褪綠七歲女孩（一個小髻，不綁紅繩小辮：那是小禾）、炭灰瘦中年（井坑那位，原本是炭灰五歲男孩：第 33 集 c05 要四個男人拉繩，審稿建議 9）；拍法 34），兩個抬起頭。稿子『約二十人』交給台詞與音效；『香爐冒煙』照圖是幾支香。稿子『竹杖一撐慢慢站起來、轉身』拆成第一格已經站起加轉身"),
    dict(loc="ct_z", cam="Medium shot, slow push in", chars=["hanbo"], night="dusk",
         comp=f"medium shot at the left end of the altar table, like the picture: kneeling on the stone floor just beyond the left end of the table, before the dark wooden post, {HAN_NOSTAFF}, side-on to us, framed from the waist up, his bamboo staff leaning against the end of the table, his face in profile to screen right toward the tablets on the table, never the lens; grave and sure, not smiling: brows level, eyes on the tablets, lips moving slowly between words; in the lower right foreground, soft, the bowed backs of two kneeling people before the table, a bent old woman with a white head cloth and a boy of about ten in a mustard-yellow jacket, their faces down; {HANDS}; exactly three people",
         lines=[("hanbo", "祖宗在上。求了三個月的雨，一滴都沒下。", "篤定")],
         motion=f"Elder Han lifts his face to the row of tablets as he speaks; {quiet('The two kneeling behind him', 'their', plural=True)}",
         zh="中景、慢推（送免費新裁 `set-citang-huang-zuo-l1`：左邊門扇與深色門柱、供桌左端、左燭、兩塊牌位、香爐；審稿必改 6：`-zhuo` 正對供桌，跪在桌前側臉朝右放不進去）：韓伯第一格已經跪在**供桌左端**外、門柱前、竹杖靠在桌端（稿子『走到供桌前、靠竹杖、雙膝跪下』在第一格完成），側面朝畫右，抬臉對著桌上的牌位篤定地說；右下前景虛焦兩個低頭跪在桌前的背影（白頭巾老婦、芥黃男孩）。稿子『身後的村民跟著低頭』在第一格已經低著"),
    dict(loc="ct_z", cam="Medium close-up, slow push in", chars=["hanbo"], night="dusk",
         comp=f"medium close-up of {HAN_NOSTAFF}, kneeling, framed from the chest up with space above his head, his face in profile to screen right toward the tablets, never the lens; he is the only person in the frame; solemn, not smiling: candlelight on his face, eyes wet, brows level, lips moving slowly, one word at a time; beside him at the right, soft, the left end of the altar table, one white candle, two plain dark wooden tablets, their faces smooth and plain, and the bronze censer",
         lines=[("hanbo", "柳溪全村，願拆祠堂的梁，給孩子換一口水。", "一字一字")],
         motion="Elder Han bows his head slowly and deeply toward the tablets and raises it again as he speaks",
         zh="中近景、慢推（送免費新裁 `set-citang-huang-zuo2-l1`：供桌左端、左燭、兩塊牌位、香爐；審稿必改 6）：韓伯跪著、側臉朝畫右的牌位，燭光照臉，慢慢深深地低頭一拜再抬起、一字一字地說（本集的轉折句）。稿子『雙手按地、額頭磕下去』改胸以上看得見的一拜（拍法 32）；稿子『身後只有燭光與空白的牌位』照圖寫成他右邊的供桌左端、燭、兩塊素面牌位與香爐（他看的東西在框裡）。原版建議：這句的畫面要一直有人跪著（他跪著）"),
    dict(loc="ct", cam="Wide shot, slow push in", chars=["hanbo", "xuyan"], night="dusk",
         comp=f"wide shot at about chest height, level, like the picture: in the doorway at the left, between the lattice door leaves swung back, {XU_PALE}, standing on the threshold, framed full figure, {ROLL} in his right hand, his face toward the hall, his lips pressed shut, never the lens; just behind him in the dim doorway, soft, two more men, a lean man in a light tan jacket and a leather apron and a big young man in a coarse brown jacket with a hoe on his shoulder, their lips closed; kneeling in two loose rows on the stone floor in the lower right foreground before the altar, the nearer row cut at the knees by the bottom of the frame, {CT_VILLAGERS}, their lips closed, never the lens; at the front of them by the altar {HAN_NOSTAFF}, kneeling, framed full figure, his face turned back over his shoulder toward the doorway, never the lens; grave, not smiling: lips moving slowly between words; {HANDS}; exactly twelve people",
         lines=[("hanbo", "許秀才，祖宗的梁拆不拆，由你來說。", "回頭")],
         motion=f"the kneeling people turn their heads one by one toward the doorway at the left as Elder Han speaks; {quiet('Xu Yan, the two men behind him and the kneeling people', 'their', plural=True)}",
         zh="全景、慢推（胸口高、水平，照圖，審稿必改 3；送整張免費的 `set-citang-huang-l1`：左邊格子門往兩邊推開、門外是門廊與另一扇透著暮光的格子門，右邊供桌牌位蠟燭，牆頂主梁）：畫左門檻上許硯右手拿圖卷（紙背朝外）、嘴閉著；他身後門裡虛焦兩個人（皮圍裙的瘦漢與扛鋤頭的褐衣大個子：石木匠與二牛**不點名、不送圖**，免得一鏡超過三張有名字的臉，拍法 1）；右下前景青石地上兩排跪著的八個村民（同 s33；近排被畫框下緣切在膝蓋，圖上供桌前的地只有一窄條，審稿建議）一個一個回頭看門口；最前面的韓伯回頭說（接點 32→33：所有人回頭看門口的許硯）。稿子『從神龕旁往門口拍』照圖改成這張圖的機位（門在左、神龕在右，回頭就是朝畫左）"),
    dict(loc="ct_men", cam="Medium close-up, slow push in", chars=["xuyan"], night="dusk", act=2,
         comp=f"medium close-up of {XU_PALE}, standing in the doorway, framed from the chest up with space above his head, {ROLL} in his right hand at the bottom of the frame, half his face in warm candlelight from the right, the other half in the dim orange dusk light from the doorway, his eyes on the hall beyond the right edge of the frame, never the lens; that side of the frame is only {SIDE_DOOR} all the way to the edge, and he is the only person in the frame; shaken and silent, not smiling: brows drawn, eyes wide and still, lips pressed shut; behind him, soft, beyond the doorway a dim passage and another lattice door glowing with the last orange dusk light",
         motion=f"Xu Yan's fingers tighten slowly on the rolled paper and he swallows once; {SILENT_HE}",
         zh="中近景、慢推（送 `-huang-men-l1`）：許硯在門口，半張臉在燭光裡、半張在暮色裡，右手的圖卷在畫面下緣（中近景才看得到手，拍法 32），手指慢慢收緊、喉嚨動一下，看著畫右外堂內（不寫跪著的人）；嘴閉著、不回答，切在這裡（本集結尾；懸念交給第 33 集：他走進祠堂、穿過跪著的人）。無台詞"),
]

HEAD = [
    "- 重製版 r2、真人版（站主 2026-11-11「之後都用真人版」）：照 `docs/videos/zhong-tian-qu-qi-e032-r2/script.md`（c01–c37 對應 s01–s37；含「這版改了什麼」「2026-11-06 審稿後的修改」「真人版的改動」）；台詞一字不改，只改拍法；每鏡一個看得見的動作、一句一筆不拆半句、預設不笑。篇章設定 `production/r2-bible-e031-e040.md`（拍法 1–43 條、〈場景〉〈接點〉），帳照 `r2-bible-e011-e060.md`。**第 4 篇章〈旱年〉第二集**。",
    "- 內部工作編號 932（`hailuo/{ff,clips}-dh-e932.json`；之後的 `colab/runs/e932/extras.json`、`colab/runs/e932-live/spec.json`、工作資料夾 `~/mokaair-work/videos/zhong-tian-qu-qi-e932-dh/`）；發布 slug `zhong-tian-qu-qi-e032-r2`。不放集數、不放片名卡；s01 接第 31 集 s41（接點 31→32：同一刻，秦霜一扁擔挑飛鋤頭）；s37 交給第 33 集（接點 32→33：許硯拿著圖卷走進祠堂）。**s01 已照第 31 集 s41 實拍（9311101 精修片）重核**：家丁站在土埂右後方水塘的淺水裡、約十四人、臉朝畫左，二牛背影佔左下四分之一、鋤頭柄往左上斜。",
    "- 照第 31 集審稿後的寫法一開始就照做：`OFFSCREEN_SPEECH = False`；系統與心裡話的鏡，每張朝鏡頭的臉都寫不說話、嘴閉著；**對畫外的人說話寫「朝畫左／右外看不到的人」，那一側到邊緣只有景、畫面裡只有他一個人，不點名、不描述不在畫裡的人**（家丁只在 s01 遠景）；過肩前景是不點名、不送圖的背影；不掛東西；不寫 open；道具與接觸寫在第一格；寫人數；每張圖照它實際的樣子寫（下面〈軸線〉）。",
    "- **秦霜**：柴刀整集不寫（拍法 5；稿子『柴刀插腰帶右邊』拿掉）；扁擔 s01–s09（s10 第一格已還給村民）、竹水筒 s17–s19、s23 起右肩扛許硯、s24 起耳根紅。**王二牛**每鏡不笑（原版必修），臉寫曬黑、不寫泛紅（原版必修：肩上一片紅暈）；第一、三場只有他一把鋤頭，第二場不拿鋤頭。**村民**：壩前與井坑是第 31 集那五人（本色麻、炭灰、褪色靛藍、暗橄欖綠、深灰，沒有鋤頭）；祠堂八人八種衣色與年紀（不穿主角的顏色、沒有紅繩小辮）。**韓伯**、**石木匠**照第 15–17 集的寫法（石木匠的墨線筆照定妝照寫成插在髮髻的木棍）。本集沒有唐小棠、阿令。",
    "- **軸線（照圖）**：第一場同第 31 集翻轉的壩：柳溪的人在左邊壩腳的石邊土路上、壩在右；s01 秦霜在二牛**右邊**（兩幫人中間），鋤頭往**左**飛，s02 起土路上左到右是許硯、二牛、秦霜，秦霜背對壩朝畫左；s10 一行人沿土路朝鏡頭走（泥水小溝流向鏡頭，村子在鏡頭這邊）。第二場 `set-jingkeng-l1`：一排土堆從左前斜到右後、**左前那口坑最近、畫得最清楚**（木盆右邊還有一口，挑片時看第二口坑裡沒有長出人），許硯下的是左前那口（稿子『中間那一口』照圖改）；韓伯、二牛、秦霜從右邊來，秦霜扛人往左走（村子在左遠處）。第三場祠堂：門在左、供桌牌位在右、主梁在牆頂；**祠堂沒有外景圖**，稿子門前石階那段（c27–c31）改在門裡門檻邊；跪著的人面向右邊的神龕、回頭朝畫左看門口。",
    "- **時間與光**：第一場午後霧白的烈日（同第 31 集）；第二場 s11–s15 清晨（送本集免費做的清晨版 `-chen` 三張，文字寫淡淡的晨光與灰霧、**不寫方向**；審稿必改 1：原本早晚都寫太陽從左、又送同一張金黃圖），**s16 起傍晚**（送原本金黃的 `set-jingkeng-l1` 一族）——時間跳在 s15→s16 這一刀，不在 s16 鏡頭裡變光（原版 c21 同鏡光線跳是必修）；第三場黃昏：送本集新做的 `set-citang-huang-l1`（門口的白天改成昏暗橘色暮光、主梁上的裂紋筆畫塗掉），堂內燭光。",
    "- **原版必修**（聖經第 32 集）：坑裡不站人（s16 改成井底手與鎬的插鏡，不見人、不見臉）、村民都整個人站在田上；二牛每鏡不笑、不寫紅；許硯被拉上來拆成 s20 繩子繃緊（他不入鏡）與 s21 第一格已經躺在坑邊、眼睛半閉，不拍爬出來；全集沒有水車（圖紙只在面板與一卷紙背朝外的紙）。",
    "- 長鏡要買的秒數（BUY，錄音還沒錄，照字數與稿子的語速估；錄好後照第 31 集 `span931.sh` 量人聲長度重核）：s05、s07、s10、s11、s13、s21、s25、s26、s28、s33、s34、s35、s36 買 8 秒（s05、s26 照審稿建議：17 字、兩個停頓／系統 17 字加兩行面板）；s01、s16、s20、s37 買 5 秒；其餘照 `gen-dh.mjs` 的預設（說話 6 秒）。稿子 c25（三句約 11 秒）、c26（兩句約 9 秒）各拆成兩鏡（s25／s25b、s26／s26b）。",
    "- **表上的「秒」欄是 lint 估法**，比錄音短；剪接以錄音的人聲長度為準。",
]
FOOT = [
    "- **參考圖**（`assets/refs-live/`）：許硯 l1、angle-a（帶笑的 angle-b 整集不送；全景 s11、s36 只送 l1）；秦霜 l1、angle-a（全景 s01、s10、s23 只送 l1）；王二牛 l1、angle-a（全景 s10、s23 只送 l1）；韓伯 `hanbo-portrait-l1`、石木匠 `shimujiang-portrait-l1`（兩人都沒有角度圖）。s01 二牛的背影、過肩前景的背影（s05、s08、s13、s15、s28、s29）、s23、s25 肩上的人（只見背影）、s16、s25b 插鏡的手、s36 門裡的石木匠與二牛、村民、家丁都不送圖。",
    "- **場景圖**：壩送第 31 集做好的 `set-shangyou-ba-fx-l1`（s01）與裁切 `-fx-lu`（s02、s04、s07、s08、s10）、`-fx-shan`（s03、s06）、`-fx-jiao`（s05）、`-fx-ding`（s09）；井坑清晨送本集免費做的 `set-jingkeng-chen-l1`（s11）、`-kou-chen-l1`（s12、s14、s15）、`-dui-chen-l1`（s13）；傍晚送 `set-jingkeng-l1`（s20）與裁切 `set-jingkeng-kou-l1`（s17–s19、s22）、`-dui-l1`（s23、s25）、`-tian-l1`（s24、s26、s26b）、`-di-l1`（s21）；**s16、s25b 是插鏡，不送任何圖**；祠堂送本集新做的 `set-citang-huang-l1`（s36）與裁切 `-huang-men-l1`（s27、s28、s30、s31、s37）、`-huang-qiang-l1`（s29）、`-huang-liang-l1`（s32）、`-huang-tang-l1`（s33）、`-huang-zuo-l1`（s34）、`-huang-zuo2-l1`（s35）；`-huang-zhuo-l1` 本集不送（審稿必改 6）。",
    "- **本集新做的免費圖**（2026-11-18，`live-action/free-e031-e040/`，各跑兩次逐位元一樣，寫進 refs-live README）：`jingkeng_crops.sh`（四張井坑裁切）、`citang_huang.sh`＋`citang_huang.py`（祠堂黃昏版與五張裁切；審稿後加 `-huang-zuo`、`-huang-zuo2`）、`jingkeng_chen.sh`＋`jingkeng_chen.py`（審稿必改 1 的清晨版三張）。**不需要試鏡**。",
    "- 共用檔：沒有改（`build-r2.py` 的 `EN` 已有每個名字）；`gen-dh.mjs`、`pilot.py`、`cast.json` 不動。對畫外說話、對牌位說話、自言自語的鏡，精修文字的通用說話視線由本檔結尾的 `live_clips()` 換成 d1 的方向句（`GAZE_REFINE`）；本集沒有唐小棠，立領句與背影名字的替換不會觸發。",
    "- **d1 前置還沒做**（照協調者：等獨立審稿後）：`colab/runs/e932/extras.json`、`colab/runs/e932-live/{mkspec.py,spec.json}`（種子 9321101／9321102）、scratchpad `prep932.sh`（照 `prep931.sh`：錨點形式給第一段、swap_pictures 絕對路徑、逐鏡查送的圖、分隔句、`preflight-prompts.py`、否定名詞／會長字的名詞／掛著的東西／open／點名的畫外人掃描）與 `e932d1.sh`。",
    "- 配音：韓伯（Enceladus）與小禾以外的新聲音本集沒有；**韓伯的音高還沒量**（聖經第 43 條、〈還沒解決的〉第 10 條），第一次錄音時量，跟同場的石木匠（Schedar，110–175 Hz）要差至少 3 個半音。",
    "- 配樂：第一場低鼓（接第 31 集），s01 挑飛一個重音後換沉穩的 strings；第二場清晨乾冷的 drone，s19 拉繩起心跳般的低鼓，s23 扛起許硯換溫柔帶一點好笑的 cue，s26 開箱一個亮的重音；第三場低沉的大提琴，s32 看梁一個重音，s35 鼓一聲，s36 停在最高點不收。音效見 script.md〈音樂與音效〉（另外：鋤頭落在土路上、二牛往井裡喊、扛起來的一聲，都交給音效）。",
]

# Seconds to buy. No recordings yet (e932 has none): estimated as e931 (a 6 s shot holds about 5.9 s of speech; e930/e931 ran
# about 2.6-3.7 characters a second; 19 or more characters, two-line shots, Elder Han's slow lines and the script's long
# shots buy 8). Re-check against the recordings' speech spans as e931 did (span931.sh) before d1.
# 8 s: s07 (18 characters and a head shake), s10 (the script's 長鏡: the walk), s11, s13, s33, s34, s35, s36 (Elder Han: 「每句
#      慢、句句篤定」; s35 the script's 長鏡, word by word), s21 (11 characters with two long pauses, breathy), s25 (two system
#      lines, 25 characters), s28 (19, hoarse).
# 5 s: s01 (no line: the flick), s16 and s20 (no line), s37 (no line, the episode's held last look).
# 6 s (gen-dh's default for a spoken line): every other shot.
BUY = {"s05": 8, "s26": 8, "s07": 8, "s10": 8, "s11": 8, "s13": 8, "s21": 8, "s25": 8, "s28": 8, "s33": 8, "s34": 8, "s35": 8, "s36": 8,
       "s01": 5, "s16": 5, "s20": 5, "s37": 5}


# ---- the refine text (as e023-e031): hailuo/clips-dh-e932.json column 0 is the motion text refine-prep.py sends with a picked
# d1 draft. gen-dh.mjs opens every clip that lists tangxiaotang with the CG-era collar sentence and names her; e032 has no
# Tang Xiaotang, so that part of live_clips() (kept from e031 so the two stay one function) finds nothing. Column 1 is
# recomputed. The d1 prep will hand stage 1 the anchor form (anchor_form(), e028 review 必改 1; rule 39).
COLLAR = "Tang Xiaotang's high stand-up collar stays closed at her throat. "
FRONT_TANG = set()
# rule 31 (e030 review 建議 10): gen-dh's speaking gaze names "the person he/she is speaking to", who is not in the frame of these
# shots (or is nobody: s21 murmurs, s23-s24 she curses to herself, s34-s35 he speaks to the tablets); the refine text gets d1's
# direction. anchor_form() puts gen-dh's words back for stage 1.
GAZE_GEN = {"he": "turned toward the person he is speaking to, face in profile or three-quarter profile, eyes on that person",
            "she": "turned toward the person she is speaking to, face in profile or three-quarter profile, eyes on that person"}
_L = "his face three-quarter to screen left toward someone out of sight beyond the left edge of the frame, his eyes on that spot"
_R = "his face three-quarter to screen right toward someone out of sight beyond the right edge of the frame, his eyes on that spot"
_AHEAD = "her face in profile to screen left, her eyes on the way ahead"
_TABLETS = "his face in profile to screen right toward the row of plain tablets on the altar table, his eyes on them"
# sid -> (pronoun, the direction sentence)
GAZE_REFINE = {
    "s03": ("he", _R), "s06": ("he", _L),
    "s11": ("he", "his face turned down toward the earth heaps he passes, his eyes on them"),  # review 建議
    "s09": ("he", _R),
    "s18": ("he", _R),
    "s21": ("he", "his half-closed eyes on nothing, his face tipped up toward the evening sky"),
    "s23": ("she", _AHEAD), "s24": ("she", _AHEAD),
    "s30": ("he", _R),
    "s33": ("he", "his face three-quarter to screen left toward the doorway beyond the left edge of the frame, his eyes on it"),
    "s34": ("he", _TABLETS), "s35": ("he", _TABLETS),
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


# e928 review 必改 1 (rule 39): ref2manifest.mjs (stage 1) strips gen-dh's refine anchor with ANCHOR_FF, and the wording
# live_clips() writes no longer matches it. The d1 prep hands stage 1 the anchor form of the live file (this), then puts the
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
