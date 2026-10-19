# S24 R2 無付費修訂稽核｜2026-10-19

R1 的盲讀及初稿檢查保留在 [verify-1.md](verify-1.md)；本頁只記修訂版。**R2 尚待另一位獨立讀者對凍結劇本重新盲評**，以下檢查不充當敘事核准。

## 固定來源與界線

| 來源 | 修正後的固定頁面 | 重開結果 | 下載文本 SHA-256 |
| --- | --- | --- | --- |
| 維特魯威《建築十書》英譯，第九書序言 9–12 節 | [E8011–8054](https://github.com/GITenberg/The-Ten-Books-on-Architecture_20239/blob/67fd1f31ae255b0f32efe423a950203d9b25bbe8/20239.txt#L8011-L8054) | HTTP 200 | `7daafe23aeef2377fe9a99bc285c5dfc0673440487ab43f78387312b6799304d` |
| 同書拉丁文 | [L27275–27310](https://github.com/GITenberg/Vitruvii-De-architectura-libri-decem_51812/blob/78eb1eed88044d5cac42a3dd811d5806e4e04cfb/51812-0.txt#L27275-L27310) | HTTP 200 | `b4fce89b0c304c7d1f26b299bf2dfcddbab8529c883f43ad1e75fae564daa861` |
| 普魯塔克〈馬塞勒斯傳〉英譯 | [P19090–19131](https://github.com/GITenberg/Plutarch-Lives-of-the-noble-Grecians-and-Romans_674/blob/6aea7c6d83ee3596f9106d2d832d705aa4ed4620/674.txt#L19090-L19131) | HTTP 200 | `11a1bb9a5d5a8436f2d4d7adf3ad91ec05bb8aef850e564ce255cf9ba2fabdd1` |

R1 的 E／L 網址漏了 GitHub 倉庫尾碼 `_20239`／`_51812`，回 404。R2 在 `research.md`、`claims.md`、`video.json` 和系列任務中更正，並把 P 的固定來源列進 `video.json`。E／L 是同一本書的兩種文字，不能算兩名目擊者；P 的所讀段落講希羅、機械及滑輪拖船，沒有金冠或浴盆，沉默也不能反證浴盆故事。銀、金、皇冠的排水比較及希臘字 `ευρηκα ευρηκα` 均歸屬維特魯威後來的敘事；拉丁文 `dicitur` 位於等重金銀塊的方法段，不在奔跑喊話句。逐句映射與物理推論限制見 [claims.md](claims.md) 及 [research.md](research.md)。

## 敘事與畫面修訂

- R1 的 `no_recap` 未過：原片尾只重說 `ac090`。R2 讓 `ac096` 提問還缺哪類證詞，`ac101` 才回答「獨立的當場見證」；正文留下問題，片尾補出具體證據缺口。仍需新讀者判讀。
- 新增 `ar201`–`ar205`，順著同一只容器、滿水起點、整件浸沒、取出後定量補水，說明三輪比較能量到什麼。新增 `ar206`–`ar207` 釐清第九書序言與 `dicitur` 的位置；`ar208` 把 P 的滑輪拖船敘事說清楚。均在 `claims.md` 逐句標明文本與推論。
- `crown-007`、`crown-030`、`crown-031` 改為浴場外街上奔跑喊話，人物下半身由前景牆遮住；`crown-032`、`crown-ab005`、`crown-033` 刪去浴場中尚未入水的皇冠；`crown-ab011` 不再畫逐寸描皇冠曲線。`crown-ap002` 畫滑輪而非空白圖；拖船鏡頭讓人物坐在船的遠處，對應 P19113–19125。
- 書頁段穿插古代書寫、街景、滑輪拖船及現代三輪水量實驗；空白／無字頁面只用來指向文本，沒有要求圖片模型寫希臘字。全部 101 個 `shot` 提示詞仍是說明插畫，沒有聲稱為古代實物或當場攝影。

## 本地一致性與時長

- `video.json`：102 景，其中 101 個插圖鏡頭與 1 個片尾；104 句旁白、104 個唯一 ID。`claims.md` 104 行按 ID 和文字與 `video.json` **逐行一致**；`script.md` 與工具的 `screenplay(video.json)` **逐字一致**。
- 工具估長 568.83 秒（9 分 28.83 秒）；開場 41.00 秒，片尾 19.50 秒，**去掉兩者的正文 508.33 秒（8 分 28.33 秒）**，超過系列 8 分鐘正文下限。這是估算，正式旁白長度需錄後檢查。
- `node tools/video/cli.mjs lint --slug curio-s24 --json`：0 errors、0 warnings。`npm run test:docs-videos`：236/236。`npm run check:tasks`：2079 份任務檔通過，只有其他任務既有提醒。
- R2 `script.md` SHA-256：`91e6dd826faa20446e5e2a706848ca1ccf3d64f39bf692d0fd6e38a4bbdafc0a`。沒有產生或購買語音、插圖、配樂；接下來應由另一位讀者以此劇本雜湊獨立盲評敘事、來源與畫面。
