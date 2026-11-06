"""Generate video.json for sothatswhy-p05-down-jacket (原來如此事務所 對話版 P05).

Run `python3 build_scenes.py` from anywhere: it rewrites video.json next to this file and freezes
every shot's camera move in cameras.json (a shot keeps the camera it was first given, so turning a
shot into a card, or deleting one, never shifts the others: the camera is in the keyframe cache key).
Edit lines and prompts here, never in video.json.
"""
import itertools, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = "sothatswhy-p05-down-jacket"
CHECKED = "2026-11-04"

# ---------- series constants (identical to P02, so the approved character sheets are reused) ----------
VOICE = {"provider": "gemini", "name": "Sulafat",
         "style": "標準國語，咬字清楚，台北人平常說話的語調。事務所的所長，溫和、有耐心，像陪一個好奇的小朋友和你一起找答案。語速像平常聊天，一秒四到五個字，句與句之間不拖。"}
SHEET = "character reference: one single full-body figure standing in the centre, facing the viewer in a slight three-quarter turn, relaxed friendly pose, both hands clearly drawn, plain empty cream background with nothing else in the picture, no turnaround, no second view, no seal, no stamp, no signature, no text"
CHARACTERS = [
    {"id": "chief", "name": "所長",
     "appearance": "a friendly middle-aged woman, the chief of a small question office, with round black glasses, shoulder-length dark hair with a streak of grey tied in a low ponytail, a warm smile, a mustard-yellow cardigan over a white blouse, ink-navy trousers, brown shoes, a yellow pencil tucked behind one ear",
     "voice": dict(VOICE), "sheet_prompt": SHEET},
    {"id": "kid", "name": "小問",
     "appearance": "a curious eight-year-old girl with a short black bob haircut with straight bangs and one small cowlick sticking up on top, large round eyes, wearing a navy raincoat-style jacket with a mustard-yellow hood, white sneakers, holding a small plain blank notebook in both hands",
     "voice": {"provider": "gemini", "name": "Leda", "style": "標準國語，咬字清楚，台北人平常說話的語調；八歲小女孩的聲音，好奇、活潑，問問題時句尾上揚，語速輕快"},
     "sheet_prompt": SHEET},
]

# Identity goes LAST in every prompt (P02: putting it first drifted some frames to photo or 3D).
KIDDESC = "the girl has a short black bob with straight bangs and one small cowlick on top and wears a navy raincoat jacket with a mustard-yellow hood"
CHIEFDESC = "the chief wears round black glasses, her dark hair with a grey streak is tied in a low ponytail, a yellow pencil is tucked behind her ear, mustard-yellow cardigan"
JACKET = "a puffy coral-orange down jacket with stitched horizontal puffy sections"  # the one throughline object
WALL = "a plain pale wall behind her"

CAMS = itertools.cycle(["push in", "pan left", "pull out", "drift", "tilt up", "pan right", "push in", "tilt down", "pull out", "drift"])
CAM_FILE = os.path.join(HERE, "cameras.json")
FROZEN = json.load(open(CAM_FILE, encoding="utf-8")) if os.path.exists(CAM_FILE) else {}

S = []
# Shots whose first drawing had mismatched or drifting pupils (owner, 2026-11-05: "在1:00的時候眼珠怪怪的");
# the redraw asks for matching eyes and is judged by the keyframe judge's eye clause.
EYES = {"kid-shiver", "down-palm", "kid-empty-gap", "kid-rug", "kid-question", "kid-dent", "chief-both-ways",
        "chief-not-heater", "chief-secret", "chief-feather", "wind-chill", "ice-back", "chief-plausible",
        "chief-one-way", "kid-sleeve", "chief-drying", "chief-shell", "kid-shake-jacket", "chief-turn-up", "kid-tile-again"}
# Eye shots whose first eye redraw still failed three takes: ask for a straight look instead.
EYES_FRONT = {"kid-sleeve", "kid-question", "down-palm", "kid-dent", "chief-shell"}
# Third eye round (independent check after the second): simple identical eyes, looking ahead.
EYES_DOTS = {"kid-question", "chief-not-heater", "chief-turn-up", "ice-back", "wind-chill"}
# Still cross-eyed after three rounds: closed happy eyes cannot point two ways.
EYES_CLOSED = {"chief-turn-up", "chief-not-heater"}
def _shot(id, prompt, chars, lines, chapter):
    cam = FROZEN.get(id) or next(CAMS)
    if id in EYES:
        eyes = ", her two eyes matching, both pupils looking the same way"
        if id in EYES_FRONT:
            eyes = ", looking straight at the viewer with two matching round eyes"
        if id in EYES_DOTS:
            eyes = ", her eyes two identical round dark eyes side by side, looking straight ahead"
        if id in EYES_CLOSED:
            eyes = ", her eyes closed as two happy curved lines behind her glasses"
        for desc in (KIDDESC, CHIEFDESC):
            prompt = prompt.replace(", " + desc, eyes + ", " + desc)
    S.append(dict(id=id, chapter=chapter, template="shot", data=dict(prompt=prompt, camera=cam, visual="still", characters=list(chars)), lines=list(lines)))
def kid(id, prompt, *lines, chapter=None):
    """The kid doing one thing, facing the camera; her hands busy or empty, never holding the notebook."""
    _shot(id, prompt.rstrip(". ") + ", " + KIDDESC, ["kid"], lines, chapter)
def chief(id, prompt, *lines, chapter=None):
    """The chief, always waist-up or head-and-shoulders, in front of a plain wall."""
    assert prompt.startswith(("Waist-up", "Head-and-shoulders")), id
    _shot(id, prompt.rstrip(". ") + ", " + CHIEFDESC, ["chief"], lines, chapter)
def scene(id, prompt, *lines, chapter=None):
    """No character: an object or place only (the kid's notebook keeps coming back otherwise)."""
    _shot(id, prompt, [], lines, chapter)
