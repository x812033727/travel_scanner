import { expect, test } from "@playwright/test";

test("primary travel flow is visible", async ({ page }) => {
  await page.goto("/");
  await expect(page.getByRole("heading", { name: /少開十個分頁/ })).toBeVisible();
  await expect(page.getByRole("button", { name: /比較完整旅程/ })).toBeVisible();
  await page.getByRole("link", { name: "方案" }).click();
  await expect(page.getByRole("heading", { name: /搜尋點數/ })).toBeVisible();
});

test("airline public fare lab is available", async ({ page }) => {
  await page.goto("/labs/airlines");
  await expect(page.getByRole("heading", { name: /三家航空/ })).toBeVisible();
  await expect(page.getByRole("button", { name: "搜尋公開票價" })).toBeVisible();
  await expect(page.getByText("中華航空")).toBeVisible();
  await expect(page.getByText("長榮航空")).toBeVisible();
  await expect(page.getByText("星宇航空")).toBeVisible();
});
