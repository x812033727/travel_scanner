import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { SearchExperience } from "./search-experience";

const { location, router } = vi.hoisted(() => ({
  location: { search: "" },
  router: { push: vi.fn(), replace: vi.fn(), refresh: vi.fn() },
}));

vi.mock("next/navigation", () => ({
  useSearchParams: () => new URLSearchParams(location.search),
}));
vi.mock("@/i18n/navigation", () => ({
  Link: ({ href, children, ...props }: React.AnchorHTMLAttributes<HTMLAnchorElement> & { href: string }) => <a href={href} {...props}>{children}</a>,
  usePathname: () => "/search",
  useRouter: () => router,
}));

type Listener = (message: MessageEvent) => void;

class FakeEventSource {
  static instances: FakeEventSource[] = [];
  listeners = new Map<string, Listener[]>();
  onerror: (() => void) | null = null;
  constructor(readonly url: string) {
    FakeEventSource.instances.push(this);
  }
  addEventListener(name: string, listener: Listener) {
    this.listeners.set(name, [...(this.listeners.get(name) || []), listener]);
  }
  emit(name: string, data: unknown) {
    for (const listener of this.listeners.get(name) || []) listener({ data: JSON.stringify(data) } as MessageEvent);
  }
  close() {}
}

const providerStatus = { provider: "mock", mode: "mock", status: "ready", modules: ["flight", "hotel"], message: "模擬資料已啟用" };
const plan = {
  id: "plan-1",
  mode: "balanced",
  title: "均衡",
  duplicate: false,
  total_cost: { confirmed_cost: 30000, estimated_cost: 5000, total_cost: 35000, components: [] },
  pros: [],
  cons: [],
  compared_with_cheapest: { price_difference: 0, flight_minutes_saved: 0 },
};
const criteria = "origin=TPE&destination=NRT&departure_date=2026-11-10&return_date=2026-11-15&adults=2";

function json(body: unknown, status = 200) {
  return new Response(JSON.stringify(body), { status, headers: { "Content-Type": "application/json" } });
}

function stubApi(options: {
  signedIn: boolean;
  tripResponses?: Array<() => Response>;
  providers?: unknown;
}) {
  const tripResponses = [...(options.tripResponses || [])];
  return vi.fn(async (input: RequestInfo | URL, init?: RequestInit) => {
    const url = String(input);
    if (url.endsWith("/auth/me")) return options.signedIn ? json({ id: "u1" }) : json({ detail: "未登入" }, 401);
    if (url.endsWith("/providers/status")) return json(options.providers ?? providerStatus);
    if (url.endsWith("/searches") && init?.method === "POST") return json({ search_id: "search-1", usage: { status: "reserved", uses: 1, reference: "u-1" } }, 202);
    if (url.endsWith("/searches/search-1")) return json({ status: "completed", result: { modules: {}, plans: [plan] }, warnings: [] });
    if (url.endsWith("/trips") && init?.method === "POST") return (tripResponses.shift() || (() => json({ id: "trip-1" })))();
    return json({ items: [] });
  });
}

function postCalls(path: string) {
  return vi.mocked(fetch).mock.calls.filter(([input, init]) => String(input).endsWith(path) && init?.method === "POST");
}

const tripCriteria = {
  trip: { id: "trip-1", name: "京都五天", version: 4, destination_name: "日本京都", start_date: "2026-11-10", end_date: "2026-11-14" },
  criteria: {
    origin: "TPE", destination: "KIX", departure_date: "2026-11-10", return_date: "2026-11-14",
    travelers: { adults: 2, children: 0, children_ages: [], rooms: 1 },
    preferences: { pace: "relaxed", interests: ["food"], budget_twd: 60000 },
    modules: ["flight"], trip_id: "trip-1",
  },
  issues: [],
  origin_options: ["TPE", "TSA", "KHH"],
};
const flightOffer = {
  id: "offer-1", provider: "mock", source_mode: "mock", airline: "長榮航空", origin: "TPE", destination: "KIX",
  departure_time: "2026-11-10T08:00:00+08:00", arrival_time: "2026-11-10T11:30:00+09:00",
  return_departure_time: "2026-11-14T13:00:00+09:00", return_arrival_time: "2026-11-14T15:00:00+08:00",
  total_price: 12000, currency: "TWD",
};

