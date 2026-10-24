# S58 R5｜正式雙盲敘事 OR 合併與剩餘修訂

2026-10-21 UTC。**敘事正式固定 OR 合併 PASS：13／13 YES，CLI exit 0、`passed:true`；史料／書面畫面仍 HOLD，不能進入付費媒體。**兩位無前情讀者各 12／13 YES，但 A 否定 `payoffs`、B 否定 `no_recap`；依官方固定 OR 規則，兩者均有另一位帶場景 ID 的 YES 而通過。個別異議仍保留，R6 作者宜窄修可核實的斷點。

| R5 凍結檔 | SHA-256 |
| --- | --- |
| `research.md` | `1f6adc58345a10655a0bfdf66c87d5337cbd87c8271f41cb4878204bf4e5d5d0` |
| `brief.md` | `fbffce22c2eff5052a4050b06b121e3fc8a62b7ab350ecfd6a150f5788214362` |
| `claims.md` | `67ed990038429d6186487e1f16504ebf3e982d2b8d7c591c75b7c58faf8cceef` |
| `video.json` | `1be17b85b1b41cb1f5e0f9fe21d18c758ef096447cb4c776c5dcba1ba79dda22` |
| `script.md` | `ce03aeae00241c3e178897ea35a4469c697abaddbb268061fd0574eed0dc35e0` |

## 原票與正式紀錄

[A 原票](raw-ballot-a.md)、[B 原票](raw-ballot-b.md)逐位元組複製自 `../r5-blind-a.md`、`../r5-blind-b.md`；SHA-256 各為 `19746ef5547ffb2de58f2ddb0ed522e5305b7b4fd8e976d43a95a2996361c097`、`bd368236f51c2f4052c4eacd3598dae9f577dab474abfeca3971904cfc492c41`。用[轉錄程式](build-merge.mjs)建立官方形狀 [A](ballot-a.json)、[B](ballot-b.json) 和[稽核](merge-audit.json)。官方 `PANEL_RULES_SHA256=5d71fef2cf3831dc33c0c32b2b297f633c47bfe41fbad18865ae08ed0c91cb75`，OR 規則是任一讀者帶場景 ID 的 YES 即通過該題。[合併答案](merged-answers.json) SHA-256 為 `66b169fd60695d982d85268680f07c0edbdc01fcdac2a3aee70db0b136e44dc2`，13 YES、0 required NO、0 advisory NO。

正式命令 `node tools/video/cli.mjs narrative --slug curio-s58 --answers docs/videos/curio-s58/review/r5-merge/merged-answers.json --workdir /tmp/curio-s58-r5-merge-formal-U1miXA --json` 的[執行收據](cli-status.json)、[原樣 stdout](cli.stdout.json)、[stderr](cli.stderr.txt)、[退出碼](cli.exit-code.txt)與[官方紀錄](official-narrative-record.json)均封存。前後五份創作檔 SHA 一致，官方紀錄 SHA-256 `fbc48245ab6e7a299f6ad38b326dc4ad4bab166cb9cd03dee546ac449cd8b339`，`narrative_hash=4e227cdc0fbe1530`。

## R6 窄修原因

- [A](../r5-blind-a.md)的 `payoffs` NO：`s58068` 問酒桶能否「過關」，而 `s58071` 表明進 Arcis 稅卡前便留下；應把問題限於先把器材**運離村子**。`s58140` 問材料實際如何出城，但 Dagron 只記了搭氣球寄出的**請求**和後來到貨；應問請求中提出哪種寄法，讓 `s58141` 直接回答。
- [B](../r5-blind-b.md)的 `no_recap` NO：`s58146` 與最後 `s58147` 都說這個例子不能量出逐封私信的到達時間；應刪掉重複的最後句，讓已完成的結論收束。
- [R5 獨立來源覆核](../r5-source-independent.md)唯一 HOLD 是 `s58108` 將「最多十八片」的郵務機關動作歸到 Dagron 本人。固定 Dagron [D420–424](https://github.com/GITenberg/La-poste-par-pigeons-voyageurs--Souvenir-du-si-ge-de-Paris_19588/blob/d2a6e7f42a608005416d925c4fbf1f85d4dbe966/19588-8.txt#L420-L424)的主語為 *l'administration*；R6 應明說這是他**回報郵務機關可最多放十八片**，不宣稱他親手裝片或獨立驗證了精確片數。

R6 改動後須重凍結五 SHA，再交非作者史料／書面畫面和兩位新盲讀。R5 的敘事 PASS 不能替代 R6 審核，也不能蓋過 R5 的來源 HOLD。
