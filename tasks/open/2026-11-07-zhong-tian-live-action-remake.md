---
id: 2026-11-07-zhong-tian-live-action-remake
title: 種田娶妻打天下改成真人版：試鏡、小樣、鎖定後逐集重做
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-11-07T12:00:49Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/series-plans/zhong-tian-qu-qi
---

# 種田娶妻打天下改成真人版：試鏡、小樣、鎖定後逐集重做

## Why

站主 2026-11-07：「種田改成真人版重做」「不要用動畫的」。3D CG 版第 1–6 集 r2 的重抽一直卡在同樣的錯（參考圖帶笑、道具每鏡不一樣），站主決定整部改成真人版。
CG 的重抽佇列（`scratchpad/chainR`–`chainU`）已經停掉，pod 也停了（這次 pod 計 US$11.50），兩個定時自查都改成不准重開 CG 佇列。
計畫在 `docs/videos/series-plans/zhong-tian-qu-qi/production/live-action-plan.md`。

## Definition of done

- [ ] 站主看過真人定妝照、場景圖，以及第 1 集三鏡小樣，點頭鎖定。
- [ ] 第 1–6 集真人版剪好，經過四道審片與獨立審片，匯入後台，站主看過。
- [ ] 每一批花了錢的東西都當天備份並驗證（missing=0 differ=0）。

## Steps

- [x] 0. `cast.json` 的畫風本來就是真人（`look.style`：photorealistic live-action），外貌照用；定妝照拿掉道具（秦霜的刀、小禾的草兔、趙捕頭的鐵尺），由 `production/live-action/screen-test.py` 產生提示詞。
- [x] 1. （2026-11-07）試鏡：三輪共 US$1.44；站主「照你的建議選，唐小棠用齊胸襦裙」，選定的放在 `production/assets/refs-live/`（README 列來源）。三位女主角另加「胸部豐滿一點」的腰上照。原本：10 個角色＋許硯現代裝的真人定妝照、6 張場景圖，各兩個種子（上限 US$8，**等站主點頭**）。
- [x] 2. 主要角色的角度圖（`refs-live/angles/`；女主角從沒改胸部的原圖重畫）。
- [x] 3. 第 1 集三鏡小樣 s23–s25：草稿 6 支（US$0.67），挑 s23-02、s24-01、s25-01，精修（US$1.09），配上原錄音給站主看（`_live-pilot/…/st2/pilot-refined.mp4`）。站主：「是可以 不過語音好像對不上」——真人畫面過關；嘴形與配音差一秒多，原因是模型的嘴照它自己生的語音在動（從 1.2–1.8 秒開始）。台詞改成從草稿語音的開始處放、長度對齊後重做給站主看（`pilot-aligned.mp4`）。正式剪接要把這個對齊做進 `assemble-v4.mjs`。
- [ ] 4. 鎖定：換掉提示詞的畫風句，重建 manifest，preflight 0 錯。
- [ ] 5. 第 1–6 集逐集做，每集上限 US$28。
  - 2026-11-08 第 2 集：草稿、fix1–fix3 重拍、兩輪獨立審片後，站主看 v2 預覽同意，22:38 以 `import --force` 送上後台（`zhong-tian-qu-qi-e002-r2`，封面 s38 真人畫面「第2集　債主上門，要拿人抵」，舊 CG 檔在匯入資料夾 `cg-old/`）；`review-files` 抓回封面、字幕逐位元相同，預覽 247.25 秒。花費約 US$26.6。站主接受、未重拍的：s18 刀刃朝胸口與道具不見、s26 視線近鏡頭（`colab/runs/e902-live/cut-review-2.md`）。
  - 2026-11-08 唐小棠服裝照定妝照（交領短襦闔上、百褶裙），`pilot.py` 的 `TANG_LIVE` 已改，第 3 集 80 支提示詞已重建，開拍等站主。
  - 2026-11-07 17:13 站主「開始拍第1集」：`runpod/live/d1` 78 支草稿（39 鏡、種子 9011101／102），`scratchpad/e901live.sh`；剪接用 `assemble-v4.mjs` 的 `clip_voice: true`（草稿原聲、字幕跟開口時間）。

## 每一集的流程（站主 2026-11-07）

1. 自己審、自己改：挑片後、剪完後各一次獨立審片；嚴重與中等的自己修好再給站主。
2. 有要檢討的就記教訓（skill 規則、寫稿說明、preflight）。
3. 一集做完：推 `claude/zt-e00N-r2`（或真人版的分支）與 `transfer/` 備份；以後要重做時需要的檔案全部備份到（草稿、精修、草稿原聲、參考圖、規格、prompts、剪接表、匯入資料夾）。
4. 刪本機檔案前，兩件都要成立（站主：「當然要後台都送上也都有才能刪除」）：(a) 這集的分支與 `transfer/zt-shared` 都推了、`verify-episode.py` 為 0、`coverage.py` 為 0，並請一個沒參與製作的代理到 GitHub 逐檔核對；(b) 這集已經送上後台（成片、字幕、封面都匯入），並在後台的影片清單逐項確認真的都在。只刪那一集。
5. 前一集在跑的時候，先做下一集的前置（轉真人版提示詞、preflight、需要的參考圖）。

