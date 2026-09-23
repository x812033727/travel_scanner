# 預檢：暫停檔背後的發布是活的還是被遺棄的

部署腳本拒絕的兩個條件（全文在 `ops/release/README.md` §一般部署腳本現在怎麼擋）：

1. 某個 `/root/mokaair-*/state.json` 在 24 小時內修改過，有 `built_at`、沒有 `activated_at` 也沒有 `failed_at`。這條 24 小時後自動失效。
2. `/root/travel-scanner-deploy.hold` 存在。腳本印出它前 600 bytes 當理由。**腳本不會清掉它**，所以它會一直擋到有人清為止。

第二種驅動（`release_phase.py`＋`host-state/`）**沒有 `state.json`**，規則 1 對它無效，只有暫停檔擋得住；它的階段是 backup → deploy → dry-run → drafts → publish-articles → publish-hubs → verify → clear。

## 證據表

| 看什麼 | 活的發布 | 被遺棄的發布 |
| --- | --- | --- |
| 鎖 `flock -n /var/lock/travel-scanner-deploy.lock true` | 階段進行中會被佔 | 空的（但階段之間也是空的，單獨不能當證據） |
| 驅動行程 `pgrep -af 'release[_]host\|publish[_]host\|deploy[_]release\|release[_]phase\|publish[_]bundle'` | 有 | 沒有 |
| 目錄最後修改時間 | 幾分鐘內 | 停很久（正常 prepare → activate 約 20 分鐘；被遺棄的曾停 6 小時） |
| `prepare.log` 結尾 | 往下走 | 停在 `TRANSFER_REQUIRED bundle -> …/publication/bundle` 之類的交接點 |
| `publication/bundle`、`baseline.json`、`activate.log`、`ci.json`、`predeploy.dump` | 陸續出現 | 空目錄、缺檔 |
| 第二種驅動：`host-state/backup.json` 有、`publisher-state/` 空 | 幾分鐘內會出現下一階段的檔 | 停在 backup 之後 |
| 它等的 CI | 還在跑 | 早就綠了 |
| 它的 target SHA 對 origin/main | 相同或更新 | main 已經超過它；續跑它的 deploy 反而會把站台往回帶 |

同一天被遺棄的 prepare 在這台主機上很常見，「被標記的目錄」不是「有發布在跑」的證據。67 分鐘的靜止是灰色地帶：**把證據攤開用有選項的提問讓站主決定**，不要自己判。

## 站主決定後的三種做法

**A. 無視暫停檔部署**：`host-deploy.sh` 帶 `--ignore-hold`。暫停檔還在，之後每次部署都要再問一次，所以只當一次性的解法。`--ignore-hold` 也會無視新出現的、真正的暫停檔，包裝腳本因此在 `--ignore-hold` 之前自己再檢查一次。

**B. 清掉暫停檔**（要站主同意）：

```bash
cd /root/travel_scanner && python3 ops/release/hold.py show
cd /root/travel_scanner && python3 ops/release/hold.py clear <release_dir> <sha40>
```

用 `hold.py clear`，不要 `rm`：它先 `verify`，暫停檔已經換成別的發布時會以 `HeldByAnother` 拒絕。清完在那個發布目錄留 `hold-cleared-<date>.txt` 與原檔備份，讓擁有它的 session 知道為什麼不見了。`ops/release/README.md` §放棄一個發布 規定的順序：先讀 `state.json`、各階段 log、`publication-*.json`，把決定寫進目錄（例如 `abandoned.md`），最後才動暫停檔。

**C. 把死掉的發布標成 `failed_at`**（改別人的狀態檔，要站主同意）：規則 1 只認 `activated_at` 或 `failed_at`，所以這是提早退休的正規出口。做法照 `release_host.py` 自己失敗時的寫法：每個目錄只在 `built_at` 有、`activated_at` 與 `failed_at` 都沒有時才動；先 `copy2` 成 `state.json.bak-<date>-retired`；寫暫存檔、fsync、複製原檔的 mode 與 owner、`os.replace`；重讀確認；留 `retired-<date>.txt`。做完 `--dry-run` 不再印 `NOTE: a real deploy would refuse to start`，守門恢復可用，值得維持，不要長期靠 `--ignore-hold`。

## 預檢腳本印什麼

`scripts/host-preflight.sh` 只讀檔案：暫停檔內容、規則 1 標記的目錄、24 小時內動過的 `mokaair-*` 目錄、鎖是不是空的、live HEAD 與 origin/main 的 SHA、work tree 乾不乾淨、磁碟、最後一份部署 log 的尾巴。加 `--full` 才印驅動行程與容器清單：分類器曾把一次包含 `ps`、`who`、`last`、`docker images` 的唯讀調查擋成 Production Reads，純讀檔的版本一直都過。列 61 個以上的發布目錄時只印被標記的與 24 小時內動過的，`| tail` 整份清單會把重要的那幾個切掉。
