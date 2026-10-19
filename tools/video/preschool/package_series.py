"""Package a completed 48-episode preschool series into four offline season ZIPs.

Run after the audio/render batch has completed. This command validates existing
media checks; it does not synthesize, render, decode, or publish any media.
Legacy sidecars are read-only compared with their checked final streams.
"""

from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
import hashlib
import json
import math
import os
from pathlib import Path
import shutil
import tempfile
from typing import Any
import zipfile

from player import write_player
from audio import PipelineError, audio_integrity, verify_picture_artifact


AUDIO_LOCALES = ("zh-TW", "en", "zh-CN", "ja", "ko")
CC_LOCALES = ("zh-TW", "zh-CN", "ja", "ko")
SEASON_NAMES = {
    1: "初次開口",
    2: "我的身體與一天",
    3: "身邊的世界",
    4: "一起玩、說短句",
}
CATALOG_NAME = "幼兒英文48集課程目錄.csv"
EPISODE_FILES = (
    "final.mp4", "picture.mp4", "poster.jpg", "checks.json",
    *(f"audio/{locale}.m4a" for locale in AUDIO_LOCALES),
    *(f"captions/{locale}.{extension}" for locale in CC_LOCALES for extension in ("srt", "vtt")),
)


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def fingerprint(value: dict[str, Any]) -> str:
    # Keep identical to build.fingerprint without importing the rendering stack.
    data = json.dumps(value, ensure_ascii=False, sort_keys=True).encode()
    return hashlib.sha256(data).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def preflight(resolved: dict[str, Any], output: Path) -> tuple[list[dict], dict[str, dict]]:
    """Reject incomplete, stale, or unchecked media before creating any package."""
    episodes = resolved.get("episodes")
    require(isinstance(episodes, list) and len(episodes) == 48,
            "Resolved lessons must contain exactly 48 episodes")
    expected_ids = [f"ep{number:02d}" for number in range(1, 49)]
    require(all(isinstance(episode, dict) for episode in episodes), "Invalid episode record")
    require(sorted(episode.get("id", "") for episode in episodes) == expected_ids,
            "Resolved lessons must contain each ID ep01–ep48 exactly once")
    episodes = sorted(episodes, key=lambda episode: episode["id"])
    records: dict[str, dict] = {}
    for number, episode in enumerate(episodes, 1):
        episode_id = episode["id"]
        season = (number - 1) // 12 + 1
        require(episode.get("number") == number and episode.get("season") == season,
                f"{episode_id}: episode number or season does not match the curriculum")
        duration = episode.get("duration")
        require(isinstance(duration, (int, float)) and math.isfinite(duration) and 180 <= duration <= 300,
                f"{episode_id}: missing or invalid measured duration")
        require(bool(episode.get("title_zh_TW")) and bool(episode.get("objectives_zh_TW")),
                f"{episode_id}: title or learning objectives are missing")
        directory = output / episode_id
        for relative in EPISODE_FILES:
            path = directory / relative
            require(path.is_file() and path.stat().st_size > 0, f"Missing or empty required file: {path}")
        record = json.loads((directory / "checks.json").read_text(encoding="utf-8"))
        require(isinstance(record, dict), f"{episode_id}: invalid checks.json")
        require(record.get("episode") == episode_id and record.get("full_decode") is True,
                f"{episode_id}: completed full-decode check is required")
        require(record.get("audio_tracks") == list(AUDIO_LOCALES),
                f"{episode_id}: checks must confirm all five audio tracks")
        require(record.get("cc_tracks") == list(CC_LOCALES) and record.get("english_cc") is False,
                f"{episode_id}: checks must confirm four CC languages and no English CC")
        require(record.get("english_text") == "embedded into picture",
                f"{episode_id}: embedded English text has not been confirmed")
        measured = record.get("duration")
        require(isinstance(measured, (int, float)) and math.isfinite(measured)
                and abs(measured - duration) < 0.2,
                f"{episode_id}: checked duration differs from resolved timing")
        require(record.get("source_sha256") == fingerprint(episode),
                f"{episode_id}: checks are stale for this resolved lesson")
        final = directory / "final.mp4"
        require(record.get("bytes") == final.stat().st_size
                and record.get("final_sha256") == file_sha256(final),
                f"{episode_id}: final.mp4 does not match its completed checks")
        audio_integrity(episode, output, final_bound=True)
        verify_picture_artifact(episode, output)
        records[episode_id] = record
    return episodes, records


