"""Generate video.json for sothatswhy-p17-gecko-feet (原來如此事務所 對話版 P17).

Run `python3 build_scenes.py` from anywhere: it rewrites video.json next to this file and freezes
every shot's camera move in cameras.json (a shot keeps the camera it was first given, so deleting
a shot never shifts the others: the camera is in the keyframe cache key).
Edit lines and prompts here, never in video.json.
Started from a copy of sothatswhy-p08-popcorn-pressure/build_scenes.py (series constants, helpers,
assembly and self-checks unchanged); the content is new.
"""
import itertools, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = "sothatswhy-p17-gecko-feet"
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
# A Taiwanese home in the morning: the gecko is resting, the room is full of sunlight (README §3.1: daylight, never lamps).
HOME = "in a bright sunny Taiwanese apartment living room with a plain white ceiling"
KITCHEN = "in a bright sunny home kitchen"
GECKO = "a cute small pale tan cartoon gecko with big round dark eyes, a long tail and wide rounded toe tips"
TOKAY = "a big chubby blue-grey cartoon gecko with orange spots, big round golden eyes and wide rounded toe tips"
# One drawing language for the whole episode (README §10.5: numbers as feelings, one metaphor throughout):
# the gecko's foot is "a sticker with no glue" (a plain round yellow sticker); the tiny pulls are soft little
# golden sparks where the tips touch; the toe hair is a soft brush of pale bristles drawn large, never a
# microscope image. Nothing is counted, nothing depends on an arrow or a direction.
STICKER = "a plain round smooth mustard-yellow sticker"
BRISTLES = "a soft dense brush of very fine pale cream bristles, drawn large as a simple flat 2D cartoon diagram"
TIPS = "each bristle tip fanning out into a little bunch of tiny flat spoon-shaped tips"
SPARK = "tiny soft golden sparkles glowing where the tips touch the surface"
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
KIDFIX_TAIL = ', exactly matching her reference sheet: the same little girl every time, short black bob with straight bangs, navy raincoat with mustard-yellow hood, long navy trousers, bare loose bob hair hanging free, simple dot-like cartoon eyes as on the reference sheet, a round young child face with big round matching eyes looking the same way, flat 2D cel-shaded cartoon drawing with ink outlines'
CHIEFFIX_TAIL = ', exactly matching her reference sheet: slim young woman, glossy jet-black hair with only one thin silver strand, mustard-yellow cardigan over a white blouse, flat 2D cel-shaded cartoon drawing with ink outlines'
# Lines added after a visual review (P08: photo-real, off-model, marks). Empty until this episode's keyframes are drawn.
FLAT = ", simple hand-drawn flat 2D children's cartoon illustration with clean ink outlines and flat colours"
HOOD = ", hood down, short black bob hanging free"
EXTRA = {'kid-ceiling': ', hood folded down, bare black bob uncovered, flat cartoon background',
    'kid-gland-q': ', hood folded down, bare black bob uncovered',
    'kid-dust-q': ', hood folded down, bare black bob uncovered',
    'kid-slip': ', loose chin-length bob, smooth round back of head, hood folded down, bare black bob uncovered',
    'kid-real-q': ', hood folded down, bare black bob uncovered, standing upright, navy sleeves, eyes looking the same way',
    'kid-oily-q': ', loose chin-length bob, smooth round back of head, both eyes the same size looking the same way',
    'kid-how-many-q': ', plain navy raincoat, pinching one strand of her own hair, loose chin-length bob, smooth round back of head',
    'kid-pull-guess': ', loose chin-length bob, hood folded down, empty hands',
    'kid-suction-guess': ', loose chin-length bob, smooth round back of head, hood folded down, bare black bob uncovered',
    'kid-dusty-sticker': ', plain navy raincoat, loose chin-length bob, smooth round back of head, holding one crumpled plain yellow sticker',
    'kid-hairy': ', hood folded down, bare black bob uncovered, smooth raincoat hood',
    'kid-opposite': ', flat cartoon kitchen with ink outlines and flat colour fills in sharp focus, one palm facing the camera and the other palm facing herself',
    'chief-sticker': ', glossy jet-black hair, round black glasses frames, the pencil only behind her ear',
    'chief-pull': ', both eyes identical dark brown looking the same way, clear lenses, one pebble pinched in each hand',
    'chief-slip-bridge': ', a plain clean background, flat 2D cel-shaded cartoon with ink outlines, holding the pan by its handle',
    'climb-fast': ', top-down view, exactly four legs clearly visible, two front and two back placed symmetrically, body pointing straight up the wall',
    'home-gecko': ', whole gecko in a clear top-down view, slim body between head and tail, exactly four legs spread flat, head in proportion'}
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
def critter(id, prompt, *lines, chapter=None):
    """The gecko itself, no person: like scene(), but without `nobody` (the gecko has a face and eyes)."""
    _shot(id, prompt, [], lines, chapter)
def k(t, e=None, tag=None): return ("kid", t, e, tag)
def c(t, e=None, tag=None): return ("chief", t, e, tag)

def C(action, close=False):
    return ("Head-and-shoulders close-up" if close else "Waist-up medium shot") + " of the chief " + action + ", " + WALL + ", " + DAY
def K(action, close=False, where=None):
    return ("Head-and-shoulders close-up" if close else "Waist-up medium shot") + " of the girl " + (where + " " if where else "") + action + ", " + DAY

