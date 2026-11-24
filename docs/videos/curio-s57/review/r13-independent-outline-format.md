# S57 R13｜A／B 大綱格式獨立覆核

2026-10-22 UTC。**PASS：僅准將推薦 A 案綁到新 `brief.md`，並重送網站 outline 卡。**這是格式與來源界線的獨立覆核，不是站主親審、音訊核准或成片驗收；本次沒有付費媒體。

我將 R13 `brief.md` 的 `## A／B 案` 區塊換回 PR #1637 的 R12 原區塊，還原的整檔 SHA-256 精確為 `0c8284f9bbceb9e751784086a1db35a8c072c9b80f4b75729a2bca15df4ec4bd`，與 R12 原檔逐位元組相等。現檔 SHA-256 為 `6b0cd77870b7a1e97efb097e6ef64f0081d517dfd19c9741e8cc29a5f4629311`；差分只在該連續區塊。舊表格經 `outlineOptions` 得 0 案；新格式恰得 A、B 兩案，標題、說明、鉤子均非空。兩案說明與舊表格逐字相同；A 仍為推薦、B 仍註明不採用。

A 新鉤子中的五道封印及日記託送，受 `research.md` P09 與 `claims.md` 的 `s57001`、`s57168` 約束，明確是 1872 年 3 月 14 日身後編刊日記所述，並未暗示日記主人隨行。B 新鉤子只問名句是否由兩名當事人共同記錄；`research.md` P04 明列史丹利書有此句、李文斯頓相遇段未記，不能推成現場逐字錄音。新增兩句是提問，未創造新史實或把單方來源升格。

`research.md`、`claims.md`、`video.json`、`script.md` 的整檔 SHA-256 依序仍為 `9663d4a0ea66b1fef3c6e3a0550b8b08cf169a68b1736ad6005d6408ac2cd667`、`2c06451d321b3b662af365463452b2fcc989babd0007cb010fdb4bc08579f556`、`a01c5dd256e81873e4796a27532e615d7ae328a04190c2d0abcd0b652d0d168d`、`1b6252886bff6b17a03cd82da67f95cf51aa3c2a1a4ea606d005b9d0e2bb7474`。現稿 `narrativeHash` 為 `dcadd0471c15f9a2`，`speechHash` 為 `fe54a277a8ce6265`。重新以現稿建立的 `policyRequest` 與 R12 保存的完整 JSON 逐欄相等；毋須再花費一次政策判斷。

R12 159／159 句已有機器轉寫但 43 句待處理，音訊維持 **HOLD**；網站 audio 卡未送。舊 outline 本地核准因 brief SHA 改變而失效。R12 當時網站舊卡為 `pending`，其選項數為 0，不能當作有效 A／B 決定；R13 後續拉回時網站已顯示該舊版曾獲准，但因內容雜湊過期而不適用於新版。使用者先前已委託採推薦決定，故允許本地透明記錄推薦 A 及重新提交有兩案的網站卡；不得聲稱站主已親自核准**新版**網站卡。

## R13 後續執行

獨立覆核 PASS 後，`approve --gate outline` 將本地推薦 A 決定重綁至 `brief.md` SHA `6b0cd77870b7…`，註記清楚寫明代理代記、網站仍待站主。`review-push --gate outline` 輸出 Jev 推薦 A（0.99），但因工作目錄沒有 `auto.json`，網站明示由站主決定；新卡狀態 **pending**，沒有宣稱自動核准。隨後 `review-pull --gate outline` 回覆舊卡「approved a version that has since changed」及新卡「waiting for the owner」（exit 3），正是新舊版分離的預期狀態。`lint --json` 為 0 errors／0 warnings、159 句。未送 audio 卡，未更動 43 句 HOLD 清單。
