import { expect, test, type Locator, type Page } from "@playwright/test";
import { pretendSignedIn } from "./session";

/**
 * Two things a reader with tired eyes needs, checked on the rendered page rather
 * than in the stylesheet: text large enough to read, and filled controls whose
 * label is actually visible against the fill.
 *
 * The contrast pass only looks at elements that paint their own opaque
 * background. Walking up the tree for an inherited background guesses wrong on
 * gradients and clipped text (the Mokaair wordmark reads as 1.39 that way), and a
 * guessed failure that nobody can reproduce is worse than no check at all.
 */

const MIN_FONT_PX = 13;
const MIN_CONTRAST = 4.5;

/** One element's own colour against its own background. Both must be opaque. */
async function contrastOf(target: Locator) {
  return target.evaluate((element) => {
    const relativeLuminance = (rgb: number[]) => {
      const channels = rgb.map((value) => {
        const scaled = value / 255;
        return scaled <= 0.03928 ? scaled / 12.92 : ((scaled + 0.055) / 1.055) ** 2.4;
      });
      return 0.2126 * channels[0] + 0.7152 * channels[1] + 0.0722 * channels[2];
    };
    const parse = (value: string) => {
      const parts = /rgba?\(([^)]+)\)/.exec(value)?.[1].split(",").map((part) => Number.parseFloat(part)) ?? [0, 0, 0];
      return [parts[0], parts[1], parts[2]];
    };
    const style = getComputedStyle(element);
    const first = relativeLuminance(parse(style.color));
    const second = relativeLuminance(parse(style.backgroundColor));
    return (Math.max(first, second) + 0.05) / (Math.min(first, second) + 0.05);
  });
}

const routes = ["/zh-TW", "/zh-TW/hotspots", "/zh-TW/foods", "/zh-TW/alerts", "/zh-TW/login", "/zh-TW/trips"];

type Small = { size: number; text: string; at: string };
type Faint = { ratio: number; text: string; color: string; background: string; at: string };

const collect = async (page: Page) =>
  page.evaluate(
    ({ minFont }) => {
      const relativeLuminance = (rgb: number[]) => {
        const channels = rgb.map((value) => {
          const scaled = value / 255;
          return scaled <= 0.03928 ? scaled / 12.92 : ((scaled + 0.055) / 1.055) ** 2.4;
        });
        return 0.2126 * channels[0] + 0.7152 * channels[1] + 0.0722 * channels[2];
      };
      const parse = (value: string) => {
        const match = /rgba?\(([^)]+)\)/.exec(value);
        if (!match) return null;
        const parts = match[1].split(",").map((part) => Number.parseFloat(part));
        return { rgb: [parts[0], parts[1], parts[2]], alpha: parts.length > 3 ? parts[3] : 1 };
      };
      const contrast = (a: number[], b: number[]) => {
        const first = relativeLuminance(a);
        const second = relativeLuminance(b);
        return (Math.max(first, second) + 0.05) / (Math.min(first, second) + 0.05);
      };
      const isVisible = (element: Element) => {
        const box = element.getBoundingClientRect();
        if (box.width < 2 || box.height < 2) return false;
        const style = getComputedStyle(element);
        return style.visibility !== "hidden" && style.display !== "none" && Number.parseFloat(style.opacity || "1") > 0.05;
      };
      const describe = (element: Element) => {
        const parts: string[] = [];
        let node: Element | null = element;
        for (let depth = 0; depth < 3 && node; depth += 1) {
          const classes = typeof node.className === "string" ? node.className.split(/\s+/).filter(Boolean).slice(0, 2).join(".") : "";
          parts.unshift(node.tagName.toLowerCase() + (classes ? `.${classes}` : ""));
          node = node.parentElement;
        }
        return parts.join(" > ").slice(0, 120);
      };

      const small: Small[] = [];
      const faint: Faint[] = [];
      document.querySelectorAll("body *").forEach((element) => {
        if (!isVisible(element)) return;
        const style = getComputedStyle(element);
        const own = Array.from(element.childNodes).filter((node) => node.nodeType === 3 && (node.textContent || "").trim().length > 1);
        const text = own.map((node) => (node.textContent || "").trim()).join(" ").replace(/\s+/g, " ").slice(0, 40);
        if (own.length) {
          const size = Number.parseFloat(style.fontSize);
          if (size < minFont) small.push({ size: Math.round(size * 10) / 10, text, at: describe(element) });
        }
        const background = parse(style.backgroundColor);
        const foreground = parse(style.color);
        if (!own.length || !background || !foreground || background.alpha < 0.95) return;
        const ratio = contrast(foreground.rgb, background.rgb);
        const weight = Number.parseInt(style.fontWeight, 10) || 400;
        const size = Number.parseFloat(style.fontSize);
        const large = size >= 24 || (size >= 18.66 && weight >= 700);
        if (ratio < (large ? 3 : 4.5)) {
          faint.push({ ratio: Math.round(ratio * 100) / 100, text, color: style.color, background: style.backgroundColor, at: describe(element) });
        }
      });
      return { small, faint };
    },
    { minFont: MIN_FONT_PX },
  );

