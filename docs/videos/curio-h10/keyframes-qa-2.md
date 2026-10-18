# H10 分鏡插畫 QA：八鏡定向修圖複核

日期：2026-10-16（Asia/Taipei）。本輪承接 [首次目視 HOLD](keyframes-qa-1.md)，只定向重畫當時列出的八鏡；其餘 65 鏡沿用先前已通過評審的圖片。`video.json` SHA-256 `A43541019B57D0EF624A6AF2573C728CC5009894121EE9DE6E8BBF5623EC8C57`；已核准的 `script.md` SHA-256 仍為 `A4A64B02732D97C9DDB216B2CD42F789D95A0B0ADEB8AB3CE22B3C9CA679E596`，劇本文字與旁白未動。`lint --slug curio-h10` exit 0、0 errors／2 個既有畫面詞頻 warnings；`status` 讀回 script approved、narration approved、keyframes drawn，送審前 storyboard 尚未核准。

新版 `keyframes/manifest.json` SHA-256 `658D8630C8B9EAACA8AD4EF3F3A572291938B471C43C6865C628DFE7D702374E`：**73／73 鏡有圖、73／73 Gemini 九題 judge passed、0 `needs_review`**。本機媒體帳本記 134 次 MiniMax 圖片、135 次 Gemini 評審，合計 **US$1.819 工具估算**；不是供應商最終帳單。這次定向修圖的 12 次圖片與 12 次評審均計入此累計；本複核者沒有再呼叫付費服務。

| 原 HOLD 鏡頭 | 新 manifest 選中圖 | 複核結果 |
| --- | --- | --- |
| `tease-map` | `tease-map-2-trim.jpg` | 北極服裝人物在桌上的海圖標示位置，舊版「在海灘畫」的矛盾已消除。 |
| `ship-cannot-move` | `ship-cannot-move-1-trim.jpg` | 船上人物面向大片浮冰，已表達困冰；額頭有小色塊但不是史實矛盾，judge 7.88／10 passed。 |
| `rae-accounts` | `rae-accounts-1-trim.jpg` | 穿厚衣的記錄者與指向海面的嚮導站在雪岸，無舊版東亞庭院。 |
| `plan-written` | `plan-written-1-trim.jpg` | 在船艙內寫計畫、窗外為冰海，已移除錯誤的東南亞地圖。 |
| `fork-shape` | `fork-shape-2.jpg` | 圖中為鏽蝕 U 形鐵件，已不再是三齒園藝叉。評審指出下方閉合，屬卡通道具造型偏差；[Parks Canada 原始敘述](https://parks.canada.ca/lhn-nhs/nu/epaveswrecks/culture/archeologie-archeology/decouvertes-discoveries/erebus)亦稱實物為 U 形並說其看似自行車前叉，故此圖足以承接旁白，沒有把它當證物精確重建。 |
| `oreilly-location` | `oreilly-location-1-trim.jpg` | 兩人看無字海岸圖，舊版假中文與英文地名已消失。 |
| `identity-scope` | `identity-scope-3-trim.jpg` | 名牌上的假中文已移除；畫面為研究者對著沒有可辨標籤的未完路線，符合身分與路線分開的界線。 |
| `next-day` | `next-day-1.jpg` | 深色聲納螢幕呈現水下船體輪廓，沒有舊版浮在海面的現代船圖樣。 |

四頁新版聯絡表均已逐頁目視，這八鏡之外沒有新發現的明顯旁白／史實相反畫面；其他已通過評審圖的景別和卡通道具細節依 `curio-episode` 規則保留。

| 頁 | 本機聯絡表 | SHA-256 |
| --- | --- | --- |
| 1 | `<home>/mokaair-work/videos/curio-h10/keyframes/contact-sheet-01.png` | `667246089C29100B7FA6A7B8F5366C02DA1D52A5438B6A2824DF2C7C2F95D78D` |
| 2 | `<home>/mokaair-work/videos/curio-h10/keyframes/contact-sheet-02.png` | `DD5D6EEAF834B81BDF95FA63D87D23302740705F22FDE946C96F7DB218680CEE` |
| 3 | `<home>/mokaair-work/videos/curio-h10/keyframes/contact-sheet-03.png` | `8F7E6E2CAC8C33E66AB9ED2ACCFF63CFF4D44DF0644642810275053DD62787A2` |
| 4 | `<home>/mokaair-work/videos/curio-h10/keyframes/contact-sheet-04.png` | `C6EB8D33D189A6F679FC0CA35F2981414D8B99BD2F7F9EF80EF70693F1E599D9` |

## 後台分鏡關卡

已執行 `review-push --slug curio-h10 --gate storyboard`，工具回報 `storyboard submitted for review (pending)`（exit 0）。隨即執行 `review-pull --slug curio-h10 --gate storyboard`，現場讀回 `storyboard: waiting for the owner`（exit 1，等待狀態）。站主需在 `/admin/videos` 查看四頁聯絡表並核准這份新版 manifest，才可進入正式成片；目前沒有站主分鏡核准。
