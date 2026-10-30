---
id: 2026-10-30-curio-s-axis-rewrite-the-28
title: Curio S axis: rewrite the 28 unmade episodes under the 10-25 rules, no burned subtitles
status: in-progress
priority: P1
area: docs
owner: claude-opus-5-5-curio-s-rewrite
claimed_at: 2026-10-30T19:40:54Z
created_at: 2026-10-30T19:36:56Z
completed_at:
branch: claude/quizzical-cray-17decd
depends_on: []
scope:
  - docs/videos/curio-s07
  - docs/videos/curio-s16
  - docs/videos/curio-s19
  - docs/videos/curio-s20
  - docs/videos/curio-s32
  - docs/videos/curio-s33
  - docs/videos/curio-s37
  - docs/videos/curio-s41
  - docs/videos/curio-s42
  - docs/videos/curio-s43
  - docs/videos/curio-s44
  - docs/videos/curio-s45
  - docs/videos/curio-s46
  - docs/videos/curio-s47
  - docs/videos/curio-s48
  - docs/videos/curio-s49
  - docs/videos/curio-s50
  - docs/videos/curio-s51
  - docs/videos/curio-s52
  - docs/videos/curio-s53
  - docs/videos/curio-s54
  - docs/videos/curio-s55
  - docs/videos/curio-s56
  - docs/videos/curio-s57
  - docs/videos/curio-s58
  - docs/videos/curio-s59
  - docs/videos/curio-s61
  - docs/videos/curio-s62
  - docs/videos/history-curiosity/topic-checks/S07.md
  - docs/videos/history-curiosity/topic-checks/S16.md
  - docs/videos/history-curiosity/topic-checks/S19.md
  - docs/videos/history-curiosity/topic-checks/S20.md
---

# Curio S axis: rewrite the 28 unmade episodes under the 10-25 rules, no burned subtitles

## Why

站主 2026-10-31：「已上架的要另外改新規則，未上架的要改新規則，還沒製作的也要改成新規則，然後都不要燒字幕了。」
這張票只管**還沒製作**的 28 支 S 軸（後台沒有成片）。已上傳片重新合成、舊規則已上架片重做、品牌故事改歸 W 軸是別的 session 的工作，
整體計畫在分支 `claude/video-reclassify-rules-44b738` 的 `docs/videos/history-curiosity/new-rules-migration-20261031.md`。

新規則（`.agents/skills/curio-episode/SKILL.md` §跟高點閱頻道的差距）：13 分鐘、開場五步、每章一句「你」與一句旁白的反應、標題公式、
縮圖 layout d、配樂、`look` 只能是 cute-mystery、每 30–45 秒一個鉤子。`video.json` 一律明寫 `"subtitles": {"burn_in": false}`。

## Definition of done

- [ ] 第一批 5 支（S07、S16、S19、S20、S48）的稿子通過獨立查核、盲評 `narrative`（兩位讀者，兩位都否才算沒過）與 `lint` 0 錯誤。
- [ ] 第一批的旁白、插圖、配樂報價交給站主，核准後才花錢。
- [ ] 其餘 23 支照〈順序〉一批最多 5 支做完。

## 28 支的稿子在哪（2026-10-31 查的）

都還不在 main 的只有後面 24 支；舊稿字數是旁白 `lines[].text` 的字元數。