# ---------- 開場（系列片頭之後直接進場景，不做濃縮；答案都不先講）----------
# Thumbnail shot (fixed before keyframes, explainer-series/README.md): the kid big, a clear face, the gecko in frame.
kid("kid-ceiling", K("pointing up at a cute small pale tan cartoon gecko on the ceiling just above her head, an excited open-mouthed face", where="in a bright sunny living room with a plain white ceiling"),
    k("所長！今天早上，我家客廳天花板上，", "興奮，跑進來報案的語氣"), k("有一隻壁虎！", "興奮"), chapter="天花板上一動也不動的壁虎")
critter("gecko-ceiling", "Medium shot looking up at " + GECKO + " resting upside down on a plain white ceiling near the corner of a sunny living room, all four feet spread flat, morning sunlight on the ceiling",
        k("牠倒掛在上面，", "壓低聲音"), k("一動也不動！", "驚奇"))
chief("chief-look", C("leaning forward with a curious smile, one hand on her chin", close=True),
      c("一動也不動？那牠多半是在休息。", "接住上一句"), c("你看到牠的四隻腳，是不是平平貼著天花板？", "問句"))
kid("kid-stuck-q", K("tilting her head and squinting up at the ceiling with a puzzled frown", close=True, where=HOME),
    k("有！貼得平平的！", "用力點頭"), k("牠的腳是黏住的嗎？", "好奇"), k("那要走的時候，腳怎麼拔起來？", "句尾上揚"))
critter("gecko-lift", "Close-up looking up at " + GECKO + " walking upside down across a plain white sunny ceiling, one front foot lifted a little off the ceiling, the other three feet flat",
        c("這就是今天的案子：腳能黏住天花板，", "放慢"), c("要跨下一步的時候，怎麼又抬得起來？", "問句", "S:main"))
kid("kid-glue-guess", K("raising one finger with a confident know-it-all grin", close=True),
    k("我知道！", "很有把握"), k("牠的腳底有膠水！", "很有把握的錯猜", "S:glue"))
critter("dusty-sill", "Close-up of " + GECKO + " walking along a dusty sunny windowsill with soft little specks of grey dust and a few crumbs around its feet, " + DAY,
        c("那你想想看，牠整天在灰塵裡爬來爬去，"), c("腳底要是有膠，不早就沾成一團了？", "賣關子", "S:dirty"))
kid("kid-slip-q", K("hugging her knees and looking up thoughtfully", close=True, where=HOME),
    k("對耶……", "想了一下"), k("那牠是不是什麼地方都黏得住？", "好奇", "S:slip"))
chief("chief-promise", C("smiling warmly with one hand open towards the viewer", close=True),
      c("也不是。有一種地方牠黏不太住，就在你家。", "賣關子"), c("還有，牠每次抬腳，都會先做一個小動作。", "賣關子", "S:move"))

# ---------- 第一章：先排除一灘膠水 ----------
chief("chief-glue-check", C("holding up a small tube of glue with a playful doubtful look"),
      c("你剛剛猜的膠水，其實很多人都猜過。", "接住上一句"), c("那就來查查你的膠水猜想。"), chapter="腳底找不到膠水")
scene("glue-tube", "Close-up of a small squeezed tube of glue with a thick shiny drop of glue oozing out of its tip onto a pale wooden table, " + DAY,
      c("如果靠膠水，腳底就得有地方，一直冒出膠來。"))
scene("toe-pad-dry", "Close-up of the underside of one small cartoon gecko foot pressed on clear glass, wide rounded toe tips with neat rows of smooth pale flaps, clean and dry, plain pale cream background, " + DAY,
      c("可是研究的人仔細看過，"), c("壁虎的腳底，沒有會分泌東西的腺體。"))
kid("kid-gland-q", K("tilting her head with one finger on her chin", close=True),
    k("腺體是什麼？", "句尾上揚"))
chief("chief-gland", C("touching the side of her own cheek with one finger and smiling", close=True),
      c("就是身上專門做汗、做口水的小工廠。"))
scene("toe-drop", "Close-up of one round clear water drop sitting high and round like a tiny glass bead on the smooth pale flaps of a cartoon gecko toe, " + DAY,
      c("而且牠的腳趾很怕水，"), c("水滴在上面，會縮成圓圓的一顆。"))
kid("kid-dry-q", K("touching the back of her own hand with a surprised face", close=True),
    k("所以牠的腳是乾的？", "句尾上揚"))
chief("chief-water-guess", C("holding up a small glass pane with a thin wet tissue stuck flat to it, a curious smile", close=True),
      c("對，乾乾的。可是有人猜，空氣裡的水氣，"), c("會在腳和牆中間留下薄薄一層，像濕紙貼在玻璃上。"))
scene("two-tiles", "Medium shot of two plain smooth square tiles side by side on a table, the left tile with a flat thin spread-out puddle of water, the right tile with round beaded water drops, " + DAY,
      c("研究的人就準備了兩種表面，"), c("一種很愛沾水，一種很怕水。"))
critter("tokay-tiles", "Medium shot of " + GECKO + " clinging calmly to a smooth plain tilted tile, feet spread flat, sunny bright room",
      c("讓壁虎的腳趾去黏，兩種黏得一樣好。"))
kid("kid-mean-q", K("scrunching her face in thought with both hands on her cheeks", close=True),
    k("這代表什麼？", "句尾上揚"))
chief("chief-mean", C("holding up both palms side by side like a fair comparison"),
      c("如果靠一層水，容易沾水的那種，應該黏得好很多。"), c("結果沒有，代表主要不是靠一層水。"))
chief("chief-humid", C("holding her palm out flat in soft morning sunlight with a thoughtful smile", close=True),
      c("不過也有研究發現，空氣裡的濕氣，"), c("還是會幫上一點忙。"))
