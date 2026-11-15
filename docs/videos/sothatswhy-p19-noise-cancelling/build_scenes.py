"""Generate video.json for sothatswhy-p19-noise-cancelling (原來如此事務所 對話版 P19).

Run `python3 build_scenes.py` from anywhere: it rewrites video.json next to this file and freezes
every shot's camera move in cameras.json.
"""
import itertools, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = "sothatswhy-p19-noise-cancelling"
CHECKED = "2026-11-14"

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
SHEET = "character reference: one single full-body figure standing in the centre, facing the viewer in a slight three-quarter turn, relaxed friendly pose, both hands clearly drawn, plain empty pale ivory background, zero turnaround, zero second view, zero seal, zero stamp, zero signature, zero lettering"
CHARACTERS = [
    {
        "id": "chief",
        "name": "所長",
        "appearance": "a friendly middle-aged woman, the chief of a small question office, with round black glasses, shoulder-length dark hair with a streak of grey tied in a low ponytail, a warm smile, a mustard-yellow cardigan over a white blouse, ink-navy trousers, brown shoes, a yellow pencil tucked behind one ear",
        "voice": VOICE,
        "sheet_prompt": SHEET + ", a friendly middle-aged woman, the chief of a question office, round black glasses, shoulder-length dark hair with a streak of grey tied in a low ponytail, mustard-yellow cardigan over a white blouse, ink-navy trousers, brown shoes, a yellow pencil tucked behind one ear",
    },
    {
        "id": "kid",
        "name": "小問",
        "appearance": "a curious young woman in her twenties, assistant in the question office, with short neat black hair, lively expressive eyes, a forest-green hoodie with the hood down, beige trousers, white canvas shoes, holding an orange question-mark mug",
        "voice": KID_VOICE,
        "sheet_prompt": SHEET + ", a curious young woman in her twenties, short neat black hair, lively expressive eyes, a forest-green hoodie with the hood down, beige trousers, white canvas shoes, holding an orange question-mark mug",
    },
]

BANNED = re.compile(r"\b(no|not|without|text|blank|lamp|night|notebook|sign|signs|paper|poster|screen|book|calendar|whiteboard|cream|cartoon)\b", re.I)

CAMS = itertools.cycle(["push in", "pan left", "pull out", "drift", "tilt up", "pan right", "push in", "tilt down", "pull out", "drift"])
CAM_FILE = os.path.join(HERE, "cameras.json")
FROZEN = json.load(open(CAM_FILE, encoding="utf-8")) if os.path.exists(CAM_FILE) else {}

S = []

def _shot(id, prompt, chars, lines, chapter):
    assert not BANNED.search(prompt), (id, BANNED.search(prompt).group(0))
    cam = FROZEN.get(id) or next(CAMS)
    S.append(dict(id=id, prompt=prompt, chars=chars, lines=lines, chapter=chapter, cam=cam))

def kid(id, prompt, *lines, chapter=None):
    _shot(id, prompt.rstrip(". "), ["kid"], lines, chapter)

def chief(id, prompt, *lines, chapter=None):
    _shot(id, prompt.rstrip(". "), ["chief"], lines, chapter)

def scene(id, prompt, *lines, chapter=None):
    _shot(id, prompt.rstrip(". "), [], lines, chapter)

def k(text, emotion, tag=None, pause=None):
    return ("kid", text, emotion, tag, pause)

def c(text, emotion, tag=None, pause=None):
    return ("chief", text, emotion, tag, pause)

