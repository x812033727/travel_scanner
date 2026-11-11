"""Generate video.json for sothatswhy-p13-gps-timing (原來如此事務所 對話版 P13).

Run `python3 build_scenes.py` from anywhere: it rewrites video.json next to this file and freezes
every shot's camera move in cameras.json (a shot keeps the camera it was first given, so deleting
a shot never shifts the others: the camera is in the keyframe cache key).
Edit lines and prompts here, never in video.json.
Started from a copy of sothatswhy-p21-car-sickness/build_scenes.py (series constants, helpers,
assembly and self-checks unchanged; EXTRA and REWRITE start empty because P21's entries were picture
fixes for P21 only); the content is new.
2026-11-11 rules applied (dialogue-pilot README §4, §9, §10.6): the faster voice style for both characters,
`pauses: {line_ms: 0, scene_ms: 150}` and `still_motion: "beat"`, no `pause_after_ms` on lines except a
BEAT_MS beat on the line right before each `P:` payoff in the same scene, and only an upper bound on length.
Shot pacing (P21 storyboard score: median 3.9 s a picture against the series' 6-12 s): a short reaction line
gets its own shot only when the picture changes something, so most shots carry two to four lines.
`script.md` is written by `node tools/video/cli.mjs script --slug sothatswhy-p13-gps-timing` after this runs.
"""
import hashlib, itertools, json, os, re, sys, unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = "sothatswhy-p13-gps-timing"
CHECKED = "2026-11-11"
BEAT_MS = 500   # 答案揭曉前的一拍；第一集照這個試，成片量過再調（README §10.6）

# ---------- series constants ----------
# Both characters are identical to P06/P07/P14/P08/P21 (approved series sheets reused through the `series` tag):
# the chief as in P02/P05/P14, the kid in her notebook-free look (series README §3.2).
# Voice styles: the 2026-11-11 faster style (README §4): only the last sentence changes.
VOICE = {"provider": "gemini", "name": "Sulafat",
         "style": "標準國語，咬字清楚，台北人平常說話的語調。事務所的所長，溫和、有耐心，像陪一個好奇的小朋友和你一起找答案。語速偏快、輕快，像節目主持人，一秒五個字以上，句與句緊接、不拖長尾音。"}
SHEET = "character reference: one single full-body figure standing in the centre, facing the viewer in a slight three-quarter turn, relaxed friendly pose, both hands clearly drawn, plain empty cream background with nothing else in the picture, no turnaround, no second view, no seal, no stamp, no signature, no text"
CHARACTERS = [
    {"id": "chief", "name": "所長",
     "appearance": "a friendly middle-aged woman, the chief of a small question office, with round black glasses, shoulder-length dark hair with a streak of grey tied in a low ponytail, a warm smile, a mustard-yellow cardigan over a white blouse, ink-navy trousers, brown shoes, a yellow pencil tucked behind one ear",
     "voice": dict(VOICE), "sheet_prompt": SHEET},
    {"id": "kid", "name": "小問",
     "appearance": "a curious eight-year-old girl with a short black bob haircut with straight bangs and one small cowlick sticking up on top, large round eyes, wearing a navy raincoat-style jacket with a mustard-yellow hood, white sneakers, both hands free",
     "voice": {"provider": "gemini", "name": "Leda", "style": "標準國語，咬字清楚，台北人平常說話的語調；八歲小女孩的聲音，好奇、活潑，問問題時句尾上揚，語速輕快，一秒五個字以上，不拖尾音"},
     "sheet_prompt": SHEET},
]


# Identity goes LAST in every prompt (P02: putting it first drifted some frames to photo or 3D).
KIDDESC = "the girl has a short black bob with straight bangs and one small cowlick on top and wears a navy raincoat jacket with a mustard-yellow hood"
CHIEFDESC = "the chief wears round black glasses, her dark hair with a grey streak is tied in a low ponytail, a yellow pencil is tucked behind her ear, mustard-yellow cardigan"
WALL = "a plain pale wall behind her"
DAY = "bright daylight"
# Prompt words that P02/P05 taught us to keep out (README §3.1): the model has no negative prompt,
# lamps and night turn frames into 3D figurines, and these props sprout fake letters.
BANNED = re.compile(r"\b(no|not|without|text|blank|lamp|night|notebook|sign|signs|paper|poster|screen|book|calendar|whiteboard|thermometer|remote|label|magnet|microscope|arrow|arrows)\b", re.I)

CAMS = itertools.cycle(["push in", "pan left", "pull out", "drift", "tilt up", "pan right", "push in", "tilt down", "pull out", "drift"])
CAM_FILE = os.path.join(HERE, "cameras.json")
FROZEN = json.load(open(CAM_FILE, encoding="utf-8")) if os.path.exists(CAM_FILE) else {}

