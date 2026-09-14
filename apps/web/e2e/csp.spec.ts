/**
 * What the Content Security Policy actually stops, and what it still only reports.
 *
 * The strict policy sat in Report-Only for ten days and nobody read the reports, so nobody
 * knew whether promoting it was safe. This suite is the evidence pass that answers that, and
 * it has to keep running: the enforced half is only safe while every script on the site still
 * either carries the request nonce or is injected by one that does, and that is a property a
 * single careless `<script>` in a new page can break.
 *
 * Run it against a production build (`PLAYWRIGHT_SERVE_BUILD=true`) — the development server
 * adds `'unsafe-eval'`, which is exactly the relaxation these cases exist to notice.
 */
import { expect, test, type Page } from "@playwright/test";

type Violation = { directive: string; blocked: string; disposition: string };

declare global {
  interface Window {
    __cspViolations?: Violation[];
    __xssRan?: boolean;
  }
}

/** Browsers report a refusal to the page itself; collecting it is how a run proves a negative. */
async function recordViolations(page: Page) {
  await page.addInitScript(() => {
    window.__cspViolations = [];
    document.addEventListener("securitypolicyviolation", (event) => {
      window.__cspViolations?.push({
        directive: event.effectiveDirective,
        blocked: event.blockedURI,
        disposition: event.disposition,
      });
    });
  });
}

const violations = (page: Page) => page.evaluate(() => window.__cspViolations ?? []);

// One per route family, in the locales that render different bootstraps. Everything here is
// reachable against the e2e runtime API, so a failure is about the policy and not about data.
const ROUTES = [
  "/zh-TW", "/en", "/ja", "/ko", "/zh-CN",
  "/zh-TW/explore", "/zh-TW/search", "/zh-TW/trips", "/zh-TW/trips/new",
  "/zh-TW/hotspots", "/zh-TW/pet-friendly", "/zh-TW/community",
  "/zh-TW/login", "/zh-TW/register", "/zh-TW/account", "/zh-TW/my", "/zh-TW/admin",
];

test("every route loads with no refusal and no report, under either policy", async ({ page }) => {
  await recordViolations(page);
  const seen: { route: string; violation: Violation }[] = [];
  for (const route of ROUTES) {
    await page.goto(route, { waitUntil: "networkidle" });
    for (const violation of await violations(page)) seen.push({ route, violation });
    await page.evaluate(() => { window.__cspViolations = []; });
  }
  // Report-Only violations fail this too, on purpose: they are the only signal that says
  // whether the rest of the policy can be promoted, and a report nobody fails on is a report
  // nobody reads.
  expect(seen).toEqual([]);
});

test("an injected inline handler is refused, not merely reported", async ({ page }) => {
  await recordViolations(page);
  await page.goto("/zh-TW", { waitUntil: "networkidle" });
  // The shape a stored-XSS payload actually takes: markup written into the parsed document,
  // carrying no nonce. Before the enforced policy this ran and was only reported.
  await page.evaluate(() => {
    const host = document.createElement("div");
    host.innerHTML = "<img src=x onerror=\"window.__xssRan = true\">";
    document.body.append(host);
  });
  await expect.poll(() => violations(page).then((found) =>
    found.some((item) => item.directive.startsWith("script-src") && item.disposition === "enforce"),
  )).toBe(true);
  expect(await page.evaluate(() => window.__xssRan === true)).toBe(false);
});

test("a connection to an unlisted host is still only reported", async ({ page }) => {
  await recordViolations(page);
  await page.goto("/zh-TW", { waitUntil: "networkidle" });
  await page.evaluate(() => fetch("https://connect-src-probe.invalid/x").catch(() => undefined));
  // This is the half deliberately left reporting: connect-src names no Google Maps host, so
  // enforcing it would cut the map's own requests the first time a real browser key is set.
  // When someone promotes the rest of the policy, this expectation is what they come and change.
  await expect.poll(() => violations(page).then((found) =>
    found.filter((item) => item.directive === "connect-src"),
  )).not.toEqual([]);
  expect(await violations(page).then((found) =>
    found.filter((item) => item.directive === "connect-src" && item.disposition === "enforce"),
  )).toEqual([]);
});

test("documents carry the enforced policy and static assets keep the baseline", async ({ page }) => {
  const document = await page.goto("/zh-TW");
  const enforced = document?.headers()["content-security-policy"] ?? "";
  expect(enforced).toContain("'strict-dynamic'");
  expect(enforced).toMatch(/script-src [^;]*'nonce-/);
  // proxy.ts replaces the next.config.ts header on documents, so the baseline's own directives
  // have to survive that replacement rather than being quietly dropped.
  for (const directive of ["object-src 'none'", "base-uri 'self'", "form-action 'self' https:", "frame-ancestors 'none'"]) {
    expect(enforced).toContain(directive);
  }
  // The middleware matcher skips files, so these keep the static baseline and never a nonce.
  const asset = await page.goto("/icon.svg");
  expect(asset?.headers()["content-security-policy"]).toBe(
    "frame-ancestors 'none'; object-src 'none'; base-uri 'self'; form-action 'self' https:",
  );
});
