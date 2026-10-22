# S53 R38｜`s53029` 九月十六日完工數來源卡獨立書面覆核

2026-10-22 UTC。**PASS，限 R38 現行 `s53029` 來源卡及 `claims.md` 同列。**我不是 R38 作者；直接讀固定 Survey 原文、R37 最後一張退件與獨立原尺寸判定、R38 實檔、精確差分及私有停線狀態。本 PASS 不等於已回綁圖單、解開 STOP、選入退件圖或完成後續製片；本次沒有更動 `video.json`、`claims.md`、私有檔、付費媒體或 Git 暫存。

## 固定來源與事實界線

固定 `/tmp/s53-sf-relief/56217-0.txt` SHA-256 `d627ed287d8a93b9c00225ea47dbdc4f97c36089a890192a602b993c3c185b72`。1913 年 *San Francisco Relief Survey* 版權頁 L225–230 標示 `MCMXIII`／`Copyright, 1913`；[D L4858–4865](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L4858-L4865) 先交代 1906 年 8 月宣布建屋計畫，原句是 `Building began September 10, and on the sixteenth 20 cottages in Hamilton Square were completed. At least two or three months, however, intervened before any considerable number of houses could be made ready for the refugees.` 因此 9 月 16 日、Hamilton Square、20 棟「完工」有直接文字支持；後句談的是相當數量的小屋備妥供難民使用，**不是**說 20 棟當日已入住，也不能反推 20 棟當日全無人使用。

R38 主文「9 月 16 日，漢密爾頓廣場 20 棟完工」忠實限定地點與完成數。上標「1906 年｜舊金山漢密爾頓廣場」承接來源段落年份；下標「1913 年《舊金山救濟調查》｜英語原文意譯」清楚交代後出來源，不冒充 1906 年原始公告或現場影像。字卡和 claims 註記均不把 20 棟說成全市總數，也不暗示 9 月 16 日已入住。

固定口播仍是「六天後，漢密爾頓廣場**先**完成二十棟。」這個「先」在 `s53028` 的 9 月 10 日開工、`s53030–s53031` 的後續備妥問題之間，讀作早期的完工里程碑；它沒有在卡面或 claims 擴寫為「全市首批／僅有 20 棟」。`s53031` 既定「大批小屋，**得再過兩三個月才**備妥」以「得…才」表示至少尚需這段等待，與原文 `At least two or three months` 相容；其 `大批` 對應 `any considerable number`。這兩句皆是 R37 已固定口播，本次沒有改寫或重錄。

## 精確版次、字卡與系列界線

現行 `video.json` SHA-256 `212aa5d440e5c6075af9341ab271e40323d81537cd229acf693f17fc3d2bdc31`；`claims.md` SHA-256 `e8892539610547dc8e6242b441b1028f6bb5865b2dd25e9c1fc9f05234285fed`；[R38 精確差分](r38-s53029-september16-source-card-structured-diff.json) SHA-256 `2726d88cdac9f355f0abcdcb3370994d9cd70eec053200a39919ca62a39314df`。我逐值核對差分 `after` 與實檔：124 景僅 `scenes[22]`／`s53029` 由 `shot` 換成 `big`、提示詞改為來源卡文案，其他 123 景不變；`claims.md` 僅第 29 行同列畫面註記改動。舊／新場景的 line ID、文字、語氣完全相同。按實檔 `ensure_ascii=false`、兩格縮排、尾端換行的 JSON 格式，把 `before` 場景反填，逐位元組得 R37 `video.json` SHA `7df8145a61b6ef66d3c65d75e89ea85aa30b6ec28fec217c114e7a05a81d59b6`；把 claims 舊整行反填，逐位元組得 R37 `claims.md` SHA `50704b954f87256796a9690ef47b12e0bcd0491633ad2645cf9b3e6e310e07b3`。差分可逆且沒有隱藏的其他景改動。

`script.md` SHA-256 仍為 `64ffcd8c0e89c4596a7fd08d41bd74f8a16f55fbc9acc2f41d7f9b914ea300fc`。我用正式 `loadProject`／`speechHash`／`visualHash` 重算：126 句、`speechHash=05c4d9a79a8708b4`、R38 `visualHash=a01a13ea3f3bc672`。私有 `timeline.json` SHA-256 `c75c8bde15f7220862ba8083d6590b7b14bb71c456f896f7b58c13352c88a054` 仍記同一 speech hash；`narration.wav` SHA-256 `08444d50c2f8b70a7079701e157397d9a7c23d08971727164df91a1101e281e1`。實跑 `VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s53 --json`：exit 0、**0 errors／0 warnings／126 lines**。正文排除 outro 後共 123 景，其中 **111 `shot`／90.2%**，高於 70%；最長非 shot 連續段只有 `s53028–s53029` **2 張**，低於最多 3 張。

