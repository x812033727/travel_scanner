import { expect, test } from "@playwright/test";
import { pretendSignedIn } from "./session";

// Browser fixtures only: these tests never authenticate to or mutate production.
const candidate = {
  id: "11111111-1111-4111-8111-111111111111", name: "審核測試景點", qid: null,
  category: "culture", destination_id: "taipei", city_code: "TPE", city_name: "台北",
  country_code: "TW", country_name: "台灣", destination_role: "primary", parent_destination_id: null,
  status: "pending", reason: null, origin: "curated", is_active: false, is_deep_travel: false,
  source_urls: ["https://example.org/evidence"], map_match_status: "verified",
  latitude: 25.03, longitude: 121.56, coordinate_source_type: "admin_verified",
  coordinate_source_url: "https://example.org/evidence", google_place_id: "ChIJ-fixture-whole-place", naver_map_url: null,
  updated_at: "2026-09-10T01:00:00Z",
};

for (const colorScheme of ["light", "dark"] as const) {
  test(`identity editor preserves draft, version and review state (${colorScheme})`, async ({ page }) => {
    await pretendSignedIn(page);
    await page.emulateMedia({ colorScheme, reducedMotion: "reduce" });
    let posts = 0;
    let approvals = 0;
    let saved: Record<string, unknown> = { ...candidate };
    await page.route("**/api/travel/admin/hotspots/**", async (route) => {
      const path = new URL(route.request().url()).pathname;
      if (path.endsWith("/candidates")) return route.fulfill({ json: { items: [saved], total: 1, page: 1, pages: 1 } });
      if (path.endsWith("/review") && route.request().method() === "POST") {
        const body = route.request().postDataJSON();
        if (body.action === "approve") {
          approvals += 1;
          expect(body.expected_updated_ats).toEqual({ [candidate.id]: saved.updated_at });
          expect(body).not.toHaveProperty("reason");
          expect(body).not.toHaveProperty("google_place_id");
          expect(saved.reason).toContain("https://example.org/evidence");
          saved = { ...saved, status: "approved", is_active: true, updated_at: "2026-09-10T03:00:00Z" };
          return route.fulfill({ json: { updated: 1, status: "approved" } });
        }
        posts += 1;
        expect(body.action).toBe("update");
        expect(body.expected_updated_at).toBe(saved.updated_at);
        expect(body.category).toBe("shopping");
        expect(body.wikidata_item_id).toBe("Q12345");
        expect(body.reason).toContain("https://example.org/evidence");
        expect(body).not.toHaveProperty("latitude");
        if (posts === 1) return route.fulfill({ status: 409, json: { code: "hotspot_review_conflict", detail: "Conflict" } });
        saved = { ...saved, category: body.category, qid: body.wikidata_item_id, reason: body.reason, updated_at: "2026-09-10T02:00:00Z" };
        return route.fulfill({ json: { updated: 1, status: "pending" } });
      }
      return route.fulfill({ json: { items: [], total: 0 } });
    });
    await page.goto(`/zh-TW/admin/hotspots?tab=places&section=identity&hotspot_id=${candidate.id}`);
    await page.getByRole("button", { name: "編輯地點", exact: true }).click();
    const fillDraft = async () => {
      await page.getByRole("combobox", { name: "景點分類", exact: true }).selectOption("shopping");
      await page.getByLabel("Wikidata ID", { exact: true }).fill("Q12345");
      await page.getByLabel("審核理由與來源", { exact: true }).fill("同一景點之官方證據 https://example.org/evidence");
    };
    await fillDraft();
    const save = page.getByRole("button", { name: "儲存地點", exact: true });
    await save.click();
    await expect(page.getByRole("alert").filter({ hasText: "草稿已保留" })).toBeVisible();
    await expect(page.getByLabel("Wikidata ID", { exact: true })).toHaveValue("Q12345");
    await expect(save).toBeDisabled();
    await page.screenshot({ path: test.info().outputPath(`editor-conflict-${colorScheme}.png`), fullPage: true });
    page.once("dialog", (dialog) => dialog.accept());
    await page.getByRole("button", { name: "重新載入最新資料", exact: true }).click();
    await expect(page.getByLabel("Wikidata ID", { exact: true })).toHaveValue("");
    await fillDraft();
    await save.click();
    await expect(page.getByRole("status").filter({ hasText: "已儲存精準地點" })).toBeVisible();
    expect(saved.status).toBe("pending");
    expect(saved.is_active).toBe(false);
    expect(posts).toBe(2);
    await page.reload();
    await page.getByRole("button", { name: "編輯地點", exact: true }).click();
    await expect(page.getByLabel("Wikidata ID", { exact: true })).toHaveAttribute("readonly", "");
    const box = await save.boundingBox();
    expect(box?.height).toBeGreaterThanOrEqual(44);
    await expect(page.locator("html")).toHaveJSProperty("scrollWidth", await page.locator("html").evaluate((node) => node.clientWidth));
    await page.screenshot({ path: test.info().outputPath(`editor-saved-${colorScheme}.png`), fullPage: true });
    await page.getByRole("button", { name: "關閉", exact: true }).click();
    await page.getByRole("checkbox", { name: `選取 ${candidate.name}`, exact: true }).check();
    await expect(page.getByLabel("本次審核理由與來源", { exact: true })).toHaveValue("");
    await page.getByRole("button", { name: "核准", exact: true }).click();
    await expect(page.getByRole("status").filter({ hasText: "已更新 1 筆景點候選" })).toBeVisible();
    expect(approvals).toBe(1);
    await page.reload();
    await expect(page.getByRole("cell", { name: /approved/ })).toBeVisible();
    await expect(page.getByText("同一景點之官方證據 https://example.org/evidence", { exact: true })).toBeVisible();
  });
}
