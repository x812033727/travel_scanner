# S52 R21｜六月三日開場光線非作者獨立覆核

2026-10-21 UTC。**史料差分 PASS；兩景書面畫面 PASS。**此結論只適用於 `video.json` SHA-256 `6d2714aa8c5fa3fd30aec85654693085afac4485efca30f69909a28d196ced36` 的紙上方案，並未驗收新生成圖、清除私有 `STOP`、放行整集續畫或替站主完成聽審／分鏡審核。[R20 HOLD](r20-opening-art-independent-20261021.md)保留為其精確版本的歷史裁決。

## 精確差分

我核對 [R21 作者回條](r21-clear-daylight-author-20261021.md)與[一葉結構化差分](r21-clear-daylight-structured-diff.json)。現檔 SHA-256 為上列 `6d2714aa…96ced36`；把唯一新值反向換回舊值，還原檔 SHA-256 **`82090b19bc31e6a218dc6b2de0304c0f5742b8f085d63156dee1de7f388414b2`**，與 R20 鎖定值相符。遞迴 JSON 比較只有 **`scenes[0].data.prompt`（`s52001`）一葉**改動：末端 `diffuse overcast light` 換成 `soft reflected light beneath the canopy`。`s52002` 整景全等 R20；相對乾淨 R19 原檔，R21 仍只差 `s52001`、`s52002` 兩個 prompt。113 景、115 句、旁白、camera、模板、卡片與 `look: {"preset":"cute-mystery"}` 未變。

`brief.md`、`research.md`、`claims.md`、`script.md` 仍分別是 R19 已獨立覆核的 SHA-256 `65f2c7c16ef4e68b07e4b65ff0f1d1977730ccddd1d4a7b26048e25ac8d036e9`、`cd3da71bdd909c2b72929e05cc09ae4b196726790c69e858c9ced736c4429e0d`、`5020e47d1501ff4faddc34f4bd6786267f90cda06127e216f61e2f3a21a64dfb`、`5c51bcff8ed8540059f6a0c456562e04223fd591cbedec0349b72ad5a29fe067`。[R19 來源與逐句回條](r19-source-independent.md)的未變部分可作差分證據；其五檔完整 SHA 的 PASS 不冒充 R21 五檔簽核。固定 Cook／Kippis／皇家學會三份本地全文的 SHA-256 仍與 `research.md` 相符。工具實算 R21 `visualHash=45e5fbd3a07a4662`，R19 為 `1d5a607b7a020c67`；R19／R21 `speechHash` 同為 `2af0a08f6e592b5d`。`node tools/video/cli.mjs lint --slug curio-s52 --json` 回 **0 errors／0 warnings**。

## 兩景來源與畫面

`s52001` 旁白是 **1769 年 6 月 3 日**庫克在大溪地岸上觀測處等候。[Cook 當日日誌 L5963–5975](https://github.com/GITenberg/Captain-Cook-s-Journal-During-His-First-Voyage-Round-the-World--13-Made-in-H.-M.-Bark--Endeavo__8106/blob/2db69c74a62f35649149b141a437a05fc0f9fdab/8106.txt#L5963-L5975)寫 **“Not a Cloud was to be seen the whole day”**。R21 改成遮棚下的柔和反射光，沒有再指定多雲；晴天的遮棚內也可有間接光，故解除 R20 具體矛盾。成年航海者、1760 年代服飾、無字紙上圓盤示意及遮蔽器材是可辨認的**概念插畫**，沒有宣稱真實肖像、精確儀器形制、可讀觀測數據或裸眼直視太陽。[1771 原報開頭](https://github.com/markjhill/2025-helsinki_cascade/blob/2ac861600a431e8cb2e2eae3b1cdcd33b7350207/data/rsc/Royal_Society_Corpus_open_v6.0_texts_txt/Royal_Society_Corpus_open_v6.0_text_106113.txt#L4-L16)亦載大型帳篷與觀測處；提示詞沒有把服飾、棚和布套標為逐項實物證據。

`s52002` 旁白說格林與索蘭德也在現場，Cook 同段明載 **“Dr. Solander observed as well as Mr. Green and myself”**。提示詞只聚焦一名成熟臉孔、穿 1760 年代衣著的成年天文觀測者調整普通器材布套，後方兩個覆蓋器材位置；單人構圖沒有聲稱現場僅一人，也沒有硬指他是哪位史人。遮棚下的 `soft indirect light` 不與晴朗日誌相反。兩景都符合系列單人行動構圖及可愛歷史**內容相關**插畫的書面要求；現有紙上文字仍不能保證模型真的畫出成年人、時代衣著或遮棚。

## 原生圖與停點

再次核對 R19 `s52001-1.jpg`／`s52002-1.jpg` 的 SHA-256 分別仍為 `4ea3178bcfd35450ce578a0d9073e0a6d06e259aa21e0c8c7018fb177460b5cd`、`49c5b8d0591304106935b2d2dcc943288c3c73978ec0986aa1bb737094c85f3d`；先前直接看原圖，兩張都是現代便服孩童，第二張是露天海灘。人工退圖不因 R21 書面 PASS 或舊機器 `passed=true` 改變。`keyframes/manifest.json` 只含這兩張、綁 R19 `visual_hash=1d5a607b7a020c67`，與 R21 不符。私有 `/workspace/.video-work/curio-s52/STOP` 存在，ledger **US$0.0270、2 image、2 judge、0 reserved**；整集既有委派上限 **US$4.46** 不變。

**下一道關卡：**依 [R19 停點](r19-native-opening-stop-20261021.md)僅各試 `s52001`、`s52002` 最多一張新圖與評審，逐張查看原生 JPEG 的成年、時代衣著、遮棚與六月三日天候；機器評分不能代替人工內容判定。新圖若過，仍須按實際狀態完成站主聽審、分鏡審核及後續成片關卡。本回條沒有進行這些動作。