# ==================== 第一章：戴上耳機那一秒，世界怎麼變安靜的？ ====================
kid(
    "kid-wear-headphones",
    "Waist-up medium shot of the girl putting on sleek matte-black over-ear headphones, eyes lighting up with amazement",
    k("所長！這副新耳機太神了！", "驚嘆開場"),
    k("捷運的轟轟聲瞬間全消失，", "興奮描繪"),
    chapter="戴上耳機那一秒，世界怎麼變安靜的？",
)
kid(
    "kid-hear-chief-talk",
    "Head-and-shoulders close-up of the girl looking sideways with a puzzled blink",
    k("可是你在旁邊講話，", "困惑"),
    k("我怎麼還聽得一清二楚？", "大惑不解，句尾上揚"),
)
chief(
    "chief-knowing-smile",
    "Waist-up medium shot of the chief sitting at a wooden desk with a gentle knowing smile",
    c("很多人以為降噪耳機是隱形防護罩，", "指出迷思"),
    c("把所有聲音統統像海綿一樣吸光。", "生動比喻"),
)
kid(
    "kid-sponge-guess",
    "Waist-up medium shot of the girl squeezing a small yellow foam earplug between her fingers",
    k("難道不是海綿擋住聲音嗎？", "直覺猜測", "S:sponge"),
)
chief(
    "chief-foam-limit",
    "Waist-up medium shot of the chief shaking her head calmly with one finger raised",
    c("海綿只能擋住高音，", "指出物理限制"),
    c("低音巨浪根本擋不住！", "反轉認知", "P:sponge"),
)
scene(
    "subway-car-rumble",
    "Medium shot of passengers sitting inside a vibrating commuter train car, blurred dark tunnel rushing past the glass window",
    c("捷運軌道跟空調的低頻轟鳴，", "生活場景引入"),
    c("震動會直接穿透耳罩縫隙鑽進耳朵。", "低頻穿透"),
)
scene(
    "foam-absorb-compare",
    "Close-up of a soft foam pad: rapid tight orange ripples get trapped in tiny pores while a massive long blue wave glides right through it",
    c("高頻尖銳聲容易被孔洞摩擦吸收，", "高音被阻擋"),
    c("但長波長的低音會直接穿透過去！", "低音穿透"),
)
kid(
    "kid-passive-wonder",
    "Head-and-shoulders close-up of the girl peering into the ear cup mesh with squinting curiosity",
    k("難怪只塞海綿耳塞，", "回想生活經驗"),
    k("引擎的震動聲還是悶悶地響！", "生動共鳴"),
)
chief(
    "chief-reveal-second-sound",
    "Waist-up medium shot of the chief leaning forward with bright engaged eyes",
    c("耳機真正的秘密不是吸收，", "語速放慢"),
    c("而是它在耳邊播了第二個聲音！", "重音揭曉核心"),
)
kid(
    "kid-two-sounds-shock",
    "Waist-up medium shot of the girl throwing both hands up in total disbelief",
    k("多播一個聲音？", "震驚懷疑"),
    k("那不是應該更吵嗎？", "尖銳追問，句尾上揚", "S:add"),
)
chief(
    "chief-counter-intuition",
    "Waist-up medium shot of the chief smiling gently in warm morning sunlight",
    c("這正是聲學最迷人的地方：", "引導好奇"),
    c("用聲音消滅聲音，一點都不吵！", "加深懸念"),
)
kid(
    "kid-eager-how",
    "Head-and-shoulders close-up of the girl clutching her mug with excited anticipation",
    k("快告訴我！", "迫不及待"),
    k("聲音到底怎麼消滅聲音？", "推動劇情推進"),
)

