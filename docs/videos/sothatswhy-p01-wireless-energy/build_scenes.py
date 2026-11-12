"""Generate video.json for sothatswhy-p01-wireless-energy (原來如此事務所 對話版 P01).

Run `python3 build_scenes.py` from anywhere: it rewrites video.json next to this file and freezes
every shot's camera move in cameras.json (a shot keeps the camera it was first given, so deleting
a shot never shifts the others: the camera is in the keyframe cache key).
Edit lines and prompts here, never in video.json.
Started from a copy of sothatswhy-p04-microgravity-flame/build_scenes.py (series constants, helpers,
BANNED, assembly and self-checks unchanged; EXTRA and REWRITE start empty; the SAY loop is P29's and
stays empty because no spoken line carries a Latin letter); the content is new.
2026-11-11 rules applied (dialogue-pilot README §4, §9, §10.6): the faster voice style for both characters,
`pauses: {line_ms: 0, scene_ms: 150}` and `still_motion: "beat"`, no `pause_after_ms` on lines except a
BEAT_MS beat on the line right before each `P:` payoff in the same scene, and only an upper bound on length.
Line caps here count punctuation (chief <= 25, kid <= 15), stricter than P04's builder.
`script.md` is written by `node tools/video/cli.mjs script --slug sothatswhy-p01-wireless-energy` after this runs.
"""
import hashlib, itertools, json, os, re, sys, unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = "sothatswhy-p01-wireless-energy"
CHECKED = "2026-11-12"
BEAT_MS = 500   # 答案揭曉前的一拍（README §10.6）

# ---------- series constants (identical to P04) ----------
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
# Prompt words that P02/P05 taught us to keep out (README §3.1).
BANNED = re.compile(r"\b(no|not|without|text|blank|lamp|night|notebook|sign|signs|paper|poster|screen|book|calendar|whiteboard|thermometer|remote|label|magnet|microscope|arrow|arrows)\b", re.I)

CAMS = itertools.cycle(["push in", "pan left", "pull out", "drift", "tilt up", "pan right", "push in", "tilt down", "pull out", "drift"])
CAM_FILE = os.path.join(HERE, "cameras.json")
FROZEN = json.load(open(CAM_FILE, encoding="utf-8")) if os.path.exists(CAM_FILE) else {}

S = []
LONG = []
KIDFIX = set()
CHIEFFIX = set()
CHIEFFIX2 = set()  # every chief shot: the base description's grey streak kept winning (P07/P14 round 5)
CHIEFFIX_DESC = "the chief is a slim young woman of about thirty with glossy jet-black hair tied in a low ponytail, round black glasses, a yellow pencil tucked behind her ear, a mustard-yellow cardigan over a white blouse, flat 2D cel-shaded cartoon drawing with ink outlines"
KIDFIX_TAIL = ', exactly matching her reference sheet: the same little girl every time, short black bob with straight bangs, navy raincoat with mustard-yellow hood, long navy trousers, hood folded down behind her neck, bare short black bob uncovered and hanging free, simple dot-like cartoon eyes as on the reference sheet, a round young child face with big round matching eyes looking the same way, flat 2D cel-shaded cartoon drawing with ink outlines'
CHIEFFIX_TAIL = ', exactly matching her reference sheet: slim young woman, glossy jet-black hair with only one thin silver strand, mustard-yellow cardigan over a white blouse, flat 2D cel-shaded cartoon drawing with ink outlines'
FLAT = ", simple hand-drawn flat 2D children's cartoon illustration with clean ink outlines and flat colours"
HOOD = ", hood down, short black bob hanging free"
EXTRA = {}     # lines added after a visual review; empty until this episode's keyframes are drawn
REWRITE = {}   # whole-prompt rewrites after a visual review; empty until then
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

# One drawing language for the whole episode (README §10.5: the image model cannot draw diagrams, labels,
# arrows, counts or directions). The main thread is ONE late afternoon into dinner: 小問 rides the metro to the
# office (her mother works late, she eats at the office), taps her transit card at the gate, puts her mother's
# phone on the chief's charging pad, and watches the chief cook noodles on a small induction hob.
# The one analogy carried from start to end is THE SLOSHING BASIN: the chief's hand sways back and forth at one
# end of a basin of water and a small toy water wheel at the other end turns; when the hand stops, the water calms
# and the wheel stops (a field has to keep changing to push current); moved to a corner or far away it turns
# slowly (coupling falls with misalignment and distance). Limits in claims.md C24.
# Every frame is an everyday object at human scale or a simple cartoon room; devices are plain smooth cartoon
# objects with nothing written on them; the card's wire loop is drawn as an illustration (the description says so).
OFFICE = "in a bright cartoon room,"
KITCHEN = "in a bright cartoon kitchenette,"
SINK = "beside a small kitchen sink with a big blue plastic basin of water,"
STYLE = ", simple flat 2D cel-shaded cartoon drawing with clean ink outlines and flat colours"
CARD = "a plain light-blue card"
XCARD = "a see-through cartoon illustration of a plain light-blue plastic card showing a thin copper wire looping around its edge a few times and joined to one tiny square chip"
GATE = "a simple plain grey cartoon metro ticket gate with one smooth round glowing reader pad on top"
PAD = "a round plain white charging pad on a wooden desk"
PHONE = "a plain dark-grey smartphone"
HOB = "a small plain black glass induction hob with a smooth unmarked surface"
POT = "a shiny steel pot of noodle soup with gentle steam rising"
GPOT = "a clear glass pot of still water"
BASIN = "a big blue plastic basin of water"
WHEEL = "a small bright yellow toy water wheel floating in the water"
def obj(id, prompt, *lines, chapter=None):
    """An everyday-object frame with nobody in it, always in the flat cartoon style."""
    scene(id, prompt + STYLE + ", clean empty corners", *lines, chapter=chapter)

