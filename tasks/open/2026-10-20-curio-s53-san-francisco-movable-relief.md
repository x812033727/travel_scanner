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
branch: codex/curio-preproduction-s46-s56-20261020
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

2026-10-22 R20 [兩景作者窄修](../../docs/videos/curio-s53/review/r20-two-prompt-author.md)只改 `s53010/18` 提示詞與 claims 畫面欄，劇本／旁白不動；[獨立紙審](../../docs/videos/curio-s53/review/r20-two-prompt-independent-paper.md) PASS，lint 0／0。兩景一次受控[原圖停線](../../docs/videos/curio-s53/review/r20-two-native-stop.md)均人工 **REJECT**：`s53010` 成長電桿街景、寫實漫畫比例，與來源的近景庭院／系列風格不符（累積兩張原生退件，下一張最多第三次）；`s53018` 畫出現代高樓及寬闊大道，與狹小公園地帶不符，雖機器 9.29 PASS 仍退件（本景首張實際原圖）。[逐圖清單](../../docs/videos/curio-s53/review/r20-two-native-inventory.json)列原生與裁圖雜湊；前 14 張 KEEP 圖單／檔案不變。帳本 **US$0.4320／33 images／32 judges／0 預約**，STOP 已恢復。兩景須先作者窄修及另人紙審，不得直接重畫；其餘章節／音樂／成片仍待。

2026-10-22 R21 [兩景作者再修](../../docs/videos/curio-s53/review/r21-two-prompt-author.md)及[獨立紙審](../../docs/videos/curio-s53/review/r21-two-prompt-independent-paper.md) **PASS 2／2**：`s53010` 改為成人與木牆圍住的近景庭院，避免長電桿街；`s53018` 由帳棚牆填滿狹縫，避免現代高樓／寬大道。僅兩個提示詞與 claims 同列畫面欄改，劇本／旁白／前 14 張 KEEP 不動；`video.json` SHA `4ac9a518d7387ea66918a89946636ee7dd6412f4926fbe7c5ccbb5a5a249f64a`，`claims.md` SHA `02ee7918a362ce130bed4a9e2c1491f0da80880207d7c57d6aa9eae1820a3022`，lint 0／0。服務 read-only dry-run 20 秒逾時，**未試 R21 原生圖**；STOP／帳本 US$0.4320／33 image／32 judge 不變。恢復後 `s53010` 僅可最後第三張、`s53018` 僅可下一張，均須看原圖而非只信機器；其餘章節／成片仍待。

2026-10-22 媒體站在 `NODE_USE_ENV_PROXY=1` 下恢復已登入 status；R21 [兩張限額原生圖與停線回條](../../docs/videos/curio-s53/review/r21-two-native-stop.md)、[雜湊清單](../../docs/videos/curio-s53/review/r21-two-native-inventory.json)已按各一 take 完成。`s53010` 第三／最後一張沒有現代車與電桿街，但原圖黑邊、人物偏右且畫風較成熟，裁圖僅解黑邊，機器 9／10 FAIL；**HOLD，不買第四張**，先評估同章收圖重用或來源卡，另人紙審。`s53018` 第二張實際原圖沒有高樓，但帳棚如照片、人物正面全身且通道過寬，機器 9／10 FAIL、人工 **REJECT**；任何下一輪先改畫面方案再獨立紙審。14 張舊 KEEP 條目／檔 SHA 未動，STOP 已恢復、jobs 空。帳本 **US$0.4590／35 image／34 judge／0 預約**，本輪新增 US$0.0270，低於 US$4.78 上限。其他分鏡、網站卡、人耳、配樂、長短片與 Studio 連結仍待完成。

