import { expect, test, type Page } from "@playwright/test";

// The trip calendar only renders one month; walk forward until the day exists.
async function pickTripDay(page: Page, iso: string) {
  const day = page.locator(`[data-date="${iso}"]`);
  for (let attempt = 0; attempt < 24 && (await day.count()) === 0; attempt += 1) {
    await page.getByRole("button", { name: "下個月" }).click();
  }
  await day.click();
}

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

  // Registration returns to the same criteria with a resume marker, so the paid
  // search starts on its own instead of asking for the start button a second time.
  await expect(page).toHaveURL(/\/search\?/, { timeout: 15_000 });
  await expect(page.getByText("分析完成")).toBeVisible({ timeout: 60_000 });
  await expect(page).not.toHaveURL(/resume=search/);
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
  // The capacity line above the list also says 追蹤中 (追蹤中 1／20 筆價格通知); match the status pill exactly.
  await expect(page.getByText("追蹤中", { exact: true })).toBeVisible();
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

test("blank trip keeps flight, hotel and meal anchors with two time modes", async ({ page }) => {
  test.setTimeout(120_000);
  const email = `schedule${Date.now()}${test.info().workerIndex}@example.com`;
  await page.goto("/zh-TW/register?next=/trips/new");
  await page.getByLabel("Email").fill(email);
  await page.getByLabel("密碼").fill("full-stack-password-123");
  await page.getByRole("button", { name: "建立免費帳號" }).click();
  await expect(page).toHaveURL(/\/trips\/new$/, { timeout: 15_000 });

  await page.getByLabel("旅程名稱").fill("東京固定餐食行程");
  await page.getByLabel("目的地").fill("日本東京");
  await pickTripDay(page, "2026-11-10");
  await pickTripDay(page, "2026-11-10");
  await expect(page.getByText(/共 1 天/)).toBeVisible();
  await page.getByRole("button", { name: /下一步/ }).click();
  await page.getByRole("button", { name: /下一步/ }).click();
  await page.getByRole("button", { name: /下一步/ }).click();
  await page.getByRole("button", { name: /交給 AI 排好行程/ }).click();
  await expect(page).toHaveURL(/\/trips\/[0-9a-f-]+$/, { timeout: 30_000 });

  const systemCards = page.locator(".planner-system-card");
  const flightCards = page.locator(".planner-flight-card");
  await expect(systemCards).toHaveCount(3);
  await expect(flightCards).toHaveCount(2);
  await expect(flightCards.first()).toContainText("去程航班尚未設定");
  await expect(flightCards.last()).toContainText("回程航班尚未設定");
  await expect(systemCards.first()).toContainText("尚未設定主要飯店");
  await expect(page.getByText("住宿據點 · 返回", { exact: true })).toHaveCount(0);
  await expect(page.getByRole("heading", { name: "午餐尚未安排", exact: true })).toBeVisible();
  await expect(page.getByRole("heading", { name: "晚餐尚未安排", exact: true })).toBeVisible();

  await page.getByRole("button", { name: "設定去程航班" }).click();
  await page.getByLabel("航空公司").fill("長榮航空");
  await page.getByLabel("班號").fill("BR 198");
  await page.getByLabel("出發機場").fill("TPE");
  await page.getByLabel("抵達機場").fill("NRT");
  await page.getByLabel("當地起飛時間").fill("2026-11-10T08:50");
  await page.getByLabel("當地抵達時間").fill("2026-11-10T13:10");
  await page.getByRole("button", { name: "儲存航班" }).click();
  await expect(page.getByRole("dialog", { name: "設定去程航班" })).toBeHidden();
  await expect(flightCards.first()).toContainText("長榮航空 BR 198");

  await page.getByRole("button", { name: "設定回程航班" }).click();
  await page.getByLabel("航空公司").fill("長榮航空");
  await page.getByLabel("班號").fill("BR 197");
  await page.getByLabel("出發機場").fill("NRT");
  await page.getByLabel("抵達機場").fill("TPE");
  await page.getByLabel("當地起飛時間").fill("2026-11-10T20:20");
  await page.getByLabel("當地抵達時間").fill("2026-11-10T23:10");
  await page.getByRole("button", { name: "儲存航班" }).click();
  await expect(flightCards.last()).toContainText("長榮航空 BR 197");

  await page.getByRole("button", { name: /^新增(?:安排)?$/ }).click();
  await page.getByLabel("安排名稱").fill("東京手動散步");
  await page.getByRole("button", { name: "加入行程" }).click();
  const generalCard = page.locator(".planner-itinerary-card").first();
  await expect(generalCard).toContainText("接續前站");
  await generalCard.getByRole("button", { name: /^編輯 / }).click();
  await page.getByRole("radio", { name: "固定時間" }).click();
  await page.getByLabel("固定開始時間").fill("15:00");
  await page.getByRole("dialog", { name: "編輯安排" }).getByRole("button", { name: "關閉" }).click();
  await expect(generalCard).toContainText("固定時間 · 15:00");

  await page.getByRole("button", { name: "設定主要飯店" }).first().click();
  // The hotel card now opens the stay-area flow first; the manual editor is one click away.
  await page.getByRole("dialog", { name: "住宿熱區" }).getByRole("button", { name: "手動輸入飯店" }).click();
  await page.getByLabel("飯店名稱").fill("丸之內測試飯店");
  await page.getByLabel("飯店地點").fill("東京都千代田區丸之內");
  await page.getByRole("button", { name: "同步所有日期" }).click();
  await expect(page.getByRole("dialog", { name: "設定主要飯店" })).toBeHidden();
  await expect(systemCards).toHaveCount(3);
  await expect(systemCards.first()).toContainText("丸之內測試飯店");
  await expect(page.getByText("住宿據點 · 返回", { exact: true })).toHaveCount(0);

  await page.getByRole("button", { name: "跳過" }).first().click();
  await expect(page.getByText("已跳過，不計停留時間與路線")).toBeVisible();
  await expect(systemCards.filter({ hasText: "午餐" })).toContainText("固定時間");
  await expect(systemCards.filter({ hasText: "午餐" })).toHaveClass(/planner-system-card-skipped/);
  await expect(page.getByRole("button", { name: "計算當日路線" })).toBeDisabled();

  await page.reload();
  await expect(flightCards.first()).toContainText("長榮航空 BR 198");
  await expect(flightCards.last()).toContainText("長榮航空 BR 197");
  await expect(page.getByText("已跳過，不計停留時間與路線")).toBeVisible();
  await page.getByRole("button", { name: "恢復" }).click();
  await expect(page.getByRole("heading", { name: "午餐尚未安排", exact: true })).toBeVisible();
  await expect(page.getByRole("button", { name: "跳過" }).first()).toBeVisible();
});
