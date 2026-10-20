---
id: 2026-10-20-curio-s55-first-human-balloon-flight
title: Curio S55 first human balloon flight episode
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-10-20T19:22:18Z
completed_at:
branch: codex/curio-s34-endurance-20261019
depends_on: []
scope:
  - docs/videos/curio-s55
---

# Curio S55 first human balloon flight episode

## Why

站主委託持續製作新的奇聞檔案局歷史片。S55 用 Franklin 1783 年致 Joseph Banks 的五封當時信追「第一次載人自由飛行」前後的氣球實驗，尤其分清無人氫氣球、動物、有人繫留熱氣球、11 月自由熱氣球及 12 月載人氫氣球；不能把預先繫留試升的樹梢事故剪成自由航程事故。

## Definition of done

- [x] 不重複既有 `curio-s*` 題目，找到三份固定版本全文並計算 SHA，寫來源等級、十二項可用主張和日期衝突。
- [x] 另一位工作者獨立重開 F／M／E 三份全文、重算雜湊、逐項核對 P01–P12；特別判定 F 信標日期、M 月份筆誤與 E 獨立日期是否處理充分。見 [題材覆核](../../docs/videos/curio-s55/source-feasibility-1.md)。
- [ ] 獨立 PASS 後寫 8–15 分鐘逐句劇本、claims、`video.json`；獨立逐句來源／書面畫面覆核與兩位新讀者敘事盲評通過。
- [ ] 配音、全季畫風插圖、配樂、長片、濃縮開場、5 秒片頭、21 秒片尾、Short 與真實連結完成工具與站台驗收；不可把待審說成已發布。

## Steps

- [x] 查重並選 A「從樹枝到脫繩」；把王室死囚軼事列為缺一手證據的 B 案而排除。
- [x] 取回 GITenberg 固定 1783 Franklin 信／1907 Rotch 編刊、1870 Marion 後出轉載與《大英百科》第九版固定機讀稿，填 [research.md](../../docs/videos/curio-s55/research.md)、[brief.md](../../docs/videos/curio-s55/brief.md)。
- [x] 獨立題材覆核 PASS；作者沒有自給 PASS。
- [x] 完成 149 句、127 個插圖分鏡、12 個回收及逐句主張的 [R1 作者凍結](../../docs/videos/curio-s55/author-freeze-r1.md)；正文以每分鐘 325 字估 8.21 分鐘，lint 0 錯誤／0 警告。
- [x] R1 [獨立逐句來源與畫面覆核](../../docs/videos/curio-s55/source-script-independent-r1.md) 判 HOLD；依九項阻點修成 [R2 作者凍結](../../docs/videos/curio-s55/author-freeze-r2.md)，149 句、138 個插圖分鏡、12 個回收。
- [x] R2 [獨立逐句來源與書面畫面覆核](../../docs/videos/curio-s55/source-script-independent-r2.md) 仍判 HOLD；作者依四項阻點和人群估算建議修成 [R3 精確凍結](../../docs/videos/curio-s55/author-freeze-r3.md)。R3 149 句、138 個插圖分鏡、12 個回收，lint 0 錯誤／0 警告，仍待另一人重新查核。
- [ ] 由另一位工作者獨立逐句核對 F／M／E 和畫面界線，再由兩位新讀者分別盲讀；此後才進付費配音與插圖。
- [ ] 核准後媒體照 curio-episode/youtube-video 的時長、付費、品管和手動上架規則往下做。

## How to verify

`git -C /tmp/s55-franklin-balloons rev-parse HEAD` 應得 `f9f2c7e6a25ffbcea1b28955239796378b00ce29`，`sha256sum /tmp/s55-franklin-balloons/43809.txt` 應得 `0db153d94652cff6845a43763400907170bfd3c5388816529e6f57f58eb3400e`；M 固定提交 `c3f6d020de7d9a0ad864aabcf89138476680574e`、`899-0.txt` SHA `2e474f42015f2e0841826202772cb94b3bd6a72a3321bfb2796161a67d8340e5`；E 固定提交 `504c6cb32cf7c33a6c40f4de191a429cf1619ccd`、百科〈Aeronautics〉檔 SHA `5f2a85e7be44b1590df9a03c988a9cd5684eeca34d482764a6beef94866b19d1`。請獨立重抓，不只相信作者本機檔。`npm run check:tasks` 驗票格式、`git diff --check` 驗空白；兩者不代替人工來源覆核。

