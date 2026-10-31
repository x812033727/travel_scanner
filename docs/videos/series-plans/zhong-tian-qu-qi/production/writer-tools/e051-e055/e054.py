EP = 54
EP_TITLE = "她第一次哭"
OUTLINE_SECONDS = 130
TARGET_MINUTES = [1, 3]
TITLE = "她選了公道不換爹的信，火堆旁將門之女第一次哭了｜種田娶妻打天下 第54集"
DESCRIPTION = "鄧押司拿一封「給妳爹的信」要秦霜放他走。秦霜只說：「信，我自己去拿。」槍桿一掃，鄧押司倒在淺灘，信飛上半空，被阿令伸手接住。許硯拿鄧押司自己腰上的鐵鏈綁住他。信拆開，裡面是一張白紙——秦霜跪在河水裡，終於哭出聲。夜裡河灘一堆篝火，火星飛進滿天星，她第一次把一切說給許硯聽：爹被定罪那天，把貼身的玉佩交給最信任的親兵送出去，那個人再也沒回來，最後一封信說到了青州柳溪；娘等不到消息，鬱鬱而終，就是竹林裡那座無名墳。許硯說：「妳爹的冤，我陪妳洗。」她第一次把頭靠在他肩上。然後她抹掉眼淚，指著他眼前的空氣：「你常對著那裡笑。那裡有什麼？」阿令也轉過頭來，等他回答。《種田娶妻打天下》第 54 集。"
THUMB = ("她哭了", "s38")
CHARACTERS = ["xuyan", "qinshuang", "aling", "dengyasi", "xitong"]
MINOR = {}
MUSIC = "a sharp drum crack as the spear sweeps the escort down, a bright rising string as the letter flies and her hand catches it, a cold clank of chain for the binding, then a fragile held guqin note as the seal breaks and a sudden silence and one low cello falling when the sheet is blank, a slow broken erhu under her crying in the river, then a warm crackling night of soft plucked zither and a breathy xiao over the campfire and the stars, a deep solemn drum for the word treason, a lonely flute for the soldier who never came back, a trembling guqin for the nameless grave, a warm swelling strings theme as he promises to clear her father's name, two soft sweet bells for her affection, a tender hush as her head rests on his shoulder, then a curious glassy shimmer and a held breath as she points at the empty air, cut before his answer, ancient Chinese rural drama, no vocals"

LOC = {
    "ford": "At the shallow ford of the north ferry outside Qingzhou late in the afternoon, a wide slow river running knee-deep over pebble shoals, the broken wooden prison cage standing in the water, a rough log raft tied to a post, reeds and sandbanks, low golden sunlight across the water",
    "fire": "On the pebble riverbank by the north ferry at night, a campfire of driftwood with sparks flying up, flat rocks around it to sit on, the dark river beyond, a sky full of stars",
}
LIGHT = {"ford": "the low golden sunlight stays unchanged", "fire": "the warm firelight and the starry night stay unchanged"}

