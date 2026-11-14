"""Generate video.json for sothatswhy-p21-car-sickness (原來如此事務所 對話版 P21).

Run `python3 build_scenes.py` from anywhere: it rewrites video.json next to this file and freezes
every shot's camera move in cameras.json (a shot keeps the camera it was first given, so deleting
a shot never shifts the others: the camera is in the keyframe cache key).
Edit lines and prompts here, never in video.json.
Started from a copy of sothatswhy-p06-bubble-film/build_scenes.py (series constants, helpers,
assembly and self-checks unchanged except for the 2026-11-11 rules below; EXTRA starts empty; REWRITE holds the 12 redraws of the 2026-11-11 zoom check
because P06's entries were picture fixes for P06 only); the content is new.
2026-11-11 rules applied (dialogue-pilot README §4, §9, §10.6): the faster voice style for both characters,
`pauses: {line_ms: 0, scene_ms: 150}` and `still_motion: "beat"`, no `pause_after_ms` on lines except a
BEAT_MS beat on the line right before each `P:` payoff in the same scene, and only an upper bound on length.
2026-11-13 rules applied (README §2, §10.6; lessons/sothatswhy.md 一般觀眾視角檢討): the kid's filler and restating
lines cut to bring her share of Han characters from 22% to under 20% (no scene, prompt or loop tag changed), the opening
starts on the problem, and the thumbnail sub and the description pose the contradiction instead of giving the cause.
`script.md` is written by `node tools/video/cli.mjs script --slug sothatswhy-p21-car-sickness` after this runs.
"""
import itertools, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = "sothatswhy-p21-car-sickness"
CHECKED = "2026-11-11"
BEAT_MS = 500   # 答案揭曉前的一拍；第一集照這個試，成片量過再調（README §10.6）

