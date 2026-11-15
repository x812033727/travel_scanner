# 《原來如此事務所》P19〈降噪耳機開著，說話聲怎麼還在？〉事實主張表（claims.md）

- **集數代碼**：`sothatswhy-p19-noise-cancelling`
- **核對日期**：2026-11-14

---

### 一、 核心物理學與聲學主張

1. **聲音的本質與聲壓疊加**：
   - 聲音是介質（空氣分子）疏密相間的縱波（壓力波）。
   - 當兩道同頻率、同振幅的聲波在同一空間點相遇時，若相位差 180 度（半個週期，波峰對波谷），合成聲壓為零，稱為「相消干涉（Destructive Interference）」。
   - 出處：Nelson & Elliott (1992), *Active Control of Sound*, Chapter 2.

2. **主動降噪（ANC）的硬體架構**：
   - 降噪耳機通常包含：外側麥克風（Feedforward 前饋）、內側靠近耳膜麥克風（Feedback 反饋）、數位訊號處理器（DSP）、以及微型喇叭單體。
   - 前饋麥克風在外界噪聲傳進耳道前提前捕捉波形；DSP 迅速運算反相波（Inverted Phase）；喇叭在耳膜前播放反相聲波抵消噪音。
   - 出處：Kuo & Morgan (1999), "Active noise control: a tutorial review", *Proceedings of the IEEE*, 87(6): 943-973.

3. **波長與空間「靜音區（Zone of Quiet）」大小**：
   - 聲速在常溫空氣中約為 343 m/s。
   - 100 Hz 低頻噪聲波長達 3.43 公尺，半波長約 1.7 公尺；在耳道幾公分的狹小空間內，全域聲壓幾何分佈均勻，耳機喇叭產生的反相波能在大範圍精準抵消。
   - 2000 Hz 噪聲波長僅 17 公分，半波長 8.5 公分；4000 Hz 波長僅 8.6 公分。只要耳機稍微晃動 1 公分，或耳膜位置相位偏移數十度，相消干涉就會失效甚至變成相長干涉（聲音變大）。
   - 出處：Nelson & Elliott (1992), *Active Control of Sound*, Chapter 8: Active headphones.

4. **運算延遲與聲速的極限賽跑**：
   - 從聲音到達外側麥克風，經由類比數位轉換（ADC）、DSP 數位濾波計算、數位類比轉換（DAC）到喇叭單體震動出聲，硬體固有電氣延遲通常在 10 到 30 微秒（microseconds）之間。
   - 聲波在空氣中傳播 1 公分約需 29 微秒。如果耳機外側麥克風距離耳道入口僅 1–2 公分，留給晶片反應的總時間只有幾十微秒。
   - 低頻波（如 100 Hz，週期 10,000 微秒）對數十微秒的延遲完全免疫（相位差不到 1 度）；高頻波（如 3000 Hz，週期約 333 微秒），幾十微秒的延遲就造成數十度相位誤差。
   - 出處：Hansen et al. (2012), *Active Control of Noise and Vibration*, CRC Press.

5. **週期性規律噪音 vs 非週期突發人聲**：
   - 飛機發動機轟鳴、冷氣壓縮機、捷運鋼軌滾動聲屬於穩定、低頻且具有強烈自相關（Auto-correlation）的週期波形，自適應濾波器（如 FXLMS）能預測下一個週期的波形，提前準備抵消訊號。
   - 人類說話語音包含爆破音（p, t, k）、摩擦音（s, f）與突發語調轉折，基頻在 85–255 Hz，共振峰與諧波跨越 300–4000 Hz，屬於高度非週期性（Non-stationary）隨機訊號，演算法「根本無法預測下一秒說什麼」，只能依賴即時反饋，因而無法被有效消除。
   - 出處：Kuo & Morgan (1999); Widrow & Stearns (1985), *Adaptive Signal Processing*.

6. **被動隔音（Passive Isolation）與人體骨傳導**：
   - 泡棉耳塞、矽膠耳套與封閉式耳罩依據「質量定律（Mass Law）」與多孔材料吸音，對 1000 Hz 以上的高頻阻隔極佳，但對長波長低頻阻隔極差。因此 ANC 與被動隔音剛好形成互補（低頻靠主動抵消，高頻靠物理阻擋）。
   - 當自己或極近距離的人說話時，聲音能量還會透過顱骨與下顎骨振動直接傳遞至內耳耳蝸（骨傳導 Bone Conduction），完全繞過耳道外側的空氣與降噪系統。
   - 出處：Stenfelt & Goode (2005), "Bone-conducted sound: physiological and clinical aspects", *Otology & Neurotology*.