# ---------- 開場（系列片頭之後直接進場景，不做濃縮；結果都不先講）----------
obj("gate-tap", "Close-up of a child's small hand holding " + CARD + " flat against " + GATE + ", a soft glow around the pad",
    k("所長！我搭捷運來的！", "急著報案的語氣"),
    k("卡片在閘門上一貼，就嗶一聲。", "興奮"), chapter="一路沒插線，鍋子先滾了")
chief("chief-cook", C("stirring a pot with long chopsticks with a cheerful smile, " + KITCHEN.rstrip(",")),
    c("歡迎。我用電磁爐煮麵，快好了。", "笑"),
    k("媽媽的手機快沒電了。"))
# Thumbnail shot (fixed before keyframes): the kid big and centred, the card in hand.
kid("kid-main-q", K("holding up " + CARD + " in one hand beside her face and looking at the viewer with wide curious eyes, in the exact centre of the picture", where=OFFICE),
    k("可以放你的充電板嗎？", "句尾上揚"),
    c("可以，放上去就好。"))
obj("phone-pad", "Close-up of " + PHONE + " lying face up on " + PAD + ", a tiny soft green glow on the edge of the pad",
    k("咦？它沒插線，也在充電耶！", "驚訝"))
obj("pot-boil", "Close-up of " + POT + " on " + HOB + ", the noodle soup bubbling, the glass around the pot clean and shiny",
    k("所長的鍋子也滾了！", "指著"),
    c("我把手靠近鍋子旁邊的爐面玻璃，不覺得燙。"),
    c("你先別碰，等一下告訴你為什麼。", "叮嚀", "S:coolglass"))
kid("kid-puzzle", K("counting on her fingers with a puzzled frown", where=OFFICE),
    k("卡片、手機、鍋子都沒插線，", "想不通"),
    k("電怎麼跑過去的？", "句尾上揚", "S:jump"),
    k("而且只有鍋子變熱？", "句尾上揚", "S:heat"))
chief("chief-energy", C("holding up three fingers with a bright smile"),
    c("這三樣東西，都是隔空收到了能量。"),
    k("能量是什麼？", "句尾上揚"),
    c("讓燈會亮、東西會動、會變熱的那份本事。"))
chief("chief-energy2", C("opening both hands with a warm smile", close=True),
    c("手機要是往旁邊挪一點點，還充得到嗎？等等你就知道。", "賣關子", "S:shift"))
chief("chief-hooks", C("counting on her fingers with a playful mysterious smile"),
    c("這口麵煮完，我再拿一口玻璃鍋上來。", None, "S:glass"),
    c("你那張卡片，離閘門多遠就不嗶了？你猜猜。", "轉向觀眾", "S:cardfar"),
    k("要貼著才嗶！電是飛過去的！", "篤定的錯猜", "S:fly"))

# ---------- 第一章：卡片貼上閘門那一下 ----------
chief("chief-not-fly", C("shaking her head gently with a kind smile, one palm raised", close=True),
    c("不是像球那樣飛過去喔。", "接住上一句"),
    c("你剛剛嗶的那張卡片，裡面有電池嗎？"),
    k("一定有！不然哪來的電？", "篤定的錯猜", "S:battery"), chapter="卡片貼上閘門那一下")
obj("card-xray", "Close-up of " + XCARD + ", on a plain pale cream background",
    c("一家做感應卡晶片的廠商說，它不需要電池。", None, "P:battery"),
    c("卡片裡藏著一圈一圈的細線，接著一顆小晶片。"))
kid("kid-chip-q", K("tilting her head with a curious face, one finger on her cheek", close=True, where=OFFICE),
    k("晶片是什麼？", "句尾上揚"),
    c("一小片會記東西、會照規則回話的電子零件。"),
    k("沒有電池，電從哪裡來？", "追問", "S:where"))
