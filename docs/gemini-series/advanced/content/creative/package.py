"""Package authored materials deterministically, excluding runtime caches and sidecars."""
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
EX = HERE / "examples"
checker = EX / "creative_checks.py"


def members(n):
    return [p for p in (EX / str(n)).rglob("*") if p.is_file() and "__pycache__" not in p.parts and not p.name.endswith(".inspect.ndjson")]


groups = [(f"lesson-{n}.zip", members(n) + [checker], EX) for n in range(63, 69)]
groups.append(("creative-verification.zip", [p for n in range(63, 69) for p in members(n)] + [checker, HERE / "verification/test_materials.py", HERE / "verification/README.md"], HERE))
for name, files, base in groups:
    with zipfile.ZipFile(EX / name, "w", zipfile.ZIP_DEFLATED) as archive:
        for file in sorted(files):
            info = zipfile.ZipInfo(file.relative_to(base).as_posix(), (2026, 9, 14, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, file.read_bytes())
print("Seven creative exercise archives built; actual Gemini/Flow outputs remain pending.")
