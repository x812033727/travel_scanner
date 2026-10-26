# C03 認證與正式主機唯讀交接

現有影片工具權杖已成功通過正式 API 認證，無須重給。預算對帳沒有 HTTP 管理路由；網站管理員權杖也不能代替正式主機操作。此環境目前沒有正式主機 SSH 身分或相應 TCP／VPN 連線。Claude 自己的主機連線不會自動共享到這裡，權杖、密碼、私鑰都不必貼到聊天。

已能連正式主機的 Claude 可以直接做下面的唯讀檢查；不必先部署或變更帳戶。若要由 Codex 執行，須先在環境連線設定提供正式主機 SSH 身分及相應網路存取。

## 給已連線的 Claude

從這個 PR 分支取得相鄰的 `host-budget-metadata-readback.py` 與 `host-budget-metadata-readback.sh`，放到主機的私人暫存目錄；不用切換正式 repo 分支、不用重建容器。先核對：

| 檔案 | SHA256 |
| --- | --- |
| Python | d7c791cf6c34d2a9e043403e297cf1dfeadc15e0a7dfa93005bedbd7be3632ee |
| Shell | 0bf2814c3d6a8a423c30d955c46aa7ed8c2bc8c6d2159744d0b3050a21a341d3 |

在既有正式主機連線執行：

```bash
bash /私人暫存目錄/host-budget-metadata-readback.sh
```

wrapper 使用主機既有 `/root/travel_scanner` Compose 的 api 與 video-worker，Python 以 stdin 執行，不安裝到映像。只查原 C03 與精確新版 `story-everyday-moleskine-c03-remake-20261025`，先驗證 PostgreSQL 的 read-only／repeatable-read，再做參數化 SELECT，最後 rollback。沒有建立帳戶、對帳套用、部署、啟用或供應商請求。

貼回輸出的安全 JSON 即可：帳戶是否存在、US$ 上限、已結／保留／未明總額、可知餘額、API／worker registry 與來源 hash。它不包含 DSN、憑證、環境變數、個別 operation／receipt 或原始 stderr。exit 3 表示只讀資料齊備但製片仍 NOT_READY；exit 4 表示資料或版本未知，需要核對。兩者都不是支出授權。

## 已完成的本地核對

[v2 獨立複查 PASS](host-budget-metadata-independent-recheck.json) 保留首次 MUST_FIX 與原四檔；27項獨立檢查、13組完全 mock shell 及作者16項修正回歸均無正式主機／DB／provider操作。完整[安全範圍](host-budget-metadata-readback.md)、[hash綁定](host-budget-metadata-sourcebinding.json)與[當前連線紀錄](connection-readiness-20261026.json)可核對。sourcebinding 的 awaiting rereview 是修改當時的凍結快照；其後的複查結果以上述獨立收據為準。

舊 `host-admission-readback.sh` 及其 QA 原樣保留。對未知新 slug，舊 CLI 在讀 DB 前先回 preproduction hold，不能據此判定帳戶不存在。最新 media/status 也未列原／新 C03，僅代表不在該 API 的顯示集合，不能推論 DB 無帳戶。

取得真實摘要後，仍須正常處理精確新版 US$25 帳戶的受審註冊／啟用、歷史帳本及全片報價，才能開始真 TTS。其他集的來源、八語與免費準備繼續；片頭片尾已依 PR1860備妥。
