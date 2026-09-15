"""Build reviewed multilingual lesson sources into the site's existing content packs.

Run with: uv run --with opencc-python-reimplemented==0.1.7 python tools/codex-learning/build.py
Then: node tools/codex-learning/render.mjs
No database writes or publication occur here.
"""
import html
import json
import re
from pathlib import Path
from opencc import OpenCC

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "docs/codex-learning/lessons"
CATALOG = ROOT / "apps/web/lib/codex-learning/catalog.json"
PACKS = ROOT / "apps/api/app/guides/content"
PUBLIC = ROOT / "apps/web/public/guides"
LOCALES = ["zh-TW", "zh-CN", "en", "ja", "ko"]
CHECKED = "2026-09-14"
HUB = "codex-learning-hub"
cc = OpenCC("t2s")
COPY = {
    "zh-TW": ["你會學到什麼", "開始之前", "逐步操作", "練習需求", "範例與驗證", "完成結果", "常見問題", "延伸閱讀", "返回 Codex 教學總目錄", "檢查項目", "驗收方式", "先確認環境", "完成一個操作", "檢查真實結果", "實作順序示意圖，非產品介面截圖。", "跨平台操作依官方文件查證；未在每個系統實測。介面與帳號提供的功能可能不同。", "預估操作時間", "分鐘", "官方來源", "準備", "操作", "驗證"],
    "en": ["What you will learn", "Before you start", "Step by step", "Practice request", "Example and verification", "Expected result", "Troubleshooting", "Continue learning", "Back to the Codex learning hub", "Check", "Acceptance method", "Confirm the environment", "Complete one action", "Inspect the actual result", "Workflow illustration, not a product screenshot.", "Cross-platform steps were checked against official documentation, not tested on every operating system. Interfaces and account availability can differ.", "Estimated practice time", "min", "Official sources", "Prepare", "Act", "Verify"],
    "ja": ["学べること", "始める前に", "操作手順", "練習用の依頼", "例と確認方法", "期待する結果", "トラブル対応", "次に学ぶこと", "Codex 学習ガイドに戻る", "確認項目", "確認方法", "環境を確かめる", "一つの操作を行う", "実際の結果を調べる", "作業の流れを表す図です。製品画面の画像ではありません。", "各 OS の手順は公式文書で確認していますが、すべての環境で実機検証したわけではありません。画面や提供状況は異なる場合があります。", "練習時間の目安", "分", "公式の出典", "準備", "操作", "確認"],
    "ko": ["학습 목표", "시작 전 준비", "단계별 작업", "연습 요청", "예시와 검증", "예상 결과", "문제 해결", "이어서 학습하기", "Codex 학습 목차로 돌아가기", "검사 항목", "확인 방법", "환경 확인", "작업 하나 완료", "실제 결과 확인", "작업 흐름을 설명하는 그림이며 제품 스크린샷이 아닙니다.", "각 OS 절차는 공식 문서로 확인했으며 모든 환경에서 직접 시험한 것은 아닙니다. 화면과 계정별 제공 기능은 다를 수 있습니다.", "예상 실습 시간", "분", "공식 출처", "준비", "실행", "검증"],
}
COPY["zh-CN"] = [cc.convert(s) for s in COPY["zh-TW"]]
TERMS = {"AGENTS.md": 10, "SKILL.md": 23, "config.toml": 16, "Codex CLI": 5,
         "README.md": 22, "MCP": 25, "Remote": 4, "GitHub": 15, "Worktree": 27,
         "worktree": 27, "/plan": 8, "/review": 21, "codex exec": 30, "Plugins": 24}
DIAGRAMS = [
    ["Task", "Environment", "Files"], ["Login", "Workspace", "Usage"],
    ["Install", "Folder", "Review"], ["Phone", "Mac / Windows", "Files"],
    ["Terminal", "codex", "Project"], ["Request", "index.html", "Browser"],
    ["Goal", "Constraints", "Acceptance"], ["Questions", "/plan", "Implementation"],
    ["Plain text", "README.md", "Preview"], ["Global", "Project", "Working directory"],
    ["Shell", "Interactive /", "Result"], ["Symptom", "One check", "Retry"],
    ["Project", "Task", "Handoff"], ["Editor", "Selection", "Diff"],
    ["GitHub", "Cloud environment", "Pull request"], ["User config", "Project config", "CLI override"],
    ["Task", "Model / effort", "Evaluation"], ["Request", "Permission", "Action"],
    ["Branch", "Diff", "Commit"], ["Reproduce", "Fix", "Regression"],
    ["Tests", "Review", "PR"], ["Evidence", "Handoff", "Resume"],
    ["SKILL.md", "Invoke", "Output"], ["Plugin", "Connect", "Tool"],
    ["Configuration", "Handshake", "Tool result"], ["Reference", "Change", "Compare"],
    ["Repository", "Worktree A / B", "Integration"], ["Bounded tasks", "Subagents", "Review"],
    ["Schedule", "Run", "Notification"], ["Prompt", "codex exec", "JSONL / report"],
    ["Brief", "HTML / CSS", "Browser checks"], ["contacts.csv", "Cleanup", "clean.csv"],
]