def card(id, template, data, *lines, chapter=None):
    S.append(dict(id=id, chapter=chapter, template=template, data=data, lines=list(lines)))
def k(t, e=None, tag=None): return ("kid", t, e, tag)
def c(t, e=None, tag=None): return ("chief", t, e, tag)

# ---------- 開場（系列片頭之後直接進場景，不做濃縮；答案都不先講）----------
kid("closet-jacket", "Medium shot of the girl in front of an open wardrobe on a winter morning, touching " + JACKET + " hanging on its hanger with one hand and flinching from the cold with one eye squeezed shut, soft cool light from a window",
    k("所長！寒流來了，我打開衣櫃，", "興奮，跑進來報案的語氣"), k("羽絨衣是冰的耶！", "不敢相信"), chapter="寒流那天，羽絨衣是冰的")
kid("jacket-fingertips", "Close-up of the girl touching " + JACKET + " lying on her bed with two fingertips and pulling her hand back with a surprised face, soft cool morning light",
    k("它不是很暖嗎？怎麼冰冰的？", "疑惑，句尾上揚", "S:cold"))
chief("chief-mug", "Waist-up medium shot of the chief sitting at a wooden desk, wrapping both hands around a mug and smiling calmly, " + WALL + ", soft morning lamp light",
      c("先別急。你摸摸自己的手，是暖的吧？", "賣關子，帶笑"))
kid("kid-sleeve", "Medium shot of the girl holding " + JACKET + " out in front of her with both hands and frowning at it suspiciously, a plain bedroom wall, soft cool morning light",
    k("暖的。可是它又沒插電，", "不服氣"), k("穿上一下下，怎麼就暖了？", "句尾上揚", "S:delay"))
kid("kid-where", "Close-up of the girl's face filling half the frame, eyes wide and mouth in a small round O, holding " + JACKET + " up at arm's length beside her, soft cool morning light",
    k("那熱是從哪裡來的？", "大驚，句尾上揚", "S:heater"))
chief("chief-secret", "Waist-up medium shot of the chief leaning forward over her desk with a playful look, one hand beside her mouth as if sharing a secret, " + WALL + ", warm lamp light",
      c("這個嘛，答案可能比你想的還要近。", "賣關子"))
kid("ice-teaser", "Medium shot of the girl kneeling at a low table and carefully folding " + JACKET + " around one ice cube on a small white plate, a second bare ice cube on another plate beside it, soft daylight",
    c("先猜一件事：用羽絨衣包住一顆冰塊，", "賣關子"), c("冰會融得比較快，還是比較慢？", "問句，最後放慢", "S:icewrap"))
kid("park-teaser", "Medium shot of the girl standing in a winter park beside a black iron railing, shaking one cold hand in the air with a surprised face, her breath a small white puff, bare trees, soft overcast light",
    c("還有，公園的鐵欄杆，為什麼摸起來比木椅冰那麼多？", "賣關子", "S:iron"))
chief("chief-promise", "Waist-up medium shot of the chief holding up a large round magnifying glass beside her face and smiling, ready to start an investigation, " + WALL + ", soft lamp light",
      c("淋濕的羽絨衣，又為什麼一下就不暖了？", "賣關子", "S:wet"))
kid("kid-question", "Close-up of the girl hugging " + JACKET + " to her chest and tilting her head with a puzzled frown, a plain wall, soft light",
    k("冰冰的衣服，為什麼穿上就暖？", "認真發問，句尾上揚", "S:warm"))

# ---------- 第一章 ----------
kid("kid-thermometer", "Medium shot of the girl tucking a plain glass thermometer with a red line between the puffy sections of " + JACKET + " lying flat on a table, concentrating hard, soft evening lamp light",
    c("你可以試試看：把溫度計塞進羽絨衣裡，放一個晚上。", "說故事的開頭"), chapter="溫度計在羽絨衣裡放了一晚")
kid("thermometer-read", "Head-and-shoulders close-up of the girl with raised eyebrows and a puzzled pout beside a window, a plain glass thermometer with a red line standing on the windowsill next to her, soft morning window light",
    c("隔天早上，它量到的跟房間差不多。"), k("它沒有比較暖？", "意外"))
kid("kid-chair", "Medium shot of the girl patting the seat of a wooden chair with one hand, " + JACKET + " draped over the chair back, a curious look, a plain wall, soft daylight",
    k("所以它跟房間裡的椅子一樣冰？", "想通一半"))
chief("chief-same-room", "Waist-up medium shot of the chief nodding warmly and spreading her open hands, " + WALL + ", soft daylight",
      c("對。椅子、桌子、這件羽絨衣，放久了都跟房間一樣。"), c("房間比你的手冷，摸起來就冰冰的。", None, "P:cold"))
kid("kid-shake-jacket", "Medium shot from the waist up of the girl lifting " + JACKET + " above her head with both hands, a determined face, a plain pale bedroom wall, soft daylight",
    k("裡面一定藏了會熱的東西！", "很有把握的錯猜"))
chief("chief-plausible", "Head-and-shoulders close-up of the chief giving a warm smile with her eyes gently closed, " + WALL + ", soft lamp light",
      c("你這樣猜很合理，穿起來真的很像它在發熱。", "溫和"))
kid("down-palm", "Close-up of the girl peering through a magnifying glass at one fluffy white down cluster resting on her open palm, its fine soft filaments spreading out in every direction, soft daylight",
    c("可是打開來看，裡面只有羽絨和布。"), c("它要是個會發熱的小暖爐，溫度計早就量到了。"))
kid("kid-under-bed", "Medium shot of the girl lying on her tummy on the floor and shining a small flashlight under her bed, turning her face to the camera with a puzzled look, soft evening light",
    k("那暖爐到底在哪裡？", "追問"))
