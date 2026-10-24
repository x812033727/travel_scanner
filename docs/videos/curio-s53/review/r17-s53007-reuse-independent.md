# S53 R17｜`s53007` 同章已收圖重用，獨立書面覆核

2026-10-22 UTC。**PASS，僅允許 `s53007` 從既有 `s53003` 圖像快取定點重綁與自己的 judge；不可買第四張新圖。**我沒有參與 R17 作者修訂，沒有更動旁白或分鏡。本結論只核對來源、圖片意義與可重用的快取條件，不是新 judge、整章或網站分鏡核准。

固定 1913 年 *San Francisco Relief Survey* SHA-256 `d627ed287d8a93b9c00225ea47dbdc4f97c36089a890192a602b993c3c185b72`；L4972–4994 記符合條件者可自費搬出小屋，L10932–10944 記費用可能由住戶、親友、房東、慈善機構承擔。`s53007` 的原句「小屋離開營地時，搬遷費會由誰付？」仍是開放問題。R16 三次嘗試後的未裁切原 JPEG 因黑邊及人物持袋而被退，不能再把它當合格視覺；R17 選的 `s53003` 已收原圖是灰髮成年住戶在低矮木屋門邊，**沒有錢袋、付款動作、搬運機械或可讀文書**，只讓觀眾回想要搬的屋，沒有預先指認付款人。兩景之間隔著三張不同畫面，也不會連續停同一張圖。

我直接重看並重算 `s53003` 原 JPEG SHA-256 `878039a01f4d0138abeb4262205886e48ed0f99ad03c5ac59c15e9f03ade9d09`、所選裁邊圖 SHA-256 `73823edb92173cf2df2be0f4988f6a25fd3c1044d9387041602c2e171a3f2f2b`，兩者皆與 R16 原圖驗收及 manifest 相同。R17 `s53007` 的 `prompt` 和 `camera` 分別與 `s53003` **逐字相同**；[可逆差分](r17-s53007-reuse-structured-diff.json)恰改 `scenes[6].data.prompt`、`.camera`，反向還原得到 R16 SHA-256 `817819fb64717fb3dc6e5bd1e1957a5e7d14d9f8fb455001ac0d4a609ee62f12`。R17 現行 `video.json` SHA-256 `6550c8f26db13d1f72e9f706404e8d80efe131789fb4b37918b2ea9f48e222ae`；其餘 123 景、126 句旁白、`claims.md` 和 `script.md` 未變。Lint 0 errors／0 warnings。

工具 `Stage.imageKey` 根據模型、合成提示詞、畫風、參考圖、種子和尺寸算鍵，不含場景 ID；camera 已一起複製。私有快取鍵 `b27d248cc2079365` 確實仍指向上述 `s53003` 原 JPEG，快取驗證重新算 SHA 成功。付款前帳本 US$0.2465／19 images／18 judges／0 reservations，STOP 在位，本集上限 US$4.78。下一步只跑 `--shot s53007 --takes 1`，用 EXIT trap 還原 STOP；若日誌沒有明示 `(reused)` 或 image 計數上升，就停線調查，不以新生成結果替代已收圖。另查 R17 新 judge、manifest 和原圖 SHA；此圖的人工 KEEP 仍需在實際快取重綁後才下結論。