S = []
# README §10.1 (P07/P14): from P08 every kid shot restates the reference (KIDFIX) and every chief
# shot uses the grey-free CHIEFFIX_DESC (CHIEFFIX2). kid() and chief() put each id into its set, so the
# sets always hold every shot of that character; CHIEFFIX (the old tail) stays empty.
KIDFIX = set()
CHIEFFIX = set()
CHIEFFIX2 = set()  # every chief shot: the base description's grey streak kept winning (P07/P14 round 5)
CHIEFFIX_DESC = "the chief is a slim young woman of about thirty with glossy jet-black hair tied in a low ponytail, round black glasses, a yellow pencil tucked behind her ear, a mustard-yellow cardigan over a white blouse, flat 2D cel-shaded cartoon drawing with ink outlines"
KIDFIX_TAIL = ', exactly matching her reference sheet: the same little girl every time, short black bob with straight bangs, navy raincoat with mustard-yellow hood, long navy trousers, hood folded down behind her neck, bare short black bob uncovered and hanging free, simple dot-like cartoon eyes as on the reference sheet, a round young child face with big round matching eyes looking the same way, flat 2D cel-shaded cartoon drawing with ink outlines'
CHIEFFIX_TAIL = ', exactly matching her reference sheet: slim young woman, glossy jet-black hair with only one thin silver strand, mustard-yellow cardigan over a white blouse, flat 2D cel-shaded cartoon drawing with ink outlines'
# Lines added after a visual review (P08: photo-real, off-model, marks). Empty until this episode's keyframes are drawn.
FLAT = ", simple hand-drawn flat 2D children's cartoon illustration with clean ink outlines and flat colours"
HOOD = ", hood down, short black bob hanging free"
EXTRA = {}
# Whole-prompt rewrites after a visual review. Empty until this episode's keyframes are drawn and checked.
REWRITE = {}
def _shot(id, prompt, chars, lines, chapter):
    prompt = REWRITE.get(id, prompt + EXTRA.get(id, ""))
    assert not BANNED.search(prompt), (id, BANNED.search(prompt).group(0))
    assert id not in {s["id"] for s in S}, id
    assert len(prompt) <= 840, (id, len(prompt))  # MiniMax prompt budget (HANDOFF: about 840 characters)
    cam = FROZEN.get(id) or next(CAMS)
    S.append(dict(id=id, chapter=chapter, template="shot", data=dict(prompt=prompt, camera=cam, visual="still", characters=list(chars)), lines=list(lines)))
def kid(id, prompt, *lines, chapter=None):
    """The kid doing one simple thing, facing the camera, waist-up or head-and-shoulders."""
    KIDFIX.add(id)
    _shot(id, prompt.rstrip(". ") + ", " + KIDDESC + (KIDFIX_TAIL if id in KIDFIX else ""), ["kid"], lines, chapter)
def chief(id, prompt, *lines, chapter=None):
    """The chief, always waist-up or head-and-shoulders, in front of a plain wall in daylight."""
    assert prompt.startswith(("Waist-up", "Head-and-shoulders")), id
    CHIEFFIX2.add(id)
    _shot(id, prompt.rstrip(". ") + ", " + (CHIEFFIX_DESC if id in CHIEFFIX2 else CHIEFDESC + (CHIEFFIX_TAIL if id in CHIEFFIX else "")), ["chief"], lines, chapter)
def scene(id, prompt, *lines, chapter=None):
    """No character: an object, a place or a mechanism drawn as a picture."""
    _shot(id, prompt, [], lines, chapter)
    S[-1]["data"]["nobody"] = True  # PR #2028: no person or face in an object-only shot
def k(t, e=None, tag=None): return ("kid", t, e, tag)
def c(t, e=None, tag=None): return ("chief", t, e, tag)

def C(action, close=False):
    return ("Head-and-shoulders close-up" if close else "Waist-up medium shot") + " of the chief " + action + ", " + WALL + ", " + DAY
def K(action, close=False, where=None):
    return ("Head-and-shoulders close-up" if close else "Waist-up medium shot") + " of the girl " + (where + " " if where else "") + action + ", " + DAY

# One drawing language for the whole episode (README §10.5, P17/P18: the image model cannot draw orbits,
# spheres, diagrams, maps with labels, arrows, counts or directions). The main thread is ONE walk: 小問 walks
# between tall glass buildings to meet her classmates in the park, and the blue dot on her phone jumps across
# the street. The one analogy carried from start to end is THE WHISTLE GAME: friends spread around a park, each
# with a very good watch, blow a whistle on the hour; how late you hear each whistle tells you how far that
# friend is. Satellites are the friends; the phone's poor watch is why a fourth friend is needed; an echo off a
# wall is multipath; two whistles of different pitch are two frequencies; a friend reading out where he stands,
# very slowly, is the navigation message. Every mechanism frame is an everyday object at human scale: a whistle,
# a wristwatch, a jump-rope ring on the lawn, a glass wall in the sun, a cartoon satellite alone in the sky.
# Phones show only coloured blocks and a blue dot (README §3.1: name what the display shows, never writing).
STREET = "on a sunny sidewalk between tall smooth glass towers,"
CORNER = "at a sunny street corner by tall smooth glass towers,"
PARK = "in a sunny green park"
STYLE = ", simple flat 2D cel-shaded cartoon drawing with clean ink outlines and flat colours"
PHONE = "a small phone showing a simple pattern of pale green and grey blocks with one glowing blue dot"
WHISTLE = "a shiny silver whistle on a red cord"
WATCH = "a simple round wristwatch with a smooth plain white face and two hands"
SAT = "one cute cartoon satellite with two wide golden solar wings floating high in a deep blue sky above soft white clouds"
def obj(id, prompt, *lines, chapter=None):
    """An everyday-object frame with nobody in it, always in the flat cartoon style (P18: object
    prompts without style words came out as photos)."""
    scene(id, prompt + STYLE + ", clean empty corners", *lines, chapter=chapter)

# ---------- 開場（系列片頭之後直接進場景，不做濃縮；答案都不先講）----------
# The first picture is the problem itself: the phone with the blue dot, between the tall buildings.
obj("phone-dot", "Close-up of a child's small hand holding " + PHONE + " on a sunny city sidewalk, tall plain glass buildings with smooth unmarked walls rising behind",
    k("所長，我跟你說！", "急著報案的語氣"), k("我走路去公園找同學，"),
    k("地圖上的藍點，", "不可思議"), k("突然跳到對面那條街！", None, "S:jump"), chapter="大樓中間，藍點跳到對街")
# Thumbnail shot (fixed before keyframes, explainer-series/README.md): the kid big and centred, the phone in hand.
kid("kid-dot-puzzled", K("holding a small phone up in front of her chest with both hands and frowning at it in puzzlement, in the exact centre of the picture", where=STREET),
    k("可是我明明在這邊，", "不服氣"), k("它又跳回來了。", "困惑"))
chief("chief-listen", C("leaning forward with a curious smile, one hand on her chin", close=True),
      c("這在大樓中間很常見。", "接住上一句"),
      c("你叫車的時候，可能也看過車停在對面。", "轉向觀眾"))
