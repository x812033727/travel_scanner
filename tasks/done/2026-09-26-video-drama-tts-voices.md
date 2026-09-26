---
id: 2026-09-26-video-drama-tts-voices
title: Video drama T3: one voice per speaker in tts, emotion in the style prompt
status: done
priority: P1
area: tools
owner: claude-fable-5-1-video-drama
claimed_at: 2026-09-26T05:35:01Z
created_at: 2026-09-26T01:53:31Z
completed_at: 2026-09-26T05:43:40Z
branch: claude/video-drama-tts-voices
depends_on:
  - 2026-09-26-video-drama-core
scope:
  - tools/video/tts
---

# Video drama T3: one voice per speaker in tts, emotion in the style prompt

## Why

漫劇一支影片有旁白加多個角色，每句由 `line.speaker` 決定聲音。伺服器的 `/video/speech` 本來就每次請求帶 `voice`，缺的是用戶端：`tools/video/tts/requests.mjs` 的 `planRequests` 以場景為單位、只用 `doc.voice`。

## Definition of done

- [x] `voiceFor(doc, line)`（來自 `core/drama.mjs`）決定每句聲音；場景內 `(speaker, emotion)` 改變就切一個請求，同一請求只有一個聲音；Gemini 聲音的 `emotion` 併進 `style`（≤400 字），Azure 忽略。
- [x] 快取鍵含聲音欄位；`tts --dry-run` 分聲音印字數與額度；角色聲音不在允許清單以結束碼 3 指名角色。
- [ ] 審聽頁與成片頁在角色句前加「【名字】」。→ `tools/video/review` 在 T4（`2026-09-26-video-drama-look-keyframes`）的 scope，由 T4 做；`timeline.json` 的每句已帶 `speaker`（T1），頁面只要讀它。
- [x] slides 影片的請求與快取完全不變（既有測試綠；新測試釘住 slides 的 clip key 算法）。

## Steps

- [x] `requests.mjs`：依 `voiceFor` 分批；`cli.mjs`：dry-run 與允許清單；`review/pages.mjs` 的標籤改由 T4 做（見上）。
- [x] 測試：一場景兩說話者 → 兩個請求；emotion 併入 style 不超長。

## How to verify

```bash
node --test tools/video/tts/*.test.mjs
node tools/video/cli.mjs tts --file tools/video/core/fixtures/drama/video.json --workdir <DIR> --dry-run
```

## Notes

設計全文在 `docs/videos/DRAMA.md`（跟 T1 一起合併）；供應商、價格、政策的研究依據也在那裡。

2026-09-26 做法（claude-fable-5-1-video-drama）：

- `planRequests` 現在每個請求帶 `speaker` 與那個說話者的聲音欄位（`voiceFields(voiceFor(doc, line))`）；場景內說話者或聲音欄位（含併進 style 的 emotion）一變就 flush。slides 的 `voiceFor` 回傳 `doc.voice` 的複本，所以請求本體與 clip key 位元組相同，既有音檔快取都還算數。
- 每句的 clip key 是 `[聲音欄位, parts]`：同一句換情緒是新的一次錄音，鄰句不受影響。
- `tts`：`voicesUsed` 列出用到的聲音、誰用它、字數；允許清單逐聲音查（`voiceProblem`），問題訊息在漫劇加上 `(spoken by yandi (炎帝))`；額度按供應商（azure／gemini 各有自己的月份）分開算與比較。`--dry-run` 多印 `voices:` 一行，`server:` 一行逐聲音報 ready；進度行在漫劇加 `[說話者]`；`state.json` 的 tts 紀錄多 `voices`。
- 沒改伺服器：`/video/speech` 本來就每個請求帶 `voice`／`style`。
