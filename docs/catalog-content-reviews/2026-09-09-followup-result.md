# 美食店家與景點介紹：2026-09-09 複審結果

本批 443 筆已逐筆複審並記錄結果；40 筆核准公開、148 筆退件、255 筆保留待補證。這是完成本批審查，不是宣稱全部內容已通過或所有資料缺口已解決。

正式資料套用成功，獨立驗證完成於 **2026-09-09 00:40:45 Asia/Taipei**；00:41:22 再次確認待審集合，沒有新漏單。

| 類型 | 本批審查 | 核准 | 退件 | 待補證 |
| --- | ---: | ---: | ---: | ---: |
| 美食店家 | 163 | 0 | 0 | 163 |
| 景點文章 | 172 | 10 | 103 | 59 |
| 景點影片 | 108 | 30 | 45 | 33 |
| 合計 | 443 | 40 | 148 | 255 |

逐筆 ID、理由、原始來源、既有／新證據區分與指紋保存在 [審核紀錄](2026-09-09-followup.json)。本輪沒有新增候選、重建商品、修改服務設定或部署程式。

## 方法與實際改善

本批來自 00:04:34 的正式站快照，443 筆與前批保留項目完全一致，沒有 ID 或資料漂移。逐筆重審先前真正取得的 Gemini／瀏覽器證據；未把沿用證據寫成今天重新造訪。

- 文章補查原站正文、實際轉址與官方參照，並檢查已知同景點來源重複。新增 10 篇可用介绍；103 篇因通用首頁、搜尋／短貼文聚合、不支援的實際語言、錯誤景點或已證實的重要內容錯誤退件。無法存取不等於失效，仍保留。
- 影片按景點片段、實質解說、可理解語言重新評選。國語解說不額外要求繁中字幕；音訊不分繁簡字體。現場可讀解說牌與播客可有介紹價值，但不偽稱為創作者字幕或實景拍攝。30 支通過；45 支有明確錯綁或完整既有證據顯示不符合有效介紹收錄規則。
- 只新增 12 次 Gemini 原生短片段分析，指定範圍合計 860 秒。11 次輸出有效，1 次時間戳超出指定片段，原樣保留為無效證據，沒有猜測時間、修復重試或用它核准。短段沉默不能推論整支長影片都沒有介紹。
- 店家逐筆核對完整資料與五組關聯指紋；另補查官方店址、旅發局／商場店家頁、Wikidata 精度與政府餐飲資料集。新查得的地址不能代替精準分店與合法座標證據。政府資料集的微熱山丘匹配為南投店，不能套用台中店；三筆 Wikidata 座標精度為公里級，未採用。

本次實際更正 4 篇文章分類：九龍寨城公園與荔枝窩 HKTB 文章由 `zh-TW` 改 `en`；鎮國寺遊記由 `ja` 改 `zh-TW`；崇禮門繁中維基頁由 `ko` 改 `zh-TW`。影片語系及所有創作者標題均未改寫。

主審使用內建瀏覽器實際核對 HKTB 英文正文及 Taipei Travel Geek 三創段落。另發現 `zh-cn/CLAPPER_STUDIO` 會轉至一般維基頁並顯示繁中：因此撤回原擬核准，仍維持 `zh-CN` 待審，沒有擅改來源網址或猜測分類。

## 正式站驗證

使用既有正常介紹審核處理器，逐筆鎖定並檢查原始完整指紋。僅允許審核欄位與 4 筆明確語系變更；不是直接任意改表。

