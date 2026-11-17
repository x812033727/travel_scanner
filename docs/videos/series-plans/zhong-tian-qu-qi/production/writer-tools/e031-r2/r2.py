"""Episode 31 remake (r2): the writer spec for ../e001-r2/build-r2.py. Source: docs/videos/zhong-tian-qu-qi-e031-r2/script.md
(c01-c41; the CG-era r2 script), including its sections 「這版改了什麼」 and 「2026-11-06 審稿後的修改」, which override the tables.
Every line is the script's, word for word; only the staging changes. c21 gets a silent front-face shot after it (s21b) and c29's
three recordings are split into s29 and s29b (below): 43 shots.
Bible: production/r2-bible-e031-e040.md (arc 4 〈旱年〉: rules 1-30 as corrected and the new rules 31-43, 〈場景〉, 〈接點〉 30->31
as corrected 2026-11-17 to the layout actually shot in e030 s41 fix2 9301301, 31->32, the props, people, picture and 原版必修
tables) and r2-bible-e011-e060.md (accounts: A-ling +4 -> 32; the drought quest; the rice seed). The FIRST episode of arc 4:
the Xu yard at dusk on the fifty-third day (the same moment as e030 s41), the same night at the well, then three months later,
early spring in a drought: the same yard in the hot afternoon, the dry stream bed and the Qian family's dam upstream.

Written from the start the way e030-r2/r2.py stands AFTER its independent review (../e030-r2/review.md: the 5 必改 and the
建議 the coordinator took; the bible folds them into rules 21, 31, 32, 35, 36, 39), with the task file's lessons and 注意:
- OFFSCREEN_SPEECH = False (rule 15): every shot with an off-screen line, a thought, a system line or Tang Xiaotang speaking from
  behind writes the silence of each face on screen (quiet(), SILENT_HE).
- Rule 31: a line said to someone outside the frame is written "toward someone out of sight beyond the left/right edge of the
  frame", that side set only all the way to the edge, and the speaker the only person in the frame (off()). No person who is not
  in the first frame is named or described anywhere: the Tang carriage, Tang Wanjin, Steward Zheng, Qin Shuang, little Xiaohe,
  Wei Shaoqing's white horse, the retainers off the dam are never written. A look at a place names the place (the yard gate, the
  well, the house door, the bowl, the dam). Over-the-shoulder foregrounds are unnamed backs with no picture (rule 2).
- Tang Xiaotang (rule 40): her lines (s05, s19, s22) are from behind, in the middle of the frame, facing straight away from us,
  head still, exactly two round buns (TBACK; nospeak; the spec drops her pictures); s20, s30 she listens from behind; in the
  wides s04, s24 she is a small back (no picture, not in `chars`). The bible's suggested silent front face is used once: s21b,
  after the sprouts (lips pressed together, a bright small smile: c22 「本鏡可以笑」), a close-up between the insert s21 and the
  medium back shot s22 (rule 40: front face and back are different shot sizes). The script's t2 high collar, 「下巴以上」,
  「襦裙從立領到腰一件闔上」, 「袖子用粉帶束起」 and the gold abacus at her waist are CG wording and are not used (rules 4, 20).
- A-ling (rule 21): s01 sends her bare portrait (aling-portrait-l1 + aling-angle-a-l1) with the gauze written as the thing itself
  (VEIL_BLOWN, from e030 s38/s39/s41); her left hand draws it back over her nose and mouth (the bible's c01). s02-s04 (only s03,
  s04 show her) send aling-veil-portrait-l1. At night (s07-s17) the veil is off, folded on her knee (GAUZE_KNEE; bare portrait).
- Wei Shaoqing (rule 30): s02-s04 only, the fan always closed (FAN), NOSMILE in all three (the bible: 咬牙、退場). The white horse
  is NOT shot (bible 〈還沒解決的〉 2): s02's background is the gate and the mud wall beside it; s04 he turns away to the right
  behind the back wall and out of the frame; the hoofbeats are a sound.
- Wang Erniu (原版必修: laughing at bad news; two Erniu in the background): not smiling in every shot (brows knotted, panting, jaw
  set); one hoe in the whole episode, his (HOE); the five villagers are grey-blue, each a different age and burden, and carry
  no hoe (VILLAGERS). Qian Yuanwai: his robe's front plain brocade (原版第 35 集 tag); s34 may fake-smile, s36 may sneer (the
  script); the retainers (rule 34) are one uniform, only far, side-on or in a row on the dam, never in a close shot.
- One visible action per shot (rule 32); the previous action done in the first frame; the hand's action in a frame where it is
  seen; hand gestures with the flat hand, fingers together. The script's follows, pans and walks are slow push-ins or a held
  frame. No word "open" (rule 36: the cloth is "lifted", the fist "uncurls"); nothing hung (rule 33: no lantern on the eaves, no
  carriage lantern: s07 Xu Yan comes out of the house door with one clay oil lamp, LAMP, and leaves it on the doorstep).
- Things are written as they should be drawn: the bowls, the rice grains with white sprouts, the gauze, the grain sacks; no
  water wheel anywhere (原版必修; the pictures have none). No blue light (rule 11): s14, s28's panels are the editor's.
- Inserts (rule 35): s18 (the buds on a twig) and s21 (the red clay bowl) open on the light and the subject: LOC["han_e"] is
  only H0, kept so gen-dh's SET ("courtyard") sends the yard picture that spec.json swaps for a crop (s18 the bare branches and
  the sky, s21 the ground), and mkspec.py strips "H0: " from their d1 prompts (as e030 s17/s22/s32). A shot sending no picture
  at all fails Ref2VA (the pseudo preflight's picture-list ERROR on a first draft of s18), so s18 sends a branches crop.

THE AXES (rules 29, 42: the pictures decide):
- Scene 1, the yard at dusk and the same night (set-xujia-yuan-dong-qing2-l1 / set-xujia-yuan-ye-dong-l1): the house and the
  firewood on the LEFT, the gate in the MIDDLE of the back wall, the bare tree behind the wall right of the gate, the low wall
  and leaning planks on the RIGHT, the well in the FRONT RIGHT; the low sun at the upper right behind. The hand-over (bible
  30->31 corrected 2026-11-17, e030 s41 fix2 9301301): Tang Xiaotang in the middle foreground, her back to us, a flat wooden box
  held against her chest (BOX); A-ling at the well front right, her hand on the windlass, the gauze on her left ear; Xu Yan at
  the left before the house, two-thirds back, facing the gate; Wei Shaoqing in the gate. So A-ling looks screen LEFT to the gate
  and Wei screen RIGHT to the well (as e030 s39/s40); Xu Yan, before the house, looks screen right to Tang Xiaotang and the
  well. At night A-ling sits on the well's rim, Xu Yan crouches and then sits at her right (screen right of her in the
  two-shot, she looks screen right to him, he screen left to her).
- Scene 2, three months later (set-xujia-yuan-han-l1, filed 37038: only the field beyond the wall changed to cracked bare earth;
  the picture's sun is low and golden, so the script's 「正午」 is written "hot hazy afternoon, low sun from the upper right"
  (bible 〈還沒解決的〉 6). The bare tree stays bare (the buds only in the s18 insert). Tang Xiaotang draws water at the well
  (front right); Xu Yan stands before the house (left) with the red clay bowl in his hands: the picture has no low table and no
  bench, so they are not written (as e030); Wang Erniu comes in through the gate in the middle of the back wall and stops at Xu
  Yan's right. Xu Yan looks screen right to them; Erniu and Tang Xiaotang look screen left to him.
- Scene 3: the dry stream bed (set-ganxi-l1, filed 37038: dry mud plates, the plank bridge, willows): the group walks from the
  left toward the right (upstream). The dam (set-shangyou-ba-l1, NOT FILED in refs-live when this was written: round 3 of the
  screen test. Its out-r3 seed 37042, looked at half size, and live-action/free-e031-e040/clean_shangyou_box.py (another
  session's, 20:38, "from seed 37042") suggest that is the pick: a long dam of stacked brown hemp sacks on a fieldstone footing
  running from the left foreground diagonally to the middle right, the muddy pond behind it on the left, a ditch of water along
  its right end, bright green rice on the right, wooded hills; no dry bed in the frame). DAM is written to fit both the round-3
  prompt and that picture. Close shots keep the bible's 31->32 axis: the Liuxi side LEFT, the dam RIGHT: Xu Yan and Erniu look
  screen right to the dam, Qian Yuanwai on the dam looks screen left and down; the wides s32, s41 look at the dam "like the
  picture". When the picture is filed, check its left/right against this and the 31->32 row (bible: 照圖改這張表), cut its
  close crops, then fix LOC["ba"]/["ba_c"] and the s32/s41 compositions to the picture before the d1 prompts are made.

PLACES (gen-dh SET takes the FIRST pattern in its list order that matches; spec.json swaps with absolute paths):
- "courtyard" (scenes 1 and 2) gives set-xujia-yuan-l3, swapped per shot for: -dong-qing2-l1 (s04), -dong-jing-l1 (s01, s03),
  -dong-men2-l1 (s02, s05), -dong-wu2-l1 (s06); -han-l1 (s24), -han-jing-l1 (s19), -han-wu-l1 (s20, s22, s23, s26, s28, s29,
  s29b, s30), -han-qiang-l1 (s21b, s27), -han-men-l1 (s25), and for the s21 insert a cleaned ground crop
  set-xujia-yuan-han-di2-l1 (NOT MADE: refs-live README warns -han-di-l1 has the leaf-shaped stone that turned e030 s32's paper
  into a leaf; make it free with colab/runs/e930-live/fix1/clean_di.py's method before s21's d1).
- "night yard of the Xu farmhouse" (s07-s17) gives dh-set-xujia-yuan-ye-t1, swapped for set-xujia-yuan-ye-dong-l1 (s07, s08) and
  -ye-dong-jing-l1 (s09-s17). -ye-dong-l1 still has the dark blank board right of the doorway (README): s07, s08 write "the plain
  stone wall of the farmhouse"; or paint a -ye-dong2-l1 with clean_yard.py (a) before d1 (free).
- "stream" (scene 3) gives dh-set-liuxi-he-t1, swapped for set-ganxi-l1 (s31) and set-shangyou-ba-l1 (s32-s41; after the pick its
  close crops, free, as the bible says, for s33-s40). No "channel", "sluice", "pool", "spring field" in any prompt (other SET rows).
- s18: set-xujia-yuan-han-shu-l1 (NOT MADE: free, -han-l1 cropped as -dong-shu-l1, crop=480:270:560:0: the bare branches
  against the glowing sky, a corner of the gate roof at the lower left; looked at in scratchpad, usable).
Shared files: none changed (build-r2.py's EN has "A-ling", "Wang Erniu", "Qian Yuanwai", "Wei Shaoqing"; gen-dh.mjs, pilot.py,
cast.json untouched). Not written here (the prep step after this, as e930): colab/runs/e931/extras.json, colab/runs/e931-live/
{mkspec.py,spec.json} (swap_pictures, drop_pictures, the d1 gaze sentences), prep931.sh, recordings.
"""
EP = 931  # internal working number; the published slug is zhong-tian-qu-qi-e031-r2
SLUG = "zhong-tian-qu-qi-e031-r2"
EP_TITLE = "認錯人了，溪斷了（重製版 r2）"
OUTLINE_SECONDS = 228  # script.md: about 228 s, 41 shots (17 + 13 + 11)
TARGET_MINUTES = [3, 4]
TITLE = "認錯人了，溪斷了｜種田娶妻打天下 第31集（重製版）"
DESCRIPTION = "井邊的面巾被風吹開，魏少卿僵在院門口。阿令把面巾拉回去：認錯人了，公子請回。「這張臉，我記下了。」當夜許硯端湯到井邊，她只肯說一句：他是在一道很高的牆裡見過我的。「好，不問。」三個月後，一滴雨都沒下，箱底那袋稻種冒出白芽，二牛卻衝進院子：柳溪斷了。系統下旱災任務：十日內讓柳溪的田見水。上游的乾溪床盡頭，錢家用土袋築了壩，錢員外說糧價再漲三成，留下十二個拿棍子的家丁。二牛舉起鋤頭衝過去——《種田娶妻打天下》第 31 集（重製版）。"
THUMB = ("柳溪斷了", "s41")
CHARACTERS = ["xuyan", "aling", "weishaoqing", "tangxiaotang", "erniu", "qianyuanwai", "xitong"]
MINOR = {}
MUSIC = "one cue per scene: low uneasy strings on a farm yard at sunset, cut off by distant hoofbeats, then a gentle night melody by a well with one soft chime; then a dry hot low drone in a parched yard, one bright note when seeds sprout, cut off by a shout, one heavy chime; then a low dry drum on a dry stream bed, one heavy accent at the sight of a dam, the drum building and stopping at its peak; ancient Chinese rural drama, no vocals"

