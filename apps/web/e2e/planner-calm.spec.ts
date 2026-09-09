import { expect, test, type Page } from "@playwright/test";
import { pretendSignedIn } from "./session";
import { editorFixture, editorPlaceOptions } from "./fixtures/itinerary-editor";

// Every browser API request is intercepted; fixtures never mutate production or call providers.
async function workspace(page: Page, failSave = false) {
  let trip = structuredClone(editorFixture);
  trip.items = trip.items.map((item) => item.id === "lunch1" ? {
    ...item, position: .5, title: "午餐尚未安排", location_name: "", latitude: null, longitude: null,
    location_source: null, data: { meal_selection_source: "unset" },
  } : item);
  const writes: string[] = [];
  const unexpected: string[] = [];
  let saves = 0;
  await pretendSignedIn(page);
  await page.route("**/api/travel/**", async (route) => {
    const request = route.request();
    const path = new URL(request.url()).pathname;
    if (path.endsWith("/auth/me")) return route.fulfill({ json: { id: "calm-fixture", email: "calm@example.test", role: "user", is_active: true } });
    if (path.endsWith("/place-options")) return route.fulfill({ json: { items: editorPlaceOptions, next_offset: null, context: "destination" } });
    if (path.endsWith("/itinerary") && request.method() === "PUT") {
      writes.push(path); saves += 1;
      if (failSave && saves === 1) return route.fulfill({ status: 503, json: { detail: "Fixture save unavailable" } });
      trip = { ...trip, version: trip.version + 1, items: request.postDataJSON().items };
      return route.fulfill({ json: trip });
    }
    if (path === "/api/travel/trips/intuitive-trip" && request.method() === "GET") return route.fulfill({ json: trip });
    if (request.method() === "GET" && /\/health$/.test(path)) return route.fulfill({ json: { days: [], issues: [] } });
    if (request.method() === "GET" && /\/community\/status$|\/discovery\/status$|\/analytics\/config$/.test(path)) return route.fulfill({ json: { enabled: false } });
    if (request.method() === "GET" && /\/usage$|\/runtime\/public-config$/.test(path)) return route.fulfill({ json: {} });
    if (request.method() === "GET" && /\/saved-items$|\/trips$/.test(path)) return route.fulfill({ json: [] });
    unexpected.push(`${request.method()} ${path}`);
    return route.fulfill({ status: 503, json: { detail: "Unstubbed request blocked" } });
  });
  await page.goto("/zh-TW/trips/intuitive-trip");
  await expect(page.getByRole("heading", { name: trip.name })).toBeVisible();
  return { writes, unexpected, current: () => trip };
}

test("390px first screen prioritizes a real stop and keeps empty slots out of the route", async ({ page }, testInfo) => {
  await page.setViewportSize({ width: 390, height: 844 });
  const state = await workspace(page);
  const card = page.locator('[data-stop-id="asakusa"]');
  await expect(card).toBeVisible();
  const bounds = (await card.boundingBox())!;
  const dock = (await page.locator(".premium-mobile-dock").boundingBox())!;
  expect(bounds.y + bounds.height).toBeLessThan(dock.y);
  await expect(page.getByText("午餐尚未安排", { exact: true })).toBeHidden();
  await expect(page.locator(".calm-connection")).toHaveCount(3);
  await expect(page.locator(".calm-connection")).not.toContainText(["午餐尚未安排"]);
  expect(await page.evaluate(() => document.documentElement.scrollWidth)).toBe(390);
  await page.screenshot({ path: testInfo.outputPath("calm-mobile-first-screen.png") });
  await page.locator(".calm-optional-arrangements > summary").click();
  await expect(page.getByRole("button", { name: "午餐尚未安排", exact: true })).toBeVisible();
  expect(state.writes).toEqual([]);
  expect(state.unexpected).toEqual([]);
});

test("cancel and discard never change the original official place", async ({ page }) => {
  const state = await workspace(page);
  const original = structuredClone(state.current());
  await page.locator('[data-stop-id="asakusa"]').getByRole("heading").click();
  const editor = page.getByRole("dialog", { name: "編輯安排", exact: true });
  await editor.getByLabel("安排名稱", { exact: true }).fill("草稿名稱");
  await editor.getByRole("combobox", { name: "地點", exact: true }).fill("尚未確認的新地點");
  await editor.getByRole("button", { name: "取消", exact: true }).click();
  const guard = page.getByRole("dialog", { name: "保留這次修改嗎？" });
  await guard.getByRole("button", { name: "繼續編輯" }).click();
  await expect(editor.getByLabel("安排名稱", { exact: true })).toHaveValue("草稿名稱");
  expect(state.writes).toEqual([]);
  await editor.getByRole("button", { name: "取消", exact: true }).click();
  await guard.getByRole("button", { name: "捨棄修改" }).click();
  await expect(page.getByRole("dialog")).toHaveCount(0);
  expect(state.current()).toEqual(original);
  expect(state.writes).toEqual([]);
});

test("save failure retains a draft and retry applies only the explicitly saved item", async ({ page }) => {
  const state = await workspace(page, true);
  await page.locator('[data-stop-id="asakusa"]').getByRole("heading").click();
  const editor = page.getByRole("dialog", { name: "編輯安排", exact: true });
  await editor.getByLabel("安排名稱", { exact: true }).fill("淺草慢慢走");
  await editor.getByRole("button", { name: "儲存修改" }).click();
  await expect(editor.getByRole("alert")).toBeVisible();
  await expect(editor.getByLabel("安排名稱", { exact: true })).toHaveValue("淺草慢慢走");
  expect(state.current().version).toBe(1);
  await editor.getByRole("button", { name: "儲存修改" }).click();
  await expect(page.getByRole("dialog")).toHaveCount(0);
  expect(state.current().items.find((item) => item.id === "asakusa")?.title).toBe("淺草慢慢走");
  expect(state.current().items.find((item) => item.id === "asakusa")?.latitude).toBe(35.714);
  expect(state.current().items.filter((item) => item.system_role)).toHaveLength(8);
});

test("catalog selection is a draft and returning retains the query", async ({ page }) => {
  const state = await workspace(page);
  const add = page.locator(".premium-desktop-actions").getByRole("button", { name: "新增安排" });
  if (await add.isVisible()) await add.click();
  else await page.getByRole("toolbar").getByRole("button", { name: "新增安排" }).click();
  const browser = page.getByRole("dialog", { name: "下一站想去哪裡？" });
  await browser.getByRole("textbox", { name: "搜尋地點", exact: true }).fill("淺草");
  await browser.getByRole("button", { name: "選擇 淺草寺" }).click();
  const editor = page.getByRole("dialog", { name: "新增安排", exact: true });
  await expect(editor.getByLabel("安排名稱", { exact: true })).toHaveValue("淺草寺");
  expect(state.writes).toEqual([]);
  await editor.getByRole("button", { name: "返回上一層", exact: true }).click();
  await page.getByRole("dialog", { name: "保留這次修改嗎？" }).getByRole("button", { name: "捨棄修改" }).click();
  await expect(browser.getByRole("textbox", { name: "搜尋地點", exact: true })).toHaveValue("淺草");
  await browser.getByRole("button", { name: "選擇 淺草寺" }).click();
  await editor.getByRole("button", { name: "加入行程", exact: true }).click();
  await expect(page.getByRole("dialog")).toHaveCount(0);
  expect(state.current().items.some((item) => item.title === "淺草寺")).toBe(true);
  expect(state.writes).toHaveLength(1);
  expect(state.unexpected).toEqual([]);
});
