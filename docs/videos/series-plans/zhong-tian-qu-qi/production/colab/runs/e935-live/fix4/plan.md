# 第 35 集真人版 fix4：s24 錢員外改背影甩袖走開、s06 窗紙破洞

第三輪修片代理 2026-11-20 寫，照協調者的決定（品質優先）：s24、s06 各重抽兩個種子，比現在的好才換；s25 保留 fix3 9351236，能不花錢讓「乾淨」更清楚就做；
motion 接受、不再為指標重拍。依據：`../fix3/plan.md`、`../fix3/review-picks.tsv`、`../review3-plan.md`、第 34 集 `../../e934-live/fix4/plan.md`（背影＋錄音的做法）、
任務檔第 18 集 fix2 的教訓。沒用 RunPod、付費圖、站台 TTS；沒 commit；第 33、34 集的檔沒動。

## 兩鏡 4 支、28 秒（英文全文在 `mkspec.py`）

| 鏡 | 種子 | 秒 | 圖 | 寫法 |
|---|---|---|---|---|
| s24 | 9351241、9351242 | 8 | 只送 fix3 的免費乾田裁切 `../fix3/set-hantian-yang-chen2-liu-gan.png` | 第 34 集 s32 fix4：**不送臉部圖、不點名**，身分句換成服裝句；第一格起寬背正對鏡頭、先吸一口氣（肩起），右寬袖往旁後狠甩一下，再大步沿田埂走向大樹、越走越遠；「背對」寫在構圖與動作兩處；沒有說話句；台詞改鋪錄音 `zq935a25` |
| s06 | 9351243、9351244 | 6 | 許硯 portrait、angle-a，場景改送 `set-xujia-wu-ye-qiang-l1`（素磚牆）| 窗寫成「淡米白窗紙糊在素木格上、紙面空白平整，右下一個拳頭大的破洞、洞裡是黑夜」；許硯拿灰布團一點一點塞進洞、紙在指節下皺起、塞滿後掌心壓平；臉放軟＋NOSMILE；不送 `-chuang`（開著的窗與夜景就是從那張圖來的） |

種子 935124x（`e935refine.sh` 的 SRC 表 `124` = fix4）。`mkjobs.py` 掃描 0（否定名詞、會長字或打開東西的字、掛著／鎖、笑字、s24 沒有任何名字與臉／嘴／說話字、
s06 只有許硯、窗紙／破洞／布團句都在、d1 的 `dark blue with night` 與 `-chuang` 圖不在、種子沒用過）；preflight、check_manifest、h3r check 都 0／0。

```
python3 -I mkspec.py && python3 -I mkjobs.py <live>/fix4
bash scratchpad/e935f4.sh                                                       # zt-live3，跑完 ONLY_SELF 釋放
SESSION=zt-live3 PREP=1 PRECHECK_ONLY=1 ONLY=s06,s24 bash scratchpad/e935refine.sh   # 讀檔順序多了 fix4/review-picks.tsv
SESSION=zt-live3 ONLY=s06,s24 bash scratchpad/e935refine.sh
bash ../e935cut.sh
```

## 結果（2026-11-20）

- **跑**：`e935f4.sh` 一輪 4/4，ONLY_SELF 釋放後 sessions 空、assignments 0；285.74 → 284.50 CU（1.24）。
- **挑片**（`review-picks.tsv`；**只有本代理一人挑**，scratchpad `e935f3/pick/f4-*`）：
  - **s24 9351241**，0.75–8.0：全程背對、甩袖、走遠，乾田＋霧＋垂柳，灰金晨光接 s22 s23。比 fix3 9351234（看鏡頭、兩格像笑）好，換。1242 是逆光日出、甩袖晚。
  - **s06 9351244**，0.75–5.75：窗紙＋右下破洞＋布團塞滿，台詞終於看得到；窗紙畫得很亮（像月光照著），第一場其他鏡的窗仍是開口。比 fix3 的壓暗好，換；剪接表拿掉 s06 的壓暗遮罩與黑點層。
    1243 句首貼著第 0 格、4 秒起咧嘴。
