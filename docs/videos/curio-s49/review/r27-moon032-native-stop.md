# S49 R27｜`moon032` 原生單張退件與停批

2026-10-22 UTC。**`moon032` 機器 PASS、人工 REJECT；R27 `moon033–039` 未開畫。** 此次是在 [R27 非作者書面 PASS](r27-moon032-033-prompt-independent-pass.md) 和[私人圖單安全重綁](r27-moon032-033-offline-manifest-rebind.md)之後，只對 `moon032` 做一次 MiniMax image-01 原生圖及一次 judge。人工直接看了 1280×720 原圖和 1280×720 自動裁圖，未用 `--accept-best`。

## 前置檢查與這張圖

- 固定 `video.json` SHA-256 `02fdb0f2ac142634d42ac24f7108bb12424e7a4625756ca559b90d52912552a3`、`claims.md` `779a8e22e6e7e202249cf7ec645a91a7ade7139c5c0e6ee2bb70c4fa50f2bd2f`、`script.md` `82369f762cc64f70e300e2104a16af3b8e99f1e3296dd81a34152e967f0ecb0a`；圖單 `visual_hash=74c5cc0713c7766d`、起始 SHA `694b319ccaaf0da0e4ed9079620945b6b95588c5a95439ec2f89d8f5d8607615`。26 張先前 KEEP 的選圖實檔 SHA 逐張吻合；`STOP` 存在、`media/jobs.json` 為 `{ "jobs": {} }`、0 預約。單張費用 US$0.0135 加在 US$1.0260 後仍低於整集 US$5.30。即時 `media-status` 顯示 MiniMax image-01 已設定，配額餘 10,092 image／8,653 judge；dry-run 的兩提示詞在 1,500 字元限制內，兩張若各一 take 估約 US$0.03。
- 受控命令只指定 `--shot moon032 --takes 1`。原圖私人路徑 `keyframes/moon032-1.jpg`，SHA `c63ee5206a89da0b70bd3be197ae9f30beeae38785389a32bad05e131d4a456b`；自動裁圖 `keyframes/moon032-1-trim.jpg`，SHA `01a381eea30c4b5293d63ff6b074cc31471d0cf64cfaaf9560c3026f3bbfc7cc`。兩檔都是 1280×720，原圖／裁圖和 CLI 前後圖單、帳本均留私人 `review/r27-moon032-033-native/`；逐項機讀紀錄見[清單](r27-moon032-native-stop-inventory.json)，其 SHA-256 為 `0f78ad96a6b4b27e597230a050166d0f3d9329a7501a460d6b116c4dcd41a91b`。
- 機器評 9.29／10、`passed=true`，只提及木椅變矮凳和百葉窗缺失。**人工 REJECT**：成年灰髮人物從一個延伸到地板的門口探出身，並非從**高處有百葉的開口**示意向下照入暗室；裁圖後仍是落地門框。右方普通日光與暗牆不構成旁白所說「高處物鏡 → 暗室焦像」可理解的空間關係，也不能拿日光冒充實際物鏡成像證據。未見 R26 的紅頭現代器材或六格偽圖，但這次仍未通過 [R27 紙審的原圖驗收重點](r27-moon032-033-prompt-independent-pass.md)。

## 停線與保全

觀察到關鍵史料畫面關係再次失效，即按預定規則停批；**R27 `moon033` 無請求、`moon034–039` 無請求**。CLI 曾把退件裁圖寫進私有 manifest，並產生兩張含退件的 contact sheet；保存 CLI 後圖單 SHA `fd11e717fb0b886d36932a10a45eff25d5c124d7125eb389d40398ea3978a978` 與原圖、裁圖、機器圖頁作證後，在 STOP 下把 26 張 KEEP 的 R27 前圖單逐位元恢復，現行 SHA 再次為 `694b319ccaaf0da0e4ed9079620945b6b95588c5a95439ec2f89d8f5d8607615`。因此現行圖單沒有 `moon032/033` 條目或退件請求鍵，`contact_sheet=null`、`contact_sheets=[]`；機器圖頁移到私人 review 目錄。26 個 KEEP 條目與現行所選檔案 SHA 不變，`moon031` 仍由來源大字卡輸出，沒有退件選圖可被 render 引用。

結束 ledger SHA `076a31adf1dd34d89a11ecc9a18c819bbaa7bec3164b56098fb1d5db4ebb9275`，**US$1.0395／77 image／77 judge／0 預約**，本輪只增加 US$0.0135；`STOP` 已恢復，jobs 仍空。`keyframeProblems` 對 26 張 KEEP 為 0；對完整 R27 則仍有 **94 張未畫**，含 `moon032/033`，因此不能送 storyboard 或宣稱本集完成。下一步限 `moon032` 的書面畫面修復及另一人獨立覆核，再判斷是否重試；先前 R27 紙審 PASS 不能代替原圖 KEEP。網站卡、人耳審核、片頭片尾、成片與 Studio 連結仍待。
