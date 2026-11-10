# S62 R4｜雙盲正式合併

2026-10-22 UTC。兩位全新讀者各自在隔離會話先讀固定正式 13 題，再只讀 R4 劇本；原始票凍結後才執行 CLI 綁定。兩份單人記錄同綁 `video.json` SHA-256 `abed73ef3b14dcfc1b8ff1804f0234919d2f03cffa70a0b4c901a72ce6b14f92`、`script.md` SHA-256 `8343a4f903fe4b405b1e6364cd67737ed7f3aead625b5fe713bf91c873c05c14`、敘事雜湊 `dc5b230a7d70f26b`、工具 script_hash `1c69c6dd6ff7a44ca1332f4726b74e05fc83799bf68e2d651b684c2699aa1a77` 與相同 panel 規則 SHA。

讀者 A 原票 **11／13**，No `payoffs/no_recap`；讀者 B **8／13**，另 No `one_line/no_toc/no_detour`。依 `mergePanelVerdicts` 逐題 OR，兩人共同 No 的必答題只有 `payoffs/no_recap`，故[正式合併 JSON](r4-formal-merged-narrative.json)為 **11／13 HOLD**，保留兩人原票與證據。以合併答卷重播官方 `narrative --slug curio-s62 --answers ... --workdir /tmp/curio-s62-r4-formal-merge --json`，exit **1**，失敗兩題一致。兩位讀者都在空隔離 workdir 首次跑 CLI，單人記錄 `round=1` 是工作目錄記錄序號；合併檔明確標創作 R4，不更改原票。

[獨立 R4 史料／書面畫面覆核](r4-independent-source-visual.md) PASS；仍因故事關卡 HOLD，不可進入 TTS 或付費插圖。R5 只需修未回收的尾段問題及重述的首夜缺點不明，維持史料承認無法辨識的界線；新 SHA 再交新史料覆核與兩位全新盲讀者。
