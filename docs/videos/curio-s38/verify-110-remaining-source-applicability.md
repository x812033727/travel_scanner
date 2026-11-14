# S38 R8ae｜剩餘 PF022–PF111 書面來源覆核沿用性

2026-10-22 UTC。獨立審者 `/root/s38_pf021_last_paper`，未撰寫本輪影片、既有剩餘提示詞或本次付費出圖。結論：**PAPER PASS，精確範圍是 PF022–PF111 共 90 個尚未產圖的 shot 場景**。既有來源覆核可沿用至現稿；這不是任何新原圖、全片分鏡、旁白聽審或成片核准。沒有改影片、claims、manifest、ledger 或媒體呼叫。

## 版本鏈與實際差異

| 證據 | 精確雜湊／結果 |
| --- | --- |
| 本票現稿 `video.json` | `a150042d8a53b5d63a86821759a81aef934240008ad4dd82c55bb83b99060844` |
| `script.md` | `e59ec137e3de3871e3b0e5063d8f6504d3eb2adb5fe22265eb3faa3d613d5951`，與 R8 相同 |
| `claims.md` | `f9de8d2771b62cc327f4e599f002af8f3278cfb0f39dbed201e7fdc857201d42`，與 R8 相同 |
| R8 原始全景來源 PASS 的 Git 版本 | `6ca6afb19`，video SHA `3dbe6dd23eedef3ff999801f6e548ab69ea480ee8a2b00095e78e1d48ec837b9`，與 `verify-8-source.md` 逐字相符 |
| 後續全景／增量紙審後 Git 版本 | `eb6cb65d0`，video SHA `33eceef58a3d25414f28606b1737258b256ff8a4bd9687f739974e42c0bb12bc` |
| 現稿 90 個完整場景 canonical JSON SHA | `768c93af93a047d51ebcc4cc45d14fa0e0bd1212e5b39808ae0c2acc2f3c7d9a`（sort_keys、compact separators、UTF-8／ensure_ascii=false） |

我從 Git 讀出兩份歷史原檔並重新實算 SHA，解析比較。**不能說這 90 景從 R8 從未改過**：R8 之後全數曾加成年／1666 英國服飾與合理建材的輪替後綴，另有九景核心措辭變更。它們經 `verify-9-audit.md`、`verify-10-audit.md`、`verify-11-audit.md`、`verify-12-audit.md` 及 `verify-13.md` 的全景或增量紙審承接。機械比較確認：**現稿 PF022–PF111 的完整場景物件 90／90 與 eb6cb65d0 完全相等**，包括 prompt、camera、visual、旁白、emotion 及章名；之後沒有剩餘景的未審新差異。頂層非 scenes 欄位亦全相等，仍由既有 cute-mystery preset 管理風格。

全片 112 句的 `(line.id, line.text)` 展平序列與 R8、eb6cb65d0 均相等。早期場景轉來源卡時，lines 物件的非口播格式可能不同，不能把整個 lines JSON 不同誤稱旁白改稿；實際 script／claims 原檔 SHA 與口播文字均未改。

## 九景核心修訂及來源界線

固定原文為 GITenberg Pepys 日記 commit `68fcf49f70ee793b989a6fd0464264d55beb4451`，本機 `/tmp/s38-r8j-pepys-4200.txt` SHA `3cd43a3c39ee72eb9c4a3657f1fcb1723afba291cedac176c65a39289483be5d`。我重讀以下關鍵連續段落以檢查增量鏈；其餘未改事件沿用 R8 的 112 句／111 提示詞全景覆核。

