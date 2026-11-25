"""Episode 39 remake (r2): the writer spec for ../e001-r2/build-r2.py. Source: docs/videos/zhong-tian-qu-qi-e039-r2/script.md
(c01-c40; the CG-era r2 script), including its sections 「這版改了什麼」 and 「2026-11-06 審稿後的修改」, which override the tables.
Every line is the script's, word for word; only the staging changes. 42 shots: one per script shot (sNN = cNN) plus two splits
that keep one voice per shot and room to cut (e938 s15b's way): s28b (c28's second system line and its panel, 突破四十 and the
reward box: the two system lines of c28 are 28 characters, past what one 8 s clip holds with the pause between them) and s29b
(Xu Yan's thought after the system's jibe of c29, about 8.5 s of speech with the pause).
Bible: production/r2-bible-e031-e040.md (arc 4 〈旱年〉: rules 1-43; 〈場景〉 (the sickroom is Tang Xiaotang's room picture as the
coordinator's paid Qwen edit of e938 left it: set-xujia-tangfang-kong-l1 by night, -kong-chen-l1 at first light; the barn front
set-gucang-wai-l1), 〈接點〉 38->39 (the same moment at the clinic door) and 39->40 (the barn front, everyone turning to Xu Yan),
the props (Doctor Bai's clay oil lamp, never a lantern (rule 33); his black lacquered medicine chest; A-ling's long grey sash; the
damp cloth, the basin, the medicine bowl; Xu Yan's old grey outer coat; Xiaohe's straw rabbit; the chestnut horse (rule 41) with
the felt saddle pad of prop-zaohongma-an-l1; Qin Shuang's spear; the crossbows; the neck rope), people (Doctor Bai's first face:
baidaifu-portrait-l1, his short white beard apart from Elder Han's long one; the guard captain duizhang-portrait-l1, one face and
one helmet as e038; A-ling's riding look; Diao Qi in his ragged tunic, never armour), 〈小角色〉 (the six crossbowmen, the torch
bearer, the village man who shouts, seen only from behind) and 原版必修 (e039: Doctor Bai never vanishes from the horse; the girl is
in the bed when he comes in; Xu Yan never laughs at 「誰？」)) and r2-bible-e011-e060.md (accounts: A-ling +12 -> 44, 突破四十, the
reward box: glass-making; Tang Xiaotang 45, Qin Shuang 48; the urgent task of e038 done in s25).
The ninth episode of arc 4: night of day 176 at the clinic door in the county town's east street (the second watch), the road back
to Liuxi before the third watch, the Xu farmhouse's first bedroom from the third watch to first light of day 177, then the barn
front at the edge of the fields in the early morning.

Written from the start the way e038-r2/r2.py stands AFTER its independent review and its fixes (writer-tools/e038-r2/{review.md,
review-independent.md}; colab/runs/e938-live/PREP.md §1-§7, fix1-fix6/plan.md), the task file's lessons (e933-e938) and the owner's
rules of 2026-11-21 to 23 (PR #2217, production/OWNER-CHECK-20261122.md):
- 38->39 from e938's cut (scratchpad e939prep/tail/sheet.jpg, e938-live.mp4 172-188.4 s): the captain's close-up, his right hand
  raised high, cut to black on 「放——」; before it A-ling on the top step from behind, both palms on the shut door, a crossbow in the
  foreground. s01 is the same moment: the two plank leaves already pushed inward, Doctor Bai on the threshold with his clay oil lamp.
- The pictures agree with the words: every place sentence follows the picture it sends; every new crop is a free id made for this
  episode (live-action/free-e031-e040/{xujia_tangfang_e939.sh,gucang_wai_e939.sh}) or e938's crops of the street, the road and
  the sickroom. The clinic's leaves are SHUT in the picture: the shots where they stand pushed inward say so in words (s01, s04, s05,
  s07); a paid edit of the doorway is listed in PREP.md §5, not made.
- No "cinema camera"; no stubble word for Xu Yan; no mud (the lime on his robe and on Diao Qi's cheek is pale white powder); no
  negated nouns (rule 18); long things never touch in the first frame (the spear, the crossbows, the walking staff, the rope); doors
  written pushed inward, ajar or shut every time they are in the picture.
- One more person than written is common: every frame says "exactly N people" or "the only person" in the composition and
  mkspec.py writes the 'only' sentence again at the end of the prompt.
- No collective noun (rule 34): the crossbowmen are six men in one black armour, side-backs and far shapes; the people at the barn
  are ten people each written with a colour and an age (never brown, blue-grey, dark brown, grey-white or peach: the leads' colours).
- OFFSCREEN_SPEECH = False (rule 15); rule 31: a line to someone out of frame is written "toward someone out of sight beyond the
  left/right edge of the frame", that side set only, the speaker the only person; a look at a thing names the thing. GAZE_REFINE
  puts the same direction into the refine text.
- No blue light (rule 11): the panels of s25, s28, s28b are the editor's; s25, s28, s28b, s29, s29b and s33 are Xu Yan's close-ups
  with his lips shut.
- Tang Xiaotang is not in this episode (script: she watches the medicine fire in the kitchen); nobody with two buns anywhere.
- Kneeling is framed to the knees (owner 2026-11-22): Diao Qi kneeling (s36, s39) is framed full figure with both knees on the
  ground; his close-up s40 does not write the kneel. Xu Yan sits on the edge of the bed in the sickroom (s14 on), never kneels.
- Qin Shuang (rule 5): her chopper is never written; e037's one spear (prop-changqiang-l1 appended) in s34, s36, s39.
- The horse (rule 41): one chestnut-red horse, its mane and tail the same deep red-brown, the felt saddle pad of the picked
  prop-zaohongma-an-l1 (e938 REVIEW 3 / fix6: H3 draws a high western saddle from any words when the picture is bare-backed; the pad
  is written as the picture shows it and the picture is sent wherever the horse is in the frame). Two riders on one horse in EVERY
  riding shot (原版必修): A-ling in front, Doctor Bai tied on behind her with her long grey sash wound twice round both their waists,
  both his arms round her waist, the medicine chest on his back, written in the first frame. Riding is seen side-on or from the side
  and behind, the riders from the waist up with the horse's head and neck, or in wides. The way back: the county town at the LEFT,
  Liuxi at the RIGHT; every riding shot goes from LEFT to RIGHT (s09-s12; s13 from behind and the side, the horse already reined in).
- Nothing hung (rule 33): Doctor Bai's lamp is one small clay oil lamp in his left hand (s01, s02, s04, s05), set down on the
  threshold by s07 (the script's hook goes); no signboard over the clinic; no milestone by the road (the script's blank stone of
  c13 goes); nothing on the barn.
- A-ling (rules 21, 22): no veil, no knife; her riding look (sleeves bound at the wrists with grey cloth strips, dark leg wraps); her
  long grey sash round her waist s01-s05, pulled off in s06, round both riders s08-s13, over her arm in s16, laid on the bed in s22;
  Xu Yan's old grey outer coat on her shoulders from s23, folded in her hands in s30.
- Doctor Bai (bible 〈人物〉, first face): baidaifu-portrait-l1 (white topknot, beard trimmed short at the chin; the portrait smiles a
  little, so every serious shot writes his lips pressed or moving between words); voice Rasalgethi (e938 a28 143 Hz).
  build-r2.py's EN gains "baidaifu": "Doctor Bai" (gen-dh.mjs's name for him; he speaks on screen for the first time).
- The guard captain (bible 〈人物〉): duizhang-portrait-l1 appended by mkspec.py (gen-dh.mjs / pilot.py know no live portrait for
  him; "duizhang" is a MINOR, as e938). Voice Iapetus.
- The village man who shouts (s36) is seen only from behind, his line a recording (MINOR "cunmin", Sadaltager, not in the frame's
  characters); Elder Han and Doctor Bai never in one scene; Qian Yuanwai the only portly round face.

THE AXES (rules 29, 42: the pictures decide):
- The east street by night (set-yiguan-men-ye-l1 and e938's crops -men, -jie): the stone-paved street running away to its far end
  at the LEFT, the shut plank shopfronts under deep eaves on the RIGHT; the clinic is the nearest two-leaf plank door with two stone
  steps and a square stone hitching post at its left. A-ling on the top step, Doctor Bai coming out of the doorway (right); the
  captain, the crossbowmen and the torch up the street toward its far end (left). The horse rides off toward the RIGHT edge (the
  near end of the street, behind the camera's side), the way back to Liuxi.
- The road by night (set-guandao-ye-l1 and e938's crops -ce2, -shu): a long line of tall dark poplars across the frame, the flat dark
  field before it; the horse gallops from the LEFT edge to the right, side-on. s13: the whole picture, the road running straight
  away between the poplars toward the moon; one small warm light far down the road (the Xu window, the only light ahead).
- The sickroom (set-xujia-tangfang-kong-l1 by night, -kong-chen-l1 at first light, their crops -chuang, -men, -zhen and this
  episode's quilt crop -bei): the plank door at the LEFT, the bed against the back wall under the small window, its pillow end at
  the RIGHT, the floor before the whole bed clear, a small low stool with one white candle in the corner at the foot of the bed
  (LEFT): its one small flame by night, unlit at first light. People come in through the door at the left (A-ling and Doctor Bai
  s16, Qin Shuang s34). Xu Yan sits on the near edge of the bed by the pillow end; Doctor Bai sits on the near edge of the bed at
  the pillow end when Xu Yan stands (s17-s21, s35); A-ling sits on the near edge of the bed at its foot by the stool, her head
  against the bedpost of the foot (the script's 「床尾的矮凳」: the stool holds the candle in the picture). The script's 「屋門在右」
  and 「桌上的油燈」 are turned the picture's way: the candle on the stool is the room's one light; Xu Yan lifts it in s17.
- The barn front in the early morning (set-gucang-wai-l1 and this episode's crops -men, -qiang, -tian): the low barn of grey
  weathered planks at the RIGHT, its two plank leaves swung back flat against its front on both sides of the dark doorway, a broad
  strip of trampled earth before it (lower right), the flooded field of young rice seedlings across the left half, dry ploughed
  fields beyond, small village houses and low hills far away, a big tree behind the barn; the low warm sun from the right. Diao Qi
  kneels on the trampled earth before the barn doorway; the people stand on the trampled earth at its left, along the edge of the
  field; Qin Shuang steps in between (s39); everyone turns to the RIGHT at the end (Xu Yan arriving out of sight: e040 s1).

PLACES (gen-dh SET takes the FIRST pattern in its list order that matches the prompt):
- The sickroom: every LOC holds "first bedroom of the Xu farmhouse" -> dh-set-xujia-tangfang-t1 = pilot.py's newest
  set-xujia-tangfang (l2), which spec.json swaps for the -kong crops.
- The street, the road and the barn front: the LOC carries " below the deep pool" (POOLMARK) only so gen-dh sends set-shentan
  ("clinic", "official road" and "granary" would take set-yiguan / set-guandao / set-gucang, which have no live picture under those
  ids: pilot.py would stop); mkspec.py takes the words out of every d1 prompt (e934-e938's way). Every later fix of these shots must
  carry the same replacement.
Shared files: build-r2.py's EN gains "baidaifu": "Doctor Bai" (a new key only, every older episode rebuilds byte for byte).
gen-dh.mjs, pilot.py, cast.json untouched. The d1 prep (colab/runs/e939/extras.json, colab/runs/e939-live/{mkspec.py,spec.json,
PREP.md}, the scratchpad's e939prep/{prep939.sh,check939.py,build939.sh,rec939-slow.sh} and e939d1.sh) was written 2026-11-24.
"""
EP = 939  # internal working number; the published slug is zhong-tian-qu-qi-e039-r2
SLUG = "zhong-tian-qu-qi-e039-r2"
EP_TITLE = "她把大夫綁在身後回村，天亮小禾退燒（重製版 r2）"
OUTLINE_SECONDS = 208  # script.md: about 208 s, 40 shots (13 + 22 + 5)
TARGET_MINUTES = [3, 4]
TITLE = "「我看見有人推你。」阿令把大夫綁在身後連夜回村，小禾退燒，全村要吊死刁七｜種田娶妻打天下 第39集（重製版）"
DESCRIPTION = "隊長的手落到一半，醫館的門開了：白大夫提著油燈喝住弩手——你娘的咳嗽是誰半夜治好的？白大夫不會騎馬，阿令解下腰帶，把他綁在自己身後，連夜往柳溪狂奔，要他閉上眼睛從一數到一百。一碗藥一口氣餵完，阿令靠著床柱睡著，許硯把外衣蓋在她肩上。天亮，小禾的燒退了；阿令好感突破四十，系統還嫌一件外衣換得便宜。小禾醒來小聲說：哥，你落水那天，我看見有人推你——戴一頂綁紅繩的草帽。穀倉前，全村要把刁七吊死在田頭，刁七抬頭冷笑：柳溪的許秀才，要殺要放，你說。《種田娶妻打天下》第 39 集（重製版）。"
THUMB = ("有人推你", "s30")
CHARACTERS = ["baidaifu", "aling", "duizhang", "xuyan", "xiaohe", "qinshuang", "cunmin", "hanbo", "qianyuanwai", "diaoqi", "erniu", "xitong"]
MINOR = {
    "duizhang": {"id": "duizhang", "name": "守軍隊長",
                 "appearance": "East Asian man of about forty-five, a square face and a short black beard, hard steady eyes, black iron lamellar armour with small red studs over a dark undercoat, a round iron helmet with cheek flaps that leaves his whole face bare and a small tuft of red horsehair on its crown",
                 "voice": {"provider": "gemini", "name": "Iapetus", "style": "標準國語，咬字清楚，台北人平常說話的語調；四十五歲的縣城守軍隊長，男聲、低沉粗硬、發號施令，吼的時候一個字一個字砸出來"}},
    "cunmin": {"id": "cunmin", "name": "村民甲",
               "appearance": "East Asian man of about forty, broad-backed, in an undyed hemp short jacket and a cloth head wrap; seen only from behind",
               "voice": {"provider": "gemini", "name": "Sadaltager", "style": "標準國語，咬字清楚，台北人平常說話的語調；四十歲的莊稼漢，男聲、粗、怒吼，氣到發抖"}},
}
MUSIC = "one cue per scene: taut high strings at a dark clinic door released all at once as the door gives, then urgent drums as a rider ties an old doctor behind her, a light quick flute over galloping drums on a moonlit road of poplars, a warm long note at one small light far ahead; then a very soft piano by one small candle flame in a sickroom, one warm accent at first light as a fever breaks, one bright note for a reward, low dark strings at a child's whisper, one heavy accent on a red cord, drums coming in at a knock; then low drums and voices before a barn in the morning, turning to taut strings, held at the highest note and cut off unresolved; ancient Chinese rural drama, no vocals"

