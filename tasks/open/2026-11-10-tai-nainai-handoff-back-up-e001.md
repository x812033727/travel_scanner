---
id: 2026-11-10-tai-nainai-handoff-back-up-e001
title: tai-nainai handoff: back up e001-e005 production files to Drive, then shoot episode 6
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-11-10T06:56:17Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/series-plans/top40-2025-2026/2025-01-tai-nainai/production/session-tools
---

# tai-nainai handoff: back up e001-e005 production files to Drive, then shoot episode 6

## Why

Describe the problem in the terms someone who has never seen it would need.

## Definition of done

- [ ] The observable outcome, not the implementation.

## Steps

- [ ] First sub-task.
- [ ] Second sub-task.

## How to verify

The exact commands or clicks that prove it works.

## Notes

Findings, decisions and dead ends, so the next agent does not repeat them.

## Context
The session that made 《恁祖媽今年18》 episodes 1–5 ended on 2026-11-10. Read
`docs/videos/series-plans/top40-2025-2026/2025-01-tai-nainai/production/session-tools/README.md` first.

- Episodes 1–5 are imported and wait for the owner at /admin/videos.
- Their production files were never copied to Google Drive (the old session could not read the rclone variables).
  Their latest copies are on the retired backup branches in `drama-backup-tn`; the host is moving those branches to Drive.
  Branches `transfer/tn-e001`, `tn-e004`, `tn-e005`, `tn-shared` match the final local files (independently checked).
  `transfer/tn-e002` and `transfer/tn-e003` are older than the final local files (e002: about 34 files — the new c15 take,
  the v3 cut and the import folder; e003 not checked). Whatever the old session decided about those is recorded below.
- Episode 6 is storyboarded and reviewed (37 shots) and nothing has been spent; the prepared manifests are in `session-tools/e006/`.
- Cap from episode 6: 40 CU (owner 2026-11-10).

- [ ] confirm the host migration put `transfer/tn-e00N` and `tn-shared` under `AI劇/恁祖媽今年18/` on Drive
- [ ] episode 6: pictures → stills → clips → pick → fix → refine → cut → review → import → todrive.sh

## 2026-11-10 第 6 集進度（接手的 session）

- 站主 2026-11-10：**第 6 集上限放寬到 55 CU**（首格兩輪後 28 張只定 22 張、已用 10.7 CU 時問的；選「上限再放寬到 55 點」）。RULES.md 第四節在 #2047 分支，合併後補一列。
- 場景圖：正廳白天 zt-day-2、飯廳 fanting-1、托盤 tray-1，已進 `assets/refs/`（舊飯廳在 `assets/refs/orig/`）。
- 首格：第一輪 56 張定 17 鏡，第二輪（`redo_stills.py`）22 張定 5 鏡，第三輪（`redo3_stills.py`，c41 從 c38 修圖）6 鏡各三個種子。挑圖都交獨立代理。
- 整集反覆的錯：飯廳燈畫成紅流蘇燈籠、鐘面數字、月棠臉太正面、前景虛焦肩膀寫在句尾就畫不出來、眼淚畫成紅色。
- CU：場景圖＋首格第一輪 7.54、第二輪 2.34（含關機後補扣 0.82），累計 10.70（2384.25 → 2373.55）。
- 錄音 25 句在 `$TN_WORK/e006voice/`（只有 t006012 用錄音，其餘用原聲）。

### 2026-11-10 上午：第 2、4 集站主看片後的修正，第 6 集首格定案

