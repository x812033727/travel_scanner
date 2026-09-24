---
id: 2026-09-24-publish-cable-labeling-source-correction
title: 把 desk-cable 文章「標記」誤連 AI Token 的修正發布到正式站
status: open
priority: P1
area: api
owner:
claimed_at:
created_at: 2026-09-24T05:22:41Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/guides/content/desk-cable-charging-organization.json
  - docs/article-localization/releases/2026-09-24-cable-source-correction
---

# 把 desk-cable 文章「標記」誤連 AI Token 的修正發布到正式站

## Why

生活分享文章 `desk-cable-charging-organization`（〈桌面線材整理不只要好看：把用途、規格與取用位置標清楚〉，目前只有 zh-TW）的第一個 rich_paragraph（`blocks[2]`，「記下桌上固定使用的裝置……」那段）有「標記」一詞，意思是追完線的兩端後在實體線材上貼標籤。這個詞被做成文章內連，連到 AI 詞彙文章 `ai-term-token`。讀者點下去會跑到講 AI Token 的頁面，意思完全不對，翻譯時也會被複製進四個語系。

repo 裡的修正已經合併：PR #690（`b626f310`，2026-09-23 14:11 UTC）只把 `/blocks/2/inlines/1` 從 ArticleInline 改成純文字 `{"type":"text","text":"標記"}`，其他欄位一個字都沒動。**正式站還沒改**。2026-09-24 05:00 UTC 查公開 API：

- `GET https://mokaair.com/api/travel/guides/life/desk-cable-charging-organization?locale=zh-TW` 回 200；
- `document.blocks[2].inlines[1]` 仍是 `{"type":"article","text":"標記","kind":"life","slug":"ai-term-token"}`；
- `article_links` 仍含 `ai-term-token`；`published_locales` 只有 `["zh-TW"]`。

原本的票 `2026-09-23-correct-cable-labeling-glossary-link-before`（持有者 `codex-cable-source-correction`）做完了 repo 端，剩下「發布到正式站」與「發布後重新匯出、釘成翻譯基準」兩項。站主 2026-09-24 決定把舊票結案，這兩項移到這張票。舊票的 Notes 有完整的前置證據：修正前的正式站原文快照、修正前後的模型雜湊、獨立審查紀錄、`source-correction-approval.json`。那些檔案不在 git 裡，放在原持有者的工作目錄。

這篇文章在 batch021 被刻意排除（`tasks/done/2026-09-23-localize-two-household-purchasing-guides-batch021.md` 第 48 行），原因就是這個連結。所以這張票擋住的是「這篇的四語翻譯」，不擋其他文章。

## Definition of done

- [ ] 正式站公開 API 回的 zh-TW `document.blocks[2].inlines[1]` 是 `{"type":"text","text":"標記"}`，`article_links` 裡沒有 `ai-term-token`，頁面上「標記」不是連結。
- [ ] 文章其他內容與 PR #690 的 repo 原文逐欄相同，包括另一個內連 `gadget-purchase-needs-checklist`（`blocks[14].inlines[0]`）。
- [ ] 修正是透過既有的 revision 服務發布的，產生了新的真實版本；舊的 v1／v6 歷史仍在，沒有手動改版本號或計數器。
- [ ] 發布後重新匯出的 draft／published／latest 三者相同，這份匯出以雜湊釘成這篇之後翻譯的基準，紀錄放在 `docs/article-localization/releases/2026-09-24-cable-source-correction/`。
- [ ] `ai-term-token` 那篇的 backlinks 不再列出這篇。

## Steps

- [ ] 先確認正式站已部署包含 `b626f310` 的版本。沒有的話走 skill `deploy`；guides 的 JSON 要在主機的程式碼裡才匯得進去。
- [ ] 寫入前重新唯讀匯出正式站這一列，跟舊票 Notes 記的「修正前」狀態比對：article v1、zh-TW v6、沒有別的語系、沒有未發布的草稿。有任何不同就停下來，先查是誰改的。
- [ ] 用 `docs/article-localization/publish_bundle.py` 的 `source_corrections` 綁定發布這一個修正。它會呼叫 `source_correction.py` 的 `verify_review`，要求審查紀錄的路徑與 SHA256 對得上，而且只允許這一個 inline 的型別與目標改變。舊的審查紀錄是綁在修正前的快照上，如果正式站在這之間有變，就要重做審查，不要硬套。
- [ ] 發布前先用 dry-run 確認只動到這一篇、這一個語系；正式發布要站主在對話中同意。流程照 skill `content-pipeline` 的 `references/publish-runbook.md`。
- [ ] **不要**對這個修正過的 pack 跑 `pack_cli autolink`。它不是匯入流程的一部分，而且可能把「標記」重新連回 Token 那篇。
- [ ] 發布後重新匯出，核對 draft／published／latest 相同、版本號確實增加，把匯出與雜湊寫進 `docs/article-localization/releases/2026-09-24-cable-source-correction/`，再開 PR。
- [ ] 在這張票的 Notes 寫下新的版本號與雜湊，讓翻譯這篇的人知道從哪個基準開始。

## How to verify

```bash
curl -s -A "Mokaair-editorial-check/1.0" "https://mokaair.com/api/travel/guides/life/desk-cable-charging-organization?locale=zh-TW" -o cable.json
PYTHONUTF8=1 python - <<'EOF'
import json
d = json.load(open("cable.json", encoding="utf-8"))
print(d["document"]["blocks"][2]["inlines"][1])      # 預期 {'type': 'text', 'text': '標記'}
print("ai-term-token" in json.dumps(d["article_links"]))  # 預期 False
print(d["published_locales"])                         # 預期 ['zh-TW']（翻譯是另一件事）
EOF
```

用瀏覽器打開 `https://mokaair.com/zh-TW/life/desk-cable-charging-organization`，「記下桌上固定使用的裝置……」那段裡的「標記」是一般文字，不是連結。

## Notes

- 2026-09-24 從 `2026-09-23-correct-cable-labeling-glossary-link-before` 拆出來（站主授權結案舊票，見舊票最後一節）。repo 端的工作與所有前置證據都在舊票。
- 正式站狀態是 2026-09-24 05:00 UTC 用上面的 How to verify 查的；接手時先重跑一次，也許有人已經發布了。
- 這篇的四語翻譯要等這張票完成，而且要從這裡釘的新基準翻，不能從舊的 v6 翻。
