"""Match all delivered ZIP bytes and execute the validators from an extracted package."""
import hashlib
import json
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path, PurePosixPath

HERE = Path(__file__).resolve().parent
packages = []
for source in sorted((HERE / "examples").glob("*.zip")):
    with zipfile.ZipFile(source) as archive:
        assert archive.testzip() is None, source.name
        names = archive.namelist()
        assert len(names) == len(set(names)), "duplicate_members"
        base = HERE if source.name == "research-verification.zip" else HERE / "examples"
        for name in names:
            relative = PurePosixPath(name)
            assert not relative.is_absolute() and ".." not in relative.parts
            assert not any(part in {".venv", "__pycache__", ".git", ".env"} for part in relative.parts)
            assert archive.read(name) == (base / name).read_bytes(), name
        packages.append({"file": source.relative_to(HERE).as_posix(), "members": len(names), "sha256": hashlib.sha256(source.read_bytes()).hexdigest(), "crc": "passed", "sourceBytes": "matched"})
assert len(packages) == 7, "expected_seven_packages"
with tempfile.TemporaryDirectory(prefix="gemini-research-delivery-") as temporary:
    with zipfile.ZipFile(HERE / "examples/research-verification.zip") as archive:
        archive.extractall(temporary)
    result = subprocess.run([sys.executable, "-X", "utf8", "verification/test_materials.py"], cwd=temporary, capture_output=True, text=True, encoding="utf-8", timeout=60, check=False)
    assert result.returncode == 0, result.stdout + result.stderr
    tests = json.loads((Path(temporary) / "verification/fixtures.json").read_text(encoding="utf-8"))
receipt = {"checkedOn": "2026-09-14", "packages": packages, "extractedFixtureTests": tests, "modelCalls": 0, "mediaGenerations": 0, "publication": "unpublished"}
(HERE / "verification/delivery.json").write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
print(json.dumps({"packages": len(packages), "extractedTests": tests["tests"], "success": tests["success"]}))
