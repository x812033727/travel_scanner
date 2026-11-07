"""Generate video.json for sothatswhy-p08-popcorn-pressure (原來如此事務所 對話版 P08).

Run `python3 build_scenes.py` from anywhere: it rewrites video.json next to this file and freezes
every shot's camera move in cameras.json (a shot keeps the camera it was first given, so deleting
a shot never shifts the others: the camera is in the keyframe cache key).
Edit lines and prompts here, never in video.json.
"""
import itertools, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = "sothatswhy-p08-popcorn-pressure"
CHECKED = "2026-11-07"

# ---------- series constants ----------
# Both characters are identical to P07/P14 (approved series sheets reused through the `series` tag):
# the chief as in P02/P05/P14, the kid in her notebook-free look (series README §3.2).
VOICE = {"provider": "gemini", "name": "Sulafat",
         "style": "標準國語，咬字清楚，台北人平常說話的語調。事務所的所長，溫和、有耐心，像陪一個好奇的小朋友和你一起找答案。語速像平常聊天，一秒四到五個字，句與句之間不拖。"}
SHEET = "character reference: one single full-body figure standing in the centre, facing the viewer in a slight three-quarter turn, relaxed friendly pose, both hands clearly drawn, plain empty cream background with nothing else in the picture, no turnaround, no second view, no seal, no stamp, no signature, no text"
CHARACTERS = [
    {"id": "chief", "name": "所長",
     "appearance": "a friendly middle-aged woman, the chief of a small question office, with round black glasses, shoulder-length dark hair with a streak of grey tied in a low ponytail, a warm smile, a mustard-yellow cardigan over a white blouse, ink-navy trousers, brown shoes, a yellow pencil tucked behind one ear",
     "voice": dict(VOICE), "sheet_prompt": SHEET},
    {"id": "kid", "name": "小問",
     "appearance": "a curious eight-year-old girl with a short black bob haircut with straight bangs and one small cowlick sticking up on top, large round eyes, wearing a navy raincoat-style jacket with a mustard-yellow hood, white sneakers, both hands free",
     "voice": {"provider": "gemini", "name": "Leda", "style": "標準國語，咬字清楚，台北人平常說話的語調；八歲小女孩的聲音，好奇、活潑，問問題時句尾上揚，語速輕快"},
     "sheet_prompt": SHEET},
]


# Identity goes LAST in every prompt (P02: putting it first drifted some frames to photo or 3D).
KIDDESC = "the girl has a short black bob with straight bangs and one small cowlick on top and wears a navy raincoat jacket with a mustard-yellow hood"
CHIEFDESC = "the chief wears round black glasses, her dark hair with a grey streak is tied in a low ponytail, a yellow pencil is tucked behind her ear, mustard-yellow cardigan"
WALL = "a plain pale wall behind her"
DAY = "bright daylight"
KITCHEN = "in a bright sunny home kitchen"
CAMP = "at a sunny grassy mountain campsite with green peaks behind her"
POT = "a small plain steel camping pot"
STOVE = "a small plain camping gas stove"
PAN = "a plain round steel pan"
# One drawing language for the whole episode (README §10.5: numbers as feelings, one metaphor throughout):
# the air pressing on the water is a soft quilt of fluffy white air, thick by the sea and thin on the mountain;
# the steam inside a kernel is a tight puffed-up balloon feeling. Nothing is counted, nothing depends on direction.
KERNEL = "one big shiny golden-yellow popcorn kernel with a smooth hard shell, drawn as a flat 2D cartoon object"
# Prompt words that P02/P05 taught us to keep out (README §3.1): the model has no negative prompt,
# lamps and night turn frames into 3D figurines, and these props sprout fake letters.
BANNED = re.compile(r"\b(no|not|without|text|blank|lamp|night|notebook|sign|signs|paper|poster|screen|book|calendar|whiteboard|thermometer|remote|label|magnet)\b", re.I)

CAMS = itertools.cycle(["push in", "pan left", "pull out", "drift", "tilt up", "pan right", "push in", "tilt down", "pull out", "drift"])
CAM_FILE = os.path.join(HERE, "cameras.json")
FROZEN = json.load(open(CAM_FILE, encoding="utf-8")) if os.path.exists(CAM_FILE) else {}

