# S38 R8f｜三景提示詞精確差分獨立覆核

2026-10-21 00:14 UTC。**PASS：僅限 R8f 書面差分、史料相容性與提示詞規格。原生圖片、整體分鏡及成片仍 HOLD；私有 `STOP` 保留。**我未撰寫 R8f 提示詞，未改創作檔、圖片、媒體帳本或網站核准，也未呼叫付費工具。

## 固定版本及獨立差分

本判定只對 `video.json` SHA-256 **`084ff89c7df3dbfc0c150263eec6d96c3dabf85fc1baacd864a7e40f41416616`**、`visualHash` **`9dce146d046f75cf`** 有效。另四檔 SHA-256：`brief.md` `fa297d70e016d88ba1a59bd92476be22eda3eefc09f36b2d08c0c82ab114643b`；`research.md` `f838518cf2c4ab23de91021ae6024d9431f907866c14301466ca0a06bb3ecdfe`；`claims.md` `f9de8d2771b62cc327f4e599f002af8f3278cfb0f39dbed201e7fdc857201d42`；`script.md` `e59ec137e3de3871e3b0e5063d8f6504d3eb2adb5fe22265eb3faa3d613d5951`。這四檔與 [R8e 停點](verify-14-art-stop.md)所記一致；`lint --slug curio-s38 --json` 實測 0 error、0 warning。

我自行將 Git `HEAD` 的 R8e `video.json`（SHA `33eceef58a3d25414f28606b1737258b256ff8a4bd9687f739974e42c0bb12bc`）與現行 R8f 解析為 JSON，遞迴比對**恰好三個不同葉節點**：`scenes[3].data.prompt`／`pf004`、`scenes[4].data.prompt`／`pf005`、`scenes[5].data.prompt`／`pf006`。每個前後字串均逐字符合[作者的結構化差分](verify-15-r8f-structured-diff.json)（該檔 SHA `564e6372d39a9d920a83a0556abd2420818e521a4ff48a93cd3cea48965b6f92`）；三個新字串也逐字符合 [R8e STOP 所列候選](verify-14-art-stop.md)，即[紙上獨立審查](verify-14-art-paper-independent.md)逐景 PASS 的候選。其餘所有解析後 JSON 完全相同，包含 112 景次序、每句旁白、來源、鏡位、品牌設定及 `look: {"preset":"cute-mystery"}`。`pf001/002/003` 整景與 R8e 相同，無旁白或視覺風格偷改。

## 史料與畫面規格

我重新下載固定 GITenberg commit `68fcf49f70ee793b989a6fd0464264d55beb4451` 的 `4200.txt`，SHA-256 **`3cd43a3c39ee72eb9c4a3657f1fcb1723afba291cedac176c65a39289483be5d`**，重讀 1666 年 9 月 2、4、5 日相應條目。各景仍只呈現一個主要成年人物及一個主要動作；倫敦紅磚斜屋頂、十七世紀服飾和空白日記頁是時代／概念線索，沒有把 `cartoon`、`chibi`、色盤等畫風命令寫入單景，也沒有要求生成可讀文字。

| 景 | 獨立核對與 KEEP 界線 |
| --- | --- |
| `pf004` | 9 月 4 日日記寫佩皮斯在花園憂心辦公室將燒，9 月 5 日才記房屋與辦公室仍在。單一住戶指向遠火與未燒的房屋，符合「最後有沒有燒到」的懸念，**不能當成史料證實了真實花園、住屋及屋頂的相對位置**。寬景又要求臉、房屋和火，原生圖須確實保留全景及成年人物；不能重現 R8e 幼童、東亞曲檐或提前揭露結局。 |
| `pf005` | 9 月 4 日日記有埋 `Parmazan cheese`，所查 2–6 日條目未交代起司下落。單一成年讀者讀素面頁、空桌，適合示意「日記有沒有交代」；此人及這一幕**不可標為經查證的佩皮斯肖像／活動**。原生圖不得有第二讀者、可讀假字、現代辦公家具或已挖回的起司。 |
| `pf006` | 9 月 2 日日記記 Jane 約凌晨三時叫醒佩皮斯看火，佩皮斯走到「她的窗」。一名成年女僕在窗前望向遠火與旁白相容，但日記沒有記 Jane 的年齡、衣著、窗框或她親見起火原因。原生圖須是成年女僕、相容的倫敦建築與黎明前遠火，不能再有童貌、東亞屋頂或黑色畫框。 |

## 仍有效的停點

私有 `/workspace/.video-work/curio-s38/STOP` 實測仍存在。`media/ledger.json` 有 12 張 image、10 次 judge、1 首 music，記帳合計 **US$0.2220**，其中 `pf003` 一筆 **US$0.0035 reserved** 仍未解；既有整集累計硬上限 **US$4.58** 未提高。沒有因 R8f 書面改詞產生新媒體支出。舊 manifest 的 `visual_hash` 仍是 R8e `14c64a52d7da49a6`，**不能當作 R8f 整體分鏡核准**。其 `pf001/002` 原生檔 SHA 與已通過的 manifest 相符，且兩景 JSON 完全未改；工具實際執行新版逐景 request-key／judge-stamp 搬移前，只能說它們**具備沿用條件**。`pf004/005` 是 R8e 判退舊圖；`pf006` 舊圖未送 judge，不是 R8f 的新圖。

**結論：R8f 三景書面差分 PASS，圖片及製作 HOLD。**下一關須另核付費前即時額度、帳本、網站音訊卡和 `STOP`，再按已記錄的窄範圍方案執行原生 1280×720 圖與 judge；三景 3／3 native KEEP 且 `pf003` reservation 另行處理前，不解除整集停畫或聲稱 S38 已完成。網站站主試聽／審核不能由本收據或本機委派紀錄代替。
