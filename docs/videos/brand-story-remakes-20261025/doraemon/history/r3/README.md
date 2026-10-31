# Doraemon remake R3作者提交包

新slug：`story-adapt-doraemon-after-fujiko-remake-20261025`。R3處理R2實際native1合併的三個shared HOLD：payoffs、no_recap、no_detour。R2 core、SOURCE PASS／verify、native1全部raw/input/binding/merge及runtime狀態均以精確SHA封存在`history/r2`，R1原保全不變。R2舊作者的actualcount0狀態保留原bytes，`history/r2/native-state-after-review.json`另外記錄事後真實actualcount1，沒有重置計數或改既有票。

友情段改問導演如何要求編劇處理冒險動機，隨即以原訪談交代工作要求、辻村原先視為理所當然的假定，以及她後來改從這一對人物關係思考的反應；不掛無法回答的電影友情問題，不編情節。刪除b042重複署名及d04/d05已被d03解答的重述，改由d023一個新工作問題接原有導演台詞建議；筆名沿革移出旁白，留在claims背景。章名advisory及B單票scene_first未列本次改稿要求。

`rows-r3.json`明列保留ID與逐句文本；build從R2固定scene讀取data，所有115個存活scene的prompt、camera及其餘非lines欄位精確不變。135句中改8句、刪14句，其餘127句完整保留，R2的2019上映年修正原句不變。23 loops及單預告→兩段回收皆有明確規劃；是否自然及真回收仍待fresh native2，不自判PASS。

從repo根目錄重播：

```bash
python docs/videos/brand-story-remakes-20261025/doraemon/build-candidate.py
node docs/videos/brand-story-remakes-20261025/doraemon/build-image-reuse-plan.mjs
node docs/videos/brand-story-remakes-20261025/doraemon/free-checks-r3.mjs
python docs/videos/brand-story-remakes-20261025/doraemon/freeze-author.py
```

free-checks只把R2 immutable字典的既有bytes複製到本次隔離目錄，沒有初始化、重建或改動字典；使用正常CLI的lint與tts --dry-run，空ctx.home／env，無憑證或網路。隔離runtime為`/workspace/work/brand-story-20261025/doraemon-audit/author-r3/free-runtime`，media另在`author-r3/media`，不回寫原runtime。dry-run只寫請求規劃，沒有真TTS、音訊、blind payload或模型讀者。

最終3101 native spokenUnits、135行、115 shots、23 loops。免費lint 0 errors、16 soft、0 narrative warnings；全部soft留在`native-author-lint-r3.json`。字數低於約3500容量目標，4.5units/s純口播算式689.11秒、native含正常間隔估值約14.5分鐘，均不是實聲，也不宣稱actual FAIL。目標固定13分鐘，實聲body720–840秒包含開場與voiced CTA，排新增5秒片頭及21秒v4片尾；不慢播、不加空白、不重述、不切碎畫面填長。

42筆下載、研究3檔、213保護項、原後台快照與9份舊原件、R1/R2歷史、原runtime、native1所有舊收據及immutable字典1 version/1 event均核SHA不變。官方對談origin HTTP503與搜尋快取仍分開，不冒充HTML200。只畫匿名工作台、空白panel、無字工具，禁止可辨角色、剪影、招牌道具、真人肖像、logo與可讀字。三端完整Stage requests/keys原樣保留，actual_same_asset_verified=false，仍需先回收takes1、live cache miss即停、三端judge、裁切後實檔SHA及組片引用相同。

當前實際native計數1，R3未prepare或重抽blind；SOURCE差分、fresh native2、念法、實聲、實圖、owner皆pending。R2 verify只存歷史，當前無verify。繁中試燒+CC、後續八語與乾淨主片保留要求不變。新片獨立US$25精確帳戶／全片quote／protected admission未建立，付費、後台、owner及Git操作0。