def write_catalog(path: Path, episodes: list[dict], records: dict[str, dict]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(["集數", "季數", "季名", "標題", "英文標題", "學習目標", "時長", "時長（秒）"])
        for episode in episodes:
            duration = float(records[episode["id"]]["duration"])
            minutes, seconds = divmod(round(duration), 60)
            objectives = episode["objectives_zh_TW"]
            goal = "；".join(str(value) for value in objectives) if isinstance(objectives, list) else str(objectives)
            writer.writerow([
                episode["number"], episode["season"], SEASON_NAMES[episode["season"]],
                episode["title_zh_TW"], episode.get("title_en", ""), goal,
                f"{minutes}:{seconds:02d}", f"{duration:.3f}",
            ])


def write_readme(path: Path, episodes: list[dict]) -> None:
    first, last = episodes[0]["number"], episodes[-1]["number"]
    path.write_text(
        f"Sunny 與 Pip 的幼兒英文小花園｜第 {first}–{last} 集（共 {len(episodes)} 集）\n\n"
        "播放方式\n"
        "1. 請先完整解壓縮 ZIP，保留資料夾結構，再用瀏覽器開啟 index.html。\n"
        "2. 選擇集數後，可分別選擇教學配音與翻譯字幕 CC，然後按播放。\n"
        "3. 也可用 VLC 開啟 epXX/final.mp4，在音訊軌與字幕軌選單切換語言。\n"
        "4. 若瀏覽器限制本機音訊播放，請改用 VLC 播放 final.mp4。\n\n"
        "字幕與聲音\n"
        "英文字幕固定在影片畫面中，沒有另外提供英文 CC。\n"
        "配音包含英文、繁體中文、簡體中文、日文、韓文，共五組；英文示範保持英文發音。\n"
        "可切換 CC 包含繁體中文、簡體中文、日文、韓文，共四組。\n"
        "聽力挑戰等待時先不顯示答案，完整等待後才揭答。\n"
        "本系列使用 Microsoft Edge 合成配音試製，尚未套用後台正式聲音，也未在後台發布。\n\n"
        "檔案說明\n"
        "每集 final.mp4 含五組音軌與四組 CC；picture.mp4 是無聲畫面。\n"
        "audio 資料夾提供各語言 M4A；captions 資料夾提供四語 SRT 與 VTT。\n"
        "checks.json 是該集成片檢查紀錄；課程目錄 CSV 使用 UTF-8 BOM，可用試算表開啟。\n"
        "可依孩子的反應暫停或重播；用指認、動作或聲音回應都可以。\n",
        encoding="utf-8",
    )


def stage_package(resolved: dict, episodes: list[dict], records: dict[str, dict],
                  media: Path, destination: Path) -> None:
    destination.mkdir(parents=True)
    for episode in episodes:
        for relative in EPISODE_FILES:
            source = media / episode["id"] / relative
            target = destination / episode["id"] / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            try:
                os.link(source, target)
            except OSError:
                # A cross-device or unsupported hard link may require a copy.
                shutil.copy2(source, target)
    write_player({**resolved, "episodes": episodes}, destination)
    write_readme(destination / "README.txt", episodes)
    catalog = CATALOG_NAME if len(episodes) == 48 else "本季課程目錄.csv"
    write_catalog(destination / catalog, episodes, records)


def create_archive(directory: Path, path: Path, episodes: list[dict]) -> dict:
    """Archive only the allowlisted files, then read every entry to verify CRCs."""
    files = sorted(item for item in directory.rglob("*") if item.is_file())
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6,
                         allowZip64=True) as archive:
        for item in files:
            # Media is already compressed; storing it avoids an expensive second pass.
            compression = zipfile.ZIP_STORED if item.suffix in {".mp4", ".m4a", ".jpg"} else zipfile.ZIP_DEFLATED
            archive.write(item, item.relative_to(directory.parent).as_posix(), compress_type=compression)
    with zipfile.ZipFile(path) as archive:
        require(archive.testzip() is None, f"ZIP integrity check failed: {path.name}")
        names = archive.namelist()
        require(len(names) == len(set(names)), f"Duplicate archive entries: {path.name}")
        expected_ids = {episode["id"] for episode in episodes}
        final_ids = {Path(name).parts[-2] for name in names if name.endswith("/final.mp4")}
        require(final_ids == expected_ids, f"Episode count or membership mismatch: {path.name}")
        require(len(names) == len(episodes) * len(EPISODE_FILES) + 3,
                f"Unexpected file count in {path.name}")
        require(not any(name.endswith(("/en.srt", "/en.vtt")) for name in names),
                f"English CC unexpectedly included in {path.name}")
    return {
        "file": path.name, "bytes": path.stat().st_size, "sha256": file_sha256(path),
        "episode_ids": [episode["id"] for episode in episodes], "episodes": len(episodes),
        "files": len(files), "video_files": len(episodes) * 2,
        "audio_files": len(episodes) * len(AUDIO_LOCALES),
        "caption_files": len(episodes) * len(CC_LOCALES) * 2,
        "zip_testzip": "passed", "english_cc": False,
    }


