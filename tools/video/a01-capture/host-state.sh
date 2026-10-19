#!/usr/bin/env bash
# Sent over plink stdin. Every operation below is read-only.
set -euo pipefail
cd /root/travel_scanner
release_sha=$(git rev-parse HEAD)
tools_tree_sha=$(git rev-parse HEAD:tools/video)
container_id=$(docker compose -f docker-compose.prod.yml --profile video ps -q video-worker)
test -n "$container_id"
worker_image_id=$(docker inspect --format '{{.Image}}' "$container_id")
[[ "$worker_image_id" =~ ^sha256:[a-f0-9]{64}$ ]]
printf 'GIT %s\n' "$release_sha"
if test -e /root/travel-scanner-deploy.hold; then
  printf 'DEPLOY_HOLD present\n'
else
  printf 'DEPLOY_HOLD absent\n'
fi
# ops/video/Dockerfile executes python3 during its image build. The video-worker
# image does not provide an unversioned `python` command in PATH.
docker compose -f docker-compose.prod.yml --profile video exec -T \
  -e "A01_RELEASE_SHA=$release_sha" \
  -e "A01_TOOLS_VIDEO_TREE_SHA=$tools_tree_sha" \
  -e "A01_WORKER_IMAGE_ID=$worker_image_id" \
  video-worker python3 - <<'PY'
import hashlib
import json
import os
import re
from pathlib import Path

slug = "story-rolling-suitcase-v2"
docs = Path("/opt/mokaair/docs/videos")
work = Path("/var/lib/mokaair/video-work")
episode = work / slug
audit = episode / "story/recheck-audit"
lexicon = docs / slug / "story-lexicon"

def reject_linked_ancestors(path):
    if any(part.is_symlink() for part in (path, *path.parents)):
        raise RuntimeError("symlink in capture source path")

def record(path):
    reject_linked_ancestors(path)
    if not path.is_file():
        if path.exists():
            raise RuntimeError("non-file in capture allowlist")
        return {"present": False, "sha256": None, "bytes": None}
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return {"present": True, "sha256": digest.hexdigest(), "bytes": path.stat().st_size}

reject_linked_ancestors(audit)
if not audit.is_dir():
    raise RuntimeError("audit directory missing or linked")
events = []
for entry in sorted(audit.iterdir(), key=lambda item: item.name):
    if entry.is_symlink() or not entry.is_dir():
        raise RuntimeError("unexpected audit entry")
    events.append({"name": entry.name, "index": record(entry / "index.json")})
if len(events) < 104 or any(not event["index"]["present"] for event in events):
    raise RuntimeError("audit has fewer than 104 complete indexes")
audit_files = {}
for entry in sorted(audit.rglob("*"), key=lambda item: str(item)):
    if entry.is_symlink():
        raise RuntimeError("linked audit member")
    if entry.is_file():
        if entry.suffix != ".json":
            raise RuntimeError("non-JSON audit member")
        audit_files[str(entry.relative_to(audit))] = record(entry)
    elif not entry.is_dir():
        raise RuntimeError("special audit member")

reject_linked_ancestors(lexicon)
if not lexicon.is_dir():
    raise RuntimeError("story lexicon snapshot missing or linked")
lexicon_files = {}
lexicon_dirs = set()
for entry in sorted(lexicon.rglob("*"), key=lambda item: str(item)):
    if entry.is_symlink():
        raise RuntimeError("linked story lexicon member")
    relative = entry.relative_to(lexicon).as_posix()
    if entry.is_dir():
        if relative not in {"events", "versions"}:
            raise RuntimeError("unexpected story lexicon directory")
        lexicon_dirs.add(relative)
    elif entry.is_file():
        if relative != "current.json" and not re.fullmatch(
            r"(?:events|versions)/[a-f0-9]{64}\.json", relative
        ):
            raise RuntimeError("unexpected story lexicon file")
        lexicon_files[f"docs/videos/{slug}/story-lexicon/{relative}"] = record(entry)
    else:
        raise RuntimeError("special story lexicon member")
