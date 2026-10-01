---
id: 2026-09-28-video-localized-thumbnails
title: Video localized thumbnails: render one thumbnail per caption locale and upload it under Languages
status: done
priority: P2
area: tools
owner: claude-opus-5-5-localized-thumbs
claimed_at: 2026-10-01T15:02:27Z
created_at: 2026-09-28T02:30:47Z
completed_at: 2026-10-01T15:24:38Z
branch: claude/video-localized-thumbnails
depends_on: []
scope:
  - tools/video/render
  - tools/video/i18n
  - tools/video/package
  - tools/video/core/translations.mjs
  - .agents/skills/youtube-video/references/publish.md
  - tools/video/qa
---

# Video localized thumbnails: render one thumbnail per caption locale and upload it under Languages

## Why

百萬點閱批次要打英文與日、韓、簡中市場，靠多語言音軌（`DUBS.md`）。YouTube 2026 也支援「多語言縮圖」：一支影片對不同語言掛不同縮圖圖檔，觀眾看到符合自己語言的縮圖，官方資料顯示這對非主要語言市場的點閱有明顯幫助。目前產線只出一張縮圖（zh-TW 的 `thumb` 版型），英文與其他語系的縮圖文字沒有本地化。這張票讓 `render` 依每個有字幕或配音的語系各出一張縮圖，`package` 放進上傳包，`UPLOAD.md` 與 `publish.md` 寫清楚怎麼在 Studio 的「語言」下每個語系上傳對應縮圖。

## Definition of done

- [x] `render` 能依 `i18n/<locale>.json` 的縮圖文字，為每個語系各產一張 1280×720 縮圖（沿用 `thumb` 版型，字換成該語系）。
- [x] `i18n-sheet`／`i18n-merge` 收「縮圖文字」這個可翻譯欄位（tag、headline、sub），雜湊比照現有 metadata 欄位。
- [x] `package` 把每語系縮圖放進上傳包（例如 `upload/thumbnails/<locale>.jpg`），`metadata.json` 列出。
- [x] `publish.md` 與 `UPLOAD.md` 寫清楚：多語言縮圖要先有該語系的音軌或字幕，才能在 Studio「語言」分頁的縮圖選項上傳；官方前提與限制照 2026-09 查到的寫。
- [x] `.agents/skills` 與 `.claude/skills` 兩份 publish.md 位元組一致（`npm run test:tools` 檢查）。

## Steps

- [x] 讀 `tools/video/render/`、`tools/video/core/translations.mjs`、`tools/video/i18n/cli.mjs` 現有的縮圖與 metadata 流程。
- [x] 縮圖文字納入 `METADATA_FIELDS` 或另立一組可翻譯欄位，`i18n-sheet` 出底稿、`i18n-merge` 寫回並算雜湊。
- [x] `render` 對每個語系渲染縮圖；`package` 收進上傳包；`qa` 的 thumbnail 檢查每語系各跑一次。
- [x] 更新兩份 `publish.md` 的「多語言」章節與 `UPLOAD.md` 範本。
- [x] 查一次官方頁（support.google.com/youtube/answer/13338784）確認多語言縮圖的前提（要先有多語言音軌）與操作位置。

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

### 2026-10-01 做完（claude-opus-5-5-localized-thumbs）

