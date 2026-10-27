# Formal ZH：原始容器兩欄位還原 PREP

只有 PREP，沒有抽音、FFmpeg／probe、音檢、網路或付費執行。原先抽出 M4A `43e936eb…`、manifest `db8c735f…`、TXT `fe8e3edf…`、原 helper／永久 marker／logs 均保持。

獨立查核發現：來源與原抽出檔的 ffprobe presentation packet、AAC payload hash及完整PCM相同；但 remux把原始 raw stts最後 sample_delta64正規化成65，raw mdhd總28153503成28153504，相差1/48000秒。此新階段不重新remux／編碼，而在同長新副本還原兩個32bit欄位。兩個欄位共8B範圍，實際只改2B：315 A0→9F、586 41→40。新檔預測SHA由獨立parser事先計算為`f6edafd3ab0dc173a86ba4c8a9828ad2973b2ae2923f846f8e1d5791119ba42f`；Root執行仍會獨立由hdlr=soun路徑推導offset／原值／來源值，驗證新副本所有其他byte及atom大小／offset完全等於舊檔。

新檔在既有D內，舊3檔不動：
- `program.original-timing.zh-TW.m4a`
- `program-audio-original-timing.txt`
- `program-audio-original-timing-manifest.json`

raw stts payload整份、mdhd timescale/duration、elst／stsz payload須精確等於來源。原mdhd語言und與M4A zho不同，保留既有zho，不宣稱整份mdhd payload相等。只修改兩個固定寬度整數，mdat／位置與長度不變，沒有CRC或別的偏移要更新。

Root先審 exact `restore.mjs`／`plan.json`／獨立peer review，正常原票claim及實際進程檢查後，建立本目錄 `root-restore-release.json`：

```
kind: ROOT_Formal_ZH_original_timing_restore_dispatch_v1
owner: /root
helper: {file, bytes, sha256}
plan: {file, bytes, sha256}
peer_review: {file, bytes, sha256}
task_claim: {file, bytes, sha256}
issued_at_utc: <真實UTC>
expires_at_utc: <最多30分鐘後>
max_metadata_restorations: 1
max_remux_calls: 0
no_TTS_ASR_paid_network: true
```

Root唯一執行命令：

```
node --use-env-proxy /workspace/work/ai-tech-next/continuation-20261027t1918/formal-zh-audio-restoration/restore.mjs execute
```

同一Node PID持有W／C正常nativelease，拒絕任何現存lease及takeover；查W、C、Cparent、全域影片、D及本目錄STOP。每個長程序監看STOP／lease／期限，失敗私有收據照存。新`restore.once.json`／`run-once`及三個新檔必須不存在；實際開始後永久消耗，不刪除或重播。

只對新檔執行一次ffprobe、一次完整f32le PCM解碼、一次ebur128量測。來源packet與來源PCM結果沿用原Root真執行保存且全SHA綁定的收據，不重跑來源FFmpeg。新packet逐項payload hash／時間／flags／side_data／codec extradata須同來源；PCM完整bytes／SHA／sampleframes須同來源，解碼exit0／error stderr空。量測LUFS／LRA／TP如實記，不新增或降低門檻。全E248／W1865／C1872及held4和舊3輸出完整SHA前後一致；不改canonical/state／語言旗標、QA、ASR或未知計費。

新TXT如實交代兩整數還原與原抽出檔保留、來源與輸出完整SHA／bytes、raw／packet／PCM真查核、容器時長及量測。105句來源只繼承原已查核證據；沒有新ASR／人工重聽、整片QA、外語完成或伺服器核准。原QA10/11 false與JA14旗標保持。
