import json, re, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
S = "ai-term-ai-alignment"
CHECKED = "2026-10-03"

def p(text): return {"type": "paragraph", "text": text}
def h2(text): return {"type": "heading", "level": 2, "text": text}
def rich(*parts):
    inl = []
    for x in parts:
        if isinstance(x, str):
            inl.append({"type": "text", "text": x})
        else:
            slug, label = x
            inl.append({"type": "article", "text": label, "kind": "life", "slug": slug})
    return {"type": "rich_paragraph", "inlines": inl}
def ul(*items): return {"type": "list", "items": list(items), "ordered": False}
def ol(*items): return {"type": "list", "items": list(items), "ordered": True}

blocks = []
exec((ROOT / "_tools" / "sections.py").read_text(encoding="utf8"))

sources = [
    ("Leike 等人 2018：Scalable agent alignment via reward modeling（arXiv，提出 agent alignment problem）", "https://arxiv.org/abs/1811.07871"),
    ("Askell 等人 2021：A General Language Assistant as a Laboratory for Alignment（arXiv，HHH 準則）", "https://arxiv.org/abs/2112.00861"),
    ("Ouyang 等人 2022：Training language models to follow instructions with human feedback（arXiv，InstructGPT）", "https://arxiv.org/abs/2203.02155"),
    ("Bai 等人 2022：Constitutional AI: Harmlessness from AI Feedback（arXiv）", "https://arxiv.org/abs/2212.08073"),
    ("Gabriel 2020：Artificial Intelligence, Values, and Alignment（arXiv，Minds and Machines 論文）", "https://arxiv.org/abs/2001.09768"),
    ("Hadfield-Menell 等人 2016：Cooperative Inverse Reinforcement Learning（arXiv，價值對齊的形式化定義）", "https://arxiv.org/abs/1606.03137"),
    ("Krakovna 等人 2020：Specification gaming: the flip side of AI ingenuity（Google DeepMind 官方文章）", "https://deepmind.google/blog/specification-gaming-the-flip-side-of-ai-ingenuity/"),
    ("Sharma 等人 2023：Towards Understanding Sycophancy in Language Models（arXiv）", "https://arxiv.org/abs/2310.13548"),
    ("NVIDIA NeMo Guardrails Library Developer Guide：Overview（官方文件）", "https://docs.nvidia.com/nemo/guardrails/about-nemo-guardrails-library/overview"),
    ("Anthropic Usage Policy（官方使用政策頁）", "https://www.anthropic.com/legal/aup"),
    ("OpenAI Model Spec（2026/08/18 版，官方頁）", "https://model-spec.openai.com/2026-08-18.html"),
]

pack = {
    "slug": S,
    "kind": "life",
    "destination_id": None,
    "topics": ["ai", "tutorial"],
    "valid_until": None,
    "featured": False,
    "display_order": 100,
    "locales": {
        "zh-TW": {
            "title": TITLE,
            "description": DESCRIPTION,
            "hero": {"src": f"/guides/{S}/hero.jpg", "alt": "對話框旁的一支箭射向靶，箭落在偏離靶心處，一條虛線箭頭指向原本想射中的靶心", "width": 1600, "height": 900},
            "blocks": blocks,
            "sources": [{"title": t, "url": u, "checked_on": CHECKED} for t, u in sources],
        }
    },
}
(ROOT / "pack.json").write_text(json.dumps(pack, ensure_ascii=False, indent=2) + "\n", encoding="utf8")

# stats, same counting as _body_length
def body_parts(bs):
    out = []
    for b in bs:
        t = b["type"]
        if t == "paragraph": out.append(b["text"])
        elif t == "rich_paragraph": out.append("".join(i["text"] for i in b["inlines"]))
        elif t == "list": out.extend(b["items"])
        elif t == "table":
            out.extend(b["header"]);
            for r in b["rows"]: out.extend(r)
        elif t == "callout": out.extend((b["title"], b["text"]))
    return out
n = sum(len(re.sub(r"\s+", "", x)) for x in body_parts(blocks))
print("body chars:", n, "| title:", len(TITLE), "| desc:", len(DESCRIPTION))
print("h2:", sum(1 for b in blocks if b["type"]=="heading" and b["level"]==2))