SHOTS = [
    dict(chapter="自己拿", loc="ford", cam="Close-up, slow push in", chars=["qinshuang"], night="ford", tag="鉤子1／開頭",
         comp="close-up of Qin Shuang in the knee-deep river, her bold brows level, her almond eyes hard and clear on Sergeant Deng off screen right, the spear shaft across her body",
         lines=[("qinshuang", "信，", "很冷"), ("qinshuang", "我自己去拿。", "一字一字")],
         motion="she shifts her weight onto her front foot and draws the spear back for a swing",
         zh="接第 53 集：秦霜特寫在齊膝的河水裡，劍眉放平，杏眼又硬又清地看著畫外右邊的鄧押司，槍桿橫在身前；重心移到前腳，把槍往後一收準備掄"),
    dict(loc="ford", cam="Wide shot, locked", chars=["qinshuang", "dengyasi"], act=2, night="ford", tag="鉤子1",
         comp="wide shot by the log raft, Qin Shuang on screen left charging through the shallows, Sergeant Deng on screen right with the old letter raised in one hand",
         motion="she sweeps the spear shaft low across his shins and his legs fly out from under him, he crashes onto his back in the water and the letter flies out of his hand",
         zh="木筏邊全景：秦霜在左踩著水衝過去，鄧押司在右一手高舉那封舊信；她槍桿貼著水面掃過他的小腿，他兩腳一飛仰面摔進水裡，信從手裡飛出去"),
    dict(loc="ford", cam="Insert of the letter in the air, locked", act=1, night="ford", tag="鉤子1",
         comp="insert of the worn folded letter with its dark wax seal tumbling through the golden air above the glittering river",
         motion="The shot opens directly on this close insert from its very first frame; the letter turns over twice in the air and a slender hand in a grey-white sleeve snaps it out of the air",
         zh="插鏡：那封摺舊、封著深色蠟的信在金色的空中翻滾，下面河面閃光；信在空中翻兩圈，一隻月白袖子的纖手一把接住"),
    dict(loc="ford", cam="Medium close-up, locked", chars=["aling"], night="ford",
         comp="medium close-up of A-ling on the bay horse in the shallows, the old letter caught between two fingers of her raised hand, her face cool",
         lines=[("aling", "拿到了。", "淡淡的")],
         motion="she lowers the letter and tucks it into her sleeve for safekeeping",
         zh="阿令中近景，騎在淺水裡的棗紅馬上，舉起的手兩根手指夾著那封信，臉很冷靜；放下信，收進袖裡"),
    dict(loc="ford", cam="Medium shot, slow push in", chars=["qinshuang", "dengyasi"], night="ford",
         comp="medium shot in the shallows, Sergeant Deng sitting in the water on screen right with river water dripping from his beard and his hands raised, Qin Shuang standing over him on screen left with the spear point held a hand's width from his chest",
         lines=[("dengyasi", "饒、饒命……", "嚇破膽")],
         motion="he scrabbles backward through the water on his elbows while the spear point follows him",
         zh="淺水中景：鄧押司在右坐在水裡、兩手舉起，秦霜在左站在他面前，槍尖離他胸口一個手掌；他用手肘在水裡往後爬，槍尖跟著他"),
    dict(loc="ford", cam="Close-up, locked", chars=["qinshuang"], night="ford",
         comp="close-up of Qin Shuang looking down at Sergeant Deng off screen right, her face cold and proud",
         lines=[("qinshuang", "州府的牢，", "冷"), ("qinshuang", "換你去坐。", "抬下巴")],
         motion="she lifts her chin and flicks the spear point once in warning",
         zh="秦霜特寫，往下看著畫外右邊的鄧押司，臉又冷又傲；下巴一抬，槍尖警告地一點"),
    dict(loc="ford", cam="Insert of the chain at his wrists, locked", act=2, night="ford", tag="鉤子2",
         comp="insert of two thick hairy wrists held together above the water, a young man's hands in faded blue-grey sleeves winding a dull iron chain around them",
         lines=[("xuyan", "這條鏈子，", "笑，冷"), ("xuyan", "還你。", "拉緊")],
         motion="The shot opens directly on this close insert from its very first frame; the chain is wrapped twice and pulled snug with one hard jerk",
         zh="插鏡：兩隻粗毛的手腕併在水面上，一雙青灰袖子的手把一條鐵鏈繞上去（第 51 集鎖秦霜的同一種鏈）；繞兩圈，用力一拉扣緊"),
    dict(loc="ford", cam="Medium close-up, locked", chars=["dengyasi"], night="ford",
         comp="medium close-up of Sergeant Deng on screen right sitting in the water with his wrists chained, his bristling beard dripping, his gloomy eyes on Xu Yan off screen left",
         lines=[("dengyasi", "你們惹的人，", "陰沉"), ("dengyasi", "惹不起。", "冷笑")],
         motion="he spits into the river and turns his face away",
         zh="鄧押司中近景在右，手腕被鏈子綁著坐在水裡，絡腮鬍滴著水，陰沉的眼睛看著畫外左邊的許硯；往河裡吐一口，把臉別開"),
    dict(chapter="白紙", loc="ford", cam="Two-shot, locked", chars=["aling", "qinshuang"], night="ford",
         comp="two-shot in the shallows, A-ling on the horse on screen left holding the old letter down toward Qin Shuang, Qin Shuang on screen right reaching up for it with both hands",
         lines=[("aling", "妳的。", "很輕")],
         motion="Qin Shuang takes the letter carefully in both hands as if it might break",
         zh="雙人鏡：淺水裡，阿令在左騎在馬上把那封信往下遞給秦霜，秦霜在右雙手伸上去接；秦霜小心翼翼地用兩手接過來，好像一碰就會碎"),
    dict(loc="ford", cam="Insert of the wax seal, locked", act=2, night="ford",
         comp="insert of the worn letter held in two hands in fitted dark brown sleeves, a thumb pressing on the dark wax seal, the fingers trembling",
         motion="The shot opens directly on this close insert from its very first frame; the thumb presses harder, the wax seal cracks, and the trembling fingers begin to unfold the paper",
         zh="插鏡：一雙深棕袖子的手拿著那封舊信，拇指按在深色封蠟上，手指在抖；拇指再一壓，封蠟裂開，發抖的手指開始把紙攤開"),
    dict(loc="ford", cam="Close-up, slow push in", chars=["qinshuang"], night="ford",
         comp="close-up of Qin Shuang's face in the golden light, her eyes shining with hope, her lips parted, looking down at the letter below the frame",
         lines=[("qinshuang", "爹……", "很輕，發抖")],
         motion="she draws one shaky breath and unfolds the last fold",
         zh="秦霜特寫，金色的光裡，眼睛裡全是期待，嘴唇張開，低頭看著畫面下方的信；她顫抖地吸一口氣，打開最後一摺"),
    dict(loc="ford", cam="Insert of the blank sheet, slow push in", act=2, night="ford", tag="鉤子3／中段鉤子",
         comp="insert of the unfolded letter held open in two hands with fitted dark brown sleeves: a completely blank white sheet with nothing on it at all, golden light on the empty paper",
         motion="The shot opens directly on this close insert from its very first frame; the hands turn the blank sheet over and the other side is just as empty",
         zh="中段鉤子：插鏡，一雙深棕袖子的手攤開那封信——一張什麼都沒有的白紙，金色的光照在空白的紙上；手把紙翻過來，背面也一樣是空的"),
    dict(loc="ford", cam="Close-up, locked", chars=["qinshuang"], night="ford", tag="鉤子3",
         comp="close-up of Qin Shuang's face, the hope draining out of it, her eyes fixed on the blank paper below the frame",
         lines=[("xuyan", "白紙？", "愣住")],
         motion="her lips tremble and her eyes slowly fill as she keeps staring at the paper",
         zh="秦霜特寫，臉上的期待一點一點流光，眼睛釘在畫面下方的白紙上；嘴唇發抖，眼睛慢慢紅起來"),
    dict(loc="ford", cam="Medium close-up, locked", chars=["dengyasi"], night="ford",
         comp="medium close-up of Sergeant Deng chained and sitting in the shallows on screen right, a nasty grin through his wet beard, his eyes on Qin Shuang off screen left",
         lines=[("dengyasi", "哪有什麼信，", "大笑"), ("dengyasi", "騙妳的。", "得意")],
         motion="he throws his head back and laughs, his chained wrists rattling",
         zh="鄧押司中近景在右，被鏈子綁著坐在淺水裡，濕鬍子裡一個難看的笑，看著畫外左邊的秦霜；仰頭大笑，綁著的手腕把鏈子搖得響"),
    dict(loc="ford", cam="Wide shot, slow push in", chars=["qinshuang"], act=3, night="ford",
         comp="wide shot of the golden ford, the broken cage behind, Qin Shuang alone in the middle of the knee-deep river holding the blank sheet, the spear floating against her legs",
         motion="her knees give way and she sinks down into the shallow water, the blank paper pressed against her chest with both hands",
         zh="金色渡口的全景，破籠在後面，秦霜一個人站在齊膝的河水中間拿著白紙，長槍漂在她腳邊；她膝蓋一軟，跪進淺水裡，雙手把白紙按在胸前"),
    dict(loc="ford", cam="Close-up, slow push in", chars=["qinshuang"], night="ford", tag="鉤子3",
         comp="close-up of Qin Shuang kneeling in the river, her proud face crumpling, tears running down her cheeks, her eyes squeezed shut",
         lines=[("qinshuang", "我以為……", "哭出聲"), ("qinshuang", "我以為找到他了……", "哽咽")],
         motion="she bows her head over the paper and her shoulders shake with sobs",
         zh="秦霜特寫，跪在河裡，倔強的臉垮下來，眼淚流下臉頰，眼睛緊閉；她低頭伏在白紙上，肩膀抽動著哭出聲（第一次在他面前哭）"),
    dict(loc="ford", cam="Two-shot, locked", chars=["xuyan", "qinshuang"], night="ford",
         comp="two-shot in the shallows, Xu Yan on screen left kneeling down in the water in front of Qin Shuang on screen right, one hand reaching to her shoulder",
         lines=[("xuyan", "我在。", "很輕")],
         motion="he rests his hand on her shoulder and stays there, steady, while she cries",
         zh="雙人鏡：淺水裡，許硯在左在秦霜面前跪進水裡，一隻手伸向她的肩，秦霜在右；他把手放在她肩上，穩穩地不動，讓她哭"),
    dict(loc="ford", cam="Medium shot, locked", chars=["aling", "dengyasi"], act=2, night="ford",
         comp="medium shot by the raft, A-ling on screen left gathering up the end of Sergeant Deng's chain, Deng sitting in the water on screen right",
         motion="she yanks the chain so he stumbles to his feet and leads him away toward the bank, turning her back to the two kneeling in the river",
         zh="木筏邊中景：阿令在左撿起鄧押司鐵鏈的一端，鄧押司在右坐在水裡；她一扯鏈子讓他站起來，牽著他往岸上走，背對著跪在河裡的兩個人（讓他們獨處）"),
    dict(chapter="火堆", loc="fire", cam="Wide shot, slow push in", chars=["xuyan", "qinshuang", "aling"], act=3, night="fire", tag="鉤子4",
         comp="wide shot of the riverbank at night, a campfire with sparks flying up into a sky full of stars, three figures seated on flat rocks around it, and further down the bank Sergeant Deng and his thugs tied in a row against a log",
         motion="a log shifts in the fire and a fountain of sparks rises and drifts up into the stars while the three sit quietly",
         zh="奇觀：夜裡的河灘全景，一堆篝火，火星往上飛進滿天星，三個人坐在火邊的平石上，河灘更遠處鄧押司和他的打手被綁成一排靠著一根木頭；一根柴塌下來，一大團火星往上飄進星空"),
    dict(loc="fire", cam="Medium close-up, locked", chars=["xuyan"], night="fire",
         comp="medium close-up of Xu Yan on screen right feeding a stick of driftwood into the fire, his face calm in the firelight, his eyes on the tied men off screen left",
         lines=[("xuyan", "那一串，", "淡淡的"), ("xuyan", "明早押回州府。", "很穩")],
         motion="he pushes the stick into the flames and brushes the ash off his hands",
         zh="許硯中近景在右，把一根漂流木推進火裡，火光裡臉很平靜，看著畫外左邊被綁的那串人；把柴推進火，拍掉手上的灰（細綱：鄧押司被押回州府）"),
    dict(loc="fire", cam="Medium shot, locked", chars=["qinshuang"], night="fire",
         comp="medium shot of Qin Shuang sitting on a flat rock on screen left hugging her knees, her high ponytail still damp, her eyes on the fire",
         lines=[("qinshuang", "我爹被定罪那天，", "很低，望著火")],
         motion="she rests her chin on her knees and draws them in tighter",
         zh="秦霜中景在左，坐在平石上抱著膝，高馬尾還有點潮，眼睛看著火；下巴擱上膝蓋，把腿抱得更緊"),
    dict(loc="fire", cam="Close-up, slow push in", chars=["qinshuang"], night="fire", tag="鉤子4",
         comp="close-up of Qin Shuang in the firelight, her eyes red from crying, her jaw set, staring into the flames",
         lines=[("qinshuang", "罪名是通敵。", "咬牙"), ("qinshuang", "他守了北疆二十年。", "聲音發顫")],
         motion="her fingers dig into her sleeves and then slowly loosen",
         zh="秦霜特寫，火光裡，哭紅的眼睛，下巴咬緊，盯著火焰；手指掐進袖子，又慢慢鬆開（m03 的 setup：秦家為什麼被定罪）"),
    dict(loc="fire", cam="Insert of the jade pendant in his palm, locked", act=1, night="fire",
         comp="insert of a young man's open palm in a faded blue-grey sleeve held out toward the fire, a small oval white jade pendant the size of a walnut lying on it, firelight glinting on the carved back",
         lines=[("qinshuang", "這塊玉，", "很輕"), ("qinshuang", "他從不離身。", "哽咽")],
         motion="The shot opens directly on this close insert from its very first frame; the thumb turns the jade over once and the firelight runs across it",
         zh="插鏡：一隻青灰袖子的手掌攤開伸向火邊，掌心一塊核桃大的橢圓白玉佩，火光在刻過的背面閃；拇指把玉翻過來，火光流過玉面（字不畫出來）"),
    dict(loc="fire", cam="Medium close-up, locked", chars=["qinshuang"], night="fire",
         comp="medium close-up of Qin Shuang on screen left looking at the jade off screen right, the firelight on her wet lashes",
         lines=[("qinshuang", "他交給最信任的親兵，", "慢慢說"), ("qinshuang", "送出去。", "很輕")],
         motion="she reaches out one finger as if to touch the jade, and stops just short of it",
         zh="秦霜中近景在左，看著畫外右邊那塊玉，火光照著她濕的睫毛；伸出一根手指像要碰那塊玉，在差一點的地方停住"),
    dict(loc="fire", cam="Close-up, locked", chars=["qinshuang"], night="fire",
         comp="close-up of Qin Shuang, her hand drawing back to her knees, her eyes on the fire again",
         lines=[("qinshuang", "那個人，", "低"), ("qinshuang", "再也沒回來。", "幾乎聽不見")],
         motion="she pulls her hand back and wraps both arms around her knees",
         zh="秦霜特寫，手收回膝上，眼睛又看回火；把手抽回來，兩手環住膝蓋"),
    dict(chapter="柳溪", loc="fire", cam="Medium close-up, slow push in", chars=["xuyan"], night="fire", tag="鉤子5",
         comp="medium close-up of Xu Yan on screen right, the jade pendant in his closed hand at his chest, his brows drawn together, his eyes on Qin Shuang off screen left",
         lines=[("xuyan", "他最後，", "小心地問"), ("xuyan", "去了哪裡？", "低")],
         motion="he leans toward her across the fire",
         zh="許硯中近景在右，握著玉佩的手放在胸前，眉頭皺起，看著畫外左邊的秦霜；隔著火往她那邊傾身"),
    dict(loc="fire", cam="Close-up, locked", chars=["qinshuang"], night="fire", tag="鉤子5",
         comp="close-up of Qin Shuang lifting her eyes from the fire to Xu Yan off screen right",
         lines=[("qinshuang", "最後一封信說，", "很慢"), ("qinshuang", "到了青州柳溪。", "看著他")],
         motion="she lifts her head off her knees and holds his gaze",
         zh="秦霜特寫，眼睛從火上抬起來看畫外右邊的許硯；把頭從膝蓋上抬起來，看著他"),
    dict(loc="fire", cam="Close-up, slow push in", chars=["xuyan"], night="fire", tag="鉤子5",
         comp="close-up of Xu Yan's face in the firelight, his eyes going wide and then dropping to the jade in his opening hand",
         lines=[("xuyan", "所以這塊玉，", "恍然"), ("xuyan", "是在柳溪丟的。", "低聲")],
         motion="he opens his fingers slowly and stares down at the jade in his palm",
         zh="許硯特寫，火光裡，眼睛先睜大，再落到慢慢攤開的手心那塊玉上；手指慢慢張開，盯著掌心的玉（m11：玉佩的來路，送玉的親兵在柳溪附近失蹤）"),
    dict(loc="fire", cam="Wide shot, locked", chars=["aling", "xuyan", "qinshuang"], act=2, night="fire",
         comp="wide shot of the campfire from beside the river, Qin Shuang and Xu Yan on the flat rocks on screen left, A-ling sitting across the fire on screen right with her face still and pale in the firelight, listening",
         motion="she picks up a dry branch and lays it carefully on the fire, her eyes never leaving Qin Shuang",
         zh="阿令中景在右，坐在火堆另一邊的平石上，火光裡臉很靜、很白，在聽；撿起一根乾枝小心放進火裡，眼睛一直看著秦霜"),
    dict(loc="fire", cam="Medium close-up, locked", chars=["qinshuang"], night="fire",
         comp="medium close-up of Qin Shuang on screen left hugging her knees, her voice breaking, her eyes on the fire",
         lines=[("qinshuang", "娘等不到消息，", "哽咽"), ("qinshuang", "一病就沒起來。", "很輕")],
         motion="she presses her lips together hard to stop them trembling",
         zh="秦霜中近景在左抱著膝，聲音斷掉，眼睛看著火；用力抿住嘴不讓它抖"),
    dict(loc="fire", cam="Close-up, slow push in", chars=["qinshuang"], night="fire", tag="鉤子6",
         comp="close-up of Qin Shuang, a tear sliding down her cheek in the firelight, her eyes on Xu Yan off screen right",
         lines=[("qinshuang", "竹林裡那座墳，", "很慢"), ("qinshuang", "是我娘。", "眼淚掉下來")],
         motion="she wipes the tear away with the back of her wrist and another one follows",
         zh="秦霜特寫，火光裡一滴眼淚滑下臉頰，看著畫外右邊的許硯；用手背抹掉，下一滴又流下來（竹林裡的無名墳）"),
    dict(loc="fire", cam="Insert of the blank sheet in her hands, locked", act=1, night="fire",
         comp="insert of the blank white sheet folded in two hands in fitted dark brown sleeves on her knees, firelight on the paper",
         motion="The shot opens directly on this close insert from its very first frame; a single tear drops onto the blank paper and spreads into a small dark spot",
         zh="插鏡：膝上一雙深棕袖子的手拿著摺起的白紙，火光照在紙上；一滴眼淚落在白紙上，暈開一個小小的深點"),
    dict(chapter="陪妳洗", loc="fire", cam="Two-shot, locked", chars=["qinshuang", "xuyan"], night="fire",
         comp="two-shot by the fire, Qin Shuang on screen left hugging her knees, Xu Yan on screen right moving to sit on the rock beside her, the jade in his hand, his face serious and gentle",
         lines=[("xuyan", "妳爹的冤，", "很穩")],
         motion="he sits down beside her and closes her fingers around the jade",
         zh="許硯中近景在右，移到秦霜旁邊的石頭坐下，手上拿著玉，臉又認真又溫柔；坐到她旁邊，把她的手指合起來握住那塊玉"),
    dict(loc="fire", cam="Close-up, slow push in", chars=["xuyan"], night="fire", tag="鉤子6",
         comp="close-up of Xu Yan's face in the firelight, his eyes steady on Qin Shuang off screen left",
         lines=[("xuyan", "我陪妳洗。", "一字一字")],
         motion="he nods once, slowly, and does not look away",
         zh="許硯特寫，火光裡，眼神穩穩地看著畫外左邊的秦霜；慢慢點一下頭，不移開眼睛"),
    dict(loc="fire", cam="Close-up, locked", chars=["qinshuang"], night="fire",
         comp="close-up of Qin Shuang looking at Xu Yan off screen right, her wet almond eyes wide, the jade held against her chest",
         lines=[("qinshuang", "客棧那晚，", "很輕"), ("qinshuang", "謝謝你按住我。", "第一次這麼軟")],
         motion="her lips curve into a small, shaky smile through the tears",
         zh="秦霜特寫，看著畫外右邊的許硯，濕濕的杏眼睜大，玉佩按在胸前；隔著眼淚，嘴角彎出一個小小的、發抖的笑（他先前選了不流血的路）"),
    dict(loc="fire", cam="Close-up, slow push in", chars=["xuyan"], night="fire",
         comp="close-up of Xu Yan in the firelight, his eyes lifting to a fixed point in the empty air in front of him",
         lines=[("xitong", "秦霜好感，六十六。", "平板電子音，叮一聲")],
         panel=[("秦霜 好感 → 66", "affection")],
         motion="his eyes track across the empty air and the corner of his mouth lifts into a soft smile",
         zh="系統面板：許硯特寫，火光裡，眼睛抬起定在面前的空中；眼睛掃過去，嘴角輕輕往上一提（破 60）"),
    dict(loc="fire", cam="Two-shot, slow push in", chars=["qinshuang", "xuyan"], act=3, night="fire", tag="顏值鏡頭",
         comp="two-shot by the campfire, Qin Shuang on screen left hugging her knees, the firelight on her tear-reddened almond eyes and her damp high ponytail, Xu Yan sitting beside her on screen right",
         motion="she slowly leans sideways and rests her head on his shoulder, and after a moment he stays very still to let her",
         zh="顏值鏡頭：篝火邊的雙人鏡，秦霜在左抱著膝，火光照著她哭紅的杏眼和還有點潮的高馬尾，許硯坐在她右邊；她慢慢往旁邊靠，把頭靠在他肩上，他一動不動讓她靠"),
    dict(loc="fire", cam="Medium close-up, locked", chars=["aling"], act=2, night="fire",
         comp="medium close-up of A-ling across the fire on screen right, the firelight on her cold beautiful face, her eyes on the two of them off screen left",
         motion="she watches a moment, then lowers her eyes and turns a stick in the embers",
         zh="阿令中近景在右、火堆另一邊，火光照著她清冷的臉，看著畫外左邊的兩個人；看了一會兒，垂下眼，用一根柴撥火裡的炭"),
    dict(chapter="那裡有什麼", loc="fire", cam="Medium shot, locked", chars=["qinshuang"], night="fire", tag="結尾",
         comp="medium shot of Qin Shuang on screen left lifting her head from Xu Yan's shoulder, Xu Yan beside her on screen right",
         lines=[("qinshuang", "許硯。", "抹掉眼淚")],
         motion="she wipes her eyes with the back of her hand and sits up straight",
         zh="結尾：秦霜中景在左，從許硯肩上抬起頭；用手背抹掉眼淚，坐直"),
    dict(loc="fire", cam="Close-up, slow push in", chars=["qinshuang"], night="fire", tag="結尾",
         comp="close-up of Qin Shuang in the firelight, her bold brows lifting with curiosity, one finger raised and pointing at the empty air toward Xu Yan off screen right",
         lines=[("qinshuang", "你常對著那裡笑。", "好奇，很直")],
         motion="she jabs the finger at the empty air twice",
         zh="秦霜特寫，火光裡，劍眉好奇地一揚，一根手指舉起來，指著畫外右邊許硯臉前的空氣；手指往那片空氣戳兩下"),
    dict(loc="fire", cam="Close-up, locked", chars=["qinshuang"], night="fire", tag="結尾",
         comp="close-up of Qin Shuang, her finger still pointing, her head tilting, her eyes on Xu Yan off screen right",
         lines=[("qinshuang", "那裡有什麼？", "追問")],
         motion="she tilts her head and leans in to look closer",
         zh="秦霜特寫，手指還指著，頭一歪，眼睛在畫外右邊他的臉上找答案；頭一歪，湊近一點看"),
    dict(loc="fire", cam="Medium close-up, slow push in", chars=["aling"], act=2, night="fire", tag="結尾",
         comp="medium close-up of A-ling across the fire on screen right, the stick still in her hand, her phoenix eyes lifting to Xu Yan off screen left",
         motion="she stops stirring the embers and slowly turns her head to him, waiting",
         zh="阿令中近景在右、火堆另一邊，手上還拿著那根柴，鳳眼抬起來看畫外左邊的許硯；她停下撥火，慢慢轉過頭來等他回答"),
    dict(loc="fire", cam="Extreme close-up, locked", chars=["xuyan"], act=2, night="fire", tag="結尾",
         comp="extreme close-up of Xu Yan's face in the firelight, caught between the two women's eyes, his lips just parting",
         motion="he draws a slow breath and his lips part to answer",
         zh="最後一格：許硯大特寫，火光裡，被兩個女人的眼睛夾在中間，嘴唇剛要張開；慢慢吸一口氣，嘴唇張開要回答——切"),
]

