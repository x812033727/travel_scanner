import assert from "node:assert/strict";
import crypto from "node:crypto";
import fs from "node:fs";
import http from "node:http";
import os from "node:os";
import path from "node:path";
import test from "node:test";
import { signGatewayRequest, startGatewayServer, verifyGatewaySignature } from "./gateway.mjs";
import { FlowOrchestrator } from "./orchestrator.mjs";
import { callRemoteMcpTool, forwardRpcOverHttps, remotePullDir, remotePushDir } from "./remote-bridge.mjs";

const TEST_SECRET = "0123456789abcdef0123456789abcdef0123456789abcdef";

function makePngBuffer(width, height) {
  const buf = Buffer.alloc(33);
  Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]).copy(buf, 0);
  buf.writeUInt32BE(13, 8);
  buf.write("IHDR", 12, "ascii");
  buf.writeUInt32BE(width, 16);
  buf.writeUInt32BE(height, 20);
  return buf;
}

test("Flow MCP HTTP Gateway enforces loopback-only binding, HMAC signature, replay protection, and serves both flow (22 tools) & flow-music (17 tools)", async () => {
  assert.throws(
    () => startGatewayServer({ host: "0.0.0.0", port: 0, secret: TEST_SECRET }),
    /non-loopback/,
  );
  assert.throws(
    () => startGatewayServer({ host: "127.0.0.1", port: 0, secret: "too-short" }),
    /at least 32/,
  );

  // Unit check replay protection
  const seen = new Map();
  const body = Buffer.from('{"jsonrpc":"2.0","id":1,"method":"ping"}', "utf8");
  const hdrs = signGatewayRequest({ secret: TEST_SECRET, method: "POST", reqPath: "/mcp/flow", bodyBuffer: body, nonce: "nonce-12345678" });
  assert.equal(verifyGatewaySignature({ secret: TEST_SECRET, method: "POST", reqPath: "/mcp/flow", bodyBuffer: body, headers: hdrs, seenNonces: seen }).ok, true);
  assert.equal(verifyGatewaySignature({ secret: TEST_SECRET, method: "POST", reqPath: "/mcp/flow", bodyBuffer: body, headers: hdrs, seenNonces: seen }).code, "gateway_nonce_replayed");

  const { server, host, port } = await startGatewayServer({ host: "127.0.0.1", port: 0, secret: TEST_SECRET });
  const baseUrl = `http://${host}:${port}`;
  try {
    // Unsigned request rejected with 401
    const unauth = await fetch(`${baseUrl}/health`);
    assert.equal(unauth.status, 401);

    // Signed /health
    const healthHeaders = signGatewayRequest({ secret: TEST_SECRET, method: "GET", reqPath: "/health", bodyBuffer: Buffer.alloc(0), nonce: "health-nonce-1" });
    const healthRes = await fetch(`${baseUrl}/health`, { headers: healthHeaders });
    assert.equal(healthRes.status, 200);
    const healthJson = await healthRes.json();
    assert.equal(healthJson.ok, true);
    assert.deepEqual(healthJson.services, ["flow", "flow-music"]);

    // Signed POST /mcp/flow tools/list -> 22 tools
    const listBody = Buffer.from(JSON.stringify({ jsonrpc: "2.0", id: 2, method: "tools/list", params: {} }), "utf8");
    const flowHeaders = {
      "Content-Type": "application/json",
      ...signGatewayRequest({ secret: TEST_SECRET, method: "POST", reqPath: "/mcp/flow", bodyBuffer: listBody, nonce: "flow-list-nonce" }),
    };
    const flowRes = await fetch(`${baseUrl}/mcp/flow`, { method: "POST", headers: flowHeaders, body: listBody });
    assert.equal(flowRes.status, 200);
    const flowJson = await flowRes.json();
    assert.equal(flowJson.result.tools.length, 22);

    // Signed POST /mcp/flow-music tools/list -> 17 tools
    const musicHeaders = {
      "Content-Type": "application/json",
      ...signGatewayRequest({ secret: TEST_SECRET, method: "POST", reqPath: "/mcp/flow-music", bodyBuffer: listBody, nonce: "music-list-nonce" }),
    };
    const musicRes = await fetch(`${baseUrl}/mcp/flow-music`, { method: "POST", headers: musicHeaders, body: listBody });
    assert.equal(musicRes.status, 200);
    const musicJson = await musicRes.json();
    assert.equal(musicJson.result.tools.length, 17);
  } finally {
    await new Promise((resolve) => server.close(resolve));
  }
});

