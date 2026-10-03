import json
slug = "ai-term-structured-outputs"
pack = {
  "slug": slug, "kind": "life", "destination_id": None, "topics": ["ai", "tutorial"],
  "valid_until": None, "featured": False, "display_order": 100,
  "locales": {"zh-TW": {
    "title": "結構化輸出（Structured Outputs）是什麼：讓 AI 照固定格式交資料",
    "description": "待寫",
    "hero": {"src": f"/guides/{slug}/hero.jpg", "alt": "待寫", "width": 1600, "height": 900},
    "blocks": [
      {"type": "paragraph", "text": "待寫導言一"},
      {"type": "paragraph", "text": "待寫導言二"},
      {"type": "heading", "level": 2, "text": "三種做法：要求、JSON 模式、schema 限制"},
      {"type": "heading", "level": 2, "text": "JSON Schema：只需要認得這幾個關鍵字"},
      {"type": "heading", "level": 2, "text": "示例：從報名信擷取姓名、日期、人數"},
      {"type": "heading", "level": 2, "text": "缺值、拒答與截斷怎麼接"},
      {"type": "heading", "level": 2, "text": "三家文件今天列出的限制"},
      {"type": "heading", "level": 2, "text": "和工具呼叫、提示詞串接的分工"},
    ],
    "sources": [
      {"title": "JSON Schema 2020-12：Core（規範原文，Internet-Draft）", "url": "https://json-schema.org/draft/2020-12/json-schema-core", "checked_on": "2026-10-03"},
      {"title": "JSON Schema 2020-12：Validation（驗證關鍵字，Internet-Draft）", "url": "https://json-schema.org/draft/2020-12/json-schema-validation", "checked_on": "2026-10-03"},
      {"title": "RFC 8259：JSON 資料交換格式（IETF 標準）", "url": "https://www.rfc-editor.org/rfc/rfc8259", "checked_on": "2026-10-03"},
      {"title": "OpenAI：Structured model outputs（官方開發者指南）", "url": "https://developers.openai.com/api/docs/guides/structured-outputs", "checked_on": "2026-10-03"},
      {"title": "Anthropic：Structured outputs（Claude Platform 官方文件）", "url": "https://platform.claude.com/docs/en/build-with-claude/structured-outputs", "checked_on": "2026-10-03"},
      {"title": "Google：Structured outputs（Gemini API 官方文件）", "url": "https://ai.google.dev/gemini-api/docs/structured-output", "checked_on": "2026-10-03"},
    ],
  }},
}
json.dump(pack, open("pack.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
