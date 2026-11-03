#!/usr/bin/env python3
"""Write the 12 zero-dialogue episode specs (e03-e05 of four series)."""
import json
from pathlib import Path

OUT = Path("/home/user/travel_scanner/docs/videos/zero-dialogue-series-ideas/production")
STATIC = " The camera holds a static shot."


def lav(expr):
    return ["-f", "lavfi", "-i", expr]


def noise(src, af):
    return ["-f", "lavfi", "-i", src, "-af", af]


SFX = {
    "tap": lav("aevalsrc='0.6*sin(2*PI*1800*t)*exp(-90*mod(t,0.22))*lt(t,0.66)':d=0.7:s=48000"),
    "lock": lav("aevalsrc='0.7*sin(2*PI*1500*t)*exp(-70*t)+0.5*sin(2*PI*900*(t-0.08))*exp(-70*(t-0.08))*gt(t,0.08)':d=0.3:s=48000"),
    "musicbox": lav("aevalsrc='0.2*sin(2*PI*1568*t)*exp(-5*mod(t,0.5))+0.15*sin(2*PI*2093*t)*exp(-5*mod(t+0.25,0.5))':d=3:s=48000"),
    "buttons": noise("anoisesrc=c=white:d=1.5:a=0.5", "tremolo=f=18:d=1,highpass=f=1500,volume=-6dB"),
    "snore": noise("anoisesrc=c=brown:d=2.5:a=0.6", "tremolo=f=0.8:d=1,lowpass=f=400,volume=6dB"),
    "beep": lav("aevalsrc='0.4*sin(2*PI*1000*t)':d=0.15:s=48000"),
    "tvoff": lav("aevalsrc='0.35*sin(2*PI*(1500*t-400*t*t))*exp(-2.5*t)':d=1.2:s=48000"),
    "tick": lav("aevalsrc='0.6*sin(2*PI*3000*t)*exp(-150*mod(t,0.5))':d=2.5:s=48000"),
    "ratchet": lav("aevalsrc='0.6*sin(2*PI*3000*t)*exp(-150*mod(t,0.08))':d=1.6:s=48000"),
    "boing": lav("aevalsrc='0.5*sin(2*PI*(220+80*sin(2*PI*9*t))*t)*exp(-3*t)':d=1.0:s=48000"),
    "cuckoo": lav("aevalsrc='0.4*(sin(2*PI*700*t)*between(t,0,0.18)+sin(2*PI*560*t)*between(t,0.22,0.45)+sin(2*PI*700*t)*between(t,0.7,0.88)+sin(2*PI*560*t)*between(t,0.92,1.15))':d=1.3:s=48000"),
    "pour": noise("anoisesrc=c=pink:d=2:a=0.5", "lowpass=f=2500,highpass=f=300,afade=t=in:d=0.1,afade=t=out:st=1.5:d=0.5"),
    "splash": noise("anoisesrc=c=white:d=0.8:a=0.9", "lowpass=f=4000,afade=t=out:st=0.05:d=0.75,volume=3dB"),
    "blower": noise("anoisesrc=c=brown:d=2:a=0.4", "tremolo=f=30:d=0.6,highpass=f=200,afade=t=out:st=1.6:d=0.4"),
    "whoosh": noise("anoisesrc=c=pink:d=0.8:a=0.8", "bandpass=f=800:width_type=o:w=2,afade=t=in:d=0.4,afade=t=out:st=0.4:d=0.4,volume=4dB"),
    "hum": noise("sine=f=120:d=2", "tremolo=f=6:d=0.7,volume=-8dB,afade=t=out:st=1.6:d=0.4"),
    "powerdown": lav("aevalsrc='0.3*sin(2*PI*(600*t-250*t*t))*exp(-1.5*t)':d=1.2:s=48000"),
    "bell": lav("aevalsrc='0.3*sin(2*PI*4200*t)*(0.6+0.4*sin(2*PI*14*t))*exp(-1.5*t)+0.2*sin(2*PI*5300*t)*(0.6+0.4*sin(2*PI*11*t))*exp(-1.5*t)':d=1.5:s=48000"),
    "typing": noise("anoisesrc=c=white:d=2:a=0.5", "tremolo=f=14:d=1,highpass=f=2000,volume=-4dB,afade=t=out:st=1.7:d=0.3"),
    "knock": lav("aevalsrc='0.8*sin(2*PI*180*t)*exp(-40*mod(t,0.25))*lt(t,0.75)':d=0.8:s=48000"),
    "aircon": noise("anoisesrc=c=pink:d=2.5:a=0.4", "lowpass=f=1200,afade=t=in:d=0.3,afade=t=out:st=2.0:d=0.5,volume=-4dB"),
    "thud": lav("aevalsrc='0.9*sin(2*PI*90*t)*exp(-12*t)':d=0.5:s=48000"),
}

INTROS = {
    "wangjia": {
        "afu": "the photo of A-Fu, a real Pembroke Welsh Corgi in blue and white striped pyjamas: keep his face, fur and pyjamas, change the pose and place as described",
        "zhenzhu": "the photo of Zhenzhu, a real red Shiba Inu in a pink floral dress: keep her face, fur and dress, change the pose and place as described",
    },
    "raccoon": {
        "doudou": "the photo of Doudou, a real young raccoon in a bright yellow hoodie with a red towel cape: keep his face, fur, hoodie and cape, change the pose and place as described",
        "mama": "the photo of Mama raccoon, a real adult raccoon in a green knitted sweater with a pearl necklace: keep her face, fur, sweater and necklace, change the pose and place as described",
        "baba": "the photo of Papa raccoon, a real adult raccoon with a round belly in a blue knitted vest over a white shirt with small reading glasses: keep his face, fur, vest, shirt and glasses, change the pose and place as described",
    },
    "piglet": {
        "fenfen": "the photo of Fenfen, a real pink pig standing upright: keep her face and skin, change the pose and place as described",
        "capy": "the photo of the capybara boyfriend, a real capybara in a green bucket hat and grey T-shirt: keep his face, fur, hat and shirt, change the pose and place as described",
    },
    "shechu": {
        "ajin": "the photo of A-Jin, a real Golden Retriever in a white office shirt with a crooked blue tie and a blank ID card: keep his face, fur, shirt, tie and card, change the pose and place as described",
        "miaozong": "the photo of Boss Miao, a real chubby orange tabby cat in a grey suit with a gold tie: keep his face, fur and suit, change the pose and place as described",
    },
}
BASE = {"wangjia": "wangjia-couple-e01", "raccoon": "raccoon-mischief-e01", "piglet": "influencer-piglet-e01", "shechu": "shechu-hell-e01"}
TAGS = {
    "wangjia": ["汪家夫妻", "柯基", "柴犬", "夫妻日常", "零台詞", "AI短劇"],
    "raccoon": ["闖禍小浣熊", "浣熊", "無厘頭", "零台詞", "AI短劇"],
    "piglet": ["網美小豬", "網美", "水豚", "小豬", "零台詞", "AI短劇"],
    "shechu": ["社畜地獄", "社畜", "貓老闆", "黃金獵犬", "零台詞", "AI短劇"],
}
SERIES_NAME = {"wangjia": "汪家夫妻", "raccoon": "闖禍小浣熊", "piglet": "網美小豬", "shechu": "社畜地獄"}
SLUG = {"wangjia": "wangjia-couple", "raccoon": "raccoon-mischief", "piglet": "influencer-piglet", "shechu": "shechu-hell"}


def S(id, camera, chars, dur, ff, clip, chapter=None, sfx=None, refs=None, cam=STATIC, inn=None):
    s = {"id": id}
    if chapter:
        s["chapter"] = chapter
    s.update({"camera": camera, "chars": chars})
    if refs is not None:
        s["refs"] = refs
    s["dur"] = dur
    if inn is not None:
        s["in"] = inn
    s["ff"] = ff
    s["clip"] = clip + cam
    if sfx:
        s["sfx"] = sfx
    return s


def brief(series, epname, premise, roles, view, outline, hook, shots):
    secs = round(sum(s["dur"] for s in shots))
    return (f"# {SERIES_NAME[series]} {epname}\n\n## 故事前提\n\n{premise}\n\n## 角色\n\n{roles}\n\n"
            f"## 站主觀點\n\n{view}\n\n## 格式\n\n- 9:16，約 {secs} 秒；Colab 首格與 H3 片段。\n\n"
            f"## 大綱\n\n### 選項 A：{epname.split('〈')[1].rstrip('〉')}\n一行說明：{outline}\n開場鉤子：{hook}\n")


