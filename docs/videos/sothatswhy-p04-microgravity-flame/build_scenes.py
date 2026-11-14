"""Generate video.json for sothatswhy-p04-microgravity-flame (原來如此事務所 對話版 P04).

Run `python3 build_scenes.py` from anywhere: it rewrites video.json next to this file and freezes
every shot's camera move in cameras.json (a shot keeps the camera it was first given, so deleting
a shot never shifts the others: the camera is in the keyframe cache key).
Edit lines and prompts here, never in video.json.
Started from a copy of sothatswhy-p13-gps-timing/build_scenes.py (series constants, helpers,
assembly and self-checks unchanged; EXTRA and REWRITE start empty because P13's entries were picture
fixes for P13 only; the SAY list for Latin terms is P29's); the content is new.
2026-11-11 rules applied (dialogue-pilot README §4, §9, §10.6): the faster voice style for both characters,
`pauses: {line_ms: 0, scene_ms: 150}` and `still_motion: "beat"`, no `pause_after_ms` on lines except a
BEAT_MS beat on the line right before each `P:` payoff in the same scene, and only an upper bound on length.
Shot pacing (P21 storyboard score: median 3.9 s a picture against the series' 6-12 s): a short reaction line
gets its own shot only when the picture changes something, so most shots carry two to four lines.
2026-11-13 rules (README §2, §10.6; lessons/sothatswhy.md 一般觀眾視角檢討): 小問's share cut from 24.6% to about 19%
of the Han characters by deleting her pure reactions and shortening her lead-in lines (no loop tag moved), the opening
greeting dropped so the round-versus-pointed flame question lands in the first lines, and the thumbnail sub and the
description's first two lines pose the contradiction instead of the cause. Scenes and prompts unchanged.
2026-11-14: the cut left the measured body at 451.2 s, under the 480 s floor; the owner chose real content over padding,
so five new shots (chief-putout … chief-earth-safe, loop `putout`) answer "how do you put out a fire on the station?"
from NASA's combustion and fire-safety page (claims.md C26), between the 1992 candle and the chapter-end hook.
`script.md` is written by `node tools/video/cli.mjs script --slug sothatswhy-p04-microgravity-flame` after this runs.
"""
import hashlib, itertools, json, os, re, sys, unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = "sothatswhy-p04-microgravity-flame"
CHECKED = "2026-11-12"
BEAT_MS = 500   # 答案揭曉前的一拍；第一集照這個試，成片量過再調（README §10.6）

