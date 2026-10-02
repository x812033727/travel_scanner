import { render, screen, within } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { ShortsReport } from "./admin-video-shorts-report";

const row = (fields: Record<string, unknown>) => ({
  slug: "receipt-total", title: "AI 真的可以算對發票嗎", youtube_video_id: "abcDEF12345", period: "d7", source: "data_api", captured_at: "2026-10-12T03:00:00Z",
  range_start: null, range_end: null, views: 12345, engaged_views: null, likes: 321, comments: 7, shares: null, subscribers_gained: null,
  avg_view_seconds: null, avg_view_percent: null, stayed_percent: null, ...fields,
});
const newest = {
  id: "r2", week_start: "2026-10-12", provider: "claude_code", model: "claude-opus-5-5", generated_at: "2026-10-19T01:00:00Z", updated_at: "2026-10-19T01:00:00Z",
  body_md: "## 這週\n盲測系列多做一支。<script>alert(1)</script>\n**發票**那支換開場。",
  rows: [
    row({}),
    row({ slug: "menu-photo", title: null, youtube_video_id: "ghiJKL67890", period: "d3", views: 800, likes: 12, comments: 0, avg_view_seconds: 23.4567 }),
    row({ youtube_video_id: "abcDEF12345", period: "d1", source: "analytics_api", range_start: "2026-10-12", range_end: "2026-10-12", views: 400, likes: null, comments: null, avg_view_percent: 71.3 }),
  ],
  plan: [{ starts_at: "2026-10-20T11:30:00Z", topic_slug: "shorts-notes-blind", line: "lab", note: "盲測系列" }, { note: "漫劇先停一週" }],
};
const older = { ...newest, id: "r1", week_start: "2026-10-05", provider: null, model: null, body_md: "第一週。", rows: [], plan: [] };

function stubFetch(items: unknown[]) {
  const calls: string[] = [];
  vi.stubGlobal("fetch", vi.fn(async (input: RequestInfo | URL) => {
    calls.push(String(input));
    return Response.json({ items });
  }));
  return calls;
}

afterEach(() => vi.unstubAllGlobals());

describe("ShortsReport", () => {
  it("shows each week newest first, the model's text as text, and the numbers it cites as YouTube gave them", async () => {
    const calls = stubFetch([newest, older]);
    render(<ShortsReport />);
    const reports = await screen.findAllByRole("article");
    expect(calls[0]).toMatch(/\/api\/travel\/admin\/video-shorts\/reports$/);
    expect(reports.map((each) => each.getAttribute("aria-label"))).toEqual(["2026-10-12 到 2026-10-18 那一週", "2026-10-05 到 2026-10-11 那一週"]);
    const [week] = reports;
    expect(week.textContent).toContain("claude_code claude-opus-5-5，");

    // Plain text: no markup is made from it, the script tag included.
    const body = within(week).getByTestId("shorts-report-body");
    expect(body.textContent).toBe(newest.body_md);
    expect(body.children).toHaveLength(0);
    expect(document.querySelector("script")).toBeNull();

    const table = within(week).getByRole("table");
    const headers = within(table).getAllByRole("columnheader").map((cell) => cell.textContent);
    // A column for each value some row carries, none for the ones nobody reported, and nothing added.
    expect(headers).toEqual(["Shorts", "時間窗", "觀看", "喜歡", "留言", "平均觀看秒數", "平均觀看百分比", "來源與讀取時間"]);
    const cells = within(table).getAllByRole("row").slice(1).map((each) => within(each).getAllByRole("cell").map((cell) => cell.textContent));
    expect(cells[0].slice(0, 6)).toEqual(["第 7 天", "12,345", "321", "7", "—", "—"]);
    expect(cells[0][6]).toMatch(/^YouTube Data API，.+ 讀取$/);
    expect(cells[1].slice(0, 6)).toEqual(["第 3 天", "800", "12", "0", "23.4567", "—"]);
    expect(cells[2].slice(0, 6)).toEqual(["第 1 天2026-10-12 到 2026-10-12", "400", "—", "—", "—", "71.3"]);
    expect(cells[2][6]).toMatch(/^YouTube Analytics API，/);
    expect(within(table).getAllByRole("rowheader").map((cell) => cell.textContent)).toEqual(["AI 真的可以算對發票嗎abcDEF12345", "menu-photoghiJKL67890", "AI 真的可以算對發票嗎abcDEF12345"]);
    // No total, average, rank or score anywhere on the page.
    expect(week.textContent).not.toMatch(/合計|平均觀看數|排名|分數/);

    const plan = within(week).getByRole("region", { name: "下週的排片" });
    const items = within(plan).getAllByRole("listitem").map((each) => each.textContent);
    expect(items[0]).toMatch(/實測 · shorts-notes-blind — 盲測系列$/);
    expect(items[1]).toBe("漫劇先停一週");

    const [, first] = reports;
    expect(first.textContent).toContain("沒有回報模型名稱");
    expect(first.textContent).toContain("這份報告沒有引用數字。");
    expect(first.textContent).toContain("報告沒有寫下週的排片。");
    expect(within(first).queryByRole("table")).toBeNull();
  });

  it("says when there is no report yet", async () => {
    stubFetch([]);
    render(<ShortsReport />);
    expect(await screen.findByText("還沒有每週報告")).toBeTruthy();
  });
});
