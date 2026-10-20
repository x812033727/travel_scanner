# S48｜R5 敘事限縮修訂與作者凍結收據

2026-10-20 UTC。[R4 正式隔離雙盲](review/r4-official-panel.md)的兩位讀者各 11/13，均將必答 `payoffs`、`no_recap` 判 No。本頁只記錄作者依此 FAIL 所作的 R5 改稿、自查與精確輸入；R4 的[獨立史料／書面畫面 PASS](review/r4-source-independent.md)綁 R4 雜湊，不移轉為 R5 判定。既有審稿與 `verify-4.md` 均保留原貌。

## 固定輸入

| 檔案 | R4 SHA-256 | R5 SHA-256 |
| --- | --- | --- |
| [brief.md](brief.md) | `875550d9b245012357c27a2360641f54202003a5e45bde638f19e1f5811ec8bf` | `7b4bc4b3f6970ac20ef9c2b9269d8a17cafacc87f2ccaf076806772b2e56ca8a` |
| [research.md](research.md) | `3d769826eff0fbfb939b35506e9eafb4166868a6c0709cb4bf234af4922dd19f` | `3d769826eff0fbfb939b35506e9eafb4166868a6c0709cb4bf234af4922dd19f` |
| [video.json](video.json) | `a2f36c1dc2c6a3b1b609ea5630a2e9cf11c9e795bf272956901d6d054bec0501` | `237e94619e963892c9252a95a2d964fd8811c1be79af78cf5f1196d802442975` |
| [script.md](script.md) | `0794fe3217bf4aab22158135d4af4ebf834b2cfb37c845a898fad4c0873a7cc6` | `2936799d767df80f762333f9c5af66eeb9c9cd740a57cb20a4fdf4eec15da434` |
| [claims.md](claims.md) | `baee71c3df9ded7d8128cf73a92855ec5743fb6f0981745ba060927672aa1183` | `971a45761e7d4f9c52e8b6bfb77c4184dc6ca9fd5b139e9e584e10ea425a4960` |

兩份固定原文未換版：Russell `/tmp/s48-russell-atlantic-telegraph.txt` SHA `558efcc342df669e7387ffff818c104690e7ec910de49e795f996abf147ea750`；Field `/tmp/s48-field-atlantic-telegraph.txt` SHA `bee659b24ace56a5e1f7104a6a306e9325ccd9c864fc373ad35b0863c5a8c675`。`node tools/video/cli.mjs narrative --slug curio-s48 --json` 的 R5 原樣 JSON SHA `bde691ac965e0aa77c9304241d79da99b05236b741e919f1fbdae3adad5fa344`，僅含旁白與 13 題；題規 SHA `5d71fef2cf3831dc33c0c32b2b297f633c47bfe41fbad18865ae08ed0c91cb75`。本機暫存 JSON 在 `/tmp/s48-r5-narrative-input.json`，亦可用同指令重產。

## R4 → R5 語義差分

