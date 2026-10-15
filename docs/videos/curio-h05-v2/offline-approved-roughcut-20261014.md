# H05 核准旁白的隔離有聲草剪與 CC 安全區（2026-10-14）

**範圍。** 這是 `curio-h05-v2` 的離線檢查，輸出在 `<home>/mokaair-work/videos/_offline-h05-approved-preview-20261014/`，不在正式媒體目錄。沒有付費呼叫、修改 `video.json`／WAV／正式時間軸／核准／manifest／帳本，也沒有把森林佔位當成素材。輸入鎖定：`video.json` SHA-256 `05abe8cf0cd4680a12e911feb118e6d3dec88c20dbba0f8b8e7ac65b51d0d870`、`timeline.json` `e1cceb2c0cd511f5c67b4e4c34de201036745ed20cf6e48ad7f85f9a000666e9`、`approvals.json` `4c9eeb731bf165350a5b4b2f4f2e5b916ad5702a12338ea286be7803f5d29a0a`、`narration.wav` `f0ce6fff529dfb60a72c0e7b4479938d48f6f476ca5961b7ea2190ba15f6feac`。`narrative_hash=25c823ca2e556693`、`speech_hash=0b7b642f114d257f`、`pictures_hash=f8d3de2a3f752907`；本輪沒有改變。外部總收據 `receipt.json` SHA-256 `01185fedbde6d29b596b1fc4792793da3c14edecb012e7482d751d80b6adaa11`，含所有中間檔的逐檔 SHA。

| 隔離 MP4（1920×1080、30 fps、AAC／H.264） | 正式幀區間與單鏡時長 | 輸出與驗證 |
| --- | --- | --- |
| `opening-three-cards-cc.mp4` | `open-threat` 699–832：133 幀／4.433 秒；`open-tail` 832–989：157 幀／5.233 秒；`open-boy` 989–1136：147 幀／4.900 秒 | 437 幀／14.566667 秒，SHA-256 `5c4da594f3dfbbd807208977b80aa50a8a11f411f7972bf209ef4199b55b8071`；音軌、影軌及容器時長皆為 14.566667 秒。 |
| `tail-night-forest-cc.mp4` | `tail-stairs-ground` 4377–4563：186 幀／6.200 秒；`night-clouds` 4563–4753：190 幀／6.333 秒；`forest-unknown` 4753–4918：165 幀／5.500 秒 | 541 幀／18.033333 秒，SHA-256 `e447d0d93d2a0f6c9df61b5294db065084a9448b72fa13f8193956aa1312d2fc`；音軌、影軌及容器時長皆為 18.033333 秒。最後一鏡只用明示「灰階佔位／尚未產圖」的卡片。 |

同一正式 renderer 的四張原生卡跑兩遍，靜格 **4／4**、入場幀 **48／48** 逐位元一致。從正式時間軸與現行 108 句重建繁中正文 CC，`checkCues` 零問題；兩段分別取 `h5v006–008` 和 `h5v031–033`，字幕入點與場景幀一致。六句既有 line WAV 的 PCM 與核准旁白母檔對應 sample **逐位元相同**，句末保留原有靜音；兩段抽出的 preview PCM 亦與母檔區間一致。這證明草剪使用同一音訊與時碼，不等於已聽審 AAC 播放品質。`inputs.json`、`encoded.json`、`audio-verification.json`、SRT／ASS、可重跑的本機程式和命令都在隔離輸出目錄。

**目視與限制。** 開場三張原創來源卡的抽格有一致的深青／紙色設計，來源與「示意」標示可讀；雙行 CC 抽格未蓋住其卡內註記。尾梯原生步驟卡到夜雲小樣的切換有明顯色彩和紋理跳動：前者平面深青，後者有亮黃、層疊裝飾性雲緣；夜雲只維持**單鏡候選**，沒有判整段合格。草剪只保持該圖，**未模擬正式 `pan right`**。森林灰階佔位只能檢查 5.5 秒節奏，不能判夜雲至實際森林鏡的風格銜接。已打開四張 renderer 靜格、佔位卡及兩段 MP4 的六張抽格；**未實際從頭以正常速度看聽**，這項仍需站主／有聲播放器覆核。此處燒錄的是正文 CC 小樣，沒有正式成片的品牌片段位移，也沒有經 YouTube 播放器測試。圖像、字卡、字幕並未進入可上傳成片。