- **s24 錄音**：`zq935a25`（站台 TTS 第一次錄的那句，原 134 Hz、說話 7.2 秒）用 `lev935.py`、`PRE=rubberband=tempo=1.15:pitch=1.12:formant=preserved` 整平到 −13.5 LUFS
  （約 146 Hz、6.2 秒；原檔在 `audio/orig/`），`voice_off` 加 s24、`line_at` c1.15（哼落在 c1.25 的甩袖上）；甩袖 swish-7 c1.25、腳步 c3.95／4.6／5.25。
- **s25「乾淨」（不花錢）**：放好的 s25 片段單獨聽寫是對的（「這片吃乾淨了」），成片裡聽成「看盡」是被 face-slap、風聲、鳥聲蓋掉。做法：s25 原聲 −4 → −2.5 dB，
  c2.15–2.75（乾淨）加 2.8 kHz +4 dB 的清晰度。沒有拿錄音替換（她在畫面上開口，換聲音會對不上嘴、音色也不同）。
  再把本鏡風聲 −17 → −25、鳥聲只到 s24。**結果**：成片 plain 仍聽成「這片吃看盡了」（帶稿是「乾淨」）——面板與字幕在，交給人耳；沒有更乾淨的不花錢辦法了。
- **精修**：`SESSION=zt-live3 ONLY=s06,s24 bash scratchpad/e935refine.sh`（PRECHECK 40 鏡全過，讀檔順序多了 fix4/review-picks.tsv），s06 一輪完成；s24 第一次 launch 逾時（600 秒），
  第二輪完成；`.seed` 由 progress 檔補（1312×736，158／192 格）。跑完留下兩台未記名 `[?]` VM（zt-live3 history 14:28 是本次的，zt-live2 最後活動 10:32、沒有別的 driver），
  手動 unassign，sessions 空、assignments 0、rate 0。舊精修在 `refined/old/s06-9351101.mp4`、`s24-9351234.mp4`。精修與草稿並排看過（scratchpad `e935f3/pick/refined4.jpg`）。
- **Colab**：285.74 → 草稿 284.50 → 精修後 276.93 CU（精修與閒置 VM 7.57）；**fix4 合計 8.81 CU，餘額 276.93 CU**。
- **剪接**（scratchpad `e935r3/run4.log` 定版）：成片 **218.93 秒**（fix3 版 217.80；s06 4.54 → 5.00、s24 6.88 → 7.58）、−14.0 LUFS、LRA 5.8、峰值 −3.4 dBFS。
  cut-qa 只有 motion FAIL（片子 4.6／靜止 24%，成片 3.8／34%；協調者接受）、jitter 40 ok、black 0；cut-jumps 0；audio-qa 36 句 0 問題。
  音高：錢員外 a25 錄音 146 對阿令 a26 192＝**4.7 半音**；許硯 s06 a08 109。聽寫：s06「別怕，哥把洞堵上，蝗蟲進不來」、s24「哼，三畝田保住又怎樣，鄰村的人可要餓死了」帶稿都對（全片見 `e935r3/fwcut-f4.txt`）。
  成片看過（`e935r3/chk/cut4.jpg`）：s06 窗紙、破洞、布團；s24 甩袖在「哼」上、背影走遠。
- **要人耳／人眼**：s24 錄音（tempo 1.15）跟 s22 片中原聲、s31 錄音像不像同一人、背影鋪錄音讀不讀得出氣走；s06 窗紙很亮（像月光），第一場其他鏡的窗仍是開口；s25「乾淨」。

## 終驗後的兩項不花錢修改（`../final-check.md` 輕微 3、7）

- s24 vf `eq=brightness=0.05:saturation=1.25,colorbalance=rm=0.03:bm=-0.03`：成片整格 Y 40–47 → 50–58（s23 尾 49、s25 78），袍子飽和度 0.68（s23 0.58）；逐格每 0.25 秒看過，全程背影、沒有破格（scratchpad `e935r3/chk/s24final.jpg`）。
- s06 cloth1 c3.8 −18 → c3.65 −10：36.86–37.1 從 −54..−50 變成 −39..−46（底 −50）。
- 重組（scratchpad `e935r3/run5.log`）：**218.93 秒**、−14.0 LUFS、峰值 −4.1 dBFS；cut-qa 只有 motion（已接受）、cut-jumps 0、audio-qa 36 句 0 問題。
