# e928-live 成片獨立審查（第 28 集真人版，第 3 篇章，第 1 位）

- 審查者：沒有參與製作的獨立代理，2026-11-17。只寫這份檔。沒有改剪接表、`picks.json`、片段、錄音、`e928cut.sh`，沒有用 Colab、RunPod 或任何付費服務，沒有 commit，沒有看另一位審查者的檔，沒有碰 e929、e930 的檔。第 27 集的成片已不在磁碟上（`_live-e927` 已清），接戲照 `e927-live/cut-review.md`、`cut-review-2.md` 與本集稿子〈這集接在哪〉的文字對照。
- 照 `_scripts/independent-review.md` 的成片審查做，格式照 `e927-live/cut-review.md`。
- 審的片：`/root/mokaair-work/videos/_live-e928/zhong-tian-qu-qi-e928-dh/cut/e928-live.mp4`
  - 200.30 秒，1920×1080，24 fps；mov_text 字幕 32 條（a12 只在面板）；41 鏡全用，鏡起點照 `cut/final.log`；s39 的 196.29 起黑到片尾，是刻意的結尾（鑼響完）。整片 −14.0 LUFS、LRA 5.6（我用 `ebur128` 重量，跟 `_note` 一樣）。
- 對照：稿子 `docs/videos/zhong-tian-qu-qi-e028-r2/script.md`（以〈真人版的改動（2026-11-17）〉為準）、剪接表 `production/hailuo/edit-dh-e928-live.json` 的 `_note`、挑片紀錄 `e928-live/{picks-merged,review3-trims}.tsv`、`fix1/review-picks.tsv`、聖經 `production/r2-bible-e021-e030.md`。
- 已接受、不再列（協調者清單）：s09／s17 賴三站著沒跪；s03b 跪倒原因弱；s03 棍落點離她兩步；s04 棍身竹節；s05 握手；笑場 s13／s17／s19／s20／s30；s22 看鏡頭與木盒；s32 黃紙淡線；s33／s39 高角度；s27 食盒像木桶；驚堂木是長板；s29 賴三沒頭巾；s34 丸子中空；s39 群眾單指；s15b 看手腕；s02 鞘頭；s31 手臂偏長；s26 許硯手上的小油燈。
- 做法：
  - 每鏡每 0.5 秒一格總表 `sh/sNN.jpg`（400 寬，標成片秒數與鏡內秒數 c）；原尺寸裁切逐格 `z/`：s07 綁手每 0.625 秒 `z/s07-hands.jpg`、s06 全景 `z/s06-full.jpg`、s18 驚堂木每 1/24 秒 `z/s18-gavel.jpg`、s20 驚堂木每 1/12 秒 `z/s20-gavel.jpg`、s36 驚堂木每 1/24 秒 `z/s36-gavel.jpg`、s03 落棍每 1/24 秒 `z/s03-hit.jpg`、s03b 跪倒 `z/s03b-knee.jpg`、s04 落地每 1/24 秒 `z/s04-land.jpg`、s10 銀子落掌每 1/24 秒 `z/s10-silver.jpg`、s32 許硯的嘴每 1/8 秒 `z/s32-mouth.jpg`、s38 賴三每 0.75 秒 `z/s38-face.jpg`、s33 與 s39 台上 `z/s33-stage.jpg`、`z/s39-stage.jpg`、s37 左緣 `z/s37-edge.jpg`、s01 賴三 `z/s01-lai.jpg`。
  - 聽寫：scratchpad 的 `fw`（faster-whisper medium、int8、2 執行緒；ffmpeg → 16 kHz f32le → `np.fromfile`，一個視窗一個行程依序跑，`tools/fwc.py`、`tools/runq.sh`）：0–68.5、68–135.5、135–200.29 三段不給提示；每句帶上下文（上一句＋本句當提示、視窗從上一句起到本句尾）再聽一次，33 個視窗，變調的 s01、s05、s19、s20、s22、s36、s38 與錄音的 a06、a08、a14、a29 都在裡面；另聽 s32、s25、s38 單鏡與片尾 192.29–200.29、196.29–200.29（`w.txt`）。
  - 聲音：每句 20 ms RMS p75／最大值與 **YIN** 音高中位與四分位（`tools/lvl.py` → `lvl-f0.txt`，60–450 Hz、閾值 0.15、RMS 門檻 0.02）；任意區段 `tools/f0span.py`；20 ms RMS 全片 `rms20.npy`（16 kHz），音效處另用 48 kHz 解碼重算 20 ms RMS；賴三四句另算有聲格的頻譜重心（音色的粗略指標）。草稿 `d1/out/s32-9281102.mp4` 的原聲分句用 20 ms RMS 量。沒有存 wav，暫存 raw 用完即刪。
  - **量測的限制**：音高量的是混音後的成片（有配樂與底噪）；句的範圍照 `lines.json`；胡縣令四句 vf 0.06–0.19，中位數不穩。對嘴是 1/8 秒抽格對 20 ms RMS，標「不確定」的要人耳／眼。
- 抽格、量測：`/tmp/claude-0/-home-user/e6a64eea-98ea-5986-b96b-5cdbc5d1572e/scratchpad/e928/cutreview1/`。
- 時間：成片秒數；c 是鏡內秒數。

## 結論

（待填）