test("remote-bridge forwards JSON-RPC over HTTPS with Bearer mkv_ token and reports missing token cleanly", async () => {
  const noTok = await forwardRpcOverHttps({
    service: "flow",
    message: { jsonrpc: "2.0", id: 1, method: "ping" },
    site: "https://mokaair.com",
    token: null,
  });
  assert.equal(noTok.error.code, -32001);
  assert.match(noTok.error.message, /login --flow/);

  const seen = [];
  const ok = await forwardRpcOverHttps({
    service: "flow-music",
    message: { jsonrpc: "2.0", id: 7, method: "ping" },
    site: "https://mokaair.com",
    token: `mkv_${"a".repeat(44)}`,
    fetchImpl: async (url, init) => {
      seen.push({ url, headers: init.headers, body: JSON.parse(init.body) });
      return new Response(JSON.stringify({ jsonrpc: "2.0", id: 7, result: {} }), {
        status: 200,
        headers: { "Content-Type": "application/json" },
      });
    },
  });
  assert.equal(seen[0].url, "https://mokaair.com/api/video/mcp/flow-music");
  assert.match(seen[0].headers.Authorization, /^Bearer mkv_/);
  assert.deepEqual(ok, { jsonrpc: "2.0", id: 7, result: {} });
});

test("remotePushDir & remotePullDir sync chunked episode assets with SHA-256 0-diff, auto-approve uploaded stills, and enforce path jail", async () => {
  const hostRepo = fs.mkdtempSync(path.join(os.tmpdir(), "flow-remote-host-"));
  const hostHome = fs.mkdtempSync(path.join(os.tmpdir(), "flow-remote-home-"));
  const clientSrc = fs.mkdtempSync(path.join(os.tmpdir(), "flow-remote-src-"));
  const clientDst = fs.mkdtempSync(path.join(os.tmpdir(), "flow-remote-dst-"));

  // Fake vdrive.mjs inside hostRepo to test flow_push_drive
  fs.mkdirSync(path.join(hostRepo, "tools", "video"), { recursive: true });
  fs.writeFileSync(path.join(hostRepo, "tools", "video", "vdrive.mjs"), "// fake vdrive\n");

  const vdriveCalls = [];
  const flowOrchestrator = new FlowOrchestrator({
    repoRoot: hostRepo,
    runtimeHome: hostHome,
    spawnSyncImpl: (cmd, args) => {
      vdriveCalls.push({ cmd, args });
      return { status: 0, stdout: "vdrive: pushed 3 file(s) (0 differences)", stderr: "" };
    },
  });

  const { server, host, port } = await startGatewayServer({
    host: "127.0.0.1",
    port: 0,
    secret: TEST_SECRET,
    flowOrchestrator,
  });

  // Adapter that simulates mokaair.com signing and forwarding to the local gateway
  let nonceSeq = 1;
  const proxyFetch = async (_url, init) => {
    const bodyBuf = Buffer.from(init.body, "utf8");
    const sigHeaders = signGatewayRequest({
      secret: TEST_SECRET,
      method: "POST",
      reqPath: "/mcp/flow",
      bodyBuffer: bodyBuf,
      nonce: `bridge-test-${nonceSeq++}-${crypto.randomBytes(4).toString("hex")}`,
    });
    return fetch(`http://${host}:${port}/mcp/flow`, {
      method: "POST",
      headers: { "Content-Type": "application/json", ...sigHeaders },
      body: bodyBuf,
    });
  };

  const token = `mkv_${"z".repeat(44)}`;
  const slug = "sothatswhy-g790-dehumidifier-winter";

  try {
    // Prepare local episode files: shot list, 16:9 PNG still, and a multi-chunk MP4
    fs.mkdirSync(path.join(clientSrc, "stills"), { recursive: true });
    fs.mkdirSync(path.join(clientSrc, "flow-clips"), { recursive: true });
    fs.writeFileSync(
      path.join(clientSrc, "flow-shot-list.json"),
      JSON.stringify({ series: "sothatswhy", shots: [{ id: "B38", track: "scenery", mode: "clip", video_prompt: "Slow push in" }] }),
    );
    fs.writeFileSync(path.join(clientSrc, "stills", "B38.png"), makePngBuffer(1376, 768));
    const bigMp4 = crypto.randomBytes(150 * 1024); // > 64 KiB chunk test
    fs.writeFileSync(path.join(clientSrc, "flow-clips", "B01.mp4"), bigMp4);
    // Disallowed file should be ignored by remotePushDir
    fs.writeFileSync(path.join(clientSrc, "ignore.sh"), "#!/bin/sh\necho hi\n");

    const pushed1 = await remotePushDir({
      slug,
      fromDir: clientSrc,
      chunkBytes: 64 * 1024,
      site: "https://mokaair.com",
      token,
      fetchImpl: proxyFetch,
    });
    assert.equal(pushed1.uploadedCount, 3);
    assert.equal(pushed1.skippedCount, 0);

    // Second push skips all 3 identical files (0-diff)
    const pushed2 = await remotePushDir({
      slug,
      fromDir: clientSrc,
      chunkBytes: 64 * 1024,
      site: "https://mokaair.com",
      token,
      fetchImpl: proxyFetch,
    });
    assert.equal(pushed2.uploadedCount, 0);
    assert.equal(pushed2.skippedCount, 3);

    // Approve uploaded still without prior qa-manifest.json
    const approved = await callRemoteMcpTool({
      name: "flow_approve_stills",
      arguments: { slug, series: "sothatswhy", approved: ["B38"], reviewer: "antigravity" },
      site: "https://mokaair.com",
      token,
      fetchImpl: proxyFetch,
    });
    assert.equal(approved.ok, true);
    assert.deepEqual(approved.updatedApproved, ["B38"]);

    // Pull everything back into clean directory with chunked download + SHA-256 verification
    const pulled1 = await remotePullDir({
      slug,
      toDir: clientDst,
      chunkBytes: 48 * 1024,
      site: "https://mokaair.com",
      token,
      fetchImpl: proxyFetch,
    });
    assert.ok(pulled1.downloadedCount >= 3);
    assert.deepEqual(fs.readFileSync(path.join(clientDst, "flow-clips", "B01.mp4")), bigMp4);

    // Second pull skips unchanged files
    const pulled2 = await remotePullDir({
      slug,
      toDir: clientDst,
      chunkBytes: 48 * 1024,
      site: "https://mokaair.com",
      token,
      fetchImpl: proxyFetch,
    });
    assert.equal(pulled2.downloadedCount, 0);
    assert.equal(pulled2.skippedCount, pulled1.downloadedCount);

    // Host-side Drive push fast-path
    const driveRes = await callRemoteMcpTool({
      name: "flow_push_drive",
      arguments: {
        slug,
        series: "sothatswhy",
        drivePath: "物理化學與日常材料/G790/製作檔/sothatswhy-g790-dehumidifier-winter",
        dryRun: true,
      },
      site: "https://mokaair.com",
      token,
      fetchImpl: proxyFetch,
    });
    assert.equal(driveRes.ok, true);
    assert.equal(vdriveCalls.length, 1);
    assert.ok(vdriveCalls[0].args.includes("--dry-run"));

    // Security rejections: traversal, dotfile, forbidden extension, SHA-256 mismatch
    await assert.rejects(
      () =>
        callRemoteMcpTool({
          name: "flow_write_file",
          arguments: { slug, relPath: "../escape.json", contentBase64: Buffer.from("{}").toString("base64") },
          site: "https://mokaair.com",
          token,
          fetchImpl: proxyFetch,
        }),
      /Forbidden path segment/,
    );
    await assert.rejects(
      () =>
        callRemoteMcpTool({
          name: "flow_write_file",
          arguments: { slug, relPath: ".env", contentBase64: Buffer.from("X=1").toString("base64") },
          site: "https://mokaair.com",
          token,
          fetchImpl: proxyFetch,
        }),
      /Forbidden path segment/,
    );
    await assert.rejects(
      () =>
        callRemoteMcpTool({
          name: "flow_write_file",
          arguments: { slug, relPath: "exploit.mjs", contentBase64: Buffer.from("1").toString("base64") },
          site: "https://mokaair.com",
          token,
          fetchImpl: proxyFetch,
        }),
      /Unsupported episode file extension/,
    );
    await assert.rejects(
      () =>
        callRemoteMcpTool({
          name: "flow_write_file",
          arguments: {
            slug,
            relPath: "bad.json",
            contentBase64: Buffer.from("{}").toString("base64"),
            expectedSha256: "0".repeat(64),
          },
          site: "https://mokaair.com",
          token,
          fetchImpl: proxyFetch,
        }),
      /SHA-256 mismatch/,
    );

    if (process.platform !== "win32") {
      const outside = path.join(hostHome, "outside.json");
      fs.writeFileSync(outside, '{"secret":true}');
      fs.symlinkSync(outside, path.join(hostRepo, "work", "video-episodes", slug, "link.json"));
      await assert.rejects(
        () =>
          callRemoteMcpTool({
            name: "flow_read_file",
            arguments: { slug, relPath: "link.json" },
            site: "https://mokaair.com",
            token,
            fetchImpl: proxyFetch,
          }),
        /Refusing symlink/,
      );
    }
  } finally {
    await new Promise((resolve) => server.close(resolve));
    fs.rmSync(hostRepo, { recursive: true, force: true });
    fs.rmSync(hostHome, { recursive: true, force: true });
    fs.rmSync(clientSrc, { recursive: true, force: true });
    fs.rmSync(clientDst, { recursive: true, force: true });
  }
});

