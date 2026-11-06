"""Generate video.json for sothatswhy-p14-sky-colors (原來如此事務所 對話版 P14).

Run `python3 build_scenes.py` from anywhere: it rewrites video.json next to this file and freezes
every shot's camera move in cameras.json (a shot keeps the camera it was first given, so deleting
a shot never shifts the others: the camera is in the keyframe cache key).
Edit lines and prompts here, never in video.json.
"""
import itertools, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = "sothatswhy-p14-sky-colors"
CHECKED = "2026-11-06"

# ---------- series constants ----------
# The chief is identical to P02/P05 (approved sheet reused). The kid drops the notebook from this
# episode on (series README §3.2, owner 2026-11-06): her sheet is redrawn once before any keyframe.
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
ROOF = "on a sunny rooftop with potted plants"
SUNSET = "a big round red-orange sun sitting low over distant rooftops, warm bright sunset glow"
# Prompt words that P02/P05 taught us to keep out (README §3.1): the model has no negative prompt,
# lamps and night turn frames into 3D figurines, and these props sprout fake letters.
BANNED = re.compile(r"\b(no|not|without|text|blank|lamp|night|notebook|sign|signs|paper|poster|screen|book|calendar|whiteboard)\b", re.I)

CAMS = itertools.cycle(["push in", "pan left", "pull out", "drift", "tilt up", "pan right", "push in", "tilt down", "pull out", "drift"])
CAM_FILE = os.path.join(HERE, "cameras.json")
FROZEN = json.load(open(CAM_FILE, encoding="utf-8")) if os.path.exists(CAM_FILE) else {}

S = []
def _shot(id, prompt, chars, lines, chapter):
    assert not BANNED.search(prompt), (id, BANNED.search(prompt).group(0))
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

# ---------- 開場（系列片頭之後直接進場景，不做濃縮；答案都不先講）----------
kid("roof-blue", "Waist-up medium shot of the girl " + ROOF + " looking up at a deep blue sky with her mouth open in wonder, " + DAY,
    k("所長！我中午跑上頂樓，", "興奮，跑進來報案的語氣"), k("天空藍得好漂亮！", "開心"), chapter="中午藍天，傍晚紅太陽")
kid("roof-sunset", "Waist-up medium shot of the girl " + ROOF + " pointing at " + SUNSET + ", her eyes wide",
    k("可是傍晚再上去，", "壓低聲音"), k("太陽變成一顆紅紅的大球！", "誇張"))
chief("chief-same-sun", C("raising one finger with a calm knowing smile"),
      c("同一個太陽，照下來的也是同一道陽光喔。", "賣關子"), c("你每天抬頭都看得到，它到底是被誰換了顏色？", "轉向觀眾"))
kid("kid-swap", "Head-and-shoulders close-up of the girl narrowing her eyes like a detective with one finger raised, a plain pale wall behind her, " + DAY,
    k("一定有人偷偷換了顏色！", "像偵探"))
chief("chief-swap", C("chuckling with one hand over her mouth", close=True),
      c("是有東西在換。它天天貼著你，你卻看不見它。", "賣關子", "S:swap"))
kid("kid-where-blue", "Head-and-shoulders close-up of the girl shading her eyes with one hand and squinting up at a blue sky, " + DAY,
    k("那天空的藍，", "疑惑"), k("是從哪裡來的？", "句尾上揚", "S:where"))
scene("milk-teaser", "Close-up of one tall clear glass of water with a faint milky cloudiness standing on a wooden kitchen table, a small flashlight lying beside it, " + DAY,
      c("先猜一件事：一杯水加幾滴牛奶，拿手電筒照，", "賣關子"), c("從旁邊看，它會是什麼顏色？", "問句，最後放慢", "S:milk"))
kid("kid-milk-guess", "Head-and-shoulders close-up of the girl peering at a tall glass of milky water on a kitchen table with a confident little smile, " + DAY,
    k("牛奶水？", "想一想"), k("應該白白的吧？", "很有把握的錯猜"))
scene("moon-teaser", "Wide view of the grey cratered surface of the Moon in bright sunshine, a small round blue Earth hanging in the sky above the horizon, ",
      c("還有，要是站在月球上，白天抬頭看，", "賣關子"), c("天空會是什麼顏色？", "問句", "S:moon"))
kid("kid-cloud-teaser", "Waist-up medium shot of the girl " + ROOF + " pointing up at one big puffy white cloud in a blue sky, a puzzled frown, " + DAY,
    k("月球上？我猜不出來。", "搖頭"), k("說到天上，還有雲！", "突然想到"), k("天空是藍的，雲怎麼是白的？", "句尾上揚", "S:cloud"))
kid("kid-question", "Head-and-shoulders close-up of the girl tilting her head with a curious frown, a plain pale wall behind her, " + DAY,
    k("同一道陽光，", "認真"), k("怎麼一下藍、一下紅？", "認真發問，句尾上揚", "S:same"))

# ---------- 第一章 ----------
kid("kid-sky-guess", "Waist-up medium shot of the girl " + ROOF + " spreading both arms wide toward the blue sky with a confident grin, " + DAY,
    k("天空本來就是藍色的吧？", "很有把握的錯猜", "S:always"), chapter="晚上的天空，藍色不見了")
chief("chief-night-q", C("tilting her head with a playful questioning look, one palm turned up"),
      c("如果它本來就是藍的，", "反問"), c("太陽下山以後，它怎麼變黑了？", "放慢"))
