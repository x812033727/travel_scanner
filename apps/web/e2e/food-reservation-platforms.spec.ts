import { expect, test, type Page } from "@playwright/test";
import { reservationPlatformDefinitions } from "../lib/reservation-platforms";
import en from "../messages/en/admin.json" with { type: "json" };
import ja from "../messages/ja/admin.json" with { type: "json" };
import ko from "../messages/ko/admin.json" with { type: "json" };
import zhTW from "../messages/zh-TW/admin.json" with { type: "json" };
import zhCN from "../messages/zh-CN/admin.json" with { type: "json" };
import { pretendSignedIn } from "./session";

const catalogs = { en, ja, ko, "zh-TW": zhTW, "zh-CN": zhCN };
const merchantId = "11111111-1111-4111-8111-111111111111";
const tablecheckUrl = "https://www.tablecheck.com/zh-TW/shin-yeh-main-restaurant/reserve/message";
const inlineUrl = "https://inline.app/booking/-Np4PbmnyNDdeWIZzRem:inline-live-3/-Np4PbzfZuNZ-afLExLd?language=zh-tw";
type PlatformRow = { id: string; provider: string; provider_label: string; canonical_url: string | null; localized_urls: Record<string, string>; status: string; checked_at: string; review_note: string | null };

/** Isolated UI data, never sent to the production catalog or a reservation site. */
async function fixture(page: Page, failFirst = false) {
  await pretendSignedIn(page);
  const links: PlatformRow[] = [{ id: "fixture-inline", provider: "inline", provider_label: "inline", canonical_url: inlineUrl, localized_urls: {}, status: "verified", checked_at: "2026-09-10T00:00:00Z", review_note: "Fixture branch identity evidence" }];
  const merchant = {
    id: merchantId, slug: "fixture-taipei-merchant", destination_id: "taipei", country_code: "TW",
    name: "Fixture Taipei restaurant", local_name: "測試餐廳・長い店名・긴 식당 이름", names: {}, resolved_names: {},
    address: "Fixture address", latitude: 25.063, longitude: 121.522,
    coordinate_source_type: "merchant_official", coordinate_source_url: "https://example.test/location",
    coordinate_verified_at: "2026-09-10T00:00:00Z", google_place_id: "ChIJ-fixture-only",
    naver_map_url: null, official_website_url: "https://example.test/restaurant", official_website_verified_at: "2026-09-10T00:00:00Z",
    map_match_status: "verified", review_status: "approved", is_active: true, display_order: 1,
    area: null, area_source: null, categories: [], foods: [], sources: [],
    expected_platform: { provider: "eztable", label: "EZTABLE" },
  };
  const writes: { method: string; path: string; body: Record<string, unknown> }[] = [];
  const fields = () => ({ platform_links: links, platform_link: links[0] ?? null });
  await page.route("**/api/travel/**", async (route) => {
    const request = route.request(), path = new URL(request.url()).pathname.replace("/api/travel", "");
    let body: unknown = { items: [], total: 0, page: 1, pages: 0 };
    if (request.method() !== "GET") {
      const payload = request.postDataJSON() ?? {};
      if (path.startsWith("/admin/")) writes.push({ method: request.method(), path, body: payload });
      if (path === `/admin/foods/merchants/${merchantId}/platform-link` && request.method() === "PUT") {
        if (failFirst && writes.length === 1) {
          await route.fulfill({ status: 409, json: { code: "reservation_platform_version_conflict", detail: "Fixture concurrent review" } });
          return;
        }
        const saved = { ...payload, id: `fixture-${payload.provider}`, provider_label: reservationPlatformDefinitions.find((item) => item.provider === payload.provider)!.label, checked_at: "2026-09-11T00:00:00Z" } as PlatformRow;
        const index = links.findIndex((item) => item.provider === saved.provider);
        if (index < 0) links.push(saved); else links[index] = saved;
        // Including stale facts in the response catches accidental whole-merchant replacement.
        body = { ...merchant, ...fields() };
      } else {
        await route.fulfill({ status: 403, json: { detail: "Unexpected write in isolated fixture" } });
        return;
      }
    } else if (path === "/auth/me") body = { id: "fixture-admin", email: "admin@example.test", is_admin: true, can_deploy: false };
    else if (path === "/analytics/config") body = { first_party_enabled: false, ga4_enabled: false };
    // The workspace keeps its settings tab mounted so drafts survive tab changes.
    // Its snapshot has a providers/audit contract, not the generic paginated list.
    else if (path === "/admin/provider-settings") body = { providers: [], audit: [], encryption_source: "isolated-fixture" };
    else if (path === "/admin/dashboard") body = { counts: {}, can_deploy: false };
    else if (path === "/admin/foods/merchants") body = { items: [{ ...merchant, ...fields() }], total: 1, page: 1, pages: 1, available_platforms: reservationPlatformDefinitions.map(({ provider, label }) => ({ provider, label })) };
    else if (path === `/admin/foods/merchants/${merchantId}/platform-links`) body = fields();
    else if (path === "/foods/cities") body = { total_merchants: 1, countries: [{ code: "TW", name: "Taiwan", merchant_count: 1, cities: [{ id: "taipei", name: "Taipei", country_code: "TW", merchant_count: 1, area_count: 0 }] }] };
    else if (path.startsWith("/runtime/") || path.startsWith("/usage-catalog")) { await route.continue(); return; }
    await route.fulfill({ status: 200, json: body });
  });
  return { writes, links };
}

