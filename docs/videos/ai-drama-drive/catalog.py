#!/usr/bin/env python3
"""Build the episode catalog of 奇聞檔案局 and 原來如此事務所 from Google Drive and the repository.

    python3 docs/videos/ai-drama-drive/catalog.py            # reads videobackup:AI劇 (rclone or gdrive)
    python3 docs/videos/ai-drama-drive/catalog.py --remote videobackup:AI劇 --out docs/videos/explainer-series
    python3 docs/videos/ai-drama-drive/catalog.py --gdrive-ai-drama-id 1EKqfreFk028Roxv1aF0k2R1Hh3DRJ7kG

Writes CATALOG.md (the table people read) and catalog.json (the same rows for tools) into --out.
Nothing on Drive is changed: the script only lists folders and reads backup.json and metadata.json.

Where each column comes from (docs/videos/explainer-series/CATALOG.md repeats this for readers):
  Drive folder, category, slug, YouTube id <- AI劇/<系列>/<分類>/<代碼>/backup.json and folder listing,
                                              written by the host worker after the upload package is built
  title, privacy, languages, bookends      <- the same folder's metadata.json (upload package)
  narration voice, look, thumbnail layout  <- docs/videos/<slug>/video.json in the repository
  dub voice                                <- inferred from the dub files' date on Drive: dubs made before
                                              2026-11-12 are Gemini; from 2026-11-12 the dub tool uses MiniMax
                                              when the site has a MiniMax key (docs/videos/DUBS.md), so those
                                              are marked as probable MiniMax until the dub timeline says so
"""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
import datetime as dt
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[3]
DEFAULT_AI_DRAMA_FOLDER_ID = "1EKqfreFk028Roxv1aF0k2R1Hh3DRJ7kG"
SERIES = [
    {
        "name": "奇聞檔案局",
        "key": "curio",
        "prefixes": ("curio-",),
        "pool": "docs/videos/history-curiosity/pool",
    },
    {
        "name": "原來如此事務所",
        "key": "so-thats-why",
        "prefixes": ("sothatswhy-",),
        "pool": "docs/videos/so-thats-why/pool",
    },
]
CURIO_CATEGORIES = {
    "H": "H-歷史懸案",
    "S": "S-歷史人物與名場面",
    "M": "M-奇異現象與自然",
    "F": "F-童話神話與怪談原版",
    "L": "L-都市傳說與消失地名",
    "G": "G-靈異與超自然公案",
    "P": "P-預言與末日",
    "U": "U-外星太空與未知訊號",
    "W": "W-商業與品牌奇聞",
    "B": "W-商業與品牌奇聞",
}
SOTHATSWHY_PLAN_CATEGORIES = {
    "P01": "數位科技與通訊工程",
    "P02": "地球天氣與太空",
    "P03": "數位科技與通訊工程",
    "P04": "地球天氣與太空",
    "P05": "物理化學與日常材料",
    "P06": "物理化學與日常材料",
    "P07": "物理化學與日常材料",
    "P08": "飲食與廚房科學",
    "P09": "數位科技與通訊工程",
    "P10": "數位科技與通訊工程",
    "P11": "數位科技與通訊工程",
    "P12": "數位科技與通訊工程",
    "P13": "數位科技與通訊工程",
    "P14": "地球天氣與太空",
    "P15": "地球天氣與太空",
    "P16": "地球天氣與太空",
    "P17": "生物動物與植物",
    "P18": "物理化學與日常材料",
    "P19": "數位科技與通訊工程",
    "P20": "物理化學與日常材料",
    "P21": "人體感官與日常行為",
    "P22": "物理化學與日常材料",
    "P23": "地球天氣與太空",
    "P24": "地球天氣與太空",
    "P25": "建築交通與商業制度",
    "P26": "建築交通與商業制度",
    "P27": "建築交通與商業制度",
    "P28": "建築交通與商業制度",
    "P29": "數位科技與通訊工程",
    "P30": "建築交通與商業制度",
}
EXPLAINER_CATEGORIES = frozenset(
    set(CURIO_CATEGORIES.values()) | set(SOTHATSWHY_PLAN_CATEGORIES.values())
)
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
FOLDER_MIME = "application/vnd.google-apps.folder"


