"""Episode 38 remake (r2): the writer spec for ../e001-r2/build-r2.py. Source: docs/videos/zhong-tian-qu-qi-e038-r2/script.md
(c01-c38; the CG-era r2 script), including its sections 「這版改了什麼」 and 「2026-11-06 審稿後的修改」, which override the tables.
Every line is the script's, word for word; only the staging changes. 40 shots: one per script shot (sNN = cNN) plus two splits
that keep one visible action and one voice per shot (s15b: Xu Yan's thought after the system line of c15, about 8.5 s of
speech with the pause, past what an 8 s clip holds with room to cut, the way e037's s16b was split; s27b: bible rule 41, the
leap over the barrier is never filmed: c27 is "charging the barrier" (s27) and "already landed on the gate side, dust" (s27b),
the jump itself left to the cut and the hoofbeats).
Bible: production/r2-bible-e031-e040.md (arc 4 〈旱年〉: rules 1-43, 〈場景〉 (the sickroom is Tang Xiaotang's room picture:
set-xujia-tangfang-l2 by night, its free dawn grade -chen-l1 by day), 〈接點〉 37->38 (the same dawn, the girl in bed the whole
scene, the damp cloth, Xu Yan kneeling at the bedside with lime on his robe) and 38->39, the props (the damp cloth, the basin, the
medicine bowl and the wooden spoon, Xiaohe's straw rabbit, the chestnut horse (rule 41), the riding whip, A-ling's long grey sash,
Qin Shuang's spear, the barrier of crossed stakes, the crossbows), people (the guard captain's first episode: duizhang-portrait-
l1, one face and one helmet the whole episode; A-ling's riding look: cuffs bound with cloth strips, leg wraps), 〈小角色〉 (the young
guard, the six crossbowmen, the torch bearer: backs, side-backs and far shapes) and 原版必修 (e038: the road by night, never
day; no milestone; the girl never vanishes from the bed)) and r2-bible-e011-e060.md (accounts: no affection change; Tang
Xiaotang 45, Qin Shuang 48, A-ling 32; the urgent task set here, done in e039).
The eighth episode of arc 4: day 176 in the Xu farmhouse's first bedroom (first light, midday, late afternoon, nightfall), the
night yard, then the second watch on the road to the county town, at its gate, and in its east street before the clinic.

Written from the start the way e037-r2/r2.py stands AFTER its independent review (writer-tools/e037-r2/{review.md,
review-independent.md}; colab/runs/e937-live/PREP.md §1-§7), the task file's lessons (e933-e937) and the owner's rules of
2026-11-21 to 23 (PR #2217, production/OWNER-CHECK-20261122.md):
- 37->38 from e937's cut (scratchpad e938prep/tail/sheet.jpg, e937-live.mp4 190-205.8 s): Xu Yan crouches on the ridge holding
  the limp girl, his right palm on her forehead (grey outer coat over the dusted robe; her lilac jacket, the straw rabbit at her
  sash). s01 is the same dawn in the sickroom: the girl already lying in the bed under the quilt with a folded damp cloth on her
  forehead, Xu Yan kneeling at the bedside with his right hand on her forehead (bible 〈接點〉 37->38).
- The pictures agree with the words: every place sentence follows the picture it sends; every crop is a free id made for this
  episode (live-action/free-e031-e040/{xujia_tangfang_e938.sh,roads_e938.sh}) or e031/e036/e037's crops of the night yard.
  The sickroom (set-xujia-tangfang-*): the plank door at the LEFT, the bed against the back wall under the small window with its
  pillow end at the RIGHT, the small table in the right front (two small paper packets on it are never written; its candle is
  "the one small flame on the table" by night and is not written by day). Morning -chen, midday -chen, late afternoon -xi (the
  free warm grade of -chen), night -l2.
- No "cinema camera" (e935 §8); no stubble word for Xu Yan; no mud (the lime on his robe is pale white powder, as e937 s35 on); no
  negated nouns (rule 18); long things never touch in the first frame (the spears, the whip, the crossbows); doors written swung
  back, ajar or shut every time they are in the picture (the bedroom door, the yard gate, the city gate's two leaves, the clinic's
  two leaves).
- One more person than written is common: every frame says "exactly N people" or "the only person" in the composition and
  mkspec.py writes the 'only' sentence again at the end of the prompt (task file 2026-11-20).
- No collective noun (rule 34): the six crossbowmen are six men in the same black armour, side-backs and far shapes, faces in the
  shadow of their helmets; the gate guards are the captain and one young guard. "exactly N people" everywhere.
- OFFSCREEN_SPEECH = False (rule 15); rule 31: a line to someone out of frame is written "toward someone out of sight beyond the
  left/right edge of the frame", that side set only, the speaker the only person; a look at a thing names the thing (the doorway,
  the gate, the torchlit wall). GAZE_REFINE puts the same direction into the refine text.
- No blue light (rule 11): the panel of s11 is the editor's; s11 and s15 are Xu Yan's close-ups with his lips shut.
- Tang Xiaotang (rules 3, 4, 20, 40): every line of hers is said from behind (s02, s04, s07, s16, s18); l1 cross-collared jacket,
  no outer coat, no stand-up collar (the script's t2 and 淡杏外衣 go), no abacus. She has NO front face this episode. Owner
  2026-11-22 (PR #2217): every back shot of hers also sends the hair reference; by day (s02, s04, s07) the owner's
  refs-live/tangxiaotang-back-shuangji-e929-w3.png, by night (s16, s18) its free night copy -w3-ye.png (e937 review 建議 1).
- Kneeling is framed to the knees (owner 2026-11-22): Xu Yan kneeling at the bedside (s01, s19) is framed full figure; s03 he sits
  on the edge of the bed, s06 he is a close-up without the kneel written.
- Qin Shuang (rule 5): her chopper is never written. She holds e037's one spear (bible 〈道具〉: "the shaft bare below the head"),
  sent with its prop picture prop-changqiang-l1 wherever it is in the frame (s09, s12, s16, s17; mkspec.py).
- The horse (rule 41): one chestnut-red horse, its mane and tail the same deep red-brown as its body (bible 〈道具〉, the picked
  prop-zaohongma-l1, bare-backed: the saddle is written in each shot), sent as the last picture wherever it is in the frame. Riding
  is seen side-on or from the side and behind, the rider from the waist up with the horse's head and neck, or in wides; the leap
  is never filmed (s27 / s27b); the tethered horse is written on its side of the frame and what it is tied to (s16 the tree, s30 the
  square stone post), never overlapping a person. The road: Liuxi at the RIGHT, the county town at the LEFT; outbound she always
  rides from right to left (s20, s21, s22, s27).
- Nothing hung (rule 33; bible 〈道具〉 items on the city wall, the clinic and the road): no notice board on the city wall, no
  signboard over the clinic door, no milestone or stone tablet by the road. The pictures have none (the city gate's plaque was
  painted out at the screen test).
- A-ling (rules 21, 22): no veil, no knife this episode; from s13 her riding look (sleeves bound at the wrists with grey cloth
  strips, dark leg wraps below the hem, her long grey sash), the riding whip in her sash from s16; outdoors a few strands blown
  loose from her hairpin, the bun and the hairpin as her picture.
- The guard captain (bible 〈人物〉, first episode): duizhang-portrait-l1 (black lamellar armour with red studs, a round iron
  helmet with cheek flaps and a small tuft of red horsehair on the crown), sent as a picture appended by mkspec.py (gen-dh.mjs and
  pilot.py know no live portrait for him; "duizhang" is a MINOR here and build-r2.py's EN gains "duizhang": "the guard captain"
  so his speaking sentence is written). His long spear s23-s26; his short knife s35-s37. Voice Iapetus (bible).
- The young guard (s24) is seen from behind and the side, his line a recording (MINOR "shoujun", Alnilam, not in the frame's
  characters); Doctor Bai is only a voice through the door (s31; cast.json Rasalgethi).

THE AXES (rules 29, 42: the pictures decide):
- The sickroom (set-xujia-tangfang-l2 / -chen-l1 / -xi-l1 and their crops -chuang, -men, -zhen): the plank door at the LEFT, the
  bed against the back wall under the small window, its pillow end at the RIGHT, the small table in the right front. People come in
  through the door at the left (Tang Xiaotang s02, Qin Shuang s09, A-ling s13) and face right toward the bed; Xu Yan kneels at the
  near side of the bed facing the back wall, or turns left toward the door. The script's 「床在畫面右後、屋門在畫面右」 is turned
  the picture's way.
- The night yard (set-xujia-yuan-ye-dong2-l1, e931's; -zhong, -wu): the house and its dark doorway at the LEFT, the yard gate in the
  MIDDLE of the back wall (its slatted plank leaf hinged on the right post, standing half swung back inward, the left half of the
  gateway clear: e037 review 必改 1), the bare tree just right of the gate, the round well in the front RIGHT. The horse stands
  tied to the bare tree; Tang Xiaotang and Qin Shuang stand before the house doorway at the left; A-ling rides out through the
  clear left half of the gateway, away from us. The script's 「院門在右、井在左前」 is turned the picture's way.
- The road by night (set-guandao-ye-l1's free crops -ce, -shu): a long line of tall dark poplars across the frame, the flat dark
  field before it, the moonlit night sky; the horse gallops from the right edge to the left, side-on.
- The city gate by night (set-chengmen-ye-l1's free crops -zha, -qiang, -men, -lu and the picture itself): the arched gate at the
  LEFT, its left leaf shut and its right leaf of studded planks standing half swung back outward, one torch fixed upright in an
  iron holder on each side of the arch, the long waist-high barrier of crossed wooden stakes along the foot of the wall to the
  right of the gate, the paving and the road back toward the RIGHT, the moon high at the right. The captain stands behind the
  barrier, facing right; A-ling comes from the right and goes in through the half-swung leaf. The script's 「門洞旁開著一扇小門」
  is the picture's half-swung leaf; its 「木柵橫在城門前的路上」 is the picture's barrier along the wall.
- The east street by night (set-yiguan-men-ye-l1 and its crops -men, -feng, -jie, -di): the stone-paved street running away to
  its far end at the LEFT, a long row of shut plank shopfronts under deep eaves on the RIGHT; the clinic is the nearest two-leaf
  plank door with two stone steps, a square stone hitching post at its left. A-ling stands on the top step facing right, her back
  to the street; the captain and the crossbowmen come up the street from its far end (left).

PLACES (gen-dh SET takes the FIRST pattern in its list order that matches the prompt):
- The sickroom: every LOC holds "first bedroom of the Xu farmhouse" -> dh-set-xujia-tangfang-t1 = pilot.py's newest
  set-xujia-tangfang (l2), which spec.json swaps for -chen-l1's crops, -xi-l1 and its crops, l2's crops.
- The yard: "night yard of the Xu farmhouse" -> dh-set-xujia-yuan-ye-t1 = set-xujia-yuan-ye-l2 (never sent), swapped for
  set-xujia-yuan-ye-dong2-l1, -zhong, -wu.
- The road, the city gate and the east street: the LOC carries " below the deep pool" (POOLMARK) only so gen-dh sends set-shentan
  ("official road", "city gate" and "clinic" would take set-guandao / set-chengmen / set-yiguan, which have no live picture under
  those ids: pilot.py would stop); mkspec.py takes the words out of every d1 prompt (e934-e937's way). Every later fix of
  s20-s38 must carry the same replacement.
Shared files: build-r2.py's EN gains "duizhang": "the guard captain" (he speaks on screen for the first time; a new key only, every
older episode rebuilds byte for byte). gen-dh.mjs, pilot.py, cast.json untouched. The d1 prep (colab/runs/e938/extras.json,
colab/runs/e938-live/{mkspec.py,spec.json,PREP.md}, the scratchpad's tools/prep938.sh, rec938-slow.sh and e938d1.sh) was
written 2026-11-23.
"""
EP = 938  # internal working number; the published slug is zhong-tian-qu-qi-e038-r2
SLUG = "zhong-tian-qu-qi-e038-r2"
EP_TITLE = "馬給我，她一騎躍過城門木柵（重製版 r2）"
OUTLINE_SECONDS = 186  # script.md: about 186 s, 38 shots (19 + 9 + 10)
TARGET_MINUTES = [3, 4]
TITLE = "「馬給我。」小禾燒到說胡話，阿令一騎闖宵禁、躍過城門木柵，弩箭對準她的背｜種田娶妻打天下 第38集（重製版）"
DESCRIPTION = "石灰陣那一夜的清晨，小禾燒得通紅。中午退了一點，傍晚又燒上來，她在夢裡喊：哥哥別下水。村裡沒有大夫，縣城因為流寇宵禁，馬只有一匹，秦霜得守村子。系統下了緊急任務：天亮前，小禾退燒。阿令開口：馬給我。許硯什麼都沒問——我信妳。她一翻身就上了馬，秦霜看出那是騎兵上馬的法子。月夜官道一騎狂奔；城門守軍喊宵禁、笑她女人騎什麼馬，她退馬三步，一夾馬腹躍過木柵。東街醫館，她拍門喊白大夫，身後一排弩對準她的背，隊長舉起手：放——。《種田娶妻打天下》第 38 集（重製版）。"
THUMB = ("馬給我", "s27")
CHARACTERS = ["xuyan", "tangxiaotang", "xiaohe", "qinshuang", "aling", "duizhang", "shoujun", "baidaifu", "xitong"]
MINOR = {
    "duizhang": {"id": "duizhang", "name": "守軍隊長",
                 "appearance": "East Asian man of about forty-five, a square face and a short black beard, hard steady eyes, black iron lamellar armour with small red studs over a dark undercoat, a round iron helmet with cheek flaps that leaves his whole face bare and a small tuft of red horsehair on its crown",
                 "voice": {"provider": "gemini", "name": "Iapetus", "style": "標準國語，咬字清楚，台北人平常說話的語調；四十五歲的縣城守軍隊長，男聲、低沉粗硬、發號施令，吼的時候一個字一個字砸出來"}},
    "shoujun": {"id": "shoujun", "name": "年輕守軍",
                "appearance": "East Asian young man of about twenty, in black iron lamellar armour and a plain iron helmet; seen only from behind and the side",
                "voice": {"provider": "gemini", "name": "Alnilam", "style": "標準國語，咬字清楚，台北人平常說話的語調；二十歲的年輕守軍，男聲、輕佻、起鬨，笑得很賤"}},
}
MUSIC = "one cue per scene: a very soft piano in a grey morning sickroom, turning to low dark strings at a feverish whisper in the orange late afternoon, one hard accent on an urgent task, one accent as a rider swings up onto a horse in a moonlit yard and urgent drums after it, then a single lonely erhu by one small flame; then fast galloping drums on a moonlit road of poplars, one huge accent on a charge at a barrier by a torchlit city gate, the drums running on; then urgent drums in a dark stone street, turning to taut rising strings as crossbows are raised, held at the highest note and cut off unresolved; ancient Chinese rural drama, no vocals"

