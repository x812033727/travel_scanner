"""Episode 14 remake (r2): the writer spec for ../e001-r2/build-r2.py. Source: docs/videos/zhong-tian-qu-qi-e014-r2/script.md
(c01-c42 = s01-s42; the CG-era r2 script of PR #2024), including its sections 「這版改了什麼」, 「2026-11-06 審稿後的修改」 and
「真人版的改動（2026-11-15）」, which override the tables. Every line is the script's, word for word; only the staging changes.
Bible: production/r2-bible-e011-e020.md (rules 1-17).

Live action from the first draft, written the way e013-r2/r2.py was written AFTER its independent review (review.md in
../e013-r2, 必改 9 and 建議 18 applied there), with the e911/e912 draft lessons (colab/runs/e911-live/{review-picks-a.tsv,
review-picks-b.tsv,pick-review.md,cut-review.md,cut-review-2.md}, e912-live/{review-picks-a.tsv,review-picks-b.tsv,pick-review.md}):
- OFFSCREEN_SPEECH = False (bible rule 15): every shot with an off-screen line, a thought or a system line writes the silence
  of each person on screen (SILENT_*, quiet()), after the action.
- No background people (e911/e912: any extra person grows a sword; an unspecified background grows spear racks): nobody is
  written who is not in the script, and every place says what is behind (BEHIND_*) and that nothing leans anywhere (NORACK).
  The shed picture has two plain wooden drying frames by the vats: they are written as drying frames, nothing sharp.
- No fire unless the script has one (e912: braziers and torch stands grow in backgrounds): the shed says "no fire in the frame";
  the grove's only fire is the dying heap of paper on bare earth (the grove picture set-zhulin-fen-l2 draws it in a metal
  bowl: "no bowl, no brazier"); the corridor's only lights are the small candles on the wall and Xu Yan's one lantern.
- Cold faces written as actions (e911/e912: "no smile" alone does not hold): frown, clench the jaw, look away, press the lips;
  the shots allowed to smile are named in their comments (s15 Erniu, s21 and s25 Xu Yan, s22 Tang Xiaotang's bowed blush,
  s32 the carpenter's eased mouth corner, s39 Xu Yan; s13 a smile that fades at once). Risky silent faces stay short.
- Two-shots set the camera to one side and name the off-screen look target (e912: people facing the lens): every face is
  "three-quarter to screen left/right toward <who>", never the lens.
- Paper is blank and front-lit (bible rules 7, 17): the ledgers' covers are plain blue cloth and their open pages blank; the
  guild's sheet is only ever seen by its blank back (it is never called a notice in a prompt); the first white sheet is matte
  and blank and its willow leaf is a faint pale shape held against the evening sun (bible rule 7), no sparkle, no writing.
- Tang Xiaotang never speaks on camera (bible rule 3): her six lines (c16, c20, c24, c26, c40, c42) are an insert of her hand
  on the wooden abacus (s16) or shot from close behind her (TBACK, `nospeak`, spec.json drops her three face pictures and her
  identity sentence) with the person she speaks to straight ahead of her, her head never turning. Her silent face (s15, s18,
  s22) gets e907's neutral face sentences in spec.json (s22 only the face half: it is the one shot she may smile, bowed).
  Costume: the live portrait l1, cross-collared and closed (bible rule 4; the script's t2 stand-up collar is not written).
- The one weapon (bible rule 5): Qin Shuang's chopping knife only in s01, s03, s05 and s07, one fixed object (KNIFE) in her
  RIGHT hand, written by its screen side: she faces Xu Yan on screen left, so it is the hand on the screen-left side of her
  body (KHAND), the edge toward his throat, never changing hands. s01 and s05 are shot from behind Xu Yan (unnamed, no
  pictures sent); his own close-ups (s02, s04, s06, s08) keep the knife below the frame and say there is no blade. The script's
  c07 "slides it back into her belt" is not shot (a thing at the belt is drawn as a scabbard): she lowers it along her right
  thigh and turns away; from s09 on nobody holds a blade and her belt is empty (extras.json drops the knife from her look).
- The corridor (bible 〈還沒解決的〉, decided here): the e909 night corridor set-xujia-zoulang-l1 (plank doors along the
  right-hand wall, timber posts on the left, small candles on the wall between the doors, the open doorway to the yard at the
  far end, left of center). No new picture. The script's 「阿令房門在左、屋門在右」 is turned to match it: A-ling steps out of the
  nearest door in the right-hand wall, Xu Yan has come in through the far doorway; s10-s14 are side-on (him screen left, her
  screen right). Her 「手掌按上對面土牆，手臂橫在他面前」 is restaged as stepping square into his path (an arm across a
  corridor drawn from the side turns into an arm at the lens); s14 she steps half a step aside, goes in and shuts her door.
- The shed: set-gongpeng-l1 (day) for s15-s42: thatch and timber roof, open on the right, two big round vats of milky pulp at
  the left, a squat stone mortar in the middle, an old wooden table at the right, the back wall where sheets dry. The pulp is
  in the nearer vat (the picture's vats are already full of white). Afternoon (s27-s34) and evening (s35-s42) by the text.
- Night is night: s01-s09 the grove with no moon, cold starlight, the dying paper fire and the one lantern; s10-s14 the
  corridor by the wall candles and the lantern, no torch.
- Nobody is flipped in the edit: every speaker wears a cross collar; sides are written as screen left/right.
State at the junction (e013 r2.py s42): the grove at night, over-the-shoulder from behind Xu Yan (unnamed) pressed against a
bamboo stalk on screen left, the lantern in his left hand, his right hand raised open beside his head; Qin Shuang facing us
right of the middle, the knife level in her right hand (the screen-left side of her body) at his neck; the grave far behind her
with the paper fire still burning. s01 is that same framing at the same instant: three drumbeats, his shoulders jerk.
Places: the grove set-zhulin-fen-l3 ("bamboo grove"; redrawn, see below), the corridor set-xujia-zoulang-l1 ("inside corridor of
the Xu farmhouse"), the shed set-gongpeng-l2 ("work shed"; redrawn, see below); gen-dh's SET already maps all three. No new person (A-ling, Wang Erniu,
Carpenter Shi, Qin Shuang, Tang Xiaotang, Xu Yan all have live portraits and EN names).

Independent review (review.md in this folder, 2026-11-15, 必改 12, 建議 17), applied with the coordinator's decisions:
- 必改 1 / 建議 1: two pictures redrawn (live-action/screen-test-e014.py, seeds 37007/37008, not run yet): set-zhulin-fen-l3
  (an edit of l2: no metal bowl, no sparks, no board on the ground, a low earth grave mound with a small upright blank
  plank, a small heap of paper burning on the bare ground) and set-gongpeng-l2 (an edit of l1: no lattice on the floor, no
  crossed sticks in the vats, no tied poles at the far left; its light kept). pilot.py takes the newest l-version, so they
  are used as soon as they are in refs-live; prep914.sh stops until both are there. The grove text writes the fire on bare
  earth with no bowl in every shot (GROVE_BACK, FIRE).
- 必改 2: s02, s04 tight close-ups from under the chin (the knife at his neck stays out of the frame, not gone);
  必改 3: s07 does not turn (the turn is in the cut); 必改 4: scene 2 keeps one side: Tang Xiaotang's back in the RIGHT
  foreground in s20, s24, Xu Yan at the left end of the table looking right in s20, s21, s24, s25;
  必改 5: s30, s32 the mould on his left (far) shoulder, s32 looks back over his right shoulder, mkspec s30 eyes ahead;
  必改 6: the shed's back wall is bare, s35 has one single wet sheet; 必改 7: every shed header writes a plain earth floor
  (no lattice), the morning light comes from the upper left as in the picture (afternoon and evening from the open right
  side: the sun crosses over during the day); 必改 8: s15 rubs his eye instead of a yawn; 必改 9: s10's header describes
  the side view only (hall_side); 必改 10: s36 is the one shot written with light through the sheet (a paper window at
  dusk, the leaf where the paper is thinner, nothing appears on the surface); 必改 11: s42 a two-shot like s40, 6 s;
  必改 12: the one-second pauses in a06 and a10 cut to 0.4 s.
- 建議: s22 a held-back smile with a dimple, head bowed to the last frame; BUY s03, s40, s42 back to 6; s16 left at 6 (its
  tail runs into s17); s26 first frame at the table; s33 shot from the left side, the nearer vat; s34 bare forearms; s37 the
  sheet comes in from the left; s39 exactly three people and a besides sentence; s40 her right hand on the post at the
  right edge, the sheet in her left; s08 the left side of his neck; s01 his raised hand below her eyes; s28 background;
  s18 the pestle in his hands at the first frame; s12, s14 drop A-ling's profile picture (angle b) in spec.json.

Bible rule 18 (2026-11-15, from both e913 pickers: the nouns a prompt negates get drawn), applied before the first draft:
every negative list is rewritten as what is there. NORACK, NOBLADE's list, STICKS's list, ONLYKNIFE, NOKNIFE_HERE, KNIFE's
"not a broad cleaver, not a sword" (now "two fingers wide"), GROVE_BACK's building/roof/lantern list, FIRE's
bowl/brazier/basin, SHED_BACK's "nothing sharp", the shed floor's mat/lattice/grid, "no fire in the frame", the lantern's
"no writing" (now a round white paper lantern held by its bamboo handle), A-ling's "no shackles", the abacus's carving list,
the sheets' "no characters/sparkle", the corridor's "no torch", the moon and daylight words, s36's rays/flare/sparkle list,
NOSMILE and quiet()'s "no smile" (now the lips pressing flat and the jaw setting after the last word) and every inline
", no smile" are gone; "nothing", "nobody" and "only" stay. extras.json keeps only "no subtitles, captions or text" and
the clear-air sentence of e913 fix1; ref2manifest's "no second copy" line stays.
"""
EP = 914  # internal working number; the published slug is zhong-tian-qu-qi-e014-r2
SLUG = "zhong-tian-qu-qi-e014-r2"
EP_TITLE = "只能說真話（重製版 r2）"
OUTLINE_SECONDS = 212.5  # script.md: 212.5 s, 42 shots (14 + 12 + 16)
TARGET_MINUTES = [3, 4]
TITLE = "只能說真話｜種田娶妻打天下 第14集（重製版）"
DESCRIPTION = "柴刀還停在喉前，遠處更鼓敲了三聲：子時到了，許硯從現在起只能說真話。對，他跟蹤了；他怕她一個人出事；他看見她在哭，墳上沒有名字。秦霜收了刀：下次要跟，腳步放輕一點。回到家，阿令在走廊攔住他：你到底是誰？他說從很遠很遠的地方來，遠到自己也回不去了。天亮，工棚裡二牛把竹子搗成了糊，唐小棠問他昨晚去哪、問她跟秦霜誰好看，真話一句接一句冒出來。石木匠扛來竹簾，一問縣太爺真要這紙嗎，許硯只能招認是騙他的。傍晚第一張白紙揭下來，對著光，紙心一片柳葉。唐小棠卻喘著氣衝進工棚：書坊行會剛貼出來，柳溪白紙，縣城一張不收。《種田娶妻打天下》第 14 集（重製版）。"
THUMB = ("只能說真話", "s39")
CHARACTERS = ["xuyan", "qinshuang", "aling", "tangxiaotang", "erniu", "shimujiang", "xitong"]
MINOR = {}  # every speaker has a cast.json voice; nobody else speaks
MUSIC = "one cue per scene: a cold quiet night cue of a low drone, soft wind in bamboo and sparse low plucks, one deep hit on three distant drumbeats, warming a little after a soft chime, only low strings left in a dark corridor; then a light playful comedy cue of pizzicato strings, wood blocks and a small drum, stopping for one beat when a pestle drops and one short mocking trumpet-like figure after a chime; then a warm cue of soft strings and a wooden flute through a golden afternoon and evening, stopping when a grumpy old craftsman turns to leave, one bright accent as the first sheet of paper is lifted, dropping out completely when a girl bursts in out of breath and ending on one heavy low note; ancient Chinese rural drama, no vocals"

