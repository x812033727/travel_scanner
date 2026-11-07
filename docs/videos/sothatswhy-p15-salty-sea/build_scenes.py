"""Generate video.json for sothatswhy-p15-salty-sea (原來如此事務所 對話版 P15).

Run `python3 build_scenes.py` from anywhere: it rewrites video.json next to this file and freezes
every shot's camera move in cameras.json (a shot keeps the camera it was first given, so deleting
a shot never shifts the others: the camera is in the keyframe cache key).
Edit lines and prompts here, never in video.json.
"""
import itertools, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = "sothatswhy-p15-salty-sea"
CHECKED = "2026-11-07"

# ---------- series constants ----------
# Both characters' `appearance` stay word for word as in P07/P08/P14: the series sheets are keyed by it
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
BEACH = "on a sunny sandy beach with gentle blue waves behind her"
RIVERMOUTH = "on a sunny grassy riverbank where a calm river flows into the blue sea behind her"
KITCHEN = "in a bright sunny home kitchen"
POT = "a big plain smooth steel soup pot"
# One drawing language for the whole episode (README §10.5: numbers as feelings, one metaphor throughout):
# the sea is a pot of soup that never stops simmering. Rivers add water carrying a little salt (tiny glittering
# specks), the sun is the fire that boils only the water away (soft wisps rising), the seafloor is the crust at the
# bottom of the pot that takes salt out. Nothing is counted, nothing depends on direction, no scale, no gauge.
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
# Round 2 (2026-11-07): rewritten after the blind panel (no_toc, no_recap, no_detour, no_orphans), the script score
# and verify-1.md (F01-F07). One metaphor only: the sea is a pot of soup that never stops simmering.
kid("kid-splash", K("laughing and squinting as a small splash of sea water hits her, standing in shallow waves", where=BEACH),
    k("所長！我昨天去海邊玩，", "興奮，跑進來報案的語氣"), k("被浪打到，喝了一口海水！", "好笑又委屈"), chapter="一口海水，一條河")
kid("kid-salty-face", K("sticking out her tongue with a scrunched-up salty face, eyes squeezed shut as two happy curved lines", close=True, where=BEACH),
    k("好鹹好鹹！", "皺臉"))
chief("chief-me-too", C("laughing warmly with a hand on her chest", close=True),
      c("哈，那一口我也喝過，", "笑"), c("鹹得整張臉都皺起來。"))
scene("river-into-sea", "Wide view from a grassy hill of a calm blue river winding across green fields and flowing into the wide blue sea, " + DAY,
      k("可是回家的路上，我看到一條河，", "轉折"), k("一直一直流進海裡。"))
kid("kid-river-q", K("pointing at the river behind her with a puzzled frown", where=RIVERMOUTH),
    k("河水是淡的耶，", "不解"), k("海怎麼沒有被沖淡？", "句尾上揚"))
scene("chief-main-q", "Wide view of many little rivers running down from green mountains on every side into one big sparkling blue sea, sunny sky, " + DAY,
      c("好問題。全世界的河，每天都把好多淡水倒進海裡，", "接住她的問題"), c("可是你去海邊嘗到的海，從來沒有變淡過。", "轉向觀眾"))
kid("kid-salt-mountain", K("spreading her arms wide with an excited know-it-all grin", close=True),
    k("我知道！", "搶答"), k("海底有一座鹽山，一直在冒鹽！", "很有把握的錯猜", "S:mountain"))
chief("chief-no-mountain", C("shaking her head gently with a warm amused smile"),
      c("鹽山？", "笑"), c("不過海底真的藏著一個祕密，等一下告訴你。", "賣關子", "S:secret"))
scene("river-glass", "Close-up of a clear glass of fresh river water standing on a mossy rock beside a sparkling mountain stream, " + DAY,
      c("還有，你說河水是淡的，"), c("它真的一點鹽都沒有嗎？", "賣關子", "S:riversalt"))
scene("soup-promise", "Medium shot of " + POT + " simmering on a stove in a bright sunny kitchen, soft steam rising, a small bowl of white salt beside it, " + DAY,
      c("我們把整片海，想成一鍋一直在熬的湯。"), c("一直加淡水的湯，為什麼還是鹹的？", "問句", "S:main"))

