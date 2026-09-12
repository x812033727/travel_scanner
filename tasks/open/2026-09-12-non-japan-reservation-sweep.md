---
id: 2026-09-12-non-japan-reservation-sweep
title: 台灣、新加坡、泰國、越南的訂位連結再掃一輪
status: in-progress
priority: P2
area: api
owner: claude-opus-5
claimed_at: 2026-09-12T16:21:20Z
created_at: 2026-09-12T13:54:35Z
completed_at:
branch: claude/food-booking-platform-links-72aee7
depends_on: []
scope:
  - apps/api/app/foods/data/platform_reviews/2026-09-13-non-japan-platforms.json
  - docs/catalog-content-reviews/2026-09-13-non-japan-platforms.md
---

# 台灣、新加坡、泰國、越南的訂位連結再掃一輪

## Why

日本第二輪（`2026-09-12-japan-korea-reservation-platforms`）證明了一件事：2026-09-11 那一輪留下的
候選頁很稀，不是因為店家沒有平台頁，而是因為當時的查法沒掃到。同樣 83 間店，第一輪只有 44 個候選頁，
第二輪用「每店一個代理去搜五個平台網域」拿到 259 個，多出來的裡面有 5 間真的能訂位。

其他國家還沒用這個方法掃過：

| 國家 | 公開店家 | 有訂位連結 |
| --- | ---: | ---: |
| 台灣 | 55 | 5 |
| 越南 | 24 | 0 |
| 泰國 | 25 | 5 |
| 新加坡 | 24 | 13 |

（香港由 `2026-09-12-hk-openrice-public` 另外處理，不要重複。）

## Definition of done

- [x] 這四國沒有訂位連結的店家都用第二輪的方法查過一次。（2026-09-13：105 間全部查過，
      結果寫在 `docs/catalog-content-reviews/2026-09-13-non-japan-platforms.md`）
- [ ] 能訂位的公開，不能訂位的存成停用，結果走 `apply-food-platform-reviews --file` 匯入。
      （這一輪沒有任何一家變成可訂位；104 筆待匯入）

## Steps

- [x] 取出四國沒有 `reservation_links` 的店家清單（公開 API 逐頁）＝105 間。
- [x] 每一國都改用該平台**自己的搜尋介面**查，而不是只看上一輪的候選頁；
      每個管道都先用平台上已知存在的店家驗證過會回傳正確結果。
- [x] 候選頁一律實際打開、依頁面上本店自己的訂位控制項機械化判斷。
- [ ] 產出 review 檔與查核摘要（已完成），PR、合併、部署、試跑、`--apply`。

## How to verify

`https://mokaair.com/api/travel/foods/merchants?limit=50` 逐頁統計 `reservation_links`。
這一輪套用後數字**不會變**（59 / 331），因為沒有新增可訂位的店家；要驗的是
`apply-food-platform-reviews --file app/foods/data/platform_reviews/2026-09-13-non-japan-platforms.json`
試跑顯示 104 筆 would_update / would_create，套用後 0 skipped。

## Notes

- 各國的支援平台：台灣 inline／EZTABLE／Maifood，新加坡 Chope／SevenRooms，泰國 Hungry Hub，
  越南 PasGo。日本新加的四個平台對這些國家沒用。
- **代理只找頁、不判斷能不能訂位**。這些平台同樣會在店頁上放別家店的訂位按鈕
  （2026-09-11 就被 OpenRice 的 Suggested Restaurants 騙過）。
- 2026-09-13 這一輪沒有用代理：四個平台裡有三個可以直接打它們自己的搜尋介面
  （EZTABLE `api-evo/search/autocomplete`、Hungry Hub `puma.hungryhub.com/graphql` 的
  `SearchSuggestions`、PasGo `Search/SearchHeader`），Chope 則有 22,631 頁的官方 sitemap 可全量比對，
  只有 inline 需要網路檢索。查核紀錄裡有每一支介面的驗證方式。

## 這一輪的結論（2026-09-13）

- **四國全數查無，可訂位的店家一間都沒有增加**，維持 59 / 331。寫入 104 筆：`not_found` 102、
  `disabled` 2。理由不是查核失敗：這 105 間以路邊攤、小吃老店、甜品店與書店咖啡為主。
- 解掉兩個 2026-09-11 的懸案：春水堂 信義店與 SIDOLI RADIO 的 inline 店頁都打開了，
  兩間都寫「抱歉，目前尚不開放線上訂位」，維持停用但理由變成「確認過不能訂位」。
- 三個**同品牌不同分店**的候選頁刻意不採用（Krua Apsorn 的 Samsen 與 Shinawatr 3、
  富錦樹台菜香檳 敦北店、The Blue Ginger Great World）。
- `singapore-song-fa` 完全不動（擁有者 2026-09-11 的決定）。

## 還沒做完的（留給下一個 session）

- `kaohsiung-jiu-zhen-nan` 的 inline 列仍是 `ambiguous`。檢索找得到「舊振南餅店 高雄中正店」
  `https://inline.app/booking/-NADjl6fHKgbU-9W6laz:inline-live-1/-NAJO8JVP2S8P6_wsanZ`，
  但被 inline 的按壓牆擋住，沒能確認它是不是清單這一家（22.63053, 120.29881）、也沒確認能不能訂位。
  這一批沒有寫入這一筆。
- `taipei-cafe-acme-fine-arts-museum`：inline 上有品牌頁 `-MYne3QpFTXQSW31f8Kt:inline-live-2`，
  但品牌頁沒有分店代碼、URL 規則不收；北美館分店的分店頁還沒拿到。
- （已解決）`kaohsiung-chun-shui-tang`、`taichung-chun-shui-siwei`：春水堂品牌頁的分店清單後來打開了，
  inline 上只有七家分店，高雄那一家（三民河堤路）與台中四維創始店都不在名單上，兩筆記成 `not_found`。
- inline 的按壓牆節奏：開一頁就會被擋，大約隔十分鐘才能再開一頁；403 對 curl 與 WebFetch 一樣，
  Firebase 也是 `Permission denied`。要一次做完這三筆，得留一段只做 inline 的時間。