# Places.
ROOM = "In the first bedroom of the Xu farmhouse"
R_MORN = f"{ROOM} at first light on the morning after the battle"
R_NOON = f"{ROOM} at midday"
R_EVE = f"{ROOM} in the late afternoon"
R_NIGHT = f"{ROOM} at nightfall"
MORN = "cold grey-white morning light from the small window, the room grey and still"
NOON = "flat bright white daylight from the small window, the room pale and still"
EVE = "low warm orange light of the late afternoon from the small window, the room dim and warm"
RNIGHT = "the one small flame on the table the only warm light, the corners of the room deep in shadow, the small window dark blue"
ROOMLAY = ("the plank door at the far left standing shut, rough cracked plaster walls, a wooden bed against the back wall under the small "
           "window with its pillow end at the right and a pink quilted cover on it, a small wooden table in the right front")  # -chen / -xi / l2
N1 = "In the night yard of the Xu farmhouse after nightfall"
NIGHT = "cool pale moonlight from above, the yard dark and still, a faint warm glow from the house doorway at the left"
YARD = ("the farmhouse on the left with its dark doorway at the far left and split firewood stacked against its front, the yard gate "
        "under its small tiled roof in the middle of the back wall with its slatted plank leaf hinged on the right gate post and standing "
        "half swung back inward, the left half of the gateway clear, a bare tree just right of the gate, the low earth-and-stone back "
        "wall running from the gate to the right edge, the round stone well with its wooden windlass in the front right, a wooden "
        "bucket in the middle of the yard, dark fields and far dark hills beyond the wall")  # -ye-dong2-l1 (e937 s09b)
POOLMARK = " below the deep pool"  # mkspec.py takes it out of every road, gate and street shot in d1 (gen-dh's SET needs "deep pool")
G1 = f"On the wide dirt road to the county town{POOLMARK} in the second watch of the same night"
GNIGHT = "cold blue moonlight, the deep blue night sky, the long shadows of the poplars across the field"
C1 = f"Before the gate of the county town{POOLMARK} in the second watch of the same night"
CNIGHT = "cold blue moonlight from the moon high at the right, the two torches by the gate the only warm light"
GATE = ("the arched gate in the grey brick city wall at the left, its left leaf of dark studded planks shut and its right leaf of studded "
        "planks standing half swung back outward, one torch fixed upright in an iron holder on each side of the arch, nobody holding "
        "them, a long waist-high barrier of crossed wooden stakes along the foot of the wall to the right of the gate, the stone "
        "paving before the gate and the road running back along the wall toward the right")  # set-chengmen-ye-l1
E1 = f"In the east street of the county town{POOLMARK} a little later in the same night"
ENIGHT = "cold blue moonlight on the stone paving, the deep eaves in black shadow, every shopfront shut and dark"
STREET = ("the stone-paved street running away to its far end at the left, a long row of shut plank shopfronts under deep tiled eaves "
          "along the right, the nearest one a two-leaf plank door with two stone steps before it and a square stone hitching post at "
          "its left")  # set-yiguan-men-ye-l1
LOC = {
    "rm_c": f"{R_MORN}, at the bedside; {MORN}",
    "rm_d": f"{R_MORN}, by the plank door; {MORN}",
    "rn_c": f"{R_NOON}, at the bedside; {NOON}",
    "re_c": f"{R_EVE}, at the bedside; {EVE}",
    "re_d": f"{R_EVE}, by the plank door; {EVE}",
    "rx_c": f"{R_NIGHT}, at the bedside; {RNIGHT}",
    "rx_d": f"{R_NIGHT}, by the plank door; {RNIGHT}",
    "ny": f"{N1}: the yard exactly as in the picture: {YARD}; {NIGHT}",
    "ny_g": f"{N1}, inside the yard gate; {NIGHT}",
    "ny_h": f"{N1}, before the dark house doorway; {NIGHT}",
    "g": f"{G1}; {GNIGHT}",
    "c": f"{C1}: the place exactly as in the picture: {GATE}; {CNIGHT}",
    "c_b": f"{C1}, at the barrier of crossed stakes; {CNIGHT}",
    "c_g": f"{C1}, by the half-swung gate leaf; {CNIGHT}",
    "c_r": f"{C1}, on the road along the wall; {CNIGHT}",
    "e": f"{E1}: the street exactly as in the picture: {STREET}; {ENIGHT}",
    "e_d": f"{E1}, at the two-leaf plank door; {ENIGHT}",
    "e_s": f"{E1}, in the street; {ENIGHT}",
    "e_x": f"{E1}; {ENIGHT}",  # the inserts s31, s34: mkspec.py leaves only "Insert close-up" (rule 35)
}
LIGHT = {
    "morn": "the grey morning light stays unchanged",
    "noon": "the white midday light stays unchanged",
    "eve": "the warm orange late-afternoon light stays unchanged",
    "lamp": "the small flame and the shadows stay unchanged",
    "night": "the cool moonlight stays unchanged",
}
# bible rule 15: no "<X> speaks off screen" / "the system voice speaks off screen".
OFFSCREEN_SPEECH = False

# Repeated wording (each prop is one object, written the same way every time).
XU_COAT = ("Xu Yan, in his faded blue-grey scholar's robe patched at one elbow, pale white lime powder dusted over the lower half of the "
           "robe, with an old grey cloth outer coat worn loose over his shoulders")  # bible 〈人物〉: the lime to e040 s1, the coat by night and this day
XIAOHE_BED = ("little Xiaohe, eight years old, lying on her back in the bed under the pink quilted cover drawn up to her chest, her whole face "
              "flushed deep red with fever, strands of her hair stuck to her forehead, her lips dry and cracked, one folded damp white cloth "
              "across her forehead, a small woven straw rabbit lying beside her pillow")
XIAOHE_BED_SHORT = "little Xiaohe, eight years old, lying in the bed under the pink quilted cover, her face flushed deep red, a folded damp white cloth on her forehead"
CLOTH = "one folded damp white cloth"
BASIN = "one shallow wooden basin of water"
BOWL = "one coarse clay medicine bowl of dark steaming broth"
SPOON = "one plain wooden spoon"
QIN = ("Qin Shuang, in her fitted dark brown cross-collared short jacket cinched with a wide plain leather belt, fitted black "
       "trousers and leather boots, her sleek high ponytail tied with black cord")  # rule 5: nothing in her belt
SPEAR = "one long spear: a plain wooden shaft taller than she is, a small plain iron spearhead, the shaft bare below the head"  # e037's, bible 〈道具〉
ALING = ("A-ling, in her plain grey-white cotton dress tailored close at the waist with a long grey cloth sash, its long sleeves down "
         "over both wrists, her long black hair pinned up with one plain wooden hairpin")
ALING_R = ("A-ling, in her plain grey-white cotton dress tailored close at the waist with a long grey cloth sash, its long sleeves bound "
           "tight at both wrists with strips of grey cloth, dark cloth leg wraps below the hem of the dress, her long black hair pinned "
           "up with one plain wooden hairpin")  # her riding look (bible 〈人物〉, s13 on)
WISPS = "a few strands of her hair blown loose from the hairpin"
WHIP = "one short riding whip with a plain bamboo handle and a plaited leather lash"
WHIP_SASH = f"{WHIP} tucked into her sash"
HORSE = ("one chestnut-red horse, its mane and tail the same deep red-brown as its body, a plain brown leather bridle and an old plain "
         "brown leather saddle on a folded dark cloth")  # rule 41, prop-zaohongma-l1 (bare-backed: the saddle written here)
CAPTAIN = ("the guard captain, a middle-aged man with a square face and a short black beard, in black iron lamellar armour with small red "
           "studs, a round iron helmet with cheek flaps that leaves his whole face bare and a small tuft of red horsehair on its crown")
CAP_SPEAR = "one long spear: a plain dark wooden shaft taller than he is, a small plain iron spearhead, the shaft bare below the head"
CAP_KNIFE = "one short plain single-edged knife with a dark wooden grip"
GUARD = "one young guard in black iron lamellar armour and a plain iron helmet"
XBOW = "one plain wooden crossbow held level in both hands"
XBOWMEN = ("six crossbowmen in the same black iron lamellar armour and plain iron helmets, their faces in the shadow of their helmets, "
           f"each with {XBOW}")
TORCHMAN = "one more guard in black armour holding up one burning torch in his right hand"
HANDS = "their hands hold only what is described here"
SILENT_HE = "He says nothing in this shot: his lips stay pressed together from the first frame to the last, his jaw still, no talking, no mouthing words"
NOBODY = "Throughout the shot the set layout stays as it is. The pictures fix the place and the objects only, never the mood. "
# rule 40 (e031 / e033 / e935-e937 TBACK): Tang Xiaotang from behind, her l1 costume (rule 4), no outer coat
TBACK = ("one young woman seen only from behind, appearing only once: the back of her head with every strand of her black hair "
         "combed smooth and gathered up into just two round buns set high on her head, one bun on each side, one short pink "
         "silk ribbon wrapped around each bun, the nape of her neck bare and clear above a pink inner collar, and her light "
         "peach-pink silk shoulders; the back of her head facing straight away from us the whole time, her head still, her ear "
         "the furthest round her head we ever see")
TBACK_SMALL = ("one young woman seen only from behind, appearing only once, her black hair in just two round buns set high on her "
               "head tied with short pink silk ribbons, in a light peach-pink silk jacket and skirt")
HEADSTILL = "the young woman with the two high round buns keeps her head still, facing straight away from us, the back of her head toward us the whole shot"
XU_EDGE = ("at the right edge of the frame, cut by it, soft and out of focus, only one shoulder and upper arm of a man in an old grey "
           "cloth outer coat, toward us the whole shot")
ALING_EDGE = ("at the left edge of the frame, cut by it, soft and out of focus, only the back of a young woman's head with black hair "
              "pinned up with one plain wooden hairpin and one grey-white shoulder, toward us the whole shot")
