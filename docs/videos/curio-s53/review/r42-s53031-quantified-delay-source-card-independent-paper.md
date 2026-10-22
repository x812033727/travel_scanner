# S53 R42｜兩三個月供屋延遲來源卡非作者紙審

2026-10-22 UTC。**PAPER PASS**，限下述精確 R42 版本；這是來源、文案、版面與既收媒體適用性的離線審核，並非將私人圖單回綁 R42 或准許付費開畫。

## 固定來源與卡片語義

重新開啟本機固定 Survey D `/tmp/s53-sf-relief/56217-0.txt`，SHA-256 `d627ed287d8a93b9c00225ea47dbdc4f97c36089a890192a602b993c3c185b72`。書名頁記 MCMXIII／Copyright 1913；L4858–4865 在 9 月 10 日開工、16 日漢密爾頓廣場完成 20 棟後明說：`At least two or three months, however, intervened before any considerable number of houses could be made ready for the refugees.` [固定 D 原文](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L4858-L4865)。因此 `s53031` 主標「至少兩三個月」保留最低間隔；上標「相當數量的小屋，才備妥供難民使用」保留 *any considerable number* 的範圍與 *made ready*，並未說全部小屋或每戶入住日。下標「1913 年《舊金山救濟調查》｜英語原文意譯」正確指出後出調查，而非 1906 年原始公文。卡上未標間隔的精確起算日；相鄰 `s53029` 的 20 棟完工也沒有被改寫成全部尚未完工。`claims.md` 的新列明示這些界限。後續剪輯或延伸文案仍不可從此卡推算每戶搬入日或指定 9 月 16 日為精確起點。

按 `.agents/skills/curio-episode/SKILL.md`，卡片只承載插圖難以說清的數字、名字、引文或出處。此景的核心是帶最低量詞的數值與來源，來源卡適用；退件施工插圖不能呈現兩三個月的間隔。`s53030` 插圖隔開此前兩張相鄰日期卡，`s53031` 不製造超限的連續卡片段。

固定 Survey F L4899–4932 說原先考慮對木屋住戶收 nominal rental，且提供租約、營地指揮官與救濟機構的脈絡。[固定 F 原文](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L4899-L4932)。`s53049` 唯一改動是未開畫 prompt 中 `relief office` → `plain administrative room`；匿名職員、零錢、無字租約、旁白與 claims 均未改。房間仍是租務的匿名概念畫面，沒有聲稱史料記載特定辦公室；較一般的地點名詞不改 F 的制度主張。有效 19-KEEP 圖單沒有 `s53049`，故這次沒有令已收的該景畫面失配。

## 精確差分及檢查

固定輸入 SHA-256：R42 `video.json` `81d681b05d12d766e6fcf70d6c60ee78a0dace86d55e93d3401b1ab8c7528ab2`、`claims.md` `eac14636b9762c539950a5c664387cd91a6512da3fcadbd2944341fdd45ee7cf`；[結構化可逆差分](r42-s53031-quantified-delay-source-card-structured-diff.json) `7ea9ac831382ffa74997956f19337184c2e7de647cd3dea711cb66a63b7ddbdc`。逐項核對差分的 `after` 與現稿，反填 `s53031` 完整 scene、`s53049` 完整 scene 及 `s53031` claims 單列，canonical JSON 重序列化後與 R41 前版**逐位元組相同**：`video.json` `56854934253b38463c3ab37cc283cb8dfdc9992dff7c81991fcd17484b622173`，`claims.md` `d6736f0a1126b773038223159e60e5fe4680b56c5abd34594e5088e6c29ea0e8`。直接比對兩版 124 景，僅 `s53031`、`s53049` 不同，其餘 **122 景相同**；126／126 條 `lines` 的 ID、文字及語氣均相同，scene 外設定相同。

`script.md` SHA-256 `64ffcd8c0e89c4596a7fd08d41bd74f8a16f55fbc9acc2f41d7f9b914ea300fc` 未變。正式 `loadProject`／`speechHash`／`visualHash` 重算：R41 與 R42 的 `speechHash` 均為 `05c4d9a79a8708b4`；`visualHash` 由 `cfbe5fb638b9afd6` 變為 `bc739bdaed3b717a`。私人 `timeline.json` SHA `c75c8bde15f7220862ba8083d6590b7b14bb71c456f896f7b58c13352c88a054`，126 行且 speech hash 相同；`narration.wav` SHA `08444d50c2f8b70a7079701e157397d9a7c23d08971727164df91a1101e281e1`，故此次未動音訊。實跑 `VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s53 --json`，exit 0、**0 errors／0 warnings／126 lines**。正文 123 景有 **110 shot（89.4%）**，高於 70% 下限；最長卡片段 **2**，低於最多 3 張。現稿 `relief` 出現在 36／110 個插圖 prompt，沒有超過三分之一；將 `s53049` 換回舊詞則是 37／110，重現該畫面多樣性 warning 的門檻。

檢視作者以正式版面產生的 `/tmp/s53-r42-s53031-card-smoke.png`，SHA-256 `b3657209073ee89494cfdfb022c3b8bf19618a34363ab2b1722604fd4a156812`；檔案為 **1920×1080** PNG，實際圖中上標、主標及 1913 年來源下標均完整且可讀，無裁字或越界。作者的 `renderer.capture` 結果記為 `problems=[]`；本紙審另以原尺寸視覺核對該 PNG。

## 私人圖單與停線

只讀重核 `/workspace/.video-work/curio-s53/keyframes/manifest.json` SHA `4cfd50a126d5d4f65c4fba6daf1bd8c9e04ecc209aed241a20cf4266d22d4011`：**19 個 KEEP** 的選圖 `file`／`sha256`／`key` 與 R41 inventory 相同，19 個實際 JPEG 雜湊逐一吻合且 `judge.passed=true`、`needs_review=false`。有效圖單沒有 `s53031` 或 `s53049`，仍綁 **R41 `visual_hash=cfbe5fb638b9afd6`**，尚未回綁 R42。`STOP` 在位；`media/jobs.json` SHA `a9d2c69ab3cb5704417b4f0968a7d8d0dae6eb0e35d37e053463220b30d55ca3` 且 `jobs={}`。`media/ledger.json` SHA `ce2d97f156a1d7d3b0079a8f1e790374013e21ea9a15bc33e4cf436fad1fec89`，累計 **US$0.7155／54 images／53 judges／0 reservations**。此 PASS 允許在既有停線下另行安全離線回綁並核對 19 KEEP；回綁完成前不得將舊 manifest 視為 R42 已完成媒體。
