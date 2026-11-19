"""Episode 34 remake (r2): the writer spec for ../e001-r2/build-r2.py. Source: docs/videos/zhong-tian-qu-qi-e034-r2/script.md
(c01-c40; the CG-era r2 script), including its sections 「這版改了什麼」 and 「2026-11-06 審稿後的修改」, which override the tables.
Every line is the script's, word for word; only the staging changes. 40 shots, one per script shot (s01-s40 = c01-c40).
Bible: production/r2-bible-e031-e040.md (arc 4 〈旱年〉: rules 1-43, 〈場景〉, 〈接點〉 33->34 (rewritten after e033's independent
review to the picture set-shentan-l3: the wheel left of the middle, twelve flat paddles, no raised field ridge) and 34->35, the
props (the wheel row: no bamboo buckets, no trough; 「第 34 集釘葉板、翻葉板照這張圖的葉板寫」), people, 〈小角色〉 and 原版必修
tables) and r2-bible-e011-e060.md (accounts: no affection change this episode; Tang Xiaotang 42, Qin Shuang 41, A-ling 32; the
drought quest 「今日日落到期」 -> 「旱災任務完成，稻種保住」). The fourth episode of arc 4: the tenth day at the deep pool, noon
(the same moment as e033 s40), the early afternoon, sunset; then the three small fields at sunset and the swarm.

Written from the start the way e033-r2/r2.py stands AFTER its independent review (writer-tools/e033-r2/review-independent.md,
必改 1-8, 建議 1-15) and the general lessons of the two e033 reviews:
- The pictures agree with the words (e033 必改 1, 2): the wheel is set-shentan-l3's (twelve flat paddles, no buckets, no
  trough), so the script's c24 「竹斗舀水倒進木槽」 becomes the paddles at the top of the turning wheel lifting sheets of water
  (s24), and every hand on a paddle is in a frame whose paddle is really there (-bian at the right, -an at the right edge).
- Long things are never touching in the first frame (e032 fix2): Elder Han's staff and the sluice rope (s20-s22 "well apart"),
  the hammer and the nail (s13), the mallet (s19), the paddles; the hooks are side-on and static with the result written first
  (s23: the wheel jerks a quarter turn, pauses, then turns faster and faster).
- The place sentence where the picture puts it (e033 必改 7): the pool is on flat dry fields; the fields are flat with a low
  grassy ridge; no "gully", no raised field ridge.
- No collective noun (e033 必改 8): every wide writes its people one by one and "exactly N people"; no "crowd".
- A shot with nobody in it has no shoes sentence (e033 必改 6): mkspec drops it from s23 and s40.
- Background people are written with what their hands hold (a paddle, buns, nothing); never a weapon word (rule 5: Qin
  Shuang's chopper is NOT written, the script's 「柴刀插腰帶」 goes); no negated noun (rule 18).
- Mud (e032 fix3): nothing is written "mud", "caked" or "yellow mud"; the water reaching the fields is "a thin sheet of brown
  water" in the furrows and "a double handful of cloudy brown water" in Elder Han's hands, never smeared on a person; the
  script's 「白鬚上沾泥水」 (c28), 「許硯半跪在泥裡」 (c29), Carpenter Shi 「渾身濕」 (c25) and Qin Shuang 「褲腳濕到膝」 (c19, c31) are
  not written (rule 12 and the look's negative "wet clothes").
- OFFSCREEN_SPEECH = False (rule 15); rule 31: a line to someone out of frame is written "toward someone out of sight beyond the
  left/right edge of the frame", that side set only, the speaker the only person; GAZE_REFINE puts the same direction into the
  refine text. A look at a thing names the thing (the paddle, the wheel, the sun, the water, the far hills).
- No blue light (rule 11): the panels of s08, s33 are the editor's; the script's 「臉被面前的淡藍光照亮」 is not written.
- No word "open" (rule 36): the sluice gate "is pulled up".

THE AXES (rules 29, 42: the pictures decide):
- The deep pool (set-shentan-l3, the e033 picture: the camera at the near stone edge, the whole wheel in the pond against the far
  stone edge, left of the middle, its axle on a small trestle; the low frame at the left with the stone steps and a small
  wooden landing; the tall frame with its long top beam at the right; the big grey boulder on the stone edge at the right; flat
  dry furrowed fields to the horizon). As e033 s31-s38: the sluice at the LEFT, at the narrow gap of the stone edge by the steps
  (-an); the villagers on the stone edge at the left; the wheel to their right (-bian: the stone edge at the left, the near rim
  and paddles at the right); Qin Shuang on the boulder at the RIGHT, facing screen left (-shi, the new crop round the boulder;
  low angles against the sky -tian). 33->34: e033 s35 (Xu Yan's two flat hands on a paddle, -bian) and s40 (Qian Yuanwai laughing
  on the field edge far at the right) -> s01 keeps s35's place and both flat hands on the paddle, a medium shot so the pinwheel
  fits at the lower left corner (e034 independent review 建議 2; the bible's 〈接點〉 33->34 says both hands now).
- The new channel (s26, set-shentan-qu-xi-l1: a dry earthen channel dug across the furrowed fields past the tall frame's posts
  and the boulder, at sunset): the water runs away from the camera into the far fields.
- The fields (set-hantian-l1, round 1, 37038, cleaned and cropped for free: rows of dry cracked furrows with short stubble, a low
  grassy ridge across the middle, a big old tree at the RIGHT, a row of small houses and the far hills at the LEFT and middle,
  a low golden light): Elder Han kneels on the ridge (-geng), Qian Yuanwai stands on the grassy bank under the big tree at the
  right (-liu; the script's 「右上田埂」), the people of the village at the left. The script stages c35-c40 back at the pool;
  here they stay at the field edge where the channel water runs in (the script's 「渠邊」), because the swarm comes over the
  NORTHERN HILLS and only the field picture has hills (the pool's horizon is flat). North is screen RIGHT in the reverse
  close-ups (s37-s39, the script's 「畫面右上」); s40 is their point of view, the far hills of the picture.

PLACES (gen-dh SET takes the FIRST pattern in its list order that matches; "deep pool" opens every LOC, so gen-dh sends
dh-set-shentan-t1 = pilot.py's newest set-shentan, l3, and spec.json swaps it with absolute paths):
- Noon (s01-s11) and the early afternoon (s12-s21): set-shentan-l3 as it is (s12, s19) and its e033 crops -an-l3 (s04, s06,
  s07, s13, s14, s15, s20, s21), -bian-l3 (s01, s08, s09, s17), -lun-l3 (s05), -tian-l3 (s02, s11, s16; the insert s03 as the
  colour of the sky only) and the new free wider crop -shi2-l3 (s10, s18; shentan_xi.sh; -shi-l3 was too tight, review 必改 2).
- Sunset at the pool (s22-s25): the free warm grade set-shentan-xi-l3 (s23) and its crops -xi-an-l3 (s22), -xi-ye-l3 (s24: the
  top of the wheel), -xi-lun-l3 (s25); the channel in a lighter grade set-shentan-qu-xi2-l1 (s26) (shentan_xi.sh; review 建議 9).
- The fields at sunset (s27-s36): set-hantian-geng-l1 (s27, s29, s34, s35), -tian-l1 (s28, s33), -liu-l1 (s30, s31, s32),
  -di-l1 (s36); the swarm darkens it (s37-s40): the free grey grade set-hantian-hui-l1 (s40) and its crops -hui-tian-l1 (s37,
  s38), -hui-geng-l1 (s39) (hantian_crops.sh; three tiny dark poles on the far field line painted out first by hantian_clean.py,
  which replaced the delogo boxes after the independent review, 建議 7).
  The field and channel LOCs carry "below the deep pool" / "At the deep pool ..., beside" only for gen-dh's SET; mkspec.py
  takes those words out of the d1 prompts (the pictures show no pool there).
Shared files: none changed (build-r2.py's EN has every speaking name; gen-dh.mjs, pilot.py, cast.json untouched). The d1 prep
(colab/runs/e934/extras.json, colab/runs/e934-live/{mkspec.py,spec.json}, the scratchpad's prep934.sh, rec934.sh and
e934d1.sh) was written 2026-11-19 (colab/runs/e934-live/PREP.md). e033 is not finished: s01 follows e033's r2.py (s35, s40)
and must be checked again against the cut e933-live.mp4 once e033 is made.
"""
EP = 934  # internal working number; the published slug is zhong-tian-qu-qi-e034-r2
SLUG = "zhong-tian-qu-qi-e034-r2"
EP_TITLE = "水上來了（重製版 r2）"
OUTLINE_SECONDS = 215  # script.md: about 215 s, 40 shots (11 + 10 + 19)
TARGET_MINUTES = [3, 4]
TITLE = "葉板裝反了！水車轉起來，北邊壓來一片黑雲｜種田娶妻打天下 第34集（重製版）"
DESCRIPTION = "水車轉了半圈就停住，小禾的紙風車在風裡倒著轉——許硯想通了：十二片葉板，角度跟水流反了。系統：今日日落到期。秦霜站上大石：一班下水卸板，二班扛板，三班上架釘！阿令提著一籃饅頭來，冷冷一句「妳數慢了，第八片已經上架了」。一個時辰，十二片全翻完。日落前，韓伯親手拉起閘門，水車顛一下、越轉越快，水頭衝進乾裂的田；韓伯跪在田邊捧起泥水，錢員外的壩白守了十天。旱災任務完成，稻種保住——笑聲裡，北邊的天一下子黑了。那不是雲，是蝗蟲。《種田娶妻打天下》第 34 集（重製版）。"
THUMB = ("水上來了！", "s27")
CHARACTERS = ["xuyan", "xiaohe", "hanbo", "shimujiang", "qinshuang", "aling", "qianyuanwai", "xitong"]
MUSIC = "one cue per scene: only a hot dry wind and the whir of a paper pinwheel by a still wooden waterwheel at noon, one bright note on a sudden idea and quickening strings; then a lively work tune of drums and plucked strings by a green pond in the white afternoon sun, one strong beat as the last paddle goes on; then breathless strings at sunset, the full orchestra rising as a great waterwheel turns faster and faster and water runs into cracked fields, a pause under a sour landlord, warm strings, then everything swallowed by a low rising hum and a deep bass as a dark band darkens the sky; ancient Chinese rural drama, no vocals"

# Places.
E1 = "At the deep pool on the flat dry fields of Liuxi at noon on the tenth day of the drought"
NOON = "harsh white noon sun high overhead in a pale clear sky, short hard shadows, a hot dry wind"
A1 = "At the deep pool on the flat dry fields of Liuxi in the early afternoon of the tenth day of the drought"
AFT = "bright white afternoon sun high in a pale clear sky, shadows still short"
X1 = "At the deep pool on the flat dry fields of Liuxi at sunset on the tenth day of the drought"
SUNSET = "low warm golden sunset light"  # self-review 必改 1: the free -xi grade keeps the noon picture's short shadows, so no shadow length is written
XQ_GEN = f"{X1}, beside"  # mkspec.py: -> XQ_LIVE in d1 (the channel picture has no pool)
XQ_LIVE = "On the flat dry fields of Liuxi at sunset on the tenth day of the drought, beside"
POOLMARK = " below the deep pool"  # mkspec.py takes it out of the field shots in d1 (gen-dh's SET needs "deep pool")
F1 = f"On the three small dry fields of Liuxi{POOLMARK} at sunset on the tenth day of the drought"
G1 = f"On the three small dry fields of Liuxi{POOLMARK} as the sunset dies on the tenth day of the drought"
GREY = "the golden sunset light dimming fast to a cold dull grey, the sky darkening"
POOL = ("a round pond of still deep green water edged with rough fieldstones in the foreground, two tall wooden frames standing "
        "at its far edge, stone steps and a small wooden landing at the left, a big grey boulder on the stone edge at the right, "
        "a flat sandy bank beyond, dry furrowed fields to the horizon")
WHEEL = "the big wooden water wheel exactly as in the picture, standing in the pond against the far stone edge, its twelve flat wooden paddles round its rim"
FIELD = ("rows of dry cracked furrows with short dry stubble, a thin sheet of brown water spreading along the furrows, a low grassy "
         "ridge across the field, a big old tree at the right, a row of small houses and far hills at the left")
