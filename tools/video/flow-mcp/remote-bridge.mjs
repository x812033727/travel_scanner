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

import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";
import { readCredentials } from "../tts/credentials.mjs";
import { EPISODE_TRANSFER_ALLOWED_EXTS, MAX_TRANSFER_CHUNK_BYTES } from "./guards/path-boundary.mjs";

const ALLOWED_SERVICES = new Set(["flow", "flow-music"]);

function sha256Buffer(buf) {
  return crypto.createHash("sha256").update(buf).digest("hex");
}

function sha256LocalFile(filePath) {
  return sha256Buffer(fs.readFileSync(filePath));
}

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

let rpcSeq = 1;

/**
 * Invokes a named tool on the remote Flow or Flow Music MCP gateway over HTTPS
 * and parses its JSON text payload.
 */
export async function callRemoteMcpTool({
  service = "flow",
  name,
  arguments: toolArgs = {},
  site = null,
  token = null,
  env = process.env,
  home = undefined,
  fetchImpl = globalThis.fetch,
}) {
  const creds = readCredentials({ env, home });
  const targetSite = (site || creds.site).replace(/\/+$/, "");
  const targetToken = token || creds.token;

  const response = await forwardRpcOverHttps({
    service,
    site: targetSite,
    token: targetToken,
    fetchImpl,
    message: {
      jsonrpc: "2.0",
      id: rpcSeq++,
      method: "tools/call",
      params: { name, arguments: toolArgs },
    },
  });

  if (!response) {
    throw new Error(`Remote MCP tool "${name}" returned empty response.`);
  }
  if (response.error) {
    throw new Error(response.error.message || `Remote MCP tool "${name}" failed.`);
  }
  const text = response.result?.content?.[0]?.text || "";
  let parsed = null;
  try {
    parsed = text ? JSON.parse(text) : null;
  } catch {
    parsed = { ok: !response.result?.isError, raw: text };
  }
  if (response.result?.isError || parsed?.ok === false) {
    const errMsg = parsed?.error?.message || parsed?.error || parsed?.message || `Tool "${name}" returned an error.`;
    throw new Error(String(errMsg));
  }
  return parsed;
}

/**
 * Uploads a single local file to the remote Flow gateway (`flow_write_file`)
 * with automatic chunking (<= 512 KiB) and end-to-end SHA-256 verification.
 */
export async function remotePushFile({
  slug,
  relPath,
  localFile,
  chunkBytes = MAX_TRANSFER_CHUNK_BYTES,
  site = null,
  token = null,
  env = process.env,
  home = undefined,
  fetchImpl = globalThis.fetch,
}) {
  const buf = fs.readFileSync(localFile);
  const sha = sha256Buffer(buf);
  const maxChunk = Math.max(1, Math.min(MAX_TRANSFER_CHUNK_BYTES, chunkBytes));
  const opts = { service: "flow", site, token, env, home, fetchImpl };

  if (buf.length <= maxChunk) {
    return callRemoteMcpTool({
      ...opts,
      name: "flow_write_file",
      arguments: {
        slug,
        relPath,
        mode: "replace",
        contentBase64: buf.toString("base64"),
        expectedSha256: sha,
      },
    });
  }

  let offset = 0;
  const firstSlice = buf.subarray(0, maxChunk);
  offset += firstSlice.length;
  const begun = await callRemoteMcpTool({
    ...opts,
    name: "flow_write_file",
    arguments: {
      slug,
      relPath,
      mode: "begin",
      contentBase64: firstSlice.toString("base64"),
    },
  });
  const uploadId = begun.uploadId;

  while (offset + maxChunk < buf.length) {
    const slice = buf.subarray(offset, offset + maxChunk);
    offset += slice.length;
    await callRemoteMcpTool({
      ...opts,
      name: "flow_write_file",
      arguments: {
        slug,
        relPath,
        mode: "append",
        uploadId,
        contentBase64: slice.toString("base64"),
      },
    });
  }

  const finalSlice = buf.subarray(offset);
  return callRemoteMcpTool({
    ...opts,
    name: "flow_write_file",
    arguments: {
      slug,
      relPath,
      mode: "commit",
      uploadId,
      contentBase64: finalSlice.toString("base64"),
      expectedSha256: sha,
    },
  });
}

/**
 * Downloads a single remote episode file (`flow_read_file`) in chunks, verifies
 * SHA-256, and writes atomically to `localFile`.
 */
export async function remotePullFile({
  slug,
  relPath,
  localFile,
  chunkBytes = MAX_TRANSFER_CHUNK_BYTES,
  site = null,
  token = null,
  env = process.env,
  home = undefined,
  fetchImpl = globalThis.fetch,
}) {
  const maxChunk = Math.max(1, Math.min(MAX_TRANSFER_CHUNK_BYTES, chunkBytes));
  const opts = { service: "flow", site, token, env, home, fetchImpl };
  const chunks = [];
  let offset = 0;
  let remoteSha = null;

  while (true) {
    const res = await callRemoteMcpTool({
      ...opts,
      name: "flow_read_file",
      arguments: { slug, relPath, offset, maxBytes: maxChunk },
    });
    if (res.sha256) remoteSha = res.sha256;
    if (res.contentBase64) {
      chunks.push(Buffer.from(res.contentBase64, "base64"));
    }
    if (res.eof) break;
    if (res.nextOffset <= offset) {
      throw new Error(`Remote read stalled at offset ${offset} for "${relPath}".`);
    }
    offset = res.nextOffset;
  }

  const full = Buffer.concat(chunks);
  const actualSha = sha256Buffer(full);
  if (remoteSha && actualSha !== remoteSha) {
    throw new Error(`SHA-256 mismatch downloading "${relPath}": remote=${remoteSha}, local=${actualSha}.`);
  }

  fs.mkdirSync(path.dirname(localFile), { recursive: true });
  const tmp = `${localFile}.tmp-${process.pid}-${Date.now()}`;
  fs.writeFileSync(tmp, full);
  fs.renameSync(tmp, localFile);

  return { ok: true, slug, relPath, localFile, bytes: full.length, sha256: actualSha };
}