- 第 6 集首格五輪定案 27 張；拿掉 c16、c17、c20、c33、c37（共 32 鏡）。c41 是月棠站在小滿**身後**扶肩（側面相對的版本三輪都失敗），c01 托盤上只有 1 只杯：兩個都是已知瑕疵，交站主看片。
- **教訓：新機器先跑 Qwen 畫圖、再在同一台跑 H3 片段會失敗**（`ComfyUI 缺少節點：['VHS_VideoCombine']`，畫圖的筆記本裝的 ComfyUI 沒有 VideoHelperSuite，H3 的筆記本又「重用」它）。第 6 集第二批 4 支因此白跑約 3 CU。片段要在新機器或先跑過 H3 的機器上跑；畫圖可以接在 H3 後面。要寫進 `minimax-h3-colab/references/lessons.md`。
- **教訓：獨立審片要逐 0.5 秒對照音量與畫面，抓「嘴在動、在笑卻只有配樂」**。第 2 集 c18（模型讓林美鳳講了劇本沒有的話）、c33（大笑沒笑聲：精修去掉了聲音、組片只把有台詞的鏡放回原聲），第 4 集 c12、c40、c45 都是同一類，之前的審片沒抓到。沒有台詞但畫面在笑的鏡，用草稿自己的笑聲當音效（`sfx-own/<鏡>-laugh.wav`）。
- 第 2 集：拿掉 c18、c33／c34 補草稿笑聲、c10 字幕對齊 27.46 秒；獨立審片通過，10:29 匯入後台（158.7 秒）。c22、c48 兩句之間嘴微張沒聲音，判斷是笑與喘，沒有插草稿畫質的反應鏡。
- 第 4 集：獨立審片＋草稿比對，**精修沒有弄壞**（c04、c19、c29、c43、c45 草稿就是這樣）。不花錢的修正寫在 `drama-backup-tn` 的 `_scratchpad/e004-post/v2/edit-v3fix.json`；白天兩場改 lift 調色；重拍 c29、c30、c36（`session-tools/e004/fix2_stills.py`，首格路線）。站主選「免費修＋重拍 3 鏡」。
- 站主：第 2、4 集修完後新檔推回 `drama-backup-tn` 的 `transfer/tn-e002`、`transfer/tn-e004`（雲端硬碟還在搬）。這個 session 的 add_repo push 被自動權限檢查擋下，要站主放行。

### 2026-11-10 下午：第 4、6 集匯入後台

- 第 6 集（157.5 秒，31 鏡）13:5x 匯入 `/admin/videos`，標題「掉了｜恁祖媽今年18 第6集」。點數約 53 CU（上限 55，站主同意放寬）。片段 77% 第一輪可用；c05、c19、c36、c01、c14、c31 重拍，c01、c14、c19 第三次改 **hero 取樣**（站主同意）才過：hero 的臉與「不笑」比 smooth 穩，但開口前 1.5–2.6 秒的無聲嘴動仍在，靠時間窗避開。
  已知瑕疵（寫在 `post/edit-e006.json` 的 `_note`）交站主：c34「虎口鬆了」少了知遠抓枸杞的插鏡（c33、c37 兩輪出亂碼字幕）、c18 句中約 1 秒嘴動無聲、c39／c36 戒指、c41 身後扶肩、飯廳吊燈各鏡不一、皮夾顏色。
  工作檔：`$TN_WORK/e006-post/`（`build.sh` 從 picks 重建；組片用改過台詞位置的 `video-work.json` 與 `voice-work.json`）。
- 第 4 集修正版（126.8 秒）匯入；重拍約 8.6 CU。審片後再修：c44 心裡話 `spill_lead` 1.4 秒、c36 剪掉無聲大笑、c27／c30 外送袋假字模糊、c41／c32 不套 lift、配樂空拍與交叉淡接。重拍清單：c29（帽子、碗）、c32（米色提袋）跟外送袋不連戲。
- **教訓：沒有台詞但在笑、哭的鏡，草稿自己的聲音要放回來**（第 2 集 c33／c34、第 4 集 c40、第 6 集 c41 都漏過）；**交叉淡接**：同一場兩段配樂之間用 `tail`＋下一段 `from_off` 負值，不要先收再起；**真峰值**：組片後量 `ebur128=peak=true`，開場配樂鼓點曾到 +1.7 dBFS。
- 備份：第 2、4、6 集的新檔都還在這個容器（`drama-backup-tn` 本機 clone 的 `_scratchpad/e00N-post/`、`$TN_WORK`）。站主 2026-11-10：雲端硬碟第 1、5 集還在搬，**等站主說搬完再對照、再傳**；推 `transfer/tn-e00N` 的權限被擋，不推。

