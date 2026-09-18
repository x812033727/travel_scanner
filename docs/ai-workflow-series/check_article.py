"""Everything one article of the AI workflow series must satisfy before it ships, in one command:

    check_article.py <slug> [--assets]

Prints ``OK`` or ``FAIL`` with one line per problem. The news batch's ``check_article.py`` is the
model, with its news-only rules dropped (event date, the five-section skeleton, sources 2-4, the
two-link ending, five locales) and three tutorial rules added: code blocks compile, carry no
secret and name only models the workspace has seen on an official page.

Run from ``apps/api`` with the API virtualenv. ``--assets`` also checks the built hero and diagram.
"""
from __future__ import annotations

import io
import json
import py_compile
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from series import (  # noqa: E402
    CONTENT,
    HUB,
    HUB_TITLE,
    INTRO,
    LOCALE,
    PUBLIC,
    RESEARCH,
    ROOT,
    SLUGS,
    TOPICS,
    WORKSPACE,
    load,
    order_of,
)

from app.guides.content_pack import ArticlePack  # noqa: E402
from app.guides.pack_ingest import (  # noqa: E402
    HERO_MAX_BYTES,
    HERO_SIZE,
    IMAGE_HARD_CAP,
    check_svg,
    errors,
    lint_document,
    missing_diagram_numbers,
)
from app.guides.schemas import CodeBlock, FaqBlock, GuideDocument, SummaryBlock  # noqa: E402
from app.guides.taxonomy import LIFE_SEED_SUBTOPICS, LIFE_SEED_TOPICS  # noqa: E402

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

# The news batch's helpers, imported by path rather than copied: the block walkers, the
# simplified-character detector and the schema-derived item bounds.
_news = ROOT / "docs/news-2026-batch-4"
_verticals = load("news_verticals", _news / "verticals.py")
_checker = load("news_check_article", _news / "check_article.py")
block_kind, block_text = _verticals.block_kind, _verticals.block_text
SIMPLIFIED, NUMBER = _checker.SIMPLIFIED, _checker.NUMBER
SUMMARY_ITEMS, FAQ_ITEMS = _checker.SUMMARY_ITEMS, _checker.FAQ_ITEMS
body_without_summary, cjk_units = _checker.body_without_summary, _checker.cjk_units
HUBS = {slug for slug, _ in LIFE_SEED_TOPICS}
PARENT = {slug: parent for slug, parent, _ in LIFE_SEED_SUBTOPICS}

BODY_RANGE = (1800, 3000)
HUB_BODY_RANGE = (900, 3000)
SOURCES_RANGE = (3, 8)
CODE_LANGUAGES = {"python", "bash", "json", "yaml"}
CODE_MAX_LINES = 80
SECRET = re.compile(r"sk-[A-Za-z0-9_-]{8,}|AKIA[0-9A-Z]{16}|api[_-]?key\s*[=:]\s*[\"'][^\"'$<{]{12,}", re.I)
PLACEHOLDER = re.compile(r"<YOUR[_ -]?[A-Z_ ]*KEY>|YOUR_API_KEY|your-api-key-here", re.I)
BASH = Path(r"C:\Program Files\Git\bin\bash.exe")


def models_seen() -> set[str]:
    path = WORKSPACE / "models-seen.json"
    if not path.is_file():
        return set()
    # An OpenRouter id is "vendor/model"; the regex below finds the model half in prose, so a
    # recorded "openai/gpt-5.6-luna" also vouches for "gpt-5.6-luna" as written in a sentence.
    ids = {entry["id"] for entry in json.loads(path.read_text(encoding="utf-8"))["models"]}
    return ids | {i.rsplit("/", 1)[-1] for i in ids}


def model_ids_in(text: str) -> set[str]:
    """Strings shaped like a model id: a vendor prefix, a version, optional suffixes."""
    return set(re.findall(r"\b(?:gpt|claude|gemini|o[1-9]|qwen|deepseek|llama|mistral|grok)[-_a-z0-9.]{2,}\b", text, re.I))


