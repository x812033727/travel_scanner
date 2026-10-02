import { readFileSync } from "node:fs";
import { expect, test as base, type Page } from "@playwright/test";
import messages from "../messages/zh-TW/admin.json" with { type: "json" };
import copy from "../lib/video-plans-messages/zh-TW.json" with { type: "json" };

import { pretendSignedIn } from "./session";

// Use the same packaged authored plans as the API, with a local browser fixture.
// This is UI acceptance, not evidence of a production database import.
type Entry = { catalog: keyof typeof copy.catalogs; id: string; title: string; video_slug: string; stage: keyof typeof copy.stages };
const bundle = JSON.parse(readFileSync(new URL("../../api/app/video_plans/data/catalog.json", import.meta.url), "utf8")) as {
  entries: Entry[]; plans_sha256: string;
};
const test = base.extend<{ readOnlyCatalog: void }>({
  readOnlyCatalog: [async ({ page, baseURL }, use, info) => {
    expect(new URL(baseURL!).hostname).toBe("127.0.0.1");
    const origin = new URL(baseURL!).origin;
    const writes: string[] = [], external: string[] = [], errors: string[] = [], failed: string[] = [];
    page.on("pageerror", (error) => errors.push(error.message));
    page.on("console", (message) => { if (message.type() === "error") errors.push(message.text()); });
    page.on("response", (response) => { if (new URL(response.url()).origin === origin && response.status() >= 400) failed.push(`${response.status()} ${new URL(response.url()).pathname}`); });
    await page.context().route("**/*", (route) => {
      const request = route.request(), url = new URL(request.url());
      if (url.origin !== origin) { external.push(url.origin + url.pathname); return route.abort("blockedbyclient"); }
      if (!["GET", "HEAD", "OPTIONS"].includes(request.method())) { writes.push(`${request.method()} ${url.pathname}`); return route.abort("blockedbyclient"); }
      if (url.pathname === "/api/travel/admin/video-plans") {
        const catalog = url.searchParams.get("catalog"), query = (url.searchParams.get("q") ?? "").toLowerCase();
        const pageNumber = Number(url.searchParams.get("page") ?? 1), size = Number(url.searchParams.get("page_size") ?? 25);
        const matched = bundle.entries.filter((entry) => (!catalog || entry.catalog === catalog) && (!query || `${entry.title} ${entry.id} ${entry.video_slug}`.toLowerCase().includes(query)));
        return route.fulfill({ json: {
          items: matched.slice((pageNumber - 1) * size, pageNumber * size), total: matched.length, page: pageNumber, page_size: size,
          catalog_total: bundle.entries.length, plans_sha256: bundle.plans_sha256,
          catalogs: Object.keys(copy.catalogs).map((catalog) => ({ catalog, count: bundle.entries.filter((entry) => entry.catalog === catalog).length })),
        } });
      }
      return route.continue();
    });
    await pretendSignedIn(page);
    await use();
    await expect.poll(() => page.locator("html").evaluate((node) => node.scrollWidth - node.clientWidth)).toBeLessThanOrEqual(1);
    await page.screenshot({ path: info.outputPath("long-form-plans.png") });
    await info.attach("read-only-catalog-traffic", { body: JSON.stringify({ writes, external, errors, failed }), contentType: "application/json" });
    expect(writes, "Reading plans must not write").toEqual([]);
    expect(external, "Local acceptance must not contact production or media providers").toEqual([]);
    expect(errors, "The catalog must render without browser errors").toEqual([]);
    expect(failed, "First-party reads must succeed").toEqual([]);
  }, { auto: true }],
});
test.use({ serviceWorkers: "block" });

async function selectedPlans(page: Page) {
  if (page.viewportSize()!.width < 768) {
    await expect(page.getByRole("combobox", { name: messages.videoReviews.tabsLabel, exact: true })).toHaveValue("plans");
  } else {
    await expect(page.getByRole("tab", { name: copy.tab, exact: true })).toHaveAttribute("aria-selected", "true");
  }
  await expect(page.getByRole("region", { name: copy.title, exact: true })).toBeVisible();
}

