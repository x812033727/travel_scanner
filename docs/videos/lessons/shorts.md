# Shorts 零台詞短劇（共用與四系列）：教訓

所有無語音（零台詞）Shorts 短劇（《汪家夫妻》《闖禍小浣熊》《網美小豬》《社畜地獄》與後續新增的直式短劇系列）在企劃、審劇本、畫首格、跑 H3 片段、剪接與雙人笑點審核中學到的教訓。

寫法：一條一段，最新的放最上面。開頭寫日期、哪一集或哪個系列（slug）、誰發現的，接著寫發生什麼、為什麼、下次怎麼做。
已經變成正式規則的，搬進 [`docs/videos/shorts-drama/`](../shorts-drama/README.md) 的共用或系列規則檔，這裡留一行「已升為規則：<檔案>」。

這份會自動同步到雲端硬碟 `AI劇/_共用規則/教訓/shorts-教訓.md` 與 `AI劇/Shorts/_規則與教訓/教訓/教訓.md`（`docs/videos/rules-sync`）。

---

## 2026-11-20 · 全系列（前檢自動化、9:16 安全區、重播迴圈與 Google Flow／Veo 3.1 路線）· 站主／規則升級
光靠文字規則與人工自檢，仍容易在寫 20 集規格檔時漏掉某鏡的 `magazine cover`、收尾音效時間超界或開頭過長（實測拿 2026-11-04 的 `influencer-piglet-e02.json` 與 `raccoon-mischief-e02.json` 跑新版前檢，立刻抓出開頭 2.6 秒過長、`magazine cover` 亂碼詞與 2.2 秒鑰匙聲反應鏡）：
- **花錢前必先跑機械前檢**：新增零外部依賴的 `docs/videos/shorts-drama/preflight.mjs`（納入 `npm run test:docs-videos` 單元測試），在送獨立審稿代理與 Colab／Google Flow 前，先用程式硬擋片長、單鏡動態 > 3.5s、SFX 超界、雙人框、人手／畫外伸手／`magazine cover`、系列禁忌與 9:16 安全區 `anchor` 超界；同時提供 `score-blind` 自動核對盲評八軸加總與抓滑走陷阱，以及 `export-flow` 一鍵產出 Google Flow（Veo 3.1）提示詞單。
- **9:16 介面安全區與無黑屏重播**：核心臉部、毛爪與地面／角落線索一律留在 `x: 78–902, y: 180–1380`，成片審核改用 `ffmpeg drawbox` 疊紅框檢查；片尾禁放無意義黑畫面或慢漸黑，讓 11–16 秒短劇自然接回第 1 格衝出 `>100%` 重播留存。
- **Google Flow／Veo 3.1 音訊避險**：Veo 3.1 原生音訊必開、容易自動冒出含糊人聲或怪配樂，Flow／Veo 提示詞必須移除 H3 的 `<Picture 1>` 並強制加無台詞防護句，剪接時預設 `-an` 抽離原片音軌改由 `edit.py` 統一混音。
- 已升為規則：`docs/videos/shorts-drama/preflight.mjs`、`docs/videos/shorts-drama/PRODUCTION-ROUTES.md`、`docs/videos/shorts-drama/WRITING.md`、`docs/videos/shorts-drama/REVIEW.md`、`docs/videos/shorts-drama/series/_template.md`。

## 2026-11-19 · 全系列（汪家夫妻／闖禍小浣熊／網美小豬／社畜地獄）· 站主
將無語音 Shorts 的五拍分鏡結構、聲音三層設計、第 0 關 AI 避險、花錢前審劇本三道檢查與成片四關品管正式收進 repo 規則，並拆成「共用區」與「四系列個別區」，納入雲端硬碟每小時規則同步：
- 先前 20 集零台詞短劇的品管規範（`QA.md`）、五輪審核紀錄（`QA-2026-11-04.md`）、重剪腳本（`recut.py`）與各系列 README 只打包在雲端硬碟 `AI/備份/Shorts/<系列>/`，沒有進 repo 的 `docs/videos/` 與 `rules-sync`，新開的對話一旦沒去翻雲端硬碟就會重新踩到「開頭太慢、畫出人手、背景有路人、笑點動作畫不出來、收尾音效被切掉」的坑。
- 下次怎麼做：做任何無語音 Shorts 或審劇本前，先讀共用區 [`docs/videos/shorts-drama/README.md`](../shorts-drama/README.md)、[`WRITING.md`](../shorts-drama/WRITING.md)、[`REVIEW.md`](../shorts-drama/REVIEW.md) 與該系列的 [`series/<slug>.md`](../shorts-drama/series/)；花點數前先跑 `WRITING.md` 第六節的「審劇本與分鏡三道檢查」。
- 已升為規則：`docs/videos/shorts-drama/README.md`、`docs/videos/shorts-drama/WRITING.md`、`docs/videos/shorts-drama/REVIEW.md`、`docs/videos/shorts-drama/series/*.md`、`.agents/skills/animation-preproduction/references/script-to-storyboard.md`。

