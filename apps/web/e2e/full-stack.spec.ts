import { expect, test } from "@playwright/test";

test("guest recommendation through alert management uses the real first-party stack", async ({ page }) => {
  test.setTimeout(120_000);
  await page.goto("/");
  for (let step = 0; step < 4; step += 1) await page.getByRole("button", { name: /下一步/ }).click();
  await page.getByRole("button", { name: /請 AI 推薦 3 組/ }).click();
  await expect(page.getByRole("heading", { name: "AI 推薦的三組旅行" })).toBeVisible();
  await page.getByRole("button", { name: /用這組條件搜尋/ }).first().click();

  await expect(page.getByRole("link", { name: "登入後開始搜尋" })).toBeVisible();
  await page.getByRole("link", { name: "登入後開始搜尋" }).click();
  await page.getByRole("link", { name: "免費註冊" }).click();
  await expect(page).toHaveURL(/\/register\?next=/);
  await expect(page.getByRole("heading", { name: "建立你的旅行帳號" })).toBeVisible();
  const email = `fullstack${Date.now()}${test.info().workerIndex}@example.com`;
  await page.getByLabel("Email").pressSequentially(email);
  await page.getByLabel("密碼").pressSequentially("full-stack-password-123");
  await expect(page.getByLabel("Email")).toHaveValue(email);
  await expect(page.getByLabel("密碼")).toHaveValue("full-stack-password-123");
  await page.getByLabel("密碼").press("Enter");

  await expect(page).toHaveURL(/\/search\?/, { timeout: 15_000 });
  await page.getByRole("button", { name: "確認條件並開始搜尋" }).click();
  await expect(page.getByText("分析完成")).toBeVisible({ timeout: 60_000 });
  await expect(page.getByText("整趟旅程預估總額").first()).toBeVisible();
  await expect(page.getByRole("button", { name: "儲存並編輯行程" }).first()).toBeVisible();
  await page.getByRole("button", { name: "儲存並編輯行程" }).first().click();

  await expect(page).toHaveURL(/\/trips\/[0-9a-f-]+$/, { timeout: 15_000 });
  await expect(page.getByText(/行程規劃器/)).toBeVisible();
  await page.getByRole("button", { name: "建立價格通知" }).click();
  await page.getByRole("button", { name: "確認建立" }).click();
  await expect(page.getByText(/價格通知已建立/)).toBeVisible();
  await page.getByRole("link", { name: "前往管理" }).click();

  await expect(page.getByRole("heading", { name: "價格通知" })).toBeVisible();
  await expect(page.getByText("追蹤中")).toBeVisible();
  await page.getByRole("button", { name: /編輯/ }).first().click();
  await page.getByLabel(/編輯.*目標價格/).fill("30000");
  await page.getByRole("button", { name: "儲存價格" }).click();
  await expect(page.getByText(/30,000/)).toBeVisible();
  await page.getByRole("button", { name: /暫停/ }).click();
  await expect(page.getByText("已暫停")).toBeVisible();
  await page.getByRole("button", { name: "刪除通知" }).click();
  await page.getByRole("button", { name: "確定刪除" }).click();
  await expect(page.getByText(/目前還沒有價格通知/)).toBeVisible();
});
