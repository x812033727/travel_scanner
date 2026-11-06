"""Generate video.json for sothatswhy-p07-fridge-door (原來如此事務所 對話版 P07).

Run `python3 build_scenes.py` from anywhere: it rewrites video.json next to this file and freezes
every shot's camera move in cameras.json (a shot keeps the camera it was first given, so deleting
a shot never shifts the others: the camera is in the keyframe cache key).
Edit lines and prompts here, never in video.json.
"""
import itertools, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = "sothatswhy-p07-fridge-door"
CHECKED = "2026-11-06"

# ---------- series constants ----------
# Both characters are identical to P14 (approved series sheets reused through the `series` tag):
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
FRIDGE = "a plain white two-door refrigerator"
BALCONY = "on a sunny apartment balcony with potted plants"
BEDROOM = "in a bright sunny bedroom"
# The floor plan the chief keeps redrawing: heat is red balls, electricity is yellow lightning bolts,
# the boundary is a dashed yellow loop (the plan in EPISODES.md P07: one plan, a wider loop each time).
PLAN = "Top-down flat floor plan of a small square kitchen seen from straight above, a white refrigerator standing against one wall, a pale wooden floor"
# Prompt words that P02/P05 taught us to keep out (README §3.1): the model has no negative prompt,
# lamps and night turn frames into 3D figurines, and these props sprout fake letters.
BANNED = re.compile(r"\b(no|not|without|text|blank|lamp|night|notebook|sign|signs|paper|poster|screen|book|calendar|whiteboard|thermometer|remote|label|magnet)\b", re.I)

CAMS = itertools.cycle(["push in", "pan left", "pull out", "drift", "tilt up", "pan right", "push in", "tilt down", "pull out", "drift"])
CAM_FILE = os.path.join(HERE, "cameras.json")
FROZEN = json.load(open(CAM_FILE, encoding="utf-8")) if os.path.exists(CAM_FILE) else {}

S = []
def _shot(id, prompt, chars, lines, chapter):
    assert not BANNED.search(prompt), (id, BANNED.search(prompt).group(0))
    assert id not in {s["id"] for s in S}, id
    cam = FROZEN.get(id) or next(CAMS)
    S.append(dict(id=id, chapter=chapter, template="shot", data=dict(prompt=prompt, camera=cam, visual="still", characters=list(chars)), lines=list(lines)))
def kid(id, prompt, *lines, chapter=None):
    """The kid doing one simple thing, facing the camera, waist-up or head-and-shoulders."""
    _shot(id, prompt.rstrip(". ") + ", " + KIDDESC, ["kid"], lines, chapter)
def chief(id, prompt, *lines, chapter=None):
    """The chief, always waist-up or head-and-shoulders, in front of a plain wall in daylight."""
    assert prompt.startswith(("Waist-up", "Head-and-shoulders")), id
    _shot(id, prompt.rstrip(". ") + ", " + CHIEFDESC, ["chief"], lines, chapter)
def scene(id, prompt, *lines, chapter=None):
    """No character: an object, a place or a mechanism drawn as a picture."""
    _shot(id, prompt, [], lines, chapter)
def k(t, e=None, tag=None): return ("kid", t, e, tag)
def c(t, e=None, tag=None): return ("chief", t, e, tag)

def C(action, close=False):
    return ("Head-and-shoulders close-up" if close else "Waist-up medium shot") + " of the chief " + action + ", " + WALL + ", " + DAY
def K(action, close=False, where=None):
    return ("Head-and-shoulders close-up" if close else "Waist-up medium shot") + " of the girl " + (where + " " if where else "") + action + ", " + DAY

# ---------- 開場（系列片頭之後直接進場景，不做濃縮；答案都不先講）----------
kid("fridge-open", K("holding the door of " + FRIDGE + " wide open with cool mist drifting onto her happy face", where=KITCHEN),
    k("所長！今天熱到不行，", "興奮，跑進來報案的語氣"), k("我把冰箱門一打開，", "得意"), k("臉馬上涼涼的！", "開心"), chapter="熱天下午，冰箱門開著")
kid("kid-idea", K("raising one finger with sparkling eyes and a clever grin", close=True, where=KITCHEN),
    k("我想到一個好方法！", "神秘"), k("冰箱門整天開著，", "得意"), k("廚房就不用開冷氣了！", "很有把握的錯猜"))
chief("chief-wait", C("raising one hand gently with an amused smile"),
      c("先別急著拔冷氣的插頭。", "笑"), c("你也可以猜猜看：冰箱門一直開著，", "轉向觀眾"), c("廚房會變涼，還是反而變熱？", "賣關子，問句", "S:room"))
kid("kid-hotter", K("with her mouth open in a shocked O, both hands on her cheeks", close=True),
    k("變熱？", "大驚"), k("冰箱明明是冷的耶！", "不服氣"))
