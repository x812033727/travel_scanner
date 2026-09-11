---
id: 2026-09-11-ci-minio-minio-latest-quay-io
title: CI 拉不到 minio/minio:latest，改用 quay.io 並釘版本
status: done
priority: P1
area: ops
owner: claude-opus-5-guides
claimed_at: 2026-09-11T22:51:20Z
created_at: 2026-09-11T22:51:16Z
completed_at: 2026-09-11T23:08:03Z
branch: claude/ci-minio-quay-pin
depends_on: []
scope:
  - .github/workflows/ci.yml
  - docker-compose.community.yml
---

# CI 拉不到 minio/minio:latest，改用 quay.io 並釘版本

## Why

2026-09-11 22:32 起，`api` 與 `full-stack-smoke` 兩個必要 check 同時開始失敗，
停在啟動 MinIO 的 step，而且都在 1 秒內就死（健康檢查迴圈跑完要 30 秒，代表
`docker run` 自己就失敗了）。完整 job log 裡的訊息是：

```
Unable to find image 'minio/minio:latest' locally
docker: Error response from daemon: pull access denied for minio/minio,
  repository does not exist or may require 'docker login':
  denied: requested access to the resource is denied
```

**不是 rate limit**：同一個 job 裡 `postgres:17-alpine` 與 `redis:7.4-alpine` 都正常
拉下來了。是 MinIO 在 Docker Hub 上的公開映像不再開放匿名拉取。

直接查 registry 確認，同一份映像在 quay.io 仍然公開：

| image | 結果 |
| --- | --- |
| `docker.io/minio/minio:latest` | HTTP 401 |
| `quay.io/minio/minio:latest` | HTTP 200 |

這會擋住這個 repo 之後的**每一個** PR，main 下次跑也會紅，所以是 P1。
發現時它正擋著 #404（`web` 已經綠了，卡在這兩個 infra check）。

## Definition of done

- [x] `api` 與 `full-stack-smoke` 能把 MinIO 拉起來，兩個 check 回到綠。
- [x] 三處 `minio/minio:latest` 全部改掉，包含本機開發用的 compose 檔——
      同一個拉取失敗在本機也會發生，只修 CI 等於只修一半。
- [x] 映像釘到確切版本，不再用 `:latest`。

## Steps

- [x] `.github/workflows/ci.yml:56`（`api` 的 Start private S3 integration companion）
- [x] `.github/workflows/ci.yml:214`（`full-stack-smoke` 的 community 測試服務）
- [x] `docker-compose.community.yml:5`

## How to verify

CI 上 `api` 與 `full-stack-smoke` 轉綠即是證明——這兩個 job 本來就是唯一會拉
MinIO 的地方，本機沒有 docker 可以先行驗證。

拉取權限本身可以不靠 docker 直接查：

```bash
curl -sS -o /dev/null -w "%{http_code}\n" \
  "https://quay.io/v2/minio/minio/manifests/RELEASE.2025-09-07T16-13-09Z" \
  -H "Accept: application/vnd.docker.distribution.manifest.v2+json,application/vnd.oci.image.index.v1+json"
```

## Notes

- 釘的版本是 `RELEASE.2025-09-07T16-13-09Z`，是 quay.io 上最新的正式 release，
  與該處 `latest` 指向同一版（兩者都是 2025-09-07）。刻意不用 `.hotfix.*` 分支：
  那是給有支援合約的使用者的，CI 用不到。
- `:latest` 正是讓這次失敗看起來像隨機失敗的原因——上游改了發佈方式，日誌上卻只
  顯示一個 pull 失敗。釘版本之後，同類變動會變成一個明確的「這個 tag 不見了」。
- 這次是先誤判成暫時性 registry 問題、重跑一次之後才拉完整 log 找到真正訊息的。
  下次遇到 1 秒內失敗的 container step，直接看 job log 裡 `docker:` 開頭那一行，
  MCP 的 tail 只會給到 service container 的 teardown。
