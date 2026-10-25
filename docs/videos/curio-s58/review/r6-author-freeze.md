# S58 R6｜來源歸屬、問答與片尾窄修作者凍結

2026-10-21 UTC。**R6 作者候選，尚待新一輪非作者史料／書面畫面覆核、兩位無前情盲讀與正式合併；不是媒體製作 PASS。** [R5 正式雙盲 OR 合併](r5-merge/summary.md)為 13／13 YES、官方 CLI `passed:true`，但[A 票](r5-blind-a.md)保留 `payoffs` NO，[B 票](r5-blind-b.md)保留 `no_recap` NO；[R5 獨立來源覆核](r5-source-independent.md)則因 `s58108` 的操作者歸屬判 HOLD。作者在 R5 全部原票和官方紀錄封存後才修 R6。

| R6 凍結檔 | SHA-256 |
| --- | --- |
| `research.md` | `b26201dd469744fe10c8d259beb93ebcda23609fdb6bc989a6f1d784d9f9779e` |
| `brief.md` | `5afefc8547bc4fb4a597bcfc99e4e93bcec7631ad237085af78b596aa269a21f` |
| `claims.md` | `f69dace9c1bc7434564da46fbcd74146a453a3bf253781dacfd86bec254f3ccd` |
| `video.json` | `0ece21cb763b15b9ce2d2cc96d363c789c5f1021bd9a52856d17c0119b51b37b` |
| `script.md` | `c1e6e201108663a6c3af9c7c96e56ad07e3fe73b60e4f13f017c8d044aeaec10` |

## 相對 R5 的修訂

- `s58068` 的問題限為倖存器材**先藏進什麼東西運離村子**，`s58069` 以空酒桶直接回答，不再暗示酒桶穿過之後 Arcis 稅卡。`s58071` 保持 R5 的史料界線：桶在稅卡前留於小村。
- `s58108` 明說「**達格隆說，薄膜夠輕，郵務機關最多能讓一隻鴿子帶十八片**」，把 *l'administration* 的操作歸屬與 *jusqu'à dix-huit* 的上限放回固定 [D420–424](https://github.com/GITenberg/La-poste-par-pigeons-voyageurs--Souvenir-du-si-ge-de-Paris_19588/blob/d2a6e7f42a608005416d925c4fbf1f85d4dbe966/19588-8.txt#L420-L424)；研究檔 P09 和企劃同步。圖仍是一位郵務員與幾片無字薄膜，不把攝影師畫成親手裝鳥，也不要求圖數出十八片。
- `s58140` 現問**請求裡指定的寄回方式**，`s58141` 直接回答「請搭第一個離城氣球」，`s58142` 仍明說實際回運載具未記，`s58143` 才講六天後材料到達；不再向觀眾發出來源無法回答的實際路線問題。
- 刪掉原最後 `s58147` 重複「逐封私信何時送到」的口播與一張插圖；結尾留在 `s58146`，只說 Dagron 的十二小時是一段鳥程，沒有量出每封私信的抵達時間。R5 原句已封存在盲讀及作者收據，沒有重編其餘場景 ID。

## 作者檢查與下一關

`video.json` 為 **146 景、141 個 `shot`、5 個 `big`**（插圖占 96.6%），與逐句 `claims.md`、衍生 `script.md` **146／146** 場景 ID 連號且口播逐字相同；系列 `look`、20 組 `loops`、配樂、片頭與 21 秒片尾設定未動。濃縮開場 183 漢字，六章正文 2691 漢字；按較快每分鐘 325 漢字估 **8.28 分鐘正文**，真正時長仍以 TTS timeline 為準。`lint --slug curio-s58 --json` **0 error／0 warning**；`script --slug` 已重產，`npm run test:docs-videos` **236／236 pass**。R6 未使用語音、插圖、配樂或合成，沒有推送站台核准卡或私有 YouTube 上架。

下一步由非作者重查四項變動及 146／146 引文、書面提示詞；兩位新盲讀者只看 R6 劇本作 13 題，正式固定 OR 合併後才重新評估是否可進一步製作。任何再改稿都會改變本五檔 SHA，不得沿用先前票。
