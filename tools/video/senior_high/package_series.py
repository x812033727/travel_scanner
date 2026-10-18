"""Validate and package all 72 senior-high lessons as six seasons and one collection."""
from __future__ import annotations

import argparse
import csv
from pathlib import Path
import os
import shutil
import sys
import tempfile
import zipfile

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from senior_high.shared import audio, build, package as shared_package, verify as shared_verify
from senior_high.profile import RENDERER
from senior_high.player import GRADE_BANDS, SEASON_NAMES, write_player
from senior_high.verify_series import verify_output, verify_structure

CATALOG_NAME = "高中英文72集課程目錄.csv"
ALL_ARCHIVE_NAME = "Sunny_Pip_Senior_High_72_Episodes.zip"
EPISODE_FILES = shared_package.EPISODE_FILES


def write_practice(episodes: list[dict], destination: Path) -> list[Path]:
    # Keep optional PDF dependencies out of verification and ordinary CI imports.
    from senior_high.practice import write_practice as produce
    return produce(episodes, destination)


def create_archive(directory: Path, path: Path, episodes: list[dict]) -> dict:
    """Archive exactly the media allowlist, player, catalog and two practice files."""
    catalog = CATALOG_NAME if len(episodes) == 72 else "本季課程目錄.csv"
    expected = {Path(episode["id"]) / relative for episode in episodes for relative in EPISODE_FILES}
    expected.update(Path(name) for name in ("index.html", "README.txt", catalog, "Practice.html", "Practice.pdf"))
    actual = {item.relative_to(directory) for item in directory.rglob("*") if item.is_file()}
    shared_verify.require(actual == expected, f"Unexpected or missing package files in {directory.name}")
    shared_verify.require(all((directory / relative).stat().st_size > 0 for relative in expected),
                          f"Empty package file in {directory.name}")
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6,
                         allowZip64=True) as archive:
        for relative in sorted(expected):
            compression = zipfile.ZIP_STORED if relative.suffix in {".mp4", ".m4a", ".jpg"} else zipfile.ZIP_DEFLATED
            archive.write(directory / relative, (Path(directory.name) / relative).as_posix(), compress_type=compression)
    with zipfile.ZipFile(path) as archive:
        shared_verify.require(archive.testzip() is None, f"ZIP integrity check failed: {path.name}")
        names = archive.namelist()
        shared_verify.require(len(names) == len(expected) and len(names) == len(set(names)),
                              f"Duplicate or missing ZIP entries: {path.name}")
        shared_verify.require(set(names) == {(Path(directory.name) / relative).as_posix() for relative in expected},
                              f"ZIP membership mismatch: {path.name}")
        shared_verify.require(not any(name.endswith(("/en.srt", "/en.vtt")) for name in names),
                              f"English CC unexpectedly included in {path.name}")
    return {
        "file": path.name, "bytes": path.stat().st_size, "sha256": build.file_sha256(path),
        "episode_ids": [episode["id"] for episode in episodes], "episodes": len(episodes), "files": len(expected),
        "video_files": len(episodes) * 2, "audio_files": len(episodes) * 5, "caption_files": len(episodes) * 8,
        "zip_testzip": "passed", "english_cc": False,
        "practice": [{"file": name, "rows": len(episodes), "bytes": (directory / name).stat().st_size,
                      "sha256": build.file_sha256(directory / name)} for name in ("Practice.html", "Practice.pdf")],
    }


def contains_authored_fields(authored, measured) -> bool:
    """Measured records may add timings, but must preserve every authored value."""
    if isinstance(authored, dict):
        return isinstance(measured, dict) and all(
            key in measured and contains_authored_fields(value, measured[key])
            for key, value in authored.items())
    if isinstance(authored, list):
        return isinstance(measured, list) and len(authored) == len(measured) and all(
            contains_authored_fields(a, b) for a, b in zip(authored, measured))
    return type(authored) is type(measured) and authored == measured


