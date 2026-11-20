# 第 34 集真人版 fix3：s15 s17 阿令冷、s30 s32 錢員外不笑、s33 許硯光臉

fix3 代理 2026-11-20 寫。依據：`../cut-review.md`（中等 1 s33 鬍子、中等 2 s15 s17 阿令笑、中等 4 s32 錢員外笑）、`../cut-review-2.md`（中等 1 s33 換臉、
中等 4 s30 s32 錢員外笑）、`../fix1/`、`../fix2/`（plan.md 與 review-picks.tsv 的教訓）、`../picks-merged.tsv`、範本 `../../e933-live/fix3/`。
協調者授權花 Colab 點數（站主規則：剩約 100 CU 才停；開跑前 360.46 CU）。沒用 RunPod、沒用付費圖、沒用站台 TTS、沒 commit。

## 五鏡 10 支、84 秒（每鏡兩個種子，同一份提示詞）

| 鏡 | 基底（成片現在用的那支，送出時的工作與提示詞，sha256 核過） | 種子 | 秒 | 改什麼（英文原句在 `mkspec.py`） |
|---|---|---|---|---|
| s15 | d1 9341101 | 9341411、9341412 | 8 | 阿令冷臉逐部位＋NOSMILE（構圖與動作兩處都寫）；視線從「the person she is speaking to」改成看壯丁手上的饅頭；遞饅頭時臉一樣冷 |
| s17 | d1 9341101 | 9341413、9341414 | 8 | 同 s15 的冷臉與 NOSMILE；「lips, jaw and cheeks moving clearly」改小嘴形、臉頰不動 |
| s30 | d1 9341102 | 9341415、9341416 | 8 | 「笑容凍住」改寫成具體的嚇呆：眼睜大盯著水、眉抬起往中間擠、下巴鬆垂、嘴角往下垂、臉發白＋NOSMILE（兩處）；拿掉 `small shrewd eyes`、`frozen stretch`（是笑的嘴形）、`fans himself`（悠哉得意的動作），改兩手鬆垂、盯著田壟裡的水 |
| s32 | fix1 9341211 | 9341417、9341418 | 8 | 保留 1211 的站位、動作、視線句（fix2 改視線與「只露側臉」後模型把人轉正、方向反）；只把 sour and dark 那串換成 fix2 做到不笑的噘嘴苦臉，並在動作句再寫一次（嘴角往下、下唇噘＋NOSMILE）；視線看的田寫明 dry cracked（fix2 長出金黃稻田） |
| s33 | d1 9341101 | 9341419、9341420 | 10 | 「a short dark stubble on his jaw」拿掉，寫「下巴、下頦、上唇刮得乾淨光滑，跟圖一樣」，動作句再寫一次光臉；拿掉 `lets out one long slow breath`（fix1 s09：吐氣會開嘴，d1 1102 就開了），改「閉一下眼，再慢慢抬眼看田」 |

### 為什麼這樣改（前兩輪的教訓）

- **表情要寫進動作段**：`refine-prep.py` 只把提示詞「never the mood. 」之後到「One continuous shot.」那段帶進精修；fix1 s32 的 NOSMILE 只寫在構圖，精修就看不到。這次每鏡的表情（s33 的光臉）都在動作段再寫一次，`mkjobs.py` 掃描擋。
- **嘴大開就像笑**：`lips, jaw and cheeks moving clearly` 會畫成大嘴、臉頰上抬；改成 small natural talking mouth shapes、臉頰不動（fix2 s28 的寫法）。
- **s30「笑容凍住」本身就是笑的形狀**：d1 寫 `mouth stuck in a stiff frozen stretch`，模型畫成咧嘴；改成看得見的另一種表情（嚇呆、嘴角往下），聖經的 NOSMILE 只要不笑。
- **s32 不再追「只露側臉」**：fix2 苦臉寫法換到了不笑，但「只見耳、頰、鬍尖」與視線改寫讓模型把人轉回正面、方向反；這次 1211 的站位、視線句一字不改，只換臉。
- **s33 首格不用另做圖**：第 34 集 d1 是參考圖生影片（Ref2V，`xuyan-portrait-l1` 與 `angle-a` 都是光臉），`runpod/a/st2/ff/s33.png` 只是挑中那支的第 0 格；鬍子來自 d1 文字裡聖經的「下巴鬍渣」。重抽後新的首格就是新草稿的第 0 格，由 `refine-prep.py` 照常抽出，**不需要付費圖**。
- 正面描述、不寫否定名詞；阿令不寫 young woman（精修掃描擋）；田裡三鏡（s30 s32 s33）沒有 pool／pond（PREP.md §6）；clear 句是 d1 原句。

## 檔案與指令（2026-11-20）

