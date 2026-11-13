"""Scene 2 (shots c20-c38) of Episode 9 r2 (zhong-tian-qu-qi-e009-r2)."""
from s01_19 import ALING_BASE, BEDROLL, NOSMILE, XU

SHORT_BLADE = (
    "one short single-edged plain iron prop blade about one palm long with no marks or writing and a black-cloth-wrapped wooden handle, "
    "held in her left hand in a forward grip with the inward edge toward his collar and the blunt back outward"
)
WRIST_MARK = "one thin faint pale old healed mark across the inner side of her left wrist"
QUILT = "one thick dark-indigo coarse cotton quilt, plain with no pattern, marks or writing"
EYES = (
    "his irises a natural dark brown from the first frame to the last, the whites of his eyes clear, "
    "only a tiny pinprick catchlight reflected in each dark pupil"
)

SHOTS_2 = [
    # c20: Corridor outside second wooden door; Xu Yan has bedroll under left arm and NO candlestick.
    dict(
        chapter="秦霜房與阿令房",
        loc="corridor",
        cam="Medium shot, slow push in",
        chars=["xuyan"],
        night="corridor",
        comp=(
            f"medium shot in the moonlit night corridor framed from the waist up with space above his head: "
            f"Xu Yan standing before the second closed plain unpainted wooden door on screen right, {XU}, "
            f"{BEDROLL} tucked under his left arm and his right hand empty with no candlestick, "
            f"his face in three-quarter profile toward the wooden door on screen right, never the lens; cautious and tired: brows slightly raised, eyes attentive"
        ),
        lines=[("xuyan", "秦霜，睡了嗎？我進來了，有事妳就喊。", "小聲詢問")],
        motion=(
            f"Xu Yan raps twice lightly on the wooden door plank with his right knuckles, pauses a beat, then pushes the door open a narrow crack and peers inside as he speaks softly; {NOSMILE}"
        ),
        zh="中景、慢推：許硯左臂夾鋪蓋（手上無燭台）在第二扇門前敲兩下，等一下推開一條門縫探頭小聲詢問",
    ),
    # c21: POV pushing through narrow door gap into Qin Shuang's empty dark bedroom.
    dict(
        loc="qin",
        cam="Point-of-view shot, slow push in",
        chars=["xuyan"],
        nospeak=["xuyan"],
        night="qin",
        comp=(
            "the shot opens directly on this point-of-view shot through the narrow gap of the dark wooden door into the empty bedroom from its very first frame: "
            "at the left edge of the doorway gap Xu Yan's right hand in a dusty faded blue-grey cotton cuff resting lightly on the dark wooden door plank, his face out of frame; "
            "beyond the doorway nobody in the room; on the right an empty wooden bed with its quilt folded neat and square; at the back a wooden casement window standing wide open onto pitch-dark night with blank plain white window paper fluttering in the night breeze; "
            "cold blue moonlight falling on an empty wooden rack on the earthen plaster wall; on a small wooden table one white candle whose tiny flame leans sideways in the draft almost out"
        ),
        lines=[("xuyan", "窗開著，柴刀也不在，大半夜去哪了？", "畫外，低聲疑惑")],
        motion="Xu Yan's right hand pushes the wooden door plank open another finger's breadth while the blank window paper flutters in the night breeze and the tilted candle flame flickers low",
        zh="主觀（許硯看房內）、推軌，前景門縫與許硯推門右手袖口：空床疊好被子、窗戶大開吹動空白窗紙、月光照空刀架、桌上蠟燭斜倒快滅；許硯畫外低聲",
    ),
    # c22: Medium tracking shot inside Qin Shuang's room; Xu Yan looks out open window at empty night wall, closes window, candle flame stands straight.
    dict(
        loc="qin",
        cam="Medium shot, tracking",
        chars=["xuyan"],
        night="qin_close",
        comp=(
            f"medium shot by the open wooden casement window framed from the waist up with space above his head: "
            f"outside the open window only an empty earthen outer wall under cold blue moonlight and a black night sky with no daylight and nobody there; "
            f"inside beside the window Xu Yan, {XU}, {BEDROLL} tucked tight under his left arm, a small table in the foreground with one lit white candle leaning in the breeze, "
            f"his face in profile toward the open window, never the lens; puzzled and quiet: brows drawn slightly together, eyes calm"
        ),
        lines=[("xuyan", "人不在，我明天再問她。窗先替她關上。", "低聲自語")],
        motion=(
            f"Xu Yan leans slightly to glance out the open dark window, reaches out with his right hand to pull the wooden window casements shut, and the candle flame on the table straightens upright as he speaks; {NOSMILE}"
        ),
        zh="中景、跟拍：許硯夾緊鋪蓋往窗外月光下的空院牆看一眼，右手關上窗戶，桌上燭火立直",
    ),
    # c23: Low-angle medium shot in dark corridor before third wooden door; Xu Yan inhales and pushes door open.
    dict(
        loc="corridor",
        cam="Low-angle medium shot, slow push in",
        chars=["xuyan"],
        night="corridor",
        comp=(
            f"low-angle medium shot in the dark night corridor framed from the waist up with space above his head: "
            f"Xu Yan standing before the third closed plain wooden door on screen right with a thin line of warm candlelight along its crack, {XU}, {BEDROLL} under his left arm, "
            f"his face three-quarter toward the third door on screen right, never the lens; braced and nervous: brows knit, jaw set"
        ),
        lines=[("xuyan", "阿令，我進來了。我只是來鋪個地鋪。", "給自己壯膽")],
        motion=(
            f"Xu Yan draws one deep breath to steady himself and pushes the third wooden door slowly open with his right palm as he speaks; {NOSMILE}"
        ),
        zh="低角度中景、慢推：許硯左臂夾鋪蓋站在第三扇透燭光的木門前，吸一口氣右手推門開口",
    ),
    # c24: Medium shot inside A-ling's dim single-candle bedroom; Xu Yan steps in, A-ling steps from behind the door on his left holding the short blade in her left hand.
    dict(
        loc="aling",
        cam="Medium shot, slow push in",
        chars=["aling", "xuyan"],
        night="aling",
        comp=(
            f"medium shot in the dim bedroom lit by a single candle, framed from the waist up with space above their heads: "
            f"in the middle Xu Yan just stepping across the threshold from the left, {XU}, {BEDROLL} in his arms, freezing stiff with wide eyes and closed lips; "
            f"right behind his left shoulder beside the wooden door panel A-ling, {ALING_BASE}, her face appearing over his left shoulder in three-quarter profile toward him, never the lens; "
            f"icy and alert: brows sharp and low, cold phoenix eyes fixed on him, corners of her mouth flat"
        ),
        lines=[("aling", "別動。碰我一下，你就沒命。", "冷，貼在身後警告")],
        motion=(
            f"as Xu Yan steps in, A-ling's right hand presses firm on his right shoulder while her left arm in its grey-white sleeve reaches forward from behind his left shoulder holding {SHORT_BLADE} steady beside the left side of his collar; Xu Yan freezes motionless with his lips closed; {NOSMILE}"
        ),
        zh="中景、慢推（暗房單燭）：許硯抱鋪蓋跨進門僵住，身後門板邊阿令右手按他右肩、左手正握短刃橫在他左側領口邊冷聲警告",
    ),
    # c25: Medium close-up of Xu Yan raising both hands slowly as the bedroll drops from his arm; short blade visible at lower edge.
    dict(
        loc="aling_c",
        cam="Medium close-up, slow push in",
        chars=["xuyan"],
        night="aling",
        comp=(
            f"medium close-up of Xu Yan framed from the chest up with space above his head, {XU}, his face pale and tense in three-quarter profile toward A-ling off screen left, never the lens: "
            f"brows raised tight, eyes wide and steady, dry lips parting carefully; at the lower edge of the frame the plain short iron blade held steady by a grey-white left sleeve near his collar"
        ),
        lines=[("xuyan", "不碰！我手上只有鋪蓋，妳看。", "聲音發乾，急忙表明")],
        motion=(
            f"Xu Yan slowly raises both open empty hands beside his shoulders while {BEDROLL} slips from under his left arm and drops out of the bottom of the frame; {NOSMILE}"
        ),
        zh="中近景、慢推：畫面下緣是阿令左手的短刃，許硯臉色發白雙手慢慢舉到肩旁，鋪蓋從左臂滑落腳邊",
    ),
    # c26: Close-up insert (Xu Yan's downward POV) opening directly on A-ling's left hand gripping the short blade and the old pale mark on her inner left wrist.
    dict(
        loc="aling_c",
        cam="Close-up insert, slow push in",
        chars=["aling"],
        nospeak=["aling"],
        act=3,
        night="aling",
        comp=(
            f"the shot opens directly on this close-up insert in warm flickering candlelight from its very first frame: "
            f"A-ling's slender left hand in a loose grey-white cotton cuff holding {SHORT_BLADE} steady near a dark blue-grey cloth collar, "
            f"clearly showing {WRIST_MARK} where the cuff slips back slightly, her face out of frame"
        ),
        motion="the warm candle flame flickers across the plain iron blade while A-ling's slender left hand stays rock-steady, her fingers tightening once slightly around the black-wrapped wooden handle",
        zh="插鏡（第一格就是握刃的左手）：燭光下阿令左手正握短刃很穩，左手腕內側露出一道發白的舊痕，手指微收緊",
    ),
    # c27: OTS past A-ling's right shoulder & wooden hairpin at Xu Yan backed against the wooden door, looking down at her wrist.
    dict(
        loc="aling",
        cam="Over-the-shoulder medium shot, slow push in",
        chars=["xuyan", "aling"],
        night="aling",
        comp=(
            f"over-the-shoulder medium shot framed from the chest up with space above Xu Yan's head: in the right foreground A-ling's grey-white right shoulder and dark hair pinned with a plain wooden hairpin, her face unseen; "
            f"on screen left Xu Yan with his back against the closed plain wooden door and both hands still raised lightly at shoulder height, {XU}, "
            f"his face three-quarter to screen right toward A-ling, never the lens; softened and quiet: brows slightly drawn, eyes gentle and serious"
        ),
        lines=[("xuyan", "妳手腕上那道傷，是怎麼來的？", "放輕聲音")],
        motion=(
            f"A-ling's right hand pushes Xu Yan's shoulder lightly so his back rests against the wooden door plank while her left hand keeps the short blade steady; Xu Yan's gaze lowers calmly toward her left wrist and then lifts to her as he speaks softly; A-ling's lips stay closed; {NOSMILE}"
        ),
        zh="過肩（阿令右肩後拍許硯）、慢推：許硯背抵門板雙手仍舉著，目光落在她左手腕舊痕上放輕聲音詢問",
    ),
    # c28: Reverse OTS past Xu Yan's left shoulder at A-ling pulling her left sleeve down with her right hand to cover her wrist.
    dict(
        loc="aling",
        cam="Over-the-shoulder medium close-up, slow push in",
        chars=["aling", "xuyan"],
        night="aling",
        comp=(
            f"over-the-shoulder medium close-up framed from the chest up with space above A-ling's head: in the left foreground Xu Yan's dark blue-grey shoulder, his face unseen; "
            f"on screen right A-ling, {ALING_BASE}, holding the short iron blade steady in her left hand with {WRIST_MARK} just visible at her cuff, "
            f"her face three-quarter to screen left toward Xu Yan, never the lens; guarded and flat: brows level, cold eyes guarded, corners of her mouth still"
        ),
        lines=[("aling", "翻牆刮的。那道牆很高，牆裡的人也狠。", "淡漠")],
        motion=(
            f"A-ling reaches across with her right hand and tugs her grey-white left cotton cuff firmly down over her left wrist to cover the mark while her left hand stays steady, shifting her eyes away toward screen right as she speaks evenly; Xu Yan's lips stay closed; {NOSMILE}"
        ),
        zh="反打（許硯肩後拍阿令）、慢推：阿令用右手把左袖往下拉蓋住手腕舊痕，眼神避開往右看淡聲回答，不笑",
    ),
    # c29: Medium close-up tracking of Xu Yan bending slowly to pick up the bedroll without pressing further.
    dict(
        loc="aling_c",
        cam="Medium close-up, tracking",
        chars=["xuyan"],
        night="aling",
        comp=(
            f"medium close-up framed from the waist up with ample headroom above Xu Yan's head: Xu Yan standing by the wooden door, {XU}, "
            f"at the right edge of the frame a grey-white left sleeve holding the short plain iron blade, "
            f"Xu Yan's face three-quarter to screen right toward A-ling off screen right, never the lens; calm and reassuring: brows relaxed, eyes steady and sincere"
        ),
        lines=[("xuyan", "好，我不問。妳睡床，我睡門口。", "平穩，不追問")],
        motion=(
            f"Xu Yan bends slowly with his whole head staying inside the frame to pick {BEDROLL} up from the floor into both arms and straightens up calmly while the grey-white left sleeve at the right edge lowers slightly with his movement; {NOSMILE}"
        ),
        zh="近景、跟拍：許硯不追問，慢慢彎腰撿起鋪蓋抱回懷裡（頭留在畫面內），右側阿令左手的短刃跟著下移",
    ),
    # c30: Medium two-shot: A-ling on right steps half a pace back frowning in disbelief; Xu Yan on left holding bedroll.
    dict(
        loc="aling",
        cam="Medium two-shot, slow push in",
        chars=["aling", "xuyan"],
        night="aling",
        comp=(
            f"medium two-shot in the dim candlelit bedroom framed from the waist up with space above their heads: "
            f"on screen right A-ling, {ALING_BASE}, her left sleeve covering her wrist and her left hand still holding the short plain iron blade low in front of her, "
            f"her face three-quarter to screen left toward Xu Yan, never the lens; wary and incredulous: brows drawn together in a frown, sharp eyes searching his face; "
            f"on screen left Xu Yan holding {BEDROLL} in his arms, {XU}, in profile toward her, lips closed"
        ),
        lines=[("aling", "門口？你不怕我半夜，一刀下去？", "皺眉，不信")],
        motion=(
            f"A-ling steps half a pace backward toward the candlelit room on screen right, her left hand keeping the short blade unlowered and her brows knitting tighter as she speaks; Xu Yan stands steady with his lips closed; {NOSMILE}"
        ),
        zh="中景、慢推：阿令退半步皺眉不信、左手短刃未放，許硯在左抱著鋪蓋安靜看著她",
    ),
    # c31: Full shot pulling back past the doorframe (8s long shot): Xu Yan backs out over the threshold, spreads the bedroll on the corridor floor outside, looks back at A-ling.
    dict(
        loc="threshold",
        cam="Full shot, slow pull out",
        chars=["xuyan", "aling"],
        night="threshold",
        comp=(
            f"full shot past the wooden doorframe with ample headroom above both heads: just outside the threshold in the cold moonlit corridor on screen left Xu Yan, {XU}, holding {BEDROLL}; "
            f"just inside the dim warm candlelit doorway on screen right A-ling standing still, {ALING_BASE}, holding the short plain iron blade at her left side, watching him with closed lips; "
            f"dark night beyond the corridor with no daylight anywhere"
        ),
        lines=[("xuyan", "怕。所以我睡外面，誰要進來，先過我。", "坦白，篤定")],
        motion=(
            f"Xu Yan steps backward across the wooden threshold into the moonlit corridor, crouches with his whole head staying inside the frame to unroll and spread the ash-grey cotton bedroll flat along the corridor floor right outside the door, then looks up toward A-ling inside the doorway as he speaks; A-ling's lips stay closed; {NOSMILE}"
        ),
        zh="全景、慢拉，前景門框（長鏡）：許硯倒退跨出門檻，把鋪蓋攤在門外走廊地上，抬頭看向門裡的阿令篤定開口",
    ),
    # c32: Medium close-up of A-ling inside the dim candlelit doorway, lowering the short blade to her side with tip pointing down.
    dict(
        loc="aling_c",
        cam="Medium close-up, slow push in",
        chars=["aling"],
        night="aling",
        comp=(
            f"medium close-up of A-ling standing inside the dim candlelit bedroom framed from the waist up with space above her head, {ALING_BASE}, "
            f"her left sleeve covering her wrist and the short plain iron blade held in her left hand, her face three-quarter to screen left toward Xu Yan off screen left, never the lens; "
            f"quietly moved beneath her calm exterior: brows softening slightly, eyes still and deep; behind her only the dark bedroom and one small candle flame"
        ),
        lines=[("aling", "傻子。門外風大，被子拿厚的那條。", "極輕，放軟一點")],
        motion=(
            "A-ling slowly lowers her left arm straight down at her side with the tip of the short iron blade pointing down toward the floor, the corner of her mouth shifting by the faintest hair without breaking into a smile as she speaks very quietly"
        ),
        zh="近景、慢推：門裡的阿令左手短刃慢慢垂到身側（尖朝地），嘴角極輕動一下不笑開，輕聲開口",
    ),
    # c33: Low-angle medium close-up on the moonlit corridor floor: thick dark-indigo quilt tossed out onto Xu Yan lying on the bedroll; system affection +10 -> 11.
    dict(
        loc="threshold",
        cam="Low-angle medium close-up, slow push in",
        chars=["xuyan"],
        night="threshold",
        comp=(
            f"low-angle medium close-up along the spread ash-grey bedroll on the moonlit corridor floor: Xu Yan lying on his back with his head toward screen right, {XU}, "
            f"the wooden threshold and open doorway crack at the upper edge of the frame, his face turned upward toward the dark eaves above, never the lens; surprised and quiet: eyes open, lips closed"
        ),
        lines=[("xitong", "叮。阿令，好感加十。", "提示音，平直")],
        panel=[("阿令 好感 +10 → 11", "good")],
        motion=(
            f"from inside the doorway at the upper edge a grey-white cotton sleeve tosses {QUILT} out so it lands softly over Xu Yan's chest; Xu Yan catches the thick dark-indigo quilt with both hands, pulls it up to his chin and lies still looking up at the dark eaves; his lips stay closed; {NOSMILE}"
        ),
        zh="低角度近景（貼地鋪）、慢推：門裡一截灰白袖子丟出一條深藍粗布厚棉被落在許硯身上，許硯拉到下巴睜眼看屋頂；系統好感 +10",
    ),
    # c34: Extreme close-up of Xu Yan's eyes blinking once; natural dark brown irises (no eye-glow); system hidden quest complete.
    dict(
        loc="threshold",
        cam="Extreme close-up, slow push in",
        chars=["xuyan"],
        night="threshold",
        comp=(
            f"the shot opens directly on this extreme close-up of Xu Yan's eyes and brows from its very first frame, framed from the bridge of his nose to his forehead so his mouth is out of frame, "
            f"lit softly from the side by cool night light, {EYES}, never looking into the lens"
        ),
        lines=[("xitong", "隱藏任務，完成。", "提示音，收束")],
        panel=[("隱藏任務，完成", "good")],
        motion="Xu Yan's dark brown eyes blink once slowly and settle still in thought while his brows relax slightly",
        zh="眼睛大特寫、慢推（第一格就是眼睛）：自然深褐瞳孔帶極小反光點，許硯眨一下眼；系統提示隱藏任務完成",
    ),
    # c35: Medium close-up of Xu Yan turning onto his side under the thick quilt, wry faint expression, mouth closed for inner monologue.
    dict(
        loc="threshold",
        cam="Medium close-up, slow push in",
        chars=["xuyan"],
        night="threshold",
        comp=(
            f"medium close-up on the moonlit corridor floor: Xu Yan lying under {QUILT} on the spread bedroll right outside the closed plain wooden door, {XU}, "
            f"his head resting on his folded arm toward screen right, never looking at the lens; relieved yet wry: tired heavy eyelids, a faint rueful twitch at one corner of his closed mouth"
        ),
        lines=[("xuyan", "種田保住了。只是這洞房，睡的是門檻。", "無奈苦笑", "inner")],
        motion="Xu Yan rolls onto his side with his back turned to the closed wooden door behind him, tucks the thick dark-indigo quilt around his shoulder and lets out a quiet breath through his nose while his lips stay closed the whole time",
        zh="近景、慢推：許硯翻身側躺背對門板、苦笑，嘴閉著念心裡話",
    ),
    # c36: Medium close-up of Xu Yan lying on his side; system dry remark, then Xu Yan pulls the thick quilt over his head.
    dict(
        loc="threshold",
        cam="Medium close-up, slow push in",
        chars=["xuyan"],
        night="threshold",
        comp=(
            f"medium close-up on the moonlit corridor floor: Xu Yan lying on his side under {QUILT} with his back to the closed wooden door, {XU}, "
            f"his face in three-quarter profile away from the lens, brows twitching in mild annoyance, lips closed"
        ),
        lines=[("xitong", "睡哪不歸系統管。好感到了，就算數。", "冷，毒舌")],
        motion=(
            f"after a beat Xu Yan grips the edge of the thick dark-indigo quilt with both hands and pulls it right up over his head to cover his face; his lips stay closed; {NOSMILE}"
        ),
        zh="近景、慢推：許硯側躺聽完系統毒舌，伸手把厚棉被往頭上一拉蒙住頭",
    ),
    # c37: Close-up inside the closed wooden door: A-ling sitting on the floor with her back against the door, placing her right palm against the wood as she speaks quietly.
    dict(
        loc="aling_c",
        cam="Close-up, slow push in",
        chars=["aling"],
        night="aling",
        comp=(
            f"the shot opens directly on the inner planks of the closed plain unpainted wooden door and A-ling sitting on the floor inside the dim candlelit room with her back leaning against the door from its very first frame: "
            f"A-ling near the left edge of the frame, {ALING_BASE}, her left sleeve pulled down covering her wrist, the short plain iron blade resting flat across her lap, "
            f"her face in clean profile facing the wooden door plank toward Xu Yan off screen left, never the lens; solemn and quiet: brows slightly drawn, long lashes low, lips serious"
        ),
        lines=[("aling", "許硯，你聽著就好。明天，我可能得走。", "隔著門板，很輕很慢")],
        motion=(
            f"A-ling slowly raises her right hand and presses her palm flat against the inner wooden door plank beside her shoulder as she speaks very quietly toward the door; {NOSMILE}"
        ),
        zh="門板內側近景、慢推（第一格就是門板內側）：阿令背靠門板坐在地上、短刃平放膝上、左袖蓋腕，右手掌貼上門板輕聲說「明天，我可能得走」",
    ),
    # c38: Medium close-up outside the closed wooden door: Xu Yan pulls the quilt down from his head, opens his eyes and turns to look at the closed door.
    dict(
        loc="threshold",
        cam="Medium close-up, slow push in",
        chars=["xuyan"],
        act=4,
        night="threshold",
        comp=(
            f"medium close-up on the moonlit corridor floor right outside the closed plain unpainted wooden door: "
            f"Xu Yan lying on the bedroll with {QUILT} pulled up covering his head at first, dark night corridor beyond with no daylight anywhere"
        ),
        motion=(
            f"Xu Yan lowers the thick dark-indigo quilt down below his chin revealing his face, opens his eyes wide, and turns his head slowly toward the closed wooden door plank beside him, staring at it in silent gravity with his lips closed; {NOSMILE}"
        ),
        zh="近景、慢推：門外的許硯把蒙頭的厚棉被拉下來，睜開眼轉頭凝視緊閉的木門板，嘴閉著（留懸念接第 10 集）",
    ),
]
