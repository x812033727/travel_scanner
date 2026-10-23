# H06 v2｜來源圖卡與兩個新鏡的免費正式預檢

> **歷史快照，已由 [同日無重錄修訂補記](no-recap-two-scene-addendum-20261014.md) 取代。**本文的「目前／現行」、104 句、15,028 格、scene 次序與原時窗、`7,617/15,028` 占比、敘事／語音／視覺／影片雜湊，只描述刪除 `berlin-name-blank` 和 `berlin-name-card` 之前的正式預檢。現行稿為 83 景、102 句、14,698 格，planned shot `7,464/14,698`；請以補記與其綁定收據為準。本文的 SVG 來源和當時預檢證據仍保留作追溯，不代表今日新版已獲盲審、音訊或畫面核准。

日期：2026-10-14。站主看過[三鏡離線有聲草剪](native-three-scene-preview-20261014.md)，接受來源圖卡方向，並授權下一次**兩個不同鏡頭各一張** MiniMax 小樣及各一次正常 judge。本次只把兩張 SVG 和兩個新 shot 提示寫入正式腳本，做免費預檢；**沒有執行付費生圖、judge、TTS、轉錄或後台審核**。這不是 storyboard 核准，也不是完成影片。舊小樣、退件圖、manifest 和帳本均保留。

## 變更範圍與來源

`video.json` 只改四個 scene 的模板與畫面資料，保留 104 個 line ID／口播、scene 次序和全部原始時窗；另在 YouTube 說明欄加一段精確的圖外揭露。差異由外部 `adoption-check.mjs` 對原稿逐欄比較，非四鏡與單句說明欄變更會報錯。

| Scene／原時窗 | 正式變更 | 來源及不可越過的界線 |
| --- | --- | --- |
| `hook-hospital-door`／293–449，156 格 | 退件 `shot→diagram`，採用[病院姓名連結 SVG](diagrams/hospital-name-link.svg) | [c03](claims.md)：1922 年病院裡有人把她與安娜塔西亞名字連在一起，但判決留下誰先說的兩種記述；圖解不指定說話者、不畫現場或文件原件。SVG 標有編輯示意及聯邦最高法院判決掃描 PDF 第 6 頁。 |
| `hook-three-answers`／601–756，155 格 | HOLD `shot→diagram`，採用[法律審 SVG](diagrams/appellate-review.svg) | [c05–c07](claims.md)：前審、1970 年法律審與身份未證明的裁定範圍；不宣稱法院裁定另一個本名。SVG 標有編輯示意及法院掃描 PDF 第 3、13、138–144 頁。 |
| `dna-hair-and-box`／9538–9752，214 格 | `big→shot`，單根髮絲、無標籤信封的現代教學構圖 | [c09](claims.md)：頭髮與保存組織分別接受分析；這不是當年的信封、檢體、紀錄或結果。此鏡只介紹材料類型，下一鏡才進入母系比對。 |
| `grave-fragments-limit`／12344–12498，154 格 | `big→shot`，紙片與尚未接通的家族分支 | [c12–c13](claims.md)：第二墓碎片與後續親緣研究；紙片不是骨牙，分支此刻不畫成已確定結果。來源為 [Coble 等人 2009 年 PLOS ONE 原文](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0004838)。 |

兩個新 shot 的實際生成提示以**肯定的可見構圖**描述，沒有要求模型寫字、畫報告或製作來源標籤：

> `dna-hair-and-box`: Wide flat 2D overhead editorial still of one plain unmarked envelope lying open on a matte tabletop. A single simplified dark hair strand curls across its pale lip. One small vermilion square guides the eye from the envelope toward an open space for the next comparison scene. Broad opaque cut-paper shapes and ink edges keep the envelope and strand as the clear focus in the centre third.

> `grave-fragments-limit`: Wide flat 2D editorial still of several small opaque cut-paper shards grouped on the left, a broad clean gap at centre, and three plain circular family tokens joined by a branching cord on the right. One short vermilion path ends before the gap, keeping the family relationship visibly unresolved. Matte paper layers and irregular ink edges give the scene one clear focal question in the centre third.

