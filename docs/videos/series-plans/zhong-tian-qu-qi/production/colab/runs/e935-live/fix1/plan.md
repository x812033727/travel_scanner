# 第 35 集真人版 fix1 重拍計畫

合併兼 fix1 代理 2026-11-20 寫。依據：`../review-picks-a.tsv`（RETAKE s17b s23 s34；s01 選 1102）、`../review-picks-b.tsv`（RETAKE s01 s17b s23 s34）、
合併結果 `../picks-merged.tsv`（各鏡裁決、剪點與備案）、`../{mkspec.py,spec.json,PREP.md}`（§6）、第 34 集 `../../e934-live/fix1`。
協調者授權 Colab（跑之前餘額 325.80 CU，門檻 100）；送在 `zt-live3`（送之前 `colab sessions` 沒有任何 session、assignments 0）。
沒有用 RunPod、付費圖、站台 TTS；沒改 `writer-tools/e035-r2/r2.py`；沒 commit。

## 重拍清單（5 鏡 10 支、76 秒）

種子 **9351211／9351212**（第 35 集的 93512xx 只有村口改圖用過 9351201–9351204）。秒數照 d1 買的長度：五鏡都不說話（畫外錄音／系統／心裡話蓋上），
錄音實測都放得下（s01 a01＋a02 4.88 秒／8；s17b a20 4.40／6；s23 a24 5.44／8；s30 a31＋a32 8.04／10；s34 無），所以不改秒數。
基底是 d1 9351101 實際送出的工作與提示詞（`../mkspec.py` 的 d1 修改已在裡面，`mkjobs.py` 先核 sha256 與每條 d1 修改），每句 fix1 替換先 assert 在 d1 提示詞裡剛好一次。

| 鏡 | 秒 × 支 | 誰標的 | 為什麼剪接救不了 | 改什麼（英文原句在 `mkspec.py`） |
|---|---|---|---|---|
| s01 | 8 × 2 | B；A 選 1102 但合併代理逐格看後改判 | 窗外 `small dark shapes` 兩支都長成動物（1102 長耳兔剪影整支、1101 熊崽爬上窗台）；第一格都沒有回頭望窗；1102 窗在畫右 | 黑影改「幾個比指尖還小的暗點掠過窗框」；構圖句加「窗在後牆、畫面左上、他身後，照 <Picture 3>」；回頭寫成第一格的結果（後腦與側臉向我們、眼睛在窗上）；撞窗改一個小暗點，然後慢慢轉回正面看桌上方的空處、手指收緊；表情逐部位＋NOSMILE；**固定鏡** |
| s17b | 6 × 2 | A、B | 鉤子『六隻鴨子同一刻轉頭』兩支都沒有（第一格就全朝右） | 近景改中景、「六隻都完整在畫裡」；頭兩秒逐隻寫方向（兩隻朝左緣、兩隻背對鏡頭、兩隻嘴在水裡）；然後一拍：「同一瞬間六隻一起抬頭猛轉向畫右緣的岸，伸長脖子，定住到最後一格」；**固定鏡**（推近會看不到六隻） |
| s23 | 8 × 2 | A、B | 錢員外兩支都開口說亂話、一直笑；鴨子是褐頭綠頸的野鴨；1102 他身後一台**電影攝影機與腳架**（開頭 `shot on a cinema camera` 被畫成物件，s22 1102 也有） | 本鏡開頭改 `with the look of a feature film`；身分句 `small shrewd eyes` → `small narrow eyes under heavy brows`；`his smug look draining away, not smiling` → 「臉慢慢垮下、發酸：嘴角往下、臉頰鬆垂」＋NOSMILE；nospeak 句加 `his jaw still` 與「這鏡他沒有聲音，只有眼睛從她的手移到水上」；背景加「左邊水上三隻白羽橘嘴的家鴨」；唐小棠丸子句加「每一根頭髮都盤進兩顆丸子」（兩支都多兩條垂辮）；**固定鏡** |
| s30 | 10 × 2 | 合併代理（A、B 都說中等偏小、建議剪接或重拍） | 1102 背後柵門橫梁上一塊木牌、兩個像字的記號，1–9 秒都在，隨推近移動約 100 px，固定框模糊蓋不住，要逐格追蹤 | 拿掉兩處 `by the gate`（門帶出牌子）；第三張圖（`-kong` 天空裁切）寫成「只給背景顏色」（同第 34 集 s37）；背後「只有遠山暗線上的橘紅天與左緣一棵柳樹垂下的暗枝，頭肩四周都是天」；表情逐部位＋NOSMILE；**固定鏡**。**1102 是備案**：fix1 不比它好就用它、剪接追蹤模糊木牌 |
| s34 | 6 × 2 | A、B | 柵門兩支都開了（破 s35『手按門閂不拉』與第 36 集『抬起門閂』）；兩個女生走到他前面 | 結果先寫：「兩扇圓木門扇從第一格到最後一格都關著，齊腰的橫門閂橫在兩扇上、扣在鐵件裡」；許硯「停在門閂前一步，門還關著」；守門兩人 `stepping aside` → 「站著不動、一人一端」；火光「只從圓木之間的窄縫透進來」；唐小棠「在他右肩後、三人的右緣」、阿令「在他左肩後」，結尾句「最後兩人仍在他身後」；守門人的表情＋NOSMILE；**固定鏡**（推近會穿過門線） |

