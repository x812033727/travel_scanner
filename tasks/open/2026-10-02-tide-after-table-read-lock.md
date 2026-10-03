---
id: 2026-10-02-tide-after-table-read-lock
title: Tide After production table read and shooting lock
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-10-02T16:41:33Z
completed_at:
branch:
depends_on:
  - 2026-10-02-tide-after-production-package
scope:
  - docs/videos/series-plans/tide-after-20260930/production
---

# Tide After production table read and shooting lock

## Why

production-v1提供四十集完整對白與自動拆表，但場內秒數仍是編寫估算，現場動線、演員讀演、專業顧問及供應商尚未實測確認。開機版本必須由實際製作團隊完成，不得把空白表複製計畫數字後宣稱已驗證。

## Definition of done

- [ ] 演員／代讀完成40集逐場讀本，保留原始錄音與實測時間，容量異常已有劇本回修及二讀。
- [ ] 導演及各組完成重點場勘景、分鏡、道具和傷妝核對；法律、鑑識、醫療及語言顧問按場號回覆。
- [ ] 實際供應商報價、演員及場地檔期寫入同版通告，製片核准預算與拍攝安排。
- [ ] 劇本、拆表與部門簽認有相同版本／日期，明確區分已鎖場次與後續修訂。

## Steps

- [ ] 依production/pilot-plan.md先做EP01完整讀本與港邊聲畫測試。
- [ ] 每批四集讀演；優先EP13／16／20的程序與關係戲、29–31跨集火場及40法律收束。
- [ ] 將實測表另存具日期檔案，保留空白模板；按演出結果調整劇本後重建拆表。
- [ ] 完成各組顧問意見、報價與現場動線，製片／導演／主創共同簽認開機版。

## How to verify

比對具日期的讀本錄音、逐場實測紀錄、顧問回覆、實際報價和簽認版本。再執行 `python3 docs/videos/series-plans/tide-after-20260930/production/build_package.py --check`；這個命令只驗證文稿與拆表一致，不能替代人的讀本與簽認。

## Notes

- 本票追蹤實際製作階段，尚未選角、約顧問、採購、付費或代為聯繫供應商。
- 起案文件：docs/videos/series-plans/tide-after-20260930/production/README.md。
- 取得實際讀本／勘景／報價資料後再認領；不要為結案虛構時長或用預算假設冒充報價。
