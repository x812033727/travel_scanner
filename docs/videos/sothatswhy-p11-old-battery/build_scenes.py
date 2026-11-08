"""Generate video.json for sothatswhy-p11-old-battery (原來如此事務所 對話版 P11).

Run `python3 build_scenes.py` from anywhere: it rewrites video.json next to this file and freezes
every shot's camera move in cameras.json (a shot keeps the camera it was first given, so deleting
a shot never shifts the others: the camera is in the keyframe cache key).
Edit lines and prompts here, never in video.json.
"""
import itertools, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = "sothatswhy-p11-old-battery"
CHECKED = "2026-11-08"

# ---------- series constants ----------
# Both characters' `appearance` stay word for word as in P07/P08/P14/P15: the series sheets are keyed by it
# (series-store.mjs sheetKey), so the approved sheets are reused and nothing is redrawn.
# The owner (2026-11-07): the chief is never described with grey hair. Every chief shot therefore picks the
# shot look `office` (drama.mjs shotCast): the same approved face sheet, an appearance with no grey at all,
# and the prompt tail CHIEFFIX_DESC, which has no grey either.
VOICE = {"provider": "gemini", "name": "Sulafat",
         "style": "標準國語，咬字清楚，台北人平常說話的語調。事務所的所長，溫和、有耐心，像陪一個好奇的小朋友和你一起找答案。語速像平常聊天，一秒四到五個字，句與句之間不拖。"}
SHEET = "character reference: one single full-body figure standing in the centre, facing the viewer in a slight three-quarter turn, relaxed friendly pose, both hands clearly drawn, plain empty cream background with nothing else in the picture, no turnaround, no second view, no seal, no stamp, no signature, no text"
CHIEF_OFFICE = "a friendly slim woman of about thirty, the chief of a small question office, with round black glasses, glossy jet-black shoulder-length hair tied in a low ponytail, a warm smile, a mustard-yellow cardigan over a white blouse, ink-navy trousers, brown shoes, a yellow pencil tucked behind one ear"
CHARACTERS = [
    {"id": "chief", "name": "所長",
     "appearance": "a friendly middle-aged woman, the chief of a small question office, with round black glasses, shoulder-length dark hair with a streak of grey tied in a low ponytail, a warm smile, a mustard-yellow cardigan over a white blouse, ink-navy trousers, brown shoes, a yellow pencil tucked behind one ear",
     "voice": dict(VOICE), "sheet_prompt": SHEET,
     "shot_looks": [{"id": "office", "appearance": CHIEF_OFFICE}]},
    {"id": "kid", "name": "小問",
     "appearance": "a curious eight-year-old girl with a short black bob haircut with straight bangs and one small cowlick sticking up on top, large round eyes, wearing a navy raincoat-style jacket with a mustard-yellow hood, white sneakers, both hands free",
     "voice": {"provider": "gemini", "name": "Leda", "style": "標準國語，咬字清楚，台北人平常說話的語調；八歲小女孩的聲音，好奇、活潑，問問題時句尾上揚，語速輕快"},
     "sheet_prompt": SHEET},
]

# Identity goes LAST in every prompt (P02: putting it first drifted some frames to photo or 3D).
KIDDESC = "the girl has a short black bob with straight bangs and one small cowlick on top and wears a navy raincoat jacket with a mustard-yellow hood"
CHIEFFIX_DESC = "the chief is a slim young woman of about thirty with glossy jet-black hair tied in a low ponytail, round black glasses, a yellow pencil tucked behind her ear, a mustard-yellow cardigan over a white blouse, flat 2D cel-shaded cartoon drawing with ink outlines"
KIDFIX_TAIL = ', exactly matching her reference sheet: the same little girl every time, short black bob with straight bangs, navy raincoat with mustard-yellow hood, long navy trousers, bare loose bob hair hanging free, simple dot-like cartoon eyes as on the reference sheet, a round young child face with big round matching eyes looking the same way, flat 2D cel-shaded cartoon drawing with ink outlines'
WALL = "a plain pale wall behind her"
DAY = "bright daylight"
FLAT = ", simple hand-drawn flat 2D children's cartoon illustration with clean ink outlines and flat colours"
OFFICE = "in a bright sunny little office"
PARK = "in a sunny park on a crisp winter day"
TABLE = "a sunny wooden table"
PHONE = "a plain smooth unmarked phone glowing softly"
BOTTLE = "a plain clear water bottle with a mustard-yellow cap"
# The spout (壺嘴) is drawn as the same bottle's mouth: its cap open to a tiny opening, or off with a wide neck.
NARROW = "a plain clear water bottle with its mustard-yellow cap open to a tiny narrow opening"
WIDE = "a plain clear water bottle with its mustard-yellow cap off and a wide open neck"
# One drawing language for the whole episode (README §10.5: numbers as feelings, one metaphor throughout):
# a battery is a water bottle. The water is the electricity: how full the bottle is now is the percentage; how big
# the bottle still is, is the maximum capacity; how wide its spout is, is how fast it can pour (power delivery).
# Ageing is a white chalky crust (水垢) growing inside: it locks some of what stores the electricity away (the bottle holds less) and narrows the mouth
# (a big gulp cannot come out fast). Nothing is counted, nothing depends on direction, no clock, no gauge, no phone
# face, no battery-level icon: a phone is only ever a plain smooth unmarked phone glowing softly.
# Prompt words that P02/P05 taught us to keep out (README §3.1): the model has no negative prompt,
# lamps and night turn frames into 3D figurines, and these props sprout fake letters.
BANNED = re.compile(r"\b(no|not|without|text|blank|lamp|night|notebook|sign|signs|paper|poster|screen|book|calendar|whiteboard|thermometer|remote|label|magnet|map|chart|grey hair|gray)\b", re.I)

