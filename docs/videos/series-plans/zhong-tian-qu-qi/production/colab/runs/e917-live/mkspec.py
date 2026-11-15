import json
from pathlib import Path
spec = {"seeds": [9171101, 9171102], "shots": {f"s{n:02d}": {} for n in range(1, 41)}}
Path(__file__).with_name("spec.json").write_text(json.dumps(spec, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
