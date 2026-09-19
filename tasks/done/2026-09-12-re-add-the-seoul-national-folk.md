---
id: 2026-09-12-re-add-the-seoul-national-folk
title: Re-add the Seoul National Folk Museum after its Wikidata QID was tombstoned
status: done
priority: P2
area: ops
owner: claude-opus-5
claimed_at: 2026-09-19T07:58:58Z
created_at: 2026-09-12T02:09:36Z
completed_at: 2026-09-19T08:00:06Z
branch: claude/host-steps-2026-09-19
depends_on: []
scope:
  - docs/hotspot-review-next-batch.md
---

# Re-add the Seoul National Folk Museum after its Wikidata QID was tombstoned

## Why

Hotspot `557a6eb0-0592-4ab2-b2a9-707eabb0febb` (國立民俗博物館, QID **Q486449**) sat pending
under city `PUS` (Busan) even though the museum is in Seoul. On 2026-09-12 a Gemini
catalog-review recommendation from run `0a194879` rejected it — "目的地設為釜山，但該實體位於
首爾特別市，目的地歸屬與地理座標完全不符" — and that rejection was applied at 01:56 UTC.

The rejection of that row is defensible: the row really was wrong. The cost is that
`discover_hotspots` skips rows whose `review_status` is `rejected`/`disabled`, keyed by
Wikidata QID, so the weekly Wikimedia pass will never re-add this museum under Seoul.
The catalog now holds no row for it at all — a genuine Seoul attraction is missing.

## Definition of done

- [x] The museum exists in the catalog under Seoul with an exact map identity (Naver for
      KR, per the publication gate), durable coordinates and their source, and is approved.
- [x] It appears in the public rankings for the Seoul destination.
- [x] The wrong Busan row stays rejected, or is corrected in place through a reviewed
      process — no blanket un-rejection of tombstones.

## Steps

- [x] Pick the route: a curated seed entry, `import-hotspot-candidates --apply` with a
      manifest, or a reviewed correction of the existing row's destination.
- [x] Get the identity the gate requires (KR rows need an exact Naver map URL, not a
      Google Place ID) and take coordinates from Wikidata P625 with its source URL.
- [x] Apply through the normal admin review flow so the audit records a real actor.

## How to verify

Read-only first: `select id, name, city_code, review_status from travel_hotspots where
wikidata_item_id = 'Q486449';`

Then the public BFF: `/api/travel/hotspots/rankings?destination_id=<seoul destination id>`
must list it (the param is `destination_id` or `city_code` — `destination` is ignored, and
attractions have no standalone detail page, so a `/hotspots/<slug>` URL returns 404).

## Notes

Cross-run exclusion lists must be carried forward: this row had been deliberately excluded
from the 2026-09-12 morning sweep of run `d943205e`, but the afternoon sweep of run
`0a194879` only carried 新福宮 in its skip list, so this one went through.

新福宮 (Q10306724, a Taipei temple filed under Taichung) is the same shape of problem and is
still `pending` — keep it out of blanket rejections for the same reason.

### 2026-09-19 準備（claude-fable-5-1）

沒有正式機權限，只做到「主機指令可以照抄」為止；完整內容在
`docs/hotspot-review-next-batch.md` 最後一節「2026-09-19: 國立民俗博物館 (Q486449)」。

**路線已定：就地修正既有列（第三條路），不是 seed，也不是 manifest。** 原因寫在程式碼裡：
`wikidata_item_id` 與 `slug` 皆為 unique，墓碑列 `557a6eb0`（`wikidata-q486449`）佔著兩者；
`seed_catalog` 依 QID 認領後被 `_seed_can_reconcile_hotspot` 拒絕（非 approved 的 curated 列），
`persist_resolutions` 回 `skipped:previously_rejected`，`collect_hotspots` 同樣略過；而
`/admin/hotspots/review` 不准替換或清除既有 QID（`hotspot_wikidata_identity_locked`），所以墓碑
無法透過審核流程讓出識別。匯入器也根本沒有 `naver_map_url` 欄位，KR 列走那條路永遠過不了守門。
manifest 仍寫進文件備查（`{"city_code": "ICN", "candidates": [{"name": "國立民俗博物館",
"district": "鍾路區"}]}`），dry-run 會花一次 Text Search Pro 然後回 `skipped:previously_rejected`。

