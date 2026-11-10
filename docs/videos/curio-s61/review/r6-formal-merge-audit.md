# S61 R6｜兩位正式盲讀合併

2026-10-22 UTC。R6 `script.md` SHA-256 `3fbc7c935bcb1e12f20ce78e68387606061cdb1086930e288f7a973205b11a32`。兩位全新讀者先核官方 13 題面板 SHA-256 `15cfd34356840ae8036c91bc9d8b29f210be52aa761f28379a2bd9ed263fa5ad`，只讀凍結劇本，各自開 CLI 前封存原票；[A 回條](r6-isolated-blind-a.md)、[B 回條](r6-isolated-blind-b.md)及官方綁定均留存。獨立[史料／書面畫面覆核](r6-independent-source-visual.md) **PASS**，不是說故事關卡。

讀者 A **11／13**，No `payoffs/no_recap`；讀者 B **11／13**，No `no_spoiler/no_recap`。依 `mergePanelVerdicts` 逐題 OR，[正式合併紀錄](r6-formal-merged-narrative.json) **12／13 HOLD**，共同 No 只有必答題 `no_recap`。A 指 `s61028/31` 均講瓦礫阻路，B 指 `s61054/61` 均講消防員沒有離崗；R7 可刪兩處重述或把後句改為有史料依據的新動作，並留意 `s61049/50` 的公地問答及開場 `s61005` 提前說出後段行動。R6 正文估算僅高於 325 CPM 的八分鐘門檻約 4.7 秒，改稿須重新量長度而不靠重述補時。

合併紀錄 SHA-256 `dcaa5edde95361937374b663ae5244ea4a1bbf7f78e92304b48226fce2ae677d`、[合併答卷](r6-formal-merged-answers.json) SHA-256 `920b9068d86fe6814874271d566c972fad7e92fdb6c1da673f8ad5f56152ce84`。用合併答卷重播官方 `narrative --slug curio-s61 --answers ... --workdir /tmp/curio-s61-r6-formal-merge --json`，exit **1**，唯一必答失敗 `no_recap`；綁定 `panel_rules_sha256=5d71fef2cf3831dc33c0c32b2b297f633c47bfe41fbad18865ae08ed0c91cb75`、`panel_narration_sha256=606cf8f69ecfa97935cd00c3a71314e1716e0934df9196d4880a05437a661f74`。R6 尚不可合成旁白或開圖。
