# H05 v2｜三張原生卡的離線替代候選

日期：2026-10-14。狀態：**僅供審查的離線候選，尚未接入正式 `video.json`，也未獲製作核准**。先前三鏡 MiniMax 小樣的人工結果為 0/3 採用，原圖、判圖、manifest 與帳本仍按[試拍收據](visual-pilot-05-20261014.md)保存；本候選沒有重抽、付費、改判圖結果或覆蓋原圖。

## 內容、來源與可見界線

三張 1600×900 原創 SVG 放在 [`diagrams/`](diagrams/)，只使用已寫入本地[查核表](claims.md)的事實。卡面標出來源與示意限制，並將文字留在底部字幕區之上。

| 現有 scene／line | 來源界線 | 候選 SVG（SHA-256） | 離線 PNG（SHA-256） |
| --- | --- | --- | --- |
| `open-threat`／`h5v006` | `c04`：男子**聲稱**公事包有炸彈；未確認裝置效力。只畫抽象的單一關閉公事包，沒有乘客、內部構造或真品外形。 | [`claim-briefcase.svg`](diagrams/claim-briefcase.svg) `5009b09fc2bcd5b01f3d92d18bfcf7cfc218ef26e365790b87b6290142581ca2` | `claim-briefcase.png` `d45b9b0b027669b80dce3f5ca44475d285e51e0491f70b4a2ea28ca412e02149` |
| `open-tail`／`h5v007` | `c07`：FAA 年表記機尾階梯在空中放下；航程並非落點。**只有文字方塊與事件箭頭**，不畫展開階梯、機構、人物、飛機或落點。 | [`tail-stairs-record.svg`](diagrams/tail-stairs-record.svg) `2eda86a8387f6a29f6d6463e0a8cee62412c6452637a9c85bc04e7a72f7f233c` | `tail-stairs-record.png` `1e80a21fe90d2c565fba77b40869fd724f01d985664584323af57a42367cb44c` |
| `open-boy`／`h5v008` | `c12`：八年多後，男孩在河岸沙地發現鈔票。只畫背面、無五官的匿名小剪影與抽象水／沙，不畫鈔票、真實外貌、現場照片或精確位置。 | [`river-bank-boy.svg`](diagrams/river-bank-boy.svg) `564ddcf0254b79eb137b3cacf065d9fe7a0fc9be63c1e5a1fa5174881dd417f5` | `river-bank-boy.png` `c5ee87def46d1879619089c32fd0b24b10e435bfe8b093303c2ddeb9f36d914c` |

PNG 與影片只在隔離目錄 `<home>/mokaair-work/videos/_offline-h05-three-native-cards-20261014-v2/`，沒有寫入正式 H05 media workdir。三張 SVG 已過 XML 載入與本機 Sharp 1600×900 轉圖；製作與主製作代理各自目視 PNG，卡面文字清晰，沒有假文字或虛構人物外貌。這是**候選視覺覆核**，不等同正式播放器、字幕安全區或故事節奏核准。

## 現行時間窗與比例

下表直接讀取現行 `timeline.json`，採 30 fps、半開影格區間；沒有改動旁白、scene 順序或口播文字。

| Scene | 影格區間 | 影格數 | 時長 |
| --- | ---: | ---: | ---: |
| `open-threat` | 699–832 | 133 | 4.433 秒 |
| `open-tail` | 832–989 | 157 | 5.233 秒 |
| `open-boy` | 989–1136 | 147 | 4.900 秒 |
| **合計** | **699–1136** | **437** | **14.567 秒** |

影片正文共 16,204 影格，目前 61 個插圖鏡頭占 9,490 影格（58.5658%）。若三鏡全部改為原生卡，插圖仍占 9,053／16,204 影格（55.8689%），高於 50% 門檻 951 影格（31.70 秒）。這只是比例可行性，不能替代敘事與畫面審核。

鎖定輸入：正式 [`video.json`](video.json) SHA-256 `472db853bc021374430ce5d80387442544cf72cd195f10e9e06aa86b07c94095`；正式外部 `timeline.json` SHA-256 `db2aeb68147ebda3ece14222198f71338dc6101fc27cce06099b66e147457aee`。三句原 WAV 的 SHA-256 依序為 `d1a1eeea07036d256228ac9db7c71a976ba688f18cc05f074fe472ba6499fdf6`、`92d2c58b90626335a4b4bf92f140519f63b9b796c082dc2e2f1b74ca3c82a0e2`、`fa41ca714ae40198e3c9449fa4436c26e4c8871485c56115635aa7dcac97d0cb`，與時間軸逐句紀錄相符。

## 隔離預覽與下一關

已把三張 PNG 按 133／157／147 影格接成 `three-card-isolated-preview.mp4`，直接取用 `h5v006–008.wav`，只在各句尾補靜音至既有 scene 時窗；沒有重新合成語音。SHA-256 `d4b63069fd6efb806727bb3dbc0ba73547f4227363afa4d312125e97a59b4c7e`。`ffprobe` 確認 437 影格、30 fps、影音皆 14.566667 秒，切點分別在 4.433 與 9.667 秒。另抽取兩個切點前後影格做 `boundary-contact.png`（SHA-256 `6853dd879e3a433e2ad578ad0842b8993063dca05456a1b1527f5d87de2b22f2`），目視確認卡片順序與切點正確。此環境可逐張目視與檢查編碼，無法可靠聆聽，因此仍要由人以正常速度播放整段，核對三句旁白、卡片可讀時間、切點與實際 YouTube CC 覆蓋位置。

若候選被接受，先在**隔離副本**把三個 scene 的 `template` 轉為 `diagram`、各自指向 SVG，維持 line IDs／口播／時窗；跑 script lint 與 timeline dry-run、產同長預覽，做獨立敘事與播放器檢查。正式 `video.json` 一旦改動，必須重新計算 narrative／pictures／timeline 雜湊並按流程重綁審核，不能沿用舊雜湊的核准。此處尚未執行正式修改。

剩餘鏡頭的下一個**單張** MiniMax 風格驗證候選為 `night-clouds`（`c07`／`c14`）。它用一般深色雲層與無法定位的遠方地平線測試海軍藍／青綠手繪版畫風，畫面可完全避開人物、機身字樣、證物與地點推定。正式 prompt 目前還有「遠處林地」，送圖前須先收窄為無可辨地貌、無飛機／人物／文字／鈔票／地標；另取得明確單張範圍後，只做一次生成與一次判圖，再人工目視。**這次沒有送出該圖。**
