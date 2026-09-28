---
id: 2026-09-27-video-drama-room-skill-docs
title: Video drama room skill docs: one drama route in the skill, and DRAMA, SERIES and AUTOMATION follow DRAMA-FLOW
status: review
priority: P2
area: docs
owner: claude-fable-5-1-video-languages
claimed_at: 2026-09-27T11:39:44Z
created_at: 2026-09-27T06:16:03Z
completed_at:
branch:
depends_on:
  - 2026-09-27-video-drama-room-worker
  - 2026-09-27-video-drama-room-web
scope:
  - .agents/skills/youtube-video
  - .claude/skills/youtube-video
  - docs/videos/DRAMA.md
  - docs/videos/SERIES.md
  - docs/videos/AUTOMATION.md
---

# Video drama room skill docs: one drama route in the skill, and DRAMA, SERIES and AUTOMATION follow DRAMA-FLOW

## Why

流程改了（`docs/videos/DRAMA-FLOW.md`）：漫劇只有一條路，關卡是文件與劇本加四個自動關卡，站主可以討論。skill `youtube-video` 與三份設計文件要跟上，否則下一個代理照舊文件做。

## Definition of done

- [x] `SKILL.md` 的路線表：「AI 漫劇」與「長篇漫劇」合成一列，關卡寫成「文件（故事聖經／設定集、總綱、細綱）、劇本」加自動的設定圖、旁白、分鏡、成片；`.claude/skills/youtube-video/SKILL.md` 同步（`tools/skills.test.mjs`）。
- [x] `references/drama.md`：關卡清單、主幹表第 1 步改成故事聖經、第 3 步後加劇本關卡、拿掉單集的選大綱、指令加 `review-push --gate script`；`references/series.md`：流程每個核准點加「討論」。
- [x] `DRAMA.md`、`SERIES.md`、`AUTOMATION.md` 照 DRAMA-FLOW.md §與既有文件的關係改（不重寫，各加一段並改關卡表）。

## Steps

- [x] skill 兩份 reference 與 SKILL.md。
- [x] 三份設計文件。

## How to verify

```bash
npm run test:tools
```

## Notes

- 2026-09-27 做完（claude-fable-5-1-video-languages）。每一句提到的指令、端點、關卡、設定名、檔名都對過程式（`tools/video/core/state.mjs` 的 19 步、`review/sync.mjs` 的關卡順序與 payload、`automation/{discuss,flow,series}.mjs`、`apps/api/app/video_automation/admin_api.py`）；後台的名稱照 web 那張的 DoD 與同一棵樹上正在落地的 `admin-video-thread.tsx`／`admin.json`（「討論」、「等模型回覆」、`?kind=one-off`）。
  - `SKILL.md`：frontmatter 改成三條路線（全自動、AI 漫劇、人工錄製）；「AI 漫劇」與「長篇漫劇」合成一列「AI 漫劇（單集與作品）」，關卡寫成文件（故事聖經／設定集、總綱、細綱）與劇本，設定圖、分鏡由 judge 決定（`auto_pick_look`、`auto_approve_storyboard` 開了才自動，預設關）、旁白與成片自動核准；reference 表列出 `series-bible.md`、`discuss.md`，`planner-drama.md` 標成只給遷移前的舊請求。`.claude/skills/youtube-video/SKILL.md` 用 `cp` 同步，`tools/skills.test.mjs` 過。
  - `references/drama.md`：關卡改成兩個站主關卡（文件、劇本）加四個自動的；主幹表 19 步、第 1 步是故事聖經（`POST …/series/<slug>/docs` `kind: "bible"`）、第 4 步是劇本關卡（`script` → `review-push --gate script` → 討論／核准 → `review-pull`）、拿掉單集的選大綱（`## 大綱` 只有選項 A，本機核准備註「依故事聖經」）；指令加 `script`、`review-push --gate script`、`review-pull`；「站主從後台發起」整段照新流程（`one-off-<請求 id 前 8 碼>`、`?kind=one-off`、`drama-requests/next` 只回舊請求）。
  - `references/series.md`：名稱表加故事聖經與討論串；主幹每個核准點寫「討論／核准」與 subject；新增「討論串（每個核准點都有）」一節（端點、variant、`{ reply, revised }`、被取代版本備註「討論後出了新版本」不算 `series_doc_rewrites`、劇本改版走 lint → 重查 → 重送、模型給不出答案的處理、核准後只留紀錄）。
  - `DRAMA.md`：2026-09-27 段落補齊；產線與關卡表第 1 步「站主核准故事聖經」、第 4 步劇本關卡、共 14 步；`Gate` 註明 `script`。`SERIES.md`：流程圖四個【站主核准／退回】改【討論／核准】；「漫劇不走「選大綱」關卡」段涵蓋單集；伺服器表補 `kind`、`bible`、`video_drama_messages`。`AUTOMATION.md`：架構圖多討論的一行；設定表補 `series_doc_rewrites`、`series_episodes_per_month`、`series_max_in_flight`、`auto_pick_look`、`auto_approve_storyboard` 與「目前的提示詞」「用量」兩列；漫劇一節改成「2026-09-27 起：單集與作品走同一條，一輪多一段「討論」」，寫工人一輪的順序（手上影片 → 討論 → 作品 → 舊請求 → 排程草稿），舊路縮成一段。
  - 三份設計文件各只加一段、改表，沒有整份重寫。
- 等 worker 與 web 落地再寫，才寫得出實際的指令與頁面名稱。
