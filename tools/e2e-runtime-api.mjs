import { createServer } from "node:http";

const visibility = {
  hotspots_enabled: true,
  trips_enabled: true,
  alerts_enabled: true,
  flight_status_enabled: true,
  airline_fares_enabled: true,
  pricing_enabled: true,
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
  response.statusCode = 404;
  response.end(JSON.stringify({ detail: "not found" }));
});

server.listen(8000, "127.0.0.1");

for (const signal of ["SIGINT", "SIGTERM"]) {
  process.on(signal, () => server.close(() => process.exit(0)));
}