# Places.
POOLMARK = " below the deep pool"  # mkspec.py takes it out of every street, road and barn shot in d1 (gen-dh's SET needs "deep pool")
E1 = f"In the east street of the county town{POOLMARK} in the second watch of the same night"
ENIGHT = "cold blue moonlight on the stone paving, the deep eaves in black shadow, the other shopfronts shut and dark"
STREET = ("the stone-paved street running away to its far end at the left, a long row of shut plank shopfronts under deep tiled eaves "
          "along the right, the nearest one a two-leaf plank door with one wide low stone step along its foot and a square stone "
          "hitching post just left of it")  # set-yiguan-men-ye-l1
G1 = f"On the wide dirt road from the county town back to Liuxi{POOLMARK} before the third watch of the same night"
GNIGHT = "cold blue moonlight, the deep blue night sky, the long shadows of the poplars across the field"
ROOM = "In the first bedroom of the Xu farmhouse"
R_NIGHT = f"{ROOM} in the third watch of the same night"
R_DAWN = f"{ROOM} at first light the next morning"
RNIGHT = "the one small flame on the low stool at the foot of the bed the only warm light, the corners of the room deep in shadow, the small window dark blue"
RCANDLE = "the one small candle flame held up beside the bed the only warm light, the corners of the room deep in shadow, the small window dark blue"
RWARM = "warm candlelight from beyond the left edge of the frame the only warm light, the corners of the room deep in shadow, the small window dark blue"  # s18 (review 建議 4)
MORN = "cold grey-white first light from the small window, the room grey and still, the one white candle on the low stool at the foot of the bed, its wick dark and unlit"
ROOMLAY = ("the plank door at the far left, rough cracked plaster walls, a wooden bed against the back wall under the small window with "
           "its pillow end at the right and a pink quilted cover on it, the floor before the whole bed clear, a small low wooden stool "
           "with one white candle in the corner at the foot of the bed at the left")  # -kong / -kong-chen (e938 必改 1)
B1 = f"Before the old plank barn at the edge of the Liuxi fields{POOLMARK} in the early morning of the next day"
BMORN = "low warm golden morning sunlight from the right, long shadows across the trampled earth, a clear pale blue sky"
BARN = ("the low old barn of grey weathered planks at the right under its pitched plank roof, its two plank door leaves swung back "
        "flat against its front on both sides of the dark doorway, a broad strip of trampled sun-warmed earth before it, the flooded "
        "field of young green rice seedlings in straight rows across the left half of the frame, dry ploughed fields beyond it, a row "
        "of small village houses and low blue hills far away, one big tree behind the barn")  # set-gucang-wai-l1
LOC = {
    "e": f"{E1}: the street exactly as in the picture: {STREET}; {ENIGHT}",
    "e_d": f"{E1}, at the two-leaf plank door; {ENIGHT}",
    "e_s": f"{E1}, in the street; {ENIGHT}",
    "g": f"{G1}; {GNIGHT}",
    "g_w": f"{G1}: the road exactly as in the picture: the wide pale dirt road running straight away between two long lines of tall dark poplars toward the far end, the bright moon high above; {GNIGHT}",
    "rx_c": f"{R_NIGHT}, at the bedside; {RNIGHT}",
    "rx_l": f"{R_NIGHT}, at the bedside; {RCANDLE}",
    "rx_w": f"{R_NIGHT}, at the bedside; {RWARM}",
    "rx_d": f"{R_NIGHT}, by the plank door; {RNIGHT}",
    "rx_x": f"{R_NIGHT}; {RNIGHT}",  # the insert s19: mkspec.py leaves only "Insert close-up" (rule 35)
    "rd_c": f"{R_DAWN}, at the bedside; {MORN}",
    "rd_d": f"{R_DAWN}, by the plank door; {MORN}",
    "b": f"{B1}: the place exactly as in the picture: {BARN}; {BMORN}",
    "b_g": f"{B1}, on the trampled earth before the barn; {BMORN}",
    "b_f": f"{B1}, at the edge of the rice field; {BMORN}",
}
LIGHT = {
    "night": "the cool moonlight stays unchanged",
    "lamp": "the small flame and the shadows stay unchanged",
    "morn": "the grey first light stays unchanged",
    "sun": "the low warm morning sunlight stays unchanged",
}
# bible rule 15: no "<X> speaks off screen" / "the system voice speaks off screen".
OFFSCREEN_SPEECH = False

# Repeated wording (each prop is one object, written the same way every time).
BAI = ("Doctor Bai, an old man of sixty-eight, lean, his white hair in a small topknot and his short white beard trimmed close at "
       "the chin, in a faded moon-white old long gown with a plain quilted cotton vest over it")
LAMP = "one small clay oil lamp with one flame held in his left hand"  # bible rule 33: never a lantern
CHEST = "one black lacquered medicine chest on a plain strap slung across his body"
ALING_R = ("A-ling, in her plain grey-white cotton dress tailored close at the waist with a long grey cloth sash, its long sleeves bound "
           "tight at both wrists with strips of grey cloth, dark cloth leg wraps below the hem of the dress, her long black hair pinned "
           "up with one plain wooden hairpin")  # her riding look, the sash still round her waist (s01-s05)
ALING_N = ("A-ling, in her plain grey-white cotton dress tailored close at the waist, its long sleeves bound tight at both wrists with "
           "strips of grey cloth, dark cloth leg wraps below the hem of the dress, her long black hair pinned up with one plain wooden "
           "hairpin")  # the sash off her waist (s06 on)
SASH = "her long grey cloth sash"
WISPS = "a few strands of her hair blown loose from the hairpin"
COAT_ON = "an old grey cloth outer coat laid over her shoulders"  # Xu Yan's (s23 on)
HORSE = ("one chestnut-red horse, its mane and tail the same deep red-brown as its body, a plain dark leather bridle and a folded "
         "dark grey-brown felt saddle pad girthed with rope")  # rule 41, prop-zaohongma-an-l1 (e938 fix6)
TWO_UP = ("A-ling in front, in her plain grey-white cotton dress, its long sleeves bound tight at both wrists with strips of grey cloth, "
          "dark cloth leg wraps below its hem, her black hair pinned up with one plain wooden hairpin, and Doctor Bai tied on behind her, "
          "his white hair in a small topknot, in his faded moon-white gown and quilted vest, her long grey cloth sash wound twice round "
          "both their waists and knotted at her front, both his arms wrapped round her waist, the black lacquered medicine chest on his "
          "back")
CAPTAIN = ("the guard captain, a middle-aged man with a square face and a short black beard, in black iron lamellar armour with small red "
           "studs, a round iron helmet with cheek flaps that leaves his whole face bare and a small tuft of red horsehair on its crown")
CAP_KNIFE = "one short plain single-edged knife with a dark wooden grip back in its plain dark sheath at his left hip"
XBOW = "one plain wooden crossbow held level in both hands"
XBOWMEN = ("six crossbowmen in the same black iron lamellar armour and plain iron helmets, their faces in the shadow of their helmets, "
           f"each with {XBOW}")
TORCHMAN = "one more guard in black armour holding up one burning torch in his right hand"
XU_COAT = ("Xu Yan, in his faded blue-grey scholar's robe patched at one elbow, pale white lime powder dusted over the lower half of the "
           "robe, with an old grey cloth outer coat worn loose over his shoulders")  # by night (s14-s23)
XU_ROBE = ("Xu Yan, in his faded blue-grey scholar's robe patched at one elbow, pale white lime powder dusted over the lower half of the "
           "robe")  # the coat on A-ling's shoulders (s23 on)
XIAOHE_BED = ("little Xiaohe, eight years old, lying on her back in the bed under the pink quilted cover drawn up to her chest, her whole face "
              "flushed deep red with fever, strands of her hair stuck to her forehead, her lips dry and cracked, one folded damp white cloth "
              "across her forehead, a small woven straw rabbit lying beside her pillow")
XIAOHE_BED_SHORT = "little Xiaohe, eight years old, lying in the bed under the pink quilted cover, her face flushed deep red, a folded damp white cloth on her forehead"
XIAOHE_WELL = ("little Xiaohe, eight years old, lying in the bed under the pink quilted cover, her face its own healthy colour again, her "
               "breathing slow and even, her forehead bare, a small woven straw rabbit lying beside her pillow")
XIAOHE_UP = ("little Xiaohe, eight years old, sitting half up against the pillow in the bed under the pink quilted cover, her face its "
             "healthy colour again, a small woven straw rabbit held in both her hands against her chest")
CLOTH = "one folded damp white cloth"
BASIN = "one shallow wooden basin of water"
BOWL = "one coarse clay medicine bowl of dark warm medicine"
QIN = ("Qin Shuang, in her fitted dark brown cross-collared short jacket cinched with a wide plain leather belt, fitted black "
       "trousers and leather boots, her sleek high ponytail tied with black cord")  # rule 5: nothing in her belt
SPEAR = "one long spear: a plain wooden shaft taller than she is, a small plain iron spearhead, the shaft bare below the head"  # e037's
HAN = ("Elder Han, in his faded washed-out grey cotton long robe, his long white beard down to his chest, his white hair in a small "
       "topknot")
STAFF = "one polished old bamboo walking staff"
QIAN = ("Qian Yuanwai, short and portly, in his dark gold silk cross-collared robe woven with small round medallions, three gold rings "
        "on his fingers")
DIAO = ("Diao Qi, in his ragged rough earth-brown homespun tunic with frayed cuffs, black leg wraps, a thick hemp rope wound round his "
        "body binding both his arms behind his back, a streak of pale white lime powder across one cheek")
NOOSE = "one thick hemp rope looped round his neck"
ERNIU = "Wang Erniu, in his coarse brown hemp short jacket with rolled sleeves, both his big hands at his sides"
# the people at the barn (rule 34): each a colour and an age, never the leads' colours
SHOUTER = "a broad-backed man of about forty in an undyed hemp short jacket and a cloth head wrap, seen only from behind"
ROPEMAN = "a lean young man in a faded rust-red jacket, seen only from behind, holding the other end of that rope taut in both hands"
FOLK = ("an old man with a white topknot in a faded grey long robe leaning on a bamboo staff, seen only from behind, a thin middle-aged "
        "man in charcoal grey, a boy of fifteen in faded indigo, a stout man of fifty in dark olive green, a middle-aged woman in dark grey with a faded indigo head cloth")
TWO_FOLK = "two men of the village seen only from behind, one in charcoal grey and one in dark olive green"
HANDS = "their hands hold only what is described here"
SILENT_HE = "He says nothing in this shot: his lips stay pressed together from the first frame to the last, his jaw still, no talking, no mouthing words"
NOBODY = "Throughout the shot the set layout stays as it is. The pictures fix the place and the objects only, never the mood. "
ALING_EDGE_COAT = ("at the left edge of the frame, cut by it, soft and out of focus, only the back of a young woman's head with black hair "
                   "pinned up with one plain wooden hairpin and one shoulder under an old grey cloth outer coat, toward us the whole shot")
ALING_EDGE_RIDE = ("in the lower left foreground, cut by the edge of the frame, soft and out of focus, only the back of a young woman's head "
                   "with black hair pinned up with one plain wooden hairpin, toward us the whole shot")
BAI_EDGE = ("at the right edge of the frame, cut by it, soft and out of focus, only the white hair in a small topknot and one shoulder in "
            "a faded moon-white gown of an old man seen from behind, the warm glow of a small oil lamp low beside him, toward us the "
            "whole shot")


def quiet(who, pr="his", plural=False):
    verb = "say" if plural else "says"
    return f"{who} {verb} nothing in this shot: {pr} lips stay pressed together from the first frame to the last, no talking, no mouthing words"


def off(side, what, he="he", only=True):
    """A line to someone outside the frame: the gaze, that side set only, and the only person (rule 31). only=False when someone
    else is in the frame (review 必改 5: "the only person" and "exactly N people" never in one prompt)."""
    edge = f"the {side} edge of the frame"
    tail = f", and {he} is the only person in the frame" if only else ""
    return (f"toward someone out of sight beyond {edge}, never the lens; that side of the frame is only {what} all the way to the "
            f"edge{tail}")


