---
id: 2026-09-14-article-image-retry
title: Article images recover from rate limits
status: done
priority: P1
area: web
owner: codex-p1-audit
claimed_at: 2026-09-29T01:59:49Z
created_at: 2026-09-14T00:37:36Z
completed_at: 2026-09-29T01:59:52Z
branch: codex/p1-task-audit
depends_on: []
scope:
  - apps/web/components/guides
  - apps/web/components/content-blocks.tsx
  - ops/nginx/10-rate-limit.conf
  - ops/nginx/mokaair.conf.example
  - ops/nginx/ci-validate.conf
  - ops/nginx/article-images.md
  - tools/test-guide-image-rate-limit.py
---

# Article images recover from rate limits

## Why

The user's existing Chrome page recorded HTTP 429 for all six intelligence covers on
2026-09-14. Failed images remain broken until reload. Both cards and article body images
share the page request bucket and lack transient-failure recovery.

## Definition of done

- [x] Local article images do not consume the SSR request budget; HTML remains limited.
- [x] Cards, hero and body images retry at most twice, including failures before hydration.
- [x] Regression checks pass and host activation steps are documented.
- [x] Merge and separately activate the web release and enabled host nginx configuration.

## Steps

- [x] Implement scoped nginx exemption and bounded image retries.
- [x] Validate and record deployment boundary.

## How to verify

- From apps/web: `npx vitest run components/guides/guide-image.test.tsx components/guides/article.test.tsx components/content-blocks.test.tsx` — 91 passed.
- `npm run lint:web`, `npm run typecheck:web`, `npm run check:i18n` — passed.
- `npm run build:web` — passed, all 293 static pages generated.
- `python3 tools/test-guide-image-rate-limit.py /path/to/nginx` — passed using nginx 1.28.3 in WSL: config syntax, 120 images, preserved page budget and 7 non-image routes.
- `node tools/tasks.mjs check` — passed (existing stale/overlap warnings).
- Host rollout and rollback: `ops/nginx/article-images.md`. Neither host nor web production has been changed.

## Notes

The keepalive task is already present in origin/main but its deployment ticket still holds
the site template and CI harness in review. This user-authorized image fix only changes
the page limit zone references in those two files; its keepalive directives remain intact.
No production activation is included in this task's current authorization.

### 2026-09-19 補註

claude-opus-5 應站主「整理目前所有工作狀態」處理，盤點見 `docs/work-status-2026-09-19.md`。

程式已隨 PR #470（2026-09-14 合併）和之後的部署上線。剩下的只有主機 nginx 設定的啟用；主機上是否已套用這次的 limit zone 引用沒有紀錄，接手時先比對 `/etc/nginx` 與 `ops/nginx`，改正式主機設定要站主同意。

### 2026-09-19 接手查核（claude-fable-5-1）

repo 這邊沒有東西可做：`ops/nginx/10-rate-limit.conf`、`mokaair.conf.example`、`ci-validate.conf` 與
`ops/nginx/article-images.md` 都已在 main，程式也隨 #470 之後的部署上線。剩下只有主機設定的啟用，要站主在主機上做，
步驟照 `ops/nginx/article-images.md`。先看主機現況再決定要不要動：

```bash
# 主機上，只讀：比對 repo 版與 /etc/nginx 生效版的 limit zone 引用
cd /root/travel_scanner
diff <(grep -n "limit_req\|limit_req_zone\|guides/" ops/nginx/10-rate-limit.conf) \
     <(grep -n "limit_req\|limit_req_zone\|guides/" /etc/nginx/conf.d/10-rate-limit.conf)
grep -rn "limit_req" /etc/nginx/sites-enabled/ /etc/nginx/conf.d/ | grep -i "image\|guides\|jpg\|svg" || echo "image exemption not present"
nginx -t
```

沒有差異就代表已套用，直接 `done`；有差異就依 `article-images.md` 的 rollout 一節套用（`nginx -t` 通過再 reload），
再用未登入的瀏覽器連開六篇 intelligence 的封面確認沒有 429，把結果貼回本票。認領已釋出。


## 2026-09-29 標記完成（由站主授權，非原持有者）

站主要求逐張核對原 64 張 P1 並處理已無剩餘工作的票。本次只結案，不重做已合併實作。
原持有者：未認領；原分支：claude/travel-scanner-pr-552-rpq36m。

- PR #470 MERGED d22c658ea23be72966e8f65098fb6dea71b9c649; original task records web code subsequently deployed.
- Later tasks/done/2026-09-19-edge-rate-limit-refuses-search-crawlers.md records actual production location / already using mokaair_content_pages, host application and reload 2026-09-19, and subsequent installer run twice changing only an eight-line comment.
- PR #568 MERGED; tasks/done/2026-09-12-nginx-deploy-checks-false-pass.md later takeover closes repository/host drift and records real nginx isolated validation: 120 image requests allowed, page budget preserved, seven non-image routes limited.
- Current prod-host-ops/references/nginx-edge.md:21-27 documents host's mokaair_content_pages and the article-image empty-key exemption.

上述後續證據補足舊清單仍未勾選的項目，已同步勾選。歷史限制保留供追溯；這是既有完成紀錄的核對，不宣稱本日重新部署、重新發布或重新跑過歷史測試。

No implementation/activation work remains supported by the historical evidence. The original 'host activation unknown' note predates later same-day verified host reconciliation.

`--force` 僅用於本次授權的任務結案記帳，未修改或接管原分支實作；已核對最新 main 與開啟 PR，完成判定依上列證據。
