"""Generate video.json for sothatswhy-p25-train-tunnel (原來如此事務所 對話版 P25).

Run `python3 build_scenes.py` from anywhere: it rewrites video.json next to this file and freezes
every shot's camera move in cameras.json (a shot keeps the camera it was first given, so deleting
a shot never shifts the others: the camera is in the keyframe cache key).
Edit lines and prompts here, never in video.json.
"""
import itertools, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = "sothatswhy-p25-train-tunnel"
CHECKED = "2026-11-14"

# ---------- series constants (2026-11-13 dialogue-explainer rules) ----------
VOICE = {
    "provider": "gemini",
    "name": "Sulafat",
    "style": "標準國語，咬字清楚，台北人平常說話的語調；溫暖清楚的解說主持人，像在跟一個好奇的朋友講道理，語速像節目主持人，一秒五個字以上，句與句緊接、不拖長尾音",
}
KID_VOICE = {
    "provider": "gemini",
    "name": "Leda",
    "style": "標準國語，咬字清楚，台北人平常說話的語調；好奇愛發問的年輕女生，像觀眾的嘴替，語氣輕快自然，語速像節目主持人，一秒五個字以上，句與句緊接、不拖長尾音",
}
SHEET = "character reference: one single full-body figure standing in the centre, facing the viewer in a slight three-quarter turn, relaxed friendly pose, both hands clearly drawn, plain empty cream background with nothing else in the picture, no turnaround, no second view, no seal, no stamp, no signature, no text"
CHARACTERS = [
    {
        "id": "chief",
        "name": "所長",
        "appearance": "a friendly middle-aged woman, the chief of a small question office, with round black glasses, shoulder-length dark hair with a streak of grey tied in a low ponytail, a warm smile, a mustard-yellow cardigan over a white blouse, ink-navy trousers, brown shoes, a yellow pencil tucked behind one ear",
        "voice": dict(VOICE),
        "sheet_prompt": SHEET,
    },
    {
        "id": "kid",
        "name": "小問",
        "appearance": "a curious eight-year-old girl with a short black bob haircut with straight bangs and one small cowlick sticking up on top, large round eyes, wearing a navy raincoat-style jacket with a mustard-yellow hood, white sneakers, both hands free",
        "voice": dict(KID_VOICE),
        "sheet_prompt": SHEET,
    },
]

TRAIN = "a sleek all-white high-speed passenger express with a smooth unmarked body"
BANNED = re.compile(r"\b(no|not|without|text|blank|lamp|night|notebook|sign|signs|paper|poster|screen|book|calendar|whiteboard|cream|cartoon)\b", re.I)

CAMS = itertools.cycle(["push in", "pan left", "pull out", "drift", "tilt up", "pan right", "push in", "tilt down", "pull out", "drift"])
CAM_FILE = os.path.join(HERE, "cameras.json")
FROZEN = json.load(open(CAM_FILE, encoding="utf-8")) if os.path.exists(CAM_FILE) else {}

S = []


def _shot(id, prompt, chars, lines, chapter):
    assert not BANNED.search(prompt), (id, BANNED.search(prompt).group(0))
    cam = FROZEN.get(id) or next(CAMS)
    S.append(
        dict(
            id=id,
            chapter=chapter,
            template="shot",
            data=dict(prompt=prompt, camera=cam, visual="still", characters=list(chars)),
            lines=list(lines),
        )
    )


def kid(id, prompt, *lines, chapter=None):
    _shot(id, prompt.rstrip(". "), ["kid"], lines, chapter)


def chief(id, prompt, *lines, chapter=None):
    assert prompt.startswith(("Waist-up", "Head-and-shoulders")), id
    _shot(id, prompt.rstrip(". "), ["chief"], lines, chapter)


def scene(id, prompt, *lines, chapter=None):
    assert prompt.startswith(("Close-up", "Medium shot", "Wide view", "Overhead view", "Low-angle view")), id
    _shot(id, prompt.rstrip(". "), [], lines, chapter)
    S[-1]["data"]["nobody"] = True


def k(t, e=None, tag=None, pause=None):
    return ("kid", t, e, tag, pause)


def c(t, e=None, tag=None, pause=None):
    return ("chief", t, e, tag, pause)


# ---------- 開場（片頭後 20 秒內直接進反差問題，不寒暄、不先破梗）----------
kid(
    "platform-nose",
    "Waist-up medium shot of the girl on the right side of the frame on a sunny railway platform pointing with wide curious eyes at the long pointed nose of " + TRAIN + " parked on the left",
    k("所長！新幹線的車鼻子，", "興奮指著車頭"),
    k("拉到十五公尺那麼長，", "比出誇張長度"),
    k("是為了切開風、減風阻嗎？", "很有把握的錯猜，句尾上揚", "S:wind"),
    chapter="長鼻子不是為了破風",
)
chief(
    "chief-not-wind",
    "Waist-up medium shot of the chief shaking her head with a calm knowing smile and raising one finger in front of a plain pale wall",
    c("大家都以為長鼻子只是為了破風，", "親切反轉"),
    c("但工程師真正怕的對手，在山洞裡。", "賣關子", "S:tunnel"),
)
kid(
    "kid-taiwan-q",
    "Head-and-shoulders close-up of the girl tilting her head with a puzzled frown and holding her two hands apart on the railway platform",
    k("山洞裡有什麼可怕的？", "追問"),
    k("而且台灣高鐵跑那麼快，", "疑惑"),
    k("鼻子怎麼比日本還短？", "句尾上揚", "S:twshort"),
)
chief(
    "chief-open-promise",
    "Waist-up medium shot of the chief smiling warmly and holding up a small toy locomotive in one hand",
    c("台灣高鐵跑得比日本原型車快，鼻子卻真的比較短。", "接住問題"),
    c("我們馬上跟著列車衝進山洞找答案！", "節奏明快"),
)

