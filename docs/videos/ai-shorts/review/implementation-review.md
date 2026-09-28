# Shorts 實作查核

Reviewer: independent Codex review
日期：2026-09-28
方法：唯讀程式審查、既有 Node 測試與 CLI 錯誤路徑檢查。父代理持續修改中；各輪行號與結論分別綁定該輪審查快照。審查者曾參與 structured 實驗輸出，但未撰寫這四個程式檔。

審查範圍：`tools/video/shorts/core.mjs`、`build.mjs`、`cli.mjs`、`core.test.mjs`；另唯讀追蹤既有 paths、WAV 與 speech helper。未改程式、未改封存實驗、未執行完整影片 build、未呼叫付費 API 或發布。此檔為本輪唯一新增文件。

## 修正複查：四個原 P2 已閉環

複查日期：2026-09-28。以下是最新狀態；後面的首輪發現保留作為歷史紀錄，不代表仍未修正。

| 原發現 | 複查結果 | 最新實作位置與證據 |
| --- | --- | --- |
| 重建失敗留下舊成功收據 | 已修正 | `build.mjs:178–182` 在 buildId 後加每次嘗試的時間戳，循序重建使用不同目錄；失敗嘗試不再覆寫前次成功包。已查程式路徑，未刻意中斷一次完整 build。 |
| hash 驗證後重新讀來源 | 已修正 | `core.mjs:39–45` 回傳驗證過的 bytes；renderer 的字型字集、HTML 與圖片都讀取同一快照。`build.mjs:176–177` 將外部 WAV 一次讀成 externalAudio，這批 bytes 同時用於 audioHash，並由 `138–156` 寫入本次目錄後供 ffmpeg 使用。 |
| HTML 素材自身裁切／缺圖未檢查 | 已修正原回歸情境 | `build.mjs:86–106` 在截圖前檢查文字 Range 相對於 viewport 與所有具有 overflow 裁切的祖先範圍，也檢查圖片載入。以最新 callback 在 Edge 實測，超出 viewport、祖先裁切和缺圖均遭拒絕。 |
| NaN 繞過音訊 duration 檢查 | 已修正 | `build.mjs:207` 明確要求有限 duration。直接執行最新 profile 判斷式：undefined、`N/A`、Infinity 與超過容差的時長均失敗，有效且在容差內才通過。 |

第一次複查讀到的過渡版還沒有外部 WAV 快照與祖先裁切檢查；已向父代理回報，再重新讀取其後補上的版本並重新測試。下列結果使用的是最後一版程式，沒有沿用過渡版 callback。

### 最新回歸結果

從磁碟重新讀取 `build.mjs`，取得 SHA-256 `47b11e00042a9d3a473fc1ce648c863003bf8c3f1007cdd99551b1f3b8ada083`，直接抽取其 assetProblems callback，放到唯讀、無外連的 800×1000 Edge 頁面執行。沒有修改來源或另存測試 HTML。

| DOM 案例 | 最新結果 |
| --- | --- |
| 正常且位於畫布內的文字 | `[]`，通過 |
| 文字位於畫布下方 | `text clipped: REQUIRED POSTER TITLE`，拒絕 |
| 父框 `[100,100,300,120]`、文字框約 `[100,100,449.734,140]`，父框 overflow:hidden | `ancestor clips text: REQUIRED POSTER TITLE`，拒絕 |
| 無法解碼的圖片 | `asset image failed`，拒絕 |

同一份最新來源的 encoded-output 判斷式也經直接執行；timeline 為 30 秒，其他 profile 欄位有效：

| audio.duration | 結果 |
| --- | --- |
| undefined | 拒絕 |
| `N/A` | 拒絕 |
| Infinity | 拒絕 |
| `30.01` | 通過 |
| `30.2` | 拒絕 |

`core.test.mjs` 再跑仍為 5/5、exit 0；修改過的 core、build 與 cli 語法檢查通過。上述 DOM 與 duration 回歸腳本皆有 assertion，失敗會非零退出。本輪未再跑已無相關邏輯修改的 CLI 錯誤路徑矩陣。

