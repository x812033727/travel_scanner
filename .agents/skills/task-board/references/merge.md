# 合併：分支保護、rebase 的坑、讀 CI

## 分支保護（全文 `.github/BRANCH_PROTECTION.md`）

- 必要檢查 `api`、`web`、`containers`、`full-stack-smoke`，即 `.github/workflows/ci.yml` 的四個 job。其他 workflow（lighthouse、瀏覽器測試）會跑，但不是合併條件。
- `strict`：分支必須跟上 main。別人一合併，你的綠燈 PR 就變 `BEHIND`（或 `DIRTY` 有衝突），要 rebase 再跑一輪 CI。2026-09-06 一個晚上五個 PR 互相追，浪費三輪 CI。
- `enforce_admins`：`gh pr merge --admin` 不是後門。
- 自動合併：`.github/workflows/auto-update-branches.yml` 設好 `AUTO_MERGE_TOKEN` 之後，會替從這個 repo 分支開、目標 main、非草稿、沒有 `no-auto-merge` 標籤、作者是站主的 PR 打開 auto-merge，並限流地 update-branch，綠了就合（全文 `.github/BRANCH_PROTECTION.md`「Automatic updates and merges」）。站主還沒同意的 PR 開成 draft 或貼標籤；已經打開的 auto-merge 要 `gh pr merge <n> --disable-auto`。這時不要對同一個 PR 跑 `merge-when-green.sh`，兩邊會同時改那個分支。
- 誰能按合併：前景的 `gh pr merge <n> --squash`（或 `gh pr checks --watch --fail-fast && gh pr merge`）只在站主對**那一個** PR 說了「合併」之後會過，同意不會延續到下一個 PR。背景迴圈（`gh pr update-branch` → 輪詢四個 check-run → `gh pr merge --squash --match-head-commit`）只有在站主下過點名條件的常設指令（例如「訂閱所有 CI，如果綠就合併」）時可以跑，這時同一個 session 之後開的 PR 也算在內；沒有這種指令、也沒有上面那個 workflow 時，就每個 PR 各問一次。問的同時在背景把分支同步、CI 跑綠，字一到就能合。
- `npm audit`／`pip-audit` 在 ci.yml 裡是 `continue-on-error`，另有每日的強制 workflow；main 自己紅了會由 `ci-red-main.yml` 開 issue。

## 一條 chain

`scripts/merge-when-green.sh <pr>` 做的事，手動版：

```bash
git fetch -q origin main && git rebase origin/main          # 衝突就停下來看
git push --force-with-lease origin <branch>
SHA=$(git rev-parse HEAD)
gh pr checks <n> --watch --interval 30                        # 等，不要接 | tail
gh api "repos/{owner}/{repo}/commits/$SHA/check-runs" -q '.check_runs[] | "\(.name)\t\(.status)\t\(.conclusion)"'
gh pr view <n> --json mergeStateStatus -q .mergeStateStatus   # CLEAN 才合；UNKNOWN 會停留一陣子，再問一次
gh pr merge <n> --squash --match-head-commit "$SHA"
gh pr view <n> --json state -q .state                         # MERGED
```

- 一次只跑一條 chain；要合併一組票時一條接一條。總整理時先把 open 的票按重疊的 scope 分組，一組一個 PR。
- `gh pr update-branch` 是非同步的：CLI 先印「✓ PR branch updated」，`headRefOid` 之後才動。呼叫前記下 head，每 10 秒 `gh pr view <n> --json headRefOid` 最多 4 分鐘等它變，再輪詢四個 check-run、用 `--match-head-commit <新 head>` 合併。它是把 main merge 進去（不 force-push），對別人的分支也安全；`merge-when-green.sh` 在本機 rebase，沒有這個問題。
- 反過來，腳本等的時候 GitHub 自己把 main merge 進 PR：`ci.yml` 的 `concurrency: ci-pr-<n>` 會取消舊 head 的 run，`api`／`web` 變 **cancelled**，腳本報 `required checks failed: api web`、exit 4；另一種是舊 head 已綠、新 head 還在跑，`mergeStateStatus=BLOCKED` → exit 7。分辨法：結論是 `cancelled` 而非 `failure`，而且 `headRefOid` 已不是腳本等的那個。修法：worktree 裡 `git merge --ff-only origin/<branch>` 再重跑。忙的日子多數 PR 都會碰到。
- push 之後 GitHub 要一兩分鐘才建立 check-run；那段期間 `gh pr checks --watch` 會立刻回「no checks reported」而不是等。腳本因此直接輪詢四個必要 check-run 直到 completed，不靠 `--watch`。
- `--match-head-commit` 是必要的：PR 的作者 session 可能還在跑、還會推，GitHub 會拒絕而不是把沒測的 head 合進去。
- PR 分支只跑 `pull_request`（`push` 只在 `main` 跑），同一個 PR 新的 push 會取消舊 run；被取消的舊 run 結論是 `cancelled`，看 head SHA 那一組。
- 合併後 GitHub 自動刪遠端分支（repo 設定），本機分支留著沒關係。

