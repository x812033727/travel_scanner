---
id: 2026-10-20-curio-s53-san-francisco-movable-relief
title: Curio S53 San Francisco movable relief cottages feasibility
status: in-progress
priority: P2
area: docs
owner: codex-s53-r11-author
claimed_at: 2026-10-21T01:49:57Z
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

2026-10-21 [下一批插圖非付費預檢](../../docs/videos/curio-s53/review/r10-next-art-paper-preflight.md)：全域額度讀回圖片餘 10,799、judge 餘 9,491、音樂餘 32，先前配額耗盡快照已過時；本集仍無付費圖／配樂，私有 `STOP` 已建立。`s53001/003/010` 的匿名人物提示詞雖有 R10 書面史料 PASS，卻缺成年／1900 年代服飾線索；參照 S38／S52 真實幼童漂移，先由作者做三景定點修補與可逆差分，交另一人獨立核對，再在建議的 US$4.78 畫圖加配樂上限內逐張試畫，原生 JPEG 不合史實即停。網站三卡與人耳仍待站主，不把技術零旗標當成網站核准。

2026-10-22 [R11 三景作者定稿](../../docs/videos/curio-s53/review/r11-three-prompt-author.md)：只改 `s53001/003/010` 三個 prompt，R11 `video.json` SHA `df63d7d13d5f440dfbf190bf7c527a99f4eae3ee21aafae6b27aae23d7c253dd`，結構化差分可逐位元還原 R10；台詞與其他四檔、既有 126 句技術音訊不變，lint 0／0。按站主常設推薦委派記錄整集插圖、judge、配樂合計 US$4.78 停線，帳本仍 US$0，STOP 存在。[R11 獨立書面覆核](../../docs/videos/curio-s53/review/r11-three-prompt-independent.md) **PASS，僅限三景逐張原生圖試畫**：先 `s53001`，直接看原圖，沒有年齡／時代／動作矛盾才續 `s53003`、`s53010`；遇到機器誤收的不合史實圖立即停。網站三卡及人耳仍待站主，這不是完成分鏡或成片核准。

2026-10-22 [R11 第一張原生圖停畫](../../docs/videos/curio-s53/review/r11-s53001-native-stop.md)：只買 `s53001` 1 圖／1 judge，原圖 SHA `af6f997ae433d7557c17ee3905210c94688d76f752203df56a2b7c6e1ccbeec6`。人物成年外觀與時代衣著尚可，但畫面變寫實住宅街與大房子，偏離 1907 廣場小型救災屋；judge 自己的 `style=0` 也判 9.71／10 FAIL。**人工 REJECT，STOP 已恢復**；帳本 US$0.0135／整集上限 US$4.78。`s53003`、`s53010` 沒有開畫。須先由作者把開放式廣場和低矮救災小屋規模定點修入 `s53001`，另人獨立紙面核對，再做最多一張定點試畫；網站、人耳、配樂、成片仍待辦。

2026-10-22 [R12 `s53001` 作者定點修補](../../docs/videos/curio-s53/review/r12-s53001-author.md)：只改首景 prompt 為開闊公共廣場與裸地上一排低矮單層木造救災屋，保留成年住戶與 1907 年六月。R12 `video.json` SHA `3b5382c1b06f882936d5e61823efe834f51b1b9c0a858c57f0fc18309be01949`，差分逐位元還原 R11；123 景與所有口播未動，lint 0／0。STOP 存在、帳本仍 US$0.0135／上限 US$4.78；**待另一人獨立核此精確提示詞和史料**，通過後僅准再試 `s53001` 一張並檢查原圖。

