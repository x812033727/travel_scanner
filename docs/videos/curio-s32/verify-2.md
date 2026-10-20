# S32 mp061 單句來源差分覆核

2026-10-20 UTC，唯讀。封版 SHA-256：`script.md` `33668db15d862341bc16585f0f00f6f54d7c8ab7c55ed18074f269f444ce77c7`；`video.json` `a4792ee4ebeed2b4e53e02cbaa7dc64cc0309310b956234abf3eb9f1e0bc338d`；`claims.md` `9fb2047617fe2605fbb65b768420a528d465b4e49837e3a8a9977263b558ed3b`。舊版從 git commit `335f28d3` 逐檔唯讀取回，hash 分別為 `ed6b4c49807c18b3b80eeaac5000df27c45f36221798eec3943461de57de71bf`、`e30355ea28b111edaee5973c18e6257cee3252f577c1f76b54d9ff9c2215bce3`、`b1948666053e369de0fb1c7800013385cfb3aaa39959fa829ae337766a8b66b4`，均與先前獨審版相符。

**結論：PASS，無硬性史料或時代誤導。** mp061 新句「卷二的杭州段，大汗的收入一筆筆列出；馬可的名字也在後面出現。」與固定 P2 Yule–Cordier 卷二（commit `95709397a514799b8bb9262bd918f19be61b009c`，原文 SHA-256 `4dcfd52725f9d6ab671c18edacb43fbbb8f206075fe2be24b6617ec271067104`）吻合：第 78 章 L11171–11205 依次談鹽、貨稅及幾類收入，L11207 明出現 `Messer Marco Polo`。此句只說名字在**這份英譯校注本的敘述中**出現，沒有宣稱馬可親自查稅或史實已證。後續 mp069–072 另交代 Pauthier 所見「受派」與 G 本「聽聞帳目」的版本差異；編者註在 L11223–11226 支持這個界線。

小心「一筆筆」不應在後續剪輯／字卡擴寫成**完整逐項帳本**：原文 L11195–11205 明說不逐件列盡，只挑幾類和總數。mp061 現行示意圖只畫元代江南行商與市集，沒有把馬可畫進官府、捏造他親手核帳，也無跨時代道具。`claims.md`、`video.json`、`script.md` 的 mp061 文字相同。未改 repo、未呼叫付費或站台寫入。

結構化 leaf 比較：兩版 `video.json` 84 場景的 ID 順序相同，**唯一變動**為 `scenes[60].lines[0].text`（mp061）；其餘旁白、來源表、所有 prompt、卡片與欄位均逐 leaf 相同。`claims.md` 僅第 67 行 mp061 的旁白字串不同，該列三個來源連結及備註未變，其餘列逐行相同。`script.md` 除 mp061 旁白外僅自動產生的 narrative／speech footer hashes 更新，沒有其他話語或場景改動。現版 `lint --slug curio-s32 --json` 為 **0 errors、0 warnings**。
