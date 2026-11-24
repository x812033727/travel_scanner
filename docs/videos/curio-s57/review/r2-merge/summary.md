# S57 R2｜正式雙盲敘事合併與 R3 修稿交接

2026-10-20 UTC。**敘事 HOLD：正式 OR 合併 9／13，四個必答題未過。** R2 [獨立史料與書面畫面](../r2-source-independent.md)是 PASS；本頁只對同一凍結稿合併兩位無前情讀者的原票，不核准劇本、政策、配音、插圖或影片。

| 凍結檔 | SHA-256 |
| --- | --- |
| `brief.md` | `911eb30d15273aa3ab5a57795e28e5a9c3fb4a8fa60059f3f152dc3eb578765a` |
| `research.md` | `9663d4a0ea66b1fef3c6e3a0550b8b08cf169a68b1736ad6005d6408ac2cd667` |
| `claims.md` | `5f03685898d9b256e9d3eaf0d7534efe3eaf4b9393f3ad86e418787ad1bb27f9` |
| `video.json` | `53ee5cd8a93ff5474ffbccbde47379c9872303a4d09442a1f1d699fb8d25b4ff` |
| `script.md` | `604a4f10dbd6ac5b8c7602939a40f58252307a82810bd70d6c2d8b2a63fd29da` |

讀者 A 的[原票](../r2-clean-blind-a/answers.json)與[隔離說明](../r2-clean-blind-a/review.md)為 9 Yes／4 No；讀者 B 的[原票](../r2-clean-blind-b/answers.json)與[隔離說明](../r2-clean-blind-b/receipt.md)為 7 Yes／6 No。兩票各有 13 題、26 個引句均逐字對上當前 `script.md` 的對應 ID。原票 SHA-256 分別為 `b7f7f35ba1666b54aa1c726cbf707e95b3e86a5fdb28b657ec851184fa59abda`、`a0ed3cbf117ead3192bef2ce32009ac5452e475a6005925a56f4f5d8a71d9c8`；兩位的規則雜湊同為 `5d71fef2cf3831dc33c0c32b2b297f633c47bfe41fbad18865ae08ed0c91cb75`，旁白雜湊同為 `edaf94d2a279f739d334ee9be264668e8b403277264d9198e57afaeed0ba16b4`。

用正式 `panelVerdict` 與 `mergePanelVerdicts` 按「任一讀者 Yes 即該題 Yes」規則合併，[完整稽核](merge-audit.json) SHA-256 `daa082661a0f421a6a8e0d0b097423eae6040320befac3246b92820d3c63b27f`。以[合併答案](merged-answers.json)跑 `node tools/video/cli.mjs narrative --slug curio-s57 --answers docs/videos/curio-s57/review/r2-merge/merged-answers.json --workdir /tmp/curio-s57-r2-merge-20261020 --json`，官方 CLI **exit 1、`passed:false`**；[原樣輸出](merged-cli-stdout.json)與[產生的紀錄](merged-cli-record.json)均為以下四題失敗，無 advisory 失敗。產生紀錄 SHA-256 `3d44f4d5d5a3042a5659cb522e2c09fc5d864f351fd706472691391ba4421a`。

| 共同 No 的必答題 | 精確敘事斷點與作者下一步 |
| --- | --- |
| `chapters_link` | `s57164` 問封存日記由誰帶走；下一章首句 `s57165` 卻轉到給班奈特的信，直到 `s57167` 才處理日記。讓章首先接住日記去向，或把上一章尾問改成下章首句確實回答的事；不可硬造未記載的因果。 |
| `payoffs` | `s57134` 問代管貨為何數目對不上，隨後只再次說短少；`s57170` 問兩人為何吃不下早餐，後文也未交代原因。若固定史料沒有原因，改成來源能回答的具體問題或刪問，不要替史料填空。 |
| `no_recap` | `s57094` 重說 `s57092` 已表達的「先保留判斷」；縮成一次，或以新的行動／有來源的新事實推進。 |
| `no_detour` | `s57139–s57143` 接連唸物資清單，`s57141` 直接稱「清單」。濃縮到與是否同行、如何補給有關的關鍵物件及其後果。 |

B 另對 `no_spoiler` 的 `s57004` 與章名 `chapters_are_events` 投 No；A 對這兩題投 Yes，因此依預定 OR 規則合併為 Yes。兩項異議保存在原票，不偷改為兩票一致。R3 修稿須重新凍結五檔，再由其他人重新查史料／書面畫面、兩位新讀者獨立盲讀並正式合併。**Jev 政策 NOT_RUN、TTS 0 次、插圖／配樂 0 次**；R2 的來源 PASS 不放行此敘事 HOLD。
