# 每週的 Dependabot PR

`.github/dependabot.yml` 每週開 PR 的有 npm（根目錄，一份 lock 涵蓋 `apps/web`）、uv（`apps/api`）、github-actions，以及 docker／docker-compose（Dockerfile 與根目錄 compose 的 `tag@sha256` 釘選，只動 digest 與 patch tag）。minor／patch 合成一個 `minor-and-patch` PR，大版本一個套件一個 PR；actions 全部合成一個；`@playwright/test` 例外，永遠自己一個 PR；字型（`@fontsource-variable/*`）與 `pinyin-pro` 也不進 `minor-and-patch`，合成自己的 `video-worker` PR（兩者都見下）。npm 與 uv 各自最多同時開 5 個，**卡住不合的大版本 PR 會一直佔名額**，所以要嘛合、要嘛明確關掉。

合併本身走 skill `task-board`（strict 保護、一次一個、`--match-head-commit`），而且要站主當次說「合併」。

## 判斷順序

1. **分類**：CI 綠、紅、環境紅。環境紅（exit code 125、`registry-1.docker.io` 逾時、見 ci-triage.md 的表）重跑就好，不算這個升級的問題。
2. **綠的大版本，CI 綠還不夠，再查三件事：**
   - **測試數量有沒有少。** 拿 PR 分叉點那一版 main 的 CI `web` job 當基準，比對 vitest 的 `Test Files`／`Tests` 兩行與 e2e 的通過數；API 看 pytest 的 passed／skipped。數字少了就是新版本默默沒跑到某些測試。
   - **engines 下限。** 看 lock 裡新版本的 `engines`（`grep -n -A60 '"node_modules/<pkg>": {' package-lock.json | grep -A2 engines`），對照本機 `node -v`、CI 的 `node-version: 24`、以及映像（`apps/web/Dockerfile` 用 `node:22-alpine`）。npm 只印 `EBADENGINE` 警告、不會失敗。例：jsdom 30 要 `^24.15.0`。
   - **破壞性變更碰不碰得到我們。** 讀 release notes 的 breaking 段，對 repo `git grep` 用到的 API／選項。例：github-script 升大版本，`ci-red-main.yml` 的腳本沒有 `require('@actions/github')` 就不受影響；React 開了 Trusted Types，但本站 CSP 沒有 `require-trusted-types-for`。
3. **紅的**：是上游卡住（自己修不了）還是自己修得了？
   - 自己修得了（例：mypy 大版本報 `redundant-cast`，刪掉 cast、放寬 specifier、`uv lock`）：在 PR 分支上修（見下），跑完整 CI。
   - 上游卡住：留一則說明原因的留言，再單獨留言 `@dependabot ignore this major version`（幾秒內自動關閉 PR），並開或更新一張 `blocked` 的票記住這個升級。
   - 跨大版本的 runtime 依賴（例如當年 redis 6→8，連 RQ、fakeredis 都要驗）：關掉 PR、當成遷移票做。

## `@playwright/test` 的 PR 一定紅，要人補兩個檔

影片工人的映像（`ops/video/Dockerfile` 的 `mcr.microsoft.com/playwright:v<版本>-noble@sha256:…`）帶的是同一版 Playwright 的瀏覽器，`ops/video/package.json` 也釘死同一版；三處（含 lock）不一致時 `tools/supply-chain.test.mjs` 紅。沒有生態系會跟著改那兩個檔（docker 那一條連 patch tag 都忽略，只刷同一個 tag 的 digest），所以這個 PR 要在它的分支上補：`docker buildx imagetools inspect mcr.microsoft.com/playwright:v<新版>-noble` 取 index digest，改 Dockerfile 的 tag 與 digest、`ops/video/package.json` 的版本，照下面「在 Dependabot 的分支上修」推回去；改到 `ops/video/` 會觸發 `Video worker image` workflow 在 CI 建一次映像，證明拉得到、瀏覽器對得上。Microsoft 還沒發布那一版的映像就先放著等。

## `video-worker` 的 PR（字型與 pinyin-pro）動到工人裝的套件就紅，要人補一個檔

