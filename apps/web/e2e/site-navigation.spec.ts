import { expect, test } from "@playwright/test";

/**
 * The grouped header: five groups on a wide screen, each opening its pages on hover, focus or
 * its chevron; the same groups as sections in the phone menu; the AI hub at `/ai` with the old
 * address answering permanently; and the video library playing a video only when asked.
 */

test.beforeEach(async ({ page }) => {
  await page.route("**/api/travel/discovery/status", (route) => route.fulfill({ json: { enabled: false } }));
});

const wide = async (page: import("@playwright/test").Page) =>
  page.evaluate(() => window.matchMedia("(min-width: 1024px)").matches);

test("the header groups open their pages from the chevron and close on Escape", async ({ page }) => {
  await page.goto("/en/videos");
  if (!(await wide(page))) {
    await page.getByRole("button", { name: "Open navigation menu" }).click();
    const sheet = page.getByRole("dialog");
    await expect(sheet.getByRole("link", { name: "AI tools", exact: true })).toHaveAttribute("href", "/en/ai");
    await expect(sheet.getByRole("link", { name: "AI news" })).toBeVisible();
    await expect(sheet.getByRole("link", { name: "Flight status" })).toBeVisible();
    // The grouped sheet must not widen the page on a phone.
    expect(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth)).toBe(true);
    return;
  }
  const header = page.getByRole("navigation", { name: "Primary navigation" });
  const news = header.getByRole("link", { name: "AI news" });
  await expect(news).toBeHidden();
  const toggle = header.getByRole("button", { name: "AI tools menu" });
  await toggle.click();
  await expect(toggle).toHaveAttribute("aria-expanded", "true");
  await expect(news).toBeVisible();
  await page.keyboard.press("Escape");
  await expect(toggle).toHaveAttribute("aria-expanded", "false");
  // Closed although the pointer still rests on the group and focus stays on its button.
  await expect(news).toBeHidden();
  await expect(toggle).toBeFocused();
  await page.mouse.move(0, 400);
  await header.getByRole("link", { name: "AI tools", exact: true }).hover();
  await expect(news).toBeVisible();
});

test("the AI hub has its own address and the old one follows it", async ({ request }) => {
  const old = await request.get("/en/life/topics/ai?sort=curated", { maxRedirects: 0 });
  expect(old.status()).toBe(308);
  expect(new URL(old.headers().location, "http://x").pathname + new URL(old.headers().location, "http://x").search).toBe("/en/ai?sort=curated");
  expect((await request.get("/en/ai")).status()).toBe(200);
});

test("the video library filters by length and plays a video in place", async ({ page }) => {
  await page.goto("/en/videos");
  await expect(page.getByRole("heading", { level: 1, name: "Videos" })).toBeVisible();
  await expect(page.getByRole("heading", { name: "Synthetic tutorial video" })).toBeVisible();
  await expect(page.getByRole("heading", { name: "Synthetic Short" })).toBeVisible();
  await expect(page.locator("iframe")).toHaveCount(0);
  await page.getByRole("button", { name: "Play “Synthetic tutorial video”" }).click();
  await expect(page.locator('iframe[src^="https://www.youtube-nocookie.com/embed/aaaaaaaaaaa"]')).toHaveCount(1);

  await page.getByRole("navigation", { name: "Length" }).getByRole("link", { name: "Shorts" }).click();
  await expect(page).toHaveURL(/\/en\/videos\?kind=shorts$/);
  await expect(page.getByRole("heading", { name: "Synthetic Short" })).toBeVisible();
  await expect(page.getByRole("heading", { name: "Synthetic tutorial video" })).toHaveCount(0);
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth)).toBe(true);
});
