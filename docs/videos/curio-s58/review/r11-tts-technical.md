# S58 R11｜旁白合成與時間軸技術收據

2026-10-21 UTC。對 [R11 凍結稿](r11-author-freeze.md)使用本地委派 A／劇本決定與[單次 3300 字元上限](r11-policy-and-gates.md)，執行 `NODE_USE_ENV_PROXY=1 NODE_NO_WARNINGS=1 VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs tts --slug curio-s58`。**146／146 句新合成、0 沿用，實際 Gemini 計費 3098 字元**，未超本地字元上限；聲線為 `gemini:Sulafat`，網站原先顯示在免費層內。CLI exit 0。這是合成成功，不是逐句音檢或站主試聽核准。

私有工作檔 `/workspace/.video-work/curio-s58/narration.wav` SHA-256 `676b1b229a24b54d38a0393c3c8428347a4c7bed39dae01e91ef2510685b86f0`；`timeline.json` SHA-256 `c69b43517398b16b9805fea7526aecba0c51cbf36f6dac38fe45edf774c1f525`。WAV 用 `ffprobe` 實測 **763.666667 秒＝12:43.67**，與時間軸 `22910 frames / 30 fps` 一致。第一章濃縮開場 `s58001–s58010` 於時間軸第 1525 格結束，為 **50.83 秒**；之後六章正文 `21385 / 30 = 712.83 秒＝11:52.83**，達非漫劇長片的八分鐘下限。這裡是實際旁白時間，尚未加入固定 5 秒片頭和 21 秒片尾。

接著完整執行 `check-audio`，區分語音錯誤與 ASR 的同音、標點、姓名異寫；只有經確認的問題句依系列上限補錄。站台音訊卡尚未送審或核准，插圖／配樂／合成／可點結束畫面仍未完成。