## 2026-11-04 · 四系列 20 集笑點審核與 `recut.py` 重剪 · 獨立笑點審片人 A／B
第一版 20 集送兩位獨立笑點審片人（21 歲常滑 Shorts 觀眾、32 歲喜劇導演）盲審時，有 10 集沒過門檻（好笑度 < 3 或核心笑點看不懂）；分析原因後發現超過七成問題出在**剪接節奏與聲音留白**，用 `recut.py` 本機重剪（加上補畫 8 鏡）後，20 集全數過關（好笑度 3–4/5）：
- **開頭鋪陳太長（4.6 秒才進正題）**：《網美小豬》第一版每集開頭放 3 秒唯美照＋1.6 秒快門閃光鏡，前 4.6 秒什麼事都沒發生。把唯美照統一砍到 **1.2 秒**（`0.9s` 打快門聲）、刪掉閃光鏡，第 1.2 秒直接拉遠揭曉假景配 `recordscratch`，五集好笑度全衝上 `4/4` 或 `4/3`。
- **驚覺反應鏡停太久（2–3 秒呆臉）**：《闖禍小浣熊》每集聽到門外鑰匙聲的呆臉停了 2–3 秒，節奏瞬間冷掉。統一砍到 **0.6–0.8 秒** 後緊接第 3 拍偽裝結果，節奏立刻緊湊。
- **轉折與揭曉後沒有停頓、也沒有抽掉音樂**：第一版背景音樂從頭播到尾，轉頭與揭曉瞬間平淡滑過。在 `edit.py` 新增 `"hold": 0.4~1.1`（最後一格定格）與 `"music_off": True`（瞬間切斷 BGM），在老婆慢轉頭、爸爸按遙控器前 0.8 秒、貓老闆從隔板頂俯視、以及結尾被抓包那一格定格並抽乾音樂，笑點力道翻倍。
- **收尾音效排在最後一鏡結束之後，根本沒播出來**：第一版有 4 支片的收尾 `sting`／`dun` 觸發秒數 `at` 設在鏡頭 `dur` 結束之後，被 `ffmpeg` 直接切掉。收尾音效的 `at + 音效長` 必須落在該鏡 `dur`（含 `hold`）結束前至少 0.3–0.5 秒。
- **爆發動作前缺一拍蓄力**：《網美小豬》EP2 第一版水豚直接打噴嚏，審片人看不懂發生什麼事；在前面插入 **1.0 秒水豚結霜臉仰頭閉眼深吸氣（`s05b-inhale`，配 `inhale` 吸氣聲＋`music_off`）**，再接噴嚏爆開，兩位審片人都給到 `4/4`。
- **揭曉順序對調強化反差**：《汪家夫妻》EP5（搶棉被）第一版先拍阿福睡寵物墊、再拍老婆大被捲，張力不足；對調成**先揭曉老婆把棉被地毯窗簾全捲在身上的超巨型被捲（`s04-mega`），再切阿福縮在角落小寵物墊拉小毛巾蓋頭（`s03` → `s05`）**，對比笑點立刻成立。
- 已升為規則：`docs/videos/shorts-drama/WRITING.md` §一／§三、`docs/videos/shorts-drama/REVIEW.md` §3／§4。

## 2026-11-04 · raccoon-mischief-e01／influencer-piglet-e03／wangjia-couple-e02 · Claude（第 2 關重畫 `redo3.py`／`redo4.py`）
「核心笑點沒畫出來」通常不是因為模型不會畫，而是提示詞寫了「動作過程」或「被取代的原物件名」：
- **寫「偽裝過程」或「堵洞動作」會畫成抱著布或站在旁邊**：《闖禍小浣熊》EP1 初版寫豆豆把自己偽裝成花瓶，模型畫成抱著一塊藍布；《網美小豬》EP3 初版寫水豚去堵漏水的水塔，模型畫成水豚站在水塔旁淋雨。重畫時改成直接寫**完成後的靜態結果造型**（`Doudou the raccoon himself is sitting inside a large blue ceramic vase, only his head and green onions poking out`；`the capybara himself is hugging the leaking water tank tightly, his round belly pressed flat against the two holes`），一次過關。
- **提到「原本掛時鐘的地方」就會畫出真時鐘**：模型只要在提示詞裡看到名詞（clock、baby、vase），就會在角色旁邊畫一個真的物件。必寫 `<角色> himself/herself is...`，且**被取代的原物件一個字都不要提**。
- **同一鏡重畫兩次還是犯同一個錯，就停手換表現方式，不再抽卡**：《汪家夫妻》EP2 `s05` 想要柴犬老婆剃平頭，因為參考圖是毛茸茸的柴犬頭，重畫三次模型都不肯把頭頂毛削平。第三次改在**地上畫滿剪下來的粉紅捲毛、手上拿著嗡嗡響的無品牌電推剪（配 `buzz` 音效）**，不用平頭也讓觀眾一秒看懂她把捲髮剃光了。
- 已升為規則：`docs/videos/shorts-drama/WRITING.md` §四、`docs/videos/shorts-drama/REVIEW.md` §4。

