---
id: 2026-10-02-video-render-stills-differ-run-to
title: Video render stills differ run to run at the same frame key
status: done
priority: P3
area: tools
owner: claude-opus-5-5-render-determinism
claimed_at: 2026-10-02T04:46:32Z
created_at: 2026-10-02T03:19:35Z
completed_at: 2026-10-02T05:50:49Z
branch: claude/render-deterministic-stills
depends_on: []
scope:
  - tools/video/render/browser.mjs
  - tools/video/render/repeat.mjs
  - tools/video/render/render.test.mjs
---

# Video render stills differ run to run at the same frame key

## Why

`render` 用 frame key（theme、HTML、素材的雜湊）當快取鍵，前提是同一個 key 畫出同一張圖。2026-10-02 做 `2026-10-02-video-japanese-thumbnails-set-in-noto` 時，在 vibe-coding-first-website-2026 的副本上用同一台機器、同一個 Edge（`VIDEO_BROWSER_CHANNEL=msedge`）從零畫了兩次，兩次 68 個狀態的 key 與 manifest 完全相同（投影片 HTML 一個位元組都沒變），但 PNG 不是：靜態畫面 55/68 相同、轉場影格 546/687 相同；跟 09-30 工作區裡畫好的那份比，靜態畫面 50/68、轉場 225/687 相同。差最多的靜態畫面 PSNR 約 30.7 dB（`a117aa66e47ab94a`，「需求範本」那頁），肉眼看是第 6、7 行的醒目底色之間多了一條細線，像是醒目區的轉場還沒完全停住就截圖。主縮圖 `thumbnail.jpg` 三次都是同一個 md5。

影響不大：重畫只畫 key 變了的狀態，`assemble` 的 PSNR 檢查也是拿同一次畫的 PNG 比。但跨機器或重畫後比對位元組（例如證明一個改動沒動到畫面）會被這個雜訊干擾，而且醒目底色的細線是看得到的瑕疵。

## Definition of done

- [x] 同一台機器同一個瀏覽器，同一個 frame key 連畫兩次，靜態畫面位元組相同（或找出無法避免的原因並寫下來）。
- [x] 醒目區（highlight）截圖時已經停在最終狀態，不會留下行與行之間的細線。

## Steps

- [x] 找出不穩定的頁面共通點（醒目區轉場？字型載入？GPU 合成？），在 `browser.mjs` 截圖前等動畫結束或關掉合成差異。
- [x] 加一個能重現的測試或腳本。

## How to verify

在一支影片的副本上，`--workdir` 指到兩個不同的空目錄各跑一次 `render`，比對 `frames/*.png` 的 md5。

## Notes

- 發現於 PR（ja 縮圖字型）的實測，那次只看 frame key 與主縮圖的位元組，沒有追原因。
- 2026-10-02 claude-opus-5-5-render-determinism：重現。vibe-coding-first-website-2026 用 Edge 從空目錄畫兩次：靜態 56/68、轉場 238/687 相同。原因有兩個，都不在 theme 或模板：
  1. **截圖追不上 seek。** 09-30 工作區的 `a117aa66e47ab94a.png` 跟它自己的 `-t11.png` 位元組完全相同：靜態畫面拍到的是最後一格轉場（面板還差半個像素沒落定，所以第 6、7 行醒目底色各自反鋸齒，中間疊出一條亮線）。同樣地，標題頁的 t00 有一次拍到半透明的標題，是動畫暫停那一刻的畫面，不是 seek 到 0 之後的。修法：`seekAnimations` 設完時間後等兩個 requestAnimationFrame 再截圖。
  2. **GPU 與合成執行緒的點陣化差異。** 只加 1 時，大字頁（big、title）的進場文字邊緣每次仍差最多約 110 的色階：進場元素有自己的合成層，合成器在什麼比例、什麼時候重新點陣化不固定。逐一試啟動旗標（每組 3 次、4–6 個場景）：只 `--disable-gpu` 靜態全同、轉場 41/56；只 `--disable-threaded-animation` 靜態 2/4；兩個都加 56/56 全同（不等 rAF 也全同，但 rAF 留著當保險，成本約每格 33 ms）。所以 `LAUNCH_ARGS = ["--disable-gpu", "--disable-threaded-animation"]`。
- 驗證（修正後，兩個空的 `--workdir` 各跑一次 `render`）：靜態 **68/68**、轉場 **687/687** 位元組相同，`thumbnail.jpg`、`contact-sheet.png` 也相同；`repeat.mjs` 全片兩次也是 68/68、687/687。`a117aa66e47ab94a.png` 第 6、7 行從 y=524 到 629 是同一個顏色，沒有細線。整片 render 383 s／408 s（修正前 301 s／438 s），軟體點陣化沒有明顯變慢。
- **frame key 沒變**（theme.css 與模板 HTML 都沒動），所以舊的快取畫面不會自動重畫；軟體點陣化的文字反鋸齒跟 GPU 版本有細微差異（肉眼看不出），同一支影片新舊畫面混用沒有問題。想讓舊影片的位元組也一致，用 `render --force` 重畫。
- 重現腳本：`node tools/video/render/repeat.mjs --slug <slug> [--channel msedge] [--runs 2] [--scenes id,id] [--out dir]`，每次開新的瀏覽器畫同一批狀態、只在記憶體比 md5，不寫工作目錄；有差就 exit 1。`render.test.mjs` 加了比對邏輯與啟動旗標的測試。
- 09-30 的那份與現在的畫面差很多（轉場 225/687），沒有追是不是 Edge 版本不同；跨版本的瀏覽器本來就不保證位元組相同，這張票只處理同一台機器同一個瀏覽器。