# ---------- 第一章：山洞出口的那一聲碰 ----------
kid(
    "kid-wind-front",
    "Waist-up medium shot of the girl pushing her open palm forward through the air as if feeling strong wind",
    k("火車開到時速三百公里，", "認真推理"),
    k("迎面撞上來的風超大，", "比手勢"),
    k("阻力不都在車頭嗎？", "句尾上揚"),
    chapter="山洞出口的那一聲碰",
)
scene(
    "long-train-wind",
    "Wide view from the side of " + TRAIN + " gliding across a green meadow, soft blue airflow ribbons skimming along the long side walls",
    c("流線型的車頭，確實能減掉一點風阻。", "肯定"),
    c("但日本鐵道綜合技術研究所算過，高鐵是十幾節連在一起的長列車。", "清楚解說"),
)
scene(
    "side-gap-drag",
    "Close-up of two sleek carriages coupled together, swirling blue air currents brushing along the side walls and the narrow gap between carriages",
    c("整列車大半的空氣阻力，其實在長長的車身側面和車廂之間，", "點出關鍵"),
    c("並不在最前面的車頭。", "肯定", "P:wind", 100),
)
kid(
    "kid-then-why",
    "Head-and-shoulders close-up of the girl leaning forward with her eyebrows raised and both hands spread open",
    k("既然大半風阻在車身側面，", "抓到矛盾"),
    k("幹嘛把車頭拉那麼長？", "句尾上揚"),
)
scene(
    "tunnel-boom",
    "Wide view of a concrete mountain tunnel exit in a green valley, concentric pressure ripples bursting out of the tunnel mouth",
    c("因為火車一鑽進窄山洞，怪事就發生了。", "壓低聲音"),
    c("火車才剛從這頭進洞，幾公里外的出口卻突然「碰」一聲巨響！", "誇張有畫面"),
)
scene(
    "window-rattle",
    "Close-up of a wooden cottage window frame near a mountain tunnel exit vibrating with small motion lines as a low pressure wave passes by",
    c("那股衝擊波不只有像放炮的聲音，", "清楚"),
    c("連聽不見的低頻震動，都會讓附近住家的門窗喀喀作響。", "清楚", "P:tunnel"),
)
kid(
    "kid-sonic-guess",
    "Waist-up medium shot of the girl making a dramatic burst gesture with both hands by her ears, eyes wide",
    k("洞口會像放炮一樣響，", "驚訝"),
    k("難道是火車跑得比聲音快，", "很有把握的錯猜"),
    k("撞出超音速的音爆嗎？", "句尾上揚", "S:sonic"),
)
chief(
    "chief-not-sonic",
    "Waist-up medium shot of the chief smiling and holding up four fingers with one finger folded down",
    c("很多人俗稱它「隧道音爆」，但火車完全沒有超音速喔。", "澄清迷思"),
    c("聲音一小時跑一千兩百多公里，高鐵最高速只有音速的四分之一。", "數字清楚"),
)
chief(
    "chief-wave-runs",
    "Waist-up medium shot of the chief pointing one finger swiftly across from left to right",
    c("真正用音速在山洞裡狂奔的，不是火車，", "強調"),
    c("而是被火車猛力擠出去的那團空氣！", "揭曉", "P:sonic", 100),
)
scene(
    "bicycle-pump",
    "Close-up of a hand air pump pushing air down a narrow clear tube beside " + TRAIN + " entering a narrow mountain tunnel",
    c("把山洞想成一根細管子，火車就是打氣筒的活塞。", "比喻鮮明"),
    c("在外面空曠處，空氣被推開，往旁邊躲就好了，對吧？", "問句互動"),
)
scene(
    "tunnel-trapped-air",
    "Medium shot inside a narrow concrete tunnel showing " + TRAIN + " compressing a glowing blue wave of air tightly against the tunnel walls",
    c("可是山洞裡四面都是牆，空氣沒地方逃，", "因果清楚"),
    c("就被車頭往前硬擠，在隧道裡形成一道壓縮波。", "清楚"),
)
scene(
    "wave-out-exit",
    "Wide view of a mountain tunnel cut open from the side: " + TRAIN + " has just entered the left portal while a bright blue air pulse pops out of the right portal",
    c("這道壓縮波用音速往另一頭狂奔，比火車快上好幾倍。", "節奏加快"),
    c("火車才剛進洞，壓縮波已經先衝到出口，放出一記脈衝。", "清楚"),
)
chief(
    "chief-micro-name",
    "Head-and-shoulders close-up of the chief holding up one finger with a gentle smile",
    c("它的正式名字叫「隧道微氣壓波」，", "清楚"),
    c("日本還幫它取了個外號，叫「隧道咚」。", "親切"),
)
kid(
    "kid-old-trains",
    "Head-and-shoulders close-up of the girl resting her chin on one hand with a skeptical squint",
    k("可是以前的火車也會過山洞，", "懷疑"),
    k("為什麼到了一九七五年，", "追問"),
    k("這個聲音才突然變嚴重？", "句尾上揚", "S:slab"),
)
scene(
    "sanyo-1975",
    "Wide view of " + TRAIN + " entering a long mountain tunnel along a coastal valley while engineers in hard hats listen near the distant portal",
    c("一九七五年，日本山陽新幹線往南延伸到博多，", "歷史場景"),
    c("通車前試車時，長隧道的出口突然砰砰作響。", "懸念"),
)
scene(
    "ballast-gravel",
    "Close-up of steel railway tracks resting on a bed of grey crushed gravel stones with tiny air pockets absorbing a soft blue wave",
    c("研究人員查出來，祕密在鐵軌底下的地板！", "轉折"),
    c("早期鐵軌下鋪滿碎石頭，縫隙像吸音海綿，會把波磨緩。", "解釋機制"),
)
scene(
    "slab-steepening",
    "Close-up of steel railway tracks mounted on a smooth solid concrete slab inside a tunnel while a blue pressure wave grows into a steep cliff",
    c("但那段新隧道為了省維修，改用平硬的水泥板軌道。", "對比"),
    c("少了碎石緩衝，波在長隧道裡越跑越陡，出口就特別響！", "清楚", "P:slab", 100),
)
kid(
    "kid-slow-down-q",
    "Waist-up medium shot of the girl tilting her head and holding two fingers slightly apart",
    k("那火車只要開快一點點，", "推理"),
    k("洞口的碰聲也只大一點點嗎？", "句尾上揚", "S:cube"),
)
chief(
    "chief-speed-cubed",
    "Waist-up medium shot of the chief raising three fingers with a serious expression, dramatic rising curve hand gesture and luminous shockwave ripples",
    c("沒那麼便宜！微氣壓波大約跟車速的三次方成正比。", "強調三次方"),
    c("車速加快一成，出口那聲碰，粗估就會增強三成以上！", "數字放慢", "P:cube"),
)
chief(
    "chief-ch1-hook",
    "Waist-up medium shot of the chief leaning forward slightly with an inviting questioning look",
    c("如果不讓火車慢下來，", "放慢"),
    c("要怎麼在進洞的第一瞬間，把那道波壓下去？", "章尾鉤子", "S:steep"),
)

