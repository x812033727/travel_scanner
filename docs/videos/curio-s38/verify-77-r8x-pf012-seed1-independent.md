# S38 R8x｜PF012 seed 1 原圖獨立覆核及單張重試紙審

2026-10-22 UTC。**現有 seed 1 圖 HOLD；僅 seed 2 的單張重試 PASS-on-paper。**此為非作者目視與紀錄覆核，沒有 image／judge／music 呼叫，亦未接受圖或放行 storyboard。

綁定 `video.json` SHA-256 `23f0662b96ba290494b044f2cdce037ba011b5222a1137d5a38b0a5e25600615`，PF012 image key `c7125ef4895d1925`，look hash `98a370ae40badbaf`，visual hash `ca70ce11119245ed`。新原圖 `keyframes/pf012-1.jpg` SHA-256 `ddf0f076cbfddc21276a126fb703aa51dcf3cc504495ce6428ad75039be43230`；入選裁圖 `keyframes/pf012-1-trim.jpg` SHA-256 `931ee1646fbd062322006de19b3a94dd51d9119583368cd6820de677bdebeff2`。兩張均已實際目視：畫中一位成年人在木門邊，暗色斗篷已穿好且領口扣妥，一手近胸、另一手扶門，沒有清楚呈現把斗篷往身上拉的動作。服裝、四肢與系列畫風沒有另見明顯違例，但主動作不可因此視為通過。

正式 judge stamp `40338aed8309ae8e`，9.71／10、`passed:false`、`subject:0`；明示 `The man is standing at the doorway already wearing the cloak instead of putting it on → show the man actively pulling on his cloak`。manifest 把 PF012 標為 `needs_review:true` 並列出同一機器修正。這個退件與原圖目視相符；不得使用 seed 1 或把舊 key `288d3959fc175dd9` 的通過判分搬到現版。manifest SHA-256 `05963cb8ba139a23588608d28ea36a2a6ef4ea003b7a17166b68daa25a169e90`，其餘 10 張既有 KEEP 不涉及本次重試，PF015 是來源引句卡而非舊退件圖片。

固定 Pepys 日記 1666-09-02 原文 SHA-256 `3cd43a3c39ee72eb9c4a3657f1fcb1723afba291cedac176c65a39289483be5d`、L65804–65808 的 `made myself ready presently, and walked to the Tower` 支持 PF012 畫面中的出門準備。原提示詞已要求成年男子 `pulls on a plain dark wool cloak`；機器修正 `show the man actively pulling on his cloak` 只把既有動作畫清楚，沒有新增史實主張或超出原場景。可依既有流程只試 **seed 2 一張**及其一次正式 judge：使用當前 R8x 提示詞、look、`push in`、相同模型和機器修正，不手改腳本／事實／其他圖。`--shot pf012 --takes 2` 會略過已判的 seed 1 再畫 seed 2；不得用 `--force` 或自動延伸 seed 3。

此刻 `STOP` 存在且 jobs 空；ledger SHA-256 `1f84217279e8a7879937965fada714e9c36235ba00212b3fd469472339e6a5a9`，累計 **US$0.728／48 image／48 judge／1 music**，另保留 US$0.0035。按本次實價每 image US$0.0035、judge US$0.01，再試一張後累計約 **US$0.7415**（連現存 reservation 約 US$0.7450），低於已核准整集 **US$4.58** 上限及三張種子上限；執行前仍應核即時報價、額度、STOP 與 jobs。恢復 STOP 後，應目視 seed 2 原圖與裁圖、查正式 judge、重驗 ledger／manifest／十張 KEEP；若仍未通過，停下再做獨立判讀，不自動續畫。PF019 仍待原圖，全片 storyboard 尚未放行。
