# S38 R8w｜PF015 同章重用獨立紙審

2026-10-22 UTC。**書面 PASS；新景的圖單與 judge 仍待重綁。**本輪僅覆核 R8w 凍結稿 `video.json` SHA-256 `af739ca32d19df378b942f04118377f8357b6b16d03f07a1e3203b53182c3bc9`，不把舊 PF015 退圖當作可用圖。`script.md` `e59ec137e3de3871e3b0e5063d8f6504d3eb2adb5fe22265eb3faa3d613d5951` 與 `claims.md` `f9de8d2771b62cc327f4e599f002af8f3278cfb0f39dbed201e7fdc857201d42` 未改。

固定 Pepys 日記 `4200.txt` 原始 SHA-256 `3cd43a3c39ee72eb9c4a3657f1fcb1723afba291cedac176c65a39289483be5d` 的 [1666-09-02 L65800–65823](https://github.com/GITenberg/The-Diary-of-Samuel-Pepys---Complete_4200/blob/68fcf49f70ee793b989a6fd0464264d55beb4451/4200.txt#L65800-L65823) 先述約七時從住處窗看較小、較遠的火，稍後上塔親見橋邊房屋著火並掛念熟人，接著從塔官**聽說**起火處，搭船才親見熟人房屋已燒。PF015 旁白以「**剛才**的遠處紅光」明示回望剛展示的 PF010 窗邊視野；PF013／014 已用來源引句卡呈現新的塔上見聞，PF016／017 接塔官的口頭說法。因此重用 PF010 是有標記的舊視野回呼，並未宣稱佩皮斯登塔後回家或從住處窗確認熟人房屋燒毀。剪輯仍須讓觀眾能辨識回望，不能把此圖當新塔上目擊。

R8v→R8w [作者結構差分](verify-71-r8w-pf015-reuse-structured-diff.json)僅改 `scenes[14].data.prompt`／`camera`；獨立逐字逆套，精確還原 R8v SHA `fd506ba278ffbcbb2b17908b957eb9a2163a2d26cd3b2b78556bab365212b7f4`。現行 `pf015.data` 與 `pf010.data` 完全相同；其餘場景與所有台詞不變。獨立 `lint --slug curio-s38 --json` exit 0，0 errors／0 warnings，112 句；開場後正文 106／111 景仍為插圖，最多兩張連續資訊卡。

直接看過 `keyframes/pf010-1-trim.jpg`：單一成年卡通人物靠舊式窗，後方是屋頂與火光，沒有現代車、可讀字或額外肢體。選圖 SHA-256 `5fc7fd687ced8649ecae9b392df16383047aab399a3525786a498b6efcc65850`；原圖 `pf010-1.jpg` SHA `b2fd9bdb55b158c6e942ef202dbddcea890ba5a4303670f73568e27ed0da60c0`，PF010 既有 judge 10／10。按現行 `shotPrompt`、MiniMax `image-01`、1K、seed 1、無參照、image selection version 0 **實算** PF010 與 PF015 的 image key 都是 `417bcf79c5715425`；`cached()` 驗證該 key 命中上述原圖且位元雜湊相同，沒有待續 job。這證明**圖片本身**可零生成費重用，但 PF010 的 judge stamp 包含 `scene.id=pf010`，不能冒稱已替 PF015 判圖。PF015 須在受控 STOP 臨時解除、禁止 image POST 的包裝下執行一次正式 PF015-context judge，然後再看原圖／選圖與新 manifest；若服務不可用就維持 HOLD。

紙審前私人 manifest SHA `2517afd911a9a49a01a555718b09ca776cd95015c6f1a32b2090900754fded0a` 尚含 PF015 第三張退圖；ledger SHA `a40873757bb51cbba4fc0240b76c6e2641b7c626e5328f18215c0b5fc73db86b`，US$0.7045／47 images／46 judges／1 music，另有既存 US$0.0035 reservation；STOP 在位。此紙審沒有付費、沒改 manifest。PF019 仍未畫，不能宣稱首章或全片分鏡完成。