### 2026-11-11：第 7 集匯入後台、雲端硬碟全部對過

- 雲端硬碟：主機搬過去的 12 條舊分支逐檔對照，11 條一致；`tn-e003` 少 7 個檔（匯入包與兩支預覽），已從分支補傳，0 差異。第 2、4、6、7 集這兩天的新檔都已用 `todrive.sh` 傳上去，每一包 0 差異。
- 第 7 集（133 秒，27 鏡）06:0x 匯入 `/admin/videos`，「我是沈家的保母｜恁祖媽今年18 第7集」。點數約 31.5 CU（上限 40；帳號同時有別的 session 在扣，照自己機器的開機時間算）。
  分鏡照種田拍法重寫成 29 鏡（舊稿 22 鏡），開拍前獨立審稿必修 8 條。拿掉 c16（書包正面兩次畫成透明的窗）、c25（多出第二個月棠）。首格四輪：**整張重生幾乎都失敗，修最接近的那張多半成功**；c07、c18、c22 用 hero 重拍才過。
- 剪接工具：`post/assemble-v4.mjs` 新增剪接表選項 `mix_gain`（固定增益＋限制器，取代動態 loudnorm）：動態 loudnorm 會把沒有對白的段落拉到對白的音量，第 7 集開場公車底噪先大後小。第 7 集用 4.9 dB。
- 教訓：`spill_lead` 只對 `spill` 清單裡的鏡生效；silencedetect 會把落地聲、底噪當成說話，字幕起點要用語音辨識核對；新機器先畫圖再跑 H3 會缺節點（片段另開一台）；同一個帳號另一個 session 開了幾個小時沒停，站主 2026-11-11 同意直接開第二台。

### 2026-11-11 晚上：第 8 集匯入後台

- 匯入 `/admin/videos`：《老太太還活著｜恁祖媽今年18 第8集》116.5 秒，等站主看片。
- 點數約 59.2 CU：首格四輪約 44.4，26 鏡片段 smooth 一次 14.8。站主先把上限從 48 調到 58，再調到 66，同意把片段剪短到「台詞長度＋1.5 秒、最少 5 秒」：總長從 210 秒剪到 169 秒。
- 拿掉的鏡：c05、c11、c19（全景，首格兩輪都畫不出來）；c25（銅鈴還露在外面）。c28 改用 c26 片段的後段。
- c26、c28 的門縫：`session-tools/e008/door_mask.py` 做遮罩，`build.sh` 疊上去。縫的中心照實拍的小滿放在畫面 47%，不是分鏡寫的 62%。
- 獨立審片之後做的修正，都不花錢：
  - c14 從 3.3 秒起用，拿掉 1.9 秒的空檔；字幕拿掉「媽，」，這聲交給 c13 的錄音。
  - c29 從 3.5 秒起用，前面她手上多了一支發亮的手機。c29 的語音提早 1 秒，從 c28 尾巴開始，講完加一下悶響。
  - 玉琴的音量調小。
  - 黃牆太亮的五鏡用 `dim` 壓暗。
  - c20 加碗盤聲換場。
- 要花錢才能修、交給站主決定：
  - c12 林美鳳露齒大笑，臉也最不像她，審片判值得重拍。
  - c14 是拉著手臂，不是抱腰。
  - 門縫裡沒有手機的光，也沒有影片的哭聲。
  - c28 沒有抱頭的動作。
- 教訓：
  - 首格要從挑定的那張修。把挑定的圖當 image 2 放進去，模型會照抄成那張的構圖（c07 第三輪就這樣）。
  - 提示詞寫「eyes darken」會畫成煙燻妝；寫 laugh 會畫成露齒的真笑。
  - 「第一格已經抱住」要首格本身就抱著才有用：首格沒抱，片段也不會抱（c14 修了四輪都沒有）。
  - smooth 的片段都晚 1.8–3.4 秒才開口，所以剪接窗口都從開口前 0.25–0.5 秒起。
  - 每鏡多買的秒數幾乎全剪掉了，所以照台詞長度買就夠。
