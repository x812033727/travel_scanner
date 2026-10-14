# H06 v2｜病院至法律審：原生圖卡與隔離有聲草剪

日期：2026-10-14。這是**離線審查候選**，不是正式分鏡核准、已完成影片或發布素材。正式 `video.json`、已核准 WAV、`timeline.json`、manifest、帳本與後台核准均未改動；沒有新增付費生圖、judge、TTS、轉錄或後台請求。三鏡實速影音仍待站主在播放器從頭看聽。

## 正式綁定與來源界線

正式 `video.json` SHA-256 是 `a41d5d784a4e7bfe189b8b2683a172656d84174bc1c2e247ff91f335c5f6f7d1`，正式時間軸是 `829335243ac71490e3ba552ea18a2c1f949c47a06362aee3979cbf6005d170d2`，已核准旁白 WAV 是 `528671067cbc165ca7d0ac32b487311dc147dc89a98eafe62515072cad57db0a`。正式敘事／語音 hash 分別是 `a8b72a5524beace9`／`9ae95e3507d3809f`。目前第一、第三鏡在正式腳本仍為 `shot`，第六輪 MiniMax 圖分別因長椅、紅色銜接及構圖問題人工 HOLD；中鏡 `hook-hospital-door-beat-2` 只是一張可留的**單鏡候選**，三鏡連戲尚未獲核准。退件原圖、judge 與費用收據保留在 [第六輪紀錄](visual-recovery-design-20261014.md)及外部 `review/pilot-revision-two-20261014T040020Z/`。

| 正式場景／句 | 影格時窗 | 隔離替代與證據界線 |
| --- | ---: | --- |
| `hook-hospital-door`／`dszz` | 293–449，156 格 | [原創 SVG](diagrams/hospital-name-link.svg) 用「身分未明」與帶問號的名字卡、未封口紅線示意 1922 年病院裡的身分聯想。[c03](claims.md)只支持有人把她與名字連在一起；不指定誰先說，不畫病院現場、人物或假史料。 |
| `hook-hospital-door-beat-2`／`v202` | 449–601，152 格 | 沿用現存單鏡候選，空門與兩側陰影表示卷宗的兩種起點；不是病院實物，也不代表整段分鏡合格。原 JPEG SHA-256 `24190e085237d6ac080804141649840d3e0074b9f23dfd1df7cae2d9be58e613`。 |
| `hook-three-answers`／`ykiq` | 601–756，155 格 | [原創 SVG](diagrams/appellate-review.svg) 以「1967 年前審 → 1970 年最高法院」示意法律審進入審查。[c05–c07](claims.md)只支持法律與程序範圍、身分未獲證明，不能畫真法院／判決原件，也不能稱法院裁定另一個本名。 |

兩張 SVG 都直接寫明「編輯圖解、非現場／原件」，附德國聯邦最高法院 1970 年判決掃描的頁碼；頁碼和可引用主張沿用 [claims.md](claims.md) 已核的來源表，這輪未重新逐頁讀取來源 PDF。SVG SHA-256：`hospital-name-link.svg=12a1dd28c2d021aa9153da709aacb461326664aec4a9a6c714eb7962281c62b9`；`appellate-review.svg=4cc9a9f180caa8be443a6879c9790758419b5a6962ab88b49cc6c39073d93001`。圖卡不是歷史照、人物肖像或可當證物的文件。

## 有聲草剪與視覺檢查

外部隔離目錄：`<home>/mokaair-work/videos/curio-h06-v2/review/native-three-scene-preview-20261014T042359Z/`。其中 `build-preview.mjs`、`build-reveal-preview.mjs`、`offline-recovery-eval.mjs` 和各 JSON 收據可重建／核對本輪推導。隔離 `video-preview.json` 只把第一、第三鏡變成 `diagram`，SHA-256 `eebd115110f5965d9573ef6a2173fde887bbd68bf1e23c3d1f8c9fa4b860f488`；不是正式輸入。三鏡聲音只取現有 WAV 的樣本 `468800–1209600`，場景與句 ID、原時窗、口播都沒有剪短或重錄。影片均為 1920×1080、30 fps、**463 格／15.433333 秒**，含 AAC 音軌。