obj("gate-coil", "Close-up of " + GATE + ", soft pale blue rings of light around the round reader pad",
    c("從閘門來。閘門的讀卡處裡，也有一圈線。", "接住上一句"),
    c("電在那圈線裡，一下往這邊跑，一下往那邊跑。"))
chief("chief-field", C("swinging one hand slowly left and right in front of her with a calm smile"),
    c("這樣，它旁邊就會有一個一直在變的磁場。"),
    k("磁場是什麼？", "句尾上揚"))
chief("chief-field2", C("cupping both hands around an empty space as if holding something invisible, a gentle smile", close=True),
    c("磁鐵旁邊那圈看不見、能吸住鐵的範圍，就是磁場。"),
    c("這類感應卡用的磁場，一秒鐘來回變一千三百多萬次。", "數字放慢"))
obj("card-near", "Close-up of " + XCARD + " held just above " + GATE + ", soft pale blue rings of light passing through the card",
    k("好快！", "驚訝"), k("可是跟卡片有什麼關係？", "句尾上揚"),
    c("一直在變的磁場，穿過卡片那圈細線，"),
    c("就會推著線裡的電，跑起來。", None, "P:where"))
chief("chief-basin", C("standing " + SINK + " with a cheerful smile, one hand resting on the rim of the basin"),
    k("看不見，我想不出來。", "苦惱"),
    c("那我們到洗手台。這盆水的那一頭，放一個小水車。"),
    c("我的手在這一頭，一前一後一直晃。"))
obj("wheel-turn", "Wide shot of " + BASIN + " seen from above, gentle round ripples moving across the water towards " + WHEEL + " at the far end, the wheel turning",
    k("水一晃過去，水車就轉了！", "驚喜"),
    c("我的手，就像閘門那圈線；晃的水，像一直變的磁場。"))
chief("chief-map", C("swaying one hand back and forth over a big blue plastic basin of water with a pleased smile"),
    c("小水車，就是卡片裡那圈細線。"),
    k("那你的手不晃呢？", "句尾上揚", "S:still"))
obj("wheel-stop", "Wide shot of " + BASIN + " seen from above, the water flat and calm like glass, " + WHEEL + " standing still at the far end",
    c("你看，水一靜下來，水車就停了。", None, "P:still"),
    c("磁場也一樣，要一直變，才推得動電。", None, "P:fly"))
chief("chief-chip-wake", C("giving a small thumbs-up with a pleased smile"),
    c("卡片收到這一點電，晶片就醒過來，"),
    c("跟閘門交換資料，閘門才嗶一聲讓你過。"),
    k("卡片沒電池，怎麼回話？", "句尾上揚", "S:talk"))
obj("card-talk", "Close-up of " + XCARD + " held just above " + GATE + ", the soft pale blue rings of light gently pulsing brighter and dimmer",
    c("它不用自己發出訊號，只是讓閘門的磁場，", "接住上一句"),
    c("被它一下多拿一點、一下少拿一點。"))
chief("chief-talk", C("tapping one ear lightly with a knowing smile", close=True),
    c("閘門感覺到這些變化，就讀懂卡片的回答。", None, "P:talk"),
    k("那卡片離開閘門以後呢？", "句尾上揚", "S:after"))
chief("chief-after", C("holding " + CARD + " far out to one side at arm's length with a gentle smile"),
    c("還記得它沒有電池嗎？離開那個磁場，就沒電可用了。", None, "P:after"),
    c("它不存電，收到的電，當下就用掉。"))
kid("kid-store-q", K("looking at " + PHONE + " in her hand with a curious frown", where=OFFICE),
    k("那媽媽的手機呢？", "追問"), k("也是收到就用掉嗎？", "章尾停住，句尾上揚", "S:store"))

# ---------- 第二章：把媽媽的手機放上充電板 ----------
obj("pad-coils", "Close-up of " + PHONE + " lying face up on " + PAD + ", seen from the side, a soft pale blue glow between the phone and the pad",
    c("不只用掉，手機還會把電存起來。", "接住上一句", "P:store"),
    c("充電板裡有一圈線，手機背面裡面也有一圈。"), chapter="把媽媽的手機放上充電板")
chief("chief-same", C("pointing at a round plain white charging pad on the desk beside her with a bright smile"),
    c("還記得卡片嗎？充電板的磁場也一直在變，"),
    c("推著手機那圈線裡的電跑起來。"),
    k("跟小水車一樣！", "開心"))
chief("chief-back-forth", C("moving one hand left and right like a pendulum with a thoughtful smile", close=True),
    c("對。可是推出來的電，一下往這邊、一下往那邊。"),
    k("那樣不能充電嗎？", "句尾上揚", "S:rect"))
chief("chief-rect", C("holding up one finger with a careful smile"),
    c("電池要的，是一直往同一邊走的電。"),
    c("所以手機裡有一個零件，叫做整流器，"))
