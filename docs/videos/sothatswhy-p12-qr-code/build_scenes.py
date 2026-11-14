"""Generate video.json for sothatswhy-p12-qr-code (原來如此事務所 對話版 P12).

Run `python3 build_scenes.py` from anywhere: it rewrites video.json next to this file and freezes
every shot's camera move in cameras.json (a shot keeps the camera it was first given, so deleting
a shot never shifts the others: the camera is in the keyframe cache key).
Edit lines and prompts here, never in video.json.
"""
import itertools, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = "sothatswhy-p12-qr-code"
CHECKED = "2026-11-14"

KIDDESC = 'the same curious girl with a short bob, straight bangs, one cowlick on top, navy hooded jacket and long navy trousers'
CHIEFFIX_DESC = 'the same warm woman in her thirties with dark hair in a low ponytail, round glasses, mustard cardigan over an ivory blouse'

CAMS = itertools.cycle(["push in", "pan left", "pull out", "drift", "tilt up", "pan right", "push in", "tilt down", "pull out", "drift"])
CAM_FILE = os.path.join(HERE, "cameras.json")
FROZEN = json.load(open(CAM_FILE, encoding="utf-8")) if os.path.exists(CAM_FILE) else {}

S = []


def _shot(id_, prompt, chars, lines, chapter=None, nobody=False):
    cam = FROZEN.get(id_) or next(CAMS)
    data = dict(prompt=prompt, camera=cam, visual="still", characters=list(chars))
    if nobody:
        data["nobody"] = True
    entry = dict(id=id_, template="shot", data=data, lines=list(lines))
    if chapter is not None:
        entry = dict(id=id_, chapter=chapter, template="shot", data=data, lines=list(lines))
    S.append(entry)


def kid(id_, prompt, *lines, chapter=None):
    full = prompt.rstrip(". ") + ", " + KIDDESC if not prompt.endswith(KIDDESC) else prompt
    _shot(id_, full, ["kid"], lines, chapter=chapter, nobody=False)


def chief(id_, prompt, *lines, chapter=None):
    full = prompt.rstrip(". ") + ", " + CHIEFFIX_DESC if not prompt.endswith(CHIEFFIX_DESC) else prompt
    _shot(id_, full, ["chief"], lines, chapter=chapter, nobody=False)


def scene(id_, prompt, *lines, chapter=None):
    _shot(id_, prompt, [], lines, chapter=chapter, nobody=True)


def k(t, e=None, tag=None, pause=None):
    return ("kid", t, e, tag, pause)


def c(t, e=None, tag=None, pause=None):
    return ("chief", t, e, tag, pause)


scene(
    'two-stands-open',
    'Close-up of two square acrylic mosaic stands side by side on a wooden cafe counter: the left stand has a brown iced-coffee splash near the middle with a glowing mint check ring above it, the right stand has clean mosaic tiles squeezed tight by floral vine trim with a coral cross icon above it',
    k('所長！轉角飲料店那張碼沾咖啡，', '急促興奮，跑進來報案'),
    k('QR Code 居然嗶過了！', '急促興奮，跑進來報案'),
    chapter='沾了咖啡還能嗶，乾淨的卻失靈',
)

kid(
    'kid-coffee-tile',
    'Head-and-shoulders close-up of the girl on the right third holding up a square acrylic stand with a stylized dark mosaic grid, three nested corner squares and a brown iced-coffee splash near the middle with huge wide surprised eyes and open mouth, plain pale wall on the left',
    k('旁邊新印的那張乾乾淨淨，', '困惑追問'),
    k('花邊貼很近卻掃不過！', '困惑追問', 'S:L01'),
)

scene(
    'open-teasers',
    'Overhead medium shot of an oak table split between stacks of colourful geometric pattern swatches under a brass magnifying glass on the left and a golden-winged space probe model beside a shiny silver compact disc on the right',
    c('這兩張碼差在哪？發明它的兩位工程師量傳單線條在找什麼？', '懸疑輕快', 'S:L02'),
    c('保護太空探測器的數學，怎麼也藏在小方塊裡？', '懸疑輕快', 'S:L03'),
)

kid(
    'kid-open-splash-q',
    'Waist-up medium shot of the girl at a tidy oak desk by a bright window pointing at two wooden trays of dark-and-light tiles, one with a single coffee drop and one with tiny ink speckles',
    k('髒掉一塊到底怎麼讀出來的？', '瞪大眼追問', 'S:L04'),
    c('不只髒一塊能讀，整滴咖啡跟小墨點命運還相反！先猜怎麼讀？', '拉高懸念', 'S:L05'),
)

kid(
    'kid-book-guess',
    'Waist-up medium shot of the girl at a tidy oak desk by a bright window tracing her finger horizontally from left to right in the air with a confident grin',
    k('我猜手機讀那個黑白方塊，', '很有把握的錯猜', 'S:L06'),
    k('是像看書從左上角讀起嗎？', '很有把握的錯猜'),
    chapter='三個角落抓方向，白邊被吃掉就瞎了',
)

scene(
    'chief-barcode-compare',
    'Close-up on a cool pale-slate counter in bright morning light of a tilted paper label of vertical dark stripes where a slanted red laser beam misses half the bars beside a glowing coral-red cross',
    c('要是像看書那樣死板，你手機拿歪一點不就全讀錯了？', '輕鬆反問', 'P:L06'),
    c('以前超市常見的一維條碼，真的只往橫的單一方向排線條。', '輕鬆反問'),
)