kid("kid-think", "Head-and-shoulders close-up of the girl with one finger on her chin and her eyes rolled up thinking hard, a plain pale wall behind her, " + DAY,
    k("因為……太陽下班了？", "想了一下，好笑"))
chief("chief-laugh", C("laughing with one thumb up", close=True),
      c("對，太陽一走，藍色就跟著走了。", "笑"), c("所以那片藍，是陽光帶來的。", None, "P:always"))
kid("kid-sunbeam", "Waist-up medium shot of the girl holding her open palm up in a bright beam of sunshine from a window, studying it, " + DAY,
    k("可是陽光是白白的啊，", "不服氣"), k("哪裡有藍色？", "句尾上揚", "S:white"))
chief("chief-mix", C("bringing both hands together as if mixing something"),
      c("白光，其實是很多顏色混在一起。", "放慢", "P:white"), c("它們一起跑進眼睛，大腦就把它們看成白的。"))
kid("kid-hose", "Waist-up medium shot of the girl in a sunny garden spraying a fine mist from a green garden hose, a small rainbow glowing in the spray, " + DAY,
    c("你夏天拿水管澆花，水霧裡有時會冒出一小道彩虹。", "轉向觀眾"), c("那些顏色，本來就藏在陽光裡。"))
kid("kid-prism", "Waist-up medium shot of the girl holding up a clear triangular glass prism in a beam of sunshine, a band of rainbow colours glowing on the pale wall beside her, " + DAY,
    c("拿一塊三角形的玻璃，叫三稜鏡，對著太陽，"), c("牆上就會出現一排顏色。"))
chief("chief-newton", C("holding a small clear triangular glass prism up beside her face and smiling"),
      c("很久以前，英國科學家牛頓，就用三稜鏡把陽光分開過。"))
kid("kid-colors", "Head-and-shoulders close-up of the girl counting on her fingers with a delighted grin, a band of rainbow colours glowing on the wall behind her, " + DAY,
    k("紅、橙、黃、綠、藍、紫！", "一個一個數"), k("全部擠在白光裡？", "驚訝"))
chief("chief-white", C("nodding warmly with her hands open", close=True),
      c("對，一個都沒少。"), k("白光好擠喔！", "好笑"))
kid("kid-differ", "Head-and-shoulders close-up of the girl squinting with a suspicious little pout, a plain pale wall behind her, " + DAY,
    k("那這些顏色，", "追問"), k("有什麼不一樣？", "句尾上揚"))
kid("rope-big", "Waist-up medium shot of the girl in a sunny schoolyard swinging one end of a long jump rope slowly so it makes one big wave, " + DAY,
    c("你甩過跳繩吧？繩子會起一波一波的浪。", "轉向觀眾"), c("光也像這樣，一波一波往前走。"))
kid("rope-small", "Waist-up medium shot of the girl in a sunny schoolyard shaking one end of a jump rope fast so it makes many small quick waves, laughing, " + DAY,
    c("紅光的波比較長，像慢慢甩出的大浪；"), c("藍光、紫光的波比較短，像抖出來的小浪。"))
chief("chief-wavelength", C("holding her two hands apart as if measuring a length, a calm smile"),
      c("一個浪頭到下一個浪頭有多長，就叫做波長。"), c("波長不一樣，眼睛看到的顏色就不一樣。"))
kid("kid-short", "Head-and-shoulders close-up of the girl holding her two hands close together to show something tiny, eyebrows raised, a plain pale wall behind her, " + DAY,
    k("我抖快一點，浪就變短了！", "邊玩邊說"), k("藍色是比較短的浪？", "確認"))
chief("chief-remember", C("tapping her temple with one finger and a playful smile", close=True),
      c("對。先記住這件事，等一下它會回來。", "前向鉤子", "S:short"))
kid("kid-air-q", "Waist-up medium shot of the girl " + ROOF + " looking up and reaching one hand toward the blue sky as if to touch it, a puzzled face, " + DAY,
    k("那天空會藍，", "推理"), k("是因為空氣是藍的嗎？", "章尾停住，句尾上揚", "S:airblue"))

# ---------- 第二章 ----------
kid("kid-jar", "Waist-up medium shot of the girl holding up an empty clear glass jar with both hands and peering into it, " + DAY,
    c("你拿一個空玻璃罐，裡面裝滿空氣，", "轉向觀眾"), c("看得到藍色嗎？"), chapter="一罐空氣看不出藍色")
kid("kid-jar-clear", "Head-and-shoulders close-up of the girl looking through an empty clear glass jar held up to one eye, a funny magnified eye, " + DAY,
    k("看不到，", "老實"), k("透明的。"))
chief("chief-thick", C("raising one open hand high above her head"),
      c("一小罐空氣，看不出顏色。"), c("可是你頭頂上的空氣，有很厚很厚一大片。"))
scene("earth-layer", "Wide view of the curved edge of the Earth seen from very high up, a thin glowing blue band of sky hugging the horizon, a dark sky above it, ",
      c("從高空看最清楚：美國空軍從兩萬公尺高拍過，"), c("地球的邊上，就是一圈薄薄的藍。"))
kid("kid-molecule-q", "Head-and-shoulders close-up of the girl squinting at the empty air in front of her as if searching for something tiny, " + DAY,
    c("這層空氣，是由很多很小的分子組成的。"), k("分子是什麼？", "立刻追問"))
chief("chief-molecule", C("pinching two fingers together to show something very tiny, eyes twinkling", close=True),
      c("你可以想成，空氣裡一顆一顆，"), c("小到眼睛看不見的小球。"))