S = []
# README §10.1 (P07/P14): from this episode every kid shot restates the reference (KIDFIX) and every chief
# shot uses the grey-free CHIEFFIX_DESC (CHIEFFIX2). kid() and chief() put each id into its set, so the
# sets always hold every shot of that character; CHIEFFIX (the old tail) stays empty.
KIDFIX = set()
CHIEFFIX = set()
CHIEFFIX2 = set()  # every chief shot: the base description's grey streak kept winning (P07/P14 round 5)
CHIEFFIX_DESC = "the chief is a slim young woman of about thirty with glossy jet-black hair tied in a low ponytail, round black glasses, a yellow pencil tucked behind her ear, a mustard-yellow cardigan over a white blouse, flat 2D cel-shaded cartoon drawing with ink outlines"
KIDFIX_TAIL = ', exactly matching her reference sheet: the same little girl every time, short black bob with straight bangs, navy raincoat with mustard-yellow hood, long navy trousers, bare loose bob hair hanging free, simple dot-like cartoon eyes as on the reference sheet, a round young child face with big round matching eyes looking the same way, flat 2D cel-shaded cartoon drawing with ink outlines'
CHIEFFIX_TAIL = ', exactly matching her reference sheet: slim young woman, glossy jet-black hair with only one thin silver strand, mustard-yellow cardigan over a white blouse, flat 2D cel-shaded cartoon drawing with ink outlines'
def _shot(id, prompt, chars, lines, chapter):
    assert not BANNED.search(prompt), (id, BANNED.search(prompt).group(0))
    assert id not in {s["id"] for s in S}, id
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

# ---------- 開場（系列片頭之後直接進場景，不做濃縮；答案都不先講）----------
kid("kid-camp-pot", K("crouching beside " + POT + " bubbling on " + STOVE + ", lifting a few limp pale noodles with chopsticks and frowning", where=CAMP),
    k("所長！我上個月去山上露營，", "興奮，跑進來報案的語氣"), k("水明明已經滾得咕嘟咕嘟，", "不解"), k("麵卻煮好久都還硬硬的！", "抱怨"), chapter="山上的麵，家裡的爆米花")
kid("kid-gas-guess", K("shaking a small camping gas canister next to her ear with a suspicious frown", close=True, where=CAMP),
    k("我還以為是山上的瓦斯，", "很有把握的錯猜"), k("不夠力！", None, "S:gas"))
kid("kid-popcorn-bowl", K("hugging a big bowl of fluffy white popcorn and grinning", close=True, where=KITCHEN),
    k("可是回家用微波爐爆米花，", "轉折"), k("一下子就啵啵啵全爆開了！", "開心"))
chief("chief-same-water", C("raising one finger with a curious smile"),
      c("這兩件事，其實是同一個角色在搗蛋：水。"), c("你也可以想想看：一樣是把水加熱，", "轉向觀眾"))
chief("chief-main-q", C("holding up both hands like two sides of a scale, eyebrows raised", close=True),
      c("為什麼山上的水滾了，麵還煮不熟，", "放慢"), c("玉米裡的水，卻能把整顆玉米炸開？", "問句", "S:main"))
kid("kid-guess-100", K("holding up both hands with fingers spread wide and a confident grin", close=True),
    k("水滾了就是一百度啊！", "很有把握的錯猜"))
chief("chief-tease-temp", C("tilting her head with a knowing smile", close=True),
      c("那你猜猜，你在山上煮的那鍋滾水，", "賣關子"), c("真的有一百度嗎？", "問句", "S:boil100"))
scene("leftover-kernels", "Close-up of a few small hard golden popcorn kernels lying at the bottom of a bowl of fluffy white popcorn, " + DAY,
      c("還有，你那碗爆米花的碗底，"), c("是不是總剩下幾顆，怎麼熱都不爆？", "賣關子", "S:unpopped"))
kid("kid-leftover", K("holding one tiny hard golden kernel between two fingers and squinting at it", close=True, where=KITCHEN),
    k("對耶，", "想起來"), k("它們是不是比較懶？", "好笑"))
chief("chief-promise", C("folding her arms with a warm smile", close=True),
      c("答案就藏在水的身上。"), c("看它是被放開的，還是被關起來的。"))

# ---------- 第一章：冒泡不代表同一溫度 ----------
scene("camp-wide", "Wide view of a sunny grassy mountain campsite high among green peaks, a small tent and a camping stove with a steaming pot in the middle distance, " + DAY,
      c("你在山上看到的那鍋滾水，跟家裡的長得一模一樣。", "接住上一句"), chapter="水滾了，不一定是一百度")
scene("home-pot", "Medium shot of a plain steel pot of water boiling hard on a gas stove in a bright sunny home kitchen, big round bubbles and soft white steam, " + DAY,
      c("水燒到冒大泡泡，在海邊附近，"), c("大約就是一百度。"))
chief("chief-flat", C("pointing down toward the floor with a warm smile", close=True),
      c("你住在平地，家裡的滾水差不多就是這樣。", "轉向觀眾"))
kid("kid-why-bubble", K("crouching to look closely at a pot of boiling water with big round bubbles, curious eyes", close=True, where=KITCHEN),
    k("那水一燙，", "好奇"), k("為什麼就會冒大泡泡？", "句尾上揚"))
chief("chief-vapour", C("wiggling her fingers upward like tiny bubbles rising, a warm smile"),
      c("水越燙，越多水想變成水氣。"), c("燙到夠了，水裡面就鼓出一顆顆水氣泡泡。"))
