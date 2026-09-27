---
id: 2026-09-24-localize-desk-cable-guide
title: Localize the desk-cable guide into en, ja, ko and zh-CN
status: done
priority: P2
area: api
owner: claude-opus-cable-localization
claimed_at: 2026-09-24T07:01:55Z
created_at: 2026-09-24T07:01:54Z
completed_at: 2026-09-24T07:22:58Z
branch: claude/cable-localization
depends_on: []
scope:
  - apps/api/app/guides/content/desk-cable-charging-organization.json
  - apps/web/public/guides/desk-cable-charging-organization
---

# Localize the desk-cable guide into en, ja, ko and zh-CN

## Why

`desk-cable-charging-organization`（〈桌面線材整理不只要好看：把用途、規格與取用位置標清楚〉）目前只有 zh-TW。batch021 刻意排除它，因為原文把「標記」誤連到 AI Token 文章。那個錯誤已在 2026-09-24 修正並發布成 zh-TW v8，發布紀錄與翻譯基準在 `docs/article-localization/releases/2026-09-24-cable-source-correction/`（正規化文件雜湊 `b67d107a…`）。站主要求補齊四個語系。

這篇和已經五語上線的 `gadget-purchase-needs-checklist`（batch021）是同一個模板：15 個區塊、同樣的 AI hero 標示格式、同一款四步驟流程圖。所以兩篇共用的樣板句，直接沿用 gadget 已審過的譯法。

## Definition of done

- [x] 內容包多出 en、ja、ko、zh-CN 四份 GuideDocument，形狀與 zh-TW 相同，都通過 `GuideDocument` 驗證；zh-TW 一個位元組都沒動。
- [x] 四張各語系的流程圖 `diagram-1-{en,ja,ko,zh-cn}.svg`，渲染後沒有溢出、裁切、重疊或缺字；hero 圖沒有文字，五個語系共用。
- [x] 每個語系都經過一位沒參與翻譯的審稿者逐句對照 zh-TW，修正已套用；審稿紀錄留在持久工作目錄。
- [x] 文末站內連結的文字逐字等於 `gadget-purchase-needs-checklist` 在該語系的標題；「標記」是純文字，不是連結。
- [x] `pack_cli lint --kind life` 對這篇零 error，內容包相關 pytest 通過。
- [ ] PR 的必要檢查全綠並合併（由本 PR 完成；合併前無法打勾）。
- [x] 發布到正式站另開一張票（要部署加上站主同意）。

## Steps

- [x] 以 zh-TW v8（`b67d107a…`）為唯一依據，四個語系各由一位翻譯代理產出文件與 SVG，自己渲染檢查。
- [x] 每個語系各一位獨立審稿者（不同代理），只交修正清單；由第三個代理套用，重新驗證、重新渲染。
- [x] 併入內容包（只加四個 locale，不動 zh-TW），SVG 放進 `apps/web/public/guides/desk-cable-charging-organization/`。
- [x] 跑 `pack_cli lint`、`tests/test_guides_content_pack.py`、`docs/news-2026-batch-4/translation_checks.py`，開 PR。
- [x] 開發布票：部署後 `guides-import --slug desk-cable-charging-organization --locale en --locale ja --locale ko --locale zh-CN` 先 dry-run、再站主同意後 `--publish`。

## How to verify

```bash
cd apps/api
.venv/Scripts/python.exe -m app.guides.pack_cli lint --kind life
.venv/Scripts/python.exe -m pytest tests/test_guides_content_pack.py -q
PYTHONUTF8=1 python ../../docs/news-2026-batch-4/translation_checks.py desk-cable desk-cable-charging-organization
```

zh-TW 不變的證明：內容包 `locales["zh-TW"]` 正規化後的 `document_hash` 仍是 `b67d107a9413dbf52e5729d0c543cbb9698524feeb332f67c6df8b0de8e3619c`。

## Notes

