# S40 直式精華：最終成片與待上架條件

2026-10-20。這份紀錄取代 [初稿查核](short-verify-1.md) 的製作狀態，保留初稿的修正歷史。現行 [shorts.json](shorts.json) SHA-256 為 `9fe9b8a0c6ca3c867aed8300e6e778150cdd7f79eb45a7f42faa241df7ab456e`；來源長片 `video.json` SHA-256 為 `5f8d6af62b3bd93550ea00effc44d9a9faf31dd4a513d31d3eb27599c8fbc2e2`。`from-episode --check` 對一支 Short 和所有入選長片影格的 SHA 均通過。

成片在 `/workspace/.video-work/shorts/curio-s40-short-1/40c6748b61c8f9f3-1792496854572/upload/`：33.000 秒、1080×1920、30 fps、H.264/AAC。`final.mp4` SHA-256 `e5792d7165c3e481aa1a0ab2ecdb176d358775921caa7b9723de1f2e244d7532`；`script.json` SHA-256 `5117e5d9f9b5cc631425982eb9c717e7ab32f79500a2e9d499fa0f917d86026f`。十句頻道聲線旁白經正式逐句音檢 **10/10、0 旗標**；輸出 −14.02 LUFS、真峰值 −1.10 dBTP。包內有封面、繁中及 en／ja／ko 定時字幕、標題、說明與 metadata；其他語言字幕是依繁中時間翻譯，未有母語盲審。

獨立來源審核逐項對照固定版普魯塔克《安東尼傳》`674.txt` SHA-256 `11a1bb9a5d5a8436f2d4d7adf3ad91ec05bb8aef850e564ce255cf9ba2fabdd1`，十句旁白、七張標題與兩個標題，共 **19/19 PASS**。證據在 `/tmp/s40-short-independent-verify.json`，SHA-256 `cb44905f1bb6ce9eac06092329a0ed5e0b4476cdaa6d990ba16e0432f0f157b6`。原尺寸 MP4 的開頭及結尾都展示**完整原長片插畫**：左邊無花果籃，右邊帶蛇女王像；先前裁切掉蛇像的版本已棄用。其餘五幕字幕在安全區內，沒有描繪確定的咬傷或死因。詳細逐格紀錄在 `/tmp/s40-short-independent-native.md`。畫面是卡通示意，不是凱旋式或陵墓的現場證據；普魯塔克也明言真正死法不明。

站台正式 QA SHA-256 `b85bc3cdfee6838debaa2a58d70b412894723e9cc6ce944c1c18e14ad02a0acf`，**10/13**：profile、loudness、layout、narration、facts、policy、captions、variety、disclosure、grammar 通過；`evidence` 因長片在站台尚未 final 核准或公開而未過，`metadata` 和 `links` 因長片尚無真實 YouTube URL 未過。最初在 Shorts 站台專案尚未登記時，Jev 誤用教學片的「示範」問題；依現行 `line: cut` 正常登記專案後重新問正式評審，**精華立場通過**（0.85、建議 0.01、業配 0.02），保留兩次結果，沒有改寫舊 QA。兩個原典網址在獨立檢查時均 HTTP 200。

`package` **3/4**：files、captions、disclosure 通過；descriptions 等待長片真網址。`metadata.json` SHA-256 `941761b4bca885ed6a91f68dc8584277dfcb51a3efb8f4158e48549c553c1082`。`shorts push` 已把現行 MP4、封面、影格證據與上述 QA 送入 `/admin/videos`；final 審核回覆 **hand-pushed pending**，未有 publish 審核或 YouTube 上傳。這不是「13/13 已過」或「已發布」。

長片在 Studio **私人上傳、取得真實影片網址**並完成站台 final 決定後，將真網址寫入 Short 說明，再重新 `qa`、`package`、`push`，處理新版本的審核。Short 須在真正可連回長片後才公開。長片片尾最後 16 秒的可點推薦影片與訂閱元素仍須在 Studio 安裝及實測；Short 不能代替該步驟。