kid("kid-suction-guess", K("pressing a round plastic suction-cup hook onto a bathroom tile with a hopeful grin", close=True),
    k("那是不是吸盤？", "再猜"), k("像浴室的掛鉤那樣？", "句尾上揚", "S:suction"))
scene("suction-hook", "Close-up of a round clear plastic suction-cup hook stuck on a smooth white bathroom tile, beside a small cartoon gecko foot with wide rounded toe tips on the same tile, " + DAY,
      c("也不是。研究的人說，壁虎黏東西，沒有用吸盤，", None, "P:suction"), c("也沒有用膠。", None, "P:glue"))
chief("chief-honest", C("holding one hand on her chest with an honest serious smile", close=True),
      c("不過有一件小事要老實說："), c("有研究在牠走過的腳印裡，找到非常薄的一層油油的東西。"))
kid("kid-oily-q", K("raising her eyebrows with a gotcha grin", close=True),
    k("那不就是膠水嗎？", "抓到了"))
scene("faint-print", "Close-up of a clean clear glass pane in sunlight with the faintest soft shimmering little gecko footprint on it, barely visible, " + DAY,
      c("不是。那層油薄到眼睛看不到，"), c("量那麼少，跟一灘膠水完全不一樣。"))
chief("chief-still-checking", C("shaking her head gently with a kind honest smile", close=True),
      c("至於那層油有沒有幫上忙，研究的人還在查。"))
chief("chief-sticker", C("holding up " + STICKER + " between two fingers with a playful smile"),
      c("既然膠水和吸盤都不是，"), c("你可以把壁虎的腳，想成一張不用膠的貼紙。"))
kid("kid-sticker-q", K("holding " + STICKER + " up to one eye and squinting at it", close=True),
    k("不用膠的貼紙？", "不解"), k("那這張貼紙靠什麼黏？", "章尾停住，句尾上揚", "S:what"))

# ---------- 第二章：把腳畫大，接觸怎麼變多 ----------
chief("chief-draw-big", C("holding a big round magnifying glass up beside her face with a curious smile", close=True),
      c("要回答這個，得看研究的人最常看的另一種大壁虎，", "接住上一句"), chapter="五十萬根小毛一起拉")
chief("chief-tokay", C("holding a small soft plush toy of a chubby blue-grey gecko with orange spots, smiling", close=True),
      c("叫大守宮，英文叫 Tokay gecko。"))
critter("tokay-intro", "Medium shot of " + TOKAY + " sitting calmly on a sunny tree trunk, " + DAY,
        c("牠的身體，大約是你家天花板上那隻的兩三倍長。"))
kid("kid-mine-q", K("pointing back over her shoulder towards her home with a curious face", close=True),
    k("那我家天花板上那隻，", "好奇"), k("腳也跟大守宮一樣嗎？", "句尾上揚", "S:species"))
chief("chief-later", C("holding up one finger with a patient smile", close=True),
      c("先記住這個問題，最後我們回來看。"), c("現在，我們把大守宮的腳畫大來看。"))
scene("toe-flaps", "Close-up of a single wide flat rounded cartoon gecko toe pad seen from directly underneath, shaped like a flat spoon, its underside crossed by six to eight parallel curved ridges like a neat stack of folded blankets, plain pale cream background, simple flat 2D diagram with ink outlines",
      c("牠的腳趾底下，有一排一排的皮，"), c("像疊起來的小毯子。"))
scene("flap-bristles", "Close-up of " + BRISTLES + " growing from one soft pale flap of a gecko toe, plain pale cream background",
      c("每一排上面，長滿很細很細的毛，"), c("一根大約只有你頭髮的十分之一粗。"))
kid("kid-how-many-q", K("holding up one strand of her own hair between two fingers with wide eyes", close=True),
    k("比頭髮還細！", "驚奇"), k("那有幾根？", "句尾上揚"))
scene("bristle-field", "Wide view of a huge soft field of very fine pale cream bristles like a thick meadow of tiny grass, drawn large on a gecko toe pad, soft sunlight, flat 2D cartoon drawing",
      c("一隻腳上，大約有五十萬根。", "數字放慢"))
kid("kid-hairy", K("pinching a lock of her own black bob hair between two fingers with a doubtful frown", close=True),
    k("可是毛毛又不黏，", "不服氣"), k("我的頭髮就不黏啊。"))
scene("bristle-tips", "Close-up of a few very fine pale cream bristles drawn large, " + TIPS + ", plain pale cream background, flat 2D cartoon drawing",
      c("壁虎的毛不一樣。每一根的尖端，又分成好幾百個更小的尖，"))
scene("spoon-tips", "Close-up of one tiny flat spoon-shaped bristle tip drawn very large, smooth and thin like a little pale spoon, beside a small silver teaspoon of the same shape, plain pale cream background, flat 2D cartoon drawing",
      c("最前面是一片小小的扁片，像一支小湯匙。"))
kid("kid-why-small-q", K("pinching her finger and thumb almost together with a puzzled face", close=True),
    k("為什麼要分那麼細？", "句尾上揚", "S:small"))
scene("wall-hills", "Close-up of the edge of a smooth white wall drawn hugely enlarged as a gentle landscape of small rolling hills and little valleys, soft pale colours, flat 2D cartoon drawing",
      c("因為牆其實沒有你想的那麼平。"), c("把牆畫大，牆面高高低低，像一片小山丘。"))
scene("finger-hills", "Close-up of one big round cartoon fingertip resting on a landscape of small rolling hills drawn large, touching only the tops of a few hills, soft pale colours, flat 2D cartoon drawing",
      c("你的手指太粗，只碰得到幾個山頂，"), c("大部分地方，都差了一點點。"))
