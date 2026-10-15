# Claude Code Mods 改寫稿查核表

確認日期：2026-10-09（Asia/Taipei）。本表支援本機改寫稿，不證明影片或 Mod 已完成實測。

| ID | 稿件主張／邊界 | 當日第一手來源 | 判定 |
| --- | --- | --- | --- |
| m01 | Mod 以事件處理函式改變 Claude Code 行為或介面；本案例在 spinner 顯示工具呼叫次數。 | [Mods overview](https://code.claude.com/docs/en/plugins/mods/overview#how-a-mod-works) | 官方文件事實 |
| m02 | 官方 first-mod 在 tool.call 一進來就加一，再交給 next；因此數的是模組載入後累積收到的事件，不是成功次數、完成任務數或帳單。0→1→2 只用作示意，呼叫失敗仍可能已被計數。 | [Create a mod](https://code.claude.com/docs/en/plugins/mods/create#write-a-mod-yourself) 的 register.js；[Mods overview](https://code.claude.com/docs/en/plugins/mods/overview#how-a-mod-works) | 原始碼可直接推得；成功與費用的區別屬明示解讀 |
| m03 | 官方 first-mod 教學由 manifest、hooks.json、register.js 三個檔案組成；modules 的路徑相對於 hooks.json；現有手寫教學含完整計數／查詢程式。 | [Create a mod](https://code.claude.com/docs/en/plugins/mods/create#write-a-mod-yourself) | 官方文件事實；本機演示未執行 |
| m04 | 圖中的模型提出工具需求，Claude Code 負責事件與工具執行，Mod 回應事件並可繪製介面。 | [Mods overview](https://code.claude.com/docs/en/plugins/mods/overview#how-a-mod-works)、[Use the mods API](https://code.claude.com/docs/en/plugins/mods/api#add-a-command-or-a-tool) | 針對本案例的簡化流程；不是完整 permission／middleware 圖 |
| m05 | hook 可觀察後交回、改寫後交回，或自己回答而不呼叫 next。官方計數器的四個事件為 session.start、tool.call、command.run、ui.render。 | [Create a mod](https://code.claude.com/docs/en/plugins/mods/create#how-the-example-mod-works) | 官方文件事實 |
| m06 | tally 是使用者 command；handler 直接回傳計數文字，不呼叫模型。剛載入且沒有事件時為 0。 | [Use the mods API](https://code.claude.com/docs/en/plugins/mods/api#add-a-command)、[Create a mod](https://code.claude.com/docs/en/plugins/mods/create#write-a-mod-yourself) | 範例程式與官方預期；不是本機輸出 |
| m07 | Mod 以使用者權限執行，可讀寫檔案、啟動程序、連網、讀對話並使用模型額度；只應載入信任來源。 | [Mods overview](https://code.claude.com/docs/en/plugins/mods/overview#what-a-mod-can-reach)、[Plugin security and trust](https://code.claude.com/docs/en/plugins/security#understand-what-a-plugin-can-do) | 官方文件事實 |
| m08 | 模組的 JS 執行環境沒有 DOM／Node，對外能力透過 $；這與 Bash sandbox 安全隔離不同。Mod 自己啟動的程序在 Bash sandbox 外。 | [官方部落格](https://claude.dev/blog/getting-started-with-claude-code-mods/)、[Plugin security and trust](https://code.claude.com/docs/en/plugins/security#understand-what-a-plugin-can-do) | 兩頁用語範圍不同，不可化約成「完全沒有任何沙盒」 |
| m09 | plugin validate 分析 manifest 與模組原始碼、不啟動 session、不執行模組；列出 hooks/calls。它不是惡意程式安全認證，也不是 runtime／視覺驗證。 | [Create a mod](https://code.claude.com/docs/en/plugins/mods/create#check-what-claude-code-reads-from-your-mod) | 官方功能＋驗證邊界；不宣稱本機跑過 |
| m10 | 目前官方 terminal 的最低版本為 2.1.287；影片未展開 Desktop 的不同門檻。 | [Mods overview](https://code.claude.com/docs/en/plugins/mods/overview#turn-mods-on-or-off) | 當日數字；未用示意版本號代替 |
| m11 | 本機唯讀 claude --version 回覆 2.1.285；另備妥隔離的 2.1.293 CLI，但後續執行被自動審查阻擋。兩者都沒有被描寫成成功 runtime 演示。 | 2026-10-09 本機命令收據；repo 外研究 FACTS-AND-DEMO.md；主協調者 STATUS | 實讀事實，不是官方來源 |
| m12 | --plugin-dir 載入資料夾只用在該 session；不等於 permanent plugin install。/plugin 可核對 Installed 清單與啟用狀態。 | [Create a mod](https://code.claude.com/docs/en/plugins/mods/create)、[Mods overview](https://code.claude.com/docs/en/plugins/mods/overview#see-which-mods-a-session-loaded) | 官方文件事實 |
| m13 | 指令不存在時應核對 mod 是否載入；版本、路徑、檔案與停用設定都是適用排查項目。 | [Create a mod](https://code.claude.com/docs/en/plugins/mods/create#write-a-mod-yourself)、[Mods overview](https://code.claude.com/docs/en/plugins/mods/overview#turn-mods-on-or-off) | 官方前提；排查順序為編輯建議 |
| m14 | 讓模型列檔讀檔會進入模型工作回合；本次沒有執行此回合。計數器的直接 command 不等同模型 prompt。 | [Create a mod](https://code.claude.com/docs/en/plugins/mods/create#write-a-mod-yourself)、[Use the mods API](https://code.claude.com/docs/en/plugins/mods/api#call-a-model) | 用量界線；不報未查核價格或方案 |
| m15 | --plugin-dir 監看變更並 hot reload；模組層 calls 變數隨重新載入歸零，需跨 reload 保留時另用 state。 | [Create a mod](https://code.claude.com/docs/en/plugins/mods/create#how-the-example-mod-works)、[官方部落格](https://claude.dev/blog/getting-started-with-claude-code-mods/) Step 3 | 官方文件事實；3→0 是示意 |
| m16 | 停用／卸載 Mod 用 plugin 管理；單次載入結束後，下次不帶參數就不經該路徑載入。若曾永久安裝則需另外停用。 | [Mods overview](https://code.claude.com/docs/en/plugins/mods/overview#turn-mods-on-or-off)、[Create a mod](https://code.claude.com/docs/en/plugins/mods/create#use-the-mod-in-other-sessions) | 範圍明確；不保證使用者不存在其他載入來源 |
| m17 | 一般 terminal 與 Desktop Code tab 可畫 Mod UI；claude -p 的 hooks 可執行但無互動 UI。 | [Mods overview](https://code.claude.com/docs/en/plugins/mods/overview#where-mods-run) | 官方文件事實；Desktop WSL 例外未列在主片概括中，畫面應標一般桌面版 |
| m18 | plugin test 不需 session、登入或網路；模型／工具用 stub；UI tree 測試不證明實際像素呈現。 | [Test a mod](https://code.claude.com/docs/en/plugins/mods/test#write-a-test)、[Test a drawing](https://code.claude.com/docs/en/plugins/mods/test#test-a-drawing) | 官方能力；本機 CLI 測試未執行，不得貼 pass 輸出 |
| e01 | 用乾淨資料夾與自製文字，讓測試範圍與比較更清楚。 | 編輯建議 | 意見；不是安全隔離保證 |
| e02 | 不把兩次當固定成功門檻，計數自載入起累積，核對當次工作時用前後差值對照該次收到的工具事件。 | 依 m02 的觀察指標推導 | 編輯測試判準 |
| e03 | 從單一需求開始，先學會最小範例再擴充。 | 站主改善方向／編輯建議 | 意見 |

## 本次證據紀錄

- 當日閱讀六個 sources 所列官方頁；blog、overview、security、test 另外以指定 Mokaair-editorial User-Agent GET，HTTP 200。
- 本機實讀版本 `2.1.285 (Claude Code)`；`--plugin-dir` 與 `validate` 可在 help 看到；plugin help 未列出 test，不據此斷言不存在。
- 未執行範例模組、未增加 model request、未更新設定或帳號狀態。
- 主協調者另備妥隔離的 2.1.293 CLI；嘗試 validate/test 被 automatic approval review 擋下，原因 `blocked by policy`；未重試。影片稿不把此限制包裝成完成測試。
- 公開文件畫面、原創說明圖、操作命令、預期結果、本機版本實讀分別標示；不製造假的 terminal stdout。

## 改掉原版的誤導風險

- 標題與開場不再用沒有範圍限定的「沒有沙盒」。
- 不再把發表日、版本比較與風險擠在觀眾還沒看懂功能的前段。
- 刪除機車／自助餐／沙坑等多套類比，改成固定角色圖與計數器。
- 未沿用原片 approvals、音訊驗證、成片完成或發布狀態。

獨立審稿修正：mc003 區分 Mod 與它畫出的文字；mc029 明寫載入後累積；mc106／mc108 用前後差值核對；mc060 明確指向 Claude Code 的指令執行沙盒，畫面仍明列 Bash。原本的本機版本停工卡換成通用版本檢查示例，不再讓製作中斷佔據教學主線。
