# 第 32 集真人版 fix1 重拍計畫（未送出）

合併代理 2026-11-18 寫。依據：`../review-picks-a.tsv`（35 挑定、RETAKE s01 s14 s19 s25）、`../review-picks-b.tsv`
（37 挑定、RETAKE s01 s25）、合併結果 `../picks-merged.tsv`、route-a.md 最後幾十條教訓、第 30／31 集 fix1 的做法。
**只寫好、檢查過，沒有送出任何生成**（Colab、RunPod 都沒開，沒用站台 TTS）。

## 重拍清單

種子 9321201／9321202，每鏡兩支，長度照 d1 買的秒數；三鏡都是第一優先（剪接救不了）。

| 鏡 | 秒數 × 支 | 為什麼剪接救不了 | 改什麼（提示詞） |
|---|---|---|---|
| s01 | 5 × 2 | 兩人都標嚴重。前景「只見背影」的大個子 0.3–3.2 秒露出圓臉、平頭的側臉（不是二牛的瘦長臉加頭頂髮髻，s41→s01→s02 會像換人）；家丁站在土埂頂上排成二十五人以上的長隊、排到畫外（第 31 集 s41 實拍約十四人，一接就看出翻倍）；1101 鋤頭 2.7 秒起變成秦霜手裡的長桿、1102 鋤頭收回肩上，都沒有「挑飛」。整支的事。 | 背影：`turned a little away from us toward the right` 換成 `his broad back square to us`，加二牛定稿的髮型 `his black hair tied up in one small round topknot on the crown of his head`，`the back of his head toward us the whole shot` 換成「後腦與髮髻從第一格到最後一格朝我們、整鏡只見後腦與耳廓」。家丁：`a short row of exactly fourteen men …`，並寫這排在哪裡結束「第十四人在畫面中間偏左、之後只有泥水與竹山」（不寫 no more）。動作：結果寫在前面「鋤頭離手、從左上角飛出畫面，他兩手空著留在頭上；扁擔一直在秦霜兩手裡」，畫面裡不留鋤頭給模型接手（原本「刃朝下插在畫左緣土路上」容易被畫成交到她手上）；鋤頭落在畫外，s04 許硯從土裡拔起仍讀得通。圖不變（秦霜定妝照＋翻轉的壩 `set-shangyou-ba-fx-l1`），二牛不點名、不送他的圖（route-a 第 8 集：背影不送臉的圖）。 |
| s19 | 6 × 2 | A 標 RETAKE、B 選 1102；協調者逐格放大後決定重拍。1101 二牛 0–3 秒露齒大笑；1102 二牛 1.4–2.9 秒明顯閉唇笑、3.4 秒仍帶笑，正壓在秦霜開口（1.88 秒）的前半句上，剪掉就切台詞；1102 秦霜 2.4 秒也張嘴笑。許硯昏在井底，笑完全不對（原版必修：二牛每鏡不笑）。兩人並排、秦霜偏正面，看不出同一條繩上一前一後。 | 二牛：`his lips pressed shut, not smiling` 換成 `not smiling: his face hard with worry, brows drawn together, jaw clenched, lips pressed together in one flat line,` ＋本季 NOSMILE 句，臉朝畫左的坑。秦霜：`commanding, not smiling` 換成 `commanding and urgent … ` ＋ NOSMILE。站位：`the two of them one behind the other along the same rope, both facing screen left`。動作：秦霜後蹬拉繩之外加「二牛在她前面跟她一起往後拉」。台詞、圖（秦霜定妝照、二牛定妝照＋angle-a、`set-jingkeng-kou-l1`）照 d1。 |
| s25 | 8 × 2 | 兩人都標。1101 畫面裡兩個秦霜（嚴重）；1102 三人朝鏡頭走，秦霜 4.1–5.5 秒從左邊出畫，最後只剩二牛中景、4.4 秒起閉唇笑到片尾。系統兩句 a22＋a23 要約 5.4–5.6 秒，1102 能用的 4.08 秒放不下。 | 構圖：`like the picture, along the row of earth heaps` 換成「鏡頭在土堆列的側面，兩人側面朝我們、在中景，從第一格到最後一格整個人小小地在畫面裡」，秦霜加 `the only woman in the frame`，`striding toward the left edge of the frame` 換成「從畫面右半慢慢往左走、側面朝我們」（不走出畫、不朝鏡頭走近）。二牛：側臉朝畫左、眼睛看著她扛的人，`brows knotted with worry, lips pressed together in one flat line` ＋ NOSMILE。人數：`exactly three people: two walking, Qin Shuang with the man over her right shoulder and Wang Erniu behind her …`。動作句加「兩人側面、在中景、整個人留在畫面裡到最後一格」。保留 d1 的慢推（mkjobs 檢查每鏡都在）。 |

