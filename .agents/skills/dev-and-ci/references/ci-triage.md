# CI 紅燈分診

## 順序

1. **拿到完整 log，不要只看最後幾行。**

   ```bash
   SHA=$(gh pr view <n> --json headRefOid -q .headRefOid)
   gh api "repos/{owner}/{repo}/commits/$SHA/check-runs" -q '.check_runs[] | "\(.name)\t\(.conclusion)\t\(.details_url)"'
   # job id 是 details_url 的尾巴
   gh api "repos/{owner}/{repo}/check-runs/<job-id>/annotations"          # 每個失敗的 vitest 一條，立刻可讀
   gh api --allow-escape-sequences "repos/{owner}/{repo}/actions/jobs/<job-id>/logs" \
     | sed -E 's/\x1b\[[0-9;]*[a-zA-Z]//g' > job.log                       # 存檔再 grep
   grep -an "FAILED\|Error\|exit code\|✘" job.log | head -40
   ```

   `gh run view <run> --log-failed` 在 run 還沒全部結束前印不出東西；`--allow-escape-sequences` 是 `gh api` 的旗標，不加 gh 會拒絕輸出含 ANSI 碼的 log。
2. **分類**：環境（registry、網路、runner）→ 已知 flake（下表）→ 自己的錯。判斷依據：同一個 commit 的另一次 run 或姊妹 job 有沒有過；失敗的測試單獨跑是不是永遠過；錯誤訊息有沒有提到你改的東西。
3. **環境與已知 flake 才重跑**：`gh run rerun <run-id> --failed`，要等整個 run 結束才能用。同一個 flake 在一個 PR 上紅第二次，就不是「運氣不好」，開票（`npm run tasks -- new`）或照下面的方法修。
4. **main 自己紅了**：`ci-red-main.yml` 會開 `ci-red-main` issue。PR 的 base 是紅的時候，你的 PR 也會帶著那個紅燈。

PR 只跑 `pull_request` 事件、同一個 PR 的新 push 會取消舊 run（`concurrency`）。被取消（`cancelled`）的 run 不是失敗；main 的 run 永遠不取消。綠的 run 應該沒有 artifact（測試結果只在 `failure() || cancelled()` 上傳），SEO audit 例外。

## 已知的、不是你的錯的紅燈

| 症狀 | 成因 | 現況／做法 |
| --- | --- | --- |
| `exit code 125`、`Unable to find image`、quay.io 502／504／reset、`auth.docker.io` timeout | 映像只拉一次，registry 一時失敗 | 已修：`tools/ci/pull-images.sh` 在獨立的「Pull container images」步驟重試，之後 `docker run --pull=never`。`denied`／not found／`unauthorized`（401）是拒絕，立刻失敗、不重試。還是 125 就看是不是拒絕 |
| cgr.dev 的 MinIO 映像 `error pulling image configuration ... denied: <!doctype html>...403` | dockerd 把任何 403 都印成 `denied:`，連 blob 上偶發的 HTML 403 也是 | 已修：blob／config 下載的 403 當暫時失敗重試。映像以 digest 釘住（`MINIO_IMAGE` 在 ci.yml），digest 不會過期、不需要 `docker login`；背景與萬一變了的選項在 `tasks/done/2026-09-24-retry-a-403-on-a-chainguard.md` |
| `community.spec.ts` 的 `read ECONNRESET` | Playwright 的 APIRequestContext 重用 keep-alive 連線、沒有自己的閒置逾時，`next start` 預設約 6 秒就關 | 已修：`apps/web/package.json` 的 start 是 `next start --keepAliveTimeout 65000`，與正式站 `KEEP_ALIVE_TIMEOUT` 相同，`tools/ci-images.test.mjs` 檢查。不要往 metric 或 manifest 方向查 |
| `community.spec.ts` 離線訊息逾時 | 產品 bug：`setOffline` 不會斷開已開的 EventSource，恢復後沒人重抓 | 已修：`apps/web/components/community/provider.tsx` 聽 `online` 事件 |
| `site-pages.spec.ts` 的 `Response has been disposed` | 測試在 `/auth/me` route handler 的 `route.fetch()` 與 `json()` 之間就結束 | 已修：先 `waitForResponse` 等 session 回應再斷言；新的短後台測試也要這樣寫 |
| `FinalizeArtifact 403` | artifact 儲存量爆掉 | 已修：測試結果只在失敗或取消時上傳 |
| vitest 在負載下偶發紅：關閉守衛落後一個 render、Escape 沒反應、焦點沒移過去（trip-editor、travel-card-actions、route-mode-panel 那一族），單獨跑永遠過 | passive effect 空檔（下一節） | 已修那四個；新的同型症狀照下一節處理 |
| 手機專案的點擊一直 `intercepts pointer events`，桌面過 | 版面被撐寬，座標全部位移 | 見 browser-measurement.md |
| 兩個各自會過的 PR 合在一起才壞 | 例：`server-only` 模組被 sitemap import | 見 checks.md |