chief("chief-back-tease", C("pointing to one side with a knowing smile"),
      c("那你走過冰箱旁邊時，把手靠近它的背後。", "轉向觀眾"), c("那裡摸起來，可一點都不冷。", "賣關子", "S:back"))
kid("kid-back-guess", K("peeking sideways around the edge of " + FRIDGE + " with a curious frown", where=KITCHEN),
    k("冰箱後面，", "疑惑"), k("藏了什麼東西？", "句尾上揚"))
scene("outdoor-unit", "Medium shot of a white outdoor air conditioner unit with a big round fan grille mounted on a sunny apartment balcony wall beside potted plants, " + DAY,
      c("還有你家陽台上，那台嗡嗡轉的大箱子，", "賣關子"), c("它吹出來的風，你猜是冷的還是熱的？", "問句", "S:outdoor"))
kid("kid-outdoor-guess", K("on a sunny balcony pointing at a white outdoor air conditioner unit with a confident grin"),
    k("冷氣的箱子，", "很有把握"), k("吹的一定是冷風吧？"))
chief("chief-promise", C("folding her arms with a warm smile", close=True),
      c("這些問題的答案，都藏在同一台冰箱裡。"), c("我們就盯著它，一路跟著它的熱走。"))

# ---------- 第一章：先只看冰箱裡面 ----------
kid("kid-cold-out", K("standing at the open door of " + FRIDGE + " scooping the cool air toward herself with both hands", where=KITCHEN),
    k("冰箱裡面裝滿了冷，", "很有把握的錯猜"), k("門一開，冷就跑出來了！", None, "S:coldthing"), chapter="冰箱裡少掉的熱")
chief("chief-tea", C("holding a steaming cup of hot tea in both hands"),
      c("先來看一杯熱茶。"), c("你把它放在桌上，過一陣子會怎樣？", "轉向觀眾"))
kid("kid-tea", K("touching the side of a cup of tea on a wooden table with one fingertip, a thoughtful face", close=True),
    k("會變溫溫的。", "想一想"), k("熱跑掉了！"))
scene("ice-cube", "Close-up of one ice cube melting into a small puddle in a little glass dish on a sunny wooden kitchen table, " + DAY,
      c("那一顆冰塊放在桌上呢？"), k("會慢慢融化。", "搶答"))
chief("chief-heat-flow", C("moving one hand slowly from high to low like something flowing downhill"),
      c("冰塊融化，是旁邊空氣的熱跑進了冰塊。"), c("熱自己走，只會從熱的地方，跑到冷的地方。"))
kid("kid-cold-run", K("tilting her head with a puzzled frown and one finger on her chin", close=True),
    k("那冷呢？", "追問"), k("冷不會自己跑嗎？", "句尾上揚"))
chief("chief-cold-less", C("lowering one flat hand a little with a calm smile", close=True),
      c("我們說的冷，其實就是熱比較少。", "放慢", "P:coldthing"), c("冷不是一種會跑出來的東西。"))
kid("kid-face-cool", K("standing at the open door of " + FRIDGE + " with her eyes closed and a small smile, cool mist on her cheeks", where=KITCHEN),
    k("那我的臉，", "追問"), k("怎麼會涼涼的？"))
chief("chief-face", C("touching her own cheek lightly with a gentle smile", close=True),
      c("冰箱裡的冷空氣流出來，碰到你的臉，"), c("你臉上的熱就跑進那團冷空氣裡。"))
kid("kid-stolen", K("holding both hands on her cheeks and laughing", close=True),
    k("我的熱被偷走了！", "好笑"))
chief("chief-circle", C("drawing a big circle in the air with one finger and a playful smile"),
      c("要抓這個小偷，我們來畫一個圈。"), c("圈裡面的熱，多了少了，我們都記下來。"))
scene("plan-inside", PLAN + ", a dashed yellow loop drawn tightly around only the inside of the refrigerator, the inside of the refrigerator tinted pale icy blue, a few small round red balls scattered across the warm kitchen floor, " + DAY,
      c("我把熱畫成一顆顆紅色的小球。"), c("先圈住冰箱的裡面就好。"))
scene("fridge-shelves", "Close-up of fresh green vegetables and a bowl of red apples on clear glass shelves inside a cold white refrigerator with a faint frosty glow, " + DAY,
      c("冷藏的那幾層，大約只有三到五度，", "數字放慢"), c("比夏天的廚房，冷了一大截。"))
scene("freezer", "Close-up of a frosty pull-out freezer drawer full of ice cube trays and frozen green peas, cold white mist drifting out, " + DAY,
      c("那下面的冷凍庫，你猜有多冷？", "轉向觀眾"), c("多半在零下十八度，甚至更冷。", "數字放慢"))
kid("kid-freezer", K("hugging herself and shivering in front of an open frosty freezer drawer, a puff of cold mist at her mouth", close=True, where=KITCHEN),
    k("零下十八度！", "大驚"), k("比台灣的冬天冷多了！"))
chief("chief-gap", C("holding one hand high and one hand low, a thoughtful face"),
      c("裡外差得越多，熱就越急著往裡面鑽。"))
