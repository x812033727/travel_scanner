# S29 初稿自查與獨立複核交接

2026-10-19；**前製稿，不是盲評通過證明，也不是聲音、插圖或成片驗收**。

## 固定稿件與來源

| 檔案 | SHA-256 |
| --- | --- |
| `video.json` | `c49a5e3e571073fc5d12456bccc408f79845c069a98a348623b9f3d47d0eaabc` |
| `script.md` | `aa34515f83ee059760f2c574dfe6eb83e8c006dc1240178aed3354126fab2755` |
| 《三國志》卷二十固定 HTML | `dec2ae1713a56e2a33d367d691904004db60740f9490023b52695bfd3740bbc8` |
| CBETA《雜寶藏經》固定 XML | `0b0d59c2c02da42fae95e3ed48f64e20813602b6f48032770a0ce557a6ff90b1` |

兩個來源的固定 commit、可點連結和逐段定位見 [research.md](research.md)；旁白每一行的主張對照見 [claims.md](claims.md)。兩份 raw 檔此次重新下載，SHA 與原來源可行性備忘錄相同。`video.json` 的 `sources[]` 帶同樣的固定 URL 和 hash。任何改稿之後都要重算這張表並重新盲評，舊稿評語不能沿用。

## 本地檢查

- `node tools/video/cli.mjs lint --slug curio-s29`：**0 errors, 0 warnings**。格式為 `drama` 解說、系列 `cute-mystery` preset、110／110 張正文 `shot` 插圖（100%，高於 70% 下限）、連續正文卡片 0、10 組 `loops`、開場約 43 秒，配樂欄已設定。
- `node tools/video/cli.mjs script --slug curio-s29`：產生上述 `script.md`，敘事摘要 hash `5bc7a3589aaa8812`。這是工具檔案版本標識，並非獨立讀者盲評。
- `estimateTimeline(video.json)`：開場第 1 景至正文第 1 景約 **43 秒**；正文第 2 章起點至 `outro` 起點估算 **603.97 秒／10 分 04 秒**，超過 480 秒門檻約 124 秒；全片估算 658.57 秒／10 分 59 秒。這只是文字估時；實際 Gemini TTS、停頓和剪輯後要從 `timeline.json` **量正文**，片頭片尾不可補正文下限。
- `npm run check:tasks`：通過（2082 份任務檔；既有其他任務的持有過久及 scope 重疊警告）。
- `npm run test:docs-videos`：**236 passed, 0 failed, 0 skipped**。
- `git diff --check`：通過；本票只編輯 `docs/videos/curio-s29/` 與自己的任務檔。

## 交給新讀者的盲評題

請新讀者先只看 **SHA `aa34515f…` 的 `script.md`**，照 `.agents/skills/youtube-video/references/script-writing.md` 的十三題說故事關卡逐題判是／否，重點核對第一章是否只種鉤而不提前揭曉、每章接前一章的具體動作、是否只有水痕這一條主線，以及《三國志》後的小馬鞍插段是否仍服務於人物傳記而非岔題。若有任何「否」，給行號與原因後退回修稿；新的稿件須重新計 SHA、lint、估時和盲評。

再由**未參與撰稿者**拿固定版兩份原文和 `claims.md` 查逐句來源：曹沖傳只說「物」，經文才說「石」；兩個人物／場景不合一；北魏漢譯的較晚署年只能界定漢譯層，不能替原故事定年，也不能推出借用、首創或傳遞方向。視覺提示詞需確認區分漢末人物傳記、經文譬喻與現代讀書場景，不讓影像暗示當場史料未說的師徒或同日互動。

新讀者通過、相應站主關卡完成以前，**不跑** Gemini TTS、MiniMax image-01、音樂或成片等付費媒體。通過後依 skill 做 `tts --dry-run`、實際旁白與 `check-audio`、整集插圖一次報價、配樂、組片；最後以實際 `timeline.json` 驗證正文 ≥480 秒，再進入品管和上架包。本次未產生任何付費媒體。