EPISODES = []


def ep(series, num, title, description, headline, thumb, epname, premise, roles, view, outline, hook, shots):
    used = sorted({c[0] for s in shots for c in s.get("sfx", [])})
    extra = {k: SFX[k] for k in used if k in SFX}
    intros = dict(INTROS[series])
    if series == "raccoon" and not any("baba" in (s.get("refs") or s["chars"]) for s in shots):
        intros.pop("baba")
    spec = {
        "base": BASE[series], "intros": intros, "title": title, "description": description,
        "tags": TAGS[series], "headline": headline, "thumb": thumb,
        "brief": brief(series, epname, premise, roles, view, outline, hook, shots),
        "sfx_extra": extra, "shots": shots, "slug": f"{SLUG[series]}-e{num:02d}",
    }
    EPISODES.append(spec)


WJ_ROLES = "- 阿福（afu）、珍珠（zhenzhu）：同系列定裝照。"
RC_ROLES = "- 豆豆（doudou）、浣熊媽媽（mama）、浣熊爸爸（baba）：同系列定裝照。"
PG_ROLES = "- 粉粉（fenfen）、水豚男友（capy）：同系列定裝照；粉粉穿系列招牌的白蕾絲洋裝、大草帽配粉紅緞帶、珍珠髮夾。"
SH_ROLES = "- 阿金（ajin）、喵總（miaozong）：同系列定裝照。"

# ---------------------------------------------------------------- 汪家夫妻
ep("wangjia", 3, "老婆說五分鐘就好，老公等到頭上築了鳥巢 #汪家夫妻",
   "老公在玄關催老婆出門。本片畫面、配樂由 AI 生成。", "等妳出門", "s03-cobweb", "EP3〈等妳出門〉",
   "阿福在玄關敲錶敲到錶面裂開、翻白眼嘆氣催珍珠出門；浴室門開一條縫，珍珠只畫好一隻眼，默默把門關上鎖起來。下一格阿福還站在原地，長出拖地的白鬍子、全身蜘蛛網、頭頂鳥巢裡三隻雛鳥，窗外在下雪。他吸一口氣想再嘆，雛鳥同時瞪他。最後浴室門終於打開，一隻粉紅拖鞋踏出來——停一拍，又縮回去。",
   WJ_ROLES + "這一集珍珠只有半張化好妝的臉與一隻腳入鏡。",
   "零台詞；集數規劃盲評 85（`docs/videos/wangjia-couple/episodes.md` 的 EP7）。採納導演建議：把「拖鞋踏出又縮回」這個最強的時機放到最後（原本的 s04、s05 對調），不加鏡、不加角色。",
   "敲錶嘆氣 → 半邊眼妝、鎖門 → 等到白鬍子、蜘蛛網、鳥巢 → 想再嘆氣被雛鳥瞪 → 拖鞋踏出又縮回。",
   "柯基敲手錶敲到錶面裂開。",
   [
       S("s01-tap", "Medium shot, locked", ["afu"], 3.0,
         "Medium shot of a small apartment entryway by the front door: A-Fu the Corgi himself stands upright in a brown jacket over his striped pyjamas, sneakers on, plain car keys dangling from one paw, a plain wristwatch with no numbers on his other wrist, an impatient face.",
         "The Corgi shown in <Picture 1> taps the glass of his wristwatch hard again and again until a crack appears on it, rolls his eyes toward the right edge of the frame and lets out a huge sigh, his round belly sinking.",
         chapter="催", sfx=[["tap", 0.2], ["pop", 1.4, -8]]),
       S("s02-door", "Medium shot, locked", ["zhenzhu"], 2.4,
         "Medium shot of a white bathroom door opened only a narrow crack: Zhenzhu the Shiba herself peeks out through the gap, heavy dramatic eye makeup on only her left eye, her right eye bare, a makeup brush in her paw, a blank stare.",
         "The Shiba shown in <Picture 1> stares through the gap without blinking, then very slowly pulls her face back and closes the bathroom door; the door clicks shut.",
         sfx=[["lock", 1.9]]),
       S("s03-cobweb", "Wide shot, locked", ["afu"], 3.2,
         "Wide shot of the same small entryway: A-Fu the Corgi himself still stands in the same spot in his brown jacket and striped pyjamas holding the car keys out, but he has grown a long white beard reaching the floor, his whole body draped with dusty cobwebs, a cobweb strung between the keys and his ear, and three small chicks in a bird's nest on top of his head; through the window behind him snow is falling.",
         "The Corgi shown in <Picture 1> stands completely still; his long white beard sways slightly; the three chicks in the nest on his head open their beaks and chirp; snowflakes drift past the window.",
         chapter="很久以後", sfx=[["wind", 0.0, -8], ["birds", 0.4]]),
       S("s04-sigh", "Close-up, locked", ["afu"], 2.4,
         "Close-up of A-Fu the Corgi himself with a long white beard, cobwebs hanging from his big ears, three small chicks in a bird's nest on top of his head.",
         "The Corgi shown in <Picture 1> slowly draws in a huge breath, cheeks puffing, about to sigh again; the three chicks in the nest above all turn their heads down and glare at him; he freezes and swallows the breath. His mouth stays closed.",
         sfx=[["tension", 0.8]]),
       S("s05-slipper", "Close shot at floor level, locked", [], 2.8,
         "Close shot at floor level of a white bathroom door opening onto a hallway: a single Shiba hind paw in a fluffy pink slipper steps out onto the wooden floor; the hem of a pink floral dress at the top edge of the frame.",
         "The paw in the pink slipper shown in <Picture 1> steps out onto the floor, pauses for one beat, then slowly pulls back inside, and the bathroom door gently swings shut.",
         chapter="終於", refs=["zhenzhu"], sfx=[["lock", 2.2]]),
   ])

