import assert from "node:assert/strict";
import test from "node:test";

import { buildQuery, normalizeApiBase, parseArgs } from "./airline-chrome-crawler.mjs";

test("normalizes local and hosted API roots safely", () => {
  assert.equal(normalizeApiBase("http://127.0.0.1:8000"), "http://127.0.0.1:8000/api/v1");
  assert.equal(normalizeApiBase("https://travel.example/api/v1/"), "https://travel.example/api/v1");
  assert.throws(() => normalizeApiBase("http://travel.example"), /HTTPS/);
});

test("parses a bounded airline query for the Chrome bridge", () => {
  const options = parseArgs(
    [
      "--origin",
      "tpe",
      "--destination",
      "nrt",
      "--departure-date",
      "2026-11-10",
      "--return-date",
      "2026-11-15",
      "--airlines",
      "CI,JX",
      "--flex-days",
      "3",
      "--limit",
      "4",
    ],
    {},
  );
  assert.deepEqual(buildQuery(options), {
    origin: "TPE",
    destination: "NRT",
    departure_date: "2026-11-10",
    return_date: "2026-11-15",
    flex_days: 3,
    cabin_class: "economy",
    airlines: ["CI", "JX"],
    limit_per_airline: 4,
  });
});

test("rejects arbitrary airline codes and unsafe remote HTTP APIs", () => {
  assert.throws(() => parseArgs(["--airlines", "CI,XX"], {}), /CI,BR,JX/);
  assert.throws(() => parseArgs(["--api-base", "http://example.com"], {}), /HTTPS/);
  assert.throws(() => parseArgs(["--cabin", "private_jet"], {}), /Cabin/);
  assert.throws(
    () => parseArgs(["--return-date", "2026-11-15"], {}),
    /requires a departure date/,
  );
});
