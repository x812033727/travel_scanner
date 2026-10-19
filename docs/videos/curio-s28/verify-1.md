# S28 獨立故事盲讀與來源複核

查核日：2026-10-19。此紀錄綁定 [`script.md`](script.md) SHA-256 `17029533a1eb318c5a78dcc5c0689634183b8f98e8f7d4cf45c850f1652fa965`，89 句、約 8.2 分鐘。覆核者未參與 S28 撰稿，先只讀劇本及 `narrative` 呈現的逐句時間稿，固定十三題答案後才開 [`research.md`](research.md)、[`claims.md`](claims.md) 與原文。`VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs narrative --slug curio-s28 --answers /tmp/curio-s28-blind-final-answers.json` **通過 13／13 題**；判斷記在工作目錄 `review/narrative.json`。

| 敘事題 | 判斷與逐句依據 |
| --- | --- |
| `scene_first`、`no_spoiler`、`opening_hooks` | 全是。`[jar001 00:00]` 有北宋庭院、孩子登甕的動作；`[jar003]` 停在石未擊出。`[jar004–08]` 懸置容器字、蘇軾行狀、球與圖畫。 |
| `one_line`、`one_thread`、`no_detour` | 全是。從《宋史》的救援，接到蘇軾的省略、言行錄的球與甕、古書異文及現代插畫的留白，始終追同一場救援如何被記下；球的段落在 `[jar051]` 清楚連回水的相反用法。 |
| `no_toc`、`chapters_link`、`chapters_are_events` | 全是。`[jar024]→[jar025]` 問蘇軾為何沒寫並立即打開行狀；`[jar041]→[jar042]` 開另一書；`[jar063]→[jar064]` 問並答《宋史》多哪一步。章名都指事件或新發現。 |
| `open_loops`、`payoffs` | 全是。問題／轉折無九十秒空檔；例如 `[jar056]` 問仁智評語來源，`[jar057–62]` 查標籤、較早文本和未定版本問題；`[jar084]→[jar085]` 直接回答「缸／甕」字。 |
| `no_recap` | **是。** `[jar005]` 的蘇軾「二十年」在 `[jar026]` 以「還記得開頭那二十年嗎？」明確回呼，並新增此話寫於行狀篇末；`[jar030]` 已刪，`[jar029]→[jar031]→[jar032]` 由省略進入可否推論的問題。`[jar018]` 的七歲與《左氏春秋》沒有在 `[jar028]` 重念；`[jar075]` 回呼 `[jar023]` 的京洛畫圖後新增「未附原圖」的限制。 |
| `outro_no_next` | 是。`[jar091 08:03]` 只邀請訂閱，沒有提下一支。 |

## 固定來源抽查

- [《宋史》卷三百三十六〈司馬光傳〉固定轉錄第 82603 行](https://github.com/garychowcmu/daizhigev20/blob/4a6d6f2088825f132521d848c2ea86cf9c9a7620/%E5%8F%B2%E8%97%8F/%E6%AD%A3%E5%8F%B2/%E5%AE%8B%E5%8F%B2.txt)：七歲講《左氏春秋》後，另敘「一兒登瓮，足跌沒水中……光持石擊瓮破之，水迸，兒得活」，再接「其後京、洛間畫以為圖」。沒有另給破甕年歲，也沒有附圖；`[jar018–23]`、`[jar075]` 的限定正確。
- [蘇軾〈司馬文正公光行狀〉固定轉錄第 1576 行](https://github.com/garychowcmu/daizhigev20/blob/4a6d6f2088825f132521d848c2ea86cf9c9a7620/%E5%8F%B2%E8%97%8F/%E4%BC%A0%E8%AE%B0/%E5%90%8D%E8%87%A3%E7%A2%91%E4%BC%A0%E7%90%AC%E7%90%B0%E9%9B%86.txt)：篇末原文「軾從公游二十年，知公平生為詳，故錄其大者為行狀，其餘非天下所以治亂安危者皆不載」。`[jar026]` 的「篇末親自寫下」與 `[jar033]` 的取材說法均吻合；整篇長傳寫七歲讀書、仕途和修史，未見破甕段。此省略不能證明蘇軾未聽過，更不能證明故事為假；`[jar031–38]` 保留這項界線。

本次獨立覆核的來源範圍是上述改稿與回呼涉及的固定段落；全片來源對照仍以 [`claims.md`](claims.md) 和 [`research.md`](research.md) 為準。沒有發現新阻斷。若再改旁白，十三題紀錄須綁新的劇本版本重做。
