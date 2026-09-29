import { expect, test as base, type Locator, type Page, type Request } from "@playwright/test";
import messages from "../messages/zh-TW/admin.json" with { type: "json" };
import { pretendSignedIn } from "./session";

// Read through the real same-origin BFF to tools/e2e-runtime-api.mjs. Nothing in
// this spec supplies API/media responses, uploads, or changes a Shorts setting.
const t = messages.videoShorts;
const reviews = messages.videoReviews;
const states = ["making", "needs_you", "library", "slotted", "scheduled", "published", "missed", "dropped"] as const;
const title = (state: typeof states[number]) => `Synthetic Shorts ${state}`;
const test = base.extend<{ runtimeGuard: void }>({
  runtimeGuard: [async ({ page, baseURL }, use, info) => {
    expect(baseURL, "A local runtime fixture URL is required").toBeTruthy();
    const origin = new URL(baseURL!).origin;
    // pretendSignedIn's owner cookie is deliberately restricted to this host.
    expect(new URL(origin).hostname).toBe("127.0.0.1");
    const errors: string[] = [], failedResponses: string[] = [], external: string[] = [], writes: string[] = [];
    page.on("pageerror", (error) => errors.push(error.message));
    page.on("console", (message) => { if (message.type() === "error") errors.push(message.text()); });
    page.on("response", (response) => {
      if (new URL(response.url()).origin === origin && response.status() >= 400) {
        failedResponses.push(`${response.status()} ${new URL(response.url()).pathname}`);
      }
    });
    await page.context().route("**/*", (route) => {
      const request = route.request(), url = new URL(request.url());
      if (url.origin !== origin) {
        external.push(url.origin + url.pathname);
        return route.abort("blockedbyclient");
      }
      if (!["GET", "HEAD", "OPTIONS"].includes(request.method())) {
        writes.push(`${request.method()} ${url.pathname}`);
        return route.abort("blockedbyclient");
      }
      return route.continue();
    });
    await pretendSignedIn(page);
    // Fix dates without stopping React's timers, media loading or polling.
    await page.clock.setFixedTime(new Date("2026-10-05T03:00:00Z"));
    await use();
    await expect.poll(() => page.locator("html").evaluate((node) => node.scrollWidth - node.clientWidth)).toBeLessThanOrEqual(1);
    await page.screenshot({ path: info.outputPath("synthetic-shorts.png"), fullPage: true });
    await info.attach("runtime-traffic", { body: JSON.stringify({ errors, failedResponses, external, writes }, null, 2), contentType: "application/json" });
    expect(failedResponses, "All first-party reads must succeed").toEqual([]);
    expect(errors, "No browser or console errors").toEqual([]);
    expect(external, "Synthetic fixture must not contact other origins").toEqual([]);
    expect(writes, "Reading Shorts must not write").toEqual([]);
  }, { auto: true }],
});
test.use({ timezoneId: "Asia/Taipei", serviceWorkers: "block", trace: "retain-on-failure" });

async function selectedTab(page: Page, label: string, name: string, value: string) {
  if (page.viewportSize()!.width < 768) {
    await expect(page.getByRole("combobox", { name: label, exact: true })).toHaveValue(value);
  } else {
    await expect(page.getByRole("tablist", { name: label, exact: true }).getByRole("tab", { name, exact: true })).toHaveAttribute("aria-selected", "true");
  }
}

async function openShorts(page: Page) {
  const uploads = page.waitForResponse((response) => new URL(response.url()).pathname === "/api/travel/admin/video-shorts/uploads" && response.ok());
  await page.goto("/zh-TW/admin/videos?tab=shorts&from=2026-10-05");
  // SSR initially renders Reviews. Wait for the hydrated URL selection and data.
  await selectedTab(page, reviews.tabsLabel, reviews.tabShorts, "shorts");
  await expect(page.getByRole("region", { name: t.top.title, exact: true }).getByText(t.top.channelNotAudited, { exact: true })).toBeVisible();
  await uploads;
  await expect(page.getByRole("region", { name: t.uploads.title, exact: true })).toBeVisible();
}

