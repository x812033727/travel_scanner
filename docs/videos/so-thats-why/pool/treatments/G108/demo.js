/* Original toy arithmetic. These are invented records, not observed people. */
(function () {
  'use strict';
  function calculate(aEasy, bEasy) {
    for (const n of [aEasy, bEasy]) {
      if (!Number.isInteger(n) || n < 0 || n > 110 || n % 10 !== 0) throw new Error('Use multiples of ten from 0 to 110');
    }
    const make = (name, easy, easyTenths, hardTenths) => {
      const hard = 110 - easy, easyCorrect = easyTenths * easy / 10, hardCorrect = hardTenths * hard / 10;
      return { name, easy, hard, easyCorrect, hardCorrect, correct: easyCorrect + hardCorrect, total: 110, percent: (easyCorrect + hardCorrect) / 110 * 100 };
    };
    return { a: make('A', aEasy, 9, 2), b: make('B', bEasy, 8, 1) };
  }
  globalThis.simpsonDemo = { calculate };
  if (typeof document === 'undefined') return;
  const inputs = [document.getElementById('a-easy'), document.getElementById('b-easy')];
  function render() {
    const result = calculate(Number(inputs[0].value), Number(inputs[1].value));
    for (const [key, row] of Object.entries(result)) {
      document.getElementById(key + '-weight').textContent = `簡單 ${row.easy} 題 · 難 ${row.hard} 題`;
      document.getElementById(key + '-easy-count').textContent = `${row.easyCorrect} / ${row.easy}` + (row.easy === 0 ? '（此組沒有題目）' : '');
      document.getElementById(key + '-hard-count').textContent = `${row.hardCorrect} / ${row.hard}` + (row.hard === 0 ? '（此組沒有題目）' : '');
      document.getElementById(key + '-count').textContent = `${row.correct} / 110`;
      document.getElementById(key + '-percent').textContent = row.percent.toFixed(1) + '%';
      document.getElementById(key + '-bar').style.width = row.percent + '%';
    }
    const difference = result.a.correct - result.b.correct;
    document.getElementById('conclusion').textContent = difference > 0 ? '合計答對率：A 較高' : difference < 0 ? '合計答對率：B 較高' : '合計答對率：相同';
    document.getElementById('zero-note').hidden = !Object.values(result).some(row => row.easy === 0 || row.hard === 0);
  }
  inputs.forEach(input => input.addEventListener('input', render));
  document.querySelectorAll('[data-preset]').forEach(button => button.addEventListener('click', () => {
    const values = { reversal: [10, 100], matched: [50, 50], exchanged: [100, 10] }[button.dataset.preset];
    inputs.forEach((input, i) => { input.value = values[i]; }); render();
  }));
  render();
}());