## Notes

F 是 1783 年當時信的 1907 年壓印副本轉錄；M 是 1870 年後出英文史書，聲稱收 d'Arlandes 信與見證報告但未找到 1783 法文原件。E 是《大英百科》第九版的後出條目，Temple University 固定機讀稿標 CC BY 4.0。F 的第三封信印「Nov. 21」又說「昨天」飛行，編者明寫應校為信 **Nov. 22**、自由飛行 **Nov. 21**；E 同載 **Nov. 21**。M 錯記自由飛行「Oct. 21」，不可拿它當歷史日期；繫留十月試驗與 11 月脫繩航行須分清。F 記動物試驗為**聽來**、落地平安是乘員當晚**轉告**、兩人的視野亦是事後說法；只有 8 月 Champ de Mars、11 月 La Muette、12 月從馬車看的升空是他在場。

2026-10-20：題材獨立 PASS 後完成 R1；R1 和 R2 的獨立逐句覆核均判 HOLD。作者依第二輪全文把十一月煙袋假設、見火時點、四處逐句引文、十一月回溯和人群估算歸屬修成 R3。**R3 尚未經獨立來源／書面畫面重查或兩位盲讀；沒有付費配音、插圖或成片。**下一位用 R3 凍結雜湊查劇本；實際 8 分鐘底線待配音後量測。

2026-10-20：R1 已有[獨立逐句來源與書面畫面覆核](../../docs/videos/curio-s55/source-script-independent-r1.md)，結論 **HOLD**。固定原文與 R1 雜湊均重驗；主史實時序及日期衝突處理通過，但逐句來源歸屬、固定行號連結及若干分鏡的地點、年代、目擊界線和日光時段必須修正。此覆核沒有做敘事盲評，也沒有付費配音或插圖；修稿後須新凍結並再獨立覆核。

2026-10-20：R2 的[第二次獨立逐句來源與書面畫面覆核](../../docs/videos/curio-s55/source-script-independent-r2.md) 結論仍 **HOLD**；作者已依其阻點修成 R3，修訂詳見[作者交接](../../docs/videos/curio-s55/author-freeze-r3.md)。下一位應以 R3 原件與固定史料重查，不把作者的機械檢查當成獨立 PASS。

2026-10-20：R3 [獨立來源與書面畫面覆核](../../docs/videos/curio-s55/source-script-independent-r3.md) 判 **PASS**；其後兩位隔離盲讀的[官方 OR](../../docs/videos/curio-s55/review/r3-isolated-merge.md) 仍以 6/13 **FAIL**。R4 作者已依七項敘事阻點把十二月第二航程縮為一句對照、刪票券未回收問題、修開場與章首、補主線來源細節，並在[精確凍結](../../docs/videos/curio-s55/review/r4-author-freeze.md)記五檔 SHA。R4 機械 lint 0 錯誤／0 警告、最速正文估 8.20 分鐘、`test:docs-videos` 236/236；**仍待新工作者以 R4 雜湊獨立查源及兩位新讀者盲評**，無付費媒體、實際配音或成片。

2026-10-20：R4 [獨立來源與書面畫面覆核](../../docs/videos/curio-s55/review/r4-source-independent.md) 判 **HOLD**。固定 F／M／E 全文與五檔凍結 SHA 重驗、145 列來源連結與 135 景書面畫面、日期及十二月一句對照均已查；阻點是 `s55032`–`s55033` 把 F 被動語態的 Gonesse 破裂原因推測指名為富蘭克林本人。作者須修 `video.json`／`claims.md`／`script.md` 並重凍結，新任覆核者再驗；`s55125` 投料畫面宜標清機制示意。R4 沒有來源 PASS，亦無 R4 雙人敘事盲評或付費媒體。

