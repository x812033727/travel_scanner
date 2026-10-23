# 正式主機上的多段式發布：部署暫停檔

正式主機有兩條部署路徑，彼此看不到對方。要在主機上跑任何分成多個階段的發布，先讀完這一頁；
共用的實作是 [`hold.py`](hold.py)，測試是 `python -m unittest discover -s ops/release -v`。

## 兩條路徑，四把鎖

| 路徑 | 做什麼 | 拿哪些鎖 |
|---|---|---|
| 一般部署腳本 `/root/deploy-travel-scanner.sh`（只在主機上，root，mode 700，不在 git 裡） | 一次跑完：fast-forward 到 `origin/main`，`compose up --build -d` 重建全部應用容器（image tag `:local`） | 只拿 `/var/lock/travel-scanner-deploy.lock` |
| 自動部署 timer（`ops/autodeploy/`，2026-10-16 正式機未安裝） | 若日後啟用，每 5 分鐘檢查 `origin/main`、CI、付費工作，再呼叫**上面那支一般部署腳本**。它自己不拿鎖、不建容器；先跑腳本的 `--dry-run`，看到 `exit 3` 就等下一輪 | 跟一般部署腳本一樣，只在腳本執行期間由腳本拿 `/var/lock/travel-scanner-deploy.lock` |
| 分段發布工具（例如 `docs/ai-terms-series/release_host.py`、`docs/ai-news-2026-ytd/deploy_release.py`） | `prepare`（建 `:<sha>` 映像、把當下的容器記成基準）→ 等 CI → `activate`（停服務、`pg_dump`、換上映像）→ 內容階段 `dry-run → drafts → publish-articles → publish-index`。每一段開始前核對容器還是上一段留下的樣子，不是就拒絕 | 每個階段執行期間持有四把：`/var/lock/travel-scanner-deploy.lock`、`/root/mokaair-deploy.lock`、`/run/mokaair-manual-deploy.lock`、`/run/travel-scanner-deployer/deploy.lock` |

鎖只在單一階段執行期間被持有。階段之間鎖是空的，一般部署腳本照樣能跑，容器一被重建，
下一個階段就會因為基準變了而拒絕繼續。2026-09-14 UTC 06:54 `prepare` 完成、07:00 另一個 session
跑了一般部署腳本、`activate` 無法繼續，最後靠一支臨時的 reconcile 工具在 07:23 才啟用。

## 一般部署腳本現在怎麼擋

自 2026-09-14 07:55 起，`/root/deploy-travel-scanner.sh` 遇到下列任一情況就 `exit 3`，
並印出 `NOT DEPLOYING: another release is in progress`：

1. `/root/mokaair-*/state.json` 在 24 小時內修改過，含 `"built_at"`，但既沒有 `"activated_at"`
   也沒有 `"failed_at"`。這只涵蓋「已 prepare、還沒 activate」的那一段。
2. `/root/travel-scanner-deploy.hold` 存在。腳本會把檔案的前 600 bytes 當作理由印出，換行換成空白。

`--dry-run` 只印 `NOTE: a real deploy would refuse to start.` 和理由；`--ignore-hold` 會無視兩條規則照常部署，
只有人工確認過發布目錄之後才可以用。

`activate` 寫入 `activated_at` 之後，第 1 條就不再保護後面的內容階段，這段期間只有暫停檔擋得住。
所以**發布工具自己負責建立與移除暫停檔**，不靠人記得。

## 暫停檔的規則

檔案是 `/root/travel-scanner-deploy.hold`，mode 0644，兩行：

1. 第一行給人看，600 bytes 以內（腳本只印這麼多），例如
   `codex-gemini-tutorials 正在發布 3b8df68c693e（/root/mokaair-gemini-3b8df68c693e，階段 prepare→…→publish-index，開始於 2026-09-14T06:54:00+00:00）；檢查該目錄後才能刪除本檔`
2. 第二行是一個 JSON：`target`（完整 40 字元 SHA）、`release_dir`、`owner`、`phases`、`created_at`。
   `verify` 和 `clear` 只比對 `target` 與 `release_dir`。