chief("chief-you-heater", "Waist-up medium shot of the chief pointing her open hand straight toward the viewer with a warm smile, " + WALL + ", soft lamp light",
      c("在你身上。", "放慢，轉向觀眾"), c("你自己，就是那個暖爐。", None, "P:heater"))
kid("kid-me", "Close-up of the girl pointing both thumbs at herself with an unconvinced, scrunched-up face, a plain wall, soft light",
    k("我？我又沒有在燒火。", "不相信"))
kid("kid-rice", "Medium shot of the girl sitting at a kitchen table behind a bowl of white rice, both cheeks puffed full, chewing happily, soft morning light",
    c("你吃下去的東西，身體會拿來用。"), k("吃飯就是在加柴火？", "好笑"))
chief("chief-fuel", "Waist-up medium shot of the chief laughing with her eyes closed and one thumb up, " + WALL + ", warm lamp light",
      c("可以這樣想。"), c("用掉的能量，最後大部分都變成了熱。"))
kid("body-heat", "Head-and-shoulders close-up of the girl with her eyes closed and a content smile, a soft warm orange glow shining all around her like a lamp, plain wall, soft evening light",
     c("一個大人安靜坐著，大約一直放出一百瓦左右的熱，", "數字放慢"), c("跟一顆老式燈泡差不多。"))
kid("kid-bulb", "Medium shot of the girl holding both palms close to a glowing old-fashioned round light bulb in a simple desk lamp, feeling its warmth with a curious grin, soft evening light",
    k("那我也是一顆燈泡？", "好笑"))
chief("chief-smaller", "Waist-up medium shot of the chief chuckling with one hand on her chest, " + WALL + ", warm lamp light",
      c("小朋友的身體比較小，放出的熱少一些，"), c("可是也一直在放；睡著的時候，也只是放得少一點。"))
kid("kid-shiver", "Medium shot of the girl at a bus stop on a cold grey morning, hugging herself with both arms and shivering, her teeth chattering, soft overcast light",
    k("那我冷到發抖的時候呢？", "追問", "S:shiver"))
chief("chief-turn-up", "Head-and-shoulders close-up of the chief raising her eyebrows with a knowing smile and one finger raised beside her face, " + WALL + ", soft lamp light",
      c("那是身體在把火力開大。"), c("發抖的時候，放出的熱可以是安靜坐著的好幾倍。", None, "P:shiver"))
kid("kid-hop", "Medium shot of the girl hopping on the spot on a cold sidewalk to warm up, laughing, soft overcast light",
    c("所以下次你冷到發抖，可以跟自己說：", "轉向觀眾，帶笑"), c("我的暖爐，正在加班。", "玩笑"))
kid("kid-breath", "Close-up of the girl blowing warm breath into her cupped hands on a cold morning, a small white puff of breath, a puzzled look over her fingers, soft overcast light",
    k("可是我一直在放熱，", "納悶"), k("為什麼還是會冷？", "章尾停住", "S:leak"))

# ---------- 第二章 ----------
chief("chief-temper", "Waist-up medium shot of the chief tracing an arrow in the air with one finger from left to right, a thoughtful smile, " + WALL + ", soft daylight",
      c("因為熱有一個脾氣：", "說故事"), c("它一定從熱的地方，往冷的地方跑。"), chapter="鐵欄杆其實沒有比較冷")
kid("kid-cocoa", "Medium shot of the girl holding a mug of hot cocoa in both hands and smiling at the curl of steam, sitting by a window, soft morning light",
    c("你雙手捧著熱可可，熱就從杯子跑進你的手。"))
kid("kid-ice-hand", "Close-up of the girl holding an ice cube on her open palm, her fingers going pink, a startled face, a plain wall, soft daylight",
    c("你手上拿一顆冰塊，手會變冰，冰會慢慢融。"), k("是冰把冷傳給我？", "很有把握的錯猜", "S:coldflow"))
chief("chief-only-heat", "Waist-up medium shot of the chief shaking her head slowly with a gentle smile, one palm turned up, " + WALL + ", soft daylight",
      c("其實是倒過來：你手上的熱，跑進冰塊裡。"), c("冷不會跑，一直在跑的是熱。", None, "P:coldflow"))
kid("kid-reverse-q", "Close-up of the girl holding an ice cube up between two fingers and squinting at it suspiciously, a plain wall, soft daylight",
    k("熱不會倒過來跑嗎？", "追問"))
chief("chief-one-way", "Head-and-shoulders close-up of the chief chuckling and shaking one finger, " + WALL + ", soft daylight",
      c("自己不會。你的手，從來不會被冰塊弄得更暖。"))
kid("kid-tiles", "Medium shot of the girl tiptoeing barefoot across a cold tiled kitchen floor with her shoulders hunched up and a wince, soft morning light",
    c("冬天光腳踩在磁磚上，熱就從你的腳跑進地板。"))
kid("kid-rug", "Medium shot of the girl standing barefoot with one foot on a fluffy round rug and one foot on grey kitchen tiles, a surprised face, soft morning light",
    k("可是踩地毯就還好，", "發現"), k("為什麼磁磚比較冰？", None, "S:tile"))
chief("chief-remember-tile", "Head-and-shoulders close-up of the chief putting one finger to her lips with a playful smile, " + WALL + ", soft daylight",
      c("先記住這個問題，等一下公園會告訴你。"))
kid("kid-frosty-window", "Close-up of the girl pressing her fingertip against a cold frosty window pane, her breath fogging the glass, a thoughtful face, soft winter light",
    k("所以冷，就是熱一直跑掉？", "恍然大悟一半"))
chief("chief-slow-down", "Waist-up medium shot of the chief holding both hands low in front of her with palms facing down, a calm smile, " + WALL + ", soft daylight",
      c("對。衣服擋不住它跑，只能讓它跑慢一點。", None, "P:leak"))
