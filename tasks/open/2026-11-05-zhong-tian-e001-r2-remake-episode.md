---
id: 2026-11-05-zhong-tian-e001-r2-remake-episode
title: Zhong-tian e001 r2: remake episode 1 (new script, camera-feel rules), stage 2 only, zh cut for the owner
status: in-progress
priority: P2
area: docs
owner: claude-opus-5.5-zt-e043
claimed_at: 2026-11-05T11:10:59Z
created_at: 2026-11-05T11:10:58Z
completed_at:
branch:
depends_on: []
scope:
  - .agents/skills/minimax-h3-runpod/scripts/route_a_st23.sh
---
# Zhong-tian e001 r2: remake episode 1, stage 2 only, zh cut for the owner

## Why

站主 2026-11-05：原版第 1 集打 40 分、參考的《孟婆今天也不想上班》80 分，要比 80 好。稿子與交辦在 `docs/videos/zhong-tian-qu-qi-e001-r2/`（`script.md`、`brief.md`），量法在 `origin/claude/zhong-tian-camera-feel` 的 `camera-feel-study-20261105.md`。預算：站主同意以 RunPod 美元計，估 US$16，**超過 US$25 先停下來回報**。

## Definition of done

- [x] 三鏡試拍（s05、s13、s22）鏡內動量 ≥ 7、靜止幀 ≤ 15%，給站主看數字
- [x] 其餘 35 鏡（每鏡兩個種子），只做到第二段 1312×736
- [x] 中文整句配音、剪接（punch false、slow_max 1.1、interpolate false、duck 3.5／900 ms）、量成片寫進 brief.md 最後一節
- [x] `import --from`（備註「第 1 集重製版 r2，對照原版第 1 集」），只送成片（2026-11-06 01:45，等站主看）

## Notes

- 內部工作編號 901：工作資料夾 `~/mokaair-work/videos/zhong-tian-qu-qi-e901-dh/`、`hailuo/*-dh-e901.json`、`colab/runs/e901/`；
  `docs/videos/zhong-tian-qu-qi-e901` 是本機指向 `zhong-tian-qu-qi-e001-r2` 的連結（`.git/info/exclude`，不進 git），發布 slug 是 `zhong-tian-qu-qi-e001-r2`。
- 製作檔由 `writer-tools/e001-r2/build-r2.py r2` 產生（`r2.py` 是 38 鏡的規格）。
- `route_a_st23.sh` 加了 `NO_UPSCALE=1`；`assemble-v4.mjs` 加了 `punch: false` 與 `duck_ratio`／`duck_release_ms`（預設不變）。
- `colab/runs/_scripts/camera-feel.py` 照研究的量法量片段或成片（第 55 集成片：動量 3.9、靜止 34%）。
- 新配樂：`cue-river`、`cue-warm`（Lyria，各約 US$0.08）。
- 工作資料夾每天推一次到 `transfer/zt-e001-r2-work`（站主同意）。
- 2026-11-05 站主（經審片轉達）：所有集會合成一支長片，r2 各集**不放片名卡、不寫集數、不回顧上一集**，每集第一鏡接上一集最後一鏡；`edit-dh-e901.json` 已拿掉 `title`。系統要換新聲音（還沒定）：系統台詞 `zq901a04`、`a08`、`a35`、`a36` 各自是一支獨立的錄音，換聲音時只重錄這四支、重跑 `asm.sh`，不必重剪。
- 第 2–10 集的 r2 稿子審片正在寫（`docs/videos/zhong-tian-qu-qi-e0NN-r2/script.md`、`production/r2-bible-e001-e010.md`），送過來之前不要開始。
- 2026-11-05 走一遍收尾流程時補的洞：
  - `stage-clips.sh` 的工作資料夾寫成 `e0$N`（901 會變 e0901），改成三位數；`SRC=refined` 改拿第二段 1312×736 的片（r2 不升 1080p）：`SRC=refined bash colab/route-a/stage-clips.sh 901`。
  - `prep-import.mjs`：`video.json` 的 slug 跟編號不同時用它的 slug（901 → `zhong-tian-qu-qi-e001-r2`）；`meta.json` 的 note 要改成「第 1 集重製版 r2，對照原版第 1 集」。
  - `gen-dh.mjs`：內心獨白（emotion 有「嘴閉著」「內心獨白」）與 `data.nospeak` 的人不再加「嘴在動」那句（s08、s38 原本會對嘴）；`build-r2.py` 把 `nospeak` 與 `BUY`（長鏡秒數）帶進 `video.json`。
  - 用已經抽好的草稿在暫存資料夾試剪一次：45 句、面板、配樂、音效、`punch: false`、新的閃避都跑得過（196.7 秒、exit 0）；照新的秒數只有 s35 還會不夠長，改買 12 秒。
