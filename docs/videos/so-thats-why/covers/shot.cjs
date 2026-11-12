const { chromium } = require('playwright');
(async () => { const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 3000, height: 3800 } });
 await p.goto('file://' + __dirname + '/cover.html'); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(800);
 await (await p.$('#pl')).screenshot({ path: __dirname + '/playlist-cover.png' });
 await (await p.$('#pod')).screenshot({ path: __dirname + '/podcast-cover.png' }); await b.close(); })();
