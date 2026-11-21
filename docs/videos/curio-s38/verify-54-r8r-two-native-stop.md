# S38 R8r｜PF009／PF013 原生圖驗收：兩張均 REJECT，STOP

2026-10-22 UTC。依 [R8r 獨立書面 PASS](verify-53-r8r-two-prompt-independent.md)，只對 `pf009,pf013` 各試一張。**兩張未裁切 1280×720 原生 JPEG 均人工 REJECT；不得進成片或把本輪視作第一章通過。** `pf015`–`pf022` 及其他未畫鏡頭沒有生成，沒有修改創作檔、commit 或 push。

## 原圖逐張判定

| 景 | 未裁切原圖 SHA-256；入選裁邊圖 SHA-256 | 人工原圖結果 |
| --- | --- | --- |
| `pf009` | `dda311479b54b18b96a3ca2a736138bb554f05dafd081588bef4781ca1839a09`；`e50614ef05b68c34d7c163be184c38078e62947a92a1f5e4dd73027075a58358` | **REJECT。** 原圖頂底仍有明顯黑色寬帶。臉與毯子的近景遮住睡袍和雙手，無法看出「回床並拉起毯子」的主動作；裁邊圖雖去黑帶，仍只見臉在毯後。漫畫造型較 R8q 接近系列，但不能彌補黑帶與動作缺失。機器 9/10 FAIL，`frame`、`details` 指向同兩問題。 |
| `pf013` | `60c46af4ba47bf8fd6b3beb110018620a385d8033926c01d0a2ef940ffcfda0d`；`6e99abdde6db8e458d94c5048216cbd80f6ea29bcbad2ff9839bcfee04720ae2` | **REJECT。** R8q 那座明顯的 1894 **Tower Bridge 雙塔／吊索已不在**，但人物正面對觀眾微笑，沒有按旁白望向橋端火；河岸、房屋與天色採半寫實柔焦，與人物的平面漫畫和既收場景畫風割裂。遠處有單拱形橋影，不能據此確認它是 1666 年舊 London Bridge；不拿它作史實證物。裁邊版沒有修正視線與背景。機器 9/10 FAIL，`style`、`details` 指向同問題。 |

前輪 PF009 原生圖 SHA `e87593dc16e5ff87e91f159fe3b3c6e622fa4cb67a87b205e794bb6c30668ed0` 與 PF013 SHA `5f81bfa4247ac033f049178cb4daafcc47fc00a1d91e08e45a1d3252d7c212b2` 已保存在私有 `review/r8r-two-pre/`／`review/r8q-six-post/`，不能把它們的機器結果誤認為本輪。新舊四張原圖均直接看過；本輪裁邊圖也直接看過。

## 有界執行與不變性

開畫前私有備份在 `/workspace/.video-work/curio-s38/review/r8r-two-pre/`，含 STOP、ledger、manifest、兩張舊原圖及 PF009 舊裁圖。以 EXIT trap 暫解 STOP，只執行 `NODE_USE_ENV_PROXY=1 VIDEO_WORKDIR=/workspace/.video-work PLAYWRIGHT_BROWSERS_PATH=/workspace/.video-work/playwright-system node tools/video/cli.mjs keyframes --slug curio-s38 --shot pf009,pf013 --takes 1`；沒有 `--force`、seed offset 或更大 shot 清單。私有執行日誌／退出碼保存在 `review/r8r-two-native.log`／`review/r8r-two-native.exit`，SHA-256 分別 `da5e457eef747e4bb66f72f65cc2dd51e7f965ec6f04a9ee675e722260a43953`／`4355a46b19d348dc2f57c046f8ef63d4538ebb936000f3c9ee954a27460dd865`；退出碼 `1` 是兩張內容關卡 `needs_review`，並非漏跑。完整後圖單、ledger、原圖、裁圖、STOP 與日誌另存於 `review/r8r-two-post/`。

私有 ledger 由 **US$0.5425／35 image／34 judge／1 music** 增至 **US$0.5695／37 image／36 judge／1 music**，恰有 PF009、PF013 各一張 US$0.0035 image 加 US$0.01 judge，合計 US$0.0270；舊 PF003 US$0.0035 reservation 未動。仍低於整集硬上限 **US$4.58**。新 ledger SHA-256 `b6823292a9fbacaf4724d057cd71b86b16fb600cc5801e9c85734c1a82454144`；新 manifest SHA-256 `45e4c9ff1b3f0245bdc52ea80482b1f9e44ccc0a67964794722c9e40a9700d8a`。兩個新 shot 各恰有一個 take，`judge.passed=false`、`needs_review=true`。已收 PF001–005、PF008、PF010–012、PF014 的十個 manifest entries 均與批前逐項相同，十張現行所選圖片各自 SHA 仍對應原 entry。STOP 執行後已恢復在位。

`video.json` SHA-256 仍為 R8r `f02fdd2bd769e746b2e76206152492593f66cec1ea48e40a07cd7bf236aaf015`；`script.md`、`claims.md` 仍為 `e59ec137e3de3871e3b0e5063d8f6504d3eb2adb5fe22265eb3faa3d613d5951`、`f9de8d2771b62cc327f4e599f002af8f3278cfb0f39dbed201e7fdc857201d42`。R8r 這次的**書面來源／差分 PASS** 沒有因圖片失敗而撤回；原生圖則明確 HOLD。後續若要修 PF009 的畫面滿框與可見拉毯動作、PF013 的背向觀火與平面背景，需另凍結候選並獨立核差分，再單景有界試畫；本輪不追加付費 take。
