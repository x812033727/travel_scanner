import { afterEach, describe, expect, it, vi } from "vitest";
import { api, apiProblemMessage } from "./api";

afterEach(() => vi.unstubAllGlobals());

describe("API error messages", () => {
  it("turns FastAPI validation issues into readable field messages", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(new Response(JSON.stringify({
      detail: [
        { type: "date_from_datetime_parsing", loc: ["body", "start_date"], msg: "Input should be a valid date or datetime" },
        { type: "missing", loc: ["body", "end_date"], msg: "Field required" },
      ],
    }), { status: 422, headers: { "Content-Type": "application/json" } })));

    await expect(api("/trips", { method: "POST" })).rejects.toMatchObject({
      message: "開始日期：請選擇有效日期；結束日期：必填",
      status: 422,
    });
  });

  it("never stringifies a structured error as object Object", () => {
    const message = apiProblemMessage({ detail: { unexpected: true } }, 500);
    expect(message).toBe("請求失敗（HTTP 500）");
    expect(message).not.toContain("[object Object]");
  });
});

describe("API error messages in other locales", () => {
  afterEach(() => {
    document.documentElement.lang = "";
  });

  it("keeps the server's localized detail instead of the Chinese catalog", () => {
    document.documentElement.lang = "en";
    expect(apiProblemMessage({ code: "trip_not_found", detail: "Trip not found" }, 404)).toBe("Trip not found");
  });

  it("falls back to a localized generic failure", () => {
    document.documentElement.lang = "en";
    expect(apiProblemMessage({ detail: { unexpected: true } }, 500)).toBe("Something went wrong. Please try again. (HTTP 500)");
  });

  it("still prefers the Chinese catalog for zh-TW", () => {
    document.documentElement.lang = "zh-TW";
    expect(apiProblemMessage({ code: "trip_not_found", detail: "Trip not found" }, 404)).toBe("找不到這個旅程");
  });
});