kid("kid-railing", "Medium shot of the girl in a winter park shaking her cold hand after touching a black iron railing, a wooden bench right beside it, bare trees, soft overcast light",
    k("走到公園，鐵欄杆好冰！", "誇張"), k("木頭椅子還好耶。"))
kid("kid-knock-iron", "Close-up of the girl beside a black iron railing, tapping it with one small fist and nodding confidently, bare trees behind, soft overcast light",
    k("鐵本來就比較冷吧？", "很有把握的錯猜"))
chief("chief-same-night", "Head-and-shoulders close-up of the chief shaking her head gently with a kind smile, " + WALL + ", soft daylight",
      c("聽起來很對。可是它們整晚都待在同一個公園，"), c("其實差不多一樣冷。", "停一拍"))
kid("kid-doubt", "Head-and-shoulders close-up of the girl frowning doubtfully with her arms crossed, bare park trees behind her, soft overcast light",
    k("怎麼可能？摸起來差好多。", "不服氣"))
chief("chief-not-thermometer", "Waist-up medium shot of the chief holding up her own open hand and looking at it with a wry smile, " + WALL + ", soft daylight",
      c("因為你的手不是溫度計。"), c("手感覺到的，是熱從手上跑走得多快。"))
scene("iron-wood", "Close-up of a small bare hand resting flat on a black iron railing bar in a snowy park, many small wavy red arrows streaming out of the palm into the iron, a wooden bench blurred in the background, flat 2D cartoon with clean dark outlines, soft overcast light",
     c("鐵把你手上的熱搬走得很快，木頭搬得很慢。", None, "P:iron"))
scene("steel-wood", "Close-up of one shiny silver metal spoon standing in a mug of hot cocoa on a kitchen table, the whole metal handle glowing orange-red with heat right up to the top, steam rising, soft kitchen light",
     c("鋼鐵傳熱的本事，比木頭快上百倍。", "數字放慢"))
kid("kid-tile-again", "Medium shot of the girl sitting on a kitchen chair with her bare feet on cold grey floor tiles, curling her toes and smiling, a fluffy round rug beside the chair, soft morning light",
    c("地毯和磁磚也是這樣：磁磚把你腳上的熱，搬得比較快。", None, "P:tile"))
kid("kid-zipper-pull", "Close-up of the girl holding the zipper of " + JACKET + " with one hand and shivering with a funny face, soft morning light",
    k("羽絨衣的拉鍊頭，也比布冰！", "發現"))
chief("chief-same-coat", "Waist-up medium shot of the chief nodding with raised eyebrows, one hand open toward the viewer, " + WALL + ", soft daylight",
      c("可是你捏著它一下下，它就不冰了：你的熱已經跑進去了。"))
chief("chief-you-touch", "Head-and-shoulders close-up of the chief looking straight at the viewer with a curious smile, one hand on her chin, " + WALL + ", soft lamp light",
      c("所以下次你摸到冰冰的東西，可以想一想：", "轉向觀眾"), c("是它真的比較冷，還是它很會把熱搬走？"))
kid("kid-bench-think", "Medium shot of the girl sitting on a wooden park bench with her hands tucked under her legs, looking up and thinking hard, bare trees, soft overcast light",
    k("那什麼最會擋熱？", "章尾停住，句尾上揚", "S:block"))

# ---------- 第三章 ----------
chief("chief-air", "Waist-up medium shot of the chief opening both hands wide as if presenting something invisible, a mischievous smile, " + WALL + ", soft daylight",
      c("答案可能會讓你意外：身邊最會擋熱的，是空氣。", "賣關子，放慢", "P:block"), chapter="羽絨把空氣關了起來")
kid("kid-wave-air", "Medium shot of the girl waving both empty hands through the air in front of her with a baffled face, a plain room, soft daylight",
    k("空氣？我們每天泡在空氣裡耶。", "不相信"))
chief("chief-still-air", "Head-and-shoulders close-up of the chief holding one hand very still in the air in front of her, a calm face, " + WALL + ", soft lamp light",
      c("不會動的空氣，非常不會傳熱。"), c("麻煩的是，空氣很難乖乖不動。"))
kid("kid-why-move", "Head-and-shoulders close-up of the girl tilting her head with a puzzled pout and one finger on her chin, a plain wall, soft light",
    k("它為什麼會動？", "追問"))
kid("kid-warm-air", "Medium shot of the girl standing outdoors on a cold morning with her arms held out, faint wavy lines of warm air rising off her shoulders and arms, bare trees behind, soft overcast light",
    c("貼著你的空氣被你弄暖了，就會往上飄走，"), c("換一批冷空氣過來，熱就被一路帶走。"))
kid("kid-why-rise", "Close-up of the girl watching a curl of steam rise from a cup of hot tea and following it upward with her eyes and one finger, soft kitchen light",
    k("暖的空氣，為什麼會往上飄？", "追問", "S:rise"))
chief("chief-lighter", "Head-and-shoulders close-up of the chief lifting one open hand slowly upward like a floating balloon, a calm smile, " + WALL + ", soft lamp light",
      c("暖空氣比旁邊的冷空氣輕，就會浮上去。", None, "P:rise"), c("所以你就算站著不動，熱也一直被帶走。", "轉向觀眾"))
kid("kid-feather-nose", "Medium shot from the waist up of the girl holding a big fluffy white feather by its quill and tickling the tip of her nose with it, grinning, a plain wall, soft daylight",
    k("那羽絨衣暖，是因為羽毛很暖？", "很有把握的錯猜", "S:feather"))
chief("chief-feather", "Waist-up medium shot of the chief holding a small fluffy white down cluster between two fingers and studying it with a gentle smile, " + WALL + ", soft lamp light",
      c("一團羽絨傳熱的本事，其實跟空氣差不多。"))
