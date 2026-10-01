---
id: 2026-09-20-kfood-isim-address-conflict
title: Verify Coffee Isim address conflict between Yeonnam and Yeonhui
status: done
priority: P2
area: api
owner: claude-opus-5-5
claimed_at: 2026-10-01T12:41:08Z
created_at: 2026-09-20T09:04:53Z
completed_at: 2026-10-01T12:46:10Z
branch: claude/isim-address
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

- [x] 兩個地址裡哪一個是今天的正確地址，有可查的依據支持
- [x] 正式站公開目錄與 `trend_merchants.json` 兩邊一致
- [x] 如果是搬家，記下搬家這件事（不要只是覆蓋掉舊地址）

## Steps

- [x] 用韓文店名在官方觀光網站（`visitseoul.net`、`visitkorea.or.kr`）找今天的店家頁
- [x] 對照 Naver 地圖的地點頁（精確地點網址，不是搜尋結果）
- [x] 判定後改正式站那筆（走後台，不是 repo）；`trend_merchants.json` 若也錯就一起改
- [x] 若判定它其實搬過家，順便檢查座標與 Place ID 是不是也停在舊址

## How to verify

```bash
curl -s "https://mokaair.com/api/travel/foods/merchants?q=이심" | python -m json.tool
```

回傳的地址與座標與官方頁、Naver 地點頁一致。

## Notes

- 查的時候 User-Agent 用 `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)`，不要放任何個人資料。
- 真正的修正在正式站後台（座標佇列），repo 這邊只有 `trend_merchants.json` 這份種子資料。scope 只列了 repo 檔案，因為後台不在 repo 裡。
- 相關：`2026-09-20-kfood-maxim-plant-evidence`（同一次研究撞到的另一筆公開店家資料問題）。
- 2026-10-01 (claude-opus-5-5): 搬家，不是錯。延南洞 동교로46길 42（觀光公社 2019 年文章）→
  西橋洞 → 2024-02-18 收店、2024-03-01 起在 서대문구 연희로15길 66。依據：正式站那筆的
  來源是首爾市休憩飲食店許可資料（OA-16095，西大門區 3120000-104-2024-00030），地址即現址，
  座標 37.57017, 126.929423 由許可建物點換算（2026-09-09），Naver 地點 37792215；
  店家移址經過見 postype「맛스플레인」2024-01-29 貼文與 polle 地點頁的評論。
  觀光公社的地點頁（ms_detail cotid=91b427c9-…）至今仍寫「마포구 서교동」，已過時，不能當依據。
- 正式站本來就對（地址、座標都是新址，沒有掛區域，沒有 Google Place ID），沒動。
  `trend_merchants.json` 改成新址與許可來源、confidence high，note 記下搬家經過；
  district_key 仍是 `yeonnam`，因為測試要求每筆都掛一個潮流街區，而延禧洞沒有街區。
  這份種子只建新 slug，既有 slug 會被跳過，所以不會覆寫正式站。
- 觀光公社兩頁過時可以用它們的「관광정보 수정요청」回報，那是對外送出，要站主決定。