HEAD = [
    "- 開頭 10 秒：接第 53 集的最後一格（鄧押司「要信，就放我走」、秦霜眉頭擰緊）：秦霜「信，我自己去拿」（0:00），槍桿一掃鄧押司摔進淺灘、信飛上半空（0:03），阿令一把接住（0:05）「拿到了」（0:06）——直接回答「秦霜要放走仇人，換爹的信嗎？」：不換，自己拿",
    "- 鉤子（站主 10-16 規則）：見 brief.md 的鉤子表",
    "- 顏值鏡頭：s37 秦霜抱膝坐在火邊、哭紅的杏眼與還有點潮的馬尾、第一次把頭靠在許硯肩上（細綱的 glamour_shot）；是臉與動作，不停在身體",
    "- 爽點：前半 villain_humbled（s02–s08 鄧押司被一槍掃倒、跪地求饒、被自己的鐵鏈綁住）、中段 level_up（s35–s36 秦霜好感破 60 到 66）",
    "- 說話鏡頭：說話的人在畫面上的鏡頭，motion 第一句都是他說這句話；畫外台詞（s07、s23 插鏡上的話，s13 秦霜的臉上許硯的「白紙？」，s36 系統）放在插鏡與臉部特寫上",
    "- H3 寫法：同第 51 集；哭的鏡頭寫眼淚與肩膀，不停在身體；火光不變句；s42 收在嘴唇剛要張開",
    "- 光：s01–s18 渡口午後低低的金色陽光；s19–s42 夜裡河灘的篝火與滿天星",
    "- 軸線：渡口岸在左、木筏在右，秦霜在左、鄧押司在右；篝火邊秦霜在左、許硯在右（坐到她旁邊後還是她左他右），阿令在火堆另一邊的右側，被綁的那串人在畫外左邊遠處",
]
FOOT = [
    "- 場景參考：s01–s18 用 `dh-set-beidu-qiantan-t1`（含 `shallow ford`，**要畫**）；s19–s42 用 `dh-set-hetan-t1`（含 `campfire`，**要畫**）。",
    "- 道具：舊信與封蠟（s03 阿令接住、s09 交給秦霜、s10 拆開、s12 是白紙，之後一直在秦霜手上，s32 眼淚落在上面）；鐵鏈（s07 綁鄧押司，第 51 集鎖秦霜的同一種）；白玉佩（s23 許硯拿出來、s33 放進秦霜手裡；背面的「秦」字不畫）；紅纓長槍（s15 漂在秦霜腳邊，火堆戲不出現）。",
    "- 連戲：第 53 集強制任務已完成。玉佩：第 41 集原主書箱裡的油布包、第 44 集秦霜認出、第 50 集她說是她爹的；本集她說爹把它交給最信任的親兵送出去，最後一封信說到了青州柳溪（細綱 general_payoffs：親兵在柳溪附近失蹤）；許硯只推到「這塊玉是在柳溪丟的」。m11 的完整答案（它是什麼、送信的人怎麼了）留給第三季，m05（原主怎麼落水）也不碰。m03 只 setup：秦烈山的罪名是通敵、他守北疆二十年；誰嫁禍、為什麼都不說（第三季）。竹林裡的無名墳是秦霜的娘（第 13–15 集的那座墳）。好感：秦霜 66（s36，因為他說陪她洗冤，而且先前在客棧選了不流血的路，s35 她自己說出來）；本集結束三人是唐小棠 61、秦霜 66、阿令 59（細綱 state）。結尾秦霜問的是系統面板（他常對著空氣笑）；第 55 集從許硯看著火回答「那裡有我想要的，一個家」接，他不說出系統。",
    "- 秒數：`gen-dh.mjs` 自動決定。",
    "- 系統面板不由模型畫：s36 的好感度在剪接時疊上（affection）。",
    "- 新的參照圖還沒畫：鄧押司的定妝照（`refs-dh/dengyasi-portrait-t1.png`），場景 `set-beidu-qiantan-t1.png`、`set-hetan-t1.png`；兩張場景圖都缺，所以本集每一鏡都要等圖。",
]