# Scene headers. Scene 1 is the grove (set-zhulin-fen-l3) and then the night corridor (set-xujia-zoulang-l1, e909); scenes 2 and
# 3 the work shed (set-gongpeng-l2) in the morning, the afternoon and the evening. Close shots use the short `_c` headers.
# No person's name in a place phrase; no "carpenter's workshop", "courtyard" or "campfire" (gen-dh SET would take another set).
# bible rule 18 (e913 picks: negative nouns are drawn): every place is written as what is there; "nothing" and "only" are
# used, the excluded thing is never named.
GROVE_BAMBOO = "only living bamboo stalks growing straight up all around"
GROVE_BACK = ("behind them only dense dark bamboo stalks growing straight up into black night; the only warm light is a small "
              "low heap of blank paper burnt down to its last embers lying directly on the bare earth in front of the grave mound")
FIRE = ("a small low heap of plain blank paper offerings burnt down almost to its last embers, glowing dull orange, lying "
        "directly on the bare earth")
SHED_BARE = "the posts and the earthen walls bare, nothing mounted on them and nothing leaning against them"
FLOOR = "the floor is plain packed earth, smooth and empty"
SHED_BACK = ("beyond the low walls only grey tiled roofs and green treetops, still and empty; beside the vats two plain low "
             "wooden drying frames, bare")
SHED_TABLE = ("two big round wooden vats at the left filled with milky white bamboo pulp, a squat stone mortar in the middle, an old "
              "plain wooden table at the right")
LOC = {
    "grove": f"In the bamboo grove behind the village at night: dense tall bamboo on both sides, a small clearing strewn with dry fallen bamboo leaves, a small low earthen grave mound with one short weathered plank stuck upright at its right front, its face bare grey wood, and in front of the mound {FIRE}; beyond the clearing only more dense bamboo fading into black, {GROVE_BAMBOO}; deep night, a sky full of cold stars through the bamboo tops, cold blue starlight, a light wind in the bamboo leaves",
    "grove_c": f"In the bamboo grove behind the village at night, deep night under cold blue starlight; {GROVE_BACK}",
    "grove_cl": f"In the bamboo grove behind the village at night, deep night under cold blue starlight; {GROVE_BACK} and the one lantern in the young man's hand",
    # review.md 必改 9: the two-shot is side-on, so its header describes only what a side view sees (the picture is a deep view).
    "hall_side": "In the inside corridor of the Xu farmhouse just after midnight: the camera stands by the timber posts on the left-hand side of the corridor and looks straight across at the right-hand wall: the cracked earthen wall with its plain plank doors and the small candles in iron holders between them runs flat across the whole background, parallel to the frame; the corridor runs from screen left to screen right; the doorway to the yard is beyond the left edge of the frame; one rough timber post soft and dark at the very left edge; every door and wall plain and unmarked, nothing leaning anywhere; deep night, lit only by the small candles on the wall and one paper lantern",
    "hall_c": "In the inside corridor of the Xu farmhouse just after midnight, lit only by the small candles on the wall and one paper lantern",
    "shed": f"In the open-sided work shed beside the Xu farmhouse on a clear autumn morning: a thatch-and-timber roof on rough wooden posts, open on the right side, a low back wall of packed earth and stone, {SHED_TABLE}; {FLOOR}; {SHED_BARE}; {SHED_BACK}; low warm morning sunlight slanting in from the upper left over the low wall, as in the location picture, the open right side bright with morning air",
    "shed_c": f"In the open-sided work shed on a clear autumn morning, low warm morning sunlight from the upper left; {SHED_BARE}",
    "pm": f"In the open-sided work shed beside the Xu farmhouse on a clear autumn afternoon: a thatch-and-timber roof on rough wooden posts, open on the right side, a low back wall of packed earth and stone, bare and warm, nothing hanging on it, {SHED_TABLE}; {FLOOR}; {SHED_BARE}; {SHED_BACK}; warm afternoon sunlight from the open right side",
    "pm_c": f"In the open-sided work shed on a clear autumn afternoon, warm afternoon sunlight from the open right side; {SHED_BARE}",
    "eve": f"In the open-sided work shed beside the Xu farmhouse at sunset: a thatch-and-timber roof on rough wooden posts, open on the right side, a low back wall of packed earth and stone, bare and warm, nothing hanging on it, {SHED_TABLE}; {FLOOR}; {SHED_BARE}; {SHED_BACK}; low golden evening sunlight slanting straight in through the open right side, long warm shadows",
    "eve_c": f"In the open-sided work shed at sunset, low golden evening sunlight from the open right side; {SHED_BARE}",
}
LIGHT = {
    "grove": "the deep night and the cold blue starlight stay unchanged, the sky stays black",
    "hall": "the deep night and the small warm candle flames stay unchanged",
    "morn": "the morning sunlight from the upper left stays unchanged",
    "pm": "the warm afternoon sunlight from the right stays unchanged",
    "eve": "the low golden evening sunlight from the right stays unchanged",
}
# bible rule 15: no "<X> speaks off screen" / "the system voice speaks off screen".
OFFSCREEN_SPEECH = False

# Repeated wording (each prop is one object).
XU = "Xu Yan, in an old plain grey cloth outer coat over his faded blue-grey scholar's robe"
XU2 = "Xu Yan, in his faded blue-grey scholar's robe patched at one elbow, the sleeves tied back above his forearms with cloth strips"
QIN = "her dark brown cross-collared short jacket, wide plain leather belt with nothing tucked in it and nothing hanging from it, black trousers, leather boots and high ponytail tied with black cord"
ALING = "A-ling in her plain grey-white cotton dress with long sleeves down over her wrists and one plain wooden hairpin"
ERNIU = "Wang Erniu, in his coarse brown short jacket with the sleeves rolled up, sweat on his brow"
CARP = ("Carpenter Shi, in his faded brown cross-collared short work jacket with the sleeves rolled up and his worn brown "
        "leather apron, one plain wooden stick through his grey topknot")
TANG = "in her peach-pink cross-collared short jacket wrapped shut over a pleated skirt with a ribbon bow"
GOLD = "the small gold abacus hanging at her waist"
ABACUS = "one plain wooden abacus with a smooth dark wooden frame and round dark wooden beads"
LEDGERS = "a tall stack of ten thread-bound account books, their covers plain unbroken dark blue cloth"
PESTLE = "one heavy plain wooden pestle as long as his arm"
PADDLE = "one plain wooden stirring paddle"
LANTERN = "one round white paper lantern held by its bamboo handle, a small candle burning inside"
MOULD = ("one papermaking mould: a flat plain rectangular wooden frame about an arm's length wide filled with very fine, closely "
         "laid thin bamboo strips, one small willow-leaf shape woven into its very middle with finer strips")
SHEET = "one sheet of fresh plain white paper the size of a book page, matte, thick and completely blank, its surface smooth and even"
CRUMPLED = "one crumpled sheet of plain paper, only its blank cream-coloured back toward us, thick and opaque, lit from the front"
BASKET = "one round bamboo basket covered with a plain cloth"
JUG = "one plain brown clay water jug"
BUNDLE = "one small empty bundle of dark blue cloth"
NOBLADE = "their hands hold only what is described here, belts and waists plain"
# bible rule 17: shots with a wooden stick say what the only long thing is.
STICKS = "the only long things anyone holds are plain wooden tools, smooth and round to their ends"
# bible rule 5 (as e013 s41-s42): the plot's knife, one fixed object, in her right hand, written by its screen side.
KNIFE = ("one old chopping knife with a short plain wooden handle and a dark iron blade two fingers wide and only a little "
         "longer than a palm, a thick blunt back and a nicked cutting edge")
KHAND = "her right hand, which is the hand on the screen-left side of her body, nearest him"
ONLYKNIFE = "the knife in her right hand is the only metal in the frame; the young man's hands hold only the lantern"
NOKNIFE_HERE = "the frame holds only his face, his raised hand, the lantern glow and the bamboo behind him"
TBACK = ("one young woman seen only from behind, appearing only once: the back of her head with two looped buns tied with pink "
         "silk ribbons and pearl pins, two long pink silk ribbons hanging from the buns down over her shoulders, a pink inner "
         "collar at the nape of her neck and her light peach-pink silk shoulders; the back of her head toward us the whole time, "
         "her ear the furthest round her head we ever see, only hair, ribbons and shoulders, her face turned fully away")
# s40, s42: back from town at a run (the script: 頭髮跑亂、一條緞帶鬆了).
TBACK_RUN = ("one young woman seen only from behind, appearing only once: the back of her head with two looped buns half come "
             "loose, wisps of hair escaping, one long pink silk ribbon come undone and hanging loose, the other still tied, a pink "
             "inner collar at the nape of her neck and her light peach-pink silk shoulders heaving; the back of her head toward us "
             "the whole time, her ear the furthest round her head we ever see, only hair, ribbons and shoulders, her face turned fully away")
HE_BACK = ("one young man seen only from behind, appearing only once, standing pressed against a thick bamboo stalk on screen "
           "left: only the back of his black topknot, his shoulder in an old plain grey cloth coat and " + LANTERN + " in his "
           "left hand lighting her face from below, his face never in the frame")
QIN_BACK = ("one young woman seen only from behind, appearing only once: only the back of her head with her high ponytail tied with "
            "black cord and her shoulder in a dark brown jacket, soft and dark, her head turned fully away from us, her ear, cheek "
            "and profile never visible, her face never in the frame, her hands below the frame")
