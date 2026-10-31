EP = 52
EP_TITLE = "真印假印"
OUTLINE_SECONDS = 110
TARGET_MINUTES = [1, 2]
TITLE = "抓她的公文蓋著州府大印，他拿喜報一比：差了一筆｜種田娶妻打天下 第52集"
DESCRIPTION = "阿令指著公文抄本上的朱印：「真印的『州』字，這一筆是斷的。」唐小棠想問她怎麼知道，許硯抬手攔住：「不用問。我信她。」要證明公文是假的，得有一張確定是真的州府公文來比。秦家軍老兵杜鐵拄著拐杖趕來，許硯託他盯著州牢；唐小棠去求知府夫人。州府大堂上，知府不在，坐堂的通判一口咬定大印是他親眼看著蓋的，翻臉就要趕人。許硯從懷裡掏出自己的解元喜報——蓋的是如假包換的州府大印。兩張紙疊在燭火前，紅印透光重合，只有一筆錯開，像一道裂縫。知府夫人把褚知府請回府，知府當堂簽下追回令。許硯說：「是我娘子看出來的。」又對唐小棠說：「沒有妳，今天就輸了。」話剛說完，杜鐵撞進大堂：囚車天沒亮就出了北門，押車的不是州府的人。《種田娶妻打天下》第 52 集。"
THUMB = ("差一筆", "s24")
CHARACTERS = ["xuyan", "aling", "tangxiaotang", "dutie", "tongpan", "zhifufuren", "chuzhifu", "xitong"]
MINOR = {
    "tongpan": {"id": "tongpan", "name": "通判", "appearance": "East Asian man of forty-five, plump and pale with heavy-lidded eyes and a thin drooping moustache, a dark blue official robe with a square embroidered badge on the chest and a black official gauze hat", "voice": {"provider": "gemini", "name": "Charon", "style": "標準國語，咬字清楚，台北人平常說話的語調；四十五歲的州府通判，男聲、倨傲、官腔十足，被逼急了就翻臉，心虛時結巴"}},
    "zhifufuren": {"id": "zhifufuren", "name": "知府夫人", "appearance": "East Asian woman of forty-five, graceful and composed, an oval face with fine brows and calm shrewd eyes, black hair in a neat high bun with one gold hairpin, a dark plum silk jacket with a high closed collar over a long skirt of the same colour", "voice": {"provider": "gemini", "name": "Kore", "style": "標準國語，咬字清楚，台北人平常說話的語調；四十五歲的知府夫人，女聲、溫和從容、話不多但很有主意"}},
}
MUSIC = "a cool single guqin pluck on the broken stroke of the seal, a warm soft xiao when he says he trusts her, a rough brass growl and a stamping drum for the old soldier's crutch, then a cold formal march of low strings and woodblock in the dim court hall, a snarling low brass when the vice-prefect turns them out, a sudden bright pipa run as the red announcement comes out of his robe, a held shimmering high string as the two seals glow through the candle flame and the one stroke parts like a crack, a gentle plucked zither in the quiet study, a full proud swell of drums and dizi when the prefect signs, two small sweet bells for the two affections, then a hard drum hit and racing strings as the old soldier crashes in, cut on one high string, ancient Chinese rural drama, no vocals"

LOC = {
    "door": "On the long street of Qingzhou at dawn in thick morning mist, in front of the open wooden door of an inn, a stone step, closed timber shopfronts with upturned eaves on both sides, unlit red lanterns, pale grey light",
    "hall": "In the court hall of the Qingzhou prefecture in the morning, a tall dim hall with red lacquered pillars, a raised dais with a long official desk draped in red cloth, a wooden gavel, a tube of bamboo tallies and one tall lit candle on it, a painted screen of sea and sun behind, runners with staves along the walls, white daylight from the open main door",
    "study": "In the prefect's residence in the Qingzhou prefecture in the morning, a quiet private study with a dark wooden desk and two armchairs, a tea set on a side table, a folding screen, shelves of case files tied with cord, a lattice door onto a small inner garden, soft morning light",
}
LIGHT = {"dawn": "the grey dawn mist stays unchanged", "hall": "the dim hall light stays unchanged"}

