# S49 R35｜`moon036` 來源卡重綁、`moon037` 童貌退圖停批

2026-10-22 UTC。**R35 只買 `moon037` 一張 1280×720 原生圖與一個 judge；機器 7.88／10 PASS，原尺寸人眼裁決 REJECT，`moon038–039` 未開畫。** 先前的 [R35 非作者紙審](r35-moon036-source-card-independent-paper.md) SHA-256 `8e93f730c9953c3eaa902a92fc40baee61c95a556c454bfa22dd965cbf656d2c` 准許 `moon036` 改用標明虛構對話的來源卡；[R26 非作者紙審](r26-next-chapter-eight-prompt-independent-pass.md) SHA-256 `9224ac098475dde5dd7e63c66c19acaa28d7faf85e3a7ea0ee7bddbe584480a2` 則要求 `moon037` 畫兩名成年人從木椅起身應答，明列少年形象為退件條件。`moon037–039` 的完整 scene 和 claims 行仍與 R26 紙審稿逐項相同。

## 離線重綁與付費前守衛

R35 精確文稿 `video.json` SHA `fe4e3c2b3fd6691fa467d253965b4efa8c44c870582159fe110160dd16b029c3`、`claims.md` SHA `824d15a121e9ca7ae147acfe60e1fa92e4e6aa871e70c788f9606c0750b0da79`、未改 `script.md` SHA `82369f762cc64f70e300e2104a16af3b8e99f1e3296dd81a34152e967f0ecb0a`。STOP 在位、jobs 空時，將 R34 29-KEEP manifest SHA `d1937dac303f4d5dd82ddcb1a4f5b6c5e797bcfba47ea25ad25d89697df2bd36` 位元備份至私人 `rebind-backups/r34-manifest-before-r35-moon036-card.json`，僅把 `visual_hash=1c3c268eca8111e4` 換成 R35 `87f0c570cd6211b0`；`look_hash=98a370ae40badbaf` 與 29 張既收完整項目及所選實檔 SHA 均不變。付費前新 manifest SHA **`8fa67b2e39426dcc5b98220624ec17096cad69444d37a6c870465de1b40c8ff4`**，`moon036` 保持來源卡、無退圖選檔；`keyframeProblems` 僅 **89 張未畫**、其他 0。

即時 `media-status` 回報 MiniMax `image-01` ready、圖片餘 10,010、judge 餘 8,337；`moon037` 只讀 dry-run 提示詞 304／1071、服務 ready。帳本付費前 US$1.1340／84 image／84 judge／0 預約，預估一圖一 judge US$0.0135，低於整集 **US$5.30** 上限。守衛核精確文稿與紙審 SHA、STOP/jobs、29 張實檔與圖單／帳本 SHA 後，僅為 `moon037` 暫解 STOP 執行一次 `keyframes --slug curio-s49 --shot moon037 --takes 1`；退出時立即恢復 STOP。

## 原尺寸裁決與位元恢復

原圖 `keyframes/moon037-1.jpg` SHA **`41e41c41e07f017a2c20675ce04d2c9584ed66a578ef7b823fa57f514cbe5553`**，1280×720，無入選裁圖。機器 7.88／10 PASS，但 `awkward=4`，指出左側人物半蹲、木椅偏小。整合者與另一位獨立盲讀者看完整原圖，均判 **HUMAN REJECT**：左側從木椅急起、張手面向右側的動作可辨，室內木家具與外套也接近年代示意；但兩人圓滑面孔、大眼、紅頰與短小身形讀成少年，坐著的右側人物尤其明顯，不能作為 R26 明確要求的兩名成年 1830 年代人物。此圖只對應固定史料中**虛構** Brewster 的反應，沒有冒稱真器材或史實會面。

保留一位獨立審看者的 **KEEP 異議**：他認為兩人年齡尚有歧義，右側高領衫、背心與靴子可讀成年民服，左側半蹲是起身過渡姿勢。最終裁決仍採 R26 紙審的明文少年退件條件，沒有把機器 PASS 或服飾線索視為成年人證據，也沒有隱去異議。

[機讀庫存](r35-moon037-native-stop-inventory.json) SHA-256 `b650758974c842bd4abad883359af5fc615cc9e7f1731c1779e6aaa60975b8e3` 逐張核 29 KEEP 所選檔案及實檔 SHA，列原圖、機器圖單、帳本與異議。私人 `review/r35-card-next-native/moon037/` 封存原圖、兩張 contact sheet、前後 manifest／ledger、CLI stdout／stderr／exit。機器曾把退圖選入 manifest SHA `5cb129630775b11a22a5dc94e2d8143178449f5853a7d30e99f6ebb880565c45`；STOP 下把付費前 **29-KEEP manifest 逐位元恢復**，並從 R32 KEEP 私人封存覆回兩張 contact sheet。現行 manifest 再為 **`8fa67b2e39426dcc5b98220624ec17096cad69444d37a6c870465de1b40c8ff4`**，不引用 `moon037` 退圖；`keyframeProblems` 僅 **89 張未畫**、其他 0。

帳本保留真實付款，SHA `91c21846627fffc589d57187fb7a39fb3e07bccd1ee1acc1e2a1a8c6e1c8913a` → **`dd9b74f40ece0c756800fa4de3a6a70fc4e162bedac4ab87fa6af255b43ed87b`**，US$1.1340／84 image／84 judge → **US$1.1475／85 image／85 judge**，0 音樂、0 預約；STOP 在位、jobs 空，低於 US$5.30。`moon038–039` 本輪零付費；先針對 `moon037` 成年外觀做有界書面修復與非作者紙審，再決定是否重試。全片 storyboard、站主卡／人耳、開頭片尾動畫、Short、成片與連結仍待。
