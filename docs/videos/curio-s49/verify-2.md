# S49 R2 作者修復收據（待獨立覆核）

2026-10-20。這是對 [R1 獨立來源與書面畫面覆核](review/r1-source-independent.md) **HOLD** 的作者差分修復紀錄；不宣稱來源、畫面或劇本 PASS。R1 報告 SHA-256：`e697b69b1ac1f4ef18fc1ad0f1328d565ef3f2a273983bd8517e9054ab1f5e67`。

## R1 發現的修復

- `moon083` 旁白改成「遠處不像鳥」，對齊 L1175–1189；`moon066` 書面草圖改成有彎角與眼上肉瓣，對齊 L825–842；`moon079` 改成明示報紙聲稱「四群」的字卡，避免單隻翼人畫面。
- `moon001`、`moon003`、`moon016`、`moon018`、`moon019`、`moon026`、`moon029`、`moon052`、`moon093`、`moon094`、`moon129`–`moon132` 補齊 R1 指出的跨錨點來源：出版日期及偽增刊名稱 `P02`、真實南天工作 `P06`、文章本體、皇家學會文件 `P03`，以及結論所串起的巨鏡、樹、翼人段落。`moon123` 發行量自述從錯誤的 `P13` 改連 1859 出版者序 `P02`。這些新增連結只支援可核文字；1859 重印本及其選錄仍不能冒充 1835 原報影像或獨立發行帳。
- `research.md` 的 `P12` 擴至 L1525–1635，涵蓋虛構失火、月相等待及土星「發現」。`moon080` 去掉錯置的「原始底片」，改說稿件聲稱有觀測圖而本集可核的是重印文字；畫面為普通紙上草圖。`moon124` 的帳簿畫面改成小冊堆疊，`moon125` 的畫面不出現銷量或帳本，旁白分別說「發行與銷售資料」。

## 固定來源與本輪交付 SHA-256

| 檔案 | SHA-256 |
| --- | --- |
| Locke 1859 固定文字 `/tmp/s49-moon-hoax-62779.txt` | `3ca0bc9b6fc5c50b090d61bf2049e925d22dd1cdef2b443a282f7fdc5749e654` |
| Jacoby 1902 固定文字 `/tmp/s49-jacoby-53396.txt` | `f5ab32e64e7ea3735ff90fb000ae8cc82dddea594e0de0c6be30b30f94485029` |
| `brief.md` | `48c3dc196b668c3ce3d58b4b3ffc26973262eb450587abfcc39d10d421057568` |
| `research.md` | `9476f53555e51da2471a72f75249e7e5fc8ed4ce3e30627578ce86cf4198c327` |
| `claims.md` | `2fcbd24ed8bbd6c6bb77d62194e81c4bc2ff4611e6aa0f8269f8a7c090e42a2d` |
| `script.md` | `ee25ba5be03898a2bfa5a6523e7fbb5bdc6000088aa91fd1eab0615a2ca84624` |
| `video.json` | `c1a298292932ba96d4b9def21a4e421426397166ea27d4597727b7cab48ee543` |

固定 commit URL、來源界線及 `Pxx` 原文範圍見 [research.md](research.md)。本輪沒有改兩份固定文字。`/tmp` 檔屬臨時下載；容器回收後須由固定 URL 重新取回並核上列 SHA。

## 靜態檢查

- `VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs script --slug curio-s49` 已重生逐句稿，narrative `a17306f19b1e97df`、speech `e49aac94fa69238f`。
- `VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s49 --json`：**0 errors／0 warnings**、136 句。`video.json` 與 `claims.md` 的 133 個 `moon` 句逐字一致；`script.md` 的全部 136 句亦與 `video.json` 一致。
- 8 句濃縮開場 167 spoken units，按較快 325 units/min 約 30.8 秒；正文 2,660 units 約 8 分 11 秒；片尾旁白 59 units。這些只是文字估時，須以 TTS 音訊實測。133 個編號場景中 126 `shot`、7 `big` 字卡，插圖場景占 94.7%；保留 12 組 `loops`。原版 5 秒品牌片頭、21 秒片尾及最後 16 秒 Studio 框仍只是包裝計畫。

**下一關：**請另一人對上述 R2 精確雜湊重新獨立讀來源、旁白及書面畫面，並更新獨立結論。R1 **HOLD** 在那之前持續有效。未生成 TTS、原圖、配樂、成片，也未做網站或 Studio 推送。
