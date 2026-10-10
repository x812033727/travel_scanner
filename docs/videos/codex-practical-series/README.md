# Codex 實作系列：任務與週報工具

18 課、36 支獨立跟做影片：每課各有 App 與 CLI 版本，使用相同需求、起始材料與驗收。主要讀者已用過 Codex，但需要建立從需求到交付的方法。繁中旁白、繁中 CC；一般單支 12–18 分鐘，17／18 課目標 18–25 分鐘。

本目錄保存可重做的規格與教材。**規格、作者參考程式、產品操作、成片、站主跟做與發布各自驗收。** 尚未取得的產品操作和媒體不列為完成。實際狀態見 [STATUS.md](STATUS.md)；原始執行與媒體放在 repository 外。

## 怎麼開始學

本機交付：[首課教材 ZIP](C:/Users/x8120/mokaair-work/codex-practical-series/build-07/delivery/codex-practical-01-materials.zip)；[18份 ZIP manifest](C:/Users/x8120/mokaair-work/codex-practical-series/build-07/delivery/manifest.json)。公開教材下載入口尚未發布；其他環境可使用下方 build 指令重建。

1. 選一課及 App／CLI 版本，取得該課的教材 ZIP。
2. 將完整 ZIP 解到新的練習資料夾。先讀 README、驗收與提示詞，再進入 `start`，不要先複製參考答案。
3. 跟做主案例，記錄你看見的結果與失敗；依驗收確認，不只讀 Codex 最後的回覆。
4. 使用獨立 `challenge` 練一次換題；先做完再讀 `answers.md`。
5. `reference` 是作者提供的可驗收參考實作，標示來源，不宣稱它是 Codex 一次生成的成品。

App 版本把專案選擇、輸入位置、結果檢查與保存完整示範；CLI 版本把工作目錄、提示、命令、輸出與退出碼完整示範。兩版不用互相補課。第 17 課分別教 App 排程與 CLI 批次執行，使用同一套報表真值核對。

## 課程與獨立入口

本表是已建立的教案與製作 brief；成片狀態請看 STATUS。教材說明可直接閱讀，完整 start／reference／challenge 程式從當課 ZIP 或 materializer 取得。

測試與獨立重做結果見 [VALIDATION.md](VALIDATION.md)。