2026-10-22 [R12 獨立來源與書面畫面](../../docs/videos/curio-s53/review/r12-s53001-independent.md) **PASS，只限一張重試**；R12 可逐位元還原 R11，1913 年調查 L4970–5001 支持 1907 年六月廣場小屋仍在。[原生圖回條](../../docs/videos/curio-s53/review/r12-s53001-native-stop.md)：追加 1 圖／1 judge，原 JPEG SHA `1b586e6956669a3b6b521a9c7ed38acb43226e6c0eeead197e3f82bc9e483759`，出現明顯現代汽車、樓房與照片式街景；機器雖 9.29／10 PASS，但自身亦指出現代車／建築，**人工 REJECT、STOP 已恢復**。帳本 US$0.0270／US$4.78；下一步作者先收緊首景局部構圖並做可逆差分、另人紙面覆核，勿續 `s53003/010` 或整片插圖。網站卡、人耳、配樂與成片仍待辦。

2026-10-22 [R13 `s53001` 中近景作者修訂](../../docs/videos/curio-s53/review/r13-s53001-author.md)：直接比較 R11/R12 原圖後，只改首景 prompt，讓成年住戶與一棟低矮單層木造救災屋佔滿畫框，收起會讓模型補現代車街的廣角背景。R13 `video.json` SHA `8b9c141a39abb6f1d0ef6d815ce80154f5d136168dc90d64659e290f513432d2`；[差分](../../docs/videos/curio-s53/review/r13-s53001-structured-diff.json)逐位元還原 R12，其他 123 景、126 句口播與四檔來源／稿件不變。Lint 0／0，MiniMax 非付費 dry-run ready；STOP 存在，帳本仍 US$0.0270／上限 US$4.78。**待另一人獨立核史料、來源視覺界線與精確變更；未獲紙面 PASS 前不再付費畫圖。**

2026-10-22 R13 [獨立紙審](../../docs/videos/curio-s53/review/r13-s53001-independent.md) PASS 後，第三張 `s53001` [原尺寸驗收](../../docs/videos/curio-s53/review/r13-s53001-native-stop.md)仍 **REJECT**：多出前景人物，看不到低矮屋頂或廣場，機器亦 FAIL；STOP 恢復，累計 US$0.0405／3 圖／3 judge。R14 [作者來源日期卡](../../docs/videos/curio-s53/review/r14-s53001-source-card-author.md)只改首景為「1907 年 6 月｜舊金山／廣場裡的小屋／1913 年救濟調查回顧」，[精確差分](../../docs/videos/curio-s53/review/r14-s53001-card-structured-diff.json)還原 R13；[獨立覆核](../../docs/videos/curio-s53/review/r14-s53001-card-independent.md) PASS，只限該卡與首章八景一次試畫。R14 `video.json` SHA `0cbe40d9189710525bf82627bf21e411c2ea600870ceabc1975873e7b0fe1c19`，script／claims／口播不變；lint 0／0，115／123＝93.5% 插圖、卡片最多連續 1。

2026-10-22 R14 首章 `s53002–s53009` 一次八景首輪因前三張同類成年／年代錯誤已觸發 STOP；[六張原圖回條](../../docs/videos/curio-s53/review/r14-first-chapter-six-native-stop.md)列 `s53002–s53007` 全部人工 **REJECT**（前五張有 judge，其中四張錯誤地機器 PASS，`s53007` 僅付圖片費尚未評審）。`s53008–s53009` 未生成。私有原圖及 manifest 已保存，STOP 在位；帳本 **US$0.1115／9 圖／8 judge／0 預約**，低於 US$4.78 上限。現行 manifest 五筆無人工 KEEP。下一步先整批改 `s53002–s53007` 年代、成年身分、舊金山廣場與臨時小屋畫面，另人逐景來源／視覺紙審；在系統性錯誤未解前**不開全片插圖**。網站企劃／劇本／音訊卡及人耳、配樂、長片、Shorts、Studio 連結仍待完成。

