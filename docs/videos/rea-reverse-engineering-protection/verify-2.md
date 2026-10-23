# verify-2：rea-reverse-engineering-protection（round 2, 2026-10-16）

獨立查核，非撰稿人，亦非 round 1 查核者。可編輯 `video.json`、`claims.md`，本檔為第二輪報告。未跑 git。
範圍（依 verifier 提示 Round 2 規則）：重查 round 1 改過的每一筆事實、round 1 確認項的隨機三分之一、以及 round 1 後新增的「修正版實跑」主張。
外部事實用 `gh api`（REA repo / README）核；內部 RUN 事實比對 `runlog.txt`、`test-target/*.cs`、`license-server.mjs`；HMAC 以 node crypto 本機重算。

## A. round 1 改過的事實（確認現況）

| # | 主張 | 出處 | 來源 | 狀態 | 裁決 | 讀數／比對 |
| --- | --- | --- | --- | --- | --- | --- |
| c02 星數 | 約 28 萬（讀到 276,024 星、69,538 fork） | stars.note；l001；l007；claims c02 | `gh api repos/morluto/rea` | 200 | CONFIRMED（未改，見備註） | 今日讀到 **276,543 星 / 69,688 fork**；進位仍為 28 萬；同日漂移 ~500 星（0.19%），非 material，依 Round 2 規則「有重大移動才改」故不改卡片精確值 |
| c09 折扣 | region=EDU 打六折（NT$150→NT$90） | three-bugs；bypass-table；claims c09；runlog [B3][B7] | NoteVault.cs 行65-71 | n/a | CONFIRMED | NT$90/NT$150=0.6＝付 60%＝六折（省四成＝40% off，與原碼註解「40% discount」一致）；三處用語全一致 |
| c08 行數 | 自寫「八十行」小程式（原始碼 79 行） | note-app；l00g；claims c08 | `wc -l NoteVault.cs` | n/a | CONFIRMED | 實測 79 行；「八十行」口語化、原碼 79 行相符 |
| c21 端點 | /api/travel/analytics/config、/api/travel/analytics/events | web-visible；l01y | runlog.txt [W1] | n/a | CONFIRMED | 與 [W1] 兩端點一字相符 |

## B. 新增的「修正版實跑」主張（c24、fix-code、fix-run、[FIX1-3]）

| # | 主張 | 出處 | 來源 | 狀態 | 裁決 | 比對 |
| --- | --- | --- | --- | --- | --- | --- |
| FIX1 | REA 掃新 client 剩網址、0 個密鑰 | fix-code l026「密鑰不見了,只剩一個網址」 | runlog [FIX1]；NoteVault-fixed.cs | n/a | CONFIRMED | [FIX1]「含 secret：false」、字串僅 NV_LICENSE_URL/端點/UI 字串；fixed.cs 內無任何密鑰、只有 VerifyUrl |
| FIX2 | 伺服器核發合法 key NV-123456-69D4F3D0 → Pro activated. | runlog（未上卡） | runlog [FIX2]；license-server.mjs | n/a | CONFIRMED | node 重算 HMAC-SHA256("nv-server-secret-only-on-the-server","123456") 前8碼＝**69D4F3D0**，與 [FIX2] 相符；無卡片、未上稿，正確 |
| FIX3 | 舊偽造 key NV-123456-78F56FB4 → Invalid license key. | fix-run.output；fxr2 | runlog [FIX3] | n/a | CONFIRMED | 卡片 output 恰為「Invalid license key.」；ran_on 2026-10-16、tool_version .NET SDK 10.0.400 均在；node 重算舊 client 密鑰 HMAC 前8碼＝**78F56FB4**（與偽造 key 相符） |
| 誠實性 | client 無簽章密鑰、密鑰只在伺服器 | NoteVault-fixed.cs；license-server.mjs | 原始碼 | n/a | CONFIRMED | fixed.cs 只有 VerifyUrl(NV_LICENSE_URL / 127.0.0.1)；SigningSecret 僅存在 license-server.mjs 的 SERVER_SECRET |
| fix-code 卡忠實度 | PostAsJsonAsync(VerifyUrl, {key})、回傳 approved | fix-code.data.code | NoteVault-fixed.cs 行28-40 | n/a | CONFIRMED | 卡片精簡但忠實呈現 fixed.cs（PostAsJsonAsync 到 VerifyUrl、讀 Reply、回傳 approved），無杜撰 |
| 不過度宣稱 | 不聲稱伺服器「偵測出假 key」 | fxr3；runlog [FIX3] 註 | — | n/a | CONFIRMED | fxr3「因為伺服器的密鑰,攻擊者倒不出來,也就算不出合法的金鑰」＝不同密鑰、拿不到就算不出；未暗示伺服器以其他方式辨識偽造，誠實 |