SHOTS = [
    # ---- scene 1: the clinic door in the east street, the second watch (38->39), and the road back to Liuxi.
    dict(chapter="醫館門口與回程的官道", loc="e_d", cam="Medium shot, slow push in", chars=["baidaifu", "aling"], night="night",
         comp=f"medium shot at the two-leaf plank door from the street side, the door at the right: both plank leaves already pushed inward from the first frame, warm lamplight glowing in the doorway and spilling onto the stone step, exactly as in the picture; on the threshold, {BAI}, {LAMP}, already stepping out from the first frame, framed from the waist up, his face three-quarter to screen left toward the street, never the lens; fierce and commanding, not smiling: white brows drawn hard, eyes blazing, mouth wide between shouted words; at the left, on the stone step, {ALING_R}, {WISPS}, already stepped aside to the left of the doorway from the first frame, side-on, framed from the waist up, her face toward him, her lips closed, not smiling, never the lens; at the left edge of the frame, soft, the head and neck of {HORSE}, tied by its reins to the square stone hitching post, well apart from her; {HANDS}; exactly two people and one horse",
         lines=[("baidaifu", "放下！她是來求醫的，誰敢放箭！", "一聲喝住")],
         motion=f"Doctor Bai strides out over the threshold onto the stone step, thrusts the little lamp forward and sweeps his flat right hand out toward the street at the left as he shouts; {quiet('A-ling', 'her')}",
         zh="中景、慢推（送 `set-yiguan-men-ye-men-l1`：最近那間兩扇木門板、兩級石階、門左方石拴馬樁；圖上門板關著，**門板往裡推開寫在文字**，付費改圖列在 PREP §5，不做）：**接點 38→39（照第 38 集定版成片 `e938-live.mp4` 最後 16 秒）**：同一刻，第 38 集停在隊長舉手『放——』切黑；本鏡第一格兩扇門板已經往裡推開、門內暖光，白大夫左手一盞**陶油燈**（聖經第 33 條：稿子的燈籠改油燈）跨出門檻、油燈往前一舉、右手平掌朝畫左的街口一揮（一個動作），一聲喝住；阿令已經讓到門口左邊、在上一級石階、嘴閉著。白大夫第一次露臉：送 `baidaifu-portrait-l1`（定妝照嘴角微揚，嚴肅寫在表情）。稿子『前景是阿令按在門板上的手』：門已經推開，不寫。**獨立審稿後**：必改 1（A）改送付費改圖的裁切 `set-yiguan-men-ye-kai-men-l1`（門板往裡推開、門內暖光；`e939qwen.sh` 還沒跑），建議 13 畫左緣加拴在樁上的馬頭頸（加送原向的配鞍馬圖），建議 2 石階寫一級"),
    dict(loc="e_s", cam="Medium wide shot from behind, slow push in", chars=["baidaifu", "duizhang"], nospeak=["baidaifu"], night="night",
         comp=f"medium wide shot from behind, up the street toward its far end at the left: in the right foreground, {BAI}, {LAMP}, seen only from behind on the stone step, framed from the waist up, the back of his head toward us the whole shot, his face turned up the street, never the lens; far up the middle of the stone-paved street, small, {CAPTAIN}, framed full figure, his right hand still raised high above his helmet from the first frame, his face toward the clinic steps, his lips closed, not smiling, never the lens; behind him in a ragged line, {XBOWMEN}, seen side-on and from the front at a distance, small, and {TORCHMAN}; {HANDS}; exactly nine people, the old man in the foreground seen only from behind",
         lines=[("baidaifu", "張隊長，你娘的咳嗽，是誰半夜出診治好的？", "盯著隊長，慢而有把握")],
         motion=f"Doctor Bai steps down off the stone step onto the paving and stands still, the little lamp held out before him, while far up the street the guard captain's raised hand stays frozen in the air; the guard captain and the crossbowmen say nothing in this shot: their lips stay pressed together from the first frame to the last, no talking, no mouthing words; the old man in the foreground keeps the back of his head toward us the whole shot",
         zh="中景偏全（從背後）、慢推（送 e938 的 `set-yiguan-men-ye-jie-l1`：石板街往左邊遠處；加送 `duizhang-portrait-l1`）：稿子『過肩（白大夫肩後拍街口）』：過肩前景照拍法 2 不點名，但說話的是他：改成從背後拍他（送定妝照、`nospeak`、頭不轉，第 38 集唐小棠背影的做法），他在右前景下一級石階、油燈舉在身前，往下走一級停住（一個動作）；街遠處隊長右手第一格還舉在頭頂、停在半空（接第 38 集最後一格），身後六個弩手排一排、一個守軍舉一支火把（拍法 37）；九個人（→ 答在 s03）"),
    dict(loc="e_s", cam="Medium shot, slow push in", chars=["duizhang"], night="night",
         comp=f"medium shot in the street: {CAPTAIN}, standing in the middle of the line, {CAP_KNIFE}, framed from the waist up, his right hand still raised high above his helmet from the first frame, his face lowered three-quarter to screen right, his eyes on the clinic steps beyond the right edge of the frame, never the lens; shaken and humbled, not smiling: brows lifting, eyes lowered, lips moving low between words; behind him at the left, soft and out of focus, two crossbowmen in the same black armour and iron helmets seen side-on, their faces in the shadow of their helmets, each with {XBOW}; {HANDS}; exactly three people",
         lines=[("duizhang", "是您……弩都放下，這人白大夫認了。", "低頭")],
         motion="the guard captain lowers his raised right hand slowly and sweeps it down and back toward the line behind him as he speaks, and the two crossbowmen behind him lower their crossbows until they point at the paving",
         zh="中景、慢推（送 `-jie-l1`；加送隊長圖）：隊長（同一張臉、同一頂盔，原版必修）右手第一格還舉著，慢慢放下、往身後一揮，身後兩個弩手把弩垂下（一個動作；稿子『把短刀收回腰間』在第一格完成：短刀已經插回左腰的刀鞘）；低頭說（答 s02）；不笑"),
    dict(loc="e_d", cam="Medium shot, slow push in", chars=["aling", "baidaifu"], night="night",
         comp=f"medium shot on the stone step of the two-leaf plank door, the door at the right, both plank leaves standing pushed inward with warm lamplight in the doorway, exactly as in the picture: at the left, {ALING_R}, {WISPS}, already turned round to face him from the first frame, side-on, framed from the waist up, out of breath, her face in profile to screen right toward him, never the lens; pleading under her breath, not smiling: brows drawn, eyes fixed on his, lips moving low and quick between breaths; at the right, on the step before the doorway, {BAI}, {LAMP}, framed from the waist up, his face three-quarter to screen left toward her, never the lens, his lips closed, not smiling; {HANDS}; exactly two people",
         lines=[("aling", "柳溪許家的妹妹燒了一天一夜，求您救她。", "喘，很輕")],
         motion=f"A-ling steps up close and grips the sleeve of his gown in her right hand as she speaks; {quiet('Doctor Bai')}",
         zh="中景、慢推（送 `-men-l1`；門板推開寫在文字）：阿令第一格已經轉過身面向白大夫（左），往前一步抓住他的袖子（一個動作），喘、很輕地說；白大夫在右、門口、油燈、嘴閉著。兩人。獨立審稿必改 1：改送 `-kai-men-l1`"),
    dict(loc="e_d", cam="Medium close-up, slow push in", chars=["baidaifu"], night="night",
         comp=f"medium close-up of {BAI}, on the stone step before the doorway, framed from the waist up with space above his head, {LAMP} held low at his side, his face three-quarter to screen left {off('left', 'the dark plank shopfronts and the moonlit stone paving')}; troubled, not smiling: brows knotted, mouth turned down, lips moving between words; behind him, soft, only the plank leaves pushed inward and the warm lamplight of the doorway; {HANDS}",
         lines=[("baidaifu", "柳溪？騎馬也要半個時辰，老夫這把骨頭不會騎馬。", "皺眉")],
         motion="Doctor Bai slaps his flat right hand once on his own thigh and shakes his head slowly as he speaks",
         zh="中近景（腰以上：拍大腿的手要在框裡）、慢推（送 `-men-l1`；稿子『身後只有醫館的門板與燈光』）：白大夫拍一下自己的大腿、慢慢搖頭（一個連續的手勢），皺眉，朝畫左外看不到的人（阿令，不寫人，拍法 31）說；不笑。獨立審稿必改 1：改送 `-kai-men-l1`"),
    dict(loc="e_d", cam="Medium shot, slow push in", chars=["aling"], night="night",
         comp=f"medium shot on the stone step: {ALING_R}, {WISPS}, standing side-on, framed from the waist up, both her hands already at the knot of the long grey sash at her waist from the first frame, her face three-quarter to screen right {off('right', 'the dark plank leaves of the doorway', he='she')}; cold as well water, not smiling: eyes level and steady, brows still, lips moving evenly between words; behind her, soft, the shut plank shopfronts and the moonlit street; {HANDS}",
         lines=[("aling", "不用您會騎。您坐我身後，我把您綁牢。", "冷得像井水")],
         motion="A-ling pulls the long grey sash free from her waist in one long sweep and snaps it straight between her two hands as she speaks",
         zh="中景、慢推（送 `-men-l1`）：阿令兩手第一格已經在腰帶結上，一把抽出灰布長腰帶、在兩手間拉直（一個動作），冷得像井水，朝畫右外看不到的人（白大夫，不寫人）說；白大夫不入鏡（稿子『白大夫嘴閉著，愣住』交給下一鏡）"),
    dict(loc="e_d", cam="Medium shot, slow push in", chars=["baidaifu"], night="night",
         comp=f"medium shot in the doorway of the two-leaf plank door, both plank leaves standing pushed inward, exactly as in the picture: {BAI}, already stepped back out onto the stone step from the first frame, framed from the waist up, the black lacquered medicine chest already held by its strap in his right hand from the first frame, the small clay oil lamp already set down on the threshold behind him, its flame steady, his face three-quarter to screen left {off('left', 'the dark plank shopfronts and the moonlit paving')}; resolved, not smiling: jaw set, brows lifted, lips moving firmly between words; behind him, soft, the warm lamplight of the doorway; {HANDS}",
         lines=[("baidaifu", "好，老夫豁出去了，藥箱我自己背。", "豁出去")],
         motion="Doctor Bai swings the strap of the medicine chest up over his head and across his body so the chest settles on his back, and draws one deep breath as he speaks",
         zh="中景、慢推（送 `-men-l1`）：白大夫第一格已經把棉背心穿好、右手提著黑漆藥箱的背帶、陶油燈已經放在身後的門檻上（2026-11-06 審稿『燈籠掛回門內的鉤子』：拍法 33 不掛，改成放在門檻上，油燈從此不見；稿子『從門內拿出藥箱』在第一格完成），把背帶往頭上一甩斜挎、深吸一口氣（一個動作）；豁出去地說（答 s06）。稿子前景『門內的藥櫃一角』：沒有門內的圖，不寫。獨立審稿必改 1：改送 `-kai-men-l1`；建議 11：『背心穿好』拿掉（定妝照是絎棉短襖）"),
    dict(loc="e_d", cam="Medium shot, slow push in", chars=["aling", "baidaifu"], night="night",
         comp=f"medium shot from the side before the stone step, behind them, soft, the clinic's two plank leaves still pushed inward and the warm glow of its doorway, exactly as in the picture: {HORSE}, standing side-on with its head toward the right, already untied from the post; on its back, {TWO_UP}, framed from the waist up with the horse's head and neck before them, already mounted from the first frame; A-ling's face three-quarter to screen right, never the lens, calm and hard, not smiling, lips moving evenly between words; Doctor Bai behind her with his eyes squeezed shut, his white brows knotted, his lips pressed together, not smiling, never the lens; {WISPS}; {HANDS}; exactly two people and one horse",
         lines=[("aling", "抓緊我的腰，路上千萬別往下看。", "淡")],
         motion=f"A-ling pulls the last knot of the sash at her front hard and tight with both hands and glances back over her shoulder at him as she speaks; {quiet('Doctor Bai')}",
         zh="中景（側面，兩人腰以上加馬頭頸，聖經第 41 條）、慢推（送 `-men-l1`；加送配鞍馬 `prop-zaohongma-an-l1`：**毛氈鞍墊、麻繩肚帶照圖**，第 38 集 fix6：只送光背馬圖 H3 會畫高鞍頭西式鞍）：兩人第一格已經在馬上（原版必修：白大夫在馬背上）、灰布腰帶在兩人腰上繞兩圈、白大夫兩手抱她的腰、藥箱在背上、緊閉雙眼；阿令把最後一個結拉緊、回頭看他一眼（一個動作），淡淡地說；馬頭朝右（回程由左往右）。獨立審稿必改 1：改送 `-kai-men-l1`，身後寫醫館兩扇門板仍往裡推開、門口暖光（照新圖）；建議 1：馬圖改送翻成頭朝右的 `prop-zaohongma-an-r-l1`"),
    dict(loc="e", cam="Wide shot, slow push in", chars=["aling", "baidaifu"], night="night", act=3,
         comp=f"wide shot down the street, like the picture: the stone-paved street running away to its far end at the left, the shut plank shopfronts under deep eaves along the right, the square stone hitching post just left of the nearest door, the two plank leaves of that door pushed inward and its doorway glowing warm, exactly as in the picture; before the stone step of the nearest door, {HORSE}, already bursting into a run from the first frame, its head toward the right, carrying {TWO_UP}, framed full figure; far up the street at the left, small and still, {CAPTAIN}, six crossbowmen in the same black iron lamellar armour and plain iron helmets, their faces in the shadow of their helmets, each holding one plain wooden crossbow pointed down at the paving, seen side-on and from the front at a distance, and {TORCHMAN}; {HANDS}; exactly ten people and one horse",
         motion=f"A-ling snaps the reins and the horse lunges off from the step and gallops down the street along the foot of the shopfronts toward us and out past the lower right corner of the frame, the stone paving ringing, while far up the street the men in black armour stand still; {quiet('A-ling, Doctor Bai and the men in black armour', 'their', plural=True)}",
         zh="全景、慢推（送整張 `set-yiguan-men-ye-l1`；加送配鞍馬圖、隊長圖）：稿子『全景、跟拍（往右）』：街往左邊遠處，**往右＝往柳溪的方向**（回程由左往右），馬從醫館階前起跑、往畫右外衝出去（一個動作；跟拍會把街轉掉，改慢推）；街遠處隊長、六個弩手（弩垂著）、舉火把的守軍站著不動（遠、小、臉在盔影裡，拍法 34）；兩人一馬、十個人。剪接剪在衝出畫右的一半。無台詞。獨立審稿後：必改 1 改送整張付費改圖 `set-yiguan-men-ye-kai-l1`；建議 2：照圖寫成沿店門往鏡頭右下角衝出去、拴馬樁在最近那扇門左邊"),
    dict(loc="g", cam="Medium shot, tracking", chars=["aling", "baidaifu"], night="night",
         comp=f"medium tracking shot alongside the galloping horse, side-on: {HORSE} at full gallop toward the right, carrying {TWO_UP}, framed from the waist up with the horse's head and neck before them; A-ling crouched low over its neck, {WISPS}, her face in profile to screen right, her eyes on the road ahead, her lips closed, not smiling, never the lens; Doctor Bai bouncing behind her, his white hair blown wild, his eyes squeezed shut, terrified, not smiling: mouth stretched wide between shaky words, never the lens; behind them, sliding past soft and dark, the line of tall poplars and the moonlit field; {HANDS}; exactly two people and one horse",
         lines=[("baidaifu", "慢、慢一點！老夫的骨頭要散了！", "閉著眼，聲音抖")],
         motion=f"the horse pounds on toward the right, Doctor Bai clamps his arms tighter round her waist and jolts with every stride, the chest bouncing on his back; {quiet('A-ling', 'her')}",
         zh="中景（側面、兩人腰以上加馬頭頸）、**跟拍**（稿子『跟拍，由左往右，跟著馬』）（送 e938 的 `set-guandao-ye-shu-l1`：楊樹一排、乾田；加送配鞍馬圖）：**月夜官道**（原版必修：不是白天）：**回程一律由左往右**（聖經：縣城在左、柳溪在右）；白大夫綁在她身後、白髮被風吹亂、兩手死抓她的腰、藥箱在背上顛（一個動作的連續），閉著眼喊；阿令伏在馬頸、嘴閉著"),
    dict(loc="g", cam="Medium close-up, tracking", chars=["aling"], night="night",
         comp=f"medium close-up riding alongside, side-on: {ALING_N}, {WISPS}, riding {HORSE} at a gallop toward the right, framed from the waist up with the horse's neck and mane before her, her face in profile to screen right, never the lens; behind her shoulder, close and soft, the white hair and the squeezed-shut eyes of the old man tied on behind her, and his two hands gripping her waist, her long grey cloth sash wound twice round both their waists and knotted at her front; cool and unhurried, not smiling: eyes level, brows still, lips moving evenly between words; behind them, sliding past soft and dark, the poplars and the moonlit field; {HANDS}; exactly two people, the old man behind her seen only as his white hair, his shut eyes and his hands",
         lines=[("aling", "閉上眼睛，從一數到一百，就到了。", "淡淡的")],
         motion="A-ling turns her head a little toward her shoulder to speak to him and presses her heels into the horse's sides, and it stretches out faster",
         zh="中近景（腰以上加馬頸鬃毛）、跟拍（送 `-shu-l1`；加送配鞍馬圖）：稿子『近景、跟拍；阿令肩後露出白大夫的白髮與抓著她腰的手』：**白大夫一定在畫面裡**（原版必修），寫成她肩後虛焦的白髮、緊閉的眼、抓著她腰的兩手（不點名、不送他的圖，拍法 2）；阿令稍稍側頭、一夾馬腹（一個動作），淡淡地說"),
    dict(loc="g", cam="Medium close-up, tracking", chars=["baidaifu"], night="night",
         comp=f"medium close-up riding alongside, side-on, framed from the chest up, the top of the red-brown mane of {HORSE} bobbing at the bottom right corner: at the right edge, cut by it and soft, only the shoulder and the back of the pinned-up head of the young woman riding in front, turned forward toward the right; just behind her, {BAI}, tied on behind her with her long grey cloth sash wound twice round both their waists and knotted at her front, his chin pressed against the back of her shoulder, his face three-quarter toward us, the strap of the medicine chest across his chest, his eyes shut tight from the first frame, never the lens; scared and counting, not smiling: brows knotted, lips moving fast between counted words; behind them, sliding past soft and dark, the poplars and the night sky; {HANDS}; exactly two people and one horse, the one in front seen only as her shoulder and the back of her head",
         lines=[("baidaifu", "九十八、九十九……老夫數完了，還沒到嗎？", "數不下去")],
         motion="Doctor Bai's lips keep counting, and at the end he lifts one eyelid and peeks past her shoulder",
         zh="中近景（側面）、跟拍（送 `-shu-l1`；加送翻成頭朝右的配鞍馬圖）：**獨立審稿必改 3**：原寫『前景她的後腦、後面他的臉』，同向騎馬拍不出來、也沒有馬與腰帶；改側面：畫右緣虛焦是她的肩與後腦（不點名、不送圖，拍法 2），白大夫綁在她身後、腰帶繞兩人腰兩圈、下巴抵在她肩後、臉朝我們四分之三、閉眼數數，數到最後掀起一邊眼皮偷看（一個動作）（→ 答在 s13）；畫右下角露出馬鬃"),
    dict(loc="g_w", cam="Wide shot from behind, slow push in", chars=["aling", "baidaifu"], night="night",
         comp=f"wide shot from behind and a little to the side on the road, like the picture; in the middle of the road, {HORSE}, already reined in to a walk from the first frame, seen from behind and the side, carrying {TWO_UP}, framed full figure, small; far ahead at the very end of the road between the dark poplars, one tiny warm light of a window, the only light ahead; {HANDS}; exactly two people and one horse",
         lines=[("aling", "到了。前面就是柳溪，許家的燈還亮著。", "鬆一口氣，仍淡")],
         motion=f"A-ling raises her flat right hand toward the tiny light far ahead and turns her face back over her shoulder toward him as she speaks; {quiet('Doctor Bai')}",
         zh="全景（從背後與側面）、慢推（送整張 `set-guandao-ye-l1`：路往遠處、兩排楊樹、月亮；加送配鞍馬圖）：稿子『大全景、跟拍、空白石碑、坡頂、坡下黑黑的柳溪村』：**石碑不寫**（拍法 33）；圖上沒有坡、沒有村子，照圖寫路的盡頭『一盞很小的暖燈』（許家的窗）；馬第一格已經放慢成走，阿令平掌往前一指、回頭對他說、再催馬（一個動作的連續）；兩人都在馬上（原版必修）。官道只有月光、天全黑（原版建議）。本場結尾"),
    # ---- scene 2: the first bedroom of the Xu farmhouse, the third watch to first light.
    dict(chapter="許家屋內，天亮前到天亮", loc="rx_c", cam="Close-up, slow push in", chars=["xuyan", "xiaohe"], night="lamp",
         comp=f"close-up at the bedside: {XU_COAT}, sitting on the near edge of the bed by its pillow end, framed from the chest up, his eyes red-rimmed and heavy, {CLOTH}, freshly wrung, already in his right hand just above her forehead from the first frame, his face lowered three-quarter to screen right toward her, never the lens; hoarse and worn out, not smiling: brows knotted, lips moving low between words; along the bottom of the frame, little Xiaohe, eight years old, lying in the bed under the pink quilted cover, her face flushed deep red, her forehead bare and damp, her eyes shut, her lips closed; behind him, soft, only the dark blue window and the dark wooden bed head; {HANDS}; exactly two people",
         lines=[("xuyan", "小禾，再撐一下，阿令就快回來了。", "整夜沒睡，啞")],
         motion=f"Xu Yan lays the damp cloth gently across her forehead and smooths it down with his palm as he speaks; {quiet('little Xiaohe', 'her')}",
         zh="近景、慢推（送 e938 的 `set-xujia-tangfang-kong-zhen-l1`：夜裡枕頭那頭、床頭欄、牆；聖經第 42 條：唐小棠房間的圖，e938 必改 1 的付費改圖）：許硯（舊灰外衣、袍子下半截石灰白粉，接第 38 集）坐在床沿枕頭那頭（近景不寫跪），眼睛布滿血絲；右手第一格已經拿著剛擰好的濕布（e938 建議 1：擰水那幾個小動作在第一格前完成），蓋上她的額頭、抹平（一個動作），啞著嗓子說；畫面下緣小禾通紅的臉、濕布、嘴閉著（床上一直有她，原版必修）。獨立審稿必改 6：小禾額頭不寫濕布（只有許硯手上那一塊）"),
    dict(loc="rx_c", cam="Close-up, slow push in", chars=["xuyan"], night="lamp",
         comp=f"close-up of {XU_COAT}, at the bedside, framed from the chest up with space above his head, his face already turned three-quarter to screen left from the first frame, his eyes on the shut plank door beyond the left edge of the frame, never the lens; he is the only person in the frame; startled hope, not smiling: eyes wide, brows lifted, lips moving quickly between words; behind him, soft, only the dark blue window and the plaster wall; {HANDS}",
         lines=[("xuyan", "外面有馬蹄聲……是阿令，她帶人回來了！", "猛地抬頭")],
         motion="Xu Yan's head jerks up toward the door and he pushes himself half up off the edge of the bed with one hand as he speaks",
         zh="近景、慢推（送 `-kong-chuang-l1`：夜裡的床、窗）：許硯抬頭朝畫左外的門（聖經：門在左；看的是門，不寫人），撐著床沿站起一半（一個動作；稿子『濕布掉進水盆』交給音效）。獨立審稿必改 4：改送沒有床的 `-kong-chuang2-l1`（窗與後牆）"),
    dict(loc="rx_d", cam="Medium shot, tracking", chars=["baidaifu", "aling"], night="lamp",
         comp=f"medium shot by the plank door at the left, the edge of the door frame soft in the left foreground: the plank door at the left shut behind them; just inside the door, already in from the first frame, {ALING_N}, {WISPS}, the long grey sash draped over her left arm, her right arm under his elbow holding him up, framed from the waist up, her face toward him, her lips closed, not smiling, never the lens; beside her, {BAI}, the black lacquered medicine chest on its strap on his back, unsteady on his feet, framed from the waist up, his face three-quarter to screen right toward the bed beyond the right edge of the frame, never the lens; urgent and out of breath, not smiling: brows knotted, lips moving fast between words; the warm light of the one small flame on the low stool at the foot of the bed falling on them; behind them, soft, the cracked plaster wall; {HANDS}; exactly two people",
         lines=[("baidaifu", "病人在哪？快把燈拿近一點。", "喘")],
         motion=f"Doctor Bai finds his feet, straightens and takes one step toward the bed as he speaks, A-ling letting go of his arm; {quiet('A-ling', 'her')}",
         zh="中景、跟拍（送 `-kong-men-l1`：左邊木板門、裂紋牆、矮凳與燭火、床尾；前景門框）：阿令（袖口紮緊、灰布腰帶搭在左臂，稿子 c15 進門解開）扶著白大夫（藥箱在背上）從左邊的門（聖經第 42 條）進來，第一格已經在門內、門在身後關著（獨立審稿必改 2：圖上的門是關的）；白大夫站穩、往床走一步（一個動作），喘著說（→ 答在 s17）；看的是畫右外的床（東西，拍法 31）"),
    dict(loc="rx_l", cam="Medium shot, slow push in", chars=["xuyan", "xiaohe", "baidaifu"], night="lamp",
         comp=f"medium shot at the bedside: {XU_COAT}, standing beside the bed, framed from the waist up, the one white candle in a plain clay dish already lifted from the low stool and held up in his right hand from the first frame, its small flame lighting the pillow, his face three-quarter to screen right toward the old man, never the lens; strained, not smiling: brows knotted, lips moving tight between words; in the bed under the small window, {XIAOHE_BED}, her eyes shut, her lips closed; at the right, by the pillow end, {BAI}, the medicine chest on his back, already lowering himself onto the near edge of the bed from the first frame, framed from the waist up, his face toward the girl, his lips closed, not smiling, never the lens; {HANDS}; exactly three people",
         lines=[("xuyan", "在這裡，燒了一天一夜，藥都壓不住。", "急")],
         motion=f"Xu Yan holds the candle down close beside the pillow so its small light falls on her flushed face, and Doctor Bai sits down on the edge of the bed by the pillow; {quiet('Doctor Bai and little Xiaohe', 'their', plural=True)}",
         zh="中景、慢推（送 `-kong-chuang-l1`）：稿子『許硯從桌上舉起油燈』：圖上沒有桌子、屋裡唯一的光是床尾矮凳上那一根白蠟燭（聖經〈場景〉：病房的燈寫凳上那一朵燭火），第一格許硯已經把蠟燭（素陶燭盤）從矮凳拿起、舉在右手，往枕邊一湊照亮小禾的臉（一個動作）；**床上一直有小禾**（原版必修：白大夫進門時床是空的）；白大夫在右、枕頭那頭坐到床沿（e938 必改 1 後床前空著）。三人（答 s16）"),
    dict(loc="rx_w", cam="Close-up, slow push in", chars=["baidaifu", "xiaohe"], night="lamp",
         comp=f"close-up at the pillow end of the bed: {BAI}, sitting on the edge of the bed, framed from the chest up, his right hand already laid on the girl's small wrist on the quilt from the first frame, feeling her pulse, his eyes shut, his face lowered three-quarter to screen right toward her, never the lens; grave and careful, not smiling: brows knotted, lips moving slowly and clearly between words; along the bottom of the frame, {XIAOHE_BED_SHORT}, her eyes shut, her lips closed; the warm candlelight falling on them from the left; behind him, soft, only the dark wooden bed head and the plaster wall; {HANDS}; exactly two people",
         lines=[("baidaifu", "燒得太久了。先退熱，其他的再慢慢調。", "慢而清楚")],
         motion=f"Doctor Bai's eyes come up from under his white brows, he lifts his hand from her wrist and lays his flat palm on her hot cheek beside the cloth as he speaks; {quiet('little Xiaohe', 'her')}",
         zh="近景、慢推（送 `-kong-zhen-l1`：枕頭那頭、床頭欄；稿子『身後只有床柱與油燈』：燭火虛焦在畫緣）：白大夫閉眼、手第一格已經搭在小禾的手腕上（拍法 32：不寫兩指、指尖，寫手搭在腕上），睜眼、手從腕上移到她發燙的臉頰（一個動作；稿子『掀開濕布摸一下』：濕布照舊留在額頭，接 s20），慢而清楚地說。獨立審稿建議 4：燭火沒人拿，改寫『暖光從畫左外照過來』"),
    dict(loc="rx_x", cam="Insert close-up, slow push in", chars=[], night="lamp",
         comp="insert close-up from slightly above, the very first frame is already a close view of one black lacquered medicine chest with its lid lifted standing on a pink quilted cover, and two old hands in faded moon-white cuffs tipping a small fold of plain oiled paper over one coarse clay bowl, fine brown medicine powder sliding from it into the bowl; far below, soft and out of focus, only the pink quilted cover and the dark wooden bed rail in warm small light fill the background to every edge; only the chest, the bowl, the paper and the two hands are in the frame",
         lines=[("baidaifu", "這一碗要一口氣餵完，中間不能停。", "畫外，慢而清楚")],
         motion=f"{NOBODY}the last of the brown powder slides from the paper into the bowl, and one hand sets the paper aside and stirs the bowl slowly with a thin wooden spoon",
         zh="插鏡、從略上方往下、慢推（**第一格就是藥箱與碗**，拍法 10、35；不寫地點句，送本集免費做的 `set-xujia-tangfang-kong-bei-l1`（夜裡粉被與床欄近景）只當背景與光）：黑漆藥箱蓋子掀起、放在粉被上，月白袖口的兩隻手把油紙包裡的藥粉倒進陶碗，倒完、拿細木湯匙攪開（一個動作；稿子『倒一點溫水、用指頭攪開』：指頭會讀錯，拍法 32，改木湯匙）；白大夫是畫外聲（`chars` 空，錄音）"),
    dict(loc="rx_c", cam="Medium shot, slow push in", chars=["xuyan", "xiaohe", "baidaifu"], night="lamp",
         comp=f"medium shot at the bedside: {XU_COAT}, sitting on the near edge of the bed, framed from the waist up, his left arm already under her shoulders lifting her head a little from the first frame, {BOWL} held to her lips in his right hand, his face lowered three-quarter to screen right toward her, never the lens; coaxing, gentle, not smiling: brows soft, lips moving softly between words; in the bed, {XIAOHE_BED_SHORT}, her eyes half shut, frowning, swallowing; at the right by the pillow end, {BAI}, sitting on the edge of the bed, framed from the waist up, watching her closely, his lips closed, not smiling, never the lens; the warm light of the one small flame on the low stool at the foot of the bed; {HANDS}; exactly three people",
         lines=[("xuyan", "乖，一口氣喝完，喝完就不燙了。", "哄著")],
         motion=f"Xu Yan tips the bowl slowly, little by little, as little Xiaohe frowns and swallows, until the bowl is empty; {quiet('Doctor Bai and little Xiaohe', 'their', plural=True)}",
         zh="中景、慢推（送 `-kong-chuang-l1`；燭火回到床尾矮凳上）：許硯左臂第一格已經托起小禾的頭、右手陶碗湊在她嘴邊，一點一點灌進去、她皺眉嚥下、碗空（一個動作；稿子『碗放在床頭』交給剪點：空碗在 s30 放在矮凳上），哄著說；白大夫在右、床沿枕頭那頭看著、嘴閉著"),
    dict(loc="rx_c", cam="Close-up, slow push in", chars=["baidaifu"], night="lamp",
         comp=f"close-up of {BAI}, sitting on the edge of the bed at its pillow end, framed from the chest up with space above his head, his face three-quarter to screen left {off('left', 'the dark plaster wall')}; tired but steady, not smiling: brows easing, lips moving calmly between words; behind him, soft, only the dark blue window and the plaster wall; {HANDS}",
         lines=[("baidaifu", "天亮之前看她退不退，退了就沒事。", "穩")],
         motion="Doctor Bai leans back against the bed head, glances once up at the dark window, and looks back as he speaks",
         zh="近景、慢推（送 `-kong-chuang-l1`；稿子『身後只有窗紙（深藍）』）：白大夫坐在床沿枕頭那頭（稿子『坐回床頭的凳子』：圖上沒有第二張凳），往後一靠、看一眼窗外的天色（一個動作；稿子『捻一下鬍鬚』：短鬚不捻），朝畫左外看不到的人（許硯，不寫人）說。獨立審稿必改 4：改送 `-kong-chuang2-l1`、畫左外只寫牆"),
    dict(loc="rx_d", cam="Medium shot, slow push in", chars=["aling"], night="lamp",
         comp=f"medium shot at the foot of the bed, the corner of the pink quilt soft in the lower right foreground: {ALING_N}, {WISPS}, sitting on the near edge of the bed at its foot beside the low stool, framed from the knees up, the long grey sash already laid folded on the bed beside her from the first frame, her head already leaning against the dark wooden bedpost of the foot, her face three-quarter to screen right {off('right', 'the pink quilt and the dark bed', he='she')}; worn out, not smiling: eyelids drooping, brows soft, lips moving very quietly between words; the one small flame on the low stool beside her the only warm light on her face; behind her, soft, the plank door at the left shut and the cracked plaster wall; {HANDS}",
         lines=[("aling", "我守著她，你們都去歇一下。", "很輕")],
         motion="A-ling's eyelids grow heavier and heavier, and when she finishes speaking her head tips gently against the bedpost and she falls asleep",
         zh="中景（膝以上：綁腿在框裡）、慢推（送 `-kong-men-l1`：矮凳與燭火、床尾的床柱、裂紋牆；前景右下被角）：稿子『阿令坐在床尾的矮凳上』：矮凳上放著那根蠟燭（圖），改坐在床尾的床沿、矮凳在她身邊；灰布腰帶第一格已經摺好放在床上（稿子『放在床頭』）；眼皮越來越重、說完頭一歪靠在床柱上睡著（一個動作）。剪接剪在頭一歪的一半（稿子〈剪接〉）"),
    dict(loc="rx_d", cam="Medium shot, slow push in", chars=["xuyan", "aling"], night="lamp", act=3,
         comp=f"medium shot at the foot of the bed: {ALING_N}, sitting on the near edge of the bed at its foot, asleep, her head leaning against the dark wooden bedpost, her eyes shut, framed from the knees up, her lips closed; beside her, standing, {XU_ROBE}, his old grey cloth outer coat already pulled off and spread wide in both hands from the first frame, framed from the waist up, his face lowered three-quarter to screen left toward her, never the lens; tender, not smiling: brows soft, lips pressed shut; the one small flame on the low stool beside them the only warm light; behind them, soft, the plank door at the left shut and the cracked plaster wall; {HANDS}; exactly two people",
         motion=f"Xu Yan lays the old grey coat gently over her shoulders, and his hands rest on it a moment before he draws them back; {quiet('Xu Yan and A-ling', 'their', plural=True)}",
         zh="中景、慢推（送 `-kong-men-l1`）：許硯第一格已經脫下舊灰外衣、兩手撐開（稿子『站起來、脫下』在第一格完成），輕輕蓋在阿令肩上、手停一下才收回（一個動作）；從這鏡起許硯只穿書生袍、阿令肩上披外衣（〈道具〉）。全程沒有人說話。稿子『窗紙一點一點轉白』：這張裁切沒有窗，天色交給 s24"),
    dict(loc="rd_c", cam="Close-up, slow push in", chars=["xuyan", "xiaohe"], night="morn",
         comp=f"close-up at the bedside at first light: {XU_ROBE}, sitting on the near edge of the bed by its pillow end, framed from the chest up, the back of his right hand already resting on her bare forehead from the first frame, his face lowered three-quarter to screen right toward her, never the lens; holding his breath, then relief: eyes wide and wet, brows lifting, lips moving softly between words, a small trembling smile at the end; along the bottom of the frame, {XIAOHE_WELL}, asleep, her lips closed; behind him, soft, only the small window glowing grey-white and the dark wooden bed head; {HANDS}; exactly two people",
         lines=[("xuyan", "不燙了……小禾的燒，真的退了！", "不敢大聲，鬆一口氣")],
         motion=f"Xu Yan turns his hand over and lays his palm on her forehead, holds it there, and his shoulders sink with relief as he speaks; {quiet('little Xiaohe', 'her')}",
         zh="近景、慢推（送 e938 的 `set-xujia-tangfang-kong-chen-zhen-l1`：清晨灰白光裡的枕頭那頭；**天亮**：蠟燭燒完熄了，照圖寫熄著）：許硯（只穿書生袍）手背第一格已經貼在小禾額頭，換掌心再摸、肩膀一鬆（一個動作），不敢大聲地說，最後可以笑一下（稿子：可以笑，鬆一口氣）；小禾臉色恢復、濕布拿掉、呼吸平穩、嘴閉著"),
    dict(loc="rd_c", cam="Close-up, slow push in", chars=["xuyan"], night="morn",
         comp=f"close-up of {XU_ROBE}, at the bedside, framed from the chest up with space above his head, his face three-quarter to screen right, his eyes on the pillow below the right edge of the frame, never the lens; he is the only person in the frame; spent, at peace, not smiling: brows easing, lips pressed shut; behind him, soft, only the small window glowing grey-white; {HANDS}",
         lines=[("xitong", "叮。任務完成。", "宣布")],
         panel=[("任務完成", "task")],
         motion=f"Xu Yan closes his eyes for a moment and lets out one long slow breath, his shoulders settling; {SILENT_HE}",
         zh="近景、慢推（送 `-kong-chen-chuang-l1`：清晨的床與窗）：許硯閉一下眼、吐一口長氣（一個動作）；系統是錄音、**全程嘴閉著**；**不寫淡藍光**（拍法 11，稿子『臉被淡藍光照亮』拿掉）；面板『任務完成』剪接時疊（第 38 集的緊急任務完成，聖經〈期限〉）、跟系統念的一字不差。獨立審稿必改 4：改送 `-kong-chen-chuang2-l1`"),
    dict(loc="rd_d", cam="Medium shot, slow push in", chars=["aling"], night="morn",
         comp=f"medium shot at the foot of the bed at first light, the dark wooden bedpost soft in the right foreground: {ALING_N}, {COAT_ON}, sitting on the near edge of the bed at its foot beside the low stool, framed from the knees up, her head already lifted from the bedpost from the first frame, her face three-quarter to screen right {off('right', 'the pink quilt and the grey plaster wall', he='she')}; just awake, not smiling: eyes searching, brows drawn, lips moving low between words; behind her, soft, the plank door at the left shut and the cracked plaster wall in the grey first light; {HANDS}",
         lines=[("aling", "燒退了嗎？這件外衣，是你蓋的？", "剛醒")],
         motion="A-ling's hand finds the coat on her shoulder, she grips its collar and looks down at it as she speaks",
         zh="中景（膝以上）、慢推（送 e938 的 `-kong-chen-men-l1`：清晨的門、裂紋牆、矮凳（蠟燭熄著）、床尾；前景床柱）：阿令第一格已經抬起頭，手摸到肩上的外衣、抓住衣領看一眼（一個動作；稿子『再看小禾、看許硯』交給說話的視線），朝畫右外看不到的人（許硯，不寫人）說（→ 答在 s27）"),
    dict(loc="rd_c", cam="Medium shot, slow push in", chars=["xuyan", "xiaohe"], night="morn",
         comp=f"medium shot at the bedside at first light: {XU_ROBE}, sitting on the near edge of the bed by its pillow end, framed from the waist up, his face three-quarter to screen left {off('left', 'the foot of the bed and the grey plaster wall', only=False)}; quiet and plain, not smiling: brows level, eyes steady, lips moving evenly between words; behind him, soft, {XIAOHE_WELL}, asleep, her eyes shut, her lips closed, and the small window glowing grey-white; {HANDS}; exactly two people",
         lines=[("xuyan", "退了。外衣是我蓋的，妳跑了一整夜。", "淡淡的")],
         motion=f"Xu Yan gives one small nod as he speaks; {quiet('little Xiaohe', 'her')}",
         zh="中景、慢推（送 `-kong-chen-chuang-l1`）：**獨立審稿必改 4、建議 5**：原是過肩（前景阿令後腦），坐在床尾的她不可能背對看得到窗的機位；改單人：許硯坐床沿枕頭那頭、朝畫左外看不到的人（阿令，不寫人）點一下頭（一個動作），淡淡地說（答 s26；好感 +12 的原因）；**身後床上熟睡的小禾**（床在畫面就寫她，原版必修）"),
    dict(loc="rd_c", cam="Close-up, slow push in", chars=["xuyan"], night="morn",
         comp=f"close-up of {XU_ROBE}, at the bedside, framed from the chest up with space above his head, his face still turned three-quarter to screen left toward the foot of the bed from the first frame, never the lens; he is the only person in the frame; surprised, not smiling: one brow lifting, lips pressed shut; behind him, soft, only the small window and the grey plaster wall; {HANDS}",
         lines=[("xitong", "叮。阿令好感，加十二。", "宣布")],
         panel=[("阿令 好感 +12 → 44", "affection")],
         motion=f"Xu Yan turns his head back to the front and one of his brows lifts slowly; {SILENT_HE}",
         zh="近景、慢推（送 `-kong-chen-zhen-l1`）：許硯轉回頭、眉頭一挑（一個動作）；系統是錄音、**全程嘴閉著**；不寫淡藍光；面板『阿令 好感 +12 → 44』（聖經〈好感帳〉：32 → 44）。獨立審稿必改 4：改送沒有枕頭的 `-kong-chen-qiang-l1`；建議 7：第一格臉還朝左"),
    dict(sid="s28b", loc="rd_c", cam="Medium close-up, slow push in", chars=["xuyan", "xiaohe"], night="morn",
         comp=f"medium close-up of {XU_ROBE}, at the bedside, framed from the waist up, both his hands resting on his thighs from the first frame, his face three-quarter to screen right, his eyes on the empty air before him, never the lens; quietly taken aback, not smiling: brows raised, lips pressed shut; behind him, soft, {XIAOHE_WELL}, asleep, her eyes shut, her lips closed, and the small window glowing grey-white; {HANDS}; exactly two people",
         lines=[("xitong", "阿令好感，突破四十。獎勵箱開啟：玻璃燒製法。", "宣布，亮")],
         panel=[("阿令好感，突破四十", "affection"), ("獎勵箱開啟：玻璃燒製法", "reward")],
         motion=f"Xu Yan's hands slowly tighten on his thighs and he draws one breath in through his nose; {SILENT_HE}; {quiet('little Xiaohe', 'her')}",
         zh="中近景（腰以上、跟 s28 不同景別）、慢推（送 `-kong-chen-chuang-l1`）：**拆鏡**：稿子 c28 第二句系統（突破四十、獎勵箱；兩句 28 字放不進一支 8 秒）；兩手在大腿上慢慢收緊、吸一口氣（一個動作）；系統是錄音、**全程嘴閉著**；面板兩行照 e932 的寫法（affection＋reward），跟系統念的一字不差。獎勵箱只在面板（拍法 36）。獨立審稿必改 4：身後床上寫熟睡的小禾（加送她的圖、兩人）"),
    dict(loc="rd_c", cam="Close-up, slow push in", chars=["xuyan"], night="morn",
         comp=f"close-up of {XU_ROBE}, at the bedside, framed from the chest up with space above his head, his face three-quarter to screen left, his eyes already on the foot of the bed beyond the left edge of the frame from the first frame, never the lens; he is the only person in the frame; wry, not smiling: brows level, mouth flat, lips pressed shut; behind him, soft, only the small window glowing grey-white and the grey plaster wall; {HANDS}",
         lines=[("xitong", "加十二。宿主一件外衣，換得倒便宜。", "冷，毒舌")],
         motion=f"Xu Yan glances toward the foot of the bed and then lowers his eyes to the floor; {SILENT_HE}",
         zh="近景、慢推（送 `-kong-chen-chuang-l1`）：許硯看一眼畫左外的床尾（阿令那邊；看的是地方，不寫人），又低下眼（一個動作）；系統的鬥嘴是錄音、**全程嘴閉著**、不出面板。稿子 c29 系統 15 字＋心裡話 15 字約 8.5 秒加停頓：照 e938 s15b 拆成本鏡與 s29b。獨立審稿必改 4：改送 `-kong-chen-chuang2-l1`"),
    dict(sid="s29b", loc="rd_c", cam="Medium close-up, slow push in", chars=["xuyan"], night="morn",
         comp=f"medium close-up of {XU_ROBE}, at the bedside, framed from the waist up, both his hands resting on his thighs from the first frame, his face three-quarter to screen left, his eyes on the foot of the bed beyond the left edge of the frame, never the lens; he is the only person in the frame; quietly moved, not smiling: brows soft, lips pressed shut; behind him, soft, only the grey plaster wall and the edge of the small window; {HANDS}",
         lines=[("xuyan", "外衣是便宜，她跑的那一夜不便宜。", "心裡話，錄得近、輕", "inner")],
         motion=f"Xu Yan draws one slow deep breath, his shoulders rising and settling, his eyes still on the foot of the bed; {SILENT_HE}",
         zh="中近景、慢推（送 `-kong-chen-zhen-l1`）：**拆鏡**：稿子 c29 的心裡話：吸一口長氣、肩膀起落（一個動作）；心裡話是錄音、**全程嘴閉著**、不笑（回系統的嘴）。獨立審稿必改 4：改送 `-kong-chen-qiang-l1`"),
    dict(loc="rd_c", cam="Medium shot, slow push in", chars=["xiaohe", "xuyan", "aling"], night="morn",
         comp=f"medium shot at the bedside at first light, the empty clay medicine bowl on the low stool at the foot of the bed soft in the lower left foreground: in the bed under the small window, {XIAOHE_UP}, framed from the waist up, her face turned three-quarter to screen left toward him, her eyes sliding aside, never the lens; frightened, not smiling: brows pinched, lips trembling, moving in a tiny whisper between words; on the near edge of the bed beside her, {XU_ROBE}, sitting, framed from the waist up, his face toward her, not smiling, brows drawing together, his lips closed, never the lens; at the left by the foot of the bed, {ALING_N}, standing, the old grey outer coat already folded over her forearms from the first frame, framed from the waist up, her face toward the girl, her lips closed, not smiling, never the lens; {HANDS}; exactly three people",
         lines=[("xiaohe", "哥，你落水那天，我看見有人推你。", "小小聲，害怕")],
         motion=f"little Xiaohe shifts a little closer to him and clutches the straw rabbit tighter against her chest as she whispers, and Xu Yan goes still; {quiet('Xu Yan and A-ling', 'their', plural=True)}",
         zh="中景、慢推（送 `-kong-chen-chuang-l1`；前景左下矮凳上的空藥碗：稿子『前景是床頭的空藥碗』照圖改）：小禾第一格已經醒、半坐、兩手抱著草兔子（`extras` 拿掉 cast 的 hugging，構圖寫兩手拿著），往許硯那邊挪一點、抱緊兔子（一個動作），小小聲、害怕、不笑（原版建議）；許硯坐床沿；阿令在床尾、外衣第一格已經摺好搭在前臂（稿子『把外衣摺好放在床頭』在第一格前完成）。三人。獨立審稿建議 6：許硯寫不笑"),
    dict(loc="rd_c", cam="Close-up, slow push in", chars=["xuyan"], night="morn",
         comp=f"close-up of {XU_ROBE}, at the bedside, framed from the chest up with space above his head, leaning forward, his face lowered three-quarter to screen right {off('right', 'the grey plaster wall')}; cold and intent, not smiling: the smile gone from his face, eyes narrowed and hard, brows down, lips moving low between words; behind him, soft, only the grey plaster wall; {HANDS}",
         lines=[("xuyan", "誰推的？妳看見他的臉了嗎？", "壓低")],
         motion="Xu Yan leans in closer and lowers his head toward the bed, his two hands closing together below the frame, as he speaks low",
         zh="近景、慢推（送 `-kong-chen-zhen-l1`）：**原版必修：許硯問『誰？』時大笑** → 笑容沒了、身體前傾、眼神變冷（構圖寫 `not smiling`、`the smile gone`）；低頭湊近、兩手在畫面下緣握住（她的小手不入鏡，不寫人）（一個動作），壓低聲音說（→ 答在 s32）。獨立審稿必改 4：改送 `-kong-chen-qiang-l1`、畫右外只寫牆；建議 16：兩手在畫面下緣合起來"),
    dict(loc="rd_c", cam="Close-up, slow push in", chars=["xiaohe"], night="morn",
         comp=f"close-up of {XIAOHE_UP}, framed from the chin up to the chest with a little space above her head, her face three-quarter to screen left {off('left', 'the grey plaster wall and the edge of the small window', he='she')}; scared and trying hard to remember, not smiling: brows pinched, lips moving in a small careful voice between words; behind her, soft, only the pink pillow and the dark wooden bed head; {HANDS}",
         lines=[("xiaohe", "戴一頂草帽，帽子綁著紅繩，我沒看見臉。", "小聲")],
         motion="little Xiaohe lets go of the rabbit with one hand and draws a wide flat circle round the top of her own head with her flat palm, then touches her palm under her chin where a cord would tie",
         zh="近景、慢推（送 `-kong-chen-zhen-l1`；稿子『身後只有窗紙』：她靠在枕頭上，身後是枕頭與床頭）：小禾鬆開一隻手、平掌在自己頭頂比一個圓（帽簷）、再比一下下巴下綁繩的地方（一個手勢的連續；拍法 32 平掌；**草帽不入鏡**，只在台詞，聖經〈伏筆〉），朝畫左外看不到的人（許硯，不寫人）小聲說（答 s31）"),
    dict(loc="rd_c", cam="Close-up, slow push in", chars=["xuyan"], night="morn",
         comp=f"close-up of {XU_ROBE}, at the bedside, framed from the chest up with space above his head, his face three-quarter to screen left, his eyes already fixed on one point in the empty air from the first frame, never the lens; he is the only person in the frame; cold and still, not smiling: eyes hard and distant, jaw tight, lips pressed shut; behind him, soft, only the small window glowing grey-white; {HANDS}",
         lines=[("xuyan", "紅繩草帽……錢府側門外，我見過一頂。", "心裡話，錄得近、輕", "inner")],
         motion=f"Xu Yan straightens slowly, and his right hand closes into a hard fist at the bottom of the frame; {SILENT_HE}",
         zh="近景、慢推（送 `-kong-chen-chuang-l1`）：許硯慢慢直起身、右手在畫面下緣握成拳（一個動作；稿子『手從小禾手上鬆開』在剪點）；心裡話是錄音、**全程嘴閉著**、不笑；不插原版的草帽插鏡（聖經〈伏筆〉：第一季不說破）。獨立審稿必改 4：改送 `-kong-chen-chuang2-l1`"),
    dict(loc="rd_d", cam="Medium shot, slow push in", chars=["qinshuang"], night="morn",
         comp=f"medium shot by the plank door at the left, the plank door at the left shut behind her: just inside the shut plank door, {QIN}, {SPEAR} upright in her right hand, its butt on the floor, already one step into the room from the first frame, out of breath, framed from the waist up, her left hand pressed flat on the shut plank door behind her, her face three-quarter to screen right {off('right', 'the grey plaster wall and the foot of the bed', he='she')}; urgent, not smiling: brows drawn, eyes hard, lips moving fast between breaths; behind her, soft, the cracked plaster wall in the grey first light; {HANDS}",
         lines=[("qinshuang", "許硯，穀倉那邊壓不住了，全村要拿刁七抵命。", "急")],
         motion="Qin Shuang pushes off from the door with her left hand and leans in toward the room as she calls out between breaths",
         zh="中景、慢推（送 `-kong-chen-men-l1`；加送 `prop-changqiang-l1`）：秦霜（右手長槍，**柴刀不寫**，拍法 5）從左邊的門衝進來（聖經第 42 條），第一格已經停在門檻上、門往裡推開，一手扶門框、身子往屋裡一探（一個動作），喘著朝畫右外看不到的人（許硯，不寫人）喊；許硯回頭交給下一鏡。**獨立審稿必改 2**：圖上房門關著：改成第一格已經進門一步、左手按在身後關上的門板、推門往屋裡一探，運鏡改慢推"),
    dict(loc="rd_c", cam="Medium shot, slow push in", chars=["xuyan", "baidaifu", "xiaohe"], night="morn",
         comp=f"medium shot at the bedside at first light: {XU_ROBE}, already risen from the edge of the bed from the first frame, standing, both hands already raised before his chest, one cupped over the other, from the first frame, framed from the waist up, his face three-quarter to screen right toward the old man, never the lens; firm, not smiling: jaw set, brows level, lips moving firmly between words; at the right by the pillow end, {BAI}, sitting on the edge of the bed, framed from the waist up, his face toward Xu Yan, his lips closed, not smiling, never the lens; in the bed beside him, {XIAOHE_UP}, her lips closed; {HANDS}; exactly three people",
         lines=[("xuyan", "我現在就去。白大夫，小禾拜託您了。", "急，穩")],
         motion=f"Xu Yan bows once to the old man over his cupped hands and turns away toward the door at the left as he speaks; {quiet('Doctor Bai and little Xiaohe', 'their', plural=True)}",
         zh="中景、慢推（送 `-kong-chen-chuang-l1`）：許硯第一格已經站起，兩手在胸前一抱拳（一手包另一手）對白大夫一拜、轉身往左邊的門（一個動作），急而穩地說（本場結尾）；白大夫坐床沿枕頭那頭、小禾在床上（床在畫面就寫她）；**阿令不寫**（拍法 1：一鏡最多三張臉，稿子『阿令站起來』交給剪點）。剪接剪在轉身走向門的一半。獨立審稿建議 8：抱拳在第一格完成，動作只留一拜、轉身"),
    # ---- scene 3: before the barn at the edge of the fields, early morning (39->40).
    dict(chapter="穀倉前的田頭，清晨", loc="b", cam="Wide shot, slow push in", chars=["diaoqi", "erniu", "qinshuang"], night="sun",
         comp=f"wide shot, like the picture, the still water of the rice field with its rows of young seedlings soft in the lower left foreground: on the trampled earth before the dark barn doorway, {DIAO}, {NOOSE}, already kneeling in the middle of the trampled earth from the first frame, framed full figure with both knees on the ground, his face lowered, never the lens; behind him, {ROPEMAN}; at the left along the edge of the rice field, standing in a loose half circle facing him, all of them on the dry trampled earth right at the edge of the water, {FOLK}, and in front of them {SHOUTER}, his right fist raised; among them in the front, {ERNIU}, framed full figure, his face toward the kneeling man, grim, not smiling, his lips closed, never the lens; by the swung-back left door leaf of the barn, {QIN}, {SPEAR} upright in her right hand, standing side-on, framed full figure, her face toward the kneeling man, her lips closed, not smiling, never the lens; every face angry or grim; {HANDS}; exactly ten people",
         lines=[("cunmin", "他帶人放火燒渠頭，差點要了全村的命！", "背影，怒吼")],
         motion=f"the broad-backed man in undyed hemp shakes his raised fist at the kneeling man, and the young man in rust-red jerks the neck rope taut so Diao Qi's head snaps up; {quiet('Diao Qi, Wang Erniu and Qin Shuang', 'their', plural=True)}",
         zh="全景、慢推（照圖；送整張 `set-gucang-wai-l1`：右邊低矮的灰木板穀倉、兩扇門板往外貼牆、黑門洞、門前一大片踩實的土地、左半是水田裡一排排青秧、遠處乾田、村子、山；加送 `prop-changqiang-l1`）：聖經〈接點〉39→40；**照圖改站位**（拍法 29、42）：穀倉在右，刁七第一格已經跪在門前空地中間、**全身入鏡、兩膝著地**（站主跪姿規則），麻繩綁身、脖子上套著粗麻繩、另一頭在他身後一個鐵鏽紅衣的年輕人手裡（只拍背影）；村民在左邊水田邊站成半圈：**十個人每人一種衣色與年紀**（拍法 34，不用主角的顏色；不寫 villagers、crowd）；村民甲（本色麻布短打、布包頭）只拍背影、舉拳、錄音（`MINOR` cunmin，Sadaltager）；二牛在前排、不笑；秦霜在穀倉左門扇旁、長槍直立。稿子『把刁七從穀倉門口拖到空地中間、推得跪下』在第一格完成，動作：村民甲揮拳、套繩一拉、刁七的頭被扯起來（一個動作）。**許硯不入鏡**（稿子『遠處許硯從右邊田埂跑來』：一鏡最多三張臉，二牛、秦霜、刁七已經三張；他在 s40 才到、第 40 集第一鏡入鏡）。獨立審稿建議 9：前景改水田、人都站在水邊的乾土上、壯漢寫五十歲、芥黃衣老漢換成背影的韓伯（白髮髻、灰長袍、竹杖，不點名、不送圖）"),
    dict(loc="b_g", cam="Medium shot, slow push in", chars=["hanbo"], night="sun",
         comp=f"medium shot on the trampled earth, {TWO_FOLK} soft and out of focus in the lower left foreground, their shoulders toward us: beyond them, {HAN}, {STAFF} in his right hand, standing facing them, framed from the waist up, his face toward the two men in the foreground, never the lens; old and weighty, not smiling: brows level, eyes steady and firm, lips moving slowly between words; behind him, soft, the grey plank barn and its dark doorway in the low morning sun; {HANDS}; exactly three people, the two in the foreground seen only from behind",
         lines=[("hanbo", "等許秀才來，這件事由他說了算。", "篤定，蒼老有分量")],
         motion="Elder Han plants the foot of the walking staff on the earth with one firm thump and lifts his free left hand, palm out, toward the two men as he speaks, and the two men in the foreground go still",
         zh="中景、慢推（送本集免費做的 `set-gucang-wai-men-l1`：穀倉、黑門洞、門前的土地）：前景左下兩個村民的背影（炭灰、暗橄欖綠，不點名、不送圖）；韓伯（白長鬚、灰長袍）面對他們、竹杖往地上一頓、左手平掌一抬（一個動作），蒼老有分量地說；**只在第三場**、跟白大夫不同場（聖經〈人物〉）"),
    dict(loc="b_f", cam="Low-angle medium shot, slow push in", chars=["qianyuanwai"], night="sun",
         comp=f"low-angle medium shot at the edge of the rice field: {QIAN}, already shoved his way through to the front from the first frame, between two men of the village seen soft at the edges of the frame, one in charcoal grey at the left and one in dark olive green at the right, framed from the waist up, his face three-quarter to screen right toward someone out of sight beyond the right edge of the frame, never the lens; that side of the frame is only the far ploughed fields and the edge of the rice field all the way to the edge, and the only face seen whole is his; shrill and vicious, not smiling: eyes narrowed, mouth wide between shrill words; behind him, soft, only the pale blue morning sky above the far fields and the small village houses; {HANDS}; exactly three people, the two at the edges seen only from behind and the side",
         lines=[("qianyuanwai", "還等什麼？流寇就該吊死在田頭！", "尖聲")],
         motion="Qian Yuanwai thrusts his flat ringed right hand out toward the right as he shrieks, the gold rings flashing in the morning sun",
         zh="略仰中景、慢推（送本集免費做的 `set-gucang-wai-tian-l1`：遠處乾田、村子、晨天）：錢員外（深金團花錦袍、三個金戒指）第一格已經推開兩個村民擠到前排（稿子『推開』在第一格完成），戴金戒指的手平掌往畫右外一伸（拍法 32：不寫單指），尖聲喊（→ 答在 s39）；韓伯不在這一框；兩邊村民只到肩與側臉（炭灰、暗橄欖綠）。獨立審稿必改 5：畫右外照圖寫遠田與水田邊，不寫『他是唯一的人』（兩邊有村民）；建議 17：兩支都像笑就 fix 改側後背影"),
    dict(loc="b_g", cam="Wide shot, slow push in", chars=["qinshuang", "diaoqi"], night="sun",
         comp=f"wide shot on the trampled earth before the barn, the slack neck rope crossing soft in the lower foreground: {QIN}, already stepped in front of the kneeling man from the first frame, standing side-on at the left of the frame, framed full figure, {SPEAR} in her right hand, her face three-quarter to screen left toward someone out of sight beyond the left edge of the frame, never the lens; that side of the frame is only the trampled earth and the green rice field all the way to the edge, and no one else stands on that side; scornful, not smiling: chin lifted, eyes cold, lips moving clipped and plain between words; behind her at the right, {DIAO}, {NOOSE}, kneeling on the trampled earth, framed full figure with both knees on the ground, his face lowered, his lips closed, not smiling, never the lens; behind them, soft, the grey plank barn and its dark doorway; {HANDS}; exactly two people",
         lines=[("qinshuang", "人是我擒的，要怎麼處置，等他一句話。", "不屑")],
         motion=f"Qin Shuang brings the butt of the spear down on the earth with one hard thump and tips the shaft across in front of the rope, holding it there as she speaks; {quiet('Diao Qi')}",
         zh="全景（兩人全身：**刁七跪姿拍到膝蓋**；shot_reading：中景偏全會讀成兩種景別）、慢推（送 `set-gucang-wai-men-l1`；加送長槍圖）：秦霜第一格已經一步站到刁七左前、刁七和村民之間（2026-11-06 審稿統一的位置），長槍往地上一頓、槍桿橫在套繩前（一個動作），抬下巴朝畫左外看不到的人（錢員外，不寫人）不屑地說（答 s38：不准）；刁七跪在她右後、嘴閉著；前景下緣鬆垂的套繩。獨立審稿必改 5：畫左外只寫那一側，不寫『她是唯一的人』"),
    dict(loc="b_g", cam="Close-up, slow push in", chars=["diaoqi"], night="sun",
         comp=f"close-up from a little below of {DIAO}, {NOOSE}, framed from the chest up with space above his head, his face already lifted three-quarter to screen right from the first frame toward someone out of sight beyond the right edge of the frame, never the lens; that side of the frame is only the sunlit grey planks of the barn wall all the way to the edge; defiant and mocking, a cold sneer: eyes narrowed, one corner of his mouth curling, lips moving rough and slow between words; behind him, soft and out of focus, the grey plank gable of the barn against the sky; at the left edge of the frame, soft and faceless, the shoulders of a few people turning their heads toward the right; {HANDS}; he is the only person in focus, the shapes behind him soft and faceless",
         lines=[("diaoqi", "柳溪的許秀才？要殺要放，你說。", "冷笑，粗啞，挑釁")],
         motion="Diao Qi's mouth curls in a cold sneer and he lifts his chin higher as he speaks, while the soft shoulders at the left edge all turn toward the right",
         zh="近景、慢推（稿子『從中近景推到近景』；送本集免費做的 `set-gucang-wai-qiang-l1`：穀倉的灰木板牆；稿子『身後只有穀倉的木板牆』）：刁七（脖子上套麻繩、臉上一道石灰白粉；近景不寫跪）第一格已經抬頭往畫右外看（許硯剛跑到，不寫人，拍法 31），冷笑、下巴抬高（一個動作），粗啞地說；身後虛焦的人影一齊轉頭往右（稿子『所有人跟著回頭』）。**本集唯一可以冷笑的鏡**（刁七挑釁）。剪接停在最高點、不收（懸念 → 第 40 集第一場：許硯站到刁七和村民之間『先問話』）。獨立審稿建議 10：寫略仰（背景是山牆與天）、轉頭的人影在畫左緣、他的前側"),
]

