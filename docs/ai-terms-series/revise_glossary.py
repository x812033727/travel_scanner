"""Apply the reviewed 50-term refresh without changing its URL or artwork."""
import json
from pathlib import Path

here = Path(__file__).resolve().parent
root = here.parents[1]
path = root / "apps/api/app/guides/content/ai-glossary-50-terms.json"
pack = json.loads(path.read_text(encoding="utf-8"))
data = json.loads((here / "glossary-revision-data.json").read_text(encoding="utf-8"))
doc = pack["locales"]["zh-TW"]
pack["topics"] = ["ai", "tutorial"]
doc["description"] = "把常見的 50 個 AI 名詞整理成可收藏的速查表，分為模型與訓練、使用與功能、推理與代理、生成與媒體、基礎設施與費用五組。每個詞附英文與白話定義，另以十組比較釐清上下文、記憶、開源、推理、搜尋和內容憑證的差異。本次依官方文件於 2026 年 9 月 14 日重新查核，並連到 81 詞專文總索引，方便從簡短解釋繼續深入閱讀。"
lists = [b for b in doc["blocks"] if b["type"] == "list"]
assert [len(b["items"]) for b in lists] == [15, 10, 8, 6, 11]
for block, items in zip(lists, data["groups"], strict=True):
    block["items"] = items
paragraphs = [b for b in doc["blocks"] if b["type"] == "paragraph"]
paragraphs[0]["text"] = "token、RAG、MCP、代理、開放權重，讀 AI 工具的說明時常會遇到這些名字。本篇保留原有 50 詞速查架構，於 2026 年 9 月 14 日重新查核定義，說明一般概念與容易誤解之處；產品功能只作示例，實際設定、供應範圍和費率應回到當期官方文件核對。這是本次整理範圍，不宣稱涵蓋所有新詞。"
paragraphs[4]["text"] = "不同聊天工具會用不同名稱呈現相近能力。這一組介紹功能的共同用途，實際資料共享、權限、保存期限與可用方案仍以該產品說明為準。"
paragraphs[6]["text"] = "文字以外的生成涉及不同資料型態，也帶來聲音授權與內容來源的問題。生成方法、生成任務，以及事後的標記與查驗應分開理解。"
table = next(b for b in doc["blocks"] if b["type"] == "table")
table["rows"] = data["rows"]
table["caption"] = "十組常混淆的概念，查核日期：2026 年 9 月 14 日。"
callout = next(b for b in doc["blocks"] if b["type"] == "callout")
callout.update(title="先分清楚概念，再查產品設定", text="相同名稱在不同工具中可能有不同範圍。需要決定是否上傳資料、開啟記憶或支付費用時，請查看該服務當期的官方說明。本文的速查定義可用來理解問題；若要看原理、情境和限制，請從 AI 名詞總索引進入各詞專文。")
index_url = "https://mokaair.com/zh-TW/life/ai-terms-index"
doc["blocks"] = [b for b in doc["blocks"] if not (b["type"] == "link" and b["url"] == index_url)]
doc["blocks"].insert(2, {"type": "link", "text": "AI 名詞總索引：從 Loop Engineering 到生成式 AI", "url": index_url})
doc["sources"] = data["sources"]
path.write_text(json.dumps(pack, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("Refreshed 50 definitions, 10 comparisons and index link; retained slug and artwork.")