scene(
    'barcode-vs-square',
    'Overhead close-up on a wooden counter comparing a narrow row of vertical dark stripes holding a tiny handful of glass beads on the left and a square mosaic grid packed both across and down with glowing beads on the right',
    c('那種傳統條碼最多大約只能裝二十個英數字元，', None),
    c('以前單線紅光刷條碼，你沒橫切過線條就讀不到。', None),
)

scene(
    'square-two-way',
    'Close-up of a neat square wooden mosaic board on an oak tabletop with two perpendicular mint arrows running across and down its rows of dark and light tiles',
    c('一般方形的 QR Code，改成橫的、直的兩個方向都裝資訊，', '清楚推進'),
    c('還在三個角落放了大大的回字形定位方框！', '清楚推進'),
)

scene(
    'three-corners-spin',
    'Overhead medium shot of a square mosaic stand spinning on a sunlit cafe table while its three bold nested corner squares glow warm gold and a handheld phone locks onto them',
    c('不管你正著拿、歪著拿、甚至整個倒過來，', '輕快有力'),
    c('三百六十度任何角度，鏡頭一抓到三個角就知道碼在哪裡！', '輕快有力'),
)

kid(
    'kid-fourth-corner',
    'Head-and-shoulders close-up of the girl in a cheerful wooden craft studio pointing at the fourth corner of a wooden square mosaic board with a puzzled frown',
    k('等一下，正方形明明有四個角！', '抓到破綻的語氣', 'S:L07'),
    k('為什麼偏偏少畫第四個角？', '抓到破綻的語氣'),
)

scene(
    'chief-fourth-rotate',
    'Overhead close-up on a cool pale-slate tabletop of two mosaic tiles each sporting four identical corner boxes, linked by a curved turquoise half-turn arrow showing identical upside-down orientation',
    c('你想想看，要是四個角落全都畫上長得一模一樣的大方框，', '引導想像'),
    c('整張碼轉了半圈，手機怎麼分得出哪邊是頭、哪邊是腳？', '引導想像'),
)

chief(
    'chief-fourth-answer',
    'Waist-up medium shot of the chief in a cheerful wooden craft studio tapping one corner of a wooden square frame with a crisp nod',
    c('正因為第四個角故意不畫大框，', '揭曉肯定'),
    c('不管轉幾度，手機一眼就認得出上下左右！', '揭曉肯定', 'P:L07', 200),
)

kid(
    'kid-clutter-q',
    'Waist-up medium shot of the girl at a warm wooden bubble-tea counter looking around at patterned drink cups, striped straws and checkered coasters with a skeptical look',
    k('可是飲料店桌上到處都是黑線條，', '懷疑追問', 'S:L08'),
    k('鏡頭怎麼不會把別的花紋看錯？', '懷疑追問'),
)

chief(
    'chief-hara-team',
    'Waist-up medium shot of the chief in front of a tidy wooden bookcase holding up two fingers with warm respect',
    c('還記得開頭發明它的兩位日本工程師嗎？', '說故事口吻'),
    c('一九九四年發表時，汽車零件廠 DENSO 原昌宏團隊只有兩人！', '說故事口吻'),
)

scene(
    'chief-hara-qr-name',
    'Close-up on a bright sunlit desk of a mosaic table stand beside a ruled grid sheet, where a camera viewfinder frame locks onto the grid sheet corner instead beside a glowing coral-red cross',
    c('QR 就是英文 Quick Response，意思是快速反應。', None),
    c('要是鏡頭老是把旁邊的表格看錯成定位框，根本快不起來！', None),
)

scene(
    'survey-brochures',
    'Wide view of a sunlit wooden studio table piled high with colourful geometric pattern swatches, striped gift boxes and shipping cartons under a brass magnifying glass',
    c('他們先挑了商務表單上最少見的正方形，', '節奏明快'),
    c('接著抱來數不清的傳單、雜誌和紙箱，全部轉成黑白圖樣！', '節奏明快'),
)

scene(
    'survey-measuring',
    'Close-up of two pairs of hands using brass calipers to measure black-and-white stripe swatches spread across a wooden workbench',
    c('兩個人連續好幾天從早到晚，一筆一筆統計黑白寬度。', '懸疑推進'),
    c('猜猜看，這些印刷品裡最罕見的比例是幾比幾？', '懸疑推進'),
)

scene(
    'ratio-blocks',
    'Close-up of one bold nested square corner frame sliced across its center by a glowing gold line beside five chunky wooden blocks in exact widths: thin dark, thin pale, triple-wide dark, thin pale, thin dark',
    c('最後找出來的罕見節奏，就是一比一比三比一比一！', '揭曉重音', 'P:L02', 200),
    c('切過回字框正中心，黑、白、黑、白、黑剛好就是這個寬度比！', '揭曉重音'),
)

chief(
    'chief-ratio-any-angle',
    'Waist-up medium shot of the chief at a tidy oak desk by a bright window slicing her open hand across the air diagonally with a confident smile',
    c('不管鏡頭從橫的、直的、斜的切過去，', None),
    c('只要撞見一比一比三比一比一，馬上確定找到碼了！', None, 'P:L08'),
)

kid(
    'kid-curved-can',
    'Waist-up medium shot of the girl at a warm wooden bubble-tea counter holding up a cold curved aluminium soda can with a mosaic grid on its side, squinting at it',
    k('那如果印在彎彎的飲料罐上，', '歪頭追問', 'S:L09'),
    k('格子都彎掉了，也能對準嗎？', '歪頭追問'),
)

scene(
    'alignment-can',
    'Close-up of a curved mint-blue aluminium beverage can on a wooden table showing a geometric mosaic grid with one small nested alignment square glowing coral near the lower right',
    c('日常掃的改良版叫 Model 2，裡面藏了小校正圖形。', '溫和清楚', 'P:L09'),
    c('印在彎曲罐子上，鏡頭也能參照這顆小框把格子對齊！', '溫和清楚'),
)