obj("rect-part", "Close-up of one tiny square black electronic part on a small green circuit board inside an opened cartoon phone, a thin copper wire loop around it, on a plain pale cream background",
    c("把來回跑的電，整理成往同一邊走。", None, "P:rect"),
    k("卡片也要整理嗎？", "句尾上揚"),
    c("要。剛剛那家廠商說，卡片的晶片裡也有整流器。"))
chief("chief-diff", C("holding out both hands like a balance with a bright smile"),
    k("手機和卡片哪裡不一樣？", "追問", "S:diff"),
    c("卡片收到電，馬上就用掉；"),
    c("手機收到電，送進電池存起來，晚一點才用。", None, "P:diff"))
obj("wheel-bell", "Wide shot of " + BASIN + " seen from above, " + WHEEL + " at the far end with one tiny brass bell on top of it",
    c("還記得水盆嗎？卡片的小水車，轉一下就敲響鈴鐺；"))
obj("wheel-pump", "Wide shot of " + BASIN + " seen from above, " + WHEEL + " at the far end joined by a thin tube to a small clear bottle half full of water beside the basin",
    c("手機的水車，接著一台小幫浦，把水打進瓶子存著。"),
    k("那瓶子滿了怎麼辦？", "句尾上揚", "S:full"))
chief("chief-full", C("holding a plain dark-grey smartphone up beside her face with a knowing smile", close=True),
    c("手機會傳話給充電板：電池滿了，可以停了。", None, "P:full"),
    k("我的卡片也放上去充電！", "興奮", "S:cardpad"))
chief("chief-no", C("holding up one hand like a gentle stop with a kind but firm smile", close=True),
    c("不行喔。做手機的公司在說明裡寫，中間別夾東西。", "認真"),
    c("卡片夾在中間，裡面的晶片可能會壞掉。", None, "P:cardpad"))
chief("chief-no2", C("shaking her head gently with a soft smile"),
    c("還記得嗎？卡片沒有電池，本來就不用充電。"),
    k("好吧。那手機會變熱嗎？", "句尾上揚", "S:phonewarm"))
obj("phone-warm", "Close-up of " + PHONE + " lying face up on " + PAD + ", faint soft wavy shimmer of warm air above the phone",
    c("會一點點。說明也寫，充電時手機可能稍微變暖。", None, "P:phonewarm"),
    c("線圈和整流器在整理電的時候，有一點會變成熱。"))
kid("kid-pot-q", K("turning to look towards the kitchen with wide eyes and sniffing the air", where=OFFICE),
    k("那鍋子為什麼那麼燙？", "章尾停住，句尾上揚", "S:pot"))

# ---------- 第三章：麵煮滾了，旁邊的玻璃不燙 ----------
chief("chief-pot-recv", C("holding long chopsticks above a steaming pot with a bright smile, " + KITCHEN.rstrip(",")),
    c("因為鍋子自己，就是接收的那一端。", "接住上一句"),
    c("電磁爐的玻璃底下，也有一圈線，磁場一直在變。"),
    k("鍋子裡也有細線嗎？", "句尾上揚", "S:potloop"), chapter="麵煮滾了，旁邊的玻璃不燙")
obj("pot-base", "Close-up of the flat round bottom of a shiny steel pot, soft glowing orange swirls drawn inside the metal of the base like little whirlpools, on a plain pale cream background",
    c("沒有細線。磁場直接穿進鍋底的金屬，", "接住上一句"),
    c("在金屬裡推出一圈一圈、繞著跑的電流。", None, "P:potloop"))
chief("chief-eddy", C("drawing small circles in the air with one finger and an amused smile", close=True),
    c("這種在金屬裡打轉的電流，叫做渦電流。"),
    c("渦，就是漩渦的渦。"),
    k("那電流要送去哪裡？", "句尾上揚"))
chief("chief-nowhere", C("rubbing her two palms together briskly with a playful grin"),
    c("哪裡都不去，就在鍋底一直繞。"),
    c("電流在金屬裡跑，會一直撞到裡面的小粒子，"))
obj("pot-heat", "Close-up of " + POT + " on " + HOB + ", the bottom of the pot glowing a soft warm orange, the glass around it clean and dark",
    c("撞來撞去，電的能量就變成了熱。"),
    k("像我搓手會熱一樣！", "聯想"))
chief("chief-from-pot", C("giving a small thumbs-up with a pleased smile"),
    c("有點像。所以熱，是從鍋子自己身上冒出來的。", None, "P:pot"),
    c("鍋子熱了，再把熱傳給湯和麵。"),
    k("那旁邊的玻璃怎麼不燙？", "句尾上揚"))
chief("chief-glass", C("holding her open hand flat in front of her with a calm smile", close=True),
    c("還記得我說等一下告訴你嗎？磁場也穿過玻璃，"),
    c("可是玻璃不導電，幾乎推不出電流。"))
