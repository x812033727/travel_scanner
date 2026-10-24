# S53 R25｜`s53023` 最後一次原生圖前的獨立書面覆核

2026-10-22 UTC。**PASS，僅限 `s53023` 的固定史料、126 句既定口播與 R25 書面畫面概念。**這不是 R25 成圖驗收，也不使舊圖單直接適用於新畫面版本；本次沒有產圖、judge、重綁圖單或付費呼叫。

## 獨立版次核對

我直接讀取 R24 Git commit `be4f68aa2b7ffed1bd1e39043ddc0574bccb1d5c`，並重新計算現行檔案與差分檔的 SHA-256：

| 檔案 | R24 Git | R25 現行 |
| --- | --- | --- |
| `video.json` | `07193188815a7b74529761f3a5c7c5656e9f1e954170b0bf71810cd9b17be1e9` | `0ca53d7d67a8601f20ae8473f5d8be0bf1389b720cd3a029cdbe446855a783c6` |
| `claims.md` | `267fdb63c5f2a36f479bdc3903f06e07a93a21a55659e570a7001b2920799dc7` | `67907db0a94cadd1e213a72995834a17537cc27f007c139ce29341ae37a02500` |
| `script.md` | `64ffcd8c0e89c4596a7fd08d41bd74f8a16f55fbc9acc2f41d7f9b914ea300fc` | `64ffcd8c0e89c4596a7fd08d41bd74f8a16f55fbc9acc2f41d7f9b914ea300fc` |

`review/r25-s53023-last-prompt-structured-diff.json` SHA-256 為 `44457268723f09e4134b6bbc2b617a459e78d3ce39ec587024f0ee0d4a626ab9`。獨立解析比較 124 景，唯一 JSON 值差異是 `scenes[17].data.prompt`；`claims.md` 132 行中只第 24 行 `s53023` 改動。兩筆舊／新值與結構差分逐字相符；把各自唯一的新值反填舊值後，兩個檔案均逐位元組重現 R24 Git 版。126／126 句口播的 ID 與文字完全相同，`s53023` 的 `camera=pan left`、`visual=still` 也未變。私人 `timeline.json` SHA-256 `c75c8bde15f7220862ba8083d6590b7b14bb71c456f896f7b58c13352c88a054`、`narration.wav` SHA-256 `08444d50c2f8b70a7079701e157397d9a7c23d08971727164df91a1101e281e1`。實跑 `VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s53 --json`：exit 0，**0 errors／0 warnings**，126 lines。

## 來源、時序與畫面界線

重開固定 1913 年 *San Francisco Relief Survey* 原文 `/tmp/s53-sf-relief/56217-0.txt`，SHA-256 `d627ed287d8a93b9c00225ea47dbdc4f97c36089a890192a602b993c3c185b72`。[G L4934–4941](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L4934-L4941)說臨時庇護多在公地；公園委員會無權正式准許使用公園、廣場，只在 1906 年 8 月 17 日同意至多一年不干預，之後小屋要儘速搬走。這直接支持「能否一直住下去」的問句。[D L4848–4870](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L4848-L4870)記錄 8 月 1 日公布建小屋計畫、9 月 10 日才開工、9 月 16 日漢密爾頓廣場先完工 20 棟。口播把本問句放在公布計畫與公地背景之後、開工之前，帳棚牆與紙上小屋構想符合這段時序。

R25 提示詞保留 1906 年舊金山公共廣場的定位，把主角縮為一位灰髮、有面紋、著深色便服的中年工作者，只露臉、肩與雙手；視線落在下巴下方手掌大小的無字折紙及兩個低矮小屋屋頂線條。背景是一面素色帆布帳棚牆，沒有建成小屋。固定史料沒有記載這位工作者、這張圖紙或該牆的具體配置；`claims.md` 已把它們明定為匿名、原創的未建屋概念示意，並排除存世平面圖、具名個案及當時已有完工小屋的主張。單一牆面本身不會交代廣場全貌，但相鄰 `s53021` 的公地廣場畫面和本句旁白提供場地脈絡。這個近景畫法可作來源誠實的**概念插圖**，不能在成圖或說明中升格為歷史文件。

系列規則要求 `look.preset=cute-mystery`、提示詞只寫景別／時地／一人一事／物件／光，不往 `look` 或提示詞加畫風字。現行 `look` 只有該 preset；R25 是一人看小紙圖，柔和陰天光、無可讀文字，未新增 `style` 或 `negative`。我直接看了 R24 未裁 1280×720 原圖 `keyframes/s53023-1.jpg`，SHA-256 `89933b6bd946a338e219566e0947e0f7518cfcc0a25a36556cb18383409b3345`：成年人與帳棚有呈現，但人物全身跪坐、背景偏攝影、手中紙上是有樓層的高屋。R25 的近景、單一帆布牆與低屋頂小折紙正對這三項失配；文字無法保證模型實際遵守，仍須驗未裁新原圖。

## 私有媒體停線與判定範圍

只讀重算有效 `keyframes/manifest.json` SHA-256 `798d0dc76304105bdb48b8217e000474c977df39cf22789024182d1d3fb17acf`；其 `visual_hash=2b988530521f84c1` 仍是 R24，14 筆 KEEP 的所選實檔全數符合各自 SHA，沒有 `s53023` 條目。現稿 `visualHash=a455331f94170433`，故圖單尚未綁 R25。`media/ledger.json` SHA-256 `338ed794a92101008aebd588edb6bdb87e513dbe72d31bb3da89fcdf91e8a1e9`：逐筆合計 **US$0.4995，38 image、37 judge**；`media/jobs.json` SHA-256 `a9d2c69ab3cb5704417b4f0968a7d8d0dae6eb0e35d37e053463220b30d55ca3` 且 jobs 空；私人 `STOP` 在位。

**書面 PASS 的範圍到此為止。**若後續安全離線重綁、即時額度預檢均通過，`s53023` 也只餘第三／最後一張原生圖可驗；其成年身分、近景、低小屋草圖、非攝影畫風及未建屋時序須由原尺寸圖與 judge 另行判定。第三張若不合格，不得以本紙審 PASS 當 KEEP，也不得購買第四張。
