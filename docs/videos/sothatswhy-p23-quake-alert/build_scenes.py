"""Generate video.json for sothatswhy-p23-quake-alert (原來如此事務所 對話版 P23).

Run `python3 build_scenes.py` from anywhere: it rewrites video.json next to this file and freezes
every shot's camera move in cameras.json (a shot keeps the camera it was first given, so deleting
a shot never shifts the others: the camera is in the keyframe cache key).
Edit lines and prompts here, never in video.json.
"""
import itertools, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = "sothatswhy-p23-quake-alert"
CHECKED = "2026-11-07"

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
LIVING = "in a bright sunny living room"
TABLE = "a sturdy plain wooden dining table"
PHONE = "a smartphone glowing bright orange and vibrating"
UNDER = "Wide cutaway view of the ground with green fields and small houses on top and thick brown rock layers below"
# One drawing language for the whole episode (README §10.5: numbers as feelings, one metaphor throughout):
# an earthquake is a race that starts deep underground. The epicentre is the starting line; the P wave is a small
# quick messenger drawn as a light bright ripple; the S wave is the big one, drawn as a tall heavy wave in the rock;
# the stations are small sturdy metal boxes in the grass (the referees by the track); the alert rides electricity,
# drawn as a glowing ribbon of light along power lines. Nothing is counted, nothing depends on direction, no clock,
# no gauge, no phone face: a phone is only ever an orange glow that vibrates.
# Prompt words that P02/P05 taught us to keep out (README §3.1): the model has no negative prompt,
# lamps and night turn frames into 3D figurines, and these props sprout fake letters.
BANNED = re.compile(r"\b(no|not|without|text|blank|lamp|night|notebook|sign|signs|paper|poster|screen|book|calendar|whiteboard|thermometer|remote|label|magnet|map|chart|grey hair|gray)\b", re.I)

CAMS = itertools.cycle(["push in", "pan left", "pull out", "drift", "tilt up", "pan right", "push in", "tilt down", "pull out", "drift"])
CAM_FILE = os.path.join(HERE, "cameras.json")
FROZEN = json.load(open(CAM_FILE, encoding="utf-8")) if os.path.exists(CAM_FILE) else {}

S = []
EXTRA = {}
def _shot(id, prompt, chars, lines, chapter):
    prompt = prompt + EXTRA.get(id, "")
    assert not BANNED.search(prompt), (id, BANNED.search(prompt).group(0))
    assert id not in {s["id"] for s in S}, id
    cam = FROZEN.get(id) or next(CAMS)
    S.append(dict(id=id, chapter=chapter, template="shot", data=dict(prompt=prompt, camera=cam, visual="still", characters=list(chars)), lines=list(lines)))
def kid(id, prompt, *lines, chapter=None):
    """The kid doing one simple thing, facing the camera, waist-up or head-and-shoulders."""
    _shot(id, prompt.rstrip(". ") + ", " + KIDDESC + KIDFIX_TAIL, ["kid"], lines, chapter)
def chief(id, prompt, *lines, chapter=None):
    """The chief, always waist-up or head-and-shoulders, in front of a plain wall in daylight, in her `office` look."""
    assert prompt.startswith(("Waist-up", "Head-and-shoulders")), id
    _shot(id, prompt.rstrip(". ") + ", " + CHIEFFIX_DESC, ["chief"], lines, chapter)
    S[-1]["data"]["character_looks"] = {"chief": "office"}
def scene(id, prompt, *lines, chapter=None):
    """No character: an object, a place or a mechanism drawn as a picture."""
    _shot(id, prompt + FLAT, [], lines, chapter)
    S[-1]["data"]["nobody"] = True  # PR #2028: no person or face in an object-only shot
def k(t, e=None, tag=None): return ("kid", t, e, tag)
def c(t, e=None, tag=None): return ("chief", t, e, tag)

def C(action, close=False):
    return ("Head-and-shoulders close-up" if close else "Waist-up medium shot") + " of the chief " + action + ", " + WALL + ", " + DAY
def K(action, close=False, where=None):
    return ("Head-and-shoulders close-up" if close else "Waist-up medium shot") + " of the girl " + (where + " " if where else "") + action + ", " + DAY

# ---------- 開場（系列片頭之後直接進場景，不做濃縮；答案都不先講）----------
# One metaphor only: an earthquake is a race. 震央 = the point on the ground over the starting line, P波 = the small
# quick messenger (小信差), S波 = the big one (大個子), 測站 = the referees by the track, the alert rides electricity.
# Round 2 (2026-11-07): verify-1 F01-F10 applied word for word; review-script-score and the blind panel's notes:
# chief shots cut to about a fifth, mechanism lines moved onto object pictures, prompts with direction, counting,
# hands at the face or a chief acting out drop-cover-hold replaced; the waves are drawn as a small thin ripple and a
# huge thick band of rock (size, never position), machines are plain smooth unmarked.
kid("kid-phone-blare", K("jumping up startled from her chair beside " + PHONE + " on " + TABLE, where=LIVING),
    k("所長！昨天早上我在吃早餐，", "興奮，跑進來報案的語氣"), k("媽媽的手機突然大叫！", "誇張"), chapter="手機先大叫，房子才搖")
