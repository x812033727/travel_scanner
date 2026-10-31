# S49 R27｜`moon032/033` 退件圖的私人 manifest 離線重綁

2026-10-22 UTC。**26 張既收圖綁定 PASS；`moon032/033` 紙審 PASS、原生圖尚待。**[R27 非作者紙審](r27-moon032-033-prompt-independent-pass.md)核准兩個提示詞後，本回只改私人 keyframes manifest；沒有生圖、judge、配樂或其他付費呼叫，也沒有把 R26 退件圖改判 KEEP。

## 綁定與安全界線

R27 `video.json` SHA-256 `02fdb0f2ac142634d42ac24f7108bb12424e7a4625756ca559b90d52912552a3`、`claims.md` `779a8e22e6e7e202249cf7ec645a91a7ade7139c5c0e6ee2bb70c4fa50f2bd2f`、未變的 `script.md` `82369f762cc64f70e300e2104a16af3b8e99f1e3296dd81a34152e967f0ecb0a`。以[作者可逆差分](r27-moon032-033-prompt-structured-diff.json)逐字還原，只有 `moon032/033` 兩個 `data.prompt` 回到 R26；舊稿 `visual_hash=5781d6810538eb41` 與舊 manifest 相符，現行 R27 工具計算值為 `74c5cc0713c7766d`，`look_hash=98a370ae40badbaf` 未變。

起始 manifest SHA-256 `57d169e58776fd22bb03e5c42cdda984a91bff3fcb45643baf49cc9a120e1be8`，有先前 **26 個人工 KEEP** 條目，以及 R26 機器 PASS／人工 REJECT 的 `moon032/033` 兩項。先以原檔 SHA 備份至 `/workspace/.video-work/curio-s49/rebind-backups/r26-manifest-before-r27-two-prompts.json`，在 `STOP`、jobs 空及帳本金額確認後，離線原子改寫：只將 `visual_hash` 換成 R27 值，並刪去 `shots.moon032`、`shots.moon033`；兩張退件的實際 JPEG 仍留私有區作證據。新 manifest SHA-256 **`694b319ccaaf0da0e4ed9079620945b6b95588c5a95439ec2f89d8f5d8607615`**，不含兩張退件選圖或請求鍵。原有 26 個完整條目與備份逐項相等，縮圖仍用已收 `moon006`，contact sheet 仍為空。`moon031` 仍無圖單條目，只讀 `renderPlan` 確認其輸出為「鏡筒重三千磅」來源大字卡。

## 26 張已收選圖的實際檔案雜湊

下表每個 SHA 都由私有選圖檔重新讀取，並與新 manifest 的 `sha256` 比對一致；逐項 JSON 證據在[重綁清單](r27-moon032-033-offline-manifest-inventory.json)，清單 SHA-256 `18a2d5fc31f0f39e37f1c91d919624106ee2867ae42b2e20cd41979585fa7ff4`。

