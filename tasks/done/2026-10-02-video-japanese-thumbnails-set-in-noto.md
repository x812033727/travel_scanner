---
id: 2026-10-02-video-japanese-thumbnails-set-in-noto
title: Video Japanese thumbnails set in Noto Sans JP instead of the Traditional Chinese font
status: done
priority: P3
area: tools
owner: claude-opus-5-5-thumb-font-ja
claimed_at: 2026-10-02T02:55:20Z
created_at: 2026-10-02T00:38:49Z
completed_at: 2026-10-02T03:21:20Z
branch: claude/thumb-font-ja
depends_on:
  - 2026-10-01-video-thumbnails-bundle-korean-and-simplified
scope:
  - tools/video/render/fonts.mjs
  - tools/video/render/render.test.mjs
  - tools/video/templates/templates.test.mjs
  - package.json
  - package-lock.json
  - tools/video/render/cli.mjs
  - tools/video/templates/templates.mjs
  - .agents/skills/youtube-video/references/publish.md
---

# Video Japanese thumbnails set in Noto Sans JP instead of the Traditional Chinese font

## Why

語言縮圖（`thumbnails/<locale>.jpg`）裡，ko 與 zh-CN 自 `2026-10-01-video-thumbnails-bundle-korean-and-simplified` 起用自己的字型（`fonts.mjs` 的 `LOCALE_FONTS`）。ja 縮圖仍然用 Noto Sans TC、頁面 `lang="zh-Hant"` 畫：假名在 TC 的範圍內所以畫得出來，但漢字是繁中字形（例如「直」「骨」「写」的筆畫與日本的標準字形不同），日本觀眾看得出來不是日文字型。en 不受影響。

## Definition of done

- [x] ja 的語言縮圖用 `@fontsource-variable/noto-sans-jp`（OFL-1.1，先確認）排在字型順序第一，頁面 `lang="ja"`；只用在 ja 的縮圖。
- [x] 現有影片的投影片、主縮圖與 en/ko/zh-CN 縮圖的 frame key 不變（ja 縮圖的 key 會變，這是預期的）。
- [x] `bundledCoverage("ja")` 只多 JP 的範圍；繁中投影片的涵蓋檢查不變。

## Steps

- [x] `npm install -D @fontsource-variable/noto-sans-jp`，lockfile 只留那一筆（別讓本機 npm 版本改寫其他套件的 `peer`／`libc` 欄位）。
- [x] `LOCALE_FONTS` 加 `ja: { font: "noto-sans-jp", family: "Noto Sans JP Variable", lang: "ja" }`，`FONT_PACKAGES` 加套件；`templates.mjs` 的 `page()` 與 `browser.mjs` 已經照 `LOCALE_FONTS` 走，不必改。
- [x] `render.test.mjs`／`templates.test.mjs` 把 ja 從「跟主縮圖同一頁」的斷言移到「有自己字型」那邊。

## How to verify

`node --test tools/video/render/render.test.mjs tools/video/templates/templates.test.mjs`；照前一張票的 Notes 在一支影片的副本上加 ja 縮圖字、`VIDEO_BROWSER_CHANNEL=msedge` 跑 `render`，看 `thumbnails/ja.jpg` 的漢字字形。

## Notes

- 2026-10-02 做 ko／zh-CN 時發現，沒有一起做：不在那張票的完成定義裡。

### 2026-10-02 做完（claude-opus-5-5-thumb-font-ja）

- **套件**：`@fontsource-variable/noto-sans-jp` 5.3.0，授權 OFL-1.1（npm registry 的 `license` 欄位與套件的 `package.json`），解開後約 5.6 MB。跟其他字型一樣放 `devDependencies`、寫 `^5.3.0`。本機 npm 重寫 lockfile 時又改了別的套件的 `peer`／`libc` 欄位，所以 lockfile 只手動併入這一筆與根的 `devDependencies`（`npm ci --dry-run` 確認同步）。
- **程式**：只有 `fonts.mjs` 的 `FONT_PACKAGES` 與 `LOCALE_FONTS` 各多一筆（`ja` → Noto Sans JP、`lang="ja"`）；`page()`、`browser.mjs` 的字型路由與 `bundledCoverage(locale)` 本來就照這兩張表走。scope 多了 `cli.mjs` 與 `templates.mjs`（只改註解：哪些語言有自己的字型）和 `.agents/skills/youtube-video/references/publish.md`（字型安排那句改成 ko、zh-CN、ja 各用自己的字型，en 用 TC）。沒改 `theme.css`。
- **涵蓋**：`bundledCoverage("ja")` 是 TC＋Mono＋JP。JP 的範圍裡有 5,524 個碼位 TC＋Mono 沒有（3,146 個 CJK 統一漢字，例如「侭」U+4FAD）；投影片仍然拒絕它們，ja 縮圖可以畫；ja 不會多出 SC 或 KR 才有的字（「佥」「바」照樣缺）。測試有寫。注意「直」「骨」「写」本來就在 TC 的範圍裡，所以這張票改的是字形，不是涵蓋。
- **畫面鍵不變的證明**（vibe-coding-first-website-2026 的 `video.json`、工作區的 `frames/manifest.json` 與 `timeline.json`；repo 的 i18n 沒有縮圖字，所以在記憶體裡給每個語言一組字）：改前改後 theme hash `387c6c9767343f5d`、68 個狀態的 frame key 摘要 `81d91228a8cd7c6f`（跟工作區 manifest 一致）、32 個段落的 segment key 摘要 `2b5f450147aa3343`（32 個段落檔都在工作區）、主縮圖 `c503eb73c3517738`、en `d1444f971ef14824`、ko `7f50591c9fd9c940`、zh-CN `1b1b8d63ba9d39ae` 完全相同；只有 ja 從 `47b7e208c2c7c6f8` 變成 `a8b5bcc083f9f777`，頁面 `lang` 從 `zh-Hant` 變成 `ja`。
- **實測（Edge，不花錢）**：工作區副本（略過 mp4／wav／m4a／build）加 docs 副本，只在副本的 `i18n/ja.json` 填縮圖字「直感コーディング／写すだけ。今日公開／骨組みから無料で」，`VIDEO_BROWSER_CHANNEL=msedge` 用這個分支與 main 的 `fonts.mjs` 各跑一次 `render`，都結束碼 0、畫出 `thumbnails/ja.jpg`。看圖：這個分支的「直」左下是日本字形的 L 形折筆、「骨」裡面的橫折朝右（日本字形），main 的是繁中字形；main 的「写」比旁邊的字細（跟上一張票看到的簡體字同一個問題），這個分支同一套粗細；句號「。」在這個分支靠左下（日文排法），main 置中。兩次的 `thumbnail.jpg` md5 相同（`854aca9b…`，也跟工作區的一樣），manifest 相同。副本已刪。
- **另開一張**：兩次畫的 HTML 完全相同，但 68 張靜態畫面裡有 13 張 PNG 位元組不同（最低 PSNR 約 30.7 dB，醒目區兩行之間多一條細線），跟 09-30 的工作區比也一樣有差：與這張票無關，是 render 本身每次畫的結果不完全一樣，開了 `2026-10-02-video-render-stills-differ-run-to`（P3）。