async function openView(page: Page, view: keyof typeof t.views) {
  if (page.viewportSize()!.width < 768) {
    await page.getByRole("combobox", { name: t.viewsLabel, exact: true }).selectOption(view);
  } else {
    await page.getByRole("tablist", { name: t.viewsLabel, exact: true }).getByRole("tab", { name: t.views[view], exact: true }).click();
  }
  await selectedTab(page, t.viewsLabel, t.views[view], view);
}

async function portrait(locator: Locator) {
  await expect(locator).toBeVisible();
  const size = await locator.boundingBox();
  expect(size).not.toBeNull();
  expect(size!.width / size!.height).toBeCloseTo(9 / 16, 2);
  return size!;
}

async function openProject(page: Page, card: Locator, state: typeof states[number]) {
  const slug = `synthetic-shorts-${state.replaceAll("_", "-")}`;
  const requests = new Set<Request>();
  const started = (request: Request) => {
    // Library cards read this same endpoint. Only a request made after the URL
    // selected this detail can prove that the detail's own data has arrived.
    if (new URL(request.url()).pathname === `/api/travel/admin/videos/${slug}` && new URL(page.url()).searchParams.get("video") === slug) requests.add(request);
  };
  page.on("request", started);
  try {
    const loaded = page.waitForResponse((response) => requests.has(response.request()));
    await card.click();
    const response = await loaded;
    expect(response.ok()).toBe(true);
    expect(await response.finished()).toBeNull();
    await expect(page.getByRole("heading", { name: title(state), exact: true })).toBeVisible();
  } finally {
    page.off("request", started);
  }
}

test("calendar distinguishes skipped and empty slots and filters each fortnight", async ({ page }) => {
  await openShorts(page);
  await selectedTab(page, t.viewsLabel, t.views.calendar, "calendar");
  const calendar = page.getByRole("region", { name: t.views.calendar, exact: true });
  const assigned = calendar.getByRole("listitem", { name: "2026-10-05 19:30", exact: true });
  await expect(assigned.getByText(title("slotted"), { exact: true })).toBeVisible();
  const skipped = calendar.getByRole("listitem", { name: "2026-10-06 12:30", exact: true });
  await expect(skipped.getByText(t.slotStatuses.skipped, { exact: true })).toBeVisible();
  await expect(skipped.getByText(t.calendar.emptySlot, { exact: true })).toHaveCount(0);
  const empty = calendar.getByRole("listitem", { name: "2026-10-06 19:30", exact: true });
  await expect(empty.getByText(t.slotStatuses.open, { exact: true })).toBeVisible();
  await expect(empty.getByText(t.calendar.emptySlot, { exact: true })).toBeVisible();
  // The overview has its own rendering of tomorrow's skipped/open slots.
  const tomorrow = page.getByRole("region", { name: t.top.title, exact: true }).locator("dt").filter({ hasText: t.top.tomorrow }).locator("..");
  await expect(tomorrow.getByText(t.slotStatuses.skipped, { exact: true })).toBeVisible();
  await expect(tomorrow.getByText(t.top.emptySlot, { exact: true })).toHaveCount(1);
  await expect(calendar.getByRole("listitem", { name: "2026-10-20 19:30", exact: true })).toHaveCount(0);

  const laterResponse = page.waitForResponse((response) => {
    const url = new URL(response.url());
    return url.pathname === "/api/travel/admin/video-shorts/slots" && url.searchParams.get("from") === "2026-10-19" && url.searchParams.get("to") === "2026-11-01";
  });
  await calendar.getByRole("button", { name: t.calendar.later, exact: true }).click();
  const response = await laterResponse;
  expect(response.ok()).toBe(true);
  expect((await response.json()).slots.map((slot: { local_date: string }) => slot.local_date)).toEqual(["2026-10-20"]);
  const later = calendar.getByRole("listitem", { name: "2026-10-20 19:30", exact: true });
  await expect(later.getByText("Synthetic later slot", { exact: true })).toBeVisible();
  await expect(later.getByText(t.slotStatuses.open, { exact: true })).toBeVisible();
  await expect(later.getByText(t.calendar.emptySlot, { exact: true })).toBeVisible();
  await expect(assigned).toHaveCount(0);
  await expect(skipped).toHaveCount(0);
  await expect(empty).toHaveCount(0);
});

