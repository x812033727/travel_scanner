---
id: 2026-09-11-destination-supported-gate-missing
title: 規格書明定為必要的目的地支援閘門從未實作
status: open
priority: P1
area: web
owner:
claimed_at:
created_at: 2026-09-11T03:21:01Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/ai/parser.py
  - apps/web/components/trip-brief-composer.tsx
  - apps/web/components/brief-confirm-panel.tsx
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

- [ ] 使用者輸入不支援的目的地時，在建立行程之前就被明確告知，並得到可用目的地的建議。
- [ ] `/ai/parse-trip` 回傳 `destination_supported`。
- [ ] 不再有「建好行程才發現是空殼」的路徑。

## Steps

- [ ] 先做最小可用的閘門，不必一次補完 PR3＋PR5：`/ai/parse-trip` 回傳 `destination_supported`，前端在進入建立流程前擋下並說明。
- [ ] 再決定 `trip-brief-composer` / `brief-confirm-panel` / `POST /trips/draft/preview` 這套草稿優先入口要不要照規格做完，或改走現行的五步精靈。**動工前先跟站主確認**——這是產品方向題，不是實作題。
- [ ] `parser.py:16` 的 text 上限是否要放寬到 4000，一併確認。
- [ ] 規格書更新：把已經做完的部分標記起來，把決定不做的部分寫清楚理由。

## How to verify

```bash
cd apps/api && uv run pytest tests -k "parse or planner" -q
cd apps/web && npm run test:web
```

手動：輸入一個明確不支援的目的地（例如南美城市），應在建立行程前就收到說明。

## Notes

- `docs/planning-flow-spec.md:325` 寫「Ingest only — inbox rows are not yet plannable」已經過時：`apps/api/app/trips/router.py:1487`（`_inbox_candidates`）、`:1463`、`:1560` 顯示 PR8 已上線，端點也改名了（規格寫 `POST /trips/{id}/places/{candidate_id}/promote`，實際是 `ingest_router.py:134` 的 `POST …/{candidate_id}/used`）。順手更正。
- `docs/affiliate-configuration.md:176-180` 的缺口 2（「合作選項只出現在搜尋頁」）也已過時——`trip-editor.tsx:2000` 已經渲染 `AffiliatePartnerOptions`。
