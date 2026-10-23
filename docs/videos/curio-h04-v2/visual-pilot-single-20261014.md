# H04 v2｜單張 MiniMax 小樣

站主解除先只做離線規劃的限制，限定 H04、H05、H06 各做一張小樣。本輪 H04 只對 `empty-speaking-room` 執行一次 `keyframes --shot empty-speaking-room --takes 1`，未重抽或擴批。送出前確認專案和上層沒有 `STOP`，以 dry-run 檢查 `image-01` 1K 提示及估價，並備份當時的 manifest。

| 項目 | 實際結果 |
| --- | --- |
| 來源 `video.json` | SHA-256 `cc74761fbe854d47e16011cae78fef032fc600f3e41aef6c502aba92d6a17658` |
| 請求 | MiniMax `image-01`，request key `3d8a5f6afadedacb`；一張圖及一次 Gemini 判圖 |
| 採用候選圖 | `keyframes/empty-speaking-room-1-trim.jpg`，SHA-256 `39a698ef3c60b51264adf8dd92e4503c1514394007dbf5afe6cfb2892db8c3c6` |
| 判圖 | 10／10，`passed=true` |
| 人工目視 | 平面 2D 空簡報室，無虛構人物或假文字；大型空白投影幕使畫面偏稀疏。只可作「發表說法後仍有問題」的通用轉場候選，未經連續影音試播。 |
| 增量費用 | 圖 US$0.0035、判圖 US$0.0100，共 **US$0.0135**；ledger 當時累計 US$2.7980。 |

原圖、送出前後 manifest、ledger、preflight 與人工結論均保存在外部 `<home>/mokaair-work/videos/curio-h04-v2/review/pilot-single-20261014/`；送出後 manifest SHA-256 `64c8d3906a06da9701e41a31b14b9418344bfd6b22514d70bef99ca1473d902e`。此張僅證明通用室內轉場能穩定做出合乎平面風格的圖，不證明雪坡、帳篷、足跡或研究模型等高風險畫面能通過來源與風格審查。

現行 49 個 `shot` 僅此鏡有圖片，其他 48 鏡仍缺圖；完整分鏡、實際連續剪輯及封面均未核准。`video.json` 的封面仍指定未通過的 `opening-question`，不可產出或送審。現行已核准旁白時間軸為 8:47.57，預定插圖占 50.3128%，最長畫面狀態 7.7 秒；這只是現有分鏡與旁白的測量，不能當作完成影片。
