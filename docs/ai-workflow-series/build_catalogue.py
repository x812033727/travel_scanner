"""``series_data/ai-workflow.json`` derived from the shipped packs, in one command:

    build_catalogue.py [--related] [--check]

The catalogue ``app.guides.series`` serves for the hub page -- four groups, three reading
paths, one ``Lesson`` per article -- is generated rather than typed. Title, sources and the
outcome sentence come from each pack; the number from ``series.SLUGS``; and what a pack does
not carry -- group, level, platforms, aliases, prerequisites, related -- from the tables
below, which are ``agents/ASSIGNMENTS.md``'s "系列內互相引用" section in code.

``--related`` also writes the related column into each pack's ``related`` field, so the
article page's further-reading grid and the catalogue agree. ``--check`` validates the
catalogue against the packs without writing anything (the tests do the same on CI).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from series import CONTENT, HUB, LOCALE, ROOT, SERIES, SLUGS  # noqa: E402

from app.guides.series import Catalogue  # noqa: E402

CATALOGUE = ROOT / "apps/api/app/guides/series_data" / f"{SERIES}.json"

GROUPS = [
    {"id": "A", "title": "觀念：流程、拆法與取捨"},
    {"id": "B", "title": "接線：統一 API、路由與交接"},
    {"id": "C", "title": "協作：互審、代理分工與 MCP"},
    {"id": "D", "title": "營運：本機混搭、追蹤與防護"},
]
GROUP_OF = {slug: "ABCD"[i // 3] for i, slug in enumerate(SLUGS)}

S = dict(zip(range(1, 13), SLUGS))
PATHS = [
    {"id": "concepts", "title": "觀念路線", "slugs": [S[1], S[2], S[3], S[12]]},
    {"id": "builder", "title": "接線路線", "slugs": [S[1], S[4], S[5], S[6], S[9], S[10]]},
    {"id": "operator", "title": "營運路線", "slugs": [S[3], S[7], S[8], S[11], S[12]]},
]
LEVEL = {**{S[i]: "beginner" for i in (1, 2, 3)}, **{S[i]: "intermediate" for i in range(4, 11)}, **{S[i]: "advanced" for i in (11, 12)}}
PLATFORMS = {**{S[i]: ["web"] for i in (1, 2, 3)}, **{S[i]: ["cli"] for i in range(4, 13)}}
PREREQUISITES = {S[2]: [S[1]], S[3]: [S[1]], S[4]: [S[3]], S[5]: [S[3], S[4]], S[6]: [S[4]], S[7]: [S[6]],
                 S[8]: [S[1]], S[9]: [S[8]], S[10]: [S[4]], S[11]: [S[7]], S[12]: [S[11]]}
RELATED = {S[1]: [S[2], S[3], S[12]], S[2]: [S[1], S[3], S[5]], S[3]: [S[2], S[5], S[11]], S[4]: [S[5], S[6], S[10]],
           S[5]: [S[3], S[4], S[6]], S[6]: [S[5], S[7], S[12]], S[7]: [S[6], S[11], S[12]], S[8]: [S[9], S[6], S[7]],
           S[9]: [S[8], S[10], S[4]], S[10]: [S[9], S[4], S[12]], S[11]: [S[7], S[3], S[12]], S[12]: [S[11], S[6], S[10]]}
ALIASES = {
    S[1]: ["工作流", "workflow", "代理", "agent", "提示詞串接"],
    S[2]: ["拆任務", "分工", "子代理", "資料敏感度"],
    S[3]: ["成本", "延遲", "p95", "快取", "批次", "定價"],
    S[4]: ["OpenRouter", "LiteLLM", "base_url", "OpenAI 相容"],
    S[5]: ["路由", "級聯", "cascade", "fallback", "重試"],
    S[6]: ["JSON Schema", "結構化輸出", "jsonschema", "交接"],
    S[7]: ["評審", "judge", "投票", "rubric", "集成"],
    S[8]: ["Claude Code", "Codex", "Gemini CLI", "headless", "claude -p", "codex exec"],
    S[9]: ["MCP", "Model Context Protocol", "工具伺服器", "設定檔"],
    S[10]: ["Ollama", "本機", "開放權重", "去識別化", "gemma4"],
    S[11]: ["追蹤", "tracing", "評測", "evals", "JSONL", "OpenTelemetry"],
    S[12]: ["防護", "guardrails", "提示詞注入", "預算", "迴圈"],
}


def load(slug: str) -> dict:
    return json.loads((CONTENT / f"{slug}.json").read_text(encoding="utf-8"))


def outcome_of(description: str) -> str:
    first = description.split("。")[0].strip()
    return (first + "。") if first else description


def build() -> dict:
    entries = []
    for number, slug in enumerate(SLUGS, 1):
        pack = load(slug)
        doc = pack["locales"][LOCALE]
        entries.append({
            "slug": slug,
            "title": doc["title"],
            "outcome": outcome_of(doc["description"]),
            "sources": [source["url"] for source in doc["sources"]],
            "number": number,
            "group": GROUP_OF[slug],
            "level": LEVEL[slug],
            "platforms": PLATFORMS[slug],
            "aliases": ALIASES[slug],
            "prerequisites": PREREQUISITES.get(slug, []),
            "related": RELATED[slug],
        })
    data = {"slug": SERIES, "locale": LOCALE, "hub": HUB, "groups": GROUPS, "paths": PATHS, "entries": entries}
    Catalogue.model_validate(data)
    return data


def write_related() -> None:
    for slug in SLUGS:
        path = CONTENT / f"{slug}.json"
        pack = json.loads(path.read_text(encoding="utf-8"))
        if pack.get("related") == RELATED[slug]:
            continue
        # Keep the key order the writers used: related sits before locales.
        rebuilt = {}
        for key, value in pack.items():
            if key == "locales":
                rebuilt["related"] = RELATED[slug]
            if key != "related":
                rebuilt[key] = value
        path.write_text(json.dumps(rebuilt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print("related written:", slug)


def main() -> int:
    missing = [slug for slug in SLUGS if not (CONTENT / f"{slug}.json").is_file()]
    if missing:
        print("packs not written yet:", *missing)
        return 1
    if "--related" in sys.argv:
        write_related()
    data = build()
    if "--check" in sys.argv:
        current = json.loads(CATALOGUE.read_text(encoding="utf-8")) if CATALOGUE.is_file() else None
        print("catalogue up to date" if current == data else "catalogue differs from the packs")
        return 0 if current == data else 1
    CATALOGUE.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("wrote", CATALOGUE.relative_to(ROOT), "with", len(data["entries"]), "entries")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
