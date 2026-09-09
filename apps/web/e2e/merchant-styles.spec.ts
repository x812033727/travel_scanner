import { expect, test, type Page } from "@playwright/test";
import en from "../messages/en/foods.json" with { type: "json" };
import ja from "../messages/ja/foods.json" with { type: "json" };
import ko from "../messages/ko/foods.json" with { type: "json" };
import tw from "../messages/zh-TW/foods.json" with { type: "json" };
import cn from "../messages/zh-CN/foods.json" with { type: "json" };
import { pretendSignedIn } from "./session";

const catalogs = { en, ja, ko, "zh-TW": tw, "zh-CN": cn };
const merchant = {
  id: "00000000-0000-4000-8000-000000000061", slug: "tokyo-style-fixture", name: "Style fixture café",
  local_name: "確認用カフェ", country_code: "JP", destination_id: "tokyo", destination_name: "Tokyo",
  categories: [{ id: "category-1", slug: "cafe-tea", name: "Cafe", is_primary: true, source: "admin" }],
  area: null, foods: [], signature_dishes: [], sources: [], map_links: [],
  latitude: null, longitude: null, coordinate_source: { type: null, url: null, verified_at: null },
  review_status: "pending", map_match_status: "unverified", is_active: false,
};
const initialReview = { style: "instagrammable", status: "pending", evidence_url: "https://shop.example/design",
  evidence_title: "Official branch design", rationale: "A branch-specific floral greenhouse design.",
  checked_on: "2026-09-08", updated_at: "2026-09-08T00:00:00+00:00" };

async function mock(page: Page) {
  await pretendSignedIn(page);
  const saved: Record<string, unknown>[] = [];
  await page.route("**/api/travel/**", async (route) => {
    const url = new URL(route.request().url());
    let body: unknown = { items: [], total: 0, has_more: false, countries: [] };
    if (url.pathname.endsWith("/auth/me")) body = { id: "test-admin", email: "test@example.test", is_admin: true };
    else if (url.pathname.endsWith("/styles")) {
      if (route.request().method() === "PUT") {
        const payload = route.request().postDataJSON(); saved.push(payload);
        body = { ...payload.review, updated_at: "2026-09-08T01:00:00+00:00" };
      } else body = { items: [initialReview] };
    } else if (url.pathname.endsWith("/merchants")) body = {
      total: 1, has_more: false, items: [merchant],
      facets: { areas: [], categories: [{ slug: "cafe-tea", name: "Cafe", merchant_count: 1 }], styles: [] },
    };
    else if (url.pathname.endsWith("/runtime/site-visibility")) body = { hotspots_enabled: true, trips_enabled: true, pricing_enabled: true };
    else if (url.pathname.endsWith("/admin/provider-settings")) body = { providers: [], audit: [], encryption_source: "fixture" };
    await route.fulfill({ json: body });
  });
  return saved;
}

for (const [locale, messages] of Object.entries(catalogs)) {
  for (const colorScheme of ["light", "dark"] as const) {
    test(`${locale} ${colorScheme} style filters retain cuisine and fit the viewport`, async ({ page }, testInfo) => {
      await mock(page);
      await page.emulateMedia({ colorScheme });
      await page.goto(`/${locale}/foods?destination_id=tokyo&category=cafe-tea&style=artsy`);
      const group = page.getByRole("group", { name: messages.styles.label, exact: true });
      await expect(group.getByRole("button", { name: messages.styles.artsy, exact: true })).toHaveAttribute("aria-pressed", "true");
      await group.getByRole("button", { name: messages.styles.instagrammable, exact: true }).click();
      await expect(page).toHaveURL(/category=cafe-tea&style=instagrammable/);
      await group.getByRole("button", { name: messages.styles.all, exact: true }).click();
      await expect(page).not.toHaveURL(/style=/);
      await expect(page).toHaveURL(/category=cafe-tea/);
      await expect(page.getByText(messages.styles.disclaimer, { exact: true })).toBeVisible();
      expect(await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth)).toBeLessThanOrEqual(1);
      await page.screenshot({ path: testInfo.outputPath("styles.png"), fullPage: true });
    });
  }
}

test("admin reviews one style without publishing the merchant and retains drafts", async ({ page }, testInfo) => {
  const saved = await mock(page);
  await page.goto("/zh-TW/admin/foods");
  await page.getByRole("button", { name: "編輯地點與來源", exact: true }).click();
  const dialog = page.getByRole("dialog", { name: merchant.name });
  await dialog.getByRole("button", { name: tw.styles.reviewTitle }).click();
  const reviewForm = dialog.getByRole("group", { name: tw.styles.reviewTitle, exact: true });
  await expect(dialog.getByLabel(tw.styles.sourceTitle)).toHaveValue(initialReview.evidence_title);
  await dialog.getByLabel(tw.styles.sourceTitle).fill("Checked branch design");
  await reviewForm.getByRole("combobox", { name: tw.styles.label, exact: true }).selectOption("artsy");
  await expect(dialog.getByLabel(tw.styles.sourceTitle)).toHaveValue("");
  await reviewForm.getByRole("combobox", { name: tw.styles.label, exact: true }).selectOption("instagrammable");
  await expect(dialog.getByLabel(tw.styles.sourceTitle)).toHaveValue("Checked branch design");
  await reviewForm.getByRole("combobox", { name: tw.styles.status, exact: true }).selectOption("approved");
  await dialog.getByLabel(tw.styles.reason).fill("已比對此分店官方設計資訊");
  await dialog.getByRole("button", { name: tw.styles.save }).click();
  await expect(dialog.getByText(tw.styles.saved)).toBeVisible();
  expect(saved).toHaveLength(1);
  expect(saved[0]).not.toHaveProperty("is_active");
  expect(saved[0].expected_updated_at).toBe(initialReview.updated_at);
  const box = await dialog.boundingBox();
  expect(box!.width).toBeLessThanOrEqual(page.viewportSize()!.width);
  await page.screenshot({ path: testInfo.outputPath("style-review.png") });
});
