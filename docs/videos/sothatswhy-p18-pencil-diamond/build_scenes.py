"""Generate video.json for sothatswhy-p18-pencil-diamond (原來如此事務所 對話版 P18).

Run `python3 build_scenes.py` from anywhere: it rewrites video.json next to this file and freezes
every shot's camera move in cameras.json (a shot keeps the camera it was first given, so deleting
a shot never shifts the others: the camera is in the keyframe cache key).
Edit lines and prompts here, never in video.json.
Started from a copy of sothatswhy-p17-gecko-feet/build_scenes.py (series constants, helpers,
assembly and self-checks unchanged; the kid tail also restates the folded hood, P17's lesson); the content is new.
`script.md` is written by `node tools/video/cli.mjs script --slug sothatswhy-p18-pencil-diamond` after this runs.
"""
import itertools, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = "sothatswhy-p18-pencil-diamond"
CHECKED = "2026-11-09"

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
def _shot(id, prompt, chars, lines, chapter):
    prompt = prompt + EXTRA.get(id, "")
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
def model(id, prompt, *lines, chapter=None):
    """The wooden ball-and-stick toy that stands for carbon (BALLS): an object shot like scene(), kept as its
    own helper so every model shot shares the one drawing language (P17: micro-mechanisms come out wrong)."""
    scene(id, prompt, *lines, chapter=chapter)
def k(t, e=None, tag=None): return ("kid", t, e, tag)
def c(t, e=None, tag=None): return ("chief", t, e, tag)

def C(action, close=False):
    return ("Head-and-shoulders close-up" if close else "Waist-up medium shot") + " of the chief " + action + ", " + WALL + ", " + DAY
def K(action, close=False, where=None):
    return ("Head-and-shoulders close-up" if close else "Waist-up medium shot") + " of the girl " + (where + " " if where else "") + action + ", " + DAY

HOME = "in a bright sunny Taiwanese apartment living room"
DESK = "at a small wooden desk by a sunny window"
PARK = "in a sunny park playground"
# One drawing language for the whole episode (README §10.5, and the P17 lesson that the image model cannot draw
# atoms, bonds or lattices): carbon is drawn as ONE box of plain wooden building toys, the same box every time.
# Graphite is that toy built as flat honeycomb nets stacked loosely like trays; diamond is the same toy built as a
# sturdy climbing frame joined in every direction. Nothing is counted, nothing depends on an arrow or a direction.
BALLS = "plain round unpainted wooden balls joined by short plain wooden sticks, a simple children's building toy"
NET = "one flat honeycomb net made of " + BALLS + ", lying flat"
STACK = "a loose stack of five flat honeycomb nets made of " + BALLS + ", stacked like trays with clear gaps between the layers"
FRAME = "a sturdy chunky climbing frame made of " + BALLS + ", the sticks joined in every direction into one solid block"
STROKE = "a thick dark grey pencil stroke on a plain white drawing sheet"
GEM = "a single small clear sparkling cut diamond"
FLATDRAW = ", simple flat 2D cartoon drawing with clean ink outlines, plain pale cream background"

# ---------- 開場（系列片頭之後直接進場景，不做濃縮；答案都不先講）----------
# The first picture is the problem itself (owner from P08 on): the smudged drawing, with nobody in it.
scene("smudged-drawing", "Close-up of a child's simple pencil drawing of a little house, a tree and a round sun on a plain white drawing sheet on a sunny wooden desk, the grey pencil lines smeared into a soft grey blur across one side, a yellow pencil lying beside it, " + DAY,
      k("所長！我畫了一整張圖，", "委屈，跑進來報案的語氣"), chapter="糊掉的那張畫")
scene("smudge-close", "Extreme close-up of soft grey pencil lines on a plain white drawing sheet smeared into a wide grey blur, the edge of the smear fading out, " + DAY,
      k("手一擦，全部糊掉了！", "委屈"))
# Thumbnail shot (fixed before keyframes, explainer-series/README.md): the kid big, a clear face, the pencil in hand.
kid("kid-grey-hand", K("holding up one open hand towards the viewer, the side of her palm smudged soft grey, a yellow pencil in her other hand, a surprised open-mouthed face", where=DESK),
    k("你看，我的手也黑黑的！", "攤開手"))
chief("chief-look", C("leaning forward with a curious smile, one hand on her chin", close=True),
      c("給我看看。你手上這層黑黑的，", "接住上一句"), c("大部分是從你的鉛筆芯磨下來的。"))
kid("kid-smudge-q", K("holding a yellow pencil up close to her face and squinting at its dark tip", where=DESK),
    k("鉛筆芯怎麼這麼容易掉？", "句尾上揚", "S:smudge"))
scene("gem-velvet", "Close-up of " + GEM + " resting on a dark blue velvet cloth, catching the sunlight with tiny rainbow glints, " + DAY,
      c("這要從一件怪事說起：這層黑黑的東西，", "賣關子"), c("跟亮晶晶的鑽石，都是碳組成的。"))
