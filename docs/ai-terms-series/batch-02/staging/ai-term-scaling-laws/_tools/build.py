"""Rebuild pack.json blocks from content/*.py sections (helper only; deleted before handoff)."""
import json, re, sys, importlib.util, pathlib

root = pathlib.Path(__file__).resolve().parent
pack_path = root.parent / "pack.json"
pack = json.loads(pack_path.read_text(encoding="utf-8"))
SLUG = pack["slug"]

def P(text): return {"type": "paragraph", "text": text}
def H(text): return {"type": "heading", "level": 2, "text": text}
def RP(*parts):
    inl = []
    for p in parts:
        if isinstance(p, str):
            inl.append({"type": "text", "text": p})
        else:
            inl.append({"type": "article", "text": p[0], "kind": "life", "slug": p[1]})
    return {"type": "rich_paragraph", "inlines": inl}
def IMG(src, alt, caption): return {"type": "image", "src": src, "alt": alt, "width": 1600, "height": 900, "caption": caption}
def TABLE(header, rows, caption): return {"type": "table", "header": header, "rows": rows, "caption": caption}
def CALLOUT(tone, title, text): return {"type": "callout", "tone": tone, "title": title, "text": text}

blocks = []
for f in sorted((root / "content").glob("*.py")):
    spec = importlib.util.spec_from_file_location(f.stem, f)
    mod = importlib.util.module_from_spec(spec)
    mod.P, mod.H, mod.RP, mod.IMG, mod.TABLE, mod.CALLOUT = P, H, RP, IMG, TABLE, CALLOUT
    spec.loader.exec_module(mod)
    blocks.extend(mod.BLOCKS)

pack["locales"]["zh-TW"]["blocks"] = blocks
pack_path.write_text(json.dumps(pack, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

def body_parts(blocks):
    parts = []
    for b in blocks:
        t = b["type"]
        if t == "paragraph": parts.append(b["text"])
        elif t == "rich_paragraph": parts.append("".join(n["text"] for n in b["inlines"]))
        elif t == "list": parts.extend(b["items"])
        elif t == "table":
            parts.extend(b["header"])
            for r in b["rows"]: parts.extend(r)
        elif t == "callout": parts.extend((b["title"], b["text"]))
    return parts

total = sum(len(re.sub(r"\s+", "", p)) for p in body_parts(blocks))
links = sum(len(n["text"]) for b in blocks if b["type"] == "rich_paragraph" for n in b["inlines"] if n["type"] == "article")
print("blocks:", len(blocks), "body_length:", total, "of which article-link text:", links, "excl links:", total - links)
for b in blocks:
    if b["type"] in ("paragraph", "rich_paragraph"):
        txt = b["text"] if b["type"] == "paragraph" else "".join(n["text"] for n in b["inlines"])
        print(" -", len(re.sub(r"\s+", "", txt)), txt[:24])
    elif b["type"] == "heading":
        print("##", b["text"])
