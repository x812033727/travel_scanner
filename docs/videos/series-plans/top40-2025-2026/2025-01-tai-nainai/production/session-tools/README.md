# 《恁祖媽今年18》交接：session 工具與第 6 集起點（2026-11-10）

前一個 session（第 1–5 集製作）結束前收進 repo 的東西。新的 session 先讀這份，再讀
[`../RULES.md`](../RULES.md)（在 PR 分支 `claude/drama-branch-backup`，#2047）、[`../LESSONS.md`](../LESSONS.md)、
`.agents/skills/minimax-h3-colab/references/lessons.md`（2026-11-09／10 的第 4、5 集各節）與 `docs/videos/AI-DRAMA-DRIVE.md`。

## 現況

| 集 | 狀態 |
| --- | --- |
| 第 1–5 集 | 都已 `import` 到 `/admin/videos`，**等站主看片核准**。各集的已知瑕疵寫在剪接表 `post/edit-e00N.json` 的 `_note` |
| 第 6 集 | 分鏡已照種田拍法重寫並過開拍前審稿的修正（37 鏡、約 192 秒，`docs/videos/tai-nainai-e006/`）；**還沒花任何 CU** |

- 每集上限：第 6 集起 **40 CU**（站主 2026-11-10，RULES 第四節）。接近上限先停下來問。
- 第 4、5 集約 39、50 CU，第一輪只過一半；超出的一半以上是機器空轉（lessons 有細節與規則）。

## 備份（2026-11-10 起只傳雲端硬碟，不推分支）

- 規則：`docs/videos/AI-DRAMA-DRIVE.md`；每集 `AI劇/恁祖媽今年18/第00N集/製作檔/`，共用 `AI劇/恁祖媽今年18/_共用/製作檔/`。
- 雲端環境「Mokaair」已設好 `RCLONE_CONFIG_VIDEOBACKUP_*`（rclone 直接用 `videobackup:`）；`apt-get install -y rclone` 就能用。
- **第 1–5 集的製作檔還沒傳上雲端硬碟**（前一個 session 讀不到那組變數）。它們最後一次推到舊的備份分支
  （`drama-backup-tn` 的 `transfer/tn-e00N`、`transfer/tn-shared`），主機正在把那些分支搬到雲端硬碟。
  站主同意最後再推一次，第 1–5 集與 shared 的分支都是前一個 session 本機的最終狀態（獨立代理逐檔核對 0 缺 0 錯；第 2、3 集的修正片段在 shared 的 `_scratchpad/fix4/`）。
  確認主機搬家後這些都在雲端硬碟 `AI劇/恁祖媽今年18/` 底下。
- `tn-drive.py`：照 `tn-bk.py` 的分集規則用硬連結排出每一集，交給 `todrive.sh` 傳。工作資料夾換了，先設 `TN_WORK`。

## 工具（從前一個 scratchpad 收進來；路徑改成 `$TN_WORK`，預設 `~/mokaair-work/videos/_tn-work`）

| 檔 | 用途 |
| --- | --- |
| `draft-chain.sh <dir> <manifest…>` | 一鏡一個 manifest 跑草稿／首格片段（timeout 600、重試一次、連三鏡失敗停）；`SS` session 名、`START=1` 開機、`STOP=1` 跑完關機 |
| `refine-chain.sh <dir> <st2 manifest>` | σ0.5 精修到 1312×736 |
| `cut-picks.py picks.txt outdir` | `cNN=<clip>@a-b` → 剪成 17k+5 格、寫 `takes.json` |
| `assemble-v2.sh eNNN <takes.json:refineddir>…` | 抽原聲、合成、跑 QA（`qa/` 四支） |
| `tn-drive.py stage|push|check eNNN|shared` | 傳雲端硬碟 |
| `tn-bk.py` | **停用**（推分支）；只留它的分集規則給 `tn-drive.py` 用 |

注意：`draft-chain.sh` 的 STOP 只在正常跑完時關機。每一個會開機的排程都要用 `trap … EXIT` 保證 `h3.sh stop`（`e006/e006-pics.sh` 是範本），
任何中斷之後先 `colab sessions` 看有沒有還開著的機器。同時只開一個 runtime（種田也用同一個帳號，`tn-` 前綴）。

## 第 6 集從這裡接

`e006/` 裡是已經寫好、還沒跑的東西：

1. `sets.json`：三張圖（Qwen 修圖）——`set-shenjia-zhengting-day-t1`（正廳早上、燈籠熄、鐘面轉開、拿掉左邊小桌）、
   修好的 `set-shenjia-fanting-t1`（一座碗櫃、黑窗、暗門外）、托盤道具圖 `prop-zisha-tuopan-t1`（以 `tray-base.png`＝第 5 集 c20 那套為樣本）。
   參考圖現在都在 `../assets/refs/`；manifest 裡的 `<TN_WORK>/e002/refs/…` 改成你的 refs 路徑。挑好的圖放進 refs（與 `assets/refs/`）。
2. `stills.json`／`make_stills.py`：28 張首格（32 鏡有臉的鏡，共用：c05→c11、c06→c08、c18→c22、c19→c23），每張畫兩個種子，**挑首格跟挑片一樣嚴**
   （四分之三側臉、眼睛明顯看一邊、建邦戴眼鏡、月棠一條辮子垂右肩、戒指只在左手、前景沒有多的東西）。
3. `make_ff.py`：挑好的首格放 `e006ff/pick/<鏡>.png` 後產生首格片段的 manifest。
4. `ref-rest.json`：參照路線的插鏡（c12、c17、c20、c33、c37）；refs 修好後重跑 `compile.py 6 --manifest` 比較保險（缺白天圖會直接報錯）。
5. `e006-pics.sh`：畫圖排程的範本（等別人的 runtime 停、開機、畫圖、等挑圖旗標、畫首格、`trap` 關機）。
6. 錄音：`node docs/videos/series-plans/zhong-tian-qu-qi/production/hailuo/local/lines.mjs` 重錄（前一個 session 錄的 25 句沒有收進來）。
7. 之後：首格片段與插鏡草稿 → 獨立挑片 → 首格修正 → 有臉的參照鏡精修 → 剪接表 `post/edit-e006.json`（照第 5 集）→ 組片 → 獨立審片 → 不花錢的修正 → import → 傳雲端硬碟。