kid("down-magnifier", "Extreme close-up of the girl looking through a big magnifying glass at one fluffy white down cluster floating in front of her, its very fine filaments spreading out in every direction, soft daylight",
    c("你用放大鏡看一朵羽絨，"), c("它像一團很細很細的小絲，往四面八方張開。"))
kid("kid-jar", "Medium shot from the waist up of the girl holding a clear glass jar full of fluffy white down feathers with both hands, delighted, soft daylight",
    c("一大把擠在一起，就撐出好多好多小空間。"))
chief("chief-locked", "Waist-up medium shot of the chief cupping her two hands together as if holding something small inside, a soft smile, " + WALL + ", warm lamp light",
      c("空氣被關在這些小空間裡，想飄也飄不走。", None, "P:feather"))
kid("kid-air-vest", "Medium shot of the girl hugging a big clear plastic bag puffed up with air to her chest like a vest, a cheeky grin, a plain wall, soft daylight",
    k("那穿一件空氣不就好了？", "開玩笑", "S:airvest"))
chief("chief-cut-small", "Head-and-shoulders close-up of the chief holding up a small square quilted cushion beside her face, a patient smile, " + WALL + ", soft daylight",
      c("一大片空氣會自己轉圈，把熱帶走。"), c("切成很多很小的格子，它才轉不起來。", None, "P:airvest"))
kid("kid-face-jacket", "Close-up of the girl resting her cheek on " + JACKET + " folded on her lap and smiling up at the camera, soft daylight",
    k("像好多好多小房間！", "驚喜"), k("羽絨衣是一件裝滿空氣的衣服！", "開心"))
chief("chief-opinion", "Waist-up medium shot of the chief laughing softly with her arms folded, " + WALL + ", warm lamp light",
      c("我覺得這是它最聰明的地方：", "意見，輕鬆"), c("最重要的材料，是不用錢的空氣。"))
kid("kid-blanket", "Medium shot of the girl wrapped up in a thick fluffy blanket on a sofa with only her face peeking out, smiling, soft evening lamp light",
    c("你的毛衣、棉被，也都在用同一招：把空氣關起來。", "轉向觀眾"))
kid("kid-cat", "Medium shot of the girl sitting on a sofa petting a fluffy grey cat asleep in her lap with both hands, smiling, soft evening lamp light",
    k("那貓咪的毛也是？", "好奇"))
chief("chief-fur", "Head-and-shoulders close-up of the chief holding a small fluffy white cat up beside her cheek with a fond smile, " + WALL + ", warm lamp light",
    c("對，動物的毛，也是把空氣關在毛裡面。"))
kid("kid-bear-hug", "Medium shot of the girl squeezing " + JACKET + " flat against her body in a tight bear hug, a curious sideways look, a plain wall, soft daylight",
    k("那我把羽絨衣壓扁呢？", "章尾停住，調皮", "S:squash"))

# ---------- 第四章 ----------
kid("kid-dent", "Close-up of the girl's hand pressing flat into " + JACKET + " lying on a table, a flattened dent around the palm, the girl leaning in above it with a curious smile, soft daylight",
    c("你用力抱住它，抱過的地方就扁了一塊。"), chapter="壓扁、淋濕、被風吹透")
chief("chief-less-air", "Head-and-shoulders close-up of the chief pressing her two palms together in front of her chin, a thoughtful face, " + WALL + ", soft daylight",
      c("扁掉的地方，關住的空氣變少，"), c("那裡就沒那麼暖。", None, "P:squash"))
kid("kid-sit-jacket", "Medium shot of the girl sitting on " + JACKET + " spread on a park bench and pointing down at it with a cheeky grin, bare trees, soft overcast light",
    k("那我坐在它上面呢？", "調皮"))
chief("chief-sit", "Head-and-shoulders close-up of the chief laughing and covering her mouth with one hand, " + WALL + ", soft daylight",
      c("那屁股底下那一塊，就被你壓得最扁。"))
kid("kid-heavy-coat", "Medium shot of the girl straining to lift a huge heavy padded winter coat with both arms, cheeks puffed out with effort, a plain wall, soft daylight",
    k("那越重越厚，就一定越暖？", "很有把握的錯猜", "S:heavy"))
chief("chief-not-weight", "Head-and-shoulders close-up of the chief shaking one finger with a gentle smile, " + WALL + ", soft lamp light",
      c("重不重，不是重點。"), c("重點是裡面，關住了多少不會動的空氣。", None, "P:heavy"))
kid("kid-drizzle", "Medium shot of the girl standing in cold drizzle holding " + JACKET + " out with both hands as raindrops darken it, a worried face, soft grey light",
    k("那下雨淋濕了呢？", "擔心"))
scene("chief-water-in", "Close-up of a yellow kitchen sponge on a white plate, water pouring onto it from a small clear glass, many little round air bubbles escaping from the wet sponge, flat 2D cartoon with clean dark outlines, soft lamp light",
      c("濕了，水就跑進那些小空間，"), c("把空氣擠出去。"))
kid("water-air", "Close-up of the girl dipping one bare hand into a glass bowl of cold water with a shocked gasp, her other hand held up in the air relaxed, a plain wall, cool grey light",
     c("水傳熱的本事，大約是空氣的二十幾倍。", "數字放慢"))
kid("kid-wring", "Head-and-shoulders close-up of the girl with soaking wet hair dripping water onto her shoulders and a grimace, rain falling behind her, soft grey light",
    c("所以衣服一濕，熱就跑得快很多，穿起來就沒那麼暖。", None, "P:wet"))
chief("chief-clump", "Waist-up medium shot of the chief squeezing a small wet ball of cotton between her fingers, a sympathetic face, " + WALL + ", soft grey light",
      c("羽絨濕了還會塌下去，撐不起那些小空間。"), c("你淋過冬天的雨，應該記得那種冷。", "轉向觀眾"))