CAMS = itertools.cycle(["push in", "pan left", "pull out", "drift", "tilt up", "pan right", "push in", "tilt down", "pull out", "drift"])
CAM_FILE = os.path.join(HERE, "cameras.json")
FROZEN = json.load(open(CAM_FILE, encoding="utf-8")) if os.path.exists(CAM_FILE) else {}

S = []
EXTRA = {}
# Picture review rounds (README §10.1): REWRITE replaces the prompt of shots with no usable take; FIX appends
# to shots with a severe fault. Both start empty for a new episode.
REWRITE = {}
FIX = {}
for _id, _fix in FIX.items():
    EXTRA[_id] = EXTRA.get(_id, "") + ", " + _fix
def _shot(id, prompt, chars, lines, chapter):
    prompt = prompt + EXTRA.get(id, "")
    assert not BANNED.search(prompt), (id, BANNED.search(prompt).group(0))
    assert id not in {s["id"] for s in S}, id
    cam = FROZEN.get(id) or next(CAMS)
    S.append(dict(id=id, chapter=chapter, template="shot", data=dict(prompt=prompt, camera=cam, visual="still", characters=list(chars)), lines=list(lines)))
def kid(id, prompt, *lines, chapter=None):
    """The kid doing one simple thing, facing the camera, waist-up or head-and-shoulders."""
    prompt = REWRITE.get(id, prompt)
    _shot(id, prompt.rstrip(". ") + ", " + KIDDESC + KIDFIX_TAIL, ["kid"], lines, chapter)
def chief(id, prompt, *lines, chapter=None):
    """The chief, always waist-up or head-and-shoulders, in front of a plain wall in daylight, in her `office` look."""
    prompt = REWRITE.get(id, prompt)
    assert prompt.startswith(("Waist-up", "Head-and-shoulders")), id
    _shot(id, prompt.rstrip(". ") + ", " + CHIEFFIX_DESC, ["chief"], lines, chapter)
    S[-1]["data"]["character_looks"] = {"chief": "office"}
def scene(id, prompt, *lines, chapter=None):
    """No character: an object, a place or a mechanism drawn as a picture."""
    prompt = REWRITE.get(id, prompt)
    _shot(id, prompt + FLAT, [], lines, chapter)
    S[-1]["data"]["nobody"] = True  # PR #2028: no person or face in an object-only shot
def k(t, e=None, tag=None): return ("kid", t, e, tag)
def c(t, e=None, tag=None): return ("chief", t, e, tag)

def C(action, close=False):
    return ("Head-and-shoulders close-up" if close else "Waist-up medium shot") + " of the chief " + action + ", " + WALL + ", " + DAY
def K(action, close=False, where=None):
    return ("Head-and-shoulders close-up" if close else "Waist-up medium shot") + " of the girl " + (where + " " if where else "") + action + ", " + DAY

# ---------- 開場（系列片頭之後直接進場景，不做濃縮；答案都不先講）----------
# One metaphor only: a battery is a water bottle. 百分比 = how full the bottle is now; 最大容量 = how big the bottle
# still is; 壺嘴 (drawn as the bottle's narrow mouth) = how fast it can pour (power delivery). 水垢 = the crust that
# grows inside (SEI in claims.md): it locks away some of what stores the electricity and narrows the mouth.
# Each mapping is defined once and then only used. Round 2 (2026-11-08): verify-1 F01-F08 word for word,
# review-script-score improvements 1-6, blind panel round 1 blocking cuts and notes.
kid("kid-park", K("running in holding " + PHONE + " in both hands with a shocked face, eyes wide", where=OFFICE),
    k("所長！今天好冷喔，", "跑進來報案的語氣", "S:cold"), k("我剛剛在公園拍松鼠，", "比手畫腳"),
    chapter="還有電，手機卻黑掉了")
scene("squirrel", "Close-up of a fluffy squirrel nibbling an acorn on a frosty tree branch in a sunny winter park, " + DAY,
      k("用的是媽媽的舊手機，"), k("一按拍照，它就黑掉了！", "誇張"))
scene("phone-dark", "Close-up of a plain smooth unmarked dark phone lying quiet on a wooden park bench, a few fallen leaves beside it, crisp winter sunshine, " + DAY,
      k("明明還有百分之二十的電！", "委屈"))
kid("kid-mom-said", K("holding " + PHONE + " with a sad little pout", close=True),
    k("媽媽說它剛買的時候，", "委屈"), k("一整天都有電耶！", None, "S:allday"), k("它是不是壞掉了？", "句尾上揚"))
chief("chief-not-broken", C("smiling gently with one hand on her chest", close=True),
      c("先別急。很多舊手機，都可能這樣突然關機。", "安撫"))
kid("kid-why-old", K("tilting her head with a puzzled frown, both hands out of frame", close=True),
    k("為什麼舊的才會這樣？", "句尾上揚"))
chief("chief-old", C("nodding with a knowing smile"),
      c("因為它的電池，已經老了。"))
