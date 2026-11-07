import sys
p = sys.argv[1]
t = open(p, encoding="utf-8").read()
def rep(old, new):
    global t
    assert t.count(old) == 1, (t.count(old), old[:80])
    t = t.replace(old, new)

# constants
rep('SOAP = "snow-white square bars of soap, each palm-sized and one finger thick with square corners, opaque and not glowing"\n',
'''SOAP_ST1 = "snow-white square bars of soap, each palm-sized and one finger thick with square corners, opaque and not glowing"  # s27 (picked)
# 2026-11-07 independent review of the stage-1 drafts (colab/runs/e905/review-picks.tsv): five RETAKE shots, one phrase
# per prop word for word in them (s08, s25 -> colab/runs/e905/fix2; s28, s31, s33 -> fix3). The phrases above stay in the
# picked shots.
# The soap (s31 drew a big long brick; s33's board read as white piano keys).
SOAP = "a snow-white square bar of soap the size of a palm and one finger thick"
# Tang Xiaotang's collar (s31: all four drafts drew a neckband over an open chest).
TANG_SHUT = "her peach-pink brocade ruqun one closed garment from the high stand-up collar buttoned at the throat to the waist"
COLLAR = "framed from the chin up, her face filling the frame, the top of her high stand-up collar buttoned to the throat at the bottom edge, one closed garment, no opening below the collar"
# s28, s31, s33: every draft laughed with her teeth showing; a concrete face, not just "unsmiling".
TANG_CALC = "serious and calculating the whole time, lips closed between words, the corners of her mouth level, brows slightly lowered, eyes narrowed, no smile and no teeth at any moment"
''')
rep('three rows of thirty {SOAP} slide out', 'three rows of thirty {SOAP_ST1} slide out')

# s08
rep('''         comp=f"medium shot, Lai San on screen left by the wooden post, his right sleeve still pinned by the chopping knife; Qin Shuang in the middle, her right hand on the knife handle, the right side of her belt empty; Xu Yan on screen right, {XU}, unsmiling",''',
'''         comp=f"medium shot, Lai San on screen left by the wooden shed post, {LAI}, both his hands empty, his right sleeve still pinned to the post by {CHOP}, its blade sunk deep into the post and its handle sticking out toward Qin Shuang; Qin Shuang in the middle, {QIN}, her right hand gripping that handle, the right side of her belt empty, frowning and unsmiling; Xu Yan on screen right, {XU}, unsmiling",''')
rep('''         motion="Xu Yan turns to Qin Shuang; she pulls the knife out of the post and slides it into the right side of her belt, edge down and back up; Lai San's sleeve tears open and his arm drops; the others' lips stay closed",
         zh="中景、慢推：許硯轉身看秦霜；秦霜右手拔出柴刀，刀刃朝下、刀背朝上插回腰帶右邊；賴三的袖子撕開一道口、手臂垂下來"),''',
'''         motion="Qin Shuang grips the handle with her right hand and wrenches the chopping knife out of the post; only then Lai San's right sleeve rips open along the forearm and hangs loose as his arm drops, his hands still empty; she slides the knife into the right side of her belt, blade down; Xu Yan turns his head to look at Qin Shuang; the others' lips stay closed",
         zh="中景、慢推（e905 fix2）：賴三在左、兩手空空，右袖還被舊柴刀釘在棚柱上（刀身深深吃進柱子，裹黑布的刀柄朝秦霜伸出）；秦霜在中間右手握住刀柄把柴刀從柱上拔出來，賴三的右袖這才沿前臂撕開、手臂垂下；秦霜把刀刃朝下插進腰帶右邊；右邊許硯轉頭看秦霜說話，其他人嘴閉著"),''')

# s25
rep('''         comp=f"medium close-up, closing in to a close-up by the end, of Qin Shuang, the old grey cloth outer coat draped over her shoulders, {QIN}, the corners of her mouth pressed down, unsmiling; behind her only the wooden shelter post of the same cooking shelter",''',
'''         comp=f"medium close-up, closing in to a close-up by the end, of Qin Shuang standing, one old grey cloth outer coat draped over her shoulders, {QIN}, her high ponytail a little messy, lips pressed together with the corners of her mouth turned down, brows drawn, a stubborn face, not smiling; at the left edge of the frame only Xu Yan's hand in a rolled-up blue-grey sleeve holding {POLE}; behind her only the wooden shelter post of the same cooking shelter",''')
rep('''         motion="she turns her face away, steps in and pulls the long stirring pole away from beside Xu Yan's hand off screen with her right hand",
         zh="近景、慢推（中近景推到近景）：秦霜（披灰外衣）別開臉，走過來右手把攪棍從許硯手邊抽走；嘴角壓著、不笑"),''',
'''         motion="she turns her face aside, steps to the stove and with her right hand pulls the long wooden stirring pole out of Xu Yan's hand at the left edge of the frame, then holds it upright beside her; she stays standing the whole time and never sits",
         zh="近景、慢推（中近景推到近景，e905 fix2）：秦霜（肩披舊灰布外衣、馬尾有點亂）別開臉，走到灶前右手把長攪棍從畫面左緣許硯手裡抽走，豎著拿在身邊；一直站著；抿嘴、嘴角往下、皺眉、嘴硬，不笑"),''')