# ---------- 第一章：河水裡偷偷藏著一點鹽 ----------
scene("mountain-rain", "Wide view of soft rain falling on big grey rocks on a green mountainside, little streams trickling between the rocks, gentle daylight",
      c("其實河水身上，偷偷帶著鹽。", "接住上一句"), chapter="河水裡偷偷藏著一點鹽")
kid("kid-river-zero", K("holding a clear cup of water up to the light and peering into it with a doubtful face", close=True, where="on a sunny riverbank"),
    k("可是喝起來淡淡的啊！", "不服氣"))
chief("chief-a-little", C("pinching her thumb and finger close together to show a tiny amount, a kind smile", close=True),
      c("因為非常非常少，", None, "P:riversalt"), c("少到你嘗不出來。"))
scene("rain-bites", "Close-up of raindrops splashing on a big rough grey rock, tiny sparkly specks washing off the rock into a little trickle of water, " + DAY,
      c("那些鹽，是從山上的石頭來的。"), c("雨水帶著一點點酸，一年一年，慢慢地啃石頭。"))
kid("kid-rain-bite", K("staring wide-eyed at a big rock in soft rain, holding a small yellow umbrella", where="on a green mountain trail"),
    k("雨會啃石頭？", "驚訝"))
scene("rock-dissolve", "Close-up of a rough grey stone under soft rain, its corners worn smooth and round, tiny glittering specks drifting away in the water, " + DAY,
      c("對，啃得非常慢，要好多好多年。"), c("石頭裡有一些小小的東西，就這樣被溶進水裡。"))
scene("river-sparkle", "Medium shot of a clear mountain river flowing over smooth round pebbles, tiny glittering specks floating inside the water, " + DAY,
      c("這些看不見的小東西，就跟著河水一路流下山。"))
kid("kid-sugar", K("stirring a spoon in a clear glass of water with a thinking face", close=True, where=KITCHEN),
    k("就像糖溶在水裡，", "推理"), k("看不見了？", "句尾上揚"))
chief("chief-sugar", C("nodding with one finger raised, a gentle smile"),
      c("對，看不見，也嘗不太出來。"), c("其中有一些，就是廚房那種鹽的材料。"))
kid("kid-why-fresh", K("crouching by a clear stream and dipping one hand in the water", where="on a sunny riverbank"),
    k("那鹽不會在河裡越積越多嗎？", "句尾上揚"))
scene("rain-refill", "Wide view of soft rain falling on a green valley and filling a winding river with fresh clear water, " + DAY,
      c("因為雨一直下，河水一直被新的雨水換掉，"), c("鹽還來不及變多，就被帶進海裡了。"))
scene("fresh-vs-sea", "Medium shot of two glasses of water on a sunny wooden table, one clear and light with only a faint sparkle, the other thick with glittering white sparkles, " + DAY,
      c("我們叫淡水的那種水，裡面的鹽，"), c("連海水的三十分之一都不到。"))
kid("kid-tiny", K("holding up a single tiny grain of salt on her fingertip and frowning at it", close=True, where=KITCHEN),
    k("這麼一點點，", "懷疑"), k("怎麼可能讓整片海變鹹？", "句尾上揚", "S:howsmall"))
scene("all-rivers", "Wide view of a huge sparkling blue sea with many rivers flowing into it from green land all around, every river glittering with tiny specks, " + DAY,
      c("可是你想想，全世界的河一起倒，", "轉向觀眾"), c("一年加起來，大約會帶四十億公噸溶掉的鹽進海裡。"))
kid("kid-billion", K("throwing both hands up with her mouth open in amazement", close=True),
    k("四十億公噸！", "驚呼"))
chief("chief-years", C("smiling and opening both hands wide"),
      c("一點點，乘上很多很多河、很多很多年，"), c("就不是一點點了。"))
scene("salt-blanket", "Wide view of green land covered by a huge thick soft white layer of salt as tall as a tall building, a few tiny houses beside it, " + DAY,
      c("現在海裡的鹽，多到如果全部撈上來，鋪在陸地上，"), c("會有大約四十層樓那麼厚。"))
