# S58 R8｜獨立史料與書面畫面覆核

2026-10-21 UTC。**HOLD：R8 口播史料與逐句對照通過，`s58144` 書面畫面尚未通過。**本結論只審固定來源、五檔文字和未生成的畫面提示詞；不代替兩位新盲讀、原生圖片、語音、配樂、成片或網站核准。我未修改五份創作檔，也未生成或購買媒體。

| R8 凍結檔 | 本次 SHA-256，與 [作者凍結](r8-author-freeze.md) 相同 |
| --- | --- |
| `research.md` | `b26201dd469744fe10c8d259beb93ebcda23609fdb6bc989a6f1d784d9f9779e` |
| `brief.md` | `5afefc8547bc4fb4a597bcfc99e4e93bcec7631ad237085af78b596aa269a21f` |
| `claims.md` | `35c33785728e092c6f4d4a22c9076f05cee92b7bdde36ca2563cad2db0fb142b` |
| `video.json` | `aa7415ade3e74e658a21fdf953eae7d7867c6f65cad62b224c03e203c2dbb390` |
| `script.md` | `d9bd044c1261ab76f3ad32a098e8c50aadfc05473d223aac3d61a621223afd6d` |

## 固定原文與全稿

我從 `research.md` 三個固定 Git 提交重新取得 D／R／C 原始位元組，三份皆可讀，SHA-256 分別為 `e9940ca3ae2050679816be212feeab4e0c29048646dd18aa7bcb77e7160ee1ea`、`ae2c78eb08b76fdac59b91ebdf6b6a187f8ef18649e4d78d461f140467bdb7f7`、`2fd3c34981595102e3f91878d50e22b90eee5737c26bbb714548cb9b9ca9c31b`，與研究檔相同。D 的雜湊是 Latin-1 **原始位元組**，解碼只供閱讀。D 是 Dagron 當事人自述，R 是 Reitlinger 十月另一球乘客親歷，C 只是後寫的二手背景；C 不能獨立證明 D 的容量、速度或送達。

`video.json` 有 **146 景／141 `shot`／5 `big`**；141 個 shot 提示詞皆非空。我逐景讀過 141 個書面提示詞與相鄰旁白。`claims.md`、`video.json` 和衍生 `script.md` 的 **146／146 ID 自 `s58001` 到 `s58146` 連號且口播逐字一致**。逐句表有 **150 個直接來源連結、21 個不同固定行號範圍**；全部落在 D／R／C 對應固定提交、檔名和原文長度內。五張排版卡的名稱、日期、數字仍有口播與來源界線。`look` 為 `cute-mystery`，141／146（96.6%）景是插圖，卡片沒有讓圖像模型生成可讀原件。

## R8 修改的來源與畫面

