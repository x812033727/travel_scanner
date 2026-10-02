---
id: 2026-10-01-video-thumbnails-bundle-korean-and-simplified
title: Video thumbnails bundle Korean and Simplified Chinese fonts for language thumbnails
status: in-progress
priority: P2
area: tools
owner: claude-opus-5-5-thumb-fonts
claimed_at: 2026-10-02T00:20:38Z
created_at: 2026-10-01T15:22:56Z
completed_at:
branch: claude/thumb-fonts-ko-sc
depends_on:
  - 2026-09-28-video-localized-thumbnails
scope:
  - tools/video/render/fonts.mjs
  - tools/video/templates/theme.css
  - tools/video/render/browser.mjs
  - package.json
  - package-lock.json
  - tools/video/templates/templates.mjs
  - tools/video/templates/templates.test.mjs
  - tools/video/render/plan.mjs
  - tools/video/render/cli.mjs
  - tools/video/render/render.test.mjs
  - .agents/skills/youtube-video/references/publish.md
---

# Video thumbnails bundle Korean and Simplified Chinese fonts for language thumbnails

## Why

語言縮圖（`2026-09-28-video-localized-thumbnails`）只用內建的 Noto Sans TC 與 JetBrains Mono 畫。2026-10-01 在 vibe-coding-first-website-2026 的副本實測：韓文縮圖「바이브 코딩／코드 없이」有 14 個音節內建字型沒有，`render` 把 ko 記成 note 不畫，所以韓文市場永遠拿不到自己的縮圖；簡中縮圖畫得出來，但「写、码、线、费、编、围」等簡體字和旁邊的字粗細明顯不同（unicode-range 有涵蓋，實際字形看起來是別的字型或較細的字重），不夠格上傳。

## Definition of done

- [x] 韓文縮圖能畫：Hangul 由內建字型涵蓋（例如 `@fontsource-variable/noto-sans-kr`），`render` 不再把 ko 記成缺字。
- [x] 簡中縮圖的簡體字與其他字同一套字型、同樣粗細（例如 `@fontsource-variable/noto-sans-sc`），只用在該語言的縮圖，繁中投影片的字型與畫面鍵不變（現有影片的 frame key 不能動）。
- [x] 字型涵蓋檢查（`tools/video/render/fonts.mjs`）照語言判斷：繁中投影片仍然拒絕簡體字。

## Steps

- [x] 查 fontsource 套件授權與大小；決定是否只在縮圖頁面載入（`thumbnailHtml` 加 `lang` 與字型 class）。
- [x] `render.test.mjs` 補測試；用一支影片的副本實際畫 ko 與 zh-CN 看圖。

## How to verify

`node --test tools/video/render/render.test.mjs`；照 `2026-09-28-video-localized-thumbnails` 的 Notes 在副本上 `i18n-sheet`／`i18n-merge`／`render`，看 `thumbnails/ko.jpg`、`thumbnails/zh-CN.jpg`。

## Notes

- 加套件會動 `package.json`／`package-lock.json`，開工前確認沒有別的票持有它們。

### 2026-10-02 做完（claude-opus-5-5-thumb-fonts）

- **套件**：`@fontsource-variable/noto-sans-kr` 與 `@fontsource-variable/noto-sans-sc`，都是 5.3.0、授權 OFL-1.1（npm registry 的 `license` 欄位，lockfile 也記了），解開後約 4.0 MB 與 5.0 MB（TC 是 4.7 MB）。跟現有兩個字型一樣放 `devDependencies`、寫 `^5.3.0`。本機 npm 11.6.2 重寫 lockfile 時會改別的套件的 `peer`／`libc` 欄位，所以 lockfile 只手動併入這兩筆與根的 `devDependencies`（`npm ci --dry-run` 確認同步）。
- **只在該語言的縮圖載入**：`fonts.mjs` 新增 `LOCALE_FONTS`（ko → KR、`lang="ko"`；zh-CN → SC、`lang="zh-Hans"`）。`templates.mjs` 的 `page()` 多一個 `{ locale }` 選項：有自己字型的語言才多一條 `<link>`、改 `lang`、在頁面自己的 `<style>` 裡把 `--font` 改成「自己的字型, Noto Sans TC Variable, sans-serif」；其他頁面一個位元組都不變。`plan.mjs` 只對語言縮圖傳 locale。
- **沒改 `theme.css`**：它的雜湊是每一個 frame key 的一部分，改一個字所有影片都要重畫；字型覆寫放在縮圖頁自己的 `<style>`，所以 scope 裡的 `theme.css` 沒動。另外 scope 加了 `templates.mjs`（`page()`／`thumbnailHtml` 要知道語言）、`plan.mjs`（傳語言）、`cli.mjs`（`localizedThumbnails` 照語言取涵蓋範圍）和兩個測試檔；`.agents/skills/youtube-video/references/publish.md` 原本寫「韓文有幾個音節內建字型缺」，改成現在的字型安排（references 沒有 `.claude` 複本）。
- **涵蓋檢查照語言**：`bundledCoverage(locale)` 是 TC＋JetBrains Mono，加上該語言自己的字型；沒有自己字型的語言（en、ja）與投影片同一份。投影片和主縮圖仍然只看 TC＋Mono，所以只有 SC 字型才有的簡體字（例如「佥」U+4F65，SC 範圍裡有 1,941 個 TC 沒有的字）照樣被拒；測試有寫。注意：常用簡體字（写、码、线……）本來就在 TC 的 unicode-range 裡，所以繁中投影片從來就沒有擋它們，這張票沒有改變這一點。
- **瀏覽器端**：`browser.mjs` 的字型路由改成照 `FONT_PACKAGES` 判斷（KR、SC 可以載，其他字型目錄一律拒絕）；字型載入與「字型沒載完」的檢查改用頁面 `--font` 的第一個字型（沒有 theme 的頁面，例如字幕條，仍是 Noto Sans TC）。
- **畫面鍵不變的證明**：用 vibe-coding-first-website-2026 的 `video.json` 與工作區的 `frames/manifest.json`、`timeline.json` 算改前改後：theme hash `387c6c9767343f5d`、68 個狀態的 frame key 摘要 `0919b6bbc67d3910`、32 個段落的 segment key 摘要 `7dc977ff32a76cf8`（32 個段落檔都在工作區）、主縮圖 key `c503eb73c3517738`，前後完全相同，而且跟工作區裡真的畫過的 manifest 一致。
- **實測（Edge，不花錢）**：工作區副本（略過 mp4／wav／m4a／build）加 docs 副本，只在副本的 i18n 填 ko 與 zh-CN 的縮圖字，`VIDEO_BROWSER_CHANNEL=msedge` 跑 `render`：結束碼 0，畫出 `thumbnails/ko.jpg`（64,415 bytes）與 `thumbnails/zh-CN.jpg`（71,019 bytes），沒有 ko 的缺字 note。看圖：Hangul 全部用 Noto Sans KR 畫出、粗細一致；簡中的「氛围编程／不写代码／今天上线／免费」裡写、码、线、费、编、围跟旁邊的字同一套字型、同樣粗細。重新畫出的 68 個狀態的 manifest `scenes` 跟原本的一模一樣，`thumbnail.jpg` 與抽查的 frame PNG 位元組完全相同（md5 相同）。副本已刪。
- **另開一張**：ja 縮圖仍用繁中字型與 `lang="zh-Hant"`，漢字是繁中字形：`2026-10-02-video-japanese-thumbnails-set-in-noto`（P3）。