# ---------- series constants ----------
# Both characters are identical to P06/P07/P14/P08 (approved series sheets reused through the `series` tag):
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
EXTRA = {}
# Whole-prompt rewrites after a visual review. Empty until this episode's keyframes are drawn and checked.
REWRITE = {  # 2026-11-11 zoom check: no usable take among three (verdict-A..D.json)
    "chief-tease-blind": "Waist-up medium shot of the chief holding a plain pale-blue fabric sleep mask with two oval eye cups and a stretchy strap up beside her face in one hand, giving a playful wink with one eye closed and a cheeky smile, a plain pale wall behind her, bright daylight, the chief is a middle-aged woman with round black glasses, dark hair with a grey streak tied in a low ponytail, a yellow pencil tucked behind one ear, a mustard-yellow cardigan over a white blouse and navy trousers, chibi proportions, simple flat 2D cel-shaded cartoon drawing with clean ink outlines and flat colours",
    "kid-close-guess": "Waist-up medium shot of one 8-year-old girl sitting in the back seat of a small family car, a diagonal seat belt across her chest, her eyes squeezed tightly shut as two curved lines, a confident proud grin, both hands resting on her knees, bright daylight through the side window, the girl is 8 years old with a short black bob, straight bangs and one small cowlick on top, a round young face with simple dot-like eyes, wearing a navy raincoat jacket with a mustard-yellow hood folded down behind her neck, simple flat 2D cel-shaded cartoon drawing with clean ink outlines and flat colours",
    "kid-blindfold": "Waist-up medium shot of one 8-year-old girl sitting calmly in the back seat of a small family car, a diagonal seat belt across her chest, a soft pastel-blue sleep mask pulled down fully over both of her eyes, a calm small smile, her hands resting in her lap, bright daylight through the side window, the girl is 8 years old with a short black bob, straight bangs and one small cowlick on top, a round young face with simple dot-like eyes, wearing a navy raincoat jacket with a mustard-yellow hood folded down behind her neck, simple flat 2D cel-shaded cartoon drawing with clean ink outlines and flat colours",
    "coach-road": "Wide shot of a big friendly round-nosed tour coach driving along a sunny green coastal road, blue sea and soft green hills around it, the coach painted smooth solid sunny yellow with one plain wide teal stripe along its side, rows of tiny round passenger heads in its windows, white clouds in a bright sky, simple flat 2D cel-shaded cartoon drawing with clean ink outlines and flat colours",
    "display-high": "View from the front passenger seat of a small family car, a child passenger's two small hands holding a small plain tablet up high at windshield level, the tablet showing colourful circles and stars, a sunny road and green hills visible all around it through the windshield, the passenger side dashboard and glovebox along the bottom of the frame, simple flat 2D cel-shaded cartoon drawing with clean ink outlines and flat colours",
    "kid-dad-q": "Waist-up medium shot of one 8-year-old girl alone in the back seat of a small family car, a diagonal seat belt across her chest, leaning forward between the two front seats with a curious frown, the back of her dad's short dark hair and his hands on the steering wheel visible in the front seat, the sunny road ahead through the windshield, bright daylight, the girl is 8 years old with a short black bob, straight bangs and one small cowlick on top, a round young face with simple dot-like eyes, wearing a navy raincoat jacket with a mustard-yellow hood folded down behind her neck, simple flat 2D cel-shaded cartoon drawing with clean ink outlines and flat colours",
    "chief-control": "Head-and-shoulders close-up of the chief, a slim woman of about thirty with round black glasses, glossy dark hair with a grey streak tied in a low ponytail, a yellow pencil tucked behind one ear, a mustard-yellow cardigan over a white blouse, nodding with a warm encouraging smile and one finger raised beside her face, a calm clean pale wall behind her, bright daylight, simple flat 2D cel-shaded cartoon drawing with clean ink outlines and flat colours",
    "chief-game-test": "Waist-up medium shot of a cheerful middle-aged woman holding a chunky dark grey game controller out towards the viewer in both hands, an inviting smile, a plain pale cream wall behind her, bright daylight. She has round black glasses, dark hair with one grey streak tied in a low ponytail, a yellow pencil tucked behind one ear, a mustard-yellow cardigan over a white blouse and navy trousers. The controller is a simple gamepad with two round thumbsticks and four coloured buttons, firmly gripped, five fingers on each hand. Cute chibi proportions with a big round head, simple flat 2D cel-shaded cartoon drawing with clean ink outlines and flat colours",
    "kid-game-guess": "Waist-up medium shot of an 8-year-old girl in a sunny living room beside a mustard sofa, holding a dark grey game controller up proudly in one raised hand with a confident grin. She has a short straight black bob with blunt straight-cut bangs and one small curl of cowlick on top, the bob uncovered and hanging free, simple dot-like eyes and round pink cheeks, and wears a navy raincoat jacket with its mustard-yellow hood folded down behind her neck and long navy trousers. Cute chibi proportions with a big round head, simple flat 2D cel-shaded cartoon drawing with clean ink outlines and flat colours",
    "kid-carscreen-q": "Waist-up medium shot of an 8-year-old girl sitting in a car back seat with a grey seat belt across her chest, holding up a small smooth dark grey tablet in one hand and pointing at it with the other, a bright idea face with raised eyebrows and a wide smile, beige cartoon car seats and a sunny side window behind her. She has a short straight black bob with blunt straight-cut bangs and one small curl of cowlick on top, simple dot-like eyes and round pink cheeks, and wears a navy raincoat jacket with its mustard-yellow hood folded down behind her neck. Cute chibi proportions with a big round head, simple flat 2D cel-shaded cartoon drawing with clean ink outlines and flat colours",
    "kids-shoes-row": "Close-up of a sunny doorstep with four pairs of children's shoes lined up in one neat row from left to right, growing steadily in size: a pair of tiny pink baby booties, a pair of small blue toddler shoes, a pair of medium yellow school sneakers and a pair of big red grown-up sneakers, eight shoes in total, each pair standing side by side, plain smooth shoe surfaces, a warm orange door behind, potted plants at both sides, simple flat 2D cel-shaded cartoon drawing with clean ink outlines and flat colours",
    "twin-shoes": "Close-up of a sunny doorstep with two identical pairs of small yellow children's sneakers standing side by side, four shoes in total, the two pairs matching exactly like twins, empty shoes standing neatly on the step, plain smooth shoe surfaces, a warm orange door behind, simple flat 2D cel-shaded cartoon drawing with clean ink outlines and flat colours",
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

HOME = "in a sunny living room"
CAR = "in a car back seat, seat belt on,"
TRAIN = "by a train window"
# One drawing language for the whole episode (README §10.5, P17/P18: the image model cannot draw anatomy,
# cross-sections, arrows, counts or directions): the inner ear is never drawn. The one metaphor carried from
# start to end is A CUP OF WATER: the balance organ is like a cup of water riding along with you (the water
# sloshes when the car turns, brakes or speeds up), and the eyes are a second reporter. Every mechanism frame is a
# cup of water somewhere human-sized: tilted in the car's cup holder, dead level on a coffee table in front of a
# racing game, held steady in someone's own hand. Nothing is counted, nothing depends on which way it tilts.
STYLE = ", simple flat 2D cel-shaded cartoon drawing with clean ink outlines and flat colours"
CUP = "a clear plastic cup of water"
COMIC = "a small comic with a plain red cover"
def obj(id, prompt, *lines, chapter=None):
    """An everyday-object frame with nobody in it, always in the flat cartoon style (P18: object
    prompts without style words came out as photos)."""
    scene(id, prompt + STYLE + ", clean empty corners", *lines, chapter=chapter)

# ---------- 開場（系列片頭之後直接進場景，不做濃縮；答案都不先講）----------
# The first picture is the problem itself: the family car on the winding mountain road to grandma's.
obj("car-mountain", "Wide shot of a small rounded family car driving along a winding green mountain road on a sunny morning, tea bushes and blue sky around it",
    k("我坐車去阿嬤家，", "委屈又急，跑進來報案的語氣"), chapter="去阿嬤家的山路")
# Thumbnail shot (fixed before keyframes, explainer-series/README.md): the kid big and centred, the comic in hand.
kid("kid-reading-open", K("giggling at " + COMIC + " held close to her face", close=True, where=CAR),
    k("看漫畫看到一半，", "難受"))
kid("kid-comic-sick", K("holding " + COMIC + " in both hands on her lap, looking up from it with a queasy pale face and puffed cheeks, in the exact centre of the picture", where=CAR),
    k("頭暈暈的，肚子也怪怪的。", "難受"))
obj("driver-view", "Wide view from the back seat of a small family car between the two empty front headrests, the steering wheel and a winding sunny mountain road ahead through the windshield",
    k("可是爸爸在前面開車，", "不服氣"), k("一點事都沒有！", None, "S:dad"))
chief("chief-listen", C("leaning forward with a curious smile, one hand on her chin", close=True),
      c("同一台車、同一條路，只有你在暈？", "接住上一句"))
chief("chief-tease-blind", C("holding a soft pastel sleep mask up in one hand and winking playfully"),
      c("還有更怪的：遮住眼睛坐車，會不會暈？", "賣關子", "S:blind"))
chief("chief-tease-sofa", C("sitting very still on a sofa holding a game controller, a puzzled playful face"),
      c("坐在沙發上不動，只看賽車畫面，又會不會暈？", "賣關子", "S:sofa"))
kid("kid-me-too", K("pointing at herself with a surprised face", where=HOME),
    k("我猜都不會！", "篤定的錯猜"))
chief("chief-promise", C("holding a clear plastic cup of water up beside her face with a warm inviting smile"),
      c("先別猜。你會暈，絕對不是你一個人。", "轉向觀眾"), c("今天就用去阿嬤家這一趟，把原因找出來。"))
kid("kid-main-q", K("holding " + COMIC + " against her chest and frowning with a puzzled tilted head", where=CAR),
    k("我的頭跟肚子，", "想不通"), k("到底怎麼了？", "句尾上揚", "S:main"))

# ---------- 第一章：眼睛和耳朵，各說各的 ----------
kid("kid-ear-guess", K("cupping one hand behind her ear with a worried little frown", close=True, where=HOME),
    k("會暈車，", "擔心"), k("我聽說是耳朵裡面不好？", "擔心的錯猜", "S:broken"), chapter="眼睛和耳朵，各說各的")
chief("chief-opposite", C("shaking her head gently with a kind smile, one hand raised", close=True),
      c("那叫內耳。不一定喔，研究暈車的人發現，", "接住上一句"), c("內耳的平衡功能完全不能用的人，才完全不會暈。", None, "P:broken"))
chief("chief-almost-all", C("opening both arms wide towards the viewer with a reassuring smile"),
      c("耳朵裡面好好的人，幾乎每一個都可能暈。"))
kid("kid-working", K("touching her own ear with one finger and a surprised delighted face", close=True, where=HOME),
    k("所以耳朵有在認真？", "驚訝"))
chief("chief-working", C("nodding with a warm amused smile", close=True),
      c("可以這麼說：會暈，代表它一直在工作。", "笑"))
kid("kid-ear-q", K("tilting her head with one hand on her ear and a curious face", where=HOME),
    k("到底在做什麼？", "追問，句尾上揚", "S:ear"))
chief("chief-inside", C("holding her thumb and finger a tiny gap apart beside her ear, a curious smile", close=True),
      c("你耳朵很深的地方，有幾條很細的小管子和小袋子，"), c("裡面裝著液體。"))
chief("chief-cup", C("holding up a clear plastic cup of water in one hand with a friendly smile"),
      c("我們借一杯水來想。", "轉向觀眾"))
obj("cup-holder-tilt", "Close-up of " + CUP + " standing in the cup holder of a small family car, the water surface tilted and sloshing up one side of the cup, sunny car interior around it",
    c("車子一轉彎，杯子裡的水就晃到一邊；"), c("一煞車、一加速，水也跟著晃。"))
chief("chief-grains", C("tipping a clear plastic cup of water gently in one hand and watching the water with a thoughtful smile", close=True),
      c("耳朵裡的液體也會晃，裡面還有很小的顆粒，被地球往下拉。"))
chief("chief-brain-reads", C("pretending to steer a car with both hands, then braking with a surprised laughing face"),
      c("大腦就看它們怎麼晃，知道你在轉、在加速，還是在煞車。", None, "P:ear"))
chief("chief-limit", C("putting a clear plastic cup of water down on a small table with an honest serious smile"),
      c("先說清楚，杯子只是比喻。真的耳朵裡面很小很小，"), c("而且管轉彎的地方，跟管加速的地方，是分開的。"))
kid("kid-eyes-q", K("pointing at her own eyes with two fingers and a curious face", close=True, where=HOME),
    k("眼睛也會告訴大腦嗎？", "追問，句尾上揚", "S:eyes"))
chief("chief-eyes", C("pointing at her own eye with one finger and a friendly smile", close=True),
      c("會。眼睛看外面的東西怎麼跑，也在告訴大腦你在動。"), c("腳底跟肌肉，也會告訴大腦。"))
kid("kid-walk-q", K("walking forward in mid-step along a sunny park path with a curious face", where="in a sunny park"),
    k("那我走路的時候呢？", "句尾上揚"))
obj("walk-cup", "Close-up of a child's small hand carrying " + CUP + " along a sunny park path, the water gently rippling, trees and grass blurred behind",
    c("你走路，眼睛看到路往後退，杯子裡的水也在晃。"), c("大家說的都一樣，大腦就很放心。", None, "P:eyes"))
kid("kid-liar-q", K("holding " + COMIC + " up and peering over it with narrowed suspicious eyes", where=CAR),
    k("那我看漫畫的時候，", "推理"), k("是誰在說謊？", "章尾停住，句尾上揚", "S:liar"))

# ---------- 第二章：漫畫跟著小問一起晃 ----------
chief("chief-nobody-lies", C("holding up two fingers with a calm friendly smile", close=True),
      c("沒有人說謊，只是它們看到的不一樣。", "接住上一句"), chapter="漫畫跟著小問一起晃")
kid("kid-reading", K("looking down at " + COMIC + " held close to her face, completely absorbed", where=CAR),
    k("我一直盯著漫畫看耶！", "回想"))
chief("chief-comic", C("holding a small red comic close in front of her chest and swaying gently with it, a thoughtful smile"),
      c("漫畫拿在你手上，跟著你一起晃。"), c("眼睛盯著它，報告的是：沒在動。"))
obj("cup-turn", "Close-up of " + CUP + " in the cup holder of a small family car on a bend, the water surface tilted and sloshing, a curving green mountain road visible through the side window",
    c("可是車子一轉彎，杯子裡的水晃了。"), c("內耳報告的是：我們在轉彎。", None, "P:liar"))
kid("kid-two-reports", K("holding up one finger on each hand with a surprised realising face", where=CAR),
    k("一個說沒動，", "恍然"), k("一個說在轉！"))
chief("chief-mismatch", C("holding her two hands apart at different heights with a calm smile", close=True),
      c("對，兩邊的報告對不上。"))
kid("kid-close-guess", K("squeezing her eyes shut tight with a confident grin", where=CAR),
    k("那我閉上眼睛，", "很有把握"), k("就不會吵了吧？", "很有把握的錯猜", "S:close"))
chief("chief-recall-blind", C("holding up one finger with a playful knowing smile", close=True),
      c("還記得我說，遮住眼睛的乘客照樣會暈嗎？", "點名回呼"))
kid("kid-blindfold", K("wearing a soft pastel sleep mask over her eyes, sitting calmly with her hands on her lap", where=CAR),
    c("英國有研究讓乘客在郊區坐車三十分鐘，"), c("遮住眼睛的人，跟看不到前面的人，差不多一樣暈。", None, "P:blind"))
chief("chief-close", C("closing her eyes gently with a calm thoughtful smile", close=True),
      c("所以閉上眼睛，也不一定能讓大腦安靜。", None, "P:close"))
kid("kid-who-q", K("lifting a sleep mask up onto her forehead with a puzzled frown", where=CAR),
    k("還在跟誰吵？", "不解，句尾上揚", "S:who"))
chief("chief-guess-brain", C("tapping her temple with one finger and a thoughtful smile"),
      c("這就是重點。大腦不只聽報告，它自己還會先猜。"))
chief("chief-predict", C("holding a clear plastic cup of water out level in front of her and watching it closely, a curious smile", close=True),
      c("它心裡有一個預想：照現在這樣，等一下應該感覺到什麼。"))
chief("chief-conflict", C("bringing her two fists together knuckle to knuckle with a serious kind smile", close=True),
      c("報告跟這個預想對不上，人就會不舒服。", None, "P:who"))
chief("chief-label", C("holding one finger up with an honest careful smile", close=True),
      c("這叫感覺衝突，是目前研究暈車最多人接受的解釋。"), c("不過它是一個解釋，還不是全部的答案。"))
kid("kid-window-q", K("pressing her nose close to the side window of the car with a hopeful face", where=CAR),
    k("看窗外會比較好嗎？", "追問，句尾上揚", "S:window"))
obj("coach-road", "Wide shot of a big friendly round-nosed tour coach driving along a sunny green coastal road, blue sea and hills around it",
    c("研究的人真的去問過。英國問了三千多位遊覽車乘客，"), c("完全看不到前面路的人，覺得不舒服的，"))
obj("road-ahead", "Wide view from the middle of the back seat of a small family car looking forward through the windshield at a long sunny mountain road and the far horizon, the two front headrests at the bottom edges",
    c("大約是看得很清楚的人的三倍。", "數字放慢"))
obj("side-window", "Medium view out of the side window of a small family car, green trees and roadside bushes streaking past in soft motion blur, a sunny sky above",
    c("剛剛那個遮眼睛的小客車實驗也發現：只看得到旁邊的窗，"), c("跟看不到前面差不多。"))
chief("chief-forward", C("pointing straight forward past the viewer with one arm and a bright smile"),
      c("看得到前面的路，才比較不暈。", None, "P:window"))
kid("kid-front-q", K("pointing forward between the two front seats with a surprised face", where=CAR),
    k("不是窗戶？", "發現，句尾上揚"))
chief("chief-seat", C("nodding with a calm smile, one open hand forward", close=True),
      c("對。那個實驗裡，坐哪個位子，反而沒有明顯差別。"))
chief("chief-my-guess", C("drawing a gentle curve in the air with one fingertip, a curious smile"),
      c("我的想法是：前面的路一彎，眼睛先看到，"), c("大腦就猜得到，杯子裡的水等一下要晃。"))
chief("chief-holland", C("holding a small plain tablet up at eye level with both hands and a curious smile", close=True),
      c("荷蘭也有實驗，讓乘客在車上邊坐邊看螢幕找東西。"))
obj("display-high", "Close-up of a small plain tablet held up high at eye level in front of a car windshield, showing a simple picture of colourful shapes, a sunny road and green hills visible all around it",
    c("螢幕擺在前窗那麼高、看得到外面，比擺在低處比較不暈。"))
kid("kid-dad-q", K("peeking forward between the front seats with a curious frown", where=CAR),
    k("那爸爸呢？", "追問"), k("就因為這樣不暈嗎？", "句尾上揚"))
chief("chief-driver", C("holding an imaginary steering wheel with both hands and a playful smile"),
      c("看前面只是一部分。司機很少暈車，研究的人也注意到了。", "接住上一句"))
obj("swivel-chair", "Close-up of a single sturdy padded swivel chair standing in the middle of a bright plain empty room, soft curved motion lines around its base, sunny window light",
    c("以色列有個實驗，讓二十二對人坐上會轉的機器。"))
chief("chief-yoked", C("holding up two fingers side by side, then wiggling only one of them, a playful smile"),
      c("每一對轉得一模一樣，可是只有一個人能控制怎麼轉。"))
kid("kid-control-q", K("pretending to steer with both hands and a hopeful grin", where=HOME),
    k("能控制的人，", "猜"), k("比較不暈？", "句尾上揚"))
chief("chief-control", C("nodding with an encouraging smile, one finger raised", close=True),
      c("對，能控制的那一個，不舒服的感覺明顯比較少。"))
obj("own-cup", "Close-up of an adult hand holding " + CUP + " steady while turning a corner along a sunny hallway, the water surface calm and level",
    c("研究的人認為：自己要轉彎，大腦早就知道，"), c("杯子裡的水一晃，剛好跟它猜的一樣。", None, "P:dad"))
chief("chief-cue", C("cupping one hand beside her mouth as if calling out softly, a friendly smile", close=True),
      c("還有實驗用聲音先提醒：什麼時候、要往哪動。"), c("有提醒的時候，同一群人也比較不暈。"))
kid("kid-dad-says", K("cupping both hands around her mouth and calling out with a cheerful grin", where=CAR),
    k("就像爸爸先喊一聲，", "笑"), k("要轉彎囉？", "句尾上揚"))
chief("chief-cue-limit", C("raising one hand with a gentle honest smile", close=True),
      c("有點像。不過那個實驗是在軌道上滑的車，不是山路。"))
kid("kid-reverse-q", K("holding " + COMIC + " upside down and staring at it with a thinking face", where=CAR),
    k("眼睛說在動，", "推理"), k("身體說沒動呢？", "章尾停住，句尾上揚", "S:reverse"))

# ---------- 第三章：換成螢幕在動 ----------
chief("chief-sofa", C("sitting on a sofa holding a game controller and smiling", close=True),
      c("那就是剛剛說的，沙發上的情況。", "接住上一句"), chapter="換成螢幕在動")
obj("sofa-tv", "Wide shot of a cosy sunny living room, a big flat television on a low cabinet showing a bright cartoon racing road rushing into green hills, a game controller resting on the sofa cushion",
    c("你坐在沙發上看賽車遊戲，畫面裡的路一直衝過來，"), c("眼睛報告：我們跑得飛快。"))
obj("table-cup", "Close-up of " + CUP + " standing on a low wooden coffee table, the water surface perfectly flat and still, a sunny living room softly blurred behind",
    c("可是茶几上那杯水，一動也不動，"), c("你的內耳報告的也是：沒在動。"))
kid("kid-reverse", K("sitting on a sofa holding a game controller and looking up with a surprised open mouth", where=HOME),
    k("這次換眼睛，", "驚訝"), k("說在動了！"))
chief("chief-reverse", C("turning one open palm over with a thoughtful smile", close=True),
      c("對，剛好跟看漫畫反過來。這樣也有人會暈，", None, "P:reverse"), c("研究的人叫它，視覺引起的暈動症。"))
kid("kid-long-name", K("counting on her fingers with a scrunched-up face", close=True, where=HOME),
    k("名字好長！", "笑"))
chief("chief-short-name", C("laughing softly with one hand raised", close=True),
      c("你就記：眼睛看出來的暈。", "笑"))
chief("chief-cinema", C("sitting in a red cinema seat holding a striped bucket of popcorn and leaning back in surprise"),
      c("在電影院看大銀幕、玩虛擬實境，都有人遇過。", None, "P:sofa"))
kid("kid-vection-q", K("sitting very still on a sofa with both hands flat on her knees and a puzzled face", where=HOME),
    k("可是我又沒在動，", "不解"), k("為什麼會覺得在動？", "句尾上揚", "S:vection"))
chief("chief-train", C("holding the edge of an imaginary window with a curious smile"),
      c("你坐過火車吧？停在月台的時候，旁邊那列開走了，"))
obj("train-window", "Medium view out of the window of a bright local train standing at a sunny platform, a neighbouring blue and white train right beside it sliding slowly past, its windows a smooth blur",
    c("你會突然覺得，是自己這列在動。"))
kid("kid-train", K("gripping the window ledge with a surprised laughing face", where=TRAIN),
    k("有！我以為車子開了！", "笑"))
chief("chief-vection", C("waving one hand past her eyes with a playful smile", close=True),
      c("那叫自己在動的錯覺。眼睛一下子，就騙過大腦了。", None, "P:vection"))
chief("chief-vection-limit", C("holding her two hands side by side with an honest thoughtful smile"),
      c("眼睛看出來的暈，常常跟這種錯覺一起出現。"))
kid("kid-train-fine", K("smiling happily and waving out of the window", where=TRAIN),
    c("可是有錯覺的人不一定會暈，兩者怎麼連，研究的人還在爭論。"))
kid("kid-either-way", K("sitting cross-legged on a sofa cushion holding both palms up like a weighing scale with a thinking face", where=HOME),
    k("所以不管哪一邊，", "推理"), k("對不上就可能暈？", "句尾上揚"))
chief("chief-works", C("nodding with a warm pleased smile", close=True),
      c("對，這是感覺衝突說得通的地方。"))
chief("chief-game-test", C("holding a game controller out towards the viewer with an inviting smile"),
      c("還有一個實驗：兩個人看一模一樣的開車遊戲畫面，"), c("一個自己玩，一個看錄下來的影片。"))
kid("kid-game-guess", K("holding a game controller up proudly with a confident grin", where=HOME),
    k("自己玩的，", "很有把握"), k("比較不暈？", "句尾上揚", "S:game"))
chief("chief-game", C("giving a small thumbs-up with a pleased smile", close=True),
      c("猜對了，自己開的人比較少說會暈。", None, "P:game"), c("就算車子只在螢幕裡，能控制還是有差。"))
kid("kid-carscreen-q", K("holding up a small plain tablet in the back seat and pointing at it with a bright idea face", where=CAR),
    k("那在車上，", "靈機一動"), k("用螢幕播前面的路呢？", "句尾上揚", "S:carscreen"))
chief("chief-carscreen", C("holding up one finger with a curious smile", close=True),
      c("那個遮眼睛的英國實驗，真的試過。"))
obj("tablet-road", "Close-up of a small plain tablet mounted on the back of a car's front seat, showing a live picture of the sunny mountain road ahead, soft car interior around it",
    c("螢幕即時播前面的路，結果，並沒有比較不暈。", None, "P:carscreen"))
kid("kid-huh", K("blinking with a baffled open mouth", close=True, where=CAR),
    k("咦，沒用耶！", "驚訝"))
chief("chief-unknown-view", C("spreading her hands with an honest shrug and a kind smile"),
      c("研究的人自己也說，還要再弄清楚，"), c("畫面裡哪些東西會讓人暈，哪些能讓人不暈。"))
chief("chief-boundary", C("holding her two hands apart as if measuring something, an honest thoughtful smile", close=True),
      c("這就是這個解釋的界線：它說得出哪裡對不上，"), c("卻還不能每次準準地說，誰會暈、暈多少。"))
kid("kid-differ-q", K("looking back over her shoulder towards the front seat with a wondering face", where=CAR),
    k("那為什麼同一台車，", "追問"), k("有人很會暈，"), k("有人一點都不會？", "章尾停住，句尾上揚", "S:differ"))

# ---------- 第四章：最會暈和最不會暈，差了一萬倍 ----------
chief("chief-first-unknown", C("holding up one finger with a serious kind smile", close=True),
      c("這個問題，研究也還沒完全解開。", "接住上一句"), chapter="最會暈和最不會暈，差了一萬倍")
chief("chief-range", C("spreading her arms very wide apart with an amazed smile"),
      c("研究暈車幾十年的科學家估計，最會暈和最不會暈的人，"), c("暈的程度可以差到一萬倍。"))
kid("kid-wow", K("throwing both hands up with wide amazed eyes", close=True, where=HOME),
    k("一萬倍！", "驚訝"))
chief("chief-age", C("holding one hand low and then raising it with a friendly smile"),
      c("美國疾病管制中心整理過：兩歲以下的小孩，通常不太會暈；"))
obj("kids-shoes-row", "Close-up of a neat row of children's shoes on a sunny doorstep, from tiny baby shoes to bigger school sneakers to grown-up walking shoes",
    c("之後越來越容易，七到十二歲最容易，再慢慢變少。"))
kid("kid-eight", K("holding up eight fingers with a surprised realising face", where=HOME),
    k("我八歲耶！", "恍然"))
chief("chief-women", C("nodding with a gentle smile, one hand open", close=True),
      c("對，你剛好在那個年紀。"))
obj("twin-shoes", "Close-up of two identical pairs of small yellow children's sneakers standing side by side on a sunny doorstep",
    c("雙胞胎研究還發現，誰比較會暈，很大一部分跟遺傳有關。"))
kid("kid-which-part", K("tapping her own head with one finger and a curious frown", close=True, where=HOME),
    k("有一部分是天生的？", "追問，句尾上揚"))
chief("chief-dunno", C("shaking her head slowly with an honest kind smile", close=True),
      c("有一部分是。可是到底差在哪裡，研究還不清楚。", None, "P:differ"))
obj("coach-again", "Wide shot of a big friendly round-nosed tour coach parked at a sunny rest stop beside green hills, its door open",
    c("那份遊覽車調查也看到：年紀越大、越常坐車的人，越少暈。"))
kid("kid-vomit-q", K("holding both hands over her tummy with a queasy face", where=CAR),
    k("為什麼偏偏是想吐？", "追問，句尾上揚", "S:vomit"))
chief("chief-second-unknown", C("holding up two fingers with a serious kind smile", close=True),
      c("老實說，還沒有人知道。說得出它怎麼被引起，"), c("卻說不出，身體為什麼要用想吐來反應。"))
chief("chief-poison", C("holding up a small green leaf between two fingers and studying it with a thoughtful smile"),
      c("有人提過一個猜法：有些毒會讓感覺亂掉，"), c("身體乾脆吐掉比較保險，暈車是不小心被晃動觸發了。"))
kid("kid-ate-wrong", K("covering her mouth with both hands and wide surprised eyes", close=True, where=HOME),
    k("我吃壞東西了？", "驚訝，句尾上揚"))
chief("chief-poison-limit", C("raising one hand with an honest careful smile", close=True),
      c("這只是一個猜法。有證據支持它，也有證據跟它對不上，"), c("所以為什麼偏偏是想吐，答案還是：不知道。", None, "P:vomit"))
kid("kid-neuron-q", K("pointing at her own forehead with a curious face", close=True, where=HOME),
    k("那大腦裡，", "追問"), k("有負責吵架的地方嗎？", "句尾上揚", "S:neuron"))
chief("chief-neurons", C("holding a clear plastic cup of water still in one hand and pointing at it with the other, a thoughtful smile"),
      c("猴子的腦裡有一群細胞，被別人帶著動時，反應特別大；"), c("自己動的時候，它們就比較安靜。"))
chief("chief-neuron-limit", C("tilting her head with an honest thoughtful smile", close=True),
      c("研究的人推測，大腦可能就是在這裡比對、找不同。"), c("可是它們怎麼讓人想吐，還沒找到。", None, "P:neuron"))
kid("kid-final-q", K("holding " + COMIC + " on her lap and looking straight ahead with a thinking face", where=CAR),
    k("所以我看漫畫會暈，", "推理"), k("到底是怎麼回事？", "章尾停住，句尾上揚"))

# ---------- 收尾 ----------
chief("chief-your-turn", C("leaning forward with an inviting grin, one hand open towards the viewer"),
      c("你自己說說看，從你的漫畫，到那杯水。", "笑"), chapter="快到阿嬤家，小問想通了")
kid("kid-got-it", K("holding " + COMIC + " up proudly with a big confident grin", where=CAR),
    k("原來如此！", "恍然大悟"), k("就像那杯水：眼睛跟耳朵說的不一樣，", "篤定"))
kid("kid-got-it-2", K("pretending to turn a big steering wheel with both hands and laughing", where=HOME),
    k("大腦一對不上，", "篤定"), k("我就暈了！", "篤定", "P:main"), k("還記得爸爸？他先知道要轉彎，"), k("所以他不暈！"))
chief("chief-opinion", C("smiling with her hands clasped, a thoughtful look", close=True),
      c("說得好。還記得一開始我說，會暈代表它一直在工作嗎？", "笑"), c("我覺得最好玩的是：你的身體一直很認真在算你怎麼動。"))
obj("grandma-house", "Wide shot of a small family car parked in front of a cosy old Taiwanese brick farmhouse with a red-tiled roof, potted plants and green hills, sunny afternoon",
    k("到阿嬤家了！", "開心"))
# The outro is three pictures, no card, no stamp (series README §3.2, §10.1): the kid gives a thumbs-up.
kid("outro", "Waist-up medium shot of the girl with a big happy smile giving a big cheerful thumbs-up with one hand, bright morning light",
    k("我要先去找阿嬤！", "開心大聲"))
chief("outro-chief", "Waist-up medium shot of the chief holding up a clear plastic cup of water with a curious smile, filling the frame, a plain pale wall behind her, bright morning light",
      c("你坐車或看什麼的時候，最容易暈？", "問句上揚，像聊天"), c("留言告訴我們。"))
chief("outro-wave", "Waist-up medium shot of the chief waving goodbye with a warm smile, a plain pale wall behind her, bright morning light",
      c("想一起找生活裡的為什麼，就訂閱原來如此事務所。", "誠懇"))

# ---------- assemble ----------
WHAT = {"main": "坐車看漫畫，頭暈肚子怪，到底怎麼了", "dad": "爸爸開同一台車，為什麼一點事都沒有",
        "blind": "遮住眼睛坐車，會不會暈", "sofa": "坐在沙發上不動，只看賽車畫面會不會暈",
        "broken": "會暈車是不是內耳不好", "ear": "內耳到底在做什麼",
        "eyes": "眼睛也會告訴大腦嗎", "liar": "看漫畫時，是誰在說謊",
        "close": "閉上眼睛是不是就不會吵", "who": "眼睛閉起來了，還在跟誰吵",
        "window": "看窗外會不會比較好", "reverse": "反過來，眼睛說在動、身體說沒動會怎樣",
        "vection": "沒在動，為什麼會覺得在動", "game": "自己玩和看錄影，誰比較不暈",
        "carscreen": "在車上用螢幕播前面的路，會不會比較不暈", "differ": "為什麼同一台車有人很會暈、有人不會",
        "vomit": "對不上，為什麼偏偏是想吐", "neuron": "大腦裡有沒有負責比對的地方"}
scenes, loops_s, loops_p, n, beats = [], {}, {}, 0, 0
for sc in S:
    lines = []
    for sp, text, emo, tag in sc["lines"]:
        n += 1; lid = f"p{n:03d}"
        line = {"id": lid, "speaker": sp, "text": text}
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
    "series": {"slug": "sothatswhy", "episode": 21, "chapter": 1},
    # 2026-11-11 (README §9 停頓, §10.6): no fixed pause between lines, a short gap between scenes, beat-timed stills.
    "pauses": {"line_ms": 0, "scene_ms": 150},
    "still_motion": "beat",
    # The series bed from P15 on (explainer-series/README.md, PR #2048): sothatswhy-bed-r2.m4a, remade from P02's paid take.
    "music": {"track": "sothatswhy-bed-r2.m4a", "sha256": "9bb4ba6fd16feb4a7f352144b2d89e9648acbbbbaa2173c27a7eefbdb70f28c6", "gain_db": -20, "duck_db": -10},
    "characters": CHARACTERS, "loops": loops,
    "youtube": {
        "category_id": 27, "made_for_kids": False, "default_language": "zh-TW",
        "title": "坐車看書，為什麼容易暈？｜原來如此事務所",
        "description": "小問在去阿嬤家的山路上看漫畫，看到一半頭暈暈、肚子怪怪的；可是在前面開車的爸爸，一點事都沒有。同一台車、同一條路，為什麼只有她在暈？\n\n"
                       "這一集，所長和小問跟著同一趟車走，手上只有一杯水當線索：看漫畫的時候，到底是誰在說謊？遮住眼睛坐車，會不會就不暈？"
                       "坐在沙發上一動也不動、只看賽車畫面，為什麼也有人會暈？最後也老實交代，科學到現在還回答不了的事：為什麼每個人差這麼多、為什麼偏偏是想吐。\n\n"
                       "本集只介紹研究看到的現象與目前的解釋，不是醫療建議；插圖由 AI 生成，是示意，不是人體構造圖。每個說法的出處列在下方參考資料。\n\n資料截至 " + CHECKED,
        "tags": ["暈車", "暈動症", "內耳", "平衡", "感覺衝突", "科普", "原來如此事務所"]},
    "thumbnail": {"template": "thumb", "data": {"headline": "看漫畫\n**就暈車？**", "sub": "開車的爸爸卻沒事？", "shot": "kid-reading-open", "subject": "right"}},
    "sources": [
        {"title": "CDC Yellow Book 2026, Motion Sickness (John F. Golding; updated 2025-04-23)", "url": "https://www.cdc.gov/yellow-book/hcp/travel-air-sea/motion-sickness.html", "checked_on": CHECKED},
        {"title": "NHS, Motion sickness (reviewed 2023-06-19)", "url": "https://www.nhs.uk/conditions/motion-sickness/", "checked_on": CHECKED},
        {"title": "Cleveland Clinic, Motion Sickness (updated 2024-04-08)", "url": "https://my.clevelandclinic.org/health/diseases/12782-motion-sickness", "checked_on": CHECKED},
        {"title": "NIDCD (NIH), Balance Disorders", "url": "https://www.nidcd.nih.gov/health/balance-disorders", "checked_on": CHECKED},
        {"title": "Lackner (2014), Motion sickness: more than nausea and vomiting, Exp Brain Res 232:2493", "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC4112051/", "checked_on": CHECKED},
        {"title": "Golding (2006), Motion sickness susceptibility, Auton Neurosci 129:67", "url": "https://pubmed.ncbi.nlm.nih.gov/16931173/", "checked_on": CHECKED},
        {"title": "Golding (2016), Motion sickness, Handb Clin Neurol 137:371", "url": "https://pubmed.ncbi.nlm.nih.gov/27638085/", "checked_on": CHECKED},
        {"title": "Griffin & Newman (2004), Visual field effects on motion sickness in cars, Aviat Space Environ Med 75:739", "url": "https://pubmed.ncbi.nlm.nih.gov/15460624/", "checked_on": CHECKED},
        {"title": "Turner & Griffin (1999), Motion sickness in public road transport, Ergonomics 42:444", "url": "https://pubmed.ncbi.nlm.nih.gov/10048305/", "checked_on": CHECKED},
        {"title": "Kuiper, Bos & Diels (2018), In-vehicle auxiliary display positioning affects carsickness, Appl Ergon 68:169", "url": "https://pubmed.ncbi.nlm.nih.gov/29409631/", "checked_on": CHECKED},
        {"title": "Rolnick & Lubow (1991), Why is the driver rarely motion sick?, Ergonomics 34:867", "url": "https://pubmed.ncbi.nlm.nih.gov/1915252/", "checked_on": CHECKED},
        {"title": "Kuiper et al. (2020), Anticipatory audio cues can mitigate motion sickness, Appl Ergon 85:103068", "url": "https://pubmed.ncbi.nlm.nih.gov/32174356/", "checked_on": CHECKED},
        {"title": "Keshavarz, Riecke, Hettinger & Campos (2015), Vection and visually induced motion sickness: how are they related?, Front Psychol 6:472", "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC4403286/", "checked_on": CHECKED},
        {"title": "Dong, Yoshida & Stoffregen (2011), Control of a virtual vehicle influences postural activity and motion sickness, J Exp Psychol Appl 17:128", "url": "https://pubmed.ncbi.nlm.nih.gov/21604911/", "checked_on": CHECKED},
        {"title": "Reavley et al. (2006), Genetic influences on motion sickness susceptibility in adult women: a classical twin study", "url": "https://pubmed.ncbi.nlm.nih.gov/17086768/", "checked_on": CHECKED},
        {"title": "Treisman (1977), Motion sickness: an evolutionary hypothesis, Science 197:493", "url": "https://pubmed.ncbi.nlm.nih.gov/301659/", "checked_on": CHECKED},
        {"title": "Oman (2012), Are evolutionary hypotheses for motion sickness \"just-so\" stories?, J Vestib Res 22:117", "url": "https://pubmed.ncbi.nlm.nih.gov/23000611/", "checked_on": CHECKED},
        {"title": "Stoffregen & Smart (1998), Postural instability precedes motion sickness, Brain Res Bull 47:437", "url": "https://pubmed.ncbi.nlm.nih.gov/10052572/", "checked_on": CHECKED},
        {"title": "Oman & Cullen (2014), Brainstem processing of vestibular sensory exafference, Exp Brain Res 232:2483", "url": "https://pubmed.ncbi.nlm.nih.gov/24838552/", "checked_on": CHECKED},
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
print(f"scenes {len(scenes)} shots {len(scenes)} lines {n} chars {chars} (body {body_chars}, body Han {body_han}) kid {kidc / chars:.0%} of chars, "
      f"{sum(l['speaker'] == 'kid' for l in lines_all) / n:.0%} of lines; est {est / 60:.1f} min at {RATE}/s "
      f"(+{len(scenes) - 1} scene gaps, {beats} beats, before the 11.9 s intro); loops {len(loops)}", file=sys.stderr)
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