兩行都不得含任何密鑰或 `.env` 的內容。

`hold.py` 提供三個函式，全部要求呼叫端**已經持有上面那四把鎖**，helper 本身不拿鎖，也不 import `fcntl`
（主機是 Python 3.14，測試也要能在 Windows 跑）：

| 函式 | 什麼時候呼叫 | 行為 |
|---|---|---|
| `acquire(release_dir, target_sha, owner, phases)` | `prepare` 拿到四把鎖之後、建置與記錄基準之前 | 用 `O_CREAT \| O_EXCL` 建檔，回傳 `"created"`。檔案已存在且指名同一個 `release_dir` 與 `target_sha` 時回傳 `"resumed"`（同一次發布續跑）；指名別的發布、或是人工寫的檔案，就丟 `HeldByAnother`，絕不覆寫 |
| `verify(release_dir, target_sha)` | `activate` 開始時，以及每個內容階段開始時 | 檔案不存在丟 `HoldMissing`；指名別人或無法解析丟 `HeldByAnother`；否則回傳 JSON 記錄 |
| `clear(release_dir, target_sha)` | 最後一個階段成功之後。沒有內容階段的純程式發布，在 `activate` 成功後 | 只刪指名自己的檔案，回傳 `"cleared"`；已經不存在回傳 `"missing"`（發布已經成功，不該因此失敗，但要印出來）；指名別人丟 `HeldByAnother` 並保留檔案 |

失敗或回滾時**不要**呼叫 `clear`：暫停檔留著，工具印出「檢查 `<release_dir>` 之後再解除」。
第 1 條規則此時也還會擋（`failed_at` 已寫入的除外），暫停檔則是不論哪一段失敗都擋。

在發布工具裡引用：

```python
import sys

sys.path.insert(0, "/root/travel_scanner/ops/release")  # 主機上的 checkout
import hold

hold.acquire(
    BASE,
    TARGET,
    "codex-gemini-tutorials",
    ["prepare", "activate", "dry-run", "drafts", "publish-articles", "publish-index"],
)
...
hold.verify(BASE, TARGET)  # activate 與每個內容階段的開頭
...
print("hold", hold.clear(BASE, TARGET))  # 最後一個階段成功後
```

也可以複製 `hold.py` 進發布目錄（`docs/ai-news-2026-ytd/release_hold.py` 就是這個約定的第一份工作本地版本，
格式相同，兩邊互認）。命令列同樣可用，拒絕時 `exit 3`，和部署腳本一致：

```bash
python3 ops/release/hold.py show
python3 ops/release/hold.py acquire /root/mokaair-x-<sha12> <sha40> <owner> prepare activate publish-index
python3 ops/release/hold.py verify  /root/mokaair-x-<sha12> <sha40>
python3 ops/release/hold.py clear   /root/mokaair-x-<sha12> <sha40>
```

## 放棄一個發布

1. 先看發布目錄：`state.json`、各階段的 log 與 `publication-*.json`，確認容器與資料庫現在是什麼狀態。
2. 在發布目錄裡寫下決定（例如 `abandoned.md`：誰、何時、為什麼、容器與資料要不要回復）。
3. 然後才刪暫停檔：`rm /root/travel-scanner-deploy.hold`。

順序不能反過來。若一般部署腳本在暫停檔刪除後執行，就會重建容器，發布目錄裡的基準再也對不上；若日後啟用自動部署 timer，它在刪除後最多 5 分鐘內也可能呼叫一般部署腳本。因此須先決定並記錄，再刪暫停檔。

## 在主機上驗證，不碰正式環境

1. 在暫存目錄用 `hold.acquire` 建一個暫停檔（`--hold-path /tmp/<dir>/hold`）。
2. 用 `sed` 複製一份 `/root/deploy-travel-scanner.sh`：`REPO=` 指到不存在的目錄，
   `LOCK_FILE=` 和 `LOG_DIR=` 指到 `/tmp`，`HOLD_FILE=` 指到剛才的暫停檔。
3. 執行複本應該 `exit 3`，並印出暫停檔第一行。萬一沒被擋下，也只會停在 `cd`，不會 fetch、merge 或建置。
4. `hold.clear` 之後再跑同一份複本，應該放行並停在 `cd`。