BRIEF = """
# 《種田娶妻打天下》第 54 集〈她第一次哭〉

## 故事前提

第 53 集收在渡口淺灘：鄧押司退到木筏邊，晃著一封「給妳爹的信」：「要信，就放我走。」秦霜的眉頭狠狠擰緊。第 54 集從她的回答開始：「信，」「我自己去拿。」槍桿貼著水面一掃，鄧押司仰面摔進淺灘，信飛上半空——阿令一把接住：「拿到了。」（細綱的 hook。）鄧押司坐在水裡求饒：「饒、饒命……」秦霜槍尖一點：「州府的牢，」「換你去坐。」許硯拿他自己腰上的鐵鏈綁住他的手腕：「這條鏈子，」「還你。」鄧押司吐一口：「你們惹的人，」「惹不起。」（細綱 satisfaction：villain_humbled。）

阿令把信遞給秦霜：「妳的。」秦霜發抖的手壓碎封蠟：「爹……」——信攤開，裡面是一張什麼都沒有的白紙（細綱的 mid_hook）。許硯一愣：「白紙？」鄧押司仰頭大笑：「哪有什麼信，」「騙妳的。」秦霜跪進淺水裡，終於哭出聲：「我以為……」「我以為找到他了……」許硯跪到她面前：「我在。」阿令牽著鄧押司的鐵鏈走上岸，背對著他們。

夜裡的河灘，一堆篝火，火星飛進滿天星（細綱的奇觀），被綁的押解靠成一排。許硯：「那一串，」「明早押回州府。」秦霜抱著膝看火，第一次把一切說出來（細綱的 turn）：「我爹被定罪那天，」「罪名是通敵。」「他守了北疆二十年。」（m03 的 setup。）許硯攤開手心的白玉：「這塊玉，」「他從不離身。」「他交給最信任的親兵，」「送出去。」「那個人，」「再也沒回來。」許硯問：「他最後，」「去了哪裡？」「最後一封信說，」「到了青州柳溪。」許硯盯著掌心的玉：「所以這塊玉，」「是在柳溪丟的。」（m11 細綱列的 payoff：玉佩是秦烈山托親兵送出的，親兵在柳溪附近失蹤；它到底是什麼，第三季。）「娘等不到消息，」「一病就沒起來。」「竹林裡那座墳，」「是我娘。」一滴眼淚落在白紙上。許硯坐到她旁邊，把她的手指合起來握住玉：「妳爹的冤，」「我陪妳洗。」秦霜含著淚笑：「客棧那晚，」「謝謝你按住我。」系統：秦霜好感六十六。她把頭靠在他肩上（細綱的顏值鏡頭）；火堆另一邊的阿令垂下眼撥炭。

然後秦霜抬起頭、抹掉眼淚，指著他眼前的空氣：「你常對著那裡笑。」「那裡有什麼？」阿令也停下手，轉過頭來等他回答——許硯吸一口氣，嘴唇剛張開（細綱的 cliffhanger，emotion，「他會說出系統的祕密嗎？」）。

本集細綱：`season-01.json` 第 54 集（130 秒，第一季第六章第四集，調性感人＋甜寵，lead_arc wins）。satisfaction：villain_humbled（s02–s08）、level_up（s35–s36）。general_payoffs 全部入鏡：秦霜好感 66、破 60（s34–s36）；鄧押司被押回州府（s07、s20）；許硯知道玉佩是秦烈山交給親兵送出的東西、親兵在柳溪附近失蹤（s23–s28）。setup m03：s22；payoff m11（細綱列的部分）：s23–s28。

## 鉤子（站主 10-16：開場、結尾之外中段還要兩三個以上）

| 鉤子 | 鏡 | 內容 |
| --- | --- | --- |
| 【鉤子1】開場 | s01–s04 | 「信，我自己去拿」，一槍掃倒鄧押司，信飛上天被阿令接住 |
| 【鉤子2】 | s05–s08 | 鄧押司求饒、被自己的鐵鏈綁住「你們惹的人，惹不起」 |
| 【鉤子3】中段鉤子 | s09–s16 | 拆信——是一張白紙；「騙妳的」；秦霜跪在河裡哭出聲 |
| 【鉤子4】 | s19–s22 | 篝火與滿天星；「罪名是通敵，他守了北疆二十年」 |
| 【鉤子5】 | s23–s28 | 玉佩交給親兵送出、再也沒回來；最後一封信「到了青州柳溪」 |
| 【鉤子6】 | s30–s36 | 「竹林裡那座墳，是我娘」；「妳爹的冤，我陪妳洗」；好感 66 |
| 【結尾】 | s39–s43 | 「你常對著那裡笑。那裡有什麼？」阿令也轉過頭來等 |

## 角色

- 秦霜（qinshuang）：全集的主線。s01「信，我自己去拿」；s02 一槍掃倒鄧押司；s05–s06「州府的牢，換你去坐」；s09–s16 拆信、白紙、跪在河裡哭；s21–s31 說出爹的罪名、玉佩、親兵、柳溪、娘與竹林的墳；s35「客棧那晚，謝謝你按住我」；s37 把頭靠在許硯肩上；s39–s41「你常對著那裡笑。那裡有什麼？」
- 許硯（xuyan）：s07 用鐵鏈綁鄧押司「這條鏈子，還你」；s13（畫外）「白紙？」；s17「我在」；s20「明早押回州府」；s23 拿出玉佩；s26「他最後，去了哪裡？」；s28「所以這塊玉，是在柳溪丟的」；s33–s34「妳爹的冤，我陪妳洗」；s36 看好感面板；s43 嘴唇剛要張開。
- 阿令（aling）：s03–s04 接住信「拿到了」；s09「妳的」；s18 牽走鄧押司、背對他們；s29 在火堆另一邊聽；s38 看他們靠在一起、垂眼撥炭；s42 轉過頭來等他回答。
- 鄧押司（dengyasi）：s02 被掃倒；s05「饒、饒命……」；s08「你們惹的人，惹不起」；s14「哪有什麼信，騙妳的」。之後只是被綁成一排的遠景。
- 系統（xitong）：s36 秦霜好感 66（`overlays.json`）。

## 地點（固定的地點字）

- 北邊渡口淺灘（午後到傍晚）：`At the shallow ford of the north ferry outside Qingzhou late in the afternoon`（`dh-set-beidu-qiantan-t1`），破掉的囚籠還在水裡，低低的金色陽光。
- 河灘篝火（夜）：`On the pebble riverbank by the north ferry at night, a campfire of driftwood`（`dh-set-hetan-t1`）；寫 `campfire`，不寫 `bonfire`（registry 的注意事項）。

## 站主觀點

站主 2026-10-16 的要求：女生要火辣漂亮，濃顏系的五官與妝、合身剪裁；不露、不濕身、鏡頭不停在身體部位；每集至少一個顏值鏡頭；結尾收在最高點；不被黃標；每集開場、結尾之外中段再兩三個以上鉤子。本集的顏值鏡頭是 s37（秦霜靠在他肩上、火光照著哭紅的眼）；她在河裡跪下的鏡頭只寫眼淚與肩膀，衣服不寫濕（「還有點潮」只寫馬尾）。沒有血：鄧押司被掃倒在水裡、槍尖離胸口一個手掌。哭是感人調性，不寫自傷。白紙就是白紙，玉佩背面的字不畫。系統面板不由模型畫；秦霜指的「那裡」是空氣，prompt 不寫任何面板。

分鏡照 `storyboard-rules.md` 2026-10-28 起的 H3 寫法（同第 51 集）；秒數由 `gen-dh.mjs` 決定；本集沒有靜圖、沒有切素材鏡。角色外觀照 `production/cast.json` 逐字照抄。
"""