scene("phone-orange", "Close-up of " + PHONE + " hard on a sunny wooden breakfast table beside a bowl of rice porridge and a glass of milk, " + DAY,
      k("爸爸的手機也一起叫，", "比手畫腳"), k("好大聲，好可怕！"))
kid("kid-table-shake", K("holding tightly onto the edge of " + TABLE + " with wide startled eyes as a glass of milk on it wobbles", where=LIVING),
    k("過了幾秒，房子就開始搖！", "緊張"), k("先輕輕的，再一下子大搖！", "比手畫腳", "S:order"), k("牛奶都灑出來了！", "委屈"))
kid("kid-how-know", K("tilting her head with a puzzled frown, both hands out of frame", close=True),
    k("手機怎麼比地震還早知道？", "句尾上揚"))
chief("chief-not-early", C("laughing softly with one hand on her chest", close=True),
      c("那個聲音，我第一次聽也嚇一跳。", "笑"), c("它叫做地震警報。"), c("不過它響的時候，地震其實已經開始了。", "接住她的問題"))
kid("kid-predict", K("blinking with a surprised round open mouth", close=True),
    k("它不是預測地震喔？", "驚訝"))
chief("chief-predict", C("shaking her head kindly with a warm smile"),
      c("不是。預測，是地震還沒發生就先猜。"), c("警報是地震已經開始了，才趕快通知你。"))
kid("kid-not-yet", K("looking down at the wooden floor with a puzzled face, both hands out of frame", where=LIVING),
    k("已經開始了，", "不解"), k("那我家怎麼還沒搖？", "句尾上揚"))
scene("milk-still", "Close-up of " + PHONE + " on a calm sunny breakfast table, a full glass of milk standing perfectly still beside it, " + DAY,
      c("問得好，這就是最奇怪的地方。"), c("地震開始了，你家還沒搖，手機卻先叫了。"))
chief("chief-tease-blind", C("leaning in a little with a serious kind face", close=True),
      c("不過你知道嗎？有些人家，大搖晃比警報還早到。", "轉向觀眾", "S:blind"))
scene("city-tease", "Wide view of a big city of plain smooth unmarked tall buildings in a green basin ringed by hills on a sunny morning, " + DAY,
      c("還有一次大地震，台北搖得很厲害，"), c("很多人的手機，卻一聲都沒響。", "賣關子", "S:taipei"))
chief("chief-main-q", C("folding her hands with a curious smile, eyebrows raised"),
      c("這一集，我們就把那幾秒找出來。", "承諾"), c("地震都已經開始了，"), c("警報怎麼還能搶在大搖晃前面？", "問句", "S:main"))

# ---------- 第一章：地底下開始的賽跑 ----------
scene("ground-start", UNDER + ", one bright glowing spot deep inside the rock with soft rings spreading out from it, " + DAY,
      c("因為地震一開始，就是一場賽跑。", "接住上一句"), c("起點在地底下，地震開始的那個地方。"), chapter="地底下開始的賽跑")
kid("kid-where-start", K("crouching to look closely at the wooden floor with a curious face, both hands out of frame", where=LIVING),
    k("起點在我家下面嗎？", "句尾上揚"))
scene("epicentre-dot", UNDER + ", one bright glowing spot deep inside the rock and one small bright yellow dot on the green grass at the surface, " + DAY,
      c("每次都不一樣，常常離你家很遠。"), c("起點正上方，地面上那一點，叫做震央。"))
kid("kid-epi", K("nodding with a serious little face, both hands out of frame", close=True),
    k("震央，在起點正上方！", "記住了"))
chief("chief-epi-yes", C("smiling and giving a small nod", close=True),
      c("對，起點在地底下，震央在它正上方。"))
kid("kid-whole-q", K("spreading both arms wide with a curious face", where=LIVING),
    k("那地震一開始，", "好奇"), k("是不是全台灣一起搖？", "句尾上揚", "S:whole"))
scene("ripple-out", "Wide view from a hill of green countryside and small towns, soft round ripples in the ground like rings on a pond, " + DAY,
      c("不是。搖晃從起點往外，一路跑出去，", None, "P:whole"), c("離震央越遠，就越晚跑到。"), c("而且跑出去的，不只一個。"))