我用實際 `slideHtml`、本庫 theme／Noto 字型及本機 Chromium 對 R38 卡片做 1920×1080 本地畫面檢查，無遠端請求或付費產圖。煙測截圖 `/tmp/s53-r38-s53029-card-smoke.png` SHA-256 `252edb99fd8597c35353db31fdc870da87dea4efb53eda8ee645ae8356c05a1d`，僅供本次紙審，並非正式影格或新選圖。主文 22 字元在 190px 分成兩行，`word fit` 未縮字、未報 overflow；下標 22 字元維持 48px，整體 `.content` 的 scroll/client 均為 1728×778，畫面沒有裁字或字卡碰撞。主文在「漢密爾／頓廣場」之間換行，略欠整齊，但上標完整寫出「漢密爾頓廣場」，兩行均可讀。我判為**輕微排版註記，非可讀性 HOLD**；此處不阻礙來源卡判讀。

## R37 退件、18 KEEP 與停線

[R37 最後一張 STOP](r37-s53029-third-native-stop.md)與[不同作者原尺寸判定](r37-s53029-third-native-independent-visual.md) SHA-256 `e1948470c6862ec1b5c2881b06dc2d23c036c1eb4221ef86a7e66418e906ded4` 已將第三／最後實際原生圖 HUMAN REJECT：原圖 SHA `0228ae5924703f57255ea2ed13d0ebcc44d5ec2d775f49b41fbc42233b568716`、所選修裁 SHA `de872537dc5febf0f8d21f65027ae437aff28270020dd070730603e17eee4920`。R38 改來源卡符合「不得買第四張」與沒有退件圖可收的結論。

目前正式私有 `keyframes/manifest.json` SHA-256 `674e1ca36d3d028ddd120b2c93737b52f55d41ab83d8f644d8835303c5b287d3`，仍綁 R37 `visual_hash=eb73bd967a3b4a7d`，**尚未回綁 R38**。我逐筆對照 [R37 STOP inventory](r37-s53029-third-native-stop-inventory.json) SHA-256 `dca470c6d626cb8f41e9ab69bfba8f1d62fcef744365ddee96fcc88a414c5c40` 的 18 筆 `prior_keep`：ID、所選路徑、SHA、request key 全相同；現存 18 個所選 JPEG 實檔 SHA 全吻合，18 筆 judge `passed=true`、`needs_review=false`；有效圖單沒有 `s53029`。所選 SHA 如下：

| ID | 所選實檔 SHA-256 |
| --- | --- |
| `s53002` | `e17678ab3fd82acd649e9f691f44530e1afdf2a3bc49a2492d753ec2df905690` |
| `s53003` | `73823edb92173cf2df2be0f4988f6a25fd3c1044d9387041602c2e171a3f2f2b` |
| `s53004` | `17c28641f67e3452e7a08a6255e502dc551da79982dd94d037eadd0adf7cfaa6` |
| `s53005` | `55acdbb1a0db155710d578e9e36ec881c09317c6900ee27b86612331fa3b44b0` |
| `s53006` | `5b73da5203ed2ac04c8f87d49053ef2af92f6e73313999d7a2a15c3d4180fb9c` |
| `s53007` | `73823edb92173cf2df2be0f4988f6a25fd3c1044d9387041602c2e171a3f2f2b` |
| `s53008` | `e1dfd630cf38cf6fc007eb110e3956c5b82a6af9280a37a72b18ba9b68b3a5f6` |
| `s53009` | `b957cf0aeee02ea366e48a64c973ca4d38bf41c676e249f0610be841bf641799` |
| `s53011` | `812d2941450d2a57d5c11c928b5d4514859723fa491efc779a26aac11207b406` |
| `s53014` | `290c0b20d56f3acd3168e1c749bb243580504613c5062c48abba11cf43199b4d` |
| `s53015` | `2e63e543f40b7dc000fd1a00dfd42c25f0cac7d53fd6dc58818436a589e728a9` |
| `s53017` | `40170d8eb8c2b63517c8a455257a58ec377a03d24d592e1409807e7dc548f278` |
| `s53020` | `1954d9dd33a86bfd87b6b6deda88580e0fd568b1dfd26eadc7f24c8212aa626e` |
| `s53021` | `2dde34b31fe93a2b676df73dc25fa8304d13413e56aa8560824f2c9cff438bc1` |
| `s53023` | `f13e14b86dc5717ecfad7ae7b4b2c332fd63daf7ed94a06abf5aff1e15e1503f` |
| `s53024` | `b297b0078061392271ec4c8c2fdee606469aa87a2397d2850bdad43a754967a5` |
| `s53025` | `16e9f62963e0cb17c614b0c90ca76e76ee93a4755c85983d8f90962810dea9c3` |
| `s53027` | `1b1f054057a8fe506086112fe03b8fccc266245833998042d77014f277c49349` |

私有 `media/ledger.json` SHA-256 `168c8be9e142222df00780bbee50957126207875d14894aaee0551e1e256e0b5`，我逐筆重加 101 條：**US$0.6750／51 image／50 judge／0 預約**，低於本集 US$4.78 上限。`media/jobs.json` SHA-256 `a9d2c69ab3cb5704417b4f0968a7d8d0dae6eb0e35d37e053463220b30d55ca3`，`jobs={}`；`STOP` 存在。後續若採用 R38 畫面，須在 STOP 下另做安全離線備份、回綁新 `visualHash` 與 18 KEEP 核對，不能把本紙審當成圖單已更新或下一景付費媒體的完成證明。