chief("chief-glass2", C("pointing down beside her with a gentle smile"),
    c("美國大學給家庭的說明也寫，鍋子周圍會保持涼。", None, "P:coolglass"),
    c("不過鍋子正下方的玻璃，會被熱鍋燙熱。"))
chief("chief-glasspot", C("holding up " + GPOT + " in both hands with a playful smile, " + KITCHEN.rstrip(",")),
    c("所以剛放過鍋子的地方，千萬別摸。", "叮嚀"),
    c("還記得我說要換一口玻璃鍋嗎？你看。"))
obj("glasspot-hob", "Close-up of " + GPOT + " sitting on " + HOB + ", the water perfectly calm and clear",
    c("一樣的爐子，玻璃鍋裡的水，就是熱不起來。", None, "P:glass"),
    k("跟剛剛那塊玻璃一樣！", "搶答"))
chief("chief-metal", C("tapping the side of a shiny steel pot with one finger and a bright smile"),
    c("對。鍋子要是金屬，電流才繞得起來。"),
    k("那金屬鍋都可以嗎？", "句尾上揚", "S:metal"))
obj("pots-row", "Wide shot of three empty cooking pots side by side on a wooden table, a dark iron pot, a shiny steel pot and a pale silver pot, a plain pale cream wall behind",
    c("也不是。教科書說，鍋底要是鐵或鋼這類材料。"),
    c("美國大學那份說明也寫，鋁鍋、銅鍋都不行。"),
    k("那我要怎麼分辨？", "句尾上揚"))
chief("chief-test", C("holding an empty steel pot upside down and looking at its bottom with a knowing smile"),
    c("拿冰箱上的磁鐵碰碰鍋底，吸得住，通常就能用。", None, "P:metal"),
    c("有的鍋子是好幾種金屬做的，就看包裝的標示。"))
kid("kid-try-mag", K("bouncing on her toes with an excited grin, both fists clenched", where=KITCHEN),
    k("我回家拿磁鐵試！", "興奮"),
    c("可以，但要等鍋子冷了、拿下爐子再試。", "叮嚀"))
kid("kid-cardcool-q", K("holding " + CARD + " up beside her cheek with a thinking face", close=True, where=KITCHEN),
    k("那卡片的細線也有電在跑，", "想不通"), k("為什麼卡片不會燙？", "句尾上揚", "S:cardcool"))
chief("chief-cardcool", C("holding out both hands like a balance with a thoughtful smile"),
    c("因為卡片收到的電，只有一點點。"),
    c("電磁爐卻是專門把能量灌進鍋底，讓它變成熱。", None, "P:cardcool"))
obj("phone-slid", "Close-up of " + PHONE + " lying face up half off the edge of " + PAD + ", slightly crooked",
    k("咦？媽媽的手機剛剛震了一下，", "發現"), k("好像沒在充了！", "章尾停住", "S:stopped"))

# ---------- 第四章：手機往旁邊挪一點點 ----------
chief("chief-slid", C("bending forward and looking down at the desk with a curious smile", close=True),
    c("你看，它震的時候，往旁邊滑開了一點點。", "接住上一句"),
    c("手機的說明真的寫著：震動可能讓手機移位，"), chapter="手機往旁邊挪一點點")
chief("chief-move-wheel", C("standing " + SINK + " and gently pushing a small yellow toy water wheel towards one corner of the basin"),
    c("充電板就可能停止供電。", None, "P:stopped"),
    k("才一點點耶！", "不敢相信"),
    c("還記得水盆嗎？我把小水車，挪到角落去。"))
obj("wheel-corner", "Wide shot of " + BASIN + " seen from above, gentle ripples crossing the middle, " + WHEEL + " pushed into one far corner, turning only a little",
    k("它轉得好慢！", "驚訝"),
    c("兩圈線對得越正，穿過去的磁場就越多；"))
chief("chief-crooked", C("tilting one flat hand sideways with a thoughtful smile", close=True),
    c("一歪掉，能接到的就少了。", None, "P:shift"),
    c("所以說明要你，最好把手機放在充電板正中間。"),
    k("那離遠一點呢？", "句尾上揚", "S:far"))
obj("wheel-far", "Wide shot of a very long blue plastic tub of water seen from above, faint tiny ripples, " + WHEEL + " far away at the very end, almost still",
    c("也一樣。離得越遠，穿過那圈線的磁場越少。", None, "P:far"),
    k("所以卡片要貼著閘門！", "恍然"),
    c("越近越好。可是一定要貼著嗎？"))
chief("chief-cardfar", C("holding up " + CARD + " between two fingers with a bright smile"),
    c("一款做車票用的卡片晶片，規格寫最遠大約十公分，"),
    c("而且還要看卡片的線圈，和閘門那一邊。", None, "P:cardfar"))
kid("kid-potcenter-q", K("pointing at " + POT + " on " + HOB + " with a curious face", where=KITCHEN),
    k("鍋子也要放正中間嗎？", "句尾上揚", "S:potcenter"))
