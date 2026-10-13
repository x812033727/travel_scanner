# 首集前置收尾：尺寸用途、逐鏡參照與連戲（2026-10-09）

本次交付以 **v4 工作提案**為準，補齊 455 鏡的參照分派與首尾狀態。這是可審閱的製作交接；候選圖、正常 look 選用、付費首格／動畫、站主接受仍是不同狀態。沒有寫正式來源、choice、approval 或 plan lock，沒有付費請求。

- [455 鏡完整資料](finalization-20261009.json)：每鏡來源 pointer、prompt SHA、角色 base/head/detail/mouth 用途、場景／道具 logical key、風險、首尾狀態、原素材重用。
- [離線 builder](build-finalization-20261009.mjs)：核對 12 份來源 SHA、455 個唯一鏡號、27 張畫像實檔 hash／PNG 尺寸、所有已分派候選的實檔 hash；缺非預期 reference 即失敗。
- [v4 差异與驗證](../episode-plan/finalization-v4-verification.json)、[v4 補訂說明](../episode-plan/finalization-v4.md)。既有 v3／v3.1 的全程／定點觀看證據保持原樣。

## 版本與優先序

新工作檔為 `<VIDEO_WORKDIR>/ou-de-jianghu-e001/plan/preflight-20261009-v4/video.json`，SHA-256 `cb341b457f28e5139cff6f0528722d2a0facebf8cfea90423aec572ed71ebd17`。保留父版 v3 SHA `7f7676d1ce39a6f9dbbdc4cacc5bc8cb39b9979e66e4a906213d2ea4235014df`；12 份正典來源逐份 SHA 與目前實檔核對結果都在 JSON。

v4 只修 a04-s038 貝錢落在包三千「右掌」，以及 a03-s086 無冠鏡誤帶的通用 complete crown 片語。455 鏡／4 張原稿字卡、台詞、鏡長、motion、camera、source reuse、風險與預算數值均與 v3 相同。總估時仍為 23:23.533，未產生新的全長實播主張。

執行優先序是 v4 逐鏡 prompt／狀態 → v3 未變的台詞／時間／人工風險 → 道具索引 → 靜態參照圖。`shot-props.json` 保留原始稿索引，不能把已改成結果插鏡的接觸動作重新塞回去。送茶鏡號則原稿與 v3/v4 本就一致：s017 沈咳嗽、s018 送茶、s019 左托右敲、s022 右手開門；錯的是舊場景包的引用索引。

## 原生尺寸的真實用途

初版 27 張實檔為：9 頭像 1254×1254；沈／無霜半身 1003×1568，其他 7 半身 1122×1402；9 全身 1024×1536。原 1600／2048 長邊及半身 4:5、全身 2:3 是 `production-list.md` 的**編輯建議**，不是 import 的硬門檻。原本 18 張 `native_below_target` 紀錄保留；最新修版尺寸另按實檔記錄，不能把舊不足標記偷偷改成已達標。

`look.mjs` 實際匯入要求為每邊 512–8192、總像素不超過 16 Mi、32 MiB 以內的有效非交錯 8-bit RGB/RGBA PNG，並檢查 CRC／IDAT。先前 27 張已直接通過 `inspectLookPng`；本 builder 再讀實檔 header 與 hash。這足以支持「原生身分／服裝參照候選」的用途提案，不等於正式採用或動畫品質通過。此次不硬放大，也不為達長邊數字重生而引入臉部漂移。

| 資產 | 使用方式 | 限制 |
|---|---|---|
| 正面頭像 | 臉部、眼色、髮線與臉上記號的身分比對 | 不能強迫側背鏡轉正面 |
| 半身／全身 | 生成正式首格前的身分、衣裝、身形參照 | 原生尺寸保留；不是已交付的 2K 首格 |
| construction-details | 冠鏈、衣扣、袖口、手與道具結構 | 當鏡無冠、持物或破損狀態優先 |
| 8 人口型板 | 會說話且臉可見時的靜態嘴形畫法 | 不是精確 phoneme／聲音同步；部分冠帽裁切，不作完整頭部母圖；殷無聲不分配 |
| 場景／道具板 | 軸線、空間座標、形狀、材質與數量 | 不把母圖上的預設燭火或道具狀態帶入較晚鏡頭 |

