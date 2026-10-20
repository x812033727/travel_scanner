---
id: 2026-10-20-curio-s53-san-francisco-movable-relief
title: Curio S53 San Francisco movable relief cottages feasibility
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-10-20T17:28:48Z
completed_at:
branch: codex/curio-s34-endurance-20261019
depends_on: []
scope:
  - docs/videos/curio-s53
---

# Curio S53 San Francisco movable relief cottages feasibility

## Why

站主委託持續製作新的奇聞檔案局歷史影片。S53 需要一個不重複既有集數、在本雲端可直接重開史料的新題，先把選案與來源界線交給獨立覆核者。

## Definition of done

- [x] `docs/videos/curio-s53/brief.md` 說明 A／B 與推薦案、單一故事線、系列片頭片尾及可點連結的後續要求。
- [x] `docs/videos/curio-s53/research.md` 固定來源提交和原始檔 hash，逐項說明可說主張與不能跨越的推論。
- [x] 另一位工作者獨立重開來源、查數字與題材去重，決定來源關卡及下一階段。

## Steps

- [x] 讀 `AGENTS.md`、`curio-episode`、`youtube-video`、`task-board`，查系列題庫、S01–S52 企劃與任務看板。
- [x] 從固定 Git 提交重開 1906 年新聞編書和 1913 年救濟調查，在本雲端讀關鍵章節並重算原檔 SHA-256。
- [x] 寫 S53 的兩案企劃、研究主張表與獨立覆核請求。
- [x] 獨立覆核完成：題材 A 來源可行 PASS，見 `review/r1-feasibility-independent.md`。
- [x] R2 作者先修企劃／主張措辭，再寫逐句稿、畫面提示詞與作者凍結。
- [x] R10 另一位工作者覆核固定來源、逐句主張與書面畫面 PASS；兩位此前未讀 R10 的讀者各 13／13，官方 OR 合併 PASS。見 [R10 獨立來源](../../docs/videos/curio-s53/review/r10-source-independent.md)與[敘事合併](../../docs/videos/curio-s53/review/r10-official-merge.md)。
- [x] R10 影片政策 PASS、企劃／劇本站台卡誠實送為 hand-pushed pending；本機委派編輯選擇後完成 126 句 TTS，兩輪限縮重錄後官方音檢零旗標、實測正文 9:48.37。見 [verify-10.md](../../docs/videos/curio-s53/verify-10.md)。
- [ ] 站主網站審查企劃／劇本／音訊三張 hand-pushed 待審卡；付費插圖、配樂、成片和發布等後續關卡仍待辦。

## How to verify

`sha256sum /tmp/s53-sf-relief/56217-0.txt /tmp/s53-sf-calamity/1560-0.txt` 核對研究表；依 `research.md` 的固定連結重開原文；`npm run check:tasks` 核票格式，`git diff --check` 核空白。

## Notes

作者候選題：1906–1908 年舊金山地震、火災後，公園救災小屋因臨時場地期限與買賣契約而搬離。主證是 1913 年編纂救濟調查（含 1908 年訪查），不是當天原始日記；1906 年新聞編書只作歸屬清楚的現場氣氛，數字不採。5,610 是建成小屋、5,343 是搬出營地、680 是較完整訪查紀錄，勿混算或誤稱全部位於金門公園。作者交接時只完成題材可行性，當時沒有獨立來源 PASS、劇本或媒體。下一位工作者的核對清單見 `docs/videos/curio-s53/research.md`。

2026-10-20 獨立覆核：兩份固定原文重新下載且 hash 對上；題材 A **來源可行 PASS**，尚非全稿史料 PASS。`docs/videos/curio-s53/review/r1-feasibility-independent.md` 逐項列 F01–F09、樣本母體與視覺界線。寫稿前必修：(1) A 案「房子究竟怎麼搬」缺搬運方式原始證據，改問誰付費及遷往哪種土地；(2) F08 的 23 起地主扣屋屬失訪 457 棟中的報告已知事件，不能當作受訪 680 戶的樣本；70 買地才是 680 內。F09 的 82% 分母不明，保持不用。清場期限仍只由 1913 報告證成，旁白要歸屬。下一階段需由作者改企劃後寫逐句劇本，不得直接進媒體。

