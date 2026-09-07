import { expect, test, type BrowserContext } from "@playwright/test";
import en from "../messages/en/travelServices.json" with { type: "json" };
import ja from "../messages/ja/travelServices.json" with { type: "json" };
import ko from "../messages/ko/travelServices.json" with { type: "json" };
import tw from "../messages/zh-TW/travelServices.json" with { type: "json" };
import cn from "../messages/zh-CN/travelServices.json" with { type: "json" };

const catalogs = { en, ja, ko, "zh-TW": tw, "zh-CN": cn };
const config = {
  public_enabled: true,
  enabled_destinations: ["tokyo"],
  enabled_kinds: ["hotel", "transfer", "tour", "esim"],
};
const items = [1, 2, 3, 4].map((id) => ({
  id: `hotel-${id}`,
  kind: "hotel",
  destination_id: "tokyo",
  title: `検証用ホテル・景色を楽しむ滞在 공간이 넓은 숙소 ${id}`,
  source_url: "https://official.example.com",
  distance_km: 1.23,
  reason: "center_distance",
  facts: {
    country_codes: ["JP"],
    languages: [],
    facilities: [],
    tethering: null,
    reference_price: null,
    currency: null,
  },
  offers: [
    { id: "offer-1", brand: "klook", brand_name: "Klook", scope: "product" },
    {
      id: "offer-2",
      brand: "kkday",
      brand_name: "KKday",
      scope: "destination",
    },
  ],
}));
const results = {
  enabled: true,
  enabled_kinds: config.enabled_kinds,
  items,
  areas: [{ code: "marunouchi", names: { en: "Tokyo Station", ja: "東京駅" } }],
  version: 1,
  start_date: "2026-11-11",
  end_date: "2026-11-13",
  selections: [],
};

async function mock(context: BrowserContext, signedIn = false) {
  await context.route("**/api/travel/**", async (route) => {
    const url = new URL(route.request().url());
    const path = url.pathname.replace("/api/travel", "");
    let body: unknown = {};
    let status = 200;
    if (path === "/travel-services/config") body = config;
    else if (path === "/travel-services" || path.endsWith("/travel-services"))
      body =
        url.searchParams.get("type") === "esim"
          ? { ...results, items: [] }
          : results;
    else if (path === "/auth/me") {
      status = signedIn ? 200 : 401;
      body = signedIn
        ? {
            id: "actor-fixture",
            email: "fixture@example.test",
            is_admin: true,
            preferred_locale: "en",
            plan_code: "PRO",
          }
        : { detail: "Sign-in required" };
    } else if (path.startsWith("/saved-items")) {
      status = signedIn ? 200 : 401;
      body = { items: [], detail: "Sign-in required" };
    } else if (path.startsWith("/affiliates/offers")) {
      await route.fulfill({
        status: 200,
        contentType: "text/html",
        body: "<title>Fixture partner page</title><p>Isolated form navigation. The real 303 is tested by API/BFF integration tests.</p>",
      });
      return;
    } else if (path === "/trips/fixture-trip")
      body = {
        id: "fixture-trip",
        name: "Tokyo test journey",
        mode: "manual",
        total_price: 0,
        currency: "TWD",
        version: 1,
        destination_name: "Tokyo",
        start_date: "2026-11-11",
        end_date: "2026-11-13",
        timezone: "Asia/Tokyo",
        data: {},
        items: [],
        route_segments: [],
        share_enabled: false,
      };
    else if (path === "/analytics/config")
      body = { first_party_enabled: false, ga4_enabled: false };
    else if (path.startsWith("/affiliates/options")) body = { options: [] };
    else if (path.startsWith("/runtime/site-visibility"))
      body = {
        hotspots_enabled: true,
        trips_enabled: true,
        alerts_enabled: true,
        pricing_enabled: true,
      };
    else if (
      path.startsWith("/usage-catalog") ||
      path.startsWith("/runtime/ui-text")
    ) {
      await route.continue();
      return;
    }
    await route.fulfill({
      status,
      contentType: "application/json",
      body: JSON.stringify(body),
    });
  });
  await context.route("https://tp.st/**", (route) =>
    route.fulfill({
      contentType: "text/html",
      body: "<title>Fixture partner page</title><p>Isolated test destination. No commission or booking.</p>",
    }),
  );
}