# Places.
Y0 = "In the courtyard of the Xu farmhouse at the end of the same cold clear early-winter day, the sun low in the west"
DUSK = "low golden evening sun from the upper right behind, long shadows stretching toward the lower left across the earth"
N0 = "In the night yard of the Xu farmhouse later the same cold clear early-winter night"
NIGHT = "cool silver moonlight from above, the yard dark and still"
H0 = "In the courtyard of the Xu farmhouse three months later, on a hot dry early-spring afternoon in a time of drought"
HOT = "hazy low afternoon sun from the upper right behind, long shadows toward the lower left across the cracked earth, fine dust drifting on the hot wind"
G0 = "On the dry bed of the Liuxi stream on the same hot afternoon"
B0 = "At the upper end of the dry stream bed on the same hot afternoon, before the Qian family's dam"
DAM = ("a long rough farmers' dam of stacked brown hemp sacks of earth on a footing of rough fieldstones across the stream bed, "
       "uneven and handmade; behind it a still pond of muddy brown water; along its right end a narrow freshly dug ditch carrying "
       "water off to a field of bright green young rice on the right; wooded green hills beyond")
BAKE = "hazy white afternoon sunlight, dust in the hot air"
LOC = {
    "yard": f"{Y0}: the yard exactly as in the picture: the farmhouse on the left, the yard gate in the middle of the back wall, the well in the front right; {DUSK}",
    "yard_j": f"{Y0}, beside the round stone well with its wooden windlass in the front right of the yard, a few planks leaning against the low mud-and-stone wall behind it; {DUSK}",
    "yard_m": f"{Y0}, by the yard gate of weathered planks under its small tiled roof in the middle of the low mud-and-stone back wall; {DUSK}",
    "yard_w": f"{Y0}, before the thatched mud-and-stone farmhouse on the left of the yard, its dark doorway and split firewood stacked against its wall; {DUSK}",
    "night": f"{N0}: the yard exactly as in the picture: the farmhouse on the left with the plain stone wall beside its dark doorway, the yard gate in the middle of the back wall, the round stone well in the front right; {NIGHT}",
    "night_j": f"{N0}, beside the round stone well with its wooden windlass in the front right of the yard, the low mud-and-stone wall behind it; {NIGHT}",
    "han": f"{H0}: the yard exactly as in the picture: the farmhouse on the left, the yard gate in the middle of the back wall, the well in the front right, cracked bare earth with a few dead stalks beyond the low wall; {HOT}",
    "han_j": f"{H0}, beside the round stone well with its wooden windlass in the front right of the yard, the low mud-and-stone wall behind it; {HOT}",
    "han_m": f"{H0}, by the yard gate of weathered planks under its small tiled roof in the middle of the low mud-and-stone back wall, cracked bare earth beyond it; {HOT}",
    "han_w": f"{H0}, before the thatched mud-and-stone farmhouse on the left of the yard, its dark doorway and split firewood stacked against its wall; {HOT}",
    "han_q": f"{H0}, before the low mud-and-stone wall of the yard with cracked bare earth and a few dead stalks beyond it, hazy low afternoon sun from the right",
    "han_e": H0,  # rule 35: kept only so gen-dh's SET ("courtyard") sends the yard picture; spec.json strips it from s21's d1
    "ganxi": f"{G0}: the stream bed exactly as in the picture: plates of dry cracked mud where the water ran, the low plank bridge with nothing under it, the willows on the banks; {BAKE}",
    "ba": f"{B0}: {DAM}; {BAKE}",
    "ba_c": f"{B0}, on the cracked earth of the gully floor below the dam of fieldstones and brown hemp sacks; {BAKE}",
}
LIGHT = {
    "dusk": "the low golden evening sunlight stays unchanged",
    "night": "the cool moonlight stays unchanged",
    "hot": "the hazy hot afternoon light stays unchanged",
}
# bible rule 15: no "<X> speaks off screen" / "the system voice speaks off screen".
OFFSCREEN_SPEECH = False

# Repeated wording (each prop is one object, written the same way every time).
XU_D = "Xu Yan, in his faded blue-grey scholar's robe patched at one elbow, its sleeves down"
XU_COAT = "Xu Yan, in his faded blue-grey scholar's robe patched at one elbow, an old plain grey cloth outer coat over it"
XU_UP = "Xu Yan, in his faded blue-grey scholar's robe patched at one elbow, its sleeves rolled up to the elbows, dust on its hem"
WEI = ("Wei Shaoqing, in his sapphire-blue brocade robe woven with gold thread, a white jade pendant at his waist, a small green "
       "jade ornament at the front of his topknot")
FAN = "one closed folding fan in his right hand, its dark bamboo ribs pressed tight together like a short slim stick"
ALING = ("A-ling, in her plain grey-white cotton dress with long sleeves covering her wrists, her black hair in a high bun with "
         "one plain wooden hairpin")
VEIL = ("a veil of soft, finely woven pale grey gauze over her nose, mouth and chin, tied behind both ears, falling down to the "
        "middle of her chest")
# rule 21 (e030 review 必改 1): with the bare portrait the gauze is the thing itself, on its tie over her left ear
VEIL_BLOWN = ("a long strip of soft, half-transparent pale grey gauze hangs from a thin grey tie looped over her left ear only, its "
              "free end blown out past her left cheek and shoulder in the wind, her nose, mouth and chin bare from the first frame")
VEIL_LOOSE = "the loose strip of pale grey gauze"
GAUZE_KNEE = "a folded square of pale grey gauze on her knee"
ERNIU = "Wang Erniu, in his coarse brown cross-collared short jacket with the sleeves rolled up, sweat on his brow"
HOE = "one hoe with a plain wooden handle and an iron blade"
QIAN = ("Qian Yuanwai, short and portly with a round face and a thin eight-shaped moustache, in his dark gold silk robe with "
        "roundel patterns, the front of the robe plain brocade, three gold rings on his fingers")
# rule 34: five villagers, grey-blue (never Erniu's brown), each a different age and burden; no hoe among them (原版必修)
VILLAGERS = ("five more people in Song-dynasty grey-blue cross-collared homespun short jackets, cloth head wraps and cloth shoes: a "
             "white-haired old man in faded grey-blue and a lean middle-aged man in dark grey-blue, each with one wooden carrying "
             "pole on his shoulder and an empty wooden bucket at each end of it; a thin boy of fifteen in pale grey-blue, a broad "
             "middle-aged man in slate blue and a middle-aged woman in grey-blue with a faded indigo head cloth, each with one "
             "bamboo basket on the back and one wooden spade in hand")
RETAINERS = ("twelve men in identical Song-dynasty black cross-collared short jackets, black cloth head wraps and cloth shoes, each "
             "holding one plain wooden staff")
BOX = "one flat plain wooden box"  # the hand-over: e030 s41 fix2 drew her holding it
BUCKET = "one round wooden bucket of well water with a rope handle"
MUD_BUCKET = "one round wooden bucket half full of muddy yellow water"
LAMP = "one small clay oil lamp with one flame"
SOUP = "one rough brown clay soup bowl with steam rising from it"
EMPTY_BOWL = "one rough brown clay soup bowl, empty"
REDBOWL = "one red clay bowl covered with a wet white cloth"
SPROUTS = "a layer of rice grains, each grain with one tiny white sprout"
REDBOWL_SPROUTS = f"one red clay bowl holding {SPROUTS}"
SACKS = "five brown hemp grain sacks stacked on a plain wooden cart bed"
MULE = "the head and neck of one grey mule at the right edge of the frame"
HANDS = "their hands hold only what is described here"
INSERT_LIGHT = "hazy low afternoon light from the right"
SKY_LIGHT = "hazy low afternoon sun from the upper right behind the branches"
SILENT_HE = "He says nothing in this shot: his lips stay pressed together from the first frame to the last, his jaw still, no talking, no mouthing words"
NOBODY = "Throughout the shot the set layout stays as it is. The pictures fix the place and the objects only, never the mood. "
TBACK = ("one young woman seen only from behind, appearing only once: the back of her head with every strand of her black hair "
         "combed smooth and gathered up into just two round buns set high on her head, one bun on each side, one short pink "
         "silk ribbon wrapped around each bun, the nape of her neck bare and clear above a pink inner collar, and her light "
         "peach-pink silk shoulders; the back of her head facing straight away from us the whole time, her head still, her ear "
         "the furthest round her head we ever see")
HEADSTILL = "the young woman with the two high round buns keeps her head still, facing straight away from us, the back of her head toward us the whole shot"
# rule 40: the one silent front face (s21b), her l1 costume (rule 4)
TANG_FACE = ("Tang Xiaotang, a young woman of eighteen with a round soft face and big round eyes, in her peach-pink silk "
             "cross-collared short jacket closed at the neck, her black hair in two round buns tied with short pink ribbons")
# rule 2: over-the-shoulder backs, unnamed, no picture
BACK_ALING = ("at the left edge of the frame, cut by it, soft and out of focus, only the back of one grey-white cotton shoulder and "
              "the back of a high black bun with one plain wooden hairpin, the back of her head toward us the whole shot")
BACK_ERNIU = ("at the right edge of the frame, cut by it, soft and out of focus, only the back of one broad shoulder in a coarse "
              "brown jacket with a wooden hoe handle resting on it and the back of a man's head, toward us the whole shot")
BACK_XU = ("at the left edge of the frame, cut by it, soft and out of focus, only the back of one shoulder in a faded blue-grey "
           "robe and the back of a man's topknot, toward us the whole shot")
BACK_QIAN = ("at the right edge of the frame, cut by it, soft and out of focus, only the back of one shoulder in dark gold brocade "
             "and the back of a round head with a small topknot, toward us the whole shot")
# set-only sides (the picture of each place, all the way to the edge)
SIDE_WALL = "the low mud-and-stone wall and the leaning planks"
SIDE_NWALL = "the dark low mud-and-stone wall"
SIDE_EARTH = "the cracked bare earth of the yard"
SIDE_GULLY = "the cracked earth of the dry gully"


def quiet(who, pr="his", plural=False):
    verb = "say" if plural else "says"
    return f"{who} {verb} nothing in this shot: {pr} lips stay pressed together from the first frame to the last, no talking, no mouthing words"


def only_tang():
    return "she is the only young woman with two high round buns in the frame"


def alone(rest, where, frame="framed from the waist up", shot="medium shot", lead=""):
    """Tang Xiaotang from behind, in the middle of the frame (not at an edge: the pickers' cheek at the frame edge)."""
    return f"{shot} from close behind{lead} {TBACK}, {where} in the middle of the frame, {frame}, facing straight away from us; {only_tang()}; {rest}"


def off(side, what, he="he"):
    """A line to someone outside the frame: the gaze, that side set only, and the only person (rule 31)."""
    edge = f"the {side} edge of the frame"
    return (f"toward someone out of sight beyond {edge}, never the lens; that side of the frame is only {what} all the way to the "
            f"edge, and {he} is the only person in the frame")


