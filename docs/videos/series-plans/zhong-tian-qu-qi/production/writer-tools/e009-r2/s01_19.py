"""Scene 1 (shots c01-c19) of Episode 9 r2 (zhong-tian-qu-qi-e009-r2)."""

XU = "his faded blue-grey scholar's robe with both shoulders whole and dust on the hem, tired with slightly reddened eyes"
TANG = "in her peach-pink cross-collared short jacket wrapped shut over a pleated skirt with a ribbon bow"
HE = "little Xiaohe in her patched lilac cotton short jacket with red-string pigtails, one front tooth missing, a small woven straw rabbit tucked into her waist sash"
ALING_BASE = "in her plain grey-white cotton dress with long sleeves and a single wooden hairpin, no shackles"
BEDROLL = "one rolled dark ash-grey coarse cotton bedroll tied with hemp cord, about as thick as his chest and as long as his torso, plain cloth with no marks or writing"
CANDLE = "one small plain brass saucer candlestick with a short handle and one lit white wax candle"
BOOKS_3 = "three thin blue-cloth-bound account books stacked shut with plain blank blue covers and no marks or writing, each the size of an open hand"
BOOKS_10 = "one heavy stack of ten thin blue-cloth-bound account books shut with plain blank blue covers and no marks or writing, stacked about a forearm high"
OPEN_BOOK = "one open account book with soft out-of-focus cream pages where no stroke or character can be read"
ABACUS = "one rectangular dark-wood abacus about the length of a forearm with brown wooden beads, plain frame with no marks or writing"
NOSMILE = "no smile at any moment, not even at the end of the shot, until the last frame"