for (const [locale, copy] of Object.entries(catalogs)) {
  for (const width of [320, 390, 1280]) {
    test(`${locale} ${width}px catalog decision facts, disclosure and filter persistence`, async ({
      page,
      context,
    }) => {
      await mock(context);
      await page.setViewportSize({ width, height: 860 });
      await page.goto(
        `/${locale}/destinations/tokyo/services?type=hotel&hotspot_id=fixture`,
      );
      await expect(
        page.getByRole("heading", { name: copy.title }),
      ).toBeVisible();
      await expect(page.getByRole("article")).toHaveCount(3);
      await expect(page.getByText(copy.externalPrices).first()).toBeVisible();
      await page.getByRole("button", { name: copy.platforms }).first().click();
      const exact = page.getByRole("button", {
        name: `Klook · ${copy.productScope} · ${copy.newTab}`,
      });
      await expect(exact).toBeVisible();
      await expect(exact.locator("..")).toHaveAttribute("target", "_blank");
      await expect(exact.locator("..")).toHaveAttribute(
        "rel",
        "noopener noreferrer",
      );
      await expect(page.getByText(copy.disclosure).first()).toBeVisible();
      await expect(page.getByText(copy.destinationScope).first()).toBeVisible();
      const popupWait = context.waitForEvent("page");
      await exact.click();
      const popup = await popupWait;
      await expect(popup).toHaveTitle("Fixture partner page");
      expect(await popup.evaluate(() => window.opener === null)).toBe(true);
      await popup.close();
      await page.getByRole("combobox", { name: copy.radius }).selectOption("5");
      await expect(page).toHaveURL(/radius_km=5/);
      await page.reload();
      await expect(
        page.getByRole("combobox", { name: copy.radius }),
      ).toHaveValue("5");
      await page
        .getByRole("button", { name: copy.viewAll.replace("{count}", "4") })
        .click();
      await expect(page.getByRole("article")).toHaveCount(4);
      expect(
        await page.evaluate(
          () =>
            document.documentElement.scrollWidth <=
            document.documentElement.clientWidth,
        ),
      ).toBe(true);
      await page.evaluate(() =>
        document.documentElement.setAttribute("data-theme", "dark"),
      );
      await expect(page.getByRole("article").last()).toBeVisible();
      if (locale === "zh-TW" && width === 390) {
        await page.screenshot({ path: "test-results/travel-services-mobile-dark.png", fullPage: true });
      }
      expect(
        await page.evaluate(
          () =>
            document.documentElement.scrollWidth <=
            document.documentElement.clientWidth,
        ),
      ).toBe(true);
    });
  }
}

test("visitor intent returns to the same service and filters after sign-in", async ({
  page,
  context,
}) => {
  await mock(context);
  await page.goto("/en/destinations/tokyo/services?type=hotel&area=marunouchi");
  await page
    .getByRole("button", { name: new RegExp(`^${en.save} ·`) })
    .first()
    .click();
  await expect(page).toHaveURL(/\/en\/login\?next=/);
  const target = new URL(page.url()).searchParams.get("next")!;
  expect(target).toContain("/destinations/tokyo/services?");
  expect(target).toContain("area=marunouchi");
  expect(target).toContain("product=hotel-1");
  expect(target).toContain("intent=save");
});

for (const width of [320, 390, 1280]) {
  test(`${width}px shared planner sheet locks scroll, traps focus and handles back`, async ({
    page,
    context,
  }) => {
    await mock(context, true);
    await page.setViewportSize({ width, height: 860 });
    await page.goto("/en/trips/fixture-trip");
    const trigger = page.getByRole("button", { name: en.hotel, exact: true });
    await expect(trigger).toBeEnabled();
    await trigger.click();
    const dialog = page.getByRole("dialog", { name: en.hotel });
    await expect(dialog).toBeVisible();
    await expect(dialog.getByRole("article")).toHaveCount(3);
    if (width === 390) await page.screenshot({ path: "test-results/travel-services-sheet.png" });
    expect(await page.evaluate(() => document.body.style.overflow)).toBe(
      "hidden",
    );
    await dialog.getByRole("button").last().focus();
    await page.keyboard.press("Tab");
    expect(
      await dialog.evaluate((node) => node.contains(document.activeElement)),
    ).toBe(true);
    expect(
      await dialog.evaluate((node) => node.scrollWidth <= node.clientWidth),
    ).toBe(true);
    await page.goBack();
    await expect(dialog).toHaveCount(0);
    await expect(trigger).toBeFocused();
    expect(await page.evaluate(() => document.body.style.overflow)).not.toBe(
      "hidden",
    );
  });
}

test("empty content never fabricates price or availability", async ({
  page,
  context,
}) => {
  await mock(context);
  await page.goto("/en/destinations/tokyo/services?type=esim");
  await expect(page.getByText(en.empty)).toBeVisible();
  await expect(page.getByRole("article")).toHaveCount(0);
});
