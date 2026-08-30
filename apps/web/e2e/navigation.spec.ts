import { expect, test } from "@playwright/test";

test("primary travel flow is visible", async ({ page }) => {
  await page.goto("/");
  await expect(page.getByRole("heading", { name: /把旅行說出來/ })).toBeVisible();
  await expect(page.getByRole("button", { name: /開始規劃完整旅程/ })).toBeVisible();
  await page.getByRole("link", { name: "方案" }).click();
  await expect(page.getByRole("heading", { name: /搜尋點數/ })).toBeVisible();
});

