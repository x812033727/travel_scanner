---
id: 2026-09-20-korea-food-specials-backlinks
title: Link city itineraries and must-eat to the Korea food specials
status: in-progress
priority: P2
area: docs
owner: claude-opus-5-5-kfood-links
claimed_at: 2026-10-02T19:26:02Z
created_at: 2026-09-20T09:41:00Z
completed_at:
branch: claude/korea-food-specials-backlinks
depends_on:
  - 2026-09-20-launch-korea-food-specials-1
scope:
  - apps/api/app/guides/content/korea-food-guide-must-eat.json
  - apps/api/app/guides/content/seoul-4-day-itinerary.json
  - apps/api/app/guides/content/busan-3-day-itinerary.json
  - apps/api/app/guides/content/jeju-3-day-itinerary.json
  - apps/api/app/guides/content/daegu-2-day-itinerary.json
  - apps/api/app/guides/content/jeonju-hanok-village-day-trip-from-seoul.json
  - apps/web/public/guides/korea-food-guide-must-eat/diagram-1.svg
---

# Link city itineraries and must-eat to the Korea food specials

## Why

2026-09-20 的韓國美食與咖啡特輯（22 篇）上線後，既有的韓國內容還不知道它們存在。讀者看完「韓國必吃美食」不會知道每道菜都有一篇寫哪裡吃得到；看完首爾四天行程也連不到當地的美食特輯。

**刻意不寫總覽文章**（那會是一直長大的清單，又跟 `korea-food-guide-must-eat` 搶同一批查詢），所以這些反向連結就是讀者發現新文章的主要路徑。

順便修掉兩個已知的用詞與事實問題：

| 檔案 | 問題 | 依據 |
| --- | --- | --- |
| `korea-food-guide-must-eat.json` | 寫「參雞湯」，特輯與料理資料庫的定案是「**蔘雞湯**」（KTO 繁中料理辭典官方名） | `docs/korea-food-specials/handoff/glossary.json` |
| `daegu-2-day-itinerary.json` | 寫「막창구이：烤牛的第四個胃 홍창」 | 官方來源今天不是這樣寫（大邱豬、牛都有，沒有來源用 홍창）。R-daegu 研究階段查證 |

## Definition of done

- [x] `korea-food-guide-must-eat` 的「各城市代表」一節，每個城市加一段連到該城市的美食特輯
- [x] 五篇城市行程各自連到該城市的美食／咖啡特輯
- [x] 「參雞湯」統一成「蔘雞湯」
- [x] 大邱行程的 막창 描述改成官方頁真的寫的內容（PR #1012 已改，見 Notes）
- [x] 每篇都通過 `pack_cli ingest --dry-run`（已入庫的內容包沒有工作區可 ingest，改跑 `pack_cli lint --slug`、intake `--from-content` 與 `test_guides_content_pack.py`，見 Notes）

## Steps

- [x] 等 `2026-09-20-launch-korea-food-specials-1` 的 22 篇在正式站發布（2026-09-21 已發布，見那張票）
- [x] 用 article inline（不是裸連結）連過去；目標都是 `howto`，不連 intel
- [x] 重新查證大邱 막창 的官方寫法再改（PR #1012 已改，這張票沒有再動那一行）
- [ ] 合併部署後（站主同意）在正式站匯入這六篇：`guides-import --slug ×6 --locale zh-TW --dry-run`，六篇都應是 `update`，再 `--publish`
- [ ] `guides-links-rebuild` 與 `guides-links-check --locale zh-TW`

## How to verify

```bash
cd apps/api && python -m app.guides.pack_cli lint --kind howto
```

零錯誤，且 `korea-food-guide-must-eat` 頁面上每個城市段落都有一個連到特輯的連結。

## Notes

- 22 篇的 slug 清單在 `2026-09-20-launch-korea-food-specials-1` 的 scope 裡。
- 不要在這些文章裡重寫特輯已經寫過的東西（店家清單、菜單解讀），一句話帶過再連過去就好。
- 相關：`2026-09-14-answer-first-howto-descriptions`。

