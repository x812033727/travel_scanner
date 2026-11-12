"""Generate video.json for sothatswhy-p29-https (原來如此事務所 對話版 P29).

Run `python3 build_scenes.py` from anywhere: it rewrites video.json next to this file, freezes
every shot's camera move in cameras.json (a shot keeps the camera it was first given, so deleting
a shot never shifts the others: the camera is in the keyframe cache key), and then writes script.md
through `node tools/video/cli.mjs script --slug sothatswhy-p29-https` (local, free).
Edit lines and prompts here, never in video.json.
Started from a copy of sothatswhy-p13-gps-timing/build_scenes.py (series constants, helpers,
assembly and self-checks unchanged; EXTRA and REWRITE start empty because P13's entries were picture
fixes for P13 only); the content is new.
2026-11-11 rules applied (dialogue-pilot README §4, §9, §10.6): the faster voice style for both characters,
`pauses: {line_ms: 0, scene_ms: 150}` and `still_motion: "beat"`, no `pause_after_ms` on lines except a
BEAT_MS beat on the line right before each `P:` payoff in the same scene, and only an upper bound on length.
Shot pacing (P21 storyboard score): a short reaction line gets its own shot only when the picture changes
something, so most shots carry two to four lines.
"""
import hashlib, itertools, json, os, re, subprocess, sys, unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
SLUG = "sothatswhy-p29-https"
CHECKED = "2026-11-12"
BEAT_MS = 500   # 答案揭曉前的一拍；第一集照這個試，成片量過再調（README §10.6）

# ---------- series constants ----------
# Both characters are identical to P06/P07/P14/P08/P21/P13 (approved series sheets reused through the `series` tag):
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
# Lines added after a visual review. Empty until this episode's keyframes are drawn.
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

# One drawing language for the whole episode (README §10.5: the image model cannot draw diagrams, maps
# with labels, arrows, counts or directions). The main thread is ONE afternoon: 小問 sits in a café with her
# mother, about to type her game password on the café's free wireless network; her mother told her to check
# that the address starts with https; later a classmate's "free gems" link turns out to be https too.
# The one analogy carried from start to end is PASSING A LETTER ACROSS THE CLASSROOM: classmates hand it on
# (the café's router and the network companies); an open note can be read and changed; the friend at the far
# end shows an ID card naming her and showing the pattern of a stamp only she owns (the certificate and its
# key); the card is signed by her teacher, whose card is signed by a head teacher the browser already knows
# (the chain to a built-in root); before writing, the two mix a secret colour of paint in front of everyone
# (the key exchange); the friend stamps the whole exchange so far (the signature over the handshake); every
# letter is sealed with that colour and carries a hidden number (sealing and sequence numbers); the thickness
# of the envelope and the name on its front still show (length, timing, the site name), and the seal says
# nothing about whether the friend is honest. Every frame is an everyday object at human scale.
# Tablets and phones show only a plain pale bar with one tiny padlock and soft colour blocks (README §3.1:
# name what the display shows, never writing).
CAFE = "at a sunny café table by a big window,"
CLASS = "in a sunny classroom with wooden desks,"
STYLE = ", simple flat 2D cel-shaded cartoon drawing with clean ink outlines and flat colours"
TABLET = "a small tablet showing a plain pale grey bar along the top with one tiny padlock icon and soft pastel colour blocks below"
LETTER = "a small cream envelope closed with a round red wax seal"
CARD = "a plain cream student card with a tiny cartoon face portrait and one round golden emblem"
def obj(id, prompt, *lines, chapter=None):
    """An everyday-object frame with nobody in it, always in the flat cartoon style (P18: object
    prompts without style words came out as photos)."""
    scene(id, prompt + STYLE + ", clean empty corners", *lines, chapter=chapter)

# ---------- 開場（系列片頭之後直接進場景，不做濃縮；答案都不先講）----------
# The first picture is the problem itself: the password about to be typed on the café's network.
obj("cafe-tablet", "Close-up of a child's two small hands holding " + TABLET + " on a sunny café table beside a mug of cocoa, a big bright window behind",
    k("所長，我在咖啡店！", "急著報案的語氣"), k("我要用店裡的免費網路，登入遊戲。"),
    chapter="咖啡店裡，網址多一個 S")
