"""Generate video.json for sothatswhy-p20-microwave-metal (原來如此事務所 對話版 P20).

Run `python3 build_scenes.py` from anywhere: it rewrites video.json next to this file and freezes
every shot's camera move in cameras.json (a shot keeps the camera it was first given, so deleting
a shot never shifts the others: the camera is in the keyframe cache key).
Edit lines and prompts here, never in video.json.
Started from a copy of sothatswhy-p01-wireless-energy/build_scenes.py (series constants, helpers,
BANNED, assembly and self-checks unchanged; EXTRA and REWRITE start empty because P01's entries were picture
fixes for P01 only; the SAY loop is P29's and spells the one Latin brand name, GE); the content is new.
2026-11-11 rules applied (dialogue-pilot README §4, §9, §10.6): the faster voice style for both characters,
`pauses: {line_ms: 0, scene_ms: 150}` and `still_motion: "beat"`, no `pause_after_ms` on lines except a
BEAT_MS beat on the line right before each `P:` payoff in the same scene, and only an upper bound on length.
Line caps here count punctuation (chief <= 25, kid <= 15), as in P01.
`script.md` is written by `node tools/video/cli.mjs script --slug sothatswhy-p20-microwave-metal` after this runs.
"""
import hashlib, itertools, json, os, re, sys, unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = "sothatswhy-p20-microwave-metal"
CHECKED = "2026-11-12"
BEAT_MS = 500   # 答案揭曉前的一拍（README §10.6）

