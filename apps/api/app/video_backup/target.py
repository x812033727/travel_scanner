"""Where a video's backup goes in Drive, how much of it, and what it must hold.

Pure functions over a VideoProject and the owner's settings (docs/videos/BACKUP.md §資料夾排法,
§每一層備份哪些檔). The worker copies what these name, and the site checks the worker's report
against them, so a file the worker forgot shows as missing instead of the video reading backed up.
"""

from __future__ import annotations

import posixpath
import re
import unicodedata
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from typing import Any, Literal

from app.models import VideoProject
from app.video_reviews.admin_service import locale_choices

Tier = Literal["basic", "full", "off"]
TIERS: tuple[Tier, ...] = ("basic", "full", "off")
# The owner's rule of 2026-10-23: every video that is backed up is backed up in full; a series
# set to basic or off in the settings is the only exception.
DEFAULT_TIER: Tier = "full"
# A series key that no rule found, and its folder.
OTHER = "other"
SHORTS = "Shorts"
# A series' shared files (its approved character sheets) beside its episodes, full tier only.
SHARED = "_共用"
DEFAULT_PATH = "AI/備份"
DEFAULT_FOLDER_NAMES: dict[str, str] = {
    "curio": "奇聞檔案局",
    "ou-de-jianghu": "偶的江湖",
    "sothatswhy": "原來如此事務所",
    "ai-terms": "AI 名詞十分鐘",
    "story": "品牌故事",
    OTHER: "其他",
    "zhong-tian-qu-qi": "種田娶妻打天下",
    "zhong-tian-qu-qi-r2": "種田娶妻打天下（真人版）",
    "tai-nainai": "恁祖媽今年18",
}
# The owner, 2026-11-10: every drama, and the two explainer series, under AI劇/<名稱>/<集數>/
# (docs/videos/BACKUP.md §資料夾排法). Any imported drama (a <series>-e033 slug) joins them.
AI_DRAMA = "AI劇"
AI_DRAMA_SERIES = frozenset(
    {"zhong-tian-qu-qi", "zhong-tian-qu-qi-r2", "tai-nainai", "curio", "sothatswhy"}
)
# An episode's older versions, inside its folder: <集數>/_舊版/<slug>/ for a whole superseded
# version, and <集數>/_舊版/<時間>/ for the files a later copy replaced (the worker's).
OLD_VERSIONS = "_舊版"
# Slug prefixes of the series that are not long-drama series rows.
SLUG_PREFIXES: tuple[tuple[str, str], ...] = (
    ("curio-", "curio"),
    ("ai-term-", "ai-terms"),
    ("sothatswhy-", "sothatswhy"),
    ("story-", "story"),
)
SERIES_KEY_PATTERN = r"^[a-z0-9][a-z0-9-]{0,39}$"
SERIES_KEY = re.compile(SERIES_KEY_PATTERN)
# An imported drama's episodes and compilations: <series>-e033, <series>-e001-005, -v2 after a
# revision, and -r2 for a remake, which is a drama of its own: zhong-tian-qu-qi-e001-r2 is the
# live-action 種田 (the owner, 2026-11-10: "當成另一部劇").
DRAMA_EPISODE = re.compile(
    r"^(?P<series>[a-z0-9][a-z0-9-]*?)-e(?P<first>\d{3})(?:-(?P<last>\d{3}))?"
    r"(?:-(?P<remake>r\d+))?(?:-v(?P<version>\d+))?$"
)
# An explainer episode's code, which names its folder: curio-h01, curio-w01-dolby-licensing,
# sothatswhy-p17-gecko-feet. They have no running episode number.
EPISODE_CODE = re.compile(r"^(?:curio|sothatswhy)-(?P<code>[a-z]\d{2})(?=-|$)")
VERSION = re.compile(r"-v(?P<version>\d+)$")
# What Google Drive for desktop cannot write on the owner's Windows PC, so a folder with it
# would never reach G:.
FORBIDDEN = re.compile(r'[<>:"|?*\\\x00-\x1f\x7f]')
# The first folder of a path pasted from the owner's PC, which is Drive's root, not a folder in it.
DRIVE_ROOTS = frozenset({"我的雲端硬碟", "my drive"})
MAX_PATH = 400
MAX_SEGMENT = 120


def as_dict(value: Any) -> dict[str, Any]:
    """``value`` when it is a JSON object, else an empty one: stored JSON is read defensively."""
    return value if isinstance(value, dict) else {}


class PathInvalid(ValueError):
    """A Drive path or folder name the backup cannot use; the message is for the owner."""


