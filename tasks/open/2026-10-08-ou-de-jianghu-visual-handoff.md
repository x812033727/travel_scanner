---
id: 2026-10-08-ou-de-jianghu-visual-handoff
title: 《偶的江湖》角色資產鎖定與第一集動畫試播交接
status: open
priority: P1
area: docs
owner:
claimed_at:
created_at: 2026-10-08T10:52:24Z
completed_at:
branch: codex/ou-de-jianghu-visual-preproduction-20261008
depends_on:
  - 2026-10-08-ou-de-jianghu-animation-reference
  - 2026-10-08-ou-de-jianghu-scene-prop-design
  - 2026-10-08-ou-de-jianghu-external-look-import
scope:
  - docs/videos/series-plans/ou-de-jianghu/visual-development/handoff
---

# 《偶的江湖》角色資產鎖定與第一集動畫試播交接

## Why

把採用圖、參照和正常look綁到同一來源，第一集試播才能沿用同一張臉；production README仍寫過期14人。

## Definition of done

- [x] 9人資產manifest含來源commit／SHA、角色／look ID、用途、版本、媒體hash、judge與站主接受狀態；額外綁shot_looks目錄hash，不冒稱原生lookHash已有。
- [ ] 經正式匯入走正常look／choice／series-store；用少量已授權關鍵影格核對真正讀入的reference及當鏡造型文字，保存實際結果，不假填。
- [ ] 劇本／look／audio／storyboard／plan lock分別列；前期畫像完成不等於動畫完成。完成原持有人交接後更新production README，將前置條件接回既有試播票，保留連續三鏡及站主接受後放量。

## Steps

- [x] 讀[前期總覽](../../docs/videos/series-plans/ou-de-jianghu/visual-development/README.md)、[造型規格](../../docs/videos/series-plans/ou-de-jianghu/visual-development/character-design.md)、[製作清單](../../docs/videos/series-plans/ou-de-jianghu/visual-development/production-list.md)，重新核對來源與既有授權。
- [x] 完成可審交接文件，將實際證據及未決問題記入本票 scope；正式採用／正常runtime與原持有人接線仍保留待辦。
- [x] 候選實看與獨立核對範圍、匯入收據、SHA及圖冊驗證已整合；正式製作條件尚未滿足，收尾release。

## How to verify

逐項查驗實際文件／圖檔、來源及媒體雜湊與接受紀錄；涉及圖像必須實看，prompt／lint不能代替圖片驗收。

`npm run check:tasks`

## Notes

- 2026-10-09 瀏覽器試拍：站主指定 Codex IAB 並登入，沿已採用316.8點pilot額度完成7次逐鏡圖像（156點）與3支H3四秒片（144點），合計實扣300點，帳戶27000→26700；無購點／續訂／API／TTS。s036兩版接觸末格都因冠尖與指段重疊歧義退回，未送接觸版影片。站主明確核准「採用懸停方案，繼續製作」，只在外部副本改s036 motion／end_frame.prompt、建立獨立native lock，原v4／正常lock未改。詳見[本輪製作紀錄](../../docs/videos/series-plans/ou-de-jianghu/visual-development/handoff/hailuo-browser-pilot-20261009.md)。正式look/audio/storyboard、變更接回及片段匯入仍待辦；s035結尾手落身側接s036懸掌存在抬手跳接，3秒／2秒估剪也需改用實際動作收勢，需在放量前解決，不能把本輪下載／decode／抽格當owner接受。本輪claim前scope無其他active、唯一PR#1388屬同隊；--force僅略過同隊未結相依，不接管production原持有人。

- 2026-10-09 正式採用：站主明確回覆「採用素材與 v4，按此點數上限鎖定 plan」。[採用紀錄](../../docs/videos/series-plans/ou-de-jianghu/visual-development/handoff/adoption-decision-20261009.md)／JSON逐一綁定146素材、既有限制、v4、兩期逐鏡預算與正常plan鎖。本期含預留26,980.8點、pilot316.8包含在內，第二期21,753.6須有實際額度，不購點／續訂、API支出授權0。原生write/check exit0且changed=false，455鏡 Hailuo Max H3/2K/assist off，lock SHA `6af3dafa4f9edc0a03270800a9d3fd44c6f487a3c015627fda4a4205f385d0c5`。ready exit1、2過429待製作，look依決定保留待判圖。
- 本輪最新9張基底（沈全身v3）已接入正常runtime，27次dry-run/import/exact-rerun全exit0，0fetch／0paid；manifest SHA `cf37aa3541380f13b864d3c01560e533fc176e7c5d85f472560408e85f7406b6`。正式來源與素材SHA重驗；沒有choice／judge／series-store或其他關卡核准。Hailuo空白表單核對Max27000點、H3 2K 4秒48點；Mokaair唯讀狀態drama=false及API單集200，未改設定。兩個剩餘DoD仍涵蓋真實判圖／參照送入／原持有人接線，因此本票保留open並release，不把plan完成當整條產線完成。