下一次真實的多段式發布，在每兩個階段之間到主機跑 `/root/deploy-travel-scanner.sh --dry-run`：
應該印出 `NOTE: a real deploy would refuse to start.` 和暫停檔內容；發布完成後同一個指令不再印出這些。

## 不在這一頁範圍內

- 已經執行完的發布工具（`docs/ai-terms-series/`、`docs/ai-news-2026-09/`）綁死已完成的 SHA 與清單，不會再跑，不要回頭改。
- 主機腳本 `/root/deploy-travel-scanner.sh` 不在 git 裡（加防護前的版本在 `/root/deploy-travel-scanner.sh.bak-20260914-hold`）。
  暫停檔的路徑或格式要改，主機腳本得同步改，而改主機腳本需要站主同意。
- 後台部署中心的主機代理（`apps/api/deployment_agent`、`ops/deployer`，預設關閉）是第四條部署路徑，
  自 2026-10-07 起也認同一個暫停檔與規則 1（`deployment_agent/release_guard.py`，拒絕碼
  `deployment_hold_active`、`deployment_staged_release_in_progress`）；它的 release 佈局仍與一般部署腳本不同，
  見 `ops/deployer/README.md`。
- 自動部署 timer 自己的暫停檔 `/root/travel-scanner-autodeploy.paused`（自動部署失敗後寫下）只擋 timer，
  不擋一般部署腳本與分段發布；規則與格式在 `ops/autodeploy/README.md`。

## 一次性部署的影片工作排空關卡（待安裝）

2026-10-16 的 #1521 部署在預檢後開始，另一筆影片寫稿在建置期間才進入
`running`，最後被 `compose up --build -d` 重建 `video-ai-worker` 打斷。因此開頭的
唯讀預檢、以及未來 auto timer 的第七關，都不能保證重建瞬間安全。

`ops/release/video_stage_drain.sh` 是最後一道關卡，需安裝為
`/opt/travel-scanner-deploy/video_stage_drain.sh`，由主機上**不在 Git 的**
`/root/deploy-travel-scanner.sh` 在正常 `compose up --build -d` 與回滾的同一命令
**各呼叫一次**。主機腳本本來就持有 `/var/lock/travel-scanner-deploy.lock`；手動包裝
與 auto timer 都呼叫它，所以兩條路徑共用此關卡。後台部署中心與分階段發布
另有執行器，須各自審核，不能以此關卡聲稱已受保護。
正式主機補丁在首次呼叫前清除 helper 的 repo、compose 與 marker 測試覆寫環境變數，
讓正常與回滾兩處關卡都使用與主機腳本相同的正式目標；離線測試仍可直接覆寫 helper。

關卡驗證目前只有一個、命令為 `python -m app.video_automation.run_jobs` 的容器。
這個命令在正式機是 PID 1、沒有 entrypoint；RQ 2.12 的第一個 SIGTERM 會停止取
新工作並等待當前 horse 完成。腳本用 `docker container stop --signal=SIGTERM
--timeout=-1`，不讓 Docker 的預設 10 秒 SIGKILL 中斷付費呼叫。停止後重新核對
相同容器 ID、正常退出、非 OOM，並由 PostgreSQL 查 `video_stage_jobs` 的
`running` 筆數必須為 0。查詢失敗、仍有 `running`、容器命令變了或排空失敗都
`exit 3`；腳本不可接著重建。`queued` 與 `uncertain` 不阻擋；也不重新派送任何工作。
排空前開始的工作會先完成，排空後唯一消費者已停，故預檢到重建之間新進工作
只會停在佇列。正常關卡成功後寫入綁定本次隨機 nonce、原始 SHA 與容器 ID 的
root-only ready 收據。若正常 `compose up` 局部失敗並刪掉 worker 容器，回滾只在
同次收據、已重設的原始 checkout、無未解 marker、DB `running=0` 都成立時允許
零容器重建；若 worker 已重啟則再排空一次。正常關卡拒絕時，主機腳本持原部署
鎖把已快進的 checkout 重設至 `LOCAL_SHA` 並讀回，留下失敗收據；worker 可能已停，
不能把重設 checkout 當成部署成功。`--no-rollback` 的故障訊息只指引先核對狀態，
不提供未經 guard 的手動 `compose up` 命令。

