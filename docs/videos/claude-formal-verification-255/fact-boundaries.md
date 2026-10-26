# 第三片：來源與原始產物最終事實邊界

核對日：2026-10-25 UTC。這是正式逐句腳本之前的來源／程式／輸出核對，不是對尚未交付旁白的逐句 PASS，也不是另一位作者重新產生的實驗。沒有執行官方 checker、付費模型、註冊、安裝或改動 repo／原始 demo。本次獨立從既有 256 列資料重算，兩份 manifest 共 14 檔全部吻合。

**結論：本題可用。官方數量、兩例結果與企劃的主要保證界線均有證據；正式稿必須遵守下面「完整修法」，不能用只改宣告的畫面替代實際修正版。**

## 正式稿必守的完整修法

1. Guard 錯版的 `uint8_t total = (uint8_t)(n + 1);`，不是只換左側型別。若保留右側 `(uint8_t)`，256 已經先變成 0，再存入 16bit 也救不回來。展示實檔完整修正版：

   ```c
   uint16_t total = (uint16_t)((uint16_t)n + 1u);
   return total <= CAPACITY;
   ```

2. Loop 也不是只換計數器宣告。必須移除更新式原有的 8bit 窄化；實檔是：

   ```c
   volatile uint16_t i = 0;
   while (i <= n) {
       i = (uint16_t)(i + 1u);
   }
   ```

3. 可說「讓總長的計算與儲存保留完整值」、「計數器和更新式都能保留 256」。不可說「只改兩個字」「只換宣告就修好」。企劃的「改兩個具體型別位置」應理解為兩份程式各自的完整修正，不能拍成兩個宣告文字替換。

## 可直接納入 claims 的核對表

| ID | 可用事實／建議口述 | 來源與不可擴張的範圍 |
|---|---|---|
| F01 | Anthropic 和 Theorem 在 **2026-10-22** 發布這次合作研究消息。 | S1 明列發布日，S2 同日列合作文章。這是公告日；實驗跨數週，未取得逐次起訖時間。不得說 239 個入口都是當天完成，也不得稱 OSS Verify 於該日首次上線。 |
| F02 | **官方報告**：Claude 為 **239 個入口、123 個 OSS-Fuzz 函式庫**寫出相應證明。 | S1。入口不是整個函式庫的全部程式。不可說本片重現、全函式庫無 bug，或把後續 36 題模型比較當 239 題的同一測試。 |
| F03 | 本日讀取的**公開 release**列有 **60 個入口、25 個函式庫**的證明。 | S4 開頭與表格；本次重數 `proofs/` 連結列為 60、不同 library 欄為 25。不是 239/123 的可比涵蓋率；不做相減／百分比。S5 說部分既有證明已適配本 release 的 binary／LPS 並重新檢查。 |
| F04 | 證明針對固定編譯產物、正式命題與機器／作業系統模型，在其條件內成立。 | S1、S4、S5：單執行緒、靜態 riscv64 Linux binary、musl、特定 LPS／記憶體前提。不是任意原始碼版本、動態 glibc、x86／ARM、呼叫端使用方式或所有現實機器。LPS 自述並不完整。正文不必朗讀容易混淆的 64 MB／MiB 門檻；若使用，須綁具體 statement。 |
| F05 | 這份公開 release 的 agreement 命題**不排除無限執行**；release 沒有已證的 halts 命題。 | S4、S6。精確短引：**“No proof in this release proves a halts statement”**（9 words）。只描述這份 release；不得改為所有 239 個研究案例都未處理終止，也不拿概述和具體命題的差別指控造假。安全性與終止是不同要求。 |
| F06 | AI 寫證明，checker 檢查它是否證明指定命題，並稽核允許的假設。 | S5。不是「檔案能編譯就算成功」，也不是任意加入假設／留下 `Admitted`。仍須信任命題、模型與 checker 等組件；我們未下載或執行該 Rocq checker。S3 的免費服務限符合條件的開源專案，由核心維護者申請，不是任何人即時貼碼的不限量產品。 |
| L01 | 本地 guard 的輸入是 **0..255**，容量是 **8 byte**，另需 **1 byte** 結尾；完整需求為「應且只應接受 **0..7**」。 | `guard.c`、完整 CSV／JSON。8bit 是長度型別，8byte 是容量，不能混稱 8bit 緩衝區。程式只回傳接受與否，沒有實際寫入緩衝區，不得宣稱真的造成越界寫入。 |
| L02 | 255 加 1 先得到 **int 值 256**，之後轉成 `uint8_t` 才變成 **0**。 | 原始 C、實際欄位 `promoted_total`／`narrowed_total`；S7 §§6.3.1.1、6.3.1.3。這是定義良好的無號窄化轉換，**不是加法本身變 0，也不是有號溢位的未定義行為**。 |
| L03 | 刻意先看的小值 **0、1、2、3、4** 都符合；同一完整 256 輸入中，錯版只多放行 **255**，總共接受 **9** 個。加寬版及 `n<8` 版各接受 **8** 個，零誤接受、零誤拒絕。 | `all-256-cases.json`；本次逐列以數學規格及 modulo256 重算，零差異。不是隨機抽樣、fuzzer 次數、AI 準確率或大型模型效能測量。 |
| L04 | 第一例另用 SymPy **命題 SAT**：錯版誤接受有解 255；排除 255 後無解；加寬版兩方向查詢均無解。 | `run_demo.py`、`sat-output.json`。八個**輸入**布林位元；位元模型對實際 C 的四項輸出逐例 256/256 一致。不是 SMT／Rocq、通用已驗證編譯器或獨立核過的證書。這麼小的有限域，完整枚舉也能得到答案，不宣稱 SAT 勝過枚舉。 |
| L05 | 一律拒絕的符號對照雖零誤接受，卻拒絕 **0..7 共 8 個**合法值；補上「該接受就接受」後便不合規。 | 常數 `false` 的實際 SAT 查詢及同域規格。這一臂是符號對照，**沒有另一個已編譯 deny-all C 執行結果**；不得借它宣稱官方修補曾如此作弊。 |
| L06 | 第二個**獨立**計數程式，錯版對 0..254 返回 n+1；n=255 子程序在本次 **0.25 秒**門檻逾時被終止。 | `loop.c`、`loop-all-256.json`。0.25 秒只是觀察，不單獨證明永不結束，也不是效能 benchmark。正確 guard 會拒絕 255；不要把第二例畫成第一例修好後放行 255 的下游。 |
| L07 | 固定 n=255 的有限控制圖中，8bit 計數器 **0..255→0**，重複週期為 **256**；加寬版 n=255 會走到 **256**、離開並返回 256。 | 完整控制狀態枚舉，加寬版 256 次實際 C 呼叫均返回 n+1；本次逐列重算零差異。這是固定域、無外部寫入者的局部 volatile 計數器模型，非通用停機定理。不是 SAT、SMT、Rocq 或 vendor proof 重現；volatile 有讀寫，不說「沒有任何記憶體存取」。 |