2026-10-22 R22 [地震日來源卡與南公園窄景作者候選](../../docs/videos/curio-s53/review/r22-s53010-card-s53018-prompt-author.md)已凍結：`s53010` 三次原生圖已盡，不買第四張，改為有 1913 年調查歸屬的 1906-04-18 日期／事件卡；`s53018` 改為一名成年工作者胸肩近景側身擠過兩道帳棚牆，僅可在獨立紙審後再試一張第三／最後原圖。只改兩個場景及 claims 兩行畫面說明，[可逆差分](../../docs/videos/curio-s53/review/r22-two-scene-structured-diff.json)可逐位元組還原 R21；126 句旁白、其餘 122 景與前 14 張 KEEP 不動。R22 `video.json` SHA `49bdd04e5ebb88ff98cd207c6da0545faf1d1721834a0dc099d514a2daf9fa99`、`claims.md` SHA `34f765eee27fb0ff083413e3e209b42d5dd09b5a2a7a89f16d14556ce1cac44b`，lint 0／0，114／123 正文景為插圖，最長卡片連續 1；帳本仍 US$0.4590，STOP／jobs 空。**待非作者重新核 R22 精確史料、卡片及畫面，方可重綁 manifest 或付費。**網站、人耳、完整分鏡、成片與 Studio 連結待辦。

2026-10-22 R22 [獨立紙審](../../docs/videos/curio-s53/review/r22-s53010-card-s53018-prompt-independent-paper.md)通過後，`s53018` 第三／最後一張[原生圖獨立退件](../../docs/videos/curio-s53/review/r22-s53018-final-native-independent-reject.md)：人物正面站在寬帳門，沒有呈現核准的狹小空間，雖機器 9.29／10 PASS，人工 **REJECT FINAL**；不買第四張。退件圖自有效 manifest 移除，14 張舊 KEEP 不變；帳本 US$0.4725／36 image／35 judge，STOP 在位、jobs 空。R23 [作者來源引句卡與未畫景修訂](../../docs/videos/curio-s53/review/r23-s53018-source-card-author.md)：`s53018` 改 1913 年救濟調查英語原文意譯卡，`s53085` 尚未畫的重複木屋提示詞換為灰髮成年住戶開門的來源相符場景。[可逆差分](../../docs/videos/curio-s53/review/r23-s53018-source-card-structured-diff.json)可逐位元組還原 R22；R23 `video.json` SHA `2b5d0bfd85a581cac1e08ac8c155a9e8f89969634cc98e1c5300fe3457c7720e`、`claims.md` SHA `a276b8561f713f6160fe8fd4d68c79f0c85640ce0f4db2cf031d81f99e3c278e`，126 句音訊及其餘 122 景未動。Lint 0 錯誤／0 警告，113／123 正文景是插圖、連續卡最多 1 張；**待另一人核 R23 精確來源與差分，再重綁 manifest**。正式 TTS 正文時間軸為 17,651 影格／9:48.37，超過 14,400 影格門檻；114 句純音檔樣本合計 7:52.66，餘下 1:55.71 為工具標準呼吸和轉景間隔，R23 未增加。2,001 漢字在極快 325 字／分估 6.16 分鐘，只是稿長壓力測試而非實測。網站卡、人耳、後續圖片、配樂、長短片與 Studio 連結仍待。

2026-10-22 R23 [獨立來源與書面畫面紙審](../../docs/videos/curio-s53/review/r23-s53018-source-card-independent-paper.md)在作者灰髮修正後的精確雜湊上 **PASS 2／2**：1913 年英語調查原文支持南公園來源引句卡及遷屋後多數續作住宅的未畫景；Chromium 1920×1080 卡片版面探針無溢出。非作者反向驗證差分逐位元組還原 R22，lint 0／0、113／123 景插圖、連續卡最多 1。R23 `visualHash=14dade824c0840b3`，私有 14-KEEP manifest 仍綁舊 R22 `133eba68d1a96469`，且沒有 `s53018` 退件圖；**先安全離線重綁，逐項核 14 KEEP，再考慮下一張限額圖片**。紙審未做重綁／付費，也不代表網站、人耳、整章分鏡或成片核准。正式時間軸 17,651／14,400 影格過八分鐘門檻，但最終成片仍需 QA。

