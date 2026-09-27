---
id: 2026-09-27-video-languages-skill-docs
title: Video languages skill docs: publish, automated and drama references, README rows and DUBS point at LANGUAGES
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-09-27T06:16:04Z
completed_at:
branch:
depends_on:
  - 2026-09-26-video-dubs-worker
scope:
  - .agents/skills/youtube-video/references
  - docs/videos/README.md
  - docs/videos/DUBS.md
---

# Video languages skill docs: publish, automated and drama references, README rows and DUBS point at LANGUAGES

## Why

語言改成每支影片選、上架等語言做好（`docs/videos/LANGUAGES.md`）之後，skill 的上架與主幹說明、頻道規格的字幕與配音兩列、`DUBS.md` 的「每支影片的選擇」都還寫著五語自動與只勾配音。

## Definition of done

- [ ] `references/publish.md`：「多語言音軌（配音）」改成「語言」一節：三個部件、面板、上架的順序、配音仍手動；`references/automated.md`：第 9 步（CC 只做勾了的）、第 13 步改成「語言」、指令表的 `i18n-sheet --parts`；`references/drama.md` 主幹加語言一步、配音第二期。
- [ ] `docs/videos/README.md` 的「字幕」「配音音軌」兩列改成每支影片選；`docs/videos/DUBS.md` 的「每支影片的選擇」一節開頭指到 LANGUAGES.md。
- [ ] 第一支實測結果（Studio 收不收 m4a、私人影片能不能加音軌、原音語言怎麼標）照 `DUBS.md` 的清單回寫 `publish.md`。

## Steps

- [ ] 三份 reference。
- [ ] README 與 DUBS。
- [ ] 實測回寫（等站主上傳第一支）。

## How to verify

```bash
npm run test:tools
```

## Notes

- references 只有 `.agents/` 一份（`tools/skills.test.mjs` 只鏡像 SKILL.md）。
