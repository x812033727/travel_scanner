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