## 尾梯來源欄的隔離修正試驗

原版 `tail-stairs-ground` 的來源「FBI 案件史｜1971 年 11 月」在畫面約 y=920，與雙行 CC 的第一行幾乎貼在一起。隔離渲染只對該頁注入 `.t-steps .caption-line { transform: translateY(-80px); max-width: calc(100% - 80px); margin-left: auto; margin-right: auto; }`；原版與候選均 **0 個 renderer 版面問題**。用當下的 `h5v031` 雙行 ASS cue 分別在 1920×1080、1280×720 燒字抽格，候選在兩種尺寸都有可見空隙、來源欄可讀，原版則貼住字幕。四張對照為 `qa-frames/{baseline,footer-up-80}-cc{1080,720}.png`，隔離收據 `layout-safety-receipt.json` SHA-256 `98149247ca138e91cea7ef6c03277e4315dbe506e9cf4c04095a734ea3761545`，保留程式、原圖、候選圖及各 PNG 雜湊。

**沒有正式採用此版面。** `steps` 只接受 `data.source` 字串，沒有 H05 單卡的來源位置欄位；直接改共用模板會影響其他影片，改此場景的資料／模板則須重新計算正式敘事、畫面及音訊綁定並重走關卡。因而本輪正式 SVG／資產 SHA、`pictures_hash`、`timeline.json` 和 `approvals.json` **均未變**；隔離 PNG 不能替換正式 frame。正式播放器中來源欄和兩行 CC 的安全距離仍是待修缺口。後續若正式採用，需另立局部版面實作與 hash／審核收據，並做實際播放器的 CC 驗證。

## 剩餘鏡頭的最小下一批

現行正式時間軸 16,204 幀，其中 58 個 `shot` 共 9,053 幀，**55.8689%**；扣掉已有單鏡候選 `night-clouds`，仍有 **57 個 shot 未取得現稿可用圖**。三個緊接夜雲的 shot slot 是 `forest-unknown`（165 幀／5.50 秒，c07／c14）、`arrival-cabin`（191 幀／6.37 秒，c26）、`aircraft-search`（178 幀／5.93 秒，c26），合計 534 幀／17.80 秒。這一組可檢查夜雲之後的段落節奏，但目前不能付費擴批。

最窄的來源安全方案：先把 `forest-unknown` 設計成明示「落點未確定」與來源的原生卡，避免現行「有樹林和山谷」提示把未知落點畫成既定地貌；`arrival-cabin` 才用無人、無字的 1970 年代機艙氣氛圖；`aircraft-search` 若用圖，提示須收窄成無可辨人物／物證近景的機艙調查氛圍，不能虛構現場搜索手法。先做隔離三鏡草剪，再決定是否單次、逐鏡付費。把 `forest-unknown` 從 shot 改原生卡會使插圖占比成 **8,888／16,204 = 54.8507%**，仍高於 50% 下限 **786 幀／26.2 秒**；全三鏡都改卡仍是 **8,519／16,204 = 52.5734%**，但會連續 17.8 秒卡片而有觀看疲勞風險。此方案若正式改 `template`／`data`，**會改敘事與時間軸審核綁定**，須獨立盲審、用既有 WAV 重綁時間軸、重新讀回音訊核准。若只窄修 shot prompt 而保留場景／台詞／時窗，預期改 `video.json` 與 `pictures_hash`，仍須重新 dry-run、付費前置與圖像人工驗收；不可把現行一張夜雲 PASS 當成三鏡通過。這些均是下一步設計，**本輪未修改或發出生成請求**。

後續另做 [forest-unknown 原創來源卡的隔離草剪](forest-unknown-sourcecard-offline-20261014.md)；本頁記錄的灰階佔位版與雜湊原樣保留供對照。新卡沒有進正式 `video.json`。