kid("kid-no-way", K("shaking her head with both hands up and a disbelieving frown", where=HOME),
    k("騙人！鑽石那麼硬，", "不相信"), k("鉛筆芯一擦就掉耶！"))
chief("chief-tease", C("holding up one finger with a mysterious playful smile", close=True),
      c("沒騙你。還有更怪的：最硬的鑽石，其實也有怕的東西。", "接住上一句，賣關子", "S:hammer"))
scene("stroke-tease", "Close-up of " + STROKE + ", a yellow pencil lying beside it on a sunny wooden desk, " + DAY,
      c("你這支鉛筆畫的線，還能做到一件鑽石做不到的事。", "賣關子", "S:lamp"))
chief("chief-promise", C("holding up a yellow pencil beside her face with a warm inviting smile"),
      c("兩樣東西只差了一件事，"), c("答案就藏在你每天握的這支鉛筆裡。"))
kid("kid-main-q", K("holding her yellow pencil in both hands and staring at it with a puzzled face", where=DESK),
    k("同樣都是碳，", "想不通"), k("怎麼會差這麼多？", "句尾上揚", "S:main"))

# ---------- 第一章：先看鉛筆留下什麼 ----------
chief("chief-start", C("tapping the tip of a yellow pencil with one finger, a curious smile", close=True),
      c("你剛剛問筆芯怎麼這麼容易掉，", "接住上一句"), c("先拆開來看：它其實是兩樣東西混在一起的。", None, "S:mix"), chapter="筆芯裡不只有碳")
kid("kid-which-q", K("holding up two fingers with a curious face", close=True),
    k("哪兩樣？", "句尾上揚"))
scene("two-powders", "Close-up of two small neat heaps on a plain wooden board, one heap of shiny dark grey powder with a metallic sheen and one heap of soft pale grey clay powder, " + DAY,
      c("一樣是黑黑亮亮的石墨，"), c("另一樣是黏土，就是可以捏陶的那種土。", None, "P:mix"))
kid("kid-clay-q", K("holding a small lump of grey clay in her palm with a surprised face", where=DESK),
    k("土也能寫字？", "驚訝"))
chief("chief-clay", C("pressing her palms together as if squeezing dough, a friendly smile"),
      c("土自己寫不黑。黏土是把石墨黏成一根，"), c("讓筆芯有形狀，也比較牢。"))
scene("two-strokes", "Close-up of two short pencil strokes side by side on a plain white drawing sheet, the left stroke pale silvery grey and thin, the right stroke deep soft black and wide, two yellow pencils lying below them, " + DAY,
      c("你有沒有發現，有的鉛筆畫起來特別黑、特別軟？", None, "S:dark"))
kid("kid-art-class", K("nodding fast with a bright remembering face, holding up a yellow pencil", where=DESK),
    k("有！我畫畫那支！", "想起來"), k("為什麼比較黑？", "句尾上揚"))
chief("chief-ratio", C("holding a short dark pencil in one hand and a long pale pencil in the other, smiling", close=True),
      c("那種筆芯裡，石墨比較多。", None, "P:dark"), c("黏土越多，筆芯越硬，線也越淡。"))
kid("kid-mine-graphite", K("holding up a short stubby yellow pencil with a proud grin", close=True, where=DESK),
    k("我那支一定很多石墨！", "得意"))
kid("kid-graphite-q", K("rubbing the grey side of one palm with a finger of her other hand, a thinking face", where=DESK),
    k("所以黑黑的是石墨？", "句尾上揚"))
chief("chief-carbon", C("nodding with one hand open towards the viewer", close=True),
      c("對。你手上那層，大部分就是石墨，"), c("就是我說，跟鑽石一樣的那種碳。"))
kid("kid-slick", K("rubbing her grey fingertip and thumb together with a curious face", close=True, where=DESK),
    k("我手上這層，摸起來滑滑的！", "發現"))
chief("chief-slick", C("rubbing her fingertip and thumb together with a curious smile", close=True),
      c("對，石墨摸起來有點滑，還帶一點金屬亮光。"), c("人們把它混進黏土做成筆芯，已經用了很久。"))
kid("kid-diamond-guess", K("raising one finger with a confident know-it-all grin", where=HOME),
    k("那鑽石呢？", "很有把握"), k("一定是別的東西吧？", "很有把握的錯猜", "S:diamond"))
kid("kid-ring", K("holding a tiny sparkling ring between her finger and thumb and gazing at it", close=True),
    k("我媽媽的戒指上，", "想起來"), k("就有一小顆！"))
scene("gem-close", "Close-up of " + GEM + " sitting on a smooth pale stone, clear as water, with soft sparkles, " + DAY,
      c("你媽媽那顆，也不是別的東西。"), c("就是我剛說的，幾乎全是碳。"))
kid("kid-better-guess", K("tilting her head with a hopeful grin, one finger on her chin", close=True),
    k("那是比較厲害的碳？", "再猜"))