HEAD = [
    "- 重製版 r2、真人版（站主 2026-11-11「之後都用真人版」）：照 `docs/videos/zhong-tian-qu-qi-e039-r2/script.md`（c01–c40 對應 s01–s40，加兩個拆鏡 s28b、s29b，共 42 鏡；含「這版改了什麼」「2026-11-06 審稿後的修改」）；台詞一字不改，只改拍法；每鏡一個看得見的動作、一句一筆不拆半句、預設不笑。篇章設定 `production/r2-bible-e031-e040.md`（拍法 1–43 條、〈場景〉〈接點〉〈道具〉〈小角色〉），帳照 `r2-bible-e011-e060.md`。**第 4 篇章〈旱年〉第 9 集**：約第一七六天夜二更過半（縣城東街醫館門口）→三更前（回程官道）→第一七七天三更到天亮（病房）→清晨（穀倉前田頭）。",
    "- 內部工作編號 939（`hailuo/{ff,clips}-dh-e939.json`；`colab/runs/e939/extras.json`、`colab/runs/e939-live/spec.json`、工作資料夾 `~/mokaair-work/videos/zhong-tian-qu-qi-e939-dh/`）；發布 slug `zhong-tian-qu-qi-e039-r2`。不放集數、不放片名卡；**s01 接第 38 集定版成片 `e938-live.mp4`（188.43 秒）的最後一鏡**（s38 隊長右手舉在頭頂『放——』切黑）；s40 交給第 40 集（同一刻，許硯站到刁七和村民之間）。",
    "- 照第 38 集的審稿、fix1–fix6、成片審查與終驗的教訓一開始就照做：參考圖跟文字一致（本集的新圖都是免費裁切、新 id）；門寫明推開、半掩或關著（醫館兩扇門板、房門、穀倉兩扇門板）；**馬送配鞍馬圖 `prop-zaohongma-an-l1`、毛氈鞍墊照圖寫**（第 38 集 fix6：只送光背馬圖 H3 一律畫高鞍頭西式鞍）；許硯不寫鬍渣；風格句不寫 cinema camera；不寫 crowd、villagers、hundreds，寫實際人數，`exactly N` 寫在構圖、`only` 句再寫一次；不寫泥（石灰寫白粉）；`OFFSCREEN_SPEECH = False`、對畫外的人說話寫「朝畫左／右外看不到的人」；不寫 open、不寫否定名詞；長東西第一格分開（長槍、竹杖、弩、套繩）；同場相鄰說話的人錄音差 ≥ 3 個半音（拍法 43）。",
    "- **站主 2026-11-21～23 規則**（PR #2217，`production/OWNER-CHECK-20261122.md`）：品質優先；跪姿拍到膝蓋（刁七 s36、s39 全身兩膝著地；s40 近景不寫跪；病房許硯一律坐床沿）；唐小棠本集不入鏡（灶房看火）；人群聲用本集錄音倒放（`colab/runs/_scripts/crowd-murmur.py 39`，穀倉前）；音效用真實音效庫本機副本 `/root/mokaair-work/videos/_series/zhong-tian-qu-qi/sfx-real-20261121/`（`zhongtian-sfx-*`）；柴刀本集不寫；錢員外正面不笑會失敗的教訓：s38 他尖聲喊、不笑寫在表情。",
    "- **人物**：**白大夫**（第一次露臉）：送 `baidaifu-portrait-l1`（白髮小髻、白鬚修到下巴、月白舊長衫加素棉背心；定妝照嘴角微揚，嚴肅寫在表情）；s01–s05 左手一盞陶油燈（拍法 33：不是燈籠），s07 起藥箱斜挎；**s08–s13 每一鏡都在馬上**（原版必修）；第二場在病房；聲音 Rasalgethi。**阿令**：騎馬的樣子（袖口灰布條紮緊、裙下綁腿）；灰布長腰帶 s01–s05 在腰上、s06 抽出、s08–s13 綁在兩人腰上、s16 搭在臂上、s22 放在床上；s23 起肩上披許硯的舊灰外衣、s30 摺好搭在前臂。**守軍隊長**：送 `duizhang-portrait-l1`（mkspec 加在最後一張），同一張臉、同一頂盔；短刀已插回左腰的刀鞘。**弩手**六人、**舉火把的守軍**一人，遠、小、臉在盔影裡。**許硯**：s14–s23 外披舊灰外衣、s23 起只穿書生袍；袍子下半截石灰白粉（到第 40 集第一場）。**小禾**：s14–s22 病中（滿臉通紅、濕布）、s24 起退燒、s30 起半坐兩手拿著草兔子；床在畫面裡就寫她。**秦霜**：第 37 集那桿長槍（送 `prop-changqiang-l1`），柴刀不寫。**韓伯**只在第三場。**錢員外**是唯一的胖圓臉。**刁七**：破布短褐、黑綁腿、**不穿皮甲**、麻繩綁身、套繩、臉上石灰白粉。**二牛**前排不笑不說話。**村民甲**只拍背影、錄音（`MINOR` cunmin，Sadaltager）。",
    "- **軸線（照圖）**：東街照 `set-yiguan-men-ye-l1`：街往**左**遠處、右邊一排關著的木板店門；醫館＝最近那間（兩扇門板、兩級石階、門左方石拴馬樁）；白大夫從門口（右）出來，隊長、弩手、火把在街的遠端（左）；**回程往右**。官道：楊樹一排橫過畫面，**縣城在左、柳溪在右，回程一律由左往右**（聖經第 41 條）；s13 送整張官道圖、路往遠處、盡頭一盞小燈。病房照 `set-xujia-tangfang-kong-l1`／`-kong-chen-l1`：**門在左**、床靠後牆在窗下（枕頭那頭在右）、床前空著、床尾左角矮凳加蠟燭；進門的人從左邊來；許硯坐床沿、白大夫坐枕頭那頭的床沿、阿令坐床尾的床沿靠床柱。穀倉前照 `set-gucang-wai-l1`：**穀倉在右**（兩扇門板往外貼牆、黑門洞）、門前一大片踩實的土地、左半是水田青秧、遠處乾田、村子、山；刁七跪在門前空地、村民在左邊水田邊、秦霜站進中間；結尾所有人往右回頭。",
    "- **時間與光**：第一場冷藍月光，醫館門裡的暖光與白大夫的油燈、街遠處一支舉著的火把；官道只有月光（**不能亮**，原版必修）；第二場三更：床尾矮凳上那一朵燭火是唯一的暖光（s17、s18 許硯把蠟燭拿起來湊在枕邊），s24 起天亮灰白（`-kong-chen`，蠟燭燒完熄著）；第三場清晨低低的暖金色斜陽從右邊來（`set-gucang-wai-l1` 照原圖的暖光，不要原版的灰冷寫實）。時間跳都在剪點（s09→s10、s13→s14、s23→s24、s35→s36）。",
    "- **原版必修**：白大夫從馬背上消失 → s08–s13 每鏡兩人都在馬上（s11 他的白髮、閉著的眼、抓著她腰的手在她肩後；s12 他在她肩後）；白大夫進門時床是空的 → 病房裡床在畫面的鏡都寫小禾（s14、s17、s18、s20、s24、s30、s35）；許硯問『誰？』時大笑 → s31 `the smile gone`、不笑。原版建議：官道整段夜、只有月光；不用里程碑（s13 不寫石碑）；小禾『有人推』害怕不笑（s30）；秦霜來報、許硯直接起身（s34–s35）；穀倉段暖色；白大夫與韓伯不同場。",
    "- 要買的秒數（BUY，錄音前照第 35–38 集實測估：一句 6 秒的鏡放得下約 5.9 秒人聲、8 秒約 7.3 秒；第 38 集量到白大夫 16 字約 5.7 秒（慢）、隊長 16 字吼約 4.9 秒、阿令約 3.4 字／秒、許硯約 4、秦霜約 3.7、系統 9 字約 2.4 秒；小禾、韓伯、錢員外、刁七、村民甲照第 33–37 集估）：**8 秒** s02（白大夫 17 字、慢）、s04（阿令 18 字、喘）、s05（白大夫 20 字）、s12（白大夫 17 字數數、停頓）、s18（白大夫 18 字、慢）、s28b（系統 19 字）、s33（許硯心裡話 15 字、停頓）、s34（秦霜 21 字）、s36（村民甲 18 字）、s37（韓伯 15 字、蒼老慢）；**5 秒** s09、s23（無台詞）、s25（系統 6 字）；其他 6 秒。錄音實測後照 `span939-buy.txt` 重核。",
    "- **表上的「秒」欄是 lint 估法**，比錄音短；剪接以錄音的人聲長度為準。",
    "- **東街、官道、穀倉前（s01–s13、s36–s40）表上的提示詞帶「below the deep pool」**：只為了讓 `gen-dh` 的 `SET` 選到深潭那張圖（再由 `spec.json` 換成本集的圖），d1 由 `mkspec.py` 拿掉；**之後每個 fix／retake spec 都要帶同一組替換**。病房的提示詞帶「first bedroom of the Xu farmhouse」讓 `SET` 選到 `set-xujia-tangfang`（l2），`spec.json` 換成本集要送的圖。",
]
FOOT = [
    "- **參考圖**（`assets/refs-live/`）：許硯 l1、angle-a（帶笑的 angle-b 整集不送）；白大夫、韓伯、刁七只有定妝照；錢員外、二牛定妝照（angle-b 不送）；阿令 angle-b 不送、全景與兩人一馬的鏡只送 l1；小禾、秦霜只送定妝照；見 `colab/runs/e939-live/mkspec.py`。馬在畫面裡的 s08–s11、s13 加送 `prop-zaohongma-an-l1`（配鞍馬：毛氈鞍墊、麻繩肚帶）；隊長的 s02、s03、s09 加送 `duizhang-portrait-l1`；秦霜有長槍的 s34、s36、s39 加送 `prop-changqiang-l1`。過肩前景（s12 阿令的後腦、s27 阿令披外衣的肩）、s11 她肩後的白大夫、弩手、舉火把的守軍、村民、s19 的手都不送圖。",
    "- **場景圖**：東街送 e938 的 `set-yiguan-men-ye-men-l1`（s01、s04–s08）、`-jie`（s02、s03）與整張 `set-yiguan-men-ye-l1`（s09）；官道送 e938 的 `set-guandao-ye-shu-l1`（s10–s12）與整張 `set-guandao-ye-l1`（s13）；病房夜送 e938 的 `set-xujia-tangfang-kong-zhen-l1`（s14、s18）、`-kong-chuang`（s15、s17、s20、s21）、`-kong-men`（s16、s22、s23）與本集免費做的 `-kong-bei`（s19 插鏡）；天亮送 e938 的 `-kong-chen-zhen`（s24、s28、s29b、s31、s32）、`-kong-chen-chuang`（s25、s27、s28b、s29、s30、s33、s35）、`-kong-chen-men`（s26、s34）；穀倉前送整張 `set-gucang-wai-l1`（s36）與本集免費做的 `-men`（s37、s39）、`-tian`（s38）、`-qiang`（s40）。",
    "- **本集新做的圖**（2026-11-24，`live-action/free-e031-e040/`，各跑兩次逐位元一樣，寫進 refs-live README）：`xujia_tangfang_e939.sh`（病房夜的粉被與床欄近景 `-kong-bei`，s19 插鏡只當背景）、`gucang_wai_e939.sh`（穀倉前的三張裁切 `-men`、`-tian`、`-qiang`）。**沒有付費圖**。",
    "- **還缺、先用最接近的圖**（不花錢、註明在這裡）：(1) **醫館門板推開的圖**：圖上兩扇門板關著，s01、s04、s05、s07 的『門板往裡推開、門內暖光』寫在文字（付費 Qwen 加一件事『兩扇門板往裡推開、門內油燈暖光』約 1 CU，列在 PREP §5，不做）。(2) **官道沒有坡、沒有村子**：s13 照圖寫路的盡頭一盞小燈。(3) 病房、官道、東街偏 CG（試鏡第一、二輪的圖）；穀倉前的垂柳是金黃秋色（聖經：接受，文字不寫葉色）。(4) 油燈、藥箱、腰帶、外衣、藥碗、濕布、套繩、竹杖、弩、火把是文字加在圖上（馬、長槍、隊長另送圖）。",
    "- 共用檔：`build-r2.py` 的 `EN` 加一個鍵 `baidaifu`（白大夫第一次在畫面上說話；`gen-dh.mjs` 的名字 Doctor Bai；只加鍵，舊集逐位元重建不變）；`gen-dh.mjs`、`pilot.py`、`cast.json` 不動。對畫外說話、對地方說話的鏡，精修文字的通用說話視線由本檔結尾的 `live_clips()` 換成 d1 的方向句（`GAZE_REFINE`）。",
    "- **自審**（2026-11-24，`writer-tools/e039-r2/review.md`，不是獨立審稿）；獨立審稿的交辦在 scratchpad `e939prep/review-prompt.md`（前置代理沒有派子代理的工具）。",
    "- **d1 前置**（2026-11-24，`colab/runs/e939-live/PREP.md`）：`colab/runs/e939/extras.json`、`colab/runs/e939-live/{mkspec.py,spec.json}`（種子 9391101／9391102）、scratchpad `e939prep/{build939.sh,prep939.sh,check939.py,rec939-slow.sh}`（錄音）、`e939d1.sh`（Colab，**沒跑**）。",
    "- **獨立審稿後（2026-11-24，`writer-tools/e039-r2/review-independent.md` 必改 6、建議 17，逐條在它結尾）**：醫館門口 s01 s04–s08 改送付費 Qwen 開門圖的裁切 `set-yiguan-men-ye-kai-men-l1`、s09 送整張 `-kai`（**圖還沒跑**：scratchpad `e939qwen.sh`）；房門照圖寫關著；s11 s12 兩人一馬補腰帶、s12 改側面加馬；近景改送沒有床的 `-kong-chuang2`／`-kong-chen-chuang2`／`-kong-chen-qiang`，s27 s28b 寫床上的小禾；`off()` 加 `only`；s14 一塊濕布；回程送翻成頭朝右的 `prop-zaohongma-an-r-l1`、s01 加拴著的馬（原向）；石階一級；s18 的光、s27 單人、s30 s28 s13 s35 s36 s40 s07 s24 s31 的字；精修 s02 開頭不點名。",
    "- 配樂：第一場 s01 拉緊的弦樂一下鬆開（門開），s06 起急促鼓點，s10–s12 鼓點裡加輕快的笛子（數數），s13 溫暖的長音；第二場很輕的鋼琴，s24 退燒一個溫暖的重音，s28b 開箱一個亮音，s30 起低沉弦樂，s32 紅繩草帽一個重音，s34 鼓點進來；第三場低沉鼓點與人聲（`crowd-murmur.py 39`），s38 起拉緊的弦樂，s40 停在最高點、不收。音效見 script.md〈音樂與音效〉，從真實音效庫挑（站主 2026-11-21）；庫裡沒有的（門板推開、油燈、腰帶抽出、藥粉倒進碗、麻繩拉緊）列給站主用 Flow 做（提示寫 sound effect only, no music）。",
]

