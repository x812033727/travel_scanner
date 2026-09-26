---
id: 2026-09-26-video-drama-tts-voices
title: Video drama T3: one voice per speaker in tts, emotion in the style prompt
status: open
priority: P1
area: tools
owner:
claimed_at:
created_at: 2026-09-26T01:53:31Z
completed_at:
branch:
depends_on:
  - 2026-09-26-video-drama-core
scope:
  - tools/video/tts
---

# Video drama T3: one voice per speaker in tts, emotion in the style prompt

## Why

漫劇一支影片有旁白加多個角色，每句由 `line.speaker` 決定聲音。伺服器的 `/video/speech` 本來就每次請求帶 `voice`，缺的是用戶端：`tools/video/tts/requests.mjs` 的 `planRequests` 以場景為單位、只用 `doc.voice`。

## Definition of done

- [ ] `voiceFor(doc, line)`（來自 `core/drama.mjs`）決定每句聲音；場景內 `(speaker, emotion)` 改變就切一個請求，同一請求只有一個聲音；Gemini 聲音的 `emotion` 併進 `style`（≤400 字），Azure 忽略。
- [ ] 快取鍵含聲音欄位；`tts --dry-run` 分聲音印字數與額度；角色聲音不在允許清單以結束碼 3 指名角色。
- [ ] 審聽頁與成片頁在角色句前加「【名字】」。
- [ ] slides 影片的請求與快取完全不變（既有測試綠）。

## Steps

- [ ] `requests.mjs`：依 `voiceFor` 分批；`cli.mjs`：dry-run 與允許清單；`review/pages.mjs` 的標籤（若在 T4 的 scope，改由 T4 做並在此註記）。
- [ ] 測試：一場景兩說話者 → 兩個請求；emotion 併入 style 不超長。

## How to verify

```bash
node --test tools/video/tts/*.test.mjs
node tools/video/cli.mjs tts --file tools/video/core/fixtures/drama/video.json --workdir <DIR> --dry-run
```

## Notes

設計全文在 `docs/videos/DRAMA.md`（跟 T1 一起合併）；供應商、價格、政策的研究依據也在那裡。