scene(
    'chief-tilted-angle',
    "Low-angle close-up at a sunlit cafe table of a tilted sleek smartphone projecting a glowing mint-green alignment grid onto a table stand's three corner boxes and tiny alignment box with a mint check",
    c('就算你坐在餐桌斜邊、拿手機斜斜地拍過去，', None),
    c('畫面稍微變形了，它照樣能幫忙順利讀出來！', None),
)

kid(
    'kid-why-second-failed',
    'Head-and-shoulders close-up of the girl at a warm wooden bubble-tea counter holding up a square acrylic stand with a stylized dark mosaic grid crowded right up to its edges by floral vine trim with both eyebrows raised in confusion',
    k('既有三個大角又有小校正框，', '不解追問', 'S:L10'),
    k('為什麼第二張乾淨新碼還是失敗？', '不解追問'),
)

scene(
    'quiet-zone-compare',
    'Overhead close-up of two square mosaic stands on an oak counter: the left sits inside a clean wide four-tile pale margin with a mint check glow, the right has floral vines pressing right against its outer dark tiles',
    c('兇手就在最外面那圈白邊！官方叫留白區，也叫靜區。', '轉折強調', 'P:L10'),
    c('規定四個邊都要留出四格寬、完全不印東西的乾淨空白！', '轉折強調'),
)

chief(
    'chief-quiet-zone-fail',
    'Head-and-shoulders close-up of the chief at a tidy oak desk by a bright window framing a small square with her fingers and shaking her head',
    c('那張新碼把花邊貼太近、吃掉四格白邊，', None),
    c('鏡頭連碼的邊界在哪裡都分不出來，直接卡在找邊界！', None),
)

kid(
    'kid-ch1-turn',
    'Head-and-shoulders close-up of the girl at a warm wooden bubble-tea counter holding up a square acrylic stand with a stylized dark mosaic grid, three nested corner squares and a brown iced-coffee splash near the middle and pointing right at the brown coffee blotch in the middle',
    k('原來第二張連邊界都沒抓到！', '恍然大悟又追問'),
    k('那第一張被蓋住的黑格，怎麼救回來？', '恍然大悟又追問', 'S:L11'),
)

chief(
    'chief-modules-intro',
    'Waist-up medium shot of the chief in a cheerful wooden craft studio pinching two fingers together to show one tiny square tile with a calm smile',
    c('邊界跟方向抓穩之後，鏡頭才開始讀裡面的黑白小方點。', None),
    c('每一顆黑白小方點，正式名字叫做一個『模組』！', None),
    chapter='八位元裝成一盒，太空數學補缺口',
)

scene(
    'versions-small-to-mid',
    'Overhead close-up of three square wooden mosaic boards on a craft bench growing step by step from a coarse twenty-one-by-twenty-one grid on the left to medium grids on the right',
    c('最小的版本一，整張是二十一乘二十一顆模組；', '清楚有畫面感'),
    c('每往上升一版，每邊就多長出四顆模組。', '清楚有畫面感'),
)

scene(
    'version-forty-giant',
    'Wide view of a huge finely detailed square wooden mosaic board resting on an easel in a sunlit workshop beside a tiny coarse Version-one board',
    c('一路長到最大的版本四十，每邊有一百七十七顆模組，', '驚嘆推進'),
    c('最多能塞進七千零八十九個純數字，或四千兩百九十六個英數字！', '驚嘆推進'),
)

kid(
    'kid-copy-guess',
    'Waist-up medium shot of the girl in a cheerful wooden craft studio holding up three fingers with a cheeky confident grin',
    k('我猜到怎麼救咖啡漬了！', '得意猜錯', 'S:L12'),
    k('一定是把同一個網址抄三遍吧？', '得意猜錯'),
)

chief(
    'chief-copy-refute',
    'Waist-up medium shot of the chief in a sunlit wooden craft studio raising one open hand to gently shake off a guess',
    c('要是傻傻抄三遍，三分之二的空間都浪費在重複的字了！', '笑著推翻', 'P:L12'),
    c('萬一那滴冰咖啡剛好把備份也蓋住，不就照樣完蛋？', '笑著推翻'),
)

chief(
    'chief-codeword-box',
    'Head-and-shoulders close-up of the chief in a cheerful wooden craft studio holding a small eight-slot wooden box of four dark and four light pegs',
    c('真正的辦法聰明多了！手機不是單獨一顆一顆救，', None),
    c('而是把八個位元打包成一小盒，叫做一個『碼字』。', None),
)

kid(
    'kid-one-dot-q',
    'Head-and-shoulders close-up of the girl in a cheerful wooden craft studio squinting closely at one chunky wooden mosaic square held between two fingers',
    k('一個碼字，', '確認細節', 'S:L13'),
    k('不是我看到的單獨一小格喔？', '確認細節'),
)

scene(
    'peg-boxes-row',
    'Close-up of neat light-wood square trays on a workbench, each tray holding eight dark-and-light round wooden pegs packed snugly together as one unit',
    c('對，要八個位元合起來才算一盒碼字！', '肯定清楚', 'P:L13'),
    c('原資料裝成一排小盒，後面再加上數學算出來的修正碼字。', '肯定清楚'),
)

chief(
    'chief-rs-origin',
    'Waist-up medium shot of the chief in front of a starry night window pointing upward with a proud intrigued smile',
    c('這套數學叫做 Reed-Solomon 碼，', '驚喜揭曉', 'P:L03'),
    c('就是開頭提到，連遙遠太空通訊都靠它保護訊號！', '驚喜揭曉'),
)