kid("kid-still-full", K("spreading both hands wide with a confused face", where=OFFICE),
    k("可是電量還有啊，", "不服氣"), k("電池怎麼會老？", "句尾上揚"))
chief("chief-you", C("leaning in a little with a friendly smile", close=True),
      c("很多人都跟你一樣，以為電量還多，電池就還好。", "轉向觀眾"))
scene("phone-tease", "Close-up of a plain smooth unmarked dark phone lying quiet on " + TABLE + ", soft warm light around it, " + DAY,
      c("其實手機突然黑掉，有一個你想不到的原因。", "賣關子", "S:onpurpose"), c("而且電池裡面，正偷偷長著一層東西。", "賣關子", "S:skin"))
kid("kid-tease", K("gasping with a round open mouth, both hands out of frame", close=True),
    k("想不到的原因？還會長東西？", "驚訝"))
scene("battery-open", "Close-up of a plain smooth rounded battery cell lying on " + TABLE + ", soft warm light, " + DAY,
      c("聽起來很怪吧？我們走進這顆老電池裡看看。", "承諾"))
chief("chief-main-q", C("folding her hands with a curious smile, eyebrows raised"),
      c("電量明明還有，電池為什麼會老，"), c("還會突然關機？", "問句", "S:main"))

# ---------- 第一章：百分之百，只是這個壺裝滿了 ----------
scene("bottle", "Close-up of " + BOTTLE + " half full of water on " + TABLE + ", sunlight shining through it, " + DAY,
      c("要回答它，先想想你每天帶的水壺。", "接住上一句"), c("電池就像一個裝電的水壺。"), chapter="百分之百，只是這個壺裝滿了")
kid("kid-bottle", K("holding " + BOTTLE + " in both hands with a curious face", where=OFFICE),
    k("我的水壺？", "好奇"), k("電也能裝在壺裡？", "句尾上揚"))
scene("bottle-level", "Close-up of " + BOTTLE + " with only a little water remaining in it, on " + TABLE + ", " + DAY,
      c("我們就這樣想：電是壺裡的水。"), c("螢幕上的百分比，是水壺現在還剩幾分滿。"))
kid("kid-twenty", K("with a small worried face, both hands out of frame", close=True),
    k("那我的手機，", "想一想"), k("就是只剩一點點水？", "句尾上揚"))
scene("bottle-fill", "Close-up of " + BOTTLE + " being filled at a kitchen tap with fresh sparkling water, sunny kitchen, " + DAY,
      c("對。用電，就是喝掉壺裡的水；"), c("充電，就是再把壺裝滿。"))
kid("kid-hundred", K("centred in the frame, large clear face, holding " + BOTTLE + " in front of her chest with both hands and a confident proud grin", close=True),
    k("那充到百分之百，", "很有把握的錯猜"), k("就跟新手機一樣多電吧？", "句尾上揚", "S:hundred"))
chief("chief-hundred", C("shaking her head kindly with a warm smile"),
      c("不一定。百分之百，只是這個壺裝滿了。"), c("壺有多大，百分比可不會告訴你。"))
scene("two-bottles", "Close-up of two plain clear water bottles with mustard-yellow caps side by side, a big one and a much smaller one, both full of water, on " + TABLE + ", " + DAY,
      c("舊電池的壺，比新的時候小了。"), c("一樣裝滿，裡面的水就是比較少。", None, "P:hundred"))
kid("kid-short", K("nodding hard with a bright face of understanding", where=OFFICE),
    k("難怪舊手機充滿了，", "恍然"), k("也撐不了一整天！", "恍然", "P:allday"))
chief("chief-settings", C("raising one finger with a friendly smile", close=True),
      c("你可以請大人打開手機的設定找找看。", "轉向觀眾"))
scene("phone-bottle", "Close-up of " + PHONE + " lying on " + TABLE + " beside " + BOTTLE + ", " + DAY,
      c("很多手機有一項「最大容量」或「電池健康度」，"), c("說的就是這個壺，現在還剩多大。"))
kid("kid-tell-mom", K("pumping one fist with an eager grin", where=OFFICE),
    k("我回家要叫媽媽找！", "躍躍欲試"), k("可是手機怎麼知道壺多大？", "句尾上揚"))
scene("phone-glow", "Close-up of " + PHONE + " resting on " + TABLE + ", a soft warm halo around it, " + DAY,
      c("它是跟全新的時候比，自己估出來的，"), c("所以不一定很準。"))
kid("kid-pct-est", K("tilting her head with a thoughtful pout, both hands out of frame", close=True),
    k("那百分比也是估的嗎？", "句尾上揚"))
scene("pour-glass", "Close-up of " + BOTTLE + " pouring a steady stream of water into a glass, " + DAY,
      c("對。手機一邊看壺裡的水倒起來多有力，"), c("一邊數倒出去多少，大約算出來。"))
kid("kid-shrink-q", K("hugging " + BOTTLE + " with a worried face", where=OFFICE),
    k("可是壺怎麼會，", "不解"), k("自己變小呢？", "句尾上揚", "S:shrink"))

# ---------- 第二章：電池裡長出一層水垢 ----------
scene("kettle", "Close-up looking into a plain metal kettle, its inside walls coated with a thick chalky white crust, sunny kitchen, " + DAY,
      c("因為壺裡面，會慢慢長出一層水垢。", "接住上一句", "P:skin"), chapter="電池裡長出一層水垢")
