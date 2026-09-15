
    const form = document.getElementById('calcForm');
    const resBox = document.getElementById('resBox');
    const srAnnouncer = document.getElementById('sr-announcer');
    let resultVisible = false;

    const fields = [
      { id: 'hc', min: 1, max: 10000, reg: /^([1-9]\d{0,3}|10000)$/ },
      { id: 'up', min: 0, max: 10000000, reg: /^(0|[1-9]\d*)(\.\d{1,2})?$/ },
      { id: 'vf', min: 0, max: 10000000, reg: /^(0|[1-9]\d*)(\.\d{1,2})?$/ },
      { id: 'cr', min: 0, max: 100, reg: /^(0|[1-9]\d*)(\.\d{1,2})?$/ }
    ].map(f => ({ 
      ...f, 
      el: document.getElementById(f.id), 
      err: document.getElementById(`${f.id}-err`),
      hintId: `${f.id}-hint`,
      errId: `${f.id}-err`
    }));
    const outs = ['base', 'cont', 'tot', 'avg'].map(id => document.getElementById(`o-${id}`));

    // 將十進位字串（元或百分比）安全地轉為 BigInt 的最小單位（分或基準點）
    function parseToCentsBigInt(str) {
      if (!str) return 0n;
      const parts = str.split('.');
      const intPart = parts[0] || "0";
      // 補齊兩位小數，例如 .5 變 .50，然後取前兩位
      const fracPart = (parts[1] || "").padEnd(2, '0').slice(0, 2);
      return BigInt(intPart + fracPart);
    }

    // 將 BigInt 的分轉回小數點格式的字串（保留兩位小數）
    function formatCents(centsBigInt) {
      const str = centsBigInt.toString();
      const isNeg = str.startsWith('-');
      const absStr = isNeg ? str.slice(1) : str;
      const padded = absStr.padStart(3, '0');
      const intPart = padded.slice(0, -2);
      const fracPart = padded.slice(-2);
      return (isNeg ? '-' : '') + intPart + '.' + fracPart;
    }

    form.addEventListener('input', () => {
      if (resultVisible) {
        resBox.style.display = 'none';
        resultVisible = false;
        srAnnouncer.textContent = '輸入已變更，結果已隱藏，請重新計算';
      }
    });
    
    form.addEventListener('reset', () => {
      resBox.style.display = 'none';
      resultVisible = false;
      fields.forEach(f => { 
        f.err.style.display = 'none'; 
        f.el.setAttribute('aria-invalid', 'false');
        f.el.setAttribute('aria-describedby', f.hintId);
      });
      srAnnouncer.textContent = '表單已重設';
    });

    form.addEventListener('submit', (e) => {
      e.preventDefault();
      let isValid = true;
      let firstErrEl = null;
      let vals = {};

      fields.forEach(f => {
        const val = f.el.value;
        let isOk = f.reg.test(val);
        // 使用 parseFloat 僅作範圍驗證（輸入範圍內安全）
        let num = parseFloat(val);
        if (isOk && (num < f.min || num > f.max)) isOk = false;

        if (!isOk) {
          f.err.style.display = 'block';
          f.el.setAttribute('aria-invalid', 'true');
          f.el.setAttribute('aria-describedby', `${f.hintId} ${f.errId}`);
          isValid = false;
          if (!firstErrEl) firstErrEl = f.el; // 紀錄第一個錯誤欄位
        } else {
          f.err.style.display = 'none';
          f.el.setAttribute('aria-invalid', 'false');
          f.el.setAttribute('aria-describedby', f.hintId);
          // 將有效字串轉為 BigInt
          vals[f.id] = f.id === 'hc' ? BigInt(val) : parseToCentsBigInt(val);
        }
      });

      if (!isValid) {
        resBox.style.display = 'none';
        resultVisible = false;
        srAnnouncer.textContent = '表單有錯誤，請檢查輸入欄位';
        firstErrEl.focus(); // 聚焦第一個錯誤欄位，無障礙友善
        return;
      }

      // 取出 BigInt 變數
      const hc = vals['hc'];
      const up = vals['up']; // 單位：分
      const vf = vals['vf']; // 單位：分
      const cr = vals['cr']; // 單位：萬分之一 (因為 % 且最多兩位小數)

      // 基本費用 = (人數 * 單價) + 場地費
      const base = (hc * up) + vf;
      
      // 備用金 = 基本費用 * 備用金比率 / 10000
      // 套用 BigInt 正數四捨五入公式: (被除數 + 除數/2) / 除數
      const cont = (base * cr + 5000n) / 10000n; 
      
      // 總額 = 基本費用 + 備用金
      const tot = base + cont;
      
      // 平均每人 = 總額 / 人數 (同樣套用四捨五入)
      const avg = (tot + (hc / 2n)) / hc;

      // 格式化輸出
      outs[0].textContent = formatCents(base);
      outs[1].textContent = formatCents(cont);
      outs[2].textContent = formatCents(tot);
      outs[3].textContent = formatCents(avg);
      
      resBox.style.display = 'block';
      resultVisible = true;
      srAnnouncer.textContent = '計算完成，請查看下方結果';
    });
  