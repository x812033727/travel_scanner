---
id: 2026-10-23-lines-video
title: 漫劇聽眾修訂常回 lines 清單而不是 video 物件，兩次就把整集擋住：工人要接受逐句修訂
status: done
priority: P1
area: tools
owner: claude-fable-5.1
claimed_at: 2026-10-23T09:53:24Z
created_at: 2026-10-23T09:50:00Z
completed_at: 2026-10-23T14:20:08Z
branch: claude/eloquent-williams-d2633d
depends_on: []
scope:
  - tools/video/automation/flow.mjs
  - tools/video/automation/prompts.mjs
  - tools/video/automation/automation.test.mjs
---

# 漫劇聽眾修訂常回 lines 清單而不是 video 物件，兩次就把整集擋住：工人要接受逐句修訂

## Why

《系統說我是 BUG》第 2、3、4 集（`xitong-shuo-wo-shi-bug-e002`…`e004`）2026-10-22 16:47–17:08Z 全部 `blocked`：`listener failed 2 times in a row: the listener edit the answer has no video object`。試片單集與第 1 集也各失敗兩次、第三次才過。四支裡三支擋住，這是貼圖漫劇（manga 等級，一集 50 多鏡）的常態，不是偶發。

聽眾階段（`flow.mjs` 的 `listen`）照 `prompts.mjs` 的 `LISTENER_BASE` 要模型回 `{"video": <整份 video.json>, "edits": [...]}`，`saveAndLint` 看不到 `answer.video` 就回「the answer has no video object」。看 e002 存下來的答案 `answers/listener-2026-10-22T16-56-46-757Z.txt`（5.7 KB、合法 JSON）：模型回的是 `{"lines":[{"id","speaker","emotion","text"}…],"notes":"…"}`——跟 `listener:rewrite` 變體一樣的逐句形狀，id 都是劇本裡的。整份 video.json 對 50 多鏡的漫劇太長，模型傾向只回改過的句子；兩次都這樣就 `blocked`，要站主按「重試」，重試也多半再撞。

## Definition of done

- [x] 聽眾回 `{"lines":[…]}`（每項至少有 `id` 與 `text`，可有 `emotion`／`speaker`）時，工人把它逐句套回 video.json（id 不在劇本裡的忽略並記 log），其餘照舊走 `saveAndLint`；`edits` 數＝套上的句數。
- [x] 回 `{"video": …}` 的舊形狀照常。
- [x] 提示詞告訴聽眾兩種回法都可以、長劇本優先回 lines（或乾脆只要 lines）。
- [x] `automation.test.mjs` 有兩個案例：lines 形狀套回成功；id 不存在時不壞檔。
- [x] 部署後在後台對 e002–e004 按「重試」，三集都過聽眾階段。

## Steps

- [x] `flow.mjs listen()`：`stage("listener")` 回來後，若 `!answer.video && Array.isArray(answer.lines)`，用 `eachLine(video)` 依 id 寫回 text／emotion，組成 `{ video, edits }` 再交給 `saveAndLint`（`rewrite` 那段 3700 行附近已有同樣的套法可抄）。
- [x] `prompts.mjs LISTENER_BASE`（約 440 行）：加一句允許回 `{"lines":[{id,text,emotion?}],"notes"}`。
- [x] 測試、`npm run test:tools`、開 PR；部署由站主決定。

## How to verify

主機工人 log 不再出現「the listener edit the answer has no video object」；e002–e004 重試後 `listener edit, N changes` 並往查核走。

## Notes

- 第 1 集卡在另一個問題（設定圖 409，票 `2026-10-22-409`，#1697 已部署，等補送）。
- 主機 `docker logs` 在 10-23 09:08Z 部署重建容器後只剩新 log，舊的失敗紀錄要看各集 `auto.json` 的 `blocked` 與 `answers/`。
- 2026-10-23 做法（claude-fable-5.1）：
  - `flow.mjs` 新增 `listenerEdits(video, answer, log)`（export，`writeVideo` 下面）：答案沒有 `video` 而 `lines` 是陣列時，把劇本 `structuredClone` 一份，用 `eachLine` 依 id 找句子，套 `text`（有非空 `emotion` 也套）；文字改了就刪掉 `say`／`say_for`（舊字的讀法會被 lint 擋）；同一 id 第二筆忽略；id 不在劇本裡的集中記一行 log 並略過；回 `{ video, edits, notes? }`。`edits` 是實際改到的句數（文字或情緒有變），所以回一模一樣的句子不算 change。`listen()` 在 `stage("listener")` 回來後先過這個函式再交 `saveAndLint`；用複本是因為後面 `scriptCheckBinding(video)` 要拿原稿比對、決定要不要重查核。
  - `prompts.mjs`：`LISTENER_BASE` 本身沒有 Return 句；原本那句在 `INSTRUCTIONS.listener`（貼圖），而漫劇的 `DRAMA_INSTRUCTIONS.listener` 根本沒寫回什麼形狀——這就是漫劇聽眾自己回 lines 的原因。抽成 `LISTENER_ANSWER`（export）放兩邊：整份 video 或 `{"lines":[{id,text,emotion?}],"notes"}` 都可以，長劇本優先 lines，並說明 lines 形狀不能刪句。
  - `automation.test.mjs`：三個案例——lines 套回成功（x9fe 只改 emotion、p5vs 改字並掉 say、zzzz 不存在記 log、`listener edit, 2 changes`、verified 變 false）；全部 id 不存在時 `0 changes`、video.json 與聽眾前一致；`listenerEdits` 對舊形狀原樣回傳、不動原稿。
  - 認領時 `scope` 跟 `2026-10-14-ai-and-tech-videos-tell-one`、`2026-10-20-tutorial-flow-and-hooks-rules-learned` 在 `prompts.mjs` 重疊（分別認領 9 天與 3 天），用 `--force` 認領；這條只動聽眾的 Return 句與新常數，不碰 register／narrative。
  - 沒部署。部署後對 e002–e004 按「重試」由站主決定；重試後工人 log 應是 `listener edit, N changes`，不再出現「the answer has no video object」。
- 2026-10-23 結果：PR #1780 於 13:15Z 併入（`a1d9570bb`），13:17Z 部署上線（host-verify 13/13，含工人容器的 `listenerEdits`／`LISTENER_ANSWER` 兩項）。13:19Z 後台對 e002–e004 按「重試」，14:12–14:17Z 主機工人 log：e002「listener edit, 1 changes」、e003「4 changes」、e004「3 changes」，三集都從 blocked 回到 active、往查核走；沒再出現「the answer has no video object」。PR 期間 main 兩度碰收據，各由審查代理（`claude-pr-review-lines-video-merge-20261023`、`…-merge2-20261023`）從三個 blob 重建聯集重綁。