ep("wangjia", 4, "凌晨三點打電動的老公，隔天被包成了嬰兒 #汪家夫妻",
   "老公凌晨三點打電動大叫。本片畫面、配樂由 AI 生成。", "凌晨三點", "s05-crib", "EP4〈凌晨三點打電動〉",
   "凌晨三點，阿福戴著大耳機在沙發上打電動大叫；走廊盡頭敷著白面膜的珍珠慢慢歪頭。隔天早上，阿福被包成嬰兒躺在嬰兒床、含著奶嘴，頭上的吊鈴是一支支迷你遊戲手把。當天晚上打電動大叫的換成珍珠，阿福在嬰兒床裡聽著，吊鈴上的一支手把慢慢轉過來對著他。",
   WJ_ROLES,
   "零台詞；集數規劃盲評 79（`docs/videos/wangjia-couple/episodes.md` 的 EP2）。採納評審建議：開頭加一秒指針時鐘指三點（只有刻度、沒有數字）、s06 珍珠腳邊也散一地零食空袋、s07 吊鈴上的迷你手把轉過來對著他。",
   "指針指三點 → 打電動大叫 → 走廊面膜歪頭 → 耳朵貼平 → 被包成嬰兒、手把吊鈴 → 當晚換老婆打 → 吊鈴的手把轉向他。",
   "一個只有刻度的時鐘，指針指著三點，藍光一閃一閃。",
   [
       S("s01-clock", "Insert close-up, locked", [], 1.4,
         "Insert close-up of a plain round wall clock with no numbers, only tick marks, its hour hand pointing at three and minute hand at the top, on a dark living room wall flickering with blue light from an off-screen TV.",
         "The clock hands stay at three o'clock; blue TV light flickers across the wall and the clock face.",
         chapter="凌晨三點", sfx=[["buttons", 0.3, -6]]),
       S("s02-game", "Medium shot, locked", ["afu"], 2.8,
         "Medium shot of a dark living room at night: A-Fu the Corgi himself sits cross-legged on a grey sofa in his striped pyjamas wearing big over-ear headphones, holding a plain game controller with no logos, his face lit by blue light from an off-screen TV, crumpled empty snack bags with no labels scattered at his feet, mouth wide open yelling.",
         "The Corgi shown in <Picture 1> mashes the controller buttons frantically, his whole body swinging left and right with the game, mouth wide open in a yell.",
         sfx=[["buttons", 0.0]]),
       S("s03-door", "Wide shot, locked", ["zhenzhu"], 2.0,
         "Wide shot of a dark hallway at night: at the far end Zhenzhu the Shiba herself stands motionless in a bedroom doorway, a bathrobe over her pink floral dress, a plain white sheet face mask covering her face, her two eyes reflecting faint blue light.",
         "The Shiba shown in <Picture 1> stands perfectly still in the dark doorway, then very slowly tilts her head to one side.",
         sfx=[["tension", 0.0]]),
       S("s04-freeze", "Close-up, locked", ["afu"], 2.0,
         "Close-up of A-Fu the Corgi himself in big over-ear headphones, mouth still wide open, lit by blue TV light, thumbs on a plain game controller.",
         "The Corgi shown in <Picture 1> stops pressing the buttons; his ears slowly flatten back one notch at a time; his eyes slowly slide toward the dark hallway at the left edge of the frame. His mouth stays open."),
       S("s05-crib", "Wide shot, locked", ["afu"], 3.0,
         "Wide shot of a sunny bedroom in the morning: A-Fu the Corgi himself is swaddled tightly in a pink baby blanket up to his neck, only his head showing, lying inside a white wooden baby crib, a pacifier in his mouth; above the crib hangs a baby mobile made of tiny toy game controllers with no buttons or logos.",
         "The Corgi shown in <Picture 1> lies still, swaddled in the crib; the mobile of tiny toy controllers slowly turns above him; he blinks twice and the pacifier bobs twice.",
         chapter="隔天早上", sfx=[["musicbox", 0.0]]),
       S("s06-again", "Medium shot, locked", ["zhenzhu"], 2.6,
         "Medium shot of the same dark living room sofa at night: Zhenzhu the Shiba herself sits cross-legged on the grey sofa in a bathrobe with a plain white sheet face mask, wearing big over-ear headphones, holding a plain game controller with no logos, lit by blue light from an off-screen TV, crumpled empty snack bags with no labels at her feet, mouth wide open yelling.",
         "The Shiba shown in <Picture 1> mashes the controller buttons frantically, her whole body swinging left and right with the game, mouth wide open in a yell.",
         chapter="當天晚上", sfx=[["buttons", 0.0]]),
       S("s07-mobile", "Close-up, locked", ["afu"], 2.4,
         "Close-up of A-Fu the Corgi himself swaddled in a pink baby blanket in a dark baby crib at night, a pacifier in his mouth, eyes wide open; one tiny toy game controller with no buttons or logos hangs from the mobile just above his face.",
         "The Corgi shown in <Picture 1> lies awake listening; the tiny toy controller hanging above slowly turns to face him; he sucks the pacifier slowly twice.",
         sfx=[["buttons", 0.0, -14], ["musicbox", 0.8, -8]]),
   ])

ep("wangjia", 5, "把棉被全捲走的老公，隔天只剩一條小毛巾 #汪家夫妻",
   "老公半夜把棉被全捲走。本片畫面、配樂由 AI 生成。", "搶被子", "s04-mega", "EP5〈搶被子〉",
   "阿福半夜把整條棉被捲在身上打呼，珍珠只剩床邊一隻發抖的腳。隔天早上阿福睡在角落的寵物軟墊、只蓋一條粉紅小毛巾；珍珠把棉被、地毯、浴室踏墊、窗簾全捲在身上，捲成佔滿整張床的大被捲。阿福把小毛巾拉上來蓋頭，腳就露出來；縮腳，頭又露出來。",
   WJ_ROLES + "s01 的珍珠只有床邊一隻柴犬腳。",
   "零台詞；集數規劃盲評 79（`docs/videos/wangjia-couple/episodes.md` 的 EP4）。採納評審建議：s02 砍到 1.6 秒；s05 毛巾蓋頭露腳、縮腳露頭來回一次，陽光正好打在他臉上。",
   "捲走整條被 → 老婆發抖、眼皮跳 → 睡寵物軟墊蓋小毛巾 → 老婆捲成整張床的大被捲 → 毛巾蓋頭露腳、縮腳露頭。",
   "由上往下看，整條棉被捲成一條只露鼻子的柯基被捲。",
   [
       S("s01-burrito", "Top-down wide shot, locked", ["afu"], 2.8,
         "Top-down wide shot of a double bed at night in a dim bedroom: A-Fu the Corgi himself is rolled up inside the entire duvet like a giant burrito, only his nose sticking out, asleep; the other half of the bed is bare sheet; at the bed edge a single Shiba paw is visible, shivering.",
         "The Corgi shown in <Picture 1> snores inside the duvet roll, the roll rising and falling with each breath; the single Shiba paw at the bed edge shivers.",
         chapter="深夜", sfx=[["snore", 0.0]]),
       S("s02-twitch", "Medium close-up, locked", ["zhenzhu"], 1.6,
         "Medium close-up in a dark bedroom of Zhenzhu the Shiba herself sitting up in bed with no blanket, hugging herself and shivering, four pink plastic hair curlers on her head.",
         "The Shiba shown in <Picture 1> shivers and lets out a small puff of white breath; one eyelid twitches twice; she slowly turns her head toward the right.",
         sfx=[["tension", 0.0]]),
       S("s03-petbed", "Wide shot, locked", ["afu"], 3.0,
         "Wide shot of a sunny bedroom corner in the morning: A-Fu the Corgi himself sleeps curled up inside a round pet bed cushion on the floor in his striped pyjamas, covered only by a tiny pink hand towel, his short legs sticking out.",
         "The Corgi shown in <Picture 1> sleeps in the round pet bed; in his sleep he grabs at the air for a blanket and catches nothing; the tiny towel slips off his legs.",
         chapter="早上", sfx=[["birds", 0.0, -8]]),
       S("s04-mega", "Top-down wide shot, locked", ["zhenzhu"], 3.2,
         "Top-down wide shot of the same double bed in bright morning sun: Zhenzhu the Shiba herself is rolled up inside one gigantic roll that fills the whole bed, with visible layers of a duvet, a patterned living room rug, a bath mat and curtains; only her nose and one pink hair curler stick out; she sleeps blissfully; the window has no curtains and sunlight blazes in.",
         "The Shiba shown in <Picture 1> sleeps blissfully inside the gigantic roll; the roll slowly rises and falls with her breath; dust floats in the bright sunlight.",
         sfx=[["pop", 0.3, -6]]),
       S("s05-towel", "Close-up, locked", ["afu"], 2.8,
         "Close-up of A-Fu the Corgi himself curled up in the round pet bed in his striped pyjamas, a tiny pink hand towel over him, one eye open, a bright beam of morning sunlight across his face.",
         "The Corgi shown in <Picture 1> pulls the tiny pink towel up over his whole head and his short hind paws pop out uncovered; he tucks his paws in and his head pops out again into the sunlight; he freezes, squinting.",
         chapter="補刀", inn=0.4),
   ])