scene("kettle-crust", "Close-up of a thick chalky white crust on the inside of an old plain metal kettle, sunny kitchen, " + DAY,
      c("就像家裡的熱水壺，用久了，裡面會黏上一層白白硬硬的東西，", "轉向觀眾"), c("那就是水垢。"))
kid("kid-battery-scale", K("gasping with a surprised round mouth, both hands out of frame", close=True),
    k("電池裡也有水垢？", "句尾上揚"))
scene("battery-layer", "A simple flat illustration of " + BOTTLE + " with a thin soft white film lining its inside walls, on " + TABLE + ", " + DAY,
      c("不是真的水垢，是很像水垢的一層薄膜。"), c("電池用得越久，它就慢慢長得越厚。"))
kid("kid-only-scale", K("tilting her head with a curious squint, both hands out of frame", close=True),
    k("電池變老，", "好奇"), k("只是因為水垢嗎？", "句尾上揚"))
chief("chief-many-causes", C("holding one hand open with a thoughtful smile"),
      c("還有別的。科學家找到好幾種讓電池變老的原因，"), c("水垢是常被提到的主要原因之一。"))
scene("bottle-crust", "Close-up of " + BOTTLE + " with a thick white crust lining its inside walls, holding only a little water, " + DAY,
      c("水垢會把一些本來能幫忙裝電的小東西，卡在裡面。"), c("長得越厚，壺能裝的電就越少。", None, "P:shrink"))
kid("kid-brush", K("with a clever confident grin, both hands out of frame", where=OFFICE),
    k("那把水垢刷掉，", "很有把握的錯猜"), k("不就好了？", "句尾上揚", "S:brush"))
chief("chief-brush", C("shaking her head with a gentle smile", close=True),
      c("刷不到。它長在電池最裡面，", None, "P:brush"), c("而且長了，就退不掉。"))
kid("kid-cycle-q", K("with a thinking face, both hands out of frame", where=OFFICE),
    k("充一次電，", "推理"), k("就長一次水垢嗎？", "句尾上揚", "S:cycle"))
chief("chief-cycle", C("holding one hand flat with a thoughtful smile"),
      c("差不多。不過手機算的是「一次循環」。"))
scene("half-bottle", "Close-up of " + BOTTLE + " half full on a sunny school desk, " + DAY,
      c("一次循環，就是喝掉一整壺的量。今天喝半壺，"), c("明天再喝半壺，加起來一整壺，才算一次。", None, "P:cycle"))
kid("kid-many", K("spreading both arms wide with a curious face", where=OFFICE),
    k("那喝很多很多次以後呢？", "句尾上揚"))
scene("bottle-shrunk", "Close-up of two plain clear water bottles with mustard-yellow caps side by side, one a little smaller than the other, both full of water, on " + TABLE + ", " + DAY,
      c("有一家手機公司說，它較新的一批手機電池，"), c("在很理想的情況下，"))
scene("bottle-eighty", "Close-up of " + BOTTLE + " with a thin white crust inside, still mostly full of sparkling water, on " + TABLE + ", " + DAY,
      c("設計成大約一千次循環後，壺還有原來的大約八成大。"))
kid("kid-thousand", K("gasping with a wide surprised face, both hands out of frame", close=True),
    k("那麼多次，", "驚訝"), k("要用好幾年吧？", "句尾上揚"))
scene("shelf-bottles", "A long sunny shelf lined with many plain clear water bottles with mustard-yellow caps, " + DAY,
      c("我們自己粗算：如果每天剛好用掉一整壺，"), c("那大約是將近三年。"))
kid("kid-two-tenths", K("throwing both fists in the air with an excited grin", where=OFFICE),
    k("那麼久，", "驚喜"), k("才少了大約兩成！", "開心"))
chief("chief-ideal", C("tilting her head with a gentle smile", close=True),
      c("那是很理想的情況。真的用起來，", "轉向觀眾"), c("要看你怎麼用、放在哪裡。"))
kid("kid-idle", K("crossing her arms with a clever confident grin", where=OFFICE),
    k("那我都不充電，", "很有把握的錯猜"), k("就不會長水垢了吧？", "句尾上揚", "S:idle"))
chief("chief-idle", C("shaking her head gently with a kind smile"),
      c("不是喔。就算收在抽屜裡不用，水垢也會慢慢長。", None, "P:idle"))
scene("hot-car", "Close-up of " + PHONE + " lying on a sunny car seat in strong summer sunshine, wavy heat lines shimmering, " + DAY,
      c("尤其放在很熱的地方，水垢長得特別快，"), c("像夏天停在大太陽底下的車子裡。"))
kid("kid-hot-q", K("with a hot sweaty face and pink cheeks, both hands out of frame", close=True),
    k("要多熱，才算太熱？", "句尾上揚", "S:hot"))
chief("chief-35", C("raising one finger with a serious kind face", close=True),
      c("手機公司說，大約超過三十五度，就太熱了。", None, "P:hot"))
kid("kid-freezer", K("standing with both hands on her hips and a clever grin", where=OFFICE),
    k("那我放進冷凍庫，", "很有把握的錯猜"), k("它就不會老了吧？", "句尾上揚", "S:freezer"))
