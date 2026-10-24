# S57 R2｜作者窄修與獨立重審交接

2026-10-20 UTC。這是依 [R1 獨立史料與書面畫面 HOLD](r1-source-independent.md) 所做的**作者修訂紀錄**，不是來源、敘事或政策 PASS。五份製作檔現已凍結；獨立審閱請以以下 SHA-256 為準。未合成語音、插圖或音樂。

| 檔案 | R1 SHA-256 | R2 SHA-256 |
| --- | --- | --- |
| `research.md` | `9663d4a0ea66b1fef3c6e3a0550b8b08cf169a68b1736ad6005d6408ac2cd667` | `9663d4a0ea66b1fef3c6e3a0550b8b08cf169a68b1736ad6005d6408ac2cd667` |
| `brief.md` | `ded775a86c0353c44c6ea5cd53265f7d95a61b7539dd61d86eed007a3bac165e` | `911eb30d15273aa3ab5a57795e28e5a9c3fb4a8fa60059f3f152dc3eb578765a` |
| `claims.md` | `f62350da54fc1500576de402faffb87267286a93c9c7b21429b1664a5edf179e` | `5f03685898d9b256e9d3eaf0d7534efe3eaf4b9393f3ad86e418787ad1bb27f9` |
| `video.json` | `366123f3ace1668236d651bc6decbb9b27b744ed74409fd3d83040e31ade76bf` | `53ee5cd8a93ff5474ffbccbde47379c9872303a4d09442a1f1d699fb8d25b4ff` |
| `script.md` | `2ea8113fcd872bf80b8342b2617deb043a4526b5cb43595c2cf532578ee1cdae` | `604a4f10dbd6ac5b8c7602939a40f58252307a82810bd70d6c2d8b2a63fd29da` |

## R1 → R2 的全部口播改動

| ID | R1 | R2 | 史料界線 |
| --- | --- | --- | --- |
| `s57050` | 李文斯頓記下相遇，卻沒記下這句原話。 | 身後編刊日記寫到相遇，這段卻沒那句原話。 | [Waller 1874 年編刊版 L5252–77](https://github.com/GITenberg/The-Last-Journals-of-David-Livingstone-in-Central-Africa-from-1865-to-His-Death-Volume-II--of__17024/blob/bd976e865f60f2bc17628640378e4510969a94ad/17024-0.txt#L5252-L5277) 僅能證明出版段落未載名句；[Stanley 節錄出版書 S9530–45](https://github.com/GITenberg/How-I-Found-Livingstone--13-Travels-adventures-and-discoveres-in-Central-Africa-including-an-a__5157/blob/41828f7623e5ba1b0db0a4c96630bda15bb0b66e/5157.txt#L9530-L9545) 載有該句。卡片同步標示「身後編刊日記／相遇段未載名句」。 |
| `s57077` | 日記還提到女兒艾格妮絲的信。 | 日記還記下女兒艾格妮絲的話。 | [L5741–51](https://github.com/GITenberg/The-Last-Journals-of-David-Livingstone-in-Central-Africa-from-1865-to-His-Death-Volume-II--of__17024/blob/bd976e865f60f2bc17628640378e4510969a94ad/17024-0.txt#L5741-L5751) 有「My daughter Agnes says」，沒有這句話所屬信件的證明。`s57077–s57079` 的真實信件道具均已移除。 |
| `s57116` | 新年剛到，暴雨就把隊伍留在湖灣。 | 新年剛到，風暴就把隊伍留在湖灣。 | [L5474–76](https://github.com/GITenberg/The-Last-Journals-of-David-Livingstone-in-Central-Africa-from-1865-to-His-Death-Volume-II--of__17024/blob/bd976e865f60f2bc17628640378e4510969a94ad/17024-0.txt#L5474-L5476) 記 *storm-stayed*，未指定暴雨。該景只寫陰沉天色及隊伍在湖畔避候；後續有來源支持的雨路鏡頭未改。 |

## 書面畫面窄修

- `s57028`、`s57030–s57032`：把 Bennett 交辦任務所在改為巴黎 Grand Hotel 房間；`s57031` 改為旅館內聽取任務，不把裝載好的遠行貨包搬進交辦場景。[S62–94](https://github.com/GITenberg/How-I-Found-Livingstone--13-Travels-adventures-and-discoveres-in-Central-Africa-including-an-a__5157/blob/41828f7623e5ba1b0db0a4c96630bda15bb0b66e/5157.txt#L62-L94)。`s57029` 卡片未動。
- `s57100–s57112` 除 `s57103` 卡片：北探結束後的 12 景改在烏吉吉東岸港口、湖畔村落或離村向東的路，不再停在湖的北岸。[L5414–28](https://github.com/GITenberg/The-Last-Journals-of-David-Livingstone-in-Central-Africa-from-1865-to-His-Death-Volume-II--of__17024/blob/bd976e865f60f2bc17628640378e4510969a94ad/17024-0.txt#L5414-L5428)；編者將烏吉吉置於湖東岸 [L478–80](https://github.com/GITenberg/The-Last-Journals-of-David-Livingstone-in-Central-Africa-from-1865-to-His-Death-Volume-II--of__17024/blob/bd976e865f60f2bc17628640378e4510969a94ad/17024-0.txt#L478-L480)。
- `s57188–s57189`：死亡卡後改為明示 **1874 年編刊／蘇西與楚馬追述**及本集回顧結語的排版卡，不再畫 1873 年後仍活動的當事人。[L9976–85](https://github.com/GITenberg/The-Last-Journals-of-David-Livingstone-in-Central-Africa-from-1865-to-His-Death-Volume-II--of__17024/blob/bd976e865f60f2bc17628640378e4510969a94ad/17024-0.txt#L9976-L9985)。

`video.json` 的改動嚴格限於 **23 個場景 ID**：`s57028`、`s57030–s57032`、`s57050`、`s57077–s57079`、`s57100–s57102`、`s57104–s57112`、`s57116`、`s57188–s57189`。其餘 **166 個場景**及所有頂層 JSON 欄位的值未改。`claims.md` 也只改相同 **23 列**的口播或畫面界線；`script.md` 從 JSON 重產，只更動上述三句與末兩景卡片標記及自動產生的版本資訊。`research.md` 未改；`brief.md` 僅更新審核狀態、R2 數量和下一關。上述 23 景不含一個無關題材重寫。

## 可機械查驗的交付狀態

- `node tools/video/cli.mjs lint --slug curio-s57 --json`：**0 errors、0 warnings**；189 句，工具估時 **14.5467 分鐘**。濃縮開場 `00:00–00:44`，之後規劃 5 秒片頭；正文至少 2,690 個漢字，按每分鐘 325 字約 **8.28 分鐘**。12 個章節鉤子／`loops` 沿用 R1，書面 `cute-mystery` 插圖鏡頭 **168/189（88.9%）**，21 張排版卡。全域 21 秒片尾、頻道與兩份固定來源連結留在 `video.json` 與 `brief.md`。
- `npm run test:docs-videos`：**236 pass、0 fail**。`npm run check:tasks`：exit 0；只見既有的無關任務板警告。
- 本修訂由作者完成，**不得用作自身的獨立 PASS**。須重做 R2 全稿史料與書面畫面覆核，另交兩位無前情讀者盲評；其後才可執行政策、付費語音、插圖與成片關卡。
