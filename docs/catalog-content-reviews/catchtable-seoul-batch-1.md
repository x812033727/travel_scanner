# CatchTable 榜單反推首爾新店家：第一批查核紀錄（2026-09-23）

站主 2026-09-22 給了 CatchTable 的兩個榜單入口，要「反推新增餐廳，並補足訂位連結」。方向與之前相反：
2026-09-11 是從目錄往 CatchTable 查（80 家公開韓國店家只有 7 家能在上面訂位、60 家根本不在上面），這次從榜單出發，
店一定在 CatchTable 上，但仍然要有官方來源才能進目錄。設計與邊界在 `docs/catchtable-ranking-discovery.md`，
候選檔在 `apps/api/app/foods/data/catchtable/2026-09-23-catchtable-seoul-1/`，票是
`2026-09-22-catchtable-ranking-discovery-batch-1`。

| 榜 | 網址 | 擷取時間（UTC） | 本批範圍 |
| --- | --- | --- | --- |
| 最佳餐廳榜（首爾） | `https://www.catchtable.net/zh-TW/ranking/location/location-seoul` | 2026-09-23 00:19 | 第 1–20 名 |
| 候位榜（首爾） | `https://www.catchtable.net/zh-TW/top-list/waiting/seoul/all` | 2026-09-23 00:06 | 第 1–10 名 |

兩榜沒有重複，合計 30 家。

## 做法

| 步驟 | 在哪裡 | 怎麼做 |
| --- | --- | --- |
| 收集榜單 | 本機內建瀏覽器 | 兩個榜都是虛擬化清單，重新載入後只用滾輪每步三格、等一秒、掃一次 DOM 累積，名次讀卡片徽章；同名次不同 alias 或同 alias 不同名次就整份作廢重抓。存 `rankings.json` |
| 去重 | 主機一次唯讀匯出 | `export-food-merchant-worklist --status all --destination seoul --include-researched`（37 家：29 approved、7 rejected、1 pending）＋ repo 內五個 `platform_reviews/*.json` 的 19 個 CatchTable alias |
| 逐店查證 | 本機內建瀏覽器，三個研究代理各一個分頁、各 10 家 | 店頁（身分、`hreflang`、訂位控制項）→ `/info` 分頁（韓文地址、電話、營網站）→ 官方來源（Visit Seoul、VisitKorea、區廳、政府名冊、店家官網）→ 每家寫完就存分片檔 |
| 複核 | 另一個代理 | 抽 `import` 的三分之一重開店頁與來源頁 |
| 轉檔 | `tools/catchtable_build_batches.py` | `--check` → `--merchants-out`；店家套用後 `--worklist … --platform-out` |

### 訂位判定（比 2026-09-21 的規則多了一條）

同時提供訂位與候位的店，店頁有 `service-tab-toggle`，底下是 `service-tab-DINING`（預訂）與
`service-tab-WAITING_REMOTE`（候位）兩個分頁，`dock-waiting-btn` 也在。2026-09-21 的規則「有『預訂』且沒有候位鈕
才算可訂位」會把這種店判成候位。本批的規則：

| 渲染後看到 | booking | 平台列 |
| --- | --- | --- |
| 有 `service-tab-DINING`，點開後有「日期 • 時間 • 人」與「尋找可用時間」（或沒有分頁切換、頁面直接就是這組控制項） | `reservation` | `verified` |
| 沒有 DINING 分頁，只有候位分頁／`waiting-remote-content`／`dock-waiting-btn` | `waiting_only` | `disabled` |
| 什麼控制項都沒有 | `none` | `disabled` |
| 404 或身分對不上 | `unclear` | 不產列 |

dock 按鈕上的「今日公休」是「現在不在營業時段」（開店前也顯示），不是公休日，不拿來判定。
頁尾「如果您喜歡」列的是別家店，那一段以下的文字不看。

### 來源規則

CatchTable、Naver、Google、Instagram、米其林只當發現與定位。進目錄要有講**這家分店**的官方頁：觀光局店家頁
（`official_tourism`）或店家自己的網站（`merchant_official`），地址（路名＋號）要對得上或明寫分店名；引文逐字、
畫面看得到、300 字內。地址只從官方頁抄；座標、Naver 精準頁、審核狀態批次一律不寫。名次只留在候選檔的
`ranking_evidence` 與平台列的一筆 evidence，不落地、不公開。

