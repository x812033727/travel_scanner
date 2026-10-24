# S38 R8w｜PF015 舊圖重用的正式評審退件

2026-10-22 UTC。接[站台停線回條](verify-73-r8w-pf015-cache-judge-upstream-hold.md)，媒體服務透過 `NODE_USE_ENV_PROXY=1` 恢復，已在整集 US$4.58 上限內，對 **PF015 情境**跑一次正式評審。**0 張新圖，1 次 judge，PF015 仍 HOLD。**

批前 `video.json` SHA-256 `af739ca32d19df378b942f04118377f8357b6b16d03f07a1e3203b53182c3bc9`；`PF015.data` 與已收的 PF010 完全相同。批前私人 manifest SHA `2517afd911a9a49a01a555718b09ca776cd95015c6f1a32b2090900754fded0a`，ledger SHA `a40873757bb51cbba4fc0240b76c6e2641b7c626e5328f18215c0b5fc73db86b`，STOP 在位，jobs 空；PF010 原圖 `keyframes/pf010-1.jpg` SHA `b2fd9bdb55b158c6e942ef202dbddcea890ba5a4303670f73568e27ed0da60c0`。執行前再次核對影片、原圖、圖單、帳本雜湊和 `pf010/pf015` 資料相等；正式 `keyframes --shot pf015 --takes 1` 在臨時解除 STOP 且 `/tmp/s38-r8w-block-image-submit.mjs` 阻斷任何新 `POST /api/video/media/images` 下執行，shell trap 已恢復 STOP。

工具顯示 **`(reused)`**，PF015 image key `417bcf79c5715425` 與 PF010 相同，重用了 PF010 原圖與裁圖，選圖 SHA `5fc7fd687ced8649ecae9b392df16383047aab399a3525786a498b6efcc65850`。新 PF015 judge **9.71／10、`passed=false`**：人物面向屋內鏡頭，火在他背後，沒有按提示詞向窗外看。親看 1280×720 原圖與裁圖也確認人物朝向；PF010 舊有 10／10 判定只屬原 PF010 情境，不能移作本景。正式工具 exit 1 並留 `needs_review=true`；缺 Playwright 對應 Chromium 令接觸表未產生，亦不能當作圖單通過。

批後 ledger SHA `8532e628f57d01fbbd9eea2e5bedaeac3c65ca22c15107745933801fb682028f`，累計 **US$0.7145／47 images／47 judges／1 music**，比批前只多一筆 **US$0.0100 judge**；另有舊 US$0.0035 reservation。manifest SHA `b03173cc2828e80a026509b5eb23628f4215e41893598dc1e8040a9ac0c0364f`；11 張其他既有 KEEP 保留，PF015 選圖雖指向 PF010 裁圖但仍退件。jobs 空、STOP 已恢復，PF019 仍未畫。PF015 三次原生試圖與兩輪提示詞修訂已用完，不再買第四張；須先選來源合格的同章重用或字卡，通過新稿 lint 與獨立紙審後才處理圖單，不能把這次高分或快取命中稱為驗收。