chief("chief-tease", C("holding a small phone up beside her face with a playful knowing smile"),
      c("更怪的是：手機算你在哪裡，靠的是時間。", "賣關子"),
      c("時間只差百萬分之一秒，你猜，距離會差多少？", "數字放慢", "S:micro"))
kid("kid-wow", K("throwing both hands up with wide amazed eyes, a small phone in one hand", close=True, where=STREET),
    k("差一兩公尺吧？", "篤定的錯猜"))
chief("chief-promise", C("holding up one finger with a warm inviting smile"),
      c("比你猜的多很多。而且手機要聽的衛星，至少要四顆。", "賣關子", "S:four"),
      c("多出來的那一顆，到底在幫誰？", "賣關子"))
kid("kid-main-q", K("looking down at a small phone in her hand with a thinking frown", where=CORNER),
    k("手機到底怎麼用時間，", "想不通"), k("知道我在哪裡？", "句尾上揚", "S:main"))

# ---------- 第一章：聽聲音，算距離 ----------
kid("kid-ask-guess", K("pointing straight up at the sky with one hand and holding a small phone in the other, a confident grin", where=STREET),
    k("是手機問衛星，", "很有把握的錯猜"), k("衛星再告訴它我在哪嗎？", "句尾上揚", "S:ask"), chapter="衛星根本不知道你在哪")
chief("chief-lighthouse", C("shaking her head gently with a kind smile, one hand raised", close=True),
      c("剛好相反，衛星根本不知道你在哪。", "接住上一句", "P:ask"),
      c("美國政府的 GPS 網站說，衛星就像燈塔，"), c("只負責一直往下廣播。"))
obj("satellite-sky", "Wide shot of " + SAT,
    c("手機只聽、不說話，"), c("它要自己從聽到的東西，算出你在哪。"),
    k("只用聽的？", "不相信"), k("那要聽什麼？", "句尾上揚", "S:listen"))
obj("lightning-hills", "Wide shot of a bright zigzag lightning bolt over distant green hills under grey storm clouds, seen from a cosy covered porch with a wooden railing in daytime",
    c("你一定玩過：看到閃電就開始數，數到打雷。", "轉向觀眾"),
    c("美國氣象局說，雷聲大約五秒走一英里，"), c("換成公里，差不多三秒一公里。"))
kid("kid-count", K("counting on her fingers with a scrunched-up thinking face", close=True, where=PARK),
    k("數到六秒，", "算算看"), k("就是兩公里遠！"))
chief("chief-whistle-game", C("holding up " + WHISTLE + " in one hand with a cheerful smile"),
      c("對。我們用這個玩一個遊戲：公園裡站著幾個朋友，"),
      c("每人戴一支很準的錶，整點一到，就吹一聲哨子。"))
obj("whistle-tree", "Close-up of " + WHISTLE + " hanging from a low tree branch in a sunny green park, a wide lawn softly blurred behind",
    c("你聽到哨聲晚了多久，就知道離那個朋友多遠。", None, "P:listen"))
chief("chief-atomic", C("holding a small toy satellite model up in one hand with a proud smile"),
      c("衛星就是那個朋友。它帶著原子鐘，就是非常非常準的鐘，"),
      c("訊號裡寫著：我是什麼時候發出來的。"))
kid("kid-travel-q", K("shading her eyes with one hand and gazing up at the sky with a wondering face", where=PARK),
    k("衛星那麼遠，", "好奇"), k("訊號要走多久？", "句尾上揚", "S:travel"))
obj("satellite-high", "Wide shot of " + SAT + ", a tiny sunny city with tall glass buildings far below under the clouds",
    c("衛星大約在兩萬公里高。訊號從衛星跑到你手上，"),
    c("通常只要六十到九十毫秒，一毫秒是千分之一秒。", "數字放慢", "P:travel"),
    k("一眨眼都不到！", "驚訝"))
chief("chief-light", C("sweeping one flat hand quickly past her face with a bright amazed smile"),
      c("因為它跟光跑得一樣快，一秒大約三十萬公里。"),
      c("所以剛剛那百萬分之一秒，"), c("光就跑了大約三百公尺，不是一兩公尺。", None, "P:micro"))
kid("kid-rel-q", K("holding " + WATCH + " up to her ear with a curious face", close=True, where=PARK),
    k("差一點點都不行！", "驚訝"), k("那衛星的錶，", "追問"), k("真的那麼準嗎？", "句尾上揚", "S:relativity"))
chief("chief-rel", C("holding a small golden pocket watch with a smooth plain face up beside her face, a curious smile"),
      c("原子鐘很準，可是還有一件事要修。"),
      c("從地面看，它走得比較快，原因很有名：相對論。"))
obj("satellite-clock", "Wide shot of " + SAT + ", far above a big round green and blue planet curve at the bottom of the frame",
    c("衛星在很高的地方，地球拉得比較沒那麼用力，"),
    c("鐘會走快一點；它又跑得很快，跑快的鐘會慢一點。"),
    c("兩個加起來，還是快。"))
chief("chief-38", C("holding up her thumb and finger a tiny gap apart with a serious smile", close=True),
      k("快多少？", "追問"),
      c("照一篇 GPS 相對論的回顧換算，"),
      c("衛星的鐘一天快了三十八微秒多。"),
      c("一微秒，就是開頭那個百萬分之一秒。"))
kid("kid-38", K("shrugging with both palms up and a doubtful grin", where=PARK),
    k("那也太短了吧？", "不以為意"))
chief("chief-11km", C("pointing one finger at the viewer with a playful raised eyebrow"),
      c("你算算看：光在這段時間，可以跑十一公里多。", None, "P:relativity"),
      c("不修的話，哨子報的時間，一天就錯這麼多。"))
obj("satellite-workshop", "Wide shot of one cute cartoon satellite with two wide golden solar wings resting on a large clean workbench in a bright white workshop, sunny windows behind",
    c("所以有些衛星的鐘，上去之前就先在地面調慢；"),
    c("有些上去以後再量，把修正寫進廣播裡。"))
