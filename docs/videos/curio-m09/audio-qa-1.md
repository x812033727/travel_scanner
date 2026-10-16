# M09 繁中旁白 QA 第 1 輪

日期：2026-10-16。劇本 video.json SHA-256 795BA47D4864702D6476B75653F27F0E4B09665D3D4D783C80C555498B3F5637，逐句音訊與 timeline 留在 C:/Users/x8120/mokaair-work/videos/curio-m09。旁白 95 句、533.1 秒（8:53.1）。check-audio 在有證據的 502 單筆恢復後讀回 95／95 句；前 20 句用原快取，另轉寫 75 句，Jev 判讀 1 次。70 句逐字吻合、7 句同音或語助詞差異、4 句 Jev 判可接受、14 句仍被自動標記。詳見 audio-qa-502-recovery.md 與本機 review/check.json。

## 初步旗標分流

依自動轉寫文字初看，沒有足夠證據立刻重錄。需要站主特別試聽的 7 句：ta55（遮／留）、ceuu（研究／眼中）、c6qp（整件原物／只見圓物）、pk3b（機構／結構）、bauw（競技／經濟）、28eg（前盤／前半）、gfsv（證據缺失太多／證據確實是太多）。另 7 句 j3at、ydxy、i5mw、5tiw、bi9k、w3c9、ams3 較像同音字或辨識偏差；目前沒有離線第二套轉寫收據，不能據此判定讀音正確。

逐句試聽頁：C:/Users/x8120/mokaair-work/videos/curio-m09/review/audio.html。離線 Whisper 因主機負載尚未產生第二份可用逐句結果，未把初步文字分流當作試聽證明。已送後台音訊關卡，review-pull 讀回 waiting for the owner；有未解旗標時須由站主試聽核准或指出句 ID。M09 插畫尚未啟動。

## 試聽核准與離線補充轉寫

站主回覆已試聽並於後台核准；協調者以 `review-pull --gate audio` 現場讀回 `audio: approval recorded`，隨後才預留本集插畫估額並啟動產圖。另一套本機 `faster-whisper small` 對上述七句離線轉寫已完成，收據為 `C:/Users/x8120/mokaair-work/videos/curio-m09/review/whisper-small-targeted.json`，SHA-256 `19850432A28CCD2DA7D82029AE340E263D5435210EE0EEEF857F77DC9B454862`；無新增付費呼叫。`ceuu`、`c6qp`、`bauw`、`28eg` 的關鍵語義與正式稿一致，`pk3b` 的「機構／結構」不改命題；`ta55` 對「遮」辨成「周」，`gfsv` 對「缺失」辨成「確實」，不能把離線 ASR 當人工試聽證明。這兩句已在站主指定試聽範圍且經站主核准，現有 WAV 沿用；若後續成片複查聽出具體錯字，再只重錄對應句子。