scene(
    'space-probe-signal',
    'Medium shot of a golden-winged planetary space probe floating in starry deep space sending glowing wave rings back toward a small blue Earth',
    c('人造衛星和行星探測器從外太空傳資料回地球，', '畫面感強'),
    c('就算半路遇到通訊雜訊，也能靠它把錯字救回來。', '畫面感強'),
)

scene(
    'music-cd-gleam',
    'Close-up of a shiny silver compact disc spinning inside a player with rainbow reflections gleaming across one tiny surface scratch while musical notes float up',
    c('後來連家裡的音樂 CD 刮到一點點還能照常唱歌，', None),
    c('背後用的也是同一套數學！', None),
)

kid(
    'kid-math-how',
    'Head-and-shoulders close-up of the girl at a tidy oak desk by a bright window tilting her head with big curious eyes and both palms open',
    k('沒有抄備份，', '好奇追問', 'S:L14'),
    k('光靠數學怎麼算出被蓋住什麼？', '好奇追問'),
)

scene(
    'three-bowls-setup',
    'Close-up of three ceramic bowls on an oak table holding three, five and two glass marbles beside a woven basket holding ten marbles',
    c('打個最簡單的比方：假設你有三個數字，三、五、二。', '親切比喻'),
    c('你不抄備份，只在旁邊多記一條線索：三個加起來等於十。', '親切比喻'),
)

scene(
    'three-bowls-solve',
    'Close-up of the same three ceramic bowls where a brown coffee napkin covers the middle bowl while five glowing marbles appear in a thought bubble above it',
    c('就算中間那個數被蓋住，你拿十減掉三和二，', '輕快揭曉'),
    c('馬上就算出中間一定是五！', '輕快揭曉', 'P:L14', 200),
)

chief(
    'chief-unknown-spot',
    'Waist-up medium shot of the chief at a tidy oak desk by a bright window raising two fingers seriously to make a clear distinction',
    c('當然，真正的演算法比加法厲害得多！', '轉折推進'),
    c('既然手機事先不知道哪一盒髒了，怎麼抓出來修？', '轉折推進'),
)

scene(
    'two-for-one-boxes',
    'Close-up on a wooden workbench of one coffee-stained peg-box on the left balanced on a small wooden seesaw against two gold-trimmed rescue peg-boxes on the right',
    c('它得同時抓出『哪一盒壞掉』，再算出『原本裝什麼』。', '清楚放慢'),
    c('所以每想救回一個壞碼字，就得事先準備兩個修正碼字！', '清楚放慢', 'P:L11'),
)

scene(
    'chief-denso-example',
    'Overhead close-up on a cool pale-slate desk of ten neat rows of ten sky-blue eight-peg wooden boxes, half shaded under a translucent espresso coffee tint inside a glowing golden rescue bracket',
    c('後來獨立的開發方 DENSO WAVE 舉過算例：', None),
    c('假設原本有一百盒資料碼字，希望壞掉五十盒也能救回來，', None),
)

scene(
    'hundred-plus-hundred',
    'Overhead medium shot of two equal neat blocks of tiny wooden peg-boxes on a table: dark-trimmed data boxes on the left and gold-trimmed rescue boxes on the right',
    c('就得加上兩倍的一百盒修正盒，總共兩百盒，', '清楚有力'),
    c('官方把修正率算成百分之二十五！', '清楚有力'),
)

kid(
    'kid-fifty-percent-q',
    'Head-and-shoulders close-up of the girl at a tidy oak desk by a bright window counting on her fingers with her brow furrowed in disbelief',
    k('等一下！剛才說一百盒救回五十盒，', '抓到矛盾大聲問', 'S:L15'),
    k('不是一半嗎？怎麼只算剛剛那二十五？', '抓到矛盾大聲問'),
)

chief(
    'chief-stain-hits-both',
    'Head-and-shoulders close-up of the chief at a warm wooden bubble-tea counter smiling and spreading both hands wide as if a coffee drop just splashed',
    c('因為冰咖啡滴下來的時候，才不會看路閃開修正碼字啊！', '好笑又清楚', 'P:L15'),
    c('原本的資料盒跟後來的修正盒，統統印在同一張圖上。', '好笑又清楚'),
    chapter='號稱能救三成，為什麼不能隨便剪？',
)

scene(
    'splash-across-all',
    'Overhead close-up of dark-trimmed data boxes and gold-trimmed rescue boxes mingled on a wooden tray with a brown coffee splash covering a few of both kinds',
    c('剛剛那兩百盒裡面，不管是哪五十盒髒掉都能修好。', None),
    c('拿全部總碼字當分母一除，就是剛剛說的百分之二十五，對應 Q 級！', None),
)

chief(
    'chief-four-levels-intro',
    'Waist-up medium shot of the chief in front of a tidy wooden bookcase holding up four fingers with a clear steady smile',
    c('官方一共把錯誤修正分成 L、M、Q、H 四個等級：', '清楚列舉'),
    c('L 級大約能救總碼字的百分之七，M 級大約百分之十五，', '清楚列舉'),
)

scene(
    'four-shields-levels',
    'Medium shot of four sturdy wooden shield emblems in ascending sizes lined up on a shelf, from a small sky-blue shield on the left to a large gold-trimmed shield on the right',
    c('往上的 Q 級就是剛剛算過的約百分之二十五，', '清楚列舉'),
    c('最高的一級 H，大約能救回總碼字的百分之三十！', '清楚列舉'),
)

kid(
    'kid-scissors-guess',
    'Waist-up medium shot of the girl in a cheerful wooden craft studio miming a snipping motion with two fingers like scissors and grinning',
    k('剛剛說開到 H 級約救三成，', '天真大膽的錯猜', 'S:L16'),
    k('那拿剪刀隨便剪掉三成也能掃囉？', '天真大膽的錯猜'),
)

