# claims：rea-reverse-engineering-protection

大綱：選項 A（站主對自己軟體開刀，收在防守清單）。製作路線：教學卡片，`format: "slides"`，沒有 `shot`、沒有翻譯檔。全片分析的目標都是自有：自寫的 NoteVault 與自家 Mokaair 正式站；所有秘密皆為假測試值。尚未經獨立代理查核（`verify-1.md` 待做）。

寫法：`c 編號｜主張（旁白或畫面上的說法）｜依據｜查核日｜用到的場景`。

簡寫：`RUN` = `docs/videos/rea-reverse-engineering-protection/runlog.txt`；`SRC` = `docs/videos/rea-reverse-engineering-protection/test-target/NoteVault.cs`；`REA` = 官方 `https://github.com/morluto/rea`（README）。卡片上的終端機輸出與程式碼，取自 RUN 與 SRC，非手打。

會過期的事實（錄製日重核）：星數與時間軸（`https://github.com/morluto/rea`、`https://star-history.com/#morluto/rea&Date`）、安裝指令與支援 agent（REA README）、REA 版本（`npx rea --version`）。

## 主張

- c01｜REA 全名 Reverse Engineer Anything，是一個把逆向分析工具接給 AI agent 的 MCP｜REA README 標題與說明｜2026-10-16｜open, what-rea
- c02｜REA 星數在 2026-10-16 約 28 萬（讀到 276,024 星、69,538 fork）｜`gh api repos/morluto/rea`｜2026-10-16｜open, stars
- c03｜報導稱 REA 2026-10-06 不到一萬星、10-12 破十萬、10-11 單日增三萬多｜dev.to/kdnuggets 報導（第三方，進稿前重核 star-history）｜2026-10-16｜stars
- c04｜官方提醒只能從 morluto/rea、rea.tools、npm 套件 rea-agents 取得，名字相近的 repo 不算官方｜REA README IMPORTANT 區塊｜2026-10-16｜trust
- c05｜REA 分析在本機跑、不上傳程式；DISCLAIMER 限分析自己擁有或被授權的軟體｜REA README FAQ「Does REA upload my app?」與 DISCLAIMER｜2026-10-16｜trust
- c06｜安裝是一行 `npx rea-agents setup`，支援 Claude Code、Codex、Cursor、Gemini CLI 等｜REA README Quick start｜2026-10-16｜install, trust
- c07｜本次用的 REA 版本是 6.5.0｜RUN [B2]｜2026-10-16｜install
- c08｜NoteVault 是自寫的約 80 行 C# 程式（原始碼 79 行），模擬有 Pro 付費功能的筆記 App｜SRC｜2026-10-16｜note-app, three-bugs
- c09｜它故意犯三個錯：授權用寫死密鑰在用戶端算、NV_INTERNAL_DEBUG=letmein 後門、region=EDU 隱藏折扣打六折（NT$150→NT$90）｜SRC 第 39、25、69 行附近｜2026-10-16｜three-bugs, license-code
- c10｜原版預設執行印出版本與月費 NT$150｜RUN [B1]｜2026-10-16｜note-app
- c11｜一個 REA 指令 inspect-managed-members 靜態（不執行程式）就倒出全部 23 個字串常數，三個秘密全中｜RUN [B3]｜2026-10-16｜rea-strings, strings-out
- c12｜看 .NET DLL 明文字串，最簡單用 strings 指令或文字檢視器就行，原版這樣就看得到密鑰｜一般工具知識；RUN [B3] 證明字串確實在檔內｜2026-10-16｜simple-way
- c13｜REA 比 strings 多做的是：讓 agent 順授權邏輯算出合法 key、實際解鎖 Pro｜RUN [B6] bin-plain｜2026-10-16｜forge-key, forge-steps
- c14｜偽造 key NV-123456-78F56FB4 由密鑰 HMAC 自算而得｜SRC License.Check；RUN [B6]｜2026-10-16｜forge-steps
- c15｜混淆版 inspect-managed-members 的字串堆為 0（HideStrings 清空）｜RUN [B4]｜2026-10-16｜obf-strings
- c16｜混淆藏字串不一致：秘密是 const 時明文仍殘留檔內，readonly 才真的消失｜RUN [B5]｜2026-10-16｜obf-inconsistent
- c17｜三種繞過（偽造 key、後門、隱藏折扣）在混淆版照樣成功｜RUN [B6]、[B7]｜2026-10-16｜obf-bypass, bypass-table
- c18｜原因是授權判斷跑在使用者的機器上，混淆只改可讀性｜SRC License.Check 在用戶端；RUN [B6] 推論｜2026-10-16｜why-clientside
- c19｜REA 對正式站 analyze-web-bundle 解析 20 支 script、229,492 個 AST 節點、0 失敗，判出 Next.js｜RUN [W1]｜2026-10-16｜web-run
- c20｜正式站 source map 不可得（REA requested=0, unavailable），bundle 無金鑰｜RUN [W1]；首頁 chunk 掃描無金鑰｜2026-10-16｜web-run, web-good
- c21｜前端仍可讀：兩個 fetch 端點 /api/travel/analytics/config、/api/travel/analytics/events｜RUN [W1]｜2026-10-16｜web-visible
- c22｜REA 自述限制「server-side behavior may remain unknown」｜RUN [W1]；REA 輸出 limitations｜2026-10-16｜web-boundary, boundary
- c23｜防守做法：授權／付費／權限判斷與秘密放伺服器，前端只收已批准結果｜SRC 對照（反例）；一般安全原則｜2026-10-16｜fix-code, checklist
- c24｜改法示範：把 License.Check 從用戶端算改成只問伺服器；密鑰不在程式裡，偽造 key 無從通過（設計推論，未建伺服器實跑）｜SRC（反例）；設計說明｜2026-10-16｜fix-code
- c25｜上線前清單：秘密不進前端／二進位、正式站關 source map、後端只回必要欄位、拔除錯後門｜RUN 各項對應一個實測失敗｜2026-10-16｜checklist