kid("kid-sneak", K("crouching beside " + FRIDGE + " and peering closely at the gap around its closed door", where=KITCHEN),
    k("廚房的熱，", "推理"), k("會想鑽進冰箱裡？"))
chief("chief-sneak", C("nodding with raised eyebrows"),
      c("會。照剛剛那條規矩，熱一定往冷的地方跑。"), c("可是冰箱的門，擋了它一下。"))
kid("kid-door-thick", K("opening " + FRIDGE + " and pressing the soft grey rubber strip around the edge of the thick door with one finger", where=KITCHEN),
    c("你打開冰箱門，摸摸它的邊，", "轉向觀眾"), c("門又厚又重，邊上還有一圈軟軟的膠條。"))
kid("kid-thermos", K("hugging a round steel thermos bottle and grinning", close=True),
    k("跟保溫瓶一樣厚！", "發現"))
chief("chief-insulate", C("pressing her palms together as if closing a door, a calm smile"),
      c("對，門和牆裡都塞了擋熱的材料。"), c("這叫做隔熱，讓熱跑得慢一點。"))
chief("chief-door-later", C("tapping the side of her glasses with a knowing smile", close=True),
      c("這道厚厚的門，你先記著，等一下它會回來。", "前向鉤子", "S:door"))
kid("kid-slow", K("frowning and holding her two hands close together as if squeezing through a tiny gap", close=True),
    k("只是慢一點？", "抓到問題"), k("那熱還是會溜進去？", "句尾上揚"))
chief("chief-must-carry", C("holding one hand up as if carrying something small out of a box"),
      c("會。冰箱裡卻一直那麼冷，"), c("就表示有東西，一直把熱搬出去。"))
scene("plan-inside-out", PLAN + ", a dashed yellow loop around only the inside of the refrigerator, small round red balls floating out through the wall of the loop toward the back of the refrigerator, " + DAY,
      c("圈裡的熱，一顆一顆被送出圈外。"))
kid("kid-where-q", K("looking around the sunny kitchen over her shoulder with wide curious eyes", where=KITCHEN),
    k("那些熱，", "追問"), k("被搬去哪裡了？", "章尾停住，句尾上揚", "S:where"))

# ---------- 第二章：走到冰箱背後 ----------
kid("kid-eat-heat", K("pretending to munch with puffed cheeks beside " + FRIDGE, close=True, where=KITCHEN),
    k("會不會是冰箱，", "很有把握的錯猜"), k("把熱吃掉了？", None, "S:vanish"), chapter="冰箱背後熱熱的")
chief("chief-vanish", C("shaking her head gently with a kind smile"),
      c("熱不會憑空變不見，只會換個地方待。", None, "P:vanish"), c("不信，你繞到冰箱的後面看看。"))
kid("kid-behind", K("holding her open palm near the back of " + FRIDGE + " pulled a little away from the wall, her eyes wide in surprise", where=KITCHEN),
    k("咦？後面暖暖的！", "驚訝"), k("有一股熱熱的風！"), c("手靠近就好，背後有電線，別伸進去亂摸。", "叮嚀"))
scene("coils", "Close-up of black zigzag metal pipes on the back of a white refrigerator, faint warm shimmering air rising from them, small round red balls drifting up into the sunny kitchen, " + DAY,
      c("冰箱背後這一排彎彎的管子，摸起來是溫的。"), c("冰箱裡少掉的熱，就是從這裡吐回廚房。", None, "P:back"))
kid("kid-moved", K("pointing back and forth between the inside and the back of " + FRIDGE + " with an excited grin", where=KITCHEN),
    k("原來熱被搬到後面了！", "想通", "P:where"))
chief("chief-feet", C("pointing down toward her feet with a playful smile", close=True),
      c("有的冰箱，還會從底下吹出溫溫的風，"), c("你站在它前面，腳邊有沒有被吹過？", "轉向觀眾"))
kid("kid-feet", K("looking down at her white sneakers in surprise as warm air ruffles her socks", close=True, where=KITCHEN),
    k("腳暖暖的，", "驚訝"), k("臉涼涼的！"))
kid("kid-no-hands", K("holding up both open hands with a puzzled shrug", close=True),
    k("可是冰箱又沒有手，", "不解"), k("它怎麼搬熱？", "句尾上揚"))
chief("chief-refrigerant", C("tracing a big loop in the air with one finger"),
      c("冰箱的管子裡，有一種會繞圈子跑的東西，"), c("叫做冷媒。"))
kid("kid-refrigerant-q", K("squinting at a thin silver pipe she holds up in one hand", close=True),
    k("冷媒？", "好奇"), k("它本身是冷的嗎？", "句尾上揚"))
chief("chief-shower-back", C("raising one finger with a playful smile"),
      c("它不一定冷，但它會變身。你洗完熱水澡，", "接住"), c("濕濕地走出浴室，是不是會冷得發抖？", "轉向觀眾"))
