# X08 Target Canada｜REDcard 段落獨立來源複查

**PASS（2026-10-20，限本版史實與來源邊界）。** 本收據接續 [完整逐句審查](source-audit.md)與[前次單句複查](source-audit-v5.md)，直接讀取 Target [FY2013 Form 10-K 原件](https://www.sec.gov/Archives/edgar/data/27419/000002741914000014/tgt-20140201x10k.htm) 的 U.S. Segment／Canadian Segment `REDcard Penetration`、Canadian Segment `Sales` 及 Canada 風險段落。該原始 HTML SHA-256 為 `dbbdbee947bf108d0b4026a0ca4923a0df7a655cfbb27ee57b074e84f6b36225`，與既有來源筆記相符。

| 鎖定檔 | SHA-256 |
| --- | --- |
| `video.json` | `7919666e43bc77f6e27d3c4d566c46bd6b77f17e675547d9e62f6ce6febcb0b8` |
| `shorts.json` | `440ceee9649b30af2bd64ff1205bf38bff47d0be381b1b544cccff4601e2d543` |

## 新增十句與一張原生卡

| 行 ID | 原件對照及判定 |
| --- | --- |
| `x0803a01` | PASS。10-K 美國與加拿大段落均列 REDcard 5% 優惠；「顧客會跟著用嗎」是疑問，沒有宣稱加拿大實際使用成效。 |
| `x0803a02` | PASS。美國段落明載 REDcard 於 `virtually all purchases` 有 5% 折扣；「九五折」換算正確。 |
| `x0803a03` | PASS。加拿大段落明載 Royal Bank of Canada 提供 Target RBC MasterCard 聯名信用卡，另有 proprietary Target Debit Card。 |
| `x0803a04` | PASS。加拿大段落明載當地 REDcard 使用同樣 5% 折扣；「同樣」指前句介紹的卡，不是所有付款卡。 |
| `x0803a05` | PASS，**限 Target 自述**。美國部門段落原文說公司追蹤 `percentage of sales that are paid for using REDcards`，因其**內部分析**認為 REDcard 的一部分增量購買亦增加 Target 銷售。口播「公司認為」保留歸屬，沒有聲稱加拿大用卡已被獨立證明增加銷售；該分析列在美國段落，不能外推為加拿大特定因果估計。 |
| `x0803a06` | PASS。10-K 的 FY2013 `Total store REDcard Penetration` 美國 **19.3%**、加拿大 **2.9%**；「接近兩成」精確且與原生卡一致。這是**以 REDcard 付帳的銷售額比例**，不是持卡率、顧客回購率或同店成長。 |
| `x0803a07` | PASS。加拿大門市 FY2013 才分批開張；美國門店已經營多年。旁白明言兩地比率不能單獨解釋加拿大虧損，沒有把成熟度差異當唯一因果。 |
| `x0803a08` | PASS。疑問句，並未將卡片占比當顧客留存的已驗證指標。 |
| `x0803a09` | PASS。10-K Canadian Segment `Sales` 原文為 `124 ... stores`、`14.2 million total retail square feet`；口播的一千四百二十萬平方英呎換算正確，不把 189 處 Zellers 租賃權誤作開店數。 |
| `x0803a10` | PASS。原件 Canada 風險段說改善銷售依賴商品組合、庫存管理與市場接受；口播是留住顧客的條件與承接疑問，不宣稱全部門市曾空架或 REDcard 低占比造成虧損。 |

原生卡 `x08-b03-a06` 的 `2.9%`、`19.3%`、FY2013 財年、加拿大新店網／美國既有店網標籤與 `U.S.／Canadian Segment` 來源皆 **PASS**。兩國分母分別是各自銷售額，卡上已提示開業階段不同；不可把差額讀成同店銷售、持卡人比例、回頭客比例或單獨的虧損原因。新增 loop `x0803a01` → `x0803a06` 提問用卡反應並以使用占比回應，不多加因果結論。

## 變更範圍與保留邊界

將目前 `video.json` 與分支原先鎖定檔逐鍵比較：僅新增十個 `x08-b03-a01`–`a10` 場景／`x0803a01`–`a10` 行及一個 loop；**既有 134 句、128 場、14 張卡沒有修改或移除**。舊 `x080316`–`x080318` 仍是原句與原場，能沿用既有查核及 TTS 句 ID。全片現為 144 句、138 場、15 張卡。長片標題、說明、來源連結、縮圖設定和其他頂層欄位均未變；`shorts.json` SHA 完全相同。新增插畫 prompt 是匿名空白付款卡、購物及店面概念畫面，沒有商標、可讀文字、真實人物或聲稱重現加拿大門店。

**未發現來源阻礙。** 此 PASS 不涵蓋新十句實際 TTS 秒數、圖片生成及評審、成片或 US$25 成本關卡；任何上述兩份鎖定檔的內容變更仍須換 SHA 重新審查。
