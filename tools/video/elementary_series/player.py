"""Offline player for all elementary grades, including isolated season ZIPs."""
from __future__ import annotations

import json
from pathlib import Path
import re

from elementary_series.shared import player as shared_player

SEASON_NAMES = {
    1: "我的英文教室", 2: "我的單字與一天", 3: "人物與地方",
    4: "日子與計畫", 5: "故事與理由", 6: "閱讀寫作與分享",
}
GRADE_BANDS = {1: "低年級", 2: "低年級", 3: "中年級", 4: "中年級", 5: "高年級", 6: "高年級"}


def write_player(resolved: dict, output: Path) -> Path:
    template = shared_player._PAGE
    replacements = {
        "幼兒英文 __EPISODE_COUNT__ 集": "國小英文 · __EPISODE_COUNT__ 集",
        "Sunny 與 Pip 的英文小花園": "Sunny 與 Pip 的英文教室",
        "PRESCHOOL · __EPISODE_COUNT__ LESSONS": "ELEMENTARY ENGLISH · __EPISODE_COUNT__ LESSONS",
        "LITTLE STEPS, HAPPY LEARNING": "LISTEN, READ, WRITE, AND SHARE",
        "小小英語，<span>一起開口。</span>": "從一句話，<span>說到小故事。</span>",
        "聽一聽、說一說，和孩子一起開始英文小冒險。": "跟 Sunny 和 Pip 從教室對話，走向閱讀、寫作與分享。",
        "幼兒啟蒙": "國小低・中・高年級",
    }
    for original, replacement in replacements.items():
        if original not in template:
            raise ValueError(f"Shared player template changed; review elementary branding: {original}")
        template = template.replace(original, replacement)
    names = json.dumps({season: f"第 {season} 季・{GRADE_BANDS[season]}・{name}"
                        for season, name in SEASON_NAMES.items()}, ensure_ascii=False)
    template, changed = re.subn(r"const seasonNames = \{[^\n]+\};", f"const seasonNames = {names};", template)
    if changed != 1:
        raise ValueError("Shared player season selector changed; review elementary template")
    return shared_player.write_player(resolved, output, page_template=template)