chief("chief-same-carbon", C("holding up two identical small plain wooden balls, one in each hand, a playful smile"),
      c("碳就是碳。石墨裡的碳，跟鑽石裡的碳，", None, "P:diamond"), c("一顆一顆拿出來比，是一模一樣的。"))
chief("chief-ingredients", C("shrugging with open palms and a knowing smile", close=True),
      c("裡面是什麼東西，科學家叫做成分。"))
kid("kid-where-q", K("crossing her arms with a puzzled frown", where=HOME),
    k("那到底差在哪裡？", "句尾上揚"))
chief("chief-arrange", C("holding a small wooden box of building toys with a curious smile"),
      c("差在這些碳，是怎麼排、怎麼手牽手的。"))
kid("kid-build-q", K("leaning forward with both fists under her chin and wide doubtful eyes", close=True),
    k("排法不一樣，", "懷疑"), k("就差這麼多嗎？", "章尾停住，句尾上揚", "S:build"))

# ---------- 第二章：同樣的碳排成不同結構 ----------
chief("chief-blocks", C("opening a small wooden box full of plain wooden balls and short sticks, a bright smile"),
      c("會。我們拿一盒積木，把兩種排法搭出來。", "接住上一句"), chapter="同一盒積木，兩種搭法")
model("toy-box", "Close-up of an open wooden box full of " + BALLS + ", some balls already joined by sticks, on a sunny wooden table, " + DAY,
      c("每一顆小木球是一顆碳，"), c("小木棍，就是它們互相牽著的手。"))
kid("kid-my-blocks", K("holding a few wooden balls joined by sticks in her hands with a happy grin", where=HOME),
    k("像我家的積木！", "開心"), k("球是碳，棍子是手！", "整理"))
kid("kid-squeeze-guess", K("squeezing her two fists together tightly with a confident grin", close=True),
    k("我猜鑽石的碳，", "很有把握的錯猜"), k("是被擠得比較緊！", None, "S:squeeze"))
chief("chief-squeeze", C("squeezing a soft round stress ball in one hand with a fair-minded smile"),
      c("這個猜法先記著，等一下量給你看。"), c("不過最大的差別，在每顆碳牽幾隻手。"))
chief("chief-four-hands", C("holding up four fingers with a friendly smile", close=True),
      c("每一顆碳，最多能牽四隻手。"))
model("flat-net", "Close-up of " + NET + " on a sunny table, " + DAY,
      c("石墨是這樣搭的：每顆球只牽旁邊三顆，"), c("全部在同一個平面上，搭成一張平平的網。"))
kid("kid-spare-hand-q", K("holding up three fingers and then wiggling her thumb with a curious face", close=True),
    k("只牽三顆？", "發現"), k("那不是空著一隻手？", "句尾上揚", "S:hand"))
chief("chief-spare-later", C("pointing at the girl's side with a pleased smile", close=True),
      c("你數得真仔細。那隻空著的手很重要，", "笑"), c("我們等一下回來看。"))
model("net-stack", "Medium shot of " + STACK + ", on a sunny wooden table, " + DAY,
      c("一張網本身很牢，可是石墨是很多張網，"), c("一層一層疊起來的。"))
kid("kid-glue-q", K("pressing her two flat palms together and pulling them apart with a curious face", close=True),
    k("那一層一層之間，", "猜"), k("是用膠黏起來的嗎？", "句尾上揚"))
model("net-gap", "Close-up from the side of " + STACK + ", the wide empty gaps between the layers clearly visible" + FLATDRAW,
      c("層跟層之間，沒有木棍連著，只靠很弱的力氣吸住。"), c("而且離得比較遠，"))
chief("chief-twice", C("holding her two hands flat one above the other with a wide gap between them, a curious smile"),
      c("大約是同一張網裡，兩顆球距離的兩倍多。"))
kid("kid-far-q", K("holding her two flat hands far apart one above the other with a curious face"),
    k("離那麼遠，", "好奇"), k("會怎麼樣？", "句尾上揚", "S:far"))
chief("chief-far-later", C("raising one finger with a patient smile", close=True),
      c("先記住，等一下推一推就知道。"))
kid("kid-strong-soft-q", K("holding a flat wooden building-toy net in both hands and squeezing it with a puzzled face", where=HOME),
    k("網子很牢，", "不解"), k("整疊怎麼會軟？", "句尾上揚"))
chief("chief-soft-where", C("holding two flat hands one above the other and sliding the top one, a knowing smile", close=True),
      c("因為軟的地方不在網裡面，"), c("在層跟層的中間。好，現在換鑽石。"))
model("toy-frame", "Medium shot of " + FRAME + ", standing on a sunny wooden table, " + DAY,
      c("同一盒積木，可是每一顆球，四隻手全部牽滿，"), c("伸向四個不同的方向。"))
kid("kid-all-used-q", K("holding up four fingers and looking at them with a curious face", close=True),
    k("四隻手都用光了？", "句尾上揚"))