kid("kid-one-q", K("holding up one finger with a hopeful questioning face", where=PARK),
    k("時間能信了，", "追問"), k("那聽一顆衛星，"), k("就知道我在哪了？", "句尾上揚", "S:one"))
obj("rope-ring", "Wide shot of a long red jump rope laid out in one big round ring on a sunny green park lawn, " + WHISTLE + " lying in the middle of the ring",
    c("還不行。只聽一個朋友，你只知道離他多遠，", "接住上一句", "P:one"),
    c("你可能在他周圍一整圈的任何地方。"), c("換到太空，是一整顆大球的表面。"))
obj("hoops-lawn", "Wide shot of three big hula hoops in red, yellow and blue lying overlapping on a sunny green park lawn, soft trees behind",
    c("再聽第二個、第三個朋友，幾圈疊在一起，"),
    c("能站的地方就縮小了。"),
    c("先說清楚，畫圓圈只是幫你想像的示意。"))
kid("kid-three-q", K("holding up three fingers with a confident grin", where=PARK),
    k("那三顆就夠了吧？", "很有把握"), k("第四顆要幹嘛？", "章尾停住，句尾上揚", "S:three"))

# ---------- 第二章：第四顆衛星，是來對錶的 ----------
chief("chief-condition", C("holding up one finger with a calm knowing smile", close=True),
      c("三顆是夠，不過有一個條件。", "接住上一句"),
      c("美國聯邦航空總署寫得很清楚：你手上也要有一顆，"),
      c("跟 GPS 對好時間的原子鐘。"), chapter="第四顆衛星，是來對錶的")
kid("kid-clock-q", K("holding a small phone up close and peering at it with narrowed curious eyes", close=True, where=STREET),
    k("我的手機裡，", "懷疑"), k("有原子鐘嗎？", "句尾上揚", "S:clock"))
chief("chief-watch-fast", C("tapping " + WATCH + " on her wrist with a playful smile"),
      c("沒有，手機裡沒有那麼準的鐘。", "接住上一句", "P:clock"),
      c("回到公園。哨子是聲音，假設你的錶慢了一秒，"))
obj("wristwatch", "Close-up of a child's wrist wearing " + WATCH + ", resting on a wooden park bench in sunshine",
    c("每一聲哨子，你都以為它走得比較短，"),
    c("聲音一秒跑三百多公尺，每個朋友都像近了這麼多。"))
kid("kid-all-close", K("looking around in confusion with both hands raised, a small phone in one hand", where=PARK),
    k("大家一起變近？", "困惑"), k("那我到底在哪？"))
chief("chief-no-match", C("spreading her hands with an honest puzzled smile"),
      c("你找不到一個點，跟每個朋友的距離都對得上。"),
      c("所以要多聽一個朋友，"),
      c("把你的錶差了多少，也當成一個要算的答案。", None, "P:four"))
chief("chief-four-unknowns", C("counting on her fingers with a thoughtful smile", close=True),
      c("換回衛星：東西、南北、高低，再加上錶差多少，"),
      c("四個不知道的數，要四顆衛星才解得出來。", None, "P:main"))
kid("kid-four-got", K("clapping her hands together with a bright realising grin", where=PARK),
    k("原來第四顆衛星，", "恍然大悟"), k("是來幫手機對錶的！", None, "P:three"))
chief("chief-practice", C("giving a small thumbs-up with a pleased smile", close=True),
      c("說得好。還記得剛剛那些圓圈嗎？"),
      c("真的手機不畫圈，是把四個答案一次算出來。"))
chief("chief-best-fit", C("bringing both open hands slowly together in front of her with a satisfied smile", close=True),
      c("聽到的衛星超過四顆，它就找一個跟大家最合得來的答案。"))
kid("kid-sky-q", K("tilting her head back and looking up at the open sky with a hopeful face", where=PARK),
    k("天上隨時都有，", "追問"), k("四顆給我聽嗎？", "句尾上揚", "S:sky"))
obj("satellite-sky-wide", "Wide shot of a bright blue sky over a sunny green park, one cute cartoon satellite with golden solar wings floating high among soft white clouds",
    c("美國政府的 GPS 網站說，衛星的基本排法有二十四個位置，"),
    c("地球上幾乎任何地方，都看得到至少四顆。", None, "P:sky"))
kid("kid-geometry-q", K("holding up four fingers with a thinking face", close=True, where=PARK),
    k("那同樣是四顆，", "追問"), k("每次都一樣準嗎？", "句尾上揚", "S:geometry"))
chief("chief-geometry", C("holding her two hands apart as if measuring something, a careful thoughtful smile"),
      c("不一樣。GPS 的官方性能標準寫：位置的誤差，"),
      c("大約是量距離的誤差，乘上一個放大的倍數。"))
chief("chief-geometry-2", C("turning a small toy satellite model slowly in one hand and studying it with a curious smile", close=True),
      c("這個倍數，看衛星和你的相對位置好不好。"),
      c("位置太差的時候，甚至算不出來。"))
chief("chief-five", C("nodding with a confident smile, one finger raised", close=True),
      c("標準也寫：用五顆以上去算，倍數一定不會比四顆差。", None, "P:geometry"))
kid("kid-sky-strip", K("looking straight up with her mouth open in surprise", where=STREET),
    k("我在大樓中間，", "發現"), k("天空只剩一條縫！"))
obj("sky-strip", "Low angle view looking straight up between two tall plain glass buildings with smooth unmarked walls, a narrow strip of bright blue sky between them",
    c("對，大樓擋住了一部分衛星，"),
    c("能用的變少，放大的倍數就可能變大。"))
kid("kid-signal-q", K("holding a small phone out at arm's length and frowning at it", where=STREET),
    k("所以藍點跳走，", "推理"), k("是衛星的訊號不準？", "章尾停住，句尾上揚", "S:signal"))

