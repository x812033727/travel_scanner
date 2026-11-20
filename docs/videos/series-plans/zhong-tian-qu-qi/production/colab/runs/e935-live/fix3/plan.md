# 第 35 集真人版 fix3：s32 柵門關著、s24 s25 不笑＋乾田、s01 s30 真的會動

第三輪修片代理 2026-11-20 寫。依據：`../cut-review.md`（審查 1：中等 1 靜止鏡、中等 2 窗、中等 3 s24 錢員外笑；輕微 1 阿令笑）、`../cut-review-2.md`（審查 2：**嚴重 1 s32 柵門大開**、
中等 2 s24、中等 4 背景水田、中等 5 motion）、`../fix1/`、`../fix2/`、範本第 34 集 `../../e934-live/fix3/`（s30 錢員外不笑的寫法）、`fix4/`（不送帶笑的角度圖、免費裁場景圖）、
`.agents/skills/minimax-h3-colab/references/motion-quality.md`（第二節：軌跡＋預備動作＋收勢、運鏡寫起訖景別）。不花錢的修改見 `../review3-plan.md`。
協調者授權 Colab（門檻 100 CU；開跑前 294.66 CU，`zt-live3`，送前 `colab sessions` 沒有 session、assignments 0、沒有別的 driver）。沒用 RunPod、付費圖、站台 TTS；沒 commit；第 33、34 集的檔沒動。

## 五鏡 10 支、76 秒（每鏡兩個種子，同一份提示詞；英文原句在 `mkspec.py`）

| 鏡 | 基底（成片原本那支，sha256 核過） | 種子 | 秒 | 改什麼 |
|---|---|---|---|---|
| s32 | d1 9351101 | 9351231、9351232 | 6 | d1 從頭到尾沒寫門扇是關的。照聖經〈道具〉柵門句把結果先寫：「兩扇圓木門扇閉合、中間一道亮縫、齊腰橫木由素鐵件扣在縫上，從第一格到最後一格都關著」，背景整面是關著的門；`beyond the gate` 拿掉，火光「只從圓木縫透進來」；守門兩人站在關著的門前不動；拉袖子後再寫一次「門扇一直關著、橫木在鐵件裡」；許硯臉逐部位＋NOSMILE |
| s24 | d1 9351101 | 9351233、9351234 | 8 | 第 34 集 fix3 s30 的寫法：臉在構圖與說話句各寫一次（「第一格臉上的得意已經沒了，酸、悶：嘴角用力往下、下唇噘起、下巴繃緊、眼瞇在粗眉下」＋NOSMILE），小嘴形；拿掉 `gritted teeth`（會畫牙）、`shrewd`；**拿掉 angle-a**；場景改送免費裁切 `set-hantian-yang-chen2-liu-gan.png`（`-chen2-liu` 的上半：大樹、乾犁溝、遠山，沒有水），文字寫「身後只有乾裂的褐土犁溝」；甩袖寫重心與力 |
| s25 | d1 9351102 | 9351235、9351236 | 6 | 阿令冷臉（第 34 集 fix3 s15 s17 的 ALING_FACE）在兩處；嘴角一挑只准「最後一個字說完之後、最後一秒」；`flooded`、`misty water` 拿掉，同一張乾田裁切；竹竿改成重心轉移加一下有重量的橫掃 |
| s01 | fix1 9351211 | 9351237、9351238 | 8 | 起始改中遠景；動作寫成軌跡：撞窗→肩一縮（預備）→轉回正面→右手把舊灰外衣拉緊（布被拉出皺褶）→重心往前壓到前臂（收勢），燭火晃、影子在牆上晃；運鏡 `pushes in with large amplitude at slow speed, from a medium wide shot to a medium shot`（fix1 是 static，d1 的 small amplitude 模型沒推） |
| s30 | fix1 9351212 | 9351239、9351230 | 10 | 起始改中景（腰上）；晚風吹動額前的頭髮與袖子、一口深呼吸（胸肩起伏）、眼睛從跪著的人移到抱孩子的婦人、吞一下、右手慢慢握拳；運鏡 `from a medium shot to a close-up` |