| 隔離產物 | SHA-256 | 檢查用途 |
| --- | --- | --- |
| `three-scene-audio-preview.mp4` | `c6971bfa57f37cc37c5a866dbef15ccda22a7e97ae0039c49d657e464bf40f87` | 三張固定畫面、正常速度有聲草剪。 |
| `three-scene-reveal-preview.mp4` | `508c4debfb9b569c6d4c9c7b4be3176d3a8cbd269727c3c6b1d0d2c786035328` | 首鏡左卡 72 格後揭露全卡 84 格；中鏡 152 格；末鏡先右卡 72 格後揭露全卡 83 格。此逐欄揭露只是隔離剪輯測試，正式 renderer 未實作或驗證。 |
| `three-scene-reveal-subtitled.mp4` | `2d8600037dffd8a7abfd023506a319646ec625f1643118ee066141b4e86271f6` | 以較大的兩行繁中字幕樣式燒錄做碰撞壓力測試；**不代表播放器或成片的最終字幕樣式**。 |
| `zh-TW-preview.srt`／`.vtt` | `1a21ffe1ab02658043716bdc29ea91d7303ef6d0bee05a7d92dd3056bd5657ab`／`c00677fcdde9de30066ba88addc13a731c11b420280500fe42f9120ab9841887` | 三句 CC；`checkCues` 為 0 問題。 |

字幕時碼相對草剪起點依序為 `dszz 0.000–4.600`、`v202 5.200–9.650`、`ykiq 10.267–14.807` 秒；場景轉點為 `5.200`、`10.267` 秒。以 `ffprobe -count_frames` 查得上述三支 MP4 均為 463 個視訊格、音軌時長 15.433333 秒；從後兩鏡揭露版抽取多處解碼格檢視。第一次字幕壓力測試確實遮到原圖卡下方來源字與部分卡片，修正前檔案及截圖保留在 `caption-overlap-before-fix/`。現行兩張來源字移到標題下，卡片收在上方約 61% 畫幅；同一種**大字兩行**字幕壓測的第 45、100、185、360、400 格抽圖沒有來源字或主要卡片文字碰撞。不同播放器的 CC 大小／位置仍需播放實測。

**已做的是**產出正常速度有聲 MP4、以 `ffprobe` 和逐句 WAV／CC 時碼機械核對、抽取並目視多個解碼格。**尚未做的是**在可聽播放器裡從頭實速看聽、逐字核對聲音、確認實際播放器字幕設定、判定完整節奏與最終美術品質。兩端皆為大字雙欄圖卡，即使逐欄揭露版比固定畫面多一個節拍，連續觀看仍可能偏簡報感；來源安全不等於吸引力或畫面驗收通過。中鏡的美術與兩端差異明顯，也需要實速看轉場是否突兀。完整檢查範圍和逐檔 SHA 見外部 `final-inspection.json`（SHA-256 `d84c70ffc9edddaf28e96a6f3d607ad60d3e700b38bec01891408fcb2a785c8e`）。

## 50% generated-shot 硬門檻與下一小批候選

正式總長 `15,028` 格，至少 `7,514` 格須為 **實際可用的 generated shot**，不能把 SVG 或未產出的提示算入。正式腳本目前 `7,560/15,028 = 50.3061%`，只有 **46 格**餘裕；兩張卡轉 `diagram` 會減去 `156+155=311` 格，成 `7,249/15,028 = 48.2366%`，差 **265 格**。單靠中鏡 152 格、拉長靜卡、重播圖或標成 shot 不會補回合格時長。

唯一列入本次離線提案的**兩個新 shot 候選**是：