2026-10-22 [R15 六景提示詞作者修訂](../../docs/videos/curio-s53/review/r15-first-chapter-six-author.md)：逐張看 R14 六張原圖後，只改 `s53002–s53007` 的提示詞，將易生成孩童、現代街屋、東亞簷口與有字文件的廣景收成 1907/1913 年室內、木屋門口和成年手部局部畫面；不改 126 句旁白、來源、運鏡或 s53001 來源卡。[六項可逆差分](../../docs/videos/curio-s53/review/r15-six-prompt-structured-diff.json)還原 R14 SHA，R15 `video.json` SHA `1617d0290291258231b1f6908f26c4dde988e0f4e77b4e0b63c0e4c9ae7cd349`。Lint 0／0、MiniMax 非付費 dry-run ready；STOP 在位、帳本不變 US$0.1115／上限 US$4.78。**待非作者獨立核六景史料與畫面後才可續畫；機器高分不能代替原尺寸驗收。**

2026-10-22 R15 [非作者六景紙審](../../docs/videos/curio-s53/review/r15-six-prompt-independent.md) PASS，僅限每景一次重畫；固定版 1913 調查與六項可逆差分、原圖、lint、STOP／預算均獨立核過。[六張原生圖驗收](../../docs/videos/curio-s53/review/r15-six-native-stop.md)：`s53002`、`s53005` 人工 **KEEP** 候選；`s53003` 背景風格與景別錯誤；`s53004`、`s53006`、`s53007` 仍把成年手部變童貌全身人物，後三張同類系統錯誤達停線。`s53006` 機器 9.29 PASS 仍人工 REJECT。六圖六 judge 新增 US$0.0810；帳本 **US$0.1925／15 images／14 judges／0 reservations**，低於 US$4.78 上限。原圖、trim、manifest、帳本與 log 私有封存，STOP 已恢復；`s53008–09` 和全片後續鏡頭未開。下一輪作者只針對四張拒收圖定點修 prompt 並記可逆差分，另人紙審後再試；網站卡、人耳、配樂、成片、Shorts 與 Studio 連結仍待完成。

2026-10-22 [R16 四景作者定點修訂](../../docs/videos/curio-s53/review/r16-four-prompt-author.md)：保留 R15 `s53002/05` 人工 KEEP 的 prompt 原字串與圖片鍵；只改 `s53003/04/06/07`，以灰髮皺紋的可見年長角色取代模型忽略的「畫外成年雙手」，木屋門口收窄背景，金屬扣包改小繫口布袋，雙表單改單張無字紙。[精確差分](../../docs/videos/curio-s53/review/r16-four-prompt-structured-diff.json)逐位元還原 R15 SHA，R16 `video.json` SHA `817819fb64717fb3dc6e5bd1e1957a5e7d14d9f8fb455001ac0d4a609ee62f12`；其餘 120 景及 126 句口播、claims／script 不變。Lint 0／0、四景非付費 dry-run ready，STOP 在位，帳本仍 US$0.1925／上限 US$4.78。**待另一人獨立核史料與畫面後，才可作一次限界重試；R16 再失敗時應評估同章合規畫面／資訊卡退路。**

2026-10-22 R16 [非作者四景紙審](../../docs/videos/curio-s53/review/r16-four-prompt-independent.md) PASS 後，僅畫 `s53003/04/06/07` 各一張並按 1280×720 未裁切原圖驗收：[原圖回條](../../docs/videos/curio-s53/review/r16-four-native-stop.md)及[逐張雜湊清單](../../docs/videos/curio-s53/review/r16-four-native-inventory.json)。`s53003/04/06` 人工 **KEEP**，`s53007` 因原圖黑邊及持袋動作易暗示單一付款人 **REJECT**，雖機器 9.29 PASS；R15 `s53002/05` KEEP 不變，首章六個原圖候選已有五張人工 KEEP。四圖四 judge 新增 US$0.0540；帳本 **US$0.2465／19 images／18 judges／0 reservations**，低於 US$4.78 上限，STOP 已恢復。`s53007` 已三次原生嘗試、兩輪提示詞修正，下一步依系列規則評估同章已收圖重用或一張合格來源卡，保持 ≥70% 插圖比率與卡片連續上限；勿再無界重試。`s53008/09` 與其餘全片插圖仍未畫，網站卡、人耳、配樂、長短片及 Studio 連結仍待辦。

