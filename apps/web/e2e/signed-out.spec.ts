import { expect, test } from "@playwright/test";

/**
 * A reader who has never signed in should not have requests sent on their behalf that
 * can only be refused. The layout knows there is no session cookie before it renders,
 * so the two providers that used to find out by asking are told instead.
 *
 * `networkidle` is not usable here: the dev server keeps an HMR socket open and never
 * reaches it, so each page is given a fixed moment to send anything it was going to.
 */

const SESSION_CALLS = /\/api\/travel\/(auth\/me|saved-items)/;
const SETTLE_MS = 1200;

test("a signed-out visit never asks who is signed in", async ({ page }) => {
  const asked: string[] = [];
  page.on("request", (request) => {
    if (SESSION_CALLS.test(request.url())) asked.push(request.url());
  });

  for (const route of ["/zh-TW", "/zh-TW/hotspots", "/zh-TW/account"]) {
    await page.goto(route);
    await page.waitForLoadState("load");
    await page.waitForTimeout(SETTLE_MS);
  }

  expect(asked, "no session cookie means nobody to ask about").toEqual([]);
  // The page still knows the answer: /account shows its sign-in notice, not a spinner.
  await expect(page.getByRole("link", { name: "前往登入" })).toBeVisible();
});

test("a session cookie is still verified, because it may have expired", async ({ page, context }) => {
  await context.addCookies([
    { name: "travel_access", value: "expired-token", domain: "127.0.0.1", path: "/" },
  ]);
  const asked: string[] = [];
  page.on("request", (request) => {
    if (SESSION_CALLS.test(request.url())) asked.push(request.url());
  });

  await page.goto("/zh-TW/account");
  await page.waitForLoadState("load");
  await page.waitForTimeout(SETTLE_MS);

  // The cookie says a session existed, not that it is still good, so both calls go out.
  expect(asked.some((url) => url.includes("/auth/me"))).toBe(true);
  expect(asked.some((url) => url.includes("/saved-items"))).toBe(true);
});