kid("kid-towel", "Medium shot of the girl with damp dripping hair and a small towel around her neck, shivering by an open window with a grimace, soft grey light",
    k("頭髮沒吹乾，也好冷！", "想到"))
chief("chief-drying", "Head-and-shoulders close-up of the chief nodding with her eyes gently closed and a knowing smile, " + WALL + ", soft lamp light",
      c("對，水在乾掉的時候，還會從你身上再帶走熱。"))
kid("kid-bridge-wind", "Head-and-shoulders close-up of the girl squinting against a cold wind, her bangs blown sideways, a plain grey winter sky behind her, soft overcast light",
    k("有風的時候，怎麼特別冷？", "追問", "S:wind"))
chief("chief-layer", "Head-and-shoulders close-up of the chief with her arms crossed over her chest and a cosy smile, " + WALL + ", soft lamp light",
      c("還記得那層會往上飄的暖空氣嗎？", "轉向觀眾"))
kid("kid-fan", "Medium shot of the girl standing in front of a small electric fan with her eyes squeezed shut and her bangs blowing back, laughing, a plain wall, soft daylight",
    c("風一來，它還沒飄走就被吹散，"), c("冷空氣換得更勤，熱就跑得更快。"))
chief("chief-faster", "Head-and-shoulders close-up of the chief with puffed cheeks blowing out a puff of air, a thoughtful look, " + WALL + ", soft lamp light",
      c("被風帶走的熱，常常比慢慢碰過去的快得多。"))
kid("wind-chill", "Medium shot of the girl walking along a windy riverside path in winter, her hair blown sideways, cupping both hands over her red cold ears with a pained squint, curved white wind lines streaming past her face, soft overcast light",
     c("這就叫做風寒：同樣的溫度，有風就覺得冷很多。", None, "P:wind"))
kid("kid-cold-ears", "Close-up of the girl on a windy footbridge cupping both hands over her ears, her cheeks and nose rosy from the cold, squinting, soft overcast light",
    c("風寒說的，是露在外面的皮膚：臉、耳朵、手。"), k("難怪我耳朵最先痛！", "恍然大悟"))
chief("chief-shell", "Head-and-shoulders close-up of the chief holding the sleeve of " + JACKET + " up beside her face and tapping its smooth outer fabric with one finger, " + WALL + ", soft daylight",
      c("所以羽絨衣外面那層布，最好能擋風，"), c("也最好別讓雨滲進去。"))
kid("kid-wall", "Medium shot from the waist up of the girl on a footbridge holding " + JACKET + " wide open in front of her with both hands, laughing, soft overcast light",
    k("像一面擋風的牆！", "開心"), k("那拉鍊沒拉好呢？", "追問", "S:zip"))
chief("chief-zip", "Head-and-shoulders close-up of the chief miming pulling a zipper up to her chin with a playful wince, " + WALL + ", soft daylight",
      c("風就從前面灌進去，把貼著你的暖空氣吹走。", None, "P:zip"), c("你應該被這樣冷過一次。", "轉向觀眾，帶笑"))
kid("kid-thermos-shake", "Medium shot of the girl holding up a shiny steel thermos with both hands and shaking it next to her ear to hear ice rattle inside, a curious face, a plain wall, soft daylight",
    k("對了，保溫瓶也沒插電，", "突然想到"), k("為什麼冰水也能保冰？", "章尾停住，句尾上揚", "S:thermos"))

# ---------- 第五章（保溫瓶：每一步都接回羽絨衣）----------
chief("chief-same-job", "Waist-up medium shot of the chief holding up a shiny steel thermos beside her face with a knowing smile, " + WALL + ", soft lamp light",
      c("因為保溫瓶跟羽絨衣，做的是同一件事。"), c("它不加熱，也不製冷，只是讓熱很難進出。"), chapter="保溫瓶把空氣幾乎抽光了")
scene("thermos-magnifier", "Close-up of two shiny steel cups on a table, a small steel cup sitting inside a bigger steel cup with an empty dark gap all around between them, flat 2D cartoon with clean dark outlines, soft daylight",
    c("保溫瓶是兩層瓶子，中間的空氣幾乎都抽掉了。"))
kid("kid-empty-gap", "Close-up of the girl tapping the side of a shiny steel thermos with one fingertip and listening closely, a curious face, a plain wall, soft daylight",
    k("羽絨衣是把空氣關起來，", "比較"), k("它是連空氣都不要？"))
chief("chief-no-bridge", "Waist-up medium shot of the chief holding her two hands in front of her chest facing each other with a small gap between them, " + WALL + ", soft daylight",
      c("對。羽絨衣裡的空氣動不了，熱還能慢慢碰過去；"), c("保溫瓶中間幾乎什麼都沒有，熱連碰都很難。"))
kid("kid-better-coat", "Close-up of the girl holding a shiny steel thermos against her chest like a little coat and grinning, a plain wall, soft daylight",
    k("那保溫瓶是更厲害的羽絨衣？", "好笑"))
chief("chief-cant-wear", "Head-and-shoulders close-up of the chief laughing and shrugging with both palms up, " + WALL + ", soft daylight",
      c("可以這樣想，只是它穿不上身。", "玩笑"))
kid("kid-thermos-neck", "Close-up of the girl's face squinting one eye into the round opening of a shiny steel thermos held right in front of her face, soft daylight",
    k("瓶口那裡，像我沒拉的拉鍊？", "想到"))
chief("chief-neck", "Waist-up medium shot of the chief tapping the rim of a shiny steel thermos with one finger, an approving smile, " + WALL + ", soft daylight",
      c("很像。瓶口沒有真空，熱很多是從那裡溜走。"))
