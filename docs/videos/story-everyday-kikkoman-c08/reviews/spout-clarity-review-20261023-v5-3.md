# C08 v5.3：瓶嘴口語與配對卡獨立差異覆核

2026-10-23（Asia/Taipei）｜審查者 `codex-c08-independent-v5-3`｜**本輪來源／配對畫面 PASS；製作時間軸仍 HOLD**。本輪只覆核 v5.2 之後改動的 `c080407–408` 旁白與 `c080407` 示意卡，連同相鄰 `c080405–410` 的語意銜接；不把舊版收據當成本版盲讀、成圖或站主核准。

| 綁定對象 | 值 |
| --- | --- |
| 草稿 PR [#1681](https://github.com/x812033727/travel_scanner/pull/1681) 的 v5.3 作者輸入 head | `6d8f14af7bcb8fb0545fd683cca8df1de150481c` |
| `script.md` SHA-256 | `B9E4C547FFA190609B433D48FF7E27A94B9C9DF4322AEB48104A3163694B3376` |
| `visual-plan.md` SHA-256 | `776F26F2E15477D443C6D8CFAC0EF32440DCBE5EFA85CA022FEDE7F883A84785` |
| `script-source-addendum.md` SHA-256 | `82D1147FE720B4ECB3A9222C8A19E76717BC40B4E70B56EA9A3256F5D22DEDE5` |

## 逐項判定

| ID | 判定與來源邊界 |
| --- | --- |
| `c080407` 旁白 | **PASS**。榮久庵[本人回憶 E1](https://toyokeizai.net/articles/-/10265?display=b)明說茶壺常是下側突出，桌上瓶反過來讓上側突出；[龜甲萬受訪 K4](https://news.mynavi.jp/techplus/article/20140106-syouyu/)明說下部短於上部。因此「下緣往瓶裡縮，上緣留在前面」作為**上下緣相對位置的口語描述**有據；不得解讀為會動的零件、精確角度或原型剖面。[MoMA M1](https://www.moma.org/collection/works/90106)的 inward angle 支持同一瓶嘴末端的內收概念，但並未量出尺寸。 |
| `c080408` 旁白 | **PASS**。往前傾再扶正的日常動作與 [M1](https://www.moma.org/collection/works/90106) 所述瓶嘴較不積液、較少滴到桌面的機制相容；[GK D1](https://www.gk-design.co.jp/en/archives/history/2242/)亦歸納截短瓶嘴處理滴漏。新句用「比較不容易」限定結果，沒有報流量、保證零滴或宣稱精確液體回流路徑。 |
| `c080407` 卡 | **PASS**。單張泛用側面示意只標「下緣收短、上緣留長」，與本版旁白同一個相對關係；文字明示非原物精確剖面，不畫角度或液路。它是後製示意卡，不能當作原始設計圖或實際生成圖驗收。 |
| 相鄰 `c080405–406,409–410` | **PASS，無新矛盾**。茶壺對照接到反轉的瓶嘴，再接較少積液／滴漏；「較不容易」的層級沒有被相鄰句升級成實測流速或零滴保證。 |

以 v5.2 review commit `f43f6242cebca866d0c4bfa5e80552e01bf8b6cc` 對 v5.3 作者 head 比對，`script.md` 的其他 **82** 列及 `visual-plan.md` 的其他 **83** 列未改；來源補充檔 SHA-256 未改。重新按資料列計數仍是 **84 句／84 鏡，73 shot／11 card**。先前 [v5.1 來源／配對畫面 PASS](line-source-visual-review-20261023-84-delta-v5-1.md) 和 [v5.2 計數 PASS](visual-count-review-20261023-v5-2.md) 各自保留原雜湊效力；本收據只補上這次差異。

**仍 HOLD 的後續關卡**：新旁白需重新做只看旁白的盲讀；正文 TTS 時長、鉤子實際間隔及插圖畫面秒數仍須以成片時間軸驗證。73／84（86.9%）只是鏡數比例，不是畫面秒數。未生成或購買素材，未匯入、上傳、合併或發布；本 PASS 也不是站主腳本／視覺核准。review-only commit 追加後的 PR head 可變，但上述三個作者檔案 SHA-256 才是此判定的內容邊界。