# ---------------------------------------------------------------- 闖禍小浣熊
ep("raccoon", 3, "砸壞電視的小浣熊，只好自己當電視 #闖禍小浣熊",
   "小浣熊豆豆又闖禍了。本片畫面、配樂由 AI 生成。", "我是電視", "s05-anchor", "EP3〈電視〉",
   "豆豆踢球砸壞電視，坐進空框裡當電視。爸爸拿起遙控器停了半拍才按——他知道。豆豆只好跟著換台：新聞主播、購物台推銷青蔥。最後一聲老電視關機音，豆豆在框裡躺平「關機」，地毯底下滾出那顆足球，停在爸爸的拖鞋前。",
   RC_ROLES + "爸爸只有拿遙控器的手與一隻拖鞋入鏡。",
   "零台詞；集數規劃盲評 82（`docs/videos/raccoon-mischief/episodes.md` 的 EP2）。採納評審建議（都不加鏡、不加角色）：第三台改成更荒謬的購物台推銷青蔥、爸爸按遙控器前停半拍（他在整人）、關機後地毯下滾出足球停在爸爸拖鞋前。",
   "裂螢幕、射門定格 → 鑰匙聲、慢看鏡頭 → 自己坐進空框當電視 → 爸爸停半拍按遙控器 → 新聞主播 → 購物台推銷青蔥 → 關機、足球滾到爸爸拖鞋前。",
   "裂成蜘蛛網的電視冒著煙，小浣熊一腳還舉在射門姿勢。",
   [
       S("s01-kick", "Medium shot, locked", ["doudou"], 2.6,
         "Medium shot of the cozy living room: the TV on the wooden TV stand has its black screen cracked into a spiderweb, nothing displayed, a thin wisp of smoke rising from it; a football lies on the rug; Doudou the young raccoon himself in his yellow hoodie and red cape stands frozen in a follow-through kicking pose, one hind leg still raised in mid-air.",
         "The young raccoon shown in <Picture 1> stays frozen mid-kick with one leg raised; the football rolls slowly across the rug and out of frame; smoke curls up from the cracked black screen.",
         chapter="闖禍", sfx=[["shatter", 0.0]]),
       S("s02-key", "Close-up, locked", ["doudou"], 2.0,
         "Close-up of Doudou the young raccoon's face in the foreground, red cape at his neck; behind him, out of focus, the front door.",
         "The young raccoon shown in <Picture 1> holds still; the door handle in the background slowly turns down; his eyes slide slowly from the door to the camera and his ears flatten back. His mouth stays closed.",
         sfx=[["keys", 0.2]]),
       S("s03-frame", "Medium shot, locked", ["doudou"], 2.8,
         "Medium shot of the wooden TV stand: the TV is now only an empty black frame and the screen is gone; Doudou the young raccoon himself sits cross-legged inside the empty TV frame in his yellow hoodie, frozen in a cartoon dance pose with both arms up, his red cape tucked behind him; in front of the TV stand a big lump bulges under the rug.",
         "The young raccoon shown in <Picture 1> holds his dance pose perfectly still inside the empty TV frame with a forced bright smile; one raised arm trembles slightly.",
         chapter="我是電視"),
       S("s04-remote", "Insert close-up, locked", [], 1.4,
         "Insert close-up of the arm of a beige sofa: a raccoon paw in a blue knitted vest sleeve with a white shirt cuff holds a plain remote control with no labels, pointing it off screen.",
         "The paw in the blue vest sleeve shown in <Picture 1> raises the remote, pauses for half a beat, then presses a button firmly.",
         refs=["baba"], sfx=[["beep", 1.0]]),
       S("s05-anchor", "Medium shot, locked", ["doudou"], 1.8,
         "Medium shot of the same wooden TV stand: Doudou the young raccoon himself sits stiffly upright inside the empty TV frame like a serious news anchor, front paws folded neatly in front of him, a stern face, red cape tucked behind him; a big lump bulges under the rug in front.",
         "The young raccoon shown in <Picture 1> sits perfectly upright with a stern anchor face; only his eyes slide sideways toward the off-screen sofa and back.",
         chapter="換台", inn=0.2),
       S("s06-onions", "Medium shot, locked", ["doudou"], 2.0,
         "Medium shot of the same wooden TV stand: Doudou the young raccoon himself sits inside the empty TV frame like a home shopping host, holding up a big bunch of green onions toward the camera with both paws, a huge stiff salesman smile, red cape tucked behind him.",
         "The young raccoon shown in <Picture 1> presents the bunch of green onions to the camera and turns it left and right like a product, with a stiff forced smile; his eyebrows twitch.",
         sfx=[["beep", 0.0]], inn=0.2),
       S("s07-off", "Medium shot, locked", ["doudou"], 3.0,
         "Medium shot of the same wooden TV stand: Doudou the young raccoon himself sits inside the empty TV frame in his yellow hoodie; in front of the TV stand a big lump bulges under the rug; at the right edge of the frame a single raccoon hind paw in a brown slipper rests on the floor.",
         "The young raccoon shown in <Picture 1> slowly leans back inside the frame, lies flat and closes his eyes as if switched off; a football rolls out from under the rug lump and stops against the slipper at the right edge.",
         chapter="關機", sfx=[["tvoff", 0.0], ["sting", 2.2]]),
   ])

ep("raccoon", 4, "盪壞掛鐘的小浣熊，自己變成時鐘 #闖禍小浣熊",
   "小浣熊豆豆又闖禍了。本片畫面、配樂由 AI 生成。", "我是時鐘", "s03-hands", "EP4〈時鐘〉",
   "豆豆吊在牆上的釘子上晃，腳下的大掛鐘摔碎、彈簧還在抖。他把自己貼在牆上當時鐘，兩隻手臂當指針指著三點。媽媽看看手錶——八點十分——再抬頭看牆，眉頭一皺；豆豆的「分針」手臂慌忙轉一大圈，轉到扭在頭上。頭頂的咕咕鐘小門打開，探出來咕咕叫的是戴老花眼鏡的爸爸。",
   RC_ROLES,
   "零台詞；集數規劃盲評 76（`docs/videos/raccoon-mischief/episodes.md` 的 EP3）。採納評審建議（都不加鏡、不加角色）：媽媽的錶清楚是另一個時間（八點十分）；第三拍升級成分針手臂慌忙轉一大圈扭到頭上，不是只跳一格。",
   "吊在釘子上、掛鐘碎在地上 → 鑰匙聲、慢看鏡頭 → 自己貼牆當時鐘 → 媽媽的錶是八點十分 → 手臂慌忙轉一圈 → 咕咕鐘探出爸爸。",
   "碎掉的掛鐘彈出一根還在抖的彈簧，上方吊著一隻小浣熊。",
   [
       S("s01-swing", "Medium shot, locked", ["doudou"], 2.8,
         "Medium shot of a living room wall: on the floor a big wooden wall clock lies smashed open, a coiled spring popped out of it; above it Doudou the young raccoon himself in his yellow hoodie and red cape hangs from a single nail on the wall by one paw, clutching a broken brass pendulum in the other.",
         "The young raccoon shown in <Picture 1> dangles from the nail by one paw, swinging slightly, the broken pendulum in his other paw; below, the spring on the smashed clock wobbles back and forth.",
         chapter="闖禍", sfx=[["shatter", 0.0], ["boing", 0.4]]),
       S("s02-key", "Close-up, locked", ["doudou"], 2.0,
         "Close-up of Doudou the young raccoon's face in the foreground as he hangs by one paw from a nail on the wall, red cape at his neck; behind him, out of focus, the front door.",
         "The young raccoon shown in <Picture 1> holds still, hanging; the door handle in the background slowly turns down; his eyes slide slowly from the door to the camera and his ears flatten back. His mouth stays closed.",
         sfx=[["keys", 0.2]]),
       S("s03-hands", "Medium shot, locked", ["doudou"], 3.0,
         "Medium shot of the living room wall where the clock used to hang: Doudou the young raccoon himself is the wall clock, pressed flat against the wall, his red towel cape spread into a round clock face behind him with twelve small dots and no numbers, his face at the centre, one arm pointing straight up and one arm pointing straight right like clock hands at three o'clock; below him a lump bulges under the rug with a spring poking out of its edge.",
         "The young raccoon shown in <Picture 1> stays pressed flat against the wall perfectly still, arms fixed like clock hands; his cheeks twitch in a steady ticking rhythm.",
         chapter="我是時鐘", sfx=[["tick", 0.0]]),
       S("s04-watch", "Close-up, locked", ["mama"], 2.0,
         "Close-up of Mama raccoon herself in her green sweater and pearl necklace looking down at a plain analog wristwatch on her wrist, with no numbers, its hands clearly at ten past eight.",
         "The mother raccoon shown in <Picture 1> looks at her wristwatch, then slowly lifts her eyes to the wall off screen; her brow furrows.",
         sfx=[["tick", 0.0, -8]]),
       S("s05-spin", "Medium shot, locked", ["doudou"], 2.4,
         "Medium shot of the same wall: Doudou the young raccoon himself pressed flat against the wall as the clock, red cape spread into a round clock face behind him, one arm up and one arm right, a bead of sweat on his forehead.",
         "The young raccoon shown in <Picture 1> frantically sweeps his right arm around in a big circle like a spinning minute hand until it ends twisted awkwardly over his head; his eyes dart sideways; sweat drips.",
         chapter="對時", sfx=[["ratchet", 0.0]]),
       S("s06-cuckoo", "Close shot, locked", ["baba"], 3.0,
         "Close shot of a large wooden cuckoo clock box mounted high on the living room wall with its little door open: Papa raccoon himself pokes his head out of the cuckoo clock door, small reading glasses on his nose, a small broken wooden bird held at the corner of his mouth, a deadpan face.",
         "The raccoon shown in <Picture 1> pops his head forward out of the little door twice in a stiff mechanical rhythm, the wooden bird bobbing at the corner of his mouth, then pulls back inside and the little door snaps shut.",
         chapter="咕咕", sfx=[["cuckoo", 0.2], ["sting", 2.3]]),
   ])

