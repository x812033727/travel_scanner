"""Generate video.json for sothatswhy-p06-bubble-film (原來如此事務所 對話版 P06).

Run `python3 build_scenes.py` from anywhere: it rewrites video.json next to this file and freezes
every shot's camera move in cameras.json (a shot keeps the camera it was first given, so deleting
a shot never shifts the others: the camera is in the keyframe cache key).
Edit lines and prompts here, never in video.json.
Started from a copy of sothatswhy-p18-pencil-diamond/build_scenes.py (series constants, helpers,
assembly and self-checks unchanged; EXTRA and REWRITE start empty because P18's entries were picture
fixes for P18 only); the content is new.
`script.md` is written by `node tools/video/cli.mjs script --slug sothatswhy-p06-bubble-film` after this runs.
"""
import itertools, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = "sothatswhy-p06-bubble-film"
CHECKED = "2026-11-10"

# ---------- series constants ----------
# Both characters are identical to P07/P14/P08 (approved series sheets reused through the `series` tag):
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

HOME = "in a bright sunny Taiwanese apartment living room"
BALCONY = "on a sunny apartment balcony"
PARK = "in a sunny park by a small pond"
# One drawing language for the whole episode (README §10.5, and the P17/P18 lesson that the image model cannot
# draw molecules, light rays, wave lines or film cross-sections): every mechanism is drawn through everyday,
# human-scale objects. The one metaphor carried from start to end is the BALLOON SKIN: the soap film is a skin that
# always pulls inward and wants to shrink (shape); for the colours, the two reflections are the two sets of ripples
# from two pebbles dropped in a pond (crest on crest grows, crest on trough goes flat). Soap bubbles themselves are
# drawable, so most mechanism frames are bubbles: round, a touching pair with a flat wall, a small one bulging
# into a big one, three meeting, striped colour bands, a dark top. Nothing is counted, nothing depends on an arrow.
STYLE = ", simple flat 2D cel-shaded cartoon drawing with clean ink outlines and flat colours"
CREAM = STYLE + ", plain warm pale cream background"
WAND = "a simple bubble wand made of plain silver wire bent into a square loop with a short straight handle"
BOTTLE = "a small plain smooth clear plastic bottle of colourless bubble liquid"
BUBBLE = "a round transparent soap bubble with soft swirling pink, green and gold sheen"
def bub(id, prompt, *lines, chapter=None):
    """A soap-bubble or everyday-object frame with nobody in it, always in the flat cartoon style (P18: object
    prompts without style words came out as photos)."""
    scene(id, prompt + STYLE, *lines, chapter=chapter)

# ---------- 開場（系列片頭之後直接進場景，不做濃縮；答案都不先講）----------
# The first picture is the problem itself (owner from P08 on): a round bubble leaving a square wand, nobody in it.
bub("square-wand", "Close-up of " + WAND + " standing in " + BOTTLE + " on a sunny balcony railing, green potted plants and blue sky behind",
    k("所長！我剛在陽台彎了方框，", "委屈又興奮，跑進來報案的語氣"), chapter="方框吹出的圓泡泡")
bub("round-from-square", "Close-up of a perfectly round soap bubble just floating free from " + WAND + ", the square loop still shiny and wet, sunny balcony and blue sky behind",
    k("吹出來的泡泡還是圓的！", "不服氣"))
bub("swirl-bubble", "Close-up of " + BUBBLE + " floating in the sunny air above a balcony, the colours swirling across its surface, blue sky behind",
    k("而且它身上的顏色一直轉，", "比手畫腳", "S:swirl"))
bub("pop-bubble", "Close-up of a round soap bubble in the sunny air at the moment it bursts, a small dark grey patch at its top and a ring of tiny sparkling droplets flying outward, blue sky behind",
    k("最後頭頂變黑，就破了！", "可惜"))
# Thumbnail shot (fixed before keyframes, explainer-series/README.md): the kid big, a clear face, the wand in hand.
kid("kid-wand", K("holding up a silver wire bubble wand with a square loop in one hand and a small clear bottle in the other, a round soap bubble beside her face, a surprised open-mouthed face", where=BALCONY),
    k("就是這支跟這瓶！", "舉起來"))
chief("chief-look", C("leaning forward with a curious smile, one hand on her chin", close=True),
      c("給我看看。很平常的方框和泡泡水嘛。", "接住上一句"), c("可是你剛剛說的，每一句都很怪。"))
kid("kid-which-q", K("holding up two fingers with a curious face", where=HOME),
    k("哪裡怪？", "句尾上揚"))
