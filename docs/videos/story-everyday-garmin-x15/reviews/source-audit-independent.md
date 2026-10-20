# Garmin X15｜來源企劃包獨立審查

**PASS，僅限來源企劃包。** 審查綁定 `source-matrix.md` SHA-256 `05ae462f1172c642f4e182a3c3f532267cf2c1ed38f84e36c42e43b9b31074dd`、`treatment.md` `1294421928f567f4a75aff62ecae193a23a2a3bfa1bdc7432548c7525a7be697`、`shorts-hooks.md` `dc5b8d7bddefab04ad828d960a844f134730eed38dc6b0970580d1a11d9f8f2f`，不批准尚未寫出的逐句稿、媒體或 PR。

我在 2026-10-20 重新以 SEC EDGAR 的原始 URL 逐份 HTTP GET，不使用作者摘要作憑據。G1–G7 皆 HTTP 200，回應位元組數與矩陣所列 SHA-256 **逐份完全相符**。G1–G6 低於工人單頁 3,145,728 bytes 上限；G7 2023 10-K 為 3,683,117 bytes，保留 `reviewer_only`，不作口播唯一證據。

| 主張 | 原件核對 |
| --- | --- |
| 2006 全年總收入約 US$1.77bn、增 73%；auto/mobile 約 US$1.1bn、增 170% | G1 明列全年 Financial Highlights；與第四季的另一組百分比清楚區分。 |
| 2008 nüvi 產品線占公司收入約 64%；auto/mobile 事業逾 70%；手機導航當時**可能**放慢成長 | G2 同時列 2006／2007／2008 的 28%／52%／64%，風險段用 “could slow our growth”；沒有把事業與產品線當同一分子。 |
| 2008 全年 US$3,494.077m，auto/mobile US$2,538.411m；2010 全年相應為 US$2,689.911m／US$1,668.939m | G3、G4 的全年 segment table 單位皆千美元，第三欄為 Auto/Mobile；本包算得 2008 比重 **72.64897%**。G4 的 19% 是 2010 相對 **2009**，企劃沒有誤套在 2008→2010。 |
| 2011 風險措辭變為已使成長停滯；nüvi 約占 48%，auto/mobile 事業約 58%；Fitness +24%、Outdoor +14% | G5 原句 “has halted our growth”，並把部門與產品線分開；產品段列 Forerunner 610、910XT，不證明它們獨自造成部門成長。 |
| 2025 全年營收 US$7,245.519m，分散至五部門 | G6 全年表中的五項原始千美元金額相加恰為 7,245,519；本包占比 32.5%、28.3%、16.3%、13.6%、9.2% 均由原數額四捨五入。Fitness + Outdoor 精確比重為 **60.9%**，2025／2008 全年總收入名目美元比為 **2.07366**。 |

G7 顯示後來的 Consumer Automotive 個人導航機歸在 Outdoor 相關產品描述，而現行 Auto OEM 供應車廠系統；因此企劃沒有把 2008 auto/mobile 的 72.65% 與 2025 Auto OEM 的 9.2% 畫成連續同口徑下降。Treatment 和 Shorts 對手機、錶款及 2025 成績的因果限制正確：公司自己的風險說法不等於獨立量化手機貢獻，也不能推論某款手錶救活全公司。短片的 60.9% 是 Fitness + Outdoor **部門收入**，不是手錶單品收入。

下一步才是寫來源標記的逐句主稿與兩支可獨立觀看的 Shorts。成稿改動後須以新的 JSON 雜湊作逐句來源與敘事盲審；這張 PASS 只證明目前企劃的證據鏈成立。
