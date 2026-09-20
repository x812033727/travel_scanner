"""Compile explicitly authored Markdown into existing content packs, never publish.

uv run --with mistune==3.1.3 --with opencc-python-reimplemented==0.1.7 python tools/codex-learning/build-depth.py
The legacy JSON remains a fallback until all translations of a lesson are authored.
"""
import argparse
import json
import re
import subprocess
from hashlib import sha256
from pathlib import Path

import mistune
from opencc import OpenCC

ROOT = Path(__file__).resolve().parents[2]
AUTHORS = ROOT / "docs/codex-learning/deep"
CATALOG = ROOT / "apps/web/lib/codex-learning/catalog.json"
PACKS = ROOT / "apps/api/app/guides/content"
SCREENSHOT_ALT = {
    "zh-TW": "待辦練習網站：Build 已完成，Read the AGENTS.md rules 尚未完成，共兩項任務。",
    "zh-CN": "待办练习网站：Build 已完成，Read the AGENTS.md rules 尚未完成，共两项任务。",
    "en": "Practice task website: Build is complete and Read the AGENTS.md rules is pending, with two tasks in total.",
    "ja": "練習用タスクサイト。Build は完了、Read the AGENTS.md rules は未完了で、合計2件。",
    "ko": "실습 할 일 사이트. Build는 완료, Read the AGENTS.md rules는 미완료이며 총 두 항목입니다.",
}
REFERENCE_ALT = {
    6: {
        "zh-TW": "修改後的練習網站：標題為 Small steps, clear progress.，Add task 按鈕有橘色鍵盤焦點框。",
        "zh-CN": "修改后的练习网站：标题为 Small steps, clear progress.，Add task 按钮有橙色键盘焦点框。",
        "en": "Edited practice website with the heading Small steps, clear progress. and an orange keyboard focus outline around Add task.",
        "ja": "変更後の練習サイト。見出しは Small steps, clear progress.、Add task ボタンに橙色のキーボードフォーカス枠。",
        "ko": "수정한 실습 사이트. 제목은 Small steps, clear progress.이며 Add task 버튼에 주황색 키보드 포커스 테두리가 있습니다.",
    },
    7: {
        "zh-TW": "提示詞練習成果：輸入框提示為 Plan one small step；Save task 按鈕有橘色焦點框。",
        "zh-CN": "提示词练习成果：输入框提示为 Plan one small step；Save task 按钮有橙色焦点框。",
        "en": "Prompt exercise result: the input hint reads Plan one small step. The Save task button has an orange focus outline.",
        "ja": "依頼文の練習結果。入力欄のヒントは Plan one small step。Save task ボタンに橙色のフォーカス枠が表示されています。",
        "ko": "프롬프트 실습 결과. 입력 힌트는 Plan one small step입니다. Save task 버튼에 주황색 포커스 테두리가 있습니다.",
    },
}
SCREENSHOT_CAPTIONS = {
    "zh-TW": "完整參考版的實際瀏覽器畫面，供修改前比對。Windows / Edge 153.0.4234.32，2026-09-14；使用虛構資料。390px 為響應式視窗，非實體手機。這不是 Codex 桌面介面截圖。",
    "zh-CN": "完整参考版的实际浏览器画面，供修改前比对。Windows / Edge 153.0.4234.32，2026-09-14；使用虚构数据。390px 为响应式窗口，非实体手机。这不是 Codex 桌面界面截图。",
    "en": "Actual browser view of the complete reference version, before lesson edits. Windows / Edge 153.0.4234.32, 2026-09-14; fictional data. 390px is a responsive viewport, not a physical phone. This is not the Codex desktop interface.",
    "ja": "変更前の完成参考版を実際のブラウザで撮影。Windows / Edge 153.0.4234.32、2026-09-14。架空データを使用。390px はレスポンシブ表示で実物のスマートフォンではありません。Codex デスクトップ UI の画像ではありません。",
    "ko": "수정 전 완성 참고 버전의 실제 브라우저 화면. Windows / Edge 153.0.4234.32, 2026-09-14, 가상 데이터. 390px은 반응형 화면이며 실제 휴대전화가 아닙니다. Codex 데스크톱 UI 화면도 아닙니다.",
}
REFERENCE_CAPTIONS = {
    "zh-TW": "本篇指定修改的參考成果，使用原始練習檔套用指定變更後，在 Windows / Edge 153.0.4234.32 於 2026-09-14 實際截圖。橘框是鍵盤焦點；資料皆為虛構。這是寬 {width}px 的響應式視窗，非實體手機，也不是 Codex 介面或模型執行紀錄。",
    "zh-CN": "本篇指定修改的参考成果，使用原始练习文件应用指定更改后，在 Windows / Edge 153.0.4234.32 于 2026-09-14 实际截图。橙框是键盘焦点；数据均为虚构。这是宽 {width}px 的响应式窗口，非实体手机，也不是 Codex 界面或模型执行记录。",
    "en": "Reference edits applied to the practice files; actual Windows / Edge 153.0.4234.32 screenshot, 2026-09-14. Orange outline: keyboard focus. Fictional data in a {width}px responsive viewport, not a physical phone. Not Codex UI or proof of model execution.",
    "ja": "元の教材に本記事の指定変更を適用した参考成果。Windows / Edge 153.0.4234.32、2026-09-14 の実画像です。橙枠はキーボードフォーカスでデータは架空です。幅 {width}px のレスポンシブ表示で、実物のスマートフォン、Codex UI、モデル実行記録ではありません。",
    "ko": "원본 실습 파일에 이 강의의 지정 변경을 적용한 참고 결과. Windows / Edge 153.0.4234.32에서 2026-09-14에 촬영했습니다. 주황 테두리는 키보드 포커스이며 데이터는 가상입니다. 너비 {width}px의 반응형 뷰포트로 실제 휴대전화, Codex UI 또는 모델 실행 기록이 아닙니다.",
}
FEATURE_CAPTIONS = {
    "zh-TW": "本篇參考修正的實際成果：Completed 保留兩筆不同識別碼的 Read，計數仍為 1 active / 3 total。Windows / Edge 153.0.4234.32，2026-09-14；虛構資料，窄版為響應式視窗，非實體手機。這是練習網站，不是 Codex 介面或模型執行證據。",
    "zh-CN": "本篇参考修正的实际成果：Completed 保留两笔不同识别码的 Read，计数仍为 1 active / 3 total。Windows / Edge 153.0.4234.32，2026-09-14；虚构数据，窄版为响应式窗口，非实体手机。这是练习网站，不是 Codex 界面或模型执行证据。",
    "en": "Actual reference repair: Completed retains two Read tasks with distinct IDs; the count remains 1 active / 3 total. Windows / Edge 153.0.4234.32, 2026-09-14; fictional data, responsive viewport rather than a physical phone. This is the practice website, not Codex UI or evidence of model execution.",
    "ja": "参考修正の実画面です。Completed に異なる ID の Read が2件残り、全体は 1 active / 3 total です。Windows / Edge 153.0.4234.32、2026-09-14。架空データで、狭い表示は実機電話ではありません。教材サイトであり Codex UI やモデル実行の証拠ではありません。",
    "ko": "참고 수정의 실제 화면입니다. Completed에 서로 다른 ID의 Read 두 개가 남고 전체는 1 active / 3 total입니다. Windows / Edge 153.0.4234.32, 2026-09-14. 가상 데이터와 반응형 화면이며 실제 휴대전화가 아닙니다. 실습 사이트로 Codex UI나 모델 실행 증거가 아닙니다.",
}
FEATURE_ALT = {
    "zh-TW": "Completed 篩選顯示兩筆 Read，總計仍有三筆任務。",
    "zh-CN": "Completed 筛选显示两笔 Read，总计仍有三笔任务。",
    "en": "Completed shows two Read tasks while three tasks remain in total.",
    "ja": "Completed は Read 2件を表示し、全体は3件のままです。",
    "ko": "Completed는 Read 두 개를 표시하고 전체 작업은 세 개로 유지됩니다.",
}
cc = OpenCC("t2s")
parse = mistune.create_markdown(renderer="ast", plugins=["table"])