## 目前產線能力與真正接線

內建 imagegen 本次可用介面沒有 native size／quality 強制欄位，prompt 寫 2K 不代表交付 2K。`keyframes.mjs` 目前 drama 的 `sizeFor=null`，走 provider 的 1K 預設；只有 illustrated／explainer 明確要求 2K。`stages.mjs` 的 IMAGE_SIZE 常數是快取／估算標籤，不能拿來證明 PNG 實測大小。最終首格 2K 可保留為後續交付目標，但必須選定／實作支援的路線，並讀回原生像素。

正常 keyframes 先要求已核准 look，從每個角色 chosen sheet 取一張 base；參照上限為 4。此文件雖列 base／head／detail／mouth 的分工，**沒有自動把這些全部送模型**。後續執行者需按鏡位挑最小必要集合、綁定最新候選 SHA、記錄真實 request/readback，再走正常 judge／choice／series-store。

H3 provider 的 `first_frame`／`last_frame` I2V 與 `reference_images` 互斥。因此 1536 長邊全身圖是「先生成 I2V 首格」時的角色參照用途提案；不能宣稱可在首格之外，再附一組角色圖給同一 H3 I2V 請求。相關原碼位置保存在 JSON 的 `capabilities.proof_sources`。

## 逐鏡分派的讀法

455 行都具備 v4 pointer／prompt SHA、場景 reference、視覺做法及風險。角色明示名單與從可見身體／手部文字補出的角色分開記；後者是規劃推論，實際首格構圖仍需逐鏡檢視。全身基底維持衣裝身分；正面頭像只在臉可見時用，手／背面插鏡跳過；construction-details 只看相關局部。口型只分配給當鏡有可見臉的發言者，畫外台詞不強迫加入嘴部圖。所有候選 `final_binding=null`、`owner_accepted=false`、`runtime_integrated=false`。

JSON 中 `reference_catalog` 保存本次已核實的候選 key／媒體 SHA 快照，讀取新的 [畫像收據](../episode1-portraits/finalized-views-receipt.json)與[動畫參照收據](../animation-reference/finalized-media-receipt.json)，包含最新修扇版沈全身／半身及無霜嘴形 v2；場景讀取現行 28 張 latest。主控整合時仍須依 latest receipt 解決最新版本；不能因有 hash 就改成 owner accepted。5 個 cut/reuse 鏡標記取既有素材，不另購動畫。這是完整 reference metadata 覆蓋，並非 455 張首格已畫好或逐格視覺 QA。

白扇拓撲唯一依據是 **shen-guihe-construction-details-v3 與 personal-prop-states-v3**，白玉骨／白紙、無扇穗／鏈／小珠掛件。概念、人物姿態、配色與群像可能還有微小手邊短線或小珠，只供臉、服裝、姿態、配色；沒有宣稱每張圖的扇部像素全面一致。每個沈可見／身體局部被命名或明示扇的鏡，JSON 都以條件式用途分配兩母圖並記 `fan_reference_policy`。只有扇可見才用，道具板不替當鏡新增扇、改手或增加動作。

三張明確限制候選為 `shen-guihe-concept-v5`、`shen-guihe-right-profile-v3`、`shen-guihe-left-three-quarter-v3`；只取身分／服裝，不取手邊短線／小珠為道具設計。其餘修版也不取代兩張唯一扇部 master。latest receipt 完成後重建結果為 193 鏡套用上述條件式分派，兩母圖皆在每個相關 row 的 detail／prop refs 中，並由 builder 逐行 assert。

## 首尾連戲與導演編輯決定

以下沒有增加劇情或動作；未由正典指定的具體落點，以「提案」標示。JSON 的 `continuity_decisions` 保存更細的 before／after 及對應鏡號。

