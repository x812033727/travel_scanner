# 《偶的江湖》第一集：Claude 接手入口

交接日期：2026-10-09。使用者要求「我要找 claude 做，跟我講要怎麼跟他說然後你收尾停止」。Codex 已停止新增生成／API／付費，保存原任務，沒有取消已付費的海螺佇列。這不是完工或素材採用紀錄。

## 先讀這些，接著做實際製作

- 工作目錄：`C:/Users/x8120/.codex/worktrees/1b93/travel_scanㄐ`
- 分支：`codex/ou-de-jianghu-visual-preproduction-20261008`
- 任務：`tasks/open/2026-10-08-ou-de-jianghu-visual-handoff.md`。Codex 收尾 release 回 open，DoD 未勾完。
- 草稿 PR #1388：<https://github.com/x812033727/travel_scanner/pull/1388>。未合併／部署／發布。
- 先讀 AGENTS.md、`.agents/skills/animation-production/SKILL.md`；鏡頭備料讀 animation-camera，原預算與改稿規則讀 animation-preproduction，音軌剪接讀 youtube-video。不要重新從零規劃或重製已有素材。
- 本機媒體根目錄 E：`C:/Users/x8120/mokaair-work/videos/ou-de-jianghu-e001`
- P：`E/browser-production/20261009`
- F：`P/finish-episode`
- O：`F/throughput-resume-20261009`
- A：`F/assembly`

以上 E/P/F/O/A 是本文路徑縮寫；命令中須展開成絕對路徑。所有媒體在外部 E，不在 Git checkout，不要以 repo 沒 MP4 誤判素材遺失。

## 已經給過的授權與不能默改的決定

- 完整第一集〈幽皇之女〉：459 卡、420 個動態母鏡、597 句中文，約 23 分鐘；不是只做十幾秒小樣。不要用静圖或跳接掩蓋缺鏡。
- 146 張素材和 v4 已正式採用，保留華麗古裝、細緻 2D 人物。
- 使用 Hailuo 網頁／原已登入瀏覽器製作，既有點數；A 期上限 26,980.8 點含預留，B 期 21,753.6 需實際有額度。禁止購點／續訂。使用者曾自行儲值，並非代理購買。
- 各鏡原圖像與影片 take cap 保持；多數是各 2 次，執行前讀 authorization/actions，不能把 HOLD 當可無限重買。
- 使用者對十一鏡改案明確回答：**保留原方案，先做其他鏡頭**。a02-s014/016/019/026/028/029/034/040/042/049/052 變更不採用，不套用改中景、第三張或其他提案例外。依據 F/eleven-shot-decision-20261009-deferred.json，SHA `0ae4f2206fe9c4b2f60b4ddac67bf8261329f102ccdfff0d2f3dc06ba2b47585`。
- 原先 pilot 懸停變更及 10.75 秒節奏另已接受，勿混同此次十一鏡未採用變更。
- 中文配音 Google，聲音由助理選，未來多國語言；中文配音及重錄 API 總上限 US$3，已取代早期 API 0。使用既有後臺影片工具權杖／Smart IDE key，不新建憑證，不將金鑰印出或存交接文件。
- 沒有上傳 YouTube、公開發布、merge 或 deploy 授權。

## 停止時的實際狀態

O/progress-snapshot-20261009-current.json 是 2026-10-09T10:45:14.212977Z 的已核快照。後續沒有新付費，只有新 QA 收據；不要把歷史 notes 數字當現值。

- 139 圖像 actions；133 張已下載圖像 take，覆蓋 89 鏡。
- 68 影片 actions；61 支已下載 take，57 個不同動態母鏡。
- 全 take 視覺狀態按鏡最佳：32 候選、10 有限候選、15 HOLD。這些都不是全片／聲畫／owner 接受。
- 420 個母鏡尚 363 個沒有下載影片；另有 HOLD／有限候選需處理。
- 597/597 句錄音候選已存在（269 舊網頁、328 後臺），完整聽驗、表演、對嘴、整集對白剪接尚未完成。v4 預覽 19 卡只有 24 句不同對白，含重疊小樣，不能相加當全片長度。
- A 期已扣 6,679＋未知預留 70＝6,749 點，已含先前 15 actions／475 點一次。最後 UI 餘額 **55,321**。本機操作批次 ceiling 7,600 是內部保護，非新 owner 總上限。
- API 返回音檔估值 US$0.2161915＋舊 a7mv 未知預留 US$0.147658＝US$0.3638495；不是供應商帳單。這轮沒有新 API 呼叫。
- **a02-s086-video-t1 沒有送出、沒有 action、沒有扣 60 點**。最後曾準備該表單，上傳停留 blob，守衛在 intent 前拒絕；輸入框後來混入人工輸入文字，不能直接按建立。重新按原 canonical 準備並驗證後才可提交。

