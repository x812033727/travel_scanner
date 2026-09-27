# 兩張票與發布紀錄

開票、claim、done、合併的做法在 skill `task-board`。這裡只講補語系這條線特有的形狀。

## 翻譯票 `localize-...`

- 標題例：`Localize four hosting setup guides batch024`、`Localize the desk-cable guide into en, ja, ko and zh-CN`；area `api`（早期有 `docs`）。
- **scope 只列會改的檔**：每篇 `apps/api/app/guides/content/<slug>.json` 與 `apps/web/public/guides/<slug>`。不要把 `docs/article-localization/releases/` 放進來，那是發布票的。
- Why：這幾篇現在只有哪個語系、原文正式站版本與正規化雜湊、有沒有刻意排除的篇（例如 batch021 排除 desk-cable，因為原文連結錯）。
- Definition of done 的常見條目：五語文件都過 `GuideDocument` 且形狀與原文相同；zh-TW 與原圖位元組不變；每語經過獨立審稿、修正已套用；站內連結文字等於目標的已公開標題；`pack_cli lint` 零 error；**另開發布票**。
- Notes 寫：原文雜湊表、每語的標題與正規化雜湊、審稿筆數與嚴重項、刻意沿用的譯法、環境坑、工作目錄在哪（寫「站主機器上的持久目錄」，不要寫完整路徑）。
- 結案時開發布票（open、不認領），`depends_on` 指向翻譯票。

## 發布票 `release-localized-...`

- scope **只有** `docs/article-localization/releases/<batch>`；它不改程式、不改內容包。
- Steps 的骨架（兩條路線都一樣）：確認內容 PR 已合併、目標 SHA 的 CI 綠 → 確認或執行部署（skill `deploy`，要站主同意）→ 預檢（暫停檔、鎖、`publish_holds.json`）→ dry-run 並核對預期的 create／publish 數 → 站主用有選項的提問同意 → `pg_dump` → 發布 → links rebuild／check → 再 dry-run 全 unchanged → 公開驗收 → 寫紀錄、開 PR。
- 發布之後原文的公開版本與雜湊要寫進 Notes，下一個人翻同一篇時從那裡開始。

## `docs/article-localization/releases/<batch>/`

目錄名：產線批次用 `batchNNN`（合併發布用 `batch007-017`），單篇或非批次用 `YYYY-MM-DD-<短名>`。只放兩類檔：

- `README.md`：給人讀的紀錄（下面的範本）。
- `evidence.json`：機器可讀的數字；路線 B 另存每語公開 API 原始回應 `published-<locale>.json`。

**不放**：資料庫快照、部署 log、截圖、憑證、資料庫 ID、actor ID、主機 IP、任何機器上的絕對路徑。早期幾份 README 寫了本機證據目錄的完整路徑，別照抄。

### README 範本（以 `docs/article-localization/releases/2026-09-24-desk-cable-localization/README.md` 為底）

```markdown
# <日期> <主題> 四語上線

`<slug>` 的 en、ja、ko、zh-CN 已在正式站發布。內容來自 PR #<n>（`<short sha>`），翻譯與審稿紀錄在 `tasks/done/<翻譯票>.md`。發布票：`tasks/done/<發布票>.md`。

## 做了什麼

1. 部署：<需要或不需要，live HEAD、是否含內容 PR>。預檢：<暫停檔、鎖、規則 1、slug 是否在 publish_holds.json>。
2. dry-run：<指令>，<預期與實際的 create／update／unchanged、taxonomy>。
3. 站主同意：<選了哪個選項>。備份 <大小>，TOC 可讀。
4. 發布：<created／published 清單，failed>。
5. 連結：<rebuild 前後筆數、dropped>；<links-check 在本篇的發現>。
6. 發布後：再跑 dry-run，<全部 unchanged>。

## 結果（本機未登入從外部查）

<verify_public.py 的結果>

| 語系 | 公開版本 | 正規化文件雜湊（正式站＝內容包） |
| --- | --- | --- |
| zh-TW | <n>（這次沒動） | `<前 16 碼>…` |
| en | 2 | `…` |

<其他觀察：article_links、published_locales>。完整數字在 `evidence.json`。
```

路線 A 的紀錄多幾段：內容 PR 與合併提交、CI 的 release-safety job、bundle manifest SHA、journal 的操作數（N 個 drafts、N 個 article publications、hub 數）、暫停檔的取得與清除、部署是否帶 migration、公開驗收的網址數／桌面手機案例數／截圖數、sitemap 分頁數。範例看 `docs/article-localization/releases/batch024/README.md`。

## 實際跑過的順序（摘要）

- batch024（路線 A）：翻譯票 15:06 claim → 16 份譯文＋48 張圖、兩組獨立審稿 → 本機 16 個檢查指令 → 開發布票 → 內容 PR #699 → 發布票 claim → 新快照再比對 → 凍結 bundle → `pg_dump` 並 `pg_restore --list` 驗證 → 持有暫停檔部署 → dry-run、16 drafts、16 publications、0 hubs → 資料庫與 journal 驗收 → 20 網址×桌面手機、80 張截圖 → 寫紀錄 → 只清自己的暫停檔。
- desk-cable（路線 B）：先修原文錯連並發布成 zh-TW v8 → 翻譯票（四語各一翻譯一審稿，第三方套用）→ PR #723 → 發布票：不必部署 → dry-run 四個 create → 站主選「先 pg_dump 再發布」→ publish → links 2,032→2,036 → dry-run 全 unchanged → `verify_public.py` 五語 PASS → 紀錄。