for (const route of routes) {
  test(`${route} keeps text readable`, async ({ page }) => {
    await page.goto(route);
    await page.waitForTimeout(1200);
    const { small, faint } = await collect(page);
    expect(small, `text under ${MIN_FONT_PX}px`).toEqual([]);
    expect(faint, `filled controls under ${MIN_CONTRAST}:1`).toEqual([]);
  });
}

/**
 * The largest text step multiplies every rem in the app, so it is the setting that
 * finds a layout with a fixed width hiding in it. 320px is the narrowest phone the
 * site claims to support.
 */
for (const route of ["/zh-TW", "/zh-TW/hotspots", "/zh-TW/foods", "/zh-TW/alerts", "/zh-TW/login"]) {
  test(`${route} survives the largest text size at 320px`, async ({ page }) => {
    await page.addInitScript(() => {
      try {
        localStorage.setItem("mokaair-text-size", "largest");
      } catch {
        // A blocked storage just means the page renders at the standard size.
      }
    });
    await page.setViewportSize({ width: 320, height: 740 });
    await page.goto(route);
    await page.waitForTimeout(1200);

    const state = await page.evaluate(() => {
      const root = document.documentElement;
      const spilling = Array.from(document.querySelectorAll("body *"))
        .filter((element) => {
          const box = element.getBoundingClientRect();
          if (box.width < 2 || box.height < 2) return false;
          const style = getComputedStyle(element);
          if (style.position === "fixed") return false;
          // A scroll rail is allowed to be wider than the screen; its children are not
          // "spilling", they are scrollable.
          let node: Element | null = element;
          while (node) {
            const nodeStyle = getComputedStyle(node);
            if (nodeStyle.overflowX === "auto" || nodeStyle.overflowX === "scroll") return false;
            node = node.parentElement;
          }
          return box.right > window.innerWidth + 4;
        })
        .slice(0, 5)
        .map((element) => element.tagName.toLowerCase() + "." + String(element.className || "").split(/\s+/).slice(0, 2).join("."));
      return {
        textSize: root.dataset.textSize,
        rootFontSize: getComputedStyle(root).fontSize,
        documentOverflowPx: root.scrollWidth - root.clientWidth,
        spilling,
      };
    });

    // The bootstrap runs in <head>, so the choice is on the element before the first
    // paint rather than after hydration.
    expect(state.textSize).toBe("largest");
    expect(state.rootFontSize).toBe("20px");
    expect(state.documentOverflowPx, `document scrolls sideways; ${state.spilling.join(", ")}`).toBeLessThanOrEqual(0);
    expect(state.spilling).toEqual([]);
  });
}

