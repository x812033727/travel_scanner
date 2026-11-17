"""Episode 25 remake (r2): the writer spec for ../e001-r2/build-r2.py. Source: docs/videos/zhong-tian-qu-qi-e025-r2/script.md
(c01-c40 = s01-s40; c20, c23 and c40 each split in two: s20/s20b, s23/s23b, s40/s40b; the CG-era r2 script), including its
sections 「這版改了什麼」, 「2026-11-06 審稿後的修改」 and 「真人版的改動（2026-11-17）」, which override the tables. Every line is the
script's, word for word; only the staging changes. Bible: production/r2-bible-e021-e030.md (rules 1-30, the 24->25 and 25->26
hand-overs, the props, people and picture tables). The fifth episode of arc 3 〈搶親〉: the sugar workshop on the third
afternoon, the ferry landing on the sixth night.

Written from the start the way e024-r2/r2.py stands AFTER its independent review (../e024-r2/review.md), with what the two
pickers caught in e921-e924 (colab/runs/e92{1,2,3,4}-live/{review-picks-a,review-picks-b,picks-merged}.tsv, e924-live/fix1):
- OFFSCREEN_SPEECH = False (rule 15): every shot with an off-screen line, a thought or a system line writes the silence of
  each person on screen (quiet(), SILENT_HE). Where a back-view or off-screen character speaks, every face toward the camera
  "says nothing, lips closed, listens"; no word that invites a smile or talk (amused, pleased, grin) on a listener.
- Tang Xiaotang never speaks on camera (rule 3) and, as in e024, never shows her face: every shot of her is from behind,
  "facing straight away from us", head still, just two round buns, one pink ribbon each, the nape bare (TBACK, e924 fix1's
  wording). Her lines: s05, s07, s10, s11, s14 (scene 1), s19 (scene 2), s32, s36, s40 (scene 3) from behind (nospeak;
  spec drops her pictures and identity sentence); s08, s17, s31 off screen; s13, s16, s38 her back in a shot with no line of
  hers (not on chars: unnamed, no picture). The wide shots s01, s09, s22, s31 leave her out (e924 s01: in a wide she turns and
  shows a cheek). The script's close-ups of her face (c05, c10, c11, c14, c16, c36), her tears, the bead she flicks (c05)
  and her turning to Xu Yan (c14) go to the recordings and the sound effects.
- The abacus (rule 20) is in no shot: no insert of it in this script.
- Name only what should be drawn: the paper is blank and plain (rule 17, 27), the letter is "one sheet of plain paper folded
  twice, its outside blank" with "one round dab of dark red wax" (the word for the seal is never written), her father's note
  is "one small strip of plain paper folded twice, its outside blank" and is never unfolded (c39: the script's "opens it,
  the back of the paper toward us" would show the strokes through it); the brush is "one slim bamboo brush with a soft black
  tip" (s11, s12 only), the black on it is never named. Nothing hung is named (signs, boards, banners, lanterns): the jetty is
  "planks", the funnels sit "upside down on a wooden rack".
- The boats (rule 23): only the wide shots s22 and s31 write three, far and soft in the fog; closer shots one bow. The bible's
  blank paper lantern at each bow is a torch fixed upright at the bow (a hung lantern grows marks: e921 s37, e924 s18). No sail,
  no canopy (set-chuan-ye-l1, a small canopy boat, is not sent). Torches on the posts are fixed on top of three of the tall
  posts, nobody holding them (rule 23's exception).
- Sticks and staves only (rule 23, 25; 原版必修: the clerk's stick turned into a gong): the Wei shop boy (bible 〈小角色〉: about
  twenty, thin, a dark red cloth short jacket, a black cloth head wrap; this episode one plain wooden stick; the script's grey
  jacket and red headband are the CG look) and eight men in grey each with "one plain wooden stick as long as his arm, smooth
  and round to its ends"; Qin Shuang "one plain long wooden staff, taller than she is"; her chopping knife is never written
  (bible: 秦霜的柴刀不寫、不拍). The two men's torches of the script are left out (fewer props in the fight).
- Counts written everywhere (rule 25): nine Wei men in s23 (the boy and eight), four in s23b, six in s27 (three youths, three
  Wei men: the script's five against eight in one side-on wide would be thirteen bodies), ten youths only in the wide s31, one
  boatman at the stern of each boat in s22 (the script's two each), two staff tips in s26.
- The shop boy is never named and never sent (no picture): chars never lists him, so his two lines (s23b, s29) are off-screen
  lines by build-r2's rule although he is seen side-on (e024's way); MINOR gives his voice (Alnilam).
- Steward Zheng (zhengbo-portrait-l1, first appearance): tall and thin, a long face, grey goatee and thin moustache, grey hair
  in a small topknot bound with a black cloth band, a dark brown satin long robe (the picture; cast.json's "a little plump ...
  gentle smile ... writing brush" is replaced in colab/runs/e925/extras.json). He may smile politely only in s37 (the script).
- A night set needs a night picture (rule 8, e921): every night shot sends set-dukou-ye-l1 or one of its two free crops.

THE AXES (rule 29: the set picture decides):
- The sugar workshop by day (set-tangfang-l1, its free crop set-tangfang-jia-l1; bible 24->25): the brick stove with its iron
  pan in the LEFT foreground, the long plaster wall on the left with a wooden rack of brown clay funnels set upside down high on
  it and a low bench beneath with a second row standing points down in squat jars (e024 review 必改 3), a round stone basin on a
  pedestal in the middle, the unwalled right side with a wooden railing, the snow and the creek. The picture's low gold sun from
  the right is the script's slanting afternoon sun from the right. Xu Yan by the bench on the LEFT, Wang Erniu by the stone
  basin in the middle, Tang Xiaotang at a plank table in the RIGHT foreground (written; not in the picture), seen from behind.
  The script's shed door on the left is the hand-over's unwalled right side: Erniu has come in from the right.
- The ferry landing at night (set-dukou-ye-l1, crops set-dukou-ye-qiao-l1 and set-dukou-ye-wu-l1): the old narrow jetty runs
  out from the LEFT into the dark water, the water and the far reeds on the RIGHT, thick fog. The boats come out of the fog on
  the RIGHT; the near muddy bank runs along the water's edge at the jetty's foot and rises into a slope on the right, where the
  Wei men come down and run left. Xu Yan, Tang Xiaotang and Erniu on the left; Qin Shuang to Xu Yan's right; Steward Zheng on
  the right (the boat side). Scene 3's back shots keep Tang Xiaotang in the LEFT foreground with Steward Zheng beyond her on the
  right; in s40 Xu Yan crouches on her left.

PLACES (the coordinator's decisions, 2026-11-17; every picture looked at full size; script.md 〈真人版的改動〉):
- The workshop: s01 set-tangfang-l1 (gen-dh's, kept); every other scene-1 shot its free crop set-tangfang-jia-l1 (e024's).
- The ferry landing: the wide shots s22, s31 set-dukou-ye-l1; the shots on the jetty its new free crop set-dukou-ye-qiao-l1
  (the jetty planks, the tall bare posts, fog and dark water); the close shots and the muddy bank (s20, s20b, s23, s23b, s25,
  s27, s28, s29, s33, s40b) its new free crop set-dukou-ye-wu-l1 (fog only, as e923's set-chuan-ye-wu-l1). gen-dh's SET phrase
  "ferry landing" gives set-dukou-l2 (pilot.py's newest set-dukou), swapped by spec.json.
- Inserts and shots with nobody named (s02, s12, s16, s17, s22, s23, s23b, s27, s29, s31, s38, s39) open their motion with
  NOBODY.
- Shared files: build-r2.py's EN gets "zhengbo": "Steward Zheng" (gen-dh's name; he speaks on screen: s33, s35, s37). Two new
  free pictures in refs-live (new ids with their own l1, rule 19; README paragraph).
"""
EP = 925  # internal working number; the published slug is zhong-tian-qu-qi-e025-r2
SLUG = "zhong-tian-qu-qi-e025-r2"
EP_TITLE = "一封信三船甘蔗，爹的字條「囡囡，吃飽沒」（重製版 r2）"
OUTLINE_SECONDS = 197  # script.md: about 197.5 s, 40 shots (18 + 13 + 9)
TARGET_MINUTES = [3, 4]
TITLE = "一封信三船甘蔗，爹的字條「囡囡，吃飽沒」｜種田娶妻打天下 第25集（重製版）"
DESCRIPTION = "全州的紅糖被魏記買光了，二牛從鄰鎮回來，抖著空麻袋：一塊都買不到。許硯說沒有紅糖就拿甘蔗直接熬，可是甘蔗要到江南才有。唐小棠苦笑：江南的甘蔗，有一半姓唐。她寫一封信，三天就有船；可是信一到，唐家知道她在哪，魏家也會知道。許硯坐到她旁邊：妳選，寫或不寫，我都在。第六日夜裡，三船甘蔗靠近柳溪渡口，魏記夥計帶人拿木棍衝下河岸，秦霜帶著少年們護船。唐家老管事鄭伯跳下船，壓低聲音問：老爺跟宰相有一筆舊帳，小姐不知道吧？甘蔗捆裡夾著一張小紙條，是她爹的話：囡囡，吃飽沒？《種田娶妻打天下》第 25 集（重製版）。"
THUMB = ("囡囡，吃飽沒", "s40")
CHARACTERS = ["xuyan", "tangxiaotang", "erniu", "qinshuang", "zhengbo", "weijihuoji", "tangwanjin", "xitong"]
MINOR = {
    "weijihuoji": {"id": "weijihuoji", "name": "魏記夥計",
                   "appearance": "East Asian young man of about twenty, thin, an ancient Chinese Song-dynasty shop boy's dark red cloth short jacket and a black cloth head wrap, one plain wooden stick in his right hand",
                   "voice": {"provider": "gemini", "name": "Alnilam", "style": "標準國語，咬字清楚，台北人平常說話的語調；二十歲左右的店鋪夥計，男聲、年輕、嗓門大，帶人來攔船，兇巴巴地扯開喉嚨喊"}},
}
MUSIC = "one cue per scene: a low heavy piano in a quiet thatched sugar shed on a cold afternoon, one soft accent on a revealed name, strings joining as the mood turns tender, one bright electronic accent; then wind and low drums at night by misty water, one big accent when boats appear, fighting drums, opening into broad strings; then a single erhu over the strings, one low accent on a hidden secret, one soft accent on a small paper note before it ends; ancient Chinese rural drama, no vocals"

