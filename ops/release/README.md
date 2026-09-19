# 正式主機上的多段式發布：部署暫停檔

正式主機有兩條部署路徑，彼此看不到對方。要在主機上跑任何分成多個階段的發布，先讀完這一頁；
共用的實作是 [`hold.py`](hold.py)，測試是 `python -m unittest discover -s ops/release -v`。

## 兩條路徑，四把鎖

| 路徑 | 做什麼 | 拿哪些鎖 |
|---|---|---|
| 一般部署腳本 `/root/deploy-travel-scanner.sh`（只在主機上，root，mode 700，不在 git 裡） | 一次跑完：fast-forward 到 `origin/main`，`compose up --build -d` 重建全部應用容器（image tag `:local`） | 只拿 `/var/lock/travel-scanner-deploy.lock` |
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

順序不能反過來。暫停檔一刪，一般部署腳本就會重建容器，發布目錄裡的基準就再也對不上了。

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
- 後台部署中心的主機代理（`apps/api/deployment_agent`、`ops/deployer`，預設關閉）是第三條部署路徑，
  啟用前也應該遵守同一個暫停檔；那是另一張票。