kid("kid-fire-up", K("pretending to turn a stove knob with a determined grin", close=True, where=KITCHEN),
    k("那火再開大，", "推理"), k("水不就會更燙？", "句尾上揚", "S:fire"))
chief("chief-fire", C("shaking her head gently with a kind smile"),
      c("不會。水一滾起來，溫度就停住了。"), c("火開大，只是泡泡冒得更兇。", None, "P:fire"))
kid("kid-where-heat", K("tilting her head with a puzzled frown and one finger on her chin", close=True),
    k("那多出來的火，", "追問"), k("跑去哪了？", "句尾上揚"))
chief("chief-into-steam", C("lifting one open hand slowly upward like steam rising"),
      c("拿去把水變成水氣，飄走了。"), c("所以滾水，有一個熱不上去的天花板。"))
kid("kid-ceiling", K("reaching one flat hand up high as if touching a ceiling, wide eyes", close=True),
    k("那個天花板，", "好奇"), k("在哪裡都一樣高嗎？", "句尾上揚"))
chief("chief-press", C("pressing both palms down gently in the air"),
      c("不一定。它要看，水的上面有多少空氣壓著它。"))
kid("kid-air-weight", K("waving one hand through the air with a doubtful laugh", close=True),
    k("空氣？", "懷疑"), k("空氣輕飄飄的，", "不服氣"), k("也會壓東西？", "句尾上揚", "S:airpress"))
chief("chief-quilt", C("patting her own shoulder as if feeling a soft heavy blanket, a playful smile"),
      c("會。你頭上有一大層又高又厚的空氣，"), c("一直輕輕壓著你，也壓著那鍋水。"))
scene("thick-quilt", "Medium shot of a plain steel pot of water on a stove by a sunny seaside, a huge thick soft fluffy quilt of white air resting over the pot, " + DAY,
      c("就像蓋著一床很厚的空氣棉被。", None, "P:airpress"), c("水裡的泡泡要冒出來，得先把棉被推開。"))
kid("kid-bubble-push", K("pushing both hands forward hard as if shoving open a heavy door", close=True),
    k("泡泡要用力推？", "驚訝"))
chief("chief-hot-enough", C("nodding with one finger raised"),
      c("對，水要熱到夠，水氣的泡泡才推得開。"), c("在海邊，這床棉被最厚，水要熱得最多。"))
kid("kid-mountain-q", K("pointing up at tall green peaks behind her with a curious face", where=CAMP),
    k("那爬到山上呢？", "追問"))
chief("chief-thin", C("lifting one hand higher and higher with a calm smile"),
      c("越往上爬，你頭上的空氣就越少，"), c("那床棉被，就變得又薄又輕。"))
scene("thin-quilt", "Medium shot of " + POT + " bubbling on " + STOVE + " at a sunny grassy mountain campsite with green peaks, a thin light wisp of white air resting over the pot, " + DAY,
      c("棉被薄了，泡泡不用那麼熱，就推得開。"))
kid("kid-cooler-boil", K("with her mouth open in surprise, both hands on her cheeks", close=True, where=CAMP),
    k("所以山上的水，", "慢慢想通"), k("不用那麼燙就滾了？", "句尾上揚"))
chief("chief-3000", C("holding up three fingers with raised eyebrows", close=True),
      c("對。在三千公尺左右的高山上，", "數字放慢"), c("水大約九十度就滾了。", None, "P:boil100"))
chief("chief-yushan", C("pointing up toward one side with a warm smile"),
      c("台灣最高的玉山，將近四千公尺，", "轉向觀眾"), c("山頂的滾水，連九十度都不到。"))
chief("chief-longer", C("holding both hands as if around a warm bowl, a gentle smile", close=True),
      c("所以在山上煮麵、煮蛋、煮飯，"), c("常常都要比在家裡多等一會兒。"))
kid("kid-yushan", K("gazing up at a tall green mountain peak with clouds around it, eyes wide", where=CAMP),
    k("滾水只有八十幾度！", "大驚"))
kid("kid-but-bubbles", K("crouching by " + POT + " full of bubbles with a stubborn pout", where=CAMP),
    k("可是它一樣在冒泡泡啊，", "不服氣"), k("為什麼麵還是硬的？", "句尾上揚", "S:noodles"))
chief("chief-cook", C("holding one hand flat and moving it slowly forward"),
      c("把麵煮熟的，是水的熱，不是泡泡。"), c("水沒那麼燙，熱鑽進麵裡就比較慢。"))
chief("chief-gas", C("shaking her head gently with a kind smile", close=True),
      c("所以麵煮得慢，不是瓦斯不夠力，", None, "P:gas"), c("是那鍋水本身就沒那麼燙。"))
kid("kid-fire-again", K("pretending to turn a stove knob all the way up with a hopeful grin", close=True, where=CAMP),
    k("那我把火轉到最大！", "想到辦法"))