# Places (gen-dh SET phrases "sugar workshop" and "ferry landing" in the first words of each LOC; see the docstring).
# The funnels on the rack are "set upside down" (no word for hung things); the right side is "unwalled" (no "open").
SHED = ("a long shed under a deep thatched roof on rough wooden posts, a brick stove with one wide cold iron pan in the left "
        "foreground, a long plaster wall on the left with a wooden rack high on it carrying a row of brown clay funnels set upside "
        "down, and a low wooden bench beneath, where a row of brown clay funnels stand points down, each in a squat clay jar, "
        "their wide mouths at chest height, wooden barrels along the wall, a round stone basin on a pedestal in the middle, the "
        "unwalled right side with a wooden railing, snow and the creek beyond it")
TABLE = "one plain wooden plank table"
LANDING = ("an old narrow wooden jetty running out from the left into the dark still water, tall bare wooden posts standing "
           "beside it, thick drifting fog over the water and a far bank of dry reeds on the right")
TORCHES = "three torches burning on top of three of the tall posts, fixed there, nobody holding them"
LOC = {
    "shed": f"In the sugar workshop by the Liuxi creek on a cold clear winter afternoon: {SHED}; low warm gold afternoon sunlight from the right across the snow and the dirt floor, long shadows",
    "shed_c": "In the sugar workshop by the Liuxi creek on a cold clear winter afternoon, under the thatched shed by the wall of brown clay funnels, in low warm gold afternoon sunlight from the right",
    "landing": f"At the ferry landing on the Liuxi creek at night: {LANDING}; {TORCHES}; cold blue night light, the warm orange glow of the torches on the fog",
    "landing_q": "At the ferry landing on the Liuxi creek at night, on the old narrow wooden jetty: its weathered planks and tall bare wooden posts, thick drifting fog over the dark water; cold blue night light and the warm orange light of a torch burning on top of one post",
    "landing_w": "At the ferry landing on the Liuxi creek at night, in thick drifting fog: cold blue night light and the warm orange light of torches",
    "bank": "At the ferry landing on the Liuxi creek at night, on the muddy bank at the foot of the jetty: a short slope of wet dark mud and dead grass rising to the right, thick drifting fog behind it; cold blue night light and the warm orange light of torches",
}
LIGHT = {
    "shed": "the low warm afternoon light stays unchanged",
    "night": "the warm torchlight and the cold dark of the night stay unchanged",  # no "blue" near "eyes" (preflight eye-glow)
}
# bible rule 15: no "<X> speaks off screen" / "the system voice speaks off screen".
OFFSCREEN_SPEECH = False

# Repeated wording (each prop is one object, written the same way every time).
XU_N = "Xu Yan, in his faded blue-grey scholar's robe patched at one elbow, its sleeves rolled to the forearms"
# the script: the old grey outer coat at night (scenes 2 and 3)
XU_C = "Xu Yan, in an old plain grey cloth outer coat worn open over his faded blue-grey scholar's robe"
ERNIU = "Wang Erniu, in his coarse brown hemp short jacket with rolled sleeves"
QIN = "Qin Shuang, in her dark brown cross-collared short jacket, wide black leather belt and black leather bracers, her high black ponytail"
STAFF = "one plain long wooden staff, taller than she is, smooth and round to its ends"
ZHENG = ("Steward Zheng, the old steward, tall and thin in his dark brown satin long robe, his grey hair in a small topknot bound "
         "with a black cloth band, a neat grey-white goatee")
BOY = ("one thin young shop boy in a dark red cloth short jacket and a black cloth head wrap, one plain wooden stick as long as "
       "his arm, smooth and round to its ends, in his right hand, seen side-on, his face in profile")
WEIMEN = "men in grey cotton short jackets and black cloth head wraps, each holding one plain wooden stick as long as his arm, smooth and round to its ends"
YOUTHS = "youths in plain Song-dynasty cross-collared hemp short jackets and cloth head wraps"
TORCH = "one burning torch held high in his right hand"
BOWL = "one shallow clay bowl heaped with fine white sugar like fresh snow"
SACK = "one empty hemp sack"
PAPER = "one sheet of blank paper, plain and opaque"
BRUSH = "one slim bamboo brush with a soft black tip"
LETTER = "one sheet of plain paper folded twice, its outside blank"
NOTE = "one small strip of plain paper folded twice, its outside blank"
BOAT = ("one long flat-bottomed wooden cargo boat sitting low in the water, piled high with bundles of green-purple sugarcane "
        "tied with straw rope, one torch burning upright at its bow")
BOATS = ("three long flat-bottomed wooden cargo boats sitting low in the water, each piled high with bundles of green-purple "
         "sugarcane tied with straw rope, one torch burning upright at the bow of each")
HANDS = "their hands hold only what is described here"
SILENT_HE = "He says nothing in this shot: his lips stay pressed together from the first frame to the last, his jaw still, no talking, no mouthing words"
NOBODY = "Throughout the shot the set layout stays as it is. The pictures fix the place and the objects only, never the mood. "
# e924 fix1's back-of-head wording (s17, s34): "facing straight away from us", just two buns, one ribbon each, the nape clear
TBACK = ("one young woman seen only from behind, appearing only once: the back of her head with every strand of her black hair "
         "combed smooth and gathered up into just two round buns set high on her head, one bun on each side, one short pink "
         "silk ribbon wrapped around each bun, the nape of her neck bare and clear above a pink inner collar, and her light "
         "peach-pink silk shoulders; the back of her head facing straight away from us the whole time, her head still, her ear "
         "the furthest round her head we ever see")
HEADSTILL = "the young woman with the two high round buns keeps her head still, facing straight away from us, the back of her head toward us the whole shot"


def quiet(who, pr="his", plural=False):
    verb = "say" if plural else "says"
    return f"{who} {verb} nothing in this shot: {pr} lips stay pressed together from the first frame to the last, no talking, no mouthing words"


def only_tang(side=None):
    if not side:
        return "she is the only young woman with two high round buns in the frame"
    return (f"she is the only young woman with two high round buns in the frame, and she stays in the {side} "
            f"foreground from the first frame to the last")


def back(rest, where, side="right", frame="framed from the waist up", facing="facing into the frame toward him", shot="over-the-shoulder medium shot"):
    """Tang Xiaotang seen from behind (rule 3) in a foreground corner; the one she speaks with faces us beyond her."""
    return f"{shot} from close behind {TBACK}, {where} in the {side} foreground, {frame}, {facing}; {only_tang(side)}; {rest}"


def alone(rest, where, frame="framed from the waist up"):
    """Tang Xiaotang alone from behind, in the middle of the frame (not at an edge: the pickers' cheek at the frame edge)."""
    return f"medium shot from close behind {TBACK}, {where} in the middle of the frame, {frame}, facing straight away from us; {only_tang()}; {rest}"


