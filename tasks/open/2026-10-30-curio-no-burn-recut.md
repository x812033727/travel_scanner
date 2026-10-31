---
id: 2026-10-30-curio-no-burn-recut
title: 已燒繁中字幕的新規則奇聞檔案局重新合成成不燒的版本並送審
status: in-progress
priority: P2
area: docs
owner: claude-opus-5-5-no-burn-recut
claimed_at: 2026-10-30T19:39:12Z
created_at: 2026-10-30T19:34:16Z
completed_at:
branch: claude/elastic-hertz-e6fc0b
depends_on: []
scope:
  - docs/videos/history-curiosity/no-burn-recut-20261031
  - docs/videos/curio-h24/i18n
  - tools/video/review/renewal.mjs
  - tools/video/review/renewal.test.mjs
---

# 已燒繁中字幕的新規則奇聞檔案局重新合成成不燒的版本並送審

## Why

站主 2026-10-25 試燒繁中字幕，2026-10-31 決定全部不燒，並要求已燒的全部重新合成。稿子、旁白、插圖都不動。整體計畫在
`docs/videos/history-curiosity/new-rules-migration-20261031.md`（PR 1941）。

## Definition of done

- [ ] 每支都有抽幀確認不燒字幕的新成片，送到 `/admin/videos` 等站主核准，狀態寫在下表。
- [ ] 已公開與已上傳私人的 7 支做好成片與上架包，換片步驟列給站主決定。

## Steps

- [x] h24 試跑：畫面無字幕、總格數不變、配音與 CC 時間軸可沿用。
- [x] 日、越、泰文說明縮到 5,000 位元組內（只刪句子，沒有重新翻譯）。
- [x] `renewal.mjs stage --checks`：片頭在濃縮之後的片也能換版。
- [x] s31-v2 確認是新規則，本機重新合成。
- [x] h24 送審（審核 `541425fb`，pending）。
- [ ] 站主開雲端 session 或登入，確認容器是否還在。
- [ ] 其餘 26 支照 `docs/videos/history-curiosity/no-burn-recut-20261031/cloud-brief.md` 重新合成。

## How to verify

每支的 `final.mp4` 抽 24 格：`ffmpeg -i final.mp4 -vf "fps=1/32,scale=480:-1,tile=6x4" -frames:v 1 scan.jpg`，總格數與舊片相同。
`node --test tools/video/review/renewal.test.mjs`。

## Notes

**h24 試跑的結果（2026-10-31）**

- 舊片同一時間點有字幕、新片沒有；整支抽 24 格都沒有字幕。總格數都是 22,760。
- `burn_in` 改 false 不會讓配音過期：ko、pt、vi、th 的 `currentDub` 都還是 current。en、id 是 stale，原因是配音比翻譯舊，
  跟字幕無關（`dub --dry-run` 顯示 en 只要重唸 1 句）；ja、es 當初就沒配完（只有 `audio/`，沒有 m4a）。
- qa 10/11，唯一沒過的是上面 en、id 的配音過期。成片送審不受影響，打包前要先補配音。

**不要照原計畫做的地方**

- **s30-v2 的本機工作目錄不能用。** 本機 `timeline.json` 是 `895dd939`、`keyframes/manifest.json` 是 `ba55a7c1`，都是後台最舊的一版；
  已核准的是重錄後的 `84bfb9b7` 與改過提示詞的 `f4e45a35`。補跑 clips 會做出旁白和插圖都不對的片，要用雲端容器的。
- **容器不在的代價不只每支 US$2。** 插圖約 US$2（26 支約 US$52），但工作目錄不在時旁白也要重唸，時間軸一變八語配音全部要重做，
  分鏡也要重新核准（生成圖不會一模一樣）。這筆要先給站主看完整範圍。
- **網站保留的檔案救不回來。** 後台只有燒字幕的 final、720p 預覽、聯絡表（每張約 2.8 MB）和旁白 m4a，沒有單張插圖。

**換版的限制**

- `final-renewal` 只收還沒上傳的片；已有 `youtube_video_id` 的 7 支回 409 `video_final_renewal_upload_started`，它們要走別的路。
- 這批的片頭都在濃縮之後（`intro_at: after_first_chapter`），原本 `renewal.mjs stage` 一律拒絕。2026-10-24 那批是在主機用改過的
  stage.mjs 繞過。現在多一個 `--checks`，checks.json 證明這支是用同一個 branding 與 body 合成的才放行。
- `stage` 要的 `--from` 是匯入格式（`meta.json`、`final.mp4`），工作目錄不能直接用，用 `candidate.mjs` 產生。
- 內建瀏覽器的 claude.ai 沒有登入，`ccd_session_mgmt` 也查不到 `session_01…`，所以本機看不到容器。

**s31-v2**

新規則：`origin/codex/curio-s31-new-rules-20261026`（PR 1874，未合併），brief 寫明 2026-10-26 新規則修訂。後台沒有任何審核紀錄，核准只記在本機。
本機 `docs/videos/curio-s31-v2` 是從該分支取來、`burn_in` 改 false，**沒有提交**，以免跟 PR 1874 衝突；PR 1874 合併前 `burn_in` 也要改成 false。
燒字幕的舊檔留在 `mokaair-work/no-burn-recut-20261031/curio-s31-v2/burned-final.mp4`。

**依賴**

`docs/videos/curio-h24/video.json` 的 `burn_in: false` 在 PR 1941 裡，這裡沒有提交。

**另外發現的**

h24 泰文 hashtag 組出來是 `#ตตนคาเมน`（母音被吃掉，原字是 ตุตันคาเมน）。雲端的票寫修好了，但 main 上還是這樣。
