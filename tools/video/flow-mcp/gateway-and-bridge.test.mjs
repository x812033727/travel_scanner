import assert from "node:assert/strict";
import test from "node:test";
import { signGatewayRequest, startGatewayServer, verifyGatewaySignature } from "./gateway.mjs";
import { forwardRpcOverHttps } from "./remote-bridge.mjs";

const TEST_SECRET = "0123456789abcdef0123456789abcdef0123456789abcdef";

test("Flow MCP HTTP Gateway enforces loopback-only binding, HMAC signature, replay protection, and serves both flow (18 tools) & flow-music (17 tools)", async () => {
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

    // Signed POST /mcp/flow tools/list -> 18 tools
    const listBody = Buffer.from(JSON.stringify({ jsonrpc: "2.0", id: 2, method: "tools/list", params: {} }), "utf8");
    const flowHeaders = {
      "Content-Type": "application/json",
      ...signGatewayRequest({ secret: TEST_SECRET, method: "POST", reqPath: "/mcp/flow", bodyBuffer: listBody, nonce: "flow-list-nonce" }),
    };
    const flowRes = await fetch(`${baseUrl}/mcp/flow`, { method: "POST", headers: flowHeaders, body: listBody });
    assert.equal(flowRes.status, 200);
    const flowJson = await flowRes.json();
    assert.equal(flowJson.result.tools.length, 18);

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