# ==================== 第二章：用聲音消滅聲音？波峰撞上波谷 ====================
chief(
    "chief-explain-wave",
    "Waist-up medium shot of the chief using two hands to trace gentle wavy curves in the air",
    c("這就是聲音最奇妙的物理：相消干涉！", "熱情引導"),
    c("聲音本質是空氣被一推一拉的壓力波。", "物理本質"),
    chapter="用聲音消滅聲音？波峰撞上波谷",
)
scene(
    "air-molecules-pressure",
    "Close-up of air particles forming alternating dense compressed zones and loose expanded bands pushing forward",
    c("空氣被推擠變密的地方叫波峰，氣壓高；", "波峰定義"),
    c("被拉開變稀疏的地方叫波谷，氣壓低。", "波谷定義"),
)
kid(
    "kid-eardrum-listen",
    "Head-and-shoulders close-up of the girl touching the side of her ear thoughtfully",
    k("耳膜被一推一拉，才聽到聲音！", "串聯生理機制"),
    k("那要怎麼把推拉拉平？", "期待追問", "S:flatten"),
)
chief(
    "chief-anti-phase-hands",
    "Waist-up medium shot of the chief holding two palms opposite each other, mirroring motions in reverse",
    c("耳機麥克風先偵測外界噪聲的波形，", "第一步：偵測"),
    c("晶片立刻算出一道顛倒的反相聲波！", "第二步：計算", "P:flatten"),
)
scene(
    "waves-cancel-diagram",
    "Close-up of an incoming blue wave crest aligning with a red wave trough, colliding and flattening into a smooth calm level line",
    c("外界波峰推過來，耳機剛好拉出波谷；", "相撞機制"),
    c("高壓加低壓，耳膜前空氣壓力歸零！", "抵消結果"),
)
kid(
    "kid-cancel-cheer",
    "Waist-up medium shot of the girl clapping hands with a joyful realization",
    k("正負相加等於零！", "恍然大悟"),
    k("聲音自己把自己吃掉了！", "生動總結", "P:add"),
)
chief(
    "chief-energy-clarify",
    "Waist-up medium shot of the chief gesturing gently with palms opening outward",
    c("在狹小的耳道空間裡，兩股壓力互相抵消，", "聲學本質說明"),
    c("耳膜完全感受不到起伏，世界就安靜了。", "回歸聽覺體驗"),
)
kid(
    "kid-energy-puzzle",
    "Head-and-shoulders close-up of the girl scratching her forehead with an analytical frown",
    k("可是兩道聲音相撞，", "物理追問"),
    k("原本聲音的能量跑到哪裡去了？", "深刻物理疑問", "S:energy"),
)
chief(
    "chief-impedance-reveal",
    "Waist-up medium shot of the chief tapping her fingertips together insightfully",
    c("問得太內行了！能量可沒有憑空消失，", "讚許深層思考"),
    c("反相波改變了耳道裡的聲學阻抗！", "聲學阻抗本質", "P:energy"),
)
scene(
    "radiation-impedance-cavity",
    "Close-up technical diagram of an acoustic speaker driver pushing against an opposing acoustic field in a compact chamber",
    c("耳機的反向推力讓外界聲源做不了功，", "做功抑制"),
    c("在耳道裡，聲音能量直接在源頭被壓制住！", "能量機制總結"),
)
kid(
    "kid-history-ask",
    "Head-and-shoulders close-up of the girl tilting head with curiosity",
    k("這麼神奇的消音魔法，", "好奇起源"),
    k("難道是這幾年晶片厲害才發明的？", "時代猜測", "S:history"),
)
chief(
    "chief-patent-history",
    "Waist-up medium shot of the chief smiling with warmth in golden morning sunlight",
    c("早在九十年前德國工程師就想過這招，", "歷史淵源"),
    c("但當時沒有電腦，根本算不出來！", "時代技術限制", "P:history"),
)
scene(
    "paul-lueg-patent-concept",
    "Close-up in a retro physics laboratory of an acoustic tube apparatus with a vibrating diaphragm and mirrored sound wave lines",
    c("一九三六年工程師魯格提出專利管子實驗，", "具體歷史專利"),
    c("真空管反應太慢，雜音反而越放越大。", "早期技術挫折"),
)
chief(
    "chief-dsp-arrival",
    "Waist-up medium shot of the chief picking up a tiny shiny black silicon microchip with tweezers",
    c("直到現代微型數位運算晶片誕生，", "技術轉折點"),
    c("主動降噪才真正裝進了小小的耳機裡。", "工程落地"),
)