LOC = {
    "nn": f"{E1}: the pool exactly as in the picture: {POOL}, and {WHEEL}; {NOON}",
    "nn_c": f"{E1}, on the stone edge of the pond beside {WHEEL}; {NOON}",
    "nn_s": f"{E1}, by the big grey boulder on the stone edge at the right of the pond, beside {WHEEL}; {NOON}",
    "nn_e": f"{E1}; {NOON}",
    "af": f"{A1}: the pool exactly as in the picture: {POOL}, and {WHEEL}; {AFT}",
    "af_c": f"{A1}, on the stone edge of the pond beside {WHEEL}; {AFT}",
    "af_s": f"{A1}, by the big grey boulder on the stone edge at the right of the pond, beside {WHEEL}; {AFT}",
    "af_e": f"{A1}; {AFT}",
    "xi": f"{X1}: the pool exactly as in the picture: {POOL}, and {WHEEL}; {SUNSET}",
    "xi_c": f"{X1}, on the stone edge of the pond beside {WHEEL}; {SUNSET}",
    "xi_e": f"{X1}; {SUNSET}",  # e034 independent review 建議 1: s24 (only the wheel and the sky) has no place sentence, as nn_e / af_e
    "xq": f"{XQ_GEN} a new dry earthen channel dug across the cracked furrowed fields past two tall wooden posts and a big grey boulder; {SUNSET}",
    "fd": f"{F1}: the fields exactly as in the picture: {FIELD}; {SUNSET}",
    "fd_c": f"{F1}, on the low grassy ridge at the edge of the dry cracked furrows; {SUNSET}",
    "fd_t": f"{F1}, on the grassy bank under the big old tree at the edge of the field; {SUNSET}",
    "gy": f"{G1}: the fields exactly as in the picture: {FIELD}; {GREY}",
    "gy_c": f"{G1}, on the low grassy ridge at the edge of the dry cracked furrows; {GREY}",
}
LIGHT = {
    "noon": "the harsh white noon light stays unchanged",
    "aft": "the bright white afternoon light stays unchanged",
    "sunset": "the low golden sunset light stays unchanged",
    "grey": "the light keeps dimming to a cold grey",
}
# bible rule 15: no "<X> speaks off screen" / "the system voice speaks off screen".
OFFSCREEN_SPEECH = False

# Repeated wording (each prop is one object, written the same way every time).
XU_WORN = ("Xu Yan, in his faded blue-grey scholar's robe patched at one elbow, its sleeves rolled up to the elbows, dark shadows "
           "under his eyes and a short dark stubble on his jaw after seven short nights")  # bible 〈人物〉: e033-e034
HAN = ("Elder Han, in his faded grey cotton cross-collared long robe, his long white beard down to his chest, his white hair in a "
       "small topknot, his polished old bamboo walking staff in one hand")
HAN_NOSTAFF = ("Elder Han, in his faded grey cotton cross-collared long robe, his long white beard down to his chest, his white "
               "hair in a small topknot")
CARP = ("Carpenter Shi, in his faded light tan cross-collared short work jacket with the sleeves rolled up and his worn brown "
        "leather apron, one plain wooden stick through his grey topknot")  # e032/e033 (the portrait; light tan, rule 12)
CARP_WORN = f"{CARP}, his eyes red-rimmed and tired, his grey stubble grown rough"  # bible: seven nights without sleep
QIN = ("Qin Shuang, in her fitted dark brown cross-collared short jacket cinched with a wide plain black leather belt, black "
       "trousers and leather boots, her high ponytail tied with black cord")  # e030's wording; no chopper (rule 5)
XIAOHE = ("little Xiaohe, an eight-year-old girl in her patched lilac cotton jacket, her two little pigtails tied with red string, "
          "one front tooth missing, a small woven straw rabbit tucked into the cloth sash at her waist")
PINWHEEL = "a little pinwheel of four plain white paper vanes on a thin bamboo stick"  # bible 〈道具〉
ALING = ("A-ling, in her plain grey-white cotton dress tailored close at the waist with a cloth sash, its long sleeves covering "
         "both wrists, her long black hair pinned up with one plain wooden hairpin")  # bible 〈人物〉: no veil (no outsiders), no shackles
BASKET = "one round bamboo basket with a dozen plain white steamed buns heaped in it"  # bible 〈道具〉: one basket
QIAN = ("Qian Yuanwai, short and portly with a round face and a thin eight-shaped moustache, in his dark gold silk robe woven "
        "with small round medallions, the front of the robe plain brocade, three gold rings on his fingers")
MALLET = "one wooden mallet with a plain wooden handle"
HAMMER = "one iron hammer with a plain wooden handle"  # bible 〈道具〉: one, Xu Yan's (e034 c13)
NAIL = "one long dark iron nail"
PADDLE = "one loose flat wooden paddle"
SLUICE = "a small wooden sluice gate of three plain wet planks set upright in the narrow gap of the stone edge, one thick rope tied to its top"
SWARM = ("a low dark brown band made of countless tiny dark specks, already pressing over the far hills from the first frame, "
         "its leading edge breaking up into scattered specks")  # bible 〈道具〉 蝗群; 原版必修 e034
HANDS = "their hands hold only what is described here"
SILENT_HE = "He says nothing in this shot: his lips stay pressed together from the first frame to the last, his jaw still, no talking, no mouthing words"
NOBODY = "Throughout the shot the set layout stays as it is. The pictures fix the place and the objects only, never the mood. "
# rule 34 (bible 〈小角色〉: three gangs, each with its own head-wrap colour: grey, faded indigo, earth-yellow; e033's men)
GANG1 = ("four men in Song-dynasty cross-collared homespun short jackets and grey cloth head wraps, each a different colour and "
         "age: a lean young man in a rust-red jacket, a stocky middle-aged man in a dull olive-green jacket, an older man with a "
         "short grey beard in a faded undyed hemp-beige jacket and a young man in a faded maroon jacket")
GANG2 = ("two men in Song-dynasty cross-collared homespun short jackets, faded indigo cloth head wraps and cloth shoes, a broad "
         "young man in a dark charcoal jacket and a thin man of about thirty in a faded green jacket")
GANG3 = ("two men in Song-dynasty cross-collared homespun short jackets and earth-yellow cloth head wraps, a tall young man in a "
         "dark teal jacket and a wiry middle-aged man in a deep wine-red jacket")
TWO_UP = ("two men in Song-dynasty cross-collared homespun short jackets and grey cloth head wraps, just up out of the water, their "
          "trousers rolled to the knees, a lean young man in a rust-red jacket and a stocky middle-aged man in a dull olive-green jacket")
TWO_FIELD = ("two women standing side-on in Song-dynasty cross-collared homespun jackets and cloth shoes, a bent old woman in a "
             "faded deep plum jacket with a white head cloth and a middle-aged woman in a dark grey jacket with a faded indigo "
             "head cloth, their hands empty")
RUNNERS = ("four people in Song-dynasty cross-collared homespun jackets and cloth shoes, each a different colour and age: a boy of "
           "about ten in a mustard-yellow jacket, a young woman in a rust-red jacket, a broad middle-aged man in a dull olive-green "
           "jacket and a lean middle-aged man in a dark charcoal jacket, their hands empty")
RETAINERS = ("two men in identical Song-dynasty black cross-collared short jackets, black cloth head wraps and cloth shoes, their "
             "hands empty at their sides")
BACKS = ("three people in Song-dynasty homespun jackets: an old man with a short grey beard in a faded undyed hemp-beige jacket "
         "and head wrap, a young woman in a rust-red jacket and a boy of about ten in a mustard-yellow jacket")
# rule 2: over-the-shoulder backs, unnamed, no picture
BACK_XU = ("at the left edge of the frame, cut by it, soft and out of focus, only the back of one shoulder in a faded blue-grey "
           "robe and the back of a man's topknot, toward us the whole shot")
BACK_CARP = ("at the upper right edge of the frame, cut by it, soft and out of focus, only the back of one shoulder in a faded "
             "light tan work jacket with the strap of a leather apron across it and the back of a grey topknot with one plain "
             "wooden stick through it, toward us the whole shot")
HAND_EDGE = ("at the lower left corner of the frame, cut by it, soft and out of focus, only a small hand in a patched lilac cotton "
             "sleeve holding up " + PINWHEEL + ", its four white vanes turning in the wind")
# set-only sides (the picture of each place, all the way to the edge)
SIDE_SKY = "the pale clear sky"
SIDE_RIM = "the rough fieldstone edge of the pond, the green water and the near rim and paddles of the wheel"
SIDE_STONE = "the stone edge of the pond and the lower paddles of the wheel"
SIDE_TREE = "the grassy bank and the trunk of the big old tree"
SIDE_HILLS = "the sky over the far hills and a few drooping branches of the big old tree"  # self-review 必改 2: -tian-l1's right edge


def quiet(who, pr="his", plural=False):
    verb = "say" if plural else "says"
    return f"{who} {verb} nothing in this shot: {pr} lips stay pressed together from the first frame to the last, no talking, no mouthing words"


def off(side, what, he="he"):
    """A line to someone outside the frame: the gaze, that side set only, and the only person (rule 31)."""
    edge = f"the {side} edge of the frame"
    return (f"toward someone out of sight beyond {edge}, never the lens; that side of the frame is only {what} all the way to the "
            f"edge, and {he} is the only person in the frame")


