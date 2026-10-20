# S52 R18｜無歷史脈絡雙盲正式合併

2026-10-20 UTC。兩名讀者用 `fork_turns:none` 各自進入空白對話，投票前只讀相同 R18 劇本和官方固定 13 題，不讀前版審核、來源或對方答卷。共同劇本 SHA-256 `1a5d07020b2f15555f3359d31ecf6d90c6f8cb4780c8d3159e4c7cc2544d6857`。先前繼承上層對話的兩份 R18 答卷保留為參考，**不參與本次正式合併**。

| 答卷 | SHA-256 | 是／否 |
| --- | --- | --- |
| 無背景 A `r18-clean-blind-a.json` | `b46976e678c12b5de5c4b7c7f1a11d415384f9d1f98d857d23e9b6ebc86b9cf6` | 9／4 |
| 無背景 B `r18-clean-blind-b.json` | `cea7a7dd082e9f87de5a5b1e4795b6b250598068b27c0e1be0b01dbb253d1987` | 8／5 |
| 正式 OR `r18-clean-merged-answers.json` | `a1612ed190a7a3cecc495b12490453ba475c67c8c4e7b0bb0b093d74070fd592` | **9／4，FAIL** |

兩人共同判 `chapters_link`、`payoffs`、`no_recap`、`no_detour` 為否：暗影難辨的問答重述舊結論、首次接觸定義無回呼重複、木星衛星觀測小段與金星讀秒主線銜接不足。B 額外判 `no_toc` 否，A 判是；依任一讀者答是即算是的正式規則，`no_toc` 通過，異議仍留 B 原卷。

實跑 `VIDEO_WORKDIR=/tmp/curio-s52-r18-clean-official NODE_USE_ENV_PROXY=1 NODE_NO_WARNINGS=1 node tools/video/cli.mjs narrative --slug curio-s52 --answers /workspace/travel_scanner/docs/videos/curio-s52/review/r18-clean-merged-answers.json --json`，退出碼 1；原始 `r18-clean-cli-receipt.json` SHA-256 `201c39467d2f809cac9e766b6f0c79d52ac9d3917ee772d5af001817384402cc`，`passed:false`，唯一四個 failed 如上，`advisory:[]`。

R18 獨立史料、主張及書面畫面另已 PASS；敘事 **HOLD**，不開 R18 新句 TTS。作者須窄幅修正共同失敗處，避免為了時長填回重複段落，然後重新做來源覆核和兩份無背景盲讀。
