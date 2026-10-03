"""Stage the dots authors' final text and manual-recording packages; never make media.

The existing youtube-video helper supplies checks, reading text, shots and draft
metadata. All chapter times are estimates until an actual edit is reviewed.
"""
from __future__ import annotations

import argparse
import contextlib
import importlib.util
import io
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

from files import copy_text_lf, digest, dumps, scoped, tree_files, write_text_lf

ROOT = Path(__file__).resolve().parents[2]
KIT_PATH = Path(".agents/skills/youtube-video/scripts/video_kit.py")
TEXT_SUFFIXES = {".md", ".txt", ".csv", ".json", ".ics", ".py"}


def load_helper(repo: Path):
    path = scoped(repo / KIT_PATH, repo, repo / ".agents/skills/youtube-video")
    spec = importlib.util.spec_from_file_location("dots_existing_video_kit", path)
    if spec is None or spec.loader is None:
        raise ValueError("The existing youtube-video helper is unavailable")
    helper = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = helper
    spec.loader.exec_module(helper)
    return helper


def normalized_script(source: str) -> str:
    """The existing helper parses YAML as strings, so null must become empty."""
    front = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n", source, flags=re.DOTALL)
    if not front:
        raise ValueError("A recording script requires video_kit frontmatter")
    value = re.sub(r"^recorded_on:\s*(?:null|~|None)\s*$", "recorded_on:", front.group(1), flags=re.MULTILINE | re.IGNORECASE)
    return "---\n" + value + "\n---\n" + source[front.end():]


def helper_command(helper, command: str, script: Path, *, out: Path | None = None, cpm: int = 250) -> subprocess.CompletedProcess:
    # Invoke the existing CLI's argument parser and command handlers in-process.
    # These four commands are local text operations; no new production engine.
    arguments = [command, str(script), "--cpm", str(cpm)]
    if out is not None:
        arguments.extend(["--out", str(out)])
    stdout, stderr = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
        code = helper.main(arguments)
    return subprocess.CompletedProcess(arguments, code, stdout.getvalue(), stderr.getvalue())


def brief(number: int, title: str, outcome: str, estimated: float, cpm: int, capture_list: str) -> str:
    slug = f"dots-lesson-{number:02}"
    planned = f"https://mokaair.com/zh-TW/life/{slug}"
    download = f"https://mokaair.com/dots-course/downloads/lesson-{number:02}.zip" if number >= 11 else None
    return "\n".join([
        f"# 第 {number:02} 課製作 brief：{title}", "",
        "狀態：文字製作包已備妥；真實畫面、旁白音訊、剪輯成片與公開核對均待完成。", "",
        f"觀眾學習成果：{outcome}", "",
        "格式：逐步畫面示範，以真實 dots 介面截圖按操作順序串接；保留 Mokaair 品牌，使用台灣口音繁中旁白。",
        "長度：目標整片 8–15 分鐘；旁白正文與示範正文至少 480 秒，片頭片尾不能補足正文。",
        f"口播估計：{estimated:.1f} 秒（每分鐘 {cpm} 單位）；此值是排稿估計，尚未測量音訊或成片。", "",
        "| 製作項目 | 當前狀態 |", "| --- | --- |",
        "| 逐課真實 dots 操作與結果 | 待驗收收據綁定 |",
        "| 真實截圖與遮罩 | 待擷取／逐張覆核 |",
        "| 台灣口音音訊 | 待合成或錄製與聆聽 |",
        "| 成片、字幕與實際章節 | 待剪輯及對時 |",
        "| 縮圖、上傳與公開 | 待完成；尚未上傳／公開 |", "",
        ("畫面製作：依 shots.csv 的步驟取真實畫面，加入可讀的游標指引、必要重點放大與文字疊字。"
         "操作結果必須實際開啟；原創教學圖不能替代產品介面或實測結果。"),
        f"製作交接：[全套交接紀錄](../../dots-series/{Path(capture_list).name})；本課擷取順序與逐段指示在 [shots.csv](shots.csv)。", "",
        f"文章預定網址（尚未公開）：{planned}",
        *([f"素材預定網址（尚未公開）：{download}"] if download else []),
        "總目錄預定網址（尚未公開）：https://mokaair.com/zh-TW/life/dots-guide", "",
        ("錄音前重查官方來源與帳號條件；錄製日期留白，完成錄製後才填實際日期。"
         "所有原始截圖、影音檔與私有驗收收據保存在 repo 外。"),
        "upload-draft.md 和 shots.csv 的時間僅為估計；不得用來宣稱成片章節或字幕同步已驗收。",
        "完成真實影音覆核後才產出繁中 SRT、實際章節與最終上架包。YouTube 上傳及按下發布由站主在 Studio 完成。", "",
        "## 接續既有畫面產線", "",
        ("現有入口為 tools/video/render/plan.mjs、tools/video/render/cli.mjs；素材與場景使用 tools/video/core/schema.mjs 的既有格式。"
         "逐步游標、框選、點擊波紋與放大由 tools/video/screencast/scene.mjs 提供，不新增影片引擎。"), "",
        ("screencast 場景的 data.steps 使用 goto、wait、click、fill、capture、mask；capture 可帶 focus 與 zoom（1–2.5）。"
        "每個 capture 對應一個狀態，台詞 reveal 合計為截圖張數減一，第一句不 reveal。"
         "範例格式在 tools/video/screencast/fixtures/tutorial/video.json。"), "",
        ("擷取產物位於 repo 外 <workdir>/<slug>/screencast/<key>/manifest.json，含 viewport、scale、captured_at；"
         "每張 capture 含 file、sha256、target（x/y/w/h）、press、zoom、masks。"
         "renderer 依這些真實擷取資料繪製游標與重點效果。登入頁由站主使用既有登入 profile，需逐張遮罩並覆核。"), "",
        ("單張 screenshot 場景使用 data.image（已遮罩、位於 apps/web/public/ 或 docs/videos/ 的 PNG/JPEG/WebP）、"
        "data.highlight（x/y/w/h 百分比）及 caption；這個模板提供框選。"
         "桌面 App 原始錄影與截圖維持在 repo 外，人工剪輯完成後可依既有 import 流程交入 final.mp4 與 meta.json。"), "",
        ("目前阻擋：02、03 尚待真實試拍及畫面／旁白節奏核對；未建立本課 video.json 與對應 capture manifests，"
         "未有音訊／成片。先完成兩課樣本驗收，再製作其餘成片；作者稿通過不能代替試拍。"), "",
        "完成真實操作、來源覆核並把稿件映射為既有 video.json 後，先執行本機檢查與配額預估：", "",
        "```powershell", f"node tools/video/cli.mjs lint --slug {slug}",
        "$dotsVideoWorkdir = Join-Path ([Environment]::GetFolderPath('UserProfile')) 'mokaair-work/dots-videos'",
        f"node tools/video/cli.mjs tts --slug {slug} --workdir $dotsVideoWorkdir --dry-run", "```", "",
        ("音訊與 capture manifests 依既有關卡就緒後，才接續既有 render、assemble、captions、qa、package。"
         "此製作包尚未執行這些媒體階段；不送出付費請求或自行使用登入 profile。"), "",
    ])