2026-10-22 R23 [離線重綁與預檢](../../docs/videos/curio-s53/review/r23-source-card-offline-rebind-and-media-preflight.md) **PASS**：私有 14-KEEP manifest 只更新至新 `visualHash=14dade824c0840b3`，實際檔 SHA／條目全不變、`keyframeProblems` 0、舊退件圖未接回；預檢 image-01 及即時全站 images／judge 餘額可用。接著僅 `s53023` 一張原生圖／一 judge：[停線回條](../../docs/videos/curio-s53/review/r23-s53023-native-stop.md)及[逐檔清單](../../docs/videos/curio-s53/review/r23-s53023-native-inventory.json)記機器 9.29 PASS，**人工 REJECT**：原圖童貌人物戴亮黃硬帽、現代感廣場和巨型示意板；示意板有小屋草圖，但沒有實體救濟木屋或帳棚，也不是核准的救濟工作者近景。於第一張退件即停，`s53024` 沒開畫；有效 manifest 安全還原 14 KEEP、退件原圖留私人證據，jobs 空、STOP 在位。帳本 **US$0.4860／37 image／36 judge／0 預約**，低於 US$4.78 上限，lint 0／0。下一位須先按原圖問題窄修 `s53023` 提示詞及 claims 畫面欄，再交非作者精確紙審方可限額重試；`s53010/s53018` 均不可第四次開畫。其餘 99 張插圖、網站卡、人耳、配樂、長短片和 Studio 連結仍待。

2026-10-22 [R23 `s53023` 原圖非作者覆核](../../docs/videos/curio-s53/review/r23-s53023-native-independent-reject.md)也為 **HUMAN REJECT**：同一 SHA 的未裁 1280×720 圖像雖有看板小屋草圖，人物全身童貌／現代亮黃硬帽、廣場鋪面與系列色盤失配，judge 的 9.29 PASS 不足採收。非作者未付費或改檔。原提示詞只寫 `anonymous relief worker`，未明寫成年，故下輪作者需明確收窄此點；原稿沒有變，仍維持 14 KEEP 與停線。

2026-10-22 R24 [作者一景窄修](../../docs/videos/curio-s53/review/r24-s53023-adult-park-author.md)：只改未畫 `s53023` 的 prompt 和 claims 對應整行，改為 1906 年裸地公園廣場帳棚前、銀髮有面紋的中年工作者近景看手持無字小紙小屋草圖，避免 R23 童貌亮黃硬帽、鋪面廣場與巨型看板。場景仍在 9 月 10 日動工前，**不提前畫出完工小屋**；新增 D 固定來源支持帳棚／建屋時序，G 原來源支持公園場地條件。R24 `video.json` SHA `07193188815a7b74529761f3a5c7c5656e9f1e954170b0bf71810cd9b17be1e9`、`claims.md` SHA `267fdb63c5f2a36f479bdc3903f06e07a93a21a55659e570a7001b2920799dc7`，[可逆差分](../../docs/videos/curio-s53/review/r24-s53023-adult-park-structured-diff.json)反向逐位元組還原 R23。其餘 123 景、126 句口播與既有音訊／14 KEEP 不動；lint 0／0、插圖 113／123、連卡最多 1。私有 manifest 尚綁 R23 `visual_hash=14dade824c0840b3`，R24 目標 `2b988530521f84c1`；帳本仍 US$0.4860／37 image／36 judge，STOP 在位、jobs 空。**待不同工作者按 R24 精確檔案作來源／畫面紙審 PASS，才能安全離線回綁與一張限額重試；本回未付費。**

2026-10-22 R24 [非作者來源與書面畫面紙審](../../docs/videos/curio-s53/review/r24-s53023-adult-park-independent-paper.md) **PASS**，確認 G／D 固定史料、公園委員會不干預期限、帳棚與建屋時序、差分反向逐位元組還原 R23、126 句不變、lint 0／0。之後[受控原生停線](../../docs/videos/curio-s53/review/r24-s53023-native-stop.md)與[圖像／帳本清單](../../docs/videos/curio-s53/review/r24-s53023-native-inventory.json)：先安全離線把私有 manifest 由 R23 回綁 R24 `visual_hash=2b988530521f84c1`，14 KEEP 實檔／條目無變，再購 `s53023` **第二張**實際原圖一張／judge 一次。原圖雖有灰髮成年人和兩頂帳棚，但帳棚／地面呈攝影寫實、人物跪地全身而非腰以上近景、紙上是高屋而非小屋屋頂簡筆；機器 9／10 FAIL，人工 **REJECT**，立即停，不試第三張或 `s53024`。原圖／裁圖與 15 景原生 manifest 留私人證據，有效 manifest 已還原 R24 14 KEEP SHA `798d0dc76304105bdb48b8217e000474c977df39cf22789024182d1d3fb17acf`，退件條目移除，jobs 空、STOP 在位。帳本 **US$0.4995／38 image／37 judge／0 預約**，低於 US$4.78。下一位須只針對此景再窄修提示詞與 claims、讓另一人按新雜湊紙審；最多第三／最後原生圖，失敗後評估同章合格圖重用或來源卡，不買第四張。`s53010/s53018` 亦不可第四次開畫。99 張未畫插圖與其餘成片關卡仍待。

