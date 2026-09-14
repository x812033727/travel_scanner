import test from "node:test";
import assert from "node:assert/strict";
import http from "node:http";
import { once } from "node:events";
import { GoogleGenAI } from "@google/genai";

test("pinned JavaScript SDK serializes Interactions and exposes output_text through local HTTP", async () => {
  const requests = [];
  const server = http.createServer(async (request, response) => {
    let body = "";
    for await (const chunk of request) body += chunk;
    requests.push({ path: request.url, body: JSON.parse(body) });
    response.writeHead(200, { "Content-Type": "application/json" });
    response.end(JSON.stringify({
      id: "fixture-js-interaction", status: "completed", object: "interaction",
      model: "gemini-3.8-flash", created: "2026-09-14T00:00:00Z",
      steps: [{ type: "model_output", content: [{ type: "text", text: "活動、日期、地點" }] }],
    }));
  });
  server.listen(0, "127.0.0.1");
  await once(server, "listening");
  try {
    const client = new GoogleGenAI({
      apiKey: "fixture-not-a-real-key",
      httpOptions: { baseUrl: `http://127.0.0.1:${server.address().port}` },
    });
    const reply = await client.interactions.create({
      model: "gemini-3.8-flash",
      input: "請用繁體中文列出整理活動公告時應核對的三個欄位。",
      store: false,
    });
    assert.equal(reply.status, "completed");
    assert.equal(reply.output_text, "活動、日期、地點");
    assert.equal(requests.length, 1);
    assert.match(requests[0].path, /interactions/);
    assert.deepEqual(requests[0].body, {
      model: "gemini-3.8-flash",
      input: "請用繁體中文列出整理活動公告時應核對的三個欄位。",
      store: false,
    });
  } finally {
    server.closeAllConnections();
    await new Promise((resolve, reject) => server.close((error) => error ? reject(error) : resolve()));
  }
});