# ---------- 第二章：長鼻子怎麼把「陡坡」變「緩坡」 ----------
kid(
    "kid-absorb-guess",
    "Waist-up medium shot of the girl pressing both hands together like squeezing a soft sponge",
    k("把車頭做成長鼻子，", "猜測"),
    k("是為了像海綿一樣，", "比手勢"),
    k("把空氣壓力吸掉嗎？", "句尾上揚"),
    chapter="把陡坡拉成緩坡",
)
chief(
    "chief-steepness",
    "Waist-up medium shot of the chief drawing a steep cliff in the air with one hand and a gentle slope with the other",
    c("長鼻子不會吃掉空氣，它改的是壓力上升的「陡度」。", "修正直覺"),
    c("出口那聲碰有多響，關鍵在壓力第一瞬間升得多陡。", "核心原理"),
)
scene(
    "blunt-nose-cliff",
    "Close-up of a blunt flat locomotive front slamming into a tunnel mouth and pushing air into a tall steep red cliff wave",
    c("如果車頭像個方盒子，一頭撞進山洞，", "生動比喻"),
    c("就像一巴掌猛拍水面，壓力瞬間衝上懸崖。", "清楚"),
)
scene(
    "long-nose-slope",
    "Close-up of a long tapered nose gliding into a tunnel mouth, easing the air into a low gentle blue slope",
    c("但把車鼻拉長，只有尖端先進洞，再一寸一寸變粗。", "放慢"),
    c("壓力從陡坡變成緩坡，出口就不會炸出巨響了。", "回收", "P:steep", 100),
)
kid(
    "kid-cone-guess",
    "Head-and-shoulders close-up of the girl bringing her fingertips together into a sharp pointed cone shape",
    k("那把車頭削成尖尖的圓錐，", "馬上追問"),
    k("像鉛筆尖一樣，", "比出尖角"),
    k("效果是不是最好？", "句尾上揚", "S:shape"),
)
scene(
    "three-shapes-test",
    "Medium shot of a laboratory table showing three smooth nose models side by side: a rounded ellipsoid, a straight cone, and a sleek paraboloid nose",
    c("日本鐵道綜合技術研究所拿圓錐和橢圓模型做過實驗。", "實驗證據"),
    c("圓錐不是第一名！它越往後截面增加越快，壓力還是會暴衝。", "指出問題"),
)
scene(
    "paraboloid-winner",
    "Close-up of a sleek rotational paraboloid nose model with evenly spaced glowing blue rings along its length showing steady area growth",
    c("效果最好的叫做「旋轉拋物體」：", "揭曉最佳形狀"),
    c("車頭每鑽進洞裡一公分，推開的空氣量都一模一樣，壓力才爬得最順暢！", "清楚", "P:shape", 100),
)
scene(
    "slim-round-body",
    "Close-up front cross-section inside a circular tunnel comparing a wide boxy carriage on the left with a slimmer rounded carriage leaving generous air space on the right",
    c("除了拉長鼻子，工程師還把車廂截面做得更細、更圓。", "補充第二招"),
    c("車身佔掉的空間變小，推進去的空氣變少，壓力波也減輕。", "清楚"),
)
kid(
    "kid-portal-hood-q",
    "Waist-up medium shot of the girl pointing toward a mountain tunnel entrance with a curious look",
    k("那山洞自己呢？", "轉移視角"),
    k("山洞口能不能也幫忙洩氣？", "句尾上揚", "S:hood"),
)
scene(
    "tunnel-hood",
    "Wide view of a mountain tunnel entrance fitted with an extended grey concrete hood angled at forty-five degrees with side vent windows letting puffs of blue air escape",
    c("日本大部分水泥板軌道的隧道口，都裝了「緩衝罩」。", "稱讚"),
    c("火車進洞時，空氣先從罩子側窗漏掉一部分，不會全灌進去。", "具體機制", "P:hood"),
)
chief(
    "chief-ch2-hook",
    "Waist-up medium shot of the chief holding a small sleek train model with a mysterious smile",
    c("可是面對更高速度的考驗，光靠那時的緩衝罩還不夠，", "鋪墊"),
    c("工程師必須向大自然搬救兵了。", "章尾鉤子", "S:bird"),
)