兩鏡 `camera=pan right`、`visual=still`。教學示意標籤**不交給生圖模型拼字**：正式 `youtube.description` 現寫明「頭髮信封與紙片家族分支畫面是現代教學示意，並非當年檢體、遺骸或檢驗紀錄。」前兩張原生 SVG 則自行承載圖解及來源文字。新 shot 如要在畫面內再加固定角標，須使用編輯器可控字體另做，不能把文字寫入 MiniMax 提示或把沒有角標的候選說成已有角標。看圖時仍須檢查模型是否自發畫出假文字、骨牙、檢驗結果或來源未允許的細節。

## 正式渲染與字幕安全

正式 renderer 讀取兩個 SVG，`renderProblems=[]`、兩個模板的 `layoutProblems=[]`、字體覆蓋缺口 `[]`；因此正式腳本選用 SVG 自帶標題和來源、**不額外加模板 caption**。外部隔離目錄 `<home>/mokaair-work/videos/curio-h06-v2/review/formal-source-card-adoption-20261014T050837Z/` 保留 `probe-formal-render.mjs`、`render-probe.json` 及四張 1920×1080 渲染圖。正式選用構圖截圖的 SHA-256：`hook-hospital-door-no-caption.png` = `5c8b55f6430839894f689758dbc97461710ccd5a9988e7222b0c7950a8601a04`；`hook-three-answers-no-caption.png` = `96f0cb7cb8c144d13d7b90de72095f5166555c183214c453f2ba5048aa0bda76`。兩張 SVG 原檔分別為 `12a1dd28c2d021aa9153da709aacb461326664aec4a9a6c714eb7962281c62b9`、`4cc9a9f180caa8be443a6879c9790758419b5a6962ab88b49cc6c39073d93001`。

另以一種較大的兩行繁中 CC 樣式（ffmpeg libass，Microsoft JhengHei 34 px、下邊距 45）在正式渲染靜格做碰撞壓測：`hook-hospital-door-large-cc.png` SHA-256 `0d3600940644d18053306e32c85f64d7911bc670d5ed8566cea927408749b770`；`hook-three-answers-large-cc.png` SHA-256 `81cb52866d9c5db698d0b0f59c7e60b8042ac297c64137afe31510ce5c5d0fe7`。兩張的來源字與主要卡片文字未被該模擬字幕遮住，對照收據 `caption-probe-receipt.json` SHA-256 `4944080ac3f0bdd9dcc2d60c82ebce1b65dc50b6eb122f1e31f7516790e3d7e7`。這僅是固定影格與一種字級；實際播放器字幕大小、位置、動態揭露、完整實速看聽尚未驗收。

## 精確綁定與比例

| 綁定 | 採納前 | 目前／離線推算 |
| --- | --- | --- |
| 正式 `video.json` SHA-256 | `a41d5d784a4e7bfe189b8b2683a172656d84174bc1c2e247ff91f335c5f6f7d1` | `17492a61530c2b09c9547f4cc71c824c993dc628ebddd8d3a97a47f0dee67ed2` |
| narrative hash | `a8b72a5524beace9` | `096ba9d5bcc08524`，舊盲審過時 |
| speech hash | `9ae95e3507d3809f` | `9ae95e3507d3809f`，104 句未變 |
| look hash | `d57461da98a0ba9b` | `d57461da98a0ba9b` |
| pictures hash | `1fa2c8f61603eff9` | `c6ed3e494f6582a7`，舊圖不能整批沿用 |
| visual hash | `529d6a4176e2c008` | `fc00fc2a753ca90d` |
| 正式 `timeline.json` SHA-256 | `829335243ac71490e3ba552ea18a2c1f949c47a06362aee3979cbf6005d170d2` | **仍是舊檔**；只用原時窗和新模板計算的**未核准**副本 `e863368587f45353e6cbbfdd78feb31e4c6b5de29fda3fbea87501e9fea58d85` |
| 旁白 WAV SHA-256 | `528671067cbc165ca7d0ac32b487311dc147dc89a98eafe62515072cad57db0a` | 不變；`approvals.json` 仍綁舊時間軸，SHA-256 `d0121b40210d9c002750c005833213f1eedc71b7ef41b92171383854a0024d45` |