SHOTS = [
    dict(chapter="斷的一筆", loc="door", cam="Insert of the vermilion seal, slow push in", act=1, night="dawn", tag="鉤子1／開頭",
         comp="insert of the warrant copy held open in a slender hand with a grey-white sleeve, columns of faint blurred brush strokes that cannot be read, a square vermilion seal impression of thick curving carved lines, a slender fingertip resting on one of its curving lines where the red line breaks off short",
         lines=[("aling", "真印的「州」字，", "很輕，很篤定")],
         motion="The shot opens directly on this close insert from its very first frame; the fingertip taps twice on the broken end of the red line",
         zh="接第 51 集：一隻月白袖子的纖手拿著公文抄本，下方一方粗線條盤曲的朱紅印，指尖按在其中一道紅線斷掉的地方；指尖在斷口上點兩下"),
    dict(loc="door", cam="Close-up, locked", chars=["aling"], night="dawn", tag="鉤子1",
         comp="close-up of A-ling on screen left, her phoenix eyes on the paper below the frame, a loose strand of black hair across her cheek, her face cool and certain",
         lines=[("aling", "這一筆，", "淡淡的"), ("aling", "是斷的。", "冷")],
         motion="after the last word her eyes lift from the paper to Xu Yan off screen right",
         zh="阿令特寫在左，鳳眼看著畫面下方的紙，一縷黑髮落在臉頰，又冷又篤定；說完眼睛從紙上抬起來看畫外右邊的許硯"),
    dict(loc="door", cam="Close-up, slow push in", chars=["tangxiaotang"], night="dawn",
         comp="close-up of Tang Xiaotang on screen right in the inn doorway, her high stand-up collar fastened at the throat, her big round eyes wide, her lips parting, looking at A-ling off screen left",
         lines=[("tangxiaotang", "阿令，妳怎麼……", "又驚又好奇")],
         motion="she steps half a pace toward A-ling with one hand raised as if to ask more",
         zh="唐小棠特寫在右、客棧門口，高領扣到喉嚨，大圓眼睛睜大、嘴唇張開，看著畫外左邊的阿令；往阿令跨半步，一手舉起來還要再問"),
    dict(loc="door", cam="Two-shot, locked", chars=["xuyan", "aling"], night="dawn", tag="鉤子1",
         comp="two-shot by the inn step, A-ling on screen left holding the warrant copy, Xu Yan on screen right lifting one open hand toward Tang Xiaotang off screen right, his eyes on A-ling",
         lines=[("xuyan", "不用問。", "抬手攔住，很穩"), ("xuyan", "我信她。", "看著阿令")],
         motion="he holds the open hand up for a beat, then lowers it and turns to face A-ling",
         zh="雙人鏡：客棧台階邊，阿令在左拿著抄本，許硯在右朝畫外的唐小棠舉起一隻手攔住，眼睛看著阿令；手停一拍，放下，轉身面向阿令"),
    dict(loc="door", cam="Close-up, locked", chars=["aling"], act=2, night="dawn",
         comp="close-up of A-ling on screen left, her cold eyes on Xu Yan off screen right, her lips slightly parted",
         motion="her lips part as if to speak, then she lowers her eyes and folds the warrant copy in half with one neat crease",
         zh="阿令特寫在左，冷冷的眼睛看著畫外右邊的許硯，嘴唇微張；像要說什麼，又垂下眼，把抄本對摺一道（她沒想到他不問）"),
    dict(loc="door", cam="Medium close-up, slow push in", chars=["xuyan"], night="dawn",
         comp="medium close-up of Xu Yan on screen right, his brows knitted in thought, one finger tapping the folded copy in A-ling's hand at the edge of the frame, his eyes on her off screen left",
         lines=[("xuyan", "要證明是假的，", "想事情"), ("xuyan", "得有一張真的比。", "低聲")],
         motion="he taps the paper twice and straightens up",
         zh="許硯中近景在右，眉頭皺著想事情，一根手指點著畫邊阿令手上的摺紙，看著畫外左邊的她；點兩下，站直"),
    dict(loc="door", cam="Close-up, locked", chars=["tangxiaotang"], night="dawn",
         comp="close-up of Tang Xiaotang on screen right, her high-collared peach-pink ruqun, the little gold abacus in her hand, her brows drawn together, looking at Xu Yan off screen left",
         lines=[("tangxiaotang", "真的州府公文，", "發愁"), ("tangxiaotang", "上哪找？", "攤手")],
         motion="she spreads both hands, the abacus swinging on its cord",
         zh="唐小棠特寫在右，高領桃粉襦裙，手上拿著小金算盤，眉頭皺起，看著畫外左邊的許硯；兩手一攤，算盤在繩上晃"),
    dict(chapter="杜鐵", loc="door", cam="Medium shot, tracking", chars=["dutie", "xuyan"], night="dawn", tag="鉤子2",
         comp="medium shot in the misty street, Du Tie limping in from screen left on his worn wooden crutch under his left arm, his patched old army jacket, his weathered face fierce, Xu Yan turning to him on screen right by the inn step",
         lines=[("dutie", "秦將軍的閨女，", "粗啞，急"), ("dutie", "真關進州牢了？", "喘著氣")],
         motion="he swings forward on the crutch in heavy uneven strides and stops in front of Xu Yan",
         zh="晨霧的街上中景：杜鐵拄著左腋下的舊木拐從左邊一拐一拐趕來，補丁舊軍襖，風霜的臉很兇，許硯在右邊台階旁轉向他；他拄拐重重地跨過來，停在許硯面前"),
    dict(loc="door", cam="Close-up, slow push in", chars=["dutie"], night="dawn",
         comp="close-up of Du Tie on screen left, his short grizzled beard, his fierce bright tiger eyes on Xu Yan off screen right, his knuckles white on the crutch",
         lines=[("dutie", "誰敢動她，", "咬牙"), ("dutie", "老子跟他拚！", "吼")],
         motion="he lifts the crutch and slams its foot down on the paving stone with a crack",
         zh="杜鐵特寫在左，花白短鬚，虎目瞪著畫外右邊的許硯，握拐的指節發白；把木拐舉起來往石板上重重一頓"),
    dict(loc="door", cam="Medium close-up, locked", chars=["xuyan"], night="dawn",
         comp="medium close-up of Xu Yan on screen right, one hand on Du Tie's shoulder at the left edge of the frame, his face steady, his eyes on Du Tie off screen left",
         lines=[("xuyan", "杜叔，", "按住他"), ("xuyan", "替我盯著州牢。", "低聲交代")],
         motion="he squeezes the shoulder once and nods toward the far end of the street",
         zh="許硯中近景在右，一手按著畫邊杜鐵的肩，臉很定，看著畫外左邊的杜鐵；按一下肩，朝長街那頭點頭"),
    dict(loc="door", cam="Medium close-up, locked", chars=["tangxiaotang"], night="dawn",
         comp="medium close-up of Tang Xiaotang on screen right, her high stand-up collar fastened at the throat, gathering her peach-pink skirt in one hand, a determined little smile, looking at Xu Yan off screen left",
         lines=[("tangxiaotang", "知府夫人那邊，", "眼睛一亮"), ("tangxiaotang", "我去說。", "很有把握")],
         motion="she lifts her skirt hem a little and turns briskly to go",
         zh="唐小棠中近景在右，高領扣到喉嚨，一手提起桃粉裙擺，嘴角一個有主意的笑，看著畫外左邊的許硯；把裙擺提起一點，俐落地轉身要走"),
    dict(loc="door", cam="Two-shot, slow push in", chars=["xuyan", "aling"], night="dawn",
         comp="two-shot, Xu Yan on screen left and A-ling on screen right setting off side by side down the misty street, his jaw set, her face cool",
         lines=[("xuyan", "我們去州府，", "邁步"), ("xuyan", "當面比。", "很穩")],
         motion="they stride off together in step, his sleeve and her skirt hem swinging",
         zh="雙人鏡：許硯在左、阿令在右，並肩往霧裡的長街走去，他下顎繃緊，她臉很冷；兩人同步大步走，袖子與裙擺擺動"),
    dict(chapter="通判", loc="hall", cam="Wide shot, locked", chars=["tongpan", "xuyan", "aling"], tag="鉤子3",
         comp="wide shot of the court hall, the vice-prefect in his dark blue robe and black gauze hat seated behind the red-draped desk on the dais on screen right, runners with staves along the walls, Xu Yan and A-ling walking in from the bright main door on screen left",
         lines=[("tongpan", "知府大人不在，", "拖長音，頭也不抬"), ("tongpan", "有事跟本官說。", "倨傲")],
         motion="the vice-prefect leans back in his chair and taps the gavel lazily, while the two of them walk up to the foot of the dais",
         zh="州府大堂全景：深藍官袍、烏紗的通判坐在右邊高台紅布長案後，兩排衙役拄著水火棍，許硯與阿令從左邊亮白的大門走進來；通判往椅背一靠，懶懶地敲一下驚堂木，兩人走到台下"),
    dict(loc="hall", cam="Medium shot, locked", chars=["xuyan"], night="hall",
         comp="medium shot of Xu Yan at the foot of the dais on screen left, bowing with both hands and holding the folded warrant copy up toward Vice-Prefect off screen right",
         lines=[("xuyan", "這張逮捕公文，", "作揖，很客氣"), ("xuyan", "印是假的。", "一字一字")],
         motion="he straightens from the bow and lifts the paper higher",
         zh="許硯中景在左、台下，雙手作揖，把摺好的公文抄本舉向畫外右邊的通判；作完揖站直，把紙舉得更高"),
    dict(loc="hall", cam="Medium close-up, locked", chars=["tongpan"], night="hall",
         comp="medium close-up of the vice-prefect on screen right behind the red-draped desk, his heavy-lidded eyes narrowing in scorn, his eyes on Xu Yan off screen left",
         lines=[("tongpan", "州府大印，", "冷笑"), ("tongpan", "本官親眼看著蓋的！", "拍案")],
         motion="he slaps his palm flat on the red cloth and leans forward",
         zh="通判中近景在右、紅布長案後，厚眼皮的眼睛輕蔑地瞇起，看著畫外左邊的許硯；手掌往紅布上一拍，身子往前探"),
    dict(loc="hall", cam="Close-up, locked", chars=["aling"], night="hall",
         comp="close-up of A-ling on screen left beside a red pillar, her chin lifted, her phoenix eyes cold on Vice-Prefect off screen right",
         lines=[("aling", "那你看錯了。", "冷冷的，不客氣")],
         motion="she takes one small step forward past Xu Yan's shoulder",
         zh="阿令特寫在左、紅柱旁，下巴抬起，鳳眼冷冷看著畫外右邊的通判；往前一小步，越過許硯的肩"),
    dict(loc="hall", cam="Medium shot, slow push in", chars=["tongpan"], night="hall", tag="鉤子4／中段鉤子",
         comp="medium shot of the vice-prefect rising from his chair behind the desk on screen right, his pale face flushing, the wooden gavel raised in his fist, his eyes on A-ling off screen left",
         lines=[("tongpan", "放肆！", "翻臉"), ("tongpan", "給我趕出去！", "吼")],
         motion="he brings the gavel down on the desk with a crack and points to the door",
         zh="中段鉤子：通判在右從長案後站起來，白臉漲紅，拳裡舉著驚堂木，瞪著畫外左邊的阿令；驚堂木「啪」地砸下，手指向大門"),
    dict(loc="hall", cam="Wide shot, locked", chars=["xuyan", "aling"], act=2, night="hall", tag="鉤子4",
         comp="wide shot from beside the dais, two runners in black on screen right stepping down toward Xu Yan and A-ling at the foot of the dais on screen left, their staves lowered across their bodies",
         motion="the runners advance two weighted steps with the staves held crosswise, and Xu Yan puts his arm out in front of A-ling",
         zh="從台邊拍的全景：右邊兩個皂衣衙役橫著水火棍走下來，逼向左邊台下的許硯與阿令；衙役重重跨兩步，許硯伸手把阿令擋在後面"),
    dict(chapter="兩方印", loc="hall", cam="Medium close-up, slow push in", chars=["xuyan"], night="hall", tag="轉折",
         comp="medium close-up of Xu Yan on screen left, one hand going into the front of his faded blue-grey robe, a calm half smile, his eyes on the vice-prefect off screen right",
         lines=[("xuyan", "慢著。", "不慌不忙"), ("xuyan", "這張呢？", "笑")],
         motion="he draws a folded sheet of red paper out of his robe and snaps it open with one flick",
         zh="轉折：許硯中近景在左，一手伸進青灰長衫的前襟，嘴角半笑，看著畫外右邊的通判；從懷裡抽出一張摺好的紅紙，手腕一抖攤開"),
    dict(loc="hall", cam="Insert of the red announcement, locked", act=1, night="hall", tag="轉折",
         comp="insert of a sheet of bright red paper held open in a young man's hands with faded blue-grey sleeves, columns of faint gold brush strokes that cannot be read, a square vermilion seal impression of thick curving carved lines at the bottom",
         lines=[("xuyan", "州府發的解元喜報。", "一字一字")],
         motion="The shot opens directly on this close insert from its very first frame; the hands lift the red paper toward the dais so the seal catches the light",
         zh="插鏡：一雙青灰袖子的手攤開一張大紅紙，一列列讀不出的金色毛筆畫（不寫字），下方一方粗線條盤曲的朱紅印；手把紅紙往高台一舉，印接住光"),
    dict(loc="hall", cam="Close-up, locked", chars=["tongpan"], night="hall",
         comp="close-up of the vice-prefect on screen right, his mouth falling open, sweat beading on his pale forehead under the gauze hat, his eyes fixed on the red paper off screen left",
         lines=[("tongpan", "這……", "愣住")],
         motion="he swallows hard and the gavel slips a little in his fingers",
         zh="通判特寫在右，嘴巴張開，烏紗下白淨的額頭冒汗，眼睛釘在畫外左邊那張紅紙上；用力吞口水，驚堂木在指間滑了一下"),
    dict(loc="hall", cam="Medium shot, locked", chars=["xuyan"], night="hall",
         comp="medium shot of Xu Yan stepping up to the red-draped desk on screen left, the warrant copy in one hand and the red announcement in the other, the tall lit candle on the desk in front of him",
         lines=[("xuyan", "兩方印，", "很穩"), ("xuyan", "對著燈看。", "舉起來")],
         motion="he lays one paper over the other and raises both together in front of the candle flame",
         zh="許硯中景在左走到紅布長案前，一手拿公文抄本、一手拿紅喜報，案上一根點著的高燭在他面前；把一張疊在另一張上，一起舉到燭火前"),
    dict(loc="hall", cam="Insert of the two seals before the candle, slow push in", act=3, night="hall", tag="鉤子5",
         comp="insert of two sheets of paper pressed together and held up before a tall candle flame, the light shining through them so that two square red seals of thick curving lines glow and lie on top of each other, every line meeting except one curving line that stands apart like a thin crack",
         motion="The shot opens directly on this close insert from its very first frame; the papers shift a hair's breadth in the fingers and settle, and the single offset line glows brighter than the rest",
         zh="奇觀：兩張紙疊在一起舉在高燭前，燭光透過來，兩方粗線條的紅印透光重合，每一道都對上，只有一道彎線錯開，像一道細細的裂縫；紙在指間挪一點停住，錯開的那一筆比別的更亮"),
    dict(loc="hall", cam="Close-up, slow push in", chars=["aling"], night="hall", tag="顏值鏡頭",
         comp="close-up of A-ling standing before the candlelight on screen left, the warm flame lighting her porcelain face and her long elegant brows, her eyes lowered to the two glowing seals before the candle",
         lines=[("aling", "差了一筆。", "很輕，篤定")],
         motion="her phoenix eyes narrow and the corner of her mouth firms with quiet certainty",
         zh="顏值鏡頭：阿令站在燭光前（畫面左），暖色的火光照著白瓷般的臉與細長的眉，垂眼看著畫外右邊透光的兩方印；鳳眼一瞇，平日冷淡的臉多了一分篤定"),
    dict(loc="hall", cam="Wide shot, slow pan right", chars=["tongpan"], act=2, night="hall",
         comp="wide shot of the court hall, the runners along the walls on screen left leaning in to look at the papers held up before the candle, the vice-prefect on the dais on screen right sinking back into his chair",
         motion="the runners crane forward and turn to murmur to each other while the vice-prefect drops heavily into his seat",
         zh="大堂全景：左邊兩排衙役探頭去看燭前的兩張紙，交頭接耳；右邊高台上的通判重重跌坐回椅子（爽點：當場揭穿）"),
    dict(loc="hall", cam="Medium close-up, locked", chars=["tongpan"], night="hall",
         comp="medium close-up of the vice-prefect on screen right gripping the arms of his chair, sweat running down his temple, his eyes darting to Xu Yan off screen left",
         lines=[("tongpan", "一筆之差，", "嘴硬"), ("tongpan", "算得了什麼？", "結巴")],
         motion="he wipes his temple with his sleeve and grips the chair again",
         zh="通判中近景在右，雙手抓著椅子扶手，汗順著太陽穴流下，眼睛往畫外左邊的許硯飄；用袖子擦一下太陽穴，又抓緊椅子"),
    dict(chapter="知府夫人", loc="study", cam="Medium shot, locked", chars=["tangxiaotang", "zhifufuren"],
         comp="medium shot in the quiet study, Tang Xiaotang in her high-collared peach-pink ruqun on screen left curtseying with her hands folded at her waist, the prefect's wife in her dark plum high-collared jacket seated in an armchair on screen right with a teacup",
         lines=[("tangxiaotang", "夫人，", "恭敬"), ("tangxiaotang", "有人借州府的印抓人。", "壓低聲音")],
         motion="she rises from the curtsey and steps closer to the armchair",
         zh="知府後宅的書房中景：高領桃粉襦裙的唐小棠在左雙手交疊腰前行禮，深紫高領的知府夫人在右坐在扶手椅上，端著茶；她起身，往椅子走近一步"),
    dict(loc="study", cam="Medium close-up, slow push in", chars=["tangxiaotang"],
         comp="medium close-up of Tang Xiaotang on screen left, her high stand-up collar fastened at the throat, her sweet face turned serious and shrewd, her eyes on the prefect's wife off screen right",
         lines=[("tangxiaotang", "出了事，", "一字一字"), ("tangxiaotang", "背鍋的是知府大人。", "算盤打得精")],
         motion="she lifts one finger and taps it lightly against the small gold abacus at her waist",
         zh="唐小棠中近景在左，高領扣到喉嚨，甜甜的臉變得精明認真，看著畫外右邊的知府夫人；舉起一根手指，在腰間的小金算盤上輕輕一點"),
    dict(loc="study", cam="Medium close-up, locked", chars=["zhifufuren"],
         comp="medium close-up of the prefect's wife on screen right in her dark plum jacket with its high closed collar, her calm shrewd eyes on Tang Xiaotang off screen left, the teacup in her hand",
         lines=[("zhifufuren", "來人，", "放下茶碗"), ("zhifufuren", "請老爺回府。", "很定")],
         motion="she sets the teacup down on the side table with a clink and rises from the armchair",
         zh="知府夫人中近景在右，深紫高領，沉穩精明的眼睛看著畫外左邊的唐小棠，手上端著茶；茶碗「叮」地放到茶几上，從扶手椅站起來"),
    dict(chapter="追回令", loc="hall", cam="Wide shot, tracking", chars=["chuzhifu", "tongpan"], tag="鉤子6",
         comp="wide shot of the court hall, Prefect Chu in his crimson robe and black gauze hat striding in from the bright main door on screen left, the runners bowing along the walls, the vice-prefect scrambling down from the dais on screen right",
         lines=[("chuzhifu", "本府的印，", "沉穩，不怒自威"), ("chuzhifu", "本府自己認。", "低")],
         motion="the prefect walks up the hall in measured strides while the vice-prefect hurries down the dais steps and bows low",
         zh="大堂全景：緋色官袍、烏紗的褚知府從左邊亮白的大門大步走進來，兩排衙役彎腰，通判在右慌忙從高台下來；知府步子穩穩地走上來，通判跑下台階深深一揖"),
    dict(loc="hall", cam="Medium close-up, slow push in", chars=["chuzhifu"], night="hall",
         comp="medium close-up of Prefect Chu on screen left holding the two papers up before the candle, his thick black brows drawing down, his steady deep-set eyes moving from the seals to Vice-Prefect off screen right",
         lines=[("chuzhifu", "這張公文，", "壓低聲音"), ("chuzhifu", "誰送來的？", "盯著通判")],
         motion="he lowers the papers slowly and turns his head toward the vice-prefect",
         zh="褚知府中近景在左，把兩張紙舉在燭前，濃眉往下壓，沉穩的深眼從印上移到畫外右邊的通判；慢慢放下紙，轉頭看向通判"),
    dict(loc="hall", cam="Close-up, locked", chars=["tongpan"], night="hall",
         comp="close-up of the vice-prefect on screen right bowed low, his gauze hat tilted, sweat on his face, his eyes on the floor",
         lines=[("tongpan", "下、下官……", "結巴"), ("tongpan", "不知。", "聲音發抖")],
         motion="he bows lower and his folded hands shake",
         zh="通判特寫在右，腰彎得很低，烏紗歪了，滿臉是汗，眼睛盯著地；腰再彎下去，合著的手發抖"),
    dict(loc="hall", cam="Insert of the brush and seal, locked", act=2, night="hall",
         comp="insert of a fresh sheet of paper on the red-draped desk, a hand in a crimson sleeve finishing a line of blurred brush strokes that cannot be read, a heavy square bronze seal waiting beside the ink stone",
         lines=[("chuzhifu", "追回令，", "沉聲"), ("chuzhifu", "本府簽了。", "落印")],
         motion="The shot opens directly on this close insert from its very first frame; the brush lifts away, the hand takes up the bronze seal and presses it down hard, leaving a square red mark",
         zh="插鏡：紅布長案上一張新紙，緋色袖子的手寫完一行讀不出的毛筆畫（不寫字），旁邊硯台邊一方沉甸甸的銅印；筆一提，手拿起銅印重重蓋下，留下一方紅印"),
    dict(loc="hall", cam="Two-shot, locked", chars=["xuyan", "chuzhifu"], night="hall",
         comp="two-shot before the dais, Xu Yan on screen left bowing to Prefect Chu on screen right, then turning one open hand toward A-ling off screen left",
         lines=[("xuyan", "大人，", "作揖"), ("xuyan", "是我娘子看出來的。", "驕傲")],
         motion="he straightens from the bow and gestures toward her with a proud smile",
         zh="雙人鏡：台前，許硯在左向右邊的褚知府作揖，然後一隻手掌朝畫外左邊的阿令攤開；作完揖站直，笑著朝她一比"),
    dict(loc="hall", cam="Close-up, slow push in", chars=["aling"], night="hall", tag="鉤子6",
         comp="close-up of A-ling on screen left by the red pillar, her cold face caught off guard, her eyes on Xu Yan off screen right",
         lines=[("xitong", "阿令好感，五十八。", "平板電子音，叮一聲")],
         panel=[("阿令 好感 → 58", "affection")],
         motion="she turns her face a little aside and tucks a loose strand of hair behind her ear",
         zh="阿令特寫在左、紅柱旁，冷冷的臉被這句話打了個措手不及，看著畫外右邊的許硯；把臉微微別開，把一縷頭髮塞到耳後"),
    dict(loc="hall", cam="Two-shot, slow push in", chars=["xuyan", "tangxiaotang"], night="hall",
         comp="two-shot by the main door of the court hall, Tang Xiaotang in her high-collared peach-pink ruqun on screen right just arrived and catching her breath, Xu Yan on screen left turning to her with a warm look",
         lines=[("xuyan", "沒有妳，", "認真"), ("xuyan", "今天就輸了。", "笑")],
         motion="he steps over to her and gives her sleeve a light tug of thanks",
         zh="雙人鏡：大堂門邊，高領桃粉襦裙的唐小棠在右剛趕到、還在喘，許硯在左轉向她，眼神很暖；走過去輕輕扯一下她的袖子道謝"),
    dict(loc="hall", cam="Close-up, locked", chars=["tangxiaotang"], night="hall",
         comp="close-up of Tang Xiaotang on screen right, her high stand-up collar fastened at the throat, her cheeks pink, a delighted dimpled smile spreading, her eyes on Xu Yan off screen left",
         lines=[("xitong", "唐小棠好感，六十一。", "平板電子音，叮一聲")],
         panel=[("唐小棠 好感 → 61", "affection")],
         motion="she presses her lips together to hide the smile and fails, ducking her chin",
         zh="唐小棠特寫在右，高領扣到喉嚨，臉頰泛粉，酒窩笑開，看著畫外左邊的許硯；抿嘴想藏笑卻藏不住，下巴一縮"),
    dict(chapter="北門", loc="hall", cam="Wide shot, locked", chars=["dutie"], tag="結尾",
         comp="wide shot of the court hall from the dais, Du Tie bursting in through the bright main door on screen left on his wooden crutch, runners turning in surprise along the walls",
         lines=[("dutie", "囚車天沒亮，", "喘著吼"), ("dutie", "就出了北門！", "急")],
         motion="he lurches forward on the crutch, nearly falls, and catches himself on a pillar",
         zh="結尾：從高台拍的大堂全景，杜鐵拄著木拐從左邊亮白的大門撞進來，兩排衙役吃驚回頭；他拄拐往前一衝，差點摔倒，一把撐住柱子"),
    dict(loc="hall", cam="Medium close-up, slow push in", chars=["dutie"], night="hall", tag="結尾",
         comp="medium close-up of Du Tie on screen left leaning on the red pillar, sweat on his weathered face, his fierce tiger eyes on Xu Yan off screen right",
         lines=[("dutie", "押車的，", "壓低"), ("dutie", "不是州府的人！", "咬牙")],
         motion="he pushes off the pillar and jabs the crutch toward the north",
         zh="杜鐵中近景在左靠著紅柱，風霜的臉上全是汗，虎目瞪著畫外右邊的許硯；從柱子上撐起來，把木拐往北邊一指"),
    dict(loc="hall", cam="Close-up, slow push in", chars=["xuyan"], night="hall", tag="結尾",
         comp="close-up of Xu Yan's face on screen right, the painted screen of sea and sun blurred far behind him, the red announcement paper clenched in his fist at the bottom of the frame, his young face draining of colour, his eyes going wide and then hard, Du Tie speaking off screen left",
         lines=[("dutie", "出了城，", "啞"), ("dutie", "人就沒了。", "一字一字")],
         motion="his jaw locks and his hand crushes the red announcement in his fist",
         zh="最後一格：許硯特寫在右，燭光照著半邊臉，眼睛先睜大、再變硬，杜鐵在畫外左邊說話；下顎咬死，手把紅喜報捏成一團"),
]

