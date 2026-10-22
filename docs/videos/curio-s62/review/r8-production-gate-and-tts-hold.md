# S62 R8｜推薦 A 案核准、媒體報價與語音服務停點

2026-10-22 UTC。R8 [獨立固定史料及畫面](r8-independent-source-visual.md) PASS（114／114 旁白、110／110 插圖文字、4／4 資料卡），[兩位正式盲讀合併](r8-formal-merge-audit.md) 13／13 PASS。`brief.md` SHA-256 `5941ebf974ad67a9926d0b56311389fd8f820d14d47f31b3e55f1b1eb31b3021` 提供 A／B，作者推薦 A「每天少一顆、又多一顆」。站主先前於對話概括授權「用推薦的決定就好不用問我」。因此本機依此選 A，向網站各送出一次 outline/script 後台審核卡，並以 `approve --gate outline`、`approve --gate script` 對精確雜湊記錄**代行核准**；網站因本集是本機手動稿而標 `hand_pushed`、卡片仍 pending，**不宣稱站主親自讀過、聽過或點選後台卡片**。本機私有 `approvals.json` 記錄大綱 `5941ebf974ad…`、劇本 `c638b0d28cfb…` 及上述來源於對話的授權。

正式 `lint --json` exit 0，0 errors／0 warnings，114 句，7 章；正文保守 325 CPM 估 **8.254 分鐘**，開場約 **46.53 秒**，影片總估 10.956 分鐘。政策一次性預檢使用網站 `judge/policy`：Jev `passed=true`，回覆「符合立場 0.71、有示範：不適用（解說）、建議 0.01、業配 0.14，通過」；完整回答只存私有工作目錄 `policy-preflight.json`，這仍不是完片 QA。

`tts --dry-run` 報 **114 句／2,514 個計費字元**，頻道聲線 `gemini:Sulafat` ready、當月餘額 7,887,491 字元；**沒有語音費用估算需要預支**。`media-status` 當時顯示 MiniMax image-01 ready、當月餘 10,066 image／8,546 judge／28 music，這集已支 US$0。`keyframes --dry-run --takes 3` 對 **110 個插圖景**報一輪約 **US$1.48**、最多三輪約 **US$4.46**；`music --dry-run` 因還沒有 TTS timeline 拒絕報價。整集插圖加配樂上限須等同版 timeline 與音樂正式 dry-run 才能精確定額；**未開畫、未生成音樂，也沒有收圖**。

唯一一次實際 `tts --slug curio-s62` 在約 42 秒後以 exit 4 回「Gemini 語音暫時忙碌或達到用量上限，請稍後重試」。私人工作目錄只有 `approvals.json` 與政策預檢答覆，**無 timeline、音檔或 speech journal**，114 句仍待合成；沒有立刻再送同一請求。此前 S60 亦遇 429／同類忙碌，下一次建議不早於太平洋午夜每日額度重置後的 **2026-10-22 07:05 UTC**，到時先重查 `media-status` 與聲線、服務，再單次重試；若仍 busy 則停，不循環佔用額度。語音逐句 `check-audio`、實測正文 ≥8 分鐘、真人聽音、整集報價與插圖均尚未過關。
