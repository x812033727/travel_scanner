# S53 R27｜`s53024` 來源與書面畫面獨立紙審

2026-10-22 UTC。**PASS：僅限 R27 精確書面來源與畫面候選。**我沒有撰寫本輪修訂，也沒有修改 `video.json`、`claims.md`、任務或私有圖單，沒有重綁、購圖或送審。此判定允許下一位先安全離線回綁 15 張 KEEP、做即時預檢，然後最多試 `s53024` 第二張原生圖；第二張仍須直接看原尺寸，紙審不等於成圖 KEEP。

## 固定來源與畫面界線

獨立重開本機固定 1913 年 *San Francisco Relief Survey* `56217-0.txt`，SHA-256 `d627ed287d8a93b9c00225ea47dbdc4f97c36089a890192a602b993c3c185b72`。G **L4934–4941** 原文說：救濟公司準備建小屋時，向公園委員會詢問使用若干公園與廣場；委員會沒有授權權力，1906 年 8 月 17 日只同意一年內不干預使用，之後小屋須儘快移走。L4919–4920 明示此 Corporation 是 San Francisco Relief and Red Cross Funds。`s53024` 仍只說「於是它向公園委員會，詢問能否使用那些空地。」；詢問行為與對象均有直接支持，沒有把下一句的有限不干預說成正式批准。

本景新 prompt 是 1906 年舊金山救濟辦公室**廣景**：一名可見灰髮、面紋、未戴帽的中年職員站在桌旁，指向平放桌面的無字示意圖，圖上以粗線勾出公園與廣場地塊。`claims.md` 同列明說這是匿名原創概念示意，不冒充實際往返信函或存世地圖。史料沒有證實辦公室、職員、服飾或地圖實物；這些元素作為卡通化抽象場景可以接受，前提是成圖不出現具體偽造公文、批准、可讀地名或與 1906 年相矛盾的道具。既有 `cute-mystery` look 沒變。

我按原尺寸打開 R26 未裁 `s53024-1.jpg`（1280×720，SHA `6b170bea5df42c202cd8d0e45b4691a3bdece844024901691f196d91b97c2651`）及裁圖 `s53024-1-trim.jpg`（1280×720，SHA `1751c48ec90ca2eaa866b1b933f4e7f3ae7defd232f63bc4442db7da5d9235be`）。兩張均呈圓臉童貌、帶黃色標記的近代棒球式軟帽、手持完全空白紙；背景基本是桌面與牆板，沒有可辨公園地塊，也不構成辦公室廣景。裁去頂邊仍留同樣失配。故同意 [R26 停線回條](r26-s53024-native-stop.md)的人工作廢；機器 `9.29/10 passed=true` 沒有解決來源／畫面問題。R27 的成年、無帽、紙上地塊及廣景指令逐項對應這四個失配。

## 精確修訂與凍結項

以 R26 Git 提交 `7e56a30d813c41423a305da658b07871838057c4` 的兩檔原位元組為基準，核 [R27 結構化差分](r27-s53024-adult-map-structured-diff.json) SHA `0fc3c18f09e0c349df5b69ca34312064d297726482372dec40233808c6fd30b2`。差分的兩個 `after` 各在現檔出現一次，兩個 `before` 各在提交版出現一次；逐一反填後，`video.json` 與 `claims.md` 都與 Git 版**逐位元組相同**。解析比較 124 景，只有 `scenes[18]` 的 `s53024.data.prompt` 不同，其他 123 景完整相同；該景 `camera=push in`、`visual=still` 未變。`claims.md` 只有 `s53024` 一整行變動；兩版 126／126 口播 ID 和文字完全相同。

| 檔案或狀態 | SHA-256／值 |
| --- | --- |
| R26 `video.json` | `0ca53d7d67a8601f20ae8473f5d8be0bf1389b720cd3a029cdbe446855a783c6` |
| R27 `video.json` | `458d3391180cff7b57abe2081eba956b711d9572a18f7acbf59c1a185c6a9b1c` |
| R26 `claims.md` | `1454b2cd995cd23607f50d54dfb6ce8f307c26678bcf5e4c31713fc4be3557a3` |
| R27 `claims.md` | `87a5b5d15e0e2e73bc14b1160b66017f6617f746fdbf76401eae4fc5dc5900c7` |
| 未變 `script.md` | `64ffcd8c0e89c4596a7fd08d41bd74f8a16f55fbc9acc2f41d7f9b914ea300fc` |
| 未變私有 `timeline.json` | `c75c8bde15f7220862ba8083d6590b7b14bb71c456f896f7b58c13352c88a054` |
| 未變私有 `narration.wav` | `08444d50c2f8b70a7079701e157397d9a7c23d08971727164df91a1101e281e1` |
| speechHash，R26＝R27 | `05c4d9a79a8708b4` |
| visualHash，R26 → R27 | `a455331f94170433` → `018662cfba7a270f` |

`VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s53 --json` 實跑 exit 0：**0 errors、0 warnings、126 lines**。R26 [停線清單](r26-s53024-native-stop-inventory.json) SHA `d3c21a28c6639f1bc28dc30447a982ad8d30434fbc16d5dd57557a265437fe42`；[R26 回條](r26-s53024-native-stop.md) SHA `8f027b06c80d2692fbb2cf5da851710ebb7c95bfaa663b4cf83d937617d63a76`；[R27 作者回條](r27-s53024-adult-map-author.md) SHA `1a6dcc432b4a1d576b9a57ff4a655b4c5943f08e3e6ac8d4789f4662aab49575`。

私有有效 `keyframes/manifest.json` SHA `246725aaf48f61a0f7e173dfdf49371f72ddbe0d998c2a67c1ccf4c2d3c834fb`，有 15 筆 KEEP，無 `s53024`，`contact_sheet=null`、`contact_sheets=[]`；和 R26 原生 16 筆備份比較，恰好只刪 `s53024`，其餘 15 筆解析值全相同，且每筆所選實檔 SHA、request key 逐項符合 R26 清單。`media/ledger.json` SHA `afaacafe7eee540979f3c525330ffbda2162cb893da1209b1fffe185ddd84bcb`，逐項合計 **US$0.5265／40 image／39 judge／0 預約**，低於整集 US$4.78 上限；`media/jobs.json` SHA `a9d2c69ab3cb5704417b4f0968a7d8d0dae6eb0e35d37e053463220b30d55ca3` 且 `jobs={}`，私有 `STOP` 在位。有效 manifest 仍綁舊 `visual_hash=a455331f94170433`，與 R27 新值不同，所以現在仍是**等待安全離線重綁**，不可把舊圖單當成已通過新稿。

**殘餘風險：**文字指令無法保證下一張原生圖會同時呈現成年面貌、1906 年相容衣著、清楚的無字公園地塊和辦公室廣景；廣景尤其可能令桌上示意圖過小。下一張必須直接核未裁原尺寸及任何裁圖，機器 PASS 不足以代替人工判斷；再退件即停在本景。此紙審沒有放行 `s53025`、已停用的 `s53010/s53018` 第四張、網站關卡或成片。