```
python3 -I mkspec.py                                    # 5 shots -> spec.json (84 s)
python3 -I mkjobs.py <live>/fix3                        # 掃描 0 命中；colab-jobs.json 10 支、84 秒
python3 -I ../../_scripts/preflight-prompts.py <live>/fix3/colab-jobs.json                        # 0 error(s), 0 warning(s)
python3 -I .agents/skills/minimax-h3-colab/scripts/check_manifest.py <live>/fix3/colab-jobs.json  # 0 error(s), 0 warning(s)
bash .agents/skills/minimax-h3-runpod/scripts/h3r.sh check --manifest <live>/fix3/colab-jobs.json # 0 error(s), 0 warning(s)
bash scratchpad/e934f3.sh                               # Colab zt-live3（zt-live2 不碰），三輪補缺，跑完 ONLY_SELF 釋放
```

`<live>` = `/root/mokaair-work/videos/zhong-tian-qu-qi-e934-dh/runpod/live`。種子 9341411–9341420 在 repo 與 `<live>` 都沒用過（`refine-prep`／`e934refine.sh` 的 SRC 表 `14` = fix3）。
mkjobs 掃描：基底 sha256 等於送出的；否定名詞、兵器字、兩個分隔句各一次、會長字或打開東西的字、掛著／鎖、笑字（NOSMILE 與 s33 d1 原句「relieved, not smiling」除外）、
畫面外的人名、田裡的潭字、clear 句一次；fix3 每句在、且不在任何 d1／fix1／fix2 提示詞（s30 借用 fix1 s32 的 `small narrow eyes under heavy brows` 除外）；
舊字已不在（moving clearly、shrewd、frozen stretch、fans himself、sour and dark、stubble、breath）；表情與光臉在動作段；台詞、s33 無台詞句；圖與秒數照基底。

**預估**：10 支、84 秒。照 fix1（8 支 64 秒約 3.5 CU、24 分）約 **4.5 CU、30 分**。

## 送出後挑片要看的

- **s15**：每 0.25 秒放大阿令的嘴與臉頰：嘴角平、不上揚、不露齒；遞饅頭讀得出、手不黏；四個人；聽寫整句一字不差。
- **s17**：同上；抬手平掌往水車架；眼睛朝畫右的輪子、不看鏡頭。
- **s30**：嚇呆或垮臉、嘴角往下，整句沒有一格像笑（尤其 3 秒張嘴那裡）；兩個家丁、三人；後退一步；聽寫整句。
- **s32**：第一格背對四分之三往右走、右肩回頭、甩袖在前段、說完在右三分之一（1211 的站位）；苦臉、不笑；田是乾裂的空田；聽寫整句。
- **s33**：每 0.5 秒放大臉：光臉、跟 s29／s34 同一張臉；嘴全程閉；不笑；面板放得下（胸前 y 840）。
- 比原片差就沿用原片（`picks-merged.tsv`／`fix2/review-picks.tsv` 現在那支）。兩位獨立挑片者各自看、不看對方，合併寫 `review-picks.tsv`。

## 結果（2026-11-20）

- **跑**：`scratchpad/e934f3.sh`，03:33–04:03，10/10 一輪完成，跑完 ONLY_SELF 釋放 zt-live3；360.46 → 356.30 CU（4.16 CU）。
- **挑片**（`review-picks.tsv`）：s15 **9341411**、s17 **9341413**、s30 **9341415**、s33 **9341420**；s32 **KEEP**（沿用 fix1 9341211）。各鏡理由、剪點、不選另一支的原因都在 tsv。
  - 有做到的：阿令兩鏡、錢員外 s30 整鏡不笑（嘴角平或往下）；s33 光臉、嘴全程閉（1420）；表情寫進動作段後精修沒有把笑或鬍子帶回來（成片 83.5–95.5、165.5–169.5、184–190.5 抽格看過）。
  - 沒做到的：**s32** 1417 照 1211 的站位走開，但一樣咧嘴笑；1418 不笑，但身體轉正、沒有走開，背景整片金黃稻田——三輪六支都沒有同時做到，教訓：這個人物在側臉說話時模型就給笑，表情寫得再具體也一樣；下次要嘛全程背對、台詞放錄音不對嘴，要嘛換鏡位。s30 兩支畫右都長出一條金黃的草（d1 也有、較窄）。s33 1419 光臉但嘴在動、帶笑。s15 1411 原聲多一個「個」，剪接用 `aselect` 剪掉（見 `../review3-plan.md`）。
- **挑片者**：任務要兩位獨立挑片者各自看；本 session 沒有派子代理的工具，兩輪是同一個代理分開做的（第一輪只看每 0.25 秒放大的臉與手、第二輪只看音訊包絡、聽寫與整支站位），**不算真的獨立**，要協調者知道。看圖在 scratchpad `e934f3/pick/`。
- **精修**：`PREP=1 ONLY=s15,s17,s30,s33 bash scratchpad/e934refine.sh`（加了 `cut-trims.tsv` 與 fix3 s30 的 d1 鞋句處理），04:05–04:35，4/4；舊精修移到 `refined/old/`；s33 的 `.seed` 由 progress 檔補（被時間切斷前已下載完整，1312×736、243 格）。精修後留下一台 `[?]` VM，zt-live3 history 證明是本次的，手動 unassign。356.30 → 352.00 CU（4.30 CU）。**fix3 合計 8.46 CU。**