SHOTS = [
    # ---- scene 1: the fifty-third day at dusk, the Xu yard (30->31: the same moment as e030 s41).
    dict(chapter="許家井邊，傍晚到當夜", loc="yard_j", cam="Medium close-up, slow push in", chars=["aling"], night="dusk",
         comp=f"medium close-up of {ALING}, standing beside the round stone well, framed from the chest up with space above her head, {VEIL_BLOWN}, her left hand already raised to the free end of the gauze at her left cheek from the first frame, her face three-quarter to screen left, her eyes on the yard gate beyond the left edge of the frame, never the lens; that side of the frame is only {SIDE_WALL} all the way to the edge, and she is the only person in the frame; cold and still as well water, not smiling: level unblinking eyes, brows level; behind her, soft, the low mud-and-stone wall and the planks leaning against it in the low evening sun; {HANDS}",
         lines=[("aling", "認錯人了。公子要找的人，不在這裡。", "冷得像井水，隔著面紗")],
         motion=f"A-ling's left hand draws {VEIL_LOOSE} back across her nose, mouth and chin, and she speaks from under it",
         zh="中近景、慢推（送 `set-xujia-yuan-dong-jing-l1`；阿令送**沒面巾**的 `aling-portrait-l1`＋`aling-angle-a-l1`，接點 30→31）：第一格灰紗只掛在左耳的細繩上、吹到左頰外（拍法 21：面巾寫成實物，同第 30 集 s38–s41），左手已經捏著紗的尾端；她左手把灰紗拉回遮住口鼻下巴、隔著紗朝畫左外的院門說（不點名魏少卿；那一側到邊緣只有泥牆與靠牆的木板）。稿子『把水桶放到井沿上』在第一格已經完成（一鏡一個動作；中近景看不到桶，不寫）；『在耳後壓好』交給剪接。稿子的『井在畫面左、院門在右』照圖反過來（拍法 29、42）"),
    dict(loc="yard_m", cam="Close-up, slow push in", chars=["weishaoqing"], night="dusk",
         comp=f"close-up of {WEI}, standing in the yard gate, framed from the chest up with space above his head, {FAN} held still in mid-air before his chest from the first frame, his face three-quarter to screen right toward the well beyond the right edge of the frame, never the lens; that side of the frame is only the low mud-and-stone wall all the way to the edge, and he is the only person in the frame; stunned and tight, not smiling: his peach-blossom eyes wide and fixed, brows drawn together, lips moving tightly between words; behind him, soft, the swung-back plank gate and the low mud-and-stone wall beside it in the low evening sun; {HANDS}",
         lines=[("weishaoqing", "你明明是……我在京裡見過這張臉！", "僵著，聲音發緊")],
         motion="Wei Shaoqing takes half a step forward into the yard as he speaks, the closed fan staying still in mid-air",
         zh="近景、慢推（送 `set-xujia-yuan-dong-men2-l1`）：魏少卿在院門口，合著的扇子第一格停在胸前半空（拍法 30），往院子裡跨半步、望著畫右外的井說（不點名、不描述阿令；那一側到邊緣只有泥牆）；不笑（聖經：本篇他的三鏡都 NOSMILE）。稿子『身後院門外的泥牆與馬的半個身子』只寫院門與泥牆：白馬不拍（聖經〈還沒解決的〉第 2 條）"),
    dict(loc="yard_j", cam="Medium shot, slow push in", chars=["aling"], night="dusk",
         comp=f"medium shot of {ALING}, {VEIL}, standing beside the round stone well, framed from the waist up, the round stone rim of the well along the bottom of the frame, {BUCKET} already held in her right hand just above the rim from the first frame, a little water slopping over its edge onto the stone, her face three-quarter to screen left toward the yard gate beyond the left edge of the frame, never the lens; that side of the frame is only {SIDE_WALL} all the way to the edge, and she is the only person in the frame; cold and closed, not smiling: eyes lowered, brows level; behind her the low mud-and-stone wall and a few planks leaning against it in the low evening sun; {HANDS}",
         lines=[("aling", "天下長得像的人多了。公子，請回。", "不回頭，隔著面紗")],
         motion="A-ling turns away from the yard gate toward the right edge of the frame, her eyes on the earth, as she speaks from under the veil",
         zh="中景（腰以上、井沿在畫面下緣，拍法 32）、慢推（送 `-dong-jing-l1`；阿令從本鏡起送 `aling-veil-portrait-l1`、不送角度圖）：第一格水桶已經提在右手、水晃出來濺在井沿；她從院門那邊轉開、朝畫右、眼睛看地，隔著面紗說（『不回頭』）。稿子『往左後的屋門走兩步才停』不拍（一鏡一個動作；剪在轉身的一半，照稿子〈剪接〉）"),
    dict(loc="yard", cam="Wide shot, slow push in", chars=["weishaoqing", "aling", "xuyan"], night="dusk",
         comp=f"wide shot at standing eye height, like the picture: far back in the yard gate in the middle of the back wall {WEI}, framed full figure, small, already standing just outside the threshold from the first frame, facing the yard, {FAN}, his jaw clenched, not smiling, never the lens; at the left before the farmhouse {XU_D}, standing, framed full figure, small, his back three-quarter to us, facing the yard gate, his lips pressed shut, never the lens; in the right foreground beside the round stone well {ALING}, {VEIL}, standing, framed full figure, {BUCKET} in her right hand, her back to the yard gate, her face turned down toward the bucket, never the lens; in the middle foreground {TBACK}, {BOX} held against her chest, {only_tang()}; {HANDS}; exactly four people",
         lines=[("weishaoqing", "好，就當我認錯了。這張臉，我記下了。", "咬牙")],
         motion=f"Wei Shaoqing turns away to the right and walks off behind the back wall, out of the frame, as he finishes speaking; {quiet('Xu Yan and A-ling', 'their', plural=True)}; {HEADSTILL}",
         zh="全景、慢推（人眼高、照圖；送 `set-xujia-yuan-dong-qing2-l1`）：照第 30 集 s41 實拍的站位（接點 30→31 更正）：後牆中間院門外小小的魏少卿（扇子合著、咬牙、不笑）說完往右轉、沿後牆外走出畫；畫左屋前許硯三分之二背面朝院門、嘴閉著；右前井邊阿令（面巾戴著，送面巾圖）背對院門、提著桶、低頭；前景正中唐小棠的背影抱著木盒、頭不動（不在 chars、不送圖）。稿子『一合扇子、解韁、翻身上馬、一勒韁繩』不拍：白馬不拍（聖經第 41 條、〈還沒解決的〉第 2 條），馬蹄遠去交給音效；跟拍改慢推。四個人有三張臉（拍法 1；唐小棠是背影）"),
    dict(loc="yard_m", cam="Medium shot from behind, slow push in", chars=["tangxiaotang", "xuyan"], nospeak=["tangxiaotang"], night="dusk",
         comp=alone(f"{BOX} held against her chest in her right arm from the first frame, her left hand already reaching out to the right sleeve of the young man before her; one step beyond her in the left third of the frame, his upper body clear of her head and shoulders, {XU_D}, standing, framed from the waist up, his back three-quarter to us, facing the yard gate, his lips pressed shut; beyond them, soft, the yard gate under its small tiled roof in the low evening sun; she stays in the middle of the frame the whole shot; {HANDS}; exactly two people, the young woman in the middle seen only from behind",
                    "standing on the packed earth of the yard,"),
         lines=[("tangxiaotang", "他認識阿令姊？還說在京裡見過她。", "小聲")],
         motion=f"her left hand tugs once at his right sleeve, only her arm moving; {quiet('Xu Yan')}; {HEADSTILL}",
         zh="中景（從背後）、慢推（送 `-dong-men2-l1`）：唐小棠背影在畫面正中、頭不動，右臂抱著木盒（接第 30 集 s41），左手拉一下前面許硯的右袖（只動手臂，拿東西的手不越過身體，拍法 32）；許硯在她前方一步、畫面左三分之一、三分之二背面朝院門、嘴閉著（nospeak，拍法 40）。稿子『下巴以上、高立領、踮腳看馬跑遠』改背影（拍法 4、40），踮腳不拍"),
    dict(loc="yard_w", cam="Medium shot from behind, slow push in", chars=["tangxiaotang", "xuyan"], nospeak=["tangxiaotang"], night="dusk",
         comp=alone(f"{BOX} held against her chest in both arms from the first frame; one step beyond her in the left third of the frame, his whole figure clear of her head and shoulders, {XU_D}, standing before the thatched farmhouse, framed from the waist up, his face three-quarter to screen right toward her, never the lens, his eyes on the house door beyond the left edge of the frame at first; calm and level, not smiling: steady eyes, brows level, lips moving evenly between words; beyond them, soft, the dark doorway and the split firewood against the farmhouse wall in the low evening sun; she stays in the middle of the frame the whole shot; {HANDS}; exactly two people, the young woman in the middle seen only from behind",
                    "standing on the packed earth of the yard,"),
         lines=[("xuyan", "不知道。她想說的時候，自然會說。", "平靜，不笑")],
         motion=f"Xu Yan's eyes come back from the house door beyond the left edge of the frame to the young woman as he speaks; {HEADSTILL}",
         zh="中景（從背後）、慢推（送 `-dong-wu2-l1`）：唐小棠背影在畫面正中抱著木盒、頭不動、不說話（拍法 40：背影過肩）；許硯在畫左三分之一、屋前，眼睛從畫左外的屋門（阿令進屋，不寫她）收回來看她、平靜地說，不笑。稿子『從肩上拈下乾柿葉、在指間轉一圈讓風帶走』不拍（一鏡一個動作；葉子交給音效）；『聽完點一下頭』不拍"),
    dict(loc="night", cam="Wide shot, slow push in", chars=["xuyan", "aling"], night="night", act=3,
         comp=f"wide shot at standing eye height, like the picture, the yard by night: at the left on the stone doorstep of the farmhouse {XU_COAT}, framed full figure, small, already stepping out of the dark doorway from the first frame, {LAMP} in his left hand, its small warm light on his robe, his face three-quarter to screen right toward the well, his lips pressed shut, never the lens; in the front right {ALING}, her face bare, sitting on the stone rim of the round well, framed full figure, small, {GAUZE_KNEE}, her face tipped up toward the night sky, her lips closed, never the lens; {HANDS}; exactly two people",
         motion=f"Xu Yan bends and sets the clay oil lamp down on the stone doorstep, its little flame steady; A-ling sits still; {quiet('Xu Yan and A-ling', 'their', plural=True)}",
         zh="全景、慢推（人眼高、照圖；送免費的 `set-xujia-yuan-ye-dong-l1`，柿子已塗掉；屋門右邊那塊深色空白木板這張還在，提示詞寫素的石牆，或開拍前照 `clean_yard.py` (a) 免費再塗一版）：天已經黑了（第一格），許硯（外披舊灰外衣）從屋門出來、左手一盞陶油燈，彎身把燈放在門前石階上；右前井沿上阿令一個人坐著、仰頭、膝上一方摺好的灰紗（聖經道具表）。無台詞。稿子『屋簷下的燈籠、唐家大車與車燈籠駛遠』不拍（拍法 33：不掛燈籠；不描述畫外的車與人，唐家回縣城交給遠處車輪與馬蹄的音效）；『錢箱、帳本』照稿子是畫外交代，不拍"),
    dict(loc="night", cam="Wide shot, slow push in", chars=["xuyan", "aling"], night="night",
         comp=f"wide shot at standing eye height, like the picture, the yard by night: in the middle of the yard {XU_COAT}, framed full figure, small, already halfway from the house toward the well from the first frame, {SOUP} carried carefully in both hands before his chest, his face three-quarter to screen right toward the young woman at the well, never the lens; gentle, not smiling: soft eyes, lips moving quietly between words; behind him on the stone doorstep of the farmhouse {LAMP} standing on the stone, nobody holding it; in the front right {ALING}, her face bare, sitting on the stone rim of the round well, framed full figure, {GAUZE_KNEE}, her face turned a little toward him, her lips closed, never the lens; {HANDS}; exactly two people",
         lines=[("xuyan", "還沒睡？夜裡風冷，喝口熱湯再進屋。", "輕聲")],
         motion=f"Xu Yan walks slowly on toward the well, careful of the steaming bowl, as he speaks; {quiet('A-ling', 'her')}",
         zh="全景、慢推（送 `-ye-dong-l1`）：許硯第一格已經走到院子中間，兩手端著冒熱氣的粗陶湯碗、小心地往右前的井走、輕聲說；陶油燈放在身後屋門石階上（沒人拿）；井沿上的阿令沒戴面巾（送 `aling-portrait-l1`），臉微微轉向他、嘴閉著。稿子『從屋門走出來』在第一格已經完成；跟拍改慢推；前景矮木桌一角不拍（圖上沒有）"),
    dict(loc="night_j", cam="Medium shot, slow push in", chars=["aling"], night="night",
         comp=f"medium shot of {ALING}, her face bare, sitting on the stone rim of the round well, framed from the waist up, {SOUP} already held in both her hands on her knees from the first frame, {GAUZE_KNEE} beside it, her face three-quarter to screen right {off('right', 'the dark wooden windlass and the low wall', he='she')}; quiet and guarded, not smiling: cool moonlight on her pale face, brows level, lips moving slowly between words; behind her, soft, the dark low mud-and-stone wall; {HANDS}",
         lines=[("aling", "你端湯過來，是想問傍晚那個人。", "不看他，慢")],
         motion="A-ling's eyes rise once to the moon above the right edge of the frame and slowly drop to the dark mouth of the well as she speaks",
         zh="中景（腰以上，碗在框裡）、慢推（送免費的 `set-xujia-yuan-ye-dong-jing-l1`）：阿令第一格已經兩手捧著湯碗放在膝上，眼睛先往上看月亮、再慢慢垂到井口，朝畫右外看不到的人說（不看他；不點名許硯）。稿子『畫面右下許硯的雙手與湯碗』不拍（不寫畫面邊緣別人的手，拍法 31）；『伸雙手接過』在第一格已經完成"),
    dict(loc="night_j", cam="Medium shot over the shoulder, slow push in", chars=["xuyan"], night="night",
         comp=f"medium shot over a shoulder: {BACK_ALING}; one step beyond it in the right half of the frame {XU_COAT}, already crouching beside the well from the first frame, framed from the waist up, his eyes level with hers, his face three-quarter to screen left toward the woman in the foreground, never the lens; frank and gentle, not smiling: moonlight on half his face, steady eyes, lips moving quietly between words; behind him, soft, the dark low mud-and-stone wall; {HANDS}; exactly two people, the one in the foreground seen only from behind",
         lines=[("xuyan", "想問。可我看得出來，妳不想說。", "坦白，不逼")],
         motion="Xu Yan rests his forearms on his knees as he speaks",
         zh="過肩中景、慢推（送 `-ye-dong-jing-l1`）：前景左是被畫框切掉、虛焦的灰白肩背與高髻木簪（不點名、不送圖，拍法 2；寫後腦朝我們，免得轉成側臉）；許硯第一格已經蹲在井邊、跟她平視，兩手肘擱到膝上、坦白地說，月光照半張臉，不笑"),
    dict(loc="night_j", cam="Close-up, slow push in", chars=["aling"], night="night",
         comp=f"close-up of {ALING}, her face bare, framed from the shoulders up, her eyes lowered from the first frame, her face three-quarter to screen right {off('right', SIDE_NWALL, he='she')}; still and grave, not smiling: cool moonlight on her face, brows level, lips moving slowly and softly between words, one word at a time; behind her, soft, only the dark night sky above the low wall",
         lines=[("aling", "他是在一道很高的牆裡，見過我的。", "很輕，一字一字")],
         motion="A-ling's eyes rise slowly to that spot beyond the right edge of the frame as she speaks",
         zh="近景、慢推（送 `-ye-dong-jing-l1`）：阿令眼睛慢慢抬起、朝畫右外看不到的人一字一字地說（伏筆：很高的牆）。稿子『手指在碗邊收緊、吸一口氣』不拍（近景看不到碗；一鏡一個動作）"),
    dict(loc="night_j", cam="Close-up, slow push in", chars=["aling"], night="night",
         comp=f"close-up of {ALING}, her face bare, framed from the shoulders up, the tips of her ears flushed pink, her face three-quarter to screen right toward someone out of sight beyond the right edge of the frame at first, never the lens; that side of the frame is only {SIDE_NWALL} all the way to the edge, and she is the only person in the frame; closed and a little shy, not smiling: brows level, lips moving softly between words; behind her, soft, only the dark night sky above the low wall",
         lines=[("aling", "就這一句。別再問了，好不好？", "很輕")],
         motion="A-ling turns her face away toward the left edge of the frame and tucks her chin down as she speaks",
         zh="近景、慢推（送 `-ye-dong-jing-l1`）：阿令耳尖微紅（拍法 12：不寫皮膚上的細點，寫整片泛紅），把臉別到畫左、下巴一收地說"),
    dict(loc="night_j", cam="Close-up, slow push in", chars=["xuyan"], night="night",
         comp=f"close-up of {XU_COAT}, crouching, framed from the chest up with space above his head, his face three-quarter to screen left {off('left', SIDE_NWALL)}; steady and calm, not smiling: moonlight on his face, steady eyes, brows level, lips moving evenly between words; behind him, soft, the dark low mud-and-stone wall",
         lines=[("xuyan", "好，不問。妳什麼時候想說，我都聽。", "很穩")],
         motion="Xu Yan gives one slow nod as he speaks",
         zh="近景、慢推（送 `-ye-dong-jing-l1`）：許硯蹲著，點一下頭，朝畫左外看不到的人很穩地說（本集好感的原因，好感帳：「好，不問」），不笑。稿子『雙手在膝上鬆開』不拍（一鏡一個動作）"),
    dict(loc="night_j", cam="Medium shot, slow push in", chars=["aling"], night="night",
         comp=f"medium shot of {ALING}, her face bare, sitting on the stone rim of the round well, framed from the waist up, {SOUP} held in both her hands on her knees, her face turned away toward screen left at first, never the lens; she is the only person in the frame; softened, not smiling: brows easing, eyes quiet; behind her, soft, the dark low mud-and-stone wall; {HANDS}",
         lines=[("xitong", "叮。阿令，好感加四。", "冷，宣布")],
         panel=[("阿令 好感 +4 → 32", "affection")],
         motion=f"A-ling turns her face back toward the right edge of the frame and her eyes rest there a moment; {quiet('A-ling', 'her')}",
         zh="中景（腰以上）、慢推（送 `-ye-dong-jing-l1`）：阿令把別開的臉轉回畫右（看畫外的許硯，不寫他），眼睛停一下；全程嘴閉著（系統畫外）。面板「阿令 好感 +4 → 32」由剪接疊上（好感帳第 31 集）。稿子『畫面右邊緣許硯的肩』不拍（拍法 31）；『低頭吹一口湯』不拍（一鏡一個動作；吹湯會動嘴）"),
    dict(loc="night_j", cam="Close-up, slow push in", chars=["xuyan"], night="night",
         comp=f"close-up of {XU_COAT}, crouching, framed from the chest up with space above his head, his face three-quarter to screen left, his eyes on a spot beyond the left edge of the frame, never the lens; he is the only person in the frame; amused with himself, not smiling: brows lifting a little, eyes bright, lips pressed shut; moonlight on his face; behind him, soft, the dark low mud-and-stone wall",
         lines=[("xuyan", "不問反而加分……那我是不是該少問一點？", "心裡話，錄得近、輕", "inner"),
                ("xitong", "宿主少說話，比少問有用。", "冷")],
         motion=f"one corner of Xu Yan's mouth starts to rise and is pressed flat again, his eyes flicking to the left edge of the frame and back; {SILENT_HE}; he is thinking, not speaking",
         zh="近景、慢推（送 `-ye-dong-jing-l1`；拍法 11 不寫藍光，稿子『臉被面前的淡藍光照亮』不照用）：許硯的心裡話與系統的吐槽（本集鬥嘴之一），嘴角想動又壓住、眼睛往畫左瞄一下又收回，全程嘴閉著。長鏡"),
    dict(loc="night_j", cam="Medium shot, slow push in", chars=["aling", "xuyan"], night="night",
         comp=f"medium shot of two people sitting side by side on the stone rim of the round well, both framed from the waist up: on the left {ALING}, her face bare, {SOUP} held in both her hands on her knees, her head bowed a little over it, her lips closed, never the lens; on the right, a little apart from her, {XU_COAT}, already sitting on the rim from the first frame, his hands on the stone behind him, his face tipped up three-quarter to screen right toward the moon, his lips pressed shut, never the lens; quiet and easy, neither smiling; moonlight on both; behind them, soft, the dark low mud-and-stone wall; {HANDS}; exactly two people",
         lines=[("xuyan", "好，閉嘴。今晚就陪她坐著。", "心裡話，錄得近、輕", "inner")],
         motion=f"Xu Yan leans back on his hands and breathes out slowly, looking up at the moon; {quiet('A-ling and Xu Yan', 'their', plural=True)}",
         zh="中景（雙人）、慢推（送 `-ye-dong-jing-l1`）：井沿上，阿令在左捧著湯碗低頭，許硯在右、第一格已經坐下，兩手撐在身後、吐一口氣看月亮；兩人嘴都閉著（心裡話）。稿子『挨著井沿坐下來』在第一格已經完成；前景木轆轤不寫；『阿令低頭喝湯』改捧碗低頭（喝湯會動嘴）"),
    dict(loc="night_j", cam="Medium close-up, slow push in", chars=["aling"], night="night",
         comp=f"medium close-up of {ALING}, her face bare, sitting on the stone rim of the well, framed from the chest up with space above her head, {EMPTY_BOWL} in both her hands before her chest from the first frame, her face three-quarter to screen right {off('right', SIDE_NWALL, he='she')}; softened: the corners of her mouth easing a little, not a smile, eyes warm and quiet, lips moving softly between words; cool moonlight on her face; behind her, soft, the dark low wall; {HANDS}",
         lines=[("aling", "湯還是熱的。許硯，謝謝你沒問。", "很輕")],
         motion="A-ling holds the empty bowl out toward the right edge of the frame in both hands as she speaks",
         zh="中近景、慢推（送 `-ye-dong-jing-l1`）：阿令兩手把空湯碗往畫右外遞出去、輕輕地說；嘴角可以鬆一點、不算笑（稿子）（第一場結尾）。稿子『許硯的手接過去』不拍（不寫畫面邊緣別人的手）"),
    # ---- scene 2: three months later, early spring in a drought, the same yard in the hot afternoon (set-xujia-yuan-han-l1).
    dict(chapter="三個月後，許家院子", loc="han_e", cam="Insert close-up, slow push in", chars=[], night="hot", act=3,
         comp=f"{SKY_LIGHT}: insert close-up seen from slightly below, the very first frame is already a close view of the tip of one bare grey twig with a few tiny pale green buds just breaking on it, one last curled dry brown leaf still holding on; beyond it, soft and out of focus, only the hazy bright sky and a few thin bare branches fill the background to every edge; only the twig, its buds, the dry leaf and the sky are in the frame",
         motion=NOBODY + "A gust of hot wind shakes the twig and the dry brown leaf breaks off and drops out of the bottom of the frame",
         zh="插鏡、慢推（第一格就是枝頭新芽，拍法 10、35；d1 不寫地點句，背景只有發亮的天與枯枝；送 `set-xujia-yuan-han-shu-l1`：**還沒做**，免費照 `-dong-shu-l1` 的 crop `480:270:560:0` 從 `-han-l1` 裁，禿枝映著發亮的天、左下一角瓦簷。Ref2VA 一張圖都不送不行（預檢 picture-list）；圖上的天是金黃的，聖經寫的藍天照圖改）：一陣熱風搖一下樹枝，最後一片乾枯的舊葉斷下、往下掉出畫面（無台詞）。稿子『往下搖到地面、跟著葉子落到裂開的地』改慢推（一鏡一個運鏡；乾裂的地交給下一鏡）。三個月的跳接就在這一刀"),
    dict(loc="han_j", cam="Medium shot from behind, slow push in", chars=["tangxiaotang"], nospeak=["tangxiaotang"], night="hot",
         comp=alone(f"both her hands already on the rope of the wooden windlass from the first frame; just beyond her on the round stone rim of the well {MUD_BUCKET}; beyond the well, soft, the low mud-and-stone wall and the cracked bare earth beyond it in the hazy afternoon sun; {HANDS}; she is the only person in the frame",
                    "standing at the round stone well,"),
         lines=[("tangxiaotang", "三個月了，一滴雨都沒下，井裡只剩半桶泥水。", "聲音悶，不笑")],
         motion=f"her shoulders rise and sink once in a long sigh, only her shoulders moving; {HEADSTILL}",
         zh="中景（從背後）、慢推（送 `set-xujia-yuan-han-jing-l1`）：唐小棠背影在畫面正中、頭不動，兩手第一格已經握著轆轤的井繩，井沿上半桶黃泥水已經提上來；肩膀一提一落嘆口氣（只動肩），說話放錄音（nospeak，拍法 40）。稿子『在井邊（畫面左）』照圖在前右（拍法 42）；『額上有汗』不寫（拍法 12）；『低頭看渾水』不拍（頭不動）"),
    dict(loc="han_w", cam="Medium shot from behind, slow push in", chars=["tangxiaotang", "xuyan"], nospeak=["tangxiaotang"], night="hot",
         comp=alone(f"both her hands empty at her sides; one step beyond her in the left third of the frame, his whole figure clear of her head and shoulders, {XU_UP}, standing before the thatched farmhouse, framed from the waist up, {REDBOWL} held in his left hand at his chest, his flat right hand already resting on the wet cloth from the first frame, his face three-quarter to screen right toward her, never the lens; quietly hopeful: a faint warm look in his eyes, lips moving evenly between words; beyond them, soft, the dark doorway and the split firewood against the farmhouse wall in the hazy afternoon sun; she stays in the middle of the frame the whole shot; {HANDS}; exactly two people, the young woman in the middle seen only from behind",
                    "standing on the cracked earth of the yard,"),
         lines=[("xuyan", "三天前我把稻種包進濕布，今天該醒了。", "平穩")],
         motion=f"Xu Yan holds the covered bowl out a little toward her as he speaks; {HEADSTILL}",
         zh="中景（從背後、過她的背）、慢推（送 `-han-wu-l1`）：唐小棠背影在畫面正中、頭不動、兩手空著（拍法 40：背影過肩）；許硯在畫左三分之一的屋前，左手拿著蓋濕白布的紅陶碗、右手平放在布上，把碗往她那邊遞一點、平穩地說。稿子『坐在矮木桌邊、把碗往桌子中間一挪』改站著拿在手上（圖上沒有矮木桌，同第 30 集）；『她提著桶走過來』在第一格已經完成"),
    dict(loc="han_e", cam="Insert close-up, slow push in", chars=[], night="hot",
         comp=f"{INSERT_LIGHT}: insert close-up seen from slightly above, looking down, the very first frame is already a close view of {REDBOWL}, held level in a man's left hand with a faded blue-grey sleeve rolled up to the elbow, the fingers of his right hand already pinching one corner of the wet cloth; far below, soft and out of focus, only cracked dry yellow earth fills the background to every edge; only the bowl, the cloth and the two hands and forearms are in the frame",
         lines=[("tangxiaotang", "發芽了！", "畫外，短喊")],
         motion=NOBODY + f"The right hand lifts the wet white cloth off the bowl: under it lies {SPROUTS}; a drop of water falls from a corner of the cloth",
         zh="插鏡、慢推（第一格就是從稍上方往下看的紅陶碗；d1 不寫院子地點句，背景只有乾裂黃土鋪到四邊，拍法 35；送 `set-xujia-yuan-han-di2-l1`：**還沒做**，`-han-di-l1` 左下有一片葉形石片，照 `e930-live/fix1/clean_di.py` 免費塗掉後再送）：許硯的手（藍灰袖子捲到手肘）把濕布掀起：碗裡一層稻種，每一粒冒出一點白芽，布角滴一滴水（拍法 36：寫 lifts，不寫 open）。唐小棠的『發芽了！』是畫外錄音"),
    dict(sid="s21b", loc="han_q", cam="Close-up, slow push in", chars=["tangxiaotang"], night="hot",
         comp=f"close-up of {TANG_FACE}, standing in the yard, framed from the shoulders up with space above her head, her face three-quarter to screen left, her eyes lowered to the bowl beyond the left edge of the frame, never the lens; she is the only person in the frame; delighted: her big round eyes shining wide, a small bright smile with her lips pressed together; behind her, soft, the low mud-and-stone wall and the cracked bare earth beyond it in the hazy afternoon sun",
         act=2,
         motion=f"Tang Xiaotang's eyes widen and brighten as she looks down at the bowl, her lips pressed together; {quiet('Tang Xiaotang', 'her')}",
         zh="近景、慢推（送 `-han-qiang-l1`；送 `tangxiaotang-portrait-l1` 與角度圖）：**本集唯一一鏡唐小棠的正臉**（拍法 40：不說話的正臉每集最多兩鏡，聖經建議用在「c21→c22 看到稻芽」）：她低頭看畫左外的碗、眼睛一亮，嘴閉著、小小地笑（稿子 c22『眼睛發亮、本鏡可以笑』）；無台詞。下一鏡 s22 是中景背影（不同景別，正臉一個髻、背影雙丸子的差別不相鄰同景別）"),
    dict(loc="han_w", cam="Medium shot from behind, slow push in", chars=["tangxiaotang", "xuyan"], nospeak=["tangxiaotang"], night="hot",
         comp=alone(f"both her hands clasped before her waist from the first frame; one step beyond her in the left third of the frame, his whole figure clear of her head and shoulders, {XU_UP}, standing before the thatched farmhouse, framed from the waist up, {REDBOWL_SPROUTS} held in both his hands at his chest, the wet cloth over his left wrist, his face three-quarter to screen right toward her, never the lens; warm: a faint pleased smile, his lips pressed together; beyond them, soft, the dark doorway and the split firewood against the farmhouse wall in the hazy afternoon sun; she stays in the middle of the frame the whole shot; {HANDS}; exactly two people, the young woman in the middle seen only from behind",
                    "standing on the cracked earth of the yard,"),
         lines=[("tangxiaotang", "真的出芽了！這袋種子，我在箱底收了三個月。", "眼睛發亮，本鏡可以笑")],
         motion=f"she leans in a little toward the bowl in his hands, only her shoulders moving; {quiet('Xu Yan')}; {HEADSTILL}",
         zh="中景（從背後）、慢推（送 `-han-wu-l1`）：唐小棠背影在畫面正中、頭不動，往他手上的碗湊近一點（只動肩），說話放錄音（拍法 40；台詞交代種子是她箱底那袋，接第 30 集）；許硯在畫左三分之一捧著出芽的紅陶碗、淡淡地笑、嘴閉著。稿子『近景下巴以上、彎腰兩手按在矮木桌邊、抬頭看許硯』改背影（正臉已在 s21b 用掉；圖上沒有桌子）"),
    dict(loc="han_w", cam="Medium close-up, slow push in", chars=["xuyan"], night="hot",
         comp=f"medium close-up of {XU_UP}, standing before the thatched farmhouse, framed from the chest up with space above his head, {REDBOWL_SPROUTS} held in his left hand at the bottom of the frame, his face three-quarter to screen right, his eyes on the bowl at first, never the lens; that side of the frame is only {SIDE_EARTH} all the way to the edge, and he is the only person in the frame; sobering, not smiling: the warmth leaving his eyes, brows drawing together, lips moving evenly between words; behind him, soft, the dark doorway and the farmhouse wall in the hazy afternoon sun; {HANDS}",
         lines=[("xuyan", "芽是醒了，可田裡沒水，插下去也活不了。", "不笑")],
         motion="Xu Yan's eyes lift from the bowl to the cracked earth beyond the right edge of the frame as he speaks, his brows drawing together",
         zh="中近景、慢推（送 `-han-wu-l1`）：許硯一個人入鏡，眼睛從碗抬到畫右外乾裂的地、眉頭收起來地說（嘴角的笑收掉，不笑）。稿子『拈起一粒、放回碗裡』不拍（一鏡一個動作，小東西在手指間會長錯）；『唐小棠的笑也收了』不拍：她的臉不入鏡（拍法 40）"),
    dict(loc="han", cam="Wide shot, slow push in", chars=["erniu"], night="hot",
         comp=f"wide shot at standing eye height, like the picture: in the yard gate in the middle of the back wall {ERNIU}, framed full figure, small, already through the swung-back plank gate from the first frame and running toward us, {HOE} on his right shoulder, his left fist clenched, not smiling: mouth wide and panting, brows knotted, never the lens; in the left foreground before the farmhouse, side by side, their backs three-quarter to us, facing the yard gate: on the left {XU_UP}, {REDBOWL} in his left hand, his lips pressed shut, and on his right {TBACK}, {only_tang()}; {HANDS}; exactly three people; the only hoe in the frame is his",
         lines=[("erniu", "許大哥！柳溪斷了，河床全裂開了！", "先在門外喊，喘，急，不笑")],
         motion=f"Wang Erniu runs across the cracked earth toward the two of them and stops, panting, as he shouts; {quiet('Xu Yan')}; {HEADSTILL}",
         zh="全景、慢推（人眼高、照圖；送 `set-xujia-yuan-han-l1`）：二牛第一格已經從後牆中間的院門衝進來，扛著鋤頭、左拳攥著一把乾泥，跑過乾裂的地停在兩人面前、喘著喊（不笑，原版必修）；左前景屋前許硯與他右邊的唐小棠背影（不在 chars、不送圖）朝院門、嘴閉著、頭不動。稿子『院門被撞開』在第一格已經完成，門外的喊聲交給錄音前半句；『前景籬笆、跟拍』照圖不拍；『許硯、唐小棠轉頭』不拍（她的頭不轉）"),
    dict(loc="han_m", cam="Close-up, slow push in", chars=["erniu"], night="hot",
         comp=f"close-up of {ERNIU}, standing, framed from the chest up with space above his head, {HOE} on his right shoulder, his left fist already raised before his chest from the first frame, clenched round a lump of dry earth, his face three-quarter to screen left {off('left', SIDE_EARTH)}; desperate, not smiling: brows knotted hard, eyes wide, chest heaving, lips moving fast between panting words; behind him, soft, the plank gate under its small tiled roof and the cracked bare earth beyond it in the hazy afternoon sun; {HANDS}",
         lines=[("erniu", "上游一滴水都不來，田全要乾死了！", "急，不笑")],
         motion="Wang Erniu's left fist uncurls and the dry earth crumbles to dust and sifts down between his fingers as he speaks",
         zh="近景、慢推（送 `-han-men-l1`）：二牛左拳第一格已經舉在胸前，拳頭鬆開、乾泥碎成粉從指縫漏下，朝畫左外看不到的人急著說（不點名許硯）；眉頭擠在一起、喘、不笑（原版必修）。拍法 36：寫 uncurls，不寫 open"),
    dict(loc="han_w", cam="Medium shot over the shoulder, slow push in", chars=["xuyan"], night="hot",
         comp=f"medium shot over a shoulder: {BACK_ERNIU}; one step beyond it in the left half of the frame {XU_UP}, standing before the thatched farmhouse, framed from the waist up, {REDBOWL} in his left hand at his side, his face three-quarter to screen right toward the man in the foreground, never the lens; cool and sharp, not smiling: brows drawn, eyes narrowing, lips moving evenly between words; behind him, soft, the farmhouse wall and the split firewood in the hazy afternoon sun; {HANDS}; exactly two people, the one in the foreground seen only from behind",
         lines=[("xuyan", "全村的田都乾了？上游錢家的田呢？", "冷靜")],
         motion="Xu Yan takes one step toward the man in the foreground as he speaks",
         zh="過肩中景、慢推（送 `-han-wu-l1`）：前景右是被畫框切掉、虛焦的褐色肩背與搭在肩上的鋤頭柄（不點名、不送圖，拍法 2；整個畫面只有這一把鋤頭）；許硯往他跨一步、冷靜地問，不笑。稿子『把稻種丟回碗裡、站起來』不拍（他一直站著；一鏡一個動作）"),
    dict(loc="han_q", cam="Medium shot over the shoulder, slow push in", chars=["erniu"], night="hot",
         comp=f"medium shot over a shoulder: {BACK_XU}; one step beyond it in the right half of the frame {ERNIU}, standing, framed from the waist up, {HOE} on his right shoulder, his face three-quarter to screen left toward the man in the foreground, never the lens; stunned turning furious, not smiling: eyes going wide and then hard, jaw clenching, lips moving fast between words; behind him, soft, the low mud-and-stone wall and the cracked bare earth beyond it in the hazy afternoon sun; {HANDS}; exactly two people, the one in the foreground seen only from behind",
         lines=[("erniu", "錢家的……我路過時，他們的田還是綠的！", "愣住，然後變臉，不笑")],
         motion="Wang Erniu's eyes go wide as it comes to him and his left hand closes into a hard fist as he speaks",
         zh="反打過肩中景、慢推（送 `-han-qiang-l1`）：前景左是虛焦的藍灰肩背與髮髻（不點名）；二牛眼睛一睜想起來、左手握成拳、變了臉地說（不笑，原版必修：只有一個二牛）。稿子『抓抓後腦』不拍（一鏡一個動作）"),
    dict(loc="han_w", cam="Close-up, slow push in", chars=["xuyan"], night="hot",
         comp=f"close-up of {XU_UP}, standing before the thatched farmhouse, framed from the chest up with space above his head, the rim of {REDBOWL} just showing at the bottom of the frame in his left hand, his face three-quarter to screen right, his eyes on a spot before him, never the lens; he is the only person in the frame; grim and tight, not smiling: brows pressed down, jaw set, lips pressed shut; behind him, soft, the dark doorway and the farmhouse wall in the hazy afternoon sun",
         lines=[("xitong", "叮。旱災任務：十日內讓柳溪的田見水。", "冷，宣布"),
                ("xitong", "失敗：稻種枯死。", "冷")],
         panel=[("旱災任務：十日內讓柳溪的田見水", "task"), ("失敗：稻種枯死", "penalty")],
         motion=f"Xu Yan's eyes drop to the bowl in his hand and rise again, his jaw tightening; {SILENT_HE}; he is listening, not speaking",
         zh="近景、慢推（送 `-han-wu-l1`；拍法 11 不寫藍光）：許硯聽系統兩句，眼睛往下看一眼手上的碗、再抬起、下巴繃緊，全程嘴閉著、不笑（原版建議）。面板「旱災任務：十日內讓柳溪的田見水」「失敗：稻種枯死」由剪接疊上（任務的面板紅框照剪接表 `panel_color`）。長鏡"),
    dict(loc="han_w", cam="Close-up, slow push in", chars=["xuyan"], night="hot",
         comp=f"close-up of {XU_UP}, standing before the thatched farmhouse, framed from the chest up with space above his head, his face three-quarter to screen right, his eyes on a spot before him, never the lens; he is the only person in the frame; weary and stubborn, not smiling: brows drawn, eyes hard, lips pressed shut; behind him, soft, the dark doorway and the farmhouse wall in the hazy afternoon sun",
         lines=[("xuyan", "十天？連雨都求不來，我上哪變出水來？", "心裡話，錄得近、輕", "inner"),
                ("xitong", "變水是神仙的事。宿主的事，是去找。", "冷")],
         motion=f"Xu Yan shuts his eyes for a moment, breathes out, and his eyes come up again; {SILENT_HE}; he is thinking, not speaking",
         zh="近景、慢推（送 `-han-wu-l1`）：許硯閉一下眼、吐一口氣、再睜開，全程嘴閉著（心裡話與系統的吐槽，本集鬥嘴之二）。稿子 c29 三句估約 11 秒（超過約 10 秒），拆成 s29（心裡話＋系統）與 s29b（心裡話），同第 28 集 c15、第 30 集 c21"),
    dict(sid="s29b", loc="han_w", cam="Close-up, slow push in", chars=["xuyan"], night="hot",
         comp=f"close-up of {XU_UP}, standing before the thatched farmhouse, framed from the chest up with space above his head, his face three-quarter to screen right, never the lens; he is the only person in the frame; set and resolved, not smiling: brows level, eyes narrowing, lips pressed shut; behind him, soft, the dark doorway and the farmhouse wall in the hazy afternoon sun",
         lines=[("xuyan", "找就找。水不會憑空不見，總有個去處。", "心裡話，錄得近、輕", "inner")],
         motion=f"Xu Yan's eyes turn toward the right edge of the frame, upstream, and narrow; {SILENT_HE}; he is thinking, not speaking",
         zh="近景、慢推（送 `-han-wu-l1`）：許硯的心裡話（錄音，嘴閉著），眼睛往畫右（上游的方向）一轉、瞇起來（稿子）。從 c29 拆出（見 s29）"),
    dict(loc="han_w", cam="Medium shot from behind, slow push in", chars=["tangxiaotang", "xuyan", "erniu"], nospeak=["tangxiaotang"], night="hot",
         comp=alone(f"both her hands empty at her sides; one step beyond her, both clear of her head and shoulders: in the left third of the frame {XU_UP}, standing before the thatched farmhouse, framed from the waist up, {REDBOWL} in his left hand, the wet cloth already laid back over it, his face three-quarter to screen right toward her, never the lens; set and urgent, not smiling: jaw set, brows pressed down, lips moving hard between words; in the right third of the frame {ERNIU}, standing, framed from the waist up, {HOE} on his right shoulder, his face three-quarter to screen left toward Xu Yan, his lips pressed shut, not smiling, never the lens; beyond them, soft, the farmhouse wall and the split firewood in the hazy afternoon sun; she stays in the middle of the frame the whole shot; {HANDS}; exactly three people, the young woman in the middle seen only from behind",
                    "standing on the cracked earth of the yard,"),
         lines=[("xuyan", "二牛叫人去上游。小棠，去田裡叫秦霜到上游找我們。", "咬牙，下令")],
         motion=f"Xu Yan sweeps his flat right hand once toward the yard gate beyond the right edge of the frame as he speaks; {quiet('Wang Erniu')}; {HEADSTILL}",
         zh="中景（從背後）、慢推（送 `-han-wu-l1`）：唐小棠背影在畫面正中、頭不動；畫左三分之一許硯（濕布已蓋回碗上，第一格完成）咬牙下令，右手平掌往畫右外的院門一揮；畫右三分之一二牛扛鋤頭、嘴閉著、不笑（三個人兩張臉）。稿子『二牛點頭轉身、唐小棠提裙跑出院門』不拍（一鏡一個動作；剪接交代；第三場她不在）；前景紅陶碗在矮木桌上不拍（圖上沒有桌子）（第二場結尾）"),
    # ---- scene 3: the same afternoon, the dry stream bed (set-ganxi-l1), then the Qian dam upstream (set-shangyou-ba-l1, NOT FILED).
    dict(chapter="乾溪床，上游的壩", loc="ganxi", cam="Wide shot, slow push in", chars=["erniu", "xuyan"], night="hot",
         comp=f"wide shot at standing eye height, like the picture, on the dry cracked bed of the stream: walking from the left toward the right in a loose line, all framed full figure, small: in front {ERNIU}, {HOE} on his right shoulder, his head turned back over his shoulder toward the others, not smiling: panting, brows knotted, lips moving between words, never the lens; just behind him {XU_UP}, his face toward Wang Erniu, his lips pressed shut, never the lens; behind them {VILLAGERS}, their lips closed, never the lens; {HANDS}; exactly seven people; the only hoe in the frame is Wang Erniu's",
         lines=[("erniu", "再往上走一里，就是錢家的地界了。", "喘，不笑")],
         motion=f"the seven of them walk steadily from the left toward the right across the cracked mud of the stream bed; {quiet('Xu Yan and the five others', 'their', plural=True)}",
         zh="全景、慢推（人眼高、照圖；送 `set-ganxi-l1`，試鏡一 37038 已歸檔：乾裂泥板的溪床、木板橋、柳樹）：一行七人由左往右走在乾裂的溪床上（往上游）：最前面二牛扛鋤頭、回頭說話（不笑）；許硯在他後面；五個村民灰藍短打、各自年紀與擔子不同（白髮老漢與瘦中年各挑扁擔兩頭空桶、十五歲少年、壯中年與包靛藍頭巾的中年婦人各背竹筐拿木鍬；拍法 34），只有二牛一把鋤頭（原版必修）。稿子『低角度跟拍、前景一個滾動的空木桶』改人眼高慢推（一鏡一個運鏡、一個動作；木桶交給音效）；溪床跟岸幾乎齊平、右岸稻田仍金黃（歸檔時記的毛病），提示詞照圖寫、不寫『只剩石頭』"),
    dict(loc="ba", cam="Point-of-view wide shot, slow push in", chars=[], night="hot",
         comp=f"point-of-view wide shot at standing eye height toward the dam, like the picture: the long dam of stacked brown hemp sacks with the muddy pond behind it; along its top, small and far, two men in identical Song-dynasty black cross-collared short jackets and black cloth head wraps stacking brown hemp sacks with iron spades, and ten more men dressed the same, each holding one plain wooden staff, standing in a loose row; at the right end of the dam top five brown hemp grain sacks stacked on a plain wooden cart bed, and beside them one stout man in a dark gold brocade robe; exactly thirteen people, all small and far; the dam and the pond as in the picture",
         lines=[("xuyan", "水沒斷，是被人用土袋截在這裡了。", "畫外，低")],
         motion=f"the men on the dam lift their heads and turn toward us, all at once; {quiet('the men on the dam', 'their', plural=True)}",
         zh="主觀全景、慢推（許硯看上游；送 `set-shangyou-ba-l1`：**試鏡第三輪，還沒歸檔**；第三輪的圖是站在溝底往上游看、壩在約三十步外橫過溝、壩後一窪泥水、右岸新溝引水到一小塊青田）：壩頂兩個家丁拿鐵鍬堆土袋、十個拿木棍站著（同一身黑短打，遠景，拍法 34），右端一輛騾車的車板上五袋糧、旁邊一個穿深金錦袍的胖子（遠、小，不送錢員外的圖）；家丁一起抬頭看過來（一個動作）。許硯的台詞是畫外（主觀，嘴不入鏡）。稿子『前景岸邊垂下的柳枝』不拍（圖上不一定有，柳枝也會被讀成掛著的東西）。**沒有水車**（原版必修）"),
    dict(loc="ba_c", cam="Medium shot, slow push in", chars=["erniu"], night="hot",
         comp=f"medium shot of {ERNIU}, standing on the cracked earth of the gully floor, framed from the waist up, {HOE} on his right shoulder from the first frame, his face three-quarter to screen right toward the dam beyond the right edge of the frame, his eyes on it, never the lens; furious, not smiling: a vein standing on his forehead, jaw clenched, teeth set, lips moving hard between shouted words; behind him, soft and out of focus, two more people in grey-blue homespun jackets, a white-haired old man with an empty bucket on a carrying pole and a thin boy of fifteen with a bamboo basket on his back and a wooden spade, their lips closed, never the lens; {HANDS}; exactly three people; the only hoe in the frame is Wang Erniu's",
         lines=[("erniu", "是錢員外！他把最後的水，全引進自家田了！", "吼，不笑")],
         motion=f"Wang Erniu swings the hoe down off his shoulder into both hands as he shouts; {quiet('the old man and the boy', 'their', plural=True)}",
         zh="中景、慢推（送 `set-shangyou-ba-l1` 挑定後的近景裁切，免費；**圖還沒歸檔**）：二牛把鋤頭從肩上甩到兩手握著、朝畫右外的壩吼（不笑，原版必修）；身後虛焦兩個村民（白髮老漢挑空桶、十五歲少年背竹筐拿木鍬），嘴閉著、沒有鋤頭（原版必修：背景兩個二牛）。稿子『一手指著壩頂的胖子』不拍（單指會讀錯，拍法 32；一鏡一個動作）"),
    dict(loc="ba", cam="Low-angle medium shot, slow push in", chars=["qianyuanwai"], night="hot",
         comp=f"low-angle medium shot of {QIAN}, standing on the beaten earth path along the top of the dam, framed from the waist up, his right hand already resting on {SACKS} beside him from the first frame, his face three-quarter to screen left, looking down toward someone out of sight beyond the lower left edge of the frame, never the lens; that side of the frame is only the hazy white sky and the edge of the dam all the way to the edge, and he is the only person in the frame; oily and smug: a sly fake smile, small eyes narrowed, lips moving slowly between drawled words; behind him, soft, the still muddy pond and the bright green field beyond it; {HANDS}",
         lines=[("qianyuanwai", "許秀才，來得正好。今年的糧價，再漲三成。", "油滑，拖長音，本鏡可以假笑")],
         motion="Qian Yuanwai pats the top grain sack twice with his right hand, a little puff of dust rising, as he speaks",
         zh="低角度中景、慢推（送 `set-shangyou-ba-l1` 的壩頂裁切，**圖還沒歸檔**）：錢員外（胸前素的錦袍、三個金戒指，原版第 35 集的吊牌不寫）站在壩頂，右手拍兩下車板上的糧袋、揚起一點灰，往畫左下外看不到的人（許硯，不點名）拖長音地說（稿子『本鏡可以假笑』）。稿子『身後兩個家丁』不拍（拍法 34：家丁不進近鏡；畫面裡只有他）；騾子在這鏡不寫"),
    dict(loc="ba_c", cam="High-angle medium shot over the shoulder, slow push in", chars=["xuyan"], night="hot",
         comp=f"high-angle medium shot over a shoulder: {BACK_QIAN}; below and beyond it in the left half of the frame {XU_UP}, already standing on a big rough rock before the dam from the first frame, framed from the waist up, his face tipped up three-quarter to screen right toward the man in the foreground, never the lens; holding his anger down, not smiling: jaw set, eyes hard, brows low, lips moving evenly between words; behind him, soft, the cracked earth of the gully floor in the hazy white sun; {HANDS}; exactly two people, the one in the foreground seen only from behind",
         lines=[("xuyan", "上游截水，下游一村人喝什麼？", "壓著火")],
         motion="Xu Yan's hands close slowly into fists at his sides as he speaks",
         zh="俯角過肩中景、慢推（送壩的近景裁切，**圖還沒歸檔**）：前景右是虛焦的深金錦袍肩背與圓圓的後腦（不點名、不送圖，拍法 2）；許硯第一格已經站上壩前的大石，仰頭、兩手慢慢握成拳、壓著火問，不笑"),
    dict(loc="ba", cam="Low-angle medium shot over the shoulder, slow push in", chars=["qianyuanwai"], night="hot",
         comp=f"low-angle medium shot over a shoulder: {BACK_XU}; above and beyond it in the right half of the frame {QIAN}, already sitting on the front of a plain wooden cart bed among brown hemp grain sacks on top of the dam from the first frame, framed from the waist up, his face turned back three-quarter to screen left down toward the man in the foreground, never the lens; {MULE}; cold and pleased with himself: a cold thin sneer, small eyes narrowed, lips moving lazily between words; behind him the hazy white sky; {HANDS}; exactly two people, the one in the foreground seen only from behind",
         lines=[("qianyuanwai", "天不下雨，老天幫我數錢。你們喝什麼，是你們的事。", "冷笑，本鏡可以冷笑")],
         motion="Qian Yuanwai leans back against the grain sacks, at his ease, as he speaks",
         zh="仰角反打過肩中景、慢推（送壩的近景裁切，**圖還沒歸檔**）：前景左是虛焦的藍灰肩背與髮髻（不點名）；錢員外第一格已經坐上騾車（灰騾只見頭頸、在畫右緣，聖經第 41 條），往糧袋上一靠、回頭冷笑地說（稿子『本鏡可以冷笑』）。稿子『扶著車轅爬上騾車』在第一格已經完成"),
    dict(loc="ba", cam="Medium shot, slow push in", chars=["qianyuanwai"], night="hot",
         comp=f"medium shot along the top of the dam: {QIAN}, sitting on the front of a plain wooden cart bed among brown hemp grain sacks, framed from the waist up, his body facing screen right, his face turned back over his left shoulder toward someone out of sight beyond the left edge of the frame, never the lens; that side of the frame is only the beaten earth path along the dam top and the hazy sky all the way to the edge; beside him at the front of the cart one carter seen only from behind, in a plain grey-brown short jacket and a grey cloth head wrap, the reins in his hands, his face never in the frame; {MULE}; smug and lazy: a thin satisfied smile, eyes half lidded, lips moving slowly between drawled words; {HANDS}; exactly two people, the carter seen only from behind",
         lines=[("qianyuanwai", "看好壩。誰敢動一袋土，就給我打回去。", "拖長音")],
         motion="Qian Yuanwai sweeps his flat right hand once back toward the left edge of the frame as he speaks; the carter's back stays to us",
         zh="中景、慢推（送壩的近景裁切，**圖還沒歸檔**）：錢員外坐在車板前、身體朝畫右，回頭朝畫左外看不到的人（家丁，不寫）平掌一揮、拖長音地吩咐；車夫只見背影（灰褐短打、灰布包頭：**不寫草帽**，紅繩草帽是落水真相的線索）；灰騾只見頭頸。稿子『車夫一甩鞭、騾車往右走、家丁一起點頭握緊棍子、兩人丟下鐵鍬拔起木棍』不拍（一鏡一個動作；家丁不進近鏡；車走交給鞭響、蹄聲與車輪的音效，家丁拿棍子在 s41 第一格已經完成）"),
    dict(loc="ba_c", cam="Medium shot, slow push in", chars=["xuyan", "erniu"], night="hot",
         comp=f"medium shot on the cracked earth of the gully floor, both men framed from the waist up, side-on to us: on the left {XU_UP}, his left hand already gripping the other man's right forearm from the first frame, facing screen right, never the lens; urgent and low, not smiling: brows drawn, eyes steady, lips moving low between words; on the right {ERNIU}, {HOE} gripped in both his hands, facing screen left, never the lens, his chest heaving, his jaw clenched, his lips pressed shut, not smiling; behind them, soft, the dry gully and its low banks in the hazy white sun; {HANDS}; exactly two people",
         lines=[("xuyan", "二牛，別衝動。秦霜還沒到，先數清他們有幾個人。", "壓低聲音")],
         motion=f"Xu Yan leans in close to Wang Erniu as he speaks low; {quiet('Wang Erniu')}",
         zh="中景（雙人、側面）、慢推（送壩的近景裁切，**圖還沒歸檔**）：許硯在畫左、第一格已經抓住二牛的右前臂，壓低身子湊近他說；二牛在畫右兩手握鋤頭、胸口起伏、咬牙、嘴閉著（不笑）"),
    dict(loc="ba_c", cam="Close-up, slow push in", chars=["erniu"], night="hot",
         comp=f"close-up of {ERNIU}, framed from the chest up with space above his head, {HOE} already gripped in both hands before his chest from the first frame, his face three-quarter to screen left {off('left', SIDE_GULLY)}; past caring, not smiling: red-rimmed eyes, jaw clenched, teeth set, lips moving hard between words; behind him, soft, only the dry cracked bank of the gully in the hazy white sun; {HANDS}",
         lines=[("erniu", "等不了！我娘的菜地，昨天就乾死了！", "豁出去，不笑")],
         motion="Wang Erniu heaves the hoe up onto his right shoulder as he speaks",
         zh="近景、慢推（送壩的近景裁切，**圖還沒歸檔**）：二牛眼睛發紅、咬牙，把鋤頭一把扛上右肩、朝畫左外看不到的人（許硯，不點名）說（不笑）。稿子『甩開許硯的手』在剪接裡交代（第一格手已經甩開；不寫畫面邊緣別人的手）"),
    dict(loc="ba_c", cam="Low-angle wide shot, slow push in", chars=["erniu", "xuyan"], night="hot",
         comp=f"low-angle wide shot from the side, close to the cracked earth of the gully floor: {ERNIU}, framed full figure, already running hard toward the right from the first frame, {HOE} raised above his head in both hands, not smiling: mouth wide in a roar, brows knotted, never the lens; a few steps behind him at the left {XU_UP}, framed full figure, his right arm already stretched out after him, his mouth wide in a shout, not smiling, never the lens; ahead at the right a low heap of rough rocks before the dam, the dam beyond them, soft, its top out of the frame; {HANDS}; exactly two people",
         lines=[("erniu", "還我們水！", "短喊，不笑"), ("xuyan", "二牛！", "短喊")],
         motion="Wang Erniu charges on toward the rocks at the right, the hoe held high, as he shouts; Xu Yan stays where he is, his arm still reaching",
         zh="低角度全景（側面）、慢推（送壩的近景裁切，**圖還沒歸檔**）：二牛第一格已經舉著鋤頭往右衝，衝向壩前的石堆、吼；許硯在左後幾步、手臂伸著沒抓到、喊（兩人都在喊，不笑）。整個衝的動作留在畫面裡（稿子）；村民不入鏡（全景只拍兩人，壩頂出畫，家丁不在這一格）；跟拍改慢推。剪在衝上石堆的一半（稿子〈剪接〉）"),
    dict(loc="ba", cam="Wide shot, slow push in", chars=[], night="hot",
         comp=f"wide shot at standing eye height toward the dam, like the picture: in the left foreground, cut at the waist by the bottom of the frame, one big young man seen only from behind, in a coarse brown cross-collared short jacket with the sleeves rolled up, {HOE} raised above his head in both hands from the first frame, the back of his head toward us the whole shot; ahead, standing in one row along the top of the dam of brown hemp sacks, {RETAINERS}, facing us, their staffs held low; {HANDS}; exactly thirteen people; the only hoe in the frame is the young man's",
         lines=[("xuyan", "二牛，回來！對面是十二根棍子！", "畫外，大喊")],
         motion=f"the twelve men on the dam raise their twelve wooden staffs at the same moment and take one step forward; the young man's hoe stays raised; {quiet('the twelve men', 'their', plural=True)}",
         zh="全景、慢推（人眼高、照圖；送整張 `set-shangyou-ba-l1`，**圖還沒歸檔**）：左前景被畫框切到腰的二牛背影（不點名、不送圖，鋤頭還舉在半空、沒落下）；壩頂一排十二個家丁（同一身黑短打、每人一根木棍，遠景正面，拍法 34）同時舉起棍子、往前壓一步；許硯的喊聲是畫外錄音，畫面上的人嘴都閉著。本集最後一鏡、懸念交給第 32 集（接點 31→32：同一刻，秦霜從二牛身後一扁擔挑飛鋤頭）"),
]

