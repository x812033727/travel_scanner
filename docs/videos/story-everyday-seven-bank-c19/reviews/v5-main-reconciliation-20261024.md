# C19｜整合分支恢復作者 v5 的精確版本

2026-10-24 核對整合後的 `origin/main`，發現四份現行稿件仍是作者 v3；作者草稿 [#1742](https://github.com/x812033727/travel_scanner/pull/1742) 的最終提交 `83415c48249250c3cff6e302c1d7a79514377610` 已到 v5。整合分支從該提交**只恢復下列四檔原始位元組**；沒有把 v3 舊稿送配音，也沒有代改作者說法。

| 檔案 | 恢復後 SHA-256 |
| --- | --- |
| `script.md` | `998DDE68704BC3BDCBDCD1EFC1B0F970754BC1820471DC4B2130CE526EB4B9C1` |
| `script-source-notes.md` | `7F685F49528F499058DEBEA16ECAF16BA53B0FE86BDA5A411FFCF6BFF19F54E0` |
| `visual-plan.md` | `BD8A1066C037CF2B304E430E7D25A54A24A197E5979EE94E98C66D73DAD5D07B` |
| `visual-plan.json` | `7D4E2479B22F937F838C554748E22EADC6371DAB87420F020E3C3B3699216332` |

機械核對：79 句劇本與 79 筆 JSON 的 ID、旁白、來源欄逐項相同；66 鏡 `shot`、13 張後製 `card`。只讀旁白投影 `narration-v5-only.txt` 的 SHA-256 是 `67F21DC1485641F2E9D9FC6673F0952ECF80DD4919084490531EA69B73BFEA4E`。

獨立全篇來源／配鏡收據 `independent-v5-source-visual.md` 對同一劇本與來源雜湊判**旁白 79/79 PASS**，當時畫面 72/79 PASS、七鏡 HOLD；後續 `independent-v5-visual-delta.md` 對本次恢復的精確畫面雜湊判七鏡 7/7 PASS，文字層面的配鏡累計 79/79 PASS。這兩份收據不驗證實際圖片。

兩位新的只讀 v5 旁白盲讀各自判 **HOLD**，細項見 `narration-v5-blind-reader-a-20261024.md`、`narration-v5-blind-reader-b-20261024.md`。因此 v5 是**已恢復且來源／文字分鏡查核通過的作者版本，尚未通過故事盲讀及站主劇本核准**。需修稿並重核受影響的來源、分鏡與故事後，才可進入配音。C19 沒有整支付費上限核准或單集可歸因的預算帳戶；不得付費產圖／配音。實際正文配音至少 480 秒、插圖畫面時間至少 70%、最終成片與繁中字幕均尚未驗證。
