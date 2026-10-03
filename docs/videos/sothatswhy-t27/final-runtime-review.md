# T27 實際成片 runtime 覆核

結果：**PASS_CURRENT_FINAL_RUNTIME_BINDINGS_AND_SAMPLES**。覆核者 codex-art-t27；記錄時間 2026-10-02T15:59:11.248Z。本次只讀檢查實際成片、時間戳、字幕、正常 gates、交付包與已保存的 backend GET proof，只寫本紀錄及 JSON。覆核者曾製作本集 SVG，沒有撰寫旁白或執行合成；插畫語義的獨立覆核由 codex-write-t27 的 `visual-review.json` 提供（目前 SHA `47a692798587e8b99cdb5c4f533eb743663347a4129d9de7ff02740c3f4397d1`）。

## 實片與完整解碼

實檔 `C:/Users/x8120/mokaair-work/videos/sothatswhy-t27/final.mp4` 的 SHA-256 為 `3894c35e2cd5860d0b834c1ba02578986600c15e1e4ce53d59d0b95f1e993016`；105455029 bytes。ffprobe 實讀 20644 video frames，影片與 AAC 音訊均為 688.200 秒（11:28.2），H.264、1920×1080、yuv420p、AAC 48 kHz 雙聲道。實測 `r_frame_rate=30/1`、`avg_frame_rate=103220/3441`，沒有硬套平均 30 fps。音訊封包 nb_frames=32258、decoded audio frames=32257 分別保留，不把 AAC priming 的差異当作掉幀。

完整 ffmpeg 解碼映射所有 video/audio 到 null，以實測來源 time base `1:15360` 輸出：exit 0、stderr 空、20644 幀、dup/drop 0、progress=end、out_time=688.200 秒；開始 15:42:49.691954Z，完成 15:44:20.250566Z。前後實片雜湊一致。

第一轮完整解碼也得到 20644 幀、exit 0，但 null 輸出留下 `8040 >= 8040` 的 DTS 警告；原始 JSON 與 stderr 沒有刪除或覆寫。來源 demux DTS 與排序後 PTS 均嚴格遞增。267.983398 與 268.016406 秒兩幀相差正的 0.033008 秒，卻在 1/30 輸出刻度一起四捨五入為 8040；改用來源 1:15360 後，相同完整流沒有警告。中間 `-enc_time_base:v -1` 曾被 wrapped_avframe 編碼器在 setup 拒絕，0 幀，獨立保留為失敗 setup 嘗試，未計入成功解碼。沒有改寫實片來掩蓋警告。

## 實測時間與畫面

Body nominal 為 20197/30 = 673.233333 秒；root PCM/PTS 實測 standalone body span 673.192968 秒、final 內 body span 673.300000 秒；137 狀態的最大起點偏差為 0.040365 秒。片頭 357 幀／11.9 秒、片尾 90 幀／3 秒，套用 branding `047ff12a4888185d8fb1cb0cd520f7a2e23b9c3538fe3f2e8d4cb35afb0720bb`；body 實檔 SHA `ee61d35e59cd381ca741749dc89c775859529deaaa14e2bc194b15874aa653f7` 與首輪 body 相同。正常 checks loudness 為 -14 LUFS、true peak -0.9 dBFS。

獨立實看四頁聯絡表，涵蓋 15 張 actual-final 取樣（13 張正文及片頭／片尾），另看 frame-003、010、012 的原尺寸圖。15 張及四頁的 bytes 雜湊全部與取樣 manifest 相符；沒有在已看樣本發現裁切、缺字、黑畫面或遺漏來源標示。17.2% 與 43.7% 為同 0–100 尺度的不同選項；日期、十人十一勾示意標示、每公里公式單位、六章卡及書擋均清楚。這是取樣實看；没有宣稱所有原圖或整支影片已由人完整播放。

root PCM/PTS 收據也逐一核對 narration WAV、body、final 雜湊。開頭／中段／最後一句的六個 PCM 比對，narration→body 偏移 0 秒，body→final 偏移 11.9 秒，量測誤差 0（解析度 1/6000 秒），最低 correlation 0.9999997180481223。這支持已取樣波形的對齊，不代替人完整聽音。

## 当前字幕、gates 與 backend 綁定

最後独立正常 API 檢查於 2026-10-02T15:55:50.807Z exit 0：checksCurrent、brandingCurrent、duration、chapters 全通過；137 still 的 render key/hash、130 SVG 的 spoken_text/caption/bytes 都符合目前 source；137 句 SRT/VTT 與目前 presentation timeline 的重新計算內容完全一致，片頭偏移 11.9 秒。286 個 source/render/caption/review snapshot 在檢查前後不變；另外把 root final-audit 的 283 個 snapshot 逐一重新雜湊，也沒有差異。

正常 QA 11 項、上傳包四項全部通過，outline/audio/final/publish 四 gates 都為 approved/current。QA 綁定 final MP4 SHA；package report 的 `final_sha256` 按正常 API 定義綁定 upload/metadata.json SHA `0b391df71413e3ea5ef4307b4984d332dd81174e43af5fc98b92e4ed0abe79d3`，不是 MP4 SHA。Upload/final.mp4 又逐 bytes 比對為同一支 actual final。旁白 check-flags 為目前 speech `e763f5bdd108bfa1`，0 flags。

保存的實際 backend GET proof SHA `bdc2f89fed065da15a9436a01a77c4fc138ea83e270bce2d7fd3a34867585c10` 與本機資料吻合：final review `cab3a243-7d28-433e-bca1-a0a4de07e247`、publish review `2922dac4-fd3a-438c-9614-128ddadd1cc2` 的內容雜湊/current gate 一致；全部九個 attachment（含 preview、contact sheet、thumbnail、narration M4A、字幕、說明、metadata、final）均和實檔重新計算的雜湊一致。

四道 gates 的核准依 backend 設定與自動 QA/Jev notes 成立，没有推定站主完整觀看／聽音。Backend 的 stage_label 雖寫 on YouTube，實際 YouTube ID 仍 null，on_youtube=false；語言選擇尚未決定，ready_to_upload=false。本紀錄不宣稱上傳、公開、站主完整播放／完整聽音或 native player CC 選取已驗證。這些保留狀態不改寫為通過。

## 收據

所有收據位於 `C:/Users/x8120/.codex/visualizations/2026/10/01/01a0f5cd-1f4c-7f91-9af1-b02370fcce78`，精確 SHA、完整命令、probe 與比對結果列於 `final-runtime-review.json`：

- `t27-independent-full-decode-initial.json` 及 `.stderr.log`：首次警告原始紀錄。
- `t27-independent-full-decode-source-timebase-option-refusal.json`：-1 setup 拒絕，0 幀。
- `t27-independent-full-decode-source-timebase.json`：完整音畫 clean decode。
- `t27-independent-video-packet-timing.json`：實際 DTS/PTS 與輸出格點證據。
- `t27-sync-readonly.json` 與 `t27-final-samples/manifest.json`：actual PCM/PTS 與實片取樣。
- `t27-final-audit.json`：root 正常 guards/count_frames；SHA `3d5ad153b104373edc3b5317d7601a4503eb3f4a252b14219adcb731411948c5`。
- `t27-remote-delivery-2026-10-02T15-52-00-323Z.json`：backend 實際 GET proof。

本次沒有尚未解決的 runtime/binding/sample 發現；本結論只對上述實際 hash 的檔案與已執行範圍有效。
