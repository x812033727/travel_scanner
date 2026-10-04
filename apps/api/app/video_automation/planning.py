"""Source-bound anime plans for review, never a shortcut into video production.

The portable bundle contains UTF-8 source files, not executable tooling. Every
receipt and structured/rendered twin is checked in Python before database access.
The caller owns the transaction. A dry run does not flush its pending changes;
an apply deliberately flushes after *all* collision checks, and never commits or
opens a savepoint. Concurrent first inserts are protected by the slug constraint
and fail the caller's whole transaction instead of overwriting an existing work.
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, cast
from uuid import uuid4

from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.models import AdminAuditLog, User, VideoProject
from app.video_automation.models import (
    VideoDramaDoc,
    VideoDramaEpisode,
    VideoDramaRequest,
    VideoDramaSeries,
)

ACTION = "video_anime_plan_imported"
MAX_BUNDLE_BYTES = 8 * 1024 * 1024
MAX_FILE_BYTES = 2 * 1024 * 1024
SOURCE_NAMES = {"authoring-contract.json", "plan.json", "setting.json"} | {
    f"season-{n:02}.json" for n in range(1, 11)
}
SUPPORT_NAMES = {"README.md", "review.md", "build.mjs", "validate.mjs", "validate.test.mjs"}
GENERATED_NAMES = {
    "setting.md",
    "outline.md",
    "outline.json",
    "documents.json",
    "continuity.md",
    "continuity.csv",
} | {f"season-{n:02}.md" for n in range(1, 11)}
FILE_NAMES = SOURCE_NAMES | SUPPORT_NAMES | GENERATED_NAMES | {"manifest.json"}
STATE_FIELDS = ("time", "knowledge", "character_state", "evidence", "carry_forward")
EPISODE_TEXT = ("title", "logline", "hook", "conflict", "turn", "theme", "consequence")
SEASON_TEXT = (
    "title",
    "theme",
    "core_conflict",
    "time_span",
    "season_resolution",
    "season_hook",
)
ENDING_TYPES = {"danger", "reveal", "choice", "reversal", "emotion"}


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def _integer(value: Any, minimum: int, maximum: int) -> bool:
    return type(value) is int and minimum <= value <= maximum


def _text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip()) and "\x00" not in value


def _pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        _require(key not in result, f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _nonfinite(value: str) -> None:
    raise ValueError(f"nonfinite JSON value: {value}")


def _json(raw: str, name: str) -> dict[str, Any]:
    try:
        value = json.loads(raw, object_pairs_hook=_pairs, parse_constant=_nonfinite)
    except (json.JSONDecodeError, RecursionError) as error:
        raise ValueError(f"{name}: invalid JSON") from error
    _require(isinstance(value, dict), f"{name}: expected JSON object")
    return cast(dict[str, Any], value)


def _same(left: dict[str, Any], right: dict[str, Any]) -> bool:
    # Python's True == 1 would otherwise accept numeric drift in redundant twins.
    return bundle_hash(left) == bundle_hash(right)


def bundle_hash(bundle: dict[str, Any]) -> str:
    """Canonical hash binding the exact complete portable source bundle."""
    raw = json.dumps(
        bundle, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False
    )
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class ValidatedPlan:
    plan: dict[str, Any]
    setting: dict[str, Any]
    seasons: list[dict[str, Any]]
    documents: list[dict[str, Any]]
    episodes: list[dict[str, Any]]
    values: dict[str, Any]
    source: str
    manifest_sha256: str


def _is_link(path: Path) -> bool:
    """A symbolic link, or a Windows directory junction, which `is_symlink()` reports as False."""
    return path.is_symlink() or path.is_junction()


def prepare_bundle(pack: Path) -> dict[str, Any]:
    """Read a complete, flat checked-in pack; never execute its JS or access a DB."""
    _require(pack.is_dir() and not _is_link(pack), "pack must be a real directory")
    children = list(pack.iterdir())
    _require({p.name for p in children} == FILE_NAMES, "pack has missing or unexpected files")
    files: dict[str, str] = {}
    for file in children:
        _require(file.is_file() and not _is_link(file), "pack cannot contain symlinks")
        _require(file.stat().st_size <= MAX_FILE_BYTES, f"{file.name}: file too large")
        # Exact bytes matter: changing LF to CRLF requires a new receipt.
        files[file.name] = file.read_bytes().decode("utf-8")
    bundle = {
        "schema_version": 1,
        "artifact_kind": "anime-planning-import",
        "source": f"docs/videos/series-plans/{pack.name}",
        "files": files,
    }
    validate_bundle(bundle)
    return bundle


def _receipt(bundle: dict[str, Any]) -> tuple[dict[str, str], dict[str, Any]]:
    _require(
        set(bundle) == {"schema_version", "artifact_kind", "source", "files"},
        "unexpected bundle fields",
    )
    _require(
        type(bundle["schema_version"]) is int
        and bundle["schema_version"] == 1
        and bundle["artifact_kind"] == "anime-planning-import",
        "invalid bundle kind/version",
    )
    files = bundle["files"]
    _require(
        isinstance(files, dict) and set(files) == FILE_NAMES,
        "bundle has missing or unexpected files",
    )
    _require(
        all(
            isinstance(raw, str)
            and "\x00" not in raw
            and len(raw.encode("utf-8")) <= MAX_FILE_BYTES
            for raw in files.values()
        ),
        "invalid or oversized file content",
    )
    _require(
        len(json.dumps(bundle, ensure_ascii=False).encode("utf-8")) <= MAX_BUNDLE_BYTES,
        "bundle too large",
    )
    manifest = _json(files["manifest.json"], "manifest.json")
    _require(
        type(manifest.get("schema_version")) is int and manifest["schema_version"] == 1,
        "invalid manifest version",
    )
    for group, expected in (
        ("source_files", SOURCE_NAMES),
        ("support_files", SUPPORT_NAMES),
        ("generated_files", GENERATED_NAMES),
    ):
        entries = manifest.get(group)
        _require(
            isinstance(entries, dict) and set(entries) == expected,
            f"{group}: missing, unexpected or unsafe manifest paths",
        )
        assert isinstance(entries, dict)
        for name, digest in entries.items():
            _require(
                isinstance(digest, str) and re.fullmatch(r"[a-f0-9]{64}", digest) is not None,
                f"{name}: invalid manifest hash",
            )
            _require(
                hashlib.sha256(files[name].encode("utf-8")).hexdigest() == digest,
                f"{name}: manifest hash mismatch",
            )
    return files, manifest


def _cell(value: Any) -> str:
    return str(value).replace("|", "／").replace("\n", " ")


def _render(lines: list[str]) -> str:
    return "\n".join(lines).rstrip() + "\n"


def _setting_md(plan: dict[str, Any], setting: dict[str, Any]) -> str:
    lines = [
        f"# {plan['title']}｜設定集",
        "",
        plan["logline"],
        "",
        f"分類：`{plan['category']}`；畫風：`{plan['style_preset']}`；10季×12集。",
        "",
        "本檔由 setting.json 與 plan.json 產生，修改來源後執行 build.mjs。"
        "這是企劃文件，不代表後台核准或媒體完成。",
        "",
        f"## 世界：{setting['world']['name']}",
        "",
        setting["world"]["premise"],
        "",
    ]
    lines += [f"- **{p['name']}：**{p['description']}" for p in setting["world"]["geography"]]
    lines += [
        "",
        "### 古代真相與揭露界線",
        "",
        setting["world"]["hidden_history"],
        "",
        setting["world"]["reveal_policy"],
        "",
        "## 核心規則",
        "",
    ]
    for rule in setting["rules"]:
        lines += [
            f"### {rule['name']}",
            "",
            rule["rule"],
            "",
            f"戲劇代價：{rule['dramatic_cost']}",
            "",
        ]
    lines += ["## 四大勢力", ""]
    for faction in setting["factions"]:
        lines += [
            f"### {faction['name']}",
            "",
            f"資源：{faction['resources']}。",
            "",
            f"需要：{faction['need']}。衝突：{faction['conflict']}。",
            "",
            f"終局交付：{faction['final_contribution']}。",
            "",
        ]
    lines += ["## 人物表", ""]
    for character in setting["characters"]:
        age = f"；登場{character['age_at_start']}歲" if character.get("age_at_start") else ""
        lines += [
            f"### {character['name']}（{character['id']}）",
            "",
            f"{character['role']}{age}。",
            "",
        ]
        for key, label in (
            ("background", "背景"),
            ("ability", "能力"),
            ("limits", "限制"),
            ("arc", "成長與責任"),
            ("ending", "結局"),
        ):
            if character.get(key):
                lines += [f"**{label}：**{character[key]}", ""]
        lines += [f"**外觀基準：**{character['appearance']}", ""]
    lines += [
        "## 長線謎團",
        "",
        "| ID | 問題 | 埋下 | 收束 | 答案 |",
        "| --- | --- | ---: | ---: | --- |",
    ]
    for thread in setting["mysteries"]:
        lines += [
            f"| {thread['id']} | {_cell(thread['question'])} | {thread['introduced_in']} "
            f"| {thread['resolved_in']} | {_cell(thread['answer'])} |"
        ]
    lines += [
        "",
        "中途 payoffs 可以是局部回收，並非整條謎團已解。"
        "最後收束集必須再次列出該謎團，對應真實劇情。",
        "",
        "## 敘事與畫面",
        "",
    ]
    lines += [f"- {text}" for text in setting["narrative_constraints"]]
    lines += [
        "",
        setting["visual_style"],
        "",
        "## 封閉結局",
        "",
        f"八年後的尾聲保留：{'、'.join(setting['finale']['permanent_costs'])}。",
        "",
        f"最後一句：**「{setting['finale']['last_line']}」**",
        "",
    ]
    return _render(lines)


def _season_md(season: dict[str, Any], names: dict[str, str]) -> str:
    episodes = season["episodes"]
    lines = [
        f"# 第{season['number']}季〈{season['title']}〉",
        "",
        f"全劇第{episodes[0]['number']}～{episodes[-1]['number']}集；時間：{season['time_span']}",
        "",
        f"**主題：**{season['theme']}",
        "",
        f"**核心衝突：**{season['core_conflict']}",
        "",
        "正文目標22分鐘；以下是兩段高張力與連貫狀態的細綱，未代替逐場台詞、分鏡或實測媒體。",
        "",
    ]
    for episode in episodes:
        lines += [
            f"## {episode['number']}｜{episode['title']}",
            "",
            episode["logline"],
            "",
            f"**開場：**{episode['hook']}",
            "",
            f"**主要衝突：**{episode['conflict']}",
            "",
            f"**中段轉折：**{episode['turn']}",
            "",
        ]
        for index, beat in enumerate(episode["high_tension"], 1):
            half = "前半" if beat["beat"] == "first_half" else "後半"
            lines += [
                f"**高張力{index}（{half}）：**{beat['event']}",
                "",
                f"賭注：{beat['stakes']}　後果：{beat['consequence']}",
                "",
            ]
        ending = "結尾收束" if episode["closed_ending"] else "結尾懸念"
        cliff = episode["cliffhanger"]
        setups = "、".join(episode["setups"]) or "—"
        payoffs = "、".join(episode["payoffs"]) or "—"
        general = "、".join(episode["general_payoffs"]) or "—"
        curve = " → ".join(map(str, episode["tension"]))
        cast = "、".join(names[c] for c in episode["characters"])
        places = "、".join(episode["locations"])
        lines += [
            f"**{ending}（{cliff['type']}）：**{cliff['text']}",
            "",
            f"**延續後果：**{episode['consequence']}",
            "",
            f"**埋下：**{setups}；**回收：**{payoffs}；**局部成果：**{general}",
            "",
            f"**五段張力：**{curve}（企劃評分，非實測）",
            "",
            f"**出場：**{cast}；**場景：**{places}",
            "",
            f"**主題句：**{episode['theme']}",
            "",
            "<details>",
            "<summary>本集連貫狀態</summary>",
            "",
        ]
        for key, label in zip(
            STATE_FIELDS, ("時間", "已知資訊", "人物狀態", "證據", "後續接續"), strict=True
        ):
            lines += [f"- {label}：{episode['state'][key]}"]
        lines += ["", "</details>", ""]
    lines += [
        "## 本季收束",
        "",
        season["season_resolution"],
        "",
        f"接續：{season['season_hook']}",
        "",
    ]
    return _render(lines)


def _outline_md(
    plan: dict[str, Any], setting: dict[str, Any], seasons: list[dict[str, Any]]
) -> str:
    lines = [
        f"# {plan['title']}｜十季總綱",
        "",
        plan["logline"],
        "",
        "分類 anime，120集，封閉結局。播出時段約30分鐘，正文約22分鐘；原定規格不縮為現行短漫劇。",
        "",
        "## 升級與真相曲線",
        "",
        "| 季 | 集數 | 時間 | 主題 | 核心衝突 |",
        "| --- | --- | --- | --- | --- |",
    ]
    for season in seasons:
        lines += [
            f"| {season['number']} | {season['episodes'][0]['number']}–"
            f"{season['episodes'][-1]['number']} | {_cell(season['time_span'])} | "
            f"{_cell(season['theme'])} | {_cell(season['core_conflict'])} |"
        ]
    for season in seasons:
        lines += [
            "",
            f"## 第{season['number']}季〈{season['title']}〉",
            "",
            f"收束：{season['season_resolution']}",
            "",
            f"接續：{season['season_hook']}",
            "",
            "| 集 | 標題 | 推進 |",
            "| ---: | --- | --- |",
        ]
        lines += [
            f"| {e['number']} | {_cell(e['title'])} | {_cell(e['logline'])} |"
            for e in season["episodes"]
        ]
    lines += [
        "",
        "## 終局",
        "",
        "三座完整天錨與北錨遺址替代樞紐完成首輪安全切換，具名載體真正分區輪休。舊債仍須償還；"
        "第120集跳八年後，沒有新敵、新門或未解異常。最後一句：" + setting["finale"]["last_line"],
        "",
    ]
    return _render(lines)


def _continuity(setting: dict[str, Any], episodes: list[dict[str, Any]]) -> tuple[str, str]:
    def quote(value: Any) -> str:
        return '"' + str(value).replace('"', '""') + '"'

    headers = ["episode", "title", *STATE_FIELDS, "setups", "payoffs", "general_payoffs"]
    rows = []
    for e in episodes:
        values = [
            e["number"],
            e["title"],
            *(e["state"][key] for key in STATE_FIELDS),
            ";".join(e["setups"]),
            ";".join(e["payoffs"]),
            ";".join(e["general_payoffs"]),
        ]
        rows.append(",".join(quote(v) for v in values))
    csv = ",".join(headers) + "\n" + "\n".join(rows) + "\n"
    lines = [
        "# 連貫性與伏筆帳",
        "",
        "各集狀態見 continuity.csv。保留已知與未知界線，角色不因觀眾已看過某場戲就自動知道答案。",
        "",
        "## 時間線",
        "",
        "| 季 | 經過月份 | 內容 |",
        "| --- | ---: | --- |",
    ]
    for item in setting["chronology"]:
        lines += [
            f"| {'、'.join(map(str, item['seasons']))} | {item['elapsed_months']} "
            f"| {item['label']} |"
        ]
    months = sum(item["elapsed_months"] for item in setting["chronology"])
    lines += [
        "",
        f"主線共約{months}個月。第72集之後完整一年試驗加後三季約十四個月，在預測區間內完成首輪退出；三年不是安全保證。",
        "",
        "## 兩小時危機",
        "",
        "54／55／56／57／58：T−120／95／65／35／0分鐘。本地訊號台與鄰區技師並行，不跨國瞬移。",
        "",
        "## 謎團埋回實際位置",
        "",
        "| ID | 埋下或推進集 | 局部或最終回收集 | 最終收束 |",
        "| --- | --- | --- | ---: |",
    ]
    for thread in setting["mysteries"]:
        setups = "、".join(str(e["number"]) for e in episodes if thread["id"] in e["setups"])
        payoffs = "、".join(str(e["number"]) for e in episodes if thread["id"] in e["payoffs"])
        lines += [f"| {thread['id']} | {setups} | {payoffs} | {thread['resolved_in']} |"]
    lines += ["", "## 永久限制", ""]
    lines += [f"- {item}" for item in setting["finale"]["permanent_costs"]]
    lines += [
        "",
        "## 製作界線",
        "",
        "這份帳追蹤的是企劃狀態，未核准劇本、未生成前情摘要、未讀取正式站狀態。人物外觀與能力限制以設定集為準。",
        "",
    ]
    return _render(lines), csv


def _semantics(
    plan: dict[str, Any],
    setting: dict[str, Any],
    contract: dict[str, Any],
    seasons: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    for name, metadata in (("plan", plan), ("authoring contract", contract)):
        _require(
            type(metadata.get("schema_version")) is int and metadata["schema_version"] == 1,
            f"{name}: invalid schema version",
        )
    _require(
        plan.get("artifact_kind") == "anime-series-plan"
        and plan.get("kind") == "series"
        and plan.get("category") == "anime"
        and plan.get("style_preset") == "anime-2d"
        and plan.get("genre") == "custom"
        and plan.get("lead") == "ensemble"
        and plan.get("open_ended") is False,
        "expected a closed ensemble anime series plan",
    )
    for key in ("title", "slug", "logline", "tone", "source_note"):
        _require(_text(plan.get(key)), f"plan requires {key}")
    _require(
        re.fullmatch(r"[a-z0-9][a-z0-9-]{1,39}", plan["slug"]) is not None, "invalid plan slug"
    )
    _require(
        len(plan["title"]) <= 200 and len(plan["logline"]) <= 4000, "title or premise too long"
    )
    for key, expected in (
        ("planned_episodes", 120),
        ("season_count", 10),
        ("episodes_per_chapter", 12),
    ):
        _require(type(plan.get(key)) is int and plan[key] == expected, f"plan: wrong {key}")
    runtime = plan.get("runtime", {})
    for key, expected in (
        ("broadcast_slot_minutes", 30),
        ("story_minutes", 22),
        ("op_ed_budget_minutes", 3),
        ("broadcast_slot_reserve_minutes", 5),
    ):
        _require(
            type(runtime.get(key)) is int and runtime[key] == expected, f"runtime: wrong {key}"
        )
    _require(
        plan.get("video_defaults")
        == {
            "category": "anime",
            "format": "drama",
            "look": {"preset": "anime-2d"},
            "locale": "zh-TW",
        },
        "video defaults drift",
    )
    for key in ("ready_for_import", "admin_series_created", "media_generated", "published"):
        _require(
            plan.get("production_support", {}).get(key) is False,
            "source cannot claim approved production",
        )
    gaps = plan["production_support"].get("gaps")
    _require(isinstance(gaps, list) and bool(gaps), "production gaps must remain explicit")
    assert isinstance(gaps, list)
    by_code: dict[str, dict[str, Any]] = {}
    for gap in gaps:
        _require(
            isinstance(gap, dict) and _text(gap.get("code")) and _text(gap.get("note")),
            "each production gap needs code and note",
        )
        _require(gap["code"] not in by_code, "duplicate production gap")
        by_code[gap["code"]] = gap
    required_gaps: dict[str, dict[str, Any]] = {
        "episode-duration": {"required_story_minutes": 22, "current_drama_max_minutes": 8},
        "ensemble-retention": {"current_genre": "custom"},
        "closed-finale": {
            "episode": 120,
            "planned_last_tension": 2,
            "current_worker_min_last_tension": 4,
        },
        "anime-category": {"pull_request": 1110},
    }
    for code, policy in required_gaps.items():
        _require(
            code in by_code
            and all(
                by_code[code].get(k) == value and type(by_code[code].get(k)) is type(value)
                for k, value in policy.items()
            ),
            f"production gap {code}: missing or changed policy",
        )
    for key in ("slug", "title", "category", "style_preset", "planned_episodes"):
        _require(
            contract.get(key) == plan[key] and type(contract.get(key)) is type(plan[key]),
            f"authoring contract differs: {key}",
        )
    _require(
        type(contract.get("story_minutes")) is int
        and contract["story_minutes"] == 22
        and type(contract.get("broadcast_minutes")) is int
        and contract["broadcast_minutes"] == 30
        and type(contract.get("episodes_per_season")) is int
        and contract["episodes_per_season"] == 12,
        "authoring runtime/count drift",
    )
    cast = setting.get("characters")
    threads = setting.get("mysteries")
    _require(
        isinstance(cast, list)
        and len(cast) >= 4
        and isinstance(threads, list)
        and 8 <= len(threads) <= 12,
        "setting needs cast and long mysteries",
    )
    assert isinstance(cast, list) and isinstance(threads, list)
    ids: set[str] = set()
    for character in cast:
        _require(
            isinstance(character, dict)
            and all(_text(character.get(k)) for k in ("id", "name", "appearance", "role")),
            "invalid character",
        )
        _require(character["id"] not in ids, "duplicate cast ID")
        _require(
            re.fullmatch(r"[a-z][a-z0-9-]{1,23}", character["id"]) is not None,
            "invalid character ID format",
        )
        ids.add(character["id"])
    _require(contract.get("character_ids") == [c["id"] for c in cast], "cast contract differs")
    mysteries: dict[str, dict[str, Any]] = {}
    for thread in threads:
        _require(
            isinstance(thread, dict)
            and all(_text(thread.get(k)) for k in ("id", "question", "answer")),
            "invalid mystery",
        )
        _require(
            thread["id"] not in mysteries
            and _integer(thread.get("introduced_in"), 1, 120)
            and _integer(thread.get("resolved_in"), thread["introduced_in"], 120),
            "duplicate or invalid mystery timeline",
        )
        mysteries[thread["id"]] = thread
    _require(contract.get("thread_ids") == list(mysteries), "thread contract differs")
    _require(contract.get("state_fields") == list(STATE_FIELDS), "state contract differs")
    _require(
        isinstance(setting.get("rules"), list)
        and len(setting["rules"]) >= 4
        and isinstance(setting.get("factions"), list)
        and len(setting["factions"]) == 4,
        "setting needs rules and four factions",
    )
    for rule in setting["rules"]:
        _require(
            isinstance(rule, dict)
            and all(_text(rule.get(k)) for k in ("name", "rule", "dramatic_cost")),
            "incomplete world rule",
        )
    for faction in setting["factions"]:
        _require(
            isinstance(faction, dict)
            and all(
                _text(faction.get(k))
                for k in ("name", "resources", "need", "conflict", "final_contribution")
            ),
            "incomplete faction",
        )
    world = setting.get("world", {})
    _require(
        isinstance(world, dict)
        and all(_text(world.get(k)) for k in ("name", "premise", "hidden_history", "reveal_policy"))
        and isinstance(world.get("geography"), list)
        and bool(world["geography"]),
        "incomplete world",
    )
    for place in world["geography"]:
        _require(
            isinstance(place, dict)
            and _text(place.get("name"))
            and _text(place.get("description")),
            "incomplete geography",
        )
    chronology = setting.get("chronology")
    _require(isinstance(chronology, list) and bool(chronology), "missing chronology")
    assert isinstance(chronology, list)
    covered = []
    for item in chronology:
        _require(
            isinstance(item, dict)
            and _integer(item.get("elapsed_months"), 1, 120)
            and _text(item.get("label"))
            and isinstance(item.get("seasons"), list)
            and all(_integer(n, 1, 10) for n in item["seasons"]),
            "invalid chronology",
        )
        covered += item["seasons"]
    _require(sorted(covered) == list(range(1, 11)), "chronology must cover all seasons once")
    finale = setting.get("finale", {})
    _require(
        finale.get("closed") is True
        and finale.get("new_crisis_or_sequel_hook") is False
        and type(finale.get("epilogue_years")) is int
        and finale["epilogue_years"] == 8
        and _text(finale.get("last_line"))
        and isinstance(finale.get("permanent_costs"), list)
        and len(finale["permanent_costs"]) >= 4
        and all(_text(cost) for cost in finale["permanent_costs"]),
        "invalid closed finale",
    )
    episodes: list[dict[str, Any]] = []
    for number, season in enumerate(seasons, 1):
        _require(
            type(season.get("number")) is int
            and season["number"] == number
            and all(_text(season.get(k)) for k in SEASON_TEXT),
            "invalid season metadata",
        )
        _require(
            isinstance(season.get("episodes"), list) and len(season["episodes"]) == 12,
            "each season needs twelve episodes",
        )
        for e in season["episodes"]:
            expected = len(episodes) + 1
            _require(
                isinstance(e, dict) and type(e.get("number")) is int and e["number"] == expected,
                "episodes must be ordered 1 through 120",
            )
            _require(
                set(contract["episode_fields"]).issubset(e)
                and all(_text(e.get(k)) for k in EPISODE_TEXT)
                and len(e["title"]) <= 200,
                f"episode {expected}: missing narrative fields",
            )
            for key in ("characters", "locations", "setups", "payoffs", "general_payoffs"):
                values = e.get(key)
                _require(
                    isinstance(values, list)
                    and all(_text(v) for v in values)
                    and len(values) == len(set(values)),
                    f"episode {expected}: invalid {key}",
                )
            _require(
                bool(e["characters"])
                and set(e["characters"]).issubset(ids)
                and bool(e["locations"]),
                f"episode {expected}: invalid cast/location",
            )
            state = e.get("state")
            _require(
                isinstance(state, dict) and all(_text(state.get(k)) for k in STATE_FIELDS),
                f"episode {expected}: incomplete continuity state",
            )
            high = e.get("high_tension")
            _require(
                isinstance(high, list)
                and len(high) == 2
                and all(
                    isinstance(b, dict)
                    and all(_text(b.get(k)) for k in ("event", "stakes", "consequence"))
                    for b in high
                )
                and [b.get("beat") for b in high] == ["first_half", "second_half"]
                and high[0]["event"] != high[1]["event"],
                f"episode {expected}: requires two distinct high-tension events",
            )
            curve = e.get("tension")
            _require(
                isinstance(curve, list)
                and len(curve) == 5
                and all(_integer(n, 1, 5) for n in curve)
                and len(set(curve)) > 1,
                f"episode {expected}: invalid tension curve",
            )
            cliff = e.get("cliffhanger")
            _require(
                isinstance(cliff, dict)
                and cliff.get("type") in ENDING_TYPES
                and _text(cliff.get("text")),
                f"episode {expected}: invalid ending",
            )
            if expected == 120:
                _require(
                    curve[-1] == by_code["closed-finale"]["planned_last_tension"],
                    "finale tension differs from declared production policy",
                )
                _require(
                    e.get("closed_ending") is True
                    and curve[-1] <= 3
                    and cliff["type"] == "emotion",
                    "finale must close without new danger",
                )
            else:
                _require(
                    e.get("closed_ending") is False and curve[-1] >= 4,
                    f"episode {expected}: invalid continuing ending",
                )
                if episodes:
                    _require(
                        cliff["type"] != episodes[-1]["cliffhanger"]["type"],
                        f"episode {expected}: consecutive ending type",
                    )
            for key in ("setups", "payoffs"):
                for thread_id in e[key]:
                    _require(
                        thread_id in mysteries
                        and expected >= mysteries[thread_id]["introduced_in"],
                        f"episode {expected}: unknown or premature thread {thread_id}",
                    )
            episodes.append(e)
    for thread_id, thread in mysteries.items():
        _require(
            thread_id in episodes[thread["introduced_in"] - 1]["setups"]
            and thread_id in episodes[thread["resolved_in"] - 1]["payoffs"],
            f"{thread_id}: missing introduction or final payoff",
        )
    for start in range(117):
        _require(
            any(e["payoffs"] or e["general_payoffs"] for e in episodes[start : start + 4]),
            f"episodes {start + 1}-{start + 4}: no local result or mystery payoff",
        )
    return episodes


def validate_bundle(bundle: dict[str, Any]) -> ValidatedPlan:
    """Validate receipts, semantics, projections and every generated readable document."""
    try:
        files, manifest = _receipt(bundle)
        plan = _json(files["plan.json"], "plan.json")
        setting = _json(files["setting.json"], "setting.json")
        contract = _json(files["authoring-contract.json"], "authoring-contract.json")
        seasons = [_json(files[f"season-{n:02}.json"], f"season-{n:02}.json") for n in range(1, 11)]
        episodes = _semantics(plan, setting, contract, seasons)
        _require(
            bundle["source"] == f"docs/videos/series-plans/{plan['slug']}",
            "source path must match plan slug",
        )
        for key, value in (
            ("slug", plan["slug"]),
            ("category", "anime"),
            ("episode_count", 120),
            ("season_count", 10),
            ("artifact_kind", "anime-series-plan"),
        ):
            _require(
                manifest.get(key) == value and type(manifest.get(key)) is type(value),
                f"manifest {key} differs",
            )
        for key in ("ready_for_import", "admin_series_created", "media_generated", "published"):
            _require(manifest.get(key) is False, "source manifest cannot claim production")
        outline = {
            "chapters": [
                {
                    "number": s["number"],
                    "title": s["title"],
                    "theme": s["theme"],
                    "episodes": [
                        {k: e[k] for k in ("number", "title", "logline")} for e in s["episodes"]
                    ],
                }
                for s in seasons
            ]
        }
        _require(
            _same(_json(files["outline.json"], "outline.json"), outline),
            "outline projection differs from source",
        )
        names = {c["id"]: c["name"] for c in setting["characters"]}
        rendered = {
            "setting.md": _setting_md(plan, setting),
            "outline.md": _outline_md(plan, setting, seasons),
        }
        rendered.update({f"season-{s['number']:02}.md": _season_md(s, names) for s in seasons})
        rendered["continuity.md"], rendered["continuity.csv"] = _continuity(setting, episodes)
        for name, raw in rendered.items():
            _require(files[name] == raw, f"{name}: rendered content differs from source")
        documents = [
            {"kind": "setting", "body_md": rendered["setting.md"], "body_json": setting},
            {"kind": "outline", "body_md": rendered["outline.md"], "body_json": outline},
        ]
        documents += [
            {
                "kind": "chapter",
                "chapter_number": s["number"],
                "body_md": rendered[f"season-{s['number']:02}.md"],
                "body_json": s,
            }
            for s in seasons
        ]
        submitted = _json(files["documents.json"], "documents.json")
        _require(
            type(submitted.get("schema_version")) is int
            and submitted["schema_version"] == 1
            and submitted.get("stage") == "planning"
            and submitted.get("category") == "anime"
            and submitted.get("ready_for_import") is False
            and _same({"documents": submitted.get("documents")}, {"documents": documents}),
            "document twins differ from source",
        )
        values = {
            "slug": plan["slug"],
            "title": plan["title"],
            "premise": plan["logline"],
            "kind": "series",
            "aspects": ["world", "bonds", "structure", "mood"],
            "tone": "no-romance",
            "style_preset": "anime-2d",
            "target_minutes": 22,
            "planned_episodes": 120,
            "episodes_per_chapter": 12,
            "open_ended": False,
            "status": "paused",
            "note": "原創長篇動漫企劃待審；保留22分鐘正文，尚未支援製作。",
            "genre": "custom",
            "lead": "ensemble",
            "hands_off": False,
            "compilation": False,
            "visual_tier": "clips",
            "total_minutes": None,
            "requested_chapter": None,
            "force_next": False,
            "category": "anime",
            "planning_only": True,
            "planning_spec": plan,
            "episodes_per_day": None,
            "image_model": None,
            "look": None,
            "compilation_slug": None,
            "compilation_started_at": None,
            "compilation_finished_at": None,
        }
        return ValidatedPlan(
            plan,
            setting,
            seasons,
            documents,
            episodes,
            values,
            bundle["source"],
            hashlib.sha256(files["manifest.json"].encode()).hexdigest(),
        )
    except (KeyError, TypeError, AttributeError, IndexError, OverflowError) as error:
        raise ValueError("malformed anime planning bundle") from error


async def import_plan(
    session: AsyncSession, bundle: dict[str, Any], *, actor: User | None = None
) -> dict[str, Any]:
    """Preflight without writes, or insert exactly one paused source-bound review plan."""
    validated = validate_bundle(bundle)
    digest = bundle_hash(bundle)
    values = validated.values
    slug = values["slug"]
    audit_metadata = {
        "source": validated.source,
        "manifest_sha256": validated.manifest_sha256,
        "bundle_sha256": digest,
        "documents": 12,
        "episodes": 120,
        "status": "paused",
        "planning_only": True,
    }
    if actor is not None:
        _require(
            actor.is_active
            and (actor.is_admin or actor.email.lower() in get_settings().admin_email_set),
            "an active administrator is required",
        )
    with session.no_autoflush:
        query = select(VideoDramaSeries).where(VideoDramaSeries.slug == slug)
        if actor is not None:
            query = query.with_for_update()
        current = await session.scalar(query)
        videos = await session.scalar(
            select(VideoProject.id).where(
                or_(
                    VideoProject.series_slug == slug,
                    VideoProject.slug == slug,
                    VideoProject.slug.like(f"{slug}-e%"),
                )
            )
        )
        request_query = select(VideoDramaRequest.id).where(
            or_(VideoDramaRequest.slug == slug, VideoDramaRequest.slug.like(f"{slug}-e%"))
        )
        if current is not None:
            request_query = select(VideoDramaRequest.id).where(
                or_(
                    VideoDramaRequest.series_id == current.id,
                    VideoDramaRequest.slug == slug,
                    VideoDramaRequest.slug.like(f"{slug}-e%"),
                )
            )
        requests = await session.scalar(request_query)
        _require(
            videos is None and requests is None, f"{slug}: existing production records collide"
        )
        audits = list(
            await session.scalars(
                select(AdminAuditLog).where(
                    AdminAuditLog.action == ACTION, AdminAuditLog.target == f"video-series:{slug}"
                )
            )
        )
        _require(current is not None or not audits, f"{slug}: orphaned import audit collides")
        if current is not None:
            docs = list(
                await session.scalars(
                    select(VideoDramaDoc).where(VideoDramaDoc.series_id == current.id)
                )
            )
            episodes = list(
                await session.scalars(
                    select(VideoDramaEpisode)
                    .where(VideoDramaEpisode.series_id == current.id)
                    .order_by(VideoDramaEpisode.number)
                )
            )
            wanted_docs = {(d["kind"], d.get("chapter_number", 0)): d for d in validated.documents}
            same = (
                _same({k: getattr(current, k) for k in values}, values)
                and len(docs) == 12
                and len(episodes) == 120
                and len(audits) == 1
                and _same(audits[0].metadata_json, audit_metadata)
                and current.created_by_user_id == audits[0].actor_user_id
            )
            seen = set()
            for doc in docs:
                key = (doc.kind, doc.chapter_number)
                wanted = wanted_docs.get(key)
                same = same and (
                    key not in seen
                    and wanted is not None
                    and doc.version == 1
                    and doc.status == "review"
                    and doc.note is None
                    and doc.decided_at is None
                    and doc.decided_by_user_id is None
                    and doc.body_md == wanted["body_md"]
                    and _same(doc.body_json, wanted["body_json"])
                )
                seen.add(key)
            for episode, wanted in zip(episodes, validated.episodes, strict=False):
                same = same and (
                    episode.number == wanted["number"]
                    and episode.chapter_number == (episode.number - 1) // 12 + 1
                    and episode.title == wanted["title"]
                    and episode.logline == wanted["logline"]
                    and _same(episode.beats, wanted)
                    and episode.status == "planned"
                    and episode.slug is None
                    and episode.request_id is None
                    and episode.recap is None
                    and episode.state_json == {}
                    and episode.started_at is None
                    and episode.finished_at is None
                )
            _require(same, f"{slug}: existing work differs; import refused")
        elif actor is not None:
            now = datetime.now(UTC)
            row = VideoDramaSeries(
                id=uuid4(), **values, created_by_user_id=actor.id, created_at=now, updated_at=now
            )
            session.add(row)
            await session.flush()
            session.add_all(
                [
                    VideoDramaDoc(
                        id=uuid4(),
                        series_id=row.id,
                        kind=d["kind"],
                        chapter_number=d.get("chapter_number", 0),
                        version=1,
                        body_md=d["body_md"],
                        body_json=d["body_json"],
                        status="review",
                        created_at=now,
                    )
                    for d in validated.documents
                ]
            )
            session.add_all(
                [
                    VideoDramaEpisode(
                        id=uuid4(),
                        series_id=row.id,
                        number=e["number"],
                        chapter_number=(e["number"] - 1) // 12 + 1,
                        title=e["title"],
                        logline=e["logline"],
                        beats=e,
                        status="planned",
                        state_json={},
                        created_at=now,
                        updated_at=now,
                    )
                    for e in validated.episodes
                ]
            )
            session.add(
                AdminAuditLog(
                    actor_user_id=actor.id,
                    action=ACTION,
                    target=f"video-series:{slug}",
                    metadata_json=audit_metadata,
                )
            )
            await session.flush()
    return {
        "slug": slug,
        "title": values["title"],
        "action": "create" if current is None else "unchanged",
        "documents": 12,
        "episodes": 120,
        "category": "anime",
        "status": "paused",
        "planning_only": True,
        "applied": actor is not None,
        "sha256": digest,
    }
