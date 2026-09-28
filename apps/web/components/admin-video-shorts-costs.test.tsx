import { fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { ShortsCosts } from "./admin-video-shorts-costs";

const budget = {
  period_start: "2026-10-04T16:00:00Z", period_end: "2026-11-03T16:00:00Z", spent_ntd: 1234.5, reserved_ntd: 90, unknown: 1, limit_ntd: 3000, soft_ntd: 2400,
  total_start: "2026-10-04T16:00:00Z", total_spent_ntd: 1234.5, total_limit_ntd: 9000, paid_work_allowed: false,
  reason: "有 1 筆花費還不知道金額，付費工作先停；補上金額後會繼續",
};
const items = [
  { id: "11111111-1111-4111-8111-111111111111", occurred_at: "2026-10-06T03:00:00Z", project_slug: "receipt-total", category: "narration", amount: 0.009, currency: "USD", fx_rate: 32.5, amount_ntd: 0.29, status: "confirmed", source: "auto", units: { seconds: 40 }, note: null, created_at: "2026-10-06T03:00:00Z" },
  { id: "22222222-2222-4222-8222-222222222222", occurred_at: "2026-10-07T03:00:00Z", project_slug: null, category: "tool", amount: null, currency: "USD", fx_rate: null, amount_ntd: null, status: "unknown", source: "manual", units: null, note: "還沒收到帳單", created_at: "2026-10-07T03:00:00Z" },
  { id: "33333333-3333-4333-8333-333333333333", occurred_at: "2026-10-08T03:00:00Z", project_slug: "drama-cut", category: "image", amount: 0.134, currency: "USD", fx_rate: 32.5, amount_ntd: 4.36, status: "reserved", source: "auto", units: null, note: null, created_at: "2026-10-08T03:00:00Z" },
];
const periods = [
  { start: "2026-10-04T16:00:00Z", end: "2026-11-03T16:00:00Z", spent_ntd: 1234.5, reserved_ntd: 90, unknown: 1, lines: 3 },
  { start: "2026-11-03T16:00:00Z", end: "2026-12-03T16:00:00Z", spent_ntd: 0, reserved_ntd: 0, unknown: 0, lines: 0 },
  { start: "2026-12-03T16:00:00Z", end: "2027-01-02T16:00:00Z", spent_ntd: 0, reserved_ntd: 0, unknown: 0, lines: 0 },
];

type Call = { url: string; method: string; body: unknown };

function stubFetch(refuse?: { status: number; detail: string }) {
  const calls: Call[] = [];
  vi.stubGlobal("fetch", vi.fn((input: RequestInfo | URL, init?: RequestInit) => {
    const call = { url: String(input), method: init?.method ?? "GET", body: init?.body ? JSON.parse(String(init.body)) : undefined };
    calls.push(call);
    if (call.method !== "GET" && refuse) return Promise.resolve(Response.json({ code: "video_shorts_rate_unavailable", detail: refuse.detail }, { status: refuse.status }));
    if (call.method === "DELETE") return Promise.resolve(new Response(null, { status: 204 }));
    if (call.method !== "GET") return Promise.resolve(Response.json(items[1], { status: call.method === "POST" ? 201 : 200 }));
    return Promise.resolve(Response.json({ items, budget, periods }));
  }));
  return calls;
}

const writes = (calls: Call[]) => calls.filter((call) => call.method !== "GET");

afterEach(() => vi.unstubAllGlobals());

describe("ShortsCosts", () => {
  it("shows where the thirty days stand, the three periods and every line", async () => {
    stubFetch();
    render(<ShortsCosts canManage onChanged={vi.fn()} />);
    const summary = await screen.findByRole("region", { name: "這 30 天" });
    expect(summary.textContent).toContain("付費工作已停");
    expect(summary.textContent).toContain("有 1 筆花費還不知道金額");
    expect(summary.textContent).toContain("已花 · NT$1,235");
    expect(summary.textContent).toContain("30 天上限 · NT$3,000");
    expect(summary.textContent).toContain("NT$1,235／NT$9,000");
    expect(within(screen.getByRole("region", { name: "每 30 天" })).getAllByRole("listitem")).toHaveLength(3);
    const rows = within(screen.getByRole("table", { name: "帳目" })).getAllByRole("row").slice(1);
    expect(rows).toHaveLength(3);
    expect(rows[0].textContent).toContain("旁白");
    expect(rows[0].textContent).toContain("0.009 USD");
    expect(rows[0].textContent).toContain("匯率 32.5");
    expect(rows[0].textContent).toContain("自動");
    // A line nobody knows the amount of shows no amount, not a zero.
    expect(rows[1].textContent).toContain("不知道金額");
    expect(rows[1].textContent).not.toContain("NT$0");
    expect(rows[2].textContent).toContain("已預留");
  });

  it("enters a line with its amount, or as unknown without one", async () => {
    const calls = stubFetch();
    const onChanged = vi.fn();
    render(<ShortsCosts canManage onChanged={onChanged} />);
    const form = await screen.findByRole("form", { name: "補一筆" });
    const add = within(form).getByRole("button", { name: "記下這一筆" });
    expect(add).toHaveProperty("disabled", true);
    fireEvent.change(within(form).getByLabelText("金額"), { target: { value: "20" } });
    fireEvent.change(within(form).getByLabelText("幣別"), { target: { value: "usd" } });
    fireEvent.change(within(form).getByLabelText("備註"), { target: { value: " 訂閱 " } });
    fireEvent.click(add);
    await waitFor(() => expect(writes(calls)).toHaveLength(1));
    expect(writes(calls)[0].url).toContain("/admin/video-shorts/costs");
    expect(writes(calls)[0].body).toEqual({ category: "subscription", status: "confirmed", amount: "20", currency: "USD", note: "訂閱" });
    await waitFor(() => expect(onChanged).toHaveBeenCalledTimes(1));

    fireEvent.change(within(form).getByLabelText("類別"), { target: { value: "tool" } });
    fireEvent.click(within(form).getByLabelText("還不知道金額"));
    expect(within(form).getByLabelText("金額")).toHaveProperty("disabled", true);
    fireEvent.click(add);
    await waitFor(() => expect(writes(calls)).toHaveLength(2));
    expect(writes(calls)[1].body).toEqual({ category: "tool", status: "unknown", currency: "USD" });
  });

  it("does not send an amount, a currency or a Short that cannot be one", async () => {
    stubFetch();
    render(<ShortsCosts canManage onChanged={vi.fn()} />);
    const form = await screen.findByRole("form", { name: "補一筆" });
    const add = within(form).getByRole("button", { name: "記下這一筆" });
    fireEvent.change(within(form).getByLabelText("金額"), { target: { value: "-5" } });
    expect(add).toHaveProperty("disabled", true);
    fireEvent.change(within(form).getByLabelText("金額"), { target: { value: "5" } });
    expect(add).toHaveProperty("disabled", false);
    fireEvent.change(within(form).getByLabelText("幣別"), { target: { value: "NT" } });
    expect(add).toHaveProperty("disabled", true);
    fireEvent.change(within(form).getByLabelText("幣別"), { target: { value: "TWD" } });
    fireEvent.change(within(form).getByLabelText("哪一支 Shorts（選填）"), { target: { value: "Not A Slug" } });
    expect(add).toHaveProperty("disabled", true);
  });

  it("gives an unknown line its amount and removes a line the owner entered", async () => {
    const calls = stubFetch();
    const confirm = vi.spyOn(window, "confirm").mockReturnValue(true);
    render(<ShortsCosts canManage onChanged={vi.fn()} />);
    const rows = within(await screen.findByRole("table", { name: "帳目" })).getAllByRole("row").slice(1);
    expect(within(rows[0]).queryByRole("button")).toBeNull();
    const fill = within(rows[1]).getByRole("button", { name: "補上" });
    expect(fill).toHaveProperty("disabled", true);
    fireEvent.change(within(rows[1]).getByLabelText("補上金額（USD）"), { target: { value: "12.5" } });
    fireEvent.click(fill);
    await waitFor(() => expect(writes(calls)).toHaveLength(1));
    expect(writes(calls)[0]).toMatchObject({ method: "PATCH", body: { status: "confirmed", amount: "12.5" } });
    expect(writes(calls)[0].url).toContain("/admin/video-shorts/costs/22222222-2222-4222-8222-222222222222");
    fireEvent.click(within(rows[1]).getByRole("button", { name: "刪掉" }));
    await waitFor(() => expect(writes(calls)).toHaveLength(2));
    expect(writes(calls)[1]).toMatchObject({ method: "DELETE" });
    expect(confirm).toHaveBeenCalledOnce();
    confirm.mockRestore();
  });

  it("says what the server said when a line is refused", async () => {
    stubFetch({ status: 409, detail: "查不到 EUR 的匯率，請自己填" });
    render(<ShortsCosts canManage onChanged={vi.fn()} />);
    const form = await screen.findByRole("form", { name: "補一筆" });
    fireEvent.change(within(form).getByLabelText("金額"), { target: { value: "5" } });
    fireEvent.click(within(form).getByRole("button", { name: "記下這一筆" }));
    expect((await within(form).findByRole("alert")).textContent).toBe("沒有記下：查不到 EUR 的匯率，請自己填");
  });

  it("lets a reader read the ledger and enter nothing", async () => {
    const calls = stubFetch();
    render(<ShortsCosts canManage={false} onChanged={vi.fn()} />);
    await screen.findByRole("table", { name: "帳目" });
    expect(screen.queryByRole("form", { name: "補一筆" })).toBeNull();
    expect(screen.queryByRole("button", { name: "補上" })).toBeNull();
    expect(screen.queryByRole("button", { name: "刪掉" })).toBeNull();
    expect(writes(calls)).toHaveLength(0);
  });
});
