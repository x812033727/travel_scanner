# S24 R4 關卡對帳與三景試畫上限｜2026-10-20

## 企劃與音訊版本

[`brief.md`](brief.md) 現為 SHA-256 `b3848b09121acf3a73baf37291ca0af7ce430726f9de3009804ba27f6b9e35b6`，將先前 R3／七旗標明確標為歷史版次，列出兩個大綱：A 案沿金冠走完整次檢查，B 案先查文獻。現行劇本採推薦 A 案。工具讀到兩選項，Jev 挑 A（1.00、立場 0.90）；`review-push outline` 精確此 brief SHA 已送站台，`review-pull` 回覆 **waiting for the owner**。依站主一直採推薦方案的委託，本機另記 A 案委派選擇；這不是站主親自讀企劃或網站已核准。

R4 `script.md` SHA-256 `2ab08047be6dbc800ef54f02b6e9321518324f9ce8e0aaea0265430242c724af`，`video.json` SHA-256 `59624d323f19dc99bb04de6ded3e2c118b00dd11c7bf0727cfc37fae710302d7`；劇本 13／13 盲讀及七句來源抽核見 [verify-6.md](verify-6.md)。`narration.wav` SHA-256 `20bd8433863ca144c6b30107a135c076c015f96bfa197dd824cb8ca2878598e7`；`timeline.json` SHA-256 `674a6db7000513d76c937050bff2dd0e28dedea374daea4aa9975213c4dbc390`。`review/check.json` SHA-256 `eb7448601a1f2d35e44dd6d1cf4b3d1dba3e42736ad0e594a4559f24d05814ae`：102／102、88 逐字、14 同音／語助、**0 未解旗標**；正文實測 8:25.73，`lint` 0 errors／0 warnings。

站台曾於 04:16 核准**同一現行**時間線 SHA `674a6db7…`，但最新 08:37 的站台音訊卡綁了另一時間線 `0edf9cf87a67a2fbbc6ecd86d2ffd51fe16e9fa6f722620fa6d53eba4958f89e`（9:17、102 句、2 flags）。因此此輪 `review-pull audio` 說「approved a version that has since changed」；本地 `status` 顯示 `[x]` 不能被拿來宣稱最新站台卡已核准現稿。`review-push audio` 已重新送現稿；工具顯示 `approved`，但隨後 pull 仍指出上述最新卡不符，沒有假定已解開站台排序。依現稿逐句零旗標與既有委託，本機另記**繼續有限製作**的音訊決定；站主尚未親自試聽本版。站台／本地差異的唯讀原始對帳見 `/tmp/s24-r4-audio-art-readonly-preflight.md`。

## 一次設定的圖樂硬上限與試畫條件

整集 99 個插圖鏡頭；`keyframes --takes 3 --dry-run` 首輪約 US$1.34、三輪圖片加評審算式為 `99 × 3 × US$0.0135 = US$4.0095`。已產生配樂 US$0.08，帳本截至開畫前為 **US$0.08、圖片 0、評審 0、未結預留 0**。依站主持續採推薦方案的授權，本輪一次設定**整集圖片加音樂硬上限 US$4.35**；理論三輪後餘額約 US$0.2605 僅留確有史料／畫質缺陷的定點修補。工具的 US$200 單片服務上限不是此集製作上限。每次付款前核帳、核共用 60 分鐘速率，累計加預估不得超過 US$4.35。

先只對 `crown-005` 浴盆、`crown-047` 定量補水、`crown-r2-021` 皇冠全浸，各做**一次正常 MiniMax image-01 圖＋評審**。三景定點 dry-run 報約 US$0.04（算式 US$0.0405）；它們與維特魯威固定原文 E8027–8033、E8040–8043、E8049–8053 及旁白逐句相合，原提示詞、各自年代／水線驗收標準見上述 `/tmp` 收據。畫後立即在專案工作目錄設 `STOP`，逐張原尺寸檢查並交另一位讀者覆看；**少於兩張真實可留圖，就不開 99 張全量批次**。不得把 chibi 畫風本身當錯，亦不得接受現代器具、東亞場景、假文字、錯誤倒水方向或半浸皇冠。本站大綱仍 pending；任何後續站台審核均如實記載。
