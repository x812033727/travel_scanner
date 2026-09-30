---
id: 2026-09-28-video-tidied-late-languages
title: 清理過的影片被勾新語言時告訴站主
status: in-progress
priority: P3
area: tools
owner: claude-opus-5-5-tidied-languages
claimed_at: 2026-09-30T15:40:56Z
created_at: 2026-09-28T11:51:48Z
completed_at:
branch: claude/video-tidied-late-languages
depends_on:
  - 2026-09-28-video-story-tidy-finished
scope:
  - tools/video/automation/flow.mjs
  - tools/video/automation/automation.test.mjs
  - tools/video/automation/cli.test.mjs
  - docs/videos/AUTOMATION.md
---

# 清理過的影片被勾新語言時告訴站主

## Why

工人會在影片上 YouTube 滿 7 天（`VIDEO_TIDY_DAYS`）後清掉它的工作檔（`tools/video/automation/tidy.mjs`，`docs/videos/AUTOMATION.md` §清理工作區）：成片、旁白、畫面都不在了。站主之後才在 `/admin/videos` 的語言面板多勾一個語言時，`Automation.languages()` 看到成片核准的 `final.mp4` 不在（`approvalState` 回 `absent`）就什麼都不做，站上那一格會一直停在「製作中」，站主不知道為什麼。

## Definition of done

- [x] `auto.json` 有 `tidied_at` 的影片被勾了新的語言部件時，工人不重做影片，而是讓站主看到原因：每個還在「製作中」的部件在語言批次裡回報成 `{status: "skipped", reason: "工作檔已在 <日期> 清掉，…"}`，或卡片清單第一列寫出原因（選一種，照 `docs/videos/LANGUAGES.md` 的現有做法）。
- [x] 沒清理過的影片行為不變。

## Steps

- [x] 在 `flow.mjs` 的 `languages()` 裡辨認清理過的影片（讀 `auto.json` 的 `tidied_at`），決定回報方式。
- [x] 測試：清理過的影片被勾新語言、沒清理過的影片照舊。

## How to verify

```bash
node --test "tools/video/automation/*.test.mjs"
npm run test:tools
```

## Notes

- 2026-09-28 清理那張票（`2026-09-28-video-story-tidy-finished`）發現的缺口；那張票不能改 `flow.mjs`（#897、#904 正在改），所以另開。
- 標題、說明、CC 的翻譯本身不需要成片，但 `languages()` 最後一步的 `package` 要複製 `final.mp4`，所以只翻不包也送不出去；要做就是回報原因，不是重做。
- 2026-09-30 claude-opus-5-5-tidied-languages 認領時用了 `--force`：工具說 scope 跟三張票重疊，三張都是已合併 PR 留下沒結案的票——`2026-09-28-drama-listener-stale-check`（codex-ten-drama，review，認領超過 24 小時，PR #978 已在 09-29 合併）、`2026-09-28-sothatswhy-shorts-from-episode`（claude-opus，認領超過 24 小時，PR #904 已合併）、`2026-09-30-video-worker-moves-two-videos-at`（claude-opus-5-5，PR #999 已合併，票還在 in-progress）。這三張票要由持有者或站主結案。
- **選的做法：語言批次裡的 skipped 部件**（不是卡片清單第一列）。`Automation.languages()` 在找成片核准之前先看 `state.tidied_at`，有就交給 `tidiedLanguages()`：把站上還是「製作中」的部件（`pendingLanguages`）每一個寫成 `{status: "skipped", reason: "工作檔已在 <日期> 清掉，成片與旁白都不在了，清理後才勾的部件做不出來；要這個語言得重做影片"}`，manifest 寫到 `review/languages.json`（跟 `languagesSubmission` 同一個檔），直接 `api.submit` 一筆 `languages` 審核，然後 `report` 成 `languages skipped`。不跑任何指令（`i18n-sheet`、`dub`、`captions`、`package`、`review-push` 都不跑）。
  - 為什麼：伺服器的 `language_states` 本來就收任何部件的 `{status: "skipped", reason}`，面板顯示「跳過（原因）」、卡片離開「語言製作中」，跟放棄的配音（`dubs/<l>/skipped.json` → `review-push` 的 payload）走同一條到站主眼前的路。卡片清單第一列那條路要站上一直標「製作中」，而且要自己記住報過沒有；批次送進去之後部件就不是 working，下一輪 `pendingLanguages` 是空的，自然不會重送。
  - 為什麼不走 `review-push`：`languagesSubmission` 只會把配音寫成 skipped，標題說明與 CC 沒有檔案就「不列」＝仍在製作中；要改就得動 `review/sync.mjs`，還要在清掉的工作區跑它。直接送只動 `flow.mjs`。
  - 批次只列新勾的部件；伺服器是「後一筆只替它列到的部件說話」，所以清理前做好的部件照舊。不會蓋掉等站主的批次：`tidy.mjs` 在站上還有 pending 審核時就不清（`PENDING_REVIEW_HOLD`），清理後不會有 pending 的語言批次。沒有音軌，伺服器直接核准。
  - 送不出去：400／422（非站主類）當成內容被拒，只卡這支影片（同 `review-push` 的 lint 結束碼）；其他錯誤 `later`，下一輪再送。
- 測試（`automation.test.mjs`，加進 scope）：用真的 `tidyRound` 清掉 `finishedVideo` 之後勾 ja 三個部件——一輪回報、沒跑任何指令、沒叫翻譯、payload 只有 ja、原因含清理日期、直接核准、下一輪不再送、en 仍是 ready；原本「上 YouTube 後才勾的語言」那個測試多驗 `tidied_at` 不存在時照舊做一批。拿掉 `tidiedLanguages` 那行時新測試會失敗（`step()` 回 null）。
- `cli.test.mjs` 的「a tidied video is not made again…」原本把舊行為（清理後勾英文 CC，`auto` 什麼都不做、不打任何 API）寫死了，`npm run test:tools` 因此失敗；改成驗新行為（一筆 `languages` 審核、en 兩個部件 skipped、原因含 2026-10-20、沒跑任何指令、檔案仍是清掉的），`fakeSite` 多一個選用的 `reviews` 收審核與回報。這個檔也加進 scope。
- `docs/videos/AUTOMATION.md` §清理工作區的兩句（「語言那一步要成片核准還在才動」「站上那一格會一直是製作中」）改成新行為，也加進 scope。
