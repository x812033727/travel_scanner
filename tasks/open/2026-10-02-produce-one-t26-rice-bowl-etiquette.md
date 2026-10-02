---
id: 2026-10-02-produce-one-t26-rice-bowl-etiquette
title: Produce one T26 rice-bowl etiquette episode with measured eight-minute body
status: in-progress
priority: P2
area: docs
owner: codex-t26-production
claimed_at: 2026-10-02T08:17:25Z
created_at: 2026-10-02T08:17:12Z
completed_at:
branch: codex/sothatswhy-t26-pilot
depends_on: []
scope:
  - docs/videos/sothatswhy-t26/
---

# Produce one T26 rice-bowl etiquette episode with measured eight-minute body

## Why

站主已在後台看到 473 份長片企劃，並指定先製作第二季 T26〈為什麼日本常端飯碗，韓國卻常放桌上？〉。原文字包只有大綱，須接成實際影片；所有長片正文與成片均須至少八分鐘。

## Definition of done

- [x] 完整繁中逐字稿、原創插畫分鏡與來源通過獨立查核及聽眾審稿。
- [ ] 依現有核准的語音供應商與額度完成旁白，插畫使用原創 SVG；正文與成片實測皆至少 480 秒。
- [ ] 繁中可選 CC、成片 QA 與預覽保存，後台可看到這一集的實際製作紀錄。

## Steps

- [x] 站主選定 T26；查任務、worktree、遠端分支與 PR，新的逐字稿目錄無碰撞。
- [x] 刷新五個一手來源，撰寫完整稿件與分鏡；179 句完成獨立事實與口語覆核。
- [x] 語音及圖片 dry-run，確認現有設定、額度與重複項目。
- [x] 完成現行 native 圖解版：180 clips、純講述 714.02 秒；正文時間軸 890.033 秒。正常音訊檢查零旗標，後台核准綁定目前時間軸。
- [ ] 單集製作、試聽、合成、字幕及實際時長 QA。

## How to verify

`node tools/video/cli.mjs lint --slug sothatswhy-t26`、`status`、`tts --dry-run`、`keyframes --dry-run`；製作後核對時間軸、成片雜湊、`checks.json`、繁中字幕 manifest 及 `qa`，在後台確認綁定同份素材的紀錄。

## Notes

- 只製作這一集；不擴成 473 題批次，不新增配音語言，不上傳或公開。
- 採直接 CLI 插畫投影片路線；舊 one-off flat-explainer 走 drama 全域 queue，不能用全域開關保證只跑一集。
- 原資料包中歷史 480 秒企劃以 long-form 有效 600 秒輸入取代；正文不得用片頭片尾湊時長。
- 媒體留在 repo 外，保留現有 uploader 關閉狀態；不輸出憑證。
- 正式站 2026-10-02 預檢：T26 無重複製作狀態，語音可用；slides/drama 生圖開關皆關閉，另有六支舊影片被圖片開關阻擋。未啟用全站開關、未暫停或重啟 worker。
- 插畫改用可精確控制餐具與左右位置的原創 SVG，使用既有 `diagram` 版型與正常素材驗證；不偽造 keyframe manifest，不沿用 AI storyboard 核准。仍逐項做正常成片 QA，另按實際時間軸驗每狀態最多 8 秒與至少一半圖解。
- 正常語音 dry-run 4,421 字元，實際初版 4,561 字元；四景正常切段 fallback 的原始付費輸出及請求雜湊已保存於 repo 外 `_requests/`。自動網路重試被外部 launcher 停止，未知結果不重送。
- 最新圖解企劃已經正常 outline judge 選 A 並重新送審；任何文字或圖像修改都須重新綁定對應的審查與素材雜湊。
- 現行主稿 SHA256 `90975caf8b5f719d6f7f49fd0da4c80a8058cd376df74fc8db6242dd8b044f25`；157 原創 SVG 與 manifest 已通過獨立逐圖覆核，實際 180 狀態最長 7.667 秒、平均 4.945 秒，圖解占正文 87.963%。
- 初次正常 render 被 157 個 diagram 的進場動畫版面誤檢阻擋：獨立 DOM 實測動畫結束後 overflow 為零；依賴修正另認領 `2026-10-02-video-render-settled-layout`，不改主題 CSS 或檢查門檻。修正後必須正常重渲染並取得零問題 manifest，不能手動清除旗標當作過關。
- 完整 180 個 renderer still 與逐句敘事映射覆核另發現 `c5-s01-detail` 餐具出現太早、`c6-s12-detail` 缺少托碗對照；原圖作者僅修正這兩張 SVG，保留已通過的台詞及 WAV，重新綁定 manifest、獨立視覺審查與正常 renderer 輸出後才能合成。
- 修訂 native manifest 為 `11cd8be93dace7a2775e2b586294c111cb9ece036db0153033c30d27cd36b3a5`。正常全片 force render 零問題，兩新圖再正常增量 render；獨立實看兩新 renderer 圖並核對全部 180 個 states、178 張未變 PNG bytes、2,096 個 transition files 及 current renderPlan，兩項必修已閉合。這不代替完整 MP4／聲音／字幕的後續檢查。
- 未使用的候選及轉換前完整主稿已逐 byte 複製、SHA256 驗證保存至 repo 外 `_source/native-conversion/`；目前 repo 保留唯一實際 `video.json`。