kid("kid-breathe", "Head-and-shoulders close-up of the girl taking a big deep breath with puffed cheeks and her eyes closed, " + DAY,
    k("我吸進去的，也是小球？", "好奇"))
chief("chief-breathe", C("laughing softly and taking a deep breath herself", close=True),
      c("對，你每吸一口氣，就吸進好多好多顆。"))
scene("molecule-wave", "Close-up of one long gentle golden light wave drawn as a wavy ribbon, beside it one tiny round sky-blue ball as small as a crumb, a pale sky-blue background, " + DAY,
      c("一顆分子，比光的一個波還要小上大約一千倍。", "數字放慢"))
kid("kid-tiny", "Head-and-shoulders close-up of the girl peering hard with one eye squeezed shut, her finger and thumb pinched almost together, " + DAY,
    k("一千倍？", "驚訝"), k("那光不就直接穿過去了？", "句尾上揚"))
scene("bounce", "Close-up of sunbeams drawn as golden arrows hitting tiny round balls in the air and short blue arrows bouncing off in every direction, a bright sky, ",
      c("大部分的光是穿過去了。"), c("可是有一部分撞到這些小球，會被彈開，"))
chief("chief-scatter", C("spreading both hands outward in every direction like a little burst"),
      c("往四面八方飛出去。這叫做散射。"), c("被彈開的光，還會撞上別的小球，再彈一次。"))
kid("kid-marbles", "Waist-up medium shot of the girl crouching on a sunny floor flicking colourful glass marbles that bounce apart, grinning, " + DAY,
    k("像打彈珠一樣！", "開心"), c("有點像，只是它會往每個方向彈。"))
kid("kid-every-color", "Waist-up medium shot of the girl " + ROOF + " holding both hands out with palms up, a curious look, " + DAY,
    k("每種顏色，", "好奇"), k("都會被彈開嗎？", "句尾上揚"))
chief("chief-short-back", C("holding her two hands close together, then pointing at them with a smile"),
      c("都會。可是還記得那些短的小浪嗎？", None, "P:short"), c("它們被彈得特別多。"))
scene("four-blue", "Close-up of several short bright blue arrows bouncing away from one tiny round ball while one single red arrow bounces away on the other side, a pale sky-blue background, " + DAY,
      c("藍光被彈開的，比紅光多好幾倍。", "數字放慢"))
kid("kid-busy", "Head-and-shoulders close-up of the girl laughing and waving both hands around fast, a plain pale wall behind her, " + DAY,
    k("好幾倍？藍光好忙！", "好笑"))
kid("kid-red-q", "Head-and-shoulders close-up of the girl holding up one finger with a questioning look, a plain pale wall behind her, " + DAY,
    k("那紅光呢？", "追問"))
chief("chief-red-straight", C("pointing one hand straight ahead like an arrow, a calm face"),
      c("紅光比較少被彈到旁邊，"), c("大多照著原來的方向，直直往前走。"), k("紅光好專心喔！", "好笑"))
chief("chief-rayleigh", C("smiling and raising one finger as if quoting someone"),
      c("十九世紀，英國科學家瑞利，把這件事算清楚了。"), c("所以這種散射，就叫做瑞利散射。"))
scene("dust-beam", "Close-up of a bright sunbeam slanting through a window into a quiet room, full of tiny glittering dust specks floating in the light, " + DAY,
      c("有趣的是，瑞利他們當時以為，", "說故事"), c("把藍光彈開的，是空氣裡的灰塵和小水滴。", None, "S:olddust"))
chief("chief-einstein", C("raising both eyebrows with a delighted smile and one finger up", close=True),
      c("後來的科學家發現：要是靠灰塵，"), c("天空的藍應該跟著天氣變很多，"), c("實際上卻沒有變那麼多。"))
chief("chief-einstein2", C("nodding with a satisfied smile, both hands open"),
      c("後來，物理學家愛因斯坦在一九一〇年算出來："), c("光靠空氣分子，就夠把天空弄藍了。"))
kid("kid-einstein", "Head-and-shoulders close-up of the girl with her mouth open in a delighted O, both hands on her cheeks, " + DAY,
    k("連愛因斯坦，", "驚訝"), k("都來算天空！"))
kid("kid-spin", "Waist-up medium shot of the girl " + ROOF + " turning round with her arms out wide under a deep blue sky, laughing, " + DAY,
    c("所以你不管往天空哪個方向看，", "轉向觀眾"), c("都有被彈過來的藍光，跑進你的眼睛。", None, "P:where"))
chief("chief-not-blue", C("shaking her head gently with a kind smile", close=True),
      c("空氣不是藍的，", None, "P:airblue"), c("它是一路把藍光彈給你看。"))
kid("kid-thrower", "Head-and-shoulders close-up of the girl laughing with both hands raised as if tossing a ball, a plain pale wall behind her, " + DAY,
    k("原來偷換顏色的，", "開心"), k("就是空氣！", None, "P:swap"))
kid("kid-sea", "Waist-up medium shot of the girl on a sunny beach pointing out at the blue sea with a confident face, " + DAY,
    k("可是我聽說，", "想到"), k("天空是海倒映上去的。", "很有把握的錯猜", "S:sea"))
chief("chief-mountain", C("smiling and raising her eyebrows, one hand pointing up and away"),
      c("很多人都這樣聽過。可是你去山上，"), c("離海很遠很遠，天空一樣是藍的。"))
