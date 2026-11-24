# S61 R5｜作者敘事修訂交接

2026-10-22 UTC。**R5 為作者候選，待其他工作者重新覆核史料／書面畫面及兩名新讀者各自盲讀；本收據不是獨立放行。** [R4 史料與書面畫面](r4-independent-source-visual.md)曾獨立 PASS；[R4 正式雙盲合併](r4-formal-merged-narrative.json)為 11／13、HOLD，兩名讀者共同否決 `no_recap` 與 `no_detour`，其中一名另否決 `payoffs`（開場帶傷撤離者的問題沒有具體回收）。本次未進付費媒體階段。

## R4→R5 改動

- 原稿 [s61022–s61025] 接連重說「未充分示警」，現保留 Prince 轉引調查的那一次判斷，以岸邊人會受什麼衝擊接到首爆。[s61034–s61038] 改成火藥庫地點、四散者如何收到警報與火勢是否真正逼近的不同問答；不再把「新警告又來」講第二遍。[s61067–s61068] 回碎街的重述刪成一次。
- 騎馬者帶來「危險已過」的 s61066 之後，**下一句 s61095 就是 Prince 明寫沒有第二次爆炸**；s61096 接他的砲兵隊灌水歸因，s61097 說明沒有另核軍方卷宗。海軍造船廠仍只標示火藥庫的位置，不替志願砲兵隊編軍種隸屬、命令或取水方法。
- 警報後的正文僅留五句：回城尋親、初期同一廢墟重找、約五小時後分區並記錄，以及公地白帳。開場 s61004 現具體問帶傷撤離者何時有安全消息與落腳處，由 s61066 與 s61081 明確回收；s61005 問警報後搜救如何接續，s61071 明確回呼並答分區。這五句完成開場留下的人的去向，沒有再展開教堂、修窗與民宅的收容清單。
- 為保留八分鐘以上正文，前半段只增 Prince 固定全文直接支持的首爆後果與初期救援：老城房屋倒塌、爆雲落下煤灰油水、海水進退、北面火勢與瓦礫下的人、通訊中斷、醫療船上岸隊及北區車站乘客。蒙特婁旅客「至少五十名」是 Prince 記下的當時數字；匿名插圖只示意急救，不重建個人。這些事由首爆損壞接到為何第二次警報會動員街上的人與已啟動的救援。
- `research.md` 的 P04、P14 及 `claims.md` 逐句錨點已擴到相關 Prince 原文；87 個 `cute-mystery` 插圖提示逐一與旁白對齊，沒有可讀的警報、官方地圖或可識別個案。六章、23 組 `loops`；濃縮開場後仍留 5 秒品牌動畫，片尾規劃 21 秒及最後 16 秒 Studio 可點連結位置。

## 固定檔案與可逆差異

| 檔案 | R5 SHA-256 |
| --- | --- |
| `brief.md` | `8fdcdf6a78f9b76834b30ce15202a8f8eda4668b6ef809e53bbdd719d5ccefb2` |
| `research.md` | `6df37abc26b603587be5d9911e454a3cb6c08ee3999fdb6772117baa43e0009e` |
| `video.json` | `7c211583bdac109bbd9763fc1059fae1b84e91c05505b8437f90061d860a6b0e` |
| `script.md` | `f0b56d78a14ca5ccf6c87e0c95cf8947cd5ffbe1cc2c1f70e566f28e42771da5` |
| `claims.md` | `9bf29859f70c39c884061ea9e608e99a72735a3fa8c2bf4be4bff2a03d5fff19` |
| [任務票](../../../../tasks/open/2026-10-22-source-and-draft-s61-halifax-second.md) | `1ba86810eea0fe22e0c1735690507305bf96ab79144e27324f4a74514e07717b` |
| [r5-author-delta.json](r5-author-delta.json) | `ea4f621694cbe4ba67b24ec829d73b9067cd0edbde77af39436238efb3b9c1b5` |

`r5-author-delta.json` 記六檔逐塊的舊／新行、座標和 SHA；已從固定 R4 版正向重放到上表 R5，亦從 R5 逆向還原 R4。Prince 固定全文仍是 GITenberg commit `befb706982ba1be631a52d4f686be301c2de7f34`，raw SHA-256 `97484e988437d13a4f5a72d5c2edbf1c594ea8dff4c5b239d8b17b7c62c29b52`。再生劇本標記 narrative `e7cb015c4e27fb45`、speech `9773d04ef0188179`。

## 作者機械檢查

`VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s61 --json`：**0 errors、0 warnings**；97 句、六章、23 組設問、87 個插圖鏡頭、7 張資訊卡。工具估全片 9.5261 分鐘；濃縮開場 59.03 秒，開場後至片尾前正文 495.47 秒（8 分 15 秒）。逐字核對 97／97 句在 `video.json`、`script.md`、`claims.md` 一致，87／87 個不重覆插圖提示詞與各自證據列一致。`npm run check:tasks` 通過 2,417 件任務檔驗證；其他任務既有逾時／範圍警告未改。Prince raw SHA 重查一致。

**下一步：**獨立史料／書面畫面覆核、兩名新讀者的盲讀及非作者正式合併。沒有 TTS、插圖、音樂、音檢、成片、上傳或實際 Studio 片尾連結。
