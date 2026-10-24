# S63 R9｜s63028 補充離線 ASR 的獨立稽核

2026-10-22。稽核者 `/root/policy_duration_incremental_review` 未撰寫補充 ASR adapter 或操作其首次辨識。本次獨立讀碼、重算音檔／時間軸雜湊、核對官方模型釋出資料，並只對同一個 WAV 重跑一次本機 CPU 辨識。

**判定：補充機器證據可用。** 同一 R9 版本的 127 句現在均有跨辨識器的機器證據：Gemini 主流程 126 句加 SenseVoice 補上 `s63028` 一句。這不能寫成「Gemini 127／127」或「主流程全過」；主流程仍是 **126／127、s63028 未轉寫／PROHIBITED_CONTENT**。本票不是人工聽音或站主親聽。

## 精確輸入與媒體綁定

| 檔案 | SHA-256 |
| --- | --- |
| R9 `video.json` | `788b20d22f3b62468c81af6a6a0f4b85669ba205809a858626c55e23b6a969f1` |
| `audio/s63028.wav` | `6f50f9beb0778d95a42a5d564097b8075f878ad27480c36199cfdac44196b56c` |
| 完整 `narration.wav` | `16cc46865808f15c7dd0a86e3353824ec82a399d09745956fea648b5b213375f` |
| `timeline.json` | `5df7d49ffb38fdbf301f87203584bf8627530dcd90d91c25c074a2ad58b4fc07` |
| 主流程 `review/check.json` | `850485f16b050a59fb7e401812df997fd2be6b53ede00d7ccc6e720951c62658` |
| 主流程 `review/check-flags.json` | `7a91cf11a9dfca288b5cf182622fa91e63843f31e7cc5536f6da4d3028ca896b` |

獨立以 Python wave 讀取：句 WAV 為單聲道、48,000 Hz、16-bit PCM，共 **290,400 samples（6.05 秒）**。時間軸 `s63028` 起始 frame **5709**、結束 **5921**，其 `audio_samples` 與 `audio_sha256` 精確符合句 WAV。由完整旁白在 `5709×48000/30` sample 起讀同長 PCM，與句 WAV 的 PCM **逐位元組相等**；不是拿別次重錄或類似句替代。完整旁白 SHA 也符合 timeline 的 `audio_evidence.narration_sha256`。另核對 127 個句 WAV 的 SHA 全數等於時間軸，126 個主流程 check clip hash 亦全數等於當前 WAV SHA 的前 16 碼；所有主流程 intended 均與現行劇本相符。

## Adapter 與模型來源

我完整讀取保存的 `review/r9-supplemental-asr-adapter.py.txt` 與實跑 `/tmp/curio_sensevoice_second_opinion.py`；兩者位元組 SHA 都是 **`37bf6791bd5fd916e50c1138c619a0ffe22bcbe0c8348daaf58e475703a5ed1f`**。程式只解析 argv 的 locale 與 WAV 路徑，把 `zh-TW` 映成 `zh`，以 ffmpeg 轉單聲道 16 kHz float PCM，再交 `OfflineRecognizer.from_sense_voice`。它不讀 script、claims、意圖句、詞彙提示檔或任何 hints 環境變數，也沒有把預期文字寫成輸出或模型輸入。使用 `use_itn=True` 是模型的逆文字正規化；本句未含數字，不影響本次詞語對照。

- 本機 runtime：Python **3.12.14**、`sherpa-onnx` **1.13.8**、`sherpa-onnx-core` **1.13.8**、NumPy **2.5.4**，套件 metadata 的 installer 為 uv，符合保留的安裝 log；ffmpeg **7.1.5**。`from_sense_voice` 的預設 provider 經 signature 檢查為 **cpu**；adapter 設 2 threads，未呼叫外部推論端點。
- 模型：SenseVoiceSmall int8 `2024-07-17`；本機 `model.int8.onnx` SHA **`c71f0ce00bec95b07744e116345e33d8cbbe08cef896382cf907bf4b51a2cd51`**，`tokens.txt` SHA **`f449eb28dc567533d7fa59be34e2abca8784f771850c78a47fb731a31429a1dc`**。模型 README 指向 FunAudioLLM/SenseVoice。
- 官方釋出：獨立以 GitHub API 讀 `k2-fsa/sherpa-onnx` 的 `asr-models` release。資產 `sherpa-onnx-sense-voice-zh-en-ja-ko-yue-int8-2024-07-17.tar.bz2`，大小 **163,002,883 bytes**，官方 API 的 digest 為 **`sha256:7d1efa2138a65b0b488df37f8b89e3d91a60676e416f515b952358d83dfd347e`**，與補充 JSON 及保留的 `archive-sha256.txt` 相同。來源網址為 `https://github.com/k2-fsa/sherpa-onnx/releases/download/asr-models/sherpa-onnx-sense-voice-zh-en-ja-ko-yue-int8-2024-07-17.tar.bz2`。壓縮包本體已未保留，本票沒有重新下載或重新解壓它；官方 digest 可獨立核實下載收據，現有解出模型的 SHA 則與補充紀錄相符，兩者證據層次不混稱。

## 獨立重跑與語義比對

只執行：

```text
/tmp/curio-sensevoice-venv/bin/python /tmp/curio_sensevoice_second_opinion.py zh-TW /workspace/.video-work/curio-s63/audio/s63028.wav
```

本次 exit 0，stderr 空；原始 stdout 與首次保留輸出**逐位元組相同**，SHA **`fa0173600a4035c549e417fddb6801d623caa3c3cd781d3c4eb9c719ae70d62d`**：

```text
s63028.wav 南希替人洗衣，布朗留下部分工钱，两人靠这些照顾孩子。
```

當前原句：`南希替人洗衣，布朗留下部分工錢；兩人靠這些照顧孩子。`。只將 `钱／两／这／顾` 對應繁體並忽略標點空白後，兩句逐字相等，沒有靠同音替換、補寫缺字或語義寬放通過；主詞、洗衣、部分工錢與共同照顧孩子均完整保留。

## 跨辨識器覆蓋的正確說法

主流程 check 保留 **126 個條目**，`s63028` 仍缺席；其中 **123** 個直接文字／同音規則 match，另 **3** 個為 Jev 分數 **0.60、0.58、0.64**（高於原工具 0.5 門檻）的既有接受結果，分別為姓名同音字或「一千二百／一千兩百」的轉寫差異。原 `check-flags.json` 的 flags 為空，不代表 provider 未轉寫句自動通過；`/tmp/s63-r9-check-audio.log` 仍保留 `s63028` 的 PROHIBITED_CONTENT 失敗。

因此可記錄「**126 句主流程接受＋1 句獨立離線 ASR 精確轉寫，跨辨識器補充機器證據覆蓋 127／127**」。不能把它宣稱為官方 CLI 原關卡已自動變綠、Gemini 已辨識第 127 句、或站主／本稽核者聽過聲音。後續製作關卡是否接受這份補充證據由協調者依既有授權透明記錄；本票未改任何 Gemini cache、flags、approval 或 production 檔案，也未操作 Git。
