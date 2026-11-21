# S38 R8r｜`pf009`／`pf013` 兩景提示詞定點修正，作者凍結

2026-10-22 UTC。R8q 六張 [原生驗收](verify-51-r8q-six-native-stop.md)收下 `pf010`、`pf011`、`pf012`、`pf014`，但 `pf009` 的黑寬帶／偏寫實動畫畫風及 `pf013` 的 **1894 Tower Bridge** 重大年代錯誤仍被退件。**R8r 只改 `pf009`、`pf013` 兩個 `data.prompt`；其餘四張已收提示詞、旁白、卡片、鏡頭運動、章節與系列 `look.preset=cute-mystery` 均未改。**這只是作者書面候選，尚未獨立核圖或付費重試。

## 可逆差分與日記界線

[逐字結構化差分](verify-52-r8r-two-prompt-structured-diff.json)記錄 `scenes[8].data.prompt` 和 `scenes[12].data.prompt` 的舊／新值。新 `video.json` SHA-256 **`f02fdd2bd769e746b2e76206152492593f66cec1ea48e40a07cd7bf236aaf015`**；將這兩個新字串在原位換回舊字串，可逐位元組還原 R8q SHA-256 **`087ae9c4cdbb8dea3430cd505d42624e06deca0a94b77e71c49164fbbcc2f4db`**。`claims.md`、`research.md`、`script.md` 分別仍是 `f9de8d2771b62cc327f4e599f002af8f3278cfb0f39dbed201e7fdc857201d42`、`f838518cf2c4ab23de91021ae6024d9431f907866c14301466ca0a06bb3ecdfe`、`e59ec137e3de3871e3b0e5063d8f6504d3eb2adb5fe22265eb3faa3d613d5951`，所以 claims 口播主張與劇本沒有另作視覺改寫。

- **`pf009`：** [佩皮斯 9 月 2 日日記](https://github.com/GITenberg/The-Diary-of-Samuel-Pepys---Complete_4200/blob/68fcf49f70ee793b989a6fd0464264d55beb4451/4200.txt#L65795-L65803)說他凌晨在 Jane 窗邊看完火後回床睡。新 prompt 聚焦一名成年男子在窄木床上拉起淺色毯子，保留睡袍和黎明前時間；刪去窗外紅光與過暗的 `dim soft light`，改用較平和的室內柔光，降低前張深夜光影與電影黑寬帶的誘因。毯色與室內光是畫面示意，非日記逐項記載；不在單鏡 prompt 加畫風字或改固定 `look`。若新原圖仍有 3D／黑邊，必須再退。
- **`pf013`：** 同日記 [L65803–65819](https://github.com/GITenberg/The-Diary-of-Samuel-Pepys---Complete_4200/blob/68fcf49f70ee793b989a6fd0464264d55beb4451/4200.txt#L65803-L65819)說佩皮斯登塔，看見橋端房屋起火；直到**搭船以後**才親見 Michell 家已燒。R8q 雖要求「old stone-arched London Bridge」，模型仍生成近代雙塔吊索橋。R8r 讓成年人物在塔的石平台看**遠處河邊房屋上方的火焰**，不要求橋體入鏡；橋的位置由同一句旁白交代，不把某戶燒毀提早確定。石平台與衣飾仍為年代示意，沒有把火源烘焙屋當作親見。

這兩景的原生退件圖與舊 manifest 已私有保存在 `review/r8q-six-post/`；四張同批 KEEP 並不因本次兩字串修正而轉成重新購圖。下一次執行 `keyframes` 時，全局圖單須按新 `visual_hash` 重綁，再逐格確認已收 `pf001`–`pf005`、`pf008`、`pf010`–`pf012`、`pf014` 的 request key、評審 stamp 與選圖 SHA；**不能**把舊 manifest 中 `pf009`、`pf013` 的機器分數視為 R8r 生成結果。

## 僅書面檢查

`VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s38 --json` 為 **0 errors／0 warnings**，112 句與估 10.016 分鐘未變。`keyframes --shot pf009,pf013 --takes 1 --dry-run`：MiniMax `image-01` ready，兩個 prompt 各 278／286 字，在 1069／1072 字預算內；首輪圖加評審報約 **US$0.03**。沒有發出 image 或 judge 請求。私有 ledger 維持 **US$0.5425／35 images／34 judges／1 music**，另有舊 `pf003` US$0.0035 reservation；整集硬上限 **US$4.58** 未變。`STOP` 現在存在；舊 manifest SHA-256 `ffd0069be9f1b368ffcea76f4b9a94b06eb7d8e1bcbc480c13f70ec90933c8fa` 綁 R8q，不是 R8r 分鏡合格證據。

下一步請另一位覆核者讀精確差分、日記的回床／塔上親見界線、兩個新畫面與四張已收圖的未改提示詞。獨立書面 PASS 後，才可在 EXIT 恢復 STOP 的單景範圍各試一次，直接檢查未裁切 1280×720 原圖和入選裁邊版；本頁不放行 `pf015`–`pf022` 或整集分鏡。