# s28
rep('''         comp=f"medium shot of Tang Xiaotang at the house door on screen right, {TANG}, her small gold abacus hanging at her waist, unsmiling",''',
'''         comp=f"medium shot of Tang Xiaotang at the house door on screen right, {TANG_SHUT}, her small gold abacus hanging at her waist, {TANG_CALC}; the long wooden board on screen left",''')
rep('''         motion="Tang Xiaotang pushes the door open and walks out, unhooking the small gold abacus from her waist and tucking it under her left arm as she walks, and stops by the long board",
         zh="中景、跟拍：唐小棠（t2，襦裙從立領到腰一件闔上）推開屋門走出來，邊走邊把腰間的小金算盤取下夾在左腋下，走到木板邊停住；不笑"),''',
'''         motion="Tang Xiaotang pushes the door open and walks out; as she walks she unhooks the small gold abacus from her waist with both hands and tucks it under her left arm, then stops at the long wooden board; her face stays serious and calculating",
         zh="中景、跟拍（e905 fix3）：唐小棠（t2，襦裙從立領扣到喉嚨、到腰一件闔上）推開屋門走出來，邊走邊用兩手把腰間的小金算盤取下夾在左腋下，走到長木板邊停住；整鏡嚴肅、在盤算：話與話之間嘴閉著、嘴角平、眉微壓、瞇眼，不笑不露齒"),''')

# s31
rep('''         comp=f"close-up of Tang Xiaotang framed from the chin up, her high stand-up collar closed at her throat, {TANG}, shrewd and unsmiling, the small gold abacus under her left arm; behind her only the persimmon tree of the same yard",''',
'''         comp=f"close-up of Tang Xiaotang {COLLAR}, her peach-pink brocade ruqun; serious and shrewd, eyes narrowed in appraisal, lips closed between words, no smile and no teeth at any moment; the small gold abacus under her left arm; behind her only the persimmon tree of the same yard",''')
rep('''         motion="she lifts one white bar of soap to her nose with her right hand and sniffs it, while the fingertips of her left hand flick three beads of the abacus under her arm",
         zh="近景、慢推（下巴以上）：唐小棠右手拿一塊白皂湊到鼻下聞，左手指尖撥過腋下算盤的三顆算珠；不笑、很精"),''',
'''         motion=f"her right hand lifts {SOAP} to just under her nose and she sniffs it, while the fingertips of her left hand flick three beads of the abacus under her left arm",
         zh="近景、慢推（下巴以上，臉填滿畫面，e905 fix3）：畫面下緣是扣到喉嚨的立領頂端，一件闔上、領下沒有開口；唐小棠右手拿一塊雪白方皂（巴掌大、一指厚）湊到鼻下聞，左手指尖撥過左腋下算盤的三顆算珠；嚴肅、精明、瞇眼打量，不笑"),''')

# s33
rep('''         comp=f"reverse over-the-shoulder shot from behind Xu Yan's shoulder in the right foreground, Tang Xiaotang on screen left framed from the chin up, her high stand-up collar closed at her throat, {TANG}, sure of herself and unsmiling; behind her only the persimmon tree of the same yard",''',
'''         comp=f"reverse over-the-shoulder shot from behind Xu Yan's right shoulder in the right foreground, Tang Xiaotang on screen left in a close-up {COLLAR}, her peach-pink brocade ruqun; calm and certain, steady eyes, lips closed between words, no smile and no teeth at any moment; on the long wooden board before her only one row of identical soap bars, each {SOAP}; behind her only the persimmon tree of the same yard",''')
rep('''         motion="she sets the white bar back on the board and lines it up neatly with the others, and only then lifts her eyes to him; Xu Yan's lips stay closed",
         zh="反打（許硯肩後拍唐小棠）、慢推（唐小棠下巴以上）：唐小棠把白皂放回木板、跟其他的對齊排好，才抬眼看他；不笑、很篤定"),''',
'''         motion=f"at the start her right hand sets {SOAP} on the wooden board in line with the row of identical square bars, and only then she looks up at Xu Yan; Xu Yan's lips stay closed",
         zh="反打（許硯右肩後拍唐小棠）、慢推（唐小棠下巴以上，立領扣到喉嚨，e905 fix3）：一開始她把一塊雪白方皂（巴掌大、一指厚）放上木板、跟一排一樣的方皂對齊，才抬眼看許硯說話；木板上只有那排方皂；平靜、篤定、眼神穩，話與話之間嘴閉著，不笑"),''')
open(p, "w", encoding="utf-8").write(t)
print("ok")
