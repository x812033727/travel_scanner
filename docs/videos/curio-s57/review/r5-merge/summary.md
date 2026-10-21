# S57 R5｜兩位隔離讀者正式敘事合併

2026-10-20 UTC。**敘事 HOLD：固定 OR 合併 12／13 YES，必答 `no_recap` 未過。**這份合併只讀兩位無前情讀者對下表固定 R5 劇本的原票，沒有重作盲讀或改票。[R5 獨立來源與書面畫面](../r5-source-independent.md)是同版 PASS，但不替代敘事關卡。未改五份創作檔，未呼叫政策或付費媒體。

| 固定創作檔 | SHA-256 |
| --- | --- |
| `research.md` | `9663d4a0ea66b1fef3c6e3a0550b8b08cf169a68b1736ad6005d6408ac2cd667` |
| `brief.md` | `25cf00d5d86c8703c459fc1de8774f7adef27059fe4006c93a1b40d7ba14e43f` |
| `claims.md` | `c238f42f44a612ef92c15a1f14f9ad4d0ef86e8f88724888ceecbba016a65230` |
| `video.json` | `07bebbb202143a25f9d942565303da91859c431c402a31c36f6d2824d9d060d9` |
| `script.md` | `464ba2b1bb7dfd5aedaaf3727e4fcaae28d598050e132e72f1dd1bb99b163452` |

## 原票、規則與轉錄

兩位讀者各自聲明只讀固定 `script.md` 與 `tools/video/core/narrative.mjs` 的官方 13 題。原始 [A 票](raw-ballot-a.md)、[B 票](raw-ballot-b.md)逐字複製，SHA-256 分別為 `7caca778fca0c430eeb9fc5f26ef6bc00044be605a53cca21005eccfcdef483c`、`c3d6315189d5312dee5a927a25e0ba9dd6e9e24538b2d481ab01f3c0847bb22a`，與原 review 檔逐位元組相同。A 是 **10 YES／3 NO**：`payoffs`、`no_recap`、`no_detour`；B 是 **12 YES／1 NO**：`no_recap`。

依每張原票的 13 個布林值轉為官方形狀的 [A 答案](ballot-a.json)和 [B 答案](ballot-b.json)，SHA-256 為 `9fc173a78dd6fc8493cb309e6064c50d017285e9981584c917d40616e547995a`、`ddb9cc8f346671c26ce88dbcef2920a3bfe1f6bdf4d2a6d1f7b7d81a5ec38a88`。原票有些理由列多個場景 ID 或僅範圍，轉錄只為 CLI 選一個固定 `script.md` 的逐字句作引用，**沒有改原票的 YES／NO**。[合併稽核](merge-audit.json)保留每題原理由、所選 ID 與逐字句、原理由是否明列該 ID、原票與答案 hash，以及官方函式的原票／合併結果。

使用 `panelVerdict` 與 `mergePanelVerdicts` 的**固定 OR**：同題任一位讀者有帶場景 ID 的 YES 即合併 YES；只有兩位均 NO 才不過。規則 SHA-256 `5d71fef2cf3831dc33c0c32b2b297f633c47bfe41fbad18865ae08ed0c91cb75`；[合併答案](merged-answers.json) SHA-256 `c58fe88f1a403253ff3c567b5d9c3cc01f8da8a14f257d932dd08417cabc9bc2`。`payoffs` 與 `no_detour` 是 **A NO、B YES，按規則合併 YES**；A 的具體異議仍保存在原票與稽核，並未假稱兩票一致。

## 唯一共同阻擋與單票異議

| 題目 | 固定 R5 讀者診斷 |
| --- | --- |
| **`no_recap`：A、B 均 NO，正式阻擋。** | A 指 `s57101` 重述 `s57091–s57093` 的北岸未定論，以及 `s57019–s57022` 已建立的失貨狀態；另指 `s57152` 在 `s57146`、`s57149` 之後又說需要隊伍。B 指 `s57081→s57082` 連續兩句重報勸歸早於二月開箱；`s57101` 再報北岸未定論；`s57182→s57189` 重報日記帶走、人留下，最後一句雖加詮釋仍重播分路事實。R6 宜逐句刪或改為新事實，避免只換同義詞。 |
| `payoffs`：A NO、B YES，**合併 YES**。 | A 指 `s57158` 已在 `s57157` 說史丹利將往海岸、開場 `s57002–s57003` 又預告日記託他之後，還問「誰」送消息；`s57165–s57167` 增加的是送出何種文書而非新「誰」。B 把 `s57158→s57161–s57167` 判作具體回收。作者可在修共同阻擋時一併檢視這句，但不能把 A 異議當正式 OR 失敗。 |
| `no_detour`：A NO、B YES，**合併 YES**。 | A 覺得 `s57113–s57123` 的牲畜、豆子、風暴、旗、獨木舟與病況仍拖慢「為何留下」主線；B 認為這些是到補給站前的短暫障礙，後接 54 天與援助結果，未構成整段岔題。兩種判讀及引用均保留。 |

其餘十題兩位讀者均 YES。相較 R4 的 9／13 合併，R5 對章接與舊箱提問已有可見改善；正式結論仍由本次 12／13 的單一共同阻擋決定。

## 官方 CLI 與交接

執行前後五份創作檔 SHA 均與上表**完全相同**。以 `node tools/video/cli.mjs narrative --slug curio-s57 --answers docs/videos/curio-s57/review/r5-merge/merged-answers.json --workdir /tmp/curio-s57-r5-merge-formal-20261020 --json` 跑正式關卡，結果 **exit 1、`passed:false`、1 個 required fail `no_recap`、0 advisory fail**。[原樣 stdout](cli.stdout.json)、[空 stderr](cli.stderr.txt)、[exit code](cli-exit-code.txt)、[命令與前後 SHA](cli-status.json)、[工具產生的正式紀錄](official-narrative-record.json)均已封存。正式紀錄 `panel_narration_sha256` 是 `9102d2db637fcd5a47e9bb1f4d1ac74a61f89f86a6d8562b6ef0907fcfc09e4c`，紀錄檔 SHA-256 是 `275ca3727588b91e264723490f5fa093b893ee8d42e9497e91c5d15104854f10`；工具在 `--workdir` 末尾另加 slug，原始紀錄路徑在 `cli-status.json`。

**交接：**R5 已完成來源／書面畫面 PASS 與正式敘事 HOLD 的精確版本封存，作者可開始 R6 針對 `no_recap` 的修稿。新創作雜湊須重新凍結、重新查源與請兩位全新隔離讀者各自盲評，再正式合併；R5 不進政策、語音、插圖、配樂或成片關卡。
