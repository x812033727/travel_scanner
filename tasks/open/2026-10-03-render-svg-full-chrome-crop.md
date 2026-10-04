---
id: 2026-10-03-render-svg-full-chrome-crop
title: render_svg crops about 88px when CHROMIUM_BIN points at full Chrome
status: in-progress
priority: P3
area: tools
owner: claude-opus-5-5-pack-ingest-fixes
claimed_at: 2026-10-04T14:47:32Z
created_at: 2026-10-03T12:04:03Z
completed_at:
branch: claude/pack-ingest-body-length-render-svg
depends_on: []
scope:
  - apps/api/app/guides/pack_ingest.py
  - apps/api/tests/test_guides_pack_ingest.py
---

# render_svg crops about 88px when CHROMIUM_BIN points at full Chrome

## Why

`render_svg` 把 SVG 截成 1600×900 的 PNG（hero.jpg 也從這裡來）。預設挑 `chromium_headless_shell`，截圖完整；
但 `CHROMIUM_BIN` 指到完整版 `/opt/pw-browsers/chromium-*/chrome-linux/chrome` 時，`--window-size=1600,900` 含視窗外框，
截圖底部約 88 px 變白邊（2026-10-03 多位撰稿代理照舊指令設了它，回報 hero 頁尾被截）。目前 ingest 沒設 `CHROMIUM_BIN`，所以正式產物沒受影響。

## Definition of done

- [x] 用完整版 chrome 也產出完整 1600×900（例如偵測非 headless-shell 時多加視窗高度、或改用 `--screenshot` 配 viewport 參數），或明確拒絕該 binary。
- [x] 測試涵蓋：產出 PNG 的尺寸與最底一列像素不是空白。

## Steps

- [x] 重現、修、加測試。（真瀏覽器重現不了，見 Notes）

## How to verify

`CHROMIUM_BIN=/opt/pw-browsers/chromium-1194/chrome-linux/chrome` 下 render 一張頁尾有字的 SVG，檢查 PNG 底部。

## Notes

- `pack_ingest.py` 目前在 `2026-09-14-codex-learning-series`（blocked）的 scope 裡，認領會被拒，要先和那張票協調。
- 2026-10-04 認領（claude-opus-5-5-pack-ingest-fixes，分支 `claude/pack-ingest-body-length-render-svg`，與
  `2026-10-03-body-length-link-only-paragraphs` 同一個 PR）：`2026-09-14-codex-learning-series` 是 `blocked` 沒有 owner，
  `tools/tasks.mjs` 的 `HOLDS_SCOPE` 只有 `in-progress`／`review`，所以它不占 scope。擋下認領的是
  `2026-10-03-illustrated-slides-round-2-a-family`（review，scope 含整個 `apps/api/tests`），它的分支已經以 #1172
  （`b0a264567`，2026-10-03T10:34Z）合併，用 `--force` 蓋過。
- 量測（Windows，2026-10-04，同一頁 1600×900 的 SVG，`--window-size=1600,900`）：
  - Playwright 的 headless shell（`chromium_headless_shell-1243`）：版面 viewport 1600×900，截圖 1600×900 完整。
  - Google Chrome 154.0.8037.93 與 Edge 154：載入時版面 viewport 只有 **1578×802**（外框算進 `--window-size`，寬 22、高 98），
    但 154 的 `--screenshot` 在截圖前把 viewport 撐回視窗大小（畫面上 `innerWidth×innerHeight` 印出 1600×900），所以這台機器上
    舊程式碼不會出現白邊。票上的 `/opt/pw-browsers/chromium-1194` 在 Linux 會（不撐回），這裡沒有那個 build；Playwright 的完整版
    chromium-1234／1243 在這台起不來（WinError 14001）。真瀏覽器重現不了，改用測試裡模擬「版面 = 視窗 − 外框、外框處留白」
    的瀏覽器：舊程式碼在 (22, 98) 與 (0, 88) 兩種外框下最底一列是白的、測試失敗；新程式碼通過。票上的 Linux 驗證命令沒有跑。
- 做法（兩種 binary 都適用，不拒絕完整版）：視窗開成圖片加 `RENDER_MARGIN`（200 px）、截圖後從左上角裁回 1600×900；
  頁面在圖片右下角外一格畫一個 `RENDER_MARK` 洋紅色像素，截圖裡看不到它（外框大過邊距、或截圖比圖片小）就丟
  `PackIngestError`，不寫出被截掉的 PNG。`--headless=new` 不是解法：Chrome 132 起 `--headless` 就是 new mode，154 的兩種寫法量起來一樣。
  `chromium_binary()` 在沒有 headless shell 時本來就會退到 `/opt/pw-browsers/chromium-*/chrome-linux/chrome` 或 PATH 上的
  `google-chrome`／`chromium`，這條退路也一併修好。
- 測試：`test_render_svg_cuts_the_picture_out_of_a_framed_window`（四種外框，含超過邊距要拒絕；CI 一定會跑）與
  `test_render_svg_keeps_the_last_row_in_a_real_browser`（真的 Chromium，`chromium_binary()` 找不到瀏覽器才 skip；
  GitHub 的 ubuntu runner 有 `google-chrome`／`chromium`，所以 CI 上應該會真的跑）。兩個都檢查 PNG 是 1600×900、最底一列與
  最右一欄沒有白點。本機以 `CHROMIUM_BIN` 指向 headless shell、Chrome 154、Edge 154 各跑一次，全過；
  `pack_cli lint --slug codex-terminal-paths --render-dir` 用 Chrome 154 輸出的圖也完整。
