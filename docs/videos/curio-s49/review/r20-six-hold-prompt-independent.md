# S49 R20｜六張 HOLD 提示詞獨立書面覆核

2026-10-22 UTC。結論：**來源及書面畫面 PASS，僅放行 `moon017/019/020/021/024/025` 各一張受控首試；不等於原圖或分鏡通過。**

我獨立打開 R19 六張 **1280×720 原生 JPEG**，對照 [R19 逐張清單](r19-first-chapter-native-inventory.json)、[作者可逆差分](r20-six-hold-prompt-structured-diff.json)、六句旁白及主張欄。`moon017` 的懸空手與黑邊、`moon019` 多出的第二本書、`moon020` 現代辦公室、`moon021` 小孩與電燈、`moon024` 可讀字及檔案箱、`moon025` 連帽衫小孩均在原圖可見；退圖原因成立。

我重讀固定 1859 年 Locke 名下重印本 [P02 L152–165](https://github.com/GITenberg/The-Moon-Hoax-Or-A-Discovery-that-the-Moon-has-a-Vast-Population-of-Human-Beings_62779/blob/ce684a827afd854e0843679fe4568fcaeeb12ae7/62779-0.txt#L152-L165)、[P03 L168–254](https://github.com/GITenberg/The-Moon-Hoax-Or-A-Discovery-that-the-Moon-has-a-Vast-Population-of-Human-Beings_62779/blob/ce684a827afd854e0843679fe4568fcaeeb12ae7/62779-0.txt#L168-L254)，及 Jacoby 1902 年 [J4063–4070](https://github.com/GITenberg/Practical-Talks-by-an-Astronomer_53396/blob/073dd7dd24b8515dec681441a1cde79477fabf08/53396-0.txt#L4063-L4070)。P03 把 Grant 消息、Herbert Home 現場繪圖、皇家學會文件寫成**報導聲稱**；沒有取得它們的原件。R20 的封口信、畫者、關門和讀報人都明示想像卡通，`moon019` 只容一本 1859 重印本。`moon024` 的關門表達遠離讀者，未呈現存世檔案；`moon025` 的後方關櫃也只是「不可即查」的對比。這兩景原圖仍須防模型添出可讀標籤或文件堆。

六景修法各對準已見錯誤：`moon017` 大報平放並露出前臂；`moon019` 讀者將唯一小書舉在胸前；`moon020/021` 指定成年、1830 年代衣裝及窗光；`moon024` 移除桌、盤、箱與文件；`moon025` 改成年讀者與 1835 報攤。提示詞仍使用系列的可愛卡通風格，不把所畫者當作照片、可核肖像、原報或真實觀測站復原。

獨立逐字檢查六項 `data.prompt` 與 claims 畫面欄：現行 `video.json` SHA-256 `b557ddb82e51608adf48052b3174ca8f72e309ee4476df630b3993da14afb8d9`，`claims.md` `84e81619c5e57981515a79d4ec3b97c976a9eb72cfb5fc5e8dd2050765d59617`，`script.md` 不變 `82369f762cc64f70e300e2104a16af3b8e99f1e3296dd81a34152e967f0ecb0a`。只把六個新字串各還原一次，原始位元組分別回到 R19 `a62df2aa4003850b38011dcd2877105bf2d98fe4fc36584304655a1d43ef2928`／`3ca1287ab6b9e579be65c975c3cc7a393beba869c28f29515f1bfe756b5481ec`；其餘 **123／129 景**與旁白、既有 KEEP 景的提示詞未改。`lint --json` 為 **0 errors／0 warnings**、131 句。六景 `--takes 1 --dry-run` 報 MiniMax `image-01` 1K ready、約 US$0.08；付費前帳本 US$0.8100／60 image／60 judge／0 配樂、保留額 0，整集累計上限 US$5.30，`STOP` 在位。

**放行範圍：**僅在 EXIT trap、同一上限和逐張原生圖人工檢查下作這六景一輪。機器 PASS 不覆蓋來源、年代、文字、人物主動作或黑邊的人工 HOLD。`moon028/030/031` 及其他批次不在此放行範圍；網站卡與人耳審核狀態不因本書審改變。
