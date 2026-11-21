# S38 R8p `pf008` 原生圖驗收：REJECT，停止本批

2026-10-22 UTC。依 [R8p 獨立書面 PASS](verify-43-r8p-pf008-independent.md)僅定點試畫 `pf008` 一張；**原生圖片與機器評審都未通過，未續畫 `pf009`／`pf010` 或其他景。** 本回條不放行整集分鏡。

## 版本與執行

- `video.json` 試畫前後 SHA-256 均為 `8db80e07bffff8863f949e4a458b9fed0a891e36ed93063bce59c3915fc6e142`。僅執行 `keyframes --slug curio-s38 --shot pf008 --takes 1`，帶 `NODE_USE_ENV_PROXY=1`、`VIDEO_WORKDIR=/workspace/.video-work`。私有 STOP 只在這支指令執行期間移開，外層 EXIT trap 已恢復；目前 STOP 存在。
- 舊 R8n manifest SHA-256 `a50d8795dbc22965784aedb7d2ed72853ea549b73839ee400c46f071597aa15e` 及舊 `pf008` 原圖 SHA-256 `8981e6d57361c0539c5a7efd4f1a08ca0390752ffdcffd2537503e02d5ac13cd` 在重試前複製到私有 `review/r8p-pf008-pre/`。新 manifest SHA-256 `0b9922a9af832df87b5a9ee18a542be679c3a14e4d4f91b0ef6c8eeb2fc8951c`，`pf008.needs_review=true`；機器沒有通過圖可入選。
- 新 1280×720 原始 `keyframes/pf008-1.jpg` SHA-256 `b272bbcb59e96eee2c5a7c0706c0d7265b5761714c5eeccc2c35ec011e5c926b`；裁邊版 SHA-256 `529cad5e67920ebcd24fcc49f4b6903e2a6d014630102be7199000e7d0f8aff7`。原圖、裁邊圖、前後 manifest 都留在上述私有備份目錄。

## 直接看原圖

人物現在有明顯成年的臉與鬍鬚，窗外紅光保持遠距離，這兩點比 R8n 的東亞兒童圖改善。但整張呈現 3D CGI 光影和材質，頂、底有寬黑邊；人物穿著帶羅紋袖口與領口的現代綠色上衣，辨不成日記中剛披上的 1660 年代睡袍。**人工 REJECT：畫風與服裝都會誤導，不能進成片。** 這不是因為卡通比例或少量裝飾而退件。

機器對裁邊版報 **9.00/10、`passed=false`**，`style=0`（3D CGI 而非本系列平塗 2D）、`details=7`（現代 sweatshirt 而非 1660s nightgown）；`frame=10` 雖未抓到黑邊，原圖仍有清楚的頂底黑帶。輸出的建議修正含畫風用語，但系列 `look.preset` 已固定；不能直接把風格字塞進單景 prompt 冒稱通過。

## 帳本與交接

私有 ledger 由 US$0.3535／21 images／20 judges／1 music 增為 **US$0.3670／22 images／21 judges／1 music**；原 `pf003` US$0.0035 預約仍在，沒有新預約。整集 US$4.58 上限未變且未超支。`pf001`–`pf005` 既有圖未重畫；`pf008` 在 R8n、R8p 各一次原生圖均 REJECT。下一步須依既有圖片的年代與畫風樣張提出新的局部構圖／服裝方案，另人先核精確史料及 prompt 差分，再以剩餘嘗試次數單景驗圖；本回合不再付費重試。網站音訊／分鏡審核、開場銜接實聽、品牌片頭片尾、整片 QA、Shorts 與 Studio 可點連結仍待完成。
