import { createServer } from "node:http";
import { createHash } from "node:crypto";

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
  ["videos", "content", "/admin/videos", "content.read", "video_reviews_pending"],
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
  ["ai_accounts", "system", "/admin/ai-accounts", "settings.read"],
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
    pending: { users: 3, hotspots_pending: 2, foods_pending: 1, hotels_pending: 1, community_jobs_pending: 0, video_reviews_pending: 0 },
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

// Browser <a download> requests bypass Playwright route interception. Serve these
// synthetic bytes over HTTP so manual-upload cases exercise the real streaming BFF.
const manualUploadFiles = new Map([
  [2, "final"], [3, "thumbnail"], [5, "captions_zh_tw"], [6, "captions_zh-CN"],
  [7, "captions_en"], [8, "captions_ja"], [9, "captions_ko"],
].map(([value, role]) => [value.toString(16).padStart(2, "0").repeat(32), `Synthetic download fixture: ${role}\n`]));
const manualUploadFilePrefix = "/api/v1/admin/videos/manual-upload-fixture/files/";

// Fixed, synthetic Shorts data for admin-video-shorts.spec.ts. Keep API response shapes
// aligned with app/video_shorts/schemas.py; the browser exercises the real JSON/file BFFs.
const shortsNow = "2026-10-05T03:00:00Z";
const shortsId = (number) => `00000000-0000-4000-8000-${String(number).padStart(12, "0")}`;
// Both decode to 18x32 (9:16). One second of solid teal, no audio or external assets.
// Generated with ffmpeg's color=c=teal:s=18x32:r=30:d=1, libx264 baseline,
// yuv420p and +faststart; the PNG is one frame of the same color source.
const shortsPreview = Buffer.from("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", "base64");
const shortsCover = Buffer.from("iVBORw0KGgoAAAANSUhEUgAAABIAAAAgCAIAAACQHr+mAAAACXBIWXMAAAABAAAAAQBPJcTWAAAAIUlEQVR4nGNkqKtjIB2wkKFnVNuotlFto9pGtY1qo5s2AHqCAXoBpr13AAAAAElFTkSuQmCC", "base64");
const shortsHash = (bytes) => createHash("sha256").update(bytes).digest("hex");
const shortsFiles = new Map([
  [shortsHash(shortsPreview), { body: shortsPreview, type: "video/mp4" }],
  [shortsHash(shortsCover), { body: shortsCover, type: "image/png" }],
]);
const shortsProjects = ["making", "needs_you", "library", "slotted", "scheduled", "published", "missed", "dropped"].map((state, index) => ({
  slug: `synthetic-shorts-${state.replaceAll("_", "-")}`, title: `Synthetic Shorts ${state}`,
  stage: state === "making" ? "render" : "final", checklist: [], pending: state === "needs_you" ? 1 : 0,
  ready_to_upload: false, locales_decided_at: null, locales: {},
  format: "shorts", shorts_line: "lab", shorts_series: "daily", shorts_state: state,
  youtube_video_id: ["scheduled", "published", "dropped"].includes(state) ? `Fixture000${index}` : null,
  last_synced_at: shortsNow, publish_approved_at: state === "published" ? "2026-10-03T03:00:00Z" : null,
  slot_at: state === "slotted" ? "2026-10-05T11:30:00Z" : null,
  youtube_publish_at: state === "scheduled" ? "2026-10-07T11:30:00Z" : ["published", "dropped"].includes(state) ? "2026-10-03T03:00:00Z" : null,
  youtube_removed_at: state === "dropped" ? "2026-10-04T04:00:00Z" : null,
  dropped_at: state === "dropped" ? "2026-10-04T04:00:00Z" : null,
  dropped_note: state === "dropped" ? "Synthetic removed Short" : null,
}));
const shortsDetail = (project) => ({ ...project, reviews: [{
  id: shortsId(100 + shortsProjects.indexOf(project)), gate: "final", content_sha256: shortsHash(shortsPreview),
  summary: "Synthetic one-second portrait preview", status: project.pending ? "pending" : "approved",
  payload: { duration_seconds: 1, titles: [project.title, "Synthetic alternate title"],
    qa: { ok: true, kind: "shorts", final_sha256: shortsHash(shortsPreview), items: [{ id: "profile", ok: true, detail: "Synthetic portrait fixture" }] } },
  files: [
    { role: "preview", sha256: shortsHash(shortsPreview), size: shortsPreview.length, content_type: "video/mp4" },
    { role: "thumbnail", sha256: shortsHash(shortsCover), size: shortsCover.length, content_type: "image/png" },
  ], choice: null, note: null, created_at: shortsNow, decided_at: project.pending ? null : shortsNow,
}] });
const shortsSlot = (number, fields) => ({
  id: shortsId(number), starts_at: "2026-10-05T11:30:00Z", local_date: "2026-10-05", local_time: "19:30", phase: 1,
  line: null, series: null, topic_slug: null, project_slug: null, project_title: null, project_line: null,
  youtube_video_id: null, status: "open", locked_at: null, note: null, ...fields,
});
const shortsSlots = [
  shortsSlot(1, { status: "assigned", project_slug: "synthetic-shorts-slotted", project_title: "Synthetic Shorts slotted", project_line: "lab" }),
  shortsSlot(2, { starts_at: "2026-10-06T04:30:00Z", local_date: "2026-10-06", local_time: "12:30", status: "skipped" }),
  shortsSlot(3, { starts_at: "2026-10-06T11:30:00Z", local_date: "2026-10-06" }),
  shortsSlot(4, { starts_at: "2026-10-20T11:30:00Z", local_date: "2026-10-20", note: "Synthetic later slot" }),
];
const shortsBudget = {
  period_start: "2026-10-04T16:00:00Z", period_end: "2026-11-03T16:00:00Z", spent_ntd: 0.29, reserved_ntd: 0, unknown: 1,
  limit_ntd: 3000, soft_ntd: 2400, total_start: "2026-10-04T16:00:00Z", total_spent_ntd: 0.29, total_limit_ntd: 9000,
  paid_work_allowed: false, reason: "Synthetic unknown cost pauses paid work",
};
const shortsOverview = {
  autopublish: "off", autopublish_problem: null, consent_expires_at: null, paused_at: null, timezone: "Asia/Taipei",
  today: shortsSlots.slice(0, 1), tomorrow: shortsSlots.slice(1, 3), stock: { count: 1, days: 2, wanted_days: 5 },
  budget: shortsBudget, channel: { linked: true, title: "Synthetic Shorts channel", audited: false, problem: null },
  worker_seen_at: shortsNow, campaign: { start: "2026-10-05", last_day: "2027-01-02", slots: 4, published: 0, missed: 0 },
  needs: [
    { kind: "review", detail: "Synthetic review needs the owner", slug: "synthetic-shorts-needs-you", count: 1 },
    { kind: "budget", detail: shortsBudget.reason, count: 1 },
  ], needs_count: 2,
};
const shortsSettings = {
  enabled: false, lines: ["lab", "cut", "drama"], weekly_quota: { lab: 5, cut: 2, drama: 0 },
  daily_pattern: [{ days: 30, counts: [1] }, { days: 60, counts: [2, 1] }], slot_times: ["19:30", "12:30"], timezone: "Asia/Taipei",
  stock_days: 5, lock_hours: 24, upload_ahead_days: 10, max_per_day: 2, seconds_min: 25, seconds_max: 55,
  voice: { provider: "gemini", name: "Sulafat", style: null, model: null, rate: "+0%" }, locales: [], made_for_kids: false, auto_approve: true,
  budget_ntd_30d: 3000, budget_soft_ntd: 2400, budget_total_ntd: 9000,
  campaign_start: "2026-10-05", autopublish: false, paused_at: null, updated_at: shortsNow,
  consent: { state: "none", problem: null, granted_at: null, granted_by_user_id: null, expires_at: null, text_sha256: null, scope: null, offer: null },
};
const shortsMetrics = { items: ["published", "dropped"].map((state) => ({
  slug: `synthetic-shorts-${state}`, title: `Synthetic Shorts ${state}`, line: "lab", series: "daily",
  youtube_video_id: state === "published" ? "Fixture0005" : "Fixture0007",
  published_at: "2026-10-03T03:00:00Z", removed_at: state === "dropped" ? "2026-10-04T04:00:00Z" : null,
  snapshots: [{ period: "d1", source: "data_api", captured_at: "2026-10-04T03:00:00Z", views: 1234, likes: 17, comments: 3 }],
})) };
const shortsCosts = {
  items: [
    { id: shortsId(201), occurred_at: shortsNow, project_slug: "synthetic-shorts-library", category: "narration", amount: 0.01, currency: "USD", fx_rate: 29, amount_ntd: 0.29, status: "confirmed", source: "auto", units: { seconds: 1 }, note: "Synthetic narration", created_at: shortsNow },
    { id: shortsId(202), occurred_at: shortsNow, project_slug: null, category: "tool", amount: null, currency: "USD", fx_rate: null, amount_ntd: null, status: "unknown", source: "manual", units: null, note: "Synthetic unknown cost", created_at: shortsNow },
  ], budget: shortsBudget,
  periods: [{ start: shortsBudget.period_start, end: shortsBudget.period_end, spent_ntd: 0.29, reserved_ntd: 0, unknown: 1, lines: 2 }],
};

