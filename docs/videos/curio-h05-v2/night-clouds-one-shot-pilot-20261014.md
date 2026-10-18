# H05 v2｜`night-clouds` 單張氣氛圖小樣

日期：2026-10-14。此輪站主只授權此鏡一次 MiniMax 生圖與一次正常 judge；未重抽、未擴批、未送 storyboard 審核。結果是**單鏡候選圖**，不是連續片段或正式成片驗收。

## 版本與付費前關卡

`night-clouds`（口播 `h5v032`）的提示由含「樹林遠景」的描述收窄為正向可見構圖：畫面只取夜空、層雲及中央留白，不建立地貌、飛機、人物或落點。`data.camera=pan right`、場景順序、line ID、口播與時窗未改。`video.json` SHA-256 `05abe8cf0cd4680a12e911feb118e6d3dec88c20dbba0f8b8e7ac65b51d0d870`；`narrative_hash=25c823ca2e556693`、`speech_hash=0b7b642f114d257f`、`pictures_hash=f8d3de2a3f752907`、`look_hash=38b9efa0cb47553f`。`lint --json` 零錯誤、零警告。

站主新核准已由 `review-pull --gate audio` 讀回：`timeline.json` SHA-256 `e1cceb2c0cd511f5c67b4e4c34de201036745ed20cf6e48ad7f85f9a000666e9`，正式 `approvals.json` SHA-256 `4c9eeb731bf165350a5b4b2f4f2e5b916ad5702a12338ea286be7803f5d29a0a`，其中音訊核准列綁同一時間軸（2026-10-14T04:07:53.585Z）。這次只改圖像提示，時間軸及 108 句 WAV 未動。

`keyframes --slug curio-h05-v2 --shot night-clouds --takes 1 --dry-run` 顯示 MiniMax `image-01` ready、1K、提示 267／872 字、無 style plate、預估單張加 judge 約 US$0.01（輸出四捨五入）；US$80 單片上限內。付費前精確帳本是 13 圖／13 judge、US$0.1755、保留額與 reservation 均為 0；本片、上層 `videos` 與 `mokaair-work` 的 `STOP` 不存在，本片 `LEASE` 不存在。當時 manifest 無 `night-clouds`。

付費前十個檔案的逐檔 SHA 核對快照、108 句 WAV 雜湊表、dry-run 與 preflight 在外部 `_receipts/night-clouds-pilot-20261014T041216Z/`。`snapshot.json` SHA-256 `febfcd2352783b6a0bfe147502f05e9971d5cbe8e427683a879bfca407c7e932`、`preflight.json` SHA-256 `8ca148ee2f8633334f0482cea849f3596147d0a88fba4b3d908ee4446dc99e07`。更早的 `_receipts/night-clouds-before-20261014T041111Z/` 是提示修訂前的中止快照，**沒有送付費請求**，並保留 `ABORTED-before-paid.txt` 說明。

## 唯一生圖與判圖結果

正式指令為 `node tools/video/cli.mjs keyframes --slug curio-h05-v2 --shot night-clouds --takes 1`，只執行一次，exit 0；原始 log SHA-256 `03d944442b02c79491d15e318d8bcb4173c13c9dc5d7d68cd1285724d21b89bd`。MiniMax image 請求鍵 `884e088a348969f9`、job ID `4556826d-edc0-46c4-bc34-5444506ab294`。`keyframes/night-clouds-1.jpg` 為 1280×720、SHA-256 `2bd4caece1c35b7c410f46762c23090803a30cb8a2c961fbd9893664885fc586`；原圖和 manifest 選圖是**同一檔**，無 trim 或第二 take。

Judge 原始結果是 **10/10、PASS**，各 rubric 分均 10、`problems=[]`；這只代表模型判圖。帳本核對為恰好 **1 次 image + 1 次 judge**，分別 US$0.0035 與 US$0.0100，合計新增 **US$0.0135**；累計 14 圖／14 judge、US$0.1890、無 reservation。後置 `manifest.json` SHA-256 `5815315788579351be33919c1d5ee0a4b5ed0e25538c5be877a28e5b40fd6e89`，`ledger.json` SHA-256 `27d3a7744faf39a10633fa11fefd84b22e936768a2c3c23b4af275a7ba87f0bc`。後置帳本、manifest、raw judge、原圖、選圖、contact sheet、cache/job 與人工覆核 JSON 已存同一外部收據；`postflight.json` SHA-256 `90ceb895829a550e87e6001509f2bdf87ce91192bed2046b4dbcaf492b10031d`。

此次新的 pictures hash 使舊 manifest 的三張已退件圖記錄不再綁現稿；新 manifest 只含 `night-clouds`。舊 `open-threat`、`open-tail`、`open-boy` 原圖仍在 `keyframes/`，前置 manifest 與費用帳本快照仍留存，並未手動認列為可用畫面。

正式 `status` 讀回 **narration approved**、storytelling panel passed，但 58 個現行 shot 中只登記本張，另外 57 鏡缺圖；frames、影片、字幕、final 等後續關卡也未完成。單鏡 judge PASS 不代表影片 ready。

## 人工實看與銜接限制

代理與主製作代理都打開原圖覆核：畫面只有星空與層雲，無可辨地貌、人物、飛機、落點或假字。深藍、青與淡黃的大色塊可作編輯式氣氛插畫；**明亮黃色雲緣與星空較裝飾化**，需放在實際前後鏡中比較風格。依 `claims.md` c07、c14，此圖只可表達「夜間、落點未知」的抽象氣氛，不能當作當夜實際天氣、跳離位置或落點的紀錄影像。

正式時間軸三個相鄰場景依序是 `tail-stairs-ground` 原生步驟卡 186 幀／6.20 秒、`night-clouds` 190 幀／6.33 秒、`forest-unknown` 165 幀／5.50 秒。前卡可讀成從機尾離開、接著詢問落點；後鏡仍無現稿對應可用圖，夜空轉日間森林的正常速度銜接尚無連續預覽證據。人工結論：**接受這一張作單鏡氣氛候選；暫不標為正片可用，也不推 storyboard**。後續需與前後鏡完成連續畫面預覽及來源／風格驗收。
