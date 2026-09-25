---
id: 2026-09-25-video-ai-agent-permissions
title: 影片：AI 代理人越界事件，和你該先設好的三道權限
status: in-progress
priority: P2
area: docs
owner: claude-opus-5-5
claimed_at: 2026-09-25T01:24:44Z
created_at: 2026-09-25T01:23:19Z
completed_at:
branch: claude/video-batch-2
depends_on: []
scope:
  - docs/videos/ai-agent-permissions
---

# 影片：AI 代理人越界事件，和你該先設好的三道權限

## Why

熱門話題研究第三名：8/26、9/18、9/24 接連三起 AI 代理在評測中越界的事件。站主 2026-09-25 選了大綱 A：每講一起事件，就帶出一道權限。企劃書在 `docs/videos/ai-agent-permissions/brief.md`，來源文章 `codex-permissions`。

## Definition of done

- [ ] `docs/videos/ai-agent-permissions/` 有 `brief.md`、`video.json`、`claims.md`、`verify-1.md`（必要時 `verify-2.md`），`lint` 零錯誤。
- [ ] 旁白通過 `check-audio`，站主核准旁白、看完成片（`approvals.json` 三筆，雜湊與成品一致）。
- [ ] 站主在 Studio 上傳成私人，影片 ID 寫回 `video.json`。

## Steps

- [x] 企劃代理寫 brief，站主選大綱（2026-09-25，選項 A）。
- [ ] 撰稿（sonnet）→ 查核（opus，換人）→ 聽眾優先審稿。新詞列在 `lexicon-additions.json`，由協調者併進共用字典。
- [ ] tts → check-audio → 核准旁白 → render → assemble → CC → package。
- [ ] Codex 修補版本號（CLI 0.149.0／Desktop 26.818.21641）只查到媒體引用，查不到官方出處，片中寫「以官網為準」。
- [ ] 不示範任何入侵手法，也不點名一手來源以外的受害公司。

## How to verify

```bash
node tools/video/cli.mjs lint --slug ai-agent-permissions
node tools/video/cli.mjs status --slug ai-agent-permissions
```

## Notes

- 2026-09-25 claude-opus-5-5 認領；分支 `claude/video-batch-2`，疊在試作片分支 `claude/video-pilot-audio` 上（要用它的 `docs/videos/lexicon.json`）。