SHOTS = [
    # ---- scene 1: noon of the tenth day, the deep pool (33->34: the same moment as e033 s35 / s40), the wheel stopped.
    dict(chapter="深潭邊，水車停住（第十日正午）", loc="nn_c", cam="Medium shot, slow push in", chars=["xuyan"], night="noon",
         comp=f"medium shot on the stone edge of the pond, like the picture: in the left half of the frame {XU_WORN}, framed from the waist up, both flat hands already resting on one wet wooden paddle on the rim of the still wheel at the right of the frame from the first frame, as in the shot before, his face three-quarter to screen right toward the paddle under his hands, his eyes on it, never the lens; drained and stunned, not smiling: brows drawn, lips pressed shut; beside him at the right, the near rim, spokes and paddles of the still wheel; {HAND_EDGE}; he is the only person in the frame, with the small hand at its corner; {HANDS}",
         motion=f"a gust of hot wind from the left sets the pinwheel spinning fast, and Xu Yan's fingers slowly curl against the paddle; {quiet('Xu Yan')}",
         zh="中景、慢推（送 `set-shentan-bian-l3`：左邊石邊、右邊輪緣與葉板；**接點 33→34：照第 33 集 r2.py 的 s35 與 s40 寫**（s35 許硯在左半、兩手按右緣的葉板、送 `-bian-l3`；s40 錢員外在田邊笑），**第 33 集成片後要照實拍重核**）：同一刻、同一個框，許硯在左半，**兩手平掌**第一格已經按在一片停住的葉板上、盯著它（第 33 集 s35 是兩手平掌、近景，本鏡照兩手、景別放到中景讓左下的小手入鏡；獨立審稿建議 2，聖經〈接點〉33→34 同步改成兩手）；畫面左下角虛焦的一隻淡紫補丁袖口的小手舉著紙風車（不點名、不送圖，拍法 2；稿子『秦霜的手按在她肩上』不寫：只要一隻手），一陣熱風從左吹來，風車呼呼轉，許硯的手指在葉板上慢慢蜷起（平掌「收緊」自相矛盾，改手指蜷起）；不重播錢員外的笑（稿子〈合併注意〉）。『倒著轉』模型讀不出方向，交給 s03 的台詞與剪接。沒有人說話"),
    dict(loc="nn_e", cam="Low-angle close-up, slow push in", chars=["xiaohe"], night="noon",
         comp=f"low-angle close-up of {XIAOHE}, seen from below, framed from the chest up with space above her head, {PINWHEEL} already held up before her chest in her right hand from the first frame, its vanes spinning in the wind, her face three-quarter to screen right {off('right', SIDE_SKY + ' and the long top beam of the tall wooden frame', he='she')}; pouting, not smiling: cheeks puffed out, brows drawn together, lips moving between words; behind her, soft, the pale clear sky and the top paddles of the still wheel at the left; {HANDS}",
         lines=[("xiaohe", "哥，你看，我的風車也轉反了。", "鼓起臉")],
         motion="Little Xiaohe holds the spinning pinwheel out toward the right edge of the frame as she speaks",
         zh="低角度近景、慢推（送 `set-shentan-tian-l3`：淡藍天、高木架頂的長橫梁、畫左是輪子頂上的葉板，稿子『身後只有天空與水車的一角』）：小禾鼓著臉、右手紙風車第一格已經舉在胸前、在風裡轉，往畫右外看不到的人（許硯，不點名）遞過去說。稿子『往風車吹一口、轉頭看哥哥』只留一個動作（遞），轉頭在第一格完成（拍法 32）"),
    dict(loc="nn_e", cam="Insert close-up, slow push in", chars=[], night="noon",
         comp=f"insert close-up, the very first frame is already a close view of {PINWHEEL}, held upright by its stick in a small hand with a patched lilac cotton cuff, its four white vanes spinning fast in the wind, every vane tilted the same way; beyond it, soft and out of focus, only the pale clear sky fills the background to every edge; only the pinwheel, the small hand and the cuff are in the frame",
         lines=[("xuyan", "轉反了……風從這邊來，葉子卻斜向那邊。", "畫外，愣住")],
         motion=NOBODY + "the gust keeps blowing from the left and the pinwheel spins faster and faster",
         zh="插鏡、慢推（第一格就是紙風車特寫，拍法 10、35；d1 不寫地點句，背景只有淡藍天；H3 參考模式至少一張圖，送 `-tian-l3` 寫成『只給天的顏色』，同第 33 集 s27）：竹籤、四片白紙葉，淡紫補丁袖口的小手拿著，風從左吹、越轉越快；紙葉斜的方向寫『每片斜同一邊』（方向本身模型讀不出，交給台詞）。許硯的話是畫外錄音，嘴不入鏡"),
    dict(loc="nn_c", cam="Medium shot, slow push in", chars=["xuyan"], night="noon",
         comp=f"medium shot on the stone edge of the pond by the stone steps, framed from the waist up: in the middle {XU_WORN}, already turned to face the still wheel at the right from the first frame, his face three-quarter to screen right toward one wet wooden paddle on its rim at the right edge of the frame, his eyes on it, never the lens; that side of the frame is only {SIDE_RIM} all the way to the edge, and he is the only person in the frame; struck by a sudden thought, not smiling: eyes wide and bright, brows lifted, lips moving fast between words; behind him, soft, the stone steps, the small wooden landing and the low wooden frame in the hard noon sun; {HANDS}",
         lines=[("xuyan", "是葉板的角度，跟這段水流反了！", "想通了")],
         motion="Xu Yan slaps his flat right hand down hard on the paddle as he speaks",
         zh="中景、慢推（送 `set-shentan-an-l3`：左邊石階、小木台、矮木架，右緣是輪緣與葉板）：許硯第一格已經轉身面向畫右的水車（稿子『猛地轉身』在第一格完成），右手平掌往葉板上一拍、眼睛發亮（**不笑**）、想通了地說（配樂一個亮的重音）"),
    dict(loc="nn_c", cam="Medium shot over the shoulder, slow push in", chars=["shimujiang"], night="noon",
         comp=f"medium shot over a shoulder, looking up: {BACK_XU}; beyond it, up on the wheel's wooden trestle in the water in the middle of the frame, {CARP_WORN}, crouching, framed from the waist up, already leaning down toward the man in the foreground from the first frame, his left hand gripping one spoke of the still wheel, his face three-quarter to screen left toward him, never the lens; frowning hard, not smiling: brows knotted, eyes narrowed, lips moving roughly between words; behind him, soft, the still spokes and paddles of the wheel and the pale sky; {HANDS}; exactly two people, the one in the foreground seen only from behind",
         lines=[("shimujiang", "反了？那就是十二片全拆下來，翻個面再釘？", "粗啞")],
         motion="Carpenter Shi leans further down from the edge of the trestle as he speaks",
         zh="過肩中景（仰）、慢推（送 `set-shentan-lun-l3`：輪子下半、輪架與葉板）：前景左是虛焦的藍灰肩背與髮髻（不點名、不送圖，拍法 2）；石木匠蹲在潭裡的輪架上，左手抓著一根輪輻，第一格已經探下身子，再往下探一點、皺緊眉頭粗啞地問"),
    dict(loc="nn_c", cam="Medium shot over the shoulder, slow push in", chars=["xuyan"], night="noon",
         comp=f"reverse medium shot over a shoulder, looking down: {BACK_CARP}; beyond it, below in the left half of the frame, {XU_WORN}, standing on the stone edge of the pond, framed from the waist up, his face tipped up three-quarter to screen right toward the man in the foreground, never the lens; sure and firm, not smiling: brows level, eyes steady, lips moving evenly between words; behind him, soft, the stone steps and the small wooden landing in the hard noon sun; {HANDS}; exactly two people, the one in the foreground seen only from behind",
         lines=[("xuyan", "對，翻過來它就轉。一片都不能漏。", "篤定")],
         motion="Xu Yan tilts his flat right hand to show the slant of a paddle and turns it over, palm up, as he speaks",
         zh="反打過肩中景（俯）、慢推（送 `-an-l3`：反打的背景換成石階那一側）：前景右上是虛焦的淺褐肩背、皮圍裙帶與插木棍的灰髮髻（不點名）；許硯在左下仰頭，平掌斜著比葉板的角度、再翻掌（一個手勢，平掌、手指併攏，拍法 32），篤定地說"),
    dict(loc="nn_c", cam="Medium shot, slow push in", chars=["hanbo"], night="noon",
         comp=f"medium shot on the stone edge of the pond by the stone steps, framed from the waist up: {HAN}, the staff in his right hand, already arrived from the left from the first frame, his face lifted three-quarter to screen right toward the high sun beyond the upper right edge of the frame, eyes narrowed against the glare, never the lens; that side of the frame is only {SIDE_RIM} all the way to the edge, and he is the only person in the frame; worried, not smiling: brows knotted, lips moving slowly between words; behind him, soft, the stone steps, the small wooden landing and the low wooden frame in the hard noon sun; {HANDS}",
         lines=[("hanbo", "十二片葉板，日落前翻得完嗎？", "擔心")],
         motion="Elder Han raises his flat free left hand to shade his eyes against the sun as he speaks",
         zh="中景、慢推（送 `-an-l3`）：韓伯拄著竹杖，第一格已經從左邊走到石邊（稿子『從左邊走過來』在第一格完成），抬頭朝畫右上看日頭、左手平掌遮在眉上（稿子『看日頭、再看水車』只留看日頭），擔心地問（答在 s10）；**不笑**"),
    dict(loc="nn_c", cam="Close-up, slow push in", chars=["xuyan"], night="noon",
         comp=f"close-up of {XU_WORN}, standing on the stone edge in the left half of the frame, framed from the chest up with space above his head, his eyes already lifted toward the high sun beyond the upper left edge of the frame from the first frame, squinting, never the lens; he is the only person in the frame; tired and dry, not smiling: brows drawn, lips pressed shut; beside him at the right, the near rim, spokes and paddles of the still wheel; {HANDS}",
         lines=[("xitong", "叮。旱災任務，今日日落到期。", "冷，宣布"), ("xuyan", "不用你說，太陽我自己看得見。", "心裡話，錄得近、輕", "inner")],
         panel=[("旱災任務，今日日落到期", "task")],
         motion=f"Xu Yan lowers his eyes from the sun to the empty air before him and the corners of his mouth press down; {SILENT_HE}",
         zh="近景、慢推（送 `set-shentan-bian-l3`：稿子『身後只有水車的葉板』）：許硯第一格已經抬眼瞇著看日頭，眼睛落回面前的空氣、嘴角一壓；系統與心裡話都是錄音、**全程嘴閉著**（拍法 15）；面板剪接時疊，**不寫淡藍光**（拍法 11）。長鏡"),
    dict(loc="nn_c", cam="Close-up, slow push in", chars=["xuyan"], night="noon",
         comp=f"close-up of {XU_WORN}, standing on the stone edge in the left half of the frame, framed from the chest up with space above his head, his eyes already lowered from the first frame, never the lens; he is the only person in the frame; resigned, not smiling: brows level, lips pressed shut; beside him at the right, the near rim, spokes and paddles of the still wheel; {HANDS}",
         lines=[("xitong", "看得見太陽，看不見葉板裝反了。", "冷"), ("xuyan", "行，這一句算你罵得對，我認。", "心裡話，錄得近、輕", "inner")],
         motion=f"Xu Yan lets out one long breath and turns his face toward the big grey boulder beyond the right edge of the frame; {SILENT_HE}",
         zh="近景、慢推（送 `-bian-l3`，同 s08）：本集的鬥嘴；許硯眼睛垂著，吐一口氣、轉頭朝畫右外的大石（秦霜那邊，不寫人；稿子『閉一下眼』不寫：閉眼再睜會寫到 open）；系統與心裡話都是錄音、**全程嘴閉著**。長鏡"),
    dict(loc="nn_s", cam="Medium shot, slow push in", chars=["xuyan", "qinshuang"], night="noon",
         comp=f"medium shot on the stone edge of the pond by the big grey boulder, like the picture: on top of the boulder at the right {QIN}, framed from the knees up, already standing there from the first frame, both hands on her belt, her face three-quarter to screen left, looking down toward the man below her, her lips pressed shut, never the lens; sharp, not smiling; at the foot of the boulder, on the flat sandy bank just behind the stone edge in the middle of the frame, {XU_WORN}, framed from the waist up, already arrived from the first frame, his face tipped up three-quarter to screen right toward her, never the lens; urgent, not smiling: brows drawn, lips moving fast between words; beside them, soft, the lower paddles of the still wheel at the left edge and the posts of the tall frame; {HANDS}; exactly two people",
         lines=[("xuyan", "秦霜，三班一起上，一個時辰翻完！", "急，交代")],
         motion=f"Xu Yan swings his flat right hand up toward her as he speaks; {quiet('Qin Shuang', 'her')}",
         zh="中景（雙人）、慢推（送本集免費做的較寬裁切 `set-shentan-shi2-l3`：畫左是輪子右下的葉板與輪架，中間是石邊上方的沙岸與高木架兩根柱，右邊大石約佔全高四成、石頂上方留得出人；獨立審稿必改 2：原本的 `-shi-l3` 放大太多、石頂上放不下膝以上的秦霜、畫左是水）：許硯第一格已經快步走到大石下、站在石邊後的沙岸上（不在水裡）（稿子的跟拍改慢推，走路在第一格完成），抬手平掌朝石上的秦霜一揮、急急地交代（答 s07）；秦霜站在大石上、兩手按著腰帶（**不寫柴刀**，拍法 5）、嘴閉著"),
    dict(loc="nn_e", cam="Low-angle medium shot, slow push in", chars=["qinshuang"], night="noon",
         comp=f"low-angle medium shot of {QIN}, seen from below, framed from the waist up, already up on the very top of the big grey boulder from the first frame, her face three-quarter to screen left, looking down toward someone out of sight beyond the lower left edge of the frame, never the lens; that side of the frame is only the pale clear sky and the top paddles of the still wheel all the way to the edge, and she is the only person in the frame; bold and commanding, not smiling: brows level, eyes bright, lips moving fast and clear between words; behind her, soft, only the pale clear sky and the long top beam of the tall wooden frame; {HANDS}",
         lines=[("qinshuang", "一班下水卸板，二班扛板，三班上架釘！", "颯爽")],
         motion="Qin Shuang sweeps both flat hands out sharply, one to the left and one to the right, as she speaks",
         zh="低角度中景、慢推（送 `-tian-l3`）：秦霜第一格已經站上大石頂（稿子『一步站上』在第一格完成），兩手平掌往左右一劈，朝畫左下外看不到的人（壯丁，不點名、不寫人）颯爽地下令（第一場結尾）。稿子『背景左遠：石木匠把閘板落下、水停』不拍（一鏡一個動作、遠處小人會長錯），交給音效（閘板落下、水停）"),
    # ---- scene 2: the early afternoon, the same pool, the paddles turned over (the same picture; white light).
    dict(chapter="深潭邊，翻葉板（午後）", loc="af", cam="Wide shot, slow push in", chars=["qinshuang"], night="aft",
         comp=f"wide shot at standing eye height, like the picture, the whole wheel in the frame: standing waist-deep in the green water at the foot of the wheel, small, {GANG1}, all four with both hands on {PADDLE} at the bottom of the rim, already prying it free from the first frame; on the stone edge at the left by the stone steps, small, {GANG2}, their hands reaching toward the water; three new plain wooden planks lying in a low stack on the stone edge in the left foreground; on top of the big grey boulder at the right {QIN}, framed full figure, her flat right hand raised toward the men in the water, her face three-quarter to screen left toward them, never the lens; loud and quick, not smiling: lips moving fast between shouted words; the six men's lips closed, never the lens; {HANDS}; exactly seven people",
         lines=[("qinshuang", "第一片下來了！二班接住，別讓它沉下去！", "喊")],
         motion=f"the four men in the water heave the loose paddle up onto the stone edge and the two men there catch it; {quiet('The six men', 'their', plural=True)}",
         zh="全景、慢推（人眼高、照圖；送整張 `set-shentan-l3`：水車每鏡同一款，原版必修）：**午後**（時間跳在 s11→s12 這一刀，光照圖：白光、影子還短，稿子 2026-11-06 審稿後的修改）。一班四個壯丁（灰頭巾：鐵鏽紅、暗橄欖綠、短灰鬚的本色麻老漢、褪色栗紅）站在輪腳齊腰深的潭水裡、第一格已經撬著一片葉板，一起把它推上石邊，二班兩人（褪色靛藍頭巾：炭灰、褪色綠）在左邊石階旁接住；左前景石邊上疊著三片新木板（獨立審稿建議 3：台詞是「第一片下來了」，前景不能已經堆著拆下的葉板；稿子『前景岸上堆著的葉板』改成新料）；穿鞋句只寫看得到腳的人（秦霜皮靴、石邊兩人布鞋，水裡四人不寫，mkspec）；秦霜在右邊大石上、右手平掌朝水裡的人一舉、喊。稿子『一班六個』照拍法 34 寫看得見的四個（人數讀得清）；推軌改慢推"),
    dict(loc="af_c", cam="Medium shot, slow push in", chars=["shimujiang", "xuyan"], night="aft",
         comp=f"medium shot on the flat sandy bank by the stone steps, both framed from the waist up, standing behind a rough plank trestle-table with one flat wooden paddle lying across it: on the left {CARP_WORN}, both flat hands already pressing the paddle down on the table from the first frame, his face three-quarter to screen right toward Xu Yan, never the lens; gruff and hoarse, not smiling: brows knotted, lips moving roughly between words; on the right {XU_WORN}, {HAMMER} raised in his right hand from the first frame, {NAIL} held upright on the paddle in his left fingers, well apart from the hammer's handle, his face bent toward the nail, his lips pressed shut, never the lens; intent, not smiling; behind them, soft, the stone steps, the small wooden landing and the still wheel in the white afternoon sun; {HANDS}; exactly two people",
         lines=[("shimujiang", "斜三分，翻過來，釘在這裡。下一片！", "粗啞")],
         motion=f"Xu Yan brings the hammer down once on the nail as Carpenter Shi speaks; {quiet('Xu Yan')}",
         zh="中景（雙人）、慢推（送 `-an-l3`）：石邊沙岸上一張粗木板架桌當工作台、一片翻過面的葉板橫在上面：石木匠在左、兩手平掌第一格已經按住葉板，粗啞地說；許硯在右、右手鐵錘舉著、左手指捏一根長鐵釘立在板上，掄錘敲一下、嘴閉著（鐵錘只在許硯手上，2026-11-06 審稿後的修改）。稿子『石木匠用墨線筆畫一道斜線』不拍（板上畫線會長出記號字；拍法 7、38），斜三分交給台詞"),
    dict(loc="af_c", cam="Wide shot, slow push in", chars=["aling", "xiaohe"], night="aft",
         comp=f"wide shot on the flat sandy bank at the left by the stone steps, both framed full figure: at the left {ALING}, {BASKET} on her left forearm, already arrived from the first frame, her face three-quarter to screen right toward the girl, her lips pressed shut, never the lens; cool and quiet, not smiling; beside her at the right {XIAOHE}, already holding the edge of A-ling's sleeve in her left hand from the first frame, {PINWHEEL} in her right hand, her face turned three-quarter to screen right toward the wheel at the right of the frame, never the lens; happy and loud: a wide gap-toothed smile, lips moving eagerly between words; behind them, soft, the stone steps, the small wooden landing and the low wooden frame in the white afternoon sun; {HANDS}; exactly two people",
         lines=[("xiaohe", "阿令嫂嫂來了！籃子裡是小棠嫂嫂蒸的饅頭！", "雀躍")],
         motion=f"Little Xiaohe tugs at the sleeve and calls out toward the wheel; {quiet('A-ling', 'her')}",
         zh="全景、慢推（送 `-an-l3`）：阿令左臂挎一個竹籃（十來個白饅頭），第一格已經從左邊小路走到沙岸上（稿子的跟拍改慢推）；灰白布裙、長袖蓋住手腕、木簪，**不戴面巾、沒有鐵鐐**（送 `aling-portrait-l1`，就是稿子要的沒戴鐵鐐那張，不用再畫）；小禾第一格已經跑到她身邊、左手拉著她的袖子，朝畫右的水車那邊喊（**本鏡可以笑**、缺門牙；`-an-l3` 右三分之一就是輪子，寫「畫右的水車」不寫「畫右外」，獨立審稿建議 11）。稿子『前景是岸邊的蘆葦』不寫（圖上沒有）"),
    dict(loc="af_c", cam="Medium shot, slow push in", chars=["aling", "xiaohe"], night="aft",
         comp=f"medium shot on the stone edge of the pond by the stone steps, framed from the waist up: in the middle {ALING}, {BASKET} already set down on a flat stone of the edge beside her from the first frame, two plain white steamed buns in her right hand held out toward the man at the right, her face three-quarter to screen right toward him, never the lens; cool and even, not smiling: brows level, lips moving calmly between words; at the right {TWO_UP}, the nearer one reaching out a flat hand for the buns, their lips closed, never the lens; at the left beside her {XIAOHE}, two plain white steamed buns held against her chest in both hands, {PINWHEEL} tucked into her sash, her lips pressed shut, never the lens; {HANDS}; exactly four people",
         lines=[("aling", "先給下水的人，他們冷。妳拿兩個給哥哥。", "淡淡的")],
         motion=f"A-ling puts the two buns into the nearer man's hand as she speaks; {quiet('Little Xiaohe and the two men', 'their', plural=True)}",
         zh="中景、慢推（送 `-an-l3`）：阿令第一格已經把竹籃放在石邊一塊平石上（稿子『放在岸邊石上』在第一格完成），把兩個饅頭塞到剛從水裡上來的壯丁（灰頭巾鐵鏽紅、暗橄欖綠，褲腳捲到膝）手裡、淡淡地說；小禾在她左邊、兩手第一格已經捧著兩個饅頭（稿子『再塞兩個到小禾手裡』在第一格完成），紙風車插在腰帶上、嘴閉著。不寫濕（拍法 12、畫風負面詞 wet clothes）"),
    dict(loc="af_e", cam="Low-angle close-up, slow push in", chars=["qinshuang"], night="aft",
         comp=f"low-angle close-up of {QIN}, seen from below, framed from the chest up with space above her head, standing on top of the big grey boulder, a few strands of hair stuck to her damp forehead, her left fist already planted on her hip from the first frame, her face three-quarter to screen left, looking down toward someone out of sight beyond the lower left edge of the frame, never the lens; that side of the frame is only the pale clear sky and the top paddles of the wheel all the way to the edge, and she is the only person in the frame; out of breath, not smiling: brows level, chest heaving, lips moving fast between panting words; behind her, soft, only the pale clear sky and the long top beam of the tall wooden frame; {HANDS}",
         lines=[("qinshuang", "第四片翻好了！後面還剩幾片？", "喘")],
         motion="Qin Shuang raises her flat right hand high toward the wheel as she calls out",
         zh="低角度近景、慢推（送 `-tian-l3`）：秦霜在大石上，額上幾縷頭髮黏著（稿子『額上汗』照拍法 12 寫黏髮），左手第一格已經叉腰，右手平掌往水車那邊高高一舉、喘著朝畫左下外看不到的人（岸上的人，不點名）喊（→ 答在 s17）。稿子『比出四根手指』改平掌（手指數目會讀錯，拍法 32）"),
    dict(loc="af_c", cam="Medium shot, slow push in", chars=["aling"], night="aft",
         comp=f"medium shot on the stone edge of the pond in the left half of the frame, framed from the waist up: {ALING}, her hands folded before her waist from the first frame, her face three-quarter to screen right toward the wheel at the right, her eyes on its paddles, never the lens; she is the only person in the frame; cold and flat, not smiling: brows level, eyes cool, lips moving evenly between words; beside her at the right, the near rim, spokes and paddles of the wheel; {HANDS}",
         lines=[("aling", "妳數慢了。第八片已經上架了，剩四片。", "冷冷地")],
         motion="A-ling lifts her flat right hand toward the top of the wheel as she speaks, her eyes staying on it",
         zh="中景、慢推（送 `-bian-l3`：左邊石邊、右邊輪緣與葉板）：阿令站在左半、兩手交疊在腰前，抬手平掌往水車架上一比、眼睛看著葉板、沒看秦霜，冷冷地說（答 s16）"),
    dict(loc="af_s", cam="Medium shot, slow push in", chars=["qinshuang"], night="aft",
         comp=f"medium shot of {QIN}, standing on top of the big grey boulder at the right of the frame, framed from the knees up, her face three-quarter to screen left {off('left', SIDE_STONE, he='she')}; dry and amused: one brow raised, a corner of her mouth tugged up, lips moving crisply between words; behind her, soft, the posts of the tall frame and the dry furrowed field in the white afternoon sun; {HANDS}",
         lines=[("qinshuang", "眼睛倒尖。三班，最後四片，一起上！", "挑眉")],
         motion="Qin Shuang steps to the very edge of the boulder, ready to jump down, as she speaks",
         zh="中景（膝以上）、慢推（送 `-shi2-l3`，獨立審稿必改 2：較寬的大石裁切，石頂上方留得出膝以上的人）：秦霜在大石上，朝畫左外看不到的人（阿令，不點名）挑一下眉、嘴角挑一下（稿子准的），一步走到大石邊上、說；稿子『從大石上跳下去落進淺水』不拍空中那一下（拍法 41 的做法：跳的那一下交給剪接，s19 第一格她已經在水裡）。稿子的近景改膝以上（走到石邊要看得見）"),
    dict(loc="af", cam="Wide shot, slow push in", chars=["shimujiang", "qinshuang", "xuyan"], night="aft",
         comp=f"wide shot at standing eye height, like the picture, the whole wheel in the frame: up on the wheel's wooden trestle in the water {CARP_WORN}, framed full figure, small, {MALLET} already lowered in his right hand from the first frame, his face toward the paddle before him, his lips pressed shut, never the lens; standing knee-deep in the green water at the foot of the wheel {QIN}, framed full figure, small, her face three-quarter to screen left toward the bank, never the lens; breathless and fierce, not smiling: lips moving fast between shouted words; a step further out beside her, waist-deep in the water, {GANG3}, their hands resting on the lowest paddle, their lips closed, never the lens; on the stone edge at the left by the stone steps {XU_WORN}, framed full figure, small, his face toward the wheel, his lips pressed shut, never the lens; {HANDS}; exactly five people",
         lines=[("qinshuang", "十二片，一個時辰，全翻完了！", "喘著，爽快")],
         motion=f"Qin Shuang thrusts her flat right hand high above her head as she shouts; {quiet('Carpenter Shi, Xu Yan and the two men', 'their', plural=True)}",
         zh="全景、慢推（送整張 `set-shentan-l3`）：石木匠在輪架上、最後一根釘第一格已經敲完、木槌垂著；秦霜站在輪腳及膝的潭水裡（s18 跳下去的結果），右手平掌高高舉起、喘著爽快地喊；三班兩人（土黃頭巾：暗青、深酒紅）在她旁邊再外面一步、齊腰的水裡、手扶最下面的葉板；穿鞋句只寫看得到腳的許硯與石木匠（秦霜及膝在水裡，mkspec；獨立審稿建議 3）；許硯在左邊石階旁的石邊、嘴閉著。稿子『最後一片被托上去、石木匠敲最後一顆釘』在第一格完成（一鏡一個動作）；稿子的低角度照圖的高度。翻完一個重音"),
    dict(loc="af_c", cam="Medium shot, slow push in", chars=["hanbo", "xuyan"], night="aft",
         comp=f"medium shot on the stone edge of the pond at the narrow gap by the stone steps, beside {SLUICE}, both framed from the waist up: on the left {HAN}, the staff in his left hand at his far side, his face three-quarter to screen right toward Xu Yan, his lips pressed shut, never the lens; moved, not smiling; on the right {XU_WORN}, already holding the loose end of the gate's rope out in both hands from the first frame, his face three-quarter to screen left toward Elder Han, never the lens; warm and steady, not smiling: brows level, lips moving gently between words; the staff stays well apart from the rope; behind them, soft, the stone steps and the small wooden landing in the white afternoon sun; {HANDS}; exactly two people",
         lines=[("xuyan", "韓伯，這一閘是柳溪的，您來開。", "把繩子遞給他")],
         motion=f"Xu Yan lays the rope's end in Elder Han's free right hand and steps back one pace as he speaks; {quiet('Elder Han')}",
         zh="中景（雙人）、慢推（送 `-an-l3`：閘門照聖經〈道具〉寫在左邊石階那段石邊缺口：三片濕木板的小閘、閘頂一條粗繩）：韓伯在左、竹杖拿在**左手**（離鏡頭那側）；許硯在右、第一格已經兩手捧著閘繩的繩頭，把繩頭放進韓伯空著的右手、退後一步說（→ 答在 s21）；韓伯嘴閉著。竹杖與繩子分開寫（第 32 集 fix2：兩根長東西第一格不相連）"),
    dict(loc="af_c", cam="Close-up, slow push in", chars=["hanbo"], night="aft",
         comp=f"close-up of {HAN_NOSTAFF}, standing at the narrow gap of the stone edge, framed from the chest up with space above his head, both hands already gripping the thick rope tied to the top of the small wooden sluice gate before him from the first frame, his face three-quarter to screen right {off('right', SIDE_RIM)}; resolute, not smiling: brows level, eyes wet, lips moving slowly and firmly between words; behind him, soft, only the stone steps and the green water in the white afternoon sun; {HANDS}",
         lines=[("hanbo", "好。祖宗的梁，就看這一下了。", "重重點頭")],
         motion="Elder Han gives one slow heavy nod as he speaks",
         zh="近景、慢推（送 `-an-l3`；稿子『身後只有閘門與潭水』）：韓伯兩手第一格已經握緊閘繩（稿子『把竹杖靠在閘邊』在第一格完成：竹杖在胸以上的框外、不寫），重重點一下頭，朝畫右外看不到的人（許硯，不點名）說（答 s20；第二場結尾）"),
    # ---- scene 3: sunset of the tenth day: the pool (the free warm grade), the channel, the fields (set-hantian), the swarm.
    dict(chapter="深潭、新渠與田，日落", loc="xi_c", cam="Medium shot, slow push in", chars=["hanbo", "xiaohe"], night="sunset",
         comp=f"medium shot on the stone edge of the pond by the stone steps, both framed from the waist up: in the left foreground {HAN_NOSTAFF}, side-on to us, already gripping in both hands from the first frame the thick rope tied to the top of the small wooden sluice gate of three plain wet planks set upright in the narrow gap between the two flights of stone steps just beyond him, his face toward the gate, his lips pressed shut, never the lens; straining, not smiling: teeth set; his bamboo staff leaning against the stone edge beside the gate, well apart from the rope; a step behind him at the right {XIAOHE}, {PINWHEEL} held upright between her two pressed palms before her chest, her face three-quarter to screen right toward the wheel at the right edge of the frame, never the lens; holding her breath, not smiling: eyes wide, lips moving in a whisper; behind them, soft, the stone steps and the small wooden landing in the low golden sunset light; {HANDS}; exactly two people",
         lines=[("xiaohe", "轉啊……求求你，這次一定要轉。", "屏住呼吸，小聲")],
         motion=f"Elder Han throws his weight back on the rope, the sluice gate is pulled up out of the gap and a white rush of water pours through the gap toward the wheel at the right; {quiet('Elder Han')}",
         zh="中景（雙人）、慢推（送本集免費做的日落調色裁切 `set-shentan-xi-an-l3`）：**日落前**（時間跳在 s21→s22 這一刀：翻完要等潭水回滿，稿子場頭）。韓伯在左前、側面，兩手第一格已經握著閘繩（閘門立在他前面兩段石階中間那道窄缺口，`-xi-an-l3` 上正好有那道暗缺口；獨立審稿必改 4），往後一仰把閘板拉起來、一股白水從缺口衝向畫右的水車（原寫「潭水穿過閘流向水車」說不通：水車立在潭裡；接 s23 水沿石邊從左衝進輪子底下）（寫 pulled up，不寫 open，拍法 36；剪在拉起的一半，照稿子〈剪接〉），竹杖靠在閘邊的石沿上、離繩子遠；小禾在他右後一步、兩掌合著夾住紙風車、朝畫右的水車屏住氣小聲唸。韓伯嘴閉著"),
    dict(loc="xi", cam="Wide shot, static", chars=[], night="sunset", act=4,
         comp=f"wide shot at standing eye height, side-on, like the picture, the whole wheel in the frame from the first frame, the camera still: a white surge of water already rushing along the stone edge from the left into the pond under the wheel; only the wheel, its frames, the pond, the stone edge and the fields are in the frame",
         lines=[("qinshuang", "轉了！", "畫外，短喊")],
         motion=NOBODY + "In this shot the wheel starts turning and keeps turning: the rushing water strikes the lowest paddles, the big wheel jerks a quarter turn, pauses for a moment, then turns again, faster and faster, its paddles sweeping round steadily to the last frame while the water churns white under it",
         zh="全景、**固定**（送本集免費做的日落調色 `set-shentan-xi-l3`；不送人）：整架水車從第一格就在畫面裡、側面、照圖（原版必修：每鏡同一款）；第一格水已經沿石邊從左邊衝進輪子底下（剪接從水打到葉板開始）；水打在最下面的葉板上，輪子顛四分之一圈、停一下、再轉起來、越轉越快，到最後一格都在轉。**結果先寫**、鏡頭固定（第 32 集 fix2、第 33 集 s34 的寫法）。秦霜『轉了！』是畫外錄音（全集最大的揭曉，整個樂團起來）。稿子『低角度、前景石槽』照圖的高度"),
    dict(loc="xi_e", cam="Close-up, static", chars=[], night="sunset", act=3,
         comp="close-up of the top of the turning wheel exactly as in the picture against the sky, from the first frame: one flat wooden paddle after another sweeping up over the top of the rim, each lifting a sheet of pond water that streams off it and falls away in bright drops; only the wheel and the sky are in the frame",
         motion=NOBODY + "The wheel turns steadily, the paddles rising over the top one after another, water pouring off each in a sheet",
         zh="近景、固定（送本集免費做的 `set-shentan-xi-ye-l3`：輪子頂上的葉板對著天；不寫地點句，只寫時間與光，獨立審稿建議 1：原本的「在潭邊石邊、立在潭裡」會把鏡頭拉出潭與石邊）：**稿子 c24 的竹斗改葉板**：挑定的水車圖上**沒有竹斗、沒有木槽**（聖經〈道具〉水車列：文字也不寫），一片片平木葉板轉過輪頂、帶起一片水往下瀉。無台詞"),
    dict(loc="xi_c", cam="Medium shot, slow push in", chars=["shimujiang"], night="sunset",
         comp=f"medium shot on the stone edge beside the turning wheel, framed from the waist up: {CARP_WORN}, his face already tipped up toward the turning wheel above him from the first frame, his eyes on it, never the lens; he is the only person in the frame; laughing hoarsely at last: his mouth wide, eyes creased, lips moving between bursts of laughing words; behind him, soft, the spokes and paddles of the turning wheel and its trestle in the low golden sunset light; {HANDS}",
         lines=[("shimujiang", "轉起來了！七天沒白熬，梁沒白拆！", "啞著嗓子，難得笑")],
         motion="Carpenter Shi thumps his fist once against the wheel's wooden trestle beside him as he speaks",
         zh="中景、慢推（送 `set-shentan-xi-lun-l3`：輪子下半與輪架，日落）：石木匠第一格已經仰頭看著轉起來的輪子（**本鏡可以大笑**），一拳捶在輪架上、啞著嗓子說。稿子『被濺了一身水』『抹一把臉』不寫（拍法 12、畫風負面詞 wet clothes；一鏡一個動作）"),
    dict(loc="xq", cam="Wide shot, slow push in", chars=[], night="sunset",
         comp=f"wide shot at standing eye height along the channel, like the picture: in the foreground the dry cracked earth of the channel's bank; a head of brown water already rushing along the dry earthen channel away from us toward the far fields, pouring into the cracks; running along the channel bank beside the water, small, framed full figure, {RUNNERS}, never the lens; {HANDS}; exactly four people",
         motion=NOBODY + "The head of water runs on along the channel into the far fields and the four people run with it, their arms raised high",
         zh="全景、慢推（送本集免費做的較輕日落調色 `set-shentan-qu-xi2-l1`：`set-shentan-qu-l1`（第四輪 37043，`set-shentan-l1` 裁切上挖出的乾土渠）降對比、降飽和、提暗部、只帶一點暖色；獨立審稿建議 9：原本的 `-qu-xi-l1` 橘黑對比太重、像 CG）：水頭沿土渠往遠處的田衝、灌進裂縫；四個村民（十歲男孩芥黃、年輕婦人鐵鏽紅、壯中年暗橄欖綠、瘦中年炭灰，空手）沿渠岸跟著跑、舉手（稿子『約十人』照拍法 34 寫看得見的四個；『遠處渠尾揮手的背影』不寫）。跟拍改慢推；音效是歡呼。無台詞"),
    dict(loc="fd_c", cam="Medium shot, slow push in", chars=["hanbo"], night="sunset",
         comp=f"medium shot on the low grassy ridge at the edge of the field, framed from the waist up: in the middle {HAN_NOSTAFF}, already kneeling on the ridge from the first frame, both hands cupped before his chest holding a double handful of cloudy brown water from the furrow, his bamboo staff lying on the grass beside him, his face bent toward the water in his hands, never the lens; weeping: eyes wet and squeezed, his mouth trembling, lips moving brokenly between words; behind him, soft, {TWO_FIELD}, their lips closed, never the lens; beyond them the furrows with a thin sheet of brown water spreading along them, the houses and the far hills in the low golden sunset light; {HANDS}; exactly three people",
         lines=[("hanbo", "水……水上來了！柳溪的田，有水了！", "哭出來")],
         motion=f"the brown water runs out between Elder Han's trembling fingers as he speaks; {quiet('The two women behind him', 'their', plural=True)}",
         zh="中景、慢推（送本集免費做的 `set-hantian-geng-l1`：近處裂開的田壟、中間一道長草的低田埂、遠處的田、一排小屋與遠山，金黃低斜光）：**田邊**（新渠把水引到這三畝）。韓伯第一格已經跪在田埂上、兩手捧著一捧混濁的褐水（不寫 mud：第 32 集 fix3，水只在手裡、不沾在人身上），竹杖丟在身邊草上，水從指縫流下、哭著說；身後兩個婦人（深梅紫老婦白頭巾、深灰中年婦人褪色靛藍頭巾，空手）側身站著、嘴閉著。稿子『身後村民』照拍法 34 寫兩個"),
    dict(loc="fd_c", cam="Medium close-up, slow push in", chars=["hanbo"], night="sunset",
         comp=f"medium close-up of {HAN_NOSTAFF}, kneeling on the grassy ridge, framed from the waist up, his empty hands already resting on his knees from the first frame, his face lifted three-quarter to screen right toward someone out of sight beyond the upper right edge of the frame, never the lens; that side of the frame is only {SIDE_HILLS} all the way to the edge, and he is the only person in the frame; grave and heavy, not smiling: eyes wet, brows lifted, lips moving slowly and heavily between words; behind him, soft, only the strip of field, the houses and the far hills in the low golden sunset light; {HANDS}",
         lines=[("hanbo", "許先生，老頭子替全村，給您磕個頭。", "很重")],
         motion="Elder Han bends slowly forward from the waist toward the ground to bow as he speaks",
         zh="中近景（腰以上）、慢推（送 `set-hantian-tian-l1`：一條田、小屋與遠山，稿子『身後只有夕陽下的田』）：韓伯跪著、空手第一格已經放回膝上（稿子『放下泥水』在第一格完成），抬頭朝畫右上外看不到的人（許硯，不點名）很重地說，身子慢慢往前俯、要磕頭。稿子的近景改腰以上（俯身要看得見）；『白鬚上沾泥水』不寫（拍法 12、第 32 集 fix3）"),
    dict(loc="fd_c", cam="Medium shot, slow push in", chars=["hanbo", "xuyan"], night="sunset",
         comp=f"medium shot on the low grassy ridge at the edge of the field, both framed from the waist up: at the left {HAN_NOSTAFF}, kneeling, his face lifted three-quarter to screen right toward Xu Yan, his lips pressed shut, never the lens; overcome, not smiling; at the right {XU_WORN}, already down on one knee in front of him from the first frame, both hands gripping the old man's forearms, his face three-quarter to screen left toward him, never the lens; urgent, not smiling: brows drawn, lips moving fast between words; behind them, soft, the furrows with a thin sheet of brown water, the houses and the far hills in the low golden sunset light; {HANDS}; exactly two people",
         lines=[("xuyan", "韓伯快起來！梁是大家拆的，水是大家引的！", "急")],
         motion=f"Xu Yan rises and lifts Elder Han up to his feet by the forearms as he speaks; {quiet('Elder Han')}",
         zh="中景（雙人）、慢推（送 `-geng-l1`）：許硯第一格已經衝到韓伯面前、單膝跪下、兩手托住他的胳膊（稿子『從右邊衝過來』在第一格完成），一把把他拉起來、急急地說（剪在托起的一半，照稿子〈剪接〉）；**不笑**。稿子『自己半跪在泥裡』只寫單膝跪在田埂上（不寫泥：第 32 集 fix3）；跟拍改慢推"),
    dict(loc="fd_t", cam="Wide shot, slow push in", chars=["qianyuanwai"], night="sunset",
         comp=f"wide shot at standing eye height across the furrows toward the grassy bank under the big old tree at the right, like the picture: on the bank, framed full figure, {QIAN}, already backing away a step from the first frame, his face three-quarter to screen left toward the water in the furrows before him, never the lens; his mouth stuck in a stiff frozen stretch, eyes staring, his face drained pale, not smiling; lips moving stiffly between words; one step behind him {RETAINERS}, their lips closed, never the lens; {HANDS}; exactly three people",
         lines=[("qianyuanwai", "我的壩……白守了十天，就這樣沒用了？", "笑凍住，擠出來的")],
         motion=f"Qian Yuanwai fans himself with one wide sleeve as he speaks; {quiet('The two men behind him', 'their', plural=True)}",
         zh="全景（照圖的高度：人眼高，獨立審稿必改 3：圖上沒有高起的田埂，不從田裡往上拍）、慢推（送 `set-hantian-liu-l1`：右邊那棵大樹、樹下長草的田埂與田壟）：錢員外站在大樹下的田埂上（稿子的『右上田埂』照圖）、身後兩個錢家家丁（黑短打、黑布包頭、空手，聖經〈小角色〉：只在遠景），看著水流進田、往後退一步（第一格完成）、扇著袖子，笑容僵住、臉發白、擠出來地說（**不是開心的笑**，原版建議；家丁嘴閉著）（→ 答在 s31）。錢員外胸前沒有吊牌（寫錦袍前襟素面）"),
    dict(loc="fd_t", cam="Medium shot, slow push in", chars=["qinshuang"], night="sunset",
         comp=f"medium shot on the grassy bank under the big old tree, framed from the waist up: {QIN}, already arrived up on the bank from the first frame, both hands planted on her belt, her face three-quarter to screen right {off('right', SIDE_TREE, he='she')}; scornful: a cold curl at one corner of her mouth, eyes narrowed, lips moving crisply between words; behind her, soft, the furrows of the field and the far hills in the low golden sunset light; {HANDS}",
         lines=[("qinshuang", "員外，你的壩沒用了，留著洗腳吧。", "不屑")],
         motion="Qin Shuang lifts her chin a little toward the right edge of the frame as she speaks",
         zh="中景、慢推（送 `-liu-l1`）：秦霜第一格已經從田邊走上田埂、停在錢員外前一步（稿子的跟拍改慢推），兩手叉在腰帶上（**柴刀不寫**，拍法 5），下巴一抬，朝畫右外看不到的人（錢員外，不點名）不屑地說（**本鏡可以冷笑**；答 s30）。稿子『褲腳濕到膝』不寫（畫風負面詞 wet clothes）"),
    dict(loc="fd_t", cam="Medium shot, slow push in", chars=["qianyuanwai"], night="sunset",
         comp=f"medium shot on the grassy bank under the big old tree, framed from the waist up: {QIAN}, already turning away to the right from the first frame, his face looking back over his right shoulder toward the field beyond the lower left edge of the frame, never the lens; he is the only person in the frame; sour and dark, not smiling: his face fallen, jaw clenched, lips moving through gritted teeth between words; behind him, soft, the trunk of the big old tree and the far hills in the low golden sunset light; {HANDS}",
         lines=[("qianyuanwai", "哼，有水算什麼。田裡長不出糧，一樣得求我。", "咬牙")],
         motion="Qian Yuanwai gives his sleeve one sharp shake, walks away toward the right edge of the frame and throws the words back over his shoulder as he goes",
         zh="中景、慢推（送 `-liu-l1`）：錢員外臉一沉、甩一下袖子往畫右走，邊走邊從**右肩**回頭朝畫左下外的田撂一句（第 33 集獨立審稿必改 3 同一件事：往右走、從靠鏡頭那側的右肩回頭）；**不笑**。稿子『家丁跟著走出畫面右』不拍（家丁只在遠景，s30 已交代）；跟拍改慢推"),
    dict(loc="fd_c", cam="Close-up, slow push in", chars=["xuyan"], night="sunset",
         comp=f"close-up of {XU_WORN}, standing at the edge of the field, framed from the chest up with space above his head, his eyes already lowered from the first frame, the low golden sunset light on one side of his face, never the lens; he is the only person in the frame; relieved, not smiling: brows easing, lips pressed shut; behind him, soft, only the strip of field, the houses and the far hills in the sunset; {HANDS}",
         lines=[("xitong", "叮。旱災任務完成，稻種保住。", "冷，宣布"), ("xuyan", "保住了。小棠顧著的那碗芽，今晚就能下田。", "心裡話，錄得近、輕", "inner")],
         panel=[("旱災任務完成，稻種保住", "task")],
         motion=f"Xu Yan lets out one long slow breath and lifts his eyes again toward the field; {SILENT_HE}",
         zh="近景、慢推（送 `-tian-l1`；稿子『身後只有轉著的水車』改成田與遠山：這一段在田邊，水車不在這個方向）：許硯眼睛垂著、半邊臉在夕陽裡，慢慢吐一口氣、再抬眼看田；系統與心裡話都是錄音、**全程嘴閉著**；面板剪接時疊（**不寫淡藍光**）。長鏡"),
    dict(loc="fd_c", cam="Medium shot, slow push in", chars=["xuyan", "xiaohe"], night="sunset",
         comp=f"medium shot at the edge of the field, framed from the waist up: in the middle {XU_WORN}, standing, both hands holding the ankles of {XIAOHE}, who already sits astride his shoulders from the first frame, {PINWHEEL} held up high in her right hand; his face lifted toward her, a tired warm smile, never the lens; her face tipped down toward him, a wide gap-toothed smile, lips moving eagerly between words, never the lens; behind them, soft, the furrows with a thin sheet of brown water, the houses and the far hills in the low golden sunset light; {HANDS}; exactly two people",
         lines=[("xiaohe", "哥，你看，風車轉對了，水車也轉對了！", "得意")],
         motion="the pinwheel spins fast in the wind as little Xiaohe holds it up high",
         zh="中景、慢推（送 `-geng-l1`）：小禾第一格已經騎在許硯肩上（稿子『一彎腰抱起、放上肩頭』在第一格完成：一鏡一個動作），許硯兩手扶著她的腳踝；她右手把紙風車高高舉著、風車**轉對了**呼呼地轉，得意地說（**本鏡兩人都可以笑**）"),
    dict(loc="fd_c", cam="Medium shot, slow push in", chars=["aling", "qinshuang"], night="sunset",
         comp=f"medium shot at the edge of the field where the channel water runs in, both framed from the waist up, side by side facing us; at their feet the brown channel water running in along the nearest furrow, glinting in the low sun, its rippling light playing on their faces: on the left {ALING}, her hands folded before her waist, her eyes down on the water, her lips pressed shut, never the lens; cool, not smiling; on the right {QIN}, already turning her head toward A-ling from the first frame, never the lens; teasing: a sly grin, lips moving lightly between words; behind them, soft, the furrows, the houses and the far hills in the low golden sunset light; {HANDS}; exactly two people",
         lines=[("qinshuang", "阿令，妳剛才嘴角動了，我看見了。", "側頭，笑著")],
         motion=f"Qin Shuang nudges A-ling's arm once with her right elbow as she speaks; {quiet('A-ling', 'her')}",
         zh="中景（雙人）、慢推（送 `-geng-l1`；稿子『渠邊』寫成渠水流進田的田邊，前景：腳邊渠水沿最近的田壟流進來、在低斜的夕陽下閃著，水光映在兩人臉上，獨立審稿建議 5：搬到田邊以後要寫出水從哪裡反光）：阿令在左、低頭看水、嘴閉著；秦霜在右，第一格已經側過頭，用**右**手肘（靠阿令那側）碰一下阿令的手臂、笑著說（**本鏡可以笑**；原版建議：有動作）"),
    dict(loc="fd_c", cam="Close-up, slow push in", chars=["aling"], night="sunset",
         comp=f"close-up of {ALING}, framed from the chest up with space above her head, the corner of her mouth already pressed flat again from the first frame, her face three-quarter to screen left toward the water running along the furrows below, her eyes on it, never the lens; she is the only person in the frame; cold and flat, not smiling: brows level, lips moving evenly between words; behind her, soft, only the furrows, the brown water running along them glinting in the low golden light; {HANDS}",
         lines=[("aling", "沒有。是水光晃到妳眼睛了。", "冷冷的")],
         motion="A-ling turns her face a little further away toward the water as she speaks",
         zh="近景、慢推（送 `set-hantian-di-l1`：田壟，水寫在文字：背景寫田壟裡流著、在金黃低光下閃著的褐水，好讓「水光晃到妳眼睛」讀得通，獨立審稿建議 5）：阿令嘴角第一格已經壓平（稿子『動了一下又壓住，不算笑』），把臉再轉開一點看著水、冷冷地說。稿子『手指撥一下頭髮』不拍（一鏡一個動作；拍法：髻與木簪照圖、不寫散髮）"),
    dict(loc="gy_c", cam="Low-angle close-up, slow push in", chars=["xiaohe"], night="grey",
         comp=f"low-angle close-up of {XIAOHE}, seen from below, high against the sky, framed from the chest up with space above her head, {PINWHEEL} already lowered in her left hand from the first frame, its vanes still, her face lifted three-quarter to screen right toward the far hills beyond the upper right edge of the frame, her eyes on them, never the lens; she is the only person in the frame; frightened, not smiling: eyes wide, lips moving uncertainly between words; behind her, soft, only the darkening grey sky; {HANDS}",
         lines=[("xiaohe", "哥……北邊的天，怎麼一下子黑了？", "笑容沒了")],
         motion="Little Xiaohe stretches her flat right hand out toward the far hills at the upper right as she speaks",
         zh="低角度近景、慢推（送本集免費做的灰暗調色裁切 `set-hantian-hui-tian-l1`：變暗的天與遠山；背景只寫變暗的天：低角度胸以上，山在下緣外，獨立審稿建議 4：山不能同時在背後又在畫右）：**光變灰**（時間在 s36→s37 這一刀：北邊的蝗群把夕陽吃掉，稿子場頭）。小禾還騎在哥哥肩上（胸以上的框只寫她高高映在天上），笑容沒了、眼睛睜大，紙風車第一格已經垂在左手、不轉，右手平掌往畫右上的遠山一伸（單指會讀錯，拍法 32），問（→ 答在 s40）；**不笑**"),
    dict(loc="gy_c", cam="Close-up, slow push in", chars=["aling"], night="grey",
         comp=f"close-up of {ALING}, framed from the chest up with space above her head, her face already lifted three-quarter to screen right toward the far hills beyond the right edge of the frame from the first frame, her eyes on them, never the lens; she is the only person in the frame; alert, not smiling: eyes narrowed, head tilted a little to listen, lips moving softly between words; behind her, soft, only the darkening grey sky; {HANDS}",
         lines=[("aling", "風是冷的，還帶著嗡嗡的聲音。", "很輕，警覺")],
         motion="A-ling tilts her head sharply to listen and holds still as she speaks",
         zh="近景、慢推（送 `-hui-tian-l1`；背景只寫變暗的天，獨立審稿建議 4）：阿令第一格已經抬頭朝畫右的北邊，猛地偏頭側耳聽、定住（動作不再寫「轉向山」：第一格已經朝右，再轉會先轉開再轉回來），很輕地說；**不笑**。稿子『冷風吹起她的裙角』在近景裡看不到，不寫"),
    dict(loc="gy_c", cam="Medium shot, slow push in", chars=["xuyan"], night="grey",
         comp=f"medium shot at the edge of the field, framed from the waist up: {XU_WORN}, standing, his face three-quarter to screen right toward the far hills beyond the right edge of the frame, his eyes on them, never the lens; tense, not smiling: jaw set, teeth clenched, lips moving low between words; across his shoulders at the top edge of the frame, cut by it, only a small girl's two legs in patched lilac trousers and cloth shoes and a small woven straw rabbit at her sash, his two hands already gripping her ankles from the first frame; behind him, soft, the furrows and the far houses under the darkening grey sky; {HANDS}; he is the only one whose face is in the frame",
         lines=[("xuyan", "小禾，抓緊哥。大家先別出聲，聽。", "壓低聲音")],
         motion="Xu Yan takes half a step back, gripping the small ankles tight, as he speaks",
         zh="中景、慢推（送 `-hui-geng-l1`）：許硯肩上是小禾，畫面上緣只露她的腿、布鞋與草兔子（不點名、不送她的圖：她的臉不在框裡），兩手第一格已經抓緊她的腳踝，往後退半步、朝畫右的北邊壓低聲音說；**不笑、咬牙**（原版建議）"),
    dict(loc="gy", cam="Wide shot, slow push in", chars=[], night="grey",
         comp=f"wide shot from low behind the people at the field edge toward the far hills, like the picture: at the bottom edge of the frame, cut by it, soft and out of focus, the backs of the heads and shoulders of {BACKS}; far beyond the fields and the row of small houses, {SWARM}; {HANDS}; exactly three people, all seen only from behind",
         lines=[("hanbo", "那不是雲，是蝗蟲！蝗蟲過山了！", "畫外，大喊")],
         motion=NOBODY + "the dark band of tiny specks rolls slowly over the hills toward us, the last warm light on the fields fades to grey, and the three people lift their heads toward it",
         zh="全景（低角度、主觀，望向遠山）、慢推（送本集免費做的灰暗調色 `set-hantian-hui-l1`：整張田、小屋與遠山）：前景下緣虛焦的三個背影（短灰鬚本色麻老漢、鐵鏽紅年輕婦人、芥黃十歲男孩，不點名）；遠山上一條**密密麻麻小黑點組成的壓低褐黑色帶子**壓過山頭往這裡移、最前面散開（原版必修：不是煙、不是火山、不是雷雨雲；照聖經〈道具〉的正面寫法，不寫否定名詞，拍法 18），田上最後一點暖光熄成灰。韓伯的喊是畫外錄音（答 s37；本集結尾，懸念交給第 35 集第一場）"),
]