test("Flow MCP Gateway supports Unix domain socket binding and rejects relative socket paths", async () => {
  assert.throws(
    () => startGatewayServer({ socketPath: "relative/gateway.sock", secret: TEST_SECRET }),
    /non-absolute socket path/,
  );

  if (process.platform === "win32") return;

  const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), "mokaair-flow-gw-"));
  const socketPath = path.join(tmpDir, "gateway.sock");
  const { server } = await startGatewayServer({ socketPath, secret: TEST_SECRET });
  try {
    const headers = signGatewayRequest({
      secret: TEST_SECRET,
      method: "GET",
      reqPath: "/health",
      bodyBuffer: Buffer.alloc(0),
      nonce: "unix-health-nonce-1",
    });
    const res = await new Promise((resolve, reject) => {
      const req = http.request({ socketPath, path: "/health", method: "GET", headers }, (response) => {
        const chunks = [];
        response.on("data", (c) => chunks.push(c));
        response.on("end", () =>
          resolve({ status: response.statusCode, json: JSON.parse(Buffer.concat(chunks).toString("utf8")) }),
        );
      });
      req.on("error", reject);
      req.end();
    });
    assert.equal(res.status, 200);
    assert.equal(res.json.ok, true);
    assert.deepEqual(res.json.services, ["flow", "flow-music"]);
  } finally {
    await new Promise((resolve) => server.close(resolve));
    fs.rmSync(tmpDir, { recursive: true, force: true });
  }
});
