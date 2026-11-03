---
id: 2026-10-31-b01-shimano-b02-lonely-planet-b03
title: 奇聞檔案局品牌三集：山葉 B01、Shimano B02、Lonely Planet B03（研究、稿子、查核、盲評，付費前報價）
status: in-progress
priority: P2
area: docs
owner: claude-opus-5-5-curio-brand-b
claimed_at: 2026-10-31T14:58:22Z
created_at: 2026-10-31T14:58:19Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/curio-b01
  - docs/videos/curio-b02
  - docs/videos/curio-b03
  - docs/videos/history-curiosity/topic-checks/B01.md
  - docs/videos/history-curiosity/topic-checks/B02.md
  - docs/videos/history-curiosity/topic-checks/B03.md
  - docs/videos/lexicon.json
---

# 奇聞檔案局品牌三集：山葉 B01、Shimano B02、Lonely Planet B03（研究、稿子、查核、盲評，付費前報價）

## Why

站主 2026-10-31 要三個黑猫研究院式的品牌題目，選了：山葉（做鋼琴的公司為什麼機車也叫山葉）、Shimano（不賣整車卻收全世界腳踏車的錢）、
Lonely Planet（BBC 買下又折價賣出的旅遊書）。站主說這類現在算奇聞檔案局系列，並說「開始做吧」。
所以照 `curio-episode` skill 做成 `curio-` slug（B 是暫定的「品牌」編號，`topics.json` 的六個主軸沒有這一類，要不要正式開 B 軸由站主決定）。

## Definition of done

- [ ] 三集各有 topic-check（逐列一手來源）、`brief.md`、`claims.md`、`video.json`（13 分鐘、開場五步、loops ≥ 8、插圖 ≥ 70%、配樂）
- [ ] 另一個代理獨立查核寫 `verify-1.md`；盲評兩位讀者沒有同否的題，存 `panel/`
- [ ] `node tools/video/cli.mjs lint --slug curio-b0N` 0 錯誤
- [ ] 旁白與插圖的張數與上限金額三集一次報給站主，核准後才跑付費步驟

## Steps

- [x] 研究：三集 topic-check（B01 70 列、B02 72 列、B03 76 列）
- [x] 撰稿：brief、claims、video.json（三集 lint 0／0；B01 13.2 分、B02 13.4 分、B03 13.3 分估計）
- [x] 獨立查核 verify-1.md（每集查核代理逐句，盲評改稿後再查改動句；B01 兩輪、B02 兩輪、B03 三輪）
- [x] 盲評 panel（B01 第 4 輪 13/13、B02 第 4 輪 13/13、B03 第 4 輪無同否；panel/ 存檔）
- [x] lint 0 錯誤、報價給站主（2026-10-31，等站主核准）
- [x] （站主核准後）tts → check-audio → keyframes → music → render/clips/assemble → captions → qa → review-push（三集成片都已送審；B03、B02 成片已核准）
- [ ] 站主勾語言（en／ja／ko）→ dub／i18n → 重新打包 → 站主上傳

## How to verify

`node tools/video/cli.mjs lint --slug curio-b01`（b02、b03 同）；`node tools/video/cli.mjs narrative --slug ...`。

## Notes

- 人物：山葉寅楠 1916 卒可畫；島野庄三郎 1958 卒未滿 70 年、不畫本人；Wheeler 夫婦在世、不畫。商標與可讀文字一律不畫。
- 容器有 2026-10-25 配對的影音權杖（`~/.mokaair/video-tool.json`），10-31 用 GET media/status 驗過有效。
- 2026-10-31 長度：skill 寫的「13 分鐘約 3,500 字（4.5 字／秒）」實際太長。lint 的估計是準的（H24 lint 12.2 分、實際旁白 12:10，約 3.5 字／秒）；
  第一版 B01 3,362 字 lint 估 16.1 分。三集改成正文約 2,700–2,800 字，lint 估 13.2–13.4 分。
- 2026-10-31 發音字典加 BBC（B B C）、Lonely、Shimano、TripAdvisor（null，待試聽）。B01 旁白沒有拉丁字母詞。
- 撰稿用的產生器在 session 暫存目錄，不進 repo；之後改稿直接改 video.json，再跑 `script --slug`。
- 2026-10-31 B01 盲評第 4 輪通過（兩位讀者 13/13）；`panel/reader-1.json`、`reader-2.json` 存檔，合併規則同主機（兩位都否才算否）。
  `narrative --answers` 要每題 evidence 以 `[tNNN]` 開頭，否則判 FAIL（不是內容問題）；合併腳本在 session 暫存，做法：取答「是」且有 id 的那份。
