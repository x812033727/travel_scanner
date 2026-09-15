"""Deterministic API packages; never include runtimes, keys or generated observations."""
import zipfile
from pathlib import Path

HERE=Path(__file__).resolve().parent
EX=HERE/"examples"
def members(folder):
    return [p for p in folder.rglob("*") if p.is_file() and "__pycache__" not in p.parts and p.name not in {".env"}]
shared=members(EX/"lablib")+[EX/"requirements.txt",EX/"README.md"]
groups=[(f"lesson-{n}.zip",members(EX/str(n))+shared,EX) for n in range(81,87)]
groups.append(("api-verification.zip",[p for n in range(81,87) for p in members(EX/str(n))]+shared+[HERE/"verification/test_materials.py",HERE/"verification/README.md"],HERE))
for name,files,base in groups:
    with zipfile.ZipFile(EX/name,"w",zipfile.ZIP_DEFLATED) as archive:
        for file in sorted(files):
            info=zipfile.ZipInfo(file.relative_to(base).as_posix(),(2026,9,14,0,0,0))
            info.compress_type=zipfile.ZIP_DEFLATED
            archive.writestr(info,file.read_bytes())
print("Seven API packages created; no live outputs included.")

