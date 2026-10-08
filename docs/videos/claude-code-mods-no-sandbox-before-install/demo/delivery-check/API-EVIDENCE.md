# API 選擇紀錄

查核：2026-10-09。僅讀取公開官方文件及型別，沒有啟動 Claude CLI、安裝、載入 Mod 或呼叫模型。原生驗證仍待完成。

## 檔案判斷

[官方型別](https://github.com/anthropics/claude-code/blob/684800b206824dfd0cc8a876e8604b20f72c3617/mods/types/claude-code.d.ts) 的 `fs.exists` 回傳布林值，描述只有網路位置會拒絕；因此不將它的 `false` 當作足以區分缺少與存取錯誤的證據。

選用 `$.fs.stat(path, options?)`。其結果是 `FsStat`，有 `kind`、`size`、`mtimeMs`、`isLink`；`kind` 可為 `file`、`dir` 或 `other`。型別描述缺路徑以 ENOENT 拒絕、OS 拒絕帶 errno，但沒有指定捕捉的錯誤物件形狀。本版僅辨識明確 `error.code`；其他情況保守回傳無法檢查，不解析任意錯誤文字。

絕對路徑依原樣交給主機；不把 Windows 反斜線當跳脫字元。範例另限制為本機絕對路徑，拒絕 UNC／裝置路徑。符號連結與其他模組攔截仍是主機行為，並非安全邊界保證。

## 指令與面板

[API 指南](https://code.claude.com/docs/en/plugins/mods/api#add-a-command)：從 `session.start` 註冊命令；`command.run` 的 `e.args` 是命令之後的整段文字，因此本程式自己去掉成對引號，不使用 shell 解析。指令回傳空物件，不提交模型提示。不開 `immediate`，故不承諾在 Claude 忙碌時立即執行。

[介面指南](https://code.claude.com/docs/en/plugins/mods/interface)：以 `$.ui.open` 開啟帶固定 ID 的面板；`ui.render` 同時核對 `Pane` 與自己的 `requestId`。`$.ui.resolve(e)` 的 `Box`、`Text`、`Button` 可直接以函式產生元素樹，毋須 JSX。按鈕有唯一 key，回呼手動刷新，完成後 invalidate；繪圖只讀取上次狀態。

指南與上述固定版本型別有一處差異：指南描述 open 回傳放置資訊；固定型別卻宣告 `Promise<void>`，`isPlaced` 位於 `$.ui.panes()` 的項目。本版採兩者共同可用的呼叫方式，只等待 open 完成，不讀取其回傳值、不因此宣稱畫面已出現。實際顯示仍需原生錄影核對；若未來需要放置狀態，先核對執行版本提供的型別。

## 模組限制

[建立指南](https://code.claude.com/docs/en/plugins/mods/create) 要求靜態相對匯入、明寫事件名稱及完整 API 呼叫。`$` 可傳給同檔頂層函式，不能傳入匯入函式。因此主機接線保留在 `register.mjs`，純邏輯模組只收資料。入口採 ES module，不用 Node、動態匯入、第三方套件或 JSX。

`session.end` 清除記憶；重載由新的模組狀態開始。較晚的刷新或換資料夾使先前未完成結果失效，避免舊資料夾結果覆蓋新的畫面。

## 證據界線

原始碼及普通 Node 的純函式測試，最多支持資料解析和判斷邏輯。它們不證明 Claude 的靜態分析器接受此程式、原生錯誤保留 code、按鈕可使用、畫面排版正確或實際查詢成功。需在允許的環境另行取得對應版本的驗證與操作紀錄，才可更新這些狀態。