# ==================== 第三章：為什麼低頻轟鳴全滅，人聲卻留下來？ ====================
kid(
    "kid-voice-puzzle",
    "Head-and-shoulders close-up of the girl tilting her head with a furrowed brow",
    k("可是所長，既然能算反相波，", "轉折提問"),
    k("為什麼不算你的聲音，專消捷運聲？", "直擊核心矛頓", "S:whyvoice"),
    chapter="為什麼低頻轟鳴全滅，人聲卻留下來？",
)
chief(
    "chief-wavelength-intro",
    "Waist-up medium shot of the chief spreading her arms wide apart to show massive scale",
    c("關鍵就在聲音的身材，也就是波長！", "點出核心變數"),
    c("低音跟高音的長度，相差幾十倍。", "強烈對比"),
)
scene(
    "wavelength-visual-scale",
    "Wide shot comparing a giant undulating blue wave spanning three meters across a room, beside tiny dense orange ripples only centimeters long",
    c("捷運一百赫茲的低頻，波長長達三點四公尺！", "低頻具體數字"),
    c("人類說話兩千赫茲的聲音，波長只有十七公分。", "人聲具體數字"),
)
kid(
    "kid-compare-scale",
    "Waist-up medium shot of the girl looking down at her own two hands with wonder",
    k("三公尺多比一張床還長！", "具象生活對照"),
    k("那波長長短，跟能不能消掉有何關係？", "追問因果", "S:tolerance"),
)
chief(
    "chief-ear-chamber",
    "Waist-up medium shot of the chief holding thumb and index finger two centimeters apart",
    c("你的耳道只有兩三公分大！", "人體尺寸"),
    c("三公尺的低頻巨浪湧進來，全耳道氣壓幾乎一樣。", "大波包小空間", "P:tolerance"),
)
scene(
    "zone-of-quiet-diagram",
    "Close-up cross section of an ear canal immersed in a massive smooth low-frequency wave, showing a uniform calm bubble around the eardrum",
    c("耳機喇叭放出的反相波，能輕鬆籠罩整個耳道，", "大範圍覆蓋"),
    c("在聲學上這叫做「局部靜音區」。", "權威名詞"),
)
kid(
    "kid-quiet-bubble-delight",
    "Waist-up medium shot of the girl smiling with a cupped hand beside her ear",
    k("就像躲進了平靜的保護泡泡裡！", "生動畫面感"),
    k("那人聲的短波浪又是怎麼回事？", "主動接續下文"),
)
chief(
    "chief-high-pitch-risk",
    "Waist-up medium shot of the chief slightly leaning in with a cautionary look",
    c("但說話聲波長太短、起伏太密了！", "高頻困難"),
    c("只要耳機晃動一公分，或是慢了幾微秒，", "極端容錯要求", "S:screech"),
)
scene(
    "wave-misalign-clash",
    "Close-up of two sound waves slightly shifted out of alignment: the crests fail to cancel, stacking into a sharp double-height spike",
    c("反相波就會錯位，波峰撞波峰，", "錯位機制"),
    c("聲音不但沒變小，反而會被放大成尖叫！", "錯位放大風險", "P:screech"),
)
kid(
    "kid-scared-spike",
    "Head-and-shoulders close-up of the girl wincing slightly and touching her ear cup",
    k("如果算錯，耳機會變得像尖叫雞！", "形象生動比喻"),
    k("所以工程師才不敢亂消高音嗎？", "推論意圖", "P:whyvoice"),
)
chief(
    "chief-acoustic-boundary",
    "Waist-up medium shot of the chief placing palms together steadily",
    c("沒錯！一千赫茲以上是相消干涉的雷區，", "確立物理分水嶺"),
    c("強行去消，只會讓耳機發出刺耳呼嘯。", "說明技術禁區"),
)
kid(
    "kid-turn-head-ask",
    "Head-and-shoulders close-up of the girl turning her head left and right playfully",
    k("那如果我轉個頭、或耳機稍微戴歪呢？", "生活常見動作", "S:misalign"),
)
chief(
    "chief-misalign-risk",
    "Waist-up medium shot of the chief holding index fingers slightly offset from each other",
    c("只要偏差零點五公分，高頻反相波就全錯位了！", "精確物理公差", "P:misalign"),
    c("原本該相消的波峰，剛好疊在另一個波峰上！", "同相疊加危害"),
)
kid(
    "kid-ear-pressure-ask",
    "Head-and-shoulders close-up of the girl blinking and swallowing to equalize ears",
    k("難怪！可是為什麼剛開降噪時，", "引出生活困惑"),
    k("耳朵總有一種悶悶的耳壓感？", "生活常見現象", "S:earpressure"),
)
chief(
    "chief-brain-contrast-explain",
    "Waist-up medium shot of the chief tapping her temple with a gentle smile",
    c("其實耳道氣壓完全沒變！", "澄清迷思"),
    c("是大腦習慣了低頻背景，突然消失產生的感官錯覺！", "感官對比真相", "P:earpressure"),
)
scene(
    "auditory-cortex-brain",
    "Close-up artistic rendering of human auditory sensory balance: sudden disappearance of low background hum causes brain to perceive false pressure",
    c("大腦誤以為自己在高速電梯下降，", "生動體驗比喻"),
    c("只要深呼吸適應兩分鐘，這種感覺就會消失。", "生活安撫建議"),
)
kid(
    "kid-how-to-guard",
    "Head-and-shoulders close-up of the girl looking intrigued with bright eyes",
    k("那耳機要怎麼知道外界聲音，", "追問技術實現"),
    k("同時又確認耳道裡有沒有安靜？", "引出雙麥克風結構", "S:hybrid"),
)

