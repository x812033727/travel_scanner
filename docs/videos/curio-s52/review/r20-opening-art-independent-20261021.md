# S52 R20｜開場兩景提示詞非作者獨立覆核

2026-10-21 UTC。**書面畫面 HOLD；R20 不放行新圖。**本回條只核 R20 精確檔案及 R19 前兩張原生圖；沒有改創作檔、私有狀態，沒有清除 `STOP` 或呼叫付費服務。

## 固定差分與既有證據

我以乾淨工作樹 `/tmp/travel_scanner_curio_preprod/docs/videos/curio-s52/video.json` 作 R19 原檔，實算 SHA-256 `91a74c5fe28f6370fb76cb49640aae1af00fc24395ddeb647c54c33900ba7fac`；目前 R20 `video.json` 為 `82090b19bc31e6a218dc6b2de0304c0f5742b8f085d63156dee1de7f388414b2`。遞迴 JSON 差分確實**只有** `scenes[0].data.prompt`（`s52001`）和 `scenes[1].data.prompt`（`s52002`）兩葉，舊／新值與 [作者結構化差分](r20-opening-art-structured-diff.json)逐字相符；把兩個新字串反向換回後，原始 JSON **位元組全等** R19，反向 SHA-256 仍為 `91a74c5f…ba7fac`。113 景、115 句、scene ID、旁白、camera、卡片、其餘圖像提示詞及 `look: {"preset":"cute-mystery"}` 均未變。

`brief.md`／`research.md`／`claims.md`／`script.md` 的 SHA-256 依序為 `65f2c7c1…8d036e9`、`cd3da71b…c69e858c9`、`5020e47d…f3a21a64dfb`、`5c51bcff…5a29fe067`，與 [R19 獨立史料回條](r19-source-independent.md)的四個鎖定值相符。因此 R19 的來源、115／115 逐句主張、雙盲、政策與音訊結論可作**未變部分**的差分證據，原五檔整體 PASS 不自動移植到 R20。固定 Cook／Kippis／皇家學會本地全文的 SHA-256 亦符合 `research.md` 所列三值。工具實算 R19→R20 `visualHash` `1d5a607b7a020c67`→`afe08482b220e39f`，`speechHash` 兩版同為 `2af0a08f6e592b5d`；`lint --slug curio-s52 --json` 為 **0 errors／0 warnings**。

直接打開 R19 兩張 1280×720 原生 JPEG：`s52001-1.jpg` SHA-256 `4ea3178bcfd35450ce578a0d9073e0a6d06e259aa21e0c8c7018fb177460b5cd`，中央和後方均是現代便服孩童；`s52002-1.jpg` SHA-256 `49c5b8d0591304106935b2d2dcc943288c3c73978ec0986aa1bb737094c85f3d`，三名現代便服孩童在露天陽光海灘和儀器旁。後者沒有書面所說的遮蔽觀測處。兩張機器評審雖記 `passed=true`、10／10 與 9.29／10，人工內容仍判退，不能作可用分鏡。R20 的 `adult`、`mature facial features`、1760 年代衣著和遮蔽帆布觀測處直接針對這些問題；`s52002` 聚焦一名成年觀測者並不聲稱現場只有一人，也沒有冒稱 Cook、Green 或 Solander 的精確肖像。紙上修正尚未證明新圖能照做。

## HOLD 原因

R20 `s52001` 新提示詞結尾是 **`diffuse overcast light`**。同景旁白明定「一七六九年六月三日」，新提示詞亦明定 June 1769 的大溪地觀測場景；[Cook 6 月 3 日日誌 L5963–5975](https://github.com/GITenberg/Captain-Cook-s-Journal-During-His-First-Voyage-Round-the-World--13-Made-in-H.-M.-Bark--Endeavo__8106/blob/2db69c74a62f35649149b141a437a05fc0f9fdab/8106.txt#L5963-L5975)明說 **“Not a Cloud was to be seen the whole day”**。即使人物站在棚下，`overcast` 仍指定多雲天空，與該日記載相反；這是新引入的來源／畫面矛盾，不能因畫風或 lint 合格而放行。`s52002` 的 `soft indirect light` 只描述遮蔽下的光線，沒有同一問題。建議作者僅把 `s52001` 的 `diffuse overcast light` 換成不聲稱天空多雲的棚下間接光，再凍結新 SHA 交非作者覆核；不要順帶改旁白、時代／成年錨點或其他景。這裏沒有替作者修改提示詞。

## 私有停點與後續邊界

讀取時 `/workspace/.video-work/curio-s52/STOP` 仍存在；私有 ledger 為 **US$0.0270、2 image、2 judge、0 reserved**。`keyframes/manifest.json` 只有上述兩景，綁 R19 `visual_hash=1d5a607b7a020c67`，與 R20 新 hash 不同；manifest 的機器 PASS 不推翻人工退圖。既有整集委派上限 **US$4.46** 不變。先取得修正版的精確差分與書面 PASS，再依 [R19 停點](r19-native-opening-stop-20261021.md)逐景有限試畫、逐張檢視原生圖；網站站主聽審、分鏡審核及成片關卡仍按真實狀態待辦。本回條不清 `STOP`，不授權整集續畫。