| 位置 | 獨立核對 |
| --- | --- |
| `s58005–s58011`，尤其 `s58006` | [R510–600](https://github.com/GITenberg/A-Diplomat-s-Memoir-of-1870-being-the-account-of-a-balloon-escape-from-the-siege-of-Paris-and__49546/blob/d29b4c2d9670430fcc4b2e5a9e3e39a9e7542f18/49546-0.txt#L510-L600)說籃子載了郵袋和鴿郵主管、氣球已升起但仍由地面牽住，籃子過屋頂才鬆繩；[R759–792](https://github.com/GITenberg/A-Diplomat-s-Memoir-of-1870-being-the-account-of-a-balloon-escape-from-the-siege-of-Paris-and__49546/blob/d29b4c2d9670430fcc4b2e5a9e3e39a9e7542f18/49546-0.txt#L759-L792)記乘客稍後用腿繫紙讓一隻鳥飛向巴黎。`s58006` 現問郵袋和鳥任務為何不同，提示詞畫**仍繫住**的吊籃與關著的鳥籠；它沒有提前說郵袋已出城或已放鳥。 |
| `s58034–s58037` | [D84–107](https://github.com/GITenberg/La-poste-par-pigeons-voyageurs--Souvenir-du-si-ge-de-Paris_19588/blob/d2a6e7f42a608005416d925c4fbf1f85d4dbe966/19588-8.txt#L84-L107)明寫 Dagron 乘 *Niepce*，約六百公斤器材同乘；同時出發的 *Daguerre* 帶三位乘客、郵件、鴿子及其餘器材。R8 先講「另一球／自己那球」的負載，`s58037` 才以工具卡寫兩球名字；畫面沒有把 Reitlinger 十月球畫進這趟十一月旅程。 |
| `s58038–s58046`，尤其 `s58042–s58045` | [D119–140](https://github.com/GITenberg/La-poste-par-pigeons-voyageurs--Souvenir-du-si-ge-de-Paris_19588/blob/d2a6e7f42a608005416d925c4fbf1f85d4dbe966/19588-8.txt#L119-L140)記兩球遭射擊、*Daguerre* 落在農舍牆並被敵方騎兵俘獲，Dagron 的球為逃脫而急升，舊棉布壓艙袋破裂後才用盤子逐次倒沙。配合 [D84–107](https://github.com/GITenberg/La-poste-par-pigeons-voyageurs--Souvenir-du-si-ge-de-Paris_19588/blob/d2a6e7f42a608005416d925c4fbf1f85d4dbe966/19588-8.txt#L84-L107) 的器材分裝，`s58042` 說**那球的機器沒隨他抵 Tours**是有界線的後果敘述；沒有推定另一球乘客傷亡。`s58043` 畫飛行員抓壓艙袋，`s58044` 問舊袋能否撐住，`s58045` 才畫袋裂，順序相合。 |
| `s58138–s58146` 口播與卡片 | [D398–404](https://github.com/GITenberg/La-poste-par-pigeons-voyageurs--Souvenir-du-si-ge-de-Paris_19588/blob/d2a6e7f42a608005416d925c4fbf1f85d4dbe966/19588-8.txt#L398-L404)支持 1 月 18 日自 Bordeaux 用鴿郵請求巴黎聯絡人以首個離城球寄化學品、24 日材料到工作間；實際回運載具未證。D 同段另報一隻鴿子飛 **Poitiers→Paris** 用十二小時。`s58143` 卡片只列六天請求與到貨，`s58145` 卡片標 Poitiers→Paris 與「Dagron自報12小時」，`s58146` 不把它擴為逐封私信時間。這些**文字**界線成立。 |

## 阻擋：`s58144` 書面畫面仍接上一個事件

[`video.json` 的 `s58144`](../video.json) 旁白現問「他另記下一段鴿子單趟飛行，那一段用了多久？」；但同景提示詞仍是 **“one workshop assistant receives a small plain parcel”**。它緊跟 `s58143`「18 日請求／24 日材料到」六天卡，又緊接 `s58145`「Poitiers→Paris／12 小時」卡。畫面重演**材料到貨**，並未呈現該景所問的**鳥單趟飛行**；連切兩張卡時，容易讓觀眾把十二小時讀成材料包裹返程，甚至以為包裹由鴿子帶走。D398–404 只給材料到達日、未給材料實際載運方式；十二小時只屬鳥的 Poitiers→Paris 一段。這個風險是提示詞與新旁白的接續，不是史料文字錯誤。

**窄修建議：**只把 `s58144` 的 shot 提示詞換成單隻無包裹、無可讀地圖或文件的返城鴿子，表明 Poitiers→Paris 的鳥程；保留 `s58143` 的六天材料卡及 `s58145` 的十二小時鳥程卡。改動 `video.json` 後須重新凍結五檔並由非作者覆核改動；本份 R8 五 SHA 的書面畫面結論仍是 HOLD。不得以本收據啟動付費媒體或網站核准。

`node tools/video/cli.mjs lint --slug curio-s58 --json` 實跑 **0 error／0 warning**，工具估全片 13.83 分鐘；實際時長仍待將來 TTS timeline。Lint 不會抓到上述意義上的畫面錯置。
