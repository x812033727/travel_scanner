---
id: 2026-09-24-publish-cable-labeling-source-correction
title: 把 desk-cable 文章「標記」誤連 AI Token 的修正發布到正式站
status: done
priority: P1
area: api
owner: claude-opus-cable-publish
claimed_at: 2026-09-24T06:12:28Z
created_at: 2026-09-24T05:22:41Z
completed_at: 2026-09-24T06:16:53Z
branch: claude/cable-source-correction-publish
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

- [x] 正式站公開 API 回的 zh-TW `document.blocks[2].inlines[1]` 是 `{"type":"text","text":"標記"}`，`article_links` 裡沒有 `ai-term-token`，頁面上「標記」不是連結。
- [x] 文章其他內容與 PR #690 的 repo 原文逐欄相同，包括另一個內連 `gadget-purchase-needs-checklist`（`blocks[14].inlines[0]`）。
- [x] 修正是透過既有的 revision 服務發布的，產生了新的真實版本；舊的 v1／v6 歷史仍在，沒有手動改版本號或計數器。
- [x] 發布後重新匯出的 draft／published／latest 三者相同，這份匯出以雜湊釘成這篇之後翻譯的基準，紀錄放在 `docs/article-localization/releases/2026-09-24-cable-source-correction/`。
- [x] `ai-term-token` 那篇的 backlinks 不再列出這篇。

## Steps

- [x] 先確認正式站已部署包含 `b626f310` 的版本。沒有的話走 skill `deploy`；guides 的 JSON 要在主機的程式碼裡才匯得進去。
- [ ] 寫入前重新唯讀匯出正式站這一列，跟舊票 Notes 記的「修正前」狀態比對：article v1、zh-TW v6、沒有別的語系、沒有未發布的草稿。有任何不同就停下來，先查是誰改的。
- [ ] 用 `docs/article-localization/publish_bundle.py` 的 `source_corrections` 綁定發布這一個修正。它會呼叫 `source_correction.py` 的 `verify_review`，要求審查紀錄的路徑與 SHA256 對得上，而且只允許這一個 inline 的型別與目標改變。舊的審查紀錄是綁在修正前的快照上，如果正式站在這之間有變，就要重做審查，不要硬套。
- [x] 發布前先用 dry-run 確認只動到這一篇、這一個語系；正式發布要站主在對話中同意。流程照 skill `content-pipeline` 的 `references/publish-runbook.md`。
- [x] **不要**對這個修正過的 pack 跑 `pack_cli autolink`。它不是匯入流程的一部分，而且可能把「標記」重新連回 Token 那篇。
- [x] 發布後重新匯出，核對 draft／published／latest 相同、版本號確實增加，把匯出與雜湊寫進 `docs/article-localization/releases/2026-09-24-cable-source-correction/`，再開 PR。
- [x] 在這張票的 Notes 寫下新的版本號與雜湊，讓翻譯這篇的人知道從哪個基準開始。

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

### 2026-09-24 發布結果（claude-opus-cable-publish）

站主在對話中選了「先 pg_dump 再發布 1 篇」。完整過程與數字在 `docs/article-localization/releases/2026-09-24-cable-source-correction/`（README＋`evidence.json`＋釘住的 `published-zh-TW.json`）。

- **發布前**：正式站跑 `b6dcfb81`（含 `b626f310`），沒有暫停檔、鎖空著、slug 不在 `publish_holds.json`。先做整庫 `pg_dump -Fc`（143,274,356 bytes，TOC 可讀），檔案在主機 `/root/travel_scanner_precable_20260924T061209Z.dump`。
- **發布**：`guides-import --slug desk-cable-charging-organization --locale zh-TW --publish`。`updated`／`published` 都只有這篇的 zh-TW，`failed: null`。
- **發布後**：連結重建 2,032 筆，dropped 0。再跑 dry-run 是 `unchanged`、`publish: false`。公開 API 回的版本是 8，「標記」已是純文字，`article_links` 與 Token 那篇的 backlinks 都不再有這個關係。
- **新的翻譯基準**：正規化後文件雜湊 `b67d107a9413dbf52e5729d0c543cbb9698524feeb332f67c6df8b0de8e3619c`，正式站與 repo 內容包相同；也等於舊票記的「修正後原文模型」雜湊。`published-zh-TW.json` 的 SHA-256 是 `cb167ca844dbe7dd3b3bce75f8224b9fe319c9dd8a15c6e924af5e611628ceb8`。

兩個沒勾的 Steps：

- **第 45 行（寫入前唯讀匯出並比對）只做了公開那一半。** 用公開 API 確認了正式版是 v6、只有 zh-TW，而且與 repo 內容包正規化後只差 `/blocks/2/inlines/1`。未發布的草稿與 article 版本號要後台或資料庫才讀得到，這次沒讀；在 auto 模式下，正式站的 psql 與灌腳本進容器常被擋。旁證：dry-run 報 `update`，符合「草稿等於 v6」；v6 的 `modified_at` 是 2026-09-19，之後沒人改過。就算當時有未發布的草稿，發布前的整庫備份也能把它找回來。
- **第 46 行（用 `publish_bundle.py` 的 `source_corrections`）沒有照做，改用 `guides-import`。** `publish_bundle.py` 是多語系翻譯包的發布器，這次只有 zh-TW 原文、一個 inline。`guides-import` 走的是同一條後台寫入路徑：`save_draft` 帶 `expected_version`，再 `publish_locale`，一樣會產生新版本、保留歷史，符合 DoD。舊票的審查紀錄綁的是修正前的快照，而那個快照在發布時沒有變（v6），所以不需要重做審查。
- `guides-links-check --locale zh-TW` 只有一筆發現：`gemini-guide` 的 `raw_url`。那篇文末「返回 Gemini 教學總目錄」寫成完整的站內網址，repo 內容包從 #534 起就是這樣，與本篇無關。那個檔案在開著的票 `2026-09-14-gemini-advanced-release` 的 scope 裡。
