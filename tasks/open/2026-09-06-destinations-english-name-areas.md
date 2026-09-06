---
id: 2026-09-06-destinations-english-name-areas
title: destinations 的 english_name 存繁中、areas 不隨語系
status: in-progress
priority: P2
area: api
owner: claude-opus-5
claimed_at: 2026-09-06T13:20:48Z
created_at: 2026-09-06T09:56:54Z
completed_at:
branch: claude/place-names-i18n
depends_on: []
scope:
  - apps/api/app/destinations/localized.py
---

# destinations 的 english_name 存繁中、areas 不隨語系

## Why

2026-09-06 正式站實測 `GET /destinations`（`X-Travel-Locale: en`）：

```json
{"id":"tokyo","city":"Tokyo","local_name":"東京","english_name":"東京",
 "areas":["新宿","上野／淺草","東京站／銀座","澀谷"]}
```

- `city` 本地化正確（Tokyo），但 `english_name` 裝的是「東京」而不是英文名，欄位名與內容不符；
  用到這個欄位的地方會拿到中文。
- `areas[]` 在 en／ja／ko 都維持繁中，和同一支回應裡已經本地化的 `city` 不一致。
  （`/hotspots/facets` 的 areas 反而是本地化的，兩邊行為不一樣。）

## Definition of done

- [x] `english_name` 是英文：33 筆全部，退回順序改成 CITY_NAMES 的英文名再退回目錄文字。
- [ ] `/destinations` 的 `areas[]` 依 `X-Travel-Locale` 回該語系，與 `/hotspots/facets` 一致。

## How to verify

```bash
curl -s -H 'X-Travel-Locale: en' http://127.0.0.1:8090/api/v1/destinations | head -c 400
```

## Notes

國家與城市名稱在 `/hotspots/facets`、`/foods/cities` 完全沒本地化，是另一張票
`2026-09-06-food-hotspot-place-names-i18n`，兩者可能共用同一套 `localized_names` 修法。

## Result（一半完成，areas 需要產品決策）

`english_name` 修好了。33 筆裡有 19 筆沒設這個欄位，所有讀取端都退回 `profile.city`（繁中），
所以一個叫 english_name 的欄位回傳中文。`CITY_NAMES` 本來就有 33 筆已核對的英文名，改成先
退回那裡。現在 0 筆回傳中文。同一個修法也套用到 `/foods/cities`。

**areas 沒有動，但原因不是我原先寫的那個。下面那段量測是錯的，已於 2026-09-06 重量並更正。**

### 更正：原本記的「只有 38 個（28%）對得上」是錯的

錯在比對方式，不在資料。兩份目錄用不同的寫法表示同一個地方：destinations 寫「澀谷」，
`HOTSPOT_AREAS` 寫「澀谷／原宿」；而且各語系用各自的連接符號——zh 用 `／`、ja 用 `・`、
en 與 ko 用 ` & ` 或 `, `。第一次量測拿整串字比對，又只切了 destinations 那一側，所以把
「同一個地方換個寫法」全部算成「對不上」。

把兩側都依 `／ / ・ & , 、` 切開，再**限制在同一個城市內**比對（跨城市比對會把首爾的明洞
配到別的城市去，不能算數），真實的數字是：

| | 筆數 | 佔 132 |
| --- | --- | --- |
| 該地名已存在於同城市的座標核可區域目錄 | 117 | 89% |
| 其中五個語系都能逐段對齊、可直接沿用已審過的譯名 | 101 | 77% |
| 存在但各語系的切法不一致（例：`白金／高砂` 的 en 只有 `Shirogane`） | 16 | 12% |
| 目錄裡完全沒有、需要新譯名 | 15 | 11% |

15 個沒有的是：濟州市、Silom、尼曼區、夜市周邊、克隆芒、西區（台中）、國分町、青葉通、
紙屋町、河畔（清萊）、舊城（清萊）、中西區（台南）、海安路、韓屋村、完山公園。

所以「另外 94 個要新造翻譯」是錯的，實際上是 15 個。`localized.py` 檔頭那條
「沒有人對照地圖檢查過的翻譯比原文更糟」的設計決定仍然成立，但它現在只擋得住 15 筆，
不是 94 筆——擋不住把已經審過的 101 筆搬過來用。

### 還是沒動的原因（現在是這個）

剩下的是三個各有代價的選項，而且**每一個都會改到 zh-TW 這個主要語系看到的文案**，
所以是產品決定不是機械修正：

1. **改成引用區域代碼。** destinations 的 areas 不再存自由字串，改存 `HOTSPOT_AREAS` 的
   area code，顯示時取該語系名稱。最乾淨，五語系一次到位，但 zh-TW 看到的會從「澀谷」
   變成「澀谷／原宿」——標籤變廣了，是文案變更。另外 15 筆沒有對應代碼的還是要處理。
2. **逐段沿用譯名。** 把 destinations 的字串依分隔符切段，每段查同城市的區域目錄取該語系
   的對應段，再用該語系自己的連接符號接回去。zh-TW 完全不變，101 筆（77%）立刻正確。
   代價是剩下 31 筆仍是繁中，而且它們**集中在少數城市**（台南 3 個裡有 2 個、全州 4 個裡
   有 2 個、清萊 4 個裡有 2 個、仙台 4 個裡有 2 個），那幾個城市會變成中英夾雜的清單。
3. **補完那 15 筆再做選項 2。** 15 個地名 × 4 個語系 = 60 句，全部是有標準譯名的知名地區。
   這是唯一能讓五個語系都乾淨的路，但它正是檔頭那條設計決定要擋的事，需要有人對照地圖核過。

我的建議是 3，但那要擁有者同意「這 15 筆值得請人核一次」。在那之前不動，比做一半好。

背景仍然成立：兩份區域目錄的用途本來就不同（destinations 的是「該住哪一區」、hotspots 的是
「篩景點用」），要哪一份當權威是產品決定。zh-CN 欄位缺漏那個前置條件已經解決，見
[[2026-09-06-zh-cn-area-labels-traditional]]。

重量的方式（任何人都能重跑）：以 `DESTINATIONS_BY_ID[*].code` 當城市鍵去查 `HOTSPOT_AREAS`，
兩側都用 `re.split(r"\s*(?:[／/・&,、]|\band\b)\s*")` 切段後比對。