# ==================== 第四章：雙麥克風的極限：耳機晶片跟得上音速嗎？ ====================
chief(
    "chief-dual-mic-intro",
    "Waist-up medium shot of the chief holding up a disassembled headphone cup showing two tiny glowing mic dots",
    c("這就要靠耳機裡的雙麥克風協同作戰了！", "引出雙麥克風"),
    c("一個朝外聽環境，一個朝內貼著耳膜檢查。", "外饋加內饋架構", "P:hybrid"),
    chapter="雙麥克風的極限：耳機晶片跟得上音速嗎？",
)
scene(
    "hybrid-anc-microphones",
    "Close-up cross section of a headphone cup: outer microphone detects exterior noise, while inner microphone monitors internal sound chamber",
    c("外側前饋麥克風提早搶先預警，", "前饋功能"),
    c("內側反饋麥克風實時微調修正漏洞。", "反饋功能"),
)
kid(
    "kid-inner-mic-doubt",
    "Head-and-shoulders close-up of the girl peering into the inner cup mesh",
    k("既然內側麥克風貼著耳朵，", "邏輯質疑"),
    k("為什麼不能靠它一個人搞定全部？", "追問單麥極限", "S:feedbacklimit"),
)
chief(
    "chief-feedback-howling",
    "Waist-up medium shot of the chief holding hands close and mimicking a speaker whistle",
    c("因為內側麥克風有致命的時間差！", "指出反饋限制"),
    c("聲音進了耳道才發現，喇叭回播慢了就會狂叫！", "閉環延遲風險", "P:feedbacklimit"),
)
scene(
    "acoustic-feedback-loop",
    "Close-up diagram of closed-loop signal delay inside an ear cavity causing phase shift and acoustic instability whistle",
    c("就像拿麥克風對準伴唱機音響，", "形象生活通感"),
    c("所以內側麥克風只能小心翼翼處理五百赫茲以下。", "嚴格工作頻段"),
)
kid(
    "kid-speed-challenge",
    "Waist-up medium shot of the girl tapping her chin with lively questioning eyes",
    k("那外側麥克風呢？", "轉向外側麥克風"),
    k("難道還跑不贏空氣裡的聲音？", "句尾上揚，提出挑戰", "S:speedrace"),
)
chief(
    "chief-sound-speed",
    "Waist-up medium shot of the chief gesturing swiftly with one palm slicing through air",
    c("聲音一秒跑三百四十三公尺！", "聲速速度"),
    c("外側麥克風到耳朵只有兩公分，空氣只給六十微秒！", "極小時間窗口", "P:speedrace"),
)
scene(
    "chip-latency-chain",
    "Close-up diagram of sound wave entering outer mic, passing through tiny glowing processor calculating phase, and outputting to inner speaker",
    c("麥克風收音、晶片計算、喇叭單體震動出聲，", "四步訊號鏈"),
    c("整套硬體最快也要花上二十微秒！", "硬體物理極限"),
)
kid(
    "kid-breath-tight",
    "Head-and-shoulders close-up of the girl holding her breath with wide focused eyes",
    k("只差幾十微秒就超時了！", "代入緊張感"),
    k("那捷運的聲音怎麼來得及？", "追問破案線索", "S:predict"),
)
chief(
    "chief-periodic-wave",
    "Waist-up medium shot of the chief waving one hand in a steady rhythmic back-and-forth swing",
    c("因為捷運和冷氣轟鳴是「規律週期波」！", "揭曉秘密武器"),
    c("每一毫秒都在重複，晶片能提早預測下一波！", "主動預判機制", "P:predict"),
)
scene(
    "periodic-vs-random-wave",
    "Close-up comparing an elegant smooth repeating sine wave on the left with a chaotic spiky jagged speech waveform on the right",
    c("晶片看懂節奏，就能提早把反相波準備好；", "週期性預測成功"),
    c("但人類說話完全是突發、隨機的！", "人聲隨機對照", "S:randomvoice"),
)
chief(
    "chief-plosive-random",
    "Waist-up medium shot of the chief making a crisp snapping gesture with her fingers",
    c("誰也猜不到你下一秒會發出爆破音「ㄆ」還是「ㄊ」，", "語音聲學例子"),
    c("晶片沒辦法預判，等算出來，聲音早就進耳朵了！", "結論收束", "P:randomvoice"),
)
kid(
    "kid-random-realization",
    "Head-and-shoulders close-up of the girl nodding rapidly in full agreement",
    k("難怪！捷運軌道是轟隆轟隆規律地轉，", "抓住規律關鍵"),
    k("大家聊天卻是隨時插話！", "生動日常體會"),
)
chief(
    "chief-summary-bridge",
    "Waist-up medium shot of the chief leaning back comfortably with an approving smile",
    c("沒錯！規律的能預算，隨機的只能乾瞪眼，", "對比總結"),
    c("這就是降噪耳機最神奇的數學邏輯。", "昇華邏輯"),
)
kid(
    "kid-transparency-ask",
    "Head-and-shoulders close-up of the girl tapping her ear cup with curious eyes",
    k("那很多耳機有的通透模式，", "生活功能聯想", "S:transparency"),
    k("又是怎麼讓我們聽見旁邊人講話的？", "好奇提問"),
)
chief(
    "chief-transparency-explain",
    "Waist-up medium shot of the chief opening both palms outward in bright golden morning sunlight",
    c("通透模式剛好相反！外側麥克風把人聲收進來，", "反向邏輯揭曉", "P:transparency"),
    c("算準時間微調，原封不動播給耳膜，就像耳機透明了！", "生動畫面感"),
)
kid(
    "kid-clues-connected",
    "Head-and-shoulders close-up of the girl with her eyes shining brightly",
    k("所以說，整套耳機的秘密，", "主動串聯線索"),
    k("根本就是一場物理與數學的精密配合？", "提問帶出收尾"),
)

