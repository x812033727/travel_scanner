"""Episode 17 remake (r2): the writer spec for ../e001-r2/build-r2.py. Source: docs/videos/zhong-tian-qu-qi-e017-r2/script.md
(c01-c40 = s01-s40; the CG-era r2 script of PR #2024), including its sections 「這版改了什麼」, 「2026-11-06 審稿後的修改」 and
「真人版的改動（2026-11-15）」, which override the tables. Every line is the script's, word for word; only the staging changes.
Bible: production/r2-bible-e011-e020.md (rules 1-18).

Live action from the first draft, written the way e016-r2/r2.py stands AFTER its independent review (review.md in ../e016-r2)
and the e913-e915 picking lessons (colab/runs/e91{3,4,5}-live/{review-picks-a,review-picks-b,picks-merged}.tsv,
e913-live/pick-review.md, the _note of hailuo/edit-dh-e914-live.json):
- OFFSCREEN_SPEECH = False (bible rule 15): every shot with an off-screen line, a thought or a system line writes the silence
  of each person on screen (quiet(), SILENT_HE), after the action.
- Bible rule 18: nothing is negated by name; backgrounds say what is there. The long things people hold are written by their
  shape (Carpenter Shi's long bamboo pole, Erniu's carrying pole, Elder Han's walking staff: smooth and round, the ends bare);
  the copper plate and the mallet are small and sized against a hand; paper is never shot (the ledger is closed, its cover
  plain). A face that must not smile gets things it does, held after the last word.
- Hands and props are placed in the composition sentence (the first frame), each prop attached to its owner's named hand:
  the old mat in A-ling's arms (s11), in Xu Yan's left arm (s13-s26) and in A-ling's lap (s32-s34); the charred lantern in
  Xu Yan's right hand from s26; Erniu's carrying pole in his right hand; Elder Han's staff in his right hand; the mallet in
  Carpenter Shi's right hand; the rice-ball tray in Xiaohe's left hand. Contact between two people starts as a state in the
  first frame (s04 her hand already on his wrist, s13 his hand already on her forearm), never as a grab.
- Tang Xiaotang never speaks on camera (bible rule 3): her four lines (s10, s17, s23, s31) are from behind her (TBACK, nospeak;
  spec.json drops her three face pictures and her identity sentence), each saying she is the only one with buns and pink
  ribbons on one fixed side (and the only young woman when A-ling is not in the frame). Her silent face (s01, s18) gets
  e907's neutral face sentences in spec.json. Costume: the live portrait l1, cross-collared and closed (bible rule 4).
- Qin Shuang's s04 line is said from behind her (she holds Xu Yan back; the script's over-the-shoulder): nospeak, her pictures
  and identity sentence dropped (the e016 Lai San way). No weapon (bible rule 5): her belt is empty (extras.json).
- No more than three named faces in a shot (bible rule 1). The crowds are a few figures at fixed positions, never rushing in
  through a doorway (e914 s40/s42, the weakest shots): the script's fifteen fire-fighters become three or four villagers in a
  short line that is already standing; the ten rebuilders become two pairs carrying logs already in the frame.
- FIRE (risk-graded per animation-preproduction; kept in the background and at the edges): the burning papermaking hut stands
  beyond the low mud wall on the right of the yard picture (set-xujia-yuan-huo-l1, l3 with the burning roof beyond the right
  wall: the house on the left, the gate at the back, the persimmon tree in the middle, the well at the front right), so in every yard shot the flames are behind the wall and
  the smoke, the yard and every person on the near side, faces lit orange by the firelight. Nobody burns, nobody bleeds:
  A-ling comes out of the smoke with only soot on her dress (s11), the roof sinks down behind the wall beyond Qin Shuang (s15). The shots
  at the hut itself (s11, s12, s16) send no set picture (the yard picture would put the yard behind them): only smoke and
  an orange glow. Skin carries sweat and one broad smear of soot, never small specks (bible rule 12).
- Night is night (s27-s35: the bonfire and two blank paper lanterns); dawn is dawn (s36-s40 get their own picture).
- Nobody is flipped in the edit: every speaker wears a cross collar; sides are written as screen left/right.
State at the junction (e016 r2.py s42): the raft at dawn nearing the ferry landing; Tang Xiaotang kneeling with the oilcloth
packet, Xu Yan standing, Qin Shuang poling at the bow; black smoke behind the village. s01 is the next moment at the jetty.
Places (the coordinator's decisions, 2026-11-15; listed again in script.md 〈真人版的改動〉):
- the ferry landing set-dukou-l2 (e016's redraw, picked 2026-11-15 while this was written: the jetty empty, the nearest
  thatched house on the right bank burning under one column of black smoke): s01 only.
- the yard set-xujia-yuan-l3 (sunrise light from the right, the well at the front right), sent as its burning version
  set-xujia-yuan-huo-l1 (see below): s02-s10, s13-s15. The script's well
  "on the left" and gate "at the left front" follow the picture instead (bible 場景格局: the well is at the front right).
- The workshop pictures (live-action/screen-test-e017.py, seeds 37019/37020, run 2026-11-15; picked by the coordinator,
  refs-live/README.md, last paragraph): the e011-e020 test's set-zhifang-shao-l1 (an intact CG thatched house) and
  set-zhifang-gujia-ye-l1 (a pure 3D render) are never sent. gen-dh SET has three lines for them (shared edit, e910-e916
  rebuild byte for byte).
AFTER THE INDEPENDENT REVIEW (review.md in this folder, second version: 15 必改 and the 建議 taken; 2026-11-15):
- The yard shots s02-s10, s13-s15 send set-xujia-yuan-huo-l1 instead of l3 (必改 1): live-action/screen-test-e017.py --r2
  (seeds 37023/37024, manifest ~/mokaair-work/videos/_series/zhong-tian-qu-qi/live-screen-test-e017/r2.json, 2 jobs, not run
  yet), l3 with one change only (the e016 ferry lesson): beyond the right wall the thatched roof of the work shed burning under
  a rolling plume of dark smoke, firelight on the wall top. A new set id with its own l1, so pilot.py still finds l3 for
  set-xujia-yuan; spec.json "swap_pictures" (applied by prep917.sh) puts the new picture in. prep917.sh stops until it is in
  refs-live. The prompts write the burning roof above the wall top (BURN; s15 sinks it behind the wall).
- The burnt workshop s17-s26 sends NO set picture (必改 15: neither seed of set-zhifang-shao-l2 was taken): spec drop_set on
  all ten, the burnt state written first and plainly in ASH (charred stumps, pale grey ash, the burnt tub at the left, the
  soot-black back wall, the knocked-down fence on the right), each shot naming only one or two of those things. gen-dh's
  "burnt paper workshop" line still maps the place (so the set clause is there to drop, and the mat's "willow" never takes the
  stream); prep917.sh checks that no job sends any set-zhifang-shao picture.
- Night s27-s35 is written to match set-zhifang-gujia-ye-l2 = 37020 (必改 3: two dark timber posts and one long crossbeam,
  old charred roof beams at the top corners, poles lying at the right, charcoal lumps at the front right, the bonfire on pale
  stones at the front left; s28 raises the third post); dawn s36-s40 to set-zhifang-gujia-chen-l1 = 37019 (必改 4: four pale
  pine posts and rafters, the ladder at the right front post, the old burnt tub of embers at the front left with one paddle,
  a heap of grey charcoal along the left wall). The change of wood and posts from night to dawn is the time cut s35 -> s36.
- extras' "the air is clear and still" is replaced per scene where the prompt has smoke (必改 2, spec.json); A-ling's loose
  hair is written so it differs from her pictures (crown bare, hair down her chest) and only her portrait (s11, s13, s17) or
  angle-a (s12, s14) is sent (必改 10); the copper plate is a raised ring round a square hole, nothing written (必改 11); s01,
  s07, s09, s15, s16, s24, s25, s26 restaged (必改 14, 9, 12, 5, 13, 6, 7, 8).
- Inserts send no set picture (the e915 s08 lesson): s20 Qin Shuang's hand, s21 Xu Yan's finger, each picture only as the
  owner of the hand.
"""
EP = 917  # internal working number; the published slug is zhong-tian-qu-qi-e017-r2
SLUG = "zhong-tian-qu-qi-e017-r2"
EP_TITLE = "火裡搶簾子，一夜立起骨架（重製版 r2）"
OUTLINE_SECONDS = 202.5  # script.md: 202.5 s, 40 shots (16 + 10 + 14)
TARGET_MINUTES = [3, 4]
TITLE = "火裡搶簾子｜種田娶妻打天下 第17集（重製版）"
DESCRIPTION = "天亮回到柳溪口，紙坊已經燒成一片火海。石木匠喊簾子還在裡面，阿令把濕布往頭上一蓋就衝進濃煙；秦霜一把抓住要跟進去的許硯，站上井沿排出傳水的人龍，二牛挑水、韓伯叫全村拿桶來。阿令抱著編柳葉的那張竹簾衝出來，轉身還要回去，許硯拉住她：「簾子可以再做，妳不行。」草頂塌了，紙坊燒光。灰裡，秦霜拉出一個燒剩的燈籠骨架，底座釘著錢府的銅片，旁邊一行一深一淺的鞋印。當夜全村扛木頭來，天亮之前骨架立起來了，系統卻亮起紅框：七日內，縱火者認罪。《種田娶妻打天下》第 17 集（重製版）。"
THUMB = ("火裡搶簾子", "s11")
CHARACTERS = ["xuyan", "aling", "qinshuang", "tangxiaotang", "erniu", "hanbo", "shimujiang", "xiaohe", "xitong"]
MINOR = {}  # every speaker has a cast.json voice; the villagers are silent
MUSIC = "one cue per scene: an urgent cue of fast drums and driving strings at a farmhouse fire at dawn, one heavy accent when a young woman runs out of the smoke, a soft chime, one big crashing accent when a burning roof falls in and then it stops; a low cue of slow strings and a little wind over grey ash in the morning, one accent on a charred lantern and a second on a name; then a warm cue of steady drums and a work chant around a night bonfire, one rising accent at dawn and one cold low accent at the end; ancient Chinese rural drama, no vocals"

# Scene 1: the ferry landing at dawn (set-dukou-l2, s01), then the Xu yard at dawn with the papermaking hut burning beyond the
# right wall (set-xujia-yuan-huo-l1 swapped in for set-xujia-yuan-l3), the shots at the hut itself with no set picture (spec
# drop_set). Scene 2: the burnt paper workshop in the morning (no set picture, spec drop_set). Scene 3: the new timber frame at
# night (set-zhifang-gujia-ye-l2) and at dawn (set-zhifang-gujia-chen-l1). Close shots use the short `_c` headers.
# No person's name in a place phrase. gen-dh SET takes the FIRST pattern in its list order that the whole prompt matches: the
# yard prompts never say "shed", "workshop", "lean-to", "bridge", "raft" or "campfire" (the hut is "the papermaking hut", the fire
# at night is a "bonfire"); the ash prompts say "burnt paper workshop" and never "new timber frame"; the dawn prompts say "new
# timber frame at dawn"; no prompt says "Qian manor", "granary", "village entrance", "well pit" or "stream".
DUKOU = ("wide calm water reflecting the sky, a few tall bare wooden mooring posts standing in the water, a low wooden jetty "
         "of bare grey planks running out from the right bank, dry grass and reeds along the right bank, a dirt path up the bank "
         "to a cluster of low thatched and tiled village houses on the right, blue hills far off at the left")
