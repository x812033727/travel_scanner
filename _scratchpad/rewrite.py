import re, sys
p = sys.argv[1]
t = open(p).read()
head, rest = t.split("SHOTS = [\n", 1)
body, tail = rest.split("\n]\n", 1)
# split body into dict blocks (keep comment lines attached to the following block)
lines = body.split("\n")
blocks, cur = [], []
for ln in lines:
    if ln.startswith("    dict(") and any(l.startswith("    dict(") for l in cur):
        # comments before this dict belong to it
        pre = []
        while cur and cur[-1].startswith("    #"):
            pre.insert(0, cur.pop())
        blocks.append(cur); cur = pre
    cur.append(ln)
blocks.append(cur)
assert len(blocks) == 40, len(blocks)

def lines_of(block):
    s = "\n".join(block)
    m = re.search(r"\n         lines=\[.*?\],\n         motion=", s, re.S)
    return m.group(0)[len("\n         "):-len(",\n         motion=")]

R = "  # 2026-11-07 retake (fix1)"
NEW = {}
NEW[1] = '''    dict(chapter="條件", loc="dawn_m", cam="Medium shot, tracking", chars=["xuyan", "tangxiaotang", "qinshuang", "aling", "xiaohe"], night="dawn",
         comp=f"medium shot past a row of white soap bars on the board in the foreground, {ONE_QIN} in the shot: Xu Yan in the middle, {XU}, red-eyed, one white bar of soap in his right hand; Tang Xiaotang beside him, {TANG}, her right hand gripping his sleeve, her small gold abacus on the board; behind them by the board Qin Shuang, {KNIFE}, A-ling, {ALING}, and little Xiaohe hugging her straw rabbit; by the end four people are in the yard: Xu Yan and Tang Xiaotang by the board, Qin Shuang alone at the persimmon tree on screen left, A-ling on the threshold of the house door on screen right",
         LINES,
         motion="Xu Yan sets the bar down and Tang Xiaotang lets go of his sleeve; meanwhile Qin Shuang walks alone to the persimmon tree on screen left and leans her back against its trunk, Xiaohe runs in through the house door on screen right and is gone, and A-ling sits down on that threshold; Xu Yan turns and walks toward them brushing his palms",
         zh="中景、跟拍、前景木板上一排白皂（接第 5 集 c40；2026-11-07 獨立審片重抽：兩稿都多一個秦霜、小禾沒進屋）：許硯（眼睛發紅、額前散髮）把手上那塊白皂放回木板，唐小棠的手從他袖子上滑開；同時秦霜一個人走到左邊柿子樹下、背靠樹幹，小禾抱草兔從右邊屋門跑進去不見，阿令在那道門的門檻坐下；許硯轉身朝她們走過去，邊走邊拍兩下手掌；結尾院子裡四個人（許硯、唐小棠、樹下的秦霜、門口的阿令），只有一個秦霜"),'''
NEW[2] = '''    dict(loc="dawn_c", cam="Medium close-up to close-up, slow push in", chars=["tangxiaotang"], night="dawn",
         comp=f"medium close-up, closing in to a close-up by the end, of Tang Xiaotang {CHIN}, {TANG}, her chin raised, {TANG_COOL}; behind her only the persimmon tree of the same yard",
         LINES,
         motion="she bends, lifts the small gold abacus off the board below the frame with both hands, straightens and hugs it flat against her chest, then raises her chin at Xu Yan off screen right; she keeps the stern look the whole shot, no smile, no dimples",
         zh="近景、慢推（中近景推到近景，下巴以上；2026-11-07 重抽：兩稿都大笑露齒）：唐小棠冷靜、公事公辦，說話之間嘴抿平，抬下巴，整鏡不笑、不露齒；彎腰兩手把小金算盤從木板上拿起，平平抱在胸前，抬下巴看許硯"),'''