# Seconds to buy, estimated from e935-e938's measured lines (e938 PREP §4: Doctor Bai 16 characters 5.72 s, the captain 16 shouted
# 4.91 s, A-ling about 3.4 characters a second, Xu Yan about 4, Qin Shuang about 3.7, the system 9 characters in about 2.4 s; a
# 6 s shot holds about 5.9 s of speech, 8 s about 7.3 s); Xiaohe, Elder Han, Qian Yuanwai, Diao Qi, the village man estimated.
# 8 s: s02, s05, s12, s18 (Doctor Bai, slow: 17, 20, 17 counted, 18), s04 (A-ling 18, out of breath), s28b (the system 19),
#      s33 (Xu Yan's thought with its pause), s34 (Qin Shuang 21), s36 (the village man 18 shouted), s37 (Elder Han 15, old and slow).
# 5 s: s09, s23 (no line), s25 (the system's six characters).
# 6 s: every other spoken shot.
BUY = {"s02": 8, "s04": 8, "s05": 8, "s12": 8, "s18": 8, "s28b": 8, "s33": 8, "s34": 8, "s36": 8, "s37": 8,
       "s09": 5, "s23": 5, "s25": 5,
       "s01": 6, "s03": 6, "s06": 6, "s07": 6, "s08": 6, "s10": 6, "s11": 6, "s13": 6, "s14": 6, "s15": 6, "s16": 6, "s17": 6,
       "s19": 6, "s20": 6, "s21": 6, "s22": 6, "s24": 6, "s26": 6, "s27": 6, "s28": 6, "s29": 6, "s29b": 6, "s30": 6, "s31": 6,
       "s32": 6, "s35": 6, "s38": 6, "s39": 6, "s40": 6}