2026-10-22 [R24 非作者原尺寸圖像覆核](../../docs/videos/curio-s53/review/r24-s53023-native-independent-reject.md)再次 **HUMAN REJECT**：逐張重算原圖／裁圖 SHA，具體指出全身跪坐、寫實帳棚與地面、紙上多層樓房型的三個失配；獨立核有效 manifest 14 KEEP、ledger US$0.4995、jobs 空和 STOP 在位。此覆核沒有改稿、購圖或放行下一張。

2026-10-22 R25 [第三／最後原生圖前作者窄修](../../docs/videos/curio-s53/review/r25-s53023-final-prompt-author.md)：只改 `s53023.data.prompt` 與 claims 同列畫面欄，從 R24 的全身／寫實背景失配收窄為銀髮中年工作者只露臉、肩、手，低頭看下巴下手掌大小、折起且無字的兩個低矮小屋屋頂草圖；背景僅一面帆布帳棚牆，沒有先畫完工小屋。[可逆差分](../../docs/videos/curio-s53/review/r25-s53023-last-prompt-structured-diff.json)反填逐位元組還原 R24；R25 `video.json` SHA `0ca53d7d67a8601f20ae8473f5d8be0bf1389b720cd3a029cdbe446855a783c6`、`claims.md` SHA `67907db0a94cadd1e213a72995834a17537cc27f007c139ce29341ae37a02500`，其餘 123 景、126 句及音訊不動。Lint 0／0，113／123 景插圖、卡片最多連續 1；私有 14-KEEP manifest 尚綁 R24 `visual_hash=2b988530521f84c1`，R25 目標 `a455331f94170433`；帳本仍 US$0.4995，STOP 在位，未付費。**待不同工作者按 R25 精確檔案獨立紙審；PASS 前不重綁、不買第三張。**第三張若仍退件，改用同章既收圖重用或有來源卡，不買第四張；`s53010/s53018` 亦不得第四次。

2026-10-22 R25 [第三／最後原生圖驗收](../../docs/videos/curio-s53/review/r25-s53023-final-native-keep.md)、[逐檔清單](../../docs/videos/curio-s53/review/r25-s53023-final-native-inventory.json)及[非作者原尺寸覆核](../../docs/videos/curio-s53/review/r25-s53023-native-independent-visual.md)：先按 R25 exact-hash 書面紙審 PASS 安全離線重綁，原 14 KEEP 條目／實檔不變，再只畫 `s53023` 第三／最後圖一張與 judge 一次。未裁原圖灰髮成年工作者持無字兩座低矮小屋**概念畫**、帆布牆背景，無已建屋或現代硬帽／廣場；機器 10／10 PASS，作者與非作者 **HUMAN KEEP**。成圖紙張約胸寬且直視前方，故只把 claims 同列畫面描述窄校正，來源／126 句旁白／`video.json`／音訊皆不動；可逆差分與新 claims SHA 見回條。有效 manifest 現 15 KEEP，14 舊圖沒變，15 景 `keyframeProblems` 0；113 張 shot 還缺 98 張。帳本 **US$0.5130／39 image／38 judge／0 預約**，整集上限 US$4.78；STOP 在位、jobs 空，lint 0／0。下一景仍須照既定來源／書面畫面界線逐張原尺寸驗收，機器高分不足代替人工；`s53010/s53018` 禁第四張。網站卡、人耳、其餘分鏡、配樂、成片與 Studio 連結未完成。