# set-dukou-l2 as picked (e016 round 2): the nearest thatched house on the bank at the right is the one burning (the paper
# workshop), orange flames at its roof under one thick column of black smoke; the jetty runs from the left middle to the right bank.
SMOKE = ("the nearest thatched house on the bank at the right on fire, orange flames at its roof and one thick column of black "
         "smoke rolling up from it into the pale dawn sky, the red glow low on the far left horizon")
YARD = ("the low thatched farmhouse with its dark open doorway, one lattice window and a stack of split firewood on the left, a "
        "plain wooden yard gate under a small tiled roof in the back wall, a bare persimmon tree in the middle with only a few "
        "orange fruits high in its branches, one round stone well with a wooden windlass at the front right, the low mud wall "
        "running along the right")
# review.md 必改 1: the yard shots send set-xujia-yuan-huo-l1 (screen-test-e017.py --r2: l3 with one change, the burning thatched
# roof of the work shed standing just beyond the right wall under a rolling plume of dark smoke, firelight on the wall top).
BURN = ("beyond the low mud wall on the right the thatched papermaking hut next door is on fire, its burning thatched roof "
        "showing just above the wall top: tall orange flames along the thatch and one thick plume of dark grey smoke rolling up "
        "and drifting to the right, the orange firelight on the top of the wall, every flame staying beyond the wall")
# review.md 必改 15: neither seed of the burnt-shed screen test was taken, so s17-s26 send no set picture (spec drop_set) and
# the burnt state is written first and plainly; every shot names only one or two things of it, each always on the same side.
ASH = ("the papermaking shed has burned down to its floor and the open pale morning sky is overhead; a few charred black posts "
       "snapped off at knee height stand up out of a floor of soft pale grey ash; long charred black bamboo poles lie across "
       "the ash; at the left one big round wooden tub burnt black, its staves split and leaning; the low stone back wall "
       "streaked black with soot from the ground to its top; a few thin wisps of white smoke rise straight up from the ash; "
       "beyond the open right side a low fence of plain bamboo stakes with one stretch knocked flat on the ground")
# review.md 必改 3: set-zhifang-gujia-ye-l2 as picked (37020): the frame is going up. Two dark timber posts (a little left of
# the middle, and at the right) joined by one long crossbeam, old charred roof beams left at the top corners, a bundle of long
# poles flat on the ground at the right, black charcoal lumps at the front right, the bonfire on pale stones at the front left.
FRAME_N = ("the swept stone floor, the low stone back wall and left wall, a few charred old roof beams still overhead at the top "
           "left and top right corners; two tall timber posts standing, one a little left of the middle and one at the right, "
           "joined across the top by one long crossbeam; a bundle of long peeled poles lying flat on the ground at the right; a "
           "long low spread of black charcoal lumps on the ground at the front right; a squat stone mortar in the middle")
FIRE_N = ("at the front left a bonfire of split logs on a ring of pale stones; two plain round pale paper lanterns glowing, "
          "hanging from the crossbeam")
# review.md 必改 4: set-zhifang-gujia-chen-l1 as picked (37019): four pale peeled pine posts with crossbeams and rafter poles,
# a ladder at the right front post, the old tub at the front left full of grey embers (its stirring stick written as one short
# paddle resting in it), a heap of grey charcoal lumps along the left wall, tiled roofs beyond the walls.
FRAME_D = ("the swept stone floor, the low stone back wall and left wall with tiled roofs beyond them; in the middle the finished "
           "frame of freshly peeled pale pine, four tall round posts with crossbeams and rafter poles laid across their tops, "
           "open to the sky; one plain wooden ladder leaning against the right front post; along the foot of the left wall a "
           "long low heap of grey charcoal lumps; at the front left the old round wooden tub, burnt dark, filled with grey "
           "embers, one short wooden stirring paddle resting in it, one thin thread of white smoke rising from it; a squat stone "
           "mortar in the middle")
LOC = {
    "dukou": f"At the ferry landing below the village at dawn: {DUKOU}; {SMOKE}; cool dawn light",
    "fire": f"In the farmhouse yard of the Xu family at dawn on a dry clear autumn morning: {YARD}; {BURN}; the orange firelight falling across the yard and on every face",
    "fire_c": "In the Xu farmhouse yard at dawn, orange firelight from the burning papermaking hut on the right and grey smoke drifting across",
    "smoke": "Beside the burning papermaking hut next to the Xu farmhouse yard at dawn: thick grey smoke filling the air, a deep orange glow of fire far behind the smoke",
    "ash": f"In the burnt paper workshop beside the Xu farmhouse on the morning after the fire: {ASH}; bright clear morning sunlight from the right, crisp shadows on the ash",
    # 必改 15 short header; 建議 s21: "blank" (the preflight paper warning on the place name; the ash is smooth and bare)
    "ash_c": "In the burnt paper workshop on the morning after the fire, smooth blank pale grey ash and charred black posts, bright morning sunlight from the right",
    "night": f"At the new timber frame being raised on the site of the burnt papermaking shed beside the Xu farmhouse late at night: {FRAME_N}; {FIRE_N}; deep dark night, a black sky full of small stars, only the bonfire and the two lanterns giving warm light",
    "night_c": "Beside the two standing posts of the new timber frame by the Xu farmhouse late at night, deep dark night, the warm orange light of a bonfire",
    "dawn": f"At the new timber frame at dawn on the site of the burnt papermaking shed beside the Xu farmhouse: {FRAME_D}; the pale dawn sky above, cool dawn light with low gold light from the right on the new pine",
    "dawn_c": "At the new timber frame at dawn beside the Xu farmhouse, cool dawn light and low gold light from the right",
}
LIGHT = {
    "dukou": "the cool dawn light and the column of smoke stay unchanged",
    "fire": "the orange firelight from the right and the grey smoke stay unchanged, every flame staying beyond the wall",
    "smoke": "the grey smoke and the orange glow far behind it stay unchanged",
    "ash": "the bright morning sunlight from the right stays unchanged",
    "night": "the deep night, the warm bonfire light and the two lantern glows stay unchanged, the sky stays black",
    "dawn": "the cool dawn light and the low gold light from the right stay unchanged",
}
# bible rule 15: no "<X> speaks off screen" / "the system voice speaks off screen".
OFFSCREEN_SPEECH = False

# Repeated wording (each prop is one object).
XU_COAT = "Xu Yan, in an old plain grey cloth outer coat over his faded blue-grey scholar's robe"
XU_SOOT = ("Xu Yan, in his faded blue-grey scholar's robe patched at one elbow, the sleeves rolled up to his elbows, robe and "
           "sleeves grey with soot, his face shiny with sweat, one broad dark smear of soot across his left cheek")
QIN = ("her dark brown cross-collared short jacket with the sleeves pushed up to her elbows, wide plain leather belt with nothing "
       "tucked in it and nothing hanging from it, black trousers, leather boots and high ponytail tied with black cord")
TANG = "in her peach-pink cross-collared short jacket wrapped shut over a pleated skirt with a ribbon bow"
GOLD = "the small gold abacus hanging at her right hip"
# 建議 s03: before the fire her dress is clean and her hair has never come down.
ALING_CLEAN = ("A-ling, in her plain grey-white cotton dress with long sleeves covering her wrists, the dress clean, her black hair "
               "pinned up with one plain wooden hairpin")
ALING_UP = ("A-ling, in her plain grey-white cotton dress with long sleeves covering her wrists, grey with soot, her black hair "
            "pinned up again with one plain wooden hairpin")
# 必改 10: the hair written so it differs from every reference picture (they all have the topknot and the pin on the crown):
# the crown smooth and bare, the hair over both shoulders and down her chest. Wet in the fire (s11-s14), dry the next morning
# (s17). spec.json sends her portrait only (s11, s13, s17) or her angle-a only (s12, s14).
def aling_loose(wet=True):
    hair = ("the wet hair falling loose over both shoulders and down her chest, a few strands stuck to her damp cheek" if wet else
            "the hair falling loose over both shoulders and down her chest")
    return ("A-ling, in her plain grey-white cotton dress with long sleeves covering her wrists, grey with soot, one broad smear "
            "of soot across her right cheek, her long glossy black hair let down completely: the crown of her head smooth and "
            f"bare, {hair}")


ALING_LOOSE = aling_loose()
ERNIU = "Wang Erniu, in his coarse brown cross-collared short jacket with the sleeves rolled up, grey with soot"
STAFF = "one polished old bamboo walking staff as tall as his shoulder, smooth and round along its whole length"
HAN = f"Elder Han, in his washed-out grey cotton long robe, his long white beard down to his chest, {STAFF} in his right hand"
CARP = ("Carpenter Shi, in his faded brown cross-collared short work jacket with the sleeves rolled up and his worn brown "
        "leather apron, both grey with soot, one plain wooden stick through his grey topknot")
XIAOHE = ("little Xiaohe, the eight-year-old girl, in her patched lilac cotton jacket, two little pigtails tied with red string, a "
          "small woven straw rabbit tucked into her sash")
SHIPOLE = "one long pole of plain green bamboo as long as two men, smooth and round along its whole length, both ends cut flat"
PUNT = ("one long punting pole of plain green bamboo about twice a man's height and as thick as a wrist, smooth and round along "
        "its whole length, both ends cut flat")
CARRY = "one plain wooden carrying pole as long as a man, flat and smooth, one short rope hanging from each end"
BUCKET = "one plain wooden bucket with a rope handle"
CLOTH = "one square of plain grey cotton cloth"
PACKET = "one small square packet wrapped in brown oilcloth and tied with string, the size of a book"
MALLET = "one wooden mallet, its plain round wooden head the size of his fist on a short handle"
TRAY = "one small round flat bamboo tray with five plain white rice balls on it"  # 建議 s30: one is already in her hand
RICE = "one plain white rice ball the size of a child's fist"
ABACUS = "one plain dark wooden abacus with a plain frame and plain round wooden beads"
LEDGER = "one thread-bound ledger lying closed, its cover plain dark blue cloth"
HAIRPIN = "one plain wooden hairpin as long as a finger"
LANTERN = ("the charred remains of one small round paper lantern: a ring of blackened bamboo strips the size of two hands, its "
           "blank paper burned away to a few brown edges, and "
           "fixed at its base one small round copper plate as small as a thumbnail, with one raised plain ring around a small "
           "square hole cut through its centre, the metal smooth and polished between the ring and the hole")  # 必改 11