chief("chief-frame", C("lacing the fingers of both hands together firmly with a confident smile", close=True),
      c("對，一隻空手都沒有，這點也要記住。"), c("整塊連成一個到處都接在一起的攀爬架。", None, "P:build"))
kid("kid-jungle-gym", K("holding the bars of a sturdy red playground climbing frame with both hands and grinning", where=PARK),
    k("像公園的攀爬架！", "興奮"), k("那個很牢！"))
kid("kid-two-ways", K("holding a flat wooden net in one hand and a small wooden climbing frame toy in the other, a proud grin", where=HOME),
    k("石墨是一疊網，", "整理"), k("鑽石是攀爬架，對吧？", "句尾上揚"))
chief("chief-model", C("holding one wooden ball up between two fingers with an honest serious smile", close=True),
      c("先說清楚，這只是一個模型。"), c("真的碳不是木球，牽手也不是木棍。"))
chief("chief-model-limit", C("laying a short wooden stick across her open palm and pointing at it with her other hand"),
      c("木棍只是幫我們看出，誰跟誰連在一起，"), c("連得多牢。"))
kid("kid-trust-q", K("narrowing her eyes with a doubtful little smile", close=True),
    k("那怎麼知道它準不準？", "追問"))
chief("chief-guess-tool", C("holding the small wooden box of building toys towards the viewer with an inviting smile"),
      c("我覺得它好用的地方，是你可以拿它來猜，"), c("再去量，猜對了，才算數。"))
kid("kid-harder-q", K("tapping her pencil against her chin with a curious face", close=True, where=DESK),
    k("那它猜得出來，", "追問"), k("誰比較硬嗎？", "章尾停住，句尾上揚", "S:harder"))

# ---------- 第三章：結構怎麼改變滑動和硬度 ----------
chief("chief-push", C("holding one flat hand out and pushing it gently sideways through the air, a playful smile"),
      c("猜得出來。先推石墨那一疊網試試。", "接住上一句"), chapter="推一推、刮一刮、敲一敲")
model("net-slide", "Medium shot of " + STACK + ", the top two nets slid sideways off the stack and fanned out, " + DAY,
      c("還記得層跟層離得遠嗎？又只是輕輕吸住，", "點名回呼"), c("所以輕輕一推，上面幾層就整片滑開了。", None, "P:far"))
kid("kid-slide", K("pushing one flat open hand forward through the air with a delighted surprised face", where=DESK),
    k("一推就滑走了！", "發現"))

scene("pencil-writes", "Close-up of a yellow pencil tip drawing a thick dark grey line on a plain white drawing sheet, tiny shiny grey flakes left along the line, " + DAY,
      c("對，你寫字就是這樣。紙面粗粗的，筆芯一磨，"), c("外面幾層石墨就滑下來，留成一條黑線。"))
kid("kid-my-hand-q", K("looking at the grey side of her palm with a dawning realisation", close=True, where=DESK),
    k("那我的手也是？", "恍然"))
chief("chief-smudge", C("brushing her palm across the air with a kind smile", close=True),
      c("對，這就是你一開始問的。手一擦，", "點名回呼", "P:smudge"), c("那些薄薄的石墨又滑到手上，畫就糊了。"))
chief("chief-weight", C("holding out both open palms as if weighing two small things, a curious smile"),
      c("這個模型還猜得到一件事：疊網中間空隙大，"), c("同樣大小，石墨應該比較輕。"))
kid("kid-weight-q", K("holding a small dark grey pebble in one palm and weighing it with a curious face", close=True, where=DESK),
    k("真的比較輕嗎？", "句尾上揚"))
scene("weight-pair", "Close-up of a dark grey chunk of shiny graphite and " + GEM + " of the same size side by side on a smooth pale wooden table, " + DAY,
      c("還記得你猜，鑽石的碳擠得比較緊嗎？", "點名回呼"), c("同樣大小的鑽石，大約比石墨重了一半多。", None, "P:squeeze"))
kid("kid-guessed", K("pumping one fist with a proud delighted grin", where=DESK),
    k("我猜對了！", "得意"))
chief("chief-no-gaps", C("pressing her two flat hands firmly together with a warm smile", close=True),
      c("對，攀爬架裡沒有那種層跟層中間的大空隙。"))
model("frame-push", "Medium shot of " + FRAME + ", standing firm and unmoved on a sunny wooden table, " + DAY,
      c("再推鑽石的攀爬架。每顆球都被四面八方牽住，"), c("沒有一層可以滑開。"))
chief("chief-break-hands", C("pulling her two tightly clasped hands apart with an effortful playful face", close=True),
      c("要刮下一點點，就得把好多隻牽得很牢的手，"), c("一起扯斷。"))
kid("kid-graphite-easy", K("flicking a tiny grey flake off her fingertip with a thinking face", close=True, where=DESK),
    k("石墨就不用扯斷？", "對照"))
