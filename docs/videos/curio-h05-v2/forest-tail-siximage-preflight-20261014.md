# 森林來源卡與兩鏡 MiniMax 免費預檢（2026-10-14）

> **歷史預檢快照：**下方「場景位置不變、原句序不變、新時間軸尚未核准、兩鏡尚未生成」只成立於此預檢時點。後續獨立盲審促使 `h5v063`–`065` 移到 `h5v084` 之後；108 句錄音本身未改，但播放順序、`speech_hash`、合併 WAV 與時間軸均改變。新盲審 11/11、後台音訊核准與兩張付費小樣結果見[年代訂正與兩鏡後檢](./authorized-six-pilot-postflight-20261014.md)。

本記錄是 H05 正式分鏡的**待重新審核版本**，不代表成片、插圖或音訊新時間軸已核准。本輪只改 H05 `video.json`／`script.md`；沒有合成語音、重跑轉錄、送後台、產圖、判圖或改寫正式外部時間軸、核准、manifest、帳本。付費範圍若後續放行，僅 `arrival-cabin` 與 `aircraft-search` 各一張圖及一次正常 judge，無同鏡重抽。

## 變更與來源界線

- `forest-unknown` 由虛構具體樹林與山谷的 `shot` 改為原創[資料摘要 SVG](diagrams/forest-unknown-source-card.svg) `diagram`。只對照「飛行員安全降落」與「跳離者不在機艙／落點未確認」，標示資料摘要示意、非當年影像，未畫落點、路線或地貌。原句 h5v033、場景 ID／位置均未動。依 `claims.md` c07／c14 與 [FBI 案件史](https://www.fbi.gov/history/cases-and-criminals/db-cooper-hijacking)。現有核准 WAV 時窗為 165 格／5.500 秒；先前隔離有聲 CC 草剪及站主對來源卡方向的目視記錄見 [森林卡草剪](forest-unknown-sourcecard-offline-20261014.md)。夜雲到大字卡仍有風格跳動，連續畫面未過關。
- `tail-stairs-ground` 原生 `steps` 的底部來源欄，在 720p／1080p 雙行 CC 時與字幕貼近。只把原有 `FBI 案件史｜1971 年 11 月` 放入第一個步驟的 detail，刪掉此一場景的底部 `source` 欄；模板與其他場景不變。隔離正式 renderer 出圖 `layout_problems=[]`，雙尺寸燒字抽格目視顯示來源與雙行 CC 分開。此處文字寫「從機尾跳出」，不畫展開的階梯、人物或落點，符合 c07。抽格是版面檢查，尚待正式播放器驗收。
- `arrival-cabin` 保留一個空座與暗窗的原有提示，作為森林來源卡後的空機艙細節鏡，沒有可辨人物、冒充現場物證或假文字。
- `aircraft-search` 移除原提示中「一名調查員走過並逐排搜查」的虛構動作，改為空機艙走道與一般座椅的抽象調查氛圍。h5v035 旁白仍說探員搜查整架飛機；FBI c26 只支持搜查事件，不支持具體動作或物證位置。此鏡不應被解讀為真實現場再現。兩個 prompt 都沿用全片深海軍藍／羊皮紙黃／低飽和藍綠的 1970s 手繪網印 look；MiniMax 實際能否延續夜雲和來源卡風格，仍待單張樣圖人工目視。

## 精確狀態與量測

改前八檔快照在外部工作目錄 `_receipts/forest-tail-siximage-preflight-20261014T050903Z/`，`snapshot.json` SHA-256 `8b385d97f27f450d778c48adfe05513e244f3bb4d8d334b704470a28e4e41535`；保留原版 video／script／森林 SVG／timeline／approvals／narration.wav／keyframe manifest／ledger。改前 `video.json` SHA-256 `05abe8cf0cd4680a12e911feb118e6d3dec88c20dbba0f8b8e7ac65b51d0d870`，改後 `3bd69dba1e4072dce229ebc08a9e7c3b946407edb623b19210af8ae74de5bc33`；改後 `script.md` SHA-256 `e73d724e5455dc5acc8edc26935c7c27822bb8d5a570386a4e0011d11d505b7e`，森林 SVG SHA-256 `cc5751a7c24842fa7a6a2b4f2735eb893bb900ac6d17b72c539b7c1899431929`。

| 綁定 | 改前 | 改後／現存 |
| --- | --- | --- |
| `narrative_hash` | `25c823ca2e556693` | `5bb0168fb306c862`，**原盲審過期** |
| `speech_hash` | `0b7b642f114d257f` | 同值；108 句文字、ID 與語音要求未變 |
| `pictures_hash` | `f8d3de2a3f752907` | `004c43befd3358c3`；既有 manifest 綁舊圖集合，不能稱整片圖片通過 |
| `timeline.json` SHA-256 | `e1cceb2c0cd511f5c67b4e4c34de201036745ed20cf6e48ad7f85f9a000666e9` | **未重建**，仍寫舊 forest `shot` 模板；舊時間軸音訊核准只適用這個 SHA |
| `narration.wav` SHA-256 | `f0ce6fff529dfb60a72c0e7b4479938d48f6f476ca5961b7ea2190ba15f6feac` | 未動 |
| manifest／ledger SHA-256 | `5815315788579351be33919c1d5ee0a4b5ed0e25538c5be877a28e5b40fd6e89`／`27d3a7744faf39a10633fa11fefd84b22e936768a2c3c23b4af275a7ba87f0bc` | 未動；帳本 28 筆，US$0.189 |

以已核准、尚未重綁的逐句時窗作**候選**量測：總長 16,204 格／30 fps；`shot` 由 58 鏡 9,053 格（55.8689%）降至 57 鏡 8,888 格（54.8507%），高於 50% 下限 786 格／26.2 秒。108 個畫面狀態平均 5.0 秒、最長 7.8 秒，`cadenceProblems=[]`。`arrival-cabin` 191 格／6.367 秒、`aircraft-search` 178 格／5.933 秒。正式新 timeline 重綁後仍需重新量測。

`lint --json` 為 0 errors／0 warnings；兩個指定鏡 `keyframes --dry-run --takes 1` 均 exit 0，MiniMax image-01 顯示 ready，提示長度各 225／873、352／872 字額，伺服器單鏡估價約 US$0.01（頁面四捨五入值，非本次支出），當時帳本 US$0.189／US$80 上限。工作目錄與兩層父目錄均無 STOP，H05 無 LEASE。單鏡 dry-run 不代表圖可用，也不代表全部 57 鏡已完成。

隔離抽格：`tail-inline-source-cc1080.png` SHA-256 `7b9d72ffe96045771a6ac4a0a73ca7ec9c30dda9a265c8ebc1df355a5a4e1681`；`tail-inline-source-cc720.png` SHA-256 `855bc081c1360e865e17bb7015d1345df40378ae27c5142e001e4f0163b0c81e`。後續以 `after-metrics.json` SHA-256 `70c5fa8542027d16762f32165150f6879d17bcaf71473d7f7a3424ac3ef8fe97` 與相同外部目錄下的 `lint-after.json`、兩個 dry-run TXT 核對。獨立盲審用的純輸出在 `narrative-blind-payload.txt`，SHA-256 `5652180bc6ce578fa51e55cdf117f762796f4866742a6cdd54f42870b004508b`。

## 後續關卡

先對 `5bb0168fb306c862` 做**新獨立盲審**；通過後才可用快取 WAV 重建時間軸，要求 0 次合成並比對所有 WAV SHA／時長。新 timeline 由於 forest 模板變更預期不同，須按新 SHA 重走音訊核准並讀回。這兩項 gate 未完成前不付費生成兩鏡；產圖後仍需每鏡一次正常 judge 與獨立人工目視，保留候選或退件，最後再驗兩鏡和相鄰卡片／夜雲的正常速度有聲銜接。`status` 目前敘事面板顯示 stale，未宣稱新稿已核准。
