---
id: 2026-10-22-independently-recheck-c11-ucc-v4-source
title: Independently recheck C11 UCC v4 source and visual delta
status: done
priority: P1
area: docs
owner: codex-c11-independent-source-v4
claimed_at: 2026-10-22T16:54:46Z
created_at: 2026-10-22T16:54:40Z
completed_at: 2026-10-22T16:56:59Z
branch: codex/brand-story-ucc-c11-script
depends_on: []
scope:
  - docs/videos/story-everyday-ucc-c11/reviews/script-source-delta-v4.md
---

# Independently recheck C11 UCC v4 source and visual delta

## Why

C11 UCC 的 v3 來源差異曾 PASS，但純旁白盲讀 A 判 HOLD。作者因此修改 42 個旁白 ID、31 個 JSON 鏡頭物件；舊收據的整檔雜湊無法核准 v4。須由未參與改稿者重讀原發行者頁面並逐 ID 審查，避免 Mira／UCC 的「第一」、罐內塗層、萬博與拉環年份越界。

## Definition of done

- [x] 一份綁定 v4 四檔 SHA 的獨立 PASS／HOLD 收據，逐 ID 記錄 42 句、31 鏡與來源 URL，說明未改列的承接界線和付費停線。

## Steps

- [x] 重讀 UCC 2025／2026、博物館、沿革、濱田市兩頁及島根縣原頁。
- [x] 由 PR head 的 Git diff 機械比對 83 個 ID，逐句和逐鏡檢查，核對 JSON／閱讀版鏡像。
- [x] 將收據寫入原草稿 PR 的窄 review scope；作者稿件保持原 SHA。

## How to verify

`Get-FileHash` 核對 script、visual JSON、visual MD、source notes；`git diff 0131b442f^ 0131b442f -- <四檔>` 確認 42／31 改字；解析三檔 ID、JSON／MD 鏡像、74 shot／9 stats；`git diff --check` 與 `npm run check:tasks`。逐 ID 判定見收據 `docs/videos/story-everyday-ucc-c11/reviews/script-source-delta-v4.md`。

## Notes

UCC 來源 U1–U4 與地方 H1–H3 均直接重讀，並保留利害關係與事後回顧限制。42 句來源界線與 31 鏡文字預檢 PASS；Mira 奶成分仍未知、UCC 博物館「含奶世界首款」仍只作館方主張、1970 會場需求仍歸屬 UCC、1981 才是第三代拉環。v4 仍待兩位新鮮旁白盲讀、實圖、TTS 與站主核准；本輪未付費。

`git diff --check` 通過；`npm run check:tasks` 退出 1，原因是本 worktree 原已留下八份同 ID 的 untracked `tasks/open/` 副本，與已提交的 `tasks/done/` 重複。那些副本不是本票範圍，未刪改；本票的窄 scope 沒有碰撞。
