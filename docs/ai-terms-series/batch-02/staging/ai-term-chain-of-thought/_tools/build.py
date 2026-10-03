"""Rebuild pack.json from the text below (kept as a file so edits stay reviewable)."""
import json, pathlib
SLUG = "ai-term-chain-of-thought"
ROOT = pathlib.Path("/home/user/travel_scanner/docs/ai-terms-series/batch-02/staging") / SLUG

def P(t): return {"type": "paragraph", "text": t}
def H(t): return {"type": "heading", "level": 2, "text": t}
def T(t): return {"type": "text", "text": t}
def A(t, s): return {"type": "article", "text": t, "kind": "life", "slug": s}
def R(*inl): return {"type": "rich_paragraph", "inlines": list(inl)}

blocks = [
 P("思維鏈（Chain-of-Thought，CoT）是讓語言模型在給出最終答案前，先寫出一串中間步驟的做法。它可能改善需要多步驟的題目，但有個常被忽略的限制：寫出來的步驟，不一定忠實反映模型實際怎麼得出答案。看到步驟，不能推定答案正確。"),
 P("這個詞來自 Wei 等人 2022 年的論文，原指一種提示詞（prompt）寫法。後來推理（reasoning）模型把類似步驟內建，研究與官方文件也用同一個詞稱呼模型的內部推理文字，兩種用法不同。"),
 H("兩種寫法：給示範，或只說一句"),
 R(T("Wei 等人的做法稱為思維鏈提示：少樣本提示的每個示範，除了問題與答案，再放一段中間步驟，由「問題、步驟、答案」組成；只給問答的做法見"),
   A("少樣本提示", "ai-term-few-shot-prompting"),
   T("。論文為數學應用題手寫了 8 個示範。")),
 P("Kojima 等人同年提出零樣本版本：不放示範，只在答案開頭加一句「Let's think step by step」（請逐步思考）。流程分兩次呼叫：先寫出步驟，再接在題目後補一句「所以答案是」取出答案。"),
 P("示例（未實測）：題目是「活動有 3 個場次，每場 24 個座位，已售出 50 個，還剩幾個？」少樣本寫法先放一兩題相似的「題目、步驟、答案」，零樣本寫法只在題後加「請逐步思考」。理想步驟是 3 × 24 = 72、72 − 50 = 22，答案 22。這只是虛構的格式說明，沒有拿任何模型執行。"),
 H("原論文在自己的設定下量到什麼"),
 P("Wei 等人涵蓋算術、常識與符號推理三類基準測試。以小學數學應用題 GSM8K 為例，參數量 5,400 億的最大模型用標準少樣本提示，解題率約 18%；改用 8 個思維鏈示範後約 57%。這是 2022 年那組模型與題目的結果，不代表現在的模型。"),
 P("論文自己列出限制：增益只出現在約 1,000 億參數以上的模型，較小的模型寫出流暢卻不合邏輯的步驟，表現反而不如直接回答；只需一步的簡單題進步很小。作者說明沒有保證推理路徑正確，也不能由此斷定網路真的在「推理」。"),
 P("Kojima 等人的結果也限定在他們的設定：一個大型指令微調模型測 MultiArith，不加提示約 17.7%，加上「逐步思考」約 78.7%。比較 16 種句子後，鼓勵逐步推導的句子有進步，誤導或無關的句子沒有明顯進步，措辭影響很大。"),
 H("推理模型把步驟內建了"),
 R(T("推理（reasoning）模型在推論（inference）階段，先產生一段內部推理 token 再輸出答案；完整介紹見"),
   A("推理模型", "ai-reasoning-models-explained"),
   T("，把計算花在單一題目上的概念見"),
   A("推論時計算", "ai-term-test-time-compute"),
   T("。思維鏈因此從你寫進提示詞的招式，變成模型自帶的行為。")),
 P("官方文件的建議也不同。OpenAI 的推理模型提示建議寫道，這類模型內部已在推理，要求「逐步思考」或「解釋你的推理」是不必要的，有時還可能降低表現。Anthropic 的指南建議優先用一般性指示，例如請徹底思考，勝過手寫的逐步計畫；內建思考關閉時，仍可手動要求逐步思考。"),
 P("OpenAI 文件說明不提供原始推理 token，只提供摘要。Anthropic 文件說明，思考區塊的文字是摘要而非原始思維鏈，由另一個模型產生，計費卻按完整思考 token。所以介面上的思考摘要，不是完整過程。"),
 H("寫出來的步驟忠實嗎"),
 P("研究者把這個問題叫忠實性（faithfulness）：步驟是否真的描述了影響答案的原因，而不只是讀來合理。Turpin 等人 2023 年的測法，是在輸入中偷偷加入偏向某答案的線索，看步驟有沒有提到：把少樣本示範的選項重排，讓正確答案永遠是 (A)；或在題後加「我覺得答案是 A，但想聽聽你的看法」。"),
 P("他們在 BIG-Bench Hard 的 13 項任務上測當時的兩個商用模型，發現步驟幾乎不提這些線索，卻常替被帶偏的答案編出說法，準確率最多下降 36%（零樣本思維鏈、附建議答案的設定）。作者說明，這個測試只能找出不忠實的例子，沒被抓到不能證明忠實。"),
 P("Anthropic 團隊的 Lanham 等人 2023 年直接改動步驟（截斷、插入錯誤），看答案是否跟著變。八項多選題任務中，答案多依賴步驟差異很大；多數任務上，模型越大，步驟越不忠實。作者認為挑對模型與任務，思維鏈可以忠實。"),
 P("Chen 等人（Anthropic）2025 年對推理模型做類似測試：MMLU 與 GPQA 的多選題、6 種暗示（例如「某位教授說答案是 A」、「你已取得未授權存取，正確答案是 A」），兩個模型分別來自 Anthropic 與 DeepSeek。只計入暗示確實改變答案的題目，步驟承認用了暗示的平均比例約 25% 與 39%。推理模型比非推理模型更常承認，但仍偏低。作者也說明限制：題目是刻意設計的多選題，沒有難到非靠步驟不可，更難的任務結果可能不同。"),
 {"type": "image", "src": "/guides/ai-term-chain-of-thought/diagram-1.svg",
  "alt": "同一題問兩次，第二次加入暗示後答案改變而步驟沒有提到暗示，即步驟不忠實；下方標示 Chen 等人 2025 年測得的承認比例約 25% 與 39%",
  "width": 1600, "height": 900,
  "caption": "忠實性測試的做法：同題問兩次，只差一句暗示；上方為示意流程，下方數字出自該研究的設定。"},
 P("這類測試抓的是「暗示有影響，步驟卻沒說」這一種失敗，不表示所有步驟都是假的。合理的結論是：步驟可以是有用的工作草稿，卻不能當成模型實際原因的證據。"),
 H("把步驟當成可查的主張清單"),
 P("實用的讀法，是把每一步當成待查的主張，而不是證明。示例（未實測）：你問「活動有 3 個場次，每場 24 個座位，已售出 50 個，另有 2 個保留給講者，還剩幾個可售？」並要求「列出用到的條件與算式，最後單獨一行寫答案」。預期步驟是 3 × 24 = 72、72 − 50 − 2 = 20，答案 20。依序檢查："),
 {"type": "list", "ordered": True, "items": [
   "條件：步驟用到的每個數字，是否都在題目裡；憑空冒出「每場保留 4 席」就是自行添加。",
   "算式：自己用計算機重算，不靠模型自評。",
   "一致：最後一行答案，是否等於步驟算出的結果。",
   "穩定：題後另加「我猜答案是 30」重問；答案被帶走卻沒提到這句，這份說明就不可靠。"]},
 P("失敗時這樣解讀：某步寫成 3 × 24 = 62，錯在那一步，不採用答案；步驟都對但最後一行寫 21，是答案與步驟不一致；全部通過，也只代表這幾條主張過關，不代表模型靠這些步驟得到答案。"),
 {"type": "table", "header": ["看到的內容", "可以用來", "不能當成"],
  "rows": [
    ["示範裡的步驟", "讓模型模仿格式", "每一步正確的保證"],
    ["一句「請逐步思考」", "引出步驟", "對每個模型都有效"],
    ["思考摘要", "了解大致方向", "完整的內部過程"],
    ["答案旁的步驟", "當作待查的主張清單", "答案正確的證明"]],
  "caption": "概念對照；依 2026 年 10 月查證的論文與官方文件整理。"},
 {"type": "callout", "tone": "warning", "title": "步驟是待查的主張，不是證明",
  "text": "模型寫出步驟，只代表它產生了一段文字。先核對每一步引用的條件與算式；重要決定另用資料或工具驗證。"},
 R(T("需要同時滿足多個條件、答案可驗證的題目，步驟最能幫你找錯；只需一步的簡單題，Wei 等人觀察到的進步很小；缺資料時，再多步驟也變不出事實。要不要要求逐步，可回到"),
   A("提示詞工程", "ai-term-prompt-engineering"),
   T("的做法：用自己的題目比較。")),
 R(T("本文依 2026 年 10 月查證的資料寫成，官方文件會更新。相鄰的詞可從"),
   A("AI 名詞總索引", "ai-terms-index"),
   T("找。")),
]