HEAD = [
    "- 重製版 r2、真人版（站主 2026-11-11「之後都用真人版」）：照 `docs/videos/zhong-tian-qu-qi-e034-r2/script.md`（c01–c40 對應 s01–s40；含「這版改了什麼」「2026-11-06 審稿後的修改」）；台詞一字不改，只改拍法；每鏡一個看得見的動作、一句一筆不拆半句、預設不笑。篇章設定 `production/r2-bible-e031-e040.md`（拍法 1–43 條、〈場景〉〈接點〉〈道具〉〈小角色〉），帳照 `r2-bible-e011-e060.md`。**第 4 篇章〈旱年〉第四集**。",
    "- 內部工作編號 934（`hailuo/{ff,clips}-dh-e934.json`；`colab/runs/e934/extras.json`、`colab/runs/e934-live/spec.json`、工作資料夾 `~/mokaair-work/videos/zhong-tian-qu-qi-e934-dh/`）；發布 slug `zhong-tian-qu-qi-e034-r2`。不放集數、不放片名卡；**s01 照第 33 集 r2.py 的 s35／s40 寫**（接點 33→34：許硯在輪子左邊石邊、右手按右緣停住的葉板，送 `set-shentan-bian-l3`；不重播錢員外的笑）——**第 33 集還沒拍完，成片後要照實拍重核 s01**；s40 交給第 35 集（同一夜、許家屋內）。",
    "- 照第 33 集兩份審稿的通則一開始就照做：參考圖跟文字一致（水車照 `set-shentan-l3`：十二片平木葉板、**沒有竹斗與木槽**，稿子 c24 的竹斗改成葉板帶水）；長東西第一格不相連（竹杖與閘繩、鐵錘與鐵釘）；場景句照圖（平地上的潭、田是平的、只有一道低田埂）；不寫 crowd、寫實際人數；沒有人的鏡不加布鞋句；背景的人寫手上拿什麼、不寫兵器字；不寫泥（水寫成褐色的水，只在手裡與田壟裡，不沾在人身上）；`OFFSCREEN_SPEECH = False`、對畫外的人說話寫「朝畫左／右外看不到的人」；不寫 open、不寫否定名詞。",
    "- **人物**：秦霜柴刀整集不寫（拍法 5）、空手；王二牛與唐小棠本集不入鏡（稿子）。阿令送 `aling-portrait-l1`（沒戴鐵鐐，稿子要的 `aling-portrait-t2` 就是它，**不用另畫**）、不戴面巾、長袖蓋住手腕、木簪；s14 起一個竹籃。小禾八歲、紙風車四片白紙葉插竹籤（聖經〈道具〉），s34 起騎在許硯肩上。韓伯一根竹杖：s07 拄著、s20 拿在左手、s21 起靠在閘邊、s27 丟在田埂上。石木匠一把木槌、鐵錘只在許硯手上（s13）。錢員外只在 s30–s32（笑容凍住、不笑；胸前沒有吊牌），家丁兩人只在 s30 遠景。壯丁三班照頭巾顏色（灰、褪色靛藍、土黃），每人衣色年紀不同。",
    "- **軸線（照圖）**：深潭照第 33 集：鏡頭在潭近端石邊，水車在中間偏左立在潭遠端，左邊石階、小木台、矮木架與閘門（石邊缺口），右邊潭邊大灰石（秦霜站的地方）、高木架；許硯、韓伯、阿令在左邊石邊，朝畫右看水車。新渠：水從近處往遠處的田流。**田**（`set-hantian-l1`）：田壟、一道低田埂、右邊一棵大樹、左邊一排小屋與遠山；韓伯跪在田埂上，錢員外在右邊大樹下的田埂（稿子的右上田埂），**s35–s40 留在田邊**（稿子寫回潭邊；蝗群要壓過北邊的山，只有田的圖有山），北邊在近景裡是畫右（稿子的畫面右上），s40 是他們的主觀鏡。",
    "- **時間與光**：第一場正午白光（照第 33 集正午的圖）；第二場午後（同一張圖，白光、影子還短）；第三場日落：潭邊送本集免費做的日落調色（`-xi`），田的圖本來就是金黃低斜光；**s37 起光變灰**（本集免費做的灰暗調色 `-hui`）。時間跳都在剪點（s11→s12、s21→s22、s36→s37），不在鏡頭裡變光（s40 的動作句寫最後的暖光熄成灰）。",
    "- **原版必修**（聖經第 34 集）：蝗群畫成火山黑煙 → s40 照聖經〈道具〉寫「無數小黑點組成的壓低褐黑色帶子，壓過遠山」、最前面散開，只拍這一鏡（不寫煙、火山的否定句：否定名詞會被畫出來）；原版建議：錢員外「我的壩」笑容凍住（s30）、許硯「小禾，抓緊」咬牙不笑（s39）、小禾「北邊」笑容收起風車停住（s37）、紙風車每鏡同一款白紙竹籤、秦霜用手肘碰阿令（s35）、渠邊空中的黑團拿掉（蝗群只在 s40）、錢員外胸前沒有吊牌。",
    "- 要買的秒數（BUY，錄音前照第 33 集的估法：一句 6 秒的鏡放得下約 5.9 秒人聲、8 秒約 7.3 秒；第 33 集量到許硯約 3.5–4 字／秒、秦霜約 3.6、石木匠 2.5–3、韓伯 2.3–2.8、小禾 3.3–3.6）：s08、s09、s33 買 10 秒（系統加心裡話）；s03、s05、s07、s13、s14、s15、s17、s21、s25、s27、s28、s29、s30、s32、s39、s40 買 8 秒（石木匠、韓伯慢；17 字以上；有刪節號停頓的；s40 揭曉）；s24、s26 買 5 秒（沒有台詞的插鏡）；s01、s23 買 6 秒（沒有台詞的接點、轉起來要看得出越轉越快）；其餘照 `gen-dh.mjs` 的預設（說話 6 秒）。**錄音後照 `span934.sh` 量人聲長度重核**，放不下的改 BUY、重 build、重跑 prep。",
    "- **表上的「秒」欄是 lint 估法**，比錄音短；剪接以錄音的人聲長度為準。",
    "- **田與渠（s26–s40）表上的提示詞帶「below the deep pool」「At the deep pool …, beside」**：只為了讓 `gen-dh` 的 `SET` 選到深潭那張圖（再由 `spec.json` 換成田與渠的圖），d1 由 `mkspec.py` 拿掉（`R2.POOLMARK`→空、`R2.XQ_GEN`→`R2.XQ_LIVE`）；**之後每個 fix／retake spec 都要帶同一組替換**，不然模型會在田裡畫出潭（獨立審稿建議 6）。",
]
FOOT = [
    "- **參考圖**（`assets/refs-live/`）：許硯 l1、angle-a（帶笑的 angle-b 整集不送；全景 s19 只送 l1）；阿令 l1、angle-a（angle-b 不送；全景 s14 只送 l1）；錢員外 l1、angle-a（angle-b 不送；全景 s30 只送 l1）；秦霜、小禾、韓伯、石木匠每鏡只送 l1（`retake.py` 只能換或拿掉圖、不能加圖；第 33 集同）。s01、s03 的小手、s05、s06 過肩的背影、s39 肩上的腿、s40 的三個背影、壯丁、村民、家丁都不送圖、不點名。",
    "- **場景圖**：正午與午後送第 33 集做好的 `set-shentan-l3`（s12、s19）與裁切 `-an-l3`（s04、s06、s07、s13、s14、s15、s20、s21）、`-bian-l3`（s01、s08、s09、s17）、`-lun-l3`（s05）、`-tian-l3`（s02、s11、s16；**s03 插鏡只當天的顏色**），加本集免費做的較寬大石裁切 `-shi2-l3`（s10、s18；獨立審稿必改 2，原本的 `-shi-l3` 不送）；日落潭邊送本集免費做的 `set-shentan-xi-l3`（s23）、`-xi-an-l3`（s22）、`-xi-ye-l3`（s24：輪頂葉板）、`-xi-lun-l3`（s25）；新渠較輕調色 `set-shentan-qu-xi2-l1`（s26；獨立審稿建議 9，`-qu-xi-l1` 不送）；田 `set-hantian-geng-l1`（s27、s29、s34、s35）、`-tian-l1`（s28、s33）、`-liu-l1`（s30、s31、s32）、`-di-l1`（s36）；變暗 `set-hantian-hui-l1`（s40）、`-hui-tian-l1`（s37、s38）、`-hui-geng-l1`（s39）。`set-shentan-l1`／`-l2` 與 l1 裁切、`-gongdi` 一族、`-chen` 一族、`set-shentan-qu-l1`（正午的光）、`set-hantian-l1` 本身（地平線三根小竿沒塗）不送。",
    "- **本集新做的圖**（2026-11-19，`live-action/free-e031-e040/`，各跑兩次逐位元一樣，寫進 refs-live README）：`shentan_xi.sh`（`set-shentan-l3` 裁大石 `-shi-l3`，獨立審稿後加較寬的 `-shi2-l3`；日落調色 `-xi-l3` 與裁切 `-xi-an`、`-xi-lun`、`-xi-ye`；`set-shentan-qu-l1` 同一個調色成 `set-shentan-qu-xi-l1`，獨立審稿後加較輕的 `-qu-xi2-l1`）；`hantian_crops.sh`（`set-hantian-l1` 先用 `hantian_clean.py` 塗掉遠處田邊三根小黑竿（一根像人影；原本用 ffmpeg delogo，留下灰色方塊，獨立審稿建議 7 後改成從框外像素橫著或直著內插、柔邊），再裁 `-geng`、`-liu`、`-tian`、`-di`，灰暗調色 `-hui` 與裁切 `-hui-tian`、`-hui-geng`）。**不花錢**；沒有付費圖。稿子要畫的 `aling-portrait-t2` 由 refs-live 的 `aling-portrait-l1`（沒戴鐵鐐）取代；`prop-shuiche-t1` 由聖經改成場景圖每鏡送。",
    "- **還缺、先用最接近的圖**（不花錢、註明在這裡）：(1) **閘門與石槽**圖上沒有：照第 33 集寫在左邊石階那段石邊缺口（文字）。(2) **工作台、鐵錘、竹籃、拆下的葉板**是文字加在圖上。(3) **水進田**：田的圖是乾的，水寫成田壟裡一薄層褐水（文字）；若草稿畫成整片水田，挑沒有的那支，兩支都滿水就 fix 時加「only the furrows nearest the ridge hold a thin sheet of water」。(4) **田的季節**：`set-hantian-l1` 的大樹與遠處的樹是金黃秋葉（挑圖時接受過；聖經〈時間線〉〈場景〉已照實改），文字只寫「the big old tree」，不寫葉色。(5) **新渠** `set-shentan-qu-l1` 很軟、偏 CG（README 記過），改送較輕的日落調色 `-qu-xi2-l1`；s26 草稿讀不出渠就剪掉（稿子：刪鏡先刪 c24、c26）。(6) **蝗群**只有文字（d1 兩支都像煙再做免費合成的小黑點參考圖）。付費改圖的建議見 `colab/runs/e934-live/PREP.md`〈還缺〉（都不擋 d1）。",
    "- 共用檔：沒有改（`build-r2.py` 的 `EN` 已有每個在畫面上說話的名字；`gen-dh.mjs`、`pilot.py`、`cast.json` 不動）。田與新渠的場景句帶「below the deep pool」「At the deep pool …, beside」只為了讓 `gen-dh` 的 `SET` 選到深潭那張（再由 `spec.json` 換成田與渠的圖），`mkspec.py` 在 d1 把這幾個字拿掉。對畫外說話、對葉板、日頭、水車、水與遠山說話的鏡，精修文字的通用說話視線由本檔結尾的 `live_clips()` 換成 d1 的方向句（`GAZE_REFINE`）；本集沒有唐小棠，`live_clips()` 只換視線。",
    "- **獨立審稿**（2026-11-19，`writer-tools/e034-r2/review-independent.md`）：必改 4 條全改（s40 與 s01–s03、s34、s38 的 clear-and-still 句逐鏡換掉，`mkspec`；s10、s18 改送較寬的大石裁切 `-shi2-l3`、s10 許硯站沙岸；s30 照圖的高度；s22 閘門位置與水流方向）；建議 12 條改了 10 條（s24 拿掉地點句、s01 兩手、s12 新木板與鞋句、s37 s38 背景只寫天、s35 s36 水光、田的裁切重塗、聖經金柳紅樹、s26 較輕的調色、s14 視線、fix／retake 的潭字替換寫進 PREP 與表頭），s40 蝗群參考圖與「田壟有水」付費圖等 d1 看了再定（PREP.md §5），s10 s18 的備案不用（必改 2 已做）。",
    "- **自審**（2026-11-19，`writer-tools/e034-r2/review.md`，不是獨立審稿）：必改 4 條已改（日落調色的影子是正午的短影，`SUNSET` 不寫影子長度；s28 那一側畫緣有大樹垂枝；`mkspec` 的全景誤列 s12；s07 視線句的 preflight 警告），建議 8 條給協調者；給獨立審查者的提示在 scratchpad `e934prep/review-prompt.md`。",
    "- **d1 前置**（2026-11-19，`colab/runs/e934-live/PREP.md`）：`colab/runs/e934/extras.json`、`colab/runs/e934-live/{mkspec.py,spec.json}`（種子 9341101／9341102）、scratchpad `tools/prep934.sh`、`tools/rec934.sh`（錄音，**沒跑**）、`e934d1.sh`（Colab session `zt-live3`，**沒跑**）。",
    "- 配音（2026-11-19 錄好 40 句，核對見 `~/mokaair-work/videos/zhong-tian-qu-qi-e934-dh/audio/README-retakes.txt`）：阿令（Achernar）四句 178–193 Hz，跟第 31 集（170–193）一樣低於聖經的 225–265，照第 31 集的決定不升（升上去會撞到秦霜）；秦霜（Autonoe）第二場 231–251，跟阿令差 3.1–4.0 個半音；第三場秦霜 s31 那句升成 `a30-p117`（234）、s35 的笑降成 `a35-p73`（258），跟阿令差 3.3 個半音以上（拍法 43）。韓伯（Enceladus）與石木匠（Schedar）：第一場韓伯 s07 降成 `a06-p93`（120，比石木匠 148 低 3.6 個半音）、第三場韓伯 s28 降成 `a27-p91`（97，比石木匠 s25 的 116 低 3.1）；石木匠這集不升（第三場韓伯哭與喊到 141–143，石木匠升 1.19 倍會撞上）。小禾（Leda）323–391、錢員外（Algenib）兩句 208–221 偏高（降調備援 `-p75`／`-p80`）。重錄 a02、a17、a19、a27 四句（`tools/rec934-retake.sh`，沒跑）。BUY 不用改（最緊 s28 a27 7.20 秒／8 秒）。",
    "- 配樂：第一場只有風聲與風車聲，s04 一個亮的重音接漸快的 strings；第二場明快的勞動曲（第 33 集工地那首的變奏），s19 翻完一個重音；第三場 s22 屏息的 strings，s23 轉起來整個樂團起來，s30 錢員外一句底下停一拍，s37 起被嗡嗡聲蓋過、只剩低音。音效見 script.md〈音樂與音效〉。",
]

