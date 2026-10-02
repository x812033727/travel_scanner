---
id: 2026-10-02-video-render-stills-differ-run-to
title: Video render stills differ run to run at the same frame key
status: open
priority: P3
area: tools
owner:
claimed_at:
created_at: 2026-10-02T03:19:35Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/render/browser.mjs
---

# Video render stills differ run to run at the same frame key

## Why

`render` 用 frame key（theme、HTML、素材的雜湊）當快取鍵，前提是同一個 key 畫出同一張圖。2026-10-02 做 `2026-10-02-video-japanese-thumbnails-set-in-noto` 時，在 vibe-coding-first-website-2026 的副本上用同一台機器、同一個 Edge（`VIDEO_BROWSER_CHANNEL=msedge`）從零畫了兩次，兩次 68 個狀態的 key 與 manifest 完全相同（投影片 HTML 一個位元組都沒變），但 PNG 不是：靜態畫面 55/68 相同、轉場影格 546/687 相同；跟 09-30 工作區裡畫好的那份比，靜態畫面 50/68、轉場 225/687 相同。差最多的靜態畫面 PSNR 約 30.7 dB（`a117aa66e47ab94a`，「需求範本」那頁），肉眼看是第 6、7 行的醒目底色之間多了一條細線，像是醒目區的轉場還沒完全停住就截圖。主縮圖 `thumbnail.jpg` 三次都是同一個 md5。

影響不大：重畫只畫 key 變了的狀態，`assemble` 的 PSNR 檢查也是拿同一次畫的 PNG 比。但跨機器或重畫後比對位元組（例如證明一個改動沒動到畫面）會被這個雜訊干擾，而且醒目底色的細線是看得到的瑕疵。

## Definition of done

- [ ] 同一台機器同一個瀏覽器，同一個 frame key 連畫兩次，靜態畫面位元組相同（或找出無法避免的原因並寫下來）。
- [ ] 醒目區（highlight）截圖時已經停在最終狀態，不會留下行與行之間的細線。

## Steps

- [ ] 找出不穩定的頁面共通點（醒目區轉場？字型載入？GPU 合成？），在 `browser.mjs` 截圖前等動畫結束或關掉合成差異。
- [ ] 加一個能重現的測試或腳本。

## How to verify

在一支影片的副本上，`--workdir` 指到兩個不同的空目錄各跑一次 `render`，比對 `frames/*.png` 的 md5。

## Notes

- 發現於 PR（ja 縮圖字型）的實測，那次只看 frame key 與主縮圖的位元組，沒有追原因。
