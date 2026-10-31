# S53 R45｜`s53033` 第二張書面窄修獨立紙審

2026-10-22 UTC。**PAPER PASS，限書面提案。** 本審是不同於 R45 作者的來源、畫面語義與停線核對；沒有生成圖片、回綁私人圖單、修改影片／claims／音訊、提交 Git 或更新 PR。

| 固定輸入 | SHA-256 |
| --- | --- |
| R45 `video.json` | `52ae0fe8bd2c5f1774af06fb1b74f4da63231122e2f3a868b2742cdc59965fce` |
| R45 `claims.md` | `54ebda69a45ff65becb8fe51650fd0842be8221854ab9d24975b89151f2a4404` |
| `script.md` | `64ffcd8c0e89c4596a7fd08d41bd74f8a16f55fbc9acc2f41d7f9b914ea300fc` |
| [R45 作者提案](r45-s53033-tight-adult-tent-dwelling-author.md) | `bd19d8069f813d8d1ebd7ce14faa3bb78de46ac77d8b97aa6046139e7ab87ea0` |
| [R45 精確差分](r45-s53033-tight-adult-tent-dwelling-structured-diff.json) | `c3d54102efb0a17bb9c927d27afe171107c321f2119c69e7c549921f24881375` |
| 固定 1913 年 *San Francisco Relief Survey* 本機原文 | `d627ed287d8a93b9c00225ea47dbdc4f97c36089a890192a602b993c3c185b72` |

逐行核對固定 [Survey E L4887–4897](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L4887-L4897)：營地指揮官分配木屋，官方營地住戶列第一、營外帳棚及棚屋住戶列第二。`s53033` 旁白「官方營地住戶，有優先分配小屋的資格」只講群組優先資格。新 prompt 裡銀灰髮成年女性站在帳棚旁，後景一棟關門低木屋，是匿名原創的資格示意；claims 同列明說沒有具名個案、存世畫面、實際受配或已入住的主張。木屋「完成」符合前一句「蓋好之後」的敘事時點；關門、屋內無可見住戶和無鑰匙／申請單／進門動作，沒有把優先資格畫成實際分配。此處不能推斷該女性就是某戶獲配者，選圖時仍須維持這個界線。

[R44 不同作者原尺寸退件](r44-s53033-first-native-independent-visual.md)的實質問題是廣景中仍可見較晚近箱型車／露營車正面，雖然 judge 9.29 PASS。R45 將同景從可見長通道的中景收成成年女性上半身、帳棚牆及右後方一棟木屋的緊近景；明列不畫道路、遠景、車輛、其他人物，並以面紋、銀灰髮與成人肩背降低童貌疑慮。這是針對退件原因的合理窄修；負面提示不保證模型遵守，第二張原圖仍須獨立原尺寸人審。prompt 588 字元，未增添來源未記載的具體分配行為。

我核對了結構化差分：現檔 `s53033` 整景及 claims 同列與 `after` 逐字相同，各只出現一次；反填 `before` 後，`video.json` **逐位元組回** R44 SHA `4a3b3447bb1f5d980b0a0965309c1e9a3fda81f64ead117e87910f340f61831d`，claims **逐位元組回** `69d91d3b6e5bf5e551060f0eeab5f7745a1704d5c24e59f1f1d10993554ba4c3`。124 景中只改 `s53033.data.prompt`；其台詞、其餘 123 景及全部 **126／126** 台詞不變。正式 `lint --slug curio-s53 --json` exit 0，**0 errors／0 warnings**，110／123 正文景是 shot，最長相鄰非 shot 為 2。重新計算 `speechHash=05c4d9a79a8708b4`、R45 `visualHash=0d5756d7c9b00bd2`；舊 timeline 同 speech hash，126／126 分句 WAV 仍在，timeline SHA `c75c8bde15f7220862ba8083d6590b7b14bb71c456f896f7b58c13352c88a054`、合成旁白 SHA `08444d50c2f8b70a7079701e157397d9a7c23d08971727164df91a1101e281e1`。

私人有效 manifest SHA `72ee1b654a045a952ed78b12373e54f036f003239b2666523e07540a0496fbd1`、contact SHA `7567d866096ae2ae1d8c92a191b8b6aa74ca1b67c56a4e5582ab6fa9cf666a57`，仍是 R44 `visual_hash=b664a4a74bbb6d8c` 的 **20 KEEP**；20 張選中 JPEG 逐張 SHA 相符，20 景 judge PASS、`needs_review=false`，`s53033` 未入選。STOP 檔在位，jobs 為 `{ "jobs": {} }`（SHA `a9d2c69ab3cb5704417b4f0968a7d8d0dae6eb0e35d37e053463220b30d55ca3`）。ledger SHA `b30c39d2018dd95c2316e5440f08a641a254dae70c9a5df8db977baf1e6929e2`，實付 **US$0.7425／56 images／55 judges／0 reservations**，包含 R44 真實退件費用，低於 US$4.78 集上限。

本 PASS 只准在上述雜湊仍一致時做 **STOP 保護下離線安全回綁**；其後需重新做即時模型、額度、上限、單景 dry-run，才可最多購 `s53033` **第二張**原生圖和一次 judge。必須看完整原圖及選用裁圖，若有較晚近車輛、明顯幼童、與資格／實際分配界線衝突的畫面，立即退件、保留真實花費並恢復 20 KEEP；不得跳到 `s53034`。
