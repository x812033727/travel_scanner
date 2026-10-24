# S53 R34｜`s53028` 第三／最後原生圖非作者原尺寸驗收

2026-10-22 UTC。**HUMAN REJECT。**我不是 R34 提示詞或出圖作者；獨立打開第三張實際 1280×720 未裁原圖與所選裁圖，對照當前 `video.json`、`claims.md`、固定 1913 年 *San Francisco Relief Survey* D 原文及 Curio 的 `cute-mystery` 畫風驗收。本回只寫此收據，沒有修改稿件、私人圖單或帳本，也沒有購買媒體。

| 核對對象 | SHA-256／狀態 |
| --- | --- |
| 第三張未裁 `keyframes/s53028-1.jpg`，1280×720；退件備份同位元組 | `aba96077b0f43e307d5a6ee191f71acb683a88701206f657e746342b15f40acb` |
| 第三張所選 `keyframes/s53028-1-trim.jpg`，1280×720；退件備份同位元組 | `bb84aa703f6814714a5e6bfe27666b0db50b587aee444fb5909003176d17c652` |
| R34 `docs/videos/curio-s53/video.json` | `f98955b261259a0f687e409a043afe910fe7e9c38a7630e2b5a2d665ebda4997` |
| R34 `docs/videos/curio-s53/claims.md` | `0197cf312874d34cc31895dee05993275357bceac6d81b951fa73334a78841d0` |
| 固定 `56217-0.txt` | `d627ed287d8a93b9c00225ea47dbdc4f97c36089a890192a602b993c3c185b72` |
| 退件時 19 筆 `manifest.json` 私人備份 | `5cbd9935c944b0c72d9caa4d086e812fb02f90a4e701943d3dcec2162ae5b9d8` |
| 恢復後有效 18 KEEP `keyframes/manifest.json` | `591f027333b3f7cd9aec89fbfc2d3400d80bfa95ffdec3e5153ea47e5d1935c9` |
| 恢復後有效 `keyframes/contact-sheet.png` | `0c1694a9150059b8656f778562ecaf925b3a4827d88b919d40464912abb0f930` |
| 有效 `media/ledger.json` | `63af8309a74c3b4348ebb8e534c66910e383e3afbe8c2da386341aa478a18e41` |

`s53028` 口播仍是「九月十日，小屋工程開始。」現行 prompt 與 claims 要一位灰髮、有面紋、未戴帽的匿名成年木匠，在裸地帳棚前，以有**可見折節**的短木摺尺量一片**另外存在、較寬且無字**的粗木板；畫面應是可愛 2D 解說插畫。[Survey D L4858–4864](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L4858-L4864) 記小屋為取代帳棚而建，1906 年 **9 月 10 日開工**，**9 月 16 日** Hamilton Square 有 20 間完工。圖中是灰髮成年人與帆布帳棚，沒有完工小屋或硬帽；**歷史日期與場景背景不是此次退件原因**。

原圖與裁圖都呈現近乎寫實的皮膚皺紋、髮絲、衣布紋理、攝影式淺景深與立體木料，人物像巨大眼睛的寫實偶人，而不是本集的平面可愛卡通；選裁圖沒有消除畫風差異。木尺上有肉眼可辨的數字和疑似微小字樣，並非只有細刻線；尺身是一條直木尺，**看不出折節／鉸鏈**。但機器 details 項說「沒有另外一塊木板」過度概括：我在兩張原尺寸圖都看得到尺下方另有一片更寬、更長、未標字的粗板，板由低鋸架承著。兩件物件可分辨，且人物把尺按在板上；不能把這項說成完全沒有量板。實際缺口是折節和整體畫風、可見數字。

私人退件圖單的機器 judge 為 **6.59／10、`passed=false`、`style=0`、`text=0`、`details=7`、`awkward=4`**。原尺寸支持它對照片／立體偶人畫風、可見數字、無折節與怪異臉部比例的判斷；上段另已校正其「無獨立木板」的說法。Curio 規則明定畫風漂移須重畫，本圖又不符合 prompt／claims 的摺尺描述，故 **HUMAN REJECT**。不能因成人與帳棚年代已對上而選入，也不能把此圖當史實施工照片。

第三張 image-01 與一次 judge 的退件原圖、裁圖、19 筆圖單和 contact sheet 已封存於私人備份；退件圖單中 `s53028` 為 `needs_review=true`，與上列機器 FAIL 一致。有效 18 KEEP manifest 與第三張前備份**逐位元組相同**，`visual_hash=4d419236d18aa61f`，沒有 `s53028`；18 筆 ID、request key、所選 SHA 與退件前既有 KEEP 一致，所選實檔 SHA 全部吻合。有效 contact sheet 亦與第三張前備份逐位元組相同。ledger 逐項合計 **US$0.6345／48 image／47 judge／0 預約**，包含本景三張實際圖及各自 judge。有效 `media/jobs.json` SHA `a9d2c69ab3cb5704417b4f0968a7d8d0dae6eb0e35d37e053463220b30d55ca3` 且 `jobs={}`，`STOP` 在位。

這是 `s53028` **第三張且最後一張**實際原生圖。依已定停線，不購第四張；後續只能另評估誠實重用已收圖或改成有來源可核的卡片，本收據不放行下一景或新付費。