NOSMILE = "after the last word the lips press flat and the jaw sets, the brows stay drawn, held to the last frame"
SILENT_HE = "He says nothing in this shot: his lips stay pressed together from the first frame to the last, his jaw still, no talking, no mouthing words"
SILENT_SHE = "She says nothing in this shot: her lips stay pressed together from the first frame to the last, her jaw still, no talking, no mouthing words"
HEADSTILL = "she keeps her head still and never turns it, the back of her head toward us the whole shot"


def quiet(who, pr="his", plural=False):
    verb = "say" if plural else "says"
    return (f"{who} {verb} nothing in this shot: {pr} lips stay pressed together from the first frame to the last, no talking, "
            f"no mouthing words, the face set and still")


SHOTS = [
    # ---- scene 1: the bamboo grove at midnight (Xu Yan on screen left against the bamboo, Qin Shuang on screen right, the grave
    # behind her), then the night corridor (side-on: Xu Yan screen left, A-ling screen right in front of her door).
    # s01 = e013 s42's framing at the same instant (bible rule 5: Xu Yan unnamed, from behind, no pictures; KHAND).
    dict(chapter="子時", loc="grove_cl", cam="Over-the-shoulder close two-shot, slow push in", chars=["qinshuang"], night="grove",
         comp=f"over-the-shoulder close two-shot from close behind {HE_BACK}, his right hand raised open beside his head on screen right, below the line of her eyes, not covering her face or the knife; facing us a little right of the middle Qin Shuang, {QIN}, framed from the chest up with space above her head, her eyes still a little red-rimmed, her face three-quarter to screen left toward him, never the lens; hard and still: brows drawn down, jaw clenched, eyes locked on him, lips pressed shut; {KNIFE}, held level in {KHAND}, its sharp edge stopped one finger's width from the side of his neck on screen left, its blunt back toward the lens, not touching his skin; far behind her the small grave mound and the dying paper fire; {ONLYKNIFE}; exactly two people",
         lines=[("xitong", "叮。子時已過，真話懲罰生效。", "冷，宣判")],
         panel=[("子時已過，真話懲罰生效", "penalty")],
         motion=f"far away three slow drumbeats of the night watch carry through the bamboo; at the third beat the young man's shoulders jerk once and his raised hand twitches, the back of his head toward us the whole shot; the knife stays level and unmoving in her right hand on the screen-left side of her body; {quiet('Qin Shuang', 'her')}",
         zh="過肩雙人近景、慢推（第一格接第 13 集 s42 同一刻、同一個機位）：前景左只有許硯的後腦、舊灰外衣肩、左手燈籠照亮她的下巴、右手張開舉在頭旁（不點名、不送圖）；秦霜正對我們偏右，右手（她身體畫左那側、靠他那隻）平舉舊柴刀、刃口停在他頸側（畫左）一指寬、刀背朝鏡頭；遠處墳與快燒完的紙錢火；更鼓三聲，第三聲時他肩膀一震、舉著的手一抖；秦霜嘴閉著、咬牙不笑；畫面裡沒有別的刀。系統句畫外，面板疊上。不寫藍光"),
    # His close-ups keep her knife below the frame (bible rule 5: his face shots carry no blade).
    dict(loc="grove_cl", cam="Close-up, slow push in", chars=["xuyan"], night="grove",
         comp=f"tight close-up of {XU}, his back pressed against a thick bamboo stalk, framed from just under his chin to just above his topknot, his neck below the bottom edge of the frame, where her knife edge still rests against it unseen, his right hand raised open beside his head at the edge of the frame, {LANTERN} hanging low in his left hand lighting his chin from below, one bead of sweat at his temple, his face three-quarter to screen right toward the woman off screen right, never the lens; startled by his own mouth: eyes narrowing at a sound, then flying wide; {NOKNIFE_HERE}",
         lines=[("xuyan", "對，我跟蹤妳。我怕妳一個人出事。", "脫口而出，句尾帶錯愕")],
         motion=f"Xu Yan's eyes narrow for an instant as if at a far sound, then his mouth opens and the words tumble out by themselves; after the last word he stares wide-eyed and presses his lips tight together; {NOSMILE}",
         zh="下巴以上的大近景、慢推（審稿必改 2：脖子與抵著的刀都在畫面下緣之外；身後只有竹子與黑夜）：許硯背貼竹竿、右手還舉著、左手燈籠低提照亮下巴，鬢角一滴汗；眼睛一縮，話自己冒出來，說完瞪大眼、把嘴抿緊；不笑"),
    dict(loc="grove_c", cam="Close-up, slow push in", chars=["qinshuang"], night="grove",
         comp=f"close-up of Qin Shuang, {QIN}, framed from the chest up with space above her head, her eyes still a little red-rimmed, her face three-quarter to screen left toward the young man off screen left, never the lens; cold: brows drawn down, jaw tight, eyes hard but wavering for one moment, lips moving low between words; {KNIFE}, held level in {KHAND} at the lower left edge of the frame, its edge pointing off screen left toward his throat, its blunt back toward the lens; the knife in her right hand is the only metal in the frame; nobody else in the frame",
         lines=[("qinshuang", "怕我出事？我拿刀的時候，你拿的是燈籠。", "冷，壓著")],
         motion=f"the knife in her right hand on the screen-left side of her body sinks one finger's width, her eyes waver once, then the knife lifts back level and her jaw sets again; {NOSMILE}",
         zh="近景、慢推（身後只有竹子與黑夜）：秦霜眼睛還有一點紅，右手（她身體畫左那側）平舉的柴刀在畫面左下緣、刃口朝畫左外的許硯；刀往下沉一指寬、眼神晃一下，又抬回來、咬緊牙說；不笑"),
    dict(loc="grove_cl", cam="Close-up, slow push in", chars=["xuyan"], night="grove",
         comp=f"tight close-up of {XU}, his back against a thick bamboo stalk, framed from just under his chin to just above his topknot, his neck below the bottom edge of the frame, where her knife edge still rests against it unseen, the glow of the lantern in his left hand from below, his face three-quarter to screen right toward the woman off screen right, never the lens; steady and earnest: brows level, eyes on her without blinking, lips moving evenly between words; {NOKNIFE_HERE}",
         lines=[("xuyan", "打不過也要跟。妳一個人進林子，我不放心。", "很穩，認真")],
         motion=f"his open right hand, still raised beside his head at the edge of the frame, slowly sinks out of the bottom of the frame, his eyes never leaving her; {NOSMILE}",
         zh="下巴以上的大近景、慢推（審稿必改 2：脖子與刀都框出去）：許硯舉在頭旁的右手慢慢沉出畫面下緣，眼睛不眨地看著畫右外的秦霜，很穩地說；一點笑都沒有"),
    # From behind Xu Yan again (unnamed, no pictures); the knife lowered to her side, still in the same hand.
    dict(loc="grove_cl", cam="Over-the-shoulder medium shot, slow push in", chars=["qinshuang"], night="grove",
         comp=f"over-the-shoulder medium shot from close behind {HE_BACK}, his hands down at his sides; a step away facing us a little right of the middle Qin Shuang, {QIN}, framed from the waist up with space above her head, her face turned half away toward screen right, her eyes sliding back toward him; guarded: brows knotted, jaw tight, lips moving low between words; {KNIFE}, now held low at her side in {KHAND}, its blade pointing at the ground; far behind her the small grave mound and the dying paper fire; {ONLYKNIFE}; exactly two people",
         lines=[("qinshuang", "你躲在竹子後面，都看見了什麼？", "低，戒備")],
         motion=f"Qin Shuang lowers the knife to her side in her right hand on the screen-left side of her body, turns her face half away toward screen right, then slides her eyes back to him as she asks; the young man keeps the back of his head toward us the whole shot; {NOSMILE}",
         zh="過肩中景、慢推：前景左只有許硯的後腦、舊灰外衣肩與左手燈籠（不點名、不送圖）；秦霜把刀放低到身側（還在右手、她身體畫左那側、刀尖朝地），臉別開一半往畫右、眼睛斜回來看他，低聲問；不笑；畫面裡沒有別的刀"),
    # Reverse: from behind Qin Shuang (unnamed, no pictures, her hands below the frame).
    dict(loc="grove_cl", cam="Over-the-shoulder medium shot, slow push in", chars=["xuyan"], night="grove",
         comp=f"over-the-shoulder medium shot from close behind {QIN_BACK}, in the right foreground; facing us on screen left a step away {XU}, his back against a thick bamboo stalk, framed from the waist up with clear space above his head, {LANTERN} hanging low in his left hand, his face three-quarter to screen right toward her, never the lens; honest and shaken: brows drawn up, eyes glancing aside for a moment, lips moving between words; {NOBLADE}; exactly two people",
         lines=[("xuyan", "看見妳在哭。墳上沒有名字，別的我沒看清。", "真話，說完愣住")],
         motion=f"Xu Yan swallows, his eyes flick past her shoulder toward the grave behind the camera and come straight back to her face as the words come out; the young woman in the foreground keeps her head still, the back of her head toward us the whole shot; {NOSMILE}",
         zh="反打過肩中景、慢推：前景右只有秦霜的後腦、高馬尾與深褐衣肩（不點名、不送圖、手在畫面下緣之外）；許硯在畫左背貼竹竿、左手燈籠，吞一口口水、眼睛往她身後的墳看一下又轉回來，說真話；不笑；畫面裡沒有刀"),
    # The script's c07 "插回腰帶右邊" is not shot (a thing at the belt is drawn as a scabbard): the knife goes down along her thigh.
    dict(loc="grove_c", cam="Medium shot, slow push in", chars=["qinshuang"], night="grove",
         comp=f"medium shot of Qin Shuang, {QIN}, framed from the knees up with space above her head, beside the small grave mound on screen right, her face three-quarter to screen left, her eyes lowered to the ground, not on the young man off screen left, never the lens; stubborn: brows knotted, jaw set, the tips of her ears faintly flushed, lips moving curtly between words; {KNIFE}, held in her right hand, the hand on the screen-left side of her body, hanging straight down along her thigh, its blade pointing at the ground, the same hand the whole shot; the knife in her right hand is the only metal in the frame; nobody else in the frame",
         lines=[("qinshuang", "下次要跟，腳步放輕一點。", "嘴硬，不看他")],
         motion=f"Qin Shuang says it curtly with her eyes on the ground, then drops her chin and stays where she is, jaw set; her body, her feet and the knife do not move until the last frame; {NOSMILE}",
         zh="中景、慢推（墳在畫右）：秦霜右手（她身體畫左那側）的柴刀垂在大腿邊、刀尖朝地（稿子的插回腰帶不拍：腰上掛東西會畫成刀鞘），眼睛看地、不看他，耳根有一點紅，硬硬說完，下巴一收、站著不動（審稿必改 3：轉身會換手，轉身交給剪接，s09 兩人已在走）；不笑"),
    # The system: he says nothing (bible rule 15), no blue light (bible rule 11).
    dict(loc="grove_cl", cam="Close-up, slow push in", chars=["xuyan"], night="grove",
         comp=f"close-up of {XU}, his back against a thick bamboo stalk, framed from the chest up with space above his head, {LANTERN} hanging low in his left hand, his face three-quarter to screen right, never the lens; drained relief: eyes closing for a moment, brows easing, lips closed the whole shot; {NOBLADE}",
         lines=[("xitong", "叮。秦霜，好感加五。", "冷，公事公辦")],
         panel=[("秦霜 好感 +5 → 18", "panel")],
         motion=f"Xu Yan reaches across with his right hand and rubs the left side of his neck, where the blade was, the lantern still in his left hand; then he lets out one long breath and his shoulders drop; {SILENT_HE}; {NOSMILE}",
         zh="近景、慢推（身後只有竹子與黑夜）：許硯摸摸脖子、長長吐一口氣、肩膀垮下來；全程嘴閉著（系統畫外，面板疊上）。不寫藍光"),
    # Both small and from behind, nobody named (the original e013 grew an extra figure in this grove). Her knife is not written.
    dict(loc="grove", cam="Extreme wide high-angle shot, slow pull out", chars=[], night="grove", act=3,
         comp=f"extreme wide high-angle shot looking down into the small clearing: in the right foreground the small earthen grave mound with its blank wooden plank and the paper fire now only a few red embers; walking away from us out of the clearing toward screen left between the bamboo, small in the frame and seen only from behind, one young woman in a dark brown short jacket with a high ponytail, {BUNDLE} under her left arm, and two steps behind her one young man in an old grey coat carrying {LANTERN}; neither face is ever visible; nobody else anywhere; {NOBLADE}",
         lines=[("qinshuang", "回去吧。這座墳裡是誰，你先別問我。", "不回頭，低")],
         motion="the young woman walks on without looking back; the young man nods once and follows her two steps behind, the lantern swaying; both keep their backs to us the whole shot; bamboo leaves stir in the wind",
         zh="大全景、高角度、慢慢拉遠（稿子是慢慢升高；gen-dh 不認升降）：右前景是墳與只剩一點紅的紙錢火；兩人很小、背對、不點名不送圖，秦霜（左臂夾空了的藍布包）往畫左走出竹林，許硯提燈籠跟在兩步後、點一下頭；都不回頭。秦霜的台詞放錄音（人小、背對）；刀不寫"),
    # The corridor (e909 picture: doors along the right-hand wall). Side-on: Xu Yan screen left, A-ling screen right.
    dict(loc="hall_side", cam="Medium two-shot, slow push in", chars=["xuyan", "aling"], night="hall",
         comp=f"medium two-shot from the side of the corridor, the row of plain plank doors in the wall behind them: on screen left {XU}, framed from the knees up with clear space above his head, {LANTERN} hanging in his left hand, having just walked in from screen left and stopped short, his face three-quarter to screen right toward her, never the lens; caught: eyes wide, lips pressed shut; on screen right a step away {ALING}, just out of the open plank door of her room behind her and standing square in his path, framed from the knees up with clear space above her head, her face three-quarter to screen left toward him, never the lens; cold and quiet: brows level, eyes narrowed and fixed on him, lips moving softly between words; {NOBLADE}; exactly two people",
         lines=[("aling", "半夜出門，這時候才回來。你到底是誰？", "很輕，很冷")],
         motion=f"A-ling takes one step out of her doorway into his path and stops; Xu Yan halts, the lantern swinging once in his hand; {quiet('Xu Yan')}",
         zh="雙人中景、慢推（側面拍，前景左一根木柱虛焦，背後是右牆那排木板門；用第 9 集夜走廊：門在右牆）：畫左許硯（外披舊灰外衣、左手燈籠）剛從走廊盡頭的門口進來、停住，燈籠一晃、嘴閉著；畫右阿令從自己房門一步跨出、站在他面前擋住去路，很輕很冷地問；不笑（稿子的「手臂橫在他面前」改成擋在他面前：側拍時手臂會伸向鏡頭）"),
    dict(loc="hall_c", cam="Close-up, slow push in", chars=["xuyan"], night="hall",
         comp=f"close-up of {XU}, framed from the chest up with space above his head, the warm light of the lantern in his left hand falling on his face from below, his face three-quarter to screen right toward A-ling off screen right, never the lens; caught by his own mouth: brows up, lips moving between words, then eyes flying wide; behind him only the cracked earthen wall and one small candle flame in an iron holder",
         lines=[("xuyan", "我是從很遠很遠的地方來的。", "真話，自己都沒想到")],
         motion=f"Xu Yan opens his mouth as if to laugh it off, but the words come out first; afterwards his eyes go wide and he swallows; {NOSMILE}",
         zh="近景、慢推（身後只有土牆與一盞小燭）：許硯燈籠的光從下面照臉，想打哈哈，嘴卻先說了；說完瞪大眼、吞口水；不笑"),
    dict(loc="hall_c", cam="Close-up, low angle, slow push in", chars=["aling"], night="hall",
         comp=f"low-angle close-up of {ALING}, framed from the chest up with space above her head, her face three-quarter to screen left toward Xu Yan off screen left, never the lens; probing and cold: eyes narrowed, brows drawn a little together, lips moving softly between words; candlelight on one side of her face; behind her only the dark timber beams of the corridor ceiling",
         lines=[("aling", "多遠？騎馬走得到嗎？比京城還遠？", "追問，冷")],
         motion=f"A-ling narrows her eyes and leans her face a little closer to his, searching his eyes; {NOSMILE}",
         zh="低角度近景、慢推（身後只有走廊的木樑）：阿令瞇起眼、把臉往前湊一點看他的眼睛，冷冷追問；不笑"),
    # A faint smile that fades at once (the script: 笑了一下，笑容慢慢收掉).
    dict(loc="hall_c", cam="Close-up, slow push in", chars=["xuyan"], night="hall",
         comp=f"close-up of {XU}, framed from the chest up with space above his head, the lantern light from below, his face three-quarter to screen right toward A-ling off screen right, never the lens; at first a faint closed-lipped smile that fades away at once, then quiet and hollow: brows easing down, eyes going distant, lips moving softly between words; behind him only the cracked earthen wall",
         lines=[("xuyan", "遠到騎馬走不到……我自己也回不去了。", "輕，眼神有點空")],
         motion="Xu Yan gives a faint closed-lipped smile that drains away at once; his eyes drift past her into the dark of the corridor as he speaks, and stay there; the smile does not come back",
         zh="近景、慢推（身後只有土牆）：許硯嘴閉著笑一下、笑容馬上收掉，眼神越過她看向走廊的黑暗，輕輕地說；之後不再笑"),
    dict(loc="hall_c", cam="Close-up, slow push in", chars=["aling"], night="hall",
         comp=f"close-up of {ALING}, framed from the chest up with space above her head, her face three-quarter to screen left toward Xu Yan off screen left, never the lens; quiet and unreadable: brows still, eyes lingering on his face, lips moving very softly between words; behind her only the open plank door of her room and the dark inside",
         lines=[("aling", "回不去的人，就好好待著。", "很輕")],
         motion=f"A-ling looks at him a moment longer, speaks very softly, then steps half a step aside, turns away into her room and pulls the plank door shut behind her; {NOSMILE}",
         zh="近景、慢推（身後只有她的房門）：阿令眼睛還停在他臉上，很輕地說完，側讓半步、轉身進房、把木門帶上（結尾）；不笑"),
    # ---- scene 2: the work shed in the morning (open on the right; vats on the left, the mortar in the middle, the table right).
    # Erniu may grin here (the script: good news). Tang's silent face: neutral sentence in spec.json.
    dict(chapter="工棚", loc="shed", cam="Wide shot, slow pan right", chars=["xuyan", "erniu", "tangxiaotang"], night="morn",
         comp=f"wide shot past the rim of a big wooden vat in the left foreground, keeping Xu Yan in the frame as he walks from screen left toward screen right: in the middle {ERNIU}, {PESTLE} in both hands at the stone mortar, framed full length with clear space above his head, his face three-quarter to screen left toward Xu Yan, never the lens; beaming: brows up, a wide open grin between words; on screen left {XU2}, walking in from the left, framed full length, his face three-quarter to screen right, never the lens; sleepy: eyes heavy and half shut, rubbing one eye with the back of his right hand; on screen right Tang Xiaotang {TANG}, {GOLD}, seated behind the old table with {ABACUS} and {LEDGERS} on it, her face three-quarter to screen left toward the men, never the lens; busy: eyes on the abacus, lips closed; {STICKS}; exactly three people",
         lines=[("erniu", "許兄弟！照你昨天交代的，竹子泡了一夜，搗成糊了！", "大嗓門，高興")],
         motion=f"Erniu thumps the pestle down into the mortar with a splat of white pulp and lifts his head to call out; Xu Yan walks in rubbing his eye; {quiet('Xu Yan and Tang Xiaotang', 'their', True)}",
         zh="全景、慢慢往右搖（跟著許硯由左往右）、前景泡竹木桶邊：中間二牛（滿頭汗、捲袖）兩手握木杵在石臼，杵一頓、白漿濺起，抬頭朝許硯大聲說（本鏡可以咧嘴笑，是好消息）；左邊許硯（袖子用布條綁起）揉著眼睛進來（審稿必改 8：打呵欠會張嘴，跟不動嘴打架）；右邊唐小棠坐在舊木桌後（木算盤、十本藍布面帳冊）低頭看算盤、嘴閉著不笑；許硯、唐小棠整鏡不說話不動嘴"),
    # Converted: her line over an insert of her hand on the wooden abacus (no face).
    dict(loc="shed_c", cam="Insert close-up, slow push in", chars=[], night="morn",
         comp=f"insert close-up, the shot opens directly on the top of the old wooden table from its very first frame: {ABACUS}, {LEDGERS} beside it, and one slender hand in a peach-pink silk sleeve resting on the abacus; only the hand, the sleeve, the abacus, the books and the wood are in the frame, no face; low morning sunlight",
         lines=[("tangxiaotang", "十天只剩八天。你昨晚半夜，到底去哪了？", "瞇眼追問，不笑")],
         motion="her forefinger flicks one bead across the wooden abacus with a click, then the hand lies flat on the table and slides forward a little as she leans in",
         zh="【改插鏡】插鏡、慢推（第一格就是舊木桌面）：素木算盤、十本藍布面帳冊，一隻桃粉袖口的手按在算盤上撥一顆，再平放桌上往前一滑（她往前湊）；臉不入鏡，台詞剪接放錄音"),
    dict(loc="shed_c", cam="Close-up, slow push in", chars=["xuyan"], night="morn",
         comp=f"close-up of {XU2}, framed from the chest up with space above his head, his face three-quarter to screen right toward Tang Xiaotang off screen right, never the lens; at first trying for a joke, then appalled at himself: brows jumping up, eyes going wide; behind him only one rough timber post of the shed and the morning light",
         lines=[("xuyan", "跟著秦霜，進了竹林裡的墳地。", "嘴巴自己說出來")],
         motion=f"Xu Yan opens his mouth to joke and the words come out by themselves; the moment the line ends he claps his right hand over his mouth, eyes wide; {NOSMILE}",
         zh="近景、慢推（身後只有工棚木柱）：許硯想打哈哈，話自己冒出來；說完一掌（右手）摀住嘴、眼睛瞪大；不笑"),
    # Erniu does not smile here (bad-news fright). Tang's silent face: neutral sentence in spec.json.
    dict(loc="shed", cam="Wide group shot, slow push in", chars=["xuyan", "erniu", "tangxiaotang"], night="morn",
         comp=f"wide group shot from the front of the shed, the three of them in a row: on screen left {XU2}, his right hand clapped over his mouth, framed full length, his face three-quarter to screen right, never the lens; eyes wide over his hand; in the middle {ERNIU}, at the stone mortar, both hands still gripping the plain wooden pestle as long as his arm, its end in the mortar, framed full length, his face three-quarter to screen left toward Xu Yan, never the lens; spooked: eyes bulging, brows shot up, mouth stammering between words; on screen right Tang Xiaotang {TANG}, {GOLD}, seated behind the old table, her hand frozen in the air above {ABACUS}, her face three-quarter to screen left toward Xu Yan, never the lens; stunned: brows up, eyes wide, lips closed; {STICKS}; exactly three people",
         lines=[("erniu", "墳……墳地？半夜去墳地做什麼？", "嚇到，結巴")],
         motion=f"the pestle slips out of Erniu's hands and drops into the mortar, splashing up white pulp; Erniu stammers it out; Tang Xiaotang's hand stops in mid-air over the abacus; {quiet('Xu Yan and Tang Xiaotang', 'their', True)}",
         zh="群像全景、慢推：左許硯（右手摀著嘴）；中二牛手上的木杵掉進石臼、濺起白漿，嚇到結巴地問（不笑）；右唐小棠撥算盤的手停在半空、嘴閉著；許硯、唐小棠整鏡不說話"),
    dict(loc="shed_c", cam="Close-up, slow push in", chars=["xuyan"], night="morn",
         comp=f"close-up of {XU2}, framed from the chest up with space above his head, his face three-quarter to screen right toward Wang Erniu off screen right, never the lens; serious: brows drawn together, mouth firm, lips moving between words; behind him only one rough timber post of the shed",
         lines=[("xuyan", "這個我不能說。說了，就對不起秦霜。", "認真")],
         motion=f"Xu Yan lowers the hand from his mouth and shakes his head once, firmly; {NOSMILE}",
         zh="近景、慢推（身後只有工棚木柱）：許硯把摀嘴的手放下，認真搖一下頭說；不笑"),
    # Converted: from close behind her at the table; Xu Yan straight ahead of her across it.
    dict(loc="shed", cam="Over-the-shoulder medium shot, slow push in", chars=["tangxiaotang", "xuyan"], nospeak=["tangxiaotang"], night="morn",
         comp=f"over-the-shoulder medium shot from close behind {TBACK}, seated behind the old wooden table in the right foreground with {ABACUS} in front of her; a step away at the left end of the table, a little left of the middle, standing, {XU2}, framed from the waist up with clear space above his head, his face three-quarter to screen right toward her, his eyes on her face just right of the lens, never the lens; cornered: brows up, eyes darting to one side, lips pressed shut; behind him only the vats and the low wall on the left; {STICKS}; exactly two people",
         lines=[("tangxiaotang", "沒被她砍就好。那我問你，我跟她誰好看？", "先笑一聲，再嘟嘴")],
         motion=f"the young woman props her chin on the back of her right hand (on screen right), her elbow on the table; {HEADSTILL}; Xu Yan's eyes dart aside and come back; {quiet('Xu Yan')}",
         zh="【改背後拍】過肩中景、慢推（審稿必改 4：守住第二場的軸線，她的背在畫右前景）：前景右只有唐小棠的後腦、雙丸子頭、兩條長粉緞帶、淡桃粉衣肩（臉與嘴不入鏡），坐在木桌後，右手（畫右）托下巴、手肘撐桌，頭始終不轉；許硯站在桌子左端、畫面中偏左，朝畫右看她，眼神閃一下又回來、嘴閉著。台詞 nospeak，剪接放錄音；spec.json 拿掉她三張臉部參考圖與身分句"),
    # Xu Yan may grin here (the script).
    dict(loc="shed_c", cam="Close-up, slow push in", chars=["xuyan"], night="morn",
         comp=f"close-up of {XU2}, framed from the chest up with space above his head, his face three-quarter to screen right toward Tang Xiaotang off screen right, never the lens; guilty and honest at once: brows up, eyes sheepish, lips moving between words, then a sheepish closed-lipped grin; behind him only one rough timber post of the shed",
         lines=[("xuyan", "妳低頭算帳的時候，最好看。", "真話，說完自己笑開")],
         motion="Xu Yan tries to play dumb, but the truth comes out first; he freezes for a beat at his own words, then a sheepish grin breaks across his face, lips closed",
         zh="近景、慢推（身後只有工棚木柱；審稿必改 4：朝畫右的她）：許硯想裝傻，真話先出口；說完自己愣一下，忍不住笑開（本鏡可以笑，嘴閉著）"),
    # Her one smile (the script): bowed over the abacus, a silent face (spec.json: the face half of the neutral sentence only).
    dict(loc="shed_c", cam="Medium close-up, slow push in", chars=["tangxiaotang"], night="morn",
         comp=f"medium close-up of Tang Xiaotang {TANG}, seated at the old wooden table, framed from the chest up with space above her head, her head bowed low over {ABACUS}, her face three-quarter to screen left and turned down to the abacus, never the lens; flustered: a pink flush spreading over her cheeks up to her ears, her lips pressed together hard to hold back a smile, the corners of her mouth twitching up anyway, a dimple showing in one cheek, her lips closed, her eyes on the abacus the whole shot; behind her only one rough timber post and the morning light",
         lines=[("xitong", "叮。唐小棠，好感加一。", "冷，公事公辦"), ("xitong", "對，只有一。", "冷，停半拍，挖苦")],
         panel=[("唐小棠 好感 +1 → 18", "panel")],
         motion=f"Tang Xiaotang ducks her head and flicks the beads of the wooden abacus fast with her right hand, never looking up; her head stays bowed until the last frame; {SILENT_SHE}",
         zh="中近景、慢推（身後只有木柱）：唐小棠低頭猛撥算盤（右手），臉一路紅到耳根，嘴角藏不住地往上翹（本鏡可以笑，嘴閉著）；不說話、不抬頭（系統兩句畫外；面板只疊好感一行，吐槽不出面板）"),
    # A thought: his silence written (bible rule 15). No blue light.
    dict(loc="shed", cam="Medium shot, slow push in", chars=["xuyan"], night="morn",
         comp=f"medium shot past the corner of the old wooden table in the right foreground with {LEDGERS} on it: {XU2}, framed from the waist up with clear space above his head, his face three-quarter to screen right toward the young woman off screen right, never the lens; wry: one brow cocked, lips closed the whole shot; behind him only the vats and the low back wall; {STICKS}",
         lines=[("xuyan", "一也是加。總比被秦霜那把刀砍了強。", "自我安慰", "inner")],
         motion=f"Xu Yan pulls a low wooden stool up to the table and sits down on it, then reaches over and drags one account book off the stack toward himself; {SILENT_HE}; he is thinking, not speaking; {NOSMILE}",
         zh="中景、慢推、前景右是木桌角與帳冊：許硯拉一張木凳在桌邊坐下，伸手把一本帳冊拉到面前；嘴一直閉著（心裡話，剪接放錄音）。不寫藍光"),
    # Converted: from close behind her; Xu Yan seated straight ahead of her across the table. Hands by screen side.
    dict(loc="shed", cam="Over-the-shoulder medium shot, slow push in", chars=["tangxiaotang", "xuyan"], nospeak=["tangxiaotang"], night="morn",
         comp=f"over-the-shoulder medium shot from close behind {TBACK}, seated behind the old wooden table in the right foreground; on the table {ABACUS}, the stack of plain blue cloth-covered account books on screen right at her right hand, and one open account book lying flat whose pages are blank; seated on a low stool at the left end of the table, a little left of the middle, {XU2}, framed from the waist up with clear space above his head, his face three-quarter to screen right toward her, his eyes on the book and then on her face just right of the lens, never the lens; mild and honest, lips pressed shut; behind him only the vats and the low back wall; {STICKS}; exactly two people",
         lines=[("tangxiaotang", "十本對完，一筆都沒錯。你今天怎麼這麼老實？", "滿意，又起疑")],
         motion=f"Xu Yan taps one place on the open book; she flicks two beads with her right hand (on screen right), then closes the book and lays it on top of the stack on screen right; {HEADSTILL}; {quiet('Xu Yan')}",
         zh="【改背後拍】過肩中景、慢推（審稿必改 4：她的背在畫右前景）：前景右只有唐小棠的後腦與肩；桌上素木算盤、畫右她右手邊一摞藍布面帳冊、一本攤開的帳冊（頁面空白）；許硯坐在桌子左端的矮凳上、畫面中偏左，朝畫右看她，指一處，她右手（畫右）撥兩下算盤，把這本闔上放到畫右那摞上，頭始終不轉；許硯嘴閉著。台詞 nospeak，剪接放錄音"),
    # Xu Yan may give a wry closed-lip smile here (the script: 苦笑).
    dict(loc="shed_c", cam="Close-up, slow push in", chars=["xuyan"], night="morn",
         comp=f"close-up of {XU2}, seated at the table, framed from the chest up with space above his head, his face three-quarter to screen right toward Tang Xiaotang off screen right, never the lens; resigned: brows lifted, a wry closed-lipped half-smile, lips moving between words; behind him only the low back wall of the shed",
         lines=[("xuyan", "今天說不了假話，就乾脆老實一天。", "苦笑")],
         motion="Xu Yan shrugs one shoulder and pushes the account book back along the table toward screen right, toward her",
         zh="近景、慢推（身後只有棚後矮牆）：許硯坐著聳一下肩，把帳冊往畫右推回她那邊說（審稿必改 4：朝畫右）（本鏡可以苦笑，嘴閉著、不露牙）"),
    # Converted: from behind her as she walks away toward the bright open side; she never turns (the script's 回頭 is dropped).
    dict(loc="shed", cam="Medium shot, slow push in", chars=["tangxiaotang"], nospeak=["tangxiaotang"], night="morn",
         comp=f"medium shot from behind: {TBACK}, {GOLD}, standing beside the old wooden table, its near corner at the right edge of the frame, her right hand (on screen right) resting on the stack of ten plain blue cloth-covered account books on that corner, tied together with a cord, their covers plain unbroken dark blue cloth, her back to us, the bright open side straight ahead of her; beyond the open side only the sunny bare ground and green trees, nobody there; {STICKS}; nobody else in the frame",
         lines=[("tangxiaotang", "帳對完，我去縣城書坊問價。紙做出來，總得有人收。", "說走就走，回頭交代")],
         motion=f"the young woman takes her right hand (on screen right) off the tied stack of books, smooths her skirt once and walks on toward the sunlight at the open side, stopping at its edge; {HEADSTILL}",
         zh="【改背後拍】中景、慢推：從背後拍唐小棠站在木桌邊（桌角在畫右緣）、右手按著桌角那摞用繩子捆好的帳冊，亮著的開口在她正前方；她右手（畫右）放開帳冊、拍一下裙子、走到開口邊停住，頭始終不轉（稿子的「在開口回頭說」不拍）。台詞 nospeak，剪接放錄音"),
    # ---- scene 3: the shed in the afternoon, then at sunset (the open side on screen right, the drying wall at the back).
    dict(chapter="第一張白紙", loc="pm", cam="Wide shot, slow push in", chars=["shimujiang", "xuyan", "erniu"], night="pm",
         comp=f"wide shot past the rim of the pulp vat in the left foreground: on screen right {CARP}, ducking in under the eave through the open side with {MOULD} on his right shoulder, framed full length with clear space above his head, his face three-quarter to screen left toward Xu Yan, never the lens; gruff: brows down, jaw set, lips moving between words; on screen left {XU2}, turning toward him from the vat, framed full length, his face three-quarter to screen right, never the lens; at the back by the second vat {ERNIU}, {PADDLE} in his hands, his face three-quarter to screen right; {STICKS}; exactly three people",
         lines=[("shimujiang", "竹簾趕出來了。熬了一夜一天，比說好的早。", "粗聲，不笑")],
         motion=f"Carpenter Shi swings the mould down off his shoulder and stands it upright against the side of the pulp vat; {quiet('Xu Yan and Wang Erniu', 'their', True)}; {NOSMILE}",
         zh="全景、慢推、前景紙漿桶邊：畫右石木匠從開口彎腰進來，右肩扛竹簾（木框、很密的細竹絲、正中一片柳葉），放下來立在紙漿桶邊，粗聲說、不笑；畫左許硯從桶邊轉身；後面二牛拿木攪棒在另一個桶邊；許硯、二牛不說話"),
    dict(loc="pm", cam="Medium shot, slow push in", chars=["shimujiang"], night="pm",
         comp=f"medium shot: {CARP}, one calloused hand on the top edge of the papermaking mould standing against the vat, framed from the knees up with clear space above his head, his face three-quarter to screen left toward Xu Yan off screen left, never the lens; suspicious: deep frown lines bunched, eyes squinting sideways, lips moving between words; behind him the low back wall and, beyond his shoulder on the right, the bright open side; nobody there; {STICKS}",
         lines=[("shimujiang", "我問你，縣太爺真要這紙？", "懷疑")],
         motion=f"Carpenter Shi squints sideways at the young man and takes half a step closer, his hand staying on the mould; {NOSMILE}",
         zh="中景、慢推：石木匠一手搭在竹簾框上，皺紋擠在一起、瞇眼斜看畫左外的許硯，往前湊半步問；不笑"),
    dict(loc="pm_c", cam="Close-up, slow push in", chars=["xuyan"], night="pm",
         comp=f"close-up of {XU2}, framed from the chest up with space above his head, his face three-quarter to screen right toward Carpenter Shi off screen right, never the lens; trying to stay polite, then giving himself away: brows up, lips moving between words, then his face screwing up; behind him only one rough timber post of the shed",
         lines=[("xuyan", "不是。縣令那句，是我昨天騙你的。", "嘴不聽話")],
         motion=f"Xu Yan starts to answer politely, but the confession comes out instead; after the last word he screws up his face and shuts his eyes tight; {NOSMILE}",
         zh="近景、慢推（身後只有工棚木柱）：許硯想客氣地答，嘴卻先招了；說完皺臉閉眼；不笑（稿子的「客氣的笑」不寫：笑一寫就收不住）"),
    dict(loc="pm", cam="Medium shot, slow pan right", chars=["shimujiang"], night="pm",
         comp=f"medium shot keeping him in the frame as he moves from the vat toward the open side on screen right: {CARP}, framed from the knees up with clear space above his head, his face three-quarter to screen right toward the open side, never the lens; furious: brows slammed down, jaw clenched, eyes hard, teeth gritted between words; beyond the open side only bare ground and trees, nobody there; {STICKS}",
         lines=[("shimujiang", "秀才果然都一個樣，這簾子我扛回去！", "火了")],
         motion=f"Carpenter Shi's face darkens; he heaves the mould up onto his left shoulder, the shoulder away from the camera, in one swing, turns toward the open side and strides off, saying it over his shoulder with his eyes ahead; {NOSMILE}",
         zh="中景、慢慢往右搖（跟著石木匠由左往右）：石木匠臉一沉，一把把竹簾扛上左肩（離鏡頭遠的那側，審稿必改 5：扛右肩會擋臉），轉身往右邊開口走，眼睛看前面、邊走邊說；咬牙、不笑"),
    dict(loc="pm", cam="Medium shot, slow push in", chars=["xuyan"], night="pm",
         comp=f"medium shot: {XU2}, framed from the knees up with clear space above his head, his face three-quarter to screen right toward the carpenter's back off screen right, never the lens; steady and sincere: brows level, eyes firm, lips moving between words; behind him only the vats and the low back wall; {STICKS}",
         lines=[("xuyan", "騙你是我不對。可一成紅利是真的，圖也是我畫的。", "認錯，很穩")],
         motion=f"Xu Yan takes one step after him and reaches his right hand out toward the carpenter's back off screen right, then stops it in mid-air and lowers it; {NOSMILE}",
         zh="中景、慢推：許硯往前追一步，右手伸向畫右外石木匠的背、停住放下，眼神很穩地說；不笑"),
    # The carpenter's mouth may ease (the script: 嘴角一鬆), never a smile.
    dict(loc="pm_c", cam="Close-up, slow push in", chars=["shimujiang"], night="pm",
         comp=f"close-up of {CARP}, at the edge of the open side with the papermaking mould on his left shoulder, the shoulder away from the camera, his body still facing the open side on screen right, framed from the chest up with space above his head, looking back over his right shoulder toward the young man off screen left, his face three-quarter to screen left, never the lens; grudging: a snort, then one corner of his mouth easing a little, his lips closed between words, lips moving between words; behind him only the bright afternoon light outside the shed, nobody there",
         lines=[("shimujiang", "敢當面認錯的秀才，我還是頭一回見。", "哼一聲，服了")],
         motion="Carpenter Shi stops, looks back over his right shoulder and snorts; then he swings the mould down off his left shoulder and holds it upright in front of him with both hands",
         zh="近景、慢推（身後只有開口外的午後光）：石木匠停在開口、竹簾在左肩（遠側）、從右肩回頭（看畫左外的許硯），哼一聲、嘴角一鬆（不笑、不露牙）說，把竹簾從肩上放下來兩手扶著"),
    dict(loc="pm", cam="Wide shot, slow push in", chars=["xuyan", "shimujiang", "erniu"], night="pm",
         comp=f"wide shot from the left side of the shed, the rim of the stone mortar soft in the right foreground: in the middle of the frame the nearer big vat full of milky pulp, and holding {MOULD} between them by its two ends, on screen left {XU2}, framed full length with clear space above his head, his face three-quarter to screen right toward the carpenter, never the lens; intent, lips closed; on screen right {CARP}, framed full length, his face three-quarter to screen left toward the young man, never the lens; instructing: brows knotted in concentration, lips moving between words; behind them at the second vat {ERNIU}, stirring it with {PADDLE}, his eyes on the mould; {STICKS}; exactly three people",
         lines=[("shimujiang", "左右晃三下，漿要鋪得一樣薄。", "教人，專心")],
         motion=f"together the two of them dip the mould slantwise into the milky pulp and rock it gently left and right three times; {quiet('Xu Yan and Wang Erniu', 'their', True)}",
         zh="全景、慢推（從工棚左側拍，前景右石臼邊虛焦；審稿建議：圖上中間是石臼不是桶）：許硯（畫左）、石木匠（畫右）在前面那個紙漿桶兩邊各抬竹簾一端，斜斜浸進紙漿、左右輕晃三下，石木匠專心教；後面二牛用木攪棒攪泡竹桶（稿子的長竿改木攪棒：長竿會畫成槍）；許硯、二牛不說話"),
    dict(loc="pm_c", cam="Insert close-up, slow tilt up", chars=[], night="pm", act=3,
         comp="insert close-up, the shot opens directly on the papermaking mould lying in the milky white pulp from its very first frame: the fine bamboo strips under the surface, two pairs of hands holding its frame: on the left a young man's bare forearms, his blue-grey sleeves tied back above them with cloth strips; on the right an older man's weathered bare forearms under rolled-up brown sleeves; only the hands, the forearms, the frame and the pulp are in the frame, no face; warm afternoon light",
         lines=[],
         motion="the two pairs of hands lift the mould level up out of the pulp; water runs off the edges of the fine bamboo strips in thin streams and drips back down, leaving one thin, even white layer on the strips",
         zh="插鏡、慢慢往上搖（第一格就是浸在紙漿裡的竹簾）：兩雙手（左是許硯綁起袖子的前臂、右是石木匠捲袖的前臂）把竹簾平平抬出紙漿，水從細竹絲邊緣一縷縷流下，簾上留下一層薄薄、勻淨的白（無台詞）"),
    # The system: both on screen silent. The sheet is matte and blank (bible rules 7, 17: no backlit, no glowing).
    dict(loc="eve", cam="Medium shot, low angle, slow push in", chars=["xuyan", "shimujiang"], night="eve",
         comp=f"low-angle medium shot at sunset: on screen left {XU2}, at the bare low back wall, where one single wet white sheet is pressed flat, the only sheet of paper anywhere in the shed, completely blank, framed from the knees up with clear space above his head, his face three-quarter to screen right toward the open side, never the lens; breathless and hopeful: brows lifted, eyes wide, lips parted then closed; on screen right a few steps away {CARP}, framed from the knees up, his face three-quarter to screen left toward the sheet, never the lens; holding his breath, lips pressed shut; {STICKS}; exactly two people",
         lines=[("xitong", "叮。第一張白紙，完成。", "冷，宣布")],
         panel=[("第一張白紙，完成", "task")],
         motion=f"Xu Yan peels {SHEET} carefully off the warm back wall with both hands, turns and lifts it up toward the low evening sun in the open side; {quiet('Xu Yan and Carpenter Shi', 'their', True)}",
         zh="低角度中景、慢推（傍晚）：許硯在棚後焙紙的土牆前（牆上只貼著這一張，審稿必改 6），兩手從溫熱的牆上揭下這張白紙（霧面、厚、整張空白），轉身舉向開口外的夕陽；畫右石木匠看著紙、屏住氣；兩人整鏡不說話（系統畫外，面板疊上）。不寫藍光、不寫透光發亮"),
    dict(loc="eve_c", cam="Insert close-up, slow push in", chars=[], night="eve", act=3,
         comp="insert close-up from inside the shed looking out toward the open side; the shot opens directly on one sheet of fresh white paper the size of a book page held low in two hands, lit from the front, matte, thick and completely blank, from its very first frame; beyond it, out of focus, the low orange evening sun in the open side; only the fingers and the paper are in the frame, no face",
         lines=[],
         motion="the two hands raise the sheet until the low sun is directly behind it; with the sun behind it the sheet lets the light through softly and evenly, warm cream like a paper window at dusk, and in its very middle one soft-edged willow-leaf shape about a thumb long shows a little brighter than the paper around it, where the paper is thinner; the leaf stays still and keeps its shape, the paper surface stays smooth, plain and still, the light soft and even",
         zh="插鏡、慢推（從棚內朝開口拍；第一格是正面打光的白紙、後面虛焦的夕陽）：兩手把紙舉到太陽正前方，紙像黃昏的窗紙一樣柔柔透光，紙心一片拇指長、比四周亮一點的柳葉形（紙較薄的地方）；葉子不動、不長線條，沒有光芒、閃粒、字（無台詞；審稿必改 10：只有這一鏡寫透光）"),
    dict(loc="eve_c", cam="Close-up, slow push in", chars=["shimujiang"], night="eve",
         comp=f"close-up of {CARP}, framed from the chest up with space above his head, the low golden evening light on his weathered face, his face three-quarter to screen left toward the sheet and the young man off screen left, never the lens; moved: eyes glistening, brows drawn up, chin trembling, lips moving hoarsely between words; behind him only the bright evening light outside the open side",
         lines=[("shimujiang", "比縣城賣的還白。那片柳葉，對著光真看得到。", "聲音發啞，感動")],
         motion=f"the edge of the white sheet reaches into the frame from the left, held by hands off screen; Carpenter Shi reaches out a thick finger and thumb and rubs its edge between them, then slowly shakes his head; {NOSMILE}",
         zh="近景、慢推（身後只有開口外的斜陽）：石木匠伸出粗手指搓著紙邊，眼眶發亮，慢慢搖頭，聲音發啞地說；不笑（是感動）"),
    dict(loc="eve", cam="Medium two-shot, slow push in", chars=["qinshuang", "aling"], night="eve",
         comp=f"medium two-shot past one rough timber post of the open side in the right foreground: just inside the open side, Qin Shuang, {QIN}, setting {BASKET} down on the old wooden table, framed from the knees up with clear space above her head, her face three-quarter to screen left toward the young man off screen left, never the lens; brisk: brows lifted, eyes on the paper in his hands, lips moving between words; a step behind her on screen right {ALING}, {JUG} in her hands, framed from the knees up, her face three-quarter to screen left, never the lens; quiet, eyes on the paper; beyond the open side only bare ground and trees in the evening light, nobody there; {NOBLADE}; exactly two people",
         lines=[("qinshuang", "飯送來了。二牛嚷了一下午，紙到底成了沒有？", "爽快，好奇")],
         motion=f"Qin Shuang sets the basket down on the table and lifts her eyes to the paper; A-ling stops just inside the open side; {quiet('A-ling', 'her')}; {NOSMILE}",
         zh="雙人中景、慢推、前景右是開口的木柱：秦霜（腰帶什麼都沒插）把蓋布的竹籃放上木桌，抬眼看畫左外許硯手上的紙說話；阿令提陶水壺停在開口內、嘴閉著；兩人都不笑"),
    # Xu Yan may smile here (the script). Over Qin Shuang's shoulder (unnamed); A-ling steps closer.
    dict(loc="eve", cam="Over-the-shoulder medium shot, slow push in", chars=["xuyan", "aling"], night="eve",
         comp=f"over-the-shoulder medium shot from close behind {QIN_BACK}, in the right foreground; on screen left {XU2}, framed from the waist up with clear space above his head, holding {SHEET} up between his two hands toward the low sun, his face three-quarter to screen right toward the women, never the lens; proud: eyes bright, the corners of his mouth turned up as he talks; in the middle a step nearer than before {ALING}, {JUG} in her left hand, framed from the waist up, her face three-quarter to screen left toward the sheet, never the lens; intent: eyes fixed on the middle of the sheet, lips closed; {NOBLADE}; exactly three people, the young woman in the foreground seen only from behind",
         lines=[("xuyan", "成了。妳們看，對著光有一片柳葉。還差九十九張。", "得意，笑")],
         motion=f"Xu Yan holds the sheet up toward the low sun in the open side so they can look through it; A-ling takes one step closer, her eyes on the middle of the sheet; the young woman in the foreground keeps her head still, the back of her head toward us the whole shot; {quiet('A-ling', 'her')}",
         zh="過肩中景、慢推：前景右只有秦霜的後腦與高馬尾（不點名、不送圖）；畫左許硯把白紙轉過來對著她們、對著光說（本鏡可以笑，嘴閉著）；中間阿令往前一步，眼睛停在柳葉上、嘴閉著、不笑"),
    # Converted: from close behind her as she bursts in; Xu Yan straight ahead of her. Her sheet shows only its blank back.
    dict(loc="eve", cam="Over-the-shoulder medium shot, slow push in", chars=["tangxiaotang", "xuyan"], nospeak=["tangxiaotang"], night="eve",
         comp=f"over-the-shoulder medium shot from close behind {TBACK_RUN}; the young woman has just stumbled in through the open side and stops short in the right foreground, one hand on the timber post at the right edge of the frame; facing us straight ahead of her a step away {XU2}, framed from the waist up with clear space above his head, the white sheet still raised beside his face, his eyes on her face just right of the lens, never the lens; startled: brows jumping up, his smile gone, lips pressed shut; behind him only the low back wall in the evening light; {NOBLADE}; exactly two people",
         lines=[("tangxiaotang", "出事了！書坊行會剛貼的告示，我撕回來了！", "喘，急")],
         motion=f"her right hand (on screen right) braces on the post, her shoulders heaving; then she thrusts {CRUMPLED} up in her left hand (on screen left) toward his face; {HEADSTILL}; {quiet('Xu Yan')}",
         zh="【改背後拍】過肩中景、慢推：前景右只有唐小棠的後腦（髮髻跑亂、一條緞帶鬆了）與起伏的肩，第一格已衝進開口停在畫右前景，右手（畫右）撐著畫右緣的木柱、肩膀起伏，左手（畫左）把一張揉皺的紙往他面前一舉（紙背朝我們、空白、不透光），頭始終不轉；許硯在她正前方，白紙還舉在臉旁，笑一下收掉、嘴閉著。台詞 nospeak，剪接放錄音"),
    dict(loc="eve_c", cam="Close-up, slow push in", chars=["xuyan"], night="eve",
         comp=f"close-up of {XU2}, framed from the chest up with space above his head, the edge of the white sheet beside his face, his face three-quarter to screen right toward Tang Xiaotang off screen right, never the lens; sobering: the warmth leaving his face, brows drawing together, jaw tightening, lips moving between words; behind him only the warm low back wall",
         lines=[("xuyan", "什麼告示？上面寫的跟我們有關？", "笑收掉，沉下來")],
         motion=f"Xu Yan's brows draw together and he slowly lowers the white sheet from beside his face; {NOSMILE}",
         zh="近景、慢推（身後只有焙紙土牆）：許硯臉上的笑收掉、眉頭皺起，把白紙從臉旁慢慢放低說；不笑"),
    # Converted: from close behind her; Xu Yan straight ahead of her (review.md 必改 11: a two-shot like s40; Qin Shuang and
    # A-ling stood at the open side in s38-s39, so they are not moved behind him; the carpenter and Erniu off screen).
    dict(loc="eve", cam="Over-the-shoulder medium shot, slow push in", chars=["tangxiaotang", "xuyan"], nospeak=["tangxiaotang"], night="eve",
         comp=f"over-the-shoulder medium shot from close behind {TBACK_RUN}, in the right foreground, holding {CRUMPLED} up at chest height in both hands toward the young man; facing us straight ahead of her a step away {XU2}, framed from the waist up with clear space above his head, the white sheet in his hands, his eyes on her face just right of the lens, never the lens; stricken: brows knotted, jaw clenched, lips pressed shut; behind him only the bare low back wall in the evening light; {NOBLADE}; exactly two people, the young woman in the foreground seen only from behind",
         lines=[("tangxiaotang", "柳溪白紙，縣城一張不收。我才問了一句價錢！", "一個字一個字，聲音發抖")],
         motion=f"the young woman's fingers crumple the edges of the sheet and it trembles in her hands; Xu Yan slowly lowers his white sheet to his side; {HEADSTILL}; {quiet('Xu Yan')}",
         zh="【改背後拍】過肩中景、慢推（從中景推到中近景；審稿必改 11：收成兩人鏡，秦霜、阿令留在 s38–s39 的開口邊，石木匠、二牛都在畫外）：前景右只有唐小棠的後腦與肩（髮亂、緞帶鬆），兩手把揉皺的紙舉在胸前對著許硯（紙背朝我們、空白），手指把紙邊捏皺、紙在抖，頭始終不轉；許硯在她正前方，手上的白紙慢慢放低，皺眉咬牙、嘴閉著（結尾，懸念接第 15 集）。台詞 nospeak，剪接放錄音（她就在前景，錄音當在場聲音混，不加畫外的空間感）"),
]