test("the phone menu opens over the whole screen", async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto("/zh-TW");
  await page.getByRole("button", { name: "開啟導覽選單" }).click();

  const geometry = await page.evaluate(() => {
    const dialog = document.querySelector('[role="dialog"]');
    const overlay = dialog?.parentElement;
    const box = (element: Element | null | undefined) => {
      if (!element) return null;
      const rect = element.getBoundingClientRect();
      return { top: Math.round(rect.top), bottom: Math.round(rect.bottom) };
    };
    return { viewport: window.innerHeight, overlay: box(overlay), dialog: box(dialog), onBody: overlay?.parentElement === document.body };
  });

  // The header paints with backdrop-filter, which makes it the containing block for
  // fixed descendants: rendered inside it, this sheet was laid out in a 68px strip
  // and only its last row was on screen.
  expect(geometry.onBody).toBe(true);
  expect(geometry.overlay?.top).toBe(0);
  expect(geometry.overlay?.bottom).toBe(geometry.viewport);
  expect(geometry.dialog?.bottom).toBe(geometry.viewport);
  expect(geometry.dialog?.top).toBeGreaterThan(0);

  await expect(page.getByRole("radiogroup", { name: "文字大小" })).toBeVisible();
});

test("the phone menu gives focus back to the button that opened it", async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto("/zh-TW");
  const trigger = page.getByRole("button", { name: "開啟導覽選單" });
  await trigger.click();
  await expect(page.getByRole("dialog")).toBeVisible();

  await page.keyboard.press("Escape");

  // Dropping focus on <body> sends a keyboard reader back to the top of the document,
  // three tab stops from where they were.
  await expect(trigger).toBeFocused();
});

test("the admin sidebar shows which page you are on", async ({ page }) => {
  await pretendSignedIn(page);
  await page.route("**/api/travel/auth/me", (route) =>
    route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify({ id: "admin", email: "admin@example.com", is_admin: true }) }),
  );
  await page.route("**/api/travel/admin/dashboard", (route) =>
    route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify({ counts: { hotspots_public: 1, foods_public: 1, users: 1, review_queue: 0 }, quick_actions: [], can_deploy: false }),
    }),
  );
  await page.goto("/zh-TW/admin");
  const current = page.locator('a[aria-current="page"]').first();
  await expect(current).toBeVisible();
  // `a { color: inherit }` written outside a layer used to beat `text-white`, so the
  // current page rendered as ink on ink: a 1:1 pill with no label in it.
  // Session hydration can change the selected link while its color transition
  // is running. Assert the settled, rendered contrast rather than a single
  // interpolated frame; a persistent contrast failure still fails this test.
  await expect.poll(() => contrastOf(current)).toBeGreaterThanOrEqual(MIN_CONTRAST);
});