def _load_theme_categories() -> dict[str, dict[str, str]]:
    out: dict[str, dict[str, str]] = {"curio": {}, "so-thats-why": {}}
    for key, rel in (
        ("curio", "docs/videos/history-curiosity/pool/themes.json"),
        ("so-thats-why", "docs/videos/so-thats-why/pool/themes.json"),
    ):
        p = ROOT / rel
        if p.exists():
            raw = json.loads(p.read_text(encoding="utf-8"))
            for item in raw.get("episodes") or []:
                out[key][str(item["id"]).upper()] = item.get("category") or ""
    # Also load target.py SOTHATSWHY_CODE_CATEGORIES if importable, for legacy T/B/A/S codes.
    target_py = ROOT / "apps/api/app/video_backup/target.py"
    if target_py.exists():
        text = target_py.read_text(encoding="utf-8")
        m = re.search(r"SOTHATSWHY_CODES_BY_CATEGORY:.*?=\s*\{(.*?)\n\}", text, re.S)
        if m:
            for cat_m in re.finditer(r'"([^"]+)":\s*\((.*?)\)|"([^"]+)":\s*"([^"]+)"', m.group(1), re.S):
                cat = cat_m.group(1) or cat_m.group(3)
                body = cat_m.group(2) if cat_m.group(1) else f'"{cat_m.group(4)}"'
                codes = " ".join(re.findall(r'"([^"]+)"', body)).split()
                for c in codes:
                    out["so-thats-why"].setdefault(c.upper(), cat)
    return out


THEME_CATEGORIES = _load_theme_categories()


def infer_category(series_key: str, code: str, slug: str) -> str:
    code = (code or "").upper()
    if series_key == "curio":
        if code and code[0] in CURIO_CATEGORIES and not code.startswith("T"):
            return CURIO_CATEGORIES[code[0]]
        if code.startswith("T"):
            return THEME_CATEGORIES["curio"].get(code, "")
        m = re.match(r"^curio-([hsmflgpuwb])-", slug or "")
        if m:
            return CURIO_CATEGORIES[m.group(1).upper()]
    elif series_key == "so-thats-why":
        if code in SOTHATSWHY_PLAN_CATEGORIES:
            return SOTHATSWHY_PLAN_CATEGORIES[code]
        if code in THEME_CATEGORIES["so-thats-why"]:
            return THEME_CATEGORIES["so-thats-why"][code]
    return ""


class RcloneBackend:
    def __init__(self, remote: str) -> None:
        self.remote = remote

    def _run(self, *args: str) -> str:
        env = dict(os.environ)
        env.setdefault("RCLONE_CONFIG", os.devnull)
        out = subprocess.run(["rclone", *args], capture_output=True, text=True, env=env)
        if out.returncode != 0:
            raise RuntimeError(f"rclone {' '.join(args)} failed: {out.stderr.strip()[-400:]}")
        return out.stdout

    def scan_series(self, series_name: str) -> tuple[dict[str, dict], dict[tuple[str, str], dict]]:
        base = f"{self.remote}/{series_name}"
        listing = json.loads(
            self._run("lsjson", "-R", "--max-depth", "4", "--no-mimetype", base)
        )
        folders: dict[str, dict] = {}
        for entry in listing:
            parts = entry["Path"].split("/")
            if parts[0].startswith("_"):
                continue
            if parts[0] in EXPLAINER_CATEGORIES:
                if len(parts) < 2 or parts[1].startswith("_"):
                    continue
                ep_key = f"{parts[0]}/{parts[1]}"
                rel = parts[2:]
            else:
                ep_key = parts[0]
                rel = parts[1:]
            info = folders.setdefault(
                ep_key,
                {
                    "category": parts[0] if parts[0] in EXPLAINER_CATEGORIES else "",
                    "top": set(),
                    "old": set(),
                    "dubs": [],
                    "final": None,
                },
            )
            if len(rel) >= 1:
                info["top"].add(rel[0])
            if len(rel) == 2 and rel[0] == "_舊版":
                info["old"].add(rel[1])
            if len(rel) == 2 and rel[0] == "dubs" and not entry["IsDir"]:
                info["dubs"].append(entry["ModTime"][:10])
            if len(rel) == 1 and rel[0] == "final.mp4":
                info["final"] = entry["ModTime"][:10]

        jsons: dict[tuple[str, str], dict] = {}
        for ep_key, info in folders.items():
            for fname in ("backup.json", "metadata.json"):
                if fname in info["top"]:
                    try:
                        jsons[(ep_key, fname)] = json.loads(
                            self._run("cat", f"{base}/{ep_key}/{fname}")
                        )
                    except (RuntimeError, json.JSONDecodeError):
                        pass
        return folders, jsons


