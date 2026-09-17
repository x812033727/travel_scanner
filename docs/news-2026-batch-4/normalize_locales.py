"""normalize_locales.py <prefix> [--apply] -- mechanical, locale-specific typography and fixed terms after review.

zh-CN: 「」『』 -> “”‘’ ; 核查 -> 查核 (batch convention).
ja:    half-width parens next to Japanese text -> full-width (legal sub-items like (a) and "Regulation (EU)" stay);
       half-width colon after Japanese text -> full-width; 《》 -> 「」; 査読 -> 確認 (査読 means peer review).
ko:    검증일 -> 확인일.
The same transformation is applied to research translations[locale] (hero_label, diagram) so captions stay identical.
Titles change too, so run align_links.py --apply afterwards. Run from apps/api with the API venv.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "apps/api"))
sys.path.insert(0, str(ROOT / "docs/news-2026-batch-4"))
from app.guides.schemas import GuideDocument  # noqa: E402
from verticals import workspace_of  # noqa: E402

CONTENT = ROOT / "apps/api/app/guides/content"
KEEP = ("url", "src", "checked_on", "type", "level", "tone", "width", "height", "slug", "kind",
        "language", "partner", "event_date", "news_date")
JP = r"\u3040-\u30ff\u3400-\u9fff"
counts = {}


def bump(key, n):
    if n:
        counts[key] = counts.get(key, 0) + n


def zh_cn(text):
    for a, b in (("「", "“"), ("」", "”"), ("『", "‘"), ("』", "’")):
        bump("zh-CN " + a, text.count(a))
        text = text.replace(a, b)
    bump("zh-CN 核查", text.count("核查"))
    return text.replace("核查", "查核")


def ja(text):
    def paren(match):
        before, inner = match.group(1), match.group(2)
        if re.fullmatch(r"[a-z]|[ivx]+|EU", inner):  # Article 14(2)(a), Regulation (EU) 2024/2847
            return match.group(0)
        if re.search(f"[{JP}]", inner) or re.match(f"[{JP}）」』％%]", before or ""):
            bump("ja paren", 1)
            return f"{before}（{inner}）"
        return match.group(0)

    if "障礙修復說明" not in text:  # a quoted Chinese title keeps its own half-width parens
        text = re.sub(r"(.?)\(([^()]*)\)", paren, text)
    new, n = re.subn(f"(?<=[{JP}%）」』]):(?!\\d) ?", "：", text)
    bump("ja colon", n)
    text = new
    for a, b in (("《", "「"), ("》", "」")):
        bump("ja " + a, text.count(a))
        text = text.replace(a, b)
    bump("ja 査読", text.count("査読"))
    return text.replace("査読", "確認")


def ko(text):
    bump("ko 검증일", text.count("검증일"))
    return text.replace("검증일", "확인일")


FIX = {"zh-CN": zh_cn, "ja": ja, "ko": ko}


def walk(node, fix):
    if isinstance(node, str):
        return fix(node)
    if isinstance(node, list):
        return [walk(item, fix) for item in node]
    if isinstance(node, dict):
        return {key: (item if key in KEEP else walk(item, fix)) for key, item in node.items()}
    return node


prefix = sys.argv[1]
apply = "--apply" in sys.argv
for path in sorted(CONTENT.glob(prefix + "*.json")):
    pack = json.loads(path.read_text(encoding="utf-8"))
    record_path = workspace_of(pack["slug"]) / "research" / path.name
    record = json.loads(record_path.read_text(encoding="utf-8"))
    for locale, fix in FIX.items():
        if locale not in pack["locales"]:
            continue
        pack["locales"][locale] = walk(pack["locales"][locale], fix)
        GuideDocument.model_validate(pack["locales"][locale])
        holder = record.get("translations", {}).get(locale)
        if holder:
            for key in ("hero_label", "diagram"):
                if key in holder:
                    holder[key] = walk(holder[key], fix)
    if apply:
        path.write_bytes((json.dumps(pack, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
        record_path.write_bytes((json.dumps(record, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
print("applied" if apply else "dry run", dict(sorted(counts.items())))