# ---------- 第三章：翠鳥給的靈感，與實驗算出來的答案 ----------
chief(
    "chief-500-challenge",
    "Waist-up medium shot of the chief holding a model of a long-nosed express and looking thoughtful",
    c("一九九〇年代，西日本鐵路開發第一款跑上最高速的五百系。", "進入故事"),
    c("但山陽線一半是隧道，截面約六十五平方公尺，非常窄。", "點出難題"),
    chapter="翠鳥靈感與超級電腦",
)
scene(
    "complaint-400m",
    "Wide view of a mountain tunnel portal with sound wave rings reaching a small house four hundred metres away on a hillside",
    c("據工程師仲津英治說，當時四百公尺外的住戶都來抱怨，", "有出處歸屬"),
    c("團隊甚至一度放棄時速三百五十公里以上的測試。", "清楚"),
)
kid(
    "kid-compressed-feel",
    "Waist-up medium shot of the girl hunching her shoulders inward as if being squeezed from all sides",
    k("四百公尺外都受不了！", "驚嘆問題規模"),
    k("那他們去哪裡找救兵？", "追問"),
)
scene(
    "kingfisher-dive",
    "Close-up of a small blue-and-orange kingfisher bird diving straight down from bright sky into a clear pond with only a tiny neat ring of water droplets",
    c("仲津也是野鳥協會會員。有人說進洞時「車廂像被壓縮」，", "人物與靈感"),
    c("讓他想到翠鳥：高速衝進水裡，濺起的水花卻非常小！", "連結物理", "P:bird", 100),
)
kid(
    "kid-copy-beak-q",
    "Head-and-shoulders close-up of the girl holding up an imaginary magnifying glass to her eye with a playful grin",
    k("所以工程師就拿翠鳥的嘴巴，", "常見迷思"),
    k("直接照著描出車頭嗎？", "句尾上揚", "S:copy"),
)
scene(
    "pipe-bullet-test",
    "Close-up in a laboratory of a transparent high-speed launch tube firing tiny bullet-shaped model trains while digital sensors measure shockwave pressures",
    c("不是照著描喔！翠鳥是靈感，形狀是實驗算出來的。", "破解迷思"),
    c("團隊把小模型射進細管測壓力波，還用超級電腦模擬。", "實驗過程"),
)
scene(
    "computer-matches-beak",
    "Close-up comparing a glowing blue paraboloid curve on a laboratory display stand beside the sleek beak-to-head profile of a kingfisher bird",
    c("結果電腦算出來的理想曲線，拿去跟翠鳥一比，", "對比"),
    c("竟然跟翠鳥從鳥嘴到額頭的形狀幾乎一模一樣！", "驚人巧合", "P:copy", 100),
)
kid(
    "kid-biologist-q",
    "Waist-up medium shot of the girl pointing with curious round eyes at a small model of a bird beak",
    k("電腦算出來的跟鳥嘴一樣！", "連結線索"),
    k("那生物學家有去測過翠鳥的嘴嗎？", "追問", "S:bio"),
)
scene(
    "kingfisher-beak-study",
    "Close-up comparing sleek narrow diving kingfisher beaks gliding smoothly into water with gentle blue streamlines around the beak-to-head curve",
    c("二〇一九年，生物學家拿七十多種翠鳥做跳水實驗，", "科學驗證"),
    c("證實天天高速插水抓魚的鳥嘴曲線，阻力最小、水花最少！", "呼應工程", "P:bio"),
)
kid(
    "kid-pantograph-q",
    "Head-and-shoulders close-up of the girl putting one hand above her head like a roof antenna and tilting her head",
    k("山洞口的碰聲解決了，", "推進下一步"),
    k("那車頂接電線的架子不會吵嗎？", "句尾上揚", "S:owl"),
)
scene(
    "owl-feather",
    "Close-up side-by-side view of a brown owl wing feather with fine comb-like serrations along its edge and a streamlined wing-shaped roof pantograph",
    c("車頂接電線的集電弓，高速切開空氣時也很吵。", "肯定追問"),
    c("據仲津說，他們模仿貓頭鷹羽毛的小鋸齒，把風切聲也壓下來。", "貓頭鷹鋸齒", "P:owl"),
)
scene(
    "train-500-debut",
    "Wide view of " + TRAIN + " with an extra-long pointed nose and a rounded cylindrical body gliding smoothly out of a mountain tunnel beside blooming cherry trees",
    c("一九九七年三月，這列新幹線把新大阪到博多縮短十五分鐘。", "里程碑"),
    c("西日本鐵路目前計畫在二〇二七年結束它的定期營業運轉。", "時效資訊"),
)
kid(
    "kid-why-shrink-q",
    "Waist-up medium shot of the girl frowning in confusion and holding both hands wide apart then bringing them closer",
    k("既然那麼長的鼻子這麼成功，", "抓出核心轉折"),
    k("為什麼後來的車頭，", "疑惑"),
    k("反而沒有越做越長？", "章尾停住，句尾上揚", "S:seat"),
)