kid("kid-two-q", K("leaning in with wide curious eyes, both hands out of frame", close=True),
    k("還有別人在跑？是誰？", "好奇"))
scene("messenger", "Wide cutaway view of brown rock layers underground with one thin small bright quick ripple, tiny next to a huge thick heavy band of rock bulging slowly",
      c("跑在最前面的，是一個快腿的小信差。"), c("它搖得很輕，多半是上下跳一跳。"))
kid("kid-updown", K("bobbing up on her toes with a surprised little smile", where=LIVING),
    k("就像地板往上頂一下？", "句尾上揚"))
scene("ripple-close", "Close-up of one thin small bright ripple glowing softly inside smooth brown rock",
      c("對，輕輕的。科學家叫這個小信差，P波。"))
scene("big-wave", "Wide cutaway view of brown rock layers underground with a huge thick heavy band of rock bulging, small houses on the green ground with gently tilted roofs",
      c("後面跟著一個大個子，叫S波。"), c("它前後左右用力晃，搖得兇多了。"))
kid("kid-big-guy", K("swaying with both arms out for balance and a wobbly grin", where=LIVING),
    k("把東西搖倒的，", "推理"), k("就是大個子？", "句尾上揚"))
scene("tilted-house", "Medium shot of a small cartoon house on green grass with its roof tilted and a little tree leaning, a fallen flowerpot beside it, " + DAY,
      c("通常是它。小信差溫柔得多。"))
kid("kid-order-got", K("with a bright face of sudden discovery, eyes wide and mouth open", close=True),
    k("所以我先覺得輕輕的，", "恍然"), k("是小信差先到！", "開心", "P:order"))
scene("milk-spill", "Close-up of a glass of milk tipped over on a sunny wooden breakfast table, a small puddle of milk spreading, " + DAY,
      c("對，後面那一下大搖，就是大個子到了。"))
kid("kid-speed-q", K("bouncing on her toes with an eager face", where=LIVING),
    k("它們兩個，到底跑多快？", "句尾上揚", "S:speed"))
scene("speed", "Wide view of a long straight country road across green fields under a sunny sky, a thin small bright quick ripple and a huge thick heavy band in the ground beside the road, " + DAY,
      c("小信差一秒，大約跑六公里半。", None, "P:speed"), c("大個子慢一點，一秒大約四公里。"))
kid("kid-fast", K("pumping one fist with an excited grin", close=True),
    k("那小信差一直跑，", "推理"), k("就會越領先越多？", "句尾上揚"))
chief("chief-count", C("leaning in with a playful smile, one finger raised", close=True),
      c("對。你數一、二，大個子跑了大約八公里，", "轉向觀眾"), c("小信差大約十三公里，已經領先大約五公里了。"))
kid("kid-gap-q", K("hugging a round cushion with a worried face", where=LIVING),
    k("小信差只早到一下下，", "擔心"), k("我怎麼來得及躲？", "句尾上揚", "S:gap"))

# ---------- 第二章：測站先聽到小信差 ----------
chief("chief-gap", C("raising her eyebrows with a knowing smile"),
      c("只靠你家感覺到的小信差，常常真的來不及。", "接住上一句"), c("所以要靠震央旁邊的測站。", None, "P:gap"), chapter="測站先聽到小信差")
kid("kid-station-q", K("tilting her head with a puzzled face, both hands out of frame", close=True),
    k("測站？是什麼東西？", "句尾上揚", "S:station"))
scene("station", "Close-up of a small sturdy plain smooth unmarked metal box half buried in green grass on a sunny hillside, a thin cable running from it into the ground, " + DAY,
      c("是一台放在地上、一直在聽地面動靜的機器。", None, "P:station"), c("台灣各地，放了很多很多台。"))
scene("stations-many", "Wide view of green hills and valleys on a sunny day with many small sturdy plain smooth unmarked metal boxes dotted across the grass, " + DAY,
      c("它們就像跑道旁邊的裁判。"), c("放得越密，就越容易有一台剛好在震央旁邊。"))
scene("station-first", "Close-up of a small sturdy plain smooth unmarked metal box in green grass, a thin small bright ripple glowing in the ground beside it, " + DAY,
      c("地震一開始，離震央最近的幾台測站，"), c("最先聽到小信差。"))
kid("kid-station-shout", K("standing on tiptoe with an excited face, both hands out of frame", where=LIVING),
    k("測站會大喊大家快躲嗎？", "很有把握的錯猜"))
scene("cable", "Wide view of green hills on a sunny day, a thin cable running across the grass from a small plain smooth unmarked metal box to a plain white building in the distance, a soft glow travelling along the cable, " + DAY,
      c("測站只負責聽，跟裁判一樣。"), c("它們馬上把小信差的樣子，傳給氣象署的電腦。"))
