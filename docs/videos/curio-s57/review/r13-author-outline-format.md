# S57 R13｜A／B 大綱卡格式修復：作者回條

2026-10-22 UTC。這是供獨立覆核的**作者候選**。R12 網站 outline 卡因 `outlineOptions` 讀不到 Markdown 表格，只顯示 0 個選項，仍待有效 A／B 卡及站主決定。本輪只改 `brief.md` 的 `## A／B 案` 區塊；未送網站、未改本地核准、未重跑 Jev 政策判斷，也未產生任何付費媒體。

## 精確可逆差分

`brief.md` 原檔 9,642 bytes，SHA-256 `0c8284f9bbceb9e751784086a1db35a8c072c9b80f4b75729a2bca15df4ec4bd`；新檔 9,838 bytes，SHA-256 `6b0cd77870b7a1e97efb097e6ef64f0081d517dfd19c9741e8cc29a5f4629311`。只替換下列單一連續區塊，前後位元組相同；把新增區塊換回刪除區塊，即精確還原 R12 原檔 SHA。舊區塊 SHA `ece8e83b6974dcd8e1ce0421b11856305d76cf578310bdace7c67e3d716de629`，新區塊 SHA `cbacd5c07d305c06ffcb2333bf43e45fea9fc085d4e757b78d9b5be21c4f6457`。

```diff
 ## A／B 案

-| 案 | 主線與取捨 |
-| --- | --- |
-| **A 推薦：找到人之後，還有第二個選擇** | 從李文斯頓在烏吉吉缺物資開場，沿相遇、勸回家、短暫同行、補給重到手與兩人分路走到答案。S 與 L 兩個視角都能逐段查；節拍比單純還原名句更有轉折。 |
-| B：名句到底說了沒有？ | 以「Dr. Livingstone, I presume?」查名言真偽。S 寫了、L 沒記，缺錄音或同場獨立逐字證詞；只能得到「史丹利出版書如此寫」，無法將十分鐘問題徹底回答。故不用 B。 |
+### 選項 A：找到人之後，還有第二個選擇（推薦）
+一行說明：從李文斯頓在烏吉吉缺物資開場，沿相遇、勸回家、短暫同行、補給重到手與兩人分路走到答案。S 與 L 兩個視角都能逐段查；節拍比單純還原名句更有轉折。
+開場鉤子：「一本五道封印的日記將隨史丹利往海岸走，日記主人會同行嗎？」
+
+### 選項 B：名句到底說了沒有？
+一行說明：以「Dr. Livingstone, I presume?」查名言真偽。S 寫了、L 沒記，缺錄音或同場獨立逐字證詞；只能得到「史丹利出版書如此寫」，無法將十分鐘問題徹底回答。故不用 B。
+開場鉤子：「那句著名英文招呼，真有兩名當事人都記下來嗎？」
```

A／B 一行說明與舊表格**逐字相同**。A 鉤子取自既有八章節拍的「一本五道封印的日記」與「日記主人要選哪條路」；B 鉤子只改寫舊 B 案的名句來源疑問，不新增歷史主張。A 仍明確推薦；B 仍明確不採用。兩案的單方／雙方來源界線、答案與 159 句口播皆未改。

## 機器核對

- 倉庫 `outlineOptions(brief)` 現回傳**恰好兩項** `A`、`B`，兩者 `title`、`summary`、`hook` 都非空；A 解析後標題為「找到人之後，還有第二個選擇」，推薦標記按解析器規則剝除。
- 五份創作檔對 R12：`research.md` `9663d4a0ea66b1fef3c6e3a0550b8b08cf169a68b1736ad6005d6408ac2cd667` 不變；`brief.md` 如上變更；`claims.md` `2c06451d321b3b662af365463452b2fcc989babd0007cb010fdb4bc08579f556` 不變；`video.json` `a01c5dd256e81873e4796a27532e615d7ae328a04190c2d0abcd0b652d0d168d` 不變；`script.md` `1b6252886bff6b17a03cd82da67f95cf51aa3c2a1a4ea606d005b9d0e2bb7474` 不變。
- `narrativeHash(video.json)` `dcadd0471c15f9a2`、`speechHash(video.json,null)` `fe54a277a8ce6265`；159 景、159 句。`policyRequest({doc,brief})` 與 R12 保存的 [請求全文](r12-media-readiness/policy-request-body.json)逐欄完全相同，該 JSON 檔 SHA 仍是 `44293cfd8731d0f15ab0d7ecdf67c5d90ddf450d33a4020752964ba0298d1206`，因此這次沒有新政策內容需要提交。
- `VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s57 --json`：0 errors、0 warnings、159 句、估 13.7972 分鐘。`npm run check:tasks`：exit 0，validated 2413 task files；既有其他任務的長期認領及範圍重疊警告仍在。

R12 [首輪機器音檢](r12-technical-audio/first-pass-triage-20261022.md)已結束：159／159 有轉寫，43 句標記，音訊 **HOLD**，尚待核聽，網站 audio 卡沒有提交。舊 `brief.md` SHA 的本地推薦 A 紀錄因本次改檔而失效；獨立審核此差分及來源界線前，不重綁本地 outline 決定，也不重送網站 outline 卡。網站 script 卡亦仍待站主決定，沒有以本回條代替任何站主親審。