2026-10-22 R26 [下一景首張原生停線](../../docs/videos/curio-s53/review/r26-s53024-native-stop.md)與[逐檔清單](../../docs/videos/curio-s53/review/r26-s53024-native-stop-inventory.json)：R5 已獨立查過的未改 `s53024` 先通過 image-01／即時額度預檢，僅一張原圖／一 judge。機器 9.29 PASS，原尺寸作者 **HUMAN REJECT**：人物童貌、近代棒球式軟帽、手持完全空白紙而非無字公園地圖，且是辦公桌中景而非辦公室廣景；裁圖不能修正。第一張退件即停，`s53025` 沒畫。16 景原生 manifest／退件原圖／裁圖／contact sheet 私人封存；有效 manifest 已安全移除退件並清空過期 sheet 引用，**15 KEEP** 各選檔 SHA 全對、`keyframeProblems` 0，STOP 在位、jobs 空。帳本 **US$0.5265／40 image／39 judge／0 預約**，低於 US$4.78；113 張 shot 尚缺 98 張。下一位需先窄修 `s53024` 提示詞及 claims 畫面欄、寫可逆差分，再由非作者按新雜湊獨立紙審，通過才可試第二張；`s53010/s53018` 禁第四張。網站卡、人耳、其餘分鏡、配樂與成片仍待。

2026-10-22 R27 [作者窄修候選](../../docs/videos/curio-s53/review/r27-s53024-adult-map-author.md)：只改 R26 首張退件 `s53024` prompt 與 claims 同列畫面欄，以 1906 年救濟辦公室廣景、可見灰髮面紋的未戴帽成年職員、桌上明顯畫出公園／廣場方格的無字概念地圖，修童貌軟帽、空紙與中景；來源 G 的詢問、委員會無權正式准許及時序未改。[可逆差分](../../docs/videos/curio-s53/review/r27-s53024-adult-map-structured-diff.json)反填逐位元組還原 R26，R27 `video.json` SHA `458d3391180cff7b57abe2081eba956b711d9572a18f7acbf59c1a185c6a9b1c`、`claims.md` SHA `87a5b5d15e0e2e73bc14b1160b66017f6617f746fdbf76401eae4fc5dc5900c7`，126 句／音訊及其他 123 景不動。Lint 0／0，新 visualHash `018662cfba7a270f`；私有 15-KEEP manifest 尚綁 R25 舊 visualHash，STOP 在位、jobs 空、帳本 US$0.5265 未付費。**待另一人按 R27 精確檔案獨立來源／畫面紙審 PASS，才可離線重綁、即時預檢、最多第二張原生圖；本輪沒有重綁或購圖。**

2026-10-22 R27 [非作者來源／書面畫面紙審](../../docs/videos/curio-s53/review/r27-s53024-adult-map-independent-paper.md) **PASS** 後，安全離線把私人 manifest 只重綁新 `visual_hash=018662cfba7a270f`，舊 15 KEEP 完整條目／選圖 SHA 全不變；即時 image-01 與全站額度預檢通過，再僅買 `s53024` **第二張**原圖／一 judge。[作者原圖驗收](../../docs/videos/curio-s53/review/r27-s53024-second-native-keep.md)、[非作者原尺寸覆核](../../docs/videos/curio-s53/review/r27-s53024-second-native-independent-visual.md)與[逐檔清單](../../docs/videos/curio-s53/review/r27-s53024-second-native-keep-inventory.json)記機器 9.29 PASS，灰髮成年職員無帽、雙手指桌上清楚的公園方格概念圖，**HUMAN KEEP**；機器只嫌中景非完整廣景，未改旁白事實。另一位審者一度疑側櫃器物／架上冊夾偏新，重讀系列規則及原尺寸後撤回確定退件，保留未能證實年代的背景疑慮；正式非作者覆核同意沒有明確時代矛盾。首張退件圖已私人備份，沒有第三張或 `s53025` 新圖。有效 manifest **16 KEEP**、16 景 `keyframeProblems` 0，113 張 shot 仍缺 97；帳本 **US$0.5400／41 image／40 judge／0 預約**，整集上限 US$4.78；STOP 在位、jobs 空，lint 0／0。`s53010/s53018` 不買第四張；網站卡、人耳、其餘分鏡、配樂、長短片與 Studio 連結仍待。