test("every filter chip is on screen, and a long row says how many it folded away", async ({ page }) => {
  const themes = [
    { slug: "sakura", kind: "season", name: "賞櫻", count: 33, months: [3, 4] },
    { slug: "koyo", kind: "season", name: "賞楓", count: 27, months: [11] },
    { slug: "ski", kind: "season", name: "滑雪", count: 2, months: [1, 2] },
    { slug: "hanabi", kind: "season", name: "花火", count: 2, months: [7, 8] },
    { slug: "illumination", kind: "season", name: "燈飾", count: 7, months: [12] },
    { slug: "snow", kind: "season", name: "賞雪", count: 8, months: [1] },
    { slug: "drugstore", kind: "shop", name: "藥妝", count: 4, months: [] },
    { slug: "electronics", kind: "shop", name: "電器", count: 8, months: [] },
    { slug: "department", kind: "shop", name: "百貨", count: 18, months: [] },
    { slug: "outlet", kind: "shop", name: "Outlet 暢貨中心", count: 3, months: [] },
    { slug: "souvenir", kind: "shop", name: "伴手禮", count: 11, months: [] },
    { slug: "vintage", kind: "shop", name: "二手古著", count: 7, months: [] },
    { slug: "anime", kind: "shop", name: "動漫周邊", count: 12, months: [] },
    { slug: "market", kind: "shop", name: "商店街／市場", count: 27, months: [] },
  ];
  await page.route("**/hotspots/facets*", (route) =>
    route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify({ total: 0, countries: [], cities: [], categories: [], areas: [], themes }),
    }),
  );
  await page.route("**/hotspots/rankings*", (route) =>
    route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify({ scope: "global", scope_key: "all", observed_on: null, window_days: 30, total: 0, has_more: false, next_cursor: null, items: [] }),
    }),
  );
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto("/zh-TW/hotspots");
  const rows = page.locator(".app-chip-row");
  await expect(rows.first()).toBeVisible();

  // The rows used to scroll sideways with `scrollbar-width: none`, so four of the
  // seven season chips were unreachable without a swipe nothing hinted at.
  const overflowing = await rows.evaluateAll((elements) =>
    elements
      .filter((element) => element.scrollWidth > element.clientWidth + 1)
      .map((element) => element.textContent?.replace(/\s+/g, " ").slice(0, 60) ?? ""),
  );
  expect(overflowing, "chip rows must not hide choices sideways").toEqual([]);

  // Eight shop chips is more than fits without burying the ranking, so the row
  // folds — but it says so, and the fold opens.
  const more = page.getByRole("button", { name: /還有 \d+ 個/ });
  await expect(more).toBeVisible();
  await expect(page.getByRole("button", { name: "商店街／市場 27" })).toHaveCount(0);
  await more.click();
  await expect(page.getByRole("button", { name: "商店街／市場 27" })).toBeVisible();

  // "熱門景點搜尋 0" is what a screen reader used to say for the filter button.
  const trigger = page.getByRole("button", { name: /熱門景點搜尋/ });
  await expect(trigger).toHaveAttribute("aria-label", "熱門景點搜尋，目前選了 0 個條件");
});

test("the admin console holds its own controls to the size it publishes", async ({ page }) => {
  await pretendSignedIn(page);
  await page.route("**/api/travel/auth/me", (route) =>
    route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify({ id: "admin", email: "admin@example.com", is_admin: true }) }),
  );
  await page.route("**/api/travel/admin/dashboard", (route) =>
    route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify({ counts: { hotspots_public: 1, foods_public: 1, users: 1, hotspots_pending: 800, merchants_pending: 10, guides_pending: 4 }, quick_actions: [], can_deploy: false }),
    }),
  );
  // Dark mode is where the review badge failed: --coral-soft flips to a dark brown and
  // the literal dark red that used to sit on it measured 2.34:1.
  await page.emulateMedia({ colorScheme: "dark" });
  await page.goto("/zh-TW/admin");

  const badge = page.getByText("814 待審");
  await expect(badge).toBeVisible();
  expect(await contrastOf(badge)).toBeGreaterThanOrEqual(MIN_CONTRAST);

  // The analytics range row was the clearest case on production: five buttons at 36px,
  // and a 24px retry link. Every panel wrote its own py-2, so the tabs, pills and
  // pagination came out between 24px and 39px while the public site holds 44 everywhere.
  await page.route("**/api/travel/admin/analytics/dashboard**", (route) =>
    route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify({
        range: "30d", timezone: "Asia/Taipei", source: "raw",
        summary: { live_sessions_30m: 0, page_views: 1, avg_daily_visitors: 1, sessions: 1, pages_per_session: 1, previous: {}, changes: {} },
        timeseries: [], funnel: [], top_pages: [], referrers: [], utm_sources: [],
        devices: [], locales: [], countries: [], heatmap: [], authoritative: {},
      }),
    }),
  );
  await page.goto("/zh-TW/admin/analytics");
  await expect(page.getByRole("button", { name: "30 天" })).toBeVisible();

  const short = await page.locator(".admin-page button, .admin-page [role='tab']").evaluateAll((elements) =>
    elements
      .filter((element) => {
        const box = element.getBoundingClientRect();
        return box.width > 2 && box.height > 2 && box.height < 44;
      })
      .map((element) => `${Math.round(element.getBoundingClientRect().height)}px ${(element.textContent || "").trim().slice(0, 20)}`),
  );
  expect(short, "admin controls under 44px").toEqual([]);
});
