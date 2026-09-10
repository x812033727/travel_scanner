// Manual browser fixture only. In-memory state, loopback binding, no external requests.
// Start Next separately with API_INTERNAL_URL=http://127.0.0.1:8112.
import { createServer } from "node:http";

const port = 8112;
const day = "2026-11-11";
const user = { id: "fixture-user", email: "fixture@example.test", role: "user", is_active: true, is_admin: false, preferred_locale: "zh-TW" };
const session = "korea-local-fixture-session";
const requests = [];
const idempotency = new Map();
const previews = new Map();
const candidates = new Map();
const visibility = { hotspots_enabled: true, trips_enabled: true, alerts_enabled: true, flight_status_enabled: true, airline_fares_enabled: true, pricing_enabled: true };

function makeTrip(city) {
  const seoul = city === "seoul";
  const labels = seoul ? ["首爾飯店 서울 호텔", "景福宮 경복궁", "北村韓屋村 북촌한옥마을"] : ["釜山飯店 부산 호텔", "海雲臺 해운대", "海東龍宮寺 해동용궁사"];
  const items = labels.map((title, index) => ({
    id: `${city}-${index}`, item_type: "custom", day_date: day, position: index,
    title: `【合成測試】${title}`, location_name: title,
    latitude: (seoul ? 37.57 : 35.16) + index * .002, longitude: (seoul ? 126.97 : 129.16) + index * .002,
    locked: false, is_estimated: false, location_source: "confirmed", location_provider: "naver_local",
    provider_place_id: `fixture-naver-${city}-${index}`, duration_minutes: 60,
    fixed_time: false, start_time: `${day}T09:00:00+09:00`, data: { place_provider: "naver_local", fixture_only: true },
    map_identities: { naver_maps: { provider: "naver_maps", place_id: String(9_900_000_000 + (seoul ? 0 : 100) + index), map_url: `https://map.naver.com/p/entry/place/${9_900_000_000 + (seoul ? 0 : 100) + index}`, status: "verified", verified_at: "2026-09-10T00:00:00Z" } },
  }));
  return {
    id: `fixture-${city}`, name: `【合成測試・無外部供應商】${seoul ? "首爾" : "釜山"}雙地圖`, mode: "manual",
    destination_name: seoul ? "韓國首爾" : "韓國釜山", destination_country_code: "KR", timezone: "Asia/Seoul",
    total_price: 0, currency: "TWD", version: 1, start_date: day, end_date: day,
    data: { fixture_only: true }, share_enabled: false, items, route_segments: [],
    routing: { status: "idle", total: 2, completed: 0, day_settings: [{ day_date: day, default_travel_mode: "transit", default_buffer_minutes: 10, route_preference: "FEWER_TRANSFERS", auto_compute: false }] },
  };
}
const trips = new Map(["seoul", "busan"].map((city) => { const trip = makeTrip(city); return [trip.id, trip]; }));

function publicFixture(value) {
  if (Array.isArray(value)) return value.map(publicFixture);
  if (!value?.data?.fixture_only || !Array.isArray(value.items)) return value;
  return { ...value, items: value.items.map((item) => ({ ...item, location_map_links: [
    { provider: "naver", url: item.map_identities.naver_maps.map_url, position_only: false },
    { provider: "google", url: item.map_identities.google_places?.map_url || `https://www.google.com/maps/search/?api=1&query=${item.latitude},${item.longitude}`, position_only: !item.map_identities.google_places },
  ] })) };
}