ep("raccoon", 5, "撞倒媽媽的盆栽，小浣熊只好自己當植物 #闖禍小浣熊",
   "小浣熊豆豆又闖禍了。本片畫面、配樂由 AI 生成。", "我是盆栽", "s05-wet", "EP5〈盆栽〉",
   "豆豆撞倒媽媽綁著粉紅緞帶的寶貝龜背芋，盆子還在地上滾。他站進盆子裡、全身黏滿葉子當植物。媽媽的澆花壺先在地毯鼓包上滴了一滴——她知道——再面不改色地往他身上澆。豆豆濕透含淚，腳邊多了一整排青蔥。隔天早上，他頭頂長出一根青蔥。",
   RC_ROLES + "媽媽只有提澆花壺的手入鏡。",
   "零台詞；集數規劃盲評 71（`docs/videos/raccoon-mischief/episodes.md` 的 EP4）。採納評審建議（都不加鏡、不加角色）：倒的是綁著粉紅緞帶的媽媽寶貝盆栽、倒下時還在滾；澆水前先在地毯鼓包上滴一滴，讓觀眾知道她知道；最後長出來的是一根青蔥。",
   "寶貝盆栽倒地還在滾 → 門縫先探進青蔥、慢看鏡頭 → 自己站進盆子當植物 → 澆花壺先滴地毯鼓包再澆 → 濕透含淚、腳邊一排青蔥 → 隔天頭上長出青蔥。",
   "綁粉紅緞帶的大盆栽倒在地上還在滾，小浣熊坐在土堆裡。",
   [
       S("s01-pot", "Medium shot, locked", ["doudou"], 2.8,
         "Medium shot of a living room corner: a huge monstera plant twice as tall as Doudou lies toppled on its side, its big ceramic pot tied with a pink ribbon bow rolling on the floor, soil spilled everywhere; Doudou the young raccoon himself sits in the pile of soil in his yellow hoodie and red cape, a broken big leaf in his paw, soil and roots on his head, frozen.",
         "The young raccoon shown in <Picture 1> stays frozen in the soil; the ceramic pot with the pink bow rolls slowly across the floor and wobbles to a stop; a clump of soil slides off his head.",
         chapter="闖禍", sfx=[["crunch", 0.0]]),
       S("s02-key", "Close-up, locked", ["doudou"], 2.0,
         "Close-up of Doudou the young raccoon's face in the foreground with soil on his head, red cape at his neck; behind him, out of focus, the front door.",
         "The young raccoon shown in <Picture 1> holds still; the front door in the background opens a crack and the green tips of a bunch of green onions poke in first; his eyes slide slowly to the camera and his ears flatten back. His mouth stays closed.",
         sfx=[["keys", 0.2]]),
       S("s03-plant", "Medium shot, locked", ["doudou"], 3.0,
         "Medium shot of the same living room corner: the big ceramic pot with the pink ribbon bow stands upright again; Doudou the young raccoon himself stands inside the pot, soil up to his knees, both arms raised and spread wide, large monstera leaves stuck all over his yellow hoodie and the biggest leaf stuck on top of his head; in the middle of the rug a big lump bulges underneath.",
         "The young raccoon shown in <Picture 1> stands perfectly still with arms raised; one leaf slowly slides down his arm and drops to the floor; his eyes follow it without moving his head.",
         chapter="我是盆栽"),
       S("s04-can", "Insert close-up, locked", [], 1.6,
         "Insert close-up at floor level: a big lump bulging under a patterned rug in the foreground; a raccoon paw in a green knitted sweater sleeve holds a metal watering can above it.",
         "The paw in the green sweater sleeve shown in <Picture 1> tips the watering can so a single drop falls onto the rug lump, pauses, then calmly swings the spout away toward the corner off screen and tilts it.",
         refs=["mama"], sfx=[["pour", 0.8]]),
       S("s05-wet", "Medium shot, locked", ["doudou"], 3.0,
         "Medium shot of the same corner: Doudou the young raccoon himself stands in the ceramic pot soaking wet from head to toe, dripping wet fur, monstera leaves plastered to his yellow hoodie, eyes teary but not moving; a neat row of fresh green onions is now planted in the soil around his feet.",
         "The young raccoon shown in <Picture 1> stands still, dripping; water drops fall from his nose and leaves; his lower lip trembles; the green onions around his feet stand upright.",
         chapter="澆水"),
       S("s06-sprout", "Close-up, locked", ["doudou"], 2.8,
         "Close-up of Doudou the young raccoon himself in morning sunlight still standing in the pot, leaves on his yellow hoodie, a single small green onion shoot growing on top of his head like a cartoon sprout.",
         "The young raccoon shown in <Picture 1> stays still; the small green onion shoot on his head slowly grows a little taller; his eyes roll up to look at it, then slowly back to the camera.",
         chapter="隔天早上", sfx=[["sting", 2.0]]),
   ])

# ---------------------------------------------------------------- 網美小豬
PG_VIEW = "零台詞；系列公式：唯美 → 閃光一瞄 → 拉遠揭曉 → 男友 → 成品照破綻 → 重擺被整。"
ep("piglet", 3, "仙境瀑布美照的真相 #網美小豬",
   "每一張美照背後，都有一個面無表情的男友。本片畫面、配樂由 AI 生成。", "瀑布真相", "s04-boyfriend", "EP3〈仙境瀑布〉",
   "粉粉在霧氣繚繞的叢林瀑布前拍美照。拉遠：陰天的頂樓，瀑布是不鏽鋼水塔破洞噴出來的水，背景是一塊印著葉子的防水布；水豚男友站在梯子上，兩隻手各堵住水塔的另一個破洞，全身濕透。她重擺姿勢，男友的手一滑，兩道水柱把她從頭沖到腳。",
   PG_ROLES,
   PG_VIEW + "EP3 題目照系列 README。",
   "叢林瀑布 → 閃光一瞄 → 頂樓水塔漏水 → 男友堵兩個破洞 → 成品照瀑布頂上有水豚臉 → 兩道水柱沖她一身。",
   "唯美瀑布前，角落有一道水往旁邊噴。",
   [
       S("s01-falls", "Close-up, locked", ["fenfen"], 2.6,
         "Close-up of Fenfen the pink pig herself in a white lace sundress, a wide straw sun hat with a long pink satin ribbon and a pearl hair clip, a dreamy three-quarter profile smile, a misty jungle waterfall cascading behind her in soft focus with ferns and mist; in the corner a thin jet of water squirts out sideways.",
         "The pink pig shown in <Picture 1> tilts her head dreamily and lifts one hoof to her hat brim; the waterfall cascades behind her; the thin jet of water in the corner sputters sideways.",
         chapter="美照"),
       S("s02-flash", "Medium close-up, locked", ["fenfen"], 2.0,
         "Medium close-up of Fenfen the pink pig herself in a white lace sundress and wide straw sun hat with a pink ribbon, frozen in a dreamy profile pose, mist and falling water behind her.",
         "A bright camera flash fires once; the pink pig shown in <Picture 1> keeps her face frozen and only her eyes slowly slide to the lower right; one eyebrow twitches.",
         sfx=[["shutter", 0.15]]),
       S("s03-roof", "Wide shot, locked", ["fenfen"], 3.0,
         "Wide shot of a shabby concrete rooftop in Taiwan under a grey sky: a big round stainless steel water tower stands on a rusty stand, and a thick stream of water gushes from a hole in its side like a waterfall; Fenfen the pink pig herself in her white lace sundress and straw hat poses under the stream holding a potted fern; a plastic tarp with a plain green leaf pattern is taped to the wall behind her.",
         "The pink pig shown in <Picture 1> holds her dreamy pose beside the stream gushing from the leaking water tower, water splashing around her feet; the green tarp flaps in the wind.",
         chapter="真相", sfx=[["recordscratch", 0.0], ["pour", 0.3, -4]]),
       S("s04-boyfriend", "Medium shot, locked", ["capy"], 2.8,
         "Medium shot on the same grey rooftop of the capybara boyfriend himself standing on a ladder against a stainless steel water tower, each front paw pressed flat over a hole in the tank, water spraying out around his paws and soaking his grey T-shirt, his green bucket hat dripping, a power bank hanging from his neck, completely deadpan.",
         "The capybara shown in <Picture 1> keeps both paws pressed on the holes while water sprays out around them; water drips from his hat brim; he blinks once slowly and his deadpan face does not change.",
         sfx=[["pour", 0.0, -6]]),
       S("s05-photo", "Insert, slow push in", ["fenfen"], 2.4,
         "The finished photo filling the vertical frame with a thin white photo border: Fenfen the pink pig in a white lace sundress and straw hat in front of a magical misty jungle waterfall, picture perfect like a magazine cover; at the top of the waterfall, between the mossy rocks, a deadpan capybara face in a green bucket hat peeks out with water pouring over it.",
         "The photo shown in <Picture 1> holds still; the capybara face at the top of the waterfall slowly blinks once as water pours over it.",
         chapter="成品", sfx=[["shutter", 0.0]], cam=" The camera pushes in with small amplitude at slow speed."),
       S("s06-splash", "Medium shot, locked", ["fenfen"], 2.8,
         "Medium shot on the grey rooftop of Fenfen the pink pig herself in her white lace sundress and straw hat, taking her dreamy profile pose again beside the leaking water tower.",
         "The pink pig shown in <Picture 1> takes her dreamy pose; suddenly two thick jets of water blast into her from the right side of the frame and drench her, flattening her straw hat; she stays frozen in the pose, smile unchanged, water dripping off her snout.",
         sfx=[["splash", 0.3]], inn=0.5),
   ])