scene("tips-valleys", "Close-up of " + BRISTLES + " pressing gently onto a landscape of small rolling hills, the tiny flat spoon-shaped tips bending down into many little valleys and lying flat on the slopes",
      c("可是那麼多小扁片，就能鑽進許多小山谷，"), c("大部分地方，都貼得上。", None, "P:small"))
chief("chief-split", C("holding up one big cookie in one hand and a small pile of cookie crumbs in the other palm, a playful smile"),
      c("分得越細，同一塊地方能貼上的點就越多。"))
kid("kid-then-q", K("leaning in eagerly with both fists under her chin", close=True),
    k("貼得上，", "追問"), k("就黏住了嗎？", "句尾上揚"))
chief("chief-pull", C("holding two small smooth pebbles almost touching in her fingers, a curious smile", close=True),
      c("其實任何兩樣東西，只要靠得非常非常近，"), c("都會互相輕輕拉一下。"))
kid("kid-desk-q", K("pressing one flat hand on a wooden table and lifting it easily with a puzzled face", close=True, where=KITCHEN),
    k("那我的手，", "懷疑"), k("怎麼沒黏在桌上？", "句尾上揚"))
scene("weak-pull", "Close-up of one big cartoon fingertip barely touching a smooth wooden table top, just one or two tiny faint golden sparkles where they meet, " + DAY,
      c("因為這一下很弱，又要近到看不見才有。"), c("你的手只碰到幾個點，根本感覺不到。"))
chief("chief-name", C("raising one finger with a gentle smile like sharing a secret", close=True),
      c("這種很近才有的小拉力，科學家叫做凡得瓦力。"), c("所以研究的人算過，尖端分細，就能黏得更牢。"))
kid("kid-real-q", K("holding up a tiny plastic brush with fine bristles and a doubtful squint", close=True),
    k("一定要用壁虎的毛嗎？", "懷疑"))
scene("fake-tips", "Close-up of a small tidy patch of tiny man-made round-tipped bristles in two different colours, one patch grey and one patch white, side by side on a smooth glass slide, " + DAY,
      c("不用。他們用兩種不同的材料，做出假的小尖，"), c("兩種都照樣黏得住。代表重點是形狀和大小。"))
scene("tips-sparks", "Close-up of " + BRISTLES + " lying flat against a smooth surface, " + TIPS + ", " + SPARK,
      c("一個小扁片拉一下，弱到不行，"), c("可是壁虎的腳上，有好多好多個小扁片一起拉。"))
kid("kid-how-many-tips-q", K("spreading all ten fingers wide with a curious face", close=True),
    k("好多是多少個？", "句尾上揚"))
critter("tokay-wall", "Medium shot of " + TOKAY + " clinging to a smooth sunny wall, all four feet spread flat, " + DAY,
        c("一隻大守宮，四隻腳的腳趾全部加起來，"), c("大約有十億個小扁片。", "數字放慢"))
kid("kid-billion", K("throwing both arms wide open with a huge amazed face", close=True),
    k("全部一起拉！", "大驚"), k("那有多大力？", "句尾上揚", "S:strong"))
scene("strong-feel", "Close-up of one very fine pale cream bristle drawn large, its tiny flat spoon-shaped tips stuck to smooth glass, one small round bead hanging gently from it on a fine thread, plain pale cream background, flat 2D cartoon drawing",
      c("研究的人先量出一根小毛的力氣，再估算，"))
scene("rice-sacks", "Medium shot of a tidy bundle of plain round burlap rice sacks tied together with one rope that runs straight up to a single small pale cartoon gecko foot pressed flat on a vertical clear glass pane at the top of the frame, the sacks dangling in mid-air above an empty floor, plain smooth sacks, " + DAY,
      c("如果小毛全部同時用上，理論上能吊起大約一百三十公斤，"), c("差不多兩個大人那麼重。"))
chief("chief-fraction", C("pinching her finger and thumb a little apart with a knowing smile", close=True),
      c("當然，牠平常只用到其中一小部分。"))
critter("one-toe", "Close-up of " + TOKAY + " hanging calmly from a smooth glass pane by just one toe, its body dangling relaxed, " + DAY,
        c("實驗裡，一根腳趾，就撐得住整隻大守宮。", None, "P:strong"))
kid("kid-one-toe", K("hanging from one finger hooked on a door frame with a strained funny face", where=HOME),
    k("我一根手指，", "好笑"), k("撐不住我自己！"))
chief("chief-sticker-back", C("holding up " + STICKER + " beside her face, a warm smile", close=True),
      c("對，所以我才說，牠的腳是一張不用膠的貼紙。", None, "P:what"))
kid("kid-letgo-q", K("frowning and pulling hard at her own sleeve stuck to nothing, puzzled", close=True),
    k("這麼黏，", "擔心"), k("牠的腳不就拔不起來了？", "章尾停住，句尾上揚", "S:letgo"))

# ---------- 第三章：黏住以後，怎麼放開 ----------
kid("kid-pull-guess", K("crouching and gripping an imaginary rope with both hands, leaning back hard with a determined grin", where=HOME),
    k("是不是用力一拔？", "很有把握的錯猜", "S:pull"), chapter="腳趾一捲就放手")
chief("chief-angle", C("tilting one flat hand slowly upward with a playful smile", close=True),
      c("牠不用硬拔。", "接住上一句"), c("還記得我說的那個小動作嗎？", "點名回呼"))
critter("toe-curl", "Close-up of " + GECKO + " on a sunny white wall, one foot with its toes curling up and back from the tips like little rolled ribbons, the rest of the foot still flat, " + DAY,
        c("你仔細看牠抬腳，腳趾會從最前面，"), c("往上、往後捲起來。", None, "P:move"))