kid("kid-cwa", K("raising one hand high like answering in class, a bright face", where=LIVING),
    k("氣象署，是報天氣的那個？", "句尾上揚"))
scene("computer", "Medium shot of a big friendly plain smooth unmarked cabinet with rows of little coloured dots in a bright clean room, sunlight from a window, " + DAY,
      c("對，地震也是他們在看。"), c("電腦等不及所有測站都聽到，"), c("只用最先聽到的那幾台，就開始算。"))
kid("kid-hurry", K("laughing with a playful face, both hands out of frame", close=True),
    k("電腦好急喔，不等一下？", "好笑"))
scene("computer-dots", "Close-up of rows of little glowing coloured dots on a plain smooth unmarked cabinet, warm sunlight, " + DAY,
      c("不等。因為每過一秒，大個子都在往前跑。"))
kid("kid-what-see", K("squinting thoughtfully with a curious face, both hands out of frame", close=True),
    k("看小信差，能看出什麼？", "句尾上揚"))
scene("towns-estimate", "Wide view of many small towns spread over green hills on a sunny day, some towns glowing a soft warm orange and others calm, " + DAY,
      c("看出起點在哪裡、地震有多大，"), c("再估計大個子會跑到哪裡、搖得多兇。"))
kid("kid-instant", K("standing with both hands on her hips and a confident grin", where=LIVING),
    k("電腦一下子就算好了吧！", "很有把握的錯猜", "S:compute"))
chief("chief-takes-time", C("tilting her head with a gentle smile"),
      c("算也要時間。像二〇一六年的美濃地震，"), c("電腦大約十二秒，才算出第一次的答案。", None, "P:compute"))
kid("kid-12", K("gasping with a big surprised open mouth, both hands out of frame", close=True),
    k("十二秒，", "驚訝"), k("大個子不就跑很遠了？", "句尾上揚"))
scene("big-wave-far", "Wide cutaway view of the ground with green hills on top and a huge thick heavy band of rock bulging far away under distant hills, " + DAY,
      c("對，已經跑了四十幾公里。"), c("而且電腦只看到地震剛開始的那一小段。"))
kid("kid-wrong-q", K("biting her lip with a worried little frown", close=True),
    k("那它會不會算錯？", "句尾上揚", "S:estimate"))
chief("chief-estimate", C("holding one hand flat and tipping it a little with a thoughtful face"),
      c("它算的是估計，有時候會估不準。"), c("這件事你先記著，後面會用到。", "轉向觀眾"))
kid("kid-catch-q", K("clenching both fists with a determined face", where=LIVING),
    k("那警報要怎麼追上大個子？", "句尾上揚", "S:overtake"))

# ---------- 第三章：警報坐上電，超過大個子 ----------
scene("wires", "Wide view of tall power poles on green hills under a sunny sky, a glowing ribbon of light racing along the wires, " + DAY,
      c("警報不用自己跑，它是用電送出去的。", "接住上一句", "P:overtake"), c("電跑得比大個子，快很多很多倍。"), chapter="警報坐上電，超過大個子")
kid("kid-electric", K("throwing one fist up in the air with a big excited grin", where=LIVING),
    k("警報坐上電，跑贏大個子！", "恍然"))
scene("wire-close", "Close-up of a power line over green fields with a bright glowing ribbon of light zipping along it, " + DAY,
      c("對。電腦一算好，警報一下子就送出去。"), c("大個子還在路上，警報已經先到了。"))
kid("kid-if-fast", K("tilting her head with a curious squint, both hands out of frame", close=True),
    k("如果大個子也跑那麼快呢？", "句尾上揚"))
chief("chief-if-fast", C("raising her eyebrows with a playful smile"),
      c("那警報就永遠追不上了。"), c("警報能搶先，靠的就是大個子跑得慢。"))
kid("kid-how-phone", K("leaning in with both hands out of frame and curious eyes", close=True),
    k("電是怎麼跑到手機裡的？", "句尾上揚"))
scene("tower", "Wide view of a tall plain smooth unmarked grey antenna tower on a rooftop in a small sunny town, soft glowing rings spreading out from its top, " + DAY,
      c("警報送到附近的基地台，就是收手機訊號的天線，"), c("再從那裡，送給附近所有的手機。"))
kid("kid-broadcast", K("tilting her head with a curious face, both hands out of frame", where=LIVING),
    k("不用一個一個打電話？", "句尾上揚"))
scene("town-glow", "Wide view of a small sunny town where every house window glows soft orange at the same moment, " + DAY,
      c("不用。它是一次廣播，附近的手機同時收到。"))
