---
id: 2026-09-28-video-localized-thumbnails
title: Video localized thumbnails: render one thumbnail per caption locale and upload it under Languages
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-09-28T02:30:47Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/render
  - tools/video/i18n
  - tools/video/package
  - tools/video/core/translations.mjs
  - .agents/skills/youtube-video/references/publish.md
  - .claude/skills/youtube-video/references/publish.md
---

# Video localized thumbnails: render one thumbnail per caption locale and upload it under Languages

## Why

百萬點閱批次要打英文與日、韓、簡中市場，靠多語言音軌（`DUBS.md`）。YouTube 2026 也支援「多語言縮圖」：一支影片對不同語言掛不同縮圖圖檔，觀眾看到符合自己語言的縮圖，官方資料顯示這對非主要語言市場的點閱有明顯幫助。目前產線只出一張縮圖（zh-TW 的 `thumb` 版型），英文與其他語系的縮圖文字沒有本地化。這張票讓 `render` 依每個有字幕或配音的語系各出一張縮圖，`package` 放進上傳包，`UPLOAD.md` 與 `publish.md` 寫清楚怎麼在 Studio 的「語言」下每個語系上傳對應縮圖。

## Definition of done

- [ ] `render` 能依 `i18n/<locale>.json` 的縮圖文字，為每個語系各產一張 1280×720 縮圖（沿用 `thumb` 版型，字換成該語系）。
- [ ] `i18n-sheet`／`i18n-merge` 收「縮圖文字」這個可翻譯欄位（tag、headline、sub），雜湊比照現有 metadata 欄位。
- [ ] `package` 把每語系縮圖放進上傳包（例如 `upload/thumbnails/<locale>.jpg`），`metadata.json` 列出。
- [ ] `publish.md` 與 `UPLOAD.md` 寫清楚：多語言縮圖要先有該語系的音軌或字幕，才能在 Studio「語言」分頁的縮圖選項上傳；官方前提與限制照 2026-09 查到的寫。
- [ ] `.agents/skills` 與 `.claude/skills` 兩份 publish.md 位元組一致（`npm run test:tools` 檢查）。

## Steps

- [ ] 讀 `tools/video/render/`、`tools/video/core/translations.mjs`、`tools/video/i18n/cli.mjs` 現有的縮圖與 metadata 流程。
- [ ] 縮圖文字納入 `METADATA_FIELDS` 或另立一組可翻譯欄位，`i18n-sheet` 出底稿、`i18n-merge` 寫回並算雜湊。
- [ ] `render` 對每個語系渲染縮圖；`package` 收進上傳包；`qa` 的 thumbnail 檢查每語系各跑一次。
- [ ] 更新兩份 `publish.md` 的「多語言」章節與 `UPLOAD.md` 範本。
- [ ] 查一次官方頁（support.google.com/youtube/answer/13338784）確認多語言縮圖的前提（要先有多語言音軌）與操作位置。

## How to verify

```bash
npm run test:tools
node tools/video/cli.mjs render --slug <slug> --workdir <VIDEO_WORKDIR>
node tools/video/cli.mjs i18n-sheet --slug <slug> --locale en,ja,ko,zh-CN
node tools/video/cli.mjs package --slug <slug>
```

## Notes

- 依 support.google.com/youtube/answer/13338784（2026-09-28 查）：多語言縮圖綁在多語言音軌上，要先有該語系的音軌（或字幕）才能上傳對應縮圖，且只能站主在 Studio 手動上傳，Data API 沒有縮圖多語言的方法。所以這張票只負責「產圖並放進上傳包」，上傳仍是站主動作。
- 服務百萬點閱批次（`docs/videos/MILLION-VIEWS.md`）：那批每支 brief 的「英文市場的包裝」都寫了英文縮圖文字，本票落地後才能一支影片對多語言各掛一張。
- 相依：多語言音軌的 `dub`／`DUBS.md`（`2026-09-26-video-dubs-*` 已完成）。
