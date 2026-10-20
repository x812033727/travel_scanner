# S50 R7｜三景一次提示詞修補凍結

2026-10-20 UTC。[原生圖獨立驗收](r7-pilot-first-independent.md)為 **0/3 KEEP**；依 [整集預算與試畫規則](r7-media-budget.md)，本輪僅替換 `fire001`, `fire013`, `fire096` 三個 `data.prompt`，各只允許再買一張。原生首輪圖、修邊版、manifest 及 ledger 已封存在私有 `review/r7-pilot-round1/`，不會以新圖覆寫而失去首輪證據。

三個新提示詞分別要求 1666 年倫敦木屋中**單一成年**匿名鄰居與窗外可見煙、舊石拱倫敦橋前**單一成年**搬運者拉車、**單一成年**麵包師指向房間鋪磚的地面。它們不指定起火者、當時目擊者或已證實的壁爐結構；維持 [R01/R02/R12](../research.md) 的證據層級。完整英文提示詞以精確版 `video.json` 為準，並已通過獨立驗收者的逐景修補提案；本收據不是新圖合格判決。

| 檔 | 重算 SHA-256 |
| --- | --- |
| `brief.md` | `bac9d05082626689833057f30718c0f9d6d798562460335c8bcb834216ed1a3b` |
| `research.md` | `27f9df563ab8376d2f6ee10837772821534515fd29b86b7e83e259eb56023a95` |
| `claims.md` | `4e07795ddf55b4b686431851664cb1c686333233417e378b87b9e96c1180bedc` |
| `script.md` | `5f9ae7f8b89b5f898c982dd51215c5d148901820bf715e10e6d43f8872ef782b` |
| `video.json` | `603dc5bbde9737dcce0cb2327cdb4db698bfd5fac7dba07e21e3bf86278a1cc1` |

劇本、來源表、口播、前述來源／敘事／政策／音檢綁定的文字沒有變。CLI lint 為 0 errors、1 片尾既有 warning；三景 `keyframes --takes 1 --dry-run` 報價約 US$0.04，開始前整集 ledger 已花 US$0.0405。三張新圖仍須逐張原生尺寸驗收，第二輪低於 2/3 即停止這套插圖方案。