2026-10-22 [R17 `s53007` 同章已收圖重用作者候選](../../docs/videos/curio-s53/review/r17-s53007-same-chapter-reuse-author.md)：R16 第三張仍 REJECT 後，不再買第四張。直接比對五張 KEEP 原圖，選第 3 句 `s53003` 的低矮救災小屋與年長住戶圖作第 7 句視覺回扣；畫面沒有錢或付款動作，避免把「誰付搬遷費？」問句指向單一付款者。只複製 `s53003` prompt＋camera 到 `s53007`，兩欄[可逆差分](../../docs/videos/curio-s53/review/r17-s53007-reuse-structured-diff.json)還原 R16；R17 `video.json` SHA `6550c8f26db13d1f72e9f706404e8d80efe131789fb4b37918b2ea9f48e222ae`，其他 123 景及全部口播不變。Lint 0／0、插圖 115／123＝93.5%、卡最多連續 1；STOP 在位、帳本仍 US$0.2465／上限 US$4.78。**待非作者核畫面來源與精確差分，通過後才定點重綁圖片快取及新 judge。**

2026-10-22 R17 [非作者同章重用紙審](../../docs/videos/curio-s53/review/r17-s53007-reuse-independent.md) PASS 後，僅對 `s53007` 重綁 `s53003` 已收圖片快取並另做此景 judge。[原生快取／judge 驗收](../../docs/videos/curio-s53/review/r17-s53007-reuse-native-pass.md)記 `10/10 (reused)`、**0 張新圖**，`s53007` 原圖和所選檔 SHA 與 `s53003` 相同，人工 **KEEP** 且沒有顯示誰付費；`s53003` 既有 manifest entry 不變。帳本只增 judge US$0.0100，現為 **US$0.2565／19 images／19 judges／0 reservations**，STOP 在位、低於 US$4.78 上限。首章 `s53002–07` 六鏡已有合格候選（第 7 鏡重用第 3 鏡），`s53001` 是來源卡；`s53008–09` 和全片後續圖片仍未畫。網站卡、人耳、配樂、長短片、Studio 可點連結仍待完成；勿把局部成功寫成全章或全片核准。

2026-10-22 R17 首章末兩景 [獨立紙審](../../docs/videos/curio-s53/review/r17-s53008-09-prompt-independent.md) PASS 後，僅畫 `s53008/09` 各一圖一 judge；[原圖停線回條](../../docs/videos/curio-s53/review/r17-last-two-native-stop.md)記兩張雖機器各 9.29 PASS，人工均 **REJECT**。`s53008` 畫成現代街景、現代背包／燈與童貌訪查員；`s53009` 有童貌、東亞街屋、缺廣場小屋及原圖黑邊。新增 US$0.0270，帳本 **US$0.2835／21 images／21 judges／0 reservations**，STOP 已恢復；首章分鏡仍 HOLD。下一步作者限兩景按原圖問題定點改 prompt、寫可逆差分，再交另一人紙審；勿擴大全片批次。網站卡、人耳、配樂、長短片及 Studio 連結仍待完成。

2026-10-22 [R18 末兩景提示詞作者定點修訂](../../docs/videos/curio-s53/review/r18-last-two-prompt-author.md)：只改 `s53008/09` 的 prompt，以 1908 年銀髮成年訪查者、低矮木屋和裸地取代現代街道／地圖；以 1907 年廣場裸地、低矮木屋、灰髮成年住戶與折起的毛毯取代東亞街屋廣角。[兩項可逆差分](../../docs/videos/curio-s53/review/r18-two-prompt-structured-diff.json)回填後逐位元還原 R17，R18 `video.json` SHA `81c8a7ef0efda1d86c02ab6ebc20199f6b9d70149c2a8cfaab731594e7d06519`。其餘 122 景、126 句口播及四檔來源／主張／劇本不變；lint 0／0、MiniMax 非付費 dry-run ready、兩景一輪約 US$0.03。STOP 仍在位、帳本仍 US$0.2835／21 images／21 judges／0 reservations，低於 US$4.78 上限。**待另一人獨立核兩景史料／畫面及精確差分後才可各試一張原圖；R17 機器 PASS 舊圖均人工 REJECT，不得沿用。**

