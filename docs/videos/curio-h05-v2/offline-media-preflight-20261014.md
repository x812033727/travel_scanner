# H05 v2｜免費媒體預檢收據

**版本註記：** 本文件的主稿 SHA-256 74102087...、正式時間軸與字幕收據是 open-note 改成原生 diagram **之前的歷史快照**。修訂後主稿 SHA-256 c14695ef580539006621e24e1f3f25e0d9ffcb2ba399eea9fdd7d69aa2edbd1f；用原 WAV 樣本重算的 108 cues 和 SRT／VTT 位元內容雖相同，新版輸入 SHA 收據在 [open-note-diagram-revision-20261014.md](open-note-diagram-revision-20261014.md)。正式時間軸和後台核准仍須重綁。

日期：2026-10-14。以下是**單張付費小樣之前完成的離線預檢**；預檢未修改主稿、語音、核准紀錄、正式 `keyframes/`、`frames/` 或 `captions/`，也未取得付費圖片。其後唯一一張 MiniMax 小樣及人工退件另見 [visual-pilot-04.md](visual-pilot-04.md)。主稿 `video.json` SHA-256 `74102087ca465c7c73044e1182671641965cc19cbd6f4d0470d11fcb9c16e6e3`；現行核准時間軸 SHA-256 `8128f74e74f2dad44ea0c6a1465f2a333c4cb30d0b7f9cfb14829f414becd984`，`narration.wav` SHA-256 `8b519d908e7b85d7d214288d3bf8c7ebb5bc897456a4b32c74143cff50253ba3`。本輪 `lint --slug curio-h05-v2 --json` 為 0 errors、0 warnings。

## 繁中字幕正文時間預檢

用目前工具 `tools/video/core/captions.mjs` 的 `buildCues`、`checkCues`、`toSrt`、`toVtt`，直接對核准時間軸及 108 句現行稿計算：**108 cues、0 缺句、0 讀速／寬度／重疊問題**。隔離輸出在 `<home>/mokaair-work/videos/curio-h05-v2/_receipts/caption-body-preflight-20261014/`：

| 檔案 | SHA-256 |
| --- | --- |
| `body.zh-TW.srt` | `b4d584b70568d201d842ad5a45d4262993b41a7bafa5b06a22e7662ab9262de2` |
| `body.zh-TW.vtt` | `d70d6c531f4fe277829f955399270c7bb4803d71d743867ae581423b4e90e7dc` |
| `receipt.json` | `71c7b56ef00af819dbc4ce7e279ede096462635f78e6c6e71bfad8a71b059f0e` |

同目錄 `receipt.json` 記錄輸入雜湊、第一／最後一個 cue 與問題清單；可重跑的單次本機程式在正式工作目錄的 `_tools/caption-body-preflight-20261014.mjs`。**這不是正式可上傳 CC。** 正式 `captions` 階段會讀成片 `checks.json` 的品牌片段安排，把片頭的時間位移納入字幕；目前尚無完整成片，`tools/video/core/stages.mjs` 因此會拒絕該指令。成片後須正式執行 `captions`，重新核對 `captions/manifest.json`、字幕內容與實際播放。

## 既有來源卡版面

在另一隔離目錄 `<home>/mokaair-work/videos/_offline-h05-native-20261014/`，複製現行 93 景及三張已登記 FBI 原件照；**只從隔離副本的縮圖設定移除仍無可用圖的 `boy-bank` 背景引用**，其餘 JSON 欄位經結構比對完全一致。副本 SHA-256 `fe6fb230d99b5a87d220c9bb92b3c3f529ce568499aea35968d079e9d3ab7fb5`；三張照片副本 SHA 與 `asset-register.md` 原件登記逐一相符。執行本機 `render --file ... --workdir ... --channel msedge` 畫出 **46 個原生卡／照片狀態、0 版面錯誤**。`frames/manifest.json` SHA-256 `61c28c0ca50c7894eaf2d870d901c614fab191796a4e282a2e0d478eaa2f1ee4`；`contact-sheet.png` SHA-256 `c6524c68e28d4102bea7806cf551707b39c9048516a94121f77306a37f7b0e9d`。

人工看完整聯絡表，並逐張打開四個照片卡畫面（機票使用兩次，另有贖金、領帶）及研究方法卡：原件沒有被裁掉，卡片署名可見，方法卡字完整。圖內右下角的 `credit` 約在 y=800/1080；真正貼近底部 CC 的是獨立主圖說 `caption`，約在 y=900/1080。預檢正文時間軸中須特別檢查的四個畫面如下；品牌片段加入後絕對時間會位移。

| 照片卡 | 正文時間（秒） | 旁白句 ID | 播放器檢查點 |
| --- | --- | --- | --- |
| `open-ticket` | 4.733–9.833 | `h5v002` | 票面姓名與主圖說 |
| `ticket-original` | 185.133–189.367 | `h5v038` | 第二次出示機票的主圖說 |
| `money-serial-match` | 273.033–277.633 | `h5v056` | 贖金圖說與來源署名 |
| `tie-original` | 322.333–327.467 | `h5v067` | 領帶圖說與來源署名 |

`photo` 場景只提供 `image`、`caption`、`credit`、`tilt` 等資料；`tools/video/templates/templates.mjs` 將 `credit` 固定在照片右下角 `bottom:14px`，將 `caption` 固定在照片下方。**沒有場景欄位能把來源署名上移。** 直接刪掉 caption 會改變照片框高度與資料說明，不能當作已驗證的 CC 修正；本輪沒有動主稿。正式字幕和播放器尚未產生，因此這四處的安全區仍待成片開 CC 實看。若確實互蓋，需要明確的版型設計與重渲染，再重做受影響關卡。隔離縮圖沒有正式使用資格；主稿縮圖仍指向未核准的 `boy-bank`。

## 一張 MiniMax 代表小樣的檢查點與結果

選現行 `open-note`：這是第一個需要讀懂「手遞無字紙條」的情境鏡頭，能測先前三輪失敗的假字、額外人物／道具、手部形貌與擬真風格漂移。其後只生成一張，對照現行 `look` 與該鏡 `data.prompt` 進行正常 judge 與人工完整圖實看；結果雖獲自動 PASS，仍因人物與紙張構圖不符而人工退件，詳見 [visual-pilot-04.md](visual-pilot-04.md)。不能從此圖推論相鄰三鏡連戲、其餘 61 鏡或縮圖可用。

下一個正式關卡仍是可用 `keyframes` 全組及 storyboard 核准；之後才是完整 `render`、`assemble`、正式繁中 CC、11 項 `qa`、成片播放與上傳包。
