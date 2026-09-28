import { fireEvent, render, screen, within } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { blankReason, type ShortMetrics } from "./admin-video-shorts-data";
import { ShortsMetrics } from "./admin-video-shorts-metrics";

// The clock stands ten days after the first Short went public: every window of it has closed.
const NOW = "2026-10-15T12:00:00Z";
const snapshot = (period: string, views: number | null, likes: number | null, comments: number | null, captured_at: string, source = "data_api") => ({ period, source, captured_at, views, likes, comments });
const items: ShortMetrics[] = [
  {
    slug: "receipt-total", title: "AI 真的可以算對發票嗎", line: "lab", series: "daily", youtube_video_id: "ShortVid001", published_at: "2026-10-05T11:30:00Z", removed_at: null,
    snapshots: [snapshot("d1", 1204, 31, 4, "2026-10-06T12:00:00Z"), snapshot("d7", 98765, null, 12, "2026-10-12T12:00:00Z"), snapshot("now", 120345, null, 15, "2026-10-15T08:00:00Z")] as ShortMetrics["snapshots"],
  },
  {
    slug: "menu-photo", title: "菜單翻譯", line: "cut", series: "ai-model-choice", youtube_video_id: "ShortVid002", published_at: "2026-10-14T11:30:00Z", removed_at: null,
    snapshots: [],
  },
  {
    slug: "taken-down", title: "已經拿掉的", line: "lab", series: "daily", youtube_video_id: "ShortVid003", published_at: "2026-10-13T11:30:00Z", removed_at: "2026-10-14T09:00:00Z",
    snapshots: [snapshot("now", 0, 0, 0, "2026-10-13T12:00:00Z")] as ShortMetrics["snapshots"],
  },
];

function stubFetch(body: unknown, status = 200) {
  const calls: string[] = [];
  vi.stubGlobal("fetch", vi.fn((input: RequestInfo | URL) => {
    calls.push(String(input));
    return Promise.resolve(Response.json(body, { status }));
  }));
  return calls;
}

const cell = (row: HTMLElement, period: string) => row.querySelector(`td[data-period="${period}"]`) as HTMLElement;

afterEach(() => {
  vi.unstubAllGlobals();
  vi.useRealTimers();
});

describe("why a window has no number", () => {
  const published = "2026-10-05T11:30:00Z";
  const at = (hours: number) => Date.parse(published) + hours * 60 * 60 * 1000;

  it("is that its time has not come, that it is open, or that it closed unread", () => {
    const short = { published_at: published, removed_at: null };
    expect(blankReason("d1", short, at(23.9))).toBe("early");
    expect(blankReason("d1", short, at(24))).toBe("waiting");
    expect(blankReason("d1", short, at(47.9))).toBe("waiting");
    expect(blankReason("d1", short, at(48))).toBe("missed");
    expect(blankReason("d3", short, at(71))).toBe("early");
    expect(blankReason("d3", short, at(72))).toBe("waiting");
    expect(blankReason("d3", short, at(96))).toBe("missed");
    expect(blankReason("d7", short, at(7 * 24 - 1))).toBe("early");
    expect(blankReason("d7", short, at(8 * 24))).toBe("waiting");
    expect(blankReason("d7", short, at(9 * 24))).toBe("missed");
    expect(blankReason("now", short, at(1))).toBe("waiting");
    expect(blankReason("d1", { published_at: null }, at(100))).toBe("early");
  });

  it("is that the Short was taken down, for every window that had not closed by then", () => {
    // Found gone sixty hours after it went public: day 1 had closed, day 3 and 7 had not.
    const short = { published_at: published, removed_at: new Date(at(60)).toISOString() };
    for (const now of [at(61), at(30 * 24)]) {
      expect(blankReason("d1", short, now)).toBe("missed");
      expect(blankReason("d3", short, now)).toBe("removed");
      expect(blankReason("d7", short, now)).toBe("removed");
      expect(blankReason("now", short, now)).toBe("removed");
    }
    expect(blankReason("d1", { published_at: null, removed_at: short.removed_at }, at(61))).toBe("removed");
  });
});