kid("kid-beach", "Waist-up medium shot of the girl standing on a sunny beach looking down at the shining blue sea with a thoughtful face, " + DAY,
    c("其實常常倒過來：從沙灘看海，", None, "P:sea"), c("海會藍，有一部分是因為它映著藍天。"))
kid("kid-violet", "Head-and-shoulders close-up of the girl holding up one small purple flower and frowning at it, " + DAY,
    k("等一下，紫光的波更短，", "抓到問題"), k("天空怎麼不是紫色的？", "句尾上揚", "S:violet"))
chief("chief-less-violet", C("holding her hand flat and lowering it a little, a thoughtful face"),
      c("問得好。陽光裡的紫光，本來就比較少。"))
chief("chief-absorb", C("closing one hand slowly as if catching something small, a calm face", close=True),
      c("有一些在很高的空中，被那裡的空氣吸收了，"), c("吸收就是被吞進去，到不了地面。"))
kid("kid-absorb", "Head-and-shoulders close-up of the girl with her mouth open in a surprised O and one hand on her tummy, " + DAY,
    k("空氣還會偷吃一點！", "驚訝"))
chief("chief-eyes", C("pointing to one of her own eyes behind her round glasses with a gentle smile", close=True),
      c("還有，我們的眼睛，對紫色比較不敏感。"))
kid("kid-violet-mix", "Waist-up medium shot of the girl " + ROOF + " holding the small purple flower up against the blue sky and comparing the colours, " + DAY,
    c("天空裡也有紫光，只是混在一起，", "放慢", "P:violet"), c("我們看起來，就成了淡淡的藍。"))
kid("kid-eye-pick", "Head-and-shoulders close-up of the girl pointing at her own eye with a surprised grin, a plain pale wall behind her, " + DAY,
    k("我的眼睛，", "驚訝"), k("也會挑顏色？"))
chief("chief-opinion", C("folding her arms and laughing softly"),
      c("我覺得這是最好玩的地方：", "意見，輕鬆"), c("你看到的顏色，眼睛也參了一腳。"), k("我的眼睛是調色盤！", "得意"))
kid("kid-sun-q", "Waist-up medium shot of the girl " + ROOF + " shading her eyes and squinting toward the bright sun, a puzzled face, " + DAY,
    k("很多藍光被彈到天上了，", "推理"), k("那太陽本身，是什麼顏色？", "章尾停住，句尾上揚", "S:suncolor"))

# ---------- 第三章 ----------
kid("kid-crayon", "Waist-up medium shot of the girl sitting at a table colouring a round sun with a big yellow crayon, a happy face, " + DAY,
    k("我畫太陽，", "很有把握"), k("都塗黃色的。"), c("很多人都這樣畫。可是要問太陽本身，得離開地面。", "帶笑"), chapter="傍晚的光，多走了好長一段路")
scene("space-sun", "Wide view of the bright white sun shining in a black sky above the curved blue edge of the Earth, seen from space, ",
      c("從太空站上看，太陽是白的。", None, "P:suncolor"), c("那裡已經在大部分的空氣外面了。"))
chief("chief-yellowish", C("holding up a pinch of two fingers with a small smile", close=True),
      c("我們從地面看偏黃，"), c("是因為一部分藍光，半路被彈走了。"))
kid("kid-bright-q", "Head-and-shoulders close-up of the girl squinting with one hand shading her eyes, bright sunshine on her face, " + DAY,
    k("藍光少了一些，", "追問"), k("太陽怎麼還這麼亮？", "句尾上揚"))
chief("chief-half", C("holding one hand flat and sweeping it straight down like a falling beam"),
      c("少掉的不算多。"), c("晴天時，一半以上的陽光，還是直直照到地面。"))
kid("kid-bright", "Waist-up medium shot of the girl " + ROOF + " spreading her arms in bright sunshine with a happy squint, " + DAY,
    k("難怪白天，", "想通"), k("地上還是亮亮的！"))
kid("kid-hot-guess", "Waist-up medium shot of the girl " + ROOF + " fanning her face with one hand as if very hot, looking at " + SUNSET,
    k("那傍晚太陽變紅，", "推理"), k("是燒得更熱了嗎？", "很有把握的錯猜", "S:sunset"))
chief("chief-same-sun2", C("shaking her head gently with a kind smile"),
      c("太陽中午和傍晚都一樣，變的不是它。"), c("變的是光走到你眼前的那條路。"))
kid("kid-path-q", "Head-and-shoulders close-up of the girl frowning in confusion with one hand scratching her head, " + DAY,
    k("路會變？", "不解"), k("太陽又沒有變遠。"))
chief("chief-path", C("drawing a long slanting line in the air with one finger"),
      c("對，距離沒變，"), c("變的是光在路上要穿過的空氣，厚了很多。"))
scene("path-overhead", "Wide view of a simple diagram of a big round Earth with a thin glowing blue air layer around it, a tiny girl standing on top, one short golden sunbeam coming straight down to her from above, " + DAY,
      c("太陽在頭頂上的時候，"), c("光是直直穿下來，走的空氣比較少。"))
scene("path-sideways", "Wide view of a simple diagram of a big round Earth with a thin glowing blue air layer around it, a tiny girl standing on top, one very long golden-red sunbeam skimming in sideways through the air layer to her, ",
      c("太陽快下山時，光是斜斜地，"), c("貼著地面穿過來。"))