| 景 | 相對 R8 的核心改義及本次判斷 |
| --- | --- |
| PF040 | 火在橋的上游、下游延伸，修正模糊的「兩邊」。L65897–65901 明記 below and above bridge；PASS。 |
| PF053 | 明示成年男子穿 1660s 睡袍乘車。L65956–65964 明記自己穿 night-gowne 坐運財物車；PASS。 |
| PF071／PF072 | 成人挖**另一個**土坑，成人手把完整硬質 Parmesan 與酒放入第二坑；L65997–66002 支持人、順序、所有人及物件。腰部裁切、完整外皮、衣飾和輪狀是插畫選擇，沒有尺寸、價格、取回主張；PASS。 |
| PF073 | 日記旁改成空桌面，避免暗示埋後起司已被取回；所查條目未交代去向；PASS。 |
| PF076 | 從信使交接改成用鵝毛筆寫全白紙。L66004–66012 直接記 wrote to Coventry，刪去未記交接；PASS。 |
| PF080 | 主動炸屋作局部阻火間隙，而非不明原因自行倒塌。L66021–66026、66051–66052 明記 blowing up、局部火停；不能擴大成全城因此熄火；PASS。 |
| PF098 | 前景一人，背景 Moorfields 擠滿人與貨。L66102–66109 明記 full of people 及各自守貨；PASS。 |
| PF104 | 佩皮斯與工人正撲滅另一處火，非只看熄火後木材。L66127–66146 的正文記他和工人前往並很快撲滅；不把中間後編者括號當現場敘述；PASS。 |

成年／時代後綴是防止模型畫成學童、現代設備或錯置服裝的正向插畫提示，不額外宣稱已知個人外貌、衣物、建材或精確地形。PF025／PF027 的無字示意圖仍只作**口頭**討論的卡通道具，不是書面王令；PF085–PF088 的船運與看守不提前變成卸貨；PF107 才是九月六日卸貨；PF109–PF110 無字頁不是存世手稿重現，PF111 空坑是觀眾假設問題，不能暗示已取回起司。上述界線仍與 R8 報告一致。

## 產圖範圍、排除及上限

只讀媒體快照：manifest SHA `f7e8c720bde9b89d144b9affa163b2a5118cf6eb70cc7f81caef8c5d4d2228fa`，`visual_hash=af822564c5a1f831` 與現稿相符。正式 `keyframeProblems` 實跑為 **90 個缺圖、0 個其他問題**。ledger SHA `fd07b364058cb99b5cb5e8356a35e891c48df39acdb18cbca4281e2a43f657b6`：已付 **US$0.8765／59 image／59 judge／1 music**，另有舊 **US$0.0035 reservation**；沒有任何 PF022–PF111 的 image 付費紀錄。STOP 在位、jobs 空。

- 本次可畫範圍：**PF022–PF111，90 景**，每景跨所有 prompt 版次合計最多 **3 張實際原生圖**。這些景在上述帳本中均為零張。
- 排除新付費：既有 14 張 KEEP **PF001／002／003／004／005／008／010／011／012／016／017／018／020／021**。必須以現行 request key／judge stamp／實檔 SHA 吃快取，不能因整集指令重新買圖；先前已用完三次的景尤其不得再生。
- 排除非 shot：**PF006／007／009／013／014／015／019** 已是來源卡，**PF112** 是 outro。不得藉整集指令把這些景改回插圖或為它們買新圖。

按當前 image US$0.0035＋judge US$0.01 計，90 景各最多三試上界為 **90 × 3 × US$0.0135 = US$3.645**。加已付 US$0.8765 及舊 reservation US$0.0035，整集上界 **US$4.525 < US$4.58**，餘 US$0.055；既有音樂支出已含在已付數，這個計算沒有再授權新配樂或額外 judge。任何價目改變、額外重評、額外保留費或其他媒體都須先重算；不得用網站通用 US$200 cap 取代本集 US$4.58。

**建議：在 live 模型／餘額／價格、精確圖單／帳本、dry-run、快取可沿用與原有製作關卡均通過後，現稿可以做一次有界的剩餘整集 `keyframes --takes 3`，符合 curio-episode 已有整集一次產圖流程。** 這個靜態 PASS 不自行移除 STOP；協調者須設受控復原、保留不可變前置快照，確保工具只新買上述 90 景、每景最多三張且總額不超限。完成後仍逐張看原始與入選圖，依 judge、材料性旁白／來源矛盾及畫風驗收；未過景可先維持 HOLD，不把批次完成等同全片 KEEP。