### 2026-10-03 (claude-opus-5-5-kfood-links)

- Claim: `claim` refused because the dependency `2026-09-20-launch-korea-food-specials-1`
  is still `review` (codex). Its PR #601 (`codex/korea-food-specials-complete`) is merged,
  no open PR uses that branch, and that ticket's notes record the 22 articles published
  on production on 2026-09-21, so the claim was forced over a stale dependency.
- All six packs are zh-TW only, so every change is in that one locale. Every link is an
  `article` inline (`kind: howto`, all 22 targets exist with zh-TW), each in a new
  `rich_paragraph` inserted after an existing block; no existing block was edited except
  for the 蔘雞湯 spelling. No two article inlines are adjacent. Lead-ins only restate what
  the linked special already says (its description or its 排進行程 section); no shop
  names, prices or hours were copied in. Indices below are after the change.
  - `korea-food-guide-must-eat` (各城市代表): blocks[28] Seoul (9 dishes + 3 cafe areas),
    [30] Busan (2 + cafe), [33] Jeju (2 + 2 cafe), [35] Daegu (2), [36] a new Jeonju
    paragraph (bibimbap + the Jeonju day trip). All 22 specials are linked from this page.
  - `seoul-4-day-itinerary`: [16] Day 2 after 廣藏市場 (dak-hanmari street, hanok cafes),
    [29] Day 4 (Yeonnam/Hongdae and Seongsu cafes), [36] after the pre-trip list (all
    9 Seoul dish specials, next to the food directory link).
  - `busan-3-day-itinerary`: [13] end of Day 2's line-1 route (dwaeji-gukbap, milmyeon,
    Jeonpo/Yeongdo cafes; the cafe guide's own "transfer at Seomyeon / bus from Nampo or
    Jungang" wording).
  - `jeju-3-day-itinerary`: [7] Day 1 東門市場 (heukdwaeji, gogi-guksu), [13] Day 2 east
    route (Sehwa cafes, plus Aewol). Open ticket `2026-09-30-link-jeju-3-day-itinerary-to`
    names `blocks[19]`; that paragraph (Hallasan, 方案 B) is now `blocks[21]`.
  - `daegu-2-day-itinerary`: [39] in 吃什麼, after the market paragraph (makchang,
    jjim-galbi).
  - `jeonju-hanok-village-day-trip-from-seoul`: [27] in 吃什麼 (bibimbap).
- 參雞湯 → 蔘雞湯: 6 in `korea-food-guide-must-eat` (heading blocks[11], blocks[12],
  the diagram description twice, blocks[27], the 怕辣 list) and 4 in its `diagram-1.svg`
  (`<desc>` twice, two labels). The SVG was added to the scope because the image
  description is lifted from its `<desc>` and the drawn labels said 參; both now match
  (desc == description checked), and the re-rendered PNG shows 蔘 in both boxes. None of
  the other five packs had 參雞湯.
- Daegu 막창: already fixed by PR #1012 (`2026-09-21-korea-dish-names-contradict`):
  "烤腸（大腸頭），菜單上豬、牛都有，돼지막창是豬、소막창是牛", the makchang guide's wording,
  whose shop pages show both 돼지 and 소막창 in
  `docs/korea-food-specials/verification/daegu-makchang-food-guide/verify-1.md`. Not
  re-fetched or changed here.
- `pack_cli ingest --dry-run` needs a writing workspace, which shipped packs do not have;
  as for other edits to shipped packs, the checks were `pack_cli lint --slug` (0 errors
  for all six; only the `no_summary` warnings that were there before), the intake check
  `--from-content` (46 new inlines all `ok`; the failure count per pack is unchanged:
  missing summary, 5-column tables, `?city=` food links and 本文/這篇 counts were all
  there before), `pack_cli lint --kind howto` (152 entries, 0 errors), and
  `tests/test_guides_content_pack.py` (9 passed, 5 skipped).
- Not done here: production import and the link rebuild/check. They need a deploy and
  the owner's consent, so those two steps stay unticked.
