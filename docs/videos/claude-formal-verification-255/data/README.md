# 形式化驗證候補：有限 8-bit guard 可行性實測

2026-10-25；10 分鐘限時可行性工作，僅 scratch。未安裝套件、未下載專案、未呼叫付費服務、未重現供應商證明。

## 可重跑指令與環境

實際執行：

```sh
python /workspace/work/ai-tech-next/formal-demo/run_demo.py
```

Python 3.12.14；GCC `gcc (Debian 14.2.0-19) 14.2.0`；SymPy 1.14.0、`satisfiable(..., algorithm="dpll2")`。PATH 未發現 Rocq/coqc、Lean/lake、Z3、cvc5、Boolector；Python 亦未裝 z3/cvc5。此處使用真正可用的**命題 SAT 求解器**，不是 SMT 或 Rocq，沒有另外匯出並獨立驗證 proof certificate。

Runner 實際編譯命令已保存在 results.json，採 C11、O0、Wall/Wextra/Werror/Wconversion/Wshadow/pedantic；編譯 exit 0，stdout/stderr 均空。完整 C 原始碼為 guard.c。無不安全記憶體寫入，只執行長度 guard。

## 完整規格與實際結果

輸入為 payload 長度整數 n∈[0,255]，固定 8-byte 容量，另需 1 byte 結尾字元。規格為數學整數 `n + 1 <= 8`，因此應且只應接受 0..7。

錯誤 guard 先把總長存回 uint8_t 再比較。初始刻意選取的五個測試 0、1、2、3、4 全通過；此抽樣不是隨機測試或統計精度實驗。編譯後 C 的全部 256 個輸入只有 255 誤接受：C 的整數提升先得到 256，再轉回 uint8_t 變 0。應說「窄化轉型後繞回」，不能說加法本身發生未定義有號溢位。

修法一以 uint16_t 保存總長；修法二直接以 n < 8 判斷。兩者在同一完整有限域的 256 例均符合規格，零誤接受與零誤拒絕。

| n | 提升後總長 | uint8_t 儲存值 | 錯誤 guard | 修正 guard／規格 |
|---:|---:|---:|---|---|
| 7 | 8 | 8 | 接受 | 接受 |
| 8 | 9 | 9 | 拒絕 | 拒絕 |
| 254 | 255 | 255 | 拒絕 | 拒絕 |
| 255 | 256 | 0 | 接受 | 拒絕 |

另外以 8 個**輸入**布林位元建立獨立 ripple-carry 加一模型，保留進位；每個輸入的符號結果均與實際編譯 C 四項結果逐例相符（256/256）。求解器可能使用輔助變數，不能稱求解全程只有八個變數。

SAT 查詢找到錯誤 guard 的反例 n=255；排除此值後沒有第二個反例（UNSAT）。修正 guard 的「接受不合格輸入」與「拒絕合格輸入」均為 UNSAT。另加「一律拒絕」對照：它也沒有不合格輸入被接受，但會拒絕合格輸入。因此只要求安全、未要求應有功能，可能讓無用的實作過關。

## 保存的證據

- guard.c、run_demo.py：完整原始碼與實際命令。
- compiled-c-results.csv、all-256-cases.json：編譯 C 的全部 256 例原始結果。
- symbolic-vs-c.json：256 例符號與 C 對照。
- sat-output.json：各查詢完整命題公式、SymPy 原始回傳、解碼結果，含排除 255 的查詢。
- results.json：環境版本、編譯 stdout/stderr、總結、來源與執行檔 SHA-256、精確範圍。
- run-demo.stdout.json：此次實際印出之完整 JSON 結果。
- manifest.json：上述九檔案的 byte size 與 SHA-256。重跑的求解時間及部分輸出排序可能改變，屆時 manifest 會記錄新產物。

## 影片可用敘述與界限

可用：「我們先寫出應接受哪些長度，再用反例修正 guard，最後檢查這 256 種輸入。這是我們自己的有限域枚舉加命題 SAT 交叉檢查，不是重現新聞中的 Rocq 證明。」

此實驗不涵蓋任意容量、任意輸入型別、實際 buffer 寫入、字串解析、並行、整個應用程式或 C-to-Boolean 的通用正確翻譯。不能外推供應商的 123 個函式庫／239 個入口已由我們驗證，也不能叫作「已形式化證明整個程式安全」。

判斷：**可行**，足以提供約 2–4 分鐘有真實操作與正向資訊增益的主幹。單靠這個 toy demo 不宜湊滿 8–12 分鐘；若未來製作，應結合官方實際 proof/spec/checker 管線、已公開子集和可核實限制。此處完成可行性即停止，不開新 episode 或進入製作付費階段。