# ---------- 第三章：時鐘和路上，怎麼帶偏藍點 ----------
chief("chief-signal-good", C("shaking her head with a confident smile, one hand raised", close=True),
      c("衛星送得其實很準。", "接住上一句"),
      c("美國政府承諾，所有衛星平均，訊號本身的誤差，"),
      c("九成五的時間在兩公尺以內。"), chapter="訊號撞上大樓，繞了遠路")
chief("chief-2021", C("holding a small toy satellite model up proudly with a bright smile"),
      c("二〇二一年四月二十日實際量到的，還不到六十五公分。"))
kid("kid-military-q", K("crossing her arms with a suspicious pout", where=CORNER),
    k("會不會給我們的，", "懷疑"), k("故意弄不準？", "句尾上揚", "S:military"))
chief("chief-sa", C("shaking her head with a calm reassuring smile", close=True),
      c("美國政府的 GPS 網站說：沒有故意把民用的弄差。", None, "P:military"),
      c("以前曾經故意讓民用的變不準，二〇〇〇年就停了。"))
kid("kid-then-why", K("pointing across a sunny street with a frustrated frown", where=CORNER),
    c("而且訊號本身變差，到處都會偏，不會專挑大樓中間。"),
    k("那我的手機，", "不服氣"), k("怎麼會差到對街？", "句尾上揚"))
chief("chief-ure-not", C("holding up one finger with an honest careful smile", close=True),
      c("官方特別說明：訊號的誤差，不等於你手上的誤差。", None, "P:signal"),
      c("手上的誤差，還要加上訊號在路上遇到的事。"))
chief("chief-mooc", C("holding a small phone out towards the viewer with a friendly smile"),
      c("史丹佛的一門線上課，讓上千個人，在一百個國家用手機量。"),
      c("開闊的地方，平均差大約五公尺。"))
obj("city-towers", "Wide shot of a sunny city street lined with very tall smooth glass towers on both sides, a few small green street trees along the sidewalk",
    c("在城市裡，誤差跟旁邊的大樓有多高，關係很大。"))
kid("kid-echo-q", K("pointing up at a tall glass building with a suspicious frown", where=STREET),
    k("是大樓把訊號，", "猜"), k("吃掉了嗎？", "句尾上揚", "S:echo"))
chief("chief-echo", C("bouncing one flat hand off the other palm with a curious smile", close=True),
      c("還記得那條天空的縫嗎？有時候是擋住；有時候更麻煩，"),
      c("訊號撞到牆，反彈以後才進你的手機。"))
obj("glass-wall", "Close-up of a tall smooth glass building wall reflecting the bright sun and the blue sky, a small green street tree in front of it",
    c("回到公園：哨聲撞到一面牆，繞了遠路才到你耳朵，"),
    c("你就以為那個朋友比較遠。這叫多路徑。", None, "P:echo"))
chief("chief-echo-where", C("holding a small phone close to a pale wall with a thoughtful smile"),
      c("歐洲太空總署的導航教材說，"),
      c("主要是因為天線太靠近會反射的東西；"),
      c("從很低的地方斜斜進來的衛星，影響最大。"))
kid("kid-iono-q", K("pointing high up at the sky with a curious face", where=PARK),
    k("那天上那段路呢？", "追問"), k("也會走歪嗎？", "句尾上揚", "S:iono"))
obj("haze-sky", "Wide shot of a bright blue sky with a soft shimmering band of pale violet haze high above the white clouds, " + SAT.replace("one cute", "a cute").replace(" floating high in a deep blue sky above soft white clouds", "") + " above the haze",
    c("會。訊號要穿過高空一層叫電離層的地方，"),
    c("在那裡會被拖慢。"),
    c("衛星用不同的頻率送訊號，就像哨子有高音和低音。"))
chief("chief-guess-model", C("shrugging with both palms up and an honest smile"),
      c("只聽一個頻率的話，只能靠預先估好的修正去猜，"),
      c("這個效應可以到幾十公尺。"))
chief("chief-model-half", C("holding her hand flat and lowering it halfway with an honest smile", close=True),
      c("衛星廣播的修正，估計全世界平均約修掉一半。"),
      c("可是拖慢多少，跟頻率有關。同時聽兩個頻率，"))
obj("two-whistles", "Close-up of two whistles lying side by side on a wooden park bench in sunshine, one big silver whistle and one small golden whistle, each on a red cord",
    c("就像同一個朋友，吹高低兩支哨子；"),
    c("比一比兩聲差多少，就知道路上被拖了多久，"),
    c("電離層的效應，可以去掉九成九以上。", None, "P:iono"))
kid("kid-slow-q", K("holding a small phone up and tapping it impatiently with a bored pout", where=CORNER),
    k("那為什麼地圖剛打開，", "抱怨"), k("藍點要等很久才出來？", "章尾停住，句尾上揚", "S:slow"))

# ---------- 第四章：等很久、飄來飄去，還是地圖畫錯？ ----------
chief("chief-almanac", C("holding up two fingers with a calm explaining smile", close=True),
      c("因為光知道距離還不夠，", "接住上一句"),
      c("還要知道衛星現在在哪、它的鐘差多少。"), chapter="剛打開地圖，藍點遲遲不出來")
obj("whistle-bench", "Close-up of " + WHISTLE + " lying on a wooden park bench in warm sunshine, a quiet green lawn behind",
    c("這些寫在衛星的廣播裡，可是它講得很慢，"),
    c("一秒只有五十個位元。"))
kid("kid-bit-q", K("tilting her head with a puzzled face, one finger on her chin", close=True, where=PARK),
    k("位元是什麼？", "句尾上揚"),
    c("資料裡最小的一格，只能是或不是。"),
    c("就像那個朋友報他站在哪裡，一個字一個字慢慢念。"))
chief("chief-36", C("tapping " + WATCH + " on her wrist and waiting patiently with a wry smile"),
      c("一整輪要三十秒，才從頭再講一次；"),
      c("鐘差跟衛星在哪，放在每一輪最前面的三段。"))