def preflight(source: dict, resolved: dict, output: Path) -> tuple[list[dict], dict[str, dict]]:
    """Require current authoring, measured speech and checked media to agree."""
    verify_structure(source)
    verify_structure(resolved)
    shared_verify.require(resolved == audio.read_json(output / "lessons.resolved.json"),
                          "Package resolution differs from the output resolution used for verification")
    episodes = resolved["episodes"]
    for authored, episode in zip(source["episodes"], episodes):
        shared_verify.require(audio.source_matches(authored, episode)
                              and contains_authored_fields(authored, episode),
                              f"{episode['id']}: resolved lesson differs from current authoring, including practice")
    report = verify_output(source, output)
    failures = "; ".join(f"{entry.get('episode', '?')}: {entry.get('error', 'failed')}"
                         for entry in report.get("errors", []))
    shared_verify.require(report.get("passed") is True,
                          "Complete current-source media verification failed: " + (failures or report.get("status", "incomplete")))
    records = {}
    for episode in episodes:
        eid = episode["id"]
        directory = output / eid
        for relative in EPISODE_FILES:
            path = directory / relative
            shared_verify.require(path.is_file() and path.stat().st_size > 0, f"Missing or empty required file: {path}")
        records[eid] = audio.read_json(directory / "checks.json")
    return episodes, records


def load_package_inputs(source_path: Path, resolved_path: Path, output: Path) -> tuple[dict, dict]:
    shared_verify.require(resolved_path.resolve() == (output / "lessons.resolved.json").resolve(),
                          "--resolved must be the output directory's lessons.resolved.json")
    source = audio.load_source(source_path.resolve(), None)
    return source, audio.read_json(resolved_path)


