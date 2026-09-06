import { fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { NewTripForm } from "./new-trip-form";

const { push } = vi.hoisted(() => ({ push: vi.fn() }));
vi.mock("@/i18n/navigation", () => ({ useRouter: () => ({ push }) }));
vi.mock("./place-picker", () => ({
  PlacePicker: ({ value, onTextChange }: { value: string; onTextChange: (value: string) => void }) => <input aria-label="目的地" value={value} onChange={(event) => onTextChange(event.target.value)} />,
}));

/**
 * The calendar asks the API for public holidays when it mounts, so a bare fetch stub would
 * hand those requests the response meant for the trip submission. This answers them
 * separately and leaves `mock` seeing only the calls the test is about.
 */
function stubFetch(mock: unknown, holidayUrls: string[] = []) {
  const submit = mock as (input: unknown, init?: RequestInit) => unknown;
  const empty = { country: "TW", country_name: "臺灣", locale: "zh-TW", coverage_start: null, coverage_end: null, attribution: "", holidays: [] };
  vi.stubGlobal("fetch", vi.fn((input: unknown, init?: RequestInit) => {
    if (String(input).includes("/holidays")) {
      holidayUrls.push(String(input));
      return Promise.resolve(new Response(JSON.stringify(empty), { status: 200, headers: { "Content-Type": "application/json" } }));
    }
    return submit(input, init);
  }));
}

function dayButton(iso: string) {
  return document.querySelector<HTMLButtonElement>(`[data-date="${iso}"]`);
}

// Walks the calendar forward until the day is on screen, then taps it.
function pickDay(iso: string) {
  for (let attempt = 0; attempt < 24 && !dayButton(iso); attempt += 1) fireEvent.click(screen.getByRole("button", { name: "下個月" }));
  const button = dayButton(iso);
  if (!button) throw new Error(`day ${iso} is not reachable`);
  fireEvent.click(button);
}

function fillRequiredFields() {
  fireEvent.change(screen.getByLabelText("旅程名稱"), { target: { value: " 東京五日賞楓 " } });
  fireEvent.change(screen.getByLabelText("目的地"), { target: { value: " 東京 " } });
  pickDay("2026-11-10");
  pickDay("2026-11-15");
}

function next() {
  fireEvent.click(screen.getByRole("button", { name: /下一步/ }));
}

function reachReview() {
  next(); next(); next();
}

describe("NewTripForm", () => {
  beforeEach(() => {
    push.mockReset();
    // The calendar only offers days from today on; pin the clock so the
    // November 2026 fixtures stay reachable and the assertions stay exact.
    vi.setSystemTime(new Date("2026-09-05T12:00:00"));
  });
  afterEach(() => {
    vi.useRealTimers();
    vi.unstubAllGlobals();
    window.sessionStorage.clear();
  });

  it("selects the trip dates as a continuous range on one calendar", () => {
    render(<NewTripForm />);
    expect(screen.queryByLabelText("開始日期")).toBeNull();
    const dates = within(screen.getByRole("group", { name: "旅行日期" }));
    expect(dates.getByRole("status").textContent).toBe("請先點選開始日期。");
    pickDay("2026-11-10");
    expect(dates.getByRole("status").textContent).toContain("再點選結束日期");
    pickDay("2026-11-15");
    expect(dates.getByRole("status").textContent).toMatch(/2026年11月10日.*→.*2026年11月15日.*共 6 天/);
    expect(dayButton("2026-11-12")?.getAttribute("aria-pressed")).toBe("true");
    expect(screen.getByText("6 天")).toBeTruthy();
    fireEvent.change(screen.getByLabelText("旅程名稱"), { target: { value: "東京賞楓" } });
    fireEvent.change(screen.getByLabelText("目的地"), { target: { value: "東京" } });
    next();
    expect(screen.queryByRole("alert")).toBeNull();
  });

  it("drops a stale draft's past dates, ignores unknown values and returns to the first step", async () => {
    window.sessionStorage.setItem("mokaair-new-trip-draft", JSON.stringify({
      step: 3, lodgingMode: "hotel", planningMode: "manual_blank", selectedInterests: ["food", "bogus"],
      form: { name: "回到過去", destination_name: "東京", start_date: "2020-01-01", end_date: "2020-01-06", pace: "turbo", route_preference: "TELEPORT" },
    }));
    render(<NewTripForm />);
    await waitFor(() => expect((screen.getByLabelText("旅程名稱") as HTMLInputElement).value).toBe("回到過去"));
    expect(document.querySelector('[data-date][aria-pressed="true"]')).toBeNull();
    expect(within(screen.getByRole("group", { name: "旅行日期" })).getByRole("status").textContent).toBe("請先點選開始日期。");
    const steps = within(screen.getByRole("list", { name: "建立步驟" })).getAllByRole("listitem");
    expect(steps[0].getAttribute("aria-current")).toBe("step");
    expect(steps[3].getAttribute("aria-current")).toBeNull();
    expect(screen.getByRole("button", { name: "適中" }).getAttribute("aria-pressed")).toBe("true");
    expect((screen.getByLabelText("大眾運輸偏好") as HTMLSelectElement).value).toBe("FEWER_TRANSFERS");
    expect(screen.getByRole("button", { name: "只住飯店" }).getAttribute("aria-pressed")).toBe("true");
    expect(screen.getByRole("button", { name: "美食" }).getAttribute("aria-pressed")).toBe("true");
    next();
    expect(screen.getByRole("alert").textContent).toContain("請選擇開始與結束日期");
  });

  it("re-focuses the alert when the same error repeats", () => {
    render(<NewTripForm />);
    next();
    const alert = screen.getByRole("alert");
    expect(document.activeElement).toBe(alert);
    alert.blur();
    expect(document.activeElement).not.toBe(alert);
    next();
    expect(document.activeElement).toBe(screen.getByRole("alert"));
  });

  it("clears the validation error as soon as the user edits a field", () => {
    render(<NewTripForm />);
    next();
    expect(screen.getByRole("alert")).toBeTruthy();
    fireEvent.change(screen.getByLabelText("旅程名稱"), { target: { value: "東京散步" } });
    expect(screen.queryByRole("alert")).toBeNull();
  });

  it("autosaves the draft and restores it after a reload", async () => {
    const first = render(<NewTripForm />);
    fireEvent.change(screen.getByLabelText("旅程名稱"), { target: { value: "草稿旅程" } });
    fireEvent.click(screen.getByRole("button", { name: "美食" }));
    await waitFor(() => expect(window.sessionStorage.getItem("mokaair-new-trip-draft")).toContain("草稿旅程"));
    first.unmount();

    render(<NewTripForm />);
    await waitFor(() => expect((screen.getByLabelText("旅程名稱") as HTMLInputElement).value).toBe("草稿旅程"));
    expect(screen.getByRole("button", { name: "美食" }).getAttribute("aria-pressed")).toBe("true");
  });

  it("submits structured travelers, lodging, interests and routing preferences", async () => {
    const fetchMock = vi.fn().mockResolvedValue(new Response(JSON.stringify({ id: "trip-1" }), { status: 201, headers: { "Content-Type": "application/json" } }));
    stubFetch(fetchMock);
    render(<NewTripForm />);
    fillRequiredFields();
    next();
    fireEvent.change(screen.getByLabelText("成人"), { target: { value: "3" } });
    fireEvent.change(screen.getByLabelText("兒童"), { target: { value: "1" } });
    fireEvent.change(screen.getByLabelText("整趟總預算（台幣）"), { target: { value: "90000.4" } });
    fireEvent.click(screen.getByRole("button", { name: "悠閒" }));
    fireEvent.click(screen.getByRole("button", { name: "美食" }));
    next();
    fireEvent.click(screen.getByRole("button", { name: "兩種都接受" }));
    fireEvent.change(screen.getByLabelText("每晚最低（台幣）"), { target: { value: "3000" } });
    fireEvent.change(screen.getByLabelText("每晚最高（台幣）"), { target: { value: "7000" } });
    fireEvent.change(screen.getByLabelText("最低星級"), { target: { value: "4" } });
    fireEvent.change(screen.getByLabelText("最低住客評分"), { target: { value: "8" } });
    fireEvent.change(screen.getByLabelText("最低評論數"), { target: { value: "100" } });
    next();
    fireEvent.change(screen.getByLabelText("大眾運輸偏好"), { target: { value: "LESS_WALKING" } });
    fireEvent.change(screen.getByLabelText("其他補充"), { target: { value: " 不要一直換飯店 " } });
    const review = within(screen.getByRole("region", { name: "完整行程條件" }));
    expect(review.getByText(/2026年11月10日.*→.*2026年11月15日/)).toBeTruthy();
    expect(review.getByText("每晚住宿預算")).toBeTruthy();
    expect(review.getByText("NT$3,000～NT$7,000")).toBeTruthy();
    expect(review.getByText("4 星以上")).toBeTruthy();
    expect(review.getByText("8.0+")).toBeTruthy();
    expect(review.getByText("100 則以上")).toBeTruthy();
    expect(review.getByText("少走路")).toBeTruthy();
    expect(screen.getByText(/不會傳送 Email、姓名或帳號識別資料/)).toBeTruthy();
    fireEvent.click(screen.getByRole("button", { name: /交給 AI 排好行程/ }));

    await waitFor(() => expect(push).toHaveBeenCalledWith("/trips/trip-1"));
    expect(window.sessionStorage.getItem("mokaair-new-trip-draft")).toBeNull();
    const headers = (fetchMock.mock.calls[0][1] as RequestInit).headers as Record<string, string>;
    expect(headers["Idempotency-Key"]).toMatch(/^[0-9a-f-]{36}$/);
    const request = JSON.parse(String((fetchMock.mock.calls[0][1] as RequestInit).body));
    expect(request).toMatchObject({
      source: "blank", planning_mode: "ai_draft", name: "東京五日賞楓", destination_name: "東京", destination_place_id: null,
      start_date: "2026-11-10", end_date: "2026-11-15", route_preference: "LESS_WALKING",
      routing: { auto_compute: true, default_travel_mode: "transit", default_buffer_minutes: 10 },
      travelers: { adults: 3, children: 1, rooms: 1 },
      preferences: {
        budget_twd: 90000, pace: "relaxed", accepted_property_types: ["hotel", "vacation_rental"],
        hotel_min_nightly_twd: 3000, hotel_max_nightly_twd: 7000, hotel_min_rating: 4,
        hotel_min_review_score: 8, hotel_min_review_count: 100, interests: ["food"],
      },
      notes: "不要一直換飯店",
    });
  });

  it("reuses the same idempotency key when the user retries after a failure", async () => {
    const fetchMock = vi.fn()
      .mockRejectedValueOnce(new Error("API 服務回應逾時"))
      .mockResolvedValueOnce(new Response(JSON.stringify({ id: "trip-2" }), { status: 201, headers: { "Content-Type": "application/json" } }));
    stubFetch(fetchMock);
    render(<NewTripForm />);
    fillRequiredFields();
    reachReview();

    fireEvent.click(screen.getByRole("button", { name: /交給 AI 排好行程/ }));
    await waitFor(() => expect(screen.getByRole("alert").textContent).toContain("逾時"));
    fireEvent.click(screen.getByRole("button", { name: /交給 AI 排好行程/ }));
    await waitFor(() => expect(push).toHaveBeenCalledWith("/trips/trip-2"));

    const keys = fetchMock.mock.calls.map((call) => ((call[1] as RequestInit).headers as Record<string, string>)["Idempotency-Key"]);
    expect(keys).toHaveLength(2);
    expect(keys[0]).toBe(keys[1]);
  });

  it("creates a blank manual timeline without automatic route computation", async () => {
    const fetchMock = vi.fn().mockResolvedValue(new Response(JSON.stringify({ id: "manual-trip" }), { status: 201, headers: { "Content-Type": "application/json" } }));
    stubFetch(fetchMock);
    render(<NewTripForm />);
    fillRequiredFields();
    reachReview();

    fireEvent.click(screen.getByRole("button", { name: /空白手動規劃/ }));
    expect(screen.getByText(/空白手動規劃不會呼叫 AI/)).toBeTruthy();
    expect(screen.queryByText(/傳給後台選定的 AI 供應商/)).toBeNull();
    fireEvent.click(screen.getByRole("button", { name: "建立空白手動行程" }));

    await waitFor(() => expect(push).toHaveBeenCalledWith("/trips/manual-trip"));
    const request = JSON.parse(String((fetchMock.mock.calls[0][1] as RequestInit).body));
    expect(request).toMatchObject({
      source: "blank",
      planning_mode: "manual_blank",
      routing: { auto_compute: false, default_travel_mode: "transit", default_buffer_minutes: 10 },
    });
  });

  it("does not submit while moving from lodging preferences to review", () => {
    const fetchMock = vi.fn();
    stubFetch(fetchMock);
    render(<NewTripForm />);
    fillRequiredFields();
    next();
    next();

    const defaultActionAllowed = fireEvent.click(screen.getByRole("button", { name: "下一步" }));

    expect(defaultActionAllowed).toBe(false);
    expect(screen.getByRole("heading", { name: "路線偏好與建立前確認" })).toBeTruthy();
    expect(screen.getByRole("button", { name: /空白手動規劃/ })).toBeTruthy();
    expect(fetchMock).not.toHaveBeenCalled();
  });

  it("blocks an inverted nightly price range before review", () => {
    render(<NewTripForm />);
    fillRequiredFields();
    next(); next();
    fireEvent.change(screen.getByLabelText("每晚最低（台幣）"), { target: { value: "8000" } });
    fireEvent.change(screen.getByLabelText("每晚最高（台幣）"), { target: { value: "3000" } });
    next();
    expect(screen.getByRole("alert").textContent).toContain("最低價格不可高於最高價格");
  });

  it("shows a readable API validation message", async () => {
    stubFetch(vi.fn().mockResolvedValue(new Response(JSON.stringify({ detail: [{ type: "missing", loc: ["body", "plan_id"], msg: "Field required" }] }), { status: 422, headers: { "Content-Type": "application/json" } })));
    render(<NewTripForm />);
    fillRequiredFields();
    reachReview();
    fireEvent.click(screen.getByRole("button", { name: /交給 AI 排好行程/ }));
    const alert = await screen.findByRole("alert");
    expect(alert.textContent).toContain("行程方案：必填");
    expect(alert.textContent).not.toContain("[object Object]");
  });
  it("marks the destination's holidays and the traveller's own, not every market", async () => {
    const holidayUrls: string[] = [];
    stubFetch(vi.fn(), holidayUrls);
    render(<NewTripForm />);
    await waitFor(() => expect(holidayUrls.length).toBe(3));

    holidayUrls.length = 0;
    fireEvent.change(screen.getByLabelText("目的地"), { target: { value: "日本東京" } });
    await waitFor(() => expect(holidayUrls.length).toBe(2));
    const asked = holidayUrls.map((url) => new URL(url, "https://travel.test").searchParams.get("country"));
    expect(asked.sort()).toEqual(["JP", "TW"]);
  });

  it("asks which shops only after 購物 is chosen, and sends them", async () => {
    const fetchMock = vi.fn().mockResolvedValue(new Response(JSON.stringify({ id: "trip-2" }), { status: 201, headers: { "Content-Type": "application/json" } }));
    stubFetch(fetchMock);
    render(<NewTripForm />);
    fillRequiredFields();
    next();

    // The shop types mean nothing on their own, so they stay out of the way.
    expect(screen.queryByRole("group", { name: "想逛哪些店？（可複選）" })).toBeNull();
    fireEvent.click(screen.getByRole("button", { name: "購物" }));
    const shops = screen.getByRole("group", { name: "想逛哪些店？（可複選）" });
    fireEvent.click(within(shops).getByRole("button", { name: "藥妝" }));
    fireEvent.click(within(shops).getByRole("button", { name: "電器／3C" }));
    expect(within(shops).getByRole("button", { name: "藥妝" }).getAttribute("aria-pressed")).toBe("true");

    next();
    next();
    fireEvent.click(screen.getByRole("button", { name: /交給 AI 排好行程/ }));

    await waitFor(() => expect(push).toHaveBeenCalledWith("/trips/trip-2"));
    const request = JSON.parse(String((fetchMock.mock.calls[0][1] as RequestInit).body));
    expect(request.preferences.interests).toContain("shopping");
    expect(request.preferences.shop_themes).toEqual(["drugstore", "electronics"]);
  });

  it("forgets the shop types when 購物 is switched off", async () => {
    const fetchMock = vi.fn().mockResolvedValue(new Response(JSON.stringify({ id: "trip-3" }), { status: 201, headers: { "Content-Type": "application/json" } }));
    stubFetch(fetchMock);
    render(<NewTripForm />);
    fillRequiredFields();
    next();

    fireEvent.click(screen.getByRole("button", { name: "購物" }));
    fireEvent.click(within(screen.getByRole("group", { name: "想逛哪些店？（可複選）" })).getByRole("button", { name: "藥妝" }));
    // Turning the interest off hides the chips; a hidden chip that stayed selected
    // would quietly steer the itinerary.
    fireEvent.click(screen.getByRole("button", { name: "購物" }));
    expect(screen.queryByRole("group", { name: "想逛哪些店？（可複選）" })).toBeNull();

    next();
    next();
    fireEvent.click(screen.getByRole("button", { name: /交給 AI 排好行程/ }));

    await waitFor(() => expect(push).toHaveBeenCalledWith("/trips/trip-3"));
    const request = JSON.parse(String((fetchMock.mock.calls[0][1] as RequestInit).body));
    expect(request.preferences.interests).not.toContain("shopping");
    expect(request.preferences.shop_themes).toEqual([]);
  });
});