# ==================== 第五章：小問自己破案與生活觀察 ====================
kid(
    "kid-break-case",
    "Waist-up medium shot of the girl smiling brightly and ticking off points on three fingers",
    k("我全部想通了！", "興奮通關"),
    k("第一是低音波長長、空間小，容錯率大！", "小問歸納第一點"),
    chapter="小問自己破案與生活觀察",
)
kid(
    "kid-case-points-two-three",
    "Head-and-shoulders close-up of the girl speaking with crisp confidence",
    k("第二是引擎聲有規律，耳機能提前預測！", "小問歸納第二點"),
    k("人聲又碎又突發，晶片來不及預判！", "小問歸納第三點"),
)
chief(
    "chief-proud-approval",
    "Waist-up medium shot of the chief smiling proudly with a warm nod",
    c("完全答對！小問今天破案速度一百分！", "正面嘉許"),
    c("高頻人聲，其實大部分是靠厚實耳罩物理阻擋的。", "補足被動隔音"),
)
scene(
    "passive-isolation-cutaway",
    "Close-up cross section of an ergonomic memory foam ear cushion sealing tightly against temple skin, keeping out external high-frequency ripples",
    c("耳罩海綿與外殼依據質量定律，", "質量定律"),
    c("能把兩千赫茲以上的人聲大幅削弱十幾分貝。", "被動降噪成效"),
)
scene(
    "office-commute-contrast",
    "Medium shot of a quiet open-plan office workspace where air conditioning hum is suppressed while a colleague taps on shoulder",
    c("這就是為什麼你在辦公室開降噪，", "辦公室生活場景"),
    c("冷氣轟鳴沒了，但同事叫你名字你依然聽得見！", "日常精準印證"),
)
kid(
    "kid-own-voice-question",
    "Head-and-shoulders close-up of the girl covering both ears with her palms and speaking a word",
    k("難怪！而且我戴著耳機自己講話，", "生活新觀察"),
    k("自己的聲音還是聽得超清楚耶？", "進階疑問", "S:bone"),
)
chief(
    "chief-bone-conduction",
    "Waist-up medium shot of the chief gently tapping her cheek and jawbone with a knowing smile",
    c("那是因為骨傳導！你講話時聲帶振動頭骨，", "骨傳導機制"),
    c("聲音直接鑽進內耳，根本不經過耳道空氣！", "解答困惑", "P:bone"),
)
scene(
    "bone-conduction-skull",
    "Close-up profile showing sound vibrations traveling directly through the jaw and skull bones into the inner cochlea",
    c("耳機就算把耳道空氣抽成真空，", "極限假設"),
    c("骨頭傳遞的聲音依然會震動你的耳蝸！", "生理真相"),
)
kid(
    "kid-plug-ears-try",
    "Waist-up medium shot of the girl putting two index fingers into her ears and humming",
    k("真的耶！手指塞住耳朵哼歌，", "即時實測驗證"),
    k("聲音反而嗡嗡作響變更大了！", "驚奇反饋", "S:occlusion"),
)
chief(
    "chief-occlusion-experiment",
    "Waist-up medium shot of the chief smiling warmly with head tilted",
    c("這在醫學上叫做「閉塞效應」！", "趣味常識"),
    c("封閉的耳道把低頻骨導震動困在裡面，聲音就變重了。", "解答閉塞效應", "P:occlusion"),
)
kid(
    "kid-home-test-ask",
    "Head-and-shoulders close-up of the girl leaning forward with playful curiosity",
    k("那我們自己在家，", "引導生活實驗"),
    k("要怎麼測試降噪耳機的極限？", "邀請觀眾實測", "S:hometest"),
)
chief(
    "chief-home-test-guide",
    "Waist-up medium shot of the chief snapping fingers beside her ear with a smile",
    c("很簡單！戴上耳機開降噪，在耳邊彈個響指或敲敲鍵盤！", "生活測試方法", "P:hometest"),
    c("清脆的高音依然在，但底下的電風扇轟鳴全不見了。", "鮮明對比驗證"),
)
scene(
    "everyday-sounds-test",
    "Close-up split view: on the left fingers snap crisp sound waves, on the right a quiet electric fan motor running silently",
    c("這個小實驗能讓你一秒體會，", "實證感受"),
    c("物理阻擋與主動降噪的完美分工！", "首尾呼應總結"),
)
chief(
    "chief-safety-thought",
    "Waist-up medium shot of the chief leaning forward with a warm conversational gaze",
    c("其實工程師沒把人聲消乾淨，也是一種保護。", "昇華思考"),
    c("走在路上若聽不見呼喊與汽車喇叭，有多危險！", "生活安全提醒"),
)
kid(
    "kid-safety-agree",
    "Head-and-shoulders close-up of the girl taking off her headphones with a relieved smile",
    k("留下一點外界聲音，", "生活安全共鳴"),
    k("走路跟上班才不會被同事嚇一大跳！", "幽默收束"),
)
chief(
    "outro-chief",
    "Waist-up medium shot of the chief smiling gently and adjusting her glasses in bright morning sunlight",
    c("你平常戴降噪耳機時，覺得哪種聲音最難消掉？", "親切問句引導互動"),
    c("留言跟我們聊聊！", "親切收尾"),
)

