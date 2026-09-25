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
- [x] 撰稿（sonnet）→ 查核（opus，換人）→ 聽眾優先審稿，2026-09-25 完成。新詞已併進共用的 `docs/videos/lexicon.json`。
  - 查核兩輪，第 2 輪不需要再加一輪。
  - 聽眾審稿改寫 ef9k、m7qy、ex3f、c8ct、29zm、drae 和片尾一句，刪掉 8iey。ef9k 原本寫「我都自己測過一次」，這是撰稿代理替站主捏造的經驗，已經改掉。
  - lint 0 錯誤，估計 10.9 分鐘。
- [ ] tts → check-audio → 核准旁白 → render → assemble → CC → package。
- [x] Codex 修補版本號：片中完全不提版本號（verify-2 #25）。
- [ ] 不示範任何入侵手法，也不點名一手來源以外的受害公司。

## How to verify

```bash
node tools/video/cli.mjs lint --slug ai-agent-permissions
node tools/video/cli.mjs status --slug ai-agent-permissions
```

## Notes

- 2026-09-25 claude-opus-5-5 認領；分支 `claude/video-batch-2`，疊在試作片分支 `claude/video-pilot-audio` 上（要用它的 `docs/videos/lexicon.json`）。
