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
branch: codex/article-missing-locales-20261007
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

### 2026-10-07 補語系來源查核

補缺語系前發現歷史階段錯誤：9/11 越南政府報導已寫明整合徵詢意見，
並提報 2/4–2/10 的七天建議方案；原文卻說到 9/15 仍在徵詢兩案。
這項修正要保留 9/17 的查證日期，以及當時「政府尚未核定」的狀態，
不能把後來 10/2 的核定冒充原始查證時已知資料。

Primary source:
https://baochinhphu.vn/thong-nhat-trinh-chinh-phu-phuong-an-nghi-tet-nguyen-dan-2027-trong-7-ngay-lien-tuc-102260911155606794.htm
查核 finding SHA b7129a38fef2756c43354647d5a837a35d4ef5f7444023c2eeda6abeb9f685db；
官方 HTML SHA 2a597e1281ab77e910a0a6aa49986714fcb001d1c155c7be9ed1a82a67849f9f。
精確三個正文 before/after 提案保存在站主的持久證據目錄，仍需獨立批准的
source-correction 收據；原有 SVG「建議方案／未定案」與日期範圍維持原樣。
四語翻譯暫留佇列，沒有開始新的模型工作或修改公開原文。