chief("chief-two", C("holding up two fingers with a friendly smile", close=True),
      c("框是方的，泡泡卻是圓的。", None, "S:square"), c("泡泡水沒有顏色，泡泡卻有。", None, "S:paint"))
kid("kid-bottle", K("holding up a small plain clear bottle of colourless bubble liquid and staring at it with a puzzled face", where=HOME),
    k("對耶，這瓶明明是透明的！", "發現"))
chief("chief-tease", C("holding up one finger with a mysterious playful smile", close=True),
      c("還有更怪的：兩顆泡泡黏在一起時，", "賣關子"), c("中間那片牆會往哪邊彎？等一下你就知道。", None, "S:push"))
bub("dark-top-tease", "Close-up of a round soap bubble resting on a square silver wire loop, its lower half shimmering in pink, green and gold bands and its very top a small smooth dark grey patch, sunny balcony background",
    c("頂上變黑也不是隨便黑的，它在跟你說一件事。", "賣關子", "S:dark"))
chief("chief-promise", C("holding up a silver wire bubble wand with a square loop beside her face with a warm inviting smile"),
      c("你每次吹泡泡，這些事都在你眼前發生，", "轉向觀眾"), c("今天就用你這支方框跟這瓶，把它們全部找出來。"))
kid("kid-main-q", K("holding the square wire bubble wand in both hands and staring at it with a puzzled face", where=BALCONY),
    k("全部？", "想不通"), k("一支方框就夠？", "句尾上揚", "S:main"))

# ---------- 第一章：一直想縮小的那層皮 ----------
chief("chief-start", C("tapping the square loop of a silver wire bubble wand with one finger, a curious smile", close=True),
      c("夠。來，你是怎麼吹的？吹給我看看。", "接住上一句"), chapter="一直想縮小的那層皮")
kid("kid-dip", K("dipping a silver wire square bubble wand into a small clear bottle with a concentrating face", where=BALCONY),
    k("沾一下泡泡水，", "示範"), k("框裡就有一片薄薄的皮！"))
bub("film-in-wand", "Close-up of " + WAND + " held level in the sunny air, a flat shiny transparent soap film stretched across the square loop like a tiny window, a faint rainbow sheen on it",
    c("對，框上那片皮是平平的。"), c("你一吹，它就被撐大，包住一團空氣。"))
kid("kid-made-q", K("peering closely at the shiny film in a square wire wand with a curious face", where=BALCONY),
    k("這層皮是什麼做的？", "句尾上揚"))
chief("chief-made", C("holding up a small clear bottle of bubble liquid and swirling it gently, a friendly smile", close=True),
      c("就是你這瓶泡泡水：很多水，加上一點肥皂。"), c("肥皂夾在兩面，水夾在中間，像一片很薄的三明治。"))
kid("kid-square-q", K("holding up the square wire wand and pointing at its square loop with a puzzled frown", where=BALCONY),
    k("可是框是方的耶，", "不解"), k("為什麼不吹出方的？", "句尾上揚"))
chief("chief-guess", C("pressing her palms slowly together as if squeezing something small, a thoughtful smile"),
      c("我的猜法是：這層皮，一直想把自己縮小。", None, "S:guess"))
kid("kid-shrink-doubt", K("tilting her head with a doubtful little frown, arms crossed", where=HOME),
    k("皮會自己縮？", "懷疑"))
bub("balloon-fly", "Medium shot of a plump red rubber balloon zooming away through a sunny living room as the air rushes out of its open neck, curly motion lines behind it, bright daylight",
    c("你吹過氣球吧？吹大的氣球皮，是被撐開的。", "轉向觀眾"), c("一放手，皮就把空氣擠出來。"))
kid("kid-balloon", K("laughing and spreading both arms wide like a zooming balloon", where=HOME),
    k("對，它會咻咻亂飛！", "笑"))
chief("chief-test", C("holding a silver wire square bubble wand towards the viewer with an inviting smile"),
      c("那我們來試：泡泡吹到一半，你停下來不吹，", "接住上一句"), c("你猜會怎樣？", "句尾上揚", "S:shrink"))
kid("kid-stay-guess", K("puffing out her cheeks proudly with a confident grin", where=BALCONY),
    k("我猜它會一直留著！", "很有把握的錯猜"))
bub("bubble-shrink", "Close-up of " + WAND + " with a small half-blown soap bubble on its square loop, the bubble shrinking back down towards the loop, soft curved motion lines around it, sunny balcony background",
    c("你試試看。泡泡會慢慢縮回去，"), c("最後在框裡，又變回一片平平的皮。", None, "P:shrink"))
