---
id: 2026-10-25-bug-5-lint-v5-s01-voice
title: 《系統說我是 BUG》第 5 集卡在 lint：設定集 v5 的石魔與六個 s01- 配角沒有 voice，重做的第 1–4 集可能一樣
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-25T05:52:41Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/automation/flow.mjs
  - tools/video/core/lint.mjs
  - tools/video/core/schema.mjs
---

# 《系統說我是 BUG》第 5 集卡在 lint：設定集的配角沒有 voice

## Why

2026-10-25 部署 #1840 後查主機：第 5 集（新規則下的第一集，`xitong-shuo-wo-shi-bug-e005`）在後台的檢查清單停在「卡住，需要人處理：lint still fails after 3 fixes: characters[3].voice: must be an object with provider and name」，工作區沒有 video.json（寫手的答案在 `run-receipts/`）。

站上設定集 v5（已核准）的 `body_json.characters` 共 13 個：前 7 個（江河、系統、千凜、白珩、阿桂、小鐵、唐測）有 `voice {provider, name, style}`，後 6 個 `shi-mo`、`s01-lao-qi`、`s01-qi-yan`、`s01-huo-zhangchui`、`s01-yan-guan`、`s01-a-zhu` 只有 `voice_note`、沒有 `voice`。`flow.mjs` 的 `castFrom` 把該集會出現的角色抄進 video.json，`core/schema.mjs` 的 `validateVoice` 對每個角色要物件，lint 自動修三次都修不回來（寫手不能自己發明聲音）。

第 1–4 集 10-25 05:48Z 已用「重做」回到 `ready`（票 2026-10-25-drama-series-episodes-can-be-redone），第 1 集 `e001-redo1` 寫手跑中；這四集的卡司也從同一本 v5 抄，只要用到那六個角色就會撞到同一個錯。

## Definition of done

- [ ] 第 5 集與重做的第 1–4 集不再因 `characters[n].voice` 被 lint 擋。
- [ ] 設定集裡沒有 `voice` 的配角有一個固定的處理：工人從作品的 `character_voice_pool`／設定集的 `voice_note` 補一個 Gemini 聲音（寫進 video.json 不改設定集），或 lint 對只有 `voice_note` 的配角明確報「設定集缺聲音」讓站主在站上補。
- [ ] 不改 `lookHash`（已畫好的設定圖不重畫）。

## Steps

- [ ] 主機看 `e005/run-receipts/` 寫手最後一版的 characters，確認 characters[3] 是哪一個角色；看 `e001-redo1` 有沒有同樣卡住。
- [ ] 決定補聲音的位置：站上改設定集（`PUT docs/setting` 帶 `approve:true`）會把總綱、細綱退回待審、ready 集退回 planned，要依序重核准，代價大；工人端在 `castFrom`／`settle` 補聲音最小。
- [ ] 補完後後台「重試」第 5 集（deferred 的要先清 `auto.json` 的 `deferred_until`）。

## Notes

- 卡司六個無聲角色的 `voice_note` 是中文描述（例如石魔「低沉、緩慢」），Gemini 聲音名要從 `character_voice_pool` 或頻道常用的男女聲挑。
- 發現於票 2026-10-25-drama-series-episodes-can-be-redone 的部署後查證。