# Thumbnail shot (fixed before keyframes, explainer-series/README.md): the kid big and centred, the tablet in hand.
kid("kid-cafe-q", K("holding a small tablet up in front of her chest with both hands and frowning at it in puzzlement, in the exact centre of the picture", where=CAFE),
    k("媽媽叫我先看網址，", "認真轉述"), k("開頭要是 HTTPS，才能打密碼。"),
    k("可是不就多一個 S？", "不服氣"))
chief("chief-listen", C("leaning forward with a curious smile, one hand on her chin", close=True),
      c("你覺得多一個 S，沒差多少？", "接住上一句"),
      k("密碼還不是一樣要傳出去！", "篤定"))
chief("chief-promise", C("holding up one finger with a warm inviting smile"),
      c("多一個 S，你的密碼在路上，差的比你想的多；", "賣關子"),
      c("可是也有些事，它根本不管。", "賣關子", "S:limits"),
      c("連網址旁邊那個小鎖頭，很多人都看錯了。", None, "S:lock"))
kid("kid-main-q", K("looking down at a small tablet in her hands with a thinking frown", where=CAFE),
    k("那到底差在哪裡？", "句尾上揚", "S:main"))

# ---------- 第一章：密碼要經過好多人的手 ----------
kid("kid-direct-guess", K("pointing out through the glass door at the busy sunny street outside with a confident grin", close=True, where="standing by the glass door of a cosy café with a tall potted plant,"),
    k("不是直接飛到", "很有把握的錯猜"), k("遊戲公司那裡嗎？", "句尾上揚", "S:direct"), chapter="密碼要經過好多人的手")
obj("router-shelf", "Close-up of a small plain white wireless router with two short antennas and tiny green lights on a wooden café shelf beside a potted plant",
    c("不是喔。它先到咖啡店的無線網路機器，", "接住上一句", "P:direct"),
    c("再交給網路公司，一站轉一站，"),
    c("經過好多台負責轉送的電腦，才到遊戲公司。"))
kid("kid-see-q", K("peering suspiciously at a small white router on a shelf, her face close to it", close=True, where=CAFE),
    k("那些機器，", "懷疑"), k("看得到我傳了什麼嗎？", "句尾上揚", "S:see"))
chief("chief-classroom", C("holding up " + LETTER + " between two fingers with a playful smile"),
      c("我們用上課傳信來想。"),
      c("你要把一封信，傳給教室另一頭的好朋友。"))
obj("classroom-pass", "Wide shot of a sunny classroom with rows of small wooden desks, one small folded cream letter resting on the corner of a desk halfway across the room, green chalkboard wall blurred behind",
    c("中間要經過好幾個同學的手。"),
    c("咖啡店的機器、網路公司，就是這些同學。"))
kid("kid-open-note", K("holding up a small folded open letter and peeking inside it with a sly grin", close=True, where=CLASS),
    k("信沒封起來的話……", "想像"),
    c("每個經手的人都能打開看，甚至改幾個字再傳下去。"))
chief("chief-chrome-help", C("holding a small phone up beside her face with a serious honest smile"),
      c("Chrome 的說明就這樣寫：沒有私密連線的網站，"),
      c("別人可能看到、也可能改掉你傳的東西。", None, "P:see"))
kid("kid-nice", K("crossing her arms with a doubtful pout", where=CLASS),
    k("可是我的同學", "不服氣"), k("人都很好啊！"))
chief("chief-assume", C("nodding with a kind smile, both palms open", close=True),
      c("大部分是。可是你沒辦法挑，誰來幫你傳。"))
chief("chief-tls", C("holding up " + LETTER + " and pointing at its red seal with a serious smile"),
      c("所以這個 S 背後的規則，叫 TLS，"),
      c("它的規格寫：就算路上的人能完全控制網路，保護也要成立。"))
kid("kid-s-q", K("tilting her head with a puzzled face, one finger on her chin", close=True, where=CAFE),
    k("那 S 到底", "好奇"), k("是什麼意思？", "句尾上揚", "S:s"))
chief("chief-secure", C("tapping a small tablet she holds with a bright explaining smile"),
      c("S 是英文「安全」那個字。", "接住上一句", "P:s"),
      c("HTTPS，就是網頁的往來，用 TLS 加密的版本。"))
kid("kid-seal-guess", K("pressing a small cream envelope shut between her palms with a pleased grin", where=CLASS),
    c("加密，就是把內容變成，只有你和對方看得懂。"),
    k("那把信封起來，", "很有把握"), k("就好了吧？", "章尾停住，句尾上揚", "S:sealonly"))