chief("chief-freezer", C("raising both eyebrows with a startled little laugh", close=True),
      c("不要喔！冰起來也還是會老。", "笑", "P:freezer"), c("手機公司說，用的時候最好在大約零度以上。"))
kid("kid-blackout-q", K("frowning with a puzzled face, both hands out of frame", close=True),
    k("可是壺變小，只是比較快沒電，", "不解"), k("怎麼會一下子黑掉？", "句尾上揚", "S:blackout"))

# ---------- 第三章：壺嘴變窄，大口倒不出來 ----------
scene("spout", "Close-up of " + NARROW + ", tipped over a glass, only a thin trickle of water coming out, " + DAY,
      c("因為水垢不只讓壺變小，也會把壺嘴慢慢堵窄。", "接住上一句"), chapter="壺嘴變窄，大口倒不出來")
scene("wide-spout", "Close-up of " + WIDE + ", tipped over a glass, a thick fast stream of water pouring out, " + DAY,
      c("壺嘴就是倒水的地方，它寬不寬，決定水一次能倒多快。"), c("手機用電，就是從壺嘴把水倒出來。"))
chief("chief-spout-you", C("holding a plain clear water bottle with a playful smile", close=True),
      c("你想想，用很窄的壺嘴倒一大杯水，", "轉向觀眾"), c("是不是要等好久？"))
kid("kid-sip", K("with a calm little smile, both hands out of frame", where=OFFICE),
    k("對耶！那小口小口喝，", "推理"), k("窄一點也沒關係？", "句尾上揚"))
scene("trickle-cup", "Close-up of " + NARROW + " slowly filling a small cup with a thin steady trickle, " + DAY,
      c("對，平常慢慢用電，窄窄的壺嘴也來得及。"))
kid("kid-gulp-q", K("tilting her head with a curious face, both hands out of frame", close=True),
    k("那什麼時候，", "好奇"), k("要一下子大口喝？", "句尾上揚"))
scene("phone-busy", "Close-up of a plain smooth unmarked phone glowing brightly with little sparkles around it on " + TABLE + ", " + DAY,
      c("像開相機拍照、玩很忙的遊戲，"), c("手機一下子就要很多電。"))
kid("kid-gulp-what", K("holding " + PHONE + " with a worried face", where=OFFICE),
    k("壺嘴太窄，倒不出來，", "擔心"), k("會怎麼樣？", "句尾上揚"))
scene("cup-short", "Close-up of a big empty glass beside " + NARROW + " that only drips thin drops into it, " + DAY,
      c("手機裡的零件，一下子拿不到夠多的電，"), c("就沒辦法好好工作。"))
kid("kid-broken-q", K("biting her lip with a worried little frown", close=True),
    k("所以它就壞掉了？", "句尾上揚"))
chief("chief-protect", C("shaking her head with a calm reassuring smile"),
      c("不是。手機會搶先一步，自己關機，", None, "P:blackout"), c("保護裡面的零件。", None, "P:onpurpose"))
kid("kid-decided", K("with a bright face of sudden discovery, eyes wide and mouth open", close=True),
    k("原來這就是想不到的原因！", "恍然"))
scene("phone-rest-safe", "Close-up of a plain smooth unmarked dark phone resting safely on a soft round cushion, " + DAY,
      c("對，所以它多半沒有壞。"))
kid("kid-liar-q", K("crossing her arms with a doubtful pout", where=OFFICE),
    k("可是我的手機明明有電，", "不服氣"), k("百分比是不是騙人？", "句尾上揚", "S:liar"))
chief("chief-liar", C("raising her eyebrows with a gentle smile", close=True),
      c("還記得百分比是估的嗎？它不一定很準。", "點名回呼"))
scene("bottle-left", "Close-up of " + NARROW + " with a little water still inside, tipped over a glass, only a thin trickle coming out, " + DAY,
      c("可是它沒騙人，壺裡多半真的還有水，", None, "P:liar"), c("只是壺嘴太窄，大口倒不出來。", None, "P:main"))
kid("kid-three", K("with a bright face of sudden discovery, both hands out of frame", where=OFFICE),
    k("壺裡的水、壺有多大，", "恍然"), k("還有壺嘴多寬，是三件事！", "恍然"))
chief("chief-three", C("nodding firmly with a proud smile", close=True),
      c("對！一點都沒錯。", "轉向觀眾"))
kid("kid-full-q", K("squinting in thought with a curious face, both hands out of frame", close=True),
    k("那電多的時候，", "推理"), k("怎麼就不會黑掉？", "句尾上揚"))
scene("full-pour", "Close-up of " + WIDE + ", full to the brim and tipped over a glass, a strong steady stream pouring out, " + DAY,
      c("壺裡水多，倒起來比較有力；"), c("可是水一少，再碰上窄壺嘴，就容易倒不夠。"))
kid("kid-cold-q", K("hugging herself with a shivering face and pink cheeks", where=OFFICE),
    k("那今天那麼冷，", "想起來"), k("也有關係嗎？", "句尾上揚"))
scene("cold-bench", "A plain smooth unmarked phone on a frosty wooden park bench on a crisp clear winter morning, a little frost on the slats, " + DAY,
      c("有。天氣冷，壺嘴也會暫時變窄一點，", None, "P:cold"), c("回到暖和的地方，就會好一些。"))