HEAD = [
    "- 開頭 10 秒：接第 51 集的最後一格（阿令看著抄本上的朱印「這印，是假的」）：指尖點在朱印斷掉的那一筆（0:00），「真印的『州』字，這一筆，是斷的」（0:00–0:05），唐小棠「阿令，妳怎麼……」（0:05），許硯抬手「不用問。我信她。」（0:07）——直接回答「阿令怎麼一眼看出印是假的？」：她說出看法，許硯不追問（細綱的 hook；她為什麼懂，本集不說）",
    "- 顏值鏡頭：s23 阿令站在燭光前垂眼看印，鳳眼一瞇（細綱的 glamour_shot）；s36 唐小棠藏不住的酒窩笑。是臉與動作，不停在身體",
    "- 爽點：前半 hidden_power（s01–s04 阿令一眼看出斷的那一筆、許硯拿出自己的解元喜報 s18–s19）、中段 public_vindication（s21–s24 兩方印對著燭火一比，差了一筆，衙役們交頭接耳，通判跌坐；s32 知府當堂簽追回令）",
    "- 說話鏡頭：說話的人在畫面上的鏡頭，motion 第一句都是他說這句話、嘴唇下巴隨每個音節動；畫外台詞（s19、s32 插鏡、s38 許硯的臉上杜鐵的話、s34 與 s36 系統）放在插鏡與臉部特寫上，prompt 寫明 off screen",
    "- H3 寫法：同第 51 集（motion 寫軌跡、一鏡一事、沒有 camera 字；光線不變句；插鏡開頭的 `The shot opens directly on this close insert` 句；畫外的人不寫局部身體）",
    "- 光：s01–s12 灰白的晨霧；s13–s25、s29–s38 州府大堂的昏暗加門口亮白的日光、案上一根高燭；s26–s28 知府後宅書房柔和的晨光",
    "- 軸線：客棧門口阿令在左、許硯與唐小棠在右，杜鐵從左邊來；大堂大門在左、高台與通判在右，許硯阿令從左邊進來站在台下，知府從左邊的大門進來；書房唐小棠在左、知府夫人在右",
]
FOOT = [
    "- 場景參考：s01–s12 用 `dh-set-zhou-jie-t1`（含 `long street of Qingzhou`，**要畫**）；s13–s25、s29–s38 用 `dh-set-zhoufu-tang-t1`（含 `court hall of the Qingzhou prefecture`，**要畫**）；s26–s28 用 `dh-set-zhoufu-houtang-t1`（含 `prefect's residence`，**要畫**）。",
    "- 道具：公文抄本（s01–s06 在阿令手上，s14 起在許硯手上）；解元喜報（大紅紙、金色筆畫、朱印，s18–s21，最後 s38 被許硯捏成一團）；案上的高燭（s13 起一直點著）；驚堂木（s13、s16）；追回令與銅印（s32）；杜鐵的舊木拐。",
    "- 連戲：細綱的地點寫「州城客棧」，本集開場在客棧門口接第 51 集（長街的場景圖），沒有進客棧裡面。細綱說「知府不在府裡」：知府夫人在後宅（同一座州府），她派人請知府回府，知府直接到大堂。秦霜本集不出場（關在州牢），囚車天沒亮就出了北門——押車的是魏家雇的人（細綱 state），本集只由杜鐵說「不是州府的人」，第 53 集才看到鄧押司。好感：阿令 58（s34，因為他當著知府說「是我娘子看出來的」）、唐小棠 61（s36，因為「沒有妳，今天就輸了」），面板只寫到達的數字，不寫增減（前幾集的數字由別的撰稿人決定）。第 53 集從阿令在大堂外勒馬一個迴旋、把許硯拉上馬背接。",
    "- 秒數：`gen-dh.mjs` 自動決定；系統面板鏡（s34、s36）只有一句，約 2.7 秒。",
    "- 系統面板不由模型畫：s34、s36 的好感度在剪接時疊上（affection）。",
    "- 新的參照圖還沒畫：杜鐵、褚知府的定妝照（`refs-dh/dutie-portrait-t1.png`、`chuzhifu-portrait-t1.png`），場景 `set-zhou-jie-t1.png`、`set-zhoufu-tang-t1.png`、`set-zhoufu-houtang-t1.png`；通判、知府夫人是小角色，沒有定妝照（外貌只寫在 video.json）。三張場景圖都缺，所以本集每一鏡都要等圖。",
]

