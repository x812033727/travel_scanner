# 撰稿工具

撰稿代理用來產生每集 `video.json`、分鏡表與跑檢查的腳本，原本在 session 的暫存區，2026-10-31 搬進 repo，免得改稿時要重寫。
路徑已改成相對於腳本所在的資料夾；從 repo 根目錄執行。

- `e043-e046/`：第 43–46 集。`e04N.py`（配 `ztlib.py`）產生 `docs/videos/zhong-tian-qu-qi-e04N/video.json`，`sb.mjs` 產生分鏡表，
  `chk.sh` 跑 lint、drama_craft_check、shot_reading 與 ref2manifest。改稿後重跑這些，三個檔才會一致。
- `e051-e055/`：第 51–55 集。在這個資料夾裡 `python3 build.py e05N` 產生 video.json 與分鏡，再跑 `node tools/video/cli.mjs script --slug zhong-tian-qu-qi-e05N`。
- `e047-e050/`：第 47–50 集。`python3 build_ep.py <spec47.py…spec50.py>` 重新產生一集並重跑檢查（用法見 build_ep.py 開頭）。
- `e056-e060/`：第 56–60 集。`b5N.py` 產生鏡頭，`d5N.py` 產生 brief 與分鏡並重建整集。

2026-10-31 連戲整理：第 56–60 集秦霜穿 `cast.json` 的深棕短褂、寬皮帶、黑繩高馬尾，跟 Ref2VA 定妝照 `assets/refs-dh/qinshuang-portrait-t1.png` 與細綱（站主定案，各季的「黑紅」已改成「深棕」）一致。
衣服寫在 `e056-e060/b5N.py` 的 `QIN`，再用 `d5N.py` 重建，所以重跑不會改掉。要換衣服，先畫新的定妝照、改 `cast.json`，再改這裡。
同一輪也改了：第 56 集 s09「給我三天，打穀場見」（s12 起是回柳溪第五日）、第 58 集冷鐵「後天就到」、第 50 集 s30 玉佩先放進秦霜手心、
第 58–60 集許硯的左前臂纏白布（`spec50.py`、`b56.py`、`b58.py`、`b59.py`、`b60.py`）。第 40、41 集沒有撰稿腳本，video.json 直接改、就是權威版本。
杜鐵的拐杖改到右腋下（左腿瘸，拐在另一邊）：`cast.json`、`e044.py`、`spec48.py`、`e052.py`，第 59 集照 `cast.json` 重建。
`e051-e055/tl.mjs`（build.py 要的時間軸）原本沒搬進來，2026-10-31 用 `tools/video/core/timeline.mjs` 的 lint 估法補上，重建結果與原檔一致。
`e043-e046/sb.mjs` 要的 `h*.md`／`f*.md` 也沒搬進來，所以第 43–46 集的分鏡表目前只能手改（`e0NN.py` 仍會重建 video.json，跑完刪掉它寫出的 `zh-e0NN.json`）。