describe("ShortsMetrics", () => {
  it("shows every number as YouTube gave it, with where it came from and when it was read", async () => {
    vi.useFakeTimers({ now: new Date(NOW), toFake: ["Date"] });
    const calls = stubFetch({ items });
    render(<ShortsMetrics onOpenVideo={vi.fn()} />);
    const row = (await screen.findByRole("rowheader", { name: /AI 真的可以算對發票嗎/ })).closest("tr") as HTMLElement;
    expect(calls).toEqual([expect.stringContaining("/admin/video-shorts/metrics")]);
    expect(row.textContent).toContain("實測");
    const first = cell(row, "d1");
    expect(first.textContent).toContain("1,204");
    expect(first.textContent).toContain("31");
    expect(first.textContent).toContain("YouTube Data API");
    expect(first.textContent).toContain("讀取");
    // The likes are hidden on the channel: the cell says so instead of showing a zero.
    const week = cell(row, "d7");
    expect(week.textContent).toContain("98,765");
    expect(within(week).getByText("YouTube 沒有提供")).toBeTruthy();
    expect(cell(row, "now").textContent).toContain("120,345");
    expect(cell(row, "d3").textContent).toBe("沒有在時間窗內讀到");
  });

  it("leaves a window empty and says why", async () => {
    vi.useFakeTimers({ now: new Date(NOW), toFake: ["Date"] });
    stubFetch({ items });
    render(<ShortsMetrics onOpenVideo={vi.fn()} />);
    const row = (await screen.findByRole("rowheader", { name: /菜單翻譯/ })).closest("tr") as HTMLElement;
    // Public for a day and half an hour: day 1 is open, the others have not come.
    expect(cell(row, "d1").textContent).toBe("等下一次讀取");
    expect(cell(row, "d3").textContent).toBe("時間還沒到");
    expect(cell(row, "d7").textContent).toBe("時間還沒到");
    expect(cell(row, "now").textContent).toBe("等下一次讀取");
  });

  it("marks a Short that was taken down and opens one from its row", async () => {
    vi.useFakeTimers({ now: new Date(NOW), toFake: ["Date"] });
    stubFetch({ items });
    const onOpenVideo = vi.fn();
    render(<ShortsMetrics onOpenVideo={onOpenVideo} />);
    const header = await screen.findByRole("rowheader", { name: /已經拿掉的/ });
    expect(header.textContent).toContain("已下架");
    // Nothing of it is read again: no cell promises a number that will not come.
    const row = header.closest("tr") as HTMLElement;
    expect(cell(row, "now").textContent).toContain("讀取");
    for (const period of ["d1", "d3", "d7"]) expect(cell(row, period).textContent).toBe("已下架，不再讀取");
    expect(row.textContent).not.toMatch(/時間還沒到|等下一次讀取/);
    fireEvent.click(within(header).getByRole("button", { name: "打開這支" }));
    expect(onOpenVideo).toHaveBeenCalledWith("taken-down");
  });

  it("makes nothing of the numbers: no sum, no average, no rate, no rank", async () => {
    vi.useFakeTimers({ now: new Date(NOW), toFake: ["Date"] });
    stubFetch({ items });
    render(<ShortsMetrics onOpenVideo={vi.fn()} />);
    const table = await screen.findByRole("table", { name: "成效" });
    expect([...table.querySelectorAll("thead th")].map((header) => header.textContent)).toEqual(["Shorts", "第 1 天", "第 3 天", "第 7 天", "最新"]);
    expect(table.querySelectorAll("tfoot").length).toBe(0);
    expect(table.textContent).not.toMatch(/%|合計|總計|平均|排名|分數/);
    // 1,204 + 98,765 + 120,345 and the like appear nowhere.
    for (const total of ["219,110", "220,314", "120,376"]) expect(table.textContent).not.toContain(total);
    expect(screen.getByText(/不顯示任何本站自己算的分數、排名或比率/)).toBeTruthy();
  });

  it("says so when nothing is public yet, and when the numbers cannot be read", async () => {
    stubFetch({ items: [] });
    const { unmount } = render(<ShortsMetrics onOpenVideo={vi.fn()} />);
    expect(await screen.findByText("還沒有公開的 Shorts")).toBeTruthy();
    unmount();
    stubFetch({ code: "forbidden", detail: "沒有權限" }, 403);
    render(<ShortsMetrics onOpenVideo={vi.fn()} />);
    expect((await screen.findByRole("alert")).textContent).toContain("沒有權限");
  });
});