kid("kid-tape-q", K("peeling the edge of " + STICKER + " off the back of her hand with a curious face", close=True),
    k("像撕下一張貼紙，", "推理"), k("從邊邊開始掀？", "句尾上揚", "S:tape"))
chief("chief-tape", C("nodding slowly with one finger raised", close=True),
      c("看起來很像。不過研究的人發現，"), c("真正讓牠放手的開關，藏在每一根小毛身上。"))
scene("bristle-lean", "Close-up of one very fine pale cream bristle drawn large, leaning over at a low slant against a smooth surface, its tiny flat spoon-shaped tips lying flat, " + SPARK + ", plain pale cream background, flat 2D cartoon drawing",
      c("小毛黏著的時候，是斜斜躺下來的。"))
scene("bristle-up", "Close-up of one very fine pale cream bristle drawn large, standing up tall and steep from a smooth surface, its tiny flat spoon-shaped tips lifted clear and free, plain pale cream background, flat 2D cartoon drawing",
      c("只要小毛跟牆的角度，翻到大約三十度以上，", "數字放慢"), c("就會自己鬆開。", None, "P:tape"))
kid("kid-itself-q", K("opening both hands wide with a surprised face", close=True),
    k("自己鬆開？", "驚訝"), k("不用力氣嗎？", "句尾上揚"))
scene("rows-release", "Close-up of a cartoon gecko toe drawn large curling up from its tip, the soft rows of pale flaps lifting off a smooth wall one after another like a zip opening, " + DAY,
      c("幾乎不用。只要腳趾往上一捲，", None, "P:pull"), c("一排一排的小毛就跟著翻起來，照順序放手。"))
critter("quick-step", "Medium shot of " + GECKO + " scurrying quickly across a sunny white wall, little speed streaks behind its feet, " + DAY,
        c("研究的人量過，壁虎放開一隻腳，"), c("大約只要百分之一秒多一點。", "數字放慢", "P:letgo"))
kid("kid-fast", K("blinking with her mouth open in amazement", close=True),
    k("那麼快！", "驚奇"), k("那牠一秒能走幾步？", "句尾上揚"))
critter("climb-fast", "Medium shot of a slim little pale grey cartoon gecko running straight up a smooth sunny white wall, legs a quick soft blur, " + DAY,
        c("有一種小壁虎在實驗裡往牆上衝，"), c("每隻腳一秒大約能貼上、放開十五次。"))
kid("kid-grip-q", K("pressing one flat palm onto a wall and looking at it curiously", close=True, where=HOME),
    k("那壁虎踩下去的時候，", "追問"), k("怎麼又黏回去？", "句尾上揚", "S:grip"))
scene("foot-press", "Close-up of one cartoon gecko foot with wide rounded toe tips pressing down flat onto a smooth sunny white wall, toes spread open, " + DAY,
      c("反過來就好。腳趾先放平貼上，"), c("再往身體這邊，輕輕拖一下。"))
scene("bristles-lay", "Close-up of " + BRISTLES + " all leaning over together and lying flat against a smooth surface, " + SPARK,
      c("這一拖，小毛就斜斜躺下、貼平，"), c("拖著的力氣越大，黏得越牢。"))
kid("kid-tap-q", K("tapping one fingertip lightly on a table with a curious frown", close=True, where=KITCHEN),
    k("只拍上去，", "試探"), k("不拖呢？", "句尾上揚"))
scene("bristles-stand", "Close-up of " + BRISTLES + " standing upright and loose above a smooth surface, the tiny tips barely touching it, plain pale cream background",
      c("那就黏得很少。小毛不拖一下的時候，是不太黏的，"), c("要拖一下，才像打開開關。", None, "P:grip"))
kid("kid-ceiling-q", K("looking straight up at the ceiling with a worried frown", where=HOME),
    k("可是倒掛的時候，", "擔心"), k("身體一直往下墜，", "擔心"), k("不會把腳撕下來嗎？", "句尾上揚", "S:ceiling"))
critter("ceiling-feet", "Close-up looking up at " + GECKO + " resting upside down on a sunny white ceiling, its front feet and back feet spread wide apart and gripping firmly, " + DAY,
        c("研究的人看到，牠倒掛的時候，"), c("會讓幾隻腳朝相反方向用力，一起往身體這邊拉。"))
chief("chief-maybe", C("holding her two fists close together and pulling gently towards each other, a thoughtful face"),
      c("他們認為，這可能就是讓每一根小毛一直保持拖著，"), c("不被體重撕開的辦法。", None, "P:ceiling"))
chief("chief-dust-back", C("brushing a little dust off her cardigan sleeve with a playful smile", close=True),
      c("還記得一開始，我問你的灰塵嗎？", "點名回呼"))
kid("kid-remember-dust", K("nodding fast with a bright remembering face, one finger raised", close=True),
    k("記得！", "想起來"), k("你說會沾成一團！"))
scene("dust-foot", "Close-up of one cartoon gecko foot with wide rounded toe tips covered in tiny round grey specks of dust, resting on a clean clear glass pane, " + DAY,
      c("研究的人把很細的小粉末，撒在大守宮的腳趾上，"), c("再按在乾淨的玻璃上踩。"))
kid("kid-dust-q", K("wiping her dusty hands on a cloth with a worried face", close=True),
    k("那牠的腳，", "擔心"), k("就不黏了吧？", "句尾上揚"))