**識別資料已齊：**
- Wikidata Q486449（https://www.wikidata.org/wiki/Q486449，revision 2515870060）：ko 국립민속박물관 /
  zh-hant 國立民俗博物館 / en National Folk Museum of Korea；P625 **37.581625, 126.97909**；
  P856 http://www.nfm.go.kr/；P131 Q36929 鍾路區；P31 Q17431399 national museum。
- Naver 精準地點：**https://map.naver.com/p/entry/place/11620599**（국립민속박물관，서울특별시 종로구
  삼청로 37，37.5815644, 126.9789313，距 P625 15.5 m），來自 `map.naver.com/p/api/search/instant-search`
  ——同站的即時搜尋端點，回純 JSON、沒有 captcha；`allSearch` 仍回 `ncaptcha`，`m.place` 429，
  `nfm.go.kr` 經 egress proxy 連線被重置，ko.wikipedia extlinks 429。九次請求全部記在文件裡。
  鄰近易混淆：`11620680` 是兒童博物館、`18664772` 是公車站。
- 落區：`resolve_area_code("ICN", …)` → `jongno`。

**還需要擁有者（依序）：**
1. 用瀏覽器開一次 `https://map.naver.com/p/entry/place/11620599`，確認是本館不是兒童博物館。
2. 主機唯讀 SQL（文件裡有完整 heredoc 版本）：`select id, slug, name, city_code, destination_id,
   review_status, map_match_status, naver_map_url, updated_at from travel_hotspots where
   wikidata_item_id in ('Q486449','Q10306724') or naver_map_url = '…/11620599';`
   ——預期 Q486449 仍是 `PUS / rejected / unverified`，且沒有第三列佔用該 Naver 網址。
3. 後台 `/zh-TW/admin/hotspots` 對 `557a6eb0` 做兩步：`update`（destination_id `seoul`、座標
   37.581625/126.97909、`coordinate_source_type` `wikidata`、`coordinate_source_url`
   https://www.wikidata.org/wiki/Q486449、`naver_map_url` 上述網址、`map_match_status` `verified`、
   reason 見文件），再 `approve`。審核紀錄會以真實管理員入帳（`hotspot_candidates_reviewed`）。
4. 最多六小時後（rankings 為快照）：
   `https://mokaair.com/api/travel/hotspots/rankings?destination_id=seoul&q=民俗&limit=50`
   應列出 `wikidata-q486449` / `seoul` / `ICN`。

**兩點更正給下一位：** 新福宮 Q10306724 依同一份文件的第四批次已於 2026-09-13 改歸 `taipei` 並以
`admin_verified` 座標核准，不再是 pending（上面的 SQL 會一併證實）；兩個 QID 在 step 2 落地前都該留在
catalog-review 的 skip list 上。本次沒有寫入任何資料庫，也沒有 commit。

### 2026-09-19 主機執行（claude-opus-5，站主逐項同意；部署 `6a254971` 之後）

- Wikidata Q486449 re-read before writing: P625 37.581625, 126.97909, revision 2515870060, as the review document records.
- In `/zh-TW/admin/hotspots?tab=places&section=identity&hotspot_id=557a6eb0-…`: moved to `seoul` with the review document's reason (admin said 「已移動 1 筆景點至 seoul」), then the location editor saved the P625 pair, source `wikidata` + `https://www.wikidata.org/wiki/Q486449`, Naver `https://map.naver.com/p/entry/place/11620599`, `verified`, and the same reason. The owner pressed 核准.
- Database afterwards: `ICN / seoul / approved / is_active / verified`, Naver URL set, reviewed 2026-09-19 07:56:07 UTC.
- Still open: the public rankings item. The day's `HotspotRanking` snapshot was rebuilt by the collector right after the 07:41 deploy, before this approval, so the museum joins the Seoul ranking on the next 6-hourly refresh.

### 2026-09-19 public ranking check (claude-opus-5)

- The 08:25 UTC redeploy restarted the collector, whose first run rebuilt the day's snapshot: `/api/travel/hotspots/rankings?destination_id=seoul&q=國立民俗博物館` returns it at rank 44.