**s14 不重拍、剪接處理**：合併代理放大 1、3、5 秒，遠山上方有一片細小黑點（B 說得對），只是沒有成帶。1101 是唯一髮型與必修都對的一支，重拍要重新賭這兩件；
台詞『蝗蟲又過山了』與 s15、s17b 已經交代。剪接在遠山上方加深黑點（疊第 34 集 s40 蝗群素材、低不透明度），人眼看手機大小讀不讀得出。

照的教訓（第 34 集 fix1、route-a）：正面描述、不寫否定名詞；不笑寫逐部位＋NOSMILE、拿掉身分句的 shrewd／smug；嘴閉的鏡不給任何開口的理由；看哪裡寫具體目標；
動作先寫結果、再寫路徑（s01 第一格回頭、s34 門關著停在門閂前、s17b 定住）；推近會毀掉構圖或動作的鏡改固定鏡（五鏡都是）。
**PREP.md §6**：田裡兩鏡（s17b、s23）沒有潭字（掃描 0）；唐小棠背影的替換、clear-air 句是 d1 原句（`mkjobs.py` 核過）。

## 檔案與指令（2026-11-20）

```
python3 -I mkspec.py                                    # 5 shots -> spec.json (76 s)
python3 -I mkjobs.py <live>/fix1                        # 掃描 0 命中；colab-jobs.json 10 支、76 秒
python3 -I ../../_scripts/preflight-prompts.py <live>/fix1/colab-jobs.json            # 0 error(s), 0 warning(s)
python3 -I .agents/skills/minimax-h3-colab/scripts/check_manifest.py <live>/fix1/colab-jobs.json   # 0／0
bash .agents/skills/minimax-h3-runpod/scripts/h3r.sh check --manifest <live>/fix1/colab-jobs.json  # 0／0
bash <scratchpad>/e935f1.sh       # G4、zt-live3、兩輪補缺、跑完 ONLY_SELF=1 colab-release.sh zt-live3；log <scratchpad>/e935f1.log
```

`<live>` = `/root/mokaair-work/videos/zhong-tian-qu-qi-e935-dh/runpod/live`。mkjobs 第一次掃描命中：s23 `hanging`（掛著的字）、s30 `open`（會開東西的字）三處、
s30／s34 d1 原句的 `not smiling`（第 34 集起的掃描不准）——改成 `slack and heavy`、`under the wide evening sky`、NOSMILE 後 0。

## 送出後挑片要看的

- **s01**：窗外只有暗藍夜與很小的暗點，沒有長成任何動物；窗在他身後畫左上；第一格回頭望窗、之後轉回正面；嘴閉、不看鏡頭、不笑；有沒有披外衣。
- **s17b**：頭兩秒六隻朝不同方向，然後同一刻一起轉向畫右的岸；六隻數得出、都在畫內。
- **s23**：錢員外嘴整鏡閉著（每 0.25 秒放大）、不笑；鴨子是白鴨；背後沒有攝影機或機器；唐小棠只兩顆丸子、頭不動、右手往左一伸。
- **s30**：背後沒有任何牌子或像字的東西；嘴閉、眼睛在畫左外；不笑。
- **s34**：門整鏡關著；兩個女生在他身後（唐小棠右後、阿令左後）；許硯停在門閂前；鏡頭不穿過門線。
- 結果與選擇寫在 `review-picks.tsv`（這一輪只有本代理一人挑）。

## 跑完的結果（2026-11-20 08:32–09:15 UTC）

- `e935f1.sh` 一輪 10／10（每支約 3.5–4.5 分鐘，含冷啟動），沒有被殺、沒有第二輪；跑完 `ONLY_SELF=1 colab-release.sh zt-live3`，再查 `colab sessions` 沒有 session、
  assignments 0、usage rate 0，沒有未記名 VM 要手動釋放。**Colab 餘額 325.80 → 322.48 CU（3.32 CU）**。
- 挑片（只有本代理一人，兩支並排逐格）寫在 `review-picks.tsv`：**s01 1211、s17b 1211（hflip）、s23 1212、s30 1212、s34 1212**，五鏡都比 d1 好，沒有沿用 d1 的。
  `../picks-merged.tsv` 的 s01、s17b、s23、s34 四列 RETAKE 與 s30 的 d1 1102 由 `review-picks.tsv` 取代（剪接以 fix1 這份為準）。

## 還要重拍的（建議，都不擋剪接）

1. **s17b（協調者決定做 fix2，已做，見 `../fix2/review-picks.tsv`：取 9351222，換掉 fix1 1211）**：轉頭不是同一刻（1.5–3.0 秒一隻接一隻抬頭），鉤子變弱。若要再拍：把動作壓成一拍——「頭兩秒六隻都低頭在水裡；在第二秒，六隻同一格猛抬頭」，
   並把岸寫在鴨子朝的那一邊（這張 `-zong2-shui` 的田埂在畫左，就寫 toward the dark bank at the left edge，剪接不必翻轉）；6 秒、兩支，約 0.7 CU。
2. 其他接受的小問題寫在 `review-picks.tsv`（s01 多一盞前景油燈與外衣不明顯、s23 唐小棠丸子下的小辮、s34 兩個女生最後並排），人眼看一次再決定，目前不建議重拍。
