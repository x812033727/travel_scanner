# 第三片草稿：110 句事實與 agreement 窄範圍核對

日期：2026-10-25 UTC。實際讀取 `third-topic-script-draft.md` 全文與 **L001–L110 共 110 句**，SHA256 `30ea3096701bf775afac9c371466752cc0e1b138e70cbc0198f23b723fd2a2a4`，16,743 bytes。這是 scratch 草稿核對，**不是正式 video.json／claims 的 PASS，也不是盲讀評分**。本檔不修改作者檔案。

**結論：草稿需修正一項確定的官方流程錯序（L089–L091）。L094–L096 的兩版無指定 error／可觀察行為集合相同，核心內容有官方支持；完整前提與有限 trace 的精確化如下。L085／L099 為 root 已交作者處理的兩項待落地修正，不能在原版本上假稱已修好。其餘口白未發現新的重大數值或條件錯誤。**

## 必修：官方 checker 的實際時序

| 定位 | 原稿問題 | 精確修法 |
|---|---|---|
| L089–L091；素材 S84–S93 的流程箭頭 | 原稿是「先符合固定命題→接著稽核假設→最後 Rocq 核心」。官方文件明說 kernel 在 `rocq compile` 編譯每個 term 時檢查，不是假設 audit 完成後才開始。 | 建議 L089「Rocq核心在編譯時，檢查AI寫出的證明。」L090「工具再把結果對到固定命題，列出它使用的假設。」L091「使用的假設，也必須通過允許清單的稽核。」可避免聲稱三道互不重疊的檢查。 |

正確圖示應為：**固定 binary／statement／LPS → AI proof → 編譯 proof 與工具產生的 wrapper（Rocq kernel 在編譯中檢查；wrapper 要求精確 statement 型別並列出假設）→ 工具稽核允許假設清單**。Kernel 不應畫在假設 audit 之後的獨立最後關卡。這也補正舊研究筆記／brief D5 中可能被讀成此錯序的箭頭；舊檔及既有評分保留歷史，不把新理解倒填成舊版本已通過。

新讀取第一手證據：

- URL：https://raw.githubusercontent.com/theorem-labs/oss-verify-proofs/main/docs/checking.md
- 人可讀官方頁：https://github.com/theorem-labs/oss-verify-proofs/blob/main/docs/checking.md
- 正常 editorial UA GET **200**，effective URL 同上。
- 讀取時間 **2026-10-25T19:06:15.979435+00:00**。
- 原始回應 SHA256：`8fea2025f3a16f72613b3a70a7b51716cf7058c11fe5b453e327d970702af160`。
- 文件 `What oft check does`：先編譯 proof/library，再編譯自動產生的 wrapper，wrapper 把 proof 的 theorem 對到目標型別並輸出 `Print Assumptions`；之後才稽核輸出。另明列 kernel 隨 `rocq compile` 檢查 term。
- 不要額外宣稱預設 CI 執行 `rocqchk`：該頁說它是可選第二檢查，不屬預設 verdict。這不否定編譯期間已執行的 kernel 檢查。沒有本地執行任何上述工具。

## L094–L096：agreement 的支持與完整條件

依據：既有官方 `README.md` 的 `The theorem, in words`，以及 `docs/statements.md` 的 `Agreement` 段落；本次重讀保存的完整原始 Markdown。

| 原句 | 判讀 | 建議精確文字／畫面 |
|---|---|---|
| L094「公開版本檢查一般版與加上錯誤檢查的版本，行為是否相符。」 | **核心正確。** plain 對 ASan、UBSan 或兩者的 sanitizer build，各有對應 agreement。不是原始碼／任意部署版本，也不是兩次執行逐步同步。 | 可保留。卡片標明 `plain ↔ sanitizer build`，綁這份 release 的固定 binary／statement／LPS。 |
| L095「在指定輸入、記憶體條件和系統模型內，兩版都不出現指定錯誤。」 | **核心正確，但前提可說得更明確。** 是符合命題前提的所有有效程序輸入；記憶體前提特別施於 plain build，而不是要求兩版共用相同預算。每份命題還規定允許的環境／系統呼叫失敗條件。 | 建議「在各命題的系統條件下，對一般版不超過記憶體預算的輸入，兩版都不出現指定錯誤。」畫面補「符合前提的所有有效程序輸入」，不要畫成抽幾筆樣本或所有現實環境。 |
| L096「它們可觀察的行為集合，也要相同。」 | **README 摘要直接支持此表述。** statements 的嚴格形式是相同的**有限 trace 集合**。輸出、退出狀態／最終檔案內容在模型定義的可觀察範圍內；不代表任何未納入觀察的內部狀態完全相同。 | 精確候選：「兩版可觀察的有限行為軌跡，集合也要相同。」卡片保留 `same set of finite traces` 的概念；不用逐步同步的動畫。 |

這裡的指定 error 包含模型所定義的 crash、無效記憶體存取、abort／失敗檢查或離開 LPS 的步驟，**不是所有邏輯錯誤**。即使 sanitizer 無法辨識的錯誤結果／資源洩漏仍存在，也不與此 agreement 矛盾。有限 trace 集合相同不排除 hang，因此 L097–L100 的終止區分成立。**「這份 release 未提供 halts 證明」不能外推官方整個 239 入口研究。**

