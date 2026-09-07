import { afterEach, describe, expect, it, vi } from "vitest";
import { ANALYTICS_SESSION_KEY } from "./analytics";
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

  it.each([
    ["zh-TW", "目前沒有足夠且符合寵物條件的已查核場所"],
    ["zh-CN", "目前没有足够且符合宠物条件的已查核场所"],
    ["en", "Not enough verified places match your pet's needs"],
    ["ja", "条件に合う確認済み施設が不足しています"],
    ["ko", "반려동물 조건에 맞는 검증된 장소가 부족합니다"],
  ])("explains conservative pet planning failures in %s", (locale, expected) => {
    document.documentElement.lang = locale;
    expect(apiProblemMessage({ code: "pet_candidates_insufficient", detail: "pet_candidates_insufficient" }, 422)).toContain(expected);
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

describe("the analytics session on API calls", () => {
  afterEach(() => {
    sessionStorage.clear();
    vi.unstubAllGlobals();
  });

  function stubOk() {
    const fetchMock = vi.fn().mockResolvedValue(new Response("{}", { status: 200 }));
    vi.stubGlobal("fetch", fetchMock);
    return fetchMock;
  }

  it("carries the browser's analytics session so a server event joins it", async () => {
    sessionStorage.setItem(ANALYTICS_SESSION_KEY, "3f2504e0-4f89-41d3-9a0c-0305e82c3301");
    const fetchMock = stubOk();

    await api("/trips", { method: "POST" });

    const headers = fetchMock.mock.calls[0][1].headers as Record<string, string>;
    expect(headers["X-Travel-Analytics-Session"]).toBe("3f2504e0-4f89-41d3-9a0c-0305e82c3301");
  });

  it("sends nothing when there is no session, rather than starting one", async () => {
    // Only the analytics provider creates the id, and only once it knows the visitor
    // has not opted out. An API call must never be what begins tracking someone.
    const fetchMock = stubOk();

    await api("/trips");

    const headers = fetchMock.mock.calls[0][1].headers as Record<string, string>;
    expect("X-Travel-Analytics-Session" in headers).toBe(false);
    expect(sessionStorage.getItem(ANALYTICS_SESSION_KEY)).toBeNull();
  });
});