| 課程教案 | 教材說明 | App 製作 brief | CLI 製作 brief |
| --- | --- | --- | --- |
| [01 接手基準](lessons/01.md) | [01](materials/lessons/01/README.md) | [App](episodes/codex-practical-01-app/brief.md) | [CLI](episodes/codex-practical-01-cli/brief.md) |
| [02 需求與計畫](lessons/02.md) | [02](materials/lessons/02/README.md) | [App](episodes/codex-practical-02-app/brief.md) | [CLI](episodes/codex-practical-02-cli/brief.md) |
| [03 搜尋與篩選](lessons/03.md) | [03](materials/lessons/03/README.md) | [App](episodes/codex-practical-03-app/brief.md) | [CLI](episodes/codex-practical-03-cli/brief.md) |
| [04 AGENTS.md](lessons/04.md) | [04](materials/lessons/04/README.md) | [App](episodes/codex-practical-04-app/brief.md) | [CLI](episodes/codex-practical-04-cli/brief.md) |
| [05 重現與修 Bug](lessons/05.md) | [05](materials/lessons/05/README.md) | [App](episodes/codex-practical-05-app/brief.md) | [CLI](episodes/codex-practical-05-cli/brief.md) |
| [06 測試的判斷力](lessons/06.md) | [06](materials/lessons/06/README.md) | [App](episodes/codex-practical-06-app/brief.md) | [CLI](episodes/codex-practical-06-cli/brief.md) |
| [07 審查修改](lessons/07.md) | [07](materials/lessons/07/README.md) | [App](episodes/codex-practical-07-app/brief.md) | [CLI](episodes/codex-practical-07-cli/brief.md) |
| [08 Git 交付與還原](lessons/08.md) | [08](materials/lessons/08/README.md) | [App](episodes/codex-practical-08-app/brief.md) | [CLI](episodes/codex-practical-08-cli/brief.md) |
| [09 資料與週報](lessons/09.md) | [09](materials/lessons/09/README.md) | [App](episodes/codex-practical-09-app/brief.md) | [CLI](episodes/codex-practical-09-cli/brief.md) |
| [10 畫面與鍵盤驗收](lessons/10.md) | [10](materials/lessons/10/README.md) | [App](episodes/codex-practical-10-app/brief.md) | [CLI](episodes/codex-practical-10-cli/brief.md) |
| [11 重構](lessons/11.md) | [11](materials/lessons/11/README.md) | [App](episodes/codex-practical-11-app/brief.md) | [CLI](episodes/codex-practical-11-cli/brief.md) |
| [12 工作交接](lessons/12.md) | [12](materials/lessons/12/README.md) | [App](episodes/codex-practical-12-app/brief.md) | [CLI](episodes/codex-practical-12-cli/brief.md) |
| [13 Skill](lessons/13.md) | [13](materials/lessons/13/README.md) | [App](episodes/codex-practical-13-app/brief.md) | [CLI](episodes/codex-practical-13-cli/brief.md) |
| [14 唯讀 MCP](lessons/14.md) | [14](materials/lessons/14/README.md) | [App](episodes/codex-practical-14-app/brief.md) | [CLI](episodes/codex-practical-14-cli/brief.md) |
| [15 Worktree](lessons/15.md) | [15](materials/lessons/15/README.md) | [App](episodes/codex-practical-15-app/brief.md) | [CLI](episodes/codex-practical-15-cli/brief.md) |
| [16 子代理分工](lessons/16.md) | [16](materials/lessons/16/README.md) | [App](episodes/codex-practical-16-app/brief.md) | [CLI](episodes/codex-practical-16-cli/brief.md) |
| [17 週報自動化](lessons/17.md) | [17](materials/lessons/17/README.md) | [App](episodes/codex-practical-17-app/brief.md) | [CLI](episodes/codex-practical-17-cli/brief.md) |
| [18 畢業交付](lessons/18.md) | [18](materials/lessons/18/README.md) | [App](episodes/codex-practical-18-app/brief.md) | [CLI](episodes/codex-practical-18-cli/brief.md) |

## 教材產生與檢查

從 repository 根目錄執行，ZIP 與展開的練習專案寫到 repo 外：

```powershell
node tools/codex-practical/course.mjs check
node --test tools/codex-practical/labs.test.mjs
$courseDelivery = Join-Path 'C:/Users/x8120/mokaair-work/codex-practical-series' ('build-' + [DateTimeOffset]::UtcNow.ToString('yyyyMMdd-HHmmss'))
node tools/codex-practical/course.mjs build `
  --output $courseDelivery `
  --python C:/Users/x8120/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe
```

輸出包含 18 份 `codex-practical-NN-materials.zip` 與 manifest。每份 ZIP 有 start／reference／challenge、操作 README、提示詞、驗收、獨立答案及檔案 SHA-256。每次選新目錄，既有輸出會被保留。`materials/lessons/NN` 在 repo 只有文字說明，完整快照在外部 build 目錄；原始碼與逐課差異在 `materials/source` 與 `tools/codex-practical/labs.mjs`，不提交大量重複快照。

每份網站資料與操作都屬於獨立起點。`localStorage` 的資料不會自動出現在 CLI；先匯出，再用指定檔案產生報表。UTC 時間儲存與 Asia/Taipei 日期區間分開處理；舊資料未知完成日期保留未知。

## 製作次序

先完成18課規格、36份獨立brief及教材；試製01兩版，再用03／05兩版驗證功能與排錯的教法，才批次製作其餘課。每課先有真實操作，再查核、寫稿、旁白與成片。App 缺原生操作素材時維持待拍，CLI 紀錄不能代替。

所有實測保留輸入、實際命令、工具版本、結果及日期。模型對照在執行前決定輸入與計分，保留沒成功的結果，不只挑成功回合。教材測試與未參與撰稿者重做分開；站主首課跟做回饋再用於修訂。

語音使用現有頻道 Sulafat 與既有製作關卡。先做字數／額度 dry-run，再執行已授權的階段。媒體產物放 repo 外；合併、部署、上傳與公開發布另列收據。
