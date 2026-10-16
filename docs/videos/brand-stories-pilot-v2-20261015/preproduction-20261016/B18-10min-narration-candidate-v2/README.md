# B18 約 10 分鐘口播縮稿候選 v2

**狀態：離線文字複審 PASS；正式製作 HOLD。** 本版只處理 v1 獨立審查報告指出的 O01 年份指代與 T01 排他措辭。v1 報告綁定舊稿、結論仍是 HOLD；[v2 獨立複審](independent-review-v2.md)綁定本版 `candidate.md`／`paragraphs.json`，確認兩處問題已關閉且 24 段連讀無新阻擋。[證據 JSON](independent-review-v2-evidence.json)與審查報告的目前 SHA-256 分別為 `ad6b71da3f0fe7cf228666f0f273f4b16e456756fe5ed36db168e415e1fd1029`、`4cb1c0bf33104ad16e549e6943a47e8065e485657e148dc754a6d12215fd0677`。兩檔只為 repo 路徑保護遮蔽了本機路徑；原始 SHA 分別為 `20d2f7e1bc11787431f07716ecaedd7c66201417a6db7b94846137a5afc3a9b3`、`4fdb5206a3c609c4502df5a9e8aaf1a885e800ceabba840edf4ad6797919ff22`。正式 worker 的逐章查核、敘事審稿及新 script-review 收據仍未完成。

| 檔案 | 用途 |
| --- | --- |
| [candidate.md](candidate.md) | 完整 24 段口播、逐段差異與提問回收；仍是離線文字候選。 |
| [paragraphs.json](paragraphs.json) | 對應段落、units 與待審事項；不是 worker 六章 JSON。 |
| [delta.md](delta.md) | v1→v2 唯二口播改句、計數及新舊審查界線。 |
| [hash-manifest.json](hash-manifest.json) | 凍結稿、v1、審查報告和 v2 的 SHA-256，以及估時口徑。 |

`hash-manifest.json` 審查時原位元組 SHA-256 為 `2d566650e66bc194693618a6c11c6e8c668b7c1305b1ae7573c11ba6f8868f57`；目前只遮蔽本機 Temp 路徑，SHA-256 `c90c4a8186e17d843e278ac7343bfcebf20432bdcd701747d8ac45e1718e213e`。v1 審查全文有同 SHA 的永久副本 [`../B18-10min-narration-candidate/independent-review-v1.md`](../B18-10min-narration-candidate/independent-review-v1.md)。兩版口播與審查結論均未因路徑遮蔽變動。

原凍結稿為 2,729 units；v1 2,293，v2 2,294，對原稿淨刪 435。依每分鐘 230–250 units 的**文字估算**，v2 正文約 550.56–598.43 秒，加 5 秒片頭與 21 秒片尾約 576.56–624.43 秒。尚未做 TTS 或媒體實測，不能據此聲稱達成約 10 分鐘成片。逐章數字見 [delta.md](delta.md)。

v1 目錄、凍結 `scripts/B18.md`、原審稿與 storyboard、`episodes/B18.json`、編譯的 `stories.json`、worker 章稿及主機均未由本目錄替換。本版未啟動付費、匯入或上傳。
