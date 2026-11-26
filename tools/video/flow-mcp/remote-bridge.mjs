#!/usr/bin/env node
/**
 * Thin stdio-to-HTTPS MCP bridge for paired cloud environments (`remote-mcp`).
 *
 * Reads the paired video tool token (`mkv_...`) from `~/.mokaair/video-tool.json`
 * (or `MOKAAIR_VIDEO_TOKEN` / `MOKAAIR_SITE`) via Mokaair's shared
 * `tools/video/tts/credentials.mjs`, and forwards JSON-RPC 2.0 messages over
 * HTTPS to `https://mokaair.com/api/video/mcp/<flow|flow-music>`.
 *
 * Supports both newline-delimited JSON-RPC and `Content-Length` framing.
 */

import { readCredentials } from "../tts/credentials.mjs";

const ALLOWED_SERVICES = new Set(["flow", "flow-music"]);

export async function forwardRpcOverHttps({
  service,
  message,
  site,
  token,
  fetchImpl = globalThis.fetch,
}) {
  if (!ALLOWED_SERVICES.has(service)) {
    throw new Error(`Unsupported MCP service "${service}". Expected "flow" or "flow-music".`);
  }
  if (!token) {
    return {
      jsonrpc: "2.0",
      id: message?.id ?? null,
      error: {
        code: -32001,
        message: "Missing video tool token (mkv_...). Run `node tools/video/cli.mjs login --flow` to pair first.",
      },
    };
  }

  const endpoint = `${site.replace(/\/+$/, "")}/api/video/mcp/${service}`;
  const res = await fetchImpl(endpoint, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${token}`,
      "Content-Type": "application/json",
      Accept: "application/json",
    },
    body: JSON.stringify(message),
  });

  if (res.status === 202 || res.status === 204) {
    return null;
  }

  const text = await res.text();
  let parsed = null;
  try {
    parsed = text ? JSON.parse(text) : null;
  } catch {
    parsed = null;
  }

  if (parsed && parsed.jsonrpc === "2.0") {
    return parsed;
  }

  const detail = parsed?.detail || parsed?.title || parsed?.message || text.slice(0, 200) || `HTTP ${res.status}`;
  return {
    jsonrpc: "2.0",
    id: message?.id ?? null,
    error: {
      code: res.status === 401 || res.status === 403 ? -32001 : -32000,
      message: `Remote MCP (${endpoint}) failed (${res.status}): ${detail}`,
      data: { status: res.status, code: parsed?.code || null },
    },
  };
}

export function startRemoteStdioBridge({
  service = "flow",
  site = null,
  token = null,
  env = process.env,
  home = undefined,
  stdin = process.stdin,
  stdout = process.stdout,
  stderr = process.stderr,
  fetchImpl = globalThis.fetch,
} = {}) {
  const creds = readCredentials({ env, home });
  const targetSite = (site || creds.site).replace(/\/+$/, "");
  const targetToken = token || creds.token;

  let buffer = Buffer.alloc(0);
  let useContentLength = false;

  const send = (obj) => {
    const json = JSON.stringify(obj);
    if (useContentLength) {
      stdout.write(`Content-Length: ${Buffer.byteLength(json, "utf8")}\r\n\r\n${json}`);
    } else {
      stdout.write(`${json}\n`);
    }
  };

  const processMessage = async (rawText) => {
    let msg;
    try {
      msg = JSON.parse(rawText);
    } catch {
      send({ jsonrpc: "2.0", id: null, error: { code: -32700, message: "Parse error" } });
      return;
    }

    try {
      const response = await forwardRpcOverHttps({
        service,
        message: msg,
        site: targetSite,
        token: targetToken,
        fetchImpl,
      });
      if (response && msg?.id !== undefined && msg?.id !== null) {
        send(response);
      }
    } catch (err) {
      stderr.write(`[remote-mcp:${service}] ${err?.message || err}\n`);
      if (msg?.id !== undefined && msg?.id !== null) {
        send({
          jsonrpc: "2.0",
          id: msg.id,
          error: { code: -32000, message: err?.message || "Remote MCP network error" },
        });
      }
    }
  };

  const drainBuffer = () => {
    while (buffer.length > 0) {
      const head = buffer.subarray(0, Math.min(32, buffer.length)).toString("utf8");
      if (/^Content-Length:/i.test(head)) {
        useContentLength = true;
        const headerEnd = buffer.indexOf("\r\n\r\n");
        if (headerEnd === -1) return;
        const lenMatch = buffer.subarray(0, headerEnd).toString("utf8").match(/Content-Length:\s*(\d+)/i);
        if (!lenMatch) {
          buffer = buffer.subarray(headerEnd + 4);
          continue;
        }
        const contentLength = Number(lenMatch[1]);
        const bodyStart = headerEnd + 4;
        if (buffer.length < bodyStart + contentLength) return;
        const body = buffer.subarray(bodyStart, bodyStart + contentLength).toString("utf8");
        buffer = buffer.subarray(bodyStart + contentLength);
        void processMessage(body);
        continue;
      }

      const newlineIdx = buffer.indexOf("\n");
      if (newlineIdx === -1) return;
      const line = buffer.subarray(0, newlineIdx).toString("utf8").trim();
      buffer = buffer.subarray(newlineIdx + 1);
      if (line) void processMessage(line);
    }
  };

  stdin.on("data", (chunk) => {
    buffer = Buffer.concat([buffer, Buffer.isBuffer(chunk) ? chunk : Buffer.from(chunk, "utf8")]);
    drainBuffer();
  });
}
