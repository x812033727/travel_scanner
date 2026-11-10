# S58 R11｜媒體就緒只讀覆核

2026-10-21 UTC。只核對 R11 企劃、分鏡、工具與本機素材，並執行不提交付費請求的檢查；沒有產生本集插圖、配樂、成片，也沒有送審或核准站台關卡。R11 的史料與敘事前製結果見 [正式合併](r11-merge/summary.md)；站台 outline/script 仍 pending，見 [政策與關卡收據](r11-policy-and-gates.md)。

## 排法與已備素材

- `brief.md` 指定 **30–60 秒濃縮開場 → 固定 5 秒片頭 → 至少 8 分鐘正文 → 固定 21 秒片尾**，片尾最後 16 秒留兩個推薦影片框與訂閱圈。`video.json` 的首章為 `s58001`–`s58010`，下一章從 `s58011` 開始；共 146 景（141 個 `shot` 靜圖、5 張 `big` 卡），`look.preset` 為 `cute-mystery`，配樂設定為系列固定提示詞、`gain_db: -20`、`duck_db: -10`。首章十句已存在的 WAV 語音長度合計 **40.67 秒**，落在濃縮開場範圍內；這不是最終 timeline 的章節時長。`lint --slug curio-s58` 為 0 errors、0 warnings，僅預估全稿 13.7 分鐘；最終正文是否 ≥8 分鐘仍以完成的 TTS timeline 為準。
- S58 的 JSON 沒有內嵌片頭／片尾欄位，本集工作目錄目前也沒有 `branding.json` pin 或 `final.mp4`。`core/branding.mjs` 對這種無角色旁白長片在首次 `assemble` 取全頻道 current，預設 `intro_at: after_first_chapter`；`assemble/cli.mjs` 以 timeline 第二章起始格切開正文，`assemble/branding.mjs` 按「首章正文 → 片頭 → 其餘正文 → 片尾」合成聲畫，成功檢查後才寫本集 pin。若首次合成前全頻道 current 改變，S58 會取當時的版本。
- 目前 `/workspace/.video-work/_branding/current.json` 指向 **`curio-archive-original-candidate-20261020-v1`**，它是本雲端環境的原創候選，**與先前核定的 v4 素材不是同一組 bytes**。已安裝 intro SHA `a5ae205fcf6fa7c92998ac4991225e54206fff482cf03493a60cfb2519e8fcef`、outro SHA `275475470f1b7b5d93a2948f561d6e300d0406f9a5b2ab17cfb0dfe4bb3f34ee` 均與 current 相符；`ffprobe` 分別讀到 150 與 630 格、1920×1080／30 fps、48 kHz 雙聲道 AAC。抽取片尾第 0、150、300、629 格檢視：第 150 格起兩個影片框和訂閱圈清楚可見，持續到末格。候選來源與其審看限制見 [素材紀錄](../../branding-release/2026-10-20-curio-local-bookends.md)。這只證明已裝候選素材的畫面和時長，不是 S58 成片驗收。
- 成片的三個框只是視覺定位。可點的兩個影片元素和訂閱元素必須在**私人上傳後**由頻道站主於 YouTube Studio 匯入範本 `oxEtlA8GWas`，把開始時間對到成片終點前 16 秒，儲存並點測；MP4 及 YouTube Data API 都不能自行安裝這些連結。S58 `youtube.video_id` 目前為 `null`。

## 不付費檢查、報價與尚缺條件

| 檢查 | 本次結果 |
| --- | --- |
| `node tools/video/cli.mjs lint --slug curio-s58` | exit 0；0 errors、0 warnings；146 句、13.7 分鐘為估算值。 |
| `NODE_USE_ENV_PROXY=1 NODE_NO_WARNINGS=1 node tools/video/cli.mjs keyframes --slug curio-s58 --workdir /workspace/.video-work --takes 3 --dry-run` | exit 0；141 張、0 結尾延伸影格；MiniMax `image-01` ready。首輪全片約 **US$1.90**，每景最多三次約 **US$5.71**。此分支只讀伺服器 status、印出提示詞和報價，不提交生成請求。 |
| `NODE_USE_ENV_PROXY=1 NODE_NO_WARNINGS=1 node tools/video/cli.mjs media-status --slug curio-s58 --workdir /workspace/.video-work`；同指令加 `--json`，查 `.status.models.music.gemini[0].usd_per_track` | exit 0；Gemini `lyria-3.5` 音樂已啟用，每首價目 **US$0.08**；本集媒體帳本 **US$0.00**，站台單片硬上限 **US$200.00**。 |
| `NODE_USE_ENV_PROXY=1 NODE_NO_WARNINGS=1 node tools/video/cli.mjs music --slug curio-s58 --workdir /workspace/.video-work --dry-run` | exit 2：`timeline.json is missing or was built for an older script; run tts first`。該 dry run 的程式在有效 timeline 後只查 status 和印報價，不送音樂生成。 |

按目前價目，**一輪插圖＋一首配樂約 US$1.98；每景三輪插圖＋一首配樂約 US$5.79**，不含語音重錄、超出三輪的改圖或任何其他新素材；站台 US$200 是硬上限，並非本集擬花額。141 景全為 `visual: still`，本集沒有規劃付費動態 clip。待 TTS 完成後可再用 `music --dry-run` 取得歌曲秒數與直接報價，並用 `timeline.json` 核定開場及正文時長。接著仍需實際生成、逐圖檢查、配樂、render／clips／assemble、字幕與成片 QA；本收據沒有宣稱任何 S58 媒體已渲染或可發布。

素材核對使用 `sha256sum /workspace/.video-work/_branding/1ffcf193d68dfface2d561c3362f69b8bfe8590a90b5d8fa257a8b783984a801/{intro,outro}.mp4`，逐檔用 `ffprobe -v error -select_streams v:0 -count_packets -show_entries stream=width,height,r_frame_rate,nb_read_packets -of json <file>` 查畫格，再用 `ffprobe -v error -show_entries stream=codec_type,codec_name,sample_rate,channels -of json <file>` 查音軌。片尾抽格用 `ffmpeg -i <outro.mp4> -vf "select='eq(n,0)+eq(n,150)+eq(n,300)+eq(n,629)',scale=640:-1,tile=2x2" -vsync 0 -frames:v 1 /tmp/s58-outro-contact.png`；這張 `/tmp` 檢查圖不是交付素材。
