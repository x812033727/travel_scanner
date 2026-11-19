---
id: 2026-11-19-heimao-four-rules-relaxed
title: 黑猫 13 支對照：四條相反規則放寬（答案方向、岔題、編號清單、章末定論）與片長無上限
status: done
priority: P2
area: tools
owner: claude-fable-heimao
claimed_at: 2026-11-19T11:09:34Z
created_at: 2026-11-19T11:07:36Z
completed_at: 2026-11-19T11:24:43Z
branch: claude/heimao-youtube-analysis-689f26
depends_on: []
scope:
  - tools/video/core/narrative.mjs
  - tools/video/core/narrative.test.mjs
  - tools/video/automation/register.mjs
  - tools/video/automation/story-prompts.test.mjs
  - .agents/skills/youtube-video/references/script-writing.md
  - tools/video/automation/explainer-series.test.mjs
  - tools/video/automation/explainer-series.mjs
  - tools/video/automation/story-prompts.mjs
  - tools/video/core/opening-review.mjs
  - .agents/skills/brand-story/SKILL.md
  - .claude/skills/brand-story/SKILL.md
  - docs/videos/packaging-refresh-20261111/README.md
  - docs/videos/STORY.md
  - .agents/skills/curio-episode/SKILL.md
  - .claude/skills/curio-episode/SKILL.md
  - docs/videos/so-thats-why/dialogue-pilot-20261103/README.md
---

# 黑猫 13 支對照：四條相反規則放寬（答案方向、岔題、編號清單、章末定論）與片長無上限

## Why

2026-11-19 本機 session 用內建瀏覽器讀了黑猫研究院（@qiqiqushi0）熱門前 10 支加近 30 天 3 支的
帶時間轉錄稿（`2026-11-19-heimao-titles-and-retitle-batch` 的筆記說要等的那份研究），整理成 52 條
寫法並對照奇聞檔案局與原來如此事務所的規則。其中六條我們刻意定成與黑猫相反，站主當天逐條決定：

| # | 黑猫 | 站主決定 |
|---|---|---|
| 13 | 承諾句之前就講出答案的方向 | 放寬：開場可以用一句話講方向；原因的細節、過程、轉折、結局照樣不講；縮圖與說明欄維持不破梗 |
| 20 | 岔題前先打招呼 | 放寬：一支片可以岔題一次，前面先說一句為什麼值得聽，限 60 秒 |
| 21 | 編號清單當段落骨架 | 有條件放寬：一支最多一段，先給總數與一個懸念，每一項是一件發生的事；開場的目錄句照樣禁 |
| 22 | 每段用一句定論收掉再轉場 | 並存：章末可以先一句帶新說法的定論，再接沒解的問題；懸念仍必備 |
| 25 | 收束前把全片重走一遍 | 維持：片尾不重述 |
| 52 | 圖上加中英雙語小標 | 維持：畫面零文字 |

站主另外更正片長：「我是 8 分鐘以上而已，沒有一定要限制在 13 分鐘內」。奇聞 SKILL 寫的
「最多 13 分鐘」不是站主的意思。

`--force` 認領是站主在對話裡明說允許的：重疊的兩張票（上面那張，以及
`2026-11-03-sothatswhy-dialogue-pilot-p02`）當時都沒有人在動這幾個檔案，前者的 PR #2179 已合併。

## Definition of done

- [x] 三個系列（`curio-`、`story-`、`sothatswhy-`，共用 `STORY_SERIES_PANEL_QUESTIONS`）的盲評
      `no_spoiler`、`no_toc`、`no_detour`、`no_recap` 照上表改寫，照新規則寫的稿子不會被退。
- [x] 撰稿提示 `STORY_OPENING_RULE` 帶這四條。
- [x] 緊鉤子節奏（45 秒）把預告過的岔題段算成最長 75 秒的例外，編號清單的每一項算一個轉折。
- [x] `script-writing.md`、奇聞 SKILL、對話試片 README 寫明四條與片長；`.claude` 鏡像同步。

