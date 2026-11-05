# 給雲端 session 的交接單：把已燒字幕的 26 支重新合成

站主 2026-10-31 決定奇聞檔案局全部不燒字幕，已燒的要重新合成。稿子、旁白、插圖都不動。這批的工作目錄只在你的容器（`/root/mokaair-work`），網站上的成片已燒字幕，不能當來源，所以這件事只有你做得到。

票：`tasks/open/2026-10-30-curio-no-burn-recut.md`。本機已用 `curio-h24` 試跑過，做法與結果寫在票上。

## 第一步：先回報，不要動手

逐支看下面 26 支的工作目錄，把結果寫到票的〈容器盤點〉，推上分支：

- 有沒有 `keyframes/manifest.json`，manifest 列的圖檔是否都在
- 有沒有 `audio/`、`timeline.json`、`music/`、`clips/manifest.json`
- `sha256sum timeline.json` 是否等於後台 audio 審核最新一筆的 `content_sha256`
- 剩餘磁碟

**任何一支缺插圖或旁白檔，那一支就停下來，不要重畫也不要重唸。** 重畫要站主先核准預算，而且重唸會改時間軸，八語配音都要重做。

```
已公開：curio-s18-v2 curio-s29-v2
已上傳私人：curio-s01-v2 curio-s02-v2 curio-s03-v2 curio-s08-v2 curio-s11-v2
未上傳：curio-s04-v2 curio-s05-v2 curio-s06-v2 curio-s09-v2 curio-s10-v2 curio-s13-v2 curio-s14-v2
        curio-s17-v2 curio-s23-v2 curio-s24-v2 curio-s25-v2 curio-s26-v2 curio-s27-v2 curio-s28-v2
        curio-s30-v2 curio-s34-v2 curio-s38-v2 curio-s39-v2 curio-s40-v2
```

`curio-s30-v2` 本機也有工作目錄，但那是第一版旁白（`895dd939`），已核准的是後來重錄的 `84bfb9b7`，所以要用你容器裡的。

## 第二步：一次一支重新合成

先把 `origin/claude/elastic-hertz-e6fc0b`（或它合併後的 main）併進來，`renewal.mjs stage --checks` 和 `candidate.mjs` 才能用。每個 `cli.mjs` 指令照舊加 `NODE_USE_ENV_PROXY=1 NODE_NO_WARNINGS=1`。

1. `docs/videos/<slug>/video.json` 的 `subtitles.burn_in` 改 `false`，提交。
2. 你先前刪過 `narration.wav`，用 `tts --slug <slug> --dry-run` 確認**要合成的字數是 0**，再跑 `tts --slug <slug>` 從快取接回來。字數不是 0 就停，那支記在票上。
3. `timeline.json` 的 sha256 要跟盤點時一樣，否則停。
4. `assemble --slug <slug>`。
5. 新舊成片的總格數要相同（`ffprobe -show_entries stream=nb_frames`），舊片的格數從已核准的 final 審核讀。
6. 整支抽 24 格看有沒有字幕，不能只看一格：
   `ffmpeg -i final.mp4 -vf "fps=1/32,scale=480:-1,tile=6x4" -frames:v 1 scan.jpg`
7. `captions --slug <slug>`、`qa --slug <slug>`，結果記在票上。
8. **未上傳的 19 支**送暫存（不會送審）：

   ```
   node docs/videos/history-curiosity/no-burn-recut-20261031/candidate.mjs <slug> <workdir> <new-dir>/candidate
   node tools/video/review/renewal.mjs stage --from <new-dir>/candidate --out <new-dir>/staged \
     --original <已核准的舊 final> --body <workdir>/build/body.mp4 \
     --branding <workdir>/branding.json --checks <workdir>/checks.json
   ```

   舊 final 的 sha256 必須等於後台目前的 final 審核；`upload/final.mp4` 不對時用 `review-files` 從網站取。
9. 把 `<new-dir>/staged/renewal-candidate.json` 複製到 `docs/videos/history-curiosity/no-burn-recut-20261031/receipts/<slug>.json`，提交推上。收據只有雜湊和中繼資料，沒有祕密。本機這邊會用站主已登入的瀏覽器送審。
10. **已公開與已上傳的 7 支**：`stage` 會拒絕，網站也不讓換版。做到第 7 步就好，保留 `final.mp4`，在票上記下 sha256。檔案怎麼交給站主，等站主決定。
11. 確認下一支的磁碟夠，再刪這一支的 `build/video.mp4`、`segments/`。`build/body.mp4` 和 `final.mp4` 留到站主核准。

## 不要做的事

- 不核准任何審核，不用 `approve`，不跑 `renewal.mjs submit`，不動 YouTube。
- 不重畫、不重唸、不重配音。花費應該是 0；看到要花錢的指令就停下來回報。
- 不要平行合成，容器磁碟 2026-10-26 爆過一次（ENOSPC）。
- 記得掛著 Monitor，session 一閒置容器就會回收，背景工作會被殺（票 `2026-10-25-pr-1844-v2-s09-s11-s14` 的 06:05 紀錄）。
