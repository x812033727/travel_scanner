# 2026-10-03 接手與 VPS 唯讀預檢

於台北時間 2026-10-03 01:32 核對 PR #1135 的
`117a867ac57634c8e01e6f513abc48a4bcffd294`。該版 10 項 CI 全過，PR 仍為草稿。
本次已由 Windows 接手，沿用原 PR 分支；SSH 可用，先前缺少主機連線的障礙已排除。
**仍未送出圖片／片段／配樂請求，未核准任何文件，未改全域設定或重建服務。**

本紀錄是上述時間的快照；後續執行前須重讀最新版本和核准，不可把它當成批准或供應商試拍成功。

## 已核對的主機條件

- VPS checkout 為 `acb935fb461e34ee110b725b742179cc22d67770`；未部署 PR #1135。
- 根磁碟可用約 105 GB，未見部署 hold；這不是完整部署預檢或部署授權。
- 現有 API、PostgreSQL、Redis 和 video worker 容器運行中；本次没有啟動或重啟它們。
- 真實資料庫 `drama_enabled=false`、`series_script_gate=true`、`music_enabled=true`。
  Global clip 仍為 `gemini-omni-1.1-flash`，圖片為 `gemini-3-pro-image`、音樂為 `lyria-3.5`。
  繼續用隔離 runner 固定 Lite，不切換全域模型或開關。
- 有有效 Gemini key，僅核對存在性，未輸出內容；現有管理員有效且具有所需內容／設定能力。
- API image 的 `video_media/jobs.py`、`meter.py`、`schemas.py`、`catalog.py` 與
  `video_reviews/admin_service.py` 的實檔 SHA 全部等於此 PR head 的 Git blobs。
  此比對不證明 provider 地域可用、實際影像規格或 PostgreSQL campaign lock 已驗證。
- 兩個 production slug 的 `VideoMediaJob` 共 0 筆；scoped runner 的 reservation/result audit 共 0 筆。

## 真實待審項目

原作品 `wedding-reckoning` 仍為 **setting**，並非 runner 要求的 active。
系列 `image_model` override 為 null。最新三份原作品文件均為 v3、status=review、decided_at=null：

| 文件 | 真實 ID | canonical body SHA-256 |
| --- | --- | --- |
| setting 0 | `9d133427-503f-45d9-8326-5249ee76ce20` | `07559d4f445a465ea357ae095e6f41f794c9f3e0fb1138104708d599017c7488` |
| outline 0 | `455497ab-6fac-4a3f-ae21-c970be3d1565` | `cb7c379f2dd202ee729c7f0874678eb959f0431ca28515618b8157f546c39ed3` |
| chapter 1 | `249e2729-03e7-4633-b2b0-651cf8e22c0d` | `a85f93948078e336c8785423bcef5f59dfe61778d45645ef4c885cd8b54930c5` |

Setting 的 source binding 為
`37328fa1c643e0edfcd1d138a158410653b36d6e02739ce7a9c555b26bc5bb9c`，與交接一致。
由站主在[原作品後台](https://mokaair.com/zh-TW/admin/videos?tab=drama&series=wedding-reckoning)
審閱並依正常流程核准文件；不直接改資料庫 status。

| 劇本 | 真實 review ID | 即時狀態 |
| --- | --- | --- |
| [E1](https://mokaair.com/zh-TW/admin/videos?video=wedding-reckoning-competition-e01) | `b909e8f3-0cfd-4488-b323-1d81dbaa0dce` | pending、decided_at=null |
| [E2](https://mokaair.com/zh-TW/admin/videos?video=wedding-reckoning-competition-e02) | `e0c54172-1349-40fa-b29f-0da3422e84cb` | pending、decided_at=null |

兩集 project 的 format、series_slug、episode_number 正確，均未 dropped。
劇本 content hash 與本版 screenplay bytes 相符；尚無 look／storyboard review。

## 本機素材與離線驗證

- `handoff.json` 的 10 份 source_files、49 份 package_files 全部符合 Git blob 和工作樹原始 bytes，
  沒有換行造成的 hash 差異；draft manifest 的 source/script/edit 5 項也相符。
- 15 項 required_input_files 全在。兩集 measured edit 與 timing report 綁定相同的 source/script。
- E1 33 句／40 窗口／10 個無聲窗口／144.86 秒；E2 34／41／7／159.05 秒。
  這些是已有文字收據的核對，不代表本機重聽過音檔。
- 已從固定 Git commit 匯出不經文字重編碼的 source bundle，並匯出 runner schema，保存在 repo 外。
  來源 zip SHA：`487795e93fe855e3a3e66b075a5b89a42b1117690dbd5fc6e9028f349e032c24`。
- **原 `/workspace/mokaair-work/.../transfer/wedding-reckoning-e01-e02-media.tar.gz` 及其
  `.sha256` 尚未移到此 Windows 環境。** 本機常用素材／下載目錄與 VPS `/root` 搜尋未找到該包。
  因而本次不能重驗包內 146 檔，也未重錄任何一句。需從原執行環境取回原包和 checksum。
- E1 L022／L026、E2 L002／L016 仍是 human-review-pending；ASR 字形差異不構成重錄理由。
  `episode-01-validation.json` 的 22 句未錄欄位是歷史快照，現況以其 current_section 和本輪實測紀錄為準。

## 接手時補上的模型防護

離線重現了系列 `image_model` 在 reservation 後、底層服務最後選模型之前改動的競態。
原 runner 只在 prepare 核對 override，服務再次讀取時可能選到另一個模型。
本次在隔離 runner 的 `ScopedSession` 攔截該次最終 SELECT；讀到非已審 Pro 模型時，
在供應商呼叫前拒絕，保留 durable reservation，不建立 job、不扣 media meter，也不自動重試。
沒有修改 shared media service，亦沒有在正式站製造競態或呼叫供應商。

修正後 runner **44 tests 通過**（exit 0）；Ruff、mypy（兩個 Python 檔）和 diff whitespace
檢查通過，另有獨立程式覆核。原音訊 builder **19 tests 通過**。
Runner raw SHA：`fd98588d18123ef96f5acbe95cbea60ea0e42c0a65ba5c3722bf7d0f17d83844`。
GitHub 新 head 的 CI 應另查，不能沿用原 `117a867ac` 的 10 綠燈。

固定 SHA 匯出的來源 zip 是原 `117a867ac` 的保存副本，**不含此後續修正**。
正式執行需從修正後 PR head 重新匯出 runner，不能直接使用上述舊 zip 中的程式。

## 下一次執行

1. 取回原 media tar.gz 和 checksum，驗整包及包內原 WAV／cache／收據；沿用原有 67 句與既有補錄版本。
2. 站主完成上述文件及兩集劇本的正常後台核准；重新核對 active 狀態、最新 IDs、bytes 和決策時間。
3. 依 [scoped-production-runbook.md](scoped-production-runbook.md) 建逐階段 manifest：
   角色設定圖 → 真實選圖 → 首鏡 keyframe → storyboard 核准。
4. 首鏡固定 `wr-e01-s01`；存下 read-only preview 的 digest，才送一個 Lite 1080p／8 秒 pilot request。
   `--first-shot` 不代替 shot_id 或人工畫質驗收。未知／失敗請求不得換 ID 自動重送。
5. 首鏡與代表 pilot 驗收後才進後續 E1／E2。外語與正式發布仍不在這次執行範圍。

原文件／劇本未核准時，沒有有效的可執行 manifest。不得移除 draft 標記、假造 approved
或先生成後補核准。此預檢也未取代角色、聲音、道具、動作、CC 或成片验收。