2026-10-20：R5 作者已按 R4 HOLD 窄修 `s55032`–`s55033` 的無署名推測歸屬，並把 `s55125` 的投料畫面標為獨立機制示意；三檔已同步、精確雜湊與檢查見 [R5 作者交接](../../docs/videos/curio-s55/review/r5-author-fix.md)。R5 lint 0 錯誤／0 警告，最速正文估 8.21 分鐘；**仍待他人以 R5 SHA 獨立來源／書面畫面重查及兩位新讀者盲評**，未做付費媒體。

2026-10-20：R5 [獨立來源／書面畫面覆核](../../docs/videos/curio-s55/review/r5-source-independent.md) 判 **PASS**；兩位新讀者的[官方 OR 盲評合併](../../docs/videos/curio-s55/review/r5-isolated-merge.md)判 **FAIL 11/13**，共同失敗 `no_recap`、`no_detour`，B 的 `chapters_link` 異議亦列入 R6 編修。R6 作者已壓縮空球支線、刪十月重複繩索描述、讓章首立即接上前一章結果、使安全落地直接導入日期查核，並同步 brief／video／claims／script；[R6 精確凍結](../../docs/videos/curio-s55/review/r6-author-fix.md)列五檔 SHA。R6 lint 0 錯誤／0 警告，最速正文估 **8.11 分鐘**；**R6 仍待他人獨立查源與兩位新讀者盲評**，無付費媒體。

2026-10-20：R6 [獨立史料與書面畫面覆核](../../docs/videos/curio-s55/review/r6-source-independent.md)判旁白及書面畫面 PASS，`claims.md` 只因 `s55041`、`s55115`、`s55145` 三格直接行號不足而窄 HOLD。R7 作者只補三格來源欄；[單一用途錨點交接](../../docs/videos/curio-s55/review/r7-author-anchor-fix.md)列 R6／R7 五檔 SHA 和反向差分校驗。R7 lint 0 錯誤／0 警告、140 列對位；**仍待他人獨立核這三格和兩位新讀者盲評**，無付費媒體。

2026-10-20：R7 [來源錨點獨立覆核](../../docs/videos/curio-s55/review/r7-anchors-independent.md)為 PASS；兩位新讀者的[官方 OR 盲評合併](../../docs/videos/curio-s55/review/r7-isolated-merge.md)為 **FAIL 12/13**，共同必答 No 是 `no_recap`，A 另認為小冊子／圖畫段落岔路，B 另認為 `s55040` 遠距回收不夠明確。R8 作者移除 `s55047` 的詳報未出重述，以富蘭克林寄小冊子的具體動作取代；`s55048` 改用當時信的「據說約兩百土瓦茲」高度估計，`s55049` 直接接動物落地風險。五檔 SHA 和機械檢查見 [R8 作者凍結](../../docs/videos/curio-s55/review/r8-author-fix.md)：lint 0 錯誤／0 警告、最速正文估 **8.17 分鐘**。**R8 尚待他人獨立來源／畫面覆核及兩位新讀者盲評**；無付費媒體、實際配音或成片。

2026-10-20 R10 WIP 前製交接：現稿 [獨立來源／書面畫面](../../docs/videos/curio-s55/review/r10-source-independent.md) PASS；[兩位無先前對話背景讀者合併](../../docs/videos/curio-s55/review/r10-clean-merge.md) 13/13 PASS；[同版 Jev 政策](../../docs/videos/curio-s55/review/r10-policy.md) PASS。語音與逐句音檢仍由另一個進行中的關卡處理，本次交接**未取得音訊 PASS**；音訊驗證文件、進行中的封存檔與私有媒體不在此 WIP。實際插圖、配樂、成片及網站站主核准亦未完成。
