# X01 Adobe｜本機試看片獨立技術複查（2026-10-20）

**本機試看片的檔案、時間軸、音量與字幕檢查通過；正式音訊及頻道品牌審核仍未完成。** 本記錄只核對已輸出的概念試看片，不能取代人耳聽核或正式工人的 `final.mp4` QA。

## 交付檔與影音規格

媒體工作區：`/workspace/.brand-video-workdir/story-everyday-adobe-cc-x01/review/local-preview/`。另有相同檔案的本機交付副本：`/workspace/brand-story-preview/adobe-x01/`。

| 檔案 | 實測 |
| --- | --- |
| `preview.mp4` | 148,158,994 bytes；SHA-256 `66de600b1cd48a635f1543a1088a7e6dc45713fb4debe2c8eb1730d6aef08d3e`。交付副本雜湊相同。 |
| `preview.zh-TW.srt` | 10,033 bytes；SHA-256 `6df0e2eb233b3244d8202d9f9c18a4da009b7c240fd45f334240e1a2c2635368`。交付副本雜湊相同。 |
| `preview.zh-TW.vtt` | 9,762 bytes；SHA-256 `323ecc75a1939432f9aa89bba8dcb621b81fbcd0fbfb7c2111be007569d8075d`。交付副本雜湊相同。 |

`ffprobe -count_packets -count_frames` 讀得 H.264 High、1920×1080、30/1 fps、yuv420p，色彩空間、primaries、transfer 均為 BT.709。視訊 **18,856 影格與 18,856 封包，628.533333 秒**，正好等於正文 18,076 影格加 5 秒片頭 150 影格及 21 秒片尾 630 影格。音訊為 AAC-LC、48 kHz、立體聲，音軌 628.600000 秒；比影像長 0.066667 秒，在此專案容許的 AAC 尾端 padding 範圍內。`ffmpeg -v error -xerror` 對整支 MP4 的影像與音訊完整解碼，exit 0、沒有解碼錯誤。

`ebur128=peak=true` 實測整體響度 **−14.0 LUFS**、LRA 3.9 LU、真峰值 **−0.9 dBFS**；符合專案 `checkLoudness` 的 −14±1 LUFS 與真峰值不高於 −0.5 dBFS。`silencedetect=noise=-50dB:d=0.5` 找到五段低於門檻的區間：52.567–53.134、176.290–176.835、345.091–346.169、513.221–514.305、607.177–608.168 秒。第一和最後一段靠近概念片頭／片尾淡入邊界，其餘落在旁白句間停頓附近；此項只量測振幅，不判斷聽感是否自然。

## 字幕與抽查

以當前 `video.json` 及 `timeline.json` 重建繁中字幕並套用 150 影格片頭位移，得到 **96 則 cue、缺句 0、`checkCues` 警告 0**。實際 SRT 與 VTT 均與 `toSrt`／`toVtt` 的重建輸出逐位元組相同。片頭 52.567–57.567 秒沒有字幕；下一則從 57.567 秒開始。最後一則在 606.123 秒結束，沒有伸進 607.533 秒開始的片尾。

從實際 MP4 抽取並檢視 1、53、55、58、119、391、515、549、608、613、623、628 秒畫面，涵蓋開場、概念片頭、正文返回、資料卡／插畫與概念片尾。這 12 張抽樣沒有顯示黑畫面或明顯遺漏的畫面；55 秒可見「本機概念試看片 非正式片頭」，613 秒後可見兩個影片框、訂閱版位及須在 YouTube Studio 設定的提示。抽樣不能證明每一影格或所有文字都正確。檢視用接觸表保存在非版本控管的 `/tmp/adobe-x01-qa-stills/contact.png`。

在四句既有轉錄旗標處，從成片音軌按時間軸位置擷取單聲道 PCM，與各句原始 WAV 做同起點波形相關比對：`x010210` 118.567 秒，r=0.9983；`x010503` 390.367 秒，r=0.9991；`x010521` 514.267 秒，r=1.0000；`x010605` 548.700 秒，r=0.9995。四句的最高相關均在 0 毫秒位移，證明這些音檔進入成片的預定時間位置；**波形吻合不能證明旁白念字正確**。

## 尚待正式審核

[`audio-check.md`](audio-check.md) 的四句近義轉錄旗標仍在，這台雲端沒有可用的獨立離線 ASR 模型，也未進行人耳聽核。正式交付前須逐句聽取 `x010210`、`x010503`、`x010521`、`x010605`，必要時重錄並重跑音訊、字幕與成片 QA。本片頭／片尾只供本機概念試看；正式頻道動畫不在此環境。片尾的框與訂閱版位只是畫面，YouTube 影片卡與訂閱鈕需上傳後在 Studio 設定並實際點擊驗證。

複查主要指令：

```bash
P=/workspace/.brand-video-workdir/story-everyday-adobe-cc-x01/review/local-preview/preview.mp4
ffprobe -v error -count_packets -count_frames -show_entries format=duration,size:stream=codec_type,codec_name,profile,width,height,r_frame_rate,pix_fmt,color_space,color_primaries,color_transfer,nb_read_packets,nb_read_frames,sample_rate,channels,duration -of json "$P"
ffmpeg -v error -xerror -i "$P" -map 0:v:0 -map 0:a:0 -f null -
ffmpeg -hide_banner -nostats -i "$P" -map 0:a:0 -af ebur128=peak=true -f null -
ffmpeg -hide_banner -nostats -i "$P" -map 0:a:0 -af silencedetect=noise=-50dB:d=0.5 -f null -
```
