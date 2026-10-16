# 執行紀錄：用 REA 逆向自己的軟體

這是這支影片的實測原始紀錄，給撰稿與查核當依據。全部在 2026-10-16、一台 Windows 11 機器上跑，分析的都是我們自己擁有或自己編譯的目標（REA 的 DISCLAIMER 只允許分析自己擁有或被授權的軟體）。原始 JSON 在該 session 的 scratchpad（`rea/runlog/`），不進 repo；下面是摘要與可引用的數字。路徑裡的使用者名稱已去識別化。

## 環境

- REA：`rea-agents` npm 套件，`6.5.0`（`npx rea-agents setup` 是官方安裝法；這裡為了隔離，直接把套件裝進一個丟棄用目錄、不改本機任何 agent 設定，CLI 用 `npx rea <command>`）。
- 本機原本就有：Node.js 24.13、.NET SDK 10.0.400、Chrome 155。沒有裝 Ghidra／IDA／Hopper（原生執行檔的深度反編譯要它們；這支用的 .NET 靜態分析與網站分析都不需要）。
- 混淆工具：Obfuscar GlobalTool 2.2.50（開源，MIT），開了 `HideStrings`、`RenameFields`、`RenameProperties`。

## 靶一：自己編譯的小程式 NoteVault（.NET）

一支約 90 行的 C# 主控台程式，模擬「有 Pro 付費功能的筆記 App」，故意犯三個常見錯誤，所有秘密都是假的測試值：

1. 授權檢查在**用戶端**：`License.Check` 用寫死的簽章密鑰 `nv-test-secret-7f3a9c` 算 HMAC 驗 key。
2. 一個除錯後門：環境變數 `NV_INTERNAL_DEBUG=letmein` 直接解鎖全部 Pro。
3. 一個隱藏折扣：region `EDU` 打四折（`NT$90`）；還有同步端點與一把假 API key `nvk_test_...` 寫在常數裡。

編譯成 Release（`NoteVault.dll`），再做兩個混淆版：
- `bin-obf`：秘密寫成 `const string`（C# 會把 const 內嵌到每個使用點）。
- `bin-obf2`：同一份程式，秘密改成 `static readonly string`。

### REA 的實測結果

一個指令 `rea inspect-managed-members NoteVault.dll`（靜態，不載入、不執行程式）：

| 版本 | REA 抽到的字串常數 | 一行位元組掃描還找得到密鑰？ |
| --- | --- | --- |
| 原版 `bin-plain` | **23 個，全部**：`nv-test-secret-7f3a9c`、`NV_INTERNAL_DEBUG`、`letmein`、`EDU`／`NT$90`、`nvk_test_...`、各區價格 | 是 |
| 混淆版（const）`bin-obf` | 0（字串堆被清空，REA 的 ldstr 視圖看不到） | **是**（密鑰仍以 UTF-16 明文躺在檔案 offset 4838；const 內嵌的字串混淆器沒真正加密） |
| 混淆版（readonly）`bin-obf2` | 0 | 否（這次才真的從位元組裡消失） |

量到的事實：
- **原版**：REA 一個指令、沒有反編譯器，就把全部 23 個字串倒出來，三個秘密全中。
- **混淆**只改「讀不讀得到」，而且**不一致**：同樣開 `HideStrings`，秘密是 `const` 時字串仍以明文留在檔案裡（REA 的字串視圖看不到，但 `strings` 等級的掃描一掃就有）；改成 `readonly` 才真的藏掉。
- 真正的重點——**不管哪個版本，付費閘門照樣繞得過**。因為驗證跑在用戶端，我用寫死的密鑰自己算出一把合法 key `NV-123456-78F56FB4`：

| 繞過手法 | bin-plain | bin-obf | bin-obf2 |
| --- | --- | --- | --- |
| 偽造的授權 key → `Pro activated.` | ✅ | ✅ | ✅ |
| `NV_INTERNAL_DEBUG=letmein` → 解鎖全部 Pro | ✅ | ✅ | ✅ |
| `NV_REGION=EDU` → 偷到四折 `NT$90` | ✅ | ✅ | ✅ |

混淆把字串藏起來了，但沒有改變「判斷在用戶的機器上做」這件事，所以三種繞過在混淆版上一字不差地成功。

DLL 雜湊（SHA256，給查核對檔）：
- plain `4eb9c4864804158d1958ea71918bc0ef167a675bee92a16fb9156ae375e96505`
- obf `7fe0adc384ab616cbf97079ac32afb3bef7966a3fbc323fcd3f59d7392b5ef2a`
- obf2 `0a7c5edd97a2e016371f3d1bc05967fe46f1f079cf0ee50ea875444e03729683`

## 靶二：Mokaair 正式站前端（Next.js）

`rea analyze-web-bundle`（開一個 headless Chrome 連遠端除錯，REA 被動擷取並靜態分析，不執行頁面上的 JavaScript）分析 `https://mokaair.com/zh-TW`：

- 擷取並解析 **20 支 script**，走訪 229,492 個 AST 節點，0 個解析失敗。
- 高信心判定前端框架是 **Next.js**。
- **Source map 不可得**（`status: unavailable`，0 requested）——我們上線時把 source map 關掉了，所以 REA 拿不到原始碼。另外抓下首頁 17 支 chunk 做位元組掃描，也沒有任何金鑰、token 或密鑰（只有登入表單的 `password` 字樣）。這是「做對了」的對照。
- 仍然讀得到的東西（這就是前端本質上公開的部分）：
  - 兩個高信心的 fetch 端點 `/api/travel/analytics/config`、`/api/travel/analytics/events`（含來源 script 與行列位置）。
  - 一串搜尋參數名（`window_start`、`min_days`、`nightly_max`、`adults`、`rooms`、`breakfast_required`…），REA 老實標成「低信心端點候選」，並警告這些可能是表單／儲存參數、不是真的端點。
  - 位元組掃描另外看得到前端用到的路由字樣（`/admin`、`/admin/community`）與 `is_admin` 這種前端旗標——它們只是「畫面要不要顯示管理入口」的判斷，真正的授權仍在後端。
- REA 自己寫的限制：「server-side behavior may remain unknown」「URL-shaped findings 不證明真的發出過請求」——也就是伺服器上的程式它拿不到。

## 給影片的三個落點（都來自上面量到的）

1. **放進前端／桌面二進位的東西 ≈ 公開**：原版 NoteVault 一個指令全洩；網站的 API 介面、參數、框架也都讀得出來。
2. **混淆是提高成本，不是上鎖**：它只改「多難讀」，且不一致（const vs readonly 差很大），完全不改「用戶端能不能被繞過」——三種繞過在混淆版照樣成功。
3. **真正的保護是把判斷與秘密搬到伺服器**：REA 明說伺服器端行為拿不到；Mokaair 關掉 source map、bundle 裡沒有金鑰，就是示範。

## 上線前檢查清單（草案，給撰稿收尾用）

- 授權／付費／權限判斷放伺服器，用戶端只拿「後端已經批准的結果」。
- 任何秘密（簽章密鑰、API key）不進前端 bundle、不進桌面二進位——它們遲早被倒出來。
- 正式站關掉 source map（Mokaair 已做到）。
- 後端對前端只回需要的欄位；`is_admin` 這種旗標決定不了權限，伺服器每個請求自己再查一次。
- 拿掉除錯後門與隱藏旗標（像 `NV_INTERNAL_DEBUG`），它們會跟著字串一起被看到。
- 想驗證？對你自己的產品跑一次 `npx rea-agents setup`，再讓 agent 分析它——你會看到別人會看到的東西。