function navigation(trip, fromId, toId, mode) {
  const from = trip.items.find((item) => item.id === fromId);
  const to = trip.items.find((item) => item.id === toId);
  if (!from || !to || !["transit", "walk", "drive"].includes(mode)) return { external_navigations: [] };
  const googleParams = new URLSearchParams({ api: "1", origin: `${from.latitude},${from.longitude}`, destination: `${to.latitude},${to.longitude}`, travelmode: mode === "walk" ? "walking" : "transit" });
  const naverParams = new URLSearchParams({ slat: String(from.latitude), slng: String(from.longitude), sname: from.title, dlat: String(to.latitude), dlng: String(to.longitude), dname: to.title, appname: "korea-local-fixture" });
  const external_navigations = [{ provider: "naver_maps", label: "NAVER Maps", travel_mode: mode, web_url: `https://map.naver.com/p/directions/${from.longitude},${from.latitude},${encodeURIComponent(from.title)}/${to.longitude},${to.latitude},${encodeURIComponent(to.title)}/-/${mode}`, app_url: `nmap://route/${mode === "transit" ? "public" : mode === "drive" ? "car" : "walk"}?${naverParams}`, reason: "合成測試連結；不是即時供應商結果。" }];
  if (mode !== "drive") external_navigations.push({ provider: "google_maps", label: "Google Maps", travel_mode: mode, web_url: `https://www.google.com/maps/dir/?${googleParams}`, app_url: `https://www.google.com/maps/dir/?${googleParams}` });
  if (mode === "transit") external_navigations.reverse();
  return { external_navigations, map_capabilities: { providers: mode === "walk" ? ["naver_maps", "google_maps"] : [mode === "transit" ? "google_maps" : "naver_maps"], default_provider: mode === "transit" ? "google_maps" : "naver_maps" } };
}

function routeSegment(trip, body, manual = false) {
  return { from_item_id: body.from_item_id, to_item_id: body.to_item_id, travel_mode: body.travel_mode,
    status: manual ? "manual" : "complete", provider: manual ? "manual" : body.travel_mode === "transit" ? "odsay" : "naver_maps",
    attribution: manual ? "手動輸入" : body.travel_mode === "transit" ? "ODsay（合成測試，未呼叫供應商）" : "NAVER（合成測試，未呼叫供應商）",
    duration_minutes: manual ? body.duration_minutes : 24, buffer_minutes: body.buffer_minutes,
    generated_at: new Date().toISOString(), schedule_mode: "preview", preference: "FEWER_TRANSFERS",
    encoded_polyline: null, steps: [], details_available: [], warnings: ["僅供本機介面測試；非真實交通資料。"],
    ...navigation(trip, body.from_item_id, body.to_item_id, body.travel_mode) };
}

async function readBody(request) {
  const chunks = [];
  let bytes = 0;
  for await (const chunk of request) {
    bytes += chunk.length;
    if (bytes > 65_536) throw new Error("Fixture payload too large");
    chunks.push(chunk);
  }
  return chunks.length ? JSON.parse(Buffer.concat(chunks).toString("utf8")) : {};
}