# ---------- 第二章：對面真的是遊戲公司嗎 ----------
chief("chief-impostor", C("raising one hand with an honest careful smile", close=True),
      c("封起來，也要封給對的人。", "接住上一句", "P:sealonly"),
      c("要是傳到一半，有人假裝是遊戲公司收下，"),
      c("你封得再好，也是把信交給他。"), chapter="小問想確認，對面是不是遊戲公司")
obj("street-ask", "Wide shot of a sunny crossroads with small shops and green trees, one tiny cartoon child on the pavement asking the way from a friendly cartoon postman who points down a side street",
    c("而且出發前，平板要先問「這個網址在哪裡」，"),
    c("那一問的回答，也可能被路上的人動手腳。"))
kid("kid-who-q", K("holding a small tablet close and squinting at it with narrowed curious eyes", close=True, where=CAFE),
    k("那我怎麼知道，", "追問"), k("對面真的是遊戲公司？", "句尾上揚", "S:who"))
chief("chief-card", C("holding up " + CARD + " beside her face with a proud smile"),
      c("網站會拿出一張證件，叫做憑證。", None, "P:who"),
      c("上面寫著網站的名字，還印著一顆專屬印章的圖樣，"),
      c("那顆章，只有這個網站自己拿著。"))
obj("card-close", "Close-up of " + CARD + " lying on a wooden school desk in sunshine",
    c("瀏覽器先看：證件上的名字，跟網址列上的一樣嗎？"),
    k("證件是誰發的？", "追問", "S:issuer"), k("自己做一張就好啦！", "調皮"))
chief("chief-ca", C("shaking her head gently with a kind smile, one finger raised", close=True),
      c("自己做的，瀏覽器不收。要找專門發憑證的機構。"),
      c("有一個免費發憑證的機構，在官網寫了它怎麼查："))
obj("desk-drawer", "Close-up of a small wooden school desk with its drawer pulled half open and one small golden card resting inside the drawer, sunny classroom softly blurred behind",
    c("例如請你在自己網站的固定位置，放一個它指定的檔案，"),
    c("再從好幾個不同的地方，同時連過來看。", None, "P:issuer"))
chief("chief-drawer", C("holding up one small golden card between two fingers with a playful smile", close=True),
      c("就像要你在自己座位的抽屜，放一張指定的小卡。"))
kid("kid-good-q", K("leaning forward with both hands on a desk and a hopeful questioning face", where=CLASS),
    k("那它有查，", "追問"), k("網站是不是好人嗎？", "句尾上揚", "S:good"))
chief("chief-control", C("shaking her head with a calm honest smile", close=True),
      c("沒有。它查的是，你管不管得了這個網址；", None, "P:good"),
      c("不是網站的人好不好、內容能不能信。"))
kid("kid-gem", K("gasping with wide surprised eyes and one hand over her open mouth, a small tablet in her other hand", close=True, where=CAFE),
    k("啊！同學剛剛傳給我一個連結，", "突然想起"),
    k("說點進去送免費寶石！"),
    k("它也是 HTTPS 耶！", "句尾上揚", "S:gem"))
chief("chief-phishing", C("raising her eyebrows with a careful warning smile, one finger raised"),
      c("那就要小心了。Chrome 團隊寫過："),
      c("幾乎所有的釣魚網站都用 HTTPS。"))
chief("chief-phish-def", C("pretending to cast a tiny fishing rod with one hand and a mischievous smile"),
      c("釣魚網站，就是假裝成別人、騙你打密碼的網站。"),
      c("騙子替自己那個長得很像的網址，一樣領得到證件。"))
obj("tablet-lock", "Close-up of " + TABLET + " lying on a sunny café table",
    c("瀏覽器很早就在網址旁邊畫一個小鎖頭，代表連線有加密。"),
    k("我看到的，", "指著平板"), k("就是這個鎖頭！"))
chief("chief-tune", C("holding a small tablet up beside her face with a thoughtful smile", close=True),
      c("他們的研究發現，"),
      c("只有百分之十一的受試者，真的懂這個鎖頭的意思。", None, "P:lock"))
