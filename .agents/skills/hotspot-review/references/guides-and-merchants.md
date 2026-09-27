# 介紹佇列、店家座標佇列、AI 目錄審核

後台儀表板的「待審工作」把幾個性質完全不同的佇列加在一起。能交給 AI 清的只有介紹。

## 介紹佇列（`hotspot_guides`）

標準探索（Brave 文章、YouTube 影片）把每筆命中直接寫成 `pending`、從不評分；`apps/api/app/hotspots/guide_review.py` 把 AI 搜尋路徑的同一套評估（`ASSESS_PROMPT`、`AssessmentBatch`、相關度 60 門檻）套到積壓上，並把分數與模型理由寫在列上。另有 `foreign_place` 先讀地理：標題或摘要只提到另一個目錄國家、從沒提到這個國家／城市／景點，就在門檻之前以「地點不符」退回（同名陷阱：河內的玉山祠與台灣玉山、圓山）。偵測到的語系跟標記不同時會搬到偵測到的語系。

```bash
# 先算要幾次呼叫：分組是 (景點, 語系)，一組至少一次呼叫，平均 2–3 筆
<COMPOSE> exec -T postgres sh -lc 'psql -U $POSTGRES_USER -d $POSTGRES_DB' <<'SQL'
SELECT count(*) FROM (SELECT hotspot_id, locale FROM hotspot_guides WHERE review_status = 'pending' GROUP BY 1, 2) g;
SQL
# 不帶 --apply 只報告；帶了才寫
<COMPOSE> exec -T api python -m app.cli review-pending-guides --provider gemini --limit 400 --max-calls 90 --max-output-tokens 24000
<COMPOSE> exec -T api python -m app.cli review-pending-guides --provider gemini --apply --limit 400 --max-calls 90 --max-output-tokens 24000
```

其他旗標：`--locale`（可重複）、`--min-relevance`（60）、`--min-quality`（40）、`--batch-size`（20）、`--verbose`。

- **`--max-output-tokens 24000`**：Gemini 的 thinking token 算在輸出上限裡，回覆被截斷就整批作廢。後台設定的介紹搜尋上限是為互動搜尋調的，可能比這低。
- 每批各自 commit，被中斷的執行再跑一次就接著做。
- `--limit 400` 分段，讓每段在背景指令十分鐘上限內跑完；**前景**的 `exec -T api python -m app.cli ...` 分類器放行，`nohup … &` 或把腳本從 stdin 灌進去的分離寫法會被擋。
- 品質夠信任：同名陷阱（鎌倉圓覺寺、內湖步道、千葉同名寺）都分對，理由用該列語言寫。核准的是主題相符的區域攻略，45–59 分被退的多半是「講到這一區但不是講這個地點」。

## 店家座標佇列（美食 → 補完 → 座標）

`apps/api/app/foods/coordinate_queue.py`，端點 `GET /admin/foods/merchants/coordinate-queue` 與 `POST /admin/foods/merchants/coordinate-queue/approve`。

- **核准只記錄 Place ID**，能驗證的國家把 `map_match_status` 設成 verified；**不寫座標**。座標與來源要另外從可引用的獨立來源補（Wikidata、官方觀光或店家官網、或管理員附 https 網址手填），Google 的座標從不變成目錄資料。
- 核准時伺服器**重新解析**，Google 的答案變了回 `candidate_changed`，不相信瀏覽器送來的東西；被退、停用、`ambiguous`／`disabled` 的回 `not_eligible`；ID 已屬別家回 `place_id_taken`。
- 名稱分數門檻 0.75、漂移上限 1 km，與景點相同。
- 查不到的店家有 24 小時負快取（`foods:coordinate_queue:no_result:<id>`），否則每次開頁都重花一次 Text Search Pro。元件只在分頁可見時掛載，同樣是為了不燒配額——改這一頁時別讓它在隱藏分頁掛載。
- KR 店家：識別存下來（`identity_saved`），但 verified 要等 Naver 精準頁（`is_exact_naver_map_url`）。

店家的 map 閘門與景點一樣，全是 unverified 時不能叫模型清。已有 Place ID 的先做 `place-ids.md` 的兩步驗證。

## AI 目錄審核頁

`/zh-TW/admin/hotspots?tab=review&section=ai`（美食在 `/zh-TW/admin/foods?tab=review&section=ai`），流程在 `docs/catalog-review.md`：Gemini 對 pending 快照抓公開證據、給建議，管理員選列預覽再確認；它不補 Place ID 與座標，韓國列仍要手貼 Naver 網址。它的建議與人工待審一樣適用 `judging.md` 的規則：拒絕是墓碑，搬過家的列要在排除清單上。