kid("kid-40", K("stretching up on tiptoe with one arm reaching high above her head, an amazed face"),
    k("一點點，", "恍然"), k("原來會變這麼多！", "驚呼", "P:howsmall"))
kid("kid-overflow", K("standing at the water's edge watching the waves, scratching her head", where=BEACH),
    k("可是河一直把水倒進去，", "不解"), k("海不是應該越來越滿、越來越淡嗎？", "句尾上揚", "S:fuller"))

# ---------- 第二章：太陽只搬走水，搬不走鹽 ----------
chief("chief-full", C("raising her eyebrows with a curious smile, one finger on her chin"),
      c("河一直在倒水，這沒錯，", "接住上一句"), c("可是海從來沒有滿出來。"), chapter="太陽只搬走水，搬不走鹽")
scene("ocean-fill", "Wide view of a calm endless blue sea meeting the sky at the far horizon under a bright sun, " + DAY,
      c("如果海是空的，光靠全世界的河來倒，"), c("大約三萬多年就倒滿了。"))
kid("kid-drain", K("crouching and peering down into the shallow sea water as if looking for a hole", where=BEACH),
    k("是不是海底有一個排水孔？", "錯猜", "S:drain"))
chief("chief-up", C("pointing one finger up toward the sky with a smile"),
      c("水的出口，不在海底，在天上。", None, "P:fuller"))
scene("sun-sea", "Wide view of the bright sun shining over a calm blue sea, soft wavy wisps of warm vapour rising gently from the water surface, " + DAY,
      c("太陽一曬，海面上的水，"), c("就慢慢變成看不見的水氣，飛上天空。"))
scene("cloud-rain", "Wide view of puffy white clouds drifting from the sea over green mountains and raining softly on them, a river running back down to the sea, " + DAY,
      c("水氣變成雲，下成雨，有的直接下回海上，"), c("有的下到山上，再從河裡流回海。"))
kid("kid-circle", K("drawing a big circle in the air with one finger, a delighted face", close=True),
    k("水在繞圈圈！", "恍然"))
kid("kid-salt-fly", K("looking up at the sky with a puzzled face, one hand shading her eyes", where=BEACH),
    k("那鹽也跟著飛上天了嗎？", "句尾上揚", "S:saltfly"))
chief("chief-cant-lift", C("shaking her head with a calm smile, both hands open"),
      c("沒有。太陽只搬得動水，"), c("搬不動鹽。"))
kid("kid-rain-fresh", K("standing in light rain catching raindrops in her open hands, a happy face", where="on a green grassy field"),
    k("所以雨不是鹹的！", "恍然", "P:saltfly"))
chief("chief-rain-proof", C("nodding warmly with a proud smile", close=True),
      c("對，你淋到的雨，幾乎就是被太陽熬出來的淡水。"))
kid("kid-plate", K("carefully setting a small plain white plate of water on a sunny windowsill", where=KITCHEN),
    k("那我也可以在家曬一碟鹽水？", "句尾上揚"))
chief("chief-plate", C("holding a small plain white plate with a thin white ring of salt on it, a pleased smile"),
      c("可以。放在太陽下幾天，"), c("水不見了，碟子上就剩一圈鹽。"))
kid("kid-soup", K("standing on tiptoe to look into " + POT + " simmering on the stove", where=KITCHEN),
    k("就像媽媽熬湯！", "恍然"), k("湯越熬越少，也越熬越鹹！", "開心"))
scene("soup-pot", "Close-up of " + POT + " simmering on a stove, soft steam rising away from the soup, a faint ring on the inside of the pot where the soup used to reach, " + DAY,
      c("對，海就是這樣一鍋湯。"), c("河水是一直加進去、帶著一點點鹽的水，"), c("太陽就是爐火。"))
kid("kid-all-salt", K("hugging her knees and looking worried at the sea", where=BEACH),
    k("那海每天被熬，", "擔心"), k("最後不就變成一大片鹽巴？", "句尾上揚", "S:allsalt"))
chief("chief-guest", C("tilting her head with a thoughtful smile"),
      c("你先別急。你看，水在這鍋湯裡，只待一下子。"))
