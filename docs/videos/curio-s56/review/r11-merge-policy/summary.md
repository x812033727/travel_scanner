# S56 R11｜正式敘事合併與政策關卡

2026-10-20 UTC。**本精確凍結版的獨立史料／書面畫面、雙讀者正式敘事與 Jev 政策均 PASS。** 這是語音前關卡，不判音檔、真實插圖、站台站主審核或成片。

| 凍結檔 | SHA-256 |
| --- | --- |
| `brief.md` | `09f731c13f1037c963aa5774b936a43e1a187b5c4ae8d09ba158581a705f1a52` |
| `research.md` | `59549e98e6ae258cedfc5b43e6684ecaa1102284d0dee13b0beef6443e4a6fb7` |
| `claims.md` | `8edaf18bee138c3dc88dd2e38e7eebd2c27a9e24158dc0bed696fb4e53904a80` |
| `video.json` | `297b576499068e12fb937bc6032394cf9408f8543065b762a95c6b26ef89cd72` |
| `script.md` | `38ef6dfdbb71bd0b59a441a4d41fc4a89b2b3aed288899a28ec902193b792d2c` |

[獨立來源與書面畫面](../r11-source-independent.md)先對這五檔判 PASS。兩位只讀劇本的讀者各自凍結答案：A 在 `no_recap` 投「否」，因 `s56036` 兩句緊鄰重述高架街段；B 對全部 13 題投「是」。兩票同樣綁定 `panel_rules_sha256=5d71fef2cf3831dc33c0c32b2b297f633c47bfe41fbad18865ae08ed0c91cb75`、`panel_narration_sha256=d019ff8288f5f8e3dd664253e5018ceadcff208cb0944fc9a6fd3bda7f76a30b`，並保持上述 `script.md` SHA。

依 `mergePanelVerdicts` 的固定雙讀者 **OR** 規則，13 題全為「是」，A 的異議保留於[合併稽核](merge-audit.json)（SHA `808bc283539a3cc88423cd2c57f0807ff1e52d7fe03c60f26dc147879750ae8a`）。[合併答案](merged-answers.json) SHA `51c9ff17960d481197a689fd683104bd306617abcd9cb7863c7104dc84b1f5f4`；正式 `narrative --slug curio-s56 --answers .../merged-answers.json --json` exit 0、`passed:true`、`failed:[]`、`advisory:[]`。[原樣 CLI 回條](merged-narrative-cli-receipt.json) SHA `3f4c13813515401abd90f2d13462914d0ca9129b53425c44751afccf7ae46a4d`。

對同一版 `video.json`、`brief.md` 以 `policyRequest({doc,brief})` 建完整旁白請求，`script` 3,192 字元、站主觀點 81 字元，請求 JSON 序列化 SHA `ff3c1b29e0d28af53af4e08652b48c9aa98f32d47af0a71db9d89bff9ac18b32`。[預送資料](policy-request-meta.json)在唯一一次 POST 前寫入；`/api/video/automation/judge/policy` 回 HTTP 200、`passed:true`、`questions:"explainer"`、立場 0.74、示範不適用、建議 0.01、業配 0.01。[原樣回覆](policy-response.raw.json) SHA `810b02b9f2e81873f6818c0fcd072e9fc925c2d85c1900525d3b32fe`；[解析回條](policy-receipt.json) SHA `43847cd11b95bbeb28a4275b74dec72a57977127e3bcd548086e5304fda88e89`，判 **PASS**。請求沒有重送。

本關沒有改任何創作檔、沒有合成語音或圖片配樂。R6 音訊的 21 句殘留旗標屬舊稿，不能轉成 R11 音檔 PASS；下一步仍須本版語音、完整音檢與後續媒體審核。