scene("clean-steps", "Side-view close-up of a simple rounded gecko toe pad shaped like a smooth pale pebble with soft ridges underneath, pressing down on a clean clear glass pane, a few tiny grey specks of dust left on the glass beside it, a plain object drawing, " + DAY,
      c("一開始是不太黏。可是腳趾才踩了幾下，"), c("就差不多又能撐住自己了。"))
kid("kid-where-dust-q", K("looking down at the floor behind her with a puzzled face", close=True),
    k("灰塵跑去哪了？", "句尾上揚"))
scene("dust-left", "Close-up of a few tiny round grey specks of dust resting on smooth clean glass, a small cartoon gecko toe with wide rounded tip lifting away above them, " + DAY,
      c("留在玻璃上了。研究的人推測，"), c("一粒灰塵被玻璃拉住的力氣，比被小扁片拉住的大。"))
critter("flick-dust", "Medium shot of " + TOKAY + " walking across a clean clear glass pane, its toes curling up as it lifts each foot, a short trail of tiny grey specks of dust behind it, " + DAY,
        c("另一個研究讓壁虎自己在玻璃上走，"), c("比較腳趾能捲、跟不讓牠捲的時候，"))
chief("chief-eighty", C("holding up one hand with fingers spread and a bright smile", close=True),
      c("能捲的，灰塵掉得快一倍，"), c("大約走四步，就回到原本抓力的八成左右。", None, "P:dirty"))
kid("kid-dusty-sticker", K("holding up a dusty crumpled yellow sticker with a sad pout", close=True),
    k("一般貼紙沾了灰就不太黏，", "比較"), k("牠比貼紙還厲害？", "句尾上揚"))
chief("chief-beat", C("giving a small proud nod with a warm smile", close=True),
      c("對，這是牠贏過貼紙的地方。"))

# ---------- 第四章：換一種表面，還黏得住嗎 ----------
chief("chief-slip-bridge", C("holding up a small plain dark grey frying pan beside her with a mysterious playful smile"),
      c("灰塵難不倒牠，可是有一種地方，", "賣關子"), c("連牠都會滑。"), chapter="連壁虎都滑的鍋子")
kid("kid-where-q", K("standing with her hands on her hips and a curious face", where=HOME),
    k("就是那個黏不太住的地方？", "點名回呼"), k("到底在哪裡？", "句尾上揚"))
scene("pan", "Close-up of a plain round dark grey nonstick frying pan with a smooth shiny coating, sitting on a stove in a bright sunny kitchen, " + DAY,
      c("就在廚房。不沾鍋上那層很滑的塗層，", "接住上一句"), c("常是一種叫鐵氟龍的材料。"))
critter("teflon-slip", "Close-up of " + GECKO + " sliding backwards across a flat smooth shiny dark grey slab with a surprised face, its toes splayed, " + DAY,
        c("研究的人讓壁虎抓住平平的乾鐵氟龍，"), c("再把牠輕輕往後拉，連壁虎都會滑。", None, "P:slip"))
kid("kid-slip", K("pretending to slip with her arms flailing and a funny surprised face", close=True),
    k("連壁虎都滑！", "大驚"))
scene("teflon-tips", "Close-up of " + BRISTLES + " lying on a very smooth shiny dark grey surface, only a few faint tiny sparkles where the tips touch",
      c("這種表面很特別，小扁片在上面，"), c("很難拉出凡得瓦力那種小拉力。"))
kid("kid-wet-guess", K("holding a dripping wet sponge with a confident grin", close=True, where=KITCHEN),
    k("那再沾水，", "推理"), k("一定滑得更厲害！", "很有把握的錯猜", "S:wet"))
critter("teflon-wet", "Close-up of " + GECKO + " clinging calmly to a smooth shiny dark grey slab under clear shallow water, little bubbles around it, " + DAY,
        c("怪就怪在這裡。把鐵氟龍泡在水裡，"), c("牠反而抓得好上好幾倍。", None, "P:wet"))
kid("kid-why-q", K("scratching her head with a very puzzled face", close=True),
    k("為什麼？", "句尾上揚"))
chief("chief-unknown", C("shrugging gently with open palms and an honest smile"),
      c("研究的人說，跟水和表面怎麼互相拉有關，"), c("算得出大方向，但還沒有完全弄懂。"))
critter("glass-wet", "Close-up of " + GECKO + " on a clear glass pane covered in shallow water, its toes splayed and slipping a little, " + DAY,
        c("換成普通玻璃，結果就倒過來。"), c("玻璃一泡水，抓力少了一大半。"))
kid("kid-opposite", K("holding her two hands up flipped opposite ways with a surprised grin", close=True, where=KITCHEN),
    k("跟鐵氟龍剛好相反！", "驚訝"))
kid("kid-rain-q", K("holding an open umbrella under falling rain on a covered balcony, curious face", close=True),
    k("所以下雨天，", "推理"), k("牠會比較難爬？", "句尾上揚"))
chief("chief-rain", C("nodding gently with a thoughtful smile"),
      c("很可能。研究的人提醒，"), c("對住在又熱又濕地方的壁虎，水恐怕是個大麻煩。"))
kid("kid-rough-q", K("rubbing her palm on a rough stone wall with a curious face", close=True),
    k("那不下雨，", "追問"), k("牆上有很細很細的小顆粒呢？", "追問"), k("應該更好抓吧？", "句尾上揚", "S:rough"))
chief("chief-hills", C("holding a big round magnifying glass up to a rough stone wall with a curious smile", close=True),
      c("不一定。還記得牆畫大，像一片小山丘嗎？", "點名回呼"), c("研究發現，有一種很細很細的小山丘，"))
