# S53 R21｜第二章兩景最後的定點提示詞修補

2026-10-22 UTC。**作者候選；尚待非作者按新雜湊紙審，未開 R21 付費圖片。**R20 [原生試畫停線](r20-two-native-stop.md)後，我直接檢查兩張 1280×720 原 JPEG：`s53010` 是偏寫實的成年人物和縱深長街／電線桿，未畫出裁近的院落；`s53018` 雖有機器 9.29/10 PASS，畫面上緣仍是一整排現代高樓，帳棚間的路也過寬。兩張都維持人工 REJECT，舊圖不可當保留圖。

| 景 | R21 僅修改的書面畫面 | 史料與後續界線 |
| --- | --- | --- |
| `s53010` | 「中近景」只容銀鬢、有鬍子與皺紋的成年住戶及一面舊木院牆。住戶轉向牆後升起的濃煙；人物與牆填滿邊界，讓模型不再借遠景長街呈現火災。較圓的頭與結實短身形是系列人物比例提示，不宣稱可辨目擊者。 | 固定 1913 年 *San Francisco Relief Survey* [L1438–1465](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L1438-L1465)記 1906-04-18 地震與後續大火；院牆與匿名住戶是概念示意。R19、R20 各有一張原生退圖；**下一張若試畫，即第三／最後一次**，原圖仍錯則只能同章合格圖重用或來源卡，不能第四次重畫。 |
| `s53018` | 「近景」從帳棚之間看，左右兩側帆布和後方第三面帆布牆封閉整個視野，只留約一人肩寬裸地；銀鬢成年工作者側身穿過。畫面沒有可展開高樓天際線或寬大道的背景。提示詞不使用 `South Park` 英文專名。 | [L4848–4870](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L4848-L4870)說南公園面積不足以容納分開的小屋；擠近的帳棚是概念示意，非南公園原始照片或平面圖。R19 是供應商拒絕且無原圖，R20 才是第一張實際退圖。 |

[可逆結構差分](r21-two-prompt-structured-diff.json)逐字保存 R20→R21 的 `scenes[9].data.prompt`、`scenes[14].data.prompt` 與 claims 的同兩行畫面說明。反向回填可位元組還原 R20：`video.json` SHA-256 `f868ce55f98f7868a8052098d0f6439344585df9e0fa1d0cb32eb0ddbbac21dd` → **`4ac9a518d7387ea66918a89946636ee7dd6412f4926fbe7c5ccbb5a5a249f64a`**；`claims.md` `81f03c571693ff7b28e9898f64dcbb64e9442ec66bde2597c6dfcd7874b7ef1c` → **`02ee7918a362ce130bed4a9e2c1491f0da80880207d7c57d6aa9eae1820a3022`**。解析比對僅有這兩個 prompt 葉節點與兩個 claims 行變更；其他 122 景、全部 126 句旁白、章界、運鏡、brief/research 均不動。`script.md` SHA 仍 `64ffcd8c0e89c4596a7fd08d41bd74f8a16f55fbc9acc2f41d7f9b914ea300fc`。CLI [lint](r21-two-prompt-lint.stdout.json) exit **0、0 errors／0 warnings**；新提示詞長 504／484 字元，短於 R20 已紙審通過的模型字元上限。

私人 manifest SHA-256 `75c59a8855284a3defe6f2acfd4f0c30bb52f344e1756bc29ef573cadfb5f1b7`、帳本 SHA-256 `c385ac8815a3ef7e3fa500c79dd1039ee6b9f21fc94bafc2c0c0deebd52c435b` 與 R20 停線時相同。首章八張及 R19 六張共 14 張先前 KEEP 候選不在本輪差分。帳本仍 **US$0.4320／33 image／32 judge／0 預約**，低於整集 US$4.78 上限；`STOP` 仍在位。唯讀 MiniMax dry-run 因 `https://mokaair.com` fetch 失敗而 exit 4，不能藉此宣稱服務已可用，也沒有造成付費。先由另一人覆核固定來源、兩景提示詞與可逆差分；之後才能在 STOP 與上限下各限一張原生 JPEG，直接目視，再決定是否能保留。網站卡、人耳審核、完整分鏡與成片均未完成。