def mat(pr="his"):
    """e914 fix1 s30/s32: the mould is written only by its shape and carried flat like a tray. The oldest of the three."""
    return ("a flat rectangular mat of thin split bamboo strips laid close side by side, as wide as " + pr + " shoulders and as "
            "deep as " + pr + " forearm is long, edged with a thin plain wooden border, the strips an old deep honey colour, one "
            "small willow-leaf shape woven into its middle in darker strips")


VILL = ("in Song-dynasty cross-collared coarse cotton short jackets and cloth head-wraps, cloth shoes, small and soft, their faces "
        "seen only from the side")
HANDS = "their hands hold only what is described here"
TBACK = ("one young woman seen only from behind, appearing only once: the back of her head with two looped buns tied with pink "
         "silk ribbons and pearl pins, two long pink silk ribbons hanging from the buns down over her shoulders, a pink inner "
         "collar at the nape of her neck and her light peach-pink silk shoulders; the back of her head toward us the whole time, "
         "her ear the furthest round her head we ever see, only hair, ribbons and shoulders, her face turned fully away")


def only_tang(side, alone_woman=True):
    """e915 s26/s41: a second Tang appeared beside her back. One person with buns and ribbons, one fixed side."""
    w = "the only young woman in the frame and " if alone_woman else ""
    return (f"she is {w}the only one in the frame with buns and pink ribbons, and she stays in the {side} foreground from the "
            f"first frame to the last")


QIN_BACK = ("one young woman seen only from behind, appearing only once: only the back of her head with her high ponytail tied "
            "with black cord and her left shoulder in a dark brown jacket with the sleeve pushed up, soft, her head turned fully "
            "away from us, her ear, cheek and profile never visible, her face never in the frame")
ALING_BACK = ("one young woman seen only from behind, appearing only once: only the back of her head with her black hair pinned "
              "up with one plain wooden hairpin and her shoulder in a grey-white cotton dress, soft, her face never in the frame")
ERNIU_BACK = ("one big broad-shouldered young man seen only from behind, appearing only once: only the back of his head with a "
              "small topknot and his broad shoulders in a coarse brown jacket, soft, his face never in the frame")
# 必改 6, 7: the carrying pole rests on Erniu's right shoulder in s24-s25, never swung.
CARRY_SH = ("the plain flat wooden carrying pole as long as a man resting across his right shoulder, his right hand on it, its two "
            "short ropes hanging loose")
# 必改 7: Elder Han's staff held level in both hands (s25): his sentence without "in his right hand".
HAN_BARE = "Elder Han, in his washed-out grey cotton long robe, his long white beard down to his chest"
SILENT_HE = "He says nothing in this shot: his lips stay pressed together from the first frame to the last, his jaw still, no talking, no mouthing words"
HEADSTILL_TANG = "the young woman with the two buns and pink ribbons keeps her head still, the back of her head toward us the whole shot"


def quiet(who, pr="his", plural=False):
    verb = "say" if plural else "says"
    return (f"{who} {verb} nothing in this shot: {pr} lips stay pressed together from the first frame to the last, no talking, "
            f"no mouthing words, the face set and still")


