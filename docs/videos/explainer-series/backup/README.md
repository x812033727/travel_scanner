# 備份工具

> **2026-11-10 起停用。** 站主：備份不再推分支，製作的所有檔案由做片的 session 用 [`todrive.sh`](../../ai-drama-drive/todrive.sh) 直接傳到雲端硬碟 `AI劇/<名稱>/<集數>/製作檔/`，規則在 [`AI-DRAMA-DRIVE.md`](../../AI-DRAMA-DRIVE.md)。`tobranch.sh` 會拒絕執行。下面是舊規則，留作紀錄；「要備份什麼」的清單仍然適用，目的地改成雲端硬碟。

規則在 [`../BACKUP-BRANCHES.md`](../BACKUP-BRANCHES.md)。兩支腳本都只用 git 的物件與索引，不動工作樹。它們推到、讀自
**執行時所在 checkout 的 `origin`**，所以要在該系列備份 repo 的 clone 裡執行（奇聞是 `x812033727/mokaair-video-backup`，
各系列見 BACKUP-BRANCHES.md〈備份推到哪個 repo〉），腳本本身從 `travel_scanner` 的 checkout 叫：

```bash
git clone --depth 1 https://github.com/x812033727/mokaair-video-backup ~/mokaair-video-backup   # 空 repo 也可以
cd ~/mokaair-video-backup
REPO=~/travel_scanner   # 工具所在的 checkout
```

## 推一支片

```bash
export TOBRANCH_TRAILERS="Co-Authored-By: …
Claude-Session: …"          # 這個 session 的署名行，不寫死在腳本裡
cd ~/mokaair-video-backup   # 不是 travel_scanner
B=transfer/curio-h24
T=docs/videos/explainer-series/backup
$REPO/$T/tobranch.sh $B ~/mokaair-work/videos/curio-h24 curio-h24 "curio-h24: 成片送審後"
$REPO/$T/tobranch.sh $B ~/mokaair-work/videos/_site/curio-h24 _site/curio-h24 "curio-h24: 站上檔案"
$REPO/$T/tobranch.sh $B $REPO/docs/videos/curio-h24 _repo/docs/videos/curio-h24 "curio-h24: 稿子快照"
```

- 每次呼叫在分支上加一個 commit（只 fast-forward），結尾印 `verify mismatches: 0` 才算成功，否則結束碼非 0。
- 超過 95 MB 的檔切成 90 MiB 的 `.partNN`，旁邊放 `.SPLIT`（sha256、大小、`cat X.part* > X`）。同一個檔再推一次會先清掉舊的 part。
- 內容沒變就印 `nothing new` 不推。
- 新寫的物件放在暫存的物件目錄，推完就刪，本機 `.git` 不會多一份整集的副本（2026-11-08 推了幾輪 H24、B01 後容器額度滿了）；也不留 `FETCH_HEAD` 和 `origin/transfer/*` 追蹤參照。

## 涵蓋檢查（刪工作目錄前，由沒參與製作的代理跑）

```bash
cd ~/mokaair-video-backup
$REPO/docs/videos/explainer-series/backup/coverage.sh transfer/curio-h24 ~/mokaair-work/videos/curio-h24 curio-h24
```

印 `missing: 0  mismatches: 0` 才算過。第二個參數給 `-` 時只核對分支上每個 `.SPLIT` 跟它的 part 相符（工作目錄已不在時用）。

## 還原

```bash
cd ~/mokaair-video-backup   # 2026-11-09 前推的分支也已搬到這裡
git fetch origin transfer/curio-h24
git archive FETCH_HEAD curio-h24 | tar -x -C ~/mokaair-work/videos
cd ~/mokaair-work/videos/curio-h24
for s in $(find . -name '*.SPLIT'); do f=${s%.SPLIT}; cat "$f".part* > "$f" && rm "$f".part* "$s"; done
```
