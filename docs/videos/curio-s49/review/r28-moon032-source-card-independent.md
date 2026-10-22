# S49 R28｜`moon032` 來源字卡獨立紙審

2026-10-22 UTC。**R28 窄修 PASS；整集 storyboard 仍 HOLD。**本審只核對固定史料、字卡與旁白、可逆差分、系列比例及既有私人媒體證據；沒有生圖、judge、重綁圖單或其他付費呼叫。

## 來源與畫面

固定的 Locke 名下 **1859 重印本** `/tmp/s49-moon-hoax-62779.txt` SHA-256 `3ca0bc9b6fc5c50b090d61bf2049e925d22dd1cdef2b443a282f7fdc5749e654`，[L398–413](https://github.com/GITenberg/The-Moon-Hoax-Or-A-Discovery-that-the-Moon-has-a-Vast-Population-of-Human-Beings_62779/blob/ce684a827afd854e0843679fe4568fcaeeb12ae7/62779-0.txt#L398-L413)寫虛構 Herschel／Brewster 對話：舊式無鏡筒望遠鏡的物鏡置於高桿，焦像投向遠處；Brewster 說若將焦像送進暗室、由反射鏡承接，就不需要鏡筒。Jacoby 的 **1902 後出評論** `/tmp/s49-jacoby-53396.txt` SHA-256 `f5ab32e64e7ea3735ff90fb000ae8cc82dddea594e0de0c6be30b30f94485029`，[J4083–4125](https://github.com/GITenberg/Practical-Talks-by-an-Astronomer_53396/blob/073dd7dd24b8515dec681441a1cde79477fabf08/53396-0.txt#L4083-L4125)明稱這段為 *imaginary conversation*、光學術語拼貼。兩文支持「報導裡的構想」，不支持真實建造或實驗。

`moon032` 原旁白「兩人想讓物鏡架在高處，把焦點影像投進暗室」未改。新字卡同屏顯示「**1835 年報導的虛構構想／物鏡架高處，焦像進暗室／1859 重印本所載，非實作紀錄**」。主文概述 L 的方案，上下標同時標出虛構與重印來源；`claims.md` 同列也明說不是實際實驗、存世設計圖、1835 原報影像或 Herschel 設備。這修復了 [R27 原生退圖](r27-moon032-native-stop.md)把高處開口畫成落地門口、看不出「高處物鏡 → 暗室焦像」的問題，不再用那張圖作 KEEP。

## 差分與系列檢查

按 [R28 可逆結構差分](r28-moon032-source-card-structured-diff.json)逐字以 `after → before` 倒填，`video.json` 精確還原 R27 SHA-256 `02fdb0f2ac142634d42ac24f7108bb12424e7a4625756ca559b90d52912552a3`，`claims.md` 精確還原 R27 `779a8e22e6e7e202249cf7ec645a91a7ade7139c5c0e6ee2bb70c4fa50f2bd2f`；正向替換也精確得到 R28。現稿雜湊分別為 **`a4d00cdc41078cc016247127c5a3676bb8a8ee98699662395bd2cfdc1f4b62a2`**、**`b89b557b52bb98dd3e4d654b665e4cd874434784a5850d71044323c7543a44e3`**。解析兩版後只有 `moon032` 的 `template/data` 改動，該景 `lines`、其他所有 scene、章節與根設定都相同；claims 只有 `moon032` 的畫面欄改動。`script.md` SHA-256 **`82369f762cc64f70e300e2104a16af3b8e99f1e3296dd81a34152e967f0ecb0a`**，與 R27 位元相同。

`moon030` 是已收插畫，`moon031` 是先前獨立通過的來源卡，`moon032` 是本卡，`moon033` 回到插畫。`renderPlan` 對 `moon031/032` 均為 `kind=stills`，且兩卡的上標、主文和下標均出現在實際可見文字；`moon033` 仍是 `kind=clip`。正文 128 景有 **119 `shot`／9 `big`，插圖 92.97%**，最長連卡 **2** 景，符合系列至少 70% 插圖、最多 3 連卡的規則。`VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s49 --json` exit 0、**0 errors／0 warnings**、131 句；`git diff --check 299168d2f^ 299168d2f` 通過。

## 私人圖單與下一關

現行私人 manifest SHA-256 **`694b319ccaaf0da0e4ed9079620945b6b95588c5a95439ec2f89d8f5d8607615`** 仍綁 R27 `visual_hash=74c5cc0713c7766d`；R28 工具值是 **`dfe0bece015e7458`**，`look_hash=98a370ae40badbaf` 不變。manifest 恰有前輪 **26 個人工 KEEP** 條目，與 [R27 清單](r27-moon032-native-stop-inventory.json)的相應選圖路徑及 SHA 逐項一致，26 個實際選圖檔 SHA 也逐張吻合；`keyframeProblems` 對這 26 景為 **0**。manifest 無 `moon031/032/033` 條目，`contact_sheet=null`、`contact_sheets=[]`，不會選到 R27 `moon032` 退圖。

私人 `STOP` 存在，`media/jobs.json` 是空 job 物件，ledger SHA-256 `076a31adf1dd34d89a11ecc9a18c819bbaa7bec3164b56098fb1d5db4ebb9275`，合計 **US$1.0395／77 image／77 judge／0 預約**，低於整集 US$5.30 上限。本輪均未變。**允許在 STOP 下離線重綁 R28 `visual_hash`**：先備份現行 manifest，只換版本綁定，保持 26 個完整條目、選圖檔與 SHA 不動，且不得加入任何 `moon031/032` 退圖條目；再重核 26 景與帳本。完成重綁後，沿用 [R27 非作者 `moon033` 書面 PASS](r27-moon032-033-prompt-independent-pass.md)，可在既有授權與停批規則下只對 `moon033` 做有界付費原圖試驗，逐張看 1280×720 原圖及裁圖，人工決定 KEEP／REJECT。現行完整 `keyframeProblems` 仍有 **93 個未畫 shot**（由 R27 的 94 減去改卡的 `moon032`）；不能送完整 storyboard、宣稱畫面全通過或把機器 PASS 當人工 KEEP。