SHOTS = [
    # ---- scene 1: the fire. s01 at the ferry landing (the raft has just reached the jetty; the jetty runs to the right bank
    # and the village path on the right). No replay of e016 s42: Xu Yan is already in the air.
    dict(chapter="火場", loc="dukou", cam="Wide shot, slow push in", chars=["xuyan", "qinshuang", "tangxiaotang"], night="dukou", act=3,
         comp=f"wide shot from the water: the bamboo raft of eight lashed green bamboo poles just bumping against the far end of the low wooden jetty at the left of the middle; {XU_COAT}, framed full length, small, already landed on the jetty planks, running along them toward the bank at the right, his face three-quarter to screen right toward the burning house, never the lens; urgent: brows drawn, mouth set; behind him Qin Shuang, {QIN}, framed full length, small, stepping off the raft onto the jetty, one boot on the raft and one on the planks, {PUNT} falling from her right hand onto the raft; kneeling in the middle of the raft Tang Xiaotang {TANG}, small, {PACKET} held against her in both arms, her face three-quarter to screen right toward the smoke, never the lens; afraid: brows drawn up, lips closed; exactly three people",
         lines=[],
         motion=f"Xu Yan runs along the jetty toward the bank at the right; Qin Shuang lets the pole drop, steps up onto the jetty and runs after him; Tang Xiaotang stays kneeling on the raft, hugging the packet; {quiet('Xu Yan, Qin Shuang and Tang Xiaotang', 'their', True)}",
         zh="全景、慢推（送 e016 重畫的 `set-dukou-l2`：棧橋空著、右岸最近那間草屋著火冒黑煙）：竹筏剛撞上棧橋左邊的盡頭；許硯（外披舊灰外衣）第一格已經落在棧橋上、往畫右著火的那間屋子跑（審稿必改 14：不寫跳在半空）；秦霜一腳在筏上、一腳踏上棧橋，竹篙從右手掉在筏上，跨上去跟著跑；唐小棠跪在筏中間抱著油布小包（小、中性臉、嘴閉著）；三人嘴閉著（無台詞）"),
    # The yard (set-xujia-yuan-l3): the hut burns beyond the mud wall on the right; Carpenter Shi by that wall.
    dict(loc="fire", cam="Medium-wide shot, slow push in", chars=["shimujiang"], night="fire",
         comp=f"medium-wide shot: on screen right beside the low mud wall {CARP}, framed from the knees up with clear space above his head, {SHIPOLE} held up in both hands, its far end reaching over the wall toward the burning thatch, his face three-quarter to screen left toward Xu Yan off screen left, never the lens; frantic: brows knotted, eyes wide, mouth wide open between words, sweat on his face; the persimmon tree and the yard gate soft behind him at the left; he is alone in the yard; {HANDS}",
         lines=[("shimujiang", "簾子還在裡面！三張都掛在架子上！", "嘶喊")],
         motion="Carpenter Shi shoves the long pole up over the wall into the smoke once, then swings his head round toward screen left and shouts; after the last word he turns back to the fire, his jaw set, the pole still in both hands",
         zh="中全景、慢推（院子 l3：紙坊在畫右土牆外燒，火都在牆那邊）：石木匠（皮圍裙、衣服灰）在畫右土牆邊，兩手把一根兩人長的青竹竿往牆外的火裡一捅，回頭朝畫左（許硯跑進來的方向）嘶喊；說完轉回去對著火、咬牙；不笑（原稿的跟拍改慢推：他不走動）"),
    # A-ling at the well (front right in the picture); Xu Yan's short shout is off screen.
    dict(loc="fire", cam="Medium shot, slow push in", chars=["aling"], night="fire",
         comp=f"medium shot: at the round stone well a little right of the middle {ALING_CLEAN}, framed from the knees up with clear space above her head, {CLOTH} in both hands over {BUCKET} full of water standing on the stone rim of the well, her face three-quarter to screen right toward the fire beyond the wall, never the lens; set and fearless: brows level, eyes narrowed on the smoke, lips pressed shut; the wooden windlass beside her; {HANDS}",
         lines=[("xuyan", "阿令！", "短喊")],
         motion=f"A-ling plunges the cloth into the bucket, throws the dripping cloth over her head and shoulders and runs out of the frame to the right toward the smoke; {quiet('A-ling', 'her')}",
         zh="中景、慢推：阿令（衣服還乾淨、木簪挽髮）在前右的石井邊（畫面中偏右），兩手把一塊灰布浸進井沿上的水桶，濕淋淋地往頭上肩上一蓋，往畫右的煙衝出畫面；嘴閉著（許硯「阿令！」短喊在畫外）"),
    # The script's over-the-shoulder from behind Qin Shuang: her back (her line nospeak; spec drops her pictures and sentence).
    dict(loc="fire", cam="Over-the-shoulder medium shot, slow push in", chars=["qinshuang", "xuyan"], nospeak=["qinshuang"], night="fire",
         comp=f"over-the-shoulder medium shot from close behind {QIN_BACK}, in the left foreground, her left arm reaching forward, her left hand already gripping Xu Yan's right wrist at the bottom of the frame from the first frame; facing us a step away a little right of the middle, {XU_COAT}, framed from the waist up with clear space above his head, his body straining toward the fire at the right, his face three-quarter to screen left toward her, never the lens; desperate: brows drawn up, jaw tight, lips pressed shut; behind him only the low mud wall and the grey smoke lit orange; {HANDS}; exactly two people, the young woman in the foreground seen only from behind",
         lines=[("qinshuang", "別進去，你不會躲火。你去顧井，我叫人排水。", "不笑，很快")],
         motion="the young woman with the ponytail in the left foreground keeps her head still, the back of her head toward us the whole shot, her hand holding his wrist; Xu Yan pulls once toward the fire, is held, and stops; his eyes go to her hand on his wrist, then back to her",
         zh="過肩中景、慢推：前景左只有秦霜的後腦、高馬尾與肩（背對鏡頭說話，nospeak；spec 拿掉她的參考圖與身分句），她的左手第一格就已經抓著許硯的右手腕（接觸寫成第一格的狀態，不演『抓』）；許硯（外衣）在畫面中偏右，身體往畫右的火掙一下、被拉住、停下，眼睛看手腕再回到她；嘴閉著。台詞剪接放錄音"),
    dict(loc="fire_c", cam="Close-up, slow push in", chars=["xuyan"], night="fire",
         comp=f"close-up of {XU_COAT}, framed from the chest up with space above his head, the orange firelight from the right on his face, his face three-quarter to screen right toward the fire, never the lens; torn: jaw clenched, brows drawn hard, eyes fixed on the smoke; behind him only drifting grey smoke and the bare persimmon branches",
         lines=[("xitong", "宿主衝進去，只會多一個要人救的。", "冷，毒舌"), ("xuyan", "我知道……可我也不能站在外面看。", "咬牙，心裡回嘴", "inner")],
         motion=f"Xu Yan stares at the fire with his jaw clenched, then lowers his eyes to his right wrist and lets out one long breath through his nose; {SILENT_HE}; he is thinking, not speaking",
         zh="近景、慢推（火光從畫右照在臉上，身後只有煙與光禿的柿子枝）：許硯咬牙盯著火，再低頭看被抓過的右手腕，鼻子長長吐一口氣；全程嘴閉著（系統吐槽與心裡話畫外，吐槽不出面板）。不寫藍光"),
    # Qin Shuang on the well rim; Xiaohe far back in the doorway; three villagers already at the gate (no rushing in).
    dict(loc="fire", cam="Wide shot, slow push in", chars=["qinshuang", "xiaohe"], night="fire",
         comp=f"wide shot: at the front right Qin Shuang, {QIN}, standing up on the low stone rim of the round well beside its wooden windlass, framed full length with clear space above her head, her body turned toward the wall and the fire at the right, her right arm stretched out toward them, her head turned over her left shoulder toward the yard gate at the back, never the lens; commanding: brows drawn, eyes hard, mouth wide between words; far back in the dark doorway of the farmhouse at the left, small, {XIAOHE}, standing still, both hands on the door frame, afraid: eyes wide, lips closed; at the yard gate at the back three villagers {VILL}, each holding {BUCKET}, standing still; {HANDS}",
         lines=[("qinshuang", "從井邊排一條，一桶接一桶傳過去！", "大喊")],
         motion=f"Qin Shuang sweeps her right arm from the well toward the wall and the fire; the three villagers at the gate start toward the well with their buckets; {quiet('little Xiaohe', 'her')}; the villagers say nothing; after the last word Qin Shuang's jaw sets",
         zh="全景、慢推：前右秦霜（腰帶空著、袖子推起）站上石井沿、木轆轤旁，身體朝畫右的牆與火、右手臂伸向那邊，頭從左肩轉回去對著後面的院門大喊（審稿建議：右臂不往身後揮）；遠處左邊屋門口小禾扶著門框（小，害怕，嘴閉著）；院門口三個拿木桶的村民（宋式短打、布包頭，小）往井走過來（審稿教訓：不拍一群人從門口湧進來；唐小棠放油布小包這拍拿掉）；不笑"),
    # Erniu with his carrying pole and two buckets, at the wall.
    dict(loc="fire", cam="Medium shot, slow push in", chars=["erniu"], night="fire",
         comp=f"medium shot: on screen right by the low mud wall {ERNIU}, framed from the knees up with clear space above his head, {CARRY} already lying on the ground at his feet with one full wooden bucket beside it, {BUCKET} full of water held up in both his hands by its rim and bottom at chest height against the top of the wall, his face three-quarter to screen right toward the fire, never the lens; furious and straining: teeth gritted, brows knotted low, mouth wide between words, sweat on his face; beyond the wall the grey smoke lit orange; {HANDS}",
         lines=[("erniu", "水來了！前面的退開，我要潑了！", "大吼")],
         motion="Wang Erniu heaves the bucket up and tips it over the top of the wall; the water pours out over the wall top and falls away behind the wall out of sight; after the last word he lowers the empty bucket, teeth gritted",
         zh="中景、慢推（原稿跟拍改慢推）：畫右土牆邊二牛（袖子捲起、衣服灰），第一格扁擔已平放在腳邊、旁邊一桶滿水，另一桶已在兩手（抓桶沿與桶底、胸口高、抵著牆頭）；把桶舉起往牆頭一倒，水越過牆頭落到牆後看不見的地方，大吼；說完放下空桶、咬牙（審稿必改 9：一鏡只一拍）；不笑"),
    dict(loc="fire", cam="Low-angle medium shot, slow push in", chars=["hanbo"], night="fire",
         comp=f"low-angle medium shot: in the plain wooden yard gate at the back {HAN}, framed from the knees up with clear space above his head, the orange firelight from the right on his face and beard, his face turned back over his left shoulder toward the village lane outside the gate, never the lens; stern and urgent: brows drawn, eyes hard, lips moving firmly between words; the tiled gate roof above him; {HANDS}",
         lines=[("hanbo", "全村的，都拿桶來！一戶都不許關門！", "揚聲")],
         motion="Elder Han stamps the foot of his staff once on the ground, then raises his left arm high and waves it toward the lane outside the gate; after the last word his mouth sets in a hard line",
         zh="低角度中景、慢推：韓伯（白長鬚、灰長袍、右手竹杖）站在後面的院門口，竹杖往地上一頓，回頭朝門外的村路舉左手揮，揚聲說；火光從畫右照在臉和鬍子上；不笑"),
    # The bucket line from the well to the wall; Xu Yan at the windlass, his coat already thrown over the well rim.
    dict(loc="fire", cam="Wide shot, slow push in", chars=["xuyan"], night="fire", act=3,
         comp=f"wide shot past one wooden bucket held up in the right foreground by two hands in coarse brown sleeves at the right edge, the villager's face out of the frame: at the round stone well {XU_SOOT}, framed full length, both hands on the handle of the wooden windlass, his grey outer coat lying thrown over the stone rim beside him, his face three-quarter to screen right, never the lens; straining: jaw set, brows drawn; four villagers {VILL}, standing in a short line from the well to the low mud wall at the right, each holding {BUCKET}; beyond the wall the grey smoke lit orange; {HANDS}",
         lines=[],
         motion=f"Xu Yan winds the windlass round twice, lifts the full bucket off its rope and hands it to the villager beside him, and each bucket passes from hand to hand along the line toward the wall; {quiet('Xu Yan')}; the villagers say nothing",
         zh="全景、慢推、前景是一個傳過去的木桶（畫右緣一雙粗布褐袖的手拿著，臉在畫外；審稿必改 12）：許硯在石井邊兩手搖轆轤（外衣第一格已經丟在井沿上，袖子捲起、衣服灰）拉起一桶水交給旁邊的村民；四個村民從井排到畫右土牆，木桶一個一個傳過去（每個桶在一個人手上）；所有人嘴閉著（無台詞）"),
    # Tang Xiaotang in the line, from behind (her line nospeak).
    dict(loc="fire", cam="Medium shot, slow push in", chars=["tangxiaotang"], nospeak=["tangxiaotang"], night="fire",
         comp=f"medium shot from behind and a little to her left: {TBACK}, standing in the bucket line in the left foreground, {GOLD}, both her hands passing {BUCKET} to one villager on her right, a man in a coarse brown short jacket and cloth head-wrap, soft, his face seen only from the side; {only_tang('left')}; beyond them over the low mud wall at the right the grey smoke lit orange; {HANDS}",
         lines=[("tangxiaotang", "阿令還沒出來！進去快一盞茶了！", "急到破音")],
         motion=f"the young woman hands the bucket over to the man on her right and keeps her face toward the smoke at the right; the man passes the bucket on; {HEADSTILL_TANG}; the man says nothing, his lips closed",
         zh="【改背後拍】中景、從她左後方拍、慢推：前景左唐小棠在傳水的人龍裡，兩手把木桶交給右邊一個男村民（側臉、虛焦），臉一直朝畫右牆外的煙；畫面裡只有她一個年輕女子、一個雙丸子頭粉緞帶的人，頭始終不轉。台詞 nospeak，剪接放錄音"),
    # A-ling comes out of the smoke (no set picture: only smoke and the glow behind it). Nothing burns on her.
    dict(loc="smoke", cam="Medium shot, slow push in", chars=["aling"], night="smoke", act=3,
         comp=f"medium shot at a gap in the low mud wall between the yard and the burning hut, the frame filled with thick grey smoke lit orange from far behind: {ALING_LOOSE}, already stumbling forward out of the smoke toward the camera a little left of the middle, framed from the knees up, {mat('her')} clutched flat against her chest in both arms, the wet grey cloth slipping off her shoulders, her face toward the ground ahead, never the lens; gasping: eyes squeezed half shut, lips parted for breath; her dress and hair are only grey with soot, the fire stays far behind in the smoke",
         lines=[],
         motion=f"A-ling stumbles two steps out of the smoke and drops onto her right knee, curling her body over the bamboo mat to shield it, and the grey cloth slides to the ground; {quiet('A-ling', 'her')}",
         zh="中景、慢推（spec 不送場景圖，只送阿令的定妝照：畫面只有院子與紙坊之間土牆缺口、被火光從後面照橘的濃煙）：阿令第一格已經從煙裡踉蹌衝出來（畫面中偏左），頭髮全散下（頭頂光、沒有髻和簪、濕髮披到胸前、幾縷貼在臉上）、臉頰一抹灰，兩臂把那張舊竹簾（竹色較深、正中編一片深色柳葉）平抱在胸前，濕灰布從肩上滑落；衝兩步單膝跪下，身體弓起護住竹簾；身上只有灰，火在後面的煙裡（無台詞）"),
    dict(loc="smoke", cam="Close-up, slow push in", chars=["aling"], night="smoke",
         comp=f"close-up of {ALING_LOOSE}, framed from the chest up with space above her head, {mat('her')} held out in both hands at the bottom of the frame toward screen left, where two hands in blue-grey sleeves rolled up to the elbows reach into the frame at the left edge to take it, her face three-quarter to screen left toward those hands, never the lens; breathless and urgent: brows drawn, eyes wide, lips moving between quick breaths; behind her only the low mud wall and the grey smoke lit orange",
         lines=[("aling", "這是最早那張……另外兩張還在架子上。", "喘")],
         motion="A-ling pushes the mat into the two hands at the left edge, which draw it away past the left edge; then she turns her head and shoulders toward the smoke at the right as if to go back in; after the last word her lips press shut, her eyes on the smoke",
         zh="近景、慢推（spec 不送場景圖，只送阿令的四分之三側面圖 angle-a；身後只有土牆與煙）：阿令頭髮散著（頭頂光、濕髮到胸前）、喘，兩手把竹簾往畫左緣伸進來的一雙捲袖的手（許硯，不點名）一塞，那雙手接走出畫；她轉頭轉肩朝畫右的煙、又要往回衝；說完抿嘴、盯著煙；不笑"),
    # Contact as a state from the first frame: his hand already on her forearm.
    dict(loc="fire", cam="Medium shot, slow push in", chars=["xuyan", "aling"], night="fire",
         comp=f"medium shot: on screen left {XU_SOOT}, framed from the waist up with clear space above his head, {mat()} clamped flat under his left arm, his right hand already holding A-ling's left forearm through her sleeve from the first frame, his face three-quarter to screen right toward her, never the lens; stern and heavy: brows drawn low, eyes fixed on her, lips moving slowly and firmly between words; on screen right {ALING_LOOSE}, framed from the waist up, half turned away toward the smoke at the right, her face in profile to screen right, never the lens, lips closed; behind them only the low mud wall and the grey smoke lit orange; {HANDS}; exactly two people",
         lines=[("xuyan", "阿令，簾子可以再做，妳不行。", "不笑，很重")],
         motion=f"A-ling leans toward the smoke and is held; she stops and turns her head back toward him; his hand stays on her forearm; {quiet('A-ling', 'her')}; after the last word his jaw sets and his eyes stay on hers",
         zh="中景、慢推：畫左許硯（袖子捲起、衣服灰、左臉一抹灰）左臂夾著竹簾，右手第一格就已經隔著袖子握住阿令的左前臂（接觸寫成狀態）；畫右阿令（散髮）半轉身朝畫右的煙、被拉住、停下、回頭看他；許硯慢慢、很重地說；說完咬住下巴；不笑"),
    dict(loc="fire_c", cam="Close-up, slow push in", chars=["aling"], night="fire",
         comp=f"close-up of {ALING_LOOSE}, framed from the chest up with space above her head, the orange firelight from the right on her cheek, her face three-quarter to screen left toward Xu Yan off screen left, never the lens; stunned and softening: brows slowly lifting, eyes on him, lips closed; behind her only grey smoke",
         lines=[("xitong", "叮。阿令，好感加一。", "宣布")],
         panel=[("阿令 好感 +1 → 19", "panel")],
         motion=f"A-ling looks back at him; the tension leaves her shoulders and her left arm slowly sinks down out of the frame; {quiet('A-ling', 'her')}",
         zh="近景、慢推（身後只有煙）：阿令回頭看他，肩膀鬆下來、被抓住的左臂慢慢垂下出畫；嘴閉著（系統畫外，面板疊上）"),
    # The roof falls in far behind Qin Shuang; she walks the people back (nobody touched).
    dict(loc="fire", cam="Wide shot, slow push in", chars=["qinshuang", "erniu"], night="fire",
         comp=f"wide shot: in the middle Qin Shuang, {QIN}, framed full length with clear space above her head, her back to the wall and the fire, both arms spread wide, her face three-quarter to screen left toward Wang Erniu, never the lens; fierce: brows drawn, eyes hard, mouth wide between words; on screen left in front of her {ERNIU}, framed full length, {BUCKET} empty in his right hand, his face three-quarter to screen right toward her and the fire, never the lens, teeth gritted; beyond the low mud wall at the right the burning thatched roof of the papermaking hut shows above the wall top in the smoke; {HANDS}; exactly two people",
         lines=[("qinshuang", "全部往後退！頂要塌了，別再靠近！", "大喊")],
         motion=f"beyond the wall the burning roof sinks down behind the wall and a cloud of orange sparks rises into the smoke; Qin Shuang steps forward toward screen left with her arms spread, herding him back, and Wang Erniu backs away toward screen left in front of her; {quiet('Wang Erniu')}; after the last word her jaw sets",
         zh="全景、慢推：秦霜在畫面中間、背對牆與火，張開雙臂面向畫左的二牛大喊，往畫左逼前一步、把他趕回去；畫左二牛右手提空桶、面朝她往畫左退（咬牙）（審稿必改 5：面向左走是前進不是倒退）；畫右土牆外第一格就看得到燒著的草頂露出牆頭，往下沉、一陣火星往煙裡竄（審稿建議）（火都在牆外遠處，原稿兩個村民拿掉；秦霜不碰人）；不笑"),
    dict(loc="smoke", cam="Close-up, slow push in", chars=["shimujiang"], night="smoke",
         comp=f"close-up of {CARP}, framed from the chest up with space above his head, sweat on his face, his empty hands hanging at his sides below the frame, his face three-quarter to screen left toward Xu Yan off screen left, never the lens; spent and bitter: brows knotted, eyes red-rimmed, the corners of his mouth pulled down, lips moving hoarsely between words; behind him only grey smoke and a low orange glow where the roof fell",
         lines=[("shimujiang", "那兩張簾子，跟著頂一起燒沒了。", "啞著嗓子")],
         motion="Carpenter Shi drags the back of his right hand once across his eyes and lets it fall, his eyes going back to Xu Yan off screen left; after the last word his mouth pulls down and his jaw works",
         zh="近景、慢推（spec 不送場景圖，身後只有煙與頂塌處的低低火光）：石木匠用右手背抹一下眼睛、放下，眼睛回到畫左的許硯（畫外），啞著嗓子說（審稿必改 13：只一個視線方向）（原稿丟竹竿那拍拿掉：近景裡長竿容易亂長）；說完嘴角往下、下巴動；不笑"),
    # ---- scene 2: the ash, the same morning (no set picture, review 必改 15: the burnt state in ASH, the knocked-down fence on
    # the open right side).
    dict(chapter="灰燼", loc="ash", cam="Medium-wide shot, slow push in", chars=["tangxiaotang", "aling"], nospeak=["tangxiaotang"], night="ash",
         comp=f"medium-wide shot past one charred post stump in the right foreground: {TBACK}, sitting on a low blackened stone step in the left foreground, hugging her knees, {GOLD}; {only_tang('left', False)}; beyond her a little right of the middle {aling_loose(False)}, framed full length, bending over the ash with her right hand reaching down to it, her face three-quarter to screen left, never the lens; quiet and drained: eyes lowered, lips closed; A-ling stays a little right of the middle from the first frame to the last; {HANDS}",
         lines=[("tangxiaotang", "紙坊……全沒了，架上晾的紙也一張不剩。", "聲音發顫")],
         motion=f"A-ling straightens up from the ash holding {HAIRPIN} in her right hand and looks down at it; the young woman on the step hugs her knees tighter, her shoulders shaking once; {HEADSTILL_TANG}; {quiet('A-ling', 'her')}",
         zh="【改背後拍】中全景、慢推、前景是一根燒焦的斷柱樁（審稿必改 15：燒毀版試鏡不取，s17–s26 不送場景圖，燒毀的樣子寫在文字裡；阿令只送定妝照）：前景左唐小棠坐在燒黑的石階上抱膝的背影（她是畫面裡唯一雙丸子頭粉緞帶的人）；後面畫面中偏右阿令（散髮）彎腰從灰裡撿起一支木簪、直起身低頭看（固定在中偏右）；唐小棠肩膀抖一下、抱得更緊；頭始終不轉。台詞 nospeak，剪接放錄音"),
    dict(loc="ash", cam="Medium shot, slow push in", chars=["xuyan", "tangxiaotang"], night="ash",
         comp=f"medium shot: on screen left Tang Xiaotang {TANG}, sitting on a low blackened stone step, her knees drawn up, {GOLD}, framed full length, her face three-quarter to screen right toward the mat, never the lens; drained: eyes lowered, lips closed; on screen right beside her {XU_SOOT}, crouching, framed full length with clear space above his head, {mat()} held upright on the ash in front of her in both hands, his face three-quarter to screen left toward her, never the lens; steady: brows level, eyes firm, lips moving evenly between words; behind them only charred post stumps and the soot-black wall; {HANDS}; exactly two people",
         lines=[("xuyan", "簾子在，紙就在。石叔，再做兩張要幾天？", "篤定")],
         motion=f"Xu Yan stands the mat up in front of her so she can see the willow leaf, then turns his head to screen right toward Carpenter Shi off screen right; Tang Xiaotang lifts her eyes to the mat; {quiet('Tang Xiaotang', 'her')}; after the last word his brows stay level, eyes on the right",
         zh="中景、慢推：畫左唐小棠坐在燒黑的石階上抱膝（中性臉、垂眼、嘴閉著）；畫右許硯蹲在她旁邊，兩手把竹簾立在灰上給她看柳葉，再轉頭朝畫右（石木匠，畫外）篤定地問；她抬眼看竹簾；不笑"),
    dict(loc="ash", cam="Medium shot, slow push in", chars=["shimujiang"], night="ash",
         comp=f"medium shot of {CARP}, already crouching beside the burnt black tub at the left, framed from the knees up with clear space above his head, one long half-burnt strip of bamboo in his right hand, pulled out of the ash, his face three-quarter to screen left toward Xu Yan off screen left, never the lens; gruff: brows knotted low, one eye narrowed, the corners of his mouth pulled down, lips moving curtly between words and pressed flat between them; behind him only the soot-black wall; {HANDS}",
         lines=[("shimujiang", "竹子還泡著，三天，兩張一張不少還你。", "嘴硬")],
         motion="Carpenter Shi turns the half-burnt strip over in his fingers and taps the ash off it against the tub; after the last word he snorts once through his nose and tosses the strip down into the ash",
         zh="中景、慢推：石木匠第一格已經蹲在燒黑的木桶邊，右手拿著一根從灰裡拉出來的半焦竹條，翻過來在桶邊敲掉灰，嘴硬地說；說完鼻子哼一聲、把竹條丟回灰裡（原稿用腳撥灰、蹲下這兩拍並進第一格）；不笑"),
    # The insert of Qin Shuang's hand (no set picture; her portrait only as the owner of the hand). Her line laid in.
    dict(loc="ash_c", cam="Insert close-up, slow push in", chars=["qinshuang"], nospeak=["qinshuang"], night="ash",
         comp=f"insert close-up, the shot opens directly on smooth grey ash on the ground from its very first frame: one hand in a dark brown sleeve pushed up to the forearm, smudged grey, already gripping the rim of {LANTERN}, half buried in the ash; only the hand, the sleeve, the ash and the charred lantern remains are in the frame; bright morning sunlight from the right",
         lines=[("qinshuang", "燈籠骨架。錢府門口的燈籠，都釘這塊銅片。", "冷")],
         motion="the hand draws the charred lantern remains up out of the ash and turns them so the small copper plate at the base faces us; grey ash slides off the blackened strips",
         zh="插鏡、慢推（第一格就是灰；spec 不送場景圖，只送秦霜的定妝照當手的主人）：一隻推起深褐袖子、沾灰的手第一格已經抓著半埋在灰裡的燒剩燈籠（一圈焦黑竹骨、兩個手掌大；底座一塊拇指甲大小的圓銅片，一圈凸起的素環圍著中間一個小方孔、沒有任何字，其餘光滑（審稿必改 11）），拉出來轉過來讓銅片朝鏡頭；灰從竹骨上滑落。台詞剪接放錄音（秦霜畫外）"),
    dict(loc="ash_c", cam="Low-angle insert close-up, slow push in", chars=["xuyan"], nospeak=["xuyan"], night="ash",
         comp="low insert close-up at ground level, the shot opens directly on a line of shoe prints pressed into smooth grey ash from its very first frame, running away from the camera toward the open side at the right, every second print deep and the prints between them shallow; one forefinger of a hand in a blue-grey sleeve rolled up to the elbow pointing at the nearest print at the bottom edge; only the hand, the ash and the prints are in the frame; bright morning sunlight from the right",
         lines=[("xuyan", "還有腳印，一路往籬笆外去了。", "低")],
         motion="the forefinger moves slowly along the line of prints from the nearest toward the far ones, then stops and points on toward the right",
         zh="低角度插鏡（貼地拍）、慢推（第一格就是灰上的一行鞋印；spec 不送場景圖，只送許硯四分之三側面圖當手的主人）：一行鞋印往畫右的開口延伸，一個深一個淺；一隻藍灰捲袖的手的食指從最近的鞋印沿著往遠處移、停住、往右一指。台詞剪接放錄音（許硯畫外）"),
    dict(loc="ash", cam="Medium shot, slow push in", chars=["qinshuang"], night="ash",
         comp=f"medium shot of Qin Shuang, {QIN}, crouching on the grey ash beside a line of shoe prints, framed from the knees up with clear space above her head, her right forefinger and middle finger pressed into one deep print, her face three-quarter to screen left toward Xu Yan off screen left, never the lens; cold: brows level, eyes hard, lips moving crisply between words; behind her the open right side and the knocked-down stretch of bamboo fence; {HANDS}",
         lines=[("qinshuang", "一腳深，一腳淺，走路的人是跛子。", "冷")],
         motion="Qin Shuang lifts her two fingers out of the deep print and presses them into the shallow one beside it, then lifts her eyes; after the last word her lips press into a hard line",
         zh="中景、慢推：秦霜蹲在鞋印旁，右手兩指第一格已經壓在一個深的鞋印裡，抬起來再壓旁邊淺的，抬眼冷冷地說；身後是開口與倒了一截的竹籬笆；說完抿成一條線；不笑"),
    dict(loc="ash", cam="Medium shot, slow push in", chars=["tangxiaotang"], nospeak=["tangxiaotang"], night="ash",
         comp=f"medium shot from behind and a little above: {TBACK}, rising from the low blackened stone step in the left foreground, {GOLD}; {only_tang('left')}; beyond her only grey ash, the burnt black tub at the left and the soot-black wall; nobody else in the frame",
         lines=[("tangxiaotang", "跛子……錢府的賴三，就是跛的！", "氣到發抖")],
         motion=f"the young woman stands up in one quick movement, drags her right sleeve across her face, then clenches both hands into fists at her sides, her shoulders shaking; {HEADSTILL_TANG}",
         zh="【改背後拍】中景、從背後稍高處、慢推：前景左唐小棠（跟 s17 同一側，審稿建議）從燒黑的石階一下站起來，右袖抹一把臉，兩手在身側握緊拳頭、肩膀發抖；前面只有灰、燒黑的木桶與燒黑的牆；畫面裡只有她一個人，頭始終不轉。台詞 nospeak，剪接放錄音"),
    dict(loc="ash", cam="Medium shot, tracking", chars=["erniu"], night="ash",
         comp=f"medium shot following him: {ERNIU}, framed from the knees up with clear space above his head, {CARRY_SH} from the first frame, striding toward screen left across the ash, his face three-quarter to screen left toward the yard gate ahead of him, never the lens; furious: teeth gritted, brows knotted low, nostrils flared, mouth wide between words; behind him only charred post stumps; {HANDS}",
         lines=[("erniu", "我這就去錢府，把那個跛子揪出來！", "怒")],
         motion="Wang Erniu strides three long steps toward screen left, the pole steady on his shoulder, shouting ahead toward the yard gate; after the last word his teeth stay gritted and he keeps walking",
         zh="中景、跟拍：二牛第一格扁擔已經扛在右肩、右手扶著（審稿必改 6：不揮、不握在手上當兵器；原稿『抄起』那拍並進第一格），大步往畫左走三步、朝前面的院門方向怒喊；說完咬牙繼續走；不笑"),
    dict(loc="ash", cam="Low-angle medium shot, slow push in", chars=["hanbo"], night="ash",
         comp=f"low-angle medium shot past {ERNIU_BACK}, in the right foreground, facing screen left, the carrying pole on his right shoulder; facing us a step in front of him, a little left of the middle, {HAN_BARE}, framed from the knees up with clear space above his head, his polished bamboo walking staff held level across his chest in both hands, a hand's width in front of the young man, his face three-quarter to screen right toward him, never the lens; grave: brows drawn, eyes steady, lips moving slowly and firmly between words; behind him only the charred stumps and the open sky; {HANDS}; exactly two people, the young man in the foreground seen only from behind",
         lines=[("hanbo", "沒人看見他放火，告到官府，官府也不認。", "沉聲")],
         motion="the young man in the right foreground keeps his head still, the back of his head toward us the whole shot, and stops, the carrying pole still on his shoulder; Elder Han holds the staff level across his chest; after the last word Elder Han's mouth sets and his eyes hold",
         zh="低角度中景、慢推：前景右只有二牛的後腦與寬肩（不點名、不送圖；面朝畫左、扁擔扛在右肩，接 s24 往畫左走；審稿必改 7），韓伯在他前面一步（畫面中偏左）、面朝畫右看他，兩手把竹杖橫在胸前、離他一掌，沉聲說；二牛停住、扁擔還在肩上；不笑"),
    # The mat goes to A-ling's hand in one beat; the lantern is already in his right hand (Qin Shuang handed it between shots).
    dict(loc="ash_c", cam="Close-up, slow push in", chars=["xuyan"], night="ash",
         comp=f"close-up of {XU_SOOT}, framed from the chest up with space above his head, {mat()} clamped under his left arm, which is on the screen-right side of his body, at the bottom right of the frame, his right hand holding {LANTERN} at chest height from the first frame, his face three-quarter to screen right toward Elder Han off screen right, never the lens; resolved: brows level, eyes hard, lips moving evenly between words; behind him only charred post stumps and the soot-black wall",
         lines=[("xuyan", "韓伯說得對。先把紙坊蓋回來，人，我會讓他自己認。", "定下來")],
         motion="one slender hand in a grey-white sleeve reaches in at the right edge, takes the mat from under his left arm and draws it away past the right edge; Xu Yan lifts the charred lantern in his right hand and looks at it, then raises his eyes; after the last word his jaw sets, lips pressed",
         zh="近景、慢推：許硯（滿臉汗、左臉一抹灰）左臂夾著竹簾、右手第一格已經拿著燒剩的燈籠（秦霜遞燈籠那拍拿掉，只留一拍交接）；竹簾在畫面右下（他臉朝畫右，左臂在身體的畫右那側）；畫右緣伸進來一隻灰白袖口的手（阿令，不點名）把竹簾從他臂下接走、從右緣出畫（審稿必改 8）；他舉起燈籠看一眼、再抬眼，定下來地說；說完咬住下巴；不笑"),
    # ---- scene 3: that night at the new frame (set-zhifang-gujia-ye-l2 = 37020: going up), then dawn (set-zhifang-gujia-chen-l1 = 37019).
    dict(chapter="一夜", loc="night", cam="Wide shot, slow push in", chars=["shimujiang"], night="night",
         comp=f"wide shot past the bonfire in the left foreground: in the middle between the two standing posts {CARP}, framed full length with clear space above his head, {MALLET} in his right hand pointing down at one dark post hole in the swept ground between the two standing posts, his eyes on the hole, never the lens; gruff and busy: brows knotted, lips moving curtly between words; two pairs of villagers {VILL}, already walking in from the left of the frame, each pair carrying one long timber post on their shoulders; {HANDS}",
         lines=[("shimujiang", "天亮之前，骨架給你立起來，少一根我賠。", "頭也不抬")],
         motion="Carpenter Shi taps the edge of the post hole twice with the mallet; the two pairs of villagers lower their posts to the ground beside it; the villagers say nothing; after the last word he snorts once and does not look up",
         zh="全景、慢推、前景是篝火（送挑好的 `set-zhifang-gujia-ye-l2` 37020：兩根深色木柱一根長橫梁、左上右上留著舊椽、右邊地上一束長木料、右前一片黑炭塊、左前淺色石圈篝火、兩盞空白燈籠；審稿必改 3 照圖寫）：石木匠在兩根立柱之間、右手木槌（拳頭大的圓木頭）指著地上的柱洞敲兩下，頭也不抬地說；兩對村民第一格已經在畫左、扛著一根長木柱走進來放下（原稿約十人改兩對、四人）；不笑"),
    dict(loc="night", cam="Low-angle medium shot, slow push in", chars=["erniu", "xuyan"], night="night",
         comp=f"low-angle medium shot: on screen left {ERNIU}, framed from the knees up with clear space above his head, and just to screen right of him {XU_SOOT}, framed from the knees up, both gripping one thick hemp rope in both hands, the rope running up to the top of one long timber post leaning at the right of the frame, its foot in a post hole, the third post of the frame; Erniu's face three-quarter to screen right toward the post, straining: teeth gritted, brows knotted, mouth wide between words; Xu Yan's face three-quarter to screen right, never the lens, jaw clenched, lips pressed shut; the bonfire light on them from the left; {HANDS}; exactly two people",
         lines=[("erniu", "一、二、起！這根柱子扶正了！", "咬牙使勁")],
         motion=f"both men lean back and haul together hand over hand, and the leaning post at the right rises slowly upright; {quiet('Xu Yan')}; after the last word Erniu lets out a hard breath, teeth still gritted",
         zh="低角度中景、慢推：畫左二牛、他右邊許硯，兩人兩手拉著一條繫在柱頂的粗麻繩，身體往後一仰一起使勁，畫右那根斜靠的長木柱（骨架的第三根柱）慢慢立直；二牛咬牙喊，許硯嘴閉著；篝火光從畫左照過來"),
    # Xiaohe may smile (script).
    dict(loc="night_c", cam="Low-angle medium shot, slow push in", chars=["xiaohe"], night="night",
         comp=f"low-angle medium shot at a child's height: {XIAOHE}, framed from the knees up with clear space above her head, {TRAY} held level in her left hand, {RICE} held up high in her right hand toward one hand in a blue-grey sleeve reaching down into the frame at the top right, her face tipped up three-quarter to screen right toward Xu Yan off screen above, never the lens; coaxing and bright: eyes wide, a small gap-toothed smile, lips moving sweetly between words; behind her only the warm bonfire glow and the dark",
         lines=[("xiaohe", "哥哥，你從早上到現在都沒吃，先吃一個！", "奶聲，催")],
         motion="little Xiaohe rises on her toes and pushes the rice ball up into the hand reaching down; the hand closes on it and lifts it away upward past the top edge",
         zh="低角度中景（小禾的高度）、慢推：小禾左手平端一個小竹盤（五個白飯糰），右手把一個飯糰舉高、踮起腳塞進畫右上方伸下來的一隻藍灰袖口的手（許硯，不點名），那隻手接走出畫；可以笑（缺門牙）"),
    dict(loc="night", cam="Medium shot, slow push in", chars=["xuyan", "xiaohe"], night="night",
         comp=f"medium shot: on screen left {XU_SOOT}, crouching down to her height, framed from the waist up with clear space above his head, {RICE} in his left hand, his right hand resting lightly on top of her head from the first frame, his face three-quarter to screen right toward her, never the lens; tired and gentle: eyes soft, brows eased, lips moving softly between words; on screen right {XIAOHE}, framed from the waist up, {TRAY} held in both hands, her face tipped up three-quarter to screen left toward him, never the lens, a small gap-toothed smile, lips closed; the bonfire glow on them; {HANDS}; exactly two people",
         lines=[("xuyan", "好，哥哥吃。妳去睡，明早起來看新紙坊。", "溫和")],
         motion=f"Xu Yan pats the top of her head once, slowly, and lifts his hand away, the rice ball still in his left hand; little Xiaohe nods hard; {quiet('little Xiaohe', 'her')}",
         zh="中景、慢推：畫左許硯蹲到她的高度，左手拿著飯糰，右手第一格就放在她頭頂、慢慢輕拍一下拿開，溫和地說；畫右小禾兩手端竹盤，仰臉看他、點頭（可以笑，嘴閉著）；不演咬飯糰（吃東西是高風險：杯子穿臉、嘴不動）"),
    # Tang Xiaotang by the bonfire, from behind (her line nospeak); the abacus and the closed ledger.
    dict(loc="night", cam="Medium shot, slow push in", chars=["tangxiaotang"], nospeak=["tangxiaotang"], night="night",
         comp=f"medium shot from behind and a little to her right: {TBACK}, sitting on a low wooden crate beside the bonfire in the left foreground, {ABACUS} on her knees, the only thing her hands touch, {LEDGER} on the crate beside her, the small gold abacus hanging at her right hip, still; {only_tang('left')}; beyond her across the firelit ground, small and soft, the two standing posts of the new frame and three villagers {VILL} carrying a long timber post; the bonfire light warm on her shoulders and ribbons; {HANDS}",
         lines=[("tangxiaotang", "四十二個人來幫工，每個人的工錢，我都記著。", "鼻子紅紅的")],
         motion=f"the young woman flicks the beads of the abacus with her right forefinger, three quick flicks, then lifts her head toward the workers and holds still; the villagers say nothing; {HEADSTILL_TANG}",
         zh="【改背後拍】中景、從她右後方拍、慢推：前景左唐小棠坐在篝火邊的矮木箱上的背影，膝上一把素木算盤（深色素框素珠）、身旁木箱上一本合起的線裝帳冊（素藍布封面、不翻開）；右手食指撥三下算珠、抬頭看幹活的人；後面遠處兩根立柱的新骨架與三個扛長木柱的村民（小、虛焦）；畫面裡只有她一個年輕女子，頭始終不轉。台詞 nospeak，剪接放錄音"),
    dict(loc="night", cam="Medium shot, slow push in", chars=["aling"], night="night",
         comp=f"medium shot: {ALING_UP}, sitting beside the bonfire a little left of the middle, framed from the knees up with clear space above her head, {mat('her')} lying across her knees, her right fingers on one charred strip at its edge, her face three-quarter to screen right, never the lens; quiet: brows level, eyes lifting, lips moving softly between words; the bonfire light warm on her face from the left; behind her only the dark and the firelit timber posts; {HANDS}",
         lines=[("aling", "起火前，我起來喝水，看見籬笆外一個背影。", "很輕")],
         motion="A-ling pulls the one charred strip out of the edge of the mat and drops it into the fire, then lifts her eyes to screen right; after the last word her lips close and her eyes stay on him",
         zh="中景、慢推：阿令頭髮已用木簪挽回去，坐在篝火邊（畫面中偏左），竹簾橫放在膝上，把簾邊一根燒焦的竹絲拔下丟進火裡，抬眼看畫右走過來的許硯，很輕地說；說完抿嘴看著他"),
    dict(loc="night", cam="Over-the-shoulder medium shot, slow push in", chars=["xuyan"], night="night",
         comp=f"over-the-shoulder medium shot from close behind {ALING_BACK}, in the left foreground, the edge of the bamboo mat on her knees soft at the bottom of the frame; facing us a step away a little right of the middle, {XU_SOOT}, already crouching beside her, framed from the waist up with clear space above his head, his hands resting on his knees, his face three-quarter to screen left toward her, never the lens; sharp and urgent: brows drawn, eyes intent, lips moving quickly between words; the bonfire light on his face from the left; behind him only the dark and one firelit timber post; {HANDS}; exactly two people, the young woman in the foreground seen only from behind",
         lines=[("xuyan", "看清楚臉了嗎？是不是賴三？", "急問")],
         motion="the young woman with the hairpin in the left foreground keeps her head still, the back of her head toward us the whole shot; Xu Yan's head turns sharply toward her and he leans in; after the last word his brows stay drawn, eyes on her",
         zh="過肩中景、慢推：前景左只有阿令的後腦（木簪挽髮）與肩、膝上竹簾的邊（不點名、不送圖）；許硯第一格已經蹲在她旁邊（畫面中偏右），猛一轉頭、往前傾，急急地問；她頭始終不轉；不笑"),
    dict(loc="night_c", cam="Close-up, slow push in", chars=["aling"], night="night",
         comp=f"close-up of {ALING_UP}, framed from the chest up with space above her head, the edge of the bamboo mat held in both hands at the bottom of the frame, her face three-quarter to screen right toward Xu Yan off screen right, never the lens; regretful: brows drawn together, eyes lowered, lips moving softly between words; behind her only the warm firelight and the dark",
         lines=[("aling", "太暗了，看不見臉，只看見他走路一拐一拐。", "輕")],
         motion="A-ling shakes her head once slowly, and her hands tighten on the edge of the mat; after the last word she presses her lips together and lifts her eyes to him",
         zh="近景、慢推（身後只有篝火光與黑）：阿令慢慢搖一下頭，兩手握緊竹簾邊，輕聲說；說完抿嘴、抬眼看他"),
    dict(loc="night_c", cam="Close-up, slow push in", chars=["xuyan"], night="night",
         comp=f"close-up of {XU_SOOT}, framed from the chest up with space above his head, the bonfire lighting half his face orange from the left and leaving the other half dark, {LANTERN} in his right hand at the bottom of the frame, his face lowered toward it, never the lens; brooding: brows drawn, eyes narrowed on the copper plate, lips pressed flat; behind him only the dark",
         lines=[("xuyan", "燈籠、腳印、背影，全指著賴三，可沒有一樣能上公堂。", "沉，心裡盤算", "inner")],
         motion=f"Xu Yan rubs his right thumb slowly across the small copper plate at the base of the charred lantern, then his hand goes still; {SILENT_HE}; he is thinking, not speaking",
         zh="近景、慢推：篝火照亮許硯半邊臉，他低頭看右手上的燒剩燈籠，拇指慢慢擦過那塊小銅片、停住；全程嘴閉著（心裡話畫外）"),
    dict(loc="dawn", cam="Wide shot, slow push in", chars=["shimujiang"], night="dawn",
         comp=f"wide shot past the old wooden tub of grey embers in the left foreground: the new pale pine frame standing in the middle; {CARP}, standing on the ladder at the right front post, framed full length, {MALLET} in his right hand raised to the joint of the last crossbeam, his face three-quarter to screen left toward the people below, never the lens; worn out: eyes red-rimmed, brows knotted, lips moving hoarsely between words; three villagers {VILL}, sitting slumped on the ground at the left of the frame, still; {HANDS}",
         lines=[("shimujiang", "立好了。我說天亮之前，就是天亮之前。", "啞著嗓子")],
         motion="Carpenter Shi knocks the crossbeam into its joint with two blows of the mallet, then lowers the mallet and looks down; the villagers say nothing; after the last word he lets out a long breath, his mouth pulled down",
         zh="全景、慢推、前景是左前那個燒黑的舊大木桶、裡面是灰燼（送挑好的 `set-zhifang-gujia-chen-l1` 37019：四根淺色剝皮松木柱、頂上橫梁椽木、右前柱靠梯、左牆根一堆灰炭塊；審稿必改 4 照圖寫）：白松骨架立在中間；石木匠站在右前柱的梯子上，右手木槌兩下把最後一根橫梁敲進榫頭，低頭啞著嗓子說（原稿下梯子那拍拿掉）；三個村民東倒西歪坐在畫左地上；不笑"),
    # Xu Yan may let the corner of his mouth ease (script).
    dict(loc="dawn", cam="Medium shot, slow push in", chars=["xuyan"], night="dawn",
         comp=f"medium shot past one new pale pine post at the left edge: {XU_SOOT}, standing in front of the new frame, framed from the waist up with clear space above his head, {LANTERN} hanging from his right hand at his side, his face tipped up three-quarter to screen right toward the crossbeams, never the lens; exhausted and relieved: brows easing, eyes tired, lips moving slowly between words; behind him the pale pine frame and the pale dawn sky; {HANDS}",
         lines=[("xuyan", "立起來了……紙坊還在，人也都在。", "累，嘴角一鬆")],
         motion="Xu Yan lifts his eyes up the new posts to the crossbeams and lets out one long breath, his shoulders dropping; after the last word the corner of his mouth eases a little, eyes still on the frame",
         zh="中景、慢推、前景左緣一根新柱子：許硯站在骨架前，右手垂著提著燒剩的燈籠，抬頭看橫梁，長長吐一口氣、肩膀鬆下來，累累地說；說完嘴角一鬆（本鏡可以）"),
    # The system shots: he says nothing (bible 15); no coloured light written (bible 11; the red frame is laid in the edit).
    dict(loc="dawn_c", cam="Close-up, slow push in", chars=["xuyan"], night="dawn",
         comp=f"close-up of {XU_SOOT}, framed from the chest up with space above his head, his face three-quarter to screen right, never the lens; the ease draining away: eyes narrowing, brows drawing together, lips pressing shut; behind him only the pale pine frame and the dawn sky",
         lines=[("xitong", "叮。強制任務：七日內，縱火者認罪。", "冷，宣布")],
         panel=[("強制任務：七日內，縱火者認罪", "task")],
         motion=f"the eased corner of Xu Yan's mouth flattens and his eyes narrow sharply; {SILENT_HE}",
         zh="近景、慢推（身後只有骨架與天光）：許硯鬆開的嘴角收回來、眼睛一縮；全程嘴閉著（系統畫外，紅框面板疊上；不寫紅光）"),
    dict(loc="dawn_c", cam="Close-up, slow push in", chars=["xuyan"], night="dawn",
         comp=f"close-up of {XU_SOOT}, framed from the chest up with space above his head, {LANTERN} in his right hand at the bottom of the frame, his face three-quarter to screen right, never the lens; stung and stubborn: brows knotting, eyes hard, jaw tight, lips pressed flat; behind him only the pale pine frame",
         lines=[("xitong", "失敗：失去種田技能。", "冷"), ("xuyan", "放火的是他，扣的倒是我的技能？", "不服，心裡回嘴", "inner"), ("xitong", "系統不抓人，只看結果。宿主自己想辦法。", "冷，毒舌")],
         panel=[("失敗：失去種田技能", "penalty")],
         motion=f"Xu Yan's grip on the charred lantern tightens and his brows knot; he glances sideways once in disbelief, then his eyes come back hard; {SILENT_HE}; he is thinking, not speaking",
         zh="近景、慢推（身後只有骨架）：許硯握燈籠的手一緊、眉頭皺起來，不服地往旁邊一瞥、再收回來；全程嘴閉著（系統兩句與心裡話畫外，紅框面板疊上）（長鏡）"),
    dict(loc="dawn", cam="Medium shot, slow push in", chars=["xuyan"], night="dawn",
         comp=f"medium shot: {XU_SOOT}, standing in front of the new frame, framed from the waist up with clear space above his head, {LANTERN} in his right hand, his face three-quarter to screen right, never the lens; set and cold: brows level and hard, eyes narrowed, lips pressed flat; behind him the pale pine frame and the dawn sky; {HANDS}",
         lines=[("xuyan", "七天……我要讓錢員外，自己開口認罪。", "沉，下決心", "inner")],
         motion=f"Xu Yan lifts the charred lantern up to his eyes, stares at the small copper plate at its base, and slowly closes his fingers tight round the blackened strips; {SILENT_HE}",
         zh="中景推到中近景、慢推：許硯把燒剩的燈籠舉到眼前，盯著底座那塊小銅片，慢慢握緊；全程嘴閉著（心裡話畫外；結尾，懸念接第 18 集）"),
]

