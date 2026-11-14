# S38 R8i｜`pf006` 第二次修詞試畫停點

2026-10-21 00:33 UTC。**STOP：`pf006` 最後一次限額試圖仍 REJECT，不再購買同一路線第三張。** R8h 已通過的 `pf004/005` 仍是獨立 KEEP；整集插圖與成片仍 HOLD。

## 固定版本與唯一付費呼叫

本次 `video.json` SHA-256 **`de27c08f77dd91e66703fcf5c875ee1ea787d34246b93bc6237af8c7fcd03861`**、`visualHash` **`79b6a9303fdfaeba`**；[R8i 獨立紙上覆核](verify-22-r8i-independent.md)先通過，`--shot pf006 --takes 1 --dry-run` 顯示 MiniMax `image-01` 就緒。唯一正式命令為 `NODE_USE_ENV_PROXY=1 NODE_NO_WARNINGS=1 VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs keyframes --slug curio-s38 --shot pf006 --takes 1`，只暫停私有 `STOP` 執行這一景，外層 `EXIT` trap 隨即恢復；結束後實測 `STOP` 在。工具回 `4 of 5 drawn shots are unchanged and keep their verdicts`，未再購 `pf001/002/004/005`。原始私有 `/tmp/curio-s38-r8i-pf006-last-pilot.log` SHA-256 **`5a8230bd44a604f8609d8d7f85868d0718b55b0a7a286b5ea4999582c7519444`**。

原生 1280×720 `keyframes/pf006-1.jpg` SHA-256 `a0afb39992a95bce5ab0ba01cab7f4f4a116545f2c82716ad99fd2bb533e29a3`，裁去紙邊後 `pf006-1-trim.jpg` SHA-256 **`43cb8ef2b6b61e784aba3e9343b18b26c564903a54e3c8e5dab520c057800d07`**。Judge 9／10 仍 **FAIL**：整張偏 3D CGI，不是系列 2D 平面卡通；人只在畫面左邊探出頭，沒有照提示詞把上身探出窗外。我直接看裁切後原圖，還有可見黑邊與逼真的陰影／街道材質，人物和年代感與同集已通過插圖不一致，故原生 **REJECT**。分數 9 不可蓋過畫風失敗；`manifest.json` 的 `pf006.needs_review=true`。

本次 image + judge 新增 **US$0.0135**；ledger 累計 **US$0.2895**（17 image、15 judge、1 music），其中 `pf003` 舊 **US$0.0035 reserved** 仍算入，整集硬上限 US$4.58 未提高。工具仍因容器缺對應 Playwright Chromium 無 contact sheet，本判定依原生 JPEG。沒有網站音訊／分鏡卡的新核准。

## 改用系列准許的失敗景處理

`pf006` 已經歷 R8e 原生判退、R8f 修詞後 R8h 原生判退、R8i 修詞後本次原生判退，符合[系列技能](../../../.agents/skills/curio-episode/SKILL.md)所述「三張圖與兩輪改提示詞仍不過」的本機停點。下一步應提出**無新付費圖**方案：改用同章已通過圖片且不曲解女僕珍妮的旁白，或改為一張只載日期／人名的卡片，並重跑 Curio 70% 插圖比、連卡數、lint、來源／畫面獨立覆核。另有 `pf003` 未解 reservation；不得重送同一付款請求、擅清 ledger，或因本次兩張 KEEP 就解除整集 STOP。若改成卡片，須重新綁定 `video.json` 和整體分鏡，讓工具核未改景的 request key／judge stamp，並把 US$0.0035 仍計入成本上限。