kid("kid-loud-q", K("wincing with her shoulders pulled up and her eyes squeezed shut as two curved lines", close=True),
    k("可是那個聲音，", "皺臉"), k("為什麼要那麼大聲？", "句尾上揚", "S:loud"))
chief("chief-loud", C("nodding with a serious caring face", close=True),
      c("因為它要在幾秒鐘裡，叫醒所有人。", None, "P:loud"))
scene("phones-many", "Medium shot of many plain smooth unmarked smartphones glowing bright orange and vibrating together on a sunny wooden table, " + DAY,
      c("收到這種警報，手機預設會發出特別的警報聲，"), c("而且不能取消接收。"))
scene("phone-family", "Medium shot of a sunny family breakfast table with rice porridge bowls and several smartphones glowing bright orange at once, " + DAY,
      c("所以你們全家的手機，才會一起叫。"))
kid("kid-my-seconds", K("nodding hard with a bright face of understanding", where=LIVING),
    k("難怪手機先叫，", "恍然"), k("房子過幾秒才搖！", "恍然"))
chief("chief-my-seconds", C("smiling and nodding warmly", close=True),
      c("對，你家搶到的，就是那幾秒。", "轉向觀眾"))
kid("kid-every-q", K("squinting in thought with a curious face, both hands out of frame", close=True),
    k("每次地震，手機都會叫嗎？", "句尾上揚", "S:when"))
scene("town-quiet", "Wide view of a calm small town under a sunny sky where only a few houses glow soft orange and the rest stay quiet, " + DAY,
      c("不會。電腦要估計地震夠大，"), c("你住的地方又會搖得夠兇，手機才叫。", None, "P:when"))
kid("kid-my-house-q", K("pressing one hand to her own chest with a curious hopeful face", close=True),
    k("那我家能搶到幾秒？", "句尾上揚"))
chief("chief-far", C("leaning in with a friendly smile", close=True),
      c("要看你家離震央多遠。", "接住她的問題"), c("還記得大個子一秒跑多遠嗎？", "點名回呼"))
kid("kid-four-km", K("with a proud grin, both hands out of frame", close=True),
    k("大約一秒四公里！", "搶答"))
scene("road-far", "Wide view of a long straight country road across green fields to small houses far away, a huge thick heavy band in the ground rolling slowly beside the road, " + DAY,
      c("對。所以你家每離震央遠四公里，", "轉向觀眾"), c("大個子就晚大約一秒到。"))
kid("kid-far-more", K("spreading her arms wide with a delighted face", where=LIVING),
    k("住得越遠，時間越多！", "恍然"), k("那美濃地震的時候，台北呢？", "句尾上揚", "S:meinong"))
scene("city-far", "Wide view of a big city of plain smooth unmarked tall buildings in a green basin ringed by hills on a calm sunny morning, a glowing ribbon of light arriving along the power lines on the hills, " + DAY,
      c("台北離美濃很遠很遠，", None, "P:meinong"), c("警報可以比大搖晃早大約四十九秒。"))
kid("kid-49", K("with a thoughtful face, both hands out of frame", close=True),
    k("那離得越近，", "推理"), k("時間就越少嗎？", "句尾上揚"))
scene("towns-near-far", "Wide view of green countryside on a sunny day with small towns among the hills and a big city of plain smooth unmarked buildings far off, " + DAY,
      c("對，同一個地震，每個地方搶到的時間都不一樣。"))
kid("kid-near-q", K("tilting her head with a curious face, both hands out of frame", where=LIVING),
    k("那住在震央旁邊的人，", "好奇"), k("一定最早收到吧？", "句尾上揚", "S:near"))

# ---------- 第四章：警報追不上、估不準的時候 ----------
chief("chief-near", C("shaking her head gently with a kind serious face"),
      c("收到不一定最早，可是那裡最難搶到時間。", "接住上一句", "P:near"), chapter="警報追不上、估不準的時候")
scene("blind-village", UNDER + ", a small village of houses on the green ground and one bright glowing spot deep in the rock under it, the house roofs already tilting, " + DAY,
      c("電腦還在算的時候，大個子常常已經跑到那裡。"), c("開頭說有些人家先搖才收到警報，就是這裡。", "點名回呼"))
scene("blind-circle", "Wide view from a hill of a small village in green countryside with a soft pale circle of light drawn around it on the grass, " + DAY,
      c("這一圈警報趕不上的地方，叫做盲區。", None, "P:blind"))
kid("kid-blind", K("smiling with her eyes closed as two happy curved lines, both hands out of frame", close=True),
    k("盲區，就是看不見？", "句尾上揚"))
chief("chief-blind-see", C("smiling and nodding a little"),
      c("差不多，是警報還來不及照顧到的地方。"))