- 2026-10-09 最後整合完成：新 [asset-manifest](../../docs/videos/series-plans/ou-de-jianghu/visual-development/handoff/asset-manifest.json) 核實 146 unique latest＝9 concepts＋27 portraits＋82 new references＋28 scenes/props，另 9 front reuse＝91 reference uses；29 份文件 hash 綁定含 portable gallery／fan／mouth reviews。455 鏡 mapping 最新 SHA 全過；193 鏡的扇分派都含 construction-details-v3＋personal-prop-states-v3，concept-v5/right-profile-v3/left-three-quarter-v3 僅身份服裝，沒有宣稱全圖扇拓撲一致。9 舊匯入逐筆保留 historical v3 與像素是否仍同新基底；沈 full-body-v3 未匯入／核准。build-manifest、其 --check、mapping --check、tasks check（1692票）與 scoped diff --check 全 exit0；只有其他票的 stale warnings。未 commit/push，release 交主控；source_commit 記當次工作基線，不因之後 commit 自動重建迴圈，正式採用 DoD 保留未勾。

- 2026-10-09 主控再分工 codex-ou-final-handoff 整合本票 `build-manifest.mjs`／README 與新收據：再次 who-is-on-it 查無 active scope、唯一 PR #1388 是同隊；claim `--force` 只略過同隊修圖／場景候選的未結相依。待主控最後修圖收據凍結後，依序重建 455 鏡 mapping 與 146 unique manifest，再 check/release；不改 production，不填 P7／owner／paid readiness，舊 9 筆匯入維持 v3 歷史。

- 2026-10-09 補交 [finalization](../../docs/videos/series-plans/ou-de-jianghu/visual-development/handoff/finalization-20261009.md) 與 455 鏡 JSON／離線 builder。消費新 finalized 畫像／動畫參照收據；57 logical keys 的候選 hash、12 正典來源、27 原生 PNG header 核實，保留 18 張 native_below_target，未放大。6 個棋局狀態逐坐標與場景決定相等；冷場全部使用 clean master-v4＋狀態 spec，舊 cold-v* 不送模型。規劃 reference 並非已送模型；全部 final binding／owner acceptance／runtime 仍未寫。舊 9 人 staging 維持 v3／沈 full v1 歷史紀錄。本次只新增收尾檔，不改 README/build-manifest/asset-manifest；release 交主控整合，正式採用 DoD 不冒填。

- 2026-10-09 本輪收尾：由主控分工 codex-ou-final-handoff 補 `handoff/finalization-20261009.md/.json` 及離線重建／驗證器，不改既有 README、build-manifest、asset-manifest、production 或 approval。who-is-on-it 再查 handoff 無其他 active claim，唯一相關 PR #1388 即本團隊目前分支；`--force` 僅略過同團隊動畫參照／場景候選尚未結案的相依，不接管其他持有人，也不表示個別候選採用。完成後交回主控整合新資產 SHA。

2026-10-09收尾：[交接包](../../docs/videos/series-plans/ou-de-jianghu/visual-development/handoff/README.md)與 [asset-manifest](../../docs/videos/series-plans/ou-de-jianghu/visual-development/handoff/asset-manifest.json)已備妥。12來源SHA、139張唯一latest候選（9概念＋27畫像＋74新角色參照＋29場景道具）、9張正面沿用關係、16種shot_looks獨立hash、9張隔離pending匯入及16份交付來源文件SHA已核對。正常lookHash為9b3e6914dbc8d109，僅來自隔離工作提案，不冒稱涵蓋shot_looks或正常runtime。455鏡v3／v3.1、全長文字animatic觀看、兩期預算及a02-s035～s037連續小樣計畫可直接審。白扇母版、紙窗近景、棋盤、原生尺寸及23:23.533估時差異均明列。剩餘兩DoD保留：正式個別採用／judge與正常關卡、當鏡真實參照驗證，以及production／原試播票持有人交接；沒有paid動畫或假approval。

- 2026-10-08 續做：本票 scope 收窄為 handoff/，先完成可審閱的第一集交接包；production/README.md 的原持有人交接及正式 runtime 選用/付費小樣仍列待辦，不占用其 scope。who-is-on-it 對 handoff/ 查無 active claim 或其他 PR。依站主「好 續繼都完成」授權，使用 --force 僅略過同一分工中尚未結案的三張相依票，並非覆蓋別人持有者、預算或站主接受。

第8集持有人占production scope，不能強行claim／覆寫。本輪未改既有試播票depends_on；接線仍待辦，要改它時先將精確路徑加入scope並完成所有權交接。後續14人／16狀態按同流程分批，不阻塞第一集。

- 2026-10-08建票快照：當時依站主「先補齊任務、造型規格與畫像製作清單」新增待辦，尚未生成或核准媒體；後续交付見2026-10-09紀錄。沒有部署或發布。