SIDE_WALL = "the rough cracked plaster wall"
SIDE_DOOR = "the shut plank door and the cracked plaster wall"


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
    # ---- scene 1: the first bedroom of the Xu farmhouse, first light to nightfall, and the night yard (37->38).
    dict(chapter="許家屋內與院子，清晨到入夜", loc="rm_c", cam="Wide shot, slow push in", chars=["xuyan", "xiaohe"], night="morn",
         comp=f"wide shot at the bedside, {BASIN} on the floor soft in the lower foreground: in the bed against the back wall, {XIAOHE_BED}, her eyes shut, her brows drawn in pain, her lips closed; kneeling on the floor at the near side of the bed, {XU_COAT}, framed full figure with both knees on the floor, his right hand already resting on the cloth on her forehead from the first frame, his face lowered three-quarter to screen right toward her, never the lens; hoarse and worried, not smiling: brows knotted, eyes red-rimmed, lips moving low between words; behind them, soft, the plaster wall under the small window; {HANDS}; exactly two people",
         lines=[("xuyan", "濕布換了三回，還是燙得嚇人。", "啞，擔心")],
         motion=f"Xu Yan lifts the cloth off her forehead, dips it into the basin, wrings it out and lays it back across her forehead as he speaks; {quiet('little Xiaohe', 'her')}",
         zh="全景（全身：**跪姿拍到膝蓋**，站主 2026-11-22）、慢推（送本集免費做的 `set-xujia-tangfang-chen-chuang-l1`：清晨灰白光裡的床、粉被、枕頭在右、桌角）：**接點 37→38（照第 37 集成片 `e937-live.mp4` 最後 15 秒）**：同一個清晨，病房（聖經第 42 條：唐小棠房間的圖，稿子不說是誰的房間）：小禾已經躺在床上蓋被（**整場床上一直有她**，原版必修）、滿臉通紅、髮絲黏額、嘴唇乾裂、額頭一塊摺好的濕布（拍法 12：不寫汗珠細點），草兔子在枕邊；許硯（舊灰外衣、袍子下半截石灰白粉，接第 37 集）跪在床前、右手第一格已經按在她額頭的濕布上；把濕布拿起、在水盆裡擰一擰、重新蓋上（一個動作的連續），啞著嗓子說；小禾嘴閉著。前景地上的水盆（稿子『前景是床頭的水盆』）"),
    dict(loc="rm_d", cam="Medium shot from behind, slow push in", chars=["tangxiaotang", "xuyan"], nospeak=["tangxiaotang"], night="morn",
         comp=alone(f"{BOWL} already held before her in both hands from the first frame, steam rising from it; one step beyond her in the left third of the frame, by the foot of the bed, {XU_COAT}, already risen to his feet from the first frame, framed from the waist up, his face three-quarter to screen right toward her, never the lens, his lips closed, not smiling: brows drawn, eyes tired; behind them, soft, the bed under the small window and the plaster wall; she stays in the middle of the frame the whole shot; {HANDS}; exactly two people, the young woman in the middle seen only from behind",
                    "just inside the plank door at the left, walking in toward the bed,"),
         lines=[("tangxiaotang", "藥熬好了，韓伯說這方子退熱最快。", "急")],
         motion=f"the bowl tips as she hurries two steps on, and her fingers jerk off its hot rim and close round it again, only her arms moving, and Xu Yan reaches out both hands toward the bowl; {quiet('Xu Yan')}; {HEADSTILL}",
         zh="中景（從背後）、慢推（送本集免費做的 `set-xujia-tangfang-chen-men-l1`：左邊的木板門、裂紋土牆、床尾）：**唐小棠從背後拍**（拍法 3、40；l1 交領短襦，**不寫 t2 高立領、不寫淡杏外衣**；不點名她的臉、拿掉她三張臉部圖，mkspec 加送站主的雙丸子背影參考圖（白天用原檔））：她第一格已經捧著冒熱氣的陶藥碗、從左邊的門走進來（聖經第 42 條：門在左），快走兩步、碗一晃、手指被燙得一甩又捧住（一個動作；稿子 c02）；許硯第一格已經從床邊站起、在她前方畫左三分之一，伸兩手要接碗、嘴閉著；她的話是錄音、頭不動（`nospeak`）。稿子『跟拍往左』改慢推"),
    dict(loc="rm_c", cam="Close-up, slow push in", chars=["xuyan", "xiaohe"], night="morn",
         comp=f"close-up at the bedside: {XU_COAT}, already sitting on the edge of the bed beside her from the first frame, framed from the chest up, {BOWL} in his left hand and {SPOON} in his right, his face lowered three-quarter to screen right toward her, never the lens; tender and tired, not smiling: brows soft, lips moving gently between words; along the bottom of the frame, {XIAOHE_BED_SHORT}, her head already lifted a little on his right forearm from the first frame, her eyes half shut, her lips closed; behind him, soft, only the small window glowing grey-white and the dark wooden bedpost; {HANDS}; exactly two people",
         lines=[("xuyan", "小禾，乖，喝一口就不燙了。", "放軟")],
         motion=f"Xu Yan blows on the spoonful, holds it to her lips and tips it in, and little Xiaohe frowns and swallows; {quiet('little Xiaohe', 'her')}",
         zh="近景、慢推（送本集免費做的 `set-xujia-tangfang-chen-zhen-l1`：枕頭那頭、床頭柱、桌角；稿子『身後只有窗紙與床柱』）：許硯第一格已經坐在床沿（不寫跪：近景看不到膝蓋，站主跪姿規則）、左手藥碗、右手木湯匙，右前臂第一格已經托著她的頭；吹涼、餵進去，她皺眉嚥下（一個動作），放軟聲音說；畫面下緣是小禾通紅的臉、嘴閉著"),
    dict(loc="rn_c", cam="Medium shot from behind, slow push in", chars=["tangxiaotang", "xuyan", "xiaohe"], nospeak=["tangxiaotang"], night="noon",
         comp=alone(f"beyond her in the bed under the small window, {XIAOHE_BED_SHORT}, asleep, her breathing easier, her lips closed; at the right, by the pillow end of the bed, {XU_COAT}, standing leaning one shoulder against the dark wooden bedpost, framed from the waist up, his face three-quarter to screen left toward the young woman, never the lens, his lips closed, not smiling: tired, brows easing; the empty clay medicine bowl and {SPOON} on the small table at the right; she stays in the middle of the frame the whole shot; {HANDS}; exactly three people, the young woman in the middle seen only from behind",
                    "sitting on the near edge of the bed,", frame="framed from the waist up"),
         lines=[("tangxiaotang", "中午燒退了一點，她總算睡著了。", "小聲，鬆一口氣")],
         motion=f"she lays her flat right hand on the girl's forehead for a moment and draws it back, her shoulders sinking with relief, only her arm moving, and Xu Yan gives one slow nod; {quiet('Xu Yan and little Xiaohe', 'their', plural=True)}; {HEADSTILL}",
         zh="中景（從背後）、慢推（送 `-chen-chuang-l1`：正午寫在光，窗紙一片白亮）：唐小棠背影坐在床沿、在畫面正中（拍法 40；她的話是錄音、頭不動，稿子『轉頭看許硯』不拍），伸手摸一下小禾額頭、收回、肩膀一鬆（一個動作）；小禾睡著、呼吸平一點、嘴閉著（床上一直有她）；許硯在畫右靠著床柱、點一下頭、嘴閉著；空藥碗與湯匙放在右邊小桌上（稿子『放在床頭』照圖寫小桌）"),
    dict(loc="re_c", cam="Close-up, slow push in", chars=["xiaohe"], night="eve",
         comp=f"close-up of {XIAOHE_BED}, framed from the chin up on the pillow with a little space above her head, her eyes shut tight, her face redder than the morning, her head already turned to screen left on the pillow from the first frame, never the lens; she is the only person in the frame; delirious and frightened, close to tears, not smiling: brows pinched, lips trembling and moving between mumbled words; behind her, soft, only the pink pillow, the dark wooden bed head and the plaster wall in the warm orange light; {HANDS}",
         lines=[("xiaohe", "哥哥……別下水……哥哥別下水……", "說胡話，含糊，哭腔")],
         motion="little Xiaohe tosses her head slowly from side to side on the pillow and her small fingers clutch at the edge of the quilt as she mumbles",
         zh="近景（下巴以上）、慢推（送本集免費做的 `set-xujia-tangfang-xi-zhen-l1`：傍晚暖橘光裡的枕頭那頭；`-xi` 是 `-chen` 免費調成傍晚的斜陽橘光，稿子『身後只有被橘光照著的窗紙』）：傍晚：小禾臉比早上更紅、髮絲黏額、眼睛閉緊，頭在枕上左右搖、手指抓緊被角（一個動作），含糊地說胡話（聖經〈伏筆〉：『哥哥別下水』，落水真相；許硯不說破）"),
    dict(loc="re_c", cam="Close-up, slow push in", chars=["xuyan"], night="eve",
         comp=f"close-up of {XU_COAT}, at the bedside, framed from the chest up with space above his head, his right hand already raised halfway toward her forehead from the first frame, frozen in mid-air at the bottom edge, his face lowered three-quarter to screen right, his eyes on the pillow below the right edge of the frame, never the lens; he is the only person in the frame; stricken, not smiling: brows drawn, eyes fixed and wide, lips pressed shut; behind him, soft, only the dark wooden bedpost and the plaster wall in the warm orange light; {HANDS}",
         lines=[("xuyan", "她夢裡還在喊我別下水……那天，她也在河邊。", "心裡話，錄得近、輕", "inner")],
         motion=f"Xu Yan's raised hand stops dead in the air and slowly draws back, his eyes never leaving the pillow; {SILENT_HE}",
         zh="近景、慢推（送 `-xi-chuang-l1`；稿子『身後只有床柱與油燈的暖光』：圖上傍晚燈還沒點，寫暖橘光）：許硯伸向她額頭的手第一格已經停在半空，停住、慢慢收回（一個動作），眼睛盯著畫右下外的枕頭（看的是東西，拍法 31）；心裡話是錄音、**全程嘴閉著**、不笑（聖經〈伏筆〉：不說破，只留『那天，她也在河邊』）"),
    dict(loc="re_c", cam="Medium shot from behind, slow push in", chars=["tangxiaotang", "xiaohe"], nospeak=["tangxiaotang"], night="eve",
         comp=alone(f"beyond her in the bed, {XIAOHE_BED_SHORT}, her eyes shut, her lips closed; behind them, soft, the plaster wall under the small window in the warm orange light; she stays in the middle of the frame the whole shot; {HANDS}; exactly two people, the young woman in the middle seen only from behind",
                    "sitting on the near edge of the bed,"),
         lines=[("tangxiaotang", "比早上還燙，這藥已經壓不住了。", "聲音發抖，快哭了")],
         motion=f"she touches the girl's forehead with her flat right hand and snatches the hand back at once, pressing it to her own chest, only her arm moving; {quiet('little Xiaohe', 'her')}; {HEADSTILL}",
         zh="中景（從背後）、慢推（送 `-xi-chuang-l1`）：稿子 c07 是唐小棠下巴以上近景說話；真人版從背後拍（拍法 3、40），她坐在床沿、在畫面正中，一摸小禾額頭就縮回手、按在自己胸前（一個動作；『咬住嘴唇』從背後看不到，交給錄音的抖），錄音、頭不動；小禾在床上、嘴閉著"),
    dict(loc="re_c", cam="Medium shot, slow push in", chars=["xuyan", "xiaohe"], night="eve",
         comp=f"medium shot at the bedside, the dark wooden bedpost soft in the right foreground: {XU_COAT}, already standing by the bed from the first frame with the old grey outer coat already pulled off his shoulders and spread wide in both hands, framed from the waist up, his face lowered three-quarter to screen right toward the bed, never the lens; desperate, not smiling: jaw clenched, brows knotted, lips moving hard between words; in the bed below him, {XIAOHE_BED_SHORT}, her eyes shut, her lips closed; behind them, soft, the plaster wall in the warm orange light; {HANDS}; exactly two people",
         lines=[("xuyan", "村裡沒有大夫，我背她進城，現在就走。", "咬牙")],
         motion=f"Xu Yan leans low over the bed and spreads the coat over the girl to wrap her in it as he speaks; {quiet('little Xiaohe', 'her')}",
         zh="中景、慢推（送 `-xi-chuang-l1`；前景床柱）：許硯第一格已經站在床邊、外衣已經扯下來兩手撐開，彎腰把外衣蓋到小禾身上要裹她（一個動作；稿子『扯下外衣、彎腰要抱』），咬牙說；唐小棠不入鏡（不寫，拍法 31）"),
    dict(loc="re_d", cam="Medium shot, slow push in", chars=["qinshuang", "xuyan"], night="eve",
         comp=f"medium shot by the plank door at the left: the plank door standing swung back inward against the wall, the dusky yard beyond the doorway; at the left, just inside the doorway, {QIN}, already in from the first frame, out of breath, framed from the waist up, her right hand gripping the door frame, {SPEAR} already leaning upright against the door frame beside her, well apart from her, her face three-quarter to screen right toward him, never the lens; urgent and blunt, not smiling: brows drawn, eyes hard, lips moving fast between breaths; at the right, {XU_COAT}, standing, the old grey outer coat bundled over his left arm, framed from the waist up, his face three-quarter to screen left toward her, his lips closed, not smiling, never the lens; behind them, soft, the cracked plaster wall in the warm orange light; {HANDS}; exactly two people",
         lines=[("qinshuang", "縣城宵禁了。昨夜流寇下山，天一黑城門就關。", "喘，直說")],
         motion=f"Qin Shuang thrusts her flat left hand out toward his chest to stop him as she speaks between breaths, and Xu Yan stops short; {quiet('Xu Yan')}",
         zh="中景、慢推（送 `-xi-men-l1`：左邊的木板門與裂紋土牆）：秦霜從左邊的門進來（聖經第 42 條；門寫明往內推開靠牆），第一格已經在門內、喘、右手扶門框、長槍已經靠在門框旁（跟她分開，長桿第一格分開；加送 `prop-changqiang-l1`；**柴刀不寫**，拍法 5；稿子『臉上沾灰』不寫細點，拍法 12），左手平掌往他胸前一攔（一個動作），喘著直說；許硯在右、外衣搭在左臂、停住、嘴閉著"),
    dict(loc="re_c", cam="Close-up, slow push in", chars=["xuyan"], night="eve",
         comp=f"close-up of {XU_COAT}, standing in the room, framed from the chest up with space above his head, the old grey outer coat already back over his shoulders from the first frame, his face three-quarter to screen left {off('left', SIDE_DOOR)}; hard and stubborn, not smiling: jaw clenched, eyes hard, lips moving tight between words; behind him, soft, only the plaster wall and the edge of the small window in the warm orange light; {HANDS}",
         lines=[("xuyan", "城門關了也得去，騎馬半個時辰就到。", "咬牙")],
         motion="Xu Yan's right hand closes into a hard fist at his side and he lifts his chin as he speaks",
         zh="近景、慢推（送 `-xi-chuang-l1`；稿子『身後只有屋門與門外的暮色』：他面向左邊的門，身後是窗那面牆）：許硯外衣第一格已經披回肩上，右手握成拳、抬起下巴（一個動作），朝畫左外看不到的人（秦霜，不點名、不寫人，拍法 31）咬牙說（答 s09）；不笑"),
    dict(loc="re_c", cam="Close-up, slow push in", chars=["xuyan"], night="eve",
         comp=f"close-up of {XU_COAT}, standing in the room, framed from the chest up with space above his head, his face three-quarter to screen left, his eyes already lifted to the empty air before him from the first frame, never the lens; he is the only person in the frame; grim, not smiling: brows drawn, lips pressed shut; behind him, soft, only the plaster wall in the warm orange light; {HANDS}",
         lines=[("xitong", "叮。緊急任務：天亮前，小禾退燒。", "冷，宣布")],
         panel=[("緊急任務：天亮前，小禾退燒", "task")],
         motion=f"Xu Yan's clenched fist slowly loosens at his side; {SILENT_HE}",
         zh="近景、慢推（送 `-xi-zhen-l1`；跟 s10 不同背景）：許硯眼睛第一格已經抬起、拳頭慢慢鬆開（一個動作）；系統是錄音、**全程嘴閉著**；**不寫淡藍光**（拍法 11）；面板『緊急任務：天亮前，小禾退燒』剪接時疊（紅框照聖經〈系統〉）、跟系統念的一字不差"),
    dict(loc="rx_d", cam="Medium shot over the shoulder, slow push in", chars=["qinshuang"], night="lamp",
         comp=f"medium shot over a shoulder: {XU_EDGE}; beyond it, in the left half of the frame, {QIN}, standing just inside the plank door, which stands swung back inward against the wall, {SPEAR} upright in her right hand, its butt on the floor, framed from the waist up, her face three-quarter to screen right toward the man at the right edge, never the lens; firm and grim, not smiling: brows level, jaw set, lips moving short and plain between words; beyond her, through the doorway, soft and out of focus, a young woman in grey-white standing just outside the threshold in the dark, only her head and shoulders, still, listening, her lips closed; {HANDS}; exactly three people, the one at the edge seen only in part, the young woman beyond the doorway soft",
         lines=[("qinshuang", "馬只有一匹。我不能走，山上還有散掉的流寇。", "直說，不容商量")],
         motion="Qin Shuang glances back once over her shoulder at the dark doorway and turns back, pressing her free left fist against the door frame as she speaks",
         zh="過肩中景、慢推（送本集免費做的 `set-xujia-tangfang-men-l1`：夜裡的門與牆；入夜：桌上那一朵火是唯一的暖光）：前景右是虛焦的舊灰外衣肩（許硯，不點名、不送圖，拍法 2）；秦霜在畫左門內、右手長槍直立（加送長槍道具圖），回頭看一眼門外、轉回來、左拳在門框上一按（一個動作），直說；**門外阿令停在門檻外聽**（2026-11-06 審稿補的：虛焦、只到肩、不點名、不送圖），c13『← 因為 c12』才成立"),
    dict(loc="rx_d", cam="Medium shot, slow push in", chars=["aling"], night="lamp",
         comp=f"medium shot in the room, the one small flame on the table soft in the lower right foreground: {ALING_R}, already stepped in through the plank door from the first frame and stopped in the middle of the room, framed from the knees up, her left cuff bound with a strip of grey cloth, the end of the strip in her right hand, her face three-quarter to screen right {off('right', 'the dark wooden bed head and the plaster wall', he='she')}; cold and steady, not smiling: eyes level, brows still, lips moving evenly between words; behind her, soft, the shut plank door and the cracked plaster wall in the warm small light; {HANDS}",
         lines=[("aling", "馬給我。我知道路，天亮前帶大夫回來。", "冷，很穩")],
         motion="A-ling gives the grey cloth strip round her left cuff one last hard pull and lets both hands fall to her sides as she speaks",
         zh="中景（膝以上：綁腿要在框裡）、慢推（送 `-men-l1`；前景右下桌上那一朵火：稿子『前景是木桌上的油燈』照圖寫）：阿令從左邊的門進來（第一格已經停在屋中間；送 `aling-portrait-l1`，**沒戴鐵鐐**，稿子要先畫的 `aling-portrait-t2` 就是它），**騎馬的樣子**：袖口用灰布條紮緊、裙下綁腿、灰布長腰帶（聖經〈人物〉第 38–39 集）；把左袖口的布條最後一拉、兩手放下（一個動作；稿子『用牙咬緊布條打結』：牙咬著說不了話，改用手拉），朝畫右外看不到的人（許硯，不點名）冷而穩地說（← 因為 s12）"),
    dict(loc="rx_c", cam="Medium close-up over the shoulder, slow push in", chars=["xuyan"], night="lamp",
         comp=f"medium close-up over a shoulder: {ALING_EDGE}; beyond it, in the right half of the frame, {XU_COAT}, standing, framed from the waist up, {WHIP} already held out level in his right hand from the first frame toward the young woman at the left edge, its lash trailing down, his face three-quarter to screen left toward her, never the lens; steady, not smiling: brows level, eyes calm, lips moving evenly between words; behind him, soft, the dark wooden bed head, the plaster wall and the one small flame on the table; {HANDS}; exactly two people, the one at the edge seen only from behind",
         lines=[("xuyan", "我不問妳會不會騎。我信妳，馬給妳。", "很穩")],
         motion="Xu Yan presses the bamboo handle of the whip into the young woman's hand at the left edge and lets go as he speaks",
         zh="過肩中近景、慢推（送本集免費做的 `set-xujia-tangfang-zhen-l1`：床頭、牆、桌上的火）：前景左是虛焦的阿令後腦與木簪、灰白肩（不點名、不送圖，拍法 2）；許硯第一格已經把馬鞭（一根，竹柄皮鞭，2026-11-06 審稿改的：不是韁繩）平舉在右手，塞進前景的手、放手（一個動作；『從釘子上取下』在第一格完成），很穩地說（答 s13：好感 +12 的原因在第 39 集回收）"),
    dict(loc="rx_c", cam="Close-up, slow push in", chars=["xuyan"], night="lamp",
         comp=f"close-up of {XU_COAT}, standing in the room, framed from the chest up with space above his head, his face three-quarter to screen left, his eyes on the dark doorway beyond the left edge of the frame, never the lens; he is the only person in the frame; uneasy, not smiling: brows tight, lips pressed shut; the small warm light on one side of his face; behind him, soft, only the plaster wall and the dark blue window; {HANDS}",
         lines=[("xitong", "宿主連她會不會騎馬，都不知道。", "冷，毒舌")],
         motion=f"Xu Yan's eyes follow something toward the doorway and his throat moves as he swallows once; {SILENT_HE}",
         zh="近景、慢推（送 `-chuang-l1`：夜裡的床與窗）：許硯看著畫左外的門口（阿令出門的方向；看的是地方，不寫人，拍法 31），喉嚨動一下（一個動作）；系統是錄音、**全程嘴閉著**；不寫淡藍光（拍法 11；系統的鬥嘴不出面板）。稿子 c15 系統 13 字＋心裡話 15 字約 8.5 秒加停頓，8 秒片段放不下剪點：照第 37 集 s16b 的做法拆成本鏡與 s15b"),
    dict(sid="s15b", loc="rx_c", cam="Medium close-up, slow push in", chars=["xuyan"], night="lamp",
         comp=f"medium close-up of {XU_COAT}, standing in the room, framed from the waist up, both his hands resting at his sides from the first frame, his face three-quarter to screen left, his eyes on the dark doorway beyond the left edge of the frame, never the lens; he is the only person in the frame; quietly certain, not smiling: brows easing, lips pressed shut; behind him, soft, only the plaster wall and the dark blue window; {HANDS}",
         lines=[("xuyan", "不知道……可她從來不說沒把握的話。", "心裡話，錄得近、輕", "inner")],
         motion=f"Xu Yan draws one slow deep breath, his shoulders rising and settling, his eyes still on the doorway; {SILENT_HE}",
         zh="中近景（腰以上、跟 s15 不同景別）、慢推（送 `-chuang-l1`）：**拆鏡**：稿子 c15 的心裡話：吸一口長氣、肩膀起落（一個動作）；心裡話是錄音、**全程嘴閉著**、不笑（回系統的嘴）"),
    dict(loc="ny", cam="Wide shot, slow push in", chars=["tangxiaotang", "qinshuang", "aling"], nospeak=["tangxiaotang"], night="night",
         comp=f"wide shot from beside the dark house doorway across the night yard, like the picture; in the lower left foreground, seen only from behind, {TBACK_SMALL}, standing before the house doorway, framed full figure, facing straight away from us; beside her at the left, {QIN}, {SPEAR} upright in her right hand, standing side-on, framed full figure, her face toward the tree, her lips closed, not smiling, never the lens; beside the bare tree, {HORSE}, side-on, head to the left, untied; at its near side, {ALING_R}, {WHIP_SASH}, framed full figure, her left foot already in the stirrup and both hands on the saddle from the first frame, her lips closed, not smiling, never the lens; {HANDS}; exactly three people and one horse",
         lines=[("tangxiaotang", "阿令姊……妳什麼時候學會騎馬的？", "驚")],
         motion=f"A-ling swings herself up into the saddle in one smooth fast move and sits firm, gathering the reins, while the horse shifts one step; {quiet('Qin Shuang and A-ling', 'their', plural=True)}; {HEADSTILL}",
         zh="全景、慢推（照圖；送第 31 集的 `set-xujia-yuan-ye-dong2-l1`：屋與門洞在左、院門在後牆中間（門扇掛在右柱往內半開，第 37 集必改 1）、光禿的樹在院門右、井在前右；加送 `prop-zaohongma-l1`：棗紅馬全身紅棕、鬃尾同色，鞍寫在文字，拍法 41）：入夜。**棗紅馬拴在院門右邊那棵光禿的樹下**（聖經：柿子樹照圖寫光禿的樹），韁繩第一格已經解開；阿令（袖口紮緊、綁腿、馬鞭插在腰帶）第一格已經左腳踩鐙、兩手按鞍，一翻身上馬坐穩（一個動作，整個動作在畫面裡；稿子『原地轉半圈』不寫）；唐小棠小背影在左下前景、屋門口（不寫淡杏外衣；她的話是錄音、頭不動），秦霜在她左邊、右手長槍直立、側身看樹、嘴閉著（加送長槍圖）。人與馬不重疊"),
    dict(loc="ny_h", cam="Close-up, slow push in", chars=["qinshuang"], night="night",
         comp=f"close-up of {QIN}, standing before the dark house doorway, framed from the chest up with space above her head, the wooden shaft of {SPEAR} upright in her right hand at the edge of the frame, her face three-quarter to screen right, her eyes on the horse under the tree beyond the right edge of the frame, never the lens; she is the only person in the frame; seeing it clearly, not smiling: eyes narrowing, brows level, lips moving quietly between words; behind her, soft, only the dark doorway and the split firewood in the moonlight; {HANDS}",
         lines=[("qinshuang", "那是騎兵上馬的法子，不是剛學的。", "很輕")],
         motion="Qin Shuang's eyes narrow and her hand tightens on the spear shaft as she speaks very quietly",
         zh="近景、慢推（送第 36 集的 `set-xujia-yuan-ye-dong2-wu-l1`：屋左的黑門洞與柴堆；稿子『身後只有屋門的門框』）：秦霜眼睛一瞇、握槍的手收緊（一個動作），看著畫右外樹下的馬（看的是東西，不寫人，拍法 31），很輕地說（答 s16；聖經〈伏筆〉：阿令的身分）；加送長槍圖"),
    dict(loc="ny_g", cam="Medium shot from behind, slow push in", chars=["tangxiaotang", "aling"], nospeak=["tangxiaotang"], night="night",
         comp=alone(f"beyond her, at the yard gate in the middle of the back wall, the slatted plank gate leaf hinged on the right gate post standing half swung back inward from the first frame to the last, unmoving; in the clear left half of the gateway, {ALING_R}, {WISPS}, already in the saddle of {HORSE} from the first frame, seen from behind and the side, framed from the waist up with the horse's hindquarters, already riding away from us out through the gateway, never the lens; she stays in the middle of the frame the whole shot; {HANDS}; exactly two people and one horse, the young woman in the middle seen only from behind",
                    "standing in the yard a few steps inside the gate, her flat right hand raised beside her shoulder,"),
         lines=[("tangxiaotang", "東街的白大夫，許記的老主顧，報許家的名字！", "揚聲")],
         motion=f"A-ling digs her heels in and the horse breaks into a gallop out through the gateway into the dark, while the young woman calls after her with her hand still raised, only her arm moving; {quiet('A-ling', 'her')}; {HEADSTILL}",
         zh="中景（從背後）、慢推（送第 36 集的 `set-xujia-yuan-ye-dong2-zhong-l1`：木桶、光禿的樹、院門；加送棗紅馬圖）：唐小棠背影在正中、右手平掌舉在肩邊（頭不動，錄音揚聲；不寫淡杏外衣）；阿令第一格已經在馬上、從背後與側面拍（拍法 41：側後、腰以上加馬身），一夾馬腹、馬從院門左半空著的門洞衝出去（一個動作；院門照圖：門扇掛右柱、往內半開，第 37 集必改 1）；稿子『阿令點一下頭』從背後看不到，不寫。白大夫的來處（許記的老主顧）在這句"),
    dict(loc="rx_c", cam="Wide shot, slow push in", chars=["xuyan", "xiaohe"], night="lamp",
         comp=f"wide shot at the bedside by night: in the bed against the back wall, {XIAOHE_BED}, her eyes already half lifted from the first frame, her lips barely moving; kneeling on the floor at the near side of the bed, {XU_COAT}, framed full figure with both knees on the floor, both his hands already folded round her small left hand from the first frame, his face lowered three-quarter to screen right toward her, never the lens; pleading and tender, not smiling: brows drawn, eyes wet, lips moving low between words; the one small flame on the table at the right lighting their faces from the side; behind them, soft, the dark blue window and the plaster wall; {HANDS}; exactly two people",
         lines=[("xiaohe", "哥……", "很弱，氣音，嘴唇微動"), ("xuyan", "哥在這裡。撐到阿令回來，天亮就不燙了。", "低，像在求她")],
         motion="little Xiaohe's small fingers stir in his hands, and Xu Yan lifts her small hand to his chin, bows his head and closes his eyes",
         zh="全景（全身：**跪姿拍到膝蓋**）、慢推（送本集免費做的 `set-xujia-tangfang-chuang-l1`：夜裡的床、窗、桌角的火；稿子『身後只有窗紙與油燈』）：屋內收尾：許硯跪回床邊、兩手第一格已經合握小禾的小手；小禾眼睛半睜、手指動一下，許硯把她的手貼到自己下巴前、低頭閉眼（一個動作）；先小禾很弱的氣音『哥……』（嘴唇微動，2026-11-06 審稿：不是短喊），再許硯低聲說（本場結尾）；小禾一直在床上（原版必修）"),
    # ---- scene 2: the road to the county town and its gate, the second watch.
    dict(chapter="夜裡的官道與縣城城門", loc="g", cam="Low-angle wide shot, slow push in", chars=["aling"], night="night", act=3,
         comp=f"low-angle wide shot from the side of the road at ground height, side-on: a long line of tall dark poplars across the frame against the deep blue night sky, the flat dark field before them and the wide pale dirt road running across the frame from the right edge to the left; on the road, {HORSE}, already galloping in from the right edge from the first frame, seen side-on, with {ALING_R}, {WISPS}, crouched low over its neck, framed full figure; dust kicking up behind the hooves; she is the only person in the frame; {HANDS}",
         motion="the horse gallops across the frame from right to left along the road and on toward the left edge, dust billowing behind it, her body low and still over its neck",
         zh="低角度全景（貼地、側面）、慢推（送本集免費做的 `set-guandao-ye-ce-l1`：一長排楊樹橫過畫面、乾田、夜空；加送棗紅馬圖）：**月夜官道**（原版必修：不是白天）：阿令伏在馬背上，**由右往左**狂奔（聖經：柳溪在右、縣城在左，去程一律右往左），馬蹄揚起黃土。**稿子前景的空白石碑不寫**（聖經第 33 條：里程碑拿掉）。無台詞"),
    dict(loc="g", cam="Medium shot, tracking", chars=["aling"], night="night", act=3,
         comp=f"medium tracking shot alongside the galloping horse, side-on: {ALING_R}, {WISPS}, {WHIP_SASH}, riding {HORSE} at full gallop toward the left, framed from the waist up with the horse's head and neck before her, crouched low, her face in profile to screen left, her eyes on the road ahead beyond the left edge of the frame, never the lens; she is the only person in the frame; tense, not smiling: lips bitten together, eyes hard; behind her, sliding past soft and dark, the line of tall poplars and the moonlit field; {HANDS}",
         motion=f"A-ling snaps the reins and drives her heels hard into the horse's flanks, and the horse lunges forward and stretches out faster, its mane streaming; {quiet('A-ling', 'her')}",
         zh="中景（側面、腰以上加馬頭頸，拍法 41）、**跟拍**（稿子『跟拍，由右往左，跟著馬』：只有這一鏡寫跟拍，好讓騎馬的人一直在畫裡）（送本集免費做的 `set-guandao-ye-shu-l1`：楊樹一排、乾田）：阿令咬著唇、髮絲被風吹出木簪（髻與木簪照圖），眼睛看著畫左外前方的路（稿子『城門火光』寫成前方的路，看的是地方），抖韁、一夾馬腹、馬往前一竄加速（一個動作）；嘴閉著。無台詞"),
    dict(loc="c_b", cam="Wide shot, slow push in", chars=["aling"], night="night", act=3,
         comp=f"wide shot at the barrier, like the picture: at the left edge the half-swung right leaf of the big studded gate with one torch fixed upright in an iron holder beside it, nobody holding it; the long waist-high barrier of crossed wooden stakes running across the frame along the foot of the lit brick wall; the stone paving before it; on the paving, {HORSE}, already reined in hard three steps short of the barrier from the first frame, seen side-on with its head toward the left, with {ALING_R}, {WISPS}, in the saddle, framed full figure, her face in profile to screen left toward the gate, never the lens, her lips closed, not smiling; she is the only person in the frame; {HANDS}",
         motion="the horse's forelegs lift off the paving and come down again, and it stamps on the spot, snorting, while A-ling holds the reins tight",
         zh="全景、慢推（送本集免費做的 `set-chengmen-ye-zha-l1`：畫左半開的門扇與插在鐵架上的火把（沒人拿，拍法 23）、橫過畫面的齊腰拒馬柵、石板地；加送棗紅馬圖）：**城門照圖**：大門左扇關著、**右扇往外半開**（稿子『門洞旁巡夜的小門開著』＝圖上半開的那扇），**拒馬柵沿著門右邊的牆**（稿子『橫在路上』照圖寫）；**牆上不寫告示板**（聖經第 33 條，原圖的匾試鏡時已塗掉）。阿令的馬第一格已經在柵前三步勒住，前蹄揚起又落下、原地踏步噴氣（一個動作）。無台詞"),
    dict(loc="c_b", cam="Medium shot, slow push in", chars=["duizhang"], night="night",
         comp=f"medium shot behind the barrier of crossed stakes, the tops of the crossed stakes soft along the bottom of the frame: {CAPTAIN}, standing behind the barrier, framed from the waist up, {CAP_SPEAR} in his right hand, his face lifted three-quarter to screen right {off('right', 'the dark road along the wall')}; harsh and loud, not smiling: brows down, jaw hard, mouth wide between shouted words; behind him, soft, the lit brick wall and one torch fixed upright in an iron holder, nobody holding it; {HANDS}",
         lines=[("duizhang", "宵禁！有流寇，天亮以前誰都不准進城！", "吼")],
         motion="the guard captain steps forward and slaps the spear shaft down level across the top of the barrier with both hands as he shouts",
         zh="中景、慢推（送本集免費做的 `set-chengmen-ye-qiang-l1`：火光照亮的磚牆、鐵架上的火把、柵頂）：**守軍隊長第一次出場**：送 `duizhang-portrait-l1`（mkspec 加在最後一張：黑甲紅釘、開面鐵盔、護耳、盔頂一撮紅纓；整集同一張臉、同一頂盔，原版必修）；他在柵後、右手長矛，往前一步、長矛往柵頂一橫（一個動作），朝畫右外看不到的人（馬上的阿令，不寫人，拍法 31）吼。稿子『身後兩個守軍（背影）』不寫（人少，拍法 34）"),
    dict(loc="c_g", cam="Medium shot from behind, slow push in", chars=[], night="night",
         comp=f"medium shot by the half-swung gate leaf, from behind and a little to one side: {GUARD}, seen only from behind and the side, only the edge of his cheek and jaw showing past the cheek flap of his helmet, leaning one shoulder against the half-swung leaf of studded planks, framed from the waist up, {CAP_SPEAR} in his right hand with its butt on the paving, his face turned toward the road at the right, never the lens; jeering, his shoulders shaking with a mocking laugh; beside the leaf, one torch fixed upright in an iron holder, nobody holding it; behind him, soft, the shut left leaf of the gate and the brick arch; {HANDS}; he is the only person in the frame",
         lines=[("shoujun", "女人騎什麼馬，回家燒飯去吧！", "起鬨，笑得很賤")],
         motion=NOBODY + "the young guard knocks the butt of the spear twice on the paving and tips his head to one side, laughing, his face staying turned away from us",
         zh="中景（從背後與側面）、慢推（送本集免費做的 `set-chengmen-ye-men-l1`：關著的左扇、半開的右扇、火把）：**年輕守軍**（小角色，不點名、不送圖：黑甲、無纓鐵盔）只拍側後，只露臉頰與下巴一角（聖經〈小角色〉），靠在半開的門扇上，矛尾往石板地敲兩下、歪頭笑（一個動作；稿子『敲木柵』：這張裁切沒有柵，改敲地）；台詞是錄音（Alnilam，`MINOR`，不在 chars）"),
    dict(loc="c_r", cam="Medium shot, slow push in", chars=["aling"], night="night",
         comp=f"medium shot on the road along the wall, side-on: {ALING_R}, {WISPS}, sitting in the saddle of {HORSE}, framed from the waist up with the horse's head and neck before her, the horse's head toward the left, her face lowered three-quarter to screen left {off('left', 'the torchlit barrier of crossed stakes', he='she')}; cold to the bone, not smiling: eyes narrowed, brows level, lips moving low and hard between words; behind her, soft, the long dark wall and the road back the way she came under the moon; {HANDS}",
         lines=[("aling", "家裡的妹妹燒了一整天，讓開。", "冷到底")],
         motion="A-ling's hands tighten on the reins and draw them in short as she speaks, the horse tossing its head once",
         zh="中景（側面、腰以上加馬頭頸，拍法 41；稿子『下巴以上近景』改中景好讓馬頭在畫裡）、慢推（送本集免費做的 `set-chengmen-ye-lu-l1`：柵的另一頭、長城牆、她來的路；稿子『身後只有城樓的火光』：她面向左，身後是來路）：阿令低頭朝畫左外看不到的人（隊長，不寫人）冷冷地說、握韁的手收緊（一個動作）（→ 答在 s26）"),
    dict(loc="c_b", cam="Medium shot, slow push in", chars=["duizhang"], night="night",
         comp=f"medium shot behind the barrier of crossed stakes, the tops of the crossed stakes soft along the bottom of the frame: {CAPTAIN}, standing behind the barrier, framed from the waist up, {CAP_SPEAR} already lowered level in both hands from the first frame, its spearhead pointing out past the right edge of the frame, his face three-quarter to screen right {off('right', 'the dark road along the wall')}; hard and final, not smiling: brows down, eyes hard, lips moving hard between words; behind him, soft, the lit brick wall and one torch fixed upright in an iron holder, nobody holding it; {HANDS}",
         lines=[("duizhang", "再往前一步，就當流寇拿下！", "喝令，拒絕")],
         motion="the guard captain thrusts the spear forward one short hard jab toward the right and holds it there as he barks the order",
         zh="中景、慢推（送 `-qiang-l1`）：隊長第一格已經兩手把長矛放平、矛尖朝畫右外，往前一戳、停住（一個動作；稿子『矛尖對著馬胸』：馬不入鏡，寫矛尖朝畫右外），喝令（答 s25：不讓）；不笑"),
    dict(loc="c_b", cam="Wide shot, slow push in", chars=["aling", "duizhang"], night="night", act=3,
         comp=f"wide shot from the side at the barrier, the whole charge inside the frame: at the left the half-swung leaf of the big studded gate with one torch fixed upright in an iron holder beside it, nobody holding it; the long waist-high barrier of crossed wooden stakes along the foot of the lit brick wall; on the paving at the right, {HORSE}, already charging at full gallop toward the barrier from the first frame, seen side-on with its head toward the left, with {ALING_R}, {WISPS}, crouched flat over its neck, framed full figure; behind the barrier at the left, {CAPTAIN}, framed full figure, small, already flinching back from the first frame, his face toward the horse, never the lens, his mouth wide in alarm; {HANDS}; exactly two people and one horse",
         motion=f"the horse pounds across the paving straight at the barrier and gathers itself at its foot, its forelegs just lifting from the ground, while the guard captain throws himself aside; {quiet('A-ling and the guard captain', 'their', plural=True)}",
         zh="全景（側面，整個衝刺在畫面裡）、慢推（送 `-zha-l1`；加送棗紅馬圖、隊長圖）：**聖經第 41 條：不拍躍起的那一下**：稿子 c27 拆成兩鏡：本鏡『衝向木柵』：阿令第一格已經伏在馬頸上全速衝向柵（稿子『勒馬往後退三步』在第一格前完成），衝到柵腳、馬蹄剛要離地就剪；柵後的隊長往旁邊一撲；空中那一下交給剪接與馬蹄聲（lessons：跳躍拆成起跳與落地兩鏡）。無台詞"),
    dict(sid="s27b", loc="c", cam="Wide shot, slow push in", chars=["aling", "duizhang"], night="night", act=3,
         comp=f"wide shot of the city gate, like the picture; a thick billow of dust already rising on the paving beside the barrier from the first frame; on the gate side of the barrier, {HORSE}, already landed on the paving from the first frame and running on at full gallop toward the half-swung right leaf of the gate, seen from the side and behind, with {ALING_R}, {WISPS}, crouched low in the saddle, framed full figure; on the paving at the right, {CAPTAIN}, already sprawled on the stones from the first frame, framed full figure, small, his spear lying beside him, his face toward the gate, never the lens; {HANDS}; exactly two people and one horse",
         motion=f"the horse runs on through the dust and plunges into the dark gap behind the half-swung gate leaf, gone from sight, while the guard captain pushes himself up on one elbow; {quiet('A-ling and the guard captain', 'their', plural=True)}",
         zh="全景（照圖；送 `set-chengmen-ye-l1` 整張；加送棗紅馬圖、隊長圖）：**拆鏡**（拍法 41）：『已經落在木柵這一側、塵土揚起』：第一格馬已經落地、塵土翻起，往半開的右扇跑、衝進門扇後面的黑暗裡（一個動作；稿子『直衝進開著的小門』）；隊長第一格已經跌坐在石板地上、長矛落在身邊，撐起一隻手肘（不是跪：手肘撐地的人小、全身入鏡）。剪接剪在馬衝進門扇的一半（稿子〈剪接〉）。無台詞"),
    dict(loc="c_g", cam="Medium shot, slow push in", chars=["duizhang"], night="night",
         comp=f"medium shot by the half-swung gate leaf: {CAPTAIN}, already back on his feet from the first frame, a dusting of grey dust over his black armour, framed from the waist up, his face three-quarter to screen left toward the dark gap behind the half-swung leaf of studded planks, never the lens; he is the only person in the frame; furious, not smiling: brows crushed down, mouth wide between shouted words; beside the leaf, one torch fixed upright in an iron holder, nobody holding it; behind him, soft, the shut left leaf of the gate and the brick arch; {HANDS}",
         lines=[("duizhang", "弩手！追上去，別讓她跑出東街！", "吼")],
         motion="the guard captain sweeps his flat right hand toward the dark gap of the gate and roars the order into it",
         zh="中景、慢推（送 `-men-l1`）：隊長第一格已經從地上爬起來、黑甲一層灰（一大片，不寫細點），朝半開門扇後的黑暗（城裡）右手平掌一揮、吼（一個動作；稿子『從地上爬起來』在第一格完成）；**稿子『身後六個弩手從城門洞裡跑出來、衝進小門』不拍**：弩手在城裡，第三場 s32 才入鏡（人少，拍法 34；畫外的人不寫，拍法 31）。本場結尾"),
    # ---- scene 3: the east street of the county town, before the clinic door.
    dict(chapter="縣城東街，醫館門口", loc="e", cam="Wide shot, slow push in", chars=["aling"], night="night",
         comp=f"wide shot down the street, like the picture: {STREET}; before the steps of the nearest two-leaf plank door at the right, {HORSE}, already reined in from the first frame, standing side-on with its head toward the right, with {ALING_R}, {WISPS}, in the saddle, framed full figure, her face toward the door, never the lens, her lips closed, not smiling; the two leaves of the plank door shut; she is the only person in the frame; {HANDS}",
         motion=f"A-ling swings down out of the saddle before the horse has quite stopped and lands on her feet on the paving beside it, the reins in her hand; {quiet('A-ling', 'her')}",
         zh="全景（照圖；送 `set-yiguan-men-ye-l1`：石板街往左邊遠處、右邊一排關著的木板店門、深屋簷；最近那間兩扇木門板、兩級石階、門左一根方石拴馬樁；加送棗紅馬圖）：**醫館＝最近那間**（聖經〈場景〉：門在右）；**門楣不寫招牌**（聖經第 33 條：原版的空白招牌也拿掉）。阿令第一格已經在階前勒住馬，不等馬停穩就翻身下馬、落地（一個動作；稿子『韁繩往拴馬樁一繞、跨上石階』交給 s30：馬拴在樁上）。兩扇門板關著。無台詞"),
    dict(loc="e_d", cam="Medium shot, slow push in", chars=["aling"], night="night",
         comp=f"medium shot at the two-leaf plank door, from the side: {ALING_R}, {WISPS}, {WHIP_SASH}, standing on the top stone step facing the door at the right, side-on, framed from the waist up, both her palms already raised flat against the shut door leaves from the first frame, her face in profile to screen right toward the door, never the lens; desperate, not smiling: brows drawn, mouth wide, shouting loud between words; at the left edge of the frame, the head and neck of {HORSE}, its reins looped round the square stone hitching post, well apart from her; she is the only person in the frame; {HANDS}",
         lines=[("aling", "白大夫！柳溪許家，求您開門！", "拍門，第一次這麼大聲")],
         motion="A-ling pounds both flat palms on the door leaves, one after the other, hard, and the leaves shudder at every blow as she shouts",
         zh="中景（側面）、慢推（送本集免費做的 `set-yiguan-men-ye-men-l1`：兩扇木門板、兩級石階、左邊方石拴馬樁；加送棗紅馬圖）：阿令站在上一級石階、面向畫右的門（背對畫左的街口），兩手掌第一格已經按在門板上，輪流重重拍門、門板一震一震（一個動作），聲音第一次這麼大（→ 答在 s31）；**棗紅馬在畫左緣，只到頭頸、韁繩繞在方石拴馬樁上、跟她分開**（拍法 41：拴著的馬寫在哪一側、拴在什麼上）；門楣不寫"),
    dict(loc="e_x", cam="Insert close-up, slow push in", chars=[], night="night",
         comp="insert close-up, the very first frame is already a close view of the narrow seam between two shut leaves of dark wooden planks, a thin line of warm light already glowing through the seam, and one hand in a grey-white sleeve bound at the wrist with a strip of grey cloth pressed flat on the planks beside it; the planks fill the background to every edge; only the planks, the seam of light and the one hand are in the frame",
         lines=[("baidaifu", "來了來了，半夜拍什麼門，門都要拍壞了。", "畫外，門裡，慢，不慌，加一點悶")],
         motion=NOBODY + "the thin line of warm light in the seam brightens slowly and wavers once, as if a small flame is carried closer behind the door, and the hand on the planks goes still",
         zh="插鏡、慢推（**第一格就是門縫**，拍法 10、35；不寫地點句，送本集免費做的 `set-yiguan-men-ye-feng-l1`（兩扇門板的門縫近景）只當背景與光）：門縫裡的暖光從暗到亮、晃一下（白大夫的油燈拿近，第 39 集他左手一盞陶油燈，拍法 33：不是燈籠）；阿令的手（灰白袖口、布條紮緊，不點名）按在門板上停住（一個動作）；白大夫是門內的畫外聲（Rasalgethi；第 39 集才入鏡）（答 s30）"),
    dict(loc="e_s", cam="Wide shot, slow push in", chars=["duizhang", "aling"], night="night",
         comp=f"wide shot up the street toward its far end at the left, the square stone hitching post soft in the right foreground: coming up the middle of the stone-paved street, already halted in a ragged line from the first frame, {XBOWMEN}, seen side-on and from the front at a distance, small, framed full figure, and {TORCHMAN}; one step in front of their line, {CAPTAIN}, framed full figure, small, his face three-quarter to screen right toward the clinic steps, never the lens; harsh, not smiling: mouth wide between shouted words; at the right edge, on the top step of the nearest plank door, {ALING_R}, seen only from behind, framed full figure, her back to the street, both her hands on the door leaves; {HANDS}; exactly nine people",
         lines=[("duizhang", "別動！轉過身來，兩手舉高！", "吼")],
         motion=f"the guard captain strides one step forward ahead of the line and throws up his flat right hand as he shouts, while the six crossbowmen stand still with their crossbows level; {quiet('A-ling and the crossbowmen', 'their', plural=True)}",
         zh="全景、慢推（送本集免費做的 `set-yiguan-men-ye-jie-l1`：石板街往左邊遠處；前景右下方石拴馬樁）：隊長帶六個弩手追到（稿子『從街口跑進來』在第一格完成：第一格已經停成一排），一個守軍舉一支火把（只有一支、拿在一個人手裡，拍法 37）；弩手是同一身黑甲鐵盔（拍法 34：一群同制服，可以同色），**正臉不拍**：遠、小、臉在盔影裡；隊長往前一步、右手平掌一舉、吼（一個動作）；畫右緣阿令背對街口站在石階上、兩手按門、嘴閉著。九個人（→ 答在 s33）"),
    dict(loc="e_d", cam="Close-up from the side, slow push in", chars=["aling"], night="night",
         comp=f"close-up from the side at the two-leaf plank door: {ALING_R}, {WISPS}, standing on the top step facing the shut door leaves at the right, side-on, framed from the chest up, her flat right palm already on the planks, her face in profile to screen right toward the door, her back to the street, never the lens; she is the only person in the frame; cold and unbending, not smiling: eyes narrowed, jaw set, lips moving low and hard between words; at the left, soft and out of focus, only a warm orange smudge of torchlight far down the dark street; {HANDS}",
         lines=[("aling", "我妹妹等不了，我只要大夫。", "冷，不回頭")],
         motion="A-ling, her head held still toward the door, slaps her flat palm once more against the door as she speaks",
         zh="側面近景、慢推（送 `-men-l1`；2026-11-06 審稿改的：門板在畫右、街口的火把光虛焦在左）：阿令面向畫右的門、背對街口、不回頭，手掌再拍一下門板（一個動作），冷冷地說（答 s32：不轉身）"),
    dict(loc="e_x", cam="Low-angle insert close-up, slow push in", chars=[], night="night",
         comp="low-angle insert close-up, the very first frame is already a close view of six plain wooden crossbows rising into the frame from the bottom edge side by side, each held in two hands in black armoured cuffs, their short bolts pointing toward the right; far below, soft and out of focus, only grey stone paving in cold moonlight fills the background to every edge; only the hands and the six crossbows are in the frame",
         motion=NOBODY + "the six crossbows rise one after another until every one is level and still, aimed toward the right",
         zh="低角度插鏡、慢推（**第一格就是弩**，拍法 10、35；不寫地點句，送本集免費做的 `set-yiguan-men-ye-di-l1`（石板地近景）只當地面與光）：六把木弩（一人一把，聖經〈道具〉）從畫面下緣一把接一把舉平、對著畫右（一個動作；稿子『拉滿』：弩上弦寫不出，交給音效）；只有黑甲袖口與手。無台詞"),
    dict(loc="e_s", cam="Medium shot, slow push in", chars=["duizhang"], night="night",
         comp=f"medium shot in the street: {CAPTAIN}, standing in the middle of the line, {CAP_KNIFE} already held out in his right hand from the first frame, its point toward the right, framed from the waist up, his face three-quarter to screen right {off('right', 'the dark street and the shut shopfronts')}; low and vicious, not smiling: eyes narrowed, jaw hard, lips moving low between words; behind him at the left, soft and out of focus, two crossbowmen in the same black armour and iron helmets seen side-on, their faces in the shadow of their helmets, each with {XBOW}; {HANDS}; exactly three people",
         lines=[("duizhang", "弩手聽令，全部對準她的背！", "低，狠")],
         motion="the guard captain thrusts the knife point out toward the right and holds it there as he gives the order low",
         zh="中景、慢推（送 `-jie-l1`）：隊長（同一張臉、同一頂盔：送同一張定妝照）站在弩手一排中間，右手短刀第一格已經拔出來指著（不拍拔刀那一下：一鏡一個動作），往畫右外一指、停住（一個動作），朝畫右外看不到的人（阿令的背，不寫人）低狠地說；身後兩個弩手虛焦、側面、臉在盔影裡"),
    dict(loc="e_d", cam="Medium shot over a crossbow, slow push in", chars=["aling"], night="night", act=3,
         comp=f"medium shot from behind a raised crossbow: the plain wooden stock of a crossbow held level in two hands in black armoured cuffs soft and dark in the lower left foreground, aimed toward the clinic door; beyond it, {ALING_R}, seen only from behind and a little to the side, standing on the top stone step, framed from the knees up, both her hands on the shut plank door leaves, her head bowed toward the door; a thin line of warm light glowing through the seam between the leaves; {HANDS}; exactly two people, the one holding the crossbow seen only as two hands",
         motion=f"the crossbow wavers a hair and steadies, A-ling's shoulders rise and fall with her breathing, and the line of light in the door seam grows brighter; {quiet('A-ling', 'her')}",
         zh="主觀（從弩手的弩後面看出去）、慢推（送 `-men-l1`）：前景左下一把木弩的弩身與兩隻黑甲袖口的手（不點名、不送圖）；阿令從背後與側面、站在石階上、兩手按門板、低頭，肩膀起伏，門縫的光越來越亮（一個動作的連續）；嘴不入鏡。無台詞"),
    dict(loc="e_s", cam="Medium shot, slow push in", chars=["duizhang"], night="night",
         comp=f"medium shot in the street: {CAPTAIN}, standing in the middle of the line, {CAP_KNIFE} already moved to his left hand from the first frame and held down at his side, framed from the waist up, his face three-quarter to screen right {off('right', 'the dark street and the shut shopfronts')}; cold and final, not smiling: brows down, eyes hard, mouth wide between shouted words; behind him at the left, soft and out of focus, two crossbowmen in the same black armour and iron helmets seen side-on, their faces in the shadow of their helmets, each with {XBOW}; {HANDS}; exactly three people",
         lines=[("duizhang", "再不轉身，我這隻手一落，就放箭！", "吼")],
         motion="the guard captain raises his empty right hand slowly straight up high over his head and holds it at the top as he shouts",
         zh="中景、慢推（送 `-jie-l1`）：隊長短刀第一格已經換到左手、垂在身側（稿子『交到左手』在第一格完成），右手空著慢慢高高舉起、停在最高點（一個動作），吼；身後兩個弩手虛焦"),
    dict(loc="e_s", cam="Close-up, slow push in", chars=["duizhang"], nospeak=["duizhang"], night="night",
         comp=f"close-up of {CAPTAIN}, standing in the street, framed from the chest up with his raised right hand already high above his helmet from the first frame, his face three-quarter to screen right {off('right', 'the dark street and the shut shopfronts')}; merciless, not smiling: brows crushed down, mouth wide on one long shouted word; behind him, soft and out of focus, only the dark street and the cold moonlight; {HANDS}",
         lines=[("duizhang", "放——", "短喊")],
         motion="the guard captain's raised right hand starts to sweep down as he shouts the one long word",
         zh="近景、慢推（送 `-jie-l1`；稿子『從中近景推到近景』）：隊長右手第一格已經舉在頭頂，手往下落（一個動作），短喊（製作端寫成張嘴喊，不放進畫面描述：`nospeak`，構圖寫嘴張開喊一個字）；**剪在手落到一半、『放——』的拖音中間**（稿子〈剪接〉；懸念 → 第 39 集第一場：醫館門開，白大夫『放下！她是來求醫的！』）"),
]