scene(
    'chief-not-guaranteed',
    'Close-up on a cool pale-porcelain studio desk in bright daylight of open silver craft scissors poised beside one big corner finder box of a mosaic card under a glowing coral-red warning cross',
    c('千萬別拿剪刀試！官方明寫能不能救要看污損情況，', '急忙提醒，轉向觀眾', 'P:L16'),
    c('可從來沒保證怎麼傷都一定救得回來！', '急忙提醒，轉向觀眾'),
)

chief(
    'chief-codewords-not-area',
    'Head-and-shoulders close-up of the chief in a cheerful wooden craft studio holding up one small wooden peg-box in one hand and a wide square frame in the other',
    c('更重要的是，剛剛那百分比算的是『總碼字盒數』，', '清楚強調'),
    c('根本不是整張圖讓你隨便撕掉的面積！', '清楚強調'),
)

scene(
    'corner-blotch-fail',
    'Close-up of a square mosaic stand where one tiny dark ink drop lands squarely over one of the three nested corner frames while a phone viewfinder ring drifts unable to lock on',
    c('你想，要是小小一滴墨水偏偏蓋爛了角落定位方框，', '對比鮮明'),
    c('手機連碼都認不出來，後面再多修正盒也輪不到上場！', '對比鮮明', None, 200),
)

kid(
    'kid-center-logo-q',
    'Waist-up medium shot of the girl at a warm wooden bubble-tea counter pointing at a square mosaic stand that has a small star emblem pasted right in its center',
    k('難怪有些店家的碼中間貼小圖案，', '突然想通追問', 'S:L17'),
    k('居然還是掃得出來！', '突然想通追問'),
)

chief(
    'chief-center-logo-a',
    'Waist-up medium shot of the chief at a warm wooden bubble-tea counter nodding approvingly while tapping the center of her open palm',
    c('完全正確！小圖案貼在正中央，剛好避開三個角跟四周白邊。', None, 'P:L17'),
    c('只要事先把容錯等級調高，預留夠多的修正碼字，', None),
)

scene(
    'center-emblem-rescue',
    'Close-up of a square wooden mosaic board with a small coral star emblem in the center while gold-trimmed rescue boxes along the side glow mint green',
    c('手機掃到的時候，就會把中間被擋住的那幾盒，', '清楚揭曉'),
    c('直接當成壞掉的碼字，靠數學算回來！', '清楚揭曉'),
)

kid(
    'kid-logo-limit-q',
    'Head-and-shoulders close-up of the girl at a warm wooden bubble-tea counter making a playfully big circle with both hands and raising her eyebrows',
    k('原來那是先花掉救命額度喔！', '恍然又追問', 'S:L18'),
    k('貼了圖就更怕再沾到髒東西囉？', '恍然又追問'),
)

chief(
    'chief-logo-limit-a',
    'Head-and-shoulders close-up of the chief at a warm wooden bubble-tea counter pointing warmly at her with a confirming nod',
    c('沒錯，先用掉一部分額度，再沾到咖啡就更容易爆表！', '讚許肯定', 'P:L18'),
    c('那還記得開頭問你的嗎？要是兩張碼遮一樣大——', '拋出懸念'),
)

kid(
    'kid-pepper-guess',
    'Head-and-shoulders close-up of the girl at a tidy oak desk by a bright window tapping tiny imaginary dots in the air with one fingertip and smiling confidently',
    c('一邊是一整滴濃咖啡，一邊是散開的小墨點，誰比較好救？', '拋出懸念'),
    k('散開的小墨點每顆都小小一點，', '直覺錯猜'),
    k('應該比較好救吧？', '直覺錯猜'),
)

chief(
    'chief-whole-box-rule',
    'Waist-up medium shot of the chief at a tidy oak desk by a bright window holding up a wooden peg-box with both hands and shaking her head with a grin',
    c('答案剛好顛倒！秘密就在剛剛說的『八位元一整盒一起算』！', '反轉揭曉', 'P:L05', 200),
    c('Reed-Solomon 修錯時，最小單位就是一整盒碼字。', '反轉揭曉'),
    chapter='一整滴咖啡救得活，散成小點卻全廢',
)

scene(
    'one-peg-vs-eight-pegs',
    'Close-up of two light-wood eight-peg boxes side by side on an oak table: the left box has just one peg smudged brown, the right box has all eight pegs smudged brown, and both carry the same single coral cross token',
    c('在同一盒裡，不管你只弄髒一個位元，還是八個位元全毀，', '清楚對比'),
    c('在解碼器的帳本上，統統都記成『壞掉一盒碼字』！', '清楚對比'),
)

scene(
    'burst-puddle-two-boxes',
    'Overhead close-up of eight neat wooden peg-boxes on a table where one round brown coffee puddle covers just two adjacent boxes while six boxes stay clean',
    c('所以官方特別指出，它最擅長對付『集中的突發損傷』！', '畫面感強'),
    c('八滴咖啡聚成一坨蓋住兩盒，帳本只壞兩盒，輕鬆救活。', '畫面感強'),
)

scene(
    'scatter-drops-eight-boxes',
    'Overhead close-up of eight neat wooden peg-boxes on a table where eight tiny dark ink droplets land one inside each of the eight separate boxes',
    c('可是像撒胡椒一樣散進八個盒子裡，就算每盒只髒一點，', '戲劇轉折'),
    c('帳本一口氣壞八盒，額度就很容易爆表！', '戲劇轉折'),
)

