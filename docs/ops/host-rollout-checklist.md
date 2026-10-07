# 主機上線清單：每晚備份與自動部署

`docs/ops/auto-deploy-and-cloud-backup-plan.md` 的 repo 端都已合併；這一頁是站主在正式主機上把兩個
timer 開起來的順序，每步寫要看到什麼。細節在 `ops/backup/README.md` 與 `ops/autodeploy/README.md`，
這裡不重抄。順序是：先更新主機 checkout，再裝備份（獨立、先有保護），最後裝自動部署。

## 0. 前置（主機外先準備）

1. GitHub 開一把 fine-grained personal access token：只選 `x812033727/travel_scanner`，權限只給
   `Actions: Read-only`，設到期日。這是自動部署查 CI 用的，跟 `ops/deployer/README.md` 要求的同規格。
2. 自己電腦上產 age 金鑰：

   ```bash
   age-keygen -o mokaair-backup.key      # 印出的 age1... 是公鑰
   ```

   私鑰檔整個放進密碼管理器，主機永遠不放。沒有這份，設定包備份打不開。

## 1. 更新主機 checkout

照 skill `deploy` 跑一次正常部署（`host-deploy.sh`），讓 `/root/travel_scanner` 在最新 main 上；兩個
installer 都從 checkout 複製檔案。部署會重建所有容器，先看預檢的 `paid video work`。

## 2. 備份

```bash
cd /root/travel_scanner
apt install age
docker compose -f docker-compose.prod.yml exec -T postgres psql -U travel -d travel_scanner \
  -Atc "select pg_size_pretty(pg_database_size('travel_scanner'))"
for v in video_media video_work video_reviews; do
  du -sh "$(docker volume inspect travel_scanner_$v -f '{{.Mountpoint}}')"
done
df -h /var/backups
sudo bash ops/backup/install.sh
vi /etc/travel-scanner/backup.env            # BACKUP_AGE_RECIPIENT=age1...
python3 /opt/travel-scanner-backup/backup.py run --dry-run
python3 /opt/travel-scanner-backup/backup.py run
bash /opt/travel-scanner-backup/status.sh     # 要 exit 0
```

要看到的：`/var/backups/travel-scanner/nightly/<ts>/` 裡有 dump、`config.tar.age`、`manifest.json`；
`sha256sum` 對得上 manifest；`status.sh` 印 `last success … (0.x h ago)`。然後照
`ops/backup/README.md` 做一次單份 dump 的還原演練（拋棄式容器、數幾張表、刪容器）。都過了才：

```bash
systemctl enable --now travel-scanner-backup.timer
systemctl list-timers travel-scanner-backup.timer
```

隔天再跑一次 `status.sh`，確認是 timer 自己跑成功的。把量到的大小記進
`tasks/open/2026-10-07-backup-google-drive-offsite.md`，那是決定 Google 雲端硬碟配額的依據。

## 3. 自動部署（乾跑一週再開）

```bash
sudo bash ops/autodeploy/install.sh
vi /etc/travel-scanner/autodeploy.env        # AUTODEPLOY_GITHUB_TOKEN=...；AUTODEPLOY_ENABLED 維持 false
python3 /opt/travel-scanner-autodeploy/autodeploy.py tick --dry-run
bash /root/travel_scanner/.agents/skills/deploy/scripts/host-preflight.sh
systemctl enable --now travel-scanner-autodeploy.timer   # ENABLED=false 時只乾跑
```

要看到的：`tick --dry-run` 每道關卡一行，結尾 `decision: idle`（live 就是 main）或
`would_deploy`；預檢多了 `-- auto deploy --` 與 `-- backups --` 兩段，內容跟剛才看到的一致。

乾跑一週，每天看一次：

```bash
python3 /opt/travel-scanner-autodeploy/autodeploy.py status
journalctl -u travel-scanner-autodeploy --since -1d | grep decision
```

每個 `would_deploy` 都要對應一個綠燈、已合併、沒有暫停檔的 SHA；有 `wait` 就看它的理由合不合理
（靜默期、CI 還在跑、付費影片工作）。順便決定環境檔裡的靜默期、禁止時段與通知 URL
（`ops/autodeploy/autodeploy.env.example`）。

一週後：

```bash
sed -i 's/^AUTODEPLOY_ENABLED=false/AUTODEPLOY_ENABLED=true/' /etc/travel-scanner/autodeploy.env   # 不用重啟
```

等下一次 main 合併，看 `status` 的 `last_deploy`：`exit=0`、`verify=PASS`，以及
`/root/deploy-logs/auto-<ts>.log`。

## 4. 收尾

- 認領 `tasks/open/2026-10-07-autodeploy-rollout-and-skill-docs.md`，把第一次自動部署的 SHA、
  耗時、驗證結果寫進 Notes，`npm run tasks -- done`。
- 從此手動部署前先看 `systemctl is-active travel-scanner-autodeploy.service`；自動部署失敗會寫
  `/root/travel-scanner-autodeploy.paused`，先讀它指的 log 再刪（skill `deploy` 規矩 9、10）。
- Google 雲端硬碟那張票要的決定：帳號與配額、影片卷要送哪些、rclone crypt 密語放密碼管理器、
  保留策略與演練頻率（規劃文件第三節第 7 到 11 項）。
