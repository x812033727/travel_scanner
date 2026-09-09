import { expect, test, type Page } from "@playwright/test";

// Unconfigured flights, lodging and meals remain available in compact disclosures.
async function openOptionalStops(page: Page) {
  const extras = page.locator(".calm-optional-arrangements:not([open]) > summary");
  if (await extras.count()) await extras.click();
  const closed = page.locator(".premium-optional-stop:not([open]) > summary");
  for (let attempt = 0; attempt < 12 && await closed.count() > 0; attempt += 1) await closed.first().click();
  await expect(closed).toHaveCount(0);
}

async function createBlankTrip(page: Page) {
  const created = page.waitForResponse((response) => new URL(response.url()).pathname === "/api/travel/trips" && response.request().method() === "POST");
  await page.getByRole("button", { name: "開始安排", exact: true }).click();
  const response = await created;
  expect(response.status()).toBe(201);
  expect(response.request().postDataJSON()).toMatchObject({
    source: "blank", planning_mode: "manual_blank", routing: { auto_compute: false },
  });
  const trip = await response.json();
  expect(trip.items.filter((item: { system_role?: string }) => item.system_role === "outbound_flight")).toHaveLength(1);
  expect(trip.items.filter((item: { system_role?: string }) => item.system_role === "return_flight")).toHaveLength(1);
  await expect(page).toHaveURL(/\/trips\/[0-9a-f-]+$/, { timeout: 30_000 });
}

test("manual insertion and single-stop cross-day move persist through the real API", async ({ page }) => {
  test.setTimeout(90_000);
  await page.goto("/zh-TW/register?next=/trips");
  await page.getByLabel("Email").fill(`order${Date.now()}${test.info().workerIndex}@example.com`);
  await page.getByLabel("密碼").fill("full-stack-password-123");
  await page.getByRole("button", { name: "建立免費帳號" }).click();
  // Do not match the register URL's ?next=/trips suffix before sign-in finishes.
  await expect(page).toHaveURL((url) => url.pathname === "/zh-TW/trips", { timeout: 15_000 });
  // Use the same-origin session established by the real browser sign-in flow.
  const created = await page.evaluate(async () => {
    const response = await fetch("/api/travel/trips", {
      method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ source: "blank", planning_mode: "manual_blank", name: "直覺排序驗證",
        destination_name: "日本東京", start_date: "2026-11-11", end_date: "2026-11-12" }),
    });
    return { status: response.status, body: await response.json() };
  });
  expect(created.status, JSON.stringify(created.body)).toBe(201);
  const trip = created.body;
  const readTrip = () => page.evaluate(async (id: string) => {
    const response = await fetch(`/api/travel/trips/${id}`);
    if (!response.ok) throw new Error(`Trip reload failed: ${response.status}`);
    return response.json();
  }, trip.id);
  const nextLunch = trip.items.find((item: { day_date: string; system_role: string }) => item.day_date === "2026-11-12" && item.system_role === "lunch").id;
  await page.goto(`/zh-TW/trips/${trip.id}`);
  await page.getByRole("button", { name: "加入第一個地點", exact: true }).click();
  const picker = page.getByRole("dialog", { name: "下一站想去哪裡？" });
  await expect(picker.getByRole("tab", { name: "我的收藏" })).toBeVisible();
  await picker.getByRole("button", { name: "自行填寫行程" }).click();
  await page.getByLabel("安排名稱").fill("只有一站也能移動");
  await page.getByRole("radio", { name: "固定時間", exact: true }).click();
  await page.getByLabel("固定開始時間").fill("10:00");
  await page.getByRole("button", { name: "加入行程" }).click();
  await page.getByLabel("只有一站也能移動 的更多操作", { exact: true }).click();
  await page.getByRole("button", { name: "移動 只有一站也能移動", exact: true }).click();
  const move = page.getByRole("dialog", { name: "移動這個行程" });
  await move.getByLabel("日期").selectOption("2026-11-12");
  await move.getByLabel("插入位置").selectOption(nextLunch);
  const saved = page.waitForResponse((response) => response.url().endsWith("/itinerary") && response.request().method() === "PUT" && response.status() === 200);
  await move.getByRole("button", { name: "移到這裡" }).click();
  await saved;
  await expect.poll(async () => {
    const state = await readTrip();
    return state.items.find((item: { title: string }) => item.title === "只有一站也能移動")?.day_date;
  }).toBe("2026-11-12");
  await page.reload();
  await page.getByRole("button", { name: /DAY 2/ }).click();
  const card = page.locator(".planner-itinerary-card").filter({ hasText: "只有一站也能移動" });
  await expect(card).toContainText("固定時間 · 10:00");
  const persisted = await readTrip();
  const day = persisted.items.filter((item: { day_date: string }) => item.day_date === "2026-11-12");
  expect(day.map((item: { system_role: string }) => item.system_role)).toEqual(["hotel_start", null, "lunch", "dinner", "hotel_end", "return_flight"]);
});