- 新增 443 筆本批審核回條、188 筆正常介紹審核紀錄；店家更新紀錄 0 筆。
- 709 筆既有相關 audit 保持不變，未重播前批操作。
- 全部店家及來源／類別／食物／平台／風格關聯不變；92 筆保留文章影片的完整資料不變。
- 所有介紹的來源 URL、創作者、原始標題、縮圖、發布時間、觀看／點擊數與其他非審核欄位不變；公開排名未使用 AI 分數。
- 五語公開查詢：新增可見 `en=7`、`ja=1`、`zh-TW=32`、`ko=0`、`zh-CN=0`；待審／退件洩漏均為 0。
- 內建瀏覽器正式站抽查「蓮池潭」顯示 0 篇文章、2 支影片，包含本輪核准的 `c7a4342f-4066-4645-aff2-6bd77938de6a`。核對顯示與原標題，沒有點擊外連增加創作者排行開啟數。
- 獨立最後集合檢查：待審介紹 92、店家 163，完全等於本批保留項目，新增／遺失 ID 都為空。
- 所有 8 個應用服務 image 仍為 `b675f5d34a353eddfb789a953968c3c6d45eac4a`；API／web running、restart 0，readiness 200、PostgreSQL／Redis 正常，schema `0063_destination_offers`。

全站介紹目前為文章 1,373 核准／428 退件／59 待審，影片 746 核准／232 退件／33 待審。店家維持 273 核准／3 退件／163 待審。

## 成本與剩餘缺口

新呼叫的 12 份結果與 12 筆 request audit 一一對應；全部 request/result 指紋及重建 request payload 一致，沒有隱藏重試。

- Gemini 回報：56,493 input + 3,323 output = **59,816 tokens**；未知用量 0。
- 應用內每日 Gemini 計数由 477 增至 489／1,000，餘 511；Google 計費日期為 `2026-09-08`。
- Brave 搜尋計數仍 30，YouTube 搜尋計數仍 80，未新增這兩者的探索呼叫。
- 未調高配額、購買服務、申請 API，沒有扣會員使用次數；token 數不是帳單金額，也不宣稱帳戶層級用量與本站計數完全相同。

仍待補證的店家主要缺口為精準分店／地圖身分、可持久保存的獨立座標來源、直接店家來源；部分另有分店不明或暫時關閉。各缺口相互重疊，不能相加當作店家總數。保留的 59 篇文章與 33 支影片仍有存取限制、語言／片段證據不足、轉址／重複來源或重要實用資訊待核對。這些項目沒有硬核准，也没有把不確定當成錯誤退件。

## 保護措施與測試

套用前新增 PostgreSQL custom-format 備份：12,908,558 bytes、權限 `600`；兩次核對 SHA256 及 `pg_restore --list`。備份只保留在受保護主機，不匯出資料庫或憑證到 repository。

| 證據 | 指紋 |
| --- | --- |
| 新備份 SHA256 | `82c7604bbac7eac0b0e597b17685a2b002d9e2e9b54d27b1eb188bd816fef5fb` |
| 原始 443 筆快照集合 | `e0ef9835bec07e55553b08275a769b1f426c4c29b8c26ef1d5847b5e7bd175fb` |
| Fresh preflight baseline | `cb8c14d63dcb98927e2dd2a93316ffa1429b9906c9a4303a1f9a055f379887bb` |
| 本批 manifest 語意指紋 | `f1ff565837229d70ba1398f137b81c4b48d3b262e79f12bb64b060e0d5cfd574` |
| 本批 manifest 檔案 SHA256（LF） | `fcd3541f21d1b35ecadf252d0db46a0efa0456f6bb028b91b945711adb3adfdb` |
| 獨立 postflight artifact | `1e0db19b381bda7399333705328c90f00ac0f1a18f162e30dd4efe8e69693e27` |

驗證：

```text
pytest tests/test_catalog_content_review_followup.py tests/test_hotspot_guides.py tests/test_catalog_review_scope.py -q
50 passed

ruff check tests/test_catalog_content_review_followup.py
All checks passed

private test_contracts_followup.py: 13 passed
private test_video_clip_contracts.py: 6 passed
fresh read-only preflight: passed
one-shot guarded apply: exit 0, 445 log lines
independent production postflight: passed
```

資料與文件操作，沒有產品程式、UI、migration 或翻譯變更，因此未重跑無關的 production build／全套 Playwright。正式來源與公開列表已按上述範圍實際核對；不得把這些檢查說成全站重新部署或完整前端回歸。

從最新 main 的隔離 `codex/content-review-evidence-followup` 工作樹作業，保留原始 dirty checkout。證據與測試保留於本機 commit；本輪沒有建立 PR、push、merge 或 deploy。