chief("chief-tune-2", C("swapping a small tablet from one hand to the other with a gentle knowing smile"),
      c("二〇二三年，他們宣布把鎖頭換成別的圖示，"),
      c("免得大家以為，有鎖就是好網站。"),
      k("那瀏覽器為什麼要相信", "追問"), k("發證件的機構？", "句尾上揚", "S:chain"))
obj("cards-stairs", "Close-up of three plain cream cards standing in a row like little stairs on a wooden desk in sunshine, each one a step higher, the tallest card golden",
    c("因為機構自己也有證件，蓋著更上面那一層的章。"),
    c("一層蓋一層往上接，最上面那張，叫根憑證。"))
chief("chief-root", C("holding both hands together in front of her chest with a warm reassuring smile"),
      c("你的瀏覽器或手機系統，一開始就內建一組根憑證，", None, "P:chain"),
      c("像你本來就認得校長，看到校長的章就放心。"))
kid("kid-mistake-q", K("biting her lip with a worried frown, both hands holding a small tablet", where=CAFE),
    k("要是機構不小心，", "擔心"), k("發錯了證件呢？", "句尾上揚", "S:ct"))
obj("glass-case", "Wide shot of a tall glass display cabinet in a bright school hallway, filled with neat rows of identical plain cream cards standing on glass shelves, sunlight through a window",
    c("現在 Chrome 和 Safari 要求，"),
    c("憑證要登記在公開的帳本上。"),
    c("這些帳本只能加、不能刪，誰都能翻。"))
chief("chief-ct", C("holding a small phone up and smiling at it as if it just buzzed", close=True),
      c("網站主人還能訂閱通知：有人用我的名字拿到憑證，", None, "P:ct"),
      c("登記進去之後，就會收到通知。"))
kid("kid-fail-q", K("holding a small tablet out at arm's length and frowning at it", where=CAFE),
    k("那檢查沒過，", "追問"), k("會怎麼樣？", "句尾上揚", "S:fail"))
chief("chief-warning", C("holding up one flat palm like a polite stop gesture, a serious kind face"),
      c("像 Chrome，會整頁跳出警告：你的連線不是私人連線。", None, "P:fail"),
      c("它的說明寫，問題可能出在網站、網路，或你的裝置。"))
kid("kid-carry-q", K("holding a small sealed cream envelope up with a thinking frown", close=True, where=CLASS),
    k("好，找對人了。", "點頭"),
    k("那信要怎麼封，", "追問"), k("才不會被同學拆開？", "章尾停住，句尾上揚", "S:carry"))

# ---------- 第三章：先調顏色，再封信 ----------
chief("chief-secret", C("holding one finger to her lips with a playful secretive smile", close=True),
      c("寫信以前，兩邊要先有一個只有彼此知道的秘密。", "接住上一句"),
      k("可是傳過去的東西，", "不相信"), k("大家都看得到啊！", None, "S:mix"), chapter="先調顏色，再封信")
obj("paint-cups", "Close-up of three small round paint cups on a wooden desk in sunshine, one filled with bright yellow paint, one with red paint, one with blue paint, a small paintbrush resting beside them",
    c("用調顏料來想。先講好一個大家都知道的顏色，"),
    c("兩個人再各自偷偷加一種，只有自己知道的顏色。"))
chief("chief-mix", C("holding a small paint cup filled with orange paint up in one hand with a delighted smile"),
      c("把調好的傳給對方，收到的人，再加上自己那一種。"),
      c("最後兩邊調出同一個顏色；"),
      c("傳信的同學只看過半成品，調不出來。", None, "P:mix"))
chief("chief-math", C("wagging one finger with an honest playful smile", close=True),
      c("這只是比喻，真的做法是數學。不過規格寫得很清楚："))
obj("two-cups", "Close-up of two identical small round paint cups filled with the same deep brown paint standing side by side on a wooden desk in sunshine",
    c("第一步就是交換這種資料，之後的往來全部封起來，"),
    c("連剛剛那張證件，也是封好才送。"))
kid("kid-record-q", K("holding a small toy cassette recorder up beside her ear with a sly grin", where=CLASS),
    k("要是有人先把整段錄下來，", "想到壞點子"), k("以後再慢慢解呢？", "句尾上揚", "S:record"))
chief("chief-erase", C("brushing her two palms against each other as if wiping them clean, a confident smile", close=True),
      c("這次調出的顏色，用完就丟。", "接住上一句"),
      c("規格寫：就算以後網站的章被偷，"),
      c("只要這次的秘密已經丟掉，以前錄下的也解不開。", None, "P:record"))
