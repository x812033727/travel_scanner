# S53 R44｜官方營地優先資格成年住戶畫面非作者紙審

2026-10-22 UTC。按精確 R44 版本獨立判 **PAPER PASS**。本審只核來源、文案、可逆差分及既收媒體適用性；不等於 `s53033` 已有圖片，也不免除之後的即時模型／額度／預算檢查和原尺寸人審。本審未修改影片、claims、私人圖單、任務或 PR，亦未呼叫付費媒體。

## 固定史料與畫面主張

重開固定 `/tmp/s53-sf-relief/56217-0.txt`，SHA-256 `d627ed287d8a93b9c00225ea47dbdc4f97c36089a890192a602b993c3c185b72`。[1913 年 *San Francisco Relief Survey* E L4887–4897](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L4887-L4897) 先說官方營地難民多獲免費帳棚，木屋替代帳棚時出現誰有使用權的問題，再明記 `Cottages were assigned by the camp commanders, first, to those in the official camps; second, to those in shacks and tents outside; third, ...`。故 `s53033` 旁白「官方營地住戶，有優先分配小屋的資格」符合群組先後；史料沒有給這名女子、特定房屋、鑰匙、入住房日或誰在鏡頭中已領屋。

[原版預檢](r44-s53033-unchanged-priority-row-preflight.md) SHA `37a422f6fcfb0bb67d624fd85ec873698bf27be4c9882a91551af1166c836693` 對匿名人物及整排小屋易誤示已分配提出開畫前 HOLD。新提示改成一位灰髮帶面紋、有成人身形的住戶站在 1906 年官方帆布帳棚營地的一頂帳棚旁，望向隔著空通道的一棟低矮木造小屋；手搭帳棚繩，木屋關門、無可見住戶，沒有鑰匙、申請單、排隊或特定交屋動作。女性、帳棚、屋子與動作是**匿名原創資格概念**。`claims.md` 明示只說群組優先，不說每位官方營地住戶立即獲屋或這名人物已入住；將一棟屋作為視覺目標沒有把來源改成個案紀錄。`wooden dwelling` 和簡樸材物適合固定 E 的木屋／帳棚語境，亦不新增 `cottage`／`relief` 同詞警告。實際生成圖若畫出受配結果、住進屋的人、幼齡人物或失去帳棚與小屋的關係，仍須按來源與系列規則另行判斷，紙審不預先判 KEEP。

## 精確差分與正式檢查

R44 `video.json` SHA-256 `4a3b3447bb1f5d980b0a0965309c1e9a3fda81f64ead117e87910f340f61831d`，`claims.md` SHA `69d91d3b6e5bf5e551060f0eeab5f7745a1704d5c24e59f1f1d10993554ba4c3`；[作者收據](r44-s53033-mature-official-camp-priority-author.md) SHA `d0bc14a72d179556f0bc3b7eddb8ec203e6d57a76ebb565148426c5f85c140ef`，[結構化可逆差分](r44-s53033-mature-official-camp-priority-structured-diff.json) SHA `45c731620cb7a50a61b4087366adede6dae37caff62f7553b8d0788acceb684a`。獨立把差分反填，`video.json`、`claims.md` 與 Git 目前 R43 已提交版逐位元組相同，分別回 SHA `76f9607d619d8be004904a22c588237c76d86200b4015fd53fbb83fd50d33b3a`、`003e44937888d2e6f3dda5baba27283caf77f2552e732deb149fe6d53e9f3448`；124 景中只 `s53033.data.prompt` 有變，claims 也只變同列。其餘 123 景及 **126／126** 句 ID、文字與語氣不變，scene 外設定不變。

`script.md` SHA `64ffcd8c0e89c4596a7fd08d41bd74f8a16f55fbc9acc2f41d7f9b914ea300fc`、私人 `timeline.json` SHA `c75c8bde15f7220862ba8083d6590b7b14bb71c456f896f7b58c13352c88a054`、`narration.wav` SHA `08444d50c2f8b70a7079701e157397d9a7c23d08971727164df91a1101e281e1` 均不變。正式重算 `speechHash=05c4d9a79a8708b4`，新 `visualHash=b664a4a74bbb6d8c`；實跑 `VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s53 --json`，exit 0、**0 errors／0 warnings**、126 行。正文 **110／123 `shot`（89.4%）**，最長相鄰來源卡 **2**。未做媒體 dry-run 或付費生成。

## 私人媒體狀態與 PASS 範圍

只讀核私人正式 `keyframes/manifest.json` SHA `32cc2e9b985a8ca8c7f6d994d75dfad1d52e083017d3b9c4277c4a57b9a3364e`：**20 KEEP** 各筆 judge PASS、`needs_review=false`，20 個所選 JPEG 實檔 SHA 逐張吻合；`s53033` 尚無選圖。manifest 仍綁 R43 `visual_hash=747fc5795d5cb270`，**沒有**回綁新 R44 visualHash。contact sheet SHA `7567d866096ae2ae1d8c92a191b8b6aa74ca1b67c56a4e5582ab6fa9cf666a57`；STOP 在位、jobs SHA `a9d2c69ab3cb5704417b4f0968a7d8d0dae6eb0e35d37e053463220b30d55ca3` 且 `{}`，ledger SHA `ae0310f9f3b3e78631d54f6815e1be4439147453da1b3fc919f2bf02b662772f`，**US$0.7290／55 images／54 judges／0 reservations**，低於整集 US$4.78 上限。

本 PASS 只放行在 STOP 下把 manifest 的 `visual_hash` 安全離線回綁 R44，逐筆保留 20 KEEP；之後仍須即時預檢 MiniMax 模型、配額、US$4.78 上限及 `s53033 --takes 1 --dry-run`。若通過，最多購 `s53033` 第一張原生圖與一 judge，直接看原尺寸；實圖如有會誤導來源／旁白的內容或系列畫風漂移，立即停線，不跳下一景。
