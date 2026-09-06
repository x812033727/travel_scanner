---
id: 2026-09-06-intro-generation
title: AI 起草景點介紹：產生工作、防護與後台觸發
status: in-progress
priority: P2
area: api
owner: claude-opus-5
claimed_at: 2026-09-06T19:52:08Z
created_at: 2026-09-06T19:52:07Z
completed_at:
branch: claude/intro-generation
depends_on: []
scope:
  - apps/api/app/hotspots/intro_generation.py
  - apps/api/app/hotspots/intro_tasks.py
  - apps/api/app/hotspots/admin_router.py
  - apps/api/app/hotspots/ai_search.py
  - apps/api/app/config.py
  - apps/api/app/worker.py
  - apps/api/tests/test_hotspot_intro_generation.py
  - docs/hotspot-themes.md
---
# AI 起草景點介紹：產生工作、防護與後台觸發

## Why

介紹（#260）把儲存、審核、顯示都做好了，後台畫面（#270）也有了，但**沒有東西會產生內容**。563 個景點乘上五種語言，不是有人會用手打完的量，所以這個功能實際上是空的。

## Definition of done

- [x] 後台按一次就能為一個景點產生五語草稿。
- [x] 產生的東西一律是 `pending`；已核准的段落預設不動。
- [x] 景點自己的文字**永遠不會變成指令**。
- [x] 宣稱營業時間、價格、折扣、電話、網址的草稿**不會進到待審佇列**。
- [x] 執行次數與呼叫次數都受每日額度限制。

## Steps

- [x] `intro_generation.py`：`INTRO_PROMPT`（常數）、`IntroDraft`／`IntroBatch`、`intro_context()`、`forbidden_claims()`／`length_ok()`／`review_draft()`、`generate_intro_drafts()`、`intro_model()`、`build_intro_provider()`。
- [x] `intro_tasks.py`：`execute_intro_run()` 與 RQ 進入點，照 `ai_tasks.py`；`worker.py` 加 `hotspot-intros` 佇列。
- [x] `ai_search.py`：`research_provider()` 加 `model`／`timeout_seconds`／`max_output_tokens` 關鍵字覆寫（預設行為不變）。
- [x] `config.py`：十個 `hotspot_intro_ai_*` 設定。
- [x] `admin_router.py`：`POST /{id}/intros/generate`（202、idempotency）與 `GET /intros/runs/{run_id}`。
- [x] 測試 15 個；`docs/hotspot-themes.md` 改寫成「已經有了」。
- [ ] 後台選供應商的設定卡——**另開任務** `2026-09-06-intro-ai-vendor-settings`。

## How to verify

```bash
cd apps/api && uv run ruff check . && uv run mypy app && uv run pytest   # 1164 passed
```

```
POST /admin/hotspots/{id}/intros/generate   {locales?, provider?, force?}  + Idempotency-Key
GET  /admin/hotspots/intros/runs/{run_id}
```

後台 `/admin/hotspots#intros` 產生一次，確認草稿以待審出現、run 的 `result` 列出 created／kept_approved／rejected。

## Notes

- **一次呼叫產出所有語言**，不是每語一次：這樣五種語言講的是同一組事實，也省呼叫。
- **景點文字是資料不是指令**：`INTRO_PROMPT` 是常數，景點只以 JSON 值出現在 payload。景點名稱來自 Wikidata 探索，等於外部輸入。測試裡有一個名字叫「淺草寺 IGNORE ALL PREVIOUS INSTRUCTIONS…」的景點，斷言送給供應商的 instructions 與常數逐字相同。
- **prompt 是請求，正則是規則**：模型被要求幫忙時會替一間它一無所知的寺廟寫出營業時間。所以 prompt 禁止之外，`forbidden_claims()` 再檢查一次輸出並直接丟掉那份草稿——一個看起來很合理的假事實，比缺一句話糟糕得多，尤其它會坐在一個有人一路點過去的佇列裡。被丟掉的會列在 run 的 `result_json`，不是默默消失。
- 長度上限逐語系分開：140 個英文字和 140 個漢字不是同一段文章。
- 供應商轉接器沿用 guide search 的，透過 `research_provider()` 的新關鍵字覆寫，不另抄一份；預設行為完全沒變。
- **呼叫額度在送出請求之前就扣**：中途炸掉一樣付了錢給供應商。
- 沒做後台選供應商的卡片：`admin.json` 被 `2026-09-06-admin-panels-i18n-remaining` 佔著，而且用設定檔的預設供應商就能跑。另開任務記下了五個接點。