obj("pot-center", "Close-up of " + POT + " sitting neatly in the middle of " + HOB + ", seen from above",
    c("要。美國大學那份說明寫，放中間爐子才會好好加熱。", None, "P:potcenter"),
    c("很多電磁爐偵測不到鍋子，就會自己停下來。"))
chief("chief-lift", C("lifting a shiny steel pot up a little with both hands and a calm smile, " + KITCHEN.rstrip(",")),
    k("那把鍋子拿起來呢？", "句尾上揚", "S:lift"),
    c("美國能源部的說明寫，鍋子一拿開，加熱就停了。", None, "P:lift"),
    c("還記得卡片離開閘門嗎？一樣是收不到了。"))
kid("kid-coin-q", K("holding up one shiny round coin between two fingers with a curious face", close=True, where=OFFICE),
    k("那硬幣放上充電板，", "好奇"), k("也會像鍋子一樣熱嗎？", "句尾上揚", "S:coin"))
chief("chief-coin", C("nodding slowly with a serious but kind face"),
    c("可能會。金屬在一直變的磁場裡，也會繞起電流。"),
    c("所以無線充電的規格，要手機回報收到多少電，"))
obj("pad-watch", "Close-up of " + PHONE + " lying neatly in the middle of " + PAD + ", a tiny soft green glow on the edge of the pad",
    c("讓充電板發現，中間是不是多了一塊會變熱的金屬。", None, "P:coin"),
    k("那我拿硬幣試試看！", "興奮"))
chief("chief-coin-no", C("holding up one hand like a gentle stop with a kind but firm smile", close=True),
    c("不行喔。金屬會變燙，硬幣、鋁箔都別放上去。", "認真"),
    k("好啦。那電怎麼隔空過去？", "章尾停住，句尾上揚"))

# ---------- 收尾 ----------
chief("chief-your-turn", C("leaning forward with an inviting grin, one hand open towards the viewer"),
    c("卡片、手機、鍋子你都看過了，你說呢？", "笑"), chapter="麵吃完，小問想通了")
kid("kid-got-it", K("holding " + CARD + " up high with a big confident grin", where=KITCHEN),
    k("原來如此！", "恍然大悟"), k("是一直在變的磁場，", "篤定"),
    k("推著線圈和鍋底的電跑！", "篤定", "P:jump"))
kid("kid-got-it2", K("counting on her fingers with a proud happy face", close=True, where=KITCHEN),
    k("卡片、手機、鍋子，", "篤定"), k("收到能量以後，", "篤定"),
    k("做的事就不一樣！", "篤定", "P:heat"))
chief("chief-opinion", C("smiling with her hands clasped, a thoughtful look", close=True),
    c("說得好。我覺得最妙的是：", "笑"),
    c("同一種推法，能讓卡片說話，也能把麵煮滾。"))
# The outro is three pictures, no card, no stamp (series README §3.2, §10.1): the kid gives a thumbs-up.
kid("outro", "Waist-up medium shot of the girl with a big happy smile giving a big cheerful thumbs-up with one hand, bright morning light",
    k("明天刷卡，我要貼正一點！", "開心大聲"))
chief("outro-chief", "Waist-up medium shot of the chief holding up a plain light-blue plastic card with a curious smile, filling the frame, a plain pale wall behind her, bright morning light",
      c("你家還有什麼東西，不插線也能收到能量？", "問句上揚，像聊天"), c("留言告訴我們。"))
chief("outro-wave", "Waist-up medium shot of the chief waving goodbye with a warm smile, a plain pale wall behind her, bright morning light",
      c("想一起找生活裡的為什麼，就訂閱原來如此事務所。", "誠懇"))

# ---------- assemble ----------
WHAT = {"jump": "沒有插線，電怎麼跑過去", "heat": "為什麼只有鍋子變熱",
        "coolglass": "鍋子旁邊的玻璃為什麼不燙", "shift": "手機往旁邊挪一點點會怎樣",
        "glass": "換一口玻璃鍋放上爐子會怎樣", "cardfar": "卡片要離閘門多近才會嗶",
        "fly": "電是不是飛過去的", "battery": "卡片裡有沒有電池",
        "where": "沒有電池，卡片的電從哪裡來", "still": "手不晃、磁場不變會怎樣",
        "after": "卡片離開閘門以後怎樣", "store": "手機是不是也收到就用掉",
        "rect": "來回跑的電能不能充電", "diff": "手機和卡片哪裡不一樣",
        "full": "電池滿了怎麼辦", "cardpad": "卡片能不能放上充電板充電",
        "phonewarm": "手機充電會不會變熱", "pot": "鍋子為什麼那麼燙",
        "potloop": "鍋子裡有沒有細線", "metal": "金屬鍋是不是都可以",
        "cardcool": "卡片也有電在跑，為什麼不燙", "stopped": "手機震了一下，為什麼沒在充",
        "far": "離遠一點會怎樣", "lift": "鍋子拿起來會怎樣", "coin": "硬幣放上充電板會不會像鍋子一樣熱", "potcenter": "鍋子要不要放正中間", "talk": "卡片沒電池怎麼回話"}