字型處理已改為在初次 setContent 解析前插入本機 font CSS，並為字型就緒加入 20 秒期限，取代原先 addStyleTag 路徑。父代理另回報兩支成片已輸出且音量 gate 通過；本審查沒有獨立重跑整支影片、播放聽審或檢查那些成片的 checks.json，因此不把該回報寫成自己的端到端驗證。四項程式缺陷閉環也不等同於已發布或成片人工驗收完成。

### 複查快照

| 檔案 | SHA-256 |
| --- | --- |
| `core.mjs` | `4d7ce09feb80801a096aed8d2f414d22c452d1392b65a4d90d5656ff2c8205d1` |
| `build.mjs` | `47b11e00042a9d3a473fc1ce648c863003bf8c3f1007cdd99551b1f3b8ada083` |
| `cli.mjs` | `c9dd4b882744f181e9b09a432ffc325d5bf676e0b9a68538ffd914fd0f661ee8` |
| `core.test.mjs` | `29ddc94694c37e7a790defcbc67a0157206c61467726875723bad90b8e9c3475` |

## 首輪發現與建議（已修正，保留歷史）

### P2：重建失敗會留下舊成功收據與已覆寫的產物

位置：`build.mjs:140–143`、`160–178`。

相同輸入的 buildId 固定，程式直接重用同一個目錄。`ffmpeg -y` 會覆寫 `upload/final.mp4`，但既有 `checks.json` 與 `upload/manifest.json` 直到所有後段檢查通過後才更新，也沒有在重建開始時失效。已成功建置後重跑，若編碼中斷、ffprobe 檢查或 loudness 檢查失敗，就會留下舊 `ok:true` 收據和舊 manifest，旁邊卻是新影片或不完整影片。manifest 中的輸出 hash 可供人工發現問題，但現行 CLI 沒有在交接前自動驗證現存整包。

建議：在獨立 staging 目錄完成整次 build、檢查與 manifest；全部成功後才切換交付目錄。若暫時沿用原目錄，至少在首次覆寫前移除成功標記並寫入 building／failed 狀態，失敗時不得保留可被當作這次成功的收據。

應補的回歸測試：已有成功包時，讓第二次執行在產生 final.mp4 後失敗；舊包仍應完整可驗證，或該目錄應明確是 failed，不能是混合狀態。

### P2：驗證 hash 後重新讀取來源，未固定實際使用的 bytes

位置：`core.mjs:39–44`；`build.mjs:62–76`、`136`。

`verifyEvidence()` 讀檔比對 hash 後只回傳檔案路徑。經過語音準備後，renderer 又重新讀 HTML／圖片。若這段期間來源被編輯，影片會使用新 bytes，但 manifest 仍記錄先前通過的舊 hash 與 `evidence_verified:true`。這在同一工作區有人持續修改素材時即可發生，無須惡意輸入。外部 audioDir 也在計算 audioHash 後，再於 speech 階段重新讀取。

建議：驗證時保存 bytes snapshot，渲染與外部音訊轉換都只使用該快照；或先將輸入複製到此次 staging 中，對複本驗 hash，再固定使用複本。只在末尾再驗來源仍無法完全排除「改過又改回」的時間窗。

應補的回歸測試：驗證後、渲染前替換來源；輸出須使用原快照，或拒絕繼續，不能保留舊 hash 而使用新內容。

### P2：HTML 素材截圖前未檢查其自身裁切或載入失敗

位置：`build.mjs:64–80`；對比 `36–50` 與 `86–90`。

HTML asset 被放到 800×1000 viewport 後立即截成 PNG。這一步沒有檢查來源 HTML 的內容邊界、overflow 或 image failed；`measurePage()` 只在外層短片字卡上執行。若來源必要文字位於 1000px 以下，或 HTML 自己設了裁切，PNG 已遺失文字，外層仍可通過「圖片載入成功且在 safe area 內」。因此現行 layout gate 能檢查短片字卡，但不能證明原海報完整。

建議：在截取每個 HTML asset 前檢查其正文文字與指定圖形的實際 bounding boxes、載入狀態和預期 viewport；將 asset 檢查結果寫入 checks。對有 overflow:hidden 的容器不能只看頁面的 scrollHeight，還要查必要文字的範圍。素材來源不合規時應中止或明確要求人工處理。

