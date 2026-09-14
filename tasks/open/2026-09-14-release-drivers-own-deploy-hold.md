---
id: 2026-09-14-release-drivers-own-deploy-hold
title: Codex 發布工具自己建立與移除部署暫停檔
status: open
priority: P1
area: ops
owner:
claimed_at:
created_at: 2026-09-14T08:13:38Z
completed_at:
branch:
depends_on: []
scope:
  - ops/release
  - AGENTS.md
---

# Codex 發布工具自己建立與移除部署暫停檔

## Why

正式主機有兩條部署路徑，彼此看不到對方：

- **一般部署腳本** `/root/deploy-travel-scanner.sh`：一次跑完。fast-forward 到 `origin/main`，
  再用 `compose up --build -d` 重建全部應用容器（image tag `:local`）。
- **Codex 的分段發布工具**，例如 `docs/ai-terms-series/release_host.py`、`publish_host.py`，
  以及 `docs/ai-news-2026-09/deploy_release.py`。流程是 `prepare`（建 `:<sha>` 映像，把當下的容器記成基準）
  → 等 CI → `activate`（停服務、`pg_dump`、換上準備好的映像）→ 內容階段
  `dry-run → drafts → publish-articles → publish-index`。每一段開始前都核對容器還是上一段留下的樣子，
  不是就拒絕繼續。

兩者共用 `/var/lock/travel-scanner-deploy.lock`，但發布工具只在單一階段執行期間持有它，
階段之間鎖是空的，一般部署腳本照樣能跑。

2026-09-14 真的發生過（時間為 UTC）：

- 06:54–06:55，Codex 為 #486（`3b8df68c`）跑完 `prepare`。
- 07:00–07:02，另一個 session 照一般流程執行 `/root/deploy-travel-scanner.sh`，全部應用容器被重建。
- `activate` 因為基準已變而無法繼續。Codex 臨時寫了 `docs/ai-terms-series/reconcile_built_release.py`
  對齊基準，07:23 才啟用，07:36 發布完。沒有資料受損，但多了一次容器重建和一支臨時工具。

07:55 起，主機上的一般部署腳本（不在 git 裡）遇到下列任一情況會 `exit 3`，並印出
`NOT DEPLOYING: another release is in progress`：

1. `/root/mokaair-*/state.json` 在 24 小時內修改過，含 `"built_at"`，但既沒有 `"activated_at"`
   也沒有 `"failed_at"`。
2. `/root/travel-scanner-deploy.hold` 存在。腳本會把它的前 600 bytes 當作理由印出，換行換成空白。

`--dry-run` 只印 `NOTE: a real deploy would refuse to start.`，`--ignore-hold` 則照樣部署。

**缺口在第 1 條只涵蓋「已 prepare、未 activate」。** `activate` 寫入 `activated_at` 之後，
drafts、publish-articles、publish-index 仍然會因為容器被換掉而拒絕，這段期間只有暫停檔擋得住，
但目前沒有任何發布工具會建立它。下一批 #490（Gemini 教學）的說明寫明 CI 通過後就部署與發布。

## Definition of done

- [ ] 從 `prepare` 開始到最後一個階段成功為止，`/root/travel-scanner-deploy.hold` 一直存在並指名這次發布。
      這段期間任何時刻執行一般部署腳本都會 `exit 3`。
- [ ] 最後一個階段成功後，暫停檔由發布工具移除，而且只移除指名自己的那份。失敗或回滾時保留它，
      並印出人工檢查後怎麼解除。
- [ ] 另一個發布已持有暫停檔時，新的 `prepare` 拒絕開始，不覆寫。
- [ ] 規則寫在 `ops/release/README.md`，`AGENTS.md` 有一段指過去。下一個寫發布工具的 agent
      不看這張票也會照做。

## Steps