# ---------- series constants (identical to P04 and P01) ----------
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
EXTRA = {     # lines added to a prompt after the storyboard score (round 1)
    "chief-not-more": ", glossy all-black hair in one uniform colour, bare earlobes, natural pale lips, round black glasses centred over her eyes, adult woman proportions",
    "chief-wire": ", glossy all-black hair in one uniform colour, bare earlobes, natural pale lips, round black glasses centred over her eyes, adult woman proportions",
    "chief-spoon": ", glossy all-black hair in one uniform colour, bare earlobes, natural pale lips, round black glasses centred over her eyes, adult woman proportions",
    "chief-fda-manual": ", glossy all-black hair in one uniform colour, bare earlobes, natural pale lips, round black glasses centred over her eyes, adult woman proportions",
    "chief-your-home": ", glossy all-black hair in one uniform colour, bare earlobes, natural pale lips, round black glasses centred over her eyes, adult woman proportions",
    "chief-spark": ", glossy all-black hair in one uniform colour, bare earlobes, natural pale lips, round black glasses centred over her eyes, adult woman proportions",
    "chief-opinion": ", glossy all-black hair in one uniform colour, bare earlobes, natural pale lips, round black glasses centred over her eyes, adult woman proportions",
    "outro-wave": ", glossy all-black hair in one uniform colour, bare earlobes, natural pale lips, round black glasses centred over her eyes, adult woman proportions",
    "chief-ptray": ", glossy all-black hair in one uniform colour, bare earlobes, natural pale lips, round black glasses centred over her eyes, adult woman proportions",
    "kid-try": ", all jet-black hair, closed navy coat",
    "kid-whose": ", all jet-black hair, closed navy coat",
    "kid-gold-q": ", all jet-black hair, closed navy coat",
    "outro": ", all jet-black hair, closed navy coat",
    "kid-charge-q": ", all jet-black hair, closed navy coat",
}
REWRITE = {   # whole-prompt rewrites after a visual review (zoom check round 1)
    "magnetron-glow": "Cutaway diagram of a plain white cartoon microwave oven seen from the side with its side panel removed, an empty grey metal cooking chamber on the left filled with many crowded bright-blue wavy lines, the wavy lines streaming to the right into a chunky silver cylinder with stacked cooling fins mounted in a slim compartment beside the chamber, the silver cylinder glowing hot red-orange with small orange sparks around it, plain cream background, simple flat 2D cel-shaded cartoon drawing with clean ink outlines and flat colours",
    "empty-bounce": "Close-up looking straight into an open plain white cartoon microwave oven with a smooth plain front and round white buttons, shiny pale grey metal inside walls and a bare round glass turntable plate in the middle, three bold bright-blue zigzag wave lines bouncing back and forth between the left and right metal walls and crossing over the empty plate, each wave line thick and clearly visible in front of the grey walls, warm cream background, simple flat 2D cel-shaded cartoon drawing with clean ink outlines and flat colours",
    "kid-gold-q": "Waist-up medium shot of the girl in a bright cartoon office kitchenette, holding up a small white rice bowl with a thin shiny gold rim around its edge in both hands and looking at it with a thinking face, bright daylight, the girl is eight, with jet-black hair cut in a short straight bob with blunt bangs and one small cowlick, simple dot-like cartoon eyes, a closed navy raincoat jacket with toggle buttons and a mustard-yellow hood resting on her shoulders, simple flat 2D cel-shaded cartoon drawing with clean ink outlines and flat colours",
    "chief-water": "Waist-up medium shot of the chief filling most of the frame against a plain pale cream wall, wiggling the fingers of both hands quickly in front of her chest with a bright smile, five small round blue water drops wobbling in the air between her hands, bright daylight, the chief is a slim adult woman of about thirty-five with glossy jet-black hair in one even colour tied in a low ponytail, bare earlobes, natural pale lips, round black glasses centred over her eyes, a yellow pencil tucked behind her ear, a mustard-yellow cardigan over a white blouse and navy trousers, simple flat 2D cel-shaded cartoon drawing with clean ink outlines and flat colours",
    "kid-allrack-q": "Waist-up medium shot of the girl in a bright cartoon office kitchenette, pointing at the open door of a plain white cartoon microwave oven with a low round chrome wire rack standing on short legs on its turntable, a curious face, round plain knobs, bright daylight, the girl is eight, with jet-black hair cut in a short straight bob with blunt bangs and one small cowlick, simple dot-like cartoon eyes, a closed navy raincoat jacket with toggle buttons and a mustard-yellow hood resting on her shoulders, simple flat 2D cel-shaded cartoon drawing with clean ink outlines and flat colours",
    "chief-electron": "Head-and-shoulders close-up of the chief holding up a short shiny metal bar in one hand, a swarm of tiny glowing blue dots zipping around inside the bar, a curious smile with clear dark eyes behind her glasses, a plain pale wall behind, bright daylight, the chief is a slim young woman of about thirty with glossy all-black hair in one uniform colour tied in a low ponytail, bare earlobes, natural pale lips, round black glasses centred over her eyes, a yellow pencil tucked behind her ear, a mustard-yellow cardigan over a white blouse, simple flat 2D cel-shaded cartoon drawing with clean ink outlines and flat colours",
    "chief-smooth": "Waist-up medium shot of the chief filling most of the frame, holding up a big smooth shiny round steel ball in one palm and running a finger over its smooth surface, a calm smile, a plain pale wall behind, bright daylight, the chief is a slim young woman of about thirty with glossy all-black hair in one uniform colour tied in a low ponytail, bare earlobes, natural pale lips, round black glasses centred over her eyes, a yellow pencil tucked behind her ear, a mustard-yellow cardigan over a white blouse, simple flat 2D cel-shaded cartoon drawing with clean ink outlines and flat colours",
    "chief-textbook": "Waist-up medium shot of the chief filling most of the frame, holding a thick open physics volume in one hand showing a simple drawing of a pointed metal tip crowded with little plus dots, pointing at the tip with her other finger, a bright clear smile, a plain pale wall behind, bright daylight, the chief is a slim young woman of about thirty with glossy all-black hair in one uniform colour tied in a low ponytail, bare earlobes, natural pale lips, round black glasses centred over her eyes, a yellow pencil tucked behind her ear, a mustard-yellow cardigan over a white blouse, simple flat 2D cel-shaded cartoon drawing with clean ink outlines and flat colours",
    "chief-tray-up": "Waist-up medium shot of the chief filling most of the frame, holding a perfectly round shallow clear plastic dish of blue water level in both hands like a pie plate, the water tilting gently to one side, a playful smile with clear dark eyes behind her glasses, a plain pale wall behind, bright daylight, the chief is a slim young woman of about thirty with glossy all-black hair in one uniform colour tied in a low ponytail, bare earlobes, natural pale lips, round black glasses centred over her eyes, a yellow pencil tucked behind her ear, a mustard-yellow cardigan over a white blouse, simple flat 2D cel-shaded cartoon drawing with clean ink outlines and flat colours",
    "oven-back": "Cutaway side view of a plain white cartoon microwave oven with its right side panel removed, showing inside the casing a chunky silver cylinder with cooling fins mounted beside the cooking chamber, three soft wavy pale-blue ripples flowing from the cylinder into the chamber toward a smooth plain white bowl of rice on a round glass turntable, three round plain knobs on the front, warm cream background, simple flat 2D cel-shaded cartoon drawing with clean ink outlines and flat colours",
    "chief-hooks": "Waist-up medium shot of the chief beside a plain white cartoon microwave oven, pointing at its closed door whose big window is covered by a dark grey grid of tiny round holes, a playful mysterious smile, a plain pale wall behind, bright daylight, the chief is a slim young woman of about thirty with glossy all-black hair in one uniform colour tied in a low ponytail, bare earlobes, natural pale lips, round black glasses centred over her eyes, a yellow pencil tucked behind her ear, a mustard-yellow cardigan over a white blouse, simple flat 2D cel-shaded cartoon drawing with clean ink outlines and flat colours",
    "foil-wing": "Close-up of one golden roast chicken drumstick lying on a plain white plate on a light wooden counter, warm cream wall behind, the thin bone end of the drumstick covered by a small sleeve of shiny silver aluminium foil pressed smooth and tight around it like a snug sock, every edge of the foil folded flat against the meat, the foil bright metallic silver with crisp white shine streaks and pale blue-grey shading, glossy golden brown skin with a few highlight shapes, simple flat 2D cel-shaded cartoon drawing with clean ink outlines and flat colours",
    "food-uneven": "Close-up of a plain white bowl of Taiwanese braised pork rice, fluffy white rice topped with glossy brown braised minced pork, on a light wooden counter. A shiny round steel pot lid rests across the left half of the bowl, and the rice peeking out under its edge looks pale and cold. The right half of the bowl is uncovered, with warm wisps of steam curling up from it. Warm cream background, clean empty corners, simple flat 2D cel-shaded cartoon drawing with clean ink outlines and flat colours",
    "ptray-splash": "Top-down view looking straight down at a light wooden counter, on it one shallow clear plastic dish shaped exactly like a big slice of pizza, a rounded wide edge at the left and one sharp pointed corner at the right, filled with bright blue water, the water calm and flat near the rounded edge and heaped up into a tall wave at the sharp pointed corner, where a little spray of round blue droplets leaps over the tip onto the counter, simple cartoon water with white highlight shapes, plain warm cream surroundings, simple flat 2D cel-shaded cartoon drawing with clean ink outlines and flat colours",
    "kid-door-q": "Waist-up medium shot of the girl standing at a light wooden counter in a bright cartoon office kitchenette, a plain white cartoon microwave oven on the counter beside her, its closed door with a big window covered by a dark grey grid of tiny round holes, the control panel showing only three round plain knobs, she reaches out and touches the door edge with one index finger, a small worried frown, the girl is an 8-year-old with a chin-length straight black bob hanging loose around her face, straight bangs and one thin curl of a cowlick on top, wearing a closed navy raincoat jacket with toggle buttons and a mustard-yellow hood resting on her shoulders, cute chibi cartoon proportions with a big round head, a small girl of eight, simple flat 2D cel-shaded cartoon drawing with clean ink outlines and flat colours",
    "mesh-close": "Close-up of the girl peering at the closed door of a plain white cartoon microwave oven, her nose almost touching the door window, the window covered by a dark grey metal grid of many tiny round holes in neat rows, behind the holes a bowl of braised pork rice clearly visible on the glass turntable in a soft warm glow, the girl is an 8-year-old with a short black bob, straight bangs and one small cowlick on top, wearing a navy raincoat jacket with a mustard-yellow hood, simple flat 2D cel-shaded cartoon drawing with clean ink outlines and flat colours",
    "chief-wavelength": "Waist-up medium shot of the chief against a plain pale cream wall, both hands raised in front of her chest with palms facing each other a hand-span apart, one short wiggly blue ribbon floating between her palms shaped like a single gentle S-curve, its two ends near each palm, she looks at it with a curious smile, the chief is a slim adult woman of about thirty-five with glossy jet-black hair in one even colour tied in a low ponytail, bare earlobes, natural pale lips, round black glasses centred over her eyes, a yellow pencil tucked behind her ear, a mustard-yellow cardigan over a white blouse and navy trousers, simple flat 2D cel-shaded cartoon drawing with clean ink outlines and flat colours",
    "kid-more-wrong": "Waist-up medium shot of the girl in a bright cartoon office kitchenette, standing beside a plain white cartoon microwave oven with its door wide open and shiny pale grey metal inside walls, looking into it with wide surprised eyes and her mouth in a little round o, one hand pointing at the metal walls, the oven control panel shows only round plain knobs, the girl is an 8-year-old with a short black bob, straight bangs and one small cowlick on top, wearing a navy raincoat jacket with a mustard-yellow hood, simple flat 2D cel-shaded cartoon drawing with clean ink outlines and flat colours",
    "fork-spoon": "Waist-up shot of the chief standing in a bright cartoon office kitchenette, holding up a shiny steel fork with four thin pointed prongs in her right hand and a thick shiny steel spoon with a smooth round bowl in her left hand, looking from one to the other with a curious smile, the chief is a slim young woman of about thirty with round black glasses centred over her eyes, glossy all-black hair in one uniform colour tied in a low ponytail, bare earlobes, natural pale lips, a yellow pencil tucked behind one ear, a mustard-yellow cardigan over a white blouse and navy trousers, simple flat 2D cel-shaded cartoon drawing with clean ink outlines and flat colours",
}
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