kid("kid-shrank", K("pointing at a silver wire square bubble wand in her hand with a surprised delighted face", where=BALCONY),
    k("真的縮回去了！", "驚喜"), k("它跟氣球一樣會擠！"))
chief("chief-tension", C("pulling her two hands slowly inward towards her chest, a calm smile", close=True),
      c("對，這種一直往內拉、想縮小的力氣，"), c("科學家叫它表面張力。", None, "P:guess"))
kid("kid-round-q", K("drawing a big circle in the air with one finger and a curious face", where=HOME),
    k("那它為什麼要縮成圓的？", "句尾上揚"))
bub("bubble-free", "Wide shot of a single round transparent soap bubble floating alone high in a clear blue sky, soft swirling pink and green sheen, sunlight glinting on it",
    c("泡泡一離開框，那團空氣就被關在裡面了。"), c("空氣一樣多，皮卻想用最少的面積把它包住。"))
kid("kid-box-q", K("holding up a small square cardboard gift box in both hands with a hopeful face", where=HOME),
    k("包成方盒子，", "追問"), k("不行嗎？", "句尾上揚", "S:box"))
bub("box-ball", "Close-up of a small plain square cardboard gift box and a plain round red rubber ball of about the same size side by side on a wooden table" + ", plain warm pale cream background",
    c("不划算。包一樣多的空氣，方盒子要的皮，"), c("比圓球多了兩成多。", "數字放慢", "P:box"))
chief("chief-sphere", C("holding a small round ball up in one hand with a pleased smile", close=True),
      c("所有形狀裡，用的皮最少的，就是圓球。"))
kid("kid-stingy", K("pinching her thumb and finger close together with a cheeky teasing grin", where=HOME),
    k("才多兩成，", "調皮"), k("泡泡也要省？", "句尾上揚"))
chief("chief-stingy", C("laughing softly with one hand raised, a playful smile", close=True),
      c("對泡泡皮來說，能縮就縮，多一點都不肯。", "笑"))
bub("many-wands", "Close-up of three simple silver wire bubble wands lying side by side on a balcony table, one with a square loop, one with a triangle loop and one with a star-shaped loop, a perfectly round soap bubble floating up above each one, sunny balcony background",
    c("所以你的方框，只管得住框裡那一片皮。", None, "P:square"))
chief("chief-limit", C("holding up one deflated red balloon with an honest serious smile", close=True),
      c("先說清楚，氣球皮只是比喻。氣球放完氣，皮會鬆掉；"), c("泡泡皮不管縮得多小，都一直在拉。"))
kid("kid-always-q", K("hugging a big round beach ball with a wondering face", where=HOME),
    k("那泡泡，", "追問"), k("永遠都是圓的嗎？", "句尾上揚"))
chief("chief-alone", C("holding one finger up beside a single soap bubble floating near her shoulder, a careful smile"),
      c("不一定。我說的是飄在空中、只有一顆的泡泡。", "接住上一句"), c("停在濕濕的盤子上，就會變成半顆圓頂。"))
kid("kid-wall-q", K("holding up two fingers side by side close together with a curious wondering face", where=BALCONY),
    k("那兩顆黏在一起呢？", "追問"), k("還會是圓的嗎？", "章尾停住，句尾上揚", "S:wall"))

# ---------- 第二章：兩顆泡泡黏在一起 ----------
chief("chief-exam", C("holding two silver wire bubble wands, one in each hand, with a playful smile"),
      c("這就是剛剛那個猜法的考試。", "接住上一句"), c("你從同一瓶，吹兩顆一樣大的泡泡，讓它們碰一下。"), chapter="兩顆泡泡黏在一起")
kid("kid-pop-guess", K("squeezing her eyes half shut and covering her ears with both hands, an expectant grin", where=BALCONY),
    k("我猜一碰就破掉！", "很有把握的錯猜"))
bub("twin-bubbles", "Close-up of two equal round transparent soap bubbles joined together side by side in the sunny air, a perfectly flat round shiny wall between them, soft pink and green sheen, blue sky behind",
    c("常常不會破，它們會黏成一對。"), c("中間多了一片兩顆一起用的牆，而且是平的。", None, "P:wall"))
kid("kid-dot-guess", K("touching the tips of her two index fingers together with a surprised face", where=BALCONY),
    k("我還以為，", "驚訝"), k("只會碰到一個點！"))
chief("chief-share", C("pressing her two flat palms together with a knowing smile", close=True),
      c("那樣各包各的，皮用得比較多。"), c("還是想省皮：兩顆合用一片牆，比較省。"))