- 第二批草稿 v2（31 鏡 × 2）：EU-CZ-1 從 16:01 起沒貨，`scratchpad/r2v2loop.sh` 每次放棄就重開，最多 4 小時。
- 2026-11-05 22:50 站主把 r2 上限從 US$25 提高到 US$28（容器 20:15 重啟，pod 閒置到 21:15 才被站台停掉，多花約 US$2.6）。
- 2026-11-06 審稿改版（`claude/zhong-tian-e001-remake` d5c8ba1ba，已合進來）：台詞不變、配音照用。對已抽片段逐鏡看過：
  - 照用：c14、c17、c25、c29、c33（背景是同一間屋／同一個院子）、c23（有鐵鐐鐵鍊）、c26、c28（刀沒出鞘）、c35（右手握紅紙）、c37（手不在畫面）；c08 剪前 5 秒照用。
  - 重抽（`colab/runs/e901/rev1/spec.json`，種子 9010701／702）：c08b（新鏡，`r2.py` 用 `sid="s08b"`，後面的鏡號與台詞編號都不動）、c18（桌上少第二個空碗）、c38（站位要秦霜、唐小棠、阿令靠井邊由前到後）。
  - 工具：`build-r2.py` 認 `sid`；`cut-qa.py` 認 `s08b` 這種鏡號；`stage-clips.sh` 改讀 `runpod/a`（找不到才讀舊的 `colab/a`）。
- 2026-11-06 01:00 站主把 r2 上限從 US$28 提高到 US$30（審稿改版要重抽 c08b、c18、c38）。容器 01:00 前後又重啟一次，rev1 草稿批次在同一個 pod（2cipw22ie9s3ce）上重跑。
  - rev1 挑片：s08b、s18、s38 都用 9010701（s18 桌上兩個碗；s38 由前到後秦霜、唐小棠、阿令，阿令戴鐵鐐鐵鍊，井不在畫面裡）。舊的 s18、s38 精修片移到 `st2/refined-old`，草稿移到 `st1/out-old`。
- 2026-11-06 成片 197.0 s、39 鏡，量測寫在 `brief.md` 最後一節（動量 6.8、靜止 4%、每句 15.6 字、-13.7 LUFS）；匯入時唯一差異是 24 fps（管線預設 30，這集刻意 24）。
- 2026-11-06 完整備份（站主：「備份要做好所有備份完整」，選每集一條）：`transfer/zt-e043-media` … `zt-e056-media`、`zt-e057-media`、`zt-e001-r2-media`、`zt-series-media`（`_series`、合集、各集發布包資料夾），共約 10 GB、17 條，每條推完都用 ls-remote 對過 commit。
  每條是孤立 commit，根目錄 `README-backup.md` 寫還原方法；沒推的只有工具免費重做的：`clips/`、`segments-v4/`、`review/`、`cut/*.mp4`（成片也在站上）。
- 2026-11-07 站主：「第一集也修掉」。s08 從 0.6 秒、s16 從 1.7 秒起剪（開頭閃一下別的畫面），重剪後 cut-jumps 0，`import --from --force` 重送後台。
- 2026-11-07 獨立審片：嚴重 c03 沒有閃電（親自看過：背影一路走、畫面沒發白）、c16 米缸半缸以上（台詞「都快見底了」）；中等 c12、c13、c02、c35、c32、c28、小禾的兔子是布偶。
  站主：修嚴重與中等，**上限提高到 US$32**。閃電用剪接加：`assemble-v4.mjs` 新增 `flash`（`edit-dh-e901.json` `"flash": {"s03": 0.4}`，加雷聲）；c32、c28 用裁剪；
  c02、c12、c13、c15、c16、c35 重抽（規格交給子代理重寫中）。
