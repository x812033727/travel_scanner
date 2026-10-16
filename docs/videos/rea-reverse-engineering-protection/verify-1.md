# verify-1：rea-reverse-engineering-protection（round 1, 2026-10-16）

獨立查核，非撰稿人。可編輯 `video.json`、`claims.md`，本檔為查核報告。未跑 git。
外部事實用 `gh api`（REA repo / README）核；內部 RUN 事實比對 `runlog.txt`（RUNLOG.md 為敘事）與 `test-target/NoteVault.cs`、`obfuscar.xml`。不能重跑（本機無 .NET/REA）。

## 主張對照表

| # | 主張 | 出處（line id / scene.data） | 來源 | 狀態 | 裁決 | before → after |
| --- | --- | --- | --- | --- | --- | --- |
| c01 | REA＝Reverse Engineer Anything，一個把逆向工具接給 agent 的 MCP | open l001-l002；stars | README 行6/8/63（gh api readme） | 200 | CONFIRMED | — |
| c02 星數 | 讀到 273,541 星、68,822 fork | stars.data.stats[0].note；l001；l007；claims c02 | `gh api repos/morluto/rea` | 200 | CHANGED | 273,541→**276,024** 星、68,822→**69,538** fork |
| c02 四捨 | 旁白／卡片「約 27 萬」「二十七萬」 | stars.value；l001；l007 | 同上（276,024 進位到 28 萬） | 200 | CHANGED | 27 萬→**28 萬**（跟隨星數漂移的依賴值） |
| c03 | 10-06 不到一萬、10-12 破十萬、10-11 單日 +3 萬 | stars.data.stats[1]；l001「十天從不到一萬」；youtube.title「一週破十萬星」 | dev.to／kdnuggets（第三方）；star-history 為渲染圖 | — | NOT CONFIRMED（第三方） | 不改（卡片已標「報導」、brief 已註第三方）；README 僅證實「250,000 stars」里程碑，無法由權威來源核日期 |
| c04 | 官方只認 morluto/rea、rea.tools、npm rea-agents；抄名字／抄 README 不算官方 | install l00w | README 行29-33 IMPORTANT | 200 | CONFIRMED | — |
| c05 | 分析在本機跑、不上傳程式；DISCLAIMER 限自有／授權軟體 | install l00v；outro | README 行63、FAQ「Does REA upload my app?」行304、Disclaimer 行368 | 200 | CONFIRMED | — |
| c06 | 安裝 `npx rea-agents setup`，支援 Claude Code、Codex、Cursor、Gemini CLI | install.command/output；l00s-l00t | README 行82、88 | 200 | CONFIRMED | 卡片 output 與 README 行84 一字對得上 |
| c07 | REA 版本 6.5.0（RUN 事實） | install.tool_version；strings-out | runlog.txt [B2] | n/a | CONFIRMED（符 runlog） | — |
| c08 | NoteVault 是自寫的「90 行」C# 程式 | note-app；l00g；claims c08 | NoteVault.cs（實測 79 行） | n/a | CHANGED | 九十行→**八十行**（原始碼 79 行） |
| c09 | 三錯：寫死密鑰用戶端算、NV_INTERNAL_DEBUG=letmein 後門、region=EDU「四折」 | three-bugs；license-code；bypass-table；claims c09 | NoteVault.cs 行39/25/69（註解寫「40% discount」） | n/a | CHANGED | 「四折」→**「六折」**：NT$150→NT$90 ＝打六折（付 60%、即 40% off）；「四折」會是 NT$60，與檔案不符 |
| c10 | 預設執行印 1.4.2 與月費 NT$150 | note-app.output；l00h | runlog.txt [B1]；NoteVault.cs 行67/76 | n/a | CONFIRMED | 卡片 output 與 [B1] 完全相同 |
| c11 | 一指令 inspect-managed-members 靜態抽出全 23 字串常數，三秘密全中 | strings-out；l00x-l00z | runlog.txt [B3] | n/a | CONFIRMED | 卡片為 [B3] 之節錄（省略路徑與 --filter 旗標），相符 |
| c12 | 「strings 也看得到明文」框架誠實，REA 價值在繞過／混淆而非看字串 | simple-way | runlog.txt [B3][B5]；一般工具知識 | n/a | CONFIRMED | — |
| c13/c14 | 讀密鑰→照算法算→拼出 NV-123456-78F56FB4、Pro activated. | forge-steps；forge-key；l017-l01b | runlog.txt [B6]；NoteVault.cs License.Check（本機重算 HMAC-SHA256("...","123456") 前8碼＝78F56FB4） | n/a | CONFIRMED | 偽造 key 值與「Pro activated.」皆符 |
| c15 | 混淆版字串堆＝0（HideStrings） | obf-strings「literal count: 0」 | runlog.txt [B4]；obfuscar.xml 行7 HideStrings=true | n/a | CONFIRMED | — |
| c16 | const 版混淆後明文殘留、readonly 版消失 | obf-inconsistent | runlog.txt [B5]；RUNLOG.md offset 4838 | n/a | CONFIRMED | — |
| c17/c18 | 三種繞過在混淆版照樣成功；因判斷在用戶端 | bypass-table；l01m-l01q；outro | runlog.txt [B6][B7]；NoteVault.cs（Check 在用戶端） | n/a | CONFIRMED | 表格三列「成功／成功」與 [B6][B7] 相符（「四折」字樣已改六折） |
| c19 | analyze-web-bundle：20 支 script、229,492 AST 節點、Next.js | web-run；l01t | runlog.txt [W1] | n/a | CONFIRMED | 旁白「二十二萬個節點」為 229,492 的無條件捨去（進位為 23 萬）；在容忍內，未改，見備註 |
| c20 | source map 不可得（requested=0）、bundle 無金鑰 | web-good；l01w-l01x | runlog.txt [W1]；RUNLOG.md 首頁 chunk 掃描 | n/a | CONFIRMED | — |
| c21 | 兩個 fetch 端點 /api/travel/analytics/config、/events | web-visible；l01y | runlog.txt [W1] | n/a | CHANGED（卡片對齊） | 第二端點 /events→**/api/travel/analytics/events**（與 [W1]、claims c21 一致） |
| c22 | REA 自述限制「server-side behavior may remain unknown」 | boundary；l021-l023 | runlog.txt [W1] | n/a | CONFIRMED | quote 與 [W1] 一字相符 |
| c23/c24 | 防守：授權搬伺服器；fix-code 改法示範、重跑確認偽造 key 失效 | fix-code；l024-l026 | 設計說明（NoteVault.cs 反例） | n/a | 部分（見備註） | 概念正確；但 l026「改完重跑…過不了了」在 runlog 無對應 [B8]，無法查核該次執行 |
| c25 | 上線前五條清單 | checklist；l027-l029；youtube.description | RUNLOG.md 清單（各對應一個實測失敗） | n/a | CONFIRMED | 影片全片一致為「五條」；brief 草稿曾寫「六條」（brief 不可編輯，僅回報） |