# ---------- series constants ----------
# Both characters are identical to P06/P07/P14/P08/P21/P13/P29 (approved series sheets reused through the `series` tag):
# the chief as in P02/P05/P14, the kid in her notebook-free look (series README §3.2).
# Voice styles: the 2026-11-11 faster style (README §4): only the last sentence changes.
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
EXTRA = {  # storyboard score R1 (47/70): off-model faces
    "chief-ladder": ", cute chibi cartoon proportions with a big round head exactly like her reference sheet, simple cartoon eyes behind round black glasses, solid jet-black hair, small round ears",
    "chief-apple": ", cute chibi cartoon proportions with a big round head exactly like her reference sheet, simple cartoon eyes behind round black glasses, solid jet-black hair, small round ears",
    "chief-same-speed": ", cute chibi cartoon proportions with a big round head exactly like her reference sheet, simple cartoon eyes behind round black glasses, solid jet-black hair, small round ears",
    "chief-safe": ", cute chibi cartoon proportions with a big round head exactly like her reference sheet, simple cartoon eyes behind round black glasses, solid jet-black hair, small round ears",
    "chief-cold": ", cute chibi cartoon proportions with a big round head exactly like her reference sheet, simple cartoon eyes behind round black glasses, solid jet-black hair, small round ears",
    "chief-why": ", cute chibi cartoon proportions with a big round head exactly like her reference sheet, simple cartoon eyes behind round black glasses, solid jet-black hair, small round ears",
    "chief-gas": ", cute chibi cartoon proportions with a big round head exactly like her reference sheet, simple cartoon eyes behind round black glasses, solid jet-black hair, small round ears",
    "chief-listen": ", cute chibi cartoon proportions with a big round head exactly like her reference sheet, simple cartoon eyes behind round black glasses, solid jet-black hair, small round ears",
    "chief-opinion": ", cute chibi cartoon proportions with a big round head exactly like her reference sheet, simple cartoon eyes behind round black glasses, solid jet-black hair, small round ears",
    "outro-wave": ", cute chibi cartoon proportions with a big round head exactly like her reference sheet, simple cartoon eyes behind round black glasses, solid jet-black hair, small round ears",
    "chief-zero-q": ", cute chibi cartoon proportions with a big round head exactly like her reference sheet, simple cartoon eyes behind round black glasses, solid jet-black hair, small round ears",
    "kid-try-fire": ", cute chibi cartoon proportions with a big round head, a small girl of eight",
    "kid-out-q": ", cute chibi cartoon proportions with a big round head, a small girl of eight",
    "kid-final-q": ", cute chibi cartoon proportions with a big round head, a small girl of eight",
    "kid-done": ", cute chibi cartoon proportions with a big round head, a small girl of eight",
}
# Whole-prompt rewrites after a visual review. Empty until this episode's keyframes are drawn and checked.
REWRITE = {  # zoom check R1 (2026-11-12): no take usable
    "cloth-flame": "Close-up through a round porthole window into a small grey metal test chamber, one long flat strip of pale cream cloth stretched in a thin metal frame across the middle, a small soft blue flame with an orange tip burning on the left end of the cloth and slowly creeping right, the burnt part behind it dark grey, the rest of the cloth clean and pale, simple flat 2D cel-shaded cartoon drawing with clean ink outlines and flat colours",
    "drop-glow": "Close-up of a dim round metal chamber seen through a round window, floating alone in the middle one tiny shiny amber drop wrapped in a perfectly round soft blue ball of flame like a marble, the ball smooth and round on every side, clean empty corners, simple flat 2D cel-shaded cartoon drawing with clean ink outlines and flat colours",
    "chief-gas": "Head-and-shoulders close-up of the chief holding up one index finger beside her face with a careful smile, smooth plain forehead, the chief is a cute chibi cartoon woman with a big round head, glossy solid jet-black hair tied in one low ponytail, big round thick black glasses, simple dot-like cartoon eyes, a small smile, a yellow pencil tucked behind one ear, a mustard-yellow cardigan over a white blouse, plain bare ears, a plain pale cream wall behind her, bright daylight, exactly like her reference sheet, simple flat 2D cel-shaded cartoon drawing with clean ink outlines and flat colours",
    "chief-apple": "Head-and-shoulders close-up of the chief holding one shiny red cartoon apple in her open palm at chest height with a gentle smile, the chief is a cute chibi cartoon woman with a big round head, glossy solid jet-black hair tied in one low ponytail, big round thick black glasses, simple dot-like cartoon eyes, a small smile, a yellow pencil tucked behind one ear, a mustard-yellow cardigan over a white blouse, plain bare ears, a plain pale cream wall behind her, bright daylight, exactly like her reference sheet, simple flat 2D cel-shaded cartoon drawing with clean ink outlines and flat colours",
    "drop-small": "Close-up of one very tiny round dull dark amber drop, the size of a pinhead, floating alone in the middle of a dark round metal chamber seen through a round porthole, the drop dim and matte, the whole chamber dark, still and quiet, deep shadowy grey tones, simple flat 2D cel-shaded cartoon drawing with clean ink outlines and flat colours",
    "drop-dark": "Close-up of one small round dull dark amber drop floating alone in the middle of a dark round metal chamber seen through a round porthole, the drop dim and matte with only a faint wavy shimmer of warm air around it, the whole chamber dark and quiet, deep shadowy grey tones, simple flat 2D cel-shaded cartoon drawing with clean ink outlines and flat colours",
    "deep-shaft": "Side view cutaway of a tall deep grey shaft dug into the ground, the walls two tall grey stripes with dark shadow between them, halfway down one small white cartoon candle falling straight down with short white speed lines above it, the candle with a small perfectly round soft blue ball of flame sitting around its wick like a marble, the ball smooth and round on every side, a plain pale cream wall behind, clean empty corners, simple flat 2D cel-shaded cartoon drawing with clean ink outlines and flat colours",
    "tablet-flame": "Close-up of a child's two small hands in navy blue raincoat sleeves holding a small white tablet in front of a plain pale cream wall. On the tablet: a tiny cartoon astronaut in a white spacesuit floating inside a white space cabin with one round window, and beside the astronaut a small round glowing blue ball of flame the size of a cherry, perfectly round like a blue marble, hovering in mid-air with a soft blue rim. Bright cheerful colours, simple flat 2D cel-shaded cartoon drawing with clean ink outlines and flat colours",
    "cup-fly": "Wide shot of a sunny back yard with a big blue plastic basin on green grass, high above the basin one small white plastic cup flying through the air in a gentle arc, the cup perfectly upright with its open top facing up, the cup filled to the brim with calm blue water, the water staying completely inside the cup with a smooth level surface, the outside of the cup dry and clean, one tiny dark dot of a hole near the bottom of the cup side with the water held still behind it, the clear air around the cup empty, three short curved motion lines trailing behind the cup, bright clear daylight, simple flat 2D cel-shaded cartoon drawing with clean ink outlines and flat colours",
    "scale-cabin": "Wide shot inside a cartoon space station cabin with soft white padded walls, grey handrails and one round window showing the blue planet and black starry space, a friendly generic astronaut in a plain white spacesuit with a clear round helmet floating with both boots resting on a flat square pale blue bathroom scale that floats in mid-air with them, the scale's round dial facing the viewer with its single red needle pointing straight up at the starting mark, simple flat 2D cel-shaded cartoon drawing with clean ink outlines and flat colours",
    "ball-curve": "Wide view from space of a big round blue and green planet in the middle of the frame with deep dark blue space all around, one small dark grey ball near the top of the planet, a thin white dotted trail running from the ball all the way around the planet in a full circle like a ring, the ring the same small distance from the planet everywhere, a few small white stars, simple flat 2D cel-shaded cartoon drawing with clean ink outlines and flat colours",
    "chief-plane": "Waist-up medium shot of the chief holding a small plain white plastic cup up in one hand and tracing a big gentle hump in the air with the index finger of her other hand, a bright cheerful smile, a plain pale wall behind her, bright daylight, the chief is a middle-aged woman with round black glasses, dark hair with one grey streak tied in a low ponytail, a yellow pencil tucked behind one ear, a mustard-yellow cardigan over a white blouse and navy trousers, simple flat 2D cel-shaded cartoon drawing with clean ink outlines and flat colours",
    "candle-base": "Close-up of a short white candle on a small round wooden saucer on a wooden table, a small orange teardrop flame on the wick, two smooth wide pale blue bands of breeze gliding in low along the tabletop, one from the left and one from the right, each band a soft flat ribbon shape that bends upward at its tip and meets right under the flame at the base of the wick, a plain pale cream wall behind, simple flat 2D cel-shaded cartoon drawing with clean ink outlines and flat colours",
    "round-flame": "Close-up of one short white candle on a small round wooden saucer on a wooden table, the candle with a small perfectly round soft blue ball of flame sitting around its wick like a marble, the ball smooth and round on every side, pale blue at its rim and deeper blue in the middle, a plain pale cream wall behind, clean empty corners, simple flat 2D cel-shaded cartoon drawing with clean ink outlines and flat colours",
    "cabin-flame": "Close-up of one clear round glass globe held by a short grey metal bracket from a soft white padded space station wall, one round porthole behind it showing black starry space and a curve of the blue Earth, inside the globe a tiny short white candle, sitting on the top of its black wick one perfectly round soft blue ball the size of a blueberry, a full smooth circle like a blue marble, pale sky blue at its rim and deeper blue in the middle, the globe filling the middle of the frame, bright even light, simple flat 2D cel-shaded cartoon drawing with clean ink outlines and flat colours",
    "candle-pair": "Wide shot of two short white candles side by side on a wooden table, the left candle with a tall orange-yellow teardrop flame pointing straight up, the right candle with a small perfectly round soft blue ball of flame sitting around its wick like a marble, the two flames clearly different in shape, a plain pale cream wall behind, clean empty corners, simple flat 2D cel-shaded cartoon drawing with clean ink outlines and flat colours",
    "half-ball": "Close-up of a single short white candle on a small round wooden saucer, above the wick a small soft blue dome shaped like half of a blueberry cut across, round on top and flat along its lower edge, hovering just above the candle top with a clear thin gap of cream background between the flat lower edge and the wax, the short dark wick reaching up into the dome, pale blue at the rim and deeper blue inside, a plain flat pale cream wall behind, simple flat 2D cel-shaded cartoon drawing with clean ink outlines and flat colours",
    "kid-same-q": "Waist-up medium shot of a little 8-year-old girl in a sunny back yard beside a big blue plastic basin on the grass, holding a small grey tablet in both hands with its plain grey back towards the viewer, head tilted with a thinking face and eyes looking up, bright daylight, she has a short black bob with straight blunt bangs, one small thin cowlick strand on top and simple dot eyes, and wears a closed navy raincoat jacket with toggles and a mustard-yellow hood resting on her shoulders, painted grass and fence behind her, simple flat 2D cel-shaded cartoon drawing with clean ink outlines and flat colours",
    "drop-pop": "Close-up view through a round porthole into a dim round metal test chamber with dark blue-grey walls, in the middle one tiny shiny amber droplet shaped like a perfect little sphere floating weightless in mid-air, wrapped in a round bright orange ball of flame, the droplet bursting apart with a pop right where it floats, four even tinier round amber droplets flying outward from it in four directions, a small yellow starburst around the droplet itself, the chamber floor far below and empty, simple flat 2D cel-shaded cartoon drawing with clean ink outlines and flat colours",
    "kid-depends": "Head-and-shoulders close-up of a little 8-year-old girl in a sunny back yard with a big blue plastic basin on the grass behind her, clapping her two open hands together in front of her chest with a bright open-mouthed realising grin, bright daylight, she has a short black bob with straight blunt bangs, one small thin cowlick strand on top and simple dot eyes, and wears a closed navy raincoat jacket with toggles and a mustard-yellow hood on her shoulders, painted flat grass and fence in the background, simple flat 2D cel-shaded cartoon drawing with clean ink outlines and flat colours",
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

# One drawing language for the whole episode (README §10.5, P17/P18: the image model cannot draw orbits,
# diagrams, labels, arrows, counts or directions). The main thread is ONE afternoon: 小問 comes to the office
# after a school video showed astronauts floating and a small round flame; the chief takes her to the back yard
# with a cup that has a small hole in it. The one analogy carried from start to end is THE LEAKY CUP
# (NASA's 1997 teacher's guide, activity "Can Throw"): held still, water runs out of the hole; tossed, the water
# stays in for the whole flight, because cup and water fall together. Chapter 1: gravity is still there, the
# cup and water are both falling (station, astronaut, apple). Chapter 2: toss it faster and it lands farther,
# Newton's cannon, orbit. Chapter 3: on the ground the heavier cold air pushes down under the flame the way the
# heavier water pushes out of the hole; when everything falls together neither pushes, so the flame is no longer
# drawn into a tip. Chapter 4: with that push gone, a flame shows things the ground hides (cool flames), and the
# gas around it still decides the ending. Every frame is an everyday object at human scale or a simple cartoon
# interior; space is never drawn photo-like, no real experiment hardware is copied, and every flame or droplet
# picture is an illustration (the description says so).
OFFICE = "in a bright simple cartoon room with a plain pale cream wall,"
YARD = "in a sunny back yard beside a big blue plastic basin on the grass,"
STYLE = ", simple flat 2D cel-shaded cartoon drawing with clean ink outlines and flat colours"
CUP = "a small plain white plastic cup with one tiny round hole near its bottom"
BASIN = "a big blue plastic basin on green grass"
TABLET = "a small tablet showing a simple cartoon of a tiny round blue flame floating inside a white space cabin"
STATION = "one simple cute cartoon space station with wide golden solar panels"
EARTH = "a big round blue and green planet curve at the bottom of the frame, deep blue space above"
CABIN = "inside a simple cartoon space station cabin with soft white padded walls, round windows and handrails"
CANDLE = "a single short white candle on a small wooden saucer"
DROP = "one tiny shiny round drop of amber liquid floating alone in the middle of a dim round metal chamber seen through a round window"
def obj(id, prompt, *lines, chapter=None):
    """An everyday-object frame with nobody in it, always in the flat cartoon style (P18: object
    prompts without style words came out as photos)."""
    scene(id, prompt + STYLE + ", clean empty corners", *lines, chapter=chapter)

# ---------- 開場（系列片頭之後直接進場景，不做濃縮；答案都不先講）----------
obj("tablet-flame", "Close-up of a child's two small hands holding " + TABLET + ", a plain pale cream wall behind",
    k("太空人飄來飄去！", "興奮"), chapter="影片裡，火圓圓的")
# Thumbnail shot (fixed before keyframes, explainer-series/README.md): the kid big and centred, the tablet in hand.
kid("kid-main-q", K("holding a small tablet up in front of her chest with both hands and looking at the viewer with wide amazed eyes, in the exact centre of the picture", where=OFFICE),
    k("旁邊有一團小火，", "比手畫腳"), k("圓圓的，像一顆球！", None, "S:round"))
chief("chief-listen", C("leaning forward with a curious smile, one hand on her chin", close=True),
    c("跟家裡蠟燭的火，不太一樣吧？", "接住上一句"),
    k("蠟燭的火是尖尖的！"))
kid("kid-guess", K("raising one finger with a very confident grin", where=OFFICE),
    k("一定是太空沒有重力！", "篤定的錯猜", "S:nograv"))
chief("chief-tease", C("holding up one finger with a playful knowing smile"),
    c("很多人都這樣猜。可是我跟你說，", "賣關子"),
    c("那些太空人，其實一直在往下掉。", "放慢", "S:falling"))
chief("chief-hooks", C("counting on her fingers with a playful mysterious smile"),
    c("等一下你會看到，一根點著的蠟燭，掉進一口很深的井。", None, "S:well"),
    c("還有一團火熄了以後，儀器卻量到一件怪事。", "賣關子", "S:ghost"))
chief("chief-promise", C("tilting her head with an inviting smile, one open hand towards the viewer", close=True),
    c("你也猜猜看：人一直在掉，火為什麼也跟著變了？", "轉向觀眾", "S:main"))
kid("kid-not-falling", K("crossing her arms with a doubtful pout", where=OFFICE),
    k("他們明明是飄著的！", "不服氣"))

# ---------- 第一章：破洞的杯子一拋，水不漏了 ----------
chief("chief-cup", C("holding up " + CUP + " with a cheerful smile"),
    c("飄著跟往下掉，可以同時發生。", "接住上一句"),
    c("我們到後院，拿這個杯子試試。它底下有一個小洞。"), chapter="破洞的杯子一拋，水不漏了")
obj("cup-leak", "Close-up of " + CUP + " full of water held above " + BASIN + ", one thin stream of water pouring from the tiny hole into the basin, sunny back yard",
    c("裝滿水拿著，水就從小洞一直流出來。"))
chief("chief-toss", C("holding the small white cup in one hand as if about to toss it gently, a playful smile"),
    c("現在，我把這杯水，輕輕拋進大水盆裡。"),
    k("那一路上，水都會灑出來吧？", "篤定的錯猜", "S:leak"))
obj("cup-fly", "Wide shot of " + CUP + " full of water flying through the air in a gentle curve over " + BASIN + ", the water staying inside the cup, sunny back yard",
    c("你仔細看。杯子在空中的時候，小洞不漏水。", None, "P:leak"))
kid("kid-gone-q", K("scratching her head with a puzzled frown", where=YARD),
    k("是不是一拋出去，", "猜"), k("重力就不見了？", "句尾上揚", "S:gone"))
chief("chief-guide", C("holding the small white cup up beside her face with a knowing smile", close=True),
    c("沒有不見喔。重力還在，杯子和水一起往下掉。", "接住上一句", "P:gone"))
obj("cup-drip", "Close-up of " + CUP + " in mid-air above " + BASIN + ", the water inside calm and still, the tiny hole dry, sunny back yard",
    c("水跟杯子掉得一樣快，就不會從小洞擠出去。"),
    k("太空站裡也是這樣？", "追問"))
obj("ladder-sky", "Wide shot of a very tall wooden ladder rising from a green hill up through white clouds into a deep blue sky, " + STATION + " small and far away at the top",
    c("對。美國太空總署說，在太空站那個高度，", "接住上一句"),
    c("地球的重力，還有地面的九成左右。", "數字放慢", "P:nograv"))
chief("chief-ladder", C("holding one hand high above her head as if at the top of a ladder, a bright amazed smile"),
    c("要是有一把梯子通到那裡，在地上量體重是一百，"),
    c("爬到梯子頂端，還有九十左右。"))
kid("kid-float-q", K("puffing out her cheeks with a confused face, both palms up", close=True, where=YARD),
    k("怎麼會飄起來？", "句尾上揚", "S:float"))
obj("apple-cabin", "Wide shot " + CABIN + ", one shiny red apple floating in the middle of the cabin, soft daylight from the round windows",
    c("還記得我說太空人一直在掉嗎？整座太空站都在掉。", "接住上一句", "P:falling"),
    c("太空人放開一顆蘋果，蘋果也在掉，"))
chief("chief-apple", C("holding a shiny red apple in her open palm with a gentle smile", close=True),
    c("只是人、蘋果、太空站掉得一樣快，看起來就像飄著。", None, "P:float"))
kid("kid-scale-q", K("looking down at her feet with a curious frown, hands on her hips", where=YARD),
    k("那太空人，", "追問"), k("站上體重計會是多少？", "句尾上揚", "S:scale"))
obj("scale-cabin", "Wide shot " + CABIN + ", one round bathroom scale with a smooth plain white top floating gently in the middle of the cabin",
    c("美國太空總署說，一直在掉的時候，體重計會顯示零。", None, "P:scale"),
    c("可是他的身體一點都沒變少，只是量不出重量。"))
kid("kid-scale-zero", K("holding both hands far apart then close together with wide surprised eyes", close=True, where=YARD),
    k("體重計也在掉！", "驚訝"))
obj("drop-ride", "Wide shot of a tall bright amusement park drop tower ride with a ring of empty cartoon seats high near the top, a sunny blue sky, colourful flags around the base",
    c("對。遊樂園的自由落體也一樣："),
    c("往下衝的時候，你放開手裡的東西，它會飄在你面前。"))
chief("chief-micro", C("pinching her thumb and finger close together in front of her chest with a curious smile"),
    c("這種好像沒有重量的樣子，叫做微重力。"),
    c("微，就是很小很小的意思。"))
chief("chief-zero-q", C("drawing a big round circle in the air with one finger and an amused smile", close=True),
    k("那可以叫零重力嗎？", "句尾上揚", "S:zero"),
    c("很多人這樣叫。對不對，等一下你自己判斷。", "笑"))
kid("kid-crash-q", K("pointing down at the grass with a worried frown", where=YARD),
    k("一直往下掉，", "擔心"), k("太空站怎麼沒撞到地球？", "章尾停住，句尾上揚", "S:crash"))

# ---------- 第二章：杯子拋得越快，落得越遠 ----------
chief("chief-sideways", C("sweeping one flat hand quickly sideways in front of her with a bright smile"),
    c("因為它不只往下掉，還往旁邊跑得非常快。", "接住上一句"),
    c("還記得剛剛拋杯子嗎？拋得越用力，落得越遠。"), chapter="杯子拋得越快，落得越遠")
obj("cup-far", "Wide shot of a sunny back yard lawn, " + CUP + " flying high and far in a long gentle curve over the grass, " + BASIN + " far away at the end of the lawn",
    c("可是不管丟多快，杯子都一邊往前、一邊往下掉。"),
    k("那丟得超級超級快呢？", "追問", "S:fast"))
chief("chief-newton", C("shading her eyes with one hand as if looking far away, an adventurous smile"),
    c("很久以前，研究重力的科學家牛頓，就想過這件事：", "接住上一句"),
    c("在很高很高的山頂上，放一座大砲。"))
obj("cannon-peak", "Wide shot of one old round cartoon cannon standing on the top of a very tall snowy mountain peak high above white clouds, a big round blue planet curve far below",
    c("砲彈射得越快，飛得越遠才落地。"),
    c("快到剛剛好，就會一直掉、一直繞著地球跑。", None, "P:fast"))
kid("kid-miss-q", K("holding a small round ball in both hands with a thinking frown", close=True, where=YARD),
    k("一直掉，", "想不通"), k("為什麼掉不到地上？", "句尾上揚", "S:miss"))
obj("ball-curve", "Wide shot of one round black cartoon cannonball flying in a long gentle curve high above a big round blue and green planet, deep blue space above",
    c("因為地球是圓的。砲彈往下彎，地面也跟著往下彎。", "接住上一句"),
    c("兩個彎得一樣，它就一直掉，卻永遠碰不到地。", None, "P:miss"))
obj("station-orbit", "Wide shot of " + STATION + " floating above " + EARTH,
    c("太空站，就是那顆繞著地球掉的砲彈。", None, "P:crash"),
    c("這樣繞著地球掉，就叫做軌道。"))
kid("kid-speed-q", K("leaning forward with sparkling curious eyes", close=True, where=YARD),
    k("那太空站要跑多快？", "句尾上揚", "S:speed"))
chief("chief-speed", C("holding up eight fingers with a big amazed smile"),
    c("美國太空總署說，一秒大約跑八公里。", "數字放慢", "P:speed"))
obj("sunrise-curve", "Wide shot of a bright golden sunrise glowing along the curved edge of a big round blue planet, seen from high above in deep blue space, " + STATION + " small in the corner",
    c("大約九十分鐘，就繞地球一圈。"))
chief("chief-same-speed", C("nodding with a warm smile, both hands open", close=True),
    c("裡面的人和東西，也都跟著跑一樣快。"),
    c("所以他們不會被太空站甩在後面。"))
kid("kid-ground-q", K("hopping up with both arms out like wings and a hopeful grin", where=YARD),
    k("不去太空，", "追問"), k("在地上也能飄起來嗎？", "句尾上揚", "S:ground"))
chief("chief-plane", C("tracing a big gentle hump in the air with one finger, a bright smile"),
    c("可以。還記得拋出去的杯子嗎？", "接住上一句"),
    c("美國太空總署給老師的手冊說，往上飛那段水也不漏。"))
chief("chief-coaster", C("bouncing lightly on her toes with a playful grin, both hands up"),
    c("你坐雲霄飛車衝過小山丘，或是跳彈簧床，"),
    c("也會有一小下，覺得自己飄起來。", None, "P:ground"))
kid("kid-fire-q", K("holding the small tablet up and pointing at it with a curious frown", where=YARD),
    k("那火呢？", "想起來"), k("火跟著一起掉，也會變嗎？", "章尾停住，句尾上揚", "S:firefall"))

# ---------- 第三章：蠟燭丟進很深的井 ----------
chief("chief-well", C("raising both eyebrows with an excited smile, one hand raised", close=True),
    c("會。美國太空總署真的讓火一起掉過。", "接住上一句"),
    c("他們有一口很深的井，東西可以在裡面一直掉五秒多。"), chapter="把蠟燭丟進很深的井")
obj("deep-shaft", "Low angle wide shot looking straight down into a very deep round smooth concrete shaft, simple cartoon rings of soft light fading far down into the dark bottom",
    c("他們把點著的蠟燭放進去，跟著一起往下掉，", None, "P:well"),
    c("火很快就變成圓圓的一團，不再尖尖的。", None, "P:firefall"))
kid("kid-try-fire", K("bouncing on her toes with an excited grin, both fists clenched", where=YARD),
    k("我也要在家丟蠟燭！", "興奮"))
chief("chief-safe", C("holding up one hand like a gentle stop with a kind but firm smile", close=True),
    c("不行喔，火很危險，這要在專門的地方做。", "認真"),
    k("好吧……那為什麼一掉就變圓？", "追問", "S:whyround"))
obj("candle-table", "Close-up of " + CANDLE + " with a tall yellow teardrop-shaped flame, on a wooden table, a plain pale cream wall behind",
    c("你先想想，平常的火為什麼尖尖的？"),
    k("是重力把火往上拉嗎？", "錯猜", "S:up"))
chief("chief-hot-air", C("shaking her head gently with a kind smile, one palm raised", close=True),
    c("重力沒有把火往上拉。是火把空氣燒熱了，", "接住上一句"),
    c("同樣一團空氣，熱的比冷的輕。"))
obj("candle-air", "Close-up of " + CANDLE + " with a tall yellow teardrop-shaped flame, soft wavy wisps of warm shimmering air rising above the tip of the flame, a plain pale cream wall behind",
    c("重力把比較重的冷空氣，拉到火的底下，"),
    c("熱空氣就被推上去，火也被拉成尖尖的。", None, "P:up"))
kid("kid-cup-link", K("holding the small white cup up and looking at its tiny hole with a thinking face", close=True, where=YARD),
    k("就像杯子的水，從小洞擠出去？", "聯想"))
chief("chief-convect", C("giving a small thumbs-up with a pleased smile"),
    c("很像，都是比較重的往下擠。"),
    c("這種熱的往上、冷的補進來的流動，叫做對流。"))
obj("candle-base", "Close-up of the bottom of " + CANDLE + ", soft pale blue curls of fresh air drifting in towards the base of a yellow flame, a plain pale cream wall behind",
    c("冷空氣從底下補進來，正好帶來新鮮的氧氣。"),
    k("氧氣是什麼？", "句尾上揚"),
    c("空氣裡，幫東西燒起來的那一種氣體。"))
chief("chief-cup-again", C("holding the small white cup up with a knowing smile", close=True),
    c("還記得那個杯子嗎？掉的時候，大家掉得一樣快，"),
    c("冷空氣不再往下擠，熱空氣也不再往上跑。"))
obj("round-flame", "Close-up of " + CANDLE + " with a small round soft glowing blue flame ball around the wick, a plain pale cream wall behind",
    c("沒有對流往上拉，氧氣只能從四面八方慢慢靠過來。", None, "P:whyround"))
obj("cabin-flame", "Wide shot " + CABIN + ", one tiny round soft blue flame glowing in the middle of the cabin inside a clear round glass globe",
    c("在太空站上，沒被吹著的小火也常這樣。"))
kid("kid-blue-q", K("pointing at the small tablet with a curious face", close=True, where=YARD),
    k("我看到的火，還是藍色的！", "句尾上揚", "S:blue"))
chief("chief-candle-two", C("holding up a short white candle in one hand with a thoughtful smile"),
    c("他們比過一根蠟燭：在地上，對流把煙灰帶到火尖，"),
    c("所以火是黃的。"))
obj("candle-pair", "Wide shot of two short white candles side by side on a wooden table, the left one with a tall yellow teardrop flame, the right one with a small round soft blue flame, a plain pale cream wall behind",
    c("在微重力裡，那根蠟燭的火是圓的、沒有煙灰，藍藍的。", None, "P:blue"),
    c("不過這只是一根蠟燭，不是每一團太空的火都長這樣。"))
kid("kid-ball-q", K("making a round ball shape with both hands and a curious face", close=True, where=YARD),
    k("那它是一整顆圓球嗎？", "句尾上揚", "S:ball"))
obj("half-ball", "Close-up of " + CANDLE + " with a small soft blue flame shaped like half a round dome sitting above the wick, a dark gap between the flame and the wax, a plain pale cream wall behind",
    c("也不一定。那本手冊說，蠟燭頂端會把熱吸走，", "接住上一句"),
    c("火的底部就熄掉一塊，只看得到球的一部分。", None, "P:ball"))
kid("kid-last-q", K("hugging her knees and gazing at the small tablet with a dreamy face", close=True, where=YARD),
    k("太空的火，", "好奇"), k("會一直燒下去嗎？", "句尾上揚", "S:last"))
chief("chief-diffuse", C("moving one hand very slowly through the air with a calm smile", close=True),
    c("不一定。剛剛說氧氣來得慢，火就燒得沒那麼旺，", "接住上一句"),
    c("溫度會慢慢降下來。"))
obj("candle-dim", "Close-up of " + CANDLE + " with a very small faint round blue flame around the wick, tiny pale blue dots drifting slowly towards it, a plain pale cream wall behind",
    c("一九九二年，在太空中做過的蠟燭實驗，"),
    c("大多一分鐘左右火就滅了，可能是盒子裡氧氣快沒了。", None, "P:last"))
# 2026-11-14 (body back over 480 s after the kid-share cut): a sourced fire-safety segment, claims.md C26.
obj("chief-putout", "Inside a bright cartoon space station module with white padded walls and yellow handrails, a small plain red fire extinguisher floating gently in mid-air, a round window showing the blue Earth",
    k("太空站失火了，要怎麼滅？", "擔心", "S:putout"),
    c("美國太空總署說，太空滅火要看火的樣子和燒的東西。", "接住上一句"))
obj("chief-worse", "Wide shot of a white cartoon space station with long solar panels orbiting above the curve of the blue Earth, a small white cargo spaceship drifting away from it, black starry sky",
    c("在地上好用的滅火方法，到太空可能沒用，", "認真"),
    c("甚至讓火更糟。所以比較大的火，他們不在太空站上燒。"))
obj("cargo-ship", "Wide shot of one small simple cute cartoon cargo spaceship shaped like a short white cylinder with two round solar panels, drifting alone in deep blue space, " + EARTH,
    c("等貨運太空船離開、上面沒有人了，才點火研究。"),
    c("這樣燒大一點的火，太空人也不會有危險。"))
obj("cloth-flame", "Close-up through a round window into a dim empty grey metal room, one long strip of pale cloth held flat in a thin metal frame in the middle, a thin line of small soft blue and orange flame creeping slowly along the cloth",
    c("他們發現，把艙裡的空氣變稀一點，火就蔓延得比較慢。"),
    c("這些研究，幫忙挑選太空船裡用的材料，"))
obj("chief-earth-safe", "A cozy cartoon living room on Earth with a sofa and a rug, a round white smoke detector on the ceiling and a small plain red fire extinguisher standing by the door, warm daylight",
    c("也讓地上的防火更安全。", None, "P:putout"),
    c("有一組研究滅火藥劑的實驗，還發現了一件怪事。", "賣關子"))
kid("kid-out-q", K("folding her arms with a satisfied little nod", where=YARD),
    k("火熄了，", "篤定"), k("就是不燒了吧？", "章尾停住，句尾上揚", "S:out"))

# ---------- 第四章：火熄了，那一滴還在變小 ----------
chief("chief-not-quite", C("holding up one finger with a mysterious smile", close=True),
    c("剛剛那組實驗就發現：不一定。", "接住上一句"), chapter="火熄了，那一滴還在變小")
obj("drop-float", "Close-up of " + DROP + ", two thin wires reaching towards it from both sides",
    c("他們讓一小滴燃料自己飄著，用燒熱的電線點火。"))
obj("drop-glow", "Close-up of " + DROP + ", a bright soft orange glowing flame ball surrounding the drop",
    c("有一次，一滴大約四公釐的燃料，先燒出看得見的火，"),
    c("燒了大約十五秒，那團火忽然熄了。"))
kid("kid-done", K("shrugging with both palms up and a bored pout", where=YARD),
    k("火都滅了，還有什麼好看？", "不以為意"))
obj("drop-dark", "Close-up of " + DROP + ", the glow gone, the dim chamber quiet around the drop",
    c("相機拍不到火了。可是，", "賣關子"),
    c("量熱的儀器發現，那一滴燃料還在發熱。", None, "P:out"))
chief("chief-shrink", C("bringing her two hands slowly closer together with a curious smile"),
    c("而且那一滴還在變小，只是變得慢一點。"),
    c("研究的人，把它叫做冷焰。", None, "P:ghost"))
kid("kid-cold-q", K("hugging herself and shivering playfully with a curious grin", close=True, where=YARD),
    k("火也有冷的？", "好奇"), k("摸起來是冰的嗎？", "句尾上揚", "S:cold"))
chief("chief-cold", C("laughing softly and shaking her head", close=True),
    c("不是冰的。它只是比一般的火溫度低，", "笑", "P:cold"),
    c("幾乎看不見，卻還在燒。"))
obj("drop-small", "Close-up of " + DROP + ", the drop much smaller now, the dim chamber still and quiet around it",
    c("最後，那一滴縮到某個大小時，冷焰突然停了，"),
    c("剩下的那一滴，只是慢慢蒸發掉。"))
kid("kid-why-q", K("looking up at the sky with a puzzled face", where=YARD),
    k("為什麼要到太空，", "追問"), k("才看得清楚？", "句尾上揚", "S:why"))
chief("chief-why", C("nodding with a thoughtful honest smile", close=True),
    c("美國太空總署說，在地上做出的冷焰，很快就熄了；", "接住上一句"),
    c("在微重力裡燒得比較久，科學家才有機會研究。", None, "P:why"))
chief("chief-quiet", C("holding both hands still in front of her with a calm content smile"),
    c("那本老師手冊也說，地上的對流，會把火的一些事蓋住。"),
    c("拿掉對流，火比較安靜，科學家更容易看懂它。"))
kid("kid-same-q", K("holding the small tablet with a thinking face", where=YARD),
    k("太空的火，", "追問"), k("是不是都會這樣？", "句尾上揚", "S:same"))
chief("chief-gas", C("holding up one finger with a careful smile", close=True),
    c("不是。同一組實驗，換掉周圍的氣體，結局就變了。", "接住上一句"))
obj("drop-pop", "Close-up of " + DROP + ", a fierce bright orange flame hugging the drop closely, the tiny drop bursting into a few even tinier droplets",
    c("像是氧氣多一點，液滴燒到很小時，會自己爆開。"))
kid("kid-depends", K("clapping her hands together with a bright realising grin", close=True, where=YARD),
    k("所以火的樣子，", "恍然"), k("還要看旁邊是什麼氣體！", None, "P:same"))
chief("chief-zero-ask", C("tilting her head with a playful questioning smile, one open hand towards the girl"),
    c("對。那還記得零重力嗎？你自己判斷呢？", "接住上一句"))
kid("kid-zero", K("raising one finger with a proud confident grin", close=True, where=YARD),
    k("不能叫零重力！", "得意"), k("重力一直在！"))
chief("chief-zero", C("giving a warm thumbs-up with a proud smile", close=True),
    c("對。美國太空總署也說，叫零重力會讓人誤會。", None, "P:zero"))
kid("kid-final-q", K("looking down at the small tablet with a thinking face", where=YARD),
    k("太空人在掉，", "推理"), k("那團火為什麼也變了？", "章尾停住，句尾上揚"))

# ---------- 收尾 ----------
chief("chief-your-turn", C("leaning forward with an inviting grin, one hand open towards the viewer"),
    c("杯子、蠟燭你都看過了，你說呢？", "笑"), chapter="回到那段影片，小問想通了")
kid("kid-got-it", K("holding the small white cup up high with a big confident grin", where=YARD),
    k("原來如此！", "恍然大悟"), k("火和旁邊的空氣，一起在掉，", "篤定"),
    k("火就不會被拉成尖尖的！", "篤定", "P:main"))
chief("chief-opinion", C("smiling with her hands clasped, a thoughtful look", close=True),
    c("說得好。我覺得最妙的是：", "笑"),
    c("讓杯子不漏水的那件事，也讓火變了樣子。", None, "P:round"))
# The outro is three pictures, no card, no stamp (series README §3.2, §10.1): the kid gives a thumbs-up.
kid("outro", "Waist-up medium shot of the girl with a big happy smile giving a big cheerful thumbs-up with one hand, bright morning light",
    k("我要拋杯子給媽媽看！", "開心大聲"))
chief("outro-chief", "Waist-up medium shot of the chief holding up a small plain white cup with a curious smile, filling the frame, a plain pale wall behind her, bright morning light",
      c("你在哪裡覺得自己飄了一下？", "問句上揚，像聊天"), c("留言告訴我們。"))
chief("outro-wave", "Waist-up medium shot of the chief waving goodbye with a warm smile, a plain pale wall behind her, bright morning light",
      c("想一起找生活裡的為什麼，就訂閱原來如此事務所。", "誠懇"))

# ---------- assemble ----------
WHAT = {"main": "人一直在掉，火為什麼也跟著變了", "round": "影片裡那團火為什麼圓圓的",
        "nograv": "是不是太空沒有重力", "falling": "太空人其實一直在往下掉，是什麼意思",
        "leak": "破洞的杯子拋出去，水會不會一路灑出來", "gone": "一拋出去，重力是不是不見了",
        "float": "太空人還那麼重，怎麼會飄", "zero": "能不能叫零重力",
        "crash": "一直往下掉，太空站怎麼沒撞到地球", "fast": "拋得超級快會怎樣",
        "miss": "一直掉，為什麼掉不到地上", "speed": "太空站要跑多快",
        "firefall": "火在掉的時候也會變嗎", "whyround": "為什麼一掉火就變圓",
        "up": "是不是重力把火往上拉", "blue": "看到的火為什麼是藍色的",
        "last": "太空裡的火會不會一直燒下去", "out": "火熄了是不是就不燒了",
        "cold": "冷焰摸起來是不是冰的",
        "why": "為什麼要到太空才看得清楚冷焰", "same": "太空裡的火是不是都一樣",
        "scale": "太空人在太空站站上體重計是多少", "ground": "不去太空，在地上能不能飄起來",
        "ball": "太空的蠟燭火是不是一整顆圓球",
        "well": "點著的蠟燭掉進很深的井會怎樣", "ghost": "哪一團火熄了以後還在燒",
        "putout": "太空站失火了要怎麼滅"}
# Latin terms the Mandarin voice must spell letter by letter (P13 GPS, P29 HTTPS/TLS). This episode says
# 美國太空總署 (the usual Taiwanese name) instead of NASA, so no spoken line carries a Latin term; the loop stays
# so a later edit that adds one is spelled and carries say_for.
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
    "series": {"slug": "sothatswhy", "episode": 4, "chapter": 1},
    # 2026-11-11 (README §9 停頓, §10.6): no fixed pause between lines, a short gap between scenes, beat-timed stills.
    "pauses": {"line_ms": 0, "scene_ms": 150},
    "still_motion": "beat",
    # The series bed from P15 on (explainer-series/README.md, PR #2048): sothatswhy-bed-r2.m4a, remade from P02's paid take.
    "music": {"track": "sothatswhy-bed-r2.m4a", "sha256": "9bb4ba6fd16feb4a7f352144b2d89e9648acbbbbaa2173c27a7eefbdb70f28c6", "gain_db": -20, "duck_db": -10},
    "characters": CHARACTERS, "loops": loops,
    "youtube": {
        "category_id": 27, "made_for_kids": False, "default_language": "zh-TW",
        "title": "太空人一直在掉，火焰為什麼也變了？｜原來如此事務所",
        "description": "太空站的影片裡，太空人飄來飄去，旁邊一團小火圓圓的，像一顆球；家裡蠟燭的火，卻是尖尖的。\n"
                       "小問說「一定是太空沒有重力」，可是太空站那個高度，重力還有地面的九成左右。那太空人為什麼會飄？火又為什麼變了樣子？\n\n"
                       "這一集，所長和小問在後院拿一個底下有小洞的杯子來想：拿著時水會從洞裡流出來，輕輕拋出去，杯子和水一起往下掉，水就不漏了。"
                       "太空站那麼高的地方，地球的重力還有地面的九成左右，太空人會飄，是因為人、東西和太空站一起在掉；它同時往旁邊跑得非常快，所以一直繞著地球掉，卻掉不到地上。"
                       "在地上，火把空氣燒熱，比較重的冷空氣被拉到火的底下，把熱空氣往上推，火就被拉成尖尖的；大家一起掉的時候，這股對流停了，火就可能變圓。"
                       "最後看太空站上的液滴燃燒實驗：看得見的火熄了以後，還有幾乎看不見的「冷焰」繼續燒；換掉周圍的氣體，結局也跟著變。所以太空裡的火不是都長一個樣子，微重力也不是零重力。\n\n"
                       "片中的杯子、蠟燭、井、太空站與液滴都是 AI 生成的示意插圖，不是實驗的照片或實際的器材；火很危險，請不要自己在家做燃燒的實驗。每個說法的出處列在下方參考資料。\n\n資料截至 " + CHECKED,
        "tags": ["微重力", "太空站", "自由落體", "火焰", "蠟燭", "對流", "冷焰", "軌道", "科普", "原來如此事務所"]},
    "thumbnail": {"template": "thumb", "data": {"headline": "太空的火\n**變圓了？**", "sub": "重力明明還有九成", "shot": "cabin-flame", "subject": "right"}},
    "sources": [
        {"title": "NASA STEM, What Is Microgravity? (Grades 5-8)", "url": "https://www.nasa.gov/learning-resources/for-kids-and-students/what-is-microgravity-grades-5-8/", "checked_on": CHECKED},
        {"title": "NASA Glenn Research Center, What is Microgravity?", "url": "https://www.nasa.gov/centers-and-facilities/glenn/what-is-microgravity/", "checked_on": CHECKED},
        {"title": "NASA, Space Station Facts and Figures", "url": "https://www.nasa.gov/international-space-station/space-station-facts-and-figures/", "checked_on": CHECKED},
        {"title": "NASA, Microgravity: A Teacher's Guide with Activities in Science, Mathematics, and Technology (EG-1997-08-110-HQ)", "url": "https://files.eric.ed.gov/fulltext/ED463964.pdf", "checked_on": CHECKED},
        {"title": "NASA Space Station Research Integration Office, Studying Combustion and Fire Safety", "url": "https://www.nasa.gov/missions/station/iss-research/studying-combustion-and-fire-safety/", "checked_on": CHECKED},
        {"title": "NASA, Candle Flame - 1g vs Microgravity", "url": "https://www.nasa.gov/image-article/candle-flame-1g-vs-microgravity/", "checked_on": CHECKED},
        {"title": "Nayagam, Dietrich, Hicks & Williams (2014), Cool-flame Extinction During N-Alkane Droplet Combustion in Microgravity (NASA NTRS 20140006750)", "url": "https://ntrs.nasa.gov/citations/20140006750", "checked_on": CHECKED},
        {"title": "Ross, Dietrich & Tien, Candle Flames in Microgravity: USML-1 Results - 1 Year Later (NASA NTRS 20030075810)", "url": "https://ntrs.nasa.gov/citations/20030075810", "checked_on": CHECKED},
    ],
    "assets": [],
    "scenes": scenes,
}
json.dump(doc, open(os.path.join(HERE, "video.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
FROZEN.update({s["id"]: s["data"]["camera"] for s in scenes if s["template"] == "shot" and s["id"] not in FROZEN})
json.dump(FROZEN, open(CAM_FILE, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# ---------- self-checks (the series rules lint does not cover for a sothatswhy- slug) ----------
# 2026-11-11: the faster style speaks about 4.4 characters a second (README §4: P06 measured 4.39), and the
# pauses are now only scene_ms between scenes plus a BEAT_MS beat before each payoff (README §10.6).
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
assert len(loops) >= 10, "the plan asks for at least 10 loops, every one paid off"
# Upper bound only (owner 2026-11-11: never pad; the 8-minute floor is judged on the honest content, README §9).
assert body_chars <= 3000, f"body {body_chars} characters: keep under 3,000 (plan 10–12 min at 4.4 chars/s)"
cams = [s["data"]["camera"] for s in scenes]
assert all(not (a == b == c_) for a, b, c_ in zip(cams, cams[1:], cams[2:])), "three shots in a row with the same camera"
