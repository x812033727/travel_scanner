# 可查核主張：三支工具同題試跑

查核日：2026-09-27。`comparison.md` 是本次第一手本機執行紀錄；`demo/` 保留起始檔案、驗收檔案與兩份實際 diff。原始 JSON／JSONL、完整測試輸出保留在 repo 外。它們是本機證據，不能冒充官方產品承諾。

| ID | 影片主張 | 依據 | 場景 |
| --- | --- | --- | --- |
| c1 | 同題試跑兩支完成，一支在登入前失敗；單次試跑不是能力排行榜 | `comparison.md`；本機 CLI 原始輸出 | opening、not-a-rank |
| c2 | 起始 `splitFareCents(100,3)` 得 `[33,33,33]`，總和 99；起始兩測試通過 | `demo/fare.mjs`、`fare.test.mjs`、`acceptance.test.mjs`；本機 `node --test` | baseline、one-hundred、old-tests |
| c3 | 三份起點與提示相同；四類驗收是三工具執行後才另寫並加入，並非事前盲測 | `comparison.md`、`demo/CHALLENGE.md`；作者確認寫作順序，本機起始複製紀錄 | fixed-input、prompt、which-version、acceptance |
| c4 | Claude Code 2.1.270 修改程式與測試；自寫 9/9，事後 4/4；核心 patch 使用商數及餘數 | `demo/claude.patch`、本機 JSON `type=result` 與測試輸出 | claude、claude-diff、two-patches |
| c5 | Codex CLI 0.158.0-alpha.2.1 修改程式與測試；自寫 5/5，事後 4/4；核心 patch 使用餘數 | `demo/codex.patch`、本機 JSONL `turn.completed` 與測試輸出 | codex、codex-diff、two-patches |
| c6 | Gemini CLI 0.61.0 以本機個人帳戶登入時回 `IneligibleTierError: UNSUPPORTED_CLIENT`，未改檔。Google 2026-06-18 起停止個人 free／Pro／Ultra 帳戶使用 Gemini CLI 的 Login with Google；企業 Code Assist 與 API 金鑰路徑仍可用。本次未測後兩者，不能據此判斷程式能力 | 本機 CLI 原始錯誤；[Google Developers 棄用說明](https://developers.google.com/gemini-code-assist/docs/deprecations/code-assist-individuals)；[Gemini CLI 團隊公告](https://github.com/google-gemini/gemini-cli/discussions/28017) | gemini、login-evidence、availability |
| c7 | 四類事後驗收含 `100/3`、餘數及零、0–500 與 1–20 的性質檢查、非法輸入；兩份 patch 全通過 | `demo/acceptance.test.mjs`；本機兩份測試輸出；`demo/claude-acceptance.png` 為真實輸出重排，來源見 `comparison.md` | acceptance、acceptance-cases、acceptance-timing、pass-table、test-output |
| c8 | Claude 輸出 `total_cost_usd=0.297987` 是工具估算值；Codex JSONL 有 token 用量但無美元帳單；這些不能推導訂閱實際扣款 | 本機原始 JSON/JSONL；[Claude CLI 參考](https://code.claude.com/docs/en/cli-reference)、[Codex CLI 文件](https://learn.chatgpt.com/docs/codex/cli) | cost、cost-caveat |
| c9 | 固定起點、提示、另寫驗收並檢查差異，是本片建議的方法，不是廠商性能事實；本次驗收並非事前盲測 | 編輯判斷；`comparison.md` | selection-sheet、choice、outro |

## 與企劃不同的地方

Gemini 本機個人帳戶不支援這次 CLI 執行，與 Google 的 2026-06 棄用政策相符。影片不做虛構的三方程式能力結論。標題明示「兩支修好，一支卡登入」。現行 [Gemini CLI 登入教學](https://geminicli.com/docs/get-started/authentication/)仍列個人帳戶，與較新的棄用公告牴觸；依具體棄用公告解釋這次結果，上架前再查政策。

## 我懷疑但沒動的事

- Gemini 企業授權或 API 金鑰登入可用性未在本機測試；未取得這類憑證，不宣稱已完成第三方比較。
- Claude `total_cost_usd` 不等於帳單；沒有讀取私人帳單，也不以現行標價推定扣款。
- 本片畫面裡的 CLI 字樣與失敗訊息仍需在上架當日覆核，避免過期。

## 進度

131 句、28 場景已寫，`lint` 零錯誤零警告；第一輪獨立查核和新增場景補查已做。Google 政策修正與新截圖場景仍待另一位查核者做第二輪；實際旁白與成片未完成。

