# 撰稿工具

撰稿代理用來產生每集 `video.json`、分鏡表與跑檢查的腳本，原本在 session 的暫存區，2026-10-31 搬進 repo，免得改稿時要重寫。
路徑已改成相對於腳本所在的資料夾；從 repo 根目錄執行。

- `e043-e046/`：第 43–46 集。`e04N.py`（配 `ztlib.py`）產生 `docs/videos/zhong-tian-qu-qi-e04N/video.json`，`sb.mjs` 產生分鏡表，
  `chk.sh` 跑 lint、drama_craft_check、shot_reading 與 ref2manifest。改稿後重跑這些，三個檔才會一致。
- `e051-e055/`：第 51–55 集。在這個資料夾裡 `python3 build.py e05N` 產生 video.json 與分鏡，再跑 `node tools/video/cli.mjs script --slug zhong-tian-qu-qi-e05N`。
- `e047-e050/`：第 47–50 集。`python3 build_ep.py <spec47.py…spec50.py>` 重新產生一集並重跑檢查（用法見 build_ep.py 開頭）。
- `e056-e060/`：第 56–60 集。`b5N.py` 產生鏡頭，`d5N.py` 產生 brief 與分鏡並重建整集。

2026-10-31 連戲整理：第 56–60 集秦霜的衣服改回 `cast.json` 的深棕短褂、寬皮帶、黑繩高馬尾（Ref2VA 定妝照 `assets/refs-dh/qinshuang-portrait-t1.png` 就是這套）。
細綱第 56 集寫「換上合身的黑色勁裝、高馬尾束紅繩」，但 prompt 換衣服會跟參考圖打架；改在 `e056-e060/b5N.py` 的 `QIN` 與 s09、s12，再用 `d5N.py` 重建，所以重跑不會改回去。
顏值鏡頭 s12 改用晨光逆光把馬尾與肩線勾成金邊、下巴微抬來拍。要換衣服，先畫新的定妝照、改 `cast.json`，再改這裡。
