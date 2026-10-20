# S39 旁白製作與整集預算交接

日期：2026-10-20。工作目錄：`/workspace/.video-work/curio-s39`。本收據記錄 **R3a** 固定稿的本機製作關卡與授權來源，不代表站主親自讀過或聽過本集。語音經兩輪定向重錄仍有六句未通過；後續 R4 最小修稿與新雜湊見 `verify-10.md`。本頁所列 R3a 劇本核准及敘事判讀**不可沿用至 R4**。

## R3a 固定稿件與獨立檢查

| 檔案 | SHA-256 |
| --- | --- |
| `brief.md` | `52b2ed80008fc16dfb4570863b13fddc535ca9ff87a6bdadc489245d93c3b635` |
| `script.md` | `f0b16c8dc9b5525fd07097851f1ec0c1e89f0987541c255cc2ef180afc19af28` |
| `claims.md` | `52a3a091510c84fff3985fa09e43379ddb15a4ef0f9206a03fdddd84d8935139` |
| `video.json` | `cefceb2ab42451f962bdad8f4910ac12b2aae849b927f6bc363c527e2d214264` |

R3 獨立盲讀封存 `/tmp/curio_s39_r3_fresh_blind_seal.md`（SHA-256 `b5d124c48420e366f01fdc311db39d0ecc3a5fe3a88eee892fe0dd7004037ea1`）：13/13 題通過。R3 來源與畫面稽核 `/tmp/curio_s39_r3_source_visual_audit.md`（SHA-256 `dfa3139a4ce8d47abeeca5f9346363a711a2db284f25a92da2b37529a3c60ade`）：五份固定來源、89/89 主張通過。R3a 聚焦提示詞覆核 `/tmp/curio_s39_r3a_focused_prompt_audit.md`（SHA-256 `1fac8d61df59233b89deb0167ed6ef60acccdacc6a5a4fcbbf7eace486f42863`）確認僅 13 個提示詞葉節點變動，均通過；稿件與主張不變。`lint --slug curio-s39 --json` 為 0 error、0 warning。

官方 `narrative` 指令的第一輪匯入因引用 `cs001` 缺少規定的方括號而判失敗；這是封存格式問題，並非新增的敘事負評。第二輪沿用同一位獨立讀者的 13 個判斷，引用改為精確的 `[cs001]` 等行號及原句，`review/narrative.json` 顯示 `passed: true`、`failed: []`、`round: 2`，綁定 `script_hash: e451ae752ded708746b6b66b68e1af6151ca0069e2784f9c3226de0d68594d51` 及 `panel_narration_sha256: b041706382a3a7aea7011f96b6b1f20d052ef78bfc1dd6462a75dbc7f58d45a3`。匯入用 JSON 為 `/tmp/curio_s39_r3_narrative_answers_cited.json`（SHA-256 `2ce0b0e535d4361690e1dda3e51526c76924f178d52f6ea7c44a73fa077dac4a`）。

## 核准記錄的實際來源

站主在對話中的持續指示為「以你推薦的就好不用問我；一直做完所以影片」。製作代理依此採用企劃推薦的 A 案，於本機 `approve --gate outline` 將 `brief.md` 的上述 SHA 登錄；同時依已通過的獨立盲讀及史料稽核，以 `approve --gate script` 登錄上述**精確劇本 SHA**。`/workspace/.video-work/curio-s39/approvals.json` 的兩筆備註均明說這是依既有委託授權所作的代理登錄，**沒有宣稱站主親自看過 S39 企劃或劇本**。

## 旁白與後續媒體關卡

`tts --dry-run`：Gemini Sulafat 頻道聲音可用，預估 87 次請求、約 2,218 個計費字元，約佔免費層 0.4%。首輪實際 `tts` 完成 **87 次請求、2,218 個計費字元、0 次重用**；首輪 `narration.wav` SHA-256 `b75828f078a802fc1dc194a7944f4dbf5ec0d92faa61bc9a301117ca31af5f25`。`ffprobe` 量得首輪全軌 **560.9 秒（09:20.9）**。

首輪 `timeline.json` SHA-256 `3dfbcfac01074b3448a21855c62b399a0ba93a87709cb151ef5add5a7047ac98`，30 fps、16,827 影格。正文從 `cs007` 第 1,234 格到 `cs086` 第 16,302 格，長 **15,068 格＝502.27 秒（08:22.3）**，符合至少八分鐘的故事正文門檻。重錄後須再量一次。

首輪 `check-audio` 跑完 89/89 句：59 句逐字相同，10 句僅同音字或口語填詞不同，5 句經 Jev 判定可接受，**15 句標記**（`review/check.json` SHA-256 `ed608f713b46ad7bc6933230604034563303abaa2c9fa20bab118334ee86e595`；`review/check-flags.json` SHA-256 `75e5504631de64879e48ea604db95336e3f7cbde70f69d81964e36c49b898bc2`）。標記中包含 `cs018` 的「祭兆」聽成「吉兆」、`cs079` 的「速記」聽成「數據」、`cs085` 陳述句聽成問句，不能放行。首輪 `tts --redo review/check-flags.json` 只重錄 15 句，**劇本文字與劇本 SHA 不改**；其後重跑逐句檢查和時間軸測量。

定向重錄兩輪後，標記數依序降到 **7、6**，仍未達 0。第三輪舊稿音軌全長 561.4 秒，正文 502.77 秒；最後六個標記為 `cs010`, `cs021`, `cs036`, `cs049`, `cs079`, `cs084`。因此未送出音訊審核，也未啟動插圖。六句改寫與完整第三輪雜湊見 `verify-10.md`；新稿需要重新獨立敘事與史料覆核、精確 SHA 核准、補錄與音訊檢查。

`keyframes --dry-run`：86 張插圖，每張最多三次；MiniMax image-01 一次全部約 **US$1.16**，整集插圖的**硬上限 US$3.48**，目前本集插圖花費 US$0.00。`music --dry-run`：Gemini Lyria-3.5 對 560.9 秒影片預計產 566 秒無人聲配樂，報價約 **US$0.08**。因此**整集插圖與配樂的最高預算為 US$3.56**（US$3.48＋US$0.08）；目前兩者均未付費生成。已向統籌通知此上限；在音訊檢查和 S04 共享 MiniMax 每小時配額協調前，不開插圖請求。

交接文件更動後重跑 `npm run test:docs-videos`：236/236 通過；`lint --slug curio-s39 --json`：0 error／0 warning、89 句。
