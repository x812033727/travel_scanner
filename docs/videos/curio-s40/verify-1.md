# S40 前製交接：獨立審核仍待進行

2026-10-20；審核對象為 `video.json` SHA-256 `0ba27dd49a63d8f8ed2abc6638bf8f9b772ca60470c460dd87a6aef6d70d9475`，`script.md` SHA-256 `026351063e493791b5b3a62bf5d0e16d2d184d6fa2b1662bf1666e4d98794ae3`。**本檔是撰稿者自查與交接，不是獨立查核結論、劇本核准或媒體品管。**

## 已完成

- 重新下載並核固定版本全文：普魯塔克 `674.txt` SHA-256 `11a1bb9a5d5a8436f2d4d7adf3ad91ec05bb8aef850e564ce255cf9ba2fabdd1`；蘇埃托尼烏斯 `6400.txt` SHA-256 `082eee2d55230c1f75f9476dae537fc37851487bc1cce5dfaef1ef2a67558b15`；狄奧 `10162.txt` SHA-256 `b0ce5d998a6eb78162fc6658b24b9efd0fd0aa23ce6a9bbe9fd10b584fdf4e83`。各 URL、提交與可見範圍見 [research.md](research.md)。
- A／B 大綱、84 張插圖景與 1 張 outro、85 句旁白的來源對應在 [brief.md](brief.md)、[claims.md](claims.md)。`look.preset` 為 `cute-mystery`，沒有付費語音、插圖、配樂。
- `lint --slug curio-s40 --json`：0 errors、0 warnings；估全段 9.41 分鐘，第一章後正文 00:36 至片尾前 09:17，約 8 分 41 秒；20 個 `loops`。這是**稿子估算**，後續須用實際 TTS 時間軸重測。
- `npm run test:docs-videos` 與 `npm run check:tasks` 均退出 0；task checker 仍列出此題無關的舊任務逾時與已存在的跨題範圍重疊警告。

## 下一位獨立審核者

1. 只提供 `node tools/video/cli.mjs narrative --slug curio-s40` 印出的劇本與 13 題，**先不要讀**本研究、主張表或歷來審稿紀錄。逐題作 Yes／No 並給稿中定位；尤其檢查開場是否洩漏結局、章首連接、`no_recap`、每個疑問是否以**新資訊**回收。再由協調者用 `narrative --answers <file>` 記錄正式結果。
2. 封存盲讀答案後，獨立重開三份固定全文，比對 [claims.md](claims.md) 的每句主張與 84 個 prompt。特別查：普魯塔克的無花果、器皿與中空髮簪都是「有人說」；狄奧的水罐／花與沾毒髮針亦是候選；蘇埃托尼烏斯寫 `supposed`。`Caesar` 在這些段落指屋大維，不是尤利烏斯・凱撒。蛇未找到不推出沒有蛇，凱旋式蛇像不推出女王必遭蛇咬。
3. 史料只在英譯層核過；未校古希臘／拉丁原文或當時驗屍／守衛記錄。畫面是情節示意；不能畫成確定的女王被蛇咬／用針刺手臂現場，也不能把當事人的私下動機或傳記對話當逐字錄音。

獨立敘事與來源／畫面審核未完成，仍保留前製狀態。任何改稿都需重新產 `script.md`、記新檔案雜湊並重新盲讀；付費媒體維持未開工。
