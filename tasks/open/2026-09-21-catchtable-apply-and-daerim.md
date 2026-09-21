---
id: 2026-09-21-catchtable-apply-and-daerim
title: CatchTable 九筆已套用；剩大林倉庫餐酒館卡在 Naver 網址
status: open
priority: P2
area: ops
owner:
claimed_at:
created_at: 2026-09-21T05:10:00Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/foods/data/platform_reviews
---

# CatchTable 九筆已套用；剩大林倉庫餐酒館卡在 Naver 網址

## Why

2026-09-21 站主要求「把 CatchTable 的連結補到對應的資料庫」。查完之後發現
**待補的空缺幾乎不存在**：正式站 80 家公開的韓國店家，全部 80 家都已經有判定結果
（7 verified、60 not_found、11 disabled、2 ambiguous）。看起來沒查過的 6 家其實是
2026-09-11 管理員在後台逐筆填的，所以不在 repo 的批次檔裡，線上早就有連結。

真正要做的縮成三件，其中兩件已經完成並合併：

| | 狀態 |
|---|---|
| D. `/ja-JP/` 網址被語言驗證擋掉 | **已合併**（PR #610，`_CATCHTABLE_LANGUAGES`） |
| B+C. 解掉 2 筆 ambiguous、7 筆補語言版本 | **已套用到正式站**（2026-09-21，`dafbf1ee` 部署後） |
| A. 大林倉庫 dining & bar 建成新店家 | **卡住**，見下 |

**B+C 已完成。** 2026-09-21 部署 `dafbf1ee` 之後套用，`updated 9 / skipped 0`，
六筆 verified、兩筆 disabled、一筆 not_found 全數寫入。正式站實測：

| 送出的語言 | 回傳的網址 |
|---|---|
| `zh-TW` | `https://www.catchtable.net/zh-TW/shop/<slug>` |
| `zh-CN` | `https://www.catchtable.net/zh-CN/shop/<slug>` |
| `ja` | `https://www.catchtable.net/ja-JP/shop/<slug>` |
| `ko` | `https://www.catchtable.net/shop/<slug>`（無前綴，CatchTable 沒有韓文版） |

`seoul-hyoddeu` 的公開訂位按鈕**已經消失**，那是這批唯一拿掉東西的一筆。

**一個會害人白忙的細節：`X-Travel-Locale` 只吃 `en / ja / ko / zh-TW / zh-CN`**
（`apps/api/app/i18n.py` 的 `LOCALES`，預設 `zh-TW`）。送 `ja-JP` 不會報錯，
會**安靜地回退到 zh-TW**，於是看起來像日文網址沒生效。驗證時別送 CatchTable 自己的代碼。
另外 `limit` 上限低於 100（`limit=50` 可、`limit=100` 回 422），`country_code` 不是有效篩選。

## Definition of done

- [x] `2026-09-21-korea-catchtable.json` 套進正式站資料庫。
- [x] 6 家 verified 的店在 API 上帶出訂位網址（zh-TW／zh-CN／ja／ko 四種都驗過）。
- [x] `seoul-hyoddeu` 已無按鈕（這批唯一拿掉東西的一筆）。
- [x] 切換語言會換到對應語言的網址。

## Steps

- [x] 先部署（要含 #610）。
- [x] dry-run，**先看計畫再套**：

```bash
docker compose -f docker-compose.prod.yml exec -T api python -m app.cli \
  apply-food-platform-reviews --file app/foods/data/platform_reviews/2026-09-21-korea-catchtable.json
```

- [x] 確認計畫無誤後加 `--apply`。
- [x] 線上驗：

```bash
curl -s -H 'X-Travel-Locale: zh-CN' "https://mokaair.com/api/travel/foods/merchants?destination_id=seoul&limit=50" \
  | python -m json.tool | grep -A3 catchtable_global
```

## Notes

### 檔案內容（9 筆）

```
daegu-nosekondo                 verified
daegu-yurang                    verified
gyeongju-yosokkoong             verified
seoul-korea-house               verified
seoul-maple-tree-house          verified
seoul-osulloc-teahouse-bukchon  verified
seoul-hyoddeu                   disabled   ← 套用前線上有按鈕，但頁面只能候位；現已移除
chunshim                        disabled
seoul-somunnanseongsugamjatang  not_found
```

**`seoul-hyoddeu` 是這次唯一拿掉東西的一筆。** 套用前正式站有那顆訂位按鈕，
但點進去的 CatchTable 頁面只能線上候位，不能訂位；依站主規則要 `disabled` 不公開。
**注意 API 的 `serviceTypes` 欄位單獨看判斷不出來**，是實際渲染頁面才看到的——
下次查別的平台時，這是唯一可靠的方法。已於 2026-09-21 套用，按鈕確認消失。

### 三個會踩到的點

- `verified` 與 `disabled` **都強制要有 `evidence` 陣列**。
- 一筆壞掉整個檔案會被拒絕，不是跳過那一筆。
- **已由管理員在後台審過的列會被跳過**，除非記錄帶上那一列精確的
  `expected_checked_at`。既有 7 筆正是管理員 2026-09-11 審過的，檔案裡已經帶了。

### A 項為什麼卡住

站主舉的例子 `catchtable.net/shop/daelimchanggobar` 指的是
**대림창고 다이닝 & 바**（餐酒館），不是資料庫裡的 `seoul-daerimcanggo`（同園區的藝廊咖啡店）。
站主裁示：建成新的獨立店家，咖啡店那筆維持 `not_found` 不動。

要生出一筆**可公開**的店家，`publishable_merchant_filters()` 要求全部滿足：
`review_status='approved'`、`is_active=True`、`map_match_status='verified'`、
座標在範圍內且 `coordinate_source_type` 屬於 `DURABLE_COORDINATE_SOURCES`、
`coordinate_source_url` 是 https、**韓國必須有帶精確地點前綴的 `naver_map_url`**、
且至少一筆 `is_current` 的 `FoodMerchantSource`。

**卡在那個 `naver_map_url`。** `map.naver.com` 在內建瀏覽器被政策擋掉，
而且**不可以改用 Chrome 或 curl 繞過**。需要站主自己貼一個 Naver 地圖網址進來，
或改由後台 `/zh-TW/admin/foods` 手動建立（`seed_food_catalog` 只會建
`pending` 且 `is_active=False` 的列，生不出公開店家）。發布類的最終按鈕依慣例由站主按。

### CatchTable 的查證方法（實測，省下次的時間）

- 它是 SPA。原始 HTML 是 6,836 bytes 的空殼，**連不存在的 slug 也回 200**，
  所以狀態碼與抓網頁都判斷不了；渲染後才會出現真正的 404，**必須用瀏覽器逐頁確認**。
  API 內容有加密（`apiDataEncrypt.util`），不走逆向。
- 各語言網址只差一個路徑前綴，由頁面的 `hreflang` 給出：繁中 `/zh-TW/`、簡中 `/zh-CN/`、
  日文 `/ja-JP/`、英文無前綴（同時是 x-default）。**韓文不在 hreflang 清單上，
  不要生一個 `/ko/` 填進去，那是捏造的。**
- 判斷可不可以訂位時**不能整頁搜關鍵字**：頁尾有「如果您喜歡」推薦其他餐廳的區塊，
  要看店家自己的控制項（日期選擇、「尋找可用時間」、「預訂」）。
- slug 沒有規律（`koreahouse`、`hieutu_yongsan`、`cave_urang`、`yosukgung.kr`、
  `hani._.noodle`），只能靠站內搜尋找；而搜尋框是 React 受控元件，
  **程式化輸入進不去**，自動化查找的路徑尚未打通。
