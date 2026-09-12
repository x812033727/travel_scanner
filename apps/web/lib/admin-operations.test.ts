import { describe, expect, it } from "vitest";
import { canAccessAdminPath, normalizeAdminBootstrap } from "./admin-operations";

const payload = (navigation: { id: string; href: string; group?: string }[]) => normalizeAdminBootstrap({
  actor: { id: "actor", email: "admin@example.com", roles: ["viewer"], capabilities: ["admin.access", "dashboard.read"] },
  environment: "test", navigation, pending: {}, system: {},
})!;

describe("admin server navigation boundary", () => {
  it("normalizes backend label keys and keeps explicit allowlist decisions authoritative", () => {
    const normalized = normalizeAdminBootstrap({
      actor: { id: "actor", email: "db@example.com", roles: ["database_operator"], capabilities: ["admin.access", "database.read", "database.maintain", "deploy.execute"] },
      navigation: [
        { id: "travel_services", label_key: "travel_services", href: "/admin/travel-services", group: "content" },
        { id: "provider_settings", label_key: "provider_settings", href: "/admin/settings", group: "system" },
      ],
      pending: {}, system: {}, environment: "production", can_deploy: false, can_manage_database: false,
    })!;
    expect(normalized.navigation.map((item) => item.key)).toEqual(["travelServices", "providers"]);
    expect(normalized.can_deploy).toBe(false);
    expect(normalized.can_manage_database).toBe(false);
  });

  it("does not let a viewer deep-link into database operations", () => {
    const viewer = payload([{ id: "dashboard", href: "/admin", group: "overview" }]);
    expect(canAccessAdminPath(viewer, "/zh-TW/admin", "zh-TW")).toBe(true);
    expect(canAccessAdminPath(viewer, "/zh-TW/admin/database?tab=tables", "zh-TW")).toBe(false);
  });

  it("does not let support deep-link into content tools absent from server navigation", () => {
    const support = payload([
      { id: "dashboard", href: "/admin", group: "overview" },
      { id: "users", href: "/admin/users", group: "operations" },
    ]);
    expect(canAccessAdminPath(support, "/en/admin/users/member-id", "en")).toBe(true);
    expect(canAccessAdminPath(support, "/en/admin/hotspots", "en")).toBe(false);
  });

  it("opens the guides editor once the server navigation lists it", () => {
    // The API registry had no guides entry, the web fallback list is consulted only when the
    // server list is empty, and this check refuses anything outside the list -- so on the live
    // site /admin/guides was forbidden by URL and absent from the sidebar: nineteen topics,
    // zero articles. The registry now carries it; this pins the web half of that fix.
    const content = payload([
      { id: "dashboard", href: "/admin", group: "overview" },
      { id: "guides", href: "/admin/guides", group: "content" },
    ]);
    expect(content.navigation.map((item) => item.key)).toContain("guides");
    expect(canAccessAdminPath(content, "/zh-TW/admin/guides", "zh-TW")).toBe(true);
    expect(canAccessAdminPath(content, "/zh-TW/admin/hotspots", "zh-TW")).toBe(false);
  });
});
