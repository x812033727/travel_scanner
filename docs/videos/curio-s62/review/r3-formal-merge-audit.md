# S62 R3｜雙盲正式合併

2026-10-22 UTC。兩位讀者在無前票的獨立會話中，先讀固定的正式 13 題，再只讀 R3 劇本，凍結原始答案後才開啟 CLI 綁定。兩份單人記錄均對同一 `video.json` SHA-256 `396e78030054ee6f8a4dca15c83be8e4361dd6530bb1c8b99e75cdb3e2922ebf`、`script.md` SHA-256 `e8f1179f11184dea4eedabddc30f6820305e2c0ef709f061b26484961d622110`，且 `narrative_hash` `fafdb295c59584bd`、工具 `script_hash` `a92c2c40a074419a53a91220433a81038bcdcbf8ec54b7713a95286125f2df1d`、panel rules SHA 相同。

[讀者 A](r3-formal-blind-a.receipt.json) 9／13、[讀者 B](r3-formal-blind-b.receipt.md) 9／13。`mergePanelVerdicts` 的逐題 OR 合併為 **9／13 FAIL**，兩人共同 No 是必答 `no_spoiler`、`payoffs`、`no_recap`、`no_detour`；[正式合併 JSON](r3-formal-merged-narrative.json)保留兩份原票及各題證據。以合併答卷重播官方 `narrative --slug curio-s62 --answers ... --workdir /tmp/curio-s62-r3-formal-merge --json`，exit **1**，失敗四題一致。B 在空的獨立 workdir 首次跑 CLI，故其單人檔 `round=1`；此數字是該 workdir 的記錄序號，不是創作版次。合併檔明確標 R3，不改任何原始票。R3 的[獨立史料／書面畫面審查](r3-independent-source-visual.md) PASS，但敘事關卡 HOLD，不能進 TTS 或付費圖。

下一版須移除開場提前揭露的可見點數、回答開場缺點的可核實部分並清楚保留無法辨認的部分、刪正文內重述，以及把英譯連結資訊留在說明欄而非旁白岔題。改稿後新 SHA 須再受史料與兩位全新盲讀者覆核。