kid("kid-copy-q", K("holding up a small cream card and pretending to photocopy it with a sly grin", where=CLASS),
    k("可是證件，", "抓到漏洞"), k("可以影印吧？", "句尾上揚", "S:copy"))
chief("chief-stamp", C("pressing an imaginary stamp down onto her open palm with a confident smile"),
      c("可以。所以光給證件不夠，網站還要當場蓋章。", "接住上一句"),
      c("影印的人，沒有那顆章。", None, "P:copy"))
kid("kid-swap-q", K("pretending to secretly swap two small paint cups on a desk with a mischievous grin", where=CLASS),
    k("要是傳信的同學，", "追問"), k("偷偷把顏色換掉呢？", "句尾上揚", "S:swap"))
chief("chief-stamp-all", C("sweeping one hand slowly from left to right in front of her with a calm explaining smile", close=True),
      c("網站那一章，是蓋在剛剛整段來回上，包括顏色。"),
      c("瀏覽器拿證件上的圖樣來對；"),
      c("顏色被換過，章就對不上，連線直接斷掉。", None, "P:swap"))
chief("chief-finished", C("giving a small thumbs-up with a pleased smile"),
      c("最後兩邊再對一次帳：整段來回，"),
      c("我看到的跟你看到的一樣嗎？對上了，才開始寄真正的信。"))
obj("sealed-letter", "Close-up of " + LETTER + " lying on a wooden school desk in warm sunshine",
    c("接下來每一封信，都用那個只有你們知道的顏色封起來。", None, "P:carry"),
    c("路上有人改了一點點，信就打不開；規格要求這時直接斷線。"))
obj("envelope-front", "Close-up of the front of a small cream envelope held shut by a long strip of red wax seal running across its whole face, lying on a sunny wooden desk",
    c("信封外面還寫著這封信有多長；"),
    c("這幾個字也算在封條裡，看得到，改不了。"))
kid("kid-replay-q", K("holding a small sealed envelope up high and grinning mischievously as if about to copy it", close=True, where=CLASS),
    k("要是有人把我那封", "想到壞點子"), k("「我要買寶石」，"), k("抄下來再寄一次呢？", "句尾上揚", "S:replay"))
chief("chief-numbers", C("counting on her fingers with a thoughtful smile", close=True),
      c("每封信都有編號，兩邊各自從零開始數，寄一封加一。"),
      c("編號不寫在外面，是混進封條裡。"))
obj("letter-row", "Wide shot of a neat row of six small cream envelopes each closed with a round red wax seal, lined up along a sunny wooden windowsill",
    c("抄來的舊信再送一次，或是順序被調換，", "接住上一句"),
    c("編號就對不上，打不開。", None, "P:replay"),
    k("所以每一封，", "開心"), k("都不能重寄！"))
chief("chief-exception", C("holding up one finger with an honest careful smile"),
      c("有一個例外，規格自己用「重要提醒」標了出來。"),
      k("什麼例外？", "句尾上揚", "S:early"))
obj("early-letter", "Close-up of one small cream envelope with a round red wax seal sliding ahead of a neat stack of other envelopes across a sunny wooden desk",
    c("你跟網站以前連過，瀏覽器可以用上次留下的秘密，"),
    c("讓第一封信搶先送出，省掉一次來回。"))
chief("chief-early", C("frowning slightly with a thoughtful serious face, one hand raised", close=True),
      c("規格說，這封搶先的信，不保證不會被重送；"),
      c("有人抄下來再寄，可能讓買東西這種事發生兩次。", None, "P:early"))
kid("kid-hole", K("pointing one finger at a small sealed envelope on a desk with a shocked frown", close=True, where=CLASS),
    k("那不就是一個洞？", "吃驚"),
    c("對。所以規格另外寫了幾種方法，讓網站自己擋。"))
chief("chief-close", C("waving one hand in a small goodbye gesture with a warm smile", close=True),
      c("還有，寄完的時候，最後一封會說：我講完了。"),
      c("信半路被剪斷，對方才分得出來。"))
kid("kid-nothing-q", K("hugging a small sealed envelope to her chest with a proud satisfied grin", where=CLASS),
    k("封條、編號都有了，", "得意"),
    k("路上的人，", "很有把握"), k("什麼都看不到了吧？", "章尾停住，句尾上揚", "S:nothing"))