影片工人的映像只照 `ops/video/package.json` 安裝（沒有 lock），那個檔又不是 workspace，Dependabot 只改 `package-lock.json`；`tools/supply-chain.test.mjs` 在兩邊版本不一樣時紅（字型會換掉成片的字，pinyin-pro 會改變 check-audio 哪些句子算「同音」）。所以這群放在 `video-worker` 一個 PR：紅的時候在它的分支上把 lock 的版本抄進 `ops/video/package.json`，照下面「在 Dependabot 的分支上修」推回去：

```bash
node -e 'const fs=require("fs");const f="ops/video/package.json";const p=JSON.parse(fs.readFileSync(f));const l=JSON.parse(fs.readFileSync("package-lock.json")).packages;for(const n in p.dependencies)p.dependencies[n]=l["node_modules/"+n].version;fs.writeFileSync(f,JSON.stringify(p,null,2)+"\n")'
```

改到 `ops/video/` 會觸發 `Video worker image` workflow 在 CI 建映像，並在映像裡把範例影片從 render 跑到 package。只動到 `ops/video/package.json` 沒列的字型時是綠的，照一般流程合。

## 目前被擋住的大版本（以票為準，動手前先看票）

| 升級 | 為什麼不能照原樣合 | 票 |
| --- | --- | --- |
| ESLint 10 | `eslint-plugin-react`（`eslint-config-next` 帶進來）還在呼叫 ESLint 10 移除的 `context.getFilename`，lint 一啟動就崩 | `tasks/open/2026-09-14-eslint-10-upgrade.md`（blocked） |
| TypeScript 7 | `typescript-eslint` 的 peer 範圍只到 `<6.1.0`，lock 會把 TS 7 巢狀放進 `apps/web` 自己的 `node_modules`、根目錄留 6.x：tsc／next build 與 ESLint 用兩套編譯器 | `tasks/open/2026-09-14-typescript-7-upgrade.md`（blocked） |

已經解決、不用再擋的：mypy 2、redis-py 8（`apps/api/pyproject.toml` 已是 `redis>=8.1,<9`）、vitest 5、jsdom 30、pytest-cov 7。

## 一次合一個，少跑白工的 CI

- 先算會不會衝突（唯讀、不動工作樹）：`git merge-tree --write-tree --name-only origin/<A> origin/<B>`。
- npm 的 lock PR 彼此一定衝突；uv 的通常不衝突（specifier 隔了幾行）。
- 有衝突的留言 `@dependabot rebase`，它約一分鐘內 force-push 重建並重跑 CI。先合的那個合進 main 後，Dependabot 也會自動重建其餘有衝突的 PR。**被人 push 過的 PR 它就不再管了**，之後只能自己 rebase。
- 只是落後（BEHIND）就 `gh pr update-branch <n>`，Dependabot 的 PR 也可以，連改 workflow 檔的也行。
- 每合一個，其餘全部變 BEHIND；照 `task-board` 一條接一條。

## 在 Dependabot 的分支上修

Edit／Write 工具只能寫 session 自己的 worktree。在自己的 worktree 裡：

```bash
git fetch origin <dependabot-branch>
git switch --detach origin/<dependabot-branch>
# 修、跑檢查（run-checks.sh）
git commit -F <msg-file>
git push origin HEAD:<dependabot-branch>
```

## 讀 job log

```bash
gh api --allow-escape-sequences "repos/{owner}/{repo}/actions/jobs/<job-id>/logs" \
  | sed -E 's/\x1b\[[0-9;]*[a-zA-Z]//g' > job.log
grep -a "Test Files\|Tests \|passed\|failed" job.log
```

不加 `--allow-escape-sequences`，gh 會拒絕輸出。

## 合併之後別忘了

- 本機每個 worktree 重新 `npm ci`／`uv sync --frozen`，否則之後的本機結果是舊版本的（local-env.md）。
- 自己開的 PR 也可能被別的 session 合掉（大家共用一個 GitHub 帳號）：合併前後都以 `gh pr view <n> --json state` 為準。
