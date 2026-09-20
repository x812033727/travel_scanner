---
id: 2026-09-20-kfood-isim-address-conflict
title: Verify Coffee Isim address conflict between Yeonnam and Yeonhui
status: open
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-09-20T09:04:53Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/foods/data/trend_merchants.json
---

# Verify Coffee Isim address conflict between Yeonnam and Yeonhui

## Why

커피상점 이심（Coffee Isim）在我們自己的兩份資料裡有兩個地址，**相差一個行政區**：

| 來源 | 地址 | 區 |
| --- | --- | --- |
| `apps/api/app/foods/data/trend_merchants.json` | `마포구 동교로46길 42` | 麻浦區延南洞 |
| 2019 年韓國觀光公社文章 | 同上 | 麻浦區延南洞 |
| 正式站公開店家目錄（2026-09-09 驗證） | `서대문구 연희로15길 66` | 西大門區延禧洞 |

兩個都對是不可能的。可能是店搬過家（延南洞→延禧洞），也可能是其中一筆從頭就錯。

這是 2026-09-20 韓國咖啡店特輯的研究階段撞到的，**不是那一批造成的**。那一批因為無法判定而**沒有收錄這家店**，所以不擋任何東西——但一筆公開的店家資料指向錯誤的地點，讀者會走錯路。

## Definition of done

- [ ] 兩個地址裡哪一個是今天的正確地址，有可查的依據支持
- [ ] 正式站公開目錄與 `trend_merchants.json` 兩邊一致
- [ ] 如果是搬家，記下搬家這件事（不要只是覆蓋掉舊地址）

## Steps

- [ ] 用韓文店名在官方觀光網站（`visitseoul.net`、`visitkorea.or.kr`）找今天的店家頁
- [ ] 對照 Naver 地圖的地點頁（精確地點網址，不是搜尋結果）
- [ ] 判定後改正式站那筆（走後台，不是 repo）；`trend_merchants.json` 若也錯就一起改
- [ ] 若判定它其實搬過家，順便檢查座標與 Place ID 是不是也停在舊址

## How to verify

```bash
curl -s "https://mokaair.com/api/travel/foods/merchants?q=이심" | python -m json.tool
```

回傳的地址與座標與官方頁、Naver 地點頁一致。

## Notes

- 查的時候 User-Agent 用 `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)`，不要放任何個人資料。
- 真正的修正在正式站後台（座標佇列），repo 這邊只有 `trend_merchants.json` 這份種子資料。scope 只列了 repo 檔案，因為後台不在 repo 裡。
- 相關：`2026-09-20-kfood-maxim-plant-evidence`（同一次研究撞到的另一筆公開店家資料問題）。
