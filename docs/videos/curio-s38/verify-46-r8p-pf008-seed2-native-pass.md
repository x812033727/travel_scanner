# S38 R8p `pf008` seed 2｜原生圖驗收 PASS，僅本鏡

2026-10-22 UTC。依 [有界復原方案](verify-45-pf008-recovery-paper.md)，只補畫 `pf008` 的 R8p seed 2。**機器評審 10/10、直接看原生圖後人工 PASS；沒有啟用第三張文字卡退路，也沒有放行整集分鏡或後續插圖。**

## 執行與保全

- `video.json` 執行前後 SHA-256 均為 `8db80e07bffff8863f949e4a458b9fed0a891e36ed93063bce59c3915fc6e142`；`look.preset` 仍為 `cute-mystery`。私有 `STOP` 在單次命令期間暫移，外層 `EXIT` trap 已恢復，目前存在。命令只對 `pf008` 執行 `keyframes --slug curio-s38 --shot pf008 --takes 2`，沒有 `--force`、seed offset 或別的景。
- 執行前的 `STOP`、manifest、R8p seed 1 原圖及裁邊圖、ledger 已複製到私有 `review/r8p-pf008-seed2-pre/`。前 manifest SHA-256 `0b9922a9af832df87b5a9ee18a542be679c3a14e4d4f91b0ef6c8eeb2fc8951c`；新 manifest SHA-256 `39dd823c0763f599bdeb5a76af6a3d5ad9f8eedda1e87b1d8b9e415f4a946b6c`。Manifest 的 `pf001`–`pf005` 五格逐物件比較完全相同，只有 `pf008` 更新；`look_hash`、`visual_hash` 均未變。
- 新 1280×720 原始 `keyframes/pf008-2.jpg` SHA-256 `011198201d2bec90858cce6a4a535abef144827578ca1e77ae24c74bfa5c566b`；入選裁邊版 `keyframes/pf008-2-trim.jpg` SHA-256 `8e08ff956a0f64c4243e584dc870acbfaa8ab4e77b18cabab809e42aabd03418`。Manifest 選 seed 2，`needs_review=false`；seed 1 的 9/10 FAIL 記錄仍保留。命令只新增 **1 image／1 judge**，未出現新 `pf009`／`pf010` 圖。

## 看圖與史料判斷

原生 JPEG 顯示**一名看起來已成年的男子**在暗室中向木框窗外看；他的衣物是寬鬆、可辨識為外披睡袍的淺色長衣，非前張的現代羅紋運動衫。人物與場景採系列的平面卡通線條及色塊，窗外紅光落在遠處屋頂後，沒有畫出精確起火屋、已證實的馬克巷位置、第二個人物或現代器具。這符合 [9 月 2 日日記](https://github.com/GITenberg/The-Diary-of-Samuel-Pepys---Complete_4200/blob/68fcf49f70ee793b989a6fd0464264d55beb4451/4200.txt#L65795-L65803)所能支持的「披睡袍到 Jane 的窗邊，以為火還遠」示意。木窗格與衣色不當成日記記下的細節。

原生圖頂、底有窄的均色邊；工具記錄 top 3.8%、bottom 1.4%、左右各 7.8% 的紙邊裁切。**實際入選的裁邊版**已去除均色邊，畫面沒有前張的黑色電影寬帶。原圖與裁邊圖均直接檢查；這次接受的是有清楚來源邊界、最終無黑邊的入選畫面。機器九項全 10、`passed=true`、無 problems，只作輔助證據，不代替上述人工核圖。

## 帳本與接續

私有 ledger 由 US$0.3670／22 images／21 judges／1 music，變為 **US$0.3805／23 images／22 judges／1 music**；舊 `pf003` 的 US$0.0035 預約仍另記，未改 US$4.58 整集上限。`STOP` 已恢復。下一步可另按既有來源與人像風險**單獨**評估 `pf009`、`pf010`；本回條不自動解鎖全批，也不代表站台音訊／分鏡核准、正式片頭片尾、可點結束畫面連結、字幕、Shorts 或整片 QA 已完成。命令另報 Playwright Chromium 未安裝，故這次沒有產生聯絡表；單鏡驗收依原圖和 manifest 完成，後續分鏡關卡需補齊聯絡表。
