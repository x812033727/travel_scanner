"""The shared offline player with elementary-specific course branding."""
from __future__ import annotations

import json
from pathlib import Path
import re

from elementary.shared import player as shared_player

SEASON_NAME = "我的英文教室"


def write_player(resolved: dict, output: Path) -> Path:
    # Adapt the trusted template before embedding any authored episode strings.
    template = shared_player._PAGE
    replacements = {
        "幼兒英文 __EPISODE_COUNT__ 集": "國小低年級英文第一季 · __EPISODE_COUNT__ 集",
        "Sunny 與 Pip 的英文小花園": "Sunny 與 Pip 的英文教室",
        "PRESCHOOL · __EPISODE_COUNT__ LESSONS": "ELEMENTARY · SEASON 1 · __EPISODE_COUNT__ LESSONS",
        "LITTLE STEPS, HAPPY LEARNING": "OUR FIRST ENGLISH CLASSROOM",
        "小小英語，<span>一起開口。</span>": "走進教室，<span>開口說英文。</span>",
        "聽一聽、說一說，和孩子一起開始英文小冒險。": "跟 Sunny 和 Pip 練習教室對話，從聽懂到自己說一句。",
        "幼兒啟蒙": "國小低年級 · 6–8 歲",
    }
    for original, replacement in replacements.items():
        if original not in template:
            raise ValueError(f"Shared player template changed; review elementary branding: {original}")
        template = template.replace(original, replacement)
    names = json.dumps({1: f"第 1 季・{SEASON_NAME}"}, ensure_ascii=False)
    template, changed = re.subn(r"const seasonNames = \{[^\n]+\};", f"const seasonNames = {names};", template)
    if changed != 1:
        raise ValueError("Shared player season selector changed; review elementary template")
    return shared_player.write_player(resolved, output, page_template=template)
