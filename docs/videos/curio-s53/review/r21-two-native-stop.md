# S53 R21｜兩景限額原生圖停線

2026-10-22 UTC。接 [R21 非作者紙審](r21-two-prompt-independent-paper.md) **2／2 PASS**，只對 `s53010`、`s53018` 各做一次 MiniMax `image-01` 原圖及正式 judge。兩次原生圖均未通過可用畫面關卡；本回**沒有**將第二章或整集分鏡判為完成。[逐圖雜湊清單](r21-two-native-inventory.json)綁原圖、裁圖、request key 與機器結果。

凍結的 `video.json` SHA-256 `4ac9a518d7387ea66918a89946636ee7dd6412f4926fbe7c5ccbb5a5a249f64a`、`claims.md` `02ee7918a362ce130bed4a9e2c1491f0da80880207d7c57d6aa9eae1820a3022`、`script.md` `64ffcd8c0e89c4596a7fd08d41bd74f8a16f55fbc9acc2f41d7f9b914ea300fc`，與紙審完全相同。試畫前 STOP、jobs 空，manifest SHA `75c59a8855284a3defe6f2acfd4f0c30bb52f344e1756bc29ef573cadfb5f1b7`，ledger SHA `c385ac8815a3ef7e3fa500c79dd1039ee6b9f21fc94bafc2c0c0deebd52c435b`，14 張既有 KEEP 條目與實際選圖 SHA 已私有備份。先以 `NODE_USE_ENV_PROXY=1` 做唯讀 dry-run，回 `image-01 ready`，兩張各一次約 US$0.03；正式命令各為 `keyframes --slug curio-s53 --shot <單一 ID> --takes 1`，每支只在 shell EXIT trap 期間移開 STOP，結束即恢復。兩支 CLI 的 exit 皆為 1，沒有第二 take 或背景待續 job。

| 景 | 原尺寸 1280×720 原圖與裁圖實看 | 判定 |
| --- | --- | --- |
| `s53010` | R19 現代車與 R20 長電桿街景已消失；畫面為銀髮成年住戶、木院牆及遠煙。原圖上下仍有黑色 letterbox，工具裁圖已去掉，但住戶在畫面右側、未佔大部分畫幅，且人物比例比首章已收的可愛大頭角色成熟。正式 judge **9／10 FAIL**，列 `details` 與 `frame`；現行 manifest `needs_review=true`。 | **HOLD**，裁圖有可用構圖元素，但不能把機器 FAIL 改寫為 PASS，也不能送分鏡卡。這是第三／最後一張原生圖；不買第四張。優先評估同章已收圖重用或來源註記卡，改動後另人書面覆核。 |
| `s53018` | 現代高樓雖已消失，帳棚背景仍有照片質感，與前景 2D 人物脫節；人物為正面全身、通道比「只餘一人肩寬」寬，沒有呈現南公園空間不足的指定近景。原圖與裁圖均同樣失配。正式 judge **9／10 FAIL**，列 `style` 與 `details`；manifest `needs_review=true`。 | **REJECT**。這是第二張實際原生圖；再試前須先提出來源相符的畫面／同章重用退路及獨立紙審，不直接擴批。 |

每張原圖與所選裁圖均為 1280×720 JPEG。`s53010` 原圖 SHA `d4becbf39847d5fa962a06a9092374cddd4cc5d08fdf1d24287c56a347528c48`、裁圖 `d625c31283a679e56c834fcb306f841964cae3158135730fa34319427d31585a`；`s53018` 原圖 `03ff3d435f6ed8b1b8e739e9be96470aec9266b65cde964e938e6ce61e8c210f`、裁圖 `fe22bfaea0abe5c79ff58ea3220080a9b46a5cb5f8c474eb892cf1fba7f1db22`。私有執行日誌 SHA 分別為 `129a0eb440769d935a020c493b535d7985a403457ee44e89c1d15b9d8d501107`、`e2ff1477577ca2c8c55564bc2decdfe044cf83f25362495abc1a6288858a5e86`，原媒體不進 repo。

批後 manifest SHA `72399b433a156ee5064f35ee2da318f2495afea8a0eacd9c7ad8b891d7df5164`、ledger SHA `786794fa452fc6049b428726516d86d4e1e7a84aca90fa772658fe26e3081499`；14 張既有 KEEP 的完整條目及實際選圖 SHA **逐項不變**，jobs 仍空，STOP 已恢復。帳本由 US$0.4320／33 image／32 judge／0 預約，增至 **US$0.4590／35 image／34 judge／0 預約**，新增 US$0.0270，低於整集 US$4.78 上限。後續章節、網站審核卡、人耳旁白、音樂與長短片仍待。
