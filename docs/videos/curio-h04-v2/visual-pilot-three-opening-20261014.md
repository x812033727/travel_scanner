# H04 v2｜MiniMax 開場三鏡小樣

站主在每支各一張小樣後，准許維持 MiniMax，再對每支影片各做三張相鄰鏡頭、每鏡只試一次。本輪 H04 限定 `opening-search`、`opening-inside`、`opening-gear`。送出前確認專案與上層無 `STOP`、沒有執行中租約，三鏡一 take dry-run 均通過；`video.json` SHA-256 `cc74761fbe854d47e16011cae78fef032fc600f3e41aef6c502aba92d6a17658`，旁白時間軸 SHA-256 `65e48861f66a7437ba3218a6601c89a1b52040a03fbcc5252ebdc5278fc2bc71`，現行旁白核准仍綁定此時間軸。沒有重錄或改動分鏡來源。

| 鏡頭 | 本次檢視圖 SHA-256 | 正常判圖 | 人工與獨立覆核 |
| --- | --- | --- | --- |
| `opening-search` | 選圖 `opening-search-1-trim.jpg`：`9ea0c9144848f5517f632d1074a84ecebd26027ebb43ce423bba91799ec08094` | 9.29，通過；判詞已指出人物不在下坡遠處 | **退件**。兩名搜救者在帳篷旁／上坡側，右側有樹線，未達「無樹廣坡、從遠處朝空帳篷看」的構圖；不能當史實還原。 |
| `opening-inside` | 本次原圖 `opening-inside-1.jpg`：`d7e3c3f89d3c2804f08438dcc5bdd01bc659c0ad334b55b6957e90a2b1bf481d` | 9.71，**未通過**；`style=0`，帳布呈厚重繪景 | **退件**。雖看得出空帳篷，材質與光影偏動畫背景畫，無法接前鏡的平面插畫。 |
| `opening-gear` | 本次原圖 `opening-gear-1.jpg`：`652fe2dd4e35f7123a91ff03d66b1cf9f3a4ca32190c8187aaf037e63e1e4f64` | 9.29，通過；判詞已指出非正上俯視、衣物堆疊 | **退件**。從帳門斜看而非頂視，衣物未分放，帳篷開口、顏色與前鏡不同，不能當同一空間的連續鏡頭。 |

三張圖各只呼叫一次 MiniMax `image-01` 和一次 Gemini 判圖，帳本增加 **US$0.0405**（每張圖 US$0.0035、每次判圖 US$0.0100），從 US$2.7980 到 US$2.8385；圖數 209→212、判圖數 207→210，沒有預留費。第三個 CLI 指令結束碼 1 是先前 `opening-inside` 的品質失敗被彙總回報，第三張本身確實產出並判圖。正常分數及 `needs_review` 原樣保留，沒有覆寫判詞。

前後 `video.json`、manifest、ledger、state、送出前 preflight 與本次原圖／選圖的 SHA 收據保存在外部 `<home>/mokaair-work/videos/curio-h04-v2/review/pilot-three-opening-20261014/`；後段 manifest SHA-256 `ca3b472a15f7c5b1c45b7a33fb9489b00755c5162afaa4fe49e694459632c02e`、ledger SHA-256 `ea284f4d6d4c64955b6897f1fcd0709652d57c28cd831f3a63f6ddc0b5b9f2ec`。工作目錄的 `opening-inside-1-trim.jpg` 與 `opening-gear-1-trim.jpg` 是 **10 月 13 日舊檔**，本次 manifest 指向新的原圖；舊裁邊檔另以 `stale-` 名稱封存，不能誤算為本輪合格圖。

本輪 **0／3 通過人工連續畫面審查**，也未做帶旁白的連續影音試播。先離線修分鏡：遠景要明確人物與帳篷的上下坡位置、視線軸線；若 MiniMax 仍無法穩定處理，就改無人物的氛圍景加來源卡。帳內兩鏡宜共用同一平面示意／自製 SVG，明標「示意」，以已登錄的 1959 卷宗第 385／386 頁及來源卡承擔鞋衣、足跡主張。這些改法需重新計算至少 50% 生成插畫時長及最長 8 秒狀態，現行僅多約 50 格餘裕。不得依兩張 judge PASS 擴批，也沒有把三張退件圖納入可用的完整分鏡。