**預估**：3 鏡 6 支、共 **38 秒**（s01 10、s19 12、s25 16）。照第 31 集實測（86 支 556 秒 ≈ 2.59 小時、約 26 CU）按秒數比例約 **0.2 小時、約 2 CU**，加 Colab 冷啟動約 0.3–0.4 小時、3–4 CU（約 US$0.3–0.4）。`colab-jobs.json` 就是全部 6 支；沒有第二優先。

### 看過但不重拍的（理由寫進 picks-merged.tsv）

- **s14**（A 單獨標 RETAKE：二牛方向錯、沒抓繩）：逐格放大 1102，二牛整鏡是側臉／四分之三朝畫左、看著他左邊的許硯（方向對，1101 也是），右手 0.75–1.5 秒握在許硯腰前的繩上。起點從 B 的 1.583 提前到 1.000 就留住抓繩。**剪接救得了**，選 1102 1.000–6.500。
- 其他兩人列的中等問題，看過都留給剪接或接受：s08、s13、s29 過肩「許硯」的鬍子下巴（放大約 1.1 倍往右裁推出畫；s05 同理往左裁）；s24 耳根紅（調色只提耳緣）；s16 鎬頭糊成鏟形（剪在兩段之間 1.667–3.750）；s26 不是倒掛（為了跟 s26b 接得上選側趴，見下）；s23 朝鏡頭走、s36 四張清楚的臉、s35 沒有明顯一拜、s10 秦霜帶笑（都是中等偏小，接受）。

## 交給剪接（已寫進 picks-merged.tsv 的 reason）

- 裁切：s08、s13、s29 放大約 1.1 倍往右裁，把左緣前景下巴的鬍子推出畫；s05 往左裁推掉右緣下巴。**不要水平翻轉**（古裝交領會變左衽）。
- 調色：s24 只把看得到的耳緣提紅一點（稿子要耳根紅）。
- 剪短：s16 只用 2.083 秒（嫌短可延到 4.375，多四格鏟形動態模糊）；s20 照稿 3 秒（可延到 5.167）；s37 4.5 秒（可延到 5.167）；s32 嫌開頭門扇亂可從 1.000 起。
- 多唸的人聲：s03（0.68–1.14）、s06（1.88–2.30）在起點前，s23（3.90 起）在終點後，剪點已避開；剪點前後要人耳聽一次。
- s26→s26b：s26 選 1101（側趴、眼皮撐開一條縫），跟 s26b 1102 同一姿勢；站主想要稿子的「倒掛的臉」就換 s26 1102，並接受兩鏡間姿勢跳接、扛他的人讀成髮髻（像二牛）。

## 檢查結果（2026-11-18，都是免費的本機檢查）

```
python3 -I mkspec.py                                    # 3 shots -> spec.json
python3 -I ../../_scripts/retake.py <live>/st1 <live>/fix1 spec.json   # 6 jobs
python3 -I mkjobs.py <live>/fix1                        # 掃描 0 命中；colab-jobs.json 6 支、38 秒
python3 -I ../../_scripts/preflight-prompts.py <live>/fix1/colab-jobs.json            # 0 error(s), 2 warning(s)
python3 -I .agents/skills/minimax-h3-colab/scripts/check_manifest.py <live>/fix1/colab-jobs.json   # 0 error(s), 0 warning(s)
bash .agents/skills/minimax-h3-runpod/scripts/h3r.sh check --manifest <live>/fix1/colab-jobs.json  # 0 error(s), 0 warning(s)
```

`<live>` = `/root/mokaair-work/videos/zhong-tian-qu-qi-e932-dh/runpod/live`，輸出會放 `<live>/fix1/out/sNN-93212xx.mp4`。
preflight 的 2 個 warning 是 s01 的 `carrying pole`（道具不在參考圖裡，d1 就有、第 30／31 集同樣接受）。
mkjobs 的掃描：否定名詞 0、兵器與 pick 字 0、會長字的字（含 open）0、掛著／鎖／攤位的字 0（s25 d1 的「頭與手臂垂在她背後」除外，PREP.md 同樣不算）、`not smiling` 與 NOSMILE 以外的笑字 0、點名不在畫面的人 0、每鏡慢推一次、fix1 句子沒漏進 d1、被換掉的 d1 字句已不在、圖與秒數照 d1。

## 送出後挑片要看的

- s01：大個子是不是全程只見後腦與頭頂髮髻（沒有側臉）；家丁放大三倍數是不是十四人、排到中間偏左就停；鋤頭有沒有被挑飛出畫、沒有留在秦霜手裡；扁擔一直在她手上。
- s19：二牛每 0.5 秒放大看，整支不笑（眉頭擠、咬牙、嘴抿直）；秦霜說話時不笑；兩人一前一後同一條繩、都朝畫左；台詞前後有沒有多的人聲。
- s25：畫面裡只有一個秦霜；兩人全程在畫面中景、側面朝左走，沒有人走出畫或走近成特寫；二牛不笑；能用的長度要放得下 a22＋a23（約 5.6 秒）。
- 重拍仍不行時的備案寫在 `review-picks.tsv` 與 `../picks-merged.tsv`。
