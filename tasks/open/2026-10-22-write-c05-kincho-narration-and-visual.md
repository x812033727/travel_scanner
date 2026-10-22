---
id: 2026-10-22-write-c05-kincho-narration-and-visual
title: Write C05 Kincho narration and visual plan
status: review
priority: P2
area: docs
owner: codex-gpt6-c05-approvals-cost
claimed_at: 2026-10-22T05:28:16Z
created_at: 2026-10-22T03:39:36Z
completed_at:
branch: codex/brand-story-kincho-c05-script
depends_on: []
scope:
  - docs/videos/story-everyday-kincho-c05/script.md
  - docs/videos/story-everyday-kincho-c05/visual-plan.md
  - docs/videos/story-everyday-kincho-c05/production-quote.md
  - docs/videos/story-everyday-kincho-c05/reviews/owner-script-approval.md
  - docs/videos/story-everyday-kincho-c05/reviews/line-review.md
  - docs/videos/story-everyday-kincho-c05/reviews/narrative-reader-1.md
  - docs/videos/story-everyday-kincho-c05/reviews/narrative-reader-2.md
---

# Write C05 Kincho narration and visual plan

## Why

站主已採用 C05 金鳥螺旋蚊香的企劃方向，但 Treatment 不是可錄音的逐句稿。要把 1890 直條、1895 試作、1900 公司記載的專利申請、1902 上市、後來雙卷運送與現行產品串成一條可查核的故事，並在任何付費製作前交站主審劇本與畫面。

## Definition of done

- [x] 依採用的 Treatment 寫六章旁白（第二輪修訂現為 79 句）、每句固定 ID，附逐句來源對照與至少八個可回收的鉤子；來源不足就縮短，不用重述灌長。
- [x] 完成逐鏡畫面計畫，遵守奇聞檔案局的 MiniMax image-01／cute-mystery、插圖時間至少七成、卡片連續最多三張、片頭片尾及 CC 規則，不產生媒體。插圖時間占比仍須實測後核准。
- [x] 修訂後稿件由不同代理完成 79／79 逐句來源及逐鏡查核，另有兩位未參與修訂的讀者各自盲讀；三份收據均綁最終新版雜湊。舊稿收據只作歷史。
- [x] 本修訂稿通過已列非付費檢查，草稿 PR 已交站主；站主已核准固定雜湊的劇本與逐鏡方向。TTS 純旁白及插圖畫面時間仍待實測。

## Steps

- [x] 由 Treatment PR #1672 的核准版本開立獨立工作樹及 `codex/brand-story-kincho-c05-script`；查無另一人持有逐字稿路徑。
- [x] 讀規則及來源，寫六章旁白、逐句來源和視覺節拍。
- [x] 獨立逐句查核、兩位嚴格盲讀，按首輪具體意見修訂；把本輪未解的節奏意見留下，不冒稱定稿。
- [x] 跑本次適用的檢查、提交並推送草稿 PR #1675，記清下一道站主審核關卡。
- [x] 2026-10-22 在同一工作樹修訂 88 句正文和逐句視覺節拍；約 1919／1922 年的商品時數、1940／約 1957 年工法與現行配方分期敘述，刪除舊稿重複揭曉；未製作媒體。
- [x] 在 Treatment／矩陣 F08／F09 窄改後，按兩位真正盲讀的 REVISE 意見把上一版 88 句收束為 79 句：雙卷、慢燃各緊接問題回答，1940→約 1955→1957→現行順序，逐鏡一對一重排；未改舊收據。
- [x] 重新做本版逐句來源查核與兩份真正盲讀；新版 Treatment／來源矩陣已獨立 PASS，站主窄幅重綁另待回覆。
- [x] 站主核准的劇本／逐鏡與非付費整支估價已交給後續獨立試片票；本票不持有 `video.json`、TTS 或圖片階段。

## How to verify

核對 Treatment 與來源矩陣 SHA-256、逐句來源 ID、`script.md` 與 `visual-plan.md` 雜湊，以及獨立收據；跑 `npm run check:tasks`、`git diff --check` 和適用的影片 lint／`npm run test:docs-videos`。任何 lint 通過不等於站主劇本核准或已生成媒體。