chief("chief-ceiling-back", C("smiling and tilting one hand side to side", close=True),
      c("還記得那個天花板嗎？火再大，", "點名回呼"), c("水也只會停在剛剛那個溫度，只是滾得更兇。"))
kid("kid-wait-long", K("sitting by " + POT + " with her chin in her hands and a bored sigh", where=CAMP),
    k("所以只能煮久一點！", "恍然大悟", "P:noodles"))
chief("chief-lid-tease", C("pressing one flat hand down on top of the other, eyebrows raised"),
      c("對。所以有人會想：那如果反過來，"), c("把蓋子壓得緊緊的，不讓水氣跑掉呢？", "賣關子"))
kid("kid-lid-q", K("pressing both hands down hard on the lid of " + POT + " with a curious face", close=True, where=KITCHEN),
    k("蓋子壓緊，", "推理"), k("水會變得更燙嗎？", "章尾停住，句尾上揚", "S:lid"))

# ---------- 第二章：把水封進玉米殼 ----------
chief("chief-cooker", C("raising one hand in a calm careful gesture"),
      c("會。有一種蓋子會鎖緊的鍋，叫做壓力鍋，", "接住上一句"), c("在很高的山上，常有人用它煮飯。"), chapter="把水關進玉米殼裡")
chief("chief-careful", C("holding up one palm gently like a careful reminder, a serious kind face", close=True),
      c("不過壓力鍋要大人照說明使用，", "叮嚀"), c("我們不自己在家關水氣做實驗。"))
chief("chief-tiny-pot", C("holding up a tiny popcorn kernel between two fingers with a playful smile"),
      c("我們看大自然做的小小壓力鍋就好，"), c("它就是你碗底的那一顆玉米。"))
scene("kernel-big", "Close-up of " + KERNEL + " sitting on a pale wooden kitchen table, " + DAY,
      c("爆米花的玉米，外面包著一層又硬又亮的殼，"), c("水氣幾乎鑽不出去。"))
kid("kid-any-corn", K("holding up a yellow corn on the cob with a hopeful grin", close=True, where=KITCHEN),
    k("那我吃的玉米棒，", "追問"), k("也能爆嗎？", "句尾上揚"))
chief("chief-strain", C("holding up one tiny kernel with a calm smile", close=True),
      c("爆米花用的是一種特別的玉米，"), c("它的殼特別硬，又不太透水，跟大多數穀物不一樣。"))
kid("kid-dry", K("holding a golden kernel close to one eye and squinting hard", close=True, where=KITCHEN),
    k("可是它乾乾硬硬的，", "懷疑"), k("裡面哪有水？", "句尾上揚", "S:dry"))
scene("kernel-inside", "Close-up cutaway of " + KERNEL + ", its inside filled with soft white starch and one small glistening drop of water tucked in the middle, " + DAY,
      c("有喔。殼的裡面是軟軟的澱粉，"), c("中間還藏著一小滴水。"))
chief("chief-percent", C("holding her finger and thumb a little apart with a warm smile", close=True),
      c("一顆好爆的玉米，大約一百份裡，"), c("有十四份左右是水。", "數字放慢", "P:dry"))
kid("kid-hidden-water", K("with her mouth open in surprise, holding up a kernel", close=True, where=KITCHEN),
    k("看起來乾乾的，", "驚訝"), k("原來偷藏著水！"))
chief("chief-heat-kernel", C("rubbing her hands together as if warming them"),
      c("鍋子一熱，這滴水也想變成水氣，"), c("可是硬殼把它關在裡面。"))
scene("kernel-puff", "Close-up of " + KERNEL + " on a warm pan, the kernel looking round and puffed up and tight like an overfilled balloon, faint soft warm glow around it, " + DAY,
      c("水氣出不去，就在殼裡越擠越多。"), c("整顆玉米，像一顆越吹越緊的氣球。"))
kid("kid-hotter-q", K("frowning and holding her two hands together tight as if squeezing a ball", close=True),
    k("可是你剛剛說，", "抓到問題"), k("水熱不過天花板呀？", "句尾上揚", "S:hotter"))
chief("chief-quilt-back", C("pressing her palms together hard with raised eyebrows"),
      c("還記得那床空氣棉被嗎？", "點名回呼"), c("在殼裡，壓著水的不是棉被，是越擠越多的水氣。"))
chief("chief-higher-ceiling", C("lifting one flat hand higher and higher in steps"),
      c("壓得越用力，泡泡越難推開，"), c("水就得熱過平地的滾水，天花板也跟著升高。", None, "P:hotter"))
kid("kid-mountain-flip", K("pointing at a golden kernel in her palm with an excited grin", close=True, where=KITCHEN),
    k("跟山上剛好相反！", "想通"))
chief("chief-180", C("holding up one finger with a calm smile", close=True),
      c("對。研究的人量過，玉米大多在一百八十度左右爆開，", "數字放慢"))
