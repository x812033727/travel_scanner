# S58 R10｜車隊、紙法與圖爾順時修訂作者凍結

2026-10-21 UTC。**R10 作者候選，待非作者史料／書面畫面及兩位新盲讀；未有媒體或站台核准。** [R9 正式敘事合併](r9-merge/summary.md) 12／13 HOLD，兩位新讀者均否定 `no_recap`；R9 的[來源口播證據](r8-source-independent.md)與[單景書面畫面 PASS](r9-visual-independent.md)綁舊五檔，不能取代 R10 覆核。

| R10 凍結檔 | SHA-256 |
| --- | --- |
| `research.md` | `b26201dd469744fe10c8d259beb93ebcda23609fdb6bc989a6f1d784d9f9779e` |
| `brief.md` | `5afefc8547bc4fb4a597bcfc99e4e93bcec7631ad237085af78b596aa269a21f` |
| `claims.md` | `4dc0fdf5c0ee1ce70d78e77e125a83afaf2b3f52fb5d474bb5e3594aa887b503` |
| `video.json` | `f5ffe0868a570ab86b993cbdbe69014922b7447f078626e2c7294d531c21bbef` |
| `script.md` | `37dbc104268814e5cc9db7ac72f13a537b2007e9e71c4c219c1252c4a2d7d3f0` |

## R9 原票指出的修訂

- `s58015` 只講風推球、乘客不知前方落點，不重說 `s58003` 郵袋出城目的；書面畫面改為一人從籃緣看模糊地平線。[R607–648](https://github.com/GITenberg/A-Diplomat-s-Memoir-of-1870-being-the-account-of-a-balloon-escape-from-the-siege-of-Paris-and__49546/blob/d29b4c2d9670430fcc4b2e5a9e3e39a9e7542f18/49546-0.txt#L607-L648)記旋轉、無羅盤與任風去向。
- `s58062` 直接問追兵逼近後往哪藏，不再重說 `s58061` 第二車還在；提示詞改為一位攝影師回望車後道路。`s58063` 仍立即回答村長閣樓。
- `s58083` 由倒敘「離城前巴黎未收到鴿郵」改為圖爾**當下** Dagron 對紙製電文不滿意的自述，固定[D355–360](https://github.com/GITenberg/La-poste-par-pigeons-voyageurs--Souvenir-du-si-ge-de-Paris_19588/blob/d2a6e7f42a608005416d925c4fbf1f85d4dbe966/19588-8.txt#L355-L360)使用的是他的評價，未推定十月那隻鳥命運；場景畫一位郵務員看紙樣。`s58084–85` 再說紙纖維與載重原因。
- `s58089` 只說舊紙製電文停止，不重說 `s58088` 已採薄膜；書面畫面只讓一位助理把紙片收進抽屜，薄膜靜置桌上。這符合[D362–370](https://github.com/GITenberg/La-poste-par-pigeons-voyageurs--Souvenir-du-si-ge-de-Paris_19588/blob/d2a6e7f42a608005416d925c4fbf1f85d4dbe966/19588-8.txt#L362-L370)的先看薄膜樣本、後放棄紙法。
- `s58144` 用「剛剛那封求助信」明確接回一月求化學材料的鴿郵，問其進城單趟鳥程；`s58145` 答普瓦捷至巴黎十二小時，`s58146` 仍限制到私人信件未驗送達。[D394–404](https://github.com/GITenberg/La-poste-par-pigeons-voyageurs--Souvenir-du-si-ge-de-Paris_19588/blob/d2a6e7f42a608005416d925c4fbf1f85d4dbe966/19588-8.txt#L394-L404)把求助、到貨與鳥程列為同一例子，不能推成材料實際由氣球回運。

五句口播在 `video.json`、`claims.md`、衍生 `script.md` 同步，四張書面 shot 畫面隨之修正；研究與企劃內容未變。仍為 **146 景／141 插圖／5 卡**，濃縮開場 185 漢字、六章正文 2638 漢字，以每分鐘 325 漢字估 **8.12 分鐘正文**，實際時長須以 TTS timeline 驗證。三檔口播表格 **146／146 逐字連號一致**，`lint --slug curio-s58 --json` 0 error／0 warning，`npm run test:docs-videos` **236／236**，`npm run check:tasks` exit 0。沒有付費語音、插圖、配樂、合成、站台核准卡或上架。

接下來由非作者覆核固定原文、五句、四張相鄰提示詞和整體書面畫面；另由兩位未看前稿的讀者只讀 R10 劇本投固定 13 題並正式 OR 合併。任何再改稿須重凍結，不能沿用 R9 票。