# Seconds to buy. Estimated as e933 (before its recordings; e933's own recheck changed nothing): a 6 s shot holds about 5.9 s of
# speech, 8 s about 7.3 s; e933's lines ran Xu Yan 3.5-4 characters a second, Qin Shuang about 3.6, Carpenter Shi 2.5-3, Elder
# Han 2.3-2.8, little Xiaohe 3.3-3.6, A-ling not yet measured (cold and slow: as Elder Han).
# 10 s: s08 (system 11 + thought 12), s09 (system 14 + thought 12), s33 (system 11 + thought 18).
# 8 s: s05, s13, s25 (Carpenter Shi 14-18), s07, s21, s27, s28 (Elder Han 11-15, slow / weeping), s15, s17 (A-ling 15-16), s03
#      (Xu Yan 15 with a long pause), s14 (Xiaohe 18), s29 (Xu Yan 17), s30 (Qian Yuanwai 14 with a pause), s32 (17), s39 (13 with
#      a pause, low), s40 (Elder Han's shout 12 over the swarm, held).
# 6 s: s01 (no line: the junction, two beats), s23 (the wheel jerks, pauses, turns faster).
# 5 s: s24, s26 (no line: the paddles, the channel).
# 6 s (gen-dh's default for a spoken line): every other shot.
BUY = {"s08": 10, "s09": 10, "s33": 10,
       "s03": 8, "s05": 8, "s07": 8, "s13": 8, "s14": 8, "s15": 8, "s17": 8, "s21": 8, "s25": 8, "s27": 8, "s28": 8, "s29": 8,
       "s30": 8, "s32": 8, "s39": 8, "s40": 8,
       "s01": 6, "s23": 6, "s24": 5, "s26": 5}


