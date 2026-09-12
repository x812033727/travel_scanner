---
id: 2026-09-11-destination-supported-gate-missing
title: 規格書明定為必要的目的地支援閘門從未實作
status: done
priority: P1
area: web
owner: claude-opus-5
claimed_at: 2026-09-11T18:39:08Z
created_at: 2026-09-11T03:21:01Z
completed_at: 2026-09-11T18:56:08Z
branch: claude/mokaair-website-access-k7xiku
depends_on: []
scope:
  - apps/api/app/ai/parser.py
  - apps/api/app/ai/router.py
  - apps/api/app/ai/trip_parser.py
  - apps/api/tests/test_ai_parser.py
  - apps/api/tests/test_ai_trip_parser_llm.py
  - apps/web/components/search-experience.tsx
  - apps/web/components/search-experience.test.tsx
  - apps/web/messages/en/search.json
  - apps/web/messages/ja/search.json
  - apps/web/messages/ko/search.json
  - apps/web/messages/zh-CN/search.json
  - apps/web/messages/zh-TW/search.json
  - docs/planning-flow-spec.md
---

# 規格書明定為必要的目的地支援閘門從未實作

## Why

`docs/planning-flow-spec.md` 把規劃流程拆成 PR1–PR12。PR4、6、7、8、11、12 都已上線，**PR3 與 PR5 沒有**，而且 `tasks/open/` 裡沒有任何一張在追蹤它們。

缺的東西：

| 規格位置 | 應有 | 現況 |
| --- | --- | --- |
| `:143-152` | `trip-brief-composer.tsx` | 不存在 |
| `:154-160` | `brief-confirm-panel.tsx` | 不存在 |
| `:267` | `POST /trips/draft/preview` | `apps/api` 零命中；`SaveTripRequest` 也沒有 `draft_preview_id` |
| `:266,317` | `/ai/parse-trip` 的 `must_include[]`、`constraints[]`、`destination_supported`，text 上限 2000→4000 | 全無；`apps/api/app/ai/parser.py:16` 仍是 `max_length=2000` |

`destination_supported` 這個欄位只出現在 `docs/`，`apps/` 裡一次都沒有。

規格自己對這件事的定調（`:157`，原文）：

> **Success, destination NOT supported (`destination_supported: false`):** stop here … **This gate is mandatory, not polish** — it will reject a real share of first attempts, and it is the difference between an honest limit and a wall.

實際後果，`docs/user-flow-plan.md:141` 講得很清楚：`match_destination` 失敗時 `_load_ai_planner_candidates` 回傳 `[]`，AI 草稿退化成一個空殼，而使用者要等到**行程已經建立之後**才發現這個目的地根本不支援。

## Definition of done

- [x] 使用者輸入不支援的目的地時，在建立行程之前就被明確告知，並得到可用目的地的建議。
- [x] `/ai/parse-trip` 回傳 `destination_supported`。
- [x] 不再有「建好行程才發現是空殼」的路徑。

## Steps

- [x] 先做最小可用的閘門，不必一次補完 PR3＋PR5：`/ai/parse-trip` 回傳 `destination_supported`，前端在進入建立流程前擋下並說明。
- [ ] 再決定 `trip-brief-composer` / `brief-confirm-panel` / `POST /trips/draft/preview` 這套草稿優先入口要不要照規格做完，或改走現行的五步精靈。**動工前先跟站主確認**——這是產品方向題，不是實作題。
- [x] `parser.py:16` 的 text 上限是否要放寬到 4000，一併確認。
- [x] 規格書更新：把已經做完的部分標記起來，把決定不做的部分寫清楚理由。

## How to verify

```bash
cd apps/api && uv run pytest tests -k "parse or planner" -q
cd apps/web && npm run test:web
```

手動：輸入一個明確不支援的目的地（例如南美城市），應在建立行程前就收到說明。

## Notes

