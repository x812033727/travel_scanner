# 第 97 篇獨立查核：claude-code-first-mod

- 對象：`docs/claude-code-series/lessons/97.md`（「建立第一個 mod：在 Claude Code 行程內數工具呼叫」）
- 查核者：獨立查核代理（Claude Opus 5.5），未參與撰稿
- 查核時間：2026-10-04（台北；UTC 2026-10-03 23:59）
- 方法：原稿拆成約 62 條主張，逐條對四頁官方文件的 Markdown 版與協調者在容器以 Claude Code 2.1.289 產生的 `validate.log`、`test.log` 核對；程式碼圍欄用 Python 與 `tools/claude-code-series/advanced/mods/first-mod/` 逐字比對。

## 重抓結果

User-Agent：`Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)`，未帶任何個人資料。

| 頁面 | URL（加 `.md`） | HTTP | bytes |
| :- | :- | :- | -: |
| Mods overview | https://code.claude.com/docs/en/plugins/mods/overview | 200 | 23225 |
| Create a mod | https://code.claude.com/docs/en/plugins/mods/create | 200 | 25270 |
| Test a mod | https://code.claude.com/docs/en/plugins/mods/test | 200 | 25561 |
| Mods reference | https://code.claude.com/docs/en/plugins/mods/reference | 200 | 27811 |

## 改掉的 20 處