| 景 | 私有選圖相對路徑 | 實際 SHA-256 |
| --- | --- | --- |
| `moon001` | `keyframes/moon001-1-trim.jpg` | `0cbf12ec1bbfa115a81b5089f56609d07a9801bf8a0cad2d4c31460824bf2683` |
| `moon002` | `keyframes/moon002-2.jpg` | `cf734518b8d85c1b8e44d13dd0585a7e1a7bf8c070b6832d2d669e6c324f9fcf` |
| `moon003` | `keyframes/moon003-1.jpg` | `c0dc2c827f76dd8b108e1e7b81c42a8ad06aa0f56f46a659ab8e0cedc2ae606d` |
| `moon004` | `keyframes/moon004-1.jpg` | `4a2b3b4eaf818e169635fd0c78d0665499032eb4727182b97d73c1dcc65aef36` |
| `moon005` | `keyframes/moon005-1.jpg` | `0a817bbdac76a92c199f5fb1a554ad44caca2ae468042a92ea0cbfa78f976d17` |
| `moon006` | `keyframes/moon006-1-trim.jpg` | `3e271b29be12a1998f87d88cc70116eb074052ef80ffb4904af37563f5c4b01a` |
| `moon007` | `keyframes/moon007-2-trim.jpg` | `f2432c7b16cab9be871f23fb947671f52ccca010d382f6b2acd6d18812a0d725` |
| `moon008` | `keyframes/moon008-1-trim.jpg` | `8139c040dc4e93058f643cf74ea00008c2177176ad6584459ce4eae7012bedce` |
| `moon009` | `keyframes/moon009-1-trim.jpg` | `6b0149bdaf83cd4f4c4b3cf3e40e7d85c0a915e934b36ec9351ed2779892042e` |
| `moon010` | `keyframes/moon010-1.jpg` | `8327f69e15437ade390f9ba2868b6856639871f9f04d91ecbdbda58eb2e5faf5` |
| `moon011` | `keyframes/moon011-1.jpg` | `5b11bed36bff63ae2038bc447819bf721aa47e8c33324d8a3a00f3ba419ef41e` |
| `moon012` | `keyframes/moon012-2.jpg` | `b214a71631577988e3f0fa51257d4c03c6ee24aee96ff52f53da2a111389da9f` |
| `moon013` | `keyframes/moon013-1.jpg` | `0bb3d4f08a8bf67d4cdc6df5938cdcc0998c322b1ac0d3abf440b81afe46ad59` |
| `moon014` | `keyframes/moon014-1.jpg` | `020e38f57cf123818e9aeca8425a9041bc9569d1a7a0887b12630b21351b0fed` |
| `moon015` | `keyframes/moon015-2.jpg` | `cbbdbda49a6e499d3d6e8d3d33721c10255389ccd8d428d92d2cbb5a30f92280` |
| `moon017` | `keyframes/moon017-1.jpg` | `9730cd91949927ff4cce4cc26bb27c0bc89b4a0b3a585250f252ba711b3a2074` |
| `moon018` | `keyframes/moon018-1.jpg` | `119fbb94e8b5651e9a053697e9f912bd44a97b081bd8fb6765f4e052a47a6a4b` |
| `moon019` | `keyframes/moon019-1-trim.jpg` | `819423ca5cfe45a55dc903d2604a96044cf077abae5dc0b58a569dd139aac315` |
| `moon020` | `keyframes/moon020-1-trim.jpg` | `a1ddc846eb0c28a6dc0ee35d3b68210b5436f766f5cb0dcc65364cd5f7e62fe3` |
| `moon021` | `keyframes/moon021-1-trim.jpg` | `6a2fb2999c01b33179c75e78c80fbd2a6451c1c76fea71ab3c658c2a2f0d513f` |
| `moon022` | `keyframes/moon022-1.jpg` | `6ef0cb929260f1146ec87df088fdce53df3cb4e8999319ece0f75f88f62efc35` |
| `moon023` | `keyframes/moon023-1-trim.jpg` | `999d7fc657a3988807994d0ee4509bda2b27e916cee79d9036cb5e82ca1cbfc4` |
| `moon024` | `keyframes/moon024-1.jpg` | `591e47dc7c2996b5460adb979338d3f59207e9bb91f97dbc4a92159fd8a345fb` |
| `moon025` | `keyframes/moon025-1.jpg` | `a56fc0b0cbba3b51630a50f18e616c54ed28deb6b0a5abdf069465354988cab1` |
| `moon028` | `keyframes/moon028-1-trim.jpg` | `48c1cf7cc044d3972ca07ecc003e3a1ffe2296e397e83efb95eb2a053b78c8cd` |
| `moon030` | `keyframes/moon030-1.jpg` | `5a5862db73081638706379b3a3ea4a279bcce05aefbc155f38973b8ac3e9d62b` |

`keyframeProblems` 對這 26 景得 **0 問題**；對完整 R27 120 個 `shot` 則仍列 **94 景未畫**，包括 `moon032/033`，沒有 `moon031` 退件圖或缺圖錯誤。這是已收圖的保全與版本綁定，**不是**全片 storyboard 核准。

私人 ledger SHA-256 `bdd5c8ebb1b7821f05532cb82af58b888424c31a98443b030a336f427d7067de` 前後相同，即 **US$1.0260／76 image／76 judge／0 reservations**，低於整集 US$5.30 上限；jobs 空、`STOP` 在位。下一步若限界重試 `moon032/033`，仍須依 R27 紙審逐張看 1280×720 原圖及裁圖，不能靠機器分數收圖。