HEAD = [
    "- 重製版 r2、真人版（站主 2026-11-11「之後都用真人版」）：照 `docs/videos/zhong-tian-qu-qi-e017-r2/script.md`（c01–c40 對應 s01–s40；2026-11-06 的 r2 稿；含「這版改了什麼」「2026-11-06 審稿後的修改」與「真人版的改動（2026-11-15）」）；台詞一字不改，只改拍法；每鏡一個看得見的動作、一句一筆不拆半句、預設不笑。篇章設定 `production/r2-bible-e011-e020.md`（拍法 1–18 條）。",
    "- 內部工作編號 917（`hailuo/{ff,clips}-dh-e917.json`、`colab/runs/e917/extras.json`、`colab/runs/e917-live/spec.json`，工作資料夾 `~/mokaair-work/videos/zhong-tian-qu-qi-e917-dh/`）；發布 slug `zhong-tian-qu-qi-e017-r2`。不放集數、不放片名卡；s01 接第 16 集 s42 的下一刻：竹筏撞上棧橋，許硯已經跳上岸。",
    "- 照第 16 集審稿後的寫法與第 13–15 集挑片的教訓一開始就照做：`OFFSCREEN_SPEECH = False`；背景寫在場的東西；長的東西（石木匠的青竹竿、二牛的扁擔、韓伯的竹杖）寫形狀；銅片與木槌寫小、跟手比大小；紙不入鏡（帳冊合著、素封面）；手與道具寫在第一格、每樣道具在主人那隻手；兩人接觸寫成第一格就已經的狀態（s04 秦霜的手已經在他手腕上、s13 他的手已經在阿令前臂上），不演『抓』。",
    "- **火（照 animation-preproduction 分級，火放在背景與邊上）**：院子用起火版 `set-xujia-yuan-huo-l1`（從 `set-xujia-yuan-l3`「只改一件事」：右牆外工棚的草頂著火冒黑煙、火光照在牆頭；屋在左、院門在後、柿子樹在中、井在前右），燒著的紙坊在**畫右土牆外**，每鏡火都在牆那邊、人都在院子這邊、臉被火光照橘；沒有人著火、沒有血。s11、s12、s16 在紙坊邊，不送場景圖，只有濃煙與後面的火光。皮膚只寫汗與一抹灰，不寫細小灰點（拍法 12）。",
    "- 唐小棠四句台詞都不露嘴、放錄音（nospeak）：s10、s17、s23、s31 從她背後拍，每鏡寫明「畫面裡唯一雙丸子頭粉緞帶的人」與固定在哪一側（沒有阿令的鏡另寫她是唯一的年輕女子）；spec.json 拿掉她三張臉部參考圖與身分句。她不說話的臉（s01、s18）用第 7 集的中性外貌句。秦霜 s04 那句從她背後拍（nospeak，spec 拿掉她的圖與身分句）。",
    "- **群眾**（第 14 集 s40、s42 一群人從門口湧進來最弱）：救火的十五人改成三、四個已經站好的村民，重建的十人改成兩對扛木頭、第一格已經在畫面裡的村民；都寫宋式短打、布包頭、小、只見側臉。一鏡最多三張有名字的臉。",
    "- 場景（2026-11-15 獨立審稿後，`writer-tools/e017-r2/review.md`）：柳溪口 `set-dukou-l2`（第 16 集重畫、已挑：棧橋空著、右岸最近那間草屋著火冒黑煙；s01）；院子 12 鏡（s02–s10、s13–s15）送**起火版** `set-xujia-yuan-huo-l1`（`live-action/screen-test-e017.py --r2`，種子 37023／37024，2 支，**還沒跑**；以 l3 為底只改一件事：右牆外工棚草頂著火、一團翻滾的黑煙、火光照在牆頭；審稿必改 1）；夜裡的新骨架 `set-zhifang-gujia-ye-l2` = 37020（s27–s35，正在立：兩根深色木柱一根長橫梁，s28 拉起第三根；必改 3 改字對圖）、天亮的新骨架 `set-zhifang-gujia-chen-l1` = 37019（s36–s40，四根淺色松柱、右前柱靠梯、左前燒黑的舊大木桶裝灰燼；必改 4）。燒毀的紙坊 s17–s26 **不送場景圖**（`set-zhifang-shao-l2` 兩個種子都不取；必改 15：燒毀的樣子正面寫在場景句最前面，spec 全部 drop_set）。篇章試鏡的 `set-zhifang-shao-l1`、`set-zhifang-gujia-ye-l1` 都不送。`prep917.sh` 在起火院子圖進 refs-live 之前停住。",
    "- 長鏡要買的秒數（BUY）：照 40 句錄音核過（`~/mokaair-work/videos/zhong-tian-qu-qi-e917-dh/audio`，見 `r2.py` 的 BUY 註解；faster-whisper 逐句聽寫，a10、a26、a30、a32、a33 重錄，第一次的檔在 `audio/take1/`）：s39 買 10 秒（系統兩句加心裡話 9.6 秒，稿子的長鏡）；s05（稿子的長鏡，6.4 秒）、s08、s25（韓伯說得慢，5.7、7.1 秒）、s26（交竹簾再說 5.6 秒）、s28（二牛數一二起 6.9 秒）、s35（心裡話 7.4 秒）買 8 秒；其餘 6 秒（容易笑場的石木匠、二牛都留 6 秒）。",
    "- **表上的「秒」欄是 lint 估法**，比錄音短；剪接以錄音長度＋0.5 秒為準。",
]
FOOT = [
    "- **參考圖**（`assets/refs-live/`）：許硯、阿令、秦霜、唐小棠（l1 交領）、二牛、韓伯、石木匠、小禾。場景 `set-dukou-l2`（第 16 集重畫、已挑）、`set-xujia-yuan-huo-l1`（起火版，`live-action/screen-test-e017.py --r2`，manifest `~/mokaair-work/videos/_series/zhong-tian-qu-qi/live-screen-test-e017/r2.json`，2 支，還沒跑；spec 的 swap_pictures 換掉 l3）、`set-zhifang-gujia-ye-l2` 37020、`set-zhifang-gujia-chen-l1` 37019（`live-action/screen-test-e017.py`，第一輪 6 支已跑、協調者已挑；燒毀版 `set-zhifang-shao-l2` 不取，s17–s26 不送場景圖）。阿令散髮 s11、s13、s17 只送定妝照，s12、s14 只送 angle-a（審稿必改 10）。",
    "- `gen-dh.mjs` 的 SET 加三行：`new timber frame at dawn` → `dh-set-zhifang-gujia-chen-t1`、`new timber frame` → `dh-set-zhifang-gujia-ye-t1`、`burnt paper workshop` → `dh-set-zhifang-shao-t1`（排在 `night work shed` 與 `work shed|workshop` 前）；第 910–916 集重建逐位元相同。`burnt paper workshop` 那行保留（讓 s17–s26 有場景句可 drop_set，竹簾的 willow 也不會被對到溪邊），spec 對 s17–s26 全部 drop_set，`prep917.sh` 另查沒有任何一支送 `set-zhifang-shao` 的圖。`build-r2.py` 的 EN 與 `cast.json` 不用改。",
    "- `colab/runs/e917/extras.json`（照 e915、e916：畫面不放字幕、空氣清澈那句——有煙的鏡由 spec 依場換成煙的句子，審稿必改 2；拿掉秦霜的柴刀、二牛的 empty-handed、小禾抱著的草兔子改塞在腰帶；石木匠與韓伯的造型句改宋式交領）與 `colab/runs/e917-live/spec.json`（`mkspec.py` 產生；種子 9171101／9171102）。",
    "- 免費準備：`prep917.sh`（`DRY=1 REFS=~/mokaair-work/videos/zhong-tian-qu-qi-e917-dh/runpod/refs-dh-e917 VIDEO_JSON=docs/videos/zhong-tian-qu-qi-e017-r2/video.json st1-ep.sh 917` → `pilot.py runpod/a/st1 runpod/live/st1 s01…s40` → `retake.py runpod/live/st1 runpod/live/d1 colab/runs/e917-live/spec.json` → `colab-jobs.json` 加 output_path → `preflight-prompts.py`），再加一步把 spec 的 swap_pictures 套進 colab-jobs.json、檢查沒有送 `set-zhifang-shao` 的圖）。草稿等起火院子圖挑好、進 refs-live 再拍。",
    "- 配樂：第一場急促鼓與弦，s11 阿令衝出一個重音、s14 叮、s15 頂塌一個大重音後收；第二場低弦與風聲，s20 燈籠一個重音、s23「賴三」第二個；第三場溫暖的鼓點與號子，s36 天亮一個上揚的重音，s38 紅框一個冷重音後收。音效表見 script.md〈音樂與音效〉。",
]

