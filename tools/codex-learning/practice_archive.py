"""Package existing exercise sources without regenerating their intentional defects."""

import argparse
import hashlib
import json
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

ROOT = Path(__file__).resolve().parents[2]
TEXT_SUFFIXES = {".html", ".css", ".js", ".mjs", ".md"}


def package_practice(source: Path, archive_path: Path, manifest_path: Path) -> int:
    files = {
        path.relative_to(source).as_posix(): path.read_bytes().replace(b"\r\n", b"\n")
        for path in sorted(source.rglob("*"), key=lambda path: path.relative_to(source).as_posix())
        if path.is_file() and path.suffix in TEXT_SUFFIXES
    }
    if not files:
        raise ValueError(f"No exercise sources found in {source}")
    archive_path.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(archive_path, "w", ZIP_DEFLATED, compresslevel=9) as archive:
        for name, content in files.items():
            info = ZipInfo(f"codex-practice/{name}", date_time=(2026, 9, 15, 0, 0, 0))
            info.compress_type = ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            archive.writestr(info, content, compresslevel=9)
    manifest = {name: hashlib.sha256(content).hexdigest() for name, content in files.items()}
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8", newline="\n")
    return len(files)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=ROOT / "docs/codex-learning/practice")
    parser.add_argument(
        "--archive", type=Path,
        default=ROOT / "apps/web/public/guides/codex-first-project/todo-practice.zip",
    )
    parser.add_argument("--manifest", type=Path)
    args = parser.parse_args()
    count = package_practice(
        args.source, args.archive, args.manifest or args.source / "manifest.json"
    )
    print(f"Packaged {count} existing files with LF line endings: {args.archive.name!a}")


if __name__ == "__main__":
    main()