scene("fine-rough", "Close-up of " + BRISTLES + " resting on a surface of very fine tightly packed little bumps drawn large, only a few faint sparkles where the tips touch",
      c("黏起來反而最差，比更平的、更粗的都差。", None, "P:rough"), c("至於為什麼，研究的人還沒有完全弄懂。"))
chief("chief-species", C("holding a small tan plush toy gecko in one hand and a big blue-grey plush toy gecko with orange spots in the other, smiling", close=True),
      c("還記得你問，你家天花板上那隻是不是也這樣？", "點名回呼"), c("家裡常見的，多半是另外幾種比較小的壁虎。"))
critter("home-gecko", "Close-up of " + GECKO + " resting on a sunny white ceiling near a window, its wide rounded toe tips spread flat, " + DAY,
        c("牠們的腳趾底下，也有一排一排的皮。"), c("可是剛剛那些實驗，大多是在大守宮身上做的。"))
kid("kid-same-q", K("tilting her head with a thinking face", close=True),
    k("所以換一種，", "推理"), k("就不一定一樣？", "句尾上揚"))
chief("chief-padless", C("holding up one finger with a calm smile", close=True),
      c("對，數字不一定一樣。"), c("而且，不是每一種壁虎都有那一排排的皮。", None, "P:species"))
critter("padless", "Close-up of a slim sandy-brown cartoon gecko with thin slender toes and small claws standing on warm sunny desert sand beside a small upright glass pane, " + DAY,
        c("有一種沒有這排皮的壁虎，連光滑的玻璃都爬不上去。"))

# ---------- 收尾 ----------
chief("chief-answer", C("sitting on the edge of a desk and leaning towards the girl with an inviting grin, one hand gesturing to her"),
      c("不管哪一種，有那排皮的壁虎，", "接住上一句"), c("用的都是同一招。小問，你能把案子說破嗎？", "笑"), chapter="說放就放的腳")
kid("kid-got-it", K("holding one hand up flat and curling her fingertips back like a peeling sticker, a proud grin", close=True, where=KITCHEN),
    k("我懂了！", "恍然大悟"), k("牠厲害的不是黏，", "篤定"), k("是腳趾一捲，說放就放！", "開心", "P:main"))
chief("chief-opinion", C("smiling with her hands clasped, a thoughtful look", close=True),
      c("說得好，這也是我最佩服的地方。", "笑"))
critter("little-gecko-back", "Medium shot of a slim little pale grey cartoon gecko trotting up a smooth sunny white wall, one foot lifted with its toes curled up, " + DAY,
        c("還記得那隻一秒貼放十五次的小壁虎嗎？", "點名回呼"), c("牠每一步都在放手。"))
chief("chief-watch", C("crouching a little and pointing up at a sunny window frame, whispering with a gentle smile"),
      c("下次你在家看到壁虎，", "轉向觀眾，輕聲"), c("看就好，別去抓牠，牠會被嚇到。"))
scene("toe-curl-end", "Close-up of one small cartoon gecko foot on a sunny white wall, its toes just starting to curl up from the tips, " + DAY,
      c("你只要盯著牠抬腳的那一下，"), c("看看腳趾，是不是先往上捲。", "點名回呼"))
# The outro is three pictures, no card, no stamp (series README §3.2, §10.1): the kid gives a thumbs-up.
kid("outro", "Head-and-shoulders close-up of the girl with a big happy smile giving a big cheerful thumbs-up with one hand, bright morning light",
    k("原來如此！", "開心大聲"))
chief("outro-chief", "Waist-up medium shot of the chief pointing up towards a small cartoon gecko on the sunny wall above her, a curious smile, filling the frame, a plain pale wall behind her, bright morning light",
      c("你家的壁虎，最常停在哪裡？", "問句上揚，像聊天"), c("留言告訴我們。"))
chief("outro-wave", "Waist-up medium shot of the chief waving goodbye with a warm smile, a plain pale wall behind her, bright morning light",
      c("想一起找生活裡的為什麼，就訂閱原來如此事務所。", "誠懇"))

