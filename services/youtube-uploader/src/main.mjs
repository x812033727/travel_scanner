import { readFileSync, mkdirSync } from "node:fs";
import path from "node:path";
import { chromium } from "playwright";
import { CHANNEL } from "./contract.mjs";
import { Store } from "./store.mjs";
import { Studio, readSelectors } from "./studio.mjs";
import { Runner } from "./runner.mjs";
import { createServer } from "./server.mjs";

const directory = process.env.UPLOADER_DATA_DIR || "/var/lib/mokaair-uploader";
const secret = readFileSync(process.env.UPLOADER_SECRET_FILE || "/run/secrets/uploader", "utf8").trim();
const channel = process.env.UPLOADER_CHANNEL_ID || "";
if (!CHANNEL.test(channel)) throw new Error("UPLOADER_CHANNEL_ID must be an exact channel ID");
const profile = path.join(directory, "browser");
mkdirSync(profile, { recursive: true, mode: 0o700 });
const store = new Store(directory);
const driver = new Studio({ store, profile, chromium, selectors: readSelectors(process.env.UPLOADER_SELECTORS_FILE) });
const runner = new Runner(store, driver);
const server = createServer({ store, secret, channel, runner });
const port = Number(process.env.UPLOADER_PORT || 8789);
server.requestTimeout = 60_000;
server.headersTimeout = 15_000;
server.listen(port, process.env.UPLOADER_BIND || "127.0.0.1");
// Open the dedicated browser for the owner's first login; never enter credentials ourselves.
await driver.connect();
await driver.page.goto("https://studio.youtube.com", { waitUntil: "domcontentloaded" }).catch(() => {});
const timer = setInterval(() => void runner.tick().catch(() => { runner.status = "error"; }), 2000);
let closing = false;
async function stop() {
  if (closing) return;
  closing = true; clearInterval(timer);
  server.close();
  await driver.close();
  // Wait for the interrupted job to record its needs_action checkpoint.
  while (runner.busy) await new Promise((resolve) => setTimeout(resolve, 100));
  store.close(); process.exit(0);
}
process.on("SIGTERM", () => void stop());
process.on("SIGINT", () => void stop());
