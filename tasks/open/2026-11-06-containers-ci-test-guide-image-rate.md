---
id: 2026-11-06-containers-ci-test-guide-image-rate
title: containers CI：test-guide-image-rate-limit.py 的 free_port 兩次可能拿到同一個埠，nginx -t 偶發 ssl_certificate 錯誤
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-11-06T13:42:21Z
completed_at:
branch:
depends_on: []
scope:
  - tools/test-guide-image-rate-limit.py
---

# containers CI：test-guide-image-rate-limit.py 的 free_port 兩次可能拿到同一個埠，nginx -t 偶發 ssl_certificate 錯誤

## Why

PR #2030（只改 docs/ 與 tasks/）的 `containers` job 在 2026-11-06 13:40 UTC 紅了：`tools/test-guide-image-rate-limit.py` 的 `nginx -t` 回報
`no "ssl_certificate" is defined for the "listen ... ssl" directive in nginx.conf:35`。第 35 行是第一個（純 HTTP）server 的 `server {`，
不是 TLS server。同一個 base commit 在 main 上同一天 05:49 是綠的，這支 job 的第一步 `nginx -t -c ci-validate.conf` 也過了。

原因：`free_port()` 連續叫兩次（`port`、`tls_port`），每次 bind 到 0 再關掉；Linux 很常把剛釋放的臨時埠再發一次，
兩個 server block 就 listen 到同一個 `127.0.0.1:PORT`，其中一個帶 `ssl`，nginx 把那個位址當成 TLS 位址，純 HTTP 的 server 沒有憑證就報錯。

## Definition of done

- [ ] `tools/test-guide-image-rate-limit.py` 兩個埠保證不同（例如迴圈取到不同的為止，或一次開兩個 socket 再一起關）。
- [ ] containers job 連跑幾次都綠。

## Steps

- [ ] 改 `free_port()` 的用法：`while tls_port == port: tls_port = free_port()`，或同時持有兩個 socket 取埠。
- [ ] 本機用 nginx 映像跑一次 `python3 tools/test-guide-image-rate-limit.py /usr/sbin/nginx`。

## How to verify

```bash
docker run --rm -v "$PWD:/workspace:ro" -w /workspace nginx:1.28-alpine sh -c 'apk add --no-cache python3 && python3 tools/test-guide-image-rate-limit.py /usr/sbin/nginx'
```

## Notes

- 看到的那次：PR #2030 run 42226958456，job 127923434334。重跑應該就過；這張票是把 flake 根除。