scene("drop-guest", "Close-up of one shiny clear water drop sparkling in warm sunshine above a calm blue sea, " + DAY,
      c("一滴水在海裡，平均待個三千年左右，"), c("就被太陽熬走了。"))
scene("salt-stay", "Close-up of tiny glittering white salt sparkles resting in calm deep blue sea water, soft sunbeams from above, " + DAY,
      c("鹽卻可以在湯裡，泡上幾千萬年。"))
kid("kid-3000", K("counting on her fingers with a wide-eyed face", close=True),
    k("三千年已經好久了！", "驚訝"))
chief("chief-3000", C("smiling gently with one hand raised a little"),
      c("可是跟鹽比，水只是在鍋裡轉一圈。"))
chief("chief-move", C("raising one finger with a mysterious smile", close=True),
      c("不過，鹽也不是永遠留在湯裡。", "賣關子"))
kid("kid-where-go", K("leaning forward with wide curious eyes", close=True),
    k("那鹽最後去哪裡？", "句尾上揚", "S:exit"))

# ---------- 第三章：鍋底偷偷把鹽收走 ----------
scene("seafloor", "Wide underwater view of a calm sandy seafloor deep in the blue sea, soft sunbeams fading from above, a few small fish",
      c("鹽的出口，在鍋底，還有鍋邊。", "接住上一句", "P:exit"), c("這就是我一開始說的那個祕密。", None, "P:secret"), chapter="鍋底和鍋邊，偷偷把鹽收走")
scene("mud-layers", "Cutaway view of the seafloor showing soft layers of mud and sand stacked like a layered cake, tiny glittering specks settling down onto the top layer, blue sea above",
      c("海水裡溶著的一些東西，會慢慢沉下去，"), c("跟泥沙一起，變成海底一層一層的泥和石頭。"))
kid("kid-crust", K("pointing at the inside bottom of " + POT + " with a surprised face", close=True, where=KITCHEN),
    k("就像鍋底的鍋巴！", "恍然"))
chief("chief-crust", C("laughing warmly and nodding"),
      c("對，這鍋湯也會結鍋巴。"), c("你下次刷鍋子，就會想起海底。", "轉向觀眾，笑"))
scene("shells", "Close-up of colourful seashells and a small pink coral on the sandy seafloor, tiny drifting plankton dots in the clear blue water",
      c("還有貝殼和珊瑚，"), c("會把水裡做殼的材料，拿去蓋自己的家。"))
kid("kid-shell-home", K("holding a big seashell up next to her ear with a curious smile", close=True, where=BEACH),
    k("貝殼的家，是用海水蓋的？", "句尾上揚"))
scene("shells-sink", "Medium underwater view of empty seashells resting on the soft sandy seafloor, half buried in the sand, blue water above",
      c("對。牠們死掉以後，殼就留在海底，"), c("那些材料，也就離開了海水。"))
kid("kid-shell-help", K("holding a small seashell in her open palm with a bright face", close=True, where=BEACH),
    k("貝殼在幫海搬東西！", "恍然"))
scene("river-mix", "Medium shot of a river flowing into the sea, the river water carrying glittering golden specks and the sea water full of white sparkles, " + DAY,
      c("河水帶來的，有很多正是做殼的材料，"), c("被拿走得比鹽快很多。"))
kid("kid-why-not-salt", K("tilting her head with a puzzled frown, one finger on her chin", close=True),
    k("那為什麼不把鹽也拿走？", "句尾上揚"))
chief("chief-table-salt", C("holding up a small bowl of white salt with a smile", close=True),
      c("因為做殼用不到廚房那種鹽。"), c("所以留在海裡最多的，就是它。"))
scene("salt-crystal", "Close-up of a few clear square white salt crystals sparkling on a dark blue plate, " + DAY,
      c("海水裡溶著的小東西，一百份裡，"), c("大約有八十五份，都是廚房那種鹽的材料。"))
scene("vents", "Wide underwater view of a dark rocky seafloor with a tall rocky chimney puffing warm shimmering water and dark smoky clouds",
      c("鍋底還有一個會冒泡的地方：很燙的熱泉。"), c("海水鑽進石頭縫裡，被煮熱了再噴出來。"))