# ---------- 第四章：鼻子多長，是一場取捨 ----------
chief(
    "chief-seat-tradeoff",
    "Waist-up medium shot of the chief holding her two hands like a balance scale tilting up and down",
    c("因為長鼻子有個代價：鼻子越長，能賣票的座位越少！", "一針見血", "P:seat", 100),
    c("車廂長度固定，前面拉出長鼻，駕駛室後退，客艙就變小了。", "解釋取捨"),
    chapter="車速、隧道與座位的取捨",
)
scene(
    "nose-vs-seats",
    "Medium shot cutaway comparison of two equal-length lead carriages: the top carriage has a very long pointed nose with fewer blue seats; the bottom carriage has a shorter duckbill nose with extra rows of blue seats",
    c("接班的七百系，時速兩百八十五公里，決定幫鼻子瘦身。", "下一代登場"),
    c("工程師用「多段旋轉拋物體」把鼻子縮回九點二公尺，保住座位！", "技術取捨"),
)
kid(
    "kid-alfa-x-q",
    "Head-and-shoulders close-up of the girl leaning forward with sparkling eyes and holding her hands very wide apart",
    k("那如果還想開得比以前更快，", "反向推論"),
    k("鼻子又得拉長囉？", "句尾上揚", "S:faster"),
)
scene(
    "long-test-nose",
    "Wide view comparing three sleek unmarked high-speed noses of different lengths: a nine-metre duckbill nose, a longer fifteen-metre nose, and an extreme twenty-two-metre experimental nose",
    c("沒錯！往北跑、時速三百二十公里的車型，車鼻又拉回原長。", "印證推論"),
    c("挑戰三百六十公里的試驗車，鼻子約二十二公尺，只剩幾排位子！", "極端案例", "P:faster"),
)
scene(
    "rtri-three-stage",
    "Close-up of a sleek three-stage sculpted nose model in a wind tunnel with smooth blue airflow lines",
    c("同時，鐵道綜合技術研究所也在研發新的三段式車頭，", "雙向研發"),
    c("想在同樣安靜的前提下，把鼻子再縮短一公尺，搶回座位。", "清楚"),
)
kid(
    "kid-taiwan-back",
    "Waist-up medium shot of the girl pointing at herself with both hands and a big puzzled frown on the railway platform",
    k("等等！那我們台灣高鐵呢？", "點名回呼開場"),
    k("它用日本原型車去改，", "複習線索"),
    k("跑更快，鼻子怎麼反而更短？", "句尾上揚"),
)
chief(
    "chief-700t-numbers",
    "Waist-up medium shot of the chief holding up eight fingers with a bright smile",
    c("這就是最精彩的地方！台灣第一代高鐵，速度比日本原型車還快，", "對比速度"),
    c("車鼻卻從九點二公尺縮成八公尺，短了一點二公尺！", "對比鼻長"),
)
kid(
    "kid-why-quiet-q",
    "Head-and-shoulders close-up of the girl scratching her head with one finger, eyes wide in disbelief on the railway platform",
    k("跑更快、鼻子又短了一點二公尺，", "抓住矛盾"),
    k("進山洞不會砰砰叫嗎？", "句尾上揚", "S:twtunnel"),
)
scene(
    "tunnel-size-compare",
    "Close-up front cross-section comparison of two mountain tunnels with identical express carriages inside: on the left, a tight tunnel fitting closely around the carriage; on the right, a spacious tunnel with nearly fifty percent more room",
    c("不會！因為秘密不在火車上，而在台灣的山洞裡。", "揭曉核心答案", "P:twshort", 100),
    c("還記得打氣筒嗎？管子變粗，空氣容易從旁邊流過，壓力波就小。", "回呼打氣筒比喻"),
)
scene(
    "taiwan-90m2",
    "Wide view inside a spacious bright concrete twin-track tunnel with generous room above and around " + TRAIN + " gliding smoothly along the rails",
    c("日本早期隧道較窄；台灣高鐵把隧道截面挖到九十平方公尺以上，", "關鍵數據"),
    c("比日本山洞大了將近五成，是不是寬敞很多？", "強調對比", "P:twtunnel", 100),
)
scene(
    "taiwan-tunnel-hood",
    "Wide view of " + TRAIN + " with an eight-metre nose entering a wide mountain tunnel portal equipped with a long angled concrete buffer hood with side vent windows on a green hillside",
    c("台灣高鐵洞口也蓋了三、四十公尺、斜切四十五度的緩衝罩。", "洞口緩衝罩"),
    c("山洞寬又有緩衝罩，八公尺車鼻就能壓住碰聲，空間留給車廂！", "完整因果"),
)
kid(
    "kid-new-train-q",
    "Waist-up medium shot of the girl looking down the sunny railway platform with an eager smile",
    k("原來是山洞比較寬！", "恍然大悟"),
    k("那台灣高鐵接下來換的新車，", "延伸好奇"),
    k("車頭長什麼樣子？", "句尾上揚", "S:newtw"),
)
scene(
    "new-train-wing",
    "Medium shot from the front three-quarter angle of " + TRAIN + " with a sleeker flatter nose and sculpted wing-like ridges curving along both sides of the nose at a modern platform",
    c("新世代列車首組在二〇二六年八月份抵台，預計隔年上線。", "最新進度"),
    c("車頭更扁平，兩側像翅膀多捏出導流稜線，在隧道更穩！", "回答新車造型", "P:newtw"),
)