class GdriveBackend:
    def __init__(self, ai_drama_id: str) -> None:
        self.ai_drama_id = ai_drama_id

    @staticmethod
    def _run(*args: str) -> str:
        import time

        for attempt in range(5):
            out = subprocess.run(["gdrive", *args], capture_output=True, text=True)
            if out.returncode == 0:
                return out.stdout
            err = out.stderr.strip()
            if attempt < 4 and any(
                tok in err
                for tok in (
                    "Error 500",
                    "Error 502",
                    "Error 503",
                    "Error 504",
                    "transientError",
                    "backendError",
                )
            ):
                time.sleep(1.5 * (2**attempt))
                continue
            raise RuntimeError(f"gdrive {' '.join(args)} failed: {err[-400:]}")
        raise AssertionError("unreachable")

    def _ls(self, folder_id: str) -> list[dict]:
        data = json.loads(self._run("readonly", "ls", folder_id, "--max", "0", "--json"))
        return data.get("files") if isinstance(data, dict) else data

    def _download_json(self, file_id: str) -> dict | None:
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tmp:
            tmp_path = Path(tmp.name)
        try:
            self._run("readonly", "download", file_id, "--out", str(tmp_path))
            return json.loads(tmp_path.read_text(encoding="utf-8"))
        except (OSError, RuntimeError, json.JSONDecodeError):
            return None
        finally:
            tmp_path.unlink(missing_ok=True)

    def scan_series(self, series_name: str) -> tuple[dict[str, dict], dict[tuple[str, str], dict]]:
        ai_children = self._ls(self.ai_drama_id)
        series_entry = next(
            (x for x in ai_children if x.get("name") == series_name and x.get("mimeType") == FOLDER_MIME),
            None,
        )
        if not series_entry:
            raise RuntimeError(f"Series folder {series_name!r} not found under {self.ai_drama_id}")
        top_items = [
            x
            for x in self._ls(series_entry["id"])
            if x.get("mimeType") == FOLDER_MIME and not str(x.get("name", "")).startswith("_")
        ]

        ep_targets: list[tuple[str, str, str]] = []  # (ep_key, category, folder_id)
        cat_items = [x for x in top_items if x["name"] in EXPLAINER_CATEGORIES]
        flat_items = [x for x in top_items if x["name"] not in EXPLAINER_CATEGORIES]
        for item in flat_items:
            ep_targets.append((item["name"], "", item["id"]))

        if cat_items:
            with ThreadPoolExecutor(max_workers=8) as pool:
                cat_lists = list(pool.map(lambda c: (c["name"], self._ls(c["id"])), cat_items))
            for cat_name, children in cat_lists:
                for child in children:
                    if child.get("mimeType") == FOLDER_MIME and not str(child.get("name", "")).startswith("_"):
                        ep_targets.append((f"{cat_name}/{child['name']}", cat_name, child["id"]))

        folders: dict[str, dict] = {}
        sub_ls_tasks: list[tuple[str, str, str]] = []  # (ep_key, kind, folder_id)
        dl_tasks: list[tuple[str, str, str]] = []  # (ep_key, fname, file_id)

        def inspect_ep(item: tuple[str, str, str]) -> tuple[str, str, list[dict]]:
            ep_key, category, fid = item
            return ep_key, category, self._ls(fid)

        with ThreadPoolExecutor(max_workers=8) as pool:
            ep_results = list(pool.map(inspect_ep, ep_targets))

        for ep_key, category, entries in ep_results:
            info = {
                "category": category,
                "top": set(),
                "old": set(),
                "dubs": [],
                "final": None,
            }
            for e in entries:
                name = e.get("name") or ""
                info["top"].add(name)
                mtime = (e.get("modifiedTime") or "")[:10]
                is_dir = e.get("mimeType") == FOLDER_MIME
                if name == "final.mp4" and not is_dir:
                    info["final"] = mtime
                elif name in ("backup.json", "metadata.json") and not is_dir:
                    dl_tasks.append((ep_key, name, e["id"]))
                elif name in ("_舊版", "dubs") and is_dir:
                    sub_ls_tasks.append((ep_key, name, e["id"]))
            folders[ep_key] = info

        if sub_ls_tasks:
            with ThreadPoolExecutor(max_workers=8) as pool:
                sub_results = list(
                    pool.map(lambda t: (t[0], t[1], self._ls(t[2])), sub_ls_tasks)
                )
            for ep_key, kind, entries in sub_results:
                for e in entries:
                    if kind == "_舊版":
                        folders[ep_key]["old"].add(e.get("name") or "")
                    elif kind == "dubs" and e.get("mimeType") != FOLDER_MIME:
                        mtime = (e.get("modifiedTime") or "")[:10]
                        if mtime:
                            folders[ep_key]["dubs"].append(mtime)

        jsons: dict[tuple[str, str], dict] = {}
        if dl_tasks:
            with ThreadPoolExecutor(max_workers=8) as pool:
                dl_results = list(
                    pool.map(lambda t: (t[0], t[1], self._download_json(t[2])), dl_tasks)
                )
            for ep_key, fname, doc in dl_results:
                if isinstance(doc, dict):
                    jsons[(ep_key, fname)] = doc

        return folders, jsons