還沒做、若再重現就開票：mailpit 映像釘版本、CI uvicorn 的 `--timeout-keep-alive`、社群 EventSource 的 `onerror`。

## passive effect 空檔：負載下才紅的那一族

**成因。** fetch 回來後的 `setState` 在 `act` 之外、走 default lane。React 19 只有 sync lane 的 commit 會當場沖掉 passive effect；其他 lane 的 `useEffect` 是 Scheduler 的下一個 task（Node 上是 `setImmediate`，5 ms 的時間片用完就讓出）。大元件 render 超過 5 ms 時，DOM 已經 commit、`useEffect` 還沒跑；RTL 的 `waitFor`／`findBy` 成立後用 `setTimeout(0)` 收尾，可能排在 Scheduler 下一個 task 之前，測試就落在空檔：ref 還是上一個 render 的 handler、Escape 的 listener 還沒掛、焦點還沒移。

**別被誤導。** 用 `flushSync` 探針「證明 ref 沒落後」只證明 sync lane 沒事——這個誤判讓它拖了三天。

**確定性重現：`apps/web/lib/testing/commit-before-passive-effects.ts`。** 它把 `IS_REACT_ACT_ENVIRONMENT` 設成 false、`vi.spyOn(performance, "now")` 每次讀 +3 ms（讓 Scheduler 一定在 commit 後讓出；+50 ms 會連 render 都不跑），然後每個 `setImmediate` 檢查 DOM 是否已 commit，一 commit 就把控制權還給測試。用法照 `apps/web/lib/modal-sheet.test.tsx`：

```tsx
let respond!: () => void;
const request = new Promise<void>((resolve) => { respond = resolve; });
render(<OpenedByRequest request={request} />);           // 元件在 effect 裡 request.then(setState)
await commitBeforePassiveEffects(respond, () => screen.queryByRole("dialog") !== null);
fireEvent.keyDown(document, { key: "Escape" });
expect(screen.queryByRole("dialog")).toBeNull();
```

測試用的 harness 不能在 render 時改寫外部變數（lint 的 `react-hooks/globals` 會擋），所以把 `request: Promise` 傳進去、在 effect 裡 `.then(setState)`。其他範例：`apps/web/components/planner-overlay.test.tsx`、`apps/web/components/route-mode-panel.test.tsx`。

**修法。** 給 handler 讀的 ref 同步、註冊 listener／layer、移焦點的 effect 改成 `useLayoutEffect`，讓它們落在畫出那個 DOM 的同一個 commit（`apps/web/lib/modal-sheet.ts`、`apps/web/components/route-mode-panel.tsx` 的註解寫了原因）。

**坑：關閉後還原焦點不能放在 layout cleanup。** layout cleanup 跑在 mutation 階段，React 在 commit 結束時會把焦點還給 commit 前持有它、而且仍在文件裡的元素（例如關閉後還留在頁面上的篩選列 sheet），蓋掉你的 `focus()`。做法：layout cleanup 記下 opener，無 deps 的 `useEffect` cleanup 才 `focus()`（`useModalSheet` 的 `returnFocusRef`）。整個 portal 卸載的元件沒有這個問題。

**驗證修正。** 用 helper 寫的回歸測試，換回舊程式要紅、修正版要綠，兩種都跑過才算。

## 大規模清查（很多 run 都紅、分不清是幾件事時）

1. `gh run list --status failure --limit 60 --json databaseId,headBranch,event,createdAt`。
2. 每批十個 run 讀失敗 job 的 log、分類（可以交給多個代理，各自只回分類與證據）。
3. 合併成不同問題，標出還擋著開著 PR 的那些；已被後來的 push 或合併修掉的劃掉。
4. 每個剩下的問題找根因，交給另一個代理反證，再修。
5. 收尾看 `git status`：代理可能在 worktree 根目錄留下 `git archive` 之類的大檔。
