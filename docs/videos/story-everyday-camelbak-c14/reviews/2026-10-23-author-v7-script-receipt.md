# C14 CamelBak｜作者 v7 敘事修稿收據（待獨立覆核）

- 日期：2026-10-23（台北時間）；作者：codex-c14-script；去向：[draft PR #1695](https://github.com/x812033727/travel_scanner/pull/1695)。
- 已採用 Treatment SHA-256 `078DC1D77C46EB49BB6F27F60535F22775781E5963783BDA7C1F7625B1A8700E`、矩陣 SHA-256 `F8CF68AA36264DF18CDBE6ECD698D4AF1F22E405DEAADA8ED275B7685050587E`，本輪重驗且未改位元組。
- [v6 雙讀者分歧收據](blind-narration-v6-coordinator.md) 綁 74 行投影 SHA-256 `4AC3A5207ACDD7343E16B1B31E4F3DD15CCC59B43C44F6A6415E13A8FBE84BDB`：A **HOLD**、B **PASS**。v6 沒有雙盲通過；[v6 O02 來源／逐鏡窄修 PASS](independent-v6-o02-delta-review.md) 也只屬舊版。此作者收據不替 v7 自簽來源、逐鏡、盲評或站主 PASS。

## v7 作者檔案 SHA-256

| 作者檔案 | SHA-256 |
| --- | --- |
| [script.md](../script.md) | `AB75F9DCDA20822A2E6D1FB9A1BE6CD36466D9F664363F71674DFBB2C2982970` |
| [script-source-notes.md](../script-source-notes.md) | `22B265AC273E534C94B81EA3C6EC82E95B711ADEEA0AEFABA0D2B9CCB5DD325A` |
| [visual-plan.md](../visual-plan.md) | `9F8A2A73AA918B6D5384FDBD032196CDFA0AB96A1A248D8F7E2DA4AE60E2936B` |
| [visual-plan.json](../visual-plan.json) | `39D59822D009A45CC4279E9CDFAE325C448EAAB66FED8034CEE8D59663478A01` |

另有 [v6 雙讀者分歧協調收據](blind-narration-v6-coordinator.md) SHA-256 `E0B180767EEF530DD1003DFB7B71944906394B6D45DAF5F1AD2D92399F5BF2EE`。若獨立盲評需要新純旁白，從 v7 70 個行 ID 擷取 `〔〕` 前句子、每行一列、UTF-8 LF 且尾端一個 LF 的投影 SHA-256 為 `914322CED7DE3D1670C36A040EC578F5CA1F23299CDD5AEA35DF0D490C13234F`；接收者應自行重建核對，不把此作者算作讀者。

## 依兩份判語所作的窄修

- I11–E05 把 **1998 送件、2000 授權是同一口器專利**說清，只留一次咬開和一次鬆口閉合；T05 用相同年份重指 S8 被 S9 水瓶申請引用。原型衣夾、較晚專利和報導水瓶仍分開。
- E06–E11 把 2003 年報導的 1,000＋500 套說成**準備寄送**的另一次背水使用場合，接「兩年後」的瓶子文件；這是時間／容器對照，沒有軍用寄送促成瓶類研發的主張。
- T11–T17 刪去口播設計獎、減少同義的通路宣告；新管理方向、初期 Better Bottle、減少一次性瓶的公司願景及 2007 設計簡報分別歸給母公司或公司新聞稿，不認展場瓶為每款 Better Bottle 的精確 SKU。
- N01–N15 把通路說法壓成兩句，N04 提問後立刻接 2012 瓶類約 34%、2014 瓶類約 50%、同年水袋背包約 37%。分母都是 **CamelBak 毛銷售額的產品占比**，不是今日數據、市占或絕對銷量。以騎乘背水／桌前拿瓶的具體示例作回答與結尾。
- 同步調整配鏡：E01 與 T05 卡明示同一口器專利申請／授權年，E08 預備寄送卡，N05–N07 三張歷史比例卡；其餘只用無標誌概念插圖，沒有專利附圖或真人／戰地重建。沒有改採用的 Treatment 或矩陣。

## 作者機械檢查與停線

- 70 個唯一口播 ID 對 70 個同序 JSON 鏡頭，六章、每句 S 來源代碼可在註解中找到；look.preset 精確為 cute-mystery，5 秒開場後片頭與 21 秒 v4 片尾欄位正確。逐句按每分鐘 250 字元換算，最長單鏡 **10.1 秒 T12**。
- 正文 **2,067 口播字元／1,678 漢字，紙估 496.0 秒**，加片頭片尾紙估 522.0 秒（8:42）。**沒有 TTS；實際正文 ≥480 秒與約十分鐘仍待測**，目前紙估餘裕只有 16 秒，不應把它當實測 PASS。
- 54 幅概念插圖／16 張後製字卡，規劃插圖 **372.8／496.0 秒＝75.16%**；最長連卡 3。只算新鉤、不重算回收鉤並計入片頭，最長紙估鉤間 **36.5 秒 O09→I05**，最後一鉤至結尾 28.7 秒。
- 作者結構檢查（ID、來源碼、秒數、圖時比例、連卡、鉤間距、prompt 禁項、採用稿 SHA）與 `git diff --check` exit 0。`npm run check:tasks` exit 1，唯一 error 為已存在且未追蹤的同 ID v4 獨立覆核 task open/done 兩份；本作者未編輯、暫存或刪除。其餘是現存 task warnings。

請另一位代理重開原件並依上面**四個 v7 SHA**逐句／逐鏡查核，再交兩位未讀 v7 的讀者各自只讀純旁白。其後仍須正常語速 TTS、生成圖逐張驗收、站主稿／分鏡採用及付費前整集報價。本輪沒有付費、匯入、上傳、合併、發布或部署。