// Trip mode: criteria answers are consumed in order (the last one sticks), as are
// from-offer answers, so a test can script a refetch or a version conflict.
function stubTripApi(options: { criteria?: unknown[]; attachResponses?: Array<() => Response> } = {}) {
  const criteria = [...(options.criteria || [tripCriteria])];
  const attachResponses = [...(options.attachResponses || [])];
  return vi.fn(async (input: RequestInfo | URL, init?: RequestInit) => {
    const url = String(input);
    if (url.endsWith("/auth/me")) return json({ id: "u1" });
    if (url.endsWith("/providers/status")) return json(providerStatus);
    if (url.includes("/trips/trip-1/search-criteria")) return json(criteria.length > 1 ? criteria.shift() : criteria[0]);
    if (url.endsWith("/trips/trip-1") && init?.method === "PATCH") return json({ id: "trip-1", version: 5 });
    if (url.endsWith("/trips/trip-1")) return json({ id: "trip-1", version: 7 });
    if (url.endsWith("/from-offer")) return (attachResponses.shift() || (() => json({ id: "trip-1", version: 5 })))();
    if (url.endsWith("/searches") && init?.method === "POST") return json({ search_id: "search-1", usage: { status: "reserved", uses: 1, reference: "u-1" } }, 202);
    if (url.endsWith("/searches/search-1")) return json({ status: "completed", result: { modules: { flight: [flightOffer] }, plans: [] }, warnings: [] });
    return json({ items: [] });
  });
}

function requestBody(call: [RequestInfo | URL, RequestInit?] | undefined) {
  return JSON.parse(String(call?.[1]?.body || "{}")) as Record<string, unknown>;
}

beforeEach(() => {
  FakeEventSource.instances = [];
  vi.stubGlobal("EventSource", FakeEventSource);
});

afterEach(() => {
  vi.unstubAllGlobals();
  router.replace.mockReset();
  router.push.mockReset();
  location.search = "";
});