chief("chief-graphite-easy", C("sliding one flat hand off the other with an easy smile", close=True),
      c("對，只要讓一層滑開，網子裡的手，一隻都不用斷。"))
kid("kid-scratch-q", K("holding up a small smooth pebble and rubbing its surface with one fingertip, curious face", where=DESK),
    k("所以鑽石很難刮傷？", "句尾上揚"))
chief("chief-hardness", C("drawing a short line in the air with one fingertip, a calm smile", close=True),
      c("對。科學家說的硬，就是不容易被刮傷。"))
scene("hardness-row", "Medium shot of a neat row of ten plain rough mineral stones on a sunny wooden shelf, arranged from a soft chalky white stone on the left to " + GEM + " on the right, " + DAY,
      c("有一種排硬度的方法：誰刮得傷誰，誰就比較硬，"), c("從最軟的一，排到最硬的十。"))
scene("graphite-low", "Close-up of a soft chunk of shiny dark grey graphite crumbling into flakes beside " + GEM + " on a smooth stone, " + DAY,
      c("石墨大約只有一到二，用指甲就刮得動；", None, "P:harder"), c("鑽石是最上面的十。"), c("只有鑽石，才刮得動鑽石。"))
kid("kid-unbreak-guess", K("making a strong fist with a confident proud grin", where=HOME),
    k("那鑽石最硬，", "很有把握"), k("一定打不破！", "很有把握的錯猜", "S:unbreak"))
chief("chief-two-things", C("holding up two fingers with a gentle smile", close=True),
      c("很多人都這樣猜。可是硬，跟不容易碎，是兩回事。"))
kid("kid-differ-q", K("scratching her head with a puzzled face", close=True),
    k("哪裡不一樣？", "句尾上揚"))
chief("chief-tough", C("tapping one fist lightly into her other palm, a thoughtful look"),
      c("硬，就是剛剛說的，比誰不容易被刮傷；"), c("耐敲，是比被重重敲一下，會不會裂開。"))
chief("chief-glass", C("holding up a plain clear drinking glass with a thoughtful smile", close=True),
      c("你想想家裡的玻璃杯：用指甲刮不出痕跡，"), c("掉到地上，卻可能摔碎。", "轉向觀眾"))
kid("kid-broke-glass", K("covering her mouth with one hand and a sheepish embarrassed grin", close=True, where=HOME),
    k("我打破過一個……", "不好意思"))
chief("chief-fear-back", C("holding up a small steel hammer with a mysterious playful smile", close=True),
      c("還記得我說，最硬的鑽石，也有怕的東西嗎？", "點名回呼"))
kid("kid-fear-q", K("leaning forward with wide curious eyes and both hands on her knees", where=HOME),
    k("記得！它怕什麼？", "句尾上揚"))
chief("chief-fear", C("tapping the hammer lightly into her open palm with a knowing smile", close=True),
      c("怕重重的一敲。", None, "P:hammer"))
scene("hammer-chip", "Close-up of a small steel hammer lying on a smooth steel block beside a tiny clear crystal that has split into a few sparkling pieces, " + DAY,
      c("研究寶石的機構說，這樣一敲，"), c("鑽石還是可能裂開，或缺掉一角。", None, "P:unbreak"))
kid("kid-frame-break-q", K("holding the bars of a sturdy red playground climbing frame with a surprised face", where=PARK),
    k("攀爬架也會裂？", "驚訝"))
chief("chief-weak-way", C("tilting one flat hand slowly to one side, a thoughtful smile", close=True),
      c("他們說，鑽石裡有幾個方向，跨過去牽著的手比較少，"), c("順著那些方向，就比較容易裂開。"))
scene("cleave-line", "Close-up of a small clear rough diamond crystal resting on a smooth steel block, a thin bright line of light running straight across it where it will split, a small steel chisel lying beside it, " + DAY,
      c("切鑽石的人，有時就是順著這種方向，故意把它敲開。"))

kid("kid-on-purpose", K("covering her open mouth with both hands in amazement", close=True),
    k("原來是故意敲的！", "驚訝"))
chief("chief-use-weak", C("tapping one finger on a small clear crystal held in her other hand, a knowing smile", close=True),
      c("對，他們就是利用它最怕的那幾個方向。"))
kid("kid-more-q", K("holding her yellow pencil up beside her face with an eager curious face", where=DESK),
    k("硬和碎都猜過了，", "追問"), k("模型還能猜別的嗎？", "章尾停住，句尾上揚", "S:more"))

# ---------- 第四章：還有哪個性質能檢驗 ----------
chief("chief-lamp-back", C("holding up a small round battery between two fingers with a playful smile", close=True),
      c("能。還記得我說，你的鉛筆線能做到一件事，", "點名回呼", "P:more"), c("鑽石做不到嗎？"), chapter="讓小燈亮起來的鉛筆線")
kid("kid-what-thing-q", K("leaning forward eagerly with both hands on the desk", where=DESK),
    k("記得！是什麼事？", "句尾上揚"))
