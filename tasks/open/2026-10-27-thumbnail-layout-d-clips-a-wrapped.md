---
id: 2026-10-27-thumbnail-layout-d-clips-a-wrapped
title: Thumbnail layout d clips a wrapped headline's second line without a warning
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-27T00:28:26Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/templates/theme.css
---

# Thumbnail layout d clips a wrapped headline's second line without a warning

## Why

2026-10-27，C11 UCC remake（`story-everyday-ucc-c11-remake-20261025`）的各語言縮圖。版型 d（`.thumb.column.layout-d h1`，150 px）的標題一行放不下時會換成兩行；欄位高度不夠，flex 把 h1 壓扁，`fitText`（`tools/video/render/browser.mjs`）只把超出 0.4 em 的高度當成「放不下」（為了 CJK 字形比行高高一點）。結果字級縮到兩行還差約 40 px 就停，第二行下緣被裁掉，`layoutProblems` 與 qa 的 thumbnail 項都沒報。

實例：ja「持ち歩けても飲めない」、ko「들고 가도 못 마신다」、pt「Levar não era beber」、id「Belum bisa diminum」、vi「Mang đi, chưa uống được」第二行都被副標題切掉；連單行的 vi「Chưa thể uống」也切到 g 的下緣。qa 只提醒其中幾張「標題縮到 21–23 px，請縮短」。當時的處理是把八語標題都縮成一行（見那支片的 i18n），工具沒改。

## Definition of done

- [ ] 版型 d 的標題換行後要嘛完整顯示（讓副標題往下或字級再縮），要嘛 render 報錯；不再靜默裁字。
- [ ] 單行標題的下伸部（g、y、越南文聲調）不被裁。
- [ ] 回歸測試：兩行的拉丁文與日文標題、單行帶下伸部的越南文標題。

## How to verify

`node --test tools/video/render/*.test.mjs tools/video/templates/*.test.mjs`；拿上面的五個標題各畫一次 `render --thumbnails-only` 並看圖。注意 `docs/videos/long-form/review.json` 可能綁著這些檔案的雜湊，改了要跟著做時長收據增量。
