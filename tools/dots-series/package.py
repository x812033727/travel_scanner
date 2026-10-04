"""Package synthetic course inputs and authoring handoff; never generate media or publish."""
from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

from files import copy_text_lf, digest, dumps, scoped, tree_files, write_text_lf

ROOT = Path(__file__).resolve().parents[2]


def package(workspace: Path, *, repo: Path = ROOT, install_downloads: bool = False) -> dict:
    workspace, repo = workspace.resolve(), repo.resolve()
    if workspace.is_relative_to(repo):
        raise ValueError("Authoring and production originals must stay outside the repository")
    archives, authoring = [], []
    # Complete the source and destination boundary preflight before any ZIP/copy.
    source_files = [path for name in ("lessons", "videos", "examples") for path in tree_files(workspace / name, workspace)]
    output_root = scoped(workspace / "build-authoring", workspace, workspace / "build-authoring")
    downloads = scoped(workspace / "assets/dots-course/downloads", workspace, workspace / "assets")
    exercise_files = {}
    for number in range(11, 17):
        directory = workspace / "examples" / str(number)
        paths = tree_files(directory, workspace)
        if len(paths) < 2:
            raise ValueError(f"Application {number}: authored initial and changed inputs are required")
        exercise_files[number] = paths
    archive_paths = {number: scoped(downloads / f"lesson-{number:02}.zip", workspace, downloads) for number in exercise_files}
    handoff_paths = {source: scoped(output_root / source.relative_to(workspace), workspace, output_root) for source in source_files}
    manifest_path = scoped(output_root / "manifest.json", workspace, output_root)
    public_paths = {number: scoped(repo / "apps/web/public/dots-course/downloads" / destination.name,
                                   repo, repo / "apps/web/public/dots-course/downloads")
                    for number, destination in archive_paths.items()} if install_downloads else {}
    for number, paths in exercise_files.items():
        destination = archive_paths[number]
        destination.parent.mkdir(parents=True, exist_ok=True)
        directory = workspace / "examples" / str(number)
        with ZipFile(destination, "w", compression=ZIP_DEFLATED) as archive:
            for path in paths:
                entry = ZipInfo(f"lesson-{number:02}/" + path.relative_to(directory).as_posix(), (2026, 10, 3, 0, 0, 0))
                entry.compress_type = ZIP_DEFLATED
                entry.external_attr = 0o644 << 16
                archive.writestr(entry, path.read_bytes())
        record = {"number": number, "path": destination.relative_to(workspace).as_posix(), "sha256": digest(destination), "files": len(paths), "state": "synthetic-practice-input"}
        archives.append(record)
        if install_downloads:
            public = public_paths[number]
            public.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(destination, public)
    for source, target in handoff_paths.items():
        target.parent.mkdir(parents=True, exist_ok=True)
        if source.suffix in {".md", ".txt", ".csv", ".json", ".ics", ".py"}:
            copy_text_lf(source, target)
        else:
            shutil.copyfile(source, target)
        authoring.append({"path": source.relative_to(workspace).as_posix(), "sha256": digest(source),
                          "output_sha256": digest(target)})
    manifest = {"version": 1, "state": "authored-inputs", "published": False, "media_generated": False, "installed_downloads": install_downloads,
                "downloads": archives, "authoring": authoring, "output": str(workspace / "build-authoring")}
    write_text_lf(manifest_path, dumps(manifest))
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", required=True, type=Path)
    parser.add_argument("--repo", default=ROOT, type=Path)
    parser.add_argument("--install-downloads", action="store_true", help="Install only the six synthetic exercise ZIPs")
    args = parser.parse_args()
    try:
        print(dumps(package(args.workspace, repo=args.repo, install_downloads=args.install_downloads)), end="")
        return 0
    except (OSError, ValueError) as error:
        print(json.dumps({"state": "blocked", "published": False, "error": str(error)}))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
