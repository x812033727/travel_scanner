import { act, cleanup, fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import type { ComponentProps, ReactNode } from "react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { ApiError } from "@/lib/api";
import type { DiscoveryItem, DiscoveryPlanning } from "@/lib/discovery";
import { completedTripDestination } from "@/lib/frontend-flow";
import { frontendCopy } from "@/lib/frontend-navigation";
import { TravelPlanAction } from "./travel-card-actions";

const mocks = vi.hoisted(() => ({
  api: vi.fn<(path: string, options?: RequestInit) => Promise<unknown>>(),
  router: { push: vi.fn(), replace: vi.fn(), refresh: vi.fn() },
  session: {
    user: { id: "member-one", email: "one@example.test" } as { id: string; email: string } | null,
    status: "authenticated",
    sessionIdentity: {} as object | null,
  },
}));

vi.mock("@/lib/api", async (importOriginal) => ({
  ...await importOriginal<typeof import("@/lib/api")>(), api: mocks.api,
}));
vi.mock("@/components/header-session", () => ({ useHeaderSession: () => mocks.session }));
vi.mock("next-intl", async (importOriginal) => ({
  ...await importOriginal<typeof import("next-intl")>(), useLocale: () => "en",
}));
vi.mock("next/navigation", () => ({ useSearchParams: () => new URLSearchParams(window.location.search) }));
vi.mock("@/i18n/navigation", () => ({
  Link: ({ href, children, ...props }: ComponentProps<"a">) => <a href={href} {...props}>{children}</a>,
  usePathname: () => "/explore", useRouter: () => mocks.router,
}));
vi.mock("@/components/community/ui", async (importOriginal) => ({
  ...await importOriginal<typeof import("@/components/community/ui")>(),
  // Focus trapping itself belongs to the native Dialog tests. Here the real
  // controls and effects remain mounted while transport outcomes are controlled.
  Dialog: ({ title, children, onClose }: { title: string; children: ReactNode; onClose: () => void }) =>
    <section role="dialog" aria-label={title}><button onClick={onClose}>Close</button>{children}</section>,
}));

const copy = frontendCopy("en");
const contentId = "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa";
const merchantId = "bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb";
const tripId = "cccccccc-cccc-4ccc-8ccc-cccccccccccc";
const otherTripId = "dddddddd-dddd-4ddd-8ddd-dddddddddddd";
const returnTo = "/en/explore?category=hotspots&destination=tokyo#reading";

function item(kind: DiscoveryItem["kind"] = "hotspot"): DiscoveryItem {
  return {
    id: `${kind}:${contentId}`, kind, title: "Reviewed fixture place", summary: "Fixture",
    locale: "en", href: "/explore", destination: { id: "tokyo", name: "Tokyo" },
    source: { label: "Fixture editorial", kind: "editorial", url: null },
    published_at: null, updated_at: null, thumbnail_url: null,
  };
}

function detail(kind: "hotspot" | "food" | "merchant" | "hotel" = "hotspot"): DiscoveryItem {
  const planning: DiscoveryPlanning = {
    kind, id: contentId, destination_id: "tokyo", merchants: [],
    ...(kind === "hotel" ? { product_id: contentId }
      : { selection_path: `/${kind === "hotspot" ? "hotspots" : kind === "merchant" ? "foods/merchants" : "foods"}/${contentId}/trip-selections` }),
  };
  if (kind === "food") planning.merchants = [{
    id: merchantId, name: "Reviewed restaurant", destination_id: "tokyo",
    selection_path: `/foods/merchants/${merchantId}/trip-selections`,
  }];
  return { ...item(kind), detail: { planning, guides: [], merchants: [] } };
}

function trip(overrides: Partial<{
  trip_id: string; name: string; version: number; start_date: string; end_date: string;
  destination_name: string; destination_id: string | null;
}> = {}) {
  return {
    trip_id: tripId, name: "My Tokyo trip", version: 3,
    start_date: "2026-11-11", end_date: "2026-11-13",
    destination_name: "東京", destination_id: "tokyo", ...overrides,
  };
}

function setupTransport(content = detail(), trips = [trip()]) {
  const state = { content, trips, write: vi.fn<() => Promise<unknown>>().mockResolvedValue({ ok: true }) };
  mocks.api.mockImplementation(async (path, options) => {
    if (options?.method === "POST") return state.write();
    if (path === "/trips/options") return { items: state.trips, can_create: true, count: state.trips.length, limit: 20 };
    if (path === `/discovery/content/${content.kind}/${contentId}`) return state.content;
    throw new Error(`Unexpected fixture request: ${path}`);
  });
  return state;
}

function writes() { return mocks.api.mock.calls.filter(([, options]) => options?.method === "POST"); }
function deferred<T>() {
  let resolve!: (value: T) => void;
  let reject!: (reason: unknown) => void;
  const promise = new Promise<T>((yes, no) => { resolve = yes; reject = no; });
  return { promise, resolve, reject };
}
async function open(kind: DiscoveryItem["kind"] = "hotspot") {
  fireEvent.click(screen.getByRole("button", { name: kind === "hotel" ? copy.hotel : copy.plan }));
  const dialog = screen.getByRole("dialog");
  await within(dialog).findByLabelText(copy.chooseTrip);
  return dialog;
}

beforeEach(() => {
  mocks.api.mockReset();
  mocks.router.push.mockReset(); mocks.router.replace.mockReset(); mocks.router.refresh.mockReset();
  mocks.session.user = { id: "member-one", email: "one@example.test" };
  mocks.session.status = "authenticated"; mocks.session.sessionIdentity = {};
  sessionStorage.clear();
  window.history.replaceState(null, "", "/explore?category=hotspots&destination=tokyo");
});
afterEach(() => { cleanup(); sessionStorage.clear(); window.history.replaceState(null, "", "/"); });

describe("shared frontend planning action", () => {
  it("preselects only a single canonical destination match across display languages", async () => {
    setupTransport(detail(), [
      trip({ trip_id: otherTripId, name: "Seoul trip", destination_name: "首爾", destination_id: "seoul" }), trip(),
    ]);
    render(<TravelPlanAction item={item()} returnTo={returnTo} />);
    const dialog = await open();
    expect((within(dialog).getByLabelText(copy.chooseTrip) as HTMLSelectElement).value).toBe(tripId);
    expect((within(dialog).getByLabelText(copy.chooseDay) as HTMLSelectElement).value).toBe("2026-11-11");
    expect(within(dialog).getByRole("button", { name: copy.confirm }).hasAttribute("disabled")).toBe(false);
    expect(writes()).toHaveLength(0);
    fireEvent.click(within(dialog).getByRole("button", { name: copy.confirm }));
    await screen.findByRole("link", { name: copy.openTrip });
    expect(JSON.parse(String(writes()[0][1]?.body))).toEqual({ trip_id: tripId, version: 3, day_date: "2026-11-11" });
  });

  it("does not guess between two matching trips", async () => {
    setupTransport(detail(), [trip(), trip({ trip_id: otherTripId, name: "Another Tokyo trip" })]);
    render(<TravelPlanAction item={item()} returnTo={returnTo} />);
    const dialog = await open();
    expect((within(dialog).getByLabelText(copy.chooseTrip) as HTMLSelectElement).value).toBe("");
    expect(within(dialog).getByRole("button", { name: copy.confirm }).hasAttribute("disabled")).toBe(true);
    expect(writes()).toHaveLength(0);
  });

  it("requires the user to select a real restaurant and meal for a dish", async () => {
    setupTransport(detail("food"));
    render(<TravelPlanAction item={item("food")} returnTo={returnTo} />);
    const dialog = await open("food");
    expect((within(dialog).getByLabelText(copy.chooseMerchant) as HTMLSelectElement).value).toBe("");
    expect(within(dialog).getByRole("button", { name: copy.confirm }).hasAttribute("disabled")).toBe(true);
    expect(writes()).toHaveLength(0);
    fireEvent.change(within(dialog).getByLabelText(copy.chooseMerchant), { target: { value: merchantId } });
    fireEvent.change(within(dialog).getByLabelText(copy.meal), { target: { value: "dinner" } });
    fireEvent.change(within(dialog).getByLabelText(copy.chooseDay), { target: { value: "2026-11-12" } });
    expect(within(dialog).getByText(copy.mealWarning)).toBeTruthy();
    fireEvent.click(within(dialog).getByRole("button", { name: copy.confirm }));
    await screen.findByRole("link", { name: copy.openTrip });
    expect(writes()[0][0]).toBe(`/foods/${contentId}/trip-selections`);
    expect(JSON.parse(String(writes()[0][1]?.body))).toEqual({
      trip_id: tripId, version: 3, day_date: "2026-11-12", merchant_id: merchantId, meal_role: "dinner",
    });
  });

  it("shows the every-day hotel replacement warning and waits for explicit confirmation", async () => {
    setupTransport(detail("hotel"));
    render(<TravelPlanAction item={item("hotel")} returnTo={returnTo} />);
    const dialog = await open("hotel");
    expect(within(dialog).getByText(copy.hotelWarning)).toBeTruthy();
    expect(within(dialog).queryByLabelText(copy.chooseDay)).toBeNull();
    expect(writes()).toHaveLength(0);
    fireEvent.click(within(dialog).getByRole("button", { name: copy.confirmHotel }));
    await screen.findByRole("link", { name: copy.openTrip });
    expect(writes()[0][0]).toBe(`/trips/${tripId}/travel-services`);
    expect(JSON.parse(String(writes()[0][1]?.body))).toEqual({ product_id: contentId, version: 3 });
    expect(new Headers(writes()[0][1]?.headers).get("Idempotency-Key")).toBeTruthy();
  });

  it("keeps a guest return intent without fetching private trips or writing", () => {
    mocks.session.user = null; mocks.session.status = "signed_out"; mocks.session.sessionIdentity = null;
    render(<TravelPlanAction item={item()} returnTo={returnTo} />);
    fireEvent.click(screen.getByRole("button", { name: copy.plan }));
    const login = screen.getByRole("link", { name: copy.login });
    const url = new URL(login.getAttribute("href")!, "https://example.test");
    expect(url.pathname).toBe("/login");
    const next = new URL(url.searchParams.get("next")!, "https://example.test");
    expect(next.pathname).toBe("/explore");
    expect(next.searchParams.get("category")).toBe("hotspots");
    expect(next.searchParams.get("destination")).toBe("tokyo");
    expect(next.searchParams.get("resume_action")).toBe("trip");
    expect(next.searchParams.get("resume_item")).toBe(`hotspot:${contentId}`);
    expect(next.hash).toBe("#reading");
    expect(mocks.api).not.toHaveBeenCalled();
    expect(sessionStorage.length).toBe(0);
  });

  it("saves an account-bound create-trip intent and returns only to confirmation when marked", async () => {
    setupTransport();
    render(<TravelPlanAction item={item()} returnTo={returnTo} />);
    const dialog = await open();
    fireEvent.click(within(dialog).getByRole("button", { name: copy.create }));
    expect(mocks.router.push).toHaveBeenCalledWith("/trips/new?resume_plan=1");
    expect(writes()).toHaveLength(0);
    const stored = JSON.parse(sessionStorage.getItem("mokaair-pending-plan:member-one")!);
    expect(stored).toMatchObject({ accountId: "member-one", kind: "hotspot", id: contentId });
    expect(stored).not.toHaveProperty("title"); expect(stored).not.toHaveProperty("trip_id");
    expect(completedTripDestination("member-two", tripId, true)).toBe(`/trips/${tripId}`);
    expect(completedTripDestination("member-one", tripId, false)).toBe(`/trips/${tripId}`);
    const resumed = new URL(completedTripDestination("member-one", tripId, true), "https://example.test");
    expect(resumed.searchParams.get("resume_trip")).toBe(tripId);
    expect(resumed.searchParams.get("resume_item")).toBe(`hotspot:${contentId}`);
    expect(sessionStorage.getItem("mokaair-pending-plan:member-one")).toBeNull();
    expect(writes()).toHaveLength(0);
  });

  it("restores a login/create-trip return to a chosen trip without automatically committing", async () => {
    window.history.replaceState(null, "", `/explore?resume_action=trip&resume_item=hotspot:${contentId}&resume_trip=${otherTripId}`);
    setupTransport(detail(), [trip(), trip({ trip_id: otherTripId, name: "New trip" })]);
    render(<TravelPlanAction item={item()} returnTo={returnTo} />);
    const dialog = await screen.findByRole("dialog");
    await waitFor(() => expect((within(dialog).getByLabelText(copy.chooseTrip) as HTMLSelectElement).value).toBe(otherTripId));
    expect(writes()).toHaveLength(0);
  });

  it("requires a fresh read and a second explicit confirmation after a version conflict", async () => {
    const transport = setupTransport();
    transport.write.mockRejectedValueOnce(new ApiError("Changed", 409));
    render(<TravelPlanAction item={item()} returnTo={returnTo} />);
    const dialog = await open();
    fireEvent.click(within(dialog).getByRole("button", { name: copy.confirm }));
    await within(dialog).findByText(copy.conflict);
    expect(within(dialog).getByRole("button", { name: copy.confirm }).hasAttribute("disabled")).toBe(true);
    transport.trips = [trip({ version: 4 })];
    fireEvent.click(within(dialog).getByRole("button", { name: copy.retry }));
    await waitFor(() => expect(within(dialog).getByRole("button", { name: copy.confirm }).hasAttribute("disabled")).toBe(false));
    expect(writes()).toHaveLength(1);
    fireEvent.click(within(dialog).getByRole("button", { name: copy.confirm }));
    await screen.findByRole("link", { name: copy.openTrip });
    expect(JSON.parse(String(writes()[1][1]?.body)).version).toBe(4);
    expect(new Headers(writes()[0][1]?.headers).get("Idempotency-Key"))
      .not.toBe(new Headers(writes()[1][1]?.headers).get("Idempotency-Key"));
  });

  it.each([new TypeError("Connection lost"), new ApiError("Gateway timeout", 504)])(
    "never resubmits an uncertain hotspot selection, including after closing and reopening (%s)", async (failure) => {
      const transport = setupTransport(); transport.write.mockRejectedValueOnce(failure);
      render(<TravelPlanAction item={item()} returnTo={returnTo} />);
      let dialog = await open();
      fireEvent.click(within(dialog).getByRole("button", { name: copy.confirm }));
      await within(dialog).findByText(copy.uncertain);
      expect(within(dialog).getByRole("button", { name: copy.confirm }).hasAttribute("disabled")).toBe(true);
      expect(within(dialog).queryByRole("button", { name: copy.retry })).toBeNull();
      expect(within(dialog).getByRole("link", { name: copy.openTrip }).getAttribute("href")).toBe(`/trips/${tripId}`);
      expect(within(dialog).getByRole("button", { name: copy.create }).hasAttribute("disabled")).toBe(true);
      fireEvent.click(within(dialog).getByRole("button", { name: "Close" }));
      transport.trips = [trip({ version: 4 })];
      dialog = await open();
      expect(within(dialog).getByText(copy.uncertain)).toBeTruthy();
      fireEvent.click(within(dialog).getByRole("button", { name: copy.confirm }));
      expect(writes()).toHaveLength(1);
    },
  );

  it("replays an uncertain hotel with its original path, body and key after a newer read", async () => {
    const transport = setupTransport(detail("hotel"));
    transport.write.mockRejectedValueOnce(new TypeError("Connection lost"));
    render(<TravelPlanAction item={item("hotel")} returnTo={returnTo} />);
    let dialog = await open("hotel");
    fireEvent.click(within(dialog).getByRole("button", { name: copy.confirmHotel }));
    await within(dialog).findByRole("alert");
    expect(within(dialog).getByLabelText(copy.chooseTrip).hasAttribute("disabled")).toBe(true);
    fireEvent.click(within(dialog).getByRole("button", { name: "Close" }));
    transport.trips = [trip({ version: 4 })];
    dialog = await open("hotel");
    fireEvent.click(within(dialog).getByRole("button", { name: copy.confirmHotel }));
    await screen.findByRole("link", { name: copy.openTrip });
    expect(writes()).toHaveLength(2);
    expect(writes()[1]).toEqual(writes()[0]);
    expect(JSON.parse(String(writes()[1][1]?.body)).version).toBe(3);
  });

  it("ignores an old account's pending write response after switching accounts", async () => {
    const pending = deferred<unknown>();
    const transport = setupTransport(); transport.write.mockReturnValueOnce(pending.promise);
    const view = render(<TravelPlanAction item={item()} returnTo={returnTo} />);
    const dialog = await open();
    fireEvent.click(within(dialog).getByRole("button", { name: copy.confirm }));
    await waitFor(() => expect(writes()).toHaveLength(1));
    mocks.session.user = { id: "member-two", email: "two@example.test" }; mocks.session.sessionIdentity = {};
    view.rerender(<TravelPlanAction item={item()} returnTo={returnTo} />);
    expect(screen.queryByRole("dialog")).toBeNull();
    await act(async () => { pending.resolve({ ok: true }); await pending.promise; });
    expect(screen.queryByRole("link", { name: copy.openTrip })).toBeNull();
    expect(screen.queryByText(copy.added)).toBeNull();
    expect(writes()).toHaveLength(1);
  });

  it("aborts and ignores an old account's private trip read", async () => {
    const pending = deferred<unknown>();
    setupTransport();
    const normal = mocks.api.getMockImplementation()!;
    mocks.api.mockImplementation((path, options) => path === "/trips/options" ? pending.promise : normal(path, options));
    const view = render(<TravelPlanAction item={item()} returnTo={returnTo} />);
    fireEvent.click(screen.getByRole("button", { name: copy.plan }));
    const originalRead = mocks.api.mock.calls.find(([path]) => path === "/trips/options")!;
    mocks.session.user = { id: "member-two", email: "two@example.test" }; mocks.session.sessionIdentity = {};
    view.rerender(<TravelPlanAction item={item()} returnTo={returnTo} />);
    expect(originalRead[1]?.signal?.aborted).toBe(true);
    await act(async () => { pending.resolve({ items: [trip({ name: "Old account private trip" })] }); await pending.promise; });
    expect(screen.queryByText(/Old account private trip/)).toBeNull();
    expect(screen.queryByRole("dialog")).toBeNull();
    expect(writes()).toHaveLength(0);
  });
});
