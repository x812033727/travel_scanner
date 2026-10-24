# 清邁／清萊交通校正：2026-10-24

兩篇既有 zh-TW 攻略與 SVG 已準備同步校正，尚未發布。Greenbus 2026-10-09 官方文章指出適用班次由清邁第 3 巴士總站（Arcade）至清萊第 1 巴士總站，單程通常約 3–4 小時，實際站點仍須核對車票。[業者官方來源](https://web.greenbusthailand.com/en/news/43)

正文、交通表、FAQ、SEO 描述、圖解文字及無障礙描述同步採用該範圍；6–8 小時僅為巴士來回的估算，另留等車及進出站時間。包車／一日遊時間依行程安排。未將巴士時間套用至包車，未宣稱一天只能看兩個景點，未插入未取得的固定票價。

原有景點事實保留。第二輪抽查白廟官方頁仍列 200 泰銖與 08:00–17:00；黑屋頁沒有票價欄，因此保留票價未知。[TAT 白廟](https://www.thailandtravel.or.jp/white-temple/)、[TAT 黑屋](https://www.thailandtravel.or.jp/baan-dam-museum/)

## 審查與驗證

- 撰稿：`remaining_decisions`；第一輪：`travel_independent_review`；第二輪：`codex-root-second-travel-review-20261024`，三者不同。
- 第一輪修正包車時間推論、硬性景點數限制、SEO 舊車程與官網仍不可用的舊說法；因超過三項事實問題，依 content-pipeline 完成第二輪，兩輪均讀回各輪凍結雜湊；其後僅五欄日期更新，另經原始 bytes 比對覆核，最終雜湊如下。
- 兩篇 GuideDocument/schema 與 lint 實際 exit 0；清萊零問題，清邁既有 `no_summary` 警告保留。兩張 1600×900 PNG 已渲染並由作者與兩位覆核者目視檢查，新標籤完整；PNG 僅作外部 QA，未新增至網站素材。
- 新增業者來源與真實查核日期；其餘來源、有效期限、相關文章與非交通內容保留。26 個 open PR 無精確路徑衝突，相關工作目錄精確路徑狀態已確認乾淨。
- 先前失敗的 Edge 渲染、資料結構與來源上限檢查紀錄保留在外部工作區，未改稱通過。
- 安裝後內容包測試：9 passed／5 skipped，實際 exit 0。

## 公開版與目前草稿比對

發布前唯讀比對發現，公開版比 repository 原稿更舊：清萊為 v4，清邁為 v8。經 GuideDocument 正規化後仍有 2／4 處差異，原先「等同基準」檢查如實失敗，沒有直接覆蓋正式內容。

追加的正式版差異覆核確認這些是 repository 已有、尚未發布的有效修正：清萊玉佛寺 07:00–17:00／免費；清邁機場到塔佩門約 15 分；Grab 預先顯示車資但不含過路費與附加費；借圍布只限部分寺院且可能收費、服裝不符仍可能拒絕入場。SEO 改寫僅濃縮既有內容。五個官方頁均於當日讀取成功，這些既有修正可明列納入本次發布計畫。[TAT 清萊玉佛寺](https://www.thailandtravel.or.jp/wat-phra-kaew/)、[TAT 塔佩門](https://www.thailandtravel.or.jp/tha-phae-gate/)、[Grab Transport](https://www.grab.com/th/en/transport/)、[TAT 寺院禮儀](https://www.thailandtravel.or.jp/visiting-temples/)

正式資料庫另以 READ ONLY transaction 讀回：兩篇僅有 zh-TW 列，草稿與公開指標一致，沒有較新的未審草稿；清萊版本 4／文章分類版本 3，清邁版本 8／文章分類版本 2。發布前必須再次核對版本與以下正規化雜湊，漂移即停止。

另將最終兩份 ArticlePack 直接傳給正式容器現有的 `plan_import`，以 READ ONLY transaction 執行並 rollback，實際 exit 0：恰為這兩個 slug、各一個 zh-TW `update`／`publish: true`、兩篇 `taxonomy: unchanged`，沒有 create、其他語系或發布保留。這是實際資料庫的限定 dry-run 計畫，未呼叫寫入函式或落地暫存檔；發布時仍須重跑並比對。

| slug | 目前草稿與公開內容 SHA-256 |
| --- | --- |
| chiang-rai-2-day-itinerary | `9d0e98e97f2c9e8a2a7ab355d9f6e901316f0541c801c96fa83619e30f948a11` |
| chiang-mai-3-day-itinerary | `98ea11c46e22f21322b8f39c2e246d85948037577b3d01cb18e3687b8c379cf2` |

| 檔案 | 最終 SHA-256 |
| --- | --- |
| chiang-rai-2-day-itinerary.json | `fd9b99e55222e79792d665d08d063cc61e407ef770595bcac5700a7f4239181e` |
| chiang-mai-3-day-itinerary.json | `b595bb6485e27062261b4b3713f57485a04dfeaeb1d3b179869190c3e112c3be` |
| 清萊 diagram-1.svg | `685684c7c8b58b5087dfadb31efec98a1f0fb7c6e20c7a8495921077096bd173` |
| 清邁 diagram-1.svg | `c76a170bbc82ec8cdbf3a38e7630abcfd12cd319624c156fcaaa7bb86e7c3688` |

## 尚待完成

原維護票繼續 open：正式發布仍需核准、部署後兩個 slug 的限定 dry-run／publish 與公開讀回。Greenbus 實際票價依出發日期／車等查詢；其他已恢復頁面尚未提供可驗證費率，不補假定數字。未執行正式站寫入、部署或發布。

五個當日實際讀取的來源 checked_on 最後更新為2026-10-24，清萊1欄、清邁4欄；不同代理驗證其餘JSONbytes、URL、順序與SVG/PNG完全不變。日期增量後schema/lint再次exit0，舊稿雜湊與五欄差異證明均保留。