test("library renders eight states, loaded portrait covers and a real portrait player", async ({ page }) => {
  await openShorts(page);
  await openView(page, "library");
  const library = page.locator(`div[aria-label="${t.views.library}"]`);
  await expect(library.getByRole("button")).toHaveCount(8);
  for (const state of states) {
    const group = library.getByRole("region", { name: t.library.groups[state], exact: true });
    const card = group.getByRole("button", { name: t.library.open.replace("{title}", title(state)), exact: true });
    await card.scrollIntoViewIfNeeded();
    await expect(card.getByText(title(state), { exact: true })).toBeVisible();
    await expect(card.getByText(t.states[state], { exact: true })).toHaveCount(1);
    const cover = card.getByRole("img", { name: t.library.cover.replace("{title}", title(state)), exact: true });
    await expect.poll(() => cover.evaluate((node: HTMLImageElement) => node.complete && node.naturalWidth > 0)).toBe(true);
    const ratio = await cover.evaluate((node: HTMLImageElement) => node.naturalWidth / node.naturalHeight);
    expect(ratio).toBeCloseTo(9 / 16, 2);
    await portrait(card.getByTestId("shorts-card-cover"));
  }
  await expect.poll(() => page.locator("html").evaluate((node) => node.scrollWidth - node.clientWidth)).toBeLessThanOrEqual(1);
  await openProject(page, library.getByRole("button", { name: t.library.open.replace("{title}", title("library")), exact: true }), "library");
  const heading = page.getByRole("heading", { name: title("library"), exact: true });
  await expect(heading).toBeVisible();
  const header = heading.locator("..").locator("..");
  await expect(header.getByText(t.states.library, { exact: true })).toHaveCount(1);
  await expect(header.getByText(reviews.publishStates.deciding, { exact: true })).toHaveCount(0);
  const history = page.locator("details").filter({ has: page.locator("summary").filter({ hasText: reviews.history }) });
  await expect(history).toHaveCount(1);
  if (!(await history.evaluate((node: HTMLDetailsElement) => node.open))) await history.locator("summary").click();
  const video = page.locator(`video[aria-label="${t.player.title}"]`);
  await expect(video).toBeVisible();
  await expect.poll(() => video.evaluate((node: HTMLVideoElement) => node.readyState >= 1 && node.videoWidth > 0)).toBe(true);
  expect(await video.evaluate((node: HTMLVideoElement) => node.videoWidth / node.videoHeight)).toBeCloseTo(9 / 16, 2);
  const frame = await portrait(page.getByTestId("shorts-frame"));
  expect(frame.height).toBeLessThanOrEqual(page.viewportSize()!.height);
  const source = new URL((await video.getAttribute("src"))!, page.url());
  expect(source.origin).toBe(new URL(page.url()).origin);
  expect(source.pathname).toMatch(/^\/api\/admin-video-files\/synthetic-shorts-library\/[a-f0-9]{64}$/);
  const range = await page.request.get(source.href, { headers: { Range: "bytes=0-15" } });
  expect(range.status()).toBe(206);
  expect(range.headers()["content-range"]).toMatch(/^bytes 0-15\/\d+$/);
  expect((await range.body()).length).toBe(16);
  await page.getByRole("checkbox", { name: t.player.cover, exact: true }).check();
  await expect(page.getByTestId("shorts-cover")).toBeVisible();
  await page.screenshot({ path: test.info().outputPath("synthetic-shorts-player.png"), fullPage: true });

  await page.getByRole("button", { name: reviews.back, exact: true }).click();
  await openProject(page, library.getByRole("button", { name: t.library.open.replace("{title}", title("published")), exact: true }), "published");
  const published = page.getByRole("heading", { name: title("published"), exact: true }).locator("..").locator("..");
  await expect(published.getByText(t.states.published, { exact: true })).toHaveCount(1);
  await expect(published.getByText(reviews.publishStates.published, { exact: true })).toHaveCount(0);
});

