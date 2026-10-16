# A01/B18 審查證據路徑遮蔽紀錄

2026-10-16 的 #1510 CI 在 `repo-hygiene.test.mjs` 發現四份 JSON 證據含本機使用者絕對路徑。此處只將路徑前綴改為 `<repo>` 或 `<home>`，保留來源內容、旁白、審查判斷、各候選檔及被引用來源的 SHA。原始位元組可由 `23f519f1389903379b81dfc79eb9896a826488d6` 的 Git 版本核對；公開版 SHA 改變是路徑遮蔽的結果，**不是重新審稿或 worker PASS**。

| 檔案 | 原 SHA-256 | 公開版 SHA-256 |
| --- | --- | --- |
| `A01-round10-independent-review/evidence.json` | `ed24f1fad05ed561a9758491e5eab2a3bcef22b4ccf9cef0caf6ad57342136f5` | `f4adbdc98897b4f438b5897859101e8f7f7658d99d5b26077cbf8fe89e701018` |
| `B18-10min-narration-candidate/independent-review-v1-evidence.json` | `8db0d7d5fe32ac7a4ad56bc526c98fc7667892e1fc34797678d519bce8751939` | `f308d36a8b4af253939db85e71756b1df3edcb8bdd075a28d51b3ca0948bbdc3` |
| `B18-10min-narration-candidate-v2/hash-manifest.json` | `2d566650e66bc194693618a6c11c6e8c668b7c1305b1ae7573c11ba6f8868f57` | `c90c4a8186e17d843e278ac7343bfcebf20432bdcd701747d8ac45e1718e213e` |
| `B18-10min-narration-candidate-v2/independent-review-v2-evidence.json` | `20d2f7e1bc11787431f07716ecaedd7c66201417a6db7b94846137a5afc3a9b3` | `ad6b71da3f0fe7cf228666f0f273f4b16e456756fe5ed36db168e415e1fd1029` |

`B18-10min-narration-candidate-v2/independent-review-v2.md` 原 SHA 為 `4fdb5206a3c609c4502df5a9e8aaf1a885e800ceabba840edf4ad6797919ff22`；為了在表格標示目前公開版 SHA 並解釋原始雜湊，文字說明亦更新，目前 SHA 為 `4cb1c0bf33104ad16e549e6943a47e8065e485657e148dc754a6d12215fd0677`。其獨立文字判定和 24 段候選旁白沒有變動。

`B18-worker-conversion-plan/source-pins.json`、`B18-authored-chapters-candidate/input-pins.json` 及其後續 pin 檔已改綁公開版 SHA。v2 審查證據內記錄的 *review-time* 來源 SHA 仍為原始值，應讀作當時觀測，不可誤認成目前檔案雜湊。A01 的 round9 FAIL 與 B18 的正式 worker／媒體待辦均維持原判。
