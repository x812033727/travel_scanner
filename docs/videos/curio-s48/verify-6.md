# S48｜R6 接頭故障限縮修訂與作者凍結收據

2026-10-20 UTC。另一位審稿者對 R5 的[獨立史料／書面畫面差分](review/r5-source-independent.md)判定**史料文字 HOLD、書面畫面 PASS**：`atl054` 的「斷索後」把稍後的轉環銷釘頭斷裂誤說成鐵索本體斷裂。本頁只記作者按該項做的限縮修訂、自查與新精確輸入；不把 R5 的任一判定移轉給 R6，也不自行宣稱來源或敘事通過。

## R5 → R6 差分

`atl054` 口播在 `video.json` 與重生的 `script.md` 同步改為「**接頭斷後**，坎寧叫人把備用鐵索接上另一個抓鉤，準備再試。」`claims.md` 的口播與來源限制也同步改「接頭斷後」。前一句 `atl053` 已說明轉接鐵件斷裂。Russell 固定版 [R4029–4045](https://github.com/GITenberg/The-Atlantic-Telegraph_40948/blob/ba499c6bc32adef8c8a91a306dcb2d54bf7e898d/40948-0.txt#L4029-L4045)把故障明記為 *head of the swivel pin* 脫斷，並記 Canning 與 Clifford 立刻讓人把備用鐵索接到另一抓鉤。R6 未改任何 `data.prompt`、景序、伏筆表或其他旁白；書面畫面沿 R5 原稿，實際插畫尚不存在。

| R6 檔案 | SHA-256 |
| --- | --- |
| `brief.md` | `7b4bc4b3f6970ac20ef9c2b9269d8a17cafacc87f2ccaf076806772b2e56ca8a` |
| `research.md` | `3d769826eff0fbfb939b35506e9eafb4166868a6c0709cb4bf234af4922dd19f` |
| `video.json` | `5d8245536c1271f6cd99b930155beb3c9532e1e0b4e1247690531282ceee9bfe` |
| `script.md` | `ddf43a0f76cef45f378d3d34c4a1050d7391eaf11bf2faf8f8f3f3f0833e3c5f` |
| `claims.md` | `4324f4a9980a2a1aaab7e85c91115c7ad43f3a9c55c79f8ab042129b76e7d3b9` |

固定原文未換版：Russell `/tmp/s48-russell-atlantic-telegraph.txt` SHA `558efcc342df669e7387ffff818c104690e7ec910de49e795f996abf147ea750`；Field `/tmp/s48-field-atlantic-telegraph.txt` SHA `bee659b24ace56a5e1f7104a6a306e9325ccd9c864fc373ad35b0863c5a8c675`。`node tools/video/cli.mjs narrative --slug curio-s48 --json` 的 R6 原樣旁白與 13 題 JSON 暫存 `/tmp/s48-r6-narrative-input.json`，SHA `06edcc48cb8c11b68a40b0e3d76e792b8aa44ddd93bbec01534744ad9b28b979`；新盲讀須只給這份輸入，不給先前報告或主張表。

## 作者自查與待辦

`node tools/video/cli.mjs script --slug curio-s48` 已重生劇本，其尾端 `narrative b9815ad3b1c18ca7`、`speech 0018090769148747` 與新口播相綁。按 ID、次序與字面核對，99 句正文加三句片尾，在 `video.json`／`script.md`／`claims.md` 為 **102/102 一致**。`VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s48 --json` 為 **0 errors／0 warnings**；99 個 `shot`、20 條伏筆、11 章。`npm run check:tasks` 通過，`git diff --check` 無錯。

`estimateTimeline` 含預設停頓，非 TTS 實長：325 單位／分的濃縮開場 45.3 秒、正文 **8:42.8**、三句片尾 12.4 秒、總旁白 9:40.5；250 單位／分正文 10:51.9。原創 5 秒片頭與共用 21 秒片尾仍只是製作計畫。

**下一關**：另一人對這五個 R6 exact SHA 與固定原文做獨立史料／書面畫面差分；來源通過後，讓兩位全新互相隔離的讀者對 R6 原樣旁白 JSON 做官方 13 題盲評。R4 正式敘事 FAIL 不因本次改字撤銷；尚無站台／Jev 核准、TTS、實際插畫或影片。
