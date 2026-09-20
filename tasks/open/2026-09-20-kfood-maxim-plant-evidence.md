---
id: 2026-09-20-kfood-maxim-plant-evidence
title: Maxim Plant is public with only B-grade evidence
status: open
priority: P3
area: api
owner:
claimed_at:
created_at: 2026-09-20T09:05:10Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/foods/data/trend_merchants.json
---

# Maxim Plant is public with only B-grade evidence

## Why

맥심플랜트（Maxim Plant，漢南洞）已經公開在正式站的店家目錄，但它的入選依據**只有品牌自己的官網與座標資料**——沒有任何觀光公社或市政府的頁面描述這家店。

2026-09-20 韓國咖啡店特輯的研究代理為了寫乙支路・漢南篇去找它的官方依據，`visitseoul.net` 與 `visitkorea.or.kr` 都找不到任何一頁講這家店，只有品牌官網與媒體報導。那一篇因此整題淘汰（合格店家只有 1 家，遠低於咖啡篇下限 4 家）。

**這不是那一批造成的**，那一批只是照出了它。要不要處理，取決於站方對「公開的店家都要有可查依據」這件事的標準：

- 如果要維持這個標準 → 補上 A 級依據，補不到就下架
- 如果品牌官網對連鎖咖啡品牌就夠 → 把這個判準寫進 `docs/catalog-review.md`，免得下次又有人來問

## Definition of done

- [ ] 這一筆的處置有明確結論（補依據／下架／確認 B 級對這類店就夠）
- [ ] 結論寫進 `docs/catalog-review.md`，不是只改這一筆

## Steps

- [ ] 再找一次官方依據（可能有新頁；也試 `english.visitkorea.or.kr` 與 `tchinese.visitseoul.net`）
- [ ] 找不到就請站主決定標準
- [ ] 照結論處理，並把判準寫進文件
- [ ] 順手檢查公開目錄裡還有沒有同類的（只有 B 級依據卻已公開）

## How to verify

```bash
curl -s "https://mokaair.com/api/travel/foods/merchants?q=맥심" | python -m json.tool
```

回傳的那筆的來源欄位符合結論（有 A 級來源，或該筆已下架，或文件已寫明 B 級對這類店可接受）。

## Notes

- 查的時候 User-Agent 用 `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)`，不要放任何個人資料。
- A／B 級的定義見 2026-09 韓國特輯的來源規則：A1 觀光公社／政府的店家專頁或官方專題點名、A2 政府認證且有公開名冊；B 級（店家官網）只能補事實，不能當入選依據。
- 相關：`2026-09-20-kfood-isim-address-conflict`（同一次研究撞到的另一筆公開店家資料問題）。