HEAD = [
    "- 重製版 r2、真人版（站主 2026-11-11「之後都用真人版」）：照 `docs/videos/zhong-tian-qu-qi-e031-r2/script.md`（c01–c41 對應 s01–s41；含「這版改了什麼」「2026-11-06 審稿後的修改」）；台詞一字不改，只改拍法；每鏡一個看得見的動作、一句一筆不拆半句、預設不笑。篇章設定 `production/r2-bible-e031-e040.md`（拍法 1–43 條、〈場景〉〈接點〉），帳照 `r2-bible-e011-e060.md`。**第 4 篇章〈旱年〉第一集**。",
    "- 內部工作編號 931（`hailuo/{ff,clips}-dh-e931.json`；之後的 `colab/runs/e931/extras.json`、`colab/runs/e931-live/spec.json`、工作資料夾 `~/mokaair-work/videos/zhong-tian-qu-qi-e931-dh/` 還沒做）；發布 slug `zhong-tian-qu-qi-e031-r2`。不放集數、不放片名卡；s01 接第 30 集 s41（接點 30→31，2026-11-17 照實拍更正：唐小棠在前景正中背對鏡頭抱木盒、阿令在前右井邊手扶轆轤、灰紗掛在左耳、許硯在畫左屋前朝院門、魏少卿在後牆中間的院門口）；s41 交給第 32 集（接點 31→32：同一刻，十二根棍子舉起）。",
    "- 照第 30 集審稿後的寫法一開始就照做（聖經拍法 31–39 條）：`OFFSCREEN_SPEECH = False`；背影、系統與心裡話的鏡，每張朝鏡頭的臉都寫不說話、嘴閉著；**對畫外的人說話寫「朝畫左／右外看不到的人」，那一側到邊緣只有景、畫面裡只有他一個人，不點名、不描述不在畫裡的人**（唐家大車、唐萬金、鄭伯、秦霜、小禾、魏少卿的白馬、畫外的家丁都不寫）；不掛東西（沒有燈籠：s07 許硯提一盞陶油燈出屋門）；不寫 open；道具與接觸寫在第一格；寫人數。",
    "- **唐小棠**（拍法 40）：說話的三鏡（s05、s19、s22）與聽的兩鏡（s20、s30）從背後拍、畫面正中、正背對、頭不動、剛好兩顆丸子；全景 s04、s24 小小的背影（不送圖）。**本集唯一一鏡正臉是 s21b**（看到稻芽、不說話、嘴閉著小小地笑；送 `tangxiaotang-portrait-l1` 與角度圖），跟背影 s22 不同景別。稿子的 t2 高立領、「下巴以上」、「袖子用粉帶束起」、腰間金算盤不寫（拍法 4、20）。",
    "- **阿令**（拍法 21）：s01 送沒面巾的定妝照＋angle-a，灰紗寫成實物、第一格掛在左耳，她左手拉回遮住口鼻；s03、s04 送 `aling-veil-portrait-l1`；夜裡（s07–s17）摘下、摺好放在膝上（送沒面巾的定妝照）。**魏少卿**（拍法 30）只在 s02–s04，扇子合著、三鏡都不笑；**白馬不拍**（聖經〈還沒解決的〉第 2 條），s04 他沿後牆外往右走出畫、馬蹄交給音效。**王二牛**每鏡不笑（原版必修），全集只有他一把鋤頭；村民灰藍、五人各自年紀與擔子不同（拍法 34）。**錢員外**錦袍胸前素的；s34 可以假笑、s36 可以冷笑（稿子）。家丁只在遠景（s32、s41）。",
    "- **場景圖說了算**（拍法 29、42）：第一場同第 30 集那組（`-dong-qing2-l1`、`-dong-jing-l1`、`-dong-men2-l1`、`-dong-wu2-l1`），夜裡送免費的 `set-xujia-yuan-ye-dong-l1` 與 `-ye-dong-jing-l1`；第二場送試鏡一挑定的 `set-xujia-yuan-han-l1` 與它的免費裁切 `-han-jing`／`-han-wu`／`-han-qiang`／`-han-men`（圖是低斜陽，稿子的「正午」照聖經改「午後斜陽、熱風捲塵」；圖上沒有矮木桌，碗拿在許硯手上）；第三場乾溪床送 `set-ganxi-l1`（已歸檔），**壩 `set-shangyou-ba-l1` 還在試鏡第三輪，s32–s41 共 10 鏡要等它（近鏡再等它的免費裁切）**；s21 插鏡要的乾淨地面 `set-xujia-yuan-han-di2-l1` 與 s18 插鏡的禿枝 `set-xujia-yuan-han-shu-l1` 還沒做（免費）。本集畫面上沒有水車（原版必修）。",
    "- 長鏡要買的秒數（BUY，錄音還沒錄，照字數估；錄好後照第 30 集量人聲長度重核）：s04、s15、s22、s28、s29、s30、s34、s36、s37、s38 與最後一鏡 s41 買 8 秒；s07、s16、s18、s21、s21b、s29b 買 5 秒；其餘照 `gen-dh.mjs` 的預設（說話 6 秒）。稿子 c29 三句估約 11 秒，拆成 s29／s29b。",
    "- **表上的「秒」欄是 lint 估法**，比錄音短；剪接以錄音的人聲長度為準。",
]
FOOT = [
    "- **參考圖**（`assets/refs-live/`）：許硯 l1、angle-a（帶笑的 angle-b 整集不送；全景只送 l1）；阿令（s01 `aling-portrait-l1`＋`aling-angle-a-l1`；s03、s04 `aling-veil-portrait-l1`、不送角度圖；s07–s17 `aling-portrait-l1`＋angle-a）；魏少卿 l1；王二牛 l1、angle-a；錢員外 l1、angle-a；唐小棠只在 s21b 送 l1 與角度圖，其餘整集不送。過肩前景的背影（s10、s26、s27、s35、s36）、s41 二牛的背影、s32 壩上的胖子、車夫、村民、家丁都不送圖。場景見上面。",
    "- **還沒有的圖**（寫的時候照名字寫，挑定、歸檔後才能開拍那幾鏡）：`set-shangyou-ba-l1`（試鏡第三輪，s32、s34、s36、s37、s41 送整張或壩頂；s33、s35、s38、s39、s40 送挑定後的免費近景裁切）；`set-xujia-yuan-han-di2-l1`（免費，`-han-di-l1` 塗掉葉形石片，s21）；`set-xujia-yuan-han-shu-l1`（免費，`-han-l1` 照 `-dong-shu-l1` 的 crop 裁，s18）。可選：`set-xujia-yuan-ye-dong2-l1`（免費，塗掉夜圖屋門右邊的空白木板，s07、s08）。其他第三輪重畫的圖（`set-shentan-l1`、`set-shanjiao-qu-l1`、`diaoqi-portrait-l1`、`prop-zaohongma-l1`、`set-gucang-wai-l1`）本集不用。",
    "- 共用檔：沒有改（`build-r2.py` 的 `EN` 已有每個名字）；`gen-dh.mjs`、`pilot.py`、`cast.json` 不動。精修文字的 CG 立領句與背影鏡唐小棠的名字由本檔結尾的 `live_clips()` 在 build 後從 `clips-dh-e931.json` 換掉（s21b 是正臉，留名字、只拿掉立領句）；對畫外說話的鏡把通用的說話視線換成 d1 的方向句（`GAZE_REFINE`）。",
    "- 之後的免費準備（照 `prep930.sh`）：`extras.json`、`mkspec.py`／`spec.json`（swap_pictures 絕對路徑、drop_pictures、d1 的方向句、s21 拿掉地點句）、`DRY=1 … st1-ep.sh 931` → `pilot.py` → `retake.py`、`preflight-prompts.py` 與否定名詞、open、燈籠、掛著的東西、『畫外的人』、精修句外漏的掃描；錄音 39 句（`lines.mjs`，聽寫帶上下文、YIN 量音高，聖經第 43 條）。",
    "- 配樂：第一場傍晚低沉的 suspense（接第 30 集），s04 馬蹄遠去時收；夜裡溫柔的夜曲，s14「叮」一個輕重音；第二場乾、熱的 drone，s21 出芽一個亮的輕音，s24 喊斷流時切掉，s28「叮」一個重音；第三場低鼓，s32 看到壩一個重音，s40 起鼓點、s41 停在最高點。音效見 script.md〈音樂與音效〉（另外：馬蹄遠去、遠處車輪與馬蹄、滾過裂泥的空木桶、騾車鞭響與車輪、丟下鐵鍬，都交給音效）。",
]