/**
 * Incrementally pushes all allowlisted files from a local episode directory
 * to the remote Flow gateway, skipping files whose SHA-256 already matches.
 */
export async function remotePushDir({
  slug,
  fromDir,
  subdir = "",
  chunkBytes = MAX_TRANSFER_CHUNK_BYTES,
  site = null,
  token = null,
  env = process.env,
  home = undefined,
  fetchImpl = globalThis.fetch,
}) {
  const cleanSubdir = String(subdir || "").replace(/\\/g, "/").replace(/^\/+|\/+$/g, "");
  const rootDir = path.resolve(fromDir);
  const scanDir = cleanSubdir ? path.join(rootDir, cleanSubdir) : rootDir;
  if (!fs.existsSync(scanDir)) {
    throw new Error(`Local directory not found: "${scanDir}".`);
  }

  const remoteListing = await callRemoteMcpTool({
    service: "flow",
    name: "flow_list_files",
    arguments: { slug, subdir: cleanSubdir, includeSha256: true },
    site,
    token,
    env,
    home,
    fetchImpl,
  });
  const remoteShaMap = new Map((remoteListing.files || []).map((f) => [f.relPath, f.sha256]));

  const localFiles = [];
  const walk = (dir, prefix) => {
    for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
      if (entry.name.startsWith(".")) continue;
      const full = path.join(dir, entry.name);
      const lstat = fs.lstatSync(full);
      if (lstat.isSymbolicLink()) continue;
      const rel = prefix ? `${prefix}/${entry.name}` : entry.name;
      if (lstat.isDirectory()) {
        walk(full, rel);
      } else if (lstat.isFile()) {
        const ext = path.posix.extname(rel).toLowerCase();
        if (EPISODE_TRANSFER_ALLOWED_EXTS.has(ext)) {
          localFiles.push({ relPath: rel, fullPath: full });
        }
      }
    }
  };
  walk(scanDir, cleanSubdir);
  localFiles.sort((a, b) => a.relPath.localeCompare(b.relPath));

  const uploaded = [];
  const skipped = [];

  for (const item of localFiles) {
    const localSha = sha256LocalFile(item.fullPath);
    if (remoteShaMap.get(item.relPath) === localSha) {
      skipped.push(item.relPath);
      continue;
    }
    const res = await remotePushFile({
      slug,
      relPath: item.relPath,
      localFile: item.fullPath,
      chunkBytes,
      site,
      token,
      env,
      home,
      fetchImpl,
    });
    uploaded.push({ relPath: item.relPath, bytes: res.bytes, sha256: res.sha256 });
  }

  return {
    ok: true,
    slug,
    subdir: cleanSubdir,
    uploadedCount: uploaded.length,
    skippedCount: skipped.length,
    uploaded,
    skipped,
  };
}

/**
 * Incrementally pulls files from the remote Flow gateway into a local directory,
 * skipping files whose local SHA-256 already matches.
 */
export async function remotePullDir({
  slug,
  toDir,
  subdir = "",
  chunkBytes = MAX_TRANSFER_CHUNK_BYTES,
  site = null,
  token = null,
  env = process.env,
  home = undefined,
  fetchImpl = globalThis.fetch,
}) {
  const cleanSubdir = String(subdir || "").replace(/\\/g, "/").replace(/^\/+|\/+$/g, "");
  const destRoot = path.resolve(toDir);
  const remoteListing = await callRemoteMcpTool({
    service: "flow",
    name: "flow_list_files",
    arguments: { slug, subdir: cleanSubdir, includeSha256: true },
    site,
    token,
    env,
    home,
    fetchImpl,
  });

  const downloaded = [];
  const skipped = [];

  for (const item of remoteListing.files || []) {
    const ext = path.posix.extname(item.relPath).toLowerCase();
    if (!EPISODE_TRANSFER_ALLOWED_EXTS.has(ext)) continue;
    const localFile = path.resolve(destRoot, ...item.relPath.split("/"));
    if (fs.existsSync(localFile) && item.sha256 && sha256LocalFile(localFile) === item.sha256) {
      skipped.push(item.relPath);
      continue;
    }
    const res = await remotePullFile({
      slug,
      relPath: item.relPath,
      localFile,
      chunkBytes,
      site,
      token,
      env,
      home,
      fetchImpl,
    });
    downloaded.push({ relPath: item.relPath, bytes: res.bytes, sha256: res.sha256 });
  }

  return {
    ok: true,
    slug,
    subdir: cleanSubdir,
    downloadedCount: downloaded.length,
    skippedCount: skipped.length,
    downloaded,
    skipped,
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
