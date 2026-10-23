# 幼兒英文前五集試播

本批依 2026-10-07 對話中的授權製作：幼兒 3–6 歲、先做五集、每集約三分鐘；英文直接出現在畫面，另提供繁體中文、簡體中文、日文、韓文的教學配音及 CC。英文原版音軌保留，英文示範音檔在五種教學音軌中完全共用。

| 集次 | 主題 | 核心英文 |
| --- | --- | --- |
| 01 | 見面與道別 | Hello / Goodbye |
| 02 | 看看心情 | Happy / Sad |
| 03 | 一起找顏色 | Red / Blue / Yellow |
| 04 | 數到三 | One / Two / Three |
| 05 | 聽英文做動作 | Stand up / Sit down / Clap |

每集十個短場景；單字示範、跟讀、指認與動作交替。答題場景先播放英文示範，保留六秒反應時間，再顯示英文及所選語言的答案字幕。其他跟讀場景保留五秒。兒童不需識字、書寫或每次出聲；看、指、揮手和模仿動作皆可。

## 製作資料

- `lessons.json`：原始英文、繁中講解、英文畫面字、教學目標與場景指示。
- `localizations.json`：簡中、日文、韓文講解與四語 CC 翻譯。
- `tools/video/preschool/audio.py`：依合成音訊實測時間安排共享英文示範、等待與揭答。
- `tools/video/preschool/visuals.py`：原創 Sunny 小熊、Pip 小鳥與教學物件動畫。
- `tools/video/preschool/build.py`：合成 MP4、封裝五組音軌與四組 CC、檢查媒體串流。
- `tools/video/preschool/player.py`：輸出離線預覽播放器，配音與字幕可獨立選擇。

影片、音檔、音訊快取與圖像輸出至 repository 外的 `/workspace/preschool-pilot-output/`，不加入公開 git。畫面為 1280×720，英文已寫入每格畫面。MP4 的預設音軌為繁中，另含英文、簡中、日文與韓文音軌；字幕只有四種指定語言，沒有英文 CC。

## 聲音與後台界線

目前工作區沒有後台影片工具的配對憑證。本批使用 Microsoft Edge read-aloud 合成聲音作為試播聲音，並在交付包標明來源，沒有聲稱使用已配置的 Gemini／Azure 聲音。英文示範與五種教學講解均為實際音檔，不依賴觀看裝置即時合成。連線保留執行環境的 proxy 與 CA 驗證。

這批是獨立、可供觀看的試播；未上傳 YouTube、未發布網站、未建立正式後台專案，也未更動後台聲音、字幕或長片設定。現有全自動產線的八分鐘下限、固定原文 CC、配音翻譯整句等行為不適用這次的幼兒需求，因此不偽裝成漫劇、也不以 smoke 旗標繞過長片驗證。

正式接入後台需要新增明確的幼兒製作規格，支援短片時長、四語 CC allowlist、固定英文畫面與共用英文示範。此項不是觀看本次試播的前提。

## 重建與驗證

合併課程及在地化資料後，先用 `audio.py --source <合併資料> --output <repo外目錄>` 產實際聲音與 `lessons.resolved.json`，再執行：

```bash
python tools/video/preschool/build.py \
  --source /workspace/preschool-pilot-output/lessons.resolved.json \
  --output /workspace/preschool-pilot-output
```

每集 `checks.json` 記錄 ffprobe 的實測長度、畫面尺寸、五組音軌及四組字幕。音訊 manifest 保存聲音來源、快取與時序；字幕依實測語音長度輸出，答題時不提前顯示翻譯答案。觀看者仍應以實際試聽判斷語音自然度與幼兒參與節奏。