| # | 原文 | 改成 | 來源原文 | 理由 |
| :- | :- | :- | :- | :- |
| 1 | 設定檔裡的 Hook 在 Claude Code 外部執行 | 設定檔 Hook 在 Claude Code 外部執行 | — | 兩種 hook 的用詞全文統一 |
| 2 | v2.1.287 or later | v2.1.287 或更新版本 | overview／create：「Mods require Claude Code v2.1.287 or later」 | 繁中正文不留英文片語，意思不變 |
| 3 | 官方文件把 mod 的事件處理函式與設定檔的 settings hook 都叫 hook | Claude Code 把兩種都叫 hook；mods 文件裡單說 hook 指 mod 的事件處理函式，設定檔那種叫 settings hook | overview Note：「Claude Code calls both kinds hooks: on these pages, "hook" means a mod's handler, and the settings-file kind is a "settings hook".」 | 原文把「Claude Code 的叫法」與「這幾頁的用法」混在一起 |
| 4 | `/plugin` 的 Installed 分頁預期列出 mod，分頁下方有 `1 mod active · first-mod` | 執行 `/plugin`，分頁列下方有一行暗色字列出數量與名稱；overview 也用這一行確認以 `--plugin-dir` 載入的範例 mod | overview「See which mods a session loaded」：「A dim line under the tabs gives the count and the names, such as `1 mod active · first-mod`.」；「Try a sample mod」：用 `--plugin-dir` 載入後「To confirm the mod loaded, check which mods the session loaded」 | create 的「Check that the mod loaded」（Installed 分頁列出 mod）屬於「Ask Claude for a mod」流程，不是 `--plugin-dir`；暗色行在分頁列下方，不是 Installed 分頁裡 |
| 5 | /tally 預期回覆次數，文字前有 `first-mod:` | 寫出文件的完整預期輸出，說明 plugin 名稱由 Claude Code 加在前面，並補「指令清單裡沒有 /tally，文件說是 module 沒載入」 | create「Try the mod」：「The transcript shows `first-mod: Claude has made 2 tool calls since this mod loaded`… Claude Code puts the plugin's name in front of the command's text.」「If `/tally` isn't in the command list, the module didn't load.」 | 讓讀者有可對照的原句與失敗判準 |
| 6 | `claude -p` 不畫介面，預期印出 0 次（寫在命令區塊之前） | 命令區塊之後寫「文件列的預期輸出是 `first-mod: Claude has made 0 tool calls since this mod loaded`」 | create 的 `claude -p "/tally" --plugin-dir ./first-mod` 範例輸出 | 「不畫介面」與「0 次」沒有因果；0 是因為這次執行沒有工具呼叫。順序也改成先命令後輸出 |
| 7 | 本站…沒跑互動 session | 沒跑互動 session，也沒跑 `claude -p`；observation.md 加記 `claude -p` 輸出 | 材料只有 validate.log、test.log | `claude -p` 也沒實測，不可留白讓人以為跑過 |
| 8 | transcript 出現 first-mod 已重載的一行 | 出現一行，說 first-mod 已重載並列出它的事件函式 | create：「A line in the transcript says `first-mod` reloaded and lists its hooks」 | 補足文件原句 |
| 9 | 跨重載保留的做法，文件指向 `$.state` | 文件指向 Draw in the interface 頁的「Keep state」一節；並補「文件說 Claude Code 會監看 `--plugin-dir` 目錄、檔案一改就熱重載」 | create：「To keep a value across reloads, see [Keep state]」；「Claude Code watches a directory loaded with `--plugin-dir` and hot-reloads the hooks module when a file in it changes.」 | 文件只指向一節，該節同時涵蓋 `$.state` 與 `$.store`，四頁沒有說 `$.state` 會跨重載保留 |
| 10 | 對 manifest 與 hooks module 做載入時同一套靜態分析 | 檢查 manifest，並對 hooks module 的原始碼跑載入時的同一套靜態分析 | create：「It checks the manifest and runs the same static analysis on the hooks module's source that Claude Code runs when it loads a mod.」 | 靜態分析只針對 hooks module |
| 11 | 已在本課材料上執行過（符號與文件範例不同） | 本站在容器以 2.1.289 執行過；行首符號是 `>` 與 `√`，文件範例是 `❯` 與 `✔`，其餘文字相同 | validate.log 與 create 範例逐行比對：換掉符號後三行完全相同 | 寫明差在哪、版本是哪個，不推測原因 |
| 12 | 事件沒列在第一行，Claude Code 就不會呼叫它；拼成 `tool.calls` 會報… | 加「文件說」，改為「也不會呼叫那個事件函式；常見原因是事件名拼錯，例如…」；「規則如下」改「文件列的規則」 | create：「If an event you meant to handle is missing from the first line, Claude Code won't call that hook either. The usual cause is a misspelled event name, which the command reports as an error such as `"tool.calls" is not an event`.」 | 錯誤訊息本站沒實測，要標成文件說法 |
| 13 | 只用相對路徑匯入目錄內的檔案，唯一的裸匯入是 `claude-code`；寫成 ES module，不用 `require` | 匯入 plugin 目錄內的檔案，唯一「允許」的裸匯入；用 `import` 不用 `require` | create：「Import only from files inside the plugin directory, by relative path. The one bare import allowed is `claude-code`」「with `import` and not `require`」 | 貼近原文 |
| 14 | 載入時 Claude Code 會把…`.d.ts` 寫進 `.claude-plugin/types/`，文件說與頁面不一致時以它們為準 | 文件說每次以 `--plugin-dir` 載入或重載 mod，會寫進 mod 目錄的 `.claude-plugin/types/`；與任何頁面不一致時以它們為準 | create：「Each time Claude Code loads or reloads a mod from a directory you pass to `--plugin-dir`, or a mod Claude wrote for you, it writes … into `.claude-plugin/types/` inside the mod's directory」「trust these files over any page, this one included」 | 原句把文件說法寫成事實，條件也不完整；本站沒看到這個目錄被產生 |
| 15 | 測試的 `$` 扮演 Claude Code | 加「不是事件函式拿到的 mods API：它的每個方法觸發同名事件並送進 mod 的事件函式」 | test：「the test's own `$`, which acts as Claude Code. It isn't the mods API that a hook receives. Each of its methods fires the event of the same name, sends it through your mod's hooks」 | 前文剛說 `$` 是 mods API，不講清楚會混淆 |
| 16 | （無） | 測試輸出前加「文件說耗時每次不同，所以括號裡的時間與文件範例不一樣」 | test／create：「with timings that vary from run to run」 | 容器 72.16ms／0.32s 與文件 22.87ms／0.19s 不同，先說明 |
| 17 | 測試沒有觸發 `session.start`，所以 /tally 並未註冊卻仍通過 | 文件說測試裡 `session.start` 不會自己執行，`$.command.run` 直接送進 `command.run` 事件函式；因此這個測試沒有經過 `$.command.register`，通過不代表 /tally 已出現在指令清單 | test：「`session.start` doesn't run by itself. Each test starts with your module freshly loaded and none of its hooks called」；「`$.command.run` then went to the mod's `command.run` hook」 | 原文把推論寫成事實；改成「文件說…；因此…」 |
| 18 | 只從信得過的作者安裝 | 只從信得過的作者與 marketplace 安裝 | overview：「Install mods only from authors and marketplaces you trust.」 | 漏了一半 |
| 19 | 文件說事件函式要碰到自己以外的東西，只能呼叫 mods API | 文件說，事件函式要在自己的程式碼之外做任何事，例如畫面、加指令、呼叫模型、讀檔、啟動程式或發網路請求，都得呼叫 mods API，沒有別的途徑，所以 Claude Code 能在安裝前列出 mod 做什麼 | overview：「To do anything outside its own code, such as draw, add a command, call a model, read a file, start a process, or make a network request, a hook calls the mods API. A hook has no other way to do those things, which is why Claude Code can list what a mod does before you install it.」 | 「碰到自己以外的東西」太模糊，改成文件的範圍與理由 |
| 20 | 前兩項本站在容器驗證過…，後兩項是文件預期 | 熱重載一項是文件預期 | — | 完成判準只有三項，「後兩項」數錯 |

