import { describe, expect, it } from "vitest";
import { RequestBodyError, limitedRequestBody } from "./request-body";

function streamingRequest(chunks: string[]): Request {
  const stream = new ReadableStream<Uint8Array>({
    start(controller) {
      for (const chunk of chunks) controller.enqueue(new TextEncoder().encode(chunk));
      controller.close();
    },
  });
  return new Request("https://mokaair.com/api/travel/trips", {
    method: "POST",
    body: stream,
    duplex: "half",
  } as RequestInit & { duplex: "half" });
}

describe("limitedRequestBody", () => {
  it("returns the buffered body when it fits", async () => {
    const request = new Request("https://mokaair.com/x", { method: "POST", body: "hello" });
    expect(new TextDecoder().decode(await limitedRequestBody(request, 100))).toBe("hello");
  });

  it("returns undefined for a request without a body", async () => {
    expect(await limitedRequestBody(new Request("https://mokaair.com/x"), 100)).toBeUndefined();
  });

  it("rejects an oversized or malformed declared length before reading", async () => {
    const oversized = new Request("https://mokaair.com/x", {
      method: "POST",
      body: "x",
      headers: { "content-length": "999" },
    });
    await expect(limitedRequestBody(oversized, 100)).rejects.toMatchObject({ reason: "too_large" });
    for (const declared of ["-1", "abc"]) {
      const malformed = new Request("https://mokaair.com/x", {
        method: "POST",
        body: "x",
        headers: { "content-length": declared },
      });
      await expect(limitedRequestBody(malformed, 100)).rejects.toMatchObject({ reason: "invalid_length" });
    }
  });

  it("stops reading a chunked body once it exceeds the limit", async () => {
    const request = streamingRequest(["a".repeat(60), "b".repeat(60), "c".repeat(60)]);
    await expect(limitedRequestBody(request, 100)).rejects.toBeInstanceOf(RequestBodyError);
    const accepted = await limitedRequestBody(streamingRequest(["a".repeat(60), "b".repeat(40)]), 100);
    expect(accepted?.byteLength).toBe(100);
  });
});