scene("vents-all", "Wide underwater view of a long dark seafloor ridge with several small rocky chimneys puffing shimmering water, blue sea above",
      c("科學家估計，全世界的海水大約一千到兩千萬年，"), c("就會從熱泉的石頭縫裡，整個鑽過一次。"))
kid("kid-mountain-right", K("gasping with a big surprised open mouth, both hands out of frame", close=True),
    k("那熱泉會冒出鹽嗎？", "句尾上揚"))
chief("chief-half-right", C("smiling and giving a small nod"),
      c("會冒出一些。你一開始說的鹽山，說對了一點點。", None, "P:mountain"))
scene("vent-swap", "Close-up of a rocky seafloor chimney with warm shimmering water swirling around it, tiny golden specks drifting out and tiny white specks sinking into the rock, blue water around",
      c("熱泉會帶出石頭裡的一些金屬，"), c("也會把海水裡的一些東西，留在石頭裡。"))
kid("kid-more-exit", K("leaning forward with both hands out of frame and curious eyes", close=True),
    k("那廚房那種鹽，要怎麼出去？", "句尾上揚", "S:saltexit"))
chief("chief-salt-exit", C("pointing down with one finger and a knowing smile"),
      c("它要從鍋邊出去，就像湯熬乾時，鍋邊那一圈鹽。"))
scene("ancient-salt", "Cutaway view of the ground showing a thick shiny white layer of salt buried deep under brown rock, green fields and a few small trees on top, " + DAY,
      c("很久很久以前，有些海灣跟大海隔開了，", None, "P:saltexit"), c("裡面的海水被曬乾，留下厚厚的鹽層，埋進地底下。"))
kid("kid-balance", K("holding both hands out flat at the same height, a thinking face"),
    k("所以河送進來的鹽，", "推理"), k("海也一直在收？", "句尾上揚"))
chief("chief-two-exits", C("holding up two fingers with a warm smile"),
      c("對，只是收得很慢。還記得你找的排水孔嗎？", "點名回呼"), c("水的出口在天上，鹽的出口在鍋底和鍋邊。", None, "P:drain"))
scene("balance-pot", "Close-up cutaway of " + POT + " simmering gently, a thin pale crust growing on its inside bottom, soft steam rising, " + DAY,
      c("一邊加一點鹽，一邊結一點鍋巴。"))
chief("chief-steady", C("folding her hands calmly with a gentle smile"),
      c("所以你問，海會不會變成一大片鹽巴？", "點名回呼"), c("海洋學家認為，現在的海，大概已經沒有再越變越鹹了。", None, "P:allsalt"))
kid("kid-same-q", K("looking out at the sea with one hand on her hip, a curious face", where=BEACH),
    k("那全世界的海，", "好奇"), k("都一樣鹹嗎？", "句尾上揚", "S:same"))

# ---------- 第四章：每一鍋湯，鹹度不一樣 ----------
scene("globe", "Wide view of a calm blue sea stretching far away under a bright sky with a few small green islands, " + DAY,
      c("不太一樣。整片海平均起來，", "接住上一句"), c("一公斤海水，大約有三十五公克的鹽。"), chapter="每一鍋湯，鹹度不一樣")
kid("kid-connected", K("spreading both arms wide with a confident face", where=BEACH),
    k("海都是連在一起的，", "很有把握的錯猜"), k("應該都一樣鹹吧！"))
chief("chief-recipe", C("holding up one finger with a warm smile"),
      c("連在一起，可是每個地方的火和水，不一樣。"))
chief("chief-guess-taiwan", C("leaning a little toward the viewer with a playful smile", close=True),
      c("有的海熬得特別兇，有的海一直在加水。"), c("你先猜猜，台灣旁邊的海，比較像哪一種？", "轉向觀眾", "S:taiwan"))
kid("kid-guess", K("tapping her chin with one finger and squinting in thought", close=True, where=BEACH),
    k("熬得很兇的那種？", "猜"))
chief("chief-later", C("smiling with a small playful shrug"),
      c("先別急，我們先去一片很熱的海看看。", "賣關子"))