| 代號 | 舊稿所在 | 舊稿字數 | 後台狀態 | 批次 |
| --- | --- | ---: | --- | ---: |
| S07 | main | 2,279 | 旁白、分鏡已核准 | 1 |
| S16 | main | 2,305 | 旁白、分鏡已核准；本機有 10-25 舊規則 `final.mp4`，沒送審 | 1 |
| S19 | main | 2,286 | 同上 | 1 |
| S20 | main | 2,328 | 同上 | 1 |
| S48 | `origin/codex/curio-preproduction-s46-s56-20261020` | 2,945 | 有旁白，插圖已畫 | 1 |
| S37 | `origin/codex/curio-s34-endurance-20261019` | 2,181 | 有旁白 | 2 |
| S42 | 同上 | 2,263 | 有旁白 | 2 |
| S43 | 同上 | 2,755 | 有旁白 | 2 |
| S44 | 同上 | 2,255 | 有旁白 | 2 |
| S45 | 同上 | 2,582 | 有旁白 | 2 |
| S46 | `origin/codex/curio-preproduction-s46-s56-20261020` | 2,696 | 有旁白 | 3 |
| S49 | 同上 | 3,225 | 有旁白；PR 1632 記 61/115 景 KEEP | 3 |
| S50 | 同上 | 2,722 | 有旁白 | 3 |
| S51 | 同上 | 2,530 | 有旁白 | 3 |
| S53 | 同上 | 2,492 | 有旁白；PR 1632 記 46/107 景 KEEP | 3 |
| S54 | 同上 | 3,244 | 有旁白 | 4 |
| S55 | 同上 | 3,193 | 有旁白 | 4 |
| S56 | 同上 | 2,919 | 有旁白 | 4 |
| S57 | `origin/codex/curio-preproduction-s57-s59-20261021` | 3,121 | 有旁白；音檔檢查 43 句待判讀 | 4 |
| S32 | `origin/codex/curio-s34-endurance-20261019` | 2,267 | 沒有旁白 | 4 |
| S33 | 同上 | 2,439 | 沒有旁白 | 5 |
| S41 | 同上 | 2,316 | 沒有旁白 | 5 |
| S47 | 同上 | 2,740 | 沒有旁白 | 5 |
| S52 | `origin/codex/curio-preproduction-s46-s56-20261020` | 2,556 | 沒有旁白 | 5 |
| S58 | `origin/codex/curio-preproduction-s57-s59-20261021` | 3,098 | 沒有旁白 | 5 |
| S59 | 同上 | 3,182 | 沒有旁白 | 6 |
| S61 | `origin/codex/curio-s61-halifax-second-20261022` | 2,668 | 沒有旁白 | 6 |
| S62 | `origin/codex/curio-s62-jupiter-20261022` | 2,574 | 沒有旁白；PR 1662 記 36/109 景 KEEP | 6 |

順序的理由：第一批是已付插圖最多的五支；之後先做旁白錢已經花掉的（改稿才要重錄，越早定案越不會再多花），沒有旁白的排最後。

## 有沒有別人在做（2026-10-31 查的）

- 其他 session：`curio-old-remakes`、`curio-w-axis`、`burn-in-reassemble` 都不碰這 28 支。
- Codex：這 28 支在遠端的最後一筆提交都是 10-22 以前，六條草稿 PR（#1632、#1637、#1661、#1662 等）從 10-22 起沒更新，判定沒有在做。Codex 若要恢復這些 PR 會跟這張票重疊，要先停。

## Notes

每批查核、盲評、報價寫在各集的 `NOTES.md`。

### 第一批進度（2026-10-31，隨做隨更新）

| 集 | 字數 | lint 估 | 查核 `verify-2.md` | 盲評 |
| --- | ---: | ---: | --- | --- |
| S07 | 2,894 | 11.8 分（低於 12） | 有條件通過，問題已全改 | 通過，七輪 |
| S16 | 3,151 | 12.8 分 | 有條件通過，問題已全改 | 通過，九輪；最後一位 13/13 |
| S19 | 2,973 | 12.1 分 | 有條件通過，問題已全改 | 通過，四輪；最後一位 13/13 |
| S20 | 2,915 | 12.1 分 | 有條件通過，問題已全改 | 通過，四輪 |
| S48 | 2,837 | 11.6 分（低於 12） | 有條件通過，問題已全改 | 通過，六輪 |

五支 `lint` 都 0 錯誤。盲評依主機規則：同一題兩位都答否才算沒過；ballot 在各集 `panel/`。查核都只覆看到改稿前的版本，查核後的修改多半是刪句，新句只有少數幾句。

### 第一批報價（2026-10-31，`--dry-run` 算的，還沒花錢，等站主核准）

| 集 | 要畫 | 插圖上限（三張，含評審） | 旁白句數／計費字 | 備註 |
| --- | ---: | ---: | --- | --- |
| S07 | 81 張 | US$3.28 | 122／約 2,970 | 舊圖在別的環境，本機沒有檔，全部重畫 |
| S16 | 3 張 | US$0.12 | 124／約 3,200 | 75 張舊圖吃本機快取 |
| S19 | 11 張 | US$0.45 | 118／約 3,060 | 59 張舊圖吃本機快取 |
| S20 | 4 張 | US$0.16 | 120／約 2,990 | 75 張舊圖吃本機快取 |
| S48 | 92 張 | US$3.73 | 112／約 2,900 | 舊圖在 Codex 的環境，本機沒有檔，全部重畫 |