// The trip calendar only renders one month; walk forward until the day exists.
async function pickTripDay(page: Page, iso: string) {
  const toggle = page.getByRole("group", { name: "旅行日期", exact: true }).getByRole("button");
  if (await toggle.getAttribute("aria-expanded") !== "true") await toggle.click();
  const day = page.locator(`[data-date="${iso}"]`);
  const nextMonth = page.getByRole("button", { name: "下個月" });
  // The calendar fills its public holidays in after it mounts, and the phone layout keeps
  // fixed furniture at both edges of the viewport, so let the page settle and put the
  // button in the middle of the screen before aiming at it. The wait needs its own
  // timeout: `networkidle` never arrives on this page in some environments, and without
  // one the catch below never runs — the wait quietly eats the whole test timeout and the
  // failure is reported against the next line, as if the month buttons were stuck.
  await page.waitForLoadState("networkidle", { timeout: 5_000 }).catch(() => {});
  for (let attempt = 0; attempt < 24 && (await day.count()) === 0; attempt += 1) {
    await nextMonth.evaluate((element) => element.scrollIntoView({ block: "center" }));
    await nextMonth.click();
  }
  await day.evaluate((element) => element.scrollIntoView({ block: "center" }));
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
  await page.getByRole("button", { name: "開啟旅程工具" }).click();
  const tripTools = page.getByRole("dialog", { name: "旅程工具" });
  await expect(tripTools).toBeVisible();
  await tripTools.getByRole("button", { name: /^旅行準備/ }).click();
  // The trip-level watch tracks the quotes the trip actually holds, one alert each,
  // instead of a total_price nothing re-checks.
  await tripTools.getByRole("button", { name: /^追蹤這趟旅程的 \d+ 筆報價$/ }).click();
  await expect(tripTools.getByText(/已追蹤 \d+ 筆報價/)).toBeVisible();
  await tripTools.getByRole("link", { name: "前往管理" }).click();

  await expect(page.getByRole("heading", { name: "價格通知" })).toBeVisible();
  // One alert per quote, so every assertion below belongs to one card rather than the list.
  const alertCard = page.locator("article.account-app-card").first();
  // The capacity line above the list also says 追蹤中 (追蹤中 1／20 筆價格通知); match the status pill exactly.
  await expect(alertCard.getByText("追蹤中", { exact: true })).toBeVisible();
  await alertCard.getByRole("button", { name: /編輯/ }).click();
  await alertCard.getByLabel(/編輯.*目標價格/).fill("30000");
  await alertCard.getByRole("button", { name: "儲存價格" }).click();
  await expect(alertCard.getByText(/30,000/)).toBeVisible();
  await alertCard.getByRole("button", { name: /暫停/ }).click();
  await expect(alertCard.getByText("已暫停")).toBeVisible();
  // Deleting re-renders the list, so wait for the row to be gone before opening the next
  // confirm — otherwise the second 確定刪除 is detached mid-click.
  const deleteButtons = page.getByRole("button", { name: "刪除通知" });
  for (let left = await deleteButtons.count(); left > 0; left -= 1) {
    await deleteButtons.first().click();
    await page.getByRole("button", { name: "確定刪除" }).first().click();
    await expect(deleteButtons).toHaveCount(left - 1);
  }
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

  await page.locator(".calm-new-trip-name > summary").click();
  await page.getByLabel("旅程名稱").fill("東京固定餐食行程");
  await page.getByLabel("目的地").fill("日本東京");
  await pickTripDay(page, "2026-11-10");
  await pickTripDay(page, "2026-11-10");
  await expect(page.getByRole("group", { name: "旅行日期", exact: true }).getByRole("button")).toContainText("1 天");
  await createBlankTrip(page);

  const systemCards = page.locator(".planner-system-card");
  const flightCards = page.locator(".planner-flight-card");
  await expect(systemCards).toHaveCount(0);
  await expect(flightCards).toHaveCount(2);
  await openOptionalStops(page);
  await expect(flightCards.first()).toContainText("去程航班尚未設定");
  await expect(flightCards.last()).toContainText("回程航班尚未設定");
  await expect(page.getByRole("button", { name: "尚未設定主要飯店", exact: true })).toBeVisible();
  await expect(page.getByText("住宿據點 · 返回", { exact: true })).toHaveCount(0);
  await expect(page.getByRole("button", { name: "午餐尚未安排", exact: true })).toBeVisible();
  await expect(page.getByRole("button", { name: "晚餐尚未安排", exact: true })).toBeVisible();

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

  await page.getByRole("button", { name: "加入第一個地點", exact: true }).click();
  await page.getByRole("button", { name: "自行填寫行程" }).click();
  await page.getByLabel("安排名稱").fill("東京手動散步");
  await page.getByRole("button", { name: "加入行程" }).click();
  const generalCard = page.locator(".planner-itinerary-card").first();
  await expect(generalCard).toContainText("時間待確認");
  await generalCard.getByLabel("東京手動散步 的更多操作", { exact: true }).click();
  await generalCard.getByRole("button", { name: /^編輯 / }).click();
  await page.getByRole("radio", { name: "固定時間" }).click();
  await page.getByLabel("固定開始時間").fill("15:00");
  await page.getByRole("dialog", { name: "編輯安排" }).getByRole("button", { name: "儲存修改" }).click();
  await expect(generalCard).toContainText("固定時間 · 15:00");

  await openOptionalStops(page);
  await page.getByRole("button", { name: "尚未設定主要飯店", exact: true }).click();
  // The hotel card now opens the stay-area flow first; the manual editor is one click away.
  await page.getByRole("dialog", { name: "住宿熱區" }).getByRole("button", { name: "手動輸入飯店" }).click();
  await page.getByLabel("飯店名稱").fill("丸之內測試飯店");
  await page.getByLabel("飯店地點").fill("東京都千代田區丸之內");
  await page.getByRole("button", { name: "同步所有日期" }).click();
  await expect(page.getByRole("dialog", { name: "設定主要飯店" })).toBeHidden();
  await openOptionalStops(page);
  await expect(systemCards).toHaveCount(2);
  await expect(systemCards.first()).toContainText("丸之內測試飯店");
  await expect(page.getByText("住宿據點 · 返回", { exact: true })).toBeVisible();

  await page.getByRole("button", { name: "略過用餐" }).first().click();
  await openOptionalStops(page);
  await expect(page.getByRole("button", { name: "恢復用餐" })).toBeVisible();
  await expect(page.locator(".calm-day-panel .planner-system-card").filter({ hasText: "午餐" })).toHaveCount(0);
  const tripId = new URL(page.url()).pathname.split("/").pop()!;
  const readLunch = () => page.evaluate(async (id) => {
    const response = await fetch(`/api/travel/trips/${id}`);
    const state = await response.json();
    return state.items.find((item: { system_role?: string }) => item.system_role === "lunch");
  }, tripId);
  await expect.poll(async () => (await readLunch()).is_skipped).toBe(true);
  expect((await readLunch()).fixed_time).toBe(true);

  await page.reload();
  await expect(flightCards).toHaveCount(2);
  await openOptionalStops(page);
  await expect(flightCards.first()).toContainText("長榮航空 BR 198");
  await expect(flightCards.last()).toContainText("長榮航空 BR 197");
  await expect(page.getByRole("button", { name: "恢復用餐" })).toBeVisible();
  await page.getByRole("button", { name: "恢復用餐" }).click();
  await expect.poll(async () => (await readLunch()).is_skipped).toBe(false);
  await expect(page.getByRole("button", { name: "午餐尚未安排", exact: true })).toBeVisible();
  await expect(page.getByRole("button", { name: "略過用餐" }).first()).toBeVisible();
});