def write_catalog(path: Path, episodes: list[dict], records: dict[str, dict]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(["集數", "季數", "程度", "季名", "標題", "英文標題", "學習目標", "時長", "時長（秒）"])
        for episode in episodes:
            season = episode["season"]
            seconds = float(records[episode["id"]]["duration"])
            minutes, remainder = divmod(round(seconds), 60)
            writer.writerow([episode["number"], season, GRADE_BANDS[season], SEASON_NAMES[season],
                             episode["title_zh_TW"], episode["title_en"], "；".join(episode["objectives_zh_TW"]),
                             f"{minutes}:{remainder:02d}", f"{seconds:.3f}"])


def write_readme(path: Path, episodes: list[dict]) -> None:
    first, last = episodes[0]["number"], episodes[-1]["number"]
    path.write_text(
        f"English Lab · Sunny & Pip｜高中英文第 {first}–{last} 集｜共 {len(episodes)} 集\n\n"
        "完整解壓縮 ZIP、保留資料夾結構，再用瀏覽器開啟 index.html。\n"
        "選擇季數、集數、教學配音與翻譯字幕 CC，再按播放；配音與 CC 可以分別選擇。\n"
        "也可用 VLC 開啟 epXX/final.mp4，切換音訊軌與字幕軌。\n"
        "若瀏覽器限制本機音訊，請改用 VLC。\n\n"
        "英文固定顯示在畫面，沒有英文 CC。配音含英文、繁體中文、簡體中文、日文、韓文五組；\n"
        "四語教學聲軌都使用同一段英文示範。CC 提供繁體中文、簡體中文、日文、韓文。\n"
        "聽讀選句活動可先看到各選項的英文，聽完示範等待六秒後才標示答案與翻譯；\n"
        "這是有提示的聽讀練習，不是獨立閱讀或純聽力評量。一般練習保留五秒回應時間。\n\n"
        "第 1–2 季為高一，第 3–4 季為高二，第 5–6 季為高三。\n"
        "依先備能力調整進度；先聽讀跟說，再完成獨立閱讀理解與段落寫作。\n"
        "六季皆使用新版高中英文畫面，銜接國中基礎至精確表達、批判閱讀、證據整合與學術溝通。\n\n"
        "每集 final.mp4 含五音軌與四 CC；picture.mp4 是無聲畫面。\n"
        "audio/ 提供五語 M4A；captions/ 提供四語 SRT、VTT；checks.json 保存成片檢查紀錄。\n"
        "課程目錄 CSV 使用 UTF-8 BOM，可用試算表開啟。\n"
        "Practice.html / Practice.pdf 每集提供短文、三題理解／應用題與有字數目標的寫作；活動與答案分頁。\n"
        "每集 PDF 含閱讀／理解頁、寫作頁與後置答案頁；全集 217 頁，各季 37 頁。\n"
        "寫作答案只是示例，並非唯一正解；影片中的聽讀選句不代替課後獨立閱讀。\n"
        "目前使用 Microsoft Edge 合成配音試製，尚未套用後台正式聲音，也未在後台發布。\n",
        encoding="utf-8",
    )


def stage_package(resolved: dict, episodes: list[dict], records: dict[str, dict],
                  output: Path, directory: Path) -> None:
    directory.mkdir(parents=True)
    for episode in episodes:
        for relative in EPISODE_FILES:
            source = output / episode["id"] / relative
            target = directory / episode["id"] / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            try:
                os.link(source, target)
            except OSError:
                shutil.copy2(source, target)
    write_player({**resolved, "episodes": episodes}, directory)
    write_readme(directory / "README.txt", episodes)
    write_practice(episodes, directory)
    write_catalog(directory / (CATALOG_NAME if len(episodes) == 72 else "本季課程目錄.csv"), episodes, records)


def package_series(source_path: Path, resolved_path: Path, output: Path, all_zip: bool = True) -> dict:
    source_path, resolved_path, output = source_path.resolve(), resolved_path.resolve(), output.resolve()
    repository = Path(__file__).resolve().parents[3]
    shared_verify.require(output != repository and repository not in output.parents,
                          "Media packages must be outside the public repository")
    source_sha256, resolved_sha256 = build.file_sha256(source_path), build.file_sha256(resolved_path)
    source, resolved = load_package_inputs(source_path, resolved_path, output)
    episodes, records = preflight(source, resolved, output)
    with tempfile.TemporaryDirectory(prefix=".package-senior-high-complete-", dir=output) as temporary:
        staging = Path(temporary)
        packages = []
        for season in range(1, 7):
            selected = [episode for episode in episodes if episode["season"] == season]
            directory = staging / "Seasons" / f"Senior_High_Season_{season:02d}"
            stage_package(resolved, selected, records, output, directory)
            archive = staging / f"Sunny_Pip_Senior_High_Season_{season:02d}.zip"
            packages.append({**create_archive(directory, archive, selected), "season": season})
        if all_zip:
            directory = staging / "Senior_High_All_72_Episodes"
            stage_package(resolved, episodes, records, output, directory)
            packages.append(create_archive(directory, staging / ALL_ARCHIVE_NAME, episodes))
        catalog = staging / CATALOG_NAME
        write_catalog(catalog, episodes, records)
        practice_paths = write_practice(episodes, staging)
        report = {
            "ready": True, "created_at": audio.stamp(), "episode_count": 72, "season_count": 6,
            "source_sha256": source_sha256, "resolved_sha256": resolved_sha256, "renderer_profiles": {
                "all_six_seasons": RENDERER.name},
            "audio_locales": list(build.LOCALES), "cc_locales": list(build.SUBTITLES), "english_cc": False,
            "validation": "Current authoring including practice, measured shared English and response intervals, uniform senior-high renderer, source and artifact hashes, exact CC timing, full-decode receipts, and ZIP CRCs and contents.",
            "packages": packages,
            "practice": [{"file": path.name, "rows": 72, "bytes": path.stat().st_size,
                          "sha256": build.file_sha256(path)} for path in practice_paths],
            "catalog": {"file": CATALOG_NAME, "rows": 72, "encoding": "UTF-8 BOM",
                        "bytes": catalog.stat().st_size, "sha256": build.file_sha256(catalog)},
        }
        shared_verify.require(build.file_sha256(source_path) == source_sha256
                              and build.file_sha256(resolved_path) == resolved_sha256,
                              "Authoring or measured lessons changed while packaging; rebuild from the current source")
        # No archive is published until every archive has passed its CRC/content checks.
        for package in packages:
            (staging / package["file"]).replace(output / package["file"])
        catalog.replace(output / CATALOG_NAME)
        for path in practice_paths:
            path.replace(output / path.name)
        audio.atomic_json(output / "package-checks.json", report)
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True, help="Current complete authoring lessons.json")
    parser.add_argument("--resolved", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--seasons-only", action="store_true", help="Skip the combined 72-episode archive")
    parser.add_argument("--check-only", action="store_true")
    args = parser.parse_args()
    try:
        if args.check_only:
            source, resolved = load_package_inputs(args.source, args.resolved, args.output.resolve())
            episodes, _ = preflight(source, resolved, args.output.resolve())
            print(f"VERIFIED {len(episodes)} senior-high episodes; no files changed")
        else:
            report = package_series(args.source, args.resolved, args.output, not args.seasons_only)
            for package in report["packages"]:
                print(f"READY {package['file']}: {package['episodes']} episodes, {package['bytes']} bytes")
            print(f"READY {CATALOG_NAME}; package-checks.json")
    except (audio.PipelineError, shared_verify.VerificationError, OSError, ValueError, KeyError, zipfile.BadZipFile) as error:
        parser.exit(1, f"Packaging failed: {error}\n")


if __name__ == "__main__":
    main()