def choose_backend(remote: str, backend: str, gdrive_id: str):
    if backend == "gdrive":
        return GdriveBackend(gdrive_id)
    if backend == "rclone":
        return RcloneBackend(remote)
    has_rclone_env = bool(os.environ.get("RCLONE_CONFIG_VIDEOBACKUP_TYPE") or os.environ.get("RCLONE_CONFIG"))
    if shutil.which("rclone") and has_rclone_env:
        return RcloneBackend(remote)
    if shutil.which("gdrive"):
        return GdriveBackend(gdrive_id)
    return RcloneBackend(remote)


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
    s = slug or ""
    m = re.match(r"^curio-([hsmflgpuwb])-([a-z]?\d+)(?=-|$)", s)
    if m:
        axis, raw = m.group(1).upper(), m.group(2).upper()
        return f"{axis}{raw}" if raw[0].isdigit() else raw
    m = re.match(r"^sothatswhy-(phy|bio|geo|tec|fod|hum|soc)-([a-z]?\d+)(?=-|$)", s)
    if m:
        pref, raw = m.group(1).upper(), m.group(2).upper()
        return f"{pref}-{raw}" if raw[0].isdigit() else raw
    m = re.match(r"^(?:curio|sothatswhy)-([a-z]\d+)\b", s)
    return m.group(1).upper() if m else ""


def other_ids(code: str, videos: dict, skip: str) -> list[str]:
    """IDs the repository records for this code, other than the one backup.json already gives."""
    found = []
    for slug, (vid, _source) in IDS_FROM_DOCS.items():
        if code and code_of(slug) == code and vid != skip:
            found.append(f"{slug}={vid}")
    for slug, repo in videos.items():
        vid = ((repo["doc"].get("youtube") or {}).get("video_id")) or ""
        if (
            vid
            and code
            and code_of(slug) == code
            and vid != skip
            and all(not f.endswith("=" + vid) for f in found)
        ):
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