## How to verify

```bash
node --test tools/video/core/narrative.test.mjs tools/video/automation/story-prompts.test.mjs tools/video/automation/explainer-series.test.mjs
npm run test:tools && npm run check:tasks
```

## Notes

- 52 條的完整報告與兩個系列的逐條對照只在那次對話裡，沒有寫進 repo；這張票只落實站主決定的部分。
- 沒做、另外要處理的：奇聞題庫工具 `tools/video/curio/pool/core.mjs` 的 `LONG_MAX = 13` 仍會擋超過
  13 分鐘的題案（改它要連帶重產題案文件）；兩個系列規則檔內部三十多處互相矛盾的舊數字；52 條裡
  「沒有／部分」的其餘手法。
- 改盲評題目會讓還沒過關的稿子用新題目重讀；已過關的收據照 `narrative.mjs` 的版本規則處理。
- 四份撰稿提示（`writer:explainer-cartoon`、`writer:discuss-cartoon`、`writer:explainer-mystery`、
  `writer:discuss-mystery`）的固定雜湊跟著動了：部署後，主機上做到一半的奇聞／原來如此單集會在下一個
  階段以 `video_ai_receipt_input_changed` 停下來，要重跑那個階段。`writer:explainer-mystery` 現在
  39,589 字，離 40,000 的上限剩約 400 字，下一次加規則之前得先瘦身。
- 開 PR 後站主請 Gemini 審了兩輪，查證屬實並在同一個 PR 修掉的：岔題的 75 秒放寬原本只算緊鄰預告句的那一格，
  而且預告句自己帶「後面會」或問號時根本認不出來（連撰稿提示的示範句都中）；清單與岔題沒有次數上限；
  `LIST_ITEM_OPENER` 漏了「第一，」「接著，第二步」「第 1 步」與常見量詞；前 300 秒觀眾審查的題目沒同步；
  「還記得」SKILL 寫 2 次、提示寫 5 次；品牌故事逐章撰稿會各用一次例外；品牌故事 SKILL 沒更新。
- 查證後不成立的：原來如此的鉤子節奏其實已是 45 秒（`lint.mjs`），所以例外對它有效；黑猫 13 支標題沒有
  一支有兩個問號。
- 用黑猫 13 支的真實標題跑 `titleProblems`（#2179）：只有辛拉麵 1 支過，7 支超過 30 字、7 支沒有數字、
  2 支沒有問號。站主同一天決定放寬，第三個 commit 改了：上限 30 → 38 字、數字不再必備、反差句
  （「不是…而是…」「…卻…」）可以沒有問號；兩個問號與「前 18 字要有利害詞或數字」照舊。放寬後 13 支過
  12 支（剩 40 字的 1TB）。今天已改名的 59 支在新規則下全過，標題表裡另外 8 列的值是 `keep`，不是標題。
- 站主接著要求把 Gemini 意見裡「採納方向」的也做在同一個 PR（第五個 commit）：撰稿提示先瘦身（十步的開頭、
  重複的片尾段、13 分鐘的換算），再加句子層三個習慣；企劃大綱多七個可填欄位（舊世界、對手的理由、
  二次反轉、彩蛋、概念詞、比喻、現在）與岔題、清單放第幾章；前 300 秒觀眾審查多一題縮圖看不看得出主角。
  品牌故事沒有企劃提示（企劃是人寫的 JSON，匯入會拒絕不認得的欄位），所以改成在每章 `point` 的文字裡
  用標記寫，撰稿提示的 `CHAPTER_GUIDE` 認得（第六個 commit）；「還記得」在共用的 `NARRATIVE_RULES` 仍寫五次，
  十步系列的段落寫明以兩次為準（改共用那段會讓其他系列做到一半的片子也停下來）。
- `script-writing.md` 只有 `.agents` 一份（`.claude/skills` 只鏡像各 skill 的 `SKILL.md`）。