# ---------- 收尾 ----------
chief(
    "chief-ask-kid",
    "Waist-up medium shot of the chief smiling warmly at the girl with both hands open",
    c("現在線索全湊齊了，小問，", "交棒給小問"),
    c("高鐵的長鼻子和短鼻子，你自己破案看看！", "鼓勵"),
    chapter="小問自己破案",
)
kid(
    "kid-summary-1",
    "Waist-up medium shot of the girl counting on her fingers with a confident beaming grin on the railway platform",
    k("火車衝進窄山洞像打氣筒，", "篤定"),
    k("壓縮波用音速跑到出口碰一聲！", "清楚"),
    k("長鼻子讓壓力像緩坡慢慢升！", "開心"),
)
kid(
    "kid-summary-2",
    "Waist-up medium shot of the girl pointing proudly at the wide tunnel in the distance and then at the sleek express",
    k("可是鼻子越長座位越少，", "篤定"),
    k("台灣的山洞比日本大將近五成，", "清楚"),
    k("所以鼻子八公尺就夠安靜了！", "開心破案"),
)
chief(
    "chief-platform-tip",
    "Waist-up medium shot of the chief smiling warmly at the viewer with her hands clasped",
    c("下次在高鐵月台等車，看一眼從鼻尖到車窗緩緩鼓起的曲線。", "給觀眾的行動建議"),
    c("那是工程師算出來、跟山洞裡空氣溫柔打招呼的形狀。", "溫暖收束"),
)
# The outro is three pictures, no card (series README §3.2).
kid(
    "outro",
    "Head-and-shoulders close-up of the girl with a big happy smile giving a big cheerful thumbs-up with one hand, bright morning light",
    k("原來如此！", "開心大聲"),
)
chief(
    "outro-chief",
    "Waist-up medium shot of the chief smiling warmly while gently touching one ear with her slender fingertips, bright warm morning light",
    c("你搭高鐵或火車進山洞時，耳朵有沒有感覺過那一下微妙的氣壓變化？", "問句上揚，像聊天"),
    c("留言告訴我們！", "親切"),
)
chief(
    "outro-wave",
    "Waist-up medium shot of the chief waving goodbye with a warm smile, bright morning light",
    c("想一起找生活裡的為什麼，就訂閱原來如此事務所。", "誠懇"),
)

# ---------- assemble ----------
WHAT = {
    "wind": "高鐵車頭拉那麼長，是不是主要為了減少風阻",
    "tunnel": "山洞裡到底有什麼可怕的對手讓工程師把車頭拉長",
    "twshort": "台灣高鐵跑得比日本原型車還快，車鼻子為什麼反而比較短",
    "sonic": "俗稱的隧道音爆，是不是火車跑得比聲音還快造成的超音速音爆",
    "slab": "為什麼到了一九七五年山陽新幹線延伸時，隧道洞口的爆破聲才突然變嚴重",
    "cube": "火車速度只快一點點，隧道洞口的碰聲也只大一點點嗎",
    "steep": "不讓火車慢下來，怎麼在進洞的第一瞬間把微氣壓波壓下去",
    "shape": "把車頭削成尖尖的圓錐形，壓低壓力陡度的效果是不是最好",
    "hood": "除了改造火車車頭，山洞口自己能不能也幫忙洩壓",
    "bird": "面對高速與狹窄隧道的考驗，工程師向大自然哪種動物搬救兵",
    "copy": "五百系新幹線的長車頭，是不是直接拿翠鳥的嘴巴照著描出來的",
    "bio": "生物學家後來有沒有驗證過翠鳥鳥嘴到額頭的入水減阻效果",
    "owl": "車頂伸上去接電線的集電弓高速切風很吵，工程師怎麼解決",
    "seat": "既然長鼻子的翠鳥新幹線這麼成功，為什麼後來的車頭沒有越做越長",
    "faster": "如果要開得更快，車鼻子又得拉長到幾公尺",
    "twtunnel": "台灣高鐵第一代車鼻短了一點二公尺又跑更快，進山洞為什麼不會砰砰叫",
    "newtw": "台灣高鐵引進的新世代列車什麼時候上線、車頭長什麼樣子",
}

