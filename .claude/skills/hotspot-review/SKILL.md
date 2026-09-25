---
name: hotspot-review
description: 清後台的三個待審佇列：景點（hotspot）、景點介紹（guide）與美食店家座標；判斷留或退（讀全文、兩名獨立覆核）、找與驗證 Google Place ID（Autocomplete 與 map-candidates 互相對答案、免配額的一次核准、Place Details Enterprise 每月上限）、map_match_status 與免費兩步驗證、Wikidata／維基座標錯時用 admin_verified 加 OSM 修、恢復被退的景點、用 Gemini 清介紹佇列、不開 Postgres 用 mock API 看 /hotspots。部署、看板、文章、CatchTable 店家、影片、主機維運、目錄匯入各有自己的 skill（deploy、task-board、content-pipeline、catchtable-discovery、youtube-video、prod-host-ops、catalog-import）。要清待審、核准或退回景點、補 Place ID、處理 409 或 map_verification_required、修錯的上游座標時，先讀這個 skill。Clear the hotspot, guide and merchant-coordinate review queues and verify map identities and coordinates.
metadata:
  short-description: 景點／介紹／店家座標待審：判斷、Place ID、座標、核准
---

# 景點待審（hotspot-review）

這個 skill 只放規矩、流程與去哪裡讀；細節在 `references/`。寫入一律走後台（`/zh-TW/admin/hotspots`、`/zh-TW/admin/foods`）或它背後的 BFF 端點 `/api/travel/admin/...`（API 本身是 `/api/v1/admin/...`），用已登入的管理員身分；CLI 在主機的 api 容器裡跑，`<SSH>` 與 `<COMPOSE>` 的寫法見 skill `deploy`（`<COMPOSE>` ＝ `docker compose -f docker-compose.prod.yml`）。

## 先認清佇列卡在哪

| 佇列 | 真正的瓶頸 | 能不能叫模型清 |
| --- | --- | --- |
| 景點（`travel_hotspots` pending） | **精準地圖識別**：核准要 `map_match_status='verified'`，也就是 Place ID（韓國是 Naver 精準頁）＋永久座標來源 | 判斷留或退可以；Place ID 與座標不行 |
| 介紹（`hotspot_guides` pending） | 沒人評分：標準探索把每筆命中直接寫成 pending | 可以，`review-pending-guides` |
| 店家座標（美食 → 補完 → 座標） | 同景點，要 Place ID 與可稽核座標 | 不行 |

`collect_hotspots` 會把每一筆 `auto_approved` 降成 `pending / map_identity_required`，所以加型別白名單從來不會讓任何東西上架。

## 不變的規矩

1. **核准一次呼叫、不花 Google 配額**：`POST /admin/hotspots/review` 帶 `action:'approve'`、`google_place_id`、`map_match_status:'verified'`、`reason`；`_validate_hotspot_location` 是純本地驗證。要錢的只有「找」Place ID。
2. **退回是永久墓碑**：探索與匯入以 QID 認領時跳過 rejected／disabled，QID 與 slug 又是唯一的。單一 pass 提的拒絕送兩名獨立覆核（一位找旅客會去的理由、一位查證據對不對得上），**逐列數票**，兩票都不反對才套用。
3. **證據不足就補全文**，不要再叫模型猜；「條目很短所以可能有東西」不是造訪理由。價值判斷（政治、爭議紀念物、施工中）交站主。
4. **Google 座標永遠不進目錄**。座標要 `DURABLE_COORDINATE_SOURCES`（curated、wikidata、official_tourism、merchant_official、admin_verified）＋ https 來源網址。
5. **一公尺吻合不是證據**：座標本身錯時候選會跟著錯。每筆核准用 Autocomplete 與 map-candidates 兩個工具對答案，名稱比對 Wikidata 全語言標籤＋別名，不只比存檔名稱。
6. **不要自己打座標**：漂移檢查只用該列真正存的座標或有來源的座標。
7. **韓國只認 `https://map.naver.com/p/entry/place/`**（或 `/v5/entry/place/`），永遠不吃 Place ID；Naver 搜尋對未驗證呼叫回 captcha，**不繞**。KR 列靠金鑰（`tasks/open/2026-09-06-naver-maps-key.md`）或人工。
8. **編輯 Wikidata 先問站主**（匿名編輯會留下這台機器的 IP，代輸密碼不做）；不動上游也能用 `admin_verified` 解。
9. **批次寫入要節流**：邊緣層限流會回 429，降並發、每筆間隔 300–450 ms 並重試；`ids` 一次最多 100 筆，Place ID／Naver 網址只能單筆。
10. 所有對外請求用 UA `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)`，不帶任何人的個資。