HEAD = [
    "- 重製版 r2、真人版（站主 2026-11-11「之後都用真人版」）：照 `docs/videos/zhong-tian-qu-qi-e014-r2/script.md`（c01–c42 對應 s01–s42；2026-11-06 的 r2 稿；含「這版改了什麼」「2026-11-06 審稿後的修改」與「真人版的改動（2026-11-15）」）；台詞一字不改，只改拍法；每鏡一個看得見的動作、一句一筆不拆半句、預設不笑。篇章設定 `production/r2-bible-e011-e020.md`（拍法 1–17 條）。",
    "- 內部工作編號 914（`hailuo/{ff,clips}-dh-e914.json`、`colab/runs/e914/extras.json`、`colab/runs/e914-live/spec.json`，工作資料夾 `~/mokaair-work/videos/zhong-tian-qu-qi-e914-dh/`）；發布 slug `zhong-tian-qu-qi-e014-r2`。不放集數、不放片名卡；s01 接第 13 集 s42（同一刻、同一個機位：從許硯背後拍，柴刀在她右手、刃口停在他頸側）。",
    "- 照第 13 集獨立審稿（`writer-tools/e013-r2/review.md`）與第 11、12 集草稿挑片（`colab/runs/e911-live`、`e912-live`）學到的寫法一開始就照做：`OFFSCREEN_SPEECH = False`；畫外句、心裡話、系統句與錄音鏡，畫面上每個人寫「says nothing… no mouthing words」；不寫劇本沒有的背景人物，每個場景句寫背後有什麼、沒有靠著的長桿；不要火的地方寫 no fire in the frame（竹林的火只有墳前快燒完的紙錢，寫明沒有盆、沒有火盆）；冷臉寫成皺眉、咬牙、別開眼；雙人鏡寫明鏡頭在哪一側、看的人在畫面哪一邊外。",
    "- 唐小棠六句台詞都不露嘴、放錄音（nospeak）：s16 是她手按素木算盤的插鏡；s20、s24、s26、s40、s42 從她背後拍（第二場她的背都在畫右前景）、對方在她前面、頭始終不轉；spec.json 拿掉她三張臉部參考圖與身分句。她不說話的臉（s15、s18）用第 7 集的中性外貌句；s22 是她唯一可以笑的鏡（低頭撥算盤、臉紅、抿嘴憋笑、一邊梨渦、不露牙、頭一直低著），只換臉部那半句。",
    "- 兵器：秦霜的柴刀只在 s01、s03、s05、s07，一把固定描述的舊柴刀，在她右手、寫成「她身體畫左那側、靠他那隻手」（bible 拍法第 5 條），刃口朝他、不換手；s01、s05 從許硯背後拍（不點名、不送圖）；許硯的近景 s02、s04 是下巴以上的大近景（脖子與抵著的刀都框出去，審稿必改 2），s06、s08 寫明畫面裡沒有刀。稿子 c07「插回腰帶」不拍（腰上掛東西會畫成刀鞘）：刀垂在大腿邊、她站著不動（轉身交給剪接，審稿必改 3）；s09 起沒有人拿刀。",
    "- 走廊用第 9 集夜景 `set-xujia-zoulang-l1`（門在右牆、左邊木柱、門與門之間牆上小燭、盡頭偏左是通院子的門口），不另畫：阿令從右牆最近的那扇房門出來，許硯從盡頭的門口進來；s10–s14 側面拍（許硯畫左、阿令畫右）；s10 的場景句只寫側拍看得到的右牆（審稿必改 9）。稿子「手臂橫在他面前」改成站到他面前擋住（側拍時手臂會伸向鏡頭）。",
    "- **獨立審稿**（`writer-tools/e014-r2/review.md`，2026-11-15，必改 12、建議 17）已照改，採納情形見 review.md 最後：竹林重畫 `set-zhulin-fen-l3`、工棚改一版 `set-gongpeng-l2`（`live-action/screen-test-e014.py`，**兩張圖進 refs-live 之前不拍**）；s02、s04 改下巴以上大近景；s07 不轉身；第二場 s20–s25 守同一側（她的背在畫右前景）；s30、s32 竹簾扛左肩；焙牆是空的；早上的光照圖從左上；s15 揉眼睛；s10 側拍的場景句；s36 唯一寫透光；s42 收成兩人鏡；a06、a10 句中停頓剪到 0.4 秒。",
    "- 工棚 `set-gongpeng-l2`（從 l1 改：拿掉地上格柵、桶裡交叉的木棍、最左邊捆起的長竿，光照舊）：開口在右，左邊兩個大木桶（紙漿在前面那個）、中間石臼、右邊舊木桌、棚後焙紙的矮牆（牆上是空的，s35 只貼一張）；地上是素土；二牛的長竿改成木攪棒（長竿會畫成槍）。第三場午後、傍晚照文字改光。",
    "- 紙：帳冊素藍布封面、攤開的頁面空白；唐小棠帶回來的紙只看得到空白的紙背（提示詞不寫 notice）；第一張白紙霧面、空白；只有 s36 這支插鏡寫紙舉到夕陽前、像黃昏的窗紙一樣透光、紙心一片比四周亮一點的柳葉形（審稿必改 10），不寫 backlit、glowing、不寫 slowly shows。",
    "- 長鏡要買的秒數（BUY）：照 41 句錄音核過（`~/mokaair-work/videos/zhong-tian-qu-qi-e914-dh/audio`，見 `r2.py` 的 BUY 註解）：最長 s24 6.5 秒、s39 6.4 秒（都買 8 秒）；s16 5.8 秒在 6 秒插鏡裡，尾巴延到 s17 開頭約 0.4 秒；台詞約 4 秒以上又有動作、或動作有好幾拍的 19 鏡買 8 秒（含稿子長鏡清單的 c26）；刀的近景 s03、唐小棠背影 s40、收尾兩人鏡 s42 審稿後降回 6 秒；a06、a10 句中一秒的停頓剪到 0.4 秒（原檔在 `audio/long-pause-takes/`）。a04、a21 第一次錄得太快（每秒 6.0、7.1 字）重錄一次，舊的在 `audio/fast-takes/`。",
    "- **拍法第 18 條（2026-11-15）**：提示詞裡被否定的名詞會被畫出來（第 13 集草稿：槍架、斧頭、珠串、竹林的屋頂與燈火），所以本集所有否定清單都改成正面寫在場的東西（光禿的土牆、上面什麼都沒掛也沒靠；只有往上長的竹子；手拿竹柄的白紙燈籠；刀身兩指寬、畫面裡唯一的金屬；說完最後一個字嘴抿平、下巴收緊）；`extras.json` 只留 no subtitles, captions or text 與空氣清澈那句。",
    "- **表上的「秒」欄是 lint 估法**，比錄音短；剪接以錄音長度＋0.5 秒為準。",
]
FOOT = [
    "- **參考圖**（`assets/refs-live/`）：許硯、秦霜、阿令（`aling-portrait-l1`，沒戴鐵鐐）、唐小棠（l1 交領）、王二牛、石木匠（`shimujiang-portrait-l1`，沒有角度圖）；場景 `set-zhulin-fen-l3`（竹林，審稿後從 l2 改：沒有火盆與火星、地上沒有木板、補矮土墳與小空白木牌、只有地上一小堆燒著的紙錢）、`set-xujia-zoulang-l1`（第 9 集夜走廊，不重畫）、`set-gongpeng-l2`（工棚，從 l1 改：拿掉地上格柵、桶裡木棍、最左邊長竿）。兩張新圖在 `live-action/screen-test-e014.py`（種子 37007／37008，manifest `~/mokaair-work/videos/_series/zhong-tian-qu-qi/live-screen-test-e014/e014.json`），**還沒跑**；`prep914.sh` 在兩張圖進 refs-live 之前停住。",
    "- `gen-dh.mjs` 的 SET 不用加：bamboo grove、inside corridor of the Xu farmhouse、work shed 三行都已有；`build-r2.py` 的 EN 也不用加（本集的人都已登記）。共用檔沒改。",
    "- `colab/runs/e914/extras.json`（照 e913：畫面不放字幕、不要霓虹線、珠串與故障效果；拿掉秦霜造型句的柴刀；石木匠的造型句改成宋式交領短工衣、皮圍裙不寫木屑；二牛的 empty-handed 拿掉，他拿木杵、木攪棒）與 `colab/runs/e914-live/spec.json`（`mkspec.py` 產生；種子 9141101／9141102）。",
    "- 免費準備：`prep914.sh`（`DRY=1 REFS=~/mokaair-work/videos/zhong-tian-qu-qi-e914-dh/runpod/refs-dh-e914 VIDEO_JSON=docs/videos/zhong-tian-qu-qi-e014-r2/video.json st1-ep.sh 914` → `pilot.py runpod/a/st1 runpod/live/st1 s01…s42` → `retake.py runpod/live/st1 runpod/live/d1 colab/runs/e914-live/spec.json` → `colab-jobs.json` 加 output_path → `preflight-prompts.py`）。兩張新圖挑好、放進 refs-live 再跑；草稿等 Colab 空出來再拍。",
    "- 配樂：第一場冷 cue（s01 更鼓三聲一個重音，s08「叮」之後轉一點暖，走廊只留低的弦）；第二場輕快喜劇 cue（s18 杵掉進石臼停一拍，s22「叮」後一個挖苦的短音型）；第三場溫暖 cue（s30 石木匠要走時停，s35 揭紙一個亮的重音，s40 唐小棠衝進來音樂收掉，s42 一個沉的重音）。音效表見 script.md〈音樂與音效〉。",
]

