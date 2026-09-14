"""Run only after writers have handed off; records final decisions and link labels."""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
def read(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))
def write(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

catalogue = read(HERE / "catalogue.json")
aliases = read(HERE / "aliases.json")
overlaps = {
    "prompt-engineering": ["ai-chat-prompt-basics"],
    "model-context-protocol": ["claude-mcp-explained", "claude-code-mcp-servers", "mcp-servers-for-everyone"],
    "agent-memory": ["chatgpt-custom-instructions-memory", "claude-memory-and-privacy"],
    "vibe-coding": ["vibe-coding-first-website"],
    "retrieval-augmented-generation": ["local-rag-chat-with-your-documents"],
    "quantization": ["gguf-quantization-explained"],
    "text-to-image": ["chatgpt-image-generation-guide", "nano-banana-image-editing"],
    "text-to-speech": ["minimax-speech-tts-guide"],
    "open-weights": ["ai-open-vs-closed-models"],
    "open-source-ai": ["ai-open-vs-closed-models"],
}
titles = {p.stem: read(p)["locales"].get("zh-TW", {}).get("title") for p in (ROOT / "apps/api/app/guides/content").glob("*.json")}
packs = {}
for term in catalogue["terms"]:
    slug = term["slug"]
    folder = HERE / "staging" / slug
    pack, research = read(folder / "pack.json"), read(folder / "research.json")
    assert research["status"] == "verified"
    key = slug.removeprefix("ai-term-")
    existing = [slug] if term["action"] != "new" else overlaps.get(key, [])
    term.update(title=pack["locales"]["zh-TW"]["title"],
                aliases=sorted(set(aliases.get(key, []) + research.get("aliases", []))),
                sources=research["sources"], checked_on=research["checked_on"],
                status="verified", existing_articles=existing,
                decision_reason=("保留既有網址，重新查核並補足獨立概念、案例、比較與限制。" if term["action"] != "new" else
                                 "收錄獨立概念及可核對的一手資料；相近既有／規劃文章偏向特定工具操作，本篇解釋通用概念。" if existing else
                                 "收錄獨立概念及具體使用情境，清單中尚無同義專文。"))
    titles[slug] = term["title"]
    packs[slug] = pack
packs["ai-terms-index"] = read(HERE / "staging/ai-terms-index/pack.json")
titles["ai-terms-index"] = packs["ai-terms-index"]["locales"]["zh-TW"]["title"]
for slug, pack in packs.items():
    for b in pack["locales"]["zh-TW"]["blocks"]:
        if b["type"] == "link" and b["url"].startswith("https://mokaair.com/zh-TW/life/"):
            target = b["url"].rstrip("/").rsplit("/", 1)[-1]
            assert titles.get(target), (slug, target)
            b["text"] = titles[target]
    write(HERE / "staging" / slug / "pack.json", pack)
glossary_path = ROOT / "apps/api/app/guides/content/ai-glossary-50-terms.json"
glossary = read(glossary_path)
for b in glossary["locales"]["zh-TW"]["blocks"]:
    if b["type"] == "link":
        target = b["url"].rsplit("/", 1)[-1]
        if titles.get(target):
            b["text"] = titles[target]
write(glossary_path, glossary)
catalogue["counts"] = {"candidate_concepts": 81, "accepted_concepts": 81, "new_concept_articles": 76, "revised_concept_articles": 5, "new_indexes": 1, "revised_quick_references": 1, "excluded_concepts": 0}
catalogue["deduplication"] = "縮寫、拼字變體與中文別名歸入同一詞條，不各自建立文章。C2PA 是支援內容憑證的標準，並非與內容憑證完全同義。"
catalogue["scope_statement"] = "首輪截至 2026-09-14，共查核並收錄 81 個獨立概念；不宣稱涵蓋所有 AI 用語。"
write(HERE / "catalogue.json", catalogue)
lines = ["# AI 名詞系列編輯清單", "", "搜尋截止：2026-09-14。81 個獨立概念全部收錄；76 篇新增、5 篇保留網址補強，另新增總索引及更新 50 詞速查。別名合併於各詞，不重複計篇。", "", "| 分類 | 名稱 | 最終標題 | 處理 | 網址 |", "| --- | --- | --- | --- | --- |"]
for t in catalogue["terms"]:
    lines.append(f'| {t["category"]} | {t["chinese"]} / {t["english"]} | {t["title"]} | {"新增" if t["action"] == "new" else "補強"} | [閱讀](https://mokaair.com/zh-TW/life/{t["slug"]}) |')
lines += ["", "此清單的閱讀網址為預定永久網址；是否已公開以 publication.json 與公開驗證紀錄為準。", "", "來源、別名、既有文章對應及個別理由見 catalogue.json。既有 220 篇 AI 教學規劃偏向工具與情境；本批以通用概念為主。進行中的 Claude／Codex／Gemini 教學與近期 AI 新聞使用不同 slug。"]
(HERE / "ARTICLES.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
print("Finalized 81 concepts, index and quick-reference cross-links.")