# One drawing language for the whole episode (README §10.5: the image model cannot draw fields, waves, charges,
# diagrams, labels, arrows, counts or directions). The main thread is ONE lunchtime: 小問 brings grandma's braised
# pork rice to the office in a takeaway box with a thin wire handle and is about to microwave it; the chief stops
# her. They look inside the office microwave (metal walls, a metal rack, a metal mesh in the door), compare a fork
# with a spoon on the counter, read the oven's owner's manual, and finally reheat the rice in a plain ceramic bowl.
# The one analogy carried from start to end is THE SHAKEN TRAY OF WATER: tip a shallow plastic tray of water from
# side to side and the water runs back and forth (the microwave pushes the electrons in metal back and forth,
# Bloomfield). In a big round-ended tray the water only rises and falls a little (the oven's big smooth walls);
# in a tray that narrows to a point the water rushes into the tip, piles up and splashes out (charge crowds at
# points and leaps into the air as a spark, OpenStax 18.7); two trays set almost touching splash across the
# narrow gap (a narrow gap needs less push to spark, OpenStax 19.2). Food water is pushed back and forth too and
# warms (FDA). Limits in claims.md C20.
# Every frame is an everyday object at human scale or a simple cartoon room; the oven has a smooth unmarked
# panel with round plain buttons; sparks are drawn as a few small bright zigzags and are an illustration.
KITCHEN = "in a bright cartoon office kitchenette,"
STYLE = ", simple flat 2D cel-shaded cartoon drawing with clean ink outlines and flat colours"
OVEN = "a plain white cartoon microwave oven with a smooth unmarked control panel and round plain buttons"
OPEN = OVEN + " standing open, its shiny pale grey metal inside walls and a round glass turntable plate in view"
RACK = "a simple shiny metal wire rack standing on short legs"
BOX = "a small white takeaway food box with a thin silver wire handle"
BOXK = "a small white takeaway box with a thin wire handle"
FORK = "a shiny steel fork with four slim prongs"
SPOON = "a thick shiny steel spoon with a smooth round bowl"
GOLD = "a white ceramic rice bowl with one thin shiny gold line around its rim"
BOWL = "a plain smooth white ceramic rice bowl"
TRAY = "a shallow clear plastic tray of blue water with smooth round ends"
PTRAY = "a shallow clear plastic tray of blue water shaped like a long triangle that narrows to one pointed corner"
SPARK = "a few small bright yellow zigzag sparks"
FOOD = "braised pork rice"
def obj(id, prompt, *lines, chapter=None):
    """An everyday-object frame with nobody in it, always in the flat cartoon style."""
    scene(id, prompt + STYLE + ", clean empty corners", *lines, chapter=chapter)

# ---------- 開場（系列片頭之後直接進場景，不做濃縮；結果都不先講）----------
obj("box-table", "Close-up of " + BOX + " on a wooden kitchen counter beside " + OVEN,
    k("阿嬤的滷肉飯，我拿去微波！", "開心"), chapter="阿嬤的便當盒，先別按")
obj("chief-stop", "Extreme close-up from above of the lid of a small white takeaway food box on a wooden counter, a thin shiny silver wire handle arching over the lid, its two thin bent wire ends hooked into the sides of the box, one tiny pointed wire end catching a bright glint",
    c("等一下，先別按。你看盒子上面。", "叮嚀"))
# Thumbnail shot (fixed before keyframes): the kid big and centred, the box in hand.
kid("kid-main-q", K("holding up " + BOXK + " in both hands at her chest, wide curious eyes on the viewer, in the exact centre of the picture", where=KITCHEN),
    k("鐵絲放進去會怎樣？", "句尾上揚", "S:handle"),
    c("有時候會出問題。先看看這台微波爐裡面。"))
obj("oven-rack", "Close-up of " + OPEN + ", " + RACK + " inside on the plate",
    c("這台本來就附了一個金屬架。", None, "S:rack"))
chief("chief-hooks", C("holding up one finger with a playful mysterious smile"),
    c("還有門上那片一格一格的網子，", "賣關子"),
    c("你猜，它是什麼做的？", "賣關子", "S:mesh"))
obj("fork-spoon", "Close-up of " + FORK + " and " + SPOON + " lying side by side on a wooden kitchen counter",
    c("再看這兩支：叉子和湯匙。", None, "S:fork"),
    c("同樣是金屬，為什麼有的會冒火花，有的不會？", "轉向觀眾", "S:main"))