2026-10-20 R2 作者已修上述 A 案與 F08／F09，寫完 135 句 `video.json`／CLI `script.md`、135 行 `claims.md`、原創插圖提示詞及 [五檔 exact-hash 作者凍結](../../docs/videos/curio-s53/review/r2-author-freeze.md)。固定 R／C 原檔 SHA 仍對上。`lint` 0 errors／0 warnings；`test:docs-videos` 236／236；`check:tasks` 2124 票格式通過；沒有付費媒體或站台核准。**下一位須獨立重開原文，覆核逐句史料與書面畫面並安排兩名全新盲讀者；作者檢查不當獨立 PASS。** 完成本輪後已釋出認領，供獨立工作者續接。

2026-10-20 R3 獨立逐句來源／書面畫面見 [r3-source-independent.md](../../docs/videos/curio-s53/review/r3-source-independent.md)：兩份 pinned raw 重新下載，hash 正確；五檔與 R3 作者凍結 exact hash 相同。**史料／主張包限縮 HOLD，書面畫面 PASS。** `claims.md` 的 `s53011` 公園暫住句需補 R L4250–4264 直接錨點；`s53095` 須把「寡婦」限為原文的「帶孩子的寡婦」，同步旁白、主張和 CLI 劇本。其他 R2 問題已核修；130／130 口播和主張對齊、120 插圖／7 卡、13 loops 有效、lint 0 errors／0 warnings，快估正文仍 8:13.57。作者窄修並重凍後需另一人查差分；兩位隔離盲讀須用同一最終版。仍無付費媒體或發布放行。

2026-10-20 R3 [官方雙人盲讀合併](../../docs/videos/curio-s53/review/r3-official-panel-merged.md)為 **10／13，FAIL**：`scene_first`、`payoffs`、`no_detour`。R4 作者已補直接公園錨點並限縮帶孩子的寡婦；將前四句留在 1907 年六月同一廣場、第五句歸屬 1913 調查，刪去木材物流和多餘名冊／公寓旁枝，把未付地租的提問接到失訪 23 起已知扣屋，見 [R4 五檔 exact-hash 作者凍結](../../docs/videos/curio-s53/review/r4-author-freeze.md)。現為 **129／129** 口播與主張對齊、119 插圖／7 卡、16 loops，lint 0 errors／0 warnings；快估正文 **8:18.67**，但不是實際 TTS。作者沒有做獨立 PASS、政策、付費媒體或站台核准。下一位只按 R4 凍結 hash 重新核變動來源與書面畫面，另安排兩位此前未讀 R4 稿者只憑同一稿隔離做官方 13 題，未全過繼續 HOLD。

2026-10-20 R10 狀態以 [verify-10.md](../../docs/videos/curio-s53/verify-10.md) 的精確五檔與私有音訊雜湊為準：獨立來源／書面畫面 PASS、隔離雙讀者官方 OR 13／13 PASS、政策 PASS；網站企劃／劇本卡皆 hand-pushed pending，R10 劇本卡取代舊 R5 卡。本機委派編輯選擇與網站待審分開記錄。語音首輪新合成 16 句、沿用 108 段；`s53110` 經兩輪單句重錄後，126／126 音檢零旗標；實測 50.33 秒開場、9:48.37 正文、17.07 秒旁白片尾。後續 [音訊卡及插圖預檢](../../docs/videos/curio-s53/review/r10-art-preflight.md)：音訊精確 timeline 卡已送出為 hand-pushed pending；116 景非付費估價約 US$1.57／最多 US$4.70，本片媒體已花 US$0／US$200 上限。網站全域 judge 剩 15 次、音樂剩 0 次，需開畫前重查額度。現有書面提示詞獨立來源／畫面鏈已過，生成圖仍要逐張驗收；按 S51／S49 順序未畫插圖、未做配樂／成片。仍需站主網站決定與聽音。