kid("kid-flat-q", K("pressing her two flat palms together in front of her chest with a curious face", where=BALCONY),
    k("那為什麼是平的？", "句尾上揚"))
chief("chief-flat", C("holding her two hands flat and level side by side with a calm smile", close=True),
      c("兩邊一樣大，誰也推不動誰，牆就平平的。"))
kid("kid-big-guess", K("holding one big round ball and one small round ball, one in each hand, with a confident grin", where=HOME),
    k("那一大一小呢？", "追問"), k("大的一定把小的壓扁！", "很有把握的錯猜", "S:big"))
chief("chief-recall-push", C("holding up one finger with a playful knowing smile", close=True),
      c("還記得我問，中間那片牆會往哪邊彎嗎？", "點名回呼"))
bub("small-big", "Close-up of a small round soap bubble stuck to the side of a big round soap bubble in the sunny air, the shared round wall between them curving outward into the big bubble like a small dome, soft pink and green sheen, blue sky behind",
    c("你看，中間那片牆，是往大泡泡那邊凸過去的。", None, "P:push"))
kid("kid-small-strong", K("making a small fist and looking at it with an amazed face", close=True, where=HOME),
    k("小的比較用力？", "不敢相信"))
chief("chief-curve", C("cupping one hand into a tight small curve and the other into a wide gentle curve, a thoughtful smile"),
      c("你可以這樣想：同一瓶泡泡水，皮拉的力氣都差不多。"), c("可是小泡泡彎得比較厲害，"))
chief("chief-squeeze", C("squeezing a small soft ball tightly in one hand with a curious smile", close=True),
      c("所以小泡泡的皮，把裡面的空氣壓得比較緊，"))
chief("chief-pressure", C("nodding with one hand open towards the viewer", close=True),
      c("所以是小的往大的那邊推。", None, "P:big"))
kid("kid-small-wins", K("jumping up with both arms raised high and a surprised delighted grin", where=PARK),
    k("小的反而贏了！", "驚訝"))
kid("kid-colour-q", K("holding the small clear bottle of bubble liquid up to the light with a puzzled face", where=BALCONY),
    k("形狀我懂了。", "想一想"), k("可是你說泡泡水沒顏色，", "不解"), k("顏色從哪來？", "章尾停住，句尾上揚"))

# ---------- 第三章：沒有顏料的顏色 ----------
chief("chief-clear", C("pouring a little clear liquid from a small bottle into her cupped palm, a curious smile"),
      c("好問題。顏料是沒有，那泡泡身上除了這層皮，還有什麼？", "接住上一句"), chapter="透明的泡泡水，變出了顏色")
kid("kid-tension-guess", K("snapping her fingers with a confident know-it-all grin", where=BALCONY),
    k("只有皮啊！", "很有把握"), k("是皮拉得太緊，", "很有把握的錯猜"), k("才變彩色的？", "句尾上揚", "S:tension"))
chief("chief-not-tension", C("shaking her head gently with a kind smile, one hand raised", close=True),
      c("很多人會這樣猜。可是這股往內拉的力氣，管的是形狀，", None, "P:tension"), c("顏色要找另一個角色：光。"))
kid("kid-white-q", K("shading her eyes with one hand and looking up at the sunny sky with a curious face", where=BALCONY),
    k("光不是白白的嗎？", "句尾上揚"))
chief("chief-white", C("holding one open hand up into a beam of warm sunlight from the side, a calm smile"),
      c("白光其實是很多種顏色混在一起。"), c("要是從裡面拿掉一種，剩下的，就會帶著顏色。"))
kid("kid-remove-q", K("pinching the air with two fingers as if picking something out, a curious face", where=HOME),
    k("拿掉一種？", "句尾上揚"))
chief("chief-yellow", C("holding up a small yellow lemon with a friendly smile", close=True),
      c("比方說，從白光裡拿掉藍色，剩下的看起來就偏黃。"))
kid("kid-who-q", K("narrowing her eyes with a curious detective-like frown", close=True, where=HOME),
    k("誰把顏色拿走？", "追問"))
chief("chief-two-faces", C("holding up a silver wire square bubble wand with a big shimmering soap bubble on it, a curious smile"),
      c("這層皮有外面和裡面兩個面。"), c("光照過來，兩個面都會把一點光，彈回你的眼睛。"))
kid("kid-two-light", K("holding up two fingers with a surprised face", where=HOME),
    k("一顆泡泡，", "驚訝"), k("彈回來兩道光？"))
chief("chief-longer", C("holding her two hands one slightly behind the other, a thoughtful smile", close=True),
      c("對。裡面那道，要在皮裡走一個來回，"), c("走的路，比外面那道長一點點。"))
