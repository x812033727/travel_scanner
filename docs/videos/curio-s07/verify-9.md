# S07 辨音改稿、獨立盲讀與旁白複核

查核日：2026-10-19。`script.md` SHA-256 `73ace39d6b07a68d59bf077b6bd6e30a565fb5d86baed910d6f774183eb169b2`，95 句／86 插圖／六章；`lint` **0 errors、0 warnings**，劇本估 8.1 分鐘。

前版 95 句旁白的首次 `check-audio` 標出六句。只重錄這六句後，三句仍被同樣誤辨：`eb061`「橋西」成「譙縣」、`eb065`「小說」成「笑聲」、`eb071`「第三聲」成「低聲」。因此只將這三句改為「軍報送出後，曹操會親自趕來嗎？」、「曹軍聽得腿都發抖，曹操卻還在橋邊。」及「張飛第三次大喊：『戰又不戰，退又不退，卻是何故？』」。前後句仍明說這是小說場面；逐句主張表同步更新，沒有添加史實主張。

新讀者在看史料與舊審稿前，先只讀新雜湊的劇本，逐題原始答案 [`blind-9.json`](blind-9.json) **13/13 通過**；CLI 確切 narrative hash `3836c13439825546`、round 5、12/12 必要題加一選答、0 失敗／警示的回執見 [`narrative-9.json`](narrative-9.json)。讀者之後才按 [`research.md`](research.md) 固定的《三國演義》第 42 回 [第 36–49 行](https://github.com/Ancient-China-Books/sanguoyanyi/blob/761813427eb5685c395804493f9fbd7ad8dc7d8d/OEBPS/Text/418.html#L36-L49) 抽查三句：飛報曹操與其親自到橋邊、曹軍「盡皆股慄」而曹操尚在場，以及前兩喝之後的第三句挑戰均有依據。這些鏡頭仍在小說限定段內；橋前騎者、曹軍扶馬及張飛挺矛的畫面未把它們宣稱為史書實錄。審讀前後劇本完整 SHA-256 一致。

依使用者既有「以你推薦的就好不用問我、一直做完所有影片」授權，代理把此版劇本送後台（pending）並透明記本機核准；沒有宣稱站主本人逐句親閱。頻道 Gemini／Sulafat 只新合成三句（57 billable characters），其餘 92 句沿用音檔。`narration.wav` 實測 **544.333 秒（09:04.3）**；新劇本 `check-audio` **95/95、0 旗標**：88 逐字相合、6 同音字或語助詞、1 Jev 接受。已送後台 audio 審聽（pending），並依上述持續授權透明記本機 audio 核准；這是轉寫核對，未宣稱站主本人親聽。

Lyria 背景配樂已生成，花費 **US$0.08**。`music/manifest.json` 指定 `music/82b387efed6e4bab.mp3`、SHA-256 `14d84291eb07e4248b140bdb81ebdb813592dfca42cfbed55699376ace8f21b4`，標記目標 550 秒；`ffprobe` 實檔僅 **177.633 秒**，組片時需循環，成片後檢查循環接縫及片尾沒有無聲段。媒體檔在 `/workspace/.video-work/curio-s07/`，不進 Git。S07 付費插圖仍暫停，等待系列負責者分配 MiniMax 額度。
