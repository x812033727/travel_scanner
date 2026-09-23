---
id: 2026-09-23-catchtable-batch-2-seoul-busan
title: CatchTable 第二批：首爾最佳榜 21–40 ＋ 釜山最佳榜前 20，操作步驟升成 skill
status: in-progress
priority: P2
area: ops
owner: claude-fable-5-1
claimed_at: 2026-09-23T06:20:35Z
created_at: 2026-09-23T06:20:33Z
completed_at:
branch: claude/catchtable-batch-2
depends_on: []
scope:
  - apps/api/app/foods/data/catchtable
  - docs/catalog-content-reviews/catchtable-batch-2.md
  - docs/catchtable-ranking-discovery.md
  - .agents/skills/catchtable-discovery
  - .claude/skills/catchtable-discovery
---

# CatchTable 第二批：首爾最佳榜 21–40 ＋ 釜山最佳榜前 20，操作步驟升成 skill

## Why

第一批（票 `2026-09-22-catchtable-ranking-discovery-batch-1`、`2026-09-23-catchtable-seoul-1-naver-approval`）量到：有官方來源 14/29、
能線上訂位 22/30、與目錄重複 1/30，14 家裡 12 家當天公開。站主 2026-09-23 同意第二批照設計文件「漏斗」一節的切法：
首爾最佳榜第 21–40 名 ＋ 釜山最佳榜前 20 名（候位榜不再取），並依設計文件的約定在第二批開跑時把「操作步驟與指令」升成 skill
（規則留在 `docs/catchtable-ranking-discovery.md`，skill 只搬指令、關卡與去哪裡讀）。

## Definition of done

- [x] `.agents/skills/catchtable-discovery/`（與 `.claude/skills/` 的逐字複本）：SKILL.md 主幹、榜頁收集片段、店頁判定片段（lazy section、隱藏面板的
      IntersectionObserver 包裝）、匯入與後台步驟、Naver 分工；`npm run test:tools` 過。
- [ ] `apps/api/app/foods/data/catchtable/2026-09-23-catchtable-batch-2/` 有 `rankings.json`、`candidates.json`、`merchants.json`、`platform-reviews.json`，
      `--check` 零錯誤，兩個匯入檔各自過 repo 解析器。
- [ ] 正式站：店家 dry-run 與報告一致後 `--apply`；平台列以 stdin 餵入 dry-run 後 `--apply`；再跑一次分別是 skipped_existing_slug／unchanged。
- [ ] 第 7 步：座標（官方頁 JSON-LD 或 OSM 節點）、Naver 精準頁（站主貼短網址、session 讀轉址）、核准；公開 API 前後計數寫進報告。
- [ ] 報告 `docs/catalog-content-reviews/catchtable-batch-2.md`：三個比例（首爾 21–40 與釜山分開量）、逐店表、無來源清單、未公開清單與原因。

## Steps

- [x] 升 skill（先做，之後照 skill 跑）。
- [x] 收集：`location-seoul` 第 21–40 名、`location-busan` 第 1–20 名，滾輪逐步累積、名次讀徽章、零衝突。
- [x] 去重：主機 worklist（seoul＋busan，`--include-researched`）＋ repo 內平台列的 CatchTable alias。
- [x] 逐店查證：研究代理各一個分頁；訂位判定在隱藏面板要用 IntersectionObserver 包裝並記 visibilityState；來源照設計文件順序（釜山：Visit Busan、KTO、區廳）。
- [ ] 複核抽三分之一 → 轉檔 → PR 一 → 部署 → 店家 dry-run／apply → worklist → 平台列 stdin dry-run／apply → PR 二。
- [ ] 第 7 步：座標 → 站主貼 Naver 短網址 → 後台逐家一次儲存「已驗證＋核准＋啟用」→ 公開 API 驗證 → 報告 → `done`。

## How to verify

```bash
python tools/catchtable_build_batches.py --candidates apps/api/app/foods/data/catchtable/2026-09-23-catchtable-batch-2/candidates-seoul.json --check
python tools/catchtable_build_batches.py --candidates apps/api/app/foods/data/catchtable/2026-09-23-catchtable-batch-2/candidates-busan.json --check
npm run test:tools && npm run check:tasks
curl -s -H 'X-Travel-Locale: zh-TW' "https://mokaair.com/api/travel/foods/merchants?destination_id=busan&limit=50" | python -m json.tool | grep -c catchtable_global
```

## Notes

- 第一批留下的兩家（산청 2 號店缺座標、고호재的 Naver 頁與韓國之家相同）不在本票；由站主決定。
- 2026-09-23 去重快照：worklist seoul 51 列（approved 41、rejected 7、pending 3）、busan 18 列（approved 15、rejected 3）。
- 2026-09-23 研究結果：首爾 21–40 → import 14、duplicate 1（alice_cheongdam）、no_official_source 5；釜山 1–20 → import 11、no_official_source 9；40 家全部 reservation。轉檔腳本一個候選檔只吃一個 destination，所以候選檔與匯入檔按城市分兩份（資料目錄 README 有寫）。