BRIEF = """
# 《種田娶妻打天下》第 52 集〈真印假印〉

## 故事前提

第 51 集收在州城客棧門口的晨霧裡：阿令接過唐小棠用唐家的錢買來的逮捕公文抄本，只看了一眼上面的朱印：「這印，是假的。」第 52 集從同一張紙接下去：她的指尖點在朱印裡斷掉的那一道紅線上：「真印的『州』字，」「這一筆，」「是斷的。」唐小棠睜大眼：「阿令，妳怎麼……」許硯抬手攔住她：「不用問。」「我信她。」（細綱的 hook：許硯沒問她怎麼知道。）阿令像要說什麼，又垂下眼把抄本對摺。許硯：「要證明是假的，」「得有一張真的比。」唐小棠發愁：「真的州府公文，」「上哪找？」（細綱的衝突。）

秦家軍老兵杜鐵拄著木拐從霧裡趕來：「秦將軍的閨女，」「真關進州牢了？」「誰敢動她，」「老子這條腿跟他拚！」許硯按住他的肩：「杜叔，」「替我盯著州牢。」唐小棠提起裙擺：「知府夫人那邊，」「我去說。」許硯與阿令並肩往州府走：「當面比。」

州府大堂，坐堂的通判頭也不抬：「知府大人不在，」「有事跟本官說。」許硯作揖舉起抄本：「這張逮捕公文，」「印是假的。」通判拍案：「州府大印，」「本官親眼看著蓋的！」阿令往前一步：「那你看錯了。」通判翻臉，驚堂木砸下：「放肆！」「給我趕出去！」（細綱的 mid_hook，0:50 左右）兩個衙役橫著水火棍逼過來，許硯把阿令擋在後面——然後從懷裡抽出一張紅紙：「慢著。」「這張呢？」「州府發的解元喜報。」通判愣住：「這……」許硯把兩張紙疊在一起舉到案上的高燭前：「兩方印，」「對著燈看。」燭光透過來，兩方紅印重合，只有一筆錯開，像一道裂縫（細綱的 turn 與奇觀）。阿令站在燭光前垂眼看印（細綱的顏值鏡頭）：「差了一筆。」衙役們交頭接耳，通判跌坐回椅子，還在嘴硬：「一筆之差，」「算得了什麼？」

知府後宅，唐小棠向知府夫人行禮：「夫人，」「有人借州府的印抓人。」「出了事，」「背鍋的是知府大人。」夫人放下茶碗：「來人，」「請老爺回府。」褚知府大步走進大堂：「本府的印，」「本府自己認。」他把兩張紙舉在燭前看完，轉頭盯著通判：「這張公文，」「誰送來的？」通判腰彎到底：「下、下官……」「不知。」知府落筆蓋印：「追回令，」「本府簽了。」許硯作揖：「大人，」「是我娘子看出來的。」系統：阿令好感五十八。唐小棠剛趕到，他扯一下她的袖子：「沒有妳，」「今天就輸了。」系統：唐小棠好感六十一。話剛落，杜鐵拄著拐撞進大堂：「囚車天沒亮，」「就出了北門！」「押車的，」「不是州府的人！」許硯的臉一下子變硬，杜鐵在畫外說：「出了城，」「人就沒了。」（細綱的 cliffhanger，danger，「追得上那輛囚車嗎？」）

本集細綱：`season-01.json` 第 52 集（110 秒，第一季第六章第二集，調性權謀＋甜寵，lead_arc suffers）。hook（line）s01–s05；mid_hook s16–s17；衝突 s06–s07（要一份確定是真的州府公文、通判是魏家的人：他咬定是真的、問他是誰送來的就說不知）；turn s18–s24（解元喜報、兩方印對燈）與 s26–s32（唐小棠說動知府夫人、知府簽追回令）；cliffhanger s37–s39。satisfaction：hidden_power（s01–s04、s18–s19）、public_vindication（s21–s24、s29–s32）。general_payoffs 全部入鏡：公文偽造坐實、知府簽下追回令（s32）；阿令好感 58（s33–s34）；唐小棠好感 61（s35–s36）。

## 鉤子（站主 10-16：開場、結尾之外中段還要兩三個以上）

| 鉤子 | 鏡 | 內容 |
| --- | --- | --- |
| 【鉤子1】開場 | s01–s07 | 「真印的『州』字，這一筆是斷的」「不用問，我信她」；「真的州府公文，上哪找？」 |
| 【鉤子2】 | s08–s12 | 杜鐵趕到「誰敢動她，老子這條腿跟他拚」；唐小棠去求知府夫人 |
| 【鉤子3】 | s13–s15 | 知府不在，通判坐堂「本官親眼看著蓋的」 |
| 【鉤子4】中段鉤子 | s16–s17 | 通判翻臉「放肆！給我趕出去！」，衙役逼過來 |
| 轉折 | s18–s20 | 「這張呢？」「州府發的解元喜報」 |
| 【鉤子5】 | s21–s25 | 兩方印對著燭火，差了一筆；通判還嘴硬 |
| 【鉤子6】 | s29–s36 | 知府「本府的印，本府自己認」、簽追回令；兩個好感度 |
| 【結尾】 | s37–s39 | 杜鐵撞進來：「囚車天沒亮就出了北門」「押車的不是州府的人」「出了城，人就沒了」 |

## 角色

- 許硯（xuyan）：s04「不用問。我信她。」；s06「要證明是假的，得有一張真的比」；s10「杜叔，替我盯著州牢」；s12「我們去州府，當面比」；s14 作揖「印是假的」；s17 把阿令擋在後面；s18–s19 拿出解元喜報；s21「兩方印，對著燈看」；s33「是我娘子看出來的」；s35「沒有妳，今天就輸了」；s39 聽到「人就沒了」。
- 阿令（aling）：s01–s02 指出斷的一筆；s05 沒想到他不問；s15「那你看錯了」；s23 顏值鏡頭「差了一筆」；s34 被許硯當眾稱「我娘子」，好感 58。她為什麼看得懂州府的印，本集不說。
- 唐小棠（tangxiaotang）：s03 想問、被攔；s07「真的州府公文，上哪找？」；s11「知府夫人那邊，我去說」；s26–s27 說動知府夫人（她自己贏的一場）；s35–s36 好感 61。每一個 prompt 都寫 high stand-up collar。
- 杜鐵（dutie）：s08–s09 趕來「誰敢動她，老子這條腿跟他拚」；s37–s39 撞進大堂報信。外貌照 cast.json，每鏡寫木拐。
- 褚知府（chuzhifu）：s29「本府的印，本府自己認」；s30「這張公文，誰送來的？」；s32 簽追回令。
- 通判（tongpan，小角色，聲音 Charon）：s13「知府大人不在，有事跟本官說」；s15「本官親眼看著蓋的」；s16「放肆！給我趕出去」；s20「這……」；s25「一筆之差，算得了什麼？」；s31「下、下官……不知」。他是魏家的人（細綱 conflict），本集只讓觀眾看他心虛，不點破。
- 知府夫人（zhifufuren，小角色，聲音 Kore）：s28「來人，請老爺回府」。高領深紫襖。
- 系統（xitong）：s34、s36 兩個好感度（`overlays.json`）。

## 地點（固定的地點字）

- 州城長街、客棧門口（清晨晨霧）：同第 51 集，`On the long street of Qingzhou at dawn in thick morning mist`（`dh-set-zhou-jie-t1`）。
- 州府大堂（早上）：`In the court hall of the Qingzhou prefecture in the morning`（`dh-set-zhoufu-tang-t1`）：紅柱、高台、紅布長案、驚堂木、籤筒、海日屏風、兩排水火棍、門口亮白的日光；本集在案上加一根點著的高燭。
- 知府後宅書房（早上）：`In the prefect's residence in the Qingzhou prefecture in the morning`（`dh-set-zhoufu-houtang-t1`）。

## 站主觀點

站主 2026-10-16 的要求：女生要火辣漂亮，濃顏系的五官與妝、合身剪裁；不露、不濕身、鏡頭不停在身體部位；每集至少一個顏值鏡頭；結尾收在最高點；不被黃標；每集開場、結尾之外中段再兩三個以上鉤子。本集的顏值鏡頭是 s23（阿令在燭光前垂眼看印）與 s36（唐小棠藏不住的笑）。沒有任何人打到人：衙役只是橫著棍子逼過來（s17）。印、喜報、公文、追回令都不由模型寫字：prompt 寫「粗線條盤曲的朱紅印」「讀不出的筆畫」，「州」字由阿令說出來；奇觀 s22 只拍兩方紅印透光重合、一道彎線錯開。系統面板不由模型畫。

分鏡照 `storyboard-rules.md` 2026-10-28 起的 H3 寫法（同第 51 集）；秒數由 `gen-dh.mjs` 決定；本集沒有靜圖、沒有切素材鏡。角色外觀照 `production/cast.json` 逐字照抄。
"""

