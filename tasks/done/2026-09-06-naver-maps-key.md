---
id: 2026-09-06-naver-maps-key
title: 沒有 NAVER 金鑰，韓國景點與店家無法發布
status: done
priority: P2
area: ops
owner: codex-open-task-reconcile-510e
claimed_at: 2026-10-24T13:19:46Z
created_at: 2026-09-06T00:54:38Z
completed_at: 2026-10-24T13:20:00Z
branch: codex/open-tasks-reconcile-20261024
depends_on: []
scope:
  - apps/api/app/places/naver.py
---

# 沒有 NAVER 金鑰，韓國景點與店家無法發布

## Why

發布守門對韓國的要求和其他國家不同：`has_exact_map_identity()` 在 `country_code == 'KR'`
時只認 NAVER 的精準地點頁（`https://map.naver.com/p/entry/place/…` 或 `/v5/entry/place/…`），
Google Place ID 不算數。

所以韓國的東西全部卡住：**176 個景點**沒有 `verified`，加上這次匯入的首爾／釜山／
濟州／大邱／全州店家（座標可以先寫進去，但 `map_match_status` 會停在 `unverified`，
匯入回報是 `coordinates_saved`）。

使用者已經知道這件事，回覆是「晚點」自己申請。這張任務存在的目的是不要讓它被忘記，
以及把金鑰到手之後該做什麼寫清楚。

## Definition of done

- [ ] 正式機有可用的 NAVER 金鑰，`python -m app.cli verify-naver-maps` 通過。
- [ ] 韓國景點與店家能取得 NAVER 精準地點頁，`map_match_status` 可以翻成 `verified`。

## Steps

- [ ] 使用者申請金鑰（個人開發者可申請；步驟先前整理過，見 Notes）。
- [ ] 金鑰放進正式機 `.env`，注意：`.env` 裡已存在的鍵會蓋掉程式預設值，
      而且改完要 `docker compose up -d <服務>`，`restart` 不會重讀。
- [ ] 跑 `verify-naver-maps` 確認可用。
- [ ] 寫一個比照 `match-food-merchant-places` 的批次，把韓國景點／店家對到 NAVER 地點頁。
- [ ] 回頭把 2026-09-06-merchant-coordinate-backlog 裡停在 `coordinates_saved` 的韓國
      店家推完最後一哩。

## How to verify

```bash
docker compose -f docker-compose.prod.yml exec -T api python -m app.cli verify-naver-maps
```

```sql
SELECT count(*) FROM travel_hotspots
WHERE city_code IN ('ICN','PUS','CJU','TAE','GYE','JEO') AND map_match_status <> 'verified';
```

跑完應該大幅下降（2026-09-06 是 176）。

## Notes

**不要試圖繞過這條規則**。用 Google Place ID 充當韓國的地圖識別會讓
`has_exact_map_identity` 形同虛設；那條規則是刻意的（韓國的地圖資料 Google 覆蓋不完整）。
座標可以先靠 `admin_verified` 寫入，識別碼不行。

**接受的網址前綴**只有兩個，寫死在 `apps/api/app/hotspots/maps.py` 的
`EXACT_NAVER_PLACE_PREFIXES`：`https://map.naver.com/p/entry/place/` 和
`https://map.naver.com/v5/entry/place/`。搜尋結果頁或短網址都不算。

座標佇列的 UI 已經會標示「韓國店家：座標可先寫入，發布仍需 Naver 精準地點頁」，
判斷用的是 `is_exact_naver_map_url()` 而不是「有沒有 naver 網址」，所以貼錯格式的
網址不會被誤判為完成。

2026-09-06 claude-fable-5-1：狀態改 `blocked`，等使用者申請金鑰；金鑰到手後上面 Steps 照順序做。
現在卡在這裡的東西比立案時多：176 個韓國景點未 verified（不變）、**65 個 KR 景點 pending**
（review 守門要 NAVER 精準頁）、**24 家 KR 店家已有 admin_verified 座標但停在
coordinates_saved**（座標佇列這輪寫入的），另外 43 家 KR 店家連座標都還沒有。


### 2026-10-24 owner-directed completion

站主要求處理open任務，本票由本輪協調者接手結案。純任務紀錄收尾，不接管其他producer。

- Outstanding: 韓國景點與店家能取得 NAVER 精準地點頁，`map_match_status` 可以翻成 `verified`。
- No current NAVER key validity probe attempted; manual precise Naver identities are a separate path and may make the old headline too broad.
- Owner 2026-10-24 explicitly chose 封存兩張供應商擴充票. Close key-enrollment expansion; no key applied, configured or verified. Actual KR candidate/merchant tasks stay open and exact-map publication guards stay unchanged.

保留並向站主確認本票的資料、帳號、成本或驗收決策；不重播未知請求。

站主本輪明確選擇「封存兩張供應商擴充票」。封存原因是暫不進行帳號／金鑰／新供應商擴充，非宣稱金鑰已配置或舊API關卡已通過。保留原研究、未勾項、URL與historical receipts；各景點／店家補值及精準地圖發布守門仍有效，不關閉其工作票。
