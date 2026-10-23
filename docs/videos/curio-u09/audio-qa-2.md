# U09 新劇本旁白與音訊 QA（2026-10-16）

- 後台讀回已核准現行劇本：`video.json` SHA-256 `719CFEA737CFCF0C21D704CB91B3085F28F83B46DCD10682A704A62996617E17`，`script.md` SHA-256 `9D29AB194E348DEEF820A4FD8816DE71447B7113EDC6BDEB18789F48FB5B56D8`。舊版核准不沿用。
- `tts --slug curio-u09` 只合成 15 個變動請求（398 個計費字元），重用 86 個快取請求；新版旁白 9:54。`timeline.json` SHA-256 `CC8A4E3F1D25713747A446784F513F659F41B22F527DFA6C1FAAEA32D42EDA38`。舊音訊核准已因時間軸變更失效。
- `check-audio` 檢查 102／102 句：58 逐字吻合、25 同音字或填充詞差異、2 由 Jev 接受、17 句留旗標；僅 15 句新轉寫及 1 次 Jev 判讀。`check.json` SHA-256 `BCF65AFF49A778840C8FC16AC68352458B96C75AFC8F1EA331FB94A40FA77D0A`，旗標檔 SHA-256 `B4DC01A4AFBCA35B96E22C750C19678E1379C8DC392DBB1F11304AB4520130FD`。
- 與 repo 外上一版 `review/audio-triage.md` 的 17 個旗標 ID 比對，本版 16 個為站主先前已試聽並核准的舊句；`8ac591de` 本版不再列旗標。唯一新增旗標是 `1dfdcacf`：核准稿「那串脈衝究竟來自多遠？」；Gemini 轉寫「微弱脈衝，究竟來自多遠？」。新 WAV SHA-256 `50AEBB2FB57DB2304E5242C0E56402F08C10A1FB4E1D89F1D8C99832EEBC4AA1`。轉寫不能單獨判定實際讀音，須定向試聽。
- 已重新產出 `review/audio.html`；`review-push --gate audio` 已將現行時間軸送後台，回應 `pending`。本機 faster-whisper 嘗試受到環境執行遲滯，未取得可信的第二份新句轉寫；不將它寫成通過或錯讀。若站主確認 `1dfdcacf` 讀錯，只重錄此句、重跑音訊 QA，再送新版音訊；若確認正確，仍須由後台核准現行時間軸。
- 共用估算停手帳本先預留並核銷新版 TTS US$0.05、音訊 QA US$0.50；U09 累計保守估算 US$4.7735／US$6。供應商最終帳單仍未提供，不能把估算當實際請款。未執行新版插畫、分鏡或成片。