_drop = {5, 10, 19, 30}  # 0-based: s07 上哪找, s12 我們去州府, s21 這……, s32 下官不知
SHOTS = [x for i, x in enumerate(SHOTS) if i not in {6, 11, 20, 31}]

HEAD = [
    "- 開頭 10 秒：接第 51 集的最後一格（阿令看著抄本上的朱印「這印，是假的」）：指尖點在朱印斷掉的那一筆（0:00），「真印的『州』字，這一筆，是斷的」（0:00–0:04），唐小棠「阿令，妳怎麼……」（0:04），許硯抬手「不用問。我信她。」（0:07）——直接回答「阿令怎麼一眼看出印是假的？」：她說出看法，許硯不追問（細綱的 hook；她為什麼懂，本集不說）",
    "- 鉤子（站主 10-16 規則）：【鉤子1】s01–s06 0:00、【鉤子2】s07–s10 0:16、【鉤子3】s11–s14 0:30、【鉤子4 中段】s15–s16 0:45、轉折 s17–s18 0:50、【鉤子5】s19–s23 0:55、【鉤子6】s27–s33 1:20、【結尾】s34–s36 1:42–1:52；相鄰兩個鉤子最多隔 25 秒（1:09–1:20 是唐小棠說動知府夫人，本身就是細綱的 turn）",
    "- 顏值鏡頭：s21 阿令站在燭光前垂眼看印，鳳眼一瞇（細綱的 glamour_shot）；s33 唐小棠藏不住的酒窩笑。是臉與動作，不停在身體",
    "- 爽點：前半 hidden_power（s01–s04 阿令一眼看出斷的那一筆；s17–s18 許硯拿出自己的解元喜報）、中段 public_vindication（s19–s22 兩方印對著燭火一比，差了一筆，衙役們交頭接耳，通判跌坐；s27–s29 知府當堂簽追回令）",
    "- 說話鏡頭：說話的人在畫面上的鏡頭，motion 第一句都是他說這句話、嘴唇下巴隨每個音節動；畫外台詞（s01、s18、s29 插鏡；s36 許硯的臉上杜鐵的話；s31、s33 系統）放在插鏡與臉部特寫上，prompt 寫明 off screen",
    "- H3 寫法：同第 51 集（motion 寫軌跡、一鏡一事、沒有 camera 字；光線不變句；插鏡開頭的 `The shot opens directly on this close insert` 句；畫外的人不寫局部身體）",
    "- 檢查：lint 0 錯誤（只剩 sources 那一條警告）、30 項結構檢查全過、分鏡讀取 0 陷阱、gen-dh 36 個鏡都有 dh-set 場景參照（長街 10、州府大堂 23、後宅 3）",
    "- 光：s01–s10 灰白的晨霧；s11–s23、s27–s36 州府大堂的昏暗加門口亮白的日光、案上一根高燭；s24–s26 知府後宅書房柔和的晨光",
    "- 軸線：客棧門口阿令在左、許硯與唐小棠在右，杜鐵從左邊來；大堂大門在左、高台與通判在右，許硯阿令從左邊進來站在台下，知府從左邊的大門進來；書房唐小棠在左、知府夫人在右",
]
FOOT = [
    "- 場景參考：s01–s10 用 `dh-set-zhou-jie-t1`（含 `long street of Qingzhou`，**要畫**）；s11–s23、s27–s36 用 `dh-set-zhoufu-tang-t1`（含 `court hall of the Qingzhou prefecture`，**要畫**）；s24–s26 用 `dh-set-zhoufu-houtang-t1`（含 `prefect's residence`，**要畫**）。",
    "- 道具：公文抄本（s01–s05 在阿令手上，s12 起在許硯手上）；解元喜報（大紅紙、金色筆畫、朱印，s17–s20，最後 s36 被許硯捏在拳裡）；案上的高燭（s11 起一直點著）；驚堂木（s11、s15）；追回令與銅印（s29）；杜鐵的舊木拐。",
    "- 連戲：細綱的地點寫「州城客棧」，本集開場在客棧門口接第 51 集（長街的場景圖），沒有進客棧裡面。細綱說「知府不在府裡」：知府夫人在後宅（同一座州府），她派人請知府回府，知府直接到大堂。秦霜本集不出場（關在州牢），囚車天沒亮就出了北門——押車的是魏家雇的人（細綱 state），本集只由杜鐵說「不是州府的人」，第 53 集才看到鄧押司。通判是魏家的人（細綱 conflict）：本集只演他咬定、翻臉、心虛，知府問「誰送來的？」他沒有回答，不點破。好感：阿令 58（s31，因為他當著知府說「是我娘子看出來的」）、唐小棠 61（s33，因為「沒有妳，今天就輸了」），面板只寫到達的數字，不寫增減（前幾集的數字由別的撰稿人決定）。第 53 集從阿令勒馬一個迴旋、把許硯拉上馬背接。",
    "- 秒數：`gen-dh.mjs` 自動決定；系統面板鏡（s31、s33）只有一句，約 2.8 秒。",
    "- 系統面板不由模型畫：s31、s33 的好感度在剪接時疊上（affection）。",
    "- 新的參照圖還沒畫：杜鐵、褚知府的定妝照（`refs-dh/dutie-portrait-t1.png`、`chuzhifu-portrait-t1.png`），場景 `set-zhou-jie-t1.png`、`set-zhoufu-tang-t1.png`、`set-zhoufu-houtang-t1.png`；通判、知府夫人是小角色，沒有定妝照（外貌只寫在 video.json）。三張場景圖都缺，所以本集每一鏡都要等圖。",
]
import re as _re
BRIEF = BRIEF.replace("唐小棠發愁：「真的州府公文，」「上哪找？」（細綱的衝突。）", "（細綱的衝突。）")
BRIEF = BRIEF.replace("「老子這條腿跟他拚！」", "「老子跟他拚！」").replace("許硯與阿令並肩往州府走：「當面比。」", "")
BRIEF = BRIEF.replace("通判愣住：「這……」許硯", "通判臉色一白。許硯")
BRIEF = BRIEF.replace("通判腰彎到底：「下、下官……」「不知。」知府", "通判腰彎到底、答不出來。知府")
BRIEF = BRIEF.replace("hook（line）s01–s05；mid_hook s16–s17；衝突 s06–s07（要一份確定是真的州府公文、通判是魏家的人：他咬定是真的、問他是誰送來的就說不知）；turn s18–s24（解元喜報、兩方印對燈）與 s26–s32（唐小棠說動知府夫人、知府簽追回令）；cliffhanger s37–s39。satisfaction：hidden_power（s01–s04、s18–s19）、public_vindication（s21–s24、s29–s32）。general_payoffs 全部入鏡：公文偽造坐實、知府簽下追回令（s32）；阿令好感 58（s33–s34）；唐小棠好感 61（s35–s36）。",
 "hook（line）s01–s05；mid_hook s15–s16（0:45–0:50）；衝突 s06（要一份確定是真的州府公文）與 s11–s15、s23、s28（通判是魏家的人：咬定是真的、翻臉、被問誰送來的答不出）；turn s17–s22（解元喜報、兩方印對燈）與 s24–s29（唐小棠說動知府夫人、知府簽追回令）；cliffhanger s34–s36。satisfaction：hidden_power（s01–s04、s17–s18）、public_vindication（s19–s22、s27–s29）。general_payoffs 全部入鏡：公文偽造坐實、知府簽下追回令（s29）；阿令好感 58（s30–s31）；唐小棠好感 61（s32–s33）。")