kid("kid-guess", K("spreading both arms wide with a very confident grin", where=KITCHEN),
    k("我知道！金屬越多，", "篤定的錯猜"), k("火花就越大！", "篤定的錯猜", "S:more"))

# ---------- 第一章：打開微波爐的門 ----------
chief("chief-look-in", C("gesturing towards an open microwave oven beside her with a warm smile"),
    c("是嗎？那你看看裡面的牆，亮亮的。", "接住上一句"), chapter="打開微波爐的門，裡面亮亮的")
obj("oven-walls", "Close-up of " + OPEN + ", soft daylight shining on the smooth metal walls",
    c("美國管食品安全的食藥署說，", "接住上一句"),
    c("微波爐裡面是金屬，微波碰到它會彈回來。"))
kid("kid-wave-q", K("tilting her head with a curious face, one finger on her cheek", close=True, where=KITCHEN),
    k("微波是什麼？", "句尾上揚"),
    c("一種看不見的波，跟收音機用的電波很像。"),
    k("微波從哪裡來？", "追問"))
obj("oven-back", "Close-up of " + OVEN + " seen from the side with its side panel drawn cut open, a small plain silver metal part with cooling fins tucked beside the cooking box",
    c("爐子裡有一個零件，叫做磁控管，"),
    c("專門做出微波，送進放食物的地方。"))
chief("chief-pass", C("holding up a clear glass cup in one hand with a bright smile"),
    c("微波碰到玻璃、陶瓷、紙、塑膠，會穿過去；"),
    c("碰到食物，會被食物吸收。"))
obj("oven-plate", "Close-up of " + OPEN + ", a plain white bowl of rice on the turntable plate in the middle",
    k("那牆把它彈回來幹嘛？", "追問"),
    c("讓它在裡面來回跑，最後被食物吸收掉。"))
kid("kid-more-wrong", K("looking around the open microwave with wide surprised eyes, mouth in a little o", where=KITCHEN),
    k("整台都是金屬，沒冒火花？", "句尾上揚"))
chief("chief-not-more", C("shaking her head gently with a kind smile, one palm raised", close=True),
    c("對，沒冒火花。所以不是金屬越多，火花就越大。", None, "P:more"),
    c("還記得門上那片網子嗎？它也是金屬。", None, "P:mesh"))
obj("door-mesh", "Close-up of the window of a microwave oven door covered with a dark grey metal mesh of many tiny round holes, a plain white bowl of rice faintly visible behind it",
    k("有洞，微波不會跑出來嗎？", "句尾上揚", "S:hole"))
chief("chief-wavelength", C("holding her two hands about a ruler's length apart with a curious smile"),
    c("一位物理學教授說，微波的一個波，", "接住上一句"),
    c("大約有十二公分長。"))
obj("mesh-close", "Extreme close-up of a dark grey metal mesh with many tiny round holes in neat rows, a soft warm glow behind it",
    c("網子的洞比它小很多，微波就鑽不過去。", None, "P:hole"),
    c("可是洞又夠你看得到裡面的食物。"))
kid("kid-door-q", K("pointing at the door of a microwave oven with a worried frown", where=KITCHEN),
    k("那門壞掉了呢？", "擔心", "S:door"))
chief("chief-door", C("nodding with a serious but kind face", close=True),
    c("美國食藥署說，門和門框好好的，微波不會漏出來。"),
    c("門關不緊、彎掉了，就別再用。", "認真", "P:door"))
chief("chief-electron", C("rubbing the tips of her fingers together with a curious smile", close=True),
    k("金屬怎麼會把微波彈回來？", "句尾上揚", "S:bounce"),
    c("金屬裡有很多會跑的小東西，叫做電子。"))
kid("kid-electron-q", K("squinting at her own hand with a puzzled frown", close=True, where=KITCHEN),
    k("電子是什麼？", "句尾上揚"),
    c("很小很小、帶著電的小粒子，在金屬裡能到處跑。"))
chief("chief-tray-up", C("holding " + TRAY + " level in both hands with a playful smile"),
    c("物理學教授說，微波會推著它們來回跑。"),
    c("就像我端著這個圓圓的水盤，左右晃一晃。"))
obj("tray-slosh", "Close-up of " + TRAY + " held level on a kitchen counter, the water rocking gently from one end to the other with soft little waves",
    c("電子在牆裡這樣來回跑，微波就被彈回去了。", None, "P:bounce"),
    k("那網子有洞，也能彈嗎？", "句尾上揚", "S:meshbounce"))
chief("chief-mesh-again", C("holding up a small square of fine dark metal mesh between two fingers with a knowing smile", close=True),
    c("可以。那位教授說，網子的洞很小，電子照樣跑，", "接住上一句"),
    c("網子就跟一整片金屬一樣，把微波彈回去。", None, "P:meshbounce"))
kid("kid-heat-q", K("looking down at " + BOXK + " in her hands with a hungry thinking face", where=KITCHEN),
    k("那彈來彈去的微波，", "想不通"), k("怎麼把飯變熱？", "章尾停住，句尾上揚", "S:heat"))

# ---------- 第二章：滷肉飯裡的水被推著晃 ----------
obj("rice-bowl", "Close-up of a plain white bowl of steaming " + FOOD + " on a wooden counter, glossy brown sauce over white rice",
    c("靠飯裡的水。微波一碰到食物，", "接住上一句"),
    c("就推著裡面的水，一直晃。"), chapter="滷肉飯裡的水，被推著晃")
chief("chief-water", C("wiggling the fingers of both hands quickly in front of her chest with a bright smile"),
    c("食藥署說，水被推著晃，互相摩擦就生出熱。", None, "P:heat"))
chief("chief-water2", C("tipping one flat hand left and right with a pleased smile", close=True),
    c("晃的是水分子，就是水最小最小的一顆。"),
    c("所以水分多的食物，像新鮮蔬菜，熱得比較快。"))
kid("kid-bowl-q", K("holding " + BOWL + " in both hands with a curious frown", close=True, where=KITCHEN),
    k("那碗會被微波加熱嗎？", "句尾上揚", "S:bowl"))
