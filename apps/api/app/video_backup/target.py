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
# An explainer episode's code, which names its folder under AI劇/<系列>/<分類>/<代碼>/:
# curio-h01 -> H-歷史懸案/H01, curio-b01 -> W-商業與品牌奇聞/B01,
# sothatswhy-p17-gecko-feet -> 生物動物與植物/P17.
CURIO_CODE_WITH_AXIS = re.compile(r"^curio-(?P<axis>[hsmflgpuwb])-(?P<code>[a-z]?\d+)(?=-|$)")
CURIO_AXIS_CODE = re.compile(r"^curio-(?P<code>[hsmflgpuwb]\d+)(?=-|$)")
CURIO_THEME_CODE = re.compile(r"^curio-(?P<code>t\d+)(?=-|$)")
SOTHATSWHY_PREFIX_CODE = re.compile(
    r"^sothatswhy-(?P<prefix>phy|bio|geo|tec|fod|hum|soc)-(?P<code>[a-z]?\d+(?:-\d+)?)(?=-|$)"
)
SOTHATSWHY_PREFIX_NUM = re.compile(
    r"^sothatswhy-(?P<prefix>phy|bio|geo|tec|fod|hum|soc)(?P<num>\d+)(?=-|$)"
)
SOTHATSWHY_CODE = re.compile(r"^sothatswhy-(?P<code>[ptbags]\d+)(?=-|$)")
CURIO_CATEGORIES: dict[str, str] = {
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
CURIO_THEME_CODES_BY_CATEGORY: dict[str, str] = {
    "H-歷史懸案": "T09 T23 T29 T66 T77 T84 T95 T98 T106 T114 T117 T124 T135 T136 T146 T151",
    "S-歷史人物與名場面": (
        "T39 T46 T47 T48 T52 T53 T54 T55 T62 T63 T64 T85 T86 T87 T96 T100 T101 T102 T103 T108 "
        "T110 T125 T143"
    ),
    "M-奇異現象與自然": "T01 T02 T37 T38 T41 T75 T88 T112 T118 T128 T129 T134 T138 T150 T154 T161",
    "F-童話神話與怪談原版": (
        "T12 T13 T14 T16 T17 T18 T19 T20 T32 T50 T57 T60 T61 T67 T68 T69 T109 T144 T148 T149 "
        "T155 T158"
    ),
    "L-都市傳說與消失地名": (
        "T11 T31 T33 T34 T43 T45 T65 T70 T71 T79 T83 T89 T90 T91 T93 T99 T107 T111 T116 T127 "
        "T132 T142 T153 T156"
    ),
    "G-靈異與超自然公案": (
        "T10 T27 T28 T44 T49 T78 T104 T113 T115 T119 T120 T123 T130 T131 T137 T141 T152 T159 "
        "T160"
    ),
    "P-預言與末日": "T24 T26 T35 T40 T51 T56 T58 T59 T73 T76 T80 T92 T94 T121 T126 T147",
    "U-外星太空與未知訊號": (
        "T03 T04 T06 T21 T22 T36 T42 T72 T74 T81 T82 T97 T105 T122 T133 T139 T140 T145 T157"
    ),
}
SOTHATSWHY_PREFIX_CATEGORIES: dict[str, str] = {
    "PHY": "物理化學與日常材料",
    "BIO": "生物動物與植物",
    "GEO": "地球天氣與太空",
    "TEC": "數位科技與通訊工程",
    "FOD": "飲食與廚房科學",
    "HUM": "人體感官與日常行為",
    "SOC": "建築交通與商業制度",
}
SOTHATSWHY_CODES_BY_CATEGORY: dict[str, str] = {
    "物理化學與日常材料": (
        "P05 P06 P07 P18 P20 P22 S07 S13 S15 S27 S33 S36 S44 S49 S53 S68 S69 S70 S72 S76 S77 "
        "S78 S81 S85 S87 S88 G01 G04 G08 G11 G13 G14 G24 G30 G31 G32 G52 G53 G54 G64 G65 G66 "
        "G73 G74 G75 G89 G90 G91 G92 G93 G94 G95 G99 G100 G101 G102 G103 G104 G108 G109 G110 "
        "G128 G129 G130 G131 G134 G140 G141 G142 G143 G152 G153 G154 G155 G177 G178 G179 G180 "
        "G181 G190 G191 G192 G193 G194 G200 G201 G202 G203 G204 G216 G217 G218 G219 G227 G228 "
        "G229 G230 G238 G239 G240 G241 G247 G248 G249 G255 G256 G257 G260 G264 G265 G266 G269 "
        "G272 G273 G274 G275 G280 G281 G282 G283 G284 G285 G286 G297 G298 G299 G315 G316 G317 "
        "G318 G319 G366 G367 G368 G369 G370 G378 G379 G380 G381 G382 G397 G398 G399 G400 G401 "
        "G416 G417 G418 G419 G420 G435 G436 G437 G438 G439 G455 G456 G457 G459 G458 G475 G476 "
        "G477 G478 G479 G490 G491 G492 G493 G513 G520 G521 G522 G523 G525 G532 G533 G542 G543 "
        "G544 G564 G565 G566 G567 G590 G597 G598 G604 G605 G606 G608 G609 G611 G621 G626 G636 "
        "G640"
    ),
    "生物動物與植物": (
        "P17 S04 S34 S35 S41 S47 S59 S60 S61 S62 S63 G06 G20 G21 G22 G27 G28 G29 G61 G62 G63 "
        "G70 G71 G72 G86 G87 G88 G96 G97 G98 G105 G106 G107 G111 G112 G113 G114 G132 G133 G135 "
        "G136 G137 G138 G139 G148 G149 G150 G151 G160 G161 G162 G163 G173 G174 G175 G176 G186 "
        "G187 G188 G189 G205 G206 G207 G208 G213 G214 G215 G231 G232 G233 G242 G243 G244 G250 "
        "G251 G258 G259 G267 G268 G276 G277 G290 G291 G292 G308 G309 G310 G311 G312 G320 G321 "
        "G322 G323 G324 G325 G326 G327 G332 G333 G334 G335 G336 G350 G351 G352 G353 G354 G374 "
        "G375 G376 G377 G388 G389 G390 G391 G392 G393 G394 G395 G396 G407 G408 G409 G410 G411 "
        "G412 G413 G414 G415 G431 G432 G433 G434 G451 G452 G453 G454 G470 G471 G472 G473 G474 "
        "G480 G481 G482 G483 G484 G485 G486 G487 G488 G489 G503 G504 G505 G506 G507 G515 G516 "
        "G517 G518 G519 G529 G530 G531 G548 G549 G550 G551 G560 G561 G562 G563 G576 G577 G580 "
        "G581 G582 G583 G585 G601 G603 G610 G615 G618 G623 G629 G630 G631 G632 G633 G634 G635 "
        "G637 G638 G639"
    ),
    "地球天氣與太空": (
        "P02 P04 P14 P15 P16 P23 P24 S02 S12 S18 S21 S23 S28 S29 S32 S42 S43 S48 S56 S57 S58 "
        "S80 S82 S83 S84 G03 G09 G10 G12 G15 G16 G33 G34 G35 G67 G68 G69 G76 G77 G78 G118 G119 "
        "G120 G121 G122 G144 G145 G146 G147 G195 G196 G197 G198 G199 G223 G224 G225 G226 G300 "
        "G301 G302 G303 G304 G305 G306 G307 G313 G314 G341 G342 G343 G344 G345 G383 G384 G385 "
        "G386 G387 G402 G403 G404 G405 G406 G421 G422 G423 G424 G425 G440 G441 G442 G443 G444 "
        "G460 G461 G462 G463 G464 G494 G495 G496 G497 G508 G509 G510 G512 G514 G524 G526 G527 "
        "G528 G534 G535 G536 G537 G545 G546 G547 G555 G556 G557 G558 G568 G569 G570 G571 G587 "
        "G588 G589 G593 G594 G595 G596 G600 G607 G613 G616 G622"
    ),
    "數位科技與通訊工程": (
        "P01 P03 P09 P10 P11 P12 P13 P19 P29 S11 S17 A01 A02 A03 A04 A05 A06 A07 A08 A09 A10 "
        "A11 A12 A13 A15 A16 A18 A19 A20 A21 A22 A24 A25 A26 A27 A28 A29 A30 A31 A32 A33 A34 "
        "A35 A36 A37 A38 A39 A40 A41 A42 A43 A44 A45 A46 A47 A48 A49 A50 A51 A52 A53 A54 A55 "
        "A56 A57 A58 A59 A60 A61 A62 A63 A64 A65 A66 A67 A68 A69 A70 A71 A72 A73 A74 A75 S86 "
        "G02 G05 G07 G17 G18 G19 G36 G37 G38 G47 G48 G58 G59 G60 G82 G83 G84 G85 G123 G124 "
        "G125 G126 G127 G164 G165 G166 G167 G168 G209 G210 G211 G212 G245 G246 G261 G262 G263 "
        "G270 G271 G278 G279 G552 G553 G554 G591"
    ),
    "飲食與廚房科學": (
        "P08 S03 S08 S09 S19 S30 S31 S46 S50 S54 S55 S71 S73 S79 G25 G39 G40 G41 G79 G80 G81 "
        "G169 G170 G171 G172 G287 G288 G289 G328 G329 G330 G331 G346 G347 G348 G349 G371 G372 "
        "G373 G426 G427 G428 G429 G430 G538 G539 G540 G541 G572 G573 G586 G612 G614 G617 G628"
    ),
    "人體感官與日常行為": (
        "P21 S05 S06 S10 S14 S20 S24 S25 T17 S26 S37 S38 S39 S40 S45 T33 S51 S52 S64 S65 S66 "
        "S67 S74 S75 G26 G49 G50 G51 G156 G157 G158 G159 G182 G183 G184 G185 G220 G221 G222 "
        "G234 G235 G236 G237 G252 G253 G254 G293 G294 G295 G296 G355 G356 G357 G358 G359 G445 "
        "G446 G447 G448 G449 G450 G465 G466 G467 G468 G469 G498 G499 G500 G501 G502 G559 G574 "
        "G575 G578 G579 G584 G602 G620 G627"
    ),
    "建築交通與商業制度": (
        "P25 P26 P27 P28 P30 B01 B02 B03 B04 B05 B06 B07 B08 B09 B10 B11 B12 B13 B14 B15 B16 "
        "B17 B18 B19 B20 B21 B22 B23 B24 B25 S01 S16 S22 T01 T02 T03 T04 T05 T06 T07 T08 T09 "
        "T10 T11 T12 T13 T14 T15 T16 T18 T19 T20 T21 T22 T23 T24 T25 A14 A17 A23 B26 B27 B28 "
        "B29 B30 B31 B32 B33 B34 B35 B36 B37 B38 B39 B40 B41 B42 B43 B44 B45 B46 B47 B48 B49 "
        "B50 T26 T27 T28 T29 T30 T31 T32 T34 T35 T36 T37 T38 T39 T40 T41 T42 T43 T44 T45 T46 "
        "T47 T48 T49 T50 B51 B52 B53 B54 B55 B56 B57 B58 B59 B60 B61 B62 B63 B64 B65 B66 B67 "
        "B68 B69 B70 B71 B72 B73 B74 B75 T51 T52 T53 T54 T55 T56 T57 T58 T59 T60 T61 T62 T63 "
        "T64 T65 T66 T67 T68 T69 T70 T71 T72 T73 T74 T75 G23 G42 G43 G44 G45 G46 G55 G56 G57 "
        "G115 G116 G117 G337 G338 G339 G340 G360 G361 G362 G363 G364 G365 G511 G592 G599 G619 "
        "G624 G625"
    ),
}
CURIO_THEME_CATEGORIES: dict[str, str] = {
    code: cat for cat, codes in CURIO_THEME_CODES_BY_CATEGORY.items() for code in codes.split()
}
SOTHATSWHY_CODE_CATEGORIES: dict[str, str] = {
    code: cat for cat, codes in SOTHATSWHY_CODES_BY_CATEGORY.items() for code in codes.split()
}
EXPLAINER_CATEGORIES: frozenset[str] = frozenset(
    set(CURIO_CATEGORIES.values()) | set(SOTHATSWHY_PREFIX_CATEGORIES.values())
)
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


def ai_episode_parts(project: VideoProject, key: str) -> tuple[str | None, str]:
    """``(category, episode)``: ``('H-歷史懸案', 'H01')``, ``('物理化學與日常材料', 'P07')``,
    or ``(None, '第033集')``.

    Explainer codes win before ``episode_number`` so ``sothatswhy-p07-fridge-door`` with
    ``episode_number=7`` lands in ``物理化學與日常材料/P07`` instead of splitting into ``第007集``.
    """
    if key == "curio":
        by_axis = CURIO_CODE_WITH_AXIS.match(project.slug)
        if by_axis:
            axis = by_axis["axis"].upper()
            raw = by_axis["code"].upper()
            code = f"{axis}{raw}" if raw[0].isdigit() else raw
            return CURIO_CATEGORIES[axis], code
        axis_code = CURIO_AXIS_CODE.match(project.slug)
        if axis_code:
            code = axis_code["code"].upper()
            return CURIO_CATEGORIES[code[0]], code
        theme_code = CURIO_THEME_CODE.match(project.slug)
        if theme_code:
            code = theme_code["code"].upper()
            return CURIO_THEME_CATEGORIES.get(code), code
    elif key == "sothatswhy":
        by_prefix = SOTHATSWHY_PREFIX_CODE.match(project.slug)
        if by_prefix:
            prefix = by_prefix["prefix"].upper()
            raw = by_prefix["code"].upper()
            code = f"{prefix}-{raw}" if raw[0].isdigit() else raw
            return SOTHATSWHY_PREFIX_CATEGORIES[prefix], code
        prefix_num = SOTHATSWHY_PREFIX_NUM.match(project.slug)
        if prefix_num:
            prefix = prefix_num["prefix"].upper()
            return SOTHATSWHY_PREFIX_CATEGORIES[prefix], f"{prefix}{prefix_num['num']}"
        stw_code = SOTHATSWHY_CODE.match(project.slug)
        if stw_code:
            code = stw_code["code"].upper()
            return SOTHATSWHY_CODE_CATEGORIES.get(code), code
    match = DRAMA_EPISODE.match(project.slug)
    if match:
        last = f"-{match['last']}" if match["last"] else ""
        return None, f"第{match['first']}{last}集"
    if project.episode_number is not None:
        return None, f"第{project.episode_number:03d}集"
    return None, version_stem(project.slug)[0]


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
    """AI劇/<名稱>/<集數>/ (or AI劇/<名稱>/<分類>/<代碼>/ for the two explainer series).

    A backup filed outside AI劇/ before 2026-11-10, or under AI劇/<系列>/<舊集數> before the
    2026-11-13 explainer category split, is moved once by the worker (``moved_from``). One already
    at its current layout stays across a series rename, except that the episode folder itself goes
    to the latest version once a later one is backed up (the later copy has already put this
    version's files under _舊版/<時間>/, so nothing moves).
    """
    drama = f"{AI_DRAMA}/{series_folder(key, False, names)}"
    category, ep_name = ai_episode_parts(project, key)
    episode = f"{drama}/{category}/{ep_name}" if category else f"{drama}/{ep_name}"
    default = f"{episode}/{OLD_VERSIONS}/{project.slug}" if superseded else episode
    stored = stored_folder(project)
    moved_from = None
    folder = default
    if stored and stored != default:
        parts = stored.split("/")
        if not stored.startswith(f"{AI_DRAMA}/"):
            moved_from = stored
        elif category and (len(parts) < 3 or parts[2] not in EXPLAINER_CATEGORIES):
            if not (superseded and len(parts) == 3):
                moved_from = stored
        elif superseded and len(parts) == (4 if category else 3):
            folder = f"{stored}/{OLD_VERSIONS}/{project.slug}"
        else:
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
