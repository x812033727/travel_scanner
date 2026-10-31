# S53 R47｜`s53036` 未燒原屋住戶領小屋畫面獨立紙審

2026-10-22 UTC。**PAPER PASS，限書面提案。** 我不是 R47 提示詞／claims 作者，獨立核對固定史料、逐位元組可逆差分、畫面語義和目前私人停線狀態。沒有修改影片、claims、音訊、私人圖單、帳本、任務、Git 或 PR，也沒有生成圖片或 judge。

| 固定輸入 | SHA-256 |
| --- | --- |
| R47 `video.json` | `bb1f7bcd556f8c687cc4683eeeb665e0edd762a5e7f39c0ab42e9cfa433bae1c` |
| R47 `claims.md` | `a7663e1ce64e53c31cdd36746237417955122ddfd52cc9c9276b45684e9c3612` |
| `script.md` | `64ffcd8c0e89c4596a7fd08d41bd74f8a16f55fbc9acc2f41d7f9b914ea300fc` |
| [R47 精確差分](r47-s53036-mature-cottage-recipient-structured-diff.json) | `e2ae4410f02982a628c8b731854a4c3069c796d1548e778a53abc6b6146d0858` |
| [原版申請單提示預檢 HOLD](r47-s53036-unchanged-application-preflight.md) | `0537b6817bdf4e63ff25c1e1fec22b56b61e18fa372e4ccd61a92571b562395f` |
| 固定 1913 年 *San Francisco Relief Survey* 本機原文 | `d627ed287d8a93b9c00225ea47dbdc4f97c36089a890192a602b993c3c185b72` |

固定 [Survey E L4887–4897](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L4887-L4897) 明記：`Some who had not been burned out, but needed to be better housed, received cottages and moved them for permanent use to lots which they owned or leased.` `s53036` 台詞只說**其中有人原住處未遭焚毀、仍需改善住房並領到小屋**；下一句 `s53037` 才談搬往自有或承租地。調查沒有記申請單、書面審批、某戶姓名或精確受配日期。R47 刪去原版主角閱讀 `blank cottage application` 的動作，改為明顯成年的匿名女性站在一棟低矮完工木屋旁，遠後方以一處完整但擁擠的舊住處提示需求。沒有鑰匙、申請單、官員、名冊、交屋儀式或搬屋車；前後房屋的距離和相對位置只是概念構圖，**不能當真實地塊、搬屋路徑或同戶個案證據**。新 claims 明寫這些界線，也沒有把「有些人」擴張成所有未被燒毀原屋的居民。

新 prompt 的銀灰髮、面紋與成年肩背線索，比原版僅寫 `anonymous adult` 更能避開本集多次出現的童貌誤讀；一棟關門的小木屋讓「領到小屋」可視，未指定已入住。背景的完整舊住處與小屋同框可能在出圖時被模型畫成同一地點的確定紀錄，故正式原圖／選圖仍須原尺寸檢查：若畫出申請文件、交鑰匙、所有權標示、現代物、明顯幼童、完工大型住宅，或將舊屋／新屋畫成有可辨史料身分與搬遷結論，即 STOP。此 PAPER PASS 不預判原生圖 HUMAN KEEP。

結構化差分的 `after` 與現檔逐字相同、各只出現一次；把 `s53036.data.prompt` 和 claims 同列反填 `before` 後，`video.json` **逐位元組回**已提交的 R46 SHA `1e16b8aaf5718f0df251947136df7e51ca3032346280703c6061feeae381f91d`、claims **逐位元組回** `05cf94f523ccdcd825ceb7dc78b0c5b61945f0bd3d4367a00364fe095dba50aa`。`s53036` 台詞、其他 123 景及全部 **126／126** 口播句不變。正式 `lint --slug curio-s53 --json` exit 0，**0 errors／0 warnings**；重算 `speechHash=05c4d9a79a8708b4`、R47 `visualHash=9568d4ed7e317c66`，舊 timeline SHA `c75c8bde15f7220862ba8083d6590b7b14bb71c456f896f7b58c13352c88a054`、合成旁白 SHA `08444d50c2f8b70a7079701e157397d9a7c23d08971727164df91a1101e281e1`。單景非付費 `--dry-run` exit 0，prompt **650／1072** 字元、MiniMax `image-01` ready；這不是正式額度或集上限預檢。

私人有效 manifest SHA `116b28ed12436e90f4fe1f16300ed670372691df94325ec7326556087512532d`、contact SHA `50d9bbd8f253f4e1dc1615e80e6671a62a6696d2570731227bd09eab427a74ea`，仍是 R46 `visual_hash=12d4b1dcd57ea4c0` 的 **22 KEEP**。22 張所選 JPEG 逐張 SHA 相符、22 景 judge PASS、`needs_review=false`；`s53036` 尚未開畫。STOP 在位，jobs `{ "jobs": {} }`（SHA `a9d2c69ab3cb5704417b4f0968a7d8d0dae6eb0e35d37e053463220b30d55ca3`）；ledger SHA `ca3c43a1e588bc38daa689a3044a4983a42412459b57fbdec71e475375c032d0`，實付 **US$0.7695／58 images／57 judges／0 reservations**，低於 US$4.78 集上限。

本 PASS 只准在上述雜湊仍一致時做 **STOP 保護下離線安全回綁**；其後須重新查即時模型、配額、集上限及單景 dry-run，才可最多購 `s53036` **第一張**原生圖與一次 judge。正式原圖及選用圖必須另做原尺寸人審；若有材料性來源／旁白誤導或畫風漂移，立即停線並保留真實已付費用。`s53037` 不因本審而放行。