# ---- the refine text (as e031, e033, e935-e938): hailuo/clips-dh-e939.json column 0 is the motion text refine-prep.py sends
# with a picked d1 draft. Tang Xiaotang is not in this episode, so the back-shot rewrite of e938 has nothing to do; the speaking
# gaze of the lines said to someone out of frame (or to a thing) is replaced with the d1 direction sentence.
COLLAR = "Tang Xiaotang's high stand-up collar stays closed at her throat. "
FRONT_TANG = set()
GAZE_GEN = {"he": "turned toward the person he is speaking to, face in profile or three-quarter profile, eyes on that person",
            "she": "turned toward the person she is speaking to, face in profile or three-quarter profile, eyes on that person"}
# sid -> (pronoun, the direction sentence): the listener is out of frame, or the speaker looks at a place
GAZE_REFINE = {
    "s01": ("he", "his face three-quarter to screen left toward the street, his eyes on it"),
    "s03": ("he", "his face lowered three-quarter to screen right, his eyes on the clinic steps beyond the right edge of the frame"),
    "s05": ("he", "his face three-quarter to screen left toward someone out of sight beyond the left edge of the frame, his eyes on that spot"),
    "s06": ("she", "her face three-quarter to screen right toward someone out of sight beyond the right edge of the frame, her eyes on that spot"),
    "s07": ("he", "his face three-quarter to screen left toward someone out of sight beyond the left edge of the frame, his eyes on that spot"),
    "s10": ("he", "his face turned toward the back of her shoulder, his eyes squeezed shut"),
    "s11": ("she", "her face turned a little back toward her shoulder, her eyes on the road ahead"),
    "s12": ("he", "his chin pressed against the back of her shoulder, his face turned toward her ear, three-quarter toward us, his eyes shut"),
    "s14": ("he", "his face lowered three-quarter to screen right toward the girl in the bed, his eyes on her"),
    "s15": ("he", "his face three-quarter to screen left, his eyes on the shut plank door beyond the left edge of the frame"),
    "s16": ("he", "his face three-quarter to screen right, his eyes on the bed beyond the right edge of the frame"),
    "s18": ("he", "his face lowered three-quarter to screen right toward the girl in the bed, his eyes on her"),
    "s20": ("he", "his face lowered three-quarter to screen right toward the girl in the bed, his eyes on her"),
    "s21": ("he", "his face three-quarter to screen left toward someone out of sight beyond the left edge of the frame, his eyes on that spot"),
    "s22": ("she", "her face three-quarter to screen right toward someone out of sight beyond the right edge of the frame, her drooping eyes on that spot"),
    "s24": ("he", "his face lowered three-quarter to screen right toward the girl in the bed, his eyes on her"),
    "s27": ("he", "his face three-quarter to screen left toward someone out of sight beyond the left edge of the frame, his eyes on that spot"),
    "s26": ("she", "her face three-quarter to screen right toward someone out of sight beyond the right edge of the frame, her eyes on that spot"),
    "s31": ("he", "his face lowered three-quarter to screen right toward someone out of sight beyond the right edge of the frame, his eyes on that spot"),
    "s32": ("she", "her face three-quarter to screen left toward someone out of sight beyond the left edge of the frame, her eyes on that spot"),
    "s34": ("she", "her face three-quarter to screen right toward someone out of sight beyond the right edge of the frame, her eyes on that spot"),
    "s38": ("he", "his face three-quarter to screen right toward someone out of sight beyond the right edge of the frame, his eyes on that spot"),
    "s39": ("she", "her face three-quarter to screen left toward someone out of sight beyond the left edge of the frame, her eyes on that spot"),
    "s40": ("he", "his face lifted three-quarter to screen right toward someone out of sight beyond the right edge of the frame, his eyes on that spot"),
}
BACK_NAME = "the young woman seen only from behind"
# review 建議 12: s02 is Doctor Bai from behind; the refine head no longer names him or his face
BAI_HEAD = "Doctor Bai shown in <Picture 1> keeps the same face, hair, costume and props as the first frame; the set layout stays as it is."
BAI_BACK = "The old man seen only from behind in <Picture 1> keeps the same hair, costume and props as the first frame, his back to us; the set layout stays as it is."