- 持久工作目錄：`C:\Users\x8120\mokaair-work\cable-localization\`（`tr/` 譯稿、`review/` 修正清單、`svg/`、`render/` PNG、`*.pre-review.*` 審稿前版本）。這是站主機器上的路徑，repo 裡沒有這些檔。
- 翻譯與審稿走 Claude 代理（翻譯 sonnet、審稿 opus），不是 `tools/article-localization` 的 Codex CLI 產線。後者的基準快照要把腳本灌進正式站容器，auto 模式會擋。

### 2026-09-24 完成內容（claude-opus-cable-localization）

| 語系 | 標題 | 正規化文件雜湊 |
| --- | --- | --- |
| zh-TW（未動） | 桌面線材整理不只要好看：把用途、規格與取用位置標清楚 | `b67d107a9413dbf5…` |
| en | Desk cable organization isn't just about looks: label each cable's purpose, specs, and where it's used | `29300977c879cb73…` |
| ja | デスクのケーブル整理は見た目だけではない：用途・規格・使う場所をはっきり示す | `99b3444a19f729aa…` |
| ko | 책상 케이블 정리, 보기 좋은 것만으로는 부족합니다: 용도·규격·사용 위치를 분명하게 표시하기 | `796d07ab7e0402e0…` |
| zh-CN | 桌面线材整理不只要好看：把用途、规格与取用位置标清楚 | `a55af5580b4ff6a4…` |

- 併入方式：原內容包能以 `json.dumps(ensure_ascii=False, indent=2)` 逐位元組重現，所以只在 zh-TW 之後加入四個 locale；diff 只有新增、沒有刪除，zh-TW 的雜湊前後都是 `b67d107a…`。
- 審稿：en 10 筆（2 筆嚴重）、ja 13 筆（1 筆嚴重）、ko 12 筆、zh-CN 4 筆，全部套用，沒有退回。嚴重的三筆是：en 與 ko 的 rich_paragraph 兩段 inline 之間少一個空格（前端直接相接，en 會印出 `andlabel`）、en「手腳」譯成 legs/feet、ja「急折」譯成「急に折り曲げ」（變成「突然地」）。
- 協調者另改三個標題（審稿者把標題列在 title_concerns、沒放進修正清單）：ko「보관 위치」→「사용 위치」、ja「取り出す位置をはっきりさせる」→「使う場所をはっきり示す」、en「and location」→「and where it's used」，都是對齊內文小標「標記使用位置」的譯法，SVG 的 `<title>` 一起改。紀錄在工作目錄 `review/coordinator-title-corrections.json`。
- 刻意沿用 gadget 已上線的譯法：圖的頁首、副標、頁尾，圖說與 description 的結尾句，hero alt 的 AI 標示與 credit。ko 圖上副標「한 번에 모두 끝내려 하지 마세요」與 gadget 已上線的圖逐字相同，所以沒改。
- 檢查：`pack_cli lint --kind life` exit 0，本篇只有 zh-TW 原本就有的 `no_summary`／`text_length` 警告（ko 1,462 字、zh-CN 1,027 字低於 1,500 的建議，原文本身只有 980 字）；`tests/test_guides_content_pack.py` 9 passed、5 skipped（需要 PostgreSQL）；`translation_checks.py` 0 hit。
- 四張 SVG 用 `render_svg` 渲染後逐張看過，沒有溢出、裁切、重疊或缺字。SVG SHA-256：en `76f4d571…`、ja `b3ee1a21…`、ko `c23205ce…`、zh-cn `1b60c03b…`。
- 環境坑：Playwright 的 `chromium-1234\chrome-win64\chrome.exe` 在這台機器啟動失敗（WinError 14001 side-by-side），改用同一版本的 `chromium_headless_shell-1234\chrome-headless-shell-win64\chrome-headless-shell.exe` 當 `CHROMIUM_BIN`。
- 發布：`2026-09-24-release-localized-desk-cable-guide`。
