# 撰稿工具

撰稿代理用來產生每集 `video.json`、分鏡表與跑檢查的腳本，原本在 session 的暫存區，2026-10-31 搬進 repo，免得改稿時要重寫。
路徑已改成相對於腳本所在的資料夾；從 repo 根目錄執行。

- `e043-e046/`：第 43–46 集。`e04N.py`（配 `ztlib.py`）產生 `docs/videos/zhong-tian-qu-qi-e04N/video.json`，`sb.mjs` 產生分鏡表，
  `chk.sh` 跑 lint、drama_craft_check、shot_reading 與 ref2manifest。改稿後重跑這些，三個檔才會一致。
- `e051-e055/`：第 51–55 集。在這個資料夾裡 `python3 build.py e05N` 產生 video.json 與分鏡，再跑 `node tools/video/cli.mjs script --slug zhong-tian-qu-qi-e05N`。
