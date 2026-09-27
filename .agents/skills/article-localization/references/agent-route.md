# 路線 B：代理翻譯、逐語審稿、併入內容包、guides-import

2026-09-24 `desk-cable-charging-organization` 走的路（票 `tasks/done/2026-09-24-localize-desk-cable-guide.md` 與 `tasks/done/2026-09-24-release-localized-desk-cable-guide.md`）。不需要把任何腳本灌進正式站容器，所以 Claude 在 auto 模式下做得完。代理的共通規矩（UA、只寫工作目錄、不跑 git）照 skill `content-pipeline` 的「不變的規矩」。

## 1. 釘來源

從公開 API 抓已發布的 zh-TW，正規化後算雜湊；這個雜湊就是整批唯一的翻譯依據，寫進票。

```bash
curl -s -A "Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)" \
  "https://mokaair.com/api/travel/guides/life/<slug>?locale=zh-TW" > <WORK>/published-zh-TW.json
```

正規化：拿掉公開文件的 `version`、`published_at`、`modified_at`（它們是傳輸欄位，不拿掉雜湊就錯，batch009 第一版基準因此作廢），經 `GuideDocument.model_validate(...).model_dump(mode="json")`，再用 `app.guides.service.document_hash`。拿同樣方法算 repo 內容包的 `locales["zh-TW"]`：兩個值要相同，不同就表示後台改過或 repo 較新，先弄清楚再翻。

翻譯前把原文讀一遍找錯：站內連結連錯文章、事實過期。有錯先開原文修正票、發布成新版本，再以新版本為基準（desk-cable 就是先修「標記」的錯連，發布成 zh-TW v8 才翻）。

## 2. 翻譯、審稿、套用（每語三個角色）

| 角色 | 模型（實測） | 產出 |
| --- | --- | --- |
| 翻譯 | sonnet，每語一位 | 完整 GuideDocument JSON 與該語系的 SVG，自己渲染檢查 |
| 審稿 | opus，每語一位，沒參與翻譯 | 只交修正清單（逐句對照 zh-TW），標嚴重程度；標題疑慮另列 |
| 套用 | 第三個代理或協調者 | 套修正、重新驗證、重新渲染；審稿前版本留成 `*.pre-review.*` |

- 所有檔寫在 `<WORK>`（`tr/`、`review/`、`svg/`、`render/`），repo 不動。
- 同模板的兄弟文章已經五語上線時，樣板句（圖的頁首頁尾、圖說結尾句、hero alt 的 AI 標示與 credit）直接沿用已審過的譯法，並告訴審稿者這是刻意的。
- 文末站內連結的文字要逐字等於目標文章在該語系的**已公開**標題；目標沒有該語系就不要連。
- desk-cable 的審稿：en 10 筆、ja 13 筆、ko 12 筆、zh-CN 4 筆。嚴重的三筆在「共通坑」裡。

## 3. 併入內容包

- 先確認原內容包能用 `json.dumps(obj, ensure_ascii=False, indent=2)` 逐位元組重現；能的話只在 zh-TW 之後加四個 locale，diff 只有新增。不能重現就停下來，別讓序列化差異混進 PR。
- SVG 放 `apps/web/public/guides/<slug>/`，命名 `diagram-1-{en,ja,ko,zh-cn}.svg`（檔名小寫 `zh-cn`，locale 鍵是 `zh-CN`）。沒有字的 hero 五語共用；hero 有字時每語要 `hero-<l>.svg` 加渲染出的 1600×900 `hero-<l>.jpg`（batch024 的做法），原圖不動。
- 併入後再算一次 zh-TW 的正規化雜湊，與步驟 1 相同才算數。

## 4. 檢查（從 `apps/api`）

```bash
<PY> -m app.guides.pack_cli lint --kind life
<PY> -m pytest tests/test_guides_content_pack.py -q
PYTHONUTF8=1 <PY> ../../docs/news-2026-batch-4/translation_checks.py <prefix> <slug>
CHROMIUM_BIN="<CHROMIUM>" <PY> -c "from pathlib import Path; from app.guides.pack_ingest import render_svg; render_svg(Path('<SVG>'), Path('<PNG>'))"
```

`translation_checks.py` 抓日文 Shift_JIS 編不出的漢字、韓文 KS X 1001 以外的音節、en／ko 裡引用了原文沒有的中文。每張 SVG 渲染後逐張看溢出、裁切、重疊、缺字。

## 5. 發布（另一張票，部署之後）

照 skill `content-pipeline` 的 `publish-runbook.md` §3–§5，差別只在 `--locale` 列四個新語系：

1. 確認 live HEAD 已包含內容 PR（部署腳本 `--dry-run` 回 up to date 就不必部署）；沒有暫停檔、鎖空著、slug 不在 `apps/api/app/guides/publish_holds.json`。
2. `guides-import --slug <slug> --locale en --locale ja --locale ko --locale zh-CN --dry-run`：預期四個 `create`、`publish: true`，taxonomy `unchanged`。另跑一次 zh-TW 的 dry-run，應是 `unchanged`。
3. 用有選項的提問讓站主選（例如「先 pg_dump 再發布 4 個語系」）；整庫 `pg_dump -Fc` 放主機 `/root/`，確認 TOC 讀得出來。
4. 同一指令換成 `--publish --actor-email <ACTOR_EMAIL>`；新語系走 `start_translation` 再 `publish_locale`，`created`／`published` 只有這四個、`failed: null`。
5. `guides-links-rebuild`（筆數應增加、dropped 0），五個語系各跑 `guides-links-check --locale <L>`；exit 1 可能來自別篇早就有的發現，看本篇有沒有。
6. 再跑步驟 2 的 dry-run，全部 `unchanged`、`publish: false`。
7. 本機未登入跑 `verify_public.py`（五語，`--sitemap`），並把每個語系的公開 API 回應存成 `published-<locale>.json`，正規化雜湊要等於內容包。