kid("kid-care-q", K("clenching both fists with a determined face", where=OFFICE),
    k("那公園那麼冷……", "若有所思"), k("我好像快想通了！先不說，", "眼睛一亮"),
    k("我想先知道，要怎麼做，", "認真"), k("才能讓電池老得慢一點？", "句尾上揚", "S:care"))

# ---------- 第四章：手機先停在八成 ----------
# Panel round 1: every care point ties back to 水垢 or the spout, and one forward hook (mom's phone) is planted.
chief("chief-good-news", C("smiling brightly with a friendly face", close=True),
      c("好消息是，很多事手機已經在幫你做了。", "接住上一句"), c("媽媽那支舊手機，等一下也有辦法。", "轉向觀眾", "S:fix"), chapter="手機先停在八成")
kid("kid-help-q", K("blinking with a surprised curious face, both hands out of frame", close=True),
    k("手機會幫我？幫什麼？", "句尾上揚"))
scene("brim-bottle", "Close-up of " + BOTTLE + " filled to the brim with water, standing in warm sunshine on " + TABLE + ", " + DAY,
      c("電池也不喜歡一直裝得滿滿的，放很久，"), c("那樣水垢也長得比較快。"))
scene("bedside", PHONE[0].upper() + PHONE[1:] + " on a bedside table beside " + BOTTLE + " filled most of the way, early morning sunshine through the curtains, " + DAY,
      c("所以很多手機會學你的習慣：", "轉向觀眾"), c("先充到大約八成，停一下，"), c("快起床時，再把它充滿。", None, "P:care"))
kid("kid-wake-q", K("gasping with a delighted surprised face, both hands out of frame", close=True),
    k("它知道我幾點起床？", "驚訝"))
chief("chief-learn", C("nodding with a playful smile"),
      c("它會慢慢記住，你平常什麼時候拔掉充電線。"), c("有的手機公司說，大約要學兩個禮拜。"))
kid("kid-unplug-q", K("squinting with a determined little face, both hands out of frame", close=True),
    k("那我要不要自己盯著，", "認真"), k("到八成就拔掉？", "句尾上揚"))
scene("phone-rest", PHONE[0].upper() + PHONE[1:] + " resting calmly on its charger on " + TABLE + ", " + DAY,
      c("不用那麼辛苦，交給手機就好。"), c("有些手機也能設定，最多只充到八成。"))
kid("kid-zero-q", K("standing with both hands on her hips and a confident grin", where=OFFICE),
    k("那我要用到完全沒電，", "很有把握的錯猜"), k("才可以充電，對吧？", "句尾上揚", "S:zero"))
chief("chief-zero", C("shaking her head kindly with a warm smile"),
      c("不用。現在的手機電池，想充就充，", None, "P:zero"), c("也不用特地先用光再充滿。"))
kid("kid-hotcharge-q", K("holding " + PHONE + " with a puzzled face", close=True),
    k("充電時它熱熱的，", "好奇"), k("要怎麼辦？", "句尾上揚"))
scene("case-off", "A plain smooth unmarked phone lying beside its soft plain silicone case on a cool wooden table in the shade, " + DAY,
      c("還記得熱會讓水垢長得快嗎？", "點名回呼"), c("所以充電時，先把手機殼拿掉，也別在大太陽底下充。"))
kid("kid-fix-q", K("hugging a plain smooth unmarked phone close with a sad hopeful face", where=OFFICE),
    k("那媽媽那支舊手機，", "心疼"), k("有什麼辦法？", "句尾上揚"))
scene("crust-stays", "Close-up of a small plain clear water bottle with a mustard-yellow cap and a thick white crust inside, on " + TABLE + ", " + DAY,
      c("還記得水垢退不掉嗎？", "點名回呼"), c("所以壺也變不回原來那麼大。"))
chief("chief-replace", C("nodding with a warm kind smile", close=True),
      c("真的太舊了，可以請大人帶去，", "轉向觀眾"), c("讓專業的人換一顆新電池。", None, "P:fix"))
scene("swollen", "Close-up of a plain smooth unmarked phone with its back slightly puffed, lying on a wooden table, " + DAY,
      c("要是它鼓鼓的、很燙，就別用也別充，馬上告訴大人。", "認真"))
kid("kid-case-q", K("holding a plain smooth unmarked phone with a serious little face", where=OFFICE),
    k("那我剛剛在公園，", "認真"), k("手機到底發生什麼事？", "句尾上揚"))

# ---------- 收尾 ----------
chief("chief-back", C("smiling warmly at the viewer with one hand open, filling the frame", close=True),
      c("其實你已經知道了。你自己說說看。", "笑"), chapter="小問自己破案")
kid("kid-got1", K("pointing proudly with one finger and a big grin", close=True),
    k("我一按拍照，要大口喝電，", "篤定"), k("舊壺嘴太窄，天氣又冷，", "篤定"))
kid("kid-got2", K("throwing both arms wide with a huge happy smile", where=OFFICE),
    k("手機就先關機，保護自己！", "開心"))
chief("chief-done", C("smiling warmly at the viewer with her hands clasped", close=True),
      c("對，就是這樣！下次冷天手機突然黑掉，", "轉向觀眾，輕聲"), c("先別怪它，帶回暖和的地方，再開機試試。"))
# The outro is three pictures, no card, no stamp (series README §3.2, §10.1): the kid gives a thumbs-up.
kid("outro", "Head-and-shoulders close-up of the girl with a big happy smile giving a big cheerful thumbs-up with one hand, bright morning light",
    k("原來如此！", "開心大聲"))