- [ ] 新增 `ops/release/hold.py`，只用標準庫，主機是 Python 3.14，不要 import `fcntl`，才能在 Windows 跑測試。提供三個函式：
  - `acquire(release_dir, target_sha, owner, phases)`：用 `O_CREAT | O_EXCL` 建立暫停檔（mode 0644）。
    已存在且指名同一個 `release_dir` 與 `target_sha` 時視為續跑；指名別的發布就拒絕。
  - `verify(release_dir, target_sha)`：每個後續階段開始前呼叫。檔案不存在或指名別人就拒絕。
  - `clear(release_dir, target_sha)`：最後一個階段成功後呼叫，只刪指名自己的檔案。
  - 三者都要求呼叫端已持有發布工具現在會拿的四把共用鎖：`/var/lock/travel-scanner-deploy.lock`、
    `/root/mokaair-deploy.lock`、`/run/mokaair-manual-deploy.lock`、`/run/travel-scanner-deployer/deploy.lock`。
    helper 本身不拿鎖。
- [ ] 暫停檔格式：
  - 第一行給人看，控制在 600 bytes 內，例如
    `codex-gemini-tutorials 正在發布 <sha12>（/root/mokaair-...，階段 prepare→…→publish-index，開始於 <UTC>）；檢查該目錄後才能刪除本檔`。
  - 第二行是一個 JSON，含 `target`、`release_dir`、`owner`、`phases`、`created_at`，給 `verify` 和 `clear` 比對。
  - 不得含任何密鑰或 `.env` 內容。
- [ ] 新增 `ops/release/test_hold.py`，用 `unittest`，以暫存目錄代替 `/root`。要涵蓋：
  - 新建成功，同一發布可以續跑，別的發布被拒。
  - 檔案被刪或被換成別人的時候，`verify` 拒絕。
  - `clear` 不刪別人的檔案。
  - 第一行不超過 600 bytes。
- [ ] 新增 `ops/release/README.md`，寫明：
  - 兩條部署路徑，以及發布工具使用的四把共用鎖（一般部署腳本只拿第一把）。
  - 呼叫時機：`prepare` 拿到鎖之後、建置與記錄基準之前 `acquire`；`activate` 和每個內容階段開始時 `verify`；
    最後一個階段成功後 `clear`。沒有內容階段的純程式發布，在 `activate` 成功後 `clear`。
  - 一般部署腳本實際檢查的兩條規則與 `--ignore-hold`。
  - 放棄一個發布的做法：先檢查發布目錄，在目錄裡寫下決定，再刪暫停檔。
- [ ] 在 `AGENTS.md` 加一小段：要在正式主機跑多段式發布，先讀 `ops/release/README.md`。

## How to verify

- 在 repo 根目錄執行 `python -m unittest discover -s ops/release -v`，全部通過。
- 在主機上驗證整條規則，不碰正式環境：
  1. 在暫存目錄用 `hold.acquire` 建一個暫停檔。
  2. 用 `sed` 複製一份 `/root/deploy-travel-scanner.sh`：`REPO=` 指到不存在的目錄，
     `LOCK_FILE=` 和 `LOG_DIR=` 指到 `/tmp`，`HOLD_FILE=` 指到剛才的暫停檔。
  3. 執行複本應該 `exit 3`，並印出暫停檔第一行。萬一沒被擋下，也只會停在 `cd`，不會 fetch、merge 或建置。
  4. `hold.clear` 之後再跑同一份複本，應該放行並停在 `cd`。
- 下一次真實的多段式發布，在每兩個階段之間到主機跑 `/root/deploy-travel-scanner.sh --dry-run`：
  應該印出 `NOTE: a real deploy would refuse to start.` 和暫停檔內容。發布完成後，同一個指令不再印出這些。

## Notes

- 不要改 `docs/ai-terms-series/`、`docs/ai-news-2026-09/` 裡已經執行完的發布工具。它們綁死已完成的 SHA
  與清單，不會再跑。共用實作放在 `ops/release`，新的發布工具引用或複製它。
- 一般部署腳本只存在於主機：`/root/deploy-travel-scanner.sh`，root，mode 700。
  加防護前的版本在 `/root/deploy-travel-scanner.sh.bak-20260914-hold`。暫停檔的路徑或格式如果要改，
  主機腳本得同步改，而改主機腳本需要站主同意。
- 事件的證據在主機 `/root/mokaair-ai-terms-3b8df68c693e/`：`state-before-external-baseline.json`、
  `reconcile_built_release.py`，以及各階段的 `publication-*.json`。
- 後台部署中心的主機代理（`apps/api/deployment_agent`、`ops/deployer`，預設關閉）是第三條部署路徑，
  啟用前也應該遵守同一個暫停檔。那不在這張票的範圍內。