說明：Demo 之所以成立，是伺服器用了 client 從未持有的密鑰（nv-server-secret-only-on-the-server）。舊偽造 key（78F56FB4）是用外洩的舊 client 密鑰（nv-test-secret-7f3a9c）算的；伺服器改用別把密鑰，對 123456 的正解是 69D4F3D0，兩者不同故被拒。腳本把拒絕原因正確歸於「不同密鑰、無法重算」，沒有任何卡片／旁白暗示伺服器「驗出假貨」或有其他偵測。

## C. round 1 確認項之隨機三分之一（複查）

| # | 主張 | 出處 | 來源 | HTTP | 裁決 | 比對 |
| --- | --- | --- | --- | --- | --- | --- |
| c05 | 分析在本機跑、不上傳；DISCLAIMER 限自有／授權 | install l00v；outro | README FAQ 行302-305、Disclaimer 行360-368 | 200 | CONFIRMED | 「REA analyzes targets locally」、「analysis of software you own or are authorized to examine」 |
| c06 | `npx rea-agents setup`，支援 Claude Code/Codex/Cursor/Gemini CLI | install.command/output；l00s-l00t | README Quick start 行82-96 | 200 | CONFIRMED | 卡片 output 與 README「Choose your agents, review the proposed changes, and approve」、「Supports Claude Code, Codex, Cursor, Gemini CLI ...」相符 |
| c11 | inspect-managed-members 抽出 23 字串常數，三秘密全中 | strings-out；l00x-l00z | runlog [B3] | n/a | CONFIRMED | [B3]「literal count: 23」+ 三秘密；卡片為其節錄 |
| c17/c18 | 三種繞過在混淆版照樣成功；因判斷在用戶端 | bypass-table；l01m-l01q | runlog [B6][B7] | n/a | CONFIRMED | [B6] bin-obf「Pro activated.」、[B7] letmein→解鎖、EDU→NT$90；三列成功/成功相符 |
| c22 | REA 自述限制「server-side behavior may remain unknown」 | boundary；l021-l023 | runlog [W1] | n/a | CONFIRMED | [W1] limitations 一字相符 |

## 摘要

- 重查主張：14 筆（A 四、B 六、C 五，c18 跨 A/C 計一）；確認 14、改動 0、找不到 0。
- 今日 REA 星數：`gh api repos/morluto/rea` 2026-10-16 讀到 **276,543 星 / 69,688 fork**（round 1 為 276,024 / 69,538）；仍進位為 28 萬，旁白「二十八萬」與卡片「約 28 萬」成立。同日 ~500 星漂移非 material，依 Round 2 規則不改精確值；卡片 note 標 276,024、claims c02 亦同，皆為同日有效快照，錄製日仍須重核。
- 修正版實跑誠實比對 runlog：全部相符。FIX1 l026「只剩一個網址」＝[FIX1] 含 secret:false；FIX2 合法 key 69D4F3D0、FIX3 偽造 key 78F56FB4 皆由 node 本機 HMAC 重算驗出，與 runlog 完全一致；fix-run 卡片 output「Invalid license key.」逐字相符、ran_on/tool_version 齊備。
- 卡片 vs 原始碼：fix-code 卡忠實呈現 NoteVault-fixed.cs（PostAsJsonAsync→VerifyUrl）；client（fixed.cs）無任何簽章密鑰、只有端點網址，密鑰只存在 license-server.mjs。無過度宣稱——fxr3 正確地把偽造 key 失敗歸因於「伺服器用不同密鑰、攻擊者算不出」，沒有任何卡片或旁白暗示伺服器「偵測出假 key」。
- 折扣用語：六折／省四成對 NT$90÷NT$150 正確；three-bugs、bypass-table、claims c09、runlog [B3][B7] 四處一致。
- 疑似但未改：星數精確快照 276,024（同日已漂到 276,543），依 material 門檻不改；旁白 l01t「二十二萬個節點」對 229,492 為無條件捨去（round 1 已記、口語容忍內）；runlog.txt / RUNLOG.md 不可編輯，無待修項。
- 意見 vs brief：站主觀點（混淆只提高門檻、真正的鎖在伺服器）與 stance/outro/fxr3 一致，無衝突。
- Lint：借 node_modules junction 後 `node tools/video/cli.mjs lint --slug rea-reverse-engineering-protection` ＝ **0 errors, 0 warnings**（估 8.7 分、92 行），junction 已刪除。
- 第三輪：**不需要**。本輪事實變更 0 筆（0 < 3 門檻）；round 1 的「c24 重跑無證據」疑慮已由新增的 [FIX1-3] 實跑與本輪 HMAC 重算解除，fix-run 卡片與 runlog 逐項相符且無過度宣稱。所有主張皆已解決，腳本事實面已完整查核。
- 唯一會過期項：REA 星數與爆紅時間軸（c02/c03），錄製日仍須以 `gh api` 與 star-history 重核；c03（10-06/10-12/10-11 時間軸、「一週破十萬」）仍為第三方報導、維持「報導」標註，非本輪可由權威來源定案的事實。
