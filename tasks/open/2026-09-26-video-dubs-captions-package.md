---
id: 2026-09-26-video-dubs-captions-package
title: Video dubs: captions follow the dub timeline, the upload package carries the tracks, UPLOAD.md gets the Languages steps
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-09-26T17:59:25Z
completed_at:
branch:
depends_on:
  - 2026-09-26-video-dubs-command
scope:
  - tools/video/core/stages.mjs
  - tools/video/core/captions.mjs
  - tools/video/package
  - tools/video/review
  - .agents/skills/youtube-video/references/publish.md
  - .agents/skills/youtube-video/references/automated.md
  - .claude/skills/youtube-video/references/publish.md
  - .claude/skills/youtube-video/references/automated.md
---

# Video dubs: captions follow the dub timeline, the upload package carries the tracks, UPLOAD.md gets the Languages steps

## Why

配音做出來之後（`video-dubs-command`），還要接上三個地方：選日文配音又開日文字幕的觀眾，字幕要跟配音的聲音走，不是跟 zh-TW 的時間走；上傳包是站主下載的全部東西，音軌要在裡面，`UPLOAD.md` 要寫 Studio「語言」的步驟；審看頁要能試聽四條音軌，第一次上傳前站主聽得到。設計在 `docs/videos/DUBS.md`。

## Definition of done

- [ ] `runCaptions`：某語系有當前的 `dubs/<locale>/timeline.json`（`speech_hash` 與翻譯雜湊都相符）時，`buildCues` 用配音每句真正說話的時間範圍（含倍率）切字幕；manifest 每個語系記 `timing: "dub"` 或 `"narration"`；配音時間軸過期就退回 zh-TW 時間並警告。沒有配音的語系與 zh-TW 字幕一個位元組都不變（快照測試）。
- [ ] `package`：把 `dubs/<locale>.<ext>` 複製到 `upload/dubs/`；`metadata.json` 多 `dubs: [{ locale, file, format, total_frames, tempo_max }]` 與 `skipped_dub_locales: { locale: reason }`（來源是 `fit.json` 與工人寫的 `dubs/<locale>/skipped.json`）；`recordStage` 記 dubs。
- [ ] `UPLOAD.md` 多一節「語言（配音音軌）」，用官方的按鈕名稱：「語言」→「新增語言」→ 選語言 →「配音」旁的「新增」→「選取檔案」→「發布」，每個語系一次；附兩個提醒：系統已自動生成該語言配音時要先刪除，以及一次性的「進階功能」與關閉「允許自動配音」（設定 → 頻道 → 進階設定）。
- [ ] 審看頁（`review/final.html`）每條配音一個播放器，`review-push --gate final` 把音軌一起送上去（既有的分段上傳）。
- [ ] skill：`publish.md` 加多語言音軌一節（資格、步驟、自動配音衝突、第一支實測的結果：Studio 收不收 m4a、私人影片能不能加音軌、原音語言怎麼標）；`automated.md` 的指令表與階段表加 `dub`；`.claude/skills` 的逐字複本同步，`npm run test:tools` 檢查得過。

## Steps

- [ ] 字幕跟配音時間軸；快照測試。
- [ ] `package` 的檔案、`metadata.json`、`UPLOAD.md`。
- [ ] 審看頁的播放器與送審。
- [ ] skill 兩份文件與複本。
- [ ] 第一支在 Studio 實測，結果回寫 `publish.md` 與 DUBS.md 的「第一支要實測」。

## How to verify

```bash
npm run test:tools
node tools/video/cli.mjs captions --slug chatgpt-ads-upgrade      # manifest 的 en 是 timing: dub
node tools/video/cli.mjs package --slug chatgpt-ads-upgrade       # 列出 upload/dubs/en.m4a
```

打開 `upload/UPLOAD.md` 照著在 Studio 做一次；「語言」頁看得到那條音軌，播放器能切換。

## Notes

- 成片的核准綁 `final.mp4` 的雜湊，配音不改它，第二批三支不必重新核准。
- 字幕檔的副檔名跟 `dub` 的 `--format` 走。
- `tools/video/package` 與兩個 skill 目錄也在 `2026-09-26-video-hands-off-worker` 的 scope 裡：那張還沒被認領時這張可以先做，後落地的那張 rebase。
