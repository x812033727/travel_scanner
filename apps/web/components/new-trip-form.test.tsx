import { fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import "@testing-library/jest-dom/vitest";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { NewTripForm } from "./new-trip-form";
import { automaticTripName, newTripCopy } from "./planner/new-trip-copy";
import { NewTripPreferenceFields, NewTripTravelerFields, type NewTripPreferenceValues } from "./planner/new-trip-fields";

const { push, identity } = vi.hoisted(() => ({ push: vi.fn(), identity: { id: "member-a", status: "authenticated" } }));
vi.mock("@/components/header-session", () => ({ useHeaderSession: () => ({ status: identity.status, user: { id: identity.id } }) }));
vi.mock("@/i18n/navigation", () => ({ useRouter: () => ({ push }) }));

/**
 * The calendar asks the API for public holidays when it mounts, so a bare fetch stub would
 * hand those requests the response meant for the trip submission. This answers them
 * separately and leaves `mock` seeing only the calls the test is about.
 */
function stubFetch(mock: unknown, holidayUrls: string[] = [], attribution = "") {
  const submit = mock as (input: unknown, init?: RequestInit) => unknown;
  const empty = { country: "TW", country_name: "臺灣", locale: "zh-TW", coverage_start: null, coverage_end: null, attribution, holidays: attribution ? [{ date: "2026-11-11", key: "example", kind: "public_holiday", is_working_day: false, name: "假日", country: "TW", country_name: "臺灣", source: "official" }] : [] };
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
  fireEvent.click(calendarToggle());
  pickDay("2026-11-10");
  pickDay("2026-11-15");
}

function calendarToggle() {
  return within(screen.getByRole("group", { name: "旅行日期" })).getByRole("button");
}
function openAdvanced() { fireEvent.click(screen.getByText("進階偏好（選填）")); }
function submit() { fireEvent.click(screen.getByRole("button", { name: /^(開始安排|重新確認原始建立)$/ })); }
async function renderReady() {
  const view = render(<NewTripForm />);
  await waitFor(() => expect(screen.getByRole("button", { name: /^(開始安排|重新確認原始建立)$/ })).not.toBeDisabled(), { timeout: 5000 });
  return view;
}

describe("NewTripForm", () => {
it("preserves existing nonstandard traveler values in the shared settings fields", async () => {
    render(<NewTripTravelerFields values={{ adults: "2", children: "8", rooms: "1" }} onChange={vi.fn()} />);
    expect(screen.getByLabelText("兒童")).toHaveValue("8");
  });

  it("preserves existing numeric preferences and can hide an unpersistable route preference", async () => {
    const values: NewTripPreferenceValues = {
      budget_twd: "", pace: "balanced", route_preference: "FEWER_TRANSFERS", nightly_min: "", nightly_max: "",
      hotel_min_rating: "2", preferred_area: "", max_station_walk_minutes: "17", min_review_score: "8.5",
      min_review_count: "75", breakfast_required: false, refundable_required: false, avoid_red_eye: true,
    };
    render(<NewTripPreferenceFields values={values} onChange={vi.fn()} lodgingMode="any" onLodgingModeChange={vi.fn()} interests={[]} onToggleInterest={vi.fn()} shopThemes={[]} onToggleShopTheme={vi.fn()} hideRoutePreference />);
    expect(screen.getByLabelText("最低星級")).toHaveValue("2");
    expect(screen.getByLabelText("車站步行上限")).toHaveValue("17");
    expect(screen.getByLabelText("最低住客評分")).toHaveValue("8.5");
    expect(screen.getByLabelText("最低評論數")).toHaveValue("75");
    expect(screen.queryByLabelText("大眾運輸偏好")).toBeNull();
  });
it("shows one page with editable default travelers and optional preferences collapsed", async () => {
    await renderReady();
    expect(screen.getByLabelText("成人")).toHaveValue("2");
    expect(screen.getByLabelText("兒童")).toHaveValue("0");
    expect(screen.getByLabelText("房間")).toHaveValue("1");
    expect(screen.getByText("進階偏好（選填）").closest("details")).not.toHaveAttribute("open");
    expect(screen.queryByRole("list", { name: "建立步驟" })).toBeNull();
    expect(screen.queryByRole("button", { name: /下一步|交給 AI|空白手動規劃/ })).toBeNull();
    expect(screen.getByText(/不會自動呼叫 AI 或計算路線/)).toBeVisible();
    expect(fetch).not.toHaveBeenCalled();
  });

  it("requires only city and dates, auto-names the trip and never calls AI, routes or geocoding", async () => {
    const fetchMock = vi.fn().mockResolvedValue(new Response(JSON.stringify({ id: "simple-trip" }), { status: 201 }));
    stubFetch(fetchMock);
    await renderReady();
    fireEvent.click(screen.getByRole("button", { name: "東京" }));
    fireEvent.click(calendarToggle());
    pickDay("2026-11-10");
    pickDay("2026-11-15");
    expect(screen.getByLabelText("旅程名稱")).toHaveValue("東京・6 天");
    expect(screen.getByLabelText("旅程名稱")).not.toBeRequired();
    submit();
    await waitFor(() => expect(push).toHaveBeenCalledWith("/trips/simple-trip"));
    expect(fetchMock).toHaveBeenCalledTimes(1);
    expect(String(fetchMock.mock.calls[0][0])).toMatch(/\/trips$/);
    expect(JSON.parse(String(fetchMock.mock.calls[0][1].body))).toMatchObject({
      name: "東京・6 天", source: "blank", planning_mode: "manual_blank", destination_place_id: null,
      travelers: { adults: 2, children: 0, rooms: 1 },
      routing: { auto_compute: false, default_travel_mode: "transit", default_buffer_minutes: 10 },
    });
  });

  it("preserves a custom name across city changes and can restore automatic naming", async () => {
    await renderReady();
    fillRequiredFields();
    fireEvent.click(document.querySelector(".calm-new-trip-name summary")!);
    fireEvent.change(screen.getByLabelText("旅程名稱"), { target: { value: "我的生日旅行" } });
    fireEvent.click(screen.getByRole("button", { name: "首爾" }));
    expect(screen.getByLabelText("旅程名稱")).toHaveValue("我的生日旅行");
    fireEvent.click(screen.getByRole("button", { name: "使用自動名稱" }));
    expect(screen.getByLabelText("旅程名稱")).toHaveValue("首爾・6 天");
    fireEvent.change(screen.getByLabelText("目的地"), { target: { value: "京都" } });
    expect(screen.getByLabelText("旅程名稱")).toHaveValue("京都・6 天");
  });

  it("blocks excess rooms and non-positive optional budget before submitting", async () => {
    const fetchMock = vi.fn();
    stubFetch(fetchMock);
    await renderReady();
    fillRequiredFields();
    fireEvent.change(screen.getByLabelText("房間"), { target: { value: "3" } });
    submit();
    expect(screen.getByRole("alert")).toHaveTextContent("房間數不可多於旅客人數");
    fireEvent.change(screen.getByLabelText("房間"), { target: { value: "1" } });
    openAdvanced();
    fireEvent.change(screen.getByLabelText("整趟總預算（台幣）"), { target: { value: "0" } });
    submit();
    expect(screen.getByRole("alert")).toHaveTextContent("總預算必須大於 0");
    expect(fetchMock).not.toHaveBeenCalled();
  });

  it("restores legacy AI draft data but always submits manual blank planning", async () => {
    window.sessionStorage.setItem("mokaair-new-trip-draft:member-a", JSON.stringify({
      step: 3, planningMode: "ai_draft", lodgingMode: "any", selectedInterests: [],
      form: { name: "已存旅程", destination_name: "東京", destination_place_id: "existing-verified-place", start_date: "2026-11-10", end_date: "2026-11-15" },
    }));
    const fetchMock = vi.fn().mockResolvedValue(new Response(JSON.stringify({ id: "restored-trip" }), { status: 201 }));
    stubFetch(fetchMock);
    await renderReady();
    await waitFor(() => expect(screen.getByLabelText("旅程名稱")).toHaveValue("已存旅程"));
    submit();
    await waitFor(() => expect(push).toHaveBeenCalledWith("/trips/restored-trip"));
    expect(JSON.parse(String(fetchMock.mock.calls[0][1].body))).toMatchObject({
      name: "已存旅程", planning_mode: "manual_blank", destination_place_id: "existing-verified-place", routing: { auto_compute: false },
    });
  });

  it("keeps the draft after authentication failure and does not navigate", async () => {
    stubFetch(vi.fn().mockResolvedValue(new Response(JSON.stringify({ detail: "請先登入" }), { status: 401 })));
    await renderReady();
    fillRequiredFields();
    await waitFor(() => expect(window.sessionStorage.getItem("mokaair-new-trip-draft:member-a")).toContain("東京"));
    submit();
    expect(await screen.findByRole("alert")).toHaveTextContent("請先登入");
    expect(window.sessionStorage.getItem("mokaair-new-trip-draft:member-a")).toContain("2026-11-10");
    expect(push).not.toHaveBeenCalled();
  });

  it("sends only one request when duplicate submits occur while the first is pending", async () => {
    let resolveRequest: (value: Response) => void = () => {};
    const fetchMock = vi.fn(() => new Promise<Response>((resolve) => { resolveRequest = resolve; }));
    stubFetch(fetchMock);
    const { container } = await renderReady();
    fillRequiredFields();
    fireEvent.submit(container.querySelector("form")!);
    fireEvent.submit(container.querySelector("form")!);
    expect(fetchMock).toHaveBeenCalledTimes(1);
    expect(screen.getByRole("button", { name: "正在建立…" })).toBeDisabled();
    expect(screen.getByLabelText("目的地")).toBeDisabled();
    resolveRequest(new Response(JSON.stringify({ id: "single-trip" }), { status: 201 }));
    await waitFor(() => expect(push).toHaveBeenCalledWith("/trips/single-trip"));
  });

  it.each([
    ["zh-TW", "東京", "東京・6 天", "開始安排"],
    ["zh-CN", "东京", "东京・6 天", "开始安排"],
    ["en", "Tokyo", "Tokyo · 6-day trip", "Start planning"],
    ["ja", "東京", "東京・6日間", "旅の計画をはじめる"],
    ["ko", "도쿄", "도쿄 6일 여행", "일정 시작하기"],
  ])("provides localized automatic names and submit copy for %s", (locale, city, name, cta) => {
    expect(automaticTripName(locale, city, 6)).toBe(name);
    expect(automaticTripName(locale, "", 0)).toBe("");
    expect(newTripCopy(locale).submit).toBe(cta);
  });
  beforeEach(() => {
    push.mockReset();
    identity.id = "member-a";
    identity.status = "authenticated";
    stubFetch(vi.fn());
    // The calendar only offers days from today on; pin the clock so the
    // November 2026 fixtures stay reachable and the assertions stay exact.
    vi.setSystemTime(new Date("2026-09-05T12:00:00"));
  });
  afterEach(() => {
    vi.useRealTimers();
    vi.unstubAllGlobals();
    window.sessionStorage.clear();
  });

  it("toggles a continuous date range calendar without losing selected dates or holiday attribution", async () => {
    stubFetch(vi.fn(), [], "官方假日資料來源");
    await renderReady();
    expect(screen.queryByRole("grid")).toBeNull();
    expect(calendarToggle()).toHaveAttribute("aria-expanded", "false");
    fireEvent.click(calendarToggle());
    expect(screen.getByRole("status")).toHaveTextContent("請先點選開始日期。");
    pickDay("2026-11-10");
    expect(screen.getByRole("status")).toHaveTextContent("再點選結束日期");
    pickDay("2026-11-15");
    expect(screen.queryByRole("grid")).toBeNull();
    expect(calendarToggle()).toHaveFocus();
    expect(calendarToggle()).toHaveTextContent("6 天");
    fireEvent.click(calendarToggle());
    expect(dayButton("2026-11-12")).toHaveAttribute("aria-pressed", "true");
    expect(await screen.findByText(/官方假日資料來源/)).toBeVisible();
  });

  it("drops stale draft dates and unknown values without restoring the old wizard", async () => {
    window.sessionStorage.setItem("mokaair-new-trip-draft:member-a", JSON.stringify({
      step: 3, lodgingMode: "hotel", planningMode: "manual_blank", selectedInterests: ["food", "bogus"],
      form: { name: "回到過去", destination_name: "東京", start_date: "2020-01-01", end_date: "2020-01-06", pace: "turbo", route_preference: "TELEPORT" },
    }));
    await renderReady();
    await waitFor(() => expect((screen.getByLabelText("旅程名稱") as HTMLInputElement).value).toBe("回到過去"));
    expect(document.querySelector('[data-date][aria-pressed="true"]')).toBeNull();
    expect(calendarToggle()).toHaveTextContent("選擇旅行日期");
    expect(screen.queryByRole("list", { name: "建立步驟" })).toBeNull();
    openAdvanced();
    expect(screen.getByRole("button", { name: "適中" }).getAttribute("aria-pressed")).toBe("true");
    expect((screen.getByLabelText("大眾運輸偏好") as HTMLSelectElement).value).toBe("FEWER_TRANSFERS");
    expect(screen.getByRole("button", { name: "只住飯店" }).getAttribute("aria-pressed")).toBe("true");
    expect(screen.getByRole("button", { name: "美食" }).getAttribute("aria-pressed")).toBe("true");
    submit();
    expect(screen.getByRole("alert").textContent).toContain("請選擇開始與結束日期");
  });

  it("re-focuses the alert when the same error repeats", async () => {
    await renderReady();
    submit();
    const alert = screen.getByRole("alert");
    expect(document.activeElement).toBe(alert);
    alert.blur();
    expect(document.activeElement).not.toBe(alert);
    submit();
    expect(document.activeElement).toBe(screen.getByRole("alert"));
  });

  it("clears the validation error as soon as the user edits a field", async () => {
    await renderReady();
    submit();
    expect(screen.getByRole("alert")).toBeTruthy();
    fireEvent.change(screen.getByLabelText("旅程名稱"), { target: { value: "東京散步" } });
    expect(screen.queryByRole("alert")).toBeNull();
  });

  it("autosaves the draft and restores it after a reload", async () => {
    const first = await renderReady();
    fireEvent.change(screen.getByLabelText("旅程名稱"), { target: { value: "草稿旅程" } });
    openAdvanced();
    fireEvent.click(screen.getByRole("button", { name: "美食" }));
    await waitFor(() => expect(window.sessionStorage.getItem("mokaair-new-trip-draft:member-a")).toContain("草稿旅程"));
    first.unmount();

    await renderReady();
    await waitFor(() => expect((screen.getByLabelText("旅程名稱") as HTMLInputElement).value).toBe("草稿旅程"));
    openAdvanced();
    expect(screen.getByRole("button", { name: "美食" }).getAttribute("aria-pressed")).toBe("true");
  });

  it("submits structured travelers, lodging, interests and routing preferences", async () => {
    const fetchMock = vi.fn().mockResolvedValue(new Response(JSON.stringify({ id: "trip-1" }), { status: 201, headers: { "Content-Type": "application/json" } }));
    stubFetch(fetchMock);
    await renderReady();
    fillRequiredFields();
    openAdvanced();
    fireEvent.change(screen.getByLabelText("成人"), { target: { value: "3" } });
    fireEvent.change(screen.getByLabelText("兒童"), { target: { value: "1" } });
    fireEvent.change(screen.getByLabelText("整趟總預算（台幣）"), { target: { value: "90000.4" } });
    fireEvent.click(screen.getByRole("button", { name: "悠閒" }));
    fireEvent.click(screen.getByRole("button", { name: "美食" }));
    fireEvent.click(screen.getByRole("button", { name: "兩種都接受" }));
    fireEvent.change(screen.getByLabelText("每晚最低（台幣）"), { target: { value: "3000" } });
    fireEvent.change(screen.getByLabelText("每晚最高（台幣）"), { target: { value: "7000" } });
    fireEvent.change(screen.getByLabelText("最低星級"), { target: { value: "4" } });
    fireEvent.change(screen.getByLabelText("最低住客評分"), { target: { value: "8" } });
    fireEvent.change(screen.getByLabelText("最低評論數"), { target: { value: "100" } });
    fireEvent.change(screen.getByLabelText("大眾運輸偏好"), { target: { value: "LESS_WALKING" } });
    fireEvent.change(screen.getByLabelText("其他補充"), { target: { value: " 不要一直換飯店 " } });
    submit();

    await waitFor(() => expect(push).toHaveBeenCalledWith("/trips/trip-1"));
    expect(window.sessionStorage.getItem("mokaair-new-trip-draft:member-a")).toBeNull();
    const headers = (fetchMock.mock.calls[0][1] as RequestInit).headers as Record<string, string>;
    expect(headers["Idempotency-Key"]).toMatch(/^[0-9a-f-]{36}$/);
    const request = JSON.parse(String((fetchMock.mock.calls[0][1] as RequestInit).body));
    expect(request).toMatchObject({
      source: "blank", planning_mode: "manual_blank", name: "東京五日賞楓", destination_name: "東京", destination_place_id: null,
      start_date: "2026-11-10", end_date: "2026-11-15", route_preference: "LESS_WALKING",
      routing: { auto_compute: false, default_travel_mode: "transit", default_buffer_minutes: 10 },
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
    await renderReady();
    fillRequiredFields();


    submit();
    await waitFor(() => expect(screen.getByRole("alert").textContent).toContain("逾時"));
    submit();
    await waitFor(() => expect(push).toHaveBeenCalledWith("/trips/trip-2"));

    const keys = fetchMock.mock.calls.map((call) => ((call[1] as RequestInit).headers as Record<string, string>)["Idempotency-Key"]);
    expect(keys).toHaveLength(2);
    expect(keys[0]).toBe(keys[1]);
    expect(fetchMock.mock.calls[0][1].body).toBe(fetchMock.mock.calls[1][1].body);
  });

  it("recovers an uncertain request after refresh without automatic submission or edited bytes", async () => {
    const fetchMock = vi.fn().mockRejectedValueOnce(new Error("connection lost"))
      .mockResolvedValueOnce(new Response(JSON.stringify({ id: "recovered" }), { status: 201 }));
    stubFetch(fetchMock);
    const first = await renderReady();
    fillRequiredFields();
    submit();
    await screen.findByText("connection lost");
    const snapshot = JSON.parse(window.sessionStorage.getItem("mokaair-new-trip-draft:member-a")!);
    expect(snapshot.pending.body).toBe(fetchMock.mock.calls[0][1].body);
    first.unmount();
    await renderReady();
    expect(screen.getByLabelText("目的地")).toBeDisabled();
    expect(screen.getByRole("region", { name: "確認上次建立結果" })).toBeVisible();
    expect(fetchMock).toHaveBeenCalledTimes(1);
    submit();
    await waitFor(() => expect(push).toHaveBeenCalledWith("/trips/recovered"));
    expect(fetchMock.mock.calls[1][1].body).toBe(fetchMock.mock.calls[0][1].body);
    expect(fetchMock.mock.calls[1][1].headers["Idempotency-Key"]).toBe(snapshot.pending.key);
  });

  it("does not retire an uncertain request just because its later retry loses authentication", async () => {
    const fetchMock = vi.fn().mockRejectedValueOnce(new Error("connection lost"))
      .mockResolvedValueOnce(new Response(JSON.stringify({ detail: "請先登入" }), { status: 401 }))
      .mockResolvedValueOnce(new Response(JSON.stringify({ id: "original" }), { status: 201 }));
    stubFetch(fetchMock);
    await renderReady();
    fillRequiredFields();
    submit();
    await screen.findByText("connection lost");
    submit();
    await screen.findByText("請先登入");
    expect(screen.getByLabelText("目的地")).toBeDisabled();
    expect(JSON.parse(window.sessionStorage.getItem("mokaair-new-trip-draft:member-a")!).pending).toBeTruthy();
    submit();
    await waitFor(() => expect(push).toHaveBeenCalledWith("/trips/original"));
    expect(new Set(fetchMock.mock.calls.map((call) => call[1].headers["Idempotency-Key"])).size).toBe(1);
  });

  it("blocks expired requests and links to My trips without generating another key", async () => {
    const fetchMock = vi.fn().mockRejectedValueOnce(new Error("connection lost"));
    stubFetch(fetchMock);
    const first = await renderReady();
    fillRequiredFields();
    submit();
    await screen.findByText("connection lost");
    const before = window.sessionStorage.getItem("mokaair-new-trip-draft:member-a");
    first.unmount();
    vi.setSystemTime(new Date("2026-09-06T12:00:01"));
    const next = render(<NewTripForm />);
    await screen.findByText(/已超過安全重試期限/);
    expect(screen.getByRole("button", { name: "重新確認原始建立" })).toBeDisabled();
    expect(screen.getByRole("link", { name: "查看我的旅程" })).toHaveAttribute("href", "/zh-TW/trips");
    fireEvent.submit(next.container.querySelector("form")!);
    expect(fetchMock).toHaveBeenCalledTimes(1);
    expect(window.sessionStorage.getItem("mokaair-new-trip-draft:member-a")).toBe(before);
  });

  it("isolates accounts and ignores responses delivered after the account changes", async () => {
    let resolveRequest: (response: Response) => void = () => {};
    const fetchMock = vi.fn(() => new Promise<Response>((resolve) => { resolveRequest = resolve; }));
    stubFetch(fetchMock);
    const view = await renderReady();
    fillRequiredFields();
    submit();
    identity.id = "member-b";
    view.rerender(<NewTripForm />);
    await waitFor(() => expect(screen.getByRole("button", { name: "開始安排" })).not.toBeDisabled());
    expect(screen.getByLabelText("目的地")).toHaveValue("");
    expect(screen.queryByRole("region", { name: "確認上次建立結果" })).toBeNull();
    resolveRequest(new Response(JSON.stringify({ id: "member-a-private-trip" }), { status: 201 }));
    await waitFor(() => expect(window.sessionStorage.getItem("mokaair-new-trip-draft:member-b")).toBeTruthy());
    expect(push).not.toHaveBeenCalled();
    expect(window.sessionStorage.getItem("mokaair-new-trip-draft:member-a")).toContain("pending");
  });

  it("refuses to POST if the immutable recovery record cannot be persisted", async () => {
    const fetchMock = vi.fn();
    stubFetch(fetchMock);
    await renderReady();
    fillRequiredFields();
    const storage = vi.spyOn(Storage.prototype, "setItem").mockImplementation(() => { throw new Error("quota"); });
    submit();
    await screen.findByText(/無法保存建立紀錄，尚未送出/);
    expect(fetchMock).not.toHaveBeenCalled();
    storage.mockRestore();
  });

  it("does not adopt a legacy draft without an account identity", async () => {
    window.sessionStorage.setItem("mokaair-new-trip-draft", JSON.stringify({ form: { destination_name: "Other member's city" } }));
    await renderReady();
    expect(screen.getByLabelText("目的地")).toHaveValue("");
  });

  it("places date errors next to the date summary and clears them on selection", async () => {
    await renderReady();
    fireEvent.click(screen.getByRole("button", { name: "東京" }));
    submit();
    expect(calendarToggle()).toHaveAttribute("aria-invalid", "true");
    expect(screen.getByRole("alert").closest("fieldset")).toContainElement(calendarToggle());
    fireEvent.click(calendarToggle());
    pickDay("2026-11-10");
    pickDay("2026-11-15");
    expect(screen.queryByRole("alert")).toBeNull();
    expect(calendarToggle()).toHaveFocus();
  });

  it("creates a blank manual timeline without automatic route computation", async () => {
    const fetchMock = vi.fn().mockResolvedValue(new Response(JSON.stringify({ id: "manual-trip" }), { status: 201, headers: { "Content-Type": "application/json" } }));
    stubFetch(fetchMock);
    await renderReady();
    fillRequiredFields();


    expect(screen.getByText(/不會自動呼叫 AI 或計算路線/)).toBeTruthy();
    expect(screen.queryByText(/傳給後台選定的 AI 供應商/)).toBeNull();
    submit();

    await waitFor(() => expect(push).toHaveBeenCalledWith("/trips/manual-trip"));
    const request = JSON.parse(String((fetchMock.mock.calls[0][1] as RequestInit).body));
    expect(request).toMatchObject({
      source: "blank",
      planning_mode: "manual_blank",
      routing: { auto_compute: false, default_travel_mode: "transit", default_buffer_minutes: 10 },
    });
  });

  it("does not submit when choosing a city, dates or optional preferences", async () => {
    const fetchMock = vi.fn();
    stubFetch(fetchMock);
    await renderReady();
    fillRequiredFields();
    fireEvent.click(screen.getByRole("button", { name: "首爾" }));
    openAdvanced();
    fireEvent.click(screen.getByRole("button", { name: "只住飯店" }));
    expect(fetchMock).not.toHaveBeenCalled();
  });

  it("blocks an inverted nightly price range before submitting", async () => {
    await renderReady();
    fillRequiredFields();
    openAdvanced();
    fireEvent.change(screen.getByLabelText("每晚最低（台幣）"), { target: { value: "8000" } });
    fireEvent.change(screen.getByLabelText("每晚最高（台幣）"), { target: { value: "3000" } });
    submit();
    expect(screen.getByRole("alert").textContent).toContain("最低價格不可高於最高價格");
  });

  it("shows a readable API validation message", async () => {
    stubFetch(vi.fn().mockResolvedValue(new Response(JSON.stringify({ detail: [{ type: "missing", loc: ["body", "plan_id"], msg: "Field required" }] }), { status: 422, headers: { "Content-Type": "application/json" } })));
    await renderReady();
    fillRequiredFields();

    submit();
    const alert = await screen.findByRole("alert");
    expect(alert.textContent).toContain("行程方案：必填");
    expect(alert.textContent).not.toContain("[object Object]");
  });
  it("marks the destination's holidays and the traveller's own, not every market", async () => {
    const holidayUrls: string[] = [];
    stubFetch(vi.fn(), holidayUrls);
    await renderReady();
    expect(holidayUrls).toEqual([]);
    fireEvent.change(screen.getByLabelText("目的地"), { target: { value: "日本東京" } });
    fireEvent.click(calendarToggle());
    await waitFor(() => expect(holidayUrls.length).toBe(2));
    const asked = holidayUrls.map((url) => new URL(url, "https://travel.test").searchParams.get("country"));
    expect(asked.sort()).toEqual(["JP", "TW"]);
  });

  it("asks which shops only after 購物 is chosen, and sends them", async () => {
    const fetchMock = vi.fn().mockResolvedValue(new Response(JSON.stringify({ id: "trip-2" }), { status: 201, headers: { "Content-Type": "application/json" } }));
    stubFetch(fetchMock);
    await renderReady();
    fillRequiredFields();
    openAdvanced();

    // The shop types mean nothing on their own, so they stay out of the way.
    expect(screen.queryByRole("group", { name: "想逛哪些店？（可複選）" })).toBeNull();
    fireEvent.click(screen.getByRole("button", { name: "購物" }));
    const shops = screen.getByRole("group", { name: "想逛哪些店？（可複選）" });
    fireEvent.click(within(shops).getByRole("button", { name: "藥妝" }));
    fireEvent.click(within(shops).getByRole("button", { name: "電器／3C" }));
    expect(within(shops).getByRole("button", { name: "藥妝" }).getAttribute("aria-pressed")).toBe("true");

    submit();

    await waitFor(() => expect(push).toHaveBeenCalledWith("/trips/trip-2"));
    const request = JSON.parse(String((fetchMock.mock.calls[0][1] as RequestInit).body));
    expect(request.preferences.interests).toContain("shopping");
    expect(request.preferences.shop_themes).toEqual(["drugstore", "electronics"]);
  });

  it("forgets the shop types when 購物 is switched off", async () => {
    const fetchMock = vi.fn().mockResolvedValue(new Response(JSON.stringify({ id: "trip-3" }), { status: 201, headers: { "Content-Type": "application/json" } }));
    stubFetch(fetchMock);
    await renderReady();
    fillRequiredFields();
    openAdvanced();

    fireEvent.click(screen.getByRole("button", { name: "購物" }));
    fireEvent.click(within(screen.getByRole("group", { name: "想逛哪些店？（可複選）" })).getByRole("button", { name: "藥妝" }));
    // Turning the interest off hides the chips; a hidden chip that stayed selected
    // would quietly steer the itinerary.
    fireEvent.click(screen.getByRole("button", { name: "購物" }));
    expect(screen.queryByRole("group", { name: "想逛哪些店？（可複選）" })).toBeNull();

    submit();

    await waitFor(() => expect(push).toHaveBeenCalledWith("/trips/trip-3"));
    const request = JSON.parse(String((fetchMock.mock.calls[0][1] as RequestInit).body));
    expect(request.preferences.interests).not.toContain("shopping");
    expect(request.preferences.shop_themes).toEqual([]);
  });
});
