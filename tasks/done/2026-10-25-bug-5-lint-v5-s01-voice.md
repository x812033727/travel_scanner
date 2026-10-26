---
id: 2026-10-25-bug-5-lint-v5-s01-voice
title: 《系統說我是 BUG》第 5 集卡在 lint：設定集 v5 的石魔與六個 s01- 配角沒有 voice，重做的第 1–4 集可能一樣
status: done
priority: P2
area: tools
owner: claude-fable-5-1-goofy-curie
claimed_at: 2026-10-25T06:20:00Z
created_at: 2026-10-25T05:52:41Z
completed_at: 2026-10-25T08:07:38Z
branch: claude/goofy-curie-35eda8
depends_on: []
scope:
  - tools/video/automation/flow.mjs
  - tools/video/automation/series.mjs
  - tools/video/automation/series.test.mjs
  - tools/video/core/lint.mjs
  - tools/video/core/lint.test.mjs
  - tools/video/core/schema.mjs
  - docs/videos/SERIES.md
  - docs/videos/long-form/review.json
  - docs/videos/long-form/review.md
---

# 《系統說我是 BUG》第 5 集卡在 lint：設定集的配角沒有 voice

## Why

2026-10-25 部署 #1840 後查主機：第 5 集（新規則下的第一集，`xitong-shuo-wo-shi-bug-e005`）在後台的檢查清單停在「卡住，需要人處理：lint still fails after 3 fixes: characters[3].voice: must be an object with provider and name」，工作區沒有 video.json（寫手的答案在 `run-receipts/`）。

站上設定集 v5（已核准）的 `body_json.characters` 共 13 個：前 7 個（江河、系統、千凜、白珩、阿桂、小鐵、唐測）有 `voice {provider, name, style}`，後 6 個 `shi-mo`、`s01-lao-qi`、`s01-qi-yan`、`s01-huo-zhangchui`、`s01-yan-guan`、`s01-a-zhu` 只有 `voice_note`、沒有 `voice`。`flow.mjs` 的 `castFrom` 把該集會出現的角色抄進 video.json，`core/schema.mjs` 的 `validateVoice` 對每個角色要物件，lint 自動修三次都修不回來（寫手不能自己發明聲音）。

第 1–4 集 10-25 05:48Z 已用「重做」回到 `ready`（票 2026-10-25-drama-series-episodes-can-be-redone），第 1 集 `e001-redo1` 寫手跑中；這四集的卡司也從同一本 v5 抄，只要用到那六個角色就會撞到同一個錯。

## Definition of done

- [x] 第 5 集與重做的第 1–4 集不再因 `characters[n].voice` 被 lint 擋（程式面：`settle` 對人物表沒有 `voice` 的角色補聲音、lint 對這種角色接受工人補的；主機上要部署後「重試」才算驗過，見 Steps 最後一項）。
- [x] 設定集裡沒有 `voice` 的配角有一個固定的處理：工人從作品的 `character_voice_pool`、再從 `SPARE_VOICES`（`series.mjs`，十二個 Gemini 內建聲音男女各半）補一個 Gemini 聲音，`voice_note` 當 `style`，寫進 `series.json`／`video.json`、不改設定集（`castVoices`，`castFrom` 起草時與 `settle` 收答案時都呼叫；lint 對人物表有 `voice` 的角色照舊要逐字相同）。
- [x] 不改 `lookHash`（`lookHash` 只讀 id、appearance、sheet_prompt；測試 `a character the setting book gives no voice …` 直接比對）。

## Steps

