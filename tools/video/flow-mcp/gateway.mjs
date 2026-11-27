#!/usr/bin/env node
/**
 * Loopback-only HTTP JSON-RPC 2.0 MCP Gateway hosting both `mokaair-flow`
 * (22 tools) and `mokaair-flow-music` (17 tools) behind HMAC-SHA256 signed
 * requests from `apps/api` (`POST /api/v1/video/mcp/{flow|flow-music}`).
 *
 * Security invariants:
 *   - Binds strictly to 127.0.0.1 (or ::1), NEVER 0.0.0.0.
 *   - Requires `FLOW_MCP_GATEWAY_SECRET` (>= 32 chars) and verifies
 *     `X-Mokaair-Timestamp`, `X-Mokaair-Nonce`, and `X-Mokaair-Signature`
 *     using constant-time comparison + replay window (±300s).
 *   - Preserves persistent `FlowOrchestrator` & `FlowMusicOrchestrator`
 *     instances so async `flow_wait` / `music_wait` jobs survive across HTTP calls.
 */

import { createHash, createHmac, timingSafeEqual } from "node:crypto";
import fs from "node:fs";
import http from "node:http";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { FlowMusicOrchestrator } from "../flow-music-mcp/orchestrator.mjs";
import {
  createToolDispatcher as createMusicDispatcher,
  handleJsonRpcMessage as handleMusicRpc,
} from "../flow-music-mcp/server.mjs";
import { FlowOrchestrator } from "./orchestrator.mjs";
import {
  createToolDispatcher as createFlowDispatcher,
  handleJsonRpcMessage as handleFlowRpc,
} from "./server.mjs";

export const DEFAULT_GATEWAY_HOST = "127.0.0.1";
export const DEFAULT_GATEWAY_PORT = 8792;
export const MAX_RPC_BODY_BYTES = 1024 * 1024; // 1 MiB
export const TIMESTAMP_SKEW_SECONDS = 300;
const LOOPBACK_HOSTS = new Set(["127.0.0.1", "localhost", "::1"]);

export function signGatewayRequest({ secret, method, reqPath, bodyBuffer, timestamp = Math.floor(Date.now() / 1000), nonce }) {
  const body = Buffer.isBuffer(bodyBuffer) ? bodyBuffer : Buffer.from(bodyBuffer || "", "utf8");
  const digest = createHash("sha256").update(body).digest("hex");
  const message = `${timestamp}\n${nonce}\n${method.toUpperCase()}\n${reqPath}\n${digest}`;
  const signature = createHmac("sha256", secret).update(message).digest("hex");
  return {
    "x-mokaair-timestamp": String(timestamp),
    "x-mokaair-nonce": String(nonce),
    "x-mokaair-signature": signature,
  };
}

export function verifyGatewaySignature({
  secret,
  method,
  reqPath,
  bodyBuffer,
  headers,
  nowSec = Math.floor(Date.now() / 1000),
  seenNonces = new Map(),
}) {
  if (!secret || secret.length < 32) {
    return { ok: false, status: 503, code: "gateway_secret_unconfigured", message: "FLOW_MCP_GATEWAY_SECRET (>=32 chars) is not configured." };
  }
  const tsRaw = headers["x-mokaair-timestamp"];
  const nonce = String(headers["x-mokaair-nonce"] || "").trim();
  const providedSig = String(headers["x-mokaair-signature"] || "").trim().toLowerCase();

  const ts = Number(tsRaw);
  if (!Number.isInteger(ts) || Math.abs(nowSec - ts) > TIMESTAMP_SKEW_SECONDS) {
    return { ok: false, status: 401, code: "gateway_timestamp_invalid", message: "Request timestamp missing or outside ±300s window." };
  }
  if (!nonce || nonce.length < 8 || nonce.length > 128) {
    return { ok: false, status: 401, code: "gateway_nonce_invalid", message: "Request nonce missing or invalid." };
  }

  // Prune expired nonces and reject replays
  for (const [k, exp] of seenNonces.entries()) {
    if (exp <= nowSec) seenNonces.delete(k);
  }
  if (seenNonces.has(nonce)) {
    return { ok: false, status: 401, code: "gateway_nonce_replayed", message: "Request nonce has already been used." };
  }

  const expected = signGatewayRequest({ secret, method, reqPath, bodyBuffer, timestamp: ts, nonce })["x-mokaair-signature"];
  const a = Buffer.from(providedSig, "utf8");
  const b = Buffer.from(expected, "utf8");
  if (a.length !== b.length || !timingSafeEqual(a, b)) {
    return { ok: false, status: 401, code: "gateway_signature_invalid", message: "HMAC signature mismatch." };
  }

  seenNonces.set(nonce, nowSec + TIMESTAMP_SKEW_SECONDS);
  return { ok: true };
}

function readBody(req, maxBytes = MAX_RPC_BODY_BYTES) {
  return new Promise((resolve, reject) => {
    const chunks = [];
    let total = 0;
    req.on("data", (chunk) => {
      total += chunk.length;
      if (total > maxBytes) {
        req.destroy();
        reject(Object.assign(new Error("Request body exceeds 1 MiB limit"), { statusCode: 413 }));
        return;
      }
      chunks.push(chunk);
    });
    req.on("end", () => resolve(Buffer.concat(chunks)));
    req.on("error", reject);
  });
}

