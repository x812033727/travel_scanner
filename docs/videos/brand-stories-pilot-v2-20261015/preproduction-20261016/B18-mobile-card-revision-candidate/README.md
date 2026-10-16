# B18 `idea-s027` 手機字卡的隔離修訂候選

2026-10-16。原作者六章、合稿與既有收據保持原樣；這個候選只改 `idea-s027.data.subtitle`，旁白與來源標籤不改。原三行重複列出「J-Net21／發明協會」，在 320×180 縮圖太小；修訂副標為「兩份資料，兩種說法」。主標和來源徽章仍逐字列出兩個發布者，後續相鄰旁白依序將撲克牌說法歸給 J-Net21、名片說法歸給發明協會，接著明言無法從兩份記載挑出唯一時刻。

`variant.json` 釘住原章／原合稿 SHA-256、場景 ID 及前後文字。`verify.mjs` 只在兩份原始檔與預期完全一致時，於本機暫存目錄輸出修訂章與合稿，並用正式 `slideHtml`／`openRenderer.capture` 渲染此張字卡。它不改原始檔、不聯網、不呼叫付費模型、不匯入主機。

```powershell
node docs/videos/brand-stories-pilot-v2-20261015/preproduction-20261016/B18-mobile-card-revision-candidate/verify.mjs
```

| 項目 | SHA-256 |
| --- | --- |
| 原章 `idea.json` | `159a25dc1a13ac1247467507064625f3599db535500c67a88c490cebaff763b1` |
| 原合稿 `video.json` | `3e39c24f64b1a719fa338db39578fbf1e31f1f95058b66c8544f934f3bffff7e` |
| 修訂章 `idea.json` 暫存輸出 | `fed58f73da9ec724cc6151b36ad806e62013eefe0db97d0914de702c0b3c4121` |
| 修訂合稿 `video.json` 暫存輸出 | `a95537f505e42d0f731b3280bf63fc543aea7e8906c8293e1a95decb09ebfd3e` |
| [320×180 字卡](idea-s027-320x180.png) | `2c777428a427d93fb1bde88461c732bb5854d96e951d51c6c05a7ec3e7bc3dd5` |

正式渲染器回報 **0 個版面、字型或資源問題**；縮圖的主標、副標均為單行，未裁切。[獨立審查](independent-review-20261016.md)重跑雜湊／渲染、對照兩份 JSON 的單欄差異，對這一張靜態字卡的可讀性與稿內來源歸屬給予限定 PASS。整片停留時間、字幕遮擋及外部來源事實仍待驗收。它不解除 B18 65 項 UNCHECKED 主張、作者章採用 #1518 的四項阻擋，也不代表可以製作付費媒體。