## 2026-11-04 · 四系列 20 集第 1 輪畫面審核（抓出 15 個高、40 多個中問題）· 三位掃描代理＋獨立審片人
20 集初版未審核前，站主一眼看出「有些地方怪怪的」；派三位掃描代理逐格檢查後，歸納出 AI 圖生影片在擬人動物短劇的 **6 大系統性畫面錯誤**與根治寫法：
1. **人類手指、手臂與指甲油（黃金獵犬、小豬、浣熊媽媽最常出現）**：只要寫 `holding` 小道具（手錶、遙控器、雷射筆、花灑），模型就把動物爪畫成人手。**解法**：第 0 關改寫成物件放在桌上／胸口／肚子上、毛爪放旁邊，並明寫 `two furry front paws, no human fingers`；已經拍完但臉部表情好的鏡頭（如浣熊 EP4 媽媽看錶），在 `plan.json` 用 `push`＋`anchor` 裁切只留臉部上半段「先低頭、再抬眼起疑」，把人手切出畫面外。
2. **背景冒出人類路人與隔間同事（《社畜地獄》辦公室、街道重災區）**：訓練資料裡的辦公室與街道都有人，寫 `no people` 擋不住。**解法**：正面寫出緊貼主角身後的封閉背景：`directly behind him is a solid plain grey wall, no cubicles, no windows to other rooms, empty room`。
3. **多一隻手或角色分身**：出現在「畫面外伸進一隻手」或雙人同框碰觸的鏡頭。**解法**：嚴守**一鏡一主角（單人框）**，對手戲一律拆正反打，不寫畫外伸手。
4. **5 秒 H3 片段後半自己硬切換景或角色變臉**：H3 常在第 3.5–5 秒自己切鏡頭，或大動作後半臉部變形（如水豚打噴嚏後半變狗臉）。**解法**：`edit.py` 自動在硬切前截斷；剪接表只取 `in: 0.2~0.3`、長 `0.8~3.0s` 最穩的前段，需要停留就用最後一格 `hold` 定格，或直接拿畫得很準的首格做慢推靜圖（`-still`）。
5. **假刊名、Apple Logo 與亂碼字**：寫 `like a magazine cover` 會長出英文雜誌名，寫 `laptop` 會長出蘋果標誌。**解法**：禁寫 `magazine cover`，所有器材與道具必寫 `plain, unbranded, no logos, no text, no numbers`。
6. **同一個 Colab session 先跑 Qwen 再跑 H3 會缺 `VHS_VideoCombine`**：因為 Qwen 啟動的 ComfyUI 環境不含影片節點；跑完首格後先把 Qwen 啟動的 ComfyUI 停掉，讓 H3 筆記本自己重開即可。
- 已升為規則：`docs/videos/shorts-drama/WRITING.md` §二／§四、`docs/videos/shorts-drama/REVIEW.md` §1／§3／§4。

## 2026-11-03 · 零台詞系列企劃三輪盲評與參考片對照 · 製片流程
把 Instagram 33.4 萬讚的狗夫妻零台詞爆紅片轉寫成文字混進新企劃讓三位評審盲評時，33 萬讚的原片只拿到 55 分，六個新企劃反而都比它高：
- **原因**：純文字盲評看不到角色僵住的微表情、慢轉頭的停頓與畫面反差。
- **下次怎麼做**：企劃階段的文字評分（門檻 70 分）只用來**排拍攝先後順序與挑出因果看不懂的盲點**（例如《汪家夫妻》EP3 原本只在空盤留一顆髮捲，三位評審都看不懂蛋糕是誰的 → 改成蛋糕本身畫成平面柴犬臉＋一路短短的柯基奶油掌印）；真正好不好笑，必須在**首格／成片階段由兩位獨立審片人看檢查圖（`qa/<slug>.jpg`）與抽格做笑點審核**。
- 已升為規則：`docs/videos/shorts-drama/WRITING.md` §六、`docs/videos/shorts-drama/REVIEW.md` §3。