精確時窗共 `15,028` 格，50% 門檻 `7,514` 格。原模板 `7,560` 格，只餘 **46 格**；兩張開頭卡轉 SVG 減 `156+155=311`，兩個新 shot 若**都實際產出並審核可用**才加 `214+154=368`，成 `7,617/15,028=50.6854%`、餘 **103 格**。若只一張成功，任一種組合均不足 50%。這是模板與時窗的**理論上限**，並未把未生成或退件圖計作已合格時長；成片必須按實際接受影格重算，低於 50% 即停。

`adoption-check.json`（SHA-256 `8e8b18d200863cc40cb91e23501cc10211d8923b670a19821167f3332cff0048`）機械驗出 104 句與全部時窗未變、`cadenceProblems=[]`、101 個畫面狀態、最長 8 秒／平均 5 秒、lint 0 error／1 個既有 `generic` 重複 warning。兩次 `keyframes --dry-run --shot … --takes 1` 各只選一個新 ID，prompt 預算為 `389/929`、`401/929` 字元；dry-run 收據 SHA-256 依序為 `b128289b0446fd5a93065cbf1e0dd7bf14f5e79bb7f15717613189f47c690368`、`be036d7e6d704dfc932837f4aeb0f91f8d6760296bf0ecc77c9b1c623651260d`。dry-run 對每鏡報 MiniMax `image-01` 1K 約 US$0.01，**不含正常 judge，沒有扣款**；實際價格以後續帳本為準。

## 外部收據與尚需關卡

上述隔離目錄保留變動前 `video-before.json`、`timeline-before.json`、`approvals-before.json`、`manifest-before.json`、`ledger-before.json`、`state-before.json`，以及第一版採納、修正提示與最終版的分別收據；不覆寫舊退件或收據。`postflight-final.json` SHA-256 `b8083f782799ec6112111835cbbec16dd6462c3a1074e95bea20ae7d729fb395` 對目前正式影片、舊時間軸、WAV、approval、manifest、ledger、state 重算 SHA；這些未改媒體及狀態檔皆與預檢相同，沒有 H06 專案及兩層上級 `STOP`／`LEASE`。帳本仍是 **11 張圖、11 次 judge、US$0.1485、0 預留**，單片上限 US$80。既有 `keyframes/manifest.json` SHA-256 `d0620e0b9486628fd5f14002bb1b89391adcb2b844c64699843373503041e75d`，ledger SHA-256 `989e26821a8690d6965676b74933534aa9f8177664f011c0a00d8966f74efd8b`，state SHA-256 `2b3998f2422bbc49bbdc19c0efa3f8819e25553453c3c5810ae31952af939a54`；本輪不手改任何 `accepted` 欄位。

獨立盲審的當前純讀稿 payload 已另存 `blind-payload-final.json`，SHA-256 `2ae486fe878e698f489ddf86f8f134bdc2902ee5349d98f30a28bed339ce5625`，綁定正式影片 `17492a61…` 與 narrative `096ba9d5bcc08524`，含 11 個問題且不含舊答案。`blind-payload-receipt.json` SHA-256 `37cb7699c634ab3328125db50b5d50a0516371d93ec7538a2946faece78d8127`。這只是送交讀稿員的輸入，不是盲審結果。

1. 針對 `096ba9d5bcc08524` 做獨立敘事盲審及來源覆核，尤其新兩鏡的示意不應被誤讀為檢體或結果。
2. 以不變的 WAV 重建正式時間軸，核對 104 句／15,028 格與 CC，再由站主對**新時間軸 SHA** 重新核准音訊。現有後台狀態顯示的舊音訊核准與舊 SRT 收據，不能替代新綁定。
3. 付費前再讀 STOP／LEASE、剩餘預算及 dry-run；授權範圍只到兩個新鏡**各一張、各一次正常 judge**。產出後分開記 judge 與人工原圖／裁切圖審查，假字、假證物或不相連的構圖須退件，不能為了湊滿 50% 手動接受。
4. 補齊其他有效 shot、縮圖與來源、正式組片，實測 generated-shot 比例／節奏，並在播放器完整實速看聽與檢查可關閉的 CC，才可進入交付關卡。
