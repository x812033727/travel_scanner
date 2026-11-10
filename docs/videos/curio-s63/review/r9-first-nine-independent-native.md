# S63 R9 首九景：獨立原圖與 selected 覆核

日期：2026-10-22 UTC。獨立 reviewer：policy_duration_incremental_review。依 curio-episode「內容相關可愛插畫」標準；非證據重建，不因 chibi、次要道具或額外協助者而重畫。已直接打開全部九張原圖（原始解析度），並另外打開 s63001／004／006 的 selected trim；其餘 selected 與原圖同一檔。STOP 已存在，log 已結束，未使用接觸表代替原圖。

## 結論

**KEEP 5：s63001–004、s63006。REJECT 3：s63005、s63007、s63009。s63008 保留現 take 的機器 FAIL／HOLD，不以人工覆核清除。** 因此現批不可全部放行。每景現有1 actual，最多2次剩餘；本次未生成、未改提示詞／媒體／manifest、未付費、未 git。

## 固定輸入 SHA-256

- `video.json`：`788b20d22f3b62468c81af6a6a0f4b85669ba205809a858626c55e23b6a969f1`
- `script.md`：`d6bc3ad0bfb85a1a61f6d721c0e6fcc205f0e69c0adbd82c5a6b831302641abd`
- `claims.md`：`68c5b82ce945e3b5b0dfad9e4dd673eb52052e62513c92f2a46722b37150c756`
- `research.md`：`d3ff4f97fae690af6caaab97aa0047695c7fd32649be31ef5c073ae687edda23`
- manifest：`88e75a44f29dd59c59ce3dc7cd04873e2791565bd8de8cc9a8152ab0290dcdf2`
- source Brown/Stearns 1849 固定本文：`6d80216184aaf20433e04aa8d1b6920076211304fcede4a095da3ef5bd62ada2`

對照 claims 首九列／research B03、B05、B07、B08、B09、B10；其中 B08 轉車箱內聽聞，B09 抵費城住處後開箱，B10 北方集會與風險，並非1850法案已發生。

## 逐景結果

### s63001 — KEEP

朋友一同搬箱符合旁白；朋友入鏡與提示詞略異，但不矛盾 B05。原圖及 trim 都保留兩人和木箱。

- 原圖：`/workspace/.video-work/curio-s63/keyframes/s63001-1.jpg`
- 原圖 SHA-256：`fba8a102f2f9af1a5439507ff1627e7b9d39327fad101e1c5f97a439f6507373`
- selected：`/workspace/.video-work/curio-s63/keyframes/s63001-1-trim.jpg`
- selected SHA-256：`62b3cf053931fe0feaabee12f3cc0854d471c1977cf5559d0a9e760bc33b2582`
- 機器：passed=True；needs_review=False；9.29/10。

### s63002 — KEEP

協助者查看開箱，符合出發前 B05；大頭短身是 chibi 表現，不能據此斷言歷史人物是兒童。

- 原圖：`/workspace/.video-work/curio-s63/keyframes/s63002-1.jpg`
- 原圖 SHA-256：`cfd903a000b95233bea1a237eb7a4977741581ce6dc7471f226ddd1f82a9bd7a`
- selected：`/workspace/.video-work/curio-s63/keyframes/s63002-1.jpg`
- selected SHA-256：`cfd903a000b95233bea1a237eb7a4977741581ce6dc7471f226ddd1f82a9bd7a`
- 機器：passed=True；needs_review=False；10/10。

### s63003 — KEEP

出發前人物與開箱相符；箱蓋豎立而非平放是道具細節，不改變尚未釘箱的敘事。

- 原圖：`/workspace/.video-work/curio-s63/keyframes/s63003-1.jpg`
- 原圖 SHA-256：`3dc46a76a83d790659194e5196a9c388903649bddddfe887bc8d2d614070f612`
- selected：`/workspace/.video-work/curio-s63/keyframes/s63003-1.jpg`
- selected SHA-256：`3dc46a76a83d790659194e5196a9c388903649bddddfe887bc8d2d614070f612`
- 機器：passed=True；needs_review=False；9.29/10。

### s63004 — KEEP

Black 卡通主角站在出發前開箱旁，表情猶疑。簡化上衣、年幼感不單獨構成重大年代／身分矛盾；trim 無關鍵內容損失。

