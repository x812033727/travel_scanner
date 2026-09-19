---
id: 2026-09-19-lny-2027-vietnam-tet-hk-lcsd
title: lunar-new-year-2027-asia-travel 2026-10-15 起每月查越南 Tết 決定（最晚 2027-01-10 完成）、2027 年 1 月康文署農曆新年安排
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-09-19T06:47:40Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/guides/content/lunar-new-year-2027-asia-travel.json
---

# lunar-new-year-2027-asia-travel 2026-10-15 起每月查越南 Tết 決定（最晚 2027-01-10 完成）、2027 年 1 月康文署農曆新年安排

## Why

`lunar-new-year-2027-asia-travel` 上線時越南政府還沒定案 Tết 2027 的假期，H2-2 整段寫「越南 Tết：政府還沒定案」；香港康文署的農曆新年開放安排每年 1 月才在 info.gov.hk 出新聞稿，H2-3 目前寫的是 2025 年的安排。規格 `docs/travel-guides-batch-7/lunar-new-year-2027-asia-travel.md`「上線後與交叉檢查」要求上線 PR 同時開一張票，scope 只含本篇內容包，checklist 寫「2026-10-15 起每月檢查一次，最晚 2027-01-10 前完成」。

## Definition of done

- [ ] 越南 Tết 2027 正式決定公布後改三處：表格越南那一格、H2-2「越南 Tết：政府還沒定案」整段（連 H2 標題一起改）、summary 第三句；`sources` 換成正式公告的網址並更新 `checked_on`。如果到 2027 年 1 月仍未公告，把那段改寫成「到 X 月 X 日仍未公告」。
- [ ] 2027 年 1 月康文署新聞稿出來後：H2-3 那段的「2025 年的安排是……」換成 2027 年的實際日期，`sources` 換掉 2025-01-06 那篇。
- [ ] 兩項最晚 2027-01-10 前完成；lint 通過。

## Steps

- [ ] **2026-10-15 起每月檢查一次（10-15、11-15、12-15，最後 2027-01-10 前）**：到 baochinhphu.vn 與 xaydungchinhsach.chinhphu.vn 查越南政府對 Tết 2027 的正式決定（chinhphu.vn 要用 WebFetch，curl 連不上）。
- [ ] **2027 年 1 月**：到 info.gov.hk 找康文署當年的農曆新年開放安排新聞稿。
- [ ] 改完檢查與 `japan-golden-week-2027` 的 2027 年日期口徑一致。
- [ ] 跑 lint 與內容包測試，部署後 `guides-import --dry-run` 再 `--publish`。

## How to verify

```bash
cd apps/api
uv run python -m app.guides.pack_cli lint --slug lunar-new-year-2027-asia-travel
uv run pytest tests/test_guides_content_pack.py -q
```

部署後 `guides-import --dry-run` 列出 `lunar-new-year-2027-asia-travel` 為 `update`，再 `--publish`；打開 `/zh-TW/guides/intel/lunar-new-year-2027-asia-travel` 看表格越南格、H2-2 與 H2-3。

## Notes

- 來源：`docs/travel-guides-batch-7/lunar-new-year-2027-asia-travel.md`「上線後與交叉檢查」，由 `2026-09-16-launch-articles-batch-7` 開出。規格明定 scope 只含本篇內容包。
- 本篇 2027-02-20 到期，過期後不改寫成 2028 年版；2027-02-21 的連結拆除在 `2026-09-19-lny-links-expire-2027-02-21`。
- 反向連結（`taiwan-long-weekends-2027-flight-planning` 新增區塊）與설날口徑對齊（同一篇表格「日韓同期」欄改成「韓國설 연휴 2/6–2/9（설날 2/7）」）都在票 `2026-09-19-batch-7-backlinks-existing-guides`（既有文章補連第七批）。
- `tasks/BOARD.md` 不要提交。
