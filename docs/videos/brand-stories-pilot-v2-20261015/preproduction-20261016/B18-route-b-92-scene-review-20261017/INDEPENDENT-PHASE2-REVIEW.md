# B18 Route B Phase 2：獨立覆核收據

**結論：HOLD；P1/P2 未清零，不得作為正式 worker 章稿、verifier 證據或付費製片許可。** 本收據記錄獨立審查代理 `/root/b18_script_scene_alignment/b18_phase2_independent_review` 對凍結候選的唯讀結論；此檔由候選製作者依審查代理的原始回覆記錄，審查代理沒有修改候選。若候選任何 byte 改變，本收據失效。

受審候選：`../B18-route-b-92-scene-candidate-20261017/`。

| 凍結物 | SHA-256 |
| --- | --- |
| 候選 `sha256.json` | `0e8613d06888d285f34b40cb2be9af54372c771676592e3dff0a07491f41ec25` |
| 第三版受審全文 `../B18-spoken-source-cadence-candidate-20261017/B18.md` | `7b2865668d8cdd21a87cd813b015ebc0088f3728712181063768d9323200e8c1` |
| 候選 `build.mjs`（由上述 manifest 釘住） | `e1e4281ee2ae12bc9ccfb66d4d79258af44270ecaee681d9b0ec3f15b516866f` |

獨立審查代理在凍結快照上重跑以下唯讀指令，`build.mjs --check` 得到 `PASS_OFFLINE_92_SCENE_DRAFT_HOLD`；`verify-worker.mjs` 得到 writer rejection。

```powershell
node docs/videos/brand-stories-pilot-v2-20261015/preproduction-20261016/B18-route-b-92-scene-candidate-20261017/build.mjs --check
node docs/videos/brand-stories-pilot-v2-20261015/preproduction-20261016/B18-route-b-92-scene-candidate-20261017/verify-worker.mjs
```

## 覆核結果

機械覆蓋：25 段口播去空白後逐字同序，92 鏡、73 張插畫／19 張 `title` 卡，插畫比例 79.35%；65 個既有 claim ID 全保留且 65/65 為 `UNCHECKED`。候選生成檢查通過只證明離線對位檔可重建，不代表逐鏡可採用。候選 `paragraph-coverage.json` 實際有兩組相鄰的兩張卡（`turn-s063/s068`、`now-s093/s095`），最長連續卡數是 **2**，仍低於 3；審查代理早期口頭提到 1，這裡依凍結檔讀回更正。

### P1：正式流程與事實對位

1. `tools/video/automation/story.mjs` 的 `readChapterAnswer` 在 `origin-s010`（origin 第三鏡）回覆：`scenes[2] is a "title": a story's scene is a shot (the last chapter ends with an outro card)`。其餘 18 張 `title` 也不符同一 writer contract；`now-s103` 仍是 `shot`，未設計片尾 `outro`。正式 `PILOT_SCRIPT_REFERENCES` 仍釘舊全文 `5326bd…`，不是本候選第三版 `7b2865…`。現用 B18 腳本不因此改動。
2. Hook 三條 loop 的萬博與後場問題共用 setup line `714fe729`；`composeStory` 以 setup 去重，離線只剩兩條。更重要的是 `readChapterAnswer(hook)` 會移除不在 hook 的跨章 payoff，而本候選 idea／engine／turn 的 loops 皆空；正式 writer roundtrip 後三條跨章回收全部消失。需給三問各自 line ID，並在各回收章另帶原 setup 與本章 payoff，再測完整 roundtrip。
3. 有九筆 claim anchor 跨鏡：`i3,i4,i8,e2,e6,e8,t3,t11,t12`。尤其 t3 法院 1967 年展店主張綁 `turn-s068`，仙台直營與東京連鎖動作卻在 `turn-s068b`；不能把 65 筆宣稱為已完成逐景查核。1970 年萬博、1967 年展店也不能在同一張「約 240 家 · 1967 年展店」字卡上暗示 1967 年即有 240 家。

### P2：視畫、節拍與片長

1. 至少四組相鄰鏡頭近乎同構：`origin-s020/s020b`、`engine-s046/s046b`、`turn-s068b/s065`、`turn-s072/s072b`。`origin-s016` 旁白是逐盤送餐，畫面卻是員工帶圍裙離職；`hook-s005` 開頭仍在說試作盤掉，畫面已跳萬博；`turn-s086` 的 1986 ㄇ字型口播配的是 1980 旁通工作台。七鏡新增了槽位，尚未全形成新的視覺狀態。
2. 七鏡超過 42 個可見字，九個 `shot` 少於 25 個可見字；turn 章 917 字／25 鏡，高於現行 worker 10 分鐘預算的 463 字／15 鏡。這是分配風險，實際 9–11 分鐘及每鏡 5–8 秒須靠 TTS、剪輯時間軸驗證。增加鏡數不能當成增加口播時間。

### 來源抽核界線

- [日本法院判決 PDF](https://www.courts.go.jp/assets/hanrei/hanrei-pdf-13913.pdf) P8 L476–495：1967 年獲授權使用餐台與元祿標示的**訴外公司**在仙台直營、東京連鎖展店；P10 L574–578：僅第 579776 號特定實用新案在 1972 年期滿。不能寫成原告自己開兩家直營，也不能推所有權利同時到期。
- [發明協會沿革](https://koueki.jiii.or.jp/innovation100/innovation_detail.php?eid=00026&age=high-growth&page=keii)同頁沿革支持後場直線送盤與後來部分店家以盤色／裝飾區分價位；沒有把這做法推給所有店家。
- [日本機械學會第 112 號機械遺產](https://www.jsme.or.jp/kikaiisan/heritage_112_jp.html)區分 1985 年製、2021 認定時堺東店仍在用的輸送機，以及另存早期板片；不是 1958 首店同一原機。

這些抽核未發現核心史實與來源相反，**不是正式 verifier PASS**。`t18` 在候選章稿是 `turn-s088/source:2/fact:null/UNCHECKED` 且有發明協會非口播字卡；但該卡被正式 writer 拒收。正式章稿先存 `fact:null`、verifier 後讀回 source 2／fact null／可見來源卡的程序均未發生。

**後續：** 保留本候選的 P1/P2 證據；若要另做 92 鏡 shot-only 版，仍需先解決 t18 等效、可驗證的非口播來源顯示，或經獨立審稿新增發明協會口播歸屬。不能用 AI 圖中文字或僅一個無法在畫面讀到的來源欄位冒充已滿足 Row10b。受審全文、舊 active 章稿及正式機都沒有在本次審查中改動。
