---
id: 2026-09-24-release-localized-desk-cable-guide
title: Release the four new desk-cable locales to production
status: open
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-09-24T07:22:27Z
completed_at:
branch:
depends_on:
  - 2026-09-24-localize-desk-cable-guide
scope:
  - docs/article-localization/releases/2026-09-24-desk-cable-localization
---

# Release the four new desk-cable locales to production

## Why

`2026-09-24-localize-desk-cable-guide` 在內容包加了 `desk-cable-charging-organization` 的 en、ja、ko、zh-CN 與四張 `diagram-1-*.svg`。內容包跟著程式部署上去，但沒匯入就不會上線；正式站目前只有 zh-TW（v8）。

## Definition of done

- [ ] 正式站公開 API 的 `published_locales` 是五個語系；每個語系的文件與內容包正規化後雜湊相同（見翻譯票 Notes 的表）。
- [ ] zh-TW 仍是 v8、雜湊 `b67d107a…`，這次沒有動它。
- [ ] 五個語系的頁面 200、h1 等於標題、canonical 正確、沒有 noindex、各語系的圖回 200，都在 sitemap 裡。
- [ ] 每個語系文末連到 `gadget-purchase-needs-checklist` 的站內連結有 materialize（該篇五語早已上線）。
- [ ] 紀錄放在 `docs/article-localization/releases/2026-09-24-desk-cable-localization/`。

## Steps

- [ ] 確認翻譯 PR 已合併、目標 SHA 的 CI 綠，正式站部署了含該 PR 的版本（沒有就走 skill `deploy`，要站主同意）。
- [ ] 預檢：沒有暫停檔、鎖空著、slug 不在 `publish_holds.json`。
- [ ] `guides-import --slug desk-cable-charging-organization --locale en --locale ja --locale ko --locale zh-CN --dry-run`：預期四個 `create`、`publish: true`，taxonomy `unchanged`，沒有別的。
- [ ] 站主用有選項的提問同意後，先 `pg_dump`，再把 `--dry-run` 換成 `--publish --actor-email <ADMIN_EMAILS 第一個>`。
- [ ] `guides-links-rebuild`，再對五個語系各跑一次 `guides-links-check --locale <L>`；之後再跑 dry-run，應全部 `unchanged`。
- [ ] 本機未登入跑 `verify_public.py --slug desk-cable-charging-organization --kind life --locale <L> --sitemap`，五個語系各一次，每次間隔 1.3 秒以上。
- [ ] 寫發布紀錄與雜湊，開 PR。

## How to verify

```bash
for L in en ja ko zh-CN; do
  curl -s -A "Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)" \
    "https://mokaair.com/api/travel/guides/life/desk-cable-charging-organization?locale=$L" \
    | python -c "import json,sys; d=json.load(sys.stdin); print(d['locale'], d['published_locales'], d['document']['title'])"
  sleep 1.5
done
```

## Notes

- 做法與前一次（zh-TW 原文修正）相同，指令與坑見 `docs/article-localization/releases/2026-09-24-cable-source-correction/README.md`：`guides-import` 走後台同一條寫入路徑（新語系是 `start_translation` 再 `publish_locale`）。
- 2026-09-24 的 zh-TW 發布前曾做整庫 `pg_dump`（143 MB），這次照樣先備份。