- [ ] 主機看 `e005/run-receipts/` 寫手最後一版的 characters，確認 characters[3] 是哪一個角色；看 `e001-redo1` 有沒有同樣卡住。**沒做到**：2026-10-25 06:2xZ 主機唯讀 plink 連兩次被 Auto 模式分類器擋（[Production Reads]），跟 10-24 一樣。做法不依賴這個答案：id 排序後 characters[3] 不管是誰，六個無聲角色全部補。站主切 Manual 後可用 scratchpad 的 `host_read.sh`（唯讀：列 run-receipts 的 characters、redo1 的 auto.json、工人 log、drama 設定的聲音池）補看。
- [x] 決定補聲音的位置：工人端。站上改設定集會把總綱、細綱退回待審、ready 集退回 planned，代價大；而且 e005 與 e001-redo1 的 `series.json` 已在起草時抄好（沒有 voice），改站上也救不了它們，所以 `settle` 也補、lint 放行人物表沒 voice 的角色。
- [x] 改法（PR）：`series.mjs` 新增 `SPARE_VOICES`、`castVoices(cast, { voices, narrator, notes })`，`castFrom(setting, episode, options)` 多收 `{ voices, narrator }`；`flow.mjs` `draftEpisode` 傳 drama 分頁的 `character_voice_pool` 與旁白聲音，`settle` 在抄完人物表後呼叫 `castVoices`；`lint.mjs` `seriesProblems` 只在人物表有 `voice` 時比對；`docs/videos/SERIES.md` 寫規則；測試 `series.test.mjs`、`lint.test.mjs` 各一個。`schema.mjs` 沒動。
- [x] 時長收據：flow.mjs、series.mjs、series.test.mjs、lint.mjs、lint.test.mjs 五個綁定檔由獨立代理做 DURATION_ONLY 增量（見 review.md 最後一節）。
- [x] **結果（2026-10-25 08:05Z）**：PR #1842 合併後 main（98aa2dea6，含 #1843）在 07:39–07:41Z 由別的 session 部署；`host-verify.sh` 14/14 PASS，含三項專屬檢查（video-worker 裡 `castVoices` 存在且 `castVoices([{id:"a",name:"x"}])` 回 Charon、lint 的 `known.voice !== undefined` 在）。e005 的重試請求（`retry_request_id 4db98e3f…`）部署後被工人接下：日誌「script fixed and passes lint」→ 事實查核四輪 → 分鏡劇本送審 → 站上自動核准；後台 stage「script approved」。video.json 七個角色都有 Gemini 聲音：`s01-lao-qi` 拿到 Zubenelgenubi（drama 分頁的 `character_voice_pool` 先用，備用聲音沒輪到）、lao-niang Gacrux、其餘照設定集。`e001-redo1` 也過 lint、查核七輪、劇本送審（script review pending，hands_off 下等站上判）；e002–e004 redo1 還是 ready、沒起草，起草時直接走新 `castFrom`。沒看到 characters[3] 的收據，但問題已不存在。
- [x] **部署後**（照 skill `deploy`）：後台對 `xitong-shuo-wo-shi-bug-e005` 按「重試」——如果 auto.json 有 `deferred_until`（退避中），「重試」會回 409，要先在主機清掉 `auto.json` 的 `deferred_until`（10-24 19:5xZ 用過的做法，`docker compose … exec -T video-worker node -` 改 `/opt/mokaair/docs/videos/<slug>/auto.json`，改前確認工人 log 沒有「writer is still running」）。重做的 `e001-redo1`～`e004-redo1` 若也卡在同一個 lint，一樣重試；還沒起草的會直接走新 `castFrom`。重試後寫手重跑一輪（答案在 `run-receipts/`），`settle` 補上六個配角的聲音，lint 應 0 errors；確認方式：後台檢查清單不再有「lint still fails … voice」，主機 `video.json` 裡 shi-mo／s01-* 各有 `voice {provider: "gemini", name, style}`。
- [ ] 部署後想固定某個配角的聲音：站上設定集給它 `voice`（會退回文件待審，代價見上）；不固定就照工人挑的。

## Notes

- 卡司六個無聲角色的 `voice_note` 是中文描述（例如石魔「低沉、緩慢」）：`castVoices` 從名字、role、`voice_note` 讀「女／姐／娘／清脆…」或「男／爺／低沉／沙啞…」決定男女聲，兩種都沒提就拿下一個沒用過的；聲音池的項目用 `hint`／`style` 判男女。正式站 drama 分頁的 `character_voice_pool` 這次沒讀到（分類器擋），空池時只用 `SPARE_VOICES`。
- 挑法對同一本設定集、同一組設定是確定的（id 順序），所以每一集同一個配角同一個聲音；聲音池或人物表改了才會變。e005 這種 `series.json` 沒 voice、`settle` 補的，style 沒有 `voice_note`（series.json 沒帶），只有聲音名；之後起草的集數由 `castFrom` 補，帶 `voice_note` 當 style。
- 發現於票 2026-10-25-drama-series-episodes-can-be-redone 的部署後查證。
