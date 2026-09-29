import { expect, test, type Page } from "@playwright/test";
import en from "../messages/en/community.json" with { type: "json" };
import ja from "../messages/ja/community.json" with { type: "json" };
import ko from "../messages/ko/community.json" with { type: "json" };
import tw from "../messages/zh-TW/community.json" with { type: "json" };
import cn from "../messages/zh-CN/community.json" with { type: "json" };
import type { Post } from "../lib/community/types";
import { pretendSignedIn } from "./session";

// Browser UI contracts against explicit synthetic responses. These do not replace
// community.spec.ts's real PostgreSQL/Redis/MinIO/Mailpit/worker acceptance.
const catalogs = { en, ja, ko, "zh-TW": tw, "zh-CN": cn };
const id = "62000000-0000-4000-8000-000000000001";
const profile = { id: "synthetic-member", handle: "synthetic-reader", display_name: "Synthetic reader", bio: "", languages: ["en"], destinations: [], avatar_id: null };
const flags = { enabled: true, posting_enabled: true, comments_enabled: true, messaging_enabled: true, translation_enabled: true, pet_reports_enabled: true };

async function fixture(page: Page, baseURL: string | undefined, locale: string) {
  const origin = new URL(baseURL || "http://127.0.0.1:3000").origin;
  expect(["localhost", "127.0.0.1", "[::1]"]).toContain(new URL(origin).hostname);
  await pretendSignedIn(page);
  let edited = false;
  let translations = 0;
  const unexpectedWrites: string[] = [];
  const external: string[] = [];
  const errors: string[] = [];
  page.on("pageerror", (error) => errors.push(error.message));
  const post = (): Post => ({
    id, revision_id: edited ? "revision-2" : "revision-1", author: { ...profile, id: "synthetic-author" },
    title: "Synthetic community acceptance story", body: edited ? "Edited synthetic original" : "Original synthetic story",
    locale: locale === "en" ? "ja" : "en", destination: "Synthetic city", kind: "story", topics: ["fixture"],
    place_ids: [], places: [], media: [], itinerary: null, allow_fork: false,
    published_at: "2026-09-07T00:00:00Z", featured: false, likes: edited ? 1 : 0, saves: 0, liked: edited, saved: false,
  });
  await page.context().route("**/*", (route) => {
    const url = new URL(route.request().url());
    if (url.origin === origin) return route.fallback();
    external.push(url.origin + url.pathname);
    return route.abort("blockedbyclient");
  });
  await page.route("**/api/travel/**", async (route) => {
    const request = route.request(), url = new URL(request.url());
    const path = url.pathname.replace("/api/travel", "");
    const send = (json: unknown, status = 200) => route.fulfill({ status, json });
    if (path === "/community/translations" && request.method() === "POST") {
      expect(request.postDataJSON()).toEqual({ kind: "post", target_id: id, locale });
      translations += 1;
      if (translations === 1) return send({ code: "community_translation_unavailable" }, 503);
      return send({ text: edited ? "Fresh synthetic translation" : "Synthetic translation before edit" });
    }
    if (path === `/community/posts/${id}/reactions/like` && request.method() === "PUT") {
      // The ordinary reaction reload returns a newer published revision, modelling
      // another author's edit while this reader has the old translation open.
      edited = true;
      return send({});
    }
    if (request.method() !== "GET") {
      unexpectedWrites.push(`${request.method()} ${path}`);
      return send({ code: "unexpected_fixture_write" }, 405);
    }
    if (path === "/auth/me") return send({ id: profile.id, email: "synthetic@example.test", is_admin: false });
    if (path === "/community/status") return send(flags);
    if (path === "/community/me") return send({ profile, verified: true, restricted: false, notification_preferences: {} });
    if (path === "/community/events/cursor") return send({ cursor: 0 });
    if (path === "/community/events") return route.fulfill({ contentType: "text/event-stream", body: ": synthetic fixture\n\n" });
    if (path === "/community/notifications") return send({ items: [], unread: 0 });
    if (path === "/community/feed") return send({ items: [post()], next_cursor: null });
    if (path === `/community/posts/${id}`) return send(post());
    if (path === `/community/posts/${id}/comments`) return send({ items: [], next_cursor: null });
    if (path === "/community/collections") return send({ items: [], next_cursor: null });
    if (path === "/analytics/config") return send({ first_party_enabled: false, ga4_enabled: false });
    if (path === "/discovery/status") return send({ enabled: false });
    if (path === "/runtime/site-visibility") return send({ hotspots_enabled: true, trips_enabled: true, pricing_enabled: true });
    if (path === "/trips") return send([]);
    if (path === "/saved-items" || path === "/saved-items/states") return send({ items: [] });
    return send({ code: "fixture_endpoint_unavailable" }, 404);
  });
  return { unexpectedWrites, external, errors, translationCount: () => translations };
}