kid("kid-36", K("walking briskly in mid-step with a small phone in her hand and a cheeky grin", where=STREET),
    c("傳統的做法要聽完這三段，最久要等大約三十六秒。"),
    k("等那麼久，", "笑"), k("我都走到對街了！"))
chief("chief-starts", C("nodding with an amused smile, one hand open", close=True),
      c("所以開機有分冷、熱。"),
      c("什麼都不知道，叫冷開機，要把整片天空找一遍；"))
chief("chief-canyon", C("holding a small phone up and looking at it with a patient smile"),
      c("手上已經有精確的衛星位置，叫熱開機，不用再等廣播。"),
      c("在大樓中間，訊號斷斷續續，等待還會更久。", None, "P:slow"))
kid("kid-assist-q", K("holding a small phone up proudly with a bright grin", where=CORNER),
    k("可是我的手機，", "不服氣"), k("一打開就有藍點耶！", None, "S:assist"))
obj("cell-tower", "Wide shot of a tall slim grey cell tower with small antennas on a green hill under a bright blue sky, a sunny city of tall glass buildings below",
    c("那多半是輔助 GPS。手機透過行動網路，"),
    c("先拿到衛星的位置和鐘差，"),
    c("只要收幾毫秒的訊號，就能算出位置。", None, "P:assist"))
chief("chief-friend-text", C("holding a small phone up beside her face and pretending to read a message with a cheerful smile"),
      c("就像有人先把每個朋友站在哪，傳訊息給你。"))
kid("kid-cost-q", K("giving a big double thumbs-up with a delighted grin", where=PARK),
    k("那就不用等了！", "開心"), k("有沒有缺點？", "句尾上揚", "S:cost"))
chief("chief-cost", C("raising one hand with an honest careful smile", close=True),
      c("有。你沒有從廣播裡，讀到精確的時間。"),
      c("衛星一直在動，時間錯一點，算出的衛星位置就錯。"))
chief("chief-800", C("spreading her arms wide apart with a serious amazed face"),
      c("一篇導航期刊的論文，引用這個方法發明人的估算："),
      c("時間每差一秒，算出的距離就錯大約八百公尺。"),
    k("又是時間！", "驚訝"))
chief("chief-fifth", C("counting on her fingers with an encouraging smile", close=True),
      c("對。所以有些手機把現在是哪一刻，也當成要算的答案。"),
      c("這是第五個不知道的數，要至少五顆衛星。", None, "P:cost"))
kid("kid-final-q", K("standing still and looking up from a small phone with a thinking face", where=STREET),
    k("所以我的藍點跳到對街，", "推理"), k("到底是怎麼回事？", "章尾停住，句尾上揚"))

# ---------- 收尾 ----------
chief("chief-your-turn", C("leaning forward with an inviting grin, one hand open towards the viewer"),
      c("你剛剛就走在那兩排大樓中間，你說呢？", "笑"), chapter="走到公園，小問想通了")
kid("kid-got-it", K("pointing back towards tall glass buildings in the distance with a big confident grin", where=PARK),
    k("原來如此！", "恍然大悟"), k("訊號撞牆晚到一點點，", "篤定"),
    k("手機就把我算到對街了！", "篤定", "P:jump"))
chief("chief-opinion", C("smiling with her hands clasped, a thoughtful look", close=True),
      c("說得好。還記得那支慢一秒的錶嗎？", "笑"),
      c("我覺得最神奇的是：手機每次定位，都在幫自己對錶。"))
obj("park-arrive", "Wide shot of the sunny entrance of a green city park, a wide grassy lawn and leafy trees, tall plain glass buildings far behind",
    k("公園到了！", "開心"))
# The outro is three pictures, no card, no stamp (series README §3.2, §10.1): the kid gives a thumbs-up.
kid("outro", "Waist-up medium shot of the girl with a big happy smile giving a big cheerful thumbs-up with one hand, bright morning light",
    k("我要跟同學玩哨子遊戲！", "開心大聲"))
chief("outro-chief", "Waist-up medium shot of the chief holding up a small phone with a curious smile, filling the frame, a plain pale wall behind her, bright morning light",
      c("你在哪裡看過藍點亂跳？", "問句上揚，像聊天"), c("留言告訴我們。"))
chief("outro-wave", "Waist-up medium shot of the chief waving goodbye with a warm smile, a plain pale wall behind her, bright morning light",
      c("想一起找生活裡的為什麼，就訂閱原來如此事務所。", "誠懇"))

# ---------- assemble ----------
WHAT = {"main": "手機怎麼用時間，知道我在哪裡", "jump": "藍點為什麼會跳到對街",
        "micro": "差百萬分之一秒，怎麼會差三百公尺", "four": "為什麼至少要四顆衛星",
        "ask": "是不是手機問衛星我在哪", "listen": "手機只用聽的，要聽什麼",
        "travel": "訊號從衛星走到手上要多久", "one": "聽一顆衛星能不能知道我在哪",
        "three": "三顆夠不夠，第四顆要幹嘛", "clock": "手機裡有沒有原子鐘",
        "sky": "天上隨時都有四顆衛星可以聽嗎", "geometry": "同樣四顆衛星，每次都一樣準嗎",
        "signal": "藍點跳走，是不是衛星訊號不準", "echo": "大樓是不是把訊號吃掉了",
        "iono": "天上那段路會不會也走歪", "military": "是不是故意給民眾不準的訊號",
        "relativity": "衛星的錶真的那麼準嗎", "slow": "地圖剛打開，藍點為什麼要等很久",
        "assist": "為什麼我的手機一打開就有藍點", "cost": "不用等的辦法有沒有缺點"}