2026-10-22 R18 [非作者兩景紙審](../../docs/videos/curio-s53/review/r18-last-two-prompt-independent.md) PASS 後，僅 `s53008/09` 各畫 MiniMax `image-01` 一圖一 judge，直接看 1280×720 原 JPEG 與所選裁圖。兩景皆人工 **KEEP**，無 R17 的童貌、現代／東亞街屋或黑邊；[原生驗收](../../docs/videos/curio-s53/review/r18-last-two-native-pass.md)及[逐圖雜湊清單](../../docs/videos/curio-s53/review/r18-last-two-native-inventory.json)列機器 9.29／10、原圖與裁圖 SHA。新增 US$0.0270；帳本 **US$0.3105／23 images／23 judges／0 reservations**，低於 US$4.78，STOP 已恢復。原 `s53002–07` 六圖與 manifest 條目未變；首章 `s53001` 來源卡及 `s53002–09` 八圖有可用候選。此容器缺相符 Playwright Chromium，CLI 未產生 contact sheet，已逐張開原圖／裁圖；完整分鏡、其餘章圖片、網站卡、人耳、配樂、長短片和 Studio 連結仍待完成。下一批先為第二章提示詞／史料做獨立紙審再限界開畫，不擴大本次兩景命令。

2026-10-22 第二章最早八張尚未畫的插圖 `s53010/11/14/15/17/18/20/21` 已做[精確雜湊獨立紙審](../../docs/videos/curio-s53/review/r18-next-chapter-eight-prompt-independent-hold.md)：八句旁白的固定來源前提均有支持，`s53010` 單景提示詞 PASS；其餘七景 **HOLD**，包括戶外帳棚卻用「窗光」、抽象匿名成年人反覆導致童貌風險，以及決策／南公園狹小／公布計畫與空泛圖紙動作不相合。整批未開畫，帳本仍 US$0.3105／23 images／23 judges，STOP 在位。作者只修這七個 `data.prompt`、保留 `s53010`，留可逆差分與新稿雜湊；另一人紙審通過後再按一景一次與三個相關失敗停線試畫。

2026-10-22 R19 [七景作者定點修訂](../../docs/videos/curio-s53/review/r19-next-chapter-seven-prompt-author.md)只改 `s53011/14/15/17/18/20/21` 圖像提示詞，`video.json` SHA `62254351988dae8424e0d94bb136a6b7171e5d991f2c9962508af03fc7248c3a`；八景[獨立書面覆核](../../docs/videos/curio-s53/review/r19-next-chapter-eight-prompt-independent-pass.md) **8／8 PASS**。受控原生[八景停線回條](../../docs/videos/curio-s53/review/r19-next-chapter-eight-native-stop.md)與[逐圖清單](../../docs/videos/curio-s53/review/r19-next-chapter-eight-native-inventory.json)：`s53011/14/15/17/20/21` 六張 1280×720 原圖人工 **KEEP**；`s53010` 因現代汽車與系列畫風不符 **REJECT**；`s53018` 供應商拒絕輸入 `input new_sensitive`，未產生圖或 judge。帳本 **US$0.4050／31 images／30 judges／0 預約**，低於 US$4.78，STOP 已恢復，首章八張 KEEP 不變。僅對這兩景窄修提示詞，另人紙審後才可再限界試畫；其餘章節、網站卡、人耳、配樂、長短片和 Studio 連結仍待。