- 盲評前三輪三集都卡在同一處：開場預告超過兩個、講掉後面章節的結果。原因之一是 lint 要開場至少 3 個 loops setup（H24 NOTES 記過）；
  做法：利害句算一個 setup，加兩個停在結果之前的預告。其次是時間倒跳（另起一條持股或台灣的平行線）與片尾重述數字——片尾答案句只放第一次出現的數字或點名回呼。
- 人物：在世或過世未滿 70 年的人，旁白講到他時畫面不能有代表他的臉（職業＋性別也算指認）；只放手、物件或明顯無關的路人。三集查核共抓到約 40 張。
- 2026-10-31 報價（dry-run，免費）：插圖 B01 114 張 US$1.54（3 takes 上限 4.62）、B02 123 張 US$1.66（4.98）、B03 116 張 US$1.57（4.70）；
  旁白 Gemini Sulafat 3,010／3,027／3,160 字，各占免費額度 0.6%；配樂每集約 US$0.08–0.15（要先有旁白才報得出）。三集上限約 US$14.8。
  付費步驟一律等站主核准；工作目錄 `~/mokaair-work/videos/curio-b0N/`（容器回收即消失，narrative.json 已在其中）。
- 2026-11-01 站主在對話裡核准三集照報價上限（約 US$14.8）開始付費步驟（「好」）。branding --pull 已裝 v4-endscreen 素材包；三集 tts 同時跑。
- 2026-11-01 站主：「可以用紙白底」「跟AI科技的一樣」——三集加 `theme: "paper"`（同 AI 新聞片的紙底卡片）；關鍵句帶（keys）沒加，因為字幕燒錄在同一區。縮圖照舊深色 bold 版型。
- 2026-11-01 B03 第一次成片 qa 8/11：pace（片尾卡 18.2 秒）→ 答案句移到新 shot `close-answer-report`（逐字沿用 trust-lectern-2 的提示詞與運鏡，吃快取 0 張新圖）；旁白文字不變，只改所屬場景，panel 綁的旁白雜湊因時間碼變動，以第 6 輪同一份兩位讀者答案重新記錄（內容同一份稿）。links 的 NPR 是一時逾時（curl 200）。
- 2026-11-01 B01 插圖：第二輪改提示詞後仍有 war-ruin、war-table 沒過 → war-ruin 逐字沿用 prop-quake-b（吃快取），war-table 的一句併進下一景 war-table-b（同一張男孩矮飯桌木琴圖，10.9 秒，lint 一個 >10 秒警告）；panel 以第 4 輪同一份兩位讀者答案重新記錄（旁白文字不變）。
- 2026-11-01 B02 第一次成片 qa 8/11：pace（片尾卡 16.8 秒）→ 營收句併到 close-answer-c（11.2 秒警告）；links：fundinguniverse 500、堺市 408（容器 curl 也一樣，研究時讀得到，請站主用瀏覽器確認）；policy 符合立場 0.57（B03 也曾 0.59），報給站主。
- 2026-11-01 B01 第一次成片 qa 8/11：pace（片尾卡 17.9 秒）→ 答案句移到新 shot close-answer（逐字沿用 open-you 的圖，首尾呼應）；links：yamaha.com 15 頁對程式回 403（研究時讀得到）；policy 符合立場 0.53——brief.md 的「站主觀點」一節混了改稿紀錄，已移到「## 改稿紀錄」。B02 第二次成片 9/11（fundinguniverse 500、policy 0.59）。
- 2026-11-01 站主貼了 S31（楊貴妃的荔枝）11/11 的品管。對照後：S31 的「站主觀點」寫得具體（一個問題、主角、不判什麼、結論只講一次、畫面守則），我們三集只有兩行 → 照 S31 結構重寫三集的站主觀點；重跑 qa：B03 符合立場 0.67（過）、B02 0.63→0.58（同一份輸入兩次差 0.05，Jev 有浮動）。連結：yamaha.com、NPR 用瀏覽器 UA 回 200，只擋 qa 的編輯 UA；B02 的 FundingUniverse 換成同一篇公司史的 Encyclopedia.com（有同一句引文），links 過。堺市頁 408 仍待站主用瀏覽器確認。
- 2026-11-01 B01 成片 qa 10/11（符合立場 0.68；只剩 yamaha.com 15 頁對 qa 編輯 UA 回 403，瀏覽器 UA 200），成片已送審。花費：B01 US$3.03、B02 US$3.12、B03 US$2.79，合計約 US$8.9。工作目錄在容器 `~/mokaair-work/videos/curio-b0N/`，容器回收前要先打包或備份。
- 2026-11-02 B01 成片站主核准；三集成片都已核准。剩語言（en／ja／ko）由站主決定，之後 package。
- 2026-11-02 站主：「八語全加」。i18n-sheet 三集八語；六個翻譯代理（每集 en/ja/ko/th、es/pt/id/vi 各一）填工作表，之後另派審稿代理、i18n-merge、dub 逐語。標題不加系列後綴（同 S31 的譯名）。
- 2026-11-02 三集八語譯文全部合併（翻譯代理 6 個＋獨立審稿 6 個；審稿共修約 100 處，含多處出處遺失、日韓「車」誤讀為汽車、葡文校名錯成東京大學）。lint 對手機標題寬度（36 全形）與泰文等說明 5,000 位元組的警告都已改完。下一步：逐語 dub。
- 2026-11-02 B01 配音 en／ja／ko／es 完成（聽檢標記 10／27／31／11 句）。逐句看過：多是轉寫把罕見詞「修正」成常見詞（fork handles→four candles、音叉→王さん、功学社→工学者、1987→1887），照 S31 定的規則接受、站主在語言關卡聽。要站主特別聽的：t002 的年份（ja 聽成 2023、ko 聽成 2015，en／es 正確）、en t017 的「It's said」（聽成 Instead，是傳說標記）、ja t013 山葉寅楠的念法。本機沒有 Whisper 第二意見（磁碟只剩約 1.3 GB，裝不下模型）。同一集一次只能跑一個 dub（專案鎖），多語要排隊。
- 2026-11-02 B01 八語配音完成（縮短約 10 句；en、vi、id 有語音念出「thought」的句子，重錄後沒了——之後的配音迴圈在刪逐句音檔前先自動重錄這種句子）。captions 九語、package 4/4、qa 10/11（只剩 yamaha.com 對 qa UA 回 403）。`review-push --gate publish` 與 `--gate languages` 已送出（pending），站主在 /admin/videos 決定。注意：`package` 對一般影片是複製 final.mp4 與配音進 upload/（約 450 MB），磁碟緊時要把它們改成硬連結（cmp 確認相同再 ln -f）。
  要站主在語言關卡特別聽：t002 的「2025 年」（ja 聽成 2023、ko 2015、vi 2020、重錄的 en 也聽成 2020——可能是聲音真的念含糊）、en t017 的 It's said、ja t013 山葉寅楠。B02 ja t004 的 1921（聽成 1920）、ko t121 的 2024（聽成 2004）。