chief("chief-thirty", C("stretching her arms far apart as if showing a very long distance, eyebrows raised"),
      c("等太陽貼到地平線上，光要穿過的空氣，", "數字放慢"), c("大約是太陽在頭頂時的三十多倍。"))
kid("kid-far", "Head-and-shoulders close-up of the girl with her mouth wide open in surprise, both hands on her cheeks, " + DAY,
    k("三十多倍？", "大驚"), k("好厚喔！"), k("光要走好長的路！"))
scene("beam-fade", "Wide view of one long sunbeam crossing the sky from left to right, many small blue arrows peeling off it along the way, the beam turning from white to golden to red-orange as it travels, ",
      c("路這麼長，藍光一路被彈走、彈走、再彈走。"), c("走到你眼睛時，剩下的多半是紅色和橙色。", None, "P:sunset"))
chief("chief-lower", C("lowering one flat hand slowly like a setting sun, a calm smile"),
      c("所以太陽越貼近地平線，通常就越紅。"), c("不過再紅的太陽，也別一直盯著看，眼睛會受傷。"))
kid("kid-leftover", "Waist-up medium shot of the girl " + ROOF + " looking at " + SUNSET + " with a thoughtful face, one hand on her chin",
    k("那早上的日出，", "追問"), k("也是這樣嗎？", "句尾上揚"))
chief("chief-leftover", C("nodding with her eyes gently closed and a warm smile", close=True),
      c("一樣。日出的時候，光也是貼著地面斜斜穿過來，"), c("只是太陽換到了東邊。"))
kid("kid-where-gone", "Head-and-shoulders close-up of the girl looking around over her shoulder with a curious face, " + DAY,
    k("那半路被彈走的藍光，", "追問"), k("跑去哪裡了？", "句尾上揚", "S:gone"))
chief("chief-elsewhere", C("pointing far away to one side with a gentle smile"),
      c("它們被彈進別的地方的天空。"), c("你這邊看著紅太陽的時候，"))
scene("far-town", "Wide view of a small faraway town of rooftops and hills under a deep bright blue afternoon sky, " + DAY,
      c("同一道光彈出去的藍光，", None, "P:gone"), c("正讓更遠的地方，看到下午的藍天。"))
chief("chief-quote", C("placing one hand on her chest with a warm thoughtful smile", close=True),
      c("美國國家氣象局的科學家科菲迪這樣說："), c("夕陽會紅，是因為白天的天空是藍的。"))
kid("kid-sky-share", "Head-and-shoulders close-up of the girl hugging herself with a delighted grin, warm sunset glow on her face",
    k("我的夕陽，", "驚喜"), k("是別人的藍天！"))
chief("chief-cup-back", C("holding up one tall clear glass of water with a faint milky cloudiness and smiling"),
      c("那杯加了牛奶的水，現在可以揭曉了。", "賣關子"))
scene("milk-side", "Close-up of a tall clear glass of milky water on a kitchen table lit from the left by a small flashlight, the water glowing a faint pale blue, " + DAY,
      c("手電筒從側邊照進去，從旁邊看，"), c("水裡帶著一點淡淡的藍。"))
scene("milk-end", "Close-up looking straight through a tall clear glass of milky water toward a small flashlight behind it, the light coming through the glass glowing soft orange-red, " + DAY,
      c("你繞到另一頭，迎著手電筒看，"), c("穿過來的光，反而偏橙、偏紅。", None, "P:milk"))
kid("kid-cup-sky", "Waist-up medium shot of the girl at a kitchen table leaning close to a tall glass of milky water with sparkling amazed eyes, " + DAY,
    k("一杯水裡，", "驚喜"), k("有天空也有夕陽！"), k("牛奶在裡面做了什麼？", "追問"))
chief("chief-milk-why", C("pinching two fingers together, then opening her hand like scattering seeds"),
      c("牛奶裡的小顆粒，就像空氣的分子在彈光。"), c("光在水裡走得越遠，被彈走的藍光就越多。"))
kid("kid-try", "Waist-up medium shot of the girl at a kitchen table pouring a few drops of milk from a small cup into a tall glass of water, concentrating, " + DAY,
    c("你在家也能試：一杯水、幾滴牛奶、一支手電筒。", "轉向觀眾"), c("看不出顏色，就再多加兩滴。"))
kid("kid-flashlight", "Head-and-shoulders close-up of the girl holding up a small flashlight in one hand with a big excited grin, " + DAY,
    k("我要借爸爸的手電筒！", "興奮"))
kid("kid-cloud-back", "Waist-up medium shot of the girl " + ROOF + " pointing up at one big puffy white cloud, a puzzled frown, " + DAY,
    c("做完杯子，你再抬頭看看窗外的雲。", "轉向觀眾"), k("雲也被同一個太陽照，", "想到"), k("它怎麼不藍也不紅？", "章尾停住，句尾上揚"))

# ---------- 第四章 ----------
chief("chief-droplets", C("cupping her two hands together as if holding a little water"),
      c("因為雲是很多小水滴，"), c("一顆小水滴，比空氣分子大得多。"), chapter="雲、霧和火山，換了天空的顏色")
scene("droplet-all", "Close-up of one round water droplet in the air with sunbeams hitting it and arrows in every colour of the rainbow bouncing off it evenly in every direction, a pale sky-blue background, " + DAY,
      c("大顆的水滴，把每種顏色都彈得差不多。"), c("全部顏色一起彈過來，混起來就是白的。", None, "P:cloud"))
kid("kid-fog", "Waist-up medium shot of the girl standing in a misty park in the morning, white fog all around, smiling and waving one hand through it, bright morning sunshine",
    k("起霧的早上，", "想到"), k("也是白白的！"))