應補的回歸測試：必要文字放在畫布下緣之外、被父容器 clip，以及缺圖三種素材；這些案例不得取得全通過的素材檢查結果。此處指出的是 gate 的缺口，未宣稱目前兩張封存海報已被裁切。

### P2：缺少音訊 duration 時，NaN 會繞過時長檢查

位置：`build.mjs:165`。

目前使用 `Math.abs(Number(audio.duration) - timeline.seconds) > .08` 判定失敗。若 ffprobe 的 duration 缺失或回傳 `N/A`，Number 得到 NaN，而比較結果為 false，該項檢查會被當成通過。影片 frame 數有檢查，但音訊時長在這個分支其實沒有得到有效量測。

建議：先把 duration 轉成數值，要求 `Number.isFinite(duration)` 且為正數，再做容差比較。若改用其他 ffprobe 欄位，應明確記錄使用哪個欄位，不能把缺值當成成功。

應補的回歸測試：duration 為 undefined、`N/A` 與 Infinity 時失敗；有限且在容差內才成功。這是以 JavaScript 比較語義確認的分支缺陷，本輪未刻意產生缺少 duration 的完整 MP4。

## 首輪已確認的行為（歷史）

| 重點 | 結果與限制 |
| --- | --- |
| 證據來源路徑 | `sourcePath()` 要求相對路徑，再以 realpath 與 containment 判定；現有 traversal 測試通過。程式有處理 canonical path，但本輪未新增 symlink fixture。 |
| 產物路徑 | 採用既有 `resolveWorkBase()` 拒絕一般位於 repo 內的 workdir；其檢查為詞法路徑判定，未在本輪驗證 junction 或 symlink 輸出目錄。 |
| 語音／字幕基準 | 使用轉成 48 kHz mono PCM 後的 sample 數決定時長，30 fps 的 frame 對應 1600 samples；字幕與畫面由同一 timeline 產生，每句加至少 0.18 秒空白。現有時間軸測試通過。 |
| 音訊內容正確性 | 程式檢查格式、非靜音、時長與 loudness；沒有自動證明 WAV 的每一句確實念對稿子。上架說明要求站主聽審，因此本輪未將此誤稱成已驗證的發音或轉錄。 |
| 短片外層 safe area | 對正文／字幕容器 overflow、正文子元素水平與下緣、字幕下緣及圖片載入有 gate。實際手機介面遮擋仍須成片檢視，本輪未宣稱已通過。 |
| 發布狀態 | manifest 為 `owner-review-required`；UPLOAD.md 明載尚未上傳、發布或排程。未發現把未經真人審核的試片標成發布完成。`checks.ok` 是技術檢查結果。 |
| CLI 退出碼 | 本輪測到的正常分支為 0，錯誤分支為 1，未見錯誤被吞成成功。未執行 build／track-init 的寫入分支。 |

## 首輪實際執行（歷史）

- `node --test tools/video/shorts/core.test.mjs`：5 tests，5 pass，exit 0。
- 四個範圍檔案各自 `node --check`：全數 exit 0。
- CLI `--help`：exit 0。
- CLI `validate --file docs/videos/ai-shorts/pilots/shorts-receipt-total.json`：exit 0，schema and source hashes OK。
- CLI 缺 `--file`、未知命令、未知旗標與不存在的 script 檔：各 exit 1。

現有五個測試覆蓋 schema／實驗 hash、基本路徑逸出、sample 時間軸、HTML escaping 與答案鍵。它們沒有覆蓋上述四個失敗情境，通過不代表這四項已排除。未做完整渲染、編碼、播放或真人聽審。

## 首輪審查快照（歷史）

讀取後與本輪 Node 檢查期間取得的 SHA-256 相同；父代理後續修改須另行確認。

| 檔案 | SHA-256 |
| --- | --- |
| `core.mjs` | `c0e218add362abbde82b38373efc24e811e5da4a3fd753dcc70414785206f137` |
| `build.mjs` | `d58eca2f3d8ed78c82b101c873a63c6aab4544bff703d2f395163e7700216cca` |
| `cli.mjs` | `50db977b349e94c870d996c6dcfef36139ab2b30666376e7fa9470503092a573` |
| `core.test.mjs` | `29ddc94694c37e7a790defcbc67a0157206c61467726875723bad90b8e9c3475` |