NEW[4] = '''    dict(loc="dawn_c", cam="Over-the-shoulder close-up, slow push in", chars=["tangxiaotang", "xuyan"], night="dawn",
         comp=f"reverse over-the-shoulder shot from behind Xu Yan's shoulder in the right foreground, Tang Xiaotang on screen left {CHIN}, {TANG}, the small gold abacus held at her chest, {TANG_COOL}; behind her only the persimmon tree of the same yard",
         LINES,
         motion="her right fingertip flicks one bead of the abacus at her chest with a click, and only then she lifts her eyes to him with a level, serious stare, never smiling; Xu Yan's lips stay closed",
         zh="反打（許硯肩後拍唐小棠）、慢推（下巴以上；2026-11-07 重抽：兩稿都笑）：唐小棠冷靜、公事公辦，嘴抿平，整鏡不笑、不露齒；右手指尖撥一顆胸前算盤的算珠「啪」一聲，再抬眼平平地、認真地看他"),'''
NEW[6] = '''    dict(loc="dawn_c", cam="Low-angle medium close-up, slow push in", chars=["qinshuang"], night="dawn",
         comp=f"low-angle medium close-up from the roots of the persimmon tree of Qin Shuang standing upright, her shoulders resting against the persimmon trunk and both boots on the ground, {QIN}, {CHOP}, cold and unsmiling; behind her only the persimmon branches and the sky of the same yard",
         LINES,
         motion="she pushes off the trunk and stands straight, her right hand presses once on the black-wrapped handle of the chopping knife in the right side of her belt, and she looks ahead toward Xu Yan off screen right, not smiling",
         zh="低角度中近景、慢推（從樹根往上拍；2026-11-07 重抽：兩稿開頭都坐在地上）：秦霜站著、肩膀靠在柿子樹幹上、兩腳踩地；背離開樹幹站直，右手按一下腰帶右邊柴刀纏黑布的刀柄，看著前方的許硯；不笑"),'''
NEW[16] = '''    dict(loc="morn_c", cam="Medium close-up, slow push in", chars=["xuyan"], night="morn",
         comp=f"medium close-up framed from the chest up of Xu Yan, {XU}, {RED_SASH}, the red cloth clearly visible across his chest in the close frame the whole shot, {RED}, {HAIR}; behind him only the persimmon tree of the same yard",
         LINES,
         motion="he straightens up, lets out one long breath and his shoulders drop; his lips stay closed the whole time, and only the corners of his mouth start to lift",
         zh="中近景、慢推（胸口以上；2026-11-07 重抽：兩稿紅布只在腰上、嘴微開）：許硯胸前一條紅布從左肩斜綁到右腰，整鏡看得清楚；直起身，長出一口氣，肩膀一鬆；嘴一直閉著，只有嘴角剛要往上；心裡話"),'''
NEW[21] = '''    dict(loc="yamen", cam="Over-the-shoulder medium shot, slow push in", chars=["zhaobutou", "xuyan"], night="yamen",
         comp=f"reverse over-the-shoulder shot from behind Xu Yan's shoulder in the left foreground, {ZHAO} on screen right one step above, eyeing him sideways, unsmiling; at the left edge Xu Yan's hands hold out {LETTERS}; no white paper anywhere",
         LINES,
         motion="Constable Zhao takes the red letters from Xu Yan's hands between two fingers of his left hand, flips through their plain red backs and looks down sideways; Xu Yan's lips stay closed",
         zh="反打（許硯肩後拍趙捕頭）、慢推（2026-11-07 重抽：兩稿婚書變米白紙、憑空出現）：畫面左緣許硯的手遞出三份摺成長條的大紅紙婚書（紅色紙背朝鏡頭、看不到字，沒有白紙）；趙捕頭左手兩指夾過來翻了翻，斜眼往下看"),'''
NEW[23] = '''    dict(loc="yamen_m", cam="Two-shot, slow push in", chars=["tangxiaotang", "xuyan", "qinshuang"], night="yamen",
         comp=f"two-shot, Tang Xiaotang in front {CHIN}, {TANG}, {FLOWER_BUN}, leaning to Xu Yan's ear, worried, her brows drawn together, unsmiling; Xu Yan beside her, {XU}, {RED_SASH}; behind them {ONE_QIN}, {QIN}, {KNIFE}, {BASKET} in the crook of her left arm",
         LINES,
         motion="Tang Xiaotang tugs his sleeve and whispers urgently at his ear, never smiling; behind, Qin Shuang steps forward with her right hand on her knife handle, and Xu Yan reaches back and grips her right wrist, the back of his hand brushing the basket on her left arm",
         zh="雙人鏡、慢推（唐小棠近景下巴以上；2026-11-07 重抽：唐小棠笑、籃子在右手或在許硯手上、沒按住手腕）：唐小棠擔心、皺眉、不笑，扯一下他的袖子湊到他耳邊急著小聲說；後面只有一個秦霜，左臂彎挎著綠葉包白皂的竹籃，右手按刀柄往前一步；許硯反手抓住她的右手腕，手背碰到她左臂上的竹籃"),'''
