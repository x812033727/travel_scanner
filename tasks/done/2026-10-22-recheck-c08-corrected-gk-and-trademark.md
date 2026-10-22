---
id: 2026-10-22-recheck-c08-corrected-gk-and-trademark
title: Recheck C08 corrected GK and trademark delta
status: done
priority: P2
area: docs
owner: codex-gpt6-c08-independent-r1-82
claimed_at: 2026-10-22T13:37:24Z
created_at: 2026-10-22T13:37:19Z
completed_at: 2026-10-22T13:38:15Z
branch: codex/brand-story-kikkoman-c08-script
depends_on: []
scope:
  - docs/videos/story-everyday-kikkoman-c08/reviews/line-source-review-20261022-r1-82-delta.md
---

# Recheck C08 corrected GK and trademark delta

## Why

PR #1681 的 C08 作者修正前輪四項來源／畫面問題，三份輸入檔 SHA 全變。需另一代理直接重讀 K3、GK Report 印刷頁 24，核對精確差異並留下新 SHA 判定。

## Definition of done

- [x] 新 SHA 的獨立來源差異收據逐一判定旁白 c080304/601/603、畫面 c080304/401/601/603 與 R1 補充，且明示舊 82 ID 表哪部分可沿用。

## Steps

- [x] 再次直接讀龜甲萬 K3 新聞稿與 GK Report No.34 印刷頁 24。
- [x] 比對 80f55bd9e..99b85ee87 的三檔差異、ID 完整性及新 SHA，寫獨立 PASS/HOLD 收據。

## How to verify

讀 docs/videos/story-everyday-kikkoman-c08/reviews/line-source-review-20261022-r1-82-delta.md；執行 Get-FileHash -Algorithm SHA256 比對三個輸入檔；git diff 80f55bd9e..99b85ee87 -- 三檔作者檔案；npm run check:tasks 與 git diff --check。

## Notes

新 SHA 的來源／畫面事實界線 PASS：GK 扶肘姿勢與 K3 2018 年 4 月公告／3 月 30 日註冊、無字食品容器範圍均已修正；酒杯實驗暗示已移除。僅差異查核；兩名敘事盲讀、獨立美術預檢、TTS、站主核准均未執行。前一輪 orphan open 票 tasks/open/2026-10-22-independently-review-c08-gk-backed-82.md 曾遭刪除政策阻擋，本輪不碰它。
2026-10-22：tasks done 寫出 done 票後仍留下本輪 open 原檔。本輪不重試此前被 policy 擋下的單檔刪除；提交只包含 done 票與 delta 收據，兩個未追蹤 open 副本都留在本機。