ep("piglet", 4, "櫻花雨美照的真相 #網美小豬",
   "每一張美照背後，都有一個面無表情的男友。本片畫面、配樂由 AI 生成。", "櫻花真相", "s04-boyfriend", "EP4〈櫻花雨〉",
   "粉粉在滿天櫻花雨裡伸手接花瓣。拉遠：灰濛濛的機車停車場，櫻花樹是一棵枯樹纏滿粉紅衛生紙和塑膠袋，花瓣是碎紙；水豚男友站在梯子上，拿吹葉機往一箱粉紅碎紙裡吹，滿臉黏著碎紙。她重擺姿勢，一整箱碎紙從天而降，把她埋成一座粉紅小山。",
   PG_ROLES,
   PG_VIEW + "EP4 題目由本批企劃，照系列公式。",
   "櫻花雨接花瓣 → 閃光一瞄 → 停車場枯樹纏衛生紙 → 男友拿吹葉機吹碎紙 → 成品照櫻花叢裡有水豚臉 → 一整箱碎紙把她埋掉。",
   "櫻花雨裡，有一片花瓣是方方正正的粉紅衛生紙。",
   [
       S("s01-sakura", "Close-up, locked", ["fenfen"], 2.6,
         "Close-up of Fenfen the pink pig herself in a white lace sundress, a wide straw sun hat with a long pink satin ribbon and a pearl hair clip, a dreamy three-quarter profile smile, pink cherry blossom petals drifting all around her in soft focus, a blooming cherry tree behind her; one falling petal near the corner is a torn square of pink tissue paper.",
         "The pink pig shown in <Picture 1> smiles dreamily and reaches one hoof up to catch a falling petal; petals drift down around her and the square scrap of pink tissue flutters past in the corner.",
         chapter="美照"),
       S("s02-flash", "Medium close-up, locked", ["fenfen"], 2.0,
         "Medium close-up of Fenfen the pink pig herself in a white lace sundress and wide straw sun hat with a pink ribbon, frozen in a dreamy profile pose, pink petals drifting around her.",
         "A bright camera flash fires once; the pink pig shown in <Picture 1> keeps her face frozen and only her eyes slowly slide to the lower right; one eyebrow twitches.",
         sfx=[["shutter", 0.15]]),
       S("s03-lot", "Wide shot, locked", ["fenfen"], 3.0,
         "Wide shot of a plain concrete scooter parking lot behind an apartment block on a grey afternoon, rows of parked scooters with no logos: Fenfen the pink pig herself in her white lace sundress and straw hat poses under a bare dead tree whose branches are wrapped with pink toilet paper and pink plastic bags; shredded pink paper swirls around her, blown in from the left edge of the frame.",
         "The pink pig shown in <Picture 1> holds her dreamy pose; shredded pink paper swirls around her; a long streamer of pink toilet paper unrolls from a branch and flaps in the wind.",
         chapter="真相", sfx=[["recordscratch", 0.0], ["blower", 0.3, -6]]),
       S("s04-boyfriend", "Medium shot, locked", ["capy"], 2.8,
         "Medium shot in the grey scooter parking lot of the capybara boyfriend himself standing on top of a stepladder, holding a leaf blower aimed into an open cardboard box full of shredded pink paper, pink paper bits stuck all over his face, fur and green bucket hat, a power bank hanging from his neck, completely deadpan.",
         "The capybara shown in <Picture 1> holds the leaf blower into the box as pink shreds blast up and away; a pink paper bit lands on his nose; his whiskers twitch; his deadpan face does not change.",
         sfx=[["blower", 0.0, -4]]),
       S("s05-photo", "Insert, slow push in", ["fenfen"], 2.4,
         "The finished photo filling the vertical frame with a thin white photo border: Fenfen the pink pig in a white lace sundress and straw hat under a dreamy blooming cherry tree in a shower of petals, picture perfect like a magazine cover; among the pink blossoms in the tree crown, a deadpan capybara face in a green bucket hat covered in pink petals peeks out.",
         "The photo shown in <Picture 1> holds still; the capybara face among the blossoms slowly blinks once and a petal slides off his nose.",
         chapter="成品", sfx=[["shutter", 0.0]], cam=" The camera pushes in with small amplitude at slow speed."),
       S("s06-dump", "Medium shot, locked", ["fenfen"], 2.8,
         "Medium shot in the grey scooter parking lot of Fenfen the pink pig herself in her white lace sundress and straw hat, taking her dreamy profile pose again under the bare tree wrapped in pink toilet paper.",
         "The pink pig shown in <Picture 1> takes her dreamy pose; suddenly a huge mass of shredded pink paper dumps down on her from above the frame and buries her into a pink mound up to her snout; she stays frozen, smile unchanged.",
         sfx=[["whoosh", 0.2], ["thud", 0.7]], inn=0.5),
   ])