scene("red-sea", "Wide view of a hot dry desert coast with bare sandy mountains beside a deep blue sea under a blazing sun, heat shimmer, " + DAY,
      c("像紅海，旁邊幾乎都是沙漠，太陽很大，"), c("很少下雨，也幾乎沒有河流進來。"))
kid("kid-fire-up", K("fanning her face with one hand on a hot sunny day, squinting", where=BEACH),
    k("爐火開大，又不加水！", "恍然"))
scene("red-sea-salty", "Close-up of sparkling white salt crystals along a rocky shore of a deep blue sea under a hot sun, " + DAY,
      c("熬得兇，紅海就比較鹹，"), c("每一公斤，比平均多了大約五公克的鹽。"))
kid("kid-fresh-sea-q", K("cupping both hands around her mouth as if calling out across the sea", where=BEACH),
    k("那有沒有很淡很淡的海？", "句尾上揚"))
scene("baltic", "Wide view of a cool cloudy northern sea with dark green pine forests on the shores and several rivers flowing into it, soft pale daylight",
      c("北邊的波羅的海剛好相反，"), c("很多河流進來，下的雨也比曬走的多。"))
kid("kid-add-water", K("pouring a cup of water into " + POT + " on the stove with a playful face", where=KITCHEN),
    k("一直加水，湯就淡了！", "恍然"))
scene("baltic-fresh", "Medium shot of calm pale blue water at a quiet northern shore with smooth pebbles and tall reeds, soft pale daylight",
      c("它最北邊的海水，一公斤只有幾公克鹽，"), c("嘗起來淡淡的。"))
scene("river-plume", "Wide aerial view of a big muddy brown river spreading its pale water far out into the deep blue sea, " + DAY,
      c("就連你看到的那條河，流進海的地方，"), c("附近的海水也會淡一點。"))
kid("kid-my-river", K("smiling and pointing back at the river behind her", where=RIVERMOUTH),
    k("我看到的那條河！", "開心"))
kid("kid-taiwan-q", K("pointing out at the blue sea with a curious smile", where=BEACH),
    k("那台灣旁邊的海呢？", "句尾上揚"))
chief("chief-pacific", C("smiling and opening one hand toward the viewer"),
      c("答案是：兩種都不太像。", None, "P:taiwan"), c("台灣附近的海水，平常一公斤大約三十四公克多，"))
chief("chief-taiwan", C("nodding with a gentle smile, one hand open", close=True),
      c("跟整片海的平均差不多。"), c("不過夏天雨多、河水多，"), c("岸邊的海水，就像你看到的河口，會淡一點。"))
kid("kid-saltiest-q", K("standing on tiptoe and shading her eyes with one hand, looking far away", where=BEACH),
    k("那有沒有超級鹹的地方？", "句尾上揚"))
scene("dead-sea", "Wide view of a calm turquoise salty lake with white salt crusts along its shore and bare brown hills around it, bright sun, " + DAY,
      c("有一個很有名的，叫死海。它其實是一個湖，"), c("水流不出去，只能被太陽熬，熬到比海水鹹快十倍。"))
chief("chief-same-thing", C("smiling and pressing her palms together"),
      c("所以，每片海鹹不鹹，看的是什麼呢？", "問句，考考她"))
kid("kid-soup-again", K("tapping the lid of " + POT + " with a spoon, grinning", where=KITCHEN),
    k("看加多少水，熬走多少水！", "篤定", "P:same"))
scene("beach-guess", "Wide view of a sunny Taiwan beach with gentle waves, a small river mouth at one end and green hills behind, " + DAY,
      c("你下次去海邊，也可以猜猜看。", "轉向觀眾"))
scene("waves-opinion", "Close-up of sparkling blue waves rolling gently onto a sunny sandy beach, " + DAY,
      c("我覺得，海最厲害的地方，", "意見，輕鬆"), c("就是它一邊收河送來的鹽，一邊把水送上天，從來沒停過。"))

# ---------- 收尾 ----------
chief("chief-back", C("smiling warmly at the viewer with one hand open, filling the frame", close=True),
      c("還記得你一開始問我的嗎？你自己說說看。", "笑"), chapter="小問自己破案")
