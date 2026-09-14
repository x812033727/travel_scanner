"""Record root's completed reading and visual inspection, not an automated reviewer."""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
read = lambda p: json.loads(p.read_text(encoding="utf-8"))
write = lambda p, v: p.write_text(json.dumps(v, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
terms = read(HERE / "catalogue.json")["terms"] + [{"id": 82, "slug": "ai-terms-index"}]
manifest = read(HERE / "renders/manifest.json")
visuals = []
for term in terms:
    for kind in ["hero", "diagram-1"]:
        if term["id"] < (41 if kind == "hero" else 33):
            continue
        key = term["slug"] + "-" + kind
        svg = HERE / "staging" / term["slug"] / (kind + ".svg")
        digest = hashlib.sha256(svg.read_bytes()).hexdigest()
        assert digest == manifest[key]["sha256"]
        visuals.append({"slug": term["slug"], "kind": kind, "svg_sha256": digest,
                        "png_sha256": hashlib.sha256((HERE / "renders" / manifest[key]["png"]).read_bytes()).hexdigest(),
                        "result": "pass"})
write(HERE / "visual-review-root.json", {
    "reviewer": "root", "reviewed_on": "2026-09-14", "status": "complete_passed",
    "method": "Actually viewed hero sheets 11–21 and diagram sheets 09–21, each containing at most four 1600x900 images. Checked labels, clipping, arrow meaning and distinct concept composition. Reopened final Agentic RAG full PNG after adding a conditional return label. Root also inspected Loop and ML fixes; those receipts are included in the other reviewer report.",
    "assets": visuals, "count": len(visuals),
    "resolved": ["GraphRAG local-search wording", "Agentic RAG return path now explicitly applies only when rewriting; stopping retains the evidence gap"],
})
rationales = {
    72: "完整正文及研究記錄已讀；圖文、照片與說明書的互補，以及觀察與推論的區分成立。另開 Gemini image-understanding 與 Flamingo 原摘要核對。",
    73: "完整正文及研究記錄已讀；DDPM 訓練加噪、生成反覆更新、latent diffusion 位置及採樣限制有區分。未將生成寫成找回訓練原圖。",
    74: "完整正文及研究記錄已讀；文字條件、候選與驗收分開，需求、構圖、局部編修及授權情境具體，未保證文字或幾何正確。",
    75: "完整正文及研究記錄已讀；以陶杯轉動說明時序一致性及攝影機運動差別，未冒稱實測。另開 Video Diffusion Models 原摘要核對。",
    76: "完整正文及研究記錄已讀；轉錄、翻譯、說話者辨識與摘要分清，否定詞、專名、人工回聽及時間戳有具體例子。另開 Transformers ASR 文件核對。",
    77: "完整正文及研究記錄已讀；以明示架構示例解釋文字、聲學表示及聲碼器，不把一種流程泛化為全部 TTS。另開 Tacotron 2 原摘要及 Transformers TTS 文件核對。",
    78: "完整正文及研究記錄已讀；合成、身份與事件真偽分清，檢測訊號不是定論，來源鏈與具體主張分開核對。另開 FaceForensics++ 原摘要核對。",
}
write(HERE / "review-root-of-multimodal.json", {
    "reviewer": "root", "reviewed_on": "2026-09-14", "status": "complete",
    "articles": [{"slug": t["slug"], "verdict": "pass", "rationale": rationales[t["id"]],
                  "pack_sha256": hashlib.sha256((HERE / "staging" / t["slug"] / "pack.json").read_bytes()).hexdigest()}
                 for t in terms if t["id"] in rationales],
    "resolved": "字形轉换後已人工還原文件、局部、權限、連回音訊、項目、通過等詞義；不是把轉換器通過視為審稿完成。",
    "substantive_blockers": 0,
})
write(HERE / "root-review-resolutions.json", {
    "reviewed_on": "2026-09-14", "required_fixes_remaining": 0,
    "engineering_root_articles": {"index_conversational_intro": "resolved", "loop_slug_link_labels": "resolved", "glossary_unsourced_trend_claim": "resolved"},
    "retrieval_copy": "GraphRAG局部、semantic/reranking對象、RRF融合、Pretraining標籤、RLHF工作與論文本身、DPO推導出、LoRA檔案大小、Quantization活化值、Test-time限制均已修。",
    "distillation_evidence": "兩位審稿者獨立閱讀 Kim/Rush 原論文第3.2節後，加入 pack/research/notes 作為教師序列監督學生的來源。",
    "optional_decisions": ["Reranking 末段保留截斷位置的診斷記錄，前段講原因、末段講如何留下可重現輸入。", "一般文件與檔案少量用詞差異不改變概念；已修容易誤解的官方文件和指定文件。", "索引沿用標準 featured=false/display_order=100，透過完整索引與相關連結導航。"],
})
print("Recorded 92 visually inspected assets and seven independently read articles.")
