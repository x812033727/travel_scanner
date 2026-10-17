# A01 round14 來源與伏筆回收獨立覆核

日期：2026-10-17（台北）
結論：**PASS_DELTA_ONLY；整片敘事、正式機實稿與付費製作仍 HOLD。**

本覆核只評估 round13 → round14 的兩句旁白、三筆 loop 變更及四處企劃片語。候選 `manifest.json` 的 SHA-256 為 `9c2b6a69360c0f701fb28043e2e1179b6cda83c6e90a91253e14224b66245162`，其中釘選的 `delta.json` SHA-256 為 `4c32d5734de4dfd5abfdfebdaddcc103a30992402d03a4c1311c9761ad447b4b`。manifest 另釘選六章、series、source map 與 validation 的逐檔雜湊；`node build.mjs --check` 通過，預覽為 79 景、108 句、lint 0 error／41 warning、cute-story 0 error。這些是離線候選與機械檢查，沒有替代正式審稿。

## 史料邊界與敘事判讀

| 變更 | 判讀 |
| --- | --- |
| `hook-07/y9b6` 問「那家人的自製輪子箱，還有一只留到今天嗎？」 | 問的是家族是否有**一只**留存，沒有把片頭 1928 年旅程示意箱與館藏品指成同一物。 |
| `origin-06/83ew` 答「有。溫尼特卡歷史學會的館藏裡，保存著安妮塔的一只自製輪子箱。」 | 館方將物件 `2005.26.576` 標為安妮塔的 1927 年箱子；館方另記述家族於 1928–1930 年使用自製輪子箱旅行，但未明確指認館藏品就是片頭旅程中那只。此句保留了必要區別。 |
| `hook/origin` 的 `y9b6 → 83ew` | 問題與回答使用同一個「是否有一只留存」範圍，沒有以一件未確認的實物身分製造回收。 |
| `origin` 的 `6h2q → idiy` | 原 payoff `3zkh` 只說到四腳輪；下一句 `idiy` 才補到繩子。把回收點移到 `idiy` 後，四輪與繩子合起來才完整回答起問。Sadow 的本人訪談支持機場輪板、四腳輪樣品與繩子。 |
| 四處企劃片語 | 片頭與起源章縮小館藏箱的指認；另一處把回收放到繩子講完之後。館方文章亦記載丈夫對輪子箱的反應與旅後巡迴講述旅行，故企劃改為保留這三句、但不展開 1933 年出書支線，有來源基礎。 |

核對的一手資料：[溫尼特卡歷史學會館藏文章](https://www.winnetkahistory.org/gazette/before-her-time-anita-willets-burnhams-rolling-suitcase/)、[館方 2010 年藏品紀錄](https://www.winnetkahistory.org/gazette/from-the-curator-fall-2010/)；輪板與樣品使用 [Sadow 本人接受 ABC News 訪談的報導](https://abcnews.com/Travel/suitcase-wheels-turns-40-radical-idea-now-travel/story?id=11779469)。本次官方文章的直接頁面讀取不穩，另核對其搜尋索引的完整正文；訪談頁可直接讀取。這個證據足以支持上述**局部**判讀，不證明 1927 館藏品與 1928 旅程示意箱的同一性。

## 未通過的關卡

- round9 真實敘事審核的 `chapters_link`、`payoffs`、`one_thread` 仍是 FAIL；round14 沒有新的正式 verifier／listener／panel 結果。尤其冷開場 Sadow 轉回 Anita 的章首接縫，以及跨數名人物是否仍是一條用途主線，尚須由完整實稿審核判定。
- 企劃 `origin.point` 繼承的「片頭動畫後明確從 1928 年出發開始」與現稿 `origin-r12-01` 先交代旅前發問、製箱再出發的句序不完全一致；這不是本輪四個精確片語所修復的部分，進入整片審核前須另行對齊。
- `o20` 及兩句新稿的精確來源紀錄仍須在實稿來源表與獨立審核中綁定。本報告沒有改 `source-map.json`、`claims.md`、正式機章稿或任何審核判定。
- round15 只改七景畫面提示詞，旁白與 loop 沿用 round14；它不提供新的敘事 PASS。片長、TTS、實際圖片、成片與預算尚未驗收。

**此文件不得當作 `story/reviews/script-review.json`、正式機寫入許可、付費媒體許可或上架核准。**
