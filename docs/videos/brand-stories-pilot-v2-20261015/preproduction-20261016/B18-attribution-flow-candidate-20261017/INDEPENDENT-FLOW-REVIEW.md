# B18 來源承接候選：獨立差異審查

**審稿者：`/root/b18_successor_independent_review`；日期：2026-10-17。結論：本次兩句改動未見 P1／P2；上一版連唸三次 J-Net21 的文字節奏 P2 已消除。整片仍 HOLD。**

父版 `B18-attributed-narration-candidate-20261017/sha256.json` 的 SHA-256 是 `7f39a6b95a8233ff4cc32986588c71431886987c75a5d4cd9764c1bf1910753f`，本版 manifest 是 `8b77652b8263fd33b02a95a3ee1288e85f96d6a847b4b88c2efd488a84ca3754`。我獨立重算本版 manifest 列出的 14 個檔案，零個不符；`build.mjs --check` 回報 `PASS_OFFLINE_CANDIDATE_HOLD`、85 景、88 句、65 筆主張。父版獨立報告固定為 `67c2f823fcf15bdfa3a9babc650d461154f7ab5f5b3fdb28d95057bb57642f5c`。

比對父版原始資料後，**只有** `remapped-chapters/idea.json` 的兩句有效口播文字更動：`idea-s032`／`i6`／line `3f5899d2` 由「J-Net21 說」變成「同一篇報導」；`idea-s033`／`i7`／line `464491bc` 由「J-Net21 記載」變成「報導還記載」。兩句都只有 `text`、沒有 `say` 覆寫，實際送旁白的文字就是本版文字。緊接前一景 `idea-s031`／`i5` 明唸「依 J-Net21 的記載」，中間沒有切到別的文獻，因此 `i6` 的「同一篇」與 `i7` 的「報導」都有唯一、可聽見的指向；`attributed:true` 的歸屬仍成立。[J-Net21](https://j-net21.smrj.go.jp/special/expo1970/20231113.html)直接支持板片別稱與約十年／1957 試作，這兩句沒有變更事實。

相鄰三景如今只在 `i5` 唸一次英數來源名，`i6/i7` 用順接指稱，按**文字朗讀**已不再有上一版每景重複「J-Net21」的 P2。`i3/i4` 的撲克牌／名片兩來源版本仍分開；沒有新添因果或混淆哪個說法。此結論是文字層級，**沒有 TTS 試聽**，不能保證「J-Net21」的發音、停頓或實際聲音自然；後續 listener 與 `check-audio` 仍需審。

`B18.json`、`series-adoption.json`、`claim-coverage.json` 和其他五章均與父版位元組相同；canonical story SHA-256 維持 `d0a9e19d311def1130c50cf6ba83a9ffb7f58c435e7c2460901abb211fe03648`。65 筆 claim 的文字、source／fact 映射及 `UNCHECKED` 判定也完全相同；法院 PDF 專屬 `h7/t7/t8` 和 `reviewer_only:[4]` 的要求保留。row hash 不變**不表示**逐字稿或旁白審核可沿用：新完整稿的 I03／I04 須與這兩句同步並獨立重審。

**可進下一步離線完整稿／聽眾複核；不可當成正式機逐景查核或影片完成。** 最終 row 仍要新 hash 綁定審核、65 筆正式 worker verifier，之後才有 TTS、圖像、CC 與成片關卡。本次沒有主機操作、匯入、付費呼叫、媒體、合併或上傳。
