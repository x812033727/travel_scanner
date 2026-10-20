# S32 R3 史料、畫面與精確差分覆核

2026-10-20 UTC；唯讀。**PASS，三項改動無新的硬性來源或畫面錯誤。**從 git commit `679b1267` 取回舊版並核 exact hash 後，比對現行檔；無 repo 編輯、站台或付費呼叫。

| 檔案 | 舊版 SHA-256 | R3 SHA-256 |
| --- | --- | --- |
| `video.json` | `a4792ee4ebeed2b4e53e02cbaa7dc64cc0309310b956234abf3eb9f1e0bc338d` | `1e85570c510b1f14a69f0c1f7791decffc9356622071d157eef1efcbd71f251d` |
| `script.md` | `33668db15d862341bc16585f0f00f6f54d7c8ab7c55ed18074f269f444ce77c7` | `d1c91eb102319d8ec78a92e1faa8c8b3f3596e9ba8132815b2d26212b45a6731` |
| `claims.md` | `9fb2047617fe2605fbb65b768420a528d465b4e49837e3a8a9977263b558ed3b` | `9532776025ac622a31a2ba033f8198eff1be230fcc757445f0f6010ab39ce53b` |
| `brief.md` | `a880aeedf4466487a93858355ed96add1beae9af281c13a064d8ab3a6c13ecd3` | `8445f3277c38e8712cde24481445e1e9f0e8a199c096c220c55d164d190eab82` |

固定原文重新核對：P1 Yule–Cordier 卷一 SHA-256 `db5fe3122057a37615ccda2813d1edee2525046177b9ce885072a2c669a893e0`；Y93《元史》卷九十三 SHA-256 `ad3da9fd1a80ca80add2f5536135fc0729cc6a1d85cda1ce3847dba57c68ba6f`。

- **第一章標題**「牢房裡有人記下大汗的樹皮錢」：P1 序言 L11963–11972 是 1298 年熱那亞囚居由魯斯蒂謙記錄見聞的**書內自述**；第 24 章 L32843–32846 寫樹皮製成紙狀貨幣。標題可作這本書的敘事濃縮，不能擴寫成紙幣實物曾在牢房。mp001 圖仍是旅人、空白羊皮紙與石牢，沒有畫紙鈔原物。
- **mp048**：P1 L32918–32920 明說舊紙鈔按面值付 `three per cent` 換新；Y93 L476–479 的工墨是三十文、減二十文、又增回。新句「不能直接當成同一費率」正確，不自行設定官史的每張或每面值計費單位。圖仍是現代研究者分開兩張不同刻度的空白算表，沒有畫等號。
- **mp077**：P1 尤爾譯法說明 L11777–11794 說以 Pauthier 為底，補 G 本，將他認為有真實性理由的 **Ramusio 版特有內容**放入方括號；其他特有但不宜置入正文者放註解。P1 L9389–9393 與 L11760 也明稱 `Ramusio's Italian`。R3 明名「拉穆西奧」，以「自認可信」標示尤爾的判斷，與 mp075–079 上下文相接。mp077 原有字卡「方括號／選入 Ramusio 版特有文字」不變；仍須保持這是尤爾英譯校注本的版本安排，不能倒說各早本共有。

結構化逐 leaf 比較：84 個場景 ID／順序相同，`video.json` **恰有 3 個 leaf 變更**：`scenes[0].chapter`、`scenes[47].lines[0].text`、`scenes[76].lines[0].text`。其餘 84 場的旁白、所有 prompt、卡片、來源與 `look`、配樂均未變。`claims.md` 只改 mp048、mp077 的旁白字串，兩列來源連結與備註未變；`script.md` 除標題與兩句外僅自動 narrative/speech footer hashes 更新。`brief.md` 只同步章名、估時與章節時間；`research.md` 仍為 SHA `339de43e87ac8c639fe60aa474271a92e0ffe8eaf404268f7775417ad549ff28`。現行 `lint --slug curio-s32 --json`：**0 errors、0 warnings**，總旁白預估 9.6094 分鐘，並非實測 TTS 正文長度。