def segment_problem(name: str) -> str | None:
    """Why ``name`` cannot be one folder of a Drive path, or None."""
    if not name:
        return "資料夾名稱不能是空的"
    if name in {".", ".."}:
        return "路徑不能有 . 或 .."
    if len(name) > MAX_SEGMENT:
        return f"資料夾名稱最多 {MAX_SEGMENT} 個字"
    if FORBIDDEN.search(name) or "/" in name:
        return '資料夾名稱不能有 < > : " | ? * / \\ 或控制字元'
    if name != name.strip() or name.endswith("."):
        return "資料夾名稱的頭尾不能是空白，也不能以句點結尾"
    return None


def normalise_path(value: str) -> str:
    """The Drive path the owner meant, from any way they paste it.

    ``G:\\我的雲端硬碟\\AI\\備份\\``, ``G:\\My Drive\\AI\\備份``, ``/AI/備份/`` and ``AI/備份``
    all become ``AI/備份``: the drive letter and Drive's root folder go, backslashes become
    slashes and the slashes at either end go.
    """
    text = unicodedata.normalize("NFC", value).strip().replace("\\", "/")
    if re.match(r"^[A-Za-z]:", text):
        text = text[2:]
    parts = [part for part in text.split("/") if part != ""]
    if parts and parts[0].casefold() in DRIVE_ROOTS:
        parts = parts[1:]
    if not parts:
        raise PathInvalid("請填雲端硬碟裡的資料夾，例如 AI/備份")
    for part in parts:
        problem = segment_problem(part)
        if problem:
            raise PathInvalid(problem)
    joined = "/".join(parts)
    if len(joined) > MAX_PATH:
        raise PathInvalid(f"路徑最多 {MAX_PATH} 個字")
    return joined


def remote_prefix(path: str, lock: str | None) -> str | None:
    """``path`` relative to the folder the host's rclone remote is locked to, or None outside it.

    The remote's ``root_folder_id`` makes ``lock`` its root, so ``AI/備份`` under the lock
    ``AI/備份`` is the remote's root (an empty prefix) and ``AI/備份/影片`` is ``影片``.
    """
    if lock is None:
        return None
    if path == lock:
        return ""
    if path.startswith(f"{lock}/"):
        return path[len(lock) + 1 :]
    return None


@dataclass(frozen=True)
class Target:
    series_key: str
    # Relative to the configured path: <series folder>/<episode folder>.
    folder: str
    tier: Tier
    # The series' shared folder, beside the episodes.
    shared_folder: str
    # The folder an earlier backup used under a rule since replaced; the worker moves it to
    # ``folder`` in Drive (no upload) and reports the new one, which then is the stored folder.
    moved_from: str | None = None


def drama_series(project: VideoProject) -> str | None:
    """The drama an imported episode belongs to, from its slug, when it has no series row."""
    if project.shorts_line is not None or project.series_slug or project.category != "drama":
        return None
    match = DRAMA_EPISODE.match(project.slug)
    if not match:
        return None
    series = f"{match['series']}-{match['remake']}" if match["remake"] else match["series"]
    return series if SERIES_KEY.match(series) else None


def version_stem(slug: str) -> tuple[str, int]:
    """A slug without its -vN, and N (1 when it has none): curio-h01-v2 is version 2 of
    curio-h01, and both are filed in one episode folder."""
    match = VERSION.search(slug)
    return (slug[: match.start()], int(match["version"])) if match else (slug, 1)


def is_ai_drama(project: VideoProject, key: str) -> bool:
    return project.shorts_line is None and (key in AI_DRAMA_SERIES or bool(drama_series(project)))


def ai_episode_folder(project: VideoProject) -> str:
    """第033集, 第001-005集 for a compilation, the code (H01) for an explainer, else the slug."""
    match = DRAMA_EPISODE.match(project.slug)
    if match:
        last = f"-{match['last']}" if match["last"] else ""
        return f"第{match['first']}{last}集"
    if project.episode_number is not None:
        return f"第{project.episode_number:03d}集"
    code = EPISODE_CODE.match(project.slug)
    return code["code"].upper() if code else version_stem(project.slug)[0]


def series_key(project: VideoProject) -> str:
    """The series a video is filed under: a Short's series, then a long series' slug, then an
    imported drama's series from its slug, then the slug's series prefix, then the category;
    ``other`` when none says."""
    if project.shorts_line is not None:
        return project.shorts_series or project.shorts_line
    if project.series_slug:
        return project.series_slug
    drama = drama_series(project)
    if drama:
        return drama
    for prefix, key in SLUG_PREFIXES:
        if project.slug.startswith(prefix):
            return key
    return project.category or OTHER


def series_folder(key: str, shorts: bool, folder_names: Mapping[str, str]) -> str:
    name = folder_names.get(key) or DEFAULT_FOLDER_NAMES.get(key) or key
    return f"{SHORTS}/{name}" if shorts else name


def episode_folder(project: VideoProject) -> str:
    if project.episode_number is not None and project.shorts_line is None:
        return f"{project.episode_number:03d}-{project.slug}"
    return project.slug


