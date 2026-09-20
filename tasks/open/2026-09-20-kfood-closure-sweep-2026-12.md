---
id: 2026-09-20-kfood-closure-sweep-2026-12
title: Quarterly closure sweep for the Korea food specials
status: open
priority: P3
area: docs
owner:
claimed_at:
created_at: 2026-09-20T09:41:20Z
completed_at:
branch:
depends_on:
  - 2026-09-20-launch-korea-food-specials-1
scope:
  - docs/korea-food-specials
---

# Quarterly closure sweep for the Korea food specials

## Why

2026-09-20 的韓國美食與咖啡特輯共 22 篇、約 120 家店，每一家都寫了韓文地址、Naver 地圖連結，多數還寫了營業時間。**餐飲店會歇業、搬遷、改時間**，而我們沒有任何自動偵測的機制——每篇文章只有一個共用的警示框要讀者自己再確認。

這是**第一次**季度複查（目標 2026 年 12 月）。之後每季重開一張。

## Definition of done

- [ ] 22 篇裡每一家店的官方依據頁今天仍然存在、仍然點名這家店
- [ ] 歇業或搬遷的店已處理（見下面的規則）
- [ ] 營業時間與官方頁一致，或已改掉
- [ ] 下一季的複查票已開

## Steps

- [ ] 逐篇重抓 `sources` 裡的每個網址（UA 用 `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)`，同網域間隔至少 1 秒）
- [ ] 官方頁消失或不再點名該店 → **直接把那家店從文章移除**，不要改用非官方來源硬留
- [ ] 移除後若該篇剩不到 3 家（咖啡篇 4 家），照「不足」規則處理：同城市的料理家族 → 官方美食街頁面 → 併進主場城市篇 → 下架該篇
- [ ] 營業時間與官方頁不一致 → 改成官方頁今天寫的；**兩個官方來源打架就兩個都不寫**
- [ ] 開下一季的票

## How to verify

```bash
cd apps/api && python -m app.guides.pack_cli lint --kind howto
```

零錯誤，且每篇 `sources` 的 `checked_on` 都更新成這次複查的日期。

## Notes

- **不要用評論平台、部落格或媒體報導補資料**。這一批的入選標準是「有官方來源點名這家店這個分店」，補不到官方依據就移除，不要降低標準。
- **引用官方頁時要整段讀完**：서울미래유산的「설명」欄會在相鄰兩句給出互相矛盾的形容（문화옥：「맑고 깔끔한」之後 69 字寫「뽀얀 진국」）。詳見 `docs/korea-food-specials/`（原始筆記在工作目錄的 `prompts/SOURCE-TIPS.md`）。
- **引文必須在 `</head>` 之後**：`meta description`／`og:description`／`twitter:description` 的文字畫面上看不到，不能當來源。這一批有兩篇的規格栽在這裡。
- 原本計畫裡還有一張 `kfood-michelin-2027-edition`，**已取消**——本批全批不寫米其林（官網對我們每個工具都 403，政府頁的轉述又互相打架），沒有東西要複查。
