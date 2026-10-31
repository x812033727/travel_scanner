# S53 R31｜`s53027` 裸地帳棚與期限畫面非作者紙審

2026-10-22 UTC。**PASS，僅限提交 `2695261fbce621a68535034759d52a6614947e8e` 的精確來源與書面畫面候選。**我不是 R31 作者；本輪只讀固定史料、R30 原圖、R31 差分與私有狀態，沒有改稿、圖單、任務、Git 或購買媒體。紙審不等於下一張原生圖 KEEP；新圖仍須直接看未裁原尺寸。

## 固定日期、帳棚脈絡與圖像界線

獨立重開固定 1913 年 *San Francisco Relief Survey* `/tmp/s53-sf-relief/56217-0.txt`，SHA-256 `d627ed287d8a93b9c00225ea47dbdc4f97c36089a890192a602b993c3c185b72`。G L4934–4941 說公園委員會無正式授權權力，**1906 年 8 月 17 日**同意至多一年不干預公園廣場佔用；D L4855–4864 說小屋是為了**取代帳棚**，機構 8 月 1 日宣布建屋及發包，**9 月 10 日**才開始施工，9 月 16 日漢密爾頓廣場完成 20 棟。故 `s53027`「木屋還沒動工，場地期限卻已開始倒數」是有根據的日期對照；它沒有說期限造成工程延誤，也沒有說 8 月已有完工小屋。當時已有帳棚的脈絡得到 D 的「取代帳棚」支持。

獨立原尺寸打開 R30 首張未裁 1280×720 `keyframes/s53027-1.jpg`，SHA-256 `e762494675c7d5de58f7adb7f99a392a8b08e700654d8a007b54c438b6e1522d`。主體是有屋頂、牆、窗及百葉的**完整兩層房屋**，前景短小童貌人物戴鮮黃稜線硬帽；木板堆與日曆不能消除「9 月 10 日以前尚未開工」的可見矛盾。這與 [R30 停線回條](r30-s53027-native-stop.md)、[清單](r30-s53027-native-stop-inventory.json)及[非作者原尺寸退件](r30-s53027-native-independent-visual.md)的 HUMAN REJECT 相符，不能因機器 10／10 PASS 而收圖。

R31 prompt 改為**1906 年夏末、尚未建小屋的救濟帳棚營地中景**：一位可見灰髮、面紋、未戴帽、穿深色平民外套的中年成年工作者，指向木箱上一張小型無字日曆紙；旁有低矮散置木板，**背景只是一面帆布帳棚牆**。這逐項處理 R30 的完工大屋、童貌硬帽及過度寬闊施工背景。日曆只象徵期限，木板只作未建屋階段的概念道具；G／D **未證明該營地在 8 月 17 日有真實備料堆、日曆原件或這名工作者**，而 `claims.md` 新註記明確否認這些具體史實主張，也排除已建小屋／屋架。提示詞中的木板仍可能被成圖誇張成真實工地材料庫或蓋好的結構，必須於下一張原尺寸審閱；書面文字本身不把象徵物當成已證實的實物。

## 可逆修訂及凍結項

核 [R31 逐字差分](r31-s53027-bare-tent-calendar-structured-diff.json) SHA-256 `a685274b59641f56030fd56372a18b41def81c221dd2a67e00cdf38cb90a1c38`。以 R30 Git `dce425151` 原始位元組作基準，差分兩個 `before` 各在原檔唯一出現，兩個 `after` 各在 R31 現檔唯一出現；將 `scenes[20].data.prompt` 和 `claims.md` 的 `s53027` 整行反填，兩檔均與 R30 Git 版**逐位元組相同**。解析比較 124 景，只有本景 prompt 不同，其他 123 景與全域設定相同；本景 `camera=drift left`、`visual=still` 未變，126／126 口播 ID 與文字相同。

| 檔案／繫結 | R30 → R31，或未變 SHA-256 |
| --- | --- |
| `video.json` | `2d2191c6a66ae253f4ce9d167babb364729134c4e56244b68723cce1b091a59a` → `b9ce6cc426d547642ff7f6a7ee8c3a2564aad2439ff4b659c0f337ba19e9fea6` |
| `claims.md` | `1479a0328bfe1783075d1b21e4dbc9fad1bc858bd22b10c1506abd0119070f6d` → `535993a24ade462411a63e5161d1d1dc3552e5470ab0d7c226d4fa677260eeda` |
| `script.md` | 未變 `64ffcd8c0e89c4596a7fd08d41bd74f8a16f55fbc9acc2f41d7f9b914ea300fc` |
| 私有 `timeline.json`／`narration.wav` | 未變 `c75c8bde15f7220862ba8083d6590b7b14bb71c456f896f7b58c13352c88a054`／`08444d50c2f8b70a7079701e157397d9a7c23d08971727164df91a1101e281e1` |
| visualHash | `7374825e2bdc1744` → `63a1d200e63843e2` |
| speechHash | 未變 `05c4d9a79a8708b4` |

實跑 `VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s53 --json` exit 0：**0 errors、0 warnings、126 lines**。有效私有 `keyframes/manifest.json` SHA-256 `10f6a61061a6145be727d3991bafec32976cabb4a4373da2eab87f92e0b7f757`，仍綁 R30 `visual_hash=7374825e2bdc1744`，有 17 筆 KEEP、沒有 `s53027` 退件條目；逐項核對 R30 清單中 17 筆 ID、request key 和所選實檔 SHA，全數吻合。私有 `media/ledger.json` SHA-256 `f4aabe398ddc7e5574779a4e018fa5dae8acfdecd43b47dec748d7796f118912`，逐筆合計 **US$0.5805／44 image／43 judge／0 預約**，低於整集 US$4.78；`media/jobs.json` SHA `a9d2c69ab3cb5704417b4f0968a7d8d0dae6eb0e35d37e053463220b30d55ca3` 且空，`STOP` 在位。R31 新 `visualHash` 尚未回綁，**不可視舊圖單為新稿合格**。

紙審 PASS 後的界線：先在 STOP 下安全備份並離線只更新圖單繫結，重新驗 17 KEEP、即時 image-01／額度及 US$4.78 上限，再最多試 `s53027` **第二張**。如成圖再出現已建屋、屋架、童貌現代硬帽，或把木板變成主體工地材料堆，立即停在本景；不得跳畫 `s53028`，也不得替 `s53010/s53018` 買第四張。本紙審沒有執行上述操作。