- `docs/planning-flow-spec.md:325` 寫「Ingest only — inbox rows are not yet plannable」已經過時：`apps/api/app/trips/router.py:1487`（`_inbox_candidates`）、`:1463`、`:1560` 顯示 PR8 已上線，端點也改名了（規格寫 `POST /trips/{id}/places/{candidate_id}/promote`，實際是 `ingest_router.py:134` 的 `POST …/{candidate_id}/used`）。順手更正。
- `docs/affiliate-configuration.md:176-180` 的缺口 2（「合作選項只出現在搜尋頁」）也已過時——`trip-editor.tsx:2000` 已經渲染 `AffiliatePartnerOptions`。

## 完成紀錄（claude-opus-5, 2026-09-11）

依站主裁示只做最小可用閘門，沒有做 PR5 的草稿優先入口。

### `destination_supported` 有三種狀態，不是兩種

規格寫的是 `bool`，但實作成 `bool | None`：

- `true` —— 說出來的地方解析到我們搜得到的城市。
- `false` —— 說了一個地方，而它既不是我們涵蓋的城市、也不是我們涵蓋的區域。
- `null` —— 根本沒提到地方。

把後兩者合在一起，就會用「我們不去那裡」回答「你還沒說要去哪」。那是兩句不同的話，而且第二句是錯的。前端只在 `=== false` 時擋，`null` 時交給既有的 `missingCriteria`。

### 只有 LLM parser 能給這個訊號

`MockAITripParser` 是關鍵字比對，它分不出「說了一個我們不認得的地方」和「什麼都沒說」——兩種情況下 `match_destination` 都回 `None`。`trip_parser.py` 的 LLM 路徑則早就在追蹤 `dropped.append("destination")`（模型給了地名但解析不出來），那正是需要的訊號。

所以**沒有設定 AI 供應商時這個閘門不會作用**。這是這個增量的真實限制，寫進規格書了，不是漏做。

### `supported_destinations` 放在 router

兩個 parser 各自填會有機會給出不一樣的清單，所以在 `ai/router.py` 統一填，且只在 `destination_supported is False` 時填——成功的解析不該拖著一份用不到的清單。取 `SEARCHABLE_DESTINATIONS` 前六個：夠讓人看出涵蓋範圍的形狀，又不會把拒絕變成一份目錄。

### `text` 上限 2000 → 4000

照規格 `:266`。一份寫了每天住哪、吃哪、必去哪的 brief，遠在它不再是「一次請求」之前就會超過 2000 字。

### 驗證

後端六個案例（`test_ai_trip_parser_llm.py`）：
- 模型給了 `Reykjavik` → `destination_supported is False`
- 給了 `NRT` → `True`
- 什麼都沒給 → `None`（**這條是重點**：不可以把「沒說」講成「不支援」）
- 給了 `Aomori` + `Japan`（涵蓋的國家、沒涵蓋的城市）→ `None`
- 端點在 `False` 時附上非空的建議清單，每筆都有 code/city/country_label
- 端點在 `True` 時建議清單是空的

寫第四條時原本用 Sapporo，結果它在目錄裡（CTS）——測試自己先紅了一次，才換成真的沒涵蓋的城市。

前端兩個案例（`search-experience.test.tsx`）：`false` 時出現說明、建議連結指向 `destination=NRT`、開始鈕停用；`null` 時這段完全不出現。

把 `unsupportedDestination` 釘成 `false` 之後第一條變紅。後端把 `False` 分支拿掉之後對應那條也變紅。

`uv run pytest` 3263 passed、ruff 與 mypy 乾淨；`npm run test:web` 230 files / 2331 tests 全過。

### 規格書

`docs/planning-flow-spec.md` 的 PR3、PR5 與端點表都加了註記：做了什麼、沒做什麼、以及為什麼 `must_include` / `constraints` 還沒做。PR5 標成「刻意延後」，並寫明 `:157` 那句「mandatory, not polish」現在已經由搜尋入口滿足，剩下的是產品方向題。