const server = createServer(async (request, response) => {
  response.setHeader("Content-Type", "application/json; charset=utf-8");
  response.setHeader("Cache-Control", "no-store");
  const url = new URL(request.url || "/", `http://127.0.0.1:${port}`);
  const path = url.pathname;
  const send = (payload, status = 200) => { response.statusCode = status; response.end(JSON.stringify(publicFixture(payload))); };
  requests.push({ method: request.method, path });
  try {
    if (path === "/fixture/state") return send({ fixture_only: true, requests, trips: [...trips.values()] });
    if (path === "/api/v1/runtime/site-visibility") return send(visibility);
    if (path === "/api/v1/runtime/ui-text") return send({ locale: url.searchParams.get("locale") || "zh-TW", version: "korea-fixture", entries: {} });
    if (path === "/api/v1/runtime/public-config") return send({ google_maps_browser_key: null, google_maps_javascript_enabled: false, google_maps_embed_enabled: false, naver_maps_browser_client_id: null, naver_dynamic_map_enabled: false, odsay_enabled: true, naver_directions_enabled: true });
    if (path === "/api/v1/auth/registration-status") return send({ registration_enabled: false });
    if (path === "/api/v1/auth/oauth/providers") return send({ providers: { google: false, line: false, apple: false } });
    if (path === "/api/v1/analytics/config") return send({ first_party_enabled: false, ga4_enabled: false });
    if (path === "/api/v1/auth/login" && request.method === "POST") {
      const body = await readBody(request);
      if (body.email !== user.email || body.password !== "Fixture-only-123") return send({ detail: "Use the documented local fixture credentials." }, 401);
      return send({ access_token: session, expires_in: 3600, user });
    }
    if (path === "/api/v1/auth/logout") return send({ ok: true });
    if (request.headers.authorization !== `Bearer ${session}` && !request.headers.cookie?.includes(`travel_access=${session}`)) return send({ detail: "Local fixture login required." }, 401);
    if (path === "/api/v1/auth/me") return send(user);
    if (path === "/api/v1/trips") return send([...trips.values()]);
    if (path === "/api/v1/usage") return send({ available_uses: 100, remaining_uses: 100, reserved_uses: 0 });
    if (path === "/api/v1/saved-items") return send([]);
    if (/\/community\/status$|\/discovery\/status$/.test(path)) return send({ enabled: false });
    if (path === "/api/v1/places/autocomplete") {
      const place_id = `fixture-google-place-${candidates.size + 1}`;
      const candidate = { provider: "google_places", place_id, name: url.searchParams.get("q") || "【合成測試】景福宮 경복궁", address: "合成測試地址・대한민국", latitude: Number(url.searchParams.get("latitude")) || 37.5796, longitude: Number(url.searchParams.get("longitude")) || 126.977, google_maps_url: `https://www.google.com/maps/search/?api=1&query_place_id=${place_id}`, attribution: "Google（合成測試）" };
      candidates.set(place_id, candidate);
      return send([candidate]);
    }
    if (path.startsWith("/api/v1/places/google_places/")) {
      const candidate = candidates.get(path.split("/").at(-1));
      return candidate ? send(candidate) : send({ detail: "Select a synthetic search result first." }, 404);
    }
    const match = path.match(/^\/api\/v1\/trips\/([^/]+)(.*)$/);
    const trip = match && trips.get(match[1]);
    if (!trip) return send({ detail: "Unknown local fixture endpoint." }, 404);
    const suffix = match[2];
    if (!suffix && request.method === "GET") return send(trip);
    if (suffix === "/health") return send({ days: [], issues: [] });
    if (suffix === "/routes/navigation") return send(navigation(trip, url.searchParams.get("from_item_id"), url.searchParams.get("to_item_id"), url.searchParams.get("travel_mode")));
    if (request.method !== "POST") return send({ detail: "Unknown local fixture endpoint." }, 404);
    const body = await readBody(request);
    const key = request.headers["idempotency-key"];
    if (key && idempotency.has(key)) return send(idempotency.get(key));
    if (body.version !== trip.version) return send({ code: "trip_version_conflict", detail: "Fixture version changed." }, 409);
    if (suffix === "/routes/preview") {
      const links = navigation(trip, body.from_item_id, body.to_item_id, body.travel_mode);
      if (body.travel_mode === "walk") return send({ kind: "external_only", preview_id: null, expires_at: null, segment: null, schedule_impact: null, ...links });
      const previewId = `fixture-preview-${trip.id}-${previews.size + 1}`;
      const segment = routeSegment(trip, body);
      previews.set(previewId, segment);
      return send({ kind: "provider", preview_id: previewId, expires_at: "2100-01-01T00:00:00Z", segment, schedule_impact: { affected_items: [], conflicts: [] }, ...links });
    }
    if (suffix === "/routes/apply") {
      const segment = body.source === "manual" ? routeSegment(trip, body, true) : previews.get(body.preview_id);
      if (!segment) return send({ detail: "Query a fixture route first." }, 409);
      trip.route_segments = [segment];
      trip.routing.status = "complete";
      trip.version += 1;
      if (key) idempotency.set(key, structuredClone(trip));
      return send(trip);
    }
    const identityMatch = suffix.match(/^\/items\/([^/]+)\/map-identities$/);
    if (identityMatch) {
      const item = trip.items.find((row) => row.id === identityMatch[1]);
      if (!item || !body.confirmed_same_place || body.provider !== "google_places") return send({ detail: "Confirm the same synthetic place." }, 422);
      item.map_identities.google_places = { provider: "google_places", place_id: body.place_id, map_url: `https://www.google.com/maps/search/?api=1&query_place_id=${encodeURIComponent(body.place_id)}`, status: "verified", verified_at: new Date().toISOString() };
      trip.version += 1;
      if (key) idempotency.set(key, structuredClone(trip));
      return send(trip);
    }
    return send({ detail: "Unknown local fixture endpoint." }, 404);
  } catch (error) { return send({ detail: error instanceof Error ? error.message : "Fixture failure" }, 400); }
});

server.listen(port, "127.0.0.1", () => {
  console.log(`SYNTHETIC KOREA MAP FIXTURE ONLY | PID ${process.pid} | http://127.0.0.1:${port}`);
  console.log("No external requests, provider keys, database or production state. Login: fixture@example.test / Fixture-only-123");
});
for (const signal of ["SIGINT", "SIGTERM"]) process.on(signal, () => server.close(() => process.exit(0)));
