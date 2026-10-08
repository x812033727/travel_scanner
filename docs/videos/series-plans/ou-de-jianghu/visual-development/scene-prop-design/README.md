# 第一集場景、道具與受控細節參照

2026-10-08。**已生成並實看：29 張最新候選 PNG，40 張原始輸出保留。** 包含 17 張主要空景、2 張光線／事件狀態空景、7 張道具板、3 張受控局部卡。圖片均由內建 imagegen 製作，不是以 HTML 或清單代替圖片。

使用者接受的原話是「保留目前華麗古裝與細緻人物風格」，只代表共同畫風方向。此包每張圖仍是 candidate；**沒有逐圖採用、正式 look 匯入、動畫穩定性或開拍核准**。主劇本、production 設定與其他任務持有人的檔案未改；沒有呼叫其他付費影片供應商。

## 使用入口

- [空間、鏡位、出入口與光色卡](scene-cards.md)
- [道具數量、持物左右與狀態規則](prop-continuity.md)
- [455 鏡來源索引與連戲清冊](shot-props.json)：每鏡保留 source pointer、原 prompt／motion、空間、道具文字命中、角色攜物核對項及重要狀態；4 張字卡另列。文字索引不等於逐影格 QA。
- [逐圖實看紀錄](review.md)
- [媒体來源與 SHA-256](media-receipt.json)、[完整生成 prompt](prompts.json)、[原始生成工作紀錄](generation-worklog.json)、[機械驗證](verification.json)、[路徑可攜化與媒體未變驗證](portability-verification.json)
- [可重跑整理器](build-artifacts.mjs)、[19 路棋局位置提案](go-layout-proposal.json)

所有媒體以單集工作目錄 `<VIDEO_WORKDIR>/ou-de-jianghu-e001` 為根。圖片與可點選原圖的並排圖廊位於：

```text
scene-props/20261008/gallery.html
scene-props/20261008/<asset-id>-v<version>.png
scene-props/20261008/go-layout-before.svg
scene-props/20261008/go-layout-after.svg
```

這是單集工作目錄相對路徑，不是 repo 相對連結。重跑整理器前，將 `OU_DE_JIANGHU_WORKDIR` 設為實際單集工作目錄，`IMAGEGEN_ORIGINAL` 設為本機原始生成圖的根目錄；公開收據與工作紀錄只使用 `<VIDEO_WORKDIR>/ou-de-jianghu-e001/...`、`<IMAGEGEN_ORIGINAL>/<thread>/<filename>`，不含個人絕對路徑。含真實本機路徑的工作紀錄另保留於單集工作目錄的 `scene-props/20261008/generation-worklog.local-paths.json`。40 個來源 PNG 保留於 imagegen 原始目錄，另逐檔複製至工作目錄並比對 SHA。尺寸由實物 PNG header 讀取於 receipt，不聲稱達到其他文件的 2048 級編輯尺寸。

## 用圖順序與限用範圍

1. 先按 shot-props 的 location 和光線狀態選空景，再依實際鏡頭文字放角色。空景中的無人、無兵器不表示劇本人物或道具刪除。
2. 角色臉、冠、服裝以同輪角色參照選定的一套母版為準；本道具板處理本集的形狀與狀態。扇墜、刀鞘細紋不能兩套各自採用。
3. 只有特定鏡使用月牙、金印或黑風卡。它們不進一般 neutral／正側背畫像，不揭第 8 集尚未確定的答案。
4. 空間 B 圖有些實際輸出為同側近角／俯角，不是 180 度反打；詳見 scene-cards。不能把鏡面翻轉當新鏡位，也不能用兩張相似畫面宣告建築幾何已鎖。
5. 生成棋盤只供木材／器形參照，其格線與落點不可信。附加 SVG 有精確 19×19 交線和合法交點位置，但點位仍是編輯提案，需選定後綁首尾格；沒有偷改劇本棋局。
6. 客房 `chess-guestroom-master-v3`、`chess-guestroom-angle-b-v2`、`chess-guestroom-cold-v2` 三圖的紙窗仍有淡月輪／透景殘影，只作空間與光線提案，不能准用作紙窗近景（CU）母圖。冷態圖僅適用翻盤後的 `a05-s031/s035/s042`，不能當 `a05-s023` 初入房同態首格。

仍須在關鍵影格／小樣階段解決的具體項目已寫入 [review](review.md) 和 [prop-continuity](prop-continuity.md)，本包不以「已產生素材」替代這些關卡。

## 來源

[實際 e001 video.json](../../../../ou-de-jianghu-e001/video.json) 和 [script.md](../../../../ou-de-jianghu-e001/script.md) 是鏡號、狀態與物件數量依據；[cast](../../production/cast.json)、[cast-notes](../../production/cast-notes.md)、[setting](../../setting.json) 約束身份與保密；[既有分場](../episode-plan/scene-and-pilot.md) 提供九處空間的整理。7 份直接來源 SHA、9 角色 appearance pointers、25 個生成參照輸入 SHA 都存於 receipt。場景燈光不寫進全域角色 style。