SHOTS = [
    # ---- scene 1: the third afternoon, the sugar workshop (24->25: Erniu has come in from the right; Xu Yan holds the bowl).
    dict(chapter="柳溪糖坊", loc="shed", cam="Wide shot, slow push in", chars=["erniu", "xuyan"], night="shed",
         comp=f"wide shot down the shed: on the left by the low bench along the wall {XU_N}, framed full figure, holding {BOWL} in both hands at his chest from the first frame, his face three-quarter to screen right toward Wang Erniu, never the lens; listening: lips pressed shut; in the middle by the stone basin {ERNIU}, framed full figure, {SACK} already held upside down by its bottom corners in both hands from the first frame, his face three-quarter to screen left toward Xu Yan, never the lens; crestfallen, not smiling: brows sagging, lips moving between words; {HANDS}; exactly two people",
         lines=[("erniu", "鄰鎮跑遍了，一塊紅糖都買不到！", "垂頭喪氣，不笑")],
         motion=f"Wang Erniu shakes the upside-down sack once, hard, and his shoulders slump as he speaks; {quiet('Xu Yan')}; Xu Yan holds the bowl still",
         zh="全景、慢推（送糖坊圖 `set-tangfang-l1`：灶在左前、漏斗架在左牆、石盆在中、右邊沒有牆、欄杆外是雪與溪；接點 24→25）：左牆矮凳邊許硯兩手捧著那碗白糖、嘴閉著；中間石盆邊二牛第一格已經進棚、兩手抓著倒過來的空麻袋，用力甩一下、肩膀垮下來，不笑地說（原版建議 s03）。稿子『二牛從棚門（畫左）進來、跟拍』改成接點的方向（他從右邊沒牆的那側進來，第一格已經在棚裡；一鏡一個運鏡）；唐小棠這一鏡不拍（第 24 集 s01 的做法：全景裡她會轉頭露臉）"),
    dict(loc="shed_c", cam="Insert close-up, slow push in", chars=[], night="shed",
         comp=f"insert close-up, the shot opens directly on the mouth of {SACK} held upside down by a big man's hands in coarse brown sleeve cuffs, from its very first frame, above the dirt floor; only the two hands, their sleeve cuffs and the sack are in the frame",
         motion=NOBODY + "the hands shake the sack twice and only a little grey dust drifts out of its mouth down to the dirt floor",
         zh="插鏡、慢推（第一格就是麻袋口；送糖坊的免費裁切 `set-tangfang-jia-l1`）：二牛的手（褐色粗布袖口）把倒過來的空麻袋抖兩下，只飄出一點灰（無台詞）"),
    dict(loc="shed_c", cam="Medium close-up, slow push in", chars=["xuyan"], night="shed",
         comp=f"medium close-up of {XU_N}, standing by the low bench along the left wall, framed from the chest up with space above his head, {BOWL} already set down on the bench beside him at the lower edge of the frame from the first frame, his right hand resting on the rim of one brown clay funnel standing in its jar on the bench, his face three-quarter to screen right toward Wang Erniu off screen right, never the lens; sure, not smiling: steady eyes, lips moving between words; behind him the plaster wall, soft; {HANDS}",
         lines=[("xuyan", "沒有紅糖，就從頭來，拿甘蔗直接熬。", "篤定")],
         motion="Xu Yan raps the rim of the funnel twice with his knuckle as he speaks; after the last word he keeps his eyes on Erniu",
         zh="中近景、慢推（送糖坊裁切）：許硯站在左牆矮凳邊，那碗白糖第一格已經放在矮凳上（稿子『放在木板桌上』改放矮凳：一鏡一個動作，碗跟著他），手搭在立在陶罐裡的漏斗口，用指節敲兩下，朝畫右的二牛（畫外）篤定地說，不笑。稿子『走兩步放碗、退回、坐上陶罐』拿掉（一鏡一個動作）"),
    dict(loc="shed_c", cam="Medium shot, slow push in", chars=["erniu"], night="shed",
         comp=f"medium shot of {ERNIU}, standing by the stone basin, framed from the waist up, {SACK} already dropped in a heap on the dirt floor at his feet from the first frame, both open hands already spread at his sides, palms up, his face three-quarter to screen left toward Xu Yan off screen left, never the lens; glum, not smiling: brows drawn together, lips moving between words; behind him the shed in the low gold light, soft; {HANDS}",
         lines=[("erniu", "甘蔗？咱們這邊不長，要到江南才有。", "不笑")],
         motion="Wang Erniu shrugs, his open hands spreading wider as he speaks; after the last word he lets them drop",
         zh="中景、慢推（送糖坊裁切）：二牛的空麻袋第一格已經丟在腳邊，兩手攤開，朝畫左的許硯（畫外）不笑地說（報壞消息不笑）。稿子『把麻袋往灶邊一丟』不拍（一鏡一個動作，丟袋交給音效）"),
    dict(loc="shed_c", cam="Over-the-shoulder medium shot, slow push in", chars=["tangxiaotang", "erniu"], nospeak=["tangxiaotang"], night="shed",
         comp=back(f"both her hands resting on the table top; facing us beyond her by the stone basin, a little left of the middle, {ERNIU}, framed from the waist up, his face three-quarter to screen right toward her, never the lens; puzzled and listening: brows up, he says nothing, his lips closed; behind him the plaster wall and the brown clay funnels, soft; {HANDS}; exactly two people, the young woman in the foreground seen only from behind",
                   f"sitting at {TABLE}"),
         lines=[("tangxiaotang", "江南的甘蔗，有一半是姓唐的。", "苦笑")],
         motion=f"the young woman's shoulders lift in one small rueful shrug as she speaks; {HEADSTILL}; {quiet('Wang Erniu')}; he listens, his brows rising",
         zh="過肩中景、慢推（送糖坊裁切）：前景右唐小棠的背影坐在木板桌後、兩手放在桌上，肩膀一聳、苦笑著說（nospeak，拍法 3）；石盆邊二牛面朝她、嘴閉著、眉毛挑起來聽（背影說話時對面的人一律寫不說話、嘴閉著）。稿子『近景下巴以上、撥一顆算珠』改背影；算珠交給音效（拍法 20）"),
    dict(loc="shed_c", cam="Low-angle close-up, slow push in", chars=["erniu"], night="shed",
         comp=f"low-angle close-up from the height of the stove of {ERNIU}, framed from the chest up with space above his head, his face three-quarter to screen right toward the young woman beyond the right edge of the frame, never the lens; stunned: brows shot up, jaw dropping, lips moving between stammered words; behind him only the thatched roof and its rough wooden beams, soft",
         lines=[("erniu", "姓、姓唐？是妳們唐家的甘蔗田？", "下巴掉下來")],
         motion="Wang Erniu's jaw drops and he leans toward her as he stammers; after the last word he stays gaping",
         zh="低角度近景（灶台高度往上）、慢推（送糖坊裁切）：二牛眉毛挑高、下巴掉下來，朝畫右的唐小棠（畫外）結巴地說（原版建議 s06：表情寫明）；身後只有茅草棚頂"),
    dict(loc="shed_c", cam="Medium shot from behind, slow push in", chars=["tangxiaotang"], nospeak=["tangxiaotang"], night="shed",
         comp=alone(f"{PAPER} already drawn out flat on the table top in front of her from the first frame, both her hands resting on it; beyond her, soft, the plaster wall and the brown clay funnels in the low gold light; {HANDS}",
                    f"sitting at {TABLE}"),
         lines=[("tangxiaotang", "是。鄭伯跟了我爹三十年，管的就是甘蔗船。", "低頭看紙")],
         motion=f"the young woman smooths the sheet flat with both palms, slowly, once; {HEADSTILL}",
         zh="中景（從背後）、慢推（送糖坊裁切）：唐小棠的背影坐在木板桌前、在畫面正中（不在畫緣），面前一張空白的紙第一格已經抽出來，兩手掌撫平一次（nospeak）。紙寫空白不透光（拍法 17）；稿子『低頭』交給錄音（低頭會露側臉）"),
    dict(loc="shed_c", cam="Medium close-up, slow push in", chars=["xuyan"], night="shed",
         comp=f"medium close-up of {XU_N}, sitting on one upturned clay jar by the low bench, his elbows on his knees, framed from the chest up with space above his head, his right thumb already at his chin from the first frame, his face three-quarter to screen right toward the young woman beyond the right edge of the frame, never the lens; thinking, listening: one brow lifted a little, lips pressed shut; behind him the brown clay funnels in their jars on the bench, soft",
         lines=[("tangxiaotang", "我寫一封信給鄭伯，三天就有船。", "輕聲")],
         motion=f"Xu Yan slowly rubs his chin with his thumb, his eyes on her; {SILENT_HE}; he is listening, not speaking",
         zh="中近景、慢推（送糖坊裁切）：許硯坐在倒扣的陶罐上、手肘撐膝，拇指慢慢摸下巴，看著畫右的唐小棠（畫外）；全程嘴閉著（她的台詞畫外）"),
    dict(loc="shed_c", cam="Medium shot, slow push in", chars=["erniu"], night="shed",
         comp=f"medium shot of {ERNIU}, standing by the stone basin, framed from the knees up, his right hand already raised from the first frame, his face three-quarter to screen right toward the young woman beyond the right edge of the frame, never the lens; eager: brows up, eyes bright, a hopeful smile, lips moving fast between words; behind him the shed in the low gold light, soft; {HANDS}",
         lines=[("erniu", "三天就有船，那還等什麼？快寫啊！", "一拍大腿")],
         motion="Wang Erniu slaps his big hand down on his thigh as he speaks; after the last word he leans toward her, waiting",
         zh="中景、慢推（送糖坊裁切）：二牛一掌拍在自己大腿上，朝畫右的唐小棠（畫外）急著說（本鏡可以笑）。稿子是全景（二牛、許硯、唐小棠三人）：唐小棠在全景的畫右緣會露臉，改成二牛一個人"),
    dict(loc="shed_c", cam="Medium shot from behind, slow push in", chars=["tangxiaotang"], nospeak=["tangxiaotang"], night="shed",
         comp=alone(f"her right hand resting on the table top beside the blank sheet from the first frame; beyond her, soft, the shed and the plaster wall in the low gold light; {HANDS}",
                    f"sitting at {TABLE}"),
         lines=[("tangxiaotang", "信一到，唐家知道我在哪，魏家也會知道。", "笑容收起")],
         motion=f"her right hand slowly closes into a fist on the table top; {HEADSTILL}",
         zh="中景（從背後）、慢推（送糖坊裁切）：唐小棠的背影在桌前、畫面正中，右手在桌上慢慢握成拳，說（nospeak）。稿子『近景下巴以上、看棚外的溪』改背影（看溪要轉頭，會露臉）"),
    dict(loc="shed_c", cam="Medium shot from behind, slow push in", chars=["tangxiaotang"], nospeak=["tangxiaotang"], night="shed",
         comp=alone(f"her right hand already raised from the first frame, holding {BRUSH} just above the blank sheet on the table; beyond her, soft, the shed and the plaster wall in the low gold light; {HANDS}",
                    f"sitting at {TABLE}"),
         lines=[("tangxiaotang", "寫了，我爹就知道我在哪……他會不會派人來帶我回去？", "握著筆，聲音發抖")],
         motion=f"her right hand pulls the brush back a hand's width from the sheet, unsteady, and holds it there above the sheet; {HEADSTILL}",
         zh="中景（從背後）、慢推（送糖坊裁切）：唐小棠的背影在桌前、畫面正中，右手第一格已經拿著細竹筆懸在空白紙上，手一抖、往回縮，聲音發抖地說（nospeak）。筆只寫筆、不寫墨（會長字的字不寫）"),
    dict(loc="shed_c", cam="High-angle insert close-up, slow push in", chars=[], night="shed",
         comp=f"high-angle insert close-up, the shot opens directly on the wet tip of {BRUSH} trembling just above {PAPER} weighed down by one smooth grey stone on {TABLE}, from its very first frame, a small hand in a thick opaque peach-pink silk sleeve cuff holding the brush; only the hand, its sleeve cuff, the brush, the stone and the blank sheet are in the frame",
         motion=NOBODY + "the brush tip trembles and one round black drop falls from it onto the corner of the sheet and spreads into a small round blot",
         zh="插鏡（俯拍）、慢推（第一格就是筆尖；送糖坊裁切）：唐小棠的手（桃粉不透的袖口）握著筆，筆尖一抖，一滴黑落在空白紙角暈開（無台詞）"),
    dict(loc="shed_c", cam="Over-the-shoulder medium shot, slow push in", chars=["xuyan"], night="shed",
         comp=back(f"her hands resting on the table top beside the blank sheet; beside her at the left end of the table, a little left of the middle, {XU_N}, sitting on a low bench, framed from the waist up, his right hand already laid flat on the table top a finger's width from her hand from the first frame, his face three-quarter to screen right toward her, never the lens; gentle and steady: steady eyes, lips moving softly between words; {HANDS}; exactly two people, the young woman in the foreground seen only from behind",
                   f"sitting at {TABLE}", facing="facing the table"),
         lines=[("xuyan", "會不會，我不知道。妳選，寫或不寫，我都在。", "很輕")],
         motion=f"Xu Yan keeps his hand flat on the table and his eyes on her as he speaks, quietly; {HEADSTILL}; {quiet('the young woman', 'her')}",
         zh="過肩中景、慢推（送糖坊裁切）：前景右唐小棠的背影坐在桌前、嘴閉著（不點名、不送圖：她這鏡沒有台詞）；她左邊（畫左）許硯坐在桌頭的矮凳上，手平放在桌上、離她的手一指寬，看著她很輕地說。稿子『從陶罐站起來、坐到長凳上』不拍（第一格已經坐好）"),
    dict(loc="shed_c", cam="Medium shot from behind, slow push in", chars=["tangxiaotang", "xuyan"], nospeak=["tangxiaotang"], night="shed",
         comp=alone(f"beside her on the left, {XU_N}, sitting on a low bench at the left end of the table, framed from the waist up, his right hand flat on the table top, his face three-quarter to screen right toward her, never the lens; listening: he says nothing, his lips closed, his eyes on her; {HANDS}; exactly two people, the young woman seen only from behind",
                    f"sitting at {TABLE}"),
         lines=[("tangxiaotang", "你不勸我？鋪子要是輸了，你也要跟著賠。", "眼眶紅")],
         motion=f"the young woman's shoulders tremble once as she speaks; {HEADSTILL}; {quiet('Xu Yan')}; he listens, his eyes on her",
         zh="中景（從正後方）、慢推（送糖坊裁切）：唐小棠的背影在畫面正中，肩膀抖一下，說（nospeak；眼眶紅、咬唇、轉頭看許硯交給錄音）；她左邊許硯坐著、手平放桌上、看著她、嘴閉著（背影說話時對面的人不說話）"),
    dict(loc="shed_c", cam="Close-up, slow push in", chars=["xuyan"], night="shed",
         comp=f"close-up of {XU_N}, sitting at the plank table, framed from the chest up with space above his head, his face three-quarter to screen right toward the young woman beyond the right edge of the frame, never the lens; tender: a small warm smile at the corners of his mouth, lips moving softly between words; behind him the brown clay funnels in the low gold light, soft",
         lines=[("xuyan", "那是妳的家，回不回、怎麼回，妳說了算。", "溫柔")],
         motion="Xu Yan nods to her once, gently, as he speaks; after the last word he keeps his eyes on her",
         zh="近景、慢推（送糖坊裁切）：許硯對畫右的唐小棠（畫外）輕輕點頭，嘴角一點溫和的笑，溫柔地說（本鏡可以笑）"),
    dict(loc="shed_c", cam="Medium shot from behind, slow push in", chars=[], night="shed",
         comp=alone(f"{BRUSH} already in her right hand from the first frame, resting above the blank sheet on the table; beyond her, soft, the shed and the plaster wall in the low gold light; {HANDS}",
                    f"sitting at {TABLE}"),
         lines=[("xitong", "叮。唐小棠，好感加六。", "冷，宣布")],
         panel=[("唐小棠 好感 +6 → 36", "affection")],
         motion=NOBODY + f"the young woman lifts the back of her left wrist to her eyes once and lowers it, and her right hand holds the brush steady over the sheet; {HEADSTILL}; {quiet('the young woman', 'her')}",
         zh="中景（從背後）、慢推（送糖坊裁切；不送人）：唐小棠的背影在畫面正中，用左手腕背抹一下眼睛、放下，右手把筆拿穩；全程嘴閉著（系統畫外，面板由剪接疊上，拍法 11）。稿子『主觀近景、一滴淚滑下臉頰、嘴角往上』改背影（她整集不露臉）"),
    dict(loc="shed_c", cam="Insert close-up, slow push in", chars=[], night="shed",
         comp=f"insert close-up, the shot opens directly on {LETTER} lying on {TABLE} from its very first frame, a small hand in a thick opaque peach-pink silk sleeve cuff holding one short stick of dark red wax just above its fold; only the hand, its sleeve cuff, the wax and the folded sheet are in the frame",
         lines=[("tangxiaotang", "二牛哥，連夜送到城外鏢局，說給江南唐家的鄭伯。", "囑咐")],
         motion=NOBODY + "the small hand presses the soft dark red wax onto the fold, leaving one round dab of dark red wax, then slides the folded sheet toward the left edge of the frame",
         zh="插鏡、慢推（第一格就是摺好的紙；送糖坊裁切）：桌上一張摺兩摺的紙、外面空白，唐小棠的手把紅蠟按在摺口上，留下一團圓的暗紅蠟，再把紙往畫左推；她的台詞畫外。稿子『在白紙上飛快地寫、對摺』不拍（紙上的字一律不拍，拍法 7、27；寫好、摺好在第一格之前）"),
    dict(loc="shed_c", cam="Medium shot, slow push in", chars=["erniu"], night="shed",
         comp=f"medium shot of {ERNIU}, standing by the plank table, framed from the waist up, {LETTER.replace('folded twice', 'folded twice and closed with one round dab of dark red wax')} already in his right hand from the first frame, his face three-quarter to screen right toward the young woman beyond the right edge of the frame, never the lens; earnest, not smiling: jaw set, lips moving between words; behind him the shed in the low gold light, soft; {HANDS}",
         lines=[("erniu", "交給我，天亮前，一定送到鏢局手上！", "接過信")],
         motion="Wang Erniu tucks the folded sheet into the front of his jacket and pats it twice as he speaks; after the last word he turns toward the unwalled right side of the shed",
         zh="中景、慢推（送糖坊裁切）：二牛手上第一格已經拿著封好的信（摺起、外面空白、一團暗紅蠟），塞進懷裡、拍兩下，不笑、很認真地說，說完轉身往右邊沒牆的那側（結尾；剪在轉身的一半）。稿子『從唐小棠手上接過』不拍（她不入鏡；接信在第一格之前）"),
    # ---- scene 2: the sixth night, the ferry landing (set-dukou-ye-l1 and its crops); the boats from the right.
    dict(chapter="柳溪渡口", loc="landing_q", cam="Medium shot from behind, slow push in", chars=["tangxiaotang", "erniu"], nospeak=["tangxiaotang"], night="night",
         comp=alone(f"facing the fog over the dark water, her hands already pressed together in front of her from the first frame; ahead of her at the far end of the jetty, small and soft, {ERNIU} seen from behind, {TORCH}; {HANDS}; exactly two people, both seen from behind",
                    "standing on the jetty planks"),
         lines=[("tangxiaotang", "信說三天，今天第三天了，船怎麼還不來？", "搓著手，不笑")],
         motion=f"the young woman rubs her hands together against the cold as she speaks; {HEADSTILL}; {quiet('Wang Erniu')}; he stands still at the end of the jetty, holding the torch high",
         zh="中景（從背後）、慢推（送渡口棧橋的免費裁切 `set-dukou-ye-qiao-l1`）：唐小棠的背影在棧橋上、畫面正中，朝霧裡的水，兩手搓著說（nospeak）；棧橋盡頭二牛的背影小小的、右手高舉火把、嘴閉著。稿子的全景（許硯、秦霜、十個少年同框）改成兩個人的背影（人多容易多出分身與半個頭；拍法 25）；踮腳看霧不拍"),
    dict(loc="landing_w", cam="Close-up, slow push in", chars=["xuyan"], night="night",
         comp=f"close-up of {XU_C}, standing on the jetty, framed from the chest up with space above his head, his face three-quarter to screen right toward the fog over the water, never the lens; grim: brows drawn, lips pressed shut; warm torchlight flickering on one side of his face; behind him only the drifting fog in the cold blue night, soft",
         lines=[("xitong", "叮。鬥商第六日，落後兩成。", "冷，宣布"),
                ("xitong", "落後兩成。宿主的白糖，到今天還是那一碗。", "冷")],
         panel=[("鬥商第六日，落後兩成", "task")],
         motion=f"Xu Yan stares into the fog and his chin tucks down a little; {SILENT_HE}; he is listening, not speaking",
         zh="近景、慢推（送渡口的霧色免費裁切 `set-dukou-ye-wu-l1`；稿子 c20 的長鏡在系統句後拆開，一鏡一個表情）：許硯（外披舊灰外衣）看著霧、下巴一收，火光在半邊臉上跳；全程嘴閉著（系統兩句畫外，面板由剪接疊上；稿子『臉被藍光照亮』不寫，拍法 11）"),
    dict(sid="s20b", loc="landing_w", cam="Close-up, slow push in", chars=["xuyan"], night="night",
         comp=f"tight close-up of {XU_C}, framed from the shoulders up with a little space above his head, his face three-quarter to screen right toward the fog over the water, never the lens; dry and stubborn: one corner of his mouth tucked in, lips pressed shut; warm torchlight on one side of his face; behind him only the drifting fog, soft",
         lines=[("xuyan", "一碗也是糖。船一到，就不只一碗。", "心裡話，錄得近、輕", "inner")],
         motion=f"Xu Yan lets out one short breath through his nose, a dry silent snort, and then his jaw sets firm; {SILENT_HE}; he is thinking, not speaking",
         zh="近景（比 s20 再近，肩以上）、慢推（送渡口霧色裁切）：聽完系統挖苦，許硯鼻子裡輕哼一聲、下巴一收、咬定；全程嘴閉著（心裡話畫外）"),
    dict(loc="landing_q", cam="Medium shot, slow push in", chars=["erniu"], night="night",
         comp=f"medium shot of {ERNIU}, standing at the far end of the jetty, framed from the waist up, {TORCH} from the first frame, his face three-quarter to screen right toward the water, never the lens; overjoyed: a huge grin, eyes wide, lips moving fast between shouted words; on the right, out of the fog over the dark water, the dark bow of {BOAT}; behind him the drifting fog; {HANDS}",
         lines=[("erniu", "來了！三條船，船上全是甘蔗！", "舉著火把大叫")],
         motion="Wang Erniu swings the torch over his head and bounces once on his toes as he shouts; after the last word he keeps the torch high",
         zh="中景、慢推（送棧橋裁切）：棧橋盡頭二牛右手高舉火把，在頭上揮、原地跳一下，朝畫右霧裡冒出來的第一條船頭大叫（本鏡可以笑）；船頭一支火把（聖經的空白紙燈籠改火把：掛著的燈籠會長字）。原版建議 s18：不寫推近"),
    dict(loc="landing", cam="Wide shot, slow push in", chars=[], night="night",
         comp=f"wide shot from the shore: the old narrow wooden jetty running out from the left into the dark water, {TORCHES}; on the right, {BOATS}, gliding one behind the other out of the thick fog toward the jetty, far and soft in the fog; at the stern of each boat one boatman in a conical straw hat and a short brown jacket seen from behind, pushing a long pole; exactly three boatmen, small and far",
         motion=NOBODY + "the three boats glide slowly toward the jetty one after the other, the torch at each bow brightening as it comes out of the fog",
         zh="全景、慢推（送渡口夜霧圖 `set-dukou-ye-l1`：棧橋從畫左伸進水裡、右邊是水與遠處蘆葦）：三條堆滿青紫甘蔗捆的平底貨船一條接一條從霧裡滑向棧橋（只有全景寫三條，拍法 23），船頭各一支火把，船尾各一個斗笠船工背影撐篙（稿子每條兩個改一個，寫實際人數）。稿子『慢慢升高』改慢推（一個運鏡、模型讀得懂的字）；岸上的人湧到棧橋邊不拍（無台詞）"),
    dict(loc="bank", cam="Wide shot, slow push in", chars=[], night="night",
         comp=f"wide shot looking along the muddy bank: down the slope of wet dark mud on the right come {BOY.replace('one thin young shop boy', 'at the front one thin young shop boy')}, and behind him eight {WEIMEN}, running down toward the left, everyone small in the frame and side-on, their lips closed; exactly nine men; in the foreground the dead grass on the bank, soft",
         lines=[("qinshuang", "右邊坡上下來九個人，都拿著棍子。", "冷")],
         motion=NOBODY + "the shop boy and the eight men run down the slope toward the left, slipping in the mud, their lips closed, nobody speaking",
         zh="全景、慢推（送渡口霧色裁切；泥岸寫在鏡頭裡）：魏記夥計（暗紅短褂、黑布包頭、一根素面木棍，側面，不點名、不送圖）帶八個灰短打的打手（各一根木棍）從右邊泥坡往畫左衝下來，人小、側面、嘴閉著；秦霜的台詞畫外（稿子 c23 的前半；拆成 s23、s23b：一鏡一個動作，夥計在她說話時不能張嘴）。稿子『從坡頂往下跟拍』改慢推；打手的兩支火把不寫（打鬥少一樣道具）"),
    dict(sid="s23b", loc="bank", cam="Medium shot, slow push in", chars=[], night="night",
         comp=f"medium shot of {BOY}, standing at the foot of the muddy slope, framed from the waist up, his stick already raised and thrust out toward the jetty on the left from the first frame, fierce, not smiling: brows down, lips moving between shouted words; behind him on the slope, soft, three of the {WEIMEN}, side-on, their lips closed; exactly four men; behind them the fog",
         lines=[("weijihuoji", "魏記的人在此，這三船貨，誰也不准卸！", "揮著木棍，兇")],
         motion=NOBODY + "the shop boy jabs his stick toward the jetty as he shouts, his mouth moving with the words; the three men behind him stand still with their sticks, their lips closed",
         zh="中景、慢推（送渡口霧色裁切）：坡腳魏記夥計第一格已經把木棍往畫左的棧橋一指，兇、不笑地喊（原版建議 s19：不咧嘴笑）；身後坡上三個打手虛焦、側面、嘴閉著。拍法 25：夥計中景只拍側面，不拍正臉近景"),
    dict(loc="landing_q", cam="Medium shot, slow push in", chars=["xuyan"], night="night",
         comp=f"medium shot of {XU_C}, standing on the jetty planks, framed from the waist up, his face three-quarter to screen right toward Qin Shuang off screen right, never the lens; firm, not smiling: steady eyes, lips moving between words; warm torchlight flickering on his face; behind him the tall bare posts and the drifting fog, soft",
         lines=[("xuyan", "護船的事，全聽秦霜的。秦霜，妳說怎麼打？", "篤定")],
         motion="Xu Yan takes half a step back as he speaks, giving her the front; after the last word he waits for her answer",
         zh="中景、慢推（送棧橋裁切）：許硯在棧橋上，火光在臉上跳，往後退半步把前面讓給畫右的秦霜（畫外），篤定地說，不笑。稿子右前景的秦霜肩與長棍不拍（畫緣會多出半個頭）"),
    dict(loc="landing_w", cam="Close-up, slow push in", chars=["qinshuang"], night="night",
         comp=f"close-up of {QIN}, standing on the jetty, framed from the chest up with space above her head, {STAFF} upright in her right hand beside her from the first frame, her ponytail lifting in the river wind, her face three-quarter to screen left toward Xu Yan off screen left, never the lens; surprised: brows lifting, lips pressed shut; warm torchlight on her face; behind her only the drifting fog, soft",
         lines=[("xitong", "叮。秦霜，好感加六。", "冷，宣布")],
         panel=[("秦霜 好感 +6 → 29", "affection")],
         motion=f"Qin Shuang's brows lift as she glances at him, and then one corner of her mouth curls up, her lips pressed together; {quiet('Qin Shuang', 'her')}",
         zh="近景、慢推（送渡口霧色裁切）：秦霜高馬尾在河風裡揚起，長棍直立在右手，驚訝地瞄畫左的許硯（畫外）一眼，嘴角一勾、嘴閉著（系統畫外，面板由剪接疊上）。稿子『長棍在手上轉一圈』不拍（一鏡一個動作；轉棍容易畫壞）"),
    dict(loc="landing_q", cam="Medium shot, slow push in", chars=["qinshuang"], night="night",
         comp=f"medium shot of {QIN}, standing on the jetty planks, framed from the waist up, {STAFF} in her right hand from the first frame, her face three-quarter to screen left toward the youths beyond the left edge of the frame, never the lens; commanding, not smiling: brows level, lips moving sharply between words; in the soft left foreground the upright round tips of two long plain wooden staves; behind her the fog over the dark water; {HANDS}",
         lines=[("qinshuang", "五個拿棍在前擋人，五個去岸邊接纜繩拉纖！", "一聲令下")],
         motion="Qin Shuang swings the staff out level at her side as she gives the order; after the last word she holds it level",
         zh="中景、慢推（送棧橋裁切）：秦霜右手長棍，朝畫左的少年們（畫外）一聲令下，說完長棍一橫；前景左虛焦兩根棍尖（不寫人）。稿子『十個少年在她身後排開、分成兩隊』不拍（少年只在全景，聖經〈小角色〉）"),
    dict(loc="bank", cam="Wide shot side-on, slow push in", chars=[], night="night",
         comp=f"wide shot side-on along the muddy bank, the whole action inside the frame: on the left three {YOUTHS}, shoulder to shoulder, each holding one plain long wooden staff level across his chest; on the right three {WEIMEN}, their sticks raised; everyone small in the frame, side-on, their lips closed; exactly six people",
         motion=NOBODY + "the three youths push forward at a walking pace and sweep their staves across, the sticks of two of the men fly spinning out of their hands, and those two men stagger back and sit down hard in the mud",
         zh="全景（側面）、慢推（送渡口霧色裁切）：泥岸上，左邊三個少年肩並肩、長棍平舉，用走路的速度往前推、一掃，右邊三個打手裡兩個的木棍轉著飛出去、往後踉蹌一屁股坐進泥裡（不見血；整個動作留在畫面裡）。稿子五個少年對八個打手改三對三（一個側面全景裡十三個人容易多出分身；寫實際人數）；火把不寫（無台詞）"),
    dict(loc="bank", cam="Low-angle medium shot side-on, slow push in", chars=["qinshuang"], night="night",
         comp=f"low-angle medium shot side-on on the muddy bank, the whole action inside the frame: on the left {QIN}, low in a crouch, framed from the knees up, {STAFF} held in both hands from the first frame, her face in profile to screen right toward the shop boy, never the lens; fierce, not smiling: eyes narrowed, lips pressed shut; on the right {BOY}, his stick raised over his head, his face in profile to screen left, angry, his lips closed; {HANDS}; exactly two people",
         motion=f"Qin Shuang's staff snaps up and knocks the stick out of his hands, the stick spinning away into the dark, and the shop boy stumbles back and sits down hard in the mud; {quiet('Qin Shuang', 'her')}; the shop boy says nothing, his lips closed",
         zh="低角度中景（側面）、慢推（送渡口霧色裁切）：左邊秦霜壓低身子雙手持棍、右邊魏記夥計舉棍（側面）；她的棍子往上一挑把他的木棍挑飛，他往後一跌坐進泥裡；兩人嘴閉著（無台詞；整個動作留在畫面裡）。稿子『再一掃他腳踝、收棍站直』拿掉（一鏡一個動作）；剪在他坐下去的一半"),
    dict(loc="bank", cam="Medium shot side-on, slow push in", chars=[], night="night",
         comp=f"medium shot side-on of one thin young shop boy in a dark red cloth short jacket, his black cloth head wrap knocked crooked, sitting in the mud at the foot of the slope, empty-handed, framed from the waist up, both elbows already planted in the mud behind him from the first frame, his face in profile to screen left toward the jetty, never the lens; frightened and furious, not smiling: eyes wide, lips moving between stammered words; at the left edge of the frame the round tip of one plain long wooden staff held level; behind him the dark slope and the fog; he is the only person in the frame",
         lines=[("weijihuoji", "你、你們等著，我回去告訴少爺！", "坐在泥裡往後退")],
         motion=NOBODY + "the shop boy scrabbles backward up the slope on his elbows and heels as he shouts, his mouth moving with the words",
         zh="中景（側面）、慢推（送渡口霧色裁切）：魏記夥計坐在泥裡、黑布包頭歪了、兩肘撐地，往後手腳並用退上坡，朝畫左的棧橋結巴地喊，不笑；畫左緣是秦霜長棍的棍尖（不點名）。稿子『紅布條歪了』照聖經〈小角色〉寫黑布包頭；打手跟著爬走交給音效"),
    dict(loc="landing_q", cam="Low-angle medium shot, slow push in", chars=["qinshuang"], night="night",
         comp=f"low-angle medium shot of {QIN}, standing at the far end of the jetty, framed from the waist up, {STAFF} in her right hand, her left arm already raised high from the first frame, her ponytail swinging in the firelight, her face three-quarter to screen left toward the youths on the bank beyond the left edge of the frame, never the lens; commanding, not smiling: lips moving sharply between words; beside her on the right the dark bow of {BOAT}; behind her the fog; {HANDS}",
         lines=[("qinshuang", "兩列，跟著我的口令，一起拉！", "手臂一揮")],
         motion="Qin Shuang sweeps her raised left arm down toward the bank as she calls out; after the last word she holds her arm out toward the bank",
         zh="仰角中景、慢推（送棧橋裁切）：秦霜站在棧橋盡頭，身旁（畫右）是剛靠過來的第一條船的船頭與船頭火把，高馬尾在火光裡甩，舉起的左手往畫左的岸上一揮（右手照聖經拿長棍）"),
    dict(loc="landing", cam="Wide shot, slow push in", chars=[], night="night",
         comp=f"wide shot from the shore: the old narrow wooden jetty running out from the left into the dark water, {TORCHES}; in the foreground along the muddy near bank two rows of five {YOUTHS}, side-on and small, each row leaning back and hauling together on one thick taut rope that runs out over the water; on the right, {BOATS}, far and soft in the fog, coming in toward the jetty one behind the other; exactly ten youths; their lips closed",
         lines=[("tangxiaotang", "三船都靠岸了，一根甘蔗都沒落水。", "鬆一口氣")],
         motion=NOBODY + "the youths haul in step and the three boats glide in one after the other until the first one bumps gently against the posts of the jetty",
         zh="全景、慢推（送渡口夜霧圖）：近岸泥地上十個少年排成兩列、側面、小小的，一起往後拉兩條纖繩，三條甘蔗船（遠、霧裡）一條接一條滑向棧橋，第一條輕輕靠上木樁；唐小棠鬆一口氣的台詞畫外（稿子全景裡的唐小棠不拍）（結尾）。稿子『慢慢升高』改慢推"),
    # ---- scene 3: the same night on the jetty; Steward Zheng on the right (the boat side), Tang Xiaotang in the LEFT foreground.
    dict(chapter="棧橋與字條", loc="landing_q", cam="Over-the-shoulder medium shot, slow push in", chars=["tangxiaotang", "zhengbo"], nospeak=["tangxiaotang"], night="night",
         comp=back(f"both her hands already holding his left forearm from the first frame; facing us close beyond her, a little right of the middle, {ZHENG}, standing on the jetty planks at the foot of a short gangplank, framed from the waist up, his face three-quarter to screen left toward her, never the lens; moved, saying nothing: his eyes wet, his lips closed, he listens; behind him the bow of {BOAT}, soft; {HANDS}; exactly two people, the young woman in the foreground seen only from behind",
                   "standing on the jetty planks", side="left"),
         lines=[("tangxiaotang", "鄭伯！你這把年紀，還親自押船來！", "喊，紅了眼")],
         motion=f"the young woman grips his forearm with both hands, her shoulders shaking once as she speaks; {HEADSTILL}; {quiet('Steward Zheng')}; he steadies himself on the planks and looks down at her",
         zh="過肩中景、慢推（送棧橋裁切）：前景左唐小棠的背影兩手第一格已經扶住鄭伯的手臂、肩膀抖一下，喊著說（nospeak）；鄭伯（定妝照 `zhengbo-portrait-l1`：高瘦、灰白山羊鬚、髻上黑布、深褐緞袍）站在跳板腳、面朝她、眼眶濕、嘴閉著；身後船頭與火把。稿子『從棧橋那頭跑過來、從船頭跨下跳板』不拍（一鏡一個動作：第一格已經下船、已經扶著）"),
    dict(loc="landing_w", cam="Medium close-up, slow push in", chars=["zhengbo"], night="night",
         comp=f"medium close-up of {ZHENG}, standing on the jetty, framed from the chest up with space above his head, both hands already raised and clasped together before his chest from the first frame, his face three-quarter to screen left toward the young woman beyond the left edge of the frame, never the lens; moved: eyes wet and red, lips moving between words; warm torchlight on his grey goatee; behind him the dark bow of one cargo boat piled with green-purple sugarcane and its torch, soft in the fog; {HANDS}",
         lines=[("zhengbo", "小姐，老奴一接到信，連夜就裝船了。這位是許公子？", "拱手，紅了眼")],
         motion="Steward Zheng bows over his clasped hands as he speaks, then lifts his eyes past her toward the young man behind her, beyond the left edge of the frame; after the last word he waits",
         zh="中近景、慢推（送渡口霧色裁切）：鄭伯雙手第一格已經拱在胸前，朝畫左的唐小棠（畫外）彎腰說，再抬眼看她身後的許硯（畫外）；火光照灰白山羊鬚，身後虛焦的船頭與甘蔗"),
    dict(loc="landing_q", cam="Medium shot, slow push in", chars=["xuyan", "zhengbo"], night="night",
         comp=f"medium shot on the jetty planks: on the left {XU_C}, framed from the waist up, both hands already raised and cupped together before his chest from the first frame, his face three-quarter to screen right toward Steward Zheng, never the lens; warm and respectful, not smiling: lips moving between words; on the right {ZHENG}, framed from the waist up, his face three-quarter to screen left toward Xu Yan, never the lens; listening: he says nothing, his lips closed; behind them the tall bare posts and the fog, soft; {HANDS}; exactly two people",
         lines=[("xuyan", "我是許硯。鄭伯一路辛苦，三船甘蔗，救了許記。", "")],
         motion=f"Xu Yan bows a little over his cupped hands as he speaks; {quiet('Steward Zheng')}; he listens, his eyes on Xu Yan",
         zh="中景、慢推（送棧橋裁切）：左許硯（外披舊灰外衣）拱手回一個禮說；右鄭伯面朝他、嘴閉著聽。稿子『伸手扶鄭伯站穩』拿掉（一鏡一個動作）"),
    dict(loc="landing_q", cam="Over-the-shoulder medium shot, slow push in", chars=["zhengbo"], night="night",
         comp=back(f"her hands low at her sides; facing us close beyond her, a little right of the middle, {ZHENG}, leaning in toward her, framed from the chest up, his face three-quarter to screen left toward her, never the lens; worried: a deep crease between his kind brows, lips moving low between words; behind him the fog and the torch at the bow, soft; {HANDS}; exactly two people, the young woman in the foreground seen only from behind",
                   "standing on the jetty planks", side="left"),
         lines=[("zhengbo", "小姐，老爺跟宰相，有一筆舊帳，您不知道吧？", "壓低聲音")],
         motion=f"Steward Zheng leans a little closer to her and lowers his voice as he speaks; {HEADSTILL}; {quiet('the young woman', 'her')}",
         zh="過肩中景、慢推（送棧橋裁切）：前景左唐小棠的背影（不點名、不送圖：這鏡她沒有台詞）、嘴閉著；鄭伯湊近她，慈眉中間一道擔憂的皺紋，壓低聲音說。稿子『回頭瞄一眼岸上』拿掉（一鏡一個動作）；稿子『畫面右緣是她的丸子』改左前景（本場她在左、鄭伯在右，不越軸）"),
    dict(loc="landing_q", cam="Over-the-shoulder medium shot, slow push in", chars=["tangxiaotang", "zhengbo"], nospeak=["tangxiaotang"], night="night",
         comp=back(f"her hands low at her sides; facing us close beyond her, a little right of the middle, {ZHENG}, framed from the chest up, his face three-quarter to screen left toward her, never the lens; grave, listening: he says nothing, his lips closed, his eyes on her; behind him the fog and the torch at the bow, soft; {HANDS}; exactly two people, the young woman in the foreground seen only from behind",
                   "standing on the jetty planks", side="left"),
         lines=[("tangxiaotang", "什麼舊帳？不就是八條鹽船嗎？", "愣住，不笑")],
         motion=f"the young woman leans a little toward him as she speaks; {HEADSTILL}; {quiet('Steward Zheng')}; he listens, grave",
         zh="過肩中景、慢推（送棧橋裁切）：前景左唐小棠的背影往前一湊，愣住地問（nospeak；皺眉交給錄音）；鄭伯看著她、嘴閉著、臉色凝重"),
    dict(loc="landing_q", cam="Medium shot, slow push in", chars=["zhengbo"], night="night",
         comp=f"medium shot of {ZHENG}, standing straight on the jetty planks a step back from where he stood, framed from the waist up, his face three-quarter to screen left toward the young woman beyond the left edge of the frame, never the lens; politely smiling: a courteous closed smile that stays out of his eyes, lips moving between words; behind him the bow of {BOAT}, soft; {HANDS}",
         lines=[("zhengbo", "不只是船。老爺說，等小姐見了他，親口說。", "換上笑臉")],
         motion="Steward Zheng draws both hands into his wide sleeves as he speaks, smiling politely; after the last word he gives a small bow",
         zh="中景、慢推（送棧橋裁切）：鄭伯第一格已經退一步站直，兩手攏進袖子裡，客氣地笑著說（本鏡可以客氣地笑），說完微微一躬。稿子左前景唐小棠的肩不拍（畫緣會露臉）"),
    dict(loc="landing_q", cam="Medium shot from behind, slow push in", chars=[], night="night",
         comp=alone(f"in front of her on the planks one bundle of green-purple sugarcane tied with straw rope, both her hands already on its knot from the first frame; beyond her, soft, the dark bow of one cargo boat and its torch in the fog; {HANDS}",
                    "crouching on the wet jetty planks", frame="framed full figure"),
         motion=NOBODY + f"the young woman pulls the straw rope loose and the canes roll apart on the planks, and she goes still; {HEADSTILL}",
         zh="中景（從背後）、慢推（送棧橋裁切；不送人）：唐小棠的背影蹲在濕木板上、畫面正中，解開一捆甘蔗的草繩，蔗稈滾開，她停住（無台詞）。稿子前景扛甘蔗的少年不拍（人少一點；少年只在全景）"),
    dict(loc="landing_q", cam="Insert close-up, slow push in", chars=[], night="night",
         comp=f"insert close-up, the shot opens directly on {NOTE} wedged between two green-purple canes of a loosened bundle lying on the wet dark planks, from its very first frame, a small hand in a thick opaque peach-pink silk sleeve cuff reaching for it; only the hand, its sleeve cuff, the canes and the folded strip are in the frame",
         lines=[("tangwanjin", "囡囡，吃飽沒？", "爹的聲音，慈愛")],
         motion=NOBODY + "the small hand draws the folded strip out from between the canes and holds it, still folded, and one teardrop falls onto it",
         zh="插鏡、慢推（第一格就是夾在蔗稈中間的小紙條；送棧橋裁切）：唐小棠的手把摺兩摺、外面空白的小紙條抽出來、拿著，不打開，一滴淚落在紙上；唐萬金的聲音畫外。稿子『打開、紙背朝鏡頭、透出幾行墨跡』不拍（透出來的筆畫會長字，拍法 7、27）"),
    dict(loc="landing_q", cam="Medium shot from behind, slow push in", chars=["tangxiaotang", "xuyan"], nospeak=["tangxiaotang"], night="night",
         comp=alone(f"both her hands pressed to her chest; beside her on the left, {XU_C}, crouching on the planks, framed from the waist up, his right hand already resting gently on her back from the first frame, his face three-quarter to screen right toward her, never the lens; tender and grave, listening: he says nothing, his lips closed, his eyes on her; behind them the fog and the warm torchlight, soft; {HANDS}; exactly two people, the young woman seen only from behind",
                    "crouching on the wet jetty planks beside the loosened sugarcane"),
         lines=[("tangxiaotang", "吃飽了……爹，囡囡吃得很飽。", "哽住，哭著")],
         motion=f"the young woman's shoulders shake as she sobs and speaks; {HEADSTILL}; {quiet('Xu Yan')}; his hand stays on her back",
         zh="中景（從背後）、慢推（送棧橋裁切）：唐小棠的背影蹲在甘蔗堆旁、兩手把紙條抱在胸口（從背後看不到紙），肩膀發抖、哭著說（nospeak）；她左邊許硯蹲著、一手第一格已經放在她背上，看著她、嘴閉著（稿子 c40 的長鏡在兩人的台詞之間拆開：s40、s40b）。秦霜在船頭放下手臂不拍（人少一點）"),
    dict(sid="s40b", loc="landing_w", cam="Close-up, slow push in", chars=["xuyan"], night="night",
         comp=f"close-up of {XU_C}, crouching on the jetty, framed from the chest up with space above his head, his face three-quarter to screen right, never the lens; grave and wary: brows drawn, lips pressed shut; warm torchlight on one side of his face; behind him only the drifting fog, soft",
         lines=[("xuyan", "鄭伯不肯說的那筆舊帳，總有一天，會自己找上門來。", "心裡話，錄得近、輕", "inner")],
         motion=f"Xu Yan slowly lifts his eyes toward the bow of the boat beyond the right edge of the frame, where the old steward stands; {SILENT_HE}; he is thinking, not speaking",
         zh="近景、慢推（送渡口霧色裁切）：許硯蹲著，慢慢抬眼往畫右外船頭的鄭伯看，眉頭壓低；全程嘴閉著（心裡話畫外）（結尾；懸念交給第 26 集，接點 25→26 是 s40 的兩人蹲在甘蔗堆旁）"),
]

