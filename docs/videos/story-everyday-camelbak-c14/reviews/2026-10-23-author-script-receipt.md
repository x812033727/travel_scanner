# C14 CamelBak｜作者 v2 旁白／v3 視覺微修收據（非獨立 PASS）

- 日期：2026-10-23（台北時間）；作者：`codex-c14-script`。
- 去向：[draft PR #1695](https://github.com/x812033727/travel_scanner/pull/1695)。兩位獨立讀者對 v1 純旁白均判 **HOLD**，詳見 `blind-narration-v1-coordinator.md`。獨立 v2 審查對 61 句來源判 **PASS**，對 I01 字卡判 **HOLD**，詳見 `independent-v2-source-visual-delta-review.md`；本 v3 是作者僅修 I01 後製字卡與分鏡說明，**不是新版逐鏡文字 PASS、雙盲 PASS、站主劇本／分鏡採用或付費授權**。
- 沿用站主已採用的 [Treatment](../treatment.md) SHA-256 `078DC1D77C46EB49BB6F27F60535F22775781E5963783BDA7C1F7625B1A8700E`、[來源矩陣](../source-matrix.md) SHA-256 `F8CF68AA36264DF18CDBE6ECD698D4AF1F22E405DEAADA8ED275B7685050587E`；作者沒有改這兩份檔案。

## 目前 v3 視覺微修交付 SHA-256

| 檔案 | SHA-256 |
| --- | --- |
| [`script.md`](../script.md) | `6F52F13283B8B14941D40A0DBE19D299B8266824A33E22201EEB99C700B25119` |
| [`script-source-notes.md`](../script-source-notes.md) | `6627DC1CDAA301B80B30C087BF3DC746DA1F60032BB29C05EA2047C95F0C9EBD` |
| [`visual-plan.md`](../visual-plan.md) | `2BC2EF8407AE25206F28A2A165A97DAD21BC6D5A4008CF04D22A754BBC517130` |
| [`visual-plan.json`](../visual-plan.json) | `99505E762A954FDED2FE119B7B475649510F2329C3782B45130492AA4AADF039` |

v2 經獨立審查時的視覺 SHA（只作前版對照）：`visual-plan.md` `003F2377E74DE402C8F2FCE477A03EBCD4206E6B890585CDC2A230DF1325DC31`；`visual-plan.json` `23E7B36BC84C2A8214CE928F72EC4C12CCCAA6F21D9ED7FF85A0236896AD0DE0`。v3 **未改** `script.md`／`script-source-notes.md` 任何位元組，因此 v2 的逐句來源 PASS 仍綁同一對 SHA；視覺文字 HOLD 須以新視覺 SHA 獨立複核。

v1 曾交出的檔案 SHA（只作歷史對照，**不指向目前工作樹**）：script `4974D957F308D2C9642BCA106BAA7B29B4EE42A8CFD605AEDB5B755596D6A104`；來源筆記 `FDE6E7272EF206E09AE03E64010D0225D1285CD17B5F7B32394ACAEF6C727BF3`；分鏡 MD `89D50B4D40A2A9D54996F68376EA6A416248B32E6822ADC6DA2CC51ADC897E95`；JSON `B83E80424E12B2180E7F2F75E8E84ED1716DC314C8D021C6DA83F25E44F50681`。v1 來源與逐鏡文字 PASS 僅綁舊版，v1 雙盲 HOLD，不能轉簽 v2。

## 作者本機機械檢查

- 61 句各有唯一 ID、行末 S／M 來源；JSON 61 鏡逐一同順序對應；六章連續。正文約 2,107 個口播字元，按 250 字元／分鐘及逐鏡四捨五入**估算** 505.4 秒；加片頭 5 秒、片尾 21 秒為 531.4 秒。**未 TTS、未實測正文是否 ≥480 秒。**
- 依具體設問標記、紙上時長與片頭計，按設問所在鏡頭終點量得最大設問間隔 40.8 秒；伏筆／回收對列於稿末。這只是標記及算術，**v2 雙讀者敘事盲評尚未結案**；作者不代簽判定。
- 49 鏡概念插圖、12 張後製字卡；插圖時間 397.5／505.4 秒，即 78.7%；最長連卡 2，最長單鏡暫估 11.3 秒。真實畫面比例須在圖像與成片後重驗。
- 圖像 prompt 自檢未出現 CamelBak、ThermoBak、Eidson、Fawcett、Wemmer、logo、專利附圖等禁項；姓名、日期、百分比只在後製卡片。插圖皆為泛用概念場景，未生成任何圖。
- v3 結構檢查 **PASS**：61 句／61 鏡同序、I01 卡為「公司回顧：1989 年成立」，505.4 秒紙上正文、397.5 秒概念插圖、78.7%、12 卡、連卡 2、單鏡最長 11.3 秒、片頭 5 秒／片尾 21 秒。`npm run check:tasks` **exit 0**（2082 張任務票已驗證；輸出含其他既存長期認領／重疊範圍警告）；`git diff --check` **exit 0**。提交前再對暫存檔跑 `git diff --cached --check`。這些機械檢查不代替內容覆核。
- `npm run test:docs-videos` 的 v1 初跑退出碼 1：此工作樹缺少 lockfile 已列的 `pinyin-pro`；當時 `npm ci --no-audit --no-fund` 逾八分鐘未完成，已停止。v3 只改視覺字卡及說明，不再重試耗時安裝；全量測試不記為通過。

## 特別交接

作者把品牌回顧的 **1989 年比賽**、較晚專利回溯的 **1988 年背包與水瓶組合**、商標的 **1988 年 first-use 聲稱** 分開；口播／字卡只留品牌回顧的 1989，後兩者留在來源筆記，均不替同一場比賽定年。I01 字卡原否定語可能誤讀為「1989 不是比賽年」，現只寫「公司回顧：1989 年成立」；O10 仍另寫品牌事後回顧騎乘 1989，兩張卡記不同事件而沒有互相否定。Fawcett 1990 申請的閥專利在介紹前已明說是**另一人的平行解法**，只留約 47 秒的技術旁支，不宣稱與首款 ThermoBak 的已證先後或採用。商品線按 **1993 走訪單車店→2006 瓶類→2014 商品與通路** 往前；騎乘不先取車架瓶與日常手邊拿瓶構成具體收束。50% 瓶類和 37% 水袋背包只屬 **CamelBak 2014 年毛銷售額**，不代表現況或任何一人巡店的成果。獨立覆核者請只針對 v3 的 I01／O10 字卡和分鏡說明重審；v2 純旁白雙盲另行進行。若 HOLD，回到稿版修訂並更新收據雜湊；不得沿用本作者收據冒充 PASS。

本次沒有付費生成、匯入、上傳、發布、合併或部署。
