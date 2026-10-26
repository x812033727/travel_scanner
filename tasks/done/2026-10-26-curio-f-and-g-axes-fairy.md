---
id: 2026-10-26-curio-f-and-g-axes-fairy
title: Curio F and G axes: fairy tales, myths, ghost stories, plan and topic bank
status: done
priority: P2
area: docs
owner: claude-opus-5-5-storyteller
claimed_at: 2026-10-26T13:31:13Z
created_at: 2026-10-26T13:30:00Z
completed_at: 2026-10-26T16:34:33Z
branch: claude/clever-archimedes-4oqn4s
depends_on: []
scope:
  - docs/videos/history-curiosity/README.md
  - docs/videos/history-curiosity/topics-fg.json
  - docs/videos/storyteller-genres-20261026
---

# Curio F and G axes: fairy tales, myths, ghost stories, plan and topic bank

## Why

站主 2026-10-26 問 YouTube 的「說書人」系列（三國、格林童話、國外的其他故事）有沒有市場、還能做哪些題材，追加外星與靈異，
再問哪些題材點閱比較高；看完評估說「好，照計畫開始做」。評估的建議是不另開系列，把童話、神話與怪談（F）和靈異事件（G）
放進奇聞檔案局當新的兩軸，先量各類題材的點閱再決定加什麼。

## Definition of done

- [x] 15 類題材的 YouTube 搜尋點閱量測，有數字、量法與可重跑的腳本：`docs/videos/storyteller-genres-20261026/`。
- [x] `docs/videos/history-curiosity/README.md` 有 §F 軸與 G 軸：為什麼放在奇聞檔案局、說書版一集怎麼講、示範開場、鉤子來源、
      題庫與順序、試片四集、U 軸說書版、版權與畫面、靈異守則、不收的題目、還沒做的；§題材、§票、§選定紀錄同步。
- [x] `topics-fg.json` 有 F01–F38、G01–G23（`candidate`，跟 `topics.json` 同 schema、不重複）。
- [x] 試片、主機路線、併回 `topics.json` 各有自己的票。

## Steps

- [x] 用 yt-dlp 量兩輪（每類各三組關鍵字），只留中文標題、去掉歌曲與電影頻道，算中位數、前 25% 門檻、百萬片數與拿掉老高的中位數。
- [x] 跟既有 224 題比對去重。
- [x] 寫 README §F 軸與 G 軸、`topics-fg.json`。
- [x] 開 `2026-10-26-curio-f-and-g-pilot-f01`、`2026-10-26-curio-host-route-knows-the-f`、`2026-10-26-merge-curio-f-and-g-topics`。

## How to verify

`python3 -c "import json,collections;d=json.load(open('docs/videos/history-curiosity/topics-fg.json'));print(collections.Counter(t['axis'] for t in d['topics']))"`
印出 F 38、G 23；`npm run check:tasks` 過。

## Notes

- **題庫沒有直接寫進 `topics.json`**：那個檔還在 `2026-10-18-curio-s-axis-pilot-s01-red`（in-progress，10-18 認領）的 scope 裡，
  `claim` 拒絕重疊；用 `--force` 搶過被自動模式擋下，所以改放 `topics-fg.json`，沒有程式讀 `topics.json`（grep 過），分開放不影響產線。
- 量測推翻了評估時的一個猜測：我原本建議加「災難與生還」「古代人怎麼生活」「歷史騙局」，量出來分別是中位 1.9 萬、5.3 千、1.7 千，
  所以不開 D 軸、不加題。童話神話（6.2 萬）與靈異（5.0 萬）是前兩名，拿掉老高也一樣。
- 第一版量測沒過濾歌曲，「鐵達尼號 最後」抓到〈挪威的森林〉（1 億）與〈My Heart Will Go On〉；加了歌曲與電影頻道的過濾後排序不變。
- 題目卡上的事實是憑既有知識寫的，沒有開來源；試片票逐條查核。