_add = {
 7: [dict(loc="ford", cam="Medium close-up, locked", chars=["dengyasi"], night="ford",
          chapter="生路", comp="medium close-up of Sergeant Deng on screen right, chained and kneeling in the shallows, a wheedling look on his heavy face, his eyes on Qin Shuang off screen left",
          lines=[("dengyasi", "信都給妳了，", "陪笑"), ("dengyasi", "放我一條生路。", "討饒")],
          motion="he shuffles forward on his knees through the water with his chained hands raised",
          zh="鄧押司中近景在右，被鏈子綁著跪在淺水裡，粗臉上堆出討好的表情，看著畫外左邊的秦霜；跪著往前挪，綁著的手舉起來"),
     dict(loc="ford", cam="Close-up, slow push in", chars=["qinshuang"], night="ford",
          comp="close-up of Qin Shuang on screen left, the golden river light on one cheek and the broken cage blurred far behind her, her face hard and proud, her eyes on Sergeant Deng off screen right",
          lines=[("qinshuang", "我爹的東西，", "冷"), ("qinshuang", "本來就是我的。", "一字一字")],
          motion="she turns her back on him and wades toward the horse",
          zh="秦霜特寫在左，臉又硬又傲，看著畫外右邊的鄧押司；轉身背對他，踩著水往馬那邊走"),
     dict(loc="ford", cam="Wide shot, locked", act=2, night="ford",
          comp="wide shot of the ford, Liuxi youths with staves herding the dripping thugs in black up onto the sandbank and tying their wrists with rope, the broken cage behind them",
          motion="two youths pull a rope tight around a thug's wrists and push him down to sit with the others in a row",
          zh="渡口全景：拿棍子的柳溪少年把濕淋淋的皂衣打手趕上沙洲，用繩子綁手腕，破籠在後面；兩個少年把一個打手的手腕拉緊綁好，推他坐進那一排"),
     dict(loc="ford", cam="Two-shot, locked", chars=["xuyan", "aling"], night="ford",
          comp="two-shot beside the bay horse in the shallows, Xu Yan on screen left looking up at A-ling in the saddle on screen right",
          lines=[("xuyan", "他說，", "低聲"), ("xuyan", "他知道妳是誰。", "看著她")],
          motion="he rests one hand on the horse's neck and waits",
          zh="雙人鏡：淺水裡的棗紅馬旁，許硯在左抬頭看坐在馬上的阿令（右）；一手扶著馬頸，等她"),
     dict(loc="ford", cam="Close-up, locked", chars=["aling"], night="ford",
          comp="close-up of A-ling in the saddle, her phoenix eyes on Xu Yan off screen left below her, guarded and cool",
          lines=[("aling", "你不問？", "很輕")],
          motion="her grip on the reins tightens a little as she waits for his answer",
          zh="阿令特寫，坐在馬上，鳳眼看著畫外左下的許硯，防備又冷淡；握韁的手緊一點，等他回答"),
     dict(loc="ford", cam="Medium close-up, slow push in", chars=["xuyan"], night="ford",
          comp="medium close-up of Xu Yan on screen left beside the horse, a calm easy smile, his eyes up on A-ling off screen right",
          lines=[("xuyan", "妳想說的時候，", "笑，很輕"), ("xuyan", "我再聽。", "很穩")],
          motion="he pats the horse's neck twice and turns to follow Qin Shuang",
          zh="許硯中近景在左、馬旁，從容的笑，抬眼看畫外右上的阿令；拍兩下馬頸，轉身去跟秦霜（他不問阿令的身分）")],
 8: [dict(loc="ford", cam="Close-up, locked", chars=["qinshuang"], night="ford",
          comp="close-up of Qin Shuang holding the sealed letter in both hands against her chest, her bold brows trembling, her eyes on Xu Yan off screen right",
          lines=[("qinshuang", "我……", "聲音發抖"), ("qinshuang", "不敢拆。", "很小聲")],
          motion="her fingers tighten on the letter and she swallows hard",
          zh="秦霜特寫，雙手把封著的信按在胸前，劍眉發抖，看著畫外右邊的許硯；手指把信抓緊，用力吞一下"),
     dict(loc="ford", cam="Two-shot, slow push in", chars=["xuyan", "qinshuang"], night="ford",
          comp="two-shot in the golden shallows, Xu Yan on screen right stepping close to Qin Shuang on screen left, his hand coming up under hers on the letter",
          lines=[("xuyan", "我陪妳拆。", "很溫柔")],
          motion="he cups her trembling hands in his own around the letter and nods to her",
          zh="雙人鏡：金色的淺水裡，許硯在右走近左邊的秦霜，手從下面托住她拿信的手；他用雙手包住她發抖的手和那封信，朝她點頭")],
}
_new = []
for _i, _x in enumerate(SHOTS):
    _new.append(_x)
    _new += _add.get(_i, [])