describe("SearchExperience from a saved trip", () => {
  it("searches what the trip says and writes each chosen leg back into its anchors", async () => {
    location.search = "trip_id=trip-1";
    vi.stubGlobal("fetch", stubTripApi());
    render(<SearchExperience />);

    expect(await screen.findByRole("heading", { name: "為〈京都五天〉找機票" })).toBeTruthy();
    expect(screen.getByText("日本京都 · 2026-11-10 → 2026-11-14")).toBeTruthy();
    expect(screen.getByRole("link", { name: "回到旅程" }).getAttribute("href")).toBe("/trips/trip-1");
    expect(screen.getByText("2 位旅客")).toBeTruthy();

    fireEvent.click(await screen.findByRole("button", { name: /^確認條件並開始搜尋 · / }));
    await waitFor(() => expect(postCalls("/searches")).toHaveLength(1));
    expect(requestBody(postCalls("/searches")[0])).toMatchObject({ trip_id: "trip-1", modules: ["flight"], origin: "TPE", destination: "KIX", departure_date: "2026-11-10", return_date: "2026-11-14" });

    await waitFor(() => expect(FakeEventSource.instances).toHaveLength(1));
    FakeEventSource.instances[0].emit("search.completed", { usage: { status: "charged", uses: 1, reference: "u-1" } });
    fireEvent.click(await screen.findByRole("button", { name: "帶入去程" }));
    await waitFor(() => expect(postCalls("/from-offer")).toHaveLength(1));
    expect(String(postCalls("/from-offer")[0][0])).toContain("/trips/trip-1/flight-anchors/outbound/from-offer");
    expect(requestBody(postCalls("/from-offer")[0])).toEqual({ version: 4, offer_id: "offer-1" });
    expect(await screen.findByRole("button", { name: "已帶入去程" })).toBeTruthy();
    expect(screen.getByText("旅程的去程錨點已更新為這筆報價。")).toBeTruthy();

    // The second leg goes in against the version the first attach came back with.
    fireEvent.click(screen.getByRole("button", { name: "帶入回程" }));
    await waitFor(() => expect(postCalls("/from-offer")).toHaveLength(2));
    expect(String(postCalls("/from-offer")[1][0])).toContain("/flight-anchors/return/from-offer");
    expect(requestBody(postCalls("/from-offer")[1])).toEqual({ version: 5, offer_id: "offer-1" });
    expect(await screen.findByText("旅程的去程與回程錨點已更新為這筆報價。")).toBeTruthy();
    // Trip mode is flights only: no plan cards, no "save as trip" button.
    expect(screen.queryByRole("tab", { name: "推薦組合" })).toBeNull();
    expect(screen.queryByRole("button", { name: "儲存並編輯行程" })).toBeNull();
  });

  it("asks for the home airport first and saves it on the trip", async () => {
    location.search = "trip_id=trip-1";
    const airportless = { ...tripCriteria, criteria: { ...tripCriteria.criteria, origin: null }, issues: [{ code: "trip_origin_required", detail: "這趟旅程還沒有出發機場" }] };
    vi.stubGlobal("fetch", stubTripApi({ criteria: [airportless, tripCriteria] }));
    render(<SearchExperience />);

    expect(await screen.findByText("這趟旅程還沒有出發機場")).toBeTruthy();
    const start = await screen.findByRole("button", { name: /^確認條件並開始搜尋 · / });
    expect((start as HTMLButtonElement).disabled).toBe(true);
    fireEvent.click(screen.getByRole("radio", { name: "松山 TSA" }));
    fireEvent.click(screen.getByRole("button", { name: "儲存出發地" }));
    await waitFor(() => expect(vi.mocked(fetch).mock.calls.some(([input, init]) => String(input).endsWith("/trips/trip-1") && init?.method === "PATCH")).toBe(true));
    const patch = vi.mocked(fetch).mock.calls.find(([input, init]) => String(input).endsWith("/trips/trip-1") && init?.method === "PATCH");
    expect(requestBody(patch as [RequestInfo | URL, RequestInit?])).toEqual({ version: 4, origin_airport: "TSA" });
    await waitFor(() => expect(screen.queryByText("這趟旅程還沒有出發機場")).toBeNull());
    expect((screen.getByRole("button", { name: /^確認條件並開始搜尋 · / }) as HTMLButtonElement).disabled).toBe(false);
    expect(postCalls("/searches")).toHaveLength(0);
  });

  it("retries an attach once with the trip's current version after a conflict", async () => {
    location.search = "trip_id=trip-1&resume=search";
    vi.stubGlobal("fetch", stubTripApi({
      attachResponses: [
        () => json({ code: "trip_version_conflict", detail: "旅程已被更新" }, 409),
        () => json({ id: "trip-1", version: 8 }),
      ],
    }));
    render(<SearchExperience />);

    await waitFor(() => expect(postCalls("/searches")).toHaveLength(1));
    await waitFor(() => expect(FakeEventSource.instances).toHaveLength(1));
    FakeEventSource.instances[0].emit("search.completed", {});
    fireEvent.click(await screen.findByRole("button", { name: "帶入回程" }));
    await waitFor(() => expect(postCalls("/from-offer")).toHaveLength(2));
    expect(requestBody(postCalls("/from-offer")[0])).toEqual({ version: 4, offer_id: "offer-1" });
    expect(requestBody(postCalls("/from-offer")[1])).toEqual({ version: 7, offer_id: "offer-1" });
    expect(await screen.findByRole("button", { name: "已帶入回程" })).toBeTruthy();
  });
});

