import { expect, test } from "@playwright/test";

test("guest recommendation through alert management uses the real first-party stack", async ({ page }) => {
  test.setTimeout(120_000);
  await page.goto("/zh-TW");
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
  await page.getByRole("button", { name: /^確認條件並開始搜尋 · / }).click();
  await expect(page.getByText("分析完成")).toBeVisible({ timeout: 60_000 });
  await expect(page.getByText("整趟旅程預估總額").first()).toBeVisible();
  await expect(page.getByRole("button", { name: "儲存並編輯行程" }).first()).toBeVisible();
  await page.getByRole("button", { name: "儲存並編輯行程" }).first().click();

  await expect(page).toHaveURL(/\/trips\/[0-9a-f-]+$/, { timeout: 15_000 });
  const tripTools = page.getByRole("button", { name: "開啟旅程工具" });
  if (test.info().project.name === "mobile-chromium") {
    await expect(tripTools).toBeVisible();
    await tripTools.click();
    await expect(page.getByRole("dialog", { name: "旅程工具" })).toBeVisible();
  } else {
    await expect(page.getByText(/行程規劃器/)).toBeVisible();
  }
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

test("blank trip keeps hotel and meal anchors while lunch bypass survives reload", async ({ page }) => {
  test.setTimeout(120_000);
  const email = `schedule${Date.now()}${test.info().workerIndex}@example.com`;
  await page.goto("/zh-TW/register?next=/trips/new");
  await page.getByLabel("Email").fill(email);
  await page.getByLabel("密碼").fill("full-stack-password-123");
  await page.getByRole("button", { name: "建立帳號" }).click();
  await expect(page).toHaveURL(/\/trips\/new$/, { timeout: 15_000 });

  await page.getByLabel("旅程名稱").fill("東京固定餐食行程");
  await page.getByLabel("目的地").fill("日本東京");
  await page.getByLabel("開始日期").fill("2026-11-10");
  await page.getByLabel("結束日期").fill("2026-11-10");
  await page.getByRole("button", { name: /下一步/ }).click();
  await page.getByRole("button", { name: /下一步/ }).click();
  await page.getByRole("button", { name: /下一步/ }).click();
  await page.getByRole("button", { name: /交給 AI 排好行程/ }).click();
  await expect(page).toHaveURL(/\/trips\/[0-9a-f-]+$/, { timeout: 30_000 });

  const systemCards = page.locator(".planner-system-card");
  await expect(systemCards).toHaveCount(4);
  await expect(systemCards.first()).toContainText("住宿據點 · 出發");
  await expect(systemCards.last()).toContainText("住宿據點 · 返回");
  await expect(page.getByText("午餐", { exact: true })).toBeVisible();
  await expect(page.getByText("晚餐", { exact: true })).toBeVisible();

  await page.getByRole("button", { name: "設定主要飯店" }).first().click();
  await page.getByLabel("飯店名稱").fill("丸之內測試飯店");
  await page.getByLabel("飯店地點").fill("東京都千代田區丸之內");
  await page.getByRole("button", { name: "同步所有日期" }).click();
  await expect(page.getByRole("dialog", { name: "設定主要飯店" })).toBeHidden();
  await expect(systemCards.first()).toContainText("丸之內測試飯店");
  await expect(systemCards.last()).toContainText("丸之內測試飯店");

  await page.getByRole("button", { name: "跳過" }).first().click();
  await expect(page.getByText("已跳過，不計停留時間與路線")).toBeVisible();
  const computeResponse = page.waitForResponse((response) =>
    response.url().includes("/routes/compute-day") && response.request().method() === "POST",
  );
  await page.getByRole("button", { name: "計算當日路線" }).click();
  expect((await computeResponse).ok()).toBe(true);
  await expect(page.getByText(/正在背景計算每一段移動時間/)).toBeVisible();

  await page.reload();
  await expect(page.getByText("已跳過，不計停留時間與路線")).toBeVisible();
  await page.getByRole("button", { name: "恢復" }).click();
  await expect(page.getByText("午餐", { exact: true })).toBeVisible();
  await expect(page.getByRole("button", { name: "跳過" }).first()).toBeVisible();
});
