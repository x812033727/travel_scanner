---
id: 2026-10-15-curio-m09-research-outline
title: Curio M09 research and outline
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-10-15T16:34:56Z
completed_at:
branch: codex/curio-next-five-20261016
depends_on: []
scope:
  - docs/videos/curio-m09
---

# Curio M09 research and outline

## Why

站主要求繼續製作五集奇聞檔案局；本票負責 M09 安提基特拉機械的更新研究與雙大綱，清楚區分殘存零件、推知功能及現代重建。

## Definition of done

- [x] 保存本次研究 research.md、可追溯 claims.md 與兩案 brief.md。
- [x] 獨立查核員覆核來源及敘事，修正確有依據的問題。
- [x] 協調者完成原大綱的站主選綱交接。
- [x] 2026-10-16 續作核准 A 的完整正式稿、逐景提示、claims、loops 與兩支 Shorts 稿。
- [x] schema／lint 與 Shorts 結構檢查通過，作者本機驗證收據落地。
- [ ] 正式稿由另一位查核員與盲評者覆核，協調者套用修正後送站主。

## Steps

- [x] 讀系列與故事規則，參考 H01-v2 前 30 景。
- [x] 唯讀承接 M09 題庫，重開主要論文、2021 更正及研究機構頁。
- [x] 補查 2024 月曆環孔數研究的作者機構摘要，避免稱前盤已完全破解。
- [x] 寫 A 推薦／B 替代、10 分鐘節拍與至少三個開場 loops 預案。
- [x] 獨立覆核。
- [x] 依站主核准 A 寫完整稿；「獨立覆核」的已勾項只指原大綱，不涵蓋這次正式稿。
- [ ] 完成正式稿的獨立查核、聽眾審稿與十三題盲評。
- [x] 回應初輪獨立退修：背盤小盤配置、2016 原論文及片尾岔題；重跑機械檢查並交新查核／盲評。

## How to verify

核對來源 ID、claim 與大綱每個轉折；兩案預算各 600 秒。確認 30 只指殘存齒輪、69 只指 2021 模型。協調者統一執行 `git diff --check` 與 `npm run check:tasks`。

## Notes

- 查核日期 2026-10-16（Asia/Taipei）；票號沿用任務工具的 UTC 2026-10-15 日期。
- 唯讀題庫來源提交 `949bb91fc85d41a53633d056062b27d87651e9d5`，不改共享題庫。
- Nature 與 PMC 一般頁部分請求回驗證殼；2021 本文與更正實際從 Europe PMC 全文 XML 讀取。2006 使用 PubMed 摘要，2008 使用可讀的 Nature 摘要，沒有聲稱讀完付費全文。
- 2024 孔數是研究模型與孔洞問題，不能替換齒輪數。本案不岔入統計細節，也不把 2021 模型叫最新定論。
- 1902 發現者、潛水深度與掃描機重量不進稿；沒有足夠本次證據就不硬加戲。
- 2026-10-16 01:01（Asia/Taipei），協調者完成手動大綱送審並讀回 `pending`；review ID：`264fb9fa-e606-4b4e-93e3-ef7c07b7878d`，對應 brief SHA-256：`B9BE6725FEA76B516A03E2498ABCEACE0A158EA3FDC40A5C88ED5EA9E850DEE7`。送審版 brief 未再修改。
- 交接完成，釋出本票認領；仍待站主選 A／B 大綱，以及本批 US$30.00 估算停手上限授權（尚未核准）。正式生產尚未開始，沒有付費請求或 worker 啟動；本票未標 done，整集尚未完成，由協調者統一 commit／PR。
- 2026-10-16 獨立覆核意見已修：2021 明標電腦重建，不暗示實體複製品已驗證；1901 開場為後見描述，不畫潛水員當場識別齒輪；盤面以同一次操作帶用途，避免三個定義連念。研究／大綱版已凍結，不代表正式稿或完整敘事 QA 已通過。

### 2026-10-16 正式稿續作

