# 第 56 篇：手動摘要來源初查

查證日期：2026-09-15。以下是 Codex 直接讀取官方頁面後的 AI 初查，不是獨立人工簽核。完整實際回答與六個可點連結存於 [manual-response.json](manual-response.json)，不改寫原回答。

## 日期、內容與適用條件

1. [Windows 桌面應用程式公告](https://workspaceupdates.googleblog.com/2026/09/the-gemini-desktop-app-is-now-available-for-Windows.html)：頁面發布日為 9 月 11 日，Windows 10／11、Alt + Space、Gmail／Drive 與圖片生成等摘要要點有依據。原回答列出的 Workspace、Individual 與個人帳號條件吻合。這也表示不能沿用「Windows 只有網頁版」的舊結論；本系列第 04 篇原稿已區分新版原生入口。
2. [Android Sheets 公告](https://workspaceupdates.googleblog.com/2026/08/gemini-in-google-sheets-is-now-available-on-Android-devices.html)：**網址路徑是 08，頁面發布日卻是 9 月 10 日**，應採頁面日期。摘要的數據問答、見解與圖表有依據，方案條件吻合；但原回答漏了「9 月 9 日起最多 15 天逐步推出」，以及複雜編輯、格式與公式仍須網頁版的限制。不能把公告當成本帳號已取得所有手機操作功能。
3. [Notebook 管理員外部共用公告](https://workspaceupdates.googleblog.com/2026/09/manage-external-sharing-for-gemini-notebook-in-the-Admin-console.html)：發布日為 9 月 10 日，四種共用控制、網域／OU／群組與預設關閉有依據。原回答漏了「9 月 10 日起最多 15 天逐步推出」。本次只有閱讀公告，沒有改動使用者管理設定或共用權限。

三項皆落在固定區間 `[2026-09-07 00:00, 2026-09-14 00:00)` Asia/Taipei，標題、直接網址與短引均可追溯。三項同屬 Workspace 來源並不違反題目；題目沒有要求每站各一項。摘要完整性仍有上述缺漏，不能把來源存在當成全部條件正確。

## 來源狀態的可證明範圍

- [Gemini API changelog](https://ai.google.dev/gemini-api/docs/changelog) 當時最新日期標題是 2026-09-03，支持原回答「未找到期間內 API 更新」的限定結論。
- [Gemini 官方入口](https://blog.google/products/gemini/) 可讀，工具導向新版 `products-and-platforms/products/gemini/` 路徑。入口可讀不代表本次已窮盡全部文章。
- [Workspace Updates](https://workspaceupdates.googleblog.com/) 與三篇直接公告均可讀。原回答的三個 `read` 是 Spark 自述；本次另行核對上述可見來源，但沒有檢查 Spark 內部網路紀錄。

## 下一版排程指示

[prompt-schedule.txt](prompt-schedule.txt) 保留相同來源範圍，增加逐步推出的起日、最長期間、手機限制與不以網址月份判斷發布日。排程使用相對週期，必須在每次結果展開絕對日期，再核對時區與邊界；不能因本次固定日期正確就假定以後都會正確。

## 摘要長度也是待核對欄位

原回答自行標示三段是 73／73／72 字。用 Unicode 字元數計算、包含英文與空白、不包含括號標籤，實際為 **88／80／71**。三個自報數字都不相符，第一段在這個明確計數規則下超過 80。原提示詞只說「80 字」，沒有指定英文與空白如何計算，因此不能把此規則偽稱為事前已約定；但足以示範不能信任模型自報字數。後續可把明確計數方式加入提示詞，再由程式計算。

[check-manual.py](check-manual.py) 從已保存回答擷取三項，檢查日期精度、摘要字數與短引長度，輸出 [manual-structure-check.json](manual-structure-check.json)。保留官方日期的「日」精度；既有 `check_digest.py` 要求帶時區的精確時間，這裡不捏造發布時分來湊格式。此腳本確認的是資料結構和可計算欄位，仍不能判定摘要有沒有漏掉推出條件。

[Spark 官方說明](https://support.google.com/gemini/answer/17094507?hl=en-GA) 與[排程說明](https://support.google.com/gemini/answer/17094710) 亦於本日讀取，用於辨別建立、立即執行、排程、暫停／恢復等操作。官方頁面對裝置關閉時的行為有不一致敘述，本次沒有關機實測，不對此作已驗證承諾。本文只記錄本帳號可見的 Beta 功能與有限案例，不推論所有地區／方案皆能使用。