NEW[27] = '''    dict(loc="yamen", cam="Two-shot, tracking", chars=["xuyan", "zhaobutou"], night="yamen",
         comp=f"two-shot, Xu Yan on screen left, {XU}, {RED_SASH}, on his two palms {PARCELS}, stacked neatly; {ZHAO} on screen right one step above",
         LINES,
         motion="Xu Yan steps up one stair and bows a little, holding the stacked parcels out on his palms; Constable Zhao lifts the top parcel off with his right hand; Zhao's lips stay closed",
         zh="雙人鏡、跟拍（2026-11-07 重抽：兩稿紅紙包變成軟布枕、只有兩個）：許硯兩掌上疊著三個分開的方形紅紙包（掌心大、一指厚、邊角方正、細紅繩繞一圈打小結），走上一階微微彎腰遞上；趙捕頭右手從最上面拿起一個"),'''
NEW[28] = '''    dict(loc="yamen_c", cam="Medium close-up to close-up, slow push in", chars=["zhaobutou"], night="yamen",
         comp=f"medium close-up, closing in to a close-up by the end, of {ZHAO}, in his right hand {PARCEL}, firm and boxy with one solid block inside, unsmiling; behind him only the vermilion gate of the same county yamen",
         LINES,
         motion="he lifts the parcel to his nose and sniffs, pauses, sniffs a second time, and only then his narrow eyes go wide",
         zh="近景、慢推（中近景推到近景；2026-11-07 重抽：兩稿紅紙包是扁紅包袋）：趙捕頭右手拿一個方正紅紙包（硬、方、裡面一整塊、細紅繩打結），湊到鼻下聞兩次，細眼瞪大"),'''
NEW[29] = '''    dict(loc="yamen_c", cam="Medium close-up, slow push in", chars=["tangxiaotang"], night="yamen",
         comp=f"medium close-up of Tang Xiaotang {CHIN}, her peach-pink brocade ruqun one closed opaque garment from the high stand-up collar fastened at her throat down to the waist, no opening, cutout or skin below the collar, {FLOWER_BUN}, the small gold abacus held at her chest, a sharp calculating stern look, unsmiling; behind her only the stone steps of the same county yamen",
         LINES,
         motion="she steps forward and her right finger flicks one bead on the abacus at her chest with a click; she keeps the stern look the whole shot, no smile, no teeth",
         zh="中近景、慢推（下巴以上；2026-11-07 重抽：兩稿大笑、01 立領下開口露肌膚、沒撥算盤、紅紙花看不到）：唐小棠襦裙從扣到喉嚨的立領到腰一件闔上、不透、沒有開口；丸子頭旁別一朵小紅紙花；精明、盤算、不笑；往前一步，右手指撥一顆胸前算盤的算珠"),'''
NEW[30] = '''    dict(loc="yamen_m", cam="Medium shot, tracking", chars=["zhaobutou", "xuyan", "tangxiaotang"], night="yamen",
         comp=f"medium shot, {ZHAO} in the middle, {PARCELS} in his hands, one square brass seal on the small table behind him; at the left edge of the frame Xu Yan, {XU}, {RED_SASH}, {LETTERS} under his left arm, and Tang Xiaotang, {TANG}, the abacus at her chest, unsmiling; no white paper anywhere",
         LINES,
         motion="Constable Zhao tucks the three red parcels inside the front of his black robe, turns, picks up the square brass seal from the small table with his right hand and turns back holding out his left hand; Xu Yan pulls the red letters from under his left arm and hands them over, their plain red backs to the camera; at the left edge Tang Xiaotang hangs her abacus back on her waist",
         zh="中景、跟拍（2026-11-07 重抽：兩稿婚書是米白紙、有印刷字，趙捕頭沒塞紅紙包、沒拿銅印）：趙捕頭把三個方正紅紙包塞進黑袍前襟，轉身右手從小桌上拿起一方銅印，轉回來伸左手；許硯從左腋下抽出摺好的大紅紙婚書遞上（紅色紙背朝鏡頭、沒有白紙、看不到字）；唐小棠在左邊緣把算盤掛回腰間"),'''