scene("stroke-dark", "Close-up of " + STROKE + ", one end touching a round battery, a tiny unlit LED standing at the other end, " + DAY,
      c("讓電通過。用軟一點的鉛筆，用力畫一條", None, "P:lamp"), c("又粗又黑、不斷掉的線，兩頭接上電池和小燈。"))
kid("kid-metal-guess", K("frowning with her arms crossed and a doubtful face", where=DESK),
    k("可是電要走電線，", "懷疑"), k("鉛筆又不是金屬！", "很有把握的錯猜", "S:metal"))
scene("stroke-lit", "Close-up of " + STROKE + ", one end touching a round battery, a tiny LED at the other end glowing warm yellow, " + DAY,
      c("可是有一間科學博物館，教大家做這個實驗，"), c("那顆小小的燈，真的亮了。", None, "P:metal"))
kid("kid-why-graphite-q", K("staring wide-eyed at a tiny glowing LED on her desk", where=DESK),
    k("好神奇！", "驚喜"), k("為什麼石墨可以？", "句尾上揚"))
chief("chief-hand-back", C("holding up three fingers and wiggling her thumb with a knowing smile", close=True),
      c("記得網子裡，每顆球空著的那隻手嗎？", "點名回呼"))
chief("chief-electron", C("running one fingertip along an imaginary line in the air with a curious smile"),
      c("電流，可以想成很多帶電的小東西往前跑，"), c("這些小東西叫電子。"))
kid("kid-run-where-q", K("tracing a line on her desk with one fingertip and a curious face", close=True, where=DESK),
    k("電子要跑去哪？", "句尾上揚"))
model("net-glow", "Close-up of " + NET + ", a soft warm golden glow running along the sticks of the net from one side to the other" + FLATDRAW,
      c("石墨每顆碳那隻空著的手，讓一個電子能跑，"), c("沿著整張網跑來跑去。", None, "P:hand"))
scene("stroke-path", "Close-up of " + STROKE + ", a soft warm golden glow running along the stroke from a round battery at one end to a tiny glowing LED at the other end, " + DAY,
      c("你那條鉛筆線，就是給電子跑的路，"), c("一路跑過小燈，燈就亮了。"))
kid("kid-diamond-lamp-q", K("holding up a tiny clear crystal between two fingers with a curious face", close=True, where=DESK),
    k("那鑽石呢？", "追問"), k("也會亮嗎？", "句尾上揚", "S:dlamp"))
scene("gem-dark", "Close-up of " + GEM + " sitting between two short wires on a sunny wooden desk, one wire running to a round battery, a tiny unlit LED beside it, " + DAY,
      c("鑽石的四隻手全部牽滿，電子被牢牢抓住，跑不動。"), c("所以一般的鑽石，幾乎不導電，燈不會亮。", None, "P:dlamp"))
chief("chief-blue", C("holding one hand on her chest with an honest smile", close=True),
      c("老實說，有一種很少見的藍色鑽石，"), c("裡面混了一點別的東西，會導一點電。"))
kid("kid-blue-q", K("raising her eyebrows high with an amazed open-mouthed face", close=True),
    k("藍色的鑽石也有？", "驚訝"))
chief("chief-rare", C("nodding with a small honest smile, one finger raised", close=True),
      c("有，可是非常少見。所以我才說，一般的鑽石。"))
kid("kid-direction-q", K("turning her yellow pencil sideways in her fingers with a thinking face", close=True, where=DESK),
    k("那石墨換個方向，", "追問"), k("電也一樣好走嗎？", "句尾上揚", "S:dir"))
model("stack-glow", "Medium shot from the side of " + STACK + ", a soft warm golden glow running along the top net only" + FLATDRAW,
      c("沿著一張網跑很順，"), c("要從這一層跳到下一層，就難多了。"))
chief("chief-hundred", C("holding one flat hand still and sliding the other hand smoothly across it, a pleased smile"),
      c("量出來，沿著層走，比穿過層好走幾百到上千倍。", "數字放慢", "P:dir"))
kid("kid-long-q", K("stretching her two hands far apart with a curious face", where=DESK),
    k("差那麼多！", "驚訝"), k("線畫很長的話，", "追問"), k("燈還會亮嗎？", "句尾上揚", "S:long"))
scene("stroke-long", "Close-up of a very long winding thick dark grey pencil stroke on a plain white drawing sheet, a round battery at one end and a tiny LED glowing faintly at the other end, " + DAY,
      c("博物館說，石墨只是還不錯的導電材料，"), c("線越長，電越難走，燈就越暗。", None, "P:long"))
kid("kid-try", K("raising one hand high with an excited grin", where=DESK),
    k("我要試試看！", "興奮"))
chief("chief-safety", C("holding up one hand like a gentle stop with a serious kind face", close=True),
      c("對了，這個小實驗只能用小電池，"), c("牆上的插座，絕對不要拿來玩。", "認真"))