# Long shots: seconds to buy. script.md 長鏡清單: c26 at 8. Measured 2026-11-15 against the 41 recordings
# (~/mokaair-work/videos/zhong-tian-qu-qi-e914-dh/audio; e013's test: a shot holds (buy - 0.3) x 1.1 s of speech, half a second
# between lines). Whole files: the longest are a25 6.52 s (s24) and a38 6.36 s (s39), both bought 8; a36 5.92 (s37, 8);
# a16 5.84 s sits in the 6 s insert s16 (5.3 s from the first to the last voiced sound): its tail runs about 0.4 s into s17,
# whose own line a17 starts after 0.54 s of silence (review.md 建議). a04 and a21 came out rushed (6.0 and 7.1 characters a
# second) and were re-recorded once (the first takes are in audio/fast-takes/). review.md 必改 12: the one-second pauses in
# a06 (after 看見妳在哭。) and a10 (after 這時候才回來。) are cut to 0.4 s (4.00 s and 4.32 s now; the originals are in
# audio/long-pause-takes/): a face speaking on screen does not hold still for a second.
# 8 s go to the shots whose line runs about 4 s or more with an action around it, or whose action has several beats: s06,
# s09, s10, s12, s15, s18, s24, s26, s27, s30, s31, s32, s37, s38, s39, and s14 (speak, step aside, turn, go in, shut the
# door), s23 (sit, pull a book, a 3.9 s thought), s33 (dip and rock three times), s35 (peel, turn, lift). review.md 建議: the
# knife close-up s03 (a03 4.88 s), Tang Xiaotang's back s40 (a39 3.52 s) and the two-shot s42 (a41 5.12 s) go back to 6
# (longer only gives the back time to turn, the knife time to change hands). The rest stay at gen-dh's 5 or 6.
BUY = {s: 8 for s in ["s06", "s09", "s10", "s12", "s14", "s15", "s18", "s23", "s24", "s26", "s27", "s30", "s31", "s32", "s33",
                      "s35", "s37", "s38", "s39"]}
