import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { AdminNewsEditorial } from "./admin-news-editorial";
import { newsEditorialCopy } from "@/lib/news-editorial";

const state = vi.hoisted(() => ({ locale: "zh-TW", api: vi.fn() }));
vi.mock("next-intl", () => ({ useLocale: () => state.locale }));
vi.mock("@/lib/api", () => ({ api: state.api }));
vi.mock("@/i18n/navigation", () => ({ Link: ({ children, ...props }: React.AnchorHTMLAttributes<HTMLAnchorElement>) => <a {...props}>{children}</a> }));
afterEach(() => { state.locale = "zh-TW"; vi.clearAllMocks(); });
const report = { enabled: true, coverage_days: 90, interval_days: 7, daily_limit: 20,
  eligible_count: 101, due_count: 70, total_count: 101, page: 1, pages: 5, items: [{ candidate_id: "00000000-0000-4000-8000-000000000123", title: "Example source update",
    published_at: null, checked_at: "2026-11-10T12:00:00Z", status: "changed",
    review_due: false, validity_expired: false }] };

describe("published news source review", () => {
  it("shows bounded coverage and a real published-candidate review link", async () => {
    state.api.mockResolvedValue(report);
    render(<AdminNewsEditorial />);
    fireEvent.click(screen.getByText(newsEditorialCopy("zh-TW").title));
    const link = await screen.findByRole("link", { name: "Example source update" });
    expect(link.getAttribute("href")).toBe("/admin/news?tab=review&queue=published&candidate=00000000-0000-4000-8000-000000000123");
    expect(screen.getByText(/範圍內 101 篇/).textContent).toContain("待檢查 70 篇");
    expect(screen.getByText(/涵蓋近 90 天/).textContent).toContain("手動匯入");
    expect(screen.getAllByText(newsEditorialCopy("zh-TW").changed).length).toBeGreaterThan(0);
  });

  it("isolates endpoint failure and permits a read-only reload", async () => {
    state.api.mockRejectedValueOnce(new Error("not available")).mockResolvedValue(report);
    render(<AdminNewsEditorial />);
    fireEvent.click(screen.getByText(newsEditorialCopy("zh-TW").title));
    await waitFor(() => expect(screen.getByRole("status").textContent).toContain(newsEditorialCopy("zh-TW").unavailable));
    fireEvent.click(screen.getByRole("button", { name: newsEditorialCopy("zh-TW").reload }));
    await screen.findByRole("link", { name: "Example source update" });
    expect(state.api).toHaveBeenLastCalledWith("/admin/news/freshness?view=all&page=1", expect.objectContaining({ signal: expect.any(AbortSignal) }));
  });

  it.each(["en", "ja", "ko", "zh-TW", "zh-CN"])("labels unknown results accurately in %s", async (locale) => {
    state.locale = locale;
    state.api.mockResolvedValue({ ...report, enabled: false, items: [{ ...report.items[0], status: "unverified" }] });
    render(<AdminNewsEditorial />);
    const copy = newsEditorialCopy(locale);
    fireEvent.click(screen.getByText(copy.title));
    await waitFor(() => expect(screen.getByText(copy.unverified)).not.toBeNull());
    expect(screen.getByText(copy.disabled)).not.toBeNull();
    expect(screen.queryByText(copy.expired)).toBeNull();
  });

  it("requests due rows and the next page rather than hiding them behind recent checks", async () => {
    state.api.mockResolvedValue(report);
    render(<AdminNewsEditorial />);
    fireEvent.click(screen.getByText(newsEditorialCopy("zh-TW").title));
    await screen.findByRole("link", { name: "Example source update" });
    fireEvent.change(screen.getByRole("combobox"), { target: { value: "due" } });
    await waitFor(() => expect(state.api).toHaveBeenLastCalledWith("/admin/news/freshness?view=due&page=1", expect.anything()));
    await screen.findByRole("link", { name: "Example source update" });
    fireEvent.click(screen.getByRole("button", { name: newsEditorialCopy("zh-TW").next }));
    await waitFor(() => expect(state.api).toHaveBeenLastCalledWith("/admin/news/freshness?view=due&page=2", expect.anything()));
  });
});