## rebase 與同步的坑

- **`git rebase --continue` 說「You must edit all merge conflicts」但 `git ls-files -u` 是空的**：那是未暫存的改動在擋，常見是 `next dev` 重寫的 `apps/web/next-env.d.ts`，或 rebase 停住時改了 `tasks/` 的筆記。把 diff 存成 patch、`git checkout -- <files>`、繼續 rebase、再 `git apply`。**不要 `git rebase --skip`**，會重設工作樹。`git checkout --ours` 只對真的有衝突的路徑有用；自動合併過的檔案留著合併後的內容，要還原就 `git checkout HEAD -- <file>`。
- **有東西把 base 合進了你的 PR 分支**（`Merge branch 'main' into …` 不是你做的；2026-09-22 在 #665 上又發生一次，`--force-with-lease` 回 `stale info`）：push 會被拒。分支上只有自己的 commit 時 `git pull --rebase`；已經被自動 merge 過的用 `git reset --hard origin/<branch>` 再 `cherry-pick` 自己的新 commit。**不要 force-push** 蓋掉別人剛推的東西。
- **疊在別的 PR 上的分支，在 base 被 squash 進 main 之後會變 `DIRTY`**：main 只有一個壓扁的 commit，你的分支帶著原本那幾個。**不要 `git merge origin/main`**：下層 PR 搬到 `tasks/done/` 的票會從你帶著的舊 commit 回到 `tasks/open/`，`check:tasks` 報重複 id、web job 變紅。也不要 rebase（會重播被壓扁的 commit）。做法：`git checkout -B <branch> origin/main`、只 cherry-pick 自己的 commit、`git push --force-with-lease`。
- **migration 編號會跟同時合併的 PR 撞號**（0085 撞過）：開 PR 前與合併前各看一次 `origin/main` 的 `apps/api/migrations/versions` 最大號。alembic revision id 不能超過 32 字元（`apps/api/tests/test_schema.py`；超過時 CI 的 `api` 與 `full-stack-smoke` 都紅）。
- 開始 chain 之前 PR 分支不能在主 checkout 被 checkout；每個 PR 一個 worktree 就沒這個問題。
- `git stash` 是所有 worktree 共用的堆疊：要暫存就 `git stash push -u -m <tag>`、記下 SHA、`apply`、依 SHA 找回 `stash@{n}` 再 drop；不要裸的 `stash`／`pop`。

## 讀 CI 失敗

```bash
gh run view <run-id> --log-failed | grep -a "FAILED tests\|Z E  "        # run 還在跑時印不出東西
gh api "repos/{owner}/{repo}/check-runs/<job-id>/annotations"          # 立刻可讀；job id 是 details_url 的尾巴
gh api "repos/{owner}/{repo}/actions/jobs/<job-id>/logs" --allow-escape-sequences | sed -E 's/\x1b\[[0-9;]*m//g' | tail -80
```

每個失敗的 vitest 測試會變成一條 annotation（檔案、行號、名稱），比 log 快。

已知的、不是你的錯的紅燈（2026-09-15 清查 60 個失敗 run，PR #522 修掉四類；再出現先想這些）：

| 症狀 | 成因 | 已修的做法 |
| --- | --- | --- |
| `exit code 125` 加 `Unable to find image`、quay.io 502／504、`auth.docker.io` timeout | 映像只拉一次 | `tools/ci/pull-images.sh` 獨立步驟重試 |
| `community.spec.ts` 的 `read ECONNRESET` | Playwright 的 keep-alive 連線比 `next start` 的閒置逾時長 | start 帶 `--keepAliveTimeout 65000`，`tools/ci-images.test.mjs` 檢查與正式站一致 |
| `site-pages.spec.ts` 的 `Response has been disposed` | 測試在 route handler 的 `fetch` 與 `json()` 之間結束 | 先 `waitForResponse` |
| `trip-editor.test.tsx` 190／292 行 | planner 關閉守衛的競態，見票 `2026-09-11-planner-overlay-close-guard-race` | 只有它紅時 PR 沒錯，推新 head 再跑 |
| 兩個各自會過的 PR 合在一起才壞 | 例：sitemap import 了 `server-only` 模組，載入它的 vitest 要 `vi.mock("@/lib/community/server")` | 照 `apps/web/app/sitemaps/sitemap.test.ts` |

本機限制：Playwright 需要的 chromium build 本機沒裝，e2e 只能靠 CI；workflow 代理留下的 `src.tar` 之類的大檔要 `git status` 清掉。

## 合併之後

- 票應該已經在 `tasks/done/`（在 PR 內結案）。停在 `review` 的票是下一次總整理的工作，見 `collisions.md`。
- 部署是另一件事：走 skill `deploy`。合併只加新檔或內容包時，正式站在部署與匯入之前什麼都不會變。
- 一組 PR 合完再部署一次，比每合一個部署一次省（每次部署重建全部容器、重跑 hotspot-collector 的額度）。
