# H05 `forest-unknown` 來源卡隔離草剪（未正式採用）

2026-10-14。保留[原創候選 SVG](diagrams/forest-unknown-source-card.svg)，SHA-256 `cc5751a7c24842fa7a6a2b4f2735eb893bb900ac6d17b72c539b7c1899431929`；與隔離草剪使用的 SVG 逐位元相同。**`video.json` 仍是 `shot`，沒有引用這張卡。** 本輪沒有改正式時間軸、旁白、核准、manifest 或帳本，也沒有付費請求。

## 來源與畫面界線

依 [claims c07／c14](claims.md) 和其中登錄的 [FBI 案件史](https://www.fbi.gov/history/cases-and-criminals/db-cooper-hijacking)，卡片用兩欄文字區分「飛行員安全降落」與「跳離者不在機艙，落點未確認」，右上明寫來源、下方明寫「資料摘要示意／非當年影像／不表示落點或路線」。它沒有畫人物、飛機、特定樹林或山谷、地圖與移動軌跡，避免原 `forest-unknown` 提示把未知落點具象化。FBI 來源說的是**飛行員**安全降落；卡片刻意比現有 `h5v033` 旁白的「機組員」窄，若將來正式採用，須由獨立敘事審稿核對用字範圍。

## 隔離影片與檢查

在 `<home>/mokaair-work/videos/_offline-h05-approved-preview-20261014/`，新檔 `tail-night-forest-sourcecard-cc.mp4` SHA-256 **`1d7ea9b5d6b96b6b22cea4391c4644c4a6c85f06f38ac92d0280b4f7d3bab383`**，1920×1080、30 fps、541 幀／18.033333 秒，完整解碼通過。舊灰階佔位版 `tail-night-forest-cc.mp4` SHA-256 `e447d0d93d2a0f6c9df61b5294db065084a9448b72fa13f8193956aa1312d2fc` 及其舊收據 SHA-256 `01185fedbde6d29b596b1fc4792793da3c14edecb012e7482d751d80b6adaa11` **原樣保留**。兩版前兩鏡相同，新卡仍佔正式 `forest-unknown` 的 165 幀／5.5 秒；重用同一核准旁白片段 WAV SHA-256 `60a6ba99dde28a8f18da5d99adad988e356734d3e1bf84f409bf9358e716d1ed` 與同一繁中 ASS。renderer 兩輪靜格／12 張入場幀逐位元一致、0 個版面問題；新卡 PNG SHA-256 `4fd1e0d982d4f232881a40812c469879b7f89bb6c8f9c4fcaea2482268e87400`。

逐張打開 `qa-frames/forest-night-before-card-1080.png`（12.500 秒）、`forest-card-enter-1080.png`（12.567 秒）、`forest-card-settled-1080.png`（12.933 秒）和 `forest-card-cc-two-line-{1080,720}.png`（14.000 秒）。`h5v033` 與卡片均由正式全片第 **4,753 幀**／草剪第 **376 幀**開始，沒有跨到前句 `h5v032` 或移動語音、CC 時碼；模板 12 幀／0.4 秒的入場讓第一瞬間先呈現深色底與雙行字幕，卡片隨後一次顯示完整結果，**可能早於 `h5v033` 後半句的口播**，正式節奏仍待實速聽看。1080p、720p 抽格的兩行字幕**沒有蓋住卡內 FBI 來源與示意註記**，但第一行幾乎緊貼大紙卡底邊；站上播放器 CC 安全區仍待實看。尾梯步驟卡舊來源欄與字幕過近的問題仍存在，此輪未偷換其版面。

**美術與節奏風險仍高。** 夜雲的亮黃／深青層雲直接切到大面積米白字卡，亮度、材質與觀看任務都跳變；這也是全片的第四張大型文字來源卡，會加重簡報感。來源安全與單張可讀不等於連續畫面通過。已完成抽格目視、逐幀／時長與原 WAV／CC 時碼機械核對；**沒有實際從頭正常速度看聽**，也沒有 YouTube 播放器驗證。完整隔離收據 `forest-sourcecard-receipt.json` SHA-256 `1b6c713b1b3d90d7fabda90bee7abb9a0c8eb5ee4ff77f9a935795e6b69fd9fa`，另有可重跑 renderer／ffmpeg 指令與逐檔 SHA。

## 正式關卡

正式 `video.json` SHA-256 `05abe8cf0cd4680a12e911feb118e6d3dec88c20dbba0f8b8e7ac65b51d0d870`；`timeline.json` `e1cceb2c0cd511f5c67b4e4c34de201036745ed20cf6e48ad7f85f9a000666e9`；`approvals.json` `4c9eeb731bf165350a5b4b2f4f2e5b916ad5702a12338ea286be7803f5d29a0a`；`pictures_hash=f8d3de2a3f752907`。候選卡尚未進入正式渲染或核准。若替換 `shot→diagram`，須另算圖像時間占比、重新盲審敘事、用未變的已核准 WAV 重綁時間軸並重新取得該時間軸的音訊核准，還須做正式播放器 CC 與連續畫面驗收。
