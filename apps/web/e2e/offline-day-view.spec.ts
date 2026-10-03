import { expect, test, type BrowserContext, type Page } from "@playwright/test";
import { pretendSignedIn } from "./session";

/**
 * The day view opens with no signal after the phone has closed the tab: a cold open, served
 * by `public/sw.js` from what it kept on the last online visit.
 *
 * Measured, not assumed (`tasks/done/2026-09-11-offline-today-e2e.md` found the opposite in
 * Playwright 1.62): `context.setOffline` and `context.route` both reach the worker's own
 * requests here, and the test checks the first of those directly before it relies on it.
 * The trip is routed at the context so that the worker's request for it is answered too,
 * and every route is removed before the network goes away, so nothing but the worker's
 * cache can answer afterwards.
 */

const TRIP_ID = "offline-day-fixture";
const DAY_PATH = `/zh-TW/trips/${TRIP_ID}?view=today`;
const TIMEZONE = "Asia/Tokyo";
const STOP = "Synthetic offline stop";

function isoDay(offset: number) {
  return new Intl.DateTimeFormat("en-CA", { timeZone: TIMEZONE }).format(new Date(Date.now() + offset * 86_400_000));
}

/** Yesterday, today and tomorrow carry the same stop, so a run across midnight still has one today. */
const trip = {
  id: TRIP_ID,
  name: "Synthetic offline trip",
  mode: "custom",
  total_price: 0,
  currency: "JPY",
  data: {},
  version: 1,
  timezone: TIMEZONE,
  items: [-1, 0, 1].map((offset, position) => ({
    id: `stop-${position}`,
    item_type: "activity",
    day_date: isoDay(offset),
    position: 0,
    title: STOP,
    start_time: `${isoDay(offset)}T09:00:00+09:00`,
    end_time: `${isoDay(offset)}T10:00:00+09:00`,
    locked: false,
    is_estimated: false,
    data: {},
  })),
};

/** Whether the worker has kept this day: its document and the trip, in the member's cache. */
function keptDay(page: Page) {
  return page.evaluate(async ({ dayPath, tripPath }) => {
    const name = (await caches.keys()).find((candidate) => candidate.startsWith("mokaair-trip-v2-"));
    if (!name) return false;
    const cache = await caches.open(name);
    return Boolean(await cache.match(dayPath)) && Boolean(await cache.match(tripPath, { ignoreVary: true }));
  }, { dayPath: DAY_PATH, tripPath: `/api/travel/trips/${TRIP_ID}` });
}

/** The scripts and stylesheets a page asked for that the worker's cache does not hold. */
function notKept(page: Page, urls: string[]) {
  return page.evaluate(async (wanted) => {
    const name = (await caches.keys()).find((candidate) => candidate.startsWith("mokaair-trip-v2-"));
    const cache = name ? await caches.open(name) : null;
    const missing: string[] = [];
    for (const url of wanted) if (!cache || !(await cache.match(url, { ignoreVary: true }))) missing.push(url);
    return missing;
  }, urls);
}

async function stopWorkers(context: BrowserContext, page: Page) {
  const session = await context.newCDPSession(page);
  await session.send("ServiceWorker.enable");
  await session.send("ServiceWorker.stopAllWorkers");
  await session.detach();
}

test("the day view opens with no signal after its tab was closed", async ({ context, page }) => {
  await pretendSignedIn(page);
  await context.route(`**/api/travel/trips/${TRIP_ID}`, (route) => route.fulfill({ json: trip }));
  const shell: string[] = [];
  page.on("request", (request) => {
    const url = new URL(request.url());
    if (url.pathname.startsWith("/_next/static/") && /\.(?:js|css)$/.test(url.pathname)) shell.push(url.href);
  });

  await page.goto(DAY_PATH);
  await expect(page.getByRole("heading", { name: trip.name })).toBeVisible();
  await expect.poll(() => keptDay(page), { timeout: 20_000 }).toBe(true);
  // Every script and stylesheet the page loaded online is what a cold open will ask for.
  expect(shell.length).toBeGreaterThan(0);
  expect(await notKept(page, shell)).toEqual([]);

  await context.unrouteAll({ behavior: "ignoreErrors" });
  await context.setOffline(true);
  const [worker] = context.serviceWorkers();
  expect(worker, "the day view registers its worker").toBeTruthy();
  // The worker's own requests fail too; otherwise this test could pass on the network.
  expect(await worker.evaluate(() => fetch("/robots.txt").then(() => "online", () => "offline"))).toBe("offline");

  // The phone closes the tab and the browser stops the idle worker.
  await stopWorkers(context, page);
  await page.close();
  const cold = await context.newPage();
  const failed: string[] = [];
  cold.on("requestfailed", (request) => {
    if (new URL(request.url()).pathname.startsWith("/_next/static/")) failed.push(request.url());
  });

  await cold.goto(DAY_PATH);

  await expect(cold.getByRole("heading", { name: trip.name })).toBeVisible();
  await expect(cold.getByText(STOP).first()).toBeVisible();
  expect(failed).toEqual([]);
  // The planner is not the day view: it is never kept, so there is nothing stale to show.
  await expect(cold.goto(`/zh-TW/trips/${TRIP_ID}`)).rejects.toThrow(/ERR_INTERNET_DISCONNECTED/);
});
