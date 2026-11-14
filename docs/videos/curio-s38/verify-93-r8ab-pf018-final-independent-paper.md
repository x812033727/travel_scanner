# S38 R8ab｜PF018 第三張前最後提示詞獨立紙審

2026-10-22 UTC。**PASS，限固定史料與 PF018 提示詞的書面畫面。**這不是第三張原生圖的驗收、私人圖單重綁、分鏡或成片放行。本審只讀取檔案與執行本機 lint；沒有付費 image、judge、music 呼叫，也沒有改動私人媒體狀態。

## 來源、敘事與畫面

- 重新實算固定轉錄 `/tmp/curio-s38-pepys-4200.txt` SHA-256 `3cd43a3c39ee72eb9c4a3657f1fcb1723afba291cedac176c65a39289483be5d`。[1666-09-02 日記 L65816–65822](https://github.com/GITenberg/The-Diary-of-Samuel-Pepys---Complete_4200/blob/68fcf49f70ee793b989a6fd0464264d55beb4451/4200.txt#L65816-L65822)先記佩皮斯 `got a boat and through bridge`，再記眾人搬走 `goods`，或投入河中，或 `bringing them into lighters that layoff`。PF018 旁白「他搭船沿河看，人們正把家當搬上平底貨船。」與 `claims.md` 的 D2a 對得上；下一景 PF019 的米切爾家來源卡和旁白也未改。畫面沒有把搬箱居民當成佩皮斯，亦沒有把他在塔上的擔憂錯當目擊。
- R8ab 提示詞要一名灰髮、有面部歲月線條、寬肩的中年**成年人**，雙手把單只木箱**越過低船舷，向平底貨船甲板內放下**。單人、單物、單動作，能表達日記的財物入 `lighters`，也直接針對[首張退件](verify-87-r8z-pf018-seed1-human-reject.md)的孩童與無人裝箱，以及[第二張退件](verify-91-r8aa-pf018-seed1-fail-stop.md)的「箱子已在甲板、看不到越舷」。木箱種類、這名居民的年齡與容貌是插圖示意；日記未辨認此人或列出箱內物品。`aboard` 鏡位和空甲板沒有宣稱佩皮斯登上該貨船或該船的精確停泊位置。
- 羊毛 doublet、亞麻領和 1666 年時間標記提供時代方向；只留河水、陰天背景，減少第二張的近代制式排屋、帆布與游離索具再現空間。`full frame without black bars` 明指未裁切原圖不可有寬黑帶。這些是提示詞的**要求**，尚非圖像事實；第三張仍要直接看未裁切原圖是否真的畫出成年居民、木箱向船內越舷、可信的船型與年代、無黑帶與無游離線段。正式 judge 的 `detached` 必須過，分數也不能取代人工核對核心動作。

## 可逆差分與靜態檢查

- 獨立核對[作者差分](verify-92-r8ab-pf018-final-prompt-structured-diff.json)：當前 `video.json` SHA-256 `b955dae2c2620b7477fcdef24606d9c1696f390c927f9fc7be10aa058d0b2ae9`；其 R8ab 新字串在原始檔恰出現一次。只反填差分列出的 R8aa 舊字串後，原始檔 SHA-256 回到 `e25b7163f2efa7f830c0b94e421511ceaa4662fb985b53d2290e3a715a16556b`；再填回可逐位元復原當前檔案。解析前後 JSON 遞迴比對**只有** `scenes[17].data.prompt` 一葉不同，該景 ID 是 `pf018`。其旁白、`camera`、`visual`、景序與其他景均相同。
- `script.md` SHA-256 `e59ec137e3de3871e3b0e5063d8f6504d3eb2adb5fe22265eb3faa3d613d5951`；`claims.md` SHA-256 `f9de8d2771b62cc327f4e599f002af8f3278cfb0f39dbed201e7fdc857201d42`，與 R8aa 記錄相同。正式 `node tools/video/cli.mjs lint --slug curio-s38 --json` exit 0，`errors=[]`、`warnings=[]`、112 句。除片尾外正文 111 景有 104 張 `shot`（93.7%），最長連卡 3。工具計算 R8aa `visualHash=819c6ff2d7c16ad0`，R8ab `visualHash=7f7b8b8dda0faefa`。

## 私人停點核對（只讀）

`/workspace/.video-work/curio-s38/STOP` 在位，`media/jobs.json` 是 `{"jobs":{}}`。現行 `keyframes/manifest.json` SHA-256 `eca0cddcec00a26be05be63d6d62e6ce71f57e775595dbd74a02ba1cd5f0e507`，仍綁 **R8aa** `visual_hash=819c6ff2d7c16ad0`；只有以下 11 筆 KEEP，沒有 PF018。完整 11 筆條目以 UTF-8、不跳脫 Unicode、鍵排序的 compact JSON 重算 SHA-256 `59cb354fcf4a4d38d746e4fc49e7dd39742d248ce1094d7de4d80a95f8a6e301`，與[第二張退件清冊](verify-91-r8aa-pf018-seed1-fail-inventory.json)相同；每張入選 JPEG 都實際讀檔重算，與 manifest `sha256` 相符。

| KEEP ID | 入選 JPEG SHA-256 |
| --- | --- |
| `pf001` | `608203b99cd453ad7218d8c773c93ca92900997d2a9a73a1be44090cba60ccb0` |
| `pf002` | `5cff4f5806cc88ff4ffa5d78b59984f0cc5e618e6c8e998ad64cc20a4f84ea39` |
| `pf003` | `608203b99cd453ad7218d8c773c93ca92900997d2a9a73a1be44090cba60ccb0` |
| `pf004` | `82efccf4b92bc59da94688527fd43e9347ad45d271b048e0877a8f3337bb7921` |
| `pf005` | `34ff83a651a59ba9383091d33151ca4bce62c9d04d6f65bd4bc75dbf55e8c52c` |
| `pf008` | `8e08ff956a0f64c4243e584dc870acbfaa8ab4e77b18cabab809e42aabd03418` |
| `pf010` | `5fc7fd687ced8649ecae9b392df16383047aab399a3525786a498b6efcc65850` |
| `pf011` | `c1bc71715db707d97170cf07c02ff7d9d83b4902ca3d6b8d388ab44bd3b60466` |
| `pf016` | `4c81c46f16a8a8db0185c1fd7814b86254480948f4c02144402977cea8c3e383` |
| `pf017` | `728004748d86146993ebf2a37dbccd61afa94b9663b0316308576cfd029cb1a4` |
| `pf012` | `d45e13d382104b92cabb56a58f0d8d902db8e8938c412102d3c6053e042e3696` |

`media/ledger.json` SHA-256 `c40120e6801716b79f867d873c4d2068ca2afd51ebdf379387f9b659a011594a`；累計 US$0.7955、53 image、53 judge、1 music，另有舊 US$0.0035 reservation，低於整集 US$4.58 硬上限。PF018 已有**兩張實際付費原圖**，換 prompt 和重用 seed 1 都不重設次數。此書面 PASS 後，仍須在 STOP 與空 jobs 下先安全離線重綁 11 筆 KEEP 至 R8ab visual hash，再依既定停線只試 PF018 **第三張且最後一張**實際原圖及一次 judge；若 FAIL 或人工 REJECT，就改同章合格圖或日記來源卡，不購第四張。
