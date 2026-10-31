# S53 R37｜`s53029` 第三張原生圖候選獨立書面覆核

2026-10-22 UTC。**PASS，限 R37 現行 `s53029` 提示詞、運鏡與 claims 畫面註記的紙審。**我不是 R37 作者；我直接核對固定史料、兩張未裁原圖、可逆差分、口播及私有停線狀態。本 PASS 不是第三張圖的 KEEP，也不是重新回綁圖單、解除 STOP、購圖或發布的授權。本次沒有改動私有媒體、付費呼叫或 Git 暫存。

## 固定來源與畫面界線

1913 年 *San Francisco Relief Survey* 固定文本 `/tmp/s53-sf-relief/56217-0.txt` SHA-256 `d627ed287d8a93b9c00225ea47dbdc4f97c36089a890192a602b993c3c185b72`，[D L4858–4865](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L4858-L4865)記 1906 年 9 月 10 日開始興建，9 月 16 日漢密爾頓廣場 **20 棟小屋完成**；但其後至少兩三個月，才有相當數量房屋備妥供難民使用。既定口播「六天後，漢密爾頓廣場先完成二十棟。」符合原文的日期與完成數。史料沒有指認木匠、門框測試、房屋實際外觀或 9 月 16 日誰入住；「相當數量尚未備妥」也不能推成當日 20 棟全部無人使用。

我以原尺寸直接看了兩張 **1280×720 未裁原圖**：R35 私有備份 `r35-s53029-first-native-rejected-original.jpg` SHA-256 `6652f9899e861d54fdba6407f658e019280faaadeed7dc2690b993e8dc82e112` 是童貌人物站在暖光門內，整片屋立面與窗戶可見，容易暗示當日孩童住用；R36 私有備份 `r36-s53029-second-native-held-original.jpg` SHA-256 `e1d4dd5aec3b4a563252b9c458aa1f9e42e9992138f0e67423e1534e9829837b` 是灰髮但臉與比例有童貌歧義的全身小人物，閒站門檻，一手靠胸，另一手部分靠框，看不出兩手分別接觸門柱與門邊，更看不出測試縫隙。R36 19 景封存 manifest 對本景仍是 `needs_review=true`，機器 **9.0／10、`passed=false`、`subject=0`、`details=7`**；這些動作與構圖缺口在原圖可見。先前人眼對 R36 年齡和可用性有分歧，不把它改寫成一致退件或一致通過。

R37 精確改成屋外胸上特寫：一位短灰髮、灰眉、灰鬍、有額紋面紋的明顯中老年成年木匠，雙手分別按住垂直門柱與半開門邊，目視可見窄縫；只留暗且空的室內及一條木板牆，裁去腿部、全門、屋頂和屋立面。`camera` 由 `pan left` 改為 `push in`，服務於接縫的近景。這直接針對前兩張的童貌／入住暗示與 R36 的閒置、全身取景缺口，沒有增添史料沒有的住戶或當日使用敘述。`claims.md` 同列明說木匠、屋型、驗框工序只是**原創概念示意**，不把單個門框說成 20 棟逐棟的存世畫像。依 Curio 的概念插圖界線，這版文字與來源相容；新圖仍須看未裁原尺寸，不能把提示詞當作已成圖事實。

## 版次與停線核對

R37 現行 `video.json` SHA-256 `7df8145a61b6ef66d3c65d75e89ea85aa30b6ec28fec217c114e7a05a81d59b6`、`claims.md` SHA-256 `50704b954f87256796a9690ef47b12e0bcd0491633ad2645cf9b3e6e310e07b3`、[精確差分](r37-s53029-final-mature-hands-on-jamb-structured-diff.json) SHA-256 `51dc910b9f51f8ec18bc4e6da29cebafa1d1ba4ea1787d4ee2b6ae6669f0bb65`。差分的 `after` 完整場景及 claims 整行各與現稿吻合且只出現一次；以差分 `before` 反填並按現有 JSON 格式序列化，**逐位元組**重現 R36 `video.json` SHA `601b54f492cb38ddf046f200f6bb02097868e25b9217605d2661abc33c1aa49e`、`claims.md` SHA `0795312a9584486511f8695faeee7dda73863fd5ca64f705da99da5ccba6a745`。124 景中只 `scenes[22]` 的 prompt／camera 有變；126／126 口播句 ID、文字、語氣及其餘場景不變，`script.md` SHA `64ffcd8c0e89c4596a7fd08d41bd74f8a16f55fbc9acc2f41d7f9b914ea300fc`。用正式程式重算 R36／R37 `speechHash` 均為 `05c4d9a79a8708b4`，同私有 timeline；R37 `visualHash=eb73bd967a3b4a7d`。實跑 `VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s53 --json`：exit 0、**0 errors／0 warnings／126 lines**。

正式 `keyframes/manifest.json` SHA-256 `deae00309dd2e438ad4f20252f6a8e3178432f15a6fb967350aeba0db27142a7`，仍綁 R36 `visual_hash=7a88c3a7a90cc951`；**18 張 KEEP** 均 `passed=true`、`needs_review=false`，18 個所選檔案 SHA 全對，且沒有 `s53029`。帳本 SHA-256 `acbe13e67db05424cbad7e252578fc8a5dd7bac5f04b38a2783ef1d3f6bc235b`，逐筆合計 **US$0.6615／50 image／49 judge／0 預約**；`jobs.json` 為空，`STOP` 在位。R37 尚無第三張成圖。若受控生成第三／最後一張，仍須獨立核機器與未裁原圖的成人辨識、兩手接觸、接縫、完工而非入住訊號及系列 2D 畫風；若退件，改考慮同章已收圖或來源卡，**不買第四張**。