HEAD = [
    "- 重製版 r2、真人版（站主 2026-11-11「之後都用真人版」）：照 `docs/videos/zhong-tian-qu-qi-e038-r2/script.md`（c01–c38 對應 s01–s38，加兩個拆鏡 s15b、s27b，共 40 鏡；含「這版改了什麼」「2026-11-06 審稿後的修改」）；台詞一字不改，只改拍法；每鏡一個看得見的動作、一句一筆不拆半句、預設不笑。篇章設定 `production/r2-bible-e031-e040.md`（拍法 1–43 條、〈場景〉〈接點〉〈道具〉〈小角色〉），帳照 `r2-bible-e011-e060.md`。**第 4 篇章〈旱年〉第 8 集**：約第一七六天清晨→正午→傍晚→入夜（病房、院子）→二更（官道、城門）→二更過半（縣城東街醫館門口）。",
    "- 內部工作編號 938（`hailuo/{ff,clips}-dh-e938.json`；`colab/runs/e938/extras.json`、`colab/runs/e938-live/spec.json`、工作資料夾 `~/mokaair-work/videos/zhong-tian-qu-qi-e938-dh/`）；發布 slug `zhong-tian-qu-qi-e038-r2`。不放集數、不放片名卡；**s01 接第 37 集定版成片 `e937-live.mp4`（205.79 秒）的最後一鏡**（s40 天快亮，許硯蹲在土埂上抱著軟下來的小禾、右手掌按她額頭）；s38 交給第 39 集（同一刻，醫館門開）。",
    "- 照第 37 集的審稿、成片審查與終驗的教訓一開始就照做：參考圖跟文字一致（本集的新圖都是免費調色與裁切、新 id）；門寫明推開、半開或關著（房門、院門、城門兩扇、醫館兩扇門板照圖）；許硯不寫鬍渣；風格句不寫 cinema camera；不寫 crowd、hundreds，寫實際人數，`exactly N` 寫在構圖、`only` 句再寫一次（多一人常見）；不寫泥（石灰寫白粉）；`OFFSCREEN_SPEECH = False`、對畫外的人說話寫「朝畫左／右外看不到的人」；不寫 open、不寫否定名詞；長東西第一格分開（長槍、長矛、馬鞭、弩）；同場相鄰說話的人錄音差 ≥ 3 個半音（拍法 43）。",
    "- **站主 2026-11-21～23 規則**（PR #2217，`production/OWNER-CHECK-20261122.md`）：品質優先；唐小棠背影鏡加送雙丸子背影參考圖（白天 s02 s04 s07 送站主原檔，夜裡 s16 s18 送免費夜版 `-ye`；mkspec）；跪姿拍到膝蓋（s01、s19 全身；s03 改坐床沿）；人群聲本集沒有（守軍、弩手不出聲；要的話照 `colab/runs/_scripts/crowd-murmur.py 38`）；音效用真實音效庫本機副本 `/root/mokaair-work/videos/_series/zhong-tian-qu-qi/sfx-real-20261121/`（`zhongtian-sfx-*`）；柴刀本集不寫。",
    "- **人物**：**唐小棠**（拍法 3、4、20、40）：說話的 s02、s04、s07、s16、s18 全部從背後拍、頭不動；l1 交領短襦，**不寫 t2 高立領、不寫淡杏外衣、不寫金算盤**；**本集沒有她的正臉**。**小禾**：病中一直躺在床上（滿臉通紅、髮絲黏額、嘴唇乾裂、額頭一塊摺好的濕布、粉被、草兔子在枕邊；原版必修：床上一直有她）。**秦霜**：柴刀不寫（拍法 5）；第 37 集那桿長槍（送道具圖 `prop-changqiang-l1`）。**阿令**：s13 起騎馬的樣子（袖口灰布條紮緊、裙下綁腿、灰布長腰帶）、s16 起馬鞭插在腰帶；第二、三場髮絲被風吹出木簪；本集沒有短刀、沒有面巾。**守軍隊長**（第一次出場）：送 `duizhang-portrait-l1`（mkspec 加在最後一張），黑甲紅釘、開面鐵盔、盔頂一撮紅纓；s23–s26 長矛、s35–s37 短刀；聲音 Iapetus（聖經）。**年輕守軍**（s24）只拍側後、錄音（Alnilam）；**弩手**六人同一身黑甲鐵盔，遠、小、側面，臉在盔影裡；**白大夫**只有 s31 門內的聲音（Rasalgethi）。",
    "- **軸線（照圖）**：病房照 `set-xujia-tangfang-l2`（拍法 42）：**門在左**、床靠後牆在窗下（枕頭那頭在右）、小桌在右前；進門的人從左邊來。院子照 `set-xujia-yuan-ye-dong2-l1`：屋與門洞在**左**、院門在後牆**中間**（門扇掛右柱往內半開、門洞左半空著）、光禿的樹在院門右、井在前右；馬拴在樹下，阿令從院門左半衝出去。官道：楊樹一排橫過畫面，**柳溪在右、縣城在左，去程一律由右往左**（聖經第 41 條）。城門照 `set-chengmen-ye-l1`：城門在**左**（左扇關、右扇往外半開、兩邊各一支插在鐵架上的火把），拒馬柵沿著門右邊的牆，路往右；阿令從右邊來、從半開的右扇衝進去。東街照 `set-yiguan-men-ye-l1`：街往**左**遠處、右邊一排關著的木板店門；醫館＝最近那間（兩扇門板、兩級石階、門左方石拴馬樁），阿令面向右、背對街，弩手從街的遠端（左）來。",
    "- **時間與光**：第一場清晨灰白（`-chen`）→正午白亮（`-chen`，光寫在文字）→傍晚暖橘（本集免費做的 `-xi`）→入夜桌上那一朵火（`-l2`）；院子冷月光；第二、三場冷藍月光，城門兩支火把、s32 起一支舉著的火把是唯一的暖光（**官道不能亮**，原版必修）。時間跳都在剪點（s03→s04、s04→s05、s11→s12、s15b→s16、s18→s19、s19→s20、s28→s29）。",
    "- **原版必修**：官道夜戲變白天、方向相反 → 只送夜圖、一律由右往左；里程碑刻拉丁亂碼 → **不寫石碑**（聖經第 33 條）；小禾從床上消失兩次 → 床在畫面裡的鏡都寫她（s01、s03–s05、s07、s08、s19）。原版建議：唐小棠『藥好了』不笑、被燙到（s02 從背後）；許硯『她等不了』咬牙不笑（s10）；騎兵上馬那鏡阿令已經上馬（s16 上馬、s17 秦霜）；隊長整集同一張臉、同一頂盔（同一張定妝照）；醫館不寫招牌。",
    "- 要買的秒數（BUY，錄音前照第 35–37 集實測估：一句 6 秒的鏡放得下約 5.9 秒人聲、8 秒約 7.3 秒；第 37 集量到許硯約 4 字／秒、唐小棠中位 3.4、阿令 3.4、秦霜約 3.7、系統 9 字約 2.4 秒；小禾、隊長、年輕守軍、白大夫照第 33–37 集估）：**8 秒** s06（許硯心裡話 17 字兩段）、s09、s12（秦霜 19 字兩句）、s13（阿令 16 字三句）、s18（唐小棠 19 字）、s19（小禾＋許硯）、s23（隊長 16 字吼）、s31（白大夫 16 字、慢）；**5 秒** s20、s21、s22、s27、s27b、s29、s34、s36（無台詞）、s38（『放——』）；其他 6 秒。錄音實測後照 `span938-buy.txt` 重核。",
    "- **表上的「秒」欄是 lint 估法**，比錄音短；剪接以錄音的人聲長度為準。",
    "- **官道、城門、東街（s20–s38）表上的提示詞帶「below the deep pool」**：只為了讓 `gen-dh` 的 `SET` 選到深潭那張圖（再由 `spec.json` 換成本集的圖），d1 由 `mkspec.py` 拿掉；**之後每個 fix／retake spec 都要帶同一組替換**。病房的提示詞帶「first bedroom of the Xu farmhouse」讓 `SET` 選到 `set-xujia-tangfang`（l2），院子帶「night yard of the Xu farmhouse」選到 `set-xujia-yuan-ye`（l2），`spec.json` 換成本集要送的圖。",
]
FOOT = [
    "- **參考圖**（`assets/refs-live/`）：許硯 l1、angle-a（帶笑的 angle-b 整集不送；全景 s01、s19 只送 l1）；唐小棠她的三張臉部圖全集都拿掉（沒有正臉），背影鏡加送雙丸子背影參考圖（s02 s04 s07 原檔、s16 s18 夜版 `-ye`）；小禾、秦霜、阿令見 `colab/runs/e938-live/mkspec.py`；秦霜有長槍的 s09、s12、s16、s17 加送 `prop-changqiang-l1`；馬在畫面裡的 s16、s18、s20–s22、s25、s27、s27b、s29、s30 加送 `prop-zaohongma-l1`；隊長的 s23、s26–s28、s32、s35、s37、s38 加送 `duizhang-portrait-l1`。過肩前景（s12 許硯的肩、s14 阿令的後腦）、門外的阿令（s12）、年輕守軍、弩手、舉火把的守軍、拿弩的手都不送圖。",
    "- **場景圖**：病房清晨送本集免費做的 `set-xujia-tangfang-chen-chuang-l1`（s01、s04）、`-chen-men`（s02）、`-chen-zhen`（s03）；傍晚 `-xi-zhen`（s05、s11）、`-xi-chuang`（s06、s07、s08、s10）、`-xi-men`（s09）；入夜 `-men`（s12、s13）、`-zhen`（s14）、`-chuang`（s15、s15b、s19）；院子送第 31 集的 `set-xujia-yuan-ye-dong2-l1`（s16）、第 36 集的 `-wu`（s17）、`-zhong`（s18）；官道送本集免費做的 `set-guandao-ye-ce-l1`（s20）、`-shu`（s21）；城門送 `set-chengmen-ye-zha-l1`（s22、s27）、`-qiang`（s23、s26）、`-men`（s24、s28）、`-lu`（s25）與整張 `set-chengmen-ye-l1`（s27b）；東街送整張 `set-yiguan-men-ye-l1`（s29）與本集免費做的 `-men`（s30、s33、s36）、`-feng`（s31 插鏡）、`-jie`（s32、s35、s37、s38）、`-di`（s34 插鏡）。",
    "- **本集新做的圖**（2026-11-23，`live-action/free-e031-e040/`，各跑兩次逐位元一樣，寫進 refs-live README）：`xujia_tangfang_e938.sh`（病房傍晚的暖橘調色 `-xi` 與清晨、傍晚、夜三組裁切）、`roads_e938.sh`（官道、城門、東街的裁切）。**不花錢**；沒有付費圖。",
    "- **還缺、先用最接近的圖**（不花錢、註明在這裡）：(1) **城門前沒有橫在路上的木柵、沒有門洞旁的小門**：照圖寫拒馬柵沿著門右邊的牆、右扇半開。(2) **官道圖是路往遠處消失的正面**：側面騎馬用左半的楊樹一排與乾田裁切，路寫在文字。(3) 病房、官道、東街偏 CG（試鏡第一、二輪的圖）。(4) 濕布、水盆、藥碗、湯匙、馬鞭、馬鞍、長矛、短刀、弩、火把是文字加在圖上（長槍、馬、隊長另送圖）。",
    "- 共用檔：`build-r2.py` 的 `EN` 加一個鍵 `duizhang`（守軍隊長第一次在畫面上說話；只加鍵，舊集逐位元重建不變）；`gen-dh.mjs`、`pilot.py`、`cast.json` 不動。對畫外說話、對地方說話的鏡，精修文字的通用說話視線由本檔結尾的 `live_clips()` 換成 d1 的方向句（`GAZE_REFINE`）；唐小棠的背影鏡：立領句拿掉、名字換成「從背後看的年輕女子」（同第 31、33、35–37 集）。",
    "- **自審**（2026-11-23，`writer-tools/e038-r2/review.md`，不是獨立審稿）；獨立審稿 `writer-tools/e038-r2/review-independent.md`（另一個沒寫稿的代理）。",
    "- **d1 前置**（2026-11-23，`colab/runs/e938-live/PREP.md`）：`colab/runs/e938/extras.json`、`colab/runs/e938-live/{mkspec.py,spec.json}`（種子 9381101／9381102）、scratchpad `tools/prep938.sh`、`tools/rec938-slow.sh`（錄音）、`e938d1.sh`（Colab，**沒跑**）。",
    "- 配樂：第一場很輕的鋼琴，s05 胡話換低沉弦樂，s11 面板一個重音，s16 上馬一個重音、接急促鼓點，s19 只剩一把胡琴；第二場急促鼓點，s27 衝刺一個大重音（剪在馬蹄離地、接 s27b 落地），s28 鼓點不停帶進第三場；第三場鼓點，s32 起拉緊的弦樂，s38 停在最高點、不收。音效見 script.md〈音樂與音效〉，從真實音效庫挑（站主 2026-11-21）；庫裡沒有的（弩上弦、門縫的燈、刀出鞘）列給站主用 Flow 做（提示寫 sound effect only, no music）。",
]

