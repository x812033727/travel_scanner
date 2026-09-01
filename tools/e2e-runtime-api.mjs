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

const server = createServer((request, response) => {
  response.setHeader("Cache-Control", "no-store");
  response.setHeader("Content-Type", "application/json");
  if (request.method === "GET" && request.url === "/api/v1/runtime/site-visibility") {
    response.end(JSON.stringify(visibility));
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
  response.statusCode = 404;
  response.end(JSON.stringify({ detail: "not found" }));
});

server.listen(8000, "127.0.0.1");

for (const signal of ["SIGINT", "SIGTERM"]) {
  process.on(signal, () => server.close(() => process.exit(0)));
}
