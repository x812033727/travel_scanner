---
id: 2026-10-23-lines-video
title: 漫劇聽眾修訂常回 lines 清單而不是 video 物件，兩次就把整集擋住：工人要接受逐句修訂
status: open
priority: P1
area: tools
owner:
claimed_at:
created_at: 2026-10-23T09:50:00Z
completed_at:
branch:
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

- [ ] 聽眾回 `{"lines":[…]}`（每項至少有 `id` 與 `text`，可有 `emotion`／`speaker`）時，工人把它逐句套回 video.json（id 不在劇本裡的忽略並記 log），其餘照舊走 `saveAndLint`；`edits` 數＝套上的句數。
- [ ] 回 `{"video": …}` 的舊形狀照常。
- [ ] 提示詞告訴聽眾兩種回法都可以、長劇本優先回 lines（或乾脆只要 lines）。
- [ ] `automation.test.mjs` 有兩個案例：lines 形狀套回成功；id 不存在時不壞檔。
- [ ] 部署後在後台對 e002–e004 按「重試」，三集都過聽眾階段。

## Steps

- [ ] `flow.mjs listen()`：`stage("listener")` 回來後，若 `!answer.video && Array.isArray(answer.lines)`，用 `eachLine(video)` 依 id 寫回 text／emotion，組成 `{ video, edits }` 再交給 `saveAndLint`（`rewrite` 那段 3700 行附近已有同樣的套法可抄）。
- [ ] `prompts.mjs LISTENER_BASE`（約 440 行）：加一句允許回 `{"lines":[{id,text,emotion?}],"notes"}`。
- [ ] 測試、`npm run test:tools`、開 PR；部署由站主決定。

## How to verify

主機工人 log 不再出現「the listener edit the answer has no video object」；e002–e004 重試後 `listener edit, N changes` 並往查核走。

## Notes

- 第 1 集卡在另一個問題（設定圖 409，票 `2026-10-22-409`，#1697 已部署，等補送）。
- 主機 `docker logs` 在 10-23 09:08Z 部署重建容器後只剩新 log，舊的失敗紀錄要看各集 `auto.json` 的 `blocked` 與 `answers/`。
