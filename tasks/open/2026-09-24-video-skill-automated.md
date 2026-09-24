---
id: 2026-09-24-video-skill-automated
title: 影片產線 T5：youtube-video skill 加上全自動路線
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-09-24T00:41:16Z
completed_at:
branch:
depends_on:
  - 2026-09-24-video-tts-azure
  - 2026-09-24-video-render-slides
  - 2026-09-24-video-assemble-package
scope:
  - .agents/skills/youtube-video
  - .claude/skills/youtube-video
  - docs/videos/README.md
---

# 影片產線 T5：youtube-video skill 加上全自動路線

## Why

`youtube-video` skill（2026-09-23 做、2026-09-24 併進來）目前是人工錄製路線：代理交稿子、分鏡、字卡與上架文字，錄音剪輯上傳是站主。站主決定把全自動路線加進同一個 skill，不另開 skill。設計全文在 `docs/videos/DESIGN.md`（T1 一起合併）；skill 是 `.agents/skills/youtube-video/`。

## Definition of done

- [ ] SKILL.md 的模式表多一列「全自動（TTS＋自動合成）」，主幹與關卡涵蓋企劃 → 撰稿 → 查核 → 聽眾優先審稿 → tts → 試聽 → render → assemble → captions → package → 站主上傳 → youtube-sync。
- [ ] 新 reference `automated.md`：`video.json` 格式、每個子指令、工作區、狀態檔、STOP、核准、結束碼。
- [ ] 代理提示：`references/prompts/planner.md`、`writer-video.md`、`verifier-video.md`，帶文章產線的硬規則（固定 User-Agent、只寫工作區、當天官方來源、骨架先存）。
- [ ] `script-writing.md` 補 TTS 專用的寫法（`say` 覆寫、發音字典、數字唸法）；`publish.md` 補五語 CC 與 API 同步的位置、非原創內容政策的對策。
- [ ] `docs/videos/README.md`：頻道規格（版型目錄、配色、選定的聲音、片頭片尾、說明欄範本、UTM、ffmpeg 版本與 SHA256）。
- [ ] `npm run test:tools` 綠（skill 提到的路徑都存在、逐字複本一致、沒有機器路徑）。

## Steps

- [ ] 等 T2–T4 合併（skill 會提到它們的路徑）。
- [ ] 改 SKILL.md（正文 ≤300 行）並複製到 `.claude/skills/youtube-video/SKILL.md`。
- [ ] 寫 references 與 prompts。
- [ ] 寫 `docs/videos/README.md`。

## How to verify

```bash
npm run test:tools
```

## Notes