kid("kid-two-flasks", "Medium shot of the girl hugging a shiny steel thermos with both arms and grinning, a plain wall, soft daylight",
    k("所以熱湯保熱，冰水也保冰！", "想通"))
chief("chief-both-ways", "Waist-up medium shot of the chief pointing one finger left and then the other right, a cheerful face, " + WALL + ", soft daylight",
      c("對。還記得熱的脾氣嗎？它往哪邊跑，瓶子就擋哪邊。", None, "P:thermos"))
kid("kid-summer", "Medium shot of the girl holding " + JACKET + " in front of an electric fan on a hot summer day, sweat on her forehead, a doubtful face, soft hazy light",
    k("那夏天穿羽絨衣呢？", "調皮", "S:summer"))
chief("chief-summer", "Head-and-shoulders close-up of the chief fanning herself with a plain paper fan and laughing, " + WALL + ", soft daylight",
      c("它一樣把你的熱留住。"), c("只是夏天你不想留，就熱得受不了。", None, "P:summer"))
kid("ice-back", "Medium shot of the girl kneeling at a low table, poking " + JACKET + " that is folded around one ice cube on a small white plate, a second bare ice cube on another plate beside it, soft daylight",
    c("那開頭那顆包著羽絨衣的冰塊呢？"), k("羽絨衣那麼暖，會融得更快吧？", "很有把握的錯猜，章尾停住"))

# ---------- 收尾 ----------
chief("chief-not-heater", "Head-and-shoulders close-up of the chief gently shaking her head with a kind smile, " + WALL + ", soft lamp light",
      c("很多人都會這樣猜。可是它裡面沒有暖爐，"), c("還記得溫度計那一晚嗎？它自己一點也沒變暖。"), chapter="把冰塊包進羽絨衣")
kid("two-cubes", "Close-up of two small white plates side by side on a low wooden table, on the left one ice cube folded inside " + JACKET + " still solid, on the right a bare ice cube already shrunk into a wide puddle, the girl peeking in from the edge of the frame with a delighted surprised face, soft daylight",
     c("很多學校課堂都會做這個比較：一顆包起來、一顆不包。"), c("包起來的那顆，融得比較慢。", None, "P:icewrap"))
kid("kid-blocker", "Close-up of the girl clapping her hands together in front of her chest with a big surprised smile, a plain wall, soft daylight",
    k("包起來，反而比較慢？！", "大驚"))
kid("kid-hug-done", "Head-and-shoulders close-up of the girl hugging " + JACKET + " to her chest with her eyes closed and a big happy smile, warm morning light from a window",
    k("我知道了！", "自己想通"), k("穿上會暖，是我的熱被它留住了！", "篤定", "P:warm"))
chief("chief-folder-done", "Waist-up medium shot of the chief closing a plain folder with both hands and smiling, " + WALL + ", warm lamp light",
      c("下次你穿上它，等一下下，", "轉向觀眾，輕聲"), c("那一下下，是你的熱正在把裡面填滿。", None, "P:delay"))
card("outro", "outro", {"title": "原來如此！", "cta": "訂閱原來如此事務所", "lines": ["暖爐是你，羽絨衣只負責把熱留住"]},
     k("原來如此！", "開心大聲"), c("冰淇淋包在羽絨衣裡，會融得比較快，還是比較慢？", "問句上揚，像聊天"),
     c("留言告訴我們你的答案。"), c("想一起找生活裡的為什麼，就訂閱原來如此事務所。", "誠懇"))

# ---------- assemble ----------
WHAT = {"cold": "羽絨衣為什麼摸起來冰冰的", "delay": "為什麼穿一下下才暖", "heater": "熱是從哪裡來的",
        "icewrap": "包著羽絨衣的冰塊融得快還是慢", "iron": "鐵欄杆為什麼摸起來比木椅冰", "warm": "冰冰的衣服，為什麼穿上就暖",
        "shiver": "冷到發抖時身體在做什麼", "leak": "一直在放熱，為什麼還是會冷", "coldflow": "是不是冰把冷傳給手",
        "tile": "磁磚為什麼比地毯冰", "block": "什麼最會擋熱", "rise": "暖空氣為什麼會往上飄", "feather": "羽毛本身暖不暖",
        "airvest": "為什麼不能直接穿一件空氣", "squash": "壓扁會怎樣", "heavy": "是不是越重越厚就越暖", "wet": "淋濕了會怎樣",
        "wind": "有風為什麼特別冷", "zip": "拉鍊沒拉好會怎樣", "thermos": "保溫瓶沒插電，為什麼也能保冰", "summer": "夏天穿羽絨衣會怎樣"}
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
loops = [{"setup": loops_s[key], "payoff": loops_p[key], "what": WHAT[key]} for key in sorted(WHAT, key=lambda key: loops_s[key])]

