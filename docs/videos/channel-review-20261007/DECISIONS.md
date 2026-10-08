# 站主的決定（2026-10-08）

對 [`README.md`](README.md) §2.4 的矛盾清單，站主 2026-10-08 在 Claude Code 的選項提問裡逐條拍板。沒列的項目維持原規格。

| 項目 | 決定 | 接著做 |
| --- | --- | --- |
| 縮圖的視覺主體 | **允許產品 logo／介面截圖當主體**（評論該產品時的合理引用） | 改 SKILL.md 規矩 6、`visuals.md` §縮圖；版型改成左 40% 大字、右 60% 主體。實作時的取捨（2026-10-08，待站主確認）：logo 與介面**只來自 screencast 的真實截圖**（`thumbnail.data.capture`），look 的 negative 維持擋 logo 與文字——AI 畫的 logo 既不準也不算合理引用；要讓 AI 畫 logo 的話另開票；票 `2026-10-07-video-thumbnails-one-subject-six-characters` |
| 教學片的真實畫面 | **解禁 screencast：公開官方頁自動截圖**；登入後的介面仍不做（不走 OBS） | `prompts.mjs` 第 103 行解禁，撰稿對 `sources` 裡每個公開官方頁至少放一個 `screencast` 景；票 `2026-10-07-video-script-rules-outro-with-a` |
| 結尾與片尾 | **旁白固定三句（回答開場問題、留言題、有理由的訂閱邀請）＋片尾卡只求訂閱、拉長到 15 秒** | 稿子規則進 `prompts.mjs` 與 `script-writing.md`；新的 `outro.mp4`（15 秒、只有「訂閱」）由站主準備素材包用 `branding --install` 安裝；`README.md` §片頭與片尾改成 15 秒 |
| 上架節奏 | **不限制，做好就上**（維持現狀） | 不做排程器；DESIGN／STORY／HANDS-OFF 的節奏段落不改。四週後若 Studio「觀眾上線時間」有明顯峰值再談 |
| 燒錄字幕 | **不燒，維持 CC** | 不改 `render/subtitles.mjs`；與 10-01 的全 CC 決定一致 |
| 人設 | **給旁白一個名字、一句固定收尾句、一個口頭禪；不做吉祥物** | 名字與那兩句話由站主填進後台「各階段常設指示」與頻道立場（文字待站主定）；撰稿規則放行自稱，第一句仍是鉤子 |
| 系列名與預告片 | **系列名當後綴、不編號；用 S88lbAsLz2E（Google Vids）當未訂閱者預告片** | 標題規則進 `metadata.mjs` lint（票 `2026-10-07-video-metadata-title-length-lint-description`）；預告片與播放清單是站主在 Studio 設 |
| 下一步 | **先把 4 張工程票做掉**（站內互導 API、稿子規則、縮圖 QA 與版型、標題／說明欄 lint），在分支 `claude/focused-hopper-t3zgz9` 逐票提交，不開 PR | 本 session 接手 |

仍要站主自己做的（README §6.1）：橫幅與說明前 45 字、頻道關鍵字、預告片、3 個系列播放清單並勾官方系列、精選區塊、18 支置頂留言與結束畫面、開 Studio 自動配音、配樂床與音效組、匯出 Studio 數據、旁白的名字與固定句、新的 15 秒片尾素材。