chief("chief-fog", C("nodding with a warm smile", close=True),
      c("對，霧也是小水滴，道理一樣。"), c("早上的霧被太陽一照，就是白茫茫一片。"))
kid("kid-gray-q", "Waist-up medium shot of the girl " + ROOF + " looking up at a big dark grey rain cloud rolling in, a worried face, bright daylight around the cloud",
    k("那快下雨的時候，", "追問"), k("雲怎麼變成灰的？", "句尾上揚", "S:gray"))
scene("thick-cloud", "Wide view of a huge thick puffy cloud with a bright white sunlit top and a dark grey underside, a few sunbeams around its edges, " + DAY,
      c("雲一變厚，陽光就穿不太過去，"), c("底下照到的光少了，看起來就灰灰暗暗。", None, "P:gray"))
chief("chief-contrast", C("raising one finger with a knowing smile", close=True),
      c("有時候雲沒那麼暗，是旁邊的天空太亮，"), c("眼睛一比，就覺得它灰。"))
kid("kid-eyes-again", "Head-and-shoulders close-up of the girl pointing at her own eye and laughing, a plain pale wall behind her, " + DAY,
    k("眼睛又在挑顏色了！", "笑"))
kid("kid-orange-cloud", "Waist-up medium shot of the girl " + ROOF + " pointing at small clouds glowing bright orange and pink near " + SUNSET,
    k("可是傍晚的雲，", "發現"), k("是橙色、粉紅色的！", "開心"))
chief("chief-cloud-light", C("raising one hand toward the side as if catching light, a pleased smile"),
      c("因為照到它的光，已經被一路彈成紅的了。"), c("雲像一塊大布幕，把收到的顏色彈給你。"))
kid("kid-movie", "Head-and-shoulders close-up of the girl clapping her hands with a delighted grin, warm orange sunset glow on her face",
    k("天空在演電影！", "開心"))
kid("kid-dust-guess", "Waist-up medium shot of the girl in a sunny street blowing a puff of dust off her palm with a confident grin, " + DAY,
    c("水滴會把天空的顏色換掉，空氣裡飄的灰塵也會。"), k("那灰塵越多，", "很有把握的錯猜"), k("天空就越藍？", None, "S:dust"))
chief("chief-opposite", C("shaking one finger gently with a smile"),
      c("還記得瑞利那時候的人怎麼猜嗎？", None, "P:olddust"), c("你跟他們想的一樣，可是答案剛好相反。"))
chief("chief-haze", C("waving one hand slowly in front of her face as if through haze", close=True),
      c("灰塵和煙的顆粒比較大，"), c("白天的藍會變淡，像蒙上一層白紗。", None, "P:dust"))
scene("hazy-city", "Wide view of a city skyline under a pale milky whitish sky in hazy sunshine, the sun a soft white disc, ",
      c("這種霧濛濛的一層，叫做霾。"), c("霾多的時候，中午的天空也可能白白一片。"))
kid("kid-clear-day", "Waist-up medium shot of the girl " + ROOF + " stretching happily under a deep clear blue sky, " + DAY,
    c("所以天空最藍的日子，"), c("常常是空氣很乾淨的日子。"), k("難怪有的日子，天空特別藍！", "想通"))
kid("kid-sunset-q", "Head-and-shoulders close-up of the girl with a curious frown and one finger raised, warm sunset glow on her face",
    k("那灰塵多的時候，", "追問"), k("夕陽會變怎樣？", "句尾上揚"))
chief("chief-unsure", C("tilting one hand side to side with an honest smile"),
      c("夕陽就說不準了：有時候更紅，"), c("有時候反而灰濛濛的。"))
kid("kid-plane", "Head-and-shoulders close-up of the girl looking out of a round airplane window at a glowing orange sky, amazed, warm bright sunset light",
    c("霾多的傍晚坐飛機，會看到：地上的夕陽淡淡的；"), c("飛機一爬過那層霾，天上的顏色就鮮豔起來。"))
kid("kid-plane-react", "Head-and-shoulders close-up of the girl pressing both palms against her cheeks with a big grin, a plain pale wall behind her, " + DAY,
    k("霾把顏色蓋住了！", "恍然大悟"))
chief("chief-high-cloud", C("raising one hand high above her head with a pleased smile"),
      c("霾都在低處，所以傍晚最紅的，常常是高雲："), c("照到它的光，還沒穿過底下那層霾。"), k("高的雲，紅得最漂亮！", "想通"))
chief("chief-volcano-q", C("leaning forward with a mysterious little smile", close=True),
      c("還有一種更特別的晚霞，跟火山有關。", "賣關子", "S:volcano"), c("一九九一年，菲律賓的皮納圖博火山大爆發。"))
scene("volcano", "Wide view of a big volcano on a green island erupting a tall grey ash column high into a blue sky, " + DAY,
      c("火山噴出的氣體，在高空變成細細的小液滴，"), c("慢慢飄散在大約二、三十公里高的地方。"))
kid("kid-so-high", "Head-and-shoulders close-up of the girl craning her neck to look straight up with her mouth open, " + DAY,
    k("飛那麼高？", "驚訝"), k("那地上看得到嗎？", "句尾上揚"))
scene("afterglow", "Wide view of a quiet town of rooftops just after sunset, the sky high above glowing soft lilac and red-orange, ",
      c("太陽下山大約十五分鐘後，地面暗了，"), c("高空那一層還照得到太陽，被照成淡紫色和橙紅色。"))