## 已付費未下載：先回收同一個原任務，禁止重送

停止時 F/actions status 為 generating；請用現有 provider_group_id 查最新結果。最後可見新影片排隊估計約 44 分鐘，不保證交接後仍相同。

| action | 類型 | 已扣 | provider_group_id |
| --- | --- | ---: | --- |
| a02-s075-start-t2 | image | 22 | 564914734458408969 |
| a02-s090-start-t2 | image | 22 | 564914989748920323 |
| a02-s091-start-t2 | image | 22 | 564914493994713097 |
| a02-s080-video-t1 | video | 48 | 564915588666126339 |
| a02-s087-video-t1 | video | 48 | 564915724544782342 |
| a01-s046-video-t1 | video | 48 | 564915874780577793 |
| a01-s049-video-t1 | video | 48 | 564916031555268614 |
| a01-s053-video-t1 | video | 48 | 564916187709198337 |
| a01-s055-video-t1 | video | 48 | 564916363408572418 |

這 9 項共 354 點已含在上面的 A 期 6,679 點，不能再加一次。保留原付費任務，下載官方無水印檔並寫 SHA 和 provider asset id；下載失敗不等於生成失敗。

三筆仍未知、保留 70 點：a01-s082-start-t1 22、a02-s030-start-t1 24、a02-s033-start-t1 24。不要盲重試，也不要因沒有在目前頁面看到就推定退款。另 a01-s047-video-t1 是已有證據的 provider_rejected_refunded，與 unknown 不同。

## 接手後優先順序

1. 核讀本檔、STOP、lease、task 與原帳本。使用者把本檔交給你並要求接手時，才恢復製作；可保存／歸檔此次 Codex STOP 紀錄，再 claim task、取得你自己的新 lease。不能沿用已退出的 Codex PID 35956。原 source／budget/take guards 必須保持。
2. 回收上表 9 個原結果並實看。075、090 第二張的皇冠留白數值只是修復目標，不能另造硬性像素門檻；091 背面沈的左手應是畫面左側托匣、右手畫面右側持閉扇。三張 t2 尚未 QA。
3. 可直接往影片推進的現有首格：a02-s086 t2（5 秒／當時 60 點）；a01-s045 t1（5 秒）、a01-s064 t1（4 秒）。先查最新 actions 避免接手後重複，實價以畫面為準。所有原 prompt／片長在 after12/next12 packets。
4. a01-s048 與 a02-s092 原鏡 t2 備料完成但未送：O/repairs-a01-048-a02-092-t2.json，SHA `3a5a3d9e95357e3f6a3c08b3366fddca8395290312f65cc2975eb52baaad2bc2`；各 2 refs，仍是原鏡位／4 秒。048 原 t1 已在平地且全身，不能承接階中下行；092 頂尖貼邊，先留第二張修正空間。
5. 新增原首格 HOLD：a01-s056 裁鳳冠；a01-s061 雙靴站在階前廣場而非最底階；a01-s063 缺沿前鏡應在右肩的彎刀。QA 已存 O/qa/first-frame-review-a01-sNNN-t1.json。這三張第二次修復尚未備，勿當候選直接付影片。
6. 依原 A 期順序批製其他鏡；原來兩次額度已用完者保留 HOLD，包括 a02-s077/082 首格，a02-s048/050 影片等，查帳本不要猜。不要反覆重做完整總稽核拖延實際製作。
7. 完成候選逐鏡 QA、完整台詞與 pause 的剪接、獨立 D/M/A/F、整集連戲及聽看覆核。靜圖合格不等於影片合格、ASR/可播不等於實聽合格。最後才輸出完整第一集與缺陷／預算報告。

## 重要來源與工具