送出第一個 SIGTERM 前寫入 `/run/travel-scanner-deploy/video-ai-drain.pending`
（內容是容器 ID）；只有停穩、同一容器 ID、DB `running=0` 後才刪。
若外層 watchdog 在 `docker stop --timeout=-1` 等待期間殺掉 deploy shell，
Docker CLI 與部署鎖可能在子程序結束前仍存活，也可能由 systemd 收掉；不能
假設它們必定同步退出。若未來啟用 auto timer，poller 的 paused 收據會阻止下一輪
自動部署；即使另一個
操作者啟動手動部署，殘留 marker 也會讓 guard 拒絕，避免向仍在排空的 RQ
worker 送出第二個 SIGTERM（RQ 會將第二次視為強制停止）。須唯讀核對 marker
中的容器、RQ job 與 DB 收據，確認工作已終結且 worker 停止後，才由站主單獨
核准清除 marker 與後續重啟；不可直接重送模型。

**安裝計畫（須另外取得主機腳本寫入核准，現在尚未安裝）：**

1. 在分支合併／下次部署前，把經獨立審查的 `video_stage_drain.sh` 與
   `video_stage_host_patch.py` 連同 SHA-256 送到主機暫存目錄；先以本機測試和
   `bash -n` 檢查兩檔。先以 `systemctl is-enabled travel-scanner-autodeploy.timer`
   和 `systemctl list-timers travel-scanner-autodeploy.timer` 記錄 timer 是否安裝／
   啟用；2026-10-16 的正式機未安裝 auto timer，不可把 repo 的 90 分鐘設定與
   paused 收據當作現場保護。若日後啟用，須先核對它呼叫相同已補丁主機腳本。
2. 唯讀核對 `/root/deploy-travel-scanner.sh` 的 SHA-256、700 權限、兩處原始
   `compose up --build -d` 錨點及目前沒有部署鎖。2026-10-16 讀到的 SHA-256 是
   `c6e69658cd22351008a179389e807304cb284052136b3aaf1522ffb281a39370`；
   若已變動，先重新審查而非覆寫。
3. 先跑 `python3 video_stage_host_patch.py --render --host-script
   /root/deploy-travel-scanner.sh`，比較預期兩處插入與 `bash -n`。再以
   `--install --expected-sha256 <剛核對的完整雜湊>` 執行；它持有同一把部署鎖、
   留下 mode 600 原稿備份，原子寫入 mode 700 的 helper 與主機腳本；若後段
   寫入或讀回失敗，仍持鎖原子還原原主機腳本並驗證原始雜湊。
4. 讀回兩檔雜湊，確認主機腳本只出現兩次 helper 路徑、`bash -n` 通過，
   `--dry-run` 仍在更動前返回；再從下一次**已另獲核准**的部署 log 核對兩種
   排空路徑與 DB 狀態。這一步會停止／重啟 worker，安裝本身不呼叫 helper。

**安裝回滾：** 若新關卡設計有問題，先擋住所有新部署入口（如有 auto timer
也保持暫停）、確認無部署鎖／執行中付費工作；用備份的完整雜湊和 `bash -n`
驗證原稿，持同一部署鎖將原稿原子還原為 `/root/deploy-travel-scanner.sh`，維持
mode 700。原稿沒有最後排空關卡，在替代保護審核及安裝前不可再次部署。helper
留存作稽核；若 guard 曾停住 worker 並拒絕，先讀 RQ 與 DB 實況，由站主決定何時
重啟，絕不因回滾腳本而自動重送模型工作。若日後安裝 repo 版本的 auto timer，其 poller
子程序超時設定為 90 分鐘，比 systemd 的兩小時上限早 30 分鐘；離線測試驗證
poller 能寫 exit 124 的 paused 收據，這不是目前正式機已有該收據的證據。超時後
仍需核查 worker 是否已停止與工作收據，不可把退出碼當成已部署。