test("a saved trip searches flights from its own criteria and takes a quote back", async ({ page }) => {
  test.setTimeout(150_000);
  const email = `tripsearch${Date.now()}${test.info().workerIndex}@example.com`;
  await page.goto("/zh-TW/register?next=/trips/new");
  await page.getByLabel("Email").fill(email);
  await page.getByLabel("密碼").fill("full-stack-password-123");
  await page.getByRole("button", { name: "建立免費帳號" }).click();
  await expect(page).toHaveURL(/\/trips\/new$/, { timeout: 15_000 });

  await page.locator(".calm-new-trip-name > summary").click();
  await page.getByLabel("旅程名稱").fill("東京查機票");
  await page.getByLabel("目的地").fill("日本東京");
  await pickTripDay(page, "2026-11-10");
  await pickTripDay(page, "2026-11-14");
  await expect(page.getByRole("group", { name: "旅行日期", exact: true }).getByRole("button")).toContainText("5 天");
  await createBlankTrip(page);
  const tripUrl = page.url();

  // The outbound anchor card is the entry. A blank trip has no home airport yet,
  // so the search page asks once and writes the answer back to the trip.
  // The timeline renders only the selected day; the return anchor is on day 5.
  // Both persisted anchors are asserted against the real create response above.
  await expect(page.locator(".planner-flight-card")).toHaveCount(1);
  await openOptionalStops(page);
  await page.locator(".planner-flight-card").first().getByRole("link", { name: /^查機票 · / }).click();
  await expect(page).toHaveURL(/\/search\?trip_id=/);
  await expect(page.getByRole("heading", { name: "為〈東京查機票〉找機票" })).toBeVisible();
  await page.getByRole("radio", { name: "桃園 TPE" }).click();
  await page.getByRole("button", { name: "儲存出發地" }).click();
  await expect(page.getByText("這趟旅程還沒有出發機場")).toBeHidden();
  await page.getByRole("button", { name: /^確認條件並開始搜尋 · / }).click();
  await expect(page.getByText("分析完成")).toBeVisible({ timeout: 60_000 });

  await page.getByRole("button", { name: "帶入去程" }).first().click();
  await expect(page.getByRole("button", { name: "已帶入去程" })).toBeVisible();
  await page.getByRole("button", { name: "帶入回程" }).first().click();
  await expect(page.getByText("旅程的去程與回程錨點已更新為這筆報價。")).toBeVisible();
  await page.getByRole("link", { name: "回到旅程" }).first().click();
  await expect(page).toHaveURL(tripUrl);
  // The anchor now shows the quote it was created from instead of "尚未設定".
  const outbound = page.locator(".planner-flight-card").first();
  await expect(outbound).not.toContainText("去程航班尚未設定");
  await expect(outbound).toContainText(/報價 NT\$/);

  // The pre-departure loop: the quote on the anchor is what gets watched, and the
  // alert it creates leads back to this trip rather than dead-ending in a list.
  await outbound.getByRole("button", { name: "建立價格通知" }).click();
  await outbound.getByRole("button", { name: "確認建立" }).click();
  await expect(page.getByText(/價格通知已建立/)).toBeVisible();
  await page.getByRole("link", { name: "前往管理" }).click();
  await expect(page.getByRole("heading", { name: "價格通知" })).toBeVisible();
  await page.getByRole("link", { name: "查看旅程" }).first().click();
  await expect(page).toHaveURL(tripUrl);

  // And the anchor's own flight-status lookup arrives prefilled with that flight.
  await page.locator(".planner-flight-card").first().getByRole("link", { name: /^查航班動態 · / }).click();
  await expect(page).toHaveURL(/\/flights\/status\?.*trip_id=/);
  await expect(page.getByLabel("班號")).not.toHaveValue("");
  await expect(page.getByLabel("出發日期")).not.toHaveValue("");
  await expect(page.getByRole("link", { name: "回到旅程" })).toBeVisible();
});