doc = {
    "schema_version": 1, "slug": SLUG, "format": "drama", "category": "explainer", "narration_locale": "zh-TW",
    "target_minutes": [10, 13], "voice": VOICE, "subtitles": {"burn_in": False}, "theme": "paper", "look": {"preset": "cute-cartoon"},
    # Same 14-minute bed as P02 (one paid Lyria take, tail trimmed, crossfaded): the series sounds the same.
    "music": {"track": "sothatswhy-p02-bed.m4a", "sha256": "54169439df49a00bc3ad993a148690be9f79d1dff8a4ea5143e64e583001b20c", "gain_db": -20, "duck_db": -10},
    "characters": CHARACTERS, "loops": loops,
    "youtube": {
        "category_id": 27, "made_for_kids": False, "default_language": "zh-TW",
        "title": "羽絨衣一點熱都不會產生，為什麼穿上就暖？｜原來如此事務所",
        "description": "寒流來的早上從衣櫃拿出羽絨衣，摸起來是冰的。它沒插電、沒有電池，自己一點熱都不會產生，為什麼穿上就暖？\n\n"
                       "這一集，所長和小問跟著同一件羽絨衣找那個暖爐：熱從哪裡來、為什麼一直往外跑、同一個公園裡的鐵欄杆為什麼摸起來比木椅冰、"
                       "什麼最會擋熱、羽絨壓扁淋濕或被風吹透為什麼就不暖，最後用保溫瓶和一顆包起來的冰塊，看保暖到底是在做什麼。\n\n"
                       "本集插圖由 AI 生成。功率與倍數都是教科書的典型值或大約的數量級；每個說法的出處列在下方參考資料。\n\n資料截至 " + CHECKED,
        "tags": ["羽絨衣", "保暖", "為什麼穿羽絨衣會暖", "熱傳導", "保溫瓶", "風寒", "科普", "原來如此事務所"],
        "video_id": None},
    "thumbnail": {"template": "thumb", "data": {"headline": "羽絨衣\n**不會發熱**", "sub": "暖爐其實是你自己", "shot": "kid-where"}},
    "sources": [
        {"title": "OpenStax College Physics 2e: 7.8 Work, Energy, and Power in Humans", "url": "https://openstax.org/books/college-physics-2e/pages/7-8-work-energy-and-power-in-humans", "checked_on": CHECKED},
        {"title": "OpenStax College Physics 2e: 13.1 Temperature", "url": "https://openstax.org/books/college-physics-2e/pages/13-1-temperature", "checked_on": CHECKED},
        {"title": "OpenStax College Physics 2e: 15.3 Introduction to the Second Law of Thermodynamics", "url": "https://openstax.org/books/college-physics-2e/pages/15-3-introduction-to-the-second-law-of-thermodynamics-heat-engines-and-their-efficiency", "checked_on": CHECKED},
        {"title": "OpenStax College Physics 2e: 14.4 Heat Transfer Methods", "url": "https://openstax.org/books/college-physics-2e/pages/14-4-heat-transfer-methods", "checked_on": CHECKED},
        {"title": "OpenStax College Physics 2e: 14.5 Conduction", "url": "https://openstax.org/books/college-physics-2e/pages/14-5-conduction", "checked_on": CHECKED},
        {"title": "OpenStax College Physics 2e: 14.6 Convection", "url": "https://openstax.org/books/college-physics-2e/pages/14-6-convection", "checked_on": CHECKED},
        {"title": "OpenStax University Physics Volume 2: 1.6 Mechanisms of Heat Transfer", "url": "https://openstax.org/books/university-physics-volume-2/pages/1-6-mechanisms-of-heat-transfer", "checked_on": CHECKED},
        {"title": "HyperPhysics: Steel and Wood at Zero Celsius", "url": "https://hyperphysics.gsu.edu/hbase/thermo/woodmet.html", "checked_on": CHECKED},
        {"title": "ColumbiaDoctors: Cold Exposure, Ways the Body Loses Heat", "url": "https://www.columbiadoctors.org/health-library/article/cold-exposure-ways-body-loses-heat", "checked_on": CHECKED},
        {"title": "National Weather Service: Wind Chill Chart", "url": "https://www.weather.gov/safety/cold-wind-chill-chart", "checked_on": CHECKED},
        {"title": "University of Illinois Physics, Ask the Van: Characteristics of Dewars", "url": "https://van.physics.illinois.edu/ask/listing/1680", "checked_on": CHECKED},
        {"title": "Wikipedia: Vacuum flask", "url": "https://en.wikipedia.org/wiki/Vacuum_flask", "checked_on": CHECKED},
        {"title": "Science Foundation Ireland: What Material Will Keep Ice Lollies the Coolest?", "url": "https://www.sfi.ie/site-files/primary-science/media/pdfs/col/keeping_ice_lollies_cool.pdf", "checked_on": CHECKED},
        {"title": "ASHRAE / WGBH ZOOM: Keep-A-Cube", "url": "https://www.ashrae.org/File%20Library/Communities/Student%20Zone/K-12%20Activities/Elem-and-Midd_-Keep-A-Cube.pdf", "checked_on": CHECKED},
        {"title": "Tes Magazine: Iceman cometh (1998)", "url": "https://www.tes.com/magazine/archive/iceman-cometh", "checked_on": CHECKED},
        {"title": "Kim & McCullough (2001), The Effect of Adjustable Garment Closures and Layering on Insulation in Cold Weather, The Korean Fashion and Textile Research Journal 3(5)", "url": "https://koreascience.or.kr/article/JAKO200123659443366.page", "checked_on": CHECKED},
        {"title": "US Patent 4,992,327: Synthetic down (wet loft comparison with down)", "url": "https://patents.google.com/patent/US4992327A/en", "checked_on": CHECKED},
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
body = [s for s in scenes if s["template"] != "outro"]
chars = sum(length(l["text"]) for s in scenes for l in s["lines"])
kidc = sum(length(l["text"]) for s in scenes for l in s["lines"] if l["speaker"] == "kid")
shots = sum(1 for s in body if s["template"] == "shot")
lines_all = [l for s in scenes for l in s["lines"]]
print(f"scenes {len(scenes)} shots {shots} cards {len(body) - shots} ({shots / len(body):.0%} pictures) lines {n} "
      f"chars {chars} kid {kidc / chars:.0%} of chars, {sum(l['speaker'] == 'kid' for l in lines_all) / n:.0%} of lines; est {chars / RATE / 60:.1f} min at {RATE}/s; loops {len(loops)}", file=sys.stderr)
run = 0
for s in body:
    run = run + 1 if s["template"] != "shot" else 0
    assert run <= 3, f"more than three cards in a row at {s['id']}"
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
cams = [s["data"]["camera"] for s in scenes if s["template"] == "shot"]
assert all(not (a == b == c_) for a, b, c_ in zip(cams, cams[1:], cams[2:])), "three shots in a row with the same camera"
