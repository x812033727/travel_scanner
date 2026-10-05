---
id: 2026-10-04-two-ja-life-articles-read-under
title: Two ja life articles read under the 1,500-character floor once link-only lines stopped counting
status: done
priority: P3
area: docs
owner: claude-opus-5-5-ja-life-length
claimed_at: 2026-10-05T06:28:37Z
created_at: 2026-10-04T15:45:25Z
completed_at: 2026-10-05T06:54:42Z
branch: claude/ja-life-length
depends_on: []
scope:
  - apps/api/app/guides/content/household-inventory-spreadsheet.json
  - apps/api/app/guides/content/weekly-review-reset-routine.json
---

# Two ja life articles read under the 1,500-character floor once link-only lines stopped counting

## Why

`2026-10-03-body-length-link-only-paragraphs`（2026-10-04）讓只含連結的 `rich_paragraph`（文末「延伸閱讀」那種單行連結）不再算進
`_body_length`。全站 2,450 個（pack, locale）裡 2,239 個字數下降，其中兩篇 ja 從剛好過線變成低於 life 的 1,500 字下限，
`pack_cli lint --kind life` 因此多了兩個 `text_length` 警告：

| pack | locale | 之前 | 之後 |
| --- | --- | --- | --- |
| `household-inventory-spreadsheet` | ja | 1,538 | 1,496 |
| `weekly-review-reset-routine` | ja | 1,512 | 1,482 |

兩篇各只有一行站內連結被扣掉，正文本身沒變；它們的 zh-TW 原文本來就短（984 → 960、984 → 957，一直有 `text_length` 警告），
所以低於下限的 pack 數不變（前後都是 19 個），只是同一篇多了一個語言被點名。這是警告不是錯誤，不擋 ingest 或 CI。

## Definition of done

- [x] 這兩篇的五個語言要嘛補到 1,500 字以上（補的是讀者用得到的內容，不是填字數），要嘛在本票 Notes 寫明為什麼保留短篇。
- [x] `uv run python -m app.guides.pack_cli lint --kind life --slug household-inventory-spreadsheet --slug weekly-review-reset-routine`
      不再有 ja 的 `text_length` 警告，或 Notes 交代保留的理由。

## Steps

- [x] 讀兩篇的 zh-TW 原文，判斷值不值得擴寫（走 skill `content-pipeline` 的改稿流程，五語一起改）。
- [x] 擴寫或記錄保留的決定。
- [ ] 合併後重新匯入正式站：publish after merge (coordinator, owner consent)。指令見 Notes。

## How to verify

```bash
cd apps/api
PYTHONUTF8=1 uv run python -m app.guides.pack_cli lint --kind life   --slug household-inventory-spreadsheet --slug weekly-review-reset-routine
```

## Notes

- 量測：2026-10-04 在 `claude/pack-ingest-body-length-render-svg` 上，用 `_body_length` 對全站每個（pack, locale）前後各算一次比對。
- 同一輪也有 25 個原本超過 6,000（intel 3,000）上限的（pack, locale）回到範圍內，例如 `ai-news-2026-january-september-index`、
  `tech-news-2026-index` 的 zh-TW。
- 2026-10-05（claude-opus-5-5-ja-life-length，`claude/ja-life-length`）：判斷值得擴寫。兩篇的 zh-TW 只有指引下限的三分之二，
  而且各缺一段讀者實際會卡住的操作，所以五語一起補，不是只替 ja 湊字：
  - `household-inventory-spreadsheet` 加 H2「約定誰在什麼時候改狀態」：把每次改狀態綁在一定會發生的動作上（拆開最後一份備品、
    下單或買回、歸位、準備採買）的分工表；不開表格的家人怎麼轉告；同一用品放兩處時只記未開封備品；表格與實物對不上時怎麼回頭調整分工。
    放在「補貨門檻」的 callout 之後、「定期刪欄位」之前。
  - `weekly-review-reset-routine` 在「先把散落的提醒收回來」加一張「入口｜容易漏掉的事」表（含口頭答應的事與共用行事曆），
    在決定表之後加一段「需要等待」事項的追問規則，文末加 H2「忙碌或中斷幾週時，先做最小版本」（三件事的最小版本、
    中斷後不補做過去幾週、時段一直被擠掉時換時段）。原有的四步驟與圖解不變，新段落沒有寫死分鐘數。
  - 沒有新增產品功能或數字的主張。兩個既有來源（Google Sheets 下拉選單、Google Calendar 任務）2026-10-05 用編輯 UA 重新打開，
    HTTP 200，內容仍支持原文的句子，`checked_on` 五語都改成 2026-10-05。
  - `_body_length` 前→後（zh-TW / en / ja / ko / zh-CN）：household 960/3,343/1,496/1,410/977 → 1,512/5,140/2,359/2,181/1,549；
    weekly 957/3,042/1,482/1,336/1,011 → 1,539/4,909/2,406/2,107/1,591。全部落在 1,500–6,000。
  - 檢查：`pack_cli lint --kind life --slug household-inventory-spreadsheet --slug weekly-review-reset-routine` 0 error，
    `text_length` 全部消失，只剩原本就有的 `no_summary` ×10；`pack_cli lint --kind life`（1,004 篇）0 error，低於下限的 pack 從 19 降到 17；
    `intake_check.py --from-content` 兩篇都 body_length ok，唯一 FAIL 是改動前就有的「first block is not summary」；
    `docs/news-2026-batch-4/translation_checks.py` 兩篇 0 hit；`pytest tests/test_guides_content_pack.py tests/test_guides_content_links.py` 12 passed、5 skipped。
  - 沒做：summary 區塊（`no_summary`、intake 的 FAIL）留給 `2026-09-15-content-summary-howto-and-life`，那張票的摘要要站主逐批審 diff。
    其餘 13 篇同批短文開成 `2026-10-05-thirteen-short-life-guides-read-under`；四個索引頁短是設計，沒有開票。
  - 發布（合併並部署之後，協調者取得站主同意才做）：
    `guides-import --slug household-inventory-spreadsheet --slug weekly-review-reset-routine --locale zh-TW --locale en --locale ja --locale ko --locale zh-CN --dry-run`
    應為兩篇各五個 `update`，再換成 `--publish --actor-email <ACTOR_EMAIL>`，之後 `guides-links-rebuild`。
