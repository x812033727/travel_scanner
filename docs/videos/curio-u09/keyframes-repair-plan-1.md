# U09 插畫定向修復收據 1

2026-10-16 05:55 UTC，只準備提示詞，尚未呼叫付費產圖或評審，也未送分鏡審核。

## 範圍與固定內容

- 本輪只改 `video.json` 中 13 個 `shot.data.prompt`。鏡頭順序、旁白、字幕、`look: {"preset":"cute-mystery"}` 均未改。
- `video.json` SHA-256：`5C98A3BF3DBB32699EC63321E8C5185E01828045A64911175D7BC5F317F1D8BE` → `66308948D11533F639C61054471F11C7671B55EE7F93966E54557F35C4C0CE8A`。
- 已核准的 `script.md` SHA-256 仍為 `A6EBACD14E9986B8422316ABAEC6178FF039D063F31FE33A1A01D14233AF3F5A`；音訊時間軸未動。現有 script、audio 核准分別綁定 `script.md` 與 `timeline.json`，本輪未要求新核准。
- 開始前的外部 `keyframes/manifest.json` SHA-256 為 `2C573FC9CA241955C3E02D976BE8EAF5DA9645E6494AA6ADA93BEC4203103CC8`；`media/ledger.json` SHA-256 為 `DC70BC992A426759B456132832FAA00500647BC92E690F232EBA103F28BE3563`。快照有 91 鏡：62 已通過、5 保留、24 未選圖。`another-pulse` 曾產生一張圖，但 HTTP 502 發生在該張評審前，因此仍列未選圖。

## 已通過但畫面與旁白牴觸：改提示詞的 8 鏡

| 鏡頭 ID | 舊圖問題 | 新提示詞要呈現的內容 |
| --- | --- | --- |
| `august-desk` | 博士生攤紙帶畫成小男孩；鏡頭也缺紀錄器。 | 成年人的手在 1967 年觀測桌攤開帶墨跡的長紙帶，紀錄器在後。 |
| `original-survey` | 1960 年代原始觀測陣列畫成現代城市基地台。 | 開闊場地的低木柱與水平線狀天線。 |
| `human-reading` | 人工檢視紙帶畫成分類彩色卡。 | 成年人的手攤開數條帶細墨線的窄紙帶。 |
| `early-arrival` | 舊觀測紙帶畫成現代儀表板圖表。 | 桌燈下比對同一卷的窄紙帶與局部墨跡。 |
| `own-machine` | 檢查設備畫成插頭斷裂、冒電火花，暗示已確認故障。 | 完整接頭插在接收器上，手正檢查連接。 |
| `dense-record` | 紙面幾乎空白，未見旁白所說擠在一起的變化。 | 長窄紙帶中心有密集細小墨跡，指尖指向該處。 |
| `christmas-holiday` | 不自然的人物從手臂伸出；彩色展開圖未呈現留下紙帶的動作。 | 一隻成年人的手把緊捲的紙帶放在桌上、筆記本旁。 |
| `before-locking` | 趕在關門前翻舊紀錄畫成小孩打開空白筆記本。 | 成年研究人員從舊紙卷堆抽出窄記錄紙。 |

以上保留的舊檔只作失敗證據，不能因先前評審 `passed=true` 就沿用為本輪定稿。人物採匿名成年手或裁去臉部的剪影，不畫仍在世人物的可辨認肖像。

## 原已保留：改提示詞的 5 鏡

| 鏡頭 ID | 三次舊圖的主要問題 | 新提示詞的簡化方向 |
| --- | --- | --- |
| `pen-runs` | 小人取代紀錄器金屬筆尖，曾出現字樣。 | 方盒紀錄器、紙卷、金屬筆尖和一道墨線。 |
| `missed-session` | 設備被畫成人形／吸塵器，另有浮水印與上下黑邊。 | 空椅、方盒紀錄器、桌上長紙帶與門。 |
| `name-not-result` | 空桌添了小人頭，另有上下黑邊。 | 背面空白的紙標籤，旁邊一條有脈衝記號的窄紙帶。 |
| `test-consequence` | 多顆星球珠和照片／3D 質感。 | 匿名成人在黑板畫一個中央點、一個環上小點和單一軌道。 |
| `brief-window` | 控制面板反覆變成照片／3D，並冒文字和人物頭。 | 成人手扳起方盒接收器的開關，上方一個無字指針表。 |

提示詞只描述畫面動作和物件，系列畫風仍由既有 `look` 套用。沒有改卡片、增加鏡頭或將插畫當史料重建。

## 後續付費批次的界線

- 只處理上述 13 鏡及仍缺圖的 24 鏡，共 37 鏡。現有其他 54 張已選圖維持快取；重跑時應以明確鏡頭 ID 限定範圍，並逐鏡核對最後選圖。
- 缺圖 ID：`another-pulse`、`same-frequency-argument`、`after-holiday`、`more-marks`、`observations-public`、`observed-versus-model`、`source-small`、`oscillation-meaning`、`unfinished-model`、`end-observation`、`public-boundary`、`motion-problem`、`new-manuscript`、`may-beacon`、`rotation-proposal`、`lighthouse`、`line-of-sight`、`beam-away`、`period-origin`、`testable-prediction`、`later-support`、`emission-open`、`archive-answer`、`comment-question`。
- 每鏡最多三次 MiniMax image-01 產圖與 Gemini 評審，以每次 US$0.0135 計，最多 `37 × 3 × 0.0135 = US$1.4985`。共享帳本已為本輪保留這筆估算；本收據未改帳本。
- 付費前帳本中的 U09 已用估算為 US$3.012／6；若用滿本輪上限，圖片完成後約 US$4.5105，另留一次約 US$0.05 最終 QA，仍低於單集 US$6。這些是工具估算，非供應商最終帳單。
- `node tools/video/cli.mjs lint --slug curio-u09`：0 errors、0 warnings；`git diff --check`：通過。實際產圖後須重新對照畫面與旁白、更新媒體帳本，確認 91／91 鏡通過後才送分鏡審核。