chief("chief-months", C("counting on her fingers with raised eyebrows"),
      c("這種火山晚霞，斷斷續續出現了大約一年半。", None, "P:volcano"), c("連地球另一邊的美國，都看得到。"))
kid("kid-volcano", "Head-and-shoulders close-up of the girl with both hands up beside her face in amazement, a plain pale wall behind her, " + DAY,
    k("火山在幫天空，", "驚喜"), k("換顏色！"))
chief("chief-strange", C("looking straight at the viewer with a curious smile, one hand on her chin", close=True),
      c("下次你看到特別怪的夕陽，可以想一想：", "轉向觀眾"), c("今天的空氣裡，多了什麼？"))

# ---------- 收尾 ----------
chief("chief-moon-back", C("pointing upward with one finger and a playful smile"),
      c("空氣多一點，顏色就變；那幾乎沒有空氣呢？", "接住上一句"), c("還記得開頭那個問題嗎？站在月球上，白天抬頭看。", "轉向觀眾"), chapter="站在月球上抬頭看")
kid("kid-moon-think", "Head-and-shoulders close-up of the girl with her eyes closed tight and both hands on her temples, thinking hard, " + DAY,
    k("月球上……", "慢慢想"), k("有空氣嗎？", "句尾上揚"))
chief("chief-almost", C("holding her finger and thumb almost touching", close=True),
      c("幾乎沒有，只有非常非常稀薄的一點點。"))
kid("kid-moon-reason", "Waist-up medium shot of the girl pointing one finger up with a sudden bright idea face, a plain pale wall behind her, " + DAY,
    k("沒有空氣，就沒有小球，", "推理"), k("把藍光彈給我……", "放慢"))
kid("kid-moon-black", "Head-and-shoulders close-up of the girl gasping with both hands over her mouth, eyes wide, " + DAY,
    k("那天空是黑的！", "大驚"))
scene("moon-black", "Wide view of the grey cratered surface of the Moon in dazzling sunshine under an inky black sky, the bright white sun in the black sky, ",
      c("對。太陽明明很亮，月球白天的天空，卻是黑的。", None, "P:moon"), c("亮亮的地面，配上一整片黑漆漆的天。"))
kid("kid-got-it", "Waist-up medium shot of the girl " + ROOF + " throwing both arms up with a huge happy smile, " + DAY,
    k("我知道了！", "自己想通"), k("還記得我在頂樓看到的藍和紅嗎？", "篤定"))
kid("kid-got-it2", "Head-and-shoulders close-up of the girl pointing proudly over her shoulder toward " + SUNSET + ", a big grin",
    k("是同一道光，", "篤定"), k("走了短的路和長的路！", "開心", "P:same"))
chief("chief-done", C("smiling warmly at the viewer with her hands clasped", close=True),
      c("下次你抬頭看天空，可以想一想：", "轉向觀眾，輕聲"), c("這道光，一路走了多遠，才來到你眼前。"))
# The outro is three pictures, no card (series README §3.2, P05).
kid("outro", "Head-and-shoulders close-up of the girl with a big happy smile proudly holding up a big red rubber stamp in one hand, bright morning light",
    k("原來如此！", "開心大聲"))
chief("outro-chief", "Waist-up medium shot of the chief tilting her head with a curious smile and one finger raised, a plain pale wall behind her, bright morning light",
      c("你看過最特別的夕陽，是什麼顏色？", "問句上揚，像聊天"), c("在哪裡看到的？留言告訴我們。"))
chief("outro-wave", "Waist-up medium shot of the chief waving goodbye with a warm smile, a plain pale wall behind her, bright morning light",
      c("想一起找生活裡的為什麼，就訂閱原來如此事務所。", "誠懇"))