ep("piglet", 5, "螢火蟲美照的真相 #網美小豬",
   "每一張美照背後，都有一個面無表情的男友。本片畫面、配樂由 AI 生成。", "螢火蟲", "s04-boyfriend", "EP5〈螢火蟲之夜〉",
   "粉粉在夜晚森林裡被螢火蟲圍繞。拉遠：地下停車場，日光燈一閃一閃，螢火蟲是一串小燈泡，從一根釣竿垂下來；水豚男友站在梯子上舉著釣竿，燈串的線接在他脖子上的行動電源，蚊子繞著他飛。她重擺姿勢，整串燈掉下來纏在她身上，一顆一顆熄掉——行動電源沒電了。",
   PG_ROLES + "水豚男友脖子上的行動電源是這集的道具。",
   PG_VIEW + "EP5 題目由本批企劃，照系列公式；男友的固定配件行動電源第一次派上用場。",
   "螢火蟲圍繞 → 閃光一瞄 → 地下停車場的燈串釣竿 → 男友用行動電源供電、被蚊子叮 → 成品照樹林裡有水豚臉 → 燈串掉下來纏住她、一顆顆熄掉。",
   "夜裡的螢火蟲，有一隻吊在一條細線上。",
   [
       S("s01-fireflies", "Close-up, locked", ["fenfen"], 2.6,
         "Close-up at night of Fenfen the pink pig herself in a white lace sundress, a wide straw sun hat with a long pink satin ribbon and a pearl hair clip, a dreamy three-quarter profile smile, dozens of tiny glowing fireflies floating around her in soft focus in a dark forest; one glowing firefly near the corner visibly hangs from a thin string.",
         "The pink pig shown in <Picture 1> gazes dreamily at the glowing lights around her and slowly raises a hoof toward one; the light in the corner bobs up and down on its thin string.",
         chapter="美照"),
       S("s02-flash", "Medium close-up, locked", ["fenfen"], 2.0,
         "Medium close-up at night of Fenfen the pink pig herself in a white lace sundress and wide straw sun hat with a pink ribbon, frozen in a dreamy profile pose, tiny warm lights glowing around her.",
         "A bright camera flash fires once; the pink pig shown in <Picture 1> keeps her face frozen and only her eyes slowly slide to the lower right; one eyebrow twitches.",
         sfx=[["shutter", 0.15]]),
       S("s03-garage", "Wide shot, locked", ["fenfen"], 3.0,
         "Wide shot of a dim concrete underground parking garage at night with one flickering fluorescent tube, grey concrete pillars and an oil stain on the floor, no signs: Fenfen the pink pig herself in her white lace sundress and straw hat poses among three small potted plants; above her dangles a string of tiny warm fairy lights hanging from a long fishing line that reaches in from the top right of the frame.",
         "The pink pig shown in <Picture 1> holds her dreamy pose; the fairy lights dangle and swing slowly on the fishing line above her; the fluorescent tube flickers.",
         chapter="真相", sfx=[["recordscratch", 0.0], ["hum", 0.3]]),
       S("s04-boyfriend", "Medium shot, locked", ["capy"], 2.8,
         "Medium shot in the dim underground parking garage of the capybara boyfriend himself standing on a stepladder, holding a long fishing rod out toward the left edge of the frame with both front paws, a thin cable running from the rod to the glowing power bank hanging around his neck, his deadpan face lit from below, three mosquitoes circling his head.",
         "The capybara shown in <Picture 1> holds the fishing rod steady and gently jiggles it so the line bobs; a mosquito lands on his nose; one ear flicks; his deadpan face does not change.",
         sfx=[["hum", 0.0, -4]]),
       S("s05-photo", "Insert, slow push in", ["fenfen"], 2.4,
         "The finished photo filling the vertical frame with a thin white photo border: Fenfen the pink pig in a white lace sundress and straw hat in a magical night forest surrounded by glowing fireflies, picture perfect like a magazine cover; deep in the dark trees in the background, a deadpan capybara face in a green bucket hat glows, lit from below by a small light.",
         "The photo shown in <Picture 1> holds still; the glowing capybara face in the dark trees slowly blinks once.",
         chapter="成品", sfx=[["shutter", 0.0]], cam=" The camera pushes in with small amplitude at slow speed."),
       S("s06-tangle", "Medium shot, locked", ["fenfen"], 3.0,
         "Medium shot in the dim underground parking garage of Fenfen the pink pig herself in her white lace sundress and straw hat, taking her dreamy profile pose again among the potted plants, tiny warm fairy lights dangling above her.",
         "The pink pig shown in <Picture 1> takes her dreamy pose; suddenly the whole string of fairy lights drops from above and tangles over her hat and shoulders; the lights die one by one; she holds the pose, smile unchanged, under the flickering fluorescent tube.",
         sfx=[["whoosh", 0.2], ["powerdown", 1.0]], inn=0.5),
   ])

# ---------------------------------------------------------------- 社畜地獄
ep("shechu", 3, "聽到鈴鐺聲，全辦公室瞬間彈起來工作 #社畜地獄",
   "員工是狗，老闆是貓。本片畫面、配樂由 AI 生成。", "主管巡視", "s07-perch", "EP3〈主管巡視〉",
   "阿金腳翹在桌上射紙飛機偷懶；遠處傳來項圈鈴鐺聲，他耳朵一豎、彈起來瘋狂打字。鈴鐺聲的來源是一隻掛著鈴鐺的發條玩具老鼠，慢慢滾過走道。阿金鬆一口氣、腳又翹回桌上——一片陰影罩下來。隔板上方，項圈上沒有鈴鐺的喵總正低頭看著他，面無表情地把隔板上的釘書機推下去。",
   SH_ROLES,
   "零台詞；貓的天性：項圈鈴鐺（拿下鈴鐺，才能悄悄巡視）與把東西推下去。",
   "腳翹桌上射紙飛機 → 鈴鐺聲、耳朵一豎 → 瘋狂打字 → 鈴鐺在發條玩具老鼠上 → 腳又翹回去 → 陰影罩下來 → 隔板上沒鈴鐺的喵總推下釘書機。",
   "上班時間，黃金獵犬腳翹在桌上射紙飛機。",
   [
       S("s01-slack", "Medium shot, locked", ["ajin"], 2.6,
         "Medium shot of a grey office desk in a small office cubicle: A-Jin the Golden Retriever himself leans far back in his office chair in his white shirt and crooked tie, hind paws up on the desk, a paper airplane in his paw, the monitor turned away from the camera.",
         "The Golden Retriever shown in <Picture 1> lazily throws the paper airplane out of frame, yawns widely and stretches his arms behind his head.",
         chapter="偷懶"),
       S("s02-ears", "Close-up, locked", ["ajin"], 1.6,
         "Close-up of A-Jin the Golden Retriever himself leaning back in his office chair with his paws behind his head, relaxed half-closed eyes.",
         "The Golden Retriever shown in <Picture 1> suddenly opens his eyes wide and his ears shoot straight up; he freezes.",
         sfx=[["bell", 0.0]]),
       S("s03-work", "Medium shot, locked", ["ajin"], 2.2,
         "Medium shot of A-Jin the Golden Retriever himself sitting bolt upright at his grey desk, tie straightened, both paws on a keyboard, the monitor turned away from the camera, a frantic fake-focused face.",
         "The Golden Retriever shown in <Picture 1> types furiously on the keyboard with a frantic serious face, his ID card swinging, eyes darting left and right.",
         sfx=[["typing", 0.0]]),
       S("s04-toy", "Insert at floor level, locked", [], 2.0,
         "Insert at floor level of the grey office carpet aisle between desks: a small grey wind-up toy mouse wearing a tiny red collar with a golden bell rolls along the carpet, its wind-up key on its back.",
         "The wind-up toy mouse rolls slowly along the carpet across the frame, its key turning, the golden bell on its collar jingling.",
         chapter="鈴鐺", sfx=[["bell", 0.0, -4]]),
       S("s05-relax", "Medium shot, locked", ["ajin"], 2.4,
         "Medium shot of A-Jin the Golden Retriever himself at his grey desk, leaning back again in his office chair with his hind paws up on the desk and his front paws behind his head, a smug relieved grin.",
         "The Golden Retriever shown in <Picture 1> lets out a long relieved breath and settles deeper into the chair with a smug grin, wiggling his hind paws on the desk."),
       S("s06-shadow", "Close-up, locked", ["ajin"], 2.2,
         "Close-up of A-Jin the Golden Retriever himself leaning back in his office chair with a smug grin, a large dark shadow beginning to fall across his face from above.",
         "The Golden Retriever shown in <Picture 1> keeps grinning as the shadow slowly covers his face; his grin freezes; his eyes slowly roll upward; his ears flatten.",
         chapter="巡視", sfx=[["dun", 0.6]]),
       S("s07-perch", "Low-angle medium shot, locked", ["miaozong"], 3.0,
         "Low-angle medium shot of Boss Miao the orange tabby cat himself perched on top of a grey office cubicle partition in his grey suit, wearing a plain red collar with an empty ring and no bell, staring down at the camera with expressionless half-closed eyes; a stapler sits on the partition beside his paw.",
         "The cat shown in <Picture 1> stares down without blinking and slowly pushes the stapler off the edge of the partition with one paw; the stapler falls out of frame.",
         sfx=[["thud", 2.0]]),
   ])