## Notes

歷史上企劃與來源矩陣曾以雜湊 `BBA52D1D55CE38560B8C7581EFCC7E739849468882C4FF91146F29F139A93C90`、`0939FD2ACEBF84FA8F84559F71C056BD8784E65BD4A875A03687F53B872CA1EA` 採用；**本輪已非這兩個檔案版本**，新雜湊與站主窄幅重綁狀態見末尾新紀錄。這張票僅占逐字稿、畫面計畫及其審查收據的確切路徑，不改 Treatment／來源矩陣，也不動 C03、C04。專利原件、1889 年優先權與妻子構想的獨立同時期證據仍缺；旁白要按來源歸屬表述。

2026-10-22 草稿 PR #1675：88 句、65 個畫面狀態（50 shot／15 card）；每句恰有一個畫面對應，連續卡片最多 2 張。`script.md` SHA-256 `7D07A7A12478E4956B1DA110819F9C30514BA0C52DA007868F8644A401D78980`；`visual-plan.md` SHA-256 `7A7068BF5E38E0784EBA4A7DEA93A36FC0A3B988AC64F5B3750EA6FABBD117C3`。插圖 76.9% 只是狀態數，**不能**替代成片畫面時間至少 70% 的檢查。全 88 句為 1,548 字元；扣除開場後，第 02–06 章正文 80 句只有 **1,402 字元**，照專案每分鐘約 250 字元的規劃值僅約 **5 分 36 秒**，離正文純語音 8 分鐘約差 598 字元；實際時長仍只能由 TTS 驗證。此稿 **不具付費製作核准資格**。不靠停頓、重複或旁支史料補時；下一步先評估有來源支撐的補強，仍不足就由站主決定短片或換題，之後重新估價與審核。

獨立查核者已對此稿 88 句逐句 PASS，並查畫面物件；兩位嚴格盲讀者都認為主線與回收可追，但指出 T05–T08 揭曉重複、T12 提問到 N09–N11 答案間隔、N14–N16 收尾太像摘要／制式邀請，與 E18–E19 的工法年代轉場可再修。這些是下一版劇本問題，**不是**可付費的通過票。初輪曾有讀者誤看來源欄，另一份超讀鉤子表，均未列為兩份正式嚴格盲讀收據。來源矩陣 F08 尚有「兩條同時押出」的勘誤需求，應回 Treatment PR #1672 受控修正並重綁採用雜湊；本稿只採原件較窄的說法。

`npm run check:tasks` 通過，稿件 ID／畫面映射與連續卡片機械檢查通過，`git diff --check` 通過。`npm run test:docs-videos` 為 235/236 PASS；唯一失敗是 `docs/videos/imported-long-languages/runner.test.mjs:679` 的 Windows 子行程 3221226505／無 stderr，與本次純文件編輯無關，且在 Treatment 工作樹重現。沒有生成圖片、音訊、影片，也沒有任何付費請求。PR 保持草稿及 `no-auto-merge`；票留在 `review`，未併入不得 `done`。

2026-10-22 **未提交的 C05 修訂稿**：`script.md` 由 `7D07A7A12478E4956B1DA110819F9C30514BA0C52DA007868F8644A401D78980` 改為 `5D6189173606555E1F9D8B1BC4CC2A481DEF1B4FEEBD5F67A03ECD2E604A511F`；`visual-plan.md` 由 `7A7068BF5E38E0784EBA4A7DEA93A36FC0A3B988AC64F5B3750EA6FABBD117C3` 改為 `45F560D94F4ED85F74FA5DD6829620B957D404A93745D9955E116FB4D2EBBB81`。新版正文第 2–6 章仍是 80 句，**2,128 漢字／2,381 字元**；照每分鐘約 250 字元的粗估約 9 分 31 秒，實際純旁白時長仍須 TTS 驗證。88 句各對應一個非付費視覺節拍，共 70 shot／18 card、最長連續 2 card；26 句超過 33 字元，實際定時後可能需要增鏡，現有 79.5% 僅為節拍數占比，不是插圖時間驗證。舊版 line-review 和兩份 blind-reader 收據**不得**算新版 PASS，沒有改那些收據或 `video.json`，也沒有 commit／push／更新 PR／付費媒體。

