import { fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { NewTripForm } from "./new-trip-form";

const { push } = vi.hoisted(() => ({ push: vi.fn() }));
vi.mock("@/i18n/navigation", () => ({ useRouter: () => ({ push }) }));
vi.mock("./place-picker", () => ({
  PlacePicker: ({ value, onTextChange }: { value: string; onTextChange: (value: string) => void }) => <input aria-label="目的地" value={value} onChange={(event) => onTextChange(event.target.value)} />,
}));

function fillRequiredFields() {
  fireEvent.change(screen.getByLabelText("旅程名稱"), { target: { value: " 東京五日賞楓 " } });
  fireEvent.change(screen.getByLabelText("目的地"), { target: { value: " 東京 " } });
  fireEvent.change(screen.getByLabelText("開始日期"), { target: { value: "2026-11-10" } });
  fireEvent.change(screen.getByLabelText("結束日期"), { target: { value: "2026-11-15" } });
}

function next() {
  fireEvent.click(screen.getByRole("button", { name: /下一步/ }));
}

function reachReview() {
  next(); next(); next();
}

describe("NewTripForm", () => {
  beforeEach(() => push.mockReset());
  afterEach(() => {
    vi.unstubAllGlobals();
    window.sessionStorage.clear();
  });

  it("rejects a start date in the past", () => {
    render(<NewTripForm />);
    fireEvent.change(screen.getByLabelText("旅程名稱"), { target: { value: "回到過去" } });
    fireEvent.change(screen.getByLabelText("目的地"), { target: { value: "東京" } });
    fireEvent.change(screen.getByLabelText("開始日期"), { target: { value: "2020-01-01" } });
    fireEvent.change(screen.getByLabelText("結束日期"), { target: { value: "2020-01-06" } });
    next();
    expect(screen.getByRole("alert").textContent).toContain("開始日期不可早於今天");
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
    vi.stubGlobal("fetch", fetchMock);
    render(<NewTripForm />);
    fillRequiredFields();
    next();
    fireEvent.change(screen.getByLabelText("成人"), { target: { value: "3" } });
    fireEvent.change(screen.getByLabelText("兒童"), { target: { value: "1" } });
    fireEvent.change(screen.getByLabelText("整趟總預算 TWD"), { target: { value: "90000" } });
    fireEvent.click(screen.getByRole("button", { name: "悠閒" }));
    fireEvent.click(screen.getByRole("button", { name: "美食" }));
    next();
    fireEvent.click(screen.getByRole("button", { name: "兩種都接受" }));
    fireEvent.change(screen.getByLabelText("每晚最低 TWD"), { target: { value: "3000" } });
    fireEvent.change(screen.getByLabelText("每晚最高 TWD"), { target: { value: "7000" } });
    fireEvent.change(screen.getByLabelText("最低星級"), { target: { value: "4" } });
    fireEvent.change(screen.getByLabelText("最低評論數"), { target: { value: "100" } });
    next();
    fireEvent.change(screen.getByLabelText("大眾運輸偏好"), { target: { value: "LESS_WALKING" } });
    fireEvent.change(screen.getByLabelText("其他補充"), { target: { value: " 不要一直換飯店 " } });
    const review = within(screen.getByRole("region", { name: "完整行程條件" }));
    expect(review.getByText("每晚住宿預算")).toBeTruthy();
    expect(review.getByText("$3,000～$7,000")).toBeTruthy();
    expect(review.getByText("4 星以上")).toBeTruthy();
    expect(review.getByText("100 則以上")).toBeTruthy();
    expect(review.getByText("少走路")).toBeTruthy();
    expect(screen.getByText(/不會傳送 Email、姓名或帳號識別資料/)).toBeTruthy();
    fireEvent.click(screen.getByRole("button", { name: /交給 AI 排好行程/ }));

    await waitFor(() => expect(push).toHaveBeenCalledWith("/trips/trip-1"));
    expect(window.sessionStorage.getItem("mokaair-new-trip-draft")).toBeNull();
    const request = JSON.parse(String((fetchMock.mock.calls[0][1] as RequestInit).body));
    expect(request).toMatchObject({
      source: "blank", planning_mode: "ai_draft", name: "東京五日賞楓", destination_name: "東京", destination_place_id: null,
      start_date: "2026-11-10", end_date: "2026-11-15", route_preference: "LESS_WALKING",
      routing: { auto_compute: true, default_travel_mode: "transit", default_buffer_minutes: 10 },
      travelers: { adults: 3, children: 1, rooms: 1 },
      preferences: {
        budget_twd: 90000, pace: "relaxed", accepted_property_types: ["hotel", "vacation_rental"],
        hotel_min_nightly_twd: 3000, hotel_max_nightly_twd: 7000, hotel_min_rating: 4,
        hotel_min_review_count: 100, interests: ["food"],
      },
      notes: "不要一直換飯店",
    });
  });

  it("creates a blank manual timeline without automatic route computation", async () => {
    const fetchMock = vi.fn().mockResolvedValue(new Response(JSON.stringify({ id: "manual-trip" }), { status: 201, headers: { "Content-Type": "application/json" } }));
    vi.stubGlobal("fetch", fetchMock);
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
    vi.stubGlobal("fetch", fetchMock);
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
    fireEvent.change(screen.getByLabelText("每晚最低 TWD"), { target: { value: "8000" } });
    fireEvent.change(screen.getByLabelText("每晚最高 TWD"), { target: { value: "3000" } });
    next();
    expect(screen.getByRole("alert").textContent).toContain("最低價格不可高於最高價格");
  });

  it("shows a readable API validation message", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(new Response(JSON.stringify({ detail: [{ type: "missing", loc: ["body", "plan_id"], msg: "Field required" }] }), { status: 422, headers: { "Content-Type": "application/json" } })));
    render(<NewTripForm />);
    fillRequiredFields();
    reachReview();
    fireEvent.click(screen.getByRole("button", { name: /交給 AI 排好行程/ }));
    const alert = await screen.findByRole("alert");
    expect(alert.textContent).toContain("行程方案：必填");
    expect(alert.textContent).not.toContain("[object Object]");
  });
});