# ---------- 第四章：封條管不到的地方 ----------
chief("chief-length", C("holding her thumb and finger apart as if measuring thickness, a careful smile", close=True),
      c("還看得到一些。規格寫得很直接：它不隱藏資料的長度。", "接住上一句", "P:nothing"), chapter="封好的信，還被看到了什麼")
obj("thick-thin", "Close-up of four small cream envelopes with red wax seals lying side by side on a sunny wooden desk, from one very thin to one very fat and puffy",
    c("信有多厚、多久寄一封，路上的人還是看得到。"),
    k("看厚度，", "不相信"), k("能看出什麼？", "句尾上揚", "S:thick"))
chief("chief-guess", C("tapping her chin with one finger and a thoughtful smile", close=True),
      c("規格提醒：看長度和時間，有時就猜得出你在做什麼，", None, "P:thick"),
      c("尤其是選擇不多的時候，像一個只放固定那些影片的網站。"))
obj("padded-letters", "Close-up of four small cream envelopes with red wax seals, all exactly the same puffy thickness, stacked neatly on a sunny wooden desk",
    c("網站可以在信裡塞空白，把信撐成一樣厚；"),
    c("可是要塞多少，規格沒有規定。"))
kid("kid-name-q", K("holding a small tablet close to her face with a worried frown", close=True, where=CAFE),
    k("那他們知道，", "擔心"), k("我在跟哪個網站說話嗎？", "句尾上揚", "S:name"))
chief("chief-name", C("nodding slowly with an honest serious face"),
      c("很可能。連線一開頭，瀏覽器會說它要找哪個網站，"),
      c("這個名字，平常是沒封起來的。", None, "P:name"))
obj("envelope-house", "Close-up of a small cream envelope with a round red wax seal, a big cheerful doodle of a little red-roofed house drawn on its front, lying on a sunny wooden desk",
    c("就像信封外面，寫著收件人。"),
    k("不能也封起來嗎？", "句尾上揚", "S:ech"))
chief("chief-ech", C("holding up two small envelopes, one tucked inside the other, with a pleased smile"),
      c("二〇二六年三月，一份新的規格正式發布，就在做這件事："),
      c("把收件人的名字，也放進裡面一層信封。", None, "P:ech"))
obj("tall-building", "Wide shot of one tall plain cream apartment building with many identical windows on a sunny street, small green trees in front",
    c("可是它自己也寫，光這樣還不夠。"),
    c("信最後送到哪一棟大樓，路上還是看得到；"))
chief("chief-same-building", C("holding both hands up shaped like a little roof with a thoughtful smile", close=True),
      c("不過很多網站常常住同一棟，"),
      c("所以信封上的名字，才是最明白的線索。"))
obj("street-ask-2", "Wide shot of a sunny crossroads with small shops and green trees, a friendly cartoon postman standing alone on the pavement pointing down a side street",
    c("還記得出發前，問「這個網址在哪裡」那一問嗎？"),
    c("那一問要是沒封，也會露出名字。"))
kid("kid-gem-back", K("looking down at a small tablet with an uneasy frown, one finger hovering above it", where=CAFE),
    k("那剛剛那個", "不安"), k("送寶石的連結……"))
chief("chief-endpoint", C("holding one hand flat over her heart with a serious caring face", close=True),
      c("這是最要緊的一點：封條只管路上。", None, "P:limits"),
      c("信到了對方手上，對方全部讀得到。"))
kid("kid-tell-q", K("clutching a small tablet with both hands and a worried pleading face", close=True, where=CAFE),
    c("對方是騙子，HTTPS 也會把密碼，好好送到騙子手上。"),
    k("那我要怎麼分？", "句尾上揚", "S:tell"))
chief("chief-check-name", C("pointing at a small tablet she holds with an encouraging smile"),
      c("Chrome 的說明也提醒：就算是安全的連線，"),
      c("也要看清楚網址列上的名字，是不是你要去的網站。", None, "P:tell"))
kid("kid-spot", K("pointing at a small tablet in her other hand with wide eyes and an excited open-mouthed grin", where=CAFE),
    k("我看到了！", "驚訝"), k("名字多了一個字母！", None, "P:gem"))

# ---------- 收尾 ----------
chief("chief-your-turn", C("leaning forward with an inviting grin, one hand open towards the viewer"),
      c("那你說，多一個 S，你的密碼在路上差了什麼？", "笑"), chapter="小問看清楚了")
