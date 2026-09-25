# `npm run check:i18n` 擋什麼、紅了怎麼修

`npm run check:i18n` 就是 `node tools/check-i18n.mjs`，不需要 npm 相依套件，CI 的 `web` job 在 lint 之後跑它。全部通過時印 `Validated 5 locales across 25 namespaces.`；任何一項失敗就把所有錯誤一次印出、exit 1。

## 六項檢查

| # | 檢查 | 什麼時候跑 |
| --- | --- | --- |
| 1 | 每個語系的 namespace 檔名集合跟 `en` 一樣 | 永遠 |
| 2 | 重複鍵：讀**原始文字**（`tools/json-duplicate-keys.mjs` 的 `duplicateKeys`），因為 `JSON.parse` 會默默留下後一個 | 永遠 |
| 3 | 攤平後的鍵集合跟 `en` 一樣（巢狀用點號連接，陣列算葉子） | 永遠 |
| 4 | 每個鍵的 ICU 參數名集合跟 `en` 一樣（抽取式 `\{([A-Za-z_][\w]*)`，排序後比對） | 永遠 |
| 5 | 可編輯 namespace 白名單：`apps/api/app/ui_text/schemas.py` 的 `UI_TEXT_NAMESPACES` 與 `apps/web/lib/ui-text.ts` 的 `EDITABLE_NAMESPACES`，都要等於 `messages/en` 減掉 `legacy`；`en/admin.json` 的 `uiText.namespaces` 要逐一描述它們 | 永遠 |
| 6 | 新增的漢字：`apps/web/{app,components,lib}` 底下非測試的 `.ts/.tsx/.js/.jsx`，某個連續漢字串出現次數比基準多，就要求改用目錄 | **只在 CI，或本機有 staged 變更時** |

第 6 項的細節：

- 基準：CI 是 `HEAD^`（PR 的 merge commit 的第一個親代，也就是 base）；本機是 `HEAD` 對 staged 內容。**沒有 `git add` 的改動本機不會檢查**，所以提交前先 `git add` 再跑一次，才等於 CI 的行為。
- 比的是「同一個漢字串的出現次數」，所以在同一個檔裡搬動既有字串不會紅；`git diff -M` 認得出的改名也跟著舊檔比。把一段中文**搬到新檔**（不是改名）會被當成新增。
- 只看漢字（`\p{Script=Han}`）。純假名、純諺文不會觸發，但日文裡的漢字會。
- 測試檔（`*.test.*`、`*.spec.*`）、`e2e/`、JSON 目錄都不在範圍內。
- 沒有豁免註解或白名單。

## 紅了怎麼修

| 訊息 | 原因 | 修法 |
| --- | --- | --- |
| `<locale>: namespace files differ from en` | 新 namespace 只建了部分語系的檔，或檔名大小寫不同 | 五個語系補齊；接著看 `references/i18n.md` 的「加一個 namespace」其他六處 |
| `<locale>/<ns>.json:<path>: duplicate key, JSON.parse silently keeps the last one` | 同一個物件裡同名鍵出現兩次，常見於兩個分支各加了同一個鍵後合併 | 保留正確的那個、刪掉另一個；五個語系都查一次 |
| `<locale>/<ns>.json: translation keys differ from en` | 缺鍵或多鍵。**訊息不說是哪個鍵，而且這個檔的參數檢查會被跳過** | `node .agents/skills/web-i18n-e2e/scripts/i18n-diff.mjs <ns>` 列出每個 missing／extra，補齊後再跑一次（參數錯誤可能這時才冒出來） |
| `<locale>/<ns>.json:<key>: ICU parameters differ from en` | 參數名被翻譯或拼錯、少一個參數、plural 分支用字母開頭（`one {one day}`）被當成參數 | 參數名照 `en` 原樣；plural 分支用 `#`；中日韓不需要 plural 時直接寫 `{count}` |
| `apps/api/app/ui_text/schemas.py: the editable namespace allowlist differs ...`（或 `apps/web/lib/ui-text.ts: ...`） | 新增或刪除了 namespace，白名單沒跟上 | 照訊息的 missing／extra 改那個檔；API 那邊還要改 `apps/api/tests/test_ui_text.py` 的數量斷言 |
| `admin.json: uiText.namespaces does not describe every editable namespace` | 編輯器的下拉選單少了新 namespace 的名稱 | 五個語系的 `admin.json` 都在 `uiText.namespaces` 加一個鍵（只加 `en` 會換成紅第 3 項） |
| `<file>: newly added display text '<漢字>' must use a message catalog` | 在元件或 lib 裡直接寫了中文 | 移到 `messages/<locale>/<ns>.json`（或該功能既有的 `lib/<feature>-messages/`），元件改用 `t("key")`；五個語系都要有翻譯 |

第 6 項常見的誤判來源：

- 註解裡的中文也算。註解改用英文（repo 的程式與註解本來就是英文）。
- 正規式或比對用的中文（例如解析 API 回來的中文地名）也算。把字串放進 JSON 或共用常數模組、從那裡 import；不要用 `\u` 跳脫字元繞過，那只是把問題藏起來。

## 驗證修好了

```bash
npm run check:i18n
git add -A apps/web && npm run check:i18n     # 讓第 6 項也跑，等同 CI
node .agents/skills/web-i18n-e2e/scripts/i18n-diff.mjs
npm run typecheck:web                         # lib/*-messages 的缺鍵只有這裡抓得到
```