1. `dna-hair-and-box`（9538–9752，214 格／7.133 秒，c09）：從「取得頭髮」接到下一鏡母系比較；俯視普通無標籤信封與一根簡化髮絲，明示現代教學示意，不冒充當年檢體、封存標籤、實驗讀數或人物。與前方玻片教學鏡頭、後方母系代幣鏡頭有不同物件與敘事任務。
2. `grave-fragments-limit`（12344–12498，154 格／5.133 秒，c12–c13）：用小紙片與尚未相接的家庭分支表示「碎片要回答家族關係」；不畫假骨牙、發掘現場、假檢驗報告或已知結果。承接 70 公尺／44 件統計，再進入「地點不能當身分」卡。

兩鏡若**都**產出且審核可用，理論值為 `7,249+214+154=7,617/15,028 = 50.6854%`，比門檻多 **103 格**。只有第一鏡合格是 `7,463` 格，仍少 51；只有第二鏡合格是 `7,403` 格，仍少 111。外部 `video-recovery-proposal.json`（SHA-256 `d2112c0da32a38cf72363a372986b944af9468e7b889117493417e22057d7bc5`）僅為四處模板的計算副本，沒有產圖或進片；`recovery-eval.json` 的實際時窗計算顯示 `cadenceProblems=[]`、`lint` 0 error／1 個既有圖片語彙重複 warning。**這是理論合規，不是現有畫面合規**；影片實際編碼時長和逐鏡接受狀態要再算。

下一個最小付費驗證提案限這**兩個不同 scene ID 各一張 MiniMax、各一次正常 judge，不重抽、不擴批**。現在不執行，也不以離線 JSON 冒充已生成。送出前須先決定兩張 SVG 在實速看聽中可否保留，覆核兩個提示的 c09、c12–c13 來源界線、分鏡連戲及單片預算／STOP／LEASE／dry-run；若任何一鏡退件，立即停下重新算 50%，不能計入退件時長。

## 走向正式版時必須重新開的關卡

- 第一、第三鏡 `shot→diagram` 與兩個其他鏡 `big→shot` 會改敘事 hash；提案計算為 `096ba9d5bcc08524`，**不是現有敘事核准**。正式修訂先做獨立盲審和來源核對，再鎖腳本。
- 104 句文字與順序未改時，提案語音 hash 仍是 `9ae95e3507d3809f`；但正式時間軸的 scene template 與 SHA 會變。不得沿用現有 `82933524…` 的音訊核准；以現有 WAV 重建時間軸、核對逐句／總格，再由站主對新 SHA 核准。預檢 SRT 時碼可能相同，舊字幕收據綁的 video SHA 仍會過期，須重產。
- 提案 `pictures_hash=53a73e9b452f9d43`、`visual_hash=9df2c9328dd4f91b`；正式改版後重新讀回，依工具重新判斷舊 shot 圖與 manifest 的有效性，不手改 `accepted`。兩個新鏡須各自 judge、原圖／裁切圖人工檢視及相鄰連戲；其餘仍缺的 shot、縮圖來源、正式組片與成片完整看聽 QA 均未完成。
- 用**成片實測**重算 generated-shot 時長與 8 秒／平均 6 秒節奏；任何時長低於 50% 立即停。最後再處理正式 CC、上傳與發布關卡，不能拿這段草剪替代成片。

## 本輪檢查讀回

`git diff --check -- docs/videos/curio-h06-v2` 通過；隔離兩圖卡候選 `lint` 0 error、比例不合格如上，四處模板提案 `lint` 0 error、`cadenceProblems=[]`。正式 `video.json`、時間軸、WAV、`approvals.json`、manifest 與帳本的 SHA 均與開工前一致。`npm run test:docs-videos` 跑出 214 PASS／1 FAIL；唯一失敗在未改動的 `docs/videos/imported-long-languages/runner.test.mjs`，其 `package-runtime.mjs` 子程序於 Windows 回 `3221226505`。單獨重跑同一測試仍失敗，不能把全套文件測試報成通過；這次 H06 SVG 仍可被 `sharp` 解碼為 1920×1080，三支草剪由 `ffprobe` 核對為 463 格。