kid("kid-got-it", K("holding a small sealed cream envelope up proudly with a big confident grin", where=CAFE),
    k("原來如此！", "恍然大悟"), k("密碼變成封好的紙條，", "篤定"),
    k("同學照樣傳，卻讀不到，", "篤定"), k("也冒充不了那個網址！", None, "P:main"))
chief("chief-opinion", C("smiling with her hands clasped, a thoughtful look", close=True),
      c("說得好。我覺得最妙的是，這個封條你每天都在用，"),
      c("卻從來沒有看見它。"))
obj("cafe-table", "Wide shot of a sunny café table by a big window with a mug of cocoa and a small tablet lying face down, a potted plant on the windowsill",
    k("我先去跟媽媽說，", "開心"), k("那個連結是假的！"))
# The outro is three pictures, no card, no stamp (series README §3.2, §10.1): the kid gives a thumbs-up.
kid("outro", "Waist-up medium shot of the girl with a big happy smile giving a big cheerful thumbs-up with one hand, bright morning light",
    k("下次打密碼，我先看名字！", "開心大聲"))
chief("outro-chief", "Waist-up medium shot of the chief holding up a small sealed cream envelope with a curious smile, filling the frame, a plain pale wall behind her, bright morning light",
      c("你收過名字很像、卻是假的網址嗎？", "問句上揚，像聊天"), c("留言告訴我們。"))
chief("outro-wave", "Waist-up medium shot of the chief waving goodbye with a warm smile, a plain pale wall behind her, bright morning light",
      c("想一起找生活裡的為什麼，就訂閱原來如此事務所。", "誠懇"))

# ---------- assemble ----------
WHAT = {"main": "多一個 S，密碼在路上差在哪裡", "limits": "有些事 HTTPS 根本不管，是哪些事",
        "direct": "密碼是不是直接飛到遊戲公司", "see": "路上的機器看不看得到我傳了什麼",
        "s": "S 是什麼意思", "sealonly": "把信封起來是不是就夠了",
        "who": "怎麼知道對面真的是遊戲公司", "issuer": "證件是誰發的、能不能自己做",
        "good": "發證件的機構有沒有查網站是不是好人", "gem": "送免費寶石的連結也是 HTTPS",
        "chain": "瀏覽器為什麼相信發證件的機構", "ct": "機構發錯證件怎麼辦",
        "fail": "檢查沒過會怎麼樣", "carry": "信要怎麼封才不會被傳信的人拆開",
        "mix": "大家都看得到，怎麼有只有兩人知道的秘密", "copy": "證件可以影印吧",
        "swap": "傳信的人偷換顏色怎麼辦", "replay": "抄下來再寄一次會怎樣",
        "early": "規格自己標出的例外是什麼", "nothing": "封好了，路上是不是什麼都看不到",
        "name": "別人知不知道我在跟哪個網站說話", "ech": "網站的名字能不能也封起來",
        "tell": "要怎麼分出騙人的網站",
        "lock": "釣魚網站也有 HTTPS，那鎖頭代表什麼", "record": "先錄下來以後再解行不行",
        "thick": "看信的厚度能看出什麼"}