kid("kid-towel2", K("wrapped in a big fluffy towel, wet hair, rubbing her arms to warm up", close=True),
    k("會！明明洗的是熱水！", "用力點頭"), c("你身上的水，變成水氣飛走的時候，"), c("會順手把你身上的熱帶走。"))
kid("kid-wet-cold", K("nodding hard with her arms crossed tight, a wet strand of hair on her forehead", close=True),
    k("所以濕濕的才會冷！", "恍然大悟"))
scene("evaporate", "Close-up cutaway of a thin silver pipe running along the inside back wall of a cold refrigerator, tiny bubbles of vapour forming inside the pipe, small round red balls drifting from the cold shelves into the pipe, " + DAY,
      c("冷媒在冰箱裡面，也是從液體變成氣體，"), c("把裡面的熱，一起帶進管子裡。"))
kid("kid-boil-q", K("peering into a cold open refrigerator with a doubtful frown", close=True, where=KITCHEN),
    k("冰箱裡那麼冷，", "懷疑"), k("冷媒也能變成氣體？", "句尾上揚"))
chief("chief-low-boil", C("nodding with a small smile and one finger raised"),
      c("能。冷媒是特別挑過的液體，很容易沸騰，"), c("冰箱裡那一點熱，就夠它變成氣體。"))
kid("kid-cold-boil", K("with her mouth open in amazement and both hands up", close=True),
    k("冰冰的還會沸騰？", "驚奇"), k("好奇怪的液體！"))
kid("kid-gas-where", K("following an imaginary pipe through the air with one pointing finger", close=True),
    k("帶著熱的氣體，", "追問"), k("接著跑去哪？", "句尾上揚"))
scene("compressor", "Close-up of a small round black metal compressor sitting low at the back corner of a white refrigerator, two thin copper pipes coming out of it, " + DAY,
      c("它跑進一顆圓圓的馬達裡。"), c("這顆馬達叫做壓縮機。"))
chief("chief-squeeze", C("squeezing her two hands together hard as if pressing a ball"),
      c("壓縮機把冷媒的氣體，擠得緊緊的。"), c("被擠緊的冷媒，流進背後那排管子，"))
scene("condense", "Close-up cutaway of the black zigzag pipes on the back of a white refrigerator, drops of liquid forming inside the pipes, small round red balls leaving the pipes into the sunny kitchen air, " + DAY,
      c("在那裡變回液體，把帶來的熱交給廚房。"), c("然後它再流回冰箱裡面，重新跑一圈。"))
kid("kid-train", K("pushing a little toy train around a circle of track on the kitchen floor, laughing", where=KITCHEN),
    k("像一台搬熱的小火車！", "開心"))
chief("chief-train", C("nodding and laughing softly", close=True),
      c("很像。一圈又一圈，把熱從裡面載到外面。"))
kid("kid-wall-q", K("pushing " + FRIDGE + " tight against the kitchen wall with both hands, a curious face", where=KITCHEN),
    k("那冰箱的背後，", "追問"), k("可以緊緊貼著牆嗎？", "句尾上揚", "S:wall"))
chief("chief-wall", C("holding her two hands a little apart, side by side, with a kind smile"),
      c("最好別貼死。背後留一點空隙，熱才散得出去，", None, "P:wall"), c("管子上積的灰塵，也要記得清。"))
kid("kid-wall", K("pulling " + FRIDGE + " a little away from the wall and smiling", where=KITCHEN),
    k("熱也要有路可以走！", "想通"))
kid("kid-plug", K("crouching beside " + FRIDGE + " and pointing at its white plug in the wall socket", where=KITCHEN),
    k("小火車要有人推吧？", "追問"))
chief("chief-electric", C("holding up one hand with fingers spread like a little spark, a calm smile"),
      c("推它的就是電。把氣體擠緊很費力，"), c("壓縮機要一直吃電，才轉得動。"))
scene("plan-bolt", PLAN + ", one bright yellow lightning bolt running along the power cord from the wall socket into the refrigerator, " + DAY,
      c("電，我們就畫成黃色的小閃電。"))
chief("chief-thermostat", C("tilting one hand side to side with a gentle smile"),
      c("它也不是一直跑：冰箱裡一變暖，它就開工，"), c("夠冷了，就停下來休息。"), k("難怪它有時候安安靜靜！", "發現"))
kid("kid-motor-q", K("crouching and peering at the small black compressor at the back of " + FRIDGE + " with a curious face", where=KITCHEN),
    k("那它吃進去的電，", "追問"), k("最後跑去哪了？", "句尾上揚", "S:motor"))
kid("kid-ledger-q", K("holding up both hands like a balance scale with a thinking face", close=True),
    k("還有，背後吐出來的熱，", "推理"), k("跟裡面搬出來的，", ), k("一樣多嗎？", "章尾停住，句尾上揚", "S:ledger"))