scenes, loops_s, loops_p, n, beats = [], {}, {}, 0, 0
for sc in S:
    lines = []
    for sp, text, emo, tag in sc["lines"]:
        n += 1; lid = f"p{n:03d}"
        line = {"id": lid, "speaker": sp, "text": text}
        if "GPS" in text:  # spelled out like the lexicon's "GPT": "G P T"; drop once lexicon.json has "GPS"
            line["say"] = text.replace("GPS", "G P S")
            line["say_for"] = hashlib.sha256(unicodedata.normalize("NFC", text).encode("utf-8")).hexdigest()[:12]
        if emo: line["emotion"] = emo
        if tag and tag.startswith("P:") and lines:
            lines[-1]["pause_after_ms"] = BEAT_MS   # 同一景裡答案的前一句（README §10.6）
            beats += 1
        lines.append(line)
        if tag:
            kind, key = tag.split(":")
            (loops_s if kind == "S" else loops_p)[key] = lid
    out = {"id": sc["id"]}
    if sc["chapter"]: out["chapter"] = sc["chapter"]
    out["template"] = sc["template"]; out["data"] = dict(sc["data"]); out["lines"] = lines
    scenes.append(out)
assert set(loops_s) == set(loops_p) == set(WHAT), set(loops_s) ^ set(loops_p) ^ set(WHAT)
assert all(loops_s[key] < loops_p[key] for key in WHAT), [key for key in WHAT if loops_s[key] >= loops_p[key]]
loops = [{"setup": loops_s[key], "payoff": loops_p[key], "what": WHAT[key]} for key in sorted(WHAT, key=lambda key: loops_s[key])]


