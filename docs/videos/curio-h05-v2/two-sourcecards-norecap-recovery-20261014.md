# H05 兩張來源卡與去重窄修（2026-10-14）

**本版為離線候選，尚未通過新敘事盲審或重綁音訊。** 已人工退件的 `arrival-cabin`、`aircraft-search` MiniMax 原圖及正常判圖、費用與失敗理由，仍以[六圖授權後檢](authorized-six-pilot-postflight-20261014.md)為準；沒有改分數、manifest、帳本或重新抽圖。

## 變更與來源

- `arrival-cabin` 改為原創 [NORJAK 代號卡](diagrams/norjak-source-card.svg)，只顯示 FBI 案件史所載代號與 **Northwest Hijacking** 的關係，標明來源及「非當年文件或現場影像」。未畫座椅、人物、機票或調查文件。
- `aircraft-search` 改為原創 [機身搜尋流程卡](diagrams/aircraft-search-source-card.svg)，以抽象的「機身整體 → 搜尋可能物證」表達 FBI 搜尋機身物證，明示沒有重建人物、物證或物證位置。這兩張卡依 [FBI D.B. Cooper Hijacking](https://www.fbi.gov/history/cases-and-criminals/db-cooper-hijacking)；網站實讀於 2026-10-14。相鄰 `forest-unknown` 來源卡未改。
- 第一版兩卡接入後，獨立敘事盲審 **9/11，FAIL**：`no_recap` 指出 `h5v003`／`h5v038` 重述購票名、`h5v100`／`h5v101` 重述埋沙灌水順序；`payoffs` 認為 `h5v109` 未在回答時再點名 `h5v107` 的五千八百美元。原始答案與正式面板的舊版快照保留在外部收據。`h5v107` 已明示「還記得…五千八百美元」且 `h5v109` 緊接回答「證明贖金，不證明人」，因此保留這組問答，交下一位獨立審查者判讀，**不把本輪 FAIL 改寫為 PASS**。
- 去重時只刪 `ticket-original`／`h5v038` 與 `burial-experiment`／`h5v100` 兩個完整場景及其句子。前者同一張 FBI 機票原照已於 `open-ticket` 出現，`h5v039`–`040` 仍解釋 D.B. Cooper 稱呼不能證明身分。後者由 `h5v101` 原錄音保留「埋沙後再灌水的對照」與紙邊幾毫米結果，`h5v102`–`103` 保留內層與先浸水後埋沙的研究推論；該研究確為人為對照，見 [Kaye、Meltzer 2020 原論文](https://pmc.ncbi.nlm.nih.gov/articles/PMC7400570/)。刪除原步驟卡也移除了畫面上「非原鈔／高濃度矽藻土水」的細節，正式聲畫審查仍須確認 `h5v101` 的對照限制不被誤讀成當年贖鈔實驗。

## 可重現的離線量測

改前原始分鏡、`script.md`、時間軸、核准、判圖 manifest、帳本及兩卡接入後的第一版分鏡、盲審答案，都在外部 `<home>/mokaair-work/videos/curio-h05-v2/_receipts/h05-two-sourcecards-20261014T053947Z/`。其中 `projected-after-cuts.json` 由原 `timeline.json` 的逐句 WAV 樣本數經正式 `buildTimeline` 函式**離線推算**；先精確重現舊時間軸所有逐句時窗，再刪兩段各 127、165 格。沒有寫回正式時間軸或重新合成音檔。

| 項目 | 本版離線候選 |
| --- | --- |
| `video.json` SHA-256 | `8727405399cd8297b5c15bb8097f05621255d1d43b06b81519a83f57cba79017` |
| `script.md` SHA-256 | `08ca84eaae2677369cf73e7a8189dd2cf33b97a291682ef4cdca818d7f259924` |
| `narrative_hash`／`speech_hash`／`pictures_hash` | `95245c2bcde00773`／`64172cdd8198a5ae`／`96ffa840e7d65492` |
| 逐句內容 | 刪 `h5v038`、`h5v100`；其餘 106 句 ID、文字、情緒、所屬場景與相對順序均未改，WAV 原件未動 |
| 預計正文 | 15,912 格／30 fps＝530.4 秒（8:50.4）；舊版 16,204 格 |
| 規劃插圖占比 | 55 個 `shot`，8,519／15,912 格＝**53.5382%**，比 50% 多 563 格；這是模板時長，**不是已驗收圖片占比** |
| 畫面節奏／lint | 106 狀態、最長 7.8 秒、平均約 5.0 秒、`cadenceProblems=[]`；lint 0 errors、0 warnings |
| 純盲審 payload | 外部 `narrative-blind-payload-after-cuts.json`，SHA-256 `064d98ec01110c20247025b82bc658a42efa0478487b6c31d26f90bb3b4b2b86`；待另一位審查者給 11 題答案 |

用正式 Chromium renderer 將兩卡各畫兩輪，兩輪靜格與 12 張入場幀逐位元相同、`layout_problems=[]`；靜格 SHA-256 依序 `8d96eaa8e09f5966c10c70cb07d205127752b43f1be6aea707aa05b2a4a55e59`、`b2b56e834f2f372976371b9c7e6424aab17a6763e06ffddf6150c54ac67ef9e4`。以實際句文拆成代表性雙行 CC，在 1920×1080 與 1280×720 四張抽格目視，來源欄、示意限制與字幕互不遮蓋；這只是**靜格版面檢查**，未做三卡正常速度有聲剪接、正式播放器或全片驗收。

舊 `timeline.json` SHA-256 `f8d106653941b3b90c9d3d6d6adf50f8bbb653bffde941073b43ce721e414468` 與其站主音訊核准只屬於 108 句舊時間軸；本版刪兩句後 speech hash 已變。`status` 可能同時列「舊稿時間軸」與 `[x] narration approved`，後者不可當本版核准。下一步須先讓新敘事盲審通過，再用保留的 WAV 重綁、核對 0 次合成與剩餘逐句音檔雜湊，最後對**新時間軸雜湊**送後台聽審並讀回核准。完整圖組、聲畫剪接、字幕、QA、成片及上傳仍未完成。

## 後續正式後檢

以上段落保留當時的離線候選及待辦狀態。其後另一位獨立讀稿員對**同一正式 `video.json` 與兩句刪除版**重新作答，11/11 PASS，正式 `review/narrative.json` 綁定 narrative hash `95245c2bcde00773`。`tts --refresh-evidence` 使用 100 個既存請求、**0 句新合成**；106 句 WAV 原件未重錄。正式 `timeline.json` SHA-256 `fd724a0c4318fe76fcb4a1811dadbf09f0aeff47d0849bfc025ceb03fed50fbc`，合成旁白 WAV SHA-256 `ce18ff45161fbffe0fb058d7d6f8d8a438b0bc5bb9492a5ca099e7c7e43aa943`，實長 15,912 格／30 fps＝8:50.4。站主聽完新版卡後在後台核准；`review-pull` 已將**相同的正式時間軸雜湊**寫回 `approvals.json`。55 個 `shot` 仍只是 8,519／15,912 格＝53.5382% 的規劃分配，尚無完整已驗收圖組。來源卡原圖與舊退件圖的人工判斷未因此變成完整畫面核准。