# ---- the refine text (as e023-e033): hailuo/clips-dh-e934.json column 0 is the motion text refine-prep.py sends with a picked
# d1 draft. No Tang Xiaotang this episode (no collar sentence, no back shot). rule 31 (e030 review 建議 10): gen-dh's speaking
# gaze names "the person he/she is speaking to", who is not in the frame of these shots (or is a thing: the paddle, the sun,
# the wheel, the water, the far hills); the refine text gets d1's direction. anchor_form() puts gen-dh's words back for stage 1.
GAZE_GEN = {"he": "turned toward the person he is speaking to, face in profile or three-quarter profile, eyes on that person",
            "she": "turned toward the person she is speaking to, face in profile or three-quarter profile, eyes on that person"}
_R = "his face three-quarter to screen right toward someone out of sight beyond the right edge of the frame, his eyes on that spot"
_HL = "her face three-quarter to screen left toward someone out of sight beyond the left edge of the frame, her eyes on that spot"
_HR = "her face three-quarter to screen right toward someone out of sight beyond the right edge of the frame, her eyes on that spot"
_HLD = "her face three-quarter to screen left, looking down toward someone out of sight beyond the lower left edge of the frame, her eyes on that spot"
_HILLS_HE = "his face three-quarter to screen right toward the far hills beyond the right edge of the frame, his eyes on them"
# sid -> (pronoun, the direction sentence)
GAZE_REFINE = {
    "s02": ("she", _HR),
    "s04": ("he", "his face three-quarter to screen right toward the paddle under his hand, his eyes on it"),
    "s07": ("he", "his face lifted three-quarter to screen right toward the high sun beyond the upper right edge of the frame, his eyes on it"),
    "s11": ("she", _HLD), "s16": ("she", _HLD), "s18": ("she", _HL),
    "s14": ("she", "her face three-quarter to screen right toward the wheel at the right of the frame, her eyes on it"),
    "s17": ("she", "her face three-quarter to screen right toward the wheel at the right, her eyes on its paddles"),
    "s21": ("he", _R),
    "s22": ("she", "her face three-quarter to screen right toward the wheel at the right edge of the frame, her eyes on it"),
    "s25": ("he", "his face tipped up toward the turning wheel above him, his eyes on it"),
    "s27": ("he", "his face bent toward the water in his cupped hands, his eyes on it"),
    "s28": ("he", "his face lifted three-quarter to screen right toward someone out of sight beyond the upper right edge of the frame, his eyes on that spot"),
    "s30": ("he", "his face three-quarter to screen left toward the water in the furrows before him, his eyes on it"),
    "s31": ("she", _HR),
    "s32": ("he", "his face looking back over his right shoulder toward the field beyond the lower left edge of the frame, his eyes on it"),
    "s36": ("she", "her face three-quarter to screen left toward the water running along the furrows below, her eyes on it"),
    "s37": ("she", "her face lifted three-quarter to screen right toward the far hills beyond the upper right edge of the frame, her eyes on them"),
    "s38": ("she", "her face lifted three-quarter to screen right toward the far hills beyond the right edge of the frame, her eyes on them"),
    "s39": ("he", _HILLS_HE),
}


def live_clips(path):
    import hashlib
    import json
    clips = json.load(open(path, encoding="utf-8"))
    for key, row in clips.items():
        text = row[0]
        sid = key.split("-", 1)[1]
        assert "stand-up collar" not in text and "Tang Xiaotang" not in text, key
        if sid in GAZE_REFINE:
            pr, gaze = GAZE_REFINE[sid]
            assert text.count(GAZE_GEN[pr]) >= 1, (key, "speaking gaze")
            text = text.replace(GAZE_GEN[pr], gaze, 1)
        row[0] = text
        row[1] = hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]
    open(path, "w", encoding="utf-8").write(json.dumps(clips, ensure_ascii=False, separators=(",", ":")))


# e928 review 必改 1 (rule 39): ref2manifest.mjs (stage 1) strips gen-dh's refine anchor with ANCHOR_FF; prep934.sh hands stage 1
# the anchor form of the live file (this), then puts the live file back; the refine text (clips-dh) keeps live_clips()'s wording.
def anchor_form(text):
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
