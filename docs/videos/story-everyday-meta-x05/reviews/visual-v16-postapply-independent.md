# X05 Meta｜v16 套用後獨立覆核

**PASS（僅限提示詞差異與零成本媒體橋接；主工作區仍 STOP）。** 以 v15 `video.json` SHA-256 `077a5a6b541cb9e5a181786b8ed2d3d00816263dc68a71db625a1a0c0520b12a` 對照 v16 `a412c6b2e9a78f8eda90238336d7ccb87521dff8f87d8ae31842b508bce0b40d`，逐場景深比，只有九個提案 ID 的 `shot.data.prompt` 改動，且九段文字均與[獨立通過的提案](visual-v16-proposal-independent.md)綁定的 SHA-256 `dd964048b45e7a8341c421b11ccc497a50d23d0afb7507a6b75f2a1bfe383fb7` 逐字相同。`drafts/lines.tsv` 的 9/9 變更只在 `visual` 欄；旁白、來源、章節、句 ID、數字卡、場景順序、look 與 `shorts.json` 未改。Shorts SHA-256 仍為 `52e2812e2bbf409b3edab3e935dcf65f3768e79b0e9c0522a898e0b9d024dfd2`。

獨立比對 v15 歸檔 manifest SHA-256 `f4092657d38f3394989a2c09977bd7e80d9104d61d5fe26011893cd3e9d28130` 與 v16 現行 manifest SHA-256 `6472a5881826813a139f98f4a6b3ad5c89a6381d161a79bc9211f1639258b02f`：24/24 未改提示詞的入選記錄完全一致，實際圖檔 SHA 逐張匹配；九個改稿鏡頭已全從現行選圖撤下，舊圖與審查證據仍歸檔。總帳 SHA-256 `b33ae0b1b4bd753be1a9d6e872259a3b7a0e8651d73f4e4962b706b9492d42bb` 與歸檔位元組相同，仍 US$0.9485／71 圖／70 評審，未新增費用。主工作區 `STOP` 仍在。

目前僅 24/64 插畫鏡頭暫可用，九個新提示詞需要重新出圖及人工原尺寸審片，其餘未試鏡頭也未完成。共享評審配額不足，**此覆核不解除 STOP、不核准付費出圖或成片發布**。
