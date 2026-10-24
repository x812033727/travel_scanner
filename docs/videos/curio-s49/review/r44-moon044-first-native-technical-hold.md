# S49 R44｜`moon044` 首張原圖黑邊技術 HOLD 與 34 KEEP 停批

2026-10-22 UTC。[R40 紙審精確適用性](r44-moon044-r40-paper-applicability.md) SHA-256 **`6ddaf058241042f3eb0d2e82edf537e06e0415f3666b38427314936e464361cd`** 已由非作者判 **PAPER PASS**。受控只買 `moon044` 一張 MiniMax 1280×720 原圖與一個 judge，沒有買 `moon045`。機器 **9.71／10、`frame=0`、NOT passed**：原圖頂端與底端有全幅黑邊；CLI 雖自動裁去約上 8%／下 7.6% 的紙邊，所選裁圖的 judge 結果仍是對**原圖**的黑邊退件，manifest 標 `needs_review=true`。S49 是 `format: drama`，工具明確禁止 `--accept-best`；本輪**不手改 manifest 或把技術失敗冒充正式 KEEP**，先停在 34 張已驗收圖。

## 守衛與原圖

付費前凍結 `video.json` SHA **`dd2dae850cdf455a01b9c99a01af2d9ef3370d81d11c7349f661d6a6220f8d9c`**、`claims.md` SHA **`70f0d9255397880586c96a49cbda77cf3ca722b68815455f29b6ac9f841c2ebb`**、R44 來源字卡和 `moon044` 非作者紙審。私人 manifest SHA **`5fe354f8fecc7d0d41922214fe0d0517616bf6ed651c7a07f3f926e8aa2f7a9f`**，34／34 KEEP 入選實檔 SHA 相符；STOP/jobs 空，ledger SHA `b6ba6f57fd69c85743396c7eaaf333c80057dc0c633a11d8b7bd663c5b39a850`、**US$1.2960／96 image／96 judge／0 預約**。新鮮服務報價 MiniMax `image-01` 每張 **US$0.0035**、judge **US$0.01**，月額餘 **9,873 image／7,890 judge**；提示詞只讀 dry-run **210／1068** 字元、server ready。即使餘下 82 張各試三次另留 US$0.15 配樂，估 **US$4.767**，低於本集核准 US$5.30。只為本張暫解 STOP，執行 `keyframes --shot moon044 --takes 1` 一次；exit **1** 後 trap 已恢復 STOP，實收一 image／一 judge。

未裁原圖 `keyframes/moon044-1.jpg` SHA **`953ee0d75c8f0c033dd80460dd3a01a1122a64ee8710ada39b3ad375d08db223`**；機器暫選 `keyframes/moon044-1-trim.jpg` SHA **`a86d16982330409a164f6e7d8112626be67c8589bdc80161889730ff8913174f`**。兩張均 1280×720。完整原尺寸目視及逐列像素檢查：原圖 y0–50／y669–719 都是全幅近黑邊；裁圖的頂底每一測試列**沒有**全幅近黑區，邊緣已被去除。人物是灰髮、有面紋的成年工匠，穿普通長袖工作衣和圍裙，雙手扶空圓模朝內看，左側柔光像爐火；沒有完工鏡片、真赫歇爾器材、可讀字、顯著現代道具或 3D 畫風。作者判**原圖因黑邊 HUMAN REJECT，裁圖僅視覺內容 HUMAN KEEP**；[非作者原尺寸審圖](r44-moon044-first-native-independent-visual.md) SHA-256 **`fac9f40b10266986fc946e8dfaccf120f21b93a6745fff6aece7ebf6c53e838e`** 亦分別判黑邊與裁圖內容。兩個人眼結論都不能改變機器 `frame=0`／drama 工具閘門，所以本景仍是**技術 HOLD**、不計第 35 張 KEEP。

## 私人恢復與下一步

在 STOP/jobs 空下封存失敗的 35-entry manifest SHA **`8798fc406f8f737536a327c2a3ffa61d9d8bac8d5c2949962a5f37a0559b8533`**、原圖、裁圖、帳本、兩張 contact sheets、執行 log；再把事前 34-KEEP active manifest 與 contact sheets 逐位元恢復。現 active manifest SHA **`5fe354f8fecc7d0d41922214fe0d0517616bf6ed651c7a07f3f926e8aa2f7a9f`**；先前 34 張完整項目與實檔 SHA 都不變，[STOP 庫存](r44-moon044-first-native-hold-inventory.json) SHA-256 **`9218a196e8aa4f9dade2e95f67cb73d3fff6bc0485e5c27d0792bbaa07c8d5b1`** 記原圖、裁圖和選檔。Ledger 現 SHA **`2608c9b2690253b72dc2f200b8dd80ed7c5721662914c41bf7139f6db6dd8ead`**、**US$1.3095／97 image／97 judge／0 預約**；STOP 在位、jobs `{}`。完整私有證據位於 `/workspace/.video-work/curio-s49/review/r44-moon044-one-native/`，不提交圖像、權杖或暫用裁圖。

下一步只對 `moon044` 做**黑邊窄修**，明示滿框、邊到邊、不得有上下黑色影像帶；成熟工匠、空鑄模、虛構來源和其他 128 景／131 句保持。先凍結可逆差分並交另一人紙審；PAPER PASS 前不重綁、不買第二張，更不開 `moon045`。若重現黑邊或內容違背固定來源，立即停批再評估來源字卡；整集 storyboard、網站聽音與成片仍 HOLD。