def live_clips(path):
    import hashlib
    import json
    clips = json.load(open(path, encoding="utf-8"))
    for key, row in clips.items():
        text = row[0]
        sid = key.split("-", 1)[1]
        assert COLLAR not in text and "Tang Xiaotang" not in text, (key, "Tang Xiaotang is not in e039")
        if sid == "s02":
            assert text.count(BAI_HEAD) == 1, (key, "s02 refine head")
            text = text.replace(BAI_HEAD, BAI_BACK)
        if sid in GAZE_REFINE:
            pr, gaze = GAZE_REFINE[sid]
            assert text.count(GAZE_GEN[pr]) >= 1, (key, "speaking gaze")
            text = text.replace(GAZE_GEN[pr], gaze, 1)
        row[0] = text
        row[1] = hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]
    open(path, "w", encoding="utf-8").write(json.dumps(clips, ensure_ascii=False, separators=(",", ":")))


# e928 review 必改 1 (rule 39): ref2manifest.mjs (stage 1) strips gen-dh's refine anchor with ANCHOR_FF; the gaze sentences
# live_clips() writes no longer match gen-dh's. prep939.sh hands stage 1 the anchor form of the live file (this), then puts the
# live file back; the refine text (clips-dh) keeps live_clips()'s wording.
def anchor_form(text):
    text = text.replace(BAI_BACK, BAI_HEAD)
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
