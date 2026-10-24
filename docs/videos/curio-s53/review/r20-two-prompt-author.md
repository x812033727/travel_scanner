# S53 R20｜第二章兩景提示詞窄修

2026-10-22 UTC。**作者候選，待非作者按精確檔案再作史料與書面畫面紙審；本輪沒有付費試圖。**R19 [八景原圖停批](r19-next-chapter-eight-native-stop.md)留下六張人工 KEEP，`s53010` 原圖 REJECT、`s53018` 供應商 `input new_sensitive` 且無圖。R20 只改這兩景的 `data.prompt` 與 `claims.md` 同列畫面說明；全 126 句旁白、`script.md`、其他場景、章界及運鏡保持原字。

| 景 | R19 原圖／供應商問題 | R20 書面修復與來源界線 |
| --- | --- | --- |
| `s53010` | 1280×720 原圖出現現代汽車、電街燈及偏一般漫畫比例的成人；機器 9/10 FAIL，人工 REJECT。 | 改近景匿名成年住戶，灰鬢、面紋、圓潤緊湊的插畫比例；畫面由住戶與裁近的 1906 年木灰牆佔滿，只在屋頂後方見火煙，不開長街透視，不畫車、街燈、招牌或現代物。這是對[1913 調查 L1438–1465](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L1438-L1465)所述地震與大火的匿名概念示意，非某名目擊者或一棟可查房屋。 |
| `s53018` | 原提示詞的英文 `South Park` 可能觸發 `input new_sensitive`；原因未經供應商確認，沒有原圖可判。 | 書面改用 `small San Francisco public relief park in summer 1906` 通稱，讓近排帆布帳棚與一條窄裸地顯示空間不足；成年工作者只看間距，無假地圖、完工屋或可讀地名。旁白仍明確說「南公園」，主張仍錨定同一[1913 調查 L4848–4870](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L4848-L4870)。 |

[逐字可逆結構差分](r20-two-prompt-structured-diff.json)保存 R19→R20 的兩個 scene prompt 與兩個完整 claims 行之舊／新內容，反向回填兩檔皆可位元組還原 R19。`video.json` SHA-256 `62254351988dae8424e0d94bb136a6b7171e5d991f2c9962508af03fc7248c3a` → **`f868ce55f98f7868a8052098d0f6439344585df9e0fa1d0cb32eb0ddbbac21dd`**；`claims.md` `b5be9bbbf8c78cc87c32efcc0964afea1cb689a225b1a216184db750623b5f84` → **`81f03c571693ff7b28e9898f64dcbb64e9442ec66bde2597c6dfcd7874b7ef1c`**。`script.md` 保持 `64ffcd8c0e89c4596a7fd08d41bd74f8a16f55fbc9acc2f41d7f9b914ea300fc`；`research.md`、`brief.md` 也未改。CLI lint exit **0，0 errors／0 warnings，126 lines**；輸出與 exit 檔同目錄。

私人 manifest SHA-256 仍 `eafb17ba8426f1c6e79c263bed1bbfcb73f896bc8150b54cff3033e7cf9f0f66`，帳本 SHA-256 仍 `e4761e22531131c77d9dbae201af16c822afad5c6bdf58d013395b16e6f68c69`；前首章八張與 R19 本章六張 KEEP 的 request key／選圖未被本輪更動。帳本 **US$0.4050／31 image／30 judge／0 預約**，低於整集 US$4.78 上限；`STOP` 在位。先由另一人對這兩景按 R20 新雜湊紙審，再在上限與 STOP 下各試最多一次、直接驗 1280×720 原圖。R19 的 `s53010` 舊退圖和 `s53018` 無圖條目不可算已收。完整第二章、網站卡、人耳旁白與成片仍待。