function sendJson(res, status, payload) {
  const body = JSON.stringify(payload);
  res.writeHead(status, {
    "Content-Type": "application/json; charset=utf-8",
    "Cache-Control": "no-store",
    "Content-Length": Buffer.byteLength(body, "utf8"),
  });
  res.end(body);
}

export function createGatewayServer({
  secret = process.env.FLOW_MCP_GATEWAY_SECRET || "",
  flowOrchestrator = new FlowOrchestrator(),
  musicOrchestrator = new FlowMusicOrchestrator(),
} = {}) {
  const flowDispatch = createFlowDispatcher(flowOrchestrator);
  const musicDispatch = createMusicDispatcher(musicOrchestrator);
  const seenNonces = new Map();
  const startedAt = Date.now();

  return http.createServer(async (req, res) => {
    const urlObj = new URL(req.url || "/", "http://127.0.0.1");
    const reqPath = urlObj.pathname;
    const method = (req.method || "GET").toUpperCase();

    let bodyBuffer;
    try {
      bodyBuffer = method === "POST" ? await readBody(req) : Buffer.alloc(0);
    } catch (err) {
      sendJson(res, err.statusCode || 400, { ok: false, code: "body_too_large", message: err.message });
      return;
    }

    const auth = verifyGatewaySignature({
      secret,
      method,
      reqPath,
      bodyBuffer,
      headers: req.headers,
      seenNonces,
    });
    if (!auth.ok) {
      sendJson(res, auth.status, { ok: false, code: auth.code, message: auth.message });
      return;
    }

    if (method === "GET" && reqPath === "/health") {
      sendJson(res, 200, {
        ok: true,
        services: ["flow", "flow-music"],
        uptimeSec: Math.round((Date.now() - startedAt) / 1000),
      });
      return;
    }

    if (method === "POST" && (reqPath === "/mcp/flow" || reqPath === "/mcp/flow-music")) {
      let msg;
      try {
        msg = JSON.parse(bodyBuffer.toString("utf8"));
      } catch {
        sendJson(res, 400, { jsonrpc: "2.0", id: null, error: { code: -32700, message: "Parse error" } });
        return;
      }

      try {
        const response =
          reqPath === "/mcp/flow"
            ? await handleFlowRpc(msg, { dispatch: flowDispatch })
            : await handleMusicRpc(msg, { dispatch: musicDispatch });

        if (response === null) {
          res.writeHead(202, { "Cache-Control": "no-store" });
          res.end();
          return;
        }
        sendJson(res, 200, response);
      } catch (err) {
        sendJson(res, 500, {
          jsonrpc: "2.0",
          id: msg?.id ?? null,
          error: { code: -32603, message: err?.message || "Internal error" },
        });
      }
      return;
    }

    sendJson(res, 404, { ok: false, code: "not_found", message: `Unknown gateway path: ${method} ${reqPath}` });
  });
}

export function startGatewayServer({
  host = process.env.FLOW_MCP_GATEWAY_HOST || DEFAULT_GATEWAY_HOST,
  port = Number(process.env.FLOW_MCP_GATEWAY_PORT || DEFAULT_GATEWAY_PORT),
  socketPath = process.env.FLOW_MCP_GATEWAY_SOCKET || "",
  secret = process.env.FLOW_MCP_GATEWAY_SECRET || "",
  flowOrchestrator,
  musicOrchestrator,
} = {}) {
  const normalizedSocket = String(socketPath || "").trim();
  if (normalizedSocket) {
    if (!path.isAbsolute(normalizedSocket)) {
      throw new Error(`Refusing to bind Flow MCP Gateway to non-absolute socket path "${normalizedSocket}".`);
    }
  } else if (!LOOPBACK_HOSTS.has(String(host))) {
    throw new Error(`Refusing to bind Flow MCP Gateway to non-loopback host "${host}". Use 127.0.0.1.`);
  }
  if (!secret || secret.length < 32) {
    throw new Error("FLOW_MCP_GATEWAY_SECRET must be set to at least 32 characters.");
  }
  const server = createGatewayServer({ secret, flowOrchestrator, musicOrchestrator });
  return new Promise((resolve, reject) => {
    server.on("error", reject);
    if (normalizedSocket) {
      fs.mkdirSync(path.dirname(normalizedSocket), { recursive: true });
      fs.rmSync(normalizedSocket, { force: true });
      server.listen(normalizedSocket, () => {
        try {
          fs.chmodSync(normalizedSocket, 0o660);
        } catch {
          // Best-effort on platforms where chmod on sockets is unsupported
        }
        resolve({ server, socketPath: normalizedSocket, host: null, port: null });
      });
      return;
    }
    server.listen(port, host, () => {
      const addr = server.address();
      resolve({ server, socketPath: null, host, port: typeof addr === "object" && addr ? addr.port : port });
    });
  });
}

if (process.argv[1] && fileURLToPath(import.meta.url) === path.resolve(process.argv[1])) {
  startGatewayServer()
    .then(({ socketPath, host, port }) => {
      const target = socketPath ? `unix://${socketPath}` : `http://${host}:${port}`;
      console.log(`[mokaair-flow-gateway] Listening on ${target} (services: flow, flow-music)`);
    })
    .catch((err) => {
      console.error(`[mokaair-flow-gateway] Failed to start: ${err?.message || err}`);
      process.exit(1);
    });
}
