---
id: 2026-10-04-ou-de-jianghu-roadmap-decisions
title: 偶的江湖 全系列路線圖：17 項待站主決定的事（生父、冥棺、超量季、支線第四部、主角缺席等）
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-10-04T13:14:13Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/series-plans/ou-de-jianghu/saga
---

# 偶的江湖 全系列路線圖：17 項待站主決定的事（生父、冥棺、超量季、支線第四部、主角缺席等）

## Why

《偶的江湖》全系列路線圖（`docs/videos/series-plans/ou-de-jianghu/saga/README.md`）把主線排成 65 季 780 集、外傳 2 季 24 集，但合併與缺漏檢查留下 17 項只有站主能決定的事，清單在路線圖最後一節「需要站主決定的事」。決定之前，第三季以後的分集細綱不能開寫：生父、冥棺、超量季與主角缺席都會改到季級的事件。

## Definition of done

- [ ] 路線圖最後一節的 17 項，每一項都有站主的決定（採用建議、改成別的、或明確不做），寫在本票 Notes。
- [ ] 路線圖、`saga/roadmap.json`、`saga/names.json` 依決定更新；標「建議，待站主核准」的字樣改成定案或刪除。
- [ ] 若決定做支線第四部，另開一張票做外傳第三季的時代企劃。

## Steps

- [ ] 把 17 項逐項問站主（可以一次問完，附路線圖的建議）。
- [ ] 依決定改路線圖與兩個 JSON；重跑名字掃描（不得出現原作人名與「霹靂」字樣）。
- [ ] 回填各時代企劃的季號與跨期生死（第 11、13 項）要等第三季以後真的開寫細綱時，在那一期的企劃包裡做，不在本票。

## How to verify

```bash
grep -c "建議，待站主核准" docs/videos/series-plans/ou-de-jianghu/saga/README.md   # 決定完應為 0
grep -rl "霹靂" docs/videos/series-plans/ou-de-jianghu || echo clean
node docs/videos/series-plans/ou-de-jianghu/validate.mjs
```

## Notes

- 各時代的完整企劃、原作研究與含原作人名的對照表不在 repo，2026-10-04 以私人檔案交給站主（含原作人名，只當內部工作檔）。
- 路線圖的「對應原作」欄在 repo 版只寫時代代號（〔原作 E05〕），原作劇名在私人版。