chief("chief-which-carbon", C("holding a yellow pencil out towards the viewer like a microphone with a playful questioning smile"),
      c("所以下次有人跟你說，碳會導電，", "轉向觀眾"), c("你可以問他：是哪一種排法的碳？"))
kid("kid-enough-q", K("looking down at her pencil in her hands with a thinking face", where=DESK),
    k("所以只知道是碳，", "推理"), k("還不夠囉？", "章尾停住，句尾上揚", "S:enough"))

# ---------- 收尾 ----------
chief("chief-answer", C("sitting on the edge of a desk and leaning forward with an inviting grin, one hand open towards the girl"),
      c("你說呢？小問，你來說說看。", "笑"), chapter="小問說出了答案")
kid("kid-got-it", K("holding up her yellow pencil proudly with a big confident grin", where=DESK),
    k("我懂了！", "恍然大悟", "P:enough"), k("不只看是碳，還要看怎麼排！", "篤定", "P:main"))
chief("chief-opinion", C("smiling with her hands clasped, a thoughtful look", close=True),
      c("說得好，而且是你自己想通的。", "笑"), c("我覺得這就是材料最有意思的地方。"))
kid("kid-redraw-q", K("holding up her smudged drawing with a hopeful face", where=DESK),
    k("那我的畫，以後還會糊嗎？", "句尾上揚"))
chief("chief-drawing-back", C("holding up a smudged child's drawing on a plain white drawing sheet with a kind smile"),
      c("會呀。不過你可以先做一個小觀察。"))
scene("two-patches", "Close-up of two small shaded pencil patches side by side on a plain white drawing sheet, one pale grey and one deep black, two yellow pencils lying below, " + DAY,
      c("下次你畫畫，拿一支比較黑、一支比較淡的鉛筆，", "轉向觀眾"))
kid("kid-two-patches", K("rubbing one fingertip across a small shaded pencil patch on a plain white drawing sheet, a curious face", where=DESK),
    k("各塗一小塊，", "接著說"), k("再用手指擦擦看？", "句尾上揚"))
chief("chief-which-smudge", C("nodding with an encouraging smile, one finger raised", close=True),
      c("對，看看哪一塊比較容易糊。"))
kid("kid-smudge-guess", K("holding up a short dark pencil next to a long pale pencil with a sure, cheeky grin", where=DESK),
    k("我猜黑的那支！", "很有把握"), k("石墨比較多！", "得意"))
chief("chief-more-clay", C("giving a small approving nod with a warm smile, holding a pale pencil", close=True),
      c("猜得有道理：淡的那支，黏土比較多。"))
# The outro is three pictures, no card, no stamp (series README §3.2, §10.1): the kid gives a thumbs-up.
kid("outro", "Waist-up medium shot of the girl with a big happy smile giving a big cheerful thumbs-up with one hand, bright morning light",
    k("原來如此！", "開心大聲"))
chief("outro-chief", "Waist-up medium shot of the chief holding up two yellow pencils with a curious smile, filling the frame, a plain pale wall behind her, bright morning light",
      c("你家的鉛筆，哪一支最容易糊？", "問句上揚，像聊天"), c("留言告訴我們。"))
chief("outro-wave", "Waist-up medium shot of the chief waving goodbye with a warm smile, a plain pale wall behind her, bright morning light",
      c("想一起找生活裡的為什麼，就訂閱原來如此事務所。", "誠懇"))

