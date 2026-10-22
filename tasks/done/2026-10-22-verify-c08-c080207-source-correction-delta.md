---
id: 2026-10-22-verify-c08-c080207-source-correction-delta
title: Verify C08 c080207 source correction delta
status: done
priority: P2
area: docs
owner: codex-gpt6-c08-independent-short75-delta
claimed_at: 2026-10-22T13:54:02Z
created_at: 2026-10-22T13:53:57Z
completed_at: 2026-10-22T13:54:43Z
branch: codex/brand-story-kikkoman-c08-script
depends_on: []
scope:
  - docs/videos/story-everyday-kikkoman-c08/reviews/line-source-review-20261022-short-75-c080207-delta.md
---

# Verify C08 c080207 source correction delta

## Why

C08 75 句全稿的獨立來源查核只因 c080207「太重」HOLD；作者改「笨重」後，需對新 SHA 直接覆核並證明其餘內容未漂移。

## Definition of done

- [x] 新 SHA 的 c080207 與相鄰文意 PASS，前次 74 句和 75 畫面 PASS 可沿用，並有獨立差異收據。

## Steps

- [x] 核對 PR 作者 head、三檔 SHA、75 個 ID、逐行差異。
- [x] 直接重讀 MoMA M1 與 GK Report No.34 印刷頁 23–24，寫入來源邊界與判定。

## How to verify

讀 reviews/line-source-review-20261022-short-75-c080207-delta.md；用 Get-FileHash -Algorithm SHA256 驗三份檔案；git diff 834ba0cdf169172ca6d93f2442e86d01335298a2..6f44c8862fbbbfa4c8511e170e945f9214980896 -- script.md visual-plan.md script-source-addendum.md（於 docs/videos/story-everyday-kikkoman-c08/）；核對 75 個 script/visual ID。

## Notes

PASS：笨重符合 M1 的 unwieldy；R1 支援大瓶在廚房／陶壺在餐桌的參與者回顧。其餘 74 句、75 畫面和來源補充未動。本機有先前 policy-blocked 的三份 orphan tasks/open 票，不重試刪除或繞過。

2026-10-22：tasks done 已寫出本輪 done 票，Windows 仍留下 open 原檔；先前同類原檔刪除遭自動審查 blocked by policy，本輪未重試或繞過。提交只納入 done 票與來源收據，四份 orphan open 原檔留在本機。

npm run check:tasks 本機 exit 1：四組 done/open 重複 ID（本輪及前三輪 orphan）；提交樹只含 done 票，因此不可把本機失敗誤報為新收據內容錯誤。
