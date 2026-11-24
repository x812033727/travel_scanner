# S63 R4｜正式雙人盲讀合併審核

2026-10-22 UTC。**HOLD：13 題中 12 題通過，共同否決 `no_recap`。**此回條在 R5 作者修改之前產生；兩位 R4 讀者的原始票、各自 CLI 回條和輸出保持獨立。

## 凍結、原票與正式重播

R4 `video.json` SHA-256 `0f4cb372e473ed68c54de32fffa9449b98e372a920e7e01700927321eba31364`；`script.md` SHA-256 `85af6713b18b42ad1177063cc3dfc5b5665810d70334678114693460dd3161d7`；`claims.md` SHA-256 `5cbcca08555bf337269a4a9b572bb0c3bd5bd28d19662715f93d9ac151861617`。兩位讀者獨立收到同一份僅含旁白和官方 13 題的 `/tmp/s63-r4-blind-packet.json`，SHA-256 `ebd4da24fcfa7ffaa740c13eed220d17ecc7baa8f503f6c973ef903ad6ffd057`；他們的 13／13 句證據各自逐一匹配該旁白原句。官方腳本內容雜湊 `70604c2503a83892b525c58479a50bb89be91cafed60442aa52e18a613c2a6dd`、題目規則雜湊 `5d71fef2cf3831dc33c0c32b2b297f633c47bfe41fbad18865ae08ed0c91cb75`、官方旁白雜湊 `694a7018a75f9835914737db6928a0ffab52b80b4530f0bba66fc76e96fdcbef` 均相符。

[A 原票](r4-isolated-blind-a.raw.json) SHA-256 `1d4bdc35bdcdb411a24ca63563c0efbb355c5e6e984c9fbd526a7a1e2875b7b3`：11／13，否決 `payoffs` 和 `no_recap`；[B 原票](r4-isolated-blind-b.raw.json) SHA-256 `a833878c4b944dca6b59ad2ee76f771ae7b94c51efd303d33db64385964ba60a`：12／13，否決 `no_recap`。各自的 `.bound.json`、`.receipt.json`、CLI stdout／stderr／exit 隨本 PR 保留。

對原票分別執行原碼 `panelVerdict`，再用 `mergePanelVerdicts` **逐題 OR**；任一讀者的有效引句「是」讓該題通過，兩人同答「否」才是合併否決。[正式合併紀錄](r4-formal-merged-narrative.json) SHA-256 `9fb60d1946d5b4a13214691aa77d73f9c4e75c844e0ab4a16bf107bea3c9f3a4`，完整保留兩位的個別判定；[合併答卷](r4-formal-merged-answers.json) SHA-256 `0ea26dd23cea912785bc5bc90ed85445604858f29367b5d3ffffe18d23ef18f1`。在新的隔離工作目錄重播官方 `node tools/video/cli.mjs narrative --slug curio-s63 --answers <合併答卷> --workdir <隔離目錄> --json`，exit **1**，只剩 `no_recap`。[CLI 狀態](r4-formal-merged-cli-status.json)、[官方判定](r4-formal-merged-cli-verdict.json)和[綁定回條](r4-formal-merged-cli-receipt.json)均已保存；隔離目錄中的 `round=1` 是該目錄首次記錄，正式 R4 紀錄標 `round=4`。

| 題目 | A | B | 正式合併 |
| --- | --- | --- | --- |
| `payoffs` | 否，指出 `s63126` 的提問 | 是，指出 `s63098` 的上車回收 | 是，僅是 OR 規則結果；不把 A 的顧慮抹去 |
| `no_recap` | 否，`s63103` 再說費城友人已知箱子會來 | 否，同一句 | **否；共同阻擋項** |

R4 的[獨立史料及書面畫面覆核](r4-source-visual-independent.md)仍只對原凍結版本有效；正式敘事關卡是 **HOLD**。後續 R5 修稿會使 R4 票的綁定失效，必須重新取得獨立史料／畫面審核和兩位全新的正式盲讀，不得沿用本輪讀者或宣稱媒體准入。尚未呼叫付費圖像或語音，也沒有成片或上架連結。
