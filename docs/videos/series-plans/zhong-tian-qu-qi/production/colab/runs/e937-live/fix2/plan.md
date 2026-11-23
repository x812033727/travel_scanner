# 第 37 集真人版 fix2（s27、s27b）

協調者 2026-11-23 決定（品質優先）：照 `../fix1/plan.md`〈還要重拍的〉的寫法再拍 s27 與 s27b，兩個種子，zt-live3，比現用的好才換。
- `mkjobs.py`：s27 基底是 fix1 9371211 實際送出的工作與提示詞（側面面對面、粉、固定鏡），把結果寫成第一格：刀已經在空中、離他空著的手一臂、旋轉往上飛，第一秒內出上緣、不再回來；
  s27b 基底是 d1 送出的工作與提示詞（d1 1102 的幾何讀得通），加「她兩步外、右臂伸直、槍頭停在喉前一掌、空隙到最後一格」、刁七臉與頭髮一層灰白粉、腰以上、固定鏡。
  兩鏡的 `reference_images` 照基底（長槍道具圖在最後一張、句子在場景句後，`mkjobs.py` 斷言）；沒有 cinema camera。preflight、check_manifest、h3r 0／0。
- `<scratchpad>/e937f2.sh`（G4、zt-live3、送之前沒有 session）：一輪 4／4，06:37–06:52 UTC；跑完 `ONLY_SELF=1 colab-release.sh zt-live3`、sessions 空、assignments 0、沒有未記名 VM。
  **餘額 190.11 → 188.67 CU（1.44 CU）**。
- 挑片（只有本代理一人）`review-picks.tsv`：**s27 9371221**（刀真的離手飛出上緣，0–1.5 秒）、**s27b 9371221**（兩步外、臂直、粉；槍頭仍貼頸側）。兩鏡都比現用的好，換。

## 精修（2026-11-23 06:50–08:44 UTC，協調者決定）

- scratchpad `e937refine.sh`（照 `e936refine.sh`）：讀檔順序 `picks-merged.tsv` → `fix1/review-picks.tsv` → `fix2/review-picks.tsv`（之後有 cut-trims／review3-trims／fix3+ 也讀），KEEP 列保留前面的選擇；
  頭句改寫 scratchpad `tools/heads937.py`（s07 s09 加「the young woman seen only from behind … her back to us」、s14 s36 加「the young man in the foreground seen only from behind … his back to us」）；
  retake 動作句的 d1 鞋句拿掉、fix1 s27 的 flicks 換字（未用到：s27 改用 fix2）；不准 `shot on a cinema camera`。
  **append_pictures**：精修只送草稿與第一格（`refine.py` 沒有參考圖），髮型圖、長槍圖的效果在草稿本身；精修文字帶的是各 retake 的動作句（`refine-prep.py`）與上面的頭句。
- `PREP=1 PRECHECK_ONLY=1` 0 錯（43 picks、openings、43 jobs、`refine.py --check` 0）。`route_a_st2.py` 分 20／20／3：BATCH=1＝st2-1（zt-live2）、BATCH=2＝st2-2＋st2-3（zt-live3）。
- 兩批同時起跑；BATCH=2 第一次 G4 拿不到（assign `Service Unavailable` 六次，st2-3 的三鏡在第三次拿到、做完），5 分鐘後重跑一次就拿到，23／23。
  沒有被 2 小時上限殺掉；缺 .seed 的由 seedfix 從 colab-progress 補（種子與 picks 相同）。兩批各自 `ONLY_SELF=1` 釋放，之後 sessions 空、assignments 0、rate 0，沒有未記名 VM。
- **43／43**。核對（scratchpad `e937refine-verify.py`）：每支 `.seed` = picks.json 種子 = 草稿檔名種子，1312×736、格數與草稿相同，**0 錯**。
  草稿／精修每支 6 格並排（scratchpad `e937rv/grp*.jpg`）全部看過：構圖、人數、道具跟草稿一致，沒有新的笑、換臉、多一人；s18 s22 s25 的刀仍是寬背刀；s14 s36 前景後腦放大沒有鬍子。
- **Colab 餘額 188.67 → 167.04 CU（精修 21.63 CU）**。