HEAD = [
    "- 重製版 r2、真人版（站主 2026-11-11「之後都用真人版」）：照 `docs/videos/zhong-tian-qu-qi-e025-r2/script.md`（c01–c40 對應 s01–s40；c20、c23、c40 各拆成兩鏡 s20／s20b、s23／s23b、s40／s40b，共 43 鏡；含「這版改了什麼」「2026-11-06 審稿後的修改」與「真人版的改動（2026-11-17）」）；台詞一字不改，只改拍法；每鏡一個看得見的動作、一句一筆不拆半句、預設不笑。篇章設定 `production/r2-bible-e021-e030.md`（拍法 1–30 條）。第 3 篇章〈搶親〉第五集。",
    "- 內部工作編號 925（`hailuo/{ff,clips}-dh-e925.json`、`colab/runs/e925/extras.json`、`colab/runs/e925-live/spec.json`，工作資料夾 `~/mokaair-work/videos/zhong-tian-qu-qi-e925-dh/`）；發布 slug `zhong-tian-qu-qi-e025-r2`。不放集數、不放片名卡；s01 接第 24 集 s36 的同一天午後（聖經接點 24→25：糖坊 `set-tangfang-l1`，灶在左前、右邊沒牆；二牛從右邊進棚抖空麻袋；許硯捧著那碗白糖站在左牆矮凳邊）；s40 交給第 26 集（接點 25→26：渡口甘蔗堆，唐小棠蹲著捧字條哭，許硯蹲在她旁邊，火把）。",
    "- 照第 24 集審稿後的寫法與第 21–24 集挑片學到的一開始就照做：`OFFSCREEN_SPEECH = False`；`quiet()` 只管嘴；背影或畫外的人說話時，每張朝鏡頭的臉都寫不說話、嘴閉著、在聽，不寫會引人笑或開口的字；掛著的東西不點名（棧橋寫木板、漏斗寫倒放在木架上）；道具與接觸寫在第一格；紙一律空白、信與字條只見摺起的外面；寫人數。",
    "- **唐小棠不露嘴說話、本集也不露臉**（拍法 3）：她的台詞全部從背後拍（s05、s07、s10、s11、s14 糖坊；s19 渡口；s32、s36、s40 棧橋；nospeak，spec 拿掉她的圖與身分句；兩顆高丸子各一條粉緞帶、後頸露出、頭不動、正背對鏡頭）；s08、s17、s31 畫外；s13、s16、s38 只有背影、不點名不送圖；全景 s01、s09、s22、s31 不拍她；她獨自的背影鏡放在畫面正中（挑片：畫緣的背影常露側頰）。**算盤本集沒有**（拍法 20：稿子 c05 撥算珠交給音效）。",
    "- **場景圖說了算**（拍法 29，協調者 2026-11-17 決定，每張放大看過）：糖坊 `set-tangfang-l1`（s01）與第 24 集的免費裁切 `set-tangfang-jia-l1`（其餘第一場）：灶在左前、漏斗在左牆、石盆在中、右邊沒牆是欄杆與雪溪；許硯在左牆矮凳邊、二牛在中、唐小棠在右前的木板桌（桌子寫在鏡頭裡）。渡口夜霧 `set-dukou-ye-l1`（全景 s22、s31）與兩張新的免費裁切：棧橋 `set-dukou-ye-qiao-l1`、霧色 `set-dukou-ye-wu-l1`（近鏡與泥岸）。棧橋從畫左伸進水裡，船從畫右的霧裡來，魏記的人從右邊泥坡往畫左衝下來。**不需要試鏡**。",
    "- **船、棍、火把**（拍法 23、25）：三條船只在全景 s22、s31（遠、在霧裡），近一點的鏡只寫一個船頭；船頭一支火把（聖經的空白紙燈籠改火把：掛著的燈籠會長字）；木樁上三支火把插著、沒人拿。魏記夥計與打手一律「一根素面木棍」（原版必修：木棍變銅鑼）；秦霜一根比人高的素木長棍，柴刀不寫；少年十人只在全景 s31。",
    "- **鄭伯**第一次出場：送 `zhengbo-portrait-l1`（高瘦長臉、灰白山羊鬚與細鬍、灰髮小髻束黑布、深褐緞袍）；`cast.json` 的「微胖、慈眉笑、袖口小毛筆」由 `colab/runs/e925/extras.json` 換掉。只有 s37 可以客氣地笑（稿子）。",
]
FOOT = [
    "- **參考圖**（`assets/refs-live/`）：許硯（l1、angle-a；帶笑的 angle-b 整集不送；近景 s15、s20、s20b、s40b 送 angle-a 與 l1）、王二牛（l1、angle-a）、秦霜 l1、鄭伯 l1。唐小棠整集不送圖。魏記夥計、打手、少年、船工、手都不送圖。場景見上面。",
    "- 共用檔：`build-r2.py` 的 `EN` 加一筆 `\"zhengbo\": \"Steward Zheng\"`（他在鏡頭上說話：s33、s35、s37；名字跟 `gen-dh.mjs` 的一樣），e910–e924 重建逐位元相同（scratchpad `bytecheck925.sh`）；`gen-dh.mjs`、`pilot.py`、`cast.json` 不動；`refs-live` 加兩張免費裁切（新 id）與 README 一段。精修文字的 CG 立領句由本檔結尾的 `live_clips()` 在 build 後從 `clips-dh-e925.json` 拿掉（第 22–24 集的做法）。",
    "- `colab/runs/e925/extras.json`（照第 24 集，加鄭伯的樣子與二牛的 open 一字）與 `colab/runs/e925-live/spec.json`（`mkspec.py` 產生；種子 9251101／9251102）。",
    "- 免費準備：scratchpad `prep925.sh`（`DRY=1 … st1-ep.sh 925` → `pilot.py` → `retake.py` → `colab-jobs.json` 加 output_path、套 swap_pictures（絕對路徑）→ 逐鏡查送的場景圖與人物圖 → 精修用的分隔句 → `preflight-prompts.py` → 否定名詞、會長字的名詞與掛著的東西掃描）。",
    "- 配樂：糖坊沉的鋼琴，s05「姓唐」輕重音，s13 起加弦樂，s16「叮」；渡口風聲與低鼓，s21 船出現重音，s23 起打鬥鼓點，s31 收成開闊的弦樂；棧橋二胡，s35「舊帳」低重音，s39 字條輕重音、s40b 收。音效見 script.md〈音樂與音效〉（另外：s04 麻袋丟地、s05 算珠、s14 轉頭、s18 跑出去、s19 踮腳、s25 長棍轉動、s28 掃腳踝、s29 打手爬走與兩支火把、s32 跑步與跳板、s34 扶穩，都交給音效）。",
]

# Long shots: seconds to buy (filled in after the recordings; see BUY).
BUY = {}


# ---- the refine text (e022 review 必改 12, as e023, e024): hailuo/clips-dh-e925.json column 0 is the motion text
# refine-prep.py sends with a picked d1 draft. gen-dh.mjs opens every clip that lists tangxiaotang with the CG-era "Tang
# Xiaotang's high stand-up collar stays closed at her throat." and names her in "<names> shown in <Picture 1>"; in a back shot
# that draws the collar back and turns her face to the lens. Every shot of her here is a back shot: the sentence goes and her
# name becomes "the young woman seen only from behind". Column 1 is recomputed.
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
            assert "Tang Xiaotang" not in text, (key, "her name is left in a back shot's refine text")
        assert "stand-up collar" not in text, key
        row[0] = text
        row[1] = hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]
    open(path, "w", encoding="utf-8").write(json.dumps(clips, ensure_ascii=False, separators=(",", ":")))


if __name__ == "r2spec":
    import atexit
    import os
    atexit.register(live_clips, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "hailuo", f"clips-dh-e{EP}.json"))
