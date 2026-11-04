---
id: 2026-11-04-curio-and-sothatswhy-stop-burning-subtitles
title: 奇聞檔案局與原來如此事務所不燒字幕：繁中與外語都走 CC
status: review
priority: P2
area: tools
owner: claude-opus-stw-dialogue
claimed_at: 2026-11-04T04:31:07Z
created_at: 2026-11-04T04:31:02Z
completed_at:
branch: claude/focused-hopper-zq70n8-p02
depends_on: []
scope:
  - tools/video/automation/flow.mjs
  - tools/video/automation/automation.test.mjs
  - tools/video/automation/explainer-family.test.mjs
---

# 奇聞檔案局與原來如此事務所不燒字幕：繁中與外語都走 CC

## Why

站主 2026-11-04：「奇聞跟原來如此都改成不燒字幕」。燒錄的繁中字幕關不掉，觀眾開外語 CC 時兩層字幕在畫面下方重疊，外語配音也對不上；
YouTube 多語言的主流做法是乾淨畫面加多條 CC 加多語言音軌（`docs/videos/DESIGN.md` 原本就是這個設計）。10-25 為了學只做中文的參考頻道讓 cute-mystery 試燒，這次收回；
原來如此的撰稿提示詞（`prompts.mjs` 的 `writer:explainer`）寫著 `burn_in: true`，但 `flow.mjs settle()` 本來就把它蓋成 false；那段文字被 `prompts.test.mjs` 釘雜湊（改了會讓主機上所有未完成的解說階段重跑、重付），所以不改文字。品牌故事（`story.mjs`）站主沒有提，不動。

## Definition of done

- [ ] 主機新做的奇聞（cute-mystery）與原來如此（cute-cartoon、flat-explainer）單集 `subtitles.burn_in` 一律 false。
- [x] 原來如此的撰稿提示詞：不改文字（見上），`settle()` 保證結果是 false。
- [ ] 測試照新規則改，`npm run test:tools` 綠；長片收據由獨立審查者重綁。
- [ ] `curio-episode` skill 的「字幕」一列改寫：它在 `2026-10-14-curio-episodes-keep-the-series-look` 的範圍內，那張票結束前不碰，改由這張票的 Notes 記錄，請站主或那張票的負責人補。

## Notes

- 已上架的燒錄集數不重做（跟 10-19 配樂的決定一樣，只管新集）。
- P02（`sothatswhy-p02-cloud-rain`）在 `2026-11-03-sothatswhy-dialogue-pilot-p02` 那張票裡改成不燒錄重新合成。