kid("kid-so-what", K("shrugging with both palms up and a puzzled face", where=HOME),
    k("長一點點，", "不解"), k("又怎樣？", "句尾上揚"))
chief("chief-pond", C("holding two small round smooth pebbles in her open palm with a playful smile"),
      c("我們用水波來想。你往池塘裡，同時丟兩顆小石頭。", "轉向觀眾"))
bub("pond-rings", "Top-down view of a calm green pond in a sunny park with two small pebbles just dropped in, two sets of round ripple rings spreading out and overlapping in the middle, lily pads at the edge",
    c("兩圈水波碰在一起：高的碰到高的，就變得更高；"), c("高的碰到低的，就互相抵掉，水面平平的。"))
kid("kid-pond", K("crouching beside a small pond and pointing at ripples on the water with a delighted face", where=PARK),
    k("我在公園看過！", "想起來"), k("有的地方特別平！"))
chief("chief-flat-spot", C("crouching and pointing down at a calm patch of water in a small round tub, a pleased smile"),
      c("對，那就是兩圈水波，互相抵掉的地方。"))
chief("chief-light-wave", C("moving one hand in a gentle up-and-down wave through the air, a calm smile", close=True),
      c("光也可以想成一種波。兩道光一碰，"), c("有的顏色被加強，有的顏色被抵掉。", None, "P:paint"))
kid("kid-which-q2", K("tapping her chin with one finger and a thinking face", where=HOME),
    k("哪一種會被抵掉？", "句尾上揚", "S:thick"))
chief("chief-guess-thick", C("holding her thumb and finger a tiny gap apart near her eye, a curious smile", close=True),
      c("我的猜法是：要看這層皮有多厚。"), c("厚薄一變，裡面那道光多走的路就跟著變，"))
bub("two-colours", "Close-up of two round soap bubbles side by side in the sunny air, the left one shimmering mostly blue and the right one shimmering mostly gold, blue sky behind",
    c("被抵掉的顏色就換一種，你看到的顏色也跟著換。"), c("比方說，紅色被抵掉，剩下的就偏藍綠。"))
kid("kid-proof-q", K("putting both hands on her hips with a doubtful challenging grin", where=HOME),
    k("要怎麼知道，", "追問"), k("你猜得對不對？", "章尾停住，句尾上揚", "S:test"))

# ---------- 第四章：顏色跟著時間，還是跟著你的眼睛 ----------
chief("chief-watch", C("holding up a silver wire square bubble wand with a bubble hanging on it, an inviting smile"),
      c("拿你那一瓶來試。把泡泡吹在框上，先別讓它飛走，", "接住上一句"), c("頭不要動，盯著它看。", "轉向觀眾"), chapter="歪一下頭，顏色也跟著變")
kid("kid-stripes", K("holding a silver wire square bubble wand with a big bubble hanging on it and staring at it with wide eyes", where=BALCONY),
    k("顏色變成一條一條的，", "驚訝"), k("橫橫的！"))
bub("bubble-stripes", "Close-up of a big round soap bubble hanging from a square silver wire loop, its surface covered in neat horizontal bands of colour: pale gold at the top, then magenta, blue and green towards the bottom, sunny balcony background",
    c("對。泡泡水會被地球往下拉，慢慢往下流，"), c("底下比較厚，頂上越來越薄，顏色就排成一條一條。"))
kid("kid-moving", K("leaning close to a bubble hanging on her square wire wand with a fascinated face", where=BALCONY),
    k("而且它們一直往下跑！", "發現"))
chief("chief-time", C("sliding one flat hand slowly downward through the air, a pleased smile", close=True),
      c("時間一過，皮一直變薄，顏色就一條一條往下換。"), c("還記得我的猜法嗎？它過關了。", None, "P:test"))
kid("kid-swirl-q", K("drawing small swirls in the air with one finger and a curious face", where=BALCONY),
    k("那一開始，", "想起來"), k("顏色為什麼會打轉？", "句尾上揚"))
bub("swirl-flow", "Close-up of a big round soap bubble on a square silver wire loop, soft breeze lines beside it, its pink, green, blue and gold colours swirling across the surface like marbled paint, sunny balcony background",
    c("風一吹，泡泡水就在皮裡流來流去，"), c("厚的薄的換了位置，顏色就跟著打轉。", None, "P:swirl"))
chief("chief-recall-dark", C("pointing one finger up with a playful knowing smile", close=True),
      c("還記得我說，頂上變黑，是它在跟你說一件事嗎？", "點名回呼"))
