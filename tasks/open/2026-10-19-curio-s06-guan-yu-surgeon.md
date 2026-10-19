---
id: 2026-10-19-curio-s06-guan-yu-surgeon
title: Curio S06 Guan Yu's unnamed surgeon and the later Hua Tuo scene
status: in-progress
priority: P2
area: docs
owner: codex-gpt6-s06
claimed_at: 2026-10-19T20:22:22Z
created_at: 2026-10-19T20:22:22Z
completed_at:
branch: codex/curio-s34-endurance-20261019
depends_on: []
scope:
  - docs/videos/curio-s06
---

# Curio S06 關羽的無名醫生與後來的華佗場景

## Why

站主要求持續製作 S 軸歷史影片。《三國志》確有關羽刮骨治傷記載，但並未寫醫生姓名與手術年份；《三國演義》第七十五回把華佗、馬良對弈與樊城戰事寫進同一幕。題庫原稿把「醫生不是華佗」寫成確定句，製作前須拆開史書可證與小說編排。

## Definition of done

- [x] 用固定版本原文建立史書、小說、華佗與曹沖年表的核對底稿。
- [ ] 完成 8–10 分鐘史料可核的企劃、逐句劇本、畫面與獨立來源覆核及盲讀。首兩輪 10/13、11/13，第三輪 13/13；語音清晰度修復後的新確切稿待重讀。
- [ ] 媒體製作、音訊與成片品管；第三輪稿 76 句旁白實測正文超過 8 分鐘，兩輪語音檢查 14→8 句旗標，新稿待盲讀／重錄；圖片仍未開畫。

## Steps

- [x] 確認沒有其他 S06 認領與同名影片，認領窄 scope。
- [x] 記錄《三國志》關羽左臂、無名醫生、未記手術年份；《三國演義》樊城右臂、華佗、馬良對弈。
- [x] 核對《三國志》華佗死於曹沖之前，曹沖卒於建安十三年；只用這條年表判定**小說放在樊城之役的華佗場景**年代不合，不推定史書無年份的治療者身分。
- [x] 依站主的持續製作委託採用 A 案，完成 `brief.md`；已送 outline 審核並以代理記錄的委託核准，明示站主未逐篇審讀。`brief.md` 核准雜湊前綴 `0a984e084485`。
- [x] 撰寫 S06 逐句劇本、分鏡與來源表：76 句／75 靜圖，`lint` 0 錯 0 警告；前兩輪盲讀與修稿見 `verify-4.md`、`verify-5.md`。
- [x] 第三輪確切劇本由新讀者獨立判 13/13、固定來源與分鏡通過，見 `verify-6.md`；合成後正文首次實測 8:30.83，見 `verify-7.md`。
- [ ] 八句音訊清晰度修復的新確切稿再送獨立來源覆核與全新 13 題盲讀；通過後重錄八句並做逐句音訊檢查。

## How to verify

閱讀 `docs/videos/curio-s06/research.md` 的固定版連結與原文定位；後續用 `node tools/video/cli.mjs lint --slug curio-s06`、獨立來源覆核及全新盲讀。

## Notes

本票僅改 `docs/videos/curio-s06`；不改 `topics.json` 或其他集。史書內容為傳世文字，不把晚出小說細節拍成歷史目擊。插圖避免傷口與血畫面。S06 旁白已合成，但尚未購買插圖或配樂。

2026-10-19 首稿 `script.md` SHA-256 `285ee983913b1862f34a49504dc9b99c0f9f0875251a11e2405147283301a793`，narrative hash `9d09a85fc0d30fa8`；作者的敘事收束與史料增量見 `verify-2.md`、`verify-3.md`。第一輪受審稿 SHA-256 `1aff6121121d09dfdb0e5ab29db0274110fd31d341c43cf10e87e36f28c3b5cb`、narrative hash `8b39e545c5e77d97`。語音與插圖仍待獨立審讀通過及共享服務容量安排。

第一輪讀者已封存上述確切版本的 10/13 原始判定，固定來源重開也指出 gs070 將小說場景與史書年份混作同一來源。第二輪受審稿依此修訂為 SHA-256 `8d86614a89c5100ba95f95d42d7b24d54ee0a376c2b9cb277e54fa748770a74e`、narrative hash `54797c250786bf4c`，76 靜圖；不沿用第一輪收據。尚未啟動付費媒體。

第二輪來源隔離盲讀在 `8d86614a…` 判 11/13，史料與主張通過，`gs006` 的目錄語、`gs060` 重述被標記；同時提醒醫生先向關平報名，之後才進棋帳。依此窄修後的**目前**確切稿 SHA-256 `cafb9255d06872ee2a083becf16cbe4046dcc698f1d18c36e7023294d15badc1`、narrative hash `d9e323dfca9ec76d`，75 張靜圖。第三輪新讀者尚未審核；語音實測與付費插圖均未開始。

上段為送第三輪時的紀錄。第三輪 `cafb9255…` 通過獨立 13/13、原件／畫面覆核；TTS 正文實測 510.83 秒，兩輪逐句檢查仍有 8 個反覆同音標記。現行八句修復稿 SHA-256 `970d27ef3efdc8e99cd1bc2f50859bf407b753ac2323df729eda8be93274825f`、narrative hash `aae8c6d4f7884e25`，76 句／75 靜圖，lint 0/0，詳見 `verify-6.md`、`verify-7.md`。新稿盲讀與語音審核未過前不購插圖；插圖支出 US$0.00。