kid("kid-blind-p", K("holding very still with wide alert eyes, both hands out of frame", close=True),
    k("就像那天早上，", "想起來"), k("先輕輕的，是小信差？", "句尾上揚"))
scene("blind-tilt", "Medium shot of small cartoon houses on green grass with gently tilting roofs and leaning little trees, a soft glow in the ground under them, " + DAY,
      c("對，大個子可能就在後面。"), c("所以在那裡，搖晃本身就是警報。"))
kid("kid-far-sure", K("hugging a round cushion with a thinking face", where=LIVING),
    k("那住得遠的人，", "好奇"), k("就一定會收到嗎？", "句尾上揚"))
chief("chief-recall-est", C("raising one finger with a serious kind face", close=True),
      c("不一定。還記得電腦算的是估計嗎？", "點名回呼"), c("開頭說的台北那一次，是二〇二四年四月，", "點名回呼"))
scene("hualien", "Wide view of tall green mountains beside the blue sea on a sunny morning, a small city at the foot of the mountains, " + DAY,
      c("花蓮的大地震。地震開始後大約九秒，"), c("第一次警報就送出去了。"))
kid("kid-nine", K("clapping her hands once with a bright surprised face", where=LIVING),
    k("九秒！花蓮的人，", "驚喜"), k("一定都躲好了吧？", "句尾上揚"))
scene("hualien-town", "Medium shot of a small sunny town of low houses at the foot of tall green mountains, the roofs gently tilting, " + DAY,
      c("可是花蓮離震央很近，"), c("測到的幾個地方，大約只搶到五到十秒。"))
kid("kid-few-use", K("tilting her head with a doubtful face, both hands out of frame", close=True),
    k("才幾秒鐘，真的有用嗎？", "句尾上揚"))
chief("chief-few-use", C("nodding with a warm firm smile"),
      c("有用。幾秒鐘，也能先保護好自己。"))
kid("kid-few", K("frowning a little with a thinking face, both hands out of frame", close=True),
    k("那台北比較遠，", "推理"), k("應該搶到更多吧？", "句尾上揚"))
scene("road-long", "Wide view of a very long winding road from tall green mountains by the sea across green countryside to a big city far away, sunny sky, " + DAY,
      c("我們自己粗算：花蓮到台北，大約一百四十公里，"), c("大個子要跑大約三十五秒才到。"))
kid("kid-calc", K("closing her eyes tight in concentration with a determined little face", close=True),
    k("比九秒久好多，", "認真算"), k("台北一定來得及！", "開心"))
scene("city-calm", "Wide view of a big city of plain smooth unmarked tall buildings in a green basin ringed by hills on a calm sunny morning, " + DAY,
      c("照理說有機會。可是那天，電腦第一次把地震估得太小，", None, "P:estimate"), c("所以就沒有送警報給台北。"))
kid("kid-taipei-q", K("leaning in with wide worried eyes, both hands out of frame", close=True),
    k("台北的手機都沒響？", "句尾上揚"))
scene("city-shake", "Wide view of a big city of plain smooth unmarked tall buildings in a green basin ringed by hills on a sunny morning, the trees on the hills leaning hard, " + DAY,
      c("沒有。可是那天台北，真的搖得很厲害。", None, "P:taipei"))
kid("kid-taipei-scared", K("hugging a round cushion tightly with a startled face", where=LIVING),
    k("台北的人一定嚇一跳！", "擔心"))
chief("chief-taipei-felt", C("nodding slowly with a kind serious face", close=True),
      c("對，很多人是先覺得在搖，才知道地震來了。"))
kid("kid-update-q", K("frowning with her arms crossed", where=LIVING),
    k("電腦後來有改嗎？", "句尾上揚"))
scene("computer-again", "Medium shot of a big friendly plain smooth unmarked cabinet with rows of little coloured dots glowing a little brighter in a bright clean room, " + DAY,
      c("有。大約十五秒的時候，它又算了一次，"), c("把地震估大一點，台北只差一點點，還是沒收到。"))
kid("kid-wait-q", K("squinting with a puzzled face, both hands out of frame", close=True),
    k("那為什麼不等久一點，", "不解"), k("算準一點再送？", "句尾上揚"))
chief("chief-wait", C("tilting her head with a thoughtful smile"),
      c("等越久，大個子就跑越遠，"), c("大家搶到的時間就越少。"))
scene("towns-glow", "Wide view of many small towns across green hills on a sunny day, most of them glowing a soft warm orange at the same moment, " + DAY,
      c("所以後來氣象署也改了規則：很大的地震，"), c("搖得沒那麼兇的地方，也會收到警報。"))
kid("kid-miss", K("hugging her knees and looking down with a thoughtful face", where=LIVING),
    k("原來警報也會漏掉……", "若有所思"))