# Latin terms the Mandarin voice must spell letter by letter (P13 GPS, P29 HTTPS/TLS). This episode says
# 無線充電／感應卡／電磁爐 and never a brand or standard name, so no spoken line carries a Latin letter; the loop
# stays so a later edit that adds one is spelled and carries say_for.
SAY = []
scenes, loops_s, loops_p, n, beats = [], {}, {}, 0, 0
for sc in S:
    lines = []
    for sp, text, emo, tag in sc["lines"]:
        n += 1; lid = f"p{n:03d}"
        line = {"id": lid, "speaker": sp, "text": text}
        spoken = text
        for term, spell in SAY:
            spoken = spoken.replace(term, spell)
        if spoken != text:
            line["say"] = spoken
            line["say_for"] = hashlib.sha256(unicodedata.normalize("NFC", text).encode("utf-8")).hexdigest()[:12]
        assert not re.search(r"[A-Za-z]", spoken), (lid, "a Latin term needs a SAY entry")
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
    "target_minutes": [10, 12], "voice": VOICE, "subtitles": {"burn_in": False}, "theme": "paper", "look": {"preset": "cute-cartoon"},
    # The series tag: the approved character sheets live in the series store and every episode reuses them (docs/videos/SERIES.md).
    "series": {"slug": "sothatswhy", "episode": 1, "chapter": 1},
    # 2026-11-11 (README §9 停頓, §10.6): no fixed pause between lines, a short gap between scenes, beat-timed stills.
    "pauses": {"line_ms": 0, "scene_ms": 150},
    "still_motion": "beat",
    # The series bed from P15 on (explainer-series/README.md, PR #2048): sothatswhy-bed-r2.m4a, remade from P02's paid take.
    "music": {"track": "sothatswhy-bed-r2.m4a", "sha256": "9bb4ba6fd16feb4a7f352144b2d89e9648acbbbbaa2173c27a7eefbdb70f28c6", "gain_db": -20, "duck_db": -10},
    "characters": CHARACTERS, "loops": loops,
    "youtube": {
        "category_id": 27, "made_for_kids": False, "default_language": "zh-TW",
        "title": "卡片不燙、鍋子卻熱：電怎麼隔空過去？｜原來如此事務所",
        "description": "小問搭捷運來事務所：交通卡在閘門上一貼就嗶一聲，媽媽的手機放上充電板就開始充電，所長的鍋子在電磁爐上煮滾了，旁邊的玻璃卻不燙。三樣東西都沒有插線，電怎麼跑過去的？為什麼只有鍋子變熱？\n\n"
                       "這一集，所長拿一盆水和一個小水車來想：手在這一頭一直晃，那一頭的水車就轉；手一停，水車也停。閘門、充電板和電磁爐的線圈裡，電一下往這邊、一下往那邊跑，旁邊就有一個一直在變的磁場，穿過附近的線圈或金屬，推著裡面的電跑起來。"
                       "收到以後，三樣東西做的事不一樣：感應卡沒有電池，靠這一點電讓晶片醒來回答閘門；手機用整流器把電整理好，存進電池；鍋子自己就是接收的那一端，電流在鍋底繞圈圈，變成熱。"
                       "對歪了、離遠了，能接到的就變少，所以手機要放在充電板中間、卡片要貼近閘門、鍋子要放在爐子中間。\n\n"
                       "片中的閘門、卡片、手機、充電板、電磁爐與水盆都是 AI 生成的示意插圖，不是實際的產品或結構圖。請不要把卡片、硬幣、鋁箔或其他金屬放在充電板或電磁爐上試；剛放過鍋子的爐面會燙。每個說法的出處列在下方參考資料。\n\n資料截至 " + CHECKED,
        "tags": ["無線充電", "電磁爐", "感應卡", "交通卡", "磁場", "電磁感應", "渦電流", "科普", "原來如此事務所"]},
    "thumbnail": {"template": "thumb", "data": {"headline": "卡片不燙\n**鍋子卻熱？**", "sub": "電怎麼隔空跑過去", "shot": "kid-main-q", "subject": "right"}},
    "sources": [
        {"title": "Microchip, microID 13.56 MHz RFID System Design Guide (DS21299E)", "url": "https://ww1.microchip.com/downloads/en/DeviceDoc/21299E.pdf", "checked_on": CHECKED},
        {"title": "OpenStax, College Physics 2e, 23.4 Eddy Currents and Magnetic Damping", "url": "https://openstax.org/books/college-physics-2e/pages/23-4-eddy-currents-and-magnetic-damping", "checked_on": CHECKED},
        {"title": "OpenStax, College Physics 2e, 23.2 Faraday's Law of Induction: Lenz's Law", "url": "https://openstax.org/books/college-physics-2e/pages/23-2-faradays-law-of-induction-lenzs-law", "checked_on": CHECKED},
        # HyperPhysics (farlaw.html, elepow.html) is served over http only, so it is a cross-check in claims.md, not a listed source.
        {"title": "OpenStax, College Physics 2e, 20.2 Ohm's Law: Resistance and Simple Circuits", "url": "https://openstax.org/books/college-physics-2e/pages/20-2-ohms-law-resistance-and-simple-circuits", "checked_on": CHECKED},
        {"title": "NFC Forum, NFC Technology: Technical Overview", "url": "https://nfc-forum.org/learn/nfc-technology/", "checked_on": CHECKED},
        {"title": "NXP, MIFARE Classic EV1 1K product data sheet MF1S50YYX_V1 (Rev. 3.2, 2018-05-23)", "url": "https://www.nxp.com/docs/en/data-sheet/MF1S50YYX_V1.pdf", "checked_on": CHECKED},
        {"title": "NXP, MIFARE DESFire EV3 product short data sheet MF3D(H)x3 (Rev. 3.1, 2024-01-11)", "url": "https://www.nxp.com/docs/en/data-sheet/MF3D_H_X3_SDS.pdf", "checked_on": CHECKED},
        {"title": "Wireless Power Consortium, Principle of Inductive Power", "url": "https://www.wirelesspowerconsortium.com/knowledge-base/magnetic-induction/principle-of-inductive-power/", "checked_on": CHECKED},
        {"title": "Wireless Power Consortium, Coupling Factor", "url": "https://www.wirelesspowerconsortium.com/knowledge-base/magnetic-induction/coupling-factor/", "checked_on": CHECKED},
        {"title": "Wireless Power Consortium, How Qi Works", "url": "https://www.wirelesspowerconsortium.com/knowledge-base/magnetic-induction/how-qi-works/", "checked_on": CHECKED},
        {"title": "Texas Instruments, BQ51013B wireless power receiver data sheet (SLUSB62D, rev. 2020-09)", "url": "https://www.ti.com/lit/ds/symlink/bq51013b.pdf", "checked_on": CHECKED},
        {"title": "Texas Instruments, SLOA192B NFC active and passive peer-to-peer communication using the TRF7970A (rev. 2019-03)", "url": "https://www.ti.com/lit/an/sloa192/sloa192.pdf", "checked_on": CHECKED},
        {"title": "Apple Support, How to wirelessly charge your iPhone (108377, 2024-04-24)", "url": "https://support.apple.com/en-us/108377", "checked_on": CHECKED},
        {"title": "U.S. Department of Energy, Making the Switch to Induction Stoves or Cooktops (2023-05-11)", "url": "https://www.energy.gov/articles/making-switch-induction-stoves-or-cooktops", "checked_on": CHECKED},
        {"title": "ENERGY STAR, Electric Cooking Products", "url": "https://www.energystar.gov/products/electric_cooking_products", "checked_on": CHECKED},
        {"title": "Iowa State University Extension AnswerLine, Induction Cooking – What You Need to Know (2022-06-07) and Portable Induction Burners (2019-09-30)", "url": "https://blogs.extension.iastate.edu/answerline/tag/induction-cooking", "checked_on": CHECKED},
        {"title": "UC Cooperative Extension, Safety Note #14: Induction Stove Safety", "url": "https://www.ccfruitandnuts.ucanr.edu/sites/default/files/2017-09/270568.pdf", "checked_on": CHECKED},
    ],
    "assets": [],
    "scenes": scenes,
}
json.dump(doc, open(os.path.join(HERE, "video.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
FROZEN.update({s["id"]: s["data"]["camera"] for s in scenes if s["template"] == "shot" and s["id"] not in FROZEN})
json.dump(FROZEN, open(CAM_FILE, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# ---------- self-checks (the series rules lint does not cover for a sothatswhy- slug) ----------
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
# Line caps count punctuation (P01 brief: chief <= 25, kid <= 15 characters, punctuation counted).
long_lines = [l for l in lines_all if len(l["text"]) > (15 if l["speaker"] == "kid" else 25)]
for l in long_lines: print(f"  long {l['speaker']} line {l['id']} ({len(l['text'])}): {l['text']}", file=sys.stderr)
assert not long_lines, "a line over its cap (punctuation counted)"
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
assert len(loops) >= 13, "the plan asks for at least 13 loops, every one paid off"
assert body_chars <= 3000, f"body {body_chars} characters: keep under 3,000"
assert all(s["data"]["camera"] for s in scenes)
cams = [s["data"]["camera"] for s in scenes]
assert all(not (a == b == c_) for a, b, c_ in zip(cams, cams[1:], cams[2:])), "three shots in a row with the same camera"