kid("kid-black-q", K("leaning forward eagerly with both hands on her knees", where=BALCONY),
    k("記得！為什麼會變黑？", "句尾上揚"))
bub("bubble-dark-top", "Close-up of a round soap bubble on a square silver wire loop, a smooth dark grey cap spreading across its top while soft gold and pink bands shimmer below, sunny balcony background",
    c("頂上的皮比光的波還薄很多，兩道光不管是什麼顏色，"), c("都剛好互相抵掉。", None, "P:thick"))
chief("chief-no-light", C("cupping both empty hands open towards the viewer with a gentle smile", close=True),
      c("沒有光彈回你的眼睛，看起來就黑了。"))
kid("kid-black-pop", K("covering her mouth with both hands and wide worried eyes", where=BALCONY),
    k("所以變黑，", "緊張"), k("就是快破了？", "句尾上揚"))
chief("chief-black", C("holding her thumb and finger almost touching with a serious kind smile", close=True),
      c("它在說：我已經薄到快撐不住了。", None, "P:dark"), c("美國舊金山一間科學博物館說，這時候頂上的皮，"))
chief("chief-thin", C("squinting closely at the tiny gap between her thumb and finger with a playful amazed face", close=True),
      c("大約只有一毫米的四萬分之一。"), c("不過不是一黑就馬上破，常常還會撐一下下。"))
kid("kid-quick", K("leaning in close with wide eager eyes and both fists under her chin", where=BALCONY),
    k("那我要看快一點！", "笑"))
kid("kid-tilt", K("tilting her head far to one side while looking at a bubble on her square wire wand, a surprised face", where=BALCONY),
    k("可是所長，", "發現"), k("我一歪頭，", None), k("顏色也變了耶！", None, "S:tilt"))
chief("chief-tilt-q", C("tilting her head to one side with a curious playful smile", close=True),
      c("好觀察。那你覺得，是皮在你歪頭那一下變薄了嗎？", "接住上一句"))
kid("kid-tilt-guess", K("scratching her head with a thinking face", where=BALCONY),
    k("應該……", "猶豫"), k("沒有那麼巧吧？"))
chief("chief-angle", C("holding one hand flat and tilting it slowly to a slant, a thoughtful smile"),
      c("對，沒有那麼巧。皮的厚薄沒變，"), c("變的是光進來、彈到你眼睛的方向。"))
chief("chief-slant", C("drawing a slanted line in the air with one fingertip, a calm smile", close=True),
      c("光斜斜地穿過皮，裡面那道光多走的路，"), c("就跟直直穿過的時候不一樣長。", None, "P:tilt"))
kid("kid-again-path", K("pointing up with one finger and a bright realising grin", where=BALCONY),
    k("又是多走的路！", "恍然"))
chief("chief-second-test", C("holding up two fingers with a warm pleased smile", close=True),
      c("對，這下又多了一條線索。我原本只猜到厚薄，"), c("沒想到你歪個頭，就把我的猜法補齊了。"))
kid("kid-tell-q", K("looking back and forth between two bubbles with a puzzled frown", where=BALCONY),
    k("那我怎麼分得出來，", "追問"), k("是哪一種在變？", "句尾上揚", "S:tell"))
chief("chief-tell", C("holding her head very still and pointing at her own eye with a playful smile", close=True),
      c("還記得往下流的顏色嗎？那是皮在變薄；"), c("泡泡不動，你一歪頭顏色就跳，是方向在變。", None, "P:tell"))
chief("chief-honest", C("holding a silver wire square bubble wand with a colourful bubble on it at arm's length, an honest thoughtful smile"),
      c("還有一件事要老實說："), c("光看顏色，沒辦法準準地量出皮有多厚。"))
kid("kid-why-not", K("tilting her head with a curious frown", where=HOME),
    k("為什麼不行？", "句尾上揚"))
chief("chief-repeat", C("drawing a few loops in the air with one finger, a thoughtful smile"),
      c("因為皮越變越薄的時候，同一種顏色會出現好幾次，"), c("光看顏色，分不出是哪一次。"))
kid("kid-loop", K("spinning one finger in small circles in the air with a curious grin", where=HOME),
    k("像在繞圈圈！", "發現"))
chief("chief-clue", C("nodding with a calm honest smile, one finger raised", close=True),
      c("對，所以顏色只能當線索，不能當尺。"))
kid("kid-two-q", K("holding the square wire wand in one hand and the small clear bottle in the other, looking from one to the other with a thinking face", where=BALCONY),
    k("那形狀跟顏色，", "推理"), k("到底有沒有關係？", "章尾停住，句尾上揚", "S:two"))