# ---------- 第三章：把整間廚房畫進圈裡 ----------
chief("chief-bigger", C("spreading both arms wide as if drawing a huge circle"),
      c("要回答這兩個問題，圈得畫大一點，"), c("把整間廚房都圈進來。"), chapter="把整間廚房圈起來")
scene("plan-room", PLAN + ", a big dashed yellow loop drawn around the whole kitchen, the refrigerator inside the loop, small round red balls and one yellow lightning bolt inside the loop, " + DAY,
      c("冰箱、冰箱背後、你站的地方，"), c("現在全在同一個圈裡。"))
chief("chief-suppose", C("holding up two fingers with a calm smile", close=True),
      c("我們先假設一組好算的數字："), c("冰箱從裡面搬出兩顆紅球的熱，", "數字放慢"))
chief("chief-one-bolt", C("holding up one finger with raised eyebrows"),
      c("壓縮機做這件事，吃了一份電。"))
kid("kid-guess-count", K("counting on her fingers with her tongue sticking out in concentration", close=True),
    k("背後會吐出幾顆？", "追問"))
scene("two-plus-one", "Close-up of two small round red balls and one bright yellow lightning bolt flowing together into the back of a white refrigerator and coming out as three small round red balls, a pale kitchen wall, " + DAY,
      c("三顆。搬出來的兩顆，加上一顆。", None, "P:ledger"), c("那一顆，就是壓縮機吃進去的電變的。", None, "P:motor"))
kid("kid-more", K("with her mouth wide open in surprise, holding up three fingers", close=True),
    k("吐出來的比搬出來的多！", "大驚"))
chief("chief-energy", C("nodding slowly with her hands open"),
      c("對。電用完不會變不見，最後也變成熱。"))
kid("kid-closed-q", K("leaning her back against the closed door of " + FRIDGE + " with a thinking face", where=KITCHEN),
    k("那門關著的時候呢？", "追問", "S:closed"))
chief("chief-closed", C("sliding one hand slowly forward as if something is sneaking in"),
      c("門關著，從牆和門邊慢慢溜進去的那些熱，"), c("冰箱照樣把它們搬出來，加上電，吐回廚房。"))
kid("kid-closed", K("holding her finger and thumb a tiny bit apart with raised eyebrows", close=True, where=KITCHEN),
    k("所以就算門關著，", "推理"), k("廚房也會熱一點點？", "句尾上揚"))
chief("chief-closed2", C("nodding with a warm smile", close=True),
      c("對，冰箱只要在跑，廚房就被它加熱了一點點。", None, "P:closed"))
kid("kid-open-again", K("pulling open the door of " + FRIDGE + " wide and holding it with a curious face", where=KITCHEN),
    k("那我把門打開，", "試探"), k("會怎樣？", "句尾上揚"))
scene("plan-loop", PLAN + ", a big dashed yellow loop around the whole kitchen, the refrigerator door standing wide open, small round red balls circling in a loop from the kitchen floor into the open door and out of the back of the refrigerator again, " + DAY,
      c("廚房的熱，從門口一直灌進冰箱，"), c("冰箱再把它們搬到背後，吐回廚房。"))
kid("kid-circle", K("spinning one finger round and round in the air with a dizzy grin", close=True),
    k("熱在繞圈圈！", "好笑"))
chief("chief-zero", C("drawing a small circle in the air and then pointing at it"),
      c("對，那兩顆熱，只是在圈裡轉來轉去，"), c("廚房的熱，一顆也沒有少。"))
scene("plan-extra", PLAN + ", a big dashed yellow loop around the whole kitchen, the refrigerator door wide open, one bright yellow lightning bolt entering the refrigerator along its power cord and turning into one extra small round red ball that joins the others on the floor, " + DAY,
      c("可是每轉一圈，那道小閃電，"), c("就在圈裡多變出一顆熱。"))
kid("kid-answer", K("slowly lowering the door of " + FRIDGE + " with a stunned face", where=KITCHEN),
    k("所以門開著，", "慢慢想通"), k("廚房反而變熱了！", None, "P:room"))
kid("kid-but-cool", K("standing at the open door of " + FRIDGE + " with cool mist on her face and a stubborn pout", where=KITCHEN),
    k("可是我站在門口，", "不服氣"), k("真的涼涼的啊！", None, "S:front"))
chief("chief-front", C("holding her two hands a little apart to show a small space, a kind smile", close=True),
      c("沒錯，門口前面那一小塊，是會涼一點。", None, "P:front"), c("可是你一走開，那塊涼就跟你沒關係了。"))
chief("chief-harder", C("wiping her brow with the back of one hand as if tired, a wry smile"),
      c("而且門一開，冰箱裡面一直變暖，"), c("壓縮機就停不下來，一直吃電。"))
kid("kid-tired", K("patting the side of " + FRIDGE + " with a sympathetic face", where=KITCHEN),
    k("冰箱好累喔！", "心疼"))
