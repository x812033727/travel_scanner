"""Apply the explicit, reviewed copy corrections recorded during cross-review."""
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
corrections = {
    "區域性": "局部",
    "適用物件": "適用對象",
    "兩套搜尋共同支援的是": "兩套搜尋共同提供的是",
    "RRF 用排名連線不同檢索訊號": "RRF 用排名融合不同檢索訊號",
    "意圖示籤": "意圖標籤",
    "很多工很難": "很多工作很難",
    "論文字身": "論文本身",
    "推匯出": "推導出",
    "文件尺寸較小": "檔案大小較小",
    "LoRA 文件": "LoRA 檔案",
    "啟用值": "活化值",
    "限製": "限制",
    "這組是你提到的 Loop Engineering 所在位置。": "這組收錄 Loop Engineering 等工程方法。",
    "，保留原文章網址並重新整理核心概念。": "，並區分模型能力與產品功能。",
    "有支援的答案": "有依據的答案",
    "注意力負責交換位置資訊": "注意力在不同位置之間交換資訊",
    "線性迴歸": "線性回歸",
    "可擴充套件的語意訊號": "可擴充的語意訊號",
    "單一演演算法": "單一演算法",
    "為瞭解釋攔截原因": "為了解釋攔截原因",
    "具體定義要看模型檔案": "具體定義要看模型文件",
    "用名次連線不同分數系統": "用名次融合不同搜尋結果",
    "指定檔案": "指定文件",
    "參考檔案": "參考文件",
    "檔案已過時": "文件已過時",
    "使用者提示與檔案攻擊": "使用者提示與文件攻擊",
}
for file in (HERE / "staging").rglob("*"):
    if file.is_file() and file.suffix in {".json", ".svg", ".md"}:
        original = file.read_text(encoding="utf-8-sig")
        edited = original
        for before, after in corrections.items():
            edited = edited.replace(before, after)
        if edited != original:
            file.write_text(edited, encoding="utf-8")
glossary = HERE.parents[1] / "apps/api/app/guides/content/ai-glossary-50-terms.json"
original = glossary.read_text(encoding="utf-8-sig")
before = "最近最常出現的新詞幾乎都在這組：模型不再只是回答，而是先想、再呼叫工具、再自己操作電腦。風險也集中在這組，最後兩條請一定看。"
after = "這組介紹推理、代理與工具執行，並說明權限及外部內容風險。模型提出工具操作之後，仍需要外部程式執行與驗證；授權範圍和人工確認方式也應事先定義。"
glossary.write_text(original.replace(before, after), encoding="utf-8")
diagram = HERE / "staging/ai-term-agentic-rag/diagram-1.svg"
svg = diagram.read_text(encoding="utf-8")
if "僅改寫後再查" not in svg:
    svg = svg.replace('<text x="1540"', '<text x="640" y="640" text-anchor="middle" font-size="24" fill="#5C6B6B">僅改寫後再查；停止則保留缺口</text><text x="1540"')
    diagram.write_text(svg, encoding="utf-8")
for slug, before, after in [
    ("ai-term-artificial-intelligence", 'd="M 1000 410 L 1120 410"', 'd="M 1000 410 H 1060 M 1060 285 V 555 M 1060 285 H 1120 M 1060 555 H 1120"'),
    ("ai-term-generative-ai", 'd="M 1020 420 L 1160 420"', 'd="M 1020 420 H 1080 M 1080 275 V 575 M 1080 275 H 1160 M 1080 575 H 1160"'),
    ("ai-context-window-explained", 'd="M1130 660 H1000"', 'd="M1325 370 V660 H990"'),
    ("ai-agents-explained", 'd="M960 530 H690 V460"', 'd="M1135 450 V530 H690 V460"'),
]:
    file = HERE / "staging" / slug / "diagram-1.svg"
    svg = file.read_text(encoding="utf-8").replace(before, after)
    svg = svg.replace('<circle cx="1120" cy="410" r="10" fill="#0D6B68"/>', '') if slug == "ai-term-artificial-intelligence" else svg
    svg = svg.replace('<circle cx="1160" cy="420" r="10" fill="#0D6B68"/>', '') if slug == "ai-term-generative-ai" else svg
    file.write_text(svg, encoding="utf-8")
file = HERE / "staging/ai-term-agent-loop/diagram-1.svg"
svg = file.read_text(encoding="utf-8")
if "未完成且可繼續" not in svg:
    svg = svg.replace('<text x="1540"', '<text x="410" y="465" font-size="25" fill="#5C6B6B">未完成且可繼續</text><text x="1540"')
    file.write_text(svg, encoding="utf-8")
folder = HERE / "staging/ai-term-knowledge-distillation"
source = {"title": "Kim、Rush：Sequence-Level Knowledge Distillation", "url": "https://arxiv.org/abs/1606.07947"}
for filename in ["research.json", "pack.json"]:
    file = folder / filename
    value = json.loads(file.read_text(encoding="utf-8"))
    sources = value["sources"] if filename == "research.json" else value["locales"]["zh-TW"]["sources"]
    if not any(s["url"] == source["url"] for s in sources):
        sources.append({**source, **({"access": "Two independent reviewers read HTML section 3.2 on 2026-09-14", "claims": ["教師生成的序列可作為學生的監督訓練目標；不將論文的翻譯實驗速度推廣為一般效果"]} if filename == "research.json" else {"checked_on": "2026-09-14"})})
        file.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
notes = folder / "notes.md"
text = notes.read_text(encoding="utf-8")
if source["url"] not in text:
    notes.write_text(text + "\n交叉審稿補證：教師生成序列作學生監督目標｜" + source["url"] + "｜2026-09-14｜兩位審稿者獨立讀取 HTML 第 3.2 節。\n", encoding="utf-8")
print("Applied cross-review copy corrections.")