doc = {
    "schema_version": 1, "slug": SLUG, "format": "drama", "category": "explainer", "narration_locale": "zh-TW",
    "target_minutes": [9, 11], "voice": VOICE, "subtitles": {"burn_in": False}, "theme": "paper", "look": {"preset": "cute-cartoon"},
    # The series tag: the approved character sheets live in the series store and every episode reuses them (docs/videos/SERIES.md).
    "series": {"slug": "sothatswhy", "episode": 13, "chapter": 1},
    # 2026-11-11 (README §9 停頓, §10.6): no fixed pause between lines, a short gap between scenes, beat-timed stills.
    "pauses": {"line_ms": 0, "scene_ms": 150},
    "still_motion": "beat",
    # The series bed from P15 on (explainer-series/README.md, PR #2048): sothatswhy-bed-r2.m4a, remade from P02's paid take.
    "music": {"track": "sothatswhy-bed-r2.m4a", "sha256": "9bb4ba6fd16feb4a7f352144b2d89e9648acbbbbaa2173c27a7eefbdb70f28c6", "gain_db": -20, "duck_db": -10},
    "characters": CHARACTERS, "loops": loops,
    "youtube": {
        "category_id": 27, "made_for_kids": False, "default_language": "zh-TW",
        "title": "GPS 差一點時間，位置怎麼差那麼遠？｜原來如此事務所",
        "description": "小問走路去公園找同學，走在兩排大樓中間，手機地圖上的藍點突然跳到對面那條街，過一下又跳回來。手機到底怎麼用時間，知道你在哪裡？\n\n"
                       "這一集，所長和小問跟著同一段路走，用一個「公園吹哨子」的遊戲來想：聽到哨聲晚了多久，就知道離那個朋友多遠。"
                       "衛星就是帶著原子鐘的朋友，訊號跑得跟光一樣快，所以時間只差百萬分之一秒，距離就差三百公尺，連衛星時鐘那一點相對論的差都一定要先修好；"
                       "手機沒有原子鐘，所以要多聽第四顆衛星，把自己的錶差多少也一起算出來。"
                       "接著看藍點為什麼會偏：衛星送得很準，藍點偏多半是訊號離開衛星以後的事——大樓擋住、牆面反彈、高空的電離層；"
                       "最後是剛開地圖時為什麼要等，以及手機怎麼靠網路省下等待，卻得多找一顆衛星。\n\n"
                       "畫圓圈找交點只是示意，真正的接收機是把位置和時間一起估算出來；插圖由 AI 生成，是示意，不是實際的衛星位置。每個說法的出處列在下方參考資料。\n\n資料截至 " + CHECKED,
        "tags": ["GPS", "衛星定位", "手機地圖", "原子鐘", "多路徑", "電離層", "相對論", "科普", "原來如此事務所"]},
    "thumbnail": {"template": "thumb", "data": {"headline": "藍點\n**跳到對街？**", "sub": "差百萬分之一秒，差三百公尺", "shot": "kid-dot-puzzled", "subject": "right"}},
    "sources": [
        {"title": "GPS.gov, GPS Accuracy (FAQ, current page)", "url": "https://www.gps.gov/node/70", "checked_on": CHECKED},
        {"title": "GPS.gov, Frequently Asked Questions (satellites are one-way beacons)", "url": "https://www.gps.gov/faq", "checked_on": CHECKED},
        {"title": "GPS.gov, Space Segment (about 20,200 km; 24 slots, at least four in view)", "url": "https://www.gps.gov/space-segment", "checked_on": CHECKED},
        {"title": "GPS.gov, Augmentation Systems (what a GPS augmentation is)", "url": "https://www.gps.gov/augmentation-systems", "checked_on": CHECKED},
        {"title": "U.S. DoD, GPS Standard Positioning Service Performance Standard, 5th ed. (April 2020)", "url": "https://archive.gps.gov/technical/ps/2020-SPS-performance-standard.pdf", "checked_on": CHECKED},
        {"title": "FAA, Satellite Navigation - GPS - How It Works", "url": "https://www.faa.gov/about/office_org/headquarters_offices/ato/service_units/techops/navservices/gnss/gps/howitworks", "checked_on": CHECKED},
        {"title": "van Diggelen & Enge (2015), The World's first GPS MOOC and Worldwide Laboratory using Smartphones, ION GNSS+ 2015 (abstract)", "url": "https://www.ion.org/publications/abstract.cfm?articleID=13079", "checked_on": CHECKED},
        {"title": "ESA Navipedia, Code Based Positioning (SPS)", "url": "https://gssc.esa.int/navipedia/index.php/Code_Based_Positioning_(SPS)", "checked_on": CHECKED},
        {"title": "ESA Navipedia, Multipath", "url": "https://gssc.esa.int/navipedia/index.php/Multipath", "checked_on": CHECKED},
        {"title": "ESA Navipedia, Ionospheric Delay", "url": "https://gssc.esa.int/navipedia/index.php/Ionospheric_Delay", "checked_on": CHECKED},
        {"title": "ESA Navipedia, Klobuchar Ionospheric Model", "url": "https://gssc.esa.int/navipedia/index.php/Klobuchar_Ionospheric_Model", "checked_on": CHECKED},
        {"title": "ESA Navipedia, TTFF", "url": "https://gssc.esa.int/navipedia/index.php/TTFF", "checked_on": CHECKED},
        {"title": "Blay, Wang & Akos (2021), Deriving Accurate Time from Assisted GNSS Using Extended Ambiguity Resolution, NAVIGATION 68(1):217", "url": "https://navi.ion.org/content/68/1/217", "checked_on": CHECKED},
        {"title": "Ashby (2003), Relativity in the Global Positioning System, Living Reviews in Relativity 6:1", "url": "https://www.ebi.ac.uk/europepmc/webservices/rest/PMC5253894/fullTextXML", "checked_on": CHECKED},
        {"title": "NOAA National Weather Service, Understanding Lightning: Thunder", "url": "https://www.weather.gov/safety/lightning-science-thunder", "checked_on": CHECKED},
        {"title": "NIST CODATA, speed of light in vacuum", "url": "https://physics.nist.gov/cgi-bin/cuu/Value?c", "checked_on": CHECKED},
    ],
    "assets": [],
    "scenes": scenes,
}
json.dump(doc, open(os.path.join(HERE, "video.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
FROZEN.update({s["id"]: s["data"]["camera"] for s in scenes if s["template"] == "shot" and s["id"] not in FROZEN})
json.dump(FROZEN, open(CAM_FILE, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# ---------- self-checks (the series rules lint does not cover for a sothatswhy- slug) ----------
# 2026-11-11: the faster style speaks about 4.4 characters a second (README §4: P06 measured 4.39), and the
# pauses are now only scene_ms between scenes plus a BEAT_MS beat before each payoff (README §10.6).
RATE = 4.4
def length(t): return sum(1 for ch in t if ch not in "，。、：；！？「」『』（）…—,.!?: ")
def han(t): return sum(1 for ch in t if "一" <= ch <= "鿿")
assert all(s["template"] == "shot" for s in scenes), "this series uses no cards"
assert not any("pause_after_ms" in l and l["pause_after_ms"] != BEAT_MS for s in scenes for l in s["lines"]), "lines carry no pause except the beat"
outro_ids = {"outro", "outro-chief", "outro-wave"}
body = [s for s in scenes if s["id"] not in outro_ids]
chars = sum(length(l["text"]) for s in scenes for l in s["lines"])
body_chars = sum(length(l["text"]) for s in body for l in s["lines"])
body_han = sum(han(l["text"]) for s in body for l in s["lines"])
kidc = sum(length(l["text"]) for s in scenes for l in s["lines"] if l["speaker"] == "kid")
lines_all = [l for s in scenes for l in s["lines"]]
est = chars / RATE + 0.15 * (len(scenes) - 1) + BEAT_MS / 1000 * beats
per_shot = sorted(len(s["lines"]) for s in scenes)
shot_secs = sorted(sum(length(l["text"]) for l in s["lines"]) / RATE for s in scenes)
print(f"scenes {len(scenes)} shots {len(scenes)} lines {n} chars {chars} (body {body_chars}, body Han {body_han}) kid {kidc / chars:.0%} of chars, "
      f"{sum(l['speaker'] == 'kid' for l in lines_all) / n:.0%} of lines; est {est / 60:.1f} min at {RATE}/s "
      f"(+{len(scenes) - 1} scene gaps, {beats} beats, before the 11.9 s intro); loops {len(loops)}; "
      f"median lines a shot {per_shot[len(per_shot) // 2]}, median shot {shot_secs[len(shot_secs) // 2]:.1f} s", file=sys.stderr)
chap_t, chap = {}, None
for s in scenes:
    chap = s.get("chapter", chap)
    chap_t[chap] = chap_t.get(chap, 0) + sum(length(l["text"]) for l in s["lines"]) / RATE + 0.15
for ch, secs in chap_t.items(): print(f"  chapter {ch}: {secs:.0f} s", file=sys.stderr)
for s in scenes:
    secs = sum(length(l["text"]) for l in s["lines"]) / RATE
    if secs > 12: print(f"  shot over 12 s: {s['id']} {secs:.1f}", file=sys.stderr)
for l in lines_all:
    cap = 15 if l["speaker"] == "kid" else 25
    if length(l["text"]) > cap: print(f"  long {l['speaker']} line {l['id']} ({length(l['text'])}): {l['text']}", file=sys.stderr)
# a hook (a question, or a loop being planted) at least every 45 s
hooks, t, last, setups, gaps = [], 0.0, 0.0, set(loops_s.values()), []
for s in body:
    for l in s["lines"]:
        t += length(l["text"]) / RATE
        if l["text"].endswith("？") or l["id"] in setups:
            if t - last > 45: gaps.append(f"{t - last:.0f} s before {l['id']}")
            last = t
for g in gaps: print(f"  hook gap {g}", file=sys.stderr)
assert not gaps, "a stretch longer than 45 s without a question or a planted loop"
assert len(loops) >= 10, "the plan asks for at least 10 loops, every one paid off"
# Upper bound only (owner 2026-11-11: never pad; the 8-minute floor is judged on the honest content, README §9).
assert body_chars <= 3000, f"body {body_chars} characters: keep under 3,000 (plan 10–12 min at 4.4 chars/s)"
cams = [s["data"]["camera"] for s in scenes]
assert all(not (a == b == c_) for a, b, c_ in zip(cams, cams[1:], cams[2:])), "three shots in a row with the same camera"