# Seconds to buy. No recordings yet (e931 has none): estimated from the characters (a 6 s shot holds about 5.9 s of speech;
# e930's recordings ran about 3.1-3.7 characters a second for 15-19 characters, so 19 or more characters, two-line shots and
# the drawled lines buy 8). Re-check against the recordings' speech spans as e930 did (span930.sh) before d1.
# 8 s: s04 (script 長鏡, 15 characters and a walk out), s15 (thought + system, script 長鏡), s22 (19), s28 (two system lines,
#      script 長鏡), s29 (thought + system, 31), s30 (21), s34 (17, drawled), s36 (21), s37 (15, drawled), s38 (20), s41 (the
#      episode's last shot: the hook needs a held tail, as e923-e930).
# 5 s: s07 and s18 (no line), s16 and s29b (short thoughts), s21 (the insert, a three-character shout), s21b (the silent face).
# 6 s (gen-dh's default for a spoken line): every other shot.
BUY = {"s04": 8, "s15": 8, "s22": 8, "s28": 8, "s29": 8, "s30": 8, "s34": 8, "s36": 8, "s37": 8, "s38": 8, "s41": 8,
       "s07": 5, "s18": 5, "s16": 5, "s29b": 5, "s21": 5, "s21b": 5}


# ---- the refine text (as e023-e030): hailuo/clips-dh-e931.json column 0 is the motion text refine-prep.py sends with a picked
# d1 draft. gen-dh.mjs opens every clip that lists tangxiaotang with the CG-era "Tang Xiaotang's high stand-up collar stays
# closed at her throat." and names her in "<names> shown in <Picture 1>"; in a back shot that draws the collar back and turns
# her face to the lens. Her back shots: the sentence goes and her name becomes "the young woman seen only from behind", and
# "keeps the same face, hair, costume and props" of a back shot alone becomes "keeps the same hair, costume and props as the
# first frame, her back to us" (with someone else: "..., the young woman's back to us"). FRONT_TANG (s21b, her one front face)
# keeps her name and only loses the collar sentence. Column 1 is recomputed. prep931.sh hands stage 1 the anchor form
# (anchor_form(), e028 review 必改 1; rule 39).
COLLAR = "Tang Xiaotang's high stand-up collar stays closed at her throat. "
FRONT_TANG = {"s21b"}
# rule 31 (e030 review 建議 10): gen-dh's speaking gaze names "the person he/she is speaking to", who is not in the frame of these
# shots; the refine text gets d1's direction. anchor_form() puts gen-dh's words back for stage 1.
GAZE_GEN = {"he": "turned toward the person he is speaking to, face in profile or three-quarter profile, eyes on that person",
            "she": "turned toward the person she is speaking to, face in profile or three-quarter profile, eyes on that person"}