function shortsFile(request, response, file) {
  const { body, type } = file;
  response.setHeader("Content-Type", type);
  response.setHeader("Accept-Ranges", "bytes");
  response.setHeader("ETag", `"${shortsHash(body)}"`);
  let start = 0, end = body.length - 1;
  if (request.headers.range) {
    const match = /^bytes=(\d*)-(\d*)$/.exec(request.headers.range);
    if (match && (match[1] || match[2])) {
      start = match[1] ? Number(match[1]) : Math.max(0, body.length - Number(match[2]));
      end = match[1] && match[2] ? Math.min(Number(match[2]), end) : end;
    } else start = body.length;
    if (start > end || start >= body.length) {
      response.statusCode = 416;
      response.setHeader("Content-Range", `bytes */${body.length}`);
      response.end();
      return;
    }
    response.statusCode = 206;
    response.setHeader("Content-Range", `bytes ${start}-${end}/${body.length}`);
  }
  response.setHeader("Content-Length", end - start + 1);
  response.end(body.subarray(start, end + 1));
}

function serveShortsFixture(request, response, url) {
  if (request.method !== "GET") return false;
  const path = url.pathname;
  let body;
  if (path === "/api/v1/admin/video-shorts/overview") body = shortsOverview;
  else if (path === "/api/v1/admin/video-shorts/settings") body = shortsSettings;
  else if (path === "/api/v1/admin/video-shorts/metrics") body = shortsMetrics;
  else if (path === "/api/v1/admin/video-shorts/costs") body = shortsCosts;
  else if (path === "/api/v1/admin/video-shorts/slots") body = {
    timezone: "Asia/Taipei", slots: shortsSlots.filter((slot) =>
      (!url.searchParams.get("from") || slot.local_date >= url.searchParams.get("from")) &&
      (!url.searchParams.get("to") || slot.local_date <= url.searchParams.get("to"))),
  };
  else if (path === "/api/v1/admin/video-shorts/uploads") body = { ahead_days: 10, items: [{
    slug: "synthetic-shorts-slotted", title: "Synthetic Shorts slotted", line: "lab", slot_at: shortsSlots[0].starts_at,
    file_name: "mokaair-short-synthetic-shorts-slotted.mp4", size: shortsPreview.length, seconds: 1,
  }] };
  else if (path === "/api/v1/admin/videos") body = url.searchParams.get("shorts") === "exclude" ? [] : shortsProjects;
  else if (path.startsWith("/api/v1/admin/videos/synthetic-shorts-")) {
    const [, slug, hash] = /^\/api\/v1\/admin\/videos\/([^/]+)(?:\/files\/([a-f0-9]{64}))?$/.exec(path) ?? [];
    const project = shortsProjects.find((item) => item.slug === slug);
    if (!project || (hash && !shortsFiles.has(hash))) return false;
    if (hash) { shortsFile(request, response, shortsFiles.get(hash)); return true; }
    body = shortsDetail(project);
  }
  else if (path === "/api/v1/admin/video-automation/settings") body = {
    voice_options: { gemini: ["Sulafat", "Kore"], gemini_models: ["gemini-3.8-flash-tts"], azure: [] }, locales: [], locale_parts: {},
  };
  else if (path === "/api/v1/admin/video-youtube") body = {
    configured: true, linked: true, audited: false, channel_id: "synthetic-channel", channel_title: "Synthetic Shorts channel",
    client_id: null, client_secret_set: false, redirect_uri: "", scope: "", channel_url: null, linked_at: null, verified_at: null, problem: null,
  };
  else return false;
  response.end(JSON.stringify(body));
  return true;
}