chief("outro-chief", "Waist-up medium shot of the chief tilting her head with a curious smile and one hand open, filling the frame, a plain pale wall behind her, bright morning light",
      c("看影片的你呢？你的手機有沒有突然黑掉過？", "問句上揚，像聊天"), c("留言告訴我們。"))
chief("outro-wave", "Waist-up medium shot of the chief waving goodbye with a warm smile, a plain pale wall behind her, bright morning light",
      c("想一起找生活裡的為什麼，就訂閱原來如此事務所。", "誠懇"))

# ---------- assemble ----------
WHAT = {"main": "電量明明還有，電池為什麼會老，還會突然關機", "cold": "那天很冷，跟手機黑掉有沒有關係",
        "onpurpose": "那一下黑掉，你想不到的原因是什麼", "skin": "電池裡偷偷長著的那一層是什麼",
        "allday": "媽媽說剛買時一整天都有電，現在為什麼撐不久",
        "hundred": "充到百分之百是不是跟新手機一樣多電", "shrink": "壺怎麼會自己變小",
        "brush": "把水垢刷掉不就好了", "cycle": "是不是充一次電就長一次水垢", "idle": "不充電是不是就不會老",
        "hot": "多熱才算太熱", "freezer": "放冷凍庫是不是就不會老",
        "blackout": "壺變小只是比較快沒電，怎麼會一下子黑掉",
        "liar": "還有電卻黑掉，百分比是不是騙人", "care": "怎麼讓電池老得慢一點",
        "zero": "是不是要用到沒電才可以充", "fix": "媽媽那支舊手機有什麼辦法"}
