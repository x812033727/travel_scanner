# S38 R8q｜`pf009`–`pf014` 六景成人／年代提示詞，作者凍結

2026-10-22 UTC。前一批 [六張原生圖](verify-48-first-chapter-six-native-stop.md)全數人工 REJECT：孩童形象、錯誤角色與紙張、現代街景及懸吊橋。**R8q 只改 `pf009`–`pf014` 的六個 `data.prompt`，不改旁白、章節、卡片、鏡頭運動、`look.preset`、其他 106 景或已收 `pf001`–`pf005`／`pf008` 提示詞。**這是作者書面候選；沒有付費試畫或放行原生圖。

## 精確差分與來源

[逐字結構化差分](verify-49-r8q-six-prompt-structured-diff.json)記下六個舊／新 prompt 及 JSON 路徑。新 `video.json` SHA-256 **`087ae9c4cdbb8dea3430cd505d42624e06deca0a94b77e71c49164fbbcc2f4db`**；依 diff 把六個新 prompt 逐一換回舊字串，位元組 SHA-256 精確回到 R8p **`8db80e07bffff8863f949e4a458b9fed0a891e36ed93063bce59c3915fc6e142`**。`claims.md`、`research.md`、`script.md` SHA-256 分別仍為 `f9de8d2771b62cc327f4e599f002af8f3278cfb0f39dbed201e7fdc857201d42`、`f838518cf2c4ab23de91021ae6024d9431f907866c14301466ca0a06bb3ecdfe`、`e59ec137e3de3871e3b0e5063d8f6504d3eb2adb5fe22265eb3faa3d613d5951`。

固定的 [佩皮斯 1666 年 9 月 2 日日記 L65795–65844](https://github.com/GITenberg/The-Diary-of-Samuel-Pepys---Complete_4200/blob/68fcf49f70ee793b989a6fd0464264d55beb4451/4200.txt#L65795-L65844)逐句支持以下動作。衣色、臥室家具、木窗及石拱橋形制是年代感示意，不宣稱日記逐項記載；畫面不得憑此新增火源位置、書面報告或已確認的熟人房屋損失。

| 景 | 史料界線與本次改法 |
| --- | --- |
| `pf009` | 日記說他看完火**回床再睡**。新 prompt 將一名成年佩皮斯放在窄木床與毯下，睡袍接上已收 `pf008`；火仍遠且尚未天亮。去掉泛稱 clerk、地板坐姿的歧義。 |
| `pf010` | 約七點他起來穿衣、再從窗邊看，當下覺得火更小、更遠。新 prompt 將一名穿 1660s 日服的成年人物放在木框窗邊，遠處只見微弱火光；不加第二名兒童或現代街道。雙面呢上衣與亞麻領是示意，不是日記記下的服裝細目。 |
| `pf011` | Jane **聽說**三百餘屋被燒，然後口頭告訴他。新 prompt 只畫一名成年女僕在門邊以空手急報，刪掉容易把轉述畫成文書的雙人互動。人物年齡不作精確歷史宣稱。 |
| `pf012` | 佩皮斯聽到消息後「made myself ready presently」去塔上親看。新 prompt 改為成年人物在門邊披外衣的一個動作，承接立即出門；沒有紙條、手冊或第二名錯置女性。披風是普通示意，日記未指明它的款式。 |
| `pf013` | 他在塔樓高處**親見**橋那端房屋起火，但此時只掛念 Michell 家。新 prompt 讓成年人在塔的石平台看舊 London Bridge 遠端房屋火；石拱輪廓旨在排除生成的近代橋型，不標出熟人家已燒。 |
| `pf014` | 橋邊的火令他掛念熟人；燒毀其屋的確認要等到 `pf019` 上船以後。新 prompt 以成年人物抓石欄、遠處河邊屋頂煙氣表現擔心，**不再要求橋體入鏡**，避免近代吊索橋與過早宣告某戶已燒。 |

六景全以景別／地點時間／單一成年人物的一個主動作／視線或物件／柔光為主句，不在 `data.prompt` 寫 cartoon、chibi、flat、negative 等畫風或否定附句。`pf011`、`pf012` 刻意只見一人；Jane 與佩皮斯的口頭交接由相鄰兩鏡與旁白建立。這解決已觀察到的主動作及人物錯誤，但模型仍可能再畫出童貌、紙張或現代道具，必須直接驗收下一張原生圖。

## 本輪檢查與交接

`VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s38 --json`：**0 errors、0 warnings**，112 句與估 10.016 分鐘未變。六景 `keyframes --dry-run --takes 1`：MiniMax `image-01` ready，提示詞長度 247–323 字／各上限 1068–1072，六張首輪含評審約 US$0.08；這只是報價，**沒有發出生成請求**。私有 `STOP` 仍存在；ledger 仍 **US$0.4615／29 image／28 judge／1 music**，另有舊 `pf003` US$0.0035 reservation，整集硬上限 US$4.58。舊 manifest 仍綁前版 `visual_hash`，其中 `pf009`–`pf014` 的機器分數與人類退件均**不是** R8q 新圖；舊原圖已保存在私有 `review/pf009-014-rejected/`。

下一步由**另一位**讀者核對 [逐字差分](verify-49-r8q-six-prompt-structured-diff.json)、日記口頭／親見層級、年代示意、既收六景的未改提示詞與預算。若獨立紙審通過，再在 STOP 的 EXIT 邊界內，只抽 `pf009`–`pf014` 各一張並逐張看原始 1280×720 圖。此作者頁不授權清除 STOP 或推整集分鏡；網站音訊／分鏡、片頭片尾、成片 QA 與 Studio 可點連結仍待完成。
