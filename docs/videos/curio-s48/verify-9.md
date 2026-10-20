# S48 R8｜新敘事盲讀 FAIL 後的作者限縮修訂

2026-10-20 UTC。R7 的兩位全新隔離讀者各自讀了精確 `script.md` SHA-256 `dcb1e33de833cd2d7d39119ac6bb12c272869bb8b56dfdb5edfebd2eca71f161`：A 12/13、B 11/13，兩人都把必答 `no_recap` 判 No；B 另把必答 `payoffs` 判 No。原始答案及具體引句留在 [A](review/r7-fresh-panel-a.md)、[B](review/r7-fresh-panel-b.md)，按固定規則的 [R7 正式合併](review/r7-official-panel.md)為 **敘事 FAIL**。以下只是作者對該 FAIL 的候選修訂，**不是 R8 的獨立史料、書面畫面或雙盲 PASS**。

| ID | R7 問題與 R8 修訂 | 固定史料界線 |
| --- | --- | --- |
| `atl024` | 原稿問碎片是自己卡進去或有人放，來源無法二選一。現在先說當時無法判定，再問第二截若出現，船上會怎麼應對；`atl033` 以部分船員懷疑破壞及調離當班工人回收。 | Russell R2970–3110 的首段碎片及 R3440–3655 的第二次發現與船上處置。疑心不等於查定有人動手。 |
| `atl035` | 把預先說出的「一千海里」改為「下一次故障時，船尾已放出多長的線？」；`atl041` 首次給出保守下限「超過一千海里」及九點五十八分切線動作。 | Russell R3302–3303、R3768–3774；原文 `1,186 miles` 此處未明定英里種類，研究 P07 的保守換算界線未變。 |
| `atl038` | 不再重念開場已說的八月二日；「開頭那場船首回收」明接 `atl001` 的場景，新增光點異常導致回收的因果，回答 `atl037` 的懸念。 | Russell R3680–3815 記清晨光點異常、決定回收及船首拉線；不預告 `atl045` 的斷落結果。 |
| `atl058` | 明說前兩截鐵絲不能證明有人動手；`atl057` 剛提供的船上脆線觀察讓意外損傷較可信，但兩截各自怎麼刺進去仍無定論，回收 `atl032`。 | Russell R3680–3760、R4090–4106。脆線來自船上儲放線圈，不是海底抓鉤樣本，也不能替各破口作逐件鑑定。 |

只改 `video.json` 的上述四個 `lines[0].text`、兩條明示伏筆（`atl024→atl033`、`atl032→atl058`）、`claims.md` 同 ID 口播與過期的 R5 狀態首段，再以 `script --slug curio-s48` 重生 `script.md`。R7 的其他 98 句、99 個 `shot` 提示詞、景序、畫風、聲線、`brief.md`、`research.md` 都未改；`loops` 21→23。未呼叫 TTS、音檢、政策、站台、插圖、配樂或組片。

| R8 精確輸入 | SHA-256 |
| --- | --- |
| `brief.md` | `7b4bc4b3f6970ac20ef9c2b9269d8a17cafacc87f2ccaf076806772b2e56ca8a` |
| `research.md` | `3d769826eff0fbfb939b35506e9eafb4166868a6c0709cb4bf234af4922dd19f` |
| `video.json` | `80523d0535eddb8d4d5b34809c58446b2d3133eeaf2bec2b1c6b6d73c2c07f39` |
| `script.md` | `52d9f1e7b3fce7805f928e72754481e79836cf35fde5aa9098929f88086e29b1` |
| `claims.md` | `4e4091edf2864daa7b5f67f932deee3ec57566cc6d756e7522e0cd68c036eaca` |

固定 Russell 原始全文 `/tmp/s48-russell-atlantic-telegraph.txt` SHA-256 `558efcc342df669e7387ffff818c104690e7ec910de49e795f996abf147ea750`；Field `/tmp/s48-field-atlantic-telegraph.txt` SHA-256 `bee659b24ace56a5e1f7104a6a306e9325ccd9c864fc373ad35b0863c5a8c675`。可重開版本及行段在 [research.md](research.md)。

## 本地一致性與時間

`video.json` 有 99 個正文 `shot`、三句片尾，**102/102** 句 ID 唯一；`claims.md` 102 列按 ID、順序、字面相同，重生 `script.md` 的 99 句正文亦逐字相同。相對 Git 的 R7，只有上述四個口播字串和兩條伏筆改變；99 個 `data.prompt` 全部逐字未動。`VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s48 --json` 為 **0 errors／0 warnings、102 lines**。`npm run check:tasks` 通過 2,123 票；其輸出另有其他票的既有提醒。`git diff --check -- docs/videos/curio-s48` 通過。

`estimateTimeline` 含預設停頓，較快的 325 單位／分估值：濃縮開場 `atl001→atl009` **45.27 秒**、正文 `atl009→atl999a` **532.07 秒（8:52.07）**、片尾 12.43 秒；250 單位／分正文 **663.90 秒（11:03.90）**。這些都是估值，**不是 R8 配音實測**。供全新讀者隔離使用的純旁白＋13 題 JSON：`/tmp/s48-r8-narrative-input.json` SHA-256 `b5078ae72af81a5062d4e551d6fcaad9ec1c830468858b7f650eb2529963517c`，由 `narrative --slug curio-s48 --json` 唯讀輸出。

R6 的 [付費音訊收據](verify-7.md)仍在私有 `/workspace/.video-work/curio-s48`：原 R6 實測正文 10:48.30、最後一次全句音檢仍 9/102 flagged，故為 **HOLD**。R7 九句聽感改稿、R8 四句敘事改稿後沒有新 TTS 實長或完整音檢；R6 WAV／時間線及 R6 政策和待審網站劇本卡均綁舊文字，不移作 R8 放行。

下一關：另一人按上表**精確 R8 五檔**與固定原文獨立核四句及書面畫面；兩位此前未讀 R8 的隔離讀者只看新 JSON 作正式敘事盲評。若兩關通過，再按精確 R8 重做全稿政策及站台劇本流程，處理改句 TTS、完整零旗標音檢；插畫、配樂和成片仍未製作。
