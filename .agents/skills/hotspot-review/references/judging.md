# 留或退：判斷景點候選

## 政策

- 拒絕碼只有五個：`not_a_place`、`no_visitor_draw`、`too_broad`、`gone`、`duplicate`。**預設 unsure**，因為拒絕是永久墓碑。
- 校準例子取自**已經上架**的列，讓類別本身不決定結果：蘭桂坊是街、濱海灣金沙是飯店、橫濱球場是球場、廣島市立袋町小學校是學校、定山渓郵便局是郵局，全都在目錄裡。
- 被一個已上架的上層地點涵蓋（公園裡的銅像、博物館本身的舊校舍）算 `duplicate`，理由寫明上層列的 slug。
- 施工中、爭議紀念物、商業空間算不算景點這類**價值判斷**交站主，不讓模型代決定；站主要的「留 pending」是合法結果。

## 證據包

判斷前先把證據備齊，不依賴現場抓取：Wikidata 標籤、描述、P31 標籤、P131、P625、遺產（P1435）、官網、part-of；加維基**全文**。

- `prop=extracts&explaintext=1` 不加 `exintro` 時一次只能查一頁（`exlimit` 對全文無效），要逐頁抓。
- 只看導言會兩個方向都誤判：市役所地下室的被爆資料展示室、小學校裡的校歌資料室、2025 年認定歷史建造物的銀行支店，都只在內文裡。改讀全文後，覆核推翻率從 68% 降到約 25%。

## 對抗式覆核

每一筆擬拒絕送兩名**獨立**覆核者：一位專找旅客會去的理由，一位查拒絕碼與證據對不對得上，並被要求證據太薄就反駁。只套用兩票都成立的拒絕。單一 pass 提的拒絕被推翻三分之二是常態，不是異常。

**數票陷阱**：覆核階段可能獨立於判定階段失敗（撞 session 上限），而 `refuted[id] || []` 這類彙總會把「從沒產生 ruling」與「有 ruling 但沒人反對」算成同一個結果——曾經 80 筆擬拒絕回報 60 筆通過，實際只審過 15 筆。**逐列數 ruling 票數**，`>= 2` 且無人反對才算通過。用 Workflow 時以 `resumeFromRunId` 重跑，判定代理走快取不重花，只重跑死掉的覆核。

## 兩輪都判不出來時

送兩名獨立裁決者，同時給拒絕論據與推翻它的反駁，並明說「交給人」不是免費選項（等於永遠沒人清）。只有兩人一致才決定。反覆出現的關鍵規則：**從缺席推論不構成造訪理由**——殘篇的沉默不能證明街上空無一物，指向路旁的公園或車站也不是走那條街的理由。留下來的要有具名證據（紀念物、DOCOMOMO 名錄、風景印）。

## 沒有 QID 的裸列（`origin='gemini_candidate'`）

沒有 QID、座標與條目，永遠過不了閘門。逐筆解析到 Wikidata，且只收落在該城市探索範圍內的：

- 已經在目錄裡 → 拒絕（`duplicate`，寫持有者）。
- 找到 QID → 單筆 `update` 補 `wikidata_item_id`（必附 `reason`），然後**直接寫入該 QID 的 P625 座標並核准**，不要把列停著等下次探索認領。
- 找不到 → 拒絕。QID 為 null 的墓碑不會擋住日後以真 QID 收錄（`discover_city` 以 QID 比對）；值得的話記下名稱讓人日後補種子。

## 型別白名單與黑名單

- 型別這條槓桿已經用盡：未分類的 P31 裡能安全全面拒絕的一個都沒有。加進 `ALLOWED_TYPES` 只會把待審理由換成 `map_identity_required`。
- `classify_types`（`apps/api/app/hotspots/discovery.py`）**先比 `DENIED_TYPES` 再比 `ALLOWED_TYPES`**，命中黑名單直接 rejected。軍事基地、小學、醫院這類黑名單型別曾誤殺真景點（琉球城跡、順化稜堡、台南歷史建築、廣島爆心地的醫院），而它們沒有 P1435 可當例外。改黑名單前先查待審與已核准列裡有多少會被打中。
- 探索只改寫 pending 列；approved、curated、rejected、disabled 都跳過，只更新 `last_seen_at`。

## 探索看得到什麼

`discover_city` 用 MediaWiki `geosearch`，單次呼叫上限是半徑 10 km、500 頁、依距離排序。現在大於 10 km 的中心會用六角格的多個 10 km 圓覆蓋整個設定半徑（`search_points`），所以設定半徑內的條目都看得到；範圍外的地標要手動補，不會被探索出來。

## 韓國列

`has_exact_map_identity` 對 KR 只認 Naver 精準頁網址。Wikidata 沒有 Naver Map 地點屬性、維基條目幾乎不外連、`map.naver.com` 在內建瀏覽器被政策擋掉、`allSearch` 對未驗證呼叫回 captcha。判斷留或退可以照做，但核准要金鑰或有人手動貼網址；`map.naver.com/p/api/search/instant-search` 曾回純 JSON，能不能拿來批次用是站主的決定（見 `tasks/open/2026-09-06-naver-maps-key.md`）。