| 範圍 | 要固定的首尾狀態 |
|---|---|
| 四箭鉗 a01-s004→005 | 三長一短共四箭，鉗夾箭桿；下一鏡已尖端向下入同一囊，鉗口在囊口上方打開、不接觸。平行束與短箭靠觀眾側是辨識提案，不加箭。 |
| 黑風 a01-s007→008／a05-s078 | 弓囊已脫離往畫左；聶右手已握一段半弦，再收拳。s078 重用 s008，不另畫第二段。 |
| 掌冠 a02-s035→037 | 寂聞右掌只從實心冠脊上 1 cm 下落接觸並停，五指同向；不碰冠鏈。下一鏡髮從遮後頸到露唯一月痕。 |
| 接匣 a02-s056→058 | 056 右閉扇敲左掌；057 已是沈左托匣底、無霜空手收袖的結果；058 只抬原有 10 cm。匣直立貼左胸是穩定持物提案，不新增雙手交接動畫。 |
| 無冠 a03-s085→087 | 冠已立桌、链收桌，無霜無冠散髮；再讀右手金線。v4 086 已刪矛盾冠前綴。 |
| 船／跳板 a04-s029→039 | 岸左船右，包在跳板低處畫左、洛在欄上高處畫右；037 右掌、038 右掌已有單枚貝錢、039 唇下不咬。不要塞銅錢。 |
| 送茶／門 a05-s018→030 | 018 雙托、019 左托右敲、022 右手開門；023 仍持盤且燭滅，026 才放桌，030 才出現翻盤結果。落在桌南靠門側是一致落點提案，地上只有一壺一杯與茶。 |
| 冷場 a05-s031／035／042 | 全部取乾淨 `chess-guestroom-master-v4` 的幾何／紙窗，另外指定冷光、局部霜、滅燭、翻盤後地面；暖廊光保留到 073 殷關門才切除。 |
| 開窗／拔釘 a05-s074→081 | 窗開一掌寬；同一根外側木條向室內翻，只有一釘固定半弦；077 已拔出的結果：左弦右釘、孔可見。081 延續左弦右釘，不加接合動作。 |
| 末白 a04-s090→a05-s091 | 長老右指懸一白、前臂桌上；燭從 a04-s091 滅。末鏡已落在指定角點，空指不動，其餘棋子完全固定。 |

獨立冷場母圖已取消：所有 `chess-guestroom-cold-v*` 都是 retained evidence／not-for-input，不得從舊圖塞回月輪，也不宣稱那些修圖已成功。場景／道具 latest 數因此回到 28，具體最新清單由場景 receipt／主控資產整合保管。

棋盤北向與座標不轉不鏡像。以原 8 黑＋8 白的 16 點為終段母集合：先扣 s051 白 [4,3]、s062 黑 [5,4]、s071 白 [15,3]、s079 白 [5,5]，早盤為 12；依序為 13、14、15、16，s079 至 a05-s090 固定 16，末白 [1,17] 才成 17。手持未落黑子及棋罐不算盤上。這是同點子集時序提案，沒有額外造棋。Builder 逐坐標比對 [六個棋局狀態](../scene-prop-design/go-layout-decision.json)；冷場三鏡則綁 [cold-state-spec](../scene-prop-design/cold-state-spec.json) 的乾淨母圖 SHA 與 rendered=false。

## 驗證與交接邊界

離線 builder 與 `--check` 命令：

```text
node docs/videos/series-plans/ou-de-jianghu/visual-development/handoff/build-finalization-20261009.mjs <VIDEO_WORKDIR> <V4_WORKDIR>
node docs/videos/series-plans/ou-de-jianghu/visual-development/handoff/build-finalization-20261009.mjs <VIDEO_WORKDIR> <V4_WORKDIR> --check
```

本輪 Windows 使用 bundled Node v24.19.0。驗證不呼叫 provider，不寫正常 runtime；57 個分派 logical keys 皆可對應候選實檔（其中含 8 嘴形）。來源與候選最新版本變動時，先保留舊收據，再重建／重驗；hash 不同就是新的輸入，不可沿用舊採用狀態。

舊 9 人 staging 綁 v3，沈全身也是舊 v1：維持歷史 pending 匯入證據，**沒有**聲稱新版 v4／修扇版已進正常 look。後續尚需個別候選採用、正式 judge／look／audio／storyboard 關卡、實際首格參照讀回與連續三鏡小樣接受；不得用此規劃文件填成已核准。