- 協調者讀回原 review `264fb9fa-e606-4b4e-93e3-ef7c07b7878d` 已核准 A；五集本批每集 US$6／總 US$30 已授權，紀錄在 `docs/videos/curio-next-five-20261016/decision-20261016.json`。本票重新以 `codex-curio-h12-m09-scripts` 認領。
- 原核准 brief SHA：`b9be6725fea76b516a03e2498abceace0a158ea3fdc40a5c88ed5ea9e850dee7`。協調者授權補現行 lint／host 所需欄位與選項外核准／預算狀態；A／B 正文到文末逐字比對原版一致。新 SHA：`ac48bd3339b2e7b0c406304574b23bff794f182529b9e611e8537c7df4a75d5d`，由協調者重新送審，不沿用舊核准 hash。
- `video.json`、`script.md`、`loops.md`、`shorts.json` 完整落地。95 景／97 句、89 插圖景，七章，估約 9.5 分鐘；不是音訊實測。2021 全文 XML 再讀，傳動、視逆行、管軸及假設指針補入 C18–C22。
- 本機 `lint` 零錯誤；2 個研究角色／室內場地頻率提示保留，同一殘片的研究主線已跨館藏、成像、盤面示意與電腦模型。三個開場鉤子與回收景 prompt 完全相同；claim ID 完整，兩支 Shorts schema 及母片 shot 引用均通過。詳見 `script-validation.json`。
- 等待正式稿獨立查核、聽眾審稿、十三題盲評、補格式大綱重核准及正式劇本核准。作者 paid calls = 0、backend submissions = 0、worker starts = 0；發音字典未改。僅提交本票及 H12/M09 文件範圍，保留進行中供覆核修訂。
- `npm run check:tasks` 通過（1895 票，既有過期認領及其他 scope 重疊警告保留）；本次文件 `git diff --check` 通過。正式稿 SHA-256：`0b429837043354ee66b02c891f9b1aee07adf0c8df7b13049885ca8e56127f37`。

### 2026-10-16 初輪退修回應與獨立重驗交接

- 補格式新版 brief 已讀回 `approved / A`，review `fd7cc099-0397-4f9c-ab08-e601b21e4e87`；讀回見批次 `format-decision-20261016.json`。brief SHA 仍為 `ac48bd3339b2e7b0c406304574b23bff794f182529b9e611e8537c7df4a75d5d`，本輪未改。
- u5ar 移除「兩大盤一小盤」暗示；b3gv 畫面包含上方 Games 及下方 Exeligmos 小盤。新增 rwa9，以同一次讀盤動作說明把小盤時數加到食象時刻。S10 原文 pp. 139、141–142 直接實讀，Callippic 小盤僅列研究假說，不說完整配置唯一確定。
- 新增 S9：2016 前蓋原論文 p. 291 金星 462 年／289 會合週期，p. 294 土星 442 年／427 會合週期。正文只念原有年數。刪片尾 n5uu／g5ga／w2sg 年代和作者旁枝，ams3 直接帶出天文方法如何接成傳動；改句／畫面見 `revision-1.json`。
- 修稿 SHA-256：`795ba47d4864702d6476b75653f27f0e4b09665d3d4d783c80c555498b3f5637`。93 景／95 句、87 插圖景，估 09:21（未合成）；schema／lint 0 error，2 個已說明的研究場景詞頻提示，Shorts 引用、主張表、開場同圖回收均通過。收據 `script-validation.json` 為作者機械驗證，不是獨立通過。
- 下一位獨立查核者接手本 scope 寫 `verify-1.md`，另需新十三題盲評。初輪結果曾退修，本輪作者不自判通過。尚未正式劇本送審或付費：paid calls = 0、worker starts = 0；每集 US$6／整批 US$30 授權仍有效，但不跳過劇本核准。此票保留 open 待覆核，不 done。

### 2026-10-16 正式稿獨立事實覆核第 1 輪

- `docs/videos/curio-m09/verify-1.md` 逐列檢查 204 個旁白、畫面文字／提示及上架文字項目；**事實 PASS** 綁定 `video.json` SHA-256 `795ba47d4864702d6476b75653f27f0e4b09665d3d4d783c80c555498b3f5637`，未留事實阻斷。2016 前／背盤原論文已實讀，先前背盤小盤配置和原論文缺鏈問題均已解決；30 殘存齒輪、69 模型齒輪、十九年／223 月及 2024 孔數均分清。
- 獨立 lint 0 error、2 個研究場景詞頻 warning。查核者未修改正式稿；此票仍 open，待協調者完成正式稿敘事／盲評收斂及站主劇本核准。
- 另一位未讀先前答案的 script-only 盲評者對修稿 SHA `795ba47d4864702d6476b75653f27f0e4b09665d3d4d783c80c555498b3f5637` 判 13 題全過，主代理匯入正規化答案後 `narrative` 工具 exit 0。`script --slug curio-m09` 生成稿 SHA `DB36B91ADE79E1B6AD06633889C4B42D07E45730D39518DB4E85F6F2C0F09C6F`；`review-push --gate script` 成功、`review-pull --gate script` 讀回 `waiting for the owner`。正式劇本已送後台，等站主核准；尚未啟動付費製作。