NEW[35] = '''    dict(chapter="市集", loc="market_m", cam="Full shot, tracking", chars=["xuyan", "tangxiaotang", "qinshuang", "aling"], night="market",
         comp=f"full shot past one overturned empty bamboo basket on the flagstones in the foreground, {STALLS}; walking in from screen left Xu Yan, {XU}, {RED_SASH}, Tang Xiaotang, {TANG}, {ONE_QIN}, {KNIFE}, {BASKET} on her left arm, and A-ling last, {ALING}; a few passers-by in Song-dynasty cross-collared coarse cotton jackets, cloth head-wraps and cloth shoes, far away on the far side of the street",
         LINES,
         motion="Qin Shuang hands the basket to Xu Yan and he takes it in his right hand; the four walk into the street, A-ling last; the far passers-by keep to the far side and walk off; Tang Xiaotang stops and stares at the nailed planks, bewildered, with a tense frown, never smiling",
         zh="全景、跟拍、前景石板上翻倒的空竹籃（長鏡；2026-11-07 重抽：兩稿攤子都開著、籃裡像高麗菜、唐小棠笑、02 多一個秦霜）：兩邊每個攤子都用粗木板釘死、什麼都沒擺；秦霜（只有一個）把綠葉包白皂的竹籃遞給許硯，許硯右手接過；四人走進街口，阿令最後；遠處幾個路人（宋式交領粗布短打、布包頭、布鞋）貼著對面走開；唐小棠停步瞪著木板，茫然、皺眉、不笑"),'''
NEW[36] = '''    dict(loc="market_c", cam="Medium shot, slow push in", chars=["xuyan"], night="market",
         comp=f"medium shot with the camera beside the board, of Xu Yan, {XU}, {RED_SASH}, {BASKET} in his right hand, grim and unsmiling, before one stall front nailed shut with rough planks, one paper notice pasted on a plank and seen almost edge-on the whole shot: only its paper edge and one red handprint show, its face never turns toward the camera; behind him only the same market street, {STALLS}",
         LINES,
         motion="Xu Yan walks up to the planks and presses the curling notice flat with his left hand, grim, and looks down at it; the camera stays beside the board, so the notice stays edge-on the whole shot",
         zh="中景、慢推、鏡頭在木板旁（長鏡；2026-11-07 重抽：兩稿告示轉正有假字、籃裡像高麗菜、攤子開著、許硯笑、用右手壓）：告示整鏡幾乎側邊入鏡，只看得到紙緣與一個紅手印，正面不轉向鏡頭；木板是釘死的攤子門面；許硯右手提綠葉包白皂的竹籃，左手把翹起的告示壓平，低頭看；臉色沉、不笑"),'''
NEW[37] = '''    dict(loc="market_c", cam="Close-up, slow push in", chars=["tangxiaotang"], night="market",
         comp=f"close-up of Tang Xiaotang {CHIN}, {TANG}, {FLOWER_BUN}, serious and tense, her lips tight, unsmiling; behind her only the boarded stalls of the same market street",
         LINES,
         motion="speaking low through tense lips, she presses the abacus at her waist with one hand and jerks her chin up toward the upper right of the frame, her eyes on Xu Yan off screen left; she never smiles",
         zh="近景、慢推（下巴以上；2026-11-07 重抽：兩稿大笑、沒朝茶樓指）：唐小棠認真、緊張、嘴抿緊、不笑，壓低聲音；一手按住腰間的算盤，下巴往畫面右上一抬，眼睛看著許硯"),'''
for i, txt in NEW.items():
    old = blocks[i - 1]
    comments = [l for l in old if l.startswith("    #")]
    s = "\n".join(old)
    assert ("chapter=" in txt) == ("chapter=" in s.split("\n")[len(comments)]), i
    blocks[i - 1] = comments + txt.replace("LINES", lines_of(old)).split("\n")
open(p, "w").write(head + "SHOTS = [\n" + "\n".join("\n".join(b) for b in blocks) + "\n]\n" + tail)