kid("kid-got1", K("throwing both arms up with a huge happy smile", where=BEACH),
    k("河水帶一點點鹽進海裡，", "篤定"), k("太陽只把水熬走，", "篤定"))
kid("kid-got2", K("pointing proudly at " + POT + " on the stove with a big grin", close=True, where=KITCHEN),
    k("海底和海邊，再慢慢把鹽收走！", "開心", "P:main"))
chief("chief-safe", C("holding a glass of clear water with a caring smile"),
      c("完全正確！對了，你昨天喝到的那口海水，", "先誇她，再叮嚀"), c("可別拿來解渴。身體要用更多的水排鹽，會越喝越渴。"))
chief("chief-done", C("smiling warmly at the viewer with her hands clasped", close=True),
      c("下次你在海邊被浪打到，嘗到那一口鹹，", "轉向觀眾，輕聲"), c("就知道那是好幾千萬年留下來的味道。", "點名回呼"))
# The outro is three pictures, no card, no stamp (series README §3.2, §10.1): the kid gives a thumbs-up.
kid("outro", "Head-and-shoulders close-up of the girl with a big happy smile giving a big cheerful thumbs-up with one hand, bright morning light",
    k("原來如此！", "開心大聲"))
chief("outro-chief", "Waist-up medium shot of the chief holding a pretty seashell in one hand with a curious smile, filling the frame, a plain pale wall behind her, bright morning light",
      c("你去過的海邊，被浪打到的時候，鹹不鹹？", "問句上揚，像聊天"), c("留言告訴我們。"))
chief("outro-wave", "Waist-up medium shot of the chief waving goodbye with a warm smile, a plain pale wall behind her, bright morning light",
      c("想一起找生活裡的為什麼，就訂閱原來如此事務所。", "誠懇"))