chief("chief-ten-times", C("spreading her arms wide as if holding something very tight"),
      c("那時殼裡的壓力，大約是外面空氣的九到十倍。", "數字放慢"))
kid("kid-ten-times", K("puffing out her cheeks like a tight balloon and laughing", close=True),
    k("殼快被撐破了！", "好笑"))
chief("chief-liquid", C("raising one finger with a curious smile", close=True),
      c("還有一件怪事：研究的人算過，殼破之前，"), c("裡面大部分的水，其實還是液體。"))
kid("kid-still-water", K("tilting her head with a puzzled frown and one finger on her chin", close=True),
    k("都那麼燙了，", "不解"), k("還沒變成水氣？", "句尾上揚"))
chief("chief-held", C("pressing both palms together tightly, then easing them apart slightly"),
      c("對，殼裂之前壓力太大，大部分只能先當水。"), c("等殼一破、壓力一鬆，它們才急著變成水氣。"))
chief("chief-cooking", C("nodding with a warm smile"),
      c("這段時間，裡面的澱粉也被燙得又軟又黏，"), c("像一團準備好的麵糊。"))
kid("kid-big-fire", K("pretending to turn a stove knob all the way up with a mischievous grin", close=True, where=KITCHEN),
    k("那我火開超大，", "試探"), k("是不是爆得更快？", "句尾上揚"))
chief("chief-too-fast", C("tilting one hand side to side with an honest smile"),
      c("太快也不好。外面的水氣太早撐破殼，"), c("中間的澱粉還沒燙軟，就變成中間硬硬的半顆。"))
kid("kid-lazy-back", K("holding up one tiny hard leftover kernel with a curious face", close=True, where=KITCHEN),
    k("那碗底那幾顆，", "點名回呼"), k("為什麼就是不爆？", "句尾上揚"))
chief("chief-too-dry", C("holding her finger and thumb almost touching, a gentle smile", close=True),
      c("常見的原因，是它太乾了。"), c("水太少，擠不出夠大的力氣撐破殼。"))
chief("chief-tip", C("pointing at the tip of a tiny kernel between two fingers, eyebrows raised"),
      c("還有，玉米尖尖那頭接著玉米棒，"), c("那裡不太擋得住水氣，加熱太慢，水氣會偷偷漏走。", None, "P:unpopped"))
kid("kid-leak", K("making a small whoosh shape with her hand by her mouth, a knowing grin", close=True),
    k("漏氣了，", "推理"), k("就爆不起來了！", "想通", "P:lid"))
kid("kid-crack-q", K("staring at a golden kernel on a warm pan with wide eyes, holding her breath", where=KITCHEN),
    k("那殼終於撐破的時候，", "追問"), k("它為什麼會跳起來？", "章尾停住，句尾上揚", "S:jump"))

# ---------- 第三章：外殼破了，接著才跳 ----------
kid("kid-rocket", K("pretending to launch a rocket upward from her hands with a big grin", close=True),
    k("是不是水氣從裂縫噴出來，", "很有把握的錯猜"), k("像火箭把它推上天？", None, "S:rocket"), chapter="殼破了，接著才跳")
chief("chief-paper", C("tapping the side of her glasses with a knowing smile", close=True),
      c("很多人都這樣猜。二〇一五年，法國有兩位研究的人，", "接住上一句"), c("想把這件事看清楚。"))
scene("camera", "Close-up of a big black high-speed camera on a tripod pointing at a plain round hot plate with a few golden popcorn kernels on it, in a bright tidy lab, " + DAY,
      c("他們把玉米放在一塊熱鐵板上，"), c("用一秒拍將近三千張的高速相機，慢慢看。"))
kid("kid-3000", K("blinking fast with her mouth open in amazement", close=True),
    k("一秒三千張！", "驚奇"), k("看到什麼了？", "句尾上揚"))
scene("kernel-crack", "Close-up of " + KERNEL + " on a warm pan with one thin crack opening across its shell and a small puff of soft white starch peeking out, " + DAY,
      c("先是殼裂開一條縫，軟軟的澱粉，"), c("就從裂縫裡一下子鼓了出來。"))
chief("chief-white", C("opening both hands wide like a flower blooming"),
      c("關了很久的水氣，一下子全部放開，"), c("把那團軟澱粉，吹成一大朵白白的泡泡。"))
kid("kid-white-q", K("holding one fluffy white popped popcorn next to one small golden kernel, puzzled", close=True, where=KITCHEN),
    k("怪不得黃黃小小的一顆，", "推理"), k("會變成白白一大朵？", "句尾上揚", "S:white"))
chief("chief-crispy", C("nodding with a warm smile", close=True),
      c("對。黃色其實只在那層殼上，"), c("裡面的澱粉，本來就是白的。", None, "P:white"))
chief("chief-set", C("pressing her fingertips together as if feeling something crisp"),
      c("那團白泡泡一離開熱鍋就變涼，"), c("馬上變硬，就是你咬的那口脆脆的。"))
