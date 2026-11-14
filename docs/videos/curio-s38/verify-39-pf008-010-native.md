# S38 R8n｜下一批首張原生圖即停畫

2026-10-21 UTC. **`pf008` 人工 REJECT；`pf009`、`pf010` 沒有開畫。** 依 [verify-38 的三張上限建議](verify-38-next-art-preflight.md)，我只逐張開始第一景；第一張即出現嚴重人物與時代漂移，因此立刻停止試批。這不是三張圖的完工驗收，也不構成整集分鏡 PASS。

## 版本與執行範圍

- `video.json` SHA-256 在執行前後皆為 R8n `df05f4a886abfe18018a85db948623cfe96537940c5ed7cf1f71461752bb1e35`；沒有改 prompt、旁白或 `look.preset`。
- 執行前原 manifest SHA-256 `6b5dc979515318a99e17faf8191d60f3e084d4d9755edf4fc99c4c716dcd010f`，已另存私有 `review/r8n-pilot-pre/manifest.json`，避免後續重試失去先前五格證據。現 manifest SHA-256 `a50d8795dbc22965784aedb7d2ed72853ea549b73839ee400c46f071597aa15e`，新增 `pf008` 的**機器選定**條目；人類退件判定只在本回條，不能把機器條目當成最終收圖。
- 唯一付費指令是 `keyframes --slug curio-s38 --shot pf008 --takes 1`；私有 STOP 僅在該指令期間暫移，外層 `EXIT` trap 已恢復。`pf009`、`pf010` 沒有圖像或 judge 呼叫。

## 原生圖判定

直接打開 1280×720 原始 `keyframes/pf008-1.jpg`，SHA-256 **`8981e6d57361c0539c5a7efd4f1a08ca0390752ffdcffd2537503e02d5ac13cd`**。畫面中央是一個明顯兒童模樣人物，背後另有多個孩子模樣的臉；主角穿近似東亞交領短衣，左方有紙格窗。這不符合 prompt 所寫的 **one** 1666 年英國成年 householder 在樓上窗邊判斷遠處火光，也會使觀眾誤以為日記人物與地點在東亞。遠方紅光與黎明時序存在，但不能抵銷人物、服裝、地點的重大矛盾。**人工 REJECT，不得進成片。** 原圖及裁邊圖已各另存私有 `review/r8n-pilot-pre/`，防止日後相同目標檔名被覆蓋。

機器 judge 對裁邊圖報 **9.29／10、`passed=true`、`needs_review=false`**，stamp `fc30c129a30c2a34`；同一份 judge 明寫 `details=7`、`East Asian style clothing and shoji-style window lattice appear instead of 17th-century British attire and architecture`。因此機器 PASS 不能用作歷史畫面的最終收圖。裁邊圖 SHA-256 `dfd8c46619307e79bc629942528c37410fb829794e7dc551cff81b56ce53c955`；它沒有修正人數或時代服裝問題。

## 帳本與下一步

私有 ledger 由 **US$0.3400／20 image／19 judge／1 music** 增至 **US$0.3535／21 image／20 judge／1 music**；仍有原 `pf003` **US$0.0035 reserved**、共 1 reservation，沒有新 reservation。整集原硬上限 **US$4.58** 不變，`STOP` 現在存在。工具的 contact sheet 因本容器 Playwright Chromium 不可用而沒產出；這不影響我對原生 JPEG 的直接檢視，也不表示整片 storyboard 已可審。

先修 `pf008` 的主體成年與 1660s 英國服飾／窗形提示詞，避免把泛稱 `householder` 和後置的成人附句交給模型自行解讀；再由非作者對精確 prompt 差分和史料做書面核對，才可在既有上限內做**一張**定點重試。`pf009`–`pf010` 也應先按這個失敗模式檢查，切勿直接續跑三張或全片。本站音訊／分鏡卡、30.20 秒開場停頓聽感、品牌片頭片尾、QA、Shorts 和 Studio 連結仍待驗收。
