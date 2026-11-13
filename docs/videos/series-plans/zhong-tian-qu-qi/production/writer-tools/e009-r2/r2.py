"""Episode 9 live-action remake specification (EP = 909 -> zhong-tian-qu-qi-e009-r2).

Strictly implements docs/videos/zhong-tian-qu-qi-e009-r2/script.md (including 2026-11-06 review fixes)
with all live-action rules from RULES.md, REVIEW.md, pilot.py, and preflight-prompts.py.
"""
from s01_19 import SHOTS_1
from s20_38 import SHOTS_2

EP = 909
SLUG = "zhong-tian-qu-qi-e009-r2"
EP_TITLE = "洞房夜三扇門（重製版 r2）"
OUTLINE_SECONDS = 197.5
TARGET_MINUTES = [3, 4]
TITLE = "洞房夜三扇門，她半夜塞出一床厚被｜種田娶妻打天下 第9集（重製版）"
DESCRIPTION = (
    "第四天夜裡，許硯三人騎著鏢局的馬回到許家院子。小禾舉著燭台擋在走廊上，不准他再躲去睡柴房，三扇門自己選一扇。"
    "第一扇門裡唐小棠要他先把三本帳對完，許硯不碰算盤心算出二十兩一錢、還抓出一筆錯帳，唐小棠好感 +2，卻又搬出十本帳冊；"
    "許硯推說明天再對溜出門。第二扇門窗開人不在，他替秦霜關上窗。第三扇門一推開，阿令亮出短刃戒備；"
    "許硯看見她手腕舊痕卻不追問，退到門外走廊鋪地鋪守門，阿令收刃丟出一條厚棉被，好感 +10，隱藏任務完成。"
    "夜深時，阿令隔著門板輕聲說：明天，我可能得走。《種田娶妻打天下》第 9 集（重製版）。"
)
THUMB = ("洞房夜三扇門", "s24")
CHARACTERS = ["xuyan", "xiaohe", "tangxiaotang", "aling", "qinshuang", "xitong"]
MINOR = {}
MUSIC = (
    "one cue per scene: first a light playful plucked-string and bamboo-flute comedy cue in the night corridor and Tang Xiaotang's candlelit room, "
    "dropping a beat on the affection chime and pausing under the system's dry remark; second a low tense suspense cue of sparse guqin and low strings "
    "at the empty room and A-ling's dark doorway with one sharp accent at s24, shifting from s32 to quiet warm strings that thin to a single soft string "
    "under A-ling's parting line in s37 and fade on s38; ancient Chinese period drama, no vocals"
)

# Careful with gen-dh.mjs SET regexes: ONLY yard_night matches dh-set-xujia-yuan-t1 (mapped to set-xujia-yuan-l2.png).
# Corridor, Tang's room, Qin's room, and A-ling's room use text-only night descriptions (avoid "mud wall", "courtyard",
# "inside the room", "farmhouse interior", "work shed", "kitchen" so gen-dh attaches ZERO daytime interior plates).
LOC = {
    "yard_night": (
        "In the dirt yard of the Xu farmhouse on a clear autumn night: a bamboo fence and open wooden gate on screen right with one plain blank paper lantern "
        "with no marks or writing glowing warm orange beside the gatepost, the dark eaves and open doorway of the main house on the back left with only darkness "
        "inside, a timber horse shed at the far back left, the night sky above pitch-black with no daylight anywhere, lit by cold blue moonlight and the warm gate lantern"
    ),
    "corridor": (
        "In a narrow roofed wooden corridor of an ancient Song-dynasty rural dwelling on a pitch-dark autumn night: dark timber pillars on the left with black night beyond "
        "and no daylight anywhere, plain earthen plaster wall and three closed plain unpainted wooden doors with no marks or writing in a row on screen right, "
        "lit by faint cold blue moonlight and thin warm candlelight seeping from the door cracks"
    ),
    "corridor_c": (
        "In a narrow roofed wooden corridor at night, plain dark earthen plaster wall behind, lit by warm flickering candlelight and faint cold blue moonlight, no daylight anywhere"
    ),
    "tang": (
        "In a warm candlelit rural Song-dynasty bridal bedroom at night: a plain wooden door on screen left with dark night corridor beyond and no daylight anywhere, "
        "a wooden table on screen right with a bed and plain dark curtains behind it, blank plain white window paper with dark night outside, lit by warm yellow candlelight"
    ),
    "tang_c": (
        "In a warm candlelit rural Song-dynasty bridal bedroom at night, dark night outside with no daylight anywhere, lit by warm yellow candlelight"
    ),
    "qin": (
        "In a quiet dark rural Song-dynasty bedroom late at night: an empty wooden bed with neatly folded bedding, an open wooden casement window with blank plain white "
        "window paper looking out onto pitch-dark night with no daylight anywhere, an empty wooden rack on the earthen plaster wall, and one flickering white candle on a small table, "
        "lit by cold blue moonlight through the window and faint wavering candlelight"
    ),
    "aling": (
        "In a very dim rural Song-dynasty bedroom late at night: a plain unpainted wooden door on screen left, a simple wooden bed on screen right and one small lit white candle "
        "on a low stand beside the bed, dark shadows in the corners and pitch-dark night outside with no daylight anywhere, lit only by that single warm candle flame"
    ),
    "aling_c": (
        "In a very dim rural Song-dynasty bedroom late at night, dark earthen plaster wall in deep shadow behind, lit only by a single warm flickering candle flame, no daylight anywhere"
    ),
    "threshold": (
        "Right outside the plain unpainted wooden doorway of a bedroom in the roofed wooden corridor late on a pitch-dark autumn night: wooden threshold and plain door planks, "
        "black night beyond the corridor pillars with no daylight anywhere, lit by cold blue moonlight outside and faint warm candlelight through the doorway"
    ),
}

