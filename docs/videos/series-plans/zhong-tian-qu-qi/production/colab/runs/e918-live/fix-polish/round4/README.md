# 第 18 集（e918）第二波重拍（round4）：s31

2026-11-22，照 `review-zt/WAVE2-BRIEF.md` 與 `WAVE2-CANDIDATES.md`。種子 9189401／9189402，兩支 960×544 Ref2VA、各 8 秒。
`python3 -I ../../../_scripts/polish-build.py 18 4` 寫出 `runpod/live/fixp4/`（2 支、16 秒）。只寫提示詞，沒送出任何工作。

| 鏡 | 錯在哪 | 改了什麼設計 | 圖 | 拿不準的 |
| --- | --- | --- | --- | --- |
| s31（B） | 三人面向鏡頭排排站；錢員外站著告狀（稿子是跪著一拜）；許硯腰上掛白布袋 | base `d1/.../ref-s31-9181101`。改堂上側拍：全員朝畫右的公案（畫右緣只露案的深色前角，縣令在上緣外，稿子本來就不入鏡）；錢員外在畫中跪著、背對我們四分之三、臉朝公案看不到（台詞本來就是錄音 a30，`voice_off` 有 s31，接 s37 的跪姿背影）；許硯、唐小棠在左邊側面站著、嘴閉。一個動作：錢員外往前一拜再直起。拿掉 base 的「胸前鼓包、領口一角暗紅綢」（白布袋的來源），腰帶寫平 | 從 7 張減成 4 張：`xuyan-angle-a-l1`、`tangxiaotang-angle-b-l1`、`qianyuanwai-angle-b-l1`、`set-xianya-gongtang-floor-l1`（拿掉三張正面定妝照與錢員外、唐小棠的另一張角度圖） | 候選清單寫「錢員外跪在畫左、縣令在畫右」；我讓縣令不入鏡（多一個有名字的人會分身），錢員外跪在畫中、許硯與唐小棠在左，跟 s33 許硯往畫右指錢員外同一邊。錢員外的側面圖臉朝畫左，正文要他朝畫右背對，模型可能轉回來。暗紅綢角這鏡看不到（第 9 項另有處理） |

## 檢查（2026-11-22）

- `polish-build.py 18 4`：1 鏡、2 支、16 秒
- `preflight-prompts.py …/fixp4/colab-jobs.json`：0 error(s)、0 warning(s)
- `h3r.sh check --manifest …/fixp4/colab-jobs.json`：0 error(s)、0 warning(s)