SHOTS_1 = [
    # c01: Xu yard at night, connecting directly from e008 s40. Keep named characters to 3 (xuyan, tangxiaotang, aling);
    # Qin Shuang is only seen from behind leading the brown horse to the shed on the back left.
    dict(
        chapter="選門與對帳",
        loc="yard_night",
        cam="Full shot, tracking",
        chars=["xuyan", "tangxiaotang", "aling"],
        act=5,
        night="yard_night",
        comp=(
            f"full shot past the bamboo fence and one plain blank paper lantern with no marks or writing in the right foreground, everyone small in the frame: "
            f"on screen right Xu Yan, {XU}, walking in through the open gate leading one brown horse by its hemp reins, brows low and lips closed; "
            f"in the middle Tang Xiaotang, {TANG}, lifting the hem of her skirt with one hand and walking briskly away toward the dark doorway on the back left, seen three-quarter from behind; "
            f"in the back left a tall woman seen only from behind in a dark brown cross-collared short jacket, wide leather belt with an old chopping knife at her right hip, black trousers and a high ponytail, her face never seen; "
            f"by the dark doorway on the back left A-ling, {ALING_BASE}, standing still, brows level and lips closed"
        ),
        motion=(
            f"Xu Yan hands the reins forward to the tall woman seen from behind, who leads the brown horse away toward the timber horse shed at the back left; "
            f"Tang Xiaotang steps briskly inside the dark doorway; A-ling glances once at Xu Yan, turns and steps into the dark doorway; all lips stay closed; {NOSMILE}"
        ),
        zh="全景、跟拍，前景竹籬笆與空白燈籠（接第 8 集 s40）：許硯牽棕馬進院門把韁繩遞給背影的秦霜牽往左後馬棚，唐小棠快步進屋，門口的阿令看許硯一眼轉身進屋；無人說話",
    ),
    # c02: Xiaohe runs out into the corridor holding the brass candlestick, blocks the way.
    dict(
        loc="corridor",
        cam="Medium shot, slow push in",
        chars=["xiaohe"],
        night="corridor",
        comp=(
            f"medium shot past a dark wooden corridor post in the left foreground, framed from the waist up with space above her head: "
            f"{HE}, holding {CANDLE} up in her right hand, her face three-quarter to screen left toward Xu Yan off screen left, never the lens; "
            f"earnest and stern: brows drawn together, big eyes wide and fixed on him, corners of her mouth firm"
        ),
        lines=[("xiaohe", "哥，昨天成親你躲去睡柴房，今晚不准再躲。", "很認真")],
        motion=(
            f"little Xiaohe hurries two steps in from screen right, plants her feet in the middle of the corridor and stretches her left arm out wide to block the passage as she speaks; {NOSMILE}"
        ),
        zh="中景、慢推，前景走廊木柱：小禾右手舉銅燭台從右邊跑出來停在中間，左手張開擋住走廊，認真不笑",
    ),
    # c03: Over Xiaohe's shoulder at Xu Yan by the firewood storeroom doorway; bends to pick up the bedroll.
    dict(
        loc="corridor",
        cam="Over-the-shoulder medium shot, slow push in",
        chars=["xuyan", "xiaohe"],
        night="corridor",
        comp=(
            f"over-the-shoulder medium shot framed with ample headroom above Xu Yan's head: in the lower right foreground the back of little Xiaohe's head with red-string pigtails, her face unseen; "
            f"in the middle Xu Yan standing beside the dark firewood storeroom doorway on screen left, {XU}, {BEDROLL} resting on the ground at his feet, "
            f"his face three-quarter to screen right toward little Xiaohe, never the lens; sheepish and tired: brows slightly raised, heavy eyelids, a faint awkward dry curl at one corner of his mouth"
        ),
        lines=[("xuyan", "我沒躲，柴房涼快。再說債剛還完，我累了。", "推託")],
        motion=(
            "Xu Yan bends slightly to scoop the rolled ash-grey bedroll up under his left arm, his whole head staying inside the frame, steps half a pace back toward the dark storeroom doorway on screen left and hugs the bedroll closer; little Xiaohe's lips stay closed"
        ),
        zh="過肩（小禾肩後拍許硯）、慢推：許硯從走廊口柴房門邊彎腰抱起灰藍粗布鋪蓋捲夾在左臂，退半步推託",
    ),
    # c04: Close-up of Xiaohe thrusting the candlestick into Xu Yan's right hand.
    dict(
        loc="corridor_c",
        cam="Medium close-up, slow push in",
        chars=["xiaohe"],
        night="corridor",
        comp=(
            f"medium close-up of {HE}, framed from the chest up with space above her head, holding {CANDLE} in her right hand, "
            f"her face three-quarter to screen left toward Xu Yan off screen left, the camera about 45 degrees off her eyeline, never the lens; "
            f"stern and insistent: brows pulled down, eyes wide and glaring up at him, lips firm between words; behind her only the dark earthen plaster wall of the same corridor"
        ),
        lines=[("xiaohe", "三扇門都留著燈，你自己選一扇進去。", "瞪眼，不退讓")],
        motion=(
            f"little Xiaohe steps forward one pace, presses the brass candlestick firmly out at the lower left edge toward Xu Yan off screen left and rises onto her tiptoes glaring up at him; {NOSMILE}"
        ),
        zh="近景、慢推：小禾上前一步把銅燭台塞往左下許硯手裡，踮腳瞪他，不笑",
    ),
    # c05: Xu Yan's POV looking down the dark corridor at the three closed plain wooden doors with warm light under the cracks.
    dict(
        loc="corridor",
        cam="Point-of-view medium shot, slow push in",
        chars=["xuyan"],
        nospeak=["xuyan"],
        night="corridor",
        comp=(
            f"the shot opens directly on this point-of-view medium shot down the dark roofed corridor from its very first frame: "
            f"three closed plain unpainted wooden doors in a row along the right wall with no plaques, marks or writing, warm yellow candlelight seeping through the narrow cracks around each door, "
            f"dark night beyond the corridor pillars on the left with no daylight anywhere, and at the bottom edge of the frame Xu Yan's right hand in a dusty blue-grey cotton cuff holding {CANDLE}, his face out of frame"
        ),
        lines=[("xuyan", "一扇算帳，一扇沒聲，一扇在磨刀。", "畫外，低聲")],
        motion="Xu Yan's hand at the bottom edge holds the brass candlestick as the candle flame sways gently in the night air while warm candlelight glimmers along the cracks of the three closed wooden doors",
        zh="主觀（許硯看走廊）、慢推：三扇空白木門門縫透燭光，畫面下緣許硯右手舉銅燭台的燭火微晃；許硯畫外低聲",
    ),
    # c06: Two-shot tracking from behind/side as Xiaohe pushes Xu Yan's waist toward the first door.
    dict(
        loc="corridor",
        cam="Medium two-shot, tracking",
        chars=["xuyan", "xiaohe"],
        night="corridor",
        comp=(
            f"medium two-shot framed from the thighs up with space above their heads: in front on screen right Xu Yan, {XU}, {BEDROLL} tucked under his left arm and {CANDLE} held in his right hand, "
            f"his face in profile toward the first closed wooden door on screen right, brows raised in dismay, lips closed; "
            f"behind him on screen left {HE}, both small hands planted against the back of Xu Yan's waist, her face three-quarter to screen right toward his back, never the lens; determined: brows knit, eyes bright and serious"
        ),
        lines=[("xiaohe", "小棠嫂嫂那扇最亮，先去那裡準沒錯。", "催促，用力推")],
        motion=(
            f"little Xiaohe pushes Xu Yan forward with both hands on his waist toward the first wooden door on screen right, making Xu Yan stumble two steps ahead while holding the candlestick steady; Xu Yan's lips stay closed; {NOSMILE}"
        ),
        zh="雙人鏡、跟拍：小禾從背後雙手推著許硯的腰往第一扇門走，許硯夾鋪蓋拿燭台踉蹌兩步",
    ),
    # c07: Full shot past doorframe into Tang Xiaotang's candlelit bedroom; Xu Yan shoulders door open, Tang sits behind table.
    dict(
        loc="tang",
        cam="Full shot, tracking",
        chars=["tangxiaotang", "xuyan"],
        night="candle",
        comp=(
            f"full shot past the dark wooden doorframe in the left foreground: on screen right behind the wooden table Tang Xiaotang seated upright, {TANG}, "
            f"on the tabletop {BOOKS_3}, {ABACUS}, and one lit white wax candle in a small dish, her face three-quarter to screen left toward Xu Yan, never the lens; "
            f"stern and businesslike: brows level and low, eyes cool and steady, corners of her mouth flat; "
            f"on screen left Xu Yan stepping across the threshold from the dark night corridor beyond, {XU}, {BEDROLL} under his left arm and {CANDLE} in his right hand, lips closed"
        ),
        lines=[("tangxiaotang", "來得正好，先把今天這三本帳對完再說。", "理所當然，認真")],
        motion=(
            f"Xu Yan nudges the wooden door open with his shoulder and steps inside; Tang Xiaotang lifts her eyes to him and sets her left palm flat on top of the three closed blue account books as she speaks; Xu Yan's lips stay closed; {NOSMILE}"
        ),
        zh="全景、跟拍進門，前景門框：許硯頂門走進，唐小棠坐在桌後左手按在三本空白藍布帳冊上開口，不笑",
    ),
    # c08: OTS past Tang Xiaotang's right shoulder at Xu Yan setting down candlestick and bedroll, dumbfounded.
    dict(
        loc="tang",
        cam="Over-the-shoulder medium shot, slow push in",
        chars=["xuyan", "tangxiaotang"],
        night="candle",
        comp=(
            f"over-the-shoulder medium shot framed with ample headroom above Xu Yan's head: in the lower right foreground Tang Xiaotang's peach-pink shoulder and hair bun with pink ribbon, her face unseen; "
            f"on screen left Xu Yan standing between the wooden door and the table, {XU}, {BEDROLL} under his left arm and {CANDLE} in his right hand, "
            f"his face three-quarter to screen right toward Tang Xiaotang, never the lens; dumbfounded: brows raised high, eyes wide, a faint wry twist at his mouth"
        ),
        lines=[("xuyan", "別人洞房喝交杯酒，我洞房對帳本？", "傻眼，無奈")],
        motion=(
            "Xu Yan sets the brass candlestick down on the corner of the wooden table, lowers the rolled bedroll onto the floor beside the shut door while his whole head stays inside the frame, glances down at the stack of account books and looks back at Tang Xiaotang; Tang Xiaotang's lips stay closed"
        ),
        zh="過肩（唐小棠肩後拍許硯）、慢推：許硯把燭台放上桌、鋪蓋放門邊地上，看看帳冊又看她，傻眼苦笑",
    ),
    # c09: Medium close-up of Tang Xiaotang pushing the wooden abacus toward Xu Yan.
    dict(
        loc="tang_c",
        cam="Medium close-up, slow push in",
        chars=["tangxiaotang"],
        night="candle",
        comp=(
            f"medium close-up of Tang Xiaotang framed from the chest up with space above her head, {TANG}, seated behind the wooden table with {ABACUS} before her, "
            f"her face three-quarter to screen left toward Xu Yan off screen left, the camera about 45 degrees off her eyeline, never the lens; "
            f"cool and matter-of-fact: brows level, eyes steady and serious, corners of her mouth flat; behind her only the plain dark bed curtains in the same candlelit bedroom"
        ),
        lines=[("tangxiaotang", "交杯酒一壺二十文，帳錯一筆可是幾兩。", "理所當然")],
        motion=(
            f"Tang Xiaotang slides the wooden abacus across the tabletop toward screen left with her right hand and lifts her chin slightly as she speaks; {NOSMILE}"
        ),
        zh="近景、慢推：唐小棠右手把木算盤推向左邊的許硯，下巴微抬，理所當然不笑",
    ),
    # c10: Overhead close-up insert of Xu Yan's hand flipping the open blurred account book and tracing lines without touching the abacus.
    dict(
        loc="tang_c",
        cam="Overhead close-up insert, slow push in",
        chars=["xuyan"],
        nospeak=["xuyan"],
        night="candle",
        comp=(
            f"the shot opens directly on this overhead close-up insert on the warm candlelit wooden tabletop from its very first frame: "
            f"Xu Yan's lean hands in dusty faded blue-grey cotton cuffs resting on {OPEN_BOOK}, and beside it on the left {ABACUS} untouched, his face out of frame"
        ),
        lines=[("xuyan", "後巷十二兩，客棧六兩，鏢局二兩一錢。", "畫外，邊翻邊念")],
        motion="Xu Yan's left hand turns one soft blurred page of the open account book and his right forefinger traces steadily down three blurred columns from top to bottom without ever touching the wooden abacus beside it",
        zh="手部特寫、慢推（第一格就是帳冊特寫）：許硯的手翻開虛焦看不到字的帳冊、食指往下劃，不碰旁邊算盤；許硯畫外念帳",
    ),
    # c11: Medium close-up of Xu Yan seated at the table, shutting the account book and looking up at Tang Xiaotang.
    dict(
        loc="tang_c",
        cam="Medium close-up, slow push in",
        chars=["xuyan"],
        night="candle",
        comp=(
            f"medium close-up of Xu Yan seated at the wooden table framed from the chest up with space above his head, {XU}, his hands resting on {OPEN_BOOK} on the tabletop, "
            f"his face three-quarter to screen right toward Tang Xiaotang off screen right, the camera about 45 degrees off his eyeline, never the lens; "
            f"calm and tired: heavy eyelids, brows relaxed and level, lips steady between words; behind him only the closed plain wooden door and earthen plaster wall in the same candlelit bedroom"
        ),
        lines=[("xuyan", "今天總共二十兩一錢，還完債剩下一錢。", "平穩，累")],
        motion=(
            f"Xu Yan closes the blue-cloth-bound account book with a plain blank cover cleanly with his right hand and lifts his eyes to Tang Xiaotang off screen right as he speaks; {NOSMILE}"
        ),
        zh="近景、慢推：許硯坐在桌前闔上空白藍布帳冊，抬頭看右邊的唐小棠開口，不笑",
    ),
    # c12: Medium close-up of Tang Xiaotang freezing on the abacus, leaning forward in astonishment.
    dict(
        loc="tang_c",
        cam="Medium close-up, slow push in",
        chars=["tangxiaotang"],
        night="candle",
        comp=(
            f"medium close-up of Tang Xiaotang framed from the chest up with ample headroom above her head, {TANG}, her fingers resting on {ABACUS} on the table before her, "
            f"her face three-quarter to screen left toward Xu Yan off screen left, the camera about 45 degrees off her eyeline, never the lens; "
            f"startled and astonished: brows raised high, big eyes wide open in shock, lips slightly parted; behind her only the plain bed curtains in the same candlelit bedroom"
        ),
        lines=[("tangxiaotang", "你連算盤都沒碰，怎麼算得這麼快？", "愣住，驚訝")],
        motion=(
            f"Tang Xiaotang's hand freezes on the wooden abacus, her eyes widen, and she leans slightly forward across the table with her whole head staying inside the frame before speaking; {NOSMILE}"
        ),
        zh="近景、慢推：唐小棠撥算盤的手停住，睜大眼往前微傾愣住開口，不笑",
    ),
    # c13: OTS past Tang Xiaotang's shoulder at Xu Yan flipping the blurred ledger open, turning it around and pointing to a line.
    dict(
        loc="tang",
        cam="Over-the-shoulder medium shot, slow push in",
        chars=["xuyan", "tangxiaotang"],
        night="candle",
        comp=(
            f"over-the-shoulder medium shot framed from the waist up with space above Xu Yan's head: in the right foreground Tang Xiaotang's peach-pink shoulder and hair bun, her face unseen; "
            f"on screen left Xu Yan seated at the wooden table, {XU}, {OPEN_BOOK} before him on the tabletop, his face three-quarter to screen right toward Tang Xiaotang, never the lens; "
            f"calm and matter-of-fact: brows level, eyes steady, expression composed"
        ),
        lines=[("xuyan", "心算。還有，第三頁這筆，三錢記成了三兩。", "輕描淡寫")],
        motion=(
            f"Xu Yan opens the account book to a soft out-of-focus cream page with no readable strokes, turns the open book round to face Tang Xiaotang, slides it across the tabletop and taps one blurred spot with his right forefinger; Tang Xiaotang's lips stay closed; {NOSMILE}"
        ),
        zh="過肩（唐小棠肩後拍許硯）、慢推：許硯把虛焦帳冊翻到第三頁轉過去推到她面前，食指點住一行，輕描淡寫",
    ),
    # c14: Overhead close-up insert of Tang Xiaotang's fingers flicking beads rapidly on the wooden abacus and stopping on one bead.
    dict(
        loc="tang_c",
        cam="Overhead close-up insert, slow push in",
        chars=["tangxiaotang"],
        nospeak=["tangxiaotang"],
        act=3,
        night="candle",
        comp=(
            f"the shot opens directly on this overhead close-up insert on the candlelit wooden tabletop from its very first frame: "
            f"Tang Xiaotang's slender right hand in a peach-pink silk brocade cuff poised over {ABACUS}, her face out of frame"
        ),
        motion="Tang Xiaotang's slender fingers flick briskly across a row of brown wooden abacus beads, stop abruptly, and her right forefinger presses down still on one wooden bead",
        zh="插鏡、俯拍、慢推（第一格就是算盤特寫）：唐小棠桃粉袖口的手指啪啪撥過一排算珠後停住，食指壓在一顆珠上",
    ),
    # c15: Medium close-up of Tang Xiaotang looking up slowly, her lips softening into a gentle smile (script allows smile).
    dict(
        loc="tang_c",
        cam="Medium close-up, slow push in",
        chars=["tangxiaotang"],
        night="candle",
        comp=(
            f"medium close-up of Tang Xiaotang framed from the chest up with space above her head, {TANG}, her eyes lowered toward the table at first, "
            f"her face three-quarter to screen left toward Xu Yan off screen left, the camera about 45 degrees off her eyeline, never the lens; "
            f"softened and impressed: brows relaxed, eyes warm and clear; behind her only the plain bed curtains in the same candlelit bedroom"
        ),
        lines=[("tangxiaotang", "真的錯了……我對了三遍都沒看出來。", "聲音軟下來")],
        motion="Tang Xiaotang slowly raises her eyes from the table to Xu Yan off screen left, the corners of her mouth curving up softly just a little as she speaks",
        zh="近景、慢推：唐小棠慢慢抬頭看許硯，嘴角這時才輕輕彎起來，聲音軟下來",
    ),
    # c16: Medium close-up of Xu Yan feeling awkward under her gaze, rubbing his nose; system chime + affection +2 -> 15.
    dict(
        loc="tang_c",
        cam="Medium close-up, slow push in",
        chars=["xuyan"],
        night="candle",
        comp=(
            f"medium close-up of Xu Yan seated at the table framed from the chest up with space above his head, {XU}, "
            f"his face three-quarter to screen right toward Tang Xiaotang off screen right, never the lens; "
            f"awkward and self-conscious: brows slightly drawn, eyes shifting uneasily, lips pressed closed; behind him only the closed plain wooden door in the same candlelit bedroom"
        ),
        lines=[("xitong", "叮。唐小棠，好感加二。", "提示音，平直")],
        panel=[("唐小棠 好感 +2 → 15", "good")],
        motion=(
            f"Xu Yan shifts his eyes sideways away from Tang Xiaotang off screen right, raises his right hand to rub the bridge of his nose once and lowers his hand again; his lips stay closed; {NOSMILE}"
        ),
        zh="近景、慢推：許硯被看得不自在，伸手摸一下鼻子、眼神往旁瞟，嘴閉著；系統提示好感 +2",
    ),
    # c17: Medium two-shot: Tang Xiaotang excitedly hauls a stack of ten blank blue account books from under the table onto the tabletop; Xu Yan leans back.
    dict(
        loc="tang",
        cam="Medium two-shot, slow push in",
        chars=["tangxiaotang", "xuyan"],
        night="candle",
        comp=(
            f"medium two-shot across the candlelit wooden table framed from the waist up with ample headroom above both heads: "
            f"on screen right Tang Xiaotang, {TANG}, leaning down slightly beside the table, her face three-quarter to screen left toward Xu Yan, never the lens, bright-eyed and eager; "
            f"on screen left Xu Yan seated at the table, {XU}, {CANDLE} burning on the tabletop between them, his face in profile toward Tang Xiaotang, eyes widening in alarm, lips closed"
        ),
        lines=[("tangxiaotang", "相公這麼會算，那這十本也天亮前對完。", "興奮")],
        motion=(
            f"Tang Xiaotang lifts {BOOKS_10} up from under the table with both hands, her whole head staying inside the frame, and sets the tall stack down with a thump in front of Xu Yan as she speaks; Xu Yan jerks his upper body backward in dismay, his lips staying closed"
        ),
        zh="雙人鏡、慢推：唐小棠彎腰從桌下抱出一疊十本空白藍布帳冊砰地堆到許硯面前興奮開口，許硯往後一仰",
    ),
    # c18: Medium tracking shot (10s long shot): Xu Yan rises, leaves candlestick on table, picks up bedroll by door, backs to doorway speaking, then nods to Tang's off-screen reply.
    dict(
        loc="tang",
        cam="Medium shot, tracking",
        chars=["xuyan"],
        night="candle",
        comp=(
            f"medium shot framed from the knees up with ample headroom above Xu Yan's head: on the right edge of the frame the corner of the wooden table with {CANDLE} left burning on it and {BOOKS_10}; "
            f"in the middle Xu Yan rising from his stool, {XU}, {BEDROLL} lying by the shut wooden door on screen left, "
            f"his face three-quarter to screen right toward Tang Xiaotang off screen right, never the lens; evasive and hurried: brows raised, eyes darting toward the door"
        ),
        lines=[
            ("xuyan", "我先去看看別人，帳本明天一定陪妳對。", "推託"),
            ("tangxiaotang", "明天就明天。相公記得，你欠我十本。", "畫外，帶笑提醒"),
        ],
        motion=(
            f"Xu Yan rises leaving the brass candlestick on the table, bends to scoop the rolled bedroll up under his left arm while his whole head stays inside the frame, backs two steps to the wooden door on screen left with his right hand on the door plank as he speaks, then closes his lips and gives one quick nod toward screen right; {NOSMILE}"
        ),
        zh="中景、跟拍（長鏡）：許硯起身把燭台留在桌上，彎腰抱起門邊鋪蓋退到門口扶門推託；唐小棠畫外回話時許硯閉嘴點一下頭",
    ),
    # c19: Medium close-up in dark corridor outside first door: Xu Yan pulls door shut, leans back, sighs, rolls eyes & rubs brow at system barb, walks right.
    dict(
        loc="corridor",
        cam="Medium close-up, slow push in",
        chars=["xuyan"],
        night="corridor",
        comp=(
            f"medium close-up in the dark night corridor framed from the waist up with space above his head: Xu Yan standing just outside the first plain wooden door, {XU}, "
            f"{BEDROLL} tucked under his left arm and his right hand empty with no candlestick, his face three-quarter to screen right down the corridor, never the lens; "
            f"weary and exasperated: heavy eyelids, brows drawn, lips closed"
        ),
        lines=[("xitong", "明天一定？宿主今晚第二次推託了。", "冷，嫌棄")],
        motion=(
            f"Xu Yan pulls the wooden door shut behind him, leans his back against the door plank letting out a long breath, then rolls his eyes upward, rubs between his brows once with his right hand and steps off toward screen right down the dark corridor; his lips stay closed; {NOSMILE}"
        ),
        zh="走廊中近景、慢推：許硯帶上門背靠門板吐氣（手上已無燭台、左臂夾鋪蓋），聽完系統吐槽翻白眼揉眉心往右邊第二扇門走",
    ),
]