chief("chief-bowl", C("holding " + BOWL + " in both hands with a careful smile", close=True),
    c("還記得嗎？陶瓷會讓微波穿過去，碗自己不會被加熱。"),
    c("可是熱的飯會把碗燙熱，拿的時候要小心。", "叮嚀", "P:bowl"))
kid("kid-wire-q", K("holding up " + BOXK + " by its thin wire handle with a thinking face", where=KITCHEN),
    k("那這條鐵絲呢？", "想起來"), k("也會被推著晃嗎？", "章尾停住，句尾上揚", "S:wire"))

# ---------- 第三章：叉子和湯匙比一比 ----------
chief("chief-wire", C("holding up one finger with a serious but kind face", close=True),
    c("會。鐵絲裡的電子，也會被推著來回跑。", "接住上一句", "P:wire"),
    c("可是鐵絲很細，又有尖尖的兩頭。"), chapter="叉子和湯匙，比一比")
obj("wire-handle", "Close-up of " + BOX + " on a wooden counter, the two thin silver wire ends poking out of the box sides",
    c("物理學教授說，細的鐵絲，可能熱到燒起來；"),
    c("而且電子容易在尖尖的那頭，擠成一堆。"))
kid("kid-crowd-q", K("squeezing her two fists together with a curious frown", close=True, where=KITCHEN),
    k("擠成一堆會怎樣？", "句尾上揚", "S:crowd"))
chief("chief-ptray", C("holding " + PTRAY + " level in both hands with an excited smile"),
    c("看這個尖尖的水盤，我一樣左右晃。", "接住上一句"))
obj("ptray-splash", "Close-up of " + PTRAY + " on a kitchen counter, the water rushing into the pointed corner, piling up high and splashing over the tip in a little spray of droplets",
    k("水擠到尖角，濺出去了！", "驚訝"))
chief("chief-textbook", C("holding up one finger with a bright clear smile"),
    c("大學的物理課本說，金屬上越尖的地方，", "接住上一句"),
    c("電荷擠得越多，周圍的推力也越強。"))
kid("kid-charge-q", K("tilting her head with a puzzled face", close=True, where=KITCHEN),
    k("什麼是電荷？", "句尾上揚"),
    c("就是那些帶著電的東西，像剛剛的電子。"))
obj("fork-spark", "Close-up of " + FORK + " lying on a round glass plate inside a microwave oven, " + SPARK + " flashing at the tips of the prongs, an illustration",
    c("推力強到一個程度，空氣也擋不住，", None),
    c("電就從尖端跳進空氣，變成一道小火花。", None, "P:crowd"))
kid("kid-lightning", K("covering her mouth with both hands and wide amazed eyes", where=KITCHEN),
    c("課本說，那是像閃電一樣的放電。"),
    k("叉子有四個尖尖的頭耶！", "發現", "S:prongs"))
chief("chief-prongs", C("holding up " + FORK + " and touching the tips of its prongs with one finger, a knowing smile", close=True),
    c("對，每個尖尖的叉子頭，電荷都會擠過去。", None, "P:prongs"))
chief("chief-spoon", C("holding up " + SPOON + " with a gentle smile", close=True),
    k("那湯匙呢？", "追問"),
    c("物理學教授說，湯匙夠厚、頭又圓圓的，"))
obj("spoon-plate", "Close-up of " + SPOON + " lying on a round glass plate, the smooth round bowl of the spoon shining softly",
    c("通常不會冒火花；叉子就可能會。", None, "P:fork"))
chief("chief-smooth", C("drawing a big smooth curve in the air with one hand and a calm smile"),
    c("課本說，又平又圓的表面，電荷比較不會跑出去。"),
    c("還記得嗎？牆又大又平，只彈回微波，不冒火花。"))
kid("kid-spoonhot-q", K("holding " + SPOON + " up close to her face with a curious frown", close=True, where=KITCHEN),
    k("湯匙裡也有電子，不會熱嗎？", "句尾上揚", "S:spoonhot"),
    c("教授說，厚湯匙導電好，電跑過去，留下的熱很少。", None, "P:spoonhot"))
obj("wire-hot", "Close-up of " + BOX + " on a wooden counter, its thin silver wire handle glowing a faint warm orange, an illustration",
    k("那細細的鐵絲呢？", "追問"),
    c("還記得嗎？它太細，熱就留在裡面，才可能燒起來。", "接住上一句"))
kid("kid-foil-q", K("bending over a wooden counter and pointing at a crumpled ball of shiny aluminium foil lying on it, nose wrinkled in curiosity", where=KITCHEN),
    k("那皺皺的鋁箔呢？", "句尾上揚", "S:foil"))
obj("foil-two", "Wide shot of a crumpled ball of shiny aluminium foil with many little folds and corners beside a flat smooth sheet of shiny aluminium foil on a wooden counter",
    c("鋁箔，就是包東西用的薄薄的金屬片。"),
    c("一家家電公司說，薄的、皺的、邊很尖的金屬，", "接住上一句"))
chief("chief-foil", C("holding up a crumpled ball of shiny aluminium foil in one hand with a careful face", close=True),
    c("會把能量集中起來，冒出火花。", None, "P:foil"),
    c("揉皺了，就多出很多尖尖的小角。"))
kid("kid-flatfoil-q", K("holding up a flat smooth sheet of shiny aluminium foil in both hands with a hopeful face", where=KITCHEN),
    k("那平平的鋁箔就沒事？", "句尾上揚", "S:flatfoil"))
obj("foil-flat", "Close-up of a flat smooth sheet of shiny aluminium foil lying on a wooden counter, its thin straight edges catching the light",
    c("平的尖角少，可是一樣很薄，邊也可能尖尖的。", "接住上一句", "P:flatfoil"),
    c("所以平的也要照說明書用，等一下翻給你看。"))
kid("kid-gap-q", K("holding two crumpled balls of shiny foil close together in her two hands with a thinking frown", where=KITCHEN),
    k("那兩塊金屬靠在一起呢？", "句尾上揚", "S:gap"))
chief("chief-gap", C("holding her two index fingers very close together with a curious smile", close=True),
    c("課本還說了一件事：兩塊金屬中間的縫越窄，", "接住上一句"),
    c("電就越容易跳過去。看這兩個水盤："))