# Seconds to buy, estimated from e935-e937's measured lines (e937 PREP §4): a 6 s shot holds about 5.9 s of speech, 8 s about
# 7.3 s; Xu Yan about 4 characters a second (thoughts slower, with pauses), Tang Xiaotang median 3.4, A-ling 3.4, Qin Shuang about
# 3.7, the system 9 characters in about 2.4 s; Xiaohe, the guard captain, the young guard and Doctor Bai estimated (to be measured).
# 8 s: s06 (Xu's thought, 17 with two pauses), s09 and s12 (Qin 19 in two sentences), s13 (A-ling 16 in three), s18 (Tang 19),
#      s19 (Xiaohe's breath + Xu 16), s23 (the captain 16 shouted), s31 (Doctor Bai 16, slow).
# 5 s: s20, s21, s22, s27, s27b, s29, s34, s36 (no line), s38 (one shouted word).
# 6 s: every other spoken shot.
BUY = {"s06": 8, "s09": 8, "s12": 8, "s13": 8, "s18": 8, "s19": 8, "s23": 8, "s31": 8,
       "s20": 5, "s21": 5, "s22": 5, "s27": 5, "s27b": 5, "s29": 5, "s34": 5, "s36": 5, "s38": 5,
       "s01": 6, "s02": 6, "s03": 6, "s04": 6, "s05": 6, "s07": 6, "s08": 6, "s10": 6, "s11": 6, "s14": 6, "s15": 6, "s15b": 6,
       "s16": 6, "s17": 6, "s24": 6, "s25": 6, "s26": 6, "s28": 6, "s30": 6, "s32": 6, "s33": 6, "s35": 6, "s37": 6}