BRIEF = BRIEF.replace("""| 【鉤子1】開場 | s01–s07 | 「真印的『州』字，這一筆是斷的」「不用問，我信她」；「真的州府公文，上哪找？」 |
| 【鉤子2】 | s08–s12 | 杜鐵趕到「誰敢動她，老子這條腿跟他拚」；唐小棠去求知府夫人 |
| 【鉤子3】 | s13–s15 | 知府不在，通判坐堂「本官親眼看著蓋的」 |
| 【鉤子4】中段鉤子 | s16–s17 | 通判翻臉「放肆！給我趕出去！」，衙役逼過來 |
| 轉折 | s18–s20 | 「這張呢？」「州府發的解元喜報」 |
| 【鉤子5】 | s21–s25 | 兩方印對著燭火，差了一筆；通判還嘴硬 |
| 【鉤子6】 | s29–s36 | 知府「本府的印，本府自己認」、簽追回令；兩個好感度 |
| 【結尾】 | s37–s39 | 杜鐵撞進來：「囚車天沒亮就出了北門」「押車的不是州府的人」「出了城，人就沒了」 |""",
"""| 【鉤子1】開場 | s01–s06 | 「真印的『州』字，這一筆是斷的」「不用問，我信她」；「得有一張真的比」 |
| 【鉤子2】 | s07–s10 | 杜鐵趕到「誰敢動她，老子跟他拚」；唐小棠去求知府夫人 |
| 【鉤子3】 | s11–s14 | 知府不在，通判坐堂「本官親眼看著蓋的」「那你看錯了」 |
| 【鉤子4】中段鉤子 | s15–s16 | 通判翻臉「放肆！給我趕出去！」，衙役逼過來 |
| 轉折 | s17–s18 | 「這張呢？」「州府發的解元喜報」 |
| 【鉤子5】 | s19–s23 | 兩方印對著燭火，差了一筆；通判還嘴硬 |
| 【鉤子6】 | s27–s33 | 知府「本府的印，本府自己認」、簽追回令；兩個好感度 |
| 【結尾】 | s34–s36 | 杜鐵撞進來：「囚車天沒亮就出了北門」「押車的不是州府的人」「出了城，人就沒了」 |""")
BRIEF = BRIEF.replace("s04「不用問。我信她。」；s06「要證明是假的，得有一張真的比」；s10「杜叔，替我盯著州牢」；s12「我們去州府，當面比」；s14 作揖「印是假的」；s17 把阿令擋在後面；s18–s19 拿出解元喜報；s21「兩方印，對著燈看」；s33「是我娘子看出來的」；s35「沒有妳，今天就輸了」；s39 聽到「人就沒了」。",
 "s04「不用問。我信她。」；s06「要證明是假的，得有一張真的比」；s09「杜叔，替我盯著州牢」；s12 作揖「印是假的」；s16 把阿令擋在後面；s17–s18 拿出解元喜報；s19「兩方印，對著燈看」；s30「是我娘子看出來的」；s32「沒有妳，今天就輸了」；s36 聽到「人就沒了」。")