obj("tray-gap", "Close-up of two shallow clear plastic trays of blue water set end to end with only a very thin gap between them on a kitchen counter, a small splash of water leaping across the thin gap",
    k("水就濺過去了！", "驚訝"),
    c("所以金屬碰到牆、或靠得很近，也比較容易冒火花。", None, "P:gap"))
kid("kid-try", K("bouncing on her toes with an excited grin, holding up " + FORK, where=KITCHEN),
    k("我拿叉子試試看！", "興奮"))
chief("chief-no-try", C("holding up one hand like a gentle stop with a kind but firm smile", close=True),
    c("不行喔。火花會燒焦東西，還可能弄壞微波爐。", "認真"),
    k("那鐵架怎麼可以？", "追問"))

# ---------- 第四章：翻開微波爐的說明書 ----------
chief("chief-manual", C("holding a thin closed grey booklet with a plain cover in both hands with a warm smile"),
    c("因為做這種爐子的公司，把架子設計好，", "接住上一句"),
    c("也把用法寫在說明書裡。"), chapter="翻開微波爐的說明書")
chief("chief-ge", C("opening a thin grey booklet and reading it with a focused smile", close=True),
    c("像這本，是GE一款微波爐的說明書。"),
    c("它附的金屬架，是給大盤子、或兩層一起熱用的。", None, "P:rack"))
obj("rack-inside", "Close-up of " + OPEN + ", " + RACK + " standing neatly in the middle with a clear gap all around it",
    c("說明書還提醒：架子要放對位置，別碰到牆。"),
    c("就是剛剛說的：金屬碰到牆，比較容易冒火花。"))
chief("chief-touch", C("holding her two flat hands a little apart with a careful smile", close=True),
    c("那家家電公司也說，金屬別碰到別的金屬。"))
kid("kid-allrack-q", K("pointing at a metal wire rack with a curious face", close=True, where=KITCHEN),
    k("那每台的架子，", "追問"), k("都能拿來微波嗎？", "句尾上揚", "S:allrack"))
chief("chief-amana", C("shaking her head gently with a careful smile"),
    c("不一定。另一家廠商說，它有些機型附的架子，", "接住上一句"),
    c("只能用在烤箱的功能；微波時放進去，可能冒火花。", None, "P:allrack"))
kid("kid-whose", K("holding her chin with a thinking face", close=True, where=KITCHEN),
    c("食藥署也說，每台微波爐的說明，"))
chief("chief-fda-manual", C("tapping a thin grey booklet with one finger and a warm smile"),
    c("上面寫著可以用哪些容器。"),
    c("它還說，一般不要放金屬鍋子或鋁箔。"))
obj("food-uneven", "Close-up of a plain white bowl of " + FOOD + " half covered by a shiny metal pot lid, the uncovered half steaming and the covered half pale",
    c("因為微波被彈開，飯會熱得不平均。"),
    k("那鋁箔一點都不能用？", "句尾上揚", "S:foilok"))
chief("chief-foil-rule", C("holding up one thin narrow strip of smooth shiny foil with a careful smile", close=True),
    c("這本說明書說，只能照它寫的方法用："),
    c("小小一條，蓋住雞翅尖那種很薄、容易過熟的地方。"))
obj("foil-wing", "Close-up of one roast chicken wing on a plain white plate, only its thin tip wrapped snugly in a small smooth strip of shiny foil",
    c("鋁箔要貼緊食物；翹起來的邊，就像叉子的尖端。"),
    c("還要離爐子的牆，至少一英寸，大約兩公分半。", None, "P:foilok"))
chief("chief-your-home", C("holding the thin grey booklet up beside her face with a kind smile", close=True),
    c("這是這一台的規則；你家那台，要看你家的說明書。", "轉向觀眾"))
kid("kid-box-again", K("holding up " + BOXK + " by its thin wire handle with a hopeful face", where=KITCHEN),
    k("那我的便當盒呢？", "句尾上揚"))
chief("chief-handle", C("pointing at a thin grey booklet with a bright smile"),
    c("說明書寫著：紙盒、塑膠盒上的鐵絲和金屬提把，"),
    c("放進去之前，要先拿掉。", None, "P:handle"))
kid("kid-gold-q", K("looking up with a thinking face, one finger on her chin", close=True, where=KITCHEN),
    k("阿嬤家的金邊碗可以嗎？", "句尾上揚", "S:gold"))
obj("gold-bowl", "Close-up of " + GOLD + " on a wooden counter, the thin gold line shining",
    c("說明書把金邊的碗，也列在會冒火花的東西裡。", "接住上一句", "P:gold"),
    c("沒有金屬邊、也沒有金屬光澤的陶瓷碗，大多可以用。"))
chief("chief-towel", C("holding up a folded soft grey kitchen towel sheet with a surprised smile", close=True),
    k("還有看不出來的金屬嗎？", "句尾上揚", "S:hidden"),
    c("有。說明書說，回收紙做的紙巾，", "接住上一句"),
    c("可能藏著小小的金屬碎片，也會冒火花。", None, "P:hidden"))
kid("kid-dirty-q", K("peeking into an open microwave oven with a curious frown", where=KITCHEN),
    k("爐子裡髒髒的也會嗎？", "句尾上揚", "S:dirty"))
obj("oven-clean", "Close-up of " + OPEN + ", a soft yellow sponge wiping one smooth wall clean, a small bowl of soapy water beside the oven",
    c("剛剛那家廠商也說，牆上卡的髒東西，可能冒火花。", "接住上一句", "P:dirty"),
    c("食藥署建議，用水和溫和的清潔劑，常常擦乾淨。"))
# 2026-11-14 added segment (body back over 8 minutes with real content, claims.md C22): running the oven empty.
# FDA's tip list puts "some ovens should not be operated when empty" right after the cleaning tip; Bloomfield
# says why (nothing absorbs the microwaves, they build up and flow back to the magnetron). Calls back C01/C02/C03.
obj("oven-empty", "Close-up of " + OPEN + ", the round glass turntable plate bare and empty in the middle, the clean shiny walls all around it",
    k("那爐子空空的，按下去呢？", "句尾上揚", "S:empty"),
    c("食藥署也說，有些微波爐不能空著開，", "接住上一句"),
    c("要看那一台的說明書。你猜為什麼？", "轉向觀眾"))
