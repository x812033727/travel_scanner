---
id: 2026-09-11-language-switcher-label-clipped
title: 撤回：被判定截斷的文字全是螢幕閱讀器專用標籤
status: done
priority: P1
area: web
owner: claude-opus-5
claimed_at: 2026-09-11T13:31:27Z
created_at: 2026-09-11T13:05:04Z
completed_at: 2026-09-11T13:36:17Z
branch: claude/mokaair-website-access-k7xiku
depends_on: []
scope:
  - apps/web/components/language-switcher.tsx
  - apps/web/app/globals.css
---

# 撤回：被判定截斷的文字全是螢幕閱讀器專用標籤

## 這張任務是錯的，不要照著做

原始主張是「『語言』被截斷 122 次、全站 293 處文字截斷」。**全部是假的。**

實測那些元素，每一個都帶 `class="sr-only"`：

```
「語言」          scrollW=32  clientW=1  overflow=hidden  cls=sr-only
「搜尋旅行靈感」   scrollW=96  clientW=1  overflow=hidden  cls=sr-only
「目的地」        scrollW=48  clientW=1  overflow=hidden  cls=sr-only
「下一站，從這裡發現」scrollW=144 clientW=1  overflow=hidden  cls=sr-only
「正在載入旅行靈感」 scrollW=128 clientW=1  overflow=hidden  cls=sr-only
```

`sr-only` 是刻意把元素壓成 1px 並 `overflow: hidden`，讓它只對螢幕閱讀器存在、對視覺使用者隱形。**那是正確的無障礙做法**，而 `scrollWidth > clientWidth` 對這種元素必然成立。

## 成因

量測程式用 `scrollWidth > clientWidth + 2 && overflow !== 'visible'` 判定截斷，沒有排除視覺隱藏的元素。`sr-only` 全部命中。

## 給下一個人

要偵測真正的文字截斷，必須先排除視覺隱藏元素。可用的判準：矩形小於等於 2×2px、`clip-path: inset(50%)`、`clip: rect(0,0,0,0)`，或 class 含 `sr-only`。這個專案大量使用 `sr-only`（圖表的 `<table>` 等價物也是），不排除就會得到整片假陽性。