HUB_INTRO = {
    "zh-TW": "從零開始使用 Codex：32 篇獨立教學分成入門、日常工作與進階實戰。先用下方搜尋、程度、平台或需求篩選找文章。每篇都有可操作的練習、驗收方法與官方來源。新手建議依序閱讀 01、03 或 05、06、09、10、11、12；手機讀者先看 04，了解遠端電腦的必要條件。",
    "en": "Learn Codex through 32 independent tutorials covering first steps, everyday work and advanced projects. Search below or filter by experience, platform and goal. Every lesson includes an exercise, acceptance checks and official sources. Beginners can follow 01, then 03 or 05, followed by 06, 09, 10, 11 and 12. Mobile readers should start with 04 to understand the remote computer requirements.",
    "ja": "Codex を初歩、日常作業、応用実践の 32 記事で学びます。下の検索や習熟度・環境・目的の絞り込みで探してください。各記事には練習、確認方法、公式出典があります。初めての方は 01、03 または 05、06、09、10、11、12 の順がおすすめです。スマートフォンでは先に 04 で接続先コンピューターの条件を確認します。",
    "ko": "Codex를 입문, 일상 작업, 고급 실습의 32개 독립 튜토리얼로 배웁니다. 아래 검색이나 수준·플랫폼·목표 필터를 사용하세요. 각 글에는 실습, 검증 방법과 공식 출처가 있습니다. 처음이라면 01, 03 또는 05, 06, 09, 10, 11, 12 순서로 읽으세요. 모바일 사용자는 04에서 연결할 컴퓨터의 조건부터 확인하세요.",
}
HUB_INTRO["zh-CN"] = cc.convert(HUB_INTRO["zh-TW"])
RELATED = [[2,3,5],[1,17,18],[4,5,13],[3,13,15],[3,11,12],[7,9,31],[8,20,22],[7,19,21],[10,22,23],[9,16,23],[5,8,30],[2,5,18],[22,27,29],[5,19,21],[18,21,27],[10,17,25],[2,7,30],[16,24,25],[20,21,27],[7,19,21],[19,20,15],[9,10,13],[10,24,25],[18,23,25],[16,18,24],[3,20,31],[13,19,28],[7,21,27],[13,18,30],[11,18,32],[6,21,26],[6,20,30]]

def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

def heading(text):
    return {"type": "heading", "level": 2, "text": text}

def svg(slug, number, labels):
    # Deliberately a diagram, never a fabricated screenshot. Only short labels enter SVG.
    boxes = []
    for i, label in enumerate(labels):
        y = 220 + i * 205
        boxes.append(f'<rect x="95" y="{y}" width="1410" height="150" rx="30" fill="#fff"/>'
                     f'<text x="130" y="{y+98}" fill="#187b78" font-size="64" font-family="Arial">0{i+1}</text>'
                     f'<text x="260" y="{y+98}" fill="#102b35" font-size="64" font-family="Arial">{html.escape(label)}</text>')
        if i < 2:
            boxes.append(f'<path d="M 800 {y+160} v 32 m -12 -12 l 12 12 12 -12" fill="none" stroke="#237d78" stroke-width="5"/>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="900" viewBox="0 0 1600 900">'
            f'<title>Codex learning diagram {number}</title><desc>{html.escape(" to ".join(labels))}</desc>'
            '<rect width="1600" height="900" fill="#edf4ef"/>'
            '<circle cx="1450" cy="80" r="250" fill="#d9e9df"/>'
            f'<text x="95" y="140" fill="#102b35" font-size="72" font-family="Arial">CODEX / {number:02d}</text>'
            + "".join(boxes) + '</svg>')