| R4 共同失敗與編輯附註 | R5 精準修訂、來源和畫面界線 |
| --- | --- |
| `atl026→027` 問「問題在哪裡」卻只能說原因未知。 | `atl026` 現問能否再收到岸上回應；`atl027` 以反光訊號突然重現直接作答，仍明說確切原因未查出，沒有把檢查寫成已證原因。Russell [R2970–3110](https://github.com/GITenberg/The-Atlantic-Telegraph_40948/blob/ba499c6bc32adef8c8a91a306dcb2d54bf7e898d/40948-0.txt#L2970-L3110)記訊號重現，並明說中斷成因難判。 |
| 開場 `atl005` 問「鉤上的是什麼」，當年沒有目視答案；`atl050→054` 重複未見舊線。 | `atl005` 收窄成「船上能確認鉤到舊線嗎？」；隔幾分鐘後 `atl050` 點名開場抓鉤，明答當時仍不能確認。`atl051` 改成繼續拉索的下一步；`atl054` 改成斷索後坎寧叫人把備用鐵索接上另一抓鉤。這是 Russell [R3870–4045](https://github.com/GITenberg/The-Atlantic-Telegraph_40948/blob/ba499c6bc32adef8c8a91a306dcb2d54bf7e898d/40948-0.txt#L3870-L4045)的船上推斷、斷接頭及再備抓鉤，沒有宣稱目擊海底鉤物。`atl054` 提示詞同步改成甲板上接備用索的單人動作，不畫海底舊線。 |
| `atl047` 原指向重複的 `atl054`，其「抓鉤能撈到嗎」也較含糊。 | 問題改為「這次能把舊線拉上船嗎」，`loops` 回收點移到 `atl053` 接頭斷裂、鉤具落回海中的結果；隨後 `atl054–055` 才接續再備抓鉤與標浮標。 |
| 編輯首讀見 `atl085→086` 重述「第三十次」；`atl085` 章首還複述上一章已拉緊的索。 | `atl085` 改成先緩緩收繩，直接接 `atl084` 如何避免再斷的問句；`atl086` 只講一次後出 Field 書的「第三十次」，另添每收一百噚張力上升的新讀數。Field [F9540–9627](https://github.com/GITenberg/The-Story-of-the-Atlantic-Telegraph_34765/blob/6b50b44d3cd2f3f1831e2c1a8fa052f53c51a4cd/34765.txt#L9540-L9627)同段支持慢收、計數與讀數，不冒充 Henry 親眼見證。`atl086` 提示詞同步改成船首工程人員看無字張力計。 |
| `atl095→096` 把愛爾蘭端可送訊說了兩遍。 | 刪去 `atl096` 景、旁白與主張列；`atl095` 的《Spectator》愛爾蘭端規律光訊後直接接 `atl097` 的舊線續鋪。Dudley 船上等待與《Spectator》岸端報導仍分層歸屬：[F9652–9719](https://github.com/GITenberg/The-Story-of-the-Atlantic-Telegraph_34765/blob/6b50b44d3cd2f3f1831e2c1a8fa052f53c51a4cd/34765.txt#L9652-L9719)。 |

企劃 A 的開場文字同步將「究竟鉤上什麼」改為「能否確認鉤到舊線」。`research.md`、1865 年張力推斷與 1866 年目視／測通的三層證據、1,186 `miles` 的單位歧義、九月初抵岸的日期收窄均未更動。其餘景的畫面提示詞維持 R4 字串；除兩句改詞所對應的 `atl054/086` 外，另刪除已無旁白的 `atl096` 畫面。這仍只是書面分鏡，未生成插畫。

## 作者自查與後續關卡

`node tools/video/cli.mjs script --slug curio-s48` 已重生 `script.md`；`VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s48 --json` 為 **0 errors／0 warnings**。本機按 ID 逐字比對 `video.json`、`script.md`、`claims.md` 為 **102/102 一致**；99 個 `shot`、20 條 `loops`、11 章；`git diff --check` 無錯。

`estimateTimeline` 含預設停頓，並非 TTS 實長：

| 估算語速（單位／分） | 濃縮開場 | 正文（不含片頭／片尾） | 三句片尾 | 全旁白 |
| --- | ---: | ---: | ---: | ---: |
| 250 | 56.4 秒 | 10:51.7 | 15.4 秒 | 12:03.4 |
| 300 | 48.2 秒 | 9:17.2 | 13.2 秒 | 10:18.6 |
| 325 | 45.3 秒 | **8:42.6** | 12.4 秒 | 9:40.3 |

R5 還須**另一人**重開固定原文、對這些改句與兩張書面提示詞做獨立史料／畫面差分，再交兩名**全新隔離讀者**只憑 R5 CLI 旁白與 13 題盲評。R4 FAIL 不由作者撤銷；本頁沒有獨立 PASS、站台 A／劇本核准、Jev 政策判定、TTS 實長、音檢、購圖、插畫或成片成果。
