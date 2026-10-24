# S49 R42｜`moon041` 第二張原圖驗收與 33 張 KEEP 停點

2026-10-22 UTC。[R42 非作者來源／書面畫面紙審](r42-moon041-candle-tabletop-independent-paper.md) SHA-256 `007c757eb65d8150894f5d7f3fd2628bb15c67b6c75b389324e25e23fd099865` 先對燭光候選 **PAPER PASS**。本輪在 STOP 下保全 32 張已收圖、精確離線重綁，隨後只買 `moon041` **第二張** MiniMax 原生圖和一個 judge。機器 **9.29／10 PASS**。我在兩份非作者原尺寸 KEEP 和一份 S53 同行原尺寸 REJECT 之間作明示裁決：**HUMAN KEEP，僅限去黑邊裁圖**，並保留反對意見。入選圖的實際物件已另由[非作者 claims 紙審](r42-moon041-selected-visual-claims-independent-paper.md) SHA-256 `25813e7384a5bbe5ef1d8324de2d6d4439d1ad790b148904e47504b13e752997` 覆核 PASS；這不等於全片審核。

## 付費前守衛與原生圖

R41 32-KEEP active manifest SHA `a28a741c18e0760a2545c3b224f1f5e8c75943dd281a5108063a9c36cd1c8c2d`、帳本 US$1.2420／92 image／92 judge、STOP/jobs 空。固定 `video.json` SHA `07ca48195b04696375564fdde0295ecf35532e75c2b09db09b61a19ba0038f75`，`script.md` SHA `82369f762cc64f70e300e2104a16af3b8e99f1e3296dd81a34152e967f0ecb0a`，`visual_hash=d43f3c8a95c29e22`。STOP 下備份舊圖單，只換 `visual_hash`；32 張 `shots` 完整項目及其實檔 SHA 逐一不變。重綁後、付費前 manifest SHA **`3837bdcbbee0b84137c07dae1cb3a8f9d6419d5a6591822d713a163363e5f230`**，帳本未變。付費前 `media-status`：MiniMax `image-01` configured、圖片餘 **9,918**、judge 餘 **8,052**，單價分別 US$0.0035／US$0.01；單景只讀提示 489／1070 字元。原累積 US$1.2420 加本次 US$0.0135 低於核准整集 **US$5.30**；即使剩餘 85 景各三次圖與 judge，另留 US$0.15 配樂，試算 US$4.8345。一次只暫解 STOP 執行 `keyframes --slug curio-s49 --shot moon041 --takes 1`，exit 0 即恢復 STOP。實收**一張 image、一個 judge**，沒有買 `moon042`。

私人 1280×720 未裁原圖 `keyframes/moon041-1.jpg` SHA **`ac27c84942331b8cfa4138273d9d442b01ee16f409ab7f1711155fba787bfd52`**；入選 1280×720 裁圖 `keyframes/moon041-1-trim.jpg` SHA **`8762bbf1c1485437dce80cabef48dd6db7c03293c0ad58eeafb58bf05286fd52`**。裁切約上緣 6.3%／下緣 4.9%，去掉未裁原圖的黑帶。成年灰髮讀者、年代深色外衣、單支裸火短蠟燭、窗外暗月及平面描邊卡通均可辨，R41 的現代有線聚光燈與半寫實 3D 偶戲感已消失。

## 畫面偏差、不同意見與裁決

紙上淡亮光斑代替提示指定的裸木桌面，桌邊多一件**小型、無字、黃銅色水平鏡筒造型物**，雖 R42 prompt 明寫 `no optical instrument`。機器 judge 的 `details=7` 正確抓到此物；不可寫成全項完全符合提示。[第一位非作者原尺寸審查](r42-moon041-second-native-independent-visual.md) SHA `7b3c5ea7e3138651732cd0921c710f5c69c6017f328191e3868a634f11737a52` 判 **KEEP 0.75**；認為道具沒有接到光斑、未指向月亮，也不呈現巨型或具名赫歇爾器材。[無先前判讀對話的盲審](r42-moon041-second-native-blind-adjudication.md) SHA `7bf853e5ebda4ac5877bcabd5f0b649ce81b1f390ca0455e95c67611c7ef4440` 判 **KEEP 0.91**，只收裁圖。另一位 S53 工作伙伴以協作訊息判 **REJECT**：他認為黃銅水平筒明顯像有底座的光學器材，紙上亮斑也與裸桌面不符，可能重新暗示真實器材。此異議**只有訊息、沒有審查檔或 SHA**，但在此完整保留，不作成一致通過。

我再以完整 1280×720 看入選裁圖。道具形狀確實像桌上望遠鏡，不能稱作「無器材」；然而它閒置且未連成照向紙上光斑或月亮的光路，沒有史料標示，未呈現 Locke 重印本所**虛構**的特定赫歇爾裝置或實驗。旁白談「桌上圖像照亮，也無法讓月球送回更多細節」；近處無細節的亮斑與窗外暗月仍傳達這個對照。Jacoby 明指那些光學對話荒謬，不能核證史實器材。依 `curio-episode`「只退與旁白／來源實質矛盾或畫風嚴重偏移」的插圖規則，對**這張裁圖**採 KEEP；紙張與額外鏡筒是需如實註明的提示偏差，不作實驗證據。若後續剪輯、字幕或口播把這件道具稱為赫歇爾真實器材，本裁決不適用。

因此作者先以[逐位元可逆單行差分](r42-moon041-selected-visual-claims-structured-diff.json)把 claims `moon041` 畫面欄寫成**實際入選圖**：灰髮成人、無字紙上的淡色燭光、裸火短蠟燭、暗月和無字黃銅小道具，並明說它**不是赫歇爾實際器材、存世圖像或實驗證據**。新 `claims.md` SHA **`b51d288b6a2d33e2a976cf054a2b1cb3fdda5109f2845b18b78d81edffbd48af`**，旁白／來源欄／video 與 131 句不變。不同人已實際對圖、固定 Locke／Jacoby 與逐位元倒填做[紙審 PASS](r42-moon041-selected-visual-claims-independent-paper.md)，仍保留 S53 的 REJECT。該紙審只核文字如實和史料界線，不把圖像補成歷史重建。

## 私人庫存與後續門檻

[逐圖 SHA 庫存](r42-moon041-second-native-keep-inventory.json) SHA-256 **`ffde7bf05e8712b2356dd133cc0ebb0252391d9c8df08aebb08f2ae34f663078`** 逐項核先前 32 張入選實檔、本張原圖及裁圖。現 active manifest SHA **`47a517c2b469ca1e48704643a1def318b59aa6f56131d30d1d4d293c56f0aa44`**，**33 KEEP／84 景未畫**，`keyframeProblems` 只有缺圖、其他 0。真實 ledger SHA **`d70880c78ace87406ca881373acfc58c9afd1e736e2decb734d5f86e65f22ae3`**，**US$1.2555／93 image／93 judge／0 預約**。STOP 在位、jobs 空。R41 首張退圖、R42 前後 manifest／ledger、media-status、原圖／裁圖、contact sheets 和執行 log 只在私人 `/workspace/.video-work/curio-s49/review/r42-moon041-second-native/`，未提交媒體或權杖。

`moon042` 的提示與來源須先重核既有 R40 八景紙審是否仍適用，然後逐項再驗 33 KEEP、STOP/jobs、即時媒體餘額、單價與 US$5.30 上限；才可**一次一張**受控生成並原尺寸驗收。首張 HUMAN REJECT 立即停、先修書面並交不同人紙審。此停點不核准其餘 84 張、整集 storyboard、網站聽音或成片。
