"""Create a reproducible learner ZIP. No network, credentials, or source mutation."""
from pathlib import Path
import argparse
import zipfile

parser = argparse.ArgumentParser()
parser.add_argument("source", type=Path)
parser.add_argument("destination", type=Path)
args = parser.parse_args()
source = args.source.resolve(strict=True)
args.destination.parent.mkdir(parents=True, exist_ok=True)
with zipfile.ZipFile(args.destination, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
    for item in sorted(source.rglob("*")):
        if not item.is_file():
            continue
        if item.is_symlink():
            raise ValueError(f"Symlinks are not learner artifacts: {item.name}")
        name = item.relative_to(source).as_posix()
        entry = zipfile.ZipInfo(name, date_time=(2026, 10, 11, 0, 0, 0))
        entry.compress_type = zipfile.ZIP_DEFLATED
        entry.external_attr = 0o100644 << 16
        archive.writestr(entry, item.read_bytes())
