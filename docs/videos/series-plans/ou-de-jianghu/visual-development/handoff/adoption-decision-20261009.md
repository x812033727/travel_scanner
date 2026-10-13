# 第一集正式採用與 Hailuo plan 鎖定

站主回覆：「採用素材與 v4，按此點數上限鎖定 plan」。依此正式採用146張素材的既定參照用途與v4，已在正常工作目錄寫入原生 `plan/lock.json`，再執行 `--check` 通過，`changed=false`。沒有改寫v4、原始素材或歷史收據。

## 本次決定

| 項目 | 正式範圍 |
| --- | --- |
| 素材 | 146張，逐圖SHA與用途見 [採用決策JSON](adoption-decision-20261009.json)；白扇、冷場、棋盤、原生尺寸與靜態嘴形限制保留 |
| 分鏡與路線 | v4、455鏡；Hailuo網頁、Max、H3、2K、最多2takes；plan設定assist off，實際頁面AI潤飾開關仍須在送出前核對 |
| 本期點數 | 現有額度最多26,980.8點，包含管理預留 |
| 首批小樣 | a02-s035／036／037，三支各4秒，上限316.8點包含在本期內；小樣驗收後才放量 |
| 第二期 | 上限21,753.6點，須實際有該期額度才能續做；兩期合計48,734.4點 |
| 付款範圍 | 不購點、不新訂／續訂、API支出授權US$0；歷史US$677.4817方案與工具內訂閱估價均不是付款授權 |

原生鎖不自動管理這份人工兩期預算。每批須核對 [逐鏡批次JSON](../episode-plan/budget-and-batches.json)、現有餘額、其他已保留支出、實扣與剩餘上限。工具仍警告片段機器期望30,304.8點超單月27,000點；人工納入接觸鏡風險後期望30,494.4點，因此本案保留分兩期的安排。不得用這次鎖定超額送出或自動付款。

## 真實關卡結果

| 檢查 | 結果 |
| --- | --- |
| 原生plan `--write` | exit0，455鏡寫入正常工作目錄 |
| 原生plan `--check` | exit0，look／visual／speech／script雜湊與路線設定均無變更 |
| 原生plan `--ready` | exit1，2項通過、429項未齊；尚不能送出動畫 |
| 最新9張角色基底 | 正常runtime各1張pending候選；9 dry-run＋9 import＋9去重重跑，全exit0，沒有fetch或付費 |
| look | 待真實judge、choice與正常核准；Mokaair `drama_enabled=false` 且本次API支出授權0，不填假結果 |
| 其餘媒體 | v4 script、audio、storyboard關卡、錄音時間線、420支clip首格及3末格仍未到位；規劃的30張still首格也尚未製作 |

v4的無台詞動作文字與原稿不同，不能拿原稿的script核准代替。角色look_hash與原稿相容只代表基底契約相符。後續製作命令須持續指向本次v4；將其整合回repo正典仍須與原檔持有人交接。本次沒有配音、關鍵影格或動畫生成，沒有扣API、購點或續費。

## 證據與重查

| 檔案 | SHA-256 |
| --- | --- |
| v4 video.json | `cb341b457f28e5139cff6f0528722d2a0facebf8cfea90423aec572ed71ebd17` |
| 正常 plan/lock.json | `6af3dafa4f9edc0a03270800a9d3fd44c6f487a3c015627fda4a4205f385d0c5` |
| 原146張清冊 | `cbda063982c38b4135745e798659e51c88a1e529b53da5b2a810cbe68af9f540` |
| 正常 characters/manifest.json | `cf37aa3541380f13b864d3c01560e533fc176e7c5d85f472560408e85f7406b6` |

完整使用者問題與回覆、逐圖接受、預算SHA及鎖定指紋在 [決策JSON](adoption-decision-20261009.json)。外部原生write／check／ready的stdout、stderr、argv與時間保存於 `<VIDEO_WORKDIR>/ou-de-jianghu-e001/adoption/20261009/approved-plan-*`。寫鎖程序持有專屬LEASE，結束已釋放；fetch禁用且呼叫次數0。

在repo根目錄重查已保存的素材與鎖定決策：

```text
node docs/videos/series-plans/ou-de-jianghu/visual-development/handoff/record-adoption-20261009.mjs <VIDEO_WORKDIR>/ou-de-jianghu-e001 --check
node docs/videos/series-plans/ou-de-jianghu/visual-development/handoff/prepare-runtime-look-20261009.mjs --check --media-base <VIDEO_WORKDIR>
```

[Hailuo頁面核對](hailuo-preflight-20261009.md)、[正常候選接入](runtime-look-preparation-20261009.md) 及 [關卡診斷](gate-preflight-20261009.md) 各保留自己的時間與範圍。頁面當時顯示27,000點、H3 2K 4秒48點，僅調整空白表單，未按建立。