- **官方頁重讀（2026-10-01，WebFetch）**：頁名「Add Multi-language features to your videos」，「Manage localized thumbnails」一節：長片可以傳不同語言的縮圖，觀眾看到符合自己語言設定的那張；步驟是 Content → 影片 → Upload thumbnail（先傳影片自己的）→ Languages → 點語言名稱 → Thumbnail 旁的 Add →「Update」；整頁多語言功能的前提是能使用進階功能。**頁面沒有明說要先有音軌或字幕**，也沒寫尺寸／數量限制、沒提 API。上面 09-28 那條「要先有音軌」在頁面上找不到原文；能確定的是要點語言名稱，所以那個語言要先列在「語言」頁。`publish.md` 與 `UPLOAD.md` 照這個寫，DoD 第 4 條的「要先有音軌或字幕」改寫成「要先列在語言頁（字幕、標題說明或配音送上去就會列出）」並註明是推論。
- **欄位**：沒有塞進 `METADATA_FIELDS`，另立 `THUMBNAIL_FIELDS`（tag、headline、sub）與 `thumbnailStatus`／`localizedThumbnail`／`thumbnailGap`（`core/translations.mjs`）。原因：lint 的 `namedWith` 與 `qa` 的 captions 項目會讀 metadata 狀態，放進去會讓每支已翻譯的影片多出 lint 警告。雜湊三個字當一筆（`source_hashes.thumbnail`），像 tags 一樣。
- **不擋任何東西**：`i18n-merge` 對縮圖字只印 `note:`、不讓結束碼非零（工人的 `translateLocale` 合併失敗會重試，而工人的提示還不會填這欄）；`render` 對沒字、過期、缺字型、版面塞不下的語系只印 note、不畫；`package` 只收畫的時候的字和現在 `i18n` 一樣的那幾張（`frames/manifest.json` 的 `thumbnail_locales.<locale>.hash`），其他寫進 `metadata.json` 的 `skipped_thumbnail_locales`；`qa` 縮圖項目每張語言縮圖再跑一次同樣檢查，有問題只出 warning（scope 加了 `tools/video/qa`，就是為了這一條）。舊影片：i18n 沒有縮圖字照常 render／package，zh-TW 縮圖不變，四個語言各一條 note。
- **上傳包**：`upload/thumbnails/<locale>.jpg`，`metadata.json` 多 `thumbnails` 與 `skipped_thumbnail_locales`（只在有 `thumbnail.jpg` 時），包檢查要求列出的檔案都在；`packageFiles` 用角色 `thumbnail_<locale>` 附到 publish 審核。`UPLOAD.md` 有東西可說時才多一節「## 4. 各語言的縮圖」，「上傳之後」順延成 5（`tools/video/dubs` 的測試看的是沒有這節時的 4）。A/B 變體只有 zh-TW。
- **`.claude/skills/youtube-video/references/publish.md` 不存在**：`.claude/skills` 只鏡像 `SKILL.md`（`tools/skills.test.mjs`），references 只有 `.agents` 一份，所以 DoD 第 5 條沒有第二份可比，scope 拿掉那條。
- **實測（不花錢）**：vibe-coding-first-website-2026 的工作區副本（略過 mp4／wav／m4a／build）加 docs 副本，`i18n-sheet --parts metadata` → 填 en／ja／ko／zh-CN 的縮圖字 → `i18n-merge`（結束碼 0）→ `render`（`VIDEO_BROWSER_CHANNEL=msedge`，68 個狀態全部重用）：畫出 `thumbnails/en.jpg`（75,751 bytes）、`ja.jpg`（72,602）、`zh-CN.jpg`（71,647），ko 是 note「no bundled font has 바 … 별」（14 個音節）。`localeThumbnails` 會收 en、ja、zh-CN；`qa` 縮圖項目 ok，「language thumbnails checked: en, ja, zh-CN」。把 i18n 換回原本的再 render：四條 note、`thumbnails/` 被清掉、結束碼 0。副本已刪。沒跑 `package`：它要核准過的 final.mp4，副本沒帶。
- **看圖發現**：zh-CN 縮圖的簡體字（写、码、线、费、编、围）粗細和旁邊不一樣，不夠格上傳；韓文幾乎全缺字。開了 `2026-10-01-video-thumbnails-bundle-korean-and-simplified`。工人翻譯員還不會填縮圖字：`2026-10-01-video-worker-translator-fills-the-thumbnail`。網站的「可以上架」卡片還不列 `thumbnail_<locale>` 下載：`2026-10-01-admin-publish-card-offers-each-language`。
