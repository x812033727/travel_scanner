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