LIGHT = {
    "yard_night": "the cold blue moonlight and the warm orange lantern glow stay unchanged",
    "corridor": "the faint cold moonlight and warm candlelight along the door cracks stay unchanged",
    "candle": "the warm yellow candlelight stays unchanged",
    "qin": "the cold blue moonlight from the open window and the low wavering candlelight stay unchanged",
    "qin_close": "the cold blue moonlight and the candle flame steadying upright stay natural",
    "aling": "the dim warm light of the single candle in the dark room stays unchanged",
    "threshold": "the cold blue moonlight in the night corridor stays unchanged",
}

SHOTS = SHOTS_1 + SHOTS_2

HEAD = [
    "- 重製版 r2：嚴格照 `docs/videos/zhong-tian-qu-qi-e009-r2/script.md`（c01–c38 對應 s01–s38，含 2026-11-06 審稿修改）；開頭不放集數、不放片名卡，s01 直接接第 8 集 s40（阿令在院門燈籠下望村路）。",
    "- 內部工作編號 909（`hailuo/*-dh-e909.json`、`colab/runs/e909-live/`）；發布 slug `zhong-tian-qu-qi-e009-r2`。",
    "- 角色與道具連戲：s01 只送三個具名角色（許硯、唐小棠、阿令）加 `set-xujia-yuan-l2`，秦霜只拍深褐短衣高馬尾背影牽馬去左後馬棚（避免超過三人撞臉複製）；小禾草編兔子改塞在腰帶上（`spec.json` 替換 `cast.json` 原句），雙手空出來拿銅燭台與推人；許硯雙肩布料完整（`both shoulders whole`），s03 抱起鋪蓋、s08 放門邊與放燭台、s18 留燭台在桌上只抱鋪蓋離開（s19 起手上無燭台）、s25 鋪蓋滑落、s29 撿起、s31 攤在門外走廊；阿令全程無鐵鐐，s24–s32 短刃固定在左手正握、s32 垂於身側尖朝地、s37 平放膝上，左手腕內側發白舊痕於 s26 露出、s28 右手拉左袖蓋住；帳冊封面一律空白無字，攤開帳頁一律虛焦無字（s10、s13）；s34 眼睛大特寫寫自然深褐瞳孔與極小反光點（禁寫藍光發光瞳孔）。",
    "- 夜景與場景圖紀律：僅 s01 掛 `set-xujia-yuan-l2`；走廊、唐小棠房、秦霜房、阿令房全部純文字描述（`sets {'dh-set-xujia-yuan': 1, 'NONE': 37}`，絕不誤掛白天屋內場景圖），所有門外、窗外與夜空寫明全黑無日光。",
]

FOOT = [
    "- 真人版收音規則：畫面中露嘴說話的台詞使用 H3 草稿原聲（`clip_voice: true`），系統音（s16、s19、s33、s34、s36）、畫外台詞（s05、s10、s18 第二句、s21）與許硯閉嘴內心獨白（s35）使用 Gemini TTS 錄音；s37 阿令隔門說話視草稿原聲品質套悶音濾波（低通）。",
    "- 好感帳核對：接第 8 集（唐小棠 13、秦霜 10、阿令 1）→ s16 唐小棠 +2 → 15；s33 阿令 +10 → 11；s34 隱藏任務完成。",
]

BUY = {
    "s02": 8,
    "s03": 8,
    "s07": 8,
    "s08": 8,
    "s10": 6,
    "s13": 8,
    "s14": 6,
    "s17": 8,
    "s18": 10,
    "s19": 8,
    "s20": 8,
    "s21": 6,
    "s22": 8,
    "s23": 8,
    "s24": 8,
    "s26": 6,
    "s29": 8,
    "s31": 8,
    "s32": 8,
    "s33": 6,
    "s34": 6,
    "s35": 6,
    "s36": 6,
    "s37": 8,
    "s38": 6,
}