## 摘要

- 外部事實今日讀數（會過期）：`gh api repos/morluto/rea` 2026-10-16 讀到 **276,024 星 / 69,538 fork**（草稿為 273,541 / 68,822，已漂移）；README 星史里程碑「250,000 stars」。安裝指令、支援 agent、DISCLAIMER、「只認官方 repo」皆仍符 README（2026-10-16）。
- c03（10-06/10-12/10-11 時間軸、「一週破十萬」）為第三方報導，無權威來源可核，維持「報導」標註，進稿前仍須以 star-history 再看一次。
- c14 偽造 key 本機重算 HMAC 得 78F56FB4，與 NV-123456-78F56FB4 相符。
- 卡片 vs runlog/原始碼：note-app、strings-out、forge-key、boundary 的終端機／引文皆對得上 runlog；install output 對得上 README。
- 已改（事實）：星數 273,541→276,024、fork 68,822→69,538、約 27 萬→28 萬（旁白＋卡片）；「九十行」→「八十行」（原始碼 79 行）；折扣「四折」→「六折」（NT$90 是打六折，非四折）；web-visible 第二端點補全為 /api/travel/analytics/events。
- 疑似但未改：旁白 l01t「二十二萬個節點」對 229,492 是無條件捨去（進位應為 23 萬），屬口語容忍範圍且非卡面硬數字，僅回報；RUNLOG.md／runlog.txt（不可編輯）亦以「四折」描述 NT$90，同一用語錯誤，無法在本輪修正。
- 過度宣稱／待站主確認：c24 l026「改完重跑，偽造 key 就過不了」宣稱一次執行，runlog 無該筆紀錄（fix-code 的 api.Post("/license/verify") 是示意端點、NoteVault 本身無伺服器）；邏輯成立但該「重跑」無證據，請站主確認是否真的跑過，否則宜改為設計說明語氣。
- 意見 vs brief：站主觀點（混淆／編譯只是提高門檻、真正的鎖在伺服器）與 stance/outro 一致，無衝突。brief 草稿寫「六條清單」、影片定為「五條」，屬草稿與成稿差異，非事實錯。
- 聽覺檢查：無句子超過 40 字；無「經查證／根據官方文件／本影片」等查核腔；旁白無括號、無 URL；Latin 術語皆為本題目標受眾的既有技術名詞（REA、App、AI、Ghidra、Mokaair、NoteVault、Claude Code、Codex、strings、const、readonly、Next.js、source map、API、Pro activated），屬預期；四條 loop 的 payoff 皆在其 setup 之後，無提前揭曉（開場 l005 揭曉為 brief 指定的冷開場鉤子）。
- Lint：`node tools/video/cli.mjs lint`（借 node_modules junction 後跑、跑完移除）＝ **0 errors, 0 warnings**；估 8.5 分、89 行。
- 第二輪：**需要**。本輪事實變更 ≥ 4 筆（星數、fork、四折→六折、九十→八十行，另＋四捨與端點對齊），超過 3 筆門檻；且 c24「重跑」一項待站主確認、c03 時間軸仍待進稿前以 star-history 再核。