## 第一手來源與讀取證據

既有正常 editorial UA HTTP 收據：`third-topic-source-http.json`，六個官方／官方 repo 頁 GET 均 200；本次重讀保存的原文與原始 Markdown，不以搜尋摘要替代。S7 本次新 GET 200。只核下列相關段落，沒有聲稱重跑供應商證明。

- **S1** https://www.anthropic.com/research/formal-verification — Published Oct 22, 2026、239/123、固定 binary／模型及 limitations。
- **S2** https://theorem.dev/blog/ — October 22 2026 的合作文章條目；不據此推首次推出日期。
- **S3** https://theorem.dev/oss-verify/ — 服務資格、核心維護者申請與優先順序。
- **S4** https://github.com/theorem-labs/oss-verify-proofs/blob/main/README.md — 60/25、agreement、no-halts、工具版本與限制。核對 raw SHA256：`58e191365e6993e596e88f9b832136bb106077935dd66088c6c5afca874706e2`。
- **S5** https://github.com/theorem-labs/oss-verify-proofs/blob/main/docs/origin.md — 精確型別／假設稽核、既有證明適配。raw SHA256：`be76fd60b434a0b68905015580c06e1a8bc41989cccd18f3f5fa9726e675c70d`。
- **S6** https://github.com/theorem-labs/oss-verify-proofs/blob/main/docs/statements.md — agreement 與 halts 是不同命題。raw SHA256：`58740a11354d8e9bcf452e923f72832e2372ad55fa4eb714f546ab055c302932`。
- **S7** https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf — C11 委員會草案（不是宣稱取得付費最終 ISO 全文）；HTTP 200，2026-10-25T18:59:19.903793Z，1,692,004 bytes，SHA256 `208969fec021e4f4ce87a1873765298c73e7bbb5209b1c5868967c7adfc8492e`。只查整數提升與有號／無號轉換相關條款。

來源使用：本報告唯一英文逐字短引為 S4 的 9 words；各頁事實摘述均控制於約 200 English-word equivalent 內。本地 L01–L07 為本片原創程式、算術與結果分析，不能掛成供應商原始測試結果。

## 本次版本綁定與驗證範圍

| 讀取產物 | SHA256 |
|---|---|
| `third-topic-brief.md` | `2b00229f67fec838c58e75f9f152d6a4602d04174e35f260a94557d67114aba9` |
| `formal-demo/guard.c` | `4bfc837e2f17c1ae8326924a926929ee3d8dec29e88ec355b77db591c0d9e799` |
| `formal-demo/run_demo.py` | `ca1a40f38cf95c35dfa45830cc6dc7d1fc50f62044a3a8e1cb6f26f84dd90393` |
| `formal-demo/results.json` | `724d32d699601eb523dafaa04a1165bf77a32459b8b4641c8ed102e7316a272c` |
| `formal-demo/all-256-cases.json` | `e957484d742ea0b6fc39c9f5c8bdb80f91d5299ef13fad574a55c1d534d5c1d8` |
| `formal-demo/sat-output.json` | `6faee1dfe1437ae212f5f13eeb6f95571edef9a2a8d9374927895ef7e8495078` |
| `formal-demo/loop.c` | `b1d181702c61b152724eeeb693891f45005e7ca0c7dfa583cb5378a6fc68f0a2` |
| `formal-demo/run_loop_demo.py` | `e6f0ccc47271a7a0895aff5023d358d0a64a8b531763fe68eecb328d02991db5` |
| `formal-demo/loop-all-256.json` | `2523d7e0650d3a89b8d90987c300b5a3d588f50ad5137262be9916167920a86c` |
| `formal-demo/loop-results.json` | `c710013a94fd45f34c90d6a40454e9691e2cf5ff078e6e8c199632b9ee4ab434` |

本次讀取程式、runner、原始輸出與 manifests，重新計算兩組既有 256 列及 60/25 目錄數量；未重新生成或覆蓋任何原始執行產物。正式 video.json、metadata、縮圖、翻譯或聲音尚不在此收據的檢查範圍。後續若劇本更改數字、運算式或命題範圍，須按正式版本再逐句審查。
