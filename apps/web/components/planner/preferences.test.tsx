import "@testing-library/jest-dom/vitest";
import { act, cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { api } from "@/lib/api";
import type { Trip } from "@/lib/trip-types";
import { PlannerPreferences } from "./preferences";

vi.mock("@/lib/api", () => ({ api: vi.fn() }));

function makeTrip(): Trip {
  return {
    id: "trip-1", name: "Tokyo", version: 4, mode: "manual", total_price: 0, currency: "TWD", items: [], route_preference: "LESS_WALKING",
    data: {
      source: "search", search_criteria: { cabin_class: "business" }, original_provider: { keep: true },
      travelers: { adults: 2, children: 1, rooms: 2, children_ages: [8], stored_unknown: "keep" },
      preferences: {
        budget_twd: 55000, pace: "relaxed", interests: ["shopping", "custom-interest"], shop_themes: ["vintage", "local-theme"],
        accepted_property_types: ["serviced_apartment"], hotel_min_review_score: 8.5, hotel_min_rating: 2,
        hotel_min_review_count: 75, max_station_walk_minutes: 17, hotel_min_nightly_twd: 1000, hotel_max_nightly_twd: 8000,
        preferred_area: "Shinjuku", preferred_areas: ["Shinjuku", "Shibuya"], avoid_red_eye: true,
        pet_companion: { species: "dog", count: 1, unknown_nested: true }, unknown_preference: { keep: true },
      },
    },
  };
}
function mount(trip = makeTrip(), prepare = vi.fn<() => Promise<Trip | undefined>>().mockResolvedValue({ ...trip, version: 7 })) {
  const onUpdated = vi.fn();
  render(<PlannerPreferences trip={trip} prepare={prepare} onUpdated={onUpdated} />);
  fireEvent.click(screen.getByText("旅伴與旅行偏好", { selector: "summary" }));
  return { trip, prepare, onUpdated };
}
function save() { fireEvent.submit(screen.getByRole("form", { name: "旅伴與旅行偏好" })); }
function body() { return JSON.parse(vi.mocked(api).mock.calls[0][1]?.body as string); }

afterEach(cleanup);
beforeEach(() => { vi.mocked(api).mockReset(); });

describe("PlannerPreferences", () => {
  it("starts collapsed with existing values and no metadata route editor", () => {
    render(<PlannerPreferences trip={makeTrip()} prepare={vi.fn()} onUpdated={vi.fn()} />);
    expect(screen.getByText("旅伴與旅行偏好", { selector: "summary" }).closest("details")).not.toHaveAttribute("open");
    fireEvent.click(screen.getByText("旅伴與旅行偏好", { selector: "summary" }));
    expect(screen.getByLabelText("成人")).toHaveValue("2");
    expect(screen.getByLabelText("整趟總預算（台幣）")).toHaveValue(55000);
    expect(screen.getByLabelText("最低星級")).toHaveValue("2");
    expect(screen.getByLabelText("最低住客評分")).toHaveValue("8.5");
    expect(screen.getByLabelText("最低評論數")).toHaveValue("75");
    expect(screen.getByLabelText("車站步行上限")).toHaveValue("17");
    expect(screen.getByRole("button", { name: "悠閒" })).toHaveAttribute("aria-pressed", "true");
    expect(screen.queryByLabelText("大眾運輸偏好")).not.toBeInTheDocument();
  });

  it("does not prepare or PATCH an unchanged form, even with unrepresented stored settings", () => {
    const { prepare, onUpdated } = mount();
    save();
    expect(prepare).not.toHaveBeenCalled(); expect(api).not.toHaveBeenCalled(); expect(onUpdated).not.toHaveBeenCalled();
    expect(screen.queryByRole("alert")).not.toBeInTheDocument();
  });

  it("keeps an unsaved edit across itinerary autosave props without reverting unrelated latest preferences", async () => {
    const trip = makeTrip();
    const latest = { ...trip, version: 9, data: { ...trip.data, preferences: { ...(trip.data.preferences as object), preferred_area: "Ueno" } } };
    const prepare = vi.fn().mockResolvedValue(latest);
    const onUpdated = vi.fn();
    const view = render(<PlannerPreferences trip={trip} prepare={prepare} onUpdated={onUpdated} />);
    fireEvent.click(screen.getByText("旅伴與旅行偏好", { selector: "summary" }));
    fireEvent.change(screen.getByLabelText("整趟總預算（台幣）"), { target: { value: "65000" } });
    view.rerender(<PlannerPreferences trip={latest} prepare={prepare} onUpdated={onUpdated} />);
    expect(screen.getByLabelText("整趟總預算（台幣）")).toHaveValue(65000);
    vi.mocked(api).mockResolvedValue({ ...latest, version: 10 });
    save();
    await waitFor(() => expect(onUpdated).toHaveBeenCalledOnce());
    expect(body()).toEqual({ version: 9, preferences: { budget_twd: 65000 } });
    expect(screen.getByLabelText("偏好住宿區域")).toHaveValue("Ueno");
  });

  it("PATCHes only changed keys after flushing, preserving unknown/source/untouched settings", async () => {
    const original = makeTrip();
    const before = JSON.stringify(original);
    const updated = { ...original, version: 8, data: { ...original.data, travelers: { ...(original.data.travelers as object), adults: 3 }, preferences: { ...(original.data.preferences as object), budget_twd: 60000 } } };
    vi.mocked(api).mockResolvedValue(updated);
    const { prepare, onUpdated } = mount(original);
    fireEvent.change(screen.getByLabelText("成人"), { target: { value: "3" } });
    fireEvent.change(screen.getByLabelText("整趟總預算（台幣）"), { target: { value: "60000" } });
    save();
    await waitFor(() => expect(onUpdated).toHaveBeenCalledWith(updated));
    expect(prepare).toHaveBeenCalledTimes(1);
    expect(api).toHaveBeenCalledWith("/trips/trip-1", expect.objectContaining({ method: "PATCH" }));
    expect(body()).toEqual({ version: 7, travelers: { adults: 3 }, preferences: { budget_twd: 60000 } });
    expect(JSON.stringify(original)).toBe(before);
    expect(screen.getByRole("status")).toHaveTextContent("偏好已儲存，原有行程保持不變。");
    save();
    expect(api).toHaveBeenCalledTimes(1);
  });

  it("validates counts and nightly bounds locally without preparing or calling the API", () => {
    const { prepare } = mount();
    fireEvent.change(screen.getByLabelText("每晚最低（台幣）"), { target: { value: "9000" } });
    save();
    expect(screen.getByRole("alert")).toHaveTextContent("請確認旅伴人數與偏好欄位。");
    expect(api).not.toHaveBeenCalled(); expect(prepare).not.toHaveBeenCalled();
    fireEvent.change(screen.getByLabelText("每晚最低（台幣）"), { target: { value: "1000" } });
    fireEvent.change(screen.getByLabelText("成人"), { target: { value: "" } });
    save();
    expect(screen.getByRole("alert")).toBeInTheDocument(); expect(api).not.toHaveBeenCalled();
  });

  it("preserves valid larger child counts and decimal review scores on unrelated edits", async () => {
    const trip = makeTrip();
    trip.data.travelers = { adults: 1, children: 7, rooms: 2, children_ages: [1, 2, 3, 4, 5, 6, 7] };
    vi.mocked(api).mockResolvedValue({ ...trip, version: 8 });
    mount(trip);
    expect(screen.getByLabelText("兒童")).toHaveValue("7");
    fireEvent.click(screen.getByRole("button", { name: "充實" }));
    save();
    await waitFor(() => expect(api).toHaveBeenCalledTimes(1));
    expect(body()).toEqual({ version: 7, preferences: { pace: "packed" } });
  });

  it("displays numeric strings from stored JSON and leaves them untouched on unrelated edits", async () => {
    const trip = makeTrip();
    trip.data.travelers = { adults: "2", children: "1", rooms: "2", children_ages: [8] };
    trip.data.preferences = { ...(trip.data.preferences as object), budget_twd: "55000", hotel_min_nightly_twd: "1000", hotel_min_review_score: "8.5" };
    vi.mocked(api).mockResolvedValue({ ...trip, version: 8 });
    mount(trip);
    expect(screen.getByLabelText("成人")).toHaveValue("2");
    expect(screen.getByLabelText("整趟總預算（台幣）")).toHaveValue(55000);
    expect(screen.getByLabelText("每晚最低（台幣）")).toHaveValue(1000);
    fireEvent.change(screen.getByLabelText("整趟總預算（台幣）"), { target: { value: "055000" } });
    save(); expect(api).not.toHaveBeenCalled();
    fireEvent.click(screen.getByRole("button", { name: "充實" })); save();
    await waitFor(() => expect(api).toHaveBeenCalledTimes(1));
    expect(body()).toEqual({ version: 7, preferences: { pace: "packed" } });
  });

  it("clears nullable fields explicitly while preserving other preferences", async () => {
    vi.mocked(api).mockResolvedValue({ ...makeTrip(), version: 8 });
    mount();
    fireEvent.change(screen.getByLabelText("整趟總預算（台幣）"), { target: { value: "" } });
    fireEvent.change(screen.getByLabelText("每晚最低（台幣）"), { target: { value: "" } });
    save();
    await waitFor(() => expect(api).toHaveBeenCalledTimes(1));
    expect(body()).toEqual({ version: 7, preferences: { budget_twd: null, hotel_min_nightly_twd: null } });
  });

  it("preserves unfamiliar interests and themes when toggling a known interest", async () => {
    vi.mocked(api).mockResolvedValue({ ...makeTrip(), version: 8 });
    mount();
    fireEvent.click(screen.getByRole("button", { name: "美食" }));
    save();
    await waitFor(() => expect(api).toHaveBeenCalledTimes(1));
    expect(body()).toEqual({ version: 7, preferences: { interests: ["shopping", "custom-interest", "food"] } });
  });

  it("clears dependent shop themes when shopping is removed", async () => {
    vi.mocked(api).mockResolvedValue({ ...makeTrip(), version: 8 });
    mount();
    fireEvent.click(screen.getByRole("button", { name: "購物" }));
    save();
    await waitFor(() => expect(api).toHaveBeenCalledTimes(1));
    expect(body()).toEqual({ version: 7, preferences: { interests: ["custom-interest"], shop_themes: [] } });
  });

  it("updates children without submitting an invalid old age list", async () => {
    vi.mocked(api).mockResolvedValue({ ...makeTrip(), version: 8 });
    mount();
    fireEvent.change(screen.getByLabelText("兒童"), { target: { value: "2" } });
    save();
    await waitFor(() => expect(api).toHaveBeenCalledTimes(1));
    expect(body()).toEqual({ version: 7, travelers: { children: 2, children_ages: [] } });
  });

  it("guards repeated submits while prepare or PATCH is in flight", async () => {
    let finishPrepare!: (value: Trip) => void;
    let finishPatch!: (value: Trip) => void;
    const prepare = vi.fn(() => new Promise<Trip>((resolve) => { finishPrepare = resolve; }));
    vi.mocked(api).mockImplementation(() => new Promise((resolve) => { finishPatch = resolve as (value: Trip) => void; }));
    const { onUpdated } = mount(makeTrip(), prepare);
    fireEvent.click(screen.getByRole("button", { name: "充實" }));
    save(); save();
    expect(prepare).toHaveBeenCalledTimes(1); expect(api).not.toHaveBeenCalled();
    expect(screen.getByRole("button", { name: "儲存偏好" })).toBeDisabled();
    await act(async () => { finishPrepare({ ...makeTrip(), version: 9 }); });
    save();
    expect(api).toHaveBeenCalledTimes(1); expect(body().version).toBe(9);
    const updated = { ...makeTrip(), version: 10 };
    await act(async () => { finishPatch(updated); });
    expect(onUpdated).toHaveBeenCalledOnce(); expect(screen.getByRole("button", { name: "儲存偏好" })).not.toBeDisabled();
  });

  it("keeps unsaved inputs and shows API conflicts locally so a retry uses a new version", async () => {
    vi.mocked(api).mockRejectedValueOnce(new Error("旅程已更新，請重新整理"));
    const { prepare, onUpdated } = mount();
    fireEvent.change(screen.getByLabelText("整趟總預算（台幣）"), { target: { value: "65000" } });
    save();
    expect(await screen.findByRole("alert")).toHaveTextContent("旅程已更新，請重新整理");
    expect(screen.getByLabelText("整趟總預算（台幣）")).toHaveValue(65000);
    expect(onUpdated).not.toHaveBeenCalled();
    prepare.mockResolvedValue({ ...makeTrip(), version: 12 });
    vi.mocked(api).mockResolvedValue({ ...makeTrip(), version: 13 });
    save();
    await waitFor(() => expect(onUpdated).toHaveBeenCalledOnce());
    expect(JSON.parse(vi.mocked(api).mock.calls[1][1]?.body as string).version).toBe(12);
  });

  it("does not PATCH when preparation cannot produce a current trip", async () => {
    const prepare = vi.fn<() => Promise<Trip | undefined>>().mockResolvedValue(undefined);
    mount(makeTrip(), prepare);
    fireEvent.click(screen.getByRole("button", { name: "充實" })); save();
    await waitFor(() => expect(screen.getByRole("button", { name: "儲存偏好" })).not.toBeDisabled());
    expect(prepare).toHaveBeenCalledOnce(); expect(api).not.toHaveBeenCalled();
  });
});
