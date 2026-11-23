# 第 37 集真人版 fix3（REVIEW 3 重拍：s27 s27b s32 s18 s09 s12 s19 s31 s28）

第三輪修片代理 2026-11-23 寫（品質優先）。依據：`../cut-review.md`（審 1，6.0／10）、`../cut-review-2.md`（審 2，6／10）、`../review3-plan.md`、範本第 36 集 `../../e936-live/fix3/`、`fix4/`，本集 `../fix2/`。
沒用 RunPod、付費圖、站台 TTS；沒 commit。

## 九鏡 18 支、110 秒（英文全文在 `mkjobs.py`；種子 9371231／9371232）

| 鏡 | 基底 | 秒 | 改了什麼（為什麼） |
| --- | --- | --- | --- |
| s27 | fix2 9371221 | 5 | 第一格：她右手低握長槍、槍頭在兩人之間的地上；刁七右手把刀平舉在胸前。動作只有一個「挑」：槍頭由下往上撞刀身、刀飛出上緣不回來（兩位審查必改：fix2 1221 空手揮、槍 c0.375 才長出來；fix2 1222 逐格看是他自己甩刀）。刁七粉量改淡、頭髮仍黑 |
| s27b | fix2 9371221 | 6 | 三大步遠、槍尖停在喉前一掌、空隙對著夜空、鏡頭在喉嚨高度（fix2 槍尖貼頸） |
| s32 | d1 9371101 | 6 | 她在左三分之一、流寇在右半邊四步外、實心深色木桶、水落在他身上、他往後倒、固定鏡（d1：桶半透明疊在他臉上、水往上噴、人縮小消失） |
| s18 | d1 9371101 | 6 | 疤照聖經寫成「左眉骨到左顴骨一整條」，臉幾乎正面讓左頰看得到；不笑 |
| s09 | d1 9371101 | 8 | 不笑：眉微皺、下巴繃、句間嘴閉（d1 兩支都笑） |
| s12 | d1 9371101 | 6 | 鋤頭扛在肩上、扁鐵刃直角（d1 是十字鎬）；兩人不笑 |
| s19 | d1 9371101 | 6 | 不笑：下巴繃緊、眼睛瞇向火光、嘴角往下 |
| s31 | d1 9371101 | 6 | 阿令的木鞘刀寫成樹皮深褐、貼在腿邊（d1 是淺色長筒）；不笑 |
| s28 | d1 9371101 | 6 | 前景插地的刀拿掉（審 2：像日本刀；1.25 倍裁切會切到跪著的膝蓋、刀還留一半）；粉改淡、長疤、刁七不笑（A、B 兩批送出之後才加的 C 批） |

`mkjobs.py` 掃描 0（基底提示詞 sha256、每句替換在基底裡正好一次、必含句、不該留的句、cinema camera／beard／stubble／sword／fog／pool／open／hang／flick／pickaxe／fountain、笑字只在 NOSMILE、否定名詞、分隔句、長槍道具圖在最後、種子沒用過）；
`preflight-prompts.py`、`check_manifest.py`、`h3r.sh check` 都 0／0。

```
python3 -I mkjobs.py /root/mokaair-work/videos/zhong-tian-qu-qi-e937-dh/runpod/live/fix3     # 18 jobs, 110 s, scan 0
BATCH=a SESSION=zt-live3 bash <scratchpad>/e937f3.sh   # s27 s27b s32 s18
BATCH=b SESSION=zt-live2 bash <scratchpad>/e937f3.sh   # s09 s12 s19 s31（同時）
BATCH=c SESSION=zt-live3 bash <scratchpad>/e937f3.sh   # s28（A 批跑完、zt-live3 釋放之後）
```

## 跑與挑片（2026-11-23）

- 送前 `colab sessions` 空、沒有別的 driver、assignments 0、餘額 **167.04 CU**。A 批（zt-live3）與 B 批（zt-live2）同時跑、各一輪 8/8（10:13–10:36 UTC），跑完各自 `ONLY_SELF=1` 釋放 → **163.06 CU（16 支 98 秒 3.98 CU）**。
- C 批 s28：zt-live3 前兩次 G4 assign 一直 `Service Unavailable`（同時 zt-live2 在精修），第二輪拿到、1232 做完，**1231 沒拍成**（1232 夠用，不補）。
- **挑片**（`review-picks.tsv`，只有第三輪修片代理一人挑；scratchpad `e937r3/look/`）：s27 1231、s32 1231、s18 1232、s09 1231、s12 1231、s19 1231、s31 1231、s28 1232 換；**s27b KEEP fix2 9371221**。
- **精修**：`SESSION=zt-live2 PREP=1 PRECHECK_ONLY=1 ONLY=… bash <scratchpad>/e937refine.sh`（picks 43 等於六個 tsv 疊起來，openings、43 jobs、refine.py --check 0 錯）→ 七鏡一次在 zt-live2 完成；
  s28 在 zt-live3 三次拿不到 G4，改 zt-live2 一次完成。`.seed` 由 progress 檔補成挑的種子，1312×736、格數等於草稿；舊精修移到 `refined/old/`。草稿／精修並排看過（`e937r3/look/ref1–3.jpg`）。
- 餘額 163.06 → 158.50（C 批＋七鏡精修）→ **158.26 CU**（s28 精修）。**fix3 合計 8.78 CU**。最後 sessions 空、assignments 0、rate 0，沒有未記名 VM。
- 換進成片：`e937cut.sh` run4（見 `../review3-plan.md`〈結果〉）。
