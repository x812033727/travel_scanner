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

**站主 2026-11-11：「之後都用真人版」**——第 7 集起所有新做的集數都走真人版路線（Ref2VA 草稿→獨立挑片與重拍→精修前審片→σ0.5 精修→clip_voice 剪接→成片三輪審片），不再做 3D CG。

**站主 2026-11-12：SeedVR2 升 1080p「先不要升，等整個都確定再來升」**——真人版精修停在 1312×736，剪接放大成 1920×1080；全部集數定案後再一起跑第三段升級（升完要重剪、重匯入，並逐鏡看有沒有變臉）。

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
  - 2026-11-10 13:32 UTC 第 4 集：站主「第 4 集送上後台」。雲端上的匯入資料夾 `zhong-tian-qu-qi-import/zhong-tian-qu-qi-e004-r2/` 還是 CG 版（170.8 秒、CG 季封面），改用真人成片 `_live-e904/.../cut/e904-live.mp4`（223.64 秒）、`e904-live.zh-TW.srt`、舊 session 做的真人封面 `_scratchpad2/thumb4/thumbnail.png`（唐小棠，「第4集　這是妳的退路」），CG 三檔移到 `cg-old/`，以 `import --force` 送上，等站主審成片。`review-files --gate final` 抓回：封面、字幕逐位元相同，預覽 223.64 秒、抽格與成片同畫面。
  - 2026-11-12 第 7 集（第一集「之後都用真人版」）：前置從 script.md 做起（`writer-tools/e007-r2/r2.py`，第 5、6 集的教訓直接寫進規格；build-r2.py 改成從自身位置找 repo）；孫掌櫃與綢緞莊後巷兩張真人參考圖（`live-action/screen-test-e007.py`，站主選 37002／37002）；33 句錄音；78 支草稿＋四輪重拍；唐小棠講台詞一直笑：中性外貌句只對不講話的鏡有效，s08、s20 改從她背後拍、放錄音（route-a 舊法）；新配樂 `cue-market.mp3`（US$0.08）；assemble-v4 面板可讀 `at`；錄音太小聲要先壓縮再拉到約 -12.5 LUFS（單純 volume+alimiter 會碰滿刻度）。精修前與成片兩輪獨立審片（`colab/runs/e907-live/`），預覽 v6 245.04 秒給站主，製作檔已傳 `第007集/製作檔/`（0 差異）。站主看預覽後說「繼續」，2026-11-12 送上後台（封面 s36 c0.8 孫掌櫃手按銀錠＋「第7集　五十兩買方子」），review-files 抓回封面、字幕逐位元相同，預覽 245.08 秒。
  - 2026-11-12 第 8 集：前置 `writer-tools/e008-r2/r2.py`；三張新場景圖（`live-action/screen-test-e008.py`，站主選鏢局 37002、錢府大門 37002、大廳 37001），新配角聲音宗鏢頭 Alnilam、門房 Schedar；47 句錄音；84 支草稿＋五輪重拍（`colab/runs/e908-live/fix1..fix5`）。教訓：唐小棠背影鏡會冒出分身，拿掉她三張臉部參考圖（`drop_pictures`）才乾淨，代價是髮型不一定是兩個丸子頭；許硯站坐要寫成高櫃台（『the countertop as high as his belt, his head at the same height as …』），只寫 STANDING 兩輪都還是坐著；主觀鏡不要送拍攝者（許硯）的參考圖，也要寫明畫面裡沒有桌子，否則他會坐進畫面；秦霜交領不能水平翻轉（會變左衽），左右對調改換片；成片審片抓到 s30 精修後秦霜臉走樣，重拍 10 秒（`duration_seconds` 改 10 可用）一次解決臉與停格。assemble-v4 新增 `clip_af`（從某秒起對片段自帶人聲套濾鏡，rubberband 降調保留共振峰，s19、s22 用；放在組裝而不是 stage.py，重新 stage 不會洗掉）；e908cut.sh 在 loudnorm2 前先限幅 -4 dBFS，否則 loudnorm2 走非線性模式會在 124.77 秒生出爆音（其他集的 loudnorm2.sh 可能也有同樣問題，尚未改共用腳本）。預覽 v1 292.11 秒給站主，站主說「繼續」，2026-11-12 送上後台（封面 s30 c3.0 秦霜扛刀＋唐小棠＋門外街坊，「第8集　太陽還沒落」），review-files 抓回封面、字幕逐位元相同，預覽 292.13 秒。製作檔傳 `第008集/製作檔/`。磁碟滿過一次：先用 `rclone check --one-way --size-only` 確認 `第005集`、`第006集` 的 `_live-e90N`、`_scratchpad-e90N` 在雲端 0 差異，才刪本機那四個資料夾。
  - 2026-11-14 第 9 集：前置 `writer-tools/e009-r2`；80 支草稿（seed 1101/1102）＋兩輪重拍（`colab/runs/e909-live/fix1`、`fix2`），兩位獨立挑片、`pick-review.md`、兩輪成片審片（`cut-review.md`、`cut-review-2.md`）與一輪修片（`review3-trims.tsv`）。教訓：誰手上拿刀要用畫面左右寫（『from screen RIGHT』），並拿掉另一人的參考圖；越肩前景不具名、不送參考圖；舊疤寫『pale whitish, never red』；`vf` 用色鍵改鋪蓋顏色會吃到膚色（s07 許硯的手變藍），拿掉；窗戶壓暗的色鍵取鄰近 3 像素最亮值，才不會在頭髮外緣留白邊；`voice_until` 只決定台詞位置，片段原聲要用 `clip_af` 靜音；`clip_af` 時間從修剪後鏡頭起點算；被剪點切掉的短句可以從草稿切出來當 sfx 補回（s30「門口」）。e909cut.sh 限幅改 -4.4 dBFS 讓 loudnorm2 留在線性模式。成片 248.08 秒、-14.0 LUFS、TP -2.5、cut-jumps 0、audio-qa 0；motion 4.4／靜止 28% 仍 FAIL（夜戲，s05、s21、s31 靜態，沒重拍）。依站主「就這樣一直拍下去」，預覽 v2 傳給站主後直接送上後台（封面 s24 c1.5 刀抵喉，「洞房夜，刀抵喉」），review-files 抓回封面、字幕相同，預覽 248.13 秒。製作檔傳 `第009集/製作檔/`。
  - 2026-11-11 第 6 集：80 支草稿＋五輪重拍（秦霜的刀最難：寫「插在鞘裡」仍常畫在手上，改成不提刀、寫「畫面無兵器」，s23 還要把她框在胸口以上才乾淨），精修前與成片兩輪獨立審片（`colab/runs/e906-live/pick-review.md`、`cut-review{,-2}.md`），剪接表 `hailuo/edit-dh-e906-live.json`，預覽 v4 256.46 秒給站主，製作檔已傳 `第006集/製作檔/`（0 差異）。站主看預覽後說「繼續」，2026-11-11 送上後台（封面 s27 c2.5 許硯遞三個紅紙包＋「第6集　聘禮是三塊肥皂」），review-files 抓回封面、字幕逐位元相同，預覽 256.56 秒。注意：`writer-tools/e001-r2/build-r2.py` 把 REPO 寫死成 /home/user/travel_scanner，在別的 worktree 跑會寫錯地方。
  - 2026-11-10 23:00 UTC 第 5 集送上後台（站主看預覽 v7 後說「繼續」）：`zhong-tian-qu-qi-e005-r2`，成片 250.79 秒，封面 s40 c5.6 三人同框＋「第5集　今天這婚，非成不可」（照第 4 集版型用 ffmpeg drawtext 做，字型文泉驛正黑），標題與說明取 video.json 的 youtube 欄。`review-files --gate final` 抓回：封面、字幕逐位元相同。三輪成片獨立審片 `colab/runs/e905-live/cut-review{,-2,-3}.md`；第 4 輪重拍 s40（fix4，唐小棠回到許硯畫左）；新配樂 `cue-night.mp3`（Lyria US$0.08，111.7 秒）放進 `_series/zhong-tian-qu-qi/music/` 給以後用；s16、s28、s31、s33、s14 的錄音照角色畫面原聲變調（剪接表 _note）。Colab 從 2384.25 用到 2254.28 CU（約 130 CU，含另一個對話同帳號的用量）。
  - 2026-11-10 第 5 集：50 支舊草稿從雲端取回，補拍 28 支；三輪獨立挑片＋重拍（fix1 14 鏡：柴刀從 chopping knife 改寫成 firewood machete；fix2 4 鏡改構圖；fix3 s35 s37 s40），精修前獨立審片 `colab/runs/e905-live/pick-review.md`，剪接表 `hailuo/edit-dh-e905-live.json`，精修進行中（Colab `zt-live`）。站主 13:3x：雲端硬碟在備份中，第 5 集之後的新檔先留在本機，之後再補傳。
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