- P/continuation-plan/video.json SHA `f682f43043109a564b5ff2cc69b1764930017b35616a58d12460b7ea6b2e1257`
- P/continuation-plan/plan/lock.json SHA `bb20a61b95383e45a814d4881633e5e8082d200939cce434e50d2bd4def6d313`
- F/throughput-next12-20261009/packet.json：a02 070/075/076/077/078/080/082/085/086/087/088/090；SHA `512a6d8365d64ff981d35b6af38463cf71f3ab7f5dfbd8616a415d60f95368fd`
- F/throughput-after12-20261009/packet.json：a02 091/092 和 a01 045/046/048/049/053/055/056/061/063/064；SHA `502133f0e07428e3a379111889a8cca940bbd90ca3f2a292c08a43e7a9e89094`
- 帳本：F/actions/*.json；另有 E/browser-pilot/20261009/actions 和 P/actions 的原 15 actions，統計時合併、去重。
- F/action-ledger-resume.mjs、F/authorization-resume.json 為現行本機守衛，不是provider API。auth 現版 SHA `02858b411f7c271a602fce9a84f8d5604ce5a63005c4b7637e76a17f7e294882`；需新 lease PID 才能恢復。F/authorization.json 是較早版本，不要誤用。改 JSON 用 Node JSON，PowerShell ConvertFrom-Json 可能把 ISO 日期轉換後破壞 baseline hash。
- O/cua-helper-definitions.js 只是已觀察 UI 的 helper 定義，不是獨立背景製作器。新環境先讀自己瀏覽器工具文件／重新取得頁面狀態，勿照舊 element id 或座標直接點。
- Hailuo 頁面 <https://hailuoai.video/zh-Hant/create/image-to-video>，IAB browser 2/tab9。新工具未必共用這些 ID 或登入狀態。
- 最新停止 UI 原文、可見 groups、截圖：O/claude-handoff-ui-readback.json、O/claude-handoff-ui.png。
- O/qa 為逐圖／片 source-bound 收據。舊歷史收據都保留。
- 中文語音、token流程、最初採用與資產映射等入口：本 handoff 目錄原有 EP1-production-progress-20261009.md、google-api-adoption-20261009.md、asset-manifest.json、adoption-decision-20261009.md。這些文件較舊的進度數字以本檔及 action帳本為準。
- 可用 bundled Node：`C:/Users/x8120/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node.exe`。

## 可直接看的既有候選與分軌

最新 v4 本機預覽：<http://127.0.0.1:8784/finish-episode/assembly/throughput-resume-20261009/local-preview-v4-20261009/preview.html>。19 卡含 055、061t2、068、076、088 有限前段及 15.208 秒 D/M/A/F 小樣。部分重疊，不是 19 個完整成片段。根據原檔的精確白名單服務，只綁本機；伺服器 PID 22284 保留給接手者。原頁、舊版本與所有素材均未刪除。

分軌混音候選 A/pilot-through-038-MAF-premix-v1/ 含獨立 D/M/A/F、ME、premix 與 REAPER 工程。M 是既有 CC0 DarkIntro 候選，曲風尚未採用；沒有把它說成正式武俠配樂。

O/next-D-055-backend-v1、next-D-061-t2-expanded-head-provisional-v1、next-D-068-expanded-head-provisional-v1、next-D-076-expanded-head-provisional-v1、next-D-088-limited-prefix-v1 為最新五段 D。原台詞/pause不縮、畫面不變速；088 前段另編碼，不能宣稱壓縮封包完全一致。075 舊影片全 take HOLD，不能因配音已備就直接接上；076 冠尖貼邊；088 全 take HOLD 保留。

## 停止與持有權

E/STOP 已寫 owner 的停止／轉交決定，SHA `17718bbcbc43d89c3b7d04b9d35e17e9e90a6ac62270fd169ac62da46c3f4e60`。Codex lease guard 已回報 lease_released，exit 0；不會背景繼續下單。既有海螺遠端任務可能自行生成完成，這不表示 Codex 還在操作。唯讀本機預覽服務保留。

交接沒有 commit/push/merge/deploy。保留本機既有 `.codex/environments/` 未追蹤檔，不要當成本次垃圾清除。精確停止驗證見 O/claude-stop-receipt.json。
