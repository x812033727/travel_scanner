---
id: 2026-09-24-video-skill-automated
title: 影片產線 T5：youtube-video skill 加上全自動路線
status: in-progress
priority: P2
area: tools
owner: claude-opus-5-5
claimed_at: 2026-09-24T03:38:20Z
created_at: 2026-09-24T00:41:16Z
completed_at:
branch: claude/video-skill
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

- [x] SKILL.md 的模式表多一列「全自動（TTS＋自動合成）」，主幹與關卡涵蓋企劃 → 撰稿 → 查核 → 聽眾優先審稿 → tts → 試聽 → render → assemble → captions → package → 站主上傳 → youtube-sync。
- [x] 新 reference `automated.md`：`video.json` 格式、每個子指令、工作區、狀態檔、STOP、核准、結束碼。
- [x] 代理提示：`references/prompts/planner.md`、`writer-video.md`、`verifier-video.md`，帶文章產線的硬規則（固定 User-Agent、只寫工作區、當天官方來源、骨架先存）。
- [x] `script-writing.md` 補 TTS 專用的寫法（`say` 覆寫、發音字典、數字唸法）；`publish.md` 補五語 CC 與 API 同步的位置、非原創內容政策的對策。
- [x] `docs/videos/README.md`：頻道規格（版型目錄、配色、選定的聲音、片頭片尾、說明欄範本、UTM、ffmpeg 版本與 SHA256）。
- [x] `npm run test:tools` 綠（skill 提到的路徑都存在、逐字複本一致、沒有機器路徑）。

## Steps

- [x] 等 T2–T4 合併（skill 會提到它們的路徑）。T2（#712）已合併；T4（#714）還開著，這個分支疊在它上面，#714 合併前 PR 的差異會包含 T4 的 commit。
- [x] 改 SKILL.md（正文 ≤300 行）並複製到 `.claude/skills/youtube-video/SKILL.md`。
- [x] 寫 references 與 prompts。
- [x] 寫 `docs/videos/README.md`。

## How to verify

```bash
npm run test:tools
```

## Notes

- 2026-09-24 claude-opus-5-5：認領時相依的票還在別的分支上，所以用了 `--force`。
- **頻道聲音還沒選**。`docs/videos/README.md` 的聲音表寫「還沒選」，並寫明用 `audition` 讓站主比較。這一步要等站主在後台填好 Azure 金鑰、建立權杖、自己跑 `login`，所以放進試作票 `2026-09-24-video-pilot-ai-model-choice` 當第一步。
- **發音字典 `lexicon.json` 還不存在**，由試作票建立（它在那張票的 scope 裡）。skill 裡只寫「`docs/videos/` 底下的 `lexicon.json`」：`tools/skills.test.mjs` 會擋 repo 裡不存在的路徑。
- **skill 測試的佔位符陷阱**：`tools/skills.test.mjs` 會先拿掉大寫的 `<PLACEHOLDER>/`，再檢查剩下的路徑。所以 `docs/videos/<SLUG>/brief.md` 會被讀成 `docs/videos/brief.md`，被判定為不存在。解法是改用 `<VIDEO_DOCS>/brief.md`，並在提示開頭定義 `<VIDEO_DOCS>`。
- 全自動路線的交接**不改 `brief.md`**：大綱的核准綁它的雜湊。人工錄製路線照舊用 `brief.md` 的狀態行。
- 這個 worktree 原本沒有 `node_modules`，Node 會往上找到主 checkout 的 `node_modules`，裡面沒有字型套件，所以 render 的測試會失敗。在 worktree 跑 `npm ci --ignore-scripts` 之後，210 項全過。
