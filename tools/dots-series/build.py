"""Compile the dots course into reviewable ArticlePacks; never import or publish.

Default output is <external-workspace>/build. --install explicitly copies validated
draft files to the checkout. Publication readiness is a separate, fail-closed audit.
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

from authoring import read_lesson
from files import copy_text_lf, digest, dumps, scoped, tree_files, write_text_lf

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "apps/api"))

from app.guides.content_pack import ArticlePack
from app.guides.pack_ingest import check_svg, lint_document
from app.guides.series import Catalogue


class MissingAsset(ValueError):
    pass


def validate_svg(source: Path) -> None:
    failures = [problem for problem in check_svg(source.read_text(encoding="utf-8"), body=True)
                if problem.level == "error"]
    if failures:
        raise ValueError(f"{source.name}: " + "; ".join(str(problem) for problem in failures))


def find_asset(src: str, workspace: Path, repo: Path) -> Path:
    if not src.startswith(("/guides/dots-", "/dots-course/")) or "\\" in src:
        raise ValueError(f"Unexpected dots asset path: {src}")
    for base, root in [(workspace / "assets", workspace), (repo / "apps/web/public", repo)]:
        path = scoped(base / src.lstrip("/"), root, base)
        if path.is_file():
            return path
    raise MissingAsset(f"Missing public asset: {src}")


def hero(slug: str, title: str, workspace: Path, repo: Path) -> dict:
    from PIL import Image

    for suffix in ("png", "jpg", "webp"):
        src = f"/guides/{slug}/hero.{suffix}"
        try:
            source = find_asset(src, workspace, repo)
        except MissingAsset:
            continue
        with Image.open(source) as image:
            image.verify()
        with Image.open(source) as image:
            width, height = image.size
        return {"src": src, "alt": title + "：Mokaair 原創課程封面", "width": width, "height": height,
                "credit": {"author": "Mokaair", "license": "© Mokaair"}}
    raise ValueError(f"Missing authored raster hero for {slug}")


def hub_document(catalogue: dict, lessons: dict) -> dict:
    blocks = [
        {"type": "paragraph", "text": "這套 OpenAI dots 教學從建立第一個 dot、第一次交辦開始，逐步介紹記憶、工具、電腦、委派工作、排程與控制，再完成旅遊、辦公、報表、學習、內容和專案六個應用。請依序完成前三課，再依需要選擇後面的練習。"},
        {"type": "summary", "items": ["完整課程共十六課：十課基礎與控制，六課實際應用。", "先依序完成第01–03課，再選擇需要的工具、排程和應用練習。"]},
        {"type": "callout", "tone": "info", "title": "使用條件與示範範圍", "text": "可用資格、聯絡管道、應用程式與介面會隨帳號、裝置和版本不同。先核對官方文件與自己的畫面；教學素材使用專用示範資料，不能替代你的帳號授權。每課操作結果與影片狀態以該課實際驗收紀錄為準。"},
        {"type": "heading", "level": 2, "text": "第 01–10 課：建立、交辦與控制"},
        {"type": "table", "header": ["學習階段", "課次", "完成成果"], "rows": [
            ["第一次使用", "01–03", "確認條件、建立 dot、完成第一份任務"],
            ["持續協作", "04–07", "更新背景、串接工具、選擇電腦與追蹤委派成果"],
            ["排程與控制", "08–10", "設定排程與通知，核對聯絡管道和停止效果"],
            ["實際應用", "11–16", "完成六個案例並接續更新資料"],
        ]},
    ]
    for entry in catalogue["entries"]:
        if entry["number"] == 11:
            blocks.append({"type": "heading", "level": 2, "text": "第 11–16 課：六個實際應用"})
        blocks.append({"type": "rich_paragraph", "inlines": [
            {"type": "article", "kind": "life", "slug": entry["slug"], "text": f'{entry["number"]:02}｜{lessons[entry["slug"]]["title"]}'},
            {"type": "text", "text": "。" + entry["outcome"]},
        ]})
    blocks.extend([
        {"type": "heading", "level": 2, "text": "如何練習與檢查完成"},
        {"type": "list", "ordered": True, "items": [
            "先讀先修條件並準備課程指定的示範資料。", "依照操作步驟與可複製提示詞完成任務，開啟成果檢查。",
            "六個應用都要再提供一次改變的資料，檢查更新結果。", "使用完成清單核對成果、來源與停止效果，再進入下一課。",
        ]},
    ])
    sources = {}
    for document in lessons.values():
        for source in document["sources"]:
            prior = sources.get(source["url"])
            if prior is None or prior["checked_on"] < source["checked_on"]:
                sources[source["url"]] = source
    return {"title": "OpenAI dots 完整教學：從入門到六個實際應用", "description": blocks[0]["text"], "blocks": blocks, "sources": list(sources.values())}


def compile_course(workspace: Path, repo: Path = ROOT, *, selected: list[int] | None = None) -> tuple[dict[str, dict], dict[str, Path], list[dict]]:
    workspace, repo = workspace.resolve(), repo.resolve()
    if workspace.is_relative_to(repo):
        raise ValueError("Authoring workspace and media originals must live outside the repository")
    catalogue_path = scoped(repo / "apps/api/app/guides/series_data/dots.json", repo, repo / "apps/api/app/guides/series_data")
    catalogue = Catalogue.model_validate_json(catalogue_path.read_text(encoding="utf-8")).model_dump(mode="json")
    if catalogue["locale"] != "zh-TW" or len(catalogue["entries"]) != 16:
        raise ValueError("The dots course must contain exactly sixteen zh-TW lessons")
    if selected is not None and (not selected or len(set(selected)) != len(selected) or any(number not in range(1, 17) for number in selected)):
        raise ValueError("Selected pilot lessons must be a nonempty unique subset of 01–16")
    selected_entries = [entry for entry in catalogue["entries"] if selected is None or entry["number"] in selected]
    for name in ("lessons", "assets"):
        scoped(workspace / name, workspace, workspace / name)
    for entry in selected_entries:
        scoped(workspace / "lessons" / f'{entry["number"]:02}.md', workspace, workspace / "lessons")
    hub_path = scoped(workspace / "lessons/00.md", workspace, workspace / "lessons")
    assets_path = scoped(workspace / "assets.json", workspace, workspace)
    lessons = {entry["slug"]: read_lesson(workspace / "lessons" / f'{entry["number"]:02}.md') for entry in selected_entries}
    if selected is None:
        hub = read_lesson(hub_path) if hub_path.exists() else hub_document(catalogue, lessons)
        documents = {**lessons, catalogue["hub"]: hub}
    else:
        documents = lessons
    known_slugs = {catalogue["hub"], *[entry["slug"] for entry in catalogue["entries"]]}
    assets_meta = json.loads(assets_path.read_text(encoding="utf-8")) if assets_path.exists() else {}
    packs, assets, warnings = {}, {}, []
    entries = {entry["slug"]: entry for entry in catalogue["entries"]}
    for slug, source_doc in documents.items():
        doc = dict(source_doc)
        doc["blocks"] = list(source_doc["blocks"])
        doc["hero"] = hero(slug, doc["title"], workspace, repo)
        figures = assets_meta.get(slug, [])
        # The full-width series directory has no article reading rail. Its hero
        # already provides the visual; explicit authored figures remain honored.
        if not figures and slug != catalogue["hub"]:
            diagram_src = f"/guides/{slug}/diagram-1.svg"
            try:
                diagram_path = find_asset(diagram_src, workspace, repo)
            except MissingAsset:
                diagram_path = None
            if diagram_path:
                from xml.etree import ElementTree

                validate_svg(diagram_path)
                svg = ElementTree.parse(diagram_path).getroot()
                description = " ".join(node.text or "" for node in svg.iter() if node.tag.split("}")[-1] == "desc").strip()
                figures = [{"src": diagram_src, "alt": doc["title"] + "：原創教學流程圖", "width": int(svg.get("width", "1600")),
                            "height": int(svg.get("height", "900")), "caption": "Mokaair 原創教學流程圖", "description": description,
                            "credit": {"author": "Mokaair", "license": "© Mokaair"}}]
        for metadata in figures:
            image = {**metadata, "type": "image"}
            if not image["src"].startswith(f"/guides/{slug}/"):
                raise ValueError(f"{slug}: figure must live under its own asset directory")
            doc["blocks"].insert(1, image)
        if slug in entries:
            if not any(block["type"] == "code" for block in doc["blocks"]):
                raise ValueError(f"{slug}: missing authored, copyable prompt")
            doc["blocks"].append({"type": "rich_paragraph", "inlines": [{"type": "article", "text": "回 dots 教學總目錄", "kind": "life", "slug": catalogue["hub"]}]})
            if entries[slug]["number"] >= 11:
                src = f'/dots-course/downloads/lesson-{entries[slug]["number"]:02}.zip'
                assets[src] = find_asset(src, workspace, repo)
                doc["blocks"].append({"type": "rich_paragraph", "inlines": [{"type": "link", "text": f'下載第 {entries[slug]["number"]:02} 課練習素材（合成資料）', "url": "https://mokaair.com" + src}]})
        elif not any(block["type"] == "rich_paragraph" and any(inline["type"] == "article" for inline in block["inlines"]) for block in doc["blocks"]):
            first = catalogue["entries"][0]
            doc["blocks"].append({"type": "rich_paragraph", "inlines": [{"type": "article", "kind": "life", "slug": first["slug"], "text": first["title"]}]})
        pack = ArticlePack.model_validate({"slug": slug, "kind": "life", "topics": ["ai", "tutorial", "ai-chat"], "featured": False,
                                          "display_order": 600 + entries[slug]["number"] if slug in entries else 599,
                                          "related": entries[slug]["related"] if slug in entries else [], "locales": {"zh-TW": doc}})
        problems = lint_document(pack.locales["zh-TW"], pack.kind, topics=pack.topics)
        failures = [problem for problem in problems if problem.level == "error"]
        if failures:
            raise ValueError(f"{slug}: " + "; ".join(str(problem) for problem in failures))
        warnings.extend({"slug": slug, "code": problem.code, "message": problem.message} for problem in problems if problem.level == "warning")
        for image in [doc["hero"], *[block for block in doc["blocks"] if block["type"] == "image"]]:
            source = find_asset(image["src"], workspace, repo)
            if source.suffix.lower() == ".svg":
                validate_svg(source)
            assets[image["src"]] = source
        for block in doc["blocks"]:
            for inline in block.get("inlines", []):
                if inline["type"] == "article" and inline["slug"] not in known_slugs:
                    reference_path = scoped(repo / "apps/api/app/guides/content" / (inline["slug"] + ".json"), repo, repo / "apps/api/app/guides/content")
                    if not reference_path.is_file():
                        raise ValueError(f"{slug}: unknown course article reference {inline['slug']}")
                if inline["type"] == "link":
                    from urllib.parse import urlsplit

                    url = urlsplit(inline["url"])
                    if url.netloc == "mokaair.com" and url.path.startswith("/dots-course/"):
                        assets[url.path] = find_asset(url.path, workspace, repo)
        packs[slug] = pack.model_dump(mode="json", exclude_none=True)
    return packs, assets, warnings


def build(workspace: Path, repo: Path = ROOT, *, install: bool = False, selected: list[int] | None = None) -> dict:
    workspace, repo = workspace.resolve(), repo.resolve()
    target = scoped(workspace / ("build" if selected is None else "build-pilot"), workspace,
                    workspace / ("build" if selected is None else "build-pilot"))
    input_paths = [path for directory in ("lessons", "videos", "examples") for path in tree_files(workspace / directory, workspace)]
    assets_path = scoped(workspace / "assets.json", workspace, workspace)
    if assets_path.is_file():
        input_paths.append(assets_path)
    if install:
        scoped(repo / "apps/api/app/guides/content", repo, repo / "apps/api/app/guides/content")
        scoped(repo / "apps/web/public", repo, repo / "apps/web/public")
    packs, assets, warnings = compile_course(workspace, repo, selected=selected)
    content_paths = {slug: scoped(target / "content" / f"{slug}.json", workspace, target) for slug in packs}
    asset_paths = {src: scoped(target / "web-public" / src.lstrip("/"), workspace, target) for src in assets}
    manifest_path = scoped(target / "build-manifest.json", workspace, target)
    install_content = {slug: scoped(repo / "apps/api/app/guides/content" / f"{slug}.json", repo, repo / "apps/api/app/guides/content")
                       for slug in packs} if install else {}
    install_assets = {src: scoped(repo / "apps/web/public" / src.lstrip("/"), repo, repo / "apps/web/public")
                      for src in assets} if install else {}
    # Source hashes are also read before any output mutation. Escaping inputs or
    # destinations cannot leave a partial ZIP/build/install behind.
    inputs = [{"path": path.relative_to(workspace).as_posix(), "sha256": digest(path)} for path in sorted(input_paths)]
    source_assets = [{"base": "workspace" if original.is_relative_to(workspace) else "repo",
                      "path": original.relative_to(workspace if original.is_relative_to(workspace) else repo).as_posix(),
                      "sha256": digest(original)} for original in sorted(set(assets.values()))]
    for slug, pack in packs.items():
        destination = content_paths[slug]
        destination.parent.mkdir(parents=True, exist_ok=True)
        write_text_lf(destination, dumps(pack))
    for src, original in assets.items():
        destination = asset_paths[src]
        destination.parent.mkdir(parents=True, exist_ok=True)
        if original.suffix == ".svg":
            copy_text_lf(original, destination)
        else:
            shutil.copyfile(original, destination)
    files = [*content_paths.values(), *asset_paths.values()]
    manifest = {"version": 1, "state": "draft", "published": False, "articles": list(packs), "warnings": warnings,
                "catalogue_sha256": digest(repo / "apps/api/app/guides/series_data/dots.json"),
                "inputs": inputs, "source_assets": source_assets,
                "files": [{"path": path.relative_to(target).as_posix(), "sha256": digest(path)} for path in sorted(files)]}
    write_text_lf(manifest_path, dumps(manifest))
    if install:
        for slug in packs:
            destination = install_content[slug]
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(content_paths[slug], destination)
        for src in assets:
            destination = install_assets[src]
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(asset_paths[src], destination)
    return {"state": "draft", "published": False, "installed": install, "articles": len(packs), "output": str(target), "warnings": warnings}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", required=True, type=Path)
    parser.add_argument("--repo", type=Path, default=ROOT)
    parser.add_argument("--install", action="store_true", help="Copy validated draft packs and public assets to this checkout; no database writes")
    parser.add_argument("--selected", help="Comma-separated pilot lesson numbers, for example 02,03; cannot satisfy the full release gate")
    args = parser.parse_args()
    try:
        selected = [int(number) for number in args.selected.split(",")] if args.selected is not None else None
        print(dumps(build(args.workspace, args.repo, install=args.install, selected=selected)), end="")
        return 0
    except (ValueError, OSError) as error:
        print(dumps({"state": "blocked", "published": False, "error": str(error)}), end="", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