kid(
    'kid-pepper-shock',
    'Head-and-shoulders close-up of the girl at a tidy oak desk by a bright window holding both hands to her cheeks with wide round eyes',
    k('每盒只沾一小點，', '驚訝恍然'),
    k('救命額度卻一下就被吃光了！', '驚訝恍然'),
)

kid(
    'kid-why-not-all-h',
    'Waist-up medium shot of the girl in a cheerful wooden craft studio raising one fist energetically with an eager look',
    k('那既然 H 級能救最多盒，', '順勢追問', 'S:L19'),
    k('為什麼不把每張碼都開到最高 H 級？', '順勢追問'),
)

chief(
    'chief-space-tradeoff',
    'Waist-up medium shot of the chief in a cheerful wooden craft studio spreading her hands like a crowded suitcase that will barely close',
    c('因為修正碼字也要佔地盤啊，天下沒有白吃的午餐！', '幽默轉向觀眾', 'P:L19'),
    c('同一版的格子總數固定，修正盒越多，原資料空間就越少。', '幽默轉向觀眾'),
)

scene(
    'v1-capacity-compare',
    'Overhead close-up of two identical small twenty-one-by-twenty-one wooden trays: the left tray holds forty-one glass marbles with few rescue blocks, the right tray is packed with rescue blocks leaving seventeen marbles',
    c('還記得剛剛最小的版本一嗎？開 L 級最多裝四十一個純數字；', None),
    c('一旦開到最高的 H 級，直接掉到只剩十七個數字！', None),
)

scene(
    'chief-upgrade-needed',
    'Overhead close-up on a cool pale-porcelain tabletop of two equal wooden trays: the left tray neatly holds all glowing blue glass marbles, while the right tray full of golden shields spills blue marbles out',
    c('反過來，要是有五十個純數字想印成碼，', '清楚推理'),
    c('版本二 M 級夠裝，改開 H 級只裝三十四個怎麼辦？', '清楚推理'),
)

scene(
    'version-upgrade-grid',
    'Medium shot of two square wooden mosaic boards on a craft desk: a smaller twenty-five-by-twenty-five board overflowing with beads beside a larger twenty-nine-by-twenty-nine board holding them all',
    c('想維持 H 級塞進剛剛那五十個數，就得升級版本三，', '清楚推理'),
    c('長大成二十九乘二十九顆模組才裝得下！', '清楚推理'),
)

scene(
    'dense-sticker-blur',
    'Close-up of two small square stickers of the exact same width on a beverage cup sleeve: the left has larger crisp dark squares, the right is crammed with tiny dense squares that blur slightly',
    c('如果杯套或發票留給你的貼紙一樣小，格子變密、黑點縮太細，', '生活感提醒'),
    c('印表機稍微暈開或你手抖一下，反而更容易掃不出來！', '生活感提醒'),
)

kid(
    'kid-tradeoff-click',
    'Head-and-shoulders close-up of the girl in a cheerful wooden craft studio giving a wry little grin with one hand on her forehead',
    k('本來想讓它更耐髒，', '恍然失笑'),
    k('結果格子太擠反而更怕糊掉！', '恍然失笑'),
)

scene(
    'chief-factory-vs-clean',
    'Close-up split view in bright light: on the left an oiled steel gear beside a rugged coarse-grid metal plate with a golden shield glow; on the right a clean glass lab dish beside a dense fine-grid card',
    c('對！所以容易沾油污的工廠常選 Q 或 H 級，', None),
    c('乾淨但資料量超大的地方就選 L 級。', None),
)

chief(
    'chief-daily-m-level',
    'Head-and-shoulders close-up of the chief in front of a tidy wooden bookcase making an okay gesture with a warm reassuring smile',
    c('而日常菜單最常選剛剛那約百分之十五的 M 級。', '親切收束'),
    c('現在看回飲料店那兩張碼，你抓出差別了嗎？', '親切收束'),
)

kid(
    'kid-solve-first',
    'Waist-up medium shot of the girl at a warm wooden bubble-tea counter holding up a square acrylic stand with a stylized dark mosaic grid, three nested corner squares and a brown iced-coffee splash near the middle with a huge proud grin',
    k('抓到了！飲料店那張沾咖啡的碼，', '自己想通，超開心'),
    k('冰咖啡沒蓋到剛剛那三個角跟白邊！', '自己想通，超開心'),
    chapter='飲料店那兩張碼，命運全解開了',
)

kid(
    'kid-solve-second',
    'Head-and-shoulders close-up of the girl at a warm wooden bubble-tea counter pointing smartly with one finger at a square acrylic stand with a stylized dark mosaic grid crowded right up to its edges by floral vine trim and beaming',
    k('而且咖啡聚成一塊，只弄壞幾盒碼字，', '篤定收束', 'P:L04'),
    k('第二張花邊吃掉白邊，連框都找不到！', '篤定收束', 'P:L01'),
)

chief(
    'chief-summary-two-steps',
    'Waist-up medium shot of the chief at a tidy oak desk by a bright window holding up two fingers warmly toward the viewer',
    c('答得漂亮！先靠剛剛那三個角、校正框和留白區抓準位置，', '溫柔收尾，轉向觀眾'),
    c('再靠剛剛那排 Reed-Solomon 修正盒補回缺口。', '溫柔收尾，轉向觀眾'),
)

chief(
    'chief-daily-look',
    'Close-up by a sunlit cafe window of the chief holding a takeaway cup sporting a neat mosaic sticker on its sleeve',
    c('下次你拿到飲料杯或發票上的方形碼，', '輕快邀請'),
    c('不妨看看它的白邊，找找右下附近有沒有小校正框！', '輕快邀請'),
)