scenes, loops_s, loops_p, n = [], {}, {}, 0
for sc in S:
    lines = []
    for sp, text, emo, tag in sc["lines"]:
        n += 1; lid = f"p{n:03d}"
        line = {"id": lid, "speaker": sp, "text": text, "pause_after_ms": 100}
        if emo: line["emotion"] = emo
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
    "target_minutes": [10, 12], "voice": VOICE, "subtitles": {"burn_in": False}, "theme": "paper", "look": {"preset": "cute-cartoon"},
    # The series tag: the approved character sheets live in the series store and every episode reuses them (docs/videos/SERIES.md).
    "series": {"slug": "sothatswhy", "episode": 11, "chapter": 1},
    # The series bed: the same paid Lyria take as P02-P14 (P02 backup music/e4225993d121c03b.mp3), rebuilt on
    # 2026-11-07 with P02's recipe because the original bed file was in no backup (tail cut at 175.15 s,
    # five copies with 3 s crossfades, 863.75 s). Nothing new was generated.
    "music": {"track": "sothatswhy-bed-r2.m4a", "sha256": "9bb4ba6fd16feb4a7f352144b2d89e9648acbbbbaa2173c27a7eefbdb70f28c6", "gain_db": -20, "duck_db": -10},
    "characters": CHARACTERS, "loops": loops,
    "youtube": {
        "category_id": 27, "made_for_kids": False, "default_language": "zh-TW",
        "title": "電量還有，手機電池為什麼已經老了？｜原來如此事務所",
        "description": "小問在公園用媽媽的舊手機拍松鼠，明明還有百分之二十的電，一按拍照就黑掉了。手機壞了嗎？電量還有，電池怎麼會老？\n\n"
                       "這一集，所長和小問把電池想成一個裝電的水壺：百分比是壺裡現在還剩幾分滿，「最大容量」是壺本身還剩多大，"
                       "壺嘴寬不寬決定電一次能倒多快。電池裡慢慢長出一層像水垢的薄膜，讓壺變小、也讓壺嘴變窄；"
                       "手機要大口用電時倒不夠快，就會自己先關機、保護裡面的零件。\n\n"
                       "也聊到手機怎麼自己照顧電池、充電時可以想充就充，以及電池鼓起來或很燙時，要停用並告訴大人。\n\n"
                       "水壺與水垢是我們的比喻，不是電池真正的構造；本集插圖由 AI 生成，畫的是示意。片中的數字大多是手機公司說明裡的大約數字，「將近三年」是我們自己粗算，"
                       "每支手機、每顆電池都不一樣。每個說法的出處列在下方參考資料。\n\n資料截至 " + CHECKED,
        "tags": ["手機電池", "電池健康度", "最大容量", "鋰電池", "突然關機", "充電", "科普", "原來如此事務所"],
        "video_id": None},
    "thumbnail": {"template": "thumb", "data": {"headline": "電量還有\n**電池已經老了**", "sub": "還有百分之二十，手機卻黑掉", "shot": "kid-hundred", "subject": "right"}},
    "sources": [
        {"title": "Apple：iPhone 電池與效能", "url": "https://support.apple.com/en-us/101575", "checked_on": CHECKED},
        {"title": "Apple：iPhone 11 及後續機型的電池與效能", "url": "https://support.apple.com/en-us/106348", "checked_on": CHECKED},
        {"title": "Apple：iPhone 的最佳化電池充電", "url": "https://support.apple.com/en-us/108055", "checked_on": CHECKED},
        {"title": "Apple：關於 iPhone 電池", "url": "https://support.apple.com/en-us/118431", "checked_on": CHECKED},
        {"title": "Apple：Why lithium-ion", "url": "https://www.apple.com/batteries/why-lithium-ion/", "checked_on": CHECKED},
        {"title": "Apple：Maximizing performance", "url": "https://www.apple.com/batteries/maximizing-performance/", "checked_on": CHECKED},
        {"title": "Apple：iPhone 重要安全資訊", "url": "https://support.apple.com/guide/iphone/important-safety-information-iph301fc905/ios", "checked_on": CHECKED},
        {"title": "Google：Understand your Pixel battery", "url": "https://support.google.com/pixelphone/answer/15738128?hl=en", "checked_on": CHECKED},
        {"title": "Google：Get the most life from your Pixel battery", "url": "https://support.google.com/pixelphone/answer/6090612?hl=en", "checked_on": CHECKED},
        {"title": "Samsung：Battery protection in One UI 6.1", "url": "https://www.samsung.com/ie/support/mobile-devices/galaxy-battery-protection-feature-in-one-ui-6-1/", "checked_on": CHECKED},
        {"title": "Battery University：BU-808 How to prolong lithium-based batteries", "url": "https://batteryuniversity.com/article/bu-808-how-to-prolong-lithium-based-batteries", "checked_on": CHECKED},
        {"title": "Battery University：BU-808b What causes Li-ion to die", "url": "https://batteryuniversity.com/article/bu-808b-what-causes-li-ion-to-die", "checked_on": CHECKED},
        {"title": "Battery University：BU-903 How to measure state-of-charge", "url": "https://batteryuniversity.com/article/bu-903-how-to-measure-state-of-charge", "checked_on": CHECKED},
        {"title": "University of Münster MEET：Battery Aging", "url": "https://www.uni-muenster.de/MEET/en/research/cell-system/Aging.html", "checked_on": CHECKED},
        {"title": "Edge et al. 2021, Lithium ion battery degradation: what you need to know (PCCP)", "url": "https://doi.org/10.1039/D1CP00359C", "checked_on": CHECKED},
        {"title": "Google：Extended Repair Program for Pixel 7a", "url": "https://support.google.com/pixelphone/answer/16043453", "checked_on": CHECKED},
    ],
    "assets": [],
    "scenes": scenes,
}
json.dump(doc, open(os.path.join(HERE, "video.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
FROZEN.update({s["id"]: s["data"]["camera"] for s in scenes if s["template"] == "shot" and s["id"] not in FROZEN})
json.dump(FROZEN, open(CAM_FILE, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# ---------- self-checks (the series rules lint does not cover for a sothatswhy- slug) ----------
# Measured on P05/P14: the two Gemini voices speak about 3.2 characters a second (P14: 2,930 chars -> 15.2 min).
RATE = 3.2
def length(t): return sum(1 for ch in t if ch not in "，。、：；！？「」『』（）…—,.!?: ")
assert all(s["template"] == "shot" for s in scenes), "this series uses no cards"
assert all(not re.search(r"grey (hair|streak)|streak of grey|silver", s["data"]["prompt"]) for s in scenes), "the chief is never described with grey hair"
assert all(not re.search(r"\b(left|right|ahead|behind|toward|towards)\b", s["data"]["prompt"].replace(WALL, "").replace("behind her ear", "")) for s in scenes), "no direction words in prompts"
outro_ids = {"outro", "outro-chief", "outro-wave"}
body = [s for s in scenes if s["id"] not in outro_ids]
chars = sum(length(l["text"]) for s in scenes for l in s["lines"])
body_chars = sum(length(l["text"]) for s in body for l in s["lines"])
kidc = sum(length(l["text"]) for s in scenes for l in s["lines"] if l["speaker"] == "kid")
lines_all = [l for s in scenes for l in s["lines"]]
print(f"scenes {len(scenes)} shots {len(scenes)} lines {n} chars {chars} (body {body_chars}) kid {kidc / chars:.0%} of chars, "
      f"{sum(l['speaker'] == 'kid' for l in lines_all) / n:.0%} of lines; est {chars / RATE / 60:.1f} min at {RATE}/s; loops {len(loops)}; "
      f"chief shots {sum(s['data']['characters'] == ['chief'] for s in scenes)}, kid shots {sum(s['data']['characters'] == ['kid'] for s in scenes)}", file=sys.stderr)
for s in scenes:
    secs = sum(length(l["text"]) for l in s["lines"]) / RATE
    if secs > 12: print(f"  shot over 12 s: {s['id']} {secs:.1f}", file=sys.stderr)
for l in lines_all:
    cap = 15 if l["speaker"] == "kid" else 25
    if length(l["text"]) > cap: print(f"  long {l['speaker']} line {l['id']} ({length(l['text'])}): {l['text']}", file=sys.stderr)
# a hook (a question, or a loop being planted) at least every 45 s
hooks, t, last, setups = [], 0.0, 0.0, set(loops_s.values())
for s in body:
    for l in s["lines"]:
        t += length(l["text"]) / RATE
        if l["text"].endswith("？") or l["id"] in setups:
            if t - last > 45: print(f"  hook gap {t - last:.0f} s before {l['id']}", file=sys.stderr)
            last = t
cams = [s["data"]["camera"] for s in scenes]
assert all(not (a == b == c_) for a, b, c_ in zip(cams, cams[1:], cams[2:])), "three shots in a row with the same camera"