chief("chief-more-heat", C("raising her hand higher and higher in steps"),
      c("吃的電越多，多變出來的熱也越多。"), c("你家的電費，也跟著一起變多。", "轉向觀眾"))
kid("kid-heater-q", K("rubbing her hands together in front of a small electric heater glowing orange", where=BEDROOM),
    k("那開著門的冰箱，", "推理"), k("像冬天用的電暖器？", "句尾上揚"))
chief("chief-heater", C("smiling and giving a small thumbs up", close=True),
      c("算起帳來很像：它吃進去的電，"), c("最後都變成熱，留在廚房裡。"))
chief("chief-opinion", C("folding her arms and laughing softly"),
      c("我覺得這是冰箱最會騙人的地方：", "意見，輕鬆"), c("它是一台搬熱的機器，不是做冷的機器。"))
kid("kid-trick", K("narrowing her eyes at " + FRIDGE + " like a detective, one finger raised", where=KITCHEN),
    k("冰箱騙了我！", "像偵探"))
kid("kid-ac-q", K("looking up at a white wall-mounted air conditioner blowing cool air, her hair fluttering, a puzzled frown", where=BEDROOM),
    k("那冷氣呢？", "推理"), k("冷氣也是搬熱的機器嗎？", "句尾上揚"))
chief("chief-ac-same", C("nodding with her hands open, a calm smile", close=True),
      c("是。冷氣和冰箱，是同一種機器。"), c("它也有冷媒、也有壓縮機，也一樣吃電。"))
kid("kid-ac-why", K("fanning herself under a cool breeze from a wall-mounted air conditioner, her brow knitted", close=True, where=BEDROOM),
    k("那開冷氣，", "不解"), k("房間怎麼就會變涼？", "章尾停住，句尾上揚", "S:acwhy"))

# ---------- 第四章：冷氣把熱的那一頭放到外面 ----------
chief("chief-balcony", C("pointing toward a window with a warm smile"),
      c("答案就在陽台上。走，我們去看那台大箱子。", "接住上一句"), chapter="冷氣把熱的那頭放到外面")
kid("kid-hot-wind", K("standing in front of a white outdoor air conditioner unit with a big round fan grille, warm air blowing her hair back, squinting", where=BALCONY),
    k("哇，吹出來的是熱風！", "驚訝"))
chief("chief-outdoor", C("nodding with a knowing smile", close=True),
      c("這台叫做室外機，它吹的熱，"), c("是從你的房間裡搬出來的。", None, "P:outdoor"))
kid("kid-outside-air", K("holding up one finger with a confident grin", close=True, where=BALCONY),
    k("我知道！冷氣是把外面的空氣，", "很有把握的錯猜"), k("變冷再吹進來的！", None, "S:outsideair"))
chief("chief-own-air", C("shaking her head gently with a kind smile"),
      c("很多人都這樣想。其實冷氣吹的，"), c("是你房間自己的空氣。", None, "P:outsideair"))
scene("indoor-unit", "Wide view of a white wall-mounted split air conditioner high on the wall of a bright sunny bedroom, two thin pipes running from it through the wall to the outside, " + DAY,
      c("房間牆上那台把空氣吸進去，拿走熱，再吹回來。"), c("它和陽台那台，中間連著兩條管子。"))
chief("chief-same-trick", C("tracing a big loop in the air with one finger and a calm smile"),
      c("冷媒就在這兩台之間繞圈子跑，"), c("聽起來，像不像冰箱裡的什麼？", "轉向觀眾"), k("搬熱的小火車！", "搶答"))
scene("plan-house", "Top-down flat floor plan of a small bedroom and the balcony outside it seen from straight above, a white air conditioner on the bedroom wall and a white outdoor unit on the balcony, a dashed yellow loop drawn around only the bedroom, small round red balls leaving the bedroom through two pipes to the balcony, " + DAY,
      c("現在把圈畫在你的房間：房間就是冰箱的裡面，"), c("而冰箱的背後，被搬到了牆外面。"))
kid("kid-hot-end", K("pointing proudly out of a sunny window toward the balcony", close=True, where=BEDROOM),
    k("熱的那一頭在外面！", "想通", "P:acwhy"))
chief("chief-ac-bolt", C("holding up one finger, then pointing out toward the side"),
      c("冷氣吃的電，大部分也變成熱，"), c("在室外機那裡，一起吐到圈外。"))
scene("one-to-three", "Close-up of one bright yellow lightning bolt on the left and three plump round red balls with a small fourth one on the right, all floating over a pale sky-blue background, " + DAY,
      c("一般的冷氣，用一份電，", "數字放慢"), c("大約能搬走三份以上的熱。"))
kid("kid-bargain", K("holding up one finger on one hand and three fingers on the other, a delighted grin", close=True),
    k("一份電搬三份熱？", "驚訝"), k("好會搬！"))
chief("chief-depends", C("tilting one hand side to side with an honest smile", close=True),
      c("確切搬多少，要看冷氣和天氣，"), c("外面越熱，通常就搬得越吃力。"))