def compile_sample(slug: str, index: int, block: CodeBlock) -> str | None:
    """None when the sample parses, otherwise the first line of the compiler's complaint."""
    samples = WORKSPACE / "renders" / "samples"
    samples.mkdir(parents=True, exist_ok=True)
    text = block.code.replace("\r\n", "\n")
    try:
        if block.language == "python":
            path = samples / f"{slug}-{index}.py"
            path.write_text(text + "\n", encoding="utf-8")
            py_compile.compile(str(path), doraise=True)
        elif block.language in ("bash", "sh", "shell"):
            path = samples / f"{slug}-{index}.sh"
            path.write_text(text + "\n", encoding="utf-8", newline="\n")
            if BASH.is_file():
                run = subprocess.run([str(BASH), "-n", str(path)], capture_output=True, text=True, timeout=60)
                if run.returncode:
                    return (run.stderr or run.stdout).strip().splitlines()[0]
        elif block.language == "json":
            json.loads(text)
        elif block.language == "yaml":
            import yaml  # noqa: PLC0415

            yaml.safe_load(text)
    except Exception as exc:  # noqa: BLE001
        return str(exc).strip().splitlines()[0] if str(exc).strip() else exc.__class__.__name__
    return None


def main() -> int:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    assets = "--assets" in sys.argv
    if len(args) != 1 or args[0] not in (*SLUGS, HUB):
        print("usage: check_article.py <slug> [--assets]")
        print("slug one of:", HUB, *SLUGS)
        return 2
    slug = args[0]
    is_hub = slug == HUB
    fails: list[str] = []
    warns: list[str] = []

    def need(ok: bool, message: str) -> None:
        if not ok:
            fails.append(message)

    pack_path = CONTENT / f"{slug}.json"
    if not pack_path.is_file():
        print(f"FAIL\n - {pack_path.name} does not exist yet (the writer saves the pack first)")
        return 1
    raw = json.loads(pack_path.read_text(encoding="utf-8"))
    try:
        pack = ArticlePack.model_validate(raw)
    except ValueError as error:
        print("FAIL\n -", str(error).replace("\n", "\n   "))
        return 1
    research_path = RESEARCH / f"{slug}.json"
    if not research_path.is_file():
        print(f"FAIL\n - no research record at {research_path.relative_to(ROOT)}")
        return 1
    research = json.loads(research_path.read_text(encoding="utf-8"))
    checked = str(research.get("checked_on", ""))
    need(re.fullmatch(r"\d{4}-\d{2}-\d{2}", checked) is not None, "research checked_on must be YYYY-MM-DD")

    # --- the pack ------------------------------------------------------------------------
    need(pack.kind == "life", "kind must be life")
    need(pack.destination_id is None, "destination_id must be null")
    need(tuple(pack.topics) == TOPICS, f"topics must be exactly {list(TOPICS)}")
    for topic in pack.topics:
        if topic in PARENT:
            need(PARENT[topic] in pack.topics, f"topic {topic} needs its parent {PARENT[topic]}")
        else:
            need(topic in HUBS, f"unknown topic {topic}")
    need(pack.display_order == order_of(slug), f"display_order must be {order_of(slug)}")
    need(pack.news_date is None, "news_date must be null: this is not a dated news item")
    need(list(pack.locales) == [LOCALE], f"locales must be exactly [{LOCALE}]")
    need(not pack.related or len(pack.related) <= 4, "related carries at most 4 slugs")
    for related in pack.related or []:
        need((CONTENT / f"{related}.json").is_file(), f"related {related} does not exist")

    doc: GuideDocument = pack.locales[LOCALE]
    blocks = raw["locales"][LOCALE]["blocks"]
    kinds = [block_kind(b) for b in blocks]
    need(cjk_units(doc.title) <= 60, f"title is {cjk_units(doc.title):.0f} units, max 60")
    need(120 <= cjk_units(doc.description) <= 200, f"description is {cjk_units(doc.description):.0f} units, not 120-200")
    need(research.get("title") == doc.title, "research title differs from zh-TW title")
    for where, text in (("title", doc.title), ("description", doc.description), ("body", "".join(block_text(b) for b in blocks))):
        hit = SIMPLIFIED.search(text)
        need(hit is None, f"simplified character '{hit.group(0) if hit else ''}' in {where}")

    # Skeleton: two opening paragraphs, then the summary, then the sections.
    need(kinds[:3] == ["paragraph", "paragraph", "summary"], "the article must open with two paragraphs and then the summary")
    need(kinds.count("summary") == 1, "exactly one summary block")
    h2 = [b for b in blocks if b["type"] == "heading" and b.get("level") == 2]
    need(3 <= len(h2) <= 6, f"{len(h2)} h2 sections, not 3-6")
    need(kinds.count("table") >= 1, "at least one table")
    need(kinds.count("callout") == 1, f"exactly one callout, found {kinds.count('callout')}")
    need(kinds.count("image") == 1, f"exactly one diagram image, found {kinds.count('image')}")
    faq = [b for b in blocks if b["type"] == "faq"]
    if is_hub:
        need(not faq or 2 <= len(faq[0]["items"]) <= FAQ_ITEMS[1], "hub faq, if any, has 2-10 items")
    else:
        need(len(faq) == 1 and 3 <= len(faq[0]["items"]) <= 8, "exactly one faq block with 3-8 items")
    for item in (faq[0]["items"] if faq else []):
        need("http" not in item["answer"], "faq answers must not carry URLs")
    links = [b for b in blocks if b["type"] == "link"]
    inline_articles = [n for b in blocks if b["type"] == "rich_paragraph" for n in b["inlines"] if n["type"] == "article"]
    if is_hub:
        need(not links, "the hub links its articles inline (rich_paragraph article), not as link blocks")
        linked = {n["slug"] for n in inline_articles}
        need(set(SLUGS) <= linked, f"hub must link every article; missing {sorted(set(SLUGS) - linked)}")
    else:
        # Before ``pack_cli relink`` the ending is two link blocks; after it, two rich paragraphs
        # each carrying one article inline. Either shape is the same two links.
        ending = kinds[-2:] == ["link", "link"] or (
            [b["type"] for b in blocks[-2:]] == ["rich_paragraph", "rich_paragraph"]
            and all(any(n["type"] == "article" for n in b["inlines"]) for b in blocks[-2:])
        )
        need(ending, "the article ends with two link blocks (hub first, then the assigned article)")
        if links:
            first = links[0]
            need(first["url"].endswith(f"/life/{HUB}"), "first closing link must point at the hub")
            need(first["text"] == HUB_TITLE, f"first closing link text must be the hub title {HUB_TITLE!r}")
            if len(links) > 1:
                target = links[1]["url"].rsplit("/", 1)[-1]
                target_path = CONTENT / f"{target}.json"
                need(target_path.is_file(), f"link target {target}.json does not exist")
                if target_path.is_file():
                    title = json.loads(target_path.read_text(encoding="utf-8"))["locales"][LOCALE]["title"]
                    need(links[1]["text"] == title, f"link text must be the title of {target}")
            body_links = [b for b in blocks[:-2] if b["type"] == "link"]
            need(not body_links, "no link blocks in the body; only the two closing ones")
    for link in links:
        need("?" not in link["url"], f"link carries a query string: {link['url']}")

    # Body length in CJK units, without the summary, the code, the table and the FAQ.
    prose = "".join(block_text(b) for b in blocks if block_kind(b) == "paragraph")
    low, high = HUB_BODY_RANGE if is_hub else BODY_RANGE
    units = cjk_units(prose)
    need(low <= units <= high, f"paragraph characters {units:.0f} not in {low}-{high}")

    # Summary ⊆ body: every number the summary states must appear outside it.
    summary = next(b for b in blocks if b["type"] == "summary")
    body = body_without_summary(doc)
    for item in summary["items"]:
        need(SUMMARY_ITEMS[0] <= len(summary["items"]) <= SUMMARY_ITEMS[1], "summary item count off the schema bounds")
        for number in NUMBER.findall(item.replace(",", "")):
            need(number in body, f"summary states {number} which the body does not")

    # --- sources -------------------------------------------------------------------------
    sources = raw["locales"][LOCALE]["sources"]
    need(SOURCES_RANGE[0] <= len(sources) <= SOURCES_RANGE[1], f"{len(sources)} sources, not {SOURCES_RANGE[0]}-{SOURCES_RANGE[1]}")
    for source in sources:
        need(source.get("checked_on") == checked, f"source checked_on {source.get('checked_on')} differs from research {checked}")
        need("?" not in source["url"] or "api." in source["url"], f"source URL carries a query string: {source['url']}")
    need([s["url"] for s in sources] == [s["url"] for s in research.get("sources", [])], "research sources differ from the pack's (url order)")
    facts = research.get("verified_facts") or []
    need(bool(facts), "research verified_facts is empty")
    urls = {s["url"] for s in sources}
    for fact in facts:
        need(fact.get("url") in urls, f"a verified fact cites {fact.get('url')} which is not in sources")
        quote = fact.get("verbatim_quote") or ""
        need(bool(quote) and "..." not in quote and "…" not in quote, "verbatim_quote must be a continuous string, not spliced")
    need(bool(research.get("unverified_or_excluded")), "research unverified_or_excluded must not be empty")

    # --- code samples --------------------------------------------------------------------
    codes = [b for b in doc.blocks if isinstance(b, CodeBlock)]
    if slug not in INTRO and not is_hub:
        need(len(codes) >= 2, f"a technical article carries at least two code blocks, found {len(codes)}")
    seen = models_seen()
    for index, block in enumerate(codes, 1):
        need(block.language in CODE_LANGUAGES, f"code block {index}: language {block.language} not in {sorted(CODE_LANGUAGES)}")
        lines = block.code.count("\n") + 1
        need(lines <= CODE_MAX_LINES, f"code block {index}: {lines} lines, max {CODE_MAX_LINES}")
        need(SECRET.search(block.code) is None, f"code block {index}: looks like a hard-coded secret")
        need(PLACEHOLDER.search(block.code) is None, f"code block {index}: key placeholder; read keys from the environment instead")
        need("rm -rf" not in block.code and "eval(" not in block.code, f"code block {index}: destructive or eval call")
        problem = compile_sample(slug, index, block)
        need(problem is None, f"code block {index} ({block.language}) does not parse: {problem}")
        for model in model_ids_in(block.code):
            need(model in seen, f"code block {index} names model {model!r} which models-seen.json has not recorded")
    labels = {c.label for c in codes}
    for sample in research.get("code_samples") or []:
        need(sample.get("label") in labels, f"research code_samples label {sample.get('label')!r} is not a code block label")
    for model in model_ids_in(prose):
        if model.lower() not in {m.lower() for m in seen}:
            warns.append(f"prose names model {model!r} which models-seen.json has not recorded")

    # --- lint, hero, diagram text --------------------------------------------------------
    problems = lint_document(doc, "life", topics=pack.topics)
    bad = errors(problems)
    need(not bad, "lint errors: " + "; ".join(f"{p.code}: {p.message}" for p in bad))
    for p in problems:
        if p not in bad:
            warns.append(f"lint {p.code}: {p.message}")
    need(doc.hero.src == f"/guides/{slug}/hero.jpg", "hero src must be /guides/<slug>/hero.jpg")
    image = next(b for b in doc.blocks if getattr(b, "type", "") == "image")
    need(image.src == f"/guides/{slug}/diagram-1.svg", "diagram src must be /guides/<slug>/diagram-1.svg")
    diagram = research.get("diagram") or {}
    need(diagram.get("caption") == image.caption, "research diagram caption differs from the image caption")
    need(diagram.get("layout") in ("flow", "grid"), "research diagram layout must be flow or grid")
    nodes = diagram.get("nodes") or []
    need(3 <= len(nodes) <= 5, f"diagram nodes {len(nodes)}, not 3-5")
    for heading, detail in nodes:
        for number in NUMBER.findall(f"{heading} {detail}".replace(",", "")):
            need(number in body, f"diagram states {number} which the body does not")
    label = research.get("hero_label") or ""
    need(0 < cjk_units(label) <= 12, f"hero_label {label!r} must be 1-12 characters")

    if assets:
        hero = PUBLIC / slug / "hero.jpg"
        need(hero.is_file(), "hero.jpg not built")
        if hero.is_file():
            from PIL import Image  # noqa: PLC0415

            with Image.open(hero) as picture:
                need(picture.size == HERO_SIZE, f"hero is {picture.size}, not {HERO_SIZE}")
            size = hero.stat().st_size
            need(size <= IMAGE_HARD_CAP, f"hero is {size} bytes, over the {IMAGE_HARD_CAP} hard cap")
            if size > HERO_MAX_BYTES:
                warns.append(f"hero is {size} bytes, over the {HERO_MAX_BYTES} guideline")
        svg = PUBLIC / slug / "diagram-1.svg"
        need(svg.is_file(), "diagram-1.svg not built")
        if svg.is_file():
            text = svg.read_text(encoding="utf-8")
            svg_problems = errors(check_svg(text))
            need(not svg_problems, "svg: " + "; ".join(f"{p.code}: {p.message}" for p in svg_problems))
            missing = missing_diagram_numbers(text, doc)
            need(not missing, f"diagram numbers not in the body: {missing}")

    if fails:
        print("FAIL")
        for f in fails:
            print(" -", f)
        return 1
    for w in warns:
        print("WARN -", w)
    print(f"OK {slug} paragraphs {units:.0f} code_blocks {len(codes)} sources {len(sources)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