kid("kid-jump-yet", K("leaning forward eagerly with both fists clenched", close=True),
    k("那它什麼時候跳？", "追問"))
scene("starch-leg", "Close-up of a popcorn piece on a warm round pan, one soft white puff of starch pressed flat against the pan like a little springy foot, " + DAY,
      c("鼓出來的澱粉，有一塊壓在鍋子上，"), c("像長出一隻短短的小腳。"))
kid("kid-leg", K("laughing and pointing at her own leg", close=True),
    k("爆米花也有腳？", "好笑，句尾上揚"))
chief("chief-spring", C("pressing one hand down then lifting it quickly like a spring"),
      c("那隻腳先被壓扁，再像彈簧一樣彈回去，"), c("就把整顆玉米踢離鍋子。", None, "P:jump"))
chief("chief-not-rocket", C("shaking her head gently with a kind smile"),
      c("所以讓它跳起來的主角，是那隻澱粉腳，"), c("不是水氣像火箭那樣噴。", None, "P:rocket"))
kid("kid-squat", K("squatting low and then springing up with arms in the air, laughing", where=KITCHEN),
    k("跟我跳遠一樣，", "開心"), k("先蹲再跳！", "開心"))
chief("chief-flea", C("holding her finger and thumb close together with a playful smile", close=True),
      c("研究的人說，它的跳法有點像跳蚤，"), c("也有點像某些會彈出種子的植物。"))
kid("kid-flea-q", K("crouching low and pretending to hop like a tiny flea, giggling", close=True),
    k("跳蚤？", "好笑"), k("那它跳得多快？", "句尾上揚"))
chief("chief-fast", C("snapping her fingers with raised eyebrows"),
      c("從殼裂開到跳起來，只有百分之幾秒，"), c("快到你的眼睛只看到一閃。"))
kid("kid-flip", K("spinning one finger round in the air with a dizzy grin", close=True),
    k("眨一下眼就錯過了！", "好笑"))
chief("chief-height", C("holding one hand just a little above the other"),
      c("如果只靠那一踢，他們估計，"), c("大約能跳一公分左右。"))
kid("kid-one-cm", K("holding her finger and thumb a tiny bit apart with raised eyebrows", close=True),
    k("才一公分？", "驚訝"), k("我還以為它會飛好高！"))
chief("chief-one-cm", C("laughing softly with one hand raised a little"),
      c("研究的人說，他們看到的跳法，"), c("跟這個估計差不多是同一個大小。"))
kid("kid-pop-q", K("cupping one hand behind her ear and listening hard", close=True, where=KITCHEN),
    k("那「啵」的一聲，", "追問"), k("是殼破掉的聲音嗎？", "章尾停住，句尾上揚", "S:sound"))

# ---------- 第四章：那聲啵又是哪一步 ----------
chief("chief-mic", C("cupping one hand behind her ear with a curious smile"),
      c("他們也想知道。所以在旁邊放了一支麥克風，", "接住上一句"), c("一邊錄聲音，一邊拍。"), chapter="那聲啵，晚了一點才出來")
scene("mic", "Close-up of a round black microphone on a small stand beside a plain round hot plate with golden popcorn kernels on it, in a bright tidy lab, " + DAY,
      c("聲音和畫面對在一起，就知道每一聲是哪一步。"))
kid("kid-how-long", K("holding her breath with puffed cheeks and wide eyes", close=True),
    k("那一聲啵，", "好奇"), k("有多長？", "句尾上揚"))
chief("chief-50ms", C("snapping her fingers once with a playful smile", close=True),
      c("他們錄到的，大約只有二十分之一秒。"))
kid("kid-crack-guess", K("making a snapping gesture with both hands with a confident grin", close=True),
    k("一定是殼裂開，", "很有把握的錯猜"), k("喀的那一下！"))
chief("chief-after", C("holding up one finger and then a second one a moment later"),
      c("聲音沒有在殼裂開的那一瞬間出來，"), c("而是晚了千分之幾秒。"))
kid("kid-foot-guess", K("stomping one foot with a curious face", close=True),
    k("那是小腳踢鍋子的聲音？", "再猜"))
chief("chief-not-foot", C("shaking her head gently with a playful smile", close=True),
      c("也不是。研究的人推測，是水氣衝出來的時候，"))
scene("hollow-ring", "Close-up of a popcorn piece bursting open on a warm pan, soft white steam rushing out of small round hollows inside the puff, gentle round ripples in the air around it, " + DAY,
      c("讓玉米裡面的小空洞，一起被震響了。", None, "P:sound"))
kid("kid-bottle", K("blowing across the top of an empty glass bottle with puffed cheeks", close=True, where=KITCHEN),
    k("像我對著瓶口吹氣，", "想到"), k("會嗚嗚叫一樣？", "句尾上揚"))