BRIEF = BRIEF.replace("s05 沒想到他不問；s15「那你看錯了」；s23 顏值鏡頭「差了一筆」；s34 被許硯", "s05 沒想到他不問；s14「那你看錯了」；s21 顏值鏡頭「差了一筆」；s31 被許硯")
BRIEF = BRIEF.replace("s03 想問、被攔；s07「真的州府公文，上哪找？」；s11「知府夫人那邊，我去說」；s26–s27 說動知府夫人（她自己贏的一場）；s35–s36 好感 61。", "s03 想問、被攔；s10「知府夫人那邊，我去說」；s24–s25 說動知府夫人（她自己贏的一場）；s32–s33 好感 61。")
BRIEF = BRIEF.replace("s08–s09 趕來「誰敢動她，老子這條腿跟他拚」；s37–s39 撞進大堂報信。", "s07–s08 趕來「誰敢動她，老子跟他拚」；s34–s36 撞進大堂報信。")
BRIEF = BRIEF.replace("s29「本府的印，本府自己認」；s30「這張公文，誰送來的？」；s32 簽追回令。", "s27「本府的印，本府自己認」；s28「這張公文，誰送來的？」；s29 簽追回令。")
BRIEF = BRIEF.replace("s13「知府大人不在，有事跟本官說」；s15「本官親眼看著蓋的」；s16「放肆！給我趕出去」；s20「這……」；s25「一筆之差，算得了什麼？」；s31「下、下官……不知」。", "s11「知府大人不在，有事跟本官說」；s13「本官親眼看著蓋的」；s15「放肆！給我趕出去」；s22 跌坐；s23「一筆之差，算得了什麼？」；s28 被問誰送來的、答不出來。")
BRIEF = BRIEF.replace("s28「來人，請老爺回府」", "s26「來人，請老爺回府」").replace("s34、s36 兩個好感度", "s31、s33 兩個好感度")
BRIEF = BRIEF.replace("本集的顏值鏡頭是 s23（阿令在燭光前垂眼看印）與 s36（唐小棠藏不住的笑）。沒有任何人打到人：衙役只是橫著棍子逼過來（s17）。", "本集的顏值鏡頭是 s21（阿令在燭光前垂眼看印）與 s33（唐小棠藏不住的笑）。沒有任何人打到人：衙役只是橫著棍子逼過來（s16）。").replace("奇觀 s22 只拍", "奇觀 s20 只拍")
BRIEF = BRIEF.replace("（細綱的 mid_hook，0:50 左右）", "（細綱的 mid_hook，0:45）")