if lexicon_dirs != {"events", "versions"} or not any(
    name.endswith("/current.json") for name in lexicon_files
) or not any("/events/" in name for name in lexicon_files) or not any(
    "/versions/" in name for name in lexicon_files
):
    raise RuntimeError("story lexicon snapshot incomplete")

required = {
    "docs/videos/lexicon.json": docs / "lexicon.json",
    f"docs/videos/{slug}/series.json": docs / slug / "series.json",
    f"docs/videos/{slug}/video.json": docs / slug / "video.json",
    f"docs/videos/{slug}/claims.md": docs / slug / "claims.md",
    f"docs/videos/{slug}/script.md": docs / slug / "script.md",
    f"{slug}/auto.json": episode / "auto.json",
    f"{slug}/review/narrative.json": episode / "review/narrative.json",
}
for chapter in ("hook", "origin", "idea", "engine", "turn", "now"):
    required[f"{slug}/story/chapters/{chapter}.json"] = episode / "story/chapters" / f"{chapter}.json"
files = {name: record(path) for name, path in required.items()}
if any(not item["present"] for item in files.values()):
    raise RuntimeError("required A01 source file missing")
optional = {
    f"docs/videos/{slug}/verify-1.md": docs / slug / "verify-1.md",
    f"{slug}/story/reviews/script-review.json": episode / "story/reviews/script-review.json",
}
files.update({name: record(path) for name, path in optional.items()})
controls = {
    "global_stop": record(work / "STOP"),
    "a01_stop": record(episode / "STOP"),
    "a01_lease": record(episode / "LEASE"),
}
worker = {
    "story_mjs": record(Path("/opt/mokaair/tools/video/automation/story.mjs")),
    "narrative_mjs": record(Path("/opt/mokaair/tools/video/core/narrative.mjs")),
}
if any(not item["present"] for item in worker.values()):
    raise RuntimeError("worker code file missing")
runtime_root = Path("/opt/mokaair/tools/video")
reject_linked_ancestors(runtime_root)
if not runtime_root.is_dir():
    raise RuntimeError("worker tools/video directory missing or linked")
runtime_files = []
for entry in runtime_root.rglob("*"):
    if entry.is_symlink():
        raise RuntimeError("linked worker tools/video member")
    if entry.is_dir():
        continue
    if not entry.is_file():
        raise RuntimeError("special worker tools/video member")
    relative = entry.relative_to(runtime_root).as_posix()
    info = record(entry)
    runtime_files.append({"path": relative, "sha256": info["sha256"],
                          "bytes": info["bytes"]})
runtime_files.sort(key=lambda item: item["path"].encode("utf-8"))
if not runtime_files:
    raise RuntimeError("worker tools/video tree empty")
runtime_digest = hashlib.sha256()
for item in runtime_files:
    runtime_digest.update(item["path"].encode("utf-8") + b"\0"
                          + item["sha256"].encode("ascii") + b"\n")
story_hash = worker["story_mjs"]["sha256"]
if next((item["sha256"] for item in runtime_files
         if item["path"] == "automation/story.mjs"), None) != story_hash:
    raise RuntimeError("worker story.mjs inventory mismatch")
print(json.dumps({
    "schema_version": 1,
    "slug": slug,
    "audit_events": events,
    "audit_files": audit_files,
    "lexicon_files": lexicon_files,
    "files": files,
    "controls": controls,
    "worker": worker,
    "release_sha": os.environ["A01_RELEASE_SHA"],
    "tools_video_tree_sha": os.environ["A01_TOOLS_VIDEO_TREE_SHA"],
    "worker_image_id": os.environ["A01_WORKER_IMAGE_ID"],
    "story_mjs_sha256": story_hash,
    "public_filter_sha256": story_hash,
    "tools_video_runtime_files": runtime_files,
    "tools_video_runtime_file_count": len(runtime_files),
    "tools_video_runtime_inventory_sha256": runtime_digest.hexdigest(),
}, sort_keys=True, separators=(",", ":")))
PY
