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
  - .agents/skills/youtube-video/SKILL.md
  - .claude/skills/youtube-video/SKILL.md
  - docs/videos/README.md
  - docs/videos/DUBS.md
---

# Video languages skill docs: publish, automated and drama references, README rows and DUBS point at LANGUAGES

## Why

語言改成每支影片選、上架等語言做好（`docs/videos/LANGUAGES.md`）之後，skill 的上架與主幹說明、頻道規格的字幕與配音兩列、`DUBS.md` 的「每支影片的選擇」都還寫著五語自動與只勾配音。

## Definition of done

- [x] `references/publish.md`：「多語言音軌（配音）」改成「語言」一節：三個部件、面板、上架的順序、配音仍手動；`references/automated.md`：第 9 步（CC 只做勾了的）、第 13 步改成「語言」、指令表的 `i18n-sheet --parts`；`references/drama.md` 主幹加語言一步、配音第二期。
- [x] `docs/videos/README.md` 的「字幕」「配音音軌」兩列改成每支影片選；`docs/videos/DUBS.md` 的「每支影片的選擇」一節開頭指到 LANGUAGES.md。
- [ ] 第一支實測結果（Studio 收不收 m4a、私人影片能不能加音軌、原音語言怎麼標）照 `DUBS.md` 的清單回寫 `publish.md`。

## Steps

- [x] 三份 reference。
- [x] README 與 DUBS。
- [ ] 實測回寫（等站主上傳第一支）。

## How to verify

```bash
npm run test:tools
```

## Notes

- references 只有 `.agents/` 一份（`tools/skills.test.mjs` 只鏡像 SKILL.md）。
- 做法（2026-09-27）：`publish.md` 的「多語言音軌（配音）」改成「語言：每支影片由站主選」（三部件、面板三顆鈕、五個上架狀態、「語言」卡片、配音仍手動、漫劇配音第二期、「待實測」清單留著給第一支）；上傳包清單多 `dubs/<語系>.m4a` 與 `metadata.json` 的 `language_choice`。`automated.md` 開頭、第 9–13 步、`status` 那段、指令表（`i18n-sheet --parts`、`captions` 讀 `languages.json`、`review-push --gate languages`）、成本、坑（縮短模式指到 `caption-translate.md`、面板沒出現、手動跑時先寫 `languages.json`）。`drama.md` 開頭與主幹第 12、13 步。`README.md` 字幕與配音兩列；`DUBS.md` §工人與 §站主要做的事開頭指到 LANGUAGES.md／AUTOMATION.md，步驟改成面板與「語言」卡片。
- SKILL.md 兩份（`.agents`、`.claude` 位元組相同）路線表的「五語 CC」與全自動主幹第 7、9 步也一起改，多一步 10「語言」；所以 scope 多了這兩個檔。
- 還沒做：第一支有配音的影片實測回寫（`publish.md` 的「待實測」），等站主上傳第一支。