test("all 473 authored plans are visible; search and catalog survive reload", async ({ page }) => {
  expect(bundle.entries).toHaveLength(473);
  await page.goto("/zh-TW/admin/videos?tab=plans");
  await selectedPlans(page);
  await expect(page.getByText("五類共 473 筆企劃", { exact: true })).toBeVisible();
  await expect(page.getByText(copy.minimum, { exact: true })).toBeVisible();
  const catalog = page.getByRole("combobox", { name: copy.catalog, exact: true });
  await expect(catalog.locator("option")).toHaveText([
    "全部分類 (473)", "原來如此事務所・第一季 (100)", "原來如此事務所・第二季 (92)", "原來如此事務所・第三季 (100)", "品牌故事 (100)", "AI 名詞 (81)",
  ]);
  await expect(page.getByRole("article")).toHaveCount(25);
  await page.getByRole("button", { name: copy.next, exact: true }).click();
  await expect(page.getByText("第 2 頁，共 19 頁", { exact: true })).toBeVisible();
  await catalog.selectOption("season2");
  await expect(page.getByText("符合條件的企劃：92 筆", { exact: true })).toBeVisible();
  await page.getByRole("searchbox", { name: copy.search, exact: true }).fill("B28");
  await page.getByRole("button", { name: copy.searchButton, exact: true }).click();
  const corrected = bundle.entries.find((entry) => entry.catalog === "season2" && entry.id === "B28")!;
  await expect(page.getByRole("heading", { name: corrected.title, exact: true })).toBeVisible();
  expect(corrected.title).toContain("Saks");
  await expect(page.getByRole("article")).toHaveCount(1);
  await page.reload();
  await selectedPlans(page);
  await expect(catalog).toHaveValue("season2");
  await expect(page.getByRole("searchbox", { name: copy.search, exact: true })).toHaveValue("B28");
  await expect(page.getByRole("heading", { name: corrected.title, exact: true })).toBeVisible();
  await page.getByText(copy.details, { exact: true }).click();
  await expect(page.getByRole("heading", { name: copy.detailLabels.effective_inputs, exact: true })).toBeVisible();
  await expect(page.getByText(copy.historical, { exact: true })).toBeVisible();
});

test("candidate and covered plans retain their stages and brand stories retain the 13-minute target", async ({ page }) => {
  await page.goto("/zh-TW/admin/videos?tab=plans&plan_catalog=season3");
  await selectedPlans(page);
  await expect(page.getByText(copy.stages.CHECKED_CANDIDATE_REQUIRES_OUTLINE, { exact: true }).first()).toBeVisible();
  const catalog = page.getByRole("combobox", { name: copy.catalog, exact: true });
  await catalog.selectOption("brand-stories");
  await expect(page.getByText("製作目標：13 分鐘", { exact: true }).first()).toBeVisible();
  await expect(page.getByText(copy.stages.REVIEWED_STORY_PLAN_NOT_MEDIA, { exact: true }).first()).toBeVisible();
  await catalog.selectOption("ai-terms");
  await page.getByRole("searchbox", { name: copy.search, exact: true }).fill("ai-agent");
  await page.getByRole("button", { name: copy.searchButton, exact: true }).click();
  await expect(page.getByText(copy.stages.COVERED_DO_NOT_REMAKE, { exact: true })).toBeVisible();
  await expect(page.getByRole("article")).toHaveCount(1);
  await page.getByText(copy.details, { exact: true }).click();
  await expect(page.getByRole("heading", { name: copy.detailLabels.source_record, exact: true })).toBeVisible();
  for (const reference of ["ai-agent-vs-chatbot", "ai-agents-explained-what-they-cost", "always-on-agent-explained"]) {
    await expect(page.getByRole("article")).toContainText(reference);
  }
  await expect(page.getByText("製作目標：10 分鐘", { exact: true })).toHaveCount(0);
  await expect(page.getByText(copy.readOnly, { exact: true })).toBeVisible();
});