種子 935123x：`e935refine.sh` 的 SRC 表用種子第 4–6 碼找資料夾（`123` = fix3），所以這輪最多十支；s22、s35 沒有重拍（改用剪接慢推，見 `../review3-plan.md`）；
s06 窗的不花錢做法看起來不像貼黑塊（見 `../review3-plan.md` B3），所以**沒有重拍 s06**。

## 檔案與指令

```
python3 -I mkspec.py                                    # 5 shots -> spec.json (76 s)
python3 -I mkjobs.py <live>/fix3                        # 掃描 0 命中；colab-jobs.json 10 支、76 秒
python3 -I ../../_scripts/preflight-prompts.py <live>/fix3/colab-jobs.json                        # 0 error(s), 0 warning(s)
python3 -I .agents/skills/minimax-h3-colab/scripts/check_manifest.py <live>/fix3/colab-jobs.json  # 0 error(s), 0 warning(s)
bash .agents/skills/minimax-h3-runpod/scripts/h3r.sh check --manifest <live>/fix3/colab-jobs.json # 0 error(s), 0 warning(s)
bash scratchpad/e935f3.sh                               # zt-live3，送前查 driver 與 server session，三輪補缺，跑完 ONLY_SELF 釋放
SESSION=zt-live3 PREP=1 PRECHECK_ONLY=1 ONLY=s01,s24,s25,s30,s32 bash scratchpad/e935refine.sh   # 免費核對
SESSION=zt-live3 ONLY=s01,s24,s25,s30,s32 bash scratchpad/e935refine.sh                          # 只精修選中的五鏡
bash ../e935cut.sh
```

`<live>` = `/root/mokaair-work/videos/zhong-tian-qu-qi-e935-dh/runpod/live`。mkjobs 掃描第一次命中兩項（s24 的兩圖開頭句跟別鏡相同、s01 的 `flickers`），
開頭句放行、`flickers` 改 `wavers` 後 0。

**剪點會不會被 refine-prep 蓋掉**：第一版的剪點是 scratchpad `e935c/applytrims.py` 直接套在 picks.json 上、沒重跑 refine-prep。`e935refine.sh` 的讀檔順序本來就是
picks-merged → fix1 → fix2 → **cut-trims** → **review3-trims** → fix3，`PREP=1` 重跑 refine-prep 後逐鏡比對新舊 picks.json：只有這輪要改的八鏡（s01 s02 s17b s24 s25 s30 s32 s35）變了，
其餘 32 鏡的種子與剪點跟 applytrims 的結果一字不差（第一版 picks.json 存在 scratchpad `e935c/bak/picks-pre-r3.json`）。

## 結果（2026-11-20）

- **跑**：`e935f3.sh` 12:22–12:43，一輪 10/10（每支 1–2 分鐘），ONLY_SELF 釋放後 `colab sessions` 沒有 session、assignments 0、rate 0，沒有未記名 VM。
  **294.66 → 292.13 CU（2.53 CU）**。
- **挑片**（`review-picks.tsv`；**這一輪只有本代理一人挑**，沒有第二位獨立挑片者：兩支並排，整格每 0.5 秒、臉每 0.25–0.5 秒放大、片中原聲 faster-whisper 帶稿與不帶稿；
  看圖在 scratchpad `e935f3/pick/`）：
  - **s32 9351231**：門整鏡關著（嚴重 1 解掉）。1232 開頭 1.5 秒門是開的、之後才關，不用。
  - **s24 9351234**：背景乾田；臉大多是酸、冷哼、凶狠的喊，不再整句咧嘴大笑；**但 3–7 秒眼睛幾乎看進鏡頭、5.75 與 6.25 兩格嘴角像笑**，要站主看。1233 一直笑著說。
  - **s25 9351236**：整鏡冷臉、不笑；背景乾田；「乾淨」不帶稿聽成「堪盡」要聽，水上鴨子是深色剪影。1235 前景一群褐色野鴨。
  - **s01 9351238**：明顯從中遠景推到中景，回頭→轉回→往前壓，外衣看得到。1237 幾乎一樣但看不出外衣。
  - **s30 9351230**：明顯從中景推到近景、風吹頭髮，橘紅天不變；左下前景一支火把。1239 天一路變紫藍，接 s31 會跳。
  - 五鏡都比原片好，全部換；沒有沿用原片的鏡，所以這輪不需要剪接慢推來補 s01、s30。
- **精修**：見下面〈精修〉。
