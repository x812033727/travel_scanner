# 備份工具

規則在 [`../BACKUP-BRANCHES.md`](../BACKUP-BRANCHES.md)。兩支腳本都只用 git 的物件與索引，不動工作樹，在 repo 任何 checkout 裡都能跑。

## 推一支片

```bash
export TOBRANCH_TRAILERS="Co-Authored-By: …
Claude-Session: …"          # 這個 session 的署名行，不寫死在腳本裡
cd ~/mokaair-work/videos
B=transfer/curio-h24
T=docs/videos/explainer-series/backup
$REPO/$T/tobranch.sh $B curio-h24 curio-h24 "curio-h24: 成片送審後"
$REPO/$T/tobranch.sh $B _site/curio-h24 _site/curio-h24 "curio-h24: 站上檔案"
$REPO/$T/tobranch.sh $B $REPO/docs/videos/curio-h24 _repo/docs/videos/curio-h24 "curio-h24: 稿子快照"
```

- 每次呼叫在分支上加一個 commit（只 fast-forward），結尾印 `verify mismatches: 0` 才算成功，否則結束碼非 0。
- 超過 95 MB 的檔切成 90 MiB 的 `.partNN`，旁邊放 `.SPLIT`（sha256、大小、`cat X.part* > X`）。同一個檔再推一次會先清掉舊的 part。
- 內容沒變就印 `nothing new` 不推。

## 涵蓋檢查（刪工作目錄前，由沒參與製作的代理跑）

```bash
git fetch origin transfer/curio-h24
$REPO/docs/videos/explainer-series/backup/coverage.sh FETCH_HEAD ~/mokaair-work/videos/curio-h24 curio-h24
```

印 `missing: 0  mismatches: 0` 才算過。第二個參數給 `-` 時只核對分支上每個 `.SPLIT` 跟它的 part 相符（工作目錄已不在時用）。

## 還原

```bash
git fetch origin transfer/curio-h24
git archive FETCH_HEAD curio-h24 | tar -x -C ~/mokaair-work/videos
cd ~/mokaair-work/videos/curio-h24
for s in $(find . -name '*.SPLIT'); do f=${s%.SPLIT}; cat "$f".part* > "$f" && rm "$f".part* "$s"; done
```
