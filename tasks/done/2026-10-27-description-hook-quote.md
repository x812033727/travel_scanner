---
id: 2026-10-27-description-hook-quote
title: 說明欄開頭句在引號裡的句號就被切斷
status: done
priority: P2
area: tools
owner: claude-opus-curio-v2
claimed_at: 2026-10-27T00:49:43Z
created_at: 2026-10-27T00:49:42Z
completed_at: 2026-10-27T00:55:14Z
branch:
depends_on: []
scope:
  - tools/video/core/metadata.test.mjs
---

# 說明欄開頭句在引號裡的句號就被切斷

## Why

`tools/video/core/metadata.mjs` 的 `splitFirstSentence` 拿說明欄第一段的第一句當開頭一行，其餘排到第二段之後。第一句若是引文、引文裡又有句號（`「徵求男子，參加危險的旅程。工資很少，危險不斷。」`），舊規則切在引文內的第一個句號，YouTube 說明欄開頭就成了半句引文，下半句被排到注意事項之後。2026-10-27 在 curio-s34-v2（廣告引文）和 curio-s26-v2（「沒有麵包，就吃蛋糕。」）的中文說明欄看到，各語譯文也跟著被切。

## Definition of done

- [x] 引號（「」『』）裡、後面沒有緊跟收引號的句號不再算句尾；引號從頭到尾沒收時退回第一個句號。
- [x] 原本的行為不變：`「真的嗎？」她問。` 仍切在 `」` 之後，拉丁句點規則不變。

## Steps

- [x] 改 `splitFirstSentence`。
- [x] 補單元測試（引文內句號、引號沒收的退回）。

## How to verify

`node --test tools/video/core/metadata.test.mjs`；用 composeMetadata 組 curio-s34-v2 的中文說明欄，第一行是整句廣告引文。

## Notes

- `npm run test:tools` 2752 pass。
- 譯文的 source hash 不受影響（改的是組說明欄的工具，不是 video.json）。