# ---------- assemble ----------
WHAT = {"where": "天空的藍是從哪裡來的", "milk": "加了牛奶的水被手電筒照，是什麼顏色", "moon": "站在月球上，白天的天空是什麼顏色",
        "cloud": "天空是藍的，雲為什麼是白的", "same": "同一道陽光，為什麼一下藍一下紅", "always": "天空是不是本來就是藍的",
        "white": "陽光是什麼顏色", "short": "藍光是比較短的浪，這件事有什麼用", "airblue": "空氣是不是藍的",
        "sea": "天空是不是海倒映上去的", "violet": "紫光的波更短，天空為什麼不是紫的", "suncolor": "太陽本身是什麼顏色",
        "sunset": "傍晚太陽變紅，是不是燒得更熱", "gone": "半路被彈走的藍光跑去哪了", "gray": "快下雨時雲為什麼變灰",
        "dust": "灰塵越多天空是不是越藍", "volcano": "跟火山有關的特別晚霞", "swap": "是什麼東西在偷換天空的顏色", "olddust": "以前的人以為是灰塵把藍光彈開"}
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
    # The series tag: the approved character sheets live in the series store and the next episode reuses them (docs/videos/SERIES.md).
    "series": {"slug": "sothatswhy", "episode": 14, "chapter": 1},
    # Same 14-minute bed as P02/P05 (one paid Lyria take, tail trimmed, crossfaded): the series sounds the same.
    "music": {"track": "sothatswhy-p02-bed.m4a", "sha256": "54169439df49a00bc3ad993a148690be9f79d1dff8a4ea5143e64e583001b20c", "gain_db": -20, "duck_db": -10},
    "characters": CHARACTERS, "loops": loops,
    "youtube": {
        "category_id": 27, "made_for_kids": False, "default_language": "zh-TW",
        "title": "同一道陽光，天空為什麼是藍的、夕陽卻是紅的？｜原來如此事務所",
        "description": "中午在頂樓抬頭，天空藍得發亮；傍晚再上去，太陽變成一顆紅紅的大球。照下來的是同一道陽光，空氣又是透明的，顏色是從哪裡來的？\n\n"
                       "這一集，所長和小問跟著同一道陽光走一趟：白光裡藏著哪些顏色、空氣怎麼把藍光彈向四面八方、天空為什麼不是紫色的、"
                       "傍晚的光為什麼多走了好長一段路、一杯加了牛奶的水怎麼同時裝著藍天和夕陽、雲為什麼是白的，最後站到月球上抬頭看一次。\n\n"
                       "本集插圖由 AI 生成。倍數與距離都是教學資料裡的大約數量級；每個說法的出處列在下方參考資料。\n\n資料截至 " + CHECKED,
        "tags": ["天空為什麼是藍的", "夕陽為什麼是紅的", "瑞利散射", "散射", "雲為什麼是白的", "牛奶實驗", "科普", "原來如此事務所"],
        "video_id": None},
    "thumbnail": {"template": "thumb", "data": {"headline": "天空的藍\n**是彈過來的**", "sub": "同一道陽光，傍晚就變紅", "shot": "roof-sunset"}},
    "sources": [
        {"title": "NASA Space Place: Why Is the Sky Blue?", "url": "https://spaceplace.nasa.gov/blue-sky/en/", "checked_on": CHECKED},
        {"title": "Philip Gibbs, Why is the sky blue? (Physics FAQ, UC Riverside)", "url": "https://math.ucr.edu/home/baez/physics/General/BlueSky/blue_sky.html", "checked_on": CHECKED},
        {"title": "Stephen F. Corfidi, The Colors of Sunset and Twilight (NOAA/NWS Storm Prediction Center)", "url": "https://www.spc.noaa.gov/publications/corfidi/sunset/", "checked_on": CHECKED},
        {"title": "NOAA JetStream: The Color of Clouds", "url": "https://www.noaa.gov/jetstream/clouds/color-of-clouds", "checked_on": CHECKED},
        {"title": "UCAR Center for Science Education: The Colors of the Sky", "url": "https://scied.ucar.edu/kids/sky-wonders/colors-sky", "checked_on": CHECKED},
        {"title": "UCAR Center for Science Education: The Appearance of the Sky", "url": "https://scied.ucar.edu/learning-zone/atmosphere/appearance-sky", "checked_on": CHECKED},
        {"title": "HyperPhysics: Blue Sky and Rayleigh Scattering", "url": "https://hyperphysics.gsu.edu/hbase/atmos/blusky.html", "checked_on": CHECKED},
        {"title": "HyperPhysics: Red Sunset, Green Flash", "url": "https://hyperphysics.gsu.edu/hbase/atmos/redsun.html", "checked_on": CHECKED},
        {"title": "NASA Goddard: What Color is the Sun?", "url": "https://science.gsfc.nasa.gov/attic/eclipse2017.gsfc.nasa.gov/what-color-sun.html", "checked_on": CHECKED},
        {"title": "Wikipedia: Air mass (solar energy)", "url": "https://en.wikipedia.org/wiki/Air_mass_(solar_energy)", "checked_on": CHECKED},
        {"title": "PVEducation: Air Mass", "url": "https://www.pveducation.org/pvcdrom/properties-of-sunlight/air-mass", "checked_on": CHECKED},
        {"title": "NASA Science: 9 Phenomena NASA Astronauts Will Encounter at the Moon's South Pole", "url": "https://science.nasa.gov/solar-system/moon/phenomena-nasa-astronauts-will-encounter-at-moons-south-pole/", "checked_on": CHECKED},
        {"title": "NASA: Dark Sky, Bright Sun", "url": "https://www.nasa.gov/image-article/dark-sky-bright-sun/", "checked_on": CHECKED},
        {"title": "Wikipedia: Critical opalescence (Einstein 1910)", "url": "https://en.wikipedia.org/wiki/Critical_opalescence", "checked_on": CHECKED},
        {"title": "Wikipedia: Isaac Newton", "url": "https://en.wikipedia.org/wiki/Isaac_Newton", "checked_on": CHECKED},
        {"title": "Wikipedia: Rayleigh scattering", "url": "https://en.wikipedia.org/wiki/Rayleigh_scattering", "checked_on": CHECKED},
        {"title": "Wikipedia: Storm Prediction Center", "url": "https://en.wikipedia.org/wiki/Storm_Prediction_Center", "checked_on": CHECKED},
        {"title": "Wikipedia: Haze", "url": "https://en.wikipedia.org/wiki/Haze", "checked_on": CHECKED},
        {"title": "Wikipedia: 1991 eruption of Mount Pinatubo", "url": "https://en.wikipedia.org/wiki/1991_eruption_of_Mount_Pinatubo", "checked_on": CHECKED},
    ],
    "assets": [],
    "scenes": scenes,
}
json.dump(doc, open(os.path.join(HERE, "video.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
FROZEN.update({s["id"]: s["data"]["camera"] for s in scenes if s["template"] == "shot" and s["id"] not in FROZEN})
json.dump(FROZEN, open(CAM_FILE, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# ---------- self-checks (the series rules lint does not cover for a sothatswhy- slug) ----------
RATE = 4.5
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