## 已經做的（2026-11-07）

- CG 版最後的狀態都已備份：`transfer/zt-e90N-media-20261107`（第 1–6 集）、`transfer/zt-series-media-20261107`、`transfer/zt-import-dubs-review-20261107`，全部 verify-bk 都是 missing=0、differ=0。
  後來又補了 `…-20261107b`，內容是第 1 集 fix3 的部分草稿與今天畫的定妝照。
- 改定妝照的教訓（畫風要寫系列自己的；舊提示詞照抄會把 CG 畫成真人）已經寫進 storyboard-shot-spec 與 route-a。

## 交接（2026-11-10 06:55 UTC，舊 session 結束前）

- **備份規則已改**（站主 2026-11-10，PR #2059）：不再推任何備份分支；製作檔用 `docs/videos/ai-drama-drive/todrive.sh` 傳到 `videobackup:AI劇/種田娶妻打天下（真人版）/第00N集/製作檔/<工作資料夾名>/`，要 0 differences。環境 Mokaair 已有 `RCLONE_CONFIG_VIDEOBACKUP_*` 與裝 rclone 的 setup script。
- **破例備份（站主 2026-11-10 07:00「破例推分支」，因為舊 session 讀不到 videobackup）**：第 4、5 集與 scratchpad 全部推到 `x812033727/drama-backup-zt`，每條都用 verify-episode.py 逐檔核對 0：
  `transfer/zt-live-e004-drafts`（e904-dh/runpod，908 檔）、`transfer/zt-live-e004-cg`（e904-dh 的 CG 時期 audio/clips/cut/music/segments，222）、`transfer/zt-live-e004-live-a`（_live-e904 的 runpod 精修、clips、first-frames、review，加匯入資料夾 e004-r2 與 zhong-tian-qu-qi-e004-r2，344）、`transfer/zt-live-e004-live-cut`（_live-e904 cut 各版，17）、`transfer/zt-live-e004-live-seg`（segments-v4，127）、`transfer/zt-live-e005-drafts`（e905-dh，第 5 集 50 支草稿，531）、`transfer/zt-scratch-20261110`（兩個 scratchpad 11/09 18:00 之後的檔，4584；`_live-e904` 頂層的 picks.json、live-clips-e904.json 在 `_scratchpad/live-e904-top/`）。超過 95 MB 的檔切成 `.partNN`，`cat X.part* > X` 還原。這 7 條要照 PR #2059 的對照表搬到 `AI劇/種田娶妻打天下（真人版）/第004集/製作檔/`、`第005集/製作檔/` 與 `_共用/製作檔/`，核對後刪分支。
- 第 5 集草稿拍到 50/78 時停下（zt-live 已停，餘額 2384.25 CU）；新 session 從備份分支取回 50 支，`zt-colab-next-ep.sh` 會跳過已有的、只拍剩下 28 支。
- **第 4 集**（`zhong-tian-qu-qi-e004-r2`）：成片 223.6 秒已做完、兩輪獨立審片修好（`colab/runs/e904-live/cut-review.md`、`cut-review-2.md`），預覽給站主看過，站主說「繼續」。**還沒送上後台**（import 被自動權限擋下，要站主明說「第 4 集送上後台」）；**製作檔沒有任何備份**（舊 session 讀不到 videobackup）。剪接表 `hailuo/edit-dh-e904-live.json`、挑片 `colab/runs/e904-live/*` 都在 repo；本機的片段、精修、成片在舊 session 的機器上，新 session 拿不到，要重做就照 repo 的挑片與剪接表重新拍、重精修（約 US$10）。
- **第 5 集**（`zhong-tian-qu-qi-e005-r2`）：拍攝稿已照第 4 集教訓改好（commit c46132110），`colab/runs/e905-live/spec.json` 在 repo；草稿 78 支拍到約 44 支，本機檔案也在舊機器上。新 session 照 chain905live 的步驟（r2 → st1-ep.sh 905 DRY → pilot.py → retake.py → colab-jobs.json 加 output_path）重建清單後再拍。
- **教訓**全在 `.agents/skills/minimax-h3-runpod/references/route-a.md` 最後幾十條（也同步到 PR #2047）。
- Colab：自己的 session 名 `zt-live`；另一個對話在用 Colab 拍祖媽，不要動它。
