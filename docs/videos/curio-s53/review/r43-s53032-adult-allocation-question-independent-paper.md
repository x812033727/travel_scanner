# S53 R43｜分屋疑問成年指揮者畫面非作者紙審

2026-10-22 UTC。對精確 R43 `s53032` 書面修訂判 **PAPER PASS**。本審只放行在 `STOP` 下安全離線回綁 19 張既收圖；不代表新圖已生成或審過，也不免除付費前的即時模型、配額、預算及單景 dry-run。

## 史料與畫面界線

重開固定 1913 年 *San Francisco Relief Survey* E `/tmp/s53-sf-relief/56217-0.txt`，SHA-256 `d627ed287d8a93b9c00225ea47dbdc4f97c36089a890192a602b993c3c185b72`，L4887–4897 原文先問 `who would be entitled to their use, and on what terms?`，再說 `Cottages were assigned by the camp commanders, first, to those in the official camps; second, to those in shacks and tents outside; third, ...`。[固定 E 原文](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L4887-L4897)。這支持 `s53032` 的分屋疑問與 `s53033` 才回答的官方營地優先；該段沒有兩張申請單、特定審表程序或逐戶搬入日期。[R43 原提示紙面 HOLD](r43-s53032-unchanged-application-slip-preflight.md) 因此有實際依據。

新英文提示只讓一名**明顯成年**、灰髮有面紋的匿名營地指揮者穿無徽章便服，在 1906 年官方帳棚營地一座低矮空屋的門旁指向空門檻；沒有另一住戶、表單或已做出的分配決定。這是問「誰能先住進去」的原創概念畫面，並非特定指揮官、房屋或當日紀錄。`claims.md` 同列明示這些界限，未暗示全部木屋已備妥、某戶已入住或有存世申請表。`wooden dwelling` 指的仍是史料的木造小屋，沒有改變分配主張；少用 `cottage` 也使 110 張插圖的同詞警告維持為零。請於未來實圖人審再確認人物確實成年、房屋低矮且空置、畫風與 1906 年背景相符；紙審不預先替實圖判 KEEP。

## 精確差分與媒體適用性

R43 固定 `video.json` SHA-256 `76f9607d619d8be004904a22c588237c76d86200b4015fd53fbb83fd50d33b3a`，`claims.md` `24aba613275829af3af975800bca0ec06c83196f3bcca50a20239bb811bc1ced`，[作者收據](r43-s53032-adult-allocation-question-author.md) `c8e56c9c941be50c42d5ea2578e15dacc0359fde6e71ee1bf6bf05912413781b`，[結構化可逆差分](r43-s53032-adult-allocation-question-structured-diff.json) `50785332dcc4c0d3153147c5a7194508466c57a61fcb0edd5fbc195f90d40ea8`。獨立以 Git R42 版逐位元組比對及差分反填：124 景中**只有 `s53032` 整景**不同，該景僅 `data.prompt` 改；claims 只改其同列。反填後 `video.json`、`claims.md` 逐位元組回 R42 SHA `81d681b05d12d766e6fcf70d6c60ee78a0dace86d55e93d3401b1ab8c7528ab2`、`eac14636b9762c539950a5c664387cd91a6512da3fcadbd2944341fdd45ee7cf`。其餘 123 景、126／126 條 `lines` 的 ID、文字、語氣、鏡頭外設定不變。

`script.md` SHA `64ffcd8c0e89c4596a7fd08d41bd74f8a16f55fbc9acc2f41d7f9b914ea300fc`、私人 `timeline.json` SHA `c75c8bde15f7220862ba8083d6590b7b14bb71c456f896f7b58c13352c88a054`、`narration.wav` SHA `08444d50c2f8b70a7079701e157397d9a7c23d08971727164df91a1101e281e1` 均未動；正式重算 `speechHash=05c4d9a79a8708b4`、新 `visualHash=747fc5795d5cb270`。實跑 `VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s53 --json`，exit 0、**0 errors／0 warnings**；正文 **110／123 插圖（89.4%）**，最長相鄰卡片 **2**。本審沒有執行媒體 dry-run 或付費呼叫。

私人正式 manifest SHA `3046213a5cce33e4178fd3d92a5d5f9bf319a4ce3cdeff228c0a797669f7e698` 仍綁 **R42** `visual_hash=bc739bdaed3b717a`；19 個 KEEP 的所選 JPEG SHA 逐張吻合，judge 全 PASS、`needs_review=false`、已收鏡頭 `keyframeProblems` 為零，`s53032` 尚無選圖。contact sheet SHA `1b58f6e22f6cd20dd339bc8a022cf2ca4546937f5c0c2b49b1021efd83c64483`；`STOP` 在位，jobs SHA `a9d2c69ab3cb5704417b4f0968a7d8d0dae6eb0e35d37e053463220b30d55ca3` 且 `{}`，ledger SHA `ce2d97f156a1d7d3b0079a8f1e790374013e21ea9a15bc33e4cf436fad1fec89`，US$0.7155／54 images／53 judges／0 reservations，低於整集 US$4.78 上限。**PASS 後只能受控離線把 manifest visualHash 回綁 R43，逐筆保留 19 KEEP；再即時預檢，最多購 `s53032` 首張一圖一 judge，直接看原尺寸，不合來源／旁白或系列畫風即 STOP。**