scenes, loops_s, loops_p, n = [], {}, {}, 0
for sc in S:
    lines = []
    for sp, text, emo, tag, pause in sc["lines"]:
        n += 1
        lid = f"p{n:03d}"
        line = {"id": lid, "speaker": sp, "text": text}
        if pause is not None:
            line["pause_after_ms"] = pause
        if emo:
            line["emotion"] = emo
        lines.append(line)
        if tag:
            kind, key = tag.split(":")
            (loops_s if kind == "S" else loops_p)[key] = lid
    out = {"id": sc["id"]}
    if sc["chapter"]:
        out["chapter"] = sc["chapter"]
    out["template"] = sc["template"]
    out["data"] = dict(sc["data"])
    out["lines"] = lines
    scenes.append(out)

assert set(loops_s) == set(loops_p) == set(WHAT), set(loops_s) ^ set(loops_p) ^ set(WHAT)
assert all(loops_s[key] < loops_p[key] for key in WHAT), [key for key in WHAT if loops_s[key] >= loops_p[key]]
loops = [{"setup": loops_s[key], "payoff": loops_p[key], "what": WHAT[key]} for key in sorted(WHAT, key=lambda key: loops_s[key])]

doc = {
    "schema_version": 1,
    "slug": SLUG,
    "format": "drama",
    "category": "explainer",
    "narration_locale": "zh-TW",
    "target_minutes": [9, 11],
    "voice": VOICE,
    "pauses": {"line_ms": 0, "scene_ms": 150},
    "still_motion": "beat",
    "subtitles": {"burn_in": False},
    "theme": "paper",
    "look": {"preset": "cute-cartoon"},
    "series": {"slug": "sothatswhy", "episode": 25, "chapter": 1},
    "music": {
        "track": "sothatswhy-bed-r2.m4a",
        "sha256": "9bb4ba6fd16feb4a7f352144b2d89e9648acbbbbaa2173c27a7eefbdb70f28c6",
        "gain_db": -20,
        "duck_db": -10,
    },
    "characters": CHARACTERS,
    "pronunciation_hints": {
        "仲津": "ㄓㄨㄥˋ ㄐㄧㄣ",
        "截面": "ㄐㄧㄝˊ ㄇㄧㄢˋ",
    },
    "loops": loops,
    "youtube": {
        "category_id": 27,
        "made_for_kids": False,
        "default_language": "zh-TW",
        "title": "高鐵車頭拉這麼長，為什麼不是為了破風？｜原來如此事務所",
        "description": (
            "日本新幹線的車頭拉出十五公尺長的尖鼻子，很多人以為這只是為了切開空氣、減少風阻；更奇怪的是，台灣高鐵跑得比日本原型車還快，車鼻子卻反而比較短！這到底是怎麼回事？\n\n"
            "這一集，所長和小問一起走進高鐵月台與山洞：先看長長的列車風阻大半在哪裡、火車衝進山洞為什麼會像打氣筒一樣在出口放出一聲「碰」（隧道微氣壓波）、"
            "為什麼換成水泥板軌道後問題才浮上檯面；接著看長鼻子怎麼把壓力從陡坡拉成緩坡、翠鳥與貓頭鷹給了工程師什麼靈感、子彈打細管實驗與超級電腦算出了什麼曲線，"
            "最後揭曉車速、隧道截面積與座位數量的取捨，看看為什麼台灣高鐵的鼻子只要八公尺就夠安靜。\n\n"
            "本集插圖由 AI 生成，畫中列車皆為泛稱示意，並非特定車型塗裝。片中提到的倍數與尺寸為工程文獻與教學資料中的約略數值；每個說法的出處皆列於下方參考資料。\n\n資料截至 "
            + CHECKED
        ),
        "tags": ["高鐵", "新幹線", "隧道微氣壓波", "隧道音爆", "翠鳥", "五百系", "台灣高鐵", "科普", "原來如此事務所"],
        "video_id": None,
    },
    "thumbnail": {
        "template": "thumb",
        "data": {
            "headline": "高鐵長鼻子\n**不是為破風？**",
            "sub": "台灣高鐵跑更快，鼻子卻更短",
            "shot": "platform-nose",
            "subject": "right",
        },
    },
    "sources": [
        {"title": "鉄道総合技術研究所（RTRI）：トンネル微気圧波低減対策", "url": "https://www.rtri.or.jp/rd/division/rd51/rd5120/rd51200101.html", "checked_on": CHECKED},
        {"title": "齋藤實俊（2015），トンネル微気圧波低減のための列車先頭形状最適化に関する研究（大阪大学博士論文）", "url": "https://doi.org/10.18910/53989", "checked_on": CHECKED},
        {"title": "小澤智（1995），新幹線トンネルにおける微気圧波の研究（京都大学数理解析研究所講究録 908）", "url": "https://www.kurims.kyoto-u.ac.jp/~kyodo/kokyuroku/contents/pdf/0908-13.pdf", "checked_on": CHECKED},
        {"title": "原田巖（2003），高速列車の先頭形状の最適化（応用数理 13(3)）", "url": "https://www.jstage.jst.go.jp/article/bjsiam/13/3/13_KJ00003509908/_pdf/-char/ja", "checked_on": CHECKED},
        {"title": "吉川岳（2017），鉄道車両の空気抵抗（RTRI 車両通信 2017-01）", "url": "https://www.rtri.or.jp/rd/news/vehicle/vehicle_201701.html", "checked_on": CHECKED},
        {"title": "鉄道総合技術研究所（2019），トンネル微気圧波を抑制する新幹線車両の三段式先頭形状", "url": "https://www.rtri.or.jp/rd/seika/2019/3-19.html", "checked_on": CHECKED},
        {"title": "仲津英治（2018），鳥に学ぶ新幹線の技術開発 ―500系新幹線の開発を中心として―（日本機械学会 2018 W20200）", "url": "https://www.jstage.jst.go.jp/article/jsmemecj/2018/0/2018_W20200/_pdf", "checked_on": CHECKED},
        {"title": "Japan for Sustainability (JFS)：Shinkansen Technology Learned from an Owl and a Kingfisher", "url": "https://www.japanfs.org/en/news/archives/news_id027795.html", "checked_on": CHECKED},
        {"title": "Crandell, Howe & Falkingham (2019), Repeated evolution of dive performance in kingfishers (J. R. Soc. Interface 16: 20190125)", "url": "https://pubmed.ncbi.nlm.nih.gov/31088257/", "checked_on": CHECKED},
        {"title": "JR西日本（2026-06-22）：500系新幹線電車および「ドクターイエロー（T5編成）」の今後の予定について", "url": "https://www.westjr.co.jp/press/article/2026/06/22/items/260622_00_press_500kei_dryellow.pdf", "checked_on": CHECKED},
        {"title": "石塚理（2005），高速鉄道車両の先頭形状（関西造船協会 らん 65）", "url": "https://www.jstage.jst.go.jp/article/ran/65/0/65_KJ00003654273/_pdf/-char/ja", "checked_on": CHECKED},
        {"title": "落合・松原・佐藤（2004），台湾高速鉄道の建設現場を訪ねて（日本機械学会誌 107(1030)）", "url": "https://www.jstage.jst.go.jp/article/jsmemag/107/1030/107_KJ00004379578/_pdf/-char/ja", "checked_on": CHECKED},
        {"title": "JR東海（2017-06-28）：東海道・山陽新幹線 次期車両（N700S）の確認試験車の製作について", "url": "https://jr-central.co.jp/news/release/_pdf/000034313.pdf", "checked_on": CHECKED},
        {"title": "Impress Travel Watch（2019-02-08）：JR東日本、次世代新幹線「ALFA-X」1号車・10号車の先頭車両を公開", "url": "https://travel.watch.impress.co.jp/docs/news/1168992.html", "checked_on": CHECKED},
        {"title": "東洋経済オンライン（2018-03-04）：新幹線の「鼻」はなぜあんなに長いのか", "url": "https://toyokeizai.net/articles/-/211231", "checked_on": CHECKED},
        {"title": "台灣高鐵（2026-08-15）：台灣高鐵新世代列車 N700ST 首組抵台", "url": "https://www.thsrc.com.tw/ArticleContent/aee431a7-eb9c-4681-be39-d56c2966f37c", "checked_on": CHECKED},
        {"title": "NASA Glenn Research Center：Speed of Sound Interactive", "url": "https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/speed-of-sound-interactive/", "checked_on": CHECKED},
    ],
    "assets": [],
    "scenes": scenes,
}

