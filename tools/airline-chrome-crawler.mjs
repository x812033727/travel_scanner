#!/usr/bin/env node

import { createHash } from "node:crypto";
import { writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { chromium } from "@playwright/test";

const AIRLINE_CODES = new Set(["CI", "BR", "JX"]);
const CABIN_CLASSES = new Set(["economy", "premium_economy", "business", "first"]);

function isIsoDate(value) {
  if (!/^\d{4}-\d{2}-\d{2}$/.test(value)) return false;
  const parsed = new Date(`${value}T00:00:00Z`);
  return !Number.isNaN(parsed.valueOf()) && parsed.toISOString().slice(0, 10) === value;
}

export function normalizeApiBase(value) {
  const parsed = new URL(value);
  const localHttp = parsed.protocol === "http:" && ["127.0.0.1", "localhost"].includes(parsed.hostname);
  if (parsed.protocol !== "https:" && !localHttp) {
    throw new Error("API must use HTTPS unless it is localhost");
  }
  const pathname = parsed.pathname.replace(/\/$/, "");
  parsed.pathname = pathname.endsWith("/api/v1") ? pathname : `${pathname}/api/v1`;
  parsed.search = "";
  parsed.hash = "";
  return parsed.toString().replace(/\/$/, "");
}

function takeValue(argv, index, flag) {
  const value = argv[index + 1];
  if (!value || value.startsWith("--")) throw new Error(`${flag} requires a value`);
  return value;
}

export function parseArgs(argv, env = process.env) {
  const options = {
    apiBase: "http://127.0.0.1:8000",
    token: env.TRAVEL_SCANNER_TOKEN || "",
    email: env.TRAVEL_SCANNER_EMAIL || "",
    password: env.TRAVEL_SCANNER_PASSWORD || "",
    origin: "TPE",
    destination: "NRT",
    departureDate: null,
    returnDate: null,
    flexDays: 7,
    cabinClass: "economy",
    airlines: ["CI", "BR", "JX"],
    limitPerAirline: 10,
    channel: "chrome",
    headed: false,
    strict: false,
    timeoutMs: 30_000,
    output: "",
    help: false,
  };

  const valueFlags = new Map([
    ["--api-base", "apiBase"],
    ["--token", "token"],
    ["--email", "email"],
    ["--origin", "origin"],
    ["--destination", "destination"],
    ["--departure-date", "departureDate"],
    ["--return-date", "returnDate"],
    ["--flex-days", "flexDays"],
    ["--cabin", "cabinClass"],
    ["--airlines", "airlines"],
    ["--limit", "limitPerAirline"],
    ["--channel", "channel"],
    ["--timeout-ms", "timeoutMs"],
    ["--output", "output"],
  ]);

  for (let index = 0; index < argv.length; index += 1) {
    const flag = argv[index];
    if (flag === "--headed") options.headed = true;
    else if (flag === "--strict") options.strict = true;
    else if (flag === "--help" || flag === "-h") options.help = true;
    else if (valueFlags.has(flag)) {
      const key = valueFlags.get(flag);
      options[key] = takeValue(argv, index, flag);
      index += 1;
    } else {
      throw new Error(`Unknown option: ${flag}`);
    }
  }

  options.apiBase = normalizeApiBase(options.apiBase);
  options.origin = String(options.origin).toUpperCase();
  options.destination = String(options.destination).toUpperCase();
  options.airlines = String(options.airlines)
    .split(",")
    .map((code) => code.trim().toUpperCase())
    .filter(Boolean);
  options.flexDays = Number(options.flexDays);
  options.limitPerAirline = Number(options.limitPerAirline);
  options.timeoutMs = Number(options.timeoutMs);

  if (!/^[A-Z]{3}$/.test(options.origin) || !/^[A-Z]{3}$/.test(options.destination)) {
    throw new Error("Origin and destination must be three-letter airport codes");
  }
  if (options.origin === options.destination) throw new Error("Origin and destination must differ");
  if (options.departureDate && !isIsoDate(options.departureDate)) {
    throw new Error("Departure date must be a valid ISO date");
  }
  if (options.returnDate && !isIsoDate(options.returnDate)) {
    throw new Error("Return date must be a valid ISO date");
  }
  if (options.returnDate && !options.departureDate) {
    throw new Error("Return date requires a departure date");
  }
  if (options.returnDate && options.returnDate < options.departureDate) {
    throw new Error("Return date must not be before departure date");
  }
  if (!CABIN_CLASSES.has(options.cabinClass)) {
    throw new Error("Cabin must be economy, premium_economy, business, or first");
  }
  if (!options.airlines.length || options.airlines.some((code) => !AIRLINE_CODES.has(code))) {
    throw new Error("Airlines must be a comma-separated subset of CI,BR,JX");
  }
  if (!Number.isInteger(options.flexDays) || options.flexDays < 0 || options.flexDays > 30) {
    throw new Error("Flex days must be an integer from 0 to 30");
  }
  if (!Number.isInteger(options.limitPerAirline) || options.limitPerAirline < 1 || options.limitPerAirline > 30) {
    throw new Error("Limit must be an integer from 1 to 30");
  }
  if (!Number.isInteger(options.timeoutMs) || options.timeoutMs < 5_000 || options.timeoutMs > 120_000) {
    throw new Error("Timeout must be an integer from 5000 to 120000 milliseconds");
  }
  if (!["chrome", "chromium"].includes(options.channel)) {
    throw new Error("Channel must be chrome or chromium");
  }
  return options;
}

export function buildQuery(options) {
  return {
    origin: options.origin,
    destination: options.destination,
    departure_date: options.departureDate,
    return_date: options.returnDate,
    flex_days: options.flexDays,
    cabin_class: options.cabinClass,
    airlines: options.airlines,
    limit_per_airline: options.limitPerAirline,
  };
}

async function requestJson(url, { method = "GET", token = "", body } = {}) {
  const headers = { Accept: "application/json" };
  if (body !== undefined) headers["Content-Type"] = "application/json";
  if (token) headers.Authorization = `Bearer ${token}`;
  const response = await fetch(url, {
    method,
    headers,
    body: body === undefined ? undefined : JSON.stringify(body),
  });
  const text = await response.text();
  let payload;
  try {
    payload = text ? JSON.parse(text) : null;
  } catch {
    payload = { detail: text || `HTTP ${response.status}` };
  }
  if (!response.ok) {
    const detail = payload?.detail || payload?.code || `HTTP ${response.status}`;
    throw new Error(`${response.status} ${detail}`);
  }
  return payload;
}

async function resolveToken(options) {
  if (options.token) return options.token;
  if (!options.email || !options.password) {
    throw new Error(
      "Set TRAVEL_SCANNER_TOKEN, or set TRAVEL_SCANNER_EMAIL and TRAVEL_SCANNER_PASSWORD",
    );
  }
  const response = await requestJson(`${options.apiBase}/auth/login`, {
    method: "POST",
    body: { email: options.email, password: options.password },
  });
  if (!response?.access_token) throw new Error("Login response did not include an access token");
  return response.access_token;
}

export async function runChromeCrawler(options) {
  const token = await resolveToken(options);
  const query = buildQuery(options);
  const prepared = await requestJson(`${options.apiBase}/crawlers/airlines/browser-targets`, {
    method: "POST",
    token,
    body: query,
  });
  const launchOptions = { headless: !options.headed };
  if (options.channel === "chrome") launchOptions.channel = "chrome";
  const browserEnv = { ...process.env };
  delete browserEnv.TRAVEL_SCANNER_TOKEN;
  delete browserEnv.TRAVEL_SCANNER_EMAIL;
  delete browserEnv.TRAVEL_SCANNER_PASSWORD;
  launchOptions.env = browserEnv;

  let browser;
  try {
    browser = await chromium.launch(launchOptions);
  } catch (error) {
    if (options.channel === "chrome") {
      throw new Error(
        `Google Chrome could not be started. Install Chrome or retry with --channel chromium. ${error.message}`,
      );
    }
    throw error;
  }

  const results = [];
  const skipped = [];
  const failures = [];
  try {
    const context = await browser.newContext({ locale: "zh-TW" });
    for (const target of prepared.targets) {
      if (!target.source_url || target.state !== "ready") {
        skipped.push({
          airline_code: target.airline_code,
          state: target.state,
          detail: target.detail,
        });
        continue;
      }
      const page = await context.newPage();
      try {
        console.error(`[${target.airline_code}] Chrome opening ${target.host}`);
        const navigation = await page.goto(target.source_url, {
          waitUntil: "domcontentloaded",
          timeout: options.timeoutMs,
        });
        if (navigation && navigation.status() >= 400) {
          throw new Error(`official page returned HTTP ${navigation.status()}`);
        }
        await page.locator("#__NEXT_DATA__").waitFor({
          state: "attached",
          timeout: options.timeoutMs,
        });
        const nextData = await page.locator("#__NEXT_DATA__").textContent();
        if (!nextData) throw new Error("official page did not expose __NEXT_DATA__");
        const fareRows = await page.locator("#__NEXT_DATA__").evaluate((node) => {
          const fields = [
            "originAirportCode",
            "destinationAirportCode",
            "departureDate",
            "returnDate",
            "flightType",
            "farenetTravelClass",
            "formattedTravelClass",
            "currencyCode",
            "totalPrice",
            "priceLastSeen",
          ];
          const rows = [];
          const visit = (value) => {
            if (Array.isArray(value)) {
              value.forEach(visit);
              return;
            }
            if (!value || typeof value !== "object") return;
            for (const [key, child] of Object.entries(value)) {
              if (key === "fares" && Array.isArray(child)) {
                for (const row of child) {
                  if (!row || typeof row !== "object" || Array.isArray(row)) continue;
                  const selected = {};
                  for (const field of fields) {
                    if (field === "priceLastSeen") {
                      const lastSeen = row[field];
                      if (lastSeen && typeof lastSeen === "object" && !Array.isArray(lastSeen)) {
                        selected[field] = { value: lastSeen.value, unit: lastSeen.unit };
                      }
                    } else if (row[field] !== undefined) selected[field] = row[field];
                  }
                  rows.push(selected);
                }
              }
              visit(child);
            }
          };
          visit(JSON.parse(node.textContent || "{}"));
          const unique = new Map(rows.map((row) => [JSON.stringify(row), row]));
          return [...unique.values()];
        });
        if (fareRows.length > 2_000) {
          throw new Error(`official page exposed too many fare rows (${fareRows.length})`);
        }
        const capture = {
          airline_code: target.airline_code,
          query,
          source_url: page.url(),
          page_title: await page.title(),
          captured_at: new Date().toISOString(),
          fare_rows: fareRows,
        };
        const parsed = await requestJson(`${options.apiBase}/crawlers/airlines/browser-captures`, {
          method: "POST",
          token,
          body: capture,
        });
        results.push(parsed);
        const documentDigest = createHash("sha256").update(nextData).digest("hex").slice(0, 12);
        console.error(
          `[${target.airline_code}] Chrome extracted ${fareRows.length} row(s); ` +
            `API parsed ${parsed.quotes.length} public fare(s); document ${documentDigest}`,
        );
      } catch (error) {
        failures.push({ airline_code: target.airline_code, detail: error.message });
        console.error(`[${target.airline_code}] ${error.message}`);
      } finally {
        await page.close();
      }
    }
  } finally {
    await browser.close();
  }

  const report = {
    captured_at: new Date().toISOString(),
    browser: options.channel,
    query,
    quotes: results.flatMap((result) => result.quotes),
    sources: results.flatMap((result) => result.sources),
    capture_sha256: results.map((result) => result.capture_sha256),
    skipped,
    failures,
  };
  if (options.output) {
    await writeFile(options.output, `${JSON.stringify(report, null, 2)}\n`, "utf8");
  }
  return report;
}

export function helpText() {
  return `Travel Scanner Chrome airline crawler

Usage:
  npm run crawl:airlines:chrome -- [options]

Authentication (prefer environment variables):
  TRAVEL_SCANNER_TOKEN
  TRAVEL_SCANNER_EMAIL and TRAVEL_SCANNER_PASSWORD

Options:
  --api-base URL           API root (default http://127.0.0.1:8000)
  --origin TPE             Origin airport
  --destination NRT        Destination airport
  --departure-date DATE    ISO date
  --return-date DATE       ISO date
  --flex-days N            Date window, 0-30
  --cabin CLASS            economy, premium_economy, business, first
  --airlines CI,BR,JX      Requested official sources
  --limit N                Quotes per airline, 1-30
  --channel chrome|chromium Browser binary (default Google Chrome)
  --headed                 Show the isolated Chrome window
  --timeout-ms N           Navigation timeout, 5000-120000
  --output FILE            Save the normalized JSON report
  --strict                 Exit non-zero when a ready target fails
`;
}

async function main() {
  const options = parseArgs(process.argv.slice(2));
  if (options.help) {
    console.log(helpText());
    return;
  }
  const report = await runChromeCrawler(options);
  console.log(JSON.stringify(report, null, 2));
  if (options.strict && report.failures.length) process.exitCode = 2;
}

const isMain = process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url);
if (isMain) {
  main().catch((error) => {
    console.error(error.message);
    process.exitCode = 1;
  });
}