# ---------- assemble ----------
WHAT = {"main": "一直加淡水的湯（海），為什麼還是鹹的", "mountain": "海底是不是有一座一直冒鹽的鹽山",
        "secret": "海底藏著的祕密是什麼", "riversalt": "河水真的一點鹽都沒有嗎",
        "howsmall": "那麼一點點鹽，怎麼可能讓整片海變鹹", "fuller": "河一直倒水，海為什麼沒有越來越滿、越來越淡",
        "drain": "海是不是有一個排水孔", "saltfly": "水被曬走時，鹽有沒有跟著飛上天",
        "allsalt": "海每天被熬，最後會不會變成一大片鹽巴", "exit": "鹽最後去哪裡",
        "same": "全世界的海都一樣鹹嗎", "saltexit": "廚房那種鹽要怎麼離開海",
        "taiwan": "台灣旁邊的海比較像熬得兇的海，還是一直加水的海"}
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
    "series": {"slug": "sothatswhy", "episode": 15, "chapter": 1},
    # The series bed: the same paid Lyria take as P02-P14 (P02 backup music/e4225993d121c03b.mp3), rebuilt on
    # 2026-11-07 with P02's recipe because the original bed file was in no backup (tail cut at 175.15 s,
    # five copies with 3 s crossfades, 863.75 s). Nothing new was generated.
    "music": {"track": "sothatswhy-bed-r2.m4a", "sha256": "9bb4ba6fd16feb4a7f352144b2d89e9648acbbbbaa2173c27a7eefbdb70f28c6", "gain_db": -20, "duck_db": -10},
    "characters": CHARACTERS, "loops": loops,
    "youtube": {
        "category_id": 27, "made_for_kids": False, "default_language": "zh-TW",
        "title": "河水一直流進海裡，海為什麼還是鹹？｜原來如此事務所",
        "description": "小問在海邊被浪打到，喝了一口好鹹的海水；回家路上，她卻看到一條淡淡的河一直流進海裡。全世界的河每天都在倒淡水，海怎麼沒有被沖淡？\n\n"
                       "這一集，所長和小問把整片海想成一鍋一直在熬的湯：先看河水從山上的石頭帶走了一點點鹽，再看太陽為什麼只搬得走水、搬不走鹽，"
                       "最後潛到海底，看貝殼、泥沙、熱泉和古老的鹽層怎麼把海水裡的東西收走，以及為什麼紅海特別鹹、波羅的海卻淡淡的。\n\n"
                       "本集插圖由 AI 生成，畫的是示意，不是量測。片中的鹽度、年數與鹽量都是海洋機關與教材裡的大約數字，每片海、每個季節都會不一樣。"
                       "海水很鹹，請不要喝。每個說法的出處列在下方參考資料。\n\n資料截至 " + CHECKED,
        "tags": ["海水", "為什麼海是鹹的", "鹽度", "水循環", "七股鹽山", "科普", "原來如此事務所"],
        "video_id": None},
    "thumbnail": {"template": "thumb", "data": {"headline": "河水一直倒\n**海還是鹹**", "sub": "太陽只搬走水，搬不走鹽", "shot": "kid-salty-face"}},
    "sources": [
        {"title": "NOAA Ocean Service: Why is the ocean salty?", "url": "https://oceanservice.noaa.gov/facts/whysalty.html", "checked_on": CHECKED},
        {"title": "NOAA Ocean Service: Why are rivers not salty?", "url": "https://oceanservice.noaa.gov/facts/riversnotsalty.html", "checked_on": CHECKED},
        {"title": "NOAA Ocean Service: Can humans drink seawater?", "url": "https://oceanservice.noaa.gov/facts/drinksw.html", "checked_on": CHECKED},
        {"title": "USGS Water Science School: Why is the ocean salty?", "url": "https://www.usgs.gov/special-topics/water-science-school/science/why-ocean-salty", "checked_on": CHECKED},
        {"title": "USGS Water Science School: Saline water and salinity", "url": "https://www.usgs.gov/special-topics/water-science-school/science/saline-water-and-salinity", "checked_on": CHECKED},
        {"title": "USGS Water Science School: How much water is there on Earth?", "url": "https://www.usgs.gov/special-topics/water-science-school/science/how-much-water-there-earth", "checked_on": CHECKED},
        {"title": "NASA Earth Observatory: A Measure of Salt", "url": "https://science.nasa.gov/earth/earth-observatory/a-measure-of-salt-78250/", "checked_on": CHECKED},
        {"title": "NASA Earth Observatory: A Global Accounting of Earth's Rivers", "url": "https://science.nasa.gov/earth/earth-observatory/global-accounting-of-earths-rivers-152742", "checked_on": CHECKED},
        {"title": "Chamberlin, Shaw & Rich, Our World Ocean, 8.09 Residence Time (LibreTexts)", "url": "https://geo.libretexts.org/Bookshelves/Oceanography/Our_World_Ocean%3A_Understanding_the_Most_Important_Ecosystem_on_Earth_Essentials_Edition_(Chamberlin_Shaw_and_Rich)/03%3A_New_Page/08%3A_The_Water_Cycle_and_Ocean_Salinity/8.09%3A_Residence_Time", "checked_on": CHECKED},
        {"title": "Martha R. Scott, Ocean Chemical Processes (Water: Science and Issues, Gale)", "url": "https://www.encyclopedia.com/science/news-wires-white-papers-and-books/ocean-chemical-processes", "checked_on": CHECKED},
        {"title": "HELCOM: Salinity of the Baltic Sea (archived)", "url": "https://archive.iwlearn.org/helcom.fi/environment2/nature/en_GB/salinity/index.html", "checked_on": CHECKED},
        {"title": "Wikipedia: Red Sea", "url": "https://en.wikipedia.org/wiki/Red_Sea", "checked_on": CHECKED},
        {"title": "Wikipedia: Baltic Sea", "url": "https://en.wikipedia.org/wiki/Baltic_Sea", "checked_on": CHECKED},
        {"title": "Wikipedia: Dead Sea", "url": "https://en.wikipedia.org/wiki/Dead_Sea", "checked_on": CHECKED},
        {"title": "水產試驗所：臺灣周邊海域漁場環境監測IV（107年度）", "url": "https://fisheryprogress.org/sites/default/files/documents_actions/Environmental%20monitoring%20of%20fishing%20grounds%20in%20the%20coastal%20and%20offshore%20waters%20around%20Taiwan.pdf", "checked_on": CHECKED},
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