- 插圖合計上限 US$7.74（191 張）；另留 US$0.40 給沿用圖換了新景 id 的重新評審。工具的 dry-run 不扣快取，所以 S16、S19、S20 是用「新稿提示詞不在舊稿裡」算的，圖片快取鍵不含景 id（`keyframes.mjs` `imageKey`）。實際多半只到上限的六成：之前同類每集 US$1.65–2.39。
- 旁白：Gemini 每秒 US$0.000225，五集約 60 分鐘，約 US$0.81，含重錄上限 US$1.25。
- 配樂：五首上限 US$0.75。
- **五集合計上限約 US$10.15，預估約 US$6。**
- 不能沿用的舊錢：五條舊旁白約 US$0.68 作廢；S16、S19、S20 本機 10-25 的舊規則成片作廢。S07、S48 已付的插圖若能從 Codex 的環境取回，可少畫約 170 張、省約 US$4；目前拿不到。

### 第二批進度（2026-10-31）

| 集 | 狀態 |
| --- | --- |
| S37 | 3,219 字，lint 估 13.3 分；查核問題全改；盲評通過（四輪，最後一位 13/13） |
| S42 | 2,829 字，lint 估 11.7 分（低於 12）；查核問題全改；**盲評未過**：其他十二題都過，`no_recap` 沒有讀者答是（五輪，各指不同句，都已改） |
| S43 | 3,100 字，lint 估 13 分；查核問題全改；盲評通過（六輪） |
| S44 | 3,239 字，lint 估 13.5 分；查核問題全改；**盲評未過**：其他十二題都過，`no_recap` 沒有讀者答是（五輪，最後指的是片尾答案那句，沒改） |
| S45 | 3,141 字，lint 估約 13 分；查核問題全改；**盲評未過**：三輪，no_spoiler、payoffs、no_recap 兩位都否，各指不同句，都已改，沒有再讀 |

五支 `lint` 都 0 錯誤，舊稿都從 `origin/codex/curio-s34-endurance-20261019` 帶進來。接手時：`docs/videos/<slug>/verify-2.md` 有查核結論；盲評照第一批的做法（只給讀者 `narrative --slug S --json` 的輸出，同一題兩位都否才算沒過，ballot 放 `panel/`）。

**第二批報價（還沒花錢，等站主核准）：** 本機沒有舊圖，全部要畫。插圖 466 張，三張上限 US$18.87（S37 4.29、S42 3.04、S43 4.05、S44 3.60、S45 3.89）；旁白約 US$0.88、含重錄上限 US$1.30；配樂上限 US$0.75。**合計上限約 US$20.9，預估約 US$12.5。** 五條舊旁白作廢。

**`no_recap` 的觀察：** 這題最容易沒完沒了。讀者照「一句破功就否」讀，每一輪都能指出新的一句，片尾答案那句更是怎麼寫都算重述。第二批七成的盲評輪次都花在這一題。後面幾批可以考慮只改讀者指出、真的是緊鄰重述的句子，其他的交站主判。

### 給後面幾批的教訓

- 撰稿代理寫出的稿子，查核每支都抓到 1–3 個真錯誤，全都在新加的句子或旁白自己接的因果；不能省。
- 盲評最常退的四件事，協調者先讀一遍就修掉，能省好幾輪（S07 不先修跑了七輪，S19 先修後第一輪只剩一題同否）：跟主線無關的軼事與支線；幾本書連著念各寫什麼；沒有答案的反問（「你還會跟嗎？」改成直述）；開場把結果講掉。
- 撰稿目標 3,300–3,600 字太高：查核表裡夠多的事實，但盲評會把岔題刪掉，定稿落在 2,900–3,250 字、lint 估 12–13.4 分。
- lint 認的問句要在句尾；句中的問號不算鉤子。

### 其餘 18 支

狀態都是「舊稿在 Codex 分支、還沒改寫」，順序見上表的批次欄（第 3 批起）。一批寫稿加查核加盲評約 150–200 萬 token（撰稿每支約 35 萬、查核約 25 萬、讀者每位約 8.5 萬）。
