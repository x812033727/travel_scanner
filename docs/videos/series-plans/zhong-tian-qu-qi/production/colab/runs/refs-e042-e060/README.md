# 第 42–60 集的定妝照與場景圖：每一輪送了什麼、留了什麼

`h3.sh images` 實際送出的 manifest（`roundN-*.json`）與 `progress*.json`（每張的 seed、時間、失敗原因）。工作資料夾的
`_series/zhong-tian-qu-qi/refs-paint/`；通過的才複製進 `assets/refs-dh/`。教訓寫在 skill `minimax-h3-colab` 的 `lessons.md` §9。

| 輪 | manifest | 結果 |
| --- | --- | --- |
| 1 | `round1-refs.json`（image 1 = 刁七、祠堂；9:16） | 全部不用：臉與光腳抄刁七，場景長出亂碼匾額 |
| 2 | `round2-refs2.json`（image 1 = 鄭伯、州城書院門口；空白匾額句） | 場景圖 12 張通過（另 4 張重抽一次，見 `progress4.json`）；定妝照構圖是全身、質感偏卡通，站主要求跟原本的定妝照一樣，作廢 |
| 3 | `round3-refs3.json`（image 1 = 趙捕頭、3:4 胸像） | 褚知府通過；杜鐵抄了趙捕頭的臉 |
| 3 試 | `round3-trial.json`（「Replace the man in image 1…」） | 人對了，但又是全身 |
| 4 | `round4-refs4.json`（`progress7` 被 HF 429 打掉，`progress8` 重跑） | 兩步的第一步（8 人）與杜鐵的第二步：杜鐵通過 |
| 5 | `round5-refs5.json` | 第二步：程山長、馮學正、魏珣、鄧押司、冷鐵通過；常公公留著第一步的白鬍子；州城酒肆重抽通過 |
| 6 | `round6-refs6.json` | 常公公：以第五輪的圖為 image 1、`latent: image1`，只剃掉鬍子 |

第二步的 image 1 是第一步那張圖裁下胸口以上（全身圖取 `crop=624:832:312:0` 再放大到 1248×1664；馮學正、常公公第一步已是胸像，整張用）。

州城客棧（`set-zhou-kezhan`）、貢院（`set-gongyuan`）、許大郎、周員外沿用另一個 session（本機 RunPod）為第 42 集畫的版本，
同一張圖才連戲；本輪畫的這四張不進 repo。