另有一處小改：protected path 一句前加「文件說」（create：「A directory you load with `--plugin-dir` is a protected path, so in `default` and `acceptEdits` modes you're asked to approve each of Claude's edits to the mod.」）；小練習補上預期 0 次的依據（test：「Each test starts with your module freshly loaded…, so module-level variables hold their initial values.」），跨平台排錯連結改寫成只針對同一個 plugin 裡的設定檔 Hook，不暗示它能解 mod 載不起來的問題。

## 查過而且正確的部分

- 四個程式碼圍欄（plugin.json、hooks.json、register.js、first-mod.test.ts）與 `tools/claude-code-series/advanced/mods/first-mod/` 及 `/root/news411/modlab/first-mod/` 逐字相同；兩份材料彼此也相同。register.js 與測試檔與 create／test 頁的程式碼相同，plugin.json 只把 author 從「Your Name」換成「Mokaair tutorial」。
- 「改一行字」區塊：等於材料 register.js 那一行把 `' · tool calls: '` 換成 `' · tools used: '`，縮排與 create 頁的 highlighted line 相同。
- 驗證輸出節錄三行逐字出現在 validate.log；測試輸出區塊與 test.log 完全相同。
- 13 個圍欄第一行都是「語言 空格 標籤」。
- 正確的主張（舉要）：mod 是多了 hooks module 的 plugin；觀察／改寫／接手三種處理；`modules` 只放一個相對路徑、有它才算 mod；manifest 沒有額外必填欄位；`register(on)` 的 `$`、`e`（deeply frozen）、`next`；matcher `{ command: 'tally' }`；`--plugin-dir` 只載入一次 session、不安裝；`Thinking · tool calls: 2…` 與 `Thinking · tools used: 1…`；重載會再執行 `register`、`calls` 歸零；`hooks:`／`calls:` 兩行的意思；`$.ui is used as a value` 與 `the event name passed to on() is not a string literal`；測試檔 `.test.ts`；stub 要在第一次呼叫 `$` 前登記；no `ls` ran；失敗時狀態 1；mod 能觸及的範圍與不在沙盒；README 寫測試版本。
- 撰稿者疑點裁決：
  - a. 暗色行 `1 mod active · first-mod` 適用於 `--plugin-dir`（overview 的 sample mod 段落明確這樣用）；「Installed 分頁列出 mod」是 create 對 Claude 寫的 mod 的說法，已刪。
  - b. 原意忠實但太模糊，已改成文件的範圍與理由（第 19 處）。
  - c. 原文把推論寫成事實，已改成「文件說…；因此…」（第 17 處）。
  - d. 符號差異的敘述正確、不誇大；已寫明是哪兩組符號、其餘文字相同，不推測原因（第 11 處）。
  - e. 日期一致：正文 2026-10-04 與材料（log 修改時間 UTC 10-03 23:48＝台北 10-04 07:48）及內容包 sources 的 checked_on 一致。
- 界線：沒有購買或訂閱建議；沒有 Claude Marketplace；原稿「本文」0 次；站內連結 4 條都在允許清單內且內容包存在；以 OpenCC s2t 逐字掃，只有「准」（核准）與「台」（別台）被標出，兩者都是台灣正體慣用字，沒有簡體字。
- 兩種 hook 用詞：「設定檔 Hook」與「mod 的事件函式」（或簡稱「事件函式」）全文一致；「hooks module」「hooks.json」「hooks: 行」是檔名或專有詞，保留。

## 留給站主的事

1. `claude --plugin-dir` 的互動 session（spinner 計數、/tally、`/plugin` 暗色行）、熱重載那一行、`claude -p "/tally"` 都沒有實測，正文已標成文件預期；若要升級成實測，需要登入的 Claude Code 2.1.287 以上跑一次並保存原文。
2. 容器輸出用 `>`／`√` 而文件用 `❯`／`✔` 的原因未查（可能是終端機或字型），正文只陳述差異。
3. 本篇不需要也沒有寫 `cleanupPeriodDays`、Installed 分頁；故障練習的兩個錯誤訊息本站沒有實際觸發過，正文寫「預期」。
4. 產生器會在內容包加上「驗證範圍」callout（含一次「本文」）與「回 Claude Code 教學總目錄」（`claude-code-tutorials`）連結；這是產生器樣板，不在原稿，請協調者確認符合本組允許的連結規則。
5. 原稿改完未重跑產生器；`claude-code-first-mod.json` 需由協調者重產。

## 結論

`ok`：程式碼與實測輸出逐字正確；文字面的 20 處已改到四頁原文與材料撐得住的說法，剩下的是需要登入 session 的實測，正文已標成文件預期。