kid("kid-reverse-q", K("turning her hand upside down with a mischievous grin", close=True, where=BALCONY),
    k("那把冷氣反過來，", "調皮"), k("從外面搬熱進來呢？", "句尾上揚", "S:reverse"))
chief("chief-reverse", C("raising her eyebrows with a delighted smile"),
      c("真的有。冷暖氣機在冬天可以倒過來跑，", None, "P:reverse"), c("從外面的冷空氣裡，把熱搬進房間。"))
kid("kid-cold-heat", K("hugging herself in a thick scarf on a chilly bright winter morning, a puzzled frown", where=BALCONY),
    k("外面那麼冷，", "不解"), k("也有熱可以搬？", "句尾上揚"))
chief("chief-cold-heat", C("tapping her temple with one finger and a playful smile", close=True),
      c("還記得嗎？冷只是熱比較少，", "點名回呼"), c("冬天的空氣裡，還是有熱可以搬。"))
chief("chief-heater-vs", C("holding up one finger on one hand and three fingers on the other, eyebrows raised"),
      c("一台電暖器，用一份電，只能給你一份熱；"), c("冷暖氣機用一份電，可以從外面搬來好幾份。"))
kid("kid-heater-vs", K("hugging herself in a thick scarf with a delighted grin", close=True, where=BALCONY),
    k("用搬的，比用做的划算！", "想通"))
chief("chief-door-back", C("pressing her palms together as if closing a heavy door"),
      c("還記得冰箱那道厚厚的門嗎？", "點名回呼", "P:door"), c("開冷氣的時候，你關上窗、拉上窗簾，"))
kid("kid-curtain", K("pulling a pale yellow curtain closed across a sunny window", where=BEDROOM),
    c("就是幫房間關上一道厚門。"), k("所以開冷氣要關窗！", "想通"))
chief("chief-two-jobs", C("holding up one hand, then the other, with a calm smile"),
      c("冷氣負責把熱搬出去，"), c("隔熱負責讓外面的熱，慢一點溜回來。"))
kid("kid-both", K("making a big round circle with both arms over her head, grinning", close=True, where=BEDROOM),
    k("一個搬，一個擋！", "開心"))
chief("chief-open-window", C("pushing one hand forward as if opening a window, eyebrows raised"),
      c("那開著冷氣又開著窗呢？", "轉向觀眾"), c("就跟開著冰箱門一樣，冷氣只好搬個不停。"))
kid("kid-big-fridge", K("spreading her arms wide in a cool bright bedroom with the curtains drawn, laughing", where=BEDROOM),
    k("開冷氣的房間，", "恍然大悟"), k("就是一台大冰箱！", "開心"), c("對，而你就住在冰箱的裡面。", "笑"))

# ---------- 收尾 ----------
chief("chief-back-kitchen", C("pointing back over her shoulder with a playful smile"),
      c("好啦，我們回廚房吧。那扇冰箱門，還開著呢。", "笑"), chapter="小問關上冰箱門")
kid("kid-close-door", K("pushing the door of " + FRIDGE + " shut with both hands and a proud smile", where=KITCHEN),
    k("還記得我的好方法嗎？", "接住上一句"), k("我要收回！", "笑"))
kid("kid-got-it", K("throwing both arms up with a huge happy smile", where=KITCHEN),
    k("冰箱門開著，熱的那一頭，", "篤定"), k("還留在廚房裡！", "開心"))
chief("chief-same-machine", C("spreading her hands to show three things in a row, a warm smile"),
      c("冰箱和冷氣，是同一種搬熱的機器，"), c("差別只在熱的那一頭，放在圈裡還是圈外。"))
chief("chief-done", C("smiling warmly at the viewer with her hands clasped", close=True),
      c("下次你走過冰箱，可以摸摸它的背後：", "轉向觀眾，輕聲"), c("那一點溫溫的，是搬出來的熱，再加上它吃的電。"))
# The outro is three pictures, no card (series README §3.2, P05).
kid("outro", "Head-and-shoulders close-up of the girl with a big happy smile proudly holding up a big red rubber stamp in one hand, bright morning light",
    k("原來如此！", "開心大聲"))
chief("outro-chief", "Waist-up medium shot of the chief tilting her head with a curious smile and one finger raised, a plain pale wall behind her, bright morning light",
      c("你家冷氣的室外機，裝在哪裡？", "問句上揚，像聊天"), c("吹出來的風有多熱？留言告訴我們。"))
chief("outro-wave", "Waist-up medium shot of the chief waving goodbye with a warm smile, a plain pale wall behind her, bright morning light",
      c("想一起找生活裡的為什麼，就訂閱原來如此事務所。", "誠懇"))

