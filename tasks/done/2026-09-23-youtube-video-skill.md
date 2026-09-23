---
id: 2026-09-23-youtube-video-skill
title: YouTube 教學與解說影片的製作 skill
status: done
priority: P2
area: tools
owner: claude-opus-5-5
claimed_at: 2026-09-23T23:02:50Z
created_at: 2026-09-23T23:02:50Z
completed_at: 2026-09-23T23:08:44Z
branch: claude/youtube-production-skill-qu0qdu
depends_on: []
scope:
  - .agents/skills/youtube-video
  - .claude/skills/youtube-video
---

# YouTube 教學與解說影片的製作 skill

## Why

站主想做像「AI模型這麼多，到底該怎麼挑？」（Kelly Tsai，觀點解說）與「Claude Code 近期更新彙整」（Gary Chen，更新彙整＋示範）那樣的中文科技 YouTube 影片。站上已經有查核過的 AI 系列與新聞，但從選題、口播稿、畫面、縮圖到上架文字沒有固定流程，每次都要從頭問。

## Definition of done

- [x] `.agents/skills/youtube-video/` 有 SKILL.md（Claude 的 byte-identical copy 在 `.claude/skills/`），說明三種格式、不變的規矩、主幹階段與指令。
- [x] references：formats、script-writing、script-format、visuals、publish，加字卡與縮圖的 HTML 範本。
- [x] `scripts/video_kit.py`（只用標準函式庫）：from-article、check、teleprompter、shots、metadata、render。

## Steps

- [x] 看兩支參考影片的標題與格式（YouTube 頁面只取得到 oEmbed 標題與頻道）。
- [x] 寫 SKILL.md 與 references。
- [x] 寫 video_kit.py，用 `claude-vs-chatgpt-writing-test` 與手寫稿實跑每個子指令；render 在 headless Chromium 出 1920x1080 字卡與 1280x720 縮圖並看過。
- [x] `npm run test:tools`、`npm run check:tasks`、`ruff check`／`ruff format --check` 通過。

## How to verify

```bash
npm run test:tools
python3 .agents/skills/youtube-video/scripts/video_kit.py from-article claude-vs-chatgpt-writing-test --out /tmp/v/script.md
python3 .agents/skills/youtube-video/scripts/video_kit.py check /tmp/v/script.md   # 骨架應該 FAIL：章節還沒有口播
```

## Notes

- 代理不登入 YouTube、不按發布；錄音、錄影、剪輯是站主的事。skill 交出讀稿機文字、分鏡表與素材、上架包。
- 章節時間只有剪完的實際時間能上架；`metadata` 沒有 `--chapters` 時會在上架包最上面標「估計時間」。
- 口播速度預設每分鐘 250 字（`--cpm` 可調），英文單字與數字串各算兩字，是粗估。
- 沒做：TTS 配音、自動剪輯（ffmpeg 組粗剪）、直接上傳 YouTube API。需要時另開票。
