import { describe, expect, it } from "vitest";
import { preserveRequestId } from "./request-id";

describe("travel BFF request tracing", () => {
  it("preserves the API request ID on the browser response", () => {
    const upstream = new Response("{}", {
      headers: { "X-Request-ID": "route-preview-7f98" },
    });
    const response = preserveRequestId(new Response("{}"), upstream);

    expect(response.headers.get("x-request-id")).toBe("route-preview-7f98");
  });
});
