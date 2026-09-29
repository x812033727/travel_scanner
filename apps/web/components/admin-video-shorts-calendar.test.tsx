import { fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { ShortsCalendar } from "./admin-video-shorts-calendar";
import { addDays, dayIn, localInput, type Slot, zonedInstant } from "./admin-video-shorts-data";

const TAIPEI = "Asia/Taipei";
const slot = (fields: Partial<Slot> & Pick<Slot, "id" | "starts_at" | "local_date" | "local_time" | "status">): Slot => ({
  phase: 1, line: null, series: null, topic_slug: null, project_slug: null, project_title: null, project_line: null, youtube_video_id: null, locked_at: null, note: null, ...fields,
});
const slots: Slot[] = [
  slot({ id: "11111111-1111-4111-8111-111111111111", starts_at: "2026-10-05T11:30:00Z", local_date: "2026-10-05", local_time: "19:30", status: "assigned", project_slug: "receipt-total", project_title: "AI 真的可以算對發票嗎", project_line: "lab" }),
  slot({ id: "22222222-2222-4222-8222-222222222222", starts_at: "2026-10-06T11:30:00Z", local_date: "2026-10-06", local_time: "19:30", status: "open" }),
  slot({ id: "33333333-3333-4333-8333-333333333333", starts_at: "2026-10-07T04:30:00Z", local_date: "2026-10-07", local_time: "12:30", status: "skipped", note: "連假" }),
  slot({ id: "44444444-4444-4444-8444-444444444444", starts_at: "2026-10-07T11:30:00Z", local_date: "2026-10-07", local_time: "19:30", status: "scheduled", project_slug: "menu-photo", project_title: "菜單翻譯", project_line: "lab", youtube_video_id: "ShortVid001" }),
];
const library = [
  { slug: "invoice-scan", title: "掃描發票", stage: "publish", checklist: [], youtube_video_id: null, last_synced_at: "2026-10-01T00:00:00Z", pending: 0, format: "shorts", shorts_line: "cut", shorts_state: "library" },
  { slug: "receipt-total", title: "AI 真的可以算對發票嗎", stage: "publish", checklist: [], youtube_video_id: null, last_synced_at: "2026-10-01T00:00:00Z", pending: 0, format: "shorts", shorts_line: "lab", shorts_state: "slotted" },
  { slug: "in-the-making", title: "還在做", stage: "final", checklist: [], youtube_video_id: null, last_synced_at: "2026-10-01T00:00:00Z", pending: 0, format: "shorts", shorts_line: "lab", shorts_state: "making" },
];

type Call = { url: string; method: string; body: unknown };

function stubFetch(answer: (call: Call) => Response | undefined = () => undefined) {
  const calls: Call[] = [];
  vi.stubGlobal("fetch", vi.fn((input: RequestInfo | URL, init?: RequestInit) => {
    const call = { url: String(input), method: init?.method ?? "GET", body: init?.body ? JSON.parse(String(init.body)) : undefined };
    calls.push(call);
    const given = answer(call);
    if (given) return Promise.resolve(given);
    if (call.method === "PATCH") return Promise.resolve(Response.json(slots[0]));
    if (call.url.includes("/admin/video-shorts/slots")) return Promise.resolve(Response.json({ timezone: TAIPEI, slots }));
    return Promise.resolve(Response.json(library));
  }));
  return calls;
}

const patches = (calls: Call[]) => calls.filter((call) => call.method === "PATCH");
/** A slot's controls are folded away until asked for. */
const unfold = (card: HTMLElement) => fireEvent.click(within(card).getByText("調整這一格", { selector: "summary" }));

function mount(canManage = true) {
  const onChanged = vi.fn();
  const onOpenVideo = vi.fn();
  render(<ShortsCalendar canManage={canManage} onChanged={onChanged} onOpenVideo={onOpenVideo} />);
  return { onChanged, onOpenVideo };
}

afterEach(() => {
  vi.unstubAllGlobals();
  vi.useRealTimers();
  window.history.replaceState(null, "", "/");
});

describe("a slot's time is a time of day in the calendar's zone", () => {
  it("reads what the owner typed in that zone, whatever zone the browser is in", () => {
    expect(zonedInstant("2026-10-05T19:30", TAIPEI)?.toISOString()).toBe("2026-10-05T11:30:00.000Z");
    expect(zonedInstant("2026-10-05T19:30", "Asia/Tokyo")?.toISOString()).toBe("2026-10-05T10:30:00.000Z");
    expect(zonedInstant("2026-10-05T19:30", "UTC")?.toISOString()).toBe("2026-10-05T19:30:00.000Z");
    // The clocks of California go forward on 2026-03-08 and back on 2026-11-01.
    expect(zonedInstant("2026-03-07T19:30", "America/Los_Angeles")?.toISOString()).toBe("2026-03-08T03:30:00.000Z");
    expect(zonedInstant("2026-03-08T19:30", "America/Los_Angeles")?.toISOString()).toBe("2026-03-09T02:30:00.000Z");
    expect(zonedInstant("2026-11-01T19:30", "America/Los_Angeles")?.toISOString()).toBe("2026-11-02T03:30:00.000Z");
    expect(zonedInstant("19:30", TAIPEI)).toBeNull();
    expect(zonedInstant("2026-10-05T19:30", "Asia/Nowhere")).toBeNull();
  });

  it("rejects nonexistent wall times and keeps the existing fall-back choice", () => {
    expect(zonedInstant("2027-03-14T02:30", "America/Los_Angeles")).toBeNull();
    // Lord Howe advances by half an hour, so a one-hour-only check is insufficient.
    expect(zonedInstant("2026-10-04T02:15", "Australia/Lord_Howe")).toBeNull();
    expect(zonedInstant("2027-03-14T01:30", "America/Los_Angeles")?.toISOString()).toBe("2027-03-14T09:30:00.000Z");
    expect(zonedInstant("2027-03-14T03:30", "America/Los_Angeles")?.toISOString()).toBe("2027-03-14T10:30:00.000Z");
    expect(zonedInstant("2026-11-01T01:30", "America/Los_Angeles")?.toISOString()).toBe("2026-11-01T08:30:00.000Z");
    expect(zonedInstant("2027-02-30T19:30", TAIPEI)).toBeNull();
  });

  it("writes an instant back as that zone's wall clock", () => {
    expect(localInput("2026-10-05T11:30:00Z", TAIPEI)).toBe("2026-10-05T19:30");
    expect(localInput("2026-10-05T16:30:00Z", TAIPEI)).toBe("2026-10-06T00:30");
    expect(localInput("not a time", TAIPEI)).toBe("");
    expect(dayIn(TAIPEI, new Date("2026-10-05T15:59:59Z"))).toBe("2026-10-05");
    expect(dayIn(TAIPEI, new Date("2026-10-05T16:00:00Z"))).toBe("2026-10-06");
    expect(addDays("2026-10-25", 13)).toBe("2026-11-07");
    expect(addDays("2026-03-01", -14)).toBe("2026-02-15");
  });
});

describe("ShortsCalendar", () => {
  it("lists a row a day and a card a slot, two weeks from the day it is asked for", async () => {
    window.history.replaceState(null, "", "/?tab=shorts&from=2026-10-05");
    const calls = stubFetch();
    const { onOpenVideo } = mount();
    const first = await screen.findByRole("listitem", { name: "2026-10-05 19:30" });
    expect(calls[0].url).toContain("/admin/video-shorts/slots?from=2026-10-05&to=2026-10-18");
    expect(first.textContent).toContain("AI 真的可以算對發票嗎");
    expect(first.textContent).toContain("已排影片");
    expect(first.textContent).toContain("實測");
    // An empty slot says it once and what it lacks; one that is not publishing says only that.
    const empty = screen.getByRole("listitem", { name: "2026-10-06 19:30" });
    expect(empty.textContent?.match(/空格/g)).toHaveLength(1);
    expect(empty.textContent).toContain("還沒有排影片");
    const skipped = screen.getByRole("listitem", { name: "2026-10-07 12:30" });
    expect(skipped.textContent).toContain("不發");
    expect(skipped.textContent).toContain("連假");
    expect(skipped.textContent).not.toMatch(/空格|還沒有排影片/);
    expect(screen.getByText("時間是 Asia/Taipei 的當地時間", { exact: false })).toBeTruthy();
    fireEvent.click(within(first).getByRole("button", { name: "打開這支" }));
    expect(onOpenVideo).toHaveBeenCalledWith("receipt-total");
  });

  it("moves through the run two weeks at a time, in the address", async () => {
    window.history.replaceState(null, "", "/?tab=shorts&from=2026-10-05");
    const calls = stubFetch();
    mount();
    await screen.findByRole("listitem", { name: "2026-10-05 19:30" });
    fireEvent.click(screen.getByRole("button", { name: "後兩週" }));
    await waitFor(() => expect(calls.some((call) => call.url.includes("from=2026-10-19&to=2026-11-01"))).toBe(true));
    expect(window.location.search).toContain("from=2026-10-19");
    fireEvent.click(screen.getByRole("button", { name: "前兩週" }));
    await waitFor(() => expect(window.location.search).toContain("from=2026-10-05"));
    fireEvent.click(screen.getByRole("button", { name: "回到今天" }));
    await waitFor(() => expect(window.location.search).not.toContain("from="));
  });

  it("sends one change at a time, the new time read in the calendar's zone", async () => {
    window.history.replaceState(null, "", "/?from=2026-10-05");
    const calls = stubFetch();
    const { onChanged } = mount();
    const card = await screen.findByRole("listitem", { name: "2026-10-05 19:30" });
    unfold(card);
    const time = within(card).getByLabelText("新的時間（Asia/Taipei）") as HTMLInputElement;
    expect(time.value).toBe("2026-10-05T19:30");
    const move = within(card).getByRole("button", { name: "換到這個時間" });
    expect(move).toHaveProperty("disabled", true);
    fireEvent.change(time, { target: { value: "2026-10-05T21:00" } });
    fireEvent.click(move);
    await waitFor(() => expect(patches(calls)).toHaveLength(1));
    expect(patches(calls)[0].url).toContain("/admin/video-shorts/slots/11111111-1111-4111-8111-111111111111");
    expect(patches(calls)[0].body).toEqual({ action: "move", starts_at: "2026-10-05T13:00:00.000Z" });
    await waitFor(() => expect(onChanged).toHaveBeenCalledTimes(1));

    fireEvent.click(within(card).getByRole("button", { name: "抽掉這支" }));
    await waitFor(() => expect(patches(calls)).toHaveLength(2));
    expect(patches(calls)[1].body).toEqual({ action: "clear" });
    fireEvent.click(within(card).getByRole("button", { name: "這格不發" }));
    await waitFor(() => expect(patches(calls)).toHaveLength(3));
    expect(patches(calls)[2].body).toEqual({ action: "skip" });
    fireEvent.change(within(card).getByLabelText("備註"), { target: { value: " 等站主確認 " } });
    fireEvent.click(within(card).getByRole("button", { name: "存備註" }));
    await waitFor(() => expect(patches(calls)).toHaveLength(4));
    expect(patches(calls)[3].body).toEqual({ action: "note", note: "等站主確認" });
  });

  it("offers an empty slot the Shorts that can take it, and a skipped one only its reopening", async () => {
    window.history.replaceState(null, "", "/?from=2026-10-05");
    const calls = stubFetch();
    mount();
    const empty = await screen.findByRole("listitem", { name: "2026-10-06 19:30" });
    unfold(empty);
    const pick = within(empty).getByLabelText("指定一支 Shorts") as HTMLSelectElement;
    await waitFor(() => expect([...pick.options].map((option) => option.value)).toEqual(["", "invoice-scan", "receipt-total"]));
    expect(within(empty).queryByRole("button", { name: "抽掉這支" })).toBeNull();
    const assign = within(empty).getByRole("button", { name: "排進這一格" });
    expect(assign).toHaveProperty("disabled", true);
    fireEvent.change(pick, { target: { value: "invoice-scan" } });
    fireEvent.click(assign);
    await waitFor(() => expect(patches(calls)).toHaveLength(1));
    expect(patches(calls)[0].url).toContain("/slots/22222222-2222-4222-8222-222222222222");
    expect(patches(calls)[0].body).toEqual({ action: "assign", project_slug: "invoice-scan" });

    const skipped = screen.getByRole("listitem", { name: "2026-10-07 12:30" });
    unfold(skipped);
    expect(within(skipped).queryByRole("button", { name: "換到這個時間" })).toBeNull();
    fireEvent.click(within(skipped).getByRole("button", { name: "重新開啟這一格" }));
    await waitFor(() => expect(patches(calls)).toHaveLength(2));
    expect(patches(calls)[1].body).toEqual({ action: "reopen" });
  });

  it("changes nothing of a slot that is on YouTube, and says what the server said when it refuses", async () => {
    window.history.replaceState(null, "", "/?from=2026-10-05");
    stubFetch((call) => (call.method === "PATCH" ? Response.json({ code: "video_shorts_day_full", detail: "那一天已經有 2 格，一天最多 2 支" }, { status: 409 }) : undefined));
    const { onChanged } = mount();
    const fixed = await screen.findByRole("listitem", { name: "2026-10-07 19:30" });
    expect(within(fixed).queryByText("調整這一格")).toBeNull();
    expect(fixed.textContent).toContain("已排程的要先撤回");
    const card = screen.getByRole("listitem", { name: "2026-10-05 19:30" });
    unfold(card);
    fireEvent.click(within(card).getByRole("button", { name: "這格不發" }));
    expect((await within(card).findByRole("alert")).textContent).toBe("沒有改成：那一天已經有 2 格，一天最多 2 支");
    expect(onChanged).not.toHaveBeenCalled();
  });

  it("lets a reader look and change nothing", async () => {
    window.history.replaceState(null, "", "/?from=2026-10-05");
    const calls = stubFetch();
    mount(false);
    const card = await screen.findByRole("listitem", { name: "2026-10-05 19:30" });
    expect(within(card).queryByText("調整這一格")).toBeNull();
    expect(within(card).getByRole("button", { name: "打開這支" })).toBeTruthy();
    expect(screen.queryByText("已排程的要先撤回", { exact: false })).toBeNull();
    expect(calls.some((call) => call.url.includes("/admin/videos"))).toBe(false);
  });

  it("says so when the days have no slots", async () => {
    window.history.replaceState(null, "", "/?from=2027-05-01");
    stubFetch((call) => (call.url.includes("/slots") ? Response.json({ timezone: TAIPEI, slots: [] }) : undefined));
    mount();
    expect(await screen.findByText("這段時間沒有時段")).toBeTruthy();
    expect(screen.getByText("還沒開跑的話，到「Shorts 設定」選第一支公開的日期。")).toBeTruthy();
  });
});
