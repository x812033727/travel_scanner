/** Original teaching diagrams. They are not product UI or execution evidence. */
import { mkdir, writeFile } from 'node:fs/promises';
import { createRequire } from 'node:module';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = fileURLToPath(new URL('../../', import.meta.url));
const require = createRequire(path.join(root, 'apps/web/package.json'));
const { chromium } = require('@playwright/test');
const lessons = [
  ['dots 完整教學', '從入門到六個實際應用', ['認識功能', '逐步操作', '成果核對']],
  ['dots 是什麼', '把持續工作交給代理', ['目標', '持續跟進', '成果']],
  ['建立你的 dot', '先確認入口與使用條件', ['桌面建立', '個人化', '首次交辦']],
  ['第一次交辦', '把完成條件寫清楚', ['資料與目標', '工作界線', '可核對成果']],
  ['記憶與接續', '追加資料，修正已有工作', ['原始資料', '變更內容', '更新結果']],
  ['串接 Google 與 Slack', '三種連接，分別設定', ['App 工具', '聯絡通道', '電腦存取']],
  ['雲端與本機', '查看環境，接管再交還', ['雲端電腦', '本機連接', '工作環境']],
  ['Activity 與委派', '開啟工作，核對實際成果', ['交辦', '委派工作', '檢查產物']],
  ['排程與事件', '指定時間、期限與通知', ['觸發條件', '實際執行', '修改或取消']],
  ['跨裝置聯絡', '同一個 dot，接續工作', ['ChatGPT', '通話與手機', 'Slack']],
  ['控制與除錯', '分別處理三種工作狀態', ['主工作', '委派任務', '未來排程']],
  ['三日旅遊規劃', '限制、預算與來源都留下', ['旅遊條件', '行程與來源', '變更核對']],
  ['會議準備助理', '從測試信件整理待決事項', ['測試信件', '會議資料', '準備文件']],
  ['營運報表更新', '獨立重算，再比對更新', ['交易資料', '分析報表', '差異核對']],
  ['七日學習計畫', '可執行的練習與追蹤', ['學習目標', '每日練習', '追蹤與調整']],
  ['四週內容企劃', '資料、月曆與草稿一致', ['研究來源', '內容月曆', '修訂草稿']],
  ['專案追蹤與週報', '把期限變更轉成下一步', ['會議紀錄', '待辦與依賴', '更新週報']],
];
const escape = (text) => text.replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('>', '&gt;');
function svg(number, diagram = false) {
  const [title, subtitle, cards] = lessons[number];
  const label = number ? `第 ${String(number).padStart(2, '0')} 課` : '課程總目錄';
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 900" width="1600" height="900" role="img" aria-label="${escape(title)}原創教學圖解">
<rect width="1600" height="900" fill="#f7f1e8"/>
<rect x="0" y="0" width="18" height="900" fill="#176d69"/>
<g font-family="Microsoft JhengHei, Noto Sans TC, sans-serif" fill="#173d3e">
<text x="95" y="104" font-size="27" letter-spacing="5">MOKAAIR · OPENAI DOTS</text>
<rect x="95" y="150" width="190" height="50" rx="25" fill="#176d69"/><text x="190" y="184" font-size="24" text-anchor="middle" fill="#ffffff">${label}</text>
<text x="95" y="300" font-size="64" font-weight="700">${escape(title)}</text>
<text x="98" y="365" font-size="32" fill="#426463">${escape(subtitle)}</text>
${cards.map((card, index) => `<g><rect x="${95 + index * 490}" y="460" width="430" height="245" rx="24" fill="${index === 1 ? '#173d3e' : '#e0ece7'}"/>
<text x="${130 + index * 490}" y="525" font-size="27" fill="${index === 1 ? '#4fc1b5' : '#176d69'}">0${index + 1}</text>
<text x="${130 + index * 490}" y="611" font-size="36" font-weight="700" fill="${index === 1 ? '#ffffff' : '#173d3e'}">${escape(card)}</text>
</g>${index < 2 ? `<path d="M${540 + index * 490},580h30m-12,-12l12,12l-12,12" fill="none" stroke="#176d69" stroke-width="4"/>` : ''}`).join('')}
<text x="98" y="810" font-size="22" fill="#426463">${diagram ? '概念圖解 · 不代表產品介面或實測結果' : '繁體中文 · 逐步操作 · 可下載練習素材'}</text>
</g></svg>`;
}

const browser = await chromium.launch({ headless: true, channel: process.env.DOTS_ART_BROWSER || 'msedge' });
const page = await browser.newPage({ viewport: { width: 1600, height: 900 }, deviceScaleFactor: 1 });
await page.route('**/*', (route) => route.abort());
const records = [];
try {
  for (let number = 0; number <= 16; number++) {
    const slug = number ? `dots-lesson-${String(number).padStart(2, '0')}` : 'dots-guide';
    const directory = path.join(root, 'apps/web/public/guides', slug);
    await mkdir(directory, { recursive: true });
    for (const name of ['hero', 'diagram-1']) {
      const source = svg(number, name === 'diagram-1');
      await writeFile(path.join(directory, `${name}.svg`), source, 'utf8');
      await page.setContent(`<meta charset="utf-8"><style>html,body{margin:0}svg{display:block}</style>${source}`);
      await page.evaluate(() => document.fonts.ready);
      const clipping = await page.locator('svg text').evaluateAll((nodes) => nodes.flatMap((node) => {
        const r = node.getBoundingClientRect();
        return r.x < 0 || r.y < 0 || r.right > 1600 || r.bottom > 900 ? [node.textContent] : [];
      }));
      if (clipping.length) throw new Error(`${slug}/${name}: clipped labels ${clipping.join(', ')}`);
      if (name === 'hero') await page.screenshot({ path: path.join(directory, 'hero.png') });
      records.push({ number, slug, name, clipped_labels: [], original_diagram: true, product_ui: false });
    }
  }
  // Review sheet is an internal QA artifact, never a lesson screenshot.
  await page.setViewportSize({ width: 1800, height: 1340 });
  await page.setContent(`<meta charset="utf-8"><style>body{margin:16px;background:#d9dfdd;font-family:sans-serif}.grid{display:grid;grid-template-columns:repeat(4,1fr);gap:14px}.cell svg{width:100%;height:auto;display:block}.label{padding:4px;font-size:18px}</style><div class="grid">${lessons.map((_, number) => `<div class="cell">${svg(number)}<div class="label">${number ? `dots-lesson-${String(number).padStart(2, '0')}` : 'dots-guide'}</div></div>`).join('')}</div>`);
  await page.evaluate(() => document.fonts.ready);
  const reviewDirectory = process.env.DOTS_ART_REVIEW_DIR || 'C:/Users/x8120/mokaair-work/dots-series/evidence/art';
  await mkdir(reviewDirectory, { recursive: true });
  await page.screenshot({ path: path.join(reviewDirectory, 'contact-sheet.png'), fullPage: true });
  await writeFile(path.join(root, 'docs/dots-series/art-render.json'), `${JSON.stringify({ rendered_at: new Date().toISOString(), status: 'rendered-awaiting-visual-review', records }, null, 2)}\n`);
  console.log(`Rendered ${lessons.length} original covers and ${lessons.length} teaching diagrams.`);
} finally {
  await browser.close();
}
