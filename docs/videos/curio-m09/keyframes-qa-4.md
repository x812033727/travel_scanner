# M09 分鏡送審前獨立驗收

日期：2026-10-16（Asia/Taipei）。本收據只確認本機分鏡狀態，**不代表**站主已核准；驗收員沒有呼叫付費工具或送後台。

## 綁定快照

- `video.json` SHA-256：`9F52ECF207849E0892F5F75DAF0C42DF9078E78D8899297ED5E464D0D9814363`。與上一版相比只把 `epicyclic-idea` 的插圖改為 `big` 數字卡；95 句旁白文字未改。**磁碟上舊 `script.md`** SHA-256 仍為 `DB36B91ADE79E1B6AD06633889C4B42D07E45730D39518DB4E85F6F2C0F09C6F`，但它尚未反映此次模板變動，不可沿用舊劇本核准。
- 本機 `<home>/mokaair-work/videos/curio-m09/keyframes/manifest.json` SHA-256：`7DC31CF579B3C8634279A0744050B27F1783BE2282CAF85E3B2D34E96B3E0251`，`visual_hash` 為 `a4e622988e97ffa0`。清單的 86 個 ID 與 `video.json` 的 86 個 `shot` 完全一致，86 張選圖檔都存在、SHA-256 與清單相符，86／86 的 `judge.passed` 均為 `true`；無遺漏或多出鏡頭。
- 四頁聯絡表均在同一 `keyframes/` 目錄，依序為 `contact-sheet-01.png` 至 `contact-sheet-04.png`；SHA-256 前 12 位依序是 `c89c09db54dd`、`315677061ff5`、`0fe78104bc9b`、`1fc2e3ce03ce`。四頁共 24＋24＋24＋14 張，已逐頁以原表尺寸查看；未見新選圖在聯絡表中缺漏、張冠李戴或明顯脫離系列可愛卡通畫風。這是聯絡表目視，不宣稱本輪把其餘 85 張全部再次放大。

## 兩個前輪阻斷鏡頭

| 鏡頭 | 現版觀察與判定 |
| --- | --- |
| `node-explain` | 選圖 `node-explain-2-trim.jpg` SHA-256 `7d54bb56ad9f7b2394b76d1d5a4826896a841756be53fa04558baf0c832e7251`，已放大看原圖。白紙上兩條不同方向的曲線有清楚交點，旁白所說「月球軌道穿過太陽視路徑的位置」可被畫面理解；沒有冒充出土零件或寫入錯誤字樣。人物手指指向紙張左上而非交點，與提示詞手勢不全合，但旁白沒有說人物手指正碰交點，不構成事實矛盾；評審 9.29 分的細節意見保留供站主查看。**內容通過。** |
| `epicyclic-idea` | 多輪插圖始終只有單圈，已改為 `big` 卡，主文「2 種圓周運動」、提示「行星逆行的問題」、副標「古代幾何方法｜Freeth 等 2021」。前後 `not-constant`、`gear-on-gear` 仍是插圖，不形成連卡。卡片忠於該鏡「兩種圓周運動疊在一起」旁白及 `M09-C20`；`claims.md` 的 C20 指向 S3 〈Period relations and ancient Greek theories〉，`video.json.sources` 列出 Freeth 等 2021 原論文。`big` 是單一數字／短語的既有模板，三欄均為簡短文字；本輪以 lint 驗證欄位，未把概念卡說成已渲染的機械圖解。**語義與版型通過，成片仍須抽看實際渲染。** |

## 系列門檻、費用與下一關

- 全片 93 景：正文 92 景（排除 1 個 `outro`），其中插圖 86 景、數字卡 6 景；插圖占 **86／92＝93.48%**，高於 70% 下限，最長連卡 **1**，低於 3 張上限。六張 `big` 卡都用於單一數字／短語，沒有把連續解說大段搬上字卡。
- `node tools/video/cli.mjs lint --slug curio-m09`：0 errors，只有研究者 37／86、房間 31／86 兩項原有畫面詞頻 warning。當前 86 張選圖都可供站主看分鏡；QA3 的兩個阻斷已解除。
- 依協調者工具帳本，本集圖片與評審估算 US$3.034，連同旁白／音訊 QA 為 US$3.734／6.000；本輪清單刷新新增 0 圖、0 評審。另有 US$0.0135 暫留帳本待協調者核銷，以上都不是供應商最終發票。
- **分鏡內容已具備送審條件，但先暫停 `review-push --gate storyboard`。** `status --slug curio-m09` 仍把磁碟上的舊 `script.md` 顯示為已核准，卻同時指出 `storytelling panel: stale`。現版 `video.json` 的 narrative hash 為 `641e4a838667ec96`，舊 `script.md` 尾端為 `b4c3ba3318fe39b9`；`narrativeHash()` 明確把場景模板納入，所以 `shot`→`big` 會使正式劇本內容雜湊改變。協調者須重建劇本、做獨立敘事複核並取得站主對新版劇本的核准，然後再送分鏡。成片、最終 QA、上傳包仍是後續關卡。
