# C20 Zippo v5r2 獨立來源／配鏡增量覆核（2026-10-24）

**結論：來源與配鏡增量 PASS；劇情盲讀另有 HOLD，本收據不能作稿件核准。** 本次只覆核 v5r1 到 v5r2 的改句及其配鏡，並確認機器檔與文字檔同步。兩份 v5r2 盲讀已另指出 `c200310–311`／`c200401–403` 的日期碼轉場仍有敘事繞路；若再改旁白或鏡頭，須重新按新雜湊查核，不能沿用此結論。

## 鎖定輸入

分支 `codex/c20-zippo-v5r2-20261024`，檢查時 HEAD `e3aed5ab1bb685c0ba5d71f8e2181193e19e568e`。下列 SHA-256 是**工作樹檔案**，包括尚未提交的 `c200401` 配鏡更正；不能單靠 HEAD 還原本次樣本。

| 檔案（皆位於 `docs/videos/story-everyday-zippo-c20/`） | SHA-256 |
| --- | --- |
| `script.md` | `957BDE8C23408E3D365CD717F43453CF659AF51483A5040B2CF0EB86E25969E0` |
| `script-source-notes.md` | `47F3ED51AFD87D6A7293A20F105129D66FFD18D57CA8D605C6A08ABBAA6AD417` |
| `visual-plan.md` | `65549FC45A2B78EBEA363C09017CB3BF232B4B8E75FF05A2FC8CAF2506F0127D` |
| `visual-plan.json` | `5B63A76FDCBE43892F1438DCB981DB85238EB3F76B07D3993B027D65C8D868C8` |
| `reviews/narration-v5r2-only.txt` | `2E0397328F8D29439437C9C6A38A742EA71CAB8F98B7A61A858035FB561E2F4C` |

逐 ID 解析五份資料：劇本、來源註、畫面 MD、畫面 JSON、純旁白投影各 **59** 筆，ID 唯一且同序；來源欄、旁白、畫面文字與 `image`／`card` 類型均逐筆相等。配鏡為 **52** 張插圖、**7** 張字卡。`c200514` 已從五份資料一致移除。此為內容相等檢查，不以筆數代替來源判斷。

## 來源與配鏡判斷

| ID | 結果與可查界線 |
| --- | --- |
| `c200310–311` | **PASS**。[US 2,032,695 原始專利](https://patentimages.storage.googleapis.com/c6/09/ea/1d1b14be9be79c/US2032695.pdf)只能證當年內外套合及鉸鏈構造；[Zippo 日期碼頁](https://kb.zippo.com/zippo-lighter/date-codes)才支持後來的品質管制與退修批次追查。旁白明說專利不能證明後世維修，日期碼不替個件診斷。空白技術紙、抽象無字底部刻痕和陰影中的鉸鏈沒有暗示真專利圖或已知故障。 |
| `c200401–403` | **PASS**。[日期碼頁](https://kb.zippo.com/zippo-lighter/date-codes)把日期碼起點放在 1950 年代中期；較早盒底仍可能有品牌／專利標記。`c200401` 更正後只說早期**無日期碼**，沒有說盒底完全無標記；JSON 與 MD 一致。`c200402` 字卡限於品質管制，`c200403` 把批次線索與個件診斷分開；抽象刻痕、空白診斷紙均無虛構結論。 |
| `c200404–407` | **PASS**。[專利原件](https://patentimages.storage.googleapis.com/c6/09/ea/1d1b14be9be79c/US2032695.pdf)支持殼與內件可分；[美國鉸鏈頁](https://kb.zippo.com/zippo-lighter/hinge-broke)、[美國外觀頁](https://kb.zippo.com/zippo-lighter/worn-deco)、[英國維修頁](https://www.zippo.co.uk/pages/zippo-repairs-windproof-lighter)支持鉸鏈、外觀及內膽走向不同。旁白是分類／提問，未替示意個案下診斷。配鏡讓三處可辨，沒有修好、換件或退回原件的結果。 |
| `c200408–409`、`c200501` | **PASS**。英國[防風款維修頁](https://www.zippo.co.uk/pages/zippo-repairs-windproof-lighter)明列只修外殼時不寄內膽；美國[保固頁](https://kb.zippo.com/warranty-repair)及鉸鏈／外觀頁是美國現行界線。旁白明分市場；兩張分置空白服務頁、未寄出的空白袋及分離機件沒有拼成全球規則。`c200501` 字卡標示英國站。 |
| `c200515` | **PASS**。[Double Arc 內膽 FAQ](https://kb.zippo.com/arc-repair-faqs-and-guidance)支持可充電內膽另有兩年保固窗；[傳統防風款保固頁](https://kb.zippo.com/warranty-repair)不足以推出新內膽自動沿用終身承諾。旁白只提出問題，畫面仍將兩件分離，沒有顯示安裝、電弧或保固結果。 |
| 刪除的 `c200514` | **PASS**。英國特定寄件要求不再成為旁白段落，也無殘留寄件路線圖；不把英國流程移植到其他市場。 |

**範圍與後續：** 這是已鎖定 v5r2 的來源／配鏡收據，不是盲讀。`c200310–311`／`c200401–403` 的兩份獨立盲讀 HOLD 仍有效；敘事修改後，應重生純旁白投影、更新雜湊並重新做來源／配鏡及盲讀，不得把本次 PASS 延用到新稿。
