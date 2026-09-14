import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import path from 'node:path';
import { createRequire } from 'node:module';
import { fileURLToPath, pathToFileURL } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, '../../../../..');
const require = createRequire(path.join(root, 'apps/web/package.json'));
const { chromium } = require('playwright');
const browser = await chromium.launch({headless: true});
const observations = [];
const errors = [];
const network = [];
const resultDir = path.join(here, 'verification');
await fs.mkdir(resultDir, {recursive: true});
try {
  for (const width of [360, 1440]) {
    const page = await browser.newPage({viewport: {width, height: 1000}, deviceScaleFactor: 1});
    page.on('pageerror', error => errors.push(String(error)));
    page.on('request', request => {if (/^https?:/.test(request.url())) network.push(request.url());});
    await page.goto(pathToFileURL(path.join(here, 'examples/53/budget-reference.html')).href);
    async function fill(values) {
      for (const [id, value] of Object.entries(values)) await page.locator('#' + id).fill(value);
    }
    for (const [id, values, total, average] of [
      ['B01', {people:'20',price:'350',venue:'2000',reserve:'10'}, 'NT$ 9,900.00','NT$ 495.00'],
      ['B02', {people:'3',price:'99.95',venue:'1000',reserve:'7.5'}, 'NT$ 1,397.34','NT$ 465.78'],
      ['B03', {people:'1',price:'0',venue:'0',reserve:'0'}, 'NT$ 0.00','NT$ 0.00']]) {
      await fill(values);
      assert.equal(await page.locator('#numbers').isVisible(), false);
      await page.getByRole('button', {name:'計算預算'}).click();
      assert.equal(await page.locator('#total').innerText(), total);
      assert.equal(await page.locator('#average').innerText(), average);
      assert.equal(await page.locator('#error').innerText(), '');
      observations.push({width, case:id, total, average, status:'passed'});
    }
    for (const [field, value] of [['people',''],['people','0'],['people','1.5'],['people','10001'],['price','abc'],['price','-1'],['price','1e3'],['price','0.001'],['venue','10000001'],['reserve','101']]) {
      await page.getByRole('button', {name:'重設'}).click();
      await page.locator('#' + field).fill(value);
      await page.getByRole('button', {name:'計算預算'}).click();
      assert.equal(await page.locator('#numbers').isVisible(), false);
      assert.ok((await page.locator('#error').innerText()).length > 0);
      observations.push({width, case:'invalid', field, value, status:'rejected'});
    }
    await page.getByRole('button', {name:'重設'}).click();
    assert.equal(await page.locator('#people').inputValue(), '20');
    assert.equal(await page.locator('#numbers').isVisible(), false);
    assert.equal(await page.locator('#error').innerText(), '');
    await page.locator('#people').focus();
    for (const expected of ['price','venue','reserve']) {
      await page.keyboard.press('Tab');
      assert.equal(await page.evaluate(() => document.activeElement.id), expected);
    }
    await page.keyboard.press('Tab');
    await page.keyboard.press('Enter');
    assert.equal(await page.locator('#total').innerText(), 'NT$ 9,900.00');
    assert.ok(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth));
    await page.screenshot({path:path.join(resultDir, `budget-${width}.png`), fullPage:true});
    observations.push({width, case:'reset-keyboard-no-overflow', status:'passed'});
    await page.close();
  }
  assert.deepEqual(errors, []);
  assert.deepEqual(network, []);
  await fs.writeFile(path.join(resultDir, 'browser-budget.json'), JSON.stringify({checkedOn:'2026-09-14', node:process.version, browser:await browser.version(), kind:'local-authored-html-playwright', observations, errors, network, modelCalls:0, canvasGenerationTested:false}, null, 2) + '\n');
  console.log(JSON.stringify({observations: observations.length, errors, network, canvasGenerationTested:false}));
} finally {
  await browser.close();
}
