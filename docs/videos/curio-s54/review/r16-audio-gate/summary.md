# S54 R16｜新版旁白與完整音檢

2026-10-20 UTC。**本地機器音訊 PASS：148／148 句完整音檢，0 旗標。** 精確 R16 五檔及前置關卡見[作者凍結](../r16-author-oral-repair.md)、[獨立史料與書面畫面 PASS](../r16-source-independent.md)、[正式雙盲敘事合併與 Jev 政策 PASS](../r16-merge-policy/summary.md)。這不是人耳或站台審核核准，也不代表長片／Shorts 成片。

R15 經兩輪重錄仍有 `s54002`、`s54013` 兩句旗標，當時已停工。R16 修改這兩句的口語與對應主張，完成新版查核後才解除舊版 `STOP`。Sulafat 乾跑預報 146 請求、其中 **2 句需新合成，約 50 計費字元**；正式執行為 2 新請求／50 字元、144 沿用。前後 148 個 WAV 的 SHA-256 核對，**只有** `s54002` 與 `s54013` 改變，沒有增減檔。實測旁白 **13:55.13**，第一章濃縮開場 **45.40 秒**，後續 **13:09.73**。

完整 `check-audio` 回傳退出碼 0：**112** 句逐字吻合、**27** 句僅同音字或口語填詞差、**9** 句經 Jev 判可接受、**0** 句旗標。本目錄保存原樣 TTS／音檢輸出、完整 `check.json`、`check-flags.json`、timeline、WAV 前後雜湊及執行摘要；77 MB 旁白 WAV 留在本機 `/workspace/.video-work/curio-s54/narration.wav`，沒有進 Git。兩句新音訊全片複檢後不再重錄。

已執行 `review-push --gate outline`、`--gate script` 與 `--gate audio`；手動推送的三張站台卡均**待站主審核**，`review-pull --gate script` 與 `--gate audio` 均回 `waiting for the owner`。推送劇本後重算 SHA-256，仍與 R16 凍結值相同。本月圖片 judge 20,000／20,000、配樂 60／60；插圖、配樂、組片、字幕、Shorts、私人 Studio 上傳及可點片尾尚未完成。
