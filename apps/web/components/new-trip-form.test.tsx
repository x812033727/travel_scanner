import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { NewTripForm } from "./new-trip-form";

const { push } = vi.hoisted(() => ({ push: vi.fn() }));
vi.mock("next/navigation", () => ({ useRouter: () => ({ push }) }));
vi.mock("./place-picker", () => ({
  PlacePicker: ({ value, onTextChange }: { value: string; onTextChange: (value: string) => void }) => (
    <input aria-label="目的地" value={value} onChange={(event) => onTextChange(event.target.value)} />
  ),
}));

function fillRequiredFields() {
  fireEvent.change(screen.getByLabelText("旅程名稱"), { target: { value: " 東京五日賞楓 " } });
  fireEvent.change(screen.getByLabelText("目的地"), { target: { value: " 東京 " } });
  fireEvent.change(screen.getByLabelText("開始日期"), { target: { value: "2026-11-10" } });
  fireEvent.change(screen.getByLabelText("結束日期"), { target: { value: "2026-11-15" } });
}

describe("NewTripForm", () => {
  beforeEach(() => push.mockReset());
  afterEach(() => vi.unstubAllGlobals());

  it("submits normalized blank-trip fields and opens the editor", async () => {
    const fetchMock = vi.fn().mockResolvedValue(new Response(JSON.stringify({ id: "trip-1" }), {
      status: 201,
      headers: { "Content-Type": "application/json" },
    }));
    vi.stubGlobal("fetch", fetchMock);
    render(<NewTripForm />);
    fillRequiredFields();
    fireEvent.click(screen.getByRole("button", { name: /建立空白行程/ }));

    await waitFor(() => expect(push).toHaveBeenCalledWith("/trips/trip-1"));
    const request = JSON.parse(String((fetchMock.mock.calls[0][1] as RequestInit).body));
    expect(request).toEqual({
      source: "blank",
      name: "東京五日賞楓",
      destination_name: "東京",
      destination_place_id: null,
      start_date: "2026-11-10",
      end_date: "2026-11-15",
      route_preference: "FEWER_TRANSFERS",
    });
  });

  it("shows a readable API validation message", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(new Response(JSON.stringify({
      detail: [{ type: "missing", loc: ["body", "plan_id"], msg: "Field required" }],
    }), { status: 422, headers: { "Content-Type": "application/json" } })));
    render(<NewTripForm />);
    fillRequiredFields();
    fireEvent.click(screen.getByRole("button", { name: /建立空白行程/ }));

    const alert = await screen.findByRole("alert");
    expect(alert.textContent).toContain("行程方案：必填");
    expect(alert.textContent).not.toContain("[object Object]");
  });
});
