"""Validate and package the twelve-episode elementary first season offline."""
from __future__ import annotations

import argparse
import csv
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile
import zipfile

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from elementary.shared import audio, build, package as shared_package, verify as shared_verify
from elementary.profile import RENDERER
from elementary.player import SEASON_NAME, write_player
from elementary.verify_series import verify_media, verify_structure

CATALOG_NAME = "國小低年級英文第一季12集課程目錄.csv"
ARCHIVE_NAME = "Sunny_Pip_Elementary_Season_01.zip"
EPISODE_FILES = shared_package.EPISODE_FILES


def preflight(resolved: dict, output: Path) -> tuple[list[dict], dict[str, dict]]:
    verify_structure(resolved)
    episodes = resolved["episodes"]
    records = {}
    for episode in episodes:
        eid = episode["id"]
        directory = output / eid
        for relative in EPISODE_FILES:
            path = directory / relative
            shared_verify.require(path.is_file() and path.stat().st_size > 0, f"Missing or empty required file: {path}")
        record = audio.read_json(directory / "checks.json")
        verify_media(episode, output, record)
        audio.audio_integrity(episode, output, final_bound=True)
        shared_verify.verify_captions(episode, output)
        build.require_picture(episode, output, 15, renderer_profile=RENDERER)
        audio.verify_picture_artifact(episode, output)
        records[eid] = record
    return episodes, records


def write_catalog(path: Path, episodes: list[dict], records: dict[str, dict]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(["集數", "季數", "季名", "標題", "英文標題", "學習目標", "時長", "時長（秒）"])
        for episode in episodes:
            seconds = float(records[episode["id"]]["duration"])
            minutes, remainder = divmod(round(seconds), 60)
            writer.writerow([episode["number"], 1, SEASON_NAME, episode["title_zh_TW"], episode["title_en"],
                             "；".join(episode["objectives_zh_TW"]), f"{minutes}:{remainder:02d}", f"{seconds:.3f}"])


def write_readme(path: Path) -> None:
    path.write_text(
        "Sunny 與 Pip 的英文教室｜國小低年級第一季｜12 集\n\n"
        "完整解壓縮 ZIP、保留資料夾結構，再用瀏覽器開啟 index.html。\n"
        "選擇集數、教學配音與翻譯字幕 CC，再按播放；配音與 CC 可以分別選擇。\n"
        "若瀏覽器限制本機音訊，請用 VLC 開啟 epXX/final.mp4，切換音訊軌與字幕軌。\n\n"
        "英文固定顯示在畫面，沒有英文 CC。配音含英文、繁體中文、簡體中文、日文、韓文五組；\n"
        "四語教學聲軌都使用同一段英文示範。CC 提供繁體中文、簡體中文、日文、韓文。\n"
        "聽力挑戰先聽英文，等待六秒後揭答；一般練習保留五秒回應時間。\n\n"
        "每集 final.mp4 含五音軌與四 CC；picture.mp4 是無聲畫面。\n"
        "audio/ 提供五語 M4A；captions/ 提供四語 SRT、VTT；checks.json 保存成片檢查紀錄。\n"
        "課程目錄 CSV 使用 UTF-8 BOM，可用試算表開啟。\n\n"
        "本季適合約 6–8 歲、剛開始學英文的孩子，依程度調整進度。\n"
        "先聽懂、指認、跟說，再和同伴交換一句話；可以暫停或重播。\n"
        "目前使用 Microsoft Edge 合成配音試製，尚未套用後台正式聲音，也未在後台發布。\n",
        encoding="utf-8",
    )


def package_series(resolved_path: Path, output: Path) -> dict:
    resolved_path, output = resolved_path.resolve(), output.resolve()
    repository = Path(__file__).resolve().parents[3]
    shared_verify.require(output != repository and repository not in output.parents,
                          "Media packages must be outside the public repository")
    resolved = audio.read_json(resolved_path)
    episodes, records = preflight(resolved, output)
    with tempfile.TemporaryDirectory(prefix=".package-elementary-", dir=output) as temporary:
        staging = Path(temporary)
        directory = staging / "Elementary_Season_01"
        directory.mkdir()
        for episode in episodes:
            for relative in EPISODE_FILES:
                source = output / episode["id"] / relative
                target = directory / episode["id"] / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                try:
                    os.link(source, target)
                except OSError:
                    shutil.copy2(source, target)
        write_player(resolved, directory)
        write_readme(directory / "README.txt")
        catalog = directory / CATALOG_NAME
        write_catalog(catalog, episodes, records)
        archive = staging / ARCHIVE_NAME
        packaged = shared_package.create_archive(directory, archive, episodes)
        report = {
            "ready": True, "created_at": audio.stamp(), "episode_count": 12, "season_count": 1,
            "resolved_sha256": build.file_sha256(resolved_path), "renderer_profile": RENDERER.name,
            "audio_locales": list(build.LOCALES), "cc_locales": list(build.SUBTITLES), "english_cc": False,
            "validation": "Elementary renderer, source and artifact hashes, exact CC timing, full-decode receipts, and ZIP CRCs and contents.",
            "packages": [{**packaged, "season": 1}],
            "catalog": {"file": CATALOG_NAME, "rows": 12, "encoding": "UTF-8 BOM",
                        "bytes": catalog.stat().st_size, "sha256": build.file_sha256(catalog)},
        }
        archive.replace(output / ARCHIVE_NAME)
        shutil.copy2(catalog, output / CATALOG_NAME)
        audio.atomic_json(output / "package-checks.json", report)
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--resolved", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--check-only", action="store_true")
    args = parser.parse_args()
    try:
        if args.check_only:
            episodes, _ = preflight(audio.read_json(args.resolved), args.output.resolve())
            print(f"VERIFIED {len(episodes)} elementary episodes; no files changed")
        else:
            report = package_series(args.resolved, args.output)
            package = report["packages"][0]
            print(f"READY {package['file']}: {package['episodes']} episodes, {package['bytes']} bytes")
            print(f"READY {CATALOG_NAME}; package-checks.json")
    except (audio.PipelineError, shared_verify.VerificationError, OSError, ValueError, KeyError, zipfile.BadZipFile) as error:
        parser.exit(1, f"Packaging failed: {error}\n")


if __name__ == "__main__":
    main()
