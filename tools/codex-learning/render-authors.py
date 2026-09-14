"""Render explicitly authored parallel paragraphs; never machine-summarize locales."""
import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
AUTHORS = ROOT / "docs/codex-learning/deep"
LOCALES = ["zh-TW", "en", "ja", "ko"]
BACK = ["返回 Codex 教學總目錄", "Back to the Codex learning hub", "Codex 教学目次に戻る", "Codex 학습 목차로 돌아가기"]


def render(module):
    outputs = {}
    for index, locale in enumerate(LOCALES):
        parts = [f"[{BACK[index]}](article:codex-learning-hub)"]
        for block in module["blocks"]:
            kind = block["type"]
            if kind == "code":
                code = block["code"]
                # Markdown tutorials can themselves contain fenced examples.
                # A longer outer fence keeps that entire example inert.
                length = max([2, *(len(run) for run in re.findall(r"`+", code))]) + 1
                fence = "`" * length
                parts.append(f'{fence}{block["language"]}\n{code.rstrip(chr(10))}\n{fence}')
            elif kind in {"h2", "h3", "p", "note"}:
                values = block["text"]
                if len(values) != 4 or any(not isinstance(value, str) or not value.strip() for value in values):
                    raise ValueError(f'{module["id"]}: every paragraph needs four complete translations')
                prefix = {"h2": "## ", "h3": "### ", "p": "", "note": "> "}[kind]
                parts.append(prefix + values[index])
            else:
                raise ValueError(f"Unsupported author block: {kind}")
        parts.append(f"[{BACK[index]}](article:codex-learning-hub)")
        outputs[locale] = "\n\n".join(parts) + "\n"
    return outputs


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    modules = list((AUTHORS / "modules").glob("*.json"))
    for path in sorted(modules):
        module = json.loads(path.read_text(encoding="utf-8"))
        if path.stem != f'{module["id"]:02d}':
            raise ValueError("Author filename must match permanent ID")
        for locale, body in render(module).items():
            target = AUTHORS / locale / f'{module["id"]:02d}.md'
            if args.check:
                if not target.exists() or target.read_text(encoding="utf-8") != body:
                    raise ValueError(f"Stale rendered author file: {target}")
            else:
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(body, encoding="utf-8")
    print(f"{len(modules)} authored modules / {len(modules) * 4} complete source translations")


if __name__ == "__main__":
    main()