chief("chief-bottle", C("nodding with a warm smile"),
      c("有一點像。都是空氣在空洞裡，"), c("一下子被推動，就發出聲音。"))
chief("chief-three", C("holding up three fingers one by one with a calm smile"),
      c("所以殼裂開、發出啵、跳起來，"), c("是三件不同的事，只是快到黏在一起。"))
chief("chief-many", C("cupping one hand behind her ear with a warm smile"),
      c("你在鍋邊聽到一串啵啵啵，", "轉向觀眾"), c("其實是好多顆玉米，一顆一顆各自走完這三步。"))
kid("kid-three", K("counting on her fingers with her tongue sticking out in concentration", close=True),
    k("原來是三件事！", "整理"))
chief("chief-compare", C("holding up both hands like two sides of a scale"),
      c("還記得山上那鍋水嗎？把它和這顆玉米擺在一起，"))
scene("pot-and-kernel", "Medium shot of " + POT + " with gentle bubbles under a thin light wisp of white air on the left, and one round tight puffed-up golden popcorn kernel glowing warm on the right, a pale cream background, " + DAY,
      c("一個鍋子開著，一顆玉米關著。"), c("差別只在，壓著水的力氣有多大。"))
kid("kid-same-rule", K("raising one finger with sparkling eyes", close=True),
    k("可是規矩是同一條？", "句尾上揚"))
chief("chief-rule", C("pressing her palms together gently with a calm smile"),
      c("對，就是剛剛那條天花板規矩，"), c("只是一個壓得輕，一個壓得重。"))
kid("kid-either", K("holding a golden kernel in one hand and a small camping pot lid in the other, a thinking face", close=True, where=KITCHEN),
    k("壓著水的，", "推理"), k("可以是空氣，也可以是水氣？", "句尾上揚"))
chief("chief-either", C("nodding with her hands open, a calm smile"),
      c("對，誰在壓都一樣。"), c("所以同一條規矩，能讓麵煮不熟，也能讓玉米炸開。"))
chief("chief-opinion", C("folding her arms and laughing softly"),
      c("我覺得，水最會騙人的就是那些泡泡：", "意見，輕鬆"), c("它們只告訴你水滾了，沒告訴你水有多燙。"))
kid("kid-trick", K("narrowing her eyes at a pot of bubbling water like a detective, one finger raised", where=KITCHEN),
    k("泡泡騙了我！", "像偵探"))

# ---------- 收尾 ----------
chief("chief-back-camp", C("smiling and pointing back over her shoulder"),
      c("還記得你一開始問我的兩件事嗎？你自己說說看。", "笑"), chapter="小問自己破案")
kid("kid-got-it", K("throwing both arms up with a huge happy smile", where=KITCHEN),
    k("就是剛剛那條薄棉被！", "篤定"), k("讓山上的水不到一百度就滾，", "篤定"), k("麵才煮得慢！", "開心"))
kid("kid-got-it2", K("holding up a fluffy white popcorn proudly with both hands", close=True, where=KITCHEN),
    k("還有剛剛那層硬殼，", "篤定"), k("把水關到熱得炸開！", "開心", "P:main"))
chief("chief-done", C("smiling warmly at the viewer with her hands clasped", close=True),
      c("下次你吃爆米花，可以先聽一聽：", "轉向觀眾，輕聲"), c("每一聲啵，就是又有一顆玉米走完了那三步。", "點名回呼"))
chief("chief-safe", C("holding up one palm gently like a careful reminder, a kind smile"),
      c("微波爐爆米花的袋子剛拿出來很燙，"), c("要讓大人打開，別把臉湊過去。", "叮嚀"))
# The outro is three pictures, no card, no stamp (series README §3.2, §10.1): the kid gives a thumbs-up.
kid("outro", "Head-and-shoulders close-up of the girl with a big happy smile giving a big cheerful thumbs-up with one hand, bright morning light",
    k("原來如此！", "開心大聲"))
chief("outro-chief", "Waist-up medium shot of the chief tilting her head with a curious smile and one finger raised, a plain pale wall behind her, bright morning light",
      c("你家的爆米花，碗底最後剩下幾顆沒爆？", "問句上揚，像聊天"), c("留言告訴我們。"))
chief("outro-wave", "Waist-up medium shot of the chief waving goodbye with a warm smile, a plain pale wall behind her, bright morning light",
      c("想一起找生活裡的為什麼，就訂閱原來如此事務所。", "誠懇"))

