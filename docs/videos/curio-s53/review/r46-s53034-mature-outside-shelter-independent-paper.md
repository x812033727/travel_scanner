# S53 R46｜`s53034` 營外簡陋棚屋書面窄修獨立紙審

2026-10-22 07:46 UTC。**PAPER PASS，僅限書面提案。** 我不是 R46 提示詞作者；獨立核對固定史料、旁白與概念畫面、精確可逆差分、正式 lint 及私人圖單。沒有生成圖片、回綁私人圖單、修改影片／claims／音訊、提交 Git 或更新 PR。

| 固定輸入 | SHA-256 |
| --- | --- |
| R46 `video.json` | `1e16b8aaf5718f0df251947136df7e51ca3032346280703c6061feeae381f91d` |
| R46 `claims.md` | `81e622a5be8daf793c3f415d803274b5455fb59a0c6380eaa3dcc3689b838f3a` |
| `script.md` | `64ffcd8c0e89c4596a7fd08d41bd74f8a16f55fbc9acc2f41d7f9b914ea300fc` |
| [R46 精確差分](r46-s53034-mature-outside-shelter-structured-diff.json) | `8b27e43edfd08cf803527ff273f63f46644bbda88e837c471031087b6dd2d8e9` |
| 固定 1913 年 *San Francisco Relief Survey* 本機原文 | `d627ed287d8a93b9c00225ea47dbdc4f97c36089a890192a602b993c3c185b72` |

逐行核對固定 [Survey E L4887–4897](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L4887-L4897)：救濟木屋由營地指揮官分配，官方營地住戶列第一，**營外棚屋和帳棚住戶列第二**。`s53034` 旁白「營地外搭棚的人排在後面，得等官方營地先分完」是先後次序的口語說法；新 claims 明確限制為群組順序，不推斷每位官方營地住戶必獲屋、營外住戶個別等候日數、特定分配事件或入住日。新提示的一名灰髮、有面紋及成人肩背的匿名成年女性與完整的低矮補丁帆布／粗竿／少量木板臨時棚屋，是**營外住戶身份的原創概念**，不是史料所記人物、個別棚屋或營地邊界。背景只留空地；沒有已完工可搬入小屋、折棚、鑰匙、分配文件或搬入動作。此構圖針對 [R45 原提示付費前 HOLD](r45-s53034-unchanged-outside-camp-preflight.md) 所見「在木屋旁折帳棚」可能誤示已獲配或搬屋的問題。提示詞排除車輛、童貌與現代標示，但負面提示不保證模型遵守，原生圖仍要原尺寸人審。

結構化差分中的 `s53034` 整景及 claims 同列與現檔 `after` 逐字相同，反填 `before` 後 `video.json` **逐位元組回** R45 SHA `52ae0fe8bd2c5f1774af06fb1b74f4da63231122e2f3a868b2742cdc59965fce`、claims **逐位元組回** `cb950a5cfe810ac1d6e28065e17b80aced461bbaefe53cd07a48bfa869e29b7c`。124 景中僅改 `s53034.data.prompt`；台詞、camera、visual、其餘 123 景及全部 **126／126** 台詞不變。正式 `lint --slug curio-s53 --json` exit 0，**0 errors／0 warnings**。重算 `speechHash=05c4d9a79a8708b4`、R46 `visualHash=12d4b1dcd57ea4c0`；R45 音訊 timeline SHA `c75c8bde15f7220862ba8083d6590b7b14bb71c456f896f7b58c13352c88a054` 和旁白 SHA `08444d50c2f8b70a7079701e157397d9a7c23d08971727164df91a1101e281e1` 未改。

私人有效 manifest SHA `64d3e65e1daf2c296dc6462934bdaf046fe1b094b1f1006704a4e27d659c8bc9`、contact SHA `a2604cc3c1a719f3bd3227a37ac8195ad4d4b6ce5f7b228a09f996a65d3aef7c`，仍是 R45 `visual_hash=0d5756d7c9b00bd2` 的 **21 KEEP**；21 張選中 JPEG 逐張 SHA 相符、21 景 judge PASS、`needs_review=false`，`s53034` 未入選。正式 `keyframeProblems` 只有尚缺的 89 張，既收圖問題零。STOP 在位，jobs `{ "jobs": {} }`（SHA `a9d2c69ab3cb5704417b4f0968a7d8d0dae6eb0e35d37e053463220b30d55ca3`）。ledger SHA `a94e6c9dc54d3a7b8774df6f3ffd8dccb84b18428e47c07995ad33ee01c3c122`，實付 **US$0.7560／57 images／56 judges／0 reservations**，含先前退件真實費用，低於 US$4.78 集上限。

本 PASS 只准在上述雜湊仍一致時做 **STOP 保護下離線安全回綁**；其後須重新做即時模型、額度、上限與 `s53034 --takes 1 --dry-run` 檢查，才可最多購 `s53034` **第一張**原生圖和一次 judge。原圖及入選裁圖若把棚屋畫成已分得的救濟木屋、折棚搬遷、明顯幼童、可辨近代物件或系列畫風漂移，立即退件並恢復 21 KEEP；不可跳到 `s53036`。
