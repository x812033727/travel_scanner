// CI-only probe: no Google account, media, or production secrets are involved.
import assert from "node:assert/strict";
import { readFileSync, writeFileSync } from "node:fs";

assert.equal(process.getuid(), 10001, "probe must use the production API UID");
const filename = "/run/mokaair-uploader/service-secret";
const secret = readFileSync(filename, "utf8").trim();
assert.ok(secret.length >= 32);
assert.throws(() => writeFileSync("/run/mokaair-uploader/mount-must-be-readonly", "probe"), { code: "EROFS" });
const url = "http://mokaair-studio-uploader:8789/status";
const denied = await fetch(url, { signal: AbortSignal.timeout(5000) });
assert.equal(denied.status, 401, "RPC must refuse missing authentication");
const accepted = await fetch(url, {
  headers: { authorization: `Bearer ${secret}` },
  signal: AbortSignal.timeout(5000),
});
assert.equal(accepted.status, 200, "API UID must authenticate using its mounted file");
const status = await accepted.json();
assert.equal(status.channel_id, process.env.UPLOADER_CHANNEL_ID);
console.log("API UID, read-only secret, Docker DNS and authenticated channel status passed");
