---
id: 2026-10-22-independently-verify-c10-oxo-v5-source
title: Independently verify C10 OXO v5 source visual delta
status: done
priority: P1
area: docs
owner: codex-c10-oxo-v5-source-delta
claimed_at: 2026-10-22T16:20:55Z
created_at: 2026-10-22T16:20:47Z
completed_at: 2026-10-22T16:24:09Z
branch: codex/brand-story-oxo-c10-script
depends_on: []
scope:
  - docs/videos/story-everyday-oxo-c10/reviews/source-visual-delta-v5.md
---

# Independently verify C10 OXO v5 source visual delta

## Why

PR #1689 的作者提交 `9ff8acc450cbb8b1547c9da76abf3a1915b179fb` 改了 C10 的 `c100514` 與 `c100601–611` 旁白、逐鏡和來源註。v4 來源 PASS 只綁舊稿，需另一名未修稿者對新 SHA 留下逐來源、逐鏡差異判定。

## Definition of done

- [x] 以新四檔 SHA 留下獨立 PASS／HOLD 收據，列明改動 ID、來源強度、畫面界線及未完成的關卡。

## Steps

- [x] 對 `git diff HEAD^ HEAD` 和上一版收據，確認本輪只有 12 句與 12 鏡改動。
- [x] 直接重讀 OXO 2017、Cooper Hewitt 2018、MoMA 館藏原頁，核對刻紋與倒油嘴、量匙、後續品類、包裝意圖、通用設計及 1989 年份。
- [x] 對照新旁白、JSON 及閱讀版，完成 ID、後製卡、提示詞禁名與書擋檢查。
- [x] 將判定寫入 `reviews/source-visual-delta-v5.md`，保留作者稿與其他代理未追蹤任務檔原樣。

## How to verify

`Get-FileHash -Algorithm SHA256` 對稿、兩份視覺稿及來源註，確認與收據一致；PowerShell 解析稿與視覺 JSON／Markdown 檢查 80 ID 同序、71 shot／9 stats、閱讀版零不符、提示詞禁名零命中；`git diff --check`；`npm run check:tasks` 並記實際退出碼。來源連結與逐 ID 判定見收據。

## Notes

收據判 **PASS**，只涵蓋文字來源／歸因及畫面提案；新 SHA 的兩位口播盲讀、TTS、按秒數圖占比、生成圖與站主付費核准仍是後續關卡。無付費生成、匯入、上傳或發布。

專屬機械檢查：稿、JSON、閱讀版各 80 個唯一 ID 且同序；71 張 `shot`、9 張 `stats`，最長連卡 2；閱讀版與 JSON 0 不符；提示詞與共通視覺契約禁名 0 命中；`look`、5 秒片頭及 21 秒 v4 片尾符合預期。`git diff --check` 通過。

`npm run check:tasks` **exit 1**：此工作樹原有七張其他審查票的未追蹤 `tasks/open` 孤檔與已追蹤 `tasks/done` 同 ID；另有不致失敗的過期認領／scope 重疊警告。未刪除、移動或修改這七張孤檔，不能把任務板檢查記為 PASS。

結案指令已產生 	asks/done 的 done 票，但 Windows 未移走本票 	asks/open 未追蹤副本，指令 exit 1。依工作範圍不手動刪除孤檔；提交 done 票和審查收據，本工作樹的重複 ID 將從七組暫增為八組，任務板檢查仍不會過。