chief("chief-helper", C("smiling warmly at the viewer with one hand on her chest", close=True),
      c("警報是你很好的幫手，可是它是估出來的。", "轉向觀眾"))
kid("kid-what-do-q", K("looking up with a serious little face, both hands out of frame", close=True),
    k("手機沒響，可是我覺得在搖，", "認真"), k("那要怎麼辦？", "句尾上揚", "S:noalert"))

# ---------- 收尾 ----------
# The drop-cover-hold lines play over the kid at the table: the chief never acts the pose out (review-script-score).
kid("kid-drop", K("crouching low beside " + TABLE + " holding onto one of its legs, a brave serious face", where=LIVING),
    c("不用等手機。聽到警報，或是覺得在搖，", "接住上一句"), c("都馬上趴下、掩護、穩住。", "清楚，一個字一個字", "P:noalert"), chapter="小問自己破案")
kid("kid-drop-under", K("peeking out from under " + TABLE + " with a calm brave face, her head tucked low", close=True),
    c("趴低，才不會被搖倒；掩護，是護住頭和脖子；"), c("穩住，就是抓好不放，等搖晃停下來。"))
kid("kid-drop-say", K("sitting on the floor after the shaking, giving a small thumbs-up with a proud smile", where=LIVING),
    k("趴下、掩護、穩住！", "認真"), c("對，也不要急著往外跑。"))
scene("bed", "Medium shot of a cosy bed with a fluffy pillow and a soft blanket in a sunny bedroom, " + DAY,
      c("如果你在床上，就待在床上，翻身趴下。"))
chief("chief-back", C("smiling warmly at the viewer with one hand open, filling the frame", close=True),
      c("還記得你一開始問我的嗎？你自己說說看。", "笑"))
kid("kid-got1", K("throwing both arms up with a huge happy smile", where=LIVING),
    k("地震一開始，", "篤定"), k("測站先聽到小信差，", "篤定"))
kid("kid-got2", K("pointing proudly up with one finger and a big grin", close=True),
    k("電腦算好，警報坐上電，", "開心"), k("就跑贏大個子了！", "開心", "P:main"))
kid("kid-got3", K("nodding firmly with her arms folded and a serious little face", where=LIVING),
    k("可是震央旁邊會來不及，", "認真"), k("電腦也可能估錯！", "認真"))
chief("chief-done", C("smiling warmly at the viewer with her hands clasped", close=True),
      c("對，就是這樣！下次手機大叫，", "轉向觀眾，輕聲"), c("大個子可能還在路上，馬上保護自己。", "點名回呼"))
# The outro is three pictures, no card, no stamp (series README §3.2, §10.1): the kid gives a thumbs-up.
kid("outro", "Head-and-shoulders close-up of the girl with a big happy smile giving a big cheerful thumbs-up with one hand, bright morning light",
    k("原來如此！", "開心大聲"))
chief("outro-chief", "Waist-up medium shot of the chief tilting her head with a curious smile and one hand open, filling the frame, a plain pale wall behind her, bright morning light",
      c("看影片的你呢？你被地震警報嚇過嗎？", "問句上揚，像聊天"), c("留言告訴我們。"))
chief("outro-wave", "Waist-up medium shot of the chief waving goodbye with a warm smile, a plain pale wall behind her, bright morning light",
      c("想一起找生活裡的為什麼，就訂閱原來如此事務所。", "誠懇"))

