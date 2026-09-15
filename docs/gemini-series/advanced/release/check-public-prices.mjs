/** Public, signed-out price lookup. Never opens checkout or a user browser profile. */
import { chromium } from "playwright";
import { writeFile } from "node:fs/promises";
import path from "node:path";

const url = "https://one.google.com/intl/zh-TW_tw/about/google-ai-plans/";
const browser = await chromium.launch({ headless: true });
let result;
try {
  const page = await browser.newPage({ locale: "zh-TW", viewport: { width: 1280, height: 900 } });
  await page.goto(url, { waitUntil: "domcontentloaded", timeout: 30000 });
  await page.waitForFunction(() => /NT\$\s*[\d,]+/.test(document.body.innerText), undefined, { timeout: 20000 });
  result = await page.evaluate(() => {
    const body = document.body.innerText;
    return { amounts: [...new Set(body.match(/NT\$\s*[\d,]+/g))],
      observations: [...body.matchAll(/NT\$\s*[\d,]+/g)].slice(0, 16).map(match => body.slice(Math.max(0, match.index - 45), match.index + 35).trim()) };
  });
  // Presence of amounts cannot establish plan mapping, billing period or offer terms.
  result.status = "amounts-loaded-review-required";
} catch (error) {
  result = { status: "unavailable", error: error.message.split("\n")[0] };
} finally { await browser.close(); }
const record = { checkedAt: new Date().toISOString(), checkedOn: new Intl.DateTimeFormat("en-CA", { timeZone: "Asia/Taipei" }).format(new Date()), url, method: "Isolated signed-out Chromium, public page after JavaScript price loading", accountCheckoutChecked: false, ...result };
await writeFile(path.join(import.meta.dirname, "public-prices.json"), JSON.stringify(record, null, 2) + "\n");
console.log(JSON.stringify(record));
process.exitCode = 1; // A person must review prices even when public amounts loaded.
