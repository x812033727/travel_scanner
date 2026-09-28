import http from "node:http";
import { timingSafeEqual } from "node:crypto";
import { CHUNK, HASH, Refused, SLUG, VIDEO, validateManifest } from "./contract.mjs";

async function body(request, limit) {
  const parts = []; let size = 0;
  for await (const chunk of request) {
    size += chunk.length;
    if (size > limit) throw new Refused("body_too_large", 413);
    parts.push(chunk);
  }
  return Buffer.concat(parts);
}
export function createServer({ store, secret, channel, runner }) {
  if (secret.length < 32) throw new Error("Service secret must contain at least 32 characters");
  const expected = Buffer.from("Bearer " + secret);
  return http.createServer(async (req, res) => {
    const send = (status, value) => {
      res.writeHead(status, { "Content-Type": "application/json", "Cache-Control": "no-store", "X-Content-Type-Options": "nosniff" });
      res.end(JSON.stringify(value));
    };
    try {
      const url = new URL(req.url, "http://localhost");
      if (req.method === "GET" && url.pathname === "/health") return send(200, { ready: true });
      const supplied = Buffer.from(req.headers.authorization || "");
      if (supplied.length !== expected.length || !timingSafeEqual(supplied, expected)) throw new Refused("unauthorized", 401);
      if (req.method === "GET" && url.pathname === "/status") return send(200, { channel_id: channel, browser: runner?.status ?? "stopped" });
      const project = /^\/projects\/([^/]+)$/.exec(url.pathname);
      if (project && req.method === "GET") {
        if (!SLUG.test(project[1])) throw new Refused("invalid_slug", 422);
        const job = store.latest(project[1]);
        return send(200, { job: job ? store.view(job) : null });
      }
      const match = /^\/jobs\/([a-f0-9]{64})(?:\/(queue|resume|cancel|files\/([a-f0-9]{64})))?$/.exec(url.pathname);
      if (!match || !HASH.test(match[1])) throw new Refused("not_found", 404);
      const [, id, action, sha] = match;
      if (req.method === "GET" && !action) return send(200, store.view(store.get(id)));
      if (req.method === "PUT" && !action) {
        const manifest = validateManifest(JSON.parse((await body(req, 100_000)).toString("utf8")), channel);
        return send(200, store.view(store.create(id, manifest)));
      }
      if (req.method === "PUT" && sha) {
        const offset = url.searchParams.get("offset");
        if (!offset || !/^(0|[1-9][0-9]*)$/.test(offset)) throw new Refused("invalid_offset", 422);
        return send(200, await store.put(id, sha, Number(offset), await body(req, CHUNK)));
      }
      if (req.method === "POST" && action === "queue") return send(200, await store.queue(id));
      if (req.method === "POST" && ["resume", "cancel"].includes(action)) {
        const bytes = await body(req, 1000);
        const value = bytes.length ? JSON.parse(bytes.toString("utf8")) : {};
        if (!value || typeof value !== "object" || Array.isArray(value)) throw new Refused("invalid_json", 422);
        if (value.video_id != null && !VIDEO.test(value.video_id)) throw new Refused("invalid_video", 422);
        return send(200, action === "resume" ? store.resume(id, value.video_id) : store.cancel(id, value.video_id));
      }
      throw new Refused("method_not_allowed", 405);
    } catch (e) {
      // Never return exception messages, browser URLs, credentials or stack traces.
      send(e instanceof Refused ? e.status : e instanceof SyntaxError ? 422 : 500,
        { code: e instanceof Refused ? e.code : e instanceof SyntaxError ? "invalid_json" : "service_error" });
    }
  });
}