def stored_folder(project: VideoProject) -> str | None:
    """The folder the first backup used, which every later backup keeps."""
    folder = as_dict(project.backup).get("folder")
    return folder if isinstance(folder, str) and folder else None


def resolve_target(
    project: VideoProject,
    *,
    tiers: Mapping[str, str] | None = None,
    folder_names: Mapping[str, str] | None = None,
    superseded: bool = False,
) -> Target:
    """Where ``project`` goes and how much of it. A folder already used stays: renaming a series
    later must not split one video between two folders. The tier follows the settings now.

    ``superseded``: a later version of the same episode is backed up too, so this one is filed
    under the episode's _舊版/ and the episode folder itself holds the latest."""
    key = series_key(project)
    names = folder_names or {}
    chosen = (tiers or {}).get(key)
    if chosen not in TIERS and drama_series(project):
        # A tier the owner set for the whole category before each drama had its own key holds
        # until they set one for the drama itself.
        chosen = (tiers or {}).get(project.category or OTHER)
    tier: Tier = chosen if chosen in TIERS else DEFAULT_TIER
    if is_ai_drama(project, key):
        return _ai_drama_target(project, key, tier, names, superseded)
    series = series_folder(key, project.shorts_line is not None, names)
    folder = stored_folder(project) or f"{series}/{episode_folder(project)}"
    return Target(key, folder, tier, f"{posixpath.dirname(folder)}/{SHARED}")


def _ai_drama_target(
    project: VideoProject, key: str, tier: Tier, names: Mapping[str, str], superseded: bool
) -> Target:
    """AI劇/<名稱>/<集數>/. A backup filed anywhere outside AI劇/ before 2026-11-10 is moved here
    once, by the worker (``moved_from``); one already under AI劇/ stays where it is, except that
    the episode folder itself goes to the latest version once a later one is backed up (the later
    copy has already put this version's files under _舊版/<時間>/, so nothing moves)."""
    drama = f"{AI_DRAMA}/{series_folder(key, False, names)}"
    episode = f"{drama}/{ai_episode_folder(project)}"
    default = f"{episode}/{OLD_VERSIONS}/{project.slug}" if superseded else episode
    stored = stored_folder(project)
    moved_from = None
    folder = default
    if stored and stored != default:
        if not stored.startswith(f"{AI_DRAMA}/"):
            moved_from = stored
        elif not (superseded and stored == episode):
            folder = stored
    return Target(key, folder, tier, f"{drama}/{SHARED}", moved_from)


# --- what a backup must hold ------------------------------------------------------------------

PARTS = ("descriptions", "captions", "dubs")
# The package's own files, by the contents flag that reports each. A Short's card pipeline
# writes final.mp4, zh-TW.srt, cover.png and titles.json, and no metadata.json
# (tools/video/shorts/build.mjs).
REQUIRED = {"final.mp4": "final", "metadata.json": "metadata"}
SHORT_REQUIRED = {"final.mp4": "final"}


def expected_parts(project: VideoProject) -> dict[str, list[str]]:
    """What a backup of ``project`` must hold: the package's own files (``required``) and the
    language files the owner's choice asks for (docs/videos/LANGUAGES.md), a description per
    language with titles chosen, a caption file per language with captions, a dub track per
    language with a dub."""
    chosen = locale_choices(project)
    return {
        "required": list(SHORT_REQUIRED if project.shorts_line is not None else REQUIRED),
        "descriptions": sorted(locale for locale, part in chosen.items() if part.metadata),
        "captions": sorted(locale for locale, part in chosen.items() if part.captions),
        "dubs": sorted(locale for locale, part in chosen.items() if part.dub),
    }


def _locales(value: Any) -> set[str]:
    return {item for item in value if isinstance(item, str)} if isinstance(value, list) else set()


def missing_files(
    contents: Mapping[str, Any] | None, expected: Mapping[str, Iterable[str]]
) -> list[str]:
    """What a backup with ``contents`` (the worker's account of the files it checked in Drive)
    lacks: each required package file, and each chosen language's file unless the package
    skipped it with a reason (a caption or dub the worker gave up on)."""
    contents = contents or {}
    flags = {**REQUIRED, **SHORT_REQUIRED}
    missing = [
        name for name in expected.get("required", REQUIRED) if contents.get(flags[name]) is not True
    ]
    skipped = as_dict(contents.get("skipped"))
    patterns = {
        "descriptions": "descriptions/{}.txt",
        "captions": "captions/{}.srt",
        "dubs": "dubs/{}",
    }
    for part in PARTS:
        have = _locales(contents.get(part)) | _locales(skipped.get(part))
        missing += [
            patterns[part].format(locale) for locale in expected.get(part, ()) if locale not in have
        ]
    return missing