# ---------- 收尾 ----------
chief("chief-answer", C("sitting on the edge of a desk and leaning forward with an inviting grin, one hand open towards the viewer"),
      c("有。你自己找找看：方框跟變黑，哪裡一樣？", "笑"), chapter="小問把方框跟變黑連起來了")
kid("kid-got-it", K("holding up the square wire bubble wand proudly with a big confident grin, a round bubble floating beside her", where=BALCONY),
    k("原來如此！", "恍然大悟"), k("全是同一層皮：", "篤定", "P:main"), k("就像你說的，", "篤定"), k("一縮變圓，一薄換色！", "篤定", "P:two"))
chief("chief-opinion", C("smiling with her hands clasped, a thoughtful look", close=True),
      c("說得好，形狀跟顏色，被你接起來了。", "笑"))
bub("bubble-thinning", "Close-up of a round soap bubble on a square silver wire loop shimmering with soft bands of gold, magenta and blue, a small dark grey cap just starting at its very top, sunny balcony background",
    c("我覺得最好玩的是：你天天吹的泡泡，藏了這麼多事。"))
kid("kid-blow-again", K("dipping the square wire wand into her small clear bottle with an excited grin", where=BALCONY),
    k("我要再吹一顆！", "興奮"))
chief("chief-observe", C("nodding with an encouraging smile, one finger raised", close=True),
      c("好啊。這次把泡泡留在框上，背後找一面深色的牆，", "轉向觀眾"), c("看看頂上變黑之前，最後一個顏色是什麼。"))
# The outro is three pictures, no card, no stamp (series README §3.2, §10.1): the kid gives a thumbs-up.
kid("outro", "Waist-up medium shot of the girl with a big happy smile giving a big cheerful thumbs-up with one hand, bright morning light",
    k("好，我去吹！", "開心大聲"))
chief("outro-chief", "Waist-up medium shot of the chief holding up a silver wire square bubble wand with a curious smile, filling the frame, a plain pale wall behind her, bright morning light",
      c("你的泡泡變黑之前，最後是什麼顏色？", "問句上揚，像聊天"), c("留言告訴我們。"))
chief("outro-wave", "Waist-up medium shot of the chief waving goodbye with a warm smile, a plain pale wall behind her, bright morning light",
      c("想一起找生活裡的為什麼，就訂閱原來如此事務所。", "誠懇"))

