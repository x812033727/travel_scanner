# S04／S05／S23／S40／S34 成片與 Shorts 本地交付查核

2026-10-22 UTC。此收據只核對本工作區私有檔案、組片報告、QA 與交付紀錄；沒有上傳 YouTube，也沒有代替站主完成網站後台或 Studio 審核。以下 SHA-256 為完整檔案雜湊。

| 集數 | 長片 `final.mp4`／`upload/final.mp4` SHA-256 | 長度 | 片頭動畫插入點 | 紀錄中的當前 Short `upload/final.mp4` SHA-256／長度 | 長片 QA |
| --- | --- | ---: | ---: | --- | --- |
| S04 | `8a00edf933edaadd0ba9ad29d3abce5e78aee5a05b3e8c7a81cc5f5867a9d116` | 515.400 秒 | 34.300 秒 | `e3f496b0ad6b9cab5b338b62724991d1ad1b840312f7ad0544572a245938242a`／29.333 秒 | 10／11，`links` 未過 |
| S05 | `349e716a174dd5fa28ab8ac687b426f04d3a0e665ede3d7a4b1a822be85eb5c6` | 617.505 秒 | 46.267 秒 | `a1b6d0bac28565c7389423574f090b250fd2a62f8cf0cf46c529687765c50a60`／31.567 秒 | 10／11，`links` 未過 |
| S23 | `9e95b324d7737c16c6d671aca2103ea3272f6f8eab99246a80dc7ebc5c9389a3` | 522.805 秒 | 32.100 秒 | `7edf01f74faaaa05505d0784b1719da8907ccae4ccf8f14131d9ae486793a31e`／30.400 秒 | 10／11，`links` 未過 |
| S40 | `cca8cb61e72d6c467b68b9c577dabd6229cd3ace227b655fbfabe81144cc2070` | 559.400 秒 | 34.533 秒 | `e5792d7165c3e481aa1a0ab2ecdb176d358775921caa7b9723de1f2e244d7532`／33.000 秒 | 10／11，`links` 未過 |
| S34 | `a14f5647283fa8a64b093eaf0e4c37158c1983d6c3cea180196ef205c183f512` | 595.800 秒 | 37.600 秒 | `4b512a95c81efe8e3e554de5b9a4853d0f9fe733da3fa8fdb6680aec57019034`／31.833 秒 | 9／11，`links`、`policy` 未過 |

長片位置均為 `/workspace/.video-work/curio-sXX/final.mp4` 與同目錄 `upload/final.mp4`。兩份實際檔案 SHA 相同，且與各自 `upload/metadata.json.final_sha256`、`review/qa.json.final_sha256` 相符。當前 Shorts 位置依序為：

- S04：`/workspace/.video-work/curio-s04-short-1/e89657a84d2c3596-1792522794968/upload/final.mp4`
- S05：`/workspace/.video-work/shorts/curio-s05-short-1/8ebb0cf7dd84b596-1792475801085/upload/final.mp4`
- S23：`/workspace/.video-work/curio-s23-short-1/9e84ee6865de1338-1792523643173/upload/final.mp4`
- S40：`/workspace/.video-work/shorts/curio-s40-short-1/40c6748b61c8f9f3-1792496854572/upload/final.mp4`
- S34：`/workspace/.video-work/shorts/curio-s34-short-1/3a4b53bf4bf00d50-1792475082476/upload/final.mp4`

上述 Short 雜湊與本工作區各集的 `short-delivery.md` 相符；S40 以 `short-verify-2.md` 的當前交付版為準。各長片根目錄的 `checks.json` 組片檢查通過：首章即上表的 32–46 秒濃縮開頭，接著插入 150 格／5 秒動畫片頭；最後接 630 格／21 秒動畫片尾，末 16 秒預留兩個推薦影片框與訂閱圈。兩段共用動畫素材確實存在，SHA 分別為片頭 `a5ae205fcf6fa7c92998ac4991225e54206fff482cf03493a60cfb2519e8fcef`、片尾 `275475470f1b7b5d93a2948f561d6e300d0406f9a5b2ab17cfb0dfe4bb3f34ee`，與各集 `branding.json` 相符。以每秒一格抽查的影格差異可見片頭與片尾有畫面變化。各長片有繁中 SRT、VTT 和上傳標題、說明、標籤、章節、縮圖、AI 內容揭露設定。英、日、韓長片字幕仍在 QA 警示中列為未翻譯。 五個當前 Short 上傳包則各有繁中、英、日、韓四份 SRT 與 `metadata.json`。

**待完成的真實交付關卡：** `checks.json.ok=true` 僅表示組片檢查通過；五集 `review/qa.json.ok` 均為 `false`。五集 `links` 失敗同指說明欄內頻道網址 `https://www.youtube.com/channel/UCR0rRWT4blMDUwEMx-TZ57Q` 的 `fetch failed`；S34 的[獨立診斷](curio-s34/qa-investigation-20261021.md)記錄本雲端代理在 CONNECT 階段回 403，因此尚不能據此判定網址本身壞掉。要在可連 YouTube 的瀏覽器或已授權 API 核對並記錄結果，再由後台明示處置，不能改 QA 布林值湊過關。

S34 的另一個失敗是 `/workspace/.video-work/curio-s34/review/qa.json` 的 `policy` 項：Jev 回 `sponsored=0.42`，伺服器門檻為 `0.30`。輸入由 `tools/video/qa/policy.mjs` 的**旁白劇本和站主觀點**組成，檢查由網站 `/api/video/automation/judge/policy` 回傳。現稿所查到的推廣詞只有對自家免費頻道「訂閱奇聞檔案局」；這支持誤判可能，但不能改寫既有未通過結果。若網站修正 Jev 題目，明確區分自家免費訂閱與第三方業配，加入兩類測例並部署，再對**同一長片 SHA**重評，則這個處理範圍是伺服器判準和 QA，**毋須重混影片**。網站真人審核也可依完整證據作明示例外，不能冒充 Jev 自動通過。若審核判定原旁白確實違規，才需要修改稿件、重錄旁白、重新組片並重新審核。詳見[原診斷](curio-s34/qa-investigation-20261021.md)。

長片 metadata 目前沒有這五集新上傳後的 YouTube 觀看 ID；Short 包裝中的長片導流網址仍是待填欄位，Short QA／包裝仍未全過。MP4 內片尾的推薦框是動畫畫面，**不是可點連結**。必須先私人上傳長片，在 YouTube Studio 將片尾最後 16 秒設成可點的影片、播放清單與訂閱元素並實測，取得真實長片 URL 後更新 Short 導流與網站版本，才可稱連結完成。不可借用其他影片的 ID 或將本地預留框稱為已設定的 Studio 元素。