def authoring_kit(workspace: Path, *, repo: Path = ROOT, install: bool = False,
                  cpm: int = 250, capture_list: str = "docs/dots-series/HANDOVER.md") -> dict:
    workspace, repo = workspace.resolve(), repo.resolve()
    if workspace.is_relative_to(repo) or cpm < 150 or cpm > 350:
        raise ValueError("Use an external authoring workspace and a realistic 150–350 CPM estimate")
    helper = load_helper(repo)
    catalogue_path = scoped(repo / "apps/api/app/guides/series_data/dots.json", repo, repo / "apps/api/app/guides/series_data")
    catalogue = json.loads(catalogue_path.read_text(encoding="utf-8"))
    entries = {entry["number"]: entry for entry in catalogue["entries"]}
    if sorted(entries) != list(range(1, 17)):
        raise ValueError("A complete sixteen-lesson catalogue is required")
    sources = [workspace / "lessons" / f"{number:02}.md" for number in range(17)]
    sources.extend(workspace / "videos" / f"{number:02}.md" for number in range(1, 17))
    exercise_sources = []
    for number in range(11, 17):
        paths = tree_files(workspace / "examples" / str(number), workspace)
        if len(paths) < 2:
            raise ValueError(f"Application {number} is missing its authored initial/changed inputs")
        exercise_sources.extend(paths)
    sources.extend(exercise_sources)
    for source in sources:
        scoped(source, workspace, workspace / source.relative_to(workspace).parts[0])
        if source.suffix not in TEXT_SUFFIXES or not source.is_file():
            raise ValueError(f"Missing or non-text authoring source: {source}")
    target = scoped(workspace / "build-authoring", workspace, workspace / "build-authoring")
    staged = scoped(target / "docs", workspace, target)
    handoff_paths = {source: scoped(staged / "dots-series" / source.relative_to(workspace), workspace, target)
                     for source in [*sources[:17], *exercise_sources]}
    filenames = ("script.md", "script-check.txt", "teleprompter.txt", "shots.csv", "upload-draft.md", "brief.md")
    recording_paths = {number: {filename: scoped(staged / "videos" / f"dots-lesson-{number:02}" / filename, workspace, target)
                                for filename in filenames} for number in range(1, 17)}
    manifest_path = scoped(staged / "dots-series/production-manifest.json", workspace, target)
    staged_files = [*handoff_paths.values(), *[path for paths in recording_paths.values() for path in paths.values()]]
    install_paths = {path: scoped(repo / path.relative_to(target), repo, repo / "docs")
                     for path in [*staged_files, manifest_path]} if install else {}
    # The helper's metadata command reads these optional content packs. Validate
    # them before invoking it, too; an existing linked pack cannot read outside.
    for number in range(1, 17):
        scoped(repo / "apps/api/app/guides/content" / f"dots-lesson-{number:02}.json", repo, repo / "apps/api/app/guides/content")
    for source in sources:
        if not source.read_text(encoding="utf-8-sig").strip():
            raise ValueError(f"Missing or non-text authoring source: {source}")
    records, errors = [], []
    for source, destination in handoff_paths.items():
        destination.parent.mkdir(parents=True, exist_ok=True)
        copy_text_lf(source, destination)
    for number in range(1, 17):
        original = workspace / "videos" / f"{number:02}.md"
        paths = recording_paths[number]
        directory = paths["script.md"].parent
        directory.mkdir(parents=True, exist_ok=True)
        script = paths["script.md"]
        write_text_lf(script, normalized_script(original.read_text(encoding="utf-8")))
        parsed = helper.parse(script)
        if parsed.meta.get("article") != f"dots-lesson-{number:02}" or not parsed.meta.get("title"):
            raise ValueError(f"Lesson {number:02}: recording script must bind the correct article and title")
        estimated = sum(helper.seconds(line, cpm) for chapter in parsed.chapters for line in chapter.narration())
        check = helper_command(helper, "check", script, cpm=cpm)
        write_text_lf(paths["script-check.txt"], check.stdout + check.stderr)
        if check.returncode:
            errors.append(f"Lesson {number:02}: video_kit check failed; inspect staged script-check.txt")
        for command, filename in (("teleprompter", "teleprompter.txt"), ("shots", "shots.csv"), ("metadata", "upload-draft.md")):
            result = helper_command(helper, command, script, out=paths[filename], cpm=cpm)
            if result.returncode:
                errors.append(f"Lesson {number:02}: video_kit {command} failed: {result.stderr.strip()}")
            elif paths[filename].is_file():
                # The existing helper writes with the platform default newline.
                # Normalize its output before hashing or installing the package.
                copy_text_lf(paths[filename], paths[filename])
        upload = paths["upload-draft.md"]
        if upload.is_file():
            text = upload.read_text(encoding="utf-8").replace("完整文字版與整理表格", "文字版預定網址（尚未公開）")
            text = text.replace("#hashtag1 #hashtag2", "#OpenAI #dots #Mokaair")
            write_text_lf(upload, "> **製作草稿，尚未錄製／上傳／公開。所有時間均為口播估計，不能作為實際章節。**\n\n" + text)
        write_text_lf(paths["brief.md"], brief(number, parsed.meta["title"], entries[number]["outcome"], estimated, cpm, capture_list))
        records.append({"number": number, "slug": f"dots-lesson-{number:02}", "title": parsed.meta["title"],
                        "state": "authored-capture-audio-video-pending", "article_url": f"https://mokaair.com/zh-TW/life/dots-lesson-{number:02}",
                        "link_state": "planned-not-published", "download_url": f"https://mokaair.com/dots-course/downloads/lesson-{number:02}.zip" if number >= 11 else None,
                        "source_article_sha256": digest(workspace / "lessons" / f"{number:02}.md"),
                        "article_output_sha256": digest(handoff_paths[workspace / "lessons" / f"{number:02}.md"]),
                        "source_script_sha256": digest(original), "normalized_script_sha256": digest(script),
                        "estimated_narration_seconds": round(estimated, 2), "estimated_cpm": cpm,
                        "target_final_seconds": [480, 900], "minimum_body_seconds": 480,
                        "measured_body_seconds": None, "measured_final_seconds": None, "video_url": None,
                        "script_check_exit_code": check.returncode})
    if errors:
        raise ValueError("; ".join(errors))
    files = [{"path": path.relative_to(target).as_posix(), "sha256": digest(path)} for path in sorted(staged_files)]
    manifest = {"version": 1, "state": "authored-production-packages", "published": False, "media_generated": False,
                "installed": install, "helper_sha256": digest(repo / KIT_PATH),
                "catalogue_sha256": digest(repo / "apps/api/app/guides/series_data/dots.json"),
                "sources": [{"path": path.relative_to(workspace).as_posix(), "sha256": digest(path),
                             **({"output_path": handoff_paths[path].relative_to(target).as_posix(),
                                 "output_sha256": digest(handoff_paths[path])} if path in handoff_paths else {})}
                            for path in sorted(sources)],
                "entries": records, "files": files}
    write_text_lf(manifest_path, dumps(manifest))
    if install:
        for original, destination in install_paths.items():
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(original, destination)
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", required=True, type=Path)
    parser.add_argument("--repo", type=Path, default=ROOT)
    parser.add_argument("--install", action="store_true", help="Install only text authoring and recording packages into docs")
    parser.add_argument("--cpm", type=int, default=250)
    parser.add_argument("--capture-list", default="docs/dots-series/HANDOVER.md")
    args = parser.parse_args()
    try:
        result = authoring_kit(args.workspace, repo=args.repo, install=args.install, cpm=args.cpm, capture_list=args.capture_list)
        print(dumps({"state": result["state"], "published": False, "media_generated": False, "installed": args.install,
                     "lessons": len(result["entries"]), "output": str(args.workspace / "build-authoring/docs")}), end="")
        return 0
    except (ValueError, OSError, subprocess.SubprocessError) as error:
        print(dumps({"state": "blocked", "published": False, "error": str(error)}), end="")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
