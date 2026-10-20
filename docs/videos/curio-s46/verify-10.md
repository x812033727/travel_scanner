# S46 R5｜雙盲失敗後的敘事修補（作者自查）

2026-10-20 UTC。[R4 雙盲](verify-9.md)的兩名新讀者共同判 `one_line`、`no_toc`、`chapters_link`、`no_recap` 為 No；B 另判鑰匙孔段落 `no_detour` No；A 指兩個伏筆回收標記早於真正答案。本紀錄只說明 R5 修稿者的自查，**不是獨立敘事、史料或畫面 PASS**。1895 年自傳的固定版本與 R4 相同；沒有取得獨立校方原件。

## 精確 R5 版本

| 對象 | SHA-256 |
| --- | --- |
| [Blackwell 1895 固定原書](https://github.com/GITenberg/Pioneer-Work-in-Opening-the-Medical-Profession-to-Women_65496/blob/16787df4911754c8e0401d12c896b943768f5d8d/65496-0.txt)，commit `16787df4911754c8e0401d12c896b943768f5d8d` | `b52caf559d763349953fe31101016cfb2d68662f152c28a564b6a6b93cac8ec6` |
| `research.md` | `99b8903431cb1e8a317513f260c33a5cd0d141aefec54b4c0a5ba205c126055d` |
| `brief.md` | `744b28fa28553f855aaa5a022bb48cef3d3ea4089dc9c74d0639e22b91bf28d3` |
| `claims.md` | `a8ca750d0c3b7e3777e6e123603d01c2975e130e1267d8050ede59597c861b2a` |
| `video.json` | `c69d4e7438eb7ec255330bc271bef40592e998838ff4d10da6cc1d2d3362fd8d` |
| `script.md` | `93039b2a79cac8f9005e99eb81062c5b83743f4c5018163f3062aa9228e019d0` |

## R4 盲讀意見與 R5 差分

| 意見 | R5 修法與史料界線 |
| --- | --- |
| 開場後目錄式宣告；未從「玩笑表決」接入主線 | `bkw010` 改成她在申請送到學生面前以前，已向幾位醫師求教女性可否成為醫師；`bkw011` 緊接醫師的否定答覆。這是行動與回答，不講述影片編排。據自傳 [L1007–1023](https://github.com/GITenberg/Pioneer-Work-in-Opening-the-Medical-Profession-to-Women_65496/blob/16787df4911754c8e0401d12c896b943768f5d8d/65496-0.txt#L1007-L1023)。第二章改名「她向醫師詢問學醫之路」。 |
| 五月信倒回六月二日之前 | 原 `bkw029–033` 的教育家信移至私人解剖課後、五月二十七日訪 Jackson 前；現 `bkw017–021` 先述 **五月二十四日**的圖書館、醫院與私教費用，再述五月二十七日、六月二日。信日期只印「Philadelphia: May 24」，1847 由上下文得知；旁白未替日期行加年份。據 [L2066–2097](https://github.com/GITenberg/Pioneer-Work-in-Opening-the-Medical-Profession-to-Women_65496/blob/16787df4911754c8e0401d12c896b943768f5d8d/65496-0.txt#L2066-L2097)及 [L1982–2020](https://github.com/GITenberg/Pioneer-Work-in-Opening-the-Medical-Profession-to-Women_65496/blob/16787df4911754c8e0401d12c896b943768f5d8d/65496-0.txt#L1982-L2020)。 |
| 畢業後回望又退回求學；「騙局」須保留晚年來源層 | 原 `bkw083–085` 移至她初進講堂後的 `bkw067–069`；不再畫老年 Blackwell。旁白仍說「她後來回憶」，只把 1895 年自傳當作對**當時申請**的後見證據，不把回憶裝作 1847 年當場對話。`bkw069` 同時引書中轉錄的學生決議，清楚區分申請被懷疑與決議文字；個別投票動機仍不可知。據 [L2436–2442](https://github.com/GITenberg/Pioneer-Work-in-Opening-the-Medical-Profession-to-Women_65496/blob/16787df4911754c8e0401d12c896b943768f5d8d/65496-0.txt#L2436-L2442)及 [L2181–2207](https://github.com/GITenberg/Pioneer-Work-in-Opening-the-Medical-Profession-to-Women_65496/blob/16787df4911754c8e0401d12c896b943768f5d8d/65496-0.txt#L2181-L2207)。 |
| 第一天五堂課即時重述；床頭卡慣例重述 | `bkw061` 改用同一封給姊妹的信中**示範員猶豫讓她參加解剖**的新資訊 [L2239–2247](https://github.com/GITenberg/Pioneer-Work-in-Opening-the-Medical-Profession-to-Women_65496/blob/16787df4911754c8e0401d12c896b943768f5d8d/65496-0.txt#L2239-L2247)；病房段先一次說舊慣例，再說住院醫師離開、卡片停填及她自己作紀錄，刪第二次慣例解說。據 [L2657–2665](https://github.com/GITenberg/Pioneer-Work-in-Opening-the-Medical-Profession-to-Women_65496/blob/16787df4911754c8e0401d12c896b943768f5d8d/65496-0.txt#L2657-L2665)。 |
| 鑰匙孔插曲沒有推進臨床資訊障礙 | 刪原 `bkw099` 的書桌與鑰匙孔。她住進醫院後直進女病房、先見卡片舊慣例，接住院醫師迴避與卡片停填；入院前卡片提示仍只畫一名男性住院醫師。 |
| 伏筆回收標得過早 | 濃縮開場演示課 `bkw006` 的 payoff 改指 `bkw083`「熱烈贊同、走回座位」；醫院 `bkw097` 改問能否得到臨床資訊，payoff 指 `bkw103`「自行整理所見」。另把首次課堂測試 `bkw062` 的 payoff 指向 `bkw066` 真正坐下聽課。 |

## 形式與長度自查

- `VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs script --slug curio-s46` 已重生上列 `script.md`；`lint --slug curio-s46 --json`：**0 errors、0 warnings**。127 個內容景的旁白逐句與 `claims.md`、`script.md` 相同；122 張 `shot`、5 張來源卡，插圖比率 96.1%，18 組 `loops`。
- 工具估計濃縮開場 **45.37 秒**，開場後至口播片尾前正文 **685.23 秒（11:25）**，口播片尾 **16.37 秒**，全口播約 **12:27**。正文 2,357 漢字，以每秒 4.5 字、不計停頓的保守朗讀仍約 **8:44**。以上均非合成語音或成片實測。
- 1847 年學生決議仍只稱自傳轉錄、其文字寫一致歡迎；晚年「騙局」只限部分學生對申請的懷疑。Blockley 的「一致准許住院」不說成另一場正式投票。`bkw008` 的 1849 年倒敘仍稱成年女子；夜抵日內瓦及翌日冷雨提示、考試後文憑／離城的來源行號已逐景核對。

R4 的來源／書面畫面 PASS 綁定 R4 文本，不能自動繼承到 R5；R5 須由未參與修稿者核對本次差分與全片書面畫面，再交兩名**全新**讀者對同一新版劇本盲讀 13 題。網站審核、付費媒體、成片及可點連結均尚未開始。