# ---------- assemble ----------
WHAT = {"main": "一樣是把水加熱，為什麼山上的麵煮不熟、玉米卻會炸開", "boil100": "山上那鍋滾水真的有一百度嗎",
        "unpopped": "碗底那幾顆為什麼怎麼熱都不爆", "fire": "火開大，水會不會更燙", "airpress": "輕飄飄的空氣也會壓東西嗎",
        "noodles": "水一樣在冒泡，山上的麵為什麼還是硬的", "lid": "把蓋子壓緊不讓水氣跑掉，水會不會更燙",
        "dry": "乾乾硬硬的玉米裡面哪有水", "hotter": "水不是熱不過天花板嗎，殼裡怎麼能更熱",
        "jump": "殼撐破的時候，玉米為什麼會跳起來", "gas": "麵煮得慢是不是山上的瓦斯不夠力", "rocket": "是不是水氣像火箭一樣把它噴上天",
        "white": "黃黃小小的一顆，怎麼變成白白一大朵", "sound": "那聲啵是不是殼破掉的聲音", }
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
    "target_minutes": [12, 14], "voice": VOICE, "subtitles": {"burn_in": False}, "theme": "paper", "look": {"preset": "cute-cartoon"},
    # The series tag: the approved character sheets live in the series store and every episode reuses them (docs/videos/SERIES.md).
    "series": {"slug": "sothatswhy", "episode": 8, "chapter": 1},
    # Same 14-minute bed as P02/P05/P07/P14 (one paid Lyria take, tail trimmed, crossfaded): the series sounds the same.
    "music": {"track": "sothatswhy-p02-bed.m4a", "sha256": "54169439df49a00bc3ad993a148690be9f79d1dff8a4ea5143e64e583001b20c", "gain_db": -20, "duck_db": -10},
    "characters": CHARACTERS, "loops": loops,
    "youtube": {
        "category_id": 27, "made_for_kids": False, "default_language": "zh-TW",
        "title": "山上滾水煮得慢，玉米為什麼又會爆開？｜原來如此事務所",
        "description": "小問去山上露營，水明明滾了，麵卻煮好久還是硬的；回家用微波爐爆米花，一下子就全爆開。一樣是把水加熱，結果怎麼差這麼多？\n\n"
                       "這一集，所長和小問跟著同一滴水走：先看滾水為什麼有一個熱不上去的天花板，山上的空氣為什麼讓這個天花板變低；"
                       "再把水關進玉米的硬殼裡，看它怎麼熱過一百度、撐到殼破；最後用二〇一五年的高速攝影研究，分開殼裂開、跳起來和那聲「啵」是哪三件事。\n\n"
                       "本集插圖由 AI 生成，畫的是示意，不是量測。片中的沸點、爆開溫度與壓力都是教學資料與研究裡的大約數字；壓力鍋只在片中提到，請不要自己在家做加壓實驗。"
                       "每個說法的出處列在下方參考資料。\n\n資料截至 " + CHECKED,
        "tags": ["爆米花", "沸點", "高山煮麵", "氣壓", "玉山", "科普", "原來如此事務所"],
        "video_id": None},
    "thumbnail": {"template": "thumb", "data": {"headline": "山上的滾水\n**不到一百度**", "sub": "玉米卻把水關到快一百八十度", "shot": "kid-popcorn-bowl"}},
    "sources": [
        {"title": "Virot & Ponomarenko (2015), Popcorn: critical temperature, jump and sound, J. R. Soc. Interface 12: 20141247", "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC4345489/", "checked_on": CHECKED},
        {"title": "OpenStax Chemistry 2e, 10.3 Phase Transitions", "url": "https://openstax.org/books/chemistry-2e/pages/10-3-phase-transitions", "checked_on": CHECKED},
        {"title": "Wikipedia: High-altitude cooking", "url": "https://en.wikipedia.org/wiki/High-altitude_cooking", "checked_on": CHECKED},
        {"title": "Wikipedia: Popcorn", "url": "https://en.wikipedia.org/wiki/Popcorn", "checked_on": CHECKED},
        {"title": "Popcorn Board: What Makes Popcorn Pop?", "url": "https://www.popcorn.org/All-About-Popcorn/What-Makes-Popcorn-Pop", "checked_on": CHECKED},
        {"title": "Wikipedia: Yushan (mountain)", "url": "https://en.wikipedia.org/wiki/Yushan_(mountain)", "checked_on": CHECKED},
        {"title": "NOAA JetStream: Air Pressure", "url": "https://www.noaa.gov/jetstream/atmosphere/air-pressure", "checked_on": CHECKED},
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
outro_ids = {"outro", "outro-chief", "outro-wave"}
body = [s for s in scenes if s["id"] not in outro_ids]
chars = sum(length(l["text"]) for s in scenes for l in s["lines"])
body_chars = sum(length(l["text"]) for s in body for l in s["lines"])
kidc = sum(length(l["text"]) for s in scenes for l in s["lines"] if l["speaker"] == "kid")
lines_all = [l for s in scenes for l in s["lines"]]
print(f"scenes {len(scenes)} shots {len(scenes)} lines {n} chars {chars} (body {body_chars}) kid {kidc / chars:.0%} of chars, "
      f"{sum(l['speaker'] == 'kid' for l in lines_all) / n:.0%} of lines; est {chars / RATE / 60:.1f} min at {RATE}/s; loops {len(loops)}", file=sys.stderr)
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
