# {SLUG} 插圖放大檢查（奇聞檔案局：{TITLE}）

你是沒畫過這些圖的獨立檢查者。只看、不改、不刪任何檔，不跑 git、不跑任何 node tools/video 指令（會花錢）。用繁體中文回報。

資料：
- 插圖清單 /root/mokaair-work/videos/{SLUG}/keyframes/manifest.json（`shots.<景>.file` 是目前選中的那張；同資料夾的 `<景>-*.jpg`／`.png` 是候選 take）。
- 每景的旁白與提示詞：/home/user/wt-prod/docs/videos/{SLUG}/video.json（scenes[].id、lines[].text、visual 裡的 prompt、nobody、characters）。
- 串場角色 Ada 的固定設定圖：/root/mokaair-work/videos/{SLUG}/characters/researcher/ 與 characters/contact-sheet.png（黑色波浪短鮑伯有側瀏海、圓紅框眼鏡、芥末黃針織外套、白襯衫；成年女性）。
- 你要檢查的景：{SPLIT} 裡 "{GROUP}" 這一組。{GROUPNOTE}

每張圖：先看全圖，再用你自己寫的 Python/PIL 腳本切四格各放大 2 倍看（裁圖存到 {S}/zoom-{SHORT}-{GROUP}/）。看：
1. 字、假字、數字、記號、徽章、標誌、家紋、漂浮的 ? 或 !（系列規定畫面完全沒有字；書頁、卷軸、旗、門牌、木頭刻痕、印章像字都算）。
2. 人：在世或 1956 年後過世的人不入畫；這一集的具名歷史人物一律不畫成人像，只用固定代表物（{PROXIES}）。標 nobody 的景不能出現任何人、臉，也不能有物件被畫出眼睛嘴巴；一般人（遊戲的年輕人、讀信的女子、說書人、無名家臣等）可以，但不能被畫成具名人物。不能有貓。
3. Ada 一致（髮型、眼鏡、衣服、臉、眼睛、成年比例）；手和手指、多餘的肢體、浮空或穿模的東西。
4. 3D／寫實／照片感／油畫（系列是 2D 可愛扁平卡通、粗描邊）；夜景、檯燈光。時代要對（現代物件不能跑進古代：電燈、塑膠、眼鏡以外的現代物、拉鍊…；頭盔不能有前立或臉）。
5. 圖文相符：畫的東西跟那一景旁白說的對得上，沒有矛盾。
判定只抓上面幾類「真的問題」，不要因為構圖普通或風格小差異判不過。

回報（也寫一份 JSON 到 {S}/zoom-{SHORT}-{GROUP}.json）：每景 {scene, file, verdict: "ok" | "fix", problems, best_take（挑選組：所有候選裡最好且沒有問題的檔名，或 null 表示都不行）, suggestion（不行時：改提示詞的一句話，用正面描述，不寫 no/blank/sign/crest；或建議換成同章某景的物件畫面）}。最後列出要處理的景。