# ---- the refine text (as e031, e033, e935-e937): hailuo/clips-dh-e938.json column 0 is the motion text refine-prep.py sends
# with a picked d1 draft. gen-dh.mjs opens every clip that lists tangxiaotang with the CG-era "Tang Xiaotang's high stand-up
# collar stays closed at her throat." and names her in "<names> shown in <Picture 1>"; in a back shot that draws the collar back
# and turns her face to the lens. Her back shots: the sentence goes and her name becomes "the young woman seen only from behind".
COLLAR = "Tang Xiaotang's high stand-up collar stays closed at her throat. "
FRONT_TANG = set()
GAZE_GEN = {"he": "turned toward the person he is speaking to, face in profile or three-quarter profile, eyes on that person",
            "she": "turned toward the person she is speaking to, face in profile or three-quarter profile, eyes on that person"}
# sid -> (pronoun, the direction sentence): the listener is out of frame, or the speaker looks at a place
GAZE_REFINE = {
    "s01": ("he", "his face lowered three-quarter to screen right toward the girl in the bed, his eyes on her"),
    "s03": ("he", "his face lowered three-quarter to screen right toward the girl in the bed, his eyes on her"),
    "s05": ("she", "her head turned toward the left on the pillow, her eyes shut tight"),
    "s08": ("he", "his face lowered three-quarter to screen right toward the girl in the bed, his eyes on her"),
    "s10": ("he", "his face three-quarter to screen left toward someone out of sight beyond the left edge of the frame, his eyes on that spot"),
    "s13": ("she", "her face three-quarter to screen right toward someone out of sight beyond the right edge of the frame, her eyes on that spot"),
    "s17": ("she", "her face three-quarter to screen right, her eyes on the horse under the tree beyond the right edge of the frame"),
    "s19": ("he", "his face lowered three-quarter to screen right toward the girl in the bed, his eyes on her"),
    "s23": ("he", "his face lifted three-quarter to screen right toward someone out of sight beyond the right edge of the frame, his eyes on that spot"),
    "s25": ("she", "her face lowered three-quarter to screen left toward someone out of sight beyond the left edge of the frame, her eyes on that spot"),
    "s26": ("he", "his face three-quarter to screen right toward someone out of sight beyond the right edge of the frame, his eyes on that spot"),
    "s28": ("he", "his face three-quarter to screen left toward the dark gap behind the half-swung gate leaf, his eyes on it"),
    "s30": ("she", "her face in profile to screen right toward the shut door, her eyes on it"),
    "s32": ("he", "his face three-quarter to screen right toward the clinic steps, his eyes on them"),
    "s33": ("she", "her face in profile to screen right toward the shut door, her eyes on it"),
    "s35": ("he", "his face three-quarter to screen right toward someone out of sight beyond the right edge of the frame, his eyes on that spot"),
    "s37": ("he", "his face three-quarter to screen right toward someone out of sight beyond the right edge of the frame, his eyes on that spot"),
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
                names = [n for n in re.split(r", | and ", m.group(1)) if n != "Tang Xiaotang"]
                who = " and ".join(names + [BACK_NAME]) if len(names) < 2 else ", ".join(names) + f" and {BACK_NAME}"
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
# live_clips() writes no longer matches it. prep938.sh hands stage 1 the anchor form of the live file (this), then puts the
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