def package_series(resolved_path: Path, output: Path, all_zip: bool = False) -> dict:
    resolved_path, output = resolved_path.resolve(), output.resolve()
    repository = Path(__file__).resolve().parents[3]
    require(output != repository and repository not in output.parents,
            "Media packages must be outside the public repository")
    require(output.is_dir(), f"Media output directory does not exist: {output}")
    resolved = json.loads(resolved_path.read_text(encoding="utf-8"))
    require(isinstance(resolved, dict), "Resolved lessons must be a JSON object")
    episodes, records = preflight(resolved, output)
    with tempfile.TemporaryDirectory(prefix=".package-series-", dir=output) as temporary:
        staging = Path(temporary)
        packages = []
        for season in range(1, 5):
            selected = [episode for episode in episodes if episode["season"] == season]
            require(len(selected) == 12, f"Season {season} must contain exactly 12 episodes")
            directory = staging / "Seasons" / f"Season_{season:02d}"
            stage_package(resolved, selected, records, output, directory)
            archive = staging / f"Sunny_Pip_Season_{season:02d}.zip"
            result = create_archive(directory, archive, selected)
            result["season"] = season
            packages.append(result)
        if all_zip:
            directory = staging / "All_48_Episodes"
            stage_package(resolved, episodes, records, output, directory)
            packages.append(create_archive(directory, staging / "Sunny_Pip_48_Episodes.zip", episodes))
        catalog = staging / CATALOG_NAME
        write_catalog(catalog, episodes, records)
        report = {
            "ready": True, "created_at": datetime.now(timezone.utc).isoformat(),
            "resolved_sha256": file_sha256(resolved_path), "episode_count": 48, "season_count": 4,
            "audio_locales": list(AUDIO_LOCALES), "cc_locales": list(CC_LOCALES),
            "english_cc": False,
            "validation": "Final full-decode checks/SHA-256 and source-bound sidecar hashes; legacy sidecars compared with checked final encoded packets/timestamps and resolved captions. ZIP CRCs and contents checked.",
            "packages": packages,
            "catalog": {"file": CATALOG_NAME, "rows": 48, "bytes": catalog.stat().st_size,
                        "sha256": file_sha256(catalog), "encoding": "UTF-8 BOM"},
        }
        # Publish only after every requested archive passed verification.
        for package in packages:
            (staging / package["file"]).replace(output / package["file"])
        catalog.replace(output / CATALOG_NAME)
        checks = staging / "package-checks.json"
        checks.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        checks.replace(output / "package-checks.json")
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--resolved", type=Path, required=True, help="completed lessons.resolved.json")
    parser.add_argument("--output", type=Path, required=True, help="existing ep01–ep48 media directory")
    parser.add_argument("--all-zip", action="store_true", help="also build Sunny_Pip_48_Episodes.zip")
    parser.add_argument("--check-only", action="store_true", help="validate every package input without writing files or ZIPs")
    args = parser.parse_args()
    try:
        if args.check_only:
            resolved = json.loads(args.resolved.read_text(encoding="utf-8"))
            episodes, _ = preflight(resolved, args.output.resolve())
            print(f"VERIFIED {len(episodes)} episodes; no media or ZIPs changed", flush=True)
            return
        report = package_series(args.resolved, args.output, args.all_zip)
    except (PipelineError, OSError, ValueError, zipfile.BadZipFile) as error:
        parser.exit(1, f"Packaging failed: {error}\n")
    for package in report["packages"]:
        print(f"READY {package['file']}: {package['episodes']} episodes, {package['bytes']} bytes", flush=True)
    print(f"READY {CATALOG_NAME}; package-checks.json", flush=True)


if __name__ == "__main__":
    main()
