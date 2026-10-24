# S56 R12｜正式敘事合併與 Jev 政策關卡

2026-10-20 UTC。**本精確 R12 五檔版本的獨立史料／書面畫面、正式雙讀者敘事合併及 Jev 政策均 PASS。** 這些是文字關卡；不構成 R12 配音、154／154 句音檢、實際插圖、成片或站主核准。R11 音檢留下的 `s56096`、`s56174` 兩旗標不能清空或借作 R12 PASS；`/workspace/.video-work/curio-s56/STOP` 仍在。

| 凍結檔 | SHA-256 |
| --- | --- |
| `brief.md` | `09f731c13f1037c963aa5774b936a43e1a187b5c4ae8d09ba158581a705f1a52` |
| `research.md` | `59549e98e6ae258cedfc5b43e6684ecaa1102284d0dee13b0beef6443e4a6fb7` |
| `claims.md` | `ca09512c0398c94578f2acaa748cdc13c4b5ebff79ac80b6107ca600d65f6b11` |
| `video.json` | `f54a4c830fb876e949f4f4910d025cb8f68331e40d27dc87ab9edf26f05bd479` |
| `script.md` | `65ae866c1761da1c83d0941a92569c7b85ec0fddda0de17adc157bbc8d046f4f` |

[R12 獨立來源與書面畫面](../r12-source-independent.md)先對這五檔判 PASS；正式兩位讀者均只讀上述 `script.md` 和官方 13 題，凍結稿中保留 [A 原票](raw-ballot-a.md) SHA `a1240f38a957a2f08c157c208fdd2fce6a737c538eddef0a5891c9db6ced7371`、[B 原票](raw-ballot-b.md) SHA `2030b082c185e7e6cab38ddefe482599572a13cb23d5c3efab26689e2f6e8b89`，與原位置逐位元相同。A 投 **12／13**，`no_recap` 為否：`s56143`、`s56147`、`s56151` 三次提北側火續往北。B 投 **12／13**，`payoffs` 為否：`s56150` 問較遠住戶門前會否守住，而 `s56151` 只說火續往北，未給那幾戶的確切結局。B 原票兩處把洛許誤寫成「Rush」；原樣保存，轉寫證據引用的是劇本實際的 `s56117` 等句，沒有採錯名作史實。兩處異議均保留於[合併稽核](merge-audit.json)，未偷偷改票。

[A 13 題轉寫](answers-a.json)與 [B 13 題轉寫](answers-b.json)保留各題原來的是／否；引文欄取票中所指的逐句 ID 和該句劇本原文。章名題的原票只引章標行數，沒有旁白 ID，轉寫用末章首句作工具所需的附 ID 證據，轉寫規則與全部原票行均留在合併稽核。`panelVerdict` 對 A 只列 `no_recap` 失敗，對 B 只列 `payoffs` 失敗；`panel_rules_sha256=5d71fef2cf3831dc33c0c32b2b297f633c47bfe41fbad18865ae08ed0c91cb75`，`panel_narration_sha256=8d56a44598d207645fb6cce61bd516b2e2ebb6847cb9e79aae507ca300284776`。依 `mergePanelVerdicts` 固定 **OR** 規則，`payoffs` 由 A 的是通過、`no_recap` 由 B 的是通過，其餘 11 題兩讀者皆是，合併 **13／13 PASS**。[合併答案](merged-answers.json) SHA `793b7f871f0d67dcc44d78457f767f6a5f1b5644894c0c354f22378767c14e91`。

正式 `node tools/video/cli.mjs narrative --slug curio-s56 --answers docs/videos/curio-s56/review/r12-merge-policy/merged-answers.json --workdir /tmp/s56-r12-official-narrative-20261020 --json` 在隔離工作目錄退出碼 **0**，`passed:true`、`failed:[]`、`advisory:[]`。保存 [CLI 原樣 stdout](merged-narrative-cli.stdout.json)、[stderr](merged-narrative-cli.stderr.txt)、[回條](merged-narrative-cli-receipt.json)與[工具綁定紀錄](merged-narrative-record.json)；回條 SHA `234d48dd22ce3a1c9befc691464dbe3fe1c7212a3be1674473ec9c97e398fe8f`，紀錄 SHA `2db6d0963d197d7b6029585003d845ad1e8ddf4a2a0c3d324134d83aea0f475f`，`narrativeReviewMatches` 對現版 `video.json` 為真。

同版 `video.json`、`brief.md` 經 `policyRequest({doc,brief})` 產生完整旁白 **3,192 字元**、站主觀點 **81 字元**的請求；JSON 序列化 SHA `372b161313435394d00072c78f1d2725b411064c3335b85063ac4d6aa0c0b9ad`。[請求全文](policy-request-body.json)與[預送中繼資料](policy-request-meta.json)在唯一 POST 前寫入。網站 `/api/video/automation/judge/policy` 回 **HTTP 200**、`passed:true`、`questions:"explainer"`、立場 `0.75`、示範不適用、建議 `0.01`、業配 `0.01`，故 Jev 政策 **PASS**；只送 **1 次**，沒有不明結果重送。[原樣回覆](policy-response.raw.json) SHA `d845f30fe0dcdd376dd4f4c3937e12e3418d577bc2405d963f959dcca79ffb88`；[解析回條](policy-receipt.json) SHA `bca1190eab363082493cfd91bb8b6bc6ba2d4c4a11ec864f2238a5cdd97ba787`。

`node tools/video/cli.mjs lint --slug curio-s56 --json` 為 **0 errors、0 warnings**（154 句）；`node --test tools/video/core/narrative.test.mjs tools/video/qa/checks.test.mjs` 為 **30／30 通過**；`npm run test:docs-videos` 為 **236／236 通過**。封存檔一致性與逐行空白檢查通過；`npm run check:tasks` 退出碼 0，驗證 2,289 張票（既有其他票的過期／重疊警告仍在）。全程沒有改 `brief.md`、`research.md`、`claims.md`、`video.json` 或 `script.md`，沒有合成音訊、生成插圖、配樂、成片或發布。下一關須以 **R12** 另做 `tts --dry-run`、新版配音和 **154／154** 句全檢，R11 音檔與舊旗標不是本版的音檢證據。
