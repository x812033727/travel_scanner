---
id: 2026-10-19-curio-s19-eiffel-tower-historical-episode
title: Curio S19 Eiffel Tower historical episode
status: in-progress
priority: P2
area: docs
owner: codex-s05
claimed_at: 2026-10-19T20:17:20Z
created_at: 2026-10-19T20:17:17Z
completed_at:
branch: codex/curio-s34-endurance-20261019
depends_on: []
scope:
  - docs/videos/curio-s19
---

# Curio S19 Eiffel Tower historical episode

## Why

使用者希望歷史系列繼續擴充。題庫 S19 說鐵塔「原本只拿到二十年的許可」和「1909 年差點拆掉」，但二十年可能是艾菲爾的經營權，不是建物必拆條款；無線試驗、軍用電報與廣播也在不同年代。必須先核對 1887 年契約與官方年表，才能把這個反差講成可信的故事。本票只認領 `docs/videos/curio-s19`，不改共用題庫或其他集數。

## Definition of done

- [ ] 固定可讀原始契約及官方歷史來源，逐句查核 20 年、期滿、抗議與無線電時序。
- [ ] 做成 8–10 分鐘 S 軸劇本、逐句 claims、70% 以上插圖分鏡、0/0 lint 和獨立敘事盲讀。
- [ ] 經根集協調付費媒體時段及整集上限後，完成語音、插圖、成片 QA 和上架包。

## Steps

- [x] 查同題是否已認領，開窄 scope 票，建立原始文件入口與風險清單。
- [ ] 取得 1887 年協議第 11 條與官方無線電史頁的固定可讀文本；解決目前代理伺服器 CONNECT 403。
- [ ] 完成企劃、劇本、來源對照與盲讀；S19 目前不得付費製作。

## How to verify

史料入口及待決問題在 `docs/videos/curio-s19/research.md`。完稿後 `node tools/video/cli.mjs lint --slug curio-s19` 應 0 errors／0 warnings，並以來源隔離讀者核對精確 `script.md` SHA。

## Notes

- 2026-10-19：SETE 官方所有權與無線電史頁、法文維基文庫協議原文均由代理伺服器回 CONNECT 403，讀取權限提高後仍相同。固定 GitHub 上的法英維基百科快照僅用於發現矛盾與定位文件，**不作已核原始證據**。題庫標題與 finding 暫不得直接變旁白；詳見 `research.md`。
- S05 仍在語音與成片製作；S19 只做無付費前期。根集要求避開目前 MiniMax 限流，付費製作時段由根集另行協調。
