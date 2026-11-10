# S62 R4｜獨立固定史料與書面畫面覆核

2026-10-22 UTC。**PASS：固定史料、逐句主張、書面畫面及 R3→R4 差分。** 我未參與 R4 寫作，也未讀本輪敘事盲讀者的答案。此判定不是敘事核准、原生圖片驗收、實際人耳音訊或成片核准。

| R4 凍結檔 | SHA-256 |
| --- | --- |
| `brief.md` | `9f63e8de4d158b2e4bdbfcc86579463274966d88bb548318e6bc4200615f4337` |
| `research.md` | `442cbe52e4c92f962726f4940e182bd10bedb41417cb239ede9daf008c5ea74a` |
| `video.json` | `abed73ef3b14dcfc1b8ff1804f0234919d2f03cffa70a0b4c901a72ce6b14f92` |
| `script.md` | `8343a4f903fe4b405b1e6364cd67737ed7f3aead625b5fe713bf91c873c05c14` |
| `claims.md` | `2edb12dd02afa0ed03744616fcb27e889498356709d4c1cf95be415c30914218` |
| [R4 結構差分](r4-author-structured-diff.json) | `6eb88e61d8e7220dc559302cf6b3e663fe7d392c0cb5cab9c3785fa0d7363164` |
| [R4 文字補丁](r4-author-text-diff.patch) | `1a5d445208a789ab38e5a6a8d89362cd7678181953fbd6167e7613577f19aaec` |

固定文本為 Galileo 的 1610 年 *Sidereus Nuncius* 經 Edward Stafford Carlos 1880 年英譯及編註的 [GITenberg commit `6672b6c62a0f30e9bb9b84410ef48c6698c37ea5`](https://github.com/GITenberg/The-Sidereal-Messenger-of-Galileo-Galilei--13-and-a-Part-of-the-Preface-to-Kepler-s-Dioptrics__46036/blob/6672b6c62a0f30e9bb9b84410ef48c6698c37ea5/46036-0.txt)。重驗本機固定 raw `/tmp/curio-s62-sidereal.txt` SHA-256 `74fc9b817b64bc33415c6a44100c30f48952bc531d380682e5f4f1a26cc56fb5`。`research.md` 與 `youtube.description` 均只提供這份固定英譯，沒有聲稱另有 1610 年原文掃描；譯者腳註的現代「satellite」稱法未冒充伽利略原話。

## 改動的來源核對

R3→R4 僅變動 `video.json` 的 14 個 leaf：五處懸念表欄位與九句旁白；**110 個提示詞、四張資訊卡、場景順序與鏡頭資料均逐位元未改**。`s62005` 的一月十日晴夜是原文 L1301–1313 所述九日雲天與十日兩點的待揭隊形，開場不先說十日點數。`s62006` 的幾小時後從另一點近旁顯出是 L1399–1409 的十七日記述；`s62008` 的「第一夜三點是否全部」是問句，不把未見的第四點指定身份。

`s62031`（原文 L1273–1278）所說排列近乎平行黃道有據；`s62061` 的東側最外點離木星兩角分、其餘西側較近見 L1360–1369。`s62062` 明確承認原書沒有識別首夜漏見的哪一點或交代其原因，沒有把一月十日的遮擋猜測移到首夜。`s62076` 把十七日「兩點先前可能相接」明說為**他猜**，符合 L1399–1409 的 *as I think*。`s62084` 同列一月十日／二十三日的遮擋猜測及十七日／二十四日的貼近判讀，結尾仍說不能反推首夜身份；未將兩種猜法說成那夜已證實的物理機制。`s62112` 的邀其他天文學家用夠準確的鏡筒續測周期，逐項見原文 L1258–1265；新增 G15 是研究表已定義的作者邀請，沒有填入後世周期值。

全片 **114／114** 場景 ID、旁白、`claims.md` 逐句主張及 `script.md` 同序同字；主張表 **137** 個 G01–G15 固定連結均指向同一 commit、有效行號，每列至少一個錨點。其餘未改的歷史句和圖片提示沿用 [R3 獨立覆核](r3-independent-source-visual.md)逐句 PASS 結論，本次另核差分沒有暗改其他史實。結構差分逐葉正向重播精確得到 R4 SHA，逐葉反向回填精確還原 R3 `video.json` SHA `396e78030054ee6f8a4dca15c83be8e4361dd6530bb1c8b99e75cdb3e2922ebf`；文字補丁 `git apply -R --check` exit 0。

## 畫面與技術界線

四張資訊卡仍是原書有據的 1 月 7 日、10 日、13 日隊形和出版時美第奇名稱；正文 **110／114 = 96.49%** 為插圖景，最多連續一張資訊卡。110 個不重複的原創插圖提示與主張表畫面欄逐項吻合。R4 沒改任何圖片提示；`s62061` 的無字籌碼只象徵四點，不能把籌碼間隔誤當兩角分的精密比例，數字以旁白／正式資訊卡為準。`s62084` 的遮住籌碼是「當時猜法」的象徵，不可剪成已核實的首夜身份。`s62112` 的無字書頁是原創概念景，不應畫成 1610 原始手稿或可讀譯本。後續原圖仍須檢查天體點數、成人年代、無現代鏡筒旋鈕／電燈、無冒充原圖的星圖及構圖品質。

重跑 `VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s62 --json`，exit **0**，**0 errors／0 warnings**、114 lines。R4 尚無 TTS、原生插圖、配樂或成片；敘事關卡須由兩位全新、只讀同一 R4 劇本的正式讀者另行合併。