const server = createServer((request, response) => {
  response.setHeader("Cache-Control", "no-store");
  response.setHeader("Content-Type", "application/json");
  if (request.method === "GET" && request.url?.startsWith(manualUploadFilePrefix)) {
    const body = manualUploadFiles.get(request.url.slice(manualUploadFilePrefix.length));
    if (!body) {
      response.statusCode = 404;
      response.end(JSON.stringify({ detail: "Unknown synthetic file" }));
      return;
    }
    response.setHeader("Content-Type", "application/octet-stream");
    response.setHeader("Content-Length", Buffer.byteLength(body));
    response.end(body);
    return;
  }
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
  // The lifestyle article proves a `life` row lands under /life/, not /guides/life/.
  // The web reads one child sitemap at a time (`?section=&locale=`, paged by `cursor`) and the
  // index reads `/summary`; both come from this one row list so they cannot disagree.
  if (request.method === "GET" && request.url?.startsWith("/api/v1/guides/sitemap")) {
    const sitemapRows = [
      { kind: "intel", slug: "synthetic-fare-notice", locale: "zh-TW", published_at: "2026-09-08T09:30:00Z", locales: ["ja", "zh-TW"] },
      { kind: "intel", slug: "synthetic-fare-notice", locale: "ja", published_at: "2026-09-07T01:00:00Z", locales: ["ja", "zh-TW"] },
      { kind: "howto", slug: "synthetic-airport-transfer", locale: "en", published_at: "2026-09-01T00:00:00Z", locales: ["en"] },
      { kind: "life", slug: "synthetic-ai-notes", locale: "zh-TW", published_at: "2026-09-05T08:00:00Z", locales: ["zh-TW"] },
    ];
    const sitemapUrl = new URL(request.url, "http://127.0.0.1:8000");
    if (sitemapUrl.pathname === "/api/v1/guides/sitemap/summary") {
      const counts = new Map();
      for (const row of sitemapRows) {
        const key = `${row.kind}:${row.locale}`;
        counts.set(key, { kind: row.kind, locale: row.locale, count: (counts.get(key)?.count ?? 0) + 1 });
      }
      response.end(JSON.stringify({ counts: [...counts.values()] }));
      return;
    }
    const section = sitemapUrl.searchParams.get("section");
    const locale = sitemapUrl.searchParams.get("locale");
    const sectionOf = (kind) => (kind === "life" ? "life" : "travel");
    const entries = sitemapRows.filter((row) =>
      (!section || sectionOf(row.kind) === section) && (!locale || row.locale === locale));
    response.end(JSON.stringify({ entries, next_cursor: null }));
    return;
  }
  // The listing behind the section hubs, published exactly where /guides/sitemap above says
  // those articles exist. A hub's robots rule and the sitemap's hub filter read these two
  // endpoints separately, so a language must not look empty to one and full to the other.
  if (request.method === "GET" && request.url?.startsWith("/api/v1/guides?")) {
    const parameters = new URL(request.url, "http://127.0.0.1:8000").searchParams;
    const kind = parameters.get("kind") === "life" ? "life"
      : parameters.get("kind") === "howto" ? "howto" : "intel";
    const publishedIn = { intel: ["zh-TW", "ja"], howto: ["en"], life: ["zh-TW"] };
    const published = publishedIn[kind].includes(parameters.get("locale"))
      ? [{
          slug: `synthetic-${kind}-listing`, kind,
          title: `Synthetic ${kind} listing`, description: "Synthetic fixture summary",
          published_at: "2026-09-08T09:30:00Z", valid_until: null, featured: false,
          destination_id: "tokyo", destination_label: "Tokyo", topics: [],
        }]
      : [];
    response.end(JSON.stringify({ articles: published, next_cursor: null }));
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
  if (serveShortsFixture(request, response, requestUrl)) return;
  if (request.method === "GET" && requestUrl.pathname === "/api/v1/community/status") {
    response.end(JSON.stringify({ enabled: false, posting_enabled: false, comments_enabled: false,
      messaging_enabled: false, translation_enabled: false, pet_reports_enabled: false }));
    return;
  }
  // Signed-in layouts ask for saved items even on an administrator page.
  if (request.method === "GET" && requestUrl.pathname === "/api/v1/saved-items") {
    response.end(JSON.stringify({ items: [] }));
    return;
  }
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
  // Advertising off, like production and like the default. Unknown paths answer 404, and a
  // 404 here would fail `admin-operations` (it counts this site's 4xx responses) and
  // `korea-dual-maps` (it counts console errors). The specs that assert zero external
  // requests depend on this staying "off"; `guides-adsense.spec.ts` turns it on per test.
  if (request.method === "GET" && requestUrl.pathname === "/api/v1/ads/config") {
    response.end(JSON.stringify({ enabled: false, publisher_id: null, slot_id: null, cmp_enabled: false }));
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