公開 proof 的範圍宜在正式卡片／claims 補全為：固定、單執行緒的靜態 riscv64 Linux binary、musl、特定 LPS 與各命題前提；L088 單說「RISC-V 二進位」並非錯誤，但不足以單獨交代整份 contract。口白可簡潔說「公開版針對固定的靜態RISC-V執行檔，在Linux程序模型內證明」。不要把它畫成整個函式庫、任意架構或整個應用程式的認證。

## root 已指定的修正與其他小精確化

| 定位 | 狀態／建議 |
|---|---|
| L085 | 原版本仍是「這次研究報告涵蓋……」。root 已要求明說**官方研究報告** 239 入口／123 庫；這是官方報告值，不是本片重現。待正式版本確認。 |
| L099 | 原版本仍是「返回相關的命題」。root 已要求改成**終止命題**，以免把作業系統程序退出與函式返回值混為一談。待正式版本確認。 |
| L063 | 建議改為「超過設定的零點二五秒門檻，被工具中止」。原資料記錄的是 `timeout=0.25`，沒有精確測得牆鐘時間剛好 0.25 秒。L065 已正確說明 timeout 本身不證明永不結束；此處不應當效能 benchmark。 |
| L015 | 可保留口語「一般整數計算」；原生 code／claims 應精確記 `n` 先提升到 `int`，再加 1。不是無號 8bit 加法先算出 0，也不是有號 UB。 |

## 全部口白的核對覆蓋

以下為本草稿實際逐句讀取後的分組結果；「未見新錯」不代表聲音、版面或正式檔案 QA。

| 範圍 | 結果與關鍵核對 |
|---|---|
| L001–L013 | 未見新錯。容量 8byte、另需 1byte 結尾、域 0..255、應接受 0..7；日期 10/22 對官方公告日，非逐次實驗完成日。編輯問題未捏造使用者經驗。 |
| L014–L029 | 未見新錯。255+1 先為 256，窄化為 0；型別 bit 與容量 byte 分開。L023–L025 已明說完整 RHS 一起改，節錄與實際修正版相符。 |
| L030–L041 | 未見新錯。五個刻意小值，完整 256 列，唯一誤接受 255；修正後兩方向均零。命題 SAT 與 C 逐例相符，未叫作 SMT／Rocq，也未說求解器在這個域超越完整枚舉。 |
| L042–L055 | 未見新錯。deny-all 僅符號臂；零誤接受、8 個誤拒絕；guard 沒有 buffer 寫入；完整契約含合法值也應接受。 |
| L056–L071 | 未見新數值／模型錯。第二個獨立程式、固定上限與無外部寫入者，255→0 的 256 步環正確。0.25 秒門檻用詞見上；逾時與有限控制圖理由已分開。 |
| L072–L083 | 未見新錯。計數器連同對應轉型一起改；255→256 離開、返回 256；所有 256 次修正版 C 呼叫返回 n+1。沒有把被修正 guard 拒絕的 255 串成下游輸入。 |
| L084–L093 | 官方數量與固定對象有支持；**L089–L091 錯序必修**，L085 歸屬依 root 修正。L093「能編譯不等於目標已完成」正確，仍須精確命題與假設稽核。 |
| L094–L100 | 核心有支持；agreement 完整前提與有限 trace 建議見上；L099 按 root 改終止命題。release 限定不能消失。 |
| L101–L107 | 未見新錯。完整枚舉／命題 SAT 對 guard，有限控制圖對 loop，兩者有各自實際 C 對照；沒有宣稱本地執行官方 Rocq 或完成整個應用程式認證。 |
| L108–L110 | 編輯 CTA，無新增可查事實或虛構私人體驗。 |

## 原始證據與收據界線

- `formal-demo/guard.c`：`4bfc837e2f17c1ae8326924a926929ee3d8dec29e88ec355b77db591c0d9e799`。
- `formal-demo/loop.c`：`b1d181702c61b152724eeeb693891f45005e7ca0c7dfa583cb5378a6fc68f0a2`。
- 官方 README raw：`58e191365e6993e596e88f9b832136bb106077935dd66088c6c5afca874706e2`。
- 官方 statements raw：`58740a11354d8e9bcf452e923f72832e2372ad55fa4eb714f546ab055c302932`。
- 官方 origin raw：`be76fd60b434a0b68905015580c06e1a8bc41989cccd18f3f5fa9726e675c70d`。
- 第一手 URL：`https://www.anthropic.com/research/formal-verification`、上述官方 repo 的 README、`docs/origin.md`、`docs/statements.md`、新增 `docs/checking.md`。

既有 `third-topic-facts-final.md` 的 F06 沒有宣稱檢查先後，保留歷史；本檔是流程順序的精確補充。官方各頁只做必要事實摘要，未加入長段逐字引用；本地算步與程式是原創分析。正式 JSON／metadata／diagram／翻譯／音訊未在此收據內；凍結後須對實際 SHA 另開正式審查，不移用本草稿結論。

後記：為供圖稿作者直接核原文，正常 UA 再 GET 同一 `checking.md`，2026-10-25T19:09:15.764950Z 回應 200，6,723 bytes，SHA 與首次讀取完全相同。原始回應保存 `third-topic-source-proofs-checking.raw`；完整 HTTP 收據為 `third-topic-source-proofs-checking.http.json`。沒有執行該頁程式。

收尾時作者已將草稿更新為 114 個口白 ID，讀到的當時 SHA 為 `3ff84cf656b4002fdf0e01e0cfbcf01cd14c3d4dacc21f34efa57bc92cc77676`（17,581 bytes）。**此報告仍只綁頂端的 110 句 30ea3096 版本，不宣稱已審新增／改寫的 114 句版本。**
