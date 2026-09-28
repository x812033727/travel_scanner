---
id: 2026-09-28-claude-five-binge-story-plans
title: Five original 120-minute binge drama plans by Claude, to compare with Codex's five
status: done
priority: P1
area: docs
owner: claude-fable-5-1
claimed_at: 2026-09-28T02:08:04Z
created_at: 2026-09-28T02:07:32Z
completed_at: 2026-09-28T06:07:04Z
branch: claude/manga-drama-planning-5qgd63
depends_on: []
scope:
  - docs/videos/series-plans/claude-binge-five-20260928
---

# Five original 120-minute binge drama plans by Claude, to compare with Codex's five

## Why

站主要做五部約兩小時、目標破百萬點閱的漫劇，同時請 Codex 與 Claude 各規劃五部，之後比誰的點閱率高、劇情好。Codex 的五部在 `codex/five-binge-story-plans`（`docs/videos/series-plans/binge-five-20260928/`）。這張票是 Claude 版：五部原創、與 Codex 那五部不重疊的 120 分鐘合集企劃，每部有設定集、四十集總綱、四篇細綱、連貫性表與上架包裝，都以產線的 `body_md`／`body_json` 形狀交付並通過工人的 `documentProblem`／`retentionProblem`。不建立後台作品、不生成媒體、不上架。

## Definition of done

- [x] 五部各有來源（`source.mjs`，第一部與第三部拆成七個模組）與由 `build.mjs` 產生的 19 個檔案。
- [x] `node validate.mjs` 對五部零錯誤零警告（工人的規則、跨篇懸念、第 20 集翻轉、謎團排程、包裝上限）；`node --test validate.test.mjs` 十項全過；重建後產生檔沒有差異。
- [x] 每部經過一輪獨立審稿，必修全部改掉。
- [x] `README.md` 說明五部、共同規格、審稿與餵進產線的方法；`COMPARE.md` 定下比較規矩，並有 `compare.mjs` 量出的兩批結構數字。
- [x] 分支推上 `claude/manga-drama-planning-5qgd63`。

## Steps

- [x] 讀 DRAMA／SERIES／BINGE 三份設計與工人、伺服器的文件驗證規則；看 Codex 版的目錄結構（寫作期間不看劇情）。
- [x] 開票、認領；寫 `build.mjs`、`validate.mjs`、`AUTHORING.md`、`validate.test.mjs`。
- [x] 定五部的故事聖經（題材、機制、人物、謎團答案、四篇、每集一句話、結局），派代理各展開一部。
- [x] 每部由沒寫過它的代理完整審讀，套用必修與大部分可改項，重建、重驗。
- [x] 寫 README、COMPARE 與 `compare.mjs`，跑兩批比較，推分支。

## How to verify

```bash
node docs/videos/series-plans/claude-binge-five-20260928/build.mjs && git status --short   # 產生檔不應有差異
node docs/videos/series-plans/claude-binge-five-20260928/validate.mjs --write-report
node --test docs/videos/series-plans/claude-binge-five-20260928/validate.test.mjs
npm run check:tasks
```

## Notes

- 五部：`reload-first-day`《開服第一天，她的天賦叫讀檔》system-game／女主；`before-the-hammer`《重生回落槌前一秒》rebirth-revenge／女主；`three-needles`《三針》urban-return／男主；`taste-of-the-throne`《她替公主試毒十年》empress-rise／女主；`ghost-at-his-side`《符師與他的鬼》custom／雙男主留白。
- 共同值由 `build.mjs` 注入：120 分鐘、每集 3 分鐘、40 集、每篇 10 集、compilation、hybrid、cinematic-3d、open_ended false；`hands_off` 預設 false，建立作品時不會誤觸全自動開拍。
- 驗證接的是工人真正的函式，另外加：鉤子 ≤ 28 字、跨篇相鄰懸念不同型、第 10／20／30／40 集揭露或反轉、第 18–22 集正好一次 `world_flip`、謎團的埋下／推進／揭曉對上細綱、每個角色與場景都登記且出場。
- 代理一次寫整部（約 12 萬字元）會撞到單次 64k 輸出上限；把來源拆成設定、四篇、包裝七個模組，每個模組一次寫入就不會。有一次代理把 12.8 萬 token 全花在思考而沒寫出字，系統要它拆小後才寫出來。修稿一律用小範圍字串替換，不重寫整檔。
- 審稿改掉的真實世界撞名：濟安堂（台中真實藥局）→守方堂、回春散（註冊成藥）→安歲散、陸沉（熱門遊戲角色）→陸謹、「一眼千年」（真實節目主題曲名）→「一眼見真」、蕭太后（遼代人物通稱）→嚴太后；試毒少女的前提接近《藥師少女的獨語》，毒改成虛構礦物烏砂、公主改名元霽。為避開 Codex 版的同名同音，另改了姜蘭因→姜含章、元珩→元琰、裴照→裴恪、陳小滿→陳小樹、沈知遠→沈仲謙、沈知微→沈亦微。
- 沒做的：沒有建立後台作品、沒有生成圖片、聲音、影片或字幕、沒有上架；百萬點閱是目標不是保證。下一步照 `COMPARE.md`：盲讀兩批，各挑一部做前三集校準（可接 `2026-09-27-video-binge-pilot`），再交錯上架比數字。
- 已知留著的弱點：《她替公主試毒十年》第 5、13 集已把硝味連到攝政王，第 34 集的指認懸念較弱；《重生回落槌前一秒》第 28 集重複第 18 集的問答；審稿各自點名一集最弱的集，只修了邏輯，沒有整集重寫。
