# S24 三景試畫與原尺寸覆核｜2026-10-20

## 版本、費用與停批

沿用 [verify-7.md](verify-7.md) 的 R4 劇本、`video.json` SHA-256 `59624d323f19dc99bb04de6ded3e2c118b00dd11c7bf0727cfc37fae710302d7`、時間線 `674a6db7000513d76c937050bff2dd0e28dedea374daea4aa9975213c4dbc390`，沒有修改旁白或繪圖提示詞。執行前定點 `keyframes --shot crown-005,crown-047,crown-r2-021 --takes 1 --dry-run` 精確列出三張，預估 US$0.04；共用過去 60 分鐘圖片請求 9 次，加三張遠低於保守 200 次上限。

正式執行只送三次 MiniMax image-01 圖與三次 Gemini 評審，日誌 `/tmp/s24-three-shot-pilot.log` SHA-256 `cfb46774a910c0fecfb3d56fb1b9297ba95f1e773ee97f5d8f6e8ba01e006538`。`keyframes/manifest.json` SHA-256 `621a82169618eb79641a57fca89a5d8f0cf99dd9b3079a301620e9fdd8c6fcd7`。執行後帳本 `/workspace/.video-work/curio-s24/media/ledger.json` SHA-256 `4fb9c7ad6dc870995763a797cb3e7207ca88cf2334b29e44851eb0526d0396cd`：累計 **US$0.1205**，其中原音樂 US$0.08、三圖各 US$0.0035、三次評審各 US$0.01；圖片 3、評審 3、未結預留 0，仍在整集 **US$4.35** 硬上限內。作業退出後建立 `/workspace/.video-work/curio-s24/STOP`；沒有開 99 景批次。

## 所選 1K 圖逐張原尺寸判讀

| 景號 | 所選圖片 SHA-256 | 機評 | 原尺寸製作判定 |
| --- | --- | --- | --- |
| `crown-005` | `e27c0b4b73d7770d7ff18856b388073b148fe07c1ed9a95ba5b31edf88b29af3` (`keyframes/crown-005-1-trim.jpg`) | 9.29／10 PASS | **不計 KEEP**：浴盆主角讀作孩童，左後又有另一浴客；獨立覆看者判成人阿基米德的角色身份未立住。卡通大眼本身不是拒絕理由，這裡是主角形象及多人的具體偏差。 |
| `crown-047` | `a528432d27700e5303cf3e1d8626044d9108f3a10fdd71c6d3e07ba1d483981a` (`keyframes/crown-047-1.jpg`) | 9.29／10 PASS | **不計 KEEP**：量杯雖向盆內倒水，但主角讀作孩童，盆內沒有可見水線到達盆緣；旁白的關鍵量測終點無法驗證，機評 details 亦指出未達 brim。 |
| `crown-r2-021` | `277c8eebb97826e859562eaf89dd3ed96556c3645c8ec77da36bd330ac2ef687` (`keyframes/crown-r2-021-1-trim.jpg`) | 9.29／10 PASS | **HARD／不計 KEEP**：皇冠上半露出水面，沒有越過盆緣的溢水；旁白明說整頂沒入、只浸一半會少算，畫面直接反轉實驗條件。人物亦讀作孩童，頂部有黑邊。 |

另一名製作覆看者以三張原生 1280×720 圖獨立判 **0／3 真正可留**；上述判定已採此較保守結論。未達先前收據規定的 **至少 2／3 真正可留** 的全量出圖門檻，維持 STOP，不再購買插圖或開 99 張批次。後續若重啟，先以固定維特魯威文本和旁白設計水線、補水、全浸與溢水都能直接看懂的受控二維示意圖，再獨立審核；此處只記錄非製作中的恢復方向。三張機評 9.29 通過均屬原尺寸驗收的假陽性。站台現行大綱仍待站主，音訊最新版站台卡仍有版次差異；本機委派決定詳見 [verify-7.md](verify-7.md)。
