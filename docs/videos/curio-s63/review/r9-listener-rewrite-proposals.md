# S63 R9｜四句持續旗標的 listener 措辭提案

2026-10-22 UTC。**僅提案，未套用或重錄。**已讀 `youtube-video/references/prompts/listener-rewrite.md`、現行四旗標及其 intended/heard、相鄰場景與固定 Brown／Stearns 原文。沒有聽原音、沒有自動核准、沒有將同音轉寫等同已核實的發音錯誤。

現行 video SHA-256 `c417bc8c6f0df78e9c4d8e910db038b6f4ea07c760cc7f3c2e69e98224f63f08`；script `63caedb24623bd8339607dd5b11e249ce1a4e6691779279a6d8c64ef5bbd665e`；claims `68c4139f38976d09b9b1b21bdb239eaa4ecb0ddd2f053b0ef445b971d636fe5e`。私人 `review/check-flags.json` SHA `be0b8f07b6e3be8c3a1c5544ef4c428bd8eef262832a114e651662aa101aeeaa`，`review/check.json` SHA `32c7ac9a73b51f76ec3d4f4e70597f69adecb6ce3564f1818898f1ed1758b701`；四個旗標為下列 ID。

| ID | 原句 → 候選 | 原因與保留界線 | claims 固定錨點 |
| --- | --- | --- | --- |
| `s63004` | 箱外有人叫他的時候，他還能答得出來嗎？<br>→ 箱子外面有人叫他時，他還能回答嗎？ | 箱外被轉寫成像外；補箱子外面，答得出來改回答。仍停在能否回應的疑問，沒有提前說他已抵達或成功出箱。 | [B05](https://github.com/GITenberg/Narrative-of-Henry-Box-Brown-Who-Escaped-from-Slavery-Enclosed-in-a-Box-3-Feet-Long-and-2-Wid__64992/blob/a92658e80effa4cce03bb19c13e96ffaaae5fa2b/64992-0.txt#L1494-L1499)、[B09](https://github.com/GITenberg/Narrative-of-Henry-Box-Brown-Who-Escaped-from-Slavery-Enclosed-in-a-Box-3-Feet-Long-and-2-Wid__64992/blob/a92658e80effa4cce03bb19c13e96ffaaae5fa2b/64992-0.txt#L1569-L1572) |
| `s63072` | 原想陪著走的朋友，到了出發時卻沒跟上；費城接收者會得到什麼通知？<br>→ 原想陪著走的朋友，到了出發時卻沒跟上；在費城等著收箱的人，會收到什麼通知？ | 費城接收者被黏成被承接者；加在費城等著收箱的人，保留費城名稱與通知鉤子，不提前在本句給出電報答案。 | [B06](https://github.com/GITenberg/Narrative-of-Henry-Box-Brown-Who-Escaped-from-Slavery-Enclosed-in-a-Box-3-Feet-Long-and-2-Wid__64992/blob/a92658e80effa4cce03bb19c13e96ffaaae5fa2b/64992-0.txt#L1500-L1517) |
| `s63085` | 箱外兩個男人說，他們已走了一段路，該坐下來歇一歇了。<br>→ 箱子外面，兩個男人說，自己已走了一段路，該坐下來歇一歇了。 | 箱／廂同音、已／已經同義，本次轉寫未必是實質聽感錯誤；若需澄清箱子而非車廂，箱子外面只展開器物名稱，不改兩個男人或談話內容，不以候選覆蓋現有旗標。 | [B07](https://github.com/GITenberg/Narrative-of-Henry-Box-Brown-Who-Escaped-from-Slavery-Enclosed-in-a-Box-3-Feet-Long-and-2-Wid__64992/blob/a92658e80effa4cce03bb19c13e96ffaaae5fa2b/64992-0.txt#L1516-L1545) |
| `s63107` | 箱外問：裡面還好嗎？<br>→ 箱子外面的人問：裡面還好嗎？ | 箱外被轉寫成向外，方向與發問者可能混淆；箱子外面的人問使主體清楚，仍是在敲箱後才提問，不編對話聲線或新人物。 | [B09](https://github.com/GITenberg/Narrative-of-Henry-Box-Brown-Who-Escaped-from-Slavery-Enclosed-in-a-Box-3-Feet-Long-and-2-Wid__64992/blob/a92658e80effa4cce03bb19c13e96ffaaae5fa2b/64992-0.txt#L1564-L1605) |

## 逐項固定來源

重開 `/tmp/curio-s63-box-brown-1849.txt`，SHA-256 `6d80216184aaf20433e04aa8d1b6920076211304fcede4a095da3ef5bd62ada2`，即 GITenberg commit `a92658e80effa4cce03bb19c13e96ffaaae5fa2b`。這是 Stearns 根據 Brown 陳述筆寫的出版敘事，候選不把它當錄音或獨立物流清單。

- `s63004`：B05 L1494–1499 在入箱前先交成箱、朋友詢問用途；B09 L1569–1572 是後續敲箱問候與 Brown 回應。開場仍只問將來能否應答，不提前揭結果。
- `s63072`：B06 L1500–1517 說先與費城對應者安排，原想陪行的朋友未同行，只傳電報；候選只換接收者描述，下一句仍首次回答通知方式。
- `s63085`：B07 L1516–1545 明記 Brown 聽見兩人說已走一段路、想坐下休息，之後才翻正箱子。候選保留「說」的聽聞歸屬，沒有添男子姓名、可核計時，亦未把翻箱動作提前。
- `s63107`：B09 L1564–1605 先送住處、一人敲箱，再問 `Is all right within?`；問候的白話意義仍是裡面還好嗎，後一句才由 Brown 回答。

四候選保持費城專名、兩個男人數量及全部事實；沒有改木箱尺寸、旅行時間、日期、人物身分或結果。正式套用後仍需同步 claims／script、lint、全新來源差分覆核與盲讀，再只重錄實際改動 ID 並跑 check-audio；最多兩輪措辭修訂。

## s63028：另列未檢查 HOLD，沒有改詞提案

原句「南希替人洗衣，布朗留下部分工錢；兩人靠這些照顧孩子。」的 claims 錨點 B02 L1245–1257 有直接支持：`she took in washing`、扣除奴役者抽取後其餘收入 `supported our family`。這是一句一般歷史家庭生計描述；本提案沒有為繞過供應商拒絕而另寫版本。

私人 check.json 只有 126 筆 line 紀錄，缺少此 ID；缺席不等於通過。三份本地日誌皆明記同一句轉寫無結果且 `PROHIBITED_CONTENT`：`/tmp/curio-s63-check-audio-resume.log:74`、`/tmp/curio-s63-check-audio-redo1-resume.log:35`、`/tmp/curio-s63-check-audio-redo2-resume.log:17`。故應保留為 **供應商未轉寫／unchecked HOLD**，另待可用的獨立核驗或實際音訊審核；它不在四個可改詞旗標的處理範圍內，不能以重寫這四句就宣稱 127／127 都已通過。

本工作只新增此提案檔；沒有修改 video、script、claims、字典或任何媒體，沒有 Git 提交。