# ---------- assemble ----------
WHAT = {"room": "冰箱門一直開著，廚房會變涼還是變熱", "back": "冰箱背後摸起來為什麼不冷", "outdoor": "陽台上冷氣的大箱子吹的是冷風還是熱風", "coldthing": "冷是不是一種會從冰箱跑出來的東西",
        "door": "冰箱那道厚厚的門，後面還有什麼用", "where": "冰箱裡的熱被搬去哪裡", "vanish": "冰箱是不是把熱吃掉了",
        "motor": "壓縮機吃進去的電最後去哪", "ledger": "背後吐出來的熱，跟裡面搬出來的一樣多嗎",
        "front": "站在冰箱門口明明是涼的", "acwhy": "冷氣也是搬熱，房間為什麼會變涼",
        "outsideair": "冷氣是不是把外面的空氣變冷吹進來", "wall": "冰箱背後可不可以緊貼著牆",
        "closed": "冰箱門關著時，廚房的熱帳怎麼算", "reverse": "把冷氣反過來，能不能從外面搬熱進來",
        }
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
    "series": {"slug": "sothatswhy", "episode": 7, "chapter": 1},
    # Same 14-minute bed as P02/P05/P14 (one paid Lyria take, tail trimmed, crossfaded): the series sounds the same.
    "music": {"track": "sothatswhy-p02-bed.m4a", "sha256": "54169439df49a00bc3ad993a148690be9f79d1dff8a4ea5143e64e583001b20c", "gain_db": -20, "duck_db": -10},
    "characters": CHARACTERS, "loops": loops,
    "youtube": {
        "category_id": 27, "made_for_kids": False, "default_language": "zh-TW",
        "title": "冰箱門打開，房間為什麼不會變涼？｜原來如此事務所",
        "description": "熱到不行的下午，小問把冰箱門一打開，臉馬上涼涼的。那冰箱門整天開著，廚房是不是就不用開冷氣了？\n\n"
                       "這一集，所長和小問盯著同一台冰箱，把圈越畫越大：先只看冰箱裡面，冷到底是不是一種會跑出來的東西；"
                       "再繞到冰箱背後，看冷媒和壓縮機怎麼把熱一圈一圈搬出去，壓縮機吃的電又去了哪裡；"
                       "然後把整間廚房圈起來算一次熱帳；最後走到陽台，看冷氣的室外機為什麼吹熱風，冷氣又為什麼能讓房間變涼。\n\n"
                       "本集插圖由 AI 生成。片中「兩顆熱加一份電」是為了好算的假設數字；冷氣搬熱的倍數是教學資料裡的大約數字，實際看機型與天氣。"
                       "每個說法的出處列在下方參考資料。\n\n資料截至 " + CHECKED,
        "tags": ["冰箱", "冰箱門打開", "冷氣", "室外機", "冷媒", "熱力學", "科普", "原來如此事務所"],
        "video_id": None},
    "thumbnail": {"template": "thumb", "data": {"headline": "冰箱門開著\n**廚房更熱**", "sub": "冰箱只是把熱搬到背後", "shot": "fridge-open"}},
    "sources": [
        {"title": "HyperPhysics (Georgia State University): Refrigerator", "url": "https://hyperphysics.gsu.edu/hbase/thermo/refrig.html", "checked_on": CHECKED},
        {"title": "HyperPhysics (Georgia State University): Heat Pump, Air Conditioners and Heat Pumps, Coefficient of Performance", "url": "https://hyperphysics.gsu.edu/hbase/thermo/heatpump.html", "checked_on": CHECKED},
        {"title": "University of Illinois Physics Van: Open Refrigerator", "url": "https://van.physics.illinois.edu/ask/listing/1790", "checked_on": CHECKED},
        {"title": "University of Sydney School of Physics: Bar Fridge (thermal physics activity)", "url": "https://www.physics.usyd.edu.au/super/physics_tut/activities/Thermal_Physics/Bar_Fridge.pdf", "checked_on": CHECKED},
        {"title": "Penn State EGEE 102: 10.4 How Air Conditioners Work", "url": "https://courses.ems.psu.edu/egee102/node/2426", "checked_on": CHECKED},
        {"title": "Wikipedia: Refrigerator", "url": "https://en.wikipedia.org/wiki/Refrigerator", "checked_on": CHECKED},
        {"title": "Wikipedia: Coefficient of performance", "url": "https://en.wikipedia.org/wiki/Coefficient_of_performance", "checked_on": CHECKED},
        {"title": "Wikipedia: Air conditioning", "url": "https://en.wikipedia.org/wiki/Air_conditioning", "checked_on": CHECKED},
        {"title": "Wikipedia: Dehumidifier", "url": "https://en.wikipedia.org/wiki/Dehumidifier", "checked_on": CHECKED},
        {"title": "HyperPhysics (Georgia State University): Thermal Conductivity", "url": "https://hyperphysics.gsu.edu/hbase/thermo/thercond.html", "checked_on": CHECKED},
        {"title": "Electrical and Mechanical Services Department, Hong Kong: Energy Saving Tips For Home, Air Conditioner", "url": "https://emsd.gov.hk/energyland/en/tips/home/air_conditioner.html", "checked_on": CHECKED},
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