SHOTS = _new

_m = {i: i for i in range(1, 9)}
_m.update({9: 15, 10: 18, 11: 19, 12: 20, 13: 21, 14: 22, 15: 23, 16: 24, 17: 25, 18: 26})
_m.update({i: i + 8 for i in range(19, 44)})
import re as _re
_f = lambda t: _re.sub(r"s(\d\d)(?!\d)", lambda m: "s%02d" % _m[int(m.group(1))] if int(m.group(1)) in _m else m.group(0), t)
HEAD = [_f(x) for x in HEAD]
FOOT = [_f(x) for x in FOOT]
BRIEF = _f(BRIEF)
BRIEF = BRIEF.replace("鄧押司吐一口：「你們惹的人，」「惹不起。」（細綱 satisfaction：villain_humbled。）",
 "鄧押司吐一口：「你們惹的人，」「惹不起。」又跪著討饒：「信都給妳了，」「放我一條生路。」秦霜轉身就走：「我爹的東西，」「本來就是我的。」（細綱 satisfaction：villain_humbled。）柳溪少年把打手綁成一排。許硯走到阿令的馬邊：「他說，」「他知道妳是誰。」阿令防著他：「你不問？」許硯笑：「妳想說的時候，」「我再聽。」（接第 53 集「她是誰，她自己說」；她的身分第一季最後一集才揭。）")
