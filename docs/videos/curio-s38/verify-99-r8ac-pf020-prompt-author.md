# S38 R8ac｜PF020 原圖退件後單景提示詞窄修

2026-10-22 UTC。**作者提案；待另一位工作者依固定史料獨立紙審。本輪修訂後沒有付費媒體呼叫。**PF020 首張原圖[已退件並停線](verify-98-r8ac-pf020-seed1-human-reject.md)：可見的不是把家當拋河，而是人抓硬箱、黑桿碰水，且旁觀者有現代服裝。已從 active 圖單隔離該圖，保存 12 張舊 KEEP。

只改 `scenes[19].data.prompt`（PF020）：從泛稱「倫敦居民傾倒家當」和多個抽象年代排除詞，改成**一名灰髮成年倫敦住戶**，穿深色羊毛 doublet、白色亞麻領，雙手在河岸邊**放開一個已離手、在水面上方的綁結亞麻布包**。背景只留開闊河水與陰天，減少產生現代旁觀者、街具、硬箱或黑桿的機會。木／石河岸、人物衣飾、布包只是 1666 年插畫示意，不宣稱佩皮斯日記辨認過此人的年齡、衣著或丟入河中的具體物件。

固定 [1666-09-02 Pepys 日記 L65816–65822](https://github.com/GITenberg/The-Diary-of-Samuel-Pepys---Complete_4200/blob/68fcf49f70ee793b989a6fd0464264d55beb4451/4200.txt#L65816-L65822)在「人們搬家當」段寫 `flinging into the river`；旁白「還有人把搬不及的東西直接丟進河裡。」和 `claims.md` D2a 均未改，畫面只表達此動作，不暗示後續撈回、損失或具名居民。

[單葉可逆差分](verify-99-r8ac-pf020-prompt-structured-diff.json)綁 `video.json` SHA-256 `b955dae2c2620b7477fcdef24606d9c1696f390c927f9fc7be10aa058d0b2ae9` → `d8d169a010a7ffce93b3aec580e7c9580dc3a5393ffbe0bbc5909b72e8559688`。反填舊 prompt 可逐位元復原；`script.md` SHA `e59ec137e3de3871e3b0e5063d8f6504d3eb2adb5fe22265eb3faa3d613d5951`、`claims.md` SHA `f9de8d2771b62cc327f4e599f002af8f3278cfb0f39dbed201e7fdc857201d42` 不變。`lint --json` 仍 **0 errors／0 warnings**、估 10.016 分鐘。改後單景 `keyframes --dry-run` 因 `mokaair.com` 暫時不可達而 exit 4，沒有取得新模型預檢或服務就緒證據；不能據此開始付費生成。

私人 active manifest SHA `f666bcc1d7afe4b7e40215cb373ccf29d2a9ee8d262606c24026ee98b3914c74` 含 12 張 KEEP，仍綁**舊** R8ab `visual_hash=7f7b8b8dda0faefa`；prompt 修訂後不可直接拿它當新圖單。ledger SHA `6696edf9ed0f77aa1b4f8e475f37f8121fe51cf997d65414327cbc086fcab14c`，US$0.8225／55 image／55 judge／1 music，另有舊 US$0.0035 reservation；STOP 在位、jobs 空。非作者紙審 PASS 後，先對新視覺雜湊安全離線重綁 12 KEEP，復查 live status／dry-run／整集 US$4.58 上限，再只准 PF020 單景一張及一次 judge；任何 FAIL 或人工 REJECT 再停線。PF021／PF022 不在本輪付費範圍。
