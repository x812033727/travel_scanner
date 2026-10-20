# X13 Spotify｜獨立一手來源查核（企劃階段）

- Reviewer: `codex-x13-source-auditor`，與企劃撰寫者不同代理。
- Original sources checked at 2026-10-20 20:03 UTC; final denominator/context recheck at 20:06 UTC。先前綁定 `83f8e178…`／`8fa02ff3…` 的 PASS **已失效**：它漏看 S5 的 €32m 總額與 €11m 解釋項之別，不能沿用。
- **Current scope binding:** `source-matrix.md` SHA-256 `ebd4620858b933c93925ee14d9758c5e5e6f25e402a4ad71ae9d89c3d253f29b`；`treatment.md` SHA-256 `918d9c13fa09b1e06de8b68718c18a5d9f2e12ecc8f8b49c49c49341fc181f24`；`shorts-hooks.md` SHA-256 `1d3875a003ea9f0610af46eb0c75000c37723e029f955905c489833d5589a7bf`。上述任一位元改變即不再套用本收據。
- Verdict: **PASS（本版企劃）：S5、S7 的業務總額與解釋項已分清；其餘 S1–S8 的關鍵事實、期間及分母再查無誤，可進下一階段撰稿。** 這不是可配音劇本或正式製作批准；後續逐句事實查核與兩名盲評仍需重新執行。

我獨立從下列八個 EDGAR URL 以正常 HTTPS／既有代理重新下載原始 HTML，HTTP 均為 200，下載位元組與企劃表的大小／SHA-256 全部一致。括號中是本次重新計算的 SHA-256 前 12 碼；完整值見 `source-matrix.md`：

| ID | SEC 原件 | 再查結果 |
| --- | --- | --- |
| S1 | [2019 Q1 6-K](https://www.sec.gov/Archives/edgar/data/1639920/000156459019013731/ck0001639920-6k_20190429.htm) | `6ece16f8b879`：Anchor 2019-02-14、€136m 對價，其中 €125m 現金／€11m 股份獎酬；Gimlet 2019-02-15、€172m，其中 €170m 現金／€2m 股份獎酬，均與表一致。Anchor 是 **create and distribute** 工具。 |
| S2 | [2020 Q1 6-K](https://www.sec.gov/Archives/edgar/data/1639920/000156459020019718/ck0001639920-6k_20200429.htm) | `407258c428f8`：The Ringer 2020-03-06、對價公允價值 €170m，其中 €138m closing cash／€32m 遞延給付現值；商業化為管理層所述收購預期。 |
| S3 | [2023 Q2 6-K](https://www.sec.gov/Archives/edgar/data/1639920/000163992023000010/spot-20230630x6xk.htm) | `4b190d58d633`：報告確寫 podcast strategic realignment、rationalize content portfolio，因該次重整產生 €30m content-asset write-off。**未寫明是何種成本壓力造成重整決策。** |
| S4 | [2023-12-04 6-K](https://www.sec.gov/Archives/edgar/data/1639920/000114036123055913/ef20015890_6k.htm) | `b15e74c6d503`：約 17% 是 **company employee base**；矩陣的分母警示正確。 |
| S5 | [2024 Q2 6-K](https://www.sec.gov/Archives/edgar/data/1639920/000163992024000009/spot-20240630x6xk.htm) | `8fef7316f4be`：2024 Q2 **Ad-Supported cost of revenue 總額**同比減 €32m／7%；報告另以去年同季 €46m 重整費用、今年沒有重大可比費用，以及約 €11m「primarily related to」播客製作與人事成本的下降解釋變動，並有 €17m 較高版稅部分抵銷。€11m 不是總額，也不能全指定給播客成本。 |
| S6 | [2024 Q4 earnings 附件](https://www.sec.gov/Archives/edgar/data/1639920/000114036125002936/ef20042791_ex99-1.htm) | `5cadbcf2cb2`：公司原文是 first full year of **Operating Income** profitability，全年約 €1.4bn、Q4 €477m；矩陣分清季度與年度正確。 |
| S7 | [2025 Q2 6-K](https://www.sec.gov/Archives/edgar/data/1639920/000163992025000012/spot-20250630x6xk.htm) | `898488dec382`：2025 前播客內容成本列 Ad-Supported；Partner Program 會員影片播客體驗相關成本轉列 Premium。2025 Q2 **Ad-Supported cost of revenue 總額**同比減 €25m／6%，報告說其中 podcast costs 減 €21m；無法拆出實際節省與分類搬移各占多少。現版矩陣分清總額與解釋項。 |
| S8 | [2026 Q2 6-K](https://www.sec.gov/Archives/edgar/data/1639920/000162828026052543/spot-20260630x6xk.htm) | `13d15583c06d`：2026-06-30 MAU 777m、Premium Subscribers 300m；Q2 營業利益 €655m（比較欄 2025 Q2 €406m）。這些是不同分母／期間；矩陣正確。 |

**初審問題與作者修正**（本次 PASS 綁定上方新雜湊）：

1. 舊版 `treatment.md` 把播客成本寫成 2023 年重整的決策原因。新版只依時間順序寫重整與內容資產減損，沒有超出 S3。
2. 舊版 Short 1 稱 Anchor「只做發布工具」。新版改為「創作與發行工具」，符合 S1 的 create and distribute。
3. 舊版把 €11m 說成 **Ad-Supported 業務分類的 Q2 成本總變動**；這仍錯，且前一版 PASS 漏抓。最新版本寫總額 €32m，並把 €11m 正確列為報表解釋項，主因與播客製作／人事相關。正式旁白仍須維持這個分母。
4. 舊版開場畫一張「被劃掉的節目清單」。新版改為沒有特定節目名稱的內容資產減損卡，避免暗示 S3 沒列出的取消節目。

結論的因果護欄應保持：首次全年**營業**獲利是全公司結果，不能推出播客單獨獲利；收購理由是當時期待；2025 成本搬進 Premium 不等於全數實際省下。此次沒有付費生成或上架動作。
