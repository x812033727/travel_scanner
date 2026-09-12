import { createServer } from "node:http";

const visibility = {
  hotspots_enabled: true,
  trips_enabled: true,
  alerts_enabled: true,
  flight_status_enabled: true,
  airline_fares_enabled: true,
  pricing_enabled: true,
};

const operationCosts = Object.fromEntries([
  "travel_search",
  "flexible_flight_search",
  "flight_hotel_search",
  "full_trip_search",
  "multi_city_search",
  "public_airline_fare_search",
  "back_to_back_fare_search",
  "live_back_to_back_fare_search",
  "flight_status_lookup",
  "ai_itinerary_generation",
  "ai_itinerary_refine",
  "itinerary_optimization",
  "price_reoptimization",
].map((operation) => [operation, 1]));

const usageCatalog = {
  trial_uses: 3,
  packages: [
    { code: "PACK_10", name: "輕量包", uses: 10, price_twd: 199, display_order: 10, is_featured: false, expires: false, purchasable: false },
    { code: "PACK_30", name: "常用包", uses: 30, price_twd: 499, display_order: 20, is_featured: true, expires: false, purchasable: false },
    { code: "PACK_100", name: "大量包", uses: 100, price_twd: 1299, display_order: 30, is_featured: false, expires: false, purchasable: false },
  ],
  operation_costs: operationCosts,
};

const fixtureNow = "2026-09-09T00:00:00Z";
const fixtureMemberId = "00000000-0000-4000-8000-000000000010";
const fixtureUser = {
  id: fixtureMemberId,
  email: "traveler@example.test",
  is_active: true,
  is_admin: false,
  effective_is_admin: false,
  admin_source: "none",
  is_self: false,
  can_adjust_usage: true,
  remaining_uses: 20,
  reserved_uses: 0,
  available_uses: 20,
  created_at: fixtureNow,
  updated_at: fixtureNow,
  status: "active",
  admin_roles: [],
  auth_methods: ["password"],
  email_verified: false,
  last_login_at: fixtureNow,
  erasure_status: "none",
};

function fixtureUserDetail() {
  return {
    ...fixtureUser,
    activity: { trips: 2, searches: 4, alerts: 1, community_posts: 0, community_comments: 0 },
    auth_identities: [],
    erasure: null,
    usage_history: [],
    admin_history: [],
  };
}

const adminCapabilities = {
  viewer: ["admin.access", "dashboard.read", "content.read", "community.read", "users.read", "analytics.read", "settings.read", "audit.read"],
  support: ["admin.access", "dashboard.read", "community.read", "community.manage", "users.read", "users.manage", "usage.manage", "audit.read"],
  content: ["admin.access", "dashboard.read", "content.read", "content.manage", "community.read", "audit.read"],
  operations: ["admin.access", "dashboard.read", "analytics.read", "settings.read", "settings.manage", "audit.read"],
  database_operator: ["admin.access", "dashboard.read", "database.read", "database.maintain", "audit.read"],
  deployer: ["admin.access", "dashboard.read", "deploy.read", "deploy.execute", "audit.read"],
};
adminCapabilities.owner = [...new Set(Object.values(adminCapabilities).flat()), "roles.manage"];

const adminNavigation = [
  ["dashboard", "overview", "/admin", "dashboard.read"],
  ["guides", "content", "/admin/guides", "content.read"],
  ["hotspots", "content", "/admin/hotspots", "content.read", "hotspots_pending"],
  ["foods", "content", "/admin/foods", "content.read", "foods_pending"],
  ["hotels", "content", "/admin/hotels", "content.read", "hotels_pending"],
  ["travel_services", "content", "/admin/travel-services", "content.read"],
  ["catalog_review", "content", "/admin/catalog-review", "content.read"],
  ["community", "community", "/admin/community", "community.read", "community_jobs_pending"],
  ["pet_friendly", "community", "/admin/pet-friendly", "community.read"],
  ["users", "operations", "/admin/users", "users.read"],
  ["analytics", "operations", "/admin/analytics", "analytics.read"],
  ["partners", "operations", "/admin/partners", "content.read"],
  ["provider_settings", "operations", "/admin/settings", "settings.read"],
  ["usage_settings", "operations", "/admin/usage-settings", "settings.read"],
  ["layout_settings", "operations", "/admin/layout-settings", "settings.read"],
  ["ui_text", "operations", "/admin/ui-text", "settings.read"],
  ["site_pages", "operations", "/admin/site-pages", "settings.read"],
  ["system_settings", "system", "/admin/system-settings", "settings.read"],
  ["database", "system", "/admin/database", "database.read"],
  ["deployments", "system", "/admin/deployments", "deploy.read"],
  ["audit", "system", "/admin/audit", "audit.read"],
].map(([id, group, href, capability, badge_key]) => ({
  id, group, href, label_key: id, capability, ...(badge_key ? { badge_key } : {}),
}));

