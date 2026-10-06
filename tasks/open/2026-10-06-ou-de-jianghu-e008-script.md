---
id: 2026-10-06-ou-de-jianghu-e008-script
title: 《偶的江湖》第 8 集劇本：鬼燈（22 分鐘長篇動畫）
status: in-progress
priority: P2
area: docs
owner: claude-fable-local
claimed_at: 2026-10-06T01:48:27Z
created_at: 2026-10-06T01:48:18Z
completed_at:
branch: claude/ou-de-jianghu-e007
depends_on:
  - 2026-10-05-ou-de-jianghu-ep8-leaflet-knowledge
scope:
  - docs/videos/ou-de-jianghu-e008
  - docs/videos/series-plans/ou-de-jianghu/production
---

# 《偶的江湖》第 8 集劇本：鬼燈（22 分鐘長篇動畫）

## Why

站主 2026-10-05 要接著寫後面的集數（第 6 集 PR #1327，第 7 集在分支 `claude/ou-de-jianghu-e007`）。第 8 集〈鬼燈〉照企劃包 `season-01.json` 第 8 集：鯨背嶼外海浮起千盞青燈，滄瀾客硬闖島底破陣、孩童甦醒；鬼燈君現身指控姬無霜嫁禍，紗女以拓片與柳不活靴底的傳單紙拆穿陣符出自鬼燈君安在舊部營的細作；姬無霜斬鬼燈君奪回幽都；懸念（reversal）是三宗長老向她道謝、紗女手裡捏著一截新的斷弦。新角色鬼燈君 `guideng-jun`（只在本集）。第 4 集留下的問題「寫傳單的人怎麼比玄門先知道秘錄不見」在本集揭細作時回答，答案由主控暫定、待站主核定（票 `2026-10-05-ou-de-jianghu-ep8-leaflet-knowledge`）。

## Definition of done

- [ ] `production/cast.json` 加 `guideng-jun`（聲音見 Notes）與本集需要的 look，`cast-notes.md` 有第 8 集段落，`ep8/meta.json`、`ep8/header.json`、`ep8/check-act.mjs` 齊；第 1–8 集同一角色的物件逐字相同。
- [ ] `production/ep8/beats.md` 十一節，經連戲審、戲劇審、修訂與對抗驗收。
- [ ] `docs/videos/ou-de-jianghu-e008/` 五檔齊；lint 0 錯誤、craft 全達標、shot_reading 0 陷阱；估算正文 1,390–1,418 秒。
- [ ] 懸念 reversal、兩段高張力在對的半場（石窟破陣在前半、灘頭拆穿與斬首在後半）；跨集連戲（對第 1–7 集）經獨立審稿；原作名稱掃描 0 筆。

## Steps

- [ ] 1. 角色表、meta、表頭。
- [ ] 2. 分場表：撰寫 → 連戲審與戲劇審 → 修訂 → 對抗驗收。
- [ ] 3. 五幕分鏡、整集審修驗收。
- [ ] 4. 合併、跨集審、brief 與 review、名字掃描。

## How to verify

```bash
s=ou-de-jianghu-e008
node tools/video/cli.mjs lint --slug $s
node .agents/skills/youtube-video/scripts/drama_craft_check.mjs docs/videos/$s/video.json
node .agents/skills/animation-camera/scripts/shot_reading.mjs docs/videos/$s/video.json
npm run check:tasks
```

## Notes

- 聲音：Gemini 男聲 16 個已全部有人用，而且都是之後還會出場的角色；玄門長老的 Schedar 雖然第 1 集後就沒台詞，但他的死是懸疑主線，借給反派會讓觀眾以為他回來了。所以鬼燈君用 Azure 的 `zh-TW-YunJheNeural`（`tools/video/tts` 支援個別角色用 Azure 聲音）。TTS 前要請站主把它加進後台「Azure 語音（影片旁白）」的允許清單，否則 tts 會停下並點名這個角色。
- 與第 7 集同一條分支起步（`claude/ou-de-jianghu-e007`）；第 7 集開 PR 時本集會切到自己的分支。
