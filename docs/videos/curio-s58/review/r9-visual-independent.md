# S58 R9｜單景書面畫面獨立覆核

2026-10-21 UTC。**PASS：R9 五檔固定版的 `s58144` 書面畫面窄修通過，R8 的視覺 HOLD 已消除。**這是未生成插圖的文字覆核；不代替兩位 R9 新盲讀及正式敘事合併，也不代表原生圖片、語音、配樂、成片或網站核准。我未修改五份創作檔，也未生成或購買媒體。

| R9 凍結檔 | 本次 SHA-256，與 [作者凍結](r9-author-freeze.md) 相同 |
| --- | --- |
| `research.md` | `b26201dd469744fe10c8d259beb93ebcda23609fdb6bc989a6f1d784d9f9779e` |
| `brief.md` | `5afefc8547bc4fb4a597bcfc99e4e93bcec7631ad237085af78b596aa269a21f` |
| `claims.md` | `35c33785728e092c6f4d4a22c9076f05cee92b7bdde36ca2563cad2db0fb142b` |
| `video.json` | `b392e57b9056df90ccda3242b95ca659aaa0395348b8c0c2210984fe885e3924` |
| `script.md` | `d9bd044c1261ab76f3ad32a098e8c50aadfc05473d223aac3d61a621223afd6d` |

## 差異與來源界線

以 R9 `video.json` 的新 `s58144.data.prompt` 換回 [R8 收據](r8-source-independent.md) 所引舊字串，重新計算的 SHA-256 **正好是 R8 `video.json` 的 `aa7415ade3e74e658a21fdf953eae7d7867c6f65cad62b224c03e203c2dbb390`**；因此這個替換足以完全復原 R8 位元組。其餘四檔 SHA 未變，尤其 `script.md` 與 R8 完全相同；R8 對口播來源的 PASS 可沿用至此相同文字。此次再核 `claims.md`、`video.json`、`script.md` 的 **146／146 ID 與口播逐字一致**；仍是 146 景、141 `shot`、5 `big`。

[D398–404](https://github.com/GITenberg/La-poste-par-pigeons-voyageurs--Souvenir-du-si-ge-de-Paris_19588/blob/d2a6e7f42a608005416d925c4fbf1f85d4dbe966/19588-8.txt#L398-L404)是 Dagron 當事人回報：1 月 18 日在 Bordeaux 用鴿郵求化學材料，**請**巴黎聯絡人以首個離城氣球寄出，1 月 24 日材料到工作間；同段另記一隻鳥由 Poitiers 至 Paris 飛十二小時。材料實際回運載具沒有紀錄，六天請求至到貨也不是鳥飛行時間。D 的這些速度與到貨描述仍只歸屬 Dagron，沒有獨立行政統計佐證。

| 相鄰景 | 書面畫面判斷 |
| --- | --- |
| `s58143` | 排版卡只寫「1月18日請求／24日材料到」，旁白說相隔六天；不畫材料搭何種載具。 |
| `s58144` | 新提示詞是 **“one pigeon flies alone over winter fields, no parcel or route map”**。它跟旁白問的「鴿子單趟飛行」相合；沒有 R8 的收包裹動作，也沒有讓鳥搬運化學品、給未記的信件或羽管、偽造路線圖。冬日田野是可愛概念插圖，不聲稱精確目擊地點。 |
| `s58145` | 排版卡明列「普瓦捷→巴黎／Dagron自報12小時」，只回答鳥程，不回指 `s58143` 的材料六天。`s58146` 再把時間限定在一段鳥程，未推成每封私信的送達時間。 |

這三景的聲畫分界現在清楚；**R9 書面畫面 PASS**。原生圖片若把禁用的包裹或路線圖畫出來，仍需依系列圖片驗收規則處理，這份文字 PASS 不能替代圖片驗收。

`node tools/video/cli.mjs lint --slug curio-s58 --json` 實跑 **0 error／0 warning**、工具估全片 **13.83 分鐘**；`npm run check:tasks` exit 0（只有既有任務佔用／scope 警告）。沒有付費媒體或網站核准。若五檔再改，這份精確 SHA 收據不自動套用到新版。
