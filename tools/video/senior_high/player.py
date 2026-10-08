"""Offline English Lab player with independent voice and translated CC controls."""
from __future__ import annotations

import json
from pathlib import Path
import re

from senior_high.shared import player as shared_player

SEASON_NAMES = {
    1: "精確表達", 2: "組織段落", 3: "觀點與證據",
    4: "批判閱讀與跨情境溝通", 5: "整合閱讀與寫作", 6: "大學銜接與學術溝通",
}
GRADE_BANDS = {1: "高一", 2: "高一", 3: "高二", 4: "高二", 5: "高三", 6: "高三"}


def write_player(resolved: dict, output: Path) -> Path:
    template = shared_player._PAGE
    replacements = {
        "幼兒英文 __EPISODE_COUNT__ 集": "高中英文 · __EPISODE_COUNT__ 集",
        "Sunny 與 Pip 的英文小花園": "English Lab · Sunny &amp; Pip",
        "PRESCHOOL · __EPISODE_COUNT__ LESSONS": "SENIOR HIGH · __EPISODE_COUNT__ LESSONS",
        "LITTLE STEPS, HAPPY LEARNING": "ENGLISH LAB / SENIOR HIGH",
        "小小英語，<span>一起開口。</span>": "讀懂觀點，<span>寫出有據的表達。</span>",
        "聽一聽、說一說，和孩子一起開始英文小冒險。": "從精確句型到閱讀分析、證據整合與學術溝通，練習清楚而有分寸的表達。",
        "幼兒啟蒙": "高一・高二・高三",
        "今天一起學什麼？": "選擇你的學習主題",
        "跟著孩子的步調，一次看一集就好。<br>想再聽一次，隨時暫停或重播。": "依先備能力選擇進度；聽讀跟說後，分析短文並完成有字數目標的寫作練習。<br>需要思考時，可以暫停或重播。",
        "陪伴學習": "自主學習",
        "這一集的小目標": "本集學習目標",
        "和孩子一起玩": "自學提醒",
        'id="parent-tip"': 'id="study-tip"',
        "$('parent-tip')": "$('study-tip')",
        'font-family:ui-rounded,': 'font-family:ui-sans-serif,',
        "--ink:#243d35;--muted:#69776c;--cream:#faf7ed;--mint:#dcebdc;--green:#2b6150;--line:#dfdfd0;--white:#fffef8;--yellow:#f5d984;--orange:#d27950":
        "--ink:#20314b;--muted:#64748b;--cream:#f4f6fa;--mint:#e2ebf4;--green:#246e82;--line:#d9e0eb;--white:#ffffff;--yellow:#f3cf76;--orange:#b05f38",
    }
    for original, replacement in replacements.items():
        if original not in template:
            raise ValueError(f"Shared player template changed; review senior-high branding: {original}")
        template = template.replace(original, replacement)
    names = json.dumps({season: f"第 {season} 季・{GRADE_BANDS[season]}・{name}"
                        for season, name in SEASON_NAMES.items()}, ensure_ascii=False)
    template, changed = re.subn(r"const seasonNames = \{[^\n]+\};", f"const seasonNames = {names};", template)
    if changed != 1:
        raise ValueError("Shared player season selector changed; review senior-high template")
    # Replace the nursery illustration with a quiet editorial subject mark.
    artwork = ('<div class="hero-art lab-mark" aria-hidden="true"><span>ENGLISH</span>'
               '<strong>Lab.</strong><small>READ / THINK / EXPRESS</small></div>')
    template, changed = re.subn(r'<svg class="hero-art".*?</svg>', artwork, template, count=1, flags=re.S)
    if changed != 1:
        raise ValueError("Shared player hero changed; review senior-high template")
    template = template.replace('</style>', '''
.lab-mark{border-left:3px solid var(--green);padding:12px 0 12px 23px;color:var(--ink)}
.lab-mark span,.lab-mark small{display:block;font-size:10px;letter-spacing:.13em;font-weight:700}
.lab-mark strong{display:block;font-size:55px;line-height:1.18;letter-spacing:-.04em}
.lab-mark small{font-size:8px;color:var(--muted);margin-top:7px}
.main-card,.learning article{border-radius:12px}.brand-mark{border-radius:7px}.tag{border-radius:5px}
.screen,.screen video{background:#e7edf5}.episode-card{border-radius:9px;background:#fff}
.episode-card:hover,.episode-card[aria-current=true]{background:#edf4f8}.learning article{background:#edf1f7}
.practice-link{margin:0 0 18px;font-size:13px}.practice-link a{margin-right:18px}
@media(max-width:650px){.lab-mark{padding-left:12px}.lab-mark strong{font-size:38px}.lab-mark small{font-size:6px}}
</style>''')
    template = template.replace('  </main>', '<p class="practice-link"><a href="Practice.html">獨立閱讀與寫作練習</a><a href="Practice.pdf">下載練習 PDF</a></p>\n  </main>')
    # The shared adapter retains its stable JSON key; every displayed tip is for learners.
    episodes = [{**episode, "parent_tip_zh_TW": episode.get("parent_tip_zh_TW") or
                 "先辨認主張與證據，再檢查推論的範圍；寫作後回看任務要求並修訂。"}
                for episode in resolved.get("episodes", [])]
    return shared_player.write_player({**resolved, "episodes": episodes}, output, page_template=template)
