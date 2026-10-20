# S42 MiniMax 三幕原圖試作與停手紀錄（2026-10-20）

## 精確範圍與來源

本輪依既定插圖加配樂上限 **US$3.44**，只試 `md001`、`md010`、`md041` 各一張 MiniMax `image-01` 1K 原圖及其評審；沒有跑完整 83 幕。試作前逐幕核對固定 1874 年英譯編纂本 `/tmp/s42-74723-0.txt`（SHA-256 `d5c8c5548d57576da07be543263e06f2a20c71f6431222a6c28dc2e5338f9a5c`）：

| 幕 | 來源與提示詞覆核 | 結論 |
| --- | --- | --- |
| `md001` | 皮加費塔記船在維德角因缺糧停靠，派小艇上岸取物資，交換後才拿到兩船米（6524–6534，`Q11`）。原 prompt 的 `wicker rice basket` 可能暗示船上已有米，且甲板場景寫 `mild window light`。 | 只改此幕 `data.prompt`：`a wicker rice basket` → `a visibly empty wicker basket`；`mild window light` → `mild daylight`。空籃仍是非史料實物的卡通示意。 |
| `md010` | 匿名葡萄牙同行者記五船由塞維亞出發、航向香料群島，再經加那利往西南（2705–2722，`Q01`）。空白航圖和未指名領航員是畫面示意。 | 原 prompt 可用作試作；無史料聲稱有這張實存圖。 |
| `md041` | 皮加費塔記維多利亞號先揚帆駛出少許，等特立尼達號起錨；後者進水，維多利亞號折返（6030–6040，`Q08`）。 | 原 prompt 的兩船相對位置有據；不應額外畫出第三船。 |

此變更只有 `video.json` 的 `md001.data.prompt` 一個欄位：前版檔案 SHA-256 `f2ac5565a573e8992e8206cc295314b3e4d8db3bdf4950b74dad1e8404b097f2`，現版 `8b8dd7b5a9754938693f758bdf3c90622a1b815ff72d6dd7c5becd19b56bfb50`；`visual_hash` 由 `26f6ef8eecb8d6de` 變成 `e3f8c90add4303e5`。口播和 `speech_hash=3acd5c6589fcf04c` 未變，`script.md` SHA-256 仍為 `ddccd9cdf418412bbcaa5159ae9ad6fe6acb4cabbde76a70640405e65b5d7b4c`，現有敘事／音訊結果仍綁原口播。`lint` 0 errors、1 個既有片尾未口播訂閱提醒。改圖後 `review-pull --gate script`、`--gate audio` 都回覆等待站主；沒有把 pending 當成核准。

## 一 take 生成與原尺寸圖

`keyframes --slug curio-s42 --shot md001,md010,md041 --takes 1 --dry-run` 顯示三張、無 end frame、MiniMax `image-01` ready、估 US$0.04、原媒體 ledger US$0.00。正式命令只對這三幕各畫一 take，並各做一次 Gemini 評審。所有原圖是 **1280×720 JPEG**，保存在工作目錄，不在 Git：

| 幕 | 原尺寸檔案與 SHA-256 | 自動評審 | 人工原圖覆核 |
| --- | --- | --- | --- |
| `md001` | `/workspace/.video-work/curio-s42/keyframes/md001-1.jpg`；`39ad26e0eeaa5fa69b3371ab9a74293803bde207f1ef810526f87aa0c1cb6620` | **FAIL 9/10**：船身有可讀字，人物在碼頭而非船上。 | 籃子確實空，但船是現代白色機動渡輪，與 1522 年帆船情境直接衝突；不接受。 |
| `md010` | `/workspace/.video-work/curio-s42/keyframes/md010-1.jpg`；`4355ee7a5be8b25ba5b08e416d4cd8e0035edfad6e2dafeb72b5b151d680b6f4` | **FAIL 7.59/10**：3D 光滑風格、人物似兒童、航圖不是空白。 | 現代船艙與星徽帽、已繪航圖都偏離原 prompt 的非具名示意；不接受。 |
| `md041` | `/workspace/.video-work/curio-s42/keyframes/md041-1.jpg`；`7617bcd38fd83157142148141f34024dd20bade195336bb48c14535e7bfe49d2` | **PASS 10/10**。 | 前景船之外，背景左、右還各有一艘船，容易讀成三船；與此處僅維多利亞號和特立尼達號的敘事不合。保留原圖待共同人工驗收，不自行接受。 |

評審 1／3 PASS，但原圖出現跨場景船舶／人物時代與船數錯誤，已按試作停手條件 **STOP 後續付費插圖**。`keyframes` 因 `md001`、`md010` 未過評審以 exit 1 結束；聯絡表因容器缺少 Playwright 對應 Chromium 未產出，原尺寸圖和逐幕 manifest 均完整可讀。沒有對失敗幕重抽，也沒有送 storyboard、製作配樂或成片。

精確 `keyframes/manifest.json` SHA-256 `58ff8f197d56dd084ec6eeaf190bc5c01f453fba3f0be1b055cd6d48f884b5d6`，保留每張 take、評語和 `needs_review`；`media/ledger.json` SHA-256 `7e1c5ffdacdf972e6427dabadc2fe96d8d615176b1a31fa3c7a39ea53ac8b42b`，三張圖各 US$0.0035、三次評審各 US$0.01，合計 **US$0.0405**，無保留中請求、無音樂支出，低於 US$3.44 上限。三張原圖路徑已送主協作者共同驗收；擴量須先處理這批時代與船數錯誤並重設提示詞試作。