kid(
    'outro',
    'Head-and-shoulders close-up of the girl at a warm wooden bubble-tea counter giving a big cheerful thumbs-up with one hand and a bright grin',
    k('原來如此！', '開心大聲'),
)

chief(
    'outro-chief',
    'Head-and-shoulders close-up of the chief leaning lightly on her oak desk with one finger raised and a curious smile',
    c('你掃過最慘烈的一張 QR Code 長什麼樣？', '像聊天問觀眾'),
    c('最後有沒有成功嗶過？留言告訴我們！', '像聊天問觀眾'),
)

chief(
    'outro-wave',
    'Waist-up medium shot of the chief standing beside a sunlit window with potted green plants, waving goodbye warmly',
    c('想一起拆解每天都在用的生活機關，就訂閱原來如此事務所！', '誠懇溫暖'),
)


LOOP_WHAT = {
  "L01": "為什麼沾了冰咖啡的碼掃得過，旁邊花邊貼很近的乾淨新碼卻沒反應",
  "L02": "當年兩位日本工程師天天統計傳單線條，在找什麼比例",
  "L03": "保護太空探測器訊號的數學怎麼藏進日常掃的方形碼裡",
  "L04": "QR Code 髒掉一塊到底怎麼把資料讀回來",
  "L05": "遮住一樣大的面積，為什麼一整滴咖啡跟散開的小墨點命運相反",
  "L06": "手機讀方形碼是不是像看書一樣從左上角照順序讀",
  "L07": "正方形有四個角，為什麼偏偏只在三個角畫大定位框",
  "L08": "飲料店桌上到處是黑線，手機怎麼不會把別的花紋看成定位角",
  "L09": "印在彎曲飲料罐上格子都彎了，手機怎麼對準",
  "L10": "既有三個大定位角又有小校正框，為什麼第二張乾淨新碼還是失敗",
  "L11": "框抓到之後，裡面被咖啡蓋住的黑格子怎麼猜回來",
  "L12": "缺一塊還能讀，是不是把同一個網址偷偷抄了三遍",
  "L13": "一個碼字是不是眼睛看到的單獨一小格",
  "L14": "沒有抄備份，光靠數學怎麼算出被蓋住的內容",
  "L15": "一百盒原資料碼字救回五十盒，為什麼官方只算百分之二十五而不是一半",
  "L16": "開到最高 H 級約百分之三十，能不能拿剪刀隨便剪掉三成面積",
  "L17": "為什麼有些 QR Code 正中間貼了小圖案還是掃得出來",
  "L18": "中間貼了小圖案的 QR Code，是不是會先花掉一部分救命額度",
  "L19": "既然 H 級能救最多碼字，為什麼不把所有 QR Code 都開到最高 H 級"
}
LOOP_ORDER = ["L01", "L02", "L03", "L04", "L05", "L06", "L07", "L08", "L09", "L10", "L11", "L12", "L13", "L14", "L15", "L16", "L17", "L18", "L19"]

scenes = []
loops_s = {}
loops_p = {}
n = 0
for s in S:
    ls = []
    for spk, text, emo, tag, pause in s["lines"]:
        n += 1
        lid = f"p{n:03d}"
        item = {"id": lid, "speaker": spk, "text": text}
        if emo is not None:
            item["emotion"] = emo
        if pause is not None:
            item["pause_after_ms"] = pause
        if tag:
            for part in tag.split(","):
                kind, key = part.split(":")
                if kind == "S":
                    loops_s[key] = lid
                elif kind == "P":
                    loops_p[key] = lid
        ls.append(item)
    entry = dict(s)
    entry["lines"] = ls
    scenes.append(entry)

loops = [{"setup": loops_s[k], "payoff": loops_p[k], "what": LOOP_WHAT[k]} for k in LOOP_ORDER]