def _collapse_flat_rules_sync_stubs(folders: dict[str, dict]) -> dict[str, dict]:
    """Collapse flat `<code>/` folders containing only `教訓` when `<分類>/<code>/` exists."""
    categorized_by_leaf: dict[str, str] = {}
    for ep_key, info in folders.items():
        if info.get("category") and "/" in ep_key:
            categorized_by_leaf[ep_key.rsplit("/", 1)[-1]] = ep_key
    cleaned: dict[str, dict] = {}
    for ep_key, info in folders.items():
        top = set(info.get("top") or ())
        if (
            not info.get("category")
            and "/" not in ep_key
            and ep_key in categorized_by_leaf
            and top <= {"教訓"}
        ):
            if "教訓" in top:
                folders[categorized_by_leaf[ep_key]]["top"].add("教訓")
            continue
        cleaned[ep_key] = info
    return cleaned


def build_series(scanner, series: dict) -> list[dict]:
    folders, jsons = scanner.scan_series(series["name"])
    folders = _collapse_flat_rules_sync_stubs(folders)
    videos = repo_videos(series["prefixes"])
    used_slugs: set[str] = set()
    rows = []
    for folder in sorted(folders):
        info = folders[folder]
        leaf = folder.rsplit("/", 1)[-1]
        backup = jsons.get((folder, "backup.json"))
        meta = jsons.get((folder, "metadata.json"))
        slug = (backup or {}).get("slug") or (meta or {}).get("slug") or ""
        code = leaf if re.fullmatch(r"[A-Z]\d+", leaf) else code_of(slug)
        category = info.get("category") or infer_category(series["key"], code, slug)
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
        rows.append(
            {
                "series": series["name"],
                "category": category,
                "folder": f"AI劇/{series['name']}/{folder}",
                "slug": slug,
                "version": version_of(slug) if slug else "",
                "status": status,
                "youtube_id": youtube,
                "youtube_url": f"https://youtu.be/{youtube}" if youtube else "",
                "privacy": (meta or {}).get("privacy_status") or "",
                "title": (meta or {}).get("title")
                or ((doc or {}).get("youtube") or {}).get("title")
                or "",
                "narration_voice": describe_voice(doc),
                "dub_voice": dub_voice,
                "dub_locales": dub_locales,
                "dub_dates": dub_dates,
                "look": look,
                "new_look": (look in NEW_LOOKS) if look else None,
                "thumbnail_layout": layout
                or ("e（預設）" if series["key"] == "curio" and doc else ""),
                "bookends_hash": ((meta or {}).get("branding_hash") or "")[:12],
                "final_date": info["final"] or "",
                "has": sorted(
                    x
                    for x in info["top"]
                    if x
                    in {
                        "final.mp4",
                        "製作檔",
                        "主機檔",
                        "教訓",
                        "recordings",
                        "keyframes",
                        "timeline.json",
                    }
                ),
                "old_versions": sorted(info["old"]),
                "repo_dir": repo["dir"] if repo else "",
                "repo_versions": [videos[s]["dir"] for s in same_code],
                "other_youtube_ids": other_ids(code, videos, youtube),
                "extra_folders": [],
            }
        )
    # Legacy fallback if any episode still had two folders before consolidation.
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
            target["repo_versions"] = sorted(
                set(target["repo_versions"]) | set(r["repo_versions"])
            )
        else:
            merged.append(r)
    rows = merged
    for slug, repo in sorted(videos.items()):
        if slug in used_slugs:
            continue
        doc = repo["doc"]
        look = (doc.get("look") or {}).get("preset") or ""
        code = code_of(slug)
        rows.append(
            {
                "series": series["name"],
                "category": infer_category(series["key"], code, slug),
                "folder": "",
                "slug": slug,
                "version": version_of(slug),
                "status": "只在 repo（雲端硬碟沒有這集的資料夾）",
                "youtube_id": "",
                "youtube_url": "",
                "privacy": "",
                "title": (doc.get("youtube") or {}).get("title") or "",
                "narration_voice": describe_voice(doc),
                "dub_voice": "",
                "dub_locales": [],
                "dub_dates": [],
                "look": look,
                "new_look": (look in NEW_LOOKS) if look else None,
                "thumbnail_layout": (doc.get("thumbnail") or {}).get("layout") or "",
                "bookends_hash": "",
                "final_date": "",
                "has": [],
                "old_versions": [],
                "repo_dir": repo["dir"],
                "repo_versions": [repo["dir"]],
                "other_youtube_ids": other_ids(code, videos, ""),
                "extra_folders": [],
            }
        )
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
        "python3 docs/videos/ai-drama-drive/catalog.py   # 自動選用 rclone (videobackup:AI劇) 或 gdrive CLI",
        "```",
        "",
        "同樣的資料在 [`catalog.json`](catalog.json)，雲端硬碟 `AI劇/<系列>/_總表/` 有一份唯讀副本。",
        "題庫與備份的紀錄在 [`../ai-drama-drive/BACKUP-LOG.md`](../ai-drama-drive/BACKUP-LOG.md)。",
        "",
        "## 欄位從哪裡來",
        "",
        "| 欄位 | 來源 | 要重製時怎麼用 |",
        "| --- | --- | --- |",
        "| 分類、雲端位置 | 雲端硬碟 `AI/備份/AI劇/<系列>/<分類>/<代碼>/` | 奇聞檔案局分 9 類（`H-歷史懸案` 等）、原來如此事務所分 7 類（`物理化學與日常材料` 等）。上架包（final.mp4、字幕、配音、縮圖、metadata.json）在集數資料夾第一層；`製作檔/` 是做片 session 傳的全部檔案；`主機檔/` 是主機重做片頭片尾時的輸入與輸出；`教訓/` 是該集 NOTES；`_舊版/<時間>/` 是被取代的舊檔 |",
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
            "| 分類 | 雲端位置 | slug | 版本 | 狀態 | YouTube | 其他版本的 YouTube ID（repo 紀錄） | 公開 | 畫風 | 縮圖 | 旁白 | 外語配音 | 片頭片尾 | 成片日期 | 雲端有 | 舊版 | repo 文件 | 標題 |",
            "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
        ]
        for r in group:
            yt = f"[{r['youtube_id']}]({r['youtube_url']})" if r["youtube_id"] else ""
            look = f"{r['look']}（{cell(r['new_look'])}）" if r["look"] else ""
            dubs = f"{r['dub_voice']} {len(r['dub_locales'])} 語" if r["dub_voice"] else ""
            repo = "、".join(
                f"`{d}`"
                for d in (r.get("repo_versions") or ([r["repo_dir"]] if r["repo_dir"] else []))
            )
            folder = "、".join(
                f"`{f.split('/', 2)[-1]}`"
                for f in ([r["folder"]] if r["folder"] else []) + r.get("extra_folders", [])
            )
            lines.append(
                "| "
                + " | ".join(
                    [
                        cell(r.get("category") or ""),
                        folder,
                        f"`{r['slug']}`" if r["slug"] else "",
                        r["version"],
                        r["status"],
                        yt,
                        cell([f"`{x}`" for x in r.get("other_youtube_ids") or []]),
                        r["privacy"],
                        look,
                        r["thumbnail_layout"],
                        r["narration_voice"],
                        dubs,
                        r["bookends_hash"],
                        r["final_date"],
                        cell(r["has"]),
                        str(len(r["old_versions"])) if r["old_versions"] else "",
                        repo,
                        cell(r["title"]),
                    ]
                )
                + " |"
            )
        lines.append("")
    out.joinpath("CATALOG.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--remote", default="videobackup:AI劇")
    parser.add_argument("--backend", choices=("auto", "rclone", "gdrive"), default="auto")
    parser.add_argument("--gdrive-ai-drama-id", default=DEFAULT_AI_DRAMA_FOLDER_ID)
    parser.add_argument("--out", default=str(ROOT / "docs/videos/explainer-series"))
    args = parser.parse_args()
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    scanner = choose_backend(args.remote, args.backend, args.gdrive_ai_drama_id)
    rows = []
    for series in SERIES:
        rows += build_series(scanner, series)
    generated = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    out.joinpath("catalog.json").write_text(
        json.dumps(
            {
                "schema_version": 1,
                "generated_at": generated,
                "remote": args.remote,
                "episodes": rows,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    write_markdown(rows, out, generated)
    print(f"catalog: {len(rows)} rows -> {out}/CATALOG.md, catalog.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
