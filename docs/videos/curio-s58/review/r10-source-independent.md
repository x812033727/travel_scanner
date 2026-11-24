# S58 R10｜獨立史料與書面畫面覆核

2026-10-21 UTC。**PASS：R10 五檔固定版的史料、逐句對照及書面畫面。**本收據只覆核固定文字與尚未生成的提示詞；兩位 R10 新盲讀與正式敘事合併仍須另行判定。它不代表原生圖片、TTS、配樂、成片、付費媒體或網站核准。我未修改五份創作檔，也未生成或購買媒體。

| R10 凍結檔 | 本次 SHA-256，與[作者凍結](r10-author-freeze.md)逐字相同 |
| --- | --- |
| `research.md` | `b26201dd469744fe10c8d259beb93ebcda23609fdb6bc989a6f1d784d9f9779e` |
| `brief.md` | `5afefc8547bc4fb4a597bcfc99e4e93bcec7631ad237085af78b596aa269a21f` |
| `claims.md` | `4dc0fdf5c0ee1ce70d78e77e125a83afaf2b3f52fb5d474bb5e3594aa887b503` |
| `video.json` | `f5ffe0868a570ab86b993cbdbe69014922b7447f078626e2c7294d531c21bbef` |
| `script.md` | `37dbc104268814e5cc9db7ac72f13a537b2007e9e71c4c219c1252c4a2d7d3f0` |

## 固定原文與全稿

我從 `research.md` 所列的三個固定 Git 提交重新取得 D／R／C 原始檔，HTTP 200，原始位元組 SHA-256 依次為 `e9940ca3ae2050679816be212feeab4e0c29048646dd18aa7bcb77e7160ee1ea`、`ae2c78eb08b76fdac59b91ebdf6b6a187f8ef18649e4d78d461f140467bdb7f7`、`2fd3c34981595102e3f91878d50e22b90eee5737c26bbb714548cb9b9ca9c31b`，皆與研究檔一致。D 的雜湊是 Latin-1 原始位元組；解碼只供閱讀。D 是 Dagron 的當事人報告，R 是 Reitlinger **十月另一球**的親歷，C 是後寫的二手背景；C 不獨立驗證 D 的數字或送達。

`claims.md`、`video.json`、衍生 `script.md` 各有 **146／146** 個 `s58001` 至 `s58146` 連號 ID，三檔每句旁白逐字一致。`video.json` 是 **141 `shot`／5 `big`**；141 個提示詞非空。我逐景讀了 141 個書面提示詞及相鄰旁白，未見新聲畫矛盾；五張排版卡的數字、日期與歸屬也與口播相合。`claims.md` 有 150 個直接來源連結，指向 D／R／C 的 20 個不同固定行號區間；每個連結的庫、提交、檔名及行號界線皆有效，沒有未固定的其他網址。

## R10 五句與相鄰畫面

| 景 | 原文、口播及書面畫面判斷 |
| --- | --- |
| `s58015` | [R607–648](https://github.com/GITenberg/A-Diplomat-s-Memoir-of-1870-being-the-account-of-a-balloon-escape-from-the-siege-of-Paris-and__49546/blob/d29b4c2d9670430fcc4b2e5a9e3e39a9e7542f18/49546-0.txt#L607-L648)記球旋轉、無羅盤、任風去向；[R542–552](https://github.com/GITenberg/A-Diplomat-s-Memoir-of-1870-being-the-account-of-a-balloon-escape-from-the-siege-of-Paris-and__49546/blob/d29b4c2d9670430fcc4b2e5a9e3e39a9e7542f18/49546-0.txt#L542-L552)亦直說不知會抵達何處。旁白只說未知落點，提示詞是一名乘客從籃緣望向模糊地平線；不重述 `s58003` 的郵袋任務，也不畫確定目的地。 |
| `s58062` | [D166–195](https://github.com/GITenberg/La-poste-par-pigeons-voyageurs--Souvenir-du-si-ge-de-Paris_19588/blob/d2a6e7f42a608005416d925c4fbf1f85d4dbe966/19588-8.txt#L166-L195)記敵兵取走第一車、眾人帶第二車逃、敵兵追趕，隨後村長藏他們於閣樓。旁白在 `s58061` 車已逃後只問「追兵又近；他們能躲在哪裡？」；畫面一位攝影師回望倖存車後道路，`s58063` 立刻回答藏處。無第二次報車輛結果或虛構交火。 |
| `s58083` | [D355–360](https://github.com/GITenberg/La-poste-par-pigeons-voyageurs--Souvenir-du-si-ge-de-Paris_19588/blob/d2a6e7f42a608005416d925c4fbf1f85d4dbe966/19588-8.txt#L355-L360)寫圖爾先做紙縮拍並稱該服務不盡滿意。R10 口播明說「達格隆認為」，只呈現他的當下評價；未把該段巴黎之前未收鴿信推成十月某隻鳥的命運。提示詞是在圖爾桌前檢視無字紙樣的一位郵務員；`s58084–85` 再交代纖維和載重。 |
| `s58089` | [D362–370](https://github.com/GITenberg/La-poste-par-pigeons-voyageurs--Souvenir-du-si-ge-de-Paris_19588/blob/d2a6e7f42a608005416d925c4fbf1f85d4dbe966/19588-8.txt#L362-L370)先記負責人看過既有薄膜樣本，再說電文的紙製攝影被放棄。`s58088` 已說採用薄膜，`s58089` 只說舊紙法停下；提示詞只有一位助理把紙片收進抽屜，薄膜靜放桌上，沒有第二個動作或可讀原件。 |
| `s58144–46` | [D394–404](https://github.com/GITenberg/La-poste-par-pigeons-voyageurs--Souvenir-du-si-ge-de-Paris_19588/blob/d2a6e7f42a608005416d925c4fbf1f85d4dbe966/19588-8.txt#L394-L404)以同一例子敘述 1 月 18 日鴿郵求化學材料、24 日到波爾多工作間，以及一隻鴿子由 Poitiers 飛至 Paris 用十二小時。`s58144` 的「剛剛那封求助信」明確接回此例，畫面只有一隻返城鳥在冬日田野上空，**無包裹或路線圖**。`s58145` 卡片標示「普瓦捷→巴黎／Dagron自報12小時」，`s58146` 限定為鳥程，不推成每封私信的抵達時間。`s58141–43` 也只把搭離城氣球列為寄送**請求**，不推定材料實際運具；六天不是鳥的飛行時間。 |

`node tools/video/cli.mjs lint --slug curio-s58 --json` 實跑 **0 error／0 warning**，工具估全片 13.77 分鐘、146 句；實際旁白正文與成片時長仍須由將來 TTS timeline 驗證。`npm run check:tasks` 目前因兩份無關的 S57 R10 `tasks/done` 檔仍標 `status: open` 而 exit 1；本覆核未改它們。`git diff --check` 通過。R9 對未改聲畫的[書面視覺覆核](r9-visual-independent.md)與 R8 對固定來源的[覆核](r8-source-independent.md)僅作交叉參照；本次 PASS 綁定上表 R10 五個 SHA，若再改稿須另行覆核。