describe("SearchExperience", () => {
  it("sends a visitor to sign in with a marker that resumes the search afterwards", async () => {
    location.search = criteria;
    vi.stubGlobal("fetch", stubApi({ signedIn: false }));
    render(<SearchExperience />);

    const link = await screen.findByRole("link", { name: "登入後開始搜尋" });
    expect(link.getAttribute("href")).toBe(`/login?next=${encodeURIComponent(`/search?${criteria}&resume=search`)}`);
    expect(postCalls("/searches")).toHaveLength(0);
  });

  it("starts the search once when a member returns with the resume marker, then drops it from the URL", async () => {
    location.search = `${criteria}&resume=search`;
    vi.stubGlobal("fetch", stubApi({ signedIn: true }));
    render(<SearchExperience />);

    await waitFor(() => expect(postCalls("/searches")).toHaveLength(1));
    expect(postCalls("/searches")[0][1]?.headers).toMatchObject({ "Idempotency-Key": expect.any(String) });
    expect(router.replace).toHaveBeenCalledWith(`/search?${criteria}`);
    expect(await screen.findByText("正在組合你的旅程")).toBeTruthy();
    // A later re-render must not fire a second paid search.
    await waitFor(() => expect(FakeEventSource.instances).toHaveLength(1));
    expect(postCalls("/searches")).toHaveLength(1);
  });

  it("never starts a paid search on its own without the marker", async () => {
    location.search = criteria;
    vi.stubGlobal("fetch", stubApi({ signedIn: true }));
    render(<SearchExperience />);

    expect(await screen.findByRole("button", { name: /^確認條件並開始搜尋 · / })).toBeTruthy();
    expect(postCalls("/searches")).toHaveLength(0);
    expect(router.replace).not.toHaveBeenCalled();
  });

  it("saves a plan with one idempotency key and reuses it when the save is retried", async () => {
    location.search = `${criteria}&resume=search`;
    vi.stubGlobal("fetch", stubApi({
      signedIn: true,
      tripResponses: [() => json({ detail: "資料庫忙碌" }, 503), () => json({ id: "trip-1" })],
    }));
    render(<SearchExperience />);

    await waitFor(() => expect(FakeEventSource.instances).toHaveLength(1));
    FakeEventSource.instances[0].emit("optimization.completed", { plans: [plan] });
    FakeEventSource.instances[0].emit("search.completed", { usage: { status: "charged", uses: 1, reference: "u-1" } });

    fireEvent.click(await screen.findByRole("button", { name: "儲存並編輯行程" }));
    await screen.findByText("資料庫忙碌");
    fireEvent.click(screen.getByRole("button", { name: "儲存並編輯行程" }));
    await waitFor(() => expect(router.push).toHaveBeenCalledWith("/trips/trip-1"));

    const saves = postCalls("/trips");
    expect(saves).toHaveLength(2);
    const keys = saves.map(([, init]) => (init?.headers as Record<string, string>)["Idempotency-Key"]);
    expect(keys[0]).toEqual(expect.any(String));
    expect(keys[1]).toBe(keys[0]);
  });

  it("says which prices are paused in the reader's language, not the API's", async () => {
    // The badge used to print the API's own `message`, and the live site greeted an
    // English reader with 「目前沒有可用的航班查價供應商。；目前沒有可用的飯店查價供應商。」
    location.search = criteria;
    vi.stubGlobal("fetch", stubApi({
      signedIn: true,
      providers: {
        provider: "none",
        mode: "disabled",
        status: "not_configured",
        modules: ["flight", "hotel"],
        message: "目前沒有可用的航班查價供應商。；目前沒有可用的飯店查價供應商。",
        module_statuses: {
          flight: { selected_provider: "none", status: "not_configured", available: false, configured: false, environment: "production", message: "目前沒有可用的航班查價供應商。" },
          hotel: { selected_provider: "none", status: "not_configured", available: false, configured: false, environment: "production", message: "目前沒有可用的飯店查價供應商。" },
        },
      },
    }));
    render(<SearchExperience />);

    expect(await screen.findByText("航班查價暫停")).toBeTruthy();
    expect(screen.getByText("住宿查價暫停")).toBeTruthy();
    expect(document.body.textContent).not.toContain("目前沒有可用的航班查價供應商");
  });

  it("names the provider when live pricing is on", async () => {
    location.search = criteria;
    vi.stubGlobal("fetch", stubApi({
      signedIn: true,
      providers: { provider: "skyscanner", mode: "live", status: "ready", modules: ["flight"], message: "Skyscanner 即時航班比價已啟用。" },
    }));
    render(<SearchExperience />);

    expect(await screen.findByText("即時報價 · skyscanner")).toBeTruthy();
  });

  it("labels the multi-source comparison as free like every other action", async () => {
    location.search = `${criteria}&resume=search`;
    vi.stubGlobal("fetch", stubApi({ signedIn: true }));
    render(<SearchExperience />);

    await waitFor(() => expect(FakeEventSource.instances).toHaveLength(1));
    FakeEventSource.instances[0].emit("search.completed", { usage: { status: "charged", uses: 1, reference: "u-1" } });
    fireEvent.click(await screen.findByRole("tab", { name: "機票" }));
    expect(await screen.findByRole("button", { name: "比較更多來源 · 不扣次" })).toBeTruthy();
  });
});
