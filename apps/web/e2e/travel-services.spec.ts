import { expect, test, type BrowserContext } from "@playwright/test";
import en from "../messages/en/travelServices.json" with { type: "json" };
import ja from "../messages/ja/travelServices.json" with { type: "json" };
import ko from "../messages/ko/travelServices.json" with { type: "json" };
import tw from "../messages/zh-TW/travelServices.json" with { type: "json" };
import cn from "../messages/zh-CN/travelServices.json" with { type: "json" };
import { klookAffiliateCopy } from "../lib/klook-affiliate-copy";

const catalogs = { en, ja, ko, "zh-TW": tw, "zh-CN": cn };

for (const [locale, copy] of Object.entries(catalogs)) {
  test(`${locale} Klook direct hotel booking stays separate from destination discovery`, async ({ page, context }) => {
    await mock(context, false, false, true);
    const modules: string[] = [];
    const priceRequests: string[] = [];
    page.on("request", (request) => {
      if (request.url().includes("hotel-quotes")) priceRequests.push(request.url());
    });
    await context.route("**/api/travel/travel-services?**", (route) => route.fulfill({
      json: { ...results, items: [{ ...items[0], offers: [], booking_options: [
        { id: "klook-option", provider: "klook", name: "Klook", mode: "affiliate", quote_status: "not_configured" },
        { id: "booking-option", provider: "booking", name: "Booking.com", mode: "direct", quote_status: "not_configured" },
      ] }] },
    }));
    await context.route("**/api/travel/affiliates/destination-offers?**", (route) => {
      const serviceModule = new URL(route.request().url()).searchParams.get("module") || "";
      modules.push(serviceModule);
      return route.fulfill({ json: {
        destination_id: "tokyo", module: serviceModule, disclosure: copy.disclosure,
        options: [{ id: `klook-${serviceModule}`, brand: "klook", display_name: "Klook", cta: `Klook ${serviceModule}`, clickout_url: `/api/travel/affiliates/destination-offers/klook-${serviceModule}/clickout` }],
      } });
    });
    await page.goto(`/${locale}/destinations/tokyo/services?type=hotel`);
    const discovery = page.getByRole("region", { name: new RegExp(klookAffiliateCopy(locale).discover) });
    await expect(discovery).toBeVisible();
    await expect(discovery.getByText(klookAffiliateCopy(locale).discoveryHint)).toBeVisible();
    expect(modules).toEqual(["hotel"]);
    await page.getByRole("button", { name: copy.platforms }).click();
    const panel = page.getByRole("dialog", { name: items[0].title });
    const klook = panel.getByRole("button", { name: /Klook/ });
    await expect(klook).toHaveCount(1);
    await expect(panel.getByRole("button", { name: /Booking.com/ })).toHaveCount(1);
    await expect(panel.getByText(copy.quoteNotConfigured)).toBeVisible();
    await expect(panel.locator('input[type="date"]')).toHaveCount(0);
    await expect(klook.locator("..")).toHaveAttribute("action", /booking-options\/klook-option\/clickout/);
    await expect(klook.locator("..")).toHaveAttribute("method", "post");
    await expect(klook.locator("..")).toHaveAttribute("rel", "noopener noreferrer");
    const box = await klook.boundingBox();
    expect(box?.height).toBeGreaterThanOrEqual(44);
    const popupWait = context.waitForEvent("page");
    await klook.click();
    const popup = await popupWait;
    await expect(popup).toHaveTitle("Fixture partner page");
    expect(await popup.evaluate(() => window.opener === null)).toBe(true);
    await popup.close();
    await page.keyboard.press("Escape");
    await expect(panel).toHaveCount(0);
    await expect(page.getByRole("button", { name: copy.platforms })).toBeFocused();
    expect(priceRequests).toEqual([]);
  });

  test(`${locale} Klook discovery follows day tour transfer and connectivity filters`, async ({ page, context }) => {
    await mock(context);
    const requests: string[] = [];
    await context.route("**/api/travel/travel-services?**", (route) => route.fulfill({ json: { ...results, items: [] } }));
    await context.route("**/api/travel/affiliates/destination-offers?**", (route) => {
      const serviceModule = new URL(route.request().url()).searchParams.get("module") || "";
      requests.push(serviceModule);
      return route.fulfill({ json: {
        destination_id: "tokyo", module: serviceModule, disclosure: copy.disclosure,
        options: [{ id: `klook-${serviceModule}`, brand: "klook", display_name: "Klook", cta: `Klook ${serviceModule}`, clickout_url: `/api/travel/affiliates/destination-offers/klook-${serviceModule}/clickout` }],
      } });
    });
    await page.goto(`/${locale}/destinations/tokyo/services?type=tour`);
    const discovery = page.getByRole("region", { name: new RegExp(klookAffiliateCopy(locale).discover) });
    await expect(discovery.getByRole("button", { name: /Klook activities/ })).toBeVisible();
    expect(requests).toEqual(["activities"]);
    for (const [kind, serviceModule] of [["transfer", "transport"], ["esim", "connectivity"]] as const) {
      await page.getByRole("button", { name: copy[kind], exact: true }).click();
      await expect(discovery.getByRole("button", { name: new RegExp(`Klook ${serviceModule}`) })).toBeVisible();
      await expect(discovery.getByRole("button")).toHaveCount(1);
      await expect(page).toHaveURL(new RegExp(`type=${kind}`));
    }
    expect(requests).toEqual(["activities", "transport", "connectivity"]);
    for (const theme of ["light", "dark"]) {
      await page.evaluate((value) => document.documentElement.setAttribute("data-theme", value), theme);
      expect(await page.evaluate(() => document.documentElement.scrollWidth <= document.documentElement.clientWidth)).toBe(true);
      expect((await discovery.getByRole("button").boundingBox())?.height).toBeGreaterThanOrEqual(44);
    }
    if (locale === "zh-TW") await page.screenshot({ path: `test-results/klook-discovery-${test.info().project.name}.png`, fullPage: true });
    // Filters intentionally replace the current history entry. Verify persistence
    // and back navigation between pages without inventing a filter-history stack.
    await page.reload();
    await expect(discovery.getByRole("button", { name: /Klook connectivity/ })).toBeVisible();
    await page.goto(`/${locale}/destinations/tokyo/services?type=tour`);
    await expect(discovery.getByRole("button", { name: /Klook activities/ })).toBeVisible();
    await page.goBack();
    await expect(discovery.getByRole("button", { name: /Klook connectivity/ })).toBeVisible();
  });
}
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