# ---------- assemble ----------
WHAT = {"main": "同樣都是碳，鉛筆芯和鑽石怎麼會差這麼多", "smudge": "鉛筆芯為什麼這麼容易掉、一擦就糊",
        "hammer": "最硬的鑽石，怕的是什麼", "lamp": "鉛筆線能做到、鑽石做不到的那件事是什麼",
        "mix": "筆芯是哪兩樣東西混在一起", "dark": "為什麼有的鉛筆特別黑、特別軟",
        "diamond": "鑽石是不是別的東西做的", "build": "排法不一樣，真的會差這麼多嗎",
        "hand": "平平的網裡，每顆碳空著的那隻手做什麼", "far": "層跟層離得遠，會怎麼樣",
        "harder": "模型猜得出誰比較硬嗎", "unbreak": "最硬的鑽石是不是一定打不破",
        "more": "模型除了硬不硬、碎不碎，還能猜別的嗎",
        "metal": "鉛筆不是金屬，電怎麼走得過去", "dlamp": "鑽石接上電池，小燈也會亮嗎",
        "dir": "石墨換個方向，電也一樣好走嗎", "long": "鉛筆線畫很長，小燈還會亮嗎", "squeeze": "鑽石的碳是不是被擠得比較緊",
        "enough": "只知道是碳，是不是還不夠", }
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
    "series": {"slug": "sothatswhy", "episode": 18, "chapter": 1},
    # The series bed from P15 on (explainer-series/README.md, PR #2048): sothatswhy-bed-r2.m4a, remade from P02's paid take.
    "music": {"track": "sothatswhy-bed-r2.m4a", "sha256": "9bb4ba6fd16feb4a7f352144b2d89e9648acbbbbaa2173c27a7eefbdb70f28c6", "gain_db": -20, "duck_db": -10},
    "characters": CHARACTERS, "loops": loops,
    "youtube": {
        "category_id": 27, "made_for_kids": False, "default_language": "zh-TW",
        "title": "都含碳，鉛筆芯和鑽石怎麼差這麼多？｜原來如此事務所",
        "description": "小問畫了一整張圖，手一擦就糊了，手掌也黑黑的。所長說，她手上那層黑黑的，跟亮晶晶的鑽石都是碳組成的。同樣都是碳，怎麼一個一擦就掉，一個最難刮傷？\n\n"
                       "這一集，所長和小問跟著同一支鉛筆走：先看鉛筆芯其實是石墨和黏土混在一起，再用一盒積木把碳的兩種排法搭出來——石墨是一層一層疊起來的平網，鑽石是到處都接在一起的攀爬架。"
                       "接著讓這個模型去猜：哪一個會滑、哪一個比較硬、最硬是不是就打不破，最後用一條鉛筆線讓小燈亮起來，看排法怎麼連導電都改掉。\n\n"
                       "本集插圖由 AI 生成，積木是示意的模型，真的碳不是木球。數字是大約的數字。鉛筆線導電的小實驗只用小電池，千萬不要接家裡的插座。每個說法的出處列在下方參考資料。\n\n資料截至 " + CHECKED,
        "tags": ["鉛筆", "鑽石", "石墨", "碳", "硬度", "導電", "科普", "原來如此事務所"]},
    "thumbnail": {"template": "thumb", "data": {"headline": "都含碳\n**差在哪？**", "sub": "鉛筆芯和鑽石", "shot": "kid-grey-hand", "subject": "right"}},
    "sources": [
        {"title": "USGS Professional Paper 1802-J (2017), Graphite (Robinson et al.), Critical Mineral Resources of the United States", "url": "https://pubs.usgs.gov/pp/1802/j/pp1802j.pdf", "checked_on": CHECKED},
        {"title": "USGS General Interest Publication, Gemstones: Mineral gemstones (Mohs hardness scale)", "url": "https://pubs.usgs.gov/gip/gemstones/mineral.html", "checked_on": CHECKED},
        {"title": "Chemistry LibreTexts, 13.7 Network Covalent Atomic Solids: Carbon and Silicates (Tro, Structure and Properties)", "url": "https://chem.libretexts.org/Bookshelves/General_Chemistry/Map%3A_Structure_and_Properties_(Tro)/13%3A_Phase_Diagrams_and_Crystalline_Solids/13.07%3A_Network_Covalent_Atomic_Solids-_Carbon_and_Silicates", "checked_on": CHECKED},
        {"title": "Chemistry LibreTexts, Covalent Network Solids (Inorganic Chemistry supplemental module)", "url": "https://chem.libretexts.org/Bookshelves/Inorganic_Chemistry/Supplemental_Modules_and_Websites_(Inorganic_Chemistry)/Crystal_Lattices/Lattice_Basics/Covalent_Network_Solids", "checked_on": CHECKED},
        {"title": "GIA, Diamond Care and Cleaning Guide (hardness, toughness, cleavage)", "url": "https://www.gia.edu/diamond-care-cleaning?lang=en", "checked_on": CHECKED},
        {"title": "GIA 4Cs blog, More than the Mohs Scale: Gem Durability", "url": "https://4cs.gia.edu/en-us/blog/more-than-mohs-scale-gem-durability/", "checked_on": CHECKED},
        {"title": "GIA 4Cs blog, Digging into Diamond Types (type IIb conducts electricity)", "url": "https://4cs.gia.edu/en-us/blog/digging-diamond-types/", "checked_on": CHECKED},
        {"title": "Science Museum Group Learning, Graphite circuits", "url": "https://www.sciencemuseumgroup.org.uk/learning/resources/graphite-circuits", "checked_on": CHECKED},
        {"title": "Windows to the Universe (NESTA), Mohs Hardness Scale (fingernail 2.5, glass 5.5)", "url": "https://windows2universe.org/earth/geology/mohs.html", "checked_on": CHECKED},
        {"title": "STAEDTLER, Pencils and accessories (graphite, clay and lead hardness)", "url": "https://www.staedtler.com/ca/en/products/pencils-and-accessories/", "checked_on": CHECKED},
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
assert len(loops) >= 11, "13 minutes need at least 11 loops"
assert 2250 <= body_chars <= 2600, f"body {body_chars} characters: write 2,250–2,600 (README §9, 3.2 chars/s; P18 blind-review rounds cut recaps and detours; EPISODES.md gives P18 11–13 min, P17 measured 2,543 chars = 12:56)"
cams = [s["data"]["camera"] for s in scenes]
assert all(not (a == b == c_) for a, b, c_ in zip(cams, cams[1:], cams[2:])), "three shots in a row with the same camera"
