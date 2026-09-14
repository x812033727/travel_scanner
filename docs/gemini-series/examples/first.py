import os
from google import genai

model = os.environ.get("GEMINI_MODEL", "gemini-3.8-flash")
with genai.Client(api_key=os.environ["GEMINI_API_KEY"]) as client:
    reply = client.interactions.create(
        model=model,
        input="請用繁體中文列出整理活動公告時應核對的三個欄位。",
        store=False,
    )
    if reply.status != "completed" or not reply.output_text:
        raise RuntimeError("回覆尚未完成或沒有文字，請檢查回傳狀態。")
    print(reply.output_text)
