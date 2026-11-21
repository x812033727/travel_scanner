# S57 R12｜政策與本地媒體前置關卡

2026-10-21 UTC。**Jev 政策 PASS；本地續作決定已記；網站站主大綱及劇本卡仍待決定。**這份回條只約束 R12 文字版本及配音前置關卡，不是站主親審或音訊核准。沒有購買圖片、片段、配樂。

| 凍結檔 | SHA-256 |
| --- | --- |
| `research.md` | `9663d4a0ea66b1fef3c6e3a0550b8b08cf169a68b1736ad6005d6408ac2cd667` |
| `brief.md` | `0c8284f9bbceb9e751784086a1db35a8c072c9b80f4b75729a2bca15df4ec4bd` |
| `claims.md` | `2c06451d321b3b662af365463452b2fcc989babd0007cb010fdb4bc08579f556` |
| `video.json` | `a01c5dd256e81873e4796a27532e615d7ae328a04190c2d0abcd0b652d0d168d` |
| `script.md` | `1b6252886bff6b17a03cd82da67f95cf51aa3c2a1a4ea606d005b9d0e2bb7474` |

[R12 獨立書面畫面](../r12-written-independent.md)判 PASS；R10 正式雙讀者 [敘事合併](../r10-merge/summary.md)為 13／13 PASS。以現版 `video.json` 對 R10 `official-narrative-record.json` 重跑 `narrativeReviewMatches` 得 `true`：R11／R12 只改畫面提示詞，159 句旁白及 `script.md` 的綁定未變。現版 `lint --json` 回 0 errors、0 warnings、159 句。

在任何配音前，先以 `review-push --report-only` 將本片註冊到 `/admin/videos`；回覆「reported; nothing submitted」。現稿 `format: drama`、`category: explainer`；網站政策回覆也確認採 `questions: "explainer"`，示範題不適用。`policyRequest({doc,brief})` 生成完整旁白 3,437 code points、觀點 90 code points；[請求全文](policy-request-body.json) SHA `44293cfd8731d0f15ab0d7ecdf67c5d90ddf450d33a4020752964ba0298d1206`，連同[五檔及請求預送資料](policy-request-meta.json)先落盤。`automationClient` 設 `attempts:1` 後只 POST 一次，無重送；[原樣回覆](policy-response.raw.json) SHA `f0be331e97d9e79da768ad886a1b021006b6691f21d38f8edbaf128e9dc522d8`，`passed:true`、立場 0.66、示範不適用、建議 0.01、業配 0.01。[解析回條](policy-receipt.json)記 `post_count:1`、`ok:true`；此文字政策關卡 **PASS**。

`review-push --gate outline` 已送出 `brief.md` SHA 的網站卡，回覆 `pending`；`review-pull --gate outline` 回覆 `waiting for the owner`（exit 3）。網站工具未把表格的 A／B 列辨識為可供 Jev 比較的選項（印出「brief has 0 options; the judge takes 2 to 3」），所以沒有 Jev 代選；**這張零選項卡不能作為有效的 A/B 大綱審核**。[最小格式修正提案](outline-format-repair-proposal.md)只提出改為解析器認得的兩個選項區塊，未改動凍結稿。使用者已說「以你推薦的就好不用問我，一直做完所有影片」及「用推薦的決定就好不用問我」；依此授權在本地 `approvals.json` 代記 `brief.md` 推薦 **A** 續作。這是代理的本地決定，站主未親自審讀網站卡。

`review-push --gate script` 已送出同一 `script.md` SHA 的網站卡，回覆 `pending`；`review-pull --gate script` 亦回覆 `waiting for the owner`（exit 3）。依同一委託及上面的來源、敘事、書面畫面證據代記本地劇本續作決定。兩筆本地紀錄的[精確快照](local-approvals.snapshot.json) SHA `34d09830a24352419231adaaced6cc63c4e60e9eb40b406a01c42ac2b3b11406`；它們沒有更動五份創作檔，也不表示網站站主已核准。

媒體上限和配音結果另見[技術音訊回條](../r12-technical-audio/summary.md)。音訊是否可接受要在實際檢查及聆聽後判斷，不能從本地大綱／劇本決定推定。