_L = "his face three-quarter to screen left toward someone out of sight beyond the left edge of the frame, his eyes on that spot"
_R = "his face three-quarter to screen right toward someone out of sight beyond the right edge of the frame, his eyes on that spot"
_HR = "her face three-quarter to screen right toward someone out of sight beyond the right edge of the frame, her eyes on that spot"
# sid -> (pronoun, the direction sentence); s40 has two speakers: only the first (Wang Erniu, shouting at the dam) is replaced
GAZE_REFINE = {
    "s01": ("she", "her face three-quarter to screen left toward the yard gate beyond the left edge of the frame, her eyes on it"),
    "s02": ("he", "his face three-quarter to screen right toward the well beyond the right edge of the frame, his eyes on it"),
    "s03": ("she", "her face turning away from the yard gate beyond the left edge of the frame toward the right edge, her eyes on the earth"),
    "s09": ("she", _HR), "s11": ("she", _HR),
    "s12": ("she", "her face turning away toward the left edge of the frame, her chin tucked down, her eyes on the earth"),
    "s13": ("he", _L), "s17": ("she", _HR),
    "s23": ("he", "his face three-quarter to screen right, his eyes on the cracked earth beyond the right edge of the frame, lifted from the bowl"),
    "s25": ("he", _L),
    "s33": ("he", "his face three-quarter to screen right toward the dam beyond the right edge of the frame, his eyes on it"),
    "s34": ("he", "his face three-quarter to screen left, looking down toward someone out of sight beyond the lower left edge of the frame, his eyes on that spot"),
    "s37": ("he", "his face turned back over his left shoulder toward someone out of sight beyond the left edge of the frame, his eyes on that spot"),
    "s39": ("he", _L),
    "s40": ("he", "his face toward the rocks and the dam at the right of the frame, his eyes on them"),
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
# live_clips() writes no longer matches it. prep931.sh hands stage 1 the anchor form of the live file (this), then puts the
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