obj("empty-bounce", "Close-up looking into " + OPEN + ", the bare glass turntable plate in the middle, soft wavy pale-blue ripples drifting between the shiny metal walls, an illustration",
    c("還記得嗎？微波在牆之間來回跑，"),
    c("本來會被飯裡的水吸收掉。"),
    c("空空的，微波就在裡面越積越多。"))
obj("magnetron-glow", "Cutaway side view of a plain white cartoon microwave oven with its right side panel removed, showing inside the casing a chunky silver cylinder with cooling fins mounted beside the bare cooking chamber, the cylinder glowing a faint warm orange, soft wavy pale-blue ripples crowding the chamber around it, three round plain knobs on the front, warm cream background, an illustration",
    c("物理學教授說，多到最後，微波會倒流回去，"),
    c("跑回做出微波的那個磁控管，"),
    c("可能把它弄壞。", None, "P:empty"))
obj("empty-bowl", "Close-up of " + BOWL + ", empty and dry, sitting alone on the round glass turntable plate inside " + OVEN + " standing open",
    c("只放一個乾乾的空碗，也跟空著差不多。"),
    c("因為陶瓷碗會讓微波穿過去，不會吸收。"))
obj("chief-empty", "Close-up of a plain white cartoon microwave oven with its door wide open, a bowl of braised pork rice sitting on the glass turntable inside, warm light glowing in the chamber, a light wooden kitchen counter",
    c("所以那位教授說，別讓微波爐空著開超過一兩秒。"),
    c("按開始之前，先看看裡面有沒有放食物。"))
kid("kid-spark-q", K("hugging " + BOWL + " to her chest with a worried face", where=KITCHEN),
    k("要是真的冒火花了呢？", "擔心", "S:spark"))
chief("chief-spark", C("pressing one big round plain button on the front of a white microwave oven with a calm face"),
    c("說明書說：先按停止，再把出問題的東西處理好。", None, "P:spark"),
    k("怎麼處理？", "追問"))
obj("oven-fixed", "Close-up of " + OPEN + ", " + RACK + " standing neatly in the middle with a clear gap all around it, a small white takeaway box set aside on the counter beside the oven",
    c("請大人來：拿掉鐵絲、架子放正、鋁箔貼緊。"),
    c("那家廠商也說，馬上停下來，通常不會弄壞爐子。"))
chief("chief-fire", C("holding up one open hand firmly with a serious caring face"),
    c("要是燒起來了，門別打開，先按停止，叫大人。"))
kid("kid-rice-q", K("holding " + BOXK + " up with a hungry pleading face", close=True, where=KITCHEN),
    k("那我的滷肉飯，現在怎麼辦？", "章尾停住，句尾上揚"))

# ---------- 收尾 ----------
obj("rice-pour", "Close-up of " + FOOD + " in " + BOWL + " sitting on the glass turntable plate inside " + OVEN + ", the empty white takeaway box with its wire handle set aside on the counter",
    c("倒進這個白碗，鐵絲盒放旁邊，就可以熱了。", "接住上一句"),
    c("你說呢？什麼時候會冒火花？", "笑"), chapter="滷肉飯熱好了，小問想通了")
kid("kid-got-it", K("holding " + BOWL + " of steaming rice up with a big confident grin", where=KITCHEN),
    k("原來如此！", "恍然大悟"), k("剛剛那些尖尖的、皺皺的，", "篤定"),
    k("還有靠得很近的金屬，", "篤定"), k("電子擠在一起，", "篤定"),
    k("就可能跳出火花！", "篤定", "P:main"))
chief("chief-opinion", C("smiling with her hands clasped, a thoughtful look", close=True),
    c("說得好。我覺得最妙的是：", "笑"),
    c("剛剛那又大又平的金屬牆和網子，正好把微波關在裡面。"))
# The outro is three pictures, no card, no stamp (series README §3.2, §10.1): the kid gives a thumbs-up.
kid("outro", "Waist-up medium shot of the girl with a big happy smile giving a big cheerful thumbs-up with one hand, bright morning light",
    k("我要叫阿嬤先拔掉鐵絲！", "開心大聲"))
chief("outro-chief", "Waist-up medium shot of the chief holding up a plain white ceramic rice bowl with a curious smile, filling the frame, a plain pale wall behind her, bright morning light",
      c("你家的微波爐裡，有沒有附一個架子？", "問句上揚，像聊天"), c("留言告訴我們。"))
chief("outro-wave", "Waist-up medium shot of the chief waving goodbye with a warm smile, a plain pale wall behind her, bright morning light",
      c("想一起找生活裡的為什麼，就訂閱原來如此事務所。", "誠懇"))

# ---------- assemble ----------
WHAT = {"handle": "便當盒的鐵絲提把放進去會怎樣", "rack": "微波爐裡本來就有金屬架，為什麼可以",
        "mesh": "門上一格一格的網子是什麼做的", "fork": "叉子和湯匙哪一支比較會冒火花",
        "main": "同樣是金屬，為什麼有的冒火花有的不會", "more": "是不是金屬越多火花越大",
        "hole": "網子有洞，微波會不會跑出來", "door": "門壞掉了怎麼辦",
        "bounce": "金屬怎麼把微波彈回來", "heat": "彈來彈去的微波怎麼把飯變熱",
        "bowl": "碗會不會被微波加熱",
        "wire": "鐵絲也會被推著晃嗎", "crowd": "電子擠成一堆會怎樣",
        "foil": "皺皺的鋁箔會怎樣", "gold": "只有一圈金邊的碗會不會冒火花",
        "allrack": "每台微波爐的架子都能拿來微波嗎", "foilok": "鋁箔是不是一點都不能用",
        "spark": "真的冒火花了怎麼辦", "prongs": "叉子有四個尖頭會怎樣",
        "flatfoil": "平平的鋁箔是不是就沒事", "hidden": "還有沒有看不出來的金屬",
        "dirty": "爐子裡髒髒的會不會冒火花", "meshbounce": "有洞的網子也能把微波彈回去嗎",
        "spoonhot": "湯匙裡也有電子在跑，不會熱起來嗎", "gap": "兩塊金屬靠在一起會怎樣",
        "empty": "微波爐空空的按下去會怎樣"}
