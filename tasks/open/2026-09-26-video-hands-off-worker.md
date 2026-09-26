---
id: 2026-09-26-video-hands-off-worker
title: 影片交給 AI 決定：工人套用頻道立場、Jev 挑大綱、送審帶品管結果與完整上傳包
status: open
priority: P1
area: tools
owner:
claimed_at:
created_at: 2026-09-26T16:18:42Z
completed_at:
branch:
depends_on:
  - 2026-09-26-video-hands-off-judge
  - 2026-09-26-video-hands-off-qa
scope:
  - tools/video/automation
  - tools/video/review
  - tools/video/package
  - tools/video/core/lint.mjs
  - .agents/skills/youtube-video
  - .claude/skills/youtube-video
  - docs/videos/AUTOMATION.md
---

# 影片交給 AI 決定：工人套用頻道立場、Jev 挑大綱、送審帶品管結果與完整上傳包

## Why

伺服器端的規則（judge 票）和 `qa` 指令做好之後，工人與本機工具要真的去用：企劃時套用頻道立場、送審大綱前先請 Jev 挑、送審成片時帶上品管結果、上傳包附上完整檔案（`docs/videos/HANDS-OFF.md`）。

## Definition of done

- [ ] 企劃與撰稿的提示詞加上「## 頻道立場」，內容從工具設定讀。
  - `brief.md` 的站主觀點第一行寫「套用立場：N、M」；
  - lint 檢查這一行存在、引用的條號都存在；立場空白時不檢查。
- [ ] 送審大綱前，先呼叫 `judge/outline`：
  - `passed`：payload 帶上 `pick` 送審；
  - 沒過：把沒過的原因當成退回意見，交給 `replan`，計入 `MAX_REPLANS`；
  - 端點回 409（沒有開）：照舊送審，等站主；
  - 外部服務失敗：交給 `later`，下一輪再試。
- [ ] 本機的 `review-push --gate outline` 走同一條路。
- [ ] `review-push --gate final` 先跑 `qa`，payload 帶上 `qa`。自動核准之後，工人照舊 `review-pull`。
- [ ] `package` 之後：
  - 跑上傳包的檢查；
  - 「確認上架」的審核附上完整檔案：`final.mp4`、`thumbnail.jpg`、`captions/*.srt`、`description.*.txt`、`metadata.json`；
  - `UPLOAD.md` 只留操作步驟，揭露的答案寫進 `metadata.json`。
- [ ] 讀回 `youtube_video_id`，寫進工作區 `video.json` 的 `youtube.video_id`，影片標成完成。
- [ ] 更新文件：
  - skill 的 `references/automated.md` 關卡表；
  - `references/prompts/planner.md` 的站主觀點規則；
  - `AUTOMATION.md` 的「關卡」列，連到 HANDS-OFF.md。

## Steps

- [ ] 提示詞與 lint。
- [ ] 大綱：judge、送審、重寫。
- [ ] 成片：`qa`、`review-push`。
- [ ] 上傳包：完整檔案、`UPLOAD.md`。
- [ ] 讀回影片 id。
- [ ] skill 與文件；`.claude/skills` 的逐字複本。

## How to verify

```bash
npm run test:tools
node tools/video/cli.mjs review-push --slug ai-agent-permissions --gate final
```

## Notes

- 工人的權杖本來就能送審，這張沒有擴大它能做的事。
- 上傳包裡的 mp4 約 90–100 MB，用既有的分段上傳送。