test("metrics preserve source values, removed reasons and readable period columns", async ({ page }) => {
  await openShorts(page);
  await openView(page, "metrics");
  const table = page.getByRole("table", { name: t.views.metrics, exact: true });
  await expect(table.locator("tbody tr")).toHaveCount(2);
  await expect(table.getByRole("columnheader")).toHaveText([t.metrics.columns.short, t.metrics.columns.d1, t.metrics.columns.d3, t.metrics.columns.d7, t.metrics.columns.now]);
  const published = table.getByRole("row").filter({ hasText: title("published") });
  const snapshot = published.locator('td[data-period="d1"]');
  await expect(snapshot.locator("dt")).toHaveText([t.metrics.views, t.metrics.likes, t.metrics.comments]);
  await expect(snapshot.locator("dd")).toHaveText(["1,234", "17", "3"]);
  await expect(snapshot.getByText(t.metrics.sources.data_api, { exact: false })).toBeVisible();
  const dropped = table.getByRole("row").filter({ hasText: title("dropped") });
  await expect(dropped.locator('td[data-period="d1"] dl')).toHaveCount(1);
  for (const period of ["d3", "d7", "now"]) {
    await expect(dropped.locator(`td[data-period="${period}"]`)).toHaveText(t.metrics.blank.removed);
  }
  const widths = await table.locator("thead th").evaluateAll((nodes) => nodes.slice(1).map((node) => node.getBoundingClientRect().width));
  expect(Math.min(...widths)).toBeGreaterThan(100);
  // Auto table layout may expand a column for its content. The regression was
  // unreadably squeezed empty periods, not a few pixels of unequal width: these
  // short fixture reasons must fit on one line in both desktop and mobile tables.
  const blankLayout = await table.locator("td > p").evaluateAll((nodes) => nodes.map((node) => {
    const range = document.createRange();
    range.selectNodeContents(node);
    return { text: node.textContent, lines: range.getClientRects().length, height: range.getBoundingClientRect().height, lineHeight: Number.parseFloat(getComputedStyle(node).lineHeight) };
  }));
  expect(blankLayout).toHaveLength(6);
  for (const reason of blankLayout) {
    expect(reason.lines, `${reason.text} must not be squeezed across lines`).toBe(1);
    expect(reason.height).toBeLessThanOrEqual(reason.lineHeight + 1);
  }
  await test.info().attach("metrics-geometry", { body: JSON.stringify({ widths, blankLayout }, null, 2), contentType: "application/json" });
  // Only the two source rows and their original three counts belong in this table;
  // no total/average/rate/ranking rows or columns may be invented by the frontend.
  await expect(table.locator("tfoot")).toHaveCount(0);
});

test("costs retain sub-dollar precision and distinguish unknown amounts from zero", async ({ page }) => {
  await openShorts(page);
  await openView(page, "costs");
  const table = page.getByRole("table", { name: t.costs.itemsTitle, exact: true });
  const confirmed = table.getByRole("row").filter({ hasText: "Synthetic narration" });
  await expect(confirmed.locator("td").nth(2)).toContainText("0.01 USD");
  await expect(confirmed.locator("td").nth(3)).toHaveText("NT$0.29");
  await expect(confirmed.locator("td").nth(4)).toContainText(t.costs.statuses.confirmed);
  const unknown = table.getByRole("row").filter({ hasText: "Synthetic unknown cost" });
  await expect(unknown.locator("td").nth(2)).toHaveText("—");
  await expect(unknown.locator("td").nth(3)).toHaveText("—");
  await expect(unknown.locator("td").nth(4)).toContainText(t.costs.statuses.unknown);
  await expect(table.locator("tbody tr")).toHaveCount(2);
});

test("settings render the stored local fixture without saving or granting consent", async ({ page }) => {
  await openShorts(page);
  await openView(page, "settings");
  await expect(page.getByRole("textbox", { name: t.settings.fields.timezone, exact: true })).toHaveValue("Asia/Taipei");
  for (const [field, value] of [["budget_ntd_30d", "3000"], ["budget_soft_ntd", "2400"], ["budget_total_ntd", "9000"]] as const) {
    await expect(page.getByRole("spinbutton", { name: t.settings.fields[field], exact: true })).toHaveValue(value);
  }
  await expect(page.getByRole("checkbox", { name: t.settings.fields.enabled, exact: true })).not.toBeChecked();
  await expect(page.getByText(t.settings.consent.states.none, { exact: true })).toBeVisible();
  await expect(page.getByRole("button", { name: t.settings.consent.agree, exact: true })).toHaveCount(0);
  await expect(page.getByRole("button", { name: t.settings.save, exact: true })).toBeDisabled();
});
