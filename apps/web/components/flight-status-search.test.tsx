import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { FlightStatusSearch } from "./flight-status-search";

const { session, location } = vi.hoisted(() => ({
  session: { status: "authenticated" as "loading" | "authenticated" | "signed_out" | "unavailable" },
  location: { search: "" },
}));
vi.mock("next/navigation", () => ({
  useSearchParams: () => new URLSearchParams(location.search),
}));
vi.mock("@/i18n/navigation", () => ({
  usePathname: () => "/flights/status",
  Link: ({ href, children, ...props }: React.AnchorHTMLAttributes<HTMLAnchorElement> & { href: string }) => <a href={href} {...props}>{children}</a>,
}));
vi.mock("@/components/saved-items-provider", () => ({
  useSavedItems: () => ({ status: session.status, isSaved: () => false, setSaved: async () => undefined, toggle: async () => false }),
}));

afterEach(() => {
  session.status = "authenticated";
  location.search = "";
  vi.unstubAllGlobals();
});

function json(body: unknown, status = 200) {
  return new Response(JSON.stringify(body), { status, headers: { "Content-Type": "application/json" } });
}

const statusItem = {
  item_id: "item-1",
  ident: "BR198",
  origin: "TPE",
  destination: "NRT",
  status: "scheduled",
  schedule_only: false,
  departure_delay_seconds: 1500,
  departure_gate: "A7",
  scheduled_out: "2026-11-10T00:50:00Z",
};

function stubApi(onSave?: () => Response) {
  return vi.fn(async (input: RequestInfo | URL, init?: RequestInit) => {
    const url = String(input);
    if (url.endsWith("/status-lookups") && init?.method === "POST") {
      return json({ id: "lookup-1", items: [statusItem], cache_hit: false, usage: { status: "charged", uses: 1 } });
    }
    if (url.endsWith("/flight-status")) return (onSave || (() => json({ id: "trip-1", version: 3 })))();
    if (url.endsWith("/trips/trip-1")) return json({ id: "trip-1", version: 2 });
    return json({});
  });
}

describe("FlightStatusSearch", () => {
  it("sends a visitor to sign in instead of showing a live charge button", () => {
    session.status = "signed_out";
    render(<FlightStatusSearch />);
    const link = screen.getByRole("link", { name: "登入後查詢 · 消耗 1 次" });
    expect(link.getAttribute("href")).toBe("/login?next=%2Fflights%2Fstatus");
    expect(screen.queryByRole("button", { name: /^查詢 · / })).toBeNull();
  });

  it("keeps the priced lookup button for a signed-in member", () => {
    render(<FlightStatusSearch />);
    expect(screen.getByRole("button", { name: "查詢 · 消耗 1 次" })).toBeTruthy();
    expect(screen.queryByRole("link", { name: /登入後查詢/ })).toBeNull();
  });

  it("arrives from a trip with the flight and day already filled in", () => {
    location.search = "trip_id=trip-1&direction=outbound&flight_number=BR198&date=2026-11-10";
    vi.stubGlobal("fetch", stubApi());
    render(<FlightStatusSearch />);

    expect((screen.getByLabelText("班號") as HTMLInputElement).value).toBe("BR198");
    expect((screen.getByLabelText("出發日期") as HTMLInputElement).value).toBe("2026-11-10");
    expect(screen.getByRole("link", { name: "回到旅程" }).getAttribute("href")).toBe("/trips/trip-1");
  });

  it("writes a result back onto the anchor against the trip's current version", async () => {
    location.search = "trip_id=trip-1&direction=outbound&flight_number=BR198&date=2026-11-10";
    const fetchMock = stubApi();
    vi.stubGlobal("fetch", fetchMock);
    render(<FlightStatusSearch />);

    fireEvent.submit(screen.getByRole("button", { name: "查詢 · 消耗 1 次" }).closest("form")!);
    fireEvent.click(await screen.findByRole("button", { name: "寫回旅程" }));
    await waitFor(() => expect(
      fetchMock.mock.calls.some(([input]) => String(input).includes("/flight-anchors/outbound/flight-status")),
    ).toBe(true));
    const call = fetchMock.mock.calls.find(([input]) => String(input).includes("/flight-status"));
    // The version is read immediately before the write; this page never held the trip.
    expect(JSON.parse(String(call?.[1]?.body))).toEqual({ version: 2, lookup_id: "lookup-1", item_id: "item-1" });
    expect(await screen.findByRole("button", { name: "已寫回旅程" })).toBeTruthy();
  });

  it("offers no write-back when the lookup did not come from a trip", async () => {
    vi.stubGlobal("fetch", stubApi());
    render(<FlightStatusSearch />);
    fireEvent.change(screen.getByLabelText("班號"), { target: { value: "BR198" } });
    fireEvent.change(screen.getByLabelText("出發日期"), { target: { value: "2026-11-10" } });
    fireEvent.submit(screen.getByRole("button", { name: "查詢 · 消耗 1 次" }).closest("form")!);
    expect(await screen.findByText("查詢結果")).toBeTruthy();
    expect(screen.queryByRole("button", { name: "寫回旅程" })).toBeNull();
  });

  it("still shows the button when the session probe failed for another reason", () => {
    session.status = "unavailable";
    render(<FlightStatusSearch />);
    expect(screen.getByRole("button", { name: "查詢 · 消耗 1 次" })).toBeTruthy();
  });
});