function adminBootstrap(request) {
  const authorization = request.headers.authorization || "";
  const token = authorization.startsWith("Bearer ") ? authorization.slice(7) : "";
  const role = token === "e2e-session" ? "owner" : token.startsWith("e2e-") ? token.slice(4) : "";
  const capabilities = adminCapabilities[role];
  if (!capabilities) return null;
  const capabilitySet = new Set(capabilities);
  // Exercise the second authorization gate instead of deriving these values from
  // RBAC alone: the isolated owner/database operator are on the database fixture
  // allowlist, while only the deployer fixture is on the deployment allowlist.
  const databaseAllowlist = new Set(["owner@example.test", "database_operator@example.test"]);
  const deploymentAllowlist = new Set(["deployer@example.test"]);
  const email = `${role}@example.test`;
  return {
    actor: {
      id: "00000000-0000-4000-8000-000000000001",
      email,
      roles: [role],
      capabilities,
    },
    environment: "e2e-isolated",
    navigation: adminNavigation.filter((item) => capabilitySet.has(item.capability)),
    pending: { users: 3, hotspots_pending: 2, foods_pending: 1, hotels_pending: 1, community_jobs_pending: 0 },
    system: {
      database: { status: "healthy", detail: "fixture schema current" },
      redis: { status: "healthy" },
      providers: { status: "degraded", detail: "fixture provider disabled" },
      background_jobs: { status: "healthy" },
      deployment: { status: "disabled", detail: "fixture agent disabled" },
      backup: { status: "disabled", detail: "fixture maintenance read-only" },
    },
    can_deploy: capabilitySet.has("deploy.execute") && deploymentAllowlist.has(email),
    can_manage_database: capabilitySet.has("database.maintain") && databaseAllowlist.has(email),
    generated_at: "2026-09-09T00:00:00Z",
  };
}

