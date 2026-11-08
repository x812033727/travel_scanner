# 種田的備份工具

這一套工具實作 [`../../../../drama/BACKUP-BRANCHES.md`](../../../../drama/BACKUP-BRANCHES.md) 的規則。原本放在 Claude 的 scratchpad 裡（2026-11-08），這裡是一份副本。

用法：先把整個資料夾複製到 scratchpad，再從那裡執行。腳本裡的 `S=` 是當時那個 session 的 scratchpad 路徑，換 session 時要改成新的。

| 檔案 | 做什麼 |
| --- | --- |
| `bk-episode.sh N` | 推真人版第 N 集到 `transfer/zt-live-e00N`，檔案清單由 `bk-lean-list.py N` 產生 |
| `bk-episode.sh cg N` | 推 CG 版第 N 集到 `transfer/zt-cg-e00N`，檔案清單由 `bk-cg-list.py N` 產生 |
| `bk-episode.sh shared` | 推 `transfer/zt-shared`：真人版的跨集檔，加上兩版都用的音效、配樂與腳本，檔案清單由 `bk-shared-split.py live` 產生 |
| `bk-episode.sh cg-shared` | 推 `transfer/zt-cg-shared`：CG 時期的跨集檔，檔案清單由 `bk-shared-split.py cg` 產生 |
| `verify-episode.py <分支>` | 逐檔核對：清單上的每個檔案跟分支裡的雜湊相同，切塊的檔案每塊都比 |
| `coverage.py` | 涵蓋檢查：工作區與 scratchpad 的每個檔案都在某一份清單裡 |

`bk-episode.sh` 的運作方式：

- 每次在同一條分支上加一個 commit，只能 fast-forward，不強推。
- 超過 95 MB 的檔案切成 90 MiB 的塊。
- 每個 commit 附 `README-backup.md`。

另外：

- `FULL=1 bash bk-episode.sh N` 照舊的做法，把那一集的資料夾全部推上去。
- 「第 43–55 集先不管」是站主 2026-11-07 的決定，寫在 `coverage.py` 裡。