# ---------- 迴圈與場景解析 ----------
WHAT = {
    "sponge": "難道耳機裡是靠高級海綿把聲音全吸掉嗎",
    "add": "多放一個聲音，為什麼反而會讓聲音變小而不是更吵",
    "flatten": "外界推拉耳膜的壓力波，耳機要如何精準拉平",
    "energy": "兩道聲音相撞抵消，原本聲音的能量跑到哪裡去了",
    "history": "這麼神奇的消音魔法難道是這幾年才發明的嗎",
    "whyvoice": "既然能算反相波，為什麼耳機不算說話聲而專消捷運聲",
    "tolerance": "波長長短跟耳機能不能消掉聲音有什麼關係",
    "screech": "如果耳機算錯高頻會發生什麼可怕後果",
    "misalign": "耳機戴歪一點或稍微轉頭會不會影響降噪效果",
    "earpressure": "為什麼剛戴上降噪耳機時會有一種悶悶的耳壓感",
    "hybrid": "耳機要如何一邊聽外界一邊檢查耳道有沒有安靜",
    "feedbacklimit": "內側反饋麥克風貼著耳膜，為什麼不能靠它搞定全部噪音",
    "speedrace": "現在晶片算那麼快，難道跑不贏空氣裡的聲音嗎",
    "predict": "反應時間只剩幾十微秒，捷運的聲音是怎麼來得及抵消的",
    "randomvoice": "人聲為什麼就無法被演算法提前預測",
    "transparency": "通透模式是如何讓我們聽見旁邊同事講話的",
    "bone": "為什麼戴著降噪耳機自己講話依然聽得超清楚",
    "occlusion": "為什麼塞住耳朵自己說話聲音反而更低沉宏亮",
    "hometest": "自己在家要怎麼一秒測試降噪耳機的物理極限",
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
    out["template"] = "shot"
    out["data"] = {
        "prompt": sc["prompt"],
        "camera": sc["cam"],
        "visual": "still",
        "characters": sc["chars"],
    }
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
    "series": {"slug": "sothatswhy", "episode": 19, "chapter": 1},
    "music": {
        "track": "sothatswhy-bed-r2.m4a",
        "sha256": "9bb4ba6fd16feb4a7f352144b2d89e9648acbbbbaa2173c27a7eefbdb70f28c6",
        "gain_db": -20,
        "duck_db": -10,
    },
    "characters": CHARACTERS,
    "pronunciation_hints": {
        "相消": "ㄒㄧㄤ ㄒㄧㄠ",
        "波峰": "ㄅㄛ ㄈㄥ",
        "波谷": "ㄅㄛ ㄍㄨˇ",
        "耳蝸": "ㄦˇ ㄨㄛ",
        "反饋": "ㄈㄢˇ ㄎㄨㄟˋ",
        "前饋": "ㄑㄧㄢˊ ㄎㄨㄟˋ",
        "阻抗": "ㄗㄨˇ ㄎㄤˋ",
    },
    "loops": loops,
    "youtube": {
        "category_id": 27,
        "made_for_kids": False,
        "default_language": "zh-TW",
        "title": "降噪耳機開著，說話聲怎麼還在？｜原來如此事務所",
        "description": (
            "捷運的轟轟聲瞬間全消失，為什麼旁邊同事講話卻還聽得一清二楚？很多人以為降噪耳機是隱形防護罩，能把所有聲音像海綿一樣吸光；但真相恰好相反：耳機不是吸走聲音，而是在耳邊播放第二個聲音！\n\n"
            "本集所長和小問帶你拆解降噪耳機的物理魔法：\n"
            "・用聲音消滅聲音？波峰撞上波谷的「相消干涉」\n"
            "・兩道聲音抵消，原本的能量跑到哪裡去了？耳道聲學阻抗的秘密\n"
            "・為什麼低頻轟鳴全滅，人聲卻留下來？波長相差二十倍的容錯對決\n"
            "・剛開降噪時的「耳壓感」從何而來？大腦感官對比的錯覺\n"
            "・六十微秒的生死時速：耳機晶片跟得上音速嗎？\n"
            "・規律週期波 vs 突發隨機人聲：為什麼演算法無法預測下一秒？\n"
            "・為什麼戴著耳機自己講話依然超大聲？骨傳導與閉塞效應\n"
            "・在家如何一秒測試耳機的降噪極限？\n\n"
            "本集插圖由 AI 生成，畫中裝置皆為泛稱示意。片中數值皆來自聲學教科書與工程文獻。\n\n資料截至 "
            + CHECKED
        ),
        "tags": ["降噪耳機", "主動降噪", "ANC", "相消干涉", "骨傳導", "聲學", "科普", "原來如此事務所"],
        "video_id": None,
    },
    "thumbnail": {
        "template": "thumb",
        "data": {
            "headline": "降噪耳機\n**說話聲怎還在？**",
            "sub": "聲音消滅聲音的物理極限",
            "shot": "kid-wear-headphones",
            "subject": "right",
        },
    },
    "sources": [
        {"title": "Nelson & Elliott (1992), Active Control of Sound (Academic Press)", "url": "https://www.sciencedirect.com/book/9780125157605/active-control-of-sound", "checked_on": CHECKED},
        {"title": "Kuo & Morgan (1999), Active noise control: a tutorial review (Proc. IEEE 87(6))", "url": "https://ieeexplore.ieee.org/document/763310", "checked_on": CHECKED},
        {"title": "Hansen et al. (2012), Active Control of Noise and Vibration (CRC Press)", "url": "https://www.routledge.com/Active-Control-of-Noise-and-Vibration/Hansen-Snyder-Qiu-Brooks-Moreau/p/book/9780415598590", "checked_on": CHECKED},
        {"title": "Paul Lueg (1936), Process of silencing sound oscillations (US Patent 2,043,416)", "url": "https://patents.google.com/patent/US2043416A/en", "checked_on": CHECKED},
        {"title": "Stenfelt & Goode (2005), Bone-conducted sound: physiological and clinical aspects (Otology & Neurotology)", "url": "https://pubmed.ncbi.nlm.nih.gov/15795627/", "checked_on": CHECKED},
    ],
    "assets": [],
    "scenes": scenes,
}

json.dump(doc, open(os.path.join(HERE, "video.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
FROZEN.update({s["id"]: s["data"]["camera"] for s in scenes if s["id"] not in FROZEN})
json.dump(FROZEN, open(CAM_FILE, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# ---------- 統計與檢查 ----------
RATE = 4.167
def length(t):
    return sum(1 for ch in t if ch not in "，。、：；！？「」『』（）…—,.!?: ")

assert all(s["template"] == "shot" for s in scenes), "this series uses no cards"
outro_ids = {"outro", "outro-chief"}
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
    cap = 18 if l["speaker"] == "kid" else 40
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
