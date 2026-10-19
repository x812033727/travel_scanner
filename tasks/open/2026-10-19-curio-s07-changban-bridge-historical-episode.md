---
id: 2026-10-19-curio-s07-changban-bridge-historical-episode
title: Curio S07 Changban bridge historical episode
status: in-progress
priority: P2
area: docs
owner: codex-s07
claimed_at: 2026-10-19T18:26:17Z
created_at: 2026-10-19T18:26:13Z
completed_at:
branch: codex/curio-s34-endurance-20261019
depends_on: []
scope:
  - docs/videos/curio-s07
---

# Curio S07 Changban bridge historical episode

## Why

題庫把《演義》說成「喝斷橋」，但《三國志·張飛傳》原已有「據水斷橋」；小說也只寫張飛退敵後命人拆橋。需要一集讓觀眾看懂劉備敗走、張飛二十騎拒後的正史核心，以及後來小說增加的疑兵、三喝和拆橋後果。

## Definition of done

- [x] 8 分鐘以上可審閱企劃、固定史料、逐句主張、`video.json`、`script.md`。
- [x] `lint` 為 0 errors、0 warnings，故事長度至少 8 分鐘。
- [ ] 完成獨立盲讀與來源覆核，再交由系列負責者決定付費媒體步驟。

## Steps

- [x] 核對固定《三國志》卷 32／36、《三國演義》第 41／42 回及建安十三年紀年。
- [x] 寫六章 99 句、90 張插圖的可愛漫劇旁白和分鏡。
- [x] 為每句建立史料或小說層級對照，避免把五千騎畫成橋頭實數。
- [ ] 由未讀企劃與史料的讀者盲讀旁白，修正故事節奏並記錄回執。

## How to verify

在 `/workspace/travel_scanner` 執行：

```sh
node tools/video/cli.mjs lint --slug curio-s07
node tools/video/cli.mjs script --slug curio-s07
node tools/video/cli.mjs narrative --slug curio-s07
```

2026-10-19 已執行首兩項：0 errors、0 warnings，估算 9.5 分鐘／120 句／1932 spoken units；劇本雜湊 `1827d1f677db0f72`。

2026-10-19：上述初版獨立盲讀僅 8／13，舊稿有返回橋頭重講、宣告「換一本書」、章首脫節、未回收敵人不敢近的原因，以及結尾重述事實等阻斷。已重構史書橋後劉備逃向漢津與小說橋後拆橋再追的後果鏈，避開總結重述。另依來源覆核刪去小說不支持的曹操「先看清楚」、曹軍「面面相看」字句；史書斷橋不指定施工者和橋材、小說在退敵後才拆橋。修訂詳 [`verify-1.md`](../../docs/videos/curio-s07/verify-1.md)。目前 **99 句／90 插圖／六章、估 8.4 分鐘、lint 0 errors / 0 warnings、script SHA-256 `8b459182e0726732487df2ccddead4cbd15bb404a74b3943500ff193f49da216`**；逐句表 99 句同步。仍待新雜湊的真正獨立盲讀與來源查核，沒有啟動付費媒體。

2026-10-19：上列版的新來源隔離盲讀 **12/13**，`one_line` 再次否決史書與小說重走同一趟橋頭；兩名讀者同題均否，故改成一次前進的時間線，把史書挑戰原句放在小說三喝的同一動作處。讀者的七組固定史料抽查通過，另提示舊 `eb094` 未明確區分原文先後與真實拆橋時點；現稿已釐清，並補第 42 回關羽截兵的固定行號。**現版 96 句／88 插圖／六章、估 8.2 分鐘、lint 0 errors / 0 warnings、script SHA-256 `93eaaf928a3853b84a0231d313ce8eff8af6fb13c04f05b396d0da956a709a03`**，逐句表同步。原始回執與改稿見 [`verify-2.md`](../../docs/videos/curio-s07/verify-2.md)；下一位獨立讀者須看此確切雜湊，媒體仍暫停。

2026-10-19：在新讀者開始前，作者再刪去小說章首「第二次來到橋頭」的說法，讓它直接新增橋東樹林的動作。最終待讀版 **SHA-256 `da7f4441442e48c2438c36853bb940df603b37070bef784b4109a3702bda8a12`**；仍為 96 句／88 插圖／估 8.2 分、lint 0/0，詳細說明見 [`verify-2.md`](../../docs/videos/curio-s07/verify-2.md)。此雜湊尚未取得新盲讀，不可沿用前版 12/13 結果。

## Notes

固定版本：`Ancient-China-Books/sanguozhi@10a0b1ab3019d8821262f7402366d14fb4aaa102` 與 `Ancient-China-Books/sanguoyanyi@761813427eb5685c395804493f9fbd7ad8dc7d8d`，直接段落連結見 `research.md`。`topics.json` 的未核句子有誤，此票不碰共享題庫；以本集已核文本為準。沒有呼叫 TTS、圖片或其他付費生成。協作分工只包含 `docs/videos/curio-s07/` 與此票，不改其他集。

2026-10-19：上一凍結稿 `da7f4441…` 的新獨立來源隔離盲讀得必要題 8/12、選答 1/1，不通過；四個阻斷為劇透、史書／小說時間線折返、開場二十騎回收太弱、結尾重複。固定史料主幹通過，另修小說挑戰字句與聲勢、露天窗光。集中改稿現版 `script.md` SHA-256 `3abd11daead95c90d68147173eec97e467828eb63d6d8f65daf84046bbb7d330`，95 句／86 插圖／六章、估 8.1 分、lint 0 errors / 0 warnings，逐句表同步。原始回執與改稿見 [`verify-3.md`](../../docs/videos/curio-s07/verify-3.md)；尚待新的確切雜湊獨立盲讀和改句來源覆核，不啟動付費媒體。
