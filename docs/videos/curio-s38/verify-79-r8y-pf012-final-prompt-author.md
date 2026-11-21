# S38 R8y｜PF012 最後一張原圖的窄修提案

2026-10-22 UTC。R8x 的 PF012 seed 1 因沒有正在披斗篷而正式 judge FAIL；seed 2 雖為機器 9.29／10 PASS，非作者逐張看[原圖與裁圖](verify-78-r8x-pf012-seed2-human-reject.md)後，確認左下角現代塑膠瓶、領帶及近現代衣著，**人工 REJECT**。不能把 `needs_review:false` 的機器狀態當成歷史圖像收件。

作者只改 `scenes[11].data.prompt` 一葉：改成**腰上特寫**，明寫成年佩皮斯正在把未扣上的深色羊毛斗篷披到兩肩、雙手拉近前緣，內衣是樸素開領亞麻衫，背景只剩木門與粉牆，排除瓶子、容器、領帶、條紋襯衫、皮帶和現代物。這是固定 [1666 年 9 月 2 日佩皮斯日記 L65804–65808](https://github.com/GITenberg/The-Diary-of-Samuel-Pepys---Complete_4200/blob/68fcf49f70ee793b989a6fd0464264d55beb4451/4200.txt#L65804-L65808) 的 `made myself ready presently, and walked to the Tower` 可容許的示意畫面；不新增任何旁白主張。PF012 `push in` 運鏡、全部 112 句旁白、PF015 日記卡、111 個正文鏡中 105 個插圖景、其他 10 張已合格圖均不變。

[單葉可逆差分](verify-79-r8y-pf012-final-prompt-structured-diff.json)把 R8x `video.json` SHA-256 `23f0662b96ba290494b044f2cdce037ba011b5222a1137d5a38b0a5e25600615` 改成 R8y `586c55b4328c96ab405156467ca2deb7cf294119e4043aaea579c27704404652`；逆填新舊 prompt 可逐位元還原 R8x。`script.md` SHA `e59ec137e3de3871e3b0e5063d8f6504d3eb2adb5fe22265eb3faa3d613d5951`、`claims.md` SHA `f9de8d2771b62cc327f4e599f002af8f3278cfb0f39dbed201e7fdc857201d42` 不變。正式 `lint --slug curio-s38 --json` exit 0、0 errors／0 warnings，112 句、lint 總估時 10.016 分鐘。

**作者提案，待非作者紙審。** PF012 累計已有兩張實際原圖；即使 prompt 換新 image key，也最多再試**一張**實際原圖及一次正式 judge，不會重算三張。紙審後先安全重綁圖單，保留並核驗 10 張既有 KEEP，從現行 manifest 移除人工退件 PF012；不能用舊機器 PASS。私人 STOP 在位、jobs 空，現有 ledger SHA `368cd9664468db66de264216fe5bc591d9086768150af028109fb057c5259b9e`：US$0.7415／49 images／49 judges／1 music，另有舊 US$0.0035 reservation，低於本集 US$4.58。任何付費呼叫前重新查即時價格／額度與確切綁定；第三張仍有實質錯誤就停，不再補畫第四張。PF019 與後續分鏡尚未收圖。
