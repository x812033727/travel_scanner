# 第 1 集：Colab 先畫首格再 H3 片段（票 `2026-10-28-1-colab-qwen-image-edit-2509`）

站主 2026-10-28：「在 Colab 先畫首格再 FL2VA」。小樣三鏡（s33–s35）的首格用站上的 Gemini 3 Pro 畫；其餘的首格在 Colab 的
GPU 畫，再用同一條 Colab 路線跑 H3 片段（`../README.md`）。進產線靠 `keyframes import`（PR #1910，`docs/videos/DRAMA.md`
「外面畫的首格」）：每張 `--judge` 用站上 judge 對設定圖驗一次（US$0.01），過了才是這一鏡的關鍵影格。

## 模型與做法

- **Qwen-Image-Edit-2509**（Apache-2.0，`QwenImageEditPlusPipeline`，一到三張輸入圖最準）：參照圖＝該鏡角色**選定的設定圖**（江小滿 B、沈照雪 A、宋管事 F）＋同一場已通過 judge 的關鍵影格當**場景參照**（`--set-ref s34`：茅屋）；沒有人的插鏡拿它當風格參照。
- A100 40 GB 放不下 bf16 的 transformer（約 41 GB），所以 transformer 以 bitsandbytes 8-bit 載入、其餘元件 CPU offload（`first_frames_colab.py`）。
- 取樣：profile `lightning`（Hugging Face 有 `lightx2v/Qwen-Image-Edit-2509-Lightning` 的 8 步 LoRA 就掛，8 步、true CFG 1.0），抓不到就退回 40 步、true CFG 4.0（`base`）。
- 畫布 1312×736（H3 首格的畫布，`motion-quality.md` 第三節），seed 寫在 manifest。

## 檔案

- `gen-first-frames-manifest.mjs`：從 `video.json`（prompt 用產線 `keyframes` 同一個組法 `shotPrompt`）、工作目錄的設定圖選擇與關鍵影格 manifest 產生 `manifest.json`（整集 45 鏡）與 `manifest-pilot.json`（`--shots`）。參照圖是工作目錄的絕對路徑，不進 git。
- `first_frames_colab.py`：在 Colab kernel 裡跑的腳本（裝 diffusers、載模型、逐鏡畫圖、打包成 tar）。
- `ff_runner.py`：本機驅動（打包 → `colab new` → `upload` → `exec` 一格 notebook → `download` → 解開 → `stop`），`progress.json` 記每一步。

```bash
export VIDEO_WORKDIR=<dir>
cd docs/videos/series-plans/xiuxian-jiangli/production/colab/first-frames
node gen-first-frames-manifest.mjs --shots s25,s26,s32 --set-ref s34 --out manifest-pilot.json
bash ../../../../../../../.agents/skills/minimax-h3-colab/scripts/h3.sh usage      # 抄餘額
python3 -I ff_runner.py --manifest manifest-pilot.json --out $VIDEO_WORKDIR/xiuxian-jiangli-e001/ff-out-pilot --profile lightning
bash ../../../../../../../.agents/skills/minimax-h3-colab/scripts/h3.sh usage      # 再抄一次，前後差寫進收據
# 進產線（每張一筆；--judge 站上驗）
node tools/video/cli.mjs keyframes import --slug xiuxian-jiangli-e001 --shot s25 --file $VIDEO_WORKDIR/xiuxian-jiangli-e001/ff-out-pilot/s25.png --provider colab --judge --credits <CU> --note "qwen-image-edit-2509 lightning 8 steps seed 1 refs=2"
```

## 小樣看什麼

臉跟設定圖同一個人（judge 的識別題）、場景跟 s34 同一間屋、畫風同 Gemini 的三張（3D 國漫、冷色暖光）、手與道具沒壞、沒有字。
站主看過三張再畫整集；不過就換模型（FLUX.1 Kontext、Gemini）或改參照。

## 收據

### 第一次真跑（2026-10-28 07:48–08:16Z，小樣 s25、s26、s32）

| 項 | 實測 |
| --- | --- |
| GPU | A100-SXM4-**80GB**（不是 40 GB；下一批 bf16 直接上 GPU） |
| 裝套件＋載模型 | 212 秒（含從 Hugging Face 抓約 45 GB） |
| 取樣 | LoRA 的 repo 名錯（`lightx2v/Qwen-Image-Edit-2509-Lightning` 401），退回 40 步、true CFG 4.0；8-bit transformer 加 CPU offload |
| 每張 | s25 416 秒（2 參照）、s26 537 秒（3 參照）、s32 408 秒；GPU 總共 1,601 秒 |
| compute units | 998.18 → 995.22，**2.96 CU／3 張**（含冷啟動） |
| 畫面 | 場景跟 s34 同一間屋（參照有效）；**人物沒守住**：s25 江小滿的臉變成誇張卡通臉、構圖被切、把參照裡的沈照雪也畫進只有他一人的鏡頭；s26 少了江小滿；s32 畫成沈照雪拿米袋（該是江小滿）。畫風偏一般 3D 動畫，不如 Gemini 的三張像國漫 |

結論（交站主）：以這個設定，身份一致性輸 Gemini 3 Pro 很多，judge 的識別題會擋。要再試就改三件事：bf16 上 GPU（已改）、掛正確的 8 步 LoRA
（`lightx2v/Qwen-Image-Lightning/Qwen-Image-Edit-2509/…8steps-V1.0-bf16`，已改）、場景參照換成**沒有人的**關鍵影格（s33 的灶）並在 prompt 裡
把「Picture 1 是誰、Picture 2 是誰、Picture 3 是場景」寫明。一輪三張約 5 分鐘、不到 1 CU。
