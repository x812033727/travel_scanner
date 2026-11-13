#!/usr/bin/env python3
"""Build the episode catalog of 奇聞檔案局 and 原來如此事務所 from Google Drive and the repository.

    python3 docs/videos/ai-drama-drive/catalog.py            # reads videobackup:AI劇 with rclone
    python3 docs/videos/ai-drama-drive/catalog.py --remote videobackup:AI劇 --out docs/videos/explainer-series

Writes CATALOG.md (the table people read) and catalog.json (the same rows for tools) into --out.
Nothing on Drive is changed: the script only lists folders and reads backup.json and metadata.json.

Where each column comes from (docs/videos/explainer-series/CATALOG.md repeats this for readers):
  Drive folder, slug, YouTube id, files   <- AI劇/<系列>/<集數>/backup.json and the folder listing,
                                             written by the host worker after the upload package is built
  title, privacy, languages, bookends     <- the same folder's metadata.json (upload package)
  narration voice, look, thumbnail layout <- docs/videos/<slug>/video.json in the repository
  dub voice                                <- inferred from the dub files' date on Drive: dubs made before
                                             2026-11-12 are Gemini; from 2026-11-12 the dub tool uses MiniMax
                                             when the site has a MiniMax key (docs/videos/DUBS.md), so those
                                             are marked as probable MiniMax until the dub timeline says so
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SERIES = [
    {"name": "奇聞檔案局", "key": "curio", "prefixes": ("curio-",), "pool": "docs/videos/history-curiosity/pool"},
    {"name": "原來如此事務所", "key": "so-thats-why", "prefixes": ("sothatswhy-",), "pool": "docs/videos/so-thats-why/pool"},
]
MINIMAX_DUBS_FROM = "2026-11-12"
# YouTube IDs that only the repository's delivery records hold: episodes uploaded before the host
# worker started writing backup.json (2026-11), and the 2026-10-12 recut uploads. slug -> (id, source).
IDS_FROM_DOCS = {
    "curio-h01": ("efSy-Jxq-s8", "docs/videos/curio-five-recuts-20261012/STUDIO-AND-BACKEND-LINKAGE.md"),
    "curio-h01-recut-20261012": ("2gdgYmiYTSk", "docs/videos/curio-five-recuts-20261012/STUDIO-AND-BACKEND-LINKAGE.md"),
    "curio-h02": ("6hswTvAftUA", "docs/videos/curio-five-recuts-20261012/STUDIO-AND-BACKEND-LINKAGE.md"),
    "curio-h02-recut-20261012": ("4gJhMFqYqC4", "docs/videos/curio-five-recuts-20261012/STUDIO-AND-BACKEND-LINKAGE.md"),
    "curio-h03": ("b98IdS1MB78", "docs/videos/curio-five-recuts-20261012/STUDIO-AND-BACKEND-LINKAGE.md"),
    "curio-h03-recut-20261012": ("JjM04OmwBjU", "docs/videos/curio-five-recuts-20261012/STUDIO-AND-BACKEND-LINKAGE.md"),
    "curio-u02": ("uZ9TlblvrCw", "docs/videos/curio-five-recuts-20261012/STUDIO-AND-BACKEND-LINKAGE.md"),
    "curio-u02-recut-20261012": ("NazQDspY5nk", "docs/videos/curio-five-recuts-20261012/STUDIO-AND-BACKEND-LINKAGE.md"),
    "curio-l08": ("mLxCEB_wSLk", "docs/videos/curio-five-recuts-20261012/STUDIO-AND-BACKEND-LINKAGE.md"),
    "curio-l08-recut-20261012": ("LQ0pV9vZdeA", "docs/videos/curio-five-recuts-20261012/STUDIO-AND-BACKEND-LINKAGE.md"),
    "curio-h12": ("QJVtVFecm7I", "docs/videos/curio-h12/delivery-package-20261017.md"),
    "curio-m09": ("yGF95x3O9U0", "docs/videos/curio-m09/youtube-readback-20261017.md"),
}
NEW_LOOKS = {"cute-mystery", "cute-cartoon"}


def rclone(*args: str) -> str:
    env = dict(os.environ)
    env.setdefault("RCLONE_CONFIG", os.devnull)
    out = subprocess.run(["rclone", *args], capture_output=True, text=True, env=env)
    if out.returncode != 0:
        raise RuntimeError(f"rclone {' '.join(args)} failed: {out.stderr.strip()[-400:]}")
    return out.stdout


def read_json(remote_path: str):
    try:
        return json.loads(rclone("cat", remote_path))
    except (RuntimeError, json.JSONDecodeError):
        return None


def repo_videos(prefixes: tuple[str, ...]) -> dict[str, dict]:
    found = {}
    for path in sorted((ROOT / "docs/videos").glob("*/video.json")):
        if not path.parent.name.startswith(prefixes):
            continue
        try:
            doc = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        slug = doc.get("slug") or path.parent.name
        found[slug] = {"doc": doc, "dir": str(path.parent.relative_to(ROOT))}
    return found


def version_of(slug: str) -> str:
    m = re.search(r"-v(\d+)$", slug or "")
    return f"v{m.group(1)}" if m else "v1"


def base_slug(slug: str) -> str:
    return re.sub(r"-v\d+$", "", slug or "")


def code_of(slug: str) -> str:
    """curio-h01-v2 -> H01, sothatswhy-p14-sky-colors -> P14: the code Drive folders use."""
    m = re.match(r"^(?:curio|sothatswhy)-([a-z]\d+)\b", slug or "")
    return m.group(1).upper() if m else ""


def other_ids(code: str, videos: dict, skip: str) -> list[str]:
    """IDs the repository records for this code, other than the one backup.json already gives."""
    found = []
    for slug, (vid, _source) in IDS_FROM_DOCS.items():
        if code and code_of(slug) == code and vid != skip:
            found.append(f"{slug}={vid}")
    for slug, repo in videos.items():
        vid = ((repo["doc"].get("youtube") or {}).get("video_id")) or ""
        if vid and code and code_of(slug) == code and vid != skip and all(not f.endswith("=" + vid) for f in found):
            found.append(f"{slug}={vid}")
    return sorted(found)


def version_key(slug: str) -> int:
    return int(version_of(slug)[1:])


def describe_voice(doc: dict | None) -> str:
    if not doc:
        return ""
    voice = doc.get("voice") or {}
    provider = voice.get("provider") or ""
    name = voice.get("name") or ""
    label = {"gemini": "Gemini", "minimax": "MiniMax", "azure": "Azure"}.get(provider, provider)
    return f"{label} {name}".strip()


def build_series(remote: str, series: dict) -> list[dict]:
    base = f"{remote}/{series['name']}"
    listing = json.loads(rclone("lsjson", "-R", "--max-depth", "3", "--no-mimetype", base))
    folders: dict[str, dict] = {}
    for entry in listing:
        parts = entry["Path"].split("/")
        if parts[0].startswith("_"):
            continue
        info = folders.setdefault(parts[0], {"top": set(), "old": set(), "dubs": [], "final": None})
        if len(parts) >= 2:
            info["top"].add(parts[1])
        if len(parts) == 3 and parts[1] == "_舊版":
            info["old"].add(parts[2])
        if len(parts) == 3 and parts[1] == "dubs" and not entry["IsDir"]:
            info["dubs"].append(entry["ModTime"][:10])
        if len(parts) == 2 and parts[1] == "final.mp4":
            info["final"] = entry["ModTime"][:10]

    videos = repo_videos(series["prefixes"])
    used_slugs: set[str] = set()
    rows = []
    for folder in sorted(folders):
        info = folders[folder]
        backup = read_json(f"{base}/{folder}/backup.json") if "backup.json" in info["top"] else None
        meta = read_json(f"{base}/{folder}/metadata.json") if "metadata.json" in info["top"] else None
        slug = (backup or {}).get("slug") or (meta or {}).get("slug") or ""
        code = folder if re.fullmatch(r"[A-Z]\d+", folder) else code_of(slug)
        same_code = sorted((s for s in videos if code and code_of(s) == code), key=version_key)
        used_slugs.update(same_code)
        repo = videos.get(slug) or videos.get(base_slug(slug))
        if not repo and not slug and same_code:
            repo = videos[same_code[-1]]
        doc = repo["doc"] if repo else None
        look = ((doc or {}).get("look") or {}).get("preset") or ""
        layout = ((doc or {}).get("thumbnail") or {}).get("layout") or ""
        dub_dates = sorted(set(info["dubs"]))
        if not dub_dates:
            dub_voice = ""
        elif dub_dates[-1] >= MINIMAX_DUBS_FROM:
            dub_voice = "MiniMax（推定）"
        else:
            dub_voice = "Gemini"
        dub_locales = [d.get("locale") for d in (meta or {}).get("dubs") or []]
        youtube = (backup or {}).get("youtube_video_id") or ""
        if backup:
            status = "已上傳 YouTube" if youtube else "有上架包，未記 YouTube ID"
        else:
            status = "只有製作檔或教訓"
        rows.append({
            "series": series["name"],
            "folder": f"AI劇/{series['name']}/{folder}",
            "slug": slug,
            "version": version_of(slug) if slug else "",
            "status": status,
            "youtube_id": youtube,
            "youtube_url": f"https://youtu.be/{youtube}" if youtube else "",
            "privacy": (meta or {}).get("privacy_status") or "",
            "title": (meta or {}).get("title") or ((doc or {}).get("youtube") or {}).get("title") or "",
            "narration_voice": describe_voice(doc),
            "dub_voice": dub_voice,
            "dub_locales": dub_locales,
            "dub_dates": dub_dates,
            "look": look,
            "new_look": (look in NEW_LOOKS) if look else None,
            "thumbnail_layout": layout or ("e（預設）" if series["key"] == "curio" and doc else ""),
            "bookends_hash": ((meta or {}).get("branding_hash") or "")[:12],
            "final_date": info["final"] or "",
            "has": sorted(x for x in info["top"] if x in {"final.mp4", "製作檔", "主機檔", "教訓", "recordings", "keyframes", "timeline.json"}),
            "old_versions": sorted(info["old"]),
            "repo_dir": repo["dir"] if repo else "",
            "repo_versions": [videos[s]["dir"] for s in same_code],
            "other_youtube_ids": other_ids(code, videos, youtube),
            "extra_folders": [],
        })
    # One episode can have two folders: 第007集/ (upload package, by episode number) and P07/ (production
    # files, by code). Fold the code folder into the numbered one so each episode is one row.
    by_code = {code_of(r["slug"]): r for r in rows if r["slug"]}
    merged = []
    for r in rows:
        name = r["folder"].rsplit("/", 1)[-1]
        target = by_code.get(name) if not r["slug"] and re.fullmatch(r"[A-Z]\d+", name) else None
        if target is not None and target is not r:
            target["extra_folders"].append(r["folder"])
            target["has"] = sorted(set(target["has"]) | {f"{name}/{x}" for x in r["has"]})
            for key in ("look", "new_look", "narration_voice", "thumbnail_layout", "title"):
                if not target[key] and r[key] not in ("", None):
                    target[key] = r[key]
            target["repo_versions"] = sorted(set(target["repo_versions"]) | set(r["repo_versions"]))
        else:
            merged.append(r)
    rows = merged
    for slug, repo in sorted(videos.items()):
        if slug in used_slugs:
            continue
        doc = repo["doc"]
        look = (doc.get("look") or {}).get("preset") or ""
        rows.append({
            "series": series["name"], "folder": "", "slug": slug, "version": version_of(slug),
            "status": "只在 repo（雲端硬碟沒有這集的資料夾）", "youtube_id": "", "youtube_url": "", "privacy": "",
            "title": (doc.get("youtube") or {}).get("title") or "", "narration_voice": describe_voice(doc),
            "dub_voice": "", "dub_locales": [], "dub_dates": [], "look": look,
            "new_look": (look in NEW_LOOKS) if look else None,
            "thumbnail_layout": (doc.get("thumbnail") or {}).get("layout") or "", "bookends_hash": "",
            "final_date": "", "has": [], "old_versions": [], "repo_dir": repo["dir"],
            "repo_versions": [repo["dir"]],
            "other_youtube_ids": other_ids(code_of(slug), videos, ""),
            "extra_folders": [],
        })
    return rows


def cell(value) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "新版" if value else "舊版"
    if isinstance(value, list):
        return "、".join(str(v) for v in value)
    return str(value).replace("|", "／").replace("\n", " ")


def write_markdown(rows: list[dict], out: Path, generated: str) -> None:
    lines = [
        "# 奇聞檔案局與原來如此事務所：各集總表",
        "",
        f"由 `docs/videos/ai-drama-drive/catalog.py` 產生（{generated}），不要手改；要更新就重跑：",
        "",
        "```bash",
        "python3 docs/videos/ai-drama-drive/catalog.py   # 需要 rclone 與 RCLONE_CONFIG_VIDEOBACKUP_*",
        "```",
        "",
        "同樣的資料在 [`catalog.json`](catalog.json)，雲端硬碟 `AI劇/<系列>/_總表/` 有一份唯讀副本。",
        "題庫與備份的紀錄在 [`../ai-drama-drive/BACKUP-LOG.md`](../ai-drama-drive/BACKUP-LOG.md)。",
        "",
        "## 欄位從哪裡來",
        "",
        "| 欄位 | 來源 | 要重製時怎麼用 |",
        "| --- | --- | --- |",
        "| 雲端位置 | 雲端硬碟 `AI/備份/AI劇/<系列>/<集數>/` | 上架包（final.mp4、字幕、配音、縮圖、metadata.json）在資料夾第一層；`製作檔/` 是做片 session 傳的全部檔案；`主機檔/` 是主機重做片頭片尾時的輸入與輸出；`教訓/` 是該集 NOTES；`_舊版/<時間>/` 是被取代的舊檔 |",
        "| slug、YouTube ID | 該資料夾的 `backup.json`（主機 worker 寫的） | 後台與 YouTube 用 slug 和 ID 找到同一支片 |",
        "| 其他版本的 YouTube ID | repo 的交付紀錄（`catalog.py` 的 `IDS_FROM_DOCS` 列了出處）與 `video.json` 的 `youtube.video_id` | 2026-11 主機開始寫 `backup.json` 之前上傳的舊版、2026-10-12 的重剪版。後台才是正本，這裡缺的到後台「影片」查 slug |",
        "| 公開 | `metadata.json` 的 `privacy_status` | 上架包要求的公開設定；實際是否已公開以 YouTube Studio 為準 |",
        "| 版本 | slug 結尾（`-v2`、`-v3`；沒有就是 v1） | 重製版是新 slug；舊版的 docs 仍在 repo |",
        "| 畫風 | repo `docs/videos/<slug>/video.json` 的 `look.preset` | `cute-mystery`（奇聞）與 `cute-cartoon`（原來如此）是系列現在的新版畫風，其他（`custom`）是舊版 |",
        "| 縮圖版型 | `video.json` 的 `thumbnail.layout` | 奇聞 2026-11-10 起不寫就是新版 `e`；寫 `d` 是刻意保留舊版 |",
        "| 旁白聲音 | `video.json` 的 `voice` | 目前兩個系列都是 Gemini `Sulafat` |",
        "| 外語配音 | 雲端 `dubs/` 檔案日期 | 2026-11-12 前做的是 Gemini；當天起工具預設用 MiniMax，標「推定」，要確定看主機的配音 `timeline.json` 的 `voice_provider`（docs/videos/DUBS.md） |",
        "| 片頭片尾 | `metadata.json` 的 `branding_hash` 前 12 碼 | 同一個 hash 是同一組片頭片尾；重做片頭片尾要換成現在那組 |",
        "| repo 文件 | `docs/videos/<slug>/`，同一個代碼（H01、P14）的各版本都列 | 腳本、查核、brief、NOTES；沒有就是在主機或別的分支做的，查雲端 `製作檔/`。雲端資料夾沒有上架包時，畫風與旁白取最新版本的 `video.json` |",
        "",
    ]
    for series in SERIES:
        group = [r for r in rows if r["series"] == series["name"]]
        uploaded = sum(1 for r in group if r["youtube_id"])
        lines += [
            f"## {series['name']}",
            "",
            f"共 {len(group)} 列：已上架（有 YouTube ID）{uploaded} 集。題庫在 `{series['pool']}`。",
            "",
            "| 雲端位置 | slug | 版本 | 狀態 | YouTube | 其他版本的 YouTube ID（repo 紀錄） | 公開 | 畫風 | 縮圖 | 旁白 | 外語配音 | 片頭片尾 | 成片日期 | 雲端有 | 舊版 | repo 文件 | 標題 |",
            "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
        ]
        for r in group:
            yt = f"[{r['youtube_id']}]({r['youtube_url']})" if r["youtube_id"] else ""
            look = f"{r['look']}（{cell(r['new_look'])}）" if r["look"] else ""
            dubs = f"{r['dub_voice']} {len(r['dub_locales'])} 語" if r["dub_voice"] else ""
            repo = "、".join(f"`{d}`" for d in (r.get("repo_versions") or ([r["repo_dir"]] if r["repo_dir"] else [])))
            folder = "、".join(f"`{f.split('/', 2)[-1]}`" for f in ([r["folder"]] if r["folder"] else []) + r.get("extra_folders", []))
            lines.append("| " + " | ".join([
                folder, f"`{r['slug']}`" if r["slug"] else "", r["version"], r["status"], yt,
                cell([f"`{x}`" for x in r.get("other_youtube_ids") or []]), r["privacy"], look,
                r["thumbnail_layout"], r["narration_voice"], dubs, r["bookends_hash"], r["final_date"],
                cell(r["has"]), str(len(r["old_versions"])) if r["old_versions"] else "", repo, cell(r["title"]),
            ]) + " |")
        lines.append("")
    out.joinpath("CATALOG.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--remote", default="videobackup:AI劇")
    parser.add_argument("--out", default=str(ROOT / "docs/videos/explainer-series"))
    args = parser.parse_args()
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    rows = []
    for series in SERIES:
        rows += build_series(args.remote, series)
    generated = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    out.joinpath("catalog.json").write_text(
        json.dumps({"schema_version": 1, "generated_at": generated, "remote": args.remote, "episodes": rows},
                   ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_markdown(rows, out, generated)
    print(f"catalog: {len(rows)} rows -> {out}/CATALOG.md, catalog.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