for (const locale of Object.keys(catalogs) as (keyof typeof catalogs)[]) {
  for (const width of [320, 390, 1280]) {
    test(`${locale} ${width}px platform-only save preserves merchant drafts and independent platforms`, async ({ page }, info) => {
      const copy = catalogs[locale].foodMerchantsPanel;
      await page.setViewportSize({ width, height: 900 });
      await page.emulateMedia({ reducedMotion: "reduce", colorScheme: width === 390 ? "dark" : "light" });
      if (width === 390) await page.addInitScript(() => localStorage.setItem("mokaair-theme", "dark"));
      const { writes, links } = await fixture(page);
      await page.goto(`/${locale}/admin/foods?tab=catalog&section=merchants`);
      await expect(page.getByRole("button", { name: copy.editButton, exact: true })).toBeVisible();
      await page.getByRole("button", { name: copy.editButton, exact: true }).click();
      const dialog = page.getByRole("dialog"), editor = dialog.getByRole("region", { name: copy.platformEditorTitle, exact: true });
      await expect.poll(() => dialog.evaluate((node) => node.contains(document.activeElement))).toBe(true);
      await page.keyboard.press("Shift+Tab");
      await expect.poll(() => dialog.evaluate((node) => node.contains(document.activeElement))).toBe(true);
      const name = dialog.getByRole("textbox", { name: copy.name, exact: true });
      await name.fill("Unsaved merchant draft");
      const provider = editor.getByRole("combobox", { name: copy.platformProvider, exact: true });
      await expect(provider.locator("option")).toHaveCount(12);
      await provider.selectOption("tablecheck");
      await editor.getByRole("combobox", { name: copy.platformReviewStatus, exact: true }).selectOption("verified");
      await editor.getByRole("textbox", { name: copy.platformCanonicalUrl, exact: true }).fill(tablecheckUrl);
      await editor.getByRole("textbox", { name: copy.platformReviewNote, exact: true }).fill("Fixture-only owner page and exact branch verified");
      if (width === 320) {
        await page.keyboard.press("Escape");
        await expect(dialog.getByRole("alert")).toBeVisible();
        await dialog.getByRole("button", { name: copy.platformKeepEditing, exact: true }).click();
        expect(writes).toEqual([]);
      }
      await provider.selectOption("inline");
      await expect(editor.getByRole("textbox", { name: copy.platformCanonicalUrl, exact: true })).toHaveValue(inlineUrl);
      await provider.selectOption("tablecheck");
      await expect(editor.getByRole("textbox", { name: copy.platformCanonicalUrl, exact: true })).toHaveValue(tablecheckUrl);
      const save = editor.getByRole("button", { name: copy.platformSaveOnly, exact: true });
      await save.scrollIntoViewIfNeeded();
      expect((await save.boundingBox())!.height).toBeGreaterThanOrEqual(44);
      await save.click();
      await expect.poll(() => writes.length).toBe(1);
      await expect(name).toHaveValue("Unsaved merchant draft");
      expect(writes[0]).toMatchObject({ method: "PUT", path: `/admin/foods/merchants/${merchantId}/platform-link`, body: { provider: "tablecheck", status: "verified", expected_checked_at: null, canonical_url: tablecheckUrl } });
      expect(Object.keys(writes[0].body).sort()).toEqual(["canonical_url", "expected_checked_at", "localized_urls", "provider", "review_note", "status"]);
      await expect(editor.getByRole("list", { name: copy.platformSavedList })).toContainText("TableCheck");
      await expect(editor.getByRole("list", { name: copy.platformSavedList })).toContainText("inline");
      await provider.selectOption("inline");
      await editor.getByRole("combobox", { name: copy.platformReviewStatus, exact: true }).selectOption("disabled");
      await save.click();
      await expect.poll(() => writes.length).toBe(2);
      expect(writes[1].body.expected_checked_at).toBe("2026-09-10T00:00:00Z");
      expect(links.find((item) => item.provider === "tablecheck")!.status).toBe("verified");
      await expect(name).toHaveValue("Unsaved merchant draft");
      const overflow = await editor.evaluate((element) => element.scrollWidth > element.clientWidth);
      expect(overflow).toBe(false);
      await editor.screenshot({ path: info.outputPath(`platforms-${locale}-${width}.png`) });
    });
  }
}

test("conflict reload preserves platform draft and requires explicit confirmation before retry", async ({ page }) => {
  const copy = zhTW.foodMerchantsPanel;
  const { writes } = await fixture(page, true);
  await page.goto("/zh-TW/admin/foods?tab=catalog&section=merchants");
  await expect(page.getByRole("button", { name: copy.editButton, exact: true })).toBeVisible();
  await page.getByRole("button", { name: copy.editButton, exact: true }).click();
  const editor = page.getByRole("dialog").getByRole("region", { name: copy.platformEditorTitle, exact: true });
  const note = editor.getByRole("textbox", { name: copy.platformReviewNote, exact: true });
  await note.fill("Retain my unsaved evidence after conflict");
  const save = editor.getByRole("button", { name: copy.platformSaveOnly, exact: true });
  await save.click();
  await expect(editor.getByRole("alert")).toBeVisible();
  await expect(save).toBeDisabled();
  await editor.getByRole("button", { name: copy.platformReloadDraft, exact: true }).click();
  await expect(note).toHaveValue("Retain my unsaved evidence after conflict");
  await expect(save).toBeDisabled();
  await editor.getByRole("button", { name: copy.platformConfirmRetry, exact: true }).click();
  await save.click();
  await expect.poll(() => writes.length).toBe(2);
  expect(writes[1].body.review_note).toBe("Retain my unsaved evidence after conflict");
});