TOP_META = json.loads('{"schema_version": 1, "slug": "sothatswhy-p12-qr-code", "format": "drama", "category": "explainer", "narration_locale": "zh-TW", "target_minutes": [9, 12], "pauses": {"line_ms": 0, "scene_ms": 150}, "still_motion": "beat", "voice": {"provider": "gemini", "name": "Sulafat", "style": "標準國語，咬字清楚，台北人平常說話的語調；溫暖清楚的解說主持人，像在跟一個好奇的朋友講道理，語速像節目主持人，一秒五個字以上，句與句緊接、不拖長尾音"}, "subtitles": {"burn_in": false}, "theme": "paper", "look": {"preset": "cute-cartoon"}, "series": {"slug": "sothatswhy", "episode": 12, "chapter": 1}, "music": {"track": "sothatswhy-bed-r2.m4a", "sha256": "9bb4ba6fd16feb4a7f352144b2d89e9648acbbbbaa2173c27a7eefbdb70f28c6", "gain_db": -20, "duck_db": -10}, "characters": [{"id": "chief", "name": "所長", "appearance": "a friendly middle-aged woman, the chief of a small question office, with round black glasses, shoulder-length dark hair with a streak of grey tied in a low ponytail, a warm smile, a mustard-yellow cardigan over a white blouse, ink-navy trousers, brown shoes, a yellow pencil tucked behind one ear", "voice": {"provider": "gemini", "name": "Sulafat", "style": "標準國語，咬字清楚，台北人平常說話的語調；溫暖清楚的解說主持人，像在跟一個好奇的朋友講道理，語速像節目主持人，一秒五個字以上，句與句緊接、不拖長尾音"}, "sheet_prompt": "character reference: one single full-body figure standing in the centre, facing the viewer in a slight three-quarter turn, relaxed friendly pose, both hands clearly drawn, plain empty cream background with nothing else in the picture, no turnaround, no second view, no seal, no stamp, no signature, no text"}, {"id": "kid", "name": "小問", "appearance": "a curious eight-year-old girl with a short black bob haircut with straight bangs and one small cowlick sticking up on top, large round eyes, wearing a navy raincoat-style jacket with a mustard-yellow hood, white sneakers, both hands free", "voice": {"provider": "gemini", "name": "Leda", "style": "標準國語，咬字清楚，台北人平常說話的語調；好奇愛發問的年輕女生，像觀眾的嘴替，語氣輕快自然，語速像節目主持人，一秒五個字以上，句與句緊接、不拖長尾音"}, "sheet_prompt": "character reference: one single full-body figure standing in the centre, facing the viewer in a slight three-quarter turn, relaxed friendly pose, both hands clearly drawn, plain empty cream background with nothing else in the picture, no turnaround, no second view, no seal, no stamp, no signature, no text"}], "youtube": {"category_id": 27, "made_for_kids": false, "default_language": "zh-TW", "title": "QR Code 沾到咖啡還能嗶，旁邊新碼卻失靈？｜原來如此事務所", "description": "飲料店桌上的 QR Code 沾了一大塊冰咖啡，手機一照居然照樣「嗶」一聲過關；旁邊另一張新印的乾乾淨淨，只是花邊貼得太近，卻怎麼掃都沒反應。同樣是黑白小方格，到底差在哪裡？\\n\\n給每次掃菜單、買手搖飲遇過掃不過，或好奇日常黑白小方格裡藏了什麼機關的人。\\n\\n這一集，所長和小問順著手機掃碼的瞬間一路拆解：三個角落為什麼能三百六十度抓方向、一九九四年問世前兩人團隊怎麼從成堆印刷品裡找出最罕見的黑白比例、太空探測器與音樂 CD 都在用的數學怎麼把缺掉的資料算回來，以及號稱最高約 30% 的容錯率到底在算什麼、為什麼遮住一樣大，一整滴咖啡跟散開的小墨點結果可能完全相反。\\n\\n本集插圖由 AI 生成。\\n\\n資料截至 2026-11-14", "tags": ["QR Code", "QR Code 原理", "QR Code 容錯", "Reed-Solomon", "錯誤修正碼", "條碼原理", "科普", "原來如此事務所"], "video_id": null}, "thumbnail": {"template": "thumb", "data": {"headline": "缺一塊\\n**還能嗶？**", "sub": "花邊貼太近反而掃不過", "tag": "科技", "pillar": "tech", "shot": "kid-solve-first", "subject": "right"}, "variants": [{"data": {"headline": "髒一大塊\\n**照樣嗶？**"}}, {"data": {"headline": "清晰 vs\\n**過密？**", "sub": "印在杯套上差在哪？", "shot": "dense-sticker-blur"}}]}, "sources": [{"title": "DENSO WAVE: What is a QR Code?", "url": "https://www.qrcode.com/en/about/", "checked_on": "2026-11-14"}, {"title": "DENSO WAVE: Readable from any direction in 360°", "url": "https://www.qrcode.com/en/about/featurePage/featurePage5.html", "checked_on": "2026-11-14"}, {"title": "DENSO WAVE: History of QR Code", "url": "https://www.qrcode.com/en/history/", "checked_on": "2026-11-14"}, {"title": "DENSO WAVE: QR Code Model 1 and Model 2", "url": "https://www.qrcode.com/en/codes/model12.html", "checked_on": "2026-11-14"}, {"title": "DENSO WAVE: Point for determining the code area", "url": "https://www.qrcode.com/en/howto/code.html", "checked_on": "2026-11-14"}, {"title": "DENSO WAVE: Information capacity and versions of QR Code", "url": "https://www.qrcode.com/en/about/version.html", "checked_on": "2026-11-14"}, {"title": "DENSO WAVE: Error correction feature", "url": "https://www.qrcode.com/en/about/error_correction.html", "checked_on": "2026-11-14"}, {"title": "DENSO WAVE: QR Code Standardization", "url": "https://www.qrcode.com/en/about/standards.html", "checked_on": "2026-11-14"}, {"title": "Riley & Richardson: An introduction to Reed-Solomon codes (CMU CS)", "url": "https://www.cs.cmu.edu/~guyb/realworld/reedsolomon/reed_solomon_codes.html", "checked_on": "2026-11-14"}, {"title": "Wikipedia: QR code", "url": "https://en.wikipedia.org/wiki/QR_code", "checked_on": "2026-11-14"}, {"title": "Wikipedia: Reed–Solomon error correction", "url": "https://en.wikipedia.org/wiki/Reed%E2%80%93Solomon_error_correction", "checked_on": "2026-11-14"}], "assets": []}')

doc = {}
for k in ['schema_version', 'slug', 'format', 'category', 'narration_locale', 'target_minutes', 'pauses', 'still_motion', 'voice', 'subtitles', 'theme', 'look', 'series', 'music', 'characters', 'loops', 'youtube', 'thumbnail', 'sources', 'assets', 'scenes']:
    if k == "loops":
        doc[k] = loops
    elif k == "scenes":
        doc[k] = scenes
    else:
        doc[k] = TOP_META[k]

with open(os.path.join(HERE, "video.json"), "w", encoding="utf-8") as fh:
    json.dump(doc, fh, ensure_ascii=False, indent=2)
    fh.write("\n")

FROZEN.update({s["id"]: s["data"]["camera"] for s in scenes if s["template"] == "shot" and s["id"] not in FROZEN})
with open(CAM_FILE, "w", encoding="utf-8") as fh:
    json.dump(FROZEN, fh, ensure_ascii=False, indent=1)