async function mock(
  context: BrowserContext,
  signedIn = false,
  ordinary = false,
  unified = false,
) {
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
          : unified
            ? {
                ...results,
                items: items.map((item) => ({
                  ...item,
                  offers: [],
                  booking_options: [
                    {
                      id: "option-1",
                      provider: "official",
                      name: null,
                      mode: "direct",
                      quote_status: "not_configured",
                    },
                    {
                      id: "option-2",
                      provider: "booking",
                      name: "Booking.com",
                      mode: "direct",
                      quote_status: "not_configured",
                    },
                    {
                      id: "option-3",
                      provider: "trip_com",
                      name: "Trip.com",
                      mode: "direct",
                      quote_status: "not_configured",
                    },
                  ],
                  facts: {
                    ...item.facts,
                    source_credits: [
                      {
                        title: "Licensed fixture dataset",
                        publisher: "Fixture publisher",
                        url: "https://official.example.com/data",
                        license_name: "CC BY 4.0",
                        license_url:
                          "https://creativecommons.org/licenses/by/4.0/",
                        changes: "Curated hotel locations",
                      },
                    ],
                  },
                })),
              }
            : ordinary
              ? {
                  ...results,
                  items: items.map((item) => ({
                    ...item,
                    offers: [],
                    direct_links: [{ provider: "official", name: null }],
                  })),
                }
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
    } else if (
      path.includes("/hotel-links/") ||
      path.includes("/booking-options/") ||
      path.startsWith("/affiliates/offers")
    ) {
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
    test(`${locale} ${width}px unified hotel panel preserves context and honest external pricing`, async ({
      page,
      context,
    }) => {
      await mock(context, false, false, true);
      await page.setViewportSize({ width, height: 860 });
      await page.goto(
        `/${locale}/destinations/tokyo/services?type=hotel&area=marunouchi`,
      );
      const opener = page.getByRole("button", { name: copy.platforms }).first();
      await opener.click();
      const panel = page.getByRole("dialog", { name: items[0].title });
      await expect(panel).toBeVisible();
      await expect(panel.getByText(copy.quoteNotConfigured)).toBeVisible();
      await expect(panel.locator('input[type="date"]')).toHaveCount(0);
      expect(await page.evaluate(() => document.body.style.overflow)).toBe(
        "hidden",
      );
      const booking = panel.getByRole("button", {
        name: `Booking.com · ${copy.checkPlatformPrice} · ${copy.newTab}`,
      });
      await expect(booking).toHaveCount(1);
      await expect(booking.locator("..")).toHaveAttribute("target", "_blank");
      const popupWait = context.waitForEvent("page");
      await booking.click();
      const popup = await popupWait;
      await expect(popup).toHaveTitle("Fixture partner page");
      expect(await popup.evaluate(() => window.opener === null)).toBe(true);
      await popup.close();
      await expect(page).toHaveURL(/area=marunouchi/);
      for (const theme of ["light", "dark"]) {
        await page.evaluate(
          (value) => document.documentElement.setAttribute("data-theme", value),
          theme,
        );
        expect(
          await panel.evaluate((el) => el.scrollWidth <= el.clientWidth),
        ).toBe(true);
      }
      await panel.locator("summary").click();
      if(locale === "zh-TW" && width === 390) await page.screenshot({path: "test-results/hotel-platform-panel-390-dark.png"});
      await expect(
        panel.getByText("Fixture publisher", { exact: false }),
      ).toBeVisible();
      const last = panel.getByRole("link", {
        name: `CC BY 4.0 · ${copy.newTab}`,
      });
      await last.focus();
      await page.keyboard.press("Tab");
      await expect(panel.locator("button").first()).toBeFocused();
      await page.goBack();
      await expect(panel).toHaveCount(0);
      await expect(opener).toBeFocused();
      await expect(page).toHaveURL(/area=marunouchi/);
      expect(await page.evaluate(() => document.body.style.overflow)).not.toBe(
        "hidden",
      );
      await opener.click();
      await page.keyboard.press("Escape");
      await expect(panel).toHaveCount(0);
    });

    test(`${locale} ${width}px ordinary hotel links do not require affiliate enrollment`, async ({
      page,
      context,
    }) => {
      await mock(context, false, true);
      await page.setViewportSize({ width, height: 860 });
      await page.goto(
        `/${locale}/destinations/tokyo/services?type=hotel&area=marunouchi`,
      );
      await page.getByRole("button", { name: copy.platforms }).first().click();
      await expect(page.getByText(copy.directDisclosure)).toBeVisible();
      await expect(page.getByText(copy.disclosure)).toHaveCount(0);
      const trigger = page.getByRole("button", {
        name: `${copy.officialHotel} · ${copy.ordinaryLink} · ${copy.newTab}`,
      });
      const popupWait = context.waitForEvent("page");
      await trigger.click();
      const popup = await popupWait;
      await expect(popup).toHaveTitle("Fixture partner page");
      expect(await popup.evaluate(() => window.opener === null)).toBe(true);
      await popup.close();
      await expect(page).toHaveURL(/area=marunouchi/);
      await expect(
        page.getByRole("button", { name: copy.selectHotel }).first(),
      ).toBeEnabled();
      for (const theme of ["light", "dark"]) {
        await page.evaluate(
          (value) => document.documentElement.setAttribute("data-theme", value),
          theme,
        );
        expect(
          await page.evaluate(
            () =>
              document.documentElement.scrollWidth <=
              document.documentElement.clientWidth,
          ),
        ).toBe(true);
      }
    });
  }
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
        await page.screenshot({
          path: "test-results/travel-services-mobile-dark.png",
          fullPage: true,
        });
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
  test(`${width}px booking panel back preserves its parent planner sheet`, async ({page, context}) => {
    await mock(context, true, false, true);
    await page.setViewportSize({width, height:860});
    await page.goto("/en/trips/fixture-trip");
    await page.getByRole("button", { name: "Open trip tools", exact: true }).click();
    await page.getByRole("button", { name: /^Travel essentials/ }).click();
    await page.getByRole("button", {name:en.hotel, exact:true}).click();
    const parent = page.getByRole("dialog",{name:en.hotel, exact:true});
    const opener = parent.getByRole("button",{name:en.platforms}).first();
    await opener.click();
    const child = page.getByRole("dialog",{name:items[0].title});
    await expect(child).toBeVisible();
    await page.keyboard.press("Escape");
    await expect(child).toHaveCount(0);
    await expect(parent).toBeVisible();
    await expect(opener).toBeFocused();
    expect(await page.evaluate(()=>document.body.style.overflow)).toBe("hidden");
    await opener.click();
    await page.goBack();
    await expect(child).toHaveCount(0);
    await expect(parent).toBeVisible();
    await page.goBack();
    await expect(parent).toHaveCount(0);
    expect(await page.evaluate(()=>document.body.style.overflow)).toBe("hidden");
    await page.getByRole("dialog", { name: "Trip tools", exact: true }).getByRole("button", { name: "Close", exact: true }).click();
    expect(await page.evaluate(()=>document.body.style.overflow)).not.toBe("hidden");
  });
  test(`${width}px shared planner sheet locks scroll, traps focus and handles back`, async ({
    page,
    context,
  }) => {
    await mock(context, true);
    await page.setViewportSize({ width, height: 860 });
    await page.goto("/en/trips/fixture-trip");
    await page.getByRole("button", { name: "Open trip tools", exact: true }).click();
    await page.getByRole("button", { name: /^Travel essentials/ }).click();
    const trigger = page.getByRole("button", { name: en.hotel, exact: true });
    await expect(trigger).toBeEnabled();
    await trigger.click();
    const dialog = page.getByRole("dialog", { name: en.hotel });
    await expect(dialog).toBeVisible();
    await expect(dialog.getByRole("article")).toHaveCount(3);
    if (width === 390)
      await page.screenshot({ path: "test-results/travel-services-sheet.png" });
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
    expect(await page.evaluate(() => document.body.style.overflow)).toBe("hidden");
    await trigger.click();
    await expect(dialog).toBeVisible();
    await page.keyboard.press("Escape");
    await expect(dialog).toHaveCount(0);
    await expect(page.getByRole("dialog", { name: "Trip tools", exact: true })).toBeVisible();
    await expect(trigger).toBeFocused();
    await page.getByRole("dialog", { name: "Trip tools", exact: true }).getByRole("button", { name: "Close", exact: true }).click();
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