json.dump(doc, open(os.path.join(HERE, "video.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
FROZEN.update({s["id"]: s["data"]["camera"] for s in scenes if s["template"] == "shot" and s["id"] not in FROZEN})
json.dump(FROZEN, open(CAM_FILE, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# ---------- self-checks ----------
RATE = 4.167
def length(t):
    return sum(1 for ch in t if ch not in "，。、：；！？「」『』（）…—,.!?: ")

assert all(s["template"] == "shot" for s in scenes), "this series uses no cards"
outro_ids = {"outro", "outro-chief", "outro-wave"}
body = [s for s in scenes if s["id"] not in outro_ids]
chars = sum(length(l["text"]) for s in scenes for l in s["lines"])
body_chars = sum(length(l["text"]) for s in body for l in s["lines"])
kidc = sum(length(l["text"]) for s in scenes for l in s["lines"] if l["speaker"] == "kid")
lines_all = [l for s in scenes for l in s["lines"]]
print(
    f"scenes {len(scenes)} shots {len(scenes)} lines {n} chars {chars} (body {body_chars}) kid {kidc / chars:.1%} of chars, "
    f"{sum(l['speaker'] == 'kid' for l in lines_all) / n:.1%} of lines; est {chars / RATE / 60:.1f} min at {RATE:.2f}/s; loops {len(loops)}",
    file=sys.stderr,
)
for s in scenes:
    sc_chars = sum(length(l["text"]) for l in s["lines"])
    secs = sc_chars / RATE + 0.15
    if secs > 11.8:
        print(f"  shot over 11.8 s ({sc_chars} chars): {s['id']} {secs:.1f}s", file=sys.stderr)
for l in lines_all:
    cap = 15 if l["speaker"] == "kid" else 40
    if length(l["text"]) > cap:
        print(f"  long {l['speaker']} line {l['id']} ({length(l['text'])}): {l['text']}", file=sys.stderr)
hooks, t, last, setups = [], 0.0, 0.0, set(loops_s.values())
for s in body:
    for l in s["lines"]:
        t += length(l["text"]) / RATE
        if l["text"].endswith("？") or l["id"] in setups:
            if t - last > 45:
                print(f"  hook gap {t - last:.0f} s before {l['id']}", file=sys.stderr)
            last = t
cams = [s["data"]["camera"] for s in scenes]
assert all(not (a == b == c_) for a, b, c_ in zip(cams, cams[1:], cams[2:])), "three shots in a row with the same camera"