def new_pack(row):
    """Prepare only complete authored lessons; no planned placeholder packs."""
    slug = row["slug"]
    artwork = {
        "zh-TW": "原創流程示意圖，非產品介面截圖。",
        "zh-CN": "原创流程示意图，非产品界面截图。",
        "en": "Original workflow illustration, not a product screenshot.",
        "ja": "独自の手順図です。製品画面の画像ではありません。",
        "ko": "직접 제작한 흐름도이며 제품 화면이 아닙니다.",
    }
    image = {"src": f"/guides/{slug}/hero.jpg", "width": 1600, "height": 900,
             "credit": {"author": "Mokaair", "license": "© Mokaair"}}
    return {"slug": slug, "kind": "life", "destination_id": None,
            "topics": ["ai", "tutorial"], "display_order": 100 + row["order"],
            "locales": {locale: {**copy, "hero": {**image, "alt": artwork[locale]},
                "blocks": [{"type": "image", **image, "src": f"/guides/{slug}/diagram-1.svg",
                            "alt": artwork[locale], "caption": artwork[locale]}], "sources": []}
                for locale, copy in row["locales"].items()}}


def create_artwork(row):
    # Code-native illustration; text belongs to the article, not a fake product UI.
    target = ROOT / "apps/web/public/guides" / row["slug"] / "diagram-1.svg"
    if target.exists():
        return
    label = "CODEX LEARNING"
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="900" viewBox="0 0 1600 900"><title>Codex learning workflow</title><desc>Three numbered stages: identify the starting point, perform the exercise, and verify the result. Original illustration, not a product screenshot.</desc>
<rect width="1600" height="900" fill="#112e35"/><circle cx="1380" cy="100" r="440" fill="#17444c"/>
<text x="100" y="140" font-family="sans-serif" font-size="50" fill="#a8ead7">{label}</text>
<path d="M420 460H650M950 460H1180" stroke="#a8ead7" stroke-width="12"/>
<path d="M620 440L650 460L620 480M1150 440L1180 460L1150 480" fill="none" stroke="#a8ead7" stroke-width="12"/>
<g fill="#f6f2e9"><rect x="120" y="290" width="300" height="340" rx="36"/>
<rect x="650" y="290" width="300" height="340" rx="36"/><rect x="1180" y="290" width="300" height="340" rx="36"/></g>
<g font-family="sans-serif" font-size="130" text-anchor="middle" fill="#17444c"><text x="270" y="510">1</text><text x="800" y="510">2</text><text x="1330" y="510">3</text></g>
<text x="100" y="810" font-family="sans-serif" font-size="32" fill="#a8ead7">MOKAAIR / ORIGINAL LEARNING DIAGRAM</text></svg>'''
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(svg, encoding="utf-8")


def inline(nodes, locale):
    result = []
    for node in nodes:
        kind = node["type"]
        if kind in {"text", "codespan"}:
            result.append({"type": "code" if kind == "codespan" else "text", "text": node["raw"]})
        elif kind in {"softbreak", "linebreak"}:
            result.append({"type": "text", "text": "\n" if kind == "linebreak" else " "})
        elif kind in {"strong", "emphasis"}:
            result.extend(inline(node["children"], locale))
        elif kind == "link":
            label = "".join(span["text"] for span in inline(node["children"], locale))
            url = node["attrs"]["url"]
            if url.startswith("article:"):
                if not re.fullmatch(r"codex-[a-z0-9]+(?:-[a-z0-9]+)*", url[8:]):
                    raise ValueError("An article reference must be a canonical Codex slug")
                result.append({"type": "article", "text": label, "kind": "life", "slug": url[8:]})
            else:
                result.append({"type": "link", "text": label, "url": url})
        else:
            raise ValueError(f"Unsupported inline {kind}")
    # Preserve spaces while reducing unneeded adjacent text nodes.
    merged = []
    for span in result:
        if not span["text"]:
            continue
        if merged and span["type"] == merged[-1]["type"] == "text":
            merged[-1]["text"] += span["text"]
        else:
            merged.append(span)
    return merged


def plain(nodes, locale):
    return "".join(span["text"] for span in inline(nodes, locale))


def linked_references(nodes, locale, *, context=None):
    """Keep authored references actionable beside legacy plain-text blocks.

    Tables, lists and callouts remain compatible with the shared API/editor.
    Only explicit author Markdown links become structured reference paragraphs;
    stored legacy text is never reparsed as Markdown.
    """
    links = [span for span in inline(nodes, locale) if span["type"] in {"article", "link"}]
    if not links:
        return []
    lead = context or {
        "zh-TW": "本段提到的教學與資源", "zh-CN": "本段提到的教学与资源",
        "en": "Lessons and resources mentioned here", "ja": "この段落の教材・資料",
        "ko": "이 단락의 학습 자료",
    }[locale]
    spans = [{"type": "text", "text": lead + ": "}]
    for index, link in enumerate(links):
        if index:
            spans.append({"type": "text", "text": " · "})
        spans.append(link)
    return [{"type": "rich_paragraph", "inlines": spans}]


def compile_body(body, locale):
    blocks = []
    for node in parse(body):
        kind = node["type"]
        if kind == "blank_line":
            continue
        if kind == "heading":
            if node["attrs"]["level"] not in {2, 3}:
                raise ValueError("Author body uses only H2/H3; title is in catalog")
            blocks.append({"type": "heading", "level": node["attrs"]["level"], "text": plain(node["children"], locale)})
        elif kind == "paragraph":
            spans = inline(node["children"], locale)
            if len(spans) == 1 and spans[0]["type"] == "link":
                blocks.append(spans[0])
            else:
                blocks.append({"type": "rich_paragraph", "inlines": spans} if any(s["type"] != "text" for s in spans)
                              else {"type": "paragraph", "text": "".join(s["text"] for s in spans)})
        elif kind == "block_code":
            info = node.get("attrs", {}).get("info", "text").split(maxsplit=1)
            label = info[1] if len(info) > 1 else {
                "zh-TW": "本步驟範例", "zh-CN": "本步骤示例", "en": "Example for this step",
                "ja": "この手順の例", "ko": "이 단계의 예제",
            }[locale]
            blocks.append({"type": "code", "label": label, "language": info[0] if info else "text", "code": node["raw"]})
        elif kind == "list":
            items = []
            references = []
            for item in node["children"]:
                if len(item["children"]) != 1 or item["children"][0]["type"] not in {"block_text", "paragraph"}:
                    raise ValueError("Use a flat list or separate prose paragraphs")
                items.append(plain(item["children"][0]["children"], locale))
                references.extend(linked_references(item["children"][0]["children"], locale))
            blocks.append({"type": "list", "ordered": node["attrs"].get("ordered", False), "items": items})
            blocks.extend(references)
        elif kind == "block_quote":
            paragraphs = node["children"]
            if not all(child["type"] == "paragraph" for child in paragraphs):
                raise ValueError("Callouts contain plain paragraphs")
            blocks.append({"type": "callout", "tone": "info", "text": "\n".join(plain(child["children"], locale) for child in paragraphs)})
            for child in paragraphs:
                blocks.extend(linked_references(child["children"], locale))
        elif kind == "table":
            head, body = node["children"]
            blocks.append({"type": "table", "header": [plain(c["children"], locale) for c in head["children"]],
                           "rows": [[plain(c["children"], locale) for c in row["children"]] for row in body["children"]]})
            for row in body["children"]:
                nodes = [child for cell in row["children"] for child in cell["children"]]
                blocks.extend(linked_references(nodes, locale, context=plain(row["children"][0]["children"], locale)))
        else:
            raise ValueError(f"Unsupported block {kind}")
    return blocks


def simplified(body):
    # Only prose and fence labels are translated. Code bytes stay identical.
    output = []
    active = None
    for line in body.splitlines(keepends=True):
        if active:
            output.append(line)
            char, length = active
            if re.fullmatch(re.escape(char) + "{" + str(length) + ",}", line.strip()):
                active = None
        else:
            output.append(cc.convert(line))
            opening = re.match(r"^ {0,3}(`{3,}|~{3,})[^\r\n]*(?:\r?\n|$)", line)
            if opening:
                fence = opening.group(1)
                active = (fence[0], len(fence))
    if active:
        raise ValueError("Unclosed fenced example in author source")
    return "".join(output)


def summary_items(description, blocks):
    """Reuse localized article prose for a two-to-five sentence opening summary."""
    sentences = [item.strip() for item in re.split(r"(?<=[.!?。！？])\s*", description) if item.strip()]
    for block in blocks:
        if len(sentences) >= 2:
            break
        if block["type"] not in {"paragraph", "note", "callout"}:
            continue
        for item in re.split(r"(?<=[.!?。！？])\s*", block.get("text", "")):
            item = item.strip()
            if item and item not in sentences and len(item) <= 300:
                sentences.append(item)
            if len(sentences) >= 2:
                break
    if len(sentences) < 2 or any(len(item) > 300 for item in sentences[:5]):
        raise ValueError("Localized prose cannot form a valid two-to-five sentence summary")
    return sentences[:5]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    known_slugs = {row["slug"] for row in catalog} | {"codex-learning-hub"}
    source = AUTHORS / "sources.json"
    sources = json.loads(source.read_text(encoding="utf-8")) if source.exists() else {}
    results = []
    pending = []
    for row in catalog:
        id_text = f'{row["id"]:02d}'
        texts = {}
        for locale in ["zh-TW", "en", "ja", "ko"]:
            path = AUTHORS / locale / f"{id_text}.md"
            if path.exists():
                texts[locale] = path.read_text(encoding="utf-8")
        if "zh-TW" in texts:
            # Convert prose only: commands and configuration inside fences are identical.
            texts["zh-CN"] = simplified(texts["zh-TW"])
        if not texts:
            continue
        entry = {"id": row["id"], "slug": row["slug"], "authoredLocales": list(texts), "fullFiveLocales": len(texts) == 5, "compiled": False}
        entry["sourceHashes"] = {locale: sha256(body.encode("utf-8")).hexdigest() for locale, body in texts.items()}
        # Parse partial drafts for author errors, but never replace a multilingual pack partially.
        compiled = {locale: compile_body(body, locale) for locale, body in texts.items()}
        for locale, blocks in compiled.items():
            missing = {span["slug"] for block in blocks for span in block.get("inlines", [])
                       if span["type"] == "article" and span["slug"] not in known_slugs}
            if missing:
                raise ValueError(f"{id_text}/{locale}: unknown article references: {sorted(missing)}")
        # A translated command can be valid syntax while changing the example's behavior.
        reference_locale = "zh-TW" if "zh-TW" in compiled else next(iter(compiled))
        reference = [(b["language"], b["code"]) for b in compiled[reference_locale] if b["type"] == "code"]
        for locale, blocks in compiled.items():
            if [(b["language"], b["code"]) for b in blocks if b["type"] == "code"] != reference:
                raise ValueError(f"{id_text}/{locale}: code differs from the shared example")
        entry["blocksByLocale"] = {locale: len(blocks) for locale, blocks in compiled.items()}
        entry["zhTWProseCharacters"] = sum(len(b.get("text", "")) + sum(len(s["text"]) for s in b.get("inlines", [])) for b in compiled.get("zh-TW", []) if b["type"] not in {"code", "heading"})
        if len(texts) == 5:
            pack_path = PACKS / f'{row["slug"]}.json'
            pack = json.loads(pack_path.read_text(encoding="utf-8")) if pack_path.exists() else new_pack(row)
            for locale, blocks in compiled.items():
                # Keep original artwork and attribution; authored prose replaces every old paragraph.
                pictures = [block for block in pack["locales"][locale]["blocks"] if block["type"] == "image"]
                if row["id"] == 31:
                    # The former static landing-page exercise is unrelated to the todo workshop.
                    legacy = {f'/guides/{row["slug"]}/workshop-{width}.png' for width in [390, 1280]}
                    pictures = [picture for picture in pictures if picture["src"] not in legacy]
                # Idempotently append real example screenshots with honest platform captions.
                if row["id"] in {3, 6, 26, 31}:
                    pictures = [picture for picture in pictures if "todo-" not in picture["src"]]
                    for width in [390, 1280]:
                        pictures.append({"type": "image", "src": f"/guides/codex-first-project/todo-{width}.png",
                                         "alt": SCREENSHOT_ALT[locale], "caption": SCREENSHOT_CAPTIONS[locale].replace("390px", f"{width}px"),
                                         "width": width, "height": 900, "credit": {"author": "Mokaair", "license": "© Mokaair"}})
                if row["id"] in {6, 7}:
                    pictures = [picture for picture in pictures if "/reference-" not in picture["src"]]
                    for width in [390, 1280]:
                        pictures.append({"type": "image", "src": f'/guides/{row["slug"]}/reference-{width}.png',
                                         "alt": REFERENCE_ALT[row["id"]][locale], "caption": REFERENCE_CAPTIONS[locale].format(width=width),
                                         "width": width, "height": 900, "credit": {"author": "Mokaair", "license": "© Mokaair"}})
                if row["id"] == 47:
                    pictures = [picture for picture in pictures if "/reference-" not in picture["src"]]
                    for width in [390, 1280]:
                        pictures.append({"type": "image", "src": f'/guides/{row["slug"]}/reference-{width}.png',
                                         "alt": FEATURE_ALT[locale], "caption": FEATURE_CAPTIONS[locale],
                                         "width": width, "height": 900, "credit": {"author": "Mokaair", "license": "© Mokaair"}})
                description = pack["locales"][locale].get("description")
                summaries = ([{"type": "summary", "items": summary_items(description, blocks)}]
                             if description else [])
                pack["locales"][locale]["blocks"] = [*summaries, *blocks, *pictures]
                pack["locales"][locale]["sources"] = sources[id_text]
            encoded = json.dumps(pack, ensure_ascii=False, indent=2) + "\n"
            entry["packHash"] = sha256(encoded.encode("utf-8")).hexdigest()
            pending.append((row, pack_path, encoded))
            entry["compiled"] = True
        results.append(entry)
    report = {"stage": "authored drafts, not editorial approval or publication", "lessons": results}
    if args.check:
        stale = [str(path.relative_to(ROOT)) for _, path, encoded in pending
                 if not path.exists() or path.read_text(encoding="utf-8") != encoded]
        if stale:
            raise ValueError("Stale compiled packs; rebuild author sources: " + ", ".join(stale))
        report_path = AUTHORS / "build-report.json"
        if not report_path.exists() or json.loads(report_path.read_text(encoding="utf-8")) != report:
            raise ValueError("Stale source/pack hash report; rebuild author sources")
    if pending:
        # The authoring environment has Markdown tools; use the project's API
        # environment for the exact runtime schema before replacing any pack.
        api_python = ROOT / "apps/api/.venv/Scripts/python.exe"
        if not api_python.exists():
            api_python = ROOT / "apps/api/.venv/bin/python"
        if not api_python.exists():
            raise ValueError("Set up apps/api/.venv before validating authored packs")
        validator = "from app.guides.content_pack import ArticlePack\nimport json, sys\nfor slug, raw in json.load(sys.stdin):\n try: ArticlePack.model_validate_json(raw)\n except Exception as exc: raise SystemExit(f'{slug}: {exc}')\n"
        checked = subprocess.run([str(api_python), "-X", "utf8", "-c", validator],
            cwd=ROOT / "apps/api", input=json.dumps([(row["slug"], encoded) for row, _, encoded in pending]),
            capture_output=True, encoding="utf-8", check=False)
        if checked.returncode:
            raise ValueError(checked.stderr or checked.stdout)
    if not args.check:
        # Validate the whole batch before replacing any published-format draft.
        for row, pack_path, encoded in pending:
            create_artwork(row)
            pack_path.write_text(encoded, encoding="utf-8")
        (AUTHORS / "build-report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"stage": report["stage"], "compiled": sum(item["compiled"] for item in results),
                      "lessons": [{key: item[key] for key in ["id", "fullFiveLocales", "zhTWProseCharacters"]} for item in results]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