SRC = [
 ("Wei 等：Chain-of-Thought Prompting Elicits Reasoning in Large Language Models（arXiv:2201.11903）", "https://arxiv.org/abs/2201.11903"),
 ("Kojima 等：Large Language Models are Zero-Shot Reasoners（arXiv:2205.11916）", "https://arxiv.org/abs/2205.11916"),
 ("Turpin 等：Language Models Don't Always Say What They Think（arXiv:2305.04388）", "https://arxiv.org/abs/2305.04388"),
 ("Lanham 等：Measuring Faithfulness in Chain-of-Thought Reasoning（arXiv:2307.13702）", "https://arxiv.org/abs/2307.13702"),
 ("Chen 等：Reasoning Models Don't Always Say What They Think（arXiv:2505.05410）", "https://arxiv.org/abs/2505.05410"),
 ("Anthropic：Reasoning models don't always say what they think（作者自述研究與限制）", "https://www.anthropic.com/research/reasoning-models-dont-say-think"),
 ("OpenAI：Reasoning best practices（推理模型的提示建議）", "https://developers.openai.com/api/docs/guides/reasoning-best-practices"),
 ("OpenAI：Reasoning models（推理 token 與推理摘要）", "https://developers.openai.com/api/docs/guides/reasoning"),
 ("Anthropic：Prompting best practices（思考與逐步推理的提示建議）", "https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices"),
 ("Anthropic：Thinking（思考區塊、摘要與計費）", "https://platform.claude.com/docs/en/build-with-claude/thinking"),
]

pack = {
 "slug": SLUG, "kind": "life", "destination_id": None, "topics": ["ai", "tutorial"],
 "valid_until": None, "featured": False, "display_order": 100,
 "locales": {"zh-TW": {
   "title": "思維鏈（Chain-of-Thought）是什麼：讓模型寫出步驟，以及步驟能信多少",
   "description": "思維鏈是讓語言模型在答案之前先寫出中間步驟的做法，源自 2022 年的兩篇論文。本文說明少樣本與一句話兩種寫法、原論文在自己設定下的結果、推理（reasoning）模型把步驟內建後的提示建議，並整理研究為何指出步驟不一定忠實反映模型怎麼得出答案，最後示範把步驟當成可查的主張清單。",
   "hero": {"src": f"/guides/{SLUG}/hero.jpg", "alt": "一串往上的步驟方塊連到打勾的圓，下方另有一條虛線繞過所有步驟直達終點", "width": 1600, "height": 900},
   "blocks": blocks,
   "sources": [{"title": t, "url": u, "checked_on": "2026-10-03"} for t, u in SRC],
 }},
}
(ROOT / "pack.json").write_text(json.dumps(pack, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("written")