def main():
    if (ROOT / "docs/codex-learning/deep/zh-TW/03.md").exists():
        raise SystemExit("Legacy 32-lesson bootstrap disabled: use build-depth.py; do not overwrite authored deep content or the 60-lesson catalog.")
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    records = {r["id"]: r for path in sorted(SOURCE.glob("*.json"))
               for r in [json.loads(path.read_text(encoding="utf-8"))]}
    ready = set(records)
    for row in catalog:
        row["related"] = RELATED[row["id"] - 1]
        row["ready"] = row["id"] in ready
        row["checkedOn"] = CHECKED if row["ready"] else None
        if not row["ready"]:
            continue
        record = records[row["id"]]
        if record.get("codeFile"):
            record["code"] = {"language": record["codeLanguage"], "code": (ROOT / record["codeFile"]).read_text(encoding="utf-8")}
        if "zh-CN" not in record["text"]:
            # Script conversion for this closely related locale; output remains reviewable JSON.
            record["text"]["zh-CN"] = json.loads(cc.convert(json.dumps(record["text"]["zh-TW"], ensure_ascii=False)))
        slug = row["slug"]
        images = PUBLIC / slug
        images.mkdir(parents=True, exist_ok=True)
        artwork = svg(slug, row["id"], DIAGRAMS[row["id"]-1])
        (images / "diagram-1.svg").write_text(artwork, encoding="utf-8")
        documents = {}
        for locale in LOCALES:
            intro, before, steps, result, trouble, prompt = record["text"][locale]
            c = COPY[locale]
            row["locales"][locale]["description"] = intro
            used = set()
            def paragraph(text):
                spans = []
                pattern = "|".join(re.escape(term) for term in sorted(TERMS, key=len, reverse=True))
                start = 0
                for match in re.finditer(pattern, text):
                    target = TERMS[match.group()]
                    if target == row["id"] or target in used or target not in ready:
                        continue
                    if match.start() > start:
                        spans.append({"type": "text", "text": text[start:match.start()]})
                    spans.append({"type": "link", "text": match.group(), "url": f'https://mokaair.com/{locale}/life/{catalog[target-1]["slug"]}'})
                    used.add(target)
                    start = match.end()
                if not spans:
                    return {"type": "paragraph", "text": text}
                if start < len(text):
                    spans.append({"type": "text", "text": text[start:]})
                return {"type": "rich_paragraph", "spans": spans}
            blocks = [paragraph(intro), heading(c[0]), paragraph(result),
                      {"type": "paragraph", "text": f'{c[16]}: {row["minutes"]} {c[17]}'},
                      heading(c[1]), paragraph(before), heading(c[2])]
            for n, step in enumerate(steps, 1):
                blocks.append(paragraph(f"{n}. {step}"))
            diagram_caption = f'{row["id"]:02d}. {row["locales"][locale]["title"]} — {c[14]} {" → ".join(DIAGRAMS[row["id"]-1])}'
            blocks.append({"type": "image", "src": f"/guides/{slug}/diagram-1.svg", "alt": diagram_caption, "width": 1600, "height": 900, "caption": diagram_caption, "credit": {"author": "Mokaair", "license": "© Mokaair", "source_url": None}})
            blocks += [heading(c[3]), {"type": "code", "language": "text", "code": prompt}, heading(c[4])]
            if record.get("code"):
                blocks.append({"type": "code", **record["code"]})
            if row["id"] == 32:
                blocks.append({"type": "code", "language": "csv", "code": (ROOT / "docs/codex-learning/examples/contacts.csv").read_text(encoding="utf-8")})
                blocks.append({"type": "code", "language": "csv", "code": "name,email\nAlice,alice@example.test\nBob,bob@example.test\n"})
            if row["id"] == 31:
                screenshot_caption = {
                    "zh-TW": "Windows 上的 Edge 153.0.4234.32 實際瀏覽器截圖，2026-09-14；使用公開虛構練習 HTML。數字 01／02／03 對應規劃、製作與驗證。390px 為模擬手機寬度，非 iPhone 或 Android 實機測試。橘框是 Tab 鍵的焦點提示。",
                    "en": "Actual browser capture: Edge 153.0.4234.32 on Windows, 2026-09-14, using fictional practice HTML. 01/02/03 identify planning, building and verification. 390px simulates a mobile viewport, not an iPhone or Android device test. The orange outline shows keyboard focus after Tab.",
                    "ja": "Windows の Edge 153.0.4234.32 による実際のブラウザー画像、2026-09-14。公開可能な架空の練習 HTML を使用。01／02／03 は計画・制作・確認です。390px はモバイル幅の模擬表示で、iPhone・Android の実機試験ではありません。オレンジ枠は Tab キーによるフォーカスです。",
                    "ko": "Windows의 Edge 153.0.4234.32 실제 브라우저 캡처, 2026-09-14. 공개 가능한 가상 연습 HTML을 사용했습니다. 01/02/03은 계획·제작·검증입니다. 390px은 모바일 화면 폭 시뮬레이션이며 iPhone·Android 실기기 시험이 아닙니다. 주황색 테두리는 Tab 키 포커스입니다.",
                }
                screenshot_caption["zh-CN"] = cc.convert(screenshot_caption["zh-TW"])
                for width, height in [(390, 1589), (1280, 1092)]:
                    blocks.append({"type": "image", "src": f"/guides/{slug}/workshop-{width}.png", "alt": f'{row["locales"][locale]["title"]} — {width}px / Windows Edge', "caption": screenshot_caption[locale], "width": width, "height": height, "credit": {"author": "Mokaair", "license": "© Mokaair"}})
            blocks.append({"type": "table", "header": [c[9], c[10]], "rows": [[c[11], before], [c[12], steps[-1]], [c[13], result]]})
            blocks += [heading(c[5]), paragraph(result), heading(c[6]), paragraph(trouble),
                       {"type": "callout", "tone": "info", "title": c[18], "text": c[15]}, heading(c[7]),
                       {"type": "link", "text": c[8], "url": f"https://mokaair.com/{locale}/life/{HUB}"}]
            documents[locale] = {"title": row["locales"][locale]["title"], "description": intro,
                "hero": {"src": f"/guides/{slug}/hero.jpg", "alt": c[14], "width": 1600, "height": 900,
                         "credit": {"author": "Mokaair", "license": "© Mokaair", "source_url": None}},
                "blocks": blocks, "sources": [{"title": p, "url": f"https://learn.chatgpt.com/docs/{p}", "checked_on": CHECKED} for p in record["sources"]]}
        write_json(PACKS / f"{slug}.json", {"slug": slug, "kind": "life", "destination_id": None, "topics": ["ai", "tutorial"], "display_order": 100 + row["id"], "locales": documents})
    write_json(CATALOG, catalog)
    hub_docs = {}
    hub_titles = ["Codex 學習中心：完整教學目錄", "Codex 学习中心：完整教程目录", "Codex learning hub: tutorial directory", "Codex 学習ガイド：全記事の目次", "Codex 학습 센터: 전체 튜토리얼 목차"]
    for i, locale in enumerate(LOCALES):
        c = COPY[locale]
        hub_docs[locale] = {"title": hub_titles[i], "description": HUB_INTRO[locale],
            "hero": {"src": f"/guides/{HUB}/hero.jpg", "alt": c[14], "width": 1600, "height": 900, "credit": {"author": "Mokaair", "license": "© Mokaair"}},
            "blocks": [heading(c[0]), {"type": "paragraph", "text": "32 / Windows · macOS · Linux · iOS · Android / CLI · IDE · Cloud"},
                       heading(c[1]), {"type": "paragraph", "text": c[15]},
                       {"type": "table", "header": [c[9], c[10]], "rows": [["01–12", c[11]], ["13–22", c[12]], ["23–32", c[13]]]},
                       heading(c[7]), {"type": "callout", "tone": "info", "text": c[15]}],
            "sources": [{"title": "OpenAI documentation index", "url": "https://learn.chatgpt.com/docs/llms.txt", "checked_on": CHECKED}]}
    (PUBLIC / HUB).mkdir(parents=True, exist_ok=True)
    (PUBLIC / HUB / "diagram-1.svg").write_text(svg(HUB, 0, ["01-12 / Start", "13-22 / Practice", "23-32 / Build"]), encoding="utf-8")
    write_json(PACKS / f"{HUB}.json", {"slug": HUB, "kind": "life", "destination_id": None, "topics": ["ai", "tutorial"], "featured": True, "display_order": 10, "locales": hub_docs})
    print(f"Built {len(records)} lessons + hub, each in {len(LOCALES)} locales; no publication.")

if __name__ == "__main__":
    main()