## 結果

（研究完成後填：看了幾家、`import`／`duplicate`／`no_official_source`／`not_a_restaurant`／`unclear` 各幾家、
`reservation`／`waiting_only`／`none` 各幾家、三個比例。）

## 逐店

（研究完成後填：名次、alias、韓文名、判定、來源等級、備註。）

## 疑似同店的判法

- `buchonyukhoe`（부촌육회，廣藏市場本店）：目錄裡已有 `seoul-buchon-yukhoe`，目前是 rejected、沒有地址。
  匯入器的第二把去重鑰匙是 `(destination, local_name)`，所以這筆記 `duplicate`，平台列會掛在那筆被退件的店上；
  別館（`buchonyukhoe_annex`，local_name 含「별관」）是另一家分店。
- `koreahouse_kohojae`（고호재）對 `seoul-korea-house`（한국의집，alias `koreahouse` 已是 verified）：同園區的另一個餐飲空間，
  以韓國之家官網是否把它列為獨立餐廳來判。
- `sancheongstar`（을지로2호점）與 `sancheong_ej`（을지로점）、`gebang`（논현／청담）與 `Gebang_ss`（성수점）：同品牌不同分店，
  `local_name` 帶分店名就不會互撞。
- `daelimchanggobar`（대림창고 다이닝 & 바）不在這兩個榜的範圍內（最佳榜前 24、候位榜前 20 都沒有），
  票 `2026-09-21-catchtable-apply-and-daerim` 的 A 項這批沒有收進來，見「還沒做完的」。

## 沒有官方來源的店

（研究完成後填：alias、韓文名、搜過的關鍵字、看到但不能用的頁。）

## 等站主貼 Naver 精準頁的店

（店家套用後填：這批新建的 pending 店家全部都要，因為韓國店家公開的守門是 Naver 精準地點頁。）

## 這批踩到的陷阱（下一批別再踩）

- **店頁的服務區塊是 lazy section。** 不往下捲就永遠不會渲染，畫面只剩底部「預訂」鈕或候位 dock。三個研究代理都把它當成
  「被擋」（其中一個還做了對照組、等了 60 秒），四家可訂位的店先被記成 `unclear`。正確做法：每步 500px、等 1 秒、最多 14 步，
  直到 `service-section-title`／`service-tab-toggle`／`waiting-remote-content` 出現；區塊出現時頁面才會呼叫 `dayslot-enc`、
  `timeslot-enc`、`online-reservation-open-schedule`。30 家全部重查後才定案。
- **同一家店同一天可能兩種畫面。** 熟成到 乙支路店 08:30 KST 有訂位＋候位雙分頁與日期選擇，兩小時後三次都只剩候位 dock；記 `unclear`，
  不硬判。
- **`RESERVED_ENTRY`（優先入場）不是訂位。** ARTIST BAKERY 的區塊有 `service-tab-RESERVED_ENTRY` 與候位分頁、沒有 DINING，仍是 `waiting_only`；
  `waiting-onsite-content`（現場候位）同理。
- 榜頁是虛擬化清單：捲到底再抓會漏掉榜首；`scrollTo` 跳著捲會撞到「徽章更新了、內容還是舊的」的回收卡片，同一家店出現在兩個名次。
  只用滾輪逐步捲＋累積＋衝突檢查才乾淨；候位榜第 1–4 名的卡片第一次渲染時是沒有 `href` 的 `<a>`。
- `export-food-merchant-worklist --out /tmp/x.json` 的檔案落在 api 容器裡，主機上 `cat` 不到；不帶 `--out` 直接讀 stdout。
- 來源網址只收 https：제주옥탑的品牌站只有 http（https 握手失敗），地址電話都對得上也只能記 `no_official_source`。
- `korean.visitkorea.or.kr` 的店家頁地址是前端動態載入、內建瀏覽器導向會被彈回原頁，用英文站（`english.visitkorea.or.kr/svc/contents/contentsView.do?vcontsId=…`）
  或 KTO 韓文頁的 `detail/ms_detail.do?cotid=…` 形式。
- 榜單會隨時間變：相隔 20 分鐘的兩次擷取，第 17–19 名順序不同。`captured_at` 是證據，用擷取當下的名次，不補位。

## 還沒做完的

（研究完成後填。）
