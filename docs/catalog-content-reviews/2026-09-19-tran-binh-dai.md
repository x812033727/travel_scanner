# 鎮平台（Q8669747）恢復核准紀錄（2026-09-19）

票：[`2026-09-19-re-approve-tran-binh-dai`](../../tasks/done/2026-09-19-re-approve-tran-binh-dai.md)。
站主在 2026-09-19 的對話中同意恢復；後台由站主登入，欄位由 claude-opus-5 填寫，最後的「核准」由站主按下。

## 為什麼被退

PR #403（2026-09-11）把 Q245016（軍事基地）加進 `DENIED_TYPES`。鎮平台在 Wikidata 上唯一的類型就是
Q245016，`classify_types` 於 2026-09-12 17:01:31 UTC 以 `denylisted_type` 把它判退。`rejected` 是墓碑，
每週的探索會永遠跳過它。PR #556 在 2026-09-19 把這個類型移出封鎖，但不會救回已經被退的列。

#556 部署後查了那張票點名的四個真景點，只有鎮平台是 `rejected`；原花園尋常小學校本館（Q10911386）、
島醫院（Q2410409）、喜屋武城（Q38278536）在 2026-09-12 都已人工核准。

## 查證

**身分。** 越南文維基的〈Trấn Bình đài〉寫它在順化京城東北角、鎮平門外，1805 年以土築成（原名太平台），
1836 年以磚重建並改名鎮平台，民間叫它芒魚屯（đồn Mang Cá）。英文維基稱為 Mang Cá Garrison。
Wikidata 條目沒有座標（P625）也沒有所在行政區（P131），只有越南文與英文維基連結。

**現況。** 芒魚屯長年是軍方用地。軍事單位已經遷出，2024–2025 年交還地方政府；
2026 年 4 月順化拆除芒魚屯圍牆、開路並改建公園，這一區正在開放給民眾。

**Place ID。** 依 [`docs/hotspot-review-next-batch.md`](../hotspot-review-next-batch.md) 的做法查兩次：

| 來源 | 查詢 | 結果 | 位置 | 與本列座標距離 |
| --- | --- | --- | --- | ---: |
| Places Autocomplete（官方 Place ID Finder） | `Đồn Mang Cá Huế` | Đồn Mang Cá，FHPG+5G4, Phu Xuan, Huế，`ChIJL5ESYAChQTERnr3JBGAuilk` | 16.4853761, 107.5755782 | 約 520 m |
| 後台 `map-candidates`（Text Search Pro，1 次） | 編輯器的「搜尋 Google 候選」，依本列資料查詢 | Hue Historic Citadel（整座順化京城） | 16.47694, 107.57396 | 約 1.47 km |

兩者不一致。Text Search 的第一筆是整座京城，不是這座堡壘，所以沒有套用；Autocomplete 的
「Đồn Mang Cá」正是維基寫明的俗名，採用它。`Trấn Bình Đài Huế` 這個查詢在 Autocomplete 找不到。
520 m 超過文件裡自動套用的 300 m 門檻，是逐筆判斷後採用：芒魚屯本身是一整片堡壘區。
寫入前確認過沒有其他景點用這個 Place ID（`google_place_id` 有唯一限制）。

## 寫入內容

「地點資料 › 地圖身分與座標」以 `hotspot_id=c149fbd0-5561-4906-b1e4-cc9ccef66058` 打開編輯器，先「儲存地點」，再在清單勾選後按「核准」：

| 欄位 | 之前 | 之後 |
| --- | --- | --- |
| 審核狀態 | `rejected` | `approved`（2026-09-19 06:57:40 UTC） |
| 比對狀態 | `unverified` | `verified` |
| Google Place ID | 無 | `ChIJL5ESYAChQTERnr3JBGAuilk` |
| 座標 | 16.489849, 107.577055 | 不變 |
| 座標來源類型 | `wikidata` | `admin_verified` |
| 座標來源網址 | `https://www.wikidata.org/wiki/Q8669747` | `https://vi.wikipedia.org/wiki/Tr%E1%BA%A5n_B%C3%ACnh_%C4%91%C3%A0i` |
| 審核理由 | `denylisted_type` | 恢復理由與兩個來源網址（450 字） |

座標沿用原值：它和越南文維基的 GeoData 完全相同，原本標的來源 Wikidata 其實沒有座標，
所以改記為人工查核、來源指向維基文章。Google 的座標沒有寫進資料庫。

## 核准後

- 資料庫：`approved`、`verified`、`admin_verified`、`is_active = true`。
- 公開排行讀的是每天的 `HotspotRanking` 快照，由 `hotspot-collector` 每 6 小時
  （`hotspot_collection_interval_seconds` = 21,600）重算。2026-09-19 的快照在核准前產生，
  所以核准當下 `/api/travel/hotspots/rankings?destination_id=hue` 仍是 53 筆、還沒有鎮平台。
  下一輪重算後才會出現，確認方法見票上的「How to verify」。

## 來源

- 越南文維基〈Trấn Bình đài〉：https://vi.wikipedia.org/wiki/Tr%E1%BA%A5n_B%C3%ACnh_%C4%91%C3%A0i
- 英文維基〈Trấn Bình đài〉：https://en.wikipedia.org/wiki/Tr%E1%BA%A5n_B%C3%ACnh_%C4%91%C3%A0i
- Tuổi Trẻ（2026-04）：https://tuoitre.vn/hue-thao-do-tuong-bao-don-mang-ca-mo-duong-va-lam-cong-vien-20260401155552459.htm
- Znews：https://lifestyle.zingnews.vn/di-doi-co-so-quan-su-ra-khoi-don-mang-ca-post1108428.html
- Nhân Dân：https://nhandan.vn/pha-tuong-mang-ca-noi-lai-mot-truc-duong-bi-cat-hon-the-ky-post952454.html