BRIEF = BRIEF.replace("阿令把信遞給秦霜：「妳的。」秦霜發抖的手壓碎封蠟：「爹……」", "阿令把信遞給秦霜：「妳的。」秦霜把信按在胸前：「我……」「不敢拆。」許硯托住她的手：「我陪妳拆。」她發抖的手壓碎封蠟：「爹……」")
BRIEF = BRIEF.replace("| 【鉤子2】 | s05–s08 | 鄧押司求饒、被自己的鐵鏈綁住「你們惹的人，惹不起」 |", "| 【鉤子2】 | s05–s14 | 鄧押司求饒、被自己的鐵鏈綁住「你們惹的人，惹不起」；「他知道妳是誰」「你不問？」「妳想說的時候，我再聽」 |")
BRIEF = BRIEF.replace("| 【鉤子3】中段鉤子 | s15–s24 |", "| 【鉤子3】中段鉤子 | s15–s24 |")
BRIEF = BRIEF.replace("s05–s06「州府的牢，換你去坐」；s15–s24 拆信", "s05–s06「州府的牢，換你去坐」；s10「我爹的東西，本來就是我的」；s15–s24 拆信、s16「不敢拆」")
BRIEF = BRIEF.replace("s07 用鐵鏈綁鄧押司「這條鏈子，還你」；", "s07 用鐵鏈綁鄧押司「這條鏈子，還你」；s12–s14 對阿令「他說他知道妳是誰」「妳想說的時候，我再聽」；s17「我陪妳拆」；")
BRIEF = BRIEF.replace("s03–s04 接住信「拿到了」；s15「妳的」；", "s03–s04 接住信「拿到了」；s13「你不問？」（好感不動，仍是 59）；s15「妳的」；")
BRIEF = BRIEF.replace("s08「你們惹的人，惹不起」；", "s08「你們惹的人，惹不起」；s09「信都給妳了，放我一條生路」；")
HEAD = [x.replace("- 鉤子（站主 10-16 規則）：見 brief.md 的鉤子表", "- 鉤子（站主 10-16 規則）：見 brief.md 的鉤子表；中段鉤子（白紙）在 0:45，比片長一半早：細綱的白紙要在河灘拆，後半的火堆戲是本集的 turn，所以把揭密放前面、把說出一切放後面；相鄰兩個鉤子最多隔約 14 秒") for x in HEAD]
HEAD.insert(7, "- 檢查：lint 0 錯誤（只剩 sources 那一條警告）、30 項結構檢查全過、分鏡讀取 0 陷阱、gen-dh 51 個鏡都有 dh-set 場景參照（渡口淺灘 26、河灘篝火 25）")
HEAD = [x.replace("s50 收在嘴唇", "s51 收在嘴唇").replace("s27–s50 夜裡", "s27–s51 夜裡") for x in HEAD]
FOOT = [x.replace("s27–s50 用", "s27–s51 用") for x in FOOT]