# ---------- assemble ----------
WHAT = {"main": "腳能黏住天花板，下一步怎麼又抬得起來", "glue": "壁虎的腳底是不是有膠水",
        "dirty": "整天在灰塵裡爬，腳要是黏的，不早就沾成一團", "slip": "壁虎是不是什麼地方都黏得住（有一種家裡就有的地方牠黏不太住）", "move": "牠每次抬腳前先做的那個小動作是什麼",
        "suction": "是不是像浴室掛鉤一樣用吸盤", "what": "不用膠的貼紙，到底靠什麼黏住",
        "small": "腳趾上的毛為什麼要分那麼細", "species": "家裡天花板上那隻壁虎，也跟大守宮一樣嗎",
        "strong": "十億個小扁片一起拉，到底有多大力", "letgo": "這麼黏，腳不就拔不起來了",
        "pull": "是不是用力一拔就拔起來", "tape": "放開是不是像撕貼紙從邊邊掀",
        "grip": "踩下去的時候，怎麼又黏回去", "ceiling": "倒掛時體重會不會把腳撕下來",
        "wet": "沾了水是不是一定更滑", "rough": "粗粗的牆是不是更好抓", }
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
    "series": {"slug": "sothatswhy", "episode": 17, "chapter": 1},
    # The series bed from P15 on (explainer-series/README.md, PR #2048): sothatswhy-bed-r2.m4a, remade from P02's paid take.
    "music": {"track": "sothatswhy-bed-r2.m4a", "sha256": "9bb4ba6fd16feb4a7f352144b2d89e9648acbbbbaa2173c27a7eefbdb70f28c6", "gain_db": -20, "duck_db": -10},
    "characters": CHARACTERS, "loops": loops,
    "youtube": {
        "category_id": 27, "made_for_kids": False, "default_language": "zh-TW",
        "title": "壁虎黏得住，怎麼又能走得動？｜原來如此事務所",
        "description": "小問在客廳的天花板上看到一隻倒掛的壁虎，一動也不動。牠的腳如果黏得住天花板，要走的時候，又怎麼抬得起來？\n\n"
                       "這一集，所長和小問跟著壁虎的一隻腳走完一圈：先查牠的腳底是不是有膠水或吸盤，再把腳趾畫大，看一排排的皮、比頭髮細得多的小毛和更小的扁片，"
                       "怎麼靠「貼得夠近、貼得夠多」的小拉力黏住；接著看牠怎麼把腳趾一捲、讓小毛翻過角度自己放手，髒了怎麼走幾步就乾淨；最後換到不沾鍋、濕玻璃和粗粗的牆，看這套辦法在哪裡不靈。\n\n"
                       "本集插圖由 AI 生成，畫的是示意，不是顯微照片，也不是量測。片中的數字大多來自以大守宮（Tokay gecko）做的研究，是大約的數字，換一種壁虎不一定一樣。"
                       "看到壁虎請不要去抓牠。每個說法的出處列在下方參考資料。\n\n資料截至 " + CHECKED,
        "tags": ["壁虎", "大守宮", "凡得瓦力", "鐵氟龍", "生物力學", "科普", "原來如此事務所"],
        "video_id": None},
    "thumbnail": {"template": "thumb", "data": {"headline": "黏得住\n**怎麼走？**", "sub": "腳底沒有膠", "shot": "kid-ceiling", "subject": "right"}},
    "sources": [
        {"title": "Autumn et al. (2000), Adhesive force of a single gecko foot-hair, Nature 405: 681–685", "url": "https://doi.org/10.1038/35015073", "checked_on": CHECKED},
        {"title": "Autumn et al. (2002), Evidence for van der Waals adhesion in gecko setae, PNAS 99: 12252–12256", "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC129431/", "checked_on": CHECKED},
        {"title": "Autumn & Peattie (2002), Mechanisms of adhesion in geckos, Integr. Comp. Biol. 42: 1081–1090", "url": "https://doi.org/10.1093/icb/42.6.1081", "checked_on": CHECKED},
        {"title": "Hansen & Autumn (2005), Evidence for self-cleaning in gecko setae, PNAS 102: 385–389", "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC544316/", "checked_on": CHECKED},
        {"title": "Huber et al. (2005), Evidence for capillarity contributions to gecko adhesion from single spatula nanomechanical measurements, PNAS 102: 16293–16296", "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC1283435/", "checked_on": CHECKED},
        {"title": "Autumn et al. (2006), Frictional adhesion: a new angle on gecko attachment, J. Exp. Biol. 209: 3569–3579", "url": "https://doi.org/10.1242/jeb.02486", "checked_on": CHECKED},
        {"title": "Tian et al. (2006), Adhesion and friction in gecko toe attachment and detachment, PNAS 103: 19320–19325", "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC1748224/", "checked_on": CHECKED},
        {"title": "Hsu et al. (2012), Direct evidence of phospholipids in gecko footprints, J. R. Soc. Interface 9: 657–664", "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC3284128/", "checked_on": CHECKED},
        {"title": "Hu et al. (2012), Dynamic self-cleaning in gecko setae via digital hyperextension, J. R. Soc. Interface 9: 2781–2790", "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC3479896/", "checked_on": CHECKED},
        {"title": "Stark et al. (2012), The effect of surface water and wetting on gecko adhesion, J. Exp. Biol. 215: 3080–3086", "url": "https://doi.org/10.1242/jeb.070912", "checked_on": CHECKED},
        {"title": "Stark et al. (2013), Surface wettability plays a significant role in gecko adhesion underwater, PNAS 110: 6340–6345", "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC3631644/", "checked_on": CHECKED},
        {"title": "Stark et al. (2015), Adhesive interactions of geckos with wet and dry fluoropolymer substrates, J. R. Soc. Interface 12: 20150464", "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC4528608/", "checked_on": CHECKED},
        {"title": "Huber et al. (2007), Influence of surface roughness on gecko adhesion, Acta Biomaterialia 3: 607–610", "url": "https://doi.org/10.1016/j.actbio.2007.01.007", "checked_on": CHECKED},
        {"title": "Gillies et al. (2014), Gecko toe and lamellar shear adhesion on macroscopic, engineered rough surfaces, J. Exp. Biol. 217: 283–289", "url": "https://doi.org/10.1242/jeb.092015", "checked_on": CHECKED},
        {"title": "OpenStax Chemistry 2e, 10.1 Intermolecular Forces", "url": "https://openstax.org/books/chemistry-2e/pages/10-1-intermolecular-forces", "checked_on": CHECKED},
        {"title": "Wikipedia: Tokay gecko", "url": "https://en.wikipedia.org/wiki/Tokay_gecko", "checked_on": CHECKED},
        {"title": "Zimin et al. (2025), Microhabitat and adhesive toepads shape gecko limb morphology, Integrative Zoology", "url": "https://doi.org/10.1111/1749-4877.12880", "checked_on": CHECKED},
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
assert 2400 <= body_chars <= 2600, f"body {body_chars} characters: write 2,400–2,600 (README §9, 3.2 chars/s)"
cams = [s["data"]["camera"] for s in scenes]
assert all(not (a == b == c_) for a, b, c_ in zip(cams, cams[1:], cams[2:])), "three shots in a row with the same camera"