# Latin terms the Mandarin voice must spell letter by letter (lexicon.json has "TLS": "T L S" already,
# HTTPS is missing there and this episode may not change that file); each spelled line carries say_for,
# exactly as P13 did for GPS. Drop an entry once lexicon.json has the term.
SAY = [("HTTPS", "H T T P S"), ("TLS", "T L S")]
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
    "series": {"slug": "sothatswhy", "episode": 29, "chapter": 1},
    # 2026-11-11 (README §9 停頓, §10.6): no fixed pause between lines, a short gap between scenes, beat-timed stills.
    "pauses": {"line_ms": 0, "scene_ms": 150},
    "still_motion": "beat",
    # The series bed from P15 on (explainer-series/README.md, PR #2048): sothatswhy-bed-r2.m4a, remade from P02's paid take.
    "music": {"track": "sothatswhy-bed-r2.m4a", "sha256": "9bb4ba6fd16feb4a7f352144b2d89e9648acbbbbaa2173c27a7eefbdb70f28c6", "gain_db": -20, "duck_db": -10},
    "characters": CHARACTERS, "loops": loops,
    "youtube": {
        "category_id": 27, "made_for_kids": False, "default_language": "zh-TW",
        "title": "網址多一個 S，資料在路上差了什麼？｜原來如此事務所",
        "description": "小問在咖啡店用免費網路登入遊戲，媽媽叫她先看網址開頭是不是 https。可是不就多一個 S 嗎？密碼還不是一樣要傳出去？\n\n"
                       "這一集，所長和小問用「上課傳信」來想：信要經過好幾個同學的手，就像你的資料要經過咖啡店的機器和網路公司。"
                       "先看怎麼確定對面真的是那個網站（網站的證件、免費發證件的機構只查你管不管得了網址、一路簽到瀏覽器內建的根憑證、公開的登記帳本），"
                       "再看兩邊怎麼在大家眼前調出只有彼此知道的秘密、怎麼把每封信封好又編上號，以及規格自己承認的例外；"
                       "最後看封條管不到的地方：信有多厚、寄給哪個網站，還有最重要的——HTTPS 只保護路上，不保證網站是好人，詐騙網站一樣有。\n\n"
                       "調顏料只是比喻，真正的做法是數學；插圖由 AI 生成，是示意。每個說法的出處列在下方參考資料。\n\n資料截至 " + CHECKED,
        "tags": ["HTTPS", "TLS", "網路安全", "憑證", "加密", "釣魚網站", "科普", "原來如此事務所"]},
    "thumbnail": {"template": "thumb", "data": {"headline": "多一個 S\n**差在哪？**", "sub": "密碼在路上，誰看得到", "shot": "kid-cafe-q", "subject": "right"}},
    "sources": [
        {"title": "RFC 8446, The Transport Layer Security (TLS) Protocol Version 1.3 (IETF, 2018)", "url": "https://www.rfc-editor.org/rfc/rfc8446", "checked_on": CHECKED},
        {"title": "RFC 9849, TLS Encrypted Client Hello (IETF, March 2026)", "url": "https://www.rfc-editor.org/rfc/rfc9849", "checked_on": CHECKED},
        {"title": "RFC 5280, Internet X.509 PKI Certificate and CRL Profile, §6.1 (IETF, 2008)", "url": "https://www.rfc-editor.org/rfc/rfc5280", "checked_on": CHECKED},
        {"title": "RFC 9110, HTTP Semantics, §4.2.2 and §4.3.4 (IETF, 2022)", "url": "https://www.rfc-editor.org/rfc/rfc9110", "checked_on": CHECKED},
        {"title": "Let's Encrypt, How It Works", "url": "https://letsencrypt.org/how-it-works/", "checked_on": CHECKED},
        {"title": "Let's Encrypt, Chains of Trust", "url": "https://letsencrypt.org/certificates/", "checked_on": CHECKED},
        {"title": "Certificate Transparency, How CT works", "url": "https://certificate.transparency.dev/howctworks/", "checked_on": CHECKED},
        {"title": "Chromium Blog, An Update on the Lock Icon (2023-05-02)", "url": "https://blog.chromium.org/2023/05/an-update-on-lock-icon.html", "checked_on": CHECKED},
        {"title": "Google Chrome Help, Check if a site's connection is secure", "url": "https://support.google.com/chrome/answer/95617?hl=en", "checked_on": CHECKED},
        {"title": "MDN Web Docs, HTTPS (glossary)", "url": "https://developer.mozilla.org/en-US/docs/Glossary/HTTPS", "checked_on": CHECKED},
        {"title": "MDN Web Docs, How does the Internet work?", "url": "https://developer.mozilla.org/en-US/docs/Learn_web_development/Howto/Web_mechanics/How_does_the_Internet_work", "checked_on": CHECKED},
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
assert body_chars <= 3300, f"body {body_chars} characters: keep under 3,300 (plan 11–13 min at 4.4 chars/s)"
cams = [s["data"]["camera"] for s in scenes]
assert all(not (a == b == c_) for a, b, c_ in zip(cams, cams[1:], cams[2:])), "three shots in a row with the same camera"

# ---------- script.md (the screenplay the owner reads; local CLI, no paid tool) ----------
r = subprocess.run(["node", os.path.join(ROOT, "tools", "video", "cli.mjs"), "script", "--slug", SLUG], cwd=ROOT, capture_output=True, text=True)
sys.stderr.write(r.stdout + r.stderr)
assert r.returncode == 0, "script.md was not written"