# ---------- assemble ----------
WHAT = {"main": "地震已經開始了，警報怎麼還能搶在大搖晃前面", "order": "為什麼先輕輕搖，再一下子大搖",
        "blind": "為什麼有些人家，大搖晃比警報還早到", "taipei": "哪一次大地震台北搖得很厲害，手機卻沒響",
        "whole": "地震一開始，是不是全台灣一起搖", "speed": "小信差和大個子跑得多快",
        "gap": "小信差只早到一下下，怎麼來得及躲", "station": "測站是什麼",
        "compute": "電腦是不是一下子就算好", "estimate": "電腦會不會算錯",
        "overtake": "警報要怎麼追上大個子", "loud": "警報聲為什麼那麼大聲",
        "when": "每次地震手機都會叫嗎", "meinong": "美濃地震時，台北搶到多少時間",
        "near": "住在震央旁邊的人是不是最早收到", "noalert": "手機沒響卻覺得在搖，要怎麼辦"}
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
    "target_minutes": [11, 13], "voice": VOICE, "subtitles": {"burn_in": False}, "theme": "paper", "look": {"preset": "cute-cartoon"},
    # The series tag: the approved character sheets live in the series store and every episode reuses them (docs/videos/SERIES.md).
    "series": {"slug": "sothatswhy", "episode": 23, "chapter": 1},
    # The series bed: the same paid Lyria take as P02-P14 (P02 backup music/e4225993d121c03b.mp3), rebuilt on
    # 2026-11-07 with P02's recipe because the original bed file was in no backup (tail cut at 175.15 s,
    # five copies with 3 s crossfades, 863.75 s). Nothing new was generated.
    "music": {"track": "sothatswhy-bed-r2.m4a", "sha256": "9bb4ba6fd16feb4a7f352144b2d89e9648acbbbbaa2173c27a7eefbdb70f28c6", "gain_db": -20, "duck_db": -10},
    "characters": CHARACTERS, "loops": loops,
    "youtube": {
        "category_id": 27, "made_for_kids": False, "default_language": "zh-TW",
        "title": "地震已經發生，警報怎麼還能搶先？｜原來如此事務所",
        "description": "小問吃早餐時，媽媽的手機突然大叫；過了幾秒，房子才開始搖。手機怎麼會比地震還早知道？它是在預測地震嗎？\n\n"
                       "這一集，所長和小問把地震想成一場從地底開始的賽跑：跑得快、搖得輕的小信差（P波），跑得慢、搖得兇的大個子（S波），"
                       "跑道旁邊聽見小信差的測站，還有坐上電、跑贏大個子的地震警報。也一起看看為什麼震央旁邊常常來不及，"
                       "以及二〇二四年花蓮大地震時，台北搖得很厲害、手機卻沒響。\n\n"
                       "地震警報不是預測：它是地震已經開始以後，電腦用最早的資料估計出來的，可能估不準，也可能來不及。"
                       "聽到警報，或是覺得在搖，都馬上趴下、掩護、穩住，不用等手機。\n\n"
                       "本集插圖由 AI 生成，畫的是示意，不是量測。片中的速度、秒數都是氣象署與研究裡的大約數字，每次地震都不一樣。"
                       "每個說法的出處列在下方參考資料。\n\n資料截至 " + CHECKED,
        "tags": ["地震", "地震警報", "國家級警報", "強震即時警報", "P波", "S波", "科普", "原來如此事務所"],
        "video_id": None},
    "thumbnail": {"template": "thumb", "data": {"headline": "地震已經開始\n**警報還能搶先**", "sub": "警報坐上電，跑贏大搖晃", "shot": "kid-phone-blare"}},
    "sources": [
        {"title": "中央氣象署 地震測報中心：常見問答 84（強震即時警報）", "url": "https://scweb.cwa.gov.tw/zh-tw/guidance/faqdetail/98", "checked_on": CHECKED},
        {"title": "中央氣象署 地震測報中心：強震即時警報原理", "url": "https://scweb.cwa.gov.tw/zh-tw/guidance/eew/3", "checked_on": CHECKED},
        {"title": "中央氣象署 地震測報中心：常見問答 21（地震波）", "url": "https://scweb.cwa.gov.tw/zh-tw/guidance/faqdetail/21", "checked_on": CHECKED},
        {"title": "中央氣象署 地震百問（兒童版）：地震波", "url": "https://edu.cwa.gov.tw/PopularScience/kids/ec/ec_9.html", "checked_on": CHECKED},
        {"title": "中央氣象署：地震速報 App 說明", "url": "https://www.cwa.gov.tw/V8/C/S/eservice/app/app_e.html", "checked_on": CHECKED},
        {"title": "中央氣象署 地震測報中心：PWS 地震速報", "url": "https://scweb.cwa.gov.tw/zh-tw/pws/info_d/2", "checked_on": CHECKED},
        {"title": "USGS: Earthquake Early Warning – Overview", "url": "https://www.usgs.gov/programs/earthquake-hazards/science/earthquake-early-warning-overview", "checked_on": CHECKED},
        {"title": "報導者：0403 花蓮地震，國家級警報為什麼沒響", "url": "https://www.twreporter.org/a/taiwan-0403earthquake", "checked_on": CHECKED},
        {"title": "公視新聞網：地震國家級警報新制（2024-08-30）", "url": "https://news.pts.org.tw/article/712421", "checked_on": CHECKED},
        {"title": "Lin & Chen, SSA 2024 abstract: EEW performance for the 2024 Hualien earthquake", "url": "https://seismosoc.secure-platform.com/a/solicitations/35/sessiongallery/1056/application/11871", "checked_on": CHECKED},
        {"title": "內政部：115 年國家防災日（趴下、掩護、穩住）", "url": "https://www.moi.gov.tw/News_Content.aspx?n=2&s=340709", "checked_on": CHECKED},
        {"title": "臺中市政府教育局轉載消防署：地震避難", "url": "https://tc.edu.tw/page/eba0fe24-e3d1-4d56-9953-5fe5796f71d1/unit-doc-content?id=4580", "checked_on": CHECKED},
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