- 2026-11-02 B02 八語配音完成（縮短約 12 句，兩句異常慢的錄音改字重錄；en、pt、id、vi 各一句念出「thought」已重錄）。qa 11/11、package 4/4，`--gate publish` 與 `--gate languages` 已送出（pending）。B03 八語配音開始（en ja ko es 先跑）。
- 2026-11-03 B03 八語完成（en ja ko es pt id vi th），captions 九語、package 4/4（上傳包複本已改回硬連結）、qa 10/11，
  `review-push --gate publish` 與 `--gate languages` 已送審（pending）。es 縮短 t106、t107 以符時窗。
  - qa 唯一沒過：links。NPR 那條 curl 重試 200（當時逾時）；`https://tonywheeler.com.au/about-tony` 在這個容器的 HTTPS 連線被對方重置，
    請站主用瀏覽器確認。
  - 站主試聽清單（B03）：ja t049「9月」聽成 10 月、ja t022「聖書」聽成「彗星」、ko t031「8810만」聽成 8110만、ko t037「수신료」聽成「10년」、
    ko t089「공유 숙박」聽成「도쿄 숙박」；th t017、t024 Gemini 安全過濾拒絕轉寫，沒有機器聽寫結果。
  - pt t102 漏出 thought，已自動重錄、重聽無漏字。th 第一次配音時磁碟寫滿導致聽寫中斷、逐句檔被清，整語重配一次（免費額度）。
- 2026-11-03 六張備份票（#1997–#2002）部署後：B03 的上架確認重送，同一筆 pending 審核多帶 291 個完整層級檔（286 張分鏡等）。
  B01、B02 的上架確認站主已核准，網站不再收新檔；要補完整層級得送一筆新的上架確認、站主重新核准（待站主決定）。
  worker 已列出 B01、B02 的 review_package（含語言批次），下一輪會抓回主機並備份上傳包。