新版補強來源是可讀的金鳥官方 HTML：[資料館](https://www.kincho.co.jp/factory/shiryou/index.html)的約 1919 年 58 公分／六小時、約 1922 年另一手卷款十二小時，以及[工廠詳細說明](https://www.kincho.co.jp/factory/listen/detail.html)的約 1955 年合成成分、約 1957 年左旋、現行製法與綠色設計。1900 年仍只按公司年表稱**專利申請**；1902 年完整量產工序與雙卷首用年份仍未查到。Treatment／來源矩陣 F08 的「兩條同時押出」已被獨立審計指出超過原頁，須在其受控路徑窄改並以新 SHA 重綁，這張票無權改它；本稿只說工人取兩根**已擠出**的條手卷。這份修訂稿待重新逐句獨立查核、兩位盲讀、站主審核與定時驗證；目前仍 HOLD。

本修訂稿本機檢查：88 個旁白 ID 與 88 個視覺節拍一對一、70 shot／18 card、最長連續 2 card、26 句超過 33 字元的機械盤點通過；`git diff --check` 通過，`npm run check:tasks` exit 0（其他票有既有長期 claim／scope 警告）。`npm run test:docs-videos` 為 **235/236 PASS、exit 1**；唯一失敗仍在未修改的 `docs/videos/imported-long-languages/runner.test.mjs:679`，`package-runtime.mjs` Windows 子行程退出 `3221226505`、stdout/stderr 空白，與舊稿同一已知失敗。這些檢查不等於新版內容查核或站主核准。

2026-10-22 補充唯讀來源盤點：金鳥官方 [資料館](https://www.kincho.co.jp/factory/shiryou/index.html) 的可讀 HTML 把約 1919 年保存商品記為 58 公分／6 小時，約 1922 年另款手卷商品記為 12 小時；兩者不能倒推 1895 年試作的燃燒時數。[戰前年表](https://www.kincho.co.jp/kaisha/ayumi/ayumi03.html)、[技術遺產頁](https://www.kincho.co.jp/new/tech/) 與 [工廠說明](https://www.kincho.co.jp/factory/listen/detail.html) 可補約 1940 年自動打型、約 1957 年工法／左旋區別的後續轉折，但不表示 1940 年已淘汰手卷。這些資料足夠做一輪精簡改稿，未證明能自然補滿八分鐘；改稿需重新逐句查核與盲讀，現在維持 HOLD。

2026-10-22 **第二輪非付費修訂、仍 HOLD**：兩位真正盲讀對上一版 `script.md` SHA-256 `5D6189173606555E1F9D8B1BC4CC2A481DEF1B4FEEBD5F67A03ECD2E604A511F` 均判 REVISE，指出供料旁支、運損／慢燃問答太遠、1940／1955／1957／現行跳時與結尾機制回收不足；其意見不能當本版 PASS。本輪 `script.md` 變為 `F5018A8D7DE2E74FC5A441D6F8D26E98EBDBFE8A68598411EDD94170F98F978A`，`visual-plan.md` 由 `45F560D94F4ED85F74FA5DD6829620B957D404A93745D9955E116FB4D2EBBB81` 變為 `06DE963E1CD0389F051BDED036FEE25B042273F7D08FED103BDE48885F2CF992`。正文第 2–6 章 71 句，**1,984 漢字／2,209 字元**；依每分鐘約 250 字元只作規劃，約 8 分 50 秒，仍須 TTS 實測。79 句逐鏡一對一，63 shot／16 card、最長連續 2 card，23 句超過 33 字元，插圖節拍占 79.7% 不是畫面時間。新 Treatment／來源矩陣 SHA-256 現已在工作樹讀回為 `4A1C596B9A8A6E9278C99205E9EE381E4FD5AF4EAD5CDC6C448A852D5E7FC8D0`／`A7EB8401ABCC5715C46352187C0EFE100FA3AA47E22A020A1FC16FFD55504516`，**站主尚待窄幅重綁新版本**。舊 review 收據與 video.json 均未改；未 commit、push、更新 PR 或付費生成。下一步是獨立逐句查核、兩份新版盲讀與定時驗證。

本輪機械檢查：79 個旁白 ID 與逐鏡 ID 逐章連號且一對一、每句一個句末標點、所有 F 來源 ID 與鉤子回收引用均存在；63 shot／16 card、連續卡片最多 2 張。`git diff --check` 與 `npm run check:tasks` 均 exit 0；後者只報其他票既有的長期認領／scope 警告。未重跑 `npm run test:docs-videos`；前述 235/236 結果綁舊版，不當成本版測試通過。

2026-10-22 **最終逐句／逐鏡審查版，待站主決定**：再窄改 E16 不暗示兩款同時販售、V001 讓直條與 H01 一樣正在燃燒、V064 畫少量氧氣仍能進入。`script.md` SHA-256 `D49FE268109DDCE4BF6E44A3E75831467735DEC23E58D11BCC92065EE533288D`；`visual-plan.md` SHA-256 `7908331CE21FE658321D8117D7429ECCA3C1F48C3D558E57B0885E5F26138CAE`。獨立代理對 79／79 句與 79／79 個畫面意圖逐項 PASS，收據在 `reviews/line-review.md`；兩名全新盲讀者各自只讀 ID＋旁白後 PASS，收據在 `reviews/narrative-reader-1.md` 和 `-2.md`，均綁上述 script SHA。正文第 2–6 章 71 句／2,209 字元，按 250 字元／分鐘**僅粗估約 8 分 50 秒**；63 shot／16 card、最長連續兩卡，79.7% 是節拍數，不是畫面時間。新版 Treatment／矩陣雜湊仍為 `4A1C596B9A8A6E9278C99205E9EE381E4FD5AF4EAD5CDC6C448A852D5E7FC8D0`／`A7EB8401ABCC5715C46352187C0EFE100FA3AA47E22A020A1FC16FFD55504516`，站主窄幅企劃重綁、劇本核准及本集付費額度均未取得；不做 TTS／圖／音樂，也未匯入、上傳或發布。

本版本機檢查：`npm run check:tasks` exit 0；`git diff --check` 無空白錯誤。`npm run test:docs-videos` 為 **235／236 通過、exit 1**，唯一失敗仍是未修改的 `docs/videos/imported-long-languages/runner.test.mjs:679`，Windows 子行程 `package-runtime.mjs` 退出 `3221226505`、沒有 stdout/stderr；這不是本集內容檢查 PASS。`tools/repo-hygiene.test.mjs` 在本分支舊版基底上找到上游 Treatment 票第 47 行的本機使用者路徑；該路徑已於 Treatment PR #1672 後續提交移除，須在本分支重接最新上游後重跑。這些測試結果不代替時長、圖片時間或站主決定。

2026-10-22：站主在修訂版企劃另行採用後，回覆 PR #1675「核准目前劇本與逐鏡方向（建議）」。新收據 `reviews/owner-script-approval.md` 精確綁定 script `D49FE268109DDCE4BF6E44A3E75831467735DEC23E58D11BCC92065EE533288D`、visual `7908331CE21FE658321D8117D7429ECCA3C1F48C3D558E57B0885E5F26138CAE`，並指出上游兩份核准雜湊；此決定不含付費。`production-quote.md` 非付費提出最多 86 張（63 基本＋23 拆鏡預留）、每張最多三次、79 句旁白與一首配樂、整支 US$25 停線，仍待 C05 專屬核准。重新只計旁白欄，正文 71 句為約 1,993 字元，不是舊筆記 2,209 字元；250 字元／分鐘僅粗估 7:58，TTS 尚未合成，未能宣稱達 480 秒。未買圖；片頭片尾、提示詞、定時與工具乾跑待後續非付費完成。

2026-10-22 試片票交接：站主已另行核准 C05 最多 86 張圖、每張最多三次、79 句旁白與一首配樂、整支 US$25 停線。此核准需要獨立雜湊綁定收據與試片票；`video.json` 從本劇本票 scope 移除，後續製作不得沿用本票的劇本核准冒充付費決定。PR #1675 仍保持草稿及 no-auto-merge；本票留 review 到合併。
