# S61 R8｜正式雙盲敘事合併

2026-10-22 UTC。**正式 OR 合併 12／13，HOLD：唯一共同 No 是必答題 `no_recap`。** 這是敘事票，不改寫已 [PASS 的 R8 獨立史料／書面畫面覆核](r8-independent-source-visual.md)，也不核准旁白、圖片或成片。

兩位隔離讀者均先收到同一份官方 13 題面板，SHA-256 `15cfd34356840ae8036c91bc9d8b29f210be52aa761f28379a2bd9ed263fa5ad`，並在各自執行 CLI 前凍結對同一 `script.md` 的完整原始票。劇本 SHA-256 `00f9734108f68b0093a3c7791fe4b0974a376cb963cbc772c1ed92cc61c11b04`。我逐項驗證兩份原票與 CLI 答卷位元相同、13 題順序及所引旁白文字正確，官方 stdout 與票吻合，兩份官方紀錄對現版 `video.json` 均通過 `narrativeReviewMatches`。共同綁定為 `narrative_hash=0eb01daae10fefd9`、`script_hash=75668f4a8fc7c929acf0cdafc2e55092eeabcead667042204c937facfacaa7e9`、`panel_rules_sha256=5d71fef2cf3831dc33c0c32b2b297f633c47bfe41fbad18865ae08ed0c91cb75`、`panel_narration_sha256=a5d60c9e07653a406c2ed6960cbf3a2acf60f9df0e9229e5aea6c2df4415b030`。

| 讀者 | 原票 SHA-256 | 官方綁定紀錄 SHA-256 | 原票結果 |
| --- | --- | --- | --- |
| [A](r8-isolated-blind-a.md) | `b2a7ab0062d1aa8d5d7bccbda4c4f5aa398aac03cd61d6b960d7c4e70722d909` | `e0aa5788d16b46f2f94f7ff8ed02ecb8ad667a5d84308f4ecf7d9416cf4daf61` | 11／13，No `no_recap`、`no_detour`；CLI exit 1 |
| [B](r8-isolated-blind-b.md) | `e17706e2bf2107b0ece05043c842ae16416f2528917b021156cf9c8b62b0807a` | `994cf112c31e6d69b9e9cce6ef17b93d7dfb5328ece7c155020b9b452fd6c026` | 10／13，No `one_line`、`payoffs`、`no_recap`；CLI exit 1 |

我對兩份 `panelVerdict` 呼叫倉庫的 `mergePanelVerdicts`，逐題 **OR**：`one_line`、`payoffs`、`no_detour` 各有一位 YES，合併後通過；`no_recap` 是兩位共同 NO。合併 [答卷](r8-formal-merged-answers.json) SHA-256 `63b8b6b97ea14f839524625820394c4a841db9f6aaa95c17d315a96d73b87187`；保留各讀者票及 `yes_readers` 的 [正式紀錄](r8-formal-merged-narrative.json) SHA-256 `c73513e0c7f173feaf46e1109a5d07837cb3455b21419756b846f3ad350d1b3e`，`passed=false`、`failed=["no_recap"]`。在隔離工作目錄 `/tmp/s61-r8-formal-merge-odhx8yv5` 用該答卷重播官方 `narrative --slug curio-s61 --answers docs/videos/curio-s61/review/r8-formal-merged-answers.json --workdir /tmp/s61-r8-formal-merge-odhx8yv5 --json`，exit **1**、stderr 空，僅 `no_recap` 失敗；[CLI stdout](r8-formal-merge-cli.stdout.json) 與[原生紀錄](r8-formal-merge-cli.official-narrative.json)的 13 項答法、證據與四個綁定值均和正式紀錄相同。原生紀錄 round 是這個新工作目錄的 1，正式合併紀錄標 R8 的 8；兩者的 PASS 判定一致。

**R9 窄修目標：**`s61123` 已說北區瓦礫下有人無法自己脫困、消防員知道；後面的 `s61059` 又說「消防員知道：有傷者被困在瓦礫下，單靠自己走不出來」，沒有點名回呼或新增動作。兩位讀者均因此給 `no_recap` No。作者須消除這一重述並保持據源；R8 以 325 CPM 估正文 **486.20 秒**，只高於八分鐘門檻 6.20 秒，刪改後必須重新量。A 另指 `s61015` 的伊莫號比利時救濟船前職可能岔出主問題；B 另指 `s61113` 問老人與病弱者到公地後在哪避寒，但 `s61081` 白帳及 `s61149` 教堂大廳未點名該群以回收相隔數分鐘的問題。這兩項**不是合併 HOLD 題**，下版可一併評估。R8 沒有進媒體關卡。
