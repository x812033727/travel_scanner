
    const form = document.getElementById('calcForm');
    const resBox = document.getElementById('resBox');
    const fields = [
      { id: 'hc', min: 1, max: 10000, reg: /^([1-9]\d{0,3}|10000)$/ },
      { id: 'up', min: 0, max: 10000000, reg: /^(0|[1-9]\d*)(\.\d{1,2})?$/ },
      { id: 'vf', min: 0, max: 10000000, reg: /^(0|[1-9]\d*)(\.\d{1,2})?$/ },
      { id: 'cr', min: 0, max: 100, reg: /^(0|[1-9]\d*)(\.\d{1,2})?$/ }
    ].map(f => ({ ...f, el: document.getElementById(f.id), err: document.getElementById(`${f.id}-err`) }));
    const outs = ['base', 'cont', 'tot', 'avg'].map(id => document.getElementById(`o-${id}`));

    form.addEventListener('input', () => resBox.style.display = 'none');
    
    form.addEventListener('reset', () => {
      resBox.style.display = 'none';
      fields.forEach(f => { f.el.classList.remove('err'); f.err.style.display = 'none'; });
    });

    form.addEventListener('submit', (e) => {
      e.preventDefault();
      let isValid = true;
      let vals = [];

      fields.forEach(f => {
        const val = f.el.value;
        let isOk = f.reg.test(val);
        let num = parseFloat(val);
        if (isOk && (num < f.min || num > f.max)) isOk = false;

        if (!isOk) {
          f.el.classList.add('err');
          f.err.style.display = 'block';
          isValid = false;
        } else {
          f.el.classList.remove('err');
          f.err.style.display = 'none';
          vals.push(f.id === 'hc' ? parseInt(val, 10) : Math.round(num * 100)); // 轉成分
        }
      });

      if (!isValid) {
        resBox.style.display = 'none';
        return;
      }

      // 進行計算 (分單位)
      const hc = vals[0];
      const base = (hc * vals[1]) + vals[2];
      const cont = Math.round(base * vals[3] / 10000); 
      const tot = base + cont;
      const avg = Math.round(tot / hc);

      // 格式化輸出回元單位
      outs[0].textContent = (base / 100).toFixed(2);
      outs[1].textContent = (cont / 100).toFixed(2);
      outs[2].textContent = (tot / 100).toFixed(2);
      outs[3].textContent = (avg / 100).toFixed(2);
      
      resBox.style.display = 'block';
    });
  