# Latin terms the Mandarin voice must spell letter by letter (P13 GPS, P29 HTTPS/TLS). The one named manual is
# GE's; the brand is said in English as its two letters (series README §3.1: brand names in the original).
# The other brand (Amana, a Whirlpool brand, claims.md C17) is not named aloud.
SAY = [("GE", "G E")]
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
        assert not re.search(r"[A-Za-z]{2,}", spoken), (lid, "a Latin term needs a SAY entry (spelled letter by letter)")
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
    "series": {"slug": "sothatswhy", "episode": 20, "chapter": 1},
    # 2026-11-11 (README §9 停頓, §10.6): no fixed pause between lines, a short gap between scenes, beat-timed stills.
    "pauses": {"line_ms": 0, "scene_ms": 150},
    "still_motion": "beat",
    # The series bed from P15 on (explainer-series/README.md, PR #2048): sothatswhy-bed-r2.m4a, remade from P02's paid take.
    "music": {"track": "sothatswhy-bed-r2.m4a", "sha256": "9bb4ba6fd16feb4a7f352144b2d89e9648acbbbbaa2173c27a7eefbdb70f28c6", "gain_db": -20, "duck_db": -10},
    "characters": CHARACTERS, "loops": loops,
    "youtube": {
        "category_id": 27, "made_for_kids": False, "default_language": "zh-TW",
        "title": "微波爐遇到金屬，什麼時候會冒火花？｜原來如此事務所",
        "description": "小問帶著阿嬤做的滷肉飯來事務所，便當盒上有一條細細的鐵絲提把，她正要放進微波爐，所長叫她先別按。可是微波爐裡本來就有一個金屬架，門上的網子是金屬，裡面的牆也是金屬。同樣是金屬，為什麼有的會冒火花，有的不會？\n\n"
                       "這一集，所長拿一盤水左右晃給小問看，從微波爐的牆、門上有洞的網子，一路比到叉子、湯匙、皺皺的鋁箔和阿嬤的金邊碗，找出它們到底差在哪裡。"
                       "最後他們翻開一台微波爐的說明書，看看哪些東西放進去之前要先拿掉，真的冒火花了又該怎麼辦。\n\n"
                       "片中的微波爐、叉子、鋁箔、碗和火花都是 AI 生成的示意插圖，不是實驗的照片。請不要把金屬放進微波爐試火花；你家的微波爐怎麼用，請照那一台的說明書。每個說法的出處列在下方參考資料。\n\n資料截至 " + CHECKED,
        "tags": ["微波爐", "金屬", "火花", "鋁箔", "電子", "電荷", "說明書", "科普", "原來如此事務所"]},
    "thumbnail": {"template": "thumb", "data": {"headline": "微波爐\n**冒火花？**", "sub": "同樣是金屬，差在哪？", "shot": "kid-main-q", "subject": "right"}},
    "sources": [
        {"title": "U.S. Food and Drug Administration, Microwave Ovens", "url": "https://www.fda.gov/radiation-emitting-products/resources-you-radiation-emitting-products/microwave-ovens", "checked_on": CHECKED},
        {"title": "Louis A. Bloomfield, How Everything Works: Why do metal objects spark/arc in the microwave? (1997-01-17)", "url": "https://howeverythingworks.org/1997/01/17/question-759/", "checked_on": CHECKED},
        {"title": "Louis A. Bloomfield, How Everything Works: If a microwave oven door reflects microwaves, why doesn't everything? (2009-03-31)", "url": "https://howeverythingworks.org/2009/03/31/question-1579/", "checked_on": CHECKED},
        {"title": "Louis A. Bloomfield, How Everything Works: What happens if you start the microwave oven with nothing inside?", "url": "https://howeverythingworks.org/1969/12/31/question-326/", "checked_on": "2026-11-14"},
        {"title": "Louis A. Bloomfield, How Everything Works: Why are you required to have an item in the microwave oven while it is operating? (1996-09-25)", "url": "https://howeverythingworks.org/1996/09/25/question-483/", "checked_on": "2026-11-14"},
        {"title": "OpenStax, College Physics 2e, 18.7 Conductors and Electric Fields in Static Equilibrium", "url": "https://openstax.org/books/college-physics-2e/pages/18-7-conductors-and-electric-fields-in-static-equilibrium", "checked_on": CHECKED},
        {"title": "OpenStax, College Physics 2e, 19.2 Electric Potential in a Uniform Electric Field", "url": "https://openstax.org/books/college-physics-2e/pages/19-2-electric-potential-in-a-uniform-electric-field", "checked_on": CHECKED},
        {"title": "GE Appliances, Spacemaker XL Microwave Oven JVM1542 Owner's Manual (49-40264)", "url": "https://products-salsify.geappliances.com/image/upload/s--BEQq86so--/3842e17e8541177381e364fb66ab5c46460333f5.pdf", "checked_on": CHECKED},
        {"title": "Amana Product Help, General Arcing and Sparking - Over-the-Range Microwave", "url": "https://producthelp.amana.com/Cooking/Microwaves/Over-the-Range_Microwave/General_Arcing_and_Sparking/General_Arcing_and_Sparking_-_Over-the-Range_Microwave", "checked_on": CHECKED},
        {"title": "JennAir Product Help, Can Metal or Aluminum Foil be Used in the Microwave", "url": "https://producthelp.jennair.com/Cooking/Microwaves/Product_Info_new/Product_Information/Can_Metal_or_Aluminum_Foil_be_Used_in_the_Microwave", "checked_on": CHECKED},
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
assert len(loops) >= 11, "the plan asks for at least 11 loops, every one paid off"
assert body_chars <= 3000, f"body {body_chars} characters: keep under 3,000"
assert all(s["data"]["camera"] for s in scenes)
cams = [s["data"]["camera"] for s in scenes]
assert all(not (a == b == c_) for a, b, c_ in zip(cams, cams[1:], cams[2:])), "three shots in a row with the same camera"
