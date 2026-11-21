# S60 R9｜最後四景正向簡化提示詞作者紀錄

2026-10-22 UTC。作者修訂，**等待另一位覆核者紙審，不宣稱獨立 PASS**。已閱讀 R8 第二輪原圖獨立覆核及親自查看四張目前原始 JPG。只修改 s60003、s60004、s60007、s60008 的 `data.prompt`；精確舊→新文字及 JSON pointer 見本輪 diff。

## 修訂與來源邊界

| 景 | 核心調整 | 固定史料支持與限制 | 次數 |
| --- | --- | --- | --- |
| s60003 | 全幅可見的三角帳門關閉，兩邊以明顯繫繩接合；成人站旁邊。 | Amundsen L13081–13083 明說離開時門牢牢繫合。等待者為匿名示意，不主張史料記下此姿勢；不先展示帳內。 | 已用 2，僅剩第 3 次 |
| s60004 | 只聚焦戴手套雙手與小張空白摺信，後方小帳與日光雪原。 | Amundsen L13064–13068：給國王的信留在帳內小袋。紙面、摺法與手勢為示意，空白紙不冒充原件內容；透過減少人物材質表現需求簡化畫面，既定 cute-mystery preset 原樣保留。 | 已用 2，僅剩第 3 次 |
| s60007 | 手持對向低太陽的開扇形黃銅六分儀，弧形刻度與短活動臂可見，聚焦雙手。 | Amundsen 測日定位章節及本輪既有獨立紙審支持對日測角；L13070 亦記六分儀。示意器材，不主張精確刻度／角度；保留先估位置、後觀測確認的敘事邊界。 | 已用 2，僅剩第 3 次 |
| s60008 | 信封半截進入布袋口，兩物件佔前景，帳內帆布與白冰。 | Amundsen L13064–13065：信放帳內小袋。信封、手套、插入瞬間為物件動作示意，不聲稱原信封形制或送達國王；旁白的收件懸念不變。 | 已用 2，僅剩第 3 次 |

固定來源 `/tmp/s60-verify-amundsen-4229.txt` SHA-256 `741b12f3e558a172bb03a1904df5479a130fd2208085b45c403911e71fdefe00`。來源定位沿用 [R8 獨立紙審](r8-independent-antarctic-visual-paper.md) 與 [R8 原圖覆核](r8-second-seven-independent-native.md)，並重新逐行核對 L13060–13083。

四景均保留南極白雪、南半球夏日；不加 style 或 negative 指令。四景提示詞變短並各只突出一個動作，不更動 preset、camera、lines、voice、script 或 claims。逐葉比較確認只有上述四個 prompt 變動；反套 diff 可逐位元組恢復原 video.json。

## 冻結版本與停止狀態

修改前已確認 private `STOP` 在位、`media/jobs.json` 為空 jobs；未移除 STOP，未呼叫付費工具、未修改任何媒體／manifest／帳本，未操作 Git。每景目前 2 次實際原圖，不因改詞歸零；最後一次失敗必須停止，不得第 4 次。

- `video.json` SHA-256 `67c40dcdc56373a9aff78f21743f67f41bae7aba296f8afd3681b7cf79061a7e`
- `script.md` SHA-256 `bf963ceec7e2f2bef79dc102a7b3ca89f4f6097b44e85907e5e98a2bea20531b`
- `claims.md` SHA-256 `21eab7637a46aebc28b7638d4bd720d08c7614d0aa78589d82a6d15034550edb`
- 修改前 video SHA-256 `21ceff1dbbab782674aa43e48156f9f1386a91a154c3e9d3e7eb97d600be0852`
- 本輪 diff SHA-256 `338de11a2a2fd764b6871790cfd5a0a607d90f0f4b4a7ee5104461cb493a6ff5`
