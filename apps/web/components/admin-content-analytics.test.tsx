import { act, fireEvent, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { contentAnalyticsCopy, isContentAnalyticsReport } from "@/lib/content-analytics";
import { AdminContentAnalytics } from "./admin-content-analytics";

const report = {
  range: "30d", timezone: "Asia/Taipei", available: true, reason: null,
  from: "2026-10-11T00:00:00Z", to: "2026-11-10T00:00:00Z", retention_days: 90,
  window_clipped: false, first_recorded_at: "2026-11-09T00:00:00Z", total_clicks: 7,
  rows: [{ source_path: "/life/news-story", target_path: "/life/next-guide", placement: "related", locale: "zh-TW", clicks: 7 }],
};
afterEach(() => vi.unstubAllGlobals());

describe("continuation analytics", () => {
  it("shows actual click counts and explicit limits with the source and destination", async () => {
    vi.stubGlobal("fetch", vi.fn(async () => new Response(JSON.stringify(report))));
    render(<AdminContentAnalytics range="30d" includeBots={false} />);
    expect((await screen.findByTestId("content-clicks-total")).textContent).toBe("7");
    expect(screen.getByText("/life/news-story")).toBeTruthy();
    expect(screen.getByText("/life/next-guide")).toBeTruthy();
    expect(screen.getByText(/不代表曝光、讀完/)).toBeTruthy();
  });

  it("does not display a fabricated zero for an unavailable 12-month window", async () => {
    vi.stubGlobal("fetch", vi.fn(async () => new Response(JSON.stringify({ ...report, available: false, reason: "raw_window_only", rows: [], total_clicks: 0 }))));
    render(<AdminContentAnalytics range="12m" includeBots={false} />);
    expect(await screen.findByText(/目前沒有 12 個月/)).toBeTruthy();
    expect(screen.queryByTestId("content-clicks-total")).toBeNull();
  });

  it("keeps absent history explicit and labels a clipped retention window", async () => {
    vi.stubGlobal("fetch", vi.fn(async () => new Response(JSON.stringify({ ...report, total_clicks: 0, rows: [], first_recorded_at: null, window_clipped: true }))));
    render(<AdminContentAnalytics range="90d" includeBots={false} />);
    expect(await screen.findByText(/不能據此判斷沒有人/)).toBeTruthy();
    expect(screen.getByText(/超過原始資料保留期限/)).toBeTruthy();
    expect(screen.getByText(/保留資料中最早的續讀點擊: 尚無記錄/)).toBeTruthy();
  });

  it("degrades a failed or legacy response and supports a local retry", async () => {
    const fetchMock = vi.fn().mockResolvedValueOnce(new Response("{}"))
      .mockResolvedValueOnce(new Response(JSON.stringify(report)));
    vi.stubGlobal("fetch", fetchMock);
    render(<AdminContentAnalytics range="30d" includeBots={false} />);
    expect(await screen.findByText(/目前無法取得續讀資料/)).toBeTruthy();
    fireEvent.click(screen.getByRole("button", { name: "重新載入" }));
    expect((await screen.findByTestId("content-clicks-total")).textContent).toBe("7");
  });

  it("does not let an older range overwrite the current one", async () => {
    let finishOld!: (value: Response) => void;
    vi.stubGlobal("fetch", vi.fn().mockImplementationOnce(() => new Promise<Response>(resolve => { finishOld = resolve; }))
      .mockResolvedValueOnce(new Response(JSON.stringify({ ...report, total_clicks: 3 }))));
    const view = render(<AdminContentAnalytics range="30d" includeBots={false} />);
    view.rerender(<AdminContentAnalytics range="7d" includeBots={true} />);
    expect((await screen.findByTestId("content-clicks-total")).textContent).toBe("3");
    await act(async () => finishOld(new Response(JSON.stringify(report))));
    expect(screen.getByTestId("content-clicks-total").textContent).toBe("3");
  });

  it("rejects unsafe report paths and keeps all five dedicated catalogs complete", () => {
    expect(isContentAnalyticsReport(report)).toBe(true);
    expect(isContentAnalyticsReport({ ...report, rows: [{ ...report.rows[0], target_path: "/admin/secrets" }] })).toBe(false);
    const keys = Object.keys(contentAnalyticsCopy("en")).sort();
    for (const locale of ["en", "ja", "ko", "zh-TW", "zh-CN"]) {
      const copy = contentAnalyticsCopy(locale);
      expect(Object.keys(copy).sort()).toEqual(keys);
      expect(Object.values(copy).every(value => typeof value === "string" && value.trim())).toBe(true);
    }
  });
});
