---
id: 2026-10-05-korea-autumn-leaves-links-expire-2026
title: 2026-12-01 韓國賞楓情報過期：刪掉南怡島、首爾四天三夜、KTX 三篇連到 korea-autumn-leaves-2026 的連結
status: open
priority: P3
area: docs
owner:
claimed_at:
created_at: 2026-10-05T08:35:57Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/guides/content/nami-island-petite-france-day-trip.json
  - apps/api/app/guides/content/seoul-4-day-itinerary.json
  - apps/api/app/guides/content/korea-ktx-srt-ticket-guide.json
---

# 2026-12-01 韓國賞楓情報過期：刪掉南怡島、首爾四天三夜、KTX 三篇連到 korea-autumn-leaves-2026 的連結

## Why

`korea-autumn-leaves-2026`（intel）的 `valid_until` 是 2026-11-30。原票
`2026-09-20-korea-autumn-leaves-2026-intel` 要求它和三篇 howto 互連，並在 `valid_until` 隔天拿掉其他文章連過來的連結
（第七批 README 的時效規則：howto 不連 2027-06-30 前過期的 intel，規格點名的季節段例外，刪除日是 intel 的 `valid_until` 隔天）。
那三個反向連結在原票的 PR 加上，這張票負責在 2026-12-01 起把它們拿掉。

三個連結都是「只有一個 article inline 的 `rich_paragraph`」：目標過期後網站會把它畫成一行沒有連結的純文字
（`apps/web/components/content-blocks.tsx` 找不到 reference 時回 `<span>`），所以不會壞，但會留下一行過期的標題，要整塊刪掉。

## Definition of done

- [ ] 2026-12-01 起：`nami-island-petite-france-day-trip` 裡文字為「2026 韓國楓葉預測：春川、首爾近郊與各地的楓紅高峰日」的 `rich_paragraph`（在 `korea-winter-events-2026` 那一行之後、「行前檢查」標題之前）整塊刪掉。
- [ ] 2026-12-01 起：`seoul-4-day-itinerary` 裡文字為「2026 韓國楓葉預測：南怡島所在的春川與首爾近郊幾號最紅」的 `rich_paragraph`（方案 A 段落之後、「方案 B：水原華城」標題之前）整塊刪掉。
- [ ] 2026-12-01 起：`korea-ktx-srt-ticket-guide` 裡文字為「秋天搭 KTX 南下賞楓：2026 內藏山、智異山與各地的楓紅預測」的 `rich_paragraph`（延伸閱讀清單最後一行，城市頁 link 之前）整塊刪掉。
- [ ] 三篇的 `related` 不動（原票沒有把 `korea-autumn-leaves-2026` 加進它們的 `related`）；`korea-autumn-leaves-2026` 本身不改寫成 2027 年版。
- [ ] 正式站三篇重新匯入後，頁面上沒有那三行。

## Steps

- [ ] 2026-12-01 或之後：確認 `korea-autumn-leaves-2026` 在站上已顯示過期。
- [ ] 用上面的文字找到三個區塊（區塊編號可能已被別的票改動），用文字刪除，不要用 `json.dump` 重寫整個檔。
- [ ] 跑 lint 與內容包測試。
- [ ] 部署後在正式站 `guides-import --slug <三個 slug> --locale zh-TW --dry-run`，確認三篇是 `update`，站主同意後 `--publish`，再 `guides-links-rebuild` 與 `guides-links-check --locale zh-TW`。

## How to verify

```bash
cd apps/api
PYTHONUTF8=1 uv run python -m app.guides.pack_cli lint --slug nami-island-petite-france-day-trip --slug seoul-4-day-itinerary --slug korea-ktx-srt-ticket-guide
PYTHONUTF8=1 uv run pytest tests/test_guides_content_pack.py -q
grep -l korea-autumn-leaves-2026 app/guides/content/*.json   # 只剩 korea-autumn-leaves-2026.json 自己
```

## Notes

- Split from `2026-09-20-korea-autumn-leaves-2026-intel`（原票的「過期處理」那一項；日期未到，所以拆出來）。
- 三個反向連結在原票的 PR（分支 `claude/korea-autumn-leaves`）加上；如果那個 PR 沒合併，這張票就不用做，直接關。
- `korea-ktx-srt-ticket-guide` 也在 `2026-09-19-sr-korail-recheck-daegu-jeonju` 的 scope 裡，改之前確認沒有人正在動。`tasks/BOARD.md` 不要提交。