## 主幹

1. **盤點**：後台 `?tab=review&section=manual` 看 pending；分國家（KR 另列）、分有沒有 QID、有沒有 Place ID；查本月 Google 用量（`references/place-ids.md`）。
2. **建證據包**：每列的 Wikidata 標籤、描述、P31、P131、P625，加維基**全文**；判斷不依賴現場抓取。
3. **判斷**：keep／reject／unsure，拒絕碼只用 `not_a_place`、`no_visitor_draw`、`too_broad`、`gone`、`duplicate`，預設 unsure；拒絕走兩名覆核（`references/judging.md`）。
4. **找 Place ID**：查詢字串逐級加細（在地名稱 → P131 → 更下一級町名 → 條目裡的現用名），兩個工具對答案，自動套用只收名稱分數 ≥ 0.75 且漂移 ≤ 0.3 km，其餘逐筆看。
5. **修座標**（只在上游錯、且有第二個獨立來源時）：`references/coordinates.md`。
6. **寫入**：一次呼叫核准；要改分類或補 QID 先單筆 `update`（必附 `reason`）再核准；409 照 `references/api.md` 分兩種處理。
7. **驗證**：排名是快照，`hotspot-collector` 每 21,600 秒重建，核准後最多等六小時才出現在 `/api/travel/hotspots/rankings?destination_id=<city>`；延伸城市一定用 `destination_id`（用 `city_code` 會 422 `destination_id_required`）。
8. **收尾**：把數字、留下的列與原因寫進票或 `docs/`；還開著的列寫清楚各自在等什麼。

## 常用指令

```bash
# 介紹佇列：先不帶 --apply 看報告，再分段套用（每段 400 筆、前景跑）
<SSH> "cd /root/travel_scanner && <COMPOSE> exec -T api python -m app.cli review-pending-guides --provider gemini --limit 400 --max-calls 90 --max-output-tokens 24000"
<SSH> "cd /root/travel_scanner && <COMPOSE> exec -T api python -m app.cli review-pending-guides --provider gemini --apply --limit 400 --max-calls 90 --max-output-tokens 24000"
# 自動配對一個目的地的 Place ID（吃 Place Details Enterprise，先 --dry-run）
<SSH> "cd /root/travel_scanner && <COMPOSE> exec -T api python -m app.cli match-hotspot-places --destination tokyo --dry-run"
<SSH> "cd /root/travel_scanner && <COMPOSE> exec -T api python -m app.cli match-hotspot-places --approve <slug>"
```

## 去哪裡讀

| 問題 | 讀 |
| --- | --- |
| 兩個找 Place ID 的工具、查詢改寫、名稱比對、配額與上限、免費兩步驗證、`map_match_status`、`match-hotspot-places`、官方 Place ID Finder | `.agents/skills/hotspot-review/references/place-ids.md` |
| 留或退的政策、對抗式覆核、數票陷阱、全文、無 QID 的裸列、型別黑白名單、探索的範圍 | `.agents/skills/hotspot-review/references/judging.md` |
| 上游座標錯怎麼判、`admin_verified`＋OSM、官方觀光網、搬城市、`search_text` | `.agents/skills/hotspot-review/references/coordinates.md` |
| review 端點的每種呼叫、409／422 錯誤碼、恢復被退的景點、後台直達網址、瀏覽器操作陷阱 | `.agents/skills/hotspot-review/references/api.md` |
| 介紹佇列（Gemini）、店家座標佇列、AI 目錄審核頁 | `.agents/skills/hotspot-review/references/guides-and-merchants.md` |
| 不開 Postgres 在本機看 `/hotspots`、區域（area）的規則 | `.agents/skills/hotspot-review/references/local-preview.md` |
| 四批清佇列的完整紀錄與數字、國立民俗博物館的就地更正 | `docs/hotspot-review-next-batch.md` |
| 排名公式、來源政策、Place 補齊的自動配對門檻、設定值 | `docs/hotspot-intelligence.md` |
| 單筆編輯器的契約（分類、補 QID、理由、版本時間） | `docs/hotspot-review-editor.md` |
| AI 目錄審核頁（Gemini）的流程 | `docs/catalog-review.md` |

`.claude/skills/hotspot-review/SKILL.md` 是這一份的逐字複本，`npm run test:tools` 會比對。