- 原圖：`/workspace/.video-work/curio-s63/keyframes/s63004-1.jpg`
- 原圖 SHA-256：`9c5ae97b78f6c9cecddd1292b002398f6196e948f74495708b715b21c9977145`
- selected：`/workspace/.video-work/curio-s63/keyframes/s63004-1-trim.jpg`
- selected SHA-256：`3a826bc08b649d00507e7dce27e028bfb69fde021632f995589887bf7095608a`
- 機器：passed=True；needs_review=False；9.29/10。

### s63005 — REJECT

原圖清楚呈現多輛現代汽車、現代路燈及街道路牌，整體街景移至二十世紀以後，與 B03 的1848年里奇蒙妻兒消息情境構成重大年代矛盾；不是一件模糊小道具。

- 原圖：`/workspace/.video-work/curio-s63/keyframes/s63005-1.jpg`
- 原圖 SHA-256：`42689eae8a6a81abd45cc6188ca407b348e7eea3096e7bea126f5019f5b5df61`
- selected：`/workspace/.video-work/curio-s63/keyframes/s63005-1.jpg`
- selected SHA-256：`42689eae8a6a81abd45cc6188ca407b348e7eea3096e7bea126f5019f5b5df61`
- 機器：passed=True；needs_review=False；9.29/10。

### s63006 — KEEP

封閉貨箱、木甲板與蒸汽船符合 B07 船上無法掌控方向；無剖箱露出布朗。黃色工帽偏現代，但按本次可愛插畫標準屬局部工人造型道具，不能單獨要求重畫；trim 保留箱與船。

- 原圖：`/workspace/.video-work/curio-s63/keyframes/s63006-1.jpg`
- 原圖 SHA-256：`c6f001dca0428c21e7448c2c86b5b8090209a7b994d2cbd11f1dfcca186d678c`
- selected：`/workspace/.video-work/curio-s63/keyframes/s63006-1-trim.jpg`
- selected SHA-256：`d2d077ba4c94a4ea36acea8969b032a1fb78588150542e25dff48652d6591f9b`
- 機器：passed=True；needs_review=False；10/10。

### s63007 — REJECT

華盛頓轉車中的箱子畫成敞口、內部可見且空無一人；這不是箱蓋擺放小差異：B08 人仍藏在箱內、到費城住處後 B09 才開蓋，畫面破壞核心隱藏運輸事實。

- 原圖：`/workspace/.video-work/curio-s63/keyframes/s63007-1.jpg`
- 原圖 SHA-256：`a904e6def5295de57a0ddf81e521491e7d481b6cfa4c12c5294e870ea5ae913c`
- selected：`/workspace/.video-work/curio-s63/keyframes/s63007-1.jpg`
- selected SHA-256：`a904e6def5295de57a0ddf81e521491e7d481b6cfa4c12c5294e870ea5ae913c`
- 機器：passed=True；needs_review=False；9.29/10。

### s63008 — HOLD / REJECT current take

實圖是淺膚色講者與兩名聽眾，不是指定空講台。集會本身與 B10 並非史實矛盾，不能將「有人」單獨誇稱歷史錯誤；但現有機器主體檢查 FAIL、needs_review=true，且具名主角未能清楚呈現。本覆核不覆寫這項未通過門檻，現 take 不可直接採用。

- 原圖：`/workspace/.video-work/curio-s63/keyframes/s63008-1.jpg`
- 原圖 SHA-256：`879ed58e773aee25084d2b852064db3e92babf7f3558e0d42edde84c828ebfa1`
- selected：`/workspace/.video-work/curio-s63/keyframes/s63008-1.jpg`
- selected SHA-256：`879ed58e773aee25084d2b852064db3e92babf7f3558e0d42edde84c828ebfa1`
- 機器：passed=False；needs_review=True；9/10。

### s63009 — REJECT

貨箱被替換成有車輪的大型鐵路車廂，旁有明確汽車、電線與現代道路標線；主角外觀也未維持既有 Black 布朗設計。重大年代／核心物件錯置已足以拒收；車廂上25及東亞文字亦不合指定無字箱。

- 原圖：`/workspace/.video-work/curio-s63/keyframes/s63009-1.jpg`
- 原圖 SHA-256：`a4c4a88df61a4ae514fe34638cc4598f07278072e92dee55573461d41f58c51f`
- selected：`/workspace/.video-work/curio-s63/keyframes/s63009-1.jpg`
- selected SHA-256：`a4c4a88df61a4ae514fe34638cc4598f07278072e92dee55573461d41f58c51f`
- 機器：passed=False；needs_review=True；8.71/10。