const server = createServer((request, response) => {
  response.setHeader("Cache-Control", "no-store");
  response.setHeader("Content-Type", "application/json");
  // Match the default production switch explicitly; homepage SSR tests must not
  // accidentally rely on an unimplemented endpoint returning 404.
  if (request.method === "GET" && request.url === "/api/v1/discovery/status") {
    response.end(JSON.stringify({ enabled: false }));
    return;
  }
  if (request.method === "GET" && request.url === "/api/v1/runtime/site-visibility") {
    response.end(JSON.stringify(visibility));
    return;
  }
  // Synthetic guide translations for the runtime sitemap only; the article pages are not served
  // here. The notice is published without English and the how-to in English alone, so
  // e2e/seo.spec.ts can check <lastmod> and each article's own hreflang set in the real XML.
  if (request.method === "GET" && request.url === "/api/v1/guides/sitemap") {
    response.end(JSON.stringify({ entries: [
      { kind: "intel", slug: "synthetic-fare-notice", locale: "zh-TW", published_at: "2026-09-08T09:30:00Z" },
      { kind: "intel", slug: "synthetic-fare-notice", locale: "ja", published_at: "2026-09-07T01:00:00Z" },
      { kind: "howto", slug: "synthetic-airport-transfer", locale: "en", published_at: "2026-09-01T00:00:00Z" },
    ] }));
    return;
  }
  if (request.method === "GET" && request.url === "/api/v1/auth/registration-status") {
    response.end(JSON.stringify({ registration_enabled: true }));
    return;
  }
  if (request.method === "GET" && request.url?.startsWith("/api/v1/usage-catalog")) {
    response.end(JSON.stringify(usageCatalog));
    return;
  }
  if (request.method === "GET" && request.url === "/api/v1/admin/bootstrap") {
    const bootstrap = adminBootstrap(request);
    if (!bootstrap) {
      response.statusCode = 401;
      response.end(JSON.stringify({ code: "invalid_session", detail: "Isolated administrator session required" }));
      return;
    }
    response.end(JSON.stringify(bootstrap));
    return;
  }
  const requestUrl = new URL(request.url || "/", "http://127.0.0.1:8000");
  // Clearly synthetic SSR fixtures: never a production policy or owner identity.
  if (request.method === "GET" && requestUrl.pathname.startsWith("/api/v1/site-pages/")) {
    const slug = requestUrl.pathname.split("/").at(-1);
    const locale = requestUrl.searchParams.get("locale") || "en";
    if (slug === "about") { response.statusCode = 503; response.end(JSON.stringify({ detail: "Fixture unavailable" })); return; }
    const unpublished = slug === "terms";
    response.end(JSON.stringify({ slug, locale, status: unpublished ? "unpublished" : "published", document: unpublished ? null : {
      title: `Synthetic ${slug} (${locale})`, description: `Synthetic published summary (${locale})`,
      version: 2, published_at: fixtureNow, effective_date: "2026-09-09",
      requirements: { operator: "Synthetic fixture operator", location: "Not a real location", contact: "fixture@example.test", retention: "Fixture only", legal: "Fixture only" },
      blocks: [{ type: "paragraph", text: `Synthetic public content (${locale}). Not a real policy.` }],
    } })); return;
  }
  if (request.method === "GET" && requestUrl.pathname === "/api/v1/auth/me") {
    response.end(JSON.stringify({
      id: "00000000-0000-4000-8000-000000000001",
      email: "owner@example.test",
      is_admin: true,
      admin_roles: ["owner"],
      admin_capabilities: adminCapabilities.owner,
      preferred_locale: "zh-TW",
      can_deploy: false,
    }));
    return;
  }
  if (request.method === "GET" && requestUrl.pathname === "/api/v1/analytics/config") {
    response.end(JSON.stringify({ first_party_enabled: false, ga4_enabled: false }));
    return;
  }
  if (request.method === "GET" && requestUrl.pathname === "/api/v1/admin/dashboard") {
    response.end(JSON.stringify({
      counts: {
        users_total: 3, hotspots_total: 10, hotspots_pending: 2,
        foods_total: 4, foods_pending: 1, hotels_total: 3, hotels_pending: 1,
        community_jobs_pending: 0, providers_unhealthy: 1,
      },
      can_deploy: false,
    }));
    return;
  }
  if (request.method === "GET" && requestUrl.pathname === "/api/v1/admin/users") {
    response.end(JSON.stringify({
      items: [fixtureUser], page: 1, limit: 20, total: 1, pages: 1,
      stats: { total: 1, active: 1, administrators: 0, available_uses: 20, suspended: 0, erasure_pending: 0 },
    }));
    return;
  }
  if (request.method === "GET" && requestUrl.pathname === `/api/v1/admin/users/${fixtureMemberId}`) {
    response.end(JSON.stringify(fixtureUserDetail()));
    return;
  }
  if (request.method === "GET" && requestUrl.pathname === "/api/v1/admin/audit") {
    response.end(JSON.stringify({
      items: [{
        id: "00000000-0000-4000-8000-000000000020",
        actor_user_id: null,
        actor_email: "owner@example.test",
        action: "user.sessions_revoked",
        target: `user:${fixtureMemberId}`,
        result: "succeeded",
        metadata: { reason: "fixture review" },
        created_at: fixtureNow,
      }],
      total: 1, page: 1, limit: 20, pages: 1,
    }));
    return;
  }
  if (request.method === "GET" && requestUrl.pathname === "/api/v1/admin/database/overview") {
    response.end(JSON.stringify({
      status: "ok",
      checked_at: fixtureNow,
      postgres: {
        version: "PostgreSQL 17",
        database_size_bytes: 1048576,
        connections: { active: 1, idle: 2, waiting: 0, maximum: 100 },
        long_transactions: 0,
        lock_waits: 0,
        cache_hit_ratio: 99.25,
      },
      schema_info: {
        current_revision: "0068_admin_operations_center",
        expected_revision: "0068_admin_operations_center",
        is_current: true,
      },
      agent: { connected: true, available: true, release_sha: "fixture-release", checks: [], active_job: null },
      active_operation: null,
      last_backup: null,
      maintenance_enabled: true,
      retention_count: 7,
    }));
    return;
  }
  if (request.method === "GET" && requestUrl.pathname === "/api/v1/admin/database/tables") {
    response.end(JSON.stringify({ items: [{
      name: "users", estimated_rows: 3, data_bytes: 16384, index_bytes: 8192,
      total_bytes: 24576, dead_rows: 0, last_analyze: fixtureNow,
    }] }));
    return;
  }
  if (request.method === "GET" && requestUrl.pathname === "/api/v1/admin/database/backups") {
    response.end(JSON.stringify({ items: [] }));
    return;
  }
  // No administrator overrides in e2e: the loader would fail open on a 404 anyway, but a
  // real empty payload keeps the run free of "could not reach the API" noise.
  if (request.method === "GET" && request.url?.startsWith("/api/v1/runtime/ui-text")) {
    response.end(JSON.stringify({ locale: "zh-TW", version: "e2e", entries: {} }));
    return;
  }
  response.statusCode = 404;
  response.end(JSON.stringify({ detail: "not found" }));
});

server.listen(Number(process.env.E2E_API_PORT || 8000), "127.0.0.1");

for (const signal of ["SIGINT", "SIGTERM"]) {
  process.on(signal, () => server.close(() => process.exit(0)));
}
