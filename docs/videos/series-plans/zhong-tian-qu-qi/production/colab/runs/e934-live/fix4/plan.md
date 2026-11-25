# 第 34 集真人版 fix4：s32 錢員外改背影甩袖走開、台詞鋪錄音

fix4 代理 2026-11-20 寫。依據：`../fix1/`、`../fix2/`、`../fix3/`（plan.md、review-picks.tsv）、`../review3-plan.md`〈還要站主決定〉第 1 條、剪接表 `_note`、
聖經 `r2-bible-e031-e040.md`（錢員外第 34 集 c30–c32 `NOSMILE`、115–175 Hz）、任務檔第 18 集 fix2 的教訓（e918 s37：不送臉部圖、不點名，從身後拍，畫外放錄音，一次成功）。
協調者授權花 Colab（約 1–2 CU；開跑前 351.15 CU，門檻 100）。沒用 RunPod、付費圖、站台 TTS；沒 commit；第 33、35 集的檔沒動。

## 為什麼這樣改

三輪六支（fix1 1211／1212、fix2 1313／1314、fix3 1417／1418）都沒同時做到「不笑＋走開＋乾田」：只要他側臉說話，模型就給咧嘴笑，表情寫得再具體也一樣；
要求只露側臉時又把人轉正、方向反，背景還長出整片金黃稻田。成片原本沿用 fix1 9341211（得意冷笑）。這輪不再跟臉拚：

| 項目 | 做法（英文原句在 `mkspec.py`） |
|---|---|
| 臉 | **不送臉部圖**（portrait、angle-a 都拿掉）、**不點名**：身分句換成服裝句（深金團花交領錦袍、寬袖、黑腰帶、高圓黑帽）；整段沒有臉、嘴、眼、說話的字（`mkjobs.py` 掃描擋） |
| 動作 | 第一格起寬背正對鏡頭；第一秒右袖往旁後一甩，之後快步沿田埂往右邊大柳樹走遠；聳肩、握拳、頭朝前（「背對」寫在構圖與動作兩處） |
| 台詞 | 說話句拿掉；成片 `voice_off` s32、鋪錄音 `zq934a31-p80`（錄音 README：用錄音就用 -p 版本），`line_at` c0.40（「哼」落在甩袖上） |
| 背景 | 場景圖 `set-hantian-liu-l1` **免費裁成左邊 940 px**（`fix4/set-hantian-liu-zuo.png`：犁溝乾田、遠山、大柳樹；裁掉樹右邊那片金黃熟田——fix2／fix3 的金黃稻田就是從那裡長出來的） |
| 精修 | `refine-prep.py` 在「never the mood. 」切動作段，所以保留一句「The picture fixes the place and its light only, never the mood. 」；動作段不用 `seen only from behind`／`back to us`（`e934refine.sh` 第 3 步只准 s05 s06 有） |

## 檔案與指令

```
python3 -I mkspec.py                                    # 1 shot -> spec.json (16 s)
python3 -I mkjobs.py <live>/fix4                        # 掃描 0 命中；colab-jobs.json 2 支、16 秒
python3 -I ../../_scripts/preflight-prompts.py <live>/fix4/colab-jobs.json                        # 0 error(s), 0 warning(s)
python3 -I .agents/skills/minimax-h3-colab/scripts/check_manifest.py <live>/fix4/colab-jobs.json  # 0 error(s), 0 warning(s)
bash .agents/skills/minimax-h3-runpod/scripts/h3r.sh check --manifest <live>/fix4/colab-jobs.json # 0 error(s), 0 warning(s)
bash scratchpad/e934f4.sh                               # Colab zt-live3，跑完 ONLY_SELF 釋放
PREP=1 ONLY=s32 bash scratchpad/e934refine.sh          # 讀檔順序 picks-merged → fix1 → fix2 → cut-trims → review3-trims → fix3 → fix4
bash ../e934cut.sh
```

`<live>` = `/root/mokaair-work/videos/zhong-tian-qu-qi-e934-dh/runpod/live`。種子 9341511／9341512（`93415xx` = fix4，`e934refine.sh` 的 SRC 表已有 `15`）。

## 結果（2026-11-20）

- **跑**：05:16–05:26，2/2 一輪完成，ONLY_SELF 釋放 zt-live3；351.15 → 350.43 CU（0.72）。當時另有一台記名的 zt-live2（別的 session 的），沒碰。
- **挑片**（`review-picks.tsv`，scratchpad `e934f4/pick/`：每 0.5 秒整格、每 0.25 秒頭部放大）：**9341511**，0.000–7.000。
  兩支都做到：全程背影、沒有一格見到嘴或正臉（1511 在 0.25–1.5 秒頭微偏右，只見右耳與一點頰邊）、甩袖、走開、乾的犁溝田＋垂柳＋遠山，沒有金黃稻田。
  選 1511：柳樹跟 s30 1415、s31 一樣是垂柳，甩袖 0.5–1.0 秒剛好壓在「哼」上。1512 樹畫成團狀，甩袖晚 0.5 秒。
  **比 fix1 9341211 好**（那支整鏡得意咧嘴笑，聖經寫 NOSMILE），所以換。
- **精修**：`PREP=1 ONLY=s32 bash scratchpad/e934refine.sh`，40 鏡核對全過，只送 s32；舊精修（9341211）移到 `refined/old/s32-9341211.mp4`；
  新精修 1312×736、192 格，背影保持（每 0.25 秒看過）。`.seed` 由 progress 檔補上。350.43 → 348.31 CU（2.12）。跑完 0 assignments、沒有 `[?]` VM。**fix4 合計 2.84 CU。**
- **剪接**：`zq934a31.wav` 換成 `zq934a31-p80` 整平到 −13.6 LUFS（`lev934.py`，原檔在 `audio/orig/`）；`voice_off` 加 s32、`line_at` zq934a31 0.40；
  甩袖 swish-7 c1.0→0.45、腳步 c2.2／3.0→1.3／1.9（scratchpad `e934r3/params.json`，舊的在 `params-r3.json`）；`e934cut.sh` 的 want／seed 表與錄音清單照改。
- **成片**：`/root/mokaair-work/videos/_live-e934/zhong-tian-qu-qi-e934-dh/cut/e934-live.mp4`，**232.75 秒**（REVIEW 3 233.25）、−14.0 LUFS、LRA 5.4、峰值 −3.7 dBFS（loudnorm2 線性）。cut-qa 只剩刻意的 held s40 1.00 秒與 black 1.04 秒、jitter 39 鏡 ok、motion 8.2／static 10%；cut-jumps 0；audio-qa 40 句 0 問題。s32 錄音在成片 f0 120 Hz（s30 原聲 128），momentary −11..−17。
- **聽寫**（scratchpad `e934f4/fwcut-f4.txt`）：40 句都在、帶提示全對；a31 單聽一字不差。
- **人耳／人眼**：背影鋪錄音讀不讀得出氣走；錄音（a31-p80）跟 s30 原聲像不像同一人。剪接表 `_note` 第一段（FIX4）同步寫了。
