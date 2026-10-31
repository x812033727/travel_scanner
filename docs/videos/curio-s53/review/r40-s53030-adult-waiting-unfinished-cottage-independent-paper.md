# S53 R40｜`s53030` 成年等待者與未完工小屋獨立書面覆核

2026-10-22 UTC。**PASS，限下列 R40 精確稿件的來源與書面畫面概念。**我不是 R40 提示詞或 claims 作者；直接核固定 Survey 原文、R39 首張退件的 1280×720 原圖與獨立人審、R40 實檔／可逆差分、系列規則及私有停線記錄。本回只寫此收據；沒有改作者稿、私有圖單或帳本，沒有生成／購買圖像、Git 暫存或提交。

## 來源與畫面判定

固定 1913 年 *San Francisco Relief Survey* `/tmp/s53-sf-relief/56217-0.txt` SHA-256 `d627ed287d8a93b9c00225ea47dbdc4f97c36089a890192a602b993c3c185b72`。[D L4850–4865](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L4850-L4865) 記營地選分開小屋作臨時與永久居所、小屋取代帳棚、9 月 10 日開工、9 月 16 日漢密爾頓廣場完成 20 棟，以及至少兩三個月後才有相當數量備妥供難民使用。這是 1913 年後出調查對 1906 年的敘述；它沒有記載 R40 畫面中的特定女子、兩位木匠、木架外形或裝板工序，也沒有說 9 月 16 日所有小屋都未完工或當日已有／沒有住戶入住。

R39 首張原圖 SHA-256 `41ce684ead97291c27cc24e1a3b924d7b842ba45e59ce29bdf101546027e3c1f`；我直接看原尺寸，確認童貌歧義的人物站在完整大型住宅與道路標誌旁，無帳棚、木匠或在建小屋。[R39 獨立視覺退件](r39-s53030-first-native-independent-visual.md) SHA-256 `1191a3293b854fa32494522b14ff5fb2fd2227319072a460a9d4f779b225f62f` 及[停線記錄](r39-s53030-first-native-stop.md) SHA-256 `d2f8a2c21c16459a34a58055ca60ebefb4bda3561df8f349e2f84c9c3c2357ec` 的 HUMAN REJECT 理由成立；舊圖不能因機器 9.29 PASS 而回收。

R40 口播仍問「可等著換進木屋的人，還要再等多久？」。新 prompt 明寫一位有灰髮、面紋、成年手及長裙披肩的中年女性在帆布帳棚外望向施工；右後方只有一間低矮、未封頂或裝門的小屋木架與兩位明顯成年木匠，排除完工大宅、鋪面街道、交通路牌及現代機具。`claims.md` 同列明定匿名、非指定日期的原創等待／施工概念，不把人物、工位及工序冒充為史料。`late 1906` 沒有指定 9 月 16 日；單間在建小屋也沒有主張當日全部小屋仍未完工。書面畫面符合 Survey 的帳棚轉小屋及供屋尚待時日脈絡，並對準 R39 的實際誤導。三人同框仍須在下一張原生圖直接檢查年齡、施工與營地是否畫對；本 PASS 不評價尚不存在的新圖。

## 精確版次及系列檢查

現行 `video.json` SHA-256 **`65bec2d34c7d8443b9e45112e1193c6645feee86e676c0552d78b79f2335c312`**；`claims.md` **`4e6ac59efe8a07e7159547cada6da853f0367dae125ee628643be94822664010`**；`script.md` **`64ffcd8c0e89c4596a7fd08d41bd74f8a16f55fbc9acc2f41d7f9b914ea300fc`**。[R40 作者候選](r40-s53030-adult-waiting-unfinished-cottage-author.md) SHA-256 `18481077388314fc0570a0f8ccc0e99728b3cd6192c51cfcb638517651fba9a0`；[精確差分](r40-s53030-adult-waiting-unfinished-cottage-structured-diff.json) SHA-256 **`5951b331070f0cef386ed16fc6b92571920872d198b9d112a0b83b2b002c08c9`**。

實檔 `scenes[23]`／`s53030` 與差分 `after` 完整相同，只改 `data.prompt`；`id`、`template`、`lines`、`camera`、`visual` 及其他 **123 景**不變。`claims.md` 只有 `s53030` 整行與差分 `after` 對上。把新場景及 claims 整行各反填差分 `before`，逐位元組還原 R39 `video.json` SHA `7ebd094e7bd89ba3ebf036440385ffb6f54aa3f8bdf746b30bbcc91c7d72ba10`、`claims.md` SHA `7ea2850176e7e8a27e10fa7807db0007358f52868eb3f8bedd87ca8a711820f4`。124 景內的 126／126 句 ID 與文字完全相同；`speechHash=05c4d9a79a8708b4`、新 `visualHash=5818abc588740097`。私有 `timeline.json` SHA `c75c8bde15f7220862ba8083d6590b7b14bb71c456f896f7b58c13352c88a054`、`narration.wav` SHA `08444d50c2f8b70a7079701e157397d9a7c23d08971727164df91a1101e281e1` 均未變。

實跑 `VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s53 --json`：exit 0、**0 errors／0 warnings／126 lines**。正文 111／123 `shot`（90.2%），最長連續卡片 2 張，符合系列 ≥70% 插圖及最多 3 張卡片。以正式 `cute-mystery` look 與 MiniMax 1,500 字元上限離線重算，`s53030` 場景 prompt **694／1072** 可用字元；合成 prompt 1121 字元，無截斷或遺落修正。

## 私有圖單、費用與停線

正式 `keyframes/manifest.json` SHA-256 **`326a87c9208d686eeb1618dbd76f8745f85aac9a48c9eebd60125ade7840d255`** 仍綁 R39 `visual_hash=09c82f30136ccbde`，尚未回綁 R40。18 筆 ID／所選路徑／SHA／request key 逐筆與 [R39 STOP inventory](r39-s53030-first-native-stop-inventory.json) SHA-256 `202d212298eba845a17b6f2912dfac9c8c88f5de311c2d3afb358f542c78473c` 相同；18 個實檔 SHA 全對、judge `passed=true`、`needs_review=false`，正式圖單沒有 `s53030`。

私有 `media/ledger.json` SHA-256 **`2c924c6368bd267e1c006e5754666fa071fd270d7c4c0c98195ae7266b7cdace`**；103 筆逐筆重加為 **US$0.6885／52 image／51 judge／0 預約**，低於整集 US$4.78 委派上限。`media/jobs.json` SHA-256 `a9d2c69ab3cb5704417b4f0968a7d8d0dae6eb0e35d37e053463220b30d55ca3` 且 `jobs={}`；`STOP` 在位。此 PASS 只結束 R40 書面審查；若續作，先在 STOP 下另行備份、離線回綁新 visual hash、重核 18 KEEP 與帳本，再按既定單景預檢與第二張一圖一審界線處理。R39 退件圖與本紙審均不能充作新圖的人眼 KEEP。