for (const [locale, messages] of Object.entries(catalogs)) {
  for (const colorScheme of ["light", "dark"] as const) {
    test(`${locale} ${colorScheme}: community reading, translation recovery and revision change`, async ({ page, baseURL }, info) => {
      const state = await fixture(page, baseURL, locale);
      await page.emulateMedia({ colorScheme, reducedMotion: "reduce" });
      await page.goto(`/${locale}/community`);
      await expect(page.locator("html")).toHaveAttribute("data-theme", colorScheme);
      await expect(page.getByRole("heading", { name: messages.feed, exact: true })).toBeVisible();
      const story = page.getByRole("link", { name: "Synthetic community acceptance story", exact: true });
      await expect(story).toBeVisible();
      await story.click();
      await expect(page.getByRole("heading", { name: "Synthetic community acceptance story", exact: true })).toBeVisible();
      const translate = page.getByRole("button", { name: messages.translate, exact: true });
      await expect(translate).toBeEnabled();
      await translate.click();
      await expect(page.getByRole("alert")).toHaveText(messages.errors.community_translation_unavailable);
      await expect(page.getByText("Original synthetic story", { exact: true })).toBeVisible();
      await translate.click();
      await expect(page.getByText("Synthetic translation before edit", { exact: true })).toBeVisible();
      await expect(page.getByText(messages.machineTranslation, { exact: true })).toBeVisible();
      await expect(page.getByRole("alert")).toHaveCount(0);
      await page.getByRole("button", { name: `${messages.like} · 0`, exact: true }).click();
      await expect(page.getByText("Edited synthetic original", { exact: true })).toBeVisible();
      await expect(page.getByText("Synthetic translation before edit", { exact: true })).toHaveCount(0);
      await translate.click();
      await expect(page.getByText("Fresh synthetic translation", { exact: true })).toBeVisible();
      await page.getByRole("button", { name: messages.showOriginal, exact: true }).click();
      await expect(page.getByText("Edited synthetic original", { exact: true })).toBeVisible();
      expect(state.translationCount()).toBe(3);

      const report = page.getByRole("button", { name: messages.report, exact: true });
      await report.click();
      const dialog = page.getByRole("dialog", { name: messages.report, exact: true });
      await expect(dialog.getByRole("textbox", { name: messages.reason, exact: true })).toBeVisible();
      await page.keyboard.press("Escape");
      await expect(dialog).toHaveCount(0);
      await expect(report).toBeFocused();
      await expect.poll(() => page.locator("html").evaluate((node) => node.scrollWidth - node.clientWidth)).toBeLessThanOrEqual(1);
      await page.screenshot({ path: info.outputPath(`synthetic-community-${locale}-${colorScheme}.png`), fullPage: true });
      expect(state.unexpectedWrites).toEqual([]);
      expect(state.external).toEqual([]);
      expect(state.errors).toEqual([]);
    });
  }
}
