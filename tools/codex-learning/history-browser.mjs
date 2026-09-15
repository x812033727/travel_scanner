import { chromium, expect } from "@playwright/test";
import { writeFile } from "node:fs/promises";
const browser = await chromium.launch({ channel: "msedge", headless: true });
const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
const cdp = await page.context().newCDPSession(page);
await cdp.send("Emulation.setCPUThrottlingRate", { rate: 4 });
const results = { checkedAt: new Date().toISOString(), environment: `Windows / Edge ${browser.version()} / 4x CPU slowdown`, checks: [], failure: null };
try {
  for (let i = 0; i < 12; i++) {
    await page.goto("http://127.0.0.1:3123/ja/life/codex-learning-hub");
    await expect(page.getByRole("searchbox")).toBeEnabled({ timeout: 30000 });
    await page.getByRole("searchbox").fill("AGENTS.md");
    await page.locator("main select").nth(3).selectOption("D");
    await expect(page).toHaveURL(/unit=D/);
    await page.reload();
    await expect(page.getByRole("searchbox")).toHaveValue("AGENTS.md");
    await expect(page.locator("main select").nth(3)).toHaveValue("D");
    await page.locator("main select").nth(3).selectOption("E");
    await page.goBack();
    await expect(page.locator("main select").nth(3)).toHaveValue("D");
    await expect(page).toHaveURL(/unit=D/);
    results.checks.push(`reload and immediate back ${i + 1}`);
  }
} catch (error) {
  results.failure = { message: error.message, navigation: await cdp.send("Page.getNavigationHistory"), currentUrl: page.url(), unit: await page.locator("main select").nth(3).inputValue() };
  throw error;
} finally {
  await writeFile("docs/codex-learning/evidence/history-browser.json", JSON.stringify(results, null, 2) + "\n");
  await browser.close();
}
console.log(`${results.checks.length} history checks passed`);
