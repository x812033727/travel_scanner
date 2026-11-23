import { readFileSync } from "node:fs";
import { expect, test as base } from "@playwright/test";
import copy from "../lib/video-pools-messages/zh-TW.json" with { type: "json" };

import { pretendSignedIn } from "./session";

// Serves the same packaged bundle as the API through a browser fixture that filters the way the API does.
// This is UI acceptance of the single-episode view, not evidence of a production deploy.
type Audience = { score: number; rank: number };
type Core = { id: string; category: string | null; question: string; hook: string; audience: Audience | null };
type Series = { key: string; name: string; revision: string; audience_min: number; counts: Record<string, number>; cores: Core[]; sources: { themes_sha256: string } };
const bundle = JSON.parse(readFileSync(new URL("../../api/app/video_pools/data/pools.json", import.meta.url), "utf8")) as { series: Series[] };
const BRAND = "W-商業與品牌奇聞";
const test = base.extend<{ readOnlyPools: void }>({
  readOnlyPools: [async ({ page, baseURL }, use, info) => {
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
      if (url.pathname === "/api/travel/admin/video-pools") {
        return route.fulfill({ json: { series: bundle.series.map((series) => ({ key: series.key, name: series.name, revision: series.revision, counts: series.counts, audience_min: series.audience_min, themes_sha256: series.sources.themes_sha256 })) } });
      }
      const match = /^\/api\/travel\/admin\/video-pools\/([^/]+)\/cores$/.exec(url.pathname);
      if (match) {
        const series = bundle.series.find((entry) => entry.key === match[1])!;
        const status = url.searchParams.get("status") ?? "passing", category = url.searchParams.get("category");
        const minimum = Number(url.searchParams.get("min_score") ?? 0), query = (url.searchParams.get("q") ?? "").toLowerCase();
        const pageNumber = Number(url.searchParams.get("page") ?? 1), size = Number(url.searchParams.get("page_size") ?? 25);
        const inStatus = series.cores.filter((core) => status === "all" || (status === "unscored" ? !core.audience : core.audience && (status === "scored" || core.audience.score >= series.audience_min)));
        const matched = inStatus
          .filter((core) => (!category || core.category === category) && (!minimum || (core.audience && core.audience.score >= minimum)) && (!query || `${core.id} ${core.question} ${core.hook}`.toLowerCase().includes(query)))
          .sort((a, b) => Number(!a.audience) - Number(!b.audience) || (a.audience?.rank ?? 0) - (b.audience?.rank ?? 0) || a.id.localeCompare(b.id));
        const facets = new Map<string, number>();
        for (const core of inStatus) if (core.category) facets.set(core.category, (facets.get(core.category) ?? 0) + 1);
        return route.fulfill({ json: {
          items: matched.slice((pageNumber - 1) * size, pageNumber * size), total: matched.length, page: pageNumber, page_size: size,
          categories: [...facets].sort(([a], [b]) => a.localeCompare(b)).map(([name, count]) => ({ category: name, count })),
        } });
      }
      return route.continue();
    });
    await pretendSignedIn(page);
    await use();
    await expect.poll(() => page.locator("html").evaluate((node) => node.scrollWidth - node.clientWidth)).toBeLessThanOrEqual(1);
    await page.screenshot({ path: info.outputPath("single-episode-topics.png"), fullPage: true });
    await info.attach("read-only-pools-traffic", { body: JSON.stringify({ writes, external, errors, failed }), contentType: "application/json" });
    expect(writes, "Reading the pools must not write").toEqual([]);
    expect(external, "Local acceptance must not contact production").toEqual([]);
    expect(errors, "The view must render without browser errors").toEqual([]);
    expect(failed, "First-party reads must succeed").toEqual([]);
  }, { auto: true }],
});
test.use({ serviceWorkers: "block" });

test("business and brand topics are reachable from the single-episode view", async ({ page }, info) => {
  const curio = bundle.series.find((series) => series.key === "curio")!;
  const brand = curio.cores.filter((core) => core.category === BRAND && core.audience && core.audience.score >= curio.audience_min);
  expect(brand.length).toBeGreaterThan(0);
  await page.goto("/zh-TW/admin/videos?tab=pools&pool_view=cores");
  await expect(page.getByRole("region", { name: copy.title, exact: true })).toBeVisible();
  await expect(page.getByRole("combobox", { name: copy.viewLabel, exact: true })).toHaveValue("cores");
  await expect(page.getByText(copy.coreResults.replace("{count}", String(curio.counts.cores_passing)), { exact: true })).toBeVisible();
  await expect(page.getByRole("article")).toHaveCount(25);
  const category = page.getByRole("combobox", { name: copy.category, exact: true });
  await category.selectOption(BRAND);
  await expect(page.getByText(copy.coreResults.replace("{count}", String(brand.length)), { exact: true })).toBeVisible();
  const top = [...brand].sort((a, b) => a.audience!.rank - b.audience!.rank)[0];
  await expect(page.getByRole("article").first().getByRole("heading")).toHaveText(top.question);
  await expect(page.getByRole("article").first().getByText(top.id, { exact: true })).toBeVisible();
  await page.reload();
  await expect(category).toHaveValue(BRAND);
  await expect(page.getByRole("article")).toHaveCount(Math.min(25, brand.length));
  await page.screenshot({ path: info.outputPath("business-and-brand.png"), fullPage: true });
  // The other series has no stand-alone topics; it says so instead of failing.
  await page.getByRole("combobox", { name: copy.seriesLabel, exact: true }).selectOption("so-thats-why");
  await expect(page.getByText(copy.coreEmpty, { exact: true })).toBeVisible();
});