# Long shots: seconds to buy. Measured 2026-11-15 against the 40 recordings (~/mokaair-work/videos/zhong-tian-qu-qi-e917-dh/audio;
# ffprobe, silencedetect -35 dB / 0.3 s; e013's test: a shot holds (buy - 0.3) x 1.1 s of speech, half a second between lines;
# faster-whisper medium read every take back: five were re-recorded, a10 (這是 heard as 赤獅, 那一張), a26 (扶正 heard as 浮上),
# a30, a32 (只 heard as 去) and a33 (an added 啊 at the end); the first takes are in audio/take1/).
# 8 s go to: s05, the script's long shot (system a04 2.50 + thought a05 3.36 + 0.5 = 6.36 s); s08 (Elder Han's slow a08 5.68 s
# after the stamp of the staff); s25 (Elder Han's a23 7.08 s, 2.4 characters a second); s26 (a24 5.64 s after the hand-over of
# the mat); s28 (Erniu's counted a26 6.92 s, 一、二、起 with pauses); s35 (the thought a33 7.44 s).
# 10 s goes to s39, the script's long shot (system a37 2.12 + thought a38 3.40 + system a39 3.05 + 2 x 0.5 = 9.57 s).
# Every other line is 1.08-5.56 s and fits 6 s with half a second to spare (s20's a18 5.56 s, s34's a32 5.44 s the tightest).
# Review check (2026-11-15, after the independent review): a07 (Erniu's shout) has a median pitch of about 320 Hz against his
# 167-193 Hz elsewhere, but faster-whisper reads it word for word; two new takes (direction "低沉、不拉高") came out at 267 Hz
# (heard 推開／潑囉) and 320 Hz again, so the original is kept (scratchpad rec917/ holds the two takes); if it sounds shrill at
# the cut, lower it there the e914 PITCH way (rubberband, formant preserved, no lower than 0.8). a20-a22: 跛 is heard as 脖／箔
# by whisper, but the pitch of 跛 dips and rises in all three (a20 250->95->296, a21 340->211->271, a22 112->167 from Erniu's
# floor): the third tone bǒ; not re-recorded.
# Laugh-prone faces stay at 6: Carpenter Shi s02, s16, s19, s27, s36; Erniu s07, s24 (his cast voice "愛憨笑").
BUY = {"s05": 8, "s08": 8, "s25": 8, "s26": 8, "s28": 8, "s35": 8, "s39": 10}