# ---------- assemble ----------
WHAT = {"main": "方框吹出圓泡泡、顏色轉、頭頂變黑，一支方框就找得出原因嗎", "square": "框是方的，泡泡為什麼是圓的",
        "paint": "泡泡水沒有顏色，泡泡為什麼有顏色", "push": "兩顆泡泡黏在一起，中間的牆往哪邊彎",
        "dark": "泡泡頂上變黑，是在說什麼", "guess": "這層皮是不是一直想把自己縮小",
        "shrink": "泡泡吹到一半停下來，會怎樣", "box": "包成方盒子不行嗎",
        "wall": "兩顆泡泡黏在一起，還會是圓的嗎", "big": "一大一小，是不是大的把小的壓扁",
        "tension": "是不是皮拉得太緊才變彩色",
        "thick": "哪一種顏色會被抵掉", "test": "怎麼知道「看厚薄」這個猜法對不對",
        "tilt": "一歪頭顏色也變，是皮變薄了嗎", "tell": "怎麼分出是厚薄在變還是方向在變",
        "two": "形狀跟顏色，到底有沒有關係", "swirl": "泡泡身上的顏色為什麼一直轉"}
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
    "series": {"slug": "sothatswhy", "episode": 6, "chapter": 1},
    # The series bed from P15 on (explainer-series/README.md, PR #2048): sothatswhy-bed-r2.m4a, remade from P02's paid take.
    "music": {"track": "sothatswhy-bed-r2.m4a", "sha256": "9bb4ba6fd16feb4a7f352144b2d89e9648acbbbbaa2173c27a7eefbdb70f28c6", "gain_db": -20, "duck_db": -10},
    "characters": CHARACTERS, "loops": loops,
    "youtube": {
        "category_id": 27, "made_for_kids": False, "default_language": "zh-TW",
        "title": "泡泡用方框吹也是圓的，顏色又從哪來？｜原來如此事務所",
        "description": "小問把鐵絲彎成方框吹泡泡，吹出來的還是圓的；泡泡水明明是透明的，泡泡身上的顏色卻一直轉，最後頭頂變黑就破了。一層薄薄的皮，怎麼同時管形狀又管顏色？\n\n"
                       "這一集，所長和小問跟著同一支方框、同一瓶泡泡水走：先用氣球皮的比喻，看泡泡皮怎麼一直想縮小、為什麼飄在空中的泡泡會被拉成圓的；"
                       "再讓兩顆、三顆泡泡黏在一起，考考這個說法——一樣大的中間是平平的牆，一大一小時，小的反而往大的那邊推。"
                       "接著換問顏色：光從皮的外面和裡面各彈回一道，像池塘裡兩圈水波碰在一起，有的顏色加強、有的被抵掉；最後用同一顆泡泡分出顏色是跟著時間在變，還是跟著你的眼睛在變。\n\n"
                       "本集插圖由 AI 生成，是示意，不是泡泡的照片。數字是大約的數字。光看照片上的顏色，沒辦法準確量出泡泡皮有多厚。每個說法的出處列在下方參考資料。\n\n資料截至 " + CHECKED,
        "tags": ["泡泡", "肥皂泡", "表面張力", "薄膜干涉", "顏色", "光", "科普", "原來如此事務所"]},
    "thumbnail": {"template": "thumb", "data": {"headline": "方框吹出\n**圓泡泡？**", "sub": "顏色藏在哪一層", "shot": "kid-wand", "subject": "right"}},
    "sources": [
        {"title": "Exploratorium (Ron Hipschman), Soap Bubbles: The Shape of Bubbles", "url": "https://annex.exploratorium.edu/ronh/bubbles/shape_of_bubbles.html", "checked_on": CHECKED},
        {"title": "Exploratorium (Ron Hipschman), Soap Bubbles: Sticky Water (surface tension)", "url": "https://annex.exploratorium.edu/ronh/bubbles/sticky_water.html", "checked_on": CHECKED},
        {"title": "Exploratorium (Ron Hipschman), Soap Bubbles: When Bubble Meets Bubble", "url": "https://annex.exploratorium.edu/ronh/bubbles/bubble_meets_bubble.html", "checked_on": CHECKED},
        {"title": "Exploratorium (Ron Hipschman), Soap Bubbles: Bubble Colors", "url": "https://annex.exploratorium.edu/ronh/bubbles/bubble_colors.html", "checked_on": CHECKED},
        {"title": "Exploratorium Science Explorer, See Colors in Bubbles (bubble dome activity)", "url": "https://annex.exploratorium.edu/science-explorer/bub_dome.html", "checked_on": CHECKED},
        {"title": "Virginia Tech / James Madison University Bubble Physics, Properties of Bubbles", "url": "https://www1.phys.vt.edu/bubble/properties-of-bubbles.html", "checked_on": CHECKED},
        {"title": "Virginia Tech / James Madison University Bubble Physics, Introduction and Basic Information (Young-Laplace, Plateau laws)", "url": "https://www1.phys.vt.edu/bubble/basic-information.html", "checked_on": CHECKED},
        {"title": "Wolfram MathWorld, Double Bubble", "url": "https://mathworld.wolfram.com/DoubleBubble.html", "checked_on": CHECKED},
        {"title": "HyperPhysics (Georgia State University), Soap Film Interference", "url": "https://hyperphysics.phy-astr.gsu.edu/hbase/phyopt/soapfilm.html", "checked_on": CHECKED},
        {"title": "University of Colorado Boulder Physics Undergraduate Labs, Interference in a Soap Film (demo 6D30.20)", "url": "https://physicslabs.colorado.edu/demos/optics/interference/thin-films/interference-in-a-soap-film/", "checked_on": CHECKED},
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
hooks, t, last, setups, gaps = [], 0.0, 0.0, set(loops_s.values()), []
for s in body:
    for l in s["lines"]:
        t += length(l["text"]) / RATE
        if l["text"].endswith("？") or l["id"] in setups:
            if t - last > 45: gaps.append(f"{t - last:.0f} s before {l['id']}")
            last = t
for g in gaps: print(f"  hook gap {g}", file=sys.stderr)
assert not gaps, "a stretch longer than 45 s without a question or a planted loop"
assert len(loops) >= 11, "11 minutes need at least 11 loops (brief: loops >= 11, every one paid off)"
assert 2050 <= body_chars <= 2400, f"body {body_chars} characters: write 2,050–2,400 (blind round 1 cut the 120° detour) (README §9, 3.2 chars/s; EPISODES.md gives P06 10–12 min)"
cams = [s["data"]["camera"] for s in scenes]
assert all(not (a == b == c_) for a, b, c_ in zip(cams, cams[1:], cams[2:])), "three shots in a row with the same camera"
