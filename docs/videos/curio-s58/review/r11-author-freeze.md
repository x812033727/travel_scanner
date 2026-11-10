# S58 R11｜重複與片尾順時修訂作者凍結

2026-10-21 UTC。**R11 作者候選；待新的獨立史料／書面畫面覆核與兩位新盲讀，未有付費媒體或站台核准。** [R10 正式敘事合併](r10-merge/summary.md)為 12／13 HOLD，兩位讀者共同否定 `no_recap`；B 另指出片尾時間順序倒退。R10 的來源／畫面 PASS 只約束其舊五檔，不能代替 R11 覆核。

| R11 凍結檔 | SHA-256 |
| --- | --- |
| `research.md` | `b26201dd469744fe10c8d259beb93ebcda23609fdb6bc989a6f1d784d9f9779e` |
| `brief.md` | `5afefc8547bc4fb4a597bcfc99e4e93bcec7631ad237085af78b596aa269a21f` |
| `claims.md` | `db0457996d4a99337e56c5b763986e1621286b258eeec1bbac9c0d1668b47aa9` |
| `video.json` | `c3464296eea71e0e65d93dc52340bec4720a8c4c9eb55e5db10e837070955d8b` |
| `script.md` | `eff9457c6d99f680b4dc5d17b10f2ec5f68504f905631590bfb0e333b3e548b9` |

## R10 原票指出的窄幅修訂

- `s58055` 章尾直接問帶箱子穿過佔領區如何躲避首次搜查，不再重說 `s58053` 的氣球破損與 `s58054` 的地面續行。書面畫面改為一位攝影師在村道旁握著關閉的相機箱、遠方只有士兵輪廓。
- `s58097` 刪去已在 `s58093` 提過的機器遺失，改講團隊把製片流程調得更快、更省成本；`s58099` 保留圖爾郵政檢查員監督，單獨提出日產量問題。[D372–386](https://github.com/GITenberg/La-poste-par-pigeons-voyageurs--Souvenir-du-si-ge-de-Paris_19588/blob/d2a6e7f42a608005416d925c4fbf1f85d4dbe966/19588-8.txt#L372-L386)為 Dagron 自述的製作與郵政安排，需按原文重核細節。
- `s58143–45` 先問、再回答一月求助信**單趟**普瓦捷至巴黎的鳥程，最後才給一月十八日求助、二十四日材料抵達波爾多的六日間隔；`s58146` 明說單趟鳥程無法量出每封私人信件的送達時間。`s58143`、`s58145` 的排版卡跟隨新順序。這些都是[D394–404](https://github.com/GITenberg/La-poste-par-pigeons-voyageurs--Souvenir-du-si-ge-de-Paris_19588/blob/d2a6e7f42a608005416d925c4fbf1f85d4dbe966/19588-8.txt#L394-L404)中的 Dagron 回報；材料的實際回運載具仍未記明。

四處口播改動在 `video.json`、`claims.md` 與衍生 `script.md` 逐字同步；研究、企劃內容未變。**146 景／141 插圖／5 卡**，濃縮開場 185 漢字，六章正文 2609 漢字，按每分鐘 325 漢字為 **8.03 分鐘正文**；實際時長須由語音時間軸驗證。三檔口播表格 **146／146 逐字連號一致**，`lint --slug curio-s58 --json` 為 0 error／0 warning，`npm run test:docs-videos` **236／236**，`npm run check:tasks` exit 0。

新一輪非作者須以這五份精確 SHA 重新查核口播、固定原文與全部書面畫面；兩位不看作者或舊票的盲讀者各自只讀 `script.md` 和固定 `NARRATIVE_PANEL`，再用官方固定 OR 合併。任何改稿都須重凍結。