ep("shechu", 4, "跟貓老闆談加薪，他只肯待在紙箱裡 #社畜地獄",
   "員工是狗，老闆是貓。本片畫面、配樂由 AI 生成。", "申請加薪", "s02-box", "EP4〈申請加薪〉",
   "阿金深呼吸、敲門要談加薪。喵總不坐大皮椅，整隻擠在辦公桌上一個小紙箱裡。阿金舉起畫著長條圖的報告、眼睛水汪汪；喵總慢慢沉進紙箱，只剩兩隻耳朵。隔天，阿金的椅子上放著一個綁紅色蝴蝶結的大紙箱——這就是他的「加薪」，他坐在裡面打電腦。最後，那個紙箱裡坐的換成了喵總。",
   SH_ROLES,
   "零台詞；貓的天性：紙箱（對貓來說紙箱就是最高獎賞，而且好紙箱一定會被老闆搶走）。",
   "敲門 → 老闆擠在紙箱裡 → 舉報告、水汪汪 → 老闆沉進紙箱 → 隔天的加薪是一個紙箱 → 紙箱被老闆搶走。",
   "大皮椅空著，胖橘貓老闆擠在桌上的小紙箱裡。",
   [
       S("s01-knock", "Medium shot, locked", ["ajin"], 2.4,
         "Medium shot of A-Jin the Golden Retriever himself standing in front of a glass office door in his white shirt and crooked tie, holding a plain folder against his chest, taking a deep nervous breath.",
         "The Golden Retriever shown in <Picture 1> takes a deep breath, straightens his tie, and knocks on the glass door three times with one knuckle.",
         chapter="加薪", sfx=[["knock", 1.2]]),
       S("s02-box", "Medium shot, locked", ["miaozong"], 2.8,
         "Medium shot of a boss's office: Boss Miao the orange tabby cat himself is squeezed inside a small cardboard box sitting on top of his big wooden desk, his grey suit jacket bulging over the edges, only his head and shoulders sticking out; his big black leather chair stands empty behind him.",
         "The cat shown in <Picture 1> stares at the camera from inside the cardboard box with half-closed eyes, then slowly blinks once.",
         chapter="紙箱", sfx=[["dun", 0.4, -6]]),
       S("s03-plead", "Medium close-up, locked", ["ajin"], 2.4,
         "Medium close-up of A-Jin the Golden Retriever himself holding up a sheet of paper with a simple hand-drawn rising bar chart with no words or numbers, big hopeful puppy eyes.",
         "The Golden Retriever shown in <Picture 1> holds up the bar chart, points eagerly at the tallest bar, and gives big pleading puppy eyes, tail wagging.",
         sfx=[["paper", 0.0, -6]]),
       S("s04-sink", "Medium shot, locked", ["miaozong"], 2.0,
         "Medium shot of Boss Miao the orange tabby cat himself inside the small cardboard box on his big wooden desk, only his head sticking out, expressionless.",
         "The cat shown in <Picture 1> slowly sinks down into the cardboard box until only his two ears stick out over the edge; the ears twitch once."),
       S("s05-gift", "Medium shot, locked", ["ajin"], 3.0,
         "Medium shot of A-Jin's grey office desk the next morning: A-Jin the Golden Retriever himself sits squeezed inside a big cardboard box placed on his office chair, a big red gift bow stuck on the front of the box, a laptop on his knees with its screen facing away, a confused but polite smile.",
         "The Golden Retriever shown in <Picture 1> sits in the box and types on the laptop; he glances down at the red bow, then back up at the camera with a confused polite smile.",
         chapter="隔天", sfx=[["paper", 0.0, -4]]),
       S("s06-steal", "Medium shot, locked", ["miaozong"], 2.6,
         "Medium shot of the same grey office desk: Boss Miao the orange tabby cat himself sits inside the big cardboard box with the red gift bow on the office chair, completely relaxed, eyes half closed; at the edge of the frame a golden retriever paw holds a laptop.",
         "The cat shown in <Picture 1> settles deeper into the box with a contented look, slowly closes his eyes and curls his tail over the edge.",
         sfx=[["dun", 1.6]]),
   ])

ep("shechu", 5, "午休回來，貓老闆睡在我的鍵盤上 #社畜地獄",
   "員工是狗，老闆是貓。本片畫面、配樂由 AI 生成。", "午休", "s04-keyboard", "EP5〈午休〉",
   "阿金的座位曬到一片暖暖的陽光，他伸個懶腰、抱著頸枕去午休。玻璃辦公室門邊，喵總的眼睛鎖定那片陽光。阿金回來，笑容垮下來：喵總四腳朝天睡在他的鍵盤上。阿金只好抱著筆電坐到印表機旁的冷角落，冷氣對著他吹。陽光慢慢移到他身上，他鬆了一口氣——辦公桌上，喵總睜開一隻眼，盯著那片陽光。",
   SH_ROLES,
   "零台詞；貓的天性：搶最暖的位置、坐鍵盤。",
   "座位曬太陽、去午休 → 喵總盯上陽光 → 阿金回來笑容垮掉 → 老闆睡在鍵盤上 → 阿金縮在冷角落 → 陽光移過來 → 老闆睜開一隻眼。",
   "黃金獵犬的座位被午後陽光曬得暖洋洋。",
   [
       S("s01-sun", "Medium shot, locked", ["ajin"], 2.6,
         "Medium shot of A-Jin the Golden Retriever himself at his grey office desk bathed in a warm beam of afternoon sunlight from the window, in his white shirt and crooked tie, holding a neck pillow, the monitor turned away from the camera.",
         "The Golden Retriever shown in <Picture 1> stretches happily in the warm sunbeam, tail wagging, tucks the neck pillow under his arm and walks out of frame to the left.",
         chapter="午休"),
       S("s02-sneak", "Close-up, locked", ["miaozong"], 2.2,
         "Close-up of Boss Miao the orange tabby cat himself peeking around the edge of his glass office door in his grey suit, eyes fixed on something bright off screen, warm light on his face.",
         "The cat shown in <Picture 1> stares without blinking; his pupils narrow to slits; his whiskers twitch and he slowly slides out from behind the door.",
         sfx=[["dun", 0.0, -6]]),
       S("s03-return", "Medium shot, locked", ["ajin"], 2.0,
         "Medium shot of A-Jin the Golden Retriever himself walking back into the office holding a neck pillow, a refreshed smile.",
         "The Golden Retriever shown in <Picture 1> walks in, stops dead, and stares down at his desk off screen; his smile drops and the neck pillow slips from his paw.",
         chapter="回來"),
       S("s04-keyboard", "Medium shot, locked", ["miaozong"], 3.0,
         "Medium shot of A-Jin's grey office desk in the warm sunbeam: Boss Miao the orange tabby cat himself is sprawled belly-up asleep across the keyboard in his grey suit, paws in the air, gold tie clip glinting, the monitor turned away from the camera.",
         "The cat shown in <Picture 1> sleeps belly-up on the keyboard in the sunbeam; his belly rises and falls; one hind paw twitches and presses the keys.",
         sfx=[["typing", 0.3, -10]]),
       S("s05-corner", "Wide shot, locked", ["ajin"], 2.6,
         "Wide shot of a dim cold office corner beside a grey printer: A-Jin the Golden Retriever himself sits on the floor with a laptop on his knees, its screen facing away, wearing the neck pillow, shivering under an air conditioner vent blowing down on him, his fur ruffled.",
         "The Golden Retriever shown in <Picture 1> shivers and types slowly on the laptop as the cold air ruffles his fur; he sniffles and hunches his shoulders.",
         chapter="角落", sfx=[["aircon", 0.0]]),
       S("s06-warm", "Close-up, locked", ["ajin"], 2.2,
         "Close-up of A-Jin the Golden Retriever himself sitting on the floor in the dim office corner wearing the neck pillow, a patch of warm sunlight creeping across the floor toward him.",
         "The Golden Retriever shown in <Picture 1> watches the warm patch of sunlight slide slowly onto his face; he closes his eyes with a relieved smile."),
       S("s07-eye", "Close-up, locked", ["miaozong"], 2.4,
         "Close-up of Boss Miao the orange tabby cat himself lying belly-up asleep on a keyboard in his grey suit, now in shade.",
         "The cat shown in <Picture 1> opens one eye, turns his head and stares fixedly toward the bright light off screen; his pupil narrows to a slit.",
         sfx=[["dun", 1.2]]),
   ])

for spec in EPISODES:
    shots = spec["shots"]
    total = sum(s["dur"] for s in shots)
    assert 5 <= len(shots) <= 7, spec["slug"]
    assert 13 <= total <= 18, (spec["slug"], total)
    assert sum(1 for s in shots if s.get("chapter")) >= 3, spec["slug"]
    assert len(spec["headline"]) <= 6, spec["slug"]
    assert spec["thumb"] in {s["id"] for s in shots}, spec["slug"]
    base_sfx = {f.stem for f in Path("/root/mokaair-work/videos", spec["base"], "edit/sfx").glob("*.wav")}
    for s in shots:
        for c in s.get("sfx", []):
            assert c[0] in base_sfx or c[0] in spec["sfx_extra"], (spec["slug"], s["id"], c[0])
            assert 0 <= c[1] < s["dur"], (s["id"], c)
        assert 1.4 <= s["dur"] <= 3.2, s["id"]
        assert len(s["chars"]) <= 1, s["id"]
        assert len(s["ff"]) <= 1000, (s["id"], len(s["ff"]))
        assert len(s["clip"]) <= 300, (spec["slug"], s["id"], len(s["clip"]))
        if s.get("sfx") is None:
            s.pop("sfx", None)
    (OUT / f"{spec['slug']}.json").write_text(json.dumps(spec, ensure_ascii=False, indent=1) + "\n")
    print(spec["slug"], len(shots), round(total, 1))